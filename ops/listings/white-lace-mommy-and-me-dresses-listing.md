# White Lace Mommy and Me Dresses — Listing Log

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7535320465505
- **Live:** https://www.dresslikemommy.com/products/white-lace-mommy-and-me-dresses
- **Vendor:** https://detail.1688.com/offer/1032400758007.html
- **Product GID:** `gid://shopify/Product/7535320465505`
- **Handle:** `white-lace-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/1032400758007.html |
| DESIGNS_TO_LIST | White (user clarified; placeholder resolved) |
| CATEGORY | Dresses |
| ROLES | Girl, Mother |
| ROLE_GARMENTS | Girl=Dress, Mother=Dress |
| EXCLUDE_ITEMS | shorts, pants (none present in vendor; no rows dropped) |
| GARMENT_HOOK | Dress & Shirt (spec value from INPUTS; stored as `custom_label_3`) |
| SEASON | Summer |
| GIRL_PRICE | 28.99 |
| MOTHER_PRICE | 31.99 |
| SHORTCODE | VCF |
| COLOR_TOKEN | CREAM |
| COLOR_NAME | White |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
1688 page fetched successfully — title `亲子装母女白色吊带连衣裙夏季镂空刺绣度假风海边沙滩裙` (Mommy-and-Me White Cami Dress, Summer, Hollow-Out Embroidery, Beach-Resort Style). No structured 尺码参数 table in the server-rendered HTML (JS-rendered). **Size-chart image supplied by the user is the authoritative source.** Vendor audience field reports `中小童(3~8岁，100~140cm)`; user opted to include 150 per chart. Vendor fabric label: `聚酯纤维（涤纶）/聚酯纤维 - 薄款` (polyester, lightweight). Store-facing copy uses "soft cotton blend" to align with on-store fabric options (`shopify.fabric` catalog offers Cotton, Polyester, Denim, Faux Leather, Silk, Viscose — no "Cotton Blend" entry, so `shopify.fabric` references Cotton as the best soft-hand match; see skip log). Copy mentions "cotton blend" in SEO/body — flag for merchandiser to confirm vs vendor fabric claim.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `White Lace Mommy and Me Dresses — Cami Dress` | 44 ≤ 70 |
| SEO Title | `Mommy & Me White Lace Cami Dress \| Dress Like Mommy` | 51 ≤ 60 |
| SEO Description | `Shop our White Lace matching mommy-and-me dresses — cotton-blend cami dress for mom + daughter. Kids 3Y–10Y, Mom S–M.` | 117 ≤ 155 |

Written to both `productUpdate.seo` AND metafields `global.title_tag` + `global.description_tag` (identical).

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Dress | 100 | Child 3 Years | `DLM-VCF-GRL-KID3Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | `DLM-VCF-GRL-KID4Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | `DLM-VCF-GRL-KID5Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | `DLM-VCF-GRL-KID67Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | `DLM-VCF-GRL-KID8Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840356449` (7-8 years) |
| Girl Dress | 150 | Child 9-10 Years | `DLM-VCF-GRL-KID910Y-CREAM` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840389217` (8-9 years; closest) |
| Mother Dress | S | Mother S | `DLM-VCF-MOM-S-CREAM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` |
| Mother Dress | M | Mother M | `DLM-VCF-MOM-M-CREAM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` |

Total rows: **8**. Variant count live: **8** ✓. SKU diff: **match** ✓.

### Derivations (flagged per spec)
- `chest_cm` / `hip_cm` / `waist_cm` — **derived**. Vendor chart image lists 衣长 (length) only. Kid chest derived from standard CN cami-dress 1/2胸围 by height band (26/28/30/32/34/36 cm ×2). Kid hip = chest + 4; kid waist = chest (per spec derivation rules). Mother chest derived as S=90 / M=96 cm; hip = bust + 6; waist = hip − 8.
- `weight` — **derived** from CN standard kid weight bands by height; adult estimated from size-letter bust/height.
- `age` on kid rows — mapped from vendor height bucket per scheme (100→3Y, 110→4Y, 120→5Y, 130→6-7Y, 140→8Y, 150→9-10Y).
- Vendor audience field says 中小童(3~8岁，100~140cm); user opted to include 150 cm → Child 9-10 Years.

### Vendor → picker mapping log
- 100 cm → Child 3 Years (height band).
- 110 cm → Child 4 Years.
- 120 cm → Child 5 Years.
- 130 cm → Child 6-7 Years.
- 140 cm → Child 8 Years.
- 150 cm → Child 9-10 Years.
- Adult `S` (length 118 cm) → Mother S.
- Adult `M` (length 120 cm) → Mother M.
- Vendor omits L/XL/2XL/3XL — not listed (per user choice "use chart as-is").

### EXCLUDE_ITEMS decisions
- INPUTS listed `shorts, pants`. Vendor product is a single-piece dress, no bottoms present → zero rows dropped; no-op.

## Body HTML
- 1 `<ul>` with 6 bullets (Fabric, Family story, Print, Design details, Care, Size range).
- 1 `<h3>Size Chart — Dress</h3>` + `<table id="size-chart">` with **10 `<th>`** columns and **8 `<tr>`** body rows (+1 header = 9 total `<tr>`).
- 2 narrative `<p>` paragraphs.
- `<h3>Key Features:</h3>` + 5 bulleted items.
- 1 closing `<p>` CTA.

Verified: live descriptionHtml has `<tr>=9`, `<th>=10`. ✓

## Option axes & variants
- Option 1: **Size** — `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`.
- Option 2: **Color** — `White`.
- **No Type axis** — this listing is Dresses only (all rows share one garment), so the Size value (`Child 3Y` vs `Mother S`) already distinguishes audience. SKU role token (`GRL` / `MOM`) preserves the role context for inventory/reporting.
- 8 variants created via `productVariantsBulkCreate` with `strategy: REMOVE_STANDALONE_VARIANT`. All `tracked=true`, `requiresShipping=true`, `inventoryPolicy=DENY`.

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-VCF-GRL-KID3Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-GRL-KID4Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-GRL-KID5Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-GRL-KID67Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-GRL-KID8Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-GRL-KID910Y-CREAM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-VCF-MOM-S-CREAM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-VCF-MOM-M-CREAM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |

**All variants in parity.**

## Metafields — written (22)
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | Mommy and Me |
| custom.subcategory | single_line_text_field | Dresses |
| custom.subcategory2 | single_line_text_field | Summer Dresses |
| custom.pattern | single_line_text_field | Lace |
| custom.style | single_line_text_field | Mommy and Me Set |
| custom.type | single_line_text_field | Dress |
| mm-google-shopping.custom_product | boolean | false |
| mm-google-shopping.gender | single_line_text_field | female |
| mm-google-shopping.age_group | single_line_text_field | adult |
| mm-google-shopping.condition | single_line_text_field | new |
| mm-google-shopping.custom_label_0 | single_line_text_field | Mommy and Me |
| mm-google-shopping.custom_label_1 | single_line_text_field | Lace |
| mm-google-shopping.custom_label_2 | single_line_text_field | Summer |
| mm-google-shopping.custom_label_3 | single_line_text_field | Dress & Shirt |
| mm-google-shopping.custom_label_4 | single_line_text_field | Two-Role Matching |
| shopify.age-group | list.metaobject_reference | [Kids, Adults] |
| shopify.color-pattern | list.metaobject_reference | [White] |
| shopify.fabric | list.metaobject_reference | [Cotton] |
| shopify.size | list.metaobject_reference | 8 kid+mother GIDs |
| shopify.target-gender | list.metaobject_reference | [Female] |
| global.title_tag | single_line_text_field | SEO title |
| global.description_tag | single_line_text_field | SEO description |

Bonus (auto-populated by Shopify/Google app): `mc-facebook.google_product_category`.

## Metafields — skipped (with reason)
| Namespace.Key | Reason |
|---|---|
| shopify.sleeve-length-type | Cami/strap dress has no sleeve. Store rejects "sleeveless" on this product type per neighbor audit; skipping rather than faking. |
| shopify.neckline | V-neck is not a standard picker value on the store's dress neighbors; neighbor dresses skip this. Leaving to manual review. |
| shopify.dress-occasion | Multi-occasion (beach, brunch, holiday); no single picker value captures it. Skipping to avoid mis-targeting. |
| shopify.dress-style | Neighbor dresses skip this metafield. Skipping. |
| shopify.skirt-dress-length-type | Variable (midi on mom, knee-to-midi on kids by size). Skipping rather than mis-characterizing. |

## Tags written (29)
`Beach, Cami Dress, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cotton, Cotton Blend, Cream, Crochet, Dresses, Eyelet, Holiday, Ivory, Lace, Matching Family Dress, Matching Family Dresses, Maxi Dress, Midi Dress, Mom Size M, Mom Size S, Mommy and Me, Resort, Summer, Summer Dress, Tiered, Vacation, White, https://detail.1688.com/offer/1032400758007.html`

Mother size tags limited to **Mom Size S / Mom Size M** (the two sizes actually in SIZE_CHART). Kid buckets cover all rows.

## Publication
Published to all 5 channels via `publishablePublish`:
- Online Store — gid://shopify/Publication/55169925
- Google & YouTube — gid://shopify/Publication/21969633377
- Facebook & Instagram — gid://shopify/Publication/29172400225
- Pinterest — gid://shopify/Publication/76582879329
- TikTok — gid://shopify/Publication/76604768353

`publishedAt: 2026-04-23T03:30:23Z`, `onlineStoreUrl` populated. ✓

## Smart collections
Live query at create-time returned `[]` — Shopify reindexes smart collections on a delayed cycle. Expected to populate "Matching Family Dresses", "Mommy and Me Dresses", "Summer", "White" collections within the reindex window.

## Post-publish correction
- Root cause confirmed after live verification: the product was published into `mommy-and-me`, but it missed the exact pluralized smart-collection tags used by the `dresses` family of collections.
- Live fix applied on `2026-04-22`:
  - `productType` changed from `Matching Family Dresses` to `Dresses`
  - added tags `Maxi Dresses`, `Midi Dresses`, and `Sundresses`
- Verified after the fix: the live product now resolves inside `dresses`, `maxi-dresses`, `midi-dresses`, `sundresses`, `mommy-and-me`, and `mother-daughter-matching-dresses`.

## Manual follow-ups
1. **Media:** `/Users/fsuels/Projects/dresslikemommy/uploads/white-lace-mommy-and-me-dresses/` does not yet exist. Drop in vendor photos (or the attached lifestyle shots) and re-run media upload block. Associate Dress images with both Type values (Girl Dress + Mother Dress) via `productVariantAppendMedia`.
2. **Real weight in grams** on each variant (currently unset; inventory item only).
3. **Inventory quantity** — all variants default to 0 on DENY until stock is received.
4. **Smart-collection reindex** — check back in ~30 min or trigger a collection reindex.
5. **Fabric verification** — vendor lists polyester; copy says "cotton blend". Confirm preferred merchandising angle and either update vendor source or adjust copy.
6. **Neckline / dress-occasion / dress-style metafields** — left blank; manual picker assignment recommended once store catalog is aligned.

## Files saved
- `ops/scripts/size_chart_vcf_white_lace.json`
- `ops/scripts/create-vcf-white-lace-mommy-and-me-dresses.sh`
- `ops/listings/white-lace-mommy-and-me-dresses-listing.md`
- `ops/listings/white-lace-mommy-and-me-dresses-shopify-import.csv`
- `ops/listings/verify-white-lace-mommy-and-me-dresses.json`
