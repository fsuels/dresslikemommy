
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
