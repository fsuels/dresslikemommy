# 2026-04-30 Standard Shopping Activation Gate

Generated: 2026-04-30 18:38 EDT

## Decision

`STANDARD_SHOPPING_ACTIVATION_GATE_PASSED_AWAITING_EXPLICIT_ENABLE_APPROVAL`

No campaign was enabled in this gate.

No budget was changed in this gate.

The exact activation candidate is:

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Current status: `Paused`
- Exact live budget: `$1.00/day`
- Activation action, if approved separately: change this campaign status from `Paused` to enabled while leaving budget at `$1.00/day`

## Required Gate Readback

### 1. Exact live budget

PASS.

Live Google Ads settings readback shows:

- Campaign status: `Paused`
- Budget: `$1.00/day`
- Campaign type: `Shopping`
- Network: `Google Search Network`
- Merchant Center/CSS: `124884876 - Dresslikemommy / CSS: Google Shopping (google.com/shopping)`
- Feed: `US (feed label)`

Evidence:

- `raw/standard_shopping_settings_live_activation_gate_expanded.txt`
- `screenshots/standard_shopping_settings_live_activation_gate_expanded.png`

### 2. Conversion action

PASS.

The campaign setting is `Conversion goals: Account-default`. The verified primary purchase conversion action for the account is:

- Conversion action: `Google Shopping App Purchase`
- Action optimization: `Purchases, Primary action`
- Value setting: `Use different values. If there's no value, use 0.`
- Source: `Website`
- Count: `Every conversion`
- Attribution: `Data-driven`
- Enhanced conversions: enabled, managed through Google Tag

Paid-value measurement gate already passed on order `6575644803169` with `value=19.99`, `currency=USD`, and transaction/order id deduplication captured in Google Ads and GA4 requests.

Evidence:

- `raw/google_ads_purchase_conversion_action_live_activation_gate.txt`
- `screenshots/google_ads_purchase_conversion_action_live_activation_gate.png`
- `../2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`

### 3. Merchant Center eligibility

PASS for this controlled Standard Shopping cohort.

Live Merchant Center label RPC readback for account `124884876` passed:

- `custom_label_0=paid_eligible`
- `custom_label_4=us_test_ready`
- `full_label_gate_status=PASS_ALL_EXPECTED_LABELS_VISIBLE`
- Observed US/en sample row last updated: `2026-04-29T22:53:29+00:00`

The local paid cohort proof still shows:

- `780` paid rows
- `81` Shopify products
- `81` Google & YouTube published products
- `780` available-for-sale variants
- `0` product issues
- `0` variant issues

Evidence:

- `raw/merchant_exact_label_readback_refresh_check.json`
- `raw/merchant_center_all_products_live_context_after_label_check.txt`
- `screenshots/merchant_center_all_products_live_context_after_label_check.png`
- `../2026-04-29-merchant-clean-label-upload/paid_label_active_status_live_shopify_check.json`
- `../2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`

### 4. Inventory filter and product-group readback

PASS.

Live campaign inventory filter readback:

- Filter enabled: `Advertise only products that match all of your requirements`
- Requirement 1: `Custom label 4 is us_test_ready`
- Requirement 2: `Custom label 0 is paid_eligible`
- Products matching filter: `780`

Live product-group readback:

- `All products`: parent row
- `us_test_ready`: `Automatic`
- `Everything else in "All products"`: `Excluded`

Evidence:

- `raw/standard_shopping_inventory_filter_live_activation_gate_expanded.txt`
- `raw/standard_shopping_inventory_filter_visible_controls.json`
- `screenshots/standard_shopping_inventory_filter_live_activation_gate_expanded.png`
- `raw/standard_shopping_product_groups_live_activation_gate.txt`
- `screenshots/standard_shopping_product_groups_live_activation_gate.png`

### 5. Bid guardrail

PASS.

Live bidding readback shows `Maximize clicks` with maximum CPC bid limit value `0.25`.

Evidence:

- `raw/standard_shopping_bidding_live_activation_gate_expanded.txt`
- `screenshots/standard_shopping_bidding_live_activation_gate_expanded.png`

### 6. Spend status

PASS.

Readback remains zero-delivery:

- Impressions: `0`
- Clicks: `0`
- Cost: `$0.00`
- Conversions: `0.00`
- Conversion value: `0.00`

Evidence:

- `raw/google_ads_all_campaigns_live_activation_readback.txt`
- `screenshots/google_ads_all_campaigns_live_activation_readback.png`
- `raw/standard_shopping_product_groups_live_activation_gate.txt`

## Rollback Requirement

Rollback trigger is documented in `ROLLBACK_TRIGGER.md`.

Immediate rollback action: pause `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, keep budget at `$1.00/day`, then re-check product groups, search terms, Merchant Center status, and purchase tracking.

## Explicit Enable Approval Required

This packet does not enable the campaign.

To approve activation, the owner must reply exactly:

`APPROVE ENABLE STANDARD SHOPPING AT $1.00/DAY NOW`

Only that approval authorizes changing `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` from paused to enabled. It does not authorize budget increases, PMax launch, Remarketing launch, or additional non-budget edits.

## Residual Risk

- Google Ads and Merchant Center reporting are not real-time.
- This campaign has no live performance history; the first run must be treated as a controlled test, not a scale launch.
- The broader Merchant Center catalog still has issues; the launch safety depends on the verified `780`-product filtered cohort and the excluded catch-all staying intact.
- Campaign conversion goals are account-default, so the account conversion setup must be watched for duplicate or newly primary actions after activation.
