# Google Shopping Shopify-Sold Product Retest Paused Setup Execution Report

UTC timestamp: `20260521T085307Z`

## Approval

I approve creating the paused-ready Google Shopping Shopify-sold-products retest from the 2026-05-21 packet only: exact item IDs in google_ads_retest_candidate_item_scope_2026-05-21.csv, max CPC $0.15, daily cap $5, no PMax, no broad catchall, no Search Partners, no Display, no GA4 optimization, no Merchant/Shopify product/feed changes, and stop for readback before enabling spend.

## Before-State Readback

- Existing retest campaign count before mutation: `0`
- Old Standard Shopping campaign status: `PAUSED`
- Customer: `dresslikemommy.com` (`3990976848`), currency `USD`

## Execution Result

- Mode: `validate_only`
- Validate-only passed: `True`
- Live mutate executed: `False`
- Operation count: `26`
- Daily cap budget micros: `5000000`
- Max CPC bid micros: `150000`

## After-State Readback

- Validation passed: `False`
- Campaigns: `0`
- Ad groups: `0`
- Product ads: `0`
- Listing groups: `0`
- Included exact item-ID units: `0`
- Excluded catchall units: `0`
- Bad catchall units: `0`
- Location criteria: `0`

## Guardrails

- Campaign, ad group, and product ad must remain paused.
- This setup does not enable spend. Stop before enabling spend.
- No Merchant, Shopify, product/feed, conversion-goal, billing, PMax, Search Partners, Display, broad catchall, GA4 optimization, or existing campaign write occurred.

## Files

- Before JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-shopify-sold-product-paid-retest/google_ads_shopify_sold_retest_before_20260521T085307Z.json`
- After JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-shopify-sold-product-paid-retest/google_ads_shopify_sold_retest_after_20260521T085307Z.json`

## Validation Issues

- Expected 1 campaign, found 0
- Expected 1 ad group, found 0
- Expected 1 product ad, found 0
- Expected 1 root subdivision, found 0
- Item ID mismatch: missing=['shopify_us_7510790733921_43768831148129', 'shopify_us_7510790733921_43768831311969', 'shopify_us_7510790733921_43768831803489', 'shopify_us_7510790733921_43768831967329', 'shopify_us_7510790733921_43768832131169', 'shopify_us_7516479848545_43831323164769', 'shopify_us_7516479848545_43831323263073', 'shopify_us_7535362015329_44057274810465', 'shopify_us_7535362015329_44057274908769', 'shopify_us_7535944368225_44076870664289', 'shopify_us_7535944368225_44076870860897', 'shopify_us_7536696295521_44082061082721', 'shopify_us_7536696295521_44082061246561', 'shopify_us_7536703012961_44082074517601', 'shopify_us_7536703012961_44082074714209', 'shopify_us_7536988520545_44083433930849', 'shopify_us_7536988520545_44083434258529', 'shopify_us_7537025613921_44083600031841', 'shopify_us_7537025613921_44083600195681'] extra=[]
- Expected 1 excluded catchall, found 0
- Expected 1 location criterion, found 0
