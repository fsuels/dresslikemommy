# Google Ads Paused Standard Shopping Build Plan

Status: review-only. Do not create or enable campaigns from this file without explicit owner approval.

Launch decision: `LAUNCH_BLOCKED`

## Campaign

- Campaign name: `US | Standard Shopping | Clean Subset | Paid Eligible | Test`
- Campaign type: Shopping
- Subtype: Standard Shopping only
- Merchant Center: Dresslikemommy / `124884876`
- Country: United States
- Inventory filter:
  - `custom_label_0 = paid_eligible`
  - `custom_label_4 = us_test_ready`
- Status: Paused
- Budget: tiny placeholder only, keep paused
- Bidding: conservative Manual CPC or equivalent low-risk bidding
- Networks: Google Search Network only if appropriate; do not enable Search Partners unless explicitly approved

## Product Groups

- Subdivide by `custom_label_2` product family.
- Then subdivide by `custom_label_1` margin tier.
- Include only rows where `paid_eligible = TRUE`.
- Exclude everything else.

## Explicit Exclusions

- Performance Max
- broad Search
- Display
- Dynamic Search Ads
- international campaigns
- all-products Shopping
- unknown-margin products
- products with feed issues
- products with PDP issues
- products not marked `paid_eligible = TRUE`

## Current Review Counts

- Total variants reviewed: 7324
- Merchant Center products matched with evidence: 0
- `paid_eligible = TRUE`: 0
- `fix_before_paid = TRUE`: 7324
- excluded/not eligible rows: 7324

## Gate

- If fewer than 20 clean products pass, keep `LAUNCH_BLOCKED`.
- If products pass but tracking/PDP/feed evidence still needs review, use `READY_FOR_PAUSED_BUILDOUT` only.
- Use `READY_FOR_LIMITED_TEST` only after measurement, feed status, margin, PDP, shipping, and return policy all pass.
