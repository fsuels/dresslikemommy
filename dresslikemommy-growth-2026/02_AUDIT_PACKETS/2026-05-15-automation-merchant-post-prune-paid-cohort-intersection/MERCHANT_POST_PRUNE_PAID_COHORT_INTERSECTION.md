# Merchant Post-Prune Paid-Cohort Intersection

Generated: `2026-05-15T13:27:13.697805+00:00`

Mode: local/read-only saved-export join. No Google Ads, Merchant, Shopify, Pinterest, feed, product, campaign, bid, budget, status, conversion, billing, or credential write occurred.

## Inputs

- Merchant post-prune browser-RPC export: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-post-shopify-region-prune-export/merchant_all_products_browser_rpc_sanitized.csv`
- Exact paid cohort: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`
- Standard Shopping normalized product export: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-shopping-readonly-export-queue/standard_shopping_products_normalized_for_join.csv`
- Related guard reports: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_POST_SHOPIFY_REGION_PRUNE_READBACK.md` and `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`

## Result

- Exact paid cohort source has `780` item IDs; all `780` are still present somewhere in the Merchant post-prune export.
- Current US/en/USD Merchant rows contain `767` paid-cohort IDs.
- Current Standard Shopping export has `767` product IDs, and `767` map to current US/en/USD Merchant rows. Missing from US/en Merchant rows: `0`.
- The exact paid cohort still has `13` IDs absent from current US/en/USD Merchant rows; keep those out of any new live scope until a fresh row-level readback exists.
- US/es/USD has `772` paid-cohort IDs, but remains blocked by current issue/capacity evidence.
- Canada English, Canada French, GB English, and AU English still have `0` paid-cohort IDs in the post-prune Merchant export.
- Non-target market/language/currency groups still contain `51033` duplicate paid-cohort rows spanning `780` unique paid-cohort IDs.

## Decision

- `US/en` Standard Shopping: hold with evidence. The current campaign export reconciles to current Merchant US/en rows, but produced `$14.17` cost, `65` clicks, and `$0.00` conversion value in the saved export, so no feed/title/product-group/bid/budget/status write is justified by this intersection alone.
- `US/es`: do not repair from row presence alone. It still needs issue/capacity clearance or a narrow owner-approved repair/capacity action.
- `CA/en`, `CA/fr`, `GB/en`, `AU/en`: Shopping remains blocked. Do not create Shopping campaigns or product groups until Merchant rows exist and the capacity after-export guard passes.
- Merchant capacity: the paid cohort is still duplicated across non-target markets, proving the next unblock must be Merchant/Google publishing-scope control or delayed propagation readback, not another Shopify region-only prune and not campaign expansion.

## Outputs

- `merchant_post_prune_paid_cohort_by_market.csv`
- `merchant_post_prune_top_non_target_paid_cohort_groups.csv`
- `merchant_post_prune_us_en_paid_cohort_gaps.csv`
- `merchant_post_prune_paid_cohort_intersection_summary.json`
