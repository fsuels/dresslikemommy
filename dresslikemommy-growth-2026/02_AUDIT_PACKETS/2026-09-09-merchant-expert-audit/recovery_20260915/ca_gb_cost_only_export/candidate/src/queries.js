// Read-only Shopify Admin 2026-07 operations. Both connections are fully paginated.
export const IDENTITY_QUERY = `query MerchantFeedIdentity {
  shop { id name currencyCode primaryDomain { url } }
  shopLocales { locale primary published }
  activeCount: productsCount(query: "status:active", limit: null) { count precision }
}`;

const ATTRIBUTES = `
  gAgeGroup: metafield(namespace: "mm-google-shopping", key: "age_group") { value }
  gGender: metafield(namespace: "mm-google-shopping", key: "gender") { value }
  gColor: metafield(namespace: "mm-google-shopping", key: "color") { value }
  gSize: metafield(namespace: "mm-google-shopping", key: "size") { value }
  gBrand: metafield(namespace: "mm-google-shopping", key: "brand") { value }
  gMpn: metafield(namespace: "mm-google-shopping", key: "mpn") { value }
  gCondition: metafield(namespace: "mm-google-shopping", key: "condition") { value }
  gIdentifierExists: metafield(namespace: "mm-google-shopping", key: "identifier_exists") { value }
`;

export const MARKET_CONTEXT_QUERY = `query MerchantFeedMarketContext($country: CountryCode!, $after: String) {
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

export const PRODUCTS_QUERY = `query MerchantFeedProducts(
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

export const VARIANTS_QUERY = `query MerchantFeedVariants($id: ID!, $after: String, $country: CountryCode!) {
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

export const MANIFEST_QUERY = `query MerchantFeedManifest($after: String, $country: CountryCode!, $onlinePublicationId: ID!, $catalogPublicationId: ID!, $verifyCatalog: Boolean!) {
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
