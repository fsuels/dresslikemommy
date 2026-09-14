import { SourceError } from './collector.js';
import { tsvChunks } from './generator.js';
import { commitStoredResult } from './worker.js';

const TSV_TYPE = 'text/tab-separated-values; charset=utf-8';
function hex(buffer) { return [...new Uint8Array(buffer)].map(byte => byte.toString(16).padStart(2, '0')).join(''); }

// Cloudflare-native bounded stream primitives. Tests/CLI inject Node adapters;
// the production core has no fs, Buffer, Node import, or full-file accumulation.
export async function publishStreamedResult(bucket, result, snapshot, market, before, {
  publisherJobId, randomId = () => crypto.randomUUID(),
  digestStream = () => new crypto.DigestStream('SHA-256'),
  fixedLengthStream = bytes => new FixedLengthStream(bytes),
} = {}) {
  if (!result.ok || !result.diagnostics.returnPolicyLabelsConfirmed) throw new SourceError('feed_not_ready_to_publish');
  if (!Number.isSafeInteger(result.bytes) || result.bytes < 1 || result.bytes > 60000000 || !Array.isArray(result.columns)) throw new SourceError('feed_stream_size_invalid');
  const stageKey = `merchant/jobs/${market.key}/${publisherJobId || randomId()}/stage-${randomId()}.tsv`;
  const fixed = fixedLengthStream(result.bytes), digest = digestStream();
  const writer = fixed.writable.getWriter(), hashWriter = digest.getWriter();
  const upload = bucket.put(stageKey, fixed.readable, { httpMetadata: { contentType: TSV_TYPE } });
  // Attach rejection handling immediately; writing and upload run together.
  upload.catch(() => {}); digest.digest.catch(() => {});
  try {
    for (const chunk of tsvChunks(result.rows, result.columns)) {
      await writer.write(chunk); await hashWriter.write(chunk);
    }
    await writer.close(); await hashWriter.close();
    const staged = await upload, sha256 = hex(await digest.digest);
    const source = await bucket.get(stageKey);
    if (!staged?.etag || !source || source.etag !== staged.etag || source.size !== result.bytes) throw new SourceError('staged_feed_invalid');
    const objectKey = `merchant/${market.key}/${sha256}.tsv`;
    // R2's own reader has a known length. R2 validates this whole-stream SHA-256
    // on the immutable copy before the current manifest can be switched.
    const stored = await bucket.put(objectKey, source.body, { sha256, httpMetadata: { contentType: TSV_TYPE } });
    return await commitStoredResult(bucket, stored, { ...result, sha256 }, snapshot, market, before, { publisherJobId });
  } catch (error) {
    await Promise.allSettled([writer.abort(), hashWriter.abort(), upload]);
    throw error instanceof SourceError ? error : new SourceError('feed_stream_failed');
  } finally {
    // This uniquely named private staging object is never a live feed/rollback.
    if (typeof bucket.delete === 'function') await bucket.delete(stageKey).catch(() => {});
  }
}
