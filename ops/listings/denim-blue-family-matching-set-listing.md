# Denim Blue Family Matching Set - Short-Sleeve Shirt and Shorts

**Status:** Live (ACTIVE, published to all 5 required sales channels)
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7536707305569
**Live URL:** https://www.dresslikemommy.com/products/denim-blue-family-matching-set
**Product ID:** gid://shopify/Product/7536707305569
**Handle:** denim-blue-family-matching-set
**Vendor (storefront):** dresslikemommy.com
**Vendor source URL (tags only):** https://detail.1688.com/offer/708209996925.html

## Title & SEO
- **Title (62/70):** Denim Blue Family Matching Set - Short-Sleeve Shirt and Shorts
- **SEO title (52/60):** Denim Shirt and Shorts Family Set | Dress Like Mommy
- **SEO description (133/155):** Relaxed denim family matching shirt-and-shorts set for moms, dads, girls and boys. Sizes Child 1-2Y-8Y and Adult S-3XL in denim blue.

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child | $28.99 | $33.99 |
| Adult | $31.99 | $36.99 |

## Vendor source-of-truth
- Direct HTTP fetch of `https://detail.1688.com/offer/708209996925.html` returned 1688 anti-bot/login markup, so the attached size chart plus supplied product images were treated as the authoritative source of truth.
- **Product info recovered from the attached screenshot:** vendor item `23B007`, fabric `牛仔` (Denim), color `牛仔蓝` (Denim Blue).
- **Size-chart source of truth:** the attached size-chart screenshot. All 13 vendor rows were transcribed directly from that image.
- **Chart columns preserved from the source:** Size, Garment Length, Chest*2, Shoulder, Pant/Short Length, Waist*2, Rise/Crotch Depth, Recommended Height, Recommended Weight.
- `chest_cm` values were derived by doubling the source `胸围*2` column to full circumference.
- `waist_cm` values were derived by doubling the source `腰围*2` column to full circumference.
- `hip_cm` was derived because the vendor chart omits hip:
  child rows use `hip = chest + 4`; adult rows use `hip = chest`.
- `rise_cm` from the vendor `档深` column is preserved in the saved size-chart JSON for rerun continuity but intentionally omitted from the shopper table so the storefront keeps the standard 10-column contract.
- Adult height guidance was backfilled from the attached fit report plus the live family-set grading curve because the source chart only publishes adult weight bands.
- Fit report preserved from the screenshot:
- Boy: 115 cm / 40 jin tried `120` - Loose fit
- Girl: 113 cm / 35 jin tried `120` - Loose fit
- Mom: 164 cm / 88 jin tried `S` - Loose fit
- Dad: 182 cm / 146 jin tried `3XL` - Loose fit
- Care guidance in the body copy is a conservative inference because the blocked vendor page did not expose wash instructions.
- Product media used for upload:
- `/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set/look-1.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set/look-2.png`

## SIZE_CHART recap
| Vendor row | Picker label | SKU | Price | shopify.size GID |
|---|---|---|---|---|
| 80 | Child 1-2 Years | DLM-DNBL-KID-KID12Y-DENIM | $28.99 | gid://shopify/Metaobject/129972797537 (12-18 months) |
| 90 | Child 2 Years | DLM-DNBL-KID-KID2Y-DENIM | $28.99 | gid://shopify/Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years | DLM-DNBL-KID-KID3Y-DENIM | $28.99 | gid://shopify/Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years | DLM-DNBL-KID-KID4Y-DENIM | $28.99 | gid://shopify/Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years | DLM-DNBL-KID-KID5Y-DENIM | $28.99 | gid://shopify/Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years | DLM-DNBL-KID-KID67Y-DENIM | $28.99 | gid://shopify/Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years | DLM-DNBL-KID-KID8Y-DENIM | $28.99 | gid://shopify/Metaobject/129973026913 (8) |
| S | Adult S | DLM-DNBL-ADT-S-DENIM | $31.99 | gid://shopify/Metaobject/129975255137 (S) |
| M | Adult M | DLM-DNBL-ADT-M-DENIM | $31.99 | gid://shopify/Metaobject/129975222369 (M) |
| L | Adult L | DLM-DNBL-ADT-L-DENIM | $31.99 | gid://shopify/Metaobject/129975189601 (L) |
| XL | Adult XL | DLM-DNBL-ADT-XL-DENIM | $31.99 | gid://shopify/Metaobject/129975287905 (XL) |
| XXL | Adult 2XL | DLM-DNBL-ADT-2XL-DENIM | $31.99 | gid://shopify/Metaobject/129975156833 (2XL) |
| 3XL | Adult 3XL | DLM-DNBL-ADT-3XL-DENIM | $31.99 | gid://shopify/Metaobject/139840421985 (3XL) |

## Notes on mapping
- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the live listing uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.
- `80` maps to `Child 1-2 Years` and uses the closest honest live `shopify.size` metaobject `12-18 months`.
- `XXL` maps to `Adult 2XL` so the live picker stays consistent with the store's standard adult size naming.
- The attached fit report confirms the set wears loosely on both kids and adults, supporting the relaxed merchandising copy.
- Price pattern was anchored to the live family-set neighbor `trail-plaid-family-matching-set`, preserving the current family-set ladder `28.99 / 31.99`.

## Tags written
`Adult 2XL, Adult 3XL, Adult L, Adult M, Adult S, Adult XL, Blue, Button-Up Shirt, Child 1-2 Years, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Contrast Stitch, Daddy and Me, Denim, Denim Blue, Family Matching, Family Photos, Matching Family Outfits, Matching Family Set, Matching Shorts, Mommy and Me, Relaxed Fit, Sets, Shirt and Shorts Set, Short Sleeve Shirt, Summer Family Matching Set, Vacation, https://detail.1688.com/offer/708209996925.html`

## Metafields written
- custom.category1 = `Family Matching`
- custom.subcategory = `Set`
- custom.subcategory2 = `Summer Family Matching Set`
- custom.pattern = `Denim Blue`
- custom.style = `Matching Family Set`
- custom.type = `Two-Piece Set`
- mm-google-shopping.custom_product = `false`
- mm-google-shopping.gender = `unisex`
- mm-google-shopping.age_group = `adult`
- mm-google-shopping.condition = `new`
- mm-google-shopping.custom_label_0 = `Family Matching`
- mm-google-shopping.custom_label_1 = `Denim Blue`
- mm-google-shopping.custom_label_2 = `Summer`
- mm-google-shopping.custom_label_3 = `Short-Sleeve Shirt and Shorts`
- mm-google-shopping.custom_label_4 = `Unisex Family Set`
- shopify.age-group -> `Kids`, `Adults`
- shopify.color-pattern -> `Blue`
- shopify.fabric -> `Denim`
- shopify.size -> 13 catalog metaobject references in chart order
- shopify.target-gender -> `Unisex`
- global.title_tag = SEO title
- global.description_tag = SEO description

## Metafields skipped
- `shopify.clothing-features` - No honest standard clothing-features entry is needed for this denim shirt-and-shorts set.
- `shopify.fit` - The Outfit Sets taxonomy exposes fit, but no reliable writable standard Shopify metafield definition is available in this store.
- `shopify.neckline` - Not written because this is an Outfit Sets listing, not a neckline-specific dress or top listing.
- `shopify.sleeve-length-type` - Not written because the vendor chart does not publish sleeve length and the Outfit Sets subtype is stricter than the photo evidence alone.
- `shopify.skirt-dress-length-type` - Not written because the product is a shirt-and-shorts set, not a skirt or dress listing.
- `shopify.dress-occasion` - Not applicable because the honest taxonomy is Outfit Sets.
- `shopify.dress-style` - Not applicable because the honest taxonomy is Outfit Sets.

## Phase 6 verification
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | PASS | 62 |
| SEO title <= 60 chars | PASS | 52 |
| SEO description <= 155 chars | PASS | 133 |
| Product options are Size / Color | PASS | Size, Color |
| Live variant count matches SIZE_CHART | PASS | 13 vs 13 |
| Live SKUs match derived SKUs | PASS | match |
| Every variant tracked + DENY + priced | PASS | all variants verified |
| Published to all required channels | PASS | all 5 target publications live |
| publishedAt not null | PASS | 2026-04-24T04:28:42Z |
| onlineStoreUrl populated | PASS | https://www.dresslikemommy.com/products/denim-blue-family-matching-set |
| Taxonomy category set | PASS | gid://shopify/TaxonomyCategory/aa-1-11 |
| Size-chart table has 10 columns | PASS | 10 |
| Size-chart table row count matches SIZE_CHART | PASS | 13 |
| Picker labels match first size-table column | PASS | exact order match |
| Size-chart cells use one unit at a time | PASS | no slash-separated values in table cells |
| Required tags present | PASS | all required tags present |
| Applicable metafields written | PASS | all expected metafields present |

## Sales channels published
- Online Store - `gid://shopify/Publication/55169925` (2026-04-24T04:28:42Z)
- Google & YouTube - `gid://shopify/Publication/21969633377` (2026-04-24T04:28:42Z)
- Facebook & Instagram - `gid://shopify/Publication/29172400225` (2026-04-24T04:28:42Z)
- Pinterest - `gid://shopify/Publication/76582879329` (2026-04-24T04:28:42Z)
- TikTok - `gid://shopify/Publication/76604768353` (2026-04-24T04:28:42Z)

## Smart collections
- New Mommy & Me (`/new-matching-outfits`)
- Family Matching Outfits (`/new-women-outfits`)
- Matching Daddy and Me Outfits (`/daddy-and-me`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Popular Family Matching Outfits (`/popular-family-matching`)
- Daddy & Me Matching Outfits (`/daddy-me`)
- Family Matching Sets (`/family-sets`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Manual follow-ups
- Inventory quantities and per-variant grams remain unset / zero and still need operator stock values.
- If the vendor page becomes directly readable later, confirm whether the set includes any extra inner layer beyond the denim shirt and shorts; the current copy assumes the white tee shown in the photos is styling only.
- If later source material exposes a direct hip or fabric-composition spec beyond plain denim, replace the derived hip values or broadened fabric copy with the exact vendor evidence.

## Files
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-denim-blue-family-matching-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-denim-blue-family-matching-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-denim-blue-family-matching-set.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-dnbl-denim-blue-family-matching-set.sh`
