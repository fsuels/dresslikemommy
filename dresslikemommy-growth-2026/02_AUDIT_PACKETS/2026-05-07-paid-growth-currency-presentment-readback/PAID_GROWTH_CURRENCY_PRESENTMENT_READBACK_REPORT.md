# Paid Growth Currency / Presentment Readback Report

Generated: 2026-05-08 00:30 EDT

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-currency-presentment-readback`

## Scope

Owner request: run read-only ES/IT/RO/PT currency/presentment investigation with a browser walkthrough to the shipping step only; no payment and no order. Keep Merchant/Pinterest monitoring parallel, and keep Ads import parked until exact approval.

Guardrails preserved: no live spend, campaign import/create/enable/pause, budget/bid/status/conversion-goal/product-scope/feed-label/product-group changes, PMax/Standard Shopping changes, Merchant upload, source refresh/sync, Google & YouTube product toggle, Shopify product data, local inventory artifacts/claims, Shopify Markets/shipping-rate changes, Pinterest drafts/spend, payment submission, or order creation.

## Lane Board

- Moving: final integration and continuity update.
- Blocked: PT browser checkout proof is blocked by storefront `429`; Merchant paid-cohort age group remains at `623`; Pinterest drafts remain blocked; Ads import remains approval-gated.
- Waiting on approval: any Ads import, Shopify Markets/currency fix, Merchant source refresh/sync/product toggle, Pinterest draft, or live spend.
- Done: ES/IT/RO browser shipping-step readbacks; PT product presentment readback; Merchant monitor; Pinterest monitor; Ads parked gate.
- Next safe parallel action: PT-only cooldown retry plus market-localization URL investigation; continued Merchant/Pinterest read-only monitoring.

## Parent Currency / Presentment Findings

Lane report: `lanes/currency/CURRENCY_PRESENTMENT_BROWSER_READBACK.md`

The prior endpoint-only readback showed USD because it did not set storefront market localization. Browser evidence shows presentment can correct after the storefront country/locale selector is set, but direct localized URLs alone are not reliable in a fresh visitor context.

| Country | Browser presentment after localization | Checkout shipping-step result | Status |
|---|---|---|---|
| ES | Product/cart EUR | Spain, `Madrid Province`, Standard Delivery `FREE`, Express `EUR 11.95`, total EUR | Reached shipping step; no payment |
| IT | Product/cart EUR | Italy, `Rome`, Standard Delivery `FREE`, Express `EUR 11.95`, total EUR | Reached shipping step; no payment |
| RO | Product/cart RON | Romania, `Bucharest`, Standard Delivery `FREE`, Express `60.00 lei`, total RON | Reached shipping step; no payment |
| PT | Product EUR | Not reached; `/cart/add.js` and one UI add-to-cart retry returned `429` | Blocked before checkout |

Important nuances:

- Fresh direct routes `/es`, `/it`, `/ro`, and `/pt` first landed in English / US / USD in isolated browser contexts.
- Storefront localization corrected product presentment for all four product pages.
- ES/IT/RO checkout pages remained mostly English (`en-ES`, `en-IT`, `en-RO`) even when product/cart pages were localized.
- RO uses RON in the live browser, not EUR. Treat future RO economics as RON/local-currency unless Admin confirms a different intended behavior.
- PT is not cleared for checkout presentment because storefront cart add hit `429`; do not infer PT checkout currency from the product page alone.

Decision: `INTERNATIONAL_PAID_STILL_NOT_READY`.

## Merchant Monitor

Lane report: `lanes/merchant/MERCHANT_CURRENCY_READBACK_MONITOR.md`

Fresh read-only result: `NOT_CLEARED_NO_NEW_IMPROVEMENT`.

- Browser product-issues export succeeded: `34,716` rows.
- Paid-cohort US/en `Missing age group`: still `623` unique item IDs, delta `0` from the prior 23:18 EDT export.
- Sample item `shopify_US_7227254276193_41871113158753` still affected.
- Sample source remains `10627623003` / `Shopify App API`, timestamp `2026-05-07T14:14:02+00:00`.
- Merchant API and Content API product-issues path still blocked by `403 PERMISSION_DENIED` insufficient OAuth scopes.
- `Missing local inventory data` exists in diagnostics but is not a DLM product-data fix target because DLM is dropshipping with no physical store or owned physical inventory.

Decision: keep monitoring read-only; do not repeat toggle, sync/refresh, upload feeds, edit products, or create local-inventory claims without fresh exact approval.

## Pinterest Monitor

Lane report: `lanes/pinterest/PINTEREST_CURRENCY_READBACK_MONITOR.md`

Fresh read-only result: `PINTEREST_US_DRAFTS_STILL_BLOCKED_BUT_ITEM_PROOF_NOW_MOSTLY_CURRENT`.

- Advertiser `549756244483`, catalog `Catalog_Retail`, catalog ID `3041764155561548387`.
- Campaign baseline remains `0 campaigns`, `0 currently being served`, `$0.00` spend.
- Event Quality remains `Fair`, updated `5/6/2026`.
- Events Overview still shows `Api - Tag` standard events.
- EN Shopify source `3041760867124595727`: `5,663/5,663`, `0` failed, `152` warnings.
- Failed sitemap source `3041760916127467912` still failed.
- Full 346-row item metadata proof improved to `337/346` EN-US in-stock; 9 Mommy & Me variants no longer resolve by historical Pinterest pin metadata.

Decision: no Pinterest drafts/spend. Future US-only paused draft should use only the 337 refreshed rows or first re-resolve/exclude the 9 missing variants, then require exact owner approval.

## Ads Parked Gate

Lane report: `lanes/ads-gate/ADS_IMPORT_PARKED_CURRENCY_GATE.md`

Status: `PARKED_NOT_APPROVED_CURRENCY_GATE_BLOCKED`.

- No live Google Ads access or action.
- Local packet still has 17 non-US paused draft campaigns, 204 ad groups, 612 exact/phrase keywords, 629 negatives, 204 RSAs, max CPC `$0.15`, and all bulk rows paused.
- Zero PMax, Standard Shopping, product-scope, feed-label, product-group, or conversion-goal rows.
- Exact owner approval remains required before any preview/import workflow.

Decision: keep Ads parked.

## Residual Risks

- Paid traffic can still land in US/USD if language-route URLs do not force or preserve market selection for fresh visitors.
- Checkout localization is not clean: ES/IT/RO checkout surfaces are still mostly English.
- PT checkout presentment is unverified because storefront cart add hit `429`.
- RO economics must use observed RON presentment unless Shopify Markets settings are changed with approval.
- Merchant paid-cohort age-group issue has stopped improving in the latest two exports.
- Pinterest is closer on item proof but still blocked by Event Quality, warnings, failed sitemap source, localized source quality, and 9 unresolved candidate rows.

## Next Best Action

1. After cooldown, rerun PT only in a fresh browser context: set Portugal / pt-BR through storefront localization, add one item, proceed to checkout, select Portugal / Lisboa, verify shipping rates and currency, stop before payment.
2. Investigate the safest URL/market-localization path for paid traffic so ES/IT/RO/PT shoppers do not land in US/USD by default.
3. Continue Merchant read-only monitoring; do not repeat source refresh/toggle/product/feed work without exact approval.
4. Keep Pinterest drafts/spend parked; use the 337 refreshed EN-US rows or re-resolve/exclude the 9 missing rows before any future paused draft request.
5. Keep Ads import parked until exact owner approval and just-in-time readbacks.
