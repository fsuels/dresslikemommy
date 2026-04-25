# Willow Mist Mommy and Me Dresses - Floral Hem Sundress

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7537109991521
- **Live:** https://www.dresslikemommy.com/products/willow-mist-mommy-and-me-dresses
- **Vendor:** https://detail.1688.com/offer/1044105977372.html
- **Product GID:** `gid://shopify/Product/7537109991521`
- **Handle:** `willow-mist-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1044105977372.html |
| SIZE_CHART_SOURCE | attached size-chart image plus supplied product images |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Dresses |
| DESIGNS_TO_LIST | White and Green as one listing with a Color option |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `WMST` |
| COLOR_TOKEN | per variant -> `WHITE` / `GREEN` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page returned Alibaba anti-bot challenge markup (`bxpunish: 1`), so the attached size-chart image and supplied product images were used as the authoritative source of truth for variants and design scope. The supplied imagery shows white/green mother-daughter floral-hem sundresses with shoulder ties, square neckline, sheer overlay, smocked back, and a softly gathered midi-length skirt. Pricing was anchored to the live dress neighbor `green-lace-garden-mommy-and-me-dresses`, size references were anchored to the store's live `shopify--size` metaobject inventory, and dress-category metafields were resolved from the supplied imagery plus the store's live dress metaobject catalog.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Willow Mist Mommy and Me Dresses - Floral Hem Sundress` | 54 |
| SEO Title | `Willow Mist Matching Dresses | Dress Like Mommy` | 47 |
| SEO Description | `Lightweight woven mommy-and-me dresses for mom + daughter in white or green. Sizes 4Y-12Y and Mom S-L with floral hems.` | 119 |

## SIZE_CHART recap
| Role | Vendor | Picker | Color | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|---|
| Girl Dress | 110 | Child 4 Years | White | `DLM-WMST-GRL-KID4Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 110 | Child 4 Years | Green | `DLM-WMST-GRL-KID4Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | White | `DLM-WMST-GRL-KID5Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 120 | Child 5 Years | Green | `DLM-WMST-GRL-KID5Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | White | `DLM-WMST-GRL-KID67Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 130 | Child 6-7 Years | Green | `DLM-WMST-GRL-KID67Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | White | `DLM-WMST-GRL-KID8Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 140 | Child 8 Years | Green | `DLM-WMST-GRL-KID8Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | White | `DLM-WMST-GRL-KID910Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Dress | 150 | Child 9-10 Years | Green | `DLM-WMST-GRL-KID910Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Dress | 160 | Child 12 Years | White | `DLM-WMST-GRL-KID12Y-WHITE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Girl Dress | 160 | Child 12 Years | Green | `DLM-WMST-GRL-KID12Y-GREEN` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Dress | 165 | Mother S | White | `DLM-WMST-MOM-S-WHITE` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | 165 | Mother S | Green | `DLM-WMST-MOM-S-GREEN` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | 170 | Mother M | White | `DLM-WMST-MOM-M-WHITE` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | 170 | Mother M | Green | `DLM-WMST-MOM-M-GREEN` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | 175 | Mother L | White | `DLM-WMST-MOM-L-WHITE` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | 175 | Mother L | Green | `DLM-WMST-MOM-L-GREEN` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975189601` (L) |

### Derivations (flagged per spec)
- The attached chart publishes vendor label, skirt length, and chest/bust in cm. Hip and waist are derived per the master prompt: child hip = chest + 4, child waist = chest; mother hip = bust + 6, mother waist = hip - 8.
- The attached chart does not publish weight guidance, so weight cells are shown as `-` instead of inventing ranges.
- Child age cells are canonical estimates from the mapped Shopify size labels because the source provided height labels, not age ranges.
- The vendor `160` child row extends beyond the stock prompt table that stops at `150`, so it was mapped to `Child 12 Years` using the live Shopify `12` size metaobject instead of dropping a vendor-backed row.

### Vendor -> picker mapping log
- 110 -> Child 4 Years
- 120 -> Child 5 Years
- 130 -> Child 6-7 Years
- 140 -> Child 8 Years
- 150 -> Child 9-10 Years
- 160 -> Child 12 Years
- 165 -> Mother S
- 170 -> Mother M
- 175 -> Mother L

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 9 body rows.
- Size table headers and cells keep both metric and imperial units so the storefront toggle works like the other listings.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Child 12 Years`, `Mother S`, `Mother M`, `Mother L`
- Option 2: `Color` -> `White`, `Green`
- Variants live: **18**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 54 |
| SEO title <= 60 chars | Y | 47 |
| SEO description <= 155 chars | Y | 119 |
| Live variant count matches derived size/color variants | Y | 18 vs 18 |
| Live SKUs match derived SKUs | Y | DLM-WMST-GRL-KID12Y-GREEN, DLM-WMST-GRL-KID12Y-WHITE, DLM-WMST-GRL-KID4Y-GREEN, DLM-WMST-GRL-KID4Y-WHITE, DLM-WMST-GRL-KID5Y-GREEN, DLM-WMST-GRL-KID5Y-WHITE, DLM-WMST-GRL-KID67Y-GREEN, DLM-WMST-GRL-KID67Y-WHITE, DLM-WMST-GRL-KID8Y-GREEN, DLM-WMST-GRL-KID8Y-WHITE, DLM-WMST-GRL-KID910Y-GREEN, DLM-WMST-GRL-KID910Y-WHITE, DLM-WMST-MOM-L-GREEN, DLM-WMST-MOM-L-WHITE, DLM-WMST-MOM-M-GREEN, DLM-WMST-MOM-M-WHITE, DLM-WMST-MOM-S-GREEN, DLM-WMST-MOM-S-WHITE |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 12 Years', 'Green'), ('Child 12 Years', 'White'), ('Child 4 Years', 'Green'), ('Child 4 Years', 'White'), ('Child 5 Years', 'Green'), ('Child 5 Years', 'White'), ('Child 6-7 Years', 'Green'), ('Child 6-7 Years', 'White'), ('Child 8 Years', 'Green'), ('Child 8 Years', 'White'), ('Child 9-10 Years', 'Green'), ('Child 9-10 Years', 'White'), ('Mother L', 'Green'), ('Mother L', 'White'), ('Mother M', 'Green'), ('Mother M', 'White'), ('Mother S', 'Green'), ('Mother S', 'White')] |
| Size table first column matches picker labels | Y | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Child 12 Years | Mother S | Mother M | Mother L |
| Age cells are blank for mother rows | Y | 4 | 5 | 6-7 | 8 | 9-10 | 11-12 |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 9 |
| Size table exposes metric + imperial units | Y | kg/lbs + cm/in |
| Waist populated for every row | Y | all rows populated |
| publishedAt is populated | Y | 2026-04-24T17:17:01Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/willow-mist-mommy-and-me-dresses |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-4 | Apparel & Accessories > Clothing > Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1044105977372.html |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-WMST-GRL-KID4Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID4Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID5Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID5Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID67Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID67Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID8Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID8Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID910Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID910Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID12Y-WHITE | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-GRL-KID12Y-GREEN | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-WMST-MOM-S-WHITE | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-WMST-MOM-S-GREEN | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-WMST-MOM-M-WHITE | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-WMST-MOM-M-GREEN | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-WMST-MOM-L-WHITE | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-WMST-MOM-L-GREEN | 34.99 | 40.99 | 34.99 | 40.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Willow Mist` |
| custom.style | single_line_text_field | `Willow Mist Sundress` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight woven mommy-and-me dresses for mom + daughter in white or green. Sizes 4Y-1...` |
| global.title_tag | single_line_text_field | `Willow Mist Matching Dresses | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Willow Mist` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Tie-Strap Sundress` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639733345","gid://shopify/Metaobject/70220546145","gid://s...` |
| shopify.dress-occasion | list.metaobject_reference | `["gid://shopify/Metaobject/69622169697","gid://shopify/Metaobject/69622202465"]` |
| shopify.dress-style | list.metaobject_reference | `["gid://shopify/Metaobject/130282520673"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.neckline | list.metaobject_reference | `["gid://shopify/Metaobject/144378429537"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972928609","gid://shopify/Metaobject/129972961377","gid:/...` |
| shopify.skirt-dress-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282487905"]` |
| shopify.sleeve-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/69622268001"]` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The store's only clothing-features option is `Insulated`, which is inaccurate for this airy summer dress, so it was intentionally left blank. |

## Tags written (30)
`Beach, Child 11-12yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Floral Hem, Garden Floral, Girl Dress, Green, https://detail.1688.com/offer/1044105977372.html, Matching Family Dress, Matching Family Dresses, Midi Dress, Midi Dresses, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Picnic, Resort, Ruffle Trim, Summer, Sundress, Sundresses, Tie Strap Dress, Vacation, White, Willow Mist`

## Publication
- Online Store
- Google & YouTube
- Facebook & Instagram
- Pinterest
- TikTok

## Smart collections
- Dresses (`/dresses`)
- Midi Dresses (`/midi-dresses`)
- Sundresses (`/sundresses`)
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)
- Mother Daughter Matching Dresses (`/mother-daughter-matching-dresses`)

## Manual follow-ups
- Confirm the exact fiber composition if the vendor page becomes accessible without captcha; `shopify.fabric` is set to `Polyester` as the best store-catalog match for the airy woven dress shown in the supplied imagery.
- Inventory quantities and per-variant grams still need operator stock values.
- Because the vendor chart is a fit guide rather than a garment-measurement table, recheck the derived bust/length ladder if a full spec sheet becomes available later.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-wmst-willow-mist-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/willow-mist-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/willow-mist-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-willow-mist-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-willow-mist-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-willow-mist-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/willow-mist-mommy-and-me-dresses`

## Sources
- Price neighbor: `green-lace-garden-mommy-and-me-dresses`
- Size reference source: `shopify--size metaobjects`
