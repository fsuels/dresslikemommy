# Next Continuation Prompt - Paid Growth Currency / Presentment

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as canonical operating prompt. Before spawning subagents or using browser/account tabs, read `AGENTS.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the latest `ops/AGENT_WORKLOG.md` entries.

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-currency-presentment-readback`

Evidence packet:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/`

Current state:

- Parent browser presentment investigation found that direct localized URLs alone are not enough: fresh `/es`, `/it`, `/ro`, and `/pt` product-route browser contexts first landed on English / United States / USD.
- After using the storefront localization form:
  - ES product/cart/checkout shipping step presented EUR; Standard Delivery was free and Express was `EUR 11.95`; checkout country Spain / region `Madrid Province`.
  - IT product/cart/checkout shipping step presented EUR; Standard Delivery was free and Express was `EUR 11.95`; checkout country Italy / province `Rome`.
  - RO product/cart/checkout shipping step presented RON; Standard Delivery was free and Express was `60.00 lei`; checkout country Romania / county `Bucharest`.
  - PT product page presented Portugal / EUR, but checkout could not be reached because `/cart/add.js` returned `429` and one UI add-to-cart retry also returned `429`.
- No payment was submitted and no order was created.
- ES/IT/RO checkout text remained mostly English (`en-ES`, `en-IT`, `en-RO`) even when product/cart pages were localized.
- Merchant monitor is still not cleared: paid-cohort US/en `Missing age group` remains `623` unique item IDs, unchanged from the previous export; sample item `shopify_US_7227254276193_41871113158753` is still affected; source remains `10627623003` / `Shopify App API` timestamp `2026-05-07T14:14:02+00:00`; Merchant API path still blocked by `403 PERMISSION_DENIED`.
- `Missing local inventory data` is not a product-data fix target. DLM is dropshipping with no physical store and no owned physical inventory. Do not create local inventory feeds, local stock claims, warehouse claims, store pickup claims, or guaranteed on-hand inventory claims.
- Pinterest monitor is improved but still blocked: advertiser `549756244483`; `0` campaigns/spend; Event Quality `Fair`; EN Shopify source `5,663/5,663`, `0` failed, `152` warnings; failed sitemap source still failed; full item proof is `337/346` EN-US in-stock, with 9 Mommy & Me variants unresolved by historical pin metadata.
- Google Ads paused international Search import remains parked and not approved. Local packet still validates as paused-only with max CPC `$0.15`, but no live Ads action is allowed without exact owner approval.

Guardrails:

- No live spend, no campaign import/create/enable/pause, no budget/bid/status/conversion-goal changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no Merchant uploads, no Google & YouTube product toggle, no Shopify product data, no Shopify Markets/shipping-rate changes, no Pinterest drafts/spend, no payment, and no order without fresh explicit approval.

Next safest subagent workstreams:

1. Parent / localization-presentment: after storefront cooldown, rerun PT only in a fresh browser context. Set Portugal / pt-BR through storefront localization, add one item, go to checkout, select Portugal / Lisboa, verify shipping rates/currency, stop before payment.
2. Market URL investigation: read-only/local/browser investigation of how to force or preserve correct market presentment for paid URLs so fresh ad traffic does not start in US/USD. Do not change Markets or theme without approval.
3. Merchant monitor: continue read-only product-issues/source timestamp monitoring later; do not repeat source refresh/toggle/product/feed edits without exact owner approval.
4. Pinterest monitor: keep drafts/spend parked; if preparing future paused US-only draft, use only the 337 refreshed EN-US in-stock rows or first re-resolve/exclude the 9 missing variants, then ask for exact approval.
5. Ads gate: keep paused international Search import parked until exact owner approval and just-in-time readbacks.

Do not let PT/429, Merchant, Pinterest, or Ads approval blockers freeze other safe local/read-only work.
