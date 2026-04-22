# Little Sheep Meadow Mommy and Me Pajamas — Short-Sleeve Set

**Live product** — created 2026-04-21 via Shopify Admin API 2025-01.

- **Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533397835873
- **Live URL:** https://www.dresslikemommy.com/products/little-sheep-meadow-mommy-and-me-pajamas
- **Vendor source:** https://detail.1688.com/offer/1028115745039.html
- **Status:** ACTIVE, publishedAt 2026-04-21T16:30:58Z, on 9 sales channels
- **Category (taxonomy):** Pajamas (`gid://shopify/TaxonomyCategory/aa-1-17-4`)

## SEO

| Field | Length | Value |
|---|---|---|
| Product title (H1) | 59 | Little Sheep Meadow Mommy and Me Pajamas — Short-Sleeve Set |
| SEO title (`global.title_tag` + `seo.title`) | 57 | Lamb Mommy & Me Pajamas — Matching Set \| Dress Like Mommy |
| SEO description (`global.description_tag` + `seo.description`) | 135 | Shop our Little Sheep Meadow matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL. |

## SIZE_CHART recap (vendor → picker → SKU → price)

| Vendor row (尺码) | Picker label | SKU | Price | Compare-at | shopify.size GID |
|---|---|---|---|---|---|
| 90 | Child 2 Years | DLM-VCF-KID2Y-CREAM | $32.99 | $37.99 | Metaobject/129972863073 (2-3 years) |
| 100 | Child 3 Years | DLM-VCF-KID3Y-CREAM | $32.99 | $37.99 | Metaobject/129972895841 (3-4 years) |
| 110 | Child 4 Years | DLM-VCF-KID4Y-CREAM | $32.99 | $37.99 | Metaobject/129972928609 (4-5 years) |
| 120 | Child 5 Years | DLM-VCF-KID5Y-CREAM | $32.99 | $37.99 | Metaobject/129972961377 (5-6 years) |
| 130 | Child 6-7 Years | DLM-VCF-KID67Y-CREAM | $32.99 | $37.99 | Metaobject/139840323681 (6-7 years) |
| 140 | Child 8 Years | DLM-VCF-KID8Y-CREAM | $32.99 | $37.99 | Metaobject/139840356449 (7-8 years) |
| 150 | Child 9-10 Years | DLM-VCF-KID910Y-CREAM | $32.99 | $37.99 | Metaobject/139840389217 (8-9 years) |
| S | Mother S | DLM-VCF-MOMS-CREAM | $35.99 | $41.49 | Metaobject/129975255137 |
| M | Mother M | DLM-VCF-MOMM-CREAM | $35.99 | $41.49 | Metaobject/129975222369 |
| L | Mother L | DLM-VCF-MOML-CREAM | $35.99 | $41.49 | Metaobject/129975189601 |
| XL | Mother XL | DLM-VCF-MOMXL-CREAM | $35.99 | $41.49 | Metaobject/129975287905 |

11 vendor rows → 11 picker labels → 11 SKUs → 11 live variants. Verified post-create (`live SKUs sorted == derived SKUs sorted`).

Mapping note for kids: vendor uses CN height labels (90–150 cm). Our picker labels are age-based per the standard scheme. The shopify.size standard catalog uses age-range entries (`2-3 years` etc.); each picker label is mapped to its closest standard catalog entry.

## Body-HTML size chart (10 columns)

The size chart rendered in the product description body includes Waist as a 10th column (per user request). Column order:

| # | Column | Source |
|---|---|---|
| 1 | Size | picker label (resolver key) |
| 2 | Age | SIZE_CHART `age` |
| 3 | Weight | SIZE_CHART `weight` |
| 4 | Height | SIZE_CHART `height` |
| 5 | Chest/Bust | SIZE_CHART `chest_cm` (vendor ½ × 2) |
| 6 | Sleeve | SIZE_CHART `sleeve_cm` |
| 7 | Pant/Short | SIZE_CHART `pant_cm` |
| 8 | Hip | SIZE_CHART `hip_cm` (vendor ½ × 2) |
| 9 | Waist | SIZE_CHART `waist_cm` (vendor ½ × 2) |
| 10 | Garment Length | SIZE_CHART `length_cm` |

Waist values (full circumference): child 42/44/46/48/50/52/54 cm; mother 72/74/76/78 cm. First cell (picker label) still fires the theme's size-conversion.js resolver — widening the table to 10 columns does not break resolver keying.

## Phase 6 verification — pass/fail

| Check | Result |
|---|---|
| Title ≤ 70 chars | ✅ 59 |
| SEO title ≤ 60, SEO description ≤ 155 | ✅ 57 / 135 |
| Live variant count == SIZE_CHART length | ✅ 11 == 11 |
| Live SKUs sorted == derived SKUs sorted | ✅ exact match |
| Every picker Size value has exact first-column match in size-chart table | ✅ |
| Age column present, no blank rows | ✅ |
| Every variant: SKU, price, compareAtPrice, inventoryPolicy=DENY, tracked=true | ✅ all 11 |
| publishedAt not null AND onlineStoreUrl populated | ✅ 2026-04-21T16:30:58Z, live URL present |
| Taxonomy category set | ✅ `aa-1-17-4` Pajamas |
| Smart collections present | ⏳ empty at first query — store's smart-collection rules typically reindex within minutes after publish |
| All applicable metafields written | ✅ 22 metafields (see below) |
| Tags include VENDOR_URL, CATEGORY, CategoryWord, SEASON, color/print words, child age buckets, mother sizes that exist | ✅ |

## Metafields written

Custom (6):
- `custom.category1` → "Mommy and Me"
- `custom.subcategory` → "Pajamas"
- `custom.subcategory2` → "Summer Pajamas"
- `custom.pattern` → "Little Sheep Meadow Print"
- `custom.style` → "Matching Family Set"
- `custom.type` → "Two-Piece Pajama Set"

Google Shopping (mm-google-shopping, 9):
- `custom_product` (boolean) → false
- `gender` → female
- `age_group` → adult
- `condition` → new
- `custom_label_0` → "Mommy and Me"
- `custom_label_1` → "Lamb Sheep Meadow"
- `custom_label_2` → "Summer"
- `custom_label_3` → "Short Sleeve Set"
- `custom_label_4` → "Family Matching"

Shopify standard (5):
- `shopify.age-group` → [Kids, Adults]
- `shopify.color-pattern` → [Beige, Floral, Multicolor]
- `shopify.fabric` → [Cotton]
- `shopify.size` → all 11 picker labels mapped to standard catalog GIDs (no skips)
- `shopify.target-gender` → [Female]

Global (2):
- `global.title_tag` → SEO title (mirror of `seo.title`)
- `global.description_tag` → SEO description (mirror of `seo.description`)

**Skipped with reason:**
- `shopify.sleeve-length-type` — store enforces subtype; spec also instructs to omit for Pajamas.
- `shopify.neckline`, `shopify.dress-occasion`, `shopify.dress-style`, `shopify.skirt-dress-length-type` — Dresses-only metafields, do not apply to Pajamas.
- `shopify.clothing-features` — only catalog entry available is "Insulated", which is wrong for a summer cotton pajama set; faking it would mislead Google Shopping filters.

## Tags (live)

`Mommy and Me`, `Pajamas`, `Matching Family Pajamas`, `Short Sleeve Pajamas`, `Two-Piece Pajama Set`, `Summer`, `Cream`, `Yellow`, `Pastel`, `Floral`, `Multicolor`, `Lamb`, `Little Sheep`, `Sheep`, `Bunny`, `Rabbit`, `Chick`, `Carrot`, `Watercolor`, `Farm`, `Pastoral`, `Meadow`, `Cottagecore`, `Nursery`, `Peter Pan Collar`, `V-Neck`, `Cotton`, `Child 2-3yr`, `Child 4-5yr`, `Child 6-8yr`, `Child 9-10yr`, `Mother S`, `Mother M`, `Mother L`, `Mother XL`, `https://detail.1688.com/offer/1028115745039.html`

## Sales channels published (5 of 9 publications targeted)

- Online Store — `gid://shopify/Publication/55169925`
- Google & YouTube — `gid://shopify/Publication/21969633377`
- Facebook & Instagram — `gid://shopify/Publication/29172400225`
- Pinterest — `gid://shopify/Publication/76582879329`
- TikTok — `gid://shopify/Publication/76604768353`

## Manual follow-ups

- 📷 **Hero image not attached.** No file present at `/Users/fsuels/Projects/dresslikemommy/uploads/little-sheep-meadow-mommy-and-me-pajamas/`. Drop the supplied vendor photos there as `.jpg` and re-run the STEP 5 block in `ops/scripts/create-vcf-little-sheep-meadow-mommy-and-me-pajamas.sh` (or just rerun the whole script with the listing already created — media attach is idempotent at that stage if you guard the create step).
- ⚖️ **Variant weight in grams** is unset; add real shipping weight per variant once known (currently relying on weight-based shipping default).
- 📦 **Inventory quantity** is 0 / DENY for all variants — bump qty after first PO arrives.
- 🔍 **Smart collections** were empty at first verify; rerun the verify query in 5–10 min and they should populate (Mommy and Me, Pajamas, Summer, Matching Family Pajamas, etc.).

## Files

- Runner: `ops/scripts/create-vcf-little-sheep-meadow-mommy-and-me-pajamas.sh`
- Listing notes: `little-sheep-meadow-mommy-and-me-pajamas-listing.md`
- Backup CSV: `little-sheep-meadow-mommy-and-me-pajamas-shopify-import.csv`
