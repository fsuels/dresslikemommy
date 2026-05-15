# Merchant Capacity Live Execution Approval Packet

Mode: local/read-only approval and readback packet. No Merchant, Shopify, Google
Ads, Pinterest, feed, product, product-group, bid, budget, status, capacity,
billing, credential, or conversion writes were made.

## Purpose

Move the current P0 Merchant capacity lane from scattered prep into one
action-time packet. This packet does not authorize live changes by itself; it
defines the exact approval phrase, before-save reconciliation, and after-export
readback required before Canada/French-Canada/GB Shopping can be considered.

## Exact Approval Phrase

`I approve the Merchant priority-market capacity cleanup execution: remove or disable from Google/Merchant publishing scope only the exact non-priority groups in merchant_capacity_platform_preview_acceptance.csv and, if Shopify Markets is the control surface, only the International regions marked remove in shopify_international_region_prune_preview.csv; preserve USA English, USA Spanish, Canada, United Kingdom, Eurozone, Australia, Europe-later groups, CA/AU duplicate hold rows, and all hold-review regions; do not delete products or change titles, prices, vendors, variants, feed labels, campaigns, product groups, bids, budgets, statuses, conversion settings, billing, or credentials; then capture a fresh Merchant all-products export and run the after-export guard.`

## Before-State From Current Evidence

- Current Merchant all-products rows: `351007`.
- Merchant first-pass remove groups: `41`.
- Expected first-pass row removal: `199684`.
- Expected after-first-pass row floor: `151323`.
- Protected USA English rows: `5491`.
- Protected USA Spanish rows: `5412`.
- Current Canada English rows: `0`.
- Current Canada French rows: `0`.
- Current GB English rows: `0`.
- Shopify `International` regions: `73`.
- Shopify first-pass removal regions: `52`.
- Shopify preserve/hold-review regions: `21`.

## Live Pre-Save Reconciliation

Before any Save, Apply, Sync, Upload, or equivalent platform action:

1. Reconcile the Merchant/feed-country preview to
   `merchant_capacity_platform_preview_acceptance.csv`.
2. If Shopify Markets is the control surface, reconcile the region preview to
   `shopify_international_region_prune_preview.csv`.
3. Confirm the selected live preview removes only the non-priority publishing
   scope, not products.
4. Confirm USA English and USA Spanish stay enabled and unselected for removal.
5. Confirm separate `Canada`, `United Kingdom`, `Eurozone`, and `Australia`
   markets are preserved; duplicate `CA` and `AU` rows inside `International`
   are not removed in this first pass.
6. Stop if the UI/API preview cannot match both CSVs.

## After-State Readback

After a live cleanup, capture a fresh Merchant all-products export and run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/build_merchant_capacity_execution_guard.py --after-export /path/to/fresh_export.csv
```

Pass criteria:

- `0` first-pass removal rows remain.
- USA English rows do not drop below `5491`.
- USA Spanish rows do not drop below `5412`.
- Canada English/French and GB English are not called Shopping-build-ready until
  fresh export rows exist.

## Hard Stops

- No whole-market removal.
- No product deletion.
- No product title, price, variant, vendor, inventory, feed-label, campaign,
  product-group, bid, budget, status, conversion, billing, credential, or
  capacity-request mutation.
- No save if either CSV cannot be reconciled.
- No Canada/GB Shopping build until the after-export proof exists.

## Files

- `merchant_capacity_live_execution_checklist.csv`
- `merchant_capacity_live_execution_packet_summary.json`
- `merchant_capacity_platform_preview_acceptance.csv`
- `shopify_international_region_prune_preview.csv`
- `MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`
- `MERCHANT_SHOPIFY_MARKETS_REGION_PRUNE_PREVIEW.md`
