# Product Metadata Backfill Summary

Input file: `products_export_1 2.csv`
Output file: `products_export_1 2_working_backfill.csv`
Target products: `588` active handles

## Product-level coverage (active products)

| Field | Before | After |
|---|---:|---:|
| SEO Title | 1/588 (0.2%) | 588/588 (100.0%) |
| SEO Description | 374/588 (63.6%) | 588/588 (100.0%) |
| Google Shopping / Google Product Category | 0/588 (0.0%) | 588/588 (100.0%) |
| Category1 (product.metafields.custom.category1) | 339/588 (57.7%) | 588/588 (100.0%) |
| SubCategory (product.metafields.custom.subcategory) | 339/588 (57.7%) | 588/588 (100.0%) |
| SubCategory2 (product.metafields.custom.subcategory2) | 57/588 (9.7%) | 588/588 (100.0%) |
| Type (product.metafields.custom.type) | 1/588 (0.2%) | 588/588 (100.0%) |
| Style (product.metafields.custom.style) | 1/588 (0.2%) | 588/588 (100.0%) |
| Pattern (product.metafields.custom.pattern) | 1/588 (0.2%) | 588/588 (100.0%) |
| Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products) | 0/588 (0.0%) | 588/588 (100.0%) |
| Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display) | 0/588 (0.0%) | 588/588 (100.0%) |
| Related products (product.metafields.shopify--discovery--product_recommendation.related_products) | 0/588 (0.0%) | 588/588 (100.0%) |
| Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries) | 0/588 (0.0%) | 588/588 (100.0%) |

## Variant-level coverage (active products)

| Field | Before | After |
|---|---:|---:|
| Variant Barcode | 1649/13990 (11.8%) | 1649/13990 (11.8%) |
| Google Shopping / MPN | 0/13990 (0.0%) | 12060/13990 (86.2%) |
| Google Shopping / Custom Product | 0/13990 (0.0%) | 13990/13990 (100.0%) |
| Google: Custom Product (product.metafields.mm-google-shopping.custom_product) | 0/13990 (0.0%) | 13990/13990 (100.0%) |
| Image Alt Text | 2552/13990 (18.2%) | 3015/13990 (21.6%) |

## Notes

- Active handles were normalized to controlled taxonomy values for Category1/SubCategory/SubCategory2/Type/Style/Pattern.
- Missing GTINs were not fabricated. Rows without barcode are marked custom product and receive MPN from SKU when available.
- Complementary/related/search boost fields are generated from taxonomy similarity and title keywords for immediate Search & Discovery seeding.
