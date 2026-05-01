# Safe Evidence Manifest

Packet: `2026-04-30-google-ads-standard-shopping-activation-gate`

## Live Google Ads Evidence

- `raw/google_ads_all_campaigns_live_activation_readback.txt`
- `screenshots/google_ads_all_campaigns_live_activation_readback.png`
- `raw/standard_shopping_settings_live_activation_gate_expanded.txt`
- `screenshots/standard_shopping_settings_live_activation_gate_expanded.png`
- `raw/standard_shopping_inventory_filter_live_activation_gate_expanded.txt`
- `raw/standard_shopping_inventory_filter_visible_controls.json`
- `screenshots/standard_shopping_inventory_filter_live_activation_gate_expanded.png`
- `raw/standard_shopping_product_groups_live_activation_gate.txt`
- `screenshots/standard_shopping_product_groups_live_activation_gate.png`
- `raw/standard_shopping_bidding_live_activation_gate_expanded.txt`
- `screenshots/standard_shopping_bidding_live_activation_gate_expanded.png`

## Conversion Evidence

- `raw/google_ads_purchase_conversion_action_live_activation_gate.txt`
- `screenshots/google_ads_purchase_conversion_action_live_activation_gate.png`
- `../2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`

## Merchant Center Evidence

- `raw/merchant_exact_label_readback_refresh_check.json`
- `raw/merchant_center_all_products_live_context_after_label_check.txt`
- `screenshots/merchant_center_all_products_live_context_after_label_check.png`
- `../2026-04-29-merchant-clean-label-upload/paid_label_active_status_live_shopify_check.json`
- `../2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`

## Decision Files

- `STANDARD_SHOPPING_ACTIVATION_GATE_REPORT.md`
- `STANDARD_SHOPPING_ACTIVATION_EXECUTION_REPORT.md`
- `standard_shopping_activation_gate_readback.csv`
- `standard_shopping_activation_execution_readback.csv`
- `ROLLBACK_TRIGGER.md`

## Post-Enable Execution Evidence

- `raw/post_enable_all_campaigns_final_readback.txt`
- `screenshots/post_enable_all_campaigns_final_readback.png`
- `raw/post_enable_settings_final_readback.txt`
- `screenshots/post_enable_settings_final_readback.png`
- `raw/post_enable_location_options_live_check.txt`
- `screenshots/post_enable_location_options_live_check.png`
- `raw/post_enable_ad_groups_readback.txt`
- `screenshots/post_enable_ad_groups_readback.png`
- `raw/post_enable_product_groups_readback.txt`
- `screenshots/post_enable_product_groups_readback.png`
- `raw/post_enable_bidding_guardrail_readback.txt`
- `screenshots/post_enable_bidding_guardrail_readback.png`
- `raw/post_enable_change_history_readback.txt`
- `screenshots/post_enable_change_history_readback.png`

## Safety Notes

- The campaign was enabled only after exact owner approval.
- Budget remained `$1.00/day`.
- No other campaign was enabled.
- No credentials, cookies, request headers, payment data, or customer PII were written to this packet.
