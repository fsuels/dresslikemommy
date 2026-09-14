# Google Shopping Shopify-Sold Product Retest Paused Setup Execution Report

UTC timestamp: `20260521T085320Z`

## Approval

I approve creating the paused-ready Google Shopping Shopify-sold-products retest from the 2026-05-21 packet only: exact item IDs in google_ads_retest_candidate_item_scope_2026-05-21.csv, max CPC $0.15, daily cap $5, no PMax, no broad catchall, no Search Partners, no Display, no GA4 optimization, no Merchant/Shopify product/feed changes, and stop for readback before enabling spend.

## Before-State Readback

- Existing retest campaign count before mutation: `0`
- Old Standard Shopping campaign status: `PAUSED`
- Customer: `dresslikemommy.com` (`3990976848`), currency `USD`

## Execution Result

- Mode: `execute`
- Validate-only passed: `True`
- Live mutate executed: `True`
- Operation count: `26`
- Daily cap budget micros: `5000000`
- Max CPC bid micros: `150000`

## After-State Readback

- Validation passed: `True`
- Campaigns: `1`
- Ad groups: `1`
- Product ads: `1`
- Listing groups: `21`
- Included exact item-ID units: `19`
- Excluded catchall units: `1`
- Bad catchall units: `0`
- Location criteria: `1`

## Guardrails

- Campaign, ad group, and product ad must remain paused.
- This setup does not enable spend. Stop before enabling spend.
- No Merchant, Shopify, product/feed, conversion-goal, billing, PMax, Search Partners, Display, broad catchall, GA4 optimization, or existing campaign write occurred.

## Files

- Before JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-shopify-sold-product-paid-retest/google_ads_shopify_sold_retest_before_20260521T085320Z.json`
- After JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-shopify-sold-product-paid-retest/google_ads_shopify_sold_retest_after_20260521T085320Z.json`
