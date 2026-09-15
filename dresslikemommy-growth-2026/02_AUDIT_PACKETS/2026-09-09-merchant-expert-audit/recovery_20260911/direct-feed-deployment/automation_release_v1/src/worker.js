import { collectCatalog, SourceError } from './collector.js';
import { createConfiguredAdminReader } from './admin-reader.js';
import { buildFeed } from './generator.js';

const TSV_TYPE = 'text/tab-separated-values; charset=utf-8';
const PREFIX = 'merchant/';
function json(value, status = 200, headers = {}) {
  return new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...headers } });
}
export function runtimeConfig(env) {
  let config;
  try {
    config = JSON.parse(env.MERCHANT_CONFIG_JSON);
    if (config.eligibilityHoldsExternal === true) {
      if (config.eligibilityHolds !== undefined || typeof env.MERCHANT_ELIGIBILITY_HOLDS_JSON !== 'string') throw new Error();
      delete config.eligibilityHoldsExternal;
      config.eligibilityHolds = JSON.parse(env.MERCHANT_ELIGIBILITY_HOLDS_JSON);
      if (!config.eligibilityHolds || typeof config.eligibilityHolds !== 'object' || Array.isArray(config.eligibilityHolds)) throw new Error();
    } else if (config.eligibilityHoldsExternal !== undefined || env.MERCHANT_ELIGIBILITY_HOLDS_JSON !== undefined) throw new Error();
  } catch { throw new SourceError('feed_config_missing_or_invalid'); }
  if (!Array.isArray(config.markets) || !config.shopId || !config.storeDomain) throw new SourceError('feed_config_missing_or_invalid');
  return config;
}
export async function currentManifest(bucket, marketKey) {
  const object = await bucket.get(`${PREFIX}${marketKey}/current.json`);
  if (!object) return { manifest: null, etag: null };
  let manifest;
  try { manifest = JSON.parse(await object.text()); } catch { throw new SourceError('manifest_invalid'); }
  if (manifest.schemaVersion !== 1 || manifest.market?.key !== marketKey || !/^[a-f0-9]{64}$/.test(manifest.sha256 || '') || !manifest.objectEtag || manifest.objectKey !== `${PREFIX}${marketKey}/${manifest.sha256}.tsv`) throw new SourceError('manifest_invalid');
  return { manifest, etag: object.etag };
}

// The one live write seam: immutable full file first, current pointer last.
// A failed source read/build or competing refresh never publishes partial rows.
export async function publishResult(bucket, result, snapshot, market, before, { publisherJobId = null } = {}) {
  if (!result.ok) throw new SourceError('feed_validation_failed');
  if (!result.diagnostics.returnPolicyLabelsConfirmed) throw new SourceError('native_return_label_not_confirmed');
  const objectKey = `${PREFIX}${market.key}/${result.sha256}.tsv`;
  const stored = await bucket.put(objectKey, result.tsv, { httpMetadata: { contentType: TSV_TYPE }, sha256: result.sha256 });
  return commitStoredResult(bucket, stored, result, snapshot, market, before, { publisherJobId });
}

export async function commitStoredResult(bucket, stored, result, snapshot, market, before, { publisherJobId = null } = {}) {
  if (!result.ok || !result.diagnostics.returnPolicyLabelsConfirmed) throw new SourceError('feed_not_ready_to_publish');
  if (!stored?.etag) throw new SourceError('feed_object_write_failed');
  const objectKey = `${PREFIX}${market.key}/${result.sha256}.tsv`;
  const manifest = {
    schemaVersion: 1, market: { key: market.key, country: market.country, locale: market.locale, currency: market.currency },
    objectKey, objectEtag: stored.etag, sha256: result.sha256, bytes: result.bytes, rows: result.rows.length,
    sourceCompletedAt: snapshot.completedAt, generatedAt: result.diagnostics.generatedAt,
    sourceParents: result.diagnostics.sourceCounts.parents, sourceVariants: result.diagnostics.sourceCounts.variants,
    publisherJobId,
    rowIds: result.rowIds,
    previous: before.manifest ? { objectKey: before.manifest.objectKey, sha256: before.manifest.sha256, sourceCompletedAt: before.manifest.sourceCompletedAt } : null,
  };
  const updated = await bucket.put(`${PREFIX}${market.key}/current.json`, JSON.stringify(manifest), {
    httpMetadata: { contentType: 'application/json' },
    onlyIf: before.etag ? { etagMatches: before.etag } : { etagDoesNotMatch: '*' },
  });
  if (updated === null) throw new SourceError('concurrent_refresh');
  return manifest;
}

export async function refreshMarket(env, marketKey, { graphql, now = () => new Date() } = {}) {
  const config = runtimeConfig(env), market = config.markets.find(m => m.key === marketKey && m.enabled);
  if (!market) throw new SourceError('market_not_enabled');
  if (!env.MERCHANT_FEED_BUCKET) throw new SourceError('feed_bucket_missing');
  const before = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  const reader = graphql || await createConfiguredAdminReader(env, config);
  const snapshot = await collectCatalog(reader, config, market, { now });
  const result = await buildFeed(snapshot, config, market, { now: now(), previousIds: before.manifest?.rowIds || [] });
  if (!result.ok) throw new SourceError('feed_validation_failed');
  const manifest = await publishResult(env.MERCHANT_FEED_BUCKET, result, snapshot, market, before);
  await env.MERCHANT_FEED_BUCKET.put(`${PREFIX}${market.key}/status.json`, JSON.stringify({
    ok: true, completedAt: now().toISOString(), sourceParents: manifest.sourceParents, sourceVariants: manifest.sourceVariants,
    rows: manifest.rows, warningCount: result.diagnostics.warnings.length, excludedParents: result.diagnostics.exclusions.length,
    requests: snapshot.trace.length + 2, sha256: manifest.sha256,
  }));
  return { manifest, diagnostics: result.diagnostics };
}

export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return json({ error: 'method_not_allowed' }, 405, { Allow: 'GET, HEAD' });
    const url = new URL(request.url);
    if (url.pathname === '/health') return json({ ok: true, service: 'merchant-feed-reader' });
    const match = url.pathname.match(/^\/feeds\/([a-z]{2}-[a-z]{2}(?:-[a-z]{2})?)\.tsv$/);
    if (!match) return json({ error: 'not_found' }, 404);
    try {
      const config = runtimeConfig(env), market = config.markets.find(m => m.key === match[1] && m.enabled);
      if (!market) return json({ error: 'market_not_enabled' }, 404);
      if (!env.MERCHANT_FEED_BUCKET) throw new SourceError('feed_bucket_missing');
      const { manifest } = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
      if (!manifest) throw new SourceError('feed_unavailable');
      if (manifest.market.country !== market.country || manifest.market.locale !== market.locale || manifest.market.currency !== market.currency) throw new SourceError('manifest_context_mismatch');
      const age = Date.now() - Date.parse(manifest.sourceCompletedAt);
      if (!Number.isFinite(age) || age < -60000 || age > (config.maxFeedAgeHours ?? 48) * 3600000) throw new SourceError('feed_stale');
      const object = await env.MERCHANT_FEED_BUCKET.get(manifest.objectKey);
      if (!object || object.size > 60000000 || object.size !== manifest.bytes || object.etag !== manifest.objectEtag) throw new SourceError('feed_object_invalid');
      // R2 validated the SHA-256 at promotion. Bind immutable key, ETag and bytes,
      // then stream; a public fetch does not buffer/hash a 17MB feed on Free CPU.
      return new Response(request.method === 'HEAD' ? null : object.body, { status: 200, headers: {
        'Content-Type': TSV_TYPE, 'Cache-Control': 'public, max-age=300', 'X-Content-Type-Options': 'nosniff',
        'Content-Length': String(manifest.bytes), ETag: `"${manifest.sha256}"`,
        'X-DLM-Feed-SHA256': manifest.sha256, 'X-DLM-Feed-Rows': String(manifest.rows),
        'X-DLM-Feed-Country': market.country, 'X-DLM-Feed-Language': market.locale,
        'X-DLM-Feed-Currency': market.currency, 'X-DLM-Feed-Source-Updated': manifest.sourceCompletedAt,
      } });
    } catch (error) { return json({ error: error instanceof SourceError ? error.code : 'feed_unavailable' }, 503); }
  },
  async scheduled(controller, env) {
    const config = runtimeConfig(env);
    const key = config.schedules?.[controller.cron] || (controller.cron === '0 */6 * * *' ? 'us-en' : null);
    if (!key || !config.markets.some(m => m.key === key && m.enabled)) return;
    try { await refreshMarket(env, key); }
    catch (error) {
      const code = error instanceof SourceError ? error.code : 'refresh_failed';
      // Only bounded status metadata; never query payloads, product text or secrets.
      if (env.MERCHANT_FEED_BUCKET) await env.MERCHANT_FEED_BUCKET.put(`${PREFIX}${key}/status.json`, JSON.stringify({ ok: false, failedAt: new Date().toISOString(), code }));
      throw new SourceError(code);
    }
  },
};
