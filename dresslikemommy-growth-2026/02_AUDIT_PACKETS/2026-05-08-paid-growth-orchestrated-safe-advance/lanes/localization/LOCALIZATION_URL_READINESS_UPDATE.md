# Localization URL Readiness Update

Date: 2026-05-08
Mode: public storefront read-only; no checkout payment, order, admin, theme, or translation write

## Result

Country-qualified URLs are sufficient for product-page country/currency presentment in the current paid tiers. Bare language URLs are not sufficient because they can render the language path while keeping `Shopify.country=US` and `USD`.

Use:

- English-first shells: `/products/<handle>?variant=<id>&country=<ISO>`.
- Localized shells: `/<locale>/products/<handle>?variant=<id>&country=<ISO>`.

## Readiness Matrix

| Market | Paused Infrastructure | Product URL Readiness | Still Needed Before Live Spend |
|---|---|---|---|
| US | Existing governed infrastructure only | Existing English routes | No duplicate build; approval for any live change |
| GB, CA, AU | Safe for paused English-first shells | `?country=` passed: GBP/CAD/AUD | Browser no-payment checkout/shipping QA |
| ES, IT, PT | Safe for localized paused shells | `/es`, `/it`, `/pt` + `country=` passed; prior checkout gates passed | Merchant/Pinterest/tracking/economics/approval |
| RO | Safe for localized paused shell | `/ro` + `country=RO` passed; RON confirmed | RON economics and normal gates |
| CH | Safe for paused English shell; localized probes passed product-level | Base `country=CH` and `/de|fr|it?...country=CH` passed CHF | No-payment checkout QA |
| DK, DE, NL, SE, FR, BE, PL, CZ, GR | Safe for paused English shells; localized product probes passed | Base `country=` passed; localized probes matched country/currency | Browser no-payment QA, policy/language quality, duties/returns clarity |

## Residual Risk

Product-page presentment is not full checkout proof. GB/CA/AU should be the next no-payment checkout QA priority, then CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR.

