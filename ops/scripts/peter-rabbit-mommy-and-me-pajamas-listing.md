# Peter Rabbit Mommy and Me Pajamas — Short-Sleeve Set

- **Handle:** `peter-rabbit-mommy-and-me-pajamas`
- **Product ID:** `gid://shopify/Product/7533379059809`
- **Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/7533379059809
- **Live URL:** https://www.dresslikemommy.com/products/peter-rabbit-mommy-and-me-pajamas
- **Vendor URL:** https://detail.1688.com/offer/792917229223.html
- **Category:** Pajamas → `Matching Family Pajamas`
- **Taxonomy GID:** `gid://shopify/TaxonomyCategory/aa-1-17-4`
- **Print name:** Peter Rabbit (彼得兔) — watercolor bunnies + wildflowers + foliage, ivory ground
- **Fabric:** 100% Cotton (vendor: 纯棉)
- **Colorway / Color option:** Peter Rabbit
- **Color token (SKU):** `CREAM`
- **Shortcode:** `VCF`
- **Designs listed:** Peter Rabbit – adult version, Peter Rabbit – children's version (vendor SKUs: 彼得兔-成人款, 彼得兔-儿童款)

## SIZE_CHART (single source of truth — vendor 尺码参数 + vendor age labels)

Vendor offers 3 child sizes (1-2岁 / 3-4岁 / 5-6岁) + adult 均码.
Picker labels mirror the vendor ages exactly (Child 1-2 Years / Child 3-4 Years / Child 5-6 Years),
rather than mapping to the default scheme. Adult 均码 → one `Mother One Size` variant
(not expanded to S/M/L/XL).

| Vendor label | Audience | Picker label | SKU suffix | Garment Length | ½ Chest | ½ Hem | Sleeve | Cuff | Age | Height | Weight |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 儿童S码（推荐1-2岁） | child | Child 1-2 Years | KID12Y | 54 cm | 33 cm (66 full) | 49.5 cm (99 full) | 19 cm | 12 cm | 1–2 | 80–90 cm | 10–13 kg |
| 儿童M码（推荐3-4岁） | child | Child 3-4 Years | KID34Y | 64 cm | 35 cm (70 full) | 51.5 cm (103 full) | 20 cm | 12.5 cm | 3–4 | 95–105 cm | 14–17 kg |
| 儿童L码（推荐5-6岁） | child | Child 5-6 Years | KID56Y | 74 cm | 37 cm (74 full) | 55.5 cm (111 full) | 21.5 cm | 13 cm | 5–6 | 110–120 cm | 18–22 kg |
| 成人均码（推荐75kg内） | mother | Mother One Size | MOMOS | 102 cm | 57 cm (114 full) | 72 cm (144 full) | 30 cm | 21.5 cm | — | 155–175 cm | up to ~75 kg |

## Variants & SKUs

| Picker | SKU | Price | Compare-at | Variant ID |
|---|---|---|---|---|
| Child 1-2 Years × Peter Rabbit | `DLM-VCF-KID12Y-CREAM` | 28.99 | 33.49 | 44046661386337 |
| Child 3-4 Years × Peter Rabbit | `DLM-VCF-KID34Y-CREAM` | 28.99 | 33.49 | 44046661419105 |
| Child 5-6 Years × Peter Rabbit | `DLM-VCF-KID56Y-CREAM` | 28.99 | 33.49 | 44046661451873 |
| Mother One Size × Peter Rabbit | `DLM-VCF-MOMOS-CREAM` | 31.99 | 36.99 | 44046661484641 |

## Title / SEO

- **Product title** (52): `Peter Rabbit Mommy and Me Pajamas — Short-Sleeve Set`
- **SEO title** (50): `Peter Rabbit Mommy & Me Pajamas | Dress Like Mommy`
- **SEO description** (136): `Shop our Peter Rabbit matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. Sizes 3Y, 5Y, 8Y & Mom One Size.`

*(SEO description size phrase not yet refreshed to the new age ranges — intentionally left at length-safe wording; can be updated to `Sizes 1–2Y, 3–4Y, 5–6Y & Mom One Size.` if desired; count = 147.)*

## Tags (live)

`Mommy and Me`, `Pajamas`, `Matching Family Pajamas`, `Short Sleeve Pajamas`, `Summer`,
`Cream`, `Ivory`, `Peter Rabbit`, `Bunny`, `Rabbit`, `Watercolor`, `Floral`, `Storybook`,
`Cotton`, `Loungewear`, `Raglan Sleeve`, `Easter`, `Child 1-2yr`, `Child 3-4yr`, `Child 5-6yr`,
`Mother One Size`, VENDOR_URL.

## Metafields written (22 universal + 5 shopify.* lists)

Universal + category: `custom.category1`, `custom.subcategory`, `custom.subcategory2`,
`custom.pattern`, `custom.style`, `custom.type`, `mm-google-shopping.custom_product`,
`mm-google-shopping.gender`, `mm-google-shopping.age_group`, `mm-google-shopping.condition`,
`mm-google-shopping.custom_label_0..4`, `shopify.age-group`, `shopify.color-pattern`,
`shopify.fabric`, `shopify.size`, `shopify.target-gender`, `global.title_tag`,
`global.description_tag`.

`shopify.size` GIDs (updated to match vendor ages):
- Child 1-2 Years → `gid://shopify/Metaobject/129972863073` (catalog entry "2-3 years", closest match)
- Child 3-4 Years → `gid://shopify/Metaobject/129972895841` (catalog entry "3-4 years", exact)
- Child 5-6 Years → `gid://shopify/Metaobject/129972961377` (catalog entry "5-6 years", exact)
- Mother One Size → no catalog entry → skipped per Phase-1 contract (no faked GIDs)

Intentionally skipped (with reason):
- `shopify.sleeve-length-type` — Store enforces subtype rejection on Matching Family Pajamas.
- `shopify.neckline`, `shopify.dress-*`, `shopify.skirt-dress-length-type` — Dresses/Tops only.
- `shopify.size` Mother One Size — no catalog entry.
- `shopify.clothing-features` — no stable catalog entries; neighbors omit.

## Collections (auto-populated)

- Pajamas
- New Arrivals
- New Mommy & Me
- Popular Mommy & Me
- Mommy and Me Matching Outfits for Mother and Daughter

## Manual follow-ups

- [ ] Upload product images (lifestyle + flat-lay + vendor size-chart) to `/Users/fsuels/Projects/dresslikemommy/uploads/peter-rabbit-mommy-and-me-pajamas/`.
- [ ] Confirm real variant weight in grams (current placeholders: 300/320/360 g child, 400 g mother).
- [ ] Set inventory quantity at default location when stock arrives.

## Change log

- 2026-04-21 — Product created with 4 variants, metafielded, published to 5 channels.
- 2026-04-21 — Size picker labels renamed to match vendor ages exactly: Child 3 Years → Child 1-2 Years, Child 5 Years → Child 3-4 Years, Child 8 Years → Child 5-6 Years. SKUs renamed to `KID12Y`/`KID34Y`/`KID56Y`. `shopify.size` GIDs updated. Body HTML rebuilt with realigned recommended weight/height ranges. Tags replaced (`Child 2-3yr`/`Child 4-5yr`/`Child 6-8yr` → `Child 1-2yr`/`Child 3-4yr`/`Child 5-6yr`). All changes scoped to product `7533379059809` only — no other listings affected.
