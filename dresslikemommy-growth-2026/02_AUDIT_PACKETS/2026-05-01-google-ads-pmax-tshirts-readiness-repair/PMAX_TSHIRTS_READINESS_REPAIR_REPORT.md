# PMax USA Google Shopping T-Shirts Readiness Repair

Confidence: H for local paid-cohort/economics proof; M for live activation readiness because no just-in-time Google Ads/Merchant UI edits or readbacks were allowed in this scope.

## Scope

Campaign: `PMax: USA Google Shopping T-Shirts` / campaign ID `18154132284`.

Allowed action: local-only repair packet. No live campaign, Merchant Center, feed, Shopify Admin, budget, product-scope, asset, audience, conversion-goal, or status changes were made.

## What Was Fixed Locally

- Replaced the broken old draft final URL. `https://www.dresslikemommy.com/collections/matching-t-shirts` returned 404, so the repaired packet uses the live product URL `https://www.dresslikemommy.com/products/family-matching-t-shirt-set-with-colorful-heart-brushstroke-design`, which returned HTTP 200 during this pass.
- Built a strict clean T-shirt cohort from the existing paid-ready Standard Shopping cohort export, instead of using mixed dresses/shorts/overalls rows from the old PMax readback.
- Confirmed the clean cohort has `42` paid-ready variant rows across `1` product: `7229259874401`.
- Confirmed all clean rows are `paid_eligible` + `us_test_ready`, Online Store published, Google & YouTube published, in stock, and have unit cost present.
- Confirmed the clean cohort price range is `$17.99` to `$21.99`, unit-cost range is `$9.00` to `$11.00`, and gross-margin percent is about `49.97%` to `49.98%` under the operator 50% all-in cost assumption.
- Created claim-safe final asset copy with unsupported claims removed: no `free delivery`, `factory low prices`, `largest selection`, `top quality`, or mixed `dresses/swimsuits/general outfits` copy.
- Added a search-theme, audience-signal, URL-control, and brand-exclusion plan.
- Added an activation checklist that keeps live PMax blocked until owner approval plus just-in-time readbacks.

## Key Files

- `pmax_tshirts_clean_cohort_review_only.csv` - exact clean item IDs for a micro PMax T-shirt scope.
- `pmax_tshirts_clean_product_summary.csv` - product-level proof for the clean scope.
- `pmax_tshirts_rejected_mixed_scope_products.csv` - shirt/T-shirt-like products rejected from this PMax because they are mixed, not T-shirt-only, or not clean.
- `pmax_tshirts_asset_copy_final_review_only.csv` - final claim-safe copy to use only after approval.
- `pmax_tshirts_search_theme_audience_url_plan.csv` - search themes, audience signals, URL control, and brand-exclusion plan.
- `pmax_tshirts_activation_gate_checklist.md` - live gate checklist.
- `pmax_tshirts_clean_cohort_summary.json` - machine-readable summary.

## Decision

`PMAX_TSHIRTS_LOCAL_REPAIR_PACKET_READY_LIVE_CHANGES_BLOCKED_PENDING_OWNER_APPROVAL`.

The campaign should stay paused. This packet makes the T-shirts path concrete enough for owner review, but it does not authorize upload, unpause, enable, budget changes, Merchant/feed changes, Shopify product edits, or conversion-goal changes.

## Residual Risks

- The clean cohort is a micro-test only: one product and `42` variants. That is safer than the old mixed scope, but may be too narrow for PMax learning.
- The active Standard Shopping campaign may already cover these paid-ready item IDs; avoid overlapping spend unless the owner explicitly accepts it after the Standard Shopping review.
- Final URL expansion, brand exclusions, asset strength, campaign budget, and product scope still require live Google Ads readback before any launch.
- Product and Merchant Center status can change after this local export; rerun a just-in-time readback before any live action.

## Suggested Approval Phrase For A Future Live Upload Gate

`APPROVE PREPARE PMAX T-SHIRTS MICRO TEST UPLOAD ONLY; KEEP CAMPAIGN PAUSED; USE ONLY THE REVIEWED CLEAN T-SHIRT COHORT; NO BUDGET, CONVERSION GOAL, OR MERCHANT FEED CHANGES`

A separate enable phrase would still be required after upload/ad review/readback.
