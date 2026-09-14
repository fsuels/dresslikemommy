import test from 'node:test';
import assert from 'node:assert/strict';
import { collectCatalog, createAdminReader, SourceError, manifestRows, readMarketContext } from '../src/collector.js';
import { buildFeed, classifyReturnPolicy, validGtin, formatPrice, cleanText, COLUMNS } from '../src/generator.js';
import worker, { refreshMarket, publishResult, currentManifest } from '../src/worker.js';
import host from '../src/host.js';
import { config, market, now, count, variant, product, snapshot, source, Bucket } from './fixtures.js';

const build = (s = snapshot(), cfg = config, target = market, opts = {}) => buildFeed(s, cfg, target, { now, ...opts });
const env = bucket => ({ MERCHANT_CONFIG_JSON: JSON.stringify(config), MERCHANT_FEED_BUCKET: bucket });

test('collects every parent and every nested variant page with final reconciliation', async () => {
  const products = [product(1, Array.from({ length: 83 }, (_, i) => variant(1000 + i))), product(2), product(3)];
  const api = source(products, { productPageSize: 1, manifestPageSize: 2 });
  const result = await collectCatalog(api.graphql, config, market, { now: () => now });
  assert.equal(result.products.length, 3); assert.equal(result.products[0].variants.length, 83);
  assert.equal(result.paginationComplete, true); assert.equal(api.calls(), 12);
  assert.equal((await build(result)).rows.length, 85);
});
test('240-parent read exposes its actual scheduled request requirement', async () => {
  const api = source(Array.from({ length: 240 }, (_, i) => product(i + 1)));
  await collectCatalog(api.graphql, config, market, { now: () => now });
  assert.equal(api.calls(), 257); assert.ok(api.calls() > 50);
});
test('country resolver binds exact active market/catalog/currency and catalog exclusion', async () => {
  const target = { ...market, marketId: 'gid://shopify/Market/544735329', expectedCatalogs: [{ id: 'gid://shopify/MarketCatalog/6881083489', publicationId: 'gid://shopify/Publication/77106053217' }] };
  const resolved = { marketsResolvedValues: { currencyCode: 'USD', catalogs: { nodes: [{ id: target.expectedCatalogs[0].id, status: 'ACTIVE', publication: { id: target.expectedCatalogs[0].publicationId }, markets: { nodes: [{ id: target.marketId, name: 'United States', status: 'ACTIVE' }], pageInfo: { hasNextPage: false } } }], pageInfo: { hasNextPage: false } } } };
  const p = product(); p.catalogPublished = false;
  const base = source([p]);
  const read = async (query, variables) => query.includes('query MerchantFeedMarketContext') ? structuredClone(resolved) : base.graphql(query, variables);
  const s = await collectCatalog(read, config, target, { now: () => now });
  assert.equal(s.marketContext.catalogs[0].publicationId, target.expectedCatalogs[0].publicationId);
  const result = await build(s, config, target); assert.equal(result.rows.length, 0); assert.equal(result.diagnostics.exclusions[0].code, 'not_in_market_catalog');
  resolved.marketsResolvedValues.currencyCode = 'EUR';
  await assert.rejects(readMarketContext(read, target, []), /resolved_market_currency_mismatch/);
  resolved.marketsResolvedValues.currencyCode = 'USD'; resolved.marketsResolvedValues.catalogs.nodes[0].publication.id = 'wrong';
  await assert.rejects(readMarketContext(read, target, []), /resolved_catalog_identity_changed/);
});
test('incomplete variants never become a snapshot', async () => {
  const p = product(); p.variantsCount = count(2);
  await assert.rejects(collectCatalog(source([p]).graphql, config, market), /variant_count_mismatch/);
});
test('duplicate and repeated pagination identifiers fail closed', async () => {
  const duplicate = source([product(1), product(1)]);
  await assert.rejects(collectCatalog(duplicate.graphql, config, market), /products_duplicate_id/);
  const api = source([product()], { intercept: (r, q) => {
    if (q.includes('query MerchantFeedProducts')) r.products.pageInfo = { hasNextPage: true, endCursor: null };
  } });
  await assert.rejects(collectCatalog(api.graphql, config, market), /products_invalid_cursor/);
});
test('changed parent or manifest prevents collection promotion', async () => {
  for (const phase of ['Variants', 'Manifest']) {
    const api = source([product()], { intercept: (r, q) => {
      if (q.includes(`query MerchantFeed${phase}`)) (r.product || r.products.nodes[0]).updatedAt = '2026-09-11T13:01:00Z';
    } });
    await assert.rejects(collectCatalog(api.graphql, config, market), /changed_during_read/);
  }
});
test('URL-bearing source tags are omitted without losing exact Final Sale fact', async () => {
  const p = product(); p.tags = ['Final Sale', 'https://example.invalid/source'];
  const result = await collectCatalog(source([p]).graphql, config, market, { now: () => now });
  assert.deepEqual(result.products[0].tags, ['Final Sale']); assert.equal(result.sanitization.omittedUrlTags, 1);
});
test('wrong identity, incomplete/future/stale snapshot and manifest mismatch reject', async () => {
  for (const mutate of [s => { s.shop.id = 'wrong'; }, s => { s.paginationComplete = false; },
    s => { s.completedAt = '2020-01-01'; }, s => { s.completedAt = '2030-01-01'; },
    s => { s.finalManifest[0].updatedAt = 'different'; }]) {
    const s = snapshot(); mutate(s); await assert.rejects(build(s), SourceError);
  }
});
test('complete replacement removes deleted/unpublished/unavailable rows and readds when buyable', async () => {
  const before = await build(snapshot([product(1, [variant(101), variant(102)]), product(2)]));
  const p = product(1, [variant(102), variant(103)]); p.variants[0].availableForSale = false;
  const hidden = product(3); hidden.onlinePublished = false;
  const country = product(4); country.countryPublished = false;
  const after = await build(snapshot([p, hidden, country]), config, market, { previousIds: before.rowIds });
  assert.equal(after.rows.length, 1); assert.equal(after.rows[0].availability, 'in_stock');
  assert.deepEqual(after.diagnostics.lifecycle.removed.sort(), ['shopify_US_1_101', 'shopify_US_1_102', 'shopify_US_2_201']);
  assert.deepEqual(after.diagnostics.lifecycle.added, ['shopify_US_1_103']); assert.equal(after.diagnostics.exclusions.length, 3);
  p.variants[0].availableForSale = true;
  const returned = await build(snapshot([p]), config, market, { previousIds: after.rowIds });
  assert.deepEqual(returned.diagnostics.lifecycle.added, ['shopify_US_1_102']);
});
test('a malformed buyable row invalidates whole replacement, never partial deletes', async () => {
  const p = product(1, [variant(101), variant(102)]); p.variants[1].contextualPricing.price.currencyCode = 'CAD';
  const result = await build(snapshot([p]));
  assert.equal(result.ok, false); assert.equal(result.tsv, null); assert.equal(result.diagnostics.errors[0].code, 'contextual_currency_mismatch');
});
test('USD/AUD/CAD/GBP retain exact contextual money, never convert or round', async () => {
  for (const [country, currency] of [['US', 'USD'], ['AU', 'AUD'], ['CA', 'CAD'], ['GB', 'GBP']]) {
    const target = { ...market, key: `${country.toLowerCase()}-en`, country, currency };
    const result = await build(snapshot([product(1, [variant(101, currency)])], target), config, target);
    assert.equal(result.rows[0].price, `21.90 ${currency}`); assert.ok(result.rows[0].id.startsWith(`shopify_${country}_`));
  }
  assert.equal(formatPrice({ amount: '9007199254740993.01', currencyCode: 'USD' }, market), '9007199254740993.01 USD');
  assert.equal(formatPrice({ amount: '1234.0', currencyCode: 'JPY' }, { currency: 'JPY', minorUnits: 0 }), '1234 JPY');
  for (const amount of ['0', '-1', '1e2', '1.001']) assert.throws(() => formatPrice({ amount, currencyCode: 'USD' }, market));
});
test('foreign content requires fresh translations and a verified localized landing context', async () => {
  const target = { ...market, key: 'ca-fr', country: 'CA', currency: 'CAD', locale: 'fr', landingBaseUrl: `${market.landingBaseUrl}/fr`, landingQuery: { country: 'CA', currency: 'CAD' } };
  const p = product(1, [variant(101, 'CAD')]);
  let s = snapshot([p], target), result = await build(s, config, target);
  assert.equal(result.ok, false); assert.equal(result.diagnostics.errors[0].code, 'missing_or_stale_translation');
  p.translations = [{ locale: 'fr', key: 'title', value: 'Tenue bleue', outdated: false }, { locale: 'fr', key: 'body_html', value: '<p>Bleu &amp; blanc</p>', outdated: false }];
  result = await build(snapshot([p], target), config, target);
  assert.equal(result.rows[0].description, 'Bleu & blanc');
  assert.equal(result.rows[0].link, 'https://www.dresslikemommy.com/fr/products/matching-outfit-1?country=CA&currency=CAD&variant=101');
  result = await build(snapshot([p], target), config, { ...target, landingContextVerified: false });
  assert.equal(result.ok, false); assert.equal(result.diagnostics.errors[0].code, 'landing_context_unverified');
  p.translations[0].outdated = true; assert.equal((await build(snapshot([p], target), config, target)).ok, false);
});
test('collector inherits global translations while retaining market overrides and their stale flags', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr', marketId: 'gid://shopify/Market/544735329',
    landingBaseUrl: `${market.landingBaseUrl}/fr`, translationFailureMode: 'exclude_product' };
  const globalRows = [
    { locale: 'fr', key: 'title', value: 'Tenue globale', outdated: false },
    { locale: 'fr', key: 'body_html', value: '<p>Description globale</p>', outdated: false },
  ];
  const overrides = new Map();
  const seenMarkets = [];
  const api = source([product(1), product(2)], { productPageSize: 1, intercept: (r, q, variables) => {
    if (q.includes('query MerchantFeedProducts')) {
      seenMarkets.push(variables.marketId);
      for (const p of r.products.nodes) p.translations = structuredClone(variables.marketId === null ? globalRows : overrides.get(p.id) || []);
    }
  } });
  let collected = await collectCatalog(api.graphql, config, target, { now: () => now });
  assert.deepEqual(seenMarkets, [target.marketId, target.marketId, null, null]);
  assert.equal(collected.market.marketId, target.marketId);
  assert.deepEqual(collected.products[0].translationSources, { title: 'global', body_html: 'global' });
  assert.equal(collected.translationContext.global.parents, 2);
  assert.equal(collected.translationContext.market.lastObservedAt, now.toISOString());
  assert.equal((await build(collected, config, target)).rows.length, 2);
  overrides.set('gid://shopify/Product/1', [
    { locale: 'fr', key: 'title', value: 'Ancien titre du marché', outdated: true },
    { locale: 'fr', key: 'body_html', value: '<p>Description du marché</p>', outdated: false },
  ]);
  collected = await collectCatalog(api.graphql, config, target, { now: () => now });
  assert.equal(collected.products[0].translations.find(t => t.key === 'title').outdated, true);
  assert.equal(collected.products[0].translations.find(t => t.key === 'body_html').value, '<p>Description du marché</p>');
  assert.equal(collected.products[0].translationSources.title, 'market');
  let result = await build(collected, config, target);
  assert.equal(result.ok, true); assert.deepEqual(result.rowIds, ['shopify_US_2_201']);
  assert.equal(result.diagnostics.exclusions[0].code, 'missing_or_stale_translation');
  overrides.get('gid://shopify/Product/1')[0].outdated = false;
  collected = await collectCatalog(api.graphql, config, target, { now: () => now });
  result = await build(collected, config, target);
  assert.equal(result.rows[0].title, 'Ancien titre du marché');
  assert.equal(result.rows[0].description, 'Description du marché');
});
test('global translation views reject source drift, missing records, duplicate keys and incomplete pagination', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr', marketId: 'gid://shopify/Market/544735329' };
  for (const fault of ['drift', 'missing_array', 'duplicate_key', 'wrong_locale', 'incomplete']) {
    const api = source([product()], { intercept: (r, q, variables) => {
      if (!q.includes('query MerchantFeedProducts') || variables.marketId !== null) return;
      const p = r.products.nodes[0];
      p.translations = [{ locale: 'fr', key: 'title', value: 'Tenue', outdated: false }];
      if (fault === 'drift') p.updatedAt = '2026-09-11T13:59:00Z';
      if (fault === 'missing_array') delete p.translations;
      if (fault === 'duplicate_key') p.translations.push({ ...p.translations[0] });
      if (fault === 'wrong_locale') p.translations[0].locale = 'en';
      if (fault === 'incomplete') r.products.pageInfo = { hasNextPage: true, endCursor: null };
    } });
    await assert.rejects(collectCatalog(api.graphql, config, target, { now: () => now }), SourceError, fault);
  }
});
test('explicit translation exclusions reconcile replacement lifecycle without hiding unavailable rows', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr', landingBaseUrl: `${market.landingBaseUrl}/fr`, translationFailureMode: 'exclude_product' };
  const translated = id => {
    const p = product(id);
    p.translations = [{ locale: 'fr', key: 'title', value: 'Tenue', outdated: false }, { locale: 'fr', key: 'body_html', value: '<p>Bleue</p>', outdated: false }];
    return p;
  };
  const before = await build(snapshot([translated(1), translated(2)], target), config, target);
  const stale = translated(1); stale.translations[0].outdated = true;
  const unavailable = translated(4); unavailable.variants[0].availableForSale = false; unavailable.translations = [];
  const after = await build(snapshot([stale, translated(3), unavailable], target), config, target, { previousIds: before.rowIds });
  assert.equal(after.ok, true); assert.deepEqual(after.rowIds, ['shopify_US_3_301']);
  assert.deepEqual(after.diagnostics.lifecycle.removed.sort(), ['shopify_US_1_101', 'shopify_US_2_201']);
  assert.deepEqual(after.diagnostics.lifecycle.added, ['shopify_US_3_301']);
  assert.equal(after.diagnostics.exclusions.find(e => e.variantId.endsWith('/101')).reason, 'translation_unusable');
  assert.equal(after.diagnostics.exclusions.find(e => e.variantId.endsWith('/401')).code, 'variant_not_available_for_sale');
  stale.translations[0].outdated = false;
  const restored = await build(snapshot([stale, translated(3)], target), config, target, { previousIds: after.rowIds });
  assert.deepEqual(restored.diagnostics.lifecycle.added, ['shopify_US_1_101']);
  const strict = await build(snapshot([product(1), translated(3)], target), config, { ...target, translationFailureMode: 'reject_feed' });
  assert.equal(strict.ok, false); assert.equal(strict.tsv, null);
});
test('translation exclusion never bypasses source integrity or the landing gate', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr', landingBaseUrl: `${market.landingBaseUrl}/fr`, translationFailureMode: 'exclude_product' };
  for (const mutate of [p => { p.variants[0].contextualPricing.price.currencyCode = 'CAD'; },
    p => { p.variants[0].availableForSale = undefined; }, p => { p.variants[0].media.nodes[0].image.url = 'http://invalid.example/image'; },
    p => { p.onlineStoreUrl = 'https://wrong.example/products/item'; }]) {
    const p = product(); mutate(p);
    const result = await build(snapshot([p], target), config, target);
    assert.equal(result.ok, false); assert.equal(result.tsv, null); assert.deepEqual(result.rows, []);
    assert.ok(result.diagnostics.errors.length);
  }
  await assert.rejects(build(snapshot([], target), config, { ...target, landingContextVerified: false }), /landing_context_unverified/);
  await assert.rejects(build(snapshot(), config, { ...market, translationFailureMode: 'exclude_product' }), /translation_exclusion_requires_foreign_locale/);
});
test('translation component clocks and parent counts are independently validated', async () => {
  const target = { ...market, key: 'us-fr', locale: 'fr' };
  const api = source([product()], { intercept: (r, q) => {
    if (q.includes('query MerchantFeedProducts')) r.products.nodes[0].translations = [
      { locale: 'fr', key: 'title', value: 'Tenue', outdated: false },
      { locale: 'fr', key: 'body_html', value: '<p>Bleue</p>', outdated: false },
    ];
  } });
  const collected = await collectCatalog(api.graphql, config, target, { now: () => now });
  assert.equal(collected.translationContext.market, null);
  assert.equal((await build(collected, config, target)).ok, true);
  for (const mutate of [s => { s.translationContext.global.firstObservedAt = '2026-09-09T14:00:00Z'; },
    s => { s.translationContext.global.lastObservedAt = '2026-09-11T15:00:00Z'; },
    s => { s.translationContext.global.parents = 2; }, s => { s.translationContext.locale = 'es'; }]) {
    const bad = structuredClone(collected); mutate(bad);
    await assert.rejects(build(bad, config, target), SourceError);
  }
});
test('variant identity/image/availability survive and optional identifiers are not invented', async () => {
  const result = await build(); const row = result.rows[0];
  assert.equal(row.link, 'https://www.dresslikemommy.com/products/matching-outfit-1?variant=101');
  assert.equal(row.image_link, 'https://cdn.shopify.com/fixture.png');
  assert.equal(row.item_group_id, 'shopify_US_1');
  for (const name of ['brand', 'mpn', 'identifier_exists', 'condition', 'gtin']) assert.equal(row[name], '');
  assert.equal(row.gender, 'female'); assert.equal(row.age_group, 'adult');
});
test('GTIN checksum validation preserves leading zeros and reports invalid source barcode', async () => {
  assert.equal(validGtin('00012345600012'), true); assert.equal(validGtin('00000000000000'), false);
  assert.equal(validGtin('123'), false); const p = product(); p.variants[0].barcode = '00012345600012';
  assert.equal((await build(snapshot([p]))).rows[0].gtin, '00012345600012');
  p.variants[0].barcode = '00012345600013'; const result = await build(snapshot([p]));
  assert.equal(result.rows[0].gtin, ''); assert.ok(result.diagnostics.warnings.some(w => w.code === 'invalid_gtin_omitted'));
});
test('explicit identifier_exists conflict is disclosed and not propagated', async () => {
  const p = product(); p.gIdentifierExists = { value: 'false' }; p.gBrand = { value: 'Verified Manufacturer' };
  const result = await build(snapshot([p])); assert.equal(result.rows[0].identifier_exists, '');
  assert.ok(result.diagnostics.warnings.some(w => w.code === 'identifier_declaration_conflict'));
});
test('child role never inherits adult age from parent or variant contradictory data', async () => {
  const p = product(); p.gAgeGroup = { value: 'adult' }; p.variants[0].selectedOptions[0].value = 'Girl 3T';
  let result = await build(snapshot([p])); assert.equal(result.rows[0].age_group, '');
  assert.ok(result.diagnostics.warnings.some(w => w.code === 'age_group_role_conflict_omitted'));
  p.variants[0].gAgeGroup = { value: 'toddler' }; result = await build(snapshot([p]));
  assert.equal(result.rows[0].age_group, 'toddler');
  p.variants[0].gAgeGroup = { value: 'adult' }; p.variants[0].selectedOptions[0].value = 'Child 13-14 Years';
  result = await build(snapshot([p])); assert.equal(result.rows[0].age_group, 'adult');
});
test('policy exceptions require exact source type/taxonomy/tag/gift-card facts', () => {
  for (const mutate of [p => { p.productType = 'Swimwear'; }, p => { p.category.fullName = 'Clothing > Swimwear > Bikinis'; }, p => { p.tags = ['Final Sale']; }, p => { p.isGiftCard = true; }]) {
    const p = product(); mutate(p); assert.equal(classifyReturnPolicy(p, config.returnPolicy).label, 'no_returns');
  }
  const p = product(); p.title = 'Sale personalized swim-inspired dress'; p.productType = 'Socks'; p.category.fullName = 'Apparel > Underwear & Socks > Socks';
  assert.equal(classifyReturnPolicy(p, config.returnPolicy).label, '');
  assert.equal(classifyReturnPolicy(p, config.returnPolicy).classification, 'no_explicit_exception_identified');
});
test('TSV has exact columns, free-listing exclusion, escaped controls and no paid allowlist claim', async () => {
  const p = product(); p.title = 'Blue\t"outfit"\n&copy;';
  const result = await build(snapshot([p]));
  assert.equal(result.tsv.split('\n')[0], COLUMNS.join('\t')); assert.equal(result.tsv.split('\n').length, 3);
  assert.ok(result.tsv.includes('"Blue ""outfit"" ©"')); assert.equal(result.rows[0].excluded_destination, 'Shopping_ads');
  assert.ok(!COLUMNS.includes('included_destination')); assert.equal(cleanText('a&#x00A0;b\u0000c'), 'a b c');
});
test('publish only switches pointer after complete object, and CAS retains newer file', async () => {
  const bucket = new Bucket(), s = snapshot(), result = await build(s);
  const manifest = await publishResult(bucket, result, s, market, { manifest: null, etag: null });
  assert.deepEqual(bucket.writes.slice(0, 2), [manifest.objectKey, 'merchant/us-en/current.json']);
  const stale = { manifest, etag: 'old-etag' };
  await assert.rejects(publishResult(bucket, result, s, market, stale), /concurrent_refresh/);
  assert.equal((await currentManifest(bucket, market.key)).manifest.sha256, result.sha256);
});
test('native exception label must be confirmed before any R2 publication', async () => {
  const p = product(); p.productType = 'Swimwear'; const s = snapshot([p]);
  const cfg = { ...config, returnPolicy: { ...config.returnPolicy, nativeLabelConfirmed: false } };
  const result = await build(s, cfg); assert.equal(result.ok, true);
  const bucket = new Bucket(); await assert.rejects(publishResult(bucket, result, s, market, { manifest: null, etag: null }), /native_return_label_not_confirmed/);
  assert.equal(bucket.writes.length, 0);
});
test('first-file option omits return labels without losing exception diagnostics', async () => {
  const p = product(); p.productType = 'Swimwear';
  const cfg = { ...config, returnPolicy: { ...config.returnPolicy, emitLabels: false, nativeLabelConfirmed: false } };
  const result = await build(snapshot([p]), cfg); assert.equal(result.rows[0].return_policy_label, '');
  assert.ok(!result.tsv.split('\n')[0].includes('return_policy_label'));
  assert.equal(result.diagnostics.exceptionRows, 1); assert.equal(result.diagnostics.returnPolicyLabelsConfirmed, true);
});
test('upstream errors and invalid currency leave previous complete pointer untouched', async () => {
  const bucket = new Bucket(); await refreshMarket(env(bucket), market.key, { graphql: source([product()]).graphql, now: () => now });
  const before = (await bucket.get('merchant/us-en/current.json')).etag;
  await assert.rejects(refreshMarket(env(bucket), market.key, { graphql: async () => { throw new SourceError('upstream_failed'); }, now: () => now }), /upstream_failed/);
  const p = product(); p.variants[0].contextualPricing.price.currencyCode = 'JPY';
  await assert.rejects(refreshMarket(env(bucket), market.key, { graphql: source([p]).graphql, now: () => now }), /feed_validation_failed/);
  assert.equal((await bucket.get('merchant/us-en/current.json')).etag, before);
});
test('public endpoint serves exact complete bytes and rejects stale/tampered/disabled/method cases', async () => {
  const bucket = new Bucket(), current = new Date(), s = snapshot(); s.completedAt = current.toISOString();
  const result = await buildFeed(s, config, market, { now: current });
  const manifest = await publishResult(bucket, result, s, market, { manifest: null, etag: null });
  const request = (path, method = 'GET') => host.fetch(new Request(`https://feed.example${path}`, { method }), env(bucket));
  let response = await request('/feeds/us-en.tsv'); assert.equal(response.status, 200); assert.equal(await response.text(), result.tsv);
  assert.equal(response.headers.get('x-dlm-feed-sha256'), result.sha256);
  response = await request('/feeds/us-en.tsv', 'HEAD'); assert.equal(response.status, 200); assert.equal(await response.text(), '');
  assert.equal((await request('/feeds/us-en.tsv', 'POST')).status, 405); assert.equal((await request('/feeds/au-en.tsv')).status, 404);
  assert.equal((await request('/secret')).status, 404);
  bucket.objects.get(manifest.objectKey).text = result.tsv.replace('21.90', '21.91');
  const originalEtag = bucket.objects.get(manifest.objectKey).etag;
  bucket.objects.get(manifest.objectKey).etag = 'changed-object-etag';
  assert.equal((await request('/feeds/us-en.tsv')).status, 503);
  bucket.objects.get(manifest.objectKey).text = result.tsv;
  bucket.objects.get(manifest.objectKey).etag = originalEtag;
  const pointer = bucket.objects.get('merchant/us-en/current.json'); const changed = JSON.parse(pointer.text); changed.sourceCompletedAt = '2020-01-01'; pointer.text = JSON.stringify(changed);
  assert.equal((await request('/feeds/us-en.tsv')).status, 503);
});
test('first release exports only read-only serving and no scheduler', () => {
  assert.deepEqual(Object.keys(host), ['fetch']);
});
test('authenticated reader requests only configured Shopify endpoint and redacts upstream failures', async () => {
  let captured;
  const reader = createAdminReader({ domain: config.storeDomain, token: 'fixture-private', sleep: async () => {}, fetchImpl: async (url, options) => {
    captured = { url, options }; return new Response(JSON.stringify({ errors: [{ message: 'secret-source-text', extensions: { code: 'ACCESS_DENIED' } }] }), { status: 200 });
  } });
  await assert.rejects(reader('query Fixture { shop { id } }', {}), { message: 'shopify_access_denied' });
  assert.equal(captured.url, 'https://dresslikemommy-com.myshopify.com/admin/api/2026-07/graphql.json');
  assert.equal(captured.options.redirect, 'error'); assert.equal(captured.options.headers['X-Shopify-Access-Token'], 'fixture-private');
});
