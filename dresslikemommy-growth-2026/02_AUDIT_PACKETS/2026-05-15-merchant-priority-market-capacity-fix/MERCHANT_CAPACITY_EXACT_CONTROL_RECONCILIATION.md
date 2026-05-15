# Merchant Capacity Exact-Control Reconciliation

Generated: 2026-05-15T07:17:00-04:00

Mode: authenticated read-only Shopify Admin GraphQL reconciliation. No Merchant,
Shopify, Google Ads, Pinterest, feed, product, product-group, bid, budget,
status, capacity, billing, credential, or conversion writes were made.

## Decision

- External write status: `NOT_EXECUTED`.
- Overall status: `SHOPIFY_REGION_SCOPE_PRUNED__MERCHANT_FEED_GROUP_GUARD_STILL_BLOCKED`.
- After-export guard status: `FAILED`.

The live Shopify Admin path is authenticated and exact for Shopify Markets
regions. Current readback shows the first-pass region scope is already pruned
from `International`, with priority/hold regions preserved. The fresh Merchant
after-export guard still fails, so Canada/GB Shopping remains blocked.

## Shopify Region Guard Preview

- Shopify Admin API version: `2026-04`.
- Active market handles seen: `australia, canada, eu, international, united-kingdom, us`.
- Market scopes present: `read_marketing_events, read_marketing_integrated_campaigns, read_markets, read_markets_home, write_marketing_events, write_marketing_integrated_campaigns, write_markets, write_markets_home`.
- Market mutations present: `customerEmailMarketingConsentUpdate, customerSmsMarketingConsentUpdate, marketCreate, marketDelete, marketLocalizationsRegister, marketLocalizationsRemove, marketUpdate, marketingActivitiesDeleteAllExternal, marketingActivityCreate, marketingActivityCreateExternal, marketingActivityDeleteExternal, marketingActivityUpdate, marketingActivityUpdateExternal, marketingActivityUpsertExternal, marketingEngagementCreate, marketingEngagementsDelete`.
- International live regions: `21`.
- Candidate first-pass remove regions still live: `0/52`.
- Protected duplicate/priority region codes preserved in preview: `AU, CA`.
- Region guard status: `LIVE_REGION_SCOPE_ALREADY_PRUNED_OUTSIDE_THIS_READBACK`.

## Merchant Feed-Group Guard Preview

- Exact feed-group removal rows required: `41`.
- Protected priority groups: `US|en|USD; US|es|USD`.
- Enable-after-cleanup rows: `CA|en|CAD=0_currently_absent; CA|fr|CAD=0_currently_absent; GB|en|GBP=0_currently_absent`.
- Non-US USD remove rows lacking country-exact Shopify region control: `5`.
- Merchant feed guard status: `BLOCKED_NO_EXACT_FEED_GROUP_CONTROL_PREVIEW`.

## Blocker

`merchant_capacity_platform_preview_acceptance.csv` requires exact
`feed_label` + `language_code` + `currency` publishing groups to show as selected
for removal or disabled from Google publishing scope before Save/Apply/Sync. The
authenticated Shopify Markets API can remove region conditions from
`International`, and the live region readback now shows those regions absent, but
it cannot prove the Merchant feed groups have been removed.

Therefore the exact-control reconciliation still fails closed for Shopping. The
after-export guard shows Merchant still has the first-pass removal rows, including
the non-US USD candidate rows.

## Next Valid Execution Path

Use a Merchant Center or Google & YouTube app control surface that can preview or
sync the exact rows in `merchant_capacity_platform_preview_acceptance.csv` by
`feed_label`, `language_code`, and `currency`. Only after that control/sync action
is reconciled, capture a fresh all-products export, then run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/build_merchant_capacity_execution_guard.py --after-export /path/to/fresh_export.csv
```

Canada/GB Shopping work remains blocked until that after-export guard passes.

## Files

- `shopify_markets_live_exact_region_readback.csv`
- `merchant_capacity_exact_control_reconciliation.json`
- `MERCHANT_CAPACITY_EXACT_CONTROL_RECONCILIATION.md`
