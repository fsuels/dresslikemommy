# Pinterest Currency/Presentment Monitor

Generated: 2026-05-08 00:04 EDT / 2026-05-08 04:04 UTC

Lane: Pinterest read-only monitoring gate for the paid-growth currency/presentment sprint.

Scope: read-only Pinterest Ads/Catalog/CDP monitoring only. No Pinterest campaign, draft, product group, catalog, pixel, tag, CAPI, audience, budget, bid, or spend write was made. No Shopify, Merchant Center, Google Ads, feed, product-data, shipping, payment, or order write was made.

## Decision

`PINTEREST_US_DRAFTS_STILL_BLOCKED_BUT_ITEM_PROOF_NOW_MOSTLY_CURRENT`

The logged-in Pinterest CDP/browser path was available. Account, campaign, Event Quality, Events Overview, catalog source, failed sitemap source, EN ingestion issues, product groups, and item metadata were readable without visible login, CAPTCHA, unsaved-change, billing, permission, or account-switch blockers.

The biggest improvement is item-level proof: the full 346-row historical US Pinterest candidate set was refreshed by pin metadata. Current readback found `337/346` rows as EN-US `IN_STOCK` in Pinterest metadata. The 9 missing rows are all from one Mommy & Me product (`7229026304097`). This is much stronger than the prior 9-row sample, but not launch-clean because Event Quality remains `Fair`, the EN Shopify source still has warning `1039`, the separate sitemap source still fails, and 9 intended rows no longer resolve by the historical Pinterest pin IDs.

## Account / Access

- CDP profile: `127.0.0.1:9333`, existing logged-in Chrome session.
- Advertiser: `549756244483`.
- Account/domain visible in UI: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- Merchant ID used by prior CDP helper: `3041760832963738705`.
- EN Shopify source/feed profile: `3041760867124595727`.
- Failed sitemap source: `3041760916127467912`.

## Campaign / Spend Baseline

Artifact: `raw/campaign_spend_baseline.txt`, `.json`, `.png`, `_network.json`.

- Date range resolved to `2026-04-08` through `2026-05-07`.
- Campaign filters included running, paused, not started, completed, and advertiser-disabled entities.
- Campaigns: `0 campaigns`.
- Serving: `0 currently being served`.
- Spend: `$0.00`.
- Results: `0`.
- Impressions: `0`.
- Pin clicks: `0`.
- CPC: `$0.00`.

## Event Quality

Artifact: `raw/event_quality.txt`, `.json`, `.png`, `_network.json`.

- Event Quality score: `Fair`.
- Updated: `5/6/2026`.
- Event sources: `Conversions API` and `Pinterest Tag`.
- Date range options visible: `Last 14 days` and `Last 1 day`.
- Top action items:
  - `Product ID` in `Add Payment Info`.
  - `Email` in `Add to Cart`.
  - `Click ID` in `Checkout`.
- Additional Event Insights gap: `Order Value` in `Add Payment Info`.
- Duplicate event health: `Event ID` appears in good health for `Page Visit` and `View Category`.

## Events Overview

Artifact: `raw/events_overview.txt`, `.json`, `.png`, `_network.json`.

| Event | Source | Total events | Last received |
|---|---|---:|---|
| PageVisit | `Api - Tag` | `19,694` | `5/8/2026 01:55am (UTC)` |
| ViewCategory | `Api - Tag` | `4,180` | `5/8/2026 01:55am (UTC)` |
| AddToCart | `Api - Tag` | `702` | `5/8/2026 12:23am (UTC)` |
| InitiateCheckout | `Api - Tag` | `122` | `5/7/2026 01:21pm (UTC)` |
| Search | `Api - Tag` | `51` | `5/7/2026 11:37pm (UTC)` |
| Checkout | `Api - Tag` | `25` | `5/7/2026 01:22pm (UTC)` |
| AddPaymentInfo | `Api - Tag` | `24` | `5/7/2026 01:22pm (UTC)` |

Interpretation: standard ecommerce events are still arriving from both API and Tag. PageVisit, ViewCategory, AddToCart, and Search refreshed after the prior readback; Checkout and AddPaymentInfo remain last received on `2026-05-07 13:22 UTC`.

## Catalog Source

Artifacts: `raw/catalog_data_sources.txt`, `raw/catalog_en_source_detail.txt`, `raw/catalog_en_ingestion_issues.txt`, and screenshots.

- EN Shopify source/feed profile: `3041760867124595727`.
- Country/language: United States / `en`.
- Source label visible in data-source list: Shopify.
- Source detail labels source as `URL` with `Data source URL: Shopify`.
- Current ingestion: `May 7 at 1:14 PM EDT`.
- Current ingestion state: `Completed`.
- Product count: `5,663`.
- Successful uploads: `5,663 of 5,663`.
- Failed uploads: `0`.
- Warnings: `152`.
- Latest ingestion issue text: `Warning 1039`, `description_html` too long; Pinterest says affected items publish without `description_html`.
- Occurrences visible in issue table: `304`.

## Failed / Localized Sources

Artifact: `raw/catalog_data_sources.txt`, `raw/catalog_failed_sitemap_detail.txt`.

- Separate sitemap source `3041760916127467912` still failed repeatedly.
- Sitemap source URL: `https://www.dresslikemommy.com/sitemap_collections_1.xml`.
- Latest failed ingestion: `May 7 at 3:31 AM EDT`.
- The failed sitemap history shows repeated failures from `Apr 28` through `May 7`, with `0` successful uploads, `0` failed uploads, and `0` warnings in the visible rows.
- Localized Shopify feeds still have visible non-clean counts:
  - `cs`: `5,577 / 86`, latest `May 7 at 2:48 AM EDT`.
  - `Deutsch`: `5,611 / 52`, latest `May 7 at 12:14 AM EDT`.
  - `Italiano`: `5,639 / 24`, latest `May 7 at 2:48 PM EDT`.
  - `ro`: `5,645 / 18`, latest `May 7 at 3:13 AM EDT`.
  - `Português (Brasil)`: `5,661 / 2`, latest `May 7 at 7:39 PM EDT`.

Interpretation: Pinterest international catalog expansion remains blocked. The EN Shopify source is still the only source close enough for a US-only paused draft gate.

## Product Groups

Artifact: `raw/catalog_product_groups_en.txt`, `.json`, `.png`.

Visible EN product groups include:

- `All Products` / `4672936303140` / `5,642` products.
- `Top Sellers` / `4673002049172` / `77` products.
- `Midi Dresses` / `4672936327429` / `226` products.
- `Dresses` / `4672936327418` / `674` products.
- `Tops` / `4672936327411` / `7` products.
- `Best Deals` / `4672936326030` / `1,051` products.
- `New Arrivals` / `4672936512464` / `100` products.
- `Back In Stock` / `4673004141096` / `3` products.
- `Matching Hawaiian Outfits for Family` / `4673008695670` / `192` products.

`Promote` controls were visible. None were clicked.

## Full Item-Level Proof

Artifacts: `raw/full_item_metadata_summary.json`, `raw/full_item_metadata_rows.csv`, `raw/full_item_metadata_api_sanitized.json`.

Method: read-only CDP metadata refresh by the 346 historical Pinterest EN-US pin IDs from `2026-04-29-pinterest-shopping-ads-gate/pinterest_paid_ready_candidate_offer_rows.csv`. This avoids creating product groups or drafts and avoids the heavier product filter path that timed out.

- Candidate rows checked: `346`.
- Unique historical Pinterest pin IDs requested: `346`.
- Metadata request count: `35`.
- Metadata rows returned: `337`.
- EN-US rows returned: `337`.
- Matched EN-US `IN_STOCK`: `337`.
- Unmatched rows: `9`.
- Other/non-in-stock matched rows: `0`.

By group:

| Group | Requested | Found EN-US in stock | Not found | Other |
|---|---:|---:|---:|---:|
| family_matching | `103` | `103` | `0` | `0` |
| mommy_me | `214` | `205` | `9` | `0` |
| pajamas | `29` | `29` | `0` | `0` |

The 9 missing rows are all Mommy & Me variants for Shopify product `7229026304097`, titled in the candidate CSV as `Elegant Floral Off-Shoulder Dress Set Perfect for S... | DLM`.

Missing variant IDs:

- `41878208249953`
- `41878208282721`
- `41878208315489`
- `41878208446561`
- `41878208479329`
- `41878208512097`
- `41878208577633`
- `41878208610401`
- `41878208643169`

Interpretation: a US-only Pinterest candidate scope could be rebuilt around the `337` refreshed EN-US in-stock rows, but the 9 missing rows should be excluded or re-resolved before any paused draft/product-group build.

## Blockers

- Event Quality remains `Fair`, updated `5/6/2026`, with unresolved Product ID, Email, Click ID, and AddPaymentInfo Order Value gaps.
- No real Pinterest ad-click traffic is serving, so real Click ID coverage cannot be fully proven.
- EN Shopify source still has `152` warnings; latest visible issue is `Warning 1039` for long `description_html`, `304` occurrences.
- The separate sitemap source `3041760916127467912` still fails.
- Localized Shopify sources still show warning/fail counts, so Pinterest international expansion is not ready.
- Full item proof is mostly current but not perfect: `9/346` historical candidate rows no longer resolve by the historical pin IDs.
- Pinterest draft/campaign/product-group creation still requires exact owner action-time approval.

## Guardrails Preserved

- No Pinterest campaigns, drafts, product groups, catalogs, audiences, budgets, bids, pixels, tags, CAPI paths, or spend were created or edited.
- No Shopify Admin, theme, product, feed, shipping-rate, Market, payment, or order action was taken.
- No Merchant Center, Google Ads, GA4/GTM, Standard Shopping, PMax, Remarketing, conversion-goal, product-scope, product-group, or feed-label action was taken.
- No duplicate theme-level Pinterest tag or custom CAPI path was added.
- No physical-store, warehouse, owned-inventory, local-inventory, or guaranteed-stock claim was introduced.

## Commands / Tools Run

- `sed -n` reads of `AGENTS.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, latest `ops/AGENT_WORKLOG.md`, and prior Pinterest packets.
- `rg --files` / `find` to locate Pinterest reports, scripts, and lane folders.
- `curl http://127.0.0.1:9333/json/version` and `/json/list` to verify local CDP browser access.
- `PINTEREST_EXISTING_ONLY=1 node .../pinterest_cdp_readback.mjs` to refresh already-open Pinterest tab text/screenshots under this lane.
- `PINTEREST_ITEM_LIMIT=346 ... node .../pinterest_cdp_readback.mjs` for full account/catalog capture; account/catalog pages succeeded, the original item filter probe timed out.
- `node .../pinterest_full_item_metadata_readback.mjs` for optimized full 346-row pin metadata proof.
- `jq`, `python3` CSV parsing, `pgrep`, and `kill` for verification and cleanup of the completed Node helper process.
- `date` and `git status --short` for timestamp and dirty-worktree awareness.

## Residual Risk

- The optimized item proof validates historical Pinterest pin metadata, not a newly created product group. It is suitable for a read-only gate, but a future build should still read back the exact rows to be included immediately before saving any paused draft.
- The 9 missing rows may be deleted/changed pins, stale pin IDs, or catalog churn. They should not be assumed eligible.
- Currency/presentment blockers from the checkout lane are outside this Pinterest lane; this report does not clear international spend.
- Existing repo files outside this lane were already dirty (`AGENTS.md`, `ops/AGENT_COORDINATION.md`, `ops/AGENT_WORKLOG.md`) and were not touched by this subagent.

## Next Safe Action

Keep Pinterest drafts and spend parked. For a future paused US-only Pinterest draft gate, use only the `337` refreshed EN-US in-stock rows or first re-resolve/exclude the 9 missing Mommy & Me variants, then ask the owner for exact paused-draft approval. Do not use localized Pinterest feeds for international expansion until their warning/fail counts and the broader currency/presentment gates are clean.
