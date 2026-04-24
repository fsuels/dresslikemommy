# Washed Denim Family Matching Vests - Sleeveless Layer

**Status:** Live (ACTIVE, published to all 5 required sales channels)
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7536709664865
**Live URL:** https://www.dresslikemommy.com/products/washed-denim-family-matching-vests
**Product ID:** gid://shopify/Product/7536709664865
**Handle:** washed-denim-family-matching-vests
**Vendor (storefront):** dresslikemommy.com
**Vendor source URL (tags only):** https://detail.1688.com/offer/884415315877.html

## Request resolution
| Input | Resolved |
|---|---|
| LISTING_MODE | Family Matching |
| PRIMARY_CATEGORY | Set -> Outerwear / Vests (deviation: the source chart only supports the vest layer) |
| Variant model | Size / Color with `Child ...` and `Adult ...` labels |
| FORCE_SPEC_PRICES | true |

## Title & SEO
- **Title (53/70):** Washed Denim Family Matching Vests - Sleeveless Layer
- **SEO title (43/60):** Washed Denim Family Vest | Dress Like Mommy
- **SEO description (115/155):** Relaxed washed denim family vest for parents and kids. Sizes Child 1-2Y-9-10Y and Adult S-3XL in a faded blue wash.

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child | $22.99 | $26.99 |
| Adult | $29.99 | $34.99 |

## Vendor source-of-truth
- Direct HTTP fetch of `https://detail.1688.com/offer/884415315877.html` returned 1688 anti-bot/login markup, so the attached size chart plus supplied product images were treated as the authoritative source of truth.
- **Photo-only fabric/color evidence:** No product-info panel was supplied; fabric and color are inferred from the attached family photos only. The published fabric call is `Denim` and the color story is `Washed Denim`.
- **Size-chart source of truth:** the attached size-chart screenshot. All 14 vendor rows were transcribed directly from that image.
- **Chart columns preserved from the source:** Size, Garment Length, Chest*2, Recommended Height, Recommended Weight.
- `chest_cm` values were derived by doubling the source `胸围*2` column to full circumference.
- `hip_cm` and `waist_cm` were derived because the vendor chart omits both values:
  child rows use `hip = chest + 4` and `waist = chest`; adult rows use `hip = chest` and `waist = chest - 12`.
- Sleeve/skirt and pant/short columns are intentionally rendered as `—` in the shopper table because the source chart does not publish those measurements for the vest.
- Adult height guidance was backfilled from the attached fit report plus the live denim family tops curve because the source chart only publishes adult weight bands.
- Fit report preserved from the screenshot:
- Boy: 110 cm / 33 jin tried `110` - Loose fit
- Girl: 113 cm / 37 jin tried `110` - True to size
- Mom: 164 cm / 88 jin tried `S` - Loose fit
- Dad: 183 cm / 156 jin tried `XXL` - Loose fit
- Care guidance in the body copy is a conservative inference because the blocked vendor page did not expose wash instructions.
- Product media used for upload:
- `/Users/fsuels/Projects/dresslikemommy/uploads/washed-denim-family-matching-vests/look-1.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/washed-denim-family-matching-vests/look-2.png`

## SIZE_CHART recap
| Vendor row | Picker label | SKU | Price | shopify.size GID |
|---|---|---|---|---|
| 80 | Child 1-2 Years | DLM-WDNV-KID-KID12Y-DENIM | $22.99 | gid://shopify/Metaobject/129972797537 (12-18 months) |
| 90 | Child 2 Years | DLM-WDNV-KID-KID2Y-DENIM | $22.99 | gid://shopify/Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years | DLM-WDNV-KID-KID3Y-DENIM | $22.99 | gid://shopify/Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years | DLM-WDNV-KID-KID4Y-DENIM | $22.99 | gid://shopify/Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years | DLM-WDNV-KID-KID5Y-DENIM | $22.99 | gid://shopify/Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years | DLM-WDNV-KID-KID67Y-DENIM | $22.99 | gid://shopify/Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years | DLM-WDNV-KID-KID8Y-DENIM | $22.99 | gid://shopify/Metaobject/129973026913 (8) |
| 150 | Child 9-10 Years | DLM-WDNV-KID-KID910Y-DENIM | $22.99 | gid://shopify/Metaobject/129971552353 (10) |
| S | Adult S | DLM-WDNV-ADT-S-DENIM | $29.99 | gid://shopify/Metaobject/129975255137 (S) |
| M | Adult M | DLM-WDNV-ADT-M-DENIM | $29.99 | gid://shopify/Metaobject/129975222369 (M) |
| L | Adult L | DLM-WDNV-ADT-L-DENIM | $29.99 | gid://shopify/Metaobject/129975189601 (L) |
| XL | Adult XL | DLM-WDNV-ADT-XL-DENIM | $29.99 | gid://shopify/Metaobject/129975287905 (XL) |
| XXL | Adult 2XL | DLM-WDNV-ADT-2XL-DENIM | $29.99 | gid://shopify/Metaobject/129975156833 (2XL) |
| 3XL | Adult 3XL | DLM-WDNV-ADT-3XL-DENIM | $29.99 | gid://shopify/Metaobject/139840421985 (3XL) |

## Notes on mapping
- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the live listing uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.
- The supplied photos show a sleeveless washed-denim vest layered over a white long-sleeve tee and wide-leg jeans. Because the chart only measures the vest, the tee and jeans are treated as styling only and are not listed as included pieces.
- `80` maps to `Child 1-2 Years` and uses the closest honest live `shopify.size` metaobject `12-18 months`.
- `150` maps to `Child 9-10 Years` and uses the closest honest live `shopify.size` metaobject label `10`.
- `XXL` maps to `Adult 2XL` so the live picker stays consistent with the store's standard adult size naming.
- The attached fit report confirms a loose fit on the boy, mom, and dad, while the girl tester landed closer to true-to-size.
- Price pattern was anchored to the live denim family-tops neighbor `matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids`, preserving the current denim family tops ladder `22.99 / 29.99`.

## Tags written
`Adult 2XL, Adult 3XL, Adult L, Adult M, Adult S, Adult XL, Blue, Button Front, Child 1-2 Years, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Daddy and Me, Denim, Family Matching, Family Photos, Layering Piece, Matching Family Outfits, Matching Family Vest, Mommy and Me, Outerwear, Relaxed Fit, Sleeveless Vest, Spring, Vests, Washed Denim, https://detail.1688.com/offer/884415315877.html`

## Metafields written
- custom.category1 = `Family Matching`
- custom.subcategory = `Outerwear`
- custom.subcategory2 = `Matching Family Vests`
- custom.pattern = `Washed Denim`
- custom.style = `Family Matching Vest`
- custom.type = `Vest`
- mm-google-shopping.custom_product = `false`
- mm-google-shopping.gender = `unisex`
- mm-google-shopping.age_group = `adult`
- mm-google-shopping.condition = `new`
- mm-google-shopping.custom_label_0 = `Family Matching`
- mm-google-shopping.custom_label_1 = `Washed Denim`
- mm-google-shopping.custom_label_2 = `Spring`
- mm-google-shopping.custom_label_3 = `Sleeveless Denim Vest`
- mm-google-shopping.custom_label_4 = `Unisex Family Vest`
- shopify.age-group -> `Kids`, `Adults`
- shopify.color-pattern -> `Blue`
- shopify.fabric -> `Denim`
- shopify.size -> 14 catalog metaobject references in chart order
- shopify.target-gender -> `Unisex`
- global.title_tag = SEO title
- global.description_tag = SEO description

## Metafields skipped
- `shopify.clothing-features` - No honest standard clothing-features entry is needed for this washed denim family vest.
- `shopify.fit` - A reliable writable standard Shopify fit metafield definition was not available in this store for this vest taxonomy.
- `shopify.neckline` - Not written because the photos suggest a simple collarless neckline, but no verified standard catalog GID was confirmed in this store.
- `shopify.sleeve-length-type` - Not written because the product is sleeveless and no verified standard Shopify metaobject GID for that value was confirmed in this store.
- `shopify.top-length-type` - Not written because the chart provides garment length but not enough evidence to map this vest to one precise standard top-length metaobject.
- `shopify.skirt-dress-length-type` - Not applicable because the honest taxonomy is Outerwear > Vests.
- `shopify.dress-occasion` - Not applicable because the honest taxonomy is Outerwear > Vests.
- `shopify.dress-style` - Not applicable because the honest taxonomy is Outerwear > Vests.

## Phase 6 verification
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | PASS | 53 |
| SEO title <= 60 chars | PASS | 43 |
| SEO description <= 155 chars | PASS | 115 |
| Product options are Size / Color | PASS | Size, Color |
| Live variant count matches SIZE_CHART | PASS | 14 vs 14 |
| Live SKUs match derived SKUs | PASS | match |
| Every variant tracked + DENY + priced | PASS | all variants verified |
| Published to all required channels | PASS | all 5 target publications live |
| publishedAt not null | PASS | 2026-04-24T04:48:01Z |
| onlineStoreUrl populated | PASS | https://www.dresslikemommy.com/products/washed-denim-family-matching-vests |
| Taxonomy category set | PASS | gid://shopify/TaxonomyCategory/aa-1-10-6 |
| Size-chart table has 10 columns | PASS | 10 |
| Size-chart table row count matches SIZE_CHART | PASS | 14 |
| Picker labels match first size-table column | PASS | exact order match |
| Size-chart cells use one unit at a time | PASS | no slash-separated values in table cells |
| Required tags present | PASS | all required tags present |
| Applicable metafields written | PASS | all expected metafields present |

## Sales channels published
- Online Store - `gid://shopify/Publication/55169925` (2026-04-24T04:48:01Z)
- Google & YouTube - `gid://shopify/Publication/21969633377` (2026-04-24T04:48:01Z)
- Facebook & Instagram - `gid://shopify/Publication/29172400225` (2026-04-24T04:48:01Z)
- Pinterest - `gid://shopify/Publication/76582879329` (2026-04-24T04:48:01Z)
- TikTok - `gid://shopify/Publication/76604768353` (2026-04-24T04:48:01Z)

## Smart collections
- New Mommy & Me (`/new-matching-outfits`)
- Family Matching Outfits (`/new-women-outfits`)
- Matching Daddy and Me Outfits (`/daddy-and-me`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Popular Family Matching Outfits (`/popular-family-matching`)
- Daddy & Me Matching Outfits (`/daddy-me`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)

## Manual follow-ups
- Inventory quantities and per-variant grams remain unset / zero and still need operator stock values.
- If the vendor page becomes directly readable later, confirm whether the offer is truly vest-only or includes any extra coordinated pieces; the current copy assumes the white tee and jeans shown in the photos are styling only.
- If later source material exposes direct waist, hip, shoulder, or exact fabric-composition specs, replace the current derived fields or broadened denim copy with the exact vendor evidence.

## Files
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/washed-denim-family-matching-vests-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/washed-denim-family-matching-vests-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-washed-denim-family-matching-vests.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-washed-denim-family-matching-vests.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-washed-denim-family-matching-vests.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-wdnv-washed-denim-family-matching-vests.sh`
