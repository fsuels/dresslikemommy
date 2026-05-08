# Localized Policy / Shipping Info Cleanup

Date: 2026-05-07 local / 2026-05-08 UTC

## Scope

Approved live public-copy cleanup only:

- Shopify Admin translation resource `gid://shopify/ShopPolicy/29845782625`, key `body`.
- Shopify Admin translation resource `gid://shopify/Page/86424617057`, key `body_html`.
- Locales: `es`, `it`, `ro`, `pt-BR`.

No paid import, no spend, no campaign create/enable/status/budget/bid/conversion-goal changes, no Merchant upload/feed/product-scope/feed-label/product-group changes, no Shopify product data, no shipping-rate or Market changes, no theme publish, no checkout/order/payment action.

## Critical Corrections Preserved

- Dress Like Mommy is an online dropshipping store.
- No physical store, no warehouse/owned inventory, no local inventory, and no in-store pickup claims were added.
- Return shipping remains customer-paid. Outbound checkout delivery rates are not return postage.

## Pre-Cleanup Slow Public Readback

Command:

```bash
python3 ops/scripts/apply_localized_shipping_policy_cleanup.py --public-only --public-stage pre-cleanup-slow-public-readback --cooldown-seconds 120 --public-delay-seconds 15
```

Result:

- No HTTP `429`.
- English `/policies/shipping-policy` and `/pages/shipping-info` were clean after cooldown.
- ES/IT/RO/PT Shipping Info public pages still served stale worldwide/four-country translated copy.
- IT Shipping Policy still served stale translated four-country copy.

## Admin Translation Write

Command:

```bash
python3 ops/scripts/apply_localized_shipping_policy_cleanup.py --execute --skip-public --approval-note "Owner approved separate localized policy/page cleanup for ES/IT/RO/PT after cooldown; no international import or spend."
```

Applied:

- Shipping Policy translations registered for `es`, `it`, `ro`, `pt-BR`.
- Shipping Info page body translations registered for `es`, `it`, `ro`, `pt-BR`.
- `translationsRegister` result count: `4` policy rows + `4` page rows.

Admin readback:

- All 8 target translations exist.
- All 8 read `outdated=false`.
- All 8 have `blocker_hits=[]`.
- All 8 include checkout-availability wording.

## Post-Cleanup Slow Public Readback

Command:

```bash
python3 ops/scripts/apply_localized_shipping_policy_cleanup.py --public-only --public-stage post-cleanup-slow-public-readback --cooldown-seconds 60 --public-delay-seconds 15
```

Result:

- All checked public URLs returned HTTP `200`.
- No HTTP `429`.

Public pages clean or partly clean:

- English Shipping Policy: clean.
- English Shipping Info: clean.
- Spanish Shipping Policy: localized and clean.
- Romanian Shipping Info: localized and clean.
- Romanian Shipping Policy: English fallback but clean, with no stale blocker phrases.
- Portuguese Shipping Policy: English fallback but clean, with no stale blocker phrases.

Public pages still stale after immediate post-write readback:

- Spanish Shipping Info still showed stale "familias de todo el mundo" / "envío gratis en cada pedido" copy.
- Italian Shipping Policy still showed stale "Attualmente spediamo a" / "Non riesci a trovare il tuo Paese" copy.
- Italian Shipping Info still showed stale "famiglie di tutto il mondo" / "spedizione gratuita per ogni ordine" copy.
- Portuguese Shipping Info still showed stale "famílias em todo o mundo" / "Frete Grátis em Todos os Pedidos" copy.

Interpretation:

- Shopify Admin native translation source is clean.
- Public storefront serving is not fully caught up, or another translation/cache layer is overriding some public page bodies.
- A read-only query found no Eurozone market-specific translation overrides for the checked resources.

## Evidence Paths

- Script: `ops/scripts/apply_localized_shipping_policy_cleanup.py`
- Plan: `localized-policy-page-cleanup/translation_plan.json`
- Execute summary: `localized-policy-page-cleanup/summary.json`
- Pre-public readback: `localized-policy-page-cleanup/pre-cleanup-slow-public-readback/readback.json`
- Post-public readback: `localized-policy-page-cleanup/post-cleanup-slow-public-readback/readback.json`
- Target translation HTML: `localized-policy-page-cleanup/target-translations/`
- Before translation HTML where present: `localized-policy-page-cleanup/before-translations/`

## Decision

Do not import or spend internationally yet.

Next closest safe action is a later slow read-only recheck of only the still-stale public URLs. If they remain stale after a longer cache window, inspect Translate & Adapt / translation app / storefront translation-serving layer for overrides before any paid international launch.
