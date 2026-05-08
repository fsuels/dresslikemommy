# Localization Public Recheck

Date: 2026-05-07 EDT / 2026-05-08 UTC

## Scope

Read-only public storefront recheck for only the four previously stale URLs:

- `https://www.dresslikemommy.com/es/pages/shipping-info`
- `https://www.dresslikemommy.com/it/policies/shipping-policy`
- `https://www.dresslikemommy.com/it/pages/shipping-info`
- `https://www.dresslikemommy.com/pt/pages/shipping-info`

No Shopify Admin writes, no theme/product/shipping/market changes, no checkout payment, and no order action.

## Method

- Requested each URL once with a 75-second delay between storefront requests.
- Stopped only if HTTP `429` appeared. It did not appear.
- Saved raw HTML and request metadata in this lane folder.
- Reprocessed the saved HTML locally with the existing public-page text cleaner from `ops/scripts/apply_localized_shipping_policy_cleanup.py`; the processed JSON is the canonical visible-text readback.

## Result

All four previously stale public URLs now pass the public copy gate.

| URL | HTTP | Stale Blocker Phrases | Checkout-Availability Wording | Fallback / Language Behavior | 429 / CAPTCHA |
|---|---:|---|---|---|---|
| `/es/pages/shipping-info` | `200` | None | Present | Localized Spanish | None visible |
| `/it/policies/shipping-policy` | `200` | None | Present | Localized Italian | None visible |
| `/it/pages/shipping-info` | `200` | None | Present | Localized Italian | None visible |
| `/pt/pages/shipping-info` | `200` | None | Present | Localized Portuguese | None visible |

## Visible Text Signals

- Spanish Shipping Info no longer shows stale `familias de todo el mundo` / `envío gratis en cada pedido` copy.
- Italian Shipping Policy no longer shows stale `Attualmente spediamo a` / `Non riesci a trovare il tuo Paese` copy.
- Italian Shipping Info no longer shows stale `famiglie di tutto il mondo` / `spedizione gratuita per ogni ordine` copy.
- Portuguese Shipping Info no longer shows stale `famílias em todo o mundo` / `Frete Grátis em Todos os Pedidos` copy.
- All four pages now use checkout-availability wording and avoid physical-store, warehouse, local-inventory, or in-store-pickup claims.

## Evidence

- Canonical parsed readback: `public_recheck_processed.json`
- Raw request metadata: `public_recheck_raw.json`
- Raw HTML: `raw/*.html`
- Clean visible text extracts: `clean-text/*.txt`

Note: `public_recheck_raw.json` includes first-pass parser fields from the fetch command. Use `public_recheck_processed.json` for the canonical visible-text blocker/CAPTCHA assessment because it was reprocessed from the saved HTML with the existing repo cleaner and no additional storefront requests.

## Decision

The four stale localized public pages are no longer the blocker. International paid launch is still not automatically cleared by this lane alone; route/currency, no-payment checkout QA, tracking, catalog/feed health, and owner approval gates still need to pass before live spend.
