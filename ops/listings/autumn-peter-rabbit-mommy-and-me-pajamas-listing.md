# Autumn Peter Rabbit Mommy and Me Pajamas — Listing Record

**Product ID:** `gid://shopify/Product/7533454098529`
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533454098529
**Live URL:** https://www.dresslikemommy.com/products/autumn-peter-rabbit-mommy-and-me-pajamas
**Handle:** `autumn-peter-rabbit-mommy-and-me-pajamas`
**Status:** ACTIVE, published 2026-04-21

## Vendor Source

- URL: https://detail.1688.com/offer/828526529351.html
- Vendor title: 四层家居服 (4-layer home wear / 4-layer cotton gauze pajamas)
- Fabric: 4-layer cotton gauze (muslin)
- **Vendor fetch fallback used:** 1688 page returned a captcha-locked body. Per the prompt's vendor-fetch fallback rule, I treated the user-attached 尺码参数 screenshot as authoritative and parsed the child 90–150 and adult XS–XXL tables from it.

## Size Chart Derivation

- Vendor columns parsed: `尺码` / `1/2胸围` / `1/2腰围` / `衣长` / `肩宽` / `袖长` / `裤长` / `1/2臀围`. All half-girth columns were doubled to full circumference for `chest_cm`, `waist_cm`, and `hip_cm`.
- Vendor provides full kid range (90, 100, 110, 120, 130, 140, 150) — mapped 1:1 to the seven kid picker labels.
- Vendor sells adult XS, S, M, L, XL, XXL. The store's `child+mother` scheme only defines S–XL, so **XS and XXL were intentionally excluded** (store scheme does not map them). This is documented here per the "Emit only sizes the vendor actually sells" + store scheme constraint: the intersection of vendor availability and store scheme is S/M/L/XL.
- Kid weight bands were inferred from the standard CN children's chart by height band (vendor provides no weight column). Each weight is presented dual-unit.
- Kid weight inference: 90 → 12–14 kg, 100 → 14–16 kg, 110 → 16–19 kg, 120 → 19–22 kg, 130 → 22–27 kg, 140 → 27–32 kg, 150 → 32–38 kg.
- Adult weight/height bands inferred from the vendor's 试穿建议 notes (身高186cm/体重180斤 XXL, 身高181cm/体重120斤 XXL loose, 身高175cm/体重135斤 XL, 身高171cm/体重150斤 XL) back-calculated to women's S–XL fit ranges.
- Waist values are all vendor-supplied (`1/2腰围` doubled); no derivation fallback was needed.

## SIZE_CHART recap

| Vendor | Picker | SKU | Price | Compare-at | shopify.size GID |
|---|---|---|---|---|---|
| 90  | Child 2 Years     | DLM-VCF-KID2Y-CREAM   | $35.99 | $40.24 | 129972863073 (2-3 years) |
| 100 | Child 3 Years     | DLM-VCF-KID3Y-CREAM   | $35.99 | $40.24 | 129972895841 (3-4 years) |
| 110 | Child 4 Years     | DLM-VCF-KID4Y-CREAM   | $35.99 | $40.24 | 129972928609 (4-5 years) |
| 120 | Child 5 Years     | DLM-VCF-KID5Y-CREAM   | $35.99 | $40.24 | 129972961377 (5-6 years) |
| 130 | Child 6-7 Years   | DLM-VCF-KID67Y-CREAM  | $35.99 | $40.24 | 139840323681 (6-7 years) |
| 140 | Child 8 Years     | DLM-VCF-KID8Y-CREAM   | $35.99 | $40.24 | 139840356449 (7-8 years) |
| 150 | Child 9-10 Years  | DLM-VCF-KID910Y-CREAM | $35.99 | $40.24 | 139840389217 (8-9 years — closest; 9-10 not in catalog) |
| S   | Mother S          | DLM-VCF-MOMS-CREAM    | $39.99 | $45.99 | 129975255137 (S) |
| M   | Mother M          | DLM-VCF-MOMM-CREAM    | $39.99 | $45.99 | 129975222369 (M) |
| L   | Mother L          | DLM-VCF-MOML-CREAM    | $39.99 | $45.99 | 129975189601 (L) |
| XL  | Mother XL         | DLM-VCF-MOMXL-CREAM   | $39.99 | $45.99 | 129975287905 (XL) |

## Metafields Written (22)

- `custom.category1` = "Mommy and Me"
- `custom.subcategory` = "Pajamas"
- `custom.subcategory2` = "Fall Pajamas"
- `custom.pattern` = "Autumn Peter Rabbit"
- `custom.style` = "Matching Family Set"
- `custom.type` = "Two-Piece Pajama Set"
- `mm-google-shopping.custom_product` = false
- `mm-google-shopping.gender` = "female"
- `mm-google-shopping.age_group` = "adult"
- `mm-google-shopping.condition` = "new"
- `mm-google-shopping.custom_label_0..4` = Mommy and Me / Peter Rabbit / Fall / Short-Sleeve Set / Family Matching
- `shopify.age-group` = [Kids, Adults]
- `shopify.color-pattern` = [Beige, Floral, Multicolor]
- `shopify.fabric` = [Cotton]
- `shopify.size` = 11 GIDs (1 per kid picker label + Mother S/M/L/XL)
- `shopify.target-gender` = [Female]
- `global.title_tag` = SEO title
- `global.description_tag` = SEO description

## Metafields Skipped — with reason

- `shopify.clothing-features` — skipped. The store's catalog entries don't include a truthful match for this summer cotton-gauze set (the closest catalog entries like "Insulated" or "Waterproof" don't apply). Per the skip rule, omit rather than fake.
- `shopify.sleeve-length-type` — skipped. Prompt rule: "omit for Pajamas, Swimsuits, Bottoms."
- `shopify.neckline` — skipped. Dresses/Tops only; not applicable to Pajamas.
- `shopify.dress-occasion` / `shopify.dress-style` / `shopify.skirt-dress-length-type` — skipped. Dresses only.

## Tags (25)

Autumn, Beige, Bunny, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cotton Gauze, Cream, Fall, Floral, Matching Family Pajamas, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Muslin, Pajamas, Peter Rabbit, Rabbit, Short Sleeve Pajamas, Woodland, https://detail.1688.com/offer/828526529351.html

## Verify (post-create)

- Title 59 / 70 ✓
- SEO title 50 / 60 ✓
- SEO description 132 / 155 ✓
- Live variant count 11 == SIZE_CHART length 11 ✓
- Live SKUs sorted == derived SKUs sorted ✓
- Body `<table id="size-chart">` → 10 `<th>`, 11 data `<tr>` rows + 1 header ✓
- Waist column populated for every row (dual unit) ✓
- Every variant: tracked=true, requiresShipping=true, inventoryPolicy=DENY, price + compareAtPrice present ✓
- publishedAt = 2026-04-21T21:22:37Z; onlineStoreUrl populated ✓
- Taxonomy category = `aa-1-17-4` (Pajamas) ✓
- Published to: Online Store, Google & YouTube, Facebook & Instagram, Pinterest, TikTok ✓

## Manual follow-ups

- **Images:** `/Users/fsuels/Projects/dresslikemommy/uploads/autumn-peter-rabbit-mommy-and-me-pajamas/` doesn't exist yet. Drop vendor photos into that folder then re-run the `media upload` block of the runner (it's idempotent) or attach in Admin.
- **Weights (g):** variant weights not yet set. Recommend 260 g kids / 480 g adults for shipping calc.
- **Inventory qty:** all variants currently 0 on-hand. Seed once stock ships.
- **Smart collection reindex:** collections returned empty at create time — this is normal. Expect 15–60 min for Shopify's smart-collection reindex to pick up matching tag/metafield rules.
- **Additional designs:** The DESIGNS_TO_LIST input also names "Polar adventure - adult edition" and "Red panda-adult." Those are separate SKUs/products (different prints) and need their own listings — not included here.
- **GARMENT_HOOK note:** user supplied "Short-Sleeve Set" but vendor product and photos are long-sleeve 4-layer cotton gauze. Followed input verbatim per the "edit these 9 lines only" contract; flag for review if the hook should read "Long-Sleeve Set."
