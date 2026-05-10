# DE/NL Checkout To Shipping Readback

Generated: 2026-05-09T01:26:34-04:00

Mode: public storefront isolated Chrome profile. No payment data was entered, no pay/place-order button was clicked, and no order was created.

## Result

Germany passed this no-payment checkout-to-shipping readiness probe for paused infrastructure only.

Netherlands did not pass. The product landing page rendered with Netherlands / EUR, but both the initial NL pass and one cooldown retry returned HTTP `429` / `Verifying your connection...` on cart add, cart read, and shipping-rates API. No CAPTCHA was solved or bypassed; probing stopped after the second grounded attempt.

| Market | Product HTTP / presentment | Cart add/read | Rates API | Checkout UI | Decision |
| --- | --- | --- | --- | --- | --- |
| DE | Product rendered with `EUR` presentment | `200` / `200`, cart currency `EUR`, 1 item | `200`; Standard `0.00 EUR`, Express `11.19 EUR` API; checkout UI showed Express `€11.95` | `en-DE`; Standard/Express and EUR visible; no verification wall; no order confirmation | `DE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| NL | Product rendered with Netherlands / `EUR` presentment | Attempt 1: `429` / `429`; cooldown retry: `429` / `429` | Attempt 1: `429`; cooldown retry: `429`; `Verifying your connection...` HTML | Did not reach checkout; browser remained on public storefront/home after blocked cart flow | `NL_CHECKOUT_STILL_BLOCKED_OR_RATES_NOT_VISIBLE` |

## Attempt Log

- 2026-05-09 01:24 EDT: Initial DE then NL run. DE passed. NL product landing rendered Netherlands / EUR, but cart add/read/rates returned HTTP `429` verification HTML.
- 2026-05-09 01:26 EDT: After cooldown, ran NL only in a fresh isolated Chrome profile. NL again returned HTTP `429` verification HTML on cart add/read/rates, so no further checkout probing was attempted.

## DE

Decision: `DE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=DE`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `EUR`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `EUR`
- Cart item count: `1`
- Shipping-rates API HTTP status: `200`

### Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `EUR` |
| `Express Delivery (7 - 11 Days)` | `11.19` | `EUR` |

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-de?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-DE`
- UI contains Standard: `True`
- UI contains Express: `True`
- UI contains currency / money signal: `True`
- Pay-now button visible: `True`
- Order confirmation text found: `False`
- Blocked by verification text: `False`

Relevant checkout lines:

- `Express checkout`
- `Saudi Arabia(+966)`
- `Ukraine(+380)`
- `Delivery`
- `Saudi Arabia`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `€11.95`
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `€21.95`
- `€21.95`
- `Shipping`
- `FREE`
- `EUR`
- `€21.95`
- `Shipping`
- `Shipping Policy`
- `At Dress Like Mommy, we want your matching outfits to arrive as clearly and reliably as possible. Review the shipping method, rate, and delivery estimate shown at checkout before placing an order.`
- `Shipping is available to the countries and regions shown at checkout. Availability depends on the destination, product, and shipping methods shown during checkout. Use the country/region selector or the checkout shipping step to confirm whether we can ship to your address before placing an order.`
- `If your destination does not appear at checkout, or if no shipping method is shown for your address, contact us at info@dresslikemommy.com before ordering.`
- `Shipping Rates`
- `Available shipping methods and rates are shown at checkout before payment. Standard shipping is free when a free standard method is shown for your destination. Express or paid options may be available for some addresses and will display before you place the order.`
- `Delivery Times`
- `Orders are processed within 1-3 business days after payment confirmation. Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout.`
- `Standard Delivery: the current checkout estimate displays before payment.`
- `Express Delivery: available for some destinations where shown at checkout.`
- `These are estimates. Actual delivery times may vary because of customs processing, carrier delays, weather, holidays, or local conditions.`
- `How Our Shipping Works`
- `Shipping Problems`
- `For shipping questions, email info@dresslikemommy.com.`

## NL

Decision: `NL_CHECKOUT_STILL_BLOCKED_OR_RATES_NOT_VISIBLE`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=NL`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `EUR`
- Cart add HTTP status: `429`
- Cart read HTTP status: `429`
- Cart currency: ``
- Cart item count: `None`
- Shipping-rates API HTTP status: `429`

### Shipping Rates

- No rates returned from the API probe.

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/`
- Checkout `html lang`: `en`
- UI contains Standard: `False`
- UI contains Express: `False`
- UI contains currency / money signal: `True`
- Pay-now button visible: `False`
- Order confirmation text found: `False`
- Blocked by verification text: `True`

Relevant checkout lines:

- `SHIPPING OPTIONS AT CHECKOUT | FAMILY MATCHING MADE EASY | SECURE CHECKOUT`
- `Netherlands | EUR €`
- `Shipping options shown at checkout, secure checkout, and helpful sizing support.`
- `Shipping options shown at checkout`
- `Shipping options shown at checkout, thoughtful help with sizing, and a family-owned team that replies within 1 business day.`
- `From €21,95 EUR`
- `From €31,95 EUR`
- `From €20,95 EUR`
- `Shipping Info`
- `Shipping policy`


## Evidence

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/checkout-de-nl/de_nl_checkout_to_shipping_summary.json`
- Compact summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/checkout-de-nl/summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/checkout-de-nl/screenshots`
- The temporary isolated Chrome profile is deleted after each run so storefront cookies/session data are not persisted in the repo.
