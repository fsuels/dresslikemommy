# Pinterest Catalog/Event Unblock Report

Generated: 2026-05-08 01:56 EDT / 2026-05-08 05:56 UTC

## Decision

`CATALOG_PROOF_NARROWED_AND_UNBLOCKED_FOR_PAUSED_US_SCOPE__EVENT_QUALITY_STILL_FAIR`

The repeating `337/346` Pinterest item-proof blocker is no longer an ambiguous blocker. I re-resolved the 9 stale rows by Shopify variant ID:

- `5` rows re-resolved as EN-US `IN_STOCK`.
- `4` rows still do not return current EN-US Pinterest item metadata and are now explicitly excluded.
- The clean local US Pinterest scope is `342` resolved EN-US in-stock rows: `103` family matching, `210` mommy_me, `29` pajamas.

This does not approve any live Pinterest draft or spend. It gives the next approved build a clean file to use instead of re-arguing over the same stale 9 rows.

## Files

- Clean scope: `lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`.
- Exclusions: `lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`.
- Clean scope summary: `lanes/pinterest/raw/pinterest_us_clean_scope_summary.json`.
- 9-row re-resolution proof: `lanes/pinterest/raw/unresolved_variant_reresolve_rows.csv`.
- Event Quality API proof: `lanes/pinterest/raw/event_quality_api_probe.json`.
- Account/campaign baseline: `lanes/pinterest/raw/campaign_spend_baseline.txt`.

## Catalog Proof

Original historical candidate rows: `346`.

Fresh proof after repair:

| Scope | Rows |
|---|---:|
| Previously resolved EN-US in-stock | `337` |
| Recovered by Shopify variant ID | `5` |
| Clean resolved scope | `342` |
| Explicitly excluded | `4` |

Recovered variants:

- `41878208282721`
- `41878208315489`
- `41878208446561`
- `41878208512097`
- `41878208643169`

Excluded variants:

- `41878208249953`
- `41878208479329`
- `41878208577633`
- `41878208610401`

Public Shopify readback showed the excluded variants are still live/available on the PDP. The exclusion is Pinterest-catalog-specific: they are absent from current EN-US Pinterest item metadata by both stale pin ID and fresh variant-ID re-resolution.

## Event Quality

Pinterest Event Quality remains `Fair`, updated `2026-05-06`.

Fresh API readback:

- Pinterest Tag latest: `2026-05-08T05:50:56.502Z`.
- Conversions API latest: `2026-05-08T05:51:13.760Z`.
- Overall WEB status: `Fair`.
- Pinterest Tag status: `Fair`.
- Conversions API status: `Fair`.
- Verified Merchant Program: `PASS`.
- Automatic Enhanced Match: `PASS`.
- Enhanced Match: `ERROR`.

Top remaining action items:

1. `product_id__ADD_PAYMENT_INFO`
2. `hashed_email__ADD_TO_CART`
3. `click_id_epik__CHECKOUT`

Interpretation: the official Pinterest app path is alive. Forcing Event Quality from `Fair` to `Good` is not a safe local/theme-only fix because it would require either official app/platform behavior to improve, more qualified lower-funnel Pinterest traffic/click IDs, or a separately approved custom Customer Events / CAPI implementation. No duplicate Pinterest tag, custom CAPI, or theme tracking code was added.

## Campaign / Spend Baseline

Read-only campaign baseline still shows:

- `0 campaigns`.
- `0 currently being served`.
- `$0.00` spend.
- `0` impressions.
- `0` pin clicks.

No Pinterest campaign, draft, ad group, product group, audience, budget, bid, tag, CAPI, catalog, data source, or spend write was made.

## Safe Next Approval

The narrowest next live-account approval is now a paused US-only draft build using the `342` clean rows and excluding the 4 unresolved variants.

Exact approval gate:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Spend should remain separately approval-gated while Event Quality is `Fair`.

## Guardrails Preserved

- No Pinterest account writes.
- No Shopify product or theme writes.
- No Merchant, Google Ads, GA4/GTM, feed, conversion-goal, shipping, payment, or order action.
- No duplicate Pinterest tag.
- No custom CAPI/token code.
- No customer PII, cookies, request headers, payment data, or credentials stored.

