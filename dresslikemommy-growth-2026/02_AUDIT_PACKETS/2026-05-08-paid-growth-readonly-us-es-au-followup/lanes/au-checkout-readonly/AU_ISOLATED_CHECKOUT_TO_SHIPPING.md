# AU Isolated Checkout To Shipping Readback

Generated: 2026-05-08T03:30:26-04:00

Mode: public storefront isolated Chrome profile. No payment data was entered, no pay/place-order button was clicked, and no order was created.

Decision: `AU_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

## Product And Cart

- Product URL: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=AU`
- Product page title: `Family Matching Sets - Christmas Print | Dress Like Mommy`
- Product `html lang`: `en`
- Product currency meta: `AUD`
- Cart add HTTP status: `200`
- Cart read HTTP status: `200`
- Cart currency: `AUD`
- Cart item count: `1`
- Shipping-rates API HTTP status: `200`

## Shipping Rates

| Rate | Price | Currency |
| --- | --- | --- |
| `Standard Delivery (10 - 14 Days)` | `0.00` | `AUD` |
| `Express Delivery (7 - 11 Days)` | `18.24` | `AUD` |

## Checkout UI

- Checkout URL redacted: `https://www.dresslikemommy.com/checkouts/REDACTED/en-au?_r=REDACTED&auto_redirect=false&edge_redirect=true&skip_shop_pay=true`
- Checkout `html lang`: `en-AU`
- UI contains Standard: `True`
- UI contains Express: `True`
- UI contains AUD / money signal: `True`
- Pay-now button visible: `True`
- Order confirmation text found: `False`
- Blocked by verification text: `False`

Relevant checkout lines:

- `Express checkout`
- `Saudi Arabia(+966)`
- `Delivery`
- `Saudi Arabia`
- `Shipping method`
- `Choose a shipping method`
- `Standard Delivery (10 - 14 Days)`
- `FREE`
- `Express Delivery (7 - 11 Days)`
- `$19.00`
- `Use shipping address as billing address`
- `Shipping`
- `$40.00`
- `$40.00`
- `Shipping`
- `FREE`
- `AUD`
- `$40.00`
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

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/au-checkout-readonly/au_isolated_checkout_to_shipping_summary.json`
- Screenshots: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/au-checkout-readonly/screenshots`
- The temporary isolated Chrome profile was deleted after the run so storefront cookies/session data are not persisted in the repo.
