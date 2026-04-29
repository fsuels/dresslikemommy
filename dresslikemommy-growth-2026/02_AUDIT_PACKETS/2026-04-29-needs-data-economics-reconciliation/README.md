# NEEDS_DATA Economics Reconciliation

Read-only reconciliation pass. No Shopify, feed, product, discount, ad, billing, or campaign changes were made.

## What improved

- Shopify Payments payouts, balance transactions, and disputes were collected through Admin GraphQL.
- Order shipping charged/refunded was reconciled into a shipping-cost worklist.
- Existing Pinterest, Google Ads, and GA4 local packets were imported into one ad/analytics evidence table.

## What remains blocked

- Actual shipping label/carrier costs still require Shopify Shipping reports or carrier invoices.
- Google Ads still needs full 30/90/365 campaign, search term, location, and device exports.
- GA4 still needs detailed ecommerce source/campaign/country/device/landing page/item exports.
- Meta Ads still needs export if it is in use.
- Official Shopify Finance reports should still be exported for report parity.
