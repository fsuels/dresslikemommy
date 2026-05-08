# Pinterest Controlled Infrastructure Gate

Generated: 2026-05-08 01:39 EDT / 2026-05-08 05:39 UTC

Lane: Pinterest read-only/local synthesis for `2026-05-08-paid-growth-controlled-infra-refresh`.

Write scope honored: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/pinterest/`.

## Decision

`PINTEREST_US_PAUSED_DRAFTS_NOT_SAFE_YET`

Pinterest is still parked for drafts and spend. The latest stored read-only evidence is fresh enough for this synthesis: advertiser/account identity was confirmed, the campaign baseline is zero, Tag and CAPI are both receiving events, and the EN Shopify catalog source is ingesting. However, Event Quality is still `Fair`, catalog warnings remain, the separate sitemap source is still failed, localized sources are not launch-clean, and the intended US paid candidate item proof is incomplete at `337/346`.

No browser/account action was needed for this synthesis, so no Pinterest tab was opened and no live Pinterest surface was touched.

## Identity / Baseline

Latest read-only Pinterest lane: `2026-05-08-paid-growth-pt-presentment-url-readback/lanes/pinterest/PINTEREST_PT_URL_READBACK_MONITOR.md`.

- Advertiser: `549756244483`.
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- Merchant ID used by helper: `3041760832963738705`.
- Campaign baseline for 2026-04-08 through 2026-05-07: `0 campaigns`, `0 currently being served`, `$0.00` spend, `0` results, `0` impressions, `0` pin clicks.

## Event Quality / Tag / CAPI

Freshest local evidence: `raw/event_quality_api_probe.json`, generated `2026-05-08T05:00:03Z`.

- Overall WEB status: `Fair`.
- Pinterest Tag status: `Fair`.
- Conversions API status: `Fair`.
- Event Quality updated date: `2026-05-06`.
- Latest conversion-source timestamps:
  - Pinterest Tag: `2026-05-08T04:58:36Z`.
  - Conversions API: `2026-05-08T04:58:48Z`.
- Verified Merchant Program conversion-health group: `PASS`.
- Automatic Enhanced Match group: `PASS`.
- Enhanced Match group: `ERROR`.
- Top remaining action items:
  - `product_id__ADD_PAYMENT_INFO`: `NEEDS_IMPROVEMENT`.
  - `hashed_email__ADD_TO_CART`: `NEEDS_IMPROVEMENT`.
  - `click_id_epik__CHECKOUT`: `NEEDS_IMPROVEMENT`.

Supporting Events Overview evidence from the already-open tab showed ecommerce events from `Api · Tag`: PageVisit, ViewCategory, AddToCart, InitiateCheckout, Search, Checkout, and AddPaymentInfo. Because that tab was not a clean fresh reload, the stronger freshness proof is the API `conversions/latest` response above.

Interpretation: Tag/CAPI are alive, but Event Quality has not cleared. The `click_id_epik` gap is partly expected before Pinterest traffic exists, but it still blocks a clean launch decision.

## Catalog Source State

Freshest local evidence: `raw/catalog_data_sources.json`, `raw/catalog_en_source_detail.json`, and `raw/catalog_failed_sitemap_detail.json` from the May 8 Pinterest lane.

EN Shopify source:

- Source/feed profile: `3041760867124595727`.
- Country/language: United States / `en`.
- Source label: Shopify.
- Current ingestion: May 7 at 1:14 PM EDT.
- Status: `Completed`.
- Product count: `5,663`.
- Successful uploads: `5,663 of 5,663`.
- Failed uploads: `0`.
- Warnings: `152`.
- Visible latest issue: `Warning 1039`, `description_html` too long; Pinterest indicates affected items publish without `description_html`.

Failed / localized source state:

- Sitemap source `3041760916127467912` remained `Failed`, latest visible ingestion May 7 at 3:31 AM EDT, source URL `sitemap_collections_1.xml`.
- Localized Shopify sources were mixed and not launch-clean in the visible source list, including warning/fail counts such as `cs` `5,577 / 86`, `Deutsch` `5,611 / 52`, `ro` `5,645 / 18`, and `hi` `5,661 / 2`.
- Pinterest international expansion remains blocked; use only the EN-US Shopify source as the plausible future US-only draft base.

## Item-Level Paid Candidate Proof

Freshest local evidence: `raw/full_item_metadata_summary.json` and `raw/full_item_metadata_rows.csv`, generated `2026-05-08T04:58:03Z`.

- Historical paid candidate rows checked: `346`.
- Unique Pinterest pin IDs requested: `346`.
- Metadata request count: `35`.
- Metadata rows returned: `337`.
- EN-US rows returned: `337`.
- Matched EN-US `IN_STOCK`: `337`.
- Non-in-stock matched rows: `0`.
- Unmatched rows: `9`.

By group:

| Group | Requested | Found EN-US in stock | Not found | Other |
|---|---:|---:|---:|---:|
| `family_matching` | `103` | `103` | `0` | `0` |
| `mommy_me` | `214` | `205` | `9` | `0` |
| `pajamas` | `29` | `29` | `0` | `0` |

The unresolved rows are all Mommy & Me variants for Shopify product `7229026304097`, `Elegant Floral Off-Shoulder Dress Set Perfect for S... | DLM`:

- `41878208249953`
- `41878208282721`
- `41878208315489`
- `41878208446561`
- `41878208479329`
- `41878208512097`
- `41878208577633`
- `41878208610401`
- `41878208643169`

Interpretation: a future US-only paused Pinterest draft should use only the `337` resolved EN-US in-stock rows, or first re-resolve and intentionally include/exclude the `9` missing rows immediately before build.

## Gate Verdict

US paused drafts are not safe yet without a fresh owner approval and a narrowed/exclusion-safe build plan.

Minimum safe path before any Pinterest draft/product-group work:

1. Re-run just-in-time read-only Event Quality and catalog source readback.
2. Re-resolve the `9` missing Mommy & Me rows or exclude them from the build.
3. Use only EN-US Shopify source `3041760867124595727`; do not use failed sitemap or localized sources.
4. Ask for exact owner approval to create paused US-only Pinterest catalog/retargeting drafts with no spend.
5. After approval, create paused-only drafts/product groups with zero live spend and read back before/after.

## Blockers / Residual Risk

- Event Quality still `Fair`, updated `2026-05-06`.
- Top quality gaps remain Product ID in AddPaymentInfo, Email in AddToCart, and Click ID in Checkout.
- EN Shopify source has `152` warnings.
- Sitemap source `3041760916127467912` remains failed.
- Localized sources are not launch-clean and should not be used for Pinterest international tests.
- Item proof is only `337/346`; `9` intended candidate rows remain unresolved.
- Real click-ID quality likely cannot fully clear until Pinterest has traffic, but that is a risk to document before any spend.

## Actions Not Taken

- No Pinterest campaigns, drafts, product groups, audiences, budgets, bids, tags, CAPI settings, catalogs, data sources, or spend were created or edited.
- No Shopify product/feed/theme, Merchant, Google Ads, GA4/GTM, shipping-rate, Market, payment, or order action was taken.
- No physical-store, local-inventory, stocked-inventory, warehouse, pickup, or guaranteed-on-hand-stock claim was introduced.

## Next Safe Action / Approval Gate

Next safe action: keep Pinterest parked and ask the parent/owner whether to prepare a US-only paused Pinterest draft plan limited to the `337` resolved EN-US in-stock rows, with the `9` unresolved rows excluded unless they re-resolve.

Exact approval gate before any Pinterest account write:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE ONLY RESOLVED EN-US IN-STOCK ROWS OR EXCLUDE UNRESOLVED ROWS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

