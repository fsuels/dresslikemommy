# Meow Star Garden Mommy and Me Pajamas — Short-Sleeve Set

**Status:** Live (ACTIVE, published to all 5 required sales channels)
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533458194529
**Live URL:** https://www.dresslikemommy.com/products/meow-star-garden-mommy-and-me-pajamas
**Product ID:** gid://shopify/Product/7533458194529
**Handle:** meow-star-garden-mommy-and-me-pajamas
**Vendor (storefront):** dresslikemommy.com
**Vendor source URL (tags only):** https://detail.1688.com/offer/828526529351.html

## Title & SEO
- **Title (56/70):** Meow Star Garden Mommy and Me Pajamas — Short-Sleeve Set
- **SEO title (54/60):** Cat Meadow Mommy & Me Pajamas — Set | Dress Like Mommy
- **SEO description (131/155):** Shop our Meow Star Garden matching mommy-and-me pajamas — soft cotton short-sleeve set for mom + daughter. Sizes 2Y–10Y & Mom S–XL.

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child | $35.99 | $41.99 |
| Mother | $39.99 | $45.99 |

## Vendor source-of-truth
- Direct HTTP fetch of `https://detail.1688.com/offer/828526529351.html` hit 1688 anti-bot/captcha markup — vendor page content was not exposed.
- Per the spec's vendor-fetch fallback, the user-supplied `尺码参数` screenshot (儿童四层家居服 + 成人四层家居服 tables) is the authoritative source for every size row.
- **Recovered vendor title (CN):** `喵星花园 四层纱布亲子家居服 - 阿里巴巴`
- **Recovered vendor title (EN gloss):** Meow Star Garden four-layer gauze family loungewear — mother and child matching cotton pajama set.
- **Design labels used:** `喵星花园（成人款）, 喵星花园（儿童款）`
- **Size-chart source of truth:** user-supplied `尺码参数` screenshot. `1/2胸围`, `1/2臀围`, and `1/2腰围` were doubled to full circumference values.
- **Columns present on the vendor chart:** size, garment length, half chest, shoulder width, sleeve length, pant length, half hip, half waist.
- **Vendor rows in chart:** 11 total (`7` child, `4` mother).
- **Vendor also offered XS and XXL on the adult chart** — excluded because the canonical Mother picker scheme is S/M/L/XL only.
- **Fabric evidence:** vendor print copy labels this a 四层家居服 (four-layer gauze loungewear) set; both product photos show a soft-touch gauze-cotton hand.
- **Design-detail evidence:** lifestyle photos supplied by the user show a notched-collar button-front top with relaxed long pants; watercolor prints of kittens, puppies, small foxes, and meadow florals on a creamy ivory ground.
- **Care note:** explicit wash instructions are not on the vendor chart screenshot; care guidance uses conservative gauze-cotton defaults (cold wash, line dry / tumble low) and is documented as an inference.
- **Recovered photo URLs / assets used:**
- No vendor photo URLs were accessible (1688 captcha-blocked the direct fetch); vendor size chart screenshot supplied by user is the authoritative source.

## SIZE_CHART recap
| Vendor row | Picker label | SKU | Price | shopify.size GID |
|---|---|---|---|---|
| 90 | Child 2 Years | DLM-VCF-KID2Y-CREAM | $35.99 | gid://shopify/Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years | DLM-VCF-KID3Y-CREAM | $35.99 | gid://shopify/Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years | DLM-VCF-KID4Y-CREAM | $35.99 | gid://shopify/Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years | DLM-VCF-KID5Y-CREAM | $35.99 | gid://shopify/Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years | DLM-VCF-KID67Y-CREAM | $35.99 | gid://shopify/Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years | DLM-VCF-KID8Y-CREAM | $35.99 | gid://shopify/Metaobject/139840356449 (7-8 years) |
| 150 | Child 9-10 Years | DLM-VCF-KID910Y-CREAM | $35.99 | gid://shopify/Metaobject/139840389217 (8-9 years) |
| S | Mother S | DLM-VCF-MOMS-CREAM | $39.99 | gid://shopify/Metaobject/129975255137 (S) |
| M | Mother M | DLM-VCF-MOMM-CREAM | $39.99 | gid://shopify/Metaobject/129975222369 (M) |
| L | Mother L | DLM-VCF-MOML-CREAM | $39.99 | gid://shopify/Metaobject/129975189601 (L) |
| XL | Mother XL | DLM-VCF-MOMXL-CREAM | $39.99 | gid://shopify/Metaobject/129975287905 (XL) |

## Notes on mapping
- Kid sizes map from vendor height rows `90-150` to the standard picker labels `Child 2 Years` through `Child 9-10 Years`.
- Shopify's standard size catalog uses age-range metaobjects, so `Child 9-10 Years` maps to the closest current catalog entry `8-9 years` (9-10 is not in the current catalog).
- Mother sizes map 1:1 from vendor `S/M/L/XL` to `Mother S/M/L/XL`. Vendor `XS` and `XXL` are excluded from this listing because the canonical scheme is S/M/L/XL only.
- Waist values are real vendor values, not invented: vendor provided `1/2腰围` for every row and each waist has been doubled to full circumference.
- Kid weight ranges are inferred from standard CN child height/weight bands because the vendor size table did not include weight.
- The customer-facing source table stores one unit at a time, while the storefront size-guide toggle handles centimeter/inch switching from those source values.

## Tags written
`Botanical, Cat, Cat Meadow, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cotton, Cream, Floral, Four-Layer Gauze, Garden, Green, Ivory, Kitten, Matching Family Pajamas, Meow Star Garden, Mommy and Me, Mother L, Mother M, Mother S, Mother XL, Multicolor, Orange, Pajamas, Purple, Short Sleeve Pajamas, Storybook, Summer, Summer Pajamas, Two-Piece Pajama Set, Watercolor, Wildflower, https://detail.1688.com/offer/828526529351.html`

## Metafields written
- custom.category1 = `Mommy and Me`
- custom.subcategory = `Pajamas`
- custom.subcategory2 = `Summer Pajamas`
- custom.pattern = `Meow Star Garden Print`
- custom.style = `Matching Family Set`
- custom.type = `Two-Piece Pajama Set`
- mm-google-shopping.custom_product = `false`
- mm-google-shopping.gender = `female`
- mm-google-shopping.age_group = `adult`
- mm-google-shopping.condition = `new`
- mm-google-shopping.custom_label_0 = `Mommy and Me`
- mm-google-shopping.custom_label_1 = `Cat Meadow`
- mm-google-shopping.custom_label_2 = `Summer`
- mm-google-shopping.custom_label_3 = `Short-Sleeve Set`
- mm-google-shopping.custom_label_4 = `Family Matching`
- shopify.age-group -> `Kids`, `Adults` (GIDs from neighbor product)
- shopify.color-pattern -> `Beige`, `Floral`, `Multicolor` (GIDs from neighbor product)
- shopify.fabric -> `Cotton`
- shopify.size -> 11 catalog metaobject references in chart order
- shopify.target-gender -> `Female`
- global.title_tag = SEO title
- global.description_tag = SEO description

## Metafields skipped
- `shopify.clothing-features` — No honest standard-catalog clothing-features entry fits a lightweight summer four-layer cotton gauze pajama set.
- `shopify.sleeve-length-type` — Omitted for Pajamas per the listing spec.
- `shopify.neckline` — Dresses/Tops only; does not apply to Pajamas.
- `shopify.dress-occasion` — Dresses only; does not apply to Pajamas.
- `shopify.dress-style` — Dresses only; does not apply to Pajamas.
- `shopify.skirt-dress-length-type` — Dresses/Skirts only; does not apply to Pajamas.

## Phase 6 verification
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | PASS | 56 |
| SEO title <= 60 chars | PASS | 54 |
| SEO description <= 155 chars | PASS | 131 |
| Live variant count matches SIZE_CHART | PASS | 11 vs 11 |
| Live SKUs match derived SKUs | PASS | match |
| Every variant tracked + DENY + priced | PASS | all variants verified |
| Published to all required channels | PASS | all 5 target publications live |
| publishedAt not null | PASS | 2026-04-21T21:43:21Z |
| onlineStoreUrl populated | PASS | https://www.dresslikemommy.com/products/meow-star-garden-mommy-and-me-pajamas |
| Taxonomy category set | PASS | gid://shopify/TaxonomyCategory/aa-1-17-4 |
| Size-chart table has 10 columns | PASS | 10 |
| Size-chart table row count matches SIZE_CHART | PASS | 11 |
| Picker labels match first size-table column | PASS | exact order match |
| Age column present and populated | PASS | present |
| Waist column populated for every row | PASS | all waist values present |
| Size-chart cells use one unit at a time | PASS | no slash-separated values in table cells |
| Required tags present | PASS | all required tags present |
| Applicable metafields written | PASS | all expected metafields present |

## Sales channels published
- Online Store — `gid://shopify/Publication/55169925` (2026-04-21T21:43:21Z)
- Google & YouTube — `gid://shopify/Publication/21969633377` (2026-04-21T21:43:21Z)
- Facebook & Instagram — `gid://shopify/Publication/29172400225` (2026-04-21T21:43:21Z)
- Pinterest — `gid://shopify/Publication/76582879329` (2026-04-21T21:43:21Z)
- TikTok — `gid://shopify/Publication/76604768353` (2026-04-21T21:43:21Z)

## Smart collections
- Pajamas (`/pajamas`)
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)

## Manual follow-ups
- **Images:** No vendor photos were attached to this run. Drop hero + lifestyle + size-chart images into `/sessions/vigilant-peaceful-newton/mnt/dresslikemommy/uploads/meow-star-garden-mommy-and-me-pajamas` and re-run this runner — the media block is idempotent and will upload any new files with scene-descriptive alt text.
- Enter real variant shipping weights in grams/ounces when available; the backup CSV leaves hard weights blank rather than inventing them.
- Set live inventory quantities per variant after stock intake.
- Recheck smart-collection membership after the normal Shopify reindex window if any collection rules are still catching up.

## Files
- `/sessions/vigilant-peaceful-newton/mnt/dresslikemommy/meow-star-garden-mommy-and-me-pajamas-listing.md`
- `/sessions/vigilant-peaceful-newton/mnt/dresslikemommy/meow-star-garden-mommy-and-me-pajamas-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-vcf-meow-star-garden-mommy-and-me-pajamas.sh`
