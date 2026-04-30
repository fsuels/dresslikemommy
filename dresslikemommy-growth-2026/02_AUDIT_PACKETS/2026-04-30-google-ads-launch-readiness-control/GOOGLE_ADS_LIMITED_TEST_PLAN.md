# Limited Google Ads Test Plan

This is the activation plan after the paid-value gate passes. It is not approval to enable today.

## First Campaign To Run

Use `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` as the first controlled paid test after the gate passes.

Reason: Standard Shopping gives more product/query control than PMax. PMax should not be the first live spend while measurement, feed, and product economics are still being proven.

## Launch Conditions

- Paid Google Ads purchase value proof passes.
- Only `paid_eligible` + `us_test_ready` products are included.
- All catch-all product groups are excluded.
- Campaign remains US Presence-only.
- Search partners are disabled if the current UI allows it for this campaign.
- Bidding is controlled with manual CPC or capped click bidding, not uncapped traffic buying.
- Starting daily budget is explicitly approved and must fit the current marketing cap.
- Rollback rule is written before enabling.

## Initial Guardrails

- Start with one campaign only.
- Do not run PMax at the same time as the first Standard Shopping test.
- Do not enable Remarketing until policy and audience gates pass.
- Do not enable Brand Search until its brand-only controls, bid cap/manual bidding, and homepage/asset review are verified.
- Do not raise any campaign above the owner-approved first-test budget.

## First 24-Hour Monitoring

Check every 2-4 hours on launch day:

- Cost today
- Clicks
- Average CPC
- Search terms / product terms where available
- Product spend concentration
- Conversions
- Conversion value
- ROAS
- CPA/CAC
- Any product or policy warning

Pause immediately if spend occurs without clean conversion-value reporting, if product scope leaks outside the paid-ready cohort, or if CPA/CAC violates the approved threshold.
