# Product / Feed Implementation Plan Recheck

Generated: 2026-04-29 03:55 EDT

## Phase Status

| Phase | Status | Evidence | Remaining fix |
| --- | --- | --- | --- |
| 1. Reconcile Shopify, Merchant Center, and Pinterest product IDs/counts | Partial | `shopify_merchant_variant_map.csv` maps 7,324 active Shopify variants to `shopify_US_<product_id>_<variant_id>` Merchant Center IDs. Merchant clean-label upload has 5,933 matched rows and excludes 1,391 stale/unmatched Merchant offers. | Pinterest item-level product IDs were not available from local exports, so those map cells are marked `NEEDS_PINTEREST_CATALOG_ITEM_EXPORT`. |
| 2. Backfill COGS/unit cost for UNKNOWN_MARGIN active variants | Fixed | Current read-only Shopify Admin check shows 7,324 active variant rows, 0 missing unit costs, and 0 updates needed. | None for active variants. |
| 3. Fix feed defects: unit cost, GTIN/barcode, SKU, image dimensions, size, color, gender, age_group | Partial | Paid cohort has 780/780 PASS for image, price, availability, shipping, and returns, with 0 missing SKU and 0 missing GTIN/barcode. Pinterest compare-at, long description, and one category issue were previously fixed and rechecked. | Across all 7,324 reviewed active rows, 1,604 still have missing SKU and 5,897 still have missing GTIN/barcode; these are excluded from paid eligibility rather than guessed. Current Merchant diagnostics still show broad catalog issues including over-capacity, missing gender, and missing size. |
| 4. Apply proposed custom labels and read back before campaign filters | Partial | Live Merchant Center readback now shows `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready` for the sampled US/en paid offer, so the two campaign filters are visible. | `custom_label_1..3` still read back as old product-level values (`set`, `true`, `summer`) instead of `margin_medium`, `mommy_me`, `aov_medium`; do not subdivide campaigns by labels 1-3 yet. |
| 5. Align shipping/returns feed settings with storefront policies | Mostly fixed for paid cohort | Storefront policy cleanup removed contradictory FAQ/shipping/return/about text. Clean Shopping paid cohort has 780/780 PASS for shipping and return policy evidence. | Merchant Center shipping/returns settings still need a fresh settings-level readback; the current proof is storefront plus item-level paid-cohort evidence. |

## Current Campaign Gate

Decision: `READY_FOR_PAUSED_CAMPAIGN_FILTER_BUILD__DO_NOT_SUBDIVIDE_BY_LABEL_1_2_3`

This does not approve enabling or restarting Google Ads. It means a paused Standard Shopping build can use only the verified filters:

- `custom_label_0=paid_eligible`
- `custom_label_4=us_test_ready`

Do not use `custom_label_1`, `custom_label_2`, or `custom_label_3` for campaign/product-group subdivisions until the full-label readback passes.

## Files

- `merchant_exact_label_readback_refresh_check.json`
- `merchant_label_keyword_readback.json`
- `shopify_merchant_variant_map.csv`
- `../2026-04-29-product-feed-plan-active-cost-readonly_SHOPIFY_COST_SYNC_50PCT/summary.json`
- `../2026-04-29-google-shopping-campaign-gate/summary.json`
