# Free Shipping Included Clarity Phase 1

Date: 2026-05-09

## Outcome

Phase 1 was implemented live. The storefront now explains that standard shipping is included in product prices, while exact delivery method, estimate, and any express upgrade are confirmed before payment.

The fix is not Denmark-only. The Shipping Policy / Shipping Info country-confirmation block uses Shopify's active checkout country list and selected-country context. Public readbacks showed `117` currently enabled checkout countries in the country list.

## Live Changes

- Removed visible "free shipping" phrasing from theme-controlled promo, cart, product, homepage, collection, and schema surfaces.
- Added country-specific reassurance to the announcement bar, cart drawer, cart page, and product shipping panel.
- Added a Shipping Policy / Shipping Info country-confirmation block that lists every current checkout country and highlights the selected country when Shopify detects it.
- Updated product JSON-LD shipping details to name the offer shipping as `Standard shipping included`, while keeping `shippingRate.value = 0` because standard shipping is included in the price.
- Updated all theme locale JSON files with the new country-confirmation keys.
- Updated Shopify Admin Shipping Policy, Shipping Info page, and Terms source copy to remove `free standard method` phrasing.
- Registered clean Shopify native translations for Shipping Policy, Shipping Info page, and Terms across all 20 published non-primary storefront locales.
- Added a small visible-text storefront safety net for stale policy translations that may still be served by Shopify's localized policy cache.

## Readbacks

- Denmark policy page via Playwright:
  - Old visible phrase `Standard shipping is free when a free standard method is shown`: `false`
  - Old visible phrase `Available shipping methods and rates are shown at checkout before payment`: `false`
  - New visible phrase `Standard shipping is included in product prices...`: `true`
  - Country list copy `Lande vi aktuelt sender til` / `Alle lande på denne liste`: `true`
- Germany policy curl readback:
  - `Länder, in die wir aktuell liefern (117)`
  - `Jedes Land in dieser Liste ist im Checkout aktiviert...`
- Spanish policy curl readback:
  - `El envío estándar está incluido...`
  - `Países a los que enviamos actualmente (117)`
- Canada product page via Playwright:
  - Visible product note: `Shipping to Canada / CAD $`
  - No visible `Free shipping`
  - No visible `Shipping options shown at checkout`
  - Meta descriptions contain `Standard shipping included + easy returns`, not `Free shipping`
  - JSON-LD uses `"name": "Standard shipping included"` and `"addressCountry": "CA"`
- United Kingdom cart curl readback:
  - `Shipping to United Kingdom. Standard shipping is included...`
  - `STANDARD SHIPPING INCLUDED TO United Kingdom...`

## Verification Commands

- `shopify theme check --path . --fail-level error`
- `git diff --check`
- `python3` JSON parse check for `locales/*.json` and `templates/*.json`
- `python3 ops/scripts/build_product_page_copy_map.py`
- `shopify theme push --store dresslikemommy-com.myshopify.com --theme 134923321441 --allow-live --nodelete --path . --strict ...`
- Shopify Admin policy/page/terms copy repair scripts using credentials loaded from local config, not repo files.
- Playwright browser readbacks for Denmark policy and Canada product pages.

## Guardrails

No Shopify Markets, shipping-rate/profile, checkout setting, product, Merchant Center, Google Ads, Pinterest, GA4/GTM, payment, or order changes were made. Admin writes were limited to Shipping Policy, Shipping Info page, Terms body copy, and their native translations.

## Residual Risk

Some localized policy source HTML may continue to show stale policy text to raw curl while Shopify cache settles, but Admin source and native translations read back clean, and browser-visible customer text is corrected by the live storefront safety net.
