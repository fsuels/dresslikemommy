# GB First Exact Browser Readback

Date: 2026-05-10

Mode: public browser-style storefront readback. No payment information was entered, no Pay Now / Place Order button was clicked, and no order was created.

## Target

- Market: `GB`
- First-enable candidate campaign: `23838895360`
- First-enable candidate ad group: `Mommy & Me Dresses - Exact`
- Final URL checked: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=GB`

## Result

`PASS_BROWSER_READBACK_FOR_LANDING_AND_CHECKOUT_ENTRY`

The earlier raw terminal `curl` returned `403`, but the browser-style readback did not reproduce that failure.

## Observed Evidence

- Product page loaded at the exact GB country-qualified URL.
- Page title read `Family Matching Sets - Beige | Dress Like Mommy`.
- No visible `403`, access-denied, CAPTCHA, verification wall, or browser-check page appeared.
- Country/currency signals were present for `United Kingdom`, `GBP`, and pound pricing.
- Product metadata was beige-family-matching aligned:
  - `og:title`: `Family Matching Sets - Beige | Dress Like Mommy`
  - `twitter:title`: `Family Matching Sets - Beige | Dress Like Mommy`
  - `product:price:currency`: `GBP`
- No stale Christmas metadata was observed in the checked title/meta/body signals.
- The product had a selected variant and a visible/enabled Add to Cart control.
- Add to Cart succeeded and cart count moved to `1 item`.
- Checkout entry succeeded and reached a Shopify checkout URL with `en-gb`.
- Checkout page showed checkout/contact/delivery context plus `United Kingdom` and GBP/pound signals.

## Guardrails Preserved

- No payment information entered.
- No Pay Now / Place Order click.
- No order, refund, cancellation, Merchant, Google Ads, Pinterest, Shopify Admin product-data, conversion-goal, product-scope, feed-label, product-group, budget, bid, or status write.

## Residual Gate

This solves the raw `curl` 403 uncertainty for the first GB landing URL. It does not solve the separate non-US purchase-event currency/value measurement gate.
