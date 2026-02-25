
Session: CTA style harmonization
Date: 2025-11-14

Changes applied (evidence-first)
- assets/theme-inline-overrides.css:600-660 - Standardized link--cta-block button styling (border, background, hover/focus) so secondary CTAs like See shipping details, Read customer reviews, and Exchange policy share a unified appearance with WCAG-friendly contrast.

Open TODOs (next session)
1) Spot-check all homepage CTAs to ensure no stray legacy styles remain and adjust copy if marketing prefers alternate labels.

Session: Homepage contrast refresh
Date: 2025-11-14

Changes applied (evidence-first)
- assets/theme-inline-overrides.css:1-120 - Introduced global text variables plus standardized primary/secondary button colors so CTA contrast meets AA across the homepage; also set alternating section bands in prior work to inherit the stronger palette.
- sections/hero-family-fit.liquid:60-150 - Moved hero body/shipping/proof text to the new muted/subtle tokens for clear legibility against the gradient background.
- sections/home-best-sellers.liquid:80-110 - Shifted subheading + fallback note colors to the shared muted/subtle palette.
- sections/home-reassurance.liquid:40-200 - Updated the reassurance subheading + captions to rely on the new contrast variables (pairs with the review snippets + rating note).
- sections/page-size-fit-guide.liquid:10-120 - Applied the strong/muted palette to intro copy, notes, and contact text so the guide stays readable on light sections.

Open TODOs (next session)
1) QA the homepage in light/dark color schemes to ensure the refreshed palette looks consistent and tweak the color tokens if additional contrast issues appear.

Session: Tile accessibility pass
Date: 2025-11-14

Changes applied (evidence-first)
- assets/theme-inline-overrides.css:1-140 - Added focus styles for the Match the moment card links, thumb tiles, and Shop this look images so keyboard users see a consistent outline; also ensured the new global text tokens/CTA colors apply across the homepage for contrast.
- sections/hero-family-fit.liquid, home-best-sellers.liquid, home-reassurance.liquid, page-size-fit-guide.liquid - Updated text color usage to the shared strong/muted/subtle tokens so grey-on-grey and text-over-image areas now meet AA contrast.

Open TODOs (next session)
1) Keyboard through the homepage to confirm the new outlines appear on every interactive tile and adjust spacing if outlines appear clipped.

Session: Product taxonomy field activation
Date: 2026-02-22

Changes applied (evidence-first)
- sections/main-product.liquid:155 - Added shopper-visible taxonomy text under the product title that renders `Type`, `Style`, and `Pattern` from `product.metafields.custom.*` when present.
- layout/theme.liquid:27 - Extended product-page meta output to include `custom-type`, `custom-style`, and `custom-pattern` meta tags (only when values are present).
- snippets/jsonld-seo.liquid:139 - Added `additionalProperty` entries in Product JSON-LD for `Type`, `Style`, and `Pattern` when metafield values exist.

Open TODOs (next session)
1) Backfill `product.metafields.custom.type`, `product.metafields.custom.style`, and `product.metafields.custom.pattern` across top-selling SKUs so the new PDP/UI/JSON-LD output appears consistently.
2) In Shopify Search & Discovery, consider adding filters for these metafields if you want collection/search filtering by Type/Style/Pattern.

Session: Product taxonomy metafields surfaced in PDP + SEO
Date: 2026-02-22

Changes applied (evidence-first)
- sections/main-product.liquid - Added `taxonomy_type`, `taxonomy_style`, and `taxonomy_pattern` assignments right after the product title and a conditional `product__text caption` line that renders `Type`, `Style`, and `Pattern` in order with ` | ` only between present values.
- layout/theme.liquid - Inside the existing `{% if template == 'product' %}` block, added the same three taxonomy assignments plus conditional `custom-type`, `custom-style`, and `custom-pattern` meta tags.
- snippets/jsonld-seo.liquid - Inside the Product JSON-LD object after `offers` and before `aggregateRating`, added taxonomy assignments and conditional `additionalProperty` `PropertyValue` objects for Type/Style/Pattern, only when values exist.

Open TODOs (next session)
1) Backfill `product.metafields.custom.type`, `product.metafields.custom.style`, and `product.metafields.custom.pattern` on products so PDP text, meta tags, and JSON-LD output consistently.

Session: PDP complementary activation + enriched ecommerce analytics
Date: 2026-02-22

Changes applied (evidence-first)
- templates/product.json - Added `sections.main.blocks.complementary_main` (`type: complementary`) with defaults: heading `Complete the family look`, non-collapsible row, `price_tag` icon, limit `10`, page size `3`, `counter` pagination, square image ratio, quick add disabled; inserted `complementary_main` into `sections.main.block_order` after `description`.
- sections/main-product.liquid - Added always-rendered `<script type="application/json" id="AnalyticsProductJSON-{{ product.id }}">` payload for PDP analytics with product core fields, taxonomy metafields (`category1`, `subcategory`, `subcategory2`, `type`, `style`, `pattern`), selected/first variant id, and per-variant `{id, sku, price, barcode}`.
- layout/theme.liquid - Added a single deferred analytics asset include: `<script defer src="{{ 'analytics.js' | asset_url }}"></script>`.
- assets/analytics.js - Recreated analytics client script and updated to prefer `AnalyticsProductJSON-*`, gracefully fallback when data is missing, enrich `view_item` + `add_to_cart` ecommerce item fields (`item_id`, `item_name`, `item_brand`, `item_variant`, `price`, `currency`, `item_category`, `item_category2`, `item_category3`, `item_type`, `style`, `pattern`, `product_handle`), and guard against duplicate initial `view_item` firing.

Open TODOs (next session)
1) Task 2 is blocked because `ops/data/top100_handles.csv` is missing. Add this file with a `handle` column so top-100 scoped export work can run.
2) After the handle list is provided, generate `ops/exports/top100_listing_patch.csv` and `ops/reports/top100_missing_barcodes.csv` per the mapping/barcode rules.
3) Validate one live PDP in preview to confirm a single enriched `view_item` and enriched `add_to_cart` payload in `window.dataLayer`.

Session: ROI audit and deferred execution plan
Date: 2026-02-22

Changes applied (evidence-first)
- No storefront code changes in this session. Performed a repo + catalog audit and documented the highest-ROI execution order.

Findings snapshot
- `GPT/products_export_1.csv` coverage by product handle (660 products): SEO Title `0%`, Google Product Category `0%`, Variant Barcode `14.2%`, Type/Style/Pattern `0%`, complementary/related/search boosts `0%`.
- `layout/theme.liquid` still loads `base.css` and `customer.css` twice (print/onload at lines `19`/`21` and standard includes at lines `541`/`542`).
- `snippets/meta-tags.liquid` has no robots noindex handling for non-index pages.
- `sections/main-product.liquid` includes static/randomized social-proof copy and numbers (`soldMessages` list + random session values).
- `assets/analytics.js` currently fires `view_item`, `add_to_cart`, and `begin_checkout`, but begin_checkout is minimal and event-level revenue parameters are not present.

Open TODOs (next session)
1) Execute top-100 SKU backfill/import priority: SEO Title, Google Product Category, barcode policy (`GTIN` where available; custom-product fallback only where legitimately needed).
2) Fill Search & Discovery fields for top-100 SKUs: complementary, related, and search boosts; keep one complementary block per PDP template.
3) Upgrade GA4 ecommerce payload completeness (event-level `currency`/`value`, cart context for begin_checkout, and purchase tracking via Shopify customer events/pixel layer).
4) Normalize taxonomy vocabulary (Category1/SubCategory/SubCategory2) to remove duplicate/synonym fragmentation before bulk import.
5) Clean technical SEO/performance debt in theme head (duplicate CSS strategy, robots policy, and oversized inline style footprint) in a controlled regression pass.

Session: ROI fixes for cross-sells, metadata coverage, analytics payloads, and schema cleanup
Date: 2026-02-22
AGENT_CONTINUITY_ANCHOR: 2026-02-22-roi-cross-sell-metadata-analytics-schema

Changes applied (evidence-first)
- templates/product.json:1 - Activated PDP complementary recommendations block (`complementary_main`) in `main.block_order` directly after `buy_buttons` and enabled quick add for higher AOV exposure near the CTA.
- assets/global.js:1303 - Updated `ProductRecommendations` loader to retry complementary recommendations with `intent=related` when complementary returns empty, so cross-sells still render before Search & Discovery data backfill is complete.
- sections/main-product.liquid:132 - Added taxonomy fallback derivation from `product.metafields.custom.*`, `product.type`, and prefixed tags (`Category1`, `Category`, `SubCategory`, `Type`, `Style`, `Pattern`) for consistent downstream usage.
- sections/main-product.liquid:1102 - Added dedicated PDP analytics payload script (`ProductAnalyticsData-*`) including id/handle/title/vendor/currency/taxonomy and variant metadata.
- assets/analytics.js:1 - Restored analytics asset and expanded GA4-style item payloads for `view_item` and `add_to_cart` with `item_category`..`item_category5` and custom taxonomy fields (`custom_category1`, `custom_subcategory`, `custom_type`, `custom_style`, `custom_pattern`), plus safer product JSON parsing and cart-update subscription handling.
- layout/theme.liquid:28 - Reworked product meta taxonomy tags to use fallback logic (metafields -> tags -> product.type), added `jsonld-seo` render as canonical schema source, and removed duplicate static Organization JSON-LD block in head.
- layout/theme.liquid:589 - Ensured only one `content_for_header` remains to avoid duplicated platform/app script injection.
- sections/header.liquid:446 - Removed duplicate Organization/WebSite JSON-LD blocks; canonical output now comes from `snippets/jsonld-seo.liquid`.
- sections/featured-product.liquid:452 - Removed section-level Product JSON-LD output to reduce schema duplication noise.
- sections/main-product.liquid:1087 - Removed duplicate PDP Product JSON-LD + `product-schema-extra` render path so Product schema is emitted from one source.
- snippets/jsonld-seo.liquid:105 - Added taxonomy fallback resolution for Product JSON-LD and included `Category1` + `SubCategory` in `additionalProperty` when present.
- snippets/jsonld-seo.liquid:136 - Added normalized GTIN emission (`gtin8`/`gtin12`/`gtin13`/`gtin14`) from sanitized variant barcodes with proper JSON quoting.
- ops/scripts/backfill_product_metadata.py:1 - Added CSV backfill tool that fills missing SEO Title, Google Product Category, Category1/SubCategory, Pattern/Style/Type, complementary/related/search boosts, and variant MPN/custom-product mitigation for missing GTIN rows.
- GPT/products_export_1_backfill.csv:1 - Generated import-ready backfilled catalog export from `GPT/products_export_1.csv`.
- ops/products_export_1_backfill_summary.md:1 - Generated before/after coverage summary for product-level and variant-level fields.

Open TODOs (next session)
1) Import `GPT/products_export_1_backfill.csv` in Shopify (or merge selectively) and verify list-reference metafield parsing for complementary/related handles in your store environment.
2) After import, QA 5-10 live PDPs in Theme Preview: confirm complementary block loads, confirm fallback-to-related behavior when complementary metafield is empty, and confirm `view_item`/`add_to_cart` items in GTM preview include taxonomy fields.
3) Run Rich Results Test on one product URL post-deploy to verify single Product schema instance and valid GTIN fields.
4) If any imported complementary/related values are rejected by Shopify CSV parser, adapt `ops/scripts/backfill_product_metadata.py` output format to the accepted list.product_reference format (handle list vs GID list) and regenerate.

Session: Active catalog full backfill + PDP trust/perf cleanup
Date: 2026-02-22
AGENT_CONTINUITY_ANCHOR: 2026-02-22-active-catalog-full-backfill

Changes applied (evidence-first)
- `ops/scripts/backfill_product_metadata.py` - Rebuilt metadata backfill workflow to target active products by default, normalize taxonomy (`Category1`, `SubCategory`, `SubCategory2`, `Type`, `Style`, `Pattern`), fill missing SEO title/description, assign Google product categories, generate complementary/related/search boost values, set `Related products settings` to `only manual`, and apply variant-level GTIN fallback policy (`Google Shopping / Custom Product`, `Google: Custom Product`, and MPN from SKU).
- `products_export_1 2_active_backfill.csv` - Generated import-ready output from `products_export_1 2.csv` for all 588 active product handles.
- `products_export_1 2_active_only_patch.csv` - Generated active-only import subset containing all rows for 588 active handles (14010 rows) so variant-level fields import correctly.
- `ops/products_export_1_2_active_backfill_summary.md` - Generated before/after coverage report for active products.
- `layout/theme.liquid` - Removed duplicate head CSS loads for `base.css` and `customer.css` from print/onload path to prevent double-load.
- `snippets/meta-tags.liquid` - Added robots noindex logic for `search`, `cart`, and `404` pages.
- `sections/main-product.liquid` - Removed synthetic urgency/sales messaging code and duplicate title heading/link output to reduce trust risk and clean PDP semantics.
- `assets/analytics.js` - Updated `begin_checkout` event payload to include ecommerce currency context for cleaner GA4 mapping.

Coverage outcome (active products)
- Product-level fields reached 100% for: `SEO Title`, `SEO Description`, `Google Shopping / Google Product Category`, `Category1`, `SubCategory`, `SubCategory2`, `Type`, `Style`, `Pattern`, `Complementary products`, `Related products settings`, `Related products`, and `Search product boosts`.
- Variant-level fields reached 100% for: `Google Shopping / Custom Product`, `Google: Custom Product`, and `Image Alt Text`.
- `Variant Barcode` remains source-limited at 11.8% and was not fabricated; fallback flags/MPN policy applied.

Open TODOs (next session)
1) Import `products_export_1 2_active_only_patch.csv` first (safer), validate metafield parsing for complementary/related list references, then import the full backfill file if needed.
2) Spot-check 10 live active PDPs after import to confirm complementary block content quality and tune manually for hero SKUs.
3) Review Merchant Center diagnostics after feed refresh; prioritize adding real GTINs on top-selling active variants still using custom-product fallback.

Session: Single-file active import output + taxonomy tag completion
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-single-file-import-ready

Changes applied (evidence-first)
- `ops/scripts/backfill_product_metadata.py` - Added deterministic taxonomy tag builder so each active product now gets required prefixed tags in `Tags`: `category1:`, `subcategory:`, `subcategory2:`, `type:`, `style:`, `pattern:` plus deduped plain tags.
- `products_export_1 2_IMPORT_READY.csv` - Generated final single import file containing all rows for 588 active handles (14010 rows), with completed product metafields/feed fields and required taxonomy prefixed tags.
- Removed extra generated CSVs to reduce confusion: `products_export_1 2_active_backfill.csv`, `products_export_1 2_active_only_patch.csv`, and `products_export_1 2_working_backfill.csv`.

Validation snapshot
- Active handles in final import file: `588`.
- Handles missing any required taxonomy prefixed tag: `0`.
- Product-level coverage for active handles is 100% for: SEO title/description, Google product category, Category1/SubCategory/SubCategory2, Type/Style/Pattern, complementary/related settings+values, and search boosts.
- Variant-level remains source-limited for GTIN (`Variant Barcode` 1649/13990); fallback fields are fully populated (`Google Shopping / Custom Product`, `Google: Custom Product`, and image alt text at 100%).

Session: Import blocker fix for missing image source data
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-image-src-import-fix

Changes applied (evidence-first)
- `ops/scripts/backfill_product_metadata.py` - Restored guard in `infer_image_alt_text` so `Image Alt Text` is only populated when `Image Src` exists; this prevents Shopify CSV import errors caused by alt text on rows without image source.
- Regenerated `products_export_1 2_IMPORT_READY.csv` from `products_export_1 2.csv` for active handles using the updated script.
- Removed temporary generator artifact `products_export_1 2_working_backfill.csv`.

Validation snapshot
- `products_export_1 2_IMPORT_READY.csv` rows: `14010` (all rows for `588` active handles).
- Rows with `Image Alt Text` but blank `Image Src`: `0`.
- Rows with `Image Position` but blank `Image Src`: `0`.
- Active handles missing required taxonomy prefixed tags: `0`.

Session: SEO quality hardening for active import output
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-seo-quality-hardening

Changes applied (evidence-first)
- `ops/scripts/backfill_product_metadata.py` - Hardened SEO normalization pipeline:
  - Added title sanitation (`normalize_marketing_title`) to strip noisy fragments (e.g., `...`, `| DLM`, quote artifacts).
  - Added phrase shortening helper to avoid awkward truncation in descriptions.
  - Upgraded SEO description generator to produce tighter, conversion-safe copy in target length range.
  - SEO title/description for active products are now set deterministically (not only when blank), ensuring consistent quality across all active handles.
- `ops/scripts/backfill_product_metadata.py` - Added gift-card override logic:
  - SEO title/description tuned for gift-card intent.
  - Google product category set to gift-card taxonomy path for the gift-card product.
- Regenerated `products_export_1 2_IMPORT_READY.csv` and removed temporary generator artifact.

Validation snapshot
- Active handles: `588`.
- SEO title length violations (`>70`): `0`.
- SEO description length violations (`<140` or `>155`): `0`.
- SEO descriptions containing `...`: `0`.
- Rows with `Image Alt Text` and blank `Image Src`: `0`.
- Handles missing required taxonomy prefixed tags: `0`.

Session: Full-funnel analytics + backfill overrides + import validator
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-analytics-overrides-validator

Changes applied (evidence-first)
- `assets/analytics.js` - Expanded ecommerce tracking from basic PDP events to broader funnel coverage:
  - Added `view_item_list` and `select_item` from product cards using intersection + click tracking.
  - Added `view_cart` for cart page load and cart drawer open.
  - Added `remove_from_cart` via cart snapshot diffs on cart update events.
  - Upgraded `begin_checkout` payload to include cart `items`, `currency`, and `value` when cart context is available.
  - Upgraded `view_item` and `add_to_cart` payloads to include event-level `currency`/`value` and consistent taxonomy fields.
- `snippets/card-product.liquid` - Added product-card analytics data attributes (id/variant/price/taxonomy/handle/vendor/title) and taxonomy fallback from prefixed tags for list/click event payload quality.
- `sections/main-cart-items.liquid` - Added cart row data attributes (line key, ids, qty, price, taxonomy) so cart events can emit richer item payloads.
- `snippets/cart-drawer.liquid` - Added equivalent cart row data attributes for cart drawer event parity.
- `sections/main-product.liquid` - Added `taxonomy_subcategory2` fallback wiring and included `subcategory2` in `ProductAnalyticsData-*` JSON payload.
- `ops/scripts/backfill_product_metadata.py` - Added optional `--overrides` CSV support keyed by handle:
  - Supports canonical output column names and short aliases (`seo_title`, `google_category`, `complementary_products`, etc.).
  - Applies overrides to generated taxonomy/SEO before recommendation generation and to discovery/tags fields after generation.
- `ops/scripts/validate_import_ready_csv.py` - Added new import validator script for import-ready CSVs with checks for:
  - required product-level field coverage,
  - taxonomy tag prefix completeness,
  - complementary/related reference integrity,
  - related settings/search boost quality,
  - image alt/src consistency,
  - GTIN/custom-product/MPN consistency.
- `ops/import_ready_validation_report.md` - Generated validator report against `products_export_1 2_IMPORT_READY.csv` provided by operator.

Validation snapshot
- Input validated: `products_export_1 2_IMPORT_READY.csv` (no overwrite performed).
- Target handles: `588` active handles.
- Result: `0` errors, `2` warnings.
  - `malformed_gtin`: `44` rows.
  - `missing_mpn_for_barcode_less`: `1886` rows.

Open TODOs (next session)
1) Run GTM/GA4 preview on PDP, collection, cart drawer, and cart page to confirm new `view_item_list`, `select_item`, `view_cart`, `remove_from_cart`, and enriched `begin_checkout` payloads are mapped correctly.
2) Decide policy for `missing_mpn_for_barcode_less` warning class (acceptable with custom-product strategy vs force-fill MPN for all barcode-less variants).
3) Review the `malformed_gtin` warning sample rows and either correct source barcodes or whitelist known non-GTIN identifiers before feed sync.

Session: PDP breadcrumb left-gutter alignment
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-pdp-breadcrumb-left-gutter

Changes applied (evidence-first)
- `sections/main-product.liquid` - Wrapped the product breadcrumb include in a `.page-width` container so it inherits Dawn horizontal gutters instead of sitting flush against the viewport edge.

Validation snapshot
- Verified `snippets/breadcrumbs.liquid` is only included by `sections/main-product.liquid`, so the change scope is limited to PDP breadcrumbs.

Session: PDP media prominence rebalance
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-pdp-media-prominence-rebalance

Changes applied (evidence-first)
- `sections/main-product.liquid` - Added PDP-scoped wrapper classes (`.page-width--product-breadcrumbs` and `.page-width--product-main`) around breadcrumb and product content containers so width/gutter tuning can be isolated to the main product section.
- `assets/section-main-product.css` - Added scoped layout overrides to increase PDP visual emphasis on media:
  - widened desktop PDP container and reduced outer horizontal padding on large screens (`>=990px`),
  - shifted `product--large` desktop split from `65/35` to `70/30` (media/info),
  - reduced desktop info-column left/right padding and tightened block spacing,
  - increased breadcrumb visual weight (size, spacing, and padding).

Validation snapshot
- Verified both new wrapper classes are present in `sections/main-product.liquid` and referenced by new CSS selectors in `assets/section-main-product.css`.
- No automated storefront visual test was run in this session; manual PDP check in theme preview is still required for desktop and mobile.

Session: PDP media prominence tuning + live preview run
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-pdp-preview-bigger-variant

Changes applied (evidence-first)
- `assets/section-main-product.css` - Tuned the prior PDP rebalance to a two-stage desktop behavior:
  - at `>=990px`: widened PDP container and moved `product--large` split to `70/30` (media/info),
  - at `>=1400px`: increased image emphasis further to `72/28` with tighter outer paddings.
- Kept breadcrumb prominence styling and compact info-column spacing from prior session.

Preview run (this session)
- Started Shopify live preview via CLI for this repo and confirmed sync:
  - local hot-reload URL: `http://127.0.0.1:9393`
  - share preview URL: `https://dresslikemommy-com.myshopify.com/?preview_theme_id=133283250273`
  - theme editor URL: `https://dresslikemommy-com.myshopify.com/admin/themes/133283250273/editor?hr=9393`

Validation snapshot
- Shopify CLI reported successful sync after CSS update (`Synced » update assets/section-main-product.css`).
- Local HTTP check returned `200` from `http://127.0.0.1:9393`, confirming preview server availability during session.

Session: PDP mobile image prominence pass
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-pdp-mobile-image-prominence

Changes applied (evidence-first)
- `assets/section-main-product.css` - Added PDP-scoped mobile overrides (`<=749px`) to prioritize hero media:
  - removed horizontal padding from `.page-width--product-main` so media can use full viewport width,
  - removed slider side offsets for the main PDP media component,
  - set media list width to `100%` and media item width to `100%`,
  - reduced space below media and preserved readable info content padding via `.product__info-wrapper`.

Validation snapshot
- Shopify CLI dev server reported sync success after edit: `Synced » update assets/section-main-product.css`.

Session: PDP ultra-wide 74/26 dominance pass
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-pdp-ultrawide-74-26

Changes applied (evidence-first)
- `assets/section-main-product.css` - Added a new ultra-wide breakpoint at `>=1600px` that increases PDP image dominance for `product--large`:
  - media/info split set to `74/26`,
  - info-column side padding reduced to `1.8rem` (left/right variant-aware) to preserve CTA usability while expanding hero media.

Validation snapshot
- Shopify CLI dev server reported sync success after edit: `Synced » update assets/section-main-product.css`.

Session: GitHub sync safety for local CSV exports
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-github-sync-csv-ignore

Changes applied (evidence-first)
- `.gitignore` - Added explicit ignore entries for `products_export_1 2.csv` and `products_export_1 2_IMPORT_READY.csv` so local product export files are not accidentally committed during theme sync work.
- `.shopifyignore` - Added rules to exclude local data/non-theme files (`products_export_1 2*.csv`, `GPT/*.csv`, `ops/*`, and `agent-backend/`) from Shopify CLI theme upload/dev sync paths.

Validation snapshot
- Confirmed both CSV files are untracked locally and now matched by `.gitignore` rules.

Session: Homepage Shop Now scroll-to-categories behavior
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-home-shopnow-smooth-scroll-categories

Changes applied (evidence-first)
- `sections/collection-list.liquid` - Added optional `anchor_id` section setting and wired it to output an HTML id on the section wrapper (handleized), enabling a stable in-page scroll target without changing layout/styling.
- `templates/index.json` - Set `anchor_id` to `categories-section` on the homepage `collection_list_PX36Hk` section (the “Mommy & Me” categories block) and updated hero button link fallback from `/collections/all` to `#categories-section`.
- `sections/hero-banner.liquid` - Updated the hero CTA markup with a scoped id/data target and added a native click handler that:
  - prevents default navigation when `#categories-section` exists,
  - smoothly scrolls via `scrollIntoView({ behavior: 'smooth', block: 'start' })`,
  - respects reduced-motion preferences by switching to `behavior: 'auto'`.

Validation snapshot
- Confirmed `categories-section` is defined on the homepage categories section through `anchor_id`.
- Confirmed hero CTA script targets `categories-section`, calls `preventDefault()`, and uses native `scrollIntoView`.
- Confirmed no styling/layout rules were changed as part of this request.

Session: Local dev homepage blank due stale theme dev runtime
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-local-dev-homepage-empty-main

Changes applied (evidence-first)
- No theme code changes were required.
- Diagnosed local runtime discrepancy: existing `shopify theme dev` process on `127.0.0.1:9292` was serving an empty `<main>` (`content_for_layout` blank) while template files still contained homepage sections.
- Confirmed a fresh `shopify theme dev` session rendered hero + categories correctly.
- Restarted `shopify theme dev` on port `9292` and verified homepage now includes:
  - `shopify-section-template--...__hero_banner_main`
  - `shopify-section-template--...__collection_list_PX36Hk`

Validation snapshot
- Before restart: `curl http://127.0.0.1:9292/` showed empty `<main id="MainContent">`.
- After restart: `curl http://127.0.0.1:9292/` includes hero/collection-list markup and matching request logs from CLI.

Session: Reapply homepage Shop Now smooth-scroll after theme replacement
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-reapply-home-shopnow-scroll-after-theme-replace

Changes applied (evidence-first)
- `sections/collection-list.liquid` - Re-added optional `anchor_id` setting and wrapper id output (`id="{{ section_anchor_id }}"`) so homepage category blocks can be targeted by in-page scroll.
- `sections/hero-banner.liquid` - Re-added CTA id/data attributes and click handler that:
  - prevents default navigation when the target exists,
  - calls `scrollIntoView({ behavior: 'smooth', block: 'start' })`,
  - falls back to `behavior: 'auto'` for reduced-motion users.
- `templates/index.json` - Re-set homepage hero CTA link to `#categories-section` and re-set `collection_list_PX36Hk.settings.anchor_id` to `categories-section`.

Validation snapshot
- Local render (`http://127.0.0.1:9292/`) now includes:
  - hero CTA `href="#categories-section"`,
  - CTA script with `preventDefault()` + `scrollIntoView`,
  - categories wrapper `id="categories-section"`.

Session: Header account/cart icon proportion and hit-area fix
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-header-icon-proportion-hitarea-fix

Changes applied (evidence-first)
- `layout/theme.liquid` - Replaced conflicting custom header icon CSS block that previously forced uneven icon container dimensions (`74x54`) and cart-only scaling.
- Added scoped normalization for `.header__icon--account` and `.header__icon--cart`:
  - equalized icon hit area to `4.4rem x 4.4rem`,
  - equalized base SVG size to `2.2rem`,
  - applied slight cart glyph compensation (`2.4rem`) due bag icon viewBox density,
  - kept `pointer-events: none` on SVG so link hitbox remains stable.

Validation snapshot
- Verified updated CSS block is present in local render output from `http://127.0.0.1:9292/`.
- Verified legacy oversized values (`74px`, `54px`) are removed from `layout/theme.liquid`.

Session: Header bag icon visual size increase
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-header-bag-icon-size-increase

Changes applied (evidence-first)
- `layout/theme.liquid` - Increased cart/bag SVG size override from `2.4rem` to `2.8rem` within `.header__icon--cart svg` while keeping the shared icon click target dimensions unchanged.

Validation snapshot
- Verified local render output on `http://127.0.0.1:9292/` includes `.header__icon--cart svg { width: 2.8rem; height: 2.8rem; }`.

Session: Strong cart icon boost + hit-area spacing correction
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-header-cart-strong-boost-margin-fix

Changes applied (evidence-first)
- `layout/theme.liquid` - Increased cart icon SVG override from `2.8rem` to `4.4rem` because the cart glyph occupies a small fraction of its `40x40` viewBox and appeared visually undersized versus account icon.
- `layout/theme.liquid` - Added `.header__icon--cart { margin-right: 0 !important; }` to neutralize Dawn's negative cart margin and prevent apparent hit-area overlap issues between account/cart.

Validation snapshot
- Verified local render output on `http://127.0.0.1:9292/` contains updated cart rules:
  - `.header__icon--cart svg { width: 4.4rem !important; height: 4.4rem !important; }`
  - `.header__icon--cart { margin-right: 0 !important; }`

Session: Header account/cart click-area interception fix (search overlay)
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-header-icon-clickarea-overlay-fix

Changes applied (evidence-first)
- `snippets/visible-header-search.liquid` - Added scoped desktop pointer-event rules for the top-level search wrapper elements:
  - set `pointer-events: none` on `.EzfyHeaderSearch--desktop > predictive-search.search-modal__form` and `.EzfyHeaderSearch--desktop > search-form.search-modal__form`,
  - restored `pointer-events: auto` on the actual interactive descendants (inner `.search-modal__form` and predictive results container).
- Purpose: prevent the full-width predictive-search wrapper from intercepting clicks in the header icon area while preserving existing search UI layout/styling.

Validation snapshot
- Playwright hit-testing before fix showed icon center points resolved to `PREDICTIVE-SEARCH.search-modal__form`.
- Playwright hit-testing after fix resolves to the expected targets:
  - account center -> `ACCOUNT-ICON.`
  - cart center -> `A.header__icon header__icon--cart link focus-inset`
- Functional click checks after fix:
  - account icon click navigates to `/account/login`,
  - cart icon click opens cart drawer (body class includes `overflow-hidden`, drawer inner receives focus).

Session: Collection/PDP breadcrumb consistency + filter readability pass
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-pdp-breadcrumb-filter-readability

Changes applied (evidence-first)
- `snippets/collection-breadcrumbs.liquid` - Replaced the prior inline CSS/JS breadcrumb implementation with a semantic, lightweight breadcrumb:
  - added explicit `Home` link and `&rsaquo;` separators,
  - kept optional subcategory switching via native `<details>` dropdown,
  - removed custom overlay script and conflicting `breadcrumb-sub-category`/`breadcrumb-dropdown` style blocks.
- `assets/template-collection.css` - Added collection-scoped overrides to align collection breadcrumb styling with PDP breadcrumb intent and neutralize global uppercase/11px overrides:
  - breadcrumb normalized to 12px medium-weight gray text with consistent spacing,
  - subtle dropdown treatment for alternate subcategory links,
  - filter labels/summaries/sort controls increased to ~13-14px with reduced letter-spacing and non-uppercase treatment.
- `snippets/breadcrumbs.liquid` - Added semantic breadcrumb classes (`product-breadcrumb__*`) to PDP breadcrumb markup for cleaner targeting and future maintenance.
- `assets/section-main-product.css` - Normalized PDP breadcrumb typography to the same 12px, medium-weight, gray visual system and explicitly overrode global uppercase breadcrumb rules.
- `templates/product.json` - Removed legacy `main-product.custom_css` breadcrumb overrides to eliminate a conflicting styling source.

Validation snapshot
- Confirmed new collection breadcrumb snippet contains no inline `<style>` or `<script>` blocks.
- Confirmed legacy collection breadcrumb classes (`breadcrumb-sub-category`, `breadcrumb-dropdown`) are no longer referenced in repository search.
- Reviewed diffs for `snippets/collection-breadcrumbs.liquid`, `assets/template-collection.css`, `snippets/breadcrumbs.liquid`, `assets/section-main-product.css`, and `templates/product.json` for selector scope and Liquid syntax integrity.
- No browser visual regression run in this session; manual storefront preview checks remain required for desktop/mobile collection and PDP views.

Open TODOs (next session)
1) In theme preview, verify collection breadcrumb alignment and dropdown behavior across collections with and without `custom.mainall`/`custom.product_tag` metafields.
2) Validate filter readability on desktop/mobile in horizontal filter mode and ensure no unintended typography changes on non-collection templates.
3) Confirm PDP breadcrumb and collection breadcrumb now render with matching visual rhythm (size/weight/color/separator) under existing global `layout/theme.liquid` custom CSS.

Session: Rollback to prior approved breadcrumb/filter state
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-rollback-to-prior-approved-breadcrumb-state

Changes applied (evidence-first)
- Reverted `layout/theme.liquid` to the prior state before the root-cause cleanup pass.
- Reverted `snippets/breadcrumbs.liquid` to the previous version that introduced only semantic class hooks (`product-breadcrumb__*`) without additional fallback/ARIA restructuring.
- Reverted `snippets/collection-breadcrumbs.liquid` to the prior version (removed added `aria-current` attributes from the rollback pass).
- Removed the superseded worklog entry for the reverted root-cause cleanup pass to keep continuity accurate.

Validation snapshot
- Confirmed current modified file set matches the earlier approved pass: `assets/section-main-product.css`, `assets/template-collection.css`, `snippets/breadcrumbs.liquid`, `snippets/collection-breadcrumbs.liquid`, `templates/product.json`, and this worklog.

Session: Collection category navigation polish (tabs + mobile select)
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-category-nav-tabs-polish

Changes applied (evidence-first)
- `snippets/collection-breadcrumbs.liquid` - Replaced the native `<details>` category switcher with a structured category navigation system:
  - kept breadcrumb trail (`Home > Main category > Current`) as stable context,
  - added horizontal pill tabs for category switching on tablet/desktop,
  - added mobile-only styled `<select>` fallback for category switching,
  - deduplicated category options by handle to avoid repeated links and preserve a single active current item.
- `assets/template-collection.css` - Added collection-scoped styling for the new category nav:
  - consistent typography via theme body font and normalized sizing/spacing,
  - polished pill-tab visuals with subtle hover/focus/active transitions,
  - lightweight staggered entry animation for tab items,
  - responsive mobile select treatment aligned with collection breadcrumb rhythm.

Validation snapshot
- Confirmed new category nav selectors exist and are wired in both files via repository search (`collection-category-nav*`).
- Confirmed legacy dropdown markup/classes are no longer present in `snippets/collection-breadcrumbs.liquid`.
- Ran `shopify theme check --fail-level error`; command reports pre-existing theme errors in unrelated files (`sections/header.liquid`, `sections/main-list-collections.liquid`, `snippets/cjpod.liquid`, etc.).
- `snippets/collection-breadcrumbs.liquid` returned warnings only (`HardcodedRoutes`), with no new syntax errors from this change.

Open TODOs (next session)
1) In theme preview, verify category tab overflow/scroll behavior on long category lists and confirm active-state contrast across all color schemes.
2) On mobile (<750px), verify select navigation works on iOS/Android and that spacing remains balanced with horizontal filters enabled.
3) Decide whether to replace hardcoded `/collections/...` links in breadcrumb/category nav with route-composed links to satisfy Theme Check style guidance.

Session: Collection category nav redesign (high-contrast premium tabs)
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-category-nav-premium-redesign

Changes applied (evidence-first)
- `snippets/collection-breadcrumbs.liquid` - Reworked category navigation logic for robust current/alternate category handling:
  - computes and deduplicates category options by handle,
  - reliably marks the current collection tab as active (including `Other` edge cases),
  - only renders the category nav when alternates exist,
  - keeps desktop tab nav + mobile select nav, both driven by the same deduped source list,
  - uses `routes.collections_url` composition for category links.
- `assets/template-collection.css` - Replaced prior low-contrast tab treatment with a high-contrast premium UI system:
  - explicit surface/text tokens to keep labels legible in all states,
  - elevated card container + scroll-fade tab rail for modern horizontal navigation,
  - refined active/hover/focus states with stronger contrast and subtle motion,
  - improved mobile select readability and interaction affordance,
  - reduced-motion fallback for users with motion preferences.

Validation snapshot
- Verified updated Liquid selectors/logic and nav classes are present in `snippets/collection-breadcrumbs.liquid`.
- Verified updated CSS selectors and contrast-focused style rules are present in `assets/template-collection.css`.
- `shopify theme check` still reports pre-existing repo-wide errors in unrelated files (e.g. `sections/header.liquid`, `sections/main-list-collections.liquid`, `snippets/cjpod.liquid`); no new syntax failures were introduced by this nav redesign.

Open TODOs (next session)
1) Visual QA in storefront preview on collections with long tag lists to verify horizontal rail overflow behavior and gradient edge treatment.
2) Confirm category ordering/content in `custom.product_tag` metafields reflects intended merchandising order for tabs.
3) If desired, add a lightweight page-transition on tab click (fade-out before navigation) after UX signoff.

Session: Collection category nav redesign v2 (minimal editorial tabs)
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-category-nav-minimal-editorial-v2

Changes applied (evidence-first)
- `assets/template-collection.css` - Replaced the heavy card/tab treatment with a cleaner modern navigation language:
  - removed panel/gradient/chip aesthetic,
  - introduced simple horizontal text tabs with animated underline indicator,
  - kept all tab text high-contrast and fully visible at rest,
  - simplified desktop interaction to color + underline only,
  - refined mobile select to a clean, understated, high-legibility control.
- `snippets/collection-breadcrumbs.liquid` - Removed decorative nav label markup to keep hierarchy minimal and content-focused while preserving robust category dedupe/current-state logic.

Validation snapshot
- Verified updated selectors and tab-state classes in `assets/template-collection.css` and `snippets/collection-breadcrumbs.liquid`.
- No inline CSS/JS was introduced; navigation remains semantic and lightweight.
- No browser visual run from terminal in this pass; storefront preview check required.

Open TODOs (next session)
1) Visual QA in storefront preview for desktop/mobile balance and confirm this minimal direction matches stakeholder preference.
2) If still too plain, add one premium accent only (e.g. subtle active tab background or micro-separator) without reducing contrast.

Session: Collection nav typography alignment to PDP breadcrumb
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-nav-typography-match-pdp-breadcrumb

Changes applied (evidence-first)
- `assets/template-collection.css` - Updated collection category nav text system to match PDP breadcrumb typography conventions from `assets/section-main-product.css`:
  - tabs set to `font-size: 1.2rem`, `font-weight: 500`, `line-height: 1.45`, `letter-spacing: 0`, non-uppercase,
  - tab default/hover/active colors aligned to breadcrumb muted/foreground pattern,
  - mobile select text adjusted to the same typography scale (`1.2rem`, `500`, `1.45`) for consistency.
- Kept category switching UX intact (desktop tabs + mobile select), while focusing this pass on text-size/style parity.

Validation snapshot
- Verified updated typography values are present in `assets/template-collection.css` under `.collection-category-nav__tab` and `.collection-category-nav__select`.
- No markup changes required for this alignment pass.

Open TODOs (next session)
1) Preview collection and product pages side-by-side to confirm perceived typographic parity under current global `layout/theme.liquid` overrides.
2) If needed, normalize only vertical rhythm (padding/margins) without changing text size/style.

Session: Remove collection style dropdown and unify category item sizing
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-collection-style-dropdown-removed-size-unified

Changes applied (evidence-first)
- `snippets/collection-breadcrumbs.liquid` - Removed mobile `<select>` category dropdown block entirely and made the category tab list the single navigation UI across breakpoints.
- `assets/template-collection.css` - Removed obsolete `.collection-category-nav__select*` styles and tuned tab spacing/height so category items stay visually consistent (including mobile) with breadcrumb typography (`1.2rem`, `500`, `1.45`).

Validation snapshot
- Confirmed no `CollectionCategorySelect` markup remains in `snippets/collection-breadcrumbs.liquid`.
- Confirmed no `.collection-category-nav__select` styles remain in `assets/template-collection.css`.
- Collection category nav now renders only as tab links (no dropdown open state).

Open TODOs (next session)
1) Visual check in preview for long category lists on narrow screens (horizontal scroll usability).
2) If needed, add subtle edge-fade cues for overflow while keeping typography unchanged.

Session: Mobile search UX + mobile announcement rotator refinement
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-search-ux-announcement-rotator

Changes applied (evidence-first)
- `snippets/header-search.liquid`
  - Added a new mobile-only empty state block (`.mobile-search-empty-state`) inside the search modal so tapping search on mobile shows a curated "Trending" list before typing.
  - Added five quick links mirroring requested competitor-style behavior:
    - Matching Family Outfits
    - Bamboo Clothes
    - Mommy and Me
    - PAW Patrol Clothes
    - Barbie Clothes
- `snippets/visible-header-search.liquid`
  - Removed the large legacy mobile override block that globally restyled mobile header/search/announcement behavior.
  - Kept this snippet focused on its desktop search wrapper rules only.
  - Scoped previous global selectors to `.EzfyHeaderSearch--desktop` to avoid affecting the mobile modal (`.search-modal__form`, `.predictive-search`, and predictive groups).
- `assets/mobile-header-ux.css` (new)
  - Added mobile-only search modal styling so the modal opens as a fixed overlay below the header (`margin-top: var(--header-height)`), preventing layout jump.
  - Styled search input and predictive results for cleaner readability and spacing.
  - Added styles for the new mobile trending list block.
  - Added mobile announcement bar polish for single-line centered text and hidden slider arrows/localization in mobile view.
- `assets/mobile-header-ux.js` (new)
  - Added mobile behavior for search modal:
    - toggles `body.mobile-search-open` while modal is open,
    - focuses search input on open,
    - shows/hides mobile empty state depending on input/predictive state,
    - relabels suggestions heading to "Trending" on mobile.
- `sections/header.liquid`
  - Included `mobile-header-ux.css` and `mobile-header-ux.js` so the new mobile search UX is active site-wide.
- `assets/mobile-announcement-rotator.js` (new)
  - Added mobile announcement rotator logic for `|`-delimited messages.
  - Rotates phrases with fade animation and adds contextual emoji prefixes (shipping/returns/secure) when none are present.
- `sections/announcement-bar.liquid`
  - Included `mobile-announcement-rotator.js`.
- `layout/theme.liquid`
  - Removed the old inline announcement/search block that included:
    - deprecated hardcoded mobile announcement CSS,
    - placeholder stylesheet loader (`PATH_TO_COMBINED_CSS_FILE`),
    - older one-off rotating text script.

Validation snapshot
- JS syntax check passed:
  - `node --check assets/mobile-header-ux.js`
  - `node --check assets/mobile-announcement-rotator.js`
- Confirmed placeholder loader string removed from active files.
- `shopify theme check` run still returns many pre-existing repo-wide warnings/errors unrelated to this session (including existing parser issues in `sections/header.liquid` and other historical files).

Open TODOs (next session)
1) Visual QA in `shopify theme dev` mobile viewport (home + collection + product) for:
   - search modal open/close transitions,
   - empty-state visibility behavior,
   - predictive search result spacing and scroll,
   - announcement rotation cadence and text truncation.
2) If desired, move trending terms from hardcoded Liquid list to a theme setting or metafield-backed source for merchant editing.
3) If the mobile announcement bar green tone should match a specific brand token, update `#0f8f68` in `assets/mobile-header-ux.css`.

Session: Mobile header alignment + announcement color revert
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-header-alignment-announcement-color-revert

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Removed hardcoded green announcement background overrides so mobile announcement bar uses the pre-existing/original theme color.
  - Preserved mobile announcement centering/one-line behavior while no longer forcing banner color.
  - Added mobile header grid alignment rules to keep menu icon, search icon, logo, and right icons in a single proportional row:
    - explicit 4-area grid (`drawer search heading icons`),
    - explicit grid-area assignment for `header-drawer`, `.mobile-header-search-icon`, heading, and icon cluster,
    - reduced/tuned mobile icon hit areas and glyph sizes,
    - reduced/tuned mobile logo max width/height for visual balance.

Validation snapshot
- Verified no `#0f8f68` references remain in `assets/mobile-header-ux.css`.
- Verified updated CSS is served by local preview (`mobile-header-ux.css` cache-busted asset URL).

Open TODOs (next session)
1) Visual QA on real devices (iPhone Safari + Android Chrome) to confirm logo centering against variable cart/account icon counts.
2) If logo appears too small/large on specific phones, tweak `max-width: 10.8rem` and `max-height: 3.2rem` in `assets/mobile-header-ux.css`.

Session: Mobile announcement bar full-bleed + compact height adjustment
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-announcement-fullbleed-compact

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Updated mobile announcement bar to be full-bleed edge-to-edge by forcing `width: 100vw` and centering with viewport margins.
  - Removed side inset on `.utility-bar__grid` (`padding-left/right: 0`) and forced `max-width: 100%`.
  - Reduced banner height to roughly half of prior mobile value (`3.2rem -> 1.6rem`) across utility/grid/announcement wrappers.
  - Enforced full centering (horizontal + vertical) for message text using flex alignment on `.announcement-bar__link` and `.announcement-bar__message`.
  - Reduced message text size to keep readability inside the new compact banner height (`1.2rem -> 1rem`).

Validation snapshot
- Verified updated rules are present in `assets/mobile-header-ux.css` under the mobile media query.
- Verified updated stylesheet is served in local preview (new cache-busted asset URL).

Open TODOs (next session)
1) Visual QA on narrow devices to confirm long rotating lines still read well at `1rem` in `1.6rem` height.
2) If text feels too tight, increase only height slightly (e.g. `1.8rem`) while preserving edge-to-edge behavior.

Session: Mobile cart icon proportional size adjustment
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-cart-icon-proportional-size

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Kept shared mobile icon glyph sizing for menu/search/account at `2rem`.
  - Increased only cart icon glyph size on mobile to `2.35rem` (`.header__icon--cart svg, .header__icon--cart .icon`) so cart appears visually proportional to menu/search.
  - No layout-width or header grid changes were made in this pass.

Validation snapshot
- Verified updated cart selector values exist in `assets/mobile-header-ux.css`.
- Verified updated stylesheet is served by local preview (new cache-busted asset URL).

Session: Mobile cart icon size increase (second pass)
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-cart-icon-second-pass

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Increased mobile cart glyph size from `2.35rem` to `2.5rem` for stronger visual parity with adjacent header controls.
  - No other mobile header spacing/layout values were changed.

Session: Desktop announcement banner full-width restoration
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-desktop-announcement-fullwidth-restored

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Added a desktop-only (`min-width: 990px`) rule block to restore full-bleed announcement banner width:
    - `announcement-bar-section` forced to viewport width (`100vw`) and centered with viewport margins,
    - utility/grid/announcement wrappers forced to `width: 100%` and `max-width: 100%`,
    - removed desktop side padding from `.utility-bar__grid`.
  - Mobile (`max-width: 989px`) announcement behavior remains unchanged.

Validation snapshot
- Verified new desktop media query block is present in `assets/mobile-header-ux.css`.
- Verified updated stylesheet is served in local preview (new cache-busted asset URL).

Session: Mobile search opens below header like menu + reliable X toggle
Date: 2026-02-23
AGENT_CONTINUITY_ANCHOR: 2026-02-23-mobile-search-below-header-x-toggle

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Updated mobile search open state to behave like a drawer under the header:
    - `details[open] > .search-modal` now anchors at `top: var(--header-height)` (instead of fullscreen inset overlay),
    - removed dimmed backdrop behavior for `.modal-overlay`,
    - set panel border/shadow and capped panel height for drawer-style UX.
  - Strengthened icon state toggling for mobile search trigger:
    - closed state hides close icon,
    - open state hides search icon and explicitly shows close (`X`) icon.

Validation snapshot
- Verified updated selectors in `assets/mobile-header-ux.css` under mobile media query.
- Verified updated stylesheet is served in local preview (new cache-busted asset URL).

Session: Mobile search drawer offset hardening + menu-like icon swap
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-offset-hardening

Changes applied (evidence-first)
- `assets/mobile-header-ux.js`
  - Added runtime mobile header metrics (`--mobile-header-bottom`, `--mobile-header-height`) based on `.section-header.getBoundingClientRect()`.
  - Ensured metrics update on mobile init, search open, viewport resize, and mobile scroll while search is open.
  - Set `--header-height` from the same measurement on mobile to avoid `0px` fallback when sticky header mode does not populate it.
- `assets/mobile-header-ux.css`
  - Updated mobile search drawer anchor to `top: var(--mobile-header-bottom, var(--header-height, 0px))` so the search panel opens below the header instead of covering it.
  - Reworked mobile search icon state swap to menu-like behavior using visibility/opacity/scale transitions between `.modal__toggle-open` and `.modal__toggle-close`.
  - Updated predictive search max-height calculations to use mobile header bottom offset for consistent available space.

Validation snapshot
- Verified updated rules exist in `assets/mobile-header-ux.css` under the mobile media query.
- Verified `assets/mobile-header-ux.js` passes syntax check (`node --check assets/mobile-header-ux.js`).

Open TODOs (next session)
1) Run manual mobile QA in local preview to confirm search drawer no longer overlays header in both sticky-header enabled and disabled configurations.
2) If any Safari-specific visual flicker appears during icon swap, add a `will-change: transform, opacity;` optimization on the toggle icons.

Session: Mobile search icon swap visibility + input icon alignment refinement
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-icon-swap-alignment

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Replaced mobile search toggle icon rules with menu-style icon swapping logic on the summary button:
    - both search and close glyphs are absolutely positioned in the trigger,
    - closed state hides `.icon-close`,
    - open state hides `.icon-search` and shows `.icon-close`.
  - Corrected mobile search input icon positioning:
    - `.search__button` and `.reset__button` now vertically center via `top: 50%` + `transform: translateY(-50%)`,
    - increased internal button hit box and centered icon alignment so icons no longer sit on the border.

Validation snapshot
- Verified updated selectors are present in `assets/mobile-header-ux.css`:
  - toggle state rules at `details[open] > .header__icon--search ...`,
  - centered field icon button placement for `.search__button` and `.reset__button`.

Open TODOs (next session)
1) Confirm on device that tapping mobile search shows the `X` immediately and consistently across repeated open/close cycles.
2) If icon appears 1-2px high/low on a specific device, tweak `top` and/or `width/height` values in `assets/mobile-header-ux.css` only.

Session: Mobile search field icon centering + focus color refinement
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-field-centering-focus-color

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Improved search field internals so the search icon and reset icon sit visually centered within the rounded input:
    - moved left icon inset inward (`left: 1.1rem`),
    - tightened icon glyph size (`1.6rem`),
    - centered buttons with explicit flex alignment and zero margin/padding.
  - Replaced harsh orange focus/edge appearance with a softer neutral style:
    - custom neutral border on `.field::after`,
    - subtle neutral focus state on `.field:focus-within`,
    - preserved existing rounded-pill look and mobile-only scope.

Validation snapshot
- Verified updated selectors and values are present in `assets/mobile-header-ux.css` (mobile media query block).

Open TODOs (next session)
1) Re-check on device after hard refresh to confirm icon sits fully inside the pill on all tested phone widths.
2) If needed, fine-tune icon inset by ±0.1rem based on device-specific rendering.

Session: Mobile search box cleanup (remove inner clear X + remove icon box)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-box-cleanup

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Removed inner clear/reset button in mobile search field by hiding `.reset__button`.
  - Reduced right-side input padding since clear button is no longer shown (`4.8rem -> 1.8rem`).
  - Removed boxed/square appearance around the left search icon button across normal/focus states by forcing:
    - transparent background,
    - no border/radius/box-shadow/outline,
    - no pseudo-element decoration on `.search__button`.

Validation snapshot
- Verified updated mobile selectors in `assets/mobile-header-ux.css`:
  - `.mobile-header-search-icon .reset__button { display: none !important; }`
  - focus-state neutralization for `.mobile-header-search-icon .search__button`.

Open TODOs (next session)
1) Confirm on-device that the search icon remains visually clean while focused/typing.
2) If needed, adjust left icon inset by small increments (`left: 1.0rem` or `1.2rem`) for final pixel alignment.

Session: Mobile search collections-first navigation + no page/article results
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-collections-routing

Changes applied (evidence-first)
- `snippets/header-search.liquid`
  - Added a mobile empty-state block that replaces generic trending suggestions with collection shortcuts:
    - Mommy and Me
    - Daddy and Me
    - Family Matching
    - Couple Matching
    - Maternity
  - Each shortcut now resolves URL via layered fallback:
    - candidate collection handles,
    - then main menu links/child links (title-normalized with `& -> and`),
    - then default `/collections/<handle>` fallback.
  - Added `data-collection-fallback-url="{{ routes.all_products_collection_url }}"` to the search form for collection-context fallback navigation.
  - Added hidden `<input name="type" value="product">` to keep full search submissions product-focused.
- `assets/mobile-header-ux.js`
  - Updated mobile search submit handling:
    - first tries keyword/title match against collection shortcuts,
    - then tries first predictive collection suggestion,
    - otherwise falls back to the all-products collection URL with query (`q`) instead of routing to a generic search page.
- `sections/predictive-search.liquid`
  - Reworked predictive rendering to only output collection + product groups.
  - Removed query/page/article groups and removed the “search for term” action block.
  - Kept product cards linking directly to product URLs.
- `assets/predictive-search.js`
  - Predictive request now explicitly scopes resources to `product,collection` (limit per resource type) and hides unavailable products.
- `sections/header.liquid`
  - Mobile header search render now passes `menu_handle: section.settings.menu` to support menu-based shortcut URL resolution.
- `snippets/visible-header-search.liquid`
  - Added hidden `<input name="type" value="product">` for visible header search to prevent page/article result routing on full search submits.

Validation snapshot
- Verified JavaScript syntax:
  - `node --check assets/mobile-header-ux.js`
  - `node --check assets/predictive-search.js`
- Verified updated collection shortcut mapping and fallback attributes in `snippets/header-search.liquid`.

Open TODOs (next session)
1) Manual mobile QA: test each shortcut and several typed queries to confirm routing lands on intended collections.
2) If any shortcut lands on an unintended collection due to menu title overlap, tighten title matching from contains-based to exact per your store menu labels.

Patch: Liquid condition compatibility fix for mobile collection shortcut matching
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-search-collections-routing-liquid-fix

Changes applied (evidence-first)
- `snippets/header-search.liquid`
  - Replaced unsupported parenthesized Liquid `if` conditions with compatible boolean-assignment pattern (`*_title_matches`) before final branch checks.

Validation snapshot
- Ran `shopify theme check --fail-level error --output json` and confirmed no `snippets/header-search.liquid` parser errors remain.
- Theme still reports unrelated pre-existing errors in other files (e.g., `sections/header.liquid`, `sections/main-list-collections.liquid`, `snippets/cjpod.liquid`, `tmp_products.json`).

Session: Mobile header mutual-exclusion (search vs menu) to prevent dual X state
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-header-mutual-exclusion

Changes applied (evidence-first)
- `assets/mobile-header-ux.js`
  - Added mobile-only helper utilities to close open header panels via native summary click paths:
    - close open mobile search details,
    - close open mobile menu drawer details.
  - Implemented top-level summary lookup without `:scope` selectors to reduce risk on older mobile browsers.
  - Added `bindMobileMenuDrawer()` to enforce single active panel on mobile:
    - when menu is opening, any open mobile search panel is closed first,
    - on menu `toggle` open state, search is force-closed as a safety net.
  - Updated mobile search `details.toggle` open branch:
    - closes any other open search panel instance,
    - closes an open menu drawer before keeping search open/focused.
  - Updated `init()` to bind both menu drawer coordination and mobile search behavior.

Validation snapshot
- Verified JavaScript syntax:
  - `node --check assets/mobile-header-ux.js`
- Verified logic is mobile-scoped (`(max-width: 989px)`) and does not run on desktop.

Open TODOs (next session)
1) Manual mobile QA: open search then tap menu, and open menu then tap search; confirm only one close icon/state is visible at any time.
2) Confirm behavior in sticky-header variants to ensure no focus-jump regressions when switching directly between menu and search.

Session: Mobile announcement bar height increase for readability
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-announcement-height

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Increased mobile-only announcement bar vertical space to reduce cramped text:
    - `.announcement-bar-section .utility-bar` height/min-height: `1.6rem -> 2.2rem`
    - `.announcement-bar-section .utility-bar .page-width.utility-bar__grid` height/min-height: `1.6rem -> 2.2rem`
    - `.announcement-bar-section .announcement-bar, .announcement-bar-section .announcement-bar__announcement` height/min-height: `1.6rem -> 2.2rem`
  - Relaxed message line box slightly for readability:
    - `.announcement-bar-section .announcement-bar__message` line-height: `1 -> 1.2`

Validation snapshot
- Confirmed the updated values are present under the mobile media query (`max-width: 989px`) in `assets/mobile-header-ux.css`.

Open TODOs (next session)
1) Manual mobile QA on a physical device: verify the announcement text no longer appears vertically cramped.
2) If final tuning is desired, adjust the shared height by +/- `0.1rem`.

Session: Mobile cart icon scale + persistent cart count bubble
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-cart-bubble-polish

Changes applied (evidence-first)
- `sections/cart-icon-bubble.liquid`
  - Added `cart_count` assignment and switched icon selection to `cart_count == 0` logic.
  - Cart count bubble now always renders (including empty cart) and always prints the numeric count.
  - Removed previous conditional that hid the bubble when cart was empty and removed the `<100` cap condition.
- `sections/header.liquid`
  - Updated header cart icon block to match the same `cart_count` logic used by `sections/cart-icon-bubble.liquid`.
  - Header now renders count bubble for empty and non-empty carts, ensuring initial render consistency before AJAX section refreshes.
- `assets/mobile-header-ux.css`
  - Increased mobile cart bag icon size (`2.5rem -> 2.95rem`) for better visual proportion with neighboring icons.
  - Added mobile-only badge styling for `.cart-count-bubble` (pill shape, gradient fill, stronger legibility, and elevated shadow).

Validation snapshot
- Ran `shopify theme check --fail-level error --output text`.
- Theme check still reports multiple pre-existing repository errors/warnings (including existing parser/schema/content issues in other files such as `sections/header.liquid`, `sections/main-list-collections.liquid`, `sections/email-signup-banner.liquid`, `snippets/cjpod.liquid`, and `tmp_products.json`).
- No command output indicated a new isolated syntax issue specific to the cart count changes.

Open TODOs (next session)
1) Mobile QA on device: confirm cart icon scale and badge position at narrow widths (320px, 375px, 430px).
2) Functional QA: add/remove items and verify header count shows `0` when empty and increments/decrements correctly in both cart drawer and cart notification flows.
3) If needed, fine-tune badge offset (`right`/`top`) by small increments for final pixel alignment with your selected logo/header spacing.

Patch: Mobile cart icon size increase (follow-up user request)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-cart-bubble-polish-followup

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Increased mobile cart icon container footprint for stronger visual presence:
    - `.section-header .header__icon--cart` size set to `4.2rem` square.
  - Increased bag glyph size further:
    - `.section-header .header__icon--cart svg/.icon` from `2.95rem` to `3.45rem`.
  - Rebalanced badge placement after icon scaling:
    - `.cart-count-bubble` offset updated to `top: 0.08rem`, `right: -0.42rem`.

Validation snapshot
- Verified updated cart sizing and offset values are present under the mobile media query block in `assets/mobile-header-ux.css`.

Open TODOs (next session)
1) Confirm on-device that the larger cart icon does not clip at 320px width and still aligns with search/menu icons.
2) If needed, fine-tune icon to `3.35rem` or `3.55rem` based on visual preference.

Session: Mobile menu-to-search handoff hardening (menu X must revert immediately)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-menu-to-search-immediate-close

Changes applied (evidence-first)
- `assets/mobile-header-ux.js`
  - Added `forceCloseMobileMenuDrawer()` fallback to immediately clear mobile menu open state when switching actions:
    - removes `open` and `menu-opening` states,
    - clears submenu open states,
    - restores menu summary `aria-expanded="false"`,
    - removes mobile/tablet/desktop overflow lock classes and `.section-header.menu-open`.
  - Updated `closeOpenMobileMenuDrawer()` to:
    - attempt native `headerDrawer.closeMenuDrawer(...)` first,
    - then force-close immediately if menu is still open (prevents persistent X icon while search opens).
  - Added capture-phase click binding on mobile search summary so opening search closes menu before the search modal open path runs.
  - Upgraded menu summary binding to capture phase for symmetric panel-switch behavior.

Validation snapshot
- Verified JavaScript syntax:
  - `node --check assets/mobile-header-ux.js`
- Verified this behavior remains mobile-scoped (`(max-width: 989px)`).

Open TODOs (next session)
1) Manual mobile QA: with menu open, tap search and confirm menu icon reverts to hamburger immediately while search opens.
2) Regression QA: open/close menu repeatedly after search handoff and confirm drawer scroll lock always clears correctly.

Patch: Mobile cart badge black + centered count + larger bag icon
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-cart-badge-black-centered

Changes applied (evidence-first)
- `assets/mobile-header-ux.css`
  - Increased cart touch target and icon size again for better proportion:
    - `.header__icon--cart` set to `4.6rem` square
    - cart icon glyph set to `3.9rem`
  - Changed item-count badge from red gradient to black:
    - `background: #111111`
    - replaced red shadow with neutral black shadow.
  - Enforced stronger centering for count text in the badge:
    - badge uses `display: grid; place-items: center;`
    - count span uses full-width/height flex centering and zero padding/margins.
  - Kept badge shape circular (`1.8rem x 1.8rem`, `border-radius: 50%`) and adjusted offset for alignment.

Validation snapshot
- Verified the new cart icon and badge rules are present under the mobile media query in `assets/mobile-header-ux.css`.

Open TODOs (next session)
1) On-device visual QA: verify badge remains centered for values `0-9` and still reads clearly.
2) If 2-digit counts are common, decide whether to keep strict circle or switch to pill (`min-width`) for `10+`.

Session: Mobile PDP breadcrumbs removed + larger media + balanced typography
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-media-typography-balance

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Added `small-hide` to the product breadcrumb wrapper:
    - `<div class="page-width page-width--product-breadcrumbs">` -> `<div class="page-width page-width--product-breadcrumbs small-hide">`
  - Effect: product breadcrumbs are hidden on mobile (`max-width: 749px`), reclaiming top-of-page space for media.
- `layout/theme.liquid`
  - Appended a new final mobile-only style block scoped to `.template-product` (`max-width: 749px`) that:
    - removes horizontal constraints/gutters around the main product media container and slider,
    - enforces full-width mobile media list items,
    - tightens product info wrapper spacing,
    - reduces mobile product title and price sizing,
    - slightly tightens vertical spacing between product info blocks.

Validation snapshot
- Verified selectors and edits are present:
  - `sections/main-product.liquid`: `page-width--product-breadcrumbs small-hide`
  - `layout/theme.liquid`: new `.template-product` mobile override block at file end.

Open TODOs (next session)
1) Mobile QA on actual device (320/375/430 widths): confirm breadcrumbs are hidden and first product image appears visually larger.
2) Visual QA for long product titles/pricing (including compare-at sale state) to confirm the new typography scale feels balanced.
3) If needed, fine-tune title size by ±`0.1rem` and info wrapper side padding by ±`0.2rem`.

Session: Mobile PDP size-chart first column sticky for horizontal scroll
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-size-chart-sticky-first-column

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Added a mobile-only CSS block (`max-width: 749px`) to keep the first table column visible while horizontally scrolling product-description tables.
  - Applied to `.template-product .product__description table` so size charts without `id="size-chart"` are also covered.
  - Sticky behavior details:
    - first `th`/`td` uses `position: sticky; left: 0;`
    - white background + subtle right divider shadow for readability while columns scroll.

Validation snapshot
- Verified selectors and sticky rules are present in `layout/theme.liquid` near the top inline style area.
- No automated theme validation run in this patch (manual mobile PDP QA still required).

Open TODOs (next session)
1) Manual QA on mobile product pages: horizontal-scroll size chart and confirm first column remains visible across varied chart widths.
2) Check a non-size table in product descriptions to confirm sticky first column does not create unwanted visual overlap.

Session: Mobile PDP full-bleed media polish + modern slider counter + balanced type scale
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-full-bleed-modern-counter-proportion-fix

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Updated the final mobile-only (`max-width: 749px`) `.template-product` override block to improve above-the-fold PDP composition:
    - Made gallery media visually edge-to-edge by removing mobile radius constraints and forcing product media images to fill (`width/height: 100%`, `object-fit: cover`) within the product media container.
    - Added more vertical breathing room between media and product info (`product__media-list` bottom spacing + increased `product__info-wrapper` top padding).
    - Reduced oversized mobile title and price typography to a more proportional premium scale.
    - Redesigned mobile image counter/controls into a modern pill treatment:
      - neutral translucent background + subtle border/shadow,
      - circular arrow buttons,
      - stronger counter hierarchy for current index.
    - Explicitly overrode earlier absolute-position slider button rule on mobile (`left/bottom/transform` reset) so controls sit cleanly below the image.

Validation snapshot
- Verified the updated mobile block is present at the end of `layout/theme.liquid` and remains scoped to `.template-product` and `max-width: 749px`.
- No automated browser visual diff in this patch; final confirmation requires manual mobile viewport QA.

Open TODOs (next session)
1) Manual QA on iPhone-class widths (320/375/390/430): confirm gallery feels full-bleed and image framing remains flattering across product aspect ratios.
2) Validate counter/arrow controls for 1 image, 2+ images, and video media; ensure disabled arrow states still look intentional.
3) If any products crop too aggressively, tune mobile media fit by switching to a softer frame (e.g., `object-position` per collection or section setting fallback).

Patch: Mobile PDP remove residual side gutters from gallery (grid--peek override)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-gallery-side-gutter-elimination

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Extended the final mobile PDP override block (`max-width: 749px`) to neutralize Dawn mobile `grid--peek` slider gutters that were still causing side whitespace:
    - removed slider left scroll-padding for product media list,
    - removed slider trailing pseudo-element spacing (`::after`),
    - removed first-slide left offset,
    - forced each media item to full-width sizing (`width/max-width/min-width/flex-basis: 100%`),
    - removed mobile grid gaps on product media list.

Validation snapshot
- Verified new selectors exist in the final mobile `.template-product` override block in `layout/theme.liquid`.
- Manual viewport QA still required to confirm edge-to-edge rendering on-device.

Open TODOs (next session)
1) Mobile QA on 320/375/390/430 widths: verify no side white space remains on first and subsequent slides.
2) Confirm no horizontal page scroll appears after removing slider pseudo-end spacing.

Patch: Mobile PDP force full-width media when constrain_to_viewport + contain are enabled
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-constrain-contain-full-width

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile `.template-product` override block, added explicit overrides for Dawn's constrained contain mode:
    - forced `.product-media-container.constrain-height` and `.product-media-container.constrain-height.media-fit-contain` to `width/max-width: 100%`,
    - reset side margins to `0`,
    - restored image media box height behavior by resetting `.product__media` padding-top to full ratio (`var(--ratio-percent)`) inside constrained containers.
  - Purpose: eliminate residual side white space caused by container width shrinking in mobile contain+constrained mode.

Validation snapshot
- Verified selectors are present in the final mobile product override block in `layout/theme.liquid`.
- Manual mobile QA required to confirm visual result in preview/device after cache refresh.

Open TODOs (next session)
1) Hard-refresh preview and verify first/next gallery images are edge-to-edge on mobile widths.
2) If any products become too tall after ratio reset, tune with a controlled mobile max-height while keeping width at 100%.

Patch: Mobile PDP gallery edge-to-edge fix moved to core section stylesheet
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-edge-to-edge-core-css

Changes applied (evidence-first)
- `assets/section-main-product.css`
  - Updated the native mobile PDP media slider rules (`max-width: 749px`) to remove side whitespace at the source:
    - removed mobile negative-margin/peek sizing (`margin-left` and `width` hacks),
    - forced product media slides to true full width (`width/max-width/min-width/flex-basis: 100%`),
    - removed mobile slider left-scroll padding and trailing pseudo spacing,
    - removed first-slide left offset from `grid--peek`,
    - removed media grid gaps on mobile.
  - Added explicit media image fill rules in the product media list (`object-fit: cover`) to keep visual coverage to both sides.
  - Added constrained-media overrides on mobile so `constrain-height`/contain mode cannot shrink media width below 100%.

Validation snapshot
- Verified updated rules are present in `assets/section-main-product.css` in both mobile media blocks.
- This patch applies through the section stylesheet directly (not reliant on `.template-product` wrapper classes).

Open TODOs (next session)
1) Hard-refresh mobile preview and verify the gallery is edge-to-edge on first and subsequent slides.
2) If any image crops too aggressively, reduce crop by switching the mobile image fit rule from `cover` to `contain` while preserving full-width container behavior.

Patch: Mobile PDP gallery counter redesigned as modern stepper
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-gallery-counter-stepper

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Converted the main product gallery mobile controls to a dedicated stepper variant:
    - added `slider-buttons--product-stepper` class on the gallery control wrapper,
    - added `slider-counter--product-stepper` class on the counter,
    - added `--step-progress` inline CSS variable initialization from `media_count`,
    - normalized the counter separator into a stylable element (`.slider-counter__separator`).
- `assets/section-main-product.css`
  - Added mobile-only (`max-width: 749px`) stepper styling scoped to product gallery controls:
    - premium pill container treatment (border, soft gradient, blur, shadow),
    - circular prev/next buttons with refined sizing and disabled/active states,
    - numeric stepper typography with tabular numerals,
    - progress track + animated fill driven by `--step-progress`.
  - Selector scope uses `.page-width--product-main` (not `.template-product`) so styles still apply in this theme variant where `<body>` is not carrying template-type classes.
- `assets/global.js`
  - Extended `SliderComponent` with `updateStepperCounter()` and invoked it during `update()`.
  - The method sets `--step-progress` from `currentPage/totalPages` so the visual stepper fill tracks slide position.

Validation snapshot
- Verified new stepper classes/selectors and JS hook are present via `rg`.
- Ran syntax validation: `node --check assets/global.js` (passes).
- Manual device/preview QA still required for final visual approval.

Open TODOs (next session)
1) Mobile QA on product pages (320/375/390/430 widths): confirm the stepper renders cleanly and updates correctly while swiping.
2) Validate behavior for media edge cases: 1 image, 2 images, many images, and mixed image/video media.
3) If legacy overrides in `layout/theme.liquid` visually conflict, consolidate/remove overlapping slider control rules there.

Patch: Mobile PDP stepper visibility fix (always below image)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-stepper-visibility-fix

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Removed legacy `hide_mobile_slider` gating logic that hid controls in several mobile states.
  - Updated stepper wrapper visibility so it now renders whenever `media_count > 0`.
  - Added `slider-buttons--single-media` class for one-image products so the line/counter still appears cleanly.
- `assets/section-main-product.css`
  - Added single-image stepper styling:
    - hides prev/next buttons for single-media case,
    - keeps the counter/progress line visible and centered below the image.

Validation snapshot
- Verified updated selectors/classes are present in markup + CSS.
- No JS changes required for this fix.

Open TODOs (next session)
1) Manual mobile QA: confirm stepper line is visible directly under gallery image on products with 1 image and with multiple images.
2) If spacing feels tight/loose, adjust top margin on `.slider-buttons--product-stepper` by ±`0.2rem`.

Patch: Mobile PDP explicit "more images" progress bar below gallery
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-more-images-progress-bar

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Added a dedicated mobile gallery progress element directly below the media slider when `media_count > 1`:
    - shows current/total (`1 / N`),
    - includes "Swipe for more photos" hint text,
    - includes a separate progress track container (`data-gallery-stepper`) not tied to `.slider-buttons` legacy selectors.
- `assets/section-main-product.css`
  - Added mobile styling for `.product-media-progress*` classes to make the indicator clean, centered, and clearly below the image.
- `assets/global.js`
  - Extended `updateStepperCounter()` so it also updates the new `data-gallery-stepper` component:
    - updates current/total text,
    - updates progress width via `--media-progress`.

Validation snapshot
- Syntax check: `node --check assets/global.js` (passes).
- Verified selectors/markup/JS hooks are present with `rg`.

Open TODOs (next session)
1) Mobile QA on live preview: verify the new progress bar is visible under the image and advances while swiping.
2) If desired, shorten/replace hint text (e.g., "More photos") for a more minimal look.

Patch: Mobile PDP image no-crop fix (prevent title-adjacent clipping)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-image-no-crop-fix

Changes applied (evidence-first)
- `assets/section-main-product.css`
  - In the mobile PDP media rules (`max-width: 749px`), changed product media image fit from `object-fit: cover` to `object-fit: contain` so full image bounds render without bottom cropping.
- `layout/theme.liquid`
  - In the final mobile `.template-product` override block, removed mobile media cap by adding `max-height: none !important;` to `.product__media-wrapper` / `.slider-mobile-gutter`.
  - Updated `.template-product .page-width--product-main .product__media img` from `object-fit: cover !important` to `object-fit: contain !important` and kept image width constrained to container (`max-width: 100% !important`).

Validation snapshot
- Verified selector updates are present with `rg` in both files:
  - `assets/section-main-product.css` mobile media image rule now uses `contain`.
  - `layout/theme.liquid` mobile product block now includes `max-height: none !important;` and `object-fit: contain !important;`.
- Manual device QA still required in theme preview (mobile widths) to confirm no cropping across mixed aspect ratios.

Open TODOs (next session)
1) Hard-refresh mobile PDP and confirm first and subsequent gallery images are fully visible (no bottom crop) on 320/375/390/430 widths.
2) Validate contain-mode appearance for very wide images; if letterboxing looks too strong, tune background/container treatment without reintroducing crop.

Patch: Mobile PDP force-gap below gallery to prevent title overlap clipping
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-force-gap-below-gallery

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Added a final mobile-only override block at end-of-file (ensures highest cascade priority over prior legacy mobile CSS) to:
    - remove media wrapper clipping caps (`max-height: none !important; overflow: visible !important;`),
    - push content below gallery down (`.product__media-wrapper { margin-bottom: 2.4rem !important; }` and `.product__info-wrapper { margin-top: 2.4rem !important; }`).
  - Scope is `.page-width--product-main` (not `.template-product`) so it applies in this theme variant even when `<body>` template class is absent.

Validation snapshot
- Verified rule placement at true file end via `nl -ba layout/theme.liquid | tail`.
- Verified selectors and values via `rg`.
- Manual mobile preview QA still required to confirm visible full image bottom on affected products.

Open TODOs (next session)
1) Hard-refresh mobile preview and verify the bottom of image is fully visible before title on 320/375/390/430 widths.
2) If spacing is too large, reduce gap values from `2.4rem` to `1.6rem` while keeping no overlap.

Patch: Mobile PDP gallery indicator de-dup + live bottom progress
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-indicator-dedupe-live-progress

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Hid the top in-slider stepper on mobile by adding `small-hide` to `slider-buttons--product-stepper` (keeps DOM controls for slider JS but removes duplicate visual control on small screens).
  - Scoped lower `product-media-progress` to mobile-only display with `medium-hide large-up-hide`.
  - Removed the "Swipe for more photos" hint text from the lower `product-media-progress` meta row.
- `assets/global.js`
  - Fixed lower progress synchronization by resolving `[data-gallery-stepper]` from the parent `media-gallery` when running inside `GalleryViewer-*`.
  - This makes lower `current/total` and `--media-progress` update while swiping/changing images.

Validation snapshot
- Syntax check: `node --check assets/global.js` (passes).
- Verified updated selectors/markup/hooks with `rg` and `nl`.

Open TODOs (next session)
1) Manual mobile QA on product page: confirm only the lower indicator is visible, the hint text is gone, and both count and line progress update on each image swipe.
2) If the lower indicator should be line-only (no numbers), remove `.product-media-progress__meta` entirely and keep only the track.

Patch: Mobile PDP product title size harmonization
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-title-size-harmonization

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the mobile product override block (`@media screen and (max-width: 767px)`), reduced title heading size for `.template-product .product__title h1, h2` from `1.72rem` to `1.44rem`.
  - Tightened title typography to better match surrounding mobile PDP text:
    - `line-height` changed from `1.34` to `1.3`
    - `letter-spacing` changed from `-0.01em` to `0`

Validation snapshot
- Verified the mobile rule values are present via targeted `sed`/`rg` inspection in `layout/theme.liquid`.
- Change is scoped to mobile-only product page title selectors; desktop title styles were not modified.

Open TODOs (next session)
1) Manual mobile preview QA on 320/375/390/430 widths to confirm title hierarchy now feels balanced against price and body text.
2) If further reduction is desired, test `1.36rem` as the next step-down while keeping the same line-height.

Patch: Mobile PDP title switched to breadcrumb-like typography
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-title-breadcrumb-style

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Replaced the mobile PDP title rule (`@media screen and (max-width: 767px)`) with breadcrumb-style typography for `.template-product .product__title h1, h2`:
    - `font-size: 1.1rem`
    - `line-height: 1.45`
    - `letter-spacing: 0.05em`
    - `text-transform: uppercase`
    - `color: #999`
  - Tightened title block spacing by reducing `.template-product .product__title` margin-bottom from `1rem` to `0.7rem`.

Validation snapshot
- Verified updated values are present in the final mobile override block.
- Change remains scoped to mobile product title selectors only.

Open TODOs (next session)
1) Manual mobile QA in preview to confirm the title now matches breadcrumb tone and no longer dominates the PDP.
2) If title becomes too faint, keep size/spacing but darken to `#7d7d7d`.

Patch: Mobile PDP size selection no-jump (disable variant auto-scroll on small screens)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-size-select-no-scroll

Changes applied (evidence-first)
- `assets/global.js`
  - Updated variant media activation call to pass a mobile-only scroll guard:
    - `setActiveMedia(..., { preventScroll: window.matchMedia('(max-width: 749px)').matches })`.
- `assets/media-gallery.js`
  - Extended `setActiveMedia()` to accept optional `options`.
  - Added `preventScroll` handling so when true, it still updates active media/horizontal slider position but skips the `window.scrollTo(...)` jump.

Why this addresses the issue
- Size selection triggers variant updates, which call `setActiveMedia()`.
- The prior behavior always attempted to scroll viewport back to media when media top was above viewport.
- On mobile, that produced the visible “screen moves up” jump after selecting a size.

Validation snapshot
- Syntax checks pass:
  - `node --check assets/global.js`
  - `node --check assets/media-gallery.js`
- Verified diff shows only the targeted mobile scroll guard changes.

Open TODOs (next session)
1) Manual mobile QA on product page (320/375/390/430 widths): select multiple sizes and confirm viewport position no longer jumps.
2) Confirm desktop behavior is unchanged when variant switches update media.

Patch: Variant selection no-jump expanded to color (always suppress variant-triggered viewport scroll)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-variant-color-no-scroll

Changes applied (evidence-first)
- `assets/global.js`
  - Updated variant media activation call in `renderProductInfo()` to always pass:
    - `setActiveMedia(..., { preventScroll: true })`
  - This replaces the prior mobile-width-only condition so both size and color variant selections avoid viewport jump.

Why this addresses the issue
- Color selections frequently switch `featured_media`, which triggers `setActiveMedia()` from variant change flow.
- Passing `preventScroll: true` for all variant-driven media switches prevents the gallery logic from calling `window.scrollTo(...)` during those updates.

Validation snapshot
- Syntax check: `node --check assets/global.js` (passes).
- Verified callsite now uses `preventScroll: true`.

Open TODOs (next session)
1) Manual product-page QA on mobile: switch between multiple colors and sizes; confirm viewport no longer moves up.
2) Quick desktop sanity check: verify variant image still updates correctly when selecting color.

Patch: Mobile PDP first-image scroll-return clipping guard
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-first-image-scroll-clipping-guard

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Extended the final mobile override block (`@media screen and (max-width: 749px)`) with additional PDP media stability rules scoped to `.page-width--product-main`:
    - removed residual mobile max-height/overflow clipping from gallery containers (`.slider-mobile-gutter`, `.product__media-list`, `.product__media-item`, including first item),
    - enforced stable image fitting (`width/height: 100%`, `object-fit: contain`, centered) for product media images,
    - disabled mobile hover transform on product media images to avoid touch/scroll-state clipping artifacts.

Why this addresses the issue
- Prior theme-level mobile overrides in `layout/theme.liquid` included conflicting image/container constraints and transform behavior.
- The new final-scoped override ensures the first visible image keeps the same framing after scrolling away and back, instead of rendering clipped.

Validation snapshot
- Verified the new rules are present at the end of `layout/theme.liquid` via `nl -ba` inspection.
- No automated storefront visual test was run in this session.

Open TODOs (next session)
1) Manual mobile QA on affected product pages (320/375/390/430 widths): scroll down and back up, confirm first image no longer appears cut.
2) Confirm swipe to second/third media still works visually as expected and no new letterboxing regressions were introduced.

Patch: Mobile PDP swipe restore (re-enable gallery horizontal overflow)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-swipe-restore-overflowx

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile PDP override block (`@media screen and (max-width: 749px)`), removed `.page-width--product-main .product__media-list` from the selector that forced `overflow: visible !important`.
  - Added a dedicated `.page-width--product-main .product__media-list` rule to preserve clipping guard intent while restoring swipe container behavior:
    - `max-height: none !important`
    - `overflow-x: auto !important`
    - `overflow-y: visible !important`

Why this addresses the issue
- Dawn mobile gallery swipe depends on the slider list (`.product__media-list.slider--mobile`) remaining horizontally scrollable.
- The previous override forced `overflow: visible !important` on the list, overriding base slider overflow and preventing horizontal swipe.

Validation snapshot
- Verified the updated mobile CSS block in `layout/theme.liquid` now keeps `overflow-x: auto` on `.product__media-list`.
- No automated storefront interaction test was run in this session.

Open TODOs (next session)
1) Manual mobile QA on product page (320/375/390/430 widths): verify horizontal swipe between gallery images works again.
2) Recheck the prior first-image clipping scenario (scroll down and back up) to confirm it remains fixed with this overflow adjustment.

Patch: Mobile sticky ATC gated by required option selection
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-sticky-atc-choose-options-gate

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Replaced the prior mobile sticky ATC implementation (one-click pass-through to `.product-form__submit`) with a stateful sticky CTA scoped to the current section id.
  - Added state logic:
    - shows `Choose options` when required selectors (for example `Size`) are not selected,
    - scrolls to and highlights the first missing option group on tap,
    - switches to mirrored main CTA behavior/text once selections are complete,
    - respects disabled main CTA state (`Sold out` / unavailable) once options are complete.
  - Added sticky price synchronization to keep sticky price aligned with variant price changes in `#price-{{ section.id }}`.
  - Kept existing intersection behavior (sticky only visible when primary ATC is out of viewport on mobile).
- `layout/theme.liquid`
  - Added mobile styles for new sticky states:
    - `requires-options` visual treatment for sticky button,
    - disabled sticky button styling,
    - temporary highlight style for missing option group target (`.sticky-option-target--highlight`).

Why this addresses the issue
- The previous sticky bar could appear and trigger submit before shopper-selected variant options were complete, which is confusing with a forced blank size placeholder.
- The new flow preserves sticky conversion intent while preventing premature add-to-cart by routing incomplete states to option selection first.

Validation snapshot
- Verified updated sticky markup/script and selectors in `sections/main-product.liquid`.
- Verified corresponding mobile CSS states in `layout/theme.liquid`.
- No automated browser test was run in this session.

Open TODOs (next session)
1) Manual mobile QA on PDP (320/375/390/430 widths):
   - initial sticky shows `Choose options` when size is blank,
   - tap scrolls to size selector and highlight appears,
   - after selecting size/color, sticky switches to `Add to cart` and submits correctly.
2) Validate edge cases:
   - single-variant products keep direct `Add to cart`,
   - sold-out variants show disabled sticky CTA after full option selection,
   - sticky price matches selected variant price.

Patch: Mobile PDP title downsize with selector scope fix
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-title-downsize-page-width-scope

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the mobile PDP override block (`@media screen and (max-width: 749px)`), expanded the title selector to include:
    - `.page-width--product-main .product__title h1`
    - `.page-width--product-main .product__title h2`
  - Kept existing `.template-product` selectors and updated mobile title typography to:
    - `font-size: 1.2rem`
    - `line-height: 1.35`
    - `letter-spacing: 0.01em`
    - `text-transform: none`

Why this addresses the issue
- The previous mobile title override depended on `.template-product`, while the current `<body>` class in `layout/theme.liquid` does not include template-specific classes.
- Scoping to `.page-width--product-main` ensures the smaller title style applies on product pages in mobile viewport.

Validation snapshot
- Verified the updated selector/value block is present in `layout/theme.liquid` near the final mobile PDP overrides.
- No browser-based visual QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on product page (320/375/390/430 widths): confirm title now appears much smaller and visually consistent with nearby PDP copy.
2) If further reduction is needed, test `1.0rem` using the same `.page-width--product-main` selectors.

Patch: Mobile PDP title and price visual rebalance (larger, polished hierarchy)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-title-price-visual-rebalance

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile PDP override block (`@media screen and (max-width: 749px)`), increased title prominence:
    - `.template-product .product__title h1/h2` and `.page-width--product-main .product__title h1/h2` set to:
      - `font-size: 1.45rem`
      - `line-height: 1.28`
      - `letter-spacing: 0`
      - `font-weight: 600`
      - `color: #1f1f1f`
  - Slightly increased title spacing:
    - `.template-product .product__title { margin-bottom: 0.8rem }`
  - Rebalanced mobile price typography so it matches the larger title and still reads as primary:
    - Added `.page-width--product-main` price selectors alongside existing `.template-product` selectors.
    - Main price (`.price--large`, regular, sale) set to:
      - `font-size: 1.82rem`
      - `line-height: 1.22`
      - `letter-spacing: -0.01em`
      - `font-weight: 600`
    - Compare-at sale price (`.price--on-sale .price-item--regular`) set to:
      - `font-size: 1.3rem`

Why this addresses the issue
- The title is now noticeably bigger and more premium, while the price is scaled to keep a clean, intentional visual hierarchy.
- Including `.page-width--product-main` ensures these mobile adjustments apply even when `.template-product` is not present on `<body>`.

Validation snapshot
- Verified updated selectors and values in `layout/theme.liquid` mobile block.
- No browser-based visual QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on PDP (320/375/390/430 widths): confirm title/price balance feels right across short and long product names.
2) If needed, fine-tune one notch:
   - title to `1.38rem` for slightly calmer hierarchy, or
   - price to `1.74rem` if it feels too dominant.

Patch: Mobile PDP size column sticky scope fix for measurement tables
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-size-column-sticky-page-width-scope

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Updated the existing mobile sticky-first-column table block (`@media screen and (max-width: 749px)`) to include `.page-width--product-main` selectors in addition to `.template-product`.
  - Added sticky/scroll coverage to:
    - `.page-width--product-main .product__description table`
    - `.page-width--product-main #size-chart`
  - Kept behavior unchanged for sticky first column:
    - `position: sticky; left: 0;`
    - white background and subtle separator shadow.

Why this addresses the issue
- The previous sticky-column rule depended on `.template-product`, but current theme `<body>` classes do not include template classes.
- Scoping to `.page-width--product-main` ensures the `Size` (first) column remains visible while horizontally scrolling measurement tables on mobile PDP.

Validation snapshot
- Verified updated selector set exists in `layout/theme.liquid` in the mobile sticky table block near the top inline styles.
- No browser-based mobile QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on product page widths `320/375/390/430`: confirm `Size` column remains pinned while scrolling measurements.
2) Check at least one non-size description table on mobile to confirm sticky first column still looks acceptable.

Patch: Mobile PDP option controls spacing and border harmonization
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-options-spacing-border-harmonization

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile PDP override block (`@media screen and (max-width: 749px)`), added a scoped mobile-only options polish for:
    - `variant-selects` container
    - `.product-form__quantity` container
    - nested select controls, labels, quantity input/buttons, and quantity helper text.
  - Key style changes:
    - Added consistent vertical spacing and internal padding for variant + quantity groups.
    - Set `max-width: 100%` and `min-width: 0` for option groups to avoid cramped fit-content behavior on small screens.
    - Simplified borders/shadows (`1px` subtle borders, `box-shadow: none`) on selects and quantity shell.
    - Increased mobile control legibility (`font-size: 1.6rem` for select/quantity input) and tightened label spacing/letter-spacing for cleaner readability.
    - Kept styling scoped to `.page-width--product-main .product__info-container` so desktop and non-PDP forms remain unaffected.

Why this addresses the issue
- The previous mobile options area inherited dense spacing and heavier visual treatment, which made size/color/quantity controls feel tight.
- The new mobile-only block creates clear separation between controls, reduces visual noise from heavy borders/shadows, and improves tap/read comfort on smaller screens.

Validation snapshot
- Verified new selectors/rules are present at the end of `layout/theme.liquid` inside the final mobile media query.
- No automated or browser-based QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA (`320/375/390/430` widths): confirm size/color/quantity spacing is consistently airy and readable.
2) Validate iOS/Android focus behavior on select and quantity controls (ensure no unintended clipping or overlap with sticky ATC).
3) Check one product using pill/swatch option style to confirm the simplified radio border rule still looks correct.

Session: PDP mobile sticky ATC gated by size+color selection
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-sticky-atc-size-color-gate

Changes applied (evidence-first)
- `sections/main-product.liquid` - Updated the sticky mobile ATC script to require size/color option selection before the sticky bar can become visible on mobile.
- `sections/main-product.liquid` - Added option-name/value parsing helpers so sticky gating detects `Size` and `Color/Colour` option groups across dropdown and radio-style pickers.
- `sections/main-product.liquid` - Updated sticky visibility flow to use an explicit `canShowSticky` gate with IntersectionObserver state, preventing sticky CTA display until required selections are complete.
- `sections/main-product.liquid` - Preserved existing behavior after required selections: price sync, disabled-state mirroring, and missing-option scroll/highlight fallback.

Open TODOs (next session)
1) QA on mobile preview with a few PDPs that use different option naming patterns (e.g., `Color`, `Colour`, products with only one option) to confirm gating and visibility transitions remain correct.

Patch: Mobile PDP gallery counter corner placement and compact vertical spacing
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-gallery-counter-corner-compact-spacing

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile PDP style override block (`@media screen and (max-width: 749px)`), repositioned the gallery counter/progress presentation for mobile:
    - Styled `.page-width--product-main .product-media-progress__meta` as a floating pill anchored at the lower-right corner area of the gallery image.
    - Tightened `.product-media-progress` vertical margins and reduced track visual height to bring the progress bar closer to the image.
  - Reduced empty vertical space between gallery and product details stack:
    - `.page-width--product-main .product__media-wrapper { margin-bottom: 0.55rem !important; }`
    - `.page-width--product-main .product__info-wrapper { margin-top: 0.35rem !important; }`
  - Compacted product content stack spacing on mobile:
    - `.page-width--product-main .product__title { margin-bottom: 0.6rem !important; }`
    - `.page-width--product-main .product__info-container > * + * { margin-top: 1.05rem !important; }`

Why this addresses the issue
- The image count indicator is now visually attached to the image area instead of feeling detached below it.
- The progress bar now sits much closer to the gallery, reducing perceived dead space.
- The product title and subsequent PDP elements start higher and flow with tighter spacing for a more compact mobile layout.

Validation snapshot
- Verified the updated selectors and values exist in `layout/theme.liquid` within the mobile PDP override block.
- No browser-based QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on PDP at `320/375/390/430` widths:
   - confirm counter badge appears in the bottom-right corner region of the image,
   - confirm progress bar sits directly below with reduced gap.
2) Validate compact spacing with long product titles and products that have many blocks (price badges, inventory, variant picker, quantity, buy buttons).
3) If the counter overlaps edge content on very tall/narrow images, adjust only `bottom`/`right` offsets in `.product-media-progress__meta`.

Patch: Mobile PDP share button anchored to image top-right
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-share-top-right-image

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Added a dedicated mobile share control directly inside the main media gallery slider markup:
    - `<button class="share-button__button product__media-share medium-hide large-up-hide" data-mobile-share-button ...>`
  - This places the control in the same DOM region as the product image, enabling reliable top-right overlay positioning on mobile.
- `assets/media-gallery.js`
  - Added `mobileShareButton` element lookup in the `media-gallery` custom element.
  - Added click handling (`handleMobileShareClick`) for the new mobile share control:
    - Uses `navigator.share` when available.
    - Falls back to `navigator.clipboard.writeText(window.location.href)` with a short visual "copied" state class toggle.
  - Kept existing gallery behavior intact; only added optional share handling.
- `layout/theme.liquid`
  - In the final inline style block:
    - Added desktop hide rule for `.product__media-share` (`min-width: 750px`) so the new control is mobile-only.
    - Added mobile-only rules (`max-width: 749px`) to:
      - hide the default info-column share block (`.product__info-container > .share-button`) to avoid duplicate share icons,
      - set `.slider-mobile-gutter` to `position: relative`,
      - position `.product__media-share` at top-right (`top/right: 1.2rem`) with circular glass-style visual treatment,
      - style icon size and copied-state appearance.
- `sections/main-product.liquid`
  - Removed the previously misplaced static `mobile-share` button that had been inserted inside complementary products slider controls (not the main product image area).

Why this addresses the issue
- The share control now lives in the product media gallery itself, so mobile positioning is anchored to the image region instead of unrelated sliders or global absolute offsets.
- Mobile styling now consistently places the share button at the product image top-right while preserving visual balance with image content and the product info stack below.

Validation snapshot
- `node --check assets/media-gallery.js` passes (no syntax errors).
- Verified selectors/anchors exist via search:
  - `data-mobile-share-button` in `snippets/product-media-gallery.liquid` and `assets/media-gallery.js`
  - `.product__media-share` and `.product__info-container > .share-button` rules in `layout/theme.liquid`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on PDP (`320/375/390/430` widths): confirm share button appears at image top-right and does not overlap critical image content.
2) Tap-test share behavior on iOS Safari + Android Chrome:
   - native share sheet opens where supported,
   - clipboard fallback applies visible copied-state where native share is unavailable.
3) Confirm desktop/tablet do not show the overlay share icon and that existing share behavior outside mobile remains acceptable.

Patch: Mobile PDP share button compact size + centered icon + subtler top-corner placement
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-share-compact-centered-corner

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the mobile PDP share overlay block (`@media screen and (max-width: 749px)`), refined `.page-width--product-main .product__media-wrapper .product__media-share.share-button__button`:
    - Reduced top-right offset from `1.2rem` to `0.8rem`.
    - Reduced circular control diameter from `3.6rem` to `2.9rem` (`width/height/min-*`), with `!important` to reliably override older global rules.
    - Added `padding: 0 !important` and `line-height: 0` to prevent any internal offset and keep icon centering exact.
    - Softened visual prominence with slightly lighter background (`rgba(255, 255, 255, 0.86)`) and lower shadow (`0 0.5rem 1.2rem rgba(16, 18, 22, 0.14)`).
  - Refined icon alignment for `.page-width--product-main .product__media-wrapper .product__media-share .icon`:
    - Reduced icon size from `1.5rem` to `1.3rem`.
    - Added `display: block`, `margin: 0`, and `flex: 0 0 auto` to keep the glyph perfectly centered inside the circular button.

Why this addresses the issue
- The share button occupies less visual space on mobile PDP.
- The icon is centered by explicit flex/padding/line-height handling, removing baseline/margin drift.
- The control sits closer to the top corner and appears less dominant over the product image.

Validation snapshot
- Verified updated selectors and values are present in `layout/theme.liquid` under the mobile PDP share overlay rules.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Mobile QA at `320/375/390/430` widths to confirm center alignment and non-overlap on varied product media.
2) Tap-test share action to ensure interaction remains unchanged after style-only adjustments.

Patch: Mobile PDP counter resized and pinned inside image bottom-right
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-counter-inside-image-bottom-right

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Moved the mobile gallery progress block (`.product-media-progress` with `data-gallery-stepper`) from a sibling of `#GalleryViewer-*` to inside the `slider-component` container.
  - This makes the counter/progress overlay position relative to the actual image slider frame instead of the area below it.
- `layout/theme.liquid`
  - In the final mobile PDP override block (`@media screen and (max-width: 749px)`), updated mobile counter/progress styling:
    - `.product-media-progress` is now `position: absolute` at the gallery bottom-right with bounded max width.
    - `.product-media-progress__meta` was reduced in footprint (smaller min-width, padding, font-size, and tighter spacing) for a subtler counter badge.
    - `.product-media-progress__track` was shortened and thinned to sit under the badge while staying inside the image area.
    - Added `.product-media-progress__track::after` override to keep the progress fill legible against the image overlay treatment.

Why this addresses the issue
- The counter is now anchored inside the product image frame, bottom-right, instead of appearing outside/below image boundaries.
- The counter badge is visibly smaller and less dominant while remaining readable.
- The progress indicator remains attached to the counter and contained within the image area for consistent mobile navigation context.

Validation snapshot
- Verified markup location change in `snippets/product-media-gallery.liquid` (progress block now inside `slider-component`).
- Verified mobile selectors/values in `layout/theme.liquid` for `.product-media-progress`, `.product-media-progress__meta`, and `.product-media-progress__track`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA on PDP (`320/375/390/430` widths): confirm the counter/track remain fully inside the image frame on first media and while swiping.
2) Validate overlap behavior on very busy image corners; if needed, only tune `right`/`bottom` offsets in `.product-media-progress`.
3) Confirm the counter remains visible when products include mixed media (image/video/model) in the gallery.

Patch: Mobile PDP title-price spacing tightened for compact hierarchy
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-title-price-gap-tighten

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the final mobile PDP override block (`@media screen and (max-width: 749px)`), added a targeted adjacency rule:
    - `.template-product .product__info-container .product__title + [id^='price-']`
    - `.page-width--product-main .product__info-container .product__title + [id^='price-']`
  - Set `margin-top: 0.35rem !important;` on the adjacent price block.

Why this addresses the issue
- The generic mobile stack rule (`.product__info-container > * + *`) still controls overall block rhythm.
- The new adjacency override only reduces spacing when the price block directly follows the product title, making title and price visually cohesive without compressing unrelated PDP sections.

Validation snapshot
- Verified the new selector/value block exists in `layout/theme.liquid` within the mobile PDP styles.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA at `320/375/390/430` widths to confirm title-to-price spacing feels compact and readable across short and long titles.
2) Check one product where title is not immediately followed by price to confirm no unintended spacing regressions.

Patch: Mobile PDP media stepper moved closer to image
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-stepper-closer-image

Changes applied (evidence-first)
- `layout/theme.liquid`
  - In the mobile product media reset block (`@media screen and (max-width: 749px)`), reduced:
    - `.template-product .page-width--product-main .product__media-list` margin from `0 0 2.2rem` to `0 0 0.65rem`.

Why this addresses the issue
- The previous `2.2rem` bottom margin created excess vertical gap under the product image before the mobile stepper/progress indicator.
- Lowering it to `0.65rem` pulls the indicator much closer to the image and uses mobile viewport height more efficiently.

Validation snapshot
- Confirmed updated value exists in `layout/theme.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA at `320/375/390/430` widths to confirm the indicator now sits snugly under/against the image with no awkward gap.
2) Verify no overlap regressions on products with mixed media ratios (portrait, landscape, video).

Patch: Mobile PDP sticky ATC size-only visibility gate + selected size display
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-sticky-atc-size-only-with-size-label

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Updated sticky ATC markup to include a details container with:
    - existing sticky price,
    - new `data-sticky-mobile-atc-size` line for selected size text.
  - Replaced the prior required-option gate function with `getSizeSelectionState()`:
    - only options whose name matches `size` are considered for sticky visibility gating,
    - sticky visibility is blocked until all size option groups have a selected value,
    - tracks first missing size option for focus/scroll targeting.
  - Added `syncStickySize()` to render `Size: <selected value>` in sticky ATC whenever size selection is complete.
  - Updated sticky state and click handling:
    - uses size-only gating for `canShowSticky`,
    - keeps existing fallback behavior that prompts for any other missing option on tap.
- `layout/theme.liquid`
  - Added mobile sticky styles for:
    - `.sticky-mobile-atc__details` (stacked price + size text),
    - `.sticky-mobile-atc__size` (small uppercase size label with ellipsis handling).

Why this addresses the issue
- On mobile PDP, sticky ATC no longer appears until the shopper picks a size.
- Once visible, sticky ATC now shows the currently selected size directly in the sticky bar.

Validation snapshot
- Verified modified markup/script blocks and selectors in `sections/main-product.liquid`.
- Verified added sticky size styling in `layout/theme.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA (`320/375/390/430` widths) for products using size dropdowns and size radio/pill pickers.
2) Verify sticky ATC shows expected behavior when size is selected but another option (e.g., color) is not yet selected.
3) Confirm long size labels truncate cleanly in `.sticky-mobile-atc__size` without crowding the CTA button.

Patch: Mobile PDP sticky ATC hidden on initial load until explicit size interaction
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-pdp-sticky-atc-hide-on-load-until-size-click

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Added `hasUserSelectedSize` session flag in sticky ATC script, defaulting to `false` on page load.
  - Updated sticky visibility gate so mobile sticky ATC remains hidden while either:
    - size is not complete, or
    - shopper has not explicitly interacted with a size option yet.
  - Added size interaction tracking helpers:
    - `getSizeGroupFromTarget(target)` to detect if an event target belongs to a size option group,
    - `markUserSizeSelection(target, eventType)` to mark explicit size selection.
  - Wired variant picker events:
    - `change` marks size selection for dropdown/radio updates,
    - `click` marks radio/pill/swatch taps (while intentionally ignoring dropdown click-only interactions).
  - Extended size state object with `firstSizeOption` so fallback scroll targeting can still focus size controls when needed.

Why this addresses the issue
- Sticky ATC cannot appear at first load anymore, even if a size is preselected by theme defaults.
- Sticky ATC appears only after the shopper has actively selected/interacted with size and the main Add to Cart button is out of viewport.

Validation snapshot
- Verified updated gate condition and event listeners in `sections/main-product.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile QA for both size dropdown and size radio/pill products to confirm sticky remains hidden until explicit size interaction.
2) Confirm preselected-size products do not show sticky until user taps/changes size.
3) Verify no regressions when size is selected and a non-size option is still missing (sticky should show choose-options state only after size interaction).

Patch: PDP info panel visual override + size details card aligned to reference design
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-info-panel-reference-style

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Appended a final, end-of-file PDP style override block (after prior PDP/mobile overrides) scoped to:
    - `.template-product .page-width--product-main .product__info-wrapper`
    - `.template-product .page-width--product-main .product__info-container`
  - Restyled the product info panel to a rounded elevated card treatment (container spacing, radius, border, shadow).
  - Updated title/price hierarchy and spacing to match the requested reference look.
  - Refined free-shipping badge styling to a larger green pill with icon alignment.
  - Normalized installment text styling for the Shop Pay line.
  - Reworked variant dropdown presentation (pill-shaped selects, larger typography, caret placement, focus ring).
  - Removed legacy boxed wrappers around `variant-selects`/quantity controls in this final override layer.
  - Restyled `.size-chart-wrapper` and `.sc-*` classes to a dark-header/white-card format with rounded metric pills.
  - Restyled quantity control to pill layout with circular +/- buttons and centered numeric input.
  - Added mobile adjustments (`max-width: 749px`) so desktop/mobile both follow the same visual language with tuned sizing.
- `assets/size-conversion.js`
  - Added robust value formatting helpers:
    - `stripTrailingZeros()`
    - `convertValueWithRange()` (handles numeric ranges for cm->in and kg->lbs conversion)
    - `appendUnitIfMissing()`
  - Updated `formatMeasurementWithUnits()` to output a single combined value string (instead of split dual pills).
  - Updated generated size card header:
    - icon changed to ruler-style,
    - title format now `SIZE DETAILS — <SELECTED SIZE>`.
  - Updated measurement row generation to:
    - include units in label text (`Height (cm / in)`),
    - render one `.sc-pill` per measurement row using formatted combined values.

Why this addresses the issue
- The final PDP override now controls the exact visual treatment of the requested area (title, price, shipping badge, Shop Pay text, size/color controls, size details card, quantity) in both mobile and desktop contexts.
- Size detail values now render in the same one-pill-per-row format as the provided reference, including correct range conversions.

Validation snapshot
- Confirmed the final override block exists at the end of `layout/theme.liquid` (after earlier PDP override blocks), ensuring precedence.
- Ran `node --check assets/size-conversion.js` successfully (no syntax errors).
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP visual QA on desktop and mobile (`320/375/390/430`, tablet, and full desktop widths) against the reference screenshot.
2) Confirm size detail output on products where source chart values are single values, pre-split values, and ranges.
3) Verify no regressions on products using pill/radio variant pickers (this override is dropdown-focused).

Patch: PDP reference override moved into document head to ensure size chart styles apply
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-size-chart-override-head-placement-fix

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Found `Final PDP visual override` style block placed after `</html>` (outside document structure).
  - Moved that entire style block to immediately before `</head>` so it is loaded as normal page CSS.
  - Confirmed line placement now:
    - override starts around `layout/theme.liquid:1604`
    - `</head>` closes after the block.

Why this addresses the issue
- CSS outside the document end is not guaranteed to apply consistently across browsers/caching states.
- Moving the override into `<head>` ensures the size chart and PDP control restyling is consistently applied.

Validation snapshot
- Verified marker and structure via search:
  - `Final PDP visual override` appears in head scope.
  - `</body>`/`</html>` now occur after the override block, with no duplicate override block after them.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Hard-refresh PDP and manually confirm size chart visuals now match reference on desktop and mobile.
2) If any single detail still differs, do a final pixel pass (header height, label weight, pill spacing).

Patch: PDP style forced to closer screenshot match (v2 exact override)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-exact-screenshot-override-v2

Changes applied (evidence-first)
- `layout/theme.liquid`
  - Added a new style block immediately before `</head>` labeled:
    - `PDP exact screenshot override (highest priority)`
  - This block intentionally re-overrides prior PDP styling for closer visual match to reference screenshot:
    - lighter gray info panel container with rounded corners/shadow,
    - adjusted title/price scale and spacing,
    - green free-shipping capsule,
    - subtler installment text,
    - full-width rounded dropdown pills (size/color) with softer borders/shadows,
    - dark-gradient size-details header,
    - larger measurement labels,
    - single rounded gray value pills,
    - compact rounded quantity control with circular +/- buttons.
- `assets/size-conversion.js`
  - Updated conversion precision to 1 decimal:
    - `cmToInches`: `toFixed(1)`
    - `kgToLbs`: `toFixed(1)`
  - This aligns generated values closer to screenshot format (e.g. `47.2-51.2`, `41.9-49.6`).

Why this addresses the issue
- Prior style layers were still visually too far from the target reference.
- This v2 override is loaded after earlier theme PDP rules and is fully scoped to PDP selectors to force a closer screenshot match.

Validation snapshot
- Verified both markers exist in `layout/theme.liquid`:
  - original final override,
  - new `PDP exact screenshot override (highest priority)` block.
- Ran `node --check assets/size-conversion.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Hard refresh and visually compare against screenshot at same viewport size.
2) If still off, tune only the remaining deltas: title size/line-break, select height, header bar height, and pill font-size.

Patch: Section-scoped PDP hard override for screenshot-style matching
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-main-product-section-scoped-hard-override

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Added section-scoped high-specificity CSS under the existing `{% style %}` block using selectors prefixed by:
    - `#MainProduct-{{ section.id }} .dlm-reference-ui ...`
  - Added class `dlm-reference-ui` to `<product-info>` container so override applies only to this PDP block.
  - Force-styled target elements to match requested screenshot aesthetic:
    - light gray rounded product info card + soft shadow,
    - bold title / clean price hierarchy,
    - soft green free-shipping capsule,
    - uppercase option labels,
    - large rounded dropdown pills (size/color) with subtle border/shadow,
    - dark header size details card,
    - larger measurement labels and gray rounded value pills,
    - compact rounded quantity control with circular +/- buttons.
- `assets/size-conversion.js`
  - Kept 1-decimal conversion precision (`toFixed(1)`) for cm->in and kg->lbs to stay close to screenshot values.

Why this addresses the issue
- Previous global head styles were still being contested by multiple theme overrides.
- This patch shifts control into the section itself with stronger scope + specificity, so the intended visual style should win for the exact product UI block.

Validation snapshot
- Verified `dlm-reference-ui` class is present on `product__info-container`.
- Verified new scoped override selectors exist at top of `sections/main-product.liquid` style block.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Hard refresh PDP and verify screenshot alignment on mobile and desktop.
2) If still off, tune only remaining deltas (title line-break weight, dropdown height, size-card header thickness, quantity width).

Patch: Hide single-value Color/Style selectors on PDP variant picker
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-hide-single-color-style-options

Changes applied (evidence-first)
- `snippets/product-variant-picker.liquid`
  - Added per-option detection for single-value Color/Style option sets:
    - `option.values.size <= 1`
    - option name contains `style`, `color`, or `colour` (case-insensitive).
  - Added `hide_single_value_option` and applied `hidden aria-hidden="true"` on rendered picker wrappers for all picker types (`swatch`, `button`, `dropdown`).
  - Kept the option markup in DOM (instead of removing it) so `variant-selects` index-based variant resolution continues to work.

Why this addresses the issue
- Customers no longer see a meaningless selector when Color/Style has only one possible value.
- Variant matching logic remains intact because hidden controls still provide the full option list expected by theme JS.

Validation snapshot
- Verified updated condition and hidden attributes are present in `snippets/product-variant-picker.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on a product with one Color/Style value: confirm selector is hidden and add-to-cart still works.
2) Manual PDP QA on a multi-color/multi-style product: confirm selectors still render and variant switching works.

Patch: Restore PDP add-to-cart after single-value Color/Style hide regression
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-atc-regression-single-option-hide-fix

Changes applied (evidence-first)
- `snippets/product-variant-picker.liquid`
  - Reworked single-value Color/Style hiding behavior:
    - still detects `style`, `color`, `colour` options with `option.values.size <= 1`,
    - now renders those options as hidden dropdown inputs (not hidden swatch/radio groups), ensuring a concrete selected value is always present for variant matching.
  - Hidden single-value controls remain in DOM for index/order compatibility with variant resolution.
- `assets/global.js`
  - Hardened `VariantSelects.updateVariantStatuses()` to avoid null dereferences when no `:checked` node is present in a wrapper.
  - Added `getOptionValue(wrapper)` helper with guarded value extraction (`select.value`, checked radio, checked option fallback).
- `sections/main-product.liquid`
  - Sticky mobile ATC option checks now skip hidden option groups (`group.hidden`) in:
    - size-completion scanning,
    - first-missing-option detection.

Why this addresses the issue
- Hidden single-value options no longer depend on radio checked state; variant matching receives stable option values.
- Defensive guards prevent JS exceptions from interrupting variant/change-to-ATC flows.
- Sticky ATC no longer blocks on intentionally hidden auto-selected option groups.

Validation snapshot
- Ran `node --check assets/global.js` successfully.
- Verified patched selectors/logic in `snippets/product-variant-picker.liquid`, `assets/global.js`, and `sections/main-product.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on products with single-value Color/Style: verify both main and sticky ATC add correctly.
2) Manual PDP QA on multi-option products: verify selectors render normally and variant switching remains correct.

Patch: PDP size details hide empty/placeholder attributes
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-size-details-hide-empty-attributes

Changes applied (evidence-first)
- `assets/size-conversion.js`
  - Added value guard helpers to normalize and classify placeholder content as missing (`-`, `—`, `–`, `--`, `---`, `n/a`, `na`, `none`, `null`, `not available`, `not applicable`, plus dash-only combinations like `- / -`).
  - Reused these guards while reading chart rows so Age/Height metadata parsing ignores placeholder entries.
  - Updated size-row rendering to skip any measurement whose label or value is missing/placeholder.
  - Updated measurement formatting to avoid carrying placeholder fragments into output pills.
  - Added no-data fallback when a resolved size row contains no valid measurement values after filtering, so the UI shows the existing unavailable message instead of an empty details card.
  - Consolidated unavailable state HTML into `unavailableSizeMarkup()` for consistent fallback output.

Why this addresses the issue
- Size details now only render attributes with actual data.
- Placeholder rows (including plain hyphen values) are omitted from the UI, keeping the section clean and relevant.
- If all attributes for a selected size are placeholders, customers see a clear unavailable state instead of empty rows.

Validation snapshot
- Ran `node --check assets/size-conversion.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on products where size chart cells include `-`, `—`, and mixed placeholders like `- / -`; confirm those rows are hidden.
2) Manual PDP QA on rows with real ranges (e.g. `120-130`) to confirm valid hyphenated values still render.

Patch: PDP rounded container alignment + interactive background spacing
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-rounded-container-interactive-spacing

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Added shared PDP style tokens inside the section-scoped override:
    - `--dlm-surface-radius` for consistent rounded shells.
    - `--dlm-control-surface-padding` for breathing room around controls.
  - Updated the outer `.dlm-reference-ui` card to use `border-radius: var(--dlm-surface-radius)` (desktop keeps larger radius by overriding the variable in the media query).
  - Added explicit gray rounded control surfaces for interactive blocks:
    - `variant-selects .product-form__input` now has gray background, matching rounded radius, and internal padding.
    - `.product-form__quantity` now has gray background, matching rounded radius, and internal padding.
  - Tightened quantity-control spacing so rounded buttons no longer visually touch the gray surface:
    - added wrap/gap/padding on `.price-per-item__container`,
    - added internal padding + box sizing on `.quantity`,
    - reduced button size and grid columns for consistent inset spacing.

Why this addresses the issue
- The outer PDP card and internal interactive surfaces now share the same radius token, so curvature is visually consistent.
- Interactive controls sit inside padded gray shells, which prevents rounded controls from overlapping/touching background edges.

Validation snapshot
- Verified updated selectors and tokens are present in `sections/main-product.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP visual QA on mobile + desktop to confirm radius consistency and control spacing match expectation.
2) Verify variant dropdown caret alignment still looks correct with the new padded control surface wrapper.

Patch: PDP remove square select rectangle + retune gray palette
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-remove-select-rectangle-retune-gray

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Added scoped color tokens for the PDP card and controls:
    - `--dlm-card-bg`, `--dlm-control-surface-bg`, `--dlm-control-pill-bg`, `--dlm-control-pill-border`.
  - Updated outer card and interactive surface backgrounds to use the new gray palette.
  - Removed Dawn default square field chrome for the Size dropdown by disabling:
    - `variant-selects .product-form__input .select:before`
    - `variant-selects .product-form__input .select:after`
  - Also disabled default quantity pseudo layers:
    - `.product-form__quantity .quantity:before`
    - `.product-form__quantity .quantity:after`
  - Tuned select/quantity pill border, fill, and shadow to keep a soft rounded look without the square inner rectangle.

Why this addresses the issue
- The square rectangle in the screenshot came from Dawn `.select` pseudo-elements; they are now explicitly removed in this PDP scope.
- Gray tones for the container and control backgrounds are now consistent and intentionally matched.

Validation snapshot
- Verified updated selectors and new color tokens exist in `sections/main-product.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Hard refresh PDP and confirm the Size area no longer shows any square rectangle on desktop/mobile.
2) Confirm adjusted gray palette matches expected mock/reference and tweak token values only if needed.

Patch: PDP add-to-cart reliability hardening (sticky + form fallback)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-atc-reliability-sticky-form-fallback

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Updated sticky mobile ATC gating to check only whether size options are complete (removed the extra `hasUserSelectedSize` requirement).
  - Removed now-unused helper functions tied to explicit size-click tracking.
  - Result: sticky ATC no longer blocks valid preselected size states.
- `assets/product-form.js`
  - Added constructor guards for missing form/submit button nodes to prevent hard runtime failures.
  - Added `canRenderCart` capability checks before calling cart drawer methods (`getSectionsToRender`, `setActiveElement`, `renderContents`).
  - Added fallback redirect to cart page when cart drawer/cart notification methods are unavailable.
  - Result: add-to-cart still submits even if cart UI custom element methods are missing/uninitialized.
- `snippets/product-variant-picker.liquid`
  - Kept the Size placeholder option, but only marks it `selected` when `option.selected_value` is blank.
  - Result: avoids conflicting selected states that can leave the picker in an inconsistent non-addable state on some browsers.

Why this addresses the issue
- Sticky ATC previously required explicit user interaction even when a valid size was already selected, which could prevent adds in real shopper flows.
- Product form submit previously assumed cart drawer methods always existed; when they do not, submission could fail before `/cart/add` request handling completed.
- Size dropdown placeholder no longer competes with real selected variants.

Validation snapshot
- Ran `node --check assets/product-form.js` successfully.
- Verified removal of `hasUserSelectedSize`/`markUserSizeSelection` references in `sections/main-product.liquid`.
- Verified updated placeholder selection logic in `snippets/product-variant-picker.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on mobile sticky ATC for products with preselected size and single-size variants.
2) Manual PDP QA on desktop main ATC to confirm cart drawer render path and fallback behavior.
3) Confirm variant defaults (including Size) show expected selected value on first load across Safari/Chrome.

Patch: Variant change ATC fail-safe + null-guard hardening
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-variant-change-atc-failsafe-null-guards

Changes applied (evidence-first)
- `assets/global.js`
  - In `onVariantChange()`, when a valid `currentVariant` exists, immediately syncs Add to Cart enabled/disabled state from variant availability before async section refresh.
  - Added null guard in `updateVariantInput()` for missing hidden `input[name="id"]` nodes.
  - Added fetch `.catch(...)` in `renderProductInfo()` to restore Add to Cart state from the selected variant if section refresh fails.
  - Added guard in inventory visibility toggle to avoid dereferencing missing `inventorySource`.
  - Hardened `toggleAddButton()` and `setUnavailable()` against missing button text node/form node.

Why this addresses the issue
- Previously, selecting a size could disable ATC while waiting on section refresh; if refresh failed/errored, the button could stay non-functional.
- The new flow keeps button state aligned with the selected variant and recovers cleanly from async refresh failures.

Validation snapshot
- Ran `node --check assets/global.js` successfully.
- Ran `node --check assets/product-form.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA: choose size, confirm main ATC becomes clickable immediately and adds to cart.
2) Manual PDP QA: confirm variant switching still updates price/media and ATC sold-out state correctly.

Patch: Single-color hide compatibility rewrite + ATC no-op safeguards
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-single-color-hide-compat-atc-noop-safeguards

Changes applied (evidence-first)
- `snippets/product-variant-picker.liquid`
  - Reworked single-value Color/Style hiding to preserve original picker structures per picker type:
    - swatch stays `fieldset` (hidden only via wrapper attributes),
    - button stays `fieldset` (hidden only via wrapper attributes),
    - dropdown stays dropdown (hidden only via wrapper attributes).
  - Removed prior custom branch that converted hidden single-value options into forced dropdown markup.
  - Moved size-chart insertion trigger from `forloop.first` to `option_downcased contains 'size'` to avoid missing chart container when first option is hidden color/style.
- `assets/global.js`
  - Added `getSingleOptionFallback(position)` and integrated it into `updateOptions()` and `updateVariantStatuses()`.
  - If an option value is missing/blank but that option has exactly one variant value across product data, variant resolution now auto-fills that single value.
  - This specifically hardens hidden single-option flows so ATC variant resolution cannot fail due an empty hidden selector value.
- `assets/product-form.js`
  - Added no-op click protections and stale-state recovery:
    - exits early on actual `disabled` / `loading` states,
    - clears stale `aria-disabled="true"` before submission attempt,
    - guards spinner lookup.
  - Added `fetchConfig` fallback if global helper is unavailable.
  - Added `cart_add_url` resolution fallback to `window.routes` and native form submit fallback when unavailable.
- `assets/size-conversion.js`
  - Removed forced `sizeSelect.value = ''` reset on load.
  - Keeps optional placeholder insertion but no longer programmatically clears an existing selected size.
  - Initializes size chart by calling `updateSizeMessage()` without resetting dropdown state.

Why this addresses the issue
- The previous hidden-single-option implementation changed control type/shape and could desync option resolution in edge cases.
- Variant resolution now has deterministic single-option fallback values for hidden controls.
- Submit path now has hard fallbacks so button clicks cannot silently no-op due stale aria state or missing helpers.
- Size conversion script no longer rewrites size state at load, reducing mismatch risk between visible selections and variant state.

Validation snapshot
- Ran `node --check assets/global.js` successfully.
- Ran `node --check assets/product-form.js` successfully.
- Ran `node --check assets/size-conversion.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on product with single Color + multiple sizes: select size then ATC (main + sticky).
2) Manual PDP QA on product with multi-color: ensure selectors render and variant switching still works.
3) Confirm size chart still appears for size dropdown when first option is hidden single-color/style.

Patch: Product-form submit now resolves variant id directly from selectors
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-product-form-direct-variant-resolution-fallback

Changes applied (evidence-first)
- `assets/product-form.js`
  - Added `resolveVariantFromSelectors()` to derive selected variant from current `variant-selects` controls + embedded variant JSON.
  - Added `getSingleOptionValue()` fallback so hidden single-value options (like one Color/Style) still resolve deterministically.
  - Added `syncVariantIdFromSelectors()` to force hidden `input[name="id"]` to the resolved variant before submit.
  - On submit, button disabled state now re-synced from the resolved variant availability, preventing stale disabled/no-op states.

Why this addresses the issue
- Even if upstream variant UI state drifts (especially after hiding single-value Color/Style), product-form now computes and submits the correct variant id directly at click time.
- This bypasses the failure mode where ATC click appears to do nothing because variant id/button state was stale.

Validation snapshot
- Ran `node --check assets/product-form.js` successfully.
- Ran `node --check assets/global.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on a product with single Color + multiple Sizes (the original regression path).
2) Confirm ATC request payload includes correct variant id after size selection.

Patch: Emergency rollback of single-value Color/Style hiding
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-emergency-rollback-single-value-color-style-hide

Changes applied (evidence-first)
- `snippets/product-variant-picker.liquid`
  - Disabled single-value Color/Style hide conditions by removing the dynamic `hide_single_value_option = true` branches.
  - Picker wrappers still support the flag, but flag is now always false (no hiding occurs).

Why this addresses the issue
- This is the safest rollback to known picker behavior while preserving all ATC submit hardening.
- It removes the most likely source of recent variant-resolution regressions tied to hidden single-option controls.

Validation snapshot
- Verified `hide_single_value_option` no longer receives true assignments.
- Ran `node --check assets/product-form.js`, `assets/global.js`, and `assets/size-conversion.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA: choose size then Add to Cart on affected products.
2) Reintroduce single-value option hiding only after adding explicit regression tests.

Patch: Product-form ATC fallback path reset to Dawn baseline + hard cart fallback
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-product-form-baseline-fallback-cart-redirect

Changes applied (evidence-first)
- `assets/product-form.js`
  - Removed the prior direct variant-resolution submit path (`resolveVariantFromSelectors` / `syncVariantIdFromSelectors`) and restored a Dawn-style submit flow.
  - Kept safe constructor guards for missing `form`/submit button and guarded hidden variant-id input enabling.
  - Added route resolver helper (`getRoute`) to support both `window.routes` and legacy `routes` globals.
  - Added robust fallback helpers:
    - `resetSubmitState(spinner)`
    - `redirectToCartOrSubmit()`
  - Submission now:
    - blocks only true in-flight submissions (`loading`) and truly disabled button states,
    - clears stale `aria-disabled` before a new attempt,
    - falls back to native form submit when `cart_add_url` is missing,
    - redirects to cart if AJAX/cart-render runtime path fails,
    - removes stale `aria-disabled` in `finally` whenever button is not disabled.

Why this addresses the issue
- Prevents the silent no-op path where submit errors (route/cart-render/runtime) leave the shopper on PDP with no cart update.
- Removes the more complex custom variant-resolution layer that introduced extra failure surfaces.
- Ensures ATC falls back to a visible cart navigation instead of failing silently.

Validation snapshot
- Ran `node --check assets/product-form.js` successfully.
- Ran `node --check assets/global.js` successfully.
- Ran `node --check assets/size-conversion.js` successfully.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on affected product: choose size, click main ATC, verify cart count/drawer updates.
2) Manual mobile QA for sticky ATC path on same product.
3) If issue persists, capture browser console + network `/cart/add` response payload for one failed click.

Patch: Hard rollback of ATC path to main-branch baseline behavior
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-hard-rollback-atc-to-main-baseline

Changes applied (evidence-first)
- Restored these files to exact `HEAD` (`main` @ `e0c7b96`) contents:
  - `assets/product-form.js`
  - `assets/global.js`
  - `snippets/product-variant-picker.liquid`
  - `assets/size-conversion.js`
- This removed all uncommitted ATC-related experimental hardening/regression paths introduced after baseline.

Why this addresses the issue
- Re-establishes the same PDP ATC and cart-drawer interaction model that existed on main branch before the recent local ATC edits.
- Removes redirect/fallback behaviors that could move shoppers away from PDP on submit-path errors.

Validation snapshot
- Ran `node --check assets/product-form.js` successfully.
- Ran `node --check assets/global.js` successfully.
- Ran `node --check assets/size-conversion.js` successfully.
- Verified these files are no longer modified in `git status`.

Open TODOs (next session)
1) Manual PDP QA on affected product: select size then click main Add to Cart.
2) Confirm cart drawer opens from right side and item count increments.
3) If still failing, inspect any remaining non-ATC local modifications (`sections/main-product.liquid`, `layout/theme.liquid`) for runtime side effects.

Patch: Product cards use full-image ratio in collections and recommendations
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-product-card-image-ratio-adapt-collections-recommendations

Changes applied (evidence-first)
- `templates/collection.json`
  - Updated `sections.product-grid.settings.image_ratio` from `"portrait"` to `"adapt"`.
- `templates/product.json`
  - Updated `sections.main.blocks.complementary_main.settings.image_ratio` from `"square"` to `"adapt"`.
  - Updated `sections.related-products.settings.image_ratio` from `"square"` to `"adapt"`.

Why this addresses the issue
- `adapt` uses each product image's native aspect ratio in card rendering, which avoids fixed-frame cropping from `square`/`portrait` and better preserves full dress/product visibility in listings and recommendations.

Validation snapshot
- Verified effective template settings with `rg`:
  - `templates/collection.json` image ratio now `adapt`.
  - `templates/product.json` recommendation image ratios now `adapt` for both complementary and related products blocks.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual QA on `/collections/*`: confirm product cards show full garments without top/bottom crop on desktop and mobile.
2) Manual QA on PDP recommendations: confirm related/complementary cards show full products and spacing remains acceptable.
3) If any card heights become visually inconsistent, adjust section-level columns or spacing instead of reintroducing fixed crop ratios.

Patch: Product gallery thumbnails switched to portrait + no-crop rendering
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-product-thumbnails-portrait-no-crop

Changes applied (evidence-first)
- `assets/section-main-product.css`
  - Changed product thumbnail tile ratio from square to portrait by updating `.thumbnail-list__item::before` padding from `100%` to `150%`.
  - Changed `.thumbnail img` from `object-fit: cover` to `object-fit: contain` and added centered positioning to prevent thumbnail cropping.
- `layout/theme.liquid`
  - Updated desktop thumbnail-grid overrides under the 750px+ media query from `80x80` to `80x120` cells.
  - Updated `.thumbnail.global-media-settings img` in that block to `height: 120px` and `object-fit: contain`.
  - Updated additional desktop thumbnail override from `100x100` to `80x120` and switched `object-fit` from `cover` to `contain`.

Why this addresses the request
- Thumbnails are now portrait/vertical instead of square.
- Thumbnail images use contain-mode rendering, so the full dress remains visible with no crop.

Validation snapshot
- Verified modified selectors and values via grep/diff:
  - Portrait ratio (`padding-bottom: 150%`) for thumbnail items.
  - Thumbnail dimensions set to portrait (`80x120`) in theme-level desktop overrides.
  - Thumbnail image fit switched to `contain` in both base and override rules.
- No browser manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA desktop/mobile: confirm all thumbnail media display full garment and spacing remains acceptable.
2) Check hover zoom on thumbnails still feels intentional now that images are contain-fit.

Patch: PDP desktop layout compact centering (image/details closer)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-desktop-compact-centered-columns

Changes applied (evidence-first)
- `assets/section-main-product.css`
  - Updated desktop PDP container sizing (`.page-width--product-main` and `.page-width--product-breadcrumbs`) to a narrower centered layout:
    - `990px+`: `max-width` from `min(178rem, calc(100vw - 2.8rem))` to `min(136rem, calc(100vw - 8rem))`.
    - `1400px+`: `max-width` from `min(184rem, calc(100vw - 2rem))` to `min(142rem, calc(100vw - 10rem))`.
    - `1600px+`: added explicit container cap `min(146rem, calc(100vw - 12rem))`.
  - Rebalanced large-media desktop columns to bring product media and details visually closer while keeping outer whitespace:
    - `990px+`: media/info `70/30` -> `58/42`.
    - `1400px+`: media/info `72/28` -> `57/43`.
    - `1600px+`: media/info `74/26` -> `56/44`.
  - Reduced desktop info-wrapper side padding for tighter inter-column spacing:
    - `2.2rem` -> `1.6rem` at `990px+`.
    - `2rem` -> `1.8rem` at `1400px+`.
  - Added explicit flex-basis values on media/info wrappers at desktop breakpoints and neutralized legacy media shift with `transform: none` on the large-media wrapper in this scope.

Why this addresses the request
- The PDP core content now stays in a tighter centered band on desktop, with extra whitespace pushed outward to the far left/right.
- The image and product detail columns are proportioned closer together, reducing the perceived empty space between them.

Validation snapshot
- Verified updated desktop selectors and breakpoint values via `git diff -- assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual desktop PDP QA at ~1024px, ~1440px, and ~1920px to confirm spacing matches the requested compact/centered feel.
2) Validate both `media_position: left` and `media_position: right` products for balanced spacing.

Patch: Mobile sticky ATC gated by explicit size selection + scroll-safe behavior
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-sticky-mobile-atc-size-gate-scroll-fix

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Updated sticky-mobile-ATC script state with `hasUserConfirmedSizeSelection` (default `false`) so sticky visibility is gated behind explicit shopper interaction with a Size option.
  - Added `markSizeSelectionFromEvent(event)` and wired it to `variant-selects` `change`/`click` listeners to capture real size-choice interaction.
  - Added `isSizeOptionGroup(group)` helper and reused it in size-state detection.
  - Updated sticky visibility logic to keep sticky hidden when Size exists but has not been explicitly selected by the user (even if a variant is preselected in the DOM).
  - Added body offset syncing when sticky is visible (`sticky-mobile-atc-visible` + `--sticky-mobile-atc-offset`) and `aria-hidden` sync on the sticky bar.
- `layout/theme.liquid`
  - In mobile sticky-ATC CSS block, added `body.template-product.sticky-mobile-atc-visible` bottom padding using `--sticky-mobile-atc-offset` + safe area inset.
  - Added sticky interaction hardening for scroll behavior:
    - `.sticky-mobile-atc` now uses `pointer-events: none` and `touch-action: pan-y`.
    - `.sticky-mobile-atc__details` is non-interactive (`pointer-events: none`).
    - `.sticky-mobile-atc__btn` remains clickable with `pointer-events: auto`, `touch-action: manipulation`, and reduced tap highlight.

Why this addresses the issue
- Sticky bar no longer appears before an explicit Size selection on the current product page, matching the requested behavior.
- Sticky visibility still depends on main ATC leaving viewport.
- Body bottom spacing and touch handling reduce mobile scroll interference from the fixed sticky bar.
- On a different product page, the script state resets and sticky stays hidden until Size is selected again.

Validation snapshot
- Reviewed diffs for `sections/main-product.liquid` and `layout/theme.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA: confirm sticky stays hidden until shopper explicitly selects Size.
2) Manual mobile PDP QA: after Size selection + scroll past main ATC, confirm sticky appears and page scroll remains smooth in both directions.
3) Manual navigation QA across multiple products to verify sticky selection state does not leak between PDPs.

Patch: Hide desktop PDP media counter when thumbnail gallery is visible
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-hide-desktop-pdp-media-total-counter

Changes applied (evidence-first)
- `assets/section-main-product.css`
  - In `@media screen and (min-width: 750px)`, added a rule to hide `.slider-counter--product-stepper` for `.product--thumbnail` and `.product--thumbnail_slider`.

Why this addresses the issue
- Removes the desktop/tablet image count indicator below the main product image when thumbnails are already visible as navigation.

Validation snapshot
- Verified added selector via `git diff` in `assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA at `>=750px`: confirm the media counter number is hidden for thumbnail layouts.
2) Confirm thumbnail navigation remains visible and functional.

Patch: Size chart streamlined to single-unit rows with cm/in toggle
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-size-chart-single-unit-toggle

Changes applied (evidence-first)
- `assets/size-conversion.js`
  - Added a persistent unit-system preference (`metric`/`imperial`) stored in `localStorage` key `dlm_size_chart_unit_system`.
  - Reworked size-chart rendering so each measurement row shows one value only, based on selected unit system.
  - Added a chart-level unit toggle (`cm` / `in`) in the header; selecting a toggle rerenders rows using the chosen system.
  - Moved units into row labels (e.g., `Bust (cm)` or `Bust (in)`), keeping value pills unit-free to avoid repeated unit text.
  - Added robust dual-unit handling for split values (`x / y`) and single-source values via unit conversion helpers.
  - Added HTML escaping for dynamic labels/values before injection.
  - Preserved existing size-resolution flow (direct match, aliases, adult token normalization, age/height fallback).
- `sections/main-product.liquid`
  - Updated scoped size-chart styles under `#MainProduct-{{ section.id }} .dlm-reference-ui` to support the new unit toggle and compact one-line row layout.
  - Added styles for `.sc-header__main`, `.sc-unit-toggle`, and `.sc-unit-toggle__btn` with active-state treatment.
  - Tightened row/value typography so labels and values read as concise single lines.

Why this addresses the request
- Shopper now chooses unit once (cm or in) via a clear toggle.
- Each measurement row renders only one unit at a time.
- Unit appears once in the label, removing duplicate/repeated units in value output.

Validation snapshot
- Syntax check passed: `node --check assets/size-conversion.js`.
- Reviewed updated selectors/logic with `nl -ba` output for both edited files.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on desktop/mobile: select size, toggle `cm`/`in`, confirm rows switch to one-unit output and labels update correctly.
2) Verify products with pre-split dual values (`x / y`) and single-source values both render correctly in each unit mode.
3) Confirm unit preference persistence across PDP reload/navigation behaves as desired.

Patch: Related products mobile swipe carousel (You may also like)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-related-products-mobile-swipe-carousel

Changes applied (evidence-first)
- `sections/related-products.liquid`
  - Added `component-slider.css` include so slider classes are available where this section renders.
  - Added mobile slider gating logic:
    - `columns_mobile_int = section.settings.columns_mobile | plus: 0`
    - `show_mobile_slider = recommendations.products_count > columns_mobile_int`
  - Updated the recommendations grid `<ul>` to include slider markup/classes when mobile overflow exists:
    - Added `id="Slider-{{ section.id }}"`.
    - Added `contains-card contains-card--product` and conditional `slider slider--mobile` classes.
  - Updated each recommendation `<li>`:
    - Added slide id `Slide-{{ section.id }}-{{ forloop.index }}`.
    - Added conditional `slider__slide` class when mobile slider is enabled.

Why this addresses the request
- On mobile (`<=749px`), related products now render as a horizontal swipe row when there are more products than the configured mobile columns.
- Desktop and non-overflow mobile layouts remain grid-based.

Validation snapshot
- Verified section diff with `git diff -- sections/related-products.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA: confirm “You may also like” scrolls horizontally via swipe and no longer stacks as a long vertical list when overflow exists.
2) Confirm desktop PDP layout remains unchanged for related products.

Patch: Size-chart regression fix (conversion + resolver hardening)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-size-chart-regression-fix-conversion-and-coverage

Changes applied (evidence-first)
- `assets/size-conversion.js`
  - Fixed multiple regex patterns that were over-escaped and failing to parse:
    - Header unit extraction (`Bust (cm/in)` style headers)
    - Numeric extraction for age/height metadata
    - Adult token extraction
    - Age and height range parsing in fallback resolvers
    - Soft normalization whitespace handling
  - Added reliable unit conversion behavior so toggle selection changes numeric values, not just UI state:
    - Supports single numbers (`95`), ranges (`86-92`), and split values (`95 / 37.4`)
    - Supports conversions for `cm<->in` and `kg<->lbs`
  - Ensured row output is concise and non-redundant:
    - Row labels now render measurement names only (no repeated `(cm/in)`)
    - Value pills show numbers only (no repeated unit text)
    - Unit context is controlled by the top toggle (`cm` / `in`)
  - Expanded size-chart table discovery from strict `#size-chart` to robust fallback selectors:
    - `table#size-chart`, `table[id*="size-chart"]`, `table[class*="size-chart"]`
  - Added age-label fallback resolver for size keys when products encode age in size names (e.g. `Baby 9 Months`) but do not provide a dedicated Age column.
  - Strengthened normalization for punctuation/case mismatch (`Mother.` vs `Mother`).

Repository audit run
- Audited `products_export_1 2_IMPORT_READY.csv` with a scripted pass over products containing `size-chart` references.
- Results:
  - Products with size-chart reference: `205`
  - Products resolvable with machine-readable chart data after logic hardening: `197`
  - Remaining unresolved: `8` (all are `no_table` cases where body has no parseable size table and appears to rely on image/static content).

Why this addresses the report
- Fixes the regression where many products could not resolve to chart rows due broken parsing.
- Toggle now updates actual measurement numbers between metric/imperial where conversion data is available.
- Removes repeated unit text in both label/value rows; toggle is now the single source of unit context.

Validation snapshot
- Syntax check passed: `node --check assets/size-conversion.js`.
- Conversion behavior sanity-tested with representative values (`cm/in`, ranges, single-unit conversion) via Node script.
- CSV-wide scripted coverage audit completed (details above).
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on affected products to verify live rendering/toggle behavior in browser.
2) Decide handling for `no_table` products (8 handles): add machine-readable HTML tables or hide dynamic widget and show static fallback message/image intentionally.

Addendum: Value-level unit inference for mixed chart formats
Date: 2026-02-24
- `assets/size-conversion.js`
  - Added `inferUnitFromText()` fallback for products where units are embedded in value cells (e.g. `95 cm / 37.4 in`) but headers do not provide parseable unit metadata.
  - This allows toggle-driven selection/conversion to still work and strips trailing unit text from displayed numbers.

Patch: Local dev auth token expiration recovery
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-local-dev-auth-token-expiration-recovery

Changes applied (evidence-first)
- Diagnosed local preview auth failure at `http://127.0.0.1:9292`:
  - `curl` returned `401 Unauthorized` with `www-authenticate: Bearer ... error="Invalid token"` and body: `The access token provided is expired, revoked, malformed, or invalid for other reasons.`
- Confirmed stale long-running local dev process:
  - `ps aux` showed `shopify theme dev` process `PID 25223` running >100 minutes and listening on port `9292`.
- Recovered by restarting local dev runtime:
  - Stopped stale process (`kill 25223`).
  - Started fresh session: `shopify theme dev --store dresslikemommy-com.myshopify.com --host 127.0.0.1 --port 9292`.
  - Re-verified `http://127.0.0.1:9292` returns `200 OK`.

Why this addresses the issue
- The local proxy was serving with an invalid/expired bearer token from a stale `theme dev` runtime.
- Restarting `shopify theme dev` refreshed session auth and restored local access.

Open TODOs (next session)
1) If the same 401 token error recurs, fully reset CLI auth (`shopify auth logout` then `shopify auth login`) before restarting `shopify theme dev`.
2) Prefer restarting `shopify theme dev` when local preview appears blank or unauthorized after long idle periods.

Patch: PDP variant partial-selection label fix (color-first no longer shows unavailable)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-variant-partial-selection-choose-options

Changes applied (evidence-first)
- `assets/global.js`
  - Updated `VariantSelects.onVariantChange()` so when no matching variant is found, it distinguishes between:
    - incomplete option selection (e.g. `size` still blank), and
    - truly unavailable combination.
  - For incomplete selection, it now sets the submit button label to `window.variantStrings.chooseOptions` instead of `Unavailable`.
  - Updated `setUnavailable()` signature to accept an optional button label argument, defaulting to `window.variantStrings.unavailable` for existing behavior.
- `layout/theme.liquid`
  - Added `chooseOptions` to `window.variantStrings`:
    - `chooseOptions: {{ 'products.product.choose_options' | t }}`

Why this addresses the request
- Selecting color first while size is still unselected no longer shows `Unavailable` on the Add to cart button.
- The button now shows `Choose options` until all required options are selected.

Validation snapshot
- Syntax check passed: `node --check assets/global.js`.
- Verified diffs for `assets/global.js` and `layout/theme.liquid`.
- No browser manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA: select Color first with Size still blank; confirm button label is `Choose options` (not `Unavailable`).
2) Confirm actual unavailable combinations still show `Unavailable` as expected.

Patch: Mobile PDP sticky ATC requires explicit Size+Color and hides over media
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-mobile-sticky-atc-size-color-media-visibility-gate

Changes applied (evidence-first)
- `sections/main-product.liquid`
  - Extended sticky-mobile-ATC gating to require explicit shopper confirmation for both Size and Color/Colour option groups before sticky can become visible.
  - Added Color option parsing/state tracking (`isColorOptionGroup`, `getColorSelectionState`, `hasUserConfirmedColorSelection`) parallel to existing Size handling.
  - Updated visibility flow so sticky remains hidden whenever any required option is incomplete/unconfirmed (including non-size/color missing options), instead of showing a `Choose options` sticky state.
  - Added media viewport guard with IntersectionObserver on `#GalleryViewer-{{ section.id }}` / `#MediaGallery-{{ section.id }}` so sticky is hidden when main media is visible.
  - Kept existing IntersectionObserver on primary ATC and reinforced combined visibility condition:
    - mobile only,
    - primary ATC out of viewport,
    - main media out of viewport,
    - required selections complete/confirmed.
  - Hardened interactive option detection to ignore option groups hidden via CSS (`display: none` / `visibility: hidden`) so hidden single-value groups do not block sticky logic.

Why this addresses the request
- Sticky ATC no longer appears after selecting only Size; Color must also be explicitly selected.
- Sticky now appears only when shopper scrolls down and the original ATC is out of view, with both required selections complete.
- Scrolling back up to the main image hides sticky so it does not overlay media.
- Scrolling back up to where the original ATC is visible keeps sticky hidden.

Validation snapshot
- Verified patch via `git diff -- sections/main-product.liquid`.
- Reviewed updated sticky script flow with `nl -ba sections/main-product.liquid`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual mobile PDP QA: select Size only; confirm sticky stays hidden until Color is explicitly selected.
2) Manual mobile PDP QA: with Size+Color selected, scroll past primary ATC; confirm sticky appears only after ATC leaves viewport.
3) Manual mobile PDP QA: scroll back up to gallery and then to ATC area; confirm sticky hides in both states.

Patch: PDP desktop share button moved to media-overlay position
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-pdp-desktop-share-overlay-alignment

Changes applied (evidence-first)
- `snippets/product-media-gallery.liquid`
  - Removed `medium-hide large-up-hide` from the gallery share button so the same media-overlay share control renders on desktop as well as mobile.
- `layout/theme.liquid`
  - Hid the legacy in-info share block for PDP across breakpoints:
    - `.page-width--product-main .product__info-container > .share-button { display: none !important; }`
  - Promoted media share positioning styles to shared scope (not mobile-only), so the gallery share button stays in the same overlay position on desktop and mobile.
  - Kept a small desktop offset override (`top/right: 1rem`) and preserved copied-state styling.

Why this addresses the request
- Desktop now uses the same share button location pattern as mobile (overlay on product media).
- The previous share button location in the product info column is suppressed.

Validation snapshot
- Verified diffs for:
  - `snippets/product-media-gallery.liquid`
  - `layout/theme.liquid`
- No browser manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on desktop and mobile to confirm share button placement and click behavior (native share/copy fallback).
2) Confirm no unwanted overlap with gallery controls on desktop across common viewport widths.

Patch: Related products desktop carousel (3-up with centered cards)
Date: 2026-02-24
AGENT_CONTINUITY_ANCHOR: 2026-02-24-related-products-desktop-carousel-3-up-centered

Changes applied (evidence-first)
- `sections/related-products.liquid`
  - Added desktop carousel gating for recommendations overflow:
    - `show_desktop_slider = recommendations.products_count > 3`
  - Forced desktop carousel viewport to 3 cards when enabled:
    - `desktop_columns = 3`
  - Wrapped related products list in `slider-component` and enabled slider classes when needed:
    - mobile-only overflow keeps existing swipe behavior (`slider--mobile`)
    - when desktop carousel is enabled, small screens use `slider--tablet` while desktop uses `slider--desktop` so desktop arrows remain visible
  - Added desktop-only slider controls (prev/next + counter) with proper `aria-controls` and labels.
- `assets/section-related-products.css`
  - Added desktop centering rules so non-slider related-product cards are centered.
  - Added scoped desktop slider overrides for this section to remove inherited first-slide left offset and trailing spacer.
  - Added a scoped 3-up width rule for `.slider--desktop.grid--3-col-desktop` so three cards are centered and visible per viewport.

Why this addresses the request
- On desktop (`>=990px`), when “You may also like” has more than 3 products, it now behaves as a click-through carousel instead of wrapping products below.
- The carousel view is constrained to 3 cards and centered in the section.

Validation snapshot
- Verified diffs for:
  - `sections/related-products.liquid`
  - `assets/section-related-products.css`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP desktop QA: with 4+ recommendations, confirm only 3 cards are visible at once and next/prev buttons move through remaining products.
2) Manual PDP desktop QA: confirm recommendation cards are centered and do not show unintended left/right offsets.
3) Manual PDP mobile QA: confirm existing swipe behavior remains intact and no extra desktop controls appear.

Patch: Product size-chart range cleanup (single-value normalization in CSV exports)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-chart-range-single-value-normalization

Changes applied (evidence-first)
- Updated size-chart values in both CSV product exports:
  - `products_export_1 2_IMPORT_READY.csv`
  - `products_export_1 2.csv`
- Scope of edit was restricted to HTML table data cells (`<td>...</td>`) inside product body content.
- For any numeric range inside a `<td>` (e.g., `a-b`), replaced it with a single midpoint value.
  - Integer ranges were rounded to nearest whole number (half-up).
  - Decimal ranges were rounded to the same decimal precision used by the source values.
- Unit pair integrity was preserved by transforming each range in-place within its own unit string, e.g.:
  - `60-65 cm / 23.6-25.6 in` -> `63 cm / 24.6 in`
  - `5-7 kg / 11-15 lbs` -> `6 kg / 13 lbs`

Validation snapshot
- Programmatic scan after edit found no remaining numeric range patterns inside `<td>` cells in either file.
- Spot checks confirmed cleaned values stayed correctly aligned by unit (`cm` with `in`, `kg` with `lbs`).
- Git status shows only the two intended CSV files modified.

Open TODOs (next session)
1) If a different normalization preference is desired (e.g., lower bound instead of midpoint), rerun with updated rule.
2) Optional: manual merch review of a few high-traffic products to confirm display/readability preferences.

Patch: Size-chart values normalized to whole numbers (no decimals)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-chart-whole-number-normalization

Changes applied (evidence-first)
- Updated both CSV exports again:
  - `products_export_1 2_IMPORT_READY.csv`
  - `products_export_1 2.csv`
- Scope remained restricted to `<td>...</td>` table cell content.
- Converted all decimal numeric values inside table cells to whole numbers using half-up rounding.
  - Examples:
    - `63 cm / 24.6 in` -> `63 cm / 25 in`
    - `6 kg / 12.1 lbs` -> `6 kg / 12 lbs`

Validation snapshot
- Post-change scans found zero decimal values remaining inside `<td>` cells in both files.
- Spot checks confirm unit pairing remains intact (`cm` with `in`, `kg` with `lbs`).

Open TODOs (next session)
1) Optional merchandising pass to verify final rounded values read naturally for top products.

Patch: Follow-up cleanup for residual size ranges outside table cells
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-range-followup-body-html-measurements

Changes applied (evidence-first)
- Addressed remaining measurement ranges that were outside `<td>` values in product Body HTML content for:
  - `products_export_1 2_IMPORT_READY.csv`
  - `products_export_1 2.csv`
- Normalized additional patterns to single whole numbers (half-up), including:
  - unit-tail ranges: `84-102cm`, `0.5-1 in`, `130–160 cm`
  - dual-unit ranges: `80cm-95cm`
  - measurement-keyword ranges without explicit trailing unit: `Bust: 90-120`, `Waist: 80-104`

Validation snapshot
- No remaining unit-based measurement ranges detected (`cm/in/kg/lbs/lb/g/mm` patterns).
- No remaining keyword measurement ranges detected (`bust/waist/chest/hip/length/height/weight/...` with range form).
- No remaining numeric ranges in `<td>` chart cells in either file.

Open TODOs (next session)
1) If merch wants age ranges preserved/changed differently in descriptive copy, handle separately from measurement values.

Patch: PDP size-chart compact 2-row layout (header preserved)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-size-chart-compact-two-row-layout

Changes applied (evidence-first)
- Updated size-chart rendering in `assets/size-conversion.js`:
  - Kept the existing header markup (`.sc-header`, title, and unit toggle) intact.
  - Replaced stacked per-measurement rows with a compact 2-row matrix under the header:
    - row 1: measurement labels
    - row 2: measurement values
  - New output classes: `.sc-matrix`, `.sc-matrix__cell--label`, `.sc-matrix__cell--value`.
- Updated size-chart styles in `sections/main-product.liquid`:
  - Replaced `.sc-row*` presentation styles with compact matrix styles.
  - Tightened spacing and typography for mobile.
  - Added horizontal overflow handling on `.sc-table` so columns remain readable on small screens.
  - Preserved existing header styling and behavior.

Validation snapshot
- `node --check assets/size-conversion.js` passed (no syntax errors).
- Diff review confirms edits are scoped to:
  - `assets/size-conversion.js`
  - `sections/main-product.liquid`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA on mobile and desktop: confirm two-row layout readability across products with many measurement columns.
2) Validate long label behavior (e.g., "Upper Bust") and tune min column width if merchandising wants less horizontal scroll.

Patch: Size-chart long-label compaction for mobile readability
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-chart-label-compaction

Changes applied (evidence-first)
- Updated `assets/size-conversion.js` to compact long measurement labels at render time:
  - Exact replacements:
    - `Recommended Height` -> `Rec. Height`
    - `Recommended Weight` -> `Rec. Weight`
  - Generic fallback:
    - Any label starting with `Recommended` now renders as `Rec. ...`
- Implemented helper: `getCompactMeasurementLabel(label)` and applied it when building size-chart matrix labels.
- Source size-table/header data remains unchanged; this is display-only in the PDP size-chart UI.

Validation snapshot
- `node --check assets/size-conversion.js` passed (no syntax errors).
- Verified helper usage in matrix label rendering path.

Open TODOs (next session)
1) Manual PDP QA: confirm compact labels are readable across products with recommendation columns.
2) If desired, add more explicit short forms (e.g., `Rec. Chest`, `Rec. Hips`) via the same map.

Patch: Size-chart label copy tweak (`Recommended Height/Weight` -> `Height/Weight`)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-chart-height-weight-label-copy

Changes applied (evidence-first)
- Updated display label mapping in `assets/size-conversion.js` (`getCompactMeasurementLabel`):
  - `Recommended Height` now renders as `Height`
  - `Recommended Weight` now renders as `Weight`
- Removed the generic `Recommended -> Rec.` fallback, so only the two explicit labels are altered.
- Data source and table headers remain unchanged; this is render-time UI text only.

Validation snapshot
- `node --check assets/size-conversion.js` passed (no syntax errors).
- Verified mapping targets in file search output.

Open TODOs (next session)
1) Manual PDP QA to confirm these labels appear as expected on products that include recommendation fields.

Patch: Removed "and below" from size-chart measurement values
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-remove-and-below-measurements

Changes applied (evidence-first)
- Updated CSV exports used for GPT/backfill content:
  - `GPT/products_export_1.csv`
  - `GPT/products_export_1_backfill.csv`
- Removed trailing phrase `and below` from measurement cell values.
  - Examples:
    - `130 cm and below` -> `130 cm`
    - `50 kg / 100 lbs and below` -> `50 kg / 100 lbs`

Validation snapshot
- Repository scan for `and below` now returns no matches.
- Spot checks around edited size-chart blocks confirm expected output format.

Open TODOs (next session)
1) If this wording should also be removed in external copies not tracked here (Shopify admin content), apply the same cleanup there.

Patch: Remove `and below` in active exports + show weight units in size-chart UI
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-size-chart-weight-units-and-below-cleanup

Changes applied (evidence-first)
- Updated active product export CSVs:
  - `products_export_1 2.csv`
  - `products_export_1 2_IMPORT_READY.csv`
- Removed trailing `and below` phrases from measurement values.
  - Examples:
    - `130 cm and below` -> `130 cm`
    - `50 kg / 100 lbs and below` -> `50 kg / 100 lbs`
- Updated `assets/size-conversion.js` rendering behavior:
  - Sanitizes any residual `and below` text at runtime before parsing (`getMeasurementForUnitSystem`).
  - For measurement labels containing `weight`, appends explicit unit in value pills:
    - metric -> `kg`
    - imperial -> `lbs`
  - Keeps header unit toggle labels (`cm` / `in`) unchanged.

Validation snapshot
- `node --check assets/size-conversion.js` passed.
- `rg` scan confirms no `and below` remains in:
  - `products_export_1 2.csv`
  - `products_export_1 2_IMPORT_READY.csv`

Open TODOs (next session)
1) Manual PDP QA: verify weight pills display as `XX kg` / `YY lbs` when toggling units.
2) If needed, mirror this cleanup in any external/off-repo CSV snapshots.

Patch: PDP related-products desktop carousel controls visibility
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-related-products-desktop-carousel-controls

Changes applied (evidence-first)
- Updated `sections/related-products.liquid`:
  - Added a scoped class on the slider wrapper: `related-products__slider`.
  - Replaced desktop control wrapper classes from `slider-buttons small-hide medium-hide` to `slider-buttons related-products__slider-buttons`.
- Updated `assets/section-related-products.css`:
  - Added section-scoped controls visibility rules so the related-products slider controls are hidden below desktop and explicitly shown on desktop (`>= 990px`).
  - Added explicit desktop button styling (size, border, background, icon dimensions) to ensure next/prev arrows are visually obvious and clickable.

Validation snapshot
- Diff review confirms edits are scoped to:
  - `sections/related-products.liquid`
  - `assets/section-related-products.css`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP desktop QA: confirm “You may also like” shows visible prev/next arrows and they move slides.
2) Manual PDP mobile/tablet QA: confirm controls remain hidden and swipe behavior is unchanged.

Patch: Added desktop stepper to PDP related-products carousel
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-related-products-desktop-stepper-added

Changes applied (evidence-first)
- Updated `sections/related-products.liquid` desktop controls:
  - Converted the counter block to a stepper-compatible counter using `slider-counter--product-stepper`.
  - Added `slider-counter__separator` class and initialized `--step-progress` inline style.
- Updated `assets/section-related-products.css` desktop controls:
  - Added scoped stepper UI styles (track + fill progress bar) for `.related-products__slider-buttons .slider-counter--product-stepper`.
  - Kept existing desktop arrow controls visible and styled.

Validation snapshot
- Diff review confirms edits are scoped to:
  - `sections/related-products.liquid`
  - `assets/section-related-products.css`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP desktop QA: verify stepper appears between arrows and progress fill updates when sliding.
2) Manual PDP desktop QA: verify counter values map to slide pages (not raw product count) during navigation.

Patch: Desktop related-products arrows moved onto carousel image area
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-related-products-overlay-arrows-on-track

Changes applied (evidence-first)
- Updated `sections/related-products.liquid` structure:
  - Added `.related-products__slider-track` wrapper around the recommendations `<ul>`.
  - Moved desktop prev/next buttons into `.related-products__slider-arrows` inside that track wrapper.
  - Kept the stepper counter (`.related-products__slider-stepper`) below the track.
- Updated `assets/section-related-products.css`:
  - Added desktop overlay positioning for `.related-products__slider-arrows` so arrows render on top of the carousel image area.
  - Right/left arrows are now positioned over the track edges and remain clickable via `pointer-events` handling.
  - Preserved and scoped stepper styling under the track.

Validation snapshot
- Diff review confirms edits are scoped to:
  - `sections/related-products.liquid`
  - `assets/section-related-products.css`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP desktop QA: verify right arrow is visible over the carousel image area and advances slides.
2) Manual PDP desktop QA: verify left arrow appears after first advance and both arrows remain clickable.
3) Manual PDP responsive QA: verify mobile/tablet behavior remains unchanged.

Patch: PDP desktop hero image emphasis (larger media first impression)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-desktop-hero-image-emphasis

Changes applied (evidence-first)
- Updated `assets/section-main-product.css` desktop layout rebalance rules:
  - Increased desktop PDP container width at `>= 990px`, `>= 1400px`, and `>= 1600px` breakpoints.
  - Shifted product grid split to prioritize media on desktop for all configured media sizes:
    - `>= 990px`: media/info `66/34`
    - `>= 1400px`: media/info `67/33`
    - `>= 1600px`: media/info `68/32`
  - Reduced desktop info-column horizontal padding so media can occupy more of first-view horizontal space.
  - Set desktop product row alignment to `align-items: flex-start` for a stronger top-aligned first impression.
- Tightened breadcrumb vertical spacing in the same file so the main image starts visually closer to breadcrumb area on load.

Validation snapshot
- `git diff --check -- assets/section-main-product.css` passed (no whitespace errors).
- Changes are scoped to `assets/section-main-product.css` only for this patch.

Open TODOs (next session)
1) Manual desktop PDP QA (>=990px): confirm the first media appears larger and starts close to breadcrumb area across representative products.
2) Manual QA for `product--right` and alternate `media_size` settings to confirm info column spacing remains intentional.

Patch: PDP desktop main image enlarged further (remove viewport cap + stronger media split)
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-desktop-main-image-larger-v2

Changes applied (evidence-first)
- Updated `assets/section-main-product.css` desktop layout split to further prioritize media:
  - `>= 990px`: media/info `70/30`
  - `>= 1400px`: media/info `71/29`
  - `>= 1600px`: media/info `72/28`
- Added a desktop-only override for constrained media containers so the main image is no longer capped by viewport-fit height logic:
  - Kept container width at full width.
  - Forced constrained media padding back to natural ratio (`var(--ratio-percent)`) on desktop.

Validation snapshot
- Diff review confirms edits are scoped to `assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual desktop PDP QA: verify the hero image now matches the intended large visual weight relative to “You may also like”.
2) If still too small for portrait assets, consider switching `main-product` setting `constrain_to_viewport` to `false` in the theme editor or template config.

Patch: PDP first image now matches collection featured image source
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-initial-image-match-collection-featured

Changes applied (evidence-first)
- Updated `snippets/product-media-gallery.liquid`:
  - Initial featured media on load now resolves from `product.featured_media` (same source used by collection product cards), with fallback to `product.selected_or_first_available_variant.featured_media`.
  - Gallery first active slide, duplicate-skip logic, and thumbnail `aria-current` logic now use the new `featured_media` variable consistently.
- Updated `snippets/product-media-modal.liquid`:
  - Modal media ordering now uses the same `product.featured_media`-first logic for consistency with the gallery.

Validation snapshot
- Diff review confirms scope is limited to:
  - `snippets/product-media-gallery.liquid`
  - `snippets/product-media-modal.liquid`
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual PDP QA: confirm first image on product page matches collection card image for products with variant-specific media.
2) Manual variant-change QA: confirm selecting a variant still switches to that variant’s image after page load.

Patch: PDP desktop hero image reduced by ~10% on request
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-hero-size-minus-10-percent

Changes applied (evidence-first)
- Updated `assets/section-main-product.css` desktop media/info column split to reduce hero image footprint by ~10% from the prior setting:
  - `>= 990px`: `70/30` -> `63/37`
  - `>= 1400px`: `71/29` -> `64/36`
  - `>= 1600px`: `72/28` -> `65/35`
- Kept the previously applied initial image source behavior (`product.featured_media` first) unchanged.

Validation snapshot
- Diff review confirms this patch only adjusts desktop width split variables in `assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual desktop PDP QA: confirm the hero image now feels correctly sized after the 10% reduction.

Patch: PDP desktop hero image reduced by another ~10% on request
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-hero-size-minus-10-percent-v2

Changes applied (evidence-first)
- Updated `assets/section-main-product.css` desktop media/info split to reduce hero image footprint another ~10% from the prior setting:
  - `>= 990px`: `63/37` -> `56/44`
  - `>= 1400px`: `64/36` -> `57/43`
  - `>= 1600px`: `65/35` -> `58/42`
- Kept initial image source behavior unchanged (`product.featured_media` first).

Validation snapshot
- Diff review confirms this patch only adjusts desktop width split variables in `assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual desktop PDP QA: confirm this second 10% reduction matches the desired visual balance.

Patch: PDP desktop hero image reduced by another ~5% on request
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-pdp-hero-size-minus-5-percent-v3

Changes applied (evidence-first)
- Updated `assets/section-main-product.css` desktop media/info split to reduce hero image footprint by another ~5% from the prior setting:
  - `>= 990px`: `56/44` -> `53/47`
  - `>= 1400px`: `57/43` -> `54/46`
  - `>= 1600px`: `58/42` -> `55/45`
- Kept initial image source behavior unchanged (`product.featured_media` first).

Validation snapshot
- Diff review confirms this patch only adjusts desktop width split variables in `assets/section-main-product.css`.
- No browser/device manual QA was run in this session.

Open TODOs (next session)
1) Manual desktop PDP QA: confirm this 5% reduction matches the desired visual balance.
