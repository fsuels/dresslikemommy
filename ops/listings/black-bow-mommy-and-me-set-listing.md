# Black Bow Mommy and Me Set - Tie-Neck Top & Skirt

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536988618849
- **Live:** https://www.dresslikemommy.com/products/black-bow-mommy-and-me-set
- **Vendor:** https://detail.1688.com/offer/1044368546950.html
- **Product GID:** `gid://shopify/Product/7536988618849`
- **Handle:** `black-bow-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1044368546950.html |
| SIZE_CHART_SOURCE | pasted vendor fit labels plus supplied product images |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Sets (Shopify taxonomy kept as Outfit Sets) |
| DESIGNS_TO_LIST | auto -> black mother-daughter top + skirt set only |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `BBTS` |
| COLOR_TOKEN | auto -> `BLACK` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page returned Alibaba anti-bot/captcha markup during this run, so the pasted vendor fit labels and supplied lifestyle photos were used as the authoritative source of truth. The supplied images show a black sleeveless tie-neck top with a flouncy skirt for girls and mothers. Pricing was anchored to `powder-blue-mommy-and-me-set`, and size metaobject GIDs were anchored to `ivory-ruffle-mommy-and-me-dresses`.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Black Bow Mommy and Me Set - Tie-Neck Top & Skirt` | 49 |
| SEO Title | `Black Bow Mommy & Me Set | Dress Like Mommy` | 43 |
| SEO Description | `Lightweight black mommy-and-me two-piece set for mom + daughter with sleeveless tie-neck top and flouncy skirt. Sizes 2Y-10Y and Mom S-L.` | 137 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Set | 90 | Child 2 Years | `DLM-BBTS-GRL-KID2Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Set | 100 | Child 3 Years | `DLM-BBTS-GRL-KID3Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Set | 110 | Child 4 Years | `DLM-BBTS-GRL-KID4Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Set | 120 | Child 5 Years | `DLM-BBTS-GRL-KID5Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Set | 130 | Child 6-7 Years | `DLM-BBTS-GRL-KID67Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Set | 140 | Child 8 Years | `DLM-BBTS-GRL-KID8Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Set | 150 | Child 9-10 Years | `DLM-BBTS-GRL-KID910Y-BLACK` | 28.99 | 33.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Set | S | Mother S | `DLM-BBTS-MOM-S-BLACK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Set | M | Mother M | `DLM-BBTS-MOM-M-BLACK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Set | L | Mother L | `DLM-BBTS-MOM-L-BLACK` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975189601` (L) |

### Derivations (flagged per spec)
- The supplied source gives size/fit labels only, not a full garment-measurement table, so `chest_cm`, `waist_cm`, `hip_cm`, `length_cm`, and `skirt_cm` were derived from the store's live loose summer set grading anchored to `powder-blue-mommy-and-me-set`.
- `hip_cm` was derived as `chest_cm + 4` from the store's loose summer set grading because the vendor size notes omit hip.
- `length_cm` represents the sleeveless top length; `skirt_cm` represents the separate flouncy skirt length so the set keeps both garment measurements distinct.
- Mother-row height guidance was derived from the store's live mommy-and-me dress/set ladder because the supplied vendor notes only publish S/M/L labels.

### Vendor -> picker mapping log
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
- No explicit exclusions were requested.
- Kept every supplied mommy-and-me row: child 90-150 plus mother S/M/L.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` + 1 size table with 10 `<th>` headers and 10 body rows.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` -> `Child 2 Years`, `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`, `Mother L`
- Option 2: `Color` -> `Black`
- Variants live: **10**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | Y | 49 |
| SEO title <= 60 chars | Y | 43 |
| SEO description <= 155 chars | Y | 137 |
| Live variant count matches SIZE_CHART | Y | 10 vs 10 |
| Live SKUs match derived SKUs | Y | DLM-BBTS-GRL-KID2Y-BLACK, DLM-BBTS-GRL-KID3Y-BLACK, DLM-BBTS-GRL-KID4Y-BLACK, DLM-BBTS-GRL-KID5Y-BLACK, DLM-BBTS-GRL-KID67Y-BLACK, DLM-BBTS-GRL-KID8Y-BLACK, DLM-BBTS-GRL-KID910Y-BLACK, DLM-BBTS-MOM-L-BLACK, DLM-BBTS-MOM-M-BLACK, DLM-BBTS-MOM-S-BLACK |
| Live option axes match derived axes | Y | Size / Color |
| Every Size x Color combination exists | Y | [('Child 2 Years', 'Black'), ('Child 3 Years', 'Black'), ('Child 4 Years', 'Black'), ('Child 5 Years', 'Black'), ('Child 6-7 Years', 'Black'), ('Child 8 Years', 'Black'), ('Child 9-10 Years', 'Black'), ('Mother L', 'Black'), ('Mother M', 'Black'), ('Mother S', 'Black')] |
| Size table first column matches picker labels | Y | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M | Mother L |
| Each size table has 10 headers | Y | 10 |
| Table row count matches SIZE_CHART | Y | 10 |
| publishedAt is populated | Y | 2026-04-24T14:26:06Z |
| onlineStoreUrl is populated | Y | https://www.dresslikemommy.com/products/black-bow-mommy-and-me-set |
| Taxonomy category is set | Y | gid://shopify/TaxonomyCategory/aa-1-11 |
| Taxonomy category full name matches expected leaf | Y | Apparel & Accessories > Clothing > Outfit Sets |
| Dress merchandising tag is present | Y | Beach, Black, Bow Neck, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Flouncy Skirt, Girl Dress, https://detail.1688.com/offer/1044368546950.html, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Matching Family Set, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Resort, Skirt Set, Sleeveless Dress, Summer, Summer Dresses, Sundresses, Tie-Neck Top, Two-Piece Set, Vacation |
| Dress smart collection is attached | Y | ['dresses', 'matching-family-vacation-outfits', 'mommy-and-me', 'mother-daughter-matching-dresses', 'new-matching-outfits', 'popular-mommy-me-1', 'sundresses'] |
| Required publications are live | Y | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Applicable metafields are written | Y | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-BBTS-GRL-KID2Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID3Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID4Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID5Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID67Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID8Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-GRL-KID910Y-BLACK | 28.99 | 33.99 | 28.99 | 33.99 | Y |
| DLM-BBTS-MOM-S-BLACK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-BBTS-MOM-M-BLACK | 31.99 | 36.99 | 31.99 | 36.99 | Y |
| DLM-BBTS-MOM-L-BLACK | 31.99 | 36.99 | 31.99 | 36.99 | Y |

## Metafields - written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Black` |
| custom.style | single_line_text_field | `Tie-Neck Top & Skirt` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Two-Piece Set` |
| global.description_tag | single_line_text_field | `Lightweight black mommy-and-me two-piece set for mom + daughter with sleeveless tie-nec...` |
| global.title_tag | single_line_text_field | `Black Bow Mommy & Me Set | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Black Bow` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Tie-Neck Top & Skirt` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69943132257"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972863073","gid://shopify/Metaobject/129972895841","gid:/...` |
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
| shopify.neckline | The images support a tie-neck gathered neckline, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.pants-length-type | Not applicable because this coordinated product pairs a sleeveless top with a skirt rather than pants or shorts. |
| shopify.skirt-dress-length-type | Not written because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`, even though the storefront merchandising override places it under dresses. |
| shopify.sleeve-length-type | The images support a sleeveless top, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.waist-rise | The skirt waist is visible in the imagery, but no reliable writable standard Shopify metafield definition is currently available in this store for this outfit-set product. |

## Tags written (29)
`Beach, Black, Bow Neck, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Flouncy Skirt, Girl Dress, https://detail.1688.com/offer/1044368546950.html, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Matching Family Set, Mom Size L, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Resort, Skirt Set, Sleeveless Dress, Summer, Summer Dresses, Sundresses, Tie-Neck Top, Two-Piece Set, Vacation`

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
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-bbts-black-bow-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/black-bow-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/black-bow-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-black-bow-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-black-bow-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-black-bow-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/black-bow-mommy-and-me-set`

## Sources
- Neighbor pricing: `powder-blue-mommy-and-me-set`
- Size metaobject map: `ivory-ruffle-mommy-and-me-dresses`
