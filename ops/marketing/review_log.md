# Marketing Safety Review Log

Last updated: 2026-05-14 10:38 EDT

Use this log for reviewer outcomes or simulated checklist runs. Keep entries short and tied to evidence.

## 2026-05-14 - Automation capability mismatch plus Merchant capacity local diagnosis

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local capability inventory only: shell, repo writes, network, Playwright MCP, Chrome DevTools MCP visibility, Computer Use visibility, GitHub MCP visibility, and OpenAI docs MCP.
- Repo-local/read-only Merchant capacity diagnosis from already-saved evidence plus current command-layer state.
- No external writes, no blocker closure without proof, and no Merchant/Shopping recommendation that exceeds approval boundaries.

Risks:

- Authenticated Merchant and Pinterest account-surface readbacks are not equivalent in this runtime because Chrome DevTools is profile-locked and Computer Use interactive access is not granted.
- The current capacity warning is real, but the exact paid-cohort intersection is still unproven; Standard Shopping still had `17` impressions yesterday, so the warning could be broad account noise.

Required gates/fixes:

- Mark the account-surface gap explicitly as `AUTOMATION_CAPABILITY_MISMATCH`.
- Do not downgrade or close the Merchant capacity blocker from local evidence alone.
- Next Merchant action must be an authenticated read-only product-level intersection against the `780`-row `us_test_ready` / `paid_eligible` cohort.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-capability-merchant-capacity-diagnosis/AUTOMATION_CAPABILITY_AND_MERCHANT_CAPACITY_DIAGNOSIS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/merchant-product-issues-export/raw/product-issues-browser-export/diagnostics_page_text_before_download_priority.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/standard-shopping-readback/raw/01_productgroups_initial.txt`

Safest next sales-moving action:

- Use an authenticated Merchant session to prove whether the capacity warning touches the live paid cohort; keep the next independent sales-moving lanes active meanwhile.

## 2026-05-14 - Reviewer/cockpit implementation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local implementation of `marketing_safety_reviewer`, cockpit, assumption log, checklist, review log, marketing guide updates, Head of Growth instruction update, team registry update, prompt log update, and worklog anchor.
- Stopped-session dirty changes before editing, including supplier/source URL sanitizer changes and May 14 marketing command-layer updates.
- Spend authorization boundary.

Risks:

- Existing paid-landing sanitizer is still local only; live paid landing remains blocked for expansion until approved theme sync and public readback.
- Existing dirty worktree includes unrelated theme and command-layer changes that this implementation must preserve.

Required gates/fixes:

- Do not publish the sanitizer or mutate external marketing systems without fresh explicit approval.
- Keep `spend_authorization.md` at `PENDING_OWNER_APPROVAL` unless owner approves activation.

Evidence:

- `git status --short`
- `ops/AGENT_WORKLOG.md` latest anchors, especially `2026-05-14-paid-landing-vendor-source-sanitizer-local`
- `ops/marketing/current_marketing_state.md`
- `ops/marketing/spend_authorization.md`

Safest next sales-moving action:

- Seek scoped approval for live theme sync of the sanitizer files, or continue read-only Merchant/Pinterest unblock work if approval is unavailable.

## 2026-05-14 - Campaign explorer dashboard implementation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard and command-layer edits only: `campaign_explorer.json`, cockpit renderer, cockpit source, prompt log, marketing guide, and worklog anchor.
- Campaign details are sourced from saved repo evidence and are labeled when stale, blocked, or not live-verified.
- No supplier/source URL domains are exposed in the human dashboard data.
- Spend authorization boundary remains unchanged.

Risks:

- Google Ads and Pinterest facts shown in the campaign explorer are saved readback evidence, not a fresh live read performed during this UI-only pass.
- Pinterest remains not active from this plan because authenticated controllable Ads Manager access is blocked.
- Ad strength for GB/CA/AU exact Search is `Pending`; zero-data campaigns must not be optimized from assumptions.

Required gates/fixes:

- Do not change budgets, bids, statuses, keywords, ads, product groups, feed/product scope, or Pinterest objects without fresh explicit approval and fresh before/after readbacks.
- Keep `campaign_explorer.json` current after every material live readback or decision.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `ops/marketing/current_marketing_state.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/LIVE_RECONCILIATION_REPORT.md`

Safest next sales-moving action:

- Obtain scoped approval for live theme sync/readback of the paid-landing sanitizer, or continue read-only Merchant/Pinterest unblock lanes if approval is unavailable.

## 2026-05-14 - Proactive test monitor dashboard upgrade

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard/data/doc updates only; no platform surfaces or live account writes.
- Active campaign monitor fields now distinguish saved readback evidence from fresh-readback gaps.
- Zero-impression tests now show activation time, T+24/T+72/T+7d clock, assumptions, and improvement triggers.

Risks:

- Today 2026-05-14 Google Ads metrics are not live-read in this UI pass; the cockpit labels them as fresh readback needed.
- Any bid, budget, status, keyword, ad, product group, feed, conversion, or Pinterest object change still needs fresh explicit approval.

Required gates/fixes:

- Run fresh read-only live metrics before any optimization recommendation.
- Treat T+72 zero-impression state as a diagnosis/approval-packet trigger, not proof that a live change is already approved.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `GB_CA_AU_FIRST_72H_OPTIMIZATION_PLAN.md`
- `final_success_summary.json`

Safest next sales-moving action:

- Fresh read-only monitor for today/yesterday GB/CA/AU metrics and Shopping/Pinterest blockers, then decide whether a T+72 zero-impression diagnosis packet is needed.

## 2026-05-14 - Success measure, bid strategy, and full attention checklist

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard/data/doc updates only; no platform surfaces or live account writes.
- Success measurement is now explicit: maximize profitable sales while targeting about `650% ROAS`, with CPA/ROAS/conversion-value proof before scale.
- Campaign detail now distinguishes Manual CPC from Maximize Clicks and explains why the saved strategy was chosen.
- Full attention checklist now covers bidding, keyword quality/Quality Score, search terms, RSA/ad quality, landing page, product/photo fit, measurement, and decision discipline.

Risks:

- Quality Score columns and today metrics were not live-read in this UI pass; the cockpit labels them as required readbacks.
- Any bid strategy change, including Maximize Clicks, is a live campaign write and still needs fresh exact approval.

Required gates/fixes:

- Run fresh read-only quality/metric readbacks before any bid, budget, keyword, ad, landing, product-group, or scale/pause recommendation.
- Keep final success tied to profitable sales and about `650% ROAS`; do not treat clicks, CTR, or ad strength as the final win condition.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `ops/marketing/daily_scorecard.md`
- `ops/marketing/AGENTS.md`

Safest next sales-moving action:

- Fresh read-only monitor for today/yesterday metrics plus keyword quality/ad/landing diagnostics, then prepare a T+72 serving-diagnosis packet if GB/CA/AU remain zero-impression.

## 2026-05-14 - Bounded proactive spend authority activation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Owner authorized spending within the set limits as long as actions respect the sales/ROAS goals.
- `spend_authorization.md` now says `APPROVED_ACTIVE` with `$80/day` total paid-media cap and `$5/day` new/test campaign cap.
- Agent rules now require proactive monitoring and green-gated bounded action when quality gates pass.
- Excluded surfaces remain excluded: billing, conversion goals, PMax, unresolved remarketing, Merchant feed/source/product-scope changes, Shopify product/price/discount/policy/theme publish, unreviewed native-language ads, and actions above caps.

Risks:

- Active authority can be misused if agents skip quality checks or treat diagnostic metrics as final success.
- Current GB/CA/AU and Shopping data still do not justify an immediate bid/budget/status write without fresh readback and quality diagnostics.
- Paid-media spend authority does not automatically approve live Shopify theme sanitizer sync or Merchant/Pinterest catalog/source writes.

Required gates/fixes:

- Use authority only for green-gated rows in `action_queue.md`.
- Before any live action, save before-state readback, check bid strategy, keyword/search-term quality, Quality Score or missing quality columns, ad/RSA quality, product/photo fit, landing page, measurement, blockers, and path to profitable sales at about `650% ROAS`.
- Save after-state readback and update command-layer files.

Evidence:

- Owner message in current session.
- `ops/marketing/spend_authorization.md`
- `ops/marketing/action_queue.md`
- `ops/marketing/AGENTS.md`

Safest next sales-moving action:

- Fresh read-only monitor today/yesterday metrics and quality diagnostics, then execute only green-gated bounded actions if gates pass; otherwise document the exact blocker or diagnosis packet.

## 2026-05-14 - Keyword discipline and continuous improvement ownership

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Campaign Explorer now records keyword selection criteria, negative-keyword criteria, daily optimization owner, and continuous improvement loop.
- GB/CA/AU exact keywords are labeled as a controlled starter hypothesis, not guaranteed-smart final keywords.
- Negative watchlist is labeled `watch_only_not_uploaded`; actual negative uploads require search-term evidence.
- Agents now have explicit responsibility for daily monitoring, action triggers, and dashboard continuity.

Risks:

- Without fresh search-term and quality readbacks, keyword quality cannot be proven today.
- Bounded authority should not turn watchlist terms into negatives without evidence.

Required gates/fixes:

- Daily Google Ads monitor must include keyword/search-term quality, Quality Score or missing quality-column readback, ad/RSA quality, landing/product/photo fit, conversion value, CPA, and ROAS.
- Expand, pause, or negative-match only from daily data and green-gated reviewer-cleared decisions.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `gb_ca_au_negative_watchlist.csv`
- `GB_CA_AU_1700_ZERO_DATA_DECISION_UPDATE.md`
- `GB_CA_AU_1721_ZERO_DATA_DECISION_UPDATE.md`

Safest next sales-moving action:

- Run the daily read-only Google Ads monitor and record whether the current keywords are producing impressions, qualified search terms, clicks, conversions, and progress toward `650% ROAS`.

## 2026-05-14 - 2026 expert playbook, personas, and anti-cannibalization

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local strategy/dashboard/agent updates only; no platform surfaces or live account writes.
- `expert_growth_playbook_2026.md` cites Google Ads Help, Pinterest Business, OpenAI, and Anthropic sources for match types, search-term evidence, negatives, Target ROAS readiness, Quality Score, landing/ad quality, creative/clickthrough fit, and agent guardrails.
- Campaign Explorer now exposes expert source standard, keyword economics/low-waste test, and anti-cannibalization rules.
- Agent personas now require senior specialist ownership instead of passive audit behavior.

Risks:

- Source-backed strategy still needs fresh live campaign/account data before any actual optimization.
- Broad/automated strategies are not rejected forever, but they remain gated until purchase value, landing quality, and search-term evidence justify them.

Required gates/fixes:

- Before any live recommendation, run the reviewer checklist, save fresh readbacks, and prove high-intent/low-waste economics, no self-cannibalization, and path to about `650% ROAS`.
- Do not treat this playbook as live-write approval.

Evidence:

- `ops/marketing/expert_growth_playbook_2026.md`
- `ops/marketing/campaign_explorer.json`
- `ops/marketing/reviewer_checklist.md`
- `.codex/agents/*.toml`

Safest next sales-moving action:

- Run the fresh daily Google Ads/Shopping read-only monitor and use the playbook rubric to decide whether GB/CA/AU need serving diagnosis, keyword expansion, negatives, bid review, landing repair, or continued hold.

## 2026-05-14 - Day 1 growth urgency and 24-hour zero-impression rule

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local command-layer and agent instruction updates only; no platform surfaces or live account writes.
- Owner directive that each day without growing sales is a failure signal and that zero impressions after one day requires action.
- Current saved GB/CA/AU evidence already shows T+24 zero-impression state, so the command layer now treats same-day diagnosis and long-tail/auction-entry planning as due.

Risks:

- Aggressive growth language could be misread as permission to skip approval, quality, measurement, or live-readback gates.
- Long-tail candidates still require evidence, landing fit, no self-cannibalization, and reviewer pass before live upload or bid/status action.

Required gates/fixes:

- Tomorrow's scorecard must report sales, revenue, CPA, ROAS, progress, and exact next action.
- Any live keyword, bid, budget, ad, status, or campaign change must remain inside `APPROVED_ACTIVE` caps or fresh exact approval and pass reviewer gates.

Evidence:

- Owner message in current session.
- `ops/marketing/expert_growth_playbook_2026.md`
- `ops/marketing/action_queue.md`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Run the Day 1 sales/ROAS monitor and GB/CA/AU zero-impression diagnosis, then build high-buyer-intent long-tail candidates with exact anti-cannibalization ownership and landing fit.

## 2026-05-14 - GB/CA/AU Day 1 keyword strategy repair

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local/read-only keyword strategy repair for active GB/CA/AU exact Search campaigns.
- Official Google Ads docs for Target ROAS math/traffic limits, low-search-volume behavior, exact/phrase/broad match controls, Quality Score components, and ad/landing relevance.
- Market/language candidate maps for GB English-UK, CA English-Canada with French-Canada gated separately, and AU English-Australia.
- No live keyword, ad, negative, bid, budget, status, campaign, feed, product, conversion, or theme write.

Risks:

- Latest Ads metrics are saved `2026-05-14 05:34 EDT` readbacks for reporting day `2026-05-13`; a fresh live monitor is still needed before any live action.
- CA/AU search-term pages remain non-actionable while the stale `Keyword: "human hair wigs"` filter is present.
- Active paid landing expansion still depends on approved live sanitizer sync/readback.

Required gates/fixes:

- Fresh before-state Google Ads readback with CA/AU filters clear, Quality Score/RSA/final URL checks, and current metrics.
- Reviewer pass for any exact keyword/ad/bid/status action.
- Live paid landing supplier/source sanitizer readback before traffic expansion.
- After-state readback and command-layer logging for any future live action.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/GB_CA_AU_DAY1_ZERO_IMPRESSION_KEYWORD_STRATEGY_REPAIR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/gb_ca_au_high_intent_candidate_map.csv`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Run the fresh read-only GB/CA/AU monitor and, only if gates pass, prepare an exact-scope bounded action packet for market-language long-tail exact/phrase rows or auction-entry changes.

## 2026-05-14 - Fresh GB/CA/AU Ads monitor and landing gate

Reviewer verdict: `BLOCK`

Checked:

- Fresh read-only Google Ads CDP/RPC/UI monitor for GB, CA, and AU.
- Search-term filter-chip removal only; no Ads entity mutation.
- Quality Score/Exp. CTR/ad relevance/landing page experience columns present in keyword UI.
- RSA/ad status and final URLs through read-only RPC and UI captures.
- Public GB/CA/AU landing source sanitizer readback.

Risks:

- All active final URLs still expose `detail.1688.com` in `data-analytics-vendor`, which violates paid-landing and supplier/source guardrails.
- The active exact keywords are `Eligible (Limited)` because `$0.15` max CPC is below first-page estimates around `$0.65-$0.74`; raising bids into generic head terms would be risky without a clean landing and conversion-value proof.
- Search terms are filter-clean now but still empty/no terms, so no negative action is justified.

Required gates/fixes:

- Scoped live theme sanitizer sync/readback must pass on GB/CA/AU final URLs before any keyword, bid, status, or traffic expansion.
- Rerun fresh Ads monitor and reviewer gate after landing is live-clean.
- Keep the exact-scope action packet `BLOCKED_DO_NOT_UPLOAD_OR_APPLY` until gates pass.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/FRESH_GB_CA_AU_ADS_MONITOR_AND_GATE_REVIEW.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Safest next sales-moving action:

- Get approval for scoped live theme sanitizer sync/readback, then rerun the GB/CA/AU monitor and only then decide whether the blocked long-tail exact packet can become a bounded live action.

## 2026-05-14 - $0.15 CPC long-tail packet correction

Reviewer verdict: `BLOCK_WITH_CORRECTION`

Checked:

- Owner hard CPC correction: clicks above `$0.15` are not acceptable for the current active Search repair.
- Fresh keyword UI readback showing active head terms below first page at `$0.65-$0.74`.
- Blocked packet rows that still proposed close head variants.
- Repo-local packet/doc correction only; no Ads or Shopify external write.

Risks:

- Close head variants can look localized while still entering the same expensive auction.
- Product-specific long tails may have low search volume; they still require read-only planner/keyword UI validation before upload.
- Live landing supplier/source URL leak still blocks traffic expansion.

Required gates/fixes:

- No bid above `$0.15`.
- No upload of `[mummy and me dresses]`, `[mommy and me dresses canada]`, `[mummy and me dresses australia]`, or other close-head variants as "long tail."
- Candidate rows must be market-specific, buyer-moment/product-specific, landing-fit, and validated at `$0.15` before live action.
- Live sanitizer readback must pass before any traffic expansion.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/CPC_015_LONG_TAIL_CORRECTION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Safest next sales-moving action:

- Sync/read back the live landing sanitizer after explicit approval, then validate only the corrected long-tail candidates at `$0.15` before any bounded upload.

## 2026-05-14 - Expert keyword factory criteria

Reviewer verdict: `PASS_LOCAL`

Checked:

- Repo-local criteria file only; no platform or live account write.
- Hard `$0.15` CPC cap and `650% ROAS` math.
- Large local universe plus small validated live batch rule.
- Fix-now rule for mistakes found during execution.

Risks:

- A big local universe still needs actual Keyword Planner/keyword UI validation before live use.
- A clean keyword list cannot overcome the live landing supplier/source leak by itself.

Required gates/fixes:

- Live uploads require clean landing readback, `$0.15` CPC validation, reviewer pass, exact row scope, and after-state readback.
- For unapproved live writes, produce the exact smallest approval packet instead of stopping at a passive blocker.

Evidence:

- `ops/marketing/keyword_factory_015_cpc_criteria.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Safest next sales-moving action:

- After landing sanitizer approval/sync, build the large local keyword universe and validate the highest-scoring exact rows at `$0.15` before upload.

## 2026-05-14 - US primary keyword correction

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner correction that US is the biggest market.
- Current command layer: US live lane is Standard Shopping; GB/CA/AU are active Search keyword repair lanes.
- Repo-local criteria/doc updates only.

Risks:

- Operators may mistake non-US Search urgency for overall market priority.
- Shopping does not accept manual keywords, so US keyword work must feed title/feed/query/product diagnostics and future Search/Pinterest packets.

Required gates/fixes:

- Keep US first in keyword universe generation.
- Do not mutate Shopping feed/product groups/titles/bids/status without approval.
- Do not upload US Search rows without `$0.15` validation, clean landing, reviewer pass, and after-state readback plan.

Evidence:

- `ops/marketing/us_primary_keyword_lane.md`
- `ops/marketing/keyword_factory_015_cpc_criteria.md`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Build the US-first local keyword universe and use it to diagnose Standard Shopping query/product/title fit, while keeping live writes gated.

## 2026-05-14 - Proactive action/results mandate

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner directive that results and actions matter more than monitor loops.
- Repo-local durable operating-doc updates only.
- No live account or production write.

Risks:

- Action language could be misread as permission to skip approval gates.
- Monitoring still matters when it produces a decision or proves no action is currently valid.

Required gates/fixes:

- Fix immediately when local/read-only or current approval covers the action.
- For unapproved live writes, prepare the exact smallest approval packet and keep other safe work moving.
- Every monitor/readback must end in a concrete result category, not vague observation.

Evidence:

- `AGENTS.md`
- `ops/marketing/AGENTS.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Safest next sales-moving action:

- Use the next live/read-only finding to either fix now, execute an approved bounded action, or produce the exact approval packet.

## 2026-05-14 - Action-biased keyword universe and scoring rubric

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner requested the expert model: large local keyword universe, small validated live batches.
- New files are local docs/data only: `keyword_strategy.md`, `keyword_scoring_rubric.md`, and `keyword_universe.csv`.
- No live Google Ads, Shopify, Merchant, Pinterest, GA4/GTM, billing, bid, budget, status, keyword, ad, feed, product, conversion, or theme write occurred.
- CSV validation passed: `105` rows, `60` US, `15` GB, `15` CA, `15` AU; scores sum correctly and thresholds match the rubric.

Risks:

- Future operators could mistake `GREEN` for upload-ready instead of validation-ready.
- Landing and CPC gates still block GB/CA/AU live expansion.

Required gates/fixes:

- Before live use: active-product fit, clean landing route, `$0.15` CPC validation, anti-cannibalization owner, reviewer pass, exact `action_queue.md` row, and after-state readback plan.
- `YELLOW` rows stay local unless used as a bounded phrase-discovery repair; `RED` rows are not paid-Search upload candidates.

Evidence:

- `ops/marketing/keyword_strategy.md`
- `ops/marketing/keyword_scoring_rubric.md`
- `ops/marketing/keyword_universe.csv`
- `ops/marketing/spend_authorization.md`

Safest next sales-moving action:

- Validate top US `GREEN` rows against Standard Shopping queries/product titles and validate GB/CA/AU `GREEN` rows only after the paid landing sanitizer is live-clean.

## 2026-05-14 - Command-layer integration guard

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner identified side documents without follow-up as a critical process failure.
- Added `ops/scripts/audit_marketing_command_integration.py`.
- Generated `ops/marketing/command_layer_integration_audit.md`.
- Initial audit found `4` risks; current rerun reports `25` tracked files and `0` side-document risks.

Risks:

- The guard only covers files under `ops/marketing/`; audit packets and broader `ops/` history remain evidence stores and still need normal tracker/worklog discipline.

Required gates/fixes:

- Any new `ops/marketing/` artifact must be registered, action-linked, continuity-logged, or marked generated/archive.
- Future closeouts must run the audit when command-layer files are created or materially changed.

Evidence:

- `ops/scripts/audit_marketing_command_integration.py`
- `ops/marketing/command_layer_integration_audit.md`
- `ops/marketing/AGENTS.md`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Keep using `action_queue.md`, `current_marketing_state.md`, and `operator_cockpit.md` as the execution surfaces; do not let new strategy docs bypass them.
