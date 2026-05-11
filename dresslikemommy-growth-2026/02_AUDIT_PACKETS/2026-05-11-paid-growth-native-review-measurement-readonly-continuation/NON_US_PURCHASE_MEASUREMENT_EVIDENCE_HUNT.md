# Non-US Purchase Measurement Evidence Hunt

Generated: 2026-05-11 02:35 EDT
Mode: `READ_ONLY_LOCAL_EVIDENCE_AND_GOOGLE_ADS_CAPTURE`

## What This Session Proved

- Read-only Google Ads conversion-action capture refreshed successfully.
- `Google Shopping App Purchase` still appears as the primary account-level purchase action with dynamic value evidence and recent request evidence.
- Shopify Admin read-only query found `7` sanitized non-USD presentment orders since 2026-04-01.
- `gcloud auth print-access-token` exists for the signed-in user, but a read-only GA4 Admin API `accountSummaries` request returned `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`, so GA4 API matching could not be completed from CLI in this session. The sanitized failed readback is stored as `ga4_admin_account_summaries_readonly.json`.
- A bounded read-only GA4 UI probe through the existing Chrome CDP session reached `Analytics | Home` for account `88409806`, property `330266838`, visible property name `dresslikemommy.com - GA4`, and a visible `Purchases` card. This proves logged-in UI access exists, but it still does not expose order-level currency/value details.
- A read-only click from the GA4 home `View events` control reached `Analytics | Events: Event name` for last 28 days and showed the first `10` of `15` event rows, total event count `21,815`, total users `2,659`, and total revenue `$1,103.34`. The visible first page included `begin_checkout` but not `purchase`; no event-level currency/value details were exposed in this bounded pass.

## What This Does Not Prove

- It does not prove that a non-US `purchase` event arrived in GA4.
- It does not prove that a non-US `purchase` conversion arrived in Google Ads with the same presentment currency/value.
- It does not prove transaction-id deduplication or absence of duplicate purchase events.

## Sanitized Shopify Order Candidates

The local JSON/CSV stores only date/time, country, masked order identifiers, fulfillment/financial status, and money/currency fields. It intentionally excludes customer names, email, phone, street address, and full order IDs.

Candidate currencies found: `CHF, DKK, GBP`.

## Read-only Next Path

1. In the logged-in GA4 UI property `330266838`, search Event reports / Explore / DebugView or Realtime where available for `purchase` events near the candidate timestamps and compare currency/value/transaction evidence. The CLI GA4 Admin/Data API path is currently blocked by insufficient OAuth scopes.
2. In Google Ads conversion diagnostics/activity, search for request or conversion details near the same candidate timestamps.
3. Use Shopify Admin only as the order-side source of truth for masked matching. Do not store PII in repo artifacts.
4. If no historical non-US purchase can be matched, request exact controlled purchase approval before creating any test order.

## Exact Approval Wording If A Test Purchase Is Required

`APPROVE CONTROLLED NON-US PURCHASE MEASUREMENT PROOF ONLY: RUN ONE LOW-VALUE NON-US TEST PURCHASE FOR DRESSLIKEMOMMY USING A COUNTRY-QUALIFIED STOREFRONT SESSION, CAPTURE TAG ASSISTANT/DEVTOOLS/GA4 DEBUGVIEW EVIDENCE FOR THE OFFICIAL GOOGLE & YOUTUBE APP PURCHASE EVENT CURRENCY, VALUE, TRANSACTION_ID, AND GOOGLE ADS CONVERSION REQUEST, THEN IMMEDIATELY REFUND AND CANCEL THE TEST ORDER IF THE PLATFORM ALLOWS; DO NOT ENABLE ANY CAMPAIGN, DO NOT CHANGE BUDGETS/BIDS/STATUSES, DO NOT CHANGE CONVERSION GOALS/ACTIONS, DO NOT EDIT SHOPIFY PRODUCTS/THEME/CUSTOMER EVENTS, DO NOT EDIT MERCHANT/PINTEREST/ADS SETTINGS, DO NOT CREATE INVENTORY OR LOCAL-PICKUP CLAIMS, AND STORE ONLY SANITIZED EVIDENCE.`
