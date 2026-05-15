# Pinterest Feed Grouping Queue Wiring Readback

Generated: 2026-05-15 09:45 EDT

Mode: repo-local/read-only automation follow-up. No Shopify, Pinterest,
Merchant, Google Ads, GA4/GTM, theme, billing, product, feed, source, tag,
CAPI, audience, campaign, budget, bid, status, or credential write occurred.

## What Was Executed

- Read the latest all-markets Pinterest feed grouping packet and freshness
  marker.
- Ran the automated feed grouping guard in report-only strict mode:

```bash
python3.13 ops/scripts/check_pinterest_feed_grouping.py --report-only --strict
```

## Readback

The guard scanned `3` current snapshots and returned the expected fix-in-progress
diagnostic state:

- `3` FAIL snapshots.
- `0` ERROR snapshots.
- Failing snapshots:
  - `pinterest_exact_product_group_item_id_import.csv`: `30` duplicate parent
    clusters without `item_group_id`.
  - `merchant_all_products_browser_rpc_sanitized.csv` from the post-prune
    Merchant export: `69` market x language buckets with duplicate parents,
    worst `96x`.
  - `merchant_all_products_browser_rpc_sanitized.csv` from the source
    eligibility export: `69` market x language buckets with duplicate parents,
    worst `96x`.

The `FIX_LANDED_FRESHNESS_MARKER.txt` file is a placeholder and does not include
the strict attest phrase. The continuity guard therefore remains in
fix-in-progress mode until per-market after-state readbacks prove the live feed
is grouped.

## Decision

Pinterest launch/readback cannot be treated as only a product-count delay. The
underlying feed schema still submits variants as standalone catalog rows without
`item_group_id`, across all markets and categories. The next sales-moving action
is owner-approved Shopify Pinterest channel grouping for all markets, or Path B
grouped TSV generation/import under a separate exact approval if the channel UI
does not expose the grouping toggle.

## Next Valid Action

Owner approves either the master all-markets phrase in
`MASTER_ALL_MARKETS_APPROVAL_PHRASE.md` or one per-market phrase under
`per_market_packets/`. After the live channel re-sync, capture the per-market
after-state readback and replace the marker contents with the required attest
line only when strict guard mode can pass.
