# Red Resort Mommy and Me Set - Tee and Skirt

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7545373130849
- **Live:** https://www.dresslikemommy.com/products/red-resort-mommy-and-me-set
- **Vendor source:** https://detail.1688.com/offer/1042663719852.html
- **Product GID:** `gid://shopify/Product/7545373130849`
- **Handle:** `red-resort-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1042663719852.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | Sets / Outfit Sets |
| DESIGNS_TO_LIST | auto -> complete red short-sleeve top plus white pleated skirt set shown in the attached image and vendor selector |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | RRES |
| COLOR_TOKEN | REDWHT |

## Vendor Fetch Status
Direct 1688 fetch returned Alibaba anti-bot/CAPTCHA punish markup (`_____tmd_____`), so the attached product and size-chart images were used as authoritative evidence per the canonical workflow. The source URL is preserved only in local operator notes and was not written to Shopify-visible fields.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Red Resort Mommy and Me Set - Tee and Skirt` | 43 |
| SEO title | `Red Mommy and Me Outfit | Dress Like Mommy` | 42 |
| SEO description | `Red mom and daughter two-piece set with short-sleeve tops and white skirts. Sizes Child 4Y-10Y and Mother S-2XL.` | 112 |

## Pricing
| Audience | Set price | Compare-at | Cost |
|---|---:|---:|---:|
| Girl | 28.99 | 33.99 | 14.50 |
| Mother | 31.99 | 36.99 | 16.00 |

## SIZE_CHART / Variant Recap
| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Girl Set | Set 110 | Child 4 Years | Two-Piece Set | `DLM-RRES-GRL-SET-KID4Y-REDWHT` | 28.99 | 14.50 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Set | Set 120 | Child 5 Years | Two-Piece Set | `DLM-RRES-GRL-SET-KID5Y-REDWHT` | 28.99 | 14.50 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Set | Set 130 | Child 6-7 Years | Two-Piece Set | `DLM-RRES-GRL-SET-KID67Y-REDWHT` | 28.99 | 14.50 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Set | Set 140 | Child 8 Years | Two-Piece Set | `DLM-RRES-GRL-SET-KID8Y-REDWHT` | 28.99 | 14.50 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Set | Set 150 | Child 9-10 Years | Two-Piece Set | `DLM-RRES-GRL-SET-KID910Y-REDWHT` | 28.99 | 14.50 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Set | Set S | Mother S | Two-Piece Set | `DLM-RRES-MOM-SET-S-REDWHT` | 31.99 | 16.00 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Set | Set M | Mother M | Two-Piece Set | `DLM-RRES-MOM-SET-M-REDWHT` | 31.99 | 16.00 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Set | Set L | Mother L | Two-Piece Set | `DLM-RRES-MOM-SET-L-REDWHT` | 31.99 | 16.00 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Set | Set XL | Mother XL | Two-Piece Set | `DLM-RRES-MOM-SET-XL-REDWHT` | 31.99 | 16.00 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Set | Set 2XL | Mother 2XL | Two-Piece Set | `DLM-RRES-MOM-SET-2XL-REDWHT` | 31.99 | 16.00 | `gid://shopify/Metaobject/129975156833` (2XL) |

## Derivations
- `LISTING_MODE` resolved to Mommy and Me because the attached product image supports mother/daughter styling only; no father or boy product image evidence was supplied.
- Owner clarified the top and skirt are sold together, so the Shopify option model is one complete `Two-Piece Set` Type per size.
- Top source `胸围` values are flat garment widths, so they were doubled into wearable `chest_cm` values. Top hips/waists follow the canonical top derivation rules.
- Skirt source `全腰围` values were copied into waist only for selector sizes 110-150. Skirt hip cells are left unavailable because the source chart does not publish them.
- The seller selector screenshot confirms set sizes 110, 120, 130, 140, 150, S, M, L, XL, and 2XL; all are listed as complete-set variants.
- The skirt measurement screenshot includes rows 160 and 170, but those do not match the adult selector labels S-2XL, so they are not mapped to Mother S/M. Adult skirt measurements are shown as unavailable rather than converted incorrectly.
- Pricing follows nearby Mommy and Me complete-set precedent: girl `28.99`, mother `31.99`; Cost per item is exactly 50%.

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status preserved | PASS | ACTIVE |
| Publication timestamp policy | PASS | 2026-05-06T06:51:10Z |
| Sales-channel publication policy | PASS | ['Google & YouTube', 'Facebook & Instagram', 'Online Store', 'Pinterest', 'Microsoft Channel', 'TikTok', 'Buy Button', 'Point of Sale', 'n8n Integration'] |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Outfit Sets |
| Variant count matches SIZE_CHART | PASS | 10 vs 10 |
| Price and cost parity | PASS | 10 variants checked |
| Source URL guard | PASS | no forbidden source tokens in Shopify product fields |
| Size table rows | PASS | 10 |
| Size table headers | PASS | 10 headers per table |

## Price Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-RRES-GRL-SET-KID4Y-REDWHT` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-RRES-GRL-SET-KID5Y-REDWHT` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-RRES-GRL-SET-KID67Y-REDWHT` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-RRES-GRL-SET-KID8Y-REDWHT` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-RRES-GRL-SET-KID910Y-REDWHT` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-RRES-MOM-SET-S-REDWHT` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RRES-MOM-SET-M-REDWHT` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RRES-MOM-SET-L-REDWHT` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RRES-MOM-SET-XL-REDWHT` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-RRES-MOM-SET-2XL-REDWHT` | 31.99 | 36.99 | 16.0 | 31.99 | 36.99 | 16.00 | yes |

## Metafields Written
- `custom.category1`
- `custom.pattern`
- `custom.style`
- `custom.subcategory`
- `custom.subcategory2`
- `custom.type`
- `global.description_tag`
- `global.title_tag`
- `mc-facebook.google_product_category`
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
- `shopify.care-instructions`
- `shopify.color-pattern`
- `shopify.size`
- `shopify.target-gender`

## Metafields Skipped
- `shopify.fabric`: Exact fiber composition was not visible in the attached charts or product image.
- `shopify.sleeve-length-type`: Top sleeve lengths are charted, but no owner-subtype-safe sleeve-length catalog value was verified for this Outfit Sets taxonomy run.
- `shopify.neckline`: The red top neckline is visible, but no catalog GID was verified for the exact tee neckline in this product subtype.
- `shopify.top-length-type`: The vendor chart gives exact top lengths, but those do not map cleanly to one standard top-length type.
- `shopify.dress-occasion`: Not applicable because this is not a dress listing.
- `shopify.dress-style`: Not applicable because the garment is a top and skirt outfit, not a dress.
- `shopify.skirt-dress-length-type`: Skirt lengths are charted, but no owner-subtype-safe skirt-length catalog value was verified for this Outfit Sets taxonomy run.

## Smart Collections
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Manual Follow-ups
- Confirm exact fabric composition before any publish-live step.
- Inventory quantities and per-variant grams still need operator stock values.
- Confirm whether the vendor can provide adult S-2XL skirt measurements before publication.
- Consider a cleaner final photoshoot image set before launch.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-rres-red-resort-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-resort-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-resort-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-red-resort-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-red-resort-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-red-resort-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/uploads/red-resort-mommy-and-me-set`