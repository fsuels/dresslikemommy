# Ocean Bloom Mommy and Me Dresses - Beach Chiffon

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7607760388193
- **Live:** not published
- **Product GID:** `gid://shopify/Product/7607760388193`
- **Handle:** `ocean-bloom-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | redacted per project source-URL policy |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me (resolved from mother + girl evidence) |
| PRIMARY_CATEGORY | Dresses |
| DESIGNS_TO_LIST | Ocean blue floral dress |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | OBLM |
| COLOR_TOKEN | BLUE |

## Source Fetch Status
Direct supplier-page proof was not usable through the web readback; the attached product and size-chart screenshots are the authoritative evidence for this draft.

## Source Measurement Notes
The attached chart publishes shoulder, bust, waist, dress length, and sleeve length. Hip values were derived from the prompt rules because the chart does not publish hip measurements.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Ocean Bloom Mommy and Me Dresses - Beach Chiffon` | 48 |
| SEO title | `Blue Floral Mommy and Me Dresses | Dress Like Mommy` | 51 |
| SEO description | `Airy blue floral chiffon-style mommy-and-me dresses for mom + daughter. Size rows cover Child 4Y-9-10Y and Mother S-XL.` | 119 |

## SIZE_CHART / Variant Recap
| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Girl Dress | 110 | Child 4 Years | Ocean Blue Floral | `DLM-OBLM-GRL-KID4Y-BLUE` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Ocean Blue Floral | `DLM-OBLM-GRL-KID5Y-BLUE` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Ocean Blue Floral | `DLM-OBLM-GRL-KID67Y-BLUE` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Ocean Blue Floral | `DLM-OBLM-GRL-KID8Y-BLUE` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Ocean Blue Floral | `DLM-OBLM-GRL-KID910Y-BLUE` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Ocean Blue Floral | `DLM-OBLM-MOM-S-BLUE` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Ocean Blue Floral | `DLM-OBLM-MOM-M-BLUE` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Ocean Blue Floral | `DLM-OBLM-MOM-L-BLUE` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | Ocean Blue Floral | `DLM-OBLM-MOM-XL-BLUE` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |

## Derivations
- Request resolved to Mommy and Me because the supplied product image shows mother + girl and no father/boy rows were evidenced.
- Primary category resolved to Dresses from the garment evidence and Shopify taxonomy guard.
- Product options are `Size` and `Color`; Ocean Blue Floral is a single color value, so variant count equals the 9 chart rows.
- Child rows map 110-150 to Child 4 Years through Child 9-10 Years. Adult rows map S/M/L/XL to Mother S/M/L/XL.
- Child hip values use `chest + 4`; mother hip values use `bust + 6`. Waist and dress length are source values.
- Pricing uses nearby active Mommy-and-Me dress products: child `31.99`, mother `34.99`; Cost per item is exactly 50 percent.

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status | PASS | DRAFT |
| Publication check | PASS | publishedAt=None; onlineStoreUrl=None; live channels=[] |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Dresses |
| Variant count matches SIZE_CHART x colors | PASS | 9 vs 9 |
| Price and cost parity | PASS | 9 variants checked |
| Source-token leak check | PASS | No source marketplace token or offer ID in Shopify product data or local artifacts |

## Localized Size-Chart Gate
| Command | Result |
|---|---|
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/poll_shopify_product_translations.py --handles ocean-bloom-mommy-and-me-dresses --execute --force-refresh` | PASS; `candidate_products=1`, `processed_products=0`, `blocked_by_error=false` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles ocean-bloom-mommy-and-me-dresses --execute` | PASS; registered `20` localized body translations with `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles ocean-bloom-mommy-and-me-dresses --fail-on-missing` | PASS; `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles ocean-bloom-mommy-and-me-dresses --fail-on-unmatched` | PASS; `products_with_unmatched_variants=0`, `unmatched_variant_locale_count=0`; because the product is a draft, `variant_locale_checks=0` |

## Price Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-OBLM-GRL-KID4Y-BLUE` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-OBLM-GRL-KID5Y-BLUE` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-OBLM-GRL-KID67Y-BLUE` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-OBLM-GRL-KID8Y-BLUE` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-OBLM-GRL-KID910Y-BLUE` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-OBLM-MOM-S-BLUE` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-OBLM-MOM-M-BLUE` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-OBLM-MOM-L-BLUE` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-OBLM-MOM-XL-BLUE` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |

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
- `shopify.size`
- `shopify.target-gender`

## Metafields Skipped
- `shopify.fabric`: Exact fiber was not visible from the supplied evidence.
- `shopify.dress-style`: No exact catalog GID was selected for this airy beach-dress style.
- `shopify.dress-occasion`: No exact catalog GID was selected for a broad vacation/photo use case.
- `shopify.skirt-dress-length-type`: Source chart provides dress length but no standardized dress-length type was selected.
- `shopify.sleeve-length-type`: Short sleeves are visible, but no exact trusted sleeve-length metaobject was selected in this run.
- `shopify.neckline`: V-neck styling is visible, but no exact trusted neckline metaobject was selected in this run.
- `shopify.top-length-type`: Product taxonomy is Dresses, not Tops.

## Tags Written
Aqua, Beach Dress, Black Floral, Blue Floral, Chiffon Dress, Child 4yr, Child 5yr, Child 6-7yr, Child 8yr, Child 9-10yr, Dresses, Floral, Girl Dress, Matching Family Dresses, Matching Mommy and Me Dresses, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Daughter Matching Set, Mother Dress, Ocean Blue, Photo Ready, Summer, Vacation

## Smart Collections
Product is a draft; collection indexing may wait until publication.

## Manual Follow-ups
1. Review the draft image and Ocean Blue Floral color naming in Shopify Admin before any separate publish-live request.
2. If exact fiber composition becomes available, add the fabric metafield before publishing.
3. If a true hip chart becomes available, replace derived hip values before publishing.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-oblm-ocean-bloom-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ocean-bloom-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ocean-bloom-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-ocean-bloom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-ocean-bloom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-ocean-bloom-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/ocean-bloom-mommy-and-me-dresses`
