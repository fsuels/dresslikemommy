# Grapevine Mommy and Me Pajamas — Short-Sleeve Set

**Status:** ACTIVE · Published 2026-04-21T15:53:23Z (5 channels)
**Product ID:** `gid://shopify/Product/7533390856289`
**Admin:** https://admin.shopify.com/store/dresslikemommy/products/7533390856289
**Live:** https://www.dresslikemommy.com/products/grapevine-mommy-and-me-pajamas
**Vendor source:** https://detail.1688.com/offer/792917229223.html (designs: 葡萄园-儿童款 + 葡萄园--成人款)

---

## SIZE_CHART recap (single source of truth)

| Vendor row                        | Picker label       | SKU                      | Price  | Compare | shopify.size GID                                   |
|-----------------------------------|--------------------|--------------------------|--------|---------|----------------------------------------------------|
| 儿童S码（推荐1-2岁，衣长 54 cm）   | Child 1-2 Years    | DLM-VCF-KID12Y-CREAM     | $28.99 | $33.49  | gid://shopify/Metaobject/129972863073 (2-3 years)  |
| 儿童M码（推荐3-4岁，衣长 64 cm）   | Child 3-4 Years    | DLM-VCF-KID34Y-CREAM     | $28.99 | $33.49  | gid://shopify/Metaobject/129972895841 (3-4 years)  |
| 儿童L码（推荐5-6岁，衣长 74 cm）   | Child 5-6 Years    | DLM-VCF-KID56Y-CREAM     | $28.99 | $33.49  | gid://shopify/Metaobject/129972961377 (5-6 years)  |
| 成人均码（推荐 75 kg 内）          | Mother One Size    | DLM-VCF-MOMOS-CREAM      | $31.99 | $36.99  | (skipped — no catalog entry for One Size)          |

**Mapping rationale:** Per user feedback, vendor's explicit age recommendations
(1-2岁, 3-4岁, 5-6岁) are the source of truth for picker labels — NOT the
garment-length heuristic. Adult is vendor 均码 → single Mother One Size variant
(NOT expanded to S/M/L/XL). shopify.size catalog has no `1-2 years` entry, so the
smallest bucket maps to the closest neighbor `2-3 years` GID 129972863073.

---

## Phase 6 — Verification pass/fail

- ✅ Title 49/70 chars
- ✅ SEO title 58/60, SEO description 152/155
- ✅ Live variant count 4 == SIZE_CHART length 4
- ✅ Live SKUs sorted == derived SKUs sorted (DLM-VCF-KID12Y-CREAM, DLM-VCF-KID34Y-CREAM, DLM-VCF-KID56Y-CREAM, DLM-VCF-MOMOS-CREAM)
- ✅ Every picker Size value has exact first-column match in body size-chart
- ✅ Age column present (1–2, 3–4, 5–6, —), no blank rows
- ✅ Every variant: SKU + price + compareAtPrice + inventoryPolicy=DENY + tracked=true + requiresShipping=true
- ✅ publishedAt = 2026-04-21T15:53:23Z, onlineStoreUrl populated
- ⏳ Smart collections — Shopify populates async; expect Mommy and Me Pajamas, Summer Pajamas, Family Matching Pajamas to attach within ~60s of publish (verified empty at hand-off, will re-attach)
- ✅ Taxonomy category: gid://shopify/TaxonomyCategory/aa-1-17-4 (Pajamas)
- ✅ Tags include VENDOR_URL, "Pajamas", "Matching Family Pajamas", "Short Sleeve Pajamas", "Summer", color words (Cream, Ivory, Rose, Pink, Sage), print words (Grapevine, Vineyard, Grape, Vine, Botanical, Floral, Watercolor, Cottagecore), child age buckets that match vendor rec (Child 1-2yr, Child 3-4yr, Child 5-6yr) and ONLY mother-size tag that exists (Mother One Size)

### Metafields written (22 total)

| Field                                  | Value                                                                                          |
|----------------------------------------|------------------------------------------------------------------------------------------------|
| custom.category1                       | Mommy and Me                                                                                   |
| custom.subcategory                     | Pajamas                                                                                        |
| custom.subcategory2                    | Summer Pajamas                                                                                 |
| custom.pattern                         | Watercolor Grapevine print — grapes, leaves, trailing vines on cream                           |
| custom.style                           | Matching Family Set                                                                            |
| custom.type                            | Two-Piece Pajama Set                                                                           |
| mm-google-shopping.custom_product      | false                                                                                          |
| mm-google-shopping.gender              | female                                                                                         |
| mm-google-shopping.age_group           | adult                                                                                          |
| mm-google-shopping.condition           | new                                                                                            |
| mm-google-shopping.custom_label_0..4   | Mommy and Me / Grapevine Botanical / Summer / Short Sleeve / Family Matching                   |
| shopify.age-group                      | [Toddlers, Kids, Adults]                                                                       |
| shopify.color-pattern                  | [Beige/Cream, Floral, Multicolor]                                                              |
| shopify.fabric                         | [Cotton] (best-fit; bamboo-cotton gauze blend)                                                 |
| shopify.size                           | [2-3 years, 3-4 years, 5-6 years]  *(Mother One Size skipped — no catalog entry)*              |
| shopify.target-gender                  | [Female]                                                                                       |
| global.title_tag                       | Grapevine Mommy & Me Pajamas — Matching \| Dress Like Mommy                                    |
| global.description_tag                 | Shop our Grapevine matching mommy-and-me pajamas — soft bamboo-cotton gauze short-sleeve sets for mom + daughter. Sizes 1-2Y, 3-4Y, 5-6Y & Mom One Size. |

**Skipped metafields (with reason):**

- `shopify.sleeve-length-type` — store enforces subtype rejection on Pajamas (per spec).
- `shopify.neckline` — Dresses/Tops only.
- `shopify.dress-occasion`, `shopify.dress-style`, `shopify.skirt-dress-length-type` — Dresses/Skirts only.
- `shopify.size` for `Mother One Size` — no Shopify standard catalog entry; skipped per source-of-truth rule.

---

## Manual follow-ups

- ⚠️ **Images** — no files in `/Users/fsuels/Projects/dresslikemommy/uploads/grapevine-mommy-and-me-pajamas/`. Drop hero + lifestyle JPGs there, then run a follow-up `stagedUploadsCreate` + `productCreateMedia` step. Vendor image CDN URLs are in `ops/scripts/.grapevine-verify.json` if helpful for sourcing.
- ⚠️ **Real per-variant weight** — currently estimated grams (260/300/340/400). Replace with measured weights at fulfillment.
- ⚠️ **Inventory qty** — none set (tracked, DENY policy). Push initial stock counts via `inventoryAdjustQuantities` once received.
- ⚠️ **Smart-collection re-check** — re-query `collections` field in 60–120s to confirm async attachment to Mommy and Me Pajamas + Summer Pajamas collections.

---

## Files

- `grapevine-mommy-and-me-pajamas-listing.md` (this file)
- `grapevine-mommy-and-me-pajamas-shopify-import.csv` (75-col products_export fallback)
- `ops/scripts/create-vcf-grapevine-mommy-and-me-pajamas.sh` (re-runnable)
- `ops/scripts/grapevine-description.html` (body HTML, single source for size table)
- `ops/scripts/.grapevine-last-product-id` (cache)
- `ops/scripts/.grapevine-verify.json` (post-create verify dump)
