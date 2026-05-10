# Next Continuation Prompt

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it.

Latest continuity anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-safe-followup-us-es-checkout`

What is already done and should not be repeated blindly:

- US/en Merchant age_group blocker is solved. Exact export showed paid-cohort `US` / `en` / `United States` `Missing age group` count `0`, down from prior `623`.
- Do not redo Shopify age_group edits, blind Merchant source refreshes, source uploads, product-scope/feed-label/product-group changes, or Standard Shopping changes.
- Merchant US/es local diagnosis is complete enough for the next read-only gate: remaining issue is `625` paid item IDs / `1,250` rows only in `US` feed label, `es` language, `United States`, split across Shopping ads and Free listings. Likely source path is `Shopify App API` source `10627981690`. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/merchant-us-es/`.
- Google Ads non-US Search local packet passed validation again. It has `17` non-US campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` paused RSAs, `1666` import rows, all `Add` and paused, max CPC `$0.15`, no US campaign `23827590655`, and no forbidden PMax/Standard Shopping/product-scope/feed-label/product-group/conversion-goal rows. It was not imported.
- Pinterest paused-draft gate is refreshed: use the clean `342` EN-US in-stock scope and exclude the `4` unresolved variants. Event Quality remains `Fair`; this blocks live spend, not exact-owner-approved paused draft creation. No Pinterest writes were made.
- GB and CA public product/cart/shipping-rate evidence passed: GB carried GBP with Standard `0.00 GBP` and Express `9.71 GBP`; CA carried CAD with Standard `0.00 CAD` and Express `18.00 CAD`. They still need visual browser checkout UI confirmation before spend.
- AU is not cleared. Product landing initially showed AUD, but cart/rates and cooldown retry hit HTTP `429` / `Verifying your connection...`. This is tracked as `PROB-2026-05-08-AU-CHECKOUT-429`.
- Economics/creative pack is ready: with `$70` AOV and `650%` ROAS, max CPA is about `$10.77`; `$0.15` CPC requires about `1.39%` CVR. Use claim-safe copy only; no fast shipping, warehouse/local inventory, review, bestseller, promo, or guaranteed-availability claims without proof.

Guardrails still active:

- No live spend.
- No campaign enablement.
- No budget, bid, campaign status, product-scope, feed-label, product-group, or conversion-goal changes.
- No PMax enable.
- No Standard Shopping changes.
- No Merchant uploads, source syncs, or source edits.
- No Shopify live product-data changes.
- No Pinterest campaign, draft, product group, tag, CAPI, audience, budget, bid, catalog, or spend writes.
- No checkout payment or order.

Problem tracker priorities:

1. `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`: next read-only gate is to inspect at least one affected Merchant product detail with `language=es` / `feedLabel=US`, and inspect source/settings for likely source `10627981690`. If a live fix is needed, ask for fresh exact approval first.
2. `PROB-2026-05-08-AU-CHECKOUT-429`: after cooldown, run AU one-country isolated browser checkout walkthrough to visible shipping rates, no payment/order. Recheck GB/CA visually when practical.
3. `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`: remains owner-approval gated for either paused US drafts using the `342` scope / `4` exclusions, or a narrow event-quality repair. Live spend remains separately gated.

Exact approval gates available:

Paused non-US Google Search build:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

Paused US Pinterest draft:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Narrow Pinterest Event Quality repair:

`APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.`

Recommended next subagents:

- `DLM-MERCHANT-US-ES-SourceDetail`: read-only Merchant product/source detail for source `10627981690`; own only Merchant readback evidence, no writes.
- `DLM-QA-AU-Checkout`: isolated-browser AU checkout-to-shipping QA; no payment/order; then GB/CA visual UI confirmation if cooldown allows.
- `DLM-GOOGLEADS-IntlSearch`: only after exact owner approval, run import preview/build for paused non-US Search; parent owns final approval and readback.
- `DLM-PINTEREST-EventCatalog`: only after exact owner approval, create paused US draft objects or run narrow Event Quality repair; parent owns final approval and readback.

Closest path to the North Star:

Clear the Merchant US/es read-only source detail and AU checkout blocker while requesting separate approvals for paused-only Google Search and Pinterest draft infrastructure. Keep live spend blocked until measurement, catalog, checkout, economics, and exact approval gates all pass.

