Continue in `/Users/fsuels/Projects/dresslikemommy`.

Read `ops/prompts/paid-growth-ai-army-continuation-prompt.md` first and follow it as the canonical operating prompt. Also read `AGENTS.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/PROBLEM_SOLVING_PROTOCOL.md`, `ops/PROBLEM_TRACKER.md`, and the latest `ops/AGENT_WORKLOG.md` entries.

Latest anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-merchant-age-group-exact-export-us-en-cleared`.

Current state:

- The Merchant exact product-issues export was run first and succeeded. Evidence packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/`.
- Exact export file: `raw/product-issues-browser-export/product_issues_2026-05-08_01-58-05.csv`.
- Original paid-cohort `US` / `en` / `United States` `Missing age group` blocker is solved: `0` current unique item IDs, down from prior `623`.
- `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT` is closed as `SOLVED_READBACK_PASSED_US_EN`.
- New follow-up `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` is active: `625` paid item IDs / `1,250` rows remain only in `US` feed label, `es` language, `United States`, split across Shopping ads and Free listings. Diagnose this read-only before any Spanish-language US paid testing or Merchant fix.
- Do not repeat Shopify age_group edits, local-inventory fixes, old Pinterest 337/9 work, old Ads approval wording, source refresh loops, or Merchant uploads.
- Standard Shopping remains live/eligible and must not be touched without fresh explicit owner approval.
- No Google Ads or Pinterest writes were made in the exact-export session because the current turn did not include either exact approval gate.

Guardrails:

- No live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads/source syncs/source edits, no Shopify live product-data changes, no Pinterest campaign/draft/product-group/tag/CAPI/audience/budget/bid writes, no theme publish, no checkout payment, and no order creation unless fresh exact action-time owner approval is present.

If the owner provides this exact approval, build only paused non-US Google Search shells:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

If the owner provides this exact approval, build only paused Pinterest US drafts:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

If neither approval is present, continue safe lanes:

1. Read-only diagnose `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`: identify the US/es Merchant source/feed path and prepare a targeted approval gate if a fix is needed.
2. Run GB/CA/AU no-payment checkout QA to shipping step only.
3. Refresh ROAS/economics, creative/RSA, and reporting packets locally/read-only.

End the session by updating `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, `ops/AGENT_WORKLOG.md` with a new `AGENT_CONTINUITY_ANCHOR`, and a new continuation prompt.
