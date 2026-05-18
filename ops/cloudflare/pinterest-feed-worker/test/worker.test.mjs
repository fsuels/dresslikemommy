import assert from 'node:assert/strict';
import test from 'node:test';
import worker, { internals } from '../src/worker.js';

const feedBody = 'id\titem_group_id\timage_link\n1\tg1\thttps://example.com/i.jpg\n';

function env(overrides = {}) {
  return {
    FEED_OBJECT_KEY: 'pinterest/pinterest_unified_all_markets.tsv',
    FEED_SHA256: '8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7',
    FEED_ROW_COUNT: '41814',
    REQUIRE_SHOPIFY_PROXY_SIGNATURE: 'false',
    PINTEREST_FEED_BUCKET: {
      async get(key) {
        if (key !== 'pinterest/pinterest_unified_all_markets.tsv') return null;
        return {
          body: feedBody,
          size: Buffer.byteLength(feedBody),
          httpEtag: '"test-etag"',
        };
      },
    },
    ...overrides,
  };
}

test('serves the TSV feed with Pinterest audit headers', async () => {
  const response = await worker.fetch(new Request('https://feed.example.com/pinterest-feed.tsv'), env());

  assert.equal(response.status, 200);
  assert.equal(response.headers.get('content-type'), 'text/tab-separated-values; charset=utf-8');
  assert.equal(response.headers.get('x-dlm-feed-rows'), '41814');
  assert.equal(
    response.headers.get('x-dlm-feed-sha256'),
    '8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7'
  );
  assert.equal(await response.text(), feedBody);
});

test('rejects non-GET feed requests', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/pinterest-feed.tsv', { method: 'POST' }),
    env()
  );

  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET');
  assert.deepEqual(await response.json(), { error: 'method_not_allowed' });
});

test('can require a Shopify app-proxy signature', async () => {
  const secret = 'test-secret';
  const unsignedUrl = new URL('https://feed.example.com/apps/pinterest-feed.tsv?shop=example.myshopify.com&timestamp=1780000000');
  const signature = await internals.hmacSha256Hex(secret, internals.canonicalShopifyProxyMessage(unsignedUrl));
  unsignedUrl.searchParams.set('signature', signature);

  const response = await worker.fetch(
    new Request(unsignedUrl),
    env({
      REQUIRE_SHOPIFY_PROXY_SIGNATURE: 'true',
      SHOPIFY_APP_PROXY_SECRET: secret,
    })
  );

  assert.equal(response.status, 200);
});

test('fails closed when signature verification is required but absent', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/apps/pinterest-feed.tsv?shop=example.myshopify.com'),
    env({
      REQUIRE_SHOPIFY_PROXY_SIGNATURE: 'true',
      SHOPIFY_APP_PROXY_SECRET: 'test-secret',
    })
  );

  assert.equal(response.status, 401);
});
