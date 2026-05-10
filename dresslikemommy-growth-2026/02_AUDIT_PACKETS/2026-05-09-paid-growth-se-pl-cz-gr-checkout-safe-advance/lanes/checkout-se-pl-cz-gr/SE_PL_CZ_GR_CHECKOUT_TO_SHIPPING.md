# SE/PL/CZ/GR Checkout To Shipping Readback

Generated: 2026-05-09T02:11:26-04:00

Mode: public storefront isolated Chrome profile. No payment data was entered, no Pay Now/Place Order button was clicked, no order was created, and no CAPTCHA or verification bypass was attempted.

## Result

- Markets attempted: `SE, PL, CZ, GR`
- Passed checkout-to-shipping for paused infrastructure only: `SE, PL, CZ, GR`
- Needs follow-up: `none`
- Stopped early: `False`
- Live-spend-ready non-US markets remain `0`; passing this lane supports paused infrastructure only.

| Market | Product/cart presentment | Rates API | Checkout UI | Decision |
| --- | --- | --- | --- | --- |
| SE | Cart `SEK`, add/read `200` / `200`, items `1` | `200`; Standard Delivery (10 - 14 Days): 0.00 SEK, Express Delivery (7 - 11 Days): 121.52 SEK | `en-SE`; Standard `True`, Express `True`, currency `True`, verification `False`, order `False` | `SE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| PL | Cart `PLN`, add/read `200` / `200`, items `1` | `200`; Standard Delivery (10 - 14 Days): 0.00 PLN, Express Delivery (7 - 11 Days): 47.40 PLN | `en-PL`; Standard `True`, Express `True`, currency `True`, verification `False`, order `False` | `PL_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| CZ | Cart `CZK`, add/read `200` / `200`, items `1` | `200`; Standard Delivery (10 - 14 Days): 0.00 CZK, Express Delivery (7 - 11 Days): 272.13 CZK | `en-CZ`; Standard `True`, Express `True`, currency `True`, verification `False`, order `False` | `CZ_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |
| GR | Cart `EUR`, add/read `200` / `200`, items `1` | `200`; Standard Delivery (10 - 14 Days): 0.00 EUR, Express Delivery (7 - 11 Days): 11.19 EUR | `en-GR`; Standard `True`, Express `True`, currency `True`, verification `False`, order `False` | `GR_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER` |

## Details

## SE

Decision: `SE_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=SE`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `SEK`
- Cart clear HTTP status: `200`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `SEK`
- Cart item count: `1`
- Shipping-rates API HTTP status: `200`

### Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `SEK` |
| `Express Delivery (7 - 11 Days)` | `121.52` | `SEK` |

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-se?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-SE`
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
- `122,00 kr`
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `234,00 kr`
- `234,00 kr`
- `Shipping`
- `FREE`
- `SEK`
- `234,00 kr`
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

## PL

Decision: `PL_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=PL`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `PLN`
- Cart clear HTTP status: `200`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `PLN`
- Cart item count: `1`
- Shipping-rates API HTTP status: `200`

### Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `PLN` |
| `Express Delivery (7 - 11 Days)` | `47.40` | `PLN` |

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-pl?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-PL`
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
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `Shipping`
- `FREE`
- `PLN`
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

## CZ

Decision: `CZ_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=CZ`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `CZK`
- Cart clear HTTP status: `200`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `CZK`
- Cart item count: `1`
- Shipping-rates API HTTP status: `200`

### Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `CZK` |
| `Express Delivery (7 - 11 Days)` | `272.13` | `CZK` |

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-cz?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-CZ`
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
- `You may receive text messages related to order confirmation and shipping updates. Reply STOP to unsubscribe. Reply HELP for help. Message frequency varies. Msg & data rates may apply. View our`
- `Delivery`
- `Saudi Arabia`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `Shipping`
- `FREE`
- `CZK`
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

## GR

Decision: `GR_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?variant=41878479831137&country=GR`
- Product page title: `Family Matching Sets - Beige | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `EUR`
- Cart clear HTTP status: `None`
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

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-gr?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-GR`
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

## Evidence

- Detailed summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/lanes/checkout-se-pl-cz-gr/se_pl_cz_gr_checkout_to_shipping_summary.json`
- Compact summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/lanes/checkout-se-pl-cz-gr/summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/lanes/checkout-se-pl-cz-gr/screenshots`
- Temporary isolated Chrome profiles are deleted after each run so storefront cookies/session data are not persisted in the repo.
