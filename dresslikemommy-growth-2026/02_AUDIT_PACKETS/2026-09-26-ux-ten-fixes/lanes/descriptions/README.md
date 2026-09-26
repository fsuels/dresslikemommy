# Lane D — description cleanup and collection sort order (read-only)

Date: 2026-09-26. Mode: read-only audit plus approval packets. **No Shopify writes** (no productUpdate, collectionUpdate, translationsRegister or menu changes), no theme edits, no git. Data comes from Admin GraphQL 2026-07 read queries (token loaded from `~/.config/dresslikemommy/admin-api-token.json`, never printed) and public storefront GETs.

## Files

| File | What it is |
|---|---|
| `copy_fixes.csv` | 78 proposed edits: product_id, handle, status, rule, before snippet, after snippet, fix_status, review note |
| `copy_fixes.json` | Apply-ready: per product `gid`, `before_updatedAt`, `before_sha256`/`after_sha256`, the full `before_html`/`after_html` (the before copy is the rollback), change list, translation impact, detection regexes, rewrite rules and the apply contract |
| `SORT_ORDER_PACKET.md` | Collection default-sort approval packet (before/after, mutations, readback, rollback, dependency) |
| `INTEGRATION.md` | Theme patches for the parent: remove the hardcoded "latest 19 arrivals"; optional sorted "Shop" link |
| `tools/` | Read-only scripts: `fetch.py`, `patterns.py`, `scan.py`, `fixes.py`, `tr.py`, `coll.py`, `coll2.py`, `gql.py` (asserts no mutation) |
| `data/` | `collections_before.json` (46 collections with sortOrder, counts, rules, live top-12), `menus.json`, `best_selling_preview.json` |

## Packet 1 — customer-copy cleanup

**Scope scanned:** all 835 products: 258 ACTIVE, 3 DRAFT, 574 ARCHIVED.
**Flagged:** 31 ACTIVE + 3 DRAFT = **34 products, 78 edits** (32 `READY`, 2 `NEEDS_REVIEW`). 10 ARCHIVED products also match. They are not shopper-visible, so they are excluded from the fix set.

**Reuses the blocked dry-run.** The 2026-09-26 "Chart-backed sizing" dry-run (`/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/3686ed1c-4587-446d-9c90-3c1276c7c210/scratchpad/desc_fix_dry.json` + `fix_desc.py`, 20 ACTIVE products, apply denied) is embedded as rule `R01` with the same regex and wording. The output is VERIFIED byte-identical for 20/20. This packet supersedes that dry-run and adds 11 more ACTIVE products, 3 DRAFTs and 17 more phrase rules. It does not duplicate the dry-run.

**Detection categories** (regexes in `copy_fixes.json.detection_patterns`): chart_backed, transcribed, supplied/attached/published chart or image, "is not supplied/specified/confirmed", maker's, factory, vendor/supplier/source, 1688/Alibaba, "not part of this listing", "N child/adult rows", evidence/verification/inference wording, hardcoded "latest N arrivals", CJK fragments, admin artifacts, "is published/publishes", SKU/variant jargon. Edits by rule: chart-backed bullet 21, "no weight guidance is published" 12, care-not-supplied 8, maker's age labels 6, "not part of this listing" 6, fiber not specified 2, plus 23 single edits.

**Example (Beanie Ghost, live):**
- "Chart-backed sizing: Six child rows… transcribed from the supplied size chart" → "Family size range: Six child sizes, five women's sizes, and five men's sizes; see the size chart for measurements."
- "Care: Follow the sewn-in garment label; an exact care method is not supplied." → "Care: Follow the care instructions on the sewn-in garment label."
- "Child sizes follow the maker's age labels" → "Child sizes are labeled by age"
- "The baby romper shown in the photo is not part of this listing." → "…is not included with your order."

Every honesty caveat is kept ("not included", "measurements are unavailable", "shirt measurements are not listed", "runs small, size up"). Unknown-fiber apologies are dropped and the known fiber is kept ("Soft knit fabric, 95% polyester."), as the master prompt's rule requires. No claims were added. The two `NEEDS_REVIEW` rows are:
- `blue-tropical-floral-…`: a truncated "…measurements on the source" bullet.
- `sunshine-stripe-family-matching-tops`: the size-table header "Vendor Label" → "Tag Size". This touches the localized size-chart tables.

**Precision (hand-read):** every distinct flagged sentence was read.
- ACTIVE/DRAFT: **46/46 true positives (100%)**. About 13 are low-severity wording, e.g. "no weight guidance is published".
- ARCHIVED: 6/9 clear. 3 are borderline "Factory measurements in cm" headings.

**Recall:** a broader candidate sweep (~200 distinct sentences plus an unflagged-jargon pass) was also hand-read. Deliberately **not** flagged as acceptable shopper copy: about 45 "X shown in the photos is/are not included" caveats, "garment measurements are not listed", "One listing covers…", and "Dashes in the size chart mark…".

Known out-of-scope findings:
1. **49 products (47 ACTIVE, 2 DRAFT)** ship template size-table headers `Pant/Short or - (cm/in)`, `Sleeve or Skirt`, `Shoulder or —`. This comes from the literal column list in `ops/prompts/shopify-listing-master-prompt.md:415`. Headers drive the unit toggle and the localized size-chart mapping, so this needs its own packet.
2. 31 products carry invisible `data-start`/`data-end` paste attributes. They are harmless.

**Apply contract (future, owner-approved):**
1. Re-read the product and require `sha256(descriptionHtml)==before_sha256`.
2. `productUpdate(product:{id, descriptionHtml: after_html})`.
3. Read back `after_sha256` and a 0-hit rescan.
4. Rollback = `before_html`.

The 2026-09-26 Chart-backed apply was denied by the permission classifier, so this also needs explicit owner permission.

**Translation impact:**
- 34 products × 20 non-primary locales (ar, cs, da, de, el, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv) = **680 `body_html` slots**.
- **660** exist and all would turn outdated.
- **80** of those are already outdated today, all 20 locales each for `trail-plaid`, `summer-sky-stripe`, `indigo-pocket` and `sunset-ombre`.
- **20** are missing: `trick-or-treat-family-matching-pajamas` has no `body_html` translation in any locale. This is a PRE-EXISTING gap.
- The localized bodies contain the same operator wording (checked on Beanie Ghost: es "transcritas de la tabla de tallas proporcionada", "no forma parte de este producto"; de "Altersangaben des Herstellers", "nicht Teil dieses Angebots"). Re-translation is required, not optional.
- Note: the brief's locale list (zh, tr, hu) does not match the shop's actual 20 locales listed above.

Re-registration path:
- `python3 ops/scripts/finalize_shopify_listing_localization.py --handles <34 handles>`. It runs `poll_shopify_product_translations.py --min-age-seconds 0 --execute --force-refresh`, then `audit_shopify_product_translation_completeness.py --fail-on-issues`, then `repair_localized_product_size_charts.py --execute`/`--fail-on-missing`, then `audit_localized_size_chart_variant_mapping.py --fail-on-unmatched`.
- `--force-refresh` also re-translates titles and SEO fields. The narrower path is `poll_shopify_product_translations.py --handles … --min-age-seconds 0 --execute` without `--force-refresh`, followed by the same repair and audits. Per code lines 1730–1750, outdated `body_html` values are not reused (EXPECTED, not run).
- `sync_shopify_translations.py` is the export/CSV bulk sync and doesn't fit here.
- The Merchant and Pinterest feed descriptions change on the next feed build.

**Prompt check.** Rule `shopify-listing-master-prompt.md:333` (added today) covers chart-backed, transcribed, supplied chart, source row, evidence wording and "explanations of why a fact is unknown". It does **not** cover:
- maker's/factory/source wording in shopper sentences
- "not part of this listing"
- "published/publishes" for chart contents
- SKU/variant jargon
- the unknown-care bullet
- template size-table headers
- hardcoded counts

Also, **65 existing runner scripts `ops/scripts/create-*.sh` still embed "Chart-backed"** (6 "maker's age labels", 5 "not part of this listing", 8 "is not supplied"). Re-running any of them after the cleanup would put the text back. Proposed rule text, not applied (another session owns the dirty prompt copy):

> - Write every customer-facing sentence as shopper copy, not provenance. Also banned: `maker`/`maker's`, `factory`, `source`/`source chart`, `vendor`, `supplier`, `published`/`publishes` for what a chart contains, `not supplied`/`not specified`/`not confirmed`, `part of this listing`, `variant`, `SKU`, and row counts (`Five child rows`). Use `Child sizes are labeled by age`, `The size chart shows …`, `The chart has no hip measurement`, `The X shown in the photos is not included`.
> - When the care method is unknown, the care bullet is exactly `Follow the care instructions on the sewn-in garment label.`
> - Size-table headers name the one measurement in that column (`Sleeve`, `Skirt Length`, `Pant Length`, `Shoulder`) with its unit. Never ship the template alternatives `Sleeve or Skirt`, `Pant/Short or —`, `Shoulder or —`; a column with no values keeps a single measurement name and `—` cells.
> - Never hardcode catalog counts (for example `latest 19 arrivals`) in product, collection or theme copy.
> - Before re-running an existing `ops/scripts/create-*.sh` runner, re-scan its body copy against these rules.

## Packet 2 — collection default sort

- `/collections/all`: VERIFIED live `title-ascending` (Alphabetically, A-Z). It is the built-in collection (no `all` handle exists) and is the main menu's "Shop" target via the theme rewrite.
- 46 collections read (45 on the Online Store). 18 menus read via GraphQL. Before-state: 40 `CREATED_DESC` (including the MANUAL-membership `new-pajama-drop`), 6 `BEST_SELLING`, and the built-in `all` `TITLE_ASC`.
- **Proposed changes: 3.**
  1. `/collections/all` → newest first. Option A is the theme link `?sort_by=created-descending` (INTEGRATION.md, no Admin write). Option B is to create a smart collection with handle `all` (risks and rollback in the packet).
  2. `family-pajamas` → MANUAL seasonal top 8: six Halloween, the Christmas onesie, then fall long-sleeve, with a scheduled flip around Oct 15.
  3. `pajamas` → the same order.
- Everything else stays. The `BEST_SELLING` previews put summer swimwear and dresses first on broad collections, which would bury the 20 new holiday products. That disproves "BEST_SELLING for broad collections" for Q4. Revisit in January.
- **Dependency:** the `family-pajamas` rules edit by another session must land first. One writer per collection.
- Adjacent findings: `maternity` and `family-swimsuits` are main-menu items with **0 live products**. The hardcoded "latest 19 arrivals" line points at an April-only manual collection.

## Statuses

- Copy scan: IMPLEMENTED and VERIFIED (0 residual hits after the proposed rewrite; dry-run parity 20/20).
- Sort audit: IMPLEMENTED and VERIFIED (live readback).
- All Shopify applies, translation re-registration and theme patches: NOT RUN (require owner approval).
- Option B `all`-handle takeover behavior: EXPECTED, not verified.
