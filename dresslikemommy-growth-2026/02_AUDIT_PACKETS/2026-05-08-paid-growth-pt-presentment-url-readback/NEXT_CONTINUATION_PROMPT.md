# Next Continuation Prompt - Paid Growth PT Presentment / URL Readback

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as canonical operating prompt. Before spawning subagents or using browser/account tabs, read `AGENTS.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the latest `ops/AGENT_WORKLOG.md` entries.

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-pt-presentment-url-readback`

Evidence packet:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/`

Current state:

- PT-only cooldown checkout QA passed. Portugal / `pt-BR` / EUR carried through product, cart, checkout country/region (`Lisboa`), and shipping rates. Standard shipping was `GRÁTIS`; Express was `€ 11,95`; total was `EUR € 24,95`. No payment was submitted and no order was created.
- Bare language-only product routes are not safe paid final URLs. A fresh `/pt/products/...` URL without `country` redirected to the base product path and presented English / United States / USD.
- Country-qualified localized URLs passed product landing readbacks in fresh contexts:
  - `/pt/products/...?country=PT` -> Portugal / `pt-BR` / EUR.
  - `/es/products/...?country=ES` -> Spain / Spanish / EUR.
  - `/it/products/...?country=IT` -> Italy / Italian / EUR.
  - `/ro/products/...?country=RO` -> Romania / Romanian / RON.
- Use this template for any future paused Ads packet update only after approval:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?country=<ISO_COUNTRY>
```

If a variant is needed:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?variant=<VARIANT_ID>&country=<ISO_COUNTRY>
```

- Merchant is still not cleared. Sample item `shopify_US_7227254276193_41871113158753` still shows source `10627623003` / `Shopify App API` timestamp `2026-05-07T14:14:02+00:00`; visible diagnostics updated at `1:02 AM May 8, 2026` and still show `Missing age group` plus `Missing local inventory data`. Fresh exact CSV count did not download; latest exact count remains prior `623` paid-cohort US/en unique item IDs. API paths remain blocked by `403 PERMISSION_DENIED`.
- `Missing local inventory data` is not a product-data fix target. DLM is dropshipping with no physical store and no owned physical inventory. Do not create local inventory feeds, local stock claims, warehouse claims, store pickup claims, or guaranteed on-hand inventory claims.
- Pinterest remains parked: advertiser `549756244483`, `0` campaigns/spend, Event Quality `Fair` updated `2026-05-06`, fresh Tag/CAPI source timestamps around `2026-05-08T04:58Z`, EN Shopify source `5,663/5,663`, `0` failed, `152` warnings, failed sitemap source still failed, item proof `337/346` EN-US in-stock with the same 9 unresolved variants.
- Google Ads paused international Search import remains parked and not approved. Local packet still validates as paused-only: `17` non-US draft campaigns, `204` ad groups, `612` exact/phrase positive keywords, `629` negatives, `204` RSAs, max CPC `$0.15`, and no PMax/Standard Shopping/product/feed/conversion-goal edit rows.

Guardrails:

- No live spend, no campaign import/create/enable/pause, no budget/bid/status/conversion-goal changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no Merchant uploads, no Google & YouTube product toggle, no Shopify product data, no Shopify Markets/shipping-rate changes, no Pinterest drafts/spend, no payment, and no order without fresh explicit approval.

Next safest subagent workstreams:

1. Merchant monitor: later read-only product-issues export retry and sample timestamp recheck; park if CSV download blocks again. Do not click source refresh/sync or repeat product toggle without exact owner approval.
2. Ads parked URL update gate: local-only update/validate paused international Search final URL templates to include `country=<ISO_COUNTRY>` if the owner asks for import readiness; no live Ads access/import without exact approval.
3. Pinterest monitor: keep drafts/spend parked; future US-only paused draft must use only the 337 resolved EN-US in-stock rows or first re-resolve/exclude the 9 missing rows.
4. Measurement/economics: refresh country-level CPC/CVR/CPA guardrails using observed currencies, especially RO as RON.

Do not let Merchant/Pinterest/Ads approval blockers freeze other safe local/read-only work.
