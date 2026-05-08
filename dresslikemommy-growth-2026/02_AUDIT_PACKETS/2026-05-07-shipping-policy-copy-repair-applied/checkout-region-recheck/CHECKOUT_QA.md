# Checkout QA - NL / ES / IT / RO / PT

Generated: 2026-05-07T16:18:41-04:00

## Parent Note

This file is the final expanded QA run after adding localized Shipping Info pages to the URL set. It hit Shopify storefront bot protection / HTTP 429 at the IT product page before cart/rate probes could run, so the rate table below reflects the stop-rule blocker.

Earlier same-session no-payment rate probes, using the corrected region values `Comunidad de Madrid`, `Roma`, `București`, and `Lisboa`, returned outbound checkout delivery rates for all five target countries. See the parent report for the combined interpretation.

## Scope

- Lane: checkout storefront/checkout QA only.
- Mode: anonymous storefront/cart reads; no payment, no order creation, no Shopify data or checkout setting changes.
- Delay between public probes: 4.0 seconds.
- Stop rule: stop remaining probes immediately if Shopify storefront bot protection, CAPTCHA, or HTTP 429 appears.

## Cart Product

- Variant ID: `41871520661601`
- Product: Beach Outfits Holiday Palm Tree Print Summer Dresse... | DLM
- Variant: Father XL / blue
- URL: https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set

## Outbound Checkout Delivery Rate Results

| Country | Test address | HTTP | Status | Rates | Blocker |
| --- | --- | ---: | --- | --- | --- |
| NL Netherlands | Amsterdam 1012 AB |  | BLOCKED_NOT_RUN | - | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |
| ES Spain | Madrid 28013 |  | BLOCKED_NOT_RUN | - | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |
| IT Italy | Rome 00118 |  | BLOCKED_NOT_RUN | - | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |
| RO Romania | Bucharest 010011 |  | BLOCKED_NOT_RUN | - | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |
| PT Portugal | Lisbon 1100-148 |  | BLOCKED_NOT_RUN | - | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |

## Locale / Policy URLs

### NL - Netherlands

- Expected storefront language route: `nl` (Dutch)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 200 | nl | - | https://www.dresslikemommy.com/nl | readable |
| product | 200 | nl | USD | https://www.dresslikemommy.com/nl/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | nl | - | https://www.dresslikemommy.com/nl/pages/shipping-info | readable |
| shipping_policy | 200 | nl | - | https://www.dresslikemommy.com/nl/policies/shipping-policy | readable |
| refund_policy | 200 | nl | - | https://www.dresslikemommy.com/nl/policies/refund-policy | readable |

### ES - Spain

- Expected storefront language route: `es` (Spanish)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 200 | es | - | https://www.dresslikemommy.com/es | readable |
| product | 200 | es | USD | https://www.dresslikemommy.com/es/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | readable |
| shipping_info | 200 | es | - | https://www.dresslikemommy.com/es/pages/shipping-info | shipping-limited copy detected |
| shipping_policy | 200 | es | - | https://www.dresslikemommy.com/es/policies/shipping-policy | readable |
| refund_policy | 200 | es | - | https://www.dresslikemommy.com/es/policies/refund-policy | readable |

Policy/shipping limitation snippets:
- `shipping_info`: o 0 0 artículos Información de envío Información de envío En Dress Like Mommy , enviamos conjuntos familiares a juego a familias de todo el mundo. Aquí tienes toda la información sobre cómo llega tu pedido a casa. 📦 Envío gratis en cada pedido Ofrecemos envío estándar GRATIS en todos los pedidos: sin compra mínima ni códigos. Es nuestra forma de hacer que la ropa
- `shipping_info`: os: sin compra mínima ni códigos. Es nuestra forma de hacer que la ropa a juego sea accesible para todas las familias. 🌍A dónde enviamos Estados Unidos — los 50 estados y territorios Canadá Reino Unido Australia ¿No encuentras tu país? Escríbenos a info@dresslikemommy.com ; quizás podamos gestionar el envío. ⏰ Tiempo de procesamiento Los pedidos se procesan en un plazo
- `shipping_info`: para todas las familias. 🌍A dónde enviamos Estados Unidos — los 50 estados y territorios Canadá Reino Unido Australia ¿No encuentras tu país? Escríbenos a info@dresslikemommy.com ; quizás podamos gestionar el envío. ⏰ Tiempo de procesamiento Los pedidos se procesan en un plazo de 2 a 3 días hábiles tras el pago. Durante temporadas altas (vacaciones, grandes

### IT - Italy

- Expected storefront language route: `it` (Italian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| home | 500 | en | - | https://www.dresslikemommy.com/it | readable |
| product | 429 | en | - | https://www.dresslikemommy.com/it/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |

### RO - Romania

- Expected storefront language route: `ro` (Romanian)
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| skipped_after_blocker |  | - | - |  | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |

### PT - Portugal

- Expected storefront language route: `pt-BR` (Portuguese (Brazil))
- Expected market currency from admin packet: `EUR`

| Page | HTTP | HTML lang | Currency meta | URL | Finding |
| --- | ---: | --- | --- | --- | --- |
| skipped_after_blocker |  | - | - |  | SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429 |

## Findings

- Live outbound checkout delivery-rate lookup returned rates for 0 of 5 target countries.
- Countries blocked by storefront rate limit/bot protection: NL, ES, IT, RO, PT.
- Countries with no rates returned: none.
- Countries with checkout address/rate validation failures: none.
- Policy/shipping pages with limited-country copy: ES:shipping_info.
- Portugal route failures in this run: none.

## Next Safe Action

Keep NL/ES/IT/RO/PT out of live paid spend until the parent integrates this with policy-copy repair and localized landing-page review. If policy copy is repaired, rerun this lane once, slowly, and then perform a human browser checkout walkthrough through the shipping step only.

## Artifacts

- `slow_checkout_qa.py`
- `checkout_probe_raw.json`
- `CHECKOUT_QA.md`
