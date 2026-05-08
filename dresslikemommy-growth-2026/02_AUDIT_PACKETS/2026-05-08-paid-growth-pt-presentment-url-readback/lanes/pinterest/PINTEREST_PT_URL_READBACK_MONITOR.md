# Pinterest PT/URL Readback Monitor

Generated: 2026-05-08 01:01 EDT / 2026-05-08 05:01 UTC

Lane: Pinterest read-only monitoring sidecar for the PT checkout / market-localized URL sprint.

Scope: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/pinterest/` only.

## Decision

`PINTEREST_DRAFTS_AND_SPEND_STILL_PARKED`

Pinterest remains usable for read-only monitoring, and the campaign/spend baseline plus item-level proof were refreshed safely. Event Quality is still `Fair`, with the same launch-relevant gaps around Click ID, Product ID, and Email. The EN Shopify catalog source remains the only plausible Pinterest paid-catalog base, but it still has warnings and the separate sitemap source remains failed. Pinterest international/catalog expansion is not ready.

No Pinterest campaign, draft, product group, audience, catalog, pixel, tag, CAPI, budget, bid, or spend write was made.

## Access / Identity

- Browser/session label used for this lane: `DLM-PINTEREST-EventCatalog-PT-URL-20260508`.
- CDP browser: `127.0.0.1:9333`, existing logged-in Chrome profile.
- Advertiser: `549756244483`.
- Visible account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- Merchant ID used by helper: `3041760832963738705`.
- EN Shopify source/feed profile: `3041760867124595727`.
- Failed sitemap source: `3041760916127467912`.

No login, CAPTCHA, account-switcher, billing prompt, permission prompt, or unsaved-change prompt appeared in the successful captures. Fresh new-tab Pinterest Ads/Catalog page loads did return blank DOM text for several pages, so I parked those visual readbacks and used safe API responses plus existing logged-in catalog tabs where available.

## Campaign / Spend Baseline

Artifact: `raw/campaign_spend_baseline.txt`, `.json`, `.png`, `_network.json`.

- Date range visible in URL: `2026-04-08` through `2026-05-07`.
- Campaigns: `0 campaigns`.
- Serving: `0 currently being served`.
- Spend: `$0.00`.
- Results: `0`.
- Impressions: `0`.
- Pin clicks: `0`.
- CPC: `$0.00`.

## Event Quality

Artifacts: `raw/event_quality_api_probe.json`, `raw/event_quality_api_probe.png`, `raw/event_quality_api_probe.txt`, plus the blank-DOM page artifacts `raw/event_quality.*`.

The fresh Event Quality visual page loaded as a blank Pinterest Ads shell (`bodyTextLength=0`), but the page made successful read-only conversions API calls. The API probe stored response bodies only; no headers or cookies were stored.

Fresh API readback:

- Overall WEB status: `Fair` for both `TAG` and `CONVERSIONS_API`.
- Updated date: `2026-05-06`.
- Latest conversion-source timestamps from `conversions/latest`:
  - Tag: `2026-05-08T04:58:36Z`.
  - Conversions API: `2026-05-08T04:58:48Z`.
- Top action items / needs-improvement signals:
  - `click_id_epik` in `CHECKOUT` remains a top action item.
  - `product_id` in `ADD_PAYMENT_INFO` remains a top action item.
  - `hashed_email` in `ADD_TO_CART` remains a top action item.
- `order_value` for `ADD_PAYMENT_INFO` read `GOOD` in the fresh API response, so I am not carrying the older AddPaymentInfo order-value UI gap as fresh proof.

Interpretation: Events are still arriving from both Tag and CAPI, but Pinterest Event Quality has not cleared. Real Click ID quality is still inherently limited while Pinterest has no serving traffic.

## Events Overview

Artifacts: `raw/events_overview.txt`, `.json`, `.png`, `_network.json`.

The already-open Events Overview tab was readable and showed standard ecommerce events from `Api · Tag`, including PageVisit, ViewCategory, AddToCart, InitiateCheckout, Search, Checkout, and AddPaymentInfo. Because this was an already-open tab rather than a clean fresh reload, I treated it as supporting evidence only. The stronger freshness signal is the API `conversions/latest` readback above, which showed both Tag and CAPI activity at `2026-05-08 04:58 UTC`.

## Catalog / Data Sources

Artifacts: `raw/catalog_data_sources.*`, `raw/catalog_en_source_detail.*`, `raw/catalog_en_ingestion_issues.*`, `raw/catalog_failed_sitemap_detail.*`.

EN Shopify source visible in the logged-in catalog tab:

- Source/feed profile: `3041760867124595727`.
- Country/language: United States / `en`.
- Source label: Shopify.
- Current ingestion: `May 7 at 1:14 PM EDT`.
- Status: `Completed`.
- Product count: `5,663`.
- Successful uploads: `5,663 of 5,663`.
- Failed uploads: `0`.
- Warnings: `152`.
- Visible latest issue: `Warning 1039`, `description_html` too long; Pinterest says affected items publish without `description_html`.
- Visible occurrences in issue table: `304`.

Failed / localized source state visible in the catalog data-source tab:

- Sitemap source `3041760916127467912` remained `Failed`, latest visible ingestion `May 7 at 3:31 AM EDT`, source URL `sitemap_collections_1.xml`.
- Localized Shopify sources were mixed and not launch-clean in the visible source list. Examples visible in this capture included `cs` `5,577 / 86`, `Deutsch` `5,611 / 52`, `ro` `5,645 / 18`, and `hi` `5,661 / 2`.
- I did not treat any localized-source row as cleared because the fresh new-tab catalog pages produced blank DOM text and the latest durable anchor already parked Pinterest international expansion.

## Product Groups

Artifact: `raw/catalog_product_groups_en.txt`, `.json`, `.png`.

Visible EN product groups included `All Products`, `Top Sellers`, `Midi Dresses`, `Dresses`, `Tops`, `Best Deals`, `New Arrivals`, `Back In Stock`, and `Matching Hawaiian Outfits for Family`.

`Promote` controls were visible. None were clicked.

## Full Item-Level Paid Candidate Proof

Artifacts: `raw/full_item_metadata_summary.json`, `raw/full_item_metadata_rows.csv`, `raw/full_item_metadata_api_sanitized.json`.

Method: read-only metadata refresh by the `346` historical Pinterest EN-US pin IDs from `2026-04-29-pinterest-shopping-ads-gate/pinterest_paid_ready_candidate_offer_rows.csv`. This avoided creating product groups or drafts.

- Candidate rows checked: `346`.
- Unique pin IDs requested: `346`.
- Metadata request count: `35`.
- Metadata rows returned: `337`.
- EN-US rows returned: `337`.
- Matched EN-US `IN_STOCK`: `337`.
- Unmatched rows: `9`.
- Non-in-stock matched rows: `0`.

By group:

| Group | Requested | Found EN-US in stock | Not found | Other |
|---|---:|---:|---:|---:|
| `family_matching` | `103` | `103` | `0` | `0` |
| `mommy_me` | `214` | `205` | `9` | `0` |
| `pajamas` | `29` | `29` | `0` | `0` |

The same `9` missing rows remain all from Shopify product `7229026304097`, title `Elegant Floral Off-Shoulder Dress Set Perfect for S... | DLM`:

- `41878208249953`
- `41878208282721`
- `41878208315489`
- `41878208446561`
- `41878208479329`
- `41878208512097`
- `41878208577633`
- `41878208610401`
- `41878208643169`

Interpretation: a future US-only paused Pinterest draft can only use the `337` currently resolved EN-US in-stock rows unless the `9` missing variants are re-resolved or intentionally excluded immediately before build.

## Blockers

- Pinterest Event Quality remains `Fair`, updated `2026-05-06`.
- `click_id_epik` for Checkout, `product_id` for AddPaymentInfo, and `hashed_email` for AddToCart remain top action items.
- EN Shopify source still has `152` warnings; latest visible issue remains long `description_html`.
- Sitemap source `3041760916127467912` remains failed.
- Localized sources are not launch-clean; do not use Pinterest for international expansion yet.
- Item proof is mostly current but still not complete: `9/346` historical rows do not resolve.
- Fresh Pinterest visual new-tab loads were partly blank, so future account readback should keep using either already-open tabs or API response-body probes when the UI shell appears blank.
- Pinterest draft/campaign/product-group creation still requires exact owner action-time approval.

## Guardrails Preserved

- No Pinterest campaigns, drafts, product groups, catalogs, audiences, budgets, bids, pixels, tags, CAPI paths, or spend were created or edited.
- No Shopify Admin, theme, product, feed, shipping-rate, Market, payment, or order action was taken.
- No Merchant Center, Google Ads, GA4/GTM, Standard Shopping, PMax, Remarketing, conversion-goal, product-scope, product-group, or feed-label action was taken.
- No duplicate theme-level Pinterest tag or custom CAPI path was added.
- No physical-store, warehouse, owned-inventory, local-inventory, stocked-inventory, store-pickup, or guaranteed-stock claim was introduced.

## Commands / Tools Run

- `sed`, `tail`, `rg`, `find`, `jq`, `date`, and `git status --short` to read required memory files and prior Pinterest evidence.
- `curl http://127.0.0.1:9333/json/version` and `/json/list` to verify CDP/browser access and tab state.
- `PINTEREST_ITEM_LIMIT=0 node .../pinterest_cdp_readback.mjs` for account/page captures without the slower item filter probe.
- `PINTEREST_EXISTING_ONLY=1 node .../pinterest_cdp_readback.mjs` for already-open Pinterest tab captures when fresh new-tab pages had blank DOM text.
- `node .../pinterest_full_item_metadata_readback.mjs` for full 346-row pin metadata proof.
- `node .../pinterest_event_quality_api_probe.mjs` for fresh Event Quality API response-body readback.

## Next Safe Action

Keep Pinterest drafts and spend parked. If the parent later asks for paused US-only Pinterest draft approval, scope it only to the `337` resolved EN-US in-stock rows or first re-resolve/exclude the `9` missing rows, then run a just-in-time Event Quality/catalog readback. Do not create drafts, product groups, audiences, campaigns, budgets, bids, or spend without exact owner approval.
