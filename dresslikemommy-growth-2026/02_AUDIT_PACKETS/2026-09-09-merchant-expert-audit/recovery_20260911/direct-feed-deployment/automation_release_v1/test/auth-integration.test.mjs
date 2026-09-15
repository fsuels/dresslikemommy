import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createConfiguredAdminReader } from '../src/admin-reader.js';
import { enqueueRefresh, consumeRefresh } from '../src/checkpoint.js';
import { currentManifest, refreshMarket, runtimeConfig } from '../src/worker.js';
import { config, market, now, product, source, Bucket } from './fixtures.js';

test('split cloud variables reconstruct the exact reviewed configuration below conservative size limits', async () => {
  const reviewed = JSON.parse(await fs.readFile(new URL('../config.json', import.meta.url), 'utf8'));
  const base = structuredClone(reviewed), holds = base.eligibilityHolds;
  delete base.eligibilityHolds; base.eligibilityHoldsExternal = true;
  const env = { MERCHANT_CONFIG_JSON: JSON.stringify(base), MERCHANT_ELIGIBILITY_HOLDS_JSON: JSON.stringify(holds) };
  assert.ok(Object.values(env).every(value => Buffer.byteLength(value, 'utf8') < 5000));
  assert.deepEqual(runtimeConfig(env), reviewed);
  assert.equal(JSON.stringify(runtimeConfig(env)), JSON.stringify(reviewed), 'job config fingerprints remain identical');
  for (const invalid of [
    { MERCHANT_CONFIG_JSON: env.MERCHANT_CONFIG_JSON },
    { ...env, MERCHANT_ELIGIBILITY_HOLDS_JSON: 'null' },
    { ...env, MERCHANT_ELIGIBILITY_HOLDS_JSON: '{' },
    { ...env, MERCHANT_CONFIG_JSON: JSON.stringify(reviewed) },
    { ...env, MERCHANT_CONFIG_JSON: JSON.stringify({ ...reviewed, eligibilityHoldsExternal: true }) },
  ]) assert.throws(() => runtimeConfig(invalid), error => error.code === 'feed_config_missing_or_invalid');
});

test('explicit cloud mode never falls back and records failure without changing the current feed', async () => {
  const env = { MERCHANT_CONFIG_JSON: JSON.stringify(config), MERCHANT_FEED_BUCKET: new Bucket(),
    MERCHANT_REFRESH_QUEUE: { messages: [], async send(message) { this.messages.push(message); } } };
  await refreshMarket(env, market.key, { graphql: source([product()]).graphql, now: () => now });
  const before = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  const pointerWrites = env.MERCHANT_FEED_BUCKET.writes.filter(key => key.endsWith('/current.json')).length;
  env.SHOPIFY_AUTH_MODE = 'client_credentials';
  env.SHOPIFY_ADMIN_ACCESS_TOKEN = 'synthetic_legacy_token_must_not_be_used';
  const later = new Date(now.getTime() + 3_600_000);
  await enqueueRefresh(env, market.key, { now: () => later });
  const result = await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { now: () => later });
  assert.deepEqual(result, { failed: true, code: 'shopify_auth_missing_credentials' });
  assert.deepEqual(await currentManifest(env.MERCHANT_FEED_BUCKET, market.key), before);
  assert.equal(env.MERCHANT_FEED_BUCKET.writes.filter(key => key.endsWith('/current.json')).length, pointerWrites);
  const control = JSON.parse(await (await env.MERCHANT_FEED_BUCKET.get('merchant/us-en/refresh.json')).text());
  assert.equal(control.status, 'FAILED');
  assert.equal(control.code, 'shopify_auth_missing_credentials');
  assert.ok(!JSON.stringify([...env.MERCHANT_FEED_BUCKET.objects]).includes(env.SHOPIFY_ADMIN_ACCESS_TOKEN));
});

test('misconfigured credential mode rejects before any authentication request', async () => {
  for (const [env, code] of [
    [{ SHOPIFY_AUTH_MODE: 'legacy', SHOPIFY_ADMIN_ACCESS_TOKEN: 'synthetic_legacy' }, 'shopify_auth_mode_invalid'],
    [{ SHOPIFY_CLIENT_ID: 'synthetic_id', SHOPIFY_CLIENT_SECRET: 'synthetic_secret' }, 'shopify_auth_mode_required'],
  ]) {
    let calls = 0;
    await assert.rejects(createConfiguredAdminReader(env, config, { fetchImpl: async () => { calls++; } }),
      error => error.code === code);
    assert.equal(calls, 0);
  }
});

test('cloud reader exchanges only at the configured shop and uses the narrow token for Admin reads', async () => {
  const calls = [], token = 'synthetic_catalog_only_token';
  const read = await createConfiguredAdminReader({ SHOPIFY_AUTH_MODE: 'client_credentials',
    SHOPIFY_CLIENT_ID: 'synthetic_integration_id', SHOPIFY_CLIENT_SECRET: 'synthetic_integration_secret',
    SHOPIFY_ADMIN_ACCESS_TOKEN: 'synthetic_broad_token_ignored' }, config, {
    domain: 'unrelated-synthetic.myshopify.com', now: () => now,
    fetchImpl: async (url, options) => {
      calls.push({ url, options });
      if (url.endsWith('/admin/oauth/access_token')) return new Response(JSON.stringify({
        access_token: token, scope: 'read_products,read_publications,read_markets,read_locales,read_translations,read_metaobjects',
        expires_in: 86399,
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      return new Response(JSON.stringify({ data: { currentAppInstallation: { accessScopes: [] } } }),
        { status: 200, headers: { 'Content-Type': 'application/json' } });
    },
  });
  await read('query MerchantAutomationCredentialScopes { currentAppInstallation { accessScopes { handle } } }', {});
  assert.equal(calls.length, 2);
  assert.equal(calls[0].url, `https://${config.storeDomain}/admin/oauth/access_token`);
  assert.equal(calls[0].options.redirect, 'error');
  assert.equal(calls[1].url, `https://${config.storeDomain}/admin/api/${config.apiVersion}/graphql.json`);
  assert.equal(calls[1].options.headers['X-Shopify-Access-Token'], token);
  assert.ok(!JSON.stringify(calls).includes('synthetic_broad_token_ignored'));
});
