# Checkout QA - NL / ES / IT / RO / PT

Generated: 2026-05-07T14:41:24-04:00

## Scope

- Lane: checkout storefront/checkout QA only.
- Mode: anonymous storefront/cart reads; no payment, no order creation, no Shopify data or checkout setting changes.
- Delay between public probes: 12.0 seconds.
- Stop rule: stop remaining probes immediately if Shopify storefront bot protection, CAPTCHA, or HTTP 429 appears.

## Cart Product

- Variant ID: `41871520661601`
- Product: Beach Outfits Holiday Palm Tree Print Summer Dresse... | DLM
- Variant: Father XL / blue
- URL: https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set

## Shipping Rate Results

| Country | Test address | HTTP | Status | Rates | Blocker |
| --- | --- | ---: | --- | --- | --- |
| NL Netherlands | Amsterdam 1012 AB | 200 | RATES_AVAILABLE | Standard Delivery (10 - 14 Days) 0.00 USD; Express Delivery (7 - 11 Days) 12.99 USD | - |
| ES Spain | Madrid 28013 | 422 | FAILED | - | - |
| IT Italy | Rome 00118 | 422 | FAILED | - | - |
| RO Romania | Bucharest 010011 | 422 | FAILED | - | - |
| PT Portugal | Lisbon 1100-148 | 422 | FAILED | - | - |

## Locale / Policy URLs

### NL - Netherlands

- Expected storefront language route: `nl` (Dutch)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 500 | en | - | https://www.dresslikemommy.com/nl | readable |
| product | 200 | nl | USD | https://www.dresslikemommy.com/nl/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_policy | 200 | nl | - | https://www.dresslikemommy.com/nl/policies/shipping-policy | readable |
| refund_policy | 200 | nl | - | https://www.dresslikemommy.com/nl/policies/refund-policy | readable |

### ES - Spain

- Expected storefront language route: `es` (Spanish)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 500 | en | - | https://www.dresslikemommy.com/es | readable |
| product | 200 | es | USD | https://www.dresslikemommy.com/es/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_policy | 200 | es | - | https://www.dresslikemommy.com/es/policies/shipping-policy | shipping-limited copy detected |
| refund_policy | 200 | es | - | https://www.dresslikemommy.com/es/policies/refund-policy | readable |

Policy/shipping limitation snippets:
- `shipping_policy`: utfits to arrive as quickly and safely as possible. Here’s everything you need to know about shipping. Where We Ship We currently ship to: United States (all 50 states + territories) Canada United Kingdom Australia Can’t find your country? Contact us at info@dresslikemommy.com — we may be able to arrange shipping to additional destinations. Shipping Rates

### IT - Italy

- Expected storefront language route: `it` (Italian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 500 | en | - | https://www.dresslikemommy.com/it | readable |
| product | 200 | it | USD | https://www.dresslikemommy.com/it/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_policy | 200 | it | - | https://www.dresslikemommy.com/it/policies/shipping-policy | readable |
| refund_policy | 200 | it | - | https://www.dresslikemommy.com/it/policies/refund-policy | readable |

### RO - Romania

- Expected storefront language route: `ro` (Romanian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 200 | ro | - | https://www.dresslikemommy.com/ro | readable |
| product | 200 | ro | USD | https://www.dresslikemommy.com/ro/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_policy | 200 | ro | - | https://www.dresslikemommy.com/ro/policies/shipping-policy | shipping-limited copy detected |
| refund_policy | 200 | ro | - | https://www.dresslikemommy.com/ro/policies/refund-policy | readable |

Policy/shipping limitation snippets:
- `shipping_policy`: utfits to arrive as quickly and safely as possible. Here’s everything you need to know about shipping. Where We Ship We currently ship to: United States (all 50 states + territories) Canada United Kingdom Australia Can’t find your country? Contact us at info@dresslikemommy.com — we may be able to arrange shipping to additional destinations. Shipping Rates

### PT - Portugal

- Expected storefront language route: `pt-BR` (Portuguese (Brazil))
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 404 | en | - | https://www.dresslikemommy.com/pt-BR | readable |
| product | 404 | en | - | https://www.dresslikemommy.com/pt-BR/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_policy | 404 | en | - | https://www.dresslikemommy.com/pt-BR/policies/shipping-policy | readable |
| refund_policy | 404 | en | - | https://www.dresslikemommy.com/pt-BR/policies/refund-policy | readable |
| pt_home_fallback | 500 | en | - | https://www.dresslikemommy.com/pt | readable |
| pt_shipping_policy_fallback | 200 | pt-BR | - | https://www.dresslikemommy.com/pt/policies/shipping-policy | shipping-limited copy detected |

Policy/shipping limitation snippets:
- `pt_shipping_policy_fallback`: utfits to arrive as quickly and safely as possible. Here’s everything you need to know about shipping. Where We Ship We currently ship to: United States (all 50 states + territories) Canada United Kingdom Australia Can’t find your country? Contact us at info@dresslikemommy.com — we may be able to arrange shipping to additional destinations. Shipping Rates

## Findings

- Live shipping-rate lookup returned rates for 1 of 5 target countries.
- Countries blocked by storefront rate limit/bot protection: none.
- Countries with no rates returned: none.
- Countries with checkout address/rate validation failures: ES HTTP 422 (`Select a province`), IT HTTP 422 (`Select a province`), RO HTTP 422 (`Select a county`), PT HTTP 422 (`Select a region`).
- Policy/shipping pages with limited-country copy: ES:shipping_policy, RO:shipping_policy, PT:pt_shipping_policy_fallback.
- Portugal route failures in this run: home HTTP 404, product HTTP 404, shipping_policy HTTP 404, refund_policy HTTP 404, pt_home_fallback HTTP 500.

## Next Safe Action

Keep NL/ES/IT/RO/PT out of live paid spend until the parent integrates this with policy-copy repair and localized landing-page review. The next no-payment pass should provide/choose required province, county, or region values for ES/IT/RO/PT and proceed only through the shipping-rate step; do not rerun immediately if the parent already owns a single follow-up probe.

## Artifacts

- `slow_checkout_qa.py`
- `checkout_probe_raw.json`
- `CHECKOUT_QA.md`
