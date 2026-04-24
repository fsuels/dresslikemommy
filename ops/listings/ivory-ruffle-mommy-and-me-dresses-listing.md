# Ivory Ruffle Mommy and Me Dresses - Tiered Sundress

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536309141601
- **Live:** https://www.dresslikemommy.com/products/ivory-ruffle-mommy-and-me-dresses
- **Vendor:** https://detail.1688.com/offer/1043178392944.html
- **Product GID:** `gid://shopify/Product/7536309141601`
- **Handle:** `ivory-ruffle-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1043178392944.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Dresses |
| DESIGNS_TO_LIST | auto -> Ivory Ruffle only |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `IRFL` |
| COLOR_TOKEN | auto -> `IVORY` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image was used as the authoritative source of truth for variants. The supplied lifestyle images show a sleeveless mother-daughter ivory tiered sundress with a gathered round neckline, layered ruffle panels, and an airy midi-length silhouette. Pricing was anchored to the live dress neighbor `white-lace-mommy-and-me-dresses`, size references were anchored to the store's live `shopify--size` metaobject inventory, and the chart's fit-report rows were transcribed below for rerun continuity.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Ivory Ruffle Mommy and Me Dresses - Tiered Sundress` | 51 |
| SEO Title | `Ivory Ruffle Matching Sundress | Dress Like Mommy` | 49 |
| SEO Description | `Lightweight woven mommy-and-me ruffle dresses for mom + daughter. Sizes 1-2Y through 10Y and Mom S-L with a breezy sleeveless fit.` | 130 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Dress | 80 | Child 1-2 Years | `DLM-IRFL-GRL-KID12Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Dress | 90 | Child 2 Years | `DLM-IRFL-GRL-KID2Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Dress | 100 | Child 3 Years | `DLM-IRFL-GRL-KID3Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | `DLM-IRFL-GRL-KID4Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | `DLM-IRFL-GRL-KID5Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | `DLM-IRFL-GRL-KID67Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | `DLM-IRFL-GRL-KID8Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | `DLM-IRFL-GRL-KID910Y-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | `DLM-IRFL-MOM-S-IVORY` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | `DLM-IRFL-MOM-M-IVORY` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | `DLM-IRFL-MOM-L-IVORY` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975189601` (L) |

### Derivations (flagged per spec)
- The vendor chest column is labeled `胸围*2`, so each published number was treated as a flat width and doubled to produce full `chest_cm` values before writing `SIZE_CHART`.
- `hip_cm` and `waist_cm` were derived from the prompt rules because the vendor chart only publishes dress length and chest guidance.
- `length_cm` and `skirt_cm` were both set from the vendor `裙长` column so the size table stays anchored to the chart without inventing a second unsupported dress-length field.
- The vendor `80` child row was mapped to `Child 1-2 Years`; its `shopify.size` reference uses the closest honest catalog size metaobject `12-18 months` because the store has no exact `1-2 years` metaobject label.
- Mother-row height guidance was derived from the live dress size ladder and the attached fit report because the vendor chart leaves adult recommended height blank.

### Vendor -> picker mapping log
- 80 -> Child 1-2 Years
- 90 -> Child 2 Years
- 100 -> Child 3 Years
- 110 -> Child 4 Years
- 120 -> Child 5 Years
- 130 -> Child 6-7 Years
- 140 -> Child 8 Years
- 150 -> Child 9-10 Years
- S -> Mother S
- M -> Mother M
- L -> Mother L

## Fit report
| Model | Height | Weight | Tried Size | Note |
|---|---|---|---|---|
| Girl | 134 cm / 52.8 in | 25 kg / 55.1 lbs | 140 | Loose |
| Mother | 164 cm / 64.6 in | 44 kg / 97.0 lbs | S | Loose |

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 11 body rows.
- Size table headers and cells keep both metric and imperial units so the storefront toggle works like the other listings.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 1-2 Years`, `Child 2 Years`, `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`, `Mother L`
- Option 2: `Color` -> `Ivory`
- Variants live: **11**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 51 |
| SEO title <= 60 chars | Y | 49 |
| SEO description <= 155 chars | Y | 130 |
| Live variant count matches SIZE_CHART | Y | 11 vs 11 |
| Live SKUs match derived SKUs | Y | DLM-IRFL-GRL-KID12Y-IVORY, DLM-IRFL-GRL-KID2Y-IVORY, DLM-IRFL-GRL-KID3Y-IVORY, DLM-IRFL-GRL-KID4Y-IVORY, DLM-IRFL-GRL-KID5Y-IVORY, DLM-IRFL-GRL-KID67Y-IVORY, DLM-IRFL-GRL-KID8Y-IVORY, DLM-IRFL-GRL-KID910Y-IVORY, DLM-IRFL-MOM-L-IVORY, DLM-IRFL-MOM-M-IVORY, DLM-IRFL-MOM-S-IVORY |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 1-2 Years', 'Ivory'), ('Child 2 Years', 'Ivory'), ('Child 3 Years', 'Ivory'), ('Child 4 Years', 'Ivory'), ('Child 5 Years', 'Ivory'), ('Child 6-7 Years', 'Ivory'), ('Child 8 Years', 'Ivory'), ('Child 9-10 Years', 'Ivory'), ('Mother L', 'Ivory'), ('Mother M', 'Ivory'), ('Mother S', 'Ivory')] |
| Size table first column matches picker labels | Y | Child 1-2 Years | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M | Mother L |
| Age cells are blank for mother rows | Y | 1-2 | 2 | 3 | 4 | 5 | 6-7 | 8 | 9-10 |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 11 |
| Size table exposes metric + imperial units | Y | kg/lbs + cm/in |
| Waist populated for every row | Y | all rows populated |
| publishedAt is populated | Y | 2026-04-23T17:48:43Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/ivory-ruffle-mommy-and-me-dresses |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-4 | Apparel & Accessories > Clothing > Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1043178392944.html |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-IRFL-GRL-KID12Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID2Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID3Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID4Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID5Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID67Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID8Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-GRL-KID910Y-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-IRFL-MOM-S-IVORY | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-IRFL-MOM-M-IVORY | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-IRFL-MOM-L-IVORY | 34.99 | 40.99 | 34.99 | 40.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Solid Ivory` |
| custom.style | single_line_text_field | `Tiered Sundress` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight woven mommy-and-me ruffle dresses for mom + daughter. Sizes 1-2Y through 10...` |
| global.title_tag | single_line_text_field | `Ivory Ruffle Matching Sundress | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Ivory Ruffle` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Tiered Sundress` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid:/...` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639733345"]` |
| shopify.dress-occasion | list.metaobject_reference | `["gid://shopify/Metaobject/69622169697","gid://shopify/Metaobject/69622202465"]` |
| shopify.dress-style | list.metaobject_reference | `["gid://shopify/Metaobject/130282520673"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.neckline | list.metaobject_reference | `["gid://shopify/Metaobject/129972469857"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972797537","gid://shopify/Metaobject/129972863073","gid:/...` |
| shopify.skirt-dress-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282487905"]` |
| shopify.sleeve-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/69622268001"]` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The store's only clothing-features option is `Insulated`, which is inaccurate for this airy summer dress, so it was intentionally left blank. |

## Tags written (30)
`Beach, Child 1-2yr, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Girl Dress, https://detail.1688.com/offer/1043178392944.html, Ivory, Matching Family Dress, Matching Family Dresses, Midi Dress, Midi Dresses, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Resort, Ruffle, Sleeveless Dress, Summer, Summer Dress, Summer Dresses, Sundress, Sundresses, Tiered, Vacation, White`

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
- Reconfirm whether merchandising wants the first kid row displayed as `Child 1-2 Years` or `Baby 12-18 Months`; the live `shopify.size` reference currently uses the closest honest `12-18 months` metaobject.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-irfl-ivory-ruffle-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ivory-ruffle-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ivory-ruffle-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-ivory-ruffle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-ivory-ruffle-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-ivory-ruffle-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/ivory-ruffle-mommy-and-me-dresses`

## Sources
- Price neighbor: `white-lace-mommy-and-me-dresses`
- Size reference source: `shopify--size metaobjects`
