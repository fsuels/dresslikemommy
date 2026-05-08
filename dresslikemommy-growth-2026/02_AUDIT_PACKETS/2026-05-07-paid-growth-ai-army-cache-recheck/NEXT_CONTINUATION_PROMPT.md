Continue paid-growth from `AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-ai-army-cache-recheck-public-copy-cleared`.

Read first:

1. `AGENTS.md`
2. `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
3. `ops/GROWTH_NORTH_STAR.md`
4. `ops/MEMORY_CONTINUITY_PROTOCOL.md`
5. `ops/AGENT_COORDINATION.md`
6. `ops/BROWSER_SUBAGENT_COORDINATION.md`
7. `ops/GOOGLE_ADS_CONTINUITY.md`
8. `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/PAID_GROWTH_AI_ARMY_CACHE_RECHECK_REPORT.md`
9. Latest `ops/AGENT_WORKLOG.md` entries

Critical corrections:

- Dress Like Mommy is dropshipping, has no physical store, and has no owned physical inventory.
- Do not imply warehouses, retail inventory, local inventory, stocked inventory, guaranteed on-hand stock, or in-store pickup.
- Merchant `Missing local inventory data` is not a product-data mistake for this business. Do not create local inventory feeds or local-stock/store-pickup claims to clear it; at most, read-only verify whether a Local Inventory Ads / physical-store setting is enabled by mistake.
- Return shipping is customer-paid; do not confuse outbound checkout delivery rates with return postage.
- Do not import, create, enable, or spend internationally yet.

What is now done:

- The four previously stale localized public URLs were rechecked slowly and are now clean:
  - `/es/pages/shipping-info`
  - `/it/policies/shipping-policy`
  - `/it/pages/shipping-info`
  - `/pt/pages/shipping-info`
- All four returned HTTP `200`, had no stale blocker phrases, had checkout-availability wording, were localized, and showed no visible 429/CAPTCHA blocker.
- Existing Google Ads international Search packet was revalidated as local-only paused infrastructure: `17` non-US paused draft campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, max CPC `$0.15`, no broad keywords, and no PMax/Standard Shopping/product-scope/feed-label/product-group/conversion-goal edit rows.
- ROAS guardrails and claim-safe copy packets were refreshed locally.
- Measurement report reconfirmed: use primary purchase value only; do not use historical `All conv. value / cost` for ROAS where pre-cleanup micro values are included.

What remains blocked:

- Merchant source/age_group has not cleared. Shopify paid-cohort age_group is still `780 already_correct`, but Merchant US/en sample source `10627623003` still shows timestamp `2026-05-07T14:14:02+00:00`; diagnostics refreshed at `10:53 PM May 7, 2026` and still included `Missing age group`; API export remains `403 PERMISSION_DENIED`.
- Pinterest drafts/spend are blocked until fresh account/Event Quality/catalog/item readbacks pass. Latest synthesis is local-only, not a fresh live account readback.
- International spend is still blocked by route/currency, no-payment checkout QA, catalog/feed, tracking, economics, and owner approval gates.
- Google Ads paused international import/create is still blocked without the exact owner approval phrase and just-in-time readbacks.

Next safe parallel lanes:

1. Localization/checkout QA subagent: slowly check ES/IT/RO/PT product route, policy route, currency behavior, and no-payment checkout rates using required region fields:
   - ES `Comunidad de Madrid`
   - IT `Roma`
   - RO `Bucuresti`
   - PT `Lisboa`
   Submit no payment and create no order.
2. Merchant subagent: run read-only sample timestamp/product-issues recheck; use scoped credentials or browser export if available; do not repeat Google & YouTube toggle and do not edit product/feed data.
3. Pinterest subagent: run fresh read-only `DLM-PINTEREST-EventCatalog` account readback for Event Quality, Events Overview, EN catalog source, failed sitemap source relevance, localized feed warnings, and current US item-level candidate proof.
4. Ads subagent: keep local paused international Search packet parked; if exact approval is given, run pre-import Google Ads readbacks and preview-first bulk upload only.
5. Parent/orchestrator: own approvals, live writes, coordination, final integration, worklog, and any AGENTS memory update.

Exact owner approval still needed for paused Google international Search import/create:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

Exact owner approval still needed for Merchant source refresh/resync:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH REVIEW: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; ATTEMPT ONLY A SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`

Do not enable PMax or Remarketing. Do not change Standard Shopping status, budget, product groups, feed labels, product scope, bids, or conversion goals without fresh exact approval. Do not create Pinterest drafts/spend without fresh exact approval after gates pass.
