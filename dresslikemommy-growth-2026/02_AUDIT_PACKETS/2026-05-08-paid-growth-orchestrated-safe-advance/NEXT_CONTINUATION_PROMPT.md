# Next Continuation Prompt

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Latest continuity anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-orchestrated-safe-advance`

Read first and follow, not summarize:

1. `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
2. `AGENTS.md`
3. `ops/MEMORY_CONTINUITY_PROTOCOL.md`
4. `ops/PROBLEM_SOLVING_PROTOCOL.md`
5. `ops/PROBLEM_TRACKER.md`
6. `ops/AGENT_COORDINATION.md`
7. `ops/BROWSER_SUBAGENT_COORDINATION.md`
8. `ops/GROWTH_NORTH_STAR.md`
9. `ops/GOOGLE_ADS_CONTINUITY.md`
10. Latest `ops/AGENT_WORKLOG.md` entries

Do not repeat:

- Shopify `mm-google-shopping.age_group` edits; Shopify side already read `780 already_correct`.
- Merchant local-inventory fixes; physical-store `Local inventory ads` was removed and diagnostics cleared. DLM has no physical store and no owned inventory.
- Old Pinterest `337`/`9` draft scope. It is superseded by the clean `342` EN-US rows and `4` exclusions.
- Old Ads international approval wording that included `US` and Pinterest. Use the corrected non-US-only Google Ads gate below.

Active problems:

- `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT`: `ACTIVE_VERIFYING`. Next safe action is a fresh read-only Merchant browser product-issues export in a dedicated tab and reconciliation against the `780` paid-cohort IDs. If export fails, inspect/download source `10651516446` processing report for the `9` unmatched rows. API fallback needs proper read-only Merchant diagnostics scopes outside the repo.
- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`: `OWNER_APPROVAL_REQUIRED`. Event Quality remains `Fair`; Tag/CAPI are alive. Paused draft can proceed only after exact owner approval using the `342`/`4` scope. Live spend remains separately gated.

Correct approval gates:

Paused non-US Google Search:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

Paused Pinterest US draft:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Recommended subagents:

- Parent owns approvals, coordination, tracker/worklog, live writes, and final integration.
- `DLM-MERCHANT-US-ExactExport`: read-only browser product-issues export/source processing report.
- `DLM-GOOGLEADS-IntlSearch`: only after approval, preview/import paused non-US Search shells; do not duplicate US.
- `DLM-PINTEREST-EventCatalog`: only after approval, create paused US draft with `342`/`4` scope; no spend.
- `DLM-QA-LandingLocalization`: no-payment checkout QA for GB/CA/AU, then CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR.
- `DLM-ROAS-Economics`: keep country CPC/budget guardrails aligned to Ads packet and actual AOV/margin.
- `DLM-Creative-RSA`: keep copy claim-safe and local-only until approved.

Guardrails remain: no live spend, enablement, budget/bid/status changes, PMax enable, Standard Shopping changes, product-scope/feed-label/product-group changes, conversion-goal changes, Merchant uploads/source syncs, Shopify live product-data changes, Pinterest draft/campaign/tag/CAPI/product-group/audience/budget/bid writes, checkout payment/order, theme publish, or credential changes unless the owner gives fresh exact action-time approval.

