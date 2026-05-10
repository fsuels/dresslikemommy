# CH/DK Checkout To Shipping QA

Generated: 2026-05-09T01:14:08-04:00

Scope: public storefront only, isolated Chrome profiles, no payment data, no Pay Now / Place order click, no order creation, and no account/admin/ad/catalog/theme writes.

Test product: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits`

## Result

Both Switzerland and Denmark passed this no-payment checkout-to-shipping readiness probe.

| Market | Product HTTP / presentment | Cart add/read | Rates API | Checkout UI | Decision |
| --- | --- | --- | --- | --- | --- |
| CH | Product rendered with `CHF` presentment | `200` / `200`, cart currency `CHF`, 1 item | `200`; Standard `0.00 CHF`, Express `10.24 CHF` | `en-CH`; Standard/Express and CHF visible; no verification wall; no order confirmation | `CH_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| DK | Product rendered with `DKK` presentment | `200` / `200`, cart currency `DKK`, 1 item | `200`; Standard `0.00 DKK`, Express `83.60 DKK` | `en-DK`; Standard/Express and DKK/kr visible; no verification wall; no order confirmation | `DK_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |

## Notes

- Checkout payment controls were visible as normal checkout behavior, but no payment fields were completed and no final order button was clicked.
- Screenshots were captured for product, cart, checkout entry, and checkout shipping/rates states for each market.
- The auto-extracted checkout text includes some noisy country/phone-selector lines; the structured probes still confirmed CH/DK country-qualified presentment, matching cart currency, and CH/DK shipping-rate responses.
- This clears CH and DK for paused-infrastructure checkout evidence only. Live spend remains gated by the broader paid-growth approval, Merchant/Pinterest/tracking/economics, and URL-quality controls.

## Evidence

- Detailed summary JSON: `ch_dk_checkout_to_shipping_summary.json`
- Compact summary JSON: `summary.json`
- Runner: `ch_dk_checkout_to_shipping.py`
- Screenshots: `screenshots/`
