import { SourceError, manifestRows } from './collector.js';
import { readEligibilityHolds, summarizeEligibilityHolds } from './eligibility.js';

export const COLUMNS = ['id', 'item_group_id', 'title', 'description', 'link', 'image_link', 'availability', 'price', 'condition', 'brand', 'gtin', 'mpn', 'identifier_exists', 'age_group', 'gender', 'color', 'size', 'return_policy_label', 'excluded_destination'];
const SUPPLIER = /(?:alibaba\.com|aliexpress\.com|1688\.com|taobao\.com|tmall\.com)/i;
const AGE = new Set(['newborn', 'infant', 'toddler', 'kids', 'adult']);
const GENDER = new Set(['female', 'male', 'unisex']);
const CONDITION = new Set(['new', 'used', 'refurbished']);
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: '\u00a0', ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”', hellip: '…', copy: '©', reg: '®', trade: '™', euro: '€', pound: '£', yen: '¥', middot: '·', times: '×', bull: '•' };

function assert(value, code) { if (!value) throw new SourceError(code); }
export function cleanText(value) {
  return String(value ?? '').replace(/&#(x[0-9a-f]+|\d+);|&([a-z]+);/gi, (original, numeric, named) => {
    if (named) return ENTITIES[named.toLowerCase()] ?? original;
    const number = numeric[0].toLowerCase() === 'x' ? parseInt(numeric.slice(1), 16) : Number(numeric);
    return number > 0 && number <= 0x10ffff && !(number >= 0xd800 && number <= 0xdfff) ? String.fromCodePoint(number) : ' ';
  }).replace(/[\u0000-\u001f\u007f-\u009f\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]/g, ' ').replace(/\s+/g, ' ').trim();
}
export function htmlToText(value) {
  return cleanText(String(value ?? '').replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]*>/g, ' '));
}
function value(entity, key) { return cleanText(entity?.[key]?.value); }
function option(variant, name) { return cleanText(variant.selectedOptions?.find(o => o.name?.trim().toLowerCase() === name)?.value); }
function taxonomy(product, key) {
  const refs = product[key]?.references;
  if (!refs || refs.pageInfo?.hasNextPage) return [];
  return (refs.nodes || []).map(n => cleanText(n?.displayName)).filter(Boolean);
}
function enumValue(raw, allowed) {
  const text = cleanText(raw).toLowerCase();
  return allowed.has(text) ? text : '';
}
function taxonomyAge(raw) {
  const names = { adults: 'adult', adult: 'adult', kids: 'kids', children: 'kids', infants: 'infant', infant: 'infant', toddlers: 'toddler', toddler: 'toddler', newborn: 'newborn' };
  return names[raw?.toLowerCase()] || '';
}
function deriveVariantAge(variant) {
  const parts = (variant.selectedOptions || []).filter(o => /^(size|role|family member|age)$/i.test(o.name || '')).map(o => cleanText(o.value));
  if (parts.some(x => /\b(adult|mother|father|mom|dad|women|woman|men|man)\b/i.test(x))) return 'adult';
  const size = option(variant, 'size');
  const match = size.match(/\b(\d+)(?:\s*[-–]\s*(\d+))?\s*(months?|years?|yrs?)\b/i);
  if (!match) return '';
  let low = Number(match[1]), high = Number(match[2] ?? match[1]);
  if (low > high) return '';
  if (/^y/i.test(match[3])) { low *= 12; high *= 12; }
  const group = months => months < 3 ? 'newborn' : months < 12 ? 'infant' : months < 60 ? 'toddler' : months < 156 ? 'kids' : 'adult';
  return group(low) === group(high) ? group(low) : '';
}
function deriveVariantGender(variant) {
  const source = (variant.selectedOptions || []).filter(o => /^(size|role|family member|gender)$/i.test(o.name || '')).map(o => o.value).join(' ');
  const female = /\b(mother|mom|women|woman|girl|daughter|female)\b/i.test(source);
  const male = /\b(father|dad|men|man|boy|son|male)\b/i.test(source);
  if (female && !male) return 'female';
  if (male && !female) return 'male';
  return /\bunisex\b/i.test(source) && !female && !male ? 'unisex' : '';
}
function variantAgeConflict(variant, age) {
  // Google classifies ages 13+ as adult even when the option says "Child".
  const groundedAge = deriveVariantAge(variant);
  if (groundedAge === age) return false;
  const source = (variant.selectedOptions || []).filter(o => /^(size|role|family member|age)$/i.test(o.name || '')).map(o => o.value).join(' ');
  const child = /\b(child|children|girl|boy|daughter|son|baby|infant|toddler|kids?)\b|\b[0-9]+T\b/i.test(source);
  const adult = /\b(adult|mother|father|mom|dad|women|woman|men|man)\b/i.test(source);
  return (age === 'adult' && child && !adult) || (age && age !== 'adult' && adult && !child);
}

export function classifyReturnPolicy(product, rules = {}) {
  const facts = [];
  if (product.isGiftCard === true) facts.push({ field: 'isGiftCard', value: true });
  const type = cleanText(product.productType);
  if ((rules.productTypes || []).some(x => x.toLowerCase() === type.toLowerCase())) facts.push({ field: 'productType', value: type });
  const names = (product.category?.fullName || '').split(' > ').map(x => x.trim());
  for (const name of rules.taxonomyNames || []) if (names.includes(name)) facts.push({ field: 'category.fullName.segment', value: name });
  for (const tag of product.tags || []) if ((rules.finalSaleTags || []).includes(tag)) facts.push({ field: 'tags.exact', value: tag });
  return facts.length ? { classification: 'verified_policy_exception', label: cleanText(rules.exceptionLabel), facts }
    : { classification: 'no_explicit_exception_identified', label: '', facts: [] };
}

export function validGtin(input) {
  const text = String(input ?? '').trim();
  if (!/^(?:\d{8}|\d{12}|\d{13}|\d{14})$/.test(text) || /^(\d)\1+$/.test(text)) return false;
  let sum = 0;
  for (let i = text.length - 2, weight = 3; i >= 0; i--, weight = weight === 3 ? 1 : 3) sum += Number(text[i]) * weight;
  return (10 - sum % 10) % 10 === Number(text.at(-1));
}

function numericId(gid, type) {
  const match = String(gid || '').match(new RegExp(`^gid://shopify/${type}/([0-9]+)$`));
  assert(match, 'invalid_shopify_id'); return match[1];
}
export function formatPrice(money, market) {
  assert(money?.currencyCode === market.currency, 'contextual_currency_mismatch');
  const raw = String(money.amount);
  assert(/^\d+(?:\.\d+)?$/.test(raw), 'invalid_contextual_price');
  let [whole, fraction = ''] = raw.split('.');
  const places = market.minorUnits ?? 2;
  assert(Number.isInteger(places) && places >= 0 && places <= 3, 'invalid_currency_minor_units');
  assert(!/[1-9]/.test(fraction.slice(places)), 'price_requires_rounding');
  whole = whole.replace(/^0+(?=\d)/, '');
  fraction = fraction.slice(0, places).padEnd(places, '0');
  assert(/[1-9]/.test(whole + fraction), 'non_positive_price');
  return `${whole}${places ? '.' + fraction : ''} ${market.currency}`;
}
// Optional evidence-bound cost only; no ETA or return annotations are inferred.
function costOnlyShipping(config, market) {
  assert(config.shippingCostOnly === undefined, 'shipping_cost_only_must_be_market_scoped');
  const spec = market.shippingCostOnly;
  if (spec === undefined) return null;
  assert(spec && typeof spec === 'object' && Object.getPrototypeOf(spec) === Object.prototype,
    'invalid_shipping_cost_only_configuration');
  const fields = ['amount', 'country', 'currency', 'evidenceSha256', 'verified'];
  assert(JSON.stringify(Object.keys(spec).sort()) === JSON.stringify(fields),
    'invalid_shipping_cost_only_fields');
  const currencies = { CA: 'CAD', GB: 'GBP' };
  assert(Object.hasOwn(currencies, market.country) && market.currency === currencies[market.country] &&
    market.key === `${market.country.toLowerCase()}-en` && market.locale === 'en' && config.sourceLocale === 'en' &&
    spec.country === market.country && spec.currency === market.currency,
    'shipping_cost_only_scope_mismatch');
  assert(market.enabled === true, 'shipping_cost_only_market_disabled');
  assert(market.landingContextVerified === true, 'landing_context_unverified');
  assert(market.landingQuery?.country === market.country && market.landingQuery?.currency === market.currency,
    'shipping_cost_only_landing_scope_mismatch');
  assert(config.eligibilityHolds !== undefined, 'shipping_cost_only_requires_eligibility_holds');
  assert(config.returnPolicy?.emitLabels === false, 'shipping_cost_only_requires_return_labels_disabled');
  assert(spec.amount === '0.00', 'shipping_cost_only_must_be_zero');
  assert(spec.verified === true && typeof spec.evidenceSha256 === 'string' &&
    /^[a-f0-9]{64}$/.test(spec.evidenceSha256) && !/^0{64}$/.test(spec.evidenceSha256),
    'shipping_cost_only_unverified');
  return `${market.country}:::0.00 ${market.currency}`;
}
function httpsUrl(raw, code) {
  let url;
  try { url = new URL(raw); } catch { throw new SourceError(code); }
  assert(url.protocol === 'https:' && !url.username && !url.password && !SUPPLIER.test(url.hostname), code);
  return url;
}
function localizedContent(product, config, market) {
  if (market.locale === config.sourceLocale) return { title: cleanText(product.title), description: cleanText(product.description), handle: product.handle };
  const translations = new Map((product.translations || []).filter(t => t.locale === market.locale && !t.outdated).map(t => [t.key, t.value]));
  assert(translations.get('title') && translations.get('body_html'), 'missing_or_stale_translation');
  const staleHandle = (product.translations || []).some(t => t.locale === market.locale && t.key === 'handle' && t.outdated);
  assert(!staleHandle, 'stale_handle_translation');
  return { title: cleanText(translations.get('title')), description: htmlToText(translations.get('body_html')), handle: translations.get('handle') || product.handle };
}
function landingLink(product, variant, content, market) {
  assert(market.landingContextVerified === true, 'landing_context_unverified');
  const base = httpsUrl(market.landingBaseUrl, 'invalid_landing_base');
  const source = httpsUrl(product.onlineStoreUrl, 'invalid_source_product_url');
  assert(source.hostname.replace(/^www\./, '') === base.hostname.replace(/^www\./, ''), 'landing_domain_mismatch');
  assert(!base.search && !base.hash && /^[-a-z0-9]+$/i.test(content.handle || ''), 'invalid_localized_handle');
  const url = new URL(`${base.href.replace(/\/$/, '')}/products/${content.handle}`);
  for (const [key, val] of Object.entries(market.landingQuery || {})) {
    assert(['country', 'currency'].includes(key), 'unsupported_landing_query');
    url.searchParams.set(key, val);
  }
  url.searchParams.set('variant', numericId(variant.id, 'ProductVariant'));
  return url.href;
}
function cell(text) {
  const result = cleanText(text);
  return result.includes('"') ? `"${result.replace(/"/g, '""')}"` : result;
}
export async function sha256(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map(x => x.toString(16).padStart(2, '0')).join('');
}

export function validateSnapshot(snapshot, config, market, now = new Date()) {
  assert(snapshot?.schemaVersion === 1 && snapshot.paginationComplete === true, 'incomplete_snapshot');
  assert(snapshot.shop?.id === config.shopId && snapshot.onlinePublicationId === config.onlinePublicationId, 'snapshot_identity_mismatch');
  assert(snapshot.sourceLocale === config.sourceLocale, 'snapshot_source_locale_mismatch');
  if (market.expectedCatalogs) {
    assert(snapshot.marketContext?.currency === market.currency && snapshot.marketContext.activeMarketIds?.includes(market.marketId), 'snapshot_market_context_missing');
    assert(JSON.stringify(snapshot.marketContext) === JSON.stringify(snapshot.finalMarketContext), 'snapshot_market_context_changed');
    assert(JSON.stringify(snapshot.marketContext.catalogs) === JSON.stringify(market.expectedCatalogs), 'snapshot_catalog_identity_mismatch');
  }
  assert(snapshot.market?.key === market.key && snapshot.market.country === market.country && snapshot.market.locale === market.locale && snapshot.market.currency === market.currency && (snapshot.market.marketId ?? null) === (market.marketId ?? null), 'snapshot_market_mismatch');
  const completed = Date.parse(snapshot.completedAt), age = now.getTime() - completed;
  assert(Number.isFinite(completed) && age >= -60000 && age <= (config.maxSnapshotAgeHours ?? 24) * 3600000, 'stale_or_future_snapshot');
  if (snapshot.translationContext) {
    const context = snapshot.translationContext;
    assert(context.strategy === 'global_with_market_overrides' && context.clockBasis === 'page_response_observations' && context.locale === market.locale &&
      context.marketId === (market.marketId ?? null) && context.global &&
      Boolean(context.market) === Boolean(market.marketId), 'translation_context_mismatch');
    for (const component of [context.global, context.market].filter(Boolean)) {
      const start = Date.parse(component.firstObservedAt), end = Date.parse(component.lastObservedAt);
      assert(Number.isFinite(start) && Number.isFinite(end) && start <= end && end <= completed &&
        now.getTime() - start >= -60000 && now.getTime() - start <= (config.maxSnapshotAgeHours ?? 24) * 3600000 &&
        component.parents === snapshot.products?.length, 'stale_or_incomplete_translation_context');
    }
  }
  assert(snapshot.activeCount?.precision === 'EXACT' && Number.isSafeInteger(snapshot.activeCount.count) && snapshot.activeCount.count >= 0, 'non_exact_parent_count');
  assert(JSON.stringify(snapshot.activeCount) === JSON.stringify(snapshot.finalActiveCount), 'active_count_changed');
  assert(Array.isArray(snapshot.products) && snapshot.products.length === snapshot.activeCount.count, 'parent_count_mismatch');
  assert(JSON.stringify(manifestRows(snapshot.products)) === JSON.stringify(manifestRows(snapshot.finalManifest || [])), 'manifest_mismatch');
  const parents = new Set(), variants = new Set();
  for (const p of snapshot.products) {
    assert(p.status === 'ACTIVE' && !parents.has(p.id), 'invalid_parent_identity'); parents.add(p.id);
    assert(p.variantsCount?.precision === 'EXACT' && Number.isSafeInteger(p.variantsCount.count) && Array.isArray(p.variants) && p.variants.length === p.variantsCount.count, 'incomplete_variants');
    assert(typeof p.onlinePublished === 'boolean' && typeof p.countryPublished === 'boolean', 'missing_publication_state');
    if (market.expectedCatalogs) assert(typeof p.catalogPublished === 'boolean', 'missing_catalog_publication_state');
    for (const v of p.variants) { assert(!variants.has(v.id), 'duplicate_variant_id'); variants.add(v.id); }
  }
  assert(!SUPPLIER.test(JSON.stringify(snapshot.products)), 'supplier_reference_in_source');
  return { parents: parents.size, variants: variants.size };
}

export function* tsvChunks(rows, columns) {
  const encoder = new TextEncoder();
  yield encoder.encode(columns.join('\t') + '\n');
  for (const row of rows) yield encoder.encode(columns.map(column => cell(row[column])).join('\t') + '\n');
}

export async function buildFeed(snapshot, config, market, { now = new Date(), previousIds = [], materialize = true } = {}) {
  const sourceCounts = validateSnapshot(snapshot, config, market, now);
  assert(/^[a-z]{2}-[a-z]{2}(?:-[a-z]{2})?$/.test(market.key) && /^[A-Z]{2}$/.test(market.country) && /^[A-Z]{3}$/.test(market.currency), 'invalid_market_configuration');
  const eligibilityHolds = readEligibilityHolds(config.eligibilityHolds);
  const shipping = costOnlyShipping(config, market);
  if (config.eligibilityHolds !== undefined) {
    assert(market.landingContextVerified === true, 'landing_context_unverified');
    httpsUrl(market.landingBaseUrl, 'invalid_landing_base');
  }
  const translationFailureMode = market.translationFailureMode ?? 'reject_feed';
  assert(['reject_feed', 'exclude_product'].includes(translationFailureMode), 'invalid_translation_failure_mode');
  if (translationFailureMode === 'exclude_product') {
    assert(market.locale !== config.sourceLocale, 'translation_exclusion_requires_foreign_locale');
    assert(market.landingContextVerified === true, 'landing_context_unverified');
  }
  const rows = [], errors = [], warnings = [], exclusions = [], returnCohorts = [];
  let exceptionRows = 0;
  for (const product of snapshot.products) {
    if (!product.onlinePublished || !product.countryPublished || (market.expectedCatalogs && !product.catalogPublished)) {
      exclusions.push({ productId: product.id, variants: product.variants.length, code: !product.onlinePublished ? 'not_on_online_store' : !product.countryPublished ? 'not_published_in_country' : 'not_in_market_catalog' }); continue;
    }
    const eligibilityHold = eligibilityHolds.parents.get(product.id);
    if (eligibilityHold) {
      // Holds can concern customer-facing content, images or unusable options.
      // Retain complete-source, identity, availability and native-money checks
      // without requiring those known-held attributes to qualify for a feed.
      for (const variant of product.variants) {
        const id = `shopify_${market.country}_${numericId(product.id, 'Product')}_${numericId(variant.id, 'ProductVariant')}`;
        try {
          assert(id.length <= 50, 'offer_id_too_long');
          assert(typeof variant.availableForSale === 'boolean', 'missing_variant_availability');
          if (!variant.availableForSale) {
            exclusions.push({ productId: product.id, variantId: variant.id, id, variants: 1, code: 'variant_not_available_for_sale' });
            continue;
          }
          formatPrice(variant.contextualPricing?.price, market);
          exclusions.push({ productId: product.id, variantId: variant.id, id, variants: 1,
            code: 'reviewed_parent_eligibility_hold', reason: eligibilityHold.reason });
        } catch (e) { errors.push({ productId: product.id, variantId: variant.id, id, code: e.code || 'invalid_variant' }); }
      }
      continue;
    }
    const returns = classifyReturnPolicy(product, config.returnPolicy);
    returnCohorts.push({ productId: product.id, variants: product.variants.length, ...returns });
    let content, translationRejectedCode;
    try {
      content = localizedContent(product, config, market);
      // All variants share these parent strings; do not make thousands of copies.
      content.title = [...content.title].slice(0, 150).join('');
      content.description = [...content.description].slice(0, 5000).join('');
    } catch (e) {
      if (translationFailureMode === 'exclude_product' &&
          ['missing_or_stale_translation', 'stale_handle_translation'].includes(e.code)) {
        translationRejectedCode = e.code;
      } else { errors.push({ productId: product.id, code: e.code || 'invalid_product_content' }); continue; }
    }
    for (const variant of product.variants) {
      const id = `shopify_${market.country}_${numericId(product.id, 'Product')}_${numericId(variant.id, 'ProductVariant')}`;
      try {
        assert(id.length <= 50, 'offer_id_too_long');
        if (!translationRejectedCode) assert(content.title && content.description, 'missing_title_or_description');
        assert(typeof variant.availableForSale === 'boolean', 'missing_variant_availability');
        if (!variant.availableForSale) {
          exclusions.push({ productId: product.id, variantId: variant.id, id, variants: 1, code: 'variant_not_available_for_sale' });
          continue;
        }
        const image = variant.media?.nodes?.find(n => n.image?.url)?.image.url || product.featuredMedia?.image?.url;
        const imageUrl = httpsUrl(image, 'missing_or_invalid_image').href;
        const explicitAge = enumValue(value(variant, 'gAgeGroup'), AGE), derivedAge = deriveVariantAge(variant);
        const parentAge = enumValue(value(product, 'gAgeGroup'), AGE);
        const ages = taxonomy(product, 'taxonomyAgeGroup').map(taxonomyAge).filter(Boolean);
        let age = explicitAge || derivedAge || parentAge || (ages.length === 1 ? ages[0] : '');
        if (variantAgeConflict(variant, age)) { warnings.push({ id, code: 'age_group_role_conflict_omitted' }); age = ''; }
        const genders = taxonomy(product, 'taxonomyGender').map(x => enumValue(x, GENDER)).filter(Boolean);
        const gender = enumValue(value(variant, 'gGender'), GENDER) || deriveVariantGender(variant) || enumValue(value(product, 'gGender'), GENDER) || (genders.length === 1 ? genders[0] : '');
        const colors = taxonomy(product, 'taxonomyColor');
        const color = value(variant, 'gColor') || option(variant, 'color') || value(product, 'gColor') || (colors.length === 1 ? colors[0] : '');
        const size = value(variant, 'gSize') || option(variant, 'size') || value(product, 'gSize');
        const barcode = String(variant.barcode || '').trim();
        const gtin = validGtin(barcode) ? barcode : '';
        if (barcode && !gtin) warnings.push({ id, code: 'invalid_gtin_omitted' });
        const brand = value(variant, 'gBrand') || value(product, 'gBrand');
        const mpn = value(variant, 'gMpn') || value(product, 'gMpn');
        const declaredIdentifier = (value(variant, 'gIdentifierExists') || value(product, 'gIdentifierExists')).toLowerCase();
        let identifier = ['true', 'yes'].includes(declaredIdentifier) ? 'yes' : ['false', 'no'].includes(declaredIdentifier) ? 'no' : '';
        if (identifier === 'no' && (gtin || mpn || brand)) { warnings.push({ id, code: 'identifier_declaration_conflict' }); identifier = ''; }
        if (!gtin && !mpn && !brand && !identifier) warnings.push({ id, code: 'identifier_status_unknown' });
        for (const [field, val] of Object.entries({ age_group: age, gender, color, size })) if (!val) warnings.push({ id, code: `missing_${field}` });
        if (returns.classification === 'verified_policy_exception') {
          assert(returns.label && returns.label.length <= 100 && /^[a-zA-Z0-9_-]+$/.test(returns.label), 'missing_or_invalid_return_exception_label');
          exceptionRows++;
        }
        const row = {
          id, item_group_id: `shopify_${market.country}_${numericId(product.id, 'Product')}`,
          title: content?.title || '', description: content?.description || '',
          link: landingLink(product, variant, content || { handle: product.handle }, market), image_link: imageUrl,
          availability: variant.availableForSale ? 'in_stock' : 'out_of_stock',
          price: formatPrice(variant.contextualPricing?.price, market),
          condition: enumValue(value(variant, 'gCondition') || value(product, 'gCondition'), CONDITION),
          brand, gtin, mpn, identifier_exists: identifier, age_group: age, gender, color, size,
          return_policy_label: config.returnPolicy?.emitLabels === false ? '' : returns.label, excluded_destination: 'Shopping_ads',
        };
        if (shipping !== null) row.shipping = shipping;
        assert(!SUPPLIER.test(JSON.stringify(row)), 'supplier_reference_in_output');
        if (translationRejectedCode) {
          // Validate source price, identity, image and landing safety first. A
          // translation exclusion must never conceal a malformed buyable row.
          exclusions.push({ productId: product.id, variantId: variant.id, id, variants: 1,
            code: translationRejectedCode, reason: 'translation_unusable' });
          continue;
        }
        rows.push(row);
      } catch (e) { errors.push({ productId: product.id, variantId: variant.id, id, code: e.code || 'invalid_variant' }); }
    }
  }
  const rowIds = rows.map(r => r.id), previous = new Set(previousIds), current = new Set(rowIds);
  assert(current.size === rows.length, 'duplicate_offer_id');
  const diagnostics = {
    generatedAt: now.toISOString(), sourceCompletedAt: snapshot.completedAt, market: market.key,
    sourceCounts, rows: rows.length, outOfStock: rows.filter(r => r.availability === 'out_of_stock').length,
    errors, warnings, exclusions, returnCohorts, exceptionRows,
    eligibilityHolds: summarizeEligibilityHolds(eligibilityHolds, snapshot.products, exclusions),
    translationFailureMode,
    returnPolicyLabelsEmitted: config.returnPolicy?.emitLabels !== false,
    returnPolicyLabelsConfirmed: config.returnPolicy?.emitLabels === false || exceptionRows === 0 || config.returnPolicy?.nativeLabelConfirmed === true,
    lifecycle: { added: rowIds.filter(id => !previous.has(id)), removed: previousIds.filter(id => !current.has(id)), retained: rowIds.filter(id => previous.has(id)), previousIdsProvided: previousIds.length > 0 },
    limits: ['Shopify buyability is not owned physical inventory.', 'Google source must separately target Free listings only.', 'Removal requires the next successful primary-file fetch and processing; serving can take 24–48 hours.', 'No explicit exception identified is not a certification of individual return eligibility.'],
  };
  if (shipping !== null) diagnostics.shippingCostOnly = {
    country: market.country, currency: market.currency, amount: '0.00',
    evidenceSha256: market.shippingCostOnly.evidenceSha256,
    deliveryTimesSubmitted: false, returnAnnotationsSubmitted: false,
    displayLimit: 'Google may still use crawled or modeled delivery times or default return information.',
  };
  // A malformed variant never turns a complete source scan into a partial live feed.
  if (errors.length) return { ok: false, diagnostics, tsv: null, rows: [], rowIds: [] };
  const baseColumns = config.returnPolicy?.emitLabels === false ? COLUMNS.filter(c => c !== 'return_policy_label') : COLUMNS;
  const columns = shipping === null ? baseColumns : [...baseColumns, 'shipping'];
  if (!materialize) {
    let bytes = 0; for (const chunk of tsvChunks(rows, columns)) bytes += chunk.byteLength;
    return { ok: true, tsv: null, rows, rowIds, columns, bytes, diagnostics };
  }
  const tsv = [columns.join('\t'), ...rows.map(r => columns.map(c => cell(r[c])).join('\t'))].join('\n') + '\n';
  return { ok: true, tsv, rows, rowIds, sha256: await sha256(tsv), bytes: new TextEncoder().encode(tsv).byteLength, diagnostics };
}
