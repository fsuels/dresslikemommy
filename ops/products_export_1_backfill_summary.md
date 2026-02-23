# Product Metadata Backfill Summary

Input file: `GPT/products_export_1.csv`
Output file: `GPT/products_export_1_backfill.csv`

## Product-level coverage

| Field | Before | After |
|---|---:|---:|
| SEO Title | 0/660 (0.0%) | 660/660 (100.0%) |
| Google Shopping / Google Product Category | 0/660 (0.0%) | 660/660 (100.0%) |
| Category1 (product.metafields.custom.category1) | 405/660 (61.4%) | 660/660 (100.0%) |
| SubCategory (product.metafields.custom.subcategory) | 405/660 (61.4%) | 660/660 (100.0%) |
| Pattern (product.metafields.custom.pattern) | 0/660 (0.0%) | 660/660 (100.0%) |
| Style (product.metafields.custom.style) | 0/660 (0.0%) | 660/660 (100.0%) |
| Type (product.metafields.custom.type) | 0/660 (0.0%) | 660/660 (100.0%) |
| Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products) | 0/660 (0.0%) | 660/660 (100.0%) |
| Related products (product.metafields.shopify--discovery--product_recommendation.related_products) | 0/660 (0.0%) | 660/660 (100.0%) |
| Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries) | 0/660 (0.0%) | 660/660 (100.0%) |

## Variant-level coverage

| Field | Before | After |
|---|---:|---:|
| Variant Barcode | 1694/16813 (10.1%) | 1694/16813 (10.1%) |
| Google Shopping / MPN | 0/16813 (0.0%) | 11057/16813 (65.8%) |

## Notes

- Missing GTINs were not fabricated. Rows missing `Variant Barcode` get `Google Shopping / Custom Product=TRUE` and MPN from SKU when available.
- Complementary/related handles are inferred from category/subcategory similarity; review before importing.
- Search boost queries are inferred from taxonomy + title keywords; tune in Search & Discovery after import.
