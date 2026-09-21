import test from 'node:test';
import assert from 'node:assert/strict';
import { SourceError } from '../src/collector.js';
import { createShopifyAdminTokenResolver, resolveShopifyAdminToken, SHOPIFY_CATALOG_READ_SCOPES } from '../src/shopify-auth.js';

const domain = 'fixture-catalog.myshopify.com';
const env = { SHOPIFY_AUTH_MODE: 'client_credentials', SHOPIFY_CLIENT_ID: 'synthetic-client-id', SHOPIFY_CLIENT_SECRET: 'synthetic-secret' };
const initialTime = Date.parse('2026-09-14T20:46:00Z');
const now = () => initialTime;
const payload = (changes = {}) => ({ access_token: 'synthetic-access-token', scope: 'read_products', expires_in: 86399, ...changes });
const reply = (data = payload(), changes = {}) => new Response(JSON.stringify(data), { status: 200, headers: { 'content-type': 'application/json' }, ...changes });
const options = fetchImpl => ({ domain, now, fetchImpl });
function deferred() { let resolve, reject; const promise = new Promise((yes, no) => { resolve = yes; reject = no; }); return { promise, resolve, reject }; }
async function expectCode(promise, code) {
  await assert.rejects(promise, error => error instanceof SourceError && error.code === code && error.message === code && !error.cause);
}

test('client credentials sends one form POST to the exact shop with redirects disabled', async () => {
  const credentials = { ...env, SHOPIFY_CLIENT_ID: 'synthetic+id&1', SHOPIFY_CLIENT_SECRET: 'synthetic=secret+&2' };
  let calls = 0;
  const token = await resolveShopifyAdminToken(credentials, options(async (url, request) => {
    calls++;
    assert.equal(url, `https://${domain}/admin/oauth/access_token`);
    assert.equal(request.method, 'POST'); assert.equal(request.redirect, 'error'); assert.equal(request.credentials, 'omit');
    assert.equal(request.headers['Content-Type'], 'application/x-www-form-urlencoded');
    assert.equal(request.headers.Accept, 'application/json');
    const body = new URLSearchParams(request.body);
    assert.deepEqual([...body.keys()].sort(), ['client_id', 'client_secret', 'grant_type']);
    assert.equal(body.get('grant_type'), 'client_credentials');
    assert.equal(body.get('client_id'), credentials.SHOPIFY_CLIENT_ID); assert.equal(body.get('client_secret'), credentials.SHOPIFY_CLIENT_SECRET);
    assert.equal(request.signal.aborted, false);
    assert.ok(!url.includes(credentials.SHOPIFY_CLIENT_SECRET));
    return reply(payload({ scope: SHOPIFY_CATALOG_READ_SCOPES.join(',') }));
  }));
  assert.equal(token, 'synthetic-access-token'); assert.equal(calls, 1);
});

test('explicit mode is mandatory and legacy access-token properties are never read', async () => {
  const resolve = createShopifyAdminTokenResolver(); let calls = 0;
  const settings = options(async () => { calls++; return reply(); });
  const guarded = { ...env };
  Object.defineProperty(guarded, 'SHOPIFY_ADMIN_ACCESS_TOKEN', { get() { throw new Error('legacy credential was read'); } });
  assert.equal(await resolve(guarded, settings), 'synthetic-access-token');
  for (const mode of [undefined, '', 'legacy', 'client_credentials ']) {
    await expectCode(resolve({ ...guarded, SHOPIFY_AUTH_MODE: mode }, settings), 'shopify_auth_mode_required');
  }
  await expectCode(resolve({ SHOPIFY_AUTH_MODE: 'client_credentials', SHOPIFY_ADMIN_ACCESS_TOKEN: 'synthetic-broad-token' }, settings), 'shopify_auth_missing_credentials');
  assert.equal(calls, 1);
});

test('invalid domains and malformed secret bindings fail before making any request', async () => {
  const resolve = createShopifyAdminTokenResolver(); let calls = 0;
  const settings = options(async () => { calls++; return reply(); });
  for (const invalid of [undefined, 'https://fixture-catalog.myshopify.com', 'fixture-catalog.myshopify.com/path',
    'fixture-catalog.myshopify.com:443', 'fixture-catalog.myshopify.com.evil.example', 'a.b.myshopify.com',
    'user@fixture-catalog.myshopify.com', 'Fixture-Catalog.myshopify.com', 'fixture_catalog.myshopify.com',
    '-fixture.myshopify.com', 'fixture-.myshopify.com', ' fixture.myshopify.com', 'fixture.myshopify.com\n', `${'a'.repeat(64)}.myshopify.com`]) {
    await expectCode(resolve(env, { ...settings, domain: invalid }), 'shopify_auth_invalid_domain');
  }
  for (const key of ['SHOPIFY_CLIENT_ID', 'SHOPIFY_CLIENT_SECRET']) {
    for (const invalid of [undefined, '', ' ', 'secret\nvalue', 12, {}, 'x'.repeat(4097)]) {
      await expectCode(resolve({ ...env, [key]: invalid }, settings), 'shopify_auth_missing_credentials');
    }
  }
  assert.equal(calls, 0);
});

test('scope readback rejects every write or unrelated read, with no token cached', async () => {
  assert.deepEqual([...SHOPIFY_CATALOG_READ_SCOPES], ['read_products', 'read_publications', 'read_markets', 'read_locales', 'read_translations', 'read_metaobjects']);
  for (const scope of ['write_products', 'read_products,write_translations', 'read_customers', 'read_orders', 'read_all_orders',
    'read_products,read_themes', 'read_metaobject_definitions', 'read_inventory', 'read_products write_products', '',
    'read_products,', 'read_products,read_products', 'read_products\n', null, ['read_products']]) {
    const resolve = createShopifyAdminTokenResolver(); let calls = 0;
    const settings = options(async () => { calls++; return reply(payload({ scope: calls === 1 ? scope : 'read_products' })); });
    await expectCode(resolve(env, settings), 'shopify_auth_scope_not_allowed');
    assert.equal(calls, 1);
    assert.equal(await resolve(env, settings), 'synthetic-access-token'); assert.equal(calls, 2);
  }
});

test('strict token response schema rejects missing, extra, malformed and oversized values', async () => {
  for (const data of [null, [], 'text', {}, payload({ access_token: '' }), payload({ access_token: 1 }),
    payload({ access_token: 'bad\r\nheader' }), payload({ access_token: 'token with spaces' }), payload({ access_token: 'ñ' }),
    payload({ access_token: 'x'.repeat(4097) }), payload({ token_type: 'Bearer' }),
    { access_token: 'synthetic-token', expires_in: 86399 }, payload({ unexpected: 'synthetic-private-response' })]) {
    const resolve = createShopifyAdminTokenResolver();
    await expectCode(resolve(env, options(async () => reply(data))), 'shopify_auth_invalid_response');
  }
  const resolve = createShopifyAdminTokenResolver();
  await expectCode(resolve(env, options(async () => new Response('x'.repeat(20_000), { headers: { 'content-type': 'application/json' } }))), 'shopify_auth_invalid_response');
  await expectCode(resolve(env, options(async () => new Response('not-json synthetic-secret', { headers: { 'content-type': 'application/json' } }))), 'shopify_auth_invalid_response');
  await expectCode(resolve(env, options(async () => reply(payload(), { headers: { 'content-type': 'text/plain' } }))), 'shopify_auth_invalid_response');
});

test('expiry requires a safe integer duration with usable margin and accounts for response latency', async () => {
  for (const expires_in of [null, 0, -1, 60, 960, 10.5, '86399', 86401, Number.MAX_SAFE_INTEGER]) {
    const resolve = createShopifyAdminTokenResolver();
    await expectCode(resolve(env, options(async () => reply(payload({ expires_in })))), 'shopify_auth_invalid_expiry');
  }
  let time = initialTime;
  const resolve = createShopifyAdminTokenResolver();
  await expectCode(resolve(env, { domain, now: () => time, fetchImpl: async () => {
    time += 60_000; return reply(payload({ expires_in: 1020 }));
  } }), 'shopify_auth_invalid_expiry');
});

test('warm cache refreshes at its 16-minute margin and supports a Date-returning clock', async () => {
  const resolve = createShopifyAdminTokenResolver(); let time = initialTime, calls = 0;
  const settings = { domain, now: () => new Date(time), fetchImpl: async () => reply(payload({ access_token: `synthetic-token-${++calls}`, expires_in: 1020 })) };
  assert.equal(await resolve(env, settings), 'synthetic-token-1');
  time += 59_999; assert.equal(await resolve(env, settings), 'synthetic-token-1'); assert.equal(calls, 1);
  time++; assert.equal(await resolve(env, settings), 'synthetic-token-2'); assert.equal(calls, 2);
  assert.equal(await resolve(env, settings), 'synthetic-token-2'); assert.equal(calls, 2);
});

test('one token survives a full 15-minute catalog invocation from the reproduced near-expiry boundary', async () => {
  for (const remaining of [61_000, 16 * 60_000 + 1]) {
    const resolve = createShopifyAdminTokenResolver(); let time = initialTime, exchanges = 0;
    const expirations = new Map();
    const settings = { domain, now: () => time, fetchImpl: async () => {
      const access_token = `synthetic-lifecycle-token-${++exchanges}`;
      expirations.set(access_token, time + 86399 * 1000);
      return reply(payload({ access_token }));
    } };
    const seeded = await resolve(env, settings);
    time = expirations.get(seeded) - remaining;
    const invocationStart = time, token = await resolve(env, settings);
    const responses = [];
    // With the former one-minute margin, the 61-second cached token returned
    // 200, 200, then 401 on the third read. No per-read OAuth calls are made.
    for (let index = 0; index < 20; index++) {
      responses.push(time < expirations.get(token) ? 200 : 401);
      time += index < 3 ? 50_000 : 40_000;
    }
    time += 70_000;
    assert.equal(time - invocationStart, 15 * 60_000);
    assert.deepEqual(responses, Array(20).fill(200));
    assert.ok(expirations.get(token) - time > 60_000);
    assert.equal(exchanges, remaining === 61_000 ? 2 : 1);
  }
});

test('domain, client-ID, secret rotation and resolver instance are separate cache identities', async () => {
  const resolve = createShopifyAdminTokenResolver(); let calls = 0;
  const settings = options(async () => reply(payload({ access_token: `synthetic-token-${++calls}` })));
  assert.equal(await resolve(env, settings), 'synthetic-token-1');
  assert.equal(await resolve({ ...env, SHOPIFY_CLIENT_ID: 'rotated-client-id' }, settings), 'synthetic-token-2');
  assert.equal(await resolve({ ...env, SHOPIFY_CLIENT_SECRET: 'rotated-secret' }, settings), 'synthetic-token-3');
  assert.equal(await resolve(env, { ...settings, domain: 'second-fixture.myshopify.com' }), 'synthetic-token-4');
  assert.equal(await resolve(env, settings), 'synthetic-token-1');
  assert.equal(await createShopifyAdminTokenResolver()(env, settings), 'synthetic-token-5');
  assert.equal(calls, 5);
});

test('concurrent requests share one exchange and do not persist an in-flight failure', async () => {
  const resolve = createShopifyAdminTokenResolver(), gate = deferred(), entered = deferred(); let calls = 0;
  const settings = options(async () => { calls++; entered.resolve(); await gate.promise; return reply(); });
  const requests = Array.from({ length: 12 }, () => resolve(env, settings));
  await entered.promise; gate.resolve();
  assert.deepEqual(await Promise.all(requests), Array(12).fill('synthetic-access-token')); assert.equal(calls, 1);
  const failResolve = createShopifyAdminTokenResolver(), failGate = deferred(), failEntered = deferred(); let failures = 0;
  const failSettings = options(async () => { failures++; failEntered.resolve(); await failGate.promise; throw new Error('synthetic-secret upstream URL'); });
  const failed = Array.from({ length: 8 }, () => failResolve(env, failSettings));
  await failEntered.promise; failGate.resolve();
  const results = await Promise.allSettled(failed);
  assert.ok(results.every(result => result.status === 'rejected' && result.reason.code === 'shopify_auth_request_failed'));
  assert.equal(failures, 1);
  assert.equal(await failResolve(env, options(async () => { failures++; return reply(); })), 'synthetic-access-token');
  assert.equal(failures, 2);
});

test('late completion of an old credential exchange cannot overwrite a rotated token', async () => {
  const resolve = createShopifyAdminTokenResolver(), oldGate = deferred(), entered = deferred(); let calls = 0;
  const settings = options(async (_, request) => {
    calls++;
    const secret = new URLSearchParams(request.body).get('client_secret');
    if (secret === env.SHOPIFY_CLIENT_SECRET) { entered.resolve(); await oldGate.promise; return reply(payload({ access_token: 'synthetic-old-token' })); }
    return reply(payload({ access_token: 'synthetic-rotated-token' }));
  });
  const old = resolve(env, settings); await entered.promise;
  const rotated = { ...env, SHOPIFY_CLIENT_SECRET: 'synthetic-rotated-secret' };
  assert.equal(await resolve(rotated, settings), 'synthetic-rotated-token');
  oldGate.resolve(); assert.equal(await old, 'synthetic-old-token');
  assert.equal(await resolve(rotated, settings), 'synthetic-rotated-token'); assert.equal(calls, 2);
});

test('HTTP and authorization failures read no error body and never retry or fall back', async () => {
  for (const [status, code] of [[401, 'shopify_auth_rejected'], [403, 'shopify_auth_rejected'], [429, 'shopify_auth_http_error'], [500, 'shopify_auth_http_error']]) {
    const resolve = createShopifyAdminTokenResolver(); let calls = 0, bodyReads = 0;
    const settings = options(async () => { calls++; return { status, redirected: false, url: '', text: async () => { bodyReads++; throw new Error('private body'); } }; });
    await expectCode(resolve({ ...env, SHOPIFY_ADMIN_ACCESS_TOKEN: 'synthetic-broad-token' }, settings), code);
    assert.equal(calls, 1); assert.equal(bodyReads, 0);
  }
});

test('renewal failure cannot reuse a token that has reached its safety margin', async () => {
  const resolve = createShopifyAdminTokenResolver(); let calls = 0, time = initialTime;
  const settings = { domain, now: () => time, fetchImpl: async () => ++calls === 1 ? reply(payload({ expires_in: 1020 })) : reply({}, { status: 401 }) };
  assert.equal(await resolve(env, settings), 'synthetic-access-token');
  time += 60_000; await expectCode(resolve(env, settings), 'shopify_auth_rejected');
  assert.equal(calls, 2);
});

test('redirect responses and mismatched response URLs are rejected without exposing destinations', async () => {
  for (const [status, redirected, url] of [[302, false, ''], [200, true, `https://${domain}/admin/oauth/access_token`],
    [200, false, 'https://unrelated.example/private'], [200, false, `https://${domain}/different-path`]]) {
    const resolve = createShopifyAdminTokenResolver();
    await expectCode(resolve(env, options(async () => ({ status, redirected, url }))), 'shopify_auth_redirect_rejected');
  }
});

test('upstream errors and malformed response operations disclose only constant codes', async () => {
  const marker = 'synthetic-private-secret https://private.example/secret';
  for (const fetchImpl of [async () => { throw new Error(marker); }, async () => {
    return { status: 200, url: '', headers: new Headers({ 'content-type': 'application/json' }), text: async () => { throw new Error(marker); } };
  }, async () => null, async () => ({ status: '200' }), async () => reply(payload({ extra: marker }))]) {
    try { await createShopifyAdminTokenResolver()(env, options(fetchImpl)); assert.fail('Expected a sanitized rejection'); }
    catch (error) {
      assert.ok(error instanceof SourceError);
      assert.ok(!`${error.stack}${JSON.stringify(error)}`.includes(marker));
      assert.ok(!error.message.includes('https://')); assert.ok(!error.cause);
    }
  }
});

test('clock errors, backward time and invalid injection options fail safely', async () => {
  const settings = options(async () => reply());
  for (const invalid of [() => NaN, () => -1, () => '2026-09-14', () => 0.1, () => { throw new Error('private-clock-error'); }]) {
    await expectCode(createShopifyAdminTokenResolver()(env, { ...settings, now: invalid }), 'shopify_auth_invalid_clock');
  }
  await expectCode(createShopifyAdminTokenResolver()(env, { ...settings, now: 42 }), 'shopify_auth_invalid_options');
  await expectCode(createShopifyAdminTokenResolver()(env, { ...settings, fetchImpl: null }), 'shopify_auth_invalid_options');
  const resolve = createShopifyAdminTokenResolver(); let time = initialTime;
  assert.equal(await resolve(env, { ...settings, now: () => time }), 'synthetic-access-token');
  time--; await expectCode(resolve(env, { ...settings, now: () => time }), 'shopify_auth_invalid_clock');
  for (const requestTimeoutMs of [0, -1, 60_001, 1.1, '1000']) assert.throws(() => createShopifyAdminTokenResolver({ requestTimeoutMs }), SourceError);
});

test('timeout aborts the request, clears concurrent state and permits a later explicit attempt', async () => {
  const resolve = createShopifyAdminTokenResolver({ requestTimeoutMs: 5 }); let signal, calls = 0;
  await expectCode(resolve(env, options(async (_, request) => { calls++; signal = request.signal; return new Promise(() => {}); })), 'shopify_auth_timeout');
  assert.equal(signal.aborted, true); assert.equal(calls, 1);
  assert.equal(await resolve(env, options(async () => { calls++; return reply(); })), 'synthetic-access-token');
  assert.equal(calls, 2);
});
