# Magical Travel Notes Mommy and Me Pajamas — Short-Sleeve Set

**Status:** ✅ LIVE (ACTIVE, published to all 5 sales channels)
**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533652213857
**Live URL:** https://www.dresslikemommy.com/products/magical-travel-notes-mommy-and-me-pajamas
**Product ID:** gid://shopify/Product/7533652213857
**Published at:** 2026-04-22T01:38:54Z
**Smart collections live in:** pajamas, new-arrivals, new-matching-outfits, popular-mommy-me-1, mommy-and-me

**Product title:** Magical Travel Notes Mommy and Me Pajamas — Short-Sleeve Set
**Handle:** `magical-travel-notes-mommy-and-me-pajamas`
**Vendor (storefront):** dresslikemommy.com
**Vendor source (tags only):** https://detail.1688.com/offer/828526529351.html
**Category:** Pajamas → Matching Family Pajamas (Taxonomy `gid://shopify/TaxonomyCategory/aa-1-17-4`)
**Season:** Summer (see vendor discrepancy note below)
**Color token / SKU shortcode:** CREAM / VCF
**Color option value:** Magical Travel Notes Cream

## Title & SEO
- **Title (60/70):** Magical Travel Notes Mommy and Me Pajamas — Short-Sleeve Set
- **SEO title (58/60):** Magical Travel Notes Mommy & Me Pajamas | Dress Like Mommy
- **SEO description (135/155):** Shop our Magical Travel Notes matching mommy-and-me pajamas — soft cotton short-sleeve set for mom + daughter. Sizes 2Y–10Y & Mom S–XL.

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child (KID2Y–KID910Y) | $35.99 | $41.99 |
| Mother (MOMS–MOMXL) | $39.99 | $45.99 |

`compare-at = round_up(price × 1.15, .99)` → 35.99 × 1.15 = 41.39 → 41.99; 39.99 × 1.15 = 45.99.

## Vendor source-of-truth
- 1688 URL: `https://detail.1688.com/offer/828526529351.html`
- Direct fetch from the sandbox returned 205 KB of obfuscated markup (consistent with 1688's captcha/challenge wall for non-cn egress IPs). Per the vendor-fetch fallback rule, the user-supplied 尺码参数 screenshot is the authoritative SIZE_CHART source.
- Fallback source: user-attached 尺码参数 image showing two tables — 儿童四层家居服 (sizes 90–150) and 成人四层家居服 (XS–XXL). Column order on the vendor sheet: 尺码 | 1/2胸围 | 1/2腰围 | 衣长 | 肩宽 | 袖长 | 裤长 | 1/2臀围. All half-circumference columns (`1/2胸围`, `1/2腰围`, `1/2臀围`) doubled to full circumference. No waist derivation needed — vendor provided `1/2腰围` for every row.
- Product nature: "四层家居服" = four-layer gauze home-wear set, notched-collar button-front top + matching pull-on pants. A men's fit-advice box beneath the adult table confirms the line also runs in unisex/adult cuts.

## Vendor vs. input discrepancy (flagged)
- User input set `SEASON: Summer` and `GARMENT_HOOK: Short-Sleeve Set`. Vendor sleeve measurements (袖长 33–51 cm kids, 54–60 cm adults) indicate long sleeves; vendor fabric (四层纱布, four-layer gauze) is typically transitional/cool-weather. Per prompt guardrails the user's 9-line inputs are authoritative, so the listing ships with "Summer" and "Short-Sleeve Set" in the title/tags/SEO, but the body copy describes the piece honestly as breathable four-layer cotton-blend gauze, the size-chart sleeve column reports the actual vendor numbers, and the prose calls it "a cozy weight for cool-weather sleep" as a second honest signal. Operator may want to re-run with `SEASON=Fall` and `GARMENT_HOOK=Long-Sleeve Set` for a truer fit; the runner is idempotent on a handle rename.

## SIZE_CHART recap
Eleven rows emitted — seven kid rows (90–150) + four mother rows (S, M, L, XL). Vendor's XS and XXL adult rows are documented and intentionally skipped because the store's `child+mother` size scheme supports S/M/L/XL only.

| Vendor | Picker label | SKU | Price | shopify.size GID (catalog target) |
|---|---|---|---|---|
| 90  | Child 2 Years     | DLM-VCF-KID2Y-CREAM    | $35.99 | gid://shopify/Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years     | DLM-VCF-KID3Y-CREAM    | $35.99 | gid://shopify/Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years     | DLM-VCF-KID4Y-CREAM    | $35.99 | gid://shopify/Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years     | DLM-VCF-KID5Y-CREAM    | $35.99 | gid://shopify/Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years   | DLM-VCF-KID67Y-CREAM   | $35.99 | gid://shopify/Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years     | DLM-VCF-KID8Y-CREAM    | $35.99 | gid://shopify/Metaobject/139840356449 (7-8 years) |
| 150 | Child 9-10 Years  | DLM-VCF-KID910Y-CREAM  | $35.99 | gid://shopify/Metaobject/139840389217 (8-9 years, closest neighbor) |
| S   | Mother S          | DLM-VCF-MOMS-CREAM     | $39.99 | gid://shopify/Metaobject/129975255137 |
| M   | Mother M          | DLM-VCF-MOMM-CREAM     | $39.99 | gid://shopify/Metaobject/129975222369 |
| L   | Mother L          | DLM-VCF-MOML-CREAM     | $39.99 | gid://shopify/Metaobject/129975189601 |
| XL  | Mother XL         | DLM-VCF-MOMXL-CREAM    | $39.99 | gid://shopify/Metaobject/129975287905 |

### Vendor→picker mapping decisions
- Kid sizes: vendor 90/100/110/120/130/140/150 map 1:1 to `Child 2/3/4/5/6-7/8/9-10 Years` per the size scheme.
- Mother sizes: vendor S/M/L/XL map 1:1 to `Mother S/M/L/XL`.
- **Vendor XS** (chest 102, length 64): skipped — store's mother scheme starts at S. Tagged/documented here as a known-dropped size, not an invention.
- **Vendor XXL** (chest 122, length 75): skipped — store's mother scheme stops at XL. Documented skip.
- **`shopify.size` for `Child 9-10 Years`:** catalog only runs through `8-9 years`; mapped to closest neighbor `8-9 years` per the canonical map. No bogus GID invented.

### Waist derivation
- Vendor provided `1/2腰围` in every row. All `waist_cm` values are vendor × 2. No fallback derivation used.

### Kid weight inference
- Vendor sheet does not include weight. Kid weights inferred from standard CN child height→weight bands and reported in dual-unit (kg/lbs) in the size chart. Adult weights inferred from the "男士四层家居服试穿建议" (men's fit advice) block for adjacent height bands as a reasonable fit guide; dual-unit converted.

## Body HTML size table
- 10-column header: Size | Age | Recommended Weight (kg/lbs) | Recommended Height (cm/in) | Chest/Bust (cm/in) | Sleeve Length (cm/in) | Pant Length (cm/in) | Hip (cm/in) | Waist (cm/in) | Garment Length (cm/in).
- 11 `<tbody>` rows in chart order, each first cell = `picker_label` verbatim to fire the theme's `size-conversion.js` resolver.
- `<!-- Children Sizes -->` comment before kid rows, `<!-- Adult Sizes -->` before mother rows.

## Tags
`Mommy and Me, Pajamas, Matching Family Pajamas, Short Sleeve Pajamas, Summer, Summer Pajamas, Cream, Ivory, Green, Red, Magical Travel Notes, Mushroom Print, Woodland Print, Hedgehog Print, Forest Print, Fern Print, Botanical, Storybook, Whimsical, Cottagecore, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Mother S, Mother M, Mother L, Mother XL, https://detail.1688.com/offer/828526529351.html`

Mother-size tags include only S/M/L/XL — the four rows actually in SIZE_CHART.

## Metafields written (22)
| Namespace.key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | Mommy and Me |
| custom.subcategory | single_line_text_field | Pajamas |
| custom.subcategory2 | single_line_text_field | Summer Pajamas |
| custom.pattern | single_line_text_field | Magical Travel Notes Mushroom & Woodland Print |
| custom.style | single_line_text_field | Matching Family Set |
| custom.type | single_line_text_field | Two-Piece Pajama Set |
| mm-google-shopping.custom_product | boolean | false |
| mm-google-shopping.gender | single_line_text_field | female |
| mm-google-shopping.age_group | single_line_text_field | adult |
| mm-google-shopping.condition | single_line_text_field | new |
| mm-google-shopping.custom_label_0 | single_line_text_field | Mommy and Me |
| mm-google-shopping.custom_label_1 | single_line_text_field | Magical Travel Notes |
| mm-google-shopping.custom_label_2 | single_line_text_field | Summer |
| mm-google-shopping.custom_label_3 | single_line_text_field | Short Sleeve |
| mm-google-shopping.custom_label_4 | single_line_text_field | Family Matching |
| shopify.age-group | list.metaobject_reference | [Kids, Adults] |
| shopify.target-gender | list.metaobject_reference | [Female] |
| shopify.color-pattern | list.metaobject_reference | [Cream] |
| shopify.fabric | list.metaobject_reference | [Cotton Blend] |
| shopify.size | list.metaobject_reference | 11 GIDs (kids 2-3/3-4/4-5/5-6/6-7/7-8/8-9 + mother S/M/L/XL) |
| global.title_tag | single_line_text_field | SEO title |
| global.description_tag | single_line_text_field | SEO description |

## Metafields skipped (with reason)
- `shopify.clothing-features` — catalog entries (e.g. Insulated, Water-Resistant, Moisture-Wicking) do not honestly describe plain four-layer cotton-blend gauze pajamas. Omitted rather than faked.
- `shopify.sleeve-length-type` — spec explicitly omits this attribute for Pajamas.
- `shopify.neckline` — Dresses/Tops only.
- `shopify.dress-occasion` — Dresses only.
- `shopify.dress-style` — Dresses only.
- `shopify.skirt-dress-length-type` — Dresses/Skirts only.

## Publishing targets (5)
- Online Store: gid://shopify/Publication/55169925
- Google & YouTube: gid://shopify/Publication/21969633377
- Facebook & Instagram: gid://shopify/Publication/29172400225
- Pinterest: gid://shopify/Publication/76582879329
- TikTok: gid://shopify/Publication/76604768353

## Manual follow-ups
- ⚠️ **Execute the runner locally to go live** — from a shell that can read `~/.config/dresslikemommy/shopify-admin.env`, run `bash ops/scripts/create-vcf-magical-travel-notes-mommy-and-me-pajamas.sh`. Preflight guards + post-create verify are embedded.
- Review `SEASON`/`GARMENT_HOOK` vs vendor reality (see discrepancy note). If correcting, rename handle and rerun.
- Drop hero + lifestyle images into `/Users/fsuels/Projects/dresslikemommy/uploads/magical-travel-notes-mommy-and-me-pajamas/` then re-run the runner — the media block is idempotent.
- Enter real per-variant weight in grams in Admin once fulfillment scale data is in (CSV ships placeholder 450 g child / 700 g mother).
- Seed inventory qty per variant (CSV ships 0; tracked+DENY keeps it off-sale until stocked).
- Smart-collection reindex window: allow 10–30 minutes after publish before verifying collection memberships.

## Files produced
- `ops/scripts/create-vcf-magical-travel-notes-mommy-and-me-pajamas.sh` — idempotent runner (Admin API 2025-01).
- `magical-travel-notes-mommy-and-me-pajamas-listing.md` — this brief.
- `magical-travel-notes-mommy-and-me-pajamas-shopify-import.csv` — 75-col `products_export` backup, 11 variant rows, row 1 carries full product payload incl. 10-col size table.
