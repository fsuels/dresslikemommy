import { IDENTITY_QUERY, PRODUCTS_QUERY, VARIANTS_QUERY, MANIFEST_QUERY, MARKET_CONTEXT_QUERY } from './queries.js';

export class SourceError extends Error {
  constructor(code) { super(code); this.name = 'SourceError'; this.code = code; }
}

function assert(value, code) { if (!value) throw new SourceError(code); }
function exact(count) {
  assert(count?.precision === 'EXACT' && Number.isSafeInteger(count.count) && count.count >= 0, 'non_exact_source_count');
  return count.count;
}

export function manifestRows(products) {
  return products.map(p => ({
    id: p.id, status: p.status, updatedAt: p.updatedAt,
    variantsCount: p.variantsCount,
    onlinePublished: p.onlinePublished, countryPublished: p.countryPublished,
    catalogPublished: p.catalogPublished,
  })).sort((a, b) => a.id.localeCompare(b.id));
}

export async function readMarketContext(graphql, market, trace) {
  let currency;
  const catalogs = await paginate(async after => {
    const result = await graphql(MARKET_CONTEXT_QUERY, { country: market.country, after });
    const resolved = result?.marketsResolvedValues;
    assert(resolved?.currencyCode === market.currency && (!currency || currency === resolved.currencyCode), 'resolved_market_currency_mismatch');
    currency = resolved.currencyCode; return result;
  }, d => d.marketsResolvedValues.catalogs, 'market_catalogs', trace);
  assert(catalogs.length > 0 && catalogs.every(c => c.status === 'ACTIVE' && c.publication?.id && c.markets?.pageInfo?.hasNextPage === false), 'market_catalog_context_incomplete');
  const activeMarkets = catalogs.flatMap(c => c.markets.nodes).filter(m => m.status === 'ACTIVE');
  assert(activeMarkets.some(m => m.id === market.marketId), 'configured_market_not_resolved');
  const actual = catalogs.map(c => ({ id: c.id, publicationId: c.publication.id })).sort((a, b) => a.id.localeCompare(b.id));
  const expected = [...market.expectedCatalogs].sort((a, b) => a.id.localeCompare(b.id));
  assert(JSON.stringify(actual) === JSON.stringify(expected), 'resolved_catalog_identity_changed');
  return { currency, catalogs: actual, activeMarketIds: [...new Set(activeMarkets.map(m => m.id))].sort() };
}

async function paginate(load, select, label, trace) {
  const rows = [], cursors = new Set(), ids = new Set();
  let after = null;
  do {
    const response = await load(after);
    const connection = select(response);
    assert(Array.isArray(connection?.nodes) && typeof connection?.pageInfo?.hasNextPage === 'boolean', `${label}_invalid_connection`);
    for (const row of connection.nodes) {
      assert(row?.id && !ids.has(row.id), `${label}_duplicate_id`);
      ids.add(row.id); rows.push(row);
    }
    trace.push({ connection: label, rows: connection.nodes.length, hasNextPage: connection.pageInfo.hasNextPage });
    if (!connection.pageInfo.hasNextPage) break;
    const cursor = connection.pageInfo.endCursor;
    assert(connection.nodes.length > 0 && cursor && !cursors.has(cursor), `${label}_invalid_cursor`);
    cursors.add(cursor); after = cursor;
    assert(cursors.size < 10000, `${label}_pagination_limit`);
  } while (true);
  return rows;
}

function resolvedTranslations(globalRows, marketRows, locale) {
  const values = new Map(), sources = {};
  for (const [source, rows] of [['global', globalRows], ['market', marketRows]]) {
    assert(Array.isArray(rows), 'invalid_translation_records');
    const keys = new Set();
    for (const row of rows) {
      assert(row?.locale === locale && typeof row.key === 'string' && row.key.length > 0 &&
        typeof row.value === 'string' && typeof row.outdated === 'boolean', 'invalid_translation_record');
      assert(!keys.has(row.key), 'duplicate_translation_key'); keys.add(row.key);
      // An empty or stale market override must remain visible to the validator.
      values.set(row.key, row); sources[row.key] = source;
    }
  }
  return { translations: [...values.values()], translationSources: sources };
}

// graphql is injectable: the authenticated reader and a connector-backed adapter
// both use this same completeness contract. No fixture or previous-feed fallback.
export async function collectCatalog(graphql, config, market, { now = () => new Date(), progress = () => {}, readObservedAt = now } = {}) {
  const startedAt = now().toISOString(), trace = [];
  const first = await graphql(IDENTITY_QUERY, {});
  assert(first?.shop?.id === config.shopId, 'wrong_shop');
  const expectedParents = exact(first.activeCount);
  const primary = first.shopLocales?.find(l => l.primary);
  assert(primary?.locale === config.sourceLocale, 'source_locale_mismatch');
  assert(first.shopLocales.some(l => l.locale === market.locale && l.published), 'locale_not_published');
  const verifyCatalog = Array.isArray(market.expectedCatalogs);
  if (verifyCatalog) assert(market.expectedCatalogs.length === 1 && market.marketId, 'single_reviewed_catalog_required');
  const marketContext = verifyCatalog ? await readMarketContext(graphql, market, trace) : null;
  const publicationVariables = { onlinePublicationId: config.onlinePublicationId, verifyCatalog, catalogPublicationId: verifyCatalog ? market.expectedCatalogs[0].publicationId : config.onlinePublicationId };
  const variables = { country: market.country, locale: market.locale, marketId: market.marketId ?? null, ...publicationVariables };
  const contentObservations = [];
  const observedProducts = async (args, observations) => {
    const response = await graphql(PRODUCTS_QUERY, args);
    const observed = readObservedAt();
    assert(Number.isFinite(observed?.getTime()), 'invalid_source_observation_time');
    observations.push(observed.toISOString()); return response;
  };
  const readWindow = (observations, parents) => {
    const sorted = [...observations].sort();
    return { firstObservedAt: sorted[0], lastObservedAt: sorted.at(-1), parents };
  };
  const products = await paginate(
    after => observedProducts({ ...variables, after }, contentObservations), d => d.products, 'products', trace
  );
  assert(products.length === expectedParents, 'active_parent_count_mismatch');
  const variantIds = new Set();
  for (let index = 0; index < products.length; index++) {
    const product = products[index];
    assert(product.status === 'ACTIVE', 'non_active_parent_returned');
    const count = exact(product.variantsCount);
    product.variants = await paginate(async after => {
      const response = await graphql(VARIANTS_QUERY, { id: product.id, country: market.country, after });
      const latest = response?.product;
      assert(latest?.id === product.id && latest.status === product.status, 'product_changed_during_read');
      assert(latest.updatedAt === product.updatedAt && exact(latest.variantsCount) === count, 'product_changed_during_read');
      return response;
    }, d => d.product.variants, `variants:${product.id}`, trace);
    assert(product.variants.length === count, 'variant_count_mismatch');
    for (const variant of product.variants) {
      assert(!variantIds.has(variant.id), 'cross_parent_duplicate_variant');
      variantIds.add(variant.id);
    }
    progress({ productsRead: index + 1, totalProducts: products.length, variantsRead: variantIds.size });
  }
  let translationContext;
  if (market.locale !== config.sourceLocale) {
    const scopedRead = readWindow(contentObservations, products.length);
    let globals = products, globalRead = scopedRead;
    if (market.marketId) {
      const globalObservations = [];
      // Only this separate translation view uses null; the real market/catalog
      // identity and both source-manifest checks remain bound to the country.
      globals = await paginate(
        after => observedProducts({ ...variables, marketId: null, after }, globalObservations),
        d => d.products, 'global_translations', trace
      );
      globalRead = readWindow(globalObservations, globals.length);
      assert(JSON.stringify(manifestRows(globals)) === JSON.stringify(manifestRows(products)), 'translation_source_manifest_mismatch');
    }
    const byId = new Map(globals.map(p => [p.id, p]));
    for (const product of products) {
      Object.assign(product, resolvedTranslations(byId.get(product.id).translations,
        market.marketId ? product.translations : [], market.locale));
    }
    translationContext = { strategy: 'global_with_market_overrides', clockBasis: 'page_response_observations', locale: market.locale,
      marketId: market.marketId ?? null, global: globalRead, market: market.marketId ? scopedRead : null };
  }
  const finalManifest = await paginate(
    after => graphql(MANIFEST_QUERY, { country: market.country, ...publicationVariables, after }),
    d => d.products, 'final_manifest', trace
  );
  const last = await graphql(IDENTITY_QUERY, {});
  assert(last?.shop?.id === config.shopId && exact(last.activeCount) === expectedParents, 'catalog_changed_during_read');
  assert(JSON.stringify(manifestRows(products)) === JSON.stringify(manifestRows(finalManifest)), 'catalog_changed_during_read');
  assert(JSON.stringify(first.shopLocales) === JSON.stringify(last.shopLocales), 'locales_changed_during_read');
  const finalMarketContext = verifyCatalog ? await readMarketContext(graphql, market, trace) : null;
  assert(JSON.stringify(marketContext) === JSON.stringify(finalMarketContext), 'market_context_changed_during_read');
  // Tags are used only for an exact Final Sale classification. A URL-bearing tag
  // is unrelated source data and must never be persisted or emitted.
  let omittedUrlTags = 0;
  for (const product of products) {
    product.tags = (product.tags || []).filter(tag => {
      if (/https?:\/\//i.test(tag)) { omittedUrlTags++; return false; }
      return true;
    });
  }
  return {
    schemaVersion: 1, startedAt, completedAt: now().toISOString(),
    shop: first.shop, sourceLocale: primary.locale,
    market: { key: market.key, country: market.country, locale: market.locale, currency: market.currency, marketId: market.marketId ?? null },
    onlinePublicationId: config.onlinePublicationId,
    marketContext, finalMarketContext,
    activeCount: first.activeCount, finalActiveCount: last.activeCount,
    products, finalManifest: manifestRows(finalManifest),
    paginationComplete: true, trace,
    ...(translationContext ? { translationContext } : {}),
    sanitization: { omittedUrlTags, customerOrOrderFieldsRequested: false },
  };
}

export function createAdminReader({ domain, token, apiVersion = '2026-07', fetchImpl = fetch, sleep = ms => new Promise(r => setTimeout(r, ms)) }) {
  assert(/^[a-z0-9][a-z0-9-]*\.myshopify\.com$/.test(domain || ''), 'invalid_admin_domain');
  assert(typeof token === 'string' && token.length > 0, 'admin_token_missing');
  assert(/^20\d{2}-(01|04|07|10)$/.test(apiVersion), 'invalid_api_version');
  const endpoint = `https://${domain}/admin/api/${apiVersion}/graphql.json`;
  return async (query, variables) => {
    let response;
    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        response = await fetchImpl(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': token },
          body: JSON.stringify({ query, variables }), signal: AbortSignal.timeout(60000), redirect: 'error',
        });
      } catch { throw new SourceError('shopify_network_error'); }
      if ([500, 502, 503, 504].includes(response.status) && attempt === 0) { await sleep(1000); continue; }
      break;
    }
    if (!response.ok) throw new SourceError(`shopify_http_${response.status}`);
    let payload;
    try { payload = await response.json(); } catch { throw new SourceError('shopify_invalid_json'); }
    if (payload.errors?.length) {
      const codes = payload.errors.map(e => e.extensions?.code);
      throw new SourceError(codes.includes('THROTTLED') ? 'shopify_throttled' : codes.includes('ACCESS_DENIED') ? 'shopify_access_denied' : 'shopify_graphql_error');
    }
    assert(payload.data, 'shopify_missing_data');
    const throttle = payload.extensions?.cost?.throttleStatus;
    // Pace before the next operation instead of hammering a depleted bucket.
    if (throttle?.restoreRate > 0 && throttle.currentlyAvailable < 900) {
      await sleep(Math.ceil((900 - throttle.currentlyAvailable) / throttle.restoreRate * 1000));
    }
    return payload.data;
  };
}
