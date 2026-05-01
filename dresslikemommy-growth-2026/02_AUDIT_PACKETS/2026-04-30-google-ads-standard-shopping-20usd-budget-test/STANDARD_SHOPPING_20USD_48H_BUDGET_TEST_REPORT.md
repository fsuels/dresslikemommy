# 2026-04-30 Standard Shopping $20/Day 48-Hour Budget Test

Generated: 2026-04-30 19:09 EDT

## Approval

Owner approval received exactly:

`APPROVE RAISE STANDARD SHOPPING TO $20/DAY FOR 48 HOURS`

## Action Taken

Changed only this campaign budget:

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Before budget: `$1.00/day`
- After budget: `$20.00/day`
- Campaign status remained: `Eligible`

No other campaign was enabled.

No PMax, Remarketing, Brand Search, conversion-goal, location, product-group, or bid-strategy edit was made.

## 48-Hour Window

Start: 2026-04-30 19:09 EDT

Review / rollback due: 2026-05-02 19:09 EDT

Google Ads account time equivalent: approximately 2026-05-02 16:09 PDT.

## Spend Guardrail

Average daily budget: `$20.00/day`.

Google Ads can overdeliver on a given day, so the practical short-window exposure can be higher than exactly `$20` per calendar day. Treat the first 48 hours as a monitored controlled test, not an unattended scale launch.

The CPC cap remains `0.25`, so the budget change increases volume without removing the per-click guardrail.

## Post-Change Readback

### Campaign table

PASS.

- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`: `Eligible`
- Budget: `$20.00/day`
- Type: `Shopping`
- Cost: `$0.00`
- Impressions: `0`
- Clicks: `0`
- Conversions: `0.00`
- Conversion value: `0.00`

Other campaigns remain paused at `$1.00/day`:

- `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`
- `PMax: Shopping ads (United States)`
- `PMax: USA Google Shopping T-Shirts`
- `Remarketing - Cart Abandoners & Checkout Starters`

Evidence:

- `raw/post_20_budget_all_campaigns_readback.txt`
- `screenshots/post_20_budget_all_campaigns_readback.png`

### Hydrated campaign settings

PASS.

- Campaign status: `Enabled`
- Budget: `$20.00/day`
- Merchant Center/CSS: `124884876 - Dresslikemommy / CSS: Google Shopping (google.com/shopping)`
- Feed: `US (feed label)`
- Conversion goals: `Account-default`
- Bidding: `Maximize clicks`
- Location: `United States (country)`
- Network: `Google Search Network`
- Inventory filter: `Advertise only products that match all of your requirements`

Evidence:

- `raw/post_20_budget_settings_hydrated_readback.txt`
- `screenshots/post_20_budget_settings_hydrated_readback.png`

### Location option

PASS.

Live location panel still shows:

- `United States` checked
- `Presence: People in or regularly in your included locations` checked

Evidence:

- `raw/post_20_budget_location_options_readback.txt`
- `screenshots/post_20_budget_location_options_readback.png`

### Product groups

PASS.

- Product group `us_test_ready`: `Automatic`
- Product group `Everything else in "All products"`: `Excluded`
- Cost: `$0.00`

Evidence:

- `raw/post_20_budget_product_groups_readback.txt`
- `screenshots/post_20_budget_product_groups_readback.png`

### Bid guardrail

PASS.

`Maximize clicks` maximum CPC bid limit still reads back as `0.25`.

Evidence:

- `raw/post_20_budget_bidding_guardrail_readback.txt`
- `raw/post_20_budget_bidding_guardrail_readback_inputs.json`
- `screenshots/post_20_budget_bidding_guardrail_readback.png`

## Failed Save Attempts

Two first attempts set the visible input but did not save because the budget panel was partially offscreen/stale. Live campaign readback stayed at `$1.00/day` during those attempts. The final successful edit used a fresh settings page, real text insertion into the budget field, and a visible save control.

## Decision

`STANDARD_SHOPPING_20_USD_PER_DAY_48H_CONTROLLED_TEST_ACTIVE`

## Required Review

At or before 2026-05-02 19:09 EDT:

1. Read cost, clicks, impressions, search terms, conversions, and conversion value.
2. Confirm product groups still restrict spend to `us_test_ready`.
3. Confirm Merchant Center paid cohort remains eligible.
4. Confirm purchase conversion requests still carry value, currency, and transaction id.
5. Decide whether to return budget to `$1.00/day`, pause, continue at `$20/day`, or revise the test.
