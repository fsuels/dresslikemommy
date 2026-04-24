# Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7535944368225
- **Live:** https://www.dresslikemommy.com/products/powder-blue-mommy-and-me-set
- **Vendor:** https://detail.1688.com/offer/1034212252780.html
- **Product GID:** `gid://shopify/Product/7535944368225`
- **Handle:** `powder-blue-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1034212252780.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto → Dresses (storefront merchandising override; Shopify taxonomy kept as Outfit Sets) |
| DESIGNS_TO_LIST | auto → Powder Blue only |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto → `PBLU` |
| COLOR_TOKEN | auto → `BLUE` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image was used as the authoritative source of truth for variants. The supplied lifestyle images show a powder-blue flutter top paired with white eyelet wide-leg pants for mother and daughter. Neighbor pricing was anchored to `blue-striped-family-matching-set`, size metaobject GIDs were anchored to `white-lace-mommy-and-me-dresses`, the Shopify taxonomy stays `Outfit Sets` for honest standard-category attributes, and the storefront merchandising fields were intentionally overridden to `Dresses` plus the `Sundresses` tag so this listing can surface under dresses and use the dress pill.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants` | 57 |
| SEO Title | `Powder Blue Mommy & Me Set | Dress Like Mommy` | 45 |
| SEO Description | `Lightweight woven mommy-and-me set with a flutter top and eyelet pants for mom + daughter. Sizes 3Y–10Y and Mom S–M.` | 116 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Set | 100 | Child 3 Years | `DLM-PBLU-GRL-KID3Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Set | 110 | Child 4 Years | `DLM-PBLU-GRL-KID4Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Set | 120 | Child 5 Years | `DLM-PBLU-GRL-KID5Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Set | 130 | Child 6-7 Years | `DLM-PBLU-GRL-KID67Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Set | 140 | Child 8 Years | `DLM-PBLU-GRL-KID8Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840356449` (7-8 years) |
| Girl Set | 150 | Child 9-10 Years | `DLM-PBLU-GRL-KID910Y-BLUE` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840389217` (8-9 years (closest live catalog match)) |
| Mother Set | S | Mother S | `DLM-PBLU-MOM-S-BLUE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` (Mother S) |
| Mother Set | M | Mother M | `DLM-PBLU-MOM-M-BLUE` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (Mother M) |

### Derivations (flagged per spec)
- `chest_cm` and `hip_cm` were derived from standard loose summer set grading because the vendor chart only publishes top-drop, pant length, and waist.
- `weight` and `height` use the store's standard child and mother size guidance for the mapped picker labels.
- The vendor column labeled `吊带（肩带可调节）` was interpreted as the garment drop/visible top length because the 44–74 cm range aligns with the supplied photos; that published value is reused for both `skirt_cm` and `length_cm` to preserve the vendor evidence without inventing a second unsupported top-length field.

### Vendor → picker mapping log
- 100 → Child 3 Years
- 110 → Child 4 Years
- 120 → Child 5 Years
- 130 → Child 6-7 Years
- 140 → Child 8 Years
- 150 → Child 9-10 Years
- S → Mother S
- M → Mother M

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported row in the attached chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` + 1 size table with 10 `<th>` headers and 8 body rows.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Size` → `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`
- Option 2: `Color` → `Blue`
- Variants live: **8**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | ✅ | 57 |
| SEO title <= 60 chars | ✅ | 45 |
| SEO description <= 155 chars | ✅ | 116 |
| Live variant count matches SIZE_CHART | ✅ | 8 vs 8 |
| Live SKUs match derived SKUs | ✅ | DLM-PBLU-GRL-KID3Y-BLUE, DLM-PBLU-GRL-KID4Y-BLUE, DLM-PBLU-GRL-KID5Y-BLUE, DLM-PBLU-GRL-KID67Y-BLUE, DLM-PBLU-GRL-KID8Y-BLUE, DLM-PBLU-GRL-KID910Y-BLUE, DLM-PBLU-MOM-M-BLUE, DLM-PBLU-MOM-S-BLUE |
| Live option axes match derived axes | ✅ | Size / Color |
| Every Size x Color combination exists | ✅ | [('Child 3 Years', 'Blue'), ('Child 4 Years', 'Blue'), ('Child 5 Years', 'Blue'), ('Child 6-7 Years', 'Blue'), ('Child 8 Years', 'Blue'), ('Child 9-10 Years', 'Blue'), ('Mother M', 'Blue'), ('Mother S', 'Blue')] |
| Size table first column matches picker labels | ✅ | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M |
| Each size table has 10 headers | ✅ | 10 |
| Table row count matches SIZE_CHART | ✅ | 8 |
| publishedAt is populated | ✅ | 2026-04-23T15:07:10Z |
| onlineStoreUrl is populated | ✅ | https://www.dresslikemommy.com/products/powder-blue-mommy-and-me-set |
| Taxonomy category is set | ✅ | gid://shopify/TaxonomyCategory/aa-1-11 |
| Taxonomy category full name matches expected leaf | ✅ | Apparel & Accessories > Clothing > Outfit Sets |
| Dress merchandising tag is present | ✅ | Beach, Blue, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Eyelet, Flutter Top, Girl Dress, https://detail.1688.com/offer/1034212252780.html, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Mother M, Mother S, Powder Blue, Resort, Ruffle, Scalloped, Sleeveless Dress, Summer, Summer Dresses, Summer Matching Outfit, Sundresses, Vacation, White, Wide-Leg Pants |
| Dress smart collection is attached | ✅ | ['dresses', 'matching-family-vacation-outfits', 'mommy-and-me', 'mother-daughter-matching-dresses', 'new-matching-outfits', 'popular-mommy-me-1', 'sundresses'] |
| Required publications are live | ✅ | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Applicable metafields are written | ✅ | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-PBLU-GRL-KID3Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-GRL-KID4Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-GRL-KID5Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-GRL-KID67Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-GRL-KID8Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-GRL-KID910Y-BLUE | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-PBLU-MOM-S-BLUE | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-PBLU-MOM-M-BLUE | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |

## Metafields — written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Powder Blue Eyelet` |
| custom.style | single_line_text_field | `Resort Sundress` |
| custom.subcategory | single_line_text_field | `Dresses` |
| custom.subcategory2 | single_line_text_field | `Summer Dresses` |
| custom.type | single_line_text_field | `Dress` |
| global.description_tag | single_line_text_field | `Lightweight woven mommy-and-me set with a flutter top and eyelet pants for mom + daught...` |
| global.title_tag | single_line_text_field | `Powder Blue Mommy & Me Set | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Powder Blue` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Flutter Top & Eyelet Pants` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69639733345"]` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622399073"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972895841","gid://shopify/Metaobject/129972928609","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |
| shopify.top-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282553441"]` |

## Metafields — skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The current store catalog only exposes values like `Insulated` in this standard metafield namespace, which would be inaccurate for this lightweight summer outfit set. |
| shopify.dress-occasion | Removed if present because the honest Shopify taxonomy for this product remains `Outfit Sets` even though the storefront merchandising override places it under dresses. |
| shopify.dress-style | Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`. |
| shopify.fit | The Outfit Sets taxonomy exposes fit, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.neckline | The images support a square neckline, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.pants-length-type | The pants are visibly full length, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.skirt-dress-length-type | Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`. |
| shopify.sleeve-length-type | The images support a sleeveless / spaghetti-strap top, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.waist-rise | The waistband sits around the natural waist visually, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |

## Tags written (32)
`Beach, Blue, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Dresses, Eyelet, Flutter Top, Girl Dress, https://detail.1688.com/offer/1034212252780.html, Matching Family Dress, Matching Family Dresses, Matching Family Outfits, Mom Size M, Mom Size S, Mommy and Me, Mother Dress, Mother M, Mother S, Powder Blue, Resort, Ruffle, Scalloped, Sleeveless Dress, Summer, Summer Dresses, Summer Matching Outfit, Sundresses, Vacation, White, Wide-Leg Pants`

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
- If Shopify exposes writable standard metafields for `fit`, `pants-length-type`, or `waist-rise` in this store later, extend the runner to write the already-inferred outfit-set attributes too.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-pblu-powder-blue-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/powder-blue-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/powder-blue-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-powder-blue-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-powder-blue-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-powder-blue-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/powder-blue-mommy-and-me-set`

## Sources
- Neighbor pricing: `blue-striped-family-matching-set`
- Size metaobject map: `white-lace-mommy-and-me-dresses`
