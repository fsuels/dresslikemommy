# 2026-04-30 Standard Shopping Activation Execution

Executed: 2026-04-30 18:51 EDT

## Approval

Owner approval received exactly:

`APPROVE ENABLE STANDARD SHOPPING AT $1.00/DAY NOW`

## Action Taken

Enabled only this campaign:

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Budget left unchanged: `$1.00/day`

No other campaign was enabled.

No budget was increased.

No PMax, Remarketing, Brand Search, or conversion-goal edit was made.

## Post-Enable Readback

### Campaign table

PASS.

- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`: `Eligible`
- Budget: `$1.00/day`
- Type: `Shopping`
- Cost: `$0.00`
- Impressions: `0`
- Clicks: `0`
- Conversions: `0.00`
- Conversion value: `0.00`

Other campaigns remain paused:

- `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`: `Paused`
- `PMax: Shopping ads (United States)`: `Paused`
- `PMax: USA Google Shopping T-Shirts`: `Paused`
- `Remarketing - Cart Abandoners & Checkout Starters`: `Paused`

Evidence:

- `raw/post_enable_all_campaigns_final_readback.txt`
- `screenshots/post_enable_all_campaigns_final_readback.png`

### Campaign settings

PASS.

- Campaign status: `Enabled`
- Budget: `$1.00/day`
- Merchant Center/CSS: `124884876 - Dresslikemommy / CSS: Google Shopping (google.com/shopping)`
- Feed: `US (feed label)`
- Conversion goals: `Account-default`
- Bidding: `Maximize clicks`
- Location: `United States (country)`
- Network: `Google Search Network`
- Inventory filter: `Advertise only products that match all of your requirements`

Evidence:

- `raw/post_enable_settings_final_readback.txt`
- `screenshots/post_enable_settings_final_readback.png`

### Location option

PASS.

Live location panel shows:

- `United States` checked
- `Presence: People in or regularly in your included locations` checked

Evidence:

- `raw/post_enable_location_options_live_check.txt`
- `screenshots/post_enable_location_options_live_check.png`

### Ad group and product groups

PASS.

- Ad group `Ad group 1`: `Eligible`
- Product group `us_test_ready`: `Automatic`
- Product group `Everything else in "All products"`: `Excluded`

Evidence:

- `raw/post_enable_ad_groups_readback.txt`
- `screenshots/post_enable_ad_groups_readback.png`
- `raw/post_enable_product_groups_readback.txt`
- `screenshots/post_enable_product_groups_readback.png`

### Bid guardrail

PASS.

`Maximize clicks` maximum CPC bid limit still reads back as `0.25`.

Evidence:

- `raw/post_enable_bidding_guardrail_readback.txt`
- `screenshots/post_enable_bidding_guardrail_readback.png`

## Change History

Captured change history immediately after activation. The campaign row already reads `Eligible`; the status-change row may lag in Google Ads change history.

Evidence:

- `raw/post_enable_change_history_readback.txt`
- `screenshots/post_enable_change_history_readback.png`

## Rollback Trigger

Rollback remains governed by `ROLLBACK_TRIGGER.md`.

Immediate rollback action: pause `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, leave budget at `$1.00/day`, and re-check product groups, Merchant Center eligibility, search terms, and purchase measurement.

## Decision

`STANDARD_SHOPPING_ENABLED_CONTROLLED_TEST_ACTIVE_AT_1_USD_PER_DAY`

This is a controlled test, not a scale launch.
