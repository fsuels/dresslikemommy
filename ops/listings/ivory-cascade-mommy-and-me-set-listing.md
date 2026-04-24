# Ivory Cascade Mommy and Me Set - Sleeveless Top & Maxi Skirt

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536703012961
- **Live:** https://www.dresslikemommy.com/products/ivory-cascade-mommy-and-me-set
- **Vendor:** https://detail.1688.com/offer/1030397527808.html
- **Product GID:** `gid://shopify/Product/7536703012961`
- **Handle:** `ivory-cascade-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1030397527808.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | Dresses (storefront merchandising override; Shopify taxonomy kept as Outfit Sets) |
| DESIGNS_TO_LIST | Dress only -> female mother-daughter top + skirt set only |
| EXCLUDE_ITEMS | shirt table, gray shorts table |
| SHORTCODE | auto -> `ICAS` |
| COLOR_TOKEN | auto -> `IVORY` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image plus supplied lifestyle photos were used as the authoritative source of truth. The chart includes multiple garment tables, but the request explicitly limited the listing to `Dress only`, so the separate tee/shirt rows and the `26B069` gray shorts rows were excluded. The kept rows are the girl + mother `26B041` sleeveless top-and-skirt set, which is merchandised under dresses while keeping the honest Shopify taxonomy at `Outfit Sets`. Pricing was anchored to `powder-blue-mommy-and-me-set`, and size metaobject GIDs were anchored to `ivory-ruffle-mommy-and-me-dresses`.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Ivory Cascade Mommy and Me Set - Sleeveless Top & Maxi Skirt` | 60 |
| SEO Title | `Ivory Cascade Mommy & Me Set | Dress Like Mommy` | 47 |
| SEO Description | `Lightweight woven mommy-and-me set with a sleeveless ruffle top and flowing skirt for mom + daughter. Sizes 1-2Y-10Y and Mom S-L.` | 129 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Set | 80 | Child 1-2 Years | `DLM-ICAS-GRL-KID12Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Set | 90 | Child 2 Years | `DLM-ICAS-GRL-KID2Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Set | 100 | Child 3 Years | `DLM-ICAS-GRL-KID3Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Set | 110 | Child 4 Years | `DLM-ICAS-GRL-KID4Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Set | 120 | Child 5 Years | `DLM-ICAS-GRL-KID5Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Set | 130 | Child 6-7 Years | `DLM-ICAS-GRL-KID67Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Set | 140 | Child 8 Years | `DLM-ICAS-GRL-KID8Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Set | 150 | Child 9-10 Years | `DLM-ICAS-GRL-KID910Y-IVORY` | 28.99 | 33.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Set | S | Mother S | `DLM-ICAS-MOM-S-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Set | M | Mother M | `DLM-ICAS-MOM-M-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Set | L | Mother L | `DLM-ICAS-MOM-L-IVORY` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975189601` (L) |

### Derivations (flagged per spec)
- The vendor columns are labeled `胸围*2` and `腰围*2`, so each published row doubles those source values into full `chest_cm` and `waist_cm` before writing `SIZE_CHART`.
- `hip_cm` was derived as `chest_cm + 4` from the store's loose summer set grading, anchored to the live `powder-blue-mommy-and-me-set`, because the supplier chart omits hip.
- `length_cm` uses the vendor `衣长` top-length column, while `skirt_cm` uses the vendor `裙长` column so the set keeps both supported garment measurements instead of inventing one merged dress length.
- Mother-row height guidance was derived from the store's live mommy-and-me dress ladder because the vendor chart only publishes adult weight guidance.
- The vendor `80` child row was mapped to `Child 1-2 Years`; its `shopify.size` reference uses the closest honest catalog size metaobject `12-18 months` because the store has no exact `1-2 years` metaobject label.

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
- Excluded the separate shirt table because the request limited the listing to `Dress only` under `Mommy and Me`.
- Excluded the `26B069` gray shorts table for the same reason.
- Kept only the girl + mother `26B041` sleeveless top-and-skirt set rows.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` + 1 size table with 10 `<th>` headers and 11 body rows.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 1-2 Years`, `Child 2 Years`, `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`, `Mother L`
- Option 2: `Color` -> `Ivory`
- Variants live: **11**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 60 |
| SEO title <= 60 chars | Y | 47 |
| SEO description <= 155 chars | Y | 129 |
| Live variant count matches SIZE_CHART | Y | 11 vs 11 |
| Live SKUs match derived SKUs | Y | DLM-ICAS-GRL-KID12Y-IVORY, DLM-ICAS-GRL-KID2Y-IVORY, DLM-ICAS-GRL-KID3Y-IVORY, DLM-ICAS-GRL-KID4Y-IVORY, DLM-ICAS-GRL-KID5Y-IVORY, DLM-ICAS-GRL-KID67Y-IVORY, DLM-ICAS-GRL-KID8Y-IVORY, DLM-ICAS-GRL-KID910Y-IVORY, DLM-ICAS-MOM-L-IVORY, DLM-ICAS-MOM-M-IVORY, DLM-ICAS-MOM-S-IVORY |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 1-2 Years', 'Ivory'), ('Child 2 Years', 'Ivory'), ('Child 3 Years', 'Ivory'), ('Child 4 Years', 'Ivory'), ('Child 5 Years', 'Ivory'), ('Child 6-7 Years', 'Ivory'), ('Child 8 Years', 'Ivory'), ('Child 9-10 Years', 'Ivory'), ('Mother L', 'Ivory'), ('Mother M', 'Ivory'), ('Mother S', 'Ivory')] |
| Size table first column matches picker labels | Y | Child 1-2 Years | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M | Mother L |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 11 |
| publishedAt is populated | Y | 2026-04-24T04:08:27Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/ivory-cascade-mommy-and-me-set |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-11 |
| Taxonomy category full name matches expected leaf | Y | Apparel & Accessories > Clothing > Outfit Sets |
| Dress merchandising tag is present | Y | Beach, Child 1-2yr, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cream, Dresses, Girl Dress, https://detail.1688.com/offer/1030397527808.html, Ivory, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Matching Family Set, Maxi Skirt, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Resort, Ruffle Top, Skirt Set, Sleeveless Dress, Summer, Summer Dresses, Sundresses, Two-Piece Set, Vacation, White |
| Dress smart collection is attached | Y | ['dresses', 'matching-family-vacation-outfits', 'mommy-and-me', 'mother-daughter-matching-dresses', 'new-matching-outfits', 'popular-mommy-me-1', 'sundresses'] |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-ICAS-GRL-KID12Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID2Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID3Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID4Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID5Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID67Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID8Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-GRL-KID910Y-IVORY | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-ICAS-MOM-S-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-ICAS-MOM-M-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-ICAS-MOM-L-IVORY | 31.99 | 36.99 | 31.99 | 36.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Solid Ivory` |
| custom.style | single_line_text_field | `Sleeveless Top & Maxi Skirt` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight woven mommy-and-me set with a sleeveless ruffle top and flowing skirt for m...` |
| global.title_tag | single_line_text_field | `Ivory Cascade Mommy & Me Set | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Ivory Cascade` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Sleeveless Top & Maxi Skirt` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639733345"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972797537","gid://shopify/Metaobject/129972863073","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |
| shopify.top-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282553441"]` |

## Metafields - skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The current store catalog only exposes values like `Insulated` in this standard metafield namespace, which would be inaccurate for this lightweight summer outfit set. |
| shopify.fabric | The direct vendor page was captcha-blocked and the supplied chart plus images do not confirm one honest fiber metaobject, so this field was left unset rather than guessing cotton, rayon, or synthetic. |
| shopify.dress-occasion | Removed if present because the honest Shopify taxonomy for this product remains `Outfit Sets` even though the storefront merchandising override places it under dresses. |
| shopify.dress-style | Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`. |
| shopify.fit | The Outfit Sets taxonomy exposes fit, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.neckline | The images support a gathered round neckline, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.pants-length-type | Not applicable because this coordinated product pairs a sleeveless top with a skirt rather than pants or shorts. |
| shopify.skirt-dress-length-type | Not written because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`, even though the storefront merchandising override places it under dresses. |
| shopify.sleeve-length-type | The images support a sleeveless top, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.waist-rise | The skirt waist is visible in the imagery, but no reliable writable standard Shopify metafield definition is currently available in this store for this outfit-set product. |

## Tags written (31)
`Beach, Child 1-2yr, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cream, Dresses, Girl Dress, https://detail.1688.com/offer/1030397527808.html, Ivory, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Matching Family Set, Maxi Skirt, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Resort, Ruffle Top, Skirt Set, Sleeveless Dress, Summer, Summer Dresses, Sundresses, Two-Piece Set, Vacation, White`

## Publication
- Online Store
- Google & YouTube
- Facebook & Instagram
- Pinterest
- TikTok

## Smart collections
- Dresses (`/dresses`)
- Sundresses (`/sundresses`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)
- Mother Daughter Matching Dresses (`/mother-daughter-matching-dresses`)

## Manual follow-ups
- Inventory quantities and per-variant grams still need operator stock values.
- If the supplier page becomes readable later, confirm the exact fiber composition and write `shopify.fabric` only if one honest material metaobject is clearly supported.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-icas-ivory-cascade-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ivory-cascade-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/ivory-cascade-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-ivory-cascade-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-ivory-cascade-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-ivory-cascade-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/ivory-cascade-mommy-and-me-set`

## Sources
- Neighbor pricing: `powder-blue-mommy-and-me-set`
- Size metaobject map: `ivory-ruffle-mommy-and-me-dresses`
