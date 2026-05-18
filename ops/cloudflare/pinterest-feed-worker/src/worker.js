const DEFAULT_FEED_OBJECT_KEY = 'pinterest/pinterest_unified_all_markets.tsv';
const DEFAULT_FEED_SHA256 = '8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7';
const DEFAULT_FEED_ROW_COUNT = '41814';

function textResponse(body, status, extraHeaders = {}) {
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
      ...extraHeaders,
    },
  });
}

function jsonError(status, error, extraHeaders = {}) {
  return textResponse(JSON.stringify({ error }), status, extraHeaders);
}

function isTruthy(value) {
  return String(value || '').toLowerCase() === 'true';
}

function timingSafeEqualHex(a, b) {
  if (!/^[a-f0-9]+$/i.test(a) || !/^[a-f0-9]+$/i.test(b)) return false;
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

function canonicalShopifyProxyMessage(url) {
  const pairs = [];
  url.searchParams.forEach((value, key) => {
    if (key !== 'signature') pairs.push([key, value]);
  });
  pairs.sort(([ak, av], [bk, bv]) => {
    const keyOrder = ak.localeCompare(bk);
    return keyOrder || av.localeCompare(bv);
  });
  return pairs.map(([key, value]) => `${key}=${value}`).join('');
}

async function hmacSha256Hex(secret, message) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(message));
  return [...new Uint8Array(signature)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
}

async function verifyShopifyAppProxy(request, env) {
  if (!isTruthy(env.REQUIRE_SHOPIFY_PROXY_SIGNATURE)) return true;
  if (!env.SHOPIFY_APP_PROXY_SECRET) return false;

  const url = new URL(request.url);
  const signature = url.searchParams.get('signature');
  if (!signature) return false;

  const expected = await hmacSha256Hex(env.SHOPIFY_APP_PROXY_SECRET, canonicalShopifyProxyMessage(url));
  return timingSafeEqualHex(signature, expected);
}

function feedHeaders(object, env) {
  const headers = new Headers();
  headers.set('Content-Type', 'text/tab-separated-values; charset=utf-8');
  headers.set('Cache-Control', 'public, max-age=86400');
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('X-DLM-Feed-SHA256', env.FEED_SHA256 || DEFAULT_FEED_SHA256);
  headers.set('X-DLM-Feed-Rows', env.FEED_ROW_COUNT || DEFAULT_FEED_ROW_COUNT);

  if (object.size != null) headers.set('Content-Length', String(object.size));
  if (object.httpEtag) headers.set('ETag', object.httpEtag);

  return headers;
}

async function serveFeed(request, env) {
  if (request.method !== 'GET') {
    return jsonError(405, 'method_not_allowed', { Allow: 'GET' });
  }
  if (!(await verifyShopifyAppProxy(request, env))) {
    return jsonError(401, 'unauthorized');
  }
  if (!env.PINTEREST_FEED_BUCKET) {
    return jsonError(503, 'feed_bucket_not_bound');
  }

  const key = env.FEED_OBJECT_KEY || DEFAULT_FEED_OBJECT_KEY;
  const object = await env.PINTEREST_FEED_BUCKET.get(key);
  if (!object) {
    return jsonError(503, 'feed_unavailable');
  }

  return new Response(object.body, {
    status: 200,
    headers: feedHeaders(object, env),
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/health') {
      return textResponse(JSON.stringify({ ok: true }), 200);
    }
    if (url.pathname === '/pinterest-feed.tsv' || url.pathname.endsWith('/pinterest-feed.tsv')) {
      return serveFeed(request, env);
    }
    return jsonError(404, 'not_found');
  },
};

export const internals = {
  canonicalShopifyProxyMessage,
  hmacSha256Hex,
};
