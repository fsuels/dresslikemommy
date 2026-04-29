# Shopify Margin CAC Export Pack

Read-only packet. No Shopify, feed, discount, ad, product, billing, or settings writes were performed.

## What this contains

- Sanitized Shopify Admin order export and order line-item model.
- Active product/variant cost-basis export.
- Product-level contribution margin, max CAC, target ROAS, and A/B/C/D tiering.
- Field map and export checklist for remaining data gaps.

## Current decision

Do not change ads, discounts, bundles, or product scaling from Shopify Home alone. Use this packet as the first economics layer, then reconcile the remaining NEEDS_DATA exports.

## Key results

- Date range: 2025-04-28T22:49:02-04:00 through 2026-04-28T22:49:02-04:00
- Orders collected: 89
- Orders included in model: 83
- Active variants: 7324
- Product model rows: 358
- Observed AOV: $73.93
- Max CAC at observed AOV: $11.09
- Target ROAS floor: 6.6667
- Tier counts: {"A": 7, "B": 33, "C": 14, "D": 304}

## Remaining gaps

- Official Shopify Finance reports still need export/reconciliation.
- Shipping label costs or carrier invoices are still needed for true fulfillment-cost proof.
- Shopify Payments payout adjustments, chargebacks, and external gateway fees still need export.
- Analytics source/device and ad-platform spend exports are still needed before CAC decisions become executable.
