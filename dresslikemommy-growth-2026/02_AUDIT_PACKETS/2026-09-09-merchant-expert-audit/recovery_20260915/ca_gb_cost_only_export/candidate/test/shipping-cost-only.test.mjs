import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { buildFeed, tsvChunks, COLUMNS } from '../src/generator.js';
import { config as baseConfig, market as baseMarket, now, count, product, variant, snapshot } from './fixtures.js';

globalThis.fetch = () => { throw new Error('network_prohibited_in_local_synthetic_test'); };
const hash = value => createHash('sha256').update(value).digest('hex');
const bindings = JSON.parse(await fs.readFile(new URL('../../dependency_bindings.json', import.meta.url), 'utf8'));
for (const input of bindings.originalInputs) assert.equal(hash(await fs.readFile(input.path)), input.sha256, input.path);
const originalPath = bindings.originalInputs.find(input => input.path.endsWith('/src/generator.js')).path;
const { buildFeed: originalBuild } = await import(pathToFileURL(originalPath));
const holds = JSON.parse(await fs.readFile(new URL('./holds.fixture.json', import.meta.url), 'utf8'));
const evidence = hash('SYNTHETIC TEST ZERO SHIPPING COST RECEIPT; NEVER PRODUCTION AUTHORITY');
const currencies = { US: 'USD', AU: 'AUD', CA: 'CAD', GB: 'GBP' };
const run = (f, options = {}) => buildFeed(f.source, f.config, f.market, { now, ...options });
const old = (f, options = {}) => originalBuild(f.source, f.config, f.market, { now, ...options });

function fixture(country = 'CA', { optIn = true, returnLabels = false, products } = {}) {
  const currency = currencies[country];
  const market = { ...structuredClone(baseMarket), country, currency, key: `${country.toLowerCase()}-en`,
    landingQuery: { country, currency }, marketId: 'gid://shopify/Market/99001',
    expectedCatalogs: [{ id: 'gid://shopify/MarketCatalog/99002', publicationId: 'gid://shopify/Publication/99003' }] };
  if (optIn) market.shippingCostOnly = { country, currency, amount: '0.00', verified: true, evidenceSha256: evidence };
  const config = structuredClone(baseConfig);
  config.eligibilityHolds = structuredClone(holds);
  config.returnPolicy.emitLabels = returnLabels;
  config.markets = [market];
  products ??= [product(1, [variant(101, currency), variant(102, currency)]), product(2, [variant(201, currency)])];
  for (const p of products) p.catalogPublished ??= true;
  const source = snapshot(products, market);
  source.marketContext = { currency, catalogs: structuredClone(market.expectedCatalogs), activeMarketIds: [market.marketId] };
  source.finalMarketContext = structuredClone(source.marketContext);
  return { config, market, source };
}
function heldProducts(currency) {
  return holds.holds.map((hold, index) => {
    const p = product(Number(hold.product_id.split('/').at(-1)), [variant(50000 + index * 2, currency), variant(50001 + index * 2, currency)]);
    p.variants[1].availableForSale = false;
    p.title = ''; p.description = ''; p.featuredMedia = null;
    p.variants.forEach(v => { v.media = null; });
    return p;
  });
}
async function rejected(f, code) { await assert.rejects(run(f), error => error.code === code); }

test('the candidate is derived from the exact active owner profile; configs remain disabled', async () => {
  assert.equal(bindings.profile, 'native-holds-20260914');
  assert.equal(bindings.profileDependenciesMatched, 14);
  assert.equal(bindings.sourceGeneratorSha256, 'a028e2f7f3bb1f0c1f03e222e6b2a608b742f46b6a8f13cc97572885fe009c4f');
  const input = bindings.originalInputs.find(input => input.path.endsWith('/ca_gb_qualification_1917/qualification.config.json'));
  const current = JSON.parse(await fs.readFile(input.path, 'utf8'));
  assert.ok(current.markets.every(m => m.enabled === false && m.landingContextVerified === false && m.shippingCostOnly === undefined));
  assert.equal(holds.holds.length, 6);
  assert.equal(holds.source.sha256, '8ef6615558d3ff08e9b2bcef424041c36e25710be17101bd8145cc46c7b33733');
});

for (const country of ['US', 'AU', 'CA', 'GB']) {
  test(`absent option preserves every ${country} default result and streaming byte with labels on/off`, async () => {
    for (const returnLabels of [false, true]) {
      const f = fixture(country, { optIn: false, returnLabels });
      f.source.products[0].title = 'Blue "outfit" &amp; white';
      f.source.products[1].productType = 'Swimwear';
      const previousIds = [`shopify_${country}_1_101`, `shopify_${country}_9_901`];
      assert.deepEqual(await run(f, { previousIds }), await old(f, { previousIds }));
      assert.deepEqual(await run(f, { previousIds, materialize: false }), await old(f, { previousIds, materialize: false }));
    }
  });
}

for (const country of ['CA', 'GB']) {
  test(`${country} opt-in changes only one TSV column; stream and materialized outputs match`, async () => {
    const f = fixture(country);
    const before = JSON.stringify(f);
    const baseline = await old(f), result = await run(f), stream = await run(f, { materialize: false });
    assert.equal(result.ok, true); assert.equal(result.rows.length, 3);
    assert.equal(result.tsv.split('\n')[0], baseline.tsv.split('\n')[0] + '\tshipping');
    const withoutColumn = result.tsv.trimEnd().split('\n').map(line => line.slice(0, line.lastIndexOf('\t'))).join('\n') + '\n';
    assert.equal(withoutColumn, baseline.tsv);
    assert.deepEqual(result.rows.map(({ shipping, ...row }) => row), baseline.rows);
    assert.ok(result.rows.every(row => row.shipping === `${country}:::0.00 ${currencies[country]}`));
    assert.ok(!stream.columns.includes('return_policy_label') && !stream.columns.includes('returns'));
    assert.ok(!stream.columns.some(c => /handling|transit/.test(c)));
    const { shippingCostOnly, ...diagnostics } = result.diagnostics;
    assert.deepEqual(diagnostics, baseline.diagnostics);
    assert.equal(shippingCostOnly.evidenceSha256, evidence);
    assert.equal(shippingCostOnly.deliveryTimesSubmitted, false);
    assert.match(shippingCostOnly.displayLimit, /crawled or modeled/);
    const streamed = Buffer.concat([...tsvChunks(stream.rows, stream.columns)].map(chunk => Buffer.from(chunk))).toString();
    assert.equal(streamed, result.tsv); assert.equal(stream.bytes, result.bytes);
    assert.equal(hash(streamed), result.sha256);
    for (const row of result.rows) {
      const url = new URL(row.link);
      assert.equal(url.searchParams.get('country'), country);
      assert.equal(url.searchParams.get('currency'), currencies[country]);
      assert.match(url.searchParams.get('variant'), /^\d+$/);
      assert.equal(row.excluded_destination, 'Shopping_ads');
    }
    assert.equal(JSON.stringify(f), before);
    assert.ok(!COLUMNS.includes('shipping'), 'the shared default column array is not mutated');
  });
  test(`${country} retains all six holds, unavailable partition and complete-source-proven archival`, async () => {
    const currency = currencies[country];
    const f = fixture(country, { products: [...heldProducts(currency), product(1, [variant(101, currency)])] });
    const result = await run(f);
    assert.equal(result.ok, true); assert.equal(result.rows.length, 1);
    assert.equal(result.diagnostics.sourceCounts.variants, 13);
    assert.equal(result.diagnostics.eligibilityHolds.removedAvailableRows, 6);
    assert.equal(result.diagnostics.eligibilityHolds.sourceParentIds.length, 6);
    assert.equal(result.diagnostics.exclusions.filter(e => e.code === 'variant_not_available_for_sale').length, 6);
    assert.equal(result.diagnostics.exclusions.length + result.rows.length, 13);
    const next = fixture(country, { products: [product(1, [variant(101, currency)])] });
    const historicalHeldId = `shopify_${country}_${holds.holds[0].product_id.split('/').at(-1)}_50000`;
    const archived = await run(next, { previousIds: [...result.rowIds, historicalHeldId] });
    assert.equal(archived.diagnostics.eligibilityHolds.sourceAbsentParentIds.length, 6);
    assert.deepEqual(archived.diagnostics.lifecycle.removed, [historicalHeldId]);
    const reactivated = await run(f, { previousIds: archived.rowIds });
    assert.deepEqual(reactivated.rowIds, archived.rowIds);
    assert.deepEqual(reactivated.diagnostics.lifecycle.added, []);
  });
}

test('no opt-in carries over to a subsequent US or AU build', async () => {
  await run(fixture('CA')); await run(fixture('GB'));
  for (const country of ['US', 'AU']) {
    const f = fixture(country, { optIn: false });
    assert.deepEqual(await run(f), await old(f));
  }
});

test('invalid or broadened country/language/currency scope is rejected', async () => {
  for (const country of ['US', 'AU']) await rejected(fixture(country), 'shipping_cost_only_scope_mismatch');
  for (const mutate of [
    f => { f.market.shippingCostOnly.country = 'GB'; },
    f => { f.market.shippingCostOnly.currency = 'USD'; },
    f => { f.market.key = 'ca-fr'; f.market.locale = 'fr'; f.source.market.key = 'ca-fr'; f.source.market.locale = 'fr'; },
    f => { f.config.sourceLocale = 'fr'; f.source.sourceLocale = 'fr'; },
  ]) { const f = fixture(); mutate(f); await rejected(f, 'shipping_cost_only_scope_mismatch'); }
});

test('an accidentally global shipping option is rejected rather than silently ignored', async () => {
  for (const optIn of [false, true]) {
    const f = fixture('CA', { optIn });
    f.config.shippingCostOnly = { country: 'CA', currency: 'CAD', amount: '0.00', verified: true, evidenceSha256: evidence };
    await rejected(f, 'shipping_cost_only_must_be_market_scoped');
  }
});

test('missing fields, unknown fields and ETA/return/service additions fail closed', async () => {
  for (const value of [null, false, 'free', [], Object.create(null)]) {
    const f = fixture(); f.market.shippingCostOnly = value;
    await rejected(f, 'invalid_shipping_cost_only_configuration');
  }
  for (const field of ['verified', 'evidenceSha256', 'country', 'currency', 'amount']) {
    const f = fixture(); delete f.market.shippingCostOnly[field]; await rejected(f, 'invalid_shipping_cost_only_fields');
  }
  for (const field of ['min_transit_time', 'max_handling_time', 'service', 'returns', 'return_policy_label', 'extra']) {
    const f = fixture(); f.market.shippingCostOnly[field] = 'ignored'; await rejected(f, 'invalid_shipping_cost_only_fields');
  }
});

test('nonzero, numeric, padded and noncanonical cost values reject without conversion', async () => {
  for (const amount of ['0.01', '-1', '1', '0', '0.0', 0, ' 0.00 ', '0.00 CAD', 'free']) {
    const f = fixture(); f.market.shippingCostOnly.amount = amount;
    await rejected(f, 'shipping_cost_only_must_be_zero');
  }
});

test('verification must be literal true and bind a nonempty SHA256 receipt', async () => {
  for (const verified of [false, null, 'true', 1]) {
    const f = fixture(); f.market.shippingCostOnly.verified = verified; await rejected(f, 'shipping_cost_only_unverified');
  }
  for (const value of ['', 'receipt.json', 'a'.repeat(63), 'a'.repeat(65), '0'.repeat(64), 'G'.repeat(64), 123]) {
    const f = fixture(); f.market.shippingCostOnly.evidenceSha256 = value; await rejected(f, 'shipping_cost_only_unverified');
  }
});

test('disabled or unverified landing scope cannot be bypassed even for an empty complete source', async () => {
  for (const products of [undefined, []]) {
    for (const enabled of [false, undefined, 'true']) {
      const f = fixture('CA', { products }); f.market.enabled = enabled;
      await rejected(f, 'shipping_cost_only_market_disabled');
    }
    const f = fixture('CA', { products }); f.market.landingContextVerified = false;
    await rejected(f, 'landing_context_unverified');
  }
  for (const query of [{}, { country: 'US', currency: 'CAD' }, { country: 'CA', currency: 'USD' }]) {
    const f = fixture(); f.market.landingQuery = query; await rejected(f, 'shipping_cost_only_landing_scope_mismatch');
  }
});

test('new opt-in requires existing holds and explicit disabled return-label emission', async () => {
  const f = fixture(); delete f.config.eligibilityHolds; await rejected(f, 'shipping_cost_only_requires_eligibility_holds');
  for (const emitLabels of [true, undefined, null]) {
    const f = fixture(); f.config.returnPolicy.emitLabels = emitLabels;
    await rejected(f, 'shipping_cost_only_requires_return_labels_disabled');
  }
  const malformed = fixture(); malformed.config.eligibilityHolds.holds.push(structuredClone(holds.holds[0]));
  await rejected(malformed, 'invalid_or_duplicate_held_parent');
});

const sourceFaults = [
  ['pagination', f => { f.source.paginationComplete = false; }, 'incomplete_snapshot'],
  ['shop identity', f => { f.source.shop.id = 'wrong'; }, 'snapshot_identity_mismatch'],
  ['stale clock', f => { f.source.completedAt = '2026-09-09T14:00:00Z'; }, 'stale_or_future_snapshot'],
  ['future clock', f => { f.source.completedAt = '2026-09-12T14:00:00Z'; }, 'stale_or_future_snapshot'],
  ['manifest drift', f => { f.source.finalManifest[0].updatedAt = 'different'; }, 'manifest_mismatch'],
  ['incomplete variants', f => { f.source.products[0].variantsCount = count(3); f.source.finalManifest[0].variantsCount = count(3); }, 'incomplete_variants'],
  ['duplicate variant', f => { f.source.products[0].variants[1].id = f.source.products[0].variants[0].id; }, 'duplicate_variant_id'],
  ['market context drift', f => { f.source.finalMarketContext.currency = 'USD'; }, 'snapshot_market_context_changed'],
  ['catalog identity', f => { f.market.expectedCatalogs[0].id = 'wrong'; }, 'snapshot_catalog_identity_mismatch'],
];
for (const [name, mutate, code] of sourceFaults) {
  test(`shipping opt-in preserves existing ${name} source rejection`, async () => {
    const f = fixture(); mutate(f);
    await assert.rejects(old(f), error => error.code === code);
    await rejected(f, code);
  });
}

test('malformed currency, price, numeric identity and unavailable state never yield a partial feed', async () => {
  for (const [mutate, code] of [
    [v => { v.contextualPricing.price.currencyCode = 'USD'; }, 'contextual_currency_mismatch'],
    [v => { v.contextualPricing.price.amount = '0'; }, 'non_positive_price'],
    [v => { v.contextualPricing.price.amount = '1.001'; }, 'price_requires_rounding'],
    [v => { delete v.availableForSale; }, 'missing_variant_availability'],
  ]) {
    const f = fixture(); mutate(f.source.products[0].variants[1]);
    const result = await run(f);
    assert.equal(result.ok, false); assert.equal(result.tsv, null); assert.deepEqual(result.rows, []);
    assert.ok(result.diagnostics.errors.some(error => error.code === code));
  }
  const f = fixture(); f.source.products[0].variants[0].id = '101'; await rejected(f, 'invalid_shopify_id');
  const held = fixture('CA', { products: [...heldProducts('CAD'), product(1, [variant(101, 'CAD')])] });
  held.source.products[0].variants[0].contextualPricing.price.currencyCode = 'USD';
  assert.equal((await run(held)).ok, false);
});

test('publication and unavailable exclusions retain exact membership and shipping applies only to kept rows', async () => {
  const kept = product(1, [variant(101, 'CAD'), variant(102, 'CAD')]); kept.variants[1].availableForSale = false;
  const hidden = product(2, [variant(201, 'CAD')]); hidden.countryPublished = false;
  const outsideCatalog = product(3, [variant(301, 'CAD')]); outsideCatalog.catalogPublished = false;
  const f = fixture('CA', { products: [kept, hidden, outsideCatalog] });
  const result = await run(f);
  assert.deepEqual(result.rowIds, ['shopify_CA_1_101']);
  assert.equal(result.rows[0].shipping, 'CA:::0.00 CAD');
  assert.deepEqual(result.diagnostics.exclusions.map(e => e.code).sort(), ['not_in_market_catalog', 'not_published_in_country', 'variant_not_available_for_sale']);
});

test('active owner dependencies and current CA/GB config bytes are still unchanged after all builds', async () => {
  for (const input of bindings.originalInputs) assert.equal(hash(await fs.readFile(input.path)), input.sha256, input.path);
});
