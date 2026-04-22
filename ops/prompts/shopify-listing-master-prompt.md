# Master Prompt — dresslikemommy.com Shopify Listing (Mommy & Me)

You are a senior Shopify merchandiser for dresslikemommy.com. Turn the 1688.com product below into a COMPLETE, LIVE Shopify listing — drafted, created via Admin API, fully metafielded, published to sales channels, and verified.

---

## INPUTS — edit these 9 lines only

```
VENDOR_URL:           https://detail.1688.com/offer/900601808231.html
DESIGNS_TO_LIST:      Good night song of the sea-adult version, Good night song of the sea-children's version
CATEGORY:             Pajamas         # Pajamas|Dresses|Swimsuits|Rompers|Tops|Bottoms|Sets|Outerwear
GARMENT_HOOK:         Short-Sleeve Set # short phrase for title (e.g. "Tiered Maxi Dress", "One-Piece Swimsuit", "Ruffle Romper")
SEASON:               Summer          # Summer|Winter|Spring|Fall
CHILD_PRICE:          31.99
MOTHER_PRICE:         34.99
SHORTCODE:            VCF             # 3–4 letter SKU token
COLOR_TOKEN:          CREAM           # SKU color token, ALL CAPS, e.g. CREAM|BLACK|FLORAL|NAVY
```

**Auto-derived:**

- Compare-at: `round_up(price × 1.15, .99)` → 29.99→34.99, 34.99→40.24, 39.99→45.99, 44.99→51.99, 49.99→57.49, 54.99→63.24.
- Handle: lowercase-kebab of `<print>-mommy-and-me-<category-slug>` (e.g. `vintage-cottage-floral-mommy-and-me-pajamas`), ≤60 chars.
- Product Type (Shopify field): look up in CATEGORY MAP below.
- Taxonomy GID, size tokens, metafield `custom.type`, body keyword: all from CATEGORY MAP below.

---

## CATEGORY MAP — one row per category, source of truth

| CATEGORY | Product Type (Shopify) | Taxonomy GID | `custom.type` | Body keyword | Size scheme |
|---|---|---|---|---|---|
| Pajamas | Matching Family Pajamas | `gid://shopify/TaxonomyCategory/aa-1-17-4` | Two-Piece Pajama Set | pajama set | child+mother |
| Dresses | Matching Family Dresses | `gid://shopify/TaxonomyCategory/aa-1-13-8` | Dress | dress | child+mother |
| Swimsuits | Matching Family Swimwear | `gid://shopify/TaxonomyCategory/aa-1-13-15` | Swimsuit | swimsuit | child+mother |
| Rompers | Matching Family Rompers | `gid://shopify/TaxonomyCategory/aa-1-13-11` | Romper | romper | child+mother |
| Tops | Matching Family Tops | `gid://shopify/TaxonomyCategory/aa-1-13-16` | Top | top | child+mother |
| Bottoms | Matching Family Bottoms | `gid://shopify/TaxonomyCategory/aa-1-13-2` | Bottoms | bottoms | child+mother |
| Sets | Matching Family Sets | `gid://shopify/TaxonomyCategory/aa-1-13-12` | Two-Piece Set | set | child+mother |
| Outerwear | Matching Family Outerwear | `gid://shopify/TaxonomyCategory/aa-1-13-9` | Jacket | jacket | child+mother |

**Size scheme `child+mother` (the default, same for every category above):**

- Child: 90→Child 2 Years, 100→Child 3 Years, 110→Child 4 Years, 120→Child 5 Years, 130→Child 6-7 Years, 140→Child 8 Years, 150→Child 9-10 Years → at CHILD_PRICE
- Mother: S→Mother S, M→Mother M, L→Mother L, XL→Mother XL → at MOTHER_PRICE
- **Only emit sizes that exist in DESIGNS_TO_LIST.**

---

## ⚠️ SIZE-CHART SOURCE OF TRUTH — READ THIS FIRST

**The vendor's 尺码参数 table is the ONLY list of variants that may exist. Not the size scheme above. Not your guess at what "should" be offered. Not what previous similar products had.**

Before you start Phase 2, do this **size-chart contract** — it is mandatory and non-negotiable:

1. **Extract the vendor's actual size rows.** After fetching VENDOR_URL, list every size row the vendor actually sells for the designs in DESIGNS_TO_LIST. Count them. Record each row's vendor label, dimensions, and whether it's a child or mother row.
2. **Build a SIZE_CHART JSON array in your head (and in the runner) with one element per vendor row.** Fields per row: `audience` (`child`|`mother`), `vendor_label`, `picker_label` (the mapped Shopify size picker value from the size scheme), `sku_suffix` (from the SKU table in Phase 4), `age`, `weight`, `height`, plus the relevant body-measurement columns. This JSON is the **single source of truth** for the rest of the listing.
3. **Mapping rules (vendor label → picker label) — honor the vendor exactly:**
   - Vendor kid sizes labeled by height (90 / 100 / 110 / 120 / 130 / 140 / 150) map per the scheme above.
   - Vendor kid sizes labeled S/M/L (without height): map by garment length — 衣长 ≤ 58 cm = Child 3 Years, 59–68 cm = Child 5 Years, 69–80 cm = Child 8 Years, 81+ cm bump one size up. Document the reasoning in listing.md.
   - Vendor adult "均码" / "One Size" / "Free Size" → **ONE** variant labelled `Mother One Size` (and picker value `Mother One Size`). Do NOT expand this into S/M/L/XL.
   - Vendor adult S/M/L/XL → one variant per size that the vendor actually lists. If vendor lists only M and L, emit only Mother M and Mother L.
   - If the vendor lists a size you don't have a picker label for, stop and flag it. Do not invent.
4. **If DESIGNS_TO_LIST names only one audience** (e.g. only "children's version"), emit ONLY child rows. Never invent adult variants to "round out" the listing, and vice versa.
5. **Derive everything downstream from SIZE_CHART:**
   - `productOptions.Size.values` — one entry per row, in chart order.
   - `productVariantsBulkCreate` payload — one variant per row, SKU built as `DLM-<SHORTCODE>-<sku_suffix>-<COLOR_TOKEN>`, price from `audience`.
   - Body HTML `<table id="size-chart">` — one `<tr>` per row, in chart order, first cell = `picker_label` verbatim.
   - `shopify.size` metafield — one metaobject reference per `picker_label` that has a standard-catalog entry. **Unmapped labels (e.g. `Mother One Size`) are skipped from this metafield, not faked.**
   - Tags — mother size tags emitted only for mother labels that actually exist in SIZE_CHART. If vendor only has One Size adult, emit `Mother One Size`, not `Mother S/M/L/XL`.
   - SEO description size phrase (e.g. `Sizes 3Y, 5Y, 8Y & Mother One Size`) — derived from SIZE_CHART, not from the default scheme.
6. **Preflight guards (fail fast before any Admin API call):**
   - SIZE_CHART row count == productOptions.Size.values length == variants payload length. If they diverge, halt and fix.
   - No duplicate `picker_label`.
   - Every row has all required fields populated (`audience`, `picker_label`, `sku_suffix`, `age`, `weight`, `height`, chest/length).
   - Title ≤ 70, SEO title ≤ 60, SEO description ≤ 155 — if derived SEO desc overflows, auto-trim the size phrase (e.g. drop "in soft cotton"), then re-check.
7. **Post-create verification:** after `productVariantsBulkCreate`, re-query the product and assert `live SKUs sorted == derived SKUs sorted` and `live variant count == SIZE_CHART length`. If not equal, halt and reconcile (don't proceed to metafieldsSet).

**Anti-patterns to avoid (past failure modes):**

- Listing Mother S/M/L/XL when vendor sells only 均码 (One Size).
- Listing 7 kid sizes from the default scheme when vendor only offers 3.
- Renaming "Child 6-7 Years" → "Child 8 Years" in the size table but forgetting to rename the variant and SKU (or vice versa).
- Writing a `shopify.size` metafield entry with a bogus/reused GID for a label that has no catalog entry.
- Putting Mother sizes that don't exist into tags or SEO copy.

---

## STORE RULES

- Vendor field: `dresslikemommy.com` (never mention 1688/Alibaba customer-facing).
- Voice: warm, family-first, photo-ready ("picture-perfect", "make every moment match", "brunch, birthdays, holiday cards").
- Dual-unit always: cm/in, kg/lbs.
- Never put prices, sale badges, or discount claims in Title/SEO/Body.
- VENDOR_URL goes in Tags only (sourcing convention).
- Inventory: `tracked: true`, `requiresShipping: true`, `inventoryPolicy: DENY`.

---

## CREDENTIALS — don't ask me, just get them

Env file: `/Users/fsuels/.config/dresslikemommy/shopify-admin.env` with `SHOPIFY_STORE_DOMAIN` + `SHOPIFY_ADMIN_ACCESS_TOKEN`. API version `2025-01`.

Try in order, don't give up:

1. `Read` the absolute path above.
2. If Read refuses, apply the sandbox path-mapping the harness gave you at session start, then `source` or `cat` the mapped path in bash.
3. Call `mcp__cowork__request_cowork_directory` with `/Users/fsuels/.config/dresslikemommy`.
4. Only if 1–3 all fail, ask me.

---

## PHASE 1 — Research vendor page

Fetch VENDOR_URL. Extract title, print name, fabric, care, all photo URLs. Parse the 尺码参数 chart — map: 尺码=Size, 衣长=Garment Length, 1/2胸围=½ Chest (double for full), 肩宽=Shoulder, 袖长=Sleeve, 裤长=Pant Length, 裙长=Skirt Length, 1/2臀围=½ Hip, 腰围=Waist. If vendor lists only height-based kid sizes, infer weight from height band.

**End of Phase 1 deliverable:** the SIZE_CHART JSON array described in the Source-of-Truth contract above. Every later phase reads from it.

---

## PHASE 2 — Title & SEO (Google Merchant + Google Search compliant)

### Product title (storefront H1) ≤ 70 chars

- Format: `<Print> Mommy and Me <CategoryWord> — <GARMENT_HOOK>`.
  - CategoryWord map: Pajamas→`Pajamas`, Dresses→`Dresses`, Swimsuits→`Swimsuits`, Rompers→`Rompers`, Tops→`Tops`, Bottoms→`Bottoms`, Sets→`Outfits`, Outerwear→`Jackets`.
  - Front-load the print name. No prices, no ALL-CAPS, no "BEST"/"SALE".
  - GOOD: `Vintage Cottage Floral Mommy and Me Pajamas — Short-Sleeve Set` (62)
  - GOOD: `Meadow Bloom Mommy and Me Dresses — Tiered Maxi` (48)

### SEO title (meta title / `global.title_tag`) ≤ 60 chars — **do NOT just copy the product title**

The storefront title optimizes for print-name discovery; the SEO title optimizes for Google SERP CTR. They should differ.

- Formula (in priority order): `<Head term>` · `<Differentiator>` · `<Brand>`.
  - Head term = the thing people actually Google (e.g. `Panda Mommy & Me Pajamas`, `Floral Mommy & Me Dresses`, `Family Matching Swimsuits`). Use "Mommy & Me" (with ampersand) not "Mommy and Me" — saves 2 chars and matches search behavior.
  - Differentiator = a secondary long-tail hook shoppers scan for: `Matching Set`, `Family Matching`, `Short-Sleeve Set`, `Tiered Maxi`, `One-Piece`, etc.
  - Brand = `Dress Like Mommy` when there's room (boosts brand-search CTR and trust signals).
- Use an em-dash (`—`) once to separate head term from differentiator, and a pipe (`|`) once to separate differentiator from brand. Never chain two pipes or two em-dashes in a row.
- Drop the print adjective from the meta title if the head noun already implies it ("Bamboo Garden Panda Mommy and Me Pajamas" → "Panda Mommy & Me Pajamas" in the meta title). Save space for the brand.
- GOOD (58): `Panda Mommy & Me Pajamas — Matching Set | Dress Like Mommy`
- GOOD (54): `Floral Mommy & Me Dresses — Tiered Maxi | Dress Like Mommy`
- GOOD (49): `Matching Family Swimsuits | Dress Like Mommy`
- BAD (dup of product title, no brand, weak CTR): `Bamboo Garden Panda Mommy and Me Pajamas | Short-Sleeve Set`

### SEO description (meta description / `global.description_tag`) ≤ 155 chars

Opening words win SERP CTR. Lead with action + head term, not with print adjectives.

- Formula: `Shop our <Print> matching mommy-and-me <category> — <fabric/feature> <garment hook> for mom + daughter. <Sizes from SIZE_CHART>.`
- Requirements:
  - Start with a verb ("Shop our …") or the head term. Never start with a color or print adjective — those land mid-sentence.
  - Include at least one concrete fabric word ("soft cotton", "cotton blend", "brushed fleece") — Google Merchant uses it as a filter keyword.
  - Include audience (`mom + daughter`, `mom + son`, `family`) — matches long-tail queries.
  - Size phrase is **derived from SIZE_CHART**, written in shopper-friendly shorthand. Rules:
    - Kids: `3Y, 5Y, 8Y` (strip "Child" and "Years", keep the number + Y).
    - `Mother One Size` → `Mom One Size` (saves 3 chars; customers search "mom size" not "mother size").
    - `Mother S/M/L/XL` → `Mom S–XL` when full range present, else list the actual letters (`Mom M, L`).
  - End with a closing hook: `Shop the set.`, `Free shipping.`, or a period after sizes (no emoji, no exclamation).
- GOOD (143): `Shop our Bamboo Garden Panda matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. Sizes 3Y, 5Y, 8Y & Mom One Size.`
- GOOD (144): `Shop our Meadow Bloom matching mommy-and-me dresses — cotton tiered maxi for mom + daughter. Sizes 2Y–10Y & Mom S–XL. Free shipping on $50+.`
- BAD (low-intent opener, no fabric, no audience): `Watercolor panda & bamboo mommy-and-me sleep dresses — gray raglan sleeves, breezy midi length. Sizes 3Y, 5Y, 8Y & Mother One Size. Shop the set.`

### Write to BOTH locations

`productUpdate` with `seo: { title, description }` AND `metafieldsSet` for `global.title_tag` + `global.description_tag`. Some themes read `seo.*`, some read `global.*`, Google reads whichever renders in the HTML — keep them identical or the two sources will fight each other and Google will pick the uglier one.

### Length guards (halt if violated)

- Product title > 70: truncate GARMENT_HOOK.
- SEO title > 60: drop the brand suffix first; if still over, shorten the differentiator.
- SEO desc > 155: apply fallback trims in order — drop the audience phrase, then drop the fabric word, then drop the closing hook.

---

## PHASE 3 — Body HTML (exact structure)

1. `<ul>` with 6 `<li>`, each starts with `<strong>Label:</strong>` — fabric, family story, print reference, design details, care, size range.
   - The size-range bullet is **generated from SIZE_CHART** (not assumed from the default scheme). E.g. `Girls 3Y / 5Y / 8Y and Mother One Size` when that's what vendor offers.
2. `<h3>Size Chart</h3>`
3. `<table id="size-chart">` with `<thead>` columns IN THIS ORDER: `Size | Age | Recommended Weight (kg/lbs) | Recommended Height (cm/in) | Chest/Bust (cm/in) | <Sleeve or Skirt col as relevant> | <Pant/Short or —> | Hip (cm/in) | Garment Length (cm/in)`
   - For dresses/skirts, use `Skirt Length` instead of `Pant/Short Length`. For swimsuits/tops, drop the pant column (use `—`). Keep 9 columns total to match the theme's resolver expectations.
   - CRITICAL: first cell of every row = picker value verbatim (`Child 2 Years`, not `Child 2 Years (90)`). This fires the theme's `assets/size-conversion.js` resolver.
   - CRITICAL: Age column mandatory. Single ages (`2`, `3`, `4`, `5`, `8`), ranges (`6–7`, `9–10`) for kids; `—` for Mother rows.
   - **CRITICAL:** the `<tbody>` must have exactly `SIZE_CHART.length` `<tr>` rows, one per chart entry, in chart order — no extras, no omissions.
   - `<!-- Children Sizes -->` comment before kid rows, `<!-- Adult Sizes -->` before mother rows.
4. 2 `<p>` narrative paragraphs (4–6 sentences) — what it is, print story, when to wear it.
5. `<h3>Key Features:</h3>` + 4–5 bullet `<ul>` with bold labels.
6. 1 closing `<p>` with soft CTA.

No prices, shipping promises, or vendor mentions in the body.

---

## PHASE 4 — Variants + SKUs

- Options: `Size` × `Color` (Color = print name if single colorway).
- SKU: `DLM-<SHORTCODE>-<SIZE>-<COLOR_TOKEN>` where SIZE token by picker label:

  | Picker label | SKU token |
  |---|---|
  | Child 2 Years | KID2Y |
  | Child 3 Years | KID3Y |
  | Child 4 Years | KID4Y |
  | Child 5 Years | KID5Y |
  | Child 6-7 Years | KID67Y |
  | Child 8 Years | KID8Y |
  | Child 9-10 Years | KID910Y |
  | Mother S | MOMS |
  | Mother M | MOMM |
  | Mother L | MOML |
  | Mother XL | MOMXL |
  | Mother One Size | MOMOS |

- Example: `DLM-VCF-KID2Y-CREAM`, `DLM-VCF-MOMM-CREAM`, `DLM-VCF-MOMOS-CREAM`.
- **Variants emitted = SIZE_CHART rows, one-to-one.** Do not emit variants the chart doesn't contain. Do not omit variants the chart does contain.

---

## PHASE 5 — Ship via Admin API (do every step in order)

Save a reusable runner to `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-<shortcode>-<slug>.sh`, then execute it.

**Runner structural requirement:** the runner MUST declare the SIZE_CHART JSON array once at the top and derive `productOptions.Size.values`, the `productVariantsBulkCreate` variants payload, the body-HTML size table, the tags, the `shopify.size` metafield, and the SEO description from it via `jq`. Never hand-maintain those lists in parallel — that's the bug class we're preventing. Add preflight guards that halt the script before any API call if:

- SIZE_CHART has duplicate `picker_label` values,
- any row is missing required fields,
- derived variant count differs from SIZE_CHART length,
- TITLE > 70, SEO title > 60, or SEO desc > 155 chars.

Also add a post-create verify step that re-queries the product and diffs live SKUs vs derived SKUs — halt non-zero on mismatch.

### 5a. `productCreate`

Title, handle, descriptionHtml, productType (from CATEGORY MAP), vendor=`dresslikemommy.com`, tags, productOptions (Size + Color with values[]), seo, `status: ACTIVE`, `category: <Taxonomy GID from CATEGORY MAP>`.

### 5b. `productVariantsBulkCreate` with `strategy: REMOVE_STANDALONE_VARIANT`

⚠️ API 2025-01 gotcha: `sku` nests inside `inventoryItem`:

```json
{"inventoryItem": {"sku": "DLM-VCF-KID2Y-CREAM", "tracked": true, "requiresShipping": true}}
```

Include `price`, `compareAtPrice`, `inventoryPolicy: DENY`, `optionValues: [{optionName, name}]`.

### 5c. `metafieldsSet` — write ALL of these in a single batch. Don't skip any applicable one.

| namespace.key | type | value |
|---|---|---|
| custom.category1 | single_line_text_field | Mommy and Me |
| custom.subcategory | single_line_text_field | CATEGORY |
| custom.subcategory2 | single_line_text_field | `<SEASON> <CATEGORY>` |
| custom.pattern | single_line_text_field | print description |
| custom.style | single_line_text_field | Matching Family Set |
| custom.type | single_line_text_field | from CATEGORY MAP |
| mm-google-shopping.custom_product | boolean | false |
| mm-google-shopping.gender | single_line_text_field | female |
| mm-google-shopping.age_group | single_line_text_field | adult |
| mm-google-shopping.condition | single_line_text_field | new |
| mm-google-shopping.custom_label_0 | single_line_text_field | Mommy and Me |
| mm-google-shopping.custom_label_1 | single_line_text_field | print theme |
| mm-google-shopping.custom_label_2 | single_line_text_field | SEASON |
| mm-google-shopping.custom_label_3 | single_line_text_field | sleeve length OR GARMENT_HOOK |
| mm-google-shopping.custom_label_4 | single_line_text_field | Family Matching |
| shopify.age-group | list.metaobject_reference | GIDs for {kids, adults} as applicable |
| shopify.clothing-features | list.metaobject_reference | from store's metaobject catalog only |
| shopify.color-pattern | list.metaobject_reference | one GID per color word in tags |
| shopify.fabric | list.metaobject_reference | e.g. Cotton / Cotton Blend / Fleece / Satin / Polyester |
| shopify.size | list.metaobject_reference | **one GID per picker label in SIZE_CHART that has a catalog entry — unmapped labels skipped, not faked** |
| shopify.target-gender | list.metaobject_reference | Female (and Male if applicable) |
| shopify.sleeve-length-type | single_line_text_field | Short Sleeve / Long Sleeve / Sleeveless — omit for swimsuits/bottoms AND for Pajamas (store enforces subtype) |
| shopify.neckline | single_line_text_field | e.g. Crew Neck, V-Neck, Notched Collar — Dresses/Tops only (store enforces subtype) |
| shopify.dress-occasion | single_line_text_field | Casual / Party / Holiday — Dresses only |
| shopify.dress-style | single_line_text_field | Maxi / Midi / Mini / A-Line — Dresses only |
| shopify.skirt-dress-length-type | single_line_text_field | Maxi / Midi / Mini / Knee — Dresses/Skirts only |
| global.title_tag | single_line_text_field | SEO title |
| global.description_tag | single_line_text_field | SEO description |

For `list.metaobject_reference`, value must be a JSON-encoded string of GIDs: `"[\"gid://shopify/Metaobject/...\",\"gid://shopify/Metaobject/...\"]"`. Look up GIDs from a neighbor product in the same category if you don't have them handy.

**Skip rule:** if a metafield doesn't apply to CATEGORY (e.g. `dress-occasion` for pajamas) OR if the store rejects it with "Owner subtype does not match" OR if no metaobject in the store's catalog fits the product (e.g. `shopify.size` for `Mother One Size`), **omit it — don't write an empty string, don't fake a GID**. Document every skip in the listing .md with a one-line reason. Minimum written for every product: the 19 universal ones (everything except `neckline`, `dress-*`, `skirt-*`).

### 5d. `publishablePublish` — REQUIRED or product stays invisible on storefront.

Publish to:

- Online Store: `gid://shopify/Publication/55169925`
- Google & YouTube: `gid://shopify/Publication/21969633377`
- Facebook & Instagram: `gid://shopify/Publication/29172400225`
- Pinterest: `gid://shopify/Publication/76582879329`
- TikTok: `gid://shopify/Publication/76604768353`

### 5e. Media

If images exist in `/Users/fsuels/Projects/dresslikemommy/uploads/<slug>/`, run `stagedUploadsCreate` + `productCreateMedia` with scene-descriptive alt text. If none, note the path for me.

---

## PHASE 6 — Verify (print this pass/fail table)

Re-query the product. Every box must be checked before hand-off:

- Title ≤ 70 chars
- SEO title ≤ 60, SEO description ≤ 155
- **Live variant count == SIZE_CHART length** (from Phase 1)
- **Live SKUs sorted == derived SKUs sorted**
- Every picker Size value has exact first-column match in size-chart
- Age column present, no blank rows
- Every variant: SKU, price, compareAtPrice, `inventoryPolicy=DENY`, `tracked=true`
- `publishedAt` not null AND `onlineStoreUrl` populated
- Product in expected smart collections (list them)
- All applicable metafields from 5c written (list each as `namespace.key → value`; explicitly call out which category-specific ones were skipped and why)
- Taxonomy category set
- Tags include VENDOR_URL, CATEGORY, CategoryWord, SEASON, color words, print words, and ONLY the mother-size tags that exist in SIZE_CHART

---

## PHASE 7 — Hand-off

- ✅ Admin URL: `https://admin.shopify.com/store/dresslikemommy/products/<id>`
- ✅ Live URL: `https://www.dresslikemommy.com/products/<handle>`
- ✅ Collections the product now appears in
- ✅ SIZE_CHART recap table (vendor row → picker label → SKU → price) — this documents the source-of-truth decision and any vendor→picker mappings you made.
- ⚠️ Manual follow-ups (images, real weight in grams, inventory qty)
- 📂 Files saved: `<slug>-listing.md`, `<slug>-shopify-import.csv`, `ops/scripts/create-<shortcode>-<slug>.sh`

---

## TAGS (always include)

`Mommy and Me`, CATEGORY, `Matching Family <CategoryWord>`, GARMENT_HOOK-derived tag (e.g. `Short Sleeve Pajamas`, `Tiered Dress`, `One-Piece Swimsuit`), SEASON, every color word, every print/theme word, child age buckets (`Child 2-3yr`, `Child 4-5yr`, `Child 6-8yr`, `Child 9-10yr`) for each bucket actually covered by SIZE_CHART kid rows, mother-size tags **only for mother rows actually in SIZE_CHART** (`Mother S`, `Mother M`, `Mother L`, `Mother XL`, or `Mother One Size`), VENDOR_URL itself, any fandom/theme implied by the print.

---

## BACKUP CSV

Write `<slug>-shopify-import.csv` using the 75-column `products_export` header as fallback. `Published=TRUE`, `Status=active`, `Variant Inventory Tracker=shopify`, `Variant Inventory Policy=deny`, `Variant Fulfillment Service=manual`, `Variant Weight Unit=oz`, `Gift Card=false`.

**The CSV must have exactly `SIZE_CHART.length` variant rows.** Row 1 carries the full product payload (title, body, tags, SEO, all metafields); rows 2..N carry only the variant-specific cells (option values, SKU, price, compare-at, variant image, option-column cells). The body-HTML size-table row count in row 1 must also equal `SIZE_CHART.length`. Regenerate the CSV any time SIZE_CHART changes.

---

## GUARDRAILS

- **Vendor size chart is the single source of truth for variants** — never emit a variant the vendor doesn't offer, never omit one it does.
- Only list DESIGNS_TO_LIST — ignore other prints on the vendor page.
- If DESIGNS_TO_LIST includes only one audience, emit only that audience's variants.
- Runner must derive all variant-dependent fields from the SIZE_CHART JSON, not from parallel hand-maintained lists.
- Runner must preflight (halt before API calls) and post-verify (halt after create) on any SIZE_CHART mismatch.
- Skip metafields that don't apply (category mismatch, subtype rejection, no catalog entry) — never fake a value to "fill" the field.
- Don't pause for mid-pipeline approvals. Only stop for: creds fail after all 4 fallbacks, API errors unrecoverable after 1 retry, prohibited actions, or a SIZE_CHART inconsistency you can't resolve automatically.
- Run Phases 1–7 in order. Report back only at Phase 7, with the SIZE_CHART recap table included.
