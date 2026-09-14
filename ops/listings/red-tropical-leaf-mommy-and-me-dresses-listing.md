# Red Tropical Leaf Mommy and Me Dresses

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7607762845793
- **Live:** https://www.dresslikemommy.com/products/red-tropical-leaf-mommy-and-me-dresses
- **Product GID:** `gid://shopify/Product/7607762845793`
- **Handle:** `red-tropical-leaf-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | redacted per project source-URL policy |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me (resolved from mother + girl evidence) |
| PRIMARY_CATEGORY | Dresses |
| DESIGNS_TO_LIST | Red tropical leaf dress |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | RTLF |
| COLOR_TOKEN | RED |

## Source Fetch Status
Direct supplier-page proof was not used for customer-facing data; the attached product, size-chart, and selector screenshots are the authoritative evidence for this active-product correction.

## Source Measurement Notes
The attached chart publishes bust/chest, waist, shoulder, and garment length. Hip values were derived from the prompt rules because the chart does not publish hip measurements.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Red Tropical Leaf Mommy and Me Dresses` | 38 |
| SEO title | `Red Mommy and Me Dresses | Dress Like Mommy` | 43 |
| SEO description | `Red leaf-print mommy-and-me beach dresses for mom + daughter. Size rows cover Child 4Y-12Y and Mother S-2XL.` | 108 |

## SIZE_CHART / Variant Recap
| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Girl Dress | 110 | Child 4 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID4Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID5Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID67Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID8Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID910Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Dress | 160 | Child 12 Years | Red Tropical Leaf | `DLM-RTLF-GRL-KID12Y-RED` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Dress | S | Mother S | Red Tropical Leaf | `DLM-RTLF-MOM-S-RED` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Red Tropical Leaf | `DLM-RTLF-MOM-M-RED` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Red Tropical Leaf | `DLM-RTLF-MOM-L-RED` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL1 | Mother XL | Red Tropical Leaf | `DLM-RTLF-MOM-XL-RED` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Dress | XXL1 | Mother 2XL | Red Tropical Leaf | `DLM-RTLF-MOM-2XL-RED` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975156833` (2XL) |

## Derivations
- Request resolved to Mommy and Me because the supplied product image shows mother + girl and no father/boy rows were evidenced.
- Primary category resolved to Dresses from the garment evidence and Shopify taxonomy guard.
- Product options are `Size` and `Color`; Red Tropical Leaf is a single color value, so variant count equals the 11 selector-backed rows.
- Child rows map 110-160 to Child 4 Years through Child 12 Years. Adult rows map S/M/L/XL1/XXL1 to Mother S/M/L/XL/2XL.
- Child hip values use `chest + 4`; mother hip values use `bust + 6`. Waist and dress length are source values for S-L and estimated for 160cm, XL1, and XXL1.
- Pricing uses nearby active Mommy-and-Me dress products: child `31.99`, mother `34.99`; Cost per item is exactly 50 percent.

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status | PASS | ACTIVE |
| Publication check | PASS | publishedAt=2026-06-29T15:59:41Z; onlineStoreUrl=https://www.dresslikemommy.com/products/red-tropical-leaf-mommy-and-me-dresses; preserved live channels=['Google & YouTube', 'Facebook & Instagram', 'Online Store', 'Pinterest', 'Microsoft Channel', 'TikTok', 'Buy Button', 'Point of Sale', 'n8n Integration'] |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Dresses |
| Variant count matches SIZE_CHART x colors | PASS | 11 vs 11 |
| Price and cost parity | PASS | 11 variants checked |
| Source-token leak check | PASS | No source marketplace token or offer ID in Shopify product data or local artifacts |

## Localized Size-Chart Gate
| Command | Result |
|---|---|
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/poll_shopify_product_translations.py --handles red-tropical-leaf-mommy-and-me-dresses --execute --force-refresh` | PASS: `candidate_products=1`, `processed_products=1`, `blocked_by_error=false` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles red-tropical-leaf-mommy-and-me-dresses --execute` | PASS: `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles red-tropical-leaf-mommy-and-me-dresses --fail-on-missing` | PASS: `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles red-tropical-leaf-mommy-and-me-dresses --fail-on-unmatched` | PASS: `unmatched_variant_locale_count=0` |

## Price Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-RTLF-GRL-KID4Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-GRL-KID5Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-GRL-KID67Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-GRL-KID8Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-GRL-KID910Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-MOM-S-RED` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-RTLF-MOM-M-RED` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-RTLF-MOM-L-RED` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-RTLF-GRL-KID12Y-RED` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RTLF-MOM-XL-RED` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-RTLF-MOM-2XL-RED` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |

## Metafields Written
- `custom.category1`
- `custom.pattern`
- `custom.style`
- `custom.subcategory`
- `custom.subcategory2`
- `custom.type`
- `global.description_tag`
- `global.title_tag`
- `mm-google-shopping.age_group`
- `mm-google-shopping.condition`
- `mm-google-shopping.custom_label_0`
- `mm-google-shopping.custom_label_1`
- `mm-google-shopping.custom_label_2`
- `mm-google-shopping.custom_label_3`
- `mm-google-shopping.custom_label_4`
- `mm-google-shopping.custom_product`
- `mm-google-shopping.gender`
- `shopify.age-group`
- `shopify.color-pattern`
- `shopify.dress-occasion`
- `shopify.size`
- `shopify.target-gender`

## Metafields Skipped
- `shopify.fabric`: Exact fiber was not visible from the supplied evidence.
- `shopify.dress-style`: No exact catalog GID was selected for this beach wrap-dress style.
- `shopify.dress-occasion`: No exact catalog GID was selected for a broad vacation/photo use case.
- `shopify.skirt-dress-length-type`: Source chart provides garment length but no standardized dress-length type.
- `shopify.sleeve-length-type`: Halter/sleeveless styling is visible, but no exact trusted metaobject was selected in this run.
- `shopify.neckline`: Halter styling is visible, but no exact trusted neckline metaobject was selected in this run.
- `shopify.top-length-type`: Product taxonomy is Dresses, not Tops.

## Tags Written
Beach Dress, Child 12yr, Child 4yr, Child 5yr, Child 6-7yr, Child 8yr, Child 9-10yr, Dresses, Girl Dress, Matching Family Dresses, Matching Mommy and Me Dresses, Mom Size 2XL, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Daughter Matching Set, Mother Dress, Photo Ready, Red, Red Tropical Leaf, Resort Dress, Summer, Tropical Leaf, Vacation, Wrap Dress

## Smart Collections
Product is active; live collection/channel indexing may still need normal platform propagation after the variant/body update.

## Manual Follow-ups
1. Review the active product image, red tropical print naming, and newly estimated size rows in Shopify Admin.
2. If exact fiber composition becomes available, add the fabric metafield.
3. If a true hip or XL/2XL chart becomes available, replace derived/estimated values.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-rtlf-red-tropical-leaf-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-tropical-leaf-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-tropical-leaf-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-red-tropical-leaf-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-red-tropical-leaf-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-red-tropical-leaf-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/red-tropical-leaf-mommy-and-me-dresses`
