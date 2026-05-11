# Public Measurement Preflight Report

Generated: 2026-05-10

Lane: `public-measurement-preflight`

Scope: safe local/public measurement preflight for next non-US paid-growth gates, focused on `PL`, `CZ`, `RO`, `PT`, and `GR`. No checkout payment, no order, no external account writes, no Shopify Admin writes, no Ads/Merchant/Pinterest writes, and no theme edits.

## Decision

`PRE_PURCHASE_PRESENTMENT_INPUTS_SUPPORTED__PURCHASE_CURRENCY_GAP_NOT_CLOSED`

The public storefront and repo evidence support that pre-purchase theme ecommerce events are intended to expose presentment currency before purchase:

- Theme ecommerce payloads resolve currency from public product-page `og:price:currency` first, then `window.Shopify.currency.active`, then default to `USD`.
- The same resolver feeds `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout`.
- Existing public storefront/cart evidence already shows presentment currency for the target markets before payment:
  - `PL`: cart/shipping `PLN`.
  - `CZ`: cart/shipping `CZK`.
  - `RO`: product/cart/checkout-to-shipping `RON`.
  - `PT`: product/cart/checkout-to-shipping `EUR`.
  - `GR`: cart/shipping `EUR`.

This does **not** close the purchase-currency gap. The theme has no `purchase` event, and purchase measurement is app-fired from Shopify checkout/thank-you by the official Google & YouTube app. Whether that app sends `currency=<presentment>` or `currency=USD` for a non-US purchase remains unverified.

## What Was Verified

### Repo measurement code

Verified by reading `assets/analytics.js`:

- `getCurrency()` reads public product metadata and Shopify active currency:
  - `meta[property="og:price:currency"]`
  - `window.Shopify.currency.active`
  - fallback `USD`
- `buildBaseItem()` sets item-level `currency: getCurrency()`.
- `buildEcommercePayload()` sets event-level `currency: getCurrency()`.
- `pushViewItemOnce()` pushes `view_item`.
- `pushAddToCartEvent()` pushes `add_to_cart`.
- `pushViewCartEvent()` pushes `view_cart`.
- `pushBeginCheckoutEvent()` pushes `begin_checkout`.

Important boundary: the repo-side theme analytics file does not author a `purchase` event. The prior measurement gap report already concluded purchase is owned by the official Shopify app path, not this theme dataLayer.

### Existing public storefront evidence used

Used existing successful storefront evidence rather than redoing checkout:

- `2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/PAID_GROWTH_SE_PL_CZ_GR_CHECKOUT_SAFE_ADVANCE_REPORT.md`
  - `PL`: cart currency `PLN`; Standard `0.00 PLN`; Express `47.40 PLN`; no payment/order.
  - `CZ`: cart currency `CZK`; Standard `0.00 CZK`; Express `272.13 CZK`; no payment/order.
  - `GR`: cart currency `EUR`; Standard `0.00 EUR`; Express `11.19 EUR`; no payment/order.
- `2026-05-07-paid-growth-currency-presentment-readback/lanes/currency/CURRENCY_PRESENTMENT_BROWSER_READBACK.json`
  - `RO`: product currency `RON`; cart currency `RON`; checkout total currency `RON`; no payment/order.
- `2026-05-08-paid-growth-pt-presentment-url-readback/PAID_GROWTH_PT_PRESENTMENT_URL_READBACK_REPORT.md`
  - `PT`: product/cart/checkout carried EUR after Portugal localization; total `EUR € 24,95`; no payment/order.

### Fresh public probe attempt

Attempted one bounded low-volume public HTTP probe for each target market against the already-used product/variant:

`matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601`

Probe intent:

- Load product URL with `country=<ISO>`.
- Read public product currency inputs (`og:price:currency`, `Shopify.currency.active`).
- Add one item to the session cart.
- Read `/cart.js` currency.
- Clear the session cart.
- Stop before checkout.

Result: Shopify returned HTTP `429` for all five product/cart attempts in this shell, so no fresh currency readback was obtained. I stopped after that bounded pass and did not retry or attempt any bypass.

Fresh probe result summary:

| Market | Expected | Product | Cart add | Cart read | Fresh result |
|---|---:|---:|---:|---:|---|
| `PL` | `PLN` | `429` | `429` | `429` | Fresh probe blocked |
| `CZ` | `CZK` | `429` | `429` | `429` | Fresh probe blocked |
| `RO` | `RON` | `429` | `429` | `429` | Fresh probe blocked |
| `PT` | `EUR` | `429` | `429` | `429` | Fresh probe blocked |
| `GR` | `EUR` | `429` | `429` | `429` | Fresh probe blocked |

## Commands And Tools Run

- `rg` over `ops/` continuity/problem/worklog files for current paid-growth state, measurement gap, currency, GA4, and Tag Assistant references.
- `find` over `dresslikemommy-growth-2026/02_AUDIT_PACKETS` to locate relevant currency, checkout, and measurement reports.
- `sed` on the current measurement/conversion gap lane report and country checkout reports.
- `rg` over theme files for `dataLayer`, ecommerce events, `currency`, and `purchase`.
- `sed` on `assets/analytics.js` around `getCurrency()`, ecommerce payload builders, and pre-purchase event pushers.
- `mcp__playwright__.browser_resize` and `mcp__chrome_devtools__.list_pages`; both were blocked by an existing browser profile lock.
- `node` public HTTP probe, one bounded pass across `PL`, `CZ`, `RO`, `PT`, and `GR`; all public requests returned `429`.
- `git status --short` to confirm the worktree had other agents' unrelated edits and this lane was initially empty.

## Evidence

Positive evidence:

- Theme code wires pre-purchase ecommerce event currency from public product/page currency signals.
- Prior public no-payment evidence confirms the target markets carry expected storefront/cart currency before purchase:
  - `PLN` for Poland.
  - `CZK` for Czechia.
  - `RON` for Romania.
  - `EUR` for Portugal.
  - `EUR` for Greece.

Negative/limiting evidence:

- Fresh HTTP probes were blocked by `429`, so this lane did not add new live public currency readbacks.
- Browser automation was unavailable because the shared browser profile was already locked.
- No GA4 Realtime, Tag Assistant, Google Ads conversion diagnostics, or checkout thank-you-page event capture was performed.

## What Remains Unverified

Still unverified and still gating non-US enablement:

- The actual `currency` parameter on the live app-fired `purchase` event for a non-US order.
- Whether Google Ads receives non-US purchases as presentment currency, converted USD, or a mismatched USD label with presentment numeric value.
- Whether GA4 receives `purchase.currency` as presentment currency for `PL`, `CZ`, `RO`, `PT`, and `GR`.
- Whether Tag Assistant sees the same currency on `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` in a real browser session for all five markets. The repo code says it should; this lane did not capture browser event logs.
- Whether the existing `Google Shopping App Purchase` conversion action has any live diagnostics or currency warnings for non-US traffic.

## Does This Close The Purchase-Currency Gap?

No.

This preflight supports the pre-purchase layer only. It says the storefront/cart layer and theme dataLayer design are aligned with presentment currency before purchase. It does not prove the purchase event that Google Ads optimizes against. The gap remains:

`Shopify checkout purchase event currency for non-US orders is unknown.`

Do not use this report as approval to enable non-US Search spend. It is only a supporting preflight for the next browser-enabled measurement gate.

## Next Browser-Enabled GA4 / Tag Assistant Action

Run this next in an isolated browser session with Tag Assistant and GA4 Realtime available:

1. Open Tag Assistant for `https://www.dresslikemommy.com/`.
2. For `PL`, `CZ`, `RO`, `PT`, and `GR`, walk product -> add to cart -> cart -> begin checkout, stopping before payment.
3. Capture event details for `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout`.
4. Confirm event-level `currency` and item-level `currency` match expected presentment:
   - `PL=PLN`
   - `CZ=CZK`
   - `RO=RON`
   - `PT=EUR`
   - `GR=EUR`
5. In GA4 Realtime, confirm the same events arrive with those currency parameters.
6. Separately, after a genuine non-US purchase or an owner-approved synthetic test order, capture the actual app-fired `purchase` request in Tag Assistant/DevTools and confirm `purchase.currency` and `value` before any non-US campaign enablement.

No payment or order should be submitted during steps 1-5.
