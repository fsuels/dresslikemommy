# Swimsuit PDP Ruler Local/Live Parity

Date: 2026-05-13

Owner report: local preview looked correct, but the live product URL did not appear to match the local ruler icon and inline chart behavior.

Product checked:

- `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`

Actions:

- Reopened the PDP ruler lane for a scoped theme-only live sync.
- Confirmed the live theme source now matches the local PDP ruler JS/CSS files.
- Added fresh asset filenames to bypass Shopify CDN immutability for newly rendered product pages:
  - `assets/product-desktop-ux-20260513-ruler-sync.js`
  - `assets/component-product-desktop-ux-ruler-sync.css`
- Updated `sections/main-product.liquid` to load those fresh asset names.
- Added a harmless `templates/product.json` comment bump as a theme-only cache refresh attempt.
- Pushed scoped files to live theme `dresslikemommy/main` `#133290917985`.

Verification:

- `node --check assets/product-desktop-ux.js`: passed.
- `node --check assets/product-desktop-ux-20260513.js`: passed.
- `node --check assets/product-desktop-ux-20260513-ruler-sync.js`: passed.
- `shopify theme check --path . --fail-level error --output json`: `[]`.
- `git diff --check`: passed.
- Shopify CLI push to live theme `#133290917985`: passed.
- Shopify CLI pullback of the scoped live files matched local source.

Final browser readback:

- Local mobile and live mobile both had `1` visible inline ruler trigger and `0` legacy fit links/old size-guide triggers.
- Local desktop and live desktop both had `1` visible inline ruler trigger and `0` legacy fit links/old size-guide triggers.
- Clicking the ruler opened the inline panel in the product card on both local and live.
- No modal opened, and the legacy full size guide did not open.
- The table rows matched exactly on local and live:
  - `S|86.36-88.9|66-68.58|92.71-95.25`
  - `M|91.44-93.98|71.12-73.66|97.79-100.33`
  - `L|97.79-101.6|77.47-81.28|104.14-107.95`
  - `XL|105.41-109.22|85.09-88.9|111.76-115.57`
- Mobile table wrapper matched local/live: `clientWidth=312`, `scrollWidth=312`, `clientHeight=102`, `scrollHeight=102`.
- Desktop table wrapper matched local/live: `clientWidth=491`, `scrollWidth=491`, `clientHeight=88`, `scrollHeight=88`.

Notes:

- The exact bare product URL can still return an older HTML asset filename in plain `curl` because of Shopify page-cache behavior, but browser readback on the same URL showed matching local/live rendered behavior and styles.
- A variant-parameter live render already shows the fresh cache-busting asset filenames.
- No Shopify Admin product/page/policy/translation/discount writes were made.
- No checkout, order, Ads, Merchant, Pinterest, GA4/GTM, budget, feed, conversion, credential, billing, or product-data changes were made.
