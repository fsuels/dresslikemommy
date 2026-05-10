# Shipping Country Clarity Guardrail

Generated: 2026-05-09

## Why

A customer asked whether Dress Like Mommy ships to Denmark because a page sounded like Denmark was not supported, while checkout allowed a Denmark delivery address.

## What Changed

Theme-only live storefront guardrail:

- Added a dynamic Shipping Policy / Shipping Info block that reads Shopify `localization.available_countries`.
- The block confirms the selected country, e.g. `Yes, we currently ship to Denmark`.
- The block shows a scrollable current country/currency list from Shopify's active checkout country selector.
- Added a compact product-page shipping note that confirms the selected country/currency and links to `/pages/shipping-info`.

Files pushed to live theme `134923321441` / `DLM CRO Preview 2026-05-06`:

- `layout/theme.liquid`
- `snippets/shipping-country-confirmation.liquid`
- `assets/component-shipping-countries-v2.css`
- `sections/main-product.liquid`

## Guardrails Preserved

No changes were made to:

- Shopify Markets
- Shipping rates, shipping profiles, or checkout settings
- Shopify product data
- Shipping Policy or Shipping Info Admin source copy
- Merchant Center, Google Ads, Pinterest, feeds, budgets, bids, campaign status, product scope, feed labels, product groups, conversion goals
- Payment or order state

## Verification

- `shopify theme check --path . --fail-level error`: passed, `262 files inspected with no offenses found`.
- `git diff --check`: passed for touched files.
- `shopify theme info --store dresslikemommy-com.myshopify.com --theme 134923321441 --json --path .`: confirmed target theme is live.
- `shopify theme push --store dresslikemommy-com.myshopify.com --theme 134923321441 --allow-live --path . --strict --json --only ...`: pushed the scoped theme files.
- `curl` public readback for `/policies/shipping-policy?country=DK`: found `Yes, we currently ship to Denmark`, `Denmark is currently included in this checkout country list`, and the `component-shipping-countries-v2.css` asset.
- `curl` public readback for `/pages/shipping-info?country=DK`: found the same Denmark confirmation and current-country block.
- `curl` public readback for a product page with `country=DK`: found `Shipping country: Denmark`, `DKK`, and `See all current shipping countries`.
- Playwright desktop and mobile snapshots confirmed the block renders without visible overlap and the country list is constrained to a scrollable 320px area.

## Evidence

- Desktop snapshot: `playwright/shipping-country-policy-dk-v2-snapshot.md`
- Desktop screenshot: `playwright/shipping-country-policy-dk-v2-desktop.png`
- Mobile snapshot: `playwright/shipping-country-policy-dk-v2-mobile-snapshot.md`
- Mobile screenshot: `playwright/shipping-country-policy-dk-v2-mobile.png`
- Initial oversized-list iteration evidence: `playwright/shipping-country-policy-dk-snapshot.md`, `playwright/shipping-country-policy-dk-desktop.png`

## Result

Denmark is now clearly answered before the policy body, and customers can inspect the current Shopify country/currency list without waiting until checkout.
