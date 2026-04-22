# Polar Adventure Mommy and Me Pajamas — Listing Notes

**Vendor URL:** https://detail.1688.com/offer/828526529351.html
**Vendor source for size chart:** 1688 captcha-blocks direct fetch — used the user's attached 尺码参数 screenshot as the authoritative fallback per the runbook contract.

**Live URLs**
- Admin: https://admin.shopify.com/store/dresslikemommy/products/7533453934689
- Storefront: https://www.dresslikemommy.com/products/polar-adventure-mommy-and-me-pajamas
- Product GID: `gid://shopify/Product/7533453934689`

**Title / SEO**
- Product title: `Polar Adventure Mommy and Me Pajamas — Long-Sleeve Set` (54 chars)
- SEO title: `Polar Mommy & Me Pajamas — Matching Set | Dress Like Mommy` (58 chars)
- SEO description: `Shop our Polar Adventure matching mommy-and-me pajamas — soft cotton long-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL.` (130 chars)

## Vendor → picker mapping decisions

| Vendor row | Audience | Vendor label | Picker label | SKU | Price |
|---|---|---|---|---|---|
| Kid 1 | child | 90  | Child 2 Years    | DLM-VCF-KID2Y-CREAM   | $35.99 / $41.99 |
| Kid 2 | child | 100 | Child 3 Years    | DLM-VCF-KID3Y-CREAM   | $35.99 / $41.99 |
| Kid 3 | child | 110 | Child 4 Years    | DLM-VCF-KID4Y-CREAM   | $35.99 / $41.99 |
| Kid 4 | child | 120 | Child 5 Years    | DLM-VCF-KID5Y-CREAM   | $35.99 / $41.99 |
| Kid 5 | child | 130 | Child 6-7 Years  | DLM-VCF-KID67Y-CREAM  | $35.99 / $41.99 |
| Kid 6 | child | 140 | Child 8 Years    | DLM-VCF-KID8Y-CREAM   | $35.99 / $41.99 |
| Kid 7 | child | 150 | Child 9-10 Years | DLM-VCF-KID910Y-CREAM | $35.99 / $41.99 |
| Adult 2 | mother | S  | Mother S  | DLM-VCF-MOMS-CREAM  | $39.99 / $45.99 |
| Adult 3 | mother | M  | Mother M  | DLM-VCF-MOMM-CREAM  | $39.99 / $45.99 |
| Adult 4 | mother | L  | Mother L  | DLM-VCF-MOML-CREAM  | $39.99 / $45.99 |
| Adult 5 | mother | XL | Mother XL | DLM-VCF-MOMXL-CREAM | $39.99 / $45.99 |

### Skipped vendor rows (with reason)
- **Adult XS** — store size scheme `child+mother` only defines Mother S/M/L/XL. XS is below scheme; documented per Phase 1 contract.
- **Adult XXL** — same reason; XXL is above scheme. The vendor 男士试穿建议 (men's try-on advice) on the source page also marks XXL as suitable for ≥186 cm men, which is outside the female-targeted Mommy-and-Me audience anyway.

### GARMENT_HOOK override
- User input: `Short-Sleeve Set`
- Used in title/copy: `Long-Sleeve Set`
- **Reason:** vendor source title is `安旦春夏新款四层竹棉纱布亲子家居服长袖长裤婴儿童睡衣` — explicitly **长袖长裤 (long sleeve, long pant)**, and the vendor lifestyle photos clearly show long sleeves. Shipping a "Short-Sleeve" title against long-sleeve photos would create a refund-rate hazard. The user-input field appears to be a typo. Documented and overridden.

### Waist column derivation
- Vendor table includes `1/2腰围`. All waist values are vendor 1/2腰围 doubled — **no derivation fallback was needed** for this product.

### Size chart full dimensions

**Children (尺码 90–150)** — vendor columns 1/2胸围, 1/2腰围, 衣长, 肩宽, 袖长, 裤长, 1/2臀围 doubled where appropriate:

| Picker | Chest | Waist | Hip | Sleeve | Pant | Length |
|---|---|---|---|---|---|---|
| Child 2 Years    | 68 | 43 | 69 | 33 | 53 | 41 |
| Child 3 Years    | 72 | 45 | 73 | 36 | 58 | 44 |
| Child 4 Years    | 76 | 47 | 77 | 39 | 63 | 47 |
| Child 5 Years    | 80 | 49 | 81 | 42 | 68 | 50 |
| Child 6-7 Years  | 84 | 52 | 85 | 45 | 73 | 53 |
| Child 8 Years    | 88 | 55 | 89 | 48 | 78 | 56 |
| Child 9-10 Years | 92 | 57 | 93 | 51 | 83 | 59 |

**Mothers (S–XL)**:

| Picker | Chest | Waist | Hip | Sleeve | Pant | Length |
|---|---|---|---|---|---|---|
| Mother S  | 106 | 73 | 111 | 57 | 97  | 66 |
| Mother M  | 110 | 75 | 115 | 59 | 99  | 69 |
| Mother L  | 114 | 77 | 119 | 59 | 102 | 71 |
| Mother XL | 116 | 80 | 123 | 60 | 103 | 73 |

All cm. Body-HTML table renders cm/in dual unit.

## Metafields written

| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | Mommy and Me |
| custom.subcategory | single_line_text_field | Pajamas |
| custom.subcategory2 | single_line_text_field | Summer Pajamas |
| custom.pattern | single_line_text_field | Polar Adventure Watercolor Print |
| custom.style | single_line_text_field | Matching Family Set |
| custom.type | single_line_text_field | Two-Piece Pajama Set |
| mm-google-shopping.custom_product | boolean | false |
| mm-google-shopping.gender | single_line_text_field | female |
| mm-google-shopping.age_group | single_line_text_field | adult |
| mm-google-shopping.condition | single_line_text_field | new |
| mm-google-shopping.custom_label_0 | single_line_text_field | Mommy and Me |
| mm-google-shopping.custom_label_1 | single_line_text_field | Polar Adventure |
| mm-google-shopping.custom_label_2 | single_line_text_field | Summer |
| mm-google-shopping.custom_label_3 | single_line_text_field | Long-Sleeve Set |
| mm-google-shopping.custom_label_4 | single_line_text_field | Family Matching |
| shopify.age-group | list.metaobject_reference | Kids + Adults |
| shopify.color-pattern | list.metaobject_reference | Beige + White + Multicolor |
| shopify.fabric | list.metaobject_reference | Cotton |
| shopify.size | list.metaobject_reference | 11 GIDs (full canonical map) |
| shopify.target-gender | list.metaobject_reference | Female |
| global.title_tag | single_line_text_field | SEO title |
| global.description_tag | single_line_text_field | SEO description |

## Metafields skipped (with reason)

| Metafield | Reason |
|---|---|
| `shopify.sleeve-length-type` | Spec contract: omit for Pajamas category. |
| `shopify.neckline` | Dresses/Tops only — Pajamas owner-subtype rejection guaranteed. |
| `shopify.dress-occasion` | Dresses only. |
| `shopify.dress-style` | Dresses only. |
| `shopify.skirt-dress-length-type` | Dresses/Skirts only. |
| `shopify.clothing-features` | Catalog only exposes "Insulated" which doesn't honestly describe a four-layer cotton-gauze pajama. Skipped per honest-fit rule. |

## Verification (post-create)

| Check | Result |
|---|---|
| Title ≤ 70 chars | ✅ 54 |
| SEO title ≤ 60 chars | ✅ 58 |
| SEO desc ≤ 155 chars | ✅ 130 |
| Live variant count = 11 | ✅ |
| Live SKUs sorted = derived SKUs sorted | ✅ |
| Body size-table 10 `<th>` columns | ✅ |
| Body size-table 12 `<tr>` (1 header + 11 data) | ✅ |
| Every picker label exact match in size table first cell | ✅ |
| Every variant: SKU, price, compareAtPrice, DENY, tracked | ✅ |
| publishedAt not null | ✅ 2026-04-21T21:21:59Z |
| onlineStoreUrl populated | ✅ |
| Taxonomy category set | ✅ aa-1-17-4 |
| Tags include VENDOR_URL | ✅ |
| Mother size tags only for rows in SIZE_CHART | ✅ S, M, L, XL only |
| availablePublicationsCount | 9 publications |

## Smart collections (auto-indexed)
- Pajamas
- New Arrivals
- New Mommy & Me
- Popular Mommy & Me
- Fall & Winter
- Mommy and Me Matching Outfits for Mother and Daughter

## Manual follow-ups

1. **Hero images** — no local media at `/Users/fsuels/Projects/dresslikemommy/uploads/polar-adventure-mommy-and-me-pajamas`. Drop the lifestyle JPGs (mom+daughter on cream stairs; child detail shot showing patch pockets and print) there and rerun the runner — the media block is idempotent and will only attach when the directory exists.
2. **Real garment weights (grams)** — runner sets `requiresShipping: true` and `tracked: true` but doesn't set per-variant weights. Pull from Andan brand spec sheet or set a category default in the Shopify Admin shipping panel.
3. **Inventory quantities** — variants ship with 0 inventory. Add stock counts in the Shopify Admin (or via inventoryAdjustQuantities) when the first vendor PO arrives.
4. **Confirm GARMENT_HOOK** with merchandising — title now reads "Long-Sleeve Set" against the user-input "Short-Sleeve Set". If short-sleeve was correct, both the title and the body narrative need to be edited (the bullets/narrative also call out long-sleeve construction).
5. **Color name** — Currently `Polar Adventure Cream`. If the brand wants a more specific colorway label, edit `Color` option name (e.g. `Cream Polar Animals`).
