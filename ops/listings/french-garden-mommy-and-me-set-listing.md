# French Garden Mommy and Me Set - Dress & Cardigan

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7541038710881
- **Live:** not published
- **Vendor:** https://detail.1688.com/offer/1045719394654.html
- **Product GID:** `gid://shopify/Product/7541038710881`
- **Handle:** `french-garden-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1045719394654.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | auto -> Mommy and Me |
| PRIMARY_CATEGORY | auto -> Sets |
| DESIGNS_TO_LIST | auto -> French Garden dress and cardigan |
| EXCLUDE_ITEMS | none |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | auto -> `FGDN` |
| COLOR_TOKEN | auto -> `GARDEN` |

## Vendor Fetch Status
Direct 1688 fetch returned Alibaba anti-bot punish markup, so the attached product image and attached size-chart image were used as the authoritative evidence per the canonical workflow.

## Pricing
Prices use nearby mixed-piece family set pattern (lavender-hydrangea-family-matching-set): child rows at `31.99` and mother rows at `36.99`. Cost per item is exactly 50 percent: `16.00` child and `18.50` mother.

## Derivations
- The chart has separate item codes/tables for the strap dress and cardigan, so variants use `Type x Size` instead of a collapsed set SKU.
- The source chest columns are half-chest style measurements, so they were doubled before writing `chest_cm`.
- Dress hip/waist and cardigan hip/waist were derived from the canonical prompt rules because the vendor chart omits those fields.
- Adult recommended height is blank in the vendor chart and is rendered as `-`; adult sizing is anchored to vendor weight rows and the attached fit report.
- A garment token (`DRS` or `CDG`) was added to SKUs because the same role and size can exist for both Dress and Cardigan in this Type listing.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `French Garden Mommy and Me Set - Dress & Cardigan` | 49 |
| SEO title | `French Garden Mommy and Me Set | Dress Like Mommy` | 49 |
| SEO description | `Ivory floral mommy-and-me dress and cardigan pieces for mom + daughter. Fit chart supports Child 1-2Y-10Y and Mother S-L.` | 121 |

## SIZE_CHART / Variant Recap
| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---|---|---|
| Girl Dress | 80 | Child 1-2 Years | Dress | `DLM-FGDN-GRL-DRS-KID12Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Dress | 90 | Child 2 Years | Dress | `DLM-FGDN-GRL-DRS-KID2Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Dress | 100 | Child 3 Years | Dress | `DLM-FGDN-GRL-DRS-KID3Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | Dress | `DLM-FGDN-GRL-DRS-KID4Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Dress | `DLM-FGDN-GRL-DRS-KID5Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Dress | `DLM-FGDN-GRL-DRS-KID67Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Dress | `DLM-FGDN-GRL-DRS-KID8Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Dress | `DLM-FGDN-GRL-DRS-KID910Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Dress | `DLM-FGDN-MOM-DRS-S-GARDEN` | 36.99 | 18.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Dress | `DLM-FGDN-MOM-DRS-M-GARDEN` | 36.99 | 18.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Dress | `DLM-FGDN-MOM-DRS-L-GARDEN` | 36.99 | 18.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Girl Cardigan | 80 | Child 1-2 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID12Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Cardigan | 90 | Child 2 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID2Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Cardigan | 100 | Child 3 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID3Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Cardigan | 110 | Child 4 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID4Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Cardigan | 120 | Child 5 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID5Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Cardigan | 130 | Child 6-7 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID67Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Cardigan | 140 | Child 8 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID8Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Cardigan | 150 | Child 9-10 Years | Cardigan | `DLM-FGDN-GRL-CDG-KID910Y-GARDEN` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Cardigan | S | Mother S | Cardigan | `DLM-FGDN-MOM-CDG-S-GARDEN` | 36.99 | 18.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Cardigan | M | Mother M | Cardigan | `DLM-FGDN-MOM-CDG-M-GARDEN` | 36.99 | 18.50 | `gid://shopify/Metaobject/129975222369` (M) |

## Verification
| Check | Result | Detail |
|---|---|---|
| Title <= 70 | PASS | 49 |
| SEO title <= 60 | PASS | 49 |
| SEO description <= 155 | PASS | 121 |
| Variant count matches SIZE_CHART | PASS | 21 vs 21 |
| Live SKUs match derived SKUs | PASS | 21 |
| Every Type x Size combination exists | PASS | 21 |
| Each size table has 10 headers | PASS | [10, 10] |
| Size table row counts match SIZE_CHART | PASS | [11, 10] |
| Waist populated for every row | PASS | all rows |
| Product status is DRAFT | PASS | DRAFT |
| publishedAt is null | PASS | None |
| No sales-channel publications are live | PASS | [] |
| Taxonomy resolves to expected leaf | PASS | Apparel & Accessories > Clothing > Outfit Sets |
| Applicable metafields are written | PASS | [] |
| Cost per item equals 50 percent | PASS | paid_eligible=true |

## Price Parity
| SKU | Live Price | Live Compare | Live Cost | Expected Cost | Match |
|---|---|---|---|---|---|
| `DLM-FGDN-GRL-DRS-KID12Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID2Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID3Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID4Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID5Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID67Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID8Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-DRS-KID910Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-MOM-DRS-S-GARDEN` | 36.99 | 42.99 | 18.50 | 18.50 | PASS |
| `DLM-FGDN-MOM-DRS-M-GARDEN` | 36.99 | 42.99 | 18.50 | 18.50 | PASS |
| `DLM-FGDN-MOM-DRS-L-GARDEN` | 36.99 | 42.99 | 18.50 | 18.50 | PASS |
| `DLM-FGDN-GRL-CDG-KID12Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID2Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID3Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID4Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID5Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID67Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID8Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-GRL-CDG-KID910Y-GARDEN` | 31.99 | 36.99 | 16.00 | 16.00 | PASS |
| `DLM-FGDN-MOM-CDG-S-GARDEN` | 36.99 | 42.99 | 18.50 | 18.50 | PASS |
| `DLM-FGDN-MOM-CDG-M-GARDEN` | 36.99 | 42.99 | 18.50 | 18.50 | PASS |

## Smart Collections
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Metafields Written
- `custom.category1` (single_line_text_field): `Mommy and Me`
- `custom.pattern` (single_line_text_field): `Ivory Floral`
- `custom.style` (single_line_text_field): `Layered Summer Set`
- `custom.subcategory` (single_line_text_field): `Set`
- `custom.subcategory2` (single_line_text_field): `Summer Mommy and Me Set`
- `custom.type` (single_line_text_field): `Dress & Cardigan`
- `global.description_tag` (single_line_text_field): `Ivory floral mommy-and-me dress and cardigan pieces for mom + daughter. Fit chart suppo...`
- `global.title_tag` (single_line_text_field): `French Garden Mommy and Me Set | Dress Like Mommy`
- `mm-google-shopping.age_group` (single_line_text_field): `adult`
- `mm-google-shopping.condition` (single_line_text_field): `new`
- `mm-google-shopping.custom_label_0` (single_line_text_field): `Mommy and Me`
- `mm-google-shopping.custom_label_1` (single_line_text_field): `French Garden`
- `mm-google-shopping.custom_label_2` (single_line_text_field): `Summer`
- `mm-google-shopping.custom_label_3` (single_line_text_field): `Dress & Cardigan`
- `mm-google-shopping.custom_label_4` (single_line_text_field): `Two-Role Matching`
- `mm-google-shopping.custom_product` (boolean): `false`
- `mm-google-shopping.gender` (single_line_text_field): `female`
- `shopify.age-group` (list.metaobject_reference): `["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid:/...`
- `shopify.care-instructions` (list.metaobject_reference): `["gid://shopify/Metaobject/130283503713"]`
- `shopify.color-pattern` (list.metaobject_reference): `["gid://shopify/Metaobject/69639733345"]`
- `shopify.size` (list.metaobject_reference): `["gid://shopify/Metaobject/129972797537","gid://shopify/Metaobject/129972863073","gid:/...`
- `shopify.target-gender` (list.metaobject_reference): `["gid://shopify/Metaobject/129971617889"]`

## Metafields Skipped
- `shopify.fabric`: exact fiber is not confirmed by the attached evidence.
- `shopify.dress-occasion`, `shopify.dress-style`, `shopify.neckline`, `shopify.skirt-dress-length-type`, `shopify.sleeve-length-type`, and `shopify.top-length-type`: product mixes Dress and Cardigan, so one product-level garment attribute would be misleading.
- `shopify.clothing-features`: no supported, specific clothing-feature metaobject was needed for the supplied evidence.

## Publication
- Draft only. The runner did not call `publishablePublish`, `publishedAt` is null, and no sales-channel publication is live.

## Manual Follow-ups
- Confirm exact fabric composition before publishing.
- Inventory quantities and per-variant grams still need operator stock values.
- The product image is vendor/lifestyle evidence; replace or retouch if brand standards require cleaner publication media.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-fgdn-french-garden-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/french-garden-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/french-garden-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-french-garden-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-french-garden-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-french-garden-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/source-size-chart-french-garden-mommy-and-me-set.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/french-garden-mommy-and-me-set`
