# Google Shopping Shopify-Sold Product Retest - Paused Setup Final Readback

Date: 2026-05-21

Customer: `399-097-6848` / `dresslikemommy.com`

## Approval Used

`I approve creating the paused-ready Google Shopping Shopify-sold-products retest from the 2026-05-21 packet only: exact item IDs in google_ads_retest_candidate_item_scope_2026-05-21.csv, max CPC $0.15, daily cap $5, no PMax, no broad catchall, no Search Partners, no Display, no GA4 optimization, no Merchant/Shopify product/feed changes, and stop for readback before enabling spend.`

## Result

Paused-ready setup was created and read back. Spend was not enabled.

- Campaign: `DLM_US_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_20260521`
- Campaign ID: `23867953136`
- Campaign status: `PAUSED`
- Campaign primary status: `PAUSED`
- Channel: `SHOPPING`
- Bidding: `MANUAL_CPC`
- Budget: `$5/day` (`5,000,000` micros), paused
- Merchant ID: `124884876`
- Feed label: `US`
- Networks: Google Search `true`, Search Network `false`, Display/content `false`, Search Partners `false`
- Geo: United States (`geoTargetConstants/2840`)
- Ad group: `Shopify Sold Products Exact Item IDs 20260521`
- Ad group status: `PAUSED`
- Ad group max CPC: `$0.15` (`150,000` micros)
- Product ad status: `PAUSED`
- Listing groups: `21` total
- Included exact item-ID units: `19`
- Excluded catchall units: `1`
- Bad catchall units: `0`

## Spend Readback

May 21 readback:

- Retest campaign: `0` impressions / `0` clicks / `$0.00` cost
- Old Standard Shopping `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`: `PAUSED`, `0` impressions / `0` clicks / `$0.00` cost

## Validate-Only / Execution Notes

- First validate-only caught a malformed catchall encoding and failed before any write.
- Catchall was corrected to a true product-item "others" case.
- Second validate-only passed.
- Live mutate then created only the paused-ready setup.
- Final existing-readback validation passed.

## Guardrails

- No campaign was enabled.
- No spend was enabled.
- No Merchant, Shopify, product/feed, conversion-goal, billing, PMax, Search Partners, Display, broad catchall, GA4 optimization, or existing campaign write occurred.
- Enabling spend requires a separate fresh approval.

## Evidence Files

- Execution report: `GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_20260521T085320Z.md`
- Execution before JSON: `google_ads_shopify_sold_retest_before_20260521T085320Z.json`
- Execution after JSON: `google_ads_shopify_sold_retest_after_20260521T085320Z.json`
- Final network/readback report: `GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_20260521T085351Z.md`
- Final network/readback JSON: `google_ads_shopify_sold_retest_after_20260521T085351Z.json`
- Today metrics readback: `google_ads_shopify_sold_retest_today_metrics_readback_20260521.json`
- Scope CSV: `google_ads_retest_candidate_item_scope_2026-05-21.csv`

## Next Action

Stop here. If the owner wants to enable spend, get a separate fresh approval after reviewing this readback.
