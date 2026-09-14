import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { buildFeed } from '../src/generator.js';
import { publishStreamedResult } from '../src/stream-publish.js';
import { currentManifest } from '../src/worker.js';
import { config, market, now, snapshot, Bucket } from './fixtures.js';
import { streamOptions } from './node-streams.js';

test('streamed bytes, length and digest exactly equal the materialized reference TSV', async () => {
  const s = snapshot(), full = await buildFeed(s, config, market, { now });
  const result = await buildFeed(s, config, market, { now, materialize: false });
  assert.equal(result.tsv, null); assert.equal(result.bytes, full.bytes);
  const bucket = new Bucket(), before = { manifest: null, etag: null };
  const manifest = await publishStreamedResult(bucket, result, s, market, before, streamOptions);
  assert.equal(manifest.sha256, full.sha256); assert.equal(await (await bucket.get(manifest.objectKey)).text(), full.tsv);
  assert.equal(createHash('sha256').update(full.tsv).digest('hex'), manifest.sha256);
  assert.ok(bucket.writes[0].startsWith('merchant/jobs/')); assert.equal(bucket.writes.at(-1), 'merchant/us-en/current.json');
  assert.ok(![...bucket.objects.keys()].some(key => key.includes('/stage-')));
});
test('incorrect declared length cannot promote a truncated stream', async () => {
  const s = snapshot(), result = await buildFeed(s, config, market, { now, materialize: false });
  const bucket = new Bucket(); result.bytes++;
  await assert.rejects(publishStreamedResult(bucket, result, s, market, { manifest: null, etag: null }, streamOptions), /feed_stream_failed/);
  assert.equal((await currentManifest(bucket, market.key)).manifest, null);
});
test('R2 immutable-copy failure preserves prior pointer and removes only private staging', async () => {
  const s = snapshot(), result = await buildFeed(s, config, market, { now, materialize: false });
  const bucket = new Bucket(), original = bucket.put.bind(bucket);
  bucket.put = async (key, data, options) => { if (key.startsWith('merchant/us-en/') && key.endsWith('.tsv')) throw new Error('synthetic_copy_failure'); return original(key, data, options); };
  await assert.rejects(publishStreamedResult(bucket, result, s, market, { manifest: null, etag: null }, streamOptions), /feed_stream_failed/);
  assert.equal((await currentManifest(bucket, market.key)).manifest, null);
  assert.ok(![...bucket.objects.keys()].some(key => key.includes('/stage-')));
});
