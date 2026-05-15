# Merchant Capacity Live Control Surface Readback

Generated: 2026-05-15T07:14:36

Mode: read-only Shopify Admin GraphQL Markets readback. No Shopify, Merchant,
Google Ads, Pinterest, feed, product, product-group, bid, budget, status,
capacity, billing, credential, or conversion writes were made.

## Decision

The authenticated Shopify control surface no longer matches the older `73`
region readback. `International` currently has `21` regions,
and all `52` prior first-pass non-priority preview
regions are absent from `International`.

Because there were no matching first-pass remove regions left in Shopify
Markets, no duplicate or broader removal was performed.

## Current International Shape

| Bucket from prior preview | Regions currently in International |
|---|---:|
| `HOLD_REVIEW_NOT_FIRST_PASS` | `19` |
| `PRESERVE_PRIORITY_OR_SEPARATE_MARKET` | `2` |

## Merchant After-Export Result

The fresh authenticated Merchant RPC export still contains `351,007` rows. The
execution guard with `--after-export` failed because all `199,684` first-pass
Merchant removal rows are still present while USA English and USA Spanish stayed
protected.

This means Shopify Markets appears pruned, but Merchant/Google product rows have
not caught up or the Merchant row generator is controlled by a different Google
publishing surface.

## Files

- `shopify_markets_live_readback_current.json`
- `shopify_markets_live_region_reconciliation.csv`
- `merchant_capacity_execution_guard_summary.json`
- `MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`
