# Green Botanical Ruffle Mommy and Me Dresses

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7607760257121
- **Live:** not published
- **Product GID:** `gid://shopify/Product/7607760257121`
- **Handle:** `green-botanical-ruffle-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | redacted per project source-URL policy |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me (resolved from mother + girl evidence) |
| PRIMARY_CATEGORY | Dresses |
| DESIGNS_TO_LIST | Green botanical ruffle dress |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | GBRF |
| COLOR_TOKEN | GREEN |

## Source Fetch Status
Direct supplier-page fetch returned anti-bot/login markup; the attached product and size-chart screenshots are the authoritative evidence for this draft.

## Source Measurement Notes
The attached chart publishes shoulder, bust, and garment length. Waist and hip values were derived from the prompt rules because the chart does not publish waist or hip measurements.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Green Botanical Ruffle Mommy and Me Dresses` | 43 |
| SEO title | `Botanical Mommy and Me Dresses | Dress Like Mommy` | 49 |
| SEO description | `Green botanical mommy-and-me dresses for mom + daughter with airy ruffles. Size rows cover Child 4Y-10Y and Mother S-XL.` | 120 |

## SIZE_CHART / Variant Recap
| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Girl Dress | 110 | Child 4 Years | Green Botanical | `DLM-GBRF-GRL-KID4Y-GREEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Green Botanical | `DLM-GBRF-GRL-KID5Y-GREEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Green Botanical | `DLM-GBRF-GRL-KID67Y-GREEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Green Botanical | `DLM-GBRF-GRL-KID8Y-GREEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Green Botanical | `DLM-GBRF-GRL-KID910Y-GREEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Green Botanical | `DLM-GBRF-MOM-S-GREEN` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Green Botanical | `DLM-GBRF-MOM-M-GREEN` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Green Botanical | `DLM-GBRF-MOM-L-GREEN` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | Green Botanical | `DLM-GBRF-MOM-XL-GREEN` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |

## Derivations
- Request resolved to Mommy and Me because the supplied product image shows mother + girl and no father/boy rows were evidenced.
- Primary category resolved to Dresses from the garment evidence and Shopify taxonomy guard.
- Product options are `Size` and `Color`; Green Botanical is a single color value, so variant count equals the 9 chart rows.
- Child rows map 110-150 to Child 4 Years through Child 9-10 Years. Adult rows map S/M/L/XL to Mother S/M/L/XL.
- Child waist values use `chest`, child hip values use `chest + 4`, mother hip values use `bust + 6`, and mother waist values use `hip - 8`; garment length is source-transcribed.
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
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/poll_shopify_product_translations.py --handles green-botanical-ruffle-mommy-and-me-dresses --execute --force-refresh` | PASS; `candidate_products=1`, `processed_products=0`, `blocked_by_error=false` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles green-botanical-ruffle-mommy-and-me-dresses --execute` | PASS; registered `20` localized body translations with `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles green-botanical-ruffle-mommy-and-me-dresses --fail-on-missing` | PASS; `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles green-botanical-ruffle-mommy-and-me-dresses --fail-on-unmatched` | PASS; `products_with_unmatched_variants=0`, `unmatched_variant_locale_count=0`; because the product is a draft, `variant_locale_checks=0` |

## Price Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-GBRF-GRL-KID4Y-GREEN` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-GBRF-GRL-KID5Y-GREEN` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-GBRF-GRL-KID67Y-GREEN` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-GBRF-GRL-KID8Y-GREEN` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-GBRF-GRL-KID910Y-GREEN` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-GBRF-MOM-S-GREEN` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-GBRF-MOM-M-GREEN` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-GBRF-MOM-L-GREEN` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-GBRF-MOM-XL-GREEN` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |

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
- `shopify.dress-style`: No exact catalog GID was selected for this halter resort style.
- `shopify.dress-occasion`: No exact catalog GID was selected for a broad vacation/photo use case.
- `shopify.skirt-dress-length-type`: Source chart provides garment length, but no exact standardized dress-length type was selected in this run.
- `shopify.sleeve-length-type`: Halter/sleeveless styling is visible, but no exact trusted metaobject was selected in this run.
- `shopify.neckline`: Halter styling is visible, but no exact trusted neckline metaobject was selected in this run.
- `shopify.top-length-type`: Product taxonomy is Dresses, not Tops.

## Tags Written
Beach, Botanical Print, Child 4yr, Child 5yr, Child 6-7yr, Child 8yr, Child 9-10yr, Dresses, Girl Dress, Green, Green Botanical Ruffle, Green Dress, Leaf Print, Matching Family Dress, Matching Family Dresses, Matching Mommy and Me Dresses, Maxi Dress, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Daughter Matching Set, Mother Dress, Photo Ready, Resort, Ruffle Dress, Sleeveless Dress, Summer, Tiered Dress, Vacation

## Smart Collections
Product is a draft; collection indexing may wait until publication.

## Manual Follow-ups
1. Review the draft image and Green Botanical color naming in Shopify Admin before any separate publish-live request.
2. If exact fiber composition becomes available, add the fabric metafield before publishing.
3. If true waist/hip chart values become available, replace derived waist/hip values before publishing.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-gbrf-green-botanical-ruffle-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/green-botanical-ruffle-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/green-botanical-ruffle-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-green-botanical-ruffle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-green-botanical-ruffle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-green-botanical-ruffle-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/green-botanical-ruffle-mommy-and-me-dresses`
