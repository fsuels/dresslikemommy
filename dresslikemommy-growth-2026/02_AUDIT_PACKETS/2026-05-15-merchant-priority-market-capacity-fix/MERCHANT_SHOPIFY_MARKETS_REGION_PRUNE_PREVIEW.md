# Merchant Shopify Markets Region Prune Preview

Mode: local/read-only preview from the sanitized Shopify Markets readback. No
Merchant, Shopify, Google Ads, Pinterest, feed, product, product-group, bid,
budget, status, capacity, billing, credential, or conversion writes were made.

## Purpose

The feed-group execution guard identifies the Merchant row groups to remove. This
region preview translates the likely Shopify Markets control surface into a
conservative first-pass checklist so the live operator does not disable a
priority market or remove products.

## Current Readback Shape

- Active market handles present: `australia, canada, eu, international, united-kingdom, us`.
- International market regions: `73`.
- First-pass high-confidence regions to remove from `International` only if the
  authenticated preview preserves priority markets: `52`.

## Region Buckets

| Bucket | Regions |
|---|---:|
| `HOLD_REVIEW_NOT_FIRST_PASS` | `19` |
| `PRESERVE_PRIORITY_OR_SEPARATE_MARKET` | `2` |
| `REMOVE_AFRICA` | `14` |
| `REMOVE_ASIA_MIDDLE_EAST` | `33` |
| `REMOVE_SOUTH_AMERICA` | `5` |

## Before-Save Rules

Use `shopify_international_region_prune_preview.csv` together with
`merchant_capacity_platform_preview_acceptance.csv` before any Save, Apply, Sync,
Upload, or equivalent live action:

1. Remove only regions classified as `REMOVE_ASIA_MIDDLE_EAST`, `REMOVE_AFRICA`,
   or `REMOVE_SOUTH_AMERICA` from the `International` publishing surface.
2. Do not remove the separate `United States`, `Canada`, `United Kingdom`,
   `Eurozone`, or `Australia` markets.
3. Do not remove `CA` or `AU` just because they appear inside `International`;
   treat duplicate coverage as a preview reconciliation issue, not a blind first
   pass.
4. Keep `HOLD_REVIEW_NOT_FIRST_PASS` and `UNKNOWN_HOLD_REVIEW` rows untouched in
   the first pass.
5. Do not delete Shopify products or change titles, variants, prices, inventory,
   vendors, product types, feed labels, campaigns, product groups, budgets, bids,
   statuses, or conversion settings.

Stop if the authenticated UI/API preview cannot show region-level changes that
preserve the priority market handles and reconcile to the Merchant feed-group
acceptance file.

## Files

- `shopify_international_region_prune_preview.csv`
- `shopify_international_region_prune_summary.json`
- `merchant_capacity_platform_preview_acceptance.csv`
