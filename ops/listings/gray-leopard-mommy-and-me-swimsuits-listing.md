# Gray Leopard Mommy and Me Swimsuits - Ruffle Bikini

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7537096949857
- **Live:** https://www.dresslikemommy.com/products/gray-leopard-mommy-and-me-swimsuits
- **Vendor:** https://detail.1688.com/offer/1043999310235.html
- **Product GID:** `gid://shopify/Product/7537096949857`
- **Handle:** `gray-leopard-mommy-and-me-swimsuits`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1043999310235.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | Swimsuit -> Swimsuits (Shopify taxonomy resolved to Swim Dresses because the adult style includes a swim skirt) |
| DESIGNS_TO_LIST | Options color and size only -> Gray Leopard only, no Type axis |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `GLPD` |
| COLOR_TOKEN | auto -> `GRAY` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page returned Alibaba anti-bot/captcha markup during this run on 2026-04-24, so the attached size-chart image and supplied product photos were used as the authoritative source of truth. The imagery shows gray leopard ruffle bikini styling with black bottoms, plus an adult sheer tie-side swim skirt. Pricing was anchored to the live swimwear neighbor `blush-garden-mommy-and-me-swimsuits`, size references were anchored to direct live `shopify--size` metaobject lookups, and the stale swimsuit taxonomy map in the prompt was corrected via live `node(id:)` validation before publish.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Gray Leopard Mommy and Me Swimsuits - Ruffle Bikini` | 51 |
| SEO Title | `Gray Leopard Mommy & Me Swimsuits | Dress Like Mommy` | 52 |
| SEO Description | `Stretch gray leopard mommy-and-me swimsuits for mom + daughter. Girls 2Y-12Y and Mother S-XL with ruffle bikini styling.` | 120 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Swimsuit | 104 | Child 2 Years | `DLM-GLPD-GRL-KID2Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Swimsuit | 116 | Child 4 Years | `DLM-GLPD-GRL-KID4Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Swimsuit | 128 | Child 5 Years | `DLM-GLPD-GRL-KID5Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Swimsuit | 140 | Child 6-7 Years | `DLM-GLPD-GRL-KID67Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Swimsuit | 152 | Child 9-10 Years | `DLM-GLPD-GRL-KID910Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Swimsuit | 164 | Child 12 Years | `DLM-GLPD-GRL-KID12Y-GRAY` | 14.99 | 17.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Swimsuit | S | Mother S | `DLM-GLPD-MOM-S-GRAY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Swimsuit | M | Mother M | `DLM-GLPD-MOM-M-GRAY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Swimsuit | L | Mother L | `DLM-GLPD-MOM-L-GRAY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Swimsuit | XL | Mother XL | `DLM-GLPD-MOM-XL-GRAY` | 16.99 | 19.99 | `gid://shopify/Metaobject/129975287905` (XL) |

### Derivations (flagged per spec)
- The swimsuit taxonomy GID in the canonical prompt (`gid://shopify/TaxonomyCategory/aa-1-13-15`) does not resolve in the live 2025-01 Admin API, so this run halted and corrected the taxonomy to the live leaf `gid://shopify/TaxonomyCategory/aa-1-20-17` (`Swim Dresses`) before publishing.
- The child chart is a fit-recommendation table with height, weight, and age only; unsupported garment columns stay `-` instead of being fabricated.
- Adult rows provide bust, waist, and hip in both cm and inches. Adult height, weight, skirt, pant, and garment length are unavailable and stay `-`.
- Child rows were mapped to the nearest honest DLM size labels using the vendor age/height ranges: 104 -> Child 2 Years, 116 -> Child 4 Years, 128 -> Child 5 Years, 140 -> Child 6-7 Years, 152 -> Child 9-10 Years, and 164 -> Child 12 Years.
- `Child 12 Years` extends the base prompt's short child mapping, but the attached chart explicitly gives a 10-12 age row and the live store exposes a truthful `shopify--size` 12 metaobject, so the row was preserved.

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
- The size table keeps vendor recommendation data honest: child height/weight and adult bust/waist/hip use metric + imperial, and unsupported measurement columns stay `-`.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 2 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 9-10 Years`, `Child 12 Years`, `Mother S`, `Mother M`, `Mother L`, `Mother XL`
- Option 2: `Color` -> `Gray Leopard`
- Variants live: **10**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 51 |
| SEO title <= 60 chars | Y | 52 |
| SEO description <= 155 chars | Y | 120 |
| Live variant count matches SIZE_CHART | Y | 10 vs 10 |
| Live SKUs match derived SKUs | Y | DLM-GLPD-GRL-KID12Y-GRAY, DLM-GLPD-GRL-KID2Y-GRAY, DLM-GLPD-GRL-KID4Y-GRAY, DLM-GLPD-GRL-KID5Y-GRAY, DLM-GLPD-GRL-KID67Y-GRAY, DLM-GLPD-GRL-KID910Y-GRAY, DLM-GLPD-MOM-L-GRAY, DLM-GLPD-MOM-M-GRAY, DLM-GLPD-MOM-S-GRAY, DLM-GLPD-MOM-XL-GRAY |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 12 Years', 'Gray Leopard'), ('Child 2 Years', 'Gray Leopard'), ('Child 4 Years', 'Gray Leopard'), ('Child 5 Years', 'Gray Leopard'), ('Child 6-7 Years', 'Gray Leopard'), ('Child 9-10 Years', 'Gray Leopard'), ('Mother L', 'Gray Leopard'), ('Mother M', 'Gray Leopard'), ('Mother S', 'Gray Leopard'), ('Mother XL', 'Gray Leopard')] |
| Size table first column matches picker labels | Y | Child 2 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 9-10 Years | Child 12 Years | Mother S | Mother M | Mother L | Mother XL |
| Age cells are blank for mother rows | Y | 2-3 | 4-5 | 5-6 | 6-8 | 8-10 | 10-12 |  |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 10 |
| Size table exposes vendor recommendation units | Y | kg/lbs + cm/in |
| Mother waist guidance is populated | Y | all mother rows populated |
| publishedAt is populated | Y | 2026-04-24T17:05:28Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/gray-leopard-mommy-and-me-swimsuits |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-20-17 | Apparel & Accessories > Clothing > Swimwear > Swim Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1043999310235.html |
| Swimsuits collection tags are present | Y | Mommy and Me, Swimsuits |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-GLPD-GRL-KID2Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-GRL-KID4Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-GRL-KID5Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-GRL-KID67Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-GRL-KID910Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-GRL-KID12Y-GRAY | 14.99 | 17.99 | 14.99 | 17.99 | Y |
| DLM-GLPD-MOM-S-GRAY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-GLPD-MOM-M-GRAY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-GLPD-MOM-L-GRAY | 16.99 | 19.99 | 16.99 | 19.99 | Y |
| DLM-GLPD-MOM-XL-GRAY | 16.99 | 19.99 | 16.99 | 19.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Gray Leopard` |
| custom.style | single_line_text_field | `Ruffle Bikini` |
| custom.subcategory | single_line_text_field | `Swimsuits` |
| custom.subcategory2 | single_line_text_field | `Two-Piece Swimsuits` |
| custom.type | single_line_text_field | `Swimsuit` |
| global.description_tag | single_line_text_field | `Stretch gray leopard mommy-and-me swimsuits for mom + daughter. Girls 2Y-12Y and Mother...` |
| global.title_tag | single_line_text_field | `Gray Leopard Mommy & Me Swimsuits | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Gray Leopard` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Ruffle Bikini` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid:/...` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69944672353","gid://shopify/Metaobject/69943132257"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972863073","gid://shopify/Metaobject/129972928609","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.care-instructions | The store's only live standard care option is `Machine washable`, which is less honest than the swim-specific rinse and hand-wash guidance used in the body copy. |
| shopify.clothing-features | The store's only live clothing-features option is `Insulated`, which is inaccurate for this lightweight swimsuit. |
| shopify.dress-occasion | Skipped because this swimwear run only writes the universal metafields required by the listing prompt plus the honest swimwear basics. |
| shopify.dress-style | Skipped because the live swimwear neighbors do not rely on this standard metafield and the run already carries the style in custom metafields. |
| shopify.neckline | The ruffle neckline is visible in the imagery, but this run keeps swimwear writes to the lean verified set used by the live swimwear catalog. |
| shopify.skirt-dress-length-type | Skipped because the chart has no garment-length or skirt-length measurements to support a length taxonomy write. |
| shopify.sleeve-length-type | Skipped per the listing prompt note used in recent swimwear and pajama runs: omit sleeve-length-type for swimsuits. |

## Tags written (33)
`Animal Print, Beach, Bikini Swimsuit, Black, Child 10-12yr, Child 2-3yr, Child 4-5yr, Child 5-6yr, Child 6-8yr, Child 8-10yr, Girl Swimsuit, Gray, High Waist Bottom, https://detail.1688.com/offer/1043999310235.html, Leopard, Matching Family Swimwear, Matching Swimwear, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Swimsuit, Pool, Resort, Ruffle, Ruffle Bikini, Spaghetti Strap, Summer, Swim Skirt, Swimsuits, Two-Piece Swimsuit, Vacation`

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
- Confirm the exact fiber composition if the vendor page becomes accessible without captcha; `shopify.fabric` is set to `Polyester` following the live swimwear precedent, but the source screenshots do not confirm fiber content.
- Re-check whether the supplier has garment-length or skirt-length measurements beyond the attached fit chart once the source page is accessible without captcha.
- Inventory quantities and per-variant grams still need operator stock values.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-glpd-gray-leopard-mommy-and-me-swimsuits.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/gray-leopard-mommy-and-me-swimsuits-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/gray-leopard-mommy-and-me-swimsuits-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-gray-leopard-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-gray-leopard-mommy-and-me-swimsuits.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-gray-leopard-mommy-and-me-swimsuits.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/gray-leopard-mommy-and-me-swimsuits`

## Sources
- Price neighbor: `blush-garden-mommy-and-me-swimsuits`
- Size reference source: `live-shopify-size-metaobject`
- Collection rules verified live: `/swimsuits` requires the tags `Swimsuits` + `Mommy and Me`.
