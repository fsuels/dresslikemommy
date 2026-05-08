# Dress Like Mommy Paid Growth Continuation Prompt

You are continuing the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

The owner wants aggressive but smart revenue growth and profit growth, aiming toward roughly `650% ROAS`, with fast execution and subagent orchestration wherever it can move faster. Do not get stuck in audit-only mode. Build and repair what can safely be built, but preserve explicit approval boundaries around live spend, campaign enabling, budgets, product scope, feed labels, conversion goals, and product data.

Important business-model correction: Dress Like Mommy is a dropshipping business. It does not have a physical store and does not hold owned physical inventory. Do not write policy, ad, listing, feed, or report copy that implies a retail location, warehouse, local inventory, stocked inventory, or guaranteed on-hand stock. Platform terms such as Merchant/Pinterest `in_stock`, Shopify `inventory`, or `Missing local inventory data` are channel/feed salability diagnostics, not permission to fabricate physical inventory claims.

Important standing owner authorization: for paid-growth continuation work, the owner does not want a single-agent-only execution model when an orchestrator plus subagents can move faster. Treat this prompt as explicit authorization to spawn parallel subagents where the platform supports it, after reading coordination files and assigning disjoint workstreams/tabs. If subagent tooling is unavailable, say so clearly in the first status update and still execute the same workstreams by the fastest safe sequential/local path.

Important non-blocking execution rule: do not let one stuck workstream freeze the whole growth sprint. If one lane is blocked by Merchant processing, app/source refresh, browser access, policy review, missing approval, login/CAPTCHA, or any other external wait, open or update the problem in `ops/PROBLEM_TRACKER.md`, record the attempts/results/evidence/next action, and continue other independent lanes that move toward the North Star. For example, if Merchant age_group/source refresh is blocked, keep moving on paused Google Search country infrastructure, Pinterest read-only gates or paused drafts, localization/shipping QA, CRO/theme-local fixes, ROAS/economics rules, creative/RSA copy packs, and reporting/readback packets where safe.

Important solve-to-completion rule: a problem is not a note. It is a live work item until it is fixed, disproven, superseded by a safer solution, or gated by exact owner approval/credentials with the next concrete unblock action named. Do not document a known problem and then evade it. Work the solution, learn from failed attempts, update the tracker, and close only with evidence.

## First actions

1. Read `AGENTS.md`.
2. Read `ops/MEMORY_CONTINUITY_PROTOCOL.md` so completed fixes are not forgotten or repeated.
3. Read `ops/PROBLEM_SOLVING_PROTOCOL.md`.
4. Read `ops/PROBLEM_TRACKER.md`.
5. Read `ops/AGENT_COORDINATION.md`.
6. Read `ops/BROWSER_SUBAGENT_COORDINATION.md` before orchestrating subagents or using logged-in ChatGPT Atlas / in-app browser tabs.
7. Read `ops/GROWTH_NORTH_STAR.md` so all work is tied to the owner’s definition of "promise land."
8. Read the latest entries in `ops/AGENT_WORKLOG.md`, especially:
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-08-problem-tracker-solve-to-completion-protocol`
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-08-merchant-local-inventory-addons-removal`
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-08-pinterest-catalog-event-unblock`
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-08-merchant-source-refresh-approved-action`
9. Read `ops/GOOGLE_ADS_CONTINUITY.md` before any Google Ads, Merchant Center, GA4, Shopify tracking, or paid-campaign work.
10. Search the problem tracker, worklog, and coordination files for the relevant campaign ID, Merchant source/feed ID, product/cohort ID, theme ID, pixel/tag name, file path, or exact issue text before fixing anything.
11. If a fix was already completed, verify it with a targeted readback instead of redoing it.
12. Honor active locks/claims. Do not clear another agent's claim unless the owner explicitly transfers or clears it.

## North Star

The promise-land goal is not merely launching campaigns. It is building a controlled paid-growth machine that increases profit.

Success means:

- Purchase tracking and ROAS reporting are trusted.
- Paid products/feed/catalog are healthy enough for Google and Pinterest optimization.
- Landing pages and international pages used for ads are clean enough to convert.
- Google Ads and Pinterest have segmented, controlled campaign structures.
- International markets are tested intelligently, not ignored and not launched blindly.
- CPC/CPA/budget guardrails are explicit and tied to AOV, margin, conversion rate, and return risk.
- Winners can be scaled and losers can be killed quickly.
- The owner can see which campaigns, products, and countries are making money.

Every session must move the business closer to this state and end with a continuation prompt that names the next closest path to the North Star.

## Memory Rule

Do not rely on chat context alone. Durable memory lives in repo files.

At the end of the session:

- Always update `ops/AGENT_WORKLOG.md` with an `AGENT_CONTINUITY_ANCHOR`.
- Always update `ops/PROBLEM_TRACKER.md` for any problem touched: attempts, failed paths, current status, evidence, next action, and fixed criteria.
- Update `ops/AGENT_COORDINATION.md` if any shared/external surface was claimed, rechecked, blocked, or completed.
- Update `AGENTS.md` only when durable bootstrap memory changed.
- Add evidence under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`.
- The final continuation prompt must say what is already done and should not be repeated.

## Current state to preserve

- Shopify ProductVariant `mm-google-shopping.age_group` is fixed for all `780` current paid-cohort variants.
- Merchant age_group materially improved on 2026-05-08: sample US/en source timestamp advanced to `2026-05-08T05:55:06+00:00`, sample no longer showed `Missing age group`, and the dedicated age_group-only source `10651516446` showed `780` updated products / `771` matched / `9` unmatched. Exact paid-cohort CSV still needs later read-only confirmation. Track this as `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT`; if rows remain, investigate the `9` unmatched rows first.
- Merchant `Missing local inventory data` was fixed the correct dropshipping way: removed active physical-store `Local inventory ads`; physical-store `Free local listings` was already inactive; diagnostics showed `Great, all your prioritized fixes are resolved`. Do not create local inventory feeds, store pickup, warehouse/local-stock, or on-hand inventory claims.
- Standard Shopping is live/eligible with tight paid cohort and lowered included child product-group CPC bids of `$0.04`; do not change its status, budget, product groups, feed labels, product scope, or conversion goals without fresh explicit owner approval.
- Paused US nonbrand Search rebuild exists: campaign `23827590655`, `$2/day`, Manual CPC, `$0.15` CPC, 12 ad groups, 36 exact/phrase keywords, 37 negatives, 12 paused RSAs.
- Remarketing remains paused because policy status was not clean.
- Pinterest official app pixel is set to Always on / share all events. The stale `337/346` catalog proof blocker is superseded by a clean `342`-row US scope with 4 excluded variants. Pinterest Event Quality may still read `Fair`; track this as `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`.
- Local-only international Search packet has a refreshed country-qualified URL copy and remains not imported; all importable entities are paused and CPC remains capped at `$0.15` in the local packet.
- No PMax enable. No international live spend. No Pinterest live spend unless the owner gives explicit action-time approval.

## Strategic posture

The owner has many languages and wants international ROI. Do not assume only US/UK/CA/AU are useful. Also do not assume every language is ready for live paid spend.

Correct approach:

- Build segmented, paused, tightly controlled country/language growth infrastructure.
- Enable only after readbacks confirm shipping clarity, landing-page language quality, conversion tracking, Merchant/Pinterest catalog health, and CPC/CPA economics.
- Cheap CPC is not enough; ROI depends on qualified traffic, conversion rate, AOV, margin, return risk, and tracking quality.

Initial Google Search market tiers:

- Priority/proven or likely high-value: US, UK, Canada, Australia, Switzerland, Denmark.
- Broader ecommerce/family-fashion tests: Germany, Netherlands, Sweden, France, Belgium, Spain, Italy.
- Lower-CPC discovery tests: Poland, Czechia, Romania, Greece, Portugal.
- Hold or extra QA before spend: Arabic/Hebrew/Japanese/Korean markets and any market with mixed-language pages or unclear shipping/returns/duties.

## Required orchestrator/subagent pattern

Use a parent/orchestrator agent by default. Within the first execution cycle after reading coordination files, identify the critical path and spawn parallel agents with disjoint scopes for sidecar work that can run without blocking the parent.

The parent should:

- Own the control lane, approvals, live writes, final integration, coordination rows, and final report.
- Keep moving on the immediate critical-path task while subagents run in parallel.
- Avoid waiting on subagents unless their output blocks the next parent action.
- Treat `BLOCKED` from one lane as a routing signal, not a stop sign for the whole sprint. Reassign attention to the next independent lane immediately.
- Keep a visible lane/problem board in the evidence packet: `moving`, `active solving`, `active verifying`, `waiting on approval`, `credentials required`, `platform refresh pending`, `done`, and `next safe parallel action`. Link each real problem to its `ops/PROBLEM_TRACKER.md` problem ID.
- Update `ops/PROBLEM_TRACKER.md` as subagents report attempts, failed paths, readbacks, or solved status.
- Integrate subagent findings into one dated evidence packet and one worklog anchor.
- If a subagent-capable tool is not available, state that limitation and continue with the same lanes sequentially rather than silently acting like a one-agent audit.

Use the logged-in ChatGPT Atlas / in-app browser when available, but keep agents separated by tab/session. Parent owns the control tab and final approval. Subagents must not share tabs, navigate away from another agent's page, switch accounts, sign out, solve CAPTCHA, accept permission prompts, or click Save/Apply/Enable/Pause/Upload/Sync unless their scope and approval explicitly allow it.

Suggested browser tab/session names:

- `DLM-PARENT-Control`
- `DLM-MERCHANT-US-SourceRefresh`
- `DLM-SHOPIFY-GoogleYouTube`
- `DLM-GOOGLEADS-IntlSearch`
- `DLM-PINTEREST-EventCatalog`
- `DLM-GA4-GSC-Measurement`
- `DLM-QA-LandingLocalization`

1. Merchant/source-refresh agent:
   - Read-only first.
   - Inspect Google & YouTube / Shopify app sync status, Merchant US Shopify App API source details, sample item API timestamps, and whether a safe official app resync/refresh is available.
   - Do not edit product data or upload feeds without explicit approval.

2. Google Ads international-search build agent:
   - Prepare or create paused campaign shells only after owner approval.
   - Use exact/phrase high-intent keywords, presence-only location targeting, CPC caps at or below `$0.20`, tight negatives, claim-safe RSAs, and no live spend.
   - Keep Standard Shopping, PMax, conversion goals, product scope, feed labels, and product groups untouched unless separately approved.

3. Pinterest growth agent:
   - Run tag/catalog/event-quality gate read-only first.
   - Create paused US catalog/retargeting drafts only if gates pass and owner approves.
   - No live Pinterest spend until explicit approval.

4. Localization/shipping QA agent:
   - Check market landing pages and language quality for the country tiers.
   - Identify pages safe for paid traffic and pages that require theme/translation/shipping copy fixes before spend.

5. ROAS/economics guardrail agent:
   - Build country/campaign CPA/CPC guardrails from target ROAS `650%`, AOV, margin assumption, and conversion-rate scenarios.
   - Produce pause/kill rules and suggested starting budgets.

6. Creative/RSA copy agent:
   - Produce local-language or English claim-safe RSAs and Pinterest copy packs for approved countries.
   - Avoid unsupported claims such as fast shipping, review counts, best seller claims, or promotions unless verified on the live site.

The parent agent must own coordination, approvals, final integration, live writes, and evidence packets. Subagents should not duplicate work or edit overlapping files/surfaces.

## Approval language to request if not already given

For paused international growth infrastructure:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

For Merchant source refresh review:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH REVIEW: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; ATTEMPT ONLY A SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`

## Reporting requirement

At the end, report:

- What changed.
- Files touched.
- Commands/tools run.
- Readback results.
- Problem tracker updates.
- Residual risks.
- Next best action.
- A continuation prompt for the next session, including the latest continuity anchor, unresolved blockers, exact approval gate if needed, and the next subagent workstreams.

Keep evidence in a dated packet under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/` and add an `AGENT_CONTINUITY_ANCHOR` to `ops/AGENT_WORKLOG.md`.
