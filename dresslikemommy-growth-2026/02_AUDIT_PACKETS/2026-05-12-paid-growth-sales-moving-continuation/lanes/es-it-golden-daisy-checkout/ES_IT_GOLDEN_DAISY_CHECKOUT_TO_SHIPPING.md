# ES/IT Golden Daisy Checkout To Shipping Readback

Generated: 2026-05-12T16:56:41-04:00

Mode: public storefront isolated Chrome profile using country-qualified Golden Daisy URLs. No payment data was entered, no pay/place-order button was clicked, and no order was created.

## ES

Decision: `ES_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=ES`
- Product page title: `Golden Daisy Mamá e hija | Dress Like Mommy`
- Product `html lang`: `es`
- Product currency meta: `EUR`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `EUR`
- Cart item count: `1`
- Shipping-rates API HTTP status: `422`

### Shipping Rates

- No rates returned from the API probe.

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-es?_r=REDACTED`
- Checkout `html lang`: `en-ES`
- Selected checkout country: `Spain` / `ES`
- UI contains Standard: `True`
- UI contains Express: `True`
- UI contains currency / money signal: `True`
- Pay-now button visible: `True`
- Order confirmation text found: `False`
- Blocked by verification text: `False`

Relevant checkout lines:

- `Express checkout`
- `Delivery`
- `Saudi Arabia`
- `Saudi Arabia(+966)`
- `Ukraine(+380)`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `€11.95`
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `€23.95`
- `€23.95`
- `Shipping`
- `FREE`
- `EUR`
- `€23.95`
- `Shipping`
- `Shipping Policy`
- `At Dress Like Mommy, we want your matching outfits to arrive as clearly and reliably as possible. Review the shipping method, rate, and delivery estimate shown at checkout before placing an order.`
- `Shipping is available to the countries and regions shown at checkout. Availability depends on the destination, product, and shipping methods shown during checkout. Use the country/region selector or the checkout shipping step to confirm whether we can ship to your address before placing an order.`
- `If your destination does not appear at checkout, or if no shipping method is shown for your address, contact us at info@dresslikemommy.com before ordering.`
- `Shipping Rates`
- `Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.`
- `Delivery Times`
- `Orders are processed within 1-3 business days after payment confirmation. Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout.`
- `Standard Delivery: the current checkout estimate displays before payment.`
- `Express Delivery: available for some destinations where shown at checkout.`
- `These are estimates. Actual delivery times may vary because of customs processing, carrier delays, weather, holidays, or local conditions.`
- `How Our Shipping Works`
- `Shipping Problems`
- `For shipping questions, email info@dresslikemommy.com.`

## IT

Decision: `IT_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

### Product And Cart

- Product URL: `https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=IT`
- Product page title: `Golden Daisy mamma e figlia | Dress Like Mommy`
- Product `html lang`: `it`
- Product currency meta: `EUR`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `EUR`
- Cart item count: `1`
- Shipping-rates API HTTP status: `422`

### Shipping Rates

- No rates returned from the API probe.

### Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-it?_r=REDACTED`
- Checkout `html lang`: `en-IT`
- Selected checkout country: `Italy` / `IT`
- UI contains Standard: `True`
- UI contains Express: `True`
- UI contains currency / money signal: `True`
- Pay-now button visible: `True`
- Order confirmation text found: `False`
- Blocked by verification text: `False`

Relevant checkout lines:

- `Express checkout`
- `Delivery`
- `Saudi Arabia`
- `Saudi Arabia(+966)`
- `Ukraine(+380)`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `€11.95`
- `Use shipping address as billing address`
- `Crypto: USDC`
- `Shipping`
- `€23.95`
- `€23.95`
- `Shipping`
- `FREE`
- `EUR`
- `€23.95`
- `Shipping`
- `Shipping Policy`
- `At Dress Like Mommy, we want your matching outfits to arrive as clearly and reliably as possible. Review the shipping method, rate, and delivery estimate shown at checkout before placing an order.`
- `Shipping is available to the countries and regions shown at checkout. Availability depends on the destination, product, and shipping methods shown during checkout. Use the country/region selector or the checkout shipping step to confirm whether we can ship to your address before placing an order.`
- `If your destination does not appear at checkout, or if no shipping method is shown for your address, contact us at info@dresslikemommy.com before ordering.`
- `Shipping Rates`
- `Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.`
- `Delivery Times`
- `Orders are processed within 1-3 business days after payment confirmation. Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout.`
- `Standard Delivery: the current checkout estimate displays before payment.`
- `Express Delivery: available for some destinations where shown at checkout.`
- `These are estimates. Actual delivery times may vary because of customs processing, carrier delays, weather, holidays, or local conditions.`
- `How Our Shipping Works`
- `Shipping Problems`
- `For shipping questions, email info@dresslikemommy.com.`


## Evidence

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/lanes/es-it-golden-daisy-checkout/es_it_golden_daisy_checkout_to_shipping_summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/lanes/es-it-golden-daisy-checkout/screenshots`
- The temporary isolated Chrome profile is deleted after each run so storefront cookies/session data are not persisted in the repo.
