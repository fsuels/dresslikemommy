# Measurement Gate Recheck Status

Captured: 2026-04-30 EDT

## Status

`PASS_PAID_VALUE_MEASUREMENT_GATE`

## Proven

- Shopify order `#9475` exists.
- Shopify confirmation number: `Q5RRDFFNR`.
- Shopify order id / transaction reference: `6575609118817`.
- Financial status: `PAID`.
- Captured total: `32.98 USD`.
- Successful authorization and capture were present in Shopify Admin evidence.
- Earlier 100% discount controlled order proved the Google Ads/GA4/Merchant Center runtime purchase path can emit purchase, currency, and dedupe fields.
- Second controlled paid checkout proved primary Google Ads paid purchase value for order `6575644803169`.

## Not Yet Proven

No remaining paid-value blocker for paused campaign cleanup. Campaign-specific launch gates still remain.

## Latest Recheck

The paid thank-you URL was opened after the original order had completed. Shopify redirected to the account order page. The runtime capture saw only page-view/scroll style measurement events and `0` purchase events.

A later Google Ads conversion diagnostics refresh from the Chrome CDP session did not provide order-level diagnostics. The saved refreshed text shows a Google Ads ad-blocker blocker rather than a usable Diagnostics/Webpages view. This is inconclusive, not a pass.

Follow-up: a new controlled paid checkout was started with capture running before payment. It produced order `#9476` / `6575644803169` and captured primary Google Ads purchase conversion `853411529` / `UbkpCN-fhogBEMmN-JYD` with `value=19.99`, `currency=USD`, and order/dedupe id `6575644803169`.

## Required Next Proof

Proceed with paused, campaign-specific cleanup. Do not enable campaigns or raise budgets until feed/product/website/policy gates and explicit owner launch approval pass.
