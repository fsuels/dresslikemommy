# Sunshine Stripe Family Matching Tops - Cotton Tee

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7545279512673
- **Live:** not published
- **Vendor source:** https://detail.1688.com/offer/1038879477265.html?
- **Product GID:** `gid://shopify/Product/7545279512673`
- **Handle:** `sunshine-stripe-family-matching-tops`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1038879477265.html? |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Family Matching, merchandised for Mommy and Me and Daddy and Me collection discovery |
| PRIMARY_CATEGORY | Tops / T-Shirts |
| DESIGNS_TO_LIST | auto -> one Sunshine Stripe tee colorway shown in the supplied product image |
| FORCE_SPEC_PRICES | true |
| SHORTCODE | SSTR |
| COLOR_TOKEN | SUNSTR |

## Vendor Fetch Status
Direct 1688 fetch returned Alibaba anti-bot/CAPTCHA punish markup, so the attached product and size-chart images were used as authoritative evidence per the canonical workflow. No source/vendor URL was written to Shopify customer-facing or feed-visible product fields.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Sunshine Stripe Family Matching Tops - Cotton Tee` | 49 |
| SEO title | `Sunshine Stripe Family Tops | Dress Like Mommy` | 46 |
| SEO description | `Cotton-spandex striped family matching tees for mom, dad, girls and boys. Short-sleeve tops in Child 2Y-10Y and Adult S-4XL.` | 124 |

## Pricing
| Audience | Price | Compare-at | Cost |
|---|---:|---:|---:|
| Child | 24.99 | 28.99 | 12.50 |
| Adult | 28.99 | 33.99 | 14.50 |

## SIZE_CHART / Variant Recap
| Role | Vendor | Picker | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---:|---:|---|
| Child Shirt | 90 | Child 2 Years | Sunshine Stripe | `DLM-SSTR-KID-KID2Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Child Shirt | 100 | Child 3 Years | Sunshine Stripe | `DLM-SSTR-KID-KID3Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Child Shirt | 110 | Child 4 Years | Sunshine Stripe | `DLM-SSTR-KID-KID4Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Child Shirt | 120 | Child 5 Years | Sunshine Stripe | `DLM-SSTR-KID-KID5Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Child Shirt | 130 | Child 6-7 Years | Sunshine Stripe | `DLM-SSTR-KID-KID67Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Child Shirt | 140 | Child 8 Years | Sunshine Stripe | `DLM-SSTR-KID-KID8Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129973026913` (8) |
| Child Shirt | 150 | Child 9-10 Years | Sunshine Stripe | `DLM-SSTR-KID-KID910Y-SUNSTR` | 24.99 | 12.50 | `gid://shopify/Metaobject/129971552353` (10) |
| Adult Shirt | S/160 | Adult S | Sunshine Stripe | `DLM-SSTR-ADT-S-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Adult Shirt | M/165 | Adult M | Sunshine Stripe | `DLM-SSTR-ADT-M-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Adult Shirt | L/170 | Adult L | Sunshine Stripe | `DLM-SSTR-ADT-L-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Adult Shirt | XL/175 | Adult XL | Sunshine Stripe | `DLM-SSTR-ADT-XL-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/129975287905` (XL) |
| Adult Shirt | 2XL/180 | Adult 2XL | Sunshine Stripe | `DLM-SSTR-ADT-2XL-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/129975156833` (2XL) |
| Adult Shirt | 3XL/185 | Adult 3XL | Sunshine Stripe | `DLM-SSTR-ADT-3XL-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/139840421985` (3XL) |
| Adult Shirt | 4XL/190 | Adult 4XL | Sunshine Stripe | `DLM-SSTR-ADT-4XL-SUNSTR` | 28.99 | 14.50 | `gid://shopify/Metaobject/139840716897` (4XL) |

## Derivations
- The chart text says `条纹短袖` and the supplied product photo shows one short-sleeve striped tee for children and adults; bottoms and props are styling only.
- The chart states fabric as `95% cotton + 5% spandex`; Shopify fabric writes the verified `Cotton` catalog value, while spandex is retained in body copy and notes because no spandex fabric metaobject was verified.
- Source chest values (`37` through `64`) are flat garment widths despite the screenshot column label reading chest; they were doubled into wearable `chest_cm` values.
- Hip and waist are derived from the canonical top/shirt rules: child top rows use `hip = chest + 4` and `waist = chest`; adult top rows use `hip = chest` and `waist = chest - 12`.
- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy/mom/dad ladders, so the variant picker uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role rows.
- Pricing is anchored to the canonical Tops fallback and nearby family-top pattern: child `24.99`, adult `28.99`; Cost per item is exactly 50%.

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status is DRAFT | PASS | DRAFT |
| publishedAt is null | PASS | None |
| No sales-channel publications live | PASS | [] |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Clothing Tops > T-Shirts |
| Variant count matches SIZE_CHART | PASS | 14 vs 14 |
| Price and cost parity | PASS | 14 variants checked |
| Source URL guard | PASS | no forbidden source tokens in Shopify product fields |
| Size table rows | PASS | 14 |
| Size table headers | PASS | 10 headers |

## Price and Cost Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---:|---:|---:|---:|---:|---:|---|
| `DLM-SSTR-KID-KID2Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID3Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID4Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID5Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID67Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID8Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-KID-KID910Y-SUNSTR` | 24.99 | 28.99 | 12.5 | 24.99 | 28.99 | 12.50 | yes |
| `DLM-SSTR-ADT-S-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-M-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-L-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-XL-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-2XL-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-3XL-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |
| `DLM-SSTR-ADT-4XL-SUNSTR` | 28.99 | 33.99 | 14.5 | 28.99 | 33.99 | 14.50 | yes |

## Metafields Written
- `custom.category1`
- `custom.pattern`
- `custom.style`
- `custom.subcategory`
- `custom.subcategory2`
- `custom.type`
- `global.description_tag`
- `global.title_tag`
- `mc-facebook.google_product_category`
- `mm-google-shopping.age_group`
- `mm-google-shopping.condition`
- `mm-google-shopping.custom_label_0`
- `mm-google-shopping.custom_label_1`
- `mm-google-shopping.custom_label_2`
- `mm-google-shopping.custom_label_3`
- `mm-google-shopping.custom_label_4`
- `mm-google-shopping.custom_product`
- `mm-google-shopping.gender`
- `shopify.age-group`
- `shopify.color-pattern`
- `shopify.fabric`
- `shopify.size`
- `shopify.target-gender`

## Metafields Skipped
- `shopify.sleeve-length-type`: Short sleeve evidence is clear, but two different `Short` catalog values exist in this store; skipped rather than guessing the owner-subtype-safe value.
- `shopify.neckline`: Crew neckline is visible in the supplied product image, but no owner-subtype-safe neckline value was verified for this T-Shirts taxonomy run.
- `shopify.top-length-type`: The vendor chart gives exact garment lengths, but those do not map cleanly to one standard top-length type.
- `shopify.dress-occasion`: Not applicable because the honest taxonomy is T-Shirts.
- `shopify.dress-style`: Not applicable because this is a Tops listing.
- `shopify.skirt-dress-length-type`: Not applicable because this listing contains shirts only.

## Tags Written
`Adult 2XL, Adult 3XL, Adult 4XL, Adult L, Adult M, Adult S, Adult Shirt, Adult XL, Blue, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Child Shirt, Cotton, Cotton Blend, Crew Neck Tee, Daddy and Me, Family Matching, Family Photos, Matching Family Outfits, Matching Family Top, Matching Family Tops, Mommy and Me, Navy, Picnic, Red, Short Sleeve Tee, Spandex, Spring, Stripe, Striped, Striped Shirt, Summer, Sunshine Stripe, Tops, Yellow`

## Smart Collections
- Tops (`/tops`)
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Family Matching Outfits (`/new-women-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Popular Family Matching Outfits (`/popular-family-matching`)
- Family Matching Tops (`/family-tops`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)

## Manual Follow-ups
- Inventory quantities remain unset / zero and need operator stock values before launch.
- If the vendor page becomes directly readable later, confirm any additional product detail-page claims before publishing.
- Review the supplied product image for crop/retouch quality before a publish-live step.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-sstr-sunshine-stripe-family-matching-tops.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/sunshine-stripe-family-matching-tops-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/sunshine-stripe-family-matching-tops-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-sunshine-stripe-family-matching-tops.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-sunshine-stripe-family-matching-tops.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-sunshine-stripe-family-matching-tops.json`
- `/Users/fsuels/Projects/dresslikemommy/uploads/sunshine-stripe-family-matching-tops`
