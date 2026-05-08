# Merchant Controlled Infrastructure Refresh

Generated: `2026-05-08T01:39:55-0400`

Mode: read-only/local evidence synthesis for the paid-growth controlled infrastructure refresh.

## Status

Merchant is **not cleared** for paid-growth expansion.

Current known exact count remains the prior completed browser CSV export: `623` paid-cohort US/en unique item IDs with `Missing age group`. The latest 2026-05-08 read-only Merchant lane did not produce a fresher exact CSV because the UI showed/triggered a download state but no CSV materialized before the lane stopped.

The latest visible Merchant diagnostics evidence from 2026-05-08 still showed:

- Account: `Dresslikemommy` / `124884876`.
- Visible diagnostics timestamp: `Last updated at 1:02 AM May 8, 2026`.
- Visible issues still included `Missing age group` and `Missing local inventory data`.
- Visible diagnostics table total: `10,985`.

The latest completed exact product-issues export from 2026-05-07 23:57 had:

- Export rows: `34,716`.
- Paid cohort input size: `780`.
- Paid-cohort US/en `Missing age group`: `623` unique item IDs, `1,246` rows across Shopping ads and Free listings.
- Paid-cohort US/en `Missing local inventory data`: `771` unique item IDs.
- Sample item `shopify_US_7227254276193_41871113158753` remained in the paid-cohort US/en `Missing age group` set.

`Missing local inventory data` remains a non-fix target for this business. Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory; do not create local inventory feeds, local stock/store/warehouse claims, pickup claims, or guaranteed on-hand stock claims to clear this diagnostic.

## Sample Source Timestamp

Sample item: `shopify_US_7227254276193_41871113158753`

Latest source readback for US/en:

- Source ID: `10627623003`.
- Source name: `Shopify App API`.
- Feed label: `US`.
- Language: `en`.
- Last updated: `2026-05-07T14:14:02+00:00`.
- Expected paid labels visible: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`.

This timestamp is still older than the Shopify-side age-group repair/readback, so the source-refresh concern remains live.

## Evidence Movement

Evidence improved only relative to the older `754` paid-cohort US/en missing-age-group count, because the later completed browser export showed `623`.

Evidence did **not** improve in this controlled-infra refresh lane:

- Latest exact count remains `623`.
- The 2026-05-08 visible diagnostics still showed `Missing age group`.
- The sample source timestamp still remained `2026-05-07T14:14:02+00:00`.
- API product/status paths are still blocked by insufficient local OAuth scopes.

## Blockers

- Fresh exact Merchant product-issues CSV was not obtained after the 2026-05-08 attempt.
- Merchant API `products.list` and Content API `productstatuses.list` remain blocked by `403 PERMISSION_DENIED` / insufficient authentication scopes.
- Source `10627623003` / `Shopify App API` appears stale for the sample US/en row.
- Any official source refresh/sync, Google & YouTube publication toggle, feed upload, product-data edit, or local-inventory action requires exact owner approval and must not be inferred from this read-only lane.

## Exact Safe Next Action

Retry a read-only Merchant product-issues export and sample source timestamp readback later, using the assigned Merchant tab/session `DLM-MERCHANT-US-SourceRefresh`. Confirm account `Dresslikemommy` / `124884876`, stop on login/CAPTCHA/modal/permission/unsaved-change risk, and do not click source refresh/sync, upload, Fix, View fix, Save, Apply, or any Google & YouTube publication toggle.

If the count remains `623` and the sample US/en source timestamp remains stale, the next non-read-only path is an owner-approved official Google & YouTube / Merchant source refresh investigation. Do not repeat the prior product publication toggle without fresh exact approval.

## Files Used

- `AGENTS.md`
- `ops/AGENT_COORDINATION.md`
- `ops/BROWSER_SUBAGENT_COORDINATION.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- `ops/AGENT_WORKLOG.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/MERCHANT_PT_URL_READBACK_MONITOR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/diagnostics-visible-summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/api-product-issues/merchant_center_api_diagnostics_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/product-issues-browser-export/download_attempt_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/merchant-product-issues-summary-2026-05-07-2357.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/product-issues-browser-export/product_issues_2026-05-07_23-57-24.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-merchant-source-refresh-readonly-review/shopify-variant-age-group-readonly/summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-merchant-source-refresh-action/post-toggle-shopify-variant-age-group-readonly/summary.json`

## Commands Used

- `sed -n '1,260p' AGENTS.md`
- `sed -n '1,220p' ops/AGENT_COORDINATION.md`
- `sed -n '1,220p' ops/BROWSER_SUBAGENT_COORDINATION.md`
- `sed -n '1,260p' ops/GOOGLE_ADS_CONTINUITY.md`
- `tail -n 240 ops/AGENT_WORKLOG.md`
- `rg -n "Merchant|Missing age group|age_group|10627623003|Shopify App API|623|754|Missing local inventory|source refresh" ...`
- `find .../lanes/merchant ... -maxdepth 3 -type f | sort`
- `jq '.' ...`
- `python3 - <<'PY' ... PY` to re-parse the prior completed browser CSV and paid-cohort file locally.
- `mkdir -p dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/merchant`

No Merchant upload, source sync/refresh, product edit, Google & YouTube toggle, Shopify product-data edit, local inventory feed/claim, Ads change, campaign change, budget/bid/status/product-scope/feed-label/conversion-goal change, browser write, or account write was performed.
