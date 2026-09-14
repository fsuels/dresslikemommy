import { manifestRows } from '../src/collector.js';

export const config = {
  shopId: 'gid://shopify/Shop/15571635', storeDomain: 'dresslikemommy-com.myshopify.com',
  apiVersion: '2026-07', onlinePublicationId: 'gid://shopify/Publication/55169925',
  sourceLocale: 'en', maxSnapshotAgeHours: 24, maxFeedAgeHours: 48,
  returnPolicy: { exceptionLabel: 'no_returns', nativeLabelConfirmed: true,
    productTypes: ['swimwear', 'intimates'], taxonomyNames: ['Swimwear', 'Underwear', 'Lingerie'], finalSaleTags: ['Final Sale'] },
  markets: [{ key: 'us-en', country: 'US', locale: 'en', currency: 'USD', minorUnits: 2,
    landingBaseUrl: 'https://www.dresslikemommy.com', landingContextVerified: true, landingQuery: {}, enabled: true }],
};
export const market = config.markets[0];
export const now = new Date('2026-09-11T14:00:00Z');
export const count = count => ({ count, precision: 'EXACT' });
export function variant(id = 101, currency = 'USD') {
  return { id: `gid://shopify/ProductVariant/${id}`, availableForSale: true, barcode: null,
    selectedOptions: [{ name: 'Size', value: 'Mother S' }, { name: 'Color', value: 'Blue' }],
    contextualPricing: { price: { amount: '21.9', currencyCode: currency } },
    media: { nodes: [{ image: { url: 'https://cdn.shopify.com/fixture.png' } }] } };
}
export function product(id = 1, variants = [variant(id * 100 + 1)]) {
  return { id: `gid://shopify/Product/${id}`, status: 'ACTIVE', updatedAt: '2026-09-11T13:00:00Z',
    handle: `matching-outfit-${id}`, title: 'Matching blue outfit', description: 'Two-piece blue outfit.',
    productType: 'Dresses', tags: [], isGiftCard: false,
    onlineStoreUrl: `https://www.dresslikemommy.com/products/matching-outfit-${id}`,
    onlinePublished: true, countryPublished: true, variantsCount: count(variants.length), variants,
    featuredMedia: { image: { url: 'https://cdn.shopify.com/parent.png' } }, translations: [],
    category: { fullName: 'Apparel & Accessories > Clothing > Dresses' } };
}
export function snapshot(products = [product()], target = market) {
  return { schemaVersion: 1, paginationComplete: true, startedAt: now.toISOString(), completedAt: now.toISOString(),
    shop: { id: config.shopId, name: 'Fixture shop', currencyCode: 'USD', primaryDomain: { url: market.landingBaseUrl } },
    sourceLocale: 'en', market: { key: target.key, country: target.country, locale: target.locale, currency: target.currency, marketId: target.marketId ?? null },
    onlinePublicationId: config.onlinePublicationId, activeCount: count(products.length), finalActiveCount: count(products.length),
    products, finalManifest: manifestRows(products), trace: [] };
}
export function source(products, { productPageSize = 25, variantPageSize = 40, manifestPageSize = 50, intercept } = {}) {
  let calls = 0;
  const connection = (items, after, size) => {
    const start = after ? Number(after) : 0, nodes = items.slice(start, start + size), end = start + nodes.length;
    return { nodes: structuredClone(nodes), pageInfo: { hasNextPage: end < items.length, endCursor: String(end) } };
  };
  const graphql = async (query, variables) => {
    calls++;
    let result;
    if (query.includes('query MerchantFeedIdentity')) result = { shop: snapshot().shop, shopLocales: [{ locale: 'en', primary: true, published: true }, { locale: 'fr', primary: false, published: true }], activeCount: count(products.length) };
    else if (query.includes('query MerchantFeedProducts')) result = { products: connection(products.map(({ variants, ...p }) => p), variables.after, productPageSize) };
    else if (query.includes('query MerchantFeedVariants')) {
      const p = products.find(p => p.id === variables.id);
      result = { product: { id: p.id, status: p.status, updatedAt: p.updatedAt, variantsCount: p.variantsCount, variants: connection(p.variants, variables.after, variantPageSize) } };
    } else if (query.includes('query MerchantFeedManifest')) result = { products: connection(manifestRows(products), variables.after, manifestPageSize) };
    else throw new Error('unexpected_fixture_query');
    return intercept ? (intercept(result, query, variables, calls) || result) : result;
  };
  return { graphql, calls: () => calls };
}
export class Bucket {
  objects = new Map(); writes = []; rejectPointer = false;
  async get(key) {
    const item = this.objects.get(key);
    return item ? { etag: item.etag, size: new TextEncoder().encode(item.text).length,
      body: new Response(item.text).body, text: async () => item.text } : null;
  }
  async put(key, text, options = {}) {
    const before = this.objects.get(key);
    if (options.onlyIf?.etagMatches && options.onlyIf.etagMatches !== before?.etag) return null;
    if (options.onlyIf?.etagDoesNotMatch === '*' && before) return null;
    if (this.rejectPointer && key.endsWith('/current.json')) return null;
    this.writes.push(key); const etag = `fixture-etag-${this.writes.length}`;
    this.objects.set(key, { text, etag }); return { etag };
  }
}
