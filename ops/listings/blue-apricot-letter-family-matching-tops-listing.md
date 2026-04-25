# Blue Apricot Letter Family Matching Tops - Raglan Tee

**Status:** Live (ACTIVE, published to all 5 required sales channels)
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7536982163553
**Live URL:** https://www.dresslikemommy.com/products/blue-apricot-letter-family-matching-tops
**Product ID:** gid://shopify/Product/7536982163553
**Handle:** blue-apricot-letter-family-matching-tops
**Vendor (storefront):** dresslikemommy.com
**Vendor source URL (tags only):** https://detail.1688.com/offer/899442174086.html?

## Request resolution
| Input | Resolved |
|---|---|
| LISTING_MODE | Family Matching |
| PRIMARY_CATEGORY | Tops -> T-Shirts taxonomy leaf (live taxonomy correction) |
| Variant model | Size / Color with `Child ...` and `Adult ...` labels |
| FORCE_SPEC_PRICES | true |

## Title & SEO
- **Title (53/70):** Blue Apricot Letter Family Matching Tops - Raglan Tee
- **SEO title (43/60):** Blue Apricot Family Tops | Dress Like Mommy
- **SEO description (113/155):** Soft knit family matching raglan tops for parents and kids. Sizes Child 2Y-9-10Y and Adult S-5XL in blue apricot.

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child | $24.99 | $28.99 |
| Adult | $28.99 | $33.99 |

## Vendor source-of-truth
- Direct HTTP fetch of `https://detail.1688.com/offer/899442174086.html?` returned 1688 anti-bot/login markup, so the attached size chart plus supplied product images were treated as the authoritative source of truth.
- **Photo-only fabric/color evidence:** The direct vendor page was not readable from this shell; fabric is described only as soft knit tee fabric from the supplied photos, with no exact fiber claim. The fabric copy is `Soft knit tee fabric` and the color story is `Blue Apricot`.
- **Size-chart source of truth:** the attached size-chart screenshot. The supported top rows were transcribed from the child and adult top tables.
- **Rows excluded from variants:** `73爬服` and `80爬服` were excluded because they are romper/crawler rows, while this request is for Tops.
- **Chart columns preserved from the source:** Size, Garment Length, Chest, Shoulder, Sleeve, Recommended Height, Recommended Weight.
- Source `推荐体重` values are shown as domestic jin ranges in the image and were converted to kg for the shopper-facing table.
- `hip_cm` and `waist_cm` were derived because the vendor chart omits both values:
  child rows use `hip = chest + 4` and `waist = chest`; adult rows use `hip = chest` and `waist = chest - 12`.
- Sleeve values are direct from the vendor chart. Pant/short cells are rendered as `—` because this listing covers tops only.
- Care guidance in the body copy is a conservative inference because the blocked vendor page did not expose wash instructions.
- Product media used for upload:
- `/Users/fsuels/Projects/dresslikemommy/uploads/blue-apricot-letter-family-matching-tops/look-1.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/blue-apricot-letter-family-matching-tops/look-2.png`

## SIZE_CHART recap
| Vendor row | Picker label | SKU | Price | shopify.size GID |
|---|---|---|---|---|
| 90 | Child 2 Years | DLM-BAPL-KID-KID2Y-BLUE | $24.99 | gid://shopify/Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years | DLM-BAPL-KID-KID3Y-BLUE | $24.99 | gid://shopify/Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years | DLM-BAPL-KID-KID4Y-BLUE | $24.99 | gid://shopify/Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years | DLM-BAPL-KID-KID5Y-BLUE | $24.99 | gid://shopify/Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years | DLM-BAPL-KID-KID67Y-BLUE | $24.99 | gid://shopify/Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years | DLM-BAPL-KID-KID8Y-BLUE | $24.99 | gid://shopify/Metaobject/129973026913 (8) |
| 150 | Child 9-10 Years | DLM-BAPL-KID-KID910Y-BLUE | $24.99 | gid://shopify/Metaobject/129971552353 (10) |
| S/160 | Adult S | DLM-BAPL-ADT-S-BLUE | $28.99 | gid://shopify/Metaobject/129975255137 (S) |
| M/165 | Adult M | DLM-BAPL-ADT-M-BLUE | $28.99 | gid://shopify/Metaobject/129975222369 (M) |
| L/170 | Adult L | DLM-BAPL-ADT-L-BLUE | $28.99 | gid://shopify/Metaobject/129975189601 (L) |
| XL/175 | Adult XL | DLM-BAPL-ADT-XL-BLUE | $28.99 | gid://shopify/Metaobject/129975287905 (XL) |
| 2XL/180 | Adult 2XL | DLM-BAPL-ADT-2XL-BLUE | $28.99 | gid://shopify/Metaobject/129975156833 (2XL) |
| 3XL/185 | Adult 3XL | DLM-BAPL-ADT-3XL-BLUE | $28.99 | gid://shopify/Metaobject/139840421985 (3XL) |
| 4XL/190 | Adult 4XL | DLM-BAPL-ADT-4XL-BLUE | $28.99 | gid://shopify/Metaobject/139840716897 (4XL) |
| 5XL/195 | Adult 5XL | DLM-BAPL-ADT-5XL-BLUE | $28.99 |  (no catalog match) |

## Notes on mapping
- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the live listing uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.
- The supplied photos show short-sleeve raglan tops with denim bottoms. Because the chart only measures the tops, the shorts, jeans, cap, bag, and shoes are treated as styling only and are not listed as included pieces.
- `150` maps to `Child 9-10 Years` and uses the closest honest live `shopify.size` metaobject label `10`.
- Adult `2XL/180` through `5XL/195` were kept because the vendor chart explicitly publishes them.
- `Adult 5XL` has no live `shopify--size` metaobject match, so the variant is live but omitted from the product-level `shopify.size` reference list.
- Price pattern uses the canonical Tops fallback matrix because no reliable modern Family Matching Tops neighbor matched this source; child variants are `24.99` and adult variants are `28.99`.

## Tags written
`Adult 2XL, Adult 3XL, Adult 4XL, Adult 5XL, Adult L, Adult M, Adult S, Adult XL, Apricot, Blue, Blue Apricot Letter, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Daddy and Me, Family Matching, Family Photos, Heart Graphic, Letter Graphic, Matching Family Outfits, Matching Family T-Shirts, Matching Family Tops, Mommy and Me, Navy Sleeves, Raglan Tee, Red, Short Sleeve Top, Summer, T-Shirts, Tops, Vacation, https://detail.1688.com/offer/899442174086.html?`

## Metafields written
- custom.category1 = `Family Matching`
- custom.subcategory = `Tops`
- custom.subcategory2 = `Matching Family T-Shirts`
- custom.pattern = `Blue Apricot Letter`
- custom.style = `Raglan Letter Tee`
- custom.type = `Top`
- mm-google-shopping.custom_product = `false`
- mm-google-shopping.gender = `unisex`
- mm-google-shopping.age_group = `adult`
- mm-google-shopping.condition = `new`
- mm-google-shopping.custom_label_0 = `Family Matching`
- mm-google-shopping.custom_label_1 = `Blue Apricot Letter`
- mm-google-shopping.custom_label_2 = `Summer`
- mm-google-shopping.custom_label_3 = `Raglan Letter Tee`
- mm-google-shopping.custom_label_4 = `Unisex Family Top`
- shopify.age-group -> `Kids`, `Adults`
- shopify.color-pattern -> `Blue`, `Beige`, `Red`
- shopify.size -> 14 catalog metaobject references in chart order; Adult 5XL has no catalog match and is skipped in the metafield only
- shopify.target-gender -> `Unisex`
- global.title_tag = SEO title
- global.description_tag = SEO description

## Metafields skipped
- `shopify.clothing-features` - No honest standard clothing-features entry is needed for this blue apricot family top.
- `shopify.fit` - A reliable writable standard Shopify fit metafield definition was not available in this store for this top taxonomy.
- `shopify.fabric` - Not written because the source supports only a soft knit tee appearance, not an exact fiber metaobject.
- `shopify.neckline` - Not written because the photos show contrast crew trim, but no verified standard catalog GID was confirmed in this store.
- `shopify.sleeve-length-type` - Not written because the product is short sleeved, but no verified standard Shopify metaobject GID for that value was confirmed in this store.
- `shopify.top-length-type` - Not written because the chart provides garment length but not enough evidence to map this top to one precise standard top-length metaobject.
- `shopify.size Adult 5XL` - The Adult 5XL variant was kept because the vendor chart publishes it, but this store has no honest 5XL size metaobject to reference.
- `shopify.skirt-dress-length-type` - Not applicable because the honest taxonomy is Clothing Tops > T-Shirts.
- `shopify.dress-occasion` - Not applicable because the honest taxonomy is Clothing Tops > T-Shirts.
- `shopify.dress-style` - Not applicable because the honest taxonomy is Clothing Tops > T-Shirts.

## Phase 6 verification
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | PASS | 53 |
| SEO title <= 60 chars | PASS | 43 |
| SEO description <= 155 chars | PASS | 113 |
| Product options are Size / Color | PASS | Size, Color |
| Live variant count matches SIZE_CHART | PASS | 15 vs 15 |
| Live SKUs match derived SKUs | PASS | match |
| Every variant tracked + DENY + priced | PASS | all variants verified |
| Published to all required channels | PASS | all 5 target publications live |
| publishedAt not null | PASS | 2026-04-24T13:30:20Z |
| onlineStoreUrl populated | PASS | https://www.dresslikemommy.com/products/blue-apricot-letter-family-matching-tops |
| Taxonomy category set | PASS | gid://shopify/TaxonomyCategory/aa-1-13-8 |
| Size-chart table has 10 columns | PASS | 10 |
| Size-chart table row count matches SIZE_CHART | PASS | 15 |
| Picker labels match first size-table column | PASS | exact order match |
| Size-chart cells use one unit at a time | PASS | no slash-separated values in table cells |
| Required tags present | PASS | all required tags present |
| Applicable metafields written | PASS | all expected metafields present |

## Sales channels published
- Online Store - `gid://shopify/Publication/55169925` (2026-04-24T13:30:20Z)
- Google & YouTube - `gid://shopify/Publication/21969633377` (2026-04-24T13:30:20Z)
- Facebook & Instagram - `gid://shopify/Publication/29172400225` (2026-04-24T13:30:20Z)
- Pinterest - `gid://shopify/Publication/76582879329` (2026-04-24T13:30:20Z)
- TikTok - `gid://shopify/Publication/76604768353` (2026-04-24T13:30:20Z)

## Smart collections
- Tops (`/tops`)
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Family Matching Outfits (`/new-women-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Popular Family Matching Outfits (`/popular-family-matching`)
- Family Matching Tops (`/family-tops`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Manual follow-ups
- Inventory quantities and per-variant grams remain unset / zero and still need operator stock values.
- If the vendor page becomes directly readable later, confirm whether the offer is truly top-only or includes any extra coordinated pieces; the current copy assumes the white tee and jeans shown in the photos are styling only.
- If later source material exposes direct waist, hip, or exact fabric-composition specs, replace the current derived fields or broad soft-knit copy with the exact vendor evidence.

## Files
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blue-apricot-letter-family-matching-tops-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/blue-apricot-letter-family-matching-tops-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-blue-apricot-letter-family-matching-tops.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-blue-apricot-letter-family-matching-tops.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-blue-apricot-letter-family-matching-tops.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-bapl-blue-apricot-letter-family-matching-tops.sh`
