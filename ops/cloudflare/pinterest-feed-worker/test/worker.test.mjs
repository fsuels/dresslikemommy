import assert from 'node:assert/strict';
import test from 'node:test';
import worker, { internals } from '../src/worker.js';

const feedBody = 'id\titem_group_id\timage_link\n1\tg1\thttps://example.com/i.jpg\n';
const paidParentFeedBody = 'id\titem_group_id\tcustom_label_2\np1\tg1\tmommy_and_me\n';
const paidParentEsFeedBody = 'id\titem_group_id\tcustom_label_0\tcustom_label_2\nes1\tg1\tus_es\tmommy_and_me\n';
const paidParentIsolatedFeedBody = 'id\titem_group_id\tcustom_label_0\tcustom_label_2\tcustom_label_4\niso1\tiso1\tus\tmommy_and_me\tcollection_intent_parent_isolated_v20260521\n';

function env(overrides = {}) {
  return {
    FEED_OBJECT_KEY: 'pinterest/pinterest_unified_all_markets.tsv',
    FEED_SHA256: 'b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0',
    FEED_ROW_COUNT: '28122',
    PAID_PARENT_FEED_OBJECT_KEY: 'pinterest/pinterest_us_paid_parent_collection_intent.tsv',
    PAID_PARENT_FEED_SHA256: 'e990b912ecc80d1c73e72b19f421f10d8a0d21aea13628506ea9230df1c114b6',
    PAID_PARENT_FEED_ROW_COUNT: '210',
    PAID_PARENT_ES_FEED_OBJECT_KEY: 'pinterest/pinterest_us_es_paid_parent_collection_intent.tsv',
    PAID_PARENT_ES_FEED_SHA256: 'f4679594f0112105f814be617ff62919019cd711be147d7d0dcae4eb73ef4a69',
    PAID_PARENT_ES_FEED_ROW_COUNT: '210',
    PAID_PARENT_ISOLATED_FEED_OBJECT_KEY: 'pinterest/pinterest_us_paid_parent_isolated_candidate.tsv',
    PAID_PARENT_ISOLATED_FEED_SHA256: 'db2fcddaa95609ccade30b5af11d3edd9d90e35c10f2d011b24fc4b57dce8113',
    PAID_PARENT_ISOLATED_FEED_ROW_COUNT: '210',
    REQUIRE_SHOPIFY_PROXY_SIGNATURE: 'false',
    PINTEREST_FEED_BUCKET: {
      async get(key) {
        if (key === 'pinterest/pinterest_unified_all_markets.tsv') {
          return {
            body: feedBody,
            size: Buffer.byteLength(feedBody),
            httpEtag: '"test-etag"',
          };
        }
        if (key === 'pinterest/pinterest_us_paid_parent_collection_intent.tsv') {
          return {
            body: paidParentFeedBody,
            size: Buffer.byteLength(paidParentFeedBody),
            httpEtag: '"parent-test-etag"',
          };
        }
        if (key === 'pinterest/pinterest_us_es_paid_parent_collection_intent.tsv') {
          return {
            body: paidParentEsFeedBody,
            size: Buffer.byteLength(paidParentEsFeedBody),
            httpEtag: '"parent-es-test-etag"',
          };
        }
        if (key === 'pinterest/pinterest_us_paid_parent_isolated_candidate.tsv') {
          return {
            body: paidParentIsolatedFeedBody,
            size: Buffer.byteLength(paidParentIsolatedFeedBody),
            httpEtag: '"parent-isolated-test-etag"',
          };
        }
        return null;
      },
    },
    ...overrides,
  };
}

test('serves the default TSV feed with Pinterest audit headers', async () => {
  const response = await worker.fetch(new Request('https://feed.example.com/pinterest-feed.tsv'), env());

  assert.equal(response.status, 200);
  assert.equal(response.headers.get('content-type'), 'text/tab-separated-values; charset=utf-8');
  assert.equal(response.headers.get('x-dlm-feed-rows'), '28122');
  assert.equal(response.headers.get('x-dlm-feed-object-key'), 'pinterest/pinterest_unified_all_markets.tsv');
  assert.equal(
    response.headers.get('x-dlm-feed-sha256'),
    'b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0'
  );
  assert.equal(await response.text(), feedBody);
});

test('serves the parent-only paid Pinterest feed route', async () => {
  const response = await worker.fetch(new Request('https://feed.example.com/pinterest-paid-parent-feed.tsv'), env());

  assert.equal(response.status, 200);
  assert.equal(response.headers.get('content-type'), 'text/tab-separated-values; charset=utf-8');
  assert.equal(response.headers.get('x-dlm-feed-rows'), '210');
  assert.equal(
    response.headers.get('x-dlm-feed-sha256'),
    'e990b912ecc80d1c73e72b19f421f10d8a0d21aea13628506ea9230df1c114b6'
  );
  assert.equal(
    response.headers.get('x-dlm-feed-object-key'),
    'pinterest/pinterest_us_paid_parent_collection_intent.tsv'
  );
  assert.equal(await response.text(), paidParentFeedBody);
});

test('serves the Spanish parent-only paid Pinterest feed route', async () => {
  const response = await worker.fetch(new Request('https://feed.example.com/pinterest-paid-parent-es-feed.tsv'), env());

  assert.equal(response.status, 200);
  assert.equal(response.headers.get('content-type'), 'text/tab-separated-values; charset=utf-8');
  assert.equal(response.headers.get('x-dlm-feed-rows'), '210');
  assert.equal(
    response.headers.get('x-dlm-feed-sha256'),
    'f4679594f0112105f814be617ff62919019cd711be147d7d0dcae4eb73ef4a69'
  );
  assert.equal(
    response.headers.get('x-dlm-feed-object-key'),
    'pinterest/pinterest_us_es_paid_parent_collection_intent.tsv'
  );
  assert.equal(await response.text(), paidParentEsFeedBody);
});

test('serves the isolated parent-only paid Pinterest feed route', async () => {
  const response = await worker.fetch(new Request('https://feed.example.com/pinterest-paid-parent-isolated-feed.tsv'), env());

  assert.equal(response.status, 200);
  assert.equal(response.headers.get('content-type'), 'text/tab-separated-values; charset=utf-8');
  assert.equal(response.headers.get('x-dlm-feed-rows'), '210');
  assert.equal(
    response.headers.get('x-dlm-feed-sha256'),
    'db2fcddaa95609ccade30b5af11d3edd9d90e35c10f2d011b24fc4b57dce8113'
  );
  assert.equal(
    response.headers.get('x-dlm-feed-object-key'),
    'pinterest/pinterest_us_paid_parent_isolated_candidate.tsv'
  );
  assert.equal(await response.text(), paidParentIsolatedFeedBody);
});

test('fails closed when a configured feed object is missing', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/pinterest-paid-parent-feed.tsv'),
    env({
      PAID_PARENT_FEED_OBJECT_KEY: 'pinterest/missing.tsv',
    })
  );

  assert.equal(response.status, 503);
  assert.deepEqual(await response.json(), { error: 'feed_unavailable' });
});

test('serves app-proxy-style paid parent feed paths', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/apps/pinterest-paid-parent-feed.tsv'),
    env()
  );

  assert.equal(response.status, 200);
  assert.equal(await response.text(), paidParentFeedBody);
});

test('serves app-proxy-style Spanish paid parent feed paths', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/apps/pinterest-paid-parent-es-feed.tsv'),
    env()
  );

  assert.equal(response.status, 200);
  assert.equal(await response.text(), paidParentEsFeedBody);
});

test('serves app-proxy-style isolated paid parent feed paths', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/apps/pinterest-paid-parent-isolated-feed.tsv'),
    env()
  );

  assert.equal(response.status, 200);
  assert.equal(await response.text(), paidParentIsolatedFeedBody);
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

test('rejects non-GET paid parent feed requests', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/pinterest-paid-parent-feed.tsv', { method: 'POST' }),
    env()
  );

  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET');
  assert.deepEqual(await response.json(), { error: 'method_not_allowed' });
});

test('rejects non-GET Spanish paid parent feed requests', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/pinterest-paid-parent-es-feed.tsv', { method: 'POST' }),
    env()
  );

  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET');
  assert.deepEqual(await response.json(), { error: 'method_not_allowed' });
});

test('rejects non-GET isolated paid parent feed requests', async () => {
  const response = await worker.fetch(
    new Request('https://feed.example.com/pinterest-paid-parent-isolated-feed.tsv', { method: 'POST' }),
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
