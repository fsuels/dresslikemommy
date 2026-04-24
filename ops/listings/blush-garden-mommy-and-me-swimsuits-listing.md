# Blush Garden Mommy and Me Swimsuits - Ruffle Swim Dress

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536469639265
- **Live:** https://www.dresslikemommy.com/products/blush-garden-mommy-and-me-swimsuits
- **Vendor:** https://detail.1688.com/offer/1039451116404.html
- **Product GID:** `gid://shopify/Product/7536469639265`
- **Handle:** `blush-garden-mommy-and-me-swimsuits`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1039451116404.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | Swimsuit -> Swimsuits (Shopify taxonomy resolved to Swim Dresses) |
| DESIGNS_TO_LIST | Options color and size only -> Blush Floral only, no Type axis |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `BGDN` |
| COLOR_TOKEN | auto -> `BLUSH` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run on 2026-04-23, so the attached size-chart image and supplied product photos were used as the authoritative source of truth. The imagery shows a white-and-blush floral mother-daughter swim dress with a square ruffle neckline, attached bottoms, and a small rosette accent at the hip. Pricing was anchored to the live swim-dress neighbor `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`, size references were anchored to direct live `shopify--size` metaobject lookups, and the stale swimsuit taxonomy map in the prompt was corrected via live `node(id:)` validation before publish.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Blush Garden Mommy and Me Swimsuits - Ruffle Swim Dress` | 55 |
| SEO Title | `Blush Garden Mommy & Me Swim Dress | Dress Like Mommy` | 53 |
| SEO Description | `Stretch floral mommy-and-me swim dresses for mom + daughter. Sizes 3Y, 4Y, 5Y, 6-7Y, 9-10Y and Mom M-4XL.` | 105 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Swimsuit | M | Child 3 Years | `DLM-BGDN-GRL-KID3Y-BLUSH` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Swimsuit | L | Child 4 Years | `DLM-BGDN-GRL-KID4Y-BLUSH` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Swimsuit | XL | Child 5 Years | `DLM-BGDN-GRL-KID5Y-BLUSH` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Swimsuit | 2XL(部分款) | Child 6-7 Years | `DLM-BGDN-GRL-KID67Y-BLUSH` | 14.99 | 17.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Swimsuit | 3XL(部分款) | Child 9-10 Years | `DLM-BGDN-GRL-KID910Y-BLUSH` | 14.99 | 17.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Swimsuit | M | Mother M | `DLM-BGDN-MOM-M-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Swimsuit | L | Mother L | `DLM-BGDN-MOM-L-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Swimsuit | XL | Mother XL | `DLM-BGDN-MOM-XL-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Swimsuit | 2XL(部分款) | Mother 2XL | `DLM-BGDN-MOM-2XL-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975156833` (2XL) |
| Mother Swimsuit | 3XL(部分款) | Mother 3XL | `DLM-BGDN-MOM-3XL-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/139840421985` (3XL) |
| Mother Swimsuit | 4XL(部分款) | Mother 4XL | `DLM-BGDN-MOM-4XL-BLUSH` | 16.99 | 19.99 | `gid://shopify/Metaobject/139840716897` (4XL) |

### Derivations (flagged per spec)
- The swimsuit taxonomy GID in the canonical prompt (`gid://shopify/TaxonomyCategory/aa-1-13-15`) does not resolve in the live 2025-01 Admin API, so this run halted and corrected the taxonomy to the live leaf `gid://shopify/TaxonomyCategory/aa-1-20-17` (`Swim Dresses`) before publishing.
- The chart is a fit-recommendation table, not a garment-measurement table. Unsupported columns such as skirt length, pant length, hip, and garment length were kept as `-` instead of being fabricated.
- Child rows were mapped to the nearest canonical DLM size labels by height midpoint: 100-105 cm -> Child 3 Years, 105-115 cm -> Child 4 Years, 116-125 cm -> Child 5 Years, 126-140 cm -> Child 6-7 Years, and 140-155 cm -> Child 9-10 Years.
- Adult waist guidance was converted from Chinese chi ranges to cm/in for the shopper-facing table while the bust guidance stayed in the vendor's published bra-size notation.
- Adult 2XL, 3XL, and 4XL rows are marked `部分款` in the vendor chart. They were retained because the operator attached this exact chart for the selected floral print and did not exclude those rows.
- `Mother 4XL` extends the printed size scheme in the prompt, but the attached chart explicitly includes a 4XL row and the live store exposes a truthful `shopify--size` 4XL metaobject, so the run preserved it instead of collapsing the size range.

### Vendor -> picker mapping log
- Child M -> Child 3 Years
- Child L -> Child 4 Years
- Child XL -> Child 5 Years
- Child 2XL(部分款) -> Child 6-7 Years
- Child 3XL(部分款) -> Child 9-10 Years
- Mother M -> Mother M
- Mother L -> Mother L
- Mother XL -> Mother XL
- Mother 2XL(部分款) -> Mother 2XL
- Mother 3XL(部分款) -> Mother 3XL
- Mother 4XL(部分款) -> Mother 4XL

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 11 body rows.
- The size table keeps vendor recommendation data honest: height and weight use metric + imperial, bust stays in vendor bra-size notation, and unsupported measurement columns stay `-`.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 9-10 Years`, `Mother M`, `Mother L`, `Mother XL`, `Mother 2XL`, `Mother 3XL`, `Mother 4XL`
- Option 2: `Color` -> `Blush Floral`
- Variants live: **11**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 55 |
| SEO title <= 60 chars | Y | 53 |
| SEO description <= 155 chars | Y | 105 |
| Live variant count matches SIZE_CHART | Y | 11 vs 11 |
| Live SKUs match derived SKUs | Y | DLM-BGDN-GRL-KID3Y-BLUSH, DLM-BGDN-GRL-KID4Y-BLUSH, DLM-BGDN-GRL-KID5Y-BLUSH, DLM-BGDN-GRL-KID67Y-BLUSH, DLM-BGDN-GRL-KID910Y-BLUSH, DLM-BGDN-MOM-2XL-BLUSH, DLM-BGDN-MOM-3XL-BLUSH, DLM-BGDN-MOM-4XL-BLUSH, DLM-BGDN-MOM-L-BLUSH, DLM-BGDN-MOM-M-BLUSH, DLM-BGDN-MOM-XL-BLUSH |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 3 Years', 'Blush Floral'), ('Child 4 Years', 'Blush Floral'), ('Child 5 Years', 'Blush Floral'), ('Child 6-7 Years', 'Blush Floral'), ('Child 9-10 Years', 'Blush Floral'), ('Mother 2XL', 'Blush Floral'), ('Mother 3XL', 'Blush Floral'), ('Mother 4XL', 'Blush Floral'), ('Mother L', 'Blush Floral'), ('Mother M', 'Blush Floral'), ('Mother XL', 'Blush Floral')] |
| Size table first column matches picker labels | Y | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 9-10 Years | Mother M | Mother L | Mother XL | Mother 2XL | Mother 3XL | Mother 4XL |
| Age cells are blank for mother rows | Y | 3 | 4 | 5 | 6-7 | 9-10 |  |  |  |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 11 |
| Size table exposes vendor recommendation units | Y | kg/lbs + cm/in + bra size |
| Mother waist guidance is populated | Y | all mother rows populated |
| publishedAt is populated | Y | 2026-04-23T20:37:28Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/blush-garden-mommy-and-me-swimsuits |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-20-17 | Apparel & Accessories > Clothing > Swimwear > Swim Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1039451116404.html |
| Swimsuits collection tags are present | Y | Mommy and Me, Swimsuits |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-BGDN-GRL-KID3Y-BLUSH | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BGDN-GRL-KID4Y-BLUSH | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BGDN-GRL-KID5Y-BLUSH | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BGDN-GRL-KID67Y-BLUSH | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BGDN-GRL-KID910Y-BLUSH | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BGDN-MOM-M-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BGDN-MOM-L-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BGDN-MOM-XL-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BGDN-MOM-2XL-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BGDN-MOM-3XL-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BGDN-MOM-4XL-BLUSH | 16.99 | 19.99 | 16.99 | 19.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Blush Floral` |
| custom.style | single_line_text_field | `Ruffle Swim Dress` |
| custom.subcategory | single_line_text_field | `Swimsuits` |
| custom.subcategory2 | single_line_text_field | `Swim Dresses` |
| custom.type | single_line_text_field | `Swimsuit` |
| global.description_tag | single_line_text_field | `Stretch floral mommy-and-me swim dresses for mom + daughter. Sizes 3Y, 4Y, 5Y, 6-7Y, 9-...` |
| global.title_tag | single_line_text_field | `Blush Garden Mommy & Me Swim Dress | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Blush Garden` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Ruffle Swim Dress` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid:/...` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639733345","gid://shopify/Metaobject/69963645025","gid://s...` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972895841","gid://shopify/Metaobject/129972928609","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.care-instructions | The store's only live standard care option is `Machine washable`, which is less honest than the swim-specific rinse and hand-wash guidance used in the body copy. |
| shopify.clothing-features | The store's only live clothing-features option is `Insulated`, which is inaccurate for this lightweight swimsuit. |
| shopify.dress-occasion | Skipped because this swim-dress run only writes the universal metafields required by the listing prompt plus the honest swimwear basics. |
| shopify.dress-style | Skipped because the live swimwear neighbors do not rely on this standard metafield and the run already carries the style in custom metafields. |
| shopify.neckline | The ruffle neckline is visible in the imagery, but this run keeps swimwear writes to the lean verified set used by the live swimwear catalog. |
| shopify.skirt-dress-length-type | Skipped because the chart is a fit-recommendation table with no garment-length measurements to support a dress-length taxonomy write. |
| shopify.sleeve-length-type | Skipped per the listing prompt note used in recent swimwear and pajama runs: omit sleeve-length-type for swimsuits. |

## Tags written (33)
`Attached Bottoms, Beach, Blush, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Floral, Girl Swimsuit, https://detail.1688.com/offer/1039451116404.html, Matching Family Swimwear, Matching Swimwear, Mom Size 2XL, Mom Size 3XL, Mom Size 4XL, Mom Size L, Mom Size M, Mom Size XL, Mommy and Me, Mother Swimsuit, One-Piece Swimsuit, Pink, Pool, Resort, Rose Trim, Ruffle, Ruffle Swim Dress, Summer, Swim Dress, Swim Dresses, Swimsuits, Vacation, White`

## Publication
- Online Store
- Google & YouTube
- Facebook & Instagram
- Pinterest
- TikTok

## Smart collections
- Mother Daughter Swimsuits (`/swimsuits`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Manual follow-ups
- Confirm the exact fiber composition if the vendor page becomes accessible without captcha; `shopify.fabric` is set to `Polyester` because that is the only honest live standard fabric metaobject available in this store for this run.
- Re-check whether the selected floral print truly carries the vendor's `部分款` 4XL row once the source page is accessible without captcha.
- Inventory quantities and per-variant grams still need operator stock values.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-bgdn-blush-garden-mommy-and-me-swimsuits.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blush-garden-mommy-and-me-swimsuits-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blush-garden-mommy-and-me-swimsuits-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-blush-garden-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-blush-garden-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-blush-garden-mommy-and-me-swimsuits.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/blush-garden-mommy-and-me-swimsuits`

## Sources
- Price neighbor: `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`
- Size reference source: `live-shopify-size-metaobject`
- Collection rules verified live: `/swimsuits` requires the tags `Swimsuits` + `Mommy and Me`.
