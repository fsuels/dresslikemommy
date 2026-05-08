# Paid Growth Controlled Infrastructure Refresh

Date: 2026-05-08
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-controlled-infra-refresh`

## Decision

`LOCAL_PAUSED_INFRASTRUCTURE_ADVANCED__LIVE_SPEND_AND_ACCOUNT_WRITES_STILL_BLOCKED`

This session moved the paid-growth sprint forward without crossing approval gates. The most concrete build result is a refreshed local-only international Google Search packet whose final URLs now use `country=<ISO>` and whose importable rows still validate as paused-only.

No live spend, campaign import/create/enable/pause, budget/bid/status/conversion-goal change, Standard Shopping/PMax/Remarketing change, Merchant upload/source refresh, Google & YouTube toggle, Shopify product-data edit, Pinterest draft/spend, shipping/Markets change, theme publish, payment, or order creation happened.

## Parent / Subagent Execution

The parent read the required continuity/coordination files first, created a lane board, added a read-only/local coordination row, then spawned six disjoint subagents:

| Lane | Output |
|---|---|
| Merchant | `lanes/merchant/MERCHANT_CONTROLLED_INFRA_REFRESH.md` |
| Google Ads intl Search | `lanes/ads-intl/ADS_INTL_COUNTRY_URL_PACKET_REFRESH.md` |
| Pinterest | `lanes/pinterest/PINTEREST_CONTROLLED_INFRA_GATE.md` |
| Localization | `lanes/localization/LOCALIZATION_CONTROLLED_INFRA_READINESS.md` |
| ROAS | `lanes/roas/ROAS_CONTROLLED_GUARDRAILS.md` |
| Creative | `lanes/creative/CREATIVE_CONTROLLED_COPY_REFRESH.md` |
| Measurement | `lanes/measurement/MEASUREMENT_CONTROLLED_READBACK.md` |

## Main Results

### Google Ads Paused International Search

- Refreshed local-only packet path: `lanes/ads-intl/`.
- Updated final URLs in copied `keyword_plan.csv`, `rsa_copy_pack.csv`, and `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`.
- ES/IT/RO/PT now use localized product paths plus `country=<ISO>`.
- Other non-US paused shells now use base English product paths plus `country=<ISO>`.
- Validation passed:
  - `17` campaigns.
  - `204` ad groups.
  - `612` exact/phrase positive keywords.
  - `629` negatives.
  - `204` RSAs.
  - `1666` web bulk rows.
  - Max CPC remains `$0.15`.
  - All importable entities remain paused.
  - `0` missing country parameters.
  - `0` bare ES/IT/RO/PT language-only URLs.
  - `0` PMax, Standard Shopping, product-scope, feed-label, product-group, or conversion-goal edit rows.

### Merchant / Google & YouTube

- Merchant remains `NOT_CLEARED_NO_NEW_EXACT_IMPROVEMENT`.
- Latest exact completed count remains prior `623` paid-cohort US/en unique item IDs with `Missing age group`.
- Sample item `shopify_US_7227254276193_41871113158753` still shows source `10627623003` / `Shopify App API`, timestamp `2026-05-07T14:14:02+00:00`.
- Visible 2026-05-08 diagnostics still showed `Missing age group` plus `Missing local inventory data`.
- Merchant API / Content API paths remain blocked by `403 PERMISSION_DENIED`.
- `Missing local inventory data` remains a non-fix target because DLM is dropshipping with no physical store or owned inventory.

### Pinterest

- Pinterest remains parked.
- Advertiser `549756244483`; catalog `Catalog_Retail`; baseline remains `0 campaigns`, `0 currently serving`, `$0.00` spend.
- Event Quality remains `Fair`, updated `2026-05-06`.
- Tag/CAPI timestamps are fresh around `2026-05-08T04:58Z`.
- EN Shopify source `3041760867124595727` remains completed `5,663/5,663`, `0` failed, `152` warnings.
- Sitemap source `3041760916127467912` remains failed.
- Item proof remains `337/346` EN-US in-stock rows; `9` Mommy & Me variants for product `7229026304097` remain unresolved.
- A concrete local solution package now exists at `lanes/pinterest-solution/`: it uses the `337` resolved EN-US in-stock rows and writes the `9` unresolved rows to `excluded_unresolved_9.csv`.
- The package includes `resolved_337_product_scope.csv`, `product_group_scope.csv`, `paused_campaign_draft_plan.csv`, and `creative_draft_rows.csv` for a future approval-gated paused US draft build.

### Merchant Solution Ladder

- A concrete Merchant solution ladder now exists at `lanes/merchant-solution/MERCHANT_SOURCE_REFRESH_SOLUTION_LADDER.md`.
- The recommended fix is not more Shopify age_group edits. It is an owner-approved official Google & YouTube / Merchant source refresh/sync/update-products action after just-in-time readbacks.
- The approval gate explicitly prohibits product data edits, feed uploads, local inventory fixes, product publication toggles, ads, budgets, bids, product scope, product groups, pixels, and conversion-goal changes.
- If no safe official refresh/sync control is visible, the parallel solution is read-only Merchant/Product Status API credential repair outside the repo so the exact issue count/source state can be queried without fragile browser CSV downloads.

### Localization / URL Readiness

- 18-market readiness matrix written.
- ES/IT/RO/PT remain the strongest localized paused-infra candidates because country-qualified URLs were browser-proven in the previous packet.
- GB/CA/AU are English-first paused-only candidates; they still need fresh country/currency/checkout readbacks before enablement.
- CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR are paused-shell-only until local route/currency/shipping/language QA clears.
- Live-spend-ready international markets: `0`.

### ROAS / Economics

- Target `650% ROAS` means max ad cost is `15.38%` of revenue.
- At `$70` AOV, target max CPA is `$10.77`.
- At `$63.25` AOV, target max CPA is `$9.73`; the prior `$9.49` conservative CAC guardrail remains useful.
- At `$70` AOV:
  - `$0.04` CPC needs about `0.37%` CVR.
  - `$0.10` CPC needs about `0.93%` CVR.
  - `$0.15` CPC needs about `1.39%` CVR.
  - `$0.20` CPC needs about `1.86%` CVR.
  - `$0.25` CPC needs about `2.32%` CVR.
- Romania presents in RON, so RO reporting must be local-currency or FX-normalized before ROAS decisions.

### Creative / Copy

- Local-only claim-safe copy pack refreshed.
- Validation passed:
  - `13` Google RSA rows.
  - `12` Pinterest rows.
  - `10` localized-market note rows.
  - Google headlines `<= 30` characters.
  - Google descriptions `<= 90` characters.
  - Forbidden customer-facing claim scan passed.
- No upload, ad creation, Pinterest draft, or account write.

### Measurement

- Google paid-value purchase gate remains trusted for local guardrails.
- Google Ads reporting cleanup remains the current rule: use primary purchase value, not historical `All conv. value / cost` polluted by old micro-conversion values.
- Fresh Google Ads, Merchant, Pinterest, storefront, and economics readbacks are still required before spend or enablement.

## Approval Gates

Paused international Google Search import/create still requires the exact paused-growth approval from `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, then just-in-time readbacks and preview-only import validation.

Merchant official source refresh still requires exact action-time approval. Do not click source/app sync, upload, product toggle, or product-data edits by inference.

Pinterest paused US drafts require fresh approval and should be limited to the `337` resolved EN-US in-stock rows unless the `9` unresolved rows are re-resolved or excluded immediately before build.

## Next Best Action

Closest path to the North Star:

1. Fix Merchant source propagation with the exact approval gate in `lanes/merchant-solution/MERCHANT_SOURCE_REFRESH_SOLUTION_LADDER.md`; execute one clearly labeled official refresh/sync/update-products control only after just-in-time readbacks.
2. If the owner wants Pinterest infrastructure, use the solution package in `lanes/pinterest-solution/` to create paused US-only drafts after exact approval; exclude the 9 unresolved rows.
3. If the owner wants Google Ads infrastructure, use the refreshed Ads packet in `lanes/ads-intl/`, run just-in-time readbacks, preview the import first, and keep everything paused.
4. Before live spend, run country-level storefront checkout/currency readbacks for GB/CA/AU and any broader countries being considered.

## Files Produced

- `LANE_BOARD.md`
- `PAID_GROWTH_CONTROLLED_INFRA_REFRESH_REPORT.md`
- `NEXT_CONTINUATION_PROMPT.md`
- Lane reports and summaries under `lanes/`

## Guardrails Preserved

No live account writes or spend. No physical-store, warehouse, local-inventory, stocked-inventory, pickup, or guaranteed-on-hand-stock claim was introduced.
