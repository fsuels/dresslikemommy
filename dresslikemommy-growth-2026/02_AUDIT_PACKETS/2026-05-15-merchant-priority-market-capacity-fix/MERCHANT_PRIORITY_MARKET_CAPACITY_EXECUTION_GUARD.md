# Merchant Priority Market Capacity Execution Guard

Mode: local/read-only guardrail for the Merchant capacity cleanup lane. No Merchant,
Shopify, Google Ads, Pinterest, feed, product, product-group, bid, budget, status,
capacity, billing, credential, or conversion writes were made.

## Purpose

The live capacity cleanup may proceed only if an authenticated platform preview can
match the exact non-priority removal groups from the packet and preserve the priority
USA English and USA Spanish groups. This guard converts the packet into runnable
acceptance criteria so the future live operator does not remove the wrong market.

## Current Before-State

- Current all-products rows: `351007`.
- Expected first-pass removal rows: `199684`.
- Expected after-removal row floor if only this first pass is removed: `151323`.
- Candidate group count: `41`.
- Protected USA English rows: `5491`.
- Protected USA Spanish rows: `5412`.
- Canada English rows now: `0`.
- Canada French rows now: `0`.
- GB English rows now: `0`.

## Removal Buckets

| Bucket | Rows |
|---|---:|
| REMOVE_ASIA_MIDDLE_EAST | `129112` |
| REMOVE_AFRICA | `37511` |
| REMOVE_SOUTH_AMERICA | `8818` |
| REMOVE_NON_US_USD_REVIEW_FIRST | `24243` |

## Before-Save Acceptance Criteria

Use `merchant_capacity_platform_preview_acceptance.csv` against the authenticated
Merchant/Shopify/Google publishing control surface before any Save, Apply, Sync, or
Upload:

1. Every `remove_exact_group` row is selected only for removal or disablement from
   Google/Merchant publishing scope.
2. `US|en|USD` and `US|es|USD` remain enabled and unselected for removal.
3. Europe-later groups are not part of the first pass.
4. Canada English/French and GB English are not treated as ready; current export rows
   are `0`, so they require enablement and a fresh export after capacity cleanup.
5. The action is market/feed-country publishing cleanup only, not product deletion.

Stop if the platform preview cannot be reconciled to the CSV.

## After-Export Validation

Run this guard again with `--after-export /path/to/fresh_export.csv` after the live
cleanup. It will fail closed if any first-pass removal group remains or if USA
English/Spanish row counts drop below the current before-state.

After-export validation: `FAILED`. Remaining removal rows: `199684`. Protected failures: `0`.

## Files

- `merchant_capacity_platform_preview_acceptance.csv`
- `merchant_capacity_execution_guard_summary.json`
- `merchant_capacity_removal_candidate_groups.csv`
- `merchant_priority_market_capacity_fix_summary.json`
