# Google Ads Paused Standard Shopping Build Plan

Status: dry-run/review-only. Do not create, enable, or restart Google Ads from this file.

Launch decision: `READY_FOR_PAUSED_BUILDOUT`

This launch decision is a local file state only. It is not approval to restart Google Ads.

## Post-Gate Google Ads Structure

Do not restart Google Ads yet. Use this structure only after each named gate passes.

| Campaign | Use only after | Required exclusions |
| --- | --- | --- |
| Brand Search — USA | Purchase conversion tracking records value correctly. | Exclude if tracking is not recording. |
| Standard Shopping — USA eligible products | Merchant Center and product-margin gates pass. | Exclude UNKNOWN_MARGIN, FIX_BEFORE_PAID, limited, and not-approved products. |
| PMax — USA eligible products | Only after feed, conversion, landing-page, and product-label gates pass. | URL expansion off unless an approved landing-page map exists. |
| Non-brand Search | Search Console query/page exports prove commercial opportunity. | Exclude pages not READY_FOR_PAID. |
| Remarketing | Policy-limited ads are fixed and tracking is deduped. | Do not use current limited ads. |

## Standard Shopping Dry-Run Campaign

- Campaign name: `US | Standard Shopping | Clean Subset | Paid Eligible | Test`
- Campaign type: Shopping
- Subtype: Standard Shopping only
- Merchant Center: Dresslikemommy / `124884876`
- Country: United States
- Inventory filter:
  - `custom_label_0 = paid_eligible`
  - `custom_label_4 = us_test_ready`
- Pre-build prerequisite: those custom labels must already be uploaded and verified in Merchant Center; otherwise use the local review files only
- Status: Paused
- Budget: tiny placeholder only, keep paused
- Bidding: conservative Manual CPC or equivalent low-risk bidding
- Networks: Shopping inventory only; do not add Search Partners, Display, PMax, non-brand Search, or remarketing without their gates

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
- `UNKNOWN_MARGIN`
- `FIX_BEFORE_PAID`
- Merchant Center `Limited` products
- Merchant Center `Not approved` products
- products with feed issues
- products with PDP issues
- products not marked `paid_eligible = TRUE`
- pages not marked `READY_FOR_PAID`

## Current Review Counts

- Total variants reviewed: 7324
- Merchant Center products matched with evidence: 7324
- `paid_eligible = TRUE`: 780
- `fix_before_paid = TRUE`: 6544
- excluded/not eligible rows: 6544

## Gate

- If fewer than 20 clean products pass, keep `LAUNCH_BLOCKED`.
- If products pass but tracking/PDP/feed evidence still needs review, use `READY_FOR_PAUSED_BUILDOUT` only.
- Use `READY_FOR_LIMITED_TEST` only after measurement, feed status, margin, PDP, shipping, and return policy all pass.
