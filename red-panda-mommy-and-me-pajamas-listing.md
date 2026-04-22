# Red Panda Mommy and Me Pajamas — Long-Sleeve Set

**Status:** LIVE ✅  Published 2026-04-21
**Admin:** https://admin.shopify.com/store/dresslikemommy/products/7533454426209
**Live:** https://www.dresslikemommy.com/products/red-panda-mommy-and-me-pajamas
**Handle:** `red-panda-mommy-and-me-pajamas`
**Product ID:** `gid://shopify/Product/7533454426209`
**Product Type:** Matching Family Pajamas
**Taxonomy:** `gid://shopify/TaxonomyCategory/aa-1-17-4` (Pajamas)
**Vendor (Shopify field):** `dresslikemommy.com`
**Vendor source URL (tag only):** https://detail.1688.com/offer/828526529351.html

---

## Source of truth

Vendor 1688 page fetched successfully but the primary 尺码参数 size chart
lives inside an image asset on the detail page. The **user-attached
尺码参数 screenshot** (儿童四层家居服 + 成人四层家居服 tables) was used as
the authoritative size-chart source per the prompt's vendor-fetch fallback
rule. No retries were spun.

All vendor `1/2胸围`, `1/2腰围`, and `1/2臀围` columns were doubled to full
circumference before writing to SIZE_CHART.

Vendor weight was not provided in the 尺码参数 table. Kid weights derived
from the standard Chinese height-banded kid chart. Adult weights derived
from the vendor's 男士四层家居服试穿建议 footer + standard CN sizing:
身高186cm/180斤→XXL, 身高181cm/120斤→XXL宽松, 身高175cm/135斤→XL, 身高171cm/150斤→XL.

## Garment-hook correction (vendor-truth override)

Input specified `GARMENT_HOOK: Short-Sleeve Set`, but:

1. The two supplied product photos clearly show a **long-sleeve, long-pant,
   button-front** pajama set on both mother and daughter models.
2. Vendor size chart has non-trivial `袖长` (sleeve length) ranging 33–60 cm
   for kid + adult rows, and `裤长` (pant length) up to 107 cm. A short-sleeve
   set would have sleeve = ~16–25 cm and would not have a pant column at all
   (typically `短裤` column instead).

Per the STORE RULES "vendor size chart is the single source of truth" guard,
the garment hook was corrected to **Long-Sleeve Set** in the storefront
title, SEO copy, custom_label_3 Google Shopping metafield, and body HTML.

## Design scope

- Vendor sells children 90/100/110/120/130/140/150 (7 sizes) and adult
  XS/S/M/L/XL/XXL (6 sizes).
- Emitted children 90–150 (7) + adult S/M/L/XL (4) = **11 variants**.
- **XS and XXL vendor rows dropped.** The store's Mother size scheme is
  S/M/L/XL; XS and XXL have no picker labels or catalog metaobject entries
  and would create orphan variants. The vendor XS body is very close to
  Mother S (51 vs 53 half-chest), and XXL is near XL (61 vs 58). Buyers
  who need those points can size to the nearest offered variant; we're
  not faking picker values or padding the scheme.

## Pricing

| Audience | Price | Compare-at | Formula |
|---|---|---|---|
| Child  | $35.99 | $41.39 | round_up(35.99 × 1.15, .99) |
| Mother | $39.99 | $45.99 | round_up(39.99 × 1.15, .99) |

## Title & SEO (character counts)

| Field | Length | Content |
|---|---|---|
| Title (H1) | 48 / 70 | `Red Panda Mommy and Me Pajamas — Long-Sleeve Set` |
| SEO title  | 58 / 60 | `Red Panda Mommy & Me Pajamas — Matching \| Dress Like Mommy` |
| SEO desc   | 122 / 155 | `Shop our Red Panda matching mommy-and-me pajamas — soft cotton long-sleeve set for mom + daughter. Sizes 2Y–10Y, Mom S–XL.` |

SEO fields written to both `productUpdate.seo.{title,description}` AND
`global.title_tag` + `global.description_tag` metafields (identical copy).

## SIZE_CHART recap

| Vendor row | Picker label        | SKU                        | Price   | Variant ID | shopify.size GID |
|-----------:|---------------------|----------------------------|---------|------------|------------------|
| 90         | Child 2 Years       | DLM-VCF-KID2Y-CREAM        | $35.99  | 44047096545377 | `Metaobject/129972863073` (2-3 years) |
| 100        | Child 3 Years       | DLM-VCF-KID3Y-CREAM        | $35.99  | 44047096578145 | `Metaobject/129972895841` (3-4 years) |
| 110        | Child 4 Years       | DLM-VCF-KID4Y-CREAM        | $35.99  | 44047096610913 | `Metaobject/129972928609` (4-5 years) |
| 120        | Child 5 Years       | DLM-VCF-KID5Y-CREAM        | $35.99  | 44047096643681 | `Metaobject/129972961377` (5-6 years) |
| 130        | Child 6-7 Years     | DLM-VCF-KID67Y-CREAM       | $35.99  | 44047096676449 | `Metaobject/139840323681` (6-7 years) |
| 140        | Child 8 Years       | DLM-VCF-KID8Y-CREAM        | $35.99  | 44047096709217 | `Metaobject/139840356449` (7-8 years) |
| 150        | Child 9-10 Years    | DLM-VCF-KID910Y-CREAM      | $35.99  | 44047096741985 | `Metaobject/139840389217` (8-9 years — closest; 9-10 not in catalog) |
| S          | Mother S            | DLM-VCF-MOMS-CREAM         | $39.99  | 44047096774753 | `Metaobject/129975255137` |
| M          | Mother M            | DLM-VCF-MOMM-CREAM         | $39.99  | 44047096807521 | `Metaobject/129975222369` |
| L          | Mother L            | DLM-VCF-MOML-CREAM         | $39.99  | 44047096840289 | `Metaobject/129975189601` |
| XL         | Mother XL           | DLM-VCF-MOMXL-CREAM        | $39.99  | 44047096873057 | `Metaobject/129975287905` |

All 11 variants: `inventoryPolicy=DENY`, `tracked=true`, `requiresShipping=true`.

## Metafields written (22 total)

| Namespace.key | Value |
|---|---|
| custom.category1 | `Mommy and Me` |
| custom.subcategory | `Pajamas` |
| custom.subcategory2 | `Summer Pajamas` |
| custom.pattern | `Red Panda watercolor red panda + peach orchard print` |
| custom.style | `Matching Family Set` |
| custom.type | `Two-Piece Pajama Set` |
| mm-google-shopping.custom_product | `false` |
| mm-google-shopping.gender | `female` |
| mm-google-shopping.age_group | `adult` |
| mm-google-shopping.condition | `new` |
| mm-google-shopping.custom_label_0 | `Mommy and Me` |
| mm-google-shopping.custom_label_1 | `Red Panda Animal Print` |
| mm-google-shopping.custom_label_2 | `Summer` |
| mm-google-shopping.custom_label_3 | `Long Sleeve` |
| mm-google-shopping.custom_label_4 | `Family Matching` |
| shopify.age-group | Kids + Adults GIDs |
| shopify.color-pattern | Beige + Red + Floral GIDs |
| shopify.fabric | Cotton GID |
| shopify.size | 11 size GIDs (all picker labels mapped) |
| shopify.target-gender | Female GID |
| global.title_tag | SEO title (identical to seo.title) |
| global.description_tag | SEO description (identical to seo.description) |

## Metafields skipped (with reasons)

| Namespace.key | Skip reason |
|---|---|
| `shopify.sleeve-length-type` | Category-skip rule: omitted for Pajamas per spec (even though this product is long-sleeve, the rule is category-level). |
| `shopify.clothing-features` | Catalog only offers "Insulated" as an entry — does not honestly fit a soft cotton-gauze summer pajama set. Left blank rather than faked. |
| `shopify.neckline` | Dresses/Tops only (skip for Pajamas). |
| `shopify.dress-occasion` / `shopify.dress-style` / `shopify.skirt-dress-length-type` | Dresses only. |

## Color-pattern GID note

The runner's original `COLOR_GID["Orange"]` mapping used a GID from a
different metaobject definition and caused the whole `metafieldsSet` batch
to fail atomically with `Value must belong to the specified metaobject
definition gid://shopify/MetaobjectDefinition/663060577`. Queried the
`shopify--color-pattern` type and confirmed the catalog has no "Orange"
entry. Best-fit colors for this print (red panda fur + peaches on ivory)
are **Beige + Red + Floral** — retried and all 22 metafields wrote cleanly.
Runner script on disk has been patched with the correct Red GID.

## Tags

```
Mommy and Me, Pajamas, Matching Family Pajamas, Long Sleeve Pajamas, Summer,
Cream, Ivory, Orange, Peach, Red Panda, Panda, Animal, Fruit, Watercolor,
Cotton, Cotton Blend, Loungewear, Four-Layer Gauze,
Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr,
Mother S, Mother M, Mother L, Mother XL,
https://detail.1688.com/offer/828526529351.html
```

## Smart collections joined

- Pajamas
- New Arrivals
- New Mommy & Me
- Popular Mommy & Me
- Mommy and Me Matching Outfits for Mother and Daughter

## Publications (5/5 ok)

- Online Store — `gid://shopify/Publication/55169925`
- Google & YouTube — `gid://shopify/Publication/21969633377`
- Facebook & Instagram — `gid://shopify/Publication/29172400225`
- Pinterest — `gid://shopify/Publication/76582879329`
- TikTok — `gid://shopify/Publication/76604768353`

## Phase 6 verification result

All 21 checks **PASS**: title ≤70, SEO title ≤60, SEO desc ≤155, status=ACTIVE,
publishedAt + onlineStoreUrl populated, taxonomy set, 11 variants all
DENY/tracked/requireShipping/priced, SKUs match derived, size table is
10 columns × 11 data rows, every picker label present verbatim, age column
fully populated, waist column dual-unit populated, all 21 required metafields
written, required tags present, mother-size tags only for variants that exist,
smart collections joined.

## Manual follow-ups

- **Images:** no `uploads/red-panda-mommy-and-me-pajamas/` folder exists.
  Drop product photos (2 supplied with the brief + any additional angles)
  into `/Users/fsuels/Projects/dresslikemommy/uploads/red-panda-mommy-and-me-pajamas/`
  and re-run the script — the media block is idempotent on the presence
  of that directory.
- **Real shipping weight (grams):** placeholder not set; add in admin once
  a vendor sample arrives.
- **Inventory quantity:** variants are `tracked=true` / policy=`DENY` but
  no qty was set — inventory defaults to 0 and the variants will show
  "sold out" until qty is pushed. Add starting stock via admin or
  `inventoryAdjustQuantities` once received.
- **Smart-collection reindex:** already joined 5 collections per Phase 6;
  no reindex needed. If Google Shopping / Pinterest feeds lag, allow the
  standard 24h feed-refresh window.

## Files

- Listing doc: `red-panda-mommy-and-me-pajamas-listing.md`
- Backup CSV: `red-panda-mommy-and-me-pajamas-shopify-import.csv`
- Runner:     `ops/scripts/create-vcf-red-panda-mommy-and-me-pajamas.sh`
