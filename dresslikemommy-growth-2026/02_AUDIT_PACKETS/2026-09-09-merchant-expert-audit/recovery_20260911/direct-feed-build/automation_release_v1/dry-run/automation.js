var __defProp = Object.defineProperty;
var __name = (target, value2) => __defProp(target, "name", { value: value2, configurable: true });

// src/host.js
var TSV_TYPE = "text/tab-separated-values; charset=utf-8";
function json(value2, status, headers = {}) {
  return new Response(JSON.stringify(value2), { status, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", ...headers } });
}
__name(json, "json");
var host_default = {
  async fetch(request, env) {
    if (!["GET", "HEAD"].includes(request.method)) return json({ error: "method_not_allowed" }, 405, { Allow: "GET, HEAD" });
    const url = new URL(request.url);
    if (url.pathname === "/health") return json({ ok: true, service: "merchant-feed-reader" }, 200);
    const match = url.pathname.match(/^\/feeds\/([a-z]{2}-[a-z]{2}(?:-[a-z]{2})?)\.tsv$/);
    if (!match) return json({ error: "not_found" }, 404);
    try {
      const config = JSON.parse(env.MERCHANT_CONFIG_JSON);
      const market = config.markets?.find((m) => m.key === match[1] && m.enabled);
      if (!market) return json({ error: "market_not_enabled" }, 404);
      const pointer = await env.MERCHANT_FEED_BUCKET.get(`merchant/${market.key}/current.json`);
      if (!pointer) return json({ error: "feed_unavailable" }, 503);
      const manifest = JSON.parse(await pointer.text());
      const age = Date.now() - Date.parse(manifest.sourceCompletedAt);
      if (manifest.schemaVersion !== 1 || manifest.market?.key !== market.key || manifest.market.country !== market.country || manifest.market.locale !== market.locale || manifest.market.currency !== market.currency || !/^[a-f0-9]{64}$/.test(manifest.sha256 || "") || !manifest.objectEtag || manifest.objectKey !== `merchant/${market.key}/${manifest.sha256}.tsv` || !Number.isFinite(age) || age < -6e4 || age > (config.maxFeedAgeHours ?? 48) * 36e5) return json({ error: "feed_manifest_invalid_or_stale" }, 503);
      const object = await env.MERCHANT_FEED_BUCKET.get(manifest.objectKey);
      if (!object || object.size > 6e7 || object.size !== manifest.bytes || object.etag !== manifest.objectEtag) return json({ error: "feed_object_invalid" }, 503);
      return new Response(request.method === "HEAD" ? null : object.body, { status: 200, headers: {
        "Content-Type": TSV_TYPE,
        "Cache-Control": "public, max-age=300",
        "X-Content-Type-Options": "nosniff",
        "Content-Length": String(manifest.bytes),
        ETag: `"${manifest.sha256}"`,
        "X-DLM-Feed-SHA256": manifest.sha256,
        "X-DLM-Feed-Rows": String(manifest.rows),
        "X-DLM-Feed-Country": market.country,
        "X-DLM-Feed-Language": market.locale,
        "X-DLM-Feed-Currency": market.currency,
        "X-DLM-Feed-Source-Updated": manifest.sourceCompletedAt
      } });
    } catch {
      return json({ error: "feed_unavailable" }, 503);
    }
  }
};

// src/queries.js
var IDENTITY_QUERY = `query MerchantFeedIdentity {
  shop { id name currencyCode primaryDomain { url } }
  shopLocales { locale primary published }
  activeCount: productsCount(query: "status:active", limit: null) { count precision }
}`;
var ATTRIBUTES = `
  gAgeGroup: metafield(namespace: "mm-google-shopping", key: "age_group") { value }
  gGender: metafield(namespace: "mm-google-shopping", key: "gender") { value }
  gColor: metafield(namespace: "mm-google-shopping", key: "color") { value }
  gSize: metafield(namespace: "mm-google-shopping", key: "size") { value }
  gBrand: metafield(namespace: "mm-google-shopping", key: "brand") { value }
  gMpn: metafield(namespace: "mm-google-shopping", key: "mpn") { value }
  gCondition: metafield(namespace: "mm-google-shopping", key: "condition") { value }
  gIdentifierExists: metafield(namespace: "mm-google-shopping", key: "identifier_exists") { value }
`;
var MARKET_CONTEXT_QUERY = `query MerchantFeedMarketContext($country: CountryCode!, $after: String) {
  marketsResolvedValues(buyerSignal: { countryCode: $country }) {
    currencyCode
    catalogs(first: 50, after: $after) {
      nodes { id status publication { id }
        markets(first: 50) { nodes { id name status } pageInfo { hasNextPage endCursor } }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}`;
var PRODUCTS_QUERY = `query MerchantFeedProducts(
  $after: String, $country: CountryCode!, $locale: String!, $marketId: ID,
  $onlinePublicationId: ID!, $catalogPublicationId: ID!, $verifyCatalog: Boolean!
) {
  products(first: 25, after: $after, sortKey: ID, query: "status:active") {
    nodes {
      id status updatedAt handle title description productType tags isGiftCard
      onlineStoreUrl
      onlinePublished: publishedOnPublication(publicationId: $onlinePublicationId)
      catalogPublished: publishedOnPublication(publicationId: $catalogPublicationId) @include(if: $verifyCatalog)
      countryPublished: publishedInContext(context: { country: $country })
      variantsCount { count precision }
      featuredMedia { ... on MediaImage { image { url } } }
      category { id name fullName }
      translations(locale: $locale, marketId: $marketId) { key value locale outdated }
      taxonomyGender: metafield(namespace: "shopify", key: "target-gender") {
        references(first: 5) { nodes { ... on Metaobject { displayName } } pageInfo { hasNextPage endCursor } }
      }
      taxonomyAgeGroup: metafield(namespace: "shopify", key: "age-group") {
        references(first: 5) { nodes { ... on Metaobject { displayName } } pageInfo { hasNextPage endCursor } }
      }
      taxonomyColor: metafield(namespace: "shopify", key: "color-pattern") {
        references(first: 5) { nodes { ... on Metaobject { displayName } } pageInfo { hasNextPage endCursor } }
      }
      ${ATTRIBUTES}
    }
    pageInfo { hasNextPage endCursor }
  }
}`;
var VARIANTS_QUERY = `query MerchantFeedVariants($id: ID!, $after: String, $country: CountryCode!) {
  product(id: $id) {
    id status updatedAt variantsCount { count precision }
    variants(first: 40, after: $after) {
      nodes {
        id availableForSale barcode selectedOptions { name value }
        contextualPricing(context: { country: $country }) { price { amount currencyCode } }
        media(first: 1) { nodes { ... on MediaImage { image { url } } } }
        ${ATTRIBUTES}
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}`;
var MANIFEST_QUERY = `query MerchantFeedManifest($after: String, $country: CountryCode!, $onlinePublicationId: ID!, $catalogPublicationId: ID!, $verifyCatalog: Boolean!) {
  products(first: 50, after: $after, sortKey: ID, query: "status:active") {
    nodes {
      id status updatedAt variantsCount { count precision }
      onlinePublished: publishedOnPublication(publicationId: $onlinePublicationId)
      catalogPublished: publishedOnPublication(publicationId: $catalogPublicationId) @include(if: $verifyCatalog)
      countryPublished: publishedInContext(context: { country: $country })
    }
    pageInfo { hasNextPage endCursor }
  }
}`;

// src/collector.js
var SourceError = class extends Error {
  static {
    __name(this, "SourceError");
  }
  constructor(code) {
    super(code);
    this.name = "SourceError";
    this.code = code;
  }
};
function assert(value2, code) {
  if (!value2) throw new SourceError(code);
}
__name(assert, "assert");
function exact(count) {
  assert(count?.precision === "EXACT" && Number.isSafeInteger(count.count) && count.count >= 0, "non_exact_source_count");
  return count.count;
}
__name(exact, "exact");
function manifestRows(products) {
  return products.map((p) => ({
    id: p.id,
    status: p.status,
    updatedAt: p.updatedAt,
    variantsCount: p.variantsCount,
    onlinePublished: p.onlinePublished,
    countryPublished: p.countryPublished,
    catalogPublished: p.catalogPublished
  })).sort((a, b) => a.id.localeCompare(b.id));
}
__name(manifestRows, "manifestRows");
async function readMarketContext(graphql, market, trace) {
  let currency;
  const catalogs = await paginate(async (after) => {
    const result = await graphql(MARKET_CONTEXT_QUERY, { country: market.country, after });
    const resolved = result?.marketsResolvedValues;
    assert(resolved?.currencyCode === market.currency && (!currency || currency === resolved.currencyCode), "resolved_market_currency_mismatch");
    currency = resolved.currencyCode;
    return result;
  }, (d) => d.marketsResolvedValues.catalogs, "market_catalogs", trace);
  assert(catalogs.length > 0 && catalogs.every((c) => c.status === "ACTIVE" && c.publication?.id && c.markets?.pageInfo?.hasNextPage === false), "market_catalog_context_incomplete");
  const activeMarkets = catalogs.flatMap((c) => c.markets.nodes).filter((m) => m.status === "ACTIVE");
  assert(activeMarkets.some((m) => m.id === market.marketId), "configured_market_not_resolved");
  const actual = catalogs.map((c) => ({ id: c.id, publicationId: c.publication.id })).sort((a, b) => a.id.localeCompare(b.id));
  const expected = [...market.expectedCatalogs].sort((a, b) => a.id.localeCompare(b.id));
  assert(JSON.stringify(actual) === JSON.stringify(expected), "resolved_catalog_identity_changed");
  return { currency, catalogs: actual, activeMarketIds: [...new Set(activeMarkets.map((m) => m.id))].sort() };
}
__name(readMarketContext, "readMarketContext");
async function paginate(load, select, label, trace) {
  const rows = [], cursors = /* @__PURE__ */ new Set(), ids = /* @__PURE__ */ new Set();
  let after = null;
  do {
    const response = await load(after);
    const connection = select(response);
    assert(Array.isArray(connection?.nodes) && typeof connection?.pageInfo?.hasNextPage === "boolean", `${label}_invalid_connection`);
    for (const row of connection.nodes) {
      assert(row?.id && !ids.has(row.id), `${label}_duplicate_id`);
      ids.add(row.id);
      rows.push(row);
    }
    trace.push({ connection: label, rows: connection.nodes.length, hasNextPage: connection.pageInfo.hasNextPage });
    if (!connection.pageInfo.hasNextPage) break;
    const cursor = connection.pageInfo.endCursor;
    assert(connection.nodes.length > 0 && cursor && !cursors.has(cursor), `${label}_invalid_cursor`);
    cursors.add(cursor);
    after = cursor;
    assert(cursors.size < 1e4, `${label}_pagination_limit`);
  } while (true);
  return rows;
}
__name(paginate, "paginate");
async function collectCatalog(graphql, config, market, { now = /* @__PURE__ */ __name(() => /* @__PURE__ */ new Date(), "now"), progress = /* @__PURE__ */ __name(() => {
}, "progress") } = {}) {
  const startedAt = now().toISOString(), trace = [];
  const first = await graphql(IDENTITY_QUERY, {});
  assert(first?.shop?.id === config.shopId, "wrong_shop");
  const expectedParents = exact(first.activeCount);
  const primary = first.shopLocales?.find((l) => l.primary);
  assert(primary?.locale === config.sourceLocale, "source_locale_mismatch");
  assert(first.shopLocales.some((l) => l.locale === market.locale && l.published), "locale_not_published");
  const verifyCatalog = Array.isArray(market.expectedCatalogs);
  if (verifyCatalog) assert(market.expectedCatalogs.length === 1 && market.marketId, "single_reviewed_catalog_required");
  const marketContext = verifyCatalog ? await readMarketContext(graphql, market, trace) : null;
  const publicationVariables = { onlinePublicationId: config.onlinePublicationId, verifyCatalog, catalogPublicationId: verifyCatalog ? market.expectedCatalogs[0].publicationId : config.onlinePublicationId };
  const variables = { country: market.country, locale: market.locale, marketId: market.marketId ?? null, ...publicationVariables };
  const products = await paginate(
    (after) => graphql(PRODUCTS_QUERY, { ...variables, after }),
    (d) => d.products,
    "products",
    trace
  );
  assert(products.length === expectedParents, "active_parent_count_mismatch");
  const variantIds = /* @__PURE__ */ new Set();
  for (let index = 0; index < products.length; index++) {
    const product = products[index];
    assert(product.status === "ACTIVE", "non_active_parent_returned");
    const count = exact(product.variantsCount);
    product.variants = await paginate(async (after) => {
      const response = await graphql(VARIANTS_QUERY, { id: product.id, country: market.country, after });
      const latest = response?.product;
      assert(latest?.id === product.id && latest.status === product.status, "product_changed_during_read");
      assert(latest.updatedAt === product.updatedAt && exact(latest.variantsCount) === count, "product_changed_during_read");
      return response;
    }, (d) => d.product.variants, `variants:${product.id}`, trace);
    assert(product.variants.length === count, "variant_count_mismatch");
    for (const variant of product.variants) {
      assert(!variantIds.has(variant.id), "cross_parent_duplicate_variant");
      variantIds.add(variant.id);
    }
    progress({ productsRead: index + 1, totalProducts: products.length, variantsRead: variantIds.size });
  }
  const finalManifest = await paginate(
    (after) => graphql(MANIFEST_QUERY, { country: market.country, ...publicationVariables, after }),
    (d) => d.products,
    "final_manifest",
    trace
  );
  const last = await graphql(IDENTITY_QUERY, {});
  assert(last?.shop?.id === config.shopId && exact(last.activeCount) === expectedParents, "catalog_changed_during_read");
  assert(JSON.stringify(manifestRows(products)) === JSON.stringify(manifestRows(finalManifest)), "catalog_changed_during_read");
  assert(JSON.stringify(first.shopLocales) === JSON.stringify(last.shopLocales), "locales_changed_during_read");
  const finalMarketContext = verifyCatalog ? await readMarketContext(graphql, market, trace) : null;
  assert(JSON.stringify(marketContext) === JSON.stringify(finalMarketContext), "market_context_changed_during_read");
  let omittedUrlTags = 0;
  for (const product of products) {
    product.tags = (product.tags || []).filter((tag) => {
      if (/https?:\/\//i.test(tag)) {
        omittedUrlTags++;
        return false;
      }
      return true;
    });
  }
  return {
    schemaVersion: 1,
    startedAt,
    completedAt: now().toISOString(),
    shop: first.shop,
    sourceLocale: primary.locale,
    market: { key: market.key, country: market.country, locale: market.locale, currency: market.currency, marketId: market.marketId ?? null },
    onlinePublicationId: config.onlinePublicationId,
    marketContext,
    finalMarketContext,
    activeCount: first.activeCount,
    finalActiveCount: last.activeCount,
    products,
    finalManifest: manifestRows(finalManifest),
    paginationComplete: true,
    trace,
    sanitization: { omittedUrlTags, customerOrOrderFieldsRequested: false }
  };
}
__name(collectCatalog, "collectCatalog");
function createAdminReader({ domain, token, apiVersion = "2026-07", fetchImpl = fetch, sleep = /* @__PURE__ */ __name((ms) => new Promise((r) => setTimeout(r, ms)), "sleep") }) {
  assert(/^[a-z0-9][a-z0-9-]*\.myshopify\.com$/.test(domain || ""), "invalid_admin_domain");
  assert(typeof token === "string" && token.length > 0, "admin_token_missing");
  assert(/^20\d{2}-(01|04|07|10)$/.test(apiVersion), "invalid_api_version");
  const endpoint = `https://${domain}/admin/api/${apiVersion}/graphql.json`;
  return async (query, variables) => {
    let response;
    for (let attempt = 0; attempt < 2; attempt++) {
      try {
        response = await fetchImpl(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-Shopify-Access-Token": token },
          body: JSON.stringify({ query, variables }),
          signal: AbortSignal.timeout(6e4),
          redirect: "error"
        });
      } catch {
        throw new SourceError("shopify_network_error");
      }
      if ([500, 502, 503, 504].includes(response.status) && attempt === 0) {
        await sleep(1e3);
        continue;
      }
      break;
    }
    if (!response.ok) throw new SourceError(`shopify_http_${response.status}`);
    let payload;
    try {
      payload = await response.json();
    } catch {
      throw new SourceError("shopify_invalid_json");
    }
    if (payload.errors?.length) {
      const codes = payload.errors.map((e) => e.extensions?.code);
      throw new SourceError(codes.includes("THROTTLED") ? "shopify_throttled" : codes.includes("ACCESS_DENIED") ? "shopify_access_denied" : "shopify_graphql_error");
    }
    assert(payload.data, "shopify_missing_data");
    const throttle = payload.extensions?.cost?.throttleStatus;
    if (throttle?.restoreRate > 0 && throttle.currentlyAvailable < 900) {
      await sleep(Math.ceil((900 - throttle.currentlyAvailable) / throttle.restoreRate * 1e3));
    }
    return payload.data;
  };
}
__name(createAdminReader, "createAdminReader");

// src/generator.js
var COLUMNS = ["id", "item_group_id", "title", "description", "link", "image_link", "availability", "price", "condition", "brand", "gtin", "mpn", "identifier_exists", "age_group", "gender", "color", "size", "return_policy_label", "excluded_destination"];
var SUPPLIER = /(?:alibaba\.com|aliexpress\.com|1688\.com|taobao\.com|tmall\.com)/i;
var AGE = /* @__PURE__ */ new Set(["newborn", "infant", "toddler", "kids", "adult"]);
var GENDER = /* @__PURE__ */ new Set(["female", "male", "unisex"]);
var CONDITION = /* @__PURE__ */ new Set(["new", "used", "refurbished"]);
var ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: "\xA0", ndash: "\u2013", mdash: "\u2014", rsquo: "\u2019", lsquo: "\u2018", ldquo: "\u201C", rdquo: "\u201D", hellip: "\u2026", copy: "\xA9", reg: "\xAE", trade: "\u2122", euro: "\u20AC", pound: "\xA3", yen: "\xA5", middot: "\xB7", times: "\xD7", bull: "\u2022" };
function assert2(value2, code) {
  if (!value2) throw new SourceError(code);
}
__name(assert2, "assert");
function cleanText(value2) {
  return String(value2 ?? "").replace(/&#(x[0-9a-f]+|\d+);|&([a-z]+);/gi, (original, numeric, named) => {
    if (named) return ENTITIES[named.toLowerCase()] ?? original;
    const number = numeric[0].toLowerCase() === "x" ? parseInt(numeric.slice(1), 16) : Number(numeric);
    return number > 0 && number <= 1114111 && !(number >= 55296 && number <= 57343) ? String.fromCodePoint(number) : " ";
  }).replace(/[\u0000-\u001f\u007f-\u009f\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]/g, " ").replace(/\s+/g, " ").trim();
}
__name(cleanText, "cleanText");
function htmlToText(value2) {
  return cleanText(String(value2 ?? "").replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<[^>]*>/g, " "));
}
__name(htmlToText, "htmlToText");
function value(entity, key) {
  return cleanText(entity?.[key]?.value);
}
__name(value, "value");
function option(variant, name) {
  return cleanText(variant.selectedOptions?.find((o) => o.name?.trim().toLowerCase() === name)?.value);
}
__name(option, "option");
function taxonomy(product, key) {
  const refs = product[key]?.references;
  if (!refs || refs.pageInfo?.hasNextPage) return [];
  return (refs.nodes || []).map((n) => cleanText(n?.displayName)).filter(Boolean);
}
__name(taxonomy, "taxonomy");
function enumValue(raw, allowed) {
  const text = cleanText(raw).toLowerCase();
  return allowed.has(text) ? text : "";
}
__name(enumValue, "enumValue");
function taxonomyAge(raw) {
  const names = { adults: "adult", adult: "adult", kids: "kids", children: "kids", infants: "infant", infant: "infant", toddlers: "toddler", toddler: "toddler", newborn: "newborn" };
  return names[raw?.toLowerCase()] || "";
}
__name(taxonomyAge, "taxonomyAge");
function deriveVariantAge(variant) {
  const parts = (variant.selectedOptions || []).filter((o) => /^(size|role|family member|age)$/i.test(o.name || "")).map((o) => cleanText(o.value));
  if (parts.some((x) => /\b(adult|mother|father|mom|dad|women|woman|men|man)\b/i.test(x))) return "adult";
  const size = option(variant, "size");
  const match = size.match(/\b(\d+)(?:\s*[-–]\s*(\d+))?\s*(months?|years?|yrs?)\b/i);
  if (!match) return "";
  let low = Number(match[1]), high = Number(match[2] ?? match[1]);
  if (low > high) return "";
  if (/^y/i.test(match[3])) {
    low *= 12;
    high *= 12;
  }
  const group = /* @__PURE__ */ __name((months) => months < 3 ? "newborn" : months < 12 ? "infant" : months < 60 ? "toddler" : months < 156 ? "kids" : "adult", "group");
  return group(low) === group(high) ? group(low) : "";
}
__name(deriveVariantAge, "deriveVariantAge");
function deriveVariantGender(variant) {
  const source = (variant.selectedOptions || []).filter((o) => /^(size|role|family member|gender)$/i.test(o.name || "")).map((o) => o.value).join(" ");
  const female = /\b(mother|mom|women|woman|girl|daughter|female)\b/i.test(source);
  const male = /\b(father|dad|men|man|boy|son|male)\b/i.test(source);
  if (female && !male) return "female";
  if (male && !female) return "male";
  return /\bunisex\b/i.test(source) && !female && !male ? "unisex" : "";
}
__name(deriveVariantGender, "deriveVariantGender");
function variantAgeConflict(variant, age) {
  const groundedAge = deriveVariantAge(variant);
  if (groundedAge === age) return false;
  const source = (variant.selectedOptions || []).filter((o) => /^(size|role|family member|age)$/i.test(o.name || "")).map((o) => o.value).join(" ");
  const child = /\b(child|children|girl|boy|daughter|son|baby|infant|toddler|kids?)\b|\b[0-9]+T\b/i.test(source);
  const adult = /\b(adult|mother|father|mom|dad|women|woman|men|man)\b/i.test(source);
  return age === "adult" && child && !adult || age && age !== "adult" && adult && !child;
}
__name(variantAgeConflict, "variantAgeConflict");
function classifyReturnPolicy(product, rules = {}) {
  const facts = [];
  if (product.isGiftCard === true) facts.push({ field: "isGiftCard", value: true });
  const type = cleanText(product.productType);
  if ((rules.productTypes || []).some((x) => x.toLowerCase() === type.toLowerCase())) facts.push({ field: "productType", value: type });
  const names = (product.category?.fullName || "").split(" > ").map((x) => x.trim());
  for (const name of rules.taxonomyNames || []) if (names.includes(name)) facts.push({ field: "category.fullName.segment", value: name });
  for (const tag of product.tags || []) if ((rules.finalSaleTags || []).includes(tag)) facts.push({ field: "tags.exact", value: tag });
  return facts.length ? { classification: "verified_policy_exception", label: cleanText(rules.exceptionLabel), facts } : { classification: "no_explicit_exception_identified", label: "", facts: [] };
}
__name(classifyReturnPolicy, "classifyReturnPolicy");
function validGtin(input) {
  const text = String(input ?? "").trim();
  if (!/^(?:\d{8}|\d{12}|\d{13}|\d{14})$/.test(text) || /^(\d)\1+$/.test(text)) return false;
  let sum = 0;
  for (let i = text.length - 2, weight = 3; i >= 0; i--, weight = weight === 3 ? 1 : 3) sum += Number(text[i]) * weight;
  return (10 - sum % 10) % 10 === Number(text.at(-1));
}
__name(validGtin, "validGtin");
function numericId(gid, type) {
  const match = String(gid || "").match(new RegExp(`^gid://shopify/${type}/([0-9]+)$`));
  assert2(match, "invalid_shopify_id");
  return match[1];
}
__name(numericId, "numericId");
function formatPrice(money, market) {
  assert2(money?.currencyCode === market.currency, "contextual_currency_mismatch");
  const raw = String(money.amount);
  assert2(/^\d+(?:\.\d+)?$/.test(raw), "invalid_contextual_price");
  let [whole, fraction = ""] = raw.split(".");
  const places = market.minorUnits ?? 2;
  assert2(Number.isInteger(places) && places >= 0 && places <= 3, "invalid_currency_minor_units");
  assert2(!/[1-9]/.test(fraction.slice(places)), "price_requires_rounding");
  whole = whole.replace(/^0+(?=\d)/, "");
  fraction = fraction.slice(0, places).padEnd(places, "0");
  assert2(/[1-9]/.test(whole + fraction), "non_positive_price");
  return `${whole}${places ? "." + fraction : ""} ${market.currency}`;
}
__name(formatPrice, "formatPrice");
function httpsUrl(raw, code) {
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new SourceError(code);
  }
  assert2(url.protocol === "https:" && !url.username && !url.password && !SUPPLIER.test(url.hostname), code);
  return url;
}
__name(httpsUrl, "httpsUrl");
function localizedContent(product, config, market) {
  if (market.locale === config.sourceLocale) return { title: cleanText(product.title), description: cleanText(product.description), handle: product.handle };
  const translations = new Map((product.translations || []).filter((t) => t.locale === market.locale && !t.outdated).map((t) => [t.key, t.value]));
  assert2(translations.get("title") && translations.get("body_html"), "missing_or_stale_translation");
  const staleHandle = (product.translations || []).some((t) => t.locale === market.locale && t.key === "handle" && t.outdated);
  assert2(!staleHandle, "stale_handle_translation");
  return { title: cleanText(translations.get("title")), description: htmlToText(translations.get("body_html")), handle: translations.get("handle") || product.handle };
}
__name(localizedContent, "localizedContent");
function landingLink(product, variant, content, market) {
  assert2(market.landingContextVerified === true, "landing_context_unverified");
  const base = httpsUrl(market.landingBaseUrl, "invalid_landing_base");
  const source = httpsUrl(product.onlineStoreUrl, "invalid_source_product_url");
  assert2(source.hostname.replace(/^www\./, "") === base.hostname.replace(/^www\./, ""), "landing_domain_mismatch");
  assert2(!base.search && !base.hash && /^[-a-z0-9]+$/i.test(content.handle || ""), "invalid_localized_handle");
  const url = new URL(`${base.href.replace(/\/$/, "")}/products/${content.handle}`);
  for (const [key, val] of Object.entries(market.landingQuery || {})) {
    assert2(["country", "currency"].includes(key), "unsupported_landing_query");
    url.searchParams.set(key, val);
  }
  url.searchParams.set("variant", numericId(variant.id, "ProductVariant"));
  return url.href;
}
__name(landingLink, "landingLink");
function cell(text) {
  const result = cleanText(text);
  return result.includes('"') ? `"${result.replace(/"/g, '""')}"` : result;
}
__name(cell, "cell");
async function sha256(text) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
__name(sha256, "sha256");
function validateSnapshot(snapshot, config, market, now = /* @__PURE__ */ new Date()) {
  assert2(snapshot?.schemaVersion === 1 && snapshot.paginationComplete === true, "incomplete_snapshot");
  assert2(snapshot.shop?.id === config.shopId && snapshot.onlinePublicationId === config.onlinePublicationId, "snapshot_identity_mismatch");
  assert2(snapshot.sourceLocale === config.sourceLocale, "snapshot_source_locale_mismatch");
  if (market.expectedCatalogs) {
    assert2(snapshot.marketContext?.currency === market.currency && snapshot.marketContext.activeMarketIds?.includes(market.marketId), "snapshot_market_context_missing");
    assert2(JSON.stringify(snapshot.marketContext) === JSON.stringify(snapshot.finalMarketContext), "snapshot_market_context_changed");
    assert2(JSON.stringify(snapshot.marketContext.catalogs) === JSON.stringify(market.expectedCatalogs), "snapshot_catalog_identity_mismatch");
  }
  assert2(snapshot.market?.key === market.key && snapshot.market.country === market.country && snapshot.market.locale === market.locale && snapshot.market.currency === market.currency && (snapshot.market.marketId ?? null) === (market.marketId ?? null), "snapshot_market_mismatch");
  const completed = Date.parse(snapshot.completedAt), age = now.getTime() - completed;
  assert2(Number.isFinite(completed) && age >= -6e4 && age <= (config.maxSnapshotAgeHours ?? 24) * 36e5, "stale_or_future_snapshot");
  assert2(snapshot.activeCount?.precision === "EXACT" && Number.isSafeInteger(snapshot.activeCount.count) && snapshot.activeCount.count >= 0, "non_exact_parent_count");
  assert2(JSON.stringify(snapshot.activeCount) === JSON.stringify(snapshot.finalActiveCount), "active_count_changed");
  assert2(Array.isArray(snapshot.products) && snapshot.products.length === snapshot.activeCount.count, "parent_count_mismatch");
  assert2(JSON.stringify(manifestRows(snapshot.products)) === JSON.stringify(manifestRows(snapshot.finalManifest || [])), "manifest_mismatch");
  const parents = /* @__PURE__ */ new Set(), variants = /* @__PURE__ */ new Set();
  for (const p of snapshot.products) {
    assert2(p.status === "ACTIVE" && !parents.has(p.id), "invalid_parent_identity");
    parents.add(p.id);
    assert2(p.variantsCount?.precision === "EXACT" && Number.isSafeInteger(p.variantsCount.count) && Array.isArray(p.variants) && p.variants.length === p.variantsCount.count, "incomplete_variants");
    assert2(typeof p.onlinePublished === "boolean" && typeof p.countryPublished === "boolean", "missing_publication_state");
    if (market.expectedCatalogs) assert2(typeof p.catalogPublished === "boolean", "missing_catalog_publication_state");
    for (const v of p.variants) {
      assert2(!variants.has(v.id), "duplicate_variant_id");
      variants.add(v.id);
    }
  }
  assert2(!SUPPLIER.test(JSON.stringify(snapshot.products)), "supplier_reference_in_source");
  return { parents: parents.size, variants: variants.size };
}
__name(validateSnapshot, "validateSnapshot");
function* tsvChunks(rows, columns) {
  const encoder = new TextEncoder();
  yield encoder.encode(columns.join("	") + "\n");
  for (const row of rows) yield encoder.encode(columns.map((column) => cell(row[column])).join("	") + "\n");
}
__name(tsvChunks, "tsvChunks");
async function buildFeed(snapshot, config, market, { now = /* @__PURE__ */ new Date(), previousIds = [], materialize = true } = {}) {
  const sourceCounts = validateSnapshot(snapshot, config, market, now);
  assert2(/^[a-z]{2}-[a-z]{2}(?:-[a-z]{2})?$/.test(market.key) && /^[A-Z]{2}$/.test(market.country) && /^[A-Z]{3}$/.test(market.currency), "invalid_market_configuration");
  const rows = [], errors = [], warnings = [], exclusions = [], returnCohorts = [];
  let exceptionRows = 0;
  for (const product of snapshot.products) {
    if (!product.onlinePublished || !product.countryPublished || market.expectedCatalogs && !product.catalogPublished) {
      exclusions.push({ productId: product.id, variants: product.variants.length, code: !product.onlinePublished ? "not_on_online_store" : !product.countryPublished ? "not_published_in_country" : "not_in_market_catalog" });
      continue;
    }
    const returns = classifyReturnPolicy(product, config.returnPolicy);
    returnCohorts.push({ productId: product.id, variants: product.variants.length, ...returns });
    let content;
    try {
      content = localizedContent(product, config, market);
      content.title = [...content.title].slice(0, 150).join("");
      content.description = [...content.description].slice(0, 5e3).join("");
    } catch (e) {
      errors.push({ productId: product.id, code: e.code || "invalid_product_content" });
      continue;
    }
    for (const variant of product.variants) {
      const id = `shopify_${market.country}_${numericId(product.id, "Product")}_${numericId(variant.id, "ProductVariant")}`;
      try {
        assert2(id.length <= 50, "offer_id_too_long");
        assert2(content.title && content.description, "missing_title_or_description");
        assert2(typeof variant.availableForSale === "boolean", "missing_variant_availability");
        if (!variant.availableForSale) {
          exclusions.push({ productId: product.id, variantId: variant.id, id, variants: 1, code: "variant_not_available_for_sale" });
          continue;
        }
        const image = variant.media?.nodes?.find((n) => n.image?.url)?.image.url || product.featuredMedia?.image?.url;
        const imageUrl = httpsUrl(image, "missing_or_invalid_image").href;
        const explicitAge = enumValue(value(variant, "gAgeGroup"), AGE), derivedAge = deriveVariantAge(variant);
        const parentAge = enumValue(value(product, "gAgeGroup"), AGE);
        const ages = taxonomy(product, "taxonomyAgeGroup").map(taxonomyAge).filter(Boolean);
        let age = explicitAge || derivedAge || parentAge || (ages.length === 1 ? ages[0] : "");
        if (variantAgeConflict(variant, age)) {
          warnings.push({ id, code: "age_group_role_conflict_omitted" });
          age = "";
        }
        const genders = taxonomy(product, "taxonomyGender").map((x) => enumValue(x, GENDER)).filter(Boolean);
        const gender = enumValue(value(variant, "gGender"), GENDER) || deriveVariantGender(variant) || enumValue(value(product, "gGender"), GENDER) || (genders.length === 1 ? genders[0] : "");
        const colors = taxonomy(product, "taxonomyColor");
        const color = value(variant, "gColor") || option(variant, "color") || value(product, "gColor") || (colors.length === 1 ? colors[0] : "");
        const size = value(variant, "gSize") || option(variant, "size") || value(product, "gSize");
        const barcode = String(variant.barcode || "").trim();
        const gtin = validGtin(barcode) ? barcode : "";
        if (barcode && !gtin) warnings.push({ id, code: "invalid_gtin_omitted" });
        const brand = value(variant, "gBrand") || value(product, "gBrand");
        const mpn = value(variant, "gMpn") || value(product, "gMpn");
        const declaredIdentifier = (value(variant, "gIdentifierExists") || value(product, "gIdentifierExists")).toLowerCase();
        let identifier = ["true", "yes"].includes(declaredIdentifier) ? "yes" : ["false", "no"].includes(declaredIdentifier) ? "no" : "";
        if (identifier === "no" && (gtin || mpn || brand)) {
          warnings.push({ id, code: "identifier_declaration_conflict" });
          identifier = "";
        }
        if (!gtin && !mpn && !brand && !identifier) warnings.push({ id, code: "identifier_status_unknown" });
        for (const [field, val] of Object.entries({ age_group: age, gender, color, size })) if (!val) warnings.push({ id, code: `missing_${field}` });
        if (returns.classification === "verified_policy_exception") {
          assert2(returns.label && returns.label.length <= 100 && /^[a-zA-Z0-9_-]+$/.test(returns.label), "missing_or_invalid_return_exception_label");
          exceptionRows++;
        }
        const row = {
          id,
          item_group_id: `shopify_${market.country}_${numericId(product.id, "Product")}`,
          title: content.title,
          description: content.description,
          link: landingLink(product, variant, content, market),
          image_link: imageUrl,
          availability: variant.availableForSale ? "in_stock" : "out_of_stock",
          price: formatPrice(variant.contextualPricing?.price, market),
          condition: enumValue(value(variant, "gCondition") || value(product, "gCondition"), CONDITION),
          brand,
          gtin,
          mpn,
          identifier_exists: identifier,
          age_group: age,
          gender,
          color,
          size,
          return_policy_label: config.returnPolicy?.emitLabels === false ? "" : returns.label,
          excluded_destination: "Shopping_ads"
        };
        assert2(!SUPPLIER.test(JSON.stringify(row)), "supplier_reference_in_output");
        rows.push(row);
      } catch (e) {
        errors.push({ productId: product.id, variantId: variant.id, id, code: e.code || "invalid_variant" });
      }
    }
  }
  const rowIds = rows.map((r) => r.id), previous = new Set(previousIds), current = new Set(rowIds);
  assert2(current.size === rows.length, "duplicate_offer_id");
  const diagnostics = {
    generatedAt: now.toISOString(),
    sourceCompletedAt: snapshot.completedAt,
    market: market.key,
    sourceCounts,
    rows: rows.length,
    outOfStock: rows.filter((r) => r.availability === "out_of_stock").length,
    errors,
    warnings,
    exclusions,
    returnCohorts,
    exceptionRows,
    returnPolicyLabelsEmitted: config.returnPolicy?.emitLabels !== false,
    returnPolicyLabelsConfirmed: config.returnPolicy?.emitLabels === false || exceptionRows === 0 || config.returnPolicy?.nativeLabelConfirmed === true,
    lifecycle: { added: rowIds.filter((id) => !previous.has(id)), removed: previousIds.filter((id) => !current.has(id)), retained: rowIds.filter((id) => previous.has(id)), previousIdsProvided: previousIds.length > 0 },
    limits: ["Shopify buyability is not owned physical inventory.", "Google source must separately target Free listings only.", "Removal requires the next successful primary-file fetch and processing; serving can take 24\u201348 hours.", "No explicit exception identified is not a certification of individual return eligibility."]
  };
  if (errors.length) return { ok: false, diagnostics, tsv: null, rows: [], rowIds: [] };
  const columns = config.returnPolicy?.emitLabels === false ? COLUMNS.filter((c) => c !== "return_policy_label") : COLUMNS;
  if (!materialize) {
    let bytes = 0;
    for (const chunk of tsvChunks(rows, columns)) bytes += chunk.byteLength;
    return { ok: true, tsv: null, rows, rowIds, columns, bytes, diagnostics };
  }
  const tsv = [columns.join("	"), ...rows.map((r) => columns.map((c) => cell(r[c])).join("	"))].join("\n") + "\n";
  return { ok: true, tsv, rows, rowIds, sha256: await sha256(tsv), bytes: new TextEncoder().encode(tsv).byteLength, diagnostics };
}
__name(buildFeed, "buildFeed");

// src/worker.js
var PREFIX = "merchant/";
function runtimeConfig(env) {
  let config;
  try {
    config = JSON.parse(env.MERCHANT_CONFIG_JSON);
  } catch {
    throw new SourceError("feed_config_missing_or_invalid");
  }
  if (!Array.isArray(config.markets) || !config.shopId || !config.storeDomain) throw new SourceError("feed_config_missing_or_invalid");
  return config;
}
__name(runtimeConfig, "runtimeConfig");
async function currentManifest(bucket, marketKey) {
  const object = await bucket.get(`${PREFIX}${marketKey}/current.json`);
  if (!object) return { manifest: null, etag: null };
  let manifest;
  try {
    manifest = JSON.parse(await object.text());
  } catch {
    throw new SourceError("manifest_invalid");
  }
  if (manifest.schemaVersion !== 1 || manifest.market?.key !== marketKey || !/^[a-f0-9]{64}$/.test(manifest.sha256 || "") || !manifest.objectEtag || manifest.objectKey !== `${PREFIX}${marketKey}/${manifest.sha256}.tsv`) throw new SourceError("manifest_invalid");
  return { manifest, etag: object.etag };
}
__name(currentManifest, "currentManifest");
async function commitStoredResult(bucket, stored, result, snapshot, market, before, { publisherJobId = null } = {}) {
  if (!result.ok || !result.diagnostics.returnPolicyLabelsConfirmed) throw new SourceError("feed_not_ready_to_publish");
  if (!stored?.etag) throw new SourceError("feed_object_write_failed");
  const objectKey = `${PREFIX}${market.key}/${result.sha256}.tsv`;
  const manifest = {
    schemaVersion: 1,
    market: { key: market.key, country: market.country, locale: market.locale, currency: market.currency },
    objectKey,
    objectEtag: stored.etag,
    sha256: result.sha256,
    bytes: result.bytes,
    rows: result.rows.length,
    sourceCompletedAt: snapshot.completedAt,
    generatedAt: result.diagnostics.generatedAt,
    sourceParents: result.diagnostics.sourceCounts.parents,
    sourceVariants: result.diagnostics.sourceCounts.variants,
    publisherJobId,
    rowIds: result.rowIds,
    previous: before.manifest ? { objectKey: before.manifest.objectKey, sha256: before.manifest.sha256, sourceCompletedAt: before.manifest.sourceCompletedAt } : null
  };
  const updated = await bucket.put(`${PREFIX}${market.key}/current.json`, JSON.stringify(manifest), {
    httpMetadata: { contentType: "application/json" },
    onlyIf: before.etag ? { etagMatches: before.etag } : { etagDoesNotMatch: "*" }
  });
  if (updated === null) throw new SourceError("concurrent_refresh");
  return manifest;
}
__name(commitStoredResult, "commitStoredResult");

// src/stream-publish.js
var TSV_TYPE2 = "text/tab-separated-values; charset=utf-8";
function hex(buffer) {
  return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}
__name(hex, "hex");
async function publishStreamedResult(bucket, result, snapshot, market, before, {
  publisherJobId,
  randomId = /* @__PURE__ */ __name(() => crypto.randomUUID(), "randomId"),
  digestStream = /* @__PURE__ */ __name(() => new crypto.DigestStream("SHA-256"), "digestStream"),
  fixedLengthStream = /* @__PURE__ */ __name((bytes) => new FixedLengthStream(bytes), "fixedLengthStream")
} = {}) {
  if (!result.ok || !result.diagnostics.returnPolicyLabelsConfirmed) throw new SourceError("feed_not_ready_to_publish");
  if (!Number.isSafeInteger(result.bytes) || result.bytes < 1 || result.bytes > 6e7 || !Array.isArray(result.columns)) throw new SourceError("feed_stream_size_invalid");
  const stageKey = `merchant/jobs/${market.key}/${publisherJobId || randomId()}/stage-${randomId()}.tsv`;
  const fixed = fixedLengthStream(result.bytes), digest = digestStream();
  const writer = fixed.writable.getWriter(), hashWriter = digest.getWriter();
  const upload = bucket.put(stageKey, fixed.readable, { httpMetadata: { contentType: TSV_TYPE2 } });
  upload.catch(() => {
  });
  digest.digest.catch(() => {
  });
  try {
    for (const chunk of tsvChunks(result.rows, result.columns)) {
      await writer.write(chunk);
      await hashWriter.write(chunk);
    }
    await writer.close();
    await hashWriter.close();
    const staged = await upload, sha2562 = hex(await digest.digest);
    const source = await bucket.get(stageKey);
    if (!staged?.etag || !source || source.etag !== staged.etag || source.size !== result.bytes) throw new SourceError("staged_feed_invalid");
    const objectKey = `merchant/${market.key}/${sha2562}.tsv`;
    const stored = await bucket.put(objectKey, source.body, { sha256: sha2562, httpMetadata: { contentType: TSV_TYPE2 } });
    return await commitStoredResult(bucket, stored, { ...result, sha256: sha2562 }, snapshot, market, before, { publisherJobId });
  } catch (error) {
    await Promise.allSettled([writer.abort(), hashWriter.abort(), upload]);
    throw error instanceof SourceError ? error : new SourceError("feed_stream_failed");
  } finally {
    if (typeof bucket.delete === "function") await bucket.delete(stageKey).catch(() => {
    });
  }
}
__name(publishStreamedResult, "publishStreamedResult");

// src/checkpoint.js
var CheckpointNeeded = class extends Error {
  static {
    __name(this, "CheckpointNeeded");
  }
};
var keyPattern = /^[a-z]{2}-[a-z]{2}(?:-[a-z]{2})?$/;
var idPattern = /^[a-f0-9-]{36}$/;
var supplierPattern = /(?:alibaba\.com|aliexpress\.com|1688\.com|taobao\.com|tmall\.com)/i;
function requireValue(value2, code) {
  if (!value2) throw new SourceError(code);
}
__name(requireValue, "requireValue");
function jobKey(key) {
  return `merchant/${key}/refresh.json`;
}
__name(jobKey, "jobKey");
function body(control) {
  return { schemaVersion: 1, key: control.key, jobId: control.jobId, revision: control.revision };
}
__name(body, "body");
async function discardJournal(bucket, control) {
  if (typeof bucket.delete === "function" && control?.journalKey?.startsWith(`merchant/jobs/${control.key}/${control.jobId}/`)) await bucket.delete(control.journalKey).catch(() => {
  });
}
__name(discardJournal, "discardJournal");
async function readControl(bucket, key) {
  const object = await bucket.get(jobKey(key));
  if (!object) return { control: null, etag: null };
  let control;
  try {
    control = JSON.parse(await object.text());
  } catch {
    throw new SourceError("refresh_control_invalid");
  }
  requireValue(control.schemaVersion === 1 && control.key === key && idPattern.test(control.jobId) && Number.isSafeInteger(control.revision), "refresh_control_invalid");
  return { control, etag: object.etag };
}
__name(readControl, "readControl");
function configured(env, key) {
  const config = runtimeConfig(env), market = config.markets.find((m) => m.key === key && m.enabled);
  requireValue(keyPattern.test(key) && market, "market_not_enabled");
  requireValue(env.MERCHANT_FEED_BUCKET && env.MERCHANT_REFRESH_QUEUE, "refresh_bindings_missing");
  return { config, market, bucket: env.MERCHANT_FEED_BUCKET, queue: env.MERCHANT_REFRESH_QUEUE };
}
__name(configured, "configured");
async function writeControl(bucket, control, beforeEtag) {
  const stored = await bucket.put(jobKey(control.key), JSON.stringify(control), {
    onlyIf: beforeEtag ? { etagMatches: beforeEtag } : { etagDoesNotMatch: "*" },
    httpMetadata: { contentType: "application/json" }
  });
  requireValue(stored !== null, "concurrent_refresh_checkpoint");
  return stored;
}
__name(writeControl, "writeControl");
async function enqueueRefresh(env, key, { now = /* @__PURE__ */ __name(() => /* @__PURE__ */ new Date(), "now"), randomId = /* @__PURE__ */ __name(() => crypto.randomUUID(), "randomId") } = {}) {
  const { config, bucket, queue } = configured(env, key);
  const hash = await sha256(JSON.stringify(config)), before = await readControl(bucket, key);
  const time = now(), old = before.control;
  const maxAge = (config.refresh?.maxJobAgeMinutes ?? 120) * 6e4;
  if (old?.status === "RUNNING" && old.configHash === hash && time - Date.parse(old.startedAt) <= maxAge) {
    await queue.send(body(old));
    return { resumed: true, jobId: old.jobId };
  }
  if (old?.status === "COMPLETE" && old.configHash === hash && time - Date.parse(old.completedAt) < (config.refresh?.minRefreshMinutes ?? 60) * 6e4) return { skipped: "recent_complete_refresh" };
  const control = {
    schemaVersion: 1,
    key,
    jobId: randomId(),
    revision: 0,
    status: "RUNNING",
    startedAt: time.toISOString(),
    updatedAt: time.toISOString(),
    configHash: hash,
    journalKey: null
  };
  requireValue(idPattern.test(control.jobId), "refresh_job_id_invalid");
  await writeControl(bucket, control, before.etag);
  await queue.send(body(control));
  await discardJournal(bucket, old);
  return { started: true, jobId: control.jobId };
}
__name(enqueueRefresh, "enqueueRefresh");
function sanitize(data) {
  for (const p of data.products?.nodes || []) if (Array.isArray(p.tags)) p.tags = p.tags.filter((tag) => !/https?:\/\//i.test(tag));
  requireValue(!supplierPattern.test(JSON.stringify(data)), "supplier_reference_in_source");
  return data;
}
__name(sanitize, "sanitize");
async function consumeRefresh(env, message, { graphql, now = /* @__PURE__ */ __name(() => /* @__PURE__ */ new Date(), "now"), randomId = /* @__PURE__ */ __name(() => crypto.randomUUID(), "randomId"), streamOptions = {} } = {}) {
  requireValue(message?.schemaVersion === 1 && keyPattern.test(message.key || "") && idPattern.test(message.jobId || "") && Number.isSafeInteger(message.revision) && message.revision >= 0, "refresh_message_invalid");
  const { config, market, bucket, queue } = configured(env, message.key);
  const before = await readControl(bucket, message.key), control = before.control;
  if (!control || control.jobId !== message.jobId || control.status !== "RUNNING") return { ignored: "superseded_or_complete_message" };
  if (message.revision < control.revision) {
    await queue.send(body(control));
    return { resumed: "latest_checkpoint_requeued" };
  }
  requireValue(message.revision === control.revision, "future_refresh_message");
  const maxAge = (config.refresh?.maxJobAgeMinutes ?? 120) * 6e4;
  const fail = /* @__PURE__ */ __name(async (code) => {
    const failed = { ...control, status: "FAILED", failedAt: now().toISOString(), code };
    await writeControl(bucket, failed, before.etag);
    await bucket.put(`merchant/${market.key}/status.json`, JSON.stringify({ ok: false, failedAt: failed.failedAt, jobId: control.jobId, code }));
    return { failed: true, code };
  }, "fail");
  if (control.configHash !== await sha256(JSON.stringify(config))) return fail("refresh_config_changed");
  if (now() - Date.parse(control.startedAt) > maxAge) return fail("refresh_expired");
  const maxCalls = config.refresh?.maxSourceCallsPerInvocation ?? 20;
  requireValue(Number.isSafeInteger(maxCalls) && maxCalls >= 1 && maxCalls <= 20, "unsafe_refresh_call_budget");
  let journal = { schemaVersion: 1, jobId: control.jobId, entries: [], beforeFeed: null };
  if (control.journalKey) {
    requireValue(control.journalKey.startsWith(`merchant/jobs/${market.key}/${control.jobId}/`), "refresh_journal_key_invalid");
    const object = await bucket.get(control.journalKey);
    requireValue(object && object.size <= 5e7, "refresh_journal_missing_or_oversize");
    journal = JSON.parse(await object.text());
    requireValue(journal.schemaVersion === 1 && journal.jobId === control.jobId && Array.isArray(journal.entries) && journal.entries.length <= 1e4, "refresh_journal_invalid");
  } else journal.beforeFeed = await currentManifest(bucket, market.key);
  const present = await currentManifest(bucket, market.key);
  if (present.manifest?.publisherJobId === control.jobId) {
    await writeControl(bucket, { ...control, status: "COMPLETE", completedAt: present.manifest.generatedAt, sha256: present.manifest.sha256, rows: present.manifest.rows }, before.etag);
    await discardJournal(bucket, control);
    return { complete: true, recoveredPromotion: true, rows: present.manifest.rows };
  }
  let index = 0, newCalls = 0, firstClock = true;
  const reader = graphql || createAdminReader({ domain: config.storeDomain, token: env.SHOPIFY_ADMIN_ACCESS_TOKEN, apiVersion: config.apiVersion });
  const replayReader = /* @__PURE__ */ __name(async (query, variables) => {
    const key = await sha256(query + "\n" + JSON.stringify(variables));
    if (index < journal.entries.length) {
      const saved = journal.entries[index++];
      requireValue(saved.key === key, "refresh_replay_mismatch");
      return structuredClone(saved.data);
    }
    if (newCalls >= maxCalls) throw new CheckpointNeeded();
    newCalls++;
    const data = sanitize(await reader(query, variables));
    journal.entries.push({ key, data });
    index++;
    requireValue(journal.entries.length <= 1e4, "refresh_request_limit");
    return structuredClone(data);
  }, "replayReader");
  let snapshot;
  try {
    snapshot = await collectCatalog(replayReader, config, market, { now: /* @__PURE__ */ __name(() => {
      if (firstClock) {
        firstClock = false;
        return new Date(control.startedAt);
      }
      return now();
    }, "now") });
  } catch (error) {
    if (!(error instanceof CheckpointNeeded)) return fail(error instanceof SourceError ? error.code : "refresh_source_failed");
    const journalKey = `merchant/jobs/${market.key}/${control.jobId}/${control.revision + 1}-${randomId()}.json`;
    const serialized = JSON.stringify(journal);
    requireValue(new TextEncoder().encode(serialized).byteLength <= 5e7, "refresh_journal_oversize");
    await bucket.put(journalKey, serialized, { httpMetadata: { contentType: "application/json" } });
    const next = { ...control, revision: control.revision + 1, journalKey, updatedAt: now().toISOString(), sourceRequests: journal.entries.length };
    await writeControl(bucket, next, before.etag);
    await queue.send(body(next));
    await discardJournal(bucket, control);
    return { checkpointed: true, revision: next.revision, newCalls, sourceRequests: journal.entries.length };
  }
  let result;
  try {
    result = await buildFeed(snapshot, config, market, { now: now(), previousIds: journal.beforeFeed.manifest?.rowIds || [], materialize: false });
  } catch (error) {
    return fail(error instanceof SourceError ? error.code : "refresh_build_failed");
  }
  const diagnosticsKey = `merchant/${market.key}/diagnostics/${control.jobId}.json`;
  await bucket.put(diagnosticsKey, JSON.stringify(result.diagnostics), { httpMetadata: { contentType: "application/json" } });
  if (!result.ok) return fail("feed_validation_failed");
  let manifest;
  try {
    manifest = await publishStreamedResult(bucket, result, snapshot, market, journal.beforeFeed, { ...streamOptions, publisherJobId: control.jobId });
  } catch (error) {
    return fail(error instanceof SourceError ? error.code : "refresh_publish_failed");
  }
  const completed = { ...control, status: "COMPLETE", completedAt: now().toISOString(), sha256: manifest.sha256, rows: manifest.rows, sourceRequests: journal.entries.length };
  await writeControl(bucket, completed, before.etag);
  await bucket.put(`merchant/${market.key}/status.json`, JSON.stringify({ ok: true, completedAt: completed.completedAt, jobId: control.jobId, sha256: manifest.sha256, rows: manifest.rows, sourceParents: manifest.sourceParents, sourceVariants: manifest.sourceVariants, requests: journal.entries.length, diagnosticsKey }));
  await discardJournal(bucket, control);
  return { complete: true, rows: manifest.rows, newCalls, sourceRequests: journal.entries.length, sha256: manifest.sha256 };
}
__name(consumeRefresh, "consumeRefresh");

// src/automation.js
var automation_default = {
  fetch: host_default.fetch,
  async scheduled(controller, env) {
    const config = runtimeConfig(env);
    const key = config.schedules?.[controller.cron] || (controller.cron === "0 * * * *" ? "us-en" : null);
    if (key && config.markets.some((m) => m.key === key && m.enabled)) await enqueueRefresh(env, key);
  },
  async queue(batch, env) {
    if (batch.messages.length !== 1) {
      for (const message of batch.messages) message.retry({ delaySeconds: 60 });
      return;
    }
    for (const message of batch.messages) {
      try {
        await consumeRefresh(env, message.body);
        message.ack();
      } catch {
        message.retry({ delaySeconds: 60 });
      }
    }
  }
};
export {
  automation_default as default
};
//# sourceMappingURL=automation.js.map
