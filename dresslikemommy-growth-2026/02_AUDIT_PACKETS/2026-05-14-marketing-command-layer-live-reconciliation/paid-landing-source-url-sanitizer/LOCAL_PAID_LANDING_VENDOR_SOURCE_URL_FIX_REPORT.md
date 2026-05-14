# Local Paid Landing Vendor Source URL Fix Report

Timestamp: 2026-05-14 06:05 EDT

Scope: active GB/CA/AU exact Search final URL, local Shopify theme sanitizer, no external writes.

## Finding

Public source readback of the active Search landing PDP returned `200`, showed correct country/currency/shipping signals, and did not show stale Christmas, local-inventory, warehouse, or retail-store copy.

The same public source exposed a supplier URL in a related product analytics attribute:

```text
data-analytics-vendor="https://detail.1688.com/offer/602107180663.html"
```

This is a paid-landing trust blocker. Supplier/source URLs must not appear in customer-visible HTML, analytics attributes, feed-visible data, ad copy, or shopper-facing copy.

## Local Fix

Patched the local theme to normalize blank, URL-like, `1688.com`, `alibaba.com`, and `aliexpress.com` vendor/brand values to `dresslikemommy.com` before they reach storefront-visible or analytics-facing attributes.

Touched local files:

- `snippets/card-product.liquid`
- `snippets/home-spotlight-card.liquid`
- `sections/main-product.liquid`
- `snippets/cart-drawer.liquid`
- `sections/main-cart-items.liquid`
- `sections/cart-notification-product.liquid`
- `sections/predictive-search.liquid`
- `assets/analytics.js`
- `assets/homepage-collection-card-images.js`

No Shopify Admin product/vendor data was edited.

## Local Readback

Local URLs checked on `http://127.0.0.1:9292`:

- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=GB`
- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=CA`
- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=AU`

Local source counts:

- `detail.1688.com`: `0`
- `1688.com`: `0`
- `alibaba.com`: `0`
- `aliexpress.com`: `0`
- `data-analytics-vendor="https://`: `0`
- `data-item-brand="https://`: `0`
- `Christmas`: `0`
- `local inventory`: `0`
- `warehouse`: `0`
- `retail store`: `0`
- `priceCurrency`: present
- `Ships to`: present

Related product cards now emit sanitized brand/vendor values such as:

```text
data-analytics-vendor="dresslikemommy.com"
```

## Verification

Passed:

- `node --check assets/analytics.js`
- `node --check assets/homepage-collection-card-images.js`
- `git diff --check`
- `shopify theme check --path . --fail-level error --output json`

## Guardrails

No external writes occurred:

- No Shopify theme push/sync/publish.
- No Shopify Admin product/vendor edit.
- No Google Ads, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product-scope, or conversion write.

## Next Action

Get fresh explicit approval for a scoped live theme sync/push of only the sanitizer files, then repeat public source and rendered DOM readback on GB/CA/AU final URLs.

Until that live readback passes, do not treat this paid landing as clean for expansion.
