# Merchant Age Group Exact Export Verification Path

Date: 2026-05-08
Mode: read-only/local analysis; no Merchant, Shopify, feed, or Ads write

Problem: `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT`

## Result

No current exact paid-cohort `Missing age group` count was found in local artifacts after the May 8 source movement.

The latest exact CSV exports are stale May 7 exports:

- `2026-05-07 23:18`: `623` paid-cohort US/en item IDs.
- `2026-05-07 23:57`: `623` paid-cohort US/en item IDs.

The May 8 post-refresh export attempt did not produce a product-issues CSV, but it did capture strong non-exact positive evidence:

- Source `upload_paid_cohort_age_group_only.txt` / `10651516446` processed `780`, matched `771`, and had `9` `Offer does not exist`.
- US/en sample item timestamp advanced to `2026-05-08T05:55:06+00:00`.
- Visible diagnostics no longer showed `Missing age group`.

## API Feasibility

Stored API probe summaries show the current local `gcloud` token lacks the needed Merchant/Content API scopes for read-only product/product-status diagnostics. API fallback requires regenerated/read-only Merchant diagnostics scopes outside the repo.

## Next Safe Action

1. Run a fresh read-only Merchant browser diagnostics product-issues export in a dedicated tab.
2. Reconcile the export against the `780` paid-cohort IDs.
3. If the export still fails, download/read the source processing report for source `10651516446` to enumerate the `9` unmatched rows.
4. Use API only after proper read-only Merchant diagnostics scopes are available outside the repo.

Status recommendation: keep `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT` as `ACTIVE_VERIFYING`.

## Evidence

- Stale exact count: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/merchant-product-issues-summary-2026-05-07-2357.json`.
- May 8 failed CSV materialization: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/readback-after-timestamp-advance/product-issues-browser-export/download_attempt_summary.json`.
- May 8 source/sample improvement: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/MERCHANT_SOURCE_REFRESH_APPROVED_ACTION_REPORT.md`.
- API scope blocker: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/merchant/api-product-issues/merchant_center_api_diagnostics_summary.json`.

