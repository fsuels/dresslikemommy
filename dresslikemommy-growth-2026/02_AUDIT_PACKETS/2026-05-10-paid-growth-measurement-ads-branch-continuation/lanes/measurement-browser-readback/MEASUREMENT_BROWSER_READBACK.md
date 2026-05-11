# Measurement Browser Readback

Date: 2026-05-10

Status: `PARTIAL_PASS_PRE_PURCHASE_ONLY__PURCHASE_EVENT_STILL_UNPROVEN`

## What Was Tested

The measurement lane checked whether non-US storefront sessions carry market currency and value into Google measurement before a purchase. It used safe browser-only checkout-entry paths and stopped before any payment or order.

Markets checked:

- `GB` / `GBP` through Tag Assistant preview and checkout entry.
- `DE` / `EUR` through an authenticated Chrome CDP storefront capture and checkout entry.

No payment data was entered. No Pay Now or Place Order action was clicked. No order, refund, or cancelation was created.

## GB / GBP Evidence

Tag Assistant connected to `dresslikemommy.com` and detected Google tags:

- `AW-853411529`
- `G-N4EQNK0MMB`
- `GT-WRH8Q3MD`

The live product URL was:

`https://www.dresslikemommy.com/products/geometric-blue-family-matching-set?variant=44085199274081&country=GB`

The storefront and checkout-entry readback showed:

- Checkout URL contained `/en-gb`.
- Checkout language was `en-GB`.
- Order summary total was `GBP 15.00`.
- `begin_checkout` dataLayer payload carried `currency: GBP`, `value: 15`, and country `GB`.
- Tag Assistant showed `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` events.

Raw evidence:

- `raw/browser/tagassistant_gb_connected.png`
- `raw/browser/tagassistant_gb_live_product.png`
- `raw/browser/tagassistant_gb_after_product.png`
- `raw/browser/tagassistant_gb_checkout_entry.png`
- `raw/browser/tagassistant_gb_after_checkout_entry.png`
- `raw/browser/gb_checkout_entry_summary.json`
- `raw/browser/tagassistant_gb_text_summary.json`

## DE / EUR Evidence

The DE check used a separate Chrome CDP tab and stopped at checkout entry.

The product URL was:

`https://www.dresslikemommy.com/products/geometric-blue-family-matching-set?variant=44085199274081&country=DE`

The sanitized request capture showed:

- `add_to_cart` requests to Google/GA endpoints with `value=17.95` and `currency=EUR`.
- `begin_checkout` Google Ads request with label `ditQCJzowY8YEMmN-JYD`, `value=17.95`, and `currency_code=EUR`.
- GA4 `begin_checkout` request with `cu=EUR`.

Raw evidence:

- `raw/browser/de_cdp_prepurchase_capture.json`
- `raw/browser/de_cdp_checkout_entry.png`

## Google Ads Conversion Action Readback

Read-only Google Ads browser/CDP readback generated:

- `lanes/measurement-browser-readback/google_ads_conversion_value_readback/google_ads_conversion_value_gate_report.md`
- `lanes/measurement-browser-readback/google_ads_conversion_value_readback/google_ads_conversion_value_gate_summary.json`
- `lanes/measurement-browser-readback/google_ads_conversion_value_readback/purchase_conversion_actions.csv`
- `lanes/measurement-browser-readback/google_ads_conversion_value_readback/sanitized_google_ads_conversion_capture.json`

Key readback points:

- Target action: `Google Shopping App Purchase`.
- Account-level primary purchase action count: `1`.
- Value setting: `Use different values. If there's no value, use 0.`
- Enhanced conversions: enabled and managed through Google Tag.
- Last received request time: `2026-05-09T02:40:54.022671+00:00`.
- Raw historical conversions/value exist: `5.0` conversions and `193.9` value.
- Campaign enable allowed by this packet: `false`.

## What This Proves

This proves that the pre-purchase measurement path is presentment-aware for at least `GBP` and `EUR` through checkout entry. It also proves the current Google Ads purchase conversion action is configured for dynamic value capture and remains the primary purchase action.

## What It Does Not Prove

This does not prove the official Shopify Google & YouTube app's non-US `purchase` event currency/value on the thank-you/order-status surface.

Cart, add-to-cart, view-cart, and begin-checkout currency are useful evidence, but they are not a substitute for an actual `purchase` event. The measurement problem remains approval-gated until a genuine non-US purchase event is observed or the owner approves a controlled test purchase/refund/cancel procedure.
