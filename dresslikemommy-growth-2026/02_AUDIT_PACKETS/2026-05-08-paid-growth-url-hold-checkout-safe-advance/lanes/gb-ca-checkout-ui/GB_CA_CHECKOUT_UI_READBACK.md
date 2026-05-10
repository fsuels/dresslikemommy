# GB / CA Visual Checkout UI Readback

Generated: 2026-05-08 23:10 EDT

Lane: `gb-ca-checkout-ui`

Mode: public storefront browser automation only. No logged-in Shopify Admin, no external ad accounts, no shipping setting edits, no payment data, no Pay Now / Place Order click, and no order creation.

## Summary

| Country | Product landing | Cart | Checkout country/currency | Visible shipping rates | Payment UI | 429/CAPTCHA | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GB | PASS: `United Kingdom | GBP £`, `GBP`, `£21.00` | PASS: 1 item, `GBP`, `£21.00` | PASS: `en-GB`, country `GB`, total `GBP £21.00` | Standard `FREE`; Express `£10.00` | Present as normal checkout UI; not submitted | None seen | PASS for paused infra only |
| CA | PASS: `Canada | CAD $`, `CAD`, `$39.00` | PASS: 1 item, `CAD`, `$39.00` | PASS: `en-CA`, country `CA`, total `CAD $39.00` | Standard `FREE`; Express `$19.00` | Present as normal checkout UI; not submitted | None seen | PASS for paused infra only |

Decision: `GB_CA_CHECKOUT_UI_PASS_FOR_PAUSED_INFRA_ONLY__NO_LIVE_SPEND_READY`.

## Important Hold

The product used for this checkout QA is still covered by `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`: the beach/vacation PDP H1 is clean, but the document title remains `Family Matching Sets - Christmas Print | Dress Like Mommy`. This QA advances the GB/CA checkout UI gate, but the tested URL should not receive live paid traffic until that URL is repaired or swapped/excluded from paid final URLs.

## GB - United Kingdom

Product URL:

`https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=GB`

Readback:

- Product landing retained `country=GB`, showed `Country/region` as `United Kingdom | GBP £`, `og:price:currency=GBP`, and visible price `£21.00`.
- Cart add/readback succeeded with HTTP `200`, currency `GBP`, 1 item, and subtotal `£21.00`.
- Checkout reached Shopify checkout UI with `html lang=en-GB`, selected country value `GB`, region value `ENG`, and test address `10 Downing Street, London SW1A 2AA`.
- Visible shipping rates: `Standard Delivery (10 - 14 Days)` = `FREE`; `Express Delivery (7 - 11 Days)` = `£10.00`.
- Order summary showed subtotal `£21.00`, shipping `FREE`, total `GBP £21.00`.
- Payment section was visible with Credit card, Shop Pay, PayPal, and Crypto: USDC. `Pay now` was visible but not clicked; no payment fields were filled.
- No `429`, CAPTCHA, or verification page appeared.

Screenshots:

- `screenshots/gb-product-landing.png`
- `screenshots/gb-checkout-shipping-payment-ui.png`

## CA - Canada

Product URL:

`https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=CA`

Readback:

- Product landing retained `country=CA`, showed `Country/region` as `Canada | CAD $`, `og:price:currency=CAD`, and visible price `$39.00`.
- Cart add/readback succeeded with HTTP `200`, currency `CAD`, 1 item, and subtotal `$39.00`.
- Checkout reached Shopify checkout UI with `html lang=en-CA`, selected country value `CA`, province value `ON`, and test address `290 Bremner Blvd, Toronto ON M5V 3L9`.
- Visible shipping rates: `Standard Delivery (10 - 14 Days)` = `FREE`; `Express Delivery (7 - 11 Days)` = `$19.00`.
- Order summary showed subtotal `$39.00`, shipping `FREE`, total `CAD $39.00`.
- Payment section was visible with Credit card, Shop Pay, PayPal, and Crypto: USDC. `Pay now` was visible but not clicked; no payment fields were filled.
- No `429`, CAPTCHA, or verification page appeared.

Screenshots:

- `screenshots/ca-product-landing.png`
- `screenshots/ca-checkout-shipping-payment-ui.png`

## Residual Risks / Next Spend Gate

- GB and CA now pass the requested visual checkout UI QA for paused infrastructure support.
- Live spend remains blocked: repair or swap/exclude the tested beach product URL because of the stale Christmas SEO/social title hold, then complete the parent Merchant/Pinterest/tracking/economics gates and get exact owner approval before any enablement.
- Express checkout UI prices differ from earlier public shipping-rate endpoint evidence: GB visual checkout showed `£10.00` vs prior `9.71 GBP`; CA visual checkout showed `$19.00` vs prior `18.00 CAD`. Standard free shipping was consistent. Use visual checkout as the customer-facing proof and reconcile Express economics if Express-rate precision matters.

## Files

- `gb_ca_checkout_ui_readback.json`
- `GB_CA_CHECKOUT_UI_READBACK.md`
- `screenshots/gb-product-landing.png`
- `screenshots/gb-checkout-shipping-payment-ui.png`
- `screenshots/ca-product-landing.png`
- `screenshots/ca-checkout-shipping-payment-ui.png`
