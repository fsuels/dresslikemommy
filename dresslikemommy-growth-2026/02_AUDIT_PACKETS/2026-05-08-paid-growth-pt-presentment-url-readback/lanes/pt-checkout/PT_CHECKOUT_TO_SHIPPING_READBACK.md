# PT Checkout To Shipping Readback

Generated: 2026-05-08 00:57 EDT

Lane: Parent PT-only browser checkout QA after cooldown.

## Scope

Continue from `AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-currency-presentment-readback` and rerun Portugal only through the storefront/cart/checkout shipping step.

Guardrails preserved: no payment data entered, no `Pagar agora` / Pay Now click, no order creation, no Shopify Admin write, no Shopify Markets/currency/shipping-rate change, no product-data write, no Merchant/Pinterest/Ads write, and no campaign import/spend.

## Method

- Browser surface: Chrome DevTools, isolated context `DLM-QA-LandingLocalization-PT-20260508`.
- Product URL tested: `/pt/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601`.
- Product variant used: `41871520661601`.
- Storefront localization used: `country_code=PT`, `locale_code=pt-BR`, return path `/pt/products/...`.
- Synthetic checkout address:
  - Country: Portugal
  - Region: Lisboa
  - City: Lisboa
  - Postal code: `1100-148`

Checkout token and query parameters are intentionally redacted/omitted from this report.

## Readback Results

| Step | Result |
|---|---|
| Fresh direct `/pt` product route | Redirected to the non-localized product path and presented English / United States / USD. Evidence: `screenshots/pt-direct-language-route-baseline.png`. |
| Storefront localization | After posting the native Shopify localization form, product route presented `Portugal | EUR €`, `Português (brasil)`, and price `€24,95 EUR`. Evidence: `screenshots/pt-localized-product-eur.png`. |
| Add to cart | Passed after cooldown. Network readback showed `POST /pt/cart/add` returned `200`; no `429` blocker recurred. |
| Cart drawer | One item present; cart total `€24,95 EUR`. Evidence: `screenshots/pt-localized-cart-eur.png`. |
| Checkout entry | Checkout opened in Portuguese with redacted path `/checkouts/cn/REDACTED/pt-br`; `html lang` read `pt-BR`. |
| Delivery country/region | Country preselected as `Portugal`; region dropdown accepted `Lisboa`. |
| Shipping rates | `Entrega padrão (10 a 14 dias)` selected at `GRÁTIS`; `Entrega expressa (7 a 11 dias)` available at `€ 11,95`. |
| Order summary | Subtotal `€ 24,95`; shipping `GRÁTIS`; total `EUR € 24,95`. Evidence: `screenshots/pt-checkout-shipping-rates-eur.png`. |
| Payment/order status | Payment section became visible because Shopify one-page checkout renders it after delivery info, but no card/payment fields were entered and `Pagar agora` was not clicked. Readback found no order-confirmation text. |

## Decision

PT checkout/currency/shipping-step QA is now `PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

Portugal can be treated like ES/IT for the narrow checkout-presentment gate: product, cart, and checkout shipping step carry EUR after correct market localization. International paid traffic is still not launch-ready until the URL-entry behavior is controlled, Merchant/Pinterest gates clear or are explicitly accepted, and Ads import receives exact approval.
