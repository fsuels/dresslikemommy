# Marketing Prompt Log

Last updated: 2026-05-14 08:24 EDT

## Canonical Paid-Growth Prompt

Primary prompt:

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`

Do not create competing paid-growth continuation prompts. Packet-level prompts may point back to the canonical prompt and name the latest anchor, blockers, and gates.

## Next Goal: Read-Only Live Reconciliation

```text
/goal Reconcile current live paid-growth state without making external writes until ops/marketing/current_marketing_state.md and ops/marketing/daily_scorecard.md show which Google Ads and Pinterest objects are enabled, eligible, serving, spending, converting, blocked, and ready for bounded execution.

Repository:
- /Users/fsuels/Projects/dresslikemommy

Read first:
- AGENTS.md
- ops/marketing/AGENTS.md
- ops/marketing/current_marketing_state.md
- ops/marketing/action_queue.md
- ops/marketing/spend_authorization.md
- ops/marketing/daily_scorecard.md
- ops/marketing/blocker_board.md
- ops/MEMORY_CONTINUITY_PROTOCOL.md
- ops/PROBLEM_SOLVING_PROTOCOL.md
- ops/PROBLEM_TRACKER.md
- ops/AGENT_COORDINATION.md
- ops/BROWSER_SUBAGENT_COORDINATION.md
- ops/GROWTH_NORTH_STAR.md
- ops/GOOGLE_ADS_CONTINUITY.md
- ops/prompts/paid-growth-ai-army-continuation-prompt.md
- Latest entries at the bottom of ops/AGENT_WORKLOG.md

Goal:
- Confirm what is actually enabled, eligible, serving, spending, converting, blocked, and decision-ready today across Google Ads GB/CA/AU exact Search, Standard Shopping, Pinterest access/draft readiness, Merchant/Pinterest blockers, and ROAS/search-term state.

Constraints:
- No live Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme writes.
- Use read-only account views, local artifacts, and public storefront readbacks only.
- Treat ops/marketing/current_marketing_state.md as stale repo-known state until live readback proves otherwise.
- Update ops/marketing/current_marketing_state.md, daily_scorecard.md, action_queue.md, blocker_board.md, decision_log.md, ops/AGENT_WORKLOG.md, and ops/PROBLEM_TRACKER.md if blockers change.

Done when:
- The command layer shows the fresh readback date/time and states.
- Each active surface has a hold/scale/pause/fix/approval-needed decision, or a precise reason data is not actionable.
- No external write occurred.
```

## Goal Execution: 2026-05-14 Read-Only Live Reconciliation

Status: `DONE_NO_EXTERNAL_WRITES`

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/LIVE_RECONCILIATION_REPORT.md`

Result:

- GB/CA/AU exact Search: enabled/eligible at approved scope, but zero cost/clicks/impressions/conversions/value for `2026-05-13`; decision `HOLD_MONITOR_NO_WRITE`.
- Standard Shopping: enabled/eligible, `17` impressions, `0` clicks, `$0.00` cost, `0.00` conversions/value for `2026-05-13`; decision `HOLD_MONITOR_NO_WRITE`.
- Pinterest: current controllable browser is unauthenticated; Ads Manager create path blocked before any draft write.
- Merchant US/es age_group: samples cleared, stale May 8 export not current; current exact all-row readback still needed before repair/closure.
- Merchant capacity: new prioritized-fix blocker observed, `Over capacity for Shopping ads (outside of CSS program)`.

## Next Goal: Landing Source Leak Fix, Active-Product Map, Merchant/Pinterest Unblock

```text
/goal Prepare the next bounded paid-growth execution step without making external writes until the active paid landing supplier/source leak, active-product advertising map, Pinterest access, and Merchant current blockers are read back cleanly.

Use:
- ops/marketing/current_marketing_state.md
- ops/marketing/daily_scorecard.md
- ops/marketing/action_queue.md
- ops/marketing/blocker_board.md
- ops/PROBLEM_TRACKER.md
- dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/LIVE_RECONCILIATION_REPORT.md

Constraints:
- No Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme writes.
- Historical note: spend authorization was `PENDING_OWNER_APPROVAL` when this prompt was written; current sessions must trust `ops/marketing/spend_authorization.md`.
- Do not advertise inactive, draft, unpublished, stale, seasonally mismatched, unresolved, or supplier-leaking products.
- Do not let supplier/vendor/source URLs appear in customer-visible HTML, analytics attributes, feed-visible data, ad copy, or shopper-facing copy.
- Do not request or perform Merchant US/es age_group repair from stale May 8 CSV evidence alone.
- Do not create Pinterest account objects until authenticated Ads Manager access and before-write readbacks are clean.

Done when:
- Active GB/CA/AU paid landing source is live-clean after approved sanitizer sync, or the exact approval needed is stated.
- Active-product/category advertising map is ready from current readbacks, with non-active and supplier-leaking URLs excluded.
- Event/category layers are intent-matched, including Father's Day routed to Daddy-and-Me and father-inclusive family matching products.
- Merchant US/es has a current exact all-row readback or a precise blocker explaining why it cannot be obtained.
- Merchant Shopping Ads capacity has a read-only impact assessment for the paid cohort / Standard Shopping.
- Pinterest Ads Manager access is either restored and read back, or the exact owner/browser unblock action is documented.
- The command layer names the single next bounded execution row and the approval phrase needed, if any.
```

## Goal Execution: 2026-05-14 GB/CA/AU Keyword Strategy Repair

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/GB_CA_AU_DAY1_ZERO_IMPRESSION_KEYWORD_STRATEGY_REPAIR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/gb_ca_au_high_intent_candidate_map.csv`

Result:

- GB/CA/AU exact Search strategy now treats the current three exact terms as starter controls, not the full plan.
- GB has English-UK mum/mummy/holiday/photo/wedding/beach candidate themes.
- CA has English-Canada candidate themes and keeps French-Canada separate until native review and landing QA.
- AU has English-Australia mum/mummy/holiday/beach-photo/swim candidate themes.
- Candidate rows are `review_only_not_uploaded`; no live Google Ads write occurred.

Next:

- Run the fresh read-only GB/CA/AU monitor with CA/AU stale filters absent, Quality Score/RSA/final URL checks, live paid-landing sanitizer state, and current sales/ROAS before any live action.

## Goal Execution: 2026-05-14 Fresh GB/CA/AU Ads Monitor And Gate Review

Status: `DONE_READONLY_BLOCKED_NO_EXTERNAL_WRITES`

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/FRESH_GB_CA_AU_ADS_MONITOR_AND_GATE_REVIEW.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Result:

- GB/CA/AU Ads-side readback passed for campaign scope, ad group scope, enabled keywords, enabled RSA, and country-qualified final URLs.
- Stale `Keyword: "human hair wigs"` search-term filters were cleared on GB/CA/AU; no search terms are available afterward.
- Keyword UI shows `Eligible (Limited)` / below-first-page-bid estimates around `$0.65-$0.74` while max CPC remains `$0.15`.
- Live GB/CA/AU final URL source still exposes `detail.1688.com` in `data-analytics-vendor`; live action is blocked.

Next:

- Get scoped live theme sanitizer sync/readback approval, then rerun the Ads monitor/reviewer before any keyword or bid action.

## Goal Execution: 2026-05-14 $0.15 CPC Long-Tail Correction

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/CPC_015_LONG_TAIL_CORRECTION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Result:

- Owner corrected that `$0.15` CPC is a hard ceiling, not a preference.
- Current active head terms read as below-first-page at about `$0.65-$0.74`, so they are rejected for bid-up or expansion.
- Close variants like `[mummy and me dresses]`, `[mommy and me dresses canada]`, and `[mummy and me dresses australia]` are now rejected as lazy close-head rows, not long-tail strategy.
- The blocked packet now contains only product-specific, buyer-moment long-tail validation candidates; they still require live landing clean readback and `$0.15` CPC validation before upload.

Next:

- After approved live sanitizer sync/readback, validate corrected long-tail rows in Keyword Planner or keyword UI at max CPC `$0.15`; do not raise bids and do not upload head/near-head variants.

## Goal Execution: 2026-05-14 Expert Keyword Factory Criteria

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `ops/marketing/keyword_factory_015_cpc_criteria.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Result:

- Added the operating criteria for creating a big high-intent long-tail keyword universe while still protecting sales/ROAS economics.
- Rule: build the candidate universe as large as possible locally, but live-upload only validated batches that pass market/language, buyer intent, landing fit, economics, conversion plausibility, no-cannibalization, and negative-fit gates.
- Added the fix-now rule: repo-local mistakes get fixed immediately; approved live mistakes get fixed and read back; unapproved live writes become exact smallest approval packets, not passive blocker notes.

## Goal Execution: 2026-05-14 Proactive Action/Results Mandate

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `AGENTS.md`
- `ops/marketing/AGENTS.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Result:

- Owner directive encoded durably: results and proactive action matter more than monitor loops.
- If a mistake, broken state, underperforming path, or clear improvement is visible, agents must fix it when safe/approved.
- If live approval is missing, agents must prepare the smallest exact approval packet and keep another safe sales-moving lane moving.
- Every monitor/readback must end in `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.

## Goal Execution: 2026-05-14 Action-Biased Keyword Universe

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `ops/marketing/keyword_strategy.md`
- `ops/marketing/keyword_scoring_rubric.md`
- `ops/marketing/keyword_universe.csv`

Result:

- Agreed with the expert correction: build the keyword universe as large as possible locally, but live-promote only small validated batches.
- Created a 105-row local universe: `60` US-first rows, `15` GB, `15` CA, and `15` AU.
- Rubric now uses buyer intent `25`, product match `20`, occasion/deadline `15`, landing match `15`, economic fit `10`, serveability `10`, and waste risk `5`.
- CSV validation passed: `77` `GREEN`, `20` `YELLOW`, `8` `RED`; all score sums and thresholds matched.
- No live keyword upload or external account write occurred.

Next:

- Validate top `GREEN` rows against active products, clean landing routes, and `$0.15` auction-entry evidence before any live packet.

## Goal Execution: 2026-05-14 Command-Layer Integration Guard

Status: `DONE_LOCAL_NO_EXTERNAL_WRITES`

Evidence:

- `ops/scripts/audit_marketing_command_integration.py`
- `ops/marketing/command_layer_integration_audit.md`
- `ops/marketing/AGENTS.md`
- `ops/marketing/action_queue.md`

Result:

- Initial integration audit found `4` side-document risks.
- Fixed them by registering keyword factory and US lane docs, marking migration trace as an archive reference, and linking the consolidation prompt through the action queue.
- Current audit reports `25` tracked files, `25` integrated/generated/archive files, and `0` side-document risks.

Next:

- Run the audit before closing any future session that creates or materially changes files under `ops/marketing/`.

## Reusable Prompt: Safe Execution With Reviewer

```text
/goal Continue Dress Like Mommy paid-growth execution from the latest AGENT_CONTINUITY_ANCHOR, execute only safe rows, and use the Marketing Safety Reviewer before risky decisions.

Repository:
- /Users/fsuels/Projects/dresslikemommy

Read first:
- AGENTS.md
- ops/marketing/AGENTS.md
- ops/marketing/operator_cockpit.md
- ops/marketing/expert_growth_playbook_2026.md
- ops/marketing/current_marketing_state.md
- ops/marketing/action_queue.md
- ops/marketing/daily_scorecard.md
- ops/marketing/blocker_board.md
- ops/marketing/spend_authorization.md
- ops/marketing/assumption_log.md
- ops/marketing/reviewer_checklist.md
- ops/marketing/review_log.md
- ops/marketing/team_registry.md
- ops/PROBLEM_TRACKER.md
- ops/AGENT_COORDINATION.md
- latest AGENT_CONTINUITY_ANCHOR in ops/AGENT_WORKLOG.md

Execution:
- First run `python3.13 ops/scripts/open_marketing_cockpit.py` so the human cockpit opens automatically in the browser.
- Continue from the latest anchor, not stale chat memory.
- Execute green safe rows when they are repo-local/read-only/paused-review-only, or when `spend_authorization.md` is `APPROVED_ACTIVE` and the action is inside caps, quality-gated, reviewer-cleared, and supports profitable sales at about `650% ROAS`.
- Do not wait passively for the owner when a bounded paid-media action is green-gated and within active authority; monitor, diagnose, act, read back, and log.
- Use `expert_growth_playbook_2026.md` before keyword, negative, bid, budget, campaign, Shopping, Pinterest, creative, landing, or measurement recommendations.
- Prioritize high-intent, low-waste, less-contested traffic; reject cheap traffic that is unlikely to buy; avoid self-cannibalization across campaigns, ad groups, countries, languages, Search, Shopping, Pinterest, and remarketing.
- Treat today as Day 1: tomorrow's scorecard must answer how many paid-growth sales happened, revenue, CPA, ROAS, whether progress improved, and what action is due today.
- If any active Search campaign has zero impressions after 24 hours, run same-day serving diagnosis and evaluate high-buyer-intent long-tail exact/phrase or auction-entry actions inside approval boundaries.
- Run or simulate marketing_safety_reviewer before any non-ops file edit, external write, blocker reclassification, or spend/budget/bid/status/feed/product/conversion recommendation.
- Clearly separate what was checked, what changed locally, what changed live, what remains blocked, next 3 tasks, assumptions, and evidence.
- Keep `ops/marketing/campaign_explorer.json` current for active/running campaigns: activation time, today/yesterday metrics, latest readback freshness, exact active objects, bid strategy and why it was chosen, keyword selection criteria, negative-keyword criteria, daily optimization owner, continuous-improvement loop, keywords/targeting, ad/creative quality, quality score or missing quality-score readback, landing-page/photo/product fit, success measurement against sales/ROAS/CPA, strategy/reasoning, assumptions being tested, improvement/pause/scale triggers, deadline/next decision, and evidence.
- Include expert-source standard, keyword economics, and anti-cannibalization rules in the campaign explorer for every active or ready lane.
- Update ops/marketing/operator_cockpit.md before stopping or compacting.
- Regenerate the one-screen human dashboard with `python3.13 ops/scripts/render_marketing_cockpit.py`.

Constraints:
- No live Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme publish write unless fresh explicit action-time approval covers it or `spend_authorization.md` is `APPROVED_ACTIVE` and the row is green-gated inside bounded paid-media authority.
- Keep bounded paid-media authority active only while ops/marketing/spend_authorization.md says APPROVED_ACTIVE; do not use it for excluded surfaces or incomplete-quality actions.
- Do not advertise inactive, draft, unpublished, stale, seasonally mismatched, unresolved, or supplier-leaking products.

Done when:
- The safest sales-moving row is completed or gated with an exact next unblock action.
- The reviewer outcome is logged when the decision is risky.
- operator_cockpit.md, operator_cockpit.html, and the relevant command-layer files reflect the current state.
```
