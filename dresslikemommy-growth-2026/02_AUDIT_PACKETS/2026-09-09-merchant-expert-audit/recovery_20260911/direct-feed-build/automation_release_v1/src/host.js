// Read-only first-release entry. No Admin token, write endpoint or Cron handler.
const TSV_TYPE = 'text/tab-separated-values; charset=utf-8';
function json(value, status, headers = {}) {
  return new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...headers } });
}
export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return json({ error: 'method_not_allowed' }, 405, { Allow: 'GET, HEAD' });
    const url = new URL(request.url);
    if (url.pathname === '/health') return json({ ok: true, service: 'merchant-feed-reader' }, 200);
    const match = url.pathname.match(/^\/feeds\/([a-z]{2}-[a-z]{2}(?:-[a-z]{2})?)\.tsv$/);
    if (!match) return json({ error: 'not_found' }, 404);
    try {
      const config = JSON.parse(env.MERCHANT_CONFIG_JSON);
      const market = config.markets?.find(m => m.key === match[1] && m.enabled);
      if (!market) return json({ error: 'market_not_enabled' }, 404);
      const pointer = await env.MERCHANT_FEED_BUCKET.get(`merchant/${market.key}/current.json`);
      if (!pointer) return json({ error: 'feed_unavailable' }, 503);
      const manifest = JSON.parse(await pointer.text());
      const age = Date.now() - Date.parse(manifest.sourceCompletedAt);
      if (manifest.schemaVersion !== 1 || manifest.market?.key !== market.key || manifest.market.country !== market.country || manifest.market.locale !== market.locale || manifest.market.currency !== market.currency || !/^[a-f0-9]{64}$/.test(manifest.sha256 || '') || !manifest.objectEtag || manifest.objectKey !== `merchant/${market.key}/${manifest.sha256}.tsv` || !Number.isFinite(age) || age < -60000 || age > (config.maxFeedAgeHours ?? 48) * 3600000) return json({ error: 'feed_manifest_invalid_or_stale' }, 503);
      const object = await env.MERCHANT_FEED_BUCKET.get(manifest.objectKey);
      if (!object || object.size > 60000000 || object.size !== manifest.bytes || object.etag !== manifest.objectEtag) return json({ error: 'feed_object_invalid' }, 503);
      // The uploader verifies full SHA-256/MD5 before publishing the pointer.
      // Bind exact immutable key/ETag/bytes here and stream without buffering.
      return new Response(request.method === 'HEAD' ? null : object.body, { status: 200, headers: {
        'Content-Type': TSV_TYPE, 'Cache-Control': 'public, max-age=300', 'X-Content-Type-Options': 'nosniff',
        'Content-Length': String(manifest.bytes), ETag: `"${manifest.sha256}"`,
        'X-DLM-Feed-SHA256': manifest.sha256, 'X-DLM-Feed-Rows': String(manifest.rows),
        'X-DLM-Feed-Country': market.country, 'X-DLM-Feed-Language': market.locale,
        'X-DLM-Feed-Currency': market.currency, 'X-DLM-Feed-Source-Updated': manifest.sourceCompletedAt,
      } });
    } catch { return json({ error: 'feed_unavailable' }, 503); }
  },
};
