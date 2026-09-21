import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

// Read-only computation. No generator/config patch, collection, build or publication.
globalThis.fetch = () => { throw new Error('network_prohibited'); };
const self = fileURLToPath(import.meta.url);
const packet = path.dirname(self);
const audit = path.resolve(packet, '../..');
const release = path.join(audit, 'recovery_20260911/direct-feed-deployment/automation_release_v1');
const local = path.join(release, '../local_lifecycle_interim');
const configPath = path.resolve(packet, '../us_spanish_qualification/isolated_config.json');
const rawPath = '/Users/fsuels/.config/dresslikemommy/merchant-evidence/20260915-us-es-full/source.json';
const sourceSha = '5b868f1470ec06834a9b74b2960021a24fcc6da1c1c6b17b8f6b2d094a39ad88';
const previousUs = path.join(local, 'runs/20260915T015530Z-us-color47-refresh/candidate/us-en.tsv');
const tropical = 'gid://shopify/Product/7227378925665';
const SUPPLIER = /(?:alibaba\.com|aliexpress\.com|1688\.com|taobao\.com|tmall\.com)/i;
const protectedIds = [
  'shopify_US_6718945034337_39756755861601',
  'shopify_US_7230336729185_41883237220449',
  'shopify_US_7230336729185_41883237285985',
  'shopify_US_7230336729185_41883237318753',
  'shopify_US_7230336729185_41883238465633',
  'shopify_US_7230336729185_41883238498401',
];
const pins = {
  [path.join(packet, 'collect_source_only.mjs')]: '7a4085b8b44f3f0b52051909c65dbe97d7e56b5eebdb67b7cca5368fdc930693',
  [path.join(release, 'src/collector.js')]: '1d0c5ef07628ed41b5b0a66f612ef454f35abe54355dfd76803f1a73259716b8',
  [path.join(release, 'src/queries.js')]: '0b7803e02adbb4f32442a0a628396d95f40a79e140b3f761c10e7824d66dbaf9',
  [path.join(release, 'src/generator.js')]: 'a028e2f7f3bb1f0c1f03e222e6b2a608b742f46b6a8f13cc97572885fe009c4f',
  [path.join(release, 'src/eligibility.js')]: '5441bb6aade0f2900f3770602109e14f0e4e964d3e819fff77bf935350038ac8',
  [path.join(release, 'config.json')]: '668e512e5c60c7a6a5696d35b6ef47903157bcc347167f7712315c59b17b2ec8',
  [configPath]: '2c85719db86f8fb4e041c6d4ef66001dfe5e8817d2f1a2e8cf37c641ed98582e',
  [path.join(local, 'eligibility_holds_20260911.json')]: '8ef6615558d3ff08e9b2bcef424041c36e25710be17101bd8145cc46c7b33733',
  [previousUs]: 'fc7aa665746887d1ce37f5bce2d3afa5ed6ea363f9cd362007d4825313797bb3',
};
const sha = value => createHash('sha256').update(value).digest('hex');
const json = value => JSON.stringify(value, null, 2) + '\n';
const compare = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const counts = {};
function check(value, code) {
  if (!value) { const error = new Error(code); error.code = code; throw error; }
  counts[code] = (counts[code] || 0) + 1;
}
async function readJson(file) { return JSON.parse(await fs.readFile(file, 'utf8')); }
function gid(value, type) {
  const match = String(value).match(new RegExp(`^gid://shopify/${type}/([0-9]+)$`));
  check(Boolean(match), 'valid_' + type + '_id'); return match[1];
}
function csv(rows, columns) {
  const cell = value => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? '"' + text.replaceAll('"', '""') + '"' : text;
  };
  return columns.join(',') + '\n' + rows.map(row => columns.map(k => cell(row[k])).join(',')).join('\n') + '\n';
}
function tsvRows(text) {
  const rows = []; let row = [], value = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '"') {
      if (quoted && text[i + 1] === '"') { value += '"'; i++; } else quoted = !quoted;
    } else if (!quoted && (ch === '\t' || ch === '\n')) {
      row.push(value); value = ''; if (ch === '\n') { rows.push(row); row = []; }
    } else value += ch;
  }
  check(!quoted && !value && !row.length, 'accepted_tsv_parse_complete');
  const header = rows.shift();
  return rows.map(values => { check(values.length === header.length, 'accepted_tsv_width'); return Object.fromEntries(header.map((k,i) => [k, values[i]])); });
}
function supplierFacts(value, productId, location = '', found = []) {
  if (typeof value === 'string' && SUPPLIER.test(value)) found.push({ productId, field: location, valueSha256: sha(value), characters: [...value].length });
  else if (Array.isArray(value)) value.forEach((v,i) => supplierFacts(v, productId, `${location}[${i}]`, found));
  else if (value && typeof value === 'object') for (const [k,v] of Object.entries(value)) supplierFacts(v, productId, location ? `${location}.${k}` : k, found);
  return found;
}

async function main() {
  check(process.argv.slice(2).every(x => x === '--verify'), 'supported_local_arguments');
  for (const [file, expected] of Object.entries(pins)) check(sha(await fs.readFile(file)) === expected, 'pinned_input');
  const { validateSnapshot, formatPrice, cleanText, htmlToText } = await import(pathToFileURL(path.join(release, 'src/generator.js')));
  const { manifestRows } = await import(pathToFileURL(path.join(release, 'src/collector.js')));
  const { readEligibilityHolds } = await import(pathToFileURL(path.join(release, 'src/eligibility.js')));
  const receiptPath = path.join(packet, 'collection_receipt.json');
  const intentPath = path.join(packet, 'execution_intent.json');
  const receipt = await readJson(receiptPath), intent = await readJson(intentPath);
  check(receipt.status === 'COMPLETE_FRESH_US_ES_SOURCE_READ' && receipt.privateSourcePath === rawPath && receipt.sourceSha256 === sourceSha, 'complete_receipt_identity');
  check(receipt.liveWrites === 0 && receipt.feedBuild === false && receipt.googleSubmission === false && intent.liveWrites === 0 && intent.feedBuild === false, 'source_only_authority');
  check((await fs.lstat(rawPath)).isFile() && !(await fs.lstat(rawPath)).isSymbolicLink(), 'private_source_regular_file');
  const raw = await fs.readFile(rawPath); check(sha(raw) === sourceSha && raw.length === receipt.sourceBytes, 'unaltered_private_source');
  const snapshot = JSON.parse(raw), originalObjectSha = sha(JSON.stringify(snapshot));
  const config = await readJson(configPath), productionConfig = await readJson(path.join(release, 'config.json'));
  const market = config.markets.find(m => m.key === 'us-es');
  check(market && !market.enabled && !market.landingContextVerified && market.country === 'US' && market.locale === 'es' && market.currency === 'USD' && market.marketId === 'gid://shopify/Market/544735329', 'isolated_us_es_configuration');
  check(Object.keys(config.schedules).length === 0 && config.returnPolicy.emitLabels === false, 'no_schedule_or_return_label_change');
  check(snapshot.completedAt === receipt.sourceCompletedAt && snapshot.startedAt === receipt.sourceStartedAt && snapshot.paginationComplete === true, 'source_clock_and_completeness');
  const evaluationTime = new Date(receipt.atUtc);
  check(Date.parse(snapshot.startedAt) <= Date.parse(snapshot.completedAt) && Date.parse(snapshot.completedAt) <= evaluationTime.getTime(), 'original_clock_order');
  check(receipt.identities.length === 2 && receipt.identities.every(i => i.shopId === config.shopId && i.activeCount.precision === 'EXACT' && i.activeCount.count === snapshot.products.length && i.shopLocales.some(l => l.locale === 'es' && l.published) && i.shopLocales.some(l => l.locale === 'en' && l.primary)), 'two_complete_shop_identities');
  check(JSON.stringify(receipt.identities[0].shopLocales) === JSON.stringify(receipt.identities[1].shopLocales), 'stable_locale_manifest');
  check(JSON.stringify(manifestRows(snapshot.products)) === JSON.stringify(manifestRows(snapshot.finalManifest)), 'complete_final_manifest');
  check(JSON.stringify(snapshot.marketContext) === JSON.stringify(receipt.marketContext) && JSON.stringify(snapshot.marketContext) === JSON.stringify(snapshot.finalMarketContext) && JSON.stringify(snapshot.marketContext.catalogs) === JSON.stringify(market.expectedCatalogs), 'exact_us_catalog_context');
  check(receipt.requests === snapshot.trace.length + 2, 'request_trace_reconciled');
  const tc = snapshot.translationContext;
  check(tc?.strategy === 'global_with_market_overrides' && tc.clockBasis === 'page_response_observations' && tc.locale === 'es' && tc.marketId === market.marketId && JSON.stringify(tc) === JSON.stringify(receipt.translationContext), 'current_collector_translation_provenance');
  check(tc.global.parents === snapshot.products.length && tc.market.parents === snapshot.products.length && Date.parse(tc.market.lastObservedAt) <= Date.parse(tc.global.firstObservedAt) && Date.parse(tc.global.lastObservedAt) <= Date.parse(snapshot.completedAt), 'separate_complete_translation_clocks');
  let guard;
  try { const result = validateSnapshot(snapshot, config, market, evaluationTime); guard = { status: 'PASS', code: null, result }; }
  catch (error) {
    check(error.code === 'supplier_reference_in_source', 'only_supplier_guard_failure_permitted_for_analysis');
    guard = { status: 'FAILED', code: error.code, result: null };
  }
  guard.snapshotModified = false; guard.evaluationTime = receipt.atUtc;
  guard.clockMeaning = 'Reproducible guard evaluation at the original collection receipt; not a new source observation.';
  const holdSpec = await readJson(path.join(local, 'eligibility_holds_20260911.json'));
  const policy = readEligibilityHolds(productionConfig.eligibilityHolds);
  check(policy.source.sha256 === pins[path.join(local, 'eligibility_holds_20260911.json')] && policy.scope === 'all_markets_and_locales', 'unchanged_hold_authority');
  check(JSON.stringify([...policy.parents.keys()].sort(compare)) === JSON.stringify(holdSpec.holds.map(h => h.product_id).sort(compare)) && policy.parents.size === 6, 'six_existing_holds_reconciled');
  const rows = [], parents = [], allVariants = new Set(), allParents = new Set(), suppliers = [], byId = new Map();
  const partition = {}, staleFields = [], selectedScopes = { global: 0, market: 0 };
  const base = new URL(market.landingBaseUrl);
  check(base.href === 'https://www.dresslikemommy.com/es' && !base.search && !base.hash, 'fixed_public_spanish_base');
  for (const product of [...snapshot.products].sort((a,b) => compare(a.id,b.id))) {
    const parentId = gid(product.id, 'Product');
    check(product.status === 'ACTIVE' && !allParents.has(product.id), 'unique_active_parent'); allParents.add(product.id);
    check(product.variantsCount.precision === 'EXACT' && product.variantsCount.count === product.variants.length, 'complete_parent_variants');
    const translations = new Map();
    for (const t of product.translations) {
      check(t.locale === 'es' && typeof t.value === 'string' && typeof t.outdated === 'boolean' && !translations.has(t.key), 'selected_translation_identity');
      check(['global','market'].includes(product.translationSources[t.key]), 'selected_translation_scope');
      translations.set(t.key,t); selectedScopes[product.translationSources[t.key]]++;
      if (t.outdated) staleFields.push({ productId: product.id, key: t.key, selectedScope: product.translationSources[t.key], valueSha256: sha(t.value) });
    }
    check(Object.keys(product.translationSources).length === translations.size, 'translation_source_map_complete');
    const issues = [];
    for (const key of ['title','body_html']) {
      const t = translations.get(key);
      if (!t || !t.value) issues.push('missing_' + key);
      else if (t.outdated) issues.push('stale_' + key);
      else if (!(key === 'title' ? cleanText(t.value) : htmlToText(t.value))) issues.push('empty_' + key);
    }
    const ht = translations.get('handle');
    if (ht?.outdated) issues.push('stale_handle');
    const handle = ht && !ht.outdated && ht.value ? ht.value : product.handle;
    const handleValid = /^[-a-z0-9]+$/i.test(handle || '');
    if (!handleValid) issues.push('invalid_localized_handle');
    const sourceUrl = new URL(product.onlineStoreUrl);
    check(sourceUrl.protocol === 'https:' && !sourceUrl.username && !sourceUrl.password && sourceUrl.hostname.replace(/^www\./,'') === base.hostname.replace(/^www\./,''), 'public_source_domain');
    const sourceFacts = supplierFacts(product, product.id); suppliers.push(...sourceFacts);
    const published = product.onlinePublished && product.countryPublished && product.catalogPublished;
    const held = policy.parents.has(product.id), factual = product.id === tropical;
    let available = 0, potential = 0;
    for (const variant of [...product.variants].sort((a,b) => compare(a.id,b.id))) {
      const variantId = gid(variant.id, 'ProductVariant');
      check(!allVariants.has(variant.id), 'unique_variant_membership'); allVariants.add(variant.id);
      check(typeof variant.availableForSale === 'boolean', 'exact_variant_availability');
      const price = formatPrice(variant.contextualPricing?.price, market); counts.exact_USD_price = (counts.exact_USD_price || 0) + 1;
      const id = `shopify_US_${parentId}_${variantId}`; check(id.length <= 50 && !byId.has(id), 'unique_intended_offer_id');
      const url = handleValid ? new URL(`${base.href}/products/${handle}`) : null;
      if (url) { url.searchParams.set('country','US'); url.searchParams.set('currency','USD'); url.searchParams.set('variant',variantId); }
      if (url) check(url.searchParams.get('variant') === variantId && url.pathname.startsWith('/es/products/') && url.searchParams.get('country') === 'US' && url.searchParams.get('currency') === 'USD', 'exact_intended_buyer_link');
      let status;
      if (!variant.availableForSale) status = 'SOURCE_NOT_AVAILABLE';
      else if (held) status = 'EXISTING_ELIGIBILITY_HOLD';
      else if (!published) status = 'PUBLICATION_OR_MARKET_REJECTED';
      else if (issues.length) status = 'TRANSLATION_REJECTED';
      else if (factual) status = 'TROPICAL_FACTUAL_HOLD';
      else status = 'SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED';
      if (variant.availableForSale) available++;
      if (status === 'SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED') potential++;
      partition[status] = (partition[status] || 0) + 1;
      const row = { country:'US', content_language:'es', proposed_feed_label:'US', intended_google_identity:`es~US~${id}`, intended_offer_id:id, product_id:product.id, variant_id:variant.id, source_price_amount:variant.contextualPricing.price.amount, source_currency:'USD', formatted_source_price:price, source_available_for_sale:variant.availableForSale, online_published:product.onlinePublished, country_published:product.countryPublished, catalog_published:product.catalogPublished, selected_options_sha256:sha(JSON.stringify(variant.selectedOptions)), source_qualification_status:status, translation_issues:issues.join('|'), title_source:product.translationSources.title || 'missing', body_source:product.translationSources.body_html || 'missing', handle_source:ht && !ht.outdated && ht.value ? product.translationSources.handle : 'product_handle_fallback', existing_six_parent_hold:held, tropical_factual_hold:factual, proposed_landing_url:url?.href || '', landing_context_verified:false, submitted:false, source_completed_at_utc:snapshot.completedAt, global_translation_last_observed_at_utc:tc.global.lastObservedAt, market_translation_last_observed_at_utc:tc.market.lastObservedAt };
      rows.push(row); byId.set(id,{row,variant,product});
    }
    parents.push({product_id:product.id,status:product.status,source_updated_at:product.updatedAt,source_title_sha256:sha(product.title),source_description_plain_sha256:sha(product.description),selected_title_sha256:translations.has('title')?sha(translations.get('title').value):'',selected_body_html_sha256:translations.has('body_html')?sha(translations.get('body_html').value):'',title_source:product.translationSources.title||'missing',body_source:product.translationSources.body_html||'missing',selected_translation_count:translations.size,global_selected_count:Object.values(product.translationSources).filter(x=>x==='global').length,market_selected_count:Object.values(product.translationSources).filter(x=>x==='market').length,required_translation_status:issues.length?'REJECTED':'CURRENT_REQUIRED_FIELDS',translation_issues:issues.join('|'),all_variant_count:product.variants.length,available_variant_count:available,potential_offer_count:potential,existing_six_parent_hold:held,tropical_factual_hold:factual,market_publication_qualified:published,supplier_reference_field_count:sourceFacts.length});
  }
  check(allParents.size === receipt.parents && allParents.size === snapshot.activeCount.count, 'all_parent_membership_reconciled');
  check(allVariants.size === receipt.variants && rows.length === allVariants.size && Object.values(partition).reduce((a,b)=>a+b,0) === rows.length, 'complete_disjoint_variant_partition');
  check((guard.status === 'FAILED') === Boolean(suppliers.length), 'supplier_guard_matches_unaltered_source');
  const accepted = new Map(tsvRows(await fs.readFile(previousUs,'utf8')).map(r => [r.id,r]));
  const representatives = [];
  function representative(id,kind) {
    const entry = byId.get(id); check(Boolean(entry), 'representative_source_membership');
    const {row,variant} = entry;
    check(row.source_qualification_status === 'SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED', 'representative_potential_membership');
    check(!SUPPLIER.test(JSON.stringify(variant.selectedOptions)) && !/https?:\/\//i.test(JSON.stringify(variant.selectedOptions)), 'representative_options_safe');
    const prior = accepted.get(id); check(Boolean(prior), 'representative_prior_membership');
    representatives.push({kind,offerId:id,productId:row.product_id,variantId:row.variant_id,expectedPrice:row.formatted_source_price,expectedSelectedOptions:variant.selectedOptions,proposedUrl:row.proposed_landing_url,titleSource:row.title_source,bodySource:row.body_source,handleSource:row.handle_source,availableForSale:row.source_available_for_sale,acceptedUSEnglishPrice:prior.price,acceptedUSEnglishPriceUnchanged:prior.price === row.formatted_source_price,buyerVerification:'NOT_RUN',checksRequired:['Spanish title/description agree with selected source','Numeric URL preselects exact variant without manual repair','Correct role/size/color, exact USD price and availability','Existing buyer-route owner verifies Add/cart only within its authority']});
  }
  for (const id of protectedIds) representative(id,'protected_pilot_or_corrected_price');
  for (const pid of ['gid://shopify/Product/7227375714401','gid://shopify/Product/7546613530721']) {
    const choice = rows.find(r => r.product_id === pid && r.source_qualification_status === 'SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED');
    if (choice) representative(choice.intended_offer_id,'previously_repaired_Spanish_parent');
  }
  check(representatives.slice(0,6).every(r=>r.acceptedUSEnglishPriceUnchanged), 'six_protected_prices_reconciled');
  check(sha(JSON.stringify(snapshot)) === originalObjectSha && sha(await fs.readFile(rawPath)) === sourceSha, 'private_snapshot_never_modified');
  for (const [file, expected] of Object.entries(pins)) check(sha(await fs.readFile(file)) === expected, 'pinned_input_after_analysis');
  const parentCsv = csv(parents,Object.keys(parents[0]));
  const partitionCsv = csv(rows,Object.keys(rows[0]));
  const repPlan = {status:'LOCAL_BUYER_PLAN_NOT_VERIFICATION',sourceCompletedAt:snapshot.completedAt,sourceSha256:sourceSha,market:{country:'US',locale:'es',currency:'USD'},samples:representatives,protectedCount:6,sampleCount:representatives.length,sourceOnly:true,landingContextVerified:false,googleSubmission:false};
  const output = {'complete_source_partition.csv':partitionCsv,'parent_translation_qualification.csv':parentCsv,'representative_plan.json':json(repPlan)};
  const bindingFiles = [self,receiptPath,intentPath,...Object.keys(pins)];
  const bindings = []; for (const file of bindingFiles) bindings.push({path:file,sha256:sha(await fs.readFile(file))});
  const result = {schema:'dlm.us_es_full_source_qualification.v1',status:'SOURCE_PARTITION_COMPLETE__UPLOAD_BLOCKED',sourceStartedAt:snapshot.startedAt,sourceCompletedAt:snapshot.completedAt,sourceReceiptAt:receipt.atUtc,privateSourcePath:rawPath,sourceSha256:sourceSha,sourceBytes:raw.length,market:snapshot.market,marketContext:snapshot.marketContext,translationContext:tc,sourceCounts:{parents:allParents.size,variants:allVariants.size,available:rows.filter(r=>r.source_available_for_sale).length,potentialParents:parents.filter(p=>p.potential_offer_count>0).length,potentialOffers:partition.SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED||0},partition,exclusionPrecedence:['SOURCE_NOT_AVAILABLE','EXISTING_ELIGIBILITY_HOLD','PUBLICATION_OR_MARKET_REJECTED','TRANSLATION_REJECTED','TROPICAL_FACTUAL_HOLD','SOURCE_TRANSLATION_QUALIFIED_LANDING_UNVERIFIED'],selectedTranslationScopes:selectedScopes,staleFields,existingHolds:{sourceSha256:policy.source.sha256,configuredParentIds:[...policy.parents.keys()],sourceAbsentParentIds:[...policy.parents.keys()].filter(id=>!allParents.has(id)),removedAvailableRows:partition.EXISTING_ELIGIBILITY_HOLD||0},tropicalFactualHold:{productId:tropical,key:'body_html',retained:true,sourceParentPresent:allParents.has(tropical),availableRows:rows.filter(r=>r.product_id===tropical&&r.source_available_for_sale).length,selectedBodyOutdated:snapshot.products.find(p=>p.id===tropical)?.translations.find(t=>t.key==='body_html')?.outdated??null,reason:'Unresolved child-weight source truth; no cosmetic re-registration or factual certification.'},supportedValidateSnapshot:guard,supplierReferences:{fields:suppliers.length,parents:new Set(suppliers.map(s=>s.productId)).size,records:suppliers},checks:{passed:Object.values(counts).reduce((a,b)=>a+b,0),failed:0,counts:{...counts}},protectedRepresentatives:{count:6,exactIdsAndCurrentUSDPricesReconciled:true},bindings,outputs:Object.fromEntries(Object.entries(output).map(([file,body])=>[file,{sha256:sha(body),bytes:Buffer.byteLength(body)}])),limits:['Potential means complete source/publication/selected required-translation partition only; not an executable or approved feed.','Supported validateSnapshot was run once on the unaltered private snapshot; any failure remains a blocker. No sanitized snapshot was substituted for a passing guard.','No new source-clock, translation refresh, semantic measurement certification, buyer verification, Google submission or serving result.','Raw product prose/vendor references stay private; outputs contain safe identifiers, source prices, hashes and derived brand-domain buyer links only.','The six existing holds and separate Tropical factual hold remain. LandingContextVerified stays false; no production config, code or theme is changed.'],sourceCollectionPerformedByThisScript:false,externalCalls:0,productionWrites:0,feedBuilt:false,googleSubmission:false,linguisticQualityCertified:false};
  output['source_qualification.json'] = json(result);
  for (const body of Object.values(output)) check(!SUPPLIER.test(body), 'safe_output_without_supplier_domains');
  if (process.argv.includes('--verify')) {
    for (const [file,body] of Object.entries(output)) check(await fs.readFile(path.join(packet,file),'utf8') === body, 'deterministic_output_exact');
  } else {
    for (const file of Object.keys(output)) { try { await fs.access(path.join(packet,file)); throw new Error('output_already_exists'); } catch(error) { if(error.code !== 'ENOENT') throw error; } }
    for (const [file,body] of Object.entries(output)) await fs.writeFile(path.join(packet,file),body,{flag:'wx',mode:0o600});
  }
  console.log(json({status:result.status,mode:process.argv.includes('--verify')?'VERIFY_ONLY':'LOCAL_FILES_WRITTEN',sourceCompletedAt:snapshot.completedAt,sourceCounts:result.sourceCounts,partition,validateSnapshot:guard.status,guardCode:guard.code,sourceQualificationSha256:sha(output['source_qualification.json']),checks:result.checks,externalCalls:0}).trim());
}
main().catch(error=>{console.error(JSON.stringify({status:'LOCAL_QUALIFICATION_FAILED',code:error.code||'local_qualification_failed',externalCalls:0,productionWrites:0}));process.exitCode=1;});
