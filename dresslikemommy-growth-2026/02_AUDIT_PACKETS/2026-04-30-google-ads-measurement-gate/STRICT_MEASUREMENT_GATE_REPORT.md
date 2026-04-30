# Strict Google Ads Measurement Gate - Purchase Runtime Proof

Generated: 2026-04-30T18:55:12.602628+00:00

## Decision

`BLOCK_NON_BUDGET_CAMPAIGN_EDITS__RUNTIME_PURCHASE_MEASUREMENT_NOT_PROVEN`

Launch status: `LAUNCH_BLOCKED`

No Google Ads, Shopify, checkout, theme, campaign, conversion-goal, or order changes were made. No test order was created. This is a read-only measurement gate.

## Bottom Line

The Google Ads configuration sub-gate still looks healthy, but the stricter measurement gate does **not** pass yet. I can prove that Google Ads has one primary purchase action and that Shopify's Google & YouTube app pixel is connected. I cannot prove, from current evidence, that a real completed purchase sends all required runtime fields: nonzero `value`, `currency`, `transaction_id`, and one deduped primary Ads purchase per order.

Therefore, only owner-approved paused budget-safety edits remain allowed. Non-budget campaign edits, conversion-goal edits, bidding edits, asset/URL/location edits, and launch/enabling work remain blocked.

## Configuration Evidence That Passed

- Google Ads target action: `Google Shopping App Purchase`.
- Action optimization: `Primary`.
- Included in account-level goals: `True`.
- Value setting: `Use different values. If there's no value, use 0.`
- Source: `Website`.
- Count: `Every conversion`.
- Enhanced conversions: `Managed through Google Tag. Enhanced conversions is enabled.`
- Last received request for target action: `2026-04-25T23:55:54.592430+00:00` (4.789 days old at capture).
- Historical target all conv. / value: `5.0` / `193.9`.
- Shopify Customer events shows Google & YouTube app pixel as `Connected` / `Optimized`.
- Theme scan found no hard-coded Google Ads `AW-`, `gtag(`, `googleadservices`, `send_to`, `transaction_id`, or `checkout_completed` purchase snippet in theme files.

## Strict Runtime Requirements

### purchase_value_runtime_value

Status: `NOT_PROVEN`

- Google Ads target setting says: Use different values. If there is no value, use 0.
- Target historical all-conversion value is 193.9; this proves historical value evidence, not a current runtime order hit.
- No completed-purchase network request or tag payload was captured in this gate.

Approval effect: Blocks non-budget campaign edits and launch work.

### purchase_currency_runtime_currency

Status: `NOT_PROVEN`

- Target Google Ads row currency is XXX, not a captured runtime USD parameter.
- Secondary purchase rows show USD in Google Ads history, but those are not the primary optimization action.
- No completed-purchase payload with currency=USD was captured.

Approval effect: Blocks value bidding, campaign-goal edits, and launch work.

### purchase_transaction_id_runtime_order_id

Status: `NOT_PROVEN`

- Google Ads manual snippet diagnostic still contains a blank transaction_id placeholder.
- Runtime tracking is expected to be owned by Shopify Google & YouTube, but no completed-purchase request was captured.
- No order id / transaction id / event id was proven in an Ads purchase hit.

Approval effect: Blocks launch work because duplicate order attribution cannot be ruled out.

### deduplication_one_purchase_per_order

Status: `PARTIAL_CONFIG_ONLY__RUNTIME_NOT_PROVEN`

- Positive config evidence: exactly one primary account-level Google Ads purchase action is present.
- Positive theme evidence: theme scan found no AW-/gtag/googleadservices/send_to/transaction_id/checkout_completed purchase snippet in theme files.
- Positive Shopify evidence: Google & YouTube app pixel is Connected / Optimized in Shopify Customer events.
- Residual risk: 4 purchase conversion actions still exist in Google Ads, including secondary actions with historical value; no order-level dedupe capture proves only one primary Ads purchase fire per order.

Approval effect: Allows read-only audit and budget safety only; blocks non-budget changes until runtime capture passes.

## Purchase Conversion Actions Seen

| Conversion action | Optimization | In account goals | Currency | All conv. | All conv. value | Last conversion | Last received request raw |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| Google Shopping App Purchase | Primary | True | XXX | 5.0 | 193.9 | 20260128 | 1777161354592430 |
| Purchases from google Adwords | Secondary | False | USD | 1284.0 | 100091.33 | 20260128 | 1774477077701497 |
| Purchases from google analytics data | Secondary | False | USD | 494.0 | 26863.31 | -- | 0 |
| dresslikemommy.com - GA4 (web) purchase | Secondary | False | USD | 16.541798 | 1300.122373636 | 20260128 | 0 |

## Evidence Files

- `google_ads_conversion_value_gate_report.md`
- `google_ads_conversion_value_gate_summary.json`
- `purchase_conversion_actions.csv`
- `screenshots/google_ads_conversion_detail.png`
- `screenshots/shopify_customer_events.png`
- `screenshots/shopify_customer_events_custom_pixels_after_coordinate_click.png`
- `raw/google_ads_conversion_detail_body_text.txt`
- `raw/shopify_customer_events_body_text.txt`
- `raw/shopify_customer_events_custom_pixels_after_coordinate_click.txt`
- `raw/theme_tracking_surface_scan.txt`
- `raw/assets_analytics_event_surface.txt`

## Required Next Proof

1. Run an owner-approved controlled checkout/test order or Tag Assistant purchase capture.
2. Capture the Google Ads purchase request/pixel payload for the primary purchase action.
3. Verify a real nonzero purchase `value`, `currency=USD`, and a real `transaction_id` / order id.
4. Verify deduplication by proving the same `transaction_id` does not create a second primary Ads purchase on repeated thank-you/order-status views.
5. Only after that proof passes should non-budget campaign edits or launch work be reconsidered.
