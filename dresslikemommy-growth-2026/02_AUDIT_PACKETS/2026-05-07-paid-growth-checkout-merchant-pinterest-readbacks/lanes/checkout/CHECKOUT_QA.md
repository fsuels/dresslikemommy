# Checkout QA - ES / IT / RO / PT

Generated: 2026-05-07T23:25:57-04:00

## Scope

- Lane: checkout storefront/checkout QA only.
- Countries: ES, IT, RO, PT only.
- Mode: anonymous storefront/cart reads; no payment, no order creation, no Shopify data or checkout setting changes.
- Delay between public probes: 25.0 seconds.
- Stop rule: stop remaining probes immediately if Shopify storefront bot protection, CAPTCHA, or HTTP 429 appears.

## Cart Product

- Variant ID: `41871520661601`
- Product: Beach Outfits Holiday Palm Tree Print Summer Dresse... | DLM
- Variant: Father XL / blue
- URL: https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set

## Outbound Checkout Delivery Rate Results

| Country | Test address | HTTP | Status | Rates | Blocker |
| --- | --- | ---: | --- | --- | --- |
| ES Spain | Madrid 28013 | 200 | RATES_AVAILABLE | Standard Delivery (10 - 14 Days) 0.00 USD; Express Delivery (7 - 11 Days) 12.99 USD | - |
| IT Italy | Roma 00118 | 200 | RATES_AVAILABLE | Standard Delivery (10 - 14 Days) 0.00 USD; Express Delivery (7 - 11 Days) 12.99 USD | - |
| RO Romania | București 010011 | 200 | RATES_AVAILABLE | Standard Delivery (10 - 14 Days) 0.00 USD; Express Delivery (7 - 11 Days) 12.99 USD | - |
| PT Portugal | Lisboa 1100-148 | 200 | RATES_AVAILABLE | Standard Delivery (10 - 14 Days) 0.00 USD; Express Delivery (7 - 11 Days) 12.99 USD | - |

## Locale / Policy URLs

### ES - Spain

- Expected storefront language route: `es` (Spanish)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | Shopify currency signal | URL | Finding |
| --- | ---: | --- | --- | --- | --- | --- |
| product | 200 | es | USD | USD | https://www.dresslikemommy.com/es/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | es | - | USD | https://www.dresslikemommy.com/es/pages/shipping-info | readable |
| shipping_policy | 200 | es | - | USD | https://www.dresslikemommy.com/es/policies/shipping-policy | readable |
| refund_policy | 200 | es | - | USD | https://www.dresslikemommy.com/es/policies/refund-policy | readable |

### IT - Italy

- Expected storefront language route: `it` (Italian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | Shopify currency signal | URL | Finding |
| --- | ---: | --- | --- | --- | --- | --- |
| product | 200 | it | USD | USD | https://www.dresslikemommy.com/it/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | it | - | USD | https://www.dresslikemommy.com/it/pages/shipping-info | readable |
| shipping_policy | 200 | it | - | USD | https://www.dresslikemommy.com/it/policies/shipping-policy | readable |
| refund_policy | 200 | it | - | USD | https://www.dresslikemommy.com/it/policies/refund-policy | readable |

### RO - Romania

- Expected storefront language route: `ro` (Romanian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | Shopify currency signal | URL | Finding |
| --- | ---: | --- | --- | --- | --- | --- |
| product | 200 | ro | USD | USD | https://www.dresslikemommy.com/ro/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | ro | - | USD | https://www.dresslikemommy.com/ro/pages/shipping-info | readable |
| shipping_policy | 200 | ro | - | USD | https://www.dresslikemommy.com/ro/policies/shipping-policy | readable |
| refund_policy | 200 | ro | - | USD | https://www.dresslikemommy.com/ro/policies/refund-policy | readable |

### PT - Portugal

- Expected storefront language route: `pt` (Portuguese)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | Shopify currency signal | URL | Finding |
| --- | ---: | --- | --- | --- | --- | --- |
| product | 200 | pt-BR | USD | USD | https://www.dresslikemommy.com/pt/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | pt-BR | - | USD | https://www.dresslikemommy.com/pt/pages/shipping-info | readable |
| shipping_policy | 200 | pt-BR | - | USD | https://www.dresslikemommy.com/pt/policies/shipping-policy | readable |
| refund_policy | 200 | pt-BR | - | USD | https://www.dresslikemommy.com/pt/policies/refund-policy | readable |

## Findings

- Live outbound checkout delivery-rate lookup returned rates for 4 of 4 target countries.
- Countries blocked by storefront rate limit/bot protection: none.
- Countries with no rates returned: none.
- Countries with checkout address/rate validation failures: none.
- Policy/shipping pages with limited-country copy: none detected in probed pages.
- Route HTTP failures in this run: none.
- Product currency meta/signals not matching expected EUR: ES:USD, IT:USD, RO:USD, PT:USD.
- Portugal route failures in this run: none.

## Next Safe Action

Keep ES/IT/RO/PT out of live paid spend until the parent integrates this with catalog/feed, tracking, route/currency, and economics gates. If spend is later considered, perform a human browser checkout walkthrough through the shipping step only; do not submit payment.

## Artifacts

- `slow_checkout_qa.py`
- `checkout_probe_raw.json`
- `CHECKOUT_QA.md`
