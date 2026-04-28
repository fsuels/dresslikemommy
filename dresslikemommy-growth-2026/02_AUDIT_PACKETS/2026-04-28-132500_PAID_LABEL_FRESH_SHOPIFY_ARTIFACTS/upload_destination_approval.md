# Paid Label Upload Destination Approval

Generated: 2026-04-28T13:32:42

## Recommended Destination

Use a Google Merchant Center supplemental feed keyed by Shopify item IDs
(`shopify_US_<product_id>_<variant_id>`) for paid-status labels.

Reason: the paid gate is variant-level. Shopify `mm-google-shopping.custom_label_*`
metafields are product-level in this store, and live `custom_label_4` currently
stores price tier. A supplemental feed can override or test paid-status labels
without mutating Shopify product metafields first.

## Prepared Upload Preview Files

- Full custom-label preview: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-132500_PAID_LABEL_FRESH_SHOPIFY_ARTIFACTS/merchant_center_supplemental_full_custom_labels.csv`
- Paid-status-only preview: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-132500_PAID_LABEL_FRESH_SHOPIFY_ARTIFACTS/merchant_center_supplemental_paid_status_only.csv`

## Approval Status

Destination approved for a future writeback: `merchant_center_supplemental_feed_paid_status_only`.

Prepared locally only. Not uploaded. No Shopify, Merchant Center, feed, or ads write was performed.

Rejected for this gate:

- `merchant_center_supplemental_feed_full_custom_labels` because it would also override existing non-paid labels.
- `shopify_product_metafields_mm-google-shopping` because those labels are product-level in this store and live `custom_label_4` currently stores price tier.

## Current Counts

- Active variant rows: 7324
- Paid status counts: {"EXCLUDE_PAID": 5910, "FIX_BEFORE_PAID": 1414}
- Gate reason counts: {"LOW_AOV_NO_BUNDLE_REPRICE_OR_COST_BASIS": 4, "OUT_OF_STOCK": 97, "UNKNOWN_COST_NO_RELIABLE_COST_BASIS": 5910}
