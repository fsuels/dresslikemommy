# Coral Blossom Mommy and Me Dresses

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7607764287585
- **Live:** not published
- **Product GID:** `gid://shopify/Product/7607764287585`
- **Handle:** `coral-blossom-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | redacted per project source-URL policy |
| SIZE_CHART_SOURCE | attached size-chart image plus selector screenshot |
| LISTING_MODE | Mommy and Me (resolved from mother + girl evidence) |
| PRIMARY_CATEGORY | Dresses |
| DESIGNS_TO_LIST | Coral blossom floral dress |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | CBLM |
| COLOR_TOKEN | CORAL |

## Source Fetch Status
Direct supplier-page proof returned challenge-like markup; the attached product image, size-chart screenshot, and owner-provided selector screenshot are the authoritative evidence for this draft.

## Source Measurement Notes
The attached chart publishes bust/chest, waist, and dress length for child 110-150 and mother S/M/L. The selector screenshot shows Mother XL; its bust, waist, and length are estimated by continuing the S/M/L progression, and hip values are derived because the chart does not publish hip measurements.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Coral Blossom Mommy and Me Dresses` | 34 |
| SEO title | `Coral Mommy and Me Dresses | Dress Like Mommy` | 45 |
| SEO description | `Coral floral mommy-and-me beach dresses for mom + daughter. Size rows cover Child 4Y-9-10Y and Mother S-XL.` | 107 |

## SIZE_CHART / Variant Recap
| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Girl Dress | 110 | Child 4 Years | Coral Blossom | `DLM-CBLM-GRL-KID4Y-CORAL` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Coral Blossom | `DLM-CBLM-GRL-KID5Y-CORAL` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Coral Blossom | `DLM-CBLM-GRL-KID67Y-CORAL` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Coral Blossom | `DLM-CBLM-GRL-KID8Y-CORAL` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Coral Blossom | `DLM-CBLM-GRL-KID910Y-CORAL` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Coral Blossom | `DLM-CBLM-MOM-S-CORAL` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Coral Blossom | `DLM-CBLM-MOM-M-CORAL` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Coral Blossom | `DLM-CBLM-MOM-L-CORAL` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | Coral Blossom | `DLM-CBLM-MOM-XL-CORAL` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |

## Derivations
- Request resolved to Mommy and Me because the supplied product image shows mother + girl and no father/boy rows were evidenced.
- Primary category resolved to Dresses from the garment evidence and Shopify taxonomy guard.
- Product options are `Size` and `Color`; Coral Blossom is a single color value, so variant count equals the 9 derived rows.
- Child rows map 110-150 to Child 4 Years through Child 9-10 Years. Adult rows map S/M/L to Mother S/M/L; selector-backed Mother XL is included with estimated measurements.
- Child hip values use `chest + 4`; mother hip values use `bust + 6`. Waist and dress length are source values for S/M/L, while Mother XL waist and length are estimated from the S/M/L progression.
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
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/poll_shopify_product_translations.py --handles coral-blossom-mommy-and-me-dresses --execute --force-refresh` | PASS: `candidate_products=1`, `processed_products=1`, `blocked_by_error=false` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles coral-blossom-mommy-and-me-dresses --execute` | PASS: `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `registered_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/repair_localized_product_size_charts.py --handles coral-blossom-mommy-and-me-dresses --fail-on-missing` | PASS: `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |
| `PYTHONPATH=/tmp/dlm-py313-test-deps python3.13 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles coral-blossom-mommy-and-me-dresses --fail-on-unmatched` | PASS: `products_with_unmatched_variants=0`, `unmatched_variant_locale_count=0`; draft product had `variant_locale_checks=0` |

## Price Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-CBLM-GRL-KID4Y-CORAL` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-CBLM-GRL-KID5Y-CORAL` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-CBLM-GRL-KID67Y-CORAL` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-CBLM-GRL-KID8Y-CORAL` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-CBLM-GRL-KID910Y-CORAL` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-CBLM-MOM-S-CORAL` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-CBLM-MOM-M-CORAL` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-CBLM-MOM-L-CORAL` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-CBLM-MOM-XL-CORAL` | 34.99 | 40.99 | 17.5 | 34.99 | 40.99 | 17.50 | yes |

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
- `shopify.dress-style`: No exact catalog GID was selected for this cold-shoulder floral dress style.
- `shopify.dress-occasion`: No exact catalog GID was selected for a broad vacation/photo use case.
- `shopify.skirt-dress-length-type`: Source chart provides dress length but no standardized dress-length type.
- `shopify.sleeve-length-type`: Cold-shoulder styling is visible, but no exact trusted metaobject was selected in this run.
- `shopify.neckline`: Ruffle neckline styling is visible, but no exact trusted neckline metaobject was selected in this run.
- `shopify.top-length-type`: Product taxonomy is Dresses, not Tops.

## Tags Written
Beach Dress, Child 4yr, Child 5yr, Child 6-7yr, Child 8yr, Child 9-10yr, Cold Shoulder Dress, Coral, Coral Blossom, Dresses, Floral, Girl Dress, Matching Family Dresses, Matching Mommy and Me Dresses, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Daughter Matching Set, Mother Dress, Photo Ready, Pink, Pink Floral, Ruffle Dress, Summer, Vacation, Vacation Dress

## Smart Collections
Product is a draft; collection indexing may wait until publication.

## Manual Follow-ups
1. Review the draft image and coral/pink floral naming in Shopify Admin before any separate publish-live request.
2. If exact fiber composition becomes available, add the fabric metafield before publishing.
3. If true XL measurements or a true hip chart become available, replace the estimated/derived values before publishing.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-cblm-coral-blossom-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/coral-blossom-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/coral-blossom-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-coral-blossom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-coral-blossom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-coral-blossom-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/coral-blossom-mommy-and-me-dresses`
