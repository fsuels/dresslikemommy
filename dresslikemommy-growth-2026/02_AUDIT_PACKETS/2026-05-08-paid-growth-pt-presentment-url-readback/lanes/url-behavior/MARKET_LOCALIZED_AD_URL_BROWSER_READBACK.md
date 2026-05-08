# Market-Localized Ad URL Browser Readback

Generated: 2026-05-08 01:02 EDT

Lane: Parent browser readback for paid ad URL entry behavior.

## Scope

Investigate how a fresh paid visitor can land in the intended country/currency/locale without first using the storefront selector.

No Shopify Admin, Markets, theme, Ads, Merchant, Pinterest, cart, checkout, payment, or order writes were made in this lane. Browser tests were limited to product landing-page reads except for the separate PT checkout lane.

## Key Finding

Bare language routes are not safe enough as paid final URLs. A fresh `/pt/products/...` URL without a country parameter redirected to the base `/products/...` route and presented English / United States / USD.

Adding Shopify's `country` query parameter to the localized language route did force the target market/currency in fresh isolated browser contexts:

| Test URL Pattern | Fresh Browser Result | Status |
|---|---|---|
| `/pt/products/...?...` with no `country` | Redirected to `/products/...`; English; `United States | USD $`; product price `$27.99 USD` | Not safe for PT ad final URL |
| `/pt/products/...?variant=...&country=PT` | Stayed localized; `html lang=pt-BR`; `Portugal | EUR €`; product price `€24,95 EUR` | Passed product landing readback |
| `/pt/products/...?variant=...&country=PT&currency=EUR` | Same as above; `country=PT` was sufficient in this readback | Passed product landing readback |
| `/es/products/...?variant=...&country=ES` | `html lang=es`; `España | EUR €`; product price `€24,95 EUR` | Passed product landing readback |
| `/it/products/...?variant=...&country=IT` | `html lang=it`; `Italia | EUR €`; product price `€24,95 EUR` | Passed product landing readback |
| `/ro/products/...?variant=...&country=RO` | `html lang=ro`; `România | RON Lei`; product price `128,00 RON` | Passed product landing readback |

## Localization Mechanics Observed

- The live storefront uses native Shopify localization forms posting to `/localization` or localized `/pt/localization`.
- Relevant form fields are `country_code`, `locale_code`, `_method=put`, and `return_to`.
- After successful localization, browser cookie names included `localization` and `cart_currency`. Cookie values were not recorded.
- Product pages with `country=PT`, `country=ES`, `country=IT`, or `country=RO` set the corresponding storefront country/currency on first load in fresh isolated contexts.

## Paid URL Implication

For paused international Search drafts, do not use bare language-only final URLs such as:

```text
https://www.dresslikemommy.com/pt/products/<handle>
```

Use a country-qualified localized final URL template instead:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?country=<ISO_COUNTRY>
```

If a variant parameter is needed, preserve it first and append country after it:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?variant=<VARIANT_ID>&country=<ISO_COUNTRY>
```

Observed target mappings from this readback:

| Market | Locale path | Country parameter | Observed currency |
|---|---|---|---|
| Spain | `/es` | `country=ES` | EUR |
| Italy | `/it` | `country=IT` | EUR |
| Romania | `/ro` | `country=RO` | RON |
| Portugal | `/pt` | `country=PT` | EUR |

## Remaining Risk

- This proves landing-page product presentment, not full checkout for every market. PT full checkout was separately cleared in `lanes/pt-checkout/PT_CHECKOUT_TO_SHIPPING_READBACK.md`; ES/IT/RO were cleared in the previous anchor after storefront localization.
- Any future Ads import still needs exact owner approval and just-in-time preview/readbacks.
- If Shopify changes Markets behavior or URL parameter handling, rerun this readback before using the URL template in live ads.
