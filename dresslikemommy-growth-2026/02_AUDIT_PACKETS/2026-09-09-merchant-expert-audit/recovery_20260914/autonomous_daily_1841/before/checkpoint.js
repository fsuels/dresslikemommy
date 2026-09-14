import { collectCatalog, createAdminReader, SourceError } from './collector.js';
import { buildFeed, sha256 } from './generator.js';
import { runtimeConfig, currentManifest } from './worker.js';
import { publishStreamedResult } from './stream-publish.js';

class CheckpointNeeded extends Error {}
const keyPattern = /^[a-z]{2}-[a-z]{2}(?:-[a-z]{2})?$/;
const idPattern = /^[a-f0-9-]{36}$/;
const supplierPattern = /(?:alibaba\.com|aliexpress\.com|1688\.com|taobao\.com|tmall\.com)/i;
function requireValue(value, code) { if (!value) throw new SourceError(code); }
function jobKey(key) { return `merchant/${key}/refresh.json`; }
function body(control) { return { schemaVersion: 1, key: control.key, jobId: control.jobId, revision: control.revision }; }
async function discardJournal(bucket, control) {
  if (typeof bucket.delete === 'function' && control?.journalKey?.startsWith(`merchant/jobs/${control.key}/${control.jobId}/`)) await bucket.delete(control.journalKey).catch(() => {});
}
async function readControl(bucket, key) {
  const object = await bucket.get(jobKey(key));
  if (!object) return { control: null, etag: null };
  let control;
  try { control = JSON.parse(await object.text()); } catch { throw new SourceError('refresh_control_invalid'); }
  requireValue(control.schemaVersion === 1 && control.key === key && idPattern.test(control.jobId) && Number.isSafeInteger(control.revision), 'refresh_control_invalid');
  return { control, etag: object.etag };
}
function configured(env, key) {
  const config = runtimeConfig(env), market = config.markets.find(m => m.key === key && m.enabled);
  requireValue(keyPattern.test(key) && market, 'market_not_enabled');
  requireValue(env.MERCHANT_FEED_BUCKET && env.MERCHANT_REFRESH_QUEUE, 'refresh_bindings_missing');
  return { config, market, bucket: env.MERCHANT_FEED_BUCKET, queue: env.MERCHANT_REFRESH_QUEUE };
}
async function writeControl(bucket, control, beforeEtag) {
  const stored = await bucket.put(jobKey(control.key), JSON.stringify(control), {
    onlyIf: beforeEtag ? { etagMatches: beforeEtag } : { etagDoesNotMatch: '*' },
    httpMetadata: { contentType: 'application/json' },
  });
  requireValue(stored !== null, 'concurrent_refresh_checkpoint');
  return stored;
}

// Cron does only small metadata I/O and sends one small message. All catalog
// parsing/generation runs inside a Queue consumer's documented CPU allowance.
export async function enqueueRefresh(env, key, { now = () => new Date(), randomId = () => crypto.randomUUID() } = {}) {
  const { config, bucket, queue } = configured(env, key);
  const hash = await sha256(JSON.stringify(config)), before = await readControl(bucket, key);
  const time = now(), old = before.control;
  const maxAge = (config.refresh?.maxJobAgeMinutes ?? 120) * 60000;
  if (old?.status === 'RUNNING' && old.configHash === hash && time - Date.parse(old.startedAt) <= maxAge) {
    await queue.send(body(old)); return { resumed: true, jobId: old.jobId };
  }
  if (old?.status === 'COMPLETE' && old.configHash === hash && time - Date.parse(old.completedAt) < (config.refresh?.minRefreshMinutes ?? 60) * 60000) return { skipped: 'recent_complete_refresh' };
  const control = {
    schemaVersion: 1, key, jobId: randomId(), revision: 0, status: 'RUNNING',
    startedAt: time.toISOString(), updatedAt: time.toISOString(), configHash: hash, journalKey: null,
  };
  requireValue(idPattern.test(control.jobId), 'refresh_job_id_invalid');
  await writeControl(bucket, control, before.etag);
  await queue.send(body(control));
  await discardJournal(bucket, old);
  return { started: true, jobId: control.jobId };
}

function sanitize(data) {
  for (const p of data.products?.nodes || []) if (Array.isArray(p.tags)) p.tags = p.tags.filter(tag => !/https?:\/\//i.test(tag));
  requireValue(!supplierPattern.test(JSON.stringify(data)), 'supplier_reference_in_source');
  return data;
}

// An immutable read journal lets the same fully tested collector resume by
// replaying already completed reads. It never falls back to an older feed.
// Twenty new logical calls mean at most 40 external fetches with the reader's
// one transient retry, below Free's 50 external subrequests per invocation.
export async function consumeRefresh(env, message, { graphql, now = () => new Date(), randomId = () => crypto.randomUUID(), streamOptions = {} } = {}) {
  requireValue(message?.schemaVersion === 1 && keyPattern.test(message.key || '') && idPattern.test(message.jobId || '') && Number.isSafeInteger(message.revision) && message.revision >= 0, 'refresh_message_invalid');
  const { config, market, bucket, queue } = configured(env, message.key);
  const before = await readControl(bucket, message.key), control = before.control;
  if (!control || control.jobId !== message.jobId || control.status !== 'RUNNING') return { ignored: 'superseded_or_complete_message' };
  if (message.revision < control.revision) {
    // If a checkpoint committed but sending its continuation failed, redelivery
    // repairs that gap immediately. CAS still makes duplicate work harmless.
    await queue.send(body(control)); return { resumed: 'latest_checkpoint_requeued' };
  }
  requireValue(message.revision === control.revision, 'future_refresh_message');
  const maxAge = (config.refresh?.maxJobAgeMinutes ?? 120) * 60000;
  const fail = async code => {
    const failed = { ...control, status: 'FAILED', failedAt: now().toISOString(), code };
    await writeControl(bucket, failed, before.etag);
    await bucket.put(`merchant/${market.key}/status.json`, JSON.stringify({ ok: false, failedAt: failed.failedAt, jobId: control.jobId, code }));
    return { failed: true, code };
  };
  if (control.configHash !== await sha256(JSON.stringify(config))) return fail('refresh_config_changed');
  if (now() - Date.parse(control.startedAt) > maxAge) return fail('refresh_expired');
  const maxCalls = config.refresh?.maxSourceCallsPerInvocation ?? 20;
  requireValue(Number.isSafeInteger(maxCalls) && maxCalls >= 1 && maxCalls <= 20, 'unsafe_refresh_call_budget');
  let journal = { schemaVersion: 1, jobId: control.jobId, entries: [], beforeFeed: null };
  if (control.journalKey) {
    requireValue(control.journalKey.startsWith(`merchant/jobs/${market.key}/${control.jobId}/`), 'refresh_journal_key_invalid');
    const object = await bucket.get(control.journalKey);
    requireValue(object && object.size <= 50000000, 'refresh_journal_missing_or_oversize');
    journal = JSON.parse(await object.text());
    requireValue(journal.schemaVersion === 1 && journal.jobId === control.jobId && Array.isArray(journal.entries) && journal.entries.length <= 10000, 'refresh_journal_invalid');
  } else journal.beforeFeed = await currentManifest(bucket, market.key);
  // A crash after pointer promotion must be idempotent on redelivery.
  const present = await currentManifest(bucket, market.key);
  if (present.manifest?.publisherJobId === control.jobId) {
    await writeControl(bucket, { ...control, status: 'COMPLETE', completedAt: present.manifest.generatedAt, sha256: present.manifest.sha256, rows: present.manifest.rows }, before.etag);
    await discardJournal(bucket, control);
    return { complete: true, recoveredPromotion: true, rows: present.manifest.rows };
  }
  let index = 0, newCalls = 0, firstClock = true;
  const reader = graphql || createAdminReader({ domain: config.storeDomain, token: env.SHOPIFY_ADMIN_ACCESS_TOKEN, apiVersion: config.apiVersion });
  const replayReader = async (query, variables) => {
    const key = await sha256(query + '\n' + JSON.stringify(variables));
    if (index < journal.entries.length) {
      const saved = journal.entries[index++]; requireValue(saved.key === key, 'refresh_replay_mismatch');
      return structuredClone(saved.data);
    }
    if (newCalls >= maxCalls) throw new CheckpointNeeded();
    newCalls++;
    const data = sanitize(await reader(query, variables));
    journal.entries.push({ key, data }); index++;
    requireValue(journal.entries.length <= 10000, 'refresh_request_limit');
    return structuredClone(data);
  };
  let snapshot;
  try {
    snapshot = await collectCatalog(replayReader, config, market, { now: () => {
      if (firstClock) { firstClock = false; return new Date(control.startedAt); }
      return now();
    } });
  } catch (error) {
    if (!(error instanceof CheckpointNeeded)) return fail(error instanceof SourceError ? error.code : 'refresh_source_failed');
    const journalKey = `merchant/jobs/${market.key}/${control.jobId}/${control.revision + 1}-${randomId()}.json`;
    const serialized = JSON.stringify(journal);
    requireValue(new TextEncoder().encode(serialized).byteLength <= 50000000, 'refresh_journal_oversize');
    await bucket.put(journalKey, serialized, { httpMetadata: { contentType: 'application/json' } });
    const next = { ...control, revision: control.revision + 1, journalKey, updatedAt: now().toISOString(), sourceRequests: journal.entries.length };
    await writeControl(bucket, next, before.etag);
    await queue.send(body(next));
    await discardJournal(bucket, control);
    return { checkpointed: true, revision: next.revision, newCalls, sourceRequests: journal.entries.length };
  }
  let result;
  try { result = await buildFeed(snapshot, config, market, { now: now(), previousIds: journal.beforeFeed.manifest?.rowIds || [], materialize: false }); }
  catch (error) { return fail(error instanceof SourceError ? error.code : 'refresh_build_failed'); }
  // Diagnostics and immutable object precede the one atomic current-pointer swap.
  const diagnosticsKey = `merchant/${market.key}/diagnostics/${control.jobId}.json`;
  await bucket.put(diagnosticsKey, JSON.stringify(result.diagnostics), { httpMetadata: { contentType: 'application/json' } });
  if (!result.ok) return fail('feed_validation_failed');
  let manifest;
  try { manifest = await publishStreamedResult(bucket, result, snapshot, market, journal.beforeFeed, { ...streamOptions, publisherJobId: control.jobId }); }
  catch (error) { return fail(error instanceof SourceError ? error.code : 'refresh_publish_failed'); }
  const completed = { ...control, status: 'COMPLETE', completedAt: now().toISOString(), sha256: manifest.sha256, rows: manifest.rows, sourceRequests: journal.entries.length };
  await writeControl(bucket, completed, before.etag);
  await bucket.put(`merchant/${market.key}/status.json`, JSON.stringify({ ok: true, completedAt: completed.completedAt, jobId: control.jobId, sha256: manifest.sha256, rows: manifest.rows, sourceParents: manifest.sourceParents, sourceVariants: manifest.sourceVariants, requests: journal.entries.length, diagnosticsKey }));
  await discardJournal(bucket, control);
  return { complete: true, rows: manifest.rows, newCalls, sourceRequests: journal.entries.length, sha256: manifest.sha256 };
}
