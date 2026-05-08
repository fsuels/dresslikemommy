# Paid Growth PT Presentment / URL Readback Report

Generated: 2026-05-08 01:20 EDT

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-pt-presentment-url-readback`

## Scope

Owner request: continue from `AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-currency-presentment-readback`; run PT-only browser checkout-to-shipping after cooldown; investigate market-localized ad URL behavior; keep Merchant/Pinterest read-only monitoring parallel; keep Ads import parked until exact approval.

Guardrails preserved: no live spend, campaign import/create/enable/pause, budget/bid/status/conversion-goal/product-scope/feed-label/product-group changes, PMax/Standard Shopping/Remarketing changes, Merchant upload, source refresh/sync, Google & YouTube product toggle, Shopify product data, local inventory feed/claim, Shopify Markets/currency/shipping-rate change, theme publish, Pinterest draft/spend, payment submission, or order creation.

## Lane Board

- Moving: final continuity update.
- Blocked: Merchant exact fresh product-issues CSV count; Merchant API scopes; Pinterest Event Quality/catalog draft gate; Ads import approval.
- Waiting on approval: Ads import/preview, Merchant refresh/sync/toggle/upload/product-data repair, Shopify Markets/theme URL helper, Pinterest draft/spend, and any live spend.
- Done: PT checkout-to-shipping; market-localized ad URL browser readback; Merchant read-only monitor parked with evidence; Pinterest read-only monitor; Ads parked gate; local theme URL analysis.
- Next safe parallel action: keep Ads import parked; run later Merchant read-only export retry; use country-qualified localized URLs in any future paused Ads packet update; keep Pinterest drafts parked or scope to resolved rows only after approval.

## PT Checkout-To-Shipping

Lane report: `lanes/pt-checkout/PT_CHECKOUT_TO_SHIPPING_READBACK.md`.

Status: `PASSED_READONLY_NO_PAYMENT_NO_ORDER`.

- Fresh direct `/pt/products/...` without country parameter redirected to the non-localized product path and presented English / United States / USD.
- After native storefront localization to Portugal / `pt-BR`, product presented `Portugal | EUR €`, `Português (brasil)`, and `€24,95 EUR`.
- Add to cart passed after cooldown. Network readback showed `POST /pt/cart/add` returned `200`; the prior `429` blocker did not recur.
- Cart drawer showed one item and total `€24,95 EUR`.
- Checkout opened in Portuguese at a redacted `/checkouts/cn/REDACTED/pt-br` path with `html lang=pt-BR`.
- Delivery country preselected as Portugal; region accepted `Lisboa`.
- Shipping methods loaded:
  - `Entrega padrão (10 a 14 dias)` / `GRÁTIS`.
  - `Entrega expressa (7 a 11 dias)` / `€ 11,95`.
- Order summary showed subtotal `€ 24,95`, shipping `GRÁTIS`, total `EUR € 24,95`.
- Payment section was visible because Shopify one-page checkout renders payment fields after shipping info, but no payment fields were entered and `Pagar agora` was not clicked. Browser readback found no order-confirmation text.

Evidence screenshots:

- `screenshots/pt-direct-language-route-baseline.png`
- `screenshots/pt-localized-product-eur.png`
- `screenshots/pt-localized-cart-eur.png`
- `screenshots/pt-checkout-shipping-rates-eur.png`

## Market-Localized Ad URL Behavior

Lane reports:

- Parent browser: `lanes/url-behavior/MARKET_LOCALIZED_AD_URL_BROWSER_READBACK.md`
- Local sidecar: `lanes/url-behavior/LOCALIZATION_THEME_URL_ANALYSIS.md`

Key result: bare language-only final URLs are not safe enough for fresh paid traffic, but the native Shopify `country` query parameter successfully forced correct market/currency in fresh browser product-page readbacks.

| Pattern | Fresh result |
|---|---|
| `/pt/products/...?...` without `country` | Redirected to base `/products/...`; English / United States / USD |
| `/pt/products/...?variant=...&country=PT` | Portugal / `pt-BR` / EUR |
| `/pt/products/...?variant=...&country=PT&currency=EUR` | Portugal / `pt-BR` / EUR; `country=PT` was sufficient in this readback |
| `/es/products/...?variant=...&country=ES` | Spain / Spanish / EUR |
| `/it/products/...?variant=...&country=IT` | Italy / Italian / EUR |
| `/ro/products/...?variant=...&country=RO` | Romania / Romanian / RON |

Recommended final URL template for any future paused international Search packet update:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?country=<ISO_COUNTRY>
```

If a variant parameter is used:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?variant=<VARIANT_ID>&country=<ISO_COUNTRY>
```

Do not import or apply Ads URLs from this packet without exact owner approval and just-in-time preview/readbacks.

## Merchant Monitor

Lane report: `lanes/merchant/MERCHANT_PT_URL_READBACK_MONITOR.md`.

Status: `PARKED_ON_USER_STOP_EXPORT_BLOCKED`.

- Merchant account visible: `Dresslikemommy` / `124884876`.
- Fresh read-only sample source readback at `2026-05-08T01:06:10`.
- Sample item `shopify_US_7227254276193_41871113158753` still shows US/en source `10627623003` / `Shopify App API`.
- Sample source timestamp remains `2026-05-07T14:14:02+00:00`, still older than the Shopify age-group repair.
- Visible Merchant diagnostics timestamp: `Last updated at 1:02 AM May 8, 2026`.
- Visible diagnostics still show `Missing age group` and `Missing local inventory data`.
- Fresh exact paid-cohort CSV count was not obtained because the UI showed `Ready to download` but no CSV materialized before the lane was stopped.
- Latest exact completed count remains prior evidence: `623` paid-cohort US/en unique item IDs, with the sample still affected.
- Merchant API and Content API product-issues paths remain blocked by `403 PERMISSION_DENIED` insufficient OAuth scopes.

`Missing local inventory data` remains a non-fix target for DLM. The business is dropshipping with no physical store and no owned inventory; do not create local inventory feeds, local-stock/store/warehouse claims, pickup claims, or guaranteed on-hand inventory claims.

## Pinterest Monitor

Lane report: `lanes/pinterest/PINTEREST_PT_URL_READBACK_MONITOR.md`.

Status: `PINTEREST_DRAFTS_AND_SPEND_STILL_PARKED`.

- Advertiser `549756244483`; catalog `Catalog_Retail`; catalog ID `3041764155561548387`.
- Campaign baseline remains `0 campaigns`, `0 currently being served`, `$0.00` spend.
- Event Quality remains `Fair`, updated `2026-05-06`.
- Fresh API readback showed latest Tag/CAPI conversion-source timestamps around `2026-05-08T04:58Z`.
- Remaining top action items: `click_id_epik` in Checkout, `product_id` in AddPaymentInfo, and `hashed_email` in AddToCart.
- EN Shopify source `3041760867124595727`: completed `5,663/5,663`, `0` failed, `152` warnings.
- Failed sitemap source `3041760916127467912` remains failed.
- Full item proof remains `337/346` EN-US in-stock; the same `9` missing Mommy & Me variants from product `7229026304097` remain unresolved.

No Pinterest campaigns, drafts, product groups, catalogs, audiences, budgets, bids, pixels/tags/CAPI paths, or spend changes were made.

## Ads Parked Gate

Lane report: `lanes/ads-gate/ADS_IMPORT_PARKED_PT_URL_GATE.md`.

Status: `PARKED_NOT_APPROVED`.

- No live Google Ads access or action.
- Local draft remains paused-only if ever approved: `17` non-US paused draft campaigns, `204` ad groups, `612` exact/phrase positive keywords, `629` negatives, `204` RSAs, `1666` bulk rows.
- Max CPC remains `$0.15`; `0` CPC values over `$0.20`.
- All importable entities are paused; `0` broad positive keywords.
- Found `0` PMax, Standard Shopping, product-scope, feed-label, product-group, or conversion-goal edit rows.

Ads import remains parked until exact owner approval. Even paused campaign creation is a live write.

## Decision

Portugal now clears the same no-payment checkout-to-shipping presentment gate as ES/IT/RO, and market-localized product landing URLs have a safer native pattern: localized path plus `country=<ISO_COUNTRY>`.

International paid remains `NOT_APPROVED_FOR_LIVE_IMPORT_OR_SPEND`: Merchant is not cleared, Pinterest remains blocked, Ads import is not approved, and any campaign import or URL update requires exact owner approval with just-in-time readbacks.

## Residual Risks

- `country=<ISO>` was validated on product landing pages, not every possible collection/product URL and not every checkout path.
- Checkout language is acceptable for PT in this readback, but ES/IT/RO checkout pages previously remained mostly English despite correct currency.
- RO correctly presents in RON, not EUR; RO economics should use RON/local pricing.
- Merchant paid-cohort age-group issue remains unresolved at the exact-count level; latest exact count is still `623`.
- Pinterest Event Quality remains Fair and catalog item proof is incomplete.

## Next Best Action

1. Keep Ads import parked. If owner gives exact approval, first update/validate the paused Ads URL template to include `country=<ISO_COUNTRY>`, then run preview-only import and just-in-time readbacks.
2. Retry Merchant read-only product-issues export later; do not click source refresh/sync, upload, product toggle, or product-data/local-inventory fixes without exact approval.
3. Keep Pinterest drafts/spend parked; a future US-only paused draft should use only the `337` resolved EN-US in-stock rows or first re-resolve/exclude the `9` missing variants.
4. Do not launch international spend until Merchant/Pinterest/tracking/economics and approval gates clear.
