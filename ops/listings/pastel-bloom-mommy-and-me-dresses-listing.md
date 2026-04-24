# Pastel Bloom Mommy and Me Dresses - Sleeveless Sundress

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536086089825
- **Live:** https://www.dresslikemommy.com/products/pastel-bloom-mommy-and-me-dresses
- **Vendor:** https://detail.1688.com/offer/895442481104.html?
- **Product GID:** `gid://shopify/Product/7536086089825`
- **Handle:** `pastel-bloom-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/895442481104.html? |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Dresses |
| DESIGNS_TO_LIST | auto -> Pastel Bloom only |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `PBLM` |
| COLOR_TOKEN | auto -> `PASTEL` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image was used as the authoritative source of truth for variants. The supplied lifestyle images show a sleeveless mother-daughter floral sundress with a rounded tie-front neckline, gathered waist, and airy midi-length skirt. Pricing was anchored to the live dress neighbor `white-lace-mommy-and-me-dresses`, size references were anchored to the store's live `shopify--size` metaobject inventory, and dress-category metafields were resolved from the supplied imagery plus the store's live dress metaobject catalog.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Pastel Bloom Mommy and Me Dresses - Sleeveless Sundress` | 55 |
| SEO Title | `Pastel Bloom Matching Sundress | Dress Like Mommy` | 49 |
| SEO Description | `Lightweight woven floral mommy-and-me sundresses for mom + daughter. Sizes 3Y-12Y and Mom M-L with an airy sleeveless resort fit.` | 129 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Dress | 100 | Child 3 Years | `DLM-PBLM-GRL-KID3Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | `DLM-PBLM-GRL-KID4Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | `DLM-PBLM-GRL-KID5Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | `DLM-PBLM-GRL-KID67Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | `DLM-PBLM-GRL-KID8Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | `DLM-PBLM-GRL-KID910Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Dress | 160 | Child 12 Years | `DLM-PBLM-GRL-KID12Y-PASTEL` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Dress | M | Mother M | `DLM-PBLM-MOM-M-PASTEL` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | `DLM-PBLM-MOM-L-PASTEL` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975189601` (L) |

### Derivations (flagged per spec)
- `hip_cm` and `waist_cm` were derived from the prompt rules because the vendor chart only publishes dress length and chest.
- `length_cm` and `skirt_cm` were both set from the vendor `裙长` column so the size table stays anchored to the chart without inventing a second unsupported dress-length field.
- The vendor `160` child row extends beyond the stock prompt table that stops at `150`, so it was mapped to `Child 12 Years` using the live Shopify `12` size metaobject instead of dropping a vendor-backed row.

### Vendor -> picker mapping log
- 100 -> Child 3 Years
- 110 -> Child 4 Years
- 120 -> Child 5 Years
- 130 -> Child 6-7 Years
- 140 -> Child 8 Years
- 150 -> Child 9-10 Years
- 160 -> Child 12 Years
- M -> Mother M
- L -> Mother L

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 9 body rows.
- Size table headers and cells keep both metric and imperial units so the storefront toggle works like the other listings.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Child 12 Years`, `Mother M`, `Mother L`
- Option 2: `Color` -> `Pastel Bloom`
- Variants live: **9**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 55 |
| SEO title <= 60 chars | Y | 49 |
| SEO description <= 155 chars | Y | 129 |
| Live variant count matches SIZE_CHART | Y | 9 vs 9 |
| Live SKUs match derived SKUs | Y | DLM-PBLM-GRL-KID12Y-PASTEL, DLM-PBLM-GRL-KID3Y-PASTEL, DLM-PBLM-GRL-KID4Y-PASTEL, DLM-PBLM-GRL-KID5Y-PASTEL, DLM-PBLM-GRL-KID67Y-PASTEL, DLM-PBLM-GRL-KID8Y-PASTEL, DLM-PBLM-GRL-KID910Y-PASTEL, DLM-PBLM-MOM-L-PASTEL, DLM-PBLM-MOM-M-PASTEL |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 12 Years', 'Pastel Bloom'), ('Child 3 Years', 'Pastel Bloom'), ('Child 4 Years', 'Pastel Bloom'), ('Child 5 Years', 'Pastel Bloom'), ('Child 6-7 Years', 'Pastel Bloom'), ('Child 8 Years', 'Pastel Bloom'), ('Child 9-10 Years', 'Pastel Bloom'), ('Mother L', 'Pastel Bloom'), ('Mother M', 'Pastel Bloom')] |
| Size table first column matches picker labels | Y | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Child 12 Years | Mother M | Mother L |
| Age cells are blank for mother rows | Y | 3 | 4 | 5 | 6-7 | 8 | 9-10 | 11-12 |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 9 |
| Size table exposes metric + imperial units | Y | kg/lbs + cm/in |
| Waist populated for every row | Y | all rows populated |
| publishedAt is populated | Y | 2026-04-23T15:12:54Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/pastel-bloom-mommy-and-me-dresses |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-4 | Apparel & Accessories > Clothing > Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/895442481104.html? |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-PBLM-GRL-KID3Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID4Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID5Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID67Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID8Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID910Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-GRL-KID12Y-PASTEL | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PBLM-MOM-M-PASTEL | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-PBLM-MOM-L-PASTEL | 34.99 | 40.99 | 34.99 | 40.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Watercolor Floral` |
| custom.style | single_line_text_field | `Resort Sundress` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight woven floral mommy-and-me sundresses for mom + daughter. Sizes 3Y-12Y and M...` |
| global.title_tag | single_line_text_field | `Pastel Bloom Matching Sundress | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Pastel Bloom` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Sleeveless Sundress` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/129971519585","gid://shopify/Metaobject/130231140449"]` |
| shopify.dress-occasion | list.metaobject_reference | `["gid://shopify/Metaobject/69622169697","gid://shopify/Metaobject/69622202465"]` |
| shopify.dress-style | list.metaobject_reference | `["gid://shopify/Metaobject/130282520673"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.neckline | list.metaobject_reference | `["gid://shopify/Metaobject/129972469857"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972895841","gid://shopify/Metaobject/129972928609","gid:/...` |
| shopify.skirt-dress-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282487905"]` |
| shopify.sleeve-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/69622268001"]` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The store's only clothing-features option is `Insulated`, which is inaccurate for this airy summer dress, so it was intentionally left blank. |

## Tags written (32)
`Beach, Bloom, Child 11-12yr, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Floral, Garden, Girl Dress, Green, https://detail.1688.com/offer/895442481104.html?, Matching Family Dress, Matching Family Dresses, Midi Dress, Midi Dresses, Mom Size L, Mom Size M, Mommy and Me, Mother Dress, Pastel, Pink, Resort, Sleeveless Dress, Summer, Sundress, Vacation, Watercolor, White, Wildflower, Yellow`

## Publication
- Online Store
- Google & YouTube
- Facebook & Instagram
- Pinterest
- TikTok

## Smart collections
- Dresses (`/dresses`)
- Midi Dresses (`/midi-dresses`)
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)
- Mother Daughter Matching Dresses (`/mother-daughter-matching-dresses`)

## Manual follow-ups
- Confirm the exact fiber composition if the vendor page becomes accessible without captcha; `shopify.fabric` is set to `Polyester` as the best store-catalog match for the airy woven dress shown in the supplied imagery.
- Inventory quantities and per-variant grams still need operator stock values.
- If merchandising prefers the bigger-kid label phrased as `Child 11-12 Years`, update the option label copy later while keeping the underlying `12` size metaobject reference.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-pblm-pastel-bloom-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/pastel-bloom-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/pastel-bloom-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-pastel-bloom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-pastel-bloom-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-pastel-bloom-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/pastel-bloom-mommy-and-me-dresses`

## Sources
- Price neighbor: `white-lace-mommy-and-me-dresses`
- Size reference source: `shopify--size metaobjects`
