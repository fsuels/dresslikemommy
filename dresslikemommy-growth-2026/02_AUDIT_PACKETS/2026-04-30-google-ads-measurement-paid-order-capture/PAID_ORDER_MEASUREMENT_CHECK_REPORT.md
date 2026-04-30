# Paid Order Measurement Check

Date: 2026-04-30
Status: `BLOCKED_GOOGLE_ADS_PAID_PURCHASE_RUNTIME_REQUEST_NOT_CAPTURED`

## What Passed

Shopify confirms the paid order exists and payment was captured.

| Field | Evidence | Result |
|---|---:|---|
| Shopify order | `#9475` | PASS |
| Confirmation number | `Q5RRDFFNR` | PASS |
| Shopify order id | `6575609118817` | PASS |
| Financial status | `PAID` | PASS |
| Paid total | `32.98 USD` | PASS |
| Subtotal | `19.99 USD` | PASS |
| Shipping | `12.99 USD` | PASS |
| Successful capture transaction | `True` | PASS |

Line item: `Tropical One-Shoulder Ruffle Swimsuit for Women and... | DLM - Mother XL / Multi-Color`; quantity `1`; variant `Mother XL / Multi-Color`.

Transactions:
- `AUTHORIZATION` `SUCCESS` via `shopify_payments`: `32.98 USD` at `2026-04-30T20:38:00Z`
- `CAPTURE` `SUCCESS` via `shopify_payments`: `32.98 USD` at `2026-04-30T20:38:04Z`

## What Did Not Pass

The owner-provided thank-you URL was opened in the remote-debuggable Chrome test profile after the order had already completed. Shopify redirected that page to the account order page. The capture observed page-view/scroll measurement requests only and found `0` paid `purchase` events.

Google Ads diagnostics page was also checked. It showed Consent Mode implemented, but did not expose an order-level paid purchase request/value confirmation for this order during this check.

## Decision

The paid order itself is valid and paid. However, the strict nonzero paid-value measurement proof is still not complete because no Google Ads purchase request with `value=32.98`, `currency_code=USD`, and `oid=6575609118817` was captured.

Keep campaign launch and non-budget edits that depend on nonzero paid purchase value blocked until either:

1. Tag Assistant / CDP captures a paid order at the moment the thank-you page first loads, or
2. Google Ads / GA4 diagnostics later shows this exact paid order value and transaction id, or
3. A new low-dollar paid test is run while capture is already active.

## Safe Evidence Files

- `paid_order_measurement_gate_summary.json`
- `raw/paid_order_shopify_admin_sanitized.json`
- `raw/paid_order_measurement_events_sanitized.json`
- `raw/paid_order_page_observation_sanitized.json`
- `raw/google_ads_conversion_detail_diagnostics_text_sanitized.txt`
