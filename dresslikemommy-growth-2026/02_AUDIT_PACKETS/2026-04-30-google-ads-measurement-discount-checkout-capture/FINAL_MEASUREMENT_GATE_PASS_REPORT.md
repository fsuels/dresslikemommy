# Google Ads Measurement Gate - Discounted Purchase Capture

Date: 2026-04-30
Status: `PASS_RUNTIME_PURCHASE_FIELDS_FOR_100_PERCENT_DISCOUNT_TEST_ORDER`
Launch decision: `LAUNCH_NOT_APPROVED_BY_THIS_PACKET`

## Result

The owner completed the controlled Shopify checkout using the 100% discount code. The thank-you page produced a Google Ads purchase request and matching GA4 / Merchant Center purchase requests. No Google Ads or campaign settings were edited.

## Required Fields

| Field | Evidence | Result |
|---|---:|---|
| Google Ads purchase event | `purchase` | PASS |
| Conversion ID | `853411529` | PASS |
| Conversion label | `UbkpCN-fhogBEMmN-JYD` | PASS |
| Purchase value field | `0` | PASS for discounted test order |
| Currency | `USD` | PASS |
| Transaction / dedupe key | `6575594274913` via `oid` | PASS |
| Google Ads request accepted | HTTP `200` | PASS |
| GA4 transaction ID | `6575594274913` | PASS |
| GA4 value / currency | `0` / `USD` | PASS for discounted test order |
| GA4 request accepted | HTTP `204` | PASS |
| Duplicate purchase on reload | `0` purchase events | PASS |

## Dedupe Interpretation

The completed order used Shopify order / transaction id `6575594274913`. Google Ads sent it as the `oid` dedupe key. GA4 and Merchant Center sent the same id as `transaction_id`. A reload/account-order follow-up produced zero additional purchase events, so the browser-side duplicate-fire check passed.

## Important Limitation

This was a 100% discounted order. The purchase value was correctly present as `0` with `USD`, which is expected for this test. This proves the runtime purchase field path exists, but it does not prove a nonzero paid order will pass nonzero revenue. The first real paid order, or a future low-dollar paid test, should still be monitored for nonzero value.

## Operating Decision

Measurement field-presence is no longer the blocker for paused-draft cleanup. This packet does not approve campaign launch, campaign enabling, budget increases, or broad Smart Bidding/tROAS scale work by itself. Those still depend on the remaining campaign/feed/site/product gates and first-paid-order monitoring.

## Safe Evidence Files

- `final_measurement_gate_summary.json`
- `raw/manual_complete_order_capture_result.json`
- `raw/manual_complete_order_measurement_requests_sanitized.json`
- `raw/thank_you_reload_capture_result.json`
- `raw/thank_you_reload_measurement_events_sanitized.json`

Raw checkout screenshots and checkout text exports were removed from this packet because they can contain customer contact or address details.
