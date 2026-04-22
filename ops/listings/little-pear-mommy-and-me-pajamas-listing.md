# Little Pear Mommy and Me Pajamas — Short-Sleeve Set

- **Handle:** `little-pear-mommy-and-me-pajamas`
- **Product ID:** `gid://shopify/Product/7533404291169`
- **Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533404291169
- **Live URL:** https://www.dresslikemommy.com/products/little-pear-mommy-and-me-pajamas
- **Vendor source:** https://detail.1688.com/offer/920493992812.html (design: 鸭梨小圆 — "Little Round Pear")
- **Category:** Pajamas (Matching Family Pajamas / Two-Piece Pajama Set)
- **Season:** Summer 2026
- **Fabric:** 100% cotton knit, thin/breathable (vendor attrs: 主面料成分=棉, 面料名称=针织, 厚薄=薄款, 适合季节=夏季)
- **Pricing:** Child $26.99 (compare $31.99) · Mother $32.99 (compare $37.99)

## Vendor → Picker mapping decisions

Vendor 鸭梨小圆 comes in both 成人款 (Adult S/M/L/XL) and 儿童款 (Child 90–150 cm).
Both audiences are listed per `DESIGNS_TO_LIST`. All 11 rows have full 尺码参数
coverage: 衣长, 1/2胸围, 袖长, 1/2臀围, 1/2腰围, 裤长. 1/2 measurements doubled
for full-circumference display.

**Vendor-fetch source:** direct HTTP fetch of `detail.1688.com/offer/920493992812.html`
succeeded (no captcha). Size-chart image attached to the task used as
cross-reference for the authoritative 尺码参数 table.

Kid height band → picker label mapping followed the standard scheme (90→2Y,
100→3Y, 110→4Y, 120→5Y, 130→6–7Y, 140→8Y, 150→9–10Y). Adult letter sizes map
1:1 to Mother S/M/L/XL.

## SIZE_CHART recap

| Audience | Vendor | Picker Label | SKU | Price | shopify.size GID |
|---|---|---|---|---|---|
| child | 90 | Child 2 Years | DLM-VCF-KID2Y-CREAM | $26.99 | 129972863073 (2-3-years) |
| child | 100 | Child 3 Years | DLM-VCF-KID3Y-CREAM | $26.99 | 129972895841 (3-4-years) |
| child | 110 | Child 4 Years | DLM-VCF-KID4Y-CREAM | $26.99 | 129972928609 (4-5-years) |
| child | 120 | Child 5 Years | DLM-VCF-KID5Y-CREAM | $26.99 | 129972961377 (5-6-years) |
| child | 130 | Child 6-7 Years | DLM-VCF-KID67Y-CREAM | $26.99 | 139840323681 (6-7-years) |
| child | 140 | Child 8 Years | DLM-VCF-KID8Y-CREAM | $26.99 | 139840356449 (7-8-years) |
| child | 150 | Child 9-10 Years | DLM-VCF-KID910Y-CREAM | $26.99 | 139840389217 (8-9-years; closest) |
| mother | S | Mother S | DLM-VCF-MOMS-CREAM | $32.99 | 129975255137 |
| mother | M | Mother M | DLM-VCF-MOMM-CREAM | $32.99 | 129975222369 |
| mother | L | Mother L | DLM-VCF-MOML-CREAM | $32.99 | 129975189601 |
| mother | XL | Mother XL | DLM-VCF-MOMXL-CREAM | $32.99 | 129975287905 |

All 11 size metaobject GIDs resolved from the store's live `shopify--size` catalog.

## Metafields written (23)

- custom.category1 = Mommy and Me
- custom.subcategory = Pajamas
- custom.subcategory2 = Summer Pajamas
- custom.pattern = Little Pear cartoon fruit print on cream with sage leaves
- custom.style = Matching Family Set
- custom.type = Two-Piece Pajama Set
- mm-google-shopping.custom_product = false
- mm-google-shopping.google_product_category = Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas
- mm-google-shopping.gender = female
- mm-google-shopping.age_group = adult
- mm-google-shopping.condition = new
- mm-google-shopping.custom_label_0..4 = Mommy and Me / Little Pear / Summer / Short Sleeve / Family Matching
- shopify.age-group = [Kids, Adults]
- shopify.color-pattern = [White, Yellow, Green]
- shopify.fabric = [Cotton]
- shopify.size = 11 GIDs (one per variant)
- shopify.target-gender = [Female]
- global.title_tag / global.description_tag = SEO title + desc

## Metafields skipped (with reason)

- `shopify.clothing-features` — skipped. Catalog entries on this store
  (e.g. "Insulated", "Waterproof") do not honestly describe a summer cotton
  sleep set. Writing a truthy entry would require a Shopify-catalog value that
  matches; none do. Better to omit than fake.
- `shopify.sleeve-length-type` — explicitly omitted for CATEGORY=Pajamas per
  store rules.
- `shopify.neckline` — dresses/tops only, N/A.
- `shopify.dress-occasion`, `shopify.dress-style`, `shopify.skirt-dress-length-type` — dresses only, N/A.

## Publish / visibility

Published to all 5 sales channels:

- Online Store (`Publication/55169925`)
- Google & YouTube (`Publication/21969633377`)
- Facebook & Instagram (`Publication/29172400225`)
- Pinterest (`Publication/76582879329`)
- TikTok (`Publication/76604768353`)

`publishedAt = 2026-04-21T17:14:22Z`, `onlineStoreUrl` populated.

## Verify pass table

| Check | Result |
|---|---|
| Title ≤ 70 chars | ✅ 51 |
| SEO title ≤ 60 chars | ✅ 55 |
| SEO desc ≤ 155 chars | ✅ 127 |
| Live variant count == SIZE_CHART length | ✅ 11 == 11 |
| Live SKUs sorted == derived SKUs sorted | ✅ |
| publishedAt not null | ✅ |
| onlineStoreUrl populated | ✅ |
| Size table <th> columns | ✅ 10 |
| Size table data <tr> rows | ✅ 11 |
| Waist populated every row (cm/in) | ✅ |
| All variants: tracked, DENY, price, compareAtPrice | ✅ |
| Taxonomy category set | ✅ aa-1-17-4 |
| Tags include vendor URL + category + season + colors + prints + child age buckets + mother sizes | ✅ |
| Smart collections appeared | ⚠️ Empty at create time — standard reindex window (5–15 min) |

## Manual follow-ups

- 📸 **Images:** no files at `/Users/fsuels/Projects/dresslikemommy/uploads/little-pear-mommy-and-me-pajamas/` yet. Runner's 5e block is idempotent — drop images there and re-run to attach.
- ⚖️ **Real weight in grams:** vendor declared 150 g (child) / 350 g (adult); already set via `inventoryItem.measurement.weight` in bulk create.
- 📦 **Inventory qty:** not set (tracked, DENY). Add stock per location once PO lands.
- 🔁 **Smart-collection reindex:** Shopify typically repopulates within 5–15 min of publish. Re-check `product.collections` in ~10 min if collection appearance matters for merchandising.

## Files

- `ops/listings/little-pear-mommy-and-me-pajamas-listing.md` (this file)
- `ops/listings/little-pear-mommy-and-me-pajamas-shopify-import.csv`
- `ops/listings/size_chart.json` (single source of truth)
- `ops/listings/body.html` (descriptionHtml as shipped)
- `ops/listings/verify.json` (post-create product query response)
- `ops/scripts/create-vcf-little-pear-pajamas.sh` (runner — idempotent on media block)
