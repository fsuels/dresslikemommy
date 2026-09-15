import { SourceError } from './collector.js';

export const SHOPIFY_CATALOG_READ_SCOPES = Object.freeze([
  'read_products', 'read_publications', 'read_markets',
  'read_locales', 'read_translations', 'read_metaobjects',
]);
const allowedScopes = new Set(SHOPIFY_CATALOG_READ_SCOPES);
const errorCodes = new Set([
  'shopify_auth_mode_required', 'shopify_auth_invalid_domain', 'shopify_auth_missing_credentials',
  'shopify_auth_invalid_options', 'shopify_auth_invalid_clock', 'shopify_auth_request_failed',
  'shopify_auth_timeout', 'shopify_auth_rejected', 'shopify_auth_http_error',
  'shopify_auth_redirect_rejected', 'shopify_auth_invalid_response', 'shopify_auth_scope_not_allowed',
  'shopify_auth_invalid_expiry', 'shopify_auth_failed',
]);
// One resolved token must cover a full 15-minute Queue invocation, plus a
// one-minute buffer, without exchanges during the catalog request sequence.
const EXPIRY_MARGIN_MS = 16 * 60_000;
const MAX_TOKEN_LIFETIME_SECONDS = 86_400;

function requireValue(value, code) { if (!value) throw new SourceError(code); }
function timestamp(now) {
  let value;
  try { value = now(); } catch { throw new SourceError('shopify_auth_invalid_clock'); }
  const time = value instanceof Date ? value.getTime() : value;
  requireValue(Number.isSafeInteger(time) && time >= 0, 'shopify_auth_invalid_clock');
  return time;
}
function credential(value) {
  return typeof value === 'string' && value.length > 0 && value.length <= 4096 && !/[\s\u0000-\u001f\u007f-\u009f]/.test(value);
}
async function credentialKey(domain, clientId, clientSecret) {
  const bytes = new TextEncoder().encode(JSON.stringify([domain, clientId, clientSecret]));
  const hash = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(hash)].map(value => value.toString(16).padStart(2, '0')).join('');
}
function validateTokenResponse(data, startedAt, completedAt) {
  requireValue(data && typeof data === 'object' && !Array.isArray(data) &&
    Object.keys(data).sort().join(',') === 'access_token,expires_in,scope', 'shopify_auth_invalid_response');
  requireValue(typeof data.access_token === 'string' && data.access_token.length > 0 && data.access_token.length <= 4096 &&
    /^[\x21-\x7e]+$/.test(data.access_token), 'shopify_auth_invalid_response');
  requireValue(typeof data.scope === 'string' && data.scope.length <= 1024 && !/[\u0000-\u001f\u007f-\u009f]/.test(data.scope), 'shopify_auth_scope_not_allowed');
  const scopes = data.scope.split(',').map(scope => scope.trim());
  requireValue(scopes.length > 0 && new Set(scopes).size === scopes.length && scopes.every(scope => allowedScopes.has(scope)), 'shopify_auth_scope_not_allowed');
  requireValue(Number.isSafeInteger(data.expires_in) && data.expires_in > EXPIRY_MARGIN_MS / 1000 &&
    data.expires_in <= MAX_TOKEN_LIFETIME_SECONDS, 'shopify_auth_invalid_expiry');
  // Use request start, not response arrival, so network/body latency cannot
  // extend the declared token lifetime. Do not return a token inside its margin.
  const refreshAt = startedAt + data.expires_in * 1000 - EXPIRY_MARGIN_MS;
  requireValue(completedAt >= startedAt && completedAt < refreshAt && Number.isSafeInteger(refreshAt), 'shopify_auth_invalid_expiry');
  return { token: data.access_token, startedAt, refreshAt };
}

async function exchange({ domain, clientId, clientSecret, fetchImpl, now, requestTimeoutMs }) {
  const startedAt = timestamp(now), endpoint = `https://${domain}/admin/oauth/access_token`;
  const controller = new AbortController();
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => { controller.abort(); reject(new SourceError('shopify_auth_timeout')); }, requestTimeoutMs);
  });
  const request = async () => {
    let response;
    try {
      response = await fetchImpl(endpoint, {
        method: 'POST', redirect: 'error', credentials: 'omit', signal: controller.signal,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/json' },
        body: new URLSearchParams({ grant_type: 'client_credentials', client_id: clientId, client_secret: clientSecret }).toString(),
      });
    } catch { throw new SourceError('shopify_auth_request_failed'); }
    requireValue(response && Number.isInteger(response.status), 'shopify_auth_invalid_response');
    requireValue(response.redirected !== true && (!response.url || response.url === endpoint), 'shopify_auth_redirect_rejected');
    if (response.status === 401 || response.status === 403) throw new SourceError('shopify_auth_rejected');
    if (response.status >= 300 && response.status < 400) throw new SourceError('shopify_auth_redirect_rejected');
    requireValue(response.status === 200, 'shopify_auth_http_error');
    requireValue(/^application\/json(?:\s*;|$)/i.test(response.headers?.get('content-type') || ''), 'shopify_auth_invalid_response');
    let body, data;
    try {
      body = await response.text();
      requireValue(new TextEncoder().encode(body).byteLength <= 16_384, 'shopify_auth_invalid_response');
      data = JSON.parse(body);
    } catch { throw new SourceError('shopify_auth_invalid_response'); }
    return validateTokenResponse(data, startedAt, timestamp(now));
  };
  try { return await Promise.race([request(), timeout]); }
  finally { clearTimeout(timer); }
}

// Cloud secret bindings are supplied by the caller. No env file, legacy token,
// disk/R2 persistence, credential logging or automatic authorization retry.
export function createShopifyAdminTokenResolver({ requestTimeoutMs = 15_000 } = {}) {
  requireValue(Number.isSafeInteger(requestTimeoutMs) && requestTimeoutMs > 0 && requestTimeoutMs <= 60_000, 'shopify_auth_invalid_options');
  const cache = new Map(), inFlight = new Map();
  return async function resolve(env, { domain, fetchImpl = globalThis.fetch, now = Date.now } = {}) {
    try {
      requireValue(env?.SHOPIFY_AUTH_MODE === 'client_credentials', 'shopify_auth_mode_required');
      requireValue(typeof domain === 'string' && /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.myshopify\.com$/.test(domain), 'shopify_auth_invalid_domain');
      const clientId = env.SHOPIFY_CLIENT_ID, clientSecret = env.SHOPIFY_CLIENT_SECRET;
      requireValue(credential(clientId) && credential(clientSecret), 'shopify_auth_missing_credentials');
      requireValue(typeof fetchImpl === 'function' && typeof now === 'function', 'shopify_auth_invalid_options');
      // Join before the asynchronous digest so even an immediate HTTP failure
      // cannot cause one exchange per concurrent caller. This transient identity
      // is removed on settlement; long-lived cache keys are SHA-256 digests.
      const identity = JSON.stringify([domain, clientId, clientSecret]);
      let pending = inFlight.get(identity);
      if (!pending) {
        pending = (async () => {
          const key = await credentialKey(domain, clientId, clientSecret), currentTime = timestamp(now);
          for (const [cachedKey, entry] of cache) if (currentTime >= entry.refreshAt) cache.delete(cachedKey);
          const cached = cache.get(key);
          if (cached) {
            requireValue(currentTime >= cached.startedAt, 'shopify_auth_invalid_clock');
            return cached;
          }
          const entry = await exchange({ domain, clientId, clientSecret, fetchImpl, now, requestTimeoutMs });
          cache.set(key, entry); return entry;
        })();
        inFlight.set(identity, pending);
      }
      try {
        const entry = await pending, completedAt = timestamp(now);
        requireValue(completedAt >= entry.startedAt && completedAt < entry.refreshAt, 'shopify_auth_invalid_expiry');
        return entry.token;
      }
      finally { if (inFlight.get(identity) === pending) inFlight.delete(identity); }
    } catch (error) {
      // Re-create only known constant codes; never expose upstream error text,
      // credentials, response bodies, endpoint URLs or an error cause.
      throw new SourceError(errorCodes.has(error?.code) ? error.code : 'shopify_auth_failed');
    }
  };
}

export const resolveShopifyAdminToken = createShopifyAdminTokenResolver();
