# Pink Lace Garden Mommy and Me Dresses - Puff Sleeve Sundress

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536696295521
- **Live:** https://www.dresslikemommy.com/products/pink-lace-garden-mommy-and-me-dresses
- **Vendor:** https://detail.1688.com/offer/1031966994369.html?
- **Product GID:** `gid://shopify/Product/7536696295521`
- **Handle:** `pink-lace-garden-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1031966994369.html? |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Dresses |
| DESIGNS_TO_LIST | Pink only (requested Pink + Green; shipped as separate per-design listings) |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `PLGD` |
| COLOR_TOKEN | auto -> `PINK` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image was used as the authoritative source of truth for variants. The supplied lifestyle image shows a pink mother-daughter floral sundress with puff sleeves, an oversized white lace collar, and a softly gathered midi-length skirt. Pricing was anchored to the live dress neighbors `ivory-ruffle-mommy-and-me-dresses` and `pastel-bloom-mommy-and-me-dresses`, size references were anchored to the store's live `shopify--size` metaobject inventory, and dress-category metafields were resolved from the supplied imagery plus the store's live dress metaobject catalog.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Pink Lace Garden Mommy and Me Dresses - Puff Sleeve Sundress` | 60 |
| SEO Title | `Pink Lace Garden Sundress | Dress Like Mommy` | 44 |
| SEO Description | `Lightweight floral mommy-and-me sundresses for mom + daughter. Sizes 4Y-12Y and Mom S-XL with puff sleeves and a lace collar.` | 125 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Dress | 110 | Child 4 Years | `DLM-PLGD-GRL-KID4Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | `DLM-PLGD-GRL-KID5Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | `DLM-PLGD-GRL-KID67Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | `DLM-PLGD-GRL-KID8Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | `DLM-PLGD-GRL-KID910Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Girl Dress | 160 | Child 12 Years | `DLM-PLGD-GRL-KID12Y-PINK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129971650657` (12) |
| Mother Dress | S | Mother S | `DLM-PLGD-MOM-S-PINK` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | `DLM-PLGD-MOM-M-PINK` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | `DLM-PLGD-MOM-L-PINK` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | `DLM-PLGD-MOM-XL-PINK` | 34.99 | 40.99 | `gid://shopify/Metaobject/129975287905` (XL) |

### Derivations (flagged per spec)
- The attached vendor chart is a fit guide with age, height, and weight only, so `chest_cm`, `hip_cm`, `waist_cm`, `length_cm`, and `skirt_cm` were derived from the store's live dress size ladder plus the prompt's mother/child dress derivation rules.
- The child age cells are the vendor's printed age guidance, while the picker labels follow the canonical Shopify size mapping for 110-160.
- The vendor `160` child row extends beyond the stock prompt table that stops at `150`, so it was mapped to `Child 12 Years` using the live Shopify `12` size metaobject instead of dropping a vendor-backed row.

### Vendor -> picker mapping log
- 110 -> Child 4 Years
- 120 -> Child 5 Years
- 130 -> Child 6-7 Years
- 140 -> Child 8 Years
- 150 -> Child 9-10 Years
- 160 -> Child 12 Years
- S -> Mother S
- M -> Mother M
- L -> Mother L
- XL -> Mother XL

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row from the chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 10 body rows.
- Size table headers and cells keep both metric and imperial units so the storefront toggle works like the other listings.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Child 12 Years`, `Mother S`, `Mother M`, `Mother L`, `Mother XL`
- Option 2: `Color` -> `Pink`
- Variants live: **10**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 60 |
| SEO title <= 60 chars | Y | 44 |
| SEO description <= 155 chars | Y | 125 |
| Live variant count matches SIZE_CHART | Y | 10 vs 10 |
| Live SKUs match derived SKUs | Y | DLM-PLGD-GRL-KID12Y-PINK, DLM-PLGD-GRL-KID4Y-PINK, DLM-PLGD-GRL-KID5Y-PINK, DLM-PLGD-GRL-KID67Y-PINK, DLM-PLGD-GRL-KID8Y-PINK, DLM-PLGD-GRL-KID910Y-PINK, DLM-PLGD-MOM-L-PINK, DLM-PLGD-MOM-M-PINK, DLM-PLGD-MOM-S-PINK, DLM-PLGD-MOM-XL-PINK |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 12 Years', 'Pink'), ('Child 4 Years', 'Pink'), ('Child 5 Years', 'Pink'), ('Child 6-7 Years', 'Pink'), ('Child 8 Years', 'Pink'), ('Child 9-10 Years', 'Pink'), ('Mother L', 'Pink'), ('Mother M', 'Pink'), ('Mother S', 'Pink'), ('Mother XL', 'Pink')] |
| Size table first column matches picker labels | Y | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Child 12 Years | Mother S | Mother M | Mother L | Mother XL |
| Age cells are blank for mother rows | Y | 3-4 | 4-6 | 7-8 | 9-10 | 10-11 | 11-12 |  |  |  |  |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 10 |
| Size table exposes metric + imperial units | Y | kg/lbs + cm/in |
| Waist populated for every row | Y | all rows populated |
| publishedAt is populated | Y | 2026-04-24T03:41:35Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/pink-lace-garden-mommy-and-me-dresses |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-4 | Apparel & Accessories > Clothing > Dresses |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Vendor URL tag present | Y | https://detail.1688.com/offer/1031966994369.html? |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-PLGD-GRL-KID4Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-GRL-KID5Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-GRL-KID67Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-GRL-KID8Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-GRL-KID910Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-GRL-KID12Y-PINK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-PLGD-MOM-S-PINK | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-PLGD-MOM-M-PINK | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-PLGD-MOM-L-PINK | 34.99 | 40.99 | 34.99 | 40.99 | Y |
| DLM-PLGD-MOM-XL-PINK | 34.99 | 40.99 | 34.99 | 40.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Pink Floral` |
| custom.style | single_line_text_field | `Lace Collar Sundress` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight floral mommy-and-me sundresses for mom + daughter. Sizes 4Y-12Y and Mom S-X...` |
| global.title_tag | single_line_text_field | `Pink Lace Garden Sundress | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Pink Lace Garden` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Puff Sleeve Sundress` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69963645025","gid://shopify/Metaobject/129971519585"]` |
| shopify.dress-occasion | list.metaobject_reference | `["gid://shopify/Metaobject/69622169697","gid://shopify/Metaobject/69622202465"]` |
| shopify.dress-style | list.metaobject_reference | `["gid://shopify/Metaobject/130282520673"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622366305"]` |
| shopify.neckline | list.metaobject_reference | `["gid://shopify/Metaobject/144378429537"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972928609","gid://shopify/Metaobject/129972961377","gid:/...` |
| shopify.skirt-dress-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282487905"]` |
| shopify.sleeve-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/129971486817"]` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The store's only clothing-features option is `Insulated`, which is inaccurate for this airy summer dress, so it was intentionally left blank. |

## Tags written (31)
`Beach, Child 11-12yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Floral, Garden, Girl Dress, https://detail.1688.com/offer/1031966994369.html?, Lace Collar, Matching Family Dress, Matching Family Dresses, Midi Dress, Midi Dresses, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Mother Dress, Picnic, Pink, Puff Sleeve Dress, Resort, Scalloped Collar, Summer, Sundress, Sundresses, Vacation, White`

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
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-plgd-pink-lace-garden-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/pink-lace-garden-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/pink-lace-garden-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-pink-lace-garden-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-pink-lace-garden-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-pink-lace-garden-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/pink-lace-garden-mommy-and-me-dresses`

## Sources
- Price neighbor: `ivory-ruffle-mommy-and-me-dresses`
- Size reference source: `shopify--size metaobjects`
