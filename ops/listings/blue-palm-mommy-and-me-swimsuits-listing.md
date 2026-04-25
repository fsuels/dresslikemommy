# Blue Palm Mommy and Me Swimsuits - Ruffle Bikini

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7537097506913
- **Live:** https://www.dresslikemommy.com/products/blue-palm-mommy-and-me-swimsuits
- **Vendor:** https://detail.1688.com/offer/1043996254484.html?
- **Product GID:** `gid://shopify/Product/7537097506913`
- **Handle:** `blue-palm-mommy-and-me-swimsuits`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1043996254484.html? |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | Swimsuit -> Swimsuits (Shopify taxonomy resolved to Classic Bikinis) |
| DESIGNS_TO_LIST | Options color and size only -> Blue Palm only, no Type axis |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `BPLM` |
| COLOR_TOKEN | auto -> `NAVY` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was inaccessible through the browser tool during this run on 2026-04-24, so the attached size-chart image and supplied product photos were used as the authoritative source of truth. The imagery shows navy ruffle bikini tops paired with blue tropical palm high-waist bottoms for mom and daughter. Pricing was anchored to the live swimsuit neighbor `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`, size references were anchored to direct live `shopify--size` metaobject lookups, and the live swimsuit taxonomy was validated via live `node(id:)` validation before publish.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Blue Palm Mommy and Me Swimsuits - Ruffle Bikini` | 48 |
| SEO Title | `Blue Palm Mommy & Me Swimsuits | Dress Like Mommy` | 49 |
| SEO Description | `Stretch blue palm mommy-and-me swimsuits for mom + daughter. Girls 2Y-12Y and Mother S-XL with ruffle bikini styling.` | 117 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Swimsuit | 104 | Child 2 Years | `DLM-BPLM-GRL-KID2Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Swimsuit | 116 | Child 4 Years | `DLM-BPLM-GRL-KID4Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Swimsuit | 128 | Child 5 Years | `DLM-BPLM-GRL-KID5Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Swimsuit | 140 | Child 6-7 Years | `DLM-BPLM-GRL-KID67Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Swimsuit | 152 | Child 9-10 Years | `DLM-BPLM-GRL-KID910Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Swimsuit | 164 | Child 12 Years | `DLM-BPLM-GRL-KID12Y-NAVY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Swimsuit | S | Mother S | `DLM-BPLM-MOM-S-NAVY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Swimsuit | M | Mother M | `DLM-BPLM-MOM-M-NAVY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Swimsuit | L | Mother L | `DLM-BPLM-MOM-L-NAVY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Swimsuit | XL | Mother XL | `DLM-BPLM-MOM-XL-NAVY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975287905` (XL) |

### Derivations (flagged per spec)
- The swimsuit taxonomy GID in the canonical prompt (`gid://shopify/TaxonomyCategory/aa-1-13-15`) does not resolve in the live 2025-01 Admin API, so this run halted and corrected the taxonomy to the live leaf `gid://shopify/TaxonomyCategory/aa-1-20-6` (`Classic Bikinis`) before publishing.
- The chart is a fit-recommendation table, not a garment-measurement table. Unsupported columns such as skirt length, pant length, hip, and garment length were kept as `-` instead of being fabricated.
- Child rows were mapped from the attached height/age recommendation chart: 104 -> Child 2 Years, 116 -> Child 4 Years, 128 -> Child 5 Years, 140 -> Child 6-7 Years, 152 -> Child 9-10 Years, and 164 -> Child 12 Years.
- Adult bust, waist, and hip ranges were transcribed from the attached adult table in cm/in. Unsupported swimsuit length fields stay `-` instead of being fabricated.
- The attached mother table includes S, M, L, and XL only, so no 2XL, 3XL, or 4XL variants were created.

### Vendor -> picker mapping log
- Child 104 -> Child 2 Years
- Child 116 -> Child 4 Years
- Child 128 -> Child 5 Years
- Child 140 -> Child 6-7 Years
- Child 152 -> Child 9-10 Years
- Child 164 -> Child 12 Years
- Mother S -> Mother S
- Mother M -> Mother M
- Mother L -> Mother L
- Mother XL -> Mother XL

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 10 body rows.
- The size table keeps vendor recommendation data honest: height, weight, bust, waist, and hip use metric + imperial, and unsupported measurement columns stay `-`.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 2 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 9-10 Years`, `Child 12 Years`, `Mother S`, `Mother M`, `Mother L`, `Mother XL`
- Option 2: `Color` -> `Blue Palm`
- Variants live: **10**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 48 |
| SEO title <= 60 chars | Y | 49 |
| SEO description <= 155 chars | Y | 117 |
| Live variant count matches SIZE_CHART | Y | 10 vs 10 |
| Live SKUs match derived SKUs | Y | DLM-BPLM-GRL-KID12Y-NAVY, DLM-BPLM-GRL-KID2Y-NAVY, DLM-BPLM-GRL-KID4Y-NAVY, DLM-BPLM-GRL-KID5Y-NAVY, DLM-BPLM-GRL-KID67Y-NAVY, DLM-BPLM-GRL-KID910Y-NAVY, DLM-BPLM-MOM-L-NAVY, DLM-BPLM-MOM-M-NAVY, DLM-BPLM-MOM-S-NAVY, DLM-BPLM-MOM-XL-NAVY |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 12 Years', 'Blue Palm'), ('Child 2 Years', 'Blue Palm'), ('Child 4 Years', 'Blue Palm'), ('Child 5 Years', 'Blue Palm'), ('Child 6-7 Years', 'Blue Palm'), ('Child 9-10 Years', 'Blue Palm'), ('Mother L', 'Blue Palm'), ('Mother M', 'Blue Palm'), ('Mother S', 'Blue Palm'), ('Mother XL', 'Blue Palm')] |
| Size table first column matches picker labels | Y | Child 2 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 9-10 Years | Child 12 Years | Mother S | Mother M | Mother L | Mother XL |
| Age cells are blank for mother rows | Y | 2-3 | 4-5 | 5-6 | 6-8 | 8-10 | 10-12 |  |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 10 |
| Size table exposes vendor recommendation units | Y | kg/lbs + cm/in |
| Mother waist guidance is populated | Y | all mother rows populated |
| publishedAt is populated | Y | 2026-04-24T17:05:55Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/blue-palm-mommy-and-me-swimsuits |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-20-6 | Apparel & Accessories > Clothing > Swimwear > Classic Bikinis |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1043996254484.html? |
| Swimsuits collection tags are present | Y | Mommy and Me, Swimsuits |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-BPLM-GRL-KID2Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-GRL-KID4Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-GRL-KID5Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-GRL-KID67Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-GRL-KID910Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-GRL-KID12Y-NAVY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-BPLM-MOM-S-NAVY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BPLM-MOM-M-NAVY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BPLM-MOM-L-NAVY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-BPLM-MOM-XL-NAVY | 16.99 | 19.99 | 16.99 | 19.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Blue Palm` |
| custom.style | single_line_text_field | `Ruffle Bikini` |
| custom.subcategory | single_line_text_field | `Swimsuits` |
| custom.subcategory2 | single_line_text_field | `Classic Bikinis` |
| custom.type | single_line_text_field | `Swimsuit` |
| global.description_tag | single_line_text_field | `Stretch blue palm mommy-and-me swimsuits for mom + daughter. Girls 2Y-12Y and Mother S-...` |
| global.title_tag | single_line_text_field | `Blue Palm Mommy & Me Swimsuits | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Blue Palm` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Ruffle Bikini` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid:/...` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69639733345","gid://s...` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972863073","gid://shopify/Metaobject/129972928609","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.care-instructions | The store's only live standard care option is `Machine washable`, which is less honest than the swim-specific rinse and hand-wash guidance used in the body copy. |
| shopify.clothing-features | The store's only live clothing-features option is `Insulated`, which is inaccurate for this lightweight swimsuit. |
| shopify.dress-occasion | Skipped because this swimsuit run only writes the universal metafields required by the listing prompt plus the honest swimwear basics. |
| shopify.dress-style | Skipped because the live swimwear neighbors do not rely on this standard metafield and the run already carries the style in custom metafields. |
| shopify.neckline | The ruffle neckline is visible in the imagery, but this run keeps swimwear writes to the lean verified set used by the live swimwear catalog. |
| shopify.skirt-dress-length-type | Skipped because the chart is a fit-recommendation table with no garment-length measurements to support a dress-length taxonomy write. |
| shopify.sleeve-length-type | Skipped per the listing prompt note used in recent swimwear and pajama runs: omit sleeve-length-type for swimsuits. |

## Tags written (31)
`Beach, Bikini Swimsuit, Blue, Child 10-12yr, Child 2-3yr, Child 4-5yr, Child 5-6yr, Child 6-8yr, Child 8-10yr, Girl Swimsuit, High Waist Bottom, https://detail.1688.com/offer/1043996254484.html?, Matching Family Swimwear, Matching Swimwear, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Swimsuit, Palm, Pool, Resort, Ruffle, Ruffle Bikini, Spaghetti Strap, Summer, Swimsuits, Tropical Print, Two-Piece Swimsuit, Vacation`

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
- Re-check the exact vendor fabric composition if the source page becomes accessible without captcha; no fiber label was visible in the attached evidence.
- Inventory quantities and per-variant grams still need operator stock values.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-bplm-blue-palm-mommy-and-me-swimsuits.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blue-palm-mommy-and-me-swimsuits-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blue-palm-mommy-and-me-swimsuits-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-blue-palm-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-blue-palm-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-blue-palm-mommy-and-me-swimsuits.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/blue-palm-mommy-and-me-swimsuits`

## Sources
- Price neighbor: `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`
- Size reference source: `live-shopify-size-metaobject`
- Collection rules verified live: `/swimsuits` requires the tags `Swimsuits` + `Mommy and Me`.
