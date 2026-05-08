# Paid Growth Orchestrated Safe Advance Report

Date: 2026-05-08
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-orchestrated-safe-advance`

## Scope

Parent/orchestrator sprint with six disjoint read-only/local subagent lanes:

- Merchant exact age_group verification path.
- Google Ads international Search packet validation.
- Pinterest Event Quality / catalog draft gate.
- Localization URL readiness.
- ROAS economics guardrails.
- Creative/RSA claim safety.

## Actions Taken

No live spend, campaign enablement, budget/bid/status change, PMax enable, Standard Shopping change, product-scope/feed-label/product-group change, conversion-goal change, Merchant upload/source sync, Shopify live product-data change, Pinterest account write, checkout payment/order, theme publish, or credential change was made.

Local evidence/control updates:

- Added this evidence packet and lane reports.
- Updated `ops/PROBLEM_TRACKER.md` attempt rows for Merchant exact export verification and Pinterest Event Quality draft gate.
- Corrected the local Google Ads international approval gate so it is non-US only, does not duplicate US nonbrand campaign `23827590655`, and does not bundle Pinterest.
- Added a supersession notice to the older Pinterest `337`/`9` local solution; future work should use the `342`/`4` scope.
- Updated ROAS packet language and CSV caps to match the current Ads packet and Pinterest `342`/`4` scope.

## Readbacks And Validation

Merchant:

- No exact current post-May-8 product-issues CSV exists locally.
- Stale May 7 exact exports remain `623` paid-cohort US/en `Missing age group` IDs.
- May 8 evidence is positive but not exact: sample timestamp advanced, source `10651516446` matched `771` of `780`, and visible diagnostics no longer showed `Missing age group`.
- Current status remains `ACTIVE_VERIFYING`.

Google Ads international Search:

- `17` non-US campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` RSAs, `1,666` web-bulk rows.
- All importable rows are add-only and paused where status applies.
- Max CPC is `0.15`, below the `$0.20` guardrail.
- `0` missing country params, `0` bare ES/IT/RO/PT language-only URL risks, `0` forbidden PMax/Standard Shopping/product-scope/product-group/feed-label/conversion-goal rows.

Pinterest:

- Older `337`/`9` scope is superseded.
- Current clean scope is `342` EN-US in-stock rows: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
- Exclude exactly `4` unresolved variants.
- Event Quality remains `Fair`; paused draft creation can be owner-approved with risk documented, but live spend remains separately gated.

Localization:

- Country-qualified product URLs work for current paid tiers.
- Bare language URLs are still unsafe because they can keep US/USD context.
- GB/CA/AU and broader non-cleared markets still need no-payment checkout QA before live spend.

ROAS:

- At `$70` AOV and `650%` ROAS, max CPA is `$10.77`.
- Required CVR: `$0.10` CPC -> `0.93%`; `$0.12` -> `1.11%`; `$0.15` -> `1.39%`; `$0.20` -> `1.86%`.
- First live learning wave should be smaller than the full `$20/day` non-US shell set; exact approval still required.
- Romania reports/presents in `RON`; use native or FX-normalized value for ROAS.

Creative:

- Customer-facing unsafe copy rows found: `0`.
- Current copy avoids unsupported fast/free shipping, reviews/star ratings, bestseller/promo/discount claims, warehouse/store-pickup/local-stock/stocked-inventory/on-hand-stock claims.

## Current Approval Gates

Paused non-US Google Search build:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

Paused Pinterest US catalog/retargeting draft:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

## Next Best Action

1. Run fresh read-only Merchant browser product-issues export and reconcile against the `780` paid-cohort IDs. If export fails, inspect source `10651516446` processing report for the `9` unmatched rows.
2. After exact owner approval, either create paused non-US Google Search campaigns using the corrected non-US-only gate or create paused Pinterest US drafts using the `342`/`4` scope. Do not enable or spend.
3. Run no-payment checkout QA for GB/CA/AU first, then CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR before any live spend in those markets.

