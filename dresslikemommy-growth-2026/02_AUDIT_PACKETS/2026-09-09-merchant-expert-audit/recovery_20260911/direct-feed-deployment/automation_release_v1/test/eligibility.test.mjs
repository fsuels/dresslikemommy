import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { SourceError } from '../src/collector.js';
import { buildFeed, sha256 } from '../src/generator.js';
import { readEligibilityHolds } from '../src/eligibility.js';
import { refreshMarket, currentManifest } from '../src/worker.js';
import { config, market, now, variant, product, snapshot, source, Bucket } from './fixtures.js';

const prepared = JSON.parse(await readFile(new URL('../config.json', import.meta.url), 'utf8'));
const canonicalBytes = await readFile(new URL('../../local_lifecycle_interim/eligibility_holds_20260911.json', import.meta.url), 'utf8');
const policy = prepared.eligibilityHolds;
const cfg = { ...config, eligibilityHolds: policy };
const parentNumbers = policy.holds.map(hold => Number(hold.product_id.split('/').at(-1)));
const build = (products, target = market, options = {}, customConfig = cfg) => buildFeed(snapshot(products, target), customConfig, target, { now, ...options });
function translated(p, locale) {
  p.translations = [
    { locale, key: 'title', value: 'Tenue bleue', outdated: false },
    { locale, key: 'body_html', value: '<p>Bleu &amp; blanc.</p>', outdated: false },
  ];
  return p;
}
function held(index = 0, currency = 'USD', count = 2) {
  return product(parentNumbers[index], Array.from({ length: count }, (_, offset) => variant(10000 + index * 10 + offset, currency)));
}

test('prepared policy preserves the six exact canonical entries and binds their source', async () => {
  assert.equal(policy.source.sha256, '8ef6615558d3ff08e9b2bcef424041c36e25710be17101bd8145cc46c7b33733');
  assert.equal(await sha256(canonicalBytes), policy.source.sha256);
  assert.equal(policy.scope, 'all_markets_and_locales');
  assert.deepEqual(policy.holds, JSON.parse(canonicalBytes).holds);
  assert.equal(readEligibilityHolds(policy).parents.size, 6);
});

test('all six held parents exclude every available variant across countries and languages', async () => {
  for (const [country, currency] of [['US', 'USD'], ['AU', 'AUD'], ['CA', 'CAD'], ['GB', 'GBP']]) {
    for (const locale of ['en', 'es', 'fr', 'de']) {
      const target = { ...market, key: `${country.toLowerCase()}-${locale}`, country, currency, locale,
        landingBaseUrl: market.landingBaseUrl + (locale === 'en' ? '' : `/${locale}`), landingQuery: { country, currency } };
      const heldProducts = parentNumbers.map((_, index) => {
        const p = held(index, currency, 3);
        p.variants[2].availableForSale = false;
        p.title = ''; p.description = ''; p.translations = [];
        p.featuredMedia = null;
        for (const v of p.variants) { v.media = null; v.selectedOptions = []; }
        return p;
      });
      const eligible = translated(product(1, [variant(101, currency)]), locale);
      const result = await build([...heldProducts, eligible], target);
      assert.equal(result.ok, true, target.key);
      assert.deepEqual(result.rowIds, [`shopify_${country}_1_101`]);
      assert.equal(result.rows[0].price, `21.90 ${currency}`);
      assert.deepEqual(result.diagnostics.sourceCounts, { parents: 7, variants: 19 });
      assert.equal(result.diagnostics.eligibilityHolds.removedAvailableRows, 12);
      assert.equal(result.diagnostics.eligibilityHolds.sourceParentIds.length, 6);
      assert.equal(result.diagnostics.exclusions.filter(row => row.code === 'variant_not_available_for_sale').length, 6);
      assert.equal(new Set(result.diagnostics.exclusions.map(row => row.id)).size, 18);
      assert.equal(result.diagnostics.exclusions.reduce((sum, row) => sum + row.variants, 0) + result.rows.length, 19);
      for (const hold of policy.holds) {
        assert.equal(result.diagnostics.eligibilityHolds.removedRowsByParent[hold.product_id], 2);
        assert.ok(result.diagnostics.exclusions.filter(row => row.productId === hold.product_id && row.code === 'reviewed_parent_eligibility_hold')
          .every(row => row.reason === hold.reason));
      }
    }
  }
});

test('retained TSV rows are byte-identical and absence of matching holds changes no feed bytes', async () => {
  const kept = product(1, [variant(101), variant(102)]); kept.title = 'Blue\t"outfit"\n&copy;';
  const products = [held(), kept];
  const before = await build(products, market, {}, config);
  const after = await build(products);
  const expected = before.tsv.split('\n').filter((line, index) => index === 0 || !line.startsWith(`shopify_US_${parentNumbers[0]}_`)).join('\n');
  assert.equal(after.tsv, expected);
  assert.deepEqual(after.rows, before.rows.filter(row => row.item_group_id === 'shopify_US_1'));
  const withUnmatchedHolds = await build([kept]);
  const withoutHolds = await build([kept], market, {}, config);
  assert.equal(withUnmatchedHolds.tsv, withoutHolds.tsv);
  assert.equal(withUnmatchedHolds.sha256, withoutHolds.sha256);
});

test('availability and publication exclusions take precedence without counting variants twice', async () => {
  const available = held(0, 'USD', 3); available.variants[1].availableForSale = false;
  const notPublished = held(1); notPublished.countryPublished = false;
  const eligible = product(1, [variant(101), variant(102)]); eligible.variants[1].availableForSale = false;
  const result = await build([available, notPublished, eligible]);
  assert.equal(result.ok, true);
  assert.equal(result.diagnostics.eligibilityHolds.removedAvailableRows, 2);
  assert.equal(result.diagnostics.exclusions.filter(row => row.code === 'variant_not_available_for_sale').length, 2);
  assert.equal(result.diagnostics.exclusions.find(row => row.code === 'not_published_in_country').variants, 2);
  assert.equal(result.diagnostics.exclusions.reduce((sum, row) => sum + row.variants, 0) + result.rows.length, 7);
  assert.equal(result.diagnostics.outOfStock, 0);
});

test('archiving a held parent does not invalidate a complete source and reactivation keeps its hold', async () => {
  const existingIds = [`shopify_US_${parentNumbers[0]}_10000`, 'shopify_US_1_101'];
  const archived = await build([product()], market, { previousIds: existingIds });
  assert.equal(archived.ok, true);
  assert.ok(archived.diagnostics.eligibilityHolds.sourceAbsentParentIds.includes(policy.holds[0].product_id));
  assert.deepEqual(archived.diagnostics.lifecycle.removed, [existingIds[0]]);
  const reactivated = await build([held(), product()], market, { previousIds: archived.rowIds });
  assert.deepEqual(reactivated.rowIds, archived.rowIds);
  assert.equal(reactivated.diagnostics.eligibilityHolds.removedAvailableRows, 2);
  assert.deepEqual(reactivated.diagnostics.lifecycle.added, []);
});

test('a hold cannot hide incomplete source, source drift, duplicate IDs or malformed availability', async () => {
  for (const mutate of [
    s => { s.paginationComplete = false; },
    s => { s.products[0].variants.pop(); },
    s => { s.finalManifest = s.finalManifest.slice(1); },
    s => { s.products.pop(); },
    s => { s.products[0].variants[1].id = s.products[0].variants[0].id; },
  ]) {
    const s = snapshot([held(), product()]); mutate(s);
    await assert.rejects(buildFeed(s, cfg, market, { now }), SourceError);
  }
  const malformedId = held(); malformedId.variants[0].id = 'wrong-variant-id';
  await assert.rejects(build([malformedId, product()]), /invalid_shopify_id/);
  const unavailableUnknown = held(); delete unavailableUnknown.variants[0].availableForSale;
  const failed = await build([unavailableUnknown, product()]);
  assert.equal(failed.ok, false); assert.equal(failed.tsv, null);
  assert.equal(failed.diagnostics.errors[0].code, 'missing_variant_availability');
});

test('held rows preserve native-price validation and global landing gates', async () => {
  for (const [mutation, expected] of [
    [v => { v.contextualPricing.price.currencyCode = 'CAD'; }, 'contextual_currency_mismatch'],
    [v => { v.contextualPricing.price.amount = '0'; }, 'non_positive_price'],
    [v => { v.contextualPricing.price.amount = '12.001'; }, 'price_requires_rounding'],
  ]) {
    const p = held(); mutation(p.variants[0]);
    const failed = await build([p, product()]);
    assert.equal(failed.ok, false); assert.equal(failed.tsv, null); assert.deepEqual(failed.rows, []);
    assert.equal(failed.diagnostics.errors[0].code, expected);
  }
  await assert.rejects(build([held()], { ...market, landingContextVerified: false }), /landing_context_unverified/);
  await assert.rejects(build([held()], { ...market, landingBaseUrl: 'http://invalid.example' }), /invalid_landing_base/);
});

test('held customer content does not stop Spanish refresh, while unheld translation policy is unchanged', async () => {
  const target = { ...market, key: 'us-es', locale: 'es', landingBaseUrl: `${market.landingBaseUrl}/es` };
  const knownHeld = held(); knownHeld.translations = [{ locale: 'es', key: 'title', value: 'Antiguo', outdated: true }];
  const healthy = translated(product(1), 'es');
  assert.equal((await build([knownHeld, healthy], target)).ok, true);
  const stale = translated(product(2), 'es'); stale.translations[0].outdated = true;
  const strict = await build([knownHeld, healthy, stale], target);
  assert.equal(strict.ok, false); assert.equal(strict.tsv, null);
  const excluded = await build([knownHeld, healthy, stale], { ...target, translationFailureMode: 'exclude_product' });
  assert.equal(excluded.ok, true); assert.deepEqual(excluded.rowIds, ['shopify_US_1_101']);
  assert.equal(excluded.diagnostics.eligibilityHolds.removedAvailableRows, 2);
  assert.equal(excluded.diagnostics.exclusions.filter(row => row.reason === 'translation_unusable').length, 1);
});

test('held return exceptions are absent from emitted exception counts and return cohorts', async () => {
  const heldException = held(); heldException.productType = 'Swimwear';
  const keptException = product(); keptException.productType = 'Swimwear';
  const result = await build([heldException, keptException]);
  assert.equal(result.ok, true);
  assert.equal(result.diagnostics.exceptionRows, 1);
  assert.deepEqual(result.diagnostics.returnCohorts.map(row => row.productId), [keptException.id]);
});

test('malformed hold policy fails closed and absent policy retains the previous generator contract', () => {
  assert.equal(readEligibilityHolds(undefined).parents.size, 0);
  for (const mutate of [
    spec => { spec.scope = 'us-en'; },
    spec => { spec.source.sha256 = 'wrong'; },
    spec => { spec.holds = null; },
    spec => { spec.holds.push(structuredClone(spec.holds[0])); },
    spec => { spec.holds[0].product_id = '7516369715297'; },
    spec => { spec.holds[0].reason = ' '; },
    spec => { spec.holds[0].release_condition = null; },
    spec => { spec.holds[0].evidence = []; },
  ]) {
    const invalid = structuredClone(policy); mutate(invalid);
    assert.throws(() => readEligibilityHolds(invalid), SourceError);
  }
  assert.throws(() => readEligibilityHolds(null), SourceError);
});

test('the existing Worker config path enforces holds without additional deployment code', async () => {
  const bucket = new Bucket();
  const p = held(); p.featuredMedia = null; p.variants.forEach(v => { v.media = null; });
  const result = await refreshMarket({ MERCHANT_CONFIG_JSON: JSON.stringify(cfg), MERCHANT_FEED_BUCKET: bucket }, market.key,
    { graphql: source([p, product()]).graphql, now: () => now });
  const current = (await currentManifest(bucket, market.key)).manifest;
  assert.equal(result.manifest.rows, 1);
  assert.deepEqual(current.rowIds, ['shopify_US_1_101']);
  assert.equal(current.sourceVariants, 3);
  assert.ok(!(await (await bucket.get(current.objectKey)).text()).includes(`shopify_US_${parentNumbers[0]}_`));
});
