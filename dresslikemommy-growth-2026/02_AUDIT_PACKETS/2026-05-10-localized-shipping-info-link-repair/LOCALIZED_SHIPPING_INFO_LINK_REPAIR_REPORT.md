# Localized Shipping Info Link Repair

Date: 2026-05-10

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-localized-shipping-info-link-browser-fallback-live`

## Why

The owner reported that the product-page link `See all current shipping countries` stopped working after changing the storefront language away from English.

## Root Cause

Live localized PDP readbacks showed malformed URLs:

- Spanish product page: `/espages/shipping-info`
- German product page: `/depages/shipping-info`
- French product page: `/frpages/shipping-info`

Both shipping snippets built the URL with:

```liquid
routes.root_url | append: 'pages/shipping-info'
```

On localized routes Shopify returned `routes.root_url` without a trailing slash (`/es`, `/de`, `/fr`), so direct append produced a broken route.

## Changes

Scoped theme patch only:

- `snippets/shipping-country-confirmation.liquid`
- `snippets/shipping-country-checker-modal.liquid`
- `layout/theme.liquid`

The snippets now normalize the localized root before appending `/pages/shipping-info`, and append `?country=<current country>` when a current country code exists.

The layout now also has a small browser fallback that repairs cached malformed Shipping Info anchors and redirects malformed localized routes such as `/espages/shipping-info` to `/es/pages/shipping-info`. This covers product-page HTML that remains stale in Shopify/browser caches after the snippet repair.

## Live Push

Pushed only the two snippets first, then pushed only `layout/theme.liquid` as the cache/route fallback, to live theme `134923321441` / `DLM CRO Preview 2026-05-06`.

## Verification

- `shopify theme check --path . --fail-level error` passed with `264` files inspected.
- `git diff --check -- layout/theme.liquid snippets/shipping-country-confirmation.liquid snippets/shipping-country-checker-modal.liquid ops/AGENT_COORDINATION.md ops/PROBLEM_TRACKER.md` passed.
- Source scan found no remaining `routes.root_url | append: 'pages/shipping-info'` pattern and no static malformed `/espages`, `/depages`, or `/frpages` links in theme files.
- Pre-push live pullback diff confirmed the only live/local differences were the URL-builder lines in the two snippets.
- Post-push live pullback diff matched local for both snippets.
- Live/local pullback after the layout fallback push matched local for `layout/theme.liquid`.
- Public product readbacks passed:
  - ES PDP now renders `/es/pages/shipping-info?country=ES` for both the PDP note and modal note.
  - DE PDP now renders `/de/pages/shipping-info?country=DE` for both the PDP note and modal note.
  - FR PDP now renders `/fr/pages/shipping-info?country=FR` for both the PDP note and modal note.
- Public linked page readbacks passed:
  - `/es/pages/shipping-info?country=ES` returned HTTP `200`, localized country confirmation, and `117` countries.
  - `/de/pages/shipping-info?country=DE` returned HTTP `200`, localized country confirmation for Germany, and the live country list.
  - `/fr/pages/shipping-info?country=FR` returned HTTP `200`, localized country confirmation for France, and `117` countries.
- Exact browser spot-check of the Spanish product combo still found cached stale product HTML with `href="/espages/shipping-info"` for `Ver todos los países de envío actuales`, so the layout fallback was tested against the real shopper path.
- Exact headless-Chrome click readback passed: clicking that stale Spanish PDP link landed on `https://www.dresslikemommy.com/es/pages/shipping-info`, showed H1 `Información de envío`, had no 404 text, and showed the current country-list copy.

## Guardrails

No Shopify Admin page/policy/product data, Shopify Markets, shipping-rate/profile/checkout settings, Merchant, Google Ads, Pinterest, feed, campaign, budget, bid, product-scope, product-group, conversion, checkout payment, or order changes were made.

## Next

Closed. If a similar localized route issue appears later, check whether `routes.root_url` is being concatenated without normalizing a trailing slash, and verify the malformed cached route in a real browser.
