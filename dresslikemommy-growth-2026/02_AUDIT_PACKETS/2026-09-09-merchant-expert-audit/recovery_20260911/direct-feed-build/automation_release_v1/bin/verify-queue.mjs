// Local read-only Shopify exercise of the actual Queue/checkpoint code.
// R2/Queue adapters write only --out; this command never deploys or calls R2.
import fs from 'node:fs/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { Readable, Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { createHash } from 'node:crypto';
import { enqueueRefresh, consumeRefresh } from '../src/checkpoint.js';
import { createAdminReader, SourceError } from '../src/collector.js';
import { streamOptions } from '../test/node-streams.js';

const args = process.argv.slice(2);
function arg(key, fallback = null) { const at = args.indexOf(key); return at < 0 ? fallback : args[at + 1]; }
async function main() {
  const output = arg('--out'); if (!output || !args.includes('--live')) throw new SourceError('explicit_live_and_local_output_required');
  const config = JSON.parse(await fs.readFile(arg('--config', new URL('../config.example.json', import.meta.url)), 'utf8'));
  const key = arg('--market', 'us-en'), root = path.resolve(output, 'local-r2');
  await fs.mkdir(root, { recursive: true });
  const hash = (value, algorithm) => createHash(algorithm).update(value).digest('hex');
  const objectPath = key => {
    const target = path.resolve(root, key);
    if (!target.startsWith(root + path.sep)) throw new SourceError('unsafe_local_object_key');
    return target;
  };
  const bucket = {
    async get(key) {
      const file = objectPath(key); let metadata;
      try { metadata = JSON.parse(await fs.readFile(file + '.metadata.json', 'utf8')); } catch (error) { if (error.code === 'ENOENT') return null; throw error; }
      return { etag: metadata.etag, size: metadata.size,
        get body() { return Readable.toWeb(createReadStream(file)); }, text: () => fs.readFile(file, 'utf8') };
    },
    async put(key, text, options = {}) {
      const file = objectPath(key), before = await this.get(key);
      if (options.onlyIf?.etagMatches && options.onlyIf.etagMatches !== before?.etag) return null;
      if (options.onlyIf?.etagDoesNotMatch === '*' && before) return null;
      await fs.mkdir(path.dirname(file), { recursive: true });
      let metadata;
      if (text instanceof ReadableStream) {
        const md5 = createHash('md5'), sha = createHash('sha256'); let size = 0;
        await pipeline(Readable.fromWeb(text), new Transform({ transform(chunk, encoding, done) {
          size += chunk.length; md5.update(chunk); sha.update(chunk); done(null, chunk);
        } }), createWriteStream(file));
        if (options.sha256 && sha.digest('hex') !== options.sha256) throw new SourceError('local_r2_checksum_mismatch');
        metadata = { etag: md5.digest('hex'), size };
      } else {
        if (options.sha256 && hash(text, 'sha256') !== options.sha256) throw new SourceError('local_r2_checksum_mismatch');
        await fs.writeFile(file, text);
        metadata = { etag: hash(text, 'md5'), size: Buffer.byteLength(text) };
      }
      await fs.writeFile(file + '.metadata.json', JSON.stringify(metadata));
      return metadata;
    },
    async delete(key) {
      await Promise.all([fs.rm(objectPath(key), { force: true }), fs.rm(objectPath(key) + '.metadata.json', { force: true })]);
    },
  };
  const queue = { messages: [], async send(message) { this.messages.push(structuredClone(message)); } };
  const credential = JSON.parse(await fs.readFile(path.join(os.homedir(), '.config/dresslikemommy/admin-api-token.json'), 'utf8'));
  if (credential.store_domain !== config.storeDomain) throw new SourceError('configured_admin_domain_mismatch');
  const authenticated = createAdminReader({ domain: credential.store_domain, token: credential.access_token, apiVersion: config.apiVersion });
  const env = { MERCHANT_CONFIG_JSON: JSON.stringify(config), MERCHANT_FEED_BUCKET: bucket, MERCHANT_REFRESH_QUEUE: queue };
  const run = { startedAt: new Date().toISOString(), localAdaptersOnly: true, ShopifyReadOnly: true, credentialsEmitted: false, steps: [] };
  const resumePath = arg('--resume-local-final-checkpoint');
  if (resumePath) {
    // Memory/crash rehearsal: replay the previously captured complete-size
    // journal, then read its missing final operations live. Never touches the
    // original proof or any remote R2 object.
    const previousControl = JSON.parse(await fs.readFile(path.join(resumePath, `merchant/${key}/refresh.json`), 'utf8'));
    if (!previousControl.journalKey) throw new SourceError('local_resume_journal_missing');
    await bucket.put(previousControl.journalKey, await fs.readFile(path.join(resumePath, previousControl.journalKey), 'utf8'));
    const resumed = { ...previousControl, status: 'RUNNING' };
    delete resumed.completedAt; delete resumed.sha256; delete resumed.rows;
    await bucket.put(`merchant/${key}/refresh.json`, JSON.stringify(resumed));
    queue.messages.push({ schemaVersion: 1, key, jobId: resumed.jobId, revision: resumed.revision });
    run.localFinalCheckpointReplay = true;
  } else await enqueueRefresh(env, key);
  while (queue.messages.length) {
    const message = queue.messages.shift(), cpu = process.cpuUsage(), start = performance.now(); let calls = 0;
    const memoryBefore = process.memoryUsage();
    const result = await consumeRefresh(env, message, { streamOptions, graphql: async (...params) => { calls++; return authenticated(...params); } });
    const used = process.cpuUsage(cpu);
    const memoryAfter = process.memoryUsage();
    const step = { ...result, calls, cpuMs: (used.user + used.system) / 1000, wallMs: performance.now() - start,
      memoryBefore, memoryAfter, processPeakRssKiB: process.resourceUsage().maxRSS };
    if (calls > 20) throw new SourceError('queue_source_call_budget_exceeded');
    run.steps.push(step); console.log(JSON.stringify({ event: 'queue_step', ...step }));
    await fs.writeFile(path.join(output, 'queue-verification.json'), JSON.stringify(run, null, 2) + '\n');
    if (result.failed) throw new SourceError(result.code);
    if (run.steps.length > 1000) throw new SourceError('local_queue_step_limit');
  }
  run.completedAt = new Date().toISOString(); run.complete = run.steps.at(-1)?.complete === true;
  run.totalLogicalCalls = run.steps.reduce((sum, step) => sum + step.calls, 0);
  run.maxCallsPerInvocation = Math.max(...run.steps.map(step => step.calls));
  run.maxObservedLocalCpuMs = Math.max(...run.steps.map(step => step.cpuMs));
  run.runtimeLimitNote = 'Node CPU is local evidence, not a measurement of Cloudflare Queue CPU. Production Queue readback is still required.';
  await fs.writeFile(path.join(output, 'queue-verification.json'), JSON.stringify(run, null, 2) + '\n');
  console.log(JSON.stringify({ ok: run.complete, invocations: run.steps.length, calls: run.totalLogicalCalls, maxCalls: run.maxCallsPerInvocation, localMaxCpuMs: run.maxObservedLocalCpuMs }));
}
main().catch(error => { console.error(JSON.stringify({ ok: false, code: error instanceof SourceError ? error.code : 'local_queue_verification_failed' })); process.exitCode = 1; });
