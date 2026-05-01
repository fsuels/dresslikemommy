# Standard Shopping Rollback Trigger

Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`

Campaign ID: `23802638621`

Approved test budget, if enabled later: `$1.00/day`

## Immediate Rollback Action

Pause the campaign immediately.

Leave the budget at `$1.00/day`.

Do not switch to PMax, Target ROAS, Maximize conversion value, or a higher budget during rollback.

## Rollback Triggers

Pause immediately if any of these happen:

- Spend occurs outside the verified `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible` inventory filter.
- `Everything else in "All products"` becomes enabled or starts receiving impressions/clicks.
- Merchant Center status for the paid cohort shows a material limited/not-approved spike.
- Purchase conversion requests stop sending value, currency, or transaction id.
- Duplicate purchase counting appears for the same order id.
- Cost reaches the daily budget without qualified Shopping traffic.
- Any non-US traffic is observed after the presence-only location setting.
- Search terms show clearly irrelevant traffic that cannot be blocked quickly with a narrow negative.
- The owner asks to stop the test.

## First-Day Monitoring

Check after first spend and again within 24 hours:

- Campaign status and budget remain `Enabled` and `$1.00/day` only if owner explicitly approved.
- Product groups still show `us_test_ready` active and catch-all excluded.
- Cost, clicks, impressions, conversions, and conversion value.
- Merchant Center item status for the paid cohort.
- Google Ads purchase action still uses value/currency and no duplicate order ids.

## Allowed Rollback Scope

Allowed without further approval:

- Pause `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
- Save screenshots/text exports proving the rollback.
- Add a narrowly scoped negative keyword only if live search terms show obvious waste and the campaign remains paused afterward.

Not allowed without separate approval:

- Increase budget.
- Enable another campaign.
- Enable PMax or Remarketing.
- Change conversion goals.
- Expand product scope beyond the verified filtered cohort.
