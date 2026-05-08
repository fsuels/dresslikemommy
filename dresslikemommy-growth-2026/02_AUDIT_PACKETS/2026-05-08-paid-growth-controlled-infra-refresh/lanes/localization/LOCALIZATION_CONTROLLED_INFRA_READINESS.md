# Localization Controlled Infrastructure Readiness

Date: 2026-05-08
Lane: LOCALIZATION
Mode: local/read-only synthesis only

## Decision

`PAUSED_INFRASTRUCTURE_CAN_BE_REFINED_LOCALLY__LIVE_INTERNATIONAL_SPEND_STILL_BLOCKED`

The latest localization evidence supports controlled, paused Google Search infrastructure planning. It does not approve live spend, campaign creation/import, shipping/Markets changes, Shopify Admin writes, theme publish, checkout payment, or order creation.

## Evidence Used

- `ops/AGENT_COORDINATION.md`: active controlled-infra lane allows local/read-only evidence and public URL QA only.
- `ops/AGENT_WORKLOG.md`: latest paid-growth anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-pt-presentment-url-readback`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/url-behavior/MARKET_LOCALIZED_AD_URL_BROWSER_READBACK.md`: country-qualified localized URLs passed for ES, IT, RO, PT.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/pt-checkout/PT_CHECKOUT_TO_SHIPPING_READBACK.md`: PT checkout-to-shipping passed with EUR, Lisboa, free standard shipping, express EUR 11.95, no payment/order.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/currency/CURRENCY_PRESENTMENT_BROWSER_READBACK.md`: ES/IT/RO checkout-to-shipping passed after storefront localization; RO presents RON.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/localization/LOCALIZATION_PUBLIC_RECHECK.md`: previously stale localized shipping/policy URLs cleared public-copy gate.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/country_tier_plan.csv`: initial country tier plan and paused-shell posture.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/measurement/MEASUREMENT_CONTROLLED_READBACK.md`: spend/import still needs just-in-time measurement, Merchant, Pinterest, storefront, and economics readbacks.

## URL Rule

Bare language-only paths are not safe final URLs for ES, IT, RO, or PT paid traffic. Fresh browser readback showed language-only routes can start as English / United States / USD.

Use country-qualified localized product URLs for those markets:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?country=<ISO_COUNTRY>
```

If a variant is required:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?variant=<VARIANT_ID>&country=<ISO_COUNTRY>
```

Observed mappings:

| Market | Recommended localized path | Country parameter | Observed presentment |
|---|---|---|---|
| Spain | `/es/products/<handle>` | `country=ES` | Spanish / EUR |
| Italy | `/it/products/<handle>` | `country=IT` | Italian / EUR |
| Romania | `/ro/products/<handle>` | `country=RO` | Romanian / RON |
| Portugal | `/pt/products/<handle>` | `country=PT` | pt-BR / EUR |

## Readiness Matrix

| Market | Final URL recommendation | Currency / presentment evidence | Shipping / policy readiness | Paid-traffic readiness | Blockers |
|---|---|---|---|---|---|
| US | Existing English landing set; do not duplicate existing paused US nonbrand campaign. | Trusted USD purchase-measurement evidence exists for US. | English source policy/page copy clean in latest continuity. | Existing governed US infrastructure only; activation still approval-gated. | Standard Shopping/Brand/US Search guardrails; live changes require approval. |
| GB | English-first product or collection URLs; add `country=GB` only after action-time readback. | Not freshly read back in this lane. | English policy copy clean; country checkout/shipping not freshly verified. | Safe for paused English-first infrastructure after approval; not live spend. | Need GB presentment, shipping, Merchant/Pinterest, economics, and Ads readbacks. |
| CA | English-first product or collection URLs; French Canada deferred. Add `country=CA` only after action-time readback. | Not freshly read back in this lane. | English policy copy clean; country checkout/shipping not freshly verified. | Safe for paused English-first infrastructure after approval; not live spend. | Need CA presentment, shipping, French-language decision, Merchant/Pinterest, economics, and Ads readbacks. |
| AU | English-first product or collection URLs; add `country=AU` only after action-time readback. | Not freshly read back in this lane. | English policy copy clean; country checkout/shipping not freshly verified. | Safe for paused English-first infrastructure after approval; not live spend. | Need AU presentment, shipping/delivery clarity, Merchant/Pinterest, economics, and Ads readbacks. |
| CH | English-only paused shell for now; local German/French/Italian variants deferred. | Not freshly read back. | English policy copy clean; country checkout/shipping not freshly verified. | Paused shell only; local-language traffic not ready. | Need CH route, language, currency, duties/returns clarity, checkout, catalog, tracking, economics. |
| DK | English-only paused shell for now; Danish variant deferred. | Not freshly read back. | English policy copy clean; country checkout/shipping not freshly verified. | Paused shell only; local-language traffic not ready. | Need DK route, currency, Danish landing quality, shipping clarity, catalog, tracking, economics. |
| DE | English-only paused shell for now; German variant deferred. | Not freshly read back. | English policy copy clean; German policy/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need DE German route, shipping/returns/duties clarity, checkout, catalog, tracking, economics. |
| NL | English-only paused shell for now; Dutch variant deferred. | Earlier no-payment rate evidence exists, but no fresh country-qualified URL readback in latest packet. | English policy copy clean; localized Dutch paid landing readiness not cleared. | Paused shell only; local-language traffic not ready. | Need NL country-qualified URL, currency, checkout, Dutch landing quality, catalog, tracking, economics. |
| SE | English-only paused shell for now; Swedish variant deferred. | Not freshly read back. | English policy copy clean; Swedish policy/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need SE route, currency, Swedish landing quality, shipping clarity, catalog, tracking, economics. |
| FR | English-only paused shell for now; French variant deferred. | Not freshly read back. | English policy copy clean; French policy/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need FR French route, shipping/returns/duties clarity, checkout, catalog, tracking, economics. |
| BE | English-only paused shell for now; French/Dutch variants deferred. | Not freshly read back. | English policy copy clean; Belgium checkout/shipping not freshly verified. | Paused shell only; local-language traffic not ready. | Need BE route, language split, currency, checkout, catalog, tracking, economics. |
| ES | Use `/es/products/<handle>?country=ES` or `?variant=<VARIANT_ID>&country=ES`. | Passed product landing as Spain / Spanish / EUR; checkout-to-shipping previously carried EUR after localization. | Localized public shipping-info page cleared stale-copy gate; checkout reached shipping step with Spain / Madrid Province, free standard, express EUR 11.95. | Strongest localized paused-infra candidate with IT/PT, but live spend still blocked. | Need Ads final URL update/readback, Merchant/Pinterest catalog health, tracking/economics, exact approval. |
| IT | Use `/it/products/<handle>?country=IT` or `?variant=<VARIANT_ID>&country=IT`. | Passed product landing as Italy / Italian / EUR; checkout-to-shipping previously carried EUR after localization. | Localized Shipping Policy and Shipping Info pages cleared stale-copy gate; checkout reached shipping step with Italy / Rome, free standard, express EUR 11.95. | Strongest localized paused-infra candidate with ES/PT, but live spend still blocked. | Need Ads final URL update/readback, Merchant/Pinterest catalog health, tracking/economics, exact approval. |
| PL | English-only paused shell for now; Polish variant deferred. | Not freshly read back. | English policy copy clean; Polish route/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need PL route, currency, Polish landing quality, shipping/returns/duties clarity, catalog, tracking, economics. |
| CZ | English-only paused shell for now; Czech variant deferred. | Not freshly read back. | English policy copy clean; Czech route/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need CZ route, currency, Czech landing quality, checkout, catalog, tracking, economics. |
| RO | Use `/ro/products/<handle>?country=RO` or `?variant=<VARIANT_ID>&country=RO`. | Passed product landing as Romania / Romanian / RON; checkout-to-shipping previously carried RON after localization. | Checkout reached shipping step with Romania / Bucharest, free standard, express 60.00 lei. | Localized paused-infra candidate; economics must use RON, not EUR. Live spend blocked. | Need RO final URL update/readback, RON economics, Merchant/Pinterest catalog health, tracking, exact approval. |
| GR | English-only paused shell for now; Greek variant deferred. | Not freshly read back. | English policy copy clean; Greek route/checkout not freshly verified. | Paused shell only; local-language traffic not ready. | Need GR route, currency, Greek landing quality, shipping/returns/duties clarity, catalog, tracking, economics. |
| PT | Use `/pt/products/<handle>?country=PT` or `?variant=<VARIANT_ID>&country=PT`. | Passed product landing as Portugal / pt-BR / EUR; PT checkout-to-shipping passed on 2026-05-08. | PT Shipping Info cleared stale-copy gate; checkout reached Portugal / Lisboa with Standard `GRATIS`, Express EUR 11.95, total EUR 24.95. | Strongest localized paused-infra candidate with ES/IT, but live spend still blocked. | Need Ads final URL update/readback, Merchant/Pinterest catalog health, tracking/economics, exact approval. |

## Status Counts

- Existing governed US template: 1 market.
- English-first paused infrastructure candidates with latest continuity support: GB, CA, AU.
- Country-qualified localized paused-infra candidates with direct product URL evidence: ES, IT, RO, PT.
- English-only shell markets needing local-language/shipping QA before local-language paid traffic: CH, DK, DE, NL, SE, FR, BE, PL, CZ, GR.
- Live-spend-ready international markets: 0.

## Guardrails Preserved

- No Shopify Admin write.
- No theme publish.
- No shipping, Markets, currency, product, Merchant, Pinterest, Google Ads, campaign, budget, bid, status, conversion-goal, product-scope, product-group, or feed-label write.
- No checkout payment.
- No order created.
- No public checkout/browser run was performed in this lane; this is a synthesis from existing evidence.

## Next Safe Actions

1. Update the paused international Search local packet only if the Ads lane owns that file scope, replacing ES/IT/RO/PT bare language URLs with `country=<ISO_COUNTRY>` templates.
2. Before any approved Ads import, preview-only validate final URLs, all entities paused, CPC caps, locations, languages, negatives, and conversion-goal inheritance.
3. Run fresh country-level storefront readbacks for GB/CA/AU before considering enablement, even if paused English-first shells are approved.
4. Do not enable international spend until Merchant/Pinterest catalog health, tracking readbacks, economics, and exact owner approval all clear.
