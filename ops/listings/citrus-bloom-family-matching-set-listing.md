# Citrus Bloom Family Matching Set — Dress & Shirt

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7536700391521
- **Live:** https://www.dresslikemommy.com/products/citrus-bloom-family-matching-set
- **Vendor:** https://detail.1688.com/offer/797837557857.html
- **Product GID:** `gid://shopify/Product/7536700391521`
- **Handle:** `citrus-bloom-family-matching-set`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/797837557857.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | Family Matching |
| PRIMARY_CATEGORY | Set → FamilySet (Shopify taxonomy kept as Outfit Sets) |
| DESIGNS_TO_LIST | Shirt, Dress |
| EXCLUDE_ITEMS | infant romper table and white shorts styling-only imagery excluded because the request only asked for Shirt + Dress |
| SHORTCODE | auto → `CTBL` |
| COLOR_TOKEN | auto → `BLOOM` |
| FORCE_SPEC_PRICES | true |

## Vendor fetch status
The direct 1688 page was captcha-blocked during this run, so the attached size-chart image and supplied family photos were used as the authoritative source of truth. The attached chart is a fit-reference-only source: it publishes recommended height and weight ladders for kids, adults, and an infant romper line, but it does not publish garment chest, hip, waist, shoulder, or length measurements for the requested shirt-and-dress design. To keep the listing honest and rerunnable, dress measurements were backfilled from the store's live `pink-horizon-family-matching-set` dress grading because its shoulder-strap/maxi silhouette and `Mother S–2XL` spread most closely match the supplied imagery and adult ladder, while shirt measurements were backfilled from the live `summer-sky-stripe-family-matching-set` collared short-sleeve shirt grading because that shirt silhouette matches the supplied photos. The `Child 1-2 Years` dress row continues the live dress curve one size down from `90`, and the `Father 4XL` shirt row continues the live collared-shirt curve one size up from `3XL`. Neighbor pricing was anchored to `pink-horizon-family-matching-set`, while size metaobject GIDs were anchored to that live family-set product plus direct live `shopify--size` lookups for the endpoint labels. The infant romper reference table and the white shorts shown in the styling photos were intentionally excluded because this request only asked for the shirt and dress designs. The Shopify taxonomy stays `Outfit Sets` for honest standard-category attributes.

## Title & SEO
| | Value | Chars |
|---|---|---|
| Product Title | `Citrus Bloom Family Matching Set — Dress & Shirt` | 48 |
| SEO Title | `Citrus Bloom Family Set | Dress Like Mommy` | 42 |
| SEO Description | `Lightweight woven family matching set with floral dresses and collared shirts for moms, dads, girls & boys. Sizes 1-2Y–10Y, Mother S–2XL, Father S–4XL.` | 151 |

## SIZE_CHART recap
| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |
|---|---|---|---|---|---|---|
| Girl Dress | 80 | Child 1-2 Years | `DLM-CTBL-GRL-KID12Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Girl Dress | 90 | Child 2 Years | `DLM-CTBL-GRL-KID2Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Dress | 100 | Child 3 Years | `DLM-CTBL-GRL-KID3Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | `DLM-CTBL-GRL-KID4Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | `DLM-CTBL-GRL-KID5Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | `DLM-CTBL-GRL-KID67Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | `DLM-CTBL-GRL-KID8Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | `DLM-CTBL-GRL-KID910Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | `DLM-CTBL-MOM-S-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | `DLM-CTBL-MOM-M-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | `DLM-CTBL-MOM-L-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | `DLM-CTBL-MOM-XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Dress | XXL | Mother 2XL | `DLM-CTBL-MOM-2XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975156833` (2XL) |
| Boy Shirt | 80 | Child 1-2 Years | `DLM-CTBL-BOY-KID12Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972797537` (12-18 months) |
| Boy Shirt | 90 | Child 2 Years | `DLM-CTBL-BOY-KID2Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Boy Shirt | 100 | Child 3 Years | `DLM-CTBL-BOY-KID3Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Boy Shirt | 110 | Child 4 Years | `DLM-CTBL-BOY-KID4Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Boy Shirt | 120 | Child 5 Years | `DLM-CTBL-BOY-KID5Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Boy Shirt | 130 | Child 6-7 Years | `DLM-CTBL-BOY-KID67Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Boy Shirt | 140 | Child 8 Years | `DLM-CTBL-BOY-KID8Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129973026913` (8) |
| Boy Shirt | 150 | Child 9-10 Years | `DLM-CTBL-BOY-KID910Y-BLOOM` | 28.99 | 33.99 | `gid://shopify/Metaobject/129971552353` (10) |
| Father Shirt | S | Father S | `DLM-CTBL-DAD-S-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975255137` (S) |
| Father Shirt | M | Father M | `DLM-CTBL-DAD-M-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975222369` (M) |
| Father Shirt | L | Father L | `DLM-CTBL-DAD-L-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975189601` (L) |
| Father Shirt | XL | Father XL | `DLM-CTBL-DAD-XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975287905` (XL) |
| Father Shirt | XXL | Father 2XL | `DLM-CTBL-DAD-2XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/129975156833` (2XL) |
| Father Shirt | 3XL | Father 3XL | `DLM-CTBL-DAD-3XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840421985` (3XL) |
| Father Shirt | 4XL | Father 4XL | `DLM-CTBL-DAD-4XL-BLOOM` | 31.99 | 36.99 | `gid://shopify/Metaobject/139840716897` (4XL) |

### Derivations (flagged per spec)
- The attached vendor chart is a fit-reference-only table, so every garment measurement column (`chest_cm`, `hip_cm`, `waist_cm`, `shoulder_cm`, `length_cm`, `skirt_cm`) was backfilled from the closest live dress/shirt grading curves already published on the store rather than fabricated from scratch.
- Child and adult weight guidance was converted from the vendor's `斤` ranges into metric `kg` ranges before the shopper-facing table converted those values to `kg/lbs`.
- Dress measurements were anchored to the live `pink-horizon-family-matching-set` dress ladder for `90-150` and `Mother S-2XL`; the `80` row continues that same grade one step down because the vendor fit chart includes `80` but the live anchor starts at `90`.
- Shirt measurements were anchored to the live `summer-sky-stripe-family-matching-set` collared short-sleeve shirt ladder for `80-150` and `Father S-3XL`; the `Father 4XL` row continues that same adult grade one step up because the vendor fit chart includes `4XL` while the live collared-shirt anchor stops at `3XL`.
- The infant romper reference table on the supplied size chart was intentionally excluded because it describes a separate baby garment family outside this `Dress` + `Shirt` listing request.
- `Child 1-2 Years` was mapped to the closest honest live size metaobject label `12-18 months` because the store does not expose an exact `1-2 years` size metaobject.

### Vendor → picker mapping log
- 80 → Child 1-2 Years
- 90 → Child 2 Years
- 100 → Child 3 Years
- 110 → Child 4 Years
- 120 → Child 5 Years
- 130 → Child 6-7 Years
- 140 → Child 8 Years
- 150 → Child 9-10 Years
- Women S / M / L / XL / 2XL → Mother S / M / L / XL / 2XL
- Men S / M / L / XL / XXL / 3XL / 4XL → Father S / M / L / XL / 2XL / 3XL / 4XL

### EXCLUDE_ITEMS decisions
- The operator did not pass an explicit `EXCLUDE_ITEMS` string.
- The infant romper reference table on the supplied size chart was excluded because it belongs to a different baby garment family than the requested shirt-and-dress listing.
- The white shorts shown on the dad model in the supplied photos are styling only and were excluded because the request explicitly limited the listing to the shirt and dress designs.

## Body HTML
- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).
- 2 garment-specific `<h3>` + `<table>` blocks (`Dress` and `Shirt`), each with 10 `<th>` headers.
- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.

## Option axes & variants
- Option 1: `Type` → `Dress`, `Shirt`
- Option 2: `Size` → `Child 1-2 Years`, `Child 2 Years`, `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 8 Years`, `Child 9-10 Years`, `Mother S`, `Mother M`, `Mother L`, `Mother XL`, `Mother 2XL`, `Father S`, `Father M`, `Father L`, `Father XL`, `Father 2XL`, `Father 3XL`, `Father 4XL`
- Variants live: **28**

## Verify pass table
| Check | Result | Detail |
|---|---|---|
| Title <= 70 chars | ✅ | 48 |
| SEO title <= 60 chars | ✅ | 42 |
| SEO description <= 155 chars | ✅ | 151 |
| Live variant count matches SIZE_CHART | ✅ | 28 vs 28 |
| Live SKUs match derived SKUs | ✅ | DLM-CTBL-BOY-KID12Y-BLOOM, DLM-CTBL-BOY-KID2Y-BLOOM, DLM-CTBL-BOY-KID3Y-BLOOM, DLM-CTBL-BOY-KID4Y-BLOOM, DLM-CTBL-BOY-KID5Y-BLOOM, DLM-CTBL-BOY-KID67Y-BLOOM, DLM-CTBL-BOY-KID8Y-BLOOM, DLM-CTBL-BOY-KID910Y-BLOOM, DLM-CTBL-DAD-2XL-BLOOM, DLM-CTBL-DAD-3XL-BLOOM, DLM-CTBL-DAD-4XL-BLOOM, DLM-CTBL-DAD-L-BLOOM, DLM-CTBL-DAD-M-BLOOM, DLM-CTBL-DAD-S-BLOOM, DLM-CTBL-DAD-XL-BLOOM, DLM-CTBL-GRL-KID12Y-BLOOM, DLM-CTBL-GRL-KID2Y-BLOOM, DLM-CTBL-GRL-KID3Y-BLOOM, DLM-CTBL-GRL-KID4Y-BLOOM, DLM-CTBL-GRL-KID5Y-BLOOM, DLM-CTBL-GRL-KID67Y-BLOOM, DLM-CTBL-GRL-KID8Y-BLOOM, DLM-CTBL-GRL-KID910Y-BLOOM, DLM-CTBL-MOM-2XL-BLOOM, DLM-CTBL-MOM-L-BLOOM, DLM-CTBL-MOM-M-BLOOM, DLM-CTBL-MOM-S-BLOOM, DLM-CTBL-MOM-XL-BLOOM |
| Live option axes match derived axes | ✅ | Type / Size |
| Live option values match derived values | ✅ | {"Type": ["Dress", "Shirt"], "Size": ["Child 1-2 Years", "Child 2 Years", "Child 3 Years", "Child 4 Years", "Child 5 Years", "Child 6-7 Years", "Child 8 Years", "Child 9-10 Years", "Mother S", "Mother M", "Mother L", "Mother XL", "Mother 2XL", "Father S", "Father M", "Father L", "Father XL", "Father 2XL", "Father 3XL", "Father 4XL"]} |
| Every Type x Size combination exists | ✅ | [('Dress', 'Child 1-2 Years'), ('Dress', 'Child 2 Years'), ('Dress', 'Child 3 Years'), ('Dress', 'Child 4 Years'), ('Dress', 'Child 5 Years'), ('Dress', 'Child 6-7 Years'), ('Dress', 'Child 8 Years'), ('Dress', 'Child 9-10 Years'), ('Dress', 'Mother 2XL'), ('Dress', 'Mother L'), ('Dress', 'Mother M'), ('Dress', 'Mother S'), ('Dress', 'Mother XL'), ('Shirt', 'Child 1-2 Years'), ('Shirt', 'Child 2 Years'), ('Shirt', 'Child 3 Years'), ('Shirt', 'Child 4 Years'), ('Shirt', 'Child 5 Years'), ('Shirt', 'Child 6-7 Years'), ('Shirt', 'Child 8 Years'), ('Shirt', 'Child 9-10 Years'), ('Shirt', 'Father 2XL'), ('Shirt', 'Father 3XL'), ('Shirt', 'Father 4XL'), ('Shirt', 'Father L'), ('Shirt', 'Father M'), ('Shirt', 'Father S'), ('Shirt', 'Father XL')] |
| Size table first column matches picker labels | ✅ | Child 1-2 Years | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M | Mother L | Mother XL | Mother 2XL | Child 1-2 Years | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Father S | Father M | Father L | Father XL | Father 2XL | Father 3XL | Father 4XL |
| Size tables expose metric + imperial units | ✅ | kg/lbs + cm/in |
| Each size table has 10 headers | ✅ | [10, 10] |
| Table row count matches SIZE_CHART | ✅ | 28 |
| publishedAt is populated | ✅ | 2026-04-24T03:48:46Z |
| onlineStoreUrl is populated | ✅ | https://www.dresslikemommy.com/products/citrus-bloom-family-matching-set |
| Taxonomy category is set | ✅ | gid://shopify/TaxonomyCategory/aa-1-11 |
| Taxonomy category full name matches expected leaf | ✅ | Apparel & Accessories > Clothing > Outfit Sets |
| Family-set merchandising tag is present | ✅ | Beach, Blue, Boy Shirt, Button Front Shirt, Child 1-2 Years, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Citrus Bloom, Citrus Print, Collared Shirt, Daddy and Me, Dress & Shirt, Family Matching, Father 2XL, Father 3XL, Father 4XL, Father L, Father M, Father S, Father Shirt, Father XL, Floral, Four-Role Matching, Garden Floral, Girl Dress, https://detail.1688.com/offer/797837557857.html, Matching Family Dress, Matching Family Outfits, Matching Family Set, Matching Family Shirt, Maxi Dress, Mommy and Me, Mother 2XL, Mother Dress, Mother L, Mother M, Mother S, Mother XL, Multicolor, Painterly Floral, Resort, Sets, Short Sleeve Shirt, Shoulder Strap Dress, Sleeveless Dress, Summer, Summer Family Matching Set, Vacation, Yellow |
| Family-set smart collection is attached | ✅ | ['daddy-and-me', 'daddy-me', 'family-sets', 'matching-family-vacation-outfits', 'mommy-and-me', 'new-matching-outfits', 'new-women-outfits', 'popular-family-matching', 'popular-mommy-me-1'] |
| Required publications are live | ✅ | ['gid://shopify/Publication/21969633377', 'gid://shopify/Publication/29172400225', 'gid://shopify/Publication/55169925', 'gid://shopify/Publication/76582879329', 'gid://shopify/Publication/76604768353'] |
| Applicable metafields are written | ✅ | [] |

## Price parity (FORCE_SPEC_PRICES=true)
| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |
|---|---|---|---|---|---|
| DLM-CTBL-GRL-KID12Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID2Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID3Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID4Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID5Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID67Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID8Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-GRL-KID910Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-MOM-S-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-MOM-M-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-MOM-L-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-MOM-XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-MOM-2XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-BOY-KID12Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID2Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID3Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID4Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID5Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID67Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID8Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-BOY-KID910Y-BLOOM | 28.99 | 33.99 | 28.99 | 33.99 | ✓ |
| DLM-CTBL-DAD-S-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-M-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-L-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-2XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-3XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |
| DLM-CTBL-DAD-4XL-BLOOM | 31.99 | 36.99 | 31.99 | 36.99 | ✓ |

## Metafields — written
| Namespace.Key | Type | Value |
|---|---|---|
| custom.category1 | single_line_text_field | `Family Matching` |
| custom.pattern | single_line_text_field | `Citrus Bloom Floral` |
| custom.style | single_line_text_field | `Matching Family Set` |
| custom.subcategory | single_line_text_field | `Set` |
| custom.subcategory2 | single_line_text_field | `Summer Family Matching Set` |
| custom.type | single_line_text_field | `Two-Piece Set` |
| global.description_tag | single_line_text_field | `Lightweight woven family matching set with floral dresses and collared shirts for moms,...` |
| global.title_tag | single_line_text_field | `Citrus Bloom Family Set | Dress Like Mommy` |
| mm-google-shopping.age_group | single_line_text_field | `adult` |
| mm-google-shopping.condition | single_line_text_field | `new` |
| mm-google-shopping.custom_label_0 | single_line_text_field | `Family Matching` |
| mm-google-shopping.custom_label_1 | single_line_text_field | `Citrus Bloom` |
| mm-google-shopping.custom_label_2 | single_line_text_field | `Summer` |
| mm-google-shopping.custom_label_3 | single_line_text_field | `Dress & Shirt` |
| mm-google-shopping.custom_label_4 | single_line_text_field | `Four-Role Matching` |
| mm-google-shopping.custom_product | boolean | `false` |
| mm-google-shopping.gender | single_line_text_field | `unisex` |
| shopify.age-group | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| shopify.care-instructions | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| shopify.color-pattern | list.metaobject_reference | `["gid://shopify/Metaobject/69622104161","gid://shopify/Metaobject/69639766113","gid://s...` |
| shopify.size | list.metaobject_reference | `["gid://shopify/Metaobject/129972797537","gid://shopify/Metaobject/129972863073","gid:/...` |
| shopify.target-gender | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889","gid://shopify/Metaobject/130231107681"]` |

## Metafields — skipped
| Namespace.Key | Reason |
|---|---|
| shopify.clothing-features | The current store catalog only exposes heavyweight or technical feature values in this namespace, which would be inaccurate for this lightweight summer family set. |
| shopify.fabric | The direct vendor page was captcha-blocked and the supplied fit chart plus images do not confirm one honest fiber metaobject, so this field was left unset rather than guessing cotton vs. synthetic. |
| shopify.dress-occasion | Not written because the honest Shopify taxonomy for this product is `Outfit Sets`, not `Dresses`, even though two of the roles wear dresses. |
| shopify.dress-style | Not written because this is a mixed-garment outfit-set listing rather than a dress-only taxonomy leaf. |
| shopify.fit | The Outfit Sets taxonomy exposes fit, but no reliable writable standard Shopify metafield definition is currently available in this store for that attribute. |
| shopify.neckline | The mixed dress-and-shirt presentation does not map cleanly to one honest neckline value at the product level for this store. |
| shopify.pants-length-type | White shorts appear in the supplied photos as styling only, and the infant romper reference table was excluded from this dress-and-shirt listing, so a pants-length metafield would misstate the product scope. |
| shopify.skirt-dress-length-type | Not written because the listing mixes dresses and shirts under `Outfit Sets`, so a dress-only length metafield would overstate the product scope. |
| shopify.sleeve-length-type | Not written because the listing mixes a dress and short-sleeve shirts, so one product-level sleeve-length value would be misleading. |
| shopify.top-length-type | Removed if present because the product mixes dress and shirt roles, and no single top-length metafield is honest for the whole listing. |
| shopify.waist-rise | The vendor chart exposes waist measurements, but no reliable writable standard Shopify metafield definition is currently available in this store for this mixed outfit-set product. |

## Tags written (54)
`Beach, Blue, Boy Shirt, Button Front Shirt, Child 1-2 Years, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Citrus Bloom, Citrus Print, Collared Shirt, Daddy and Me, Dress & Shirt, Family Matching, Father 2XL, Father 3XL, Father 4XL, Father L, Father M, Father S, Father Shirt, Father XL, Floral, Four-Role Matching, Garden Floral, Girl Dress, https://detail.1688.com/offer/797837557857.html, Matching Family Dress, Matching Family Outfits, Matching Family Set, Matching Family Shirt, Maxi Dress, Mommy and Me, Mother 2XL, Mother Dress, Mother L, Mother M, Mother S, Mother XL, Multicolor, Painterly Floral, Resort, Sets, Short Sleeve Shirt, Shoulder Strap Dress, Sleeveless Dress, Summer, Summer Family Matching Set, Vacation, Yellow`

## Publication
- Online Store
- Google & YouTube
- Facebook & Instagram
- Pinterest
- TikTok

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
- Inventory quantities and per-variant grams still need operator stock values.
- Re-confirm the exact fiber composition if the vendor page becomes directly readable later; `shopify.fabric` is intentionally left unset for now rather than guessing.
- If the vendor page becomes directly readable later and publishes garment measurements for this exact print, replace the backfilled dress/shirt grading with the direct source measurements on a rerun.
- If Shopify exposes writable standard metafields for `fit`, `pants-length-type`, or `waist-rise` in this store later, extend the runner to write the already-inferred outfit-set attributes too.

## Files saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-ctbl-citrus-bloom-family-matching-set.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/citrus-bloom-family-matching-set-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/citrus-bloom-family-matching-set-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-citrus-bloom-family-matching-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-citrus-bloom-family-matching-set.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-citrus-bloom-family-matching-set.html`
- `/Users/fsuels/Projects/dresslikemommy/uploads/citrus-bloom-family-matching-set`

## Sources
- Neighbor pricing: `pink-horizon-family-matching-set`
- Garment grading anchors: `pink-horizon-family-matching-set` for the dress ladder and `summer-sky-stripe-family-matching-set` for the collared-shirt ladder
- Size metaobject map: `pink-horizon-family-matching-set` plus direct live `shopify--size` lookups for endpoint sizes not present on that anchor
