# Shopify International Region Prune Execution Report

Generated: 2026-05-15T07:07:28

Mode: `EXECUTED`.

Scope: bounded Shopify Markets publishing-scope cleanup. This removed only the approved first-pass non-priority `International` country regions from Shopify Markets. It did not delete products or change titles, prices, variants, inventory, vendors, product types, Merchant feeds, Google Ads, Pinterest, product groups, bids, budgets, statuses, conversions, billing, or credentials.

## Result

- International region count before: `73`.
- Requested first-pass remove regions: `52`.
- International region count after: `21`.
- Removed region count: `52`.
- Remaining selected remove codes: `0`.
- Unexpected removed codes: `0`.
- Protected duplicate `CA` and `AU` still present inside International: `AU, CA`.
- Required active markets still present: `australia, canada, eu, international, united-kingdom, us`.

## Removed Region Codes

`AC, AE, AM, AZ, BH, BN, BT, BW, CI, CL, CO, CV, EG, FK, GE, GS, HK, ID, IL, IN, IO, JO, JP, KG, KR, KW, KZ, LB, LK, MA, MN, MO, MU, MV, MY, OM, PE, PH, QA, SA, SC, SG, SH, ST, SZ, TA, TH, TN, TR, TW, VN, ZA`

## Evidence Files

- `shopify_markets_before_region_prune_sanitized.json`
- `shopify_markets_before_region_prune_sanitized.csv`
- `shopify_markets_after_region_prune_sanitized.json`
- `shopify_markets_after_region_prune_sanitized.csv`
- `shopify_international_region_prune_execution_summary.json`

## Decision Boundary

Before any Shopping build, re-export Merchant all-products/source eligibility and prove Canada English, Canada French, and GB English rows exist. If Merchant still shows zero rows after this Shopify Markets cleanup, treat that as a Google/YouTube channel publishing-sync blocker, not permission to build Shopping from stale or absent rows.
