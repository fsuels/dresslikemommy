# NL Checkout Retry To Shipping Readback

Generated: 2026-05-09T10:51:43-04:00

Mode: single public storefront Netherlands cooldown retry in an isolated Chrome profile. No payment data was entered, no Pay Now/Place Order button was clicked, no order was created, and no CAPTCHA or verification bypass was attempted.

## Result

- Decision: `NL_API_RATES_PASS_CHECKOUT_REACHED_NL_SELECTION_NOT_CONFIRMED_NO_PAYMENT_NO_ORDER`
- Stop reason: `STOP_PAYMENT_STEP_VISIBLE_BEFORE_ALLOWED`
- Product reached: `True`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Shipping-rates API HTTP status: `200`
- Checkout reached: `True`
- Selected Netherlands confirmed in checkout UI: `False`
- Payment-action guardrail triggered: `True`
- Checkout shipping UI pass: `False`
- Blocked by verification text: `False`
- Payment/order created: `False`
- Live-spend-ready non-US markets remain `0`; this lane is paused-infrastructure QA only.
- Note: this single retry was not repeated. It cleared the prior NL `429` on cart/rates, then stopped at checkout entry before address fill because the conservative guardrail detected payment-action text on the checkout page.

## Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=NL`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `EUR`
- Product presentment text includes Netherlands/EUR: `True`
- Cart currency: `EUR`
- Cart item count: `1`

## Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `EUR` |
| `Express Delivery (7 - 11 Days)` | `11.19` | `EUR` |

## Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-nl?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-NL`
- UI contains Standard: `True`
- UI contains Express: `True`
- UI contains currency / money signal: `True`
- Pay-now button visible: `False`
- Order confirmation text found: `False`

Relevant visible lines:

- `Express checkout`
- `Delivery`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `€11.95`
- `Use shipping address as billing address`
- `Shipping`
- `€21.95`
- `€21.95`
- `Shipping`
- `FREE`
- `EUR`
- `€21.95`
- `Updated total price: €21.95 EURUpdated shipping method: Standard Delivery (10 - 14 Days)`

## Evidence

- Detailed summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-checkout-standard-metrics-safe-advance/lanes/nl-checkout-retry/nl_checkout_retry_summary.json`
- Compact summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-checkout-standard-metrics-safe-advance/lanes/nl-checkout-retry/summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-nl-checkout-standard-metrics-safe-advance/lanes/nl-checkout-retry/screenshots`
- Temporary isolated Chrome profile was deleted after the run.
