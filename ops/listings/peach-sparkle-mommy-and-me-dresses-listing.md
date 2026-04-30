# Peach Sparkle Mommy and Me Dresses - Sequin Waist

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7541028651105
- **Live:** not published
- **Vendor:** https://detail.1688.com/offer/784122696506.html
- **Product GID:** `gid://shopify/Product/7541028651105`
- **Handle:** `peach-sparkle-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/784122696506.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | inferred Mommy and Me from supplied product image |
| PRIMARY_CATEGORY | Dresses |
| DESIGNS_TO_LIST | mother/daughter dress only |
| EXCLUDE_ITEMS | infant crawler rows and father rows excluded |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | PSPK |
| COLOR_TOKEN | PEACH |

## Vendor Fetch Status
The direct 1688 page returned Alibaba anti-bot challenge markup, so the attached size-chart image and supplied product image were used as the authoritative evidence. The image shows the mother and daughter dress only. The separate infant crawler size table and father rows were excluded because no supplied product evidence supports those garments for this listing.

## Pricing
Prices use the prevailing live Mommy and Me Dresses pattern: child rows at `31.99` and mother rows at `34.99`. Cost per item was set to exactly 50% of each selling price: `16.00` for child variants and `17.50` for mother variants.

## Derivations
- The attached chart publishes height and weight guidance only, so garment chest, hip, waist, and dress length values use the existing Dress Like Mommy mommy-and-me dress grading curve for this same 80-150 / Mother S-2XL ladder.
- Child hip and waist values follow the canonical dress derivation rule from chest measurements.
- Mother hip and waist values follow the canonical dress derivation rule from bust measurements.
- Vendor weight ranges were converted from jin to kg before rendering shopper-facing kg/lbs cells.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Peach Sparkle Mommy and Me Dresses - Sequin Waist` | 49 |
| SEO title | `Peach Sparkle Matching Dresses | Dress Like Mommy` | 49 |
| SEO description | `Peach sequin-waist mommy-and-me dresses for mom + daughter. Fit chart supports Child 1-2Y-9-10Y and Mother S-2XL.` | 113 |

## SIZE_CHART / Variant Recap
| Role | Vendor | Picker | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---|---|---|
| Girl Dress | 80 | Child 1-2 Years | Peach Sparkle | `DLM-PSPK-GRL-KID12Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Dress | 90 | Child 2 Years | Peach Sparkle | `DLM-PSPK-GRL-KID2Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Dress | 100 | Child 3 Years | Peach Sparkle | `DLM-PSPK-GRL-KID3Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | Peach Sparkle | `DLM-PSPK-GRL-KID4Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Peach Sparkle | `DLM-PSPK-GRL-KID5Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Peach Sparkle | `DLM-PSPK-GRL-KID67Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Peach Sparkle | `DLM-PSPK-GRL-KID8Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Peach Sparkle | `DLM-PSPK-GRL-KID910Y-PEACH` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Peach Sparkle | `DLM-PSPK-MOM-S-PEACH` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Peach Sparkle | `DLM-PSPK-MOM-M-PEACH` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Peach Sparkle | `DLM-PSPK-MOM-L-PEACH` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | Peach Sparkle | `DLM-PSPK-MOM-XL-PEACH` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Dress | 2XL | Mother 2XL | Peach Sparkle | `DLM-PSPK-MOM-2XL-PEACH` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975156833` (2XL) |

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status is DRAFT | PASS | DRAFT |
| publishedAt is null | PASS | None |
| Online Store URL absent | PASS | None |
| Variant count matches SIZE_CHART | PASS | 13 vs 13 |
| Live SKUs match derived SKUs | PASS | 13 expected |
| Price parity | PASS | FORCE_SPEC_PRICES=true |
| Cost parity | PASS | every unitCost equals price x 0.50 |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Dresses |
| Publications not live | PASS | [] |
| Size table row count | PASS | 13 |
| Size table header count | PASS | [10] |

## Smart Collections
New Arrivals, New Mommy & Me, Popular Mommy & Me, Mommy and Me Matching Outfits for Mother and Daughter, Matching Family Vacation Outfits

## Metafields Written
- `global.title_tag` (single_line_text_field)
- `global.description_tag` (single_line_text_field)
- `mc-facebook.google_product_category` (string)
- `custom.category1` (single_line_text_field)
- `custom.subcategory` (single_line_text_field)
- `custom.subcategory2` (single_line_text_field)
- `custom.pattern` (single_line_text_field)
- `custom.style` (single_line_text_field)
- `custom.type` (single_line_text_field)
- `mm-google-shopping.custom_product` (boolean)
- `mm-google-shopping.gender` (single_line_text_field)
- `mm-google-shopping.age_group` (single_line_text_field)
- `mm-google-shopping.condition` (single_line_text_field)
- `mm-google-shopping.custom_label_0` (single_line_text_field)
- `mm-google-shopping.custom_label_1` (single_line_text_field)
- `mm-google-shopping.custom_label_2` (single_line_text_field)
- `mm-google-shopping.custom_label_3` (single_line_text_field)
- `mm-google-shopping.custom_label_4` (single_line_text_field)
- `shopify.age-group` (list.metaobject_reference)
- `shopify.care-instructions` (list.metaobject_reference)
- `shopify.color-pattern` (list.metaobject_reference)
- `shopify.dress-occasion` (list.metaobject_reference)
- `shopify.dress-style` (list.metaobject_reference)
- `shopify.neckline` (list.metaobject_reference)
- `shopify.size` (list.metaobject_reference)
- `shopify.skirt-dress-length-type` (list.metaobject_reference)
- `shopify.sleeve-length-type` (list.metaobject_reference)
- `shopify.target-gender` (list.metaobject_reference)

## Metafields Skipped
- `shopify.fabric`: Exact fiber composition was not confirmed by the vendor page or attached images, so no fabric metafield was written.
- `shopify.top-length-type`: Does not apply to a dress listing.
- `shopify.clothing-features`: No supported, specific clothing-feature metaobject was needed for the supplied evidence.

## Manual Follow-ups
- Confirm exact fabric composition before publishing.
- Inventory quantities and per-variant weights still need operator stock values.
- Product remains draft and intentionally unpublished until a separate publish-live request.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-pspk-peach-sparkle-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/peach-sparkle-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/peach-sparkle-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-peach-sparkle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-peach-sparkle-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-peach-sparkle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/source-size-chart-peach-sparkle-mommy-and-me-dresses.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/peach-sparkle-mommy-and-me-dresses`
