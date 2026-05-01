# Standard Shopping $20/Day 48-Hour Monitoring And Rollback

Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`

Campaign ID: `23802638621`

Budget test start: 2026-04-30 19:09 EDT

Review / rollback due: 2026-05-02 19:09 EDT

## Normal End Of 48-Hour Test

At the deadline, do not let the budget continue by inertia.

Review performance and choose one explicit action:

- Restore budget to `$1.00/day`.
- Pause campaign.
- Continue at `$20.00/day` only with a new owner approval.
- Set a different budget only with a new owner approval.

## Immediate Rollback Triggers

Pause the campaign or restore budget to `$1.00/day` immediately if any of these occur:

- Spend appears outside `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- `Everything else in "All products"` becomes enabled or receives impressions/clicks.
- Merchant Center status for the paid cohort materially worsens.
- Purchase conversion tracking misses value, currency, or transaction id.
- Duplicate purchase counting appears for one order id.
- Clearly irrelevant Shopping search terms appear and cannot be controlled quickly.
- Non-US traffic appears despite presence-only targeting.
- Cost reaches `$20` with no qualified traffic or no useful search-term data.
- The owner asks to stop.

## First Checks

Check after first spend and again within 24 hours:

- Cost
- Clicks
- Impressions
- Search terms
- Product-group spend
- Conversions and conversion value
- Merchant Center item status for paid cohort
- CPC cap still `0.25`

## Scope Boundary

This budget test does not authorize:

- PMax launch
- Remarketing launch
- Brand Search launch
- Conversion-goal edits
- Product-scope expansion
- Budget above `$20.00/day`
