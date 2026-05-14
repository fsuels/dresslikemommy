# Marketing Safety Review Log

Last updated: 2026-05-14

Use this log for reviewer outcomes or simulated checklist runs. Keep entries short and tied to evidence.

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
