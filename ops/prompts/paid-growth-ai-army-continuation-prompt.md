# Dress Like Mommy Paid Growth Continuation Prompt

## Owner-Standard Prompt

This is the single reusable prompt the owner wants to paste into any new session. Keep it stable, and keep this file's operating context current behind it.

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it, not just summarize it.

Set goal: build and run a profitable paid-growth machine for Dress Like Mommy, with expert Google Ads and Pinterest campaigns active across every viable language/market, aiming for as many profitable conversions as possible at about 650% ROAS.

Do not stop at audit-only work. Show progress through actual sales-moving changes: approved live tests enabled/monitored, paused-ready campaigns or Pinterest drafts built, keywords/negatives/copy/assets improved, landing/feed/catalog blockers fixed, performance decisions made from evidence, or exact unblock actions prepared.

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

The set goal is to build and run a profitable paid-growth machine for Dress Like Mommy: Google Ads and Pinterest campaigns active across every viable language/market, executed expertly and safely, aiming for as many profitable conversions as possible at about `650% ROAS`.

The owner wants aggressive but smart revenue growth and profit growth, with fast execution and subagent orchestration wherever it can move faster. Do not get stuck in audit-only mode. Audits are support work only; progress must show up as actual sales-moving changes or exact unblock actions: controlled campaigns built/enabled under approval, performance monitored, keywords/negatives/copy/assets improved, landing pages fixed, catalog/feed blockers removed, approved paused drafts built, or blockers narrowed to one concrete next action. Build and repair what can safely be built, but preserve explicit approval boundaries around live spend, campaign enabling, budgets, product scope, feed labels, conversion goals, and product data.

Important business-model correction: Dress Like Mommy is a dropshipping business. It does not have a physical store and does not hold owned physical inventory. Do not write policy, ad, listing, feed, or report copy that implies a retail location, warehouse, local inventory, stocked inventory, or guaranteed on-hand stock. Platform terms such as Merchant/Pinterest `in_stock`, Shopify `inventory`, or `Missing local inventory data` are channel/feed salability diagnostics, not permission to fabricate physical inventory claims.

Important standing owner authorization: for paid-growth continuation work, the owner does not want a single-agent-only execution model when an orchestrator plus subagents can move faster. Treat this prompt as explicit authorization to spawn parallel subagents where the platform supports it, after reading coordination files and assigning disjoint workstreams/tabs. If subagent tooling is unavailable, say so clearly in the first status update and still execute the same workstreams by the fastest safe sequential/local path.

Important non-blocking execution rule: do not let one stuck workstream freeze the whole growth sprint. If one lane is blocked by Merchant processing, app/source refresh, browser access, policy review, missing approval, login/CAPTCHA, or any other external wait, open or update the problem in `ops/PROBLEM_TRACKER.md`, record the attempts/results/evidence/next action, and continue other independent lanes that move toward the North Star. For example, if Merchant age_group/source refresh is blocked, keep moving on paused Google Search country infrastructure, Pinterest read-only gates or paused drafts, localization/shipping QA, CRO/theme-local fixes, ROAS/economics rules, creative/RSA copy packs, and reporting/readback packets where safe.

Important solve-to-completion rule: a problem is not a note. It is a live work item until it is fixed, disproven, superseded by a safer solution, or gated by exact owner approval/credentials with the next concrete unblock action named. Do not document a known problem and then evade it. Work the solution, learn from failed attempts, update the tracker, and close only with evidence.

Important progress standard: the owner needs to see movement toward sales, not just better paperwork. Every substantial session should end with at least one of these outcomes unless every lane is gated: live approved campaign progress, paused/ready campaign infrastructure created, platform access restored, landing/conversion/feed blocker fixed, search-term/ROAS optimization decision made from evidence, or a precise owner/platform unblock action prepared. If a lane is blocked, keep another independent paid-growth lane moving.

## First actions

1. Read `AGENTS.md`.
2. Read `ops/MEMORY_CONTINUITY_PROTOCOL.md` so completed fixes are not forgotten or repeated.
3. Read `ops/PROBLEM_SOLVING_PROTOCOL.md`.
4. Read `ops/PROBLEM_TRACKER.md`.
5. Read `ops/AGENT_COORDINATION.md`.
6. Read `ops/BROWSER_SUBAGENT_COORDINATION.md` before orchestrating subagents or using logged-in ChatGPT Atlas / in-app browser tabs.
7. Read `ops/GROWTH_NORTH_STAR.md` so all work is tied to the owner’s definition of "promise land."
8. Read the latest entries at the bottom of `ops/AGENT_WORKLOG.md`. As of this prompt refresh, the latest paid-growth anchor is:
   - `AGENT_CONTINUITY_ANCHOR: 2026-05-12-es-it-native-signoff-bundle`
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
- The owner can also see what changed that could produce sales, not just what was audited.

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
- The owner gave the exact paused non-US Google Search `TEST BUILD` approval on 2026-05-10. Parent/orchestrator performed a partial approved build. Non-US Search campaigns were built and final-readback passed for `GB` (`23838895360`, `$2/day`), `CA` (`23834423669`, `$2/day`), `AU` (`23834424182`, `$2/day`), `CH` (`23834425358`, `$1/day`), `DK` (`23838969244`, `$1/day`), `DE` (`23834427575`, `$1/day`), `NL` (`23829110118`, `$1/day`), `SE` (`23838970036`, `$1/day`), `ES` (`23829133584`, `$1/day`), `IT` (`23829232530`, `$1/day`), `PL` (`23829238698`, `$1/day`), and `CZ` (`23829253812`, `$1/day`). All 12 were created as Search, presence-only, content/YouTube off, with paused status at creation and `88/88 # OK` preview/apply validation where applied; `GB`, `IT`, `PL`, and `CZ` required narrow approved presence-only repairs after readback found positive geo targeting at `DONT_CARE`, and post-repair readbacks passed. After exact 2026-05-12 owner approvals, `GB`, `CA`, and `AU` are now the first English-first exact Search live micro-cohort: each has campaign enabled, exact ad group `Mommy & Me Dresses - Exact` enabled, exact keywords `mommy and me dresses`, `mother daughter dresses`, and `mom and daughter matching outfits` enabled, and one RSA enabled. Final URLs were rechecked before inner enable and matched the intended market presentment: GB/GBP, CA/CAD, AU/AUD. Final RPC readback confirmed budgets remain `$2/day`, Search only, content/YouTube off, presence-only, no campaign conversion-goal override, and all other GB/CA/AU ad groups paused. Entity-page UI showed exact keywords and RSAs eligible; a follow-up campaign overview monitor at `2026-05-12T07:38:01-04:00` showed all three campaigns `Enabled` / `Eligible`, clearing the stale paused-inner-entity message. The shared 37-term negative base is acceptable only for the exact-match opening layer; phrase/broad/native expansion requires country/language-specific negatives from evidence. No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product-scope, feed-label, product-group, conversion-goal, budget, bid, or product/feed/conversion write occurred outside the exact approved GB/CA/AU status scope. `RO` remains absent/uncreated: a 2026-05-10 recheck first found the existing preview still in progress/error `0`, then a refreshed upload-history readback plus 90-second poll made the `RO` preview not visible; no `RO` apply was clicked. `PT` and `GR` remain absent/unattempted because the one-country-at-a-time guard blocks stacking behind unresolved `RO`. `FR` is parked because a stale/in-progress preview/apply recovery produced `completed with errors` / `no changes` and no FR campaign; `BE` is parked because Google Ads returned an upload-throttle message (`too many simultaneous uploads` / too many recent spreadsheets). `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE` is still `PARTIAL_12_APPLIED_RO_UPLOAD_THROTTLE_STILL_ACTIVE_PT_GR_ABSENT_FR_STALE_BE_THROTTLE`. Next Ads build action is wait for upload-throttle/file-picker cooldown, confirm no active in-progress RO/FR/BE row and no RO campaign, then retry one-country `RO` preview only; `FR` still needs a fresh non-stale completed `88/88 # OK` preview and no-duplicate readback, and `BE` remains last after upload-throttle cooldown. Do not re-upload completed countries. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/GB_CA_AU_INNER_ENABLE_EXECUTION_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/raw/post-enable-readback/final_success_summary.json`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/raw/post-inner-ui-entity-pages/`, the updated GB/CA/AU monitoring packet, the GB shell-enable packet, the CA/AU shell-enable packet, and prior 2026-05-10 build packets.
- Stale local packet guard: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/` is historical/reference-only for Ads state. It predates `IT`, `PL`, and `CZ` completion plus the later `RO` stale/not-visible readback. Use `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/PAID_GROWTH_GOAL_ORCHESTRATED_FOLLOWUP_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-measurement-ads-branch-continuation/PAID_GROWTH_MEASUREMENT_ADS_BRANCH_CONTINUATION_REPORT.md`, and the later RO/PT/GR reports for current state.
- Current measurement gate `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` is `GA4_TRANSACTION_REPORT_VISIBLE__ORDER_LEVEL_NON_US_CURRENCY_VALUE_PROOF_STILL_REQUIRED`: a 2026-05-10 browser readback partially passed pre-purchase measurement for `GB`/`GBP` and `DE`/`EUR`, and the 2026-05-11 read-only Google Ads conversion-action refresh again showed `Google Shopping App Purchase` as the single Primary account-level purchase action with dynamic value/recent request evidence. The 2026-05-11 Shopify Admin read-only hunt found `7` sanitized non-USD presentment order candidates since 2026-04-01 (`DKK`, `GBP`, `CHF`). GA4 UI access to account `88409806`, property `330266838`, visible `dresslikemommy.com - GA4` is proven, and Events pagination showed `purchase` row `12` for `Apr 13 - May 10, 2026` with `17` events, `16` users, and `$1,103.34` total revenue. A 2026-05-12 read-only GA4 UI/CDP pass advanced this by reaching the GA4 transaction ID report route with visible `purchase` and `transaction` text, but it still did not expose usable order-level event currency, value, or a sanitized non-USD order-candidate match. A sanitized network-response probe found report/config snippets only, not order-level proof. Read-only GA4 Admin/Data API matching remains blocked by `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT` with the existing `gcloud` token. Before any non-US enablement, use GA4 UI Explore/report export or refreshed read-only GA4 API scopes to prove actual `purchase` event currency/value/transaction evidence; if no genuine event can be observed, request exact owner approval for a controlled non-US test purchase/refund/cancel procedure. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-measurement-safe-lanes/PAID_GROWTH_MEASUREMENT_SAFE_LANES_REPORT.md`, `ga4_readonly_probe/ga4_event_level_dimension_probe_summary.json`, `ga4_readonly_probe/ga4_network_sanitized_probe_summary.json`, and the prior 2026-05-11/2026-05-10 measurement packets.
- `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` is now `ES_IT_SIGNOFF_BUNDLE_PENDING_NATIVE_REVIEW__NO_UPLOAD`: the 2026-05-10 expert-hardened packet remains the source layer with `700` exact/phrase keyword rows, `205` localized negative-keyword review rows, and `70` RSA rows across `14` locale variants, all `REVIEW_ONLY_NOT_UPLOAD`. A 2026-05-11 AI/native-risk triage reviewed the packet by locale without regenerating it; the follow-up local-only rewrite packet then created `450` keyword replacement rows, `45` RSA replacement rows, `133` negative-review replacement rows, and `15` locale-status rows for `es-ES`, `it-IT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`, `pl-PL`, and `cs-CZ`. A 2026-05-12 ES/IT slice packet extracted `100` keyword rows, `10` RSA rows, `30` negative-review rows, and `2` locale-status rows for native review, all `REVIEW_ONLY_NOT_UPLOAD`, and created `ES_IT_NATIVE_REVIEW_REQUEST.md`. Slow country-qualified Golden Daisy landing QA passed for `/es/products/golden-daisy-mommy-and-me-set?country=ES` and `/it/products/golden-daisy-mommy-and-me-set?country=IT`: HTTP `200`, `es`/`it`, EUR, expected native terms, no verification/429, no supplier/source-domain hits, and no stale paid blockers. The Golden Daisy-only ES/IT microtest passed its 44-check verifier and now has a concrete native-review signoff bundle: `ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_BUNDLE.md`, `ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_FORM.csv`, and `validate_es_it_native_signoff_form.py`. Latest validator result is `PENDING_NATIVE_REVIEW`, `platform_use_ready=false`, `8` pending rows, and all structural checks pass. ES/IT still require real native-speaker signoff and exact owner action-time approval before platform use. `pt-PT`, `da-DK`, `fr-BE`, `nl-BE`, `el-GR`, and `CH` remain gated until documented dialect/native-review/language-split decisions and landing-language QA are resolved. RO/DE/SE/CZ still have public supplier/source-token blockers; DE/SE have language/route issues; NL/FR/PL/CZ need native landing review plus updated country-qualified final URL maps before platform use. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_BUNDLE.md`, `ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_FORM.csv`, `es_it_golden_daisy_native_review_signoff_validation_summary.json`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/ES_IT_NATIVE_REVIEW_REQUEST.md`, `ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md`, `ES_IT_NATIVE_QA_NO_UPLOAD_SLICE_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/NATIVE_REWRITE_LOCAL_ONLY_REPORT.md`, and `validation_summary.json`.
- Pinterest review-only paused-draft templates now exist for the clean `342` EN-US scope with `4` exclusions; the templates are not Pinterest upload files and are marked review-only. Event Quality remains `Fair`; any Pinterest draft, campaign, product-group, audience, budget, bid, tag/CAPI, status, or spend write still requires exact owner approval and readbacks. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`.
- Pinterest multilingual keyword/copy quality now has a local-only `54`-row catalog/copy term plan in the 2026-05-10 keyword-quality packet. It treats Pinterest quality as catalog/source, product-group, creative copy, destination consistency, country targeting, and Event Quality proof, not as a Google-style keyword import. Non-US Pinterest remains account-write-gated because no country-specific Pinterest source/catalog/product-group readbacks exist. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade/pinterest_multilingual_keyword_interest_quality_plan.csv`, `PINTEREST_KEYWORD_QUALITY_GATES.md`.

- 2026-05-10 authority safe-launch prep update: owner clarified broad authority to get everything ready and start advertising only when the setup is clean. Packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/` now defines the hard pass gates before any new spend, corrects the first-enable GB ad group name to the actual readback value `Mommy & Me Dresses - Exact` (not stale `Mommy & Me Dresses - Exact only`), adds first-14-day monitoring templates, runs fresh read-only GB campaign RPC and absent readbacks for `RO`/`PT`/`GR`/`FR`/`BE`, and resolves the GB final-URL raw `curl` uncertainty with a browser-style readback: the exact GB URL loaded, showed GB/GBP presentment, no visible verification wall or stale Christmas metadata, add-to-cart worked, and checkout entry was reached with no payment/order. Live advertising is still not clean to start because non-US purchase-event currency/value proof remains open and Google Ads upload throttle still blocks `RO`. No live spend or enablement occurred.
- 2026-05-10 Pinterest/native prep update: non-US Pinterest now has local-only review templates for all 17 markets, but every non-US Pinterest market remains account-write-gated because no country-specific Pinterest source/catalog/product-group/readback scope exists; first future local packet candidates are `GB`, `CA`, then `AU`. Native-copy deep QA covers all 14 locale variants and `70` theme rows with `0` length violations and `0` automated forbidden-claim hits, but `pt-PT`, `da-DK`, `fr-BE`, and `nl-BE` are platform-use-blocked until named language/split issues close; `es-ES`, `it-IT`, and `ro-RO` are only concept-ready pending native review.
- 2026-05-10 multilingual matrix update: packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-platform-matrix/` confirms all Google Ads language/platform cells and Pinterest cells are either complete to safe extent or gated. Google Ads is `12 built / 3 absent / 2 parked`; all 17 split CSVs remain locally safe. Pinterest is account-ready only for US `en-US`; the later non-US Pinterest files are local-only operator templates, with no non-US country-specific Pinterest catalog/source/product-group/readback scope. Because the current owner goal forbids budget/bid/status changes, no new paused account objects were created in that session; future paused account-object creation requires fresh action-time approval that reconciles necessary initial budget/bid/status setup fields.
- AU checkout `429` is solved: isolated-browser QA reached AU/AUD shipping rates with no verification page, no payment, and no order. GB and CA visual checkout UI is solved for paused infrastructure. CH, DK, DE, FR, BE, SE, PL, CZ, and GR no-payment checkout-to-shipping QA passed on 2026-05-09. NL is now also solved for paused-infrastructure checkout evidence: after the prior cart/rates `429` cleared, one adjusted isolated no-payment/no-bypass pass confirmed Netherlands selected in checkout UI, checkout `en-NL`, cart currency `EUR`, Standard `FREE`, Express `EUR 11.95`, no `429`/CAPTCHA/verification, no payment data, no Pay Now/Place Order click, and no order. All `17` international target markets passed low-volume product landing GET checks, and all `17` proposed non-US Search countries now have at least paused-infrastructure checkout/rate evidence, but live-spend-ready markets remain `0` until approval, tracking/catalog/feed/URL/economics gates clear. `PROB-2026-05-09-DE-NL-CHECKOUT-QA`, `PROB-2026-05-09-FR-BE-CHECKOUT-QA`, and `PROB-2026-05-09-SE-PL-CZ-GR-CHECKOUT-QA` are solved as readbacks for paused infrastructure only.
- Paid-landing blocker `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`: product `7227378892897` / handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` has stale Christmas title/OG/Twitter metadata on a beach/vacation paid-candidate URL, including sampled ES/IT/RO/PT localized metadata. Local Ads import risk is partially mitigated by the held `1496`-row CSV, but do not send live paid traffic to this URL until exact-owner-approved Shopify SEO/social-title repair passes public readback, or use the held/excluded URL packet for any future approved paused Ads import.
- No PMax enable. No international live spend. No Pinterest live spend unless the owner gives explicit action-time approval.
- 2026-05-12 owner directive: stop spending time rechecking tags/Event Quality/GA4 proof as a launch-prep blocker; assume tags are correct. The owner also set the active operating objective to grow paid-marketing sales as fast as safely possible, aiming for profitable 650% ROAS conversions with no artificial ceiling. This authorizes nonstop safe read-only/local/paused/prep work and exact-approved live actions, but it still does not authorize unnamed broad live spend/status/budget/feed/product/conversion/Pinterest account writes. GB/CA/AU exact Search inner entities were later enabled under exact approval: campaigns `23838895360`, `23834423669`, and `23834424182`; exact ad groups `194138528537`, `196679079575`, and `198852670520`; exact keyword criteria `299141671628`, `301154335636`, and `301154336396` in each market; RSA ads `808406712704`, `808294804728`, and `808328767090`. Readbacks passed with budgets `$2/day`, Search only, presence-only, no conversion override, and all other GB/CA/AU ad groups paused. URLs were checked for GB/GBP, CA/CAD, and AU/AUD; entity UI showed eligible rows; follow-up campaign overview monitor showed all three campaigns `Enabled` / `Eligible`. Controlled GB/GBP purchase precheck reached `GBP £12.00` total with no payment and stopped because no safe payment/test path was available. Pinterest paused US draft build is exact-approved but blocked by authenticated Pinterest Ads Manager access in the controllable browser. RO paused Google Search build is exact-approved but blocked by Google Ads native/custom file-picker access; no RO preview/apply occurred and RO remains absent. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/GB_CA_AU_INNER_ENABLE_EXECUTION_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/raw/post-enable-readback/final_success_summary.json`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/raw/monitoring_summary.json`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-ca-au-enable-live/CA_AU_ENABLE_EXECUTION_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-non-us-first-enable-gb-live/FIRST_ENABLE_GB_EXECUTION_REPORT.md`, and `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-controlled-measurement-pinterest-build/CONTROLLED_MEASUREMENT_PINTEREST_BUILD_REPORT.md`.
- 2026-05-12 performance/access/local growth update after GB/CA/AU: post-inner GB/CA/AU route probe shows fresh-start reporting zeros: `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions, `0.00` conversion value, and no actionable attributable search terms yet. The working Google Ads search-term route is `/aw/keywords/searchterms`; direct `/aw/searchterms` and `/aw/search-terms` returned `404`, and the working page showed an unrelated stale `Keyword: "human hair wigs"` UI filter, so no negative edit was made. Pinterest GB/CA/AU local readiness packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-pinterest-gb-ca-au-local-scope-readiness/PINTEREST_GB_CA_AU_LOCAL_SCOPE_READINESS.md`; it confirms US `342` EN-US scope remains the only proven Pinterest scope and GB/CA/AU have no country-specific Pinterest source/catalog/product-group readback yet. The approved paused US Pinterest draft remains blocked because fresh CDP retry landed on `https://ads.pinterest.com/` with login hints and no Create control; Chrome DevTools profile recovery was locked and Computer Use returned Apple event error `-1743`. ES/IT native no-upload packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice/`; extracted ES/IT rows are `100` keywords, `10` RSAs, `30` negative-review rows, and `2` locale-status rows, all `REVIEW_ONLY_NOT_UPLOAD`; native-review request is ready; country-qualified Golden Daisy landing QA passed. No Pinterest account write, Google Ads preview/import/upload/copy association, campaign/ad group/ad/keyword/status/budget/bid edit, Merchant/Shopify product/feed/conversion write, or live spend occurred in these packets.
- 2026-05-12 sales-moving continuation update: latest paid-growth anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-12-gb-ca-au-1721-zero-data-monitor`. Parent reran GB/CA/AU read-only monitoring at `2026-05-12T17:20:41-04:00`; all three campaigns still read enabled/eligible at the exact approved scope, `$2/day`, Search only, presence-only, no conversion override, with only `Mommy & Me Dresses - Exact` enabled, `9` other ad groups paused, and still `0` impressions/clicks/cost/conversions/value. A fresh route probe at `2026-05-12T17:21:23-04:00` confirmed direct `/aw/searchterms` and `/aw/search-terms` still return `404`; the working route remains `/aw/keywords/searchterms`, but it still carries stale unrelated filter `Keyword: "human hair wigs"`, so there is no attributable search-term action. This zero-data state is appended to `gb_ca_au_optimization_baseline_log.csv`; no negative, pause, scale, budget/bid, status, or ROAS decision is justified until data appears. Pinterest access recovery remains blocked, but a local machine-readable Pinterest paused US draft build spec exists and has a semantic verifier: `validate_pinterest_us_paused_draft_spec.py` passed `21` checks against the clean `342` scope and `4` exclusions. Golden Daisy is the cleaner ES/IT candidate after native signoff; its `REVIEW_ONLY_NOT_UPLOAD` microtest packet now has a semantic verifier, `validate_es_it_golden_daisy_microtest.py`, which passed `44` checks against the source native packet, landing QA, checkout-to-shipping QA, fixed ES/IT Golden Daisy URLs, `EUR` cart currency, no verification wall, and no payment/order. `RO` has a local preview-only execution spec for `RO_intl_search_paused_draft_web_bulk.csv` with explicit no-duplicate/clean-preview/apply-readback gates. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live/GB_CA_AU_1721_ZERO_DATA_DECISION_UPDATE.md`, `gb_ca_au_optimization_baseline_log.csv`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/raw/monitoring_summary.json`, `raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary.json`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_pinterest_us_paused_draft_spec.py`, `pinterest_us_paused_draft_build_spec_validation_summary.json`, `validate_es_it_golden_daisy_microtest.py`, `es_it_golden_daisy_microtest_validation_summary.json`, `PINTEREST_US_PAUSED_DRAFT_BUILD_SPEC.md`, `ES_IT_GOLDEN_DAISY_MICROTEST_REVIEW_ONLY.md`, `RO_GOOGLE_SEARCH_PREVIEW_ONLY_EXECUTION_SPEC.md`, and `CONTINUATION_HANDOFF.md`.
- 2026-05-12 follow-up: latest paid-growth anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-12-pinterest-es-it-verifier-refresh-auth-blocked`. Parent retried Pinterest access after the `17:21` zero-data Ads monitor: the Chrome skill path could not expose the preferred `node_repl` runtime, Chrome DevTools MCP was locked on the running profile, Playwright reached only the public unauthenticated Pinterest Ads page, and Computer Use still failed with Apple event error `-1743`. No Pinterest write occurred. Parent refreshed the local gates: clean Pinterest scope still has `342` rows plus header, exclusions still have `4` rows plus header, SHA256 values match the validated scope, `validate_pinterest_us_paused_draft_spec.py` passed `21` checks, and `validate_es_it_golden_daisy_microtest.py` passed `44` checks. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/PINTEREST_ES_IT_VERIFIER_REFRESH_AND_ACCESS_BLOCK.md`. Next: restore authenticated Pinterest Ads Manager access for advertiser `549756244483`, then build only paused US draft objects from the `342` scope with `4` exclusions after before-write readbacks; send ES/IT Golden Daisy to native review; re-monitor GB/CA/AU when reporting data exists.
- 2026-05-12 monitoring hardening update: latest paid-growth anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-12-gb-ca-au-searchterms-filter-guard`. Parent updated `gb_ca_au_perf_search_terms_route_probe.py` to expose `active_filter_lines`, `has_stale_human_hair_filter`, `stale_filter_hits`, `search_terms_actionable`, and `search_terms_actionability_note`, plus a fast `--routes keywords_searchterms` mode. A full read-only route probe at `2026-05-12T17:36:21-04:00` still showed GB/CA/AU visible metrics at `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions/value. Direct `/aw/searchterms` and `/aw/search-terms` remain `404`; `/aw/keywords/searchterms` loads but all three markets are non-actionable because the stale unrelated `Keyword: "human hair wigs"` filter is present. No negative, pause, scale, budget/bid/status, CPA, or ROAS action is justified. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/GB_CA_AU_SEARCH_TERM_PROBE_FILTER_GUARD.md`.
- 2026-05-12 evaluator update: latest paid-growth anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-12-gb-ca-au-optimization-readiness-evaluator`. Parent added and ran a local-only optimizer decision evaluator: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/evaluate_gb_ca_au_optimization_readiness.py`. It reads saved monitor artifacts only, applies the first-72h plan (`650%` ROAS, `$10.77` target CPA, `$16.00` zero-purchase pause-review threshold), and wrote `GB_CA_AU_OPTIMIZATION_READINESS_DECISION.md`, `raw/gb_ca_au_optimization_readiness_summary.json`, and `raw/gb_ca_au_optimization_readiness_summary.csv`. Result: GB, CA, and AU all safety-pass but remain `HOLD_MONITOR_NO_OPTIMIZATION_WRITE`; no live negative, pause, scale, budget/bid/status, CPA, or ROAS conclusion is justified. Next Ads action is another read-only monitor after reporting/search terms become actionable.

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
