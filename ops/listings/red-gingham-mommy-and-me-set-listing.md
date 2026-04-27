# Red Gingham Mommy and Me Set - Lace Top & Pants

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7537366597729
- **Live:** not published (`DRAFT`)
- **Vendor:** https://detail.1688.com/offer/1041874678820.html
- **Product GID:** `gid://shopify/Product/7537366597729`
- **Handle:** `red-gingham-mommy-and-me-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1041874678820.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Mommy and Me |
| PRIMARY_CATEGORY | auto -> Sets (Shopify taxonomy kept as Outfit Sets) |
| DESIGNS_TO_LIST | auto -> Red Gingham only |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `RGHM` |
| COLOR_TOKEN | auto -> `RED` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 detail page loaded through the logged-in helper browser during this run. It confirmed a 2026 summer mother-daughter top-and-pants set, cotton/cotton-blend fabric wording, source-factory supplier signals, stock/dropship wording, 12 years on 1688, and 82% repeat-buyer rate. The attached size-chart image was used as the authoritative source of truth for measurements. The detail enrichment scorer marked the lead Reject because it parsed `100+ sold` as MOQ 100 and flagged the vendor brand field; the raw page text shows `1件起批` and the vendor brand is not used customer-facing.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Red Gingham Mommy and Me Separates - Top or Pants` | 50 |
| SEO Title | `Red Gingham Mommy & Me Separates | Dress Like Mommy` | 52 |
| SEO Description | `Mommy-and-me cotton-blend separates: choose the white lace-trim top or red gingham pants for mom + daughter. Sizes 2Y-8Y and Mom M.` | 136 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Set | 90 | Child 2 Years | `DLM-RGHM-GRL-KID2Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Set | 100 | Child 3 Years | `DLM-RGHM-GRL-KID3Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Set | 110 | Child 4 Years | `DLM-RGHM-GRL-KID4Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Set | 120 | Child 5 Years | `DLM-RGHM-GRL-KID5Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Set | 130 | Child 6-7 Years | `DLM-RGHM-GRL-KID67Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Set | 140 | Child 8 Years | `DLM-RGHM-GRL-KID8Y-RED` | 28.99 | 33.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Mother Set | M | Mother M | `DLM-RGHM-MOM-M-RED` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (M) |

### Derivations (flagged per spec)
- The vendor chart labels bust and waist as half measurements (`*2`), so `chest_cm` and `waist_cm` were doubled into full circumference values.
- Child `height` uses the vendor chart exactly; child `weight` was derived from the store's standard size guidance because the vendor chart omits child weight.
- Mother `height` guidance was derived from the store's standard mother size guidance because the vendor chart provides recommended weight only for adult M.
- `hip_cm` was derived as `chest_cm + 4` from the store's loose summer set grading because the vendor chart omits hip.
- The `Sleeve or Skirt` body column is `—` for every row because the top is sleeveless and the product is a pants set, not a skirt set.

### Vendor → picker mapping log
- 90 -> Child 2 Years
- 100 -> Child 3 Years
- 110 -> Child 4 Years
- 120 -> Child 5 Years
- 130 -> Child 6-7 Years
- 140 -> Child 8 Years
- M -> Mother M

### EXCLUDE_ITEMS decisions
- No exclusions were requested, so every vendor-supported mommy-and-me row in the attached chart was kept.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 1 `<h3>` + 1 size table with 10 `<th>` headers and 7 body rows.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Type` → `Top`, `Pants`
- Option 2: `Size` → `Child 2 Years`, `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Mother M`
- Variants live: **14**

### Repair note — 2026-04-25
- Vendor evidence lists `白色上衣` (white top) and `红色格子裤` (red gingham pants) as separate purchasable item choices under the 1688 selector.
- The original Shopify product incorrectly collapsed those choices into one `Set` variant per size using `Size x Color`.
- The live product has been repaired to `Type x Size` so shoppers choose `Top` or `Pants` before choosing size.
- The single-value `Color` option was removed because it was not a real shopper choice.

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Product status | ✅ | `DRAFT` |
| Published state | ✅ | `publishedAt=null`, `onlineStoreUrl=null` |
| Required publications | ✅ | No Online Store, Google & YouTube, Facebook & Instagram, Pinterest, or TikTok publication is live |
| Option axes | ✅ | `Type` / `Size` |
| Type values | ✅ | `Top`, `Pants` |
| Variant count | ✅ | 14 |
| SKU model | ✅ | Every SKU includes `TOP` or `PNT` and matches the `Type x Size` variant |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-RGHM-GRL-KID2Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-GRL-KID3Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-GRL-KID4Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-GRL-KID5Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-GRL-KID67Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-GRL-KID8Y-RED | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-RGHM-MOM-M-RED | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |

## Metafields — written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Mommy and Me` |
| custom.pattern | single_line_text_field | `Red Gingham` |
| custom.style | single_line_text_field | `Lace Top & Gingham Pants` |
| custom.subcategory | single_line_text_field | `Sets` |
| custom.subcategory2 | single_line_text_field | `Summer Matching Sets` |
| custom.type | single_line_text_field | `Two-Piece Set` |
| global.description_tag | single_line_text_field | `Cotton-blend mommy-and-me set with a white lace-trim top and red gingham pants for mom ...` |
| global.title_tag | single_line_text_field | `Red Gingham Mommy & Me Set | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Red Gingham` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Lace Top & Gingham Pants` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Two-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `female` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69600804961","gid://shopify/Metaobject/69639733345","gid://s...` |
| shopify.fabric | list.metaobject_reference | `["gid://shopify/Metaobject/69622399073"]` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972863073","gid://shopify/Metaobject/129972895841","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |
| shopify.top-length-type | list.metaobject_reference | `["gid://shopify/Metaobject/130282553441"]` |

## Metafields — skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The current store catalog only exposes values like `Insulated` in this standard metafield namespace, which would be inaccurate for this lightweight summer outfit set. |
| shopify.dress-occasion | Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`. |
| shopify.dress-style | Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`. |
| shopify.fit | The Outfit Sets taxonomy exposes fit, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.neckline | The images support a round sleeveless neckline, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.pants-length-type | The pants are visibly full length, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.skirt-dress-length-type | Not applicable because this coordinated product pairs a sleeveless top with pants rather than a skirt or dress. |
| shopify.sleeve-length-type | The images support a sleeveless top, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store. |
| shopify.waist-rise | The waistband sits around the natural waist visually, but no writable standard Shopify metafield definition is currently available in this store for that attribute. |

## Tags written (35)
`Beach, category1:Mommy and Me, Checkered, Child 2-3yr, Child 4-5yr, Child 6-8yr, Cotton Blend, Gingham, Girl Pants, Girl Top, https://detail.1688.com/offer/1041874678820.html, Lace Trim, Matching Family Outfits, Matching Family Separates, Matching Family Set, Mom Size M, Mommy and Me, Mother M, Mother Pants, Mother Top, Pants, pattern:Red Gingham, Red, Red Gingham, Sets, Sleeveless Top, style:Lace Top & Gingham Pants, subcategory2:Summer Matching Sets, subcategory:Sets, Summer, Top, type:Two-Piece Separates, Vacation, White, Wide-Leg Pants`

## Publication
- `DRAFT`; not published to Online Store, Google & YouTube, Facebook & Instagram, Pinterest, TikTok, or any other sales channel.

## Smart collections
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Manual follow-ups
- Inventory quantities and per-variant grams still need operator stock values.
- If Shopify exposes writable standard metafields for `fit`, `pants-length-type`, or `waist-rise` in this store later, extend the runner to write the already-inferred outfit-set attributes too.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-rghm-red-gingham-mommy-and-me-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-gingham-mommy-and-me-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/red-gingham-mommy-and-me-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-red-gingham-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-red-gingham-mommy-and-me-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-red-gingham-mommy-and-me-set.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/red-gingham-mommy-and-me-set`

## Sources
- Neighbor pricing: `powder-blue-mommy-and-me-set`
- Size metaobject map: `ivory-ruffle-mommy-and-me-dresses`
