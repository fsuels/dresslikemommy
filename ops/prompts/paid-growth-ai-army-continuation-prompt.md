# Dress Like Mommy Paid Growth Continuation Prompt

## Owner-Standard Prompt

This is the single reusable prompt the owner wants to paste into any new session. Keep it stable, and keep this file's operating context current behind it.

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it, not just summarize it.

Act as the parent/orchestrator. Use parallel subagents wherever supported, with disjoint workstreams and separate browser/account tabs when needed.

Follow the problem-solving protocol and update `ops/PROBLEM_TRACKER.md` for every active problem, failed readback, blocker, attempt, result, approval gate, and solved status. Do not document known problems passively. Work the solution until fixed, disproven, superseded by a safer path, or gated with the exact next unblock action.

Guardrails: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, and no Shopify live product-data changes unless I give fresh explicit action-time approval.

Start now. Inspect, plan, split the work, execute safe read-only/local/paused-build work, verify, update evidence packets, update `ops/PROBLEM_TRACKER.md`, update `ops/AGENT_WORKLOG.md` with a new `AGENT_CONTINUITY_ANCHOR`, and finish with the next continuation prompt.
```

Single-prompt rule:

- Do not create competing bespoke prompts as the primary handoff.
- If an evidence packet needs `NEXT_CONTINUATION_PROMPT.md`, it should point back to this canonical prompt and name only the latest anchor, blockers, and next gates. It must not become a different operating prompt.
- Final responses should finish with the same owner-standard prompt above, plus the newest `AGENT_CONTINUITY_ANCHOR` and next best action. Do not give the owner three different prompts to choose from.
- When the owner pastes the stable prompt in a new session, the agent must read this file plus `AGENTS.md`, `ops/AGENT_WORKLOG.md`, `ops/PROBLEM_TRACKER.md`, and `ops/AGENT_COORDINATION.md` to reconstruct the true latest state.

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
8. Read the latest entries at the bottom of `ops/AGENT_WORKLOG.md`. As of this prompt refresh, the latest paid-growth anchor is:
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-10-google-ads-non-us-search-paused-build-it-still-in-progress-remaining-absent`
   If the worklog or `AGENTS.md` contains a newer paid-growth anchor, the newer durable state supersedes this line.
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

Every session must move the business closer to this state and end with the single owner-standard continuation prompt plus the latest anchor, blockers, gates, and next closest path to the North Star.

## Memory Rule

Do not rely on chat context alone. Durable memory lives in repo files.

At the end of the session:

- Always update `ops/AGENT_WORKLOG.md` with an `AGENT_CONTINUITY_ANCHOR`.
- Always update `ops/PROBLEM_TRACKER.md` for any problem touched: attempts, failed paths, current status, evidence, next action, and fixed criteria.
- Update `ops/AGENT_COORDINATION.md` if any shared/external surface was claimed, rechecked, blocked, or completed.
- Update `AGENTS.md` only when durable bootstrap memory changed.
- Add evidence under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`.
- The final continuation prompt must follow the single-prompt rule above: use the owner-standard prompt, then name the newest anchor, what is already done and should not be repeated, the next exact gate, and the next best action. Do not emit a second bespoke operating prompt that competes with this file.

## Current state to preserve

- Shopify ProductVariant `mm-google-shopping.age_group` is fixed for all `780` current paid-cohort variants.
- Merchant age_group materially improved on 2026-05-08. The old paid-cohort `US` / `en` / `United States` `Missing age group` count is now `0`, down from prior exact `623`; `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT` is solved. Do not redo US/en age_group fixes.
- Remaining Merchant age_group follow-up is `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`: source `10627981690` / `Shopify App API` has affected `US` / `es` products without effective `n:age_group`. Status is `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`; any repair must be narrow, exact-owner-approved, and read back before/after. Do not broad-refresh, upload, source-edit, Shopify-edit, or change product scope/feed labels/product groups by inference.
- Merchant `Missing local inventory data` was fixed the correct dropshipping way: removed active physical-store `Local inventory ads`; physical-store `Free local listings` was already inactive; diagnostics showed `Great, all your prioritized fixes are resolved`. Do not create local inventory feeds, store pickup, warehouse/local-stock, or on-hand inventory claims.
- Standard Shopping is live/eligible with tight paid cohort and lowered included child product-group CPC bids of `$0.04`; do not change its status, budget, product groups, feed labels, product scope, or conversion goals without fresh explicit owner approval. Fresh metrics readback is now tracked as `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK` / `SOLVED_READBACK_PASSED_CUSTOM_RANGE_NO_ADS_WRITES`: a 2026-05-09 read-only Google Ads browser/CDP capture showed campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` Enabled / Eligible, Shopping, budget `US$20.00/day`, all-time range `2017-05-04` to `2026-05-09`, `82` clicks, `3,962` impressions, `US$18.60` cost, avg CPC `US$0.23`, `0.00` conversions, and `0.00` conversion value; a later custom range readback for `2026-05-06` through `2026-05-09` in Google Ads Pacific time showed `1` click, `58` impressions, `US$0.02` cost, avg CPC `US$0.02`, `0.00` conversions/value, only `us_test_ready / mommy_me` with click/cost, and `Everything else in All products` still excluded. No Ads writes were made.
- Paused US nonbrand Search rebuild exists: campaign `23827590655`, `$2/day`, Manual CPC, `$0.15` CPC, 12 ad groups, 36 exact/phrase keywords, 37 negatives, 12 paused RSAs.
- Remarketing remains paused because policy status was not clean.
- Pinterest official app pixel is set to Always on / share all events. The stale `337/346` catalog proof blocker is superseded by a clean `342`-row US scope with 4 excluded variants. Pinterest Event Quality may still read `Fair`; track this as `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`.
- The owner gave the exact paused non-US Google Search `TEST BUILD` approval on 2026-05-10. Parent/orchestrator performed a partial approved build. Paused Search campaigns now exist and final-readback passed for `GB` (`23838895360`, `$2/day`), `CA` (`23834423669`, `$2/day`), `AU` (`23834424182`, `$2/day`), `CH` (`23834425358`, `$1/day`), `DK` (`23838969244`, `$1/day`), `DE` (`23834427575`, `$1/day`), `NL` (`23829110118`, `$1/day`), `SE` (`23838970036`, `$1/day`), and `ES` (`23829133584`, `$1/day`). All 9 are paused, Search, presence-only, content/YouTube off, and had `88/88 # OK` preview/apply validation where applied; `GB` required a narrow approved presence-only repair after readback found positive geo targeting at `DONT_CARE`, and post-repair readback passed. No live spend or enablement was started. No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product-scope, feed-label, product-group, conversion-goal, existing budget/bid/status-enable, or product/feed/conversion write was made. `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR` remain absent/uncreated. `FR` is parked because a stale/in-progress preview/apply recovery produced `completed with errors` / `no changes` and no FR campaign; `BE` is parked because Google Ads returned an upload-throttle message (`too many simultaneous uploads` / too many recent spreadsheets); `IT` is parked because a fresh resume preview stayed in progress at `0` changes / `0` success / `0` errors after bounded waits, and a later 2026-05-10 02:05 EDT browser/CDP recheck still showed the IT preview in progress at `0/0/0`. No IT apply was clicked and no IT campaign exists. `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE` is now `PARTIAL_9_APPLIED_REMAINING_BLOCKED_BY_FR_STALE_PREVIEW_BE_THROTTLE_IT_STILL_IN_PROGRESS_PREVIEW`. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/GOOGLE_ADS_NON_US_SEARCH_PAUSED_TEST_BUILD_APPROVED_PARTIAL_REPORT.md` and `working/final_campaign_readback_summary_2026-05-10_it_still_in_progress.json`.
- `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` is now `PARTIALLY_MITIGATED_LOCAL_OPTIONS_READY__OWNER_DECISION_REQUIRED`: local native-language copy options exist for `14` locale variants (`es-ES`, `it-IT`, `pt-PT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `fr-BE`, `nl-BE`, `sv-SE`, `da-DK`, `pl-PL`, `cs-CZ`, `el-GR`) with `0` forbidden-claim hits, max headline length `24`, and max description length `73`; every locale remains concept-ready only and requires native-speaker review plus landing-language QA before platform use. The market activation scorecard still has live-spend-ready non-US markets at `0`; top staged sequence is `GB`, `CA`, `AU`, then `ES`, `IT`, `RO`, `PT`, and the smallest future spend unit after separate approval is `GB / Mommy & Me Dresses - Exact only`. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/PAID_GROWTH_LOCALIZED_COPY_PINTEREST_MANIFEST_SAFE_ADVANCE_REPORT.md`.
- Pinterest review-only paused-draft templates now exist for the clean `342` EN-US scope with `4` exclusions; the templates are not Pinterest upload files and are marked review-only. Event Quality remains `Fair`; any Pinterest draft, campaign, product-group, audience, budget, bid, tag/CAPI, status, or spend write still requires exact owner approval and readbacks. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`.
- AU checkout `429` is solved: isolated-browser QA reached AU/AUD shipping rates with no verification page, no payment, and no order. GB and CA visual checkout UI is solved for paused infrastructure. CH, DK, DE, FR, BE, SE, PL, CZ, and GR no-payment checkout-to-shipping QA passed on 2026-05-09. NL is now also solved for paused-infrastructure checkout evidence: after the prior cart/rates `429` cleared, one adjusted isolated no-payment/no-bypass pass confirmed Netherlands selected in checkout UI, checkout `en-NL`, cart currency `EUR`, Standard `FREE`, Express `EUR 11.95`, no `429`/CAPTCHA/verification, no payment data, no Pay Now/Place Order click, and no order. All `17` international target markets passed low-volume product landing GET checks, and all `17` proposed non-US Search countries now have at least paused-infrastructure checkout/rate evidence, but live-spend-ready markets remain `0` until approval, tracking/catalog/feed/URL/economics gates clear. `PROB-2026-05-09-DE-NL-CHECKOUT-QA`, `PROB-2026-05-09-FR-BE-CHECKOUT-QA`, and `PROB-2026-05-09-SE-PL-CZ-GR-CHECKOUT-QA` are solved as readbacks for paused infrastructure only.
- Paid-landing blocker `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`: product `7227378892897` / handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` has stale Christmas title/OG/Twitter metadata on a beach/vacation paid-candidate URL, including sampled ES/IT/RO/PT localized metadata. Local Ads import risk is partially mitigated by the held `1496`-row CSV, but do not send live paid traffic to this URL until exact-owner-approved Shopify SEO/social-title repair passes public readback, or use the held/excluded URL packet for any future approved paused Ads import.
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

For paused non-US Google Search infrastructure only:

`APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.`

For paused Pinterest US drafts only:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

For Merchant US/es age_group repair review:

`APPROVE MERCHANT US/ES AGE_GROUP REPAIR REVIEW FOR SOURCE 10627981690: READ BACK THE US/ES PRODUCT DETAIL AND SOURCE STATE FIRST; THEN USE ONLY THE NARROWEST SAFE OFFICIAL REPAIR PATH FOR US FEED LABEL / ES LANGUAGE / UNITED STATES MISSING AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO BROAD SOURCE REFRESH, MERCHANT UPLOAD, SOURCE EDIT, OR SHOPIFY DATA EDIT WITHOUT A PREVIEW, EXACT ROW SCOPE, AND POST-READBACK.`

## Reporting requirement

At the end, report:

- What changed.
- Files touched.
- Commands/tools run.
- Readback results.
- Problem tracker updates.
- Residual risks.
- Next best action.
- The single owner-standard continuation prompt from the top of this file, plus the latest continuity anchor, unresolved blockers, exact approval gate if needed, and the next subagent workstreams. Do not create multiple alternative prompts.

Keep evidence in a dated packet under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/` and add an `AGENT_CONTINUITY_ANCHOR` to `ops/AGENT_WORKLOG.md`.
