# Measurement Read-only Lane Report

Generated: `2026-05-11T12:31:34+00:00`
GA4 property: `330266838`
Date range attempted: `2026-04-01` through `2026-05-10`
Gate status: `NOT_SOLVED_CREDENTIAL_SCOPE_OR_UI_EXPORT_REQUIRED`

## What Ran

- Reconciled the prior sanitized Shopify non-USD candidate file into local candidate JSON/CSV.
- Tested existing `gcloud` user and ADC credential availability without storing tokens.
- Attempted read-only GA4 Admin API `accountSummaries` and GA4 Data API metadata/runReport calls.
- Scanned selected local measurement/GA4/export packet artifacts for non-US purchase transaction/currency evidence without saving excerpts.

## Candidate Reconciliation

- Prior sanitized Shopify non-USD candidates: `7`.
- High-priority paid non-zero candidates: `6`.
- Candidate currencies: `CHF, DKK, GBP`.
- Strongest windows remain the paid non-zero DKK/GBP/CHF orders already documented; the refunded GBP row is useful only as a control/original-value reference.

## GA4 API Result

- `gcloud` user token available: `True`.
- Analytics-readonly scoped token request available: `False`.
- Analytics-readonly scoped token request error: `ERROR: (gcloud.auth.print-access-token) Invalid value for [--scopes]: Invalid scopes value. Please make sure the scopes are from [('openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/appengine.admin', 'https://www.googleapis.com/auth/sqlservice.login', 'https://www.googleapis.com/auth/compute')]`.
- ADC token available: `False`.
- Analytics OAuth scopes visible from tokeninfo: `none`.
- Admin API statuses: `403`.
- Data metadata statuses: `403`.
- Data runReport attempts: `2`.
- Error/status reasons observed: `ACCESS_TOKEN_SCOPE_INSUFFICIENT; PERMISSION_DENIED: Request had insufficient authentication scopes.`.

The existing CLI token did not yield order-level GA4 `purchase` rows with transaction/currency/value evidence. No GA4 settings were changed.

## Local Export Scan

- Text/zip files scanned: `61`.
- Non-US purchase/transaction/currency term hits: `13`.
- Conclusion: no existing local export in the selected packet set proves GA4 order-level non-US purchase currency/value/transaction.

## Files In This Lane

- `ga4_readonly_measurement_probe.py`
- `ga4_api_readonly_probe_sanitized.json`
- `reconciled_shopify_non_usd_candidates.json`
- `reconciled_shopify_non_usd_candidates.csv`
- `local_export_scan_summary.json`
- `PURCHASE_MEASUREMENT_READONLY_REPORT.md`

## Next Action

Refresh/provide a read-only Google Analytics OAuth credential with Analytics Data API scope for property `330266838`, then rerun this lane's Data API query for `eventName = purchase` with `transactionId`, `currencyCode`, country/date, and purchase revenue fields. If that cannot expose historical order-level fields, the remaining gate is logged-in GA4 UI Explore/export or exact owner approval for the controlled non-US test-purchase/refund/cancel procedure already documented in the prior packet.

Guardrails preserved: no GA4/GTM/Google Ads/Shopify/Pinterest settings writes, no checkout/payment/order/refund/cancel, no token storage, no customer PII, and no full order or transaction IDs stored.
