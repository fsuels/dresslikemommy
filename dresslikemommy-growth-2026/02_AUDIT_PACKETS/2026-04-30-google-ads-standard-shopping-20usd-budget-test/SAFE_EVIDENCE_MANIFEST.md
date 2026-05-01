# Safe Evidence Manifest

Packet: `2026-04-30-google-ads-standard-shopping-20usd-budget-test`

## Decision Files

- `STANDARD_SHOPPING_20USD_48H_BUDGET_TEST_REPORT.md`
- `ROLLBACK_AND_MONITORING_48H.md`
- `standard_shopping_20usd_budget_readback.csv`

## Pre-Change Evidence

- `raw/pre_budget_raise_settings_readback.txt`
- `screenshots/pre_budget_raise_settings_readback.png`

## Budget Edit Evidence

- `raw/budget_panel_open_before_20.txt`
- `raw/budget_panel_open_before_20.json`
- `screenshots/budget_panel_open_before_20.png`
- `raw/fresh_settings_before_budget_retry.txt`
- `raw/fresh_budget_panel_open_retry.txt`
- `raw/fresh_budget_panel_open_retry_inputs.json`
- `screenshots/fresh_budget_panel_open_retry.png`
- `raw/post_budget_keyboard_insert_save_attempt.txt`
- `screenshots/post_budget_keyboard_insert_save_attempt.png`

## Post-Change Evidence

- `raw/post_20_budget_all_campaigns_readback.txt`
- `screenshots/post_20_budget_all_campaigns_readback.png`
- `raw/post_20_budget_settings_hydrated_readback.txt`
- `screenshots/post_20_budget_settings_hydrated_readback.png`
- `raw/post_20_budget_product_groups_readback.txt`
- `screenshots/post_20_budget_product_groups_readback.png`
- `raw/post_20_budget_location_options_readback.txt`
- `screenshots/post_20_budget_location_options_readback.png`
- `raw/post_20_budget_bidding_guardrail_readback.txt`
- `raw/post_20_budget_bidding_guardrail_readback_inputs.json`
- `screenshots/post_20_budget_bidding_guardrail_readback.png`
- `raw/post_20_budget_change_history_readback.txt`
- `screenshots/post_20_budget_change_history_readback.png`

## Safety Notes

- Only the Standard Shopping budget was changed.
- Budget changed from `$1.00/day` to `$20.00/day`.
- Standard Shopping remains the only enabled campaign.
- PMax, Remarketing, and Brand Search remain paused.
- No credentials, cookies, request headers, payment data, or customer PII were written to this packet.
