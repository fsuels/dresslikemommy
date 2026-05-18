# Gate B-1 Unified Pinterest Feed Readback

Generated: 2026-05-17 11:42 EDT

Mode: owner-approved Gate B-1 only. Read-only Shopify Admin GraphQL fetches plus local repo evidence generation. No Shopify product, channel, feed, theme, app-proxy, or Admin setting write. No Pinterest catalog/source/product-group/campaign/budget/bid/status/tag/CAPI/audience/billing write. No Merchant, Google Ads, GA4/GTM, order/payment, credential, or destructive filesystem write.

## Approval Scope Used

Owner approved the Gate B-1 step from `PATH_B_PRIMARY_FIX_PLAN.md`: generate the Pinterest unified feed locally for read-back only, run `ops/scripts/generate_pinterest_feed_grouped.py` read-only for every active Shopify Market (`us`, `canada`, `united-kingdom`, `eu`, `australia`, `international`), then merge with country/language audit columns. Output stays in the repo evidence folder only.

## What Changed Locally

- Added `ops/scripts/build_pinterest_unified_feed.py`.
- Regenerated the six per-market grouped TSV feeds.
- Created:
  - `feeds/pinterest_unified_all_markets.tsv`
  - `feeds/pinterest_unified_all_markets.summary.json`
  - `feeds/pinterest_unified_all_markets.sha256`

## Unified Feed Result

| Metric | Result |
|---|---:|
| Unified rows | 41,814 |
| Unique item IDs | 41,814 |
| Duplicate item IDs | 0 |
| Missing `item_group_id` | 0 |
| Missing `image_link` | 0 |
| Parent groups with multiple `image_link` values inside the same market | 0 |
| Supplier/source host hits | 0 |
| SHA-256 | `8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7` |

Per-market rows:

| Market | Country audit column | Language audit column | Rows | Unique parent groups |
|---|---|---|---:|---:|
| `us` | `US` | `en` | 6,969 | 326 |
| `canada` | `CA` | `en` | 6,969 | 326 |
| `united-kingdom` | `GB` | `en` | 6,969 | 326 |
| `eu` | blank aggregate-market marker | `en` | 6,969 | 326 |
| `australia` | `AU` | `en` | 6,969 | 326 |
| `international` | blank aggregate-market marker | `en` | 6,969 | 326 |

The blank `country` values for `eu` and `international` are intentional in Gate B-1. Those Shopify Markets are aggregate surfaces, not one Pinterest target country. Gate B-3 must decide exact Pinterest source/market mapping before any live import.

## Commands Run

```bash
python3.13 ops/scripts/build_pinterest_unified_feed.py
python3.13 -m py_compile ops/scripts/build_pinterest_unified_feed.py ops/scripts/generate_pinterest_feed_grouped.py ops/scripts/check_pinterest_feed_grouping.py
python3.13 ops/scripts/check_pinterest_feed_grouping.py --report-only --strict
python3.13 ops/scripts/check_continuity_integrity.py --strict
```

## Verification

- `build_pinterest_unified_feed.py` regenerated all six per-market feeds and produced the unified feed with all internal guards passing.
- Compile check passed for the new builder and related Pinterest feed scripts.
- Pinterest feed grouping guard now scans `10` snapshots: `7` generated Path B feeds PASS (`6` per-market plus unified), while the `3` upstream/live-equivalent snapshots remain expected FAIL / `0` ERROR.
- Continuity integrity passed with `CONTINUITY_OK`; `pinterest_feed_grouping` remains in fix-in-progress mode because live upstream snapshots still fail and the freshness marker is not attested.

## Decision

Gate B-1 is complete locally. This is not live upload authority and not a Pinterest launch unblock by itself.

Next gated step is Gate B-2: use `GATE_B2_B3_APPROVAL_PACKET.md` to approve the Shopify app-proxy/file-hosting implementation for `https://www.dresslikemommy.com/apps/<proxy_handle>/pinterest-feed.tsv`. Do not deploy the proxy, configure Pinterest catalog source, pause legacy feeds, or attest `FIX_LANDED_FRESHNESS_MARKER.txt` without a fresh exact approval and readback plan.
