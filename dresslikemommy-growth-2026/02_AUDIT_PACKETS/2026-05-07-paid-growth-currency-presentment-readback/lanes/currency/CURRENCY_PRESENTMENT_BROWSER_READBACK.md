# Currency / Presentment Browser Readback

Generated: 2026-05-08 00:25 EDT

Scope: parent browser walkthrough for ES, IT, RO, and PT. No payment details were entered, `Pay now` was not clicked, no order was created, and no Shopify/Admin/Market/shipping-rate settings were changed.

## Decision

`INTERNATIONAL_PAID_STILL_NOT_READY`

The result is more nuanced than the prior endpoint-only readback. Currency can present correctly after the storefront country/locale selector is set, but a fresh direct localized route can still start as United States / English / USD. That is risky for paid traffic unless the ad URL or storefront market selection path reliably lands shoppers in the intended market.

## Country Results

| Country | Fresh direct route | After storefront localization | Checkout shipping step | Decision |
|---|---|---|---|---|
| ES | Direct `/es` first landed on English / US / USD in a fresh browser context | Spain / Spanish / EUR on product and cart | Reached shipping step; country Spain; region `Madrid Province`; Standard Delivery `FREE`; Express `EUR 11.95`; total in EUR | Presentment works after localization, but direct-route behavior and English checkout are still caution flags |
| IT | Direct `/it` first landed on English / US / USD in a fresh browser context | Italy / Italian / EUR on product and cart | Reached shipping step; country Italy; province `Rome`; Standard Delivery `FREE`; Express `EUR 11.95`; total in EUR | Presentment works after localization, but direct-route behavior and English checkout are still caution flags |
| RO | Direct `/ro` first landed on English / US / USD in a fresh browser context | Romania / Romanian / RON on product and cart | Reached shipping step; country Romania; county `Bucharest`; Standard Delivery `FREE`; Express `60.00 lei`; total in RON | Presentment works after localization, but in RON, not EUR; use actual RON economics if testing RO |
| PT | Direct `/pt` first landed on English / US / USD in a fresh browser context | Portugal / pt-BR / EUR on product page | Not reached; `/cart/add.js` returned `429`, then one UI add-to-cart retry also returned `429` | Product presentment looks correct after localization, but browser checkout/shipping-step proof remains blocked by storefront `429` |

## Important Findings

- Language paths alone are not enough evidence for market presentment. In fresh browser contexts, `/es`, `/it`, `/ro`, and `/pt` initially landed on the base English product URL with `United States | USD`.
- The storefront localization form corrected presentment for ES, IT, RO, and PT product pages.
- ES and IT carried EUR through cart and checkout shipping.
- RO carried RON through cart and checkout shipping. This contradicts the earlier simplified "expected EUR" assumption; the live browser presents Romania in local RON.
- PT product page presented EUR after localization, but PT checkout could not be completed to shipping step because cart add hit storefront `429`.
- ES, IT, and RO checkout pages were still mostly English (`en-ES`, `en-IT`, `en-RO`) even when product/cart pages were localized.
- Payment sections became visible on Shopify's one-page checkout after rates loaded for ES/IT/RO. No payment data was entered and no pay/submit action was taken.

## Artifacts

- `CURRENCY_PRESENTMENT_BROWSER_READBACK.json`
- ES screenshots: `es_02_product_after_localization.png`, `es_03_cart_after_add.png`, `es_04_checkout_shipping_step.png`
- IT screenshots/snapshot: `it_02_product_after_localization.png`, `it_03_cart_after_add.png`, `it_04_checkout_shipping_step.png`, `it_04_checkout_shipping_step_snapshot.txt`
- RO screenshots/snapshot: `ro_02_product_after_localization.png`, `ro_03_cart_after_add.png`, `ro_04_checkout_shipping_step.png`, `ro_04_checkout_shipping_step_snapshot.txt`
- PT screenshots: `pt_02_product_after_localization.png`, `pt_429_product_after_add_attempt.png`

## Guardrails Preserved

- No payment submitted.
- No order created.
- No Shopify Admin, Markets, shipping-rate, product-data, theme, Merchant, Pinterest, Google Ads, feed, budget, bid, status, conversion-goal, product-scope, product-group, or feed-label change.
- No CAPTCHA bypass or aggressive retry after `429`.

## Next Safe Action

Wait for storefront cooldown, then rerun PT only from a fresh browser context: set Portugal / pt-BR through the storefront localization form, add one item to cart, proceed to checkout, select Portugal / Lisboa, verify shipping rates and final currency, and stop before payment. Separately, decide whether paid URLs must include or force a market-localization step so ad traffic does not start in US/USD.
