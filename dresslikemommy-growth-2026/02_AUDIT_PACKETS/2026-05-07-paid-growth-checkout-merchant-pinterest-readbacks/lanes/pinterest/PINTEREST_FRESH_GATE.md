# Pinterest Fresh Read-Only Gate

Generated: 2026-05-07 23:30 EDT / 2026-05-08 03:30 UTC

Lane: Pinterest fresh read-only gate.

Scope: read-only Pinterest Ads/Catalog/CDP readback only. No Pinterest campaign, draft, product group, catalog, pixel, tag, CAPI, audience, budget, bid, or spend write was made. No Shopify, Merchant Center, Google Ads, feed, product-data, shipping, payment, or order write was made.

## Decision

`PINTEREST_US_DRAFTS_REMAIN_BLOCKED_PENDING_FULL_ITEM_PROOF_EVENT_QUALITY_ACCEPTANCE_AND_EXPLICIT_APPROVAL`

The logged-in Pinterest browser/CDP path is available and current account surfaces are readable. The account still shows `0 campaigns`, `0 currently being served`, and `$0.00` spend. Event receipt is healthy enough to see standard ecommerce events from `Api + Tag`, including Checkout and AddPaymentInfo after the Shopify app pixel repair, but Event Quality itself is still `Fair` and last updated `5/6/2026`.

The EN Shopify catalog source is current to May 7 and completed with `0` failed uploads, but it still has warnings. Current item-level access is partially proven: a fresh bounded 9-row candidate sample returned `6/9` EN-US in-stock matches through the Pinterest catalog API. That is useful freshness proof, but not enough to create or approve Pinterest drafts; the full `346` historical candidate rows still need a complete current proof pass.

## Account And Access

- CDP profile: `127.0.0.1:9333`, existing Pinterest background Chrome session.
- Advertiser: `549756244483`.
- Account/domain visible in UI: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- No visible login, CAPTCHA, unsaved-change, billing, permission, or account-switch blocker appeared in captured page text.
- Invisible reCAPTCHA iframes were present in the page list as normal Pinterest assets, but no visible CAPTCHA blocker appeared in the readback text.

## Campaign / Spend Baseline

Artifact: `raw/campaign_spend_baseline.txt` and `.png`.

- Date range: Last 30 days, final URL resolved to `start_date=2026-04-08` and `end_date=2026-05-07`.
- Filters included running, paused, not started, completed, and advertiser-disabled entities.
- Campaigns: `0 campaigns`.
- Serving: `0 currently being served`.
- Spend: `$0.00`.
- Results: `0`.
- Impressions: `0`.
- Pin clicks: `0`.
- CPC: `$0.00`.

## Event Quality

Artifact: `raw/event_quality.txt` and `.png`.

- Event Quality score: `Fair`.
- Updated: `5/6/2026`.
- Source path: `Conversions API` and `Pinterest Tag`.
- Date range options visible: `Last 14 days` and `Last 1 day`.
- Top visible action items:
  - `Product ID` in `Add Payment Info`.
  - `Email` in `Add to Cart`.
  - `Click ID` in `Checkout`.
- Additional Event Insights gap: `Order Value` in `Add Payment Info`.
- Duplicate-event health: `Event ID` visible in good health for `Page Visit` and `View Category`.

## Events Overview

Artifact: `raw/events_overview.txt` and `.png`.

| Event | Source | Total events | Last received |
|---|---|---:|---|
| PageVisit | `Api · Tag` | `19,913` | `5/7/2026 06:38pm (UTC)` |
| ViewCategory | `Api · Tag` | `4,224` | `5/7/2026 03:18pm (UTC)` |
| AddToCart | `Api · Tag` | `703` | `5/7/2026 02:29pm (UTC)` |
| InitiateCheckout | `Api · Tag` | `124` | `5/7/2026 01:21pm (UTC)` |
| Search | `Api · Tag` | `40` | `5/2/2026 07:07am (UTC)` |
| Checkout | `Api · Tag` | `25` | `5/7/2026 01:22pm (UTC)` |
| AddPaymentInfo | `Api · Tag` | `24` | `5/7/2026 01:22pm (UTC)` |

Interpretation: checkout-stage events are still arriving after the Shopify Customer Events Pinterest pixel repair, but the health score has not refreshed beyond `Fair`.

## Catalog Source

Artifacts: `raw/catalog_data_sources.txt`, `raw/catalog_en_source_detail.txt`, `raw/catalog_en_ingestion_issues.txt`, and screenshots.

- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- EN Shopify source: `3041760867124595727`.
- Country/language: United States / `en`.
- Source label: Shopify.
- Current ingestion: `May 7 at 1:14 PM EDT`.
- Current ingestion state: `Completed`.
- Product count: `5,663`.
- Successful uploads: `5,663 of 5,663`.
- Failed uploads: `0`.
- Warning count in source history: `152`.
- Visible ingestion issue: `Warning 1039`, `description_html` too long, with `304` occurrences in the issue table.

Visible EN product groups include `All Products`, `Top Sellers`, `Midi Dresses`, `Dresses`, `Tops`, `Best Deals`, `New Arrivals`, `Back In Stock`, `Matching Hawaiian Outfits for Family`, and other Shopify collection groups. `Promote` controls were visible; none were clicked.

## Failed / Localized Sources

Artifact: `raw/catalog_data_sources.txt`.

- Separate sitemap data source `3041760916127467912` still showed `Failed`, latest ingestion `May 7 at 3:31 AM EDT`, source `URL sitemap_collections_1.xml`, United States / English (US).
- Localized Shopify sources still showed visible non-clean paired counts in the Status column:
  - `cs`: `5,577` / `86`, latest `May 7 at 2:48 AM EDT`.
  - `Deutsch`: `5,611` / `52`, latest `May 7 at 12:14 AM EDT`.
  - `ro`: `5,645` / `18`, latest `May 7 at 3:13 AM EDT`.
  - `hi`: `5,661` / `2`, latest `May 6 at 6:12 PM EDT`.
- Other visible localized feeds mostly showed `5,663`; `pl` showed `5,664`.

Interpretation: the EN Shopify source is the only Pinterest catalog source close enough for a US-only draft gate. The failed sitemap and localized feed warnings/failures remain blockers for Pinterest international catalog expansion.

## Item-Level Proof

Artifacts: `raw/item_level_probe_summary.json`, `raw/item_level_probe_rows.csv`, and `raw/item_level_probe_api_sanitized.json`.

Fresh read-only API sample:

- Historical candidate rows available: `346`.
- Rows sampled: `9`, stratified across `family_matching`, `mommy_me`, and `pajamas`.
- Pinterest pin IDs returned by the filter API: `171`.
- Metadata rows returned: `101`.
- EN-US rows returned: `6`.
- EN-US in-stock matches: `6/9`.

By group:

| Group | Sampled | EN-US in-stock found | Not found |
|---|---:|---:|---:|
| family_matching | `3` | `2` | `1` |
| mommy_me | `3` | `2` | `1` |
| pajamas | `3` | `2` | `1` |

Interpretation: item-level API access is alive, but the current proof is partial. The full `346` candidate rows must be refreshed before any product-group or campaign draft build.

## Blockers

- Event Quality remains `Fair` and still calls out Product ID, Email, Click ID, and AddPaymentInfo Order Value gaps.
- No real Pinterest ad-click traffic is serving, so true Click ID coverage cannot be proven yet.
- Full current EN-US item-level proof is not complete; the bounded sample found `3/9` sampled rows missing from the EN-US in-stock result.
- Separate sitemap source still reads `Failed`.
- Localized Pinterest sources still show warning/fail counts; do not use them for international Pinterest testing yet.
- Pinterest draft creation still needs exact owner action-time approval.

## Guardrails Preserved

- No Pinterest campaigns, drafts, product groups, catalogs, audiences, budgets, bids, pixels, tags, CAPI, or spend were created or edited.
- No Shopify, Merchant Center, Google Ads, feed, product-data, shipping-rate, Market, payment, or order action was taken.
- No duplicate theme-level Pinterest tag or custom CAPI path was added.
- No physical-store, warehouse, owned-inventory, or guaranteed-stock claim was introduced.

## Raw Artifacts

Key artifacts under `raw/`:

- `campaign_spend_baseline.txt`, `.json`, `.png`, `_network.json`
- `event_quality.txt`, `.json`, `.png`, `_network.json`
- `events_overview.txt`, `.json`, `.png`
- `catalog_data_sources.txt`, `.json`, `.png`
- `catalog_en_source_detail.txt`, `.json`, `.png`
- `catalog_en_ingestion_issues.txt`, `.json`, `.png`
- `catalog_product_groups_en.txt`, `.json`, `.png`
- `item_level_probe_summary.json`
- `item_level_probe_rows.csv`
- `item_level_probe_api_sanitized.json`
- `cdp_capture_summary.json`
- `existing_pages_capture_summary.json`

Note: the first full CDP run captured account pages successfully, the second run completed the item probe but some new-tab React pages returned zero-length text. `existing_pages_capture_summary.json` and the refreshed `.txt`/`.png` files from already-open Pinterest tabs supersede those zero-length new-tab entries.

## Commands Run

- `sed -n` reads of required repo memory, lane board, and prior Pinterest evidence.
- `rg` searches for Pinterest continuity, reports, and prior artifacts.
- `curl http://127.0.0.1:9333/json/version` and `/json/list` to verify CDP access.
- `node lanes/pinterest/pinterest_cdp_readback.mjs` with `PINTEREST_ITEM_LIMIT=45`, then with `PINTEREST_ITEM_LIMIT=9`.
- `node lanes/pinterest/pinterest_cdp_readback.mjs` with `PINTEREST_EXISTING_ONLY=1`.
- `pgrep -fl 'pinterest_cdp_readback.mjs'` to confirm no lane script remained running.

## Next Safe Action

Keep Pinterest drafts and spend parked. Next safe read-only step is a full current item-level proof pass for all `346` intended US candidate rows, then decide whether the owner wants to explicitly accept the remaining `Fair` Event Quality gaps for a paused US-only draft build. Any draft/build still requires the exact paused-Pinterest approval gate and must remain no-spend until a separate launch approval.
