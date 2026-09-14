import test from 'node:test';
import assert from 'node:assert/strict';
import { enqueueRefresh, consumeRefresh } from '../src/checkpoint.js';
import { currentManifest, refreshMarket } from '../src/worker.js';
import automation from '../src/automation.js';
import { streamOptions } from './node-streams.js';
import { config, market, now, product, variant, source, Bucket } from './fixtures.js';

const initial = '01234567-89ab-4cde-8012-3456789abcde';
function environment(options = {}) {
  const queue = { messages: [], failNext: false, async send(message) {
    if (this.failNext) { this.failNext = false; throw new Error('queue_unavailable'); }
    this.messages.push(structuredClone(message));
  } };
  const cfg = { ...structuredClone(config), refresh: { maxSourceCallsPerInvocation: 20, maxJobAgeMinutes: 120, minRefreshMinutes: 60 }, ...options };
  return { MERCHANT_CONFIG_JSON: JSON.stringify(cfg), MERCHANT_FEED_BUCKET: new Bucket(), MERCHANT_REFRESH_QUEUE: queue };
}
async function run(env, api, time = now) {
  await enqueueRefresh(env, market.key, { now: () => time, randomId: () => crypto.randomUUID() });
  const steps = [];
  while (env.MERCHANT_REFRESH_QUEUE.messages.length) {
    const message = env.MERCHANT_REFRESH_QUEUE.messages.shift();
    const prior = api.calls();
    const result = await consumeRefresh(env, message, { streamOptions, graphql: api.graphql, now: () => time });
    assert.ok(api.calls() - prior <= 20, 'maximum 20 external logical operations per Queue consumer');
    steps.push(result); assert.ok(steps.length <= 1000);
  }
  return steps;
}

test('240-parent complete refresh resumes below Free subrequest limit and promotes once', async () => {
  const env = environment(), api = source(Array.from({ length: 240 }, (_, i) => product(i + 1)));
  const steps = await run(env, api);
  assert.equal(api.calls(), 257); assert.equal(steps.length, 13); assert.equal(steps.at(-1).complete, true);
  assert.equal(steps.at(-1).rows, 240);
  assert.equal(env.MERCHANT_FEED_BUCKET.writes.filter(k => k === 'merchant/us-en/current.json').length, 1);
  assert.ok(steps.slice(0, -1).every(s => s.checkpointed));
  assert.equal([...env.MERCHANT_FEED_BUCKET.objects.keys()].filter(key => key.startsWith('merchant/jobs/')).length, 0);
});
test('large nested variant pagination remains exact across checkpoint boundaries', async () => {
  const env = environment({ refresh: { maxSourceCallsPerInvocation: 2 } });
  const api = source([product(1, Array.from({ length: 91 }, (_, i) => variant(i + 100)))]);
  const steps = await run(env, api); assert.equal(steps.at(-1).rows, 91); assert.equal(api.calls(), 7);
});
test('resumed foreign feeds preserve translation observation age, including legacy journals', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr', marketId: 'gid://shopify/Market/544735329',
    landingBaseUrl: `${market.landingBaseUrl}/fr`, translationFailureMode: 'exclude_product' };
  for (const [minutes, legacy, expectedSuccess] of [[30, false, true], [90, false, false], [90, true, false]]) {
    const env = environment({ markets: [target], maxSnapshotAgeHours: 1,
      refresh: { maxSourceCallsPerInvocation: 4, maxJobAgeMinutes: 120, minRefreshMinutes: 60 } });
    const api = source([product()], { intercept: (r, q, variables) => {
      if (q.includes('query MerchantFeedProducts')) r.products.nodes[0].translations = variables.marketId === null ? [
        { locale: 'fr', key: 'title', value: 'Tenue', outdated: false },
        { locale: 'fr', key: 'body_html', value: '<p>Bleue</p>', outdated: false },
      ] : [];
    } });
    await enqueueRefresh(env, target.key, { now: () => now });
    const first = await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { streamOptions, graphql: api.graphql, now: () => now });
    assert.equal(first.checkpointed, true); assert.equal(api.calls(), 4);
    const journalKey = [...env.MERCHANT_FEED_BUCKET.objects.keys()].find(k => k.startsWith('merchant/jobs/'));
    const journal = JSON.parse(await (await env.MERCHANT_FEED_BUCKET.get(journalKey)).text());
    assert.ok(journal.entries.every(e => e.observedAt === now.toISOString()));
    if (legacy) {
      for (const entry of journal.entries) delete entry.observedAt;
      await env.MERCHANT_FEED_BUCKET.put(journalKey, JSON.stringify(journal));
    }
    const resumedAt = new Date(now.getTime() + minutes * 60000);
    const result = await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { streamOptions, graphql: api.graphql, now: () => resumedAt });
    assert.equal(api.calls(), 6, 'cached translation pages are replayed without new source requests');
    if (expectedSuccess) {
      assert.equal(result.complete, true);
      assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, target.key)).manifest.rows, 1);
    } else {
      assert.equal(result.code, 'stale_or_incomplete_translation_context');
      assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, target.key)).manifest, null);
    }
  }
});
test('new, deleted, archived, unpublished, unavailable and returned variants reconcile on every successful run', async () => {
  const env = environment();
  await run(env, source([product(1), product(2), product(3), product(4), product(5)]));
  const old = (await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).manifest;
  const unpublished = product(3); unpublished.onlinePublished = false;
  const countryRemoved = product(4); countryRemoved.countryPublished = false;
  const soldOut = product(5); soldOut.variants[0].availableForSale = false;
  // Parents 1 and 2 are absent from the next ACTIVE source: deleted or archived.
  await run(env, source([unpublished, countryRemoved, soldOut, product(6)]), new Date(now.getTime() + 3600000));
  let present = (await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).manifest;
  assert.deepEqual(present.rowIds, ['shopify_US_6_601']); assert.equal(old.rowIds.length, 5);
  soldOut.variants[0].availableForSale = true;
  await run(env, source([soldOut, product(6)]), new Date(now.getTime() + 7200000));
  present = (await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).manifest;
  assert.deepEqual(present.rowIds, ['shopify_US_5_501', 'shopify_US_6_601']);
});
test('partial source failure retains previous complete feed and records actionable failure', async () => {
  const env = environment(); await run(env, source([product()]));
  const before = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  const api = source(Array.from({ length: 35 }, (_, i) => product(i + 1)), { intercept: (data, query, variables, calls) => {
    if (calls === 22) throw new Error('synthetic_transport_failure');
  } });
  const steps = await run(env, api, new Date(now.getTime() + 3600000));
  assert.equal(steps.at(-1).failed, true);
  const after = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  assert.equal(after.etag, before.etag); assert.equal(after.manifest.sha256, before.manifest.sha256);
  const status = JSON.parse(await (await env.MERCHANT_FEED_BUCKET.get('merchant/us-en/status.json')).text());
  assert.equal(status.ok, false); assert.equal(status.code, 'refresh_source_failed');
});
test('source mutation during paused read fails reconciliation and preserves old pointer', async () => {
  const env = environment(); await run(env, source([product()]));
  const before = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  const api = source(Array.from({ length: 25 }, (_, i) => product(i + 1)), { intercept: (data, query) => {
    if (query.includes('query MerchantFeedManifest')) data.products.nodes[0].updatedAt = 'changed';
  } });
  const steps = await run(env, api, new Date(now.getTime() + 3600000));
  assert.equal(steps.at(-1).code, 'catalog_changed_during_read');
  assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).etag, before.etag);
});
test('old delivery repairs a failed continuation send immediately; Cron also recovers a lost message', async () => {
  const env = environment({ refresh: { maxSourceCallsPerInvocation: 2 } }), api = source([product()]);
  await enqueueRefresh(env, market.key, { now: () => now, randomId: () => initial });
  const message = env.MERCHANT_REFRESH_QUEUE.messages.shift();
  env.MERCHANT_REFRESH_QUEUE.failNext = true;
  await assert.rejects(consumeRefresh(env, message, { streamOptions, graphql: api.graphql, now: () => now }), /queue_unavailable/);
  assert.equal((await consumeRefresh(env, message, { streamOptions, graphql: api.graphql, now: () => now })).resumed, 'latest_checkpoint_requeued');
  assert.equal(api.calls(), 2);
  assert.equal(env.MERCHANT_REFRESH_QUEUE.messages.length, 1);
  env.MERCHANT_REFRESH_QUEUE.messages.length = 0;
  const resume = await enqueueRefresh(env, market.key, { now: () => now }); assert.equal(resume.resumed, true);
  while (env.MERCHANT_REFRESH_QUEUE.messages.length) await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { streamOptions, graphql: api.graphql, now: () => now });
  assert.equal(api.calls(), 5); assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).manifest.rows, 1);
});
test('configuration changes abort in-flight journal without source reads or promotion', async () => {
  const env = environment(), api = source([product()]);
  await enqueueRefresh(env, market.key, { now: () => now });
  const cfg = JSON.parse(env.MERCHANT_CONFIG_JSON); cfg.maxFeedAgeHours = 12; env.MERCHANT_CONFIG_JSON = JSON.stringify(cfg);
  const result = await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { streamOptions, graphql: api.graphql, now: () => now });
  assert.equal(result.code, 'refresh_config_changed'); assert.equal(api.calls(), 0);
  assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).manifest, null);
});
test('unsafe batch size retries without multiplying the per-invocation request budget', async () => {
  let retried = 0, acked = 0;
  await automation.queue({ messages: Array.from({ length: 2 }, () => ({ body: {}, retry: () => retried++, ack: () => acked++ })) }, {});
  assert.equal(retried, 2); assert.equal(acked, 0);
});
test('checkpoint data contains neither credentials nor URL-bearing source tags', async () => {
  const env = environment({ refresh: { maxSourceCallsPerInvocation: 2 } }), p = product(); p.tags = ['Final Sale', 'https://private.example/source'];
  await run(env, source([p]));
  const persisted = [...env.MERCHANT_FEED_BUCKET.objects.values()].map(v => v.text).join('\n');
  assert.ok(!persisted.includes('private.example')); assert.ok(!persisted.includes('X-Shopify-Access-Token'));
  assert.ok(persisted.includes('Final Sale'));
});
test('a newer independent promotion wins against an older paused refresh', async () => {
  const env = environment({ refresh: { maxSourceCallsPerInvocation: 2 } }), api = source([product()]);
  await enqueueRefresh(env, market.key, { now: () => now });
  const initialMessage = env.MERCHANT_REFRESH_QUEUE.messages.shift();
  await consumeRefresh(env, initialMessage, { streamOptions, graphql: api.graphql, now: () => now });
  await refreshMarket(env, market.key, { graphql: source([product(9)]).graphql, now: () => now });
  const newer = await currentManifest(env.MERCHANT_FEED_BUCKET, market.key);
  const steps = [];
  while (env.MERCHANT_REFRESH_QUEUE.messages.length) steps.push(await consumeRefresh(env, env.MERCHANT_REFRESH_QUEUE.messages.shift(), { streamOptions, graphql: api.graphql, now: () => now }));
  assert.equal(steps.at(-1).code, 'concurrent_refresh');
  assert.equal((await currentManifest(env.MERCHANT_FEED_BUCKET, market.key)).etag, newer.etag);
});
test('crash after feed promotion recovers idempotently without another source call', async () => {
  const env = environment({ refresh: { maxSourceCallsPerInvocation: 2 } }), api = source([product()]);
  const originalPut = env.MERCHANT_FEED_BUCKET.put.bind(env.MERCHANT_FEED_BUCKET); let crash = true;
  env.MERCHANT_FEED_BUCKET.put = async (key, value, options) => {
    if (key.endsWith('/refresh.json') && JSON.parse(value).status === 'COMPLETE' && crash) { crash = false; throw new Error('crash_after_promotion'); }
    return originalPut(key, value, options);
  };
  await enqueueRefresh(env, market.key, { now: () => now }); let failedMessage;
  while (env.MERCHANT_REFRESH_QUEUE.messages.length) {
    const message = env.MERCHANT_REFRESH_QUEUE.messages.shift();
    try { await consumeRefresh(env, message, { streamOptions, graphql: api.graphql, now: () => now }); }
    catch (error) { assert.equal(error.message, 'crash_after_promotion'); failedMessage = message; }
  }
  assert.ok(failedMessage); const before = api.calls();
  const result = await consumeRefresh(env, failedMessage, { streamOptions, graphql: api.graphql, now: () => now });
  assert.equal(result.recoveredPromotion, true); assert.equal(api.calls(), before);
  assert.equal(env.MERCHANT_FEED_BUCKET.writes.filter(k => k === 'merchant/us-en/current.json').length, 1);
});
