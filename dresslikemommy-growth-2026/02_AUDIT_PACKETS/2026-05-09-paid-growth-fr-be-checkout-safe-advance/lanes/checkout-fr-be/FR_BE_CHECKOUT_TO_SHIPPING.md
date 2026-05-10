# FR/BE Checkout To Shipping Readback

Generated: 2026-05-09T01:52:58-04:00

Mode: public storefront isolated Chrome profile. No payment data was entered, no pay/place-order button was clicked, and no order was created.

## Result

France and Belgium both passed this no-payment checkout-to-shipping readiness probe for paused infrastructure only.

| Market | Product/cart presentment | Rates API | Checkout UI | Decision |
| --- | --- | --- | --- | --- |
| FR | Product/cart carried `EUR`; cart add/read returned `200` / `200` with 1 item | `200`; Standard `0.00 EUR`, Express `11.19 EUR` | `en-FR`; Standard/Express/EUR visible; no verification wall; no order confirmation | `FR_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| BE | Product/cart carried `EUR`; cart add/read returned `200` / `200` with 1 item | `200`; Standard `0.00 EUR`, Express `11.19 EUR` | `en-BE`; Standard/Express/EUR visible; no verification wall; no order confirmation | `BE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |

## Attempt Log

- 2026-05-09 01:52 EDT: Initial FR and BE isolated Chrome run completed. Both countries reached checkout shipping method visibility with EUR presentment and no `429`, CAPTCHA, verification wall, payment data, Pay Now/Place Order click, or order.

## FR

Decision: `FR_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=FR`
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

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-fr?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-FR`
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

## BE

Decision: `BE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=BE`
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

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-be?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-BE`
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
- `Crypto: USDC`
- `Same as shipping address`
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


## Evidence

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-fr-be-checkout-safe-advance/lanes/checkout-fr-be/fr_be_checkout_to_shipping_summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-fr-be-checkout-safe-advance/lanes/checkout-fr-be/screenshots`
- The temporary isolated Chrome profile is deleted after each run so storefront cookies/session data are not persisted in the repo.
