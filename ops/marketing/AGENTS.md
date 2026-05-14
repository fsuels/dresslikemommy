# Marketing Command Layer Guide

Scope: `ops/marketing/` is the daily execution command layer for Dress Like Mommy paid growth. It does not replace historical evidence in `ops/`, `ops/AGENT_WORKLOG.md`, `ops/PROBLEM_TRACKER.md`, or audit packets.

## Source Of Truth

- `current_marketing_state.md`: compact repo-known paid-growth state and live-readback-needed unknowns.
- `action_queue.md`: green/yellow/red execution queue for the next marketing actions.
- `spend_authorization.md`: standing/bounded spend policy. If it says `PENDING_OWNER_APPROVAL`, it is not authority.
- `daily_scorecard.md`: current daily operating scoreboard and required live readbacks.
- `blocker_board.md`: compact blocker view that must map back to `ops/PROBLEM_TRACKER.md`.
- `decision_log.md`: marketing decisions made from evidence.
- `prompt_log.md`: canonical prompts and goal handoffs.
- `memory_digest.md`: compressed handoff facts for future agents.
- `team_registry.md`: Codex custom agents, owner lanes, and write boundaries.
- `operator_cockpit.md`: human-readable current dashboard source; update before stopping, compacting, or handing off.
- `operator_cockpit.html`: one-screen human UI generated from the command layer; regenerate with `python3.13 ops/scripts/render_marketing_cockpit.py`.
- `campaign_explorer.json`: human-facing campaign detail data for the dashboard; keep active/running status, targeting, ad/creative quality, strategy, evidence, and next checks current.
- `command_layer_integration_audit.md`: generated side-document guard report; regenerate with `python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk`.
- `ops/scripts/check_continuity_integrity.py`: strict broad continuity guard for canonical worklog presence, alternate-worklog quarantine, latest-anchor resolution, spend-authority agreement, cockpit freshness, and marketing integration audit pass.
- `expert_growth_playbook_2026.md`: source-backed paid-growth strategy, keyword economics, anti-cannibalization rules, channel standards, and agent personas.
- `keyword_factory_015_cpc_criteria.md`: `$0.15` CPC keyword factory criteria and hard promotion gates.
- `keyword_strategy.md`: action-biased keyword operating model: build a large local universe, promote only small validated batches, and force action after no-impression or low-serveability evidence.
- `keyword_scoring_rubric.md`: `0-100` scoring system for buyer intent, product match, occasion/deadline, landing match, economics, serveability, and waste risk.
- `keyword_universe.csv`: local keyword universe. It is not a live upload file; rows must be validated and promoted through `action_queue.md`.
- `us_primary_keyword_lane.md`: US-first keyword-intelligence lane for Shopping query/title/product-fit diagnosis and future Search/Pinterest packets.
- `assumption_log.md`: important assumptions that affect marketing decisions, especially stale or gated facts.
- `reviewer_checklist.md`: safety checklist for risky decisions and recommendations.
- `review_log.md`: concise record of reviewer outcomes or simulated checklist runs.
- `dream_consolidation_prompt.md`: periodic consolidation prompt to keep this command layer sharp.
- `migration_trace.md`: historical compaction trace. Integration status is `ARCHIVE_REFERENCE`; do not use it as current execution state.

## Required First Loop

1. If the session starts from the owner prompt `/goal Continue the Dress Like Mommy paid-growth command layer from the latest AGENT_CONTINUITY_ANCHOR`, immediately run `python3.13 ops/scripts/open_marketing_cockpit.py` so the human cockpit opens in the browser.
2. Read root `AGENTS.md`, this file, `operator_cockpit.md`, `expert_growth_playbook_2026.md`, `current_marketing_state.md`, `spend_authorization.md`, `action_queue.md`, `daily_scorecard.md`, `blocker_board.md`, `assumption_log.md`, `reviewer_checklist.md`, and `team_registry.md`.
3. Read `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/PROBLEM_SOLVING_PROTOCOL.md`, `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the canonical paid-growth prompt.
4. Reconcile repo-known state against the latest worklog and problem tracker before acting.
5. For account access, read `ops/ACCOUNT_ACCESS_PROTOCOL.md` and complete its recovery ladder before marking Google Ads, Merchant Center, GA4/GTM, Search Console, Shopify Admin, Pinterest, GitHub, or business email as blocked. A fresh login page in one new tab is not enough evidence.
6. For live marketing execution, run read-only live reconciliation first: enabled, eligible, serving, spending, converting, ROAS, search terms, catalog/feed health, Pinterest access, and blockers.
7. Update the command-layer files after any material readback, decision, gate change, or owner approval.

## Command-Layer Integration Gate

No new `ops/marketing/` artifact counts as done if it is merely created. It must be wired into the operating loop.

Before stopping after creating or materially changing any `ops/marketing/` file:

1. Register the file in this `Source Of Truth` list, unless it is clearly generated or an archive reference.
2. Link it from at least one action surface: `action_queue.md`, `current_marketing_state.md`, `daily_scorecard.md`, `blocker_board.md`, `operator_cockpit.md`, or `ops/PROBLEM_TRACKER.md`.
3. Log the change in continuity: `ops/AGENT_WORKLOG.md` plus the relevant `decision_log.md`, `review_log.md`, `assumption_log.md`, `memory_digest.md`, or `ops/AGENT_COORDINATION.md`.
4. If the file is not meant to drive action, mark it explicitly as `Integration status: ARCHIVE_REFERENCE` or `Integration status: GENERATED`.
5. Run:

```bash
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
python3.13 ops/scripts/check_continuity_integrity.py --strict
```

If either audit reports a risk, fix the canonical wiring before calling the work complete. A strategy document without action ownership, current-state visibility, and follow-up is a defect.

## Safety Review Gate

Run or simulate `.codex/agents/marketing_safety_reviewer.toml` and `reviewer_checklist.md` before:

- Any non-ops file edit.
- Any external write.
- Any blocker reclassification.
- Any spend, budget, bid, status, feed, product, or conversion recommendation.

The reviewer is read-only by default. It must not edit files, operate external accounts, or click any Save/Apply/Upload/Publish/Enable/Pause/Sync/Submit control. The parent or active operator owns implementation after the review passes.

Record meaningful reviews in `review_log.md`, especially `PASS_WITH_GATES` or `BLOCK` outcomes.

## Daily Decision Loop

- Pull current live metrics/readbacks before making decisions.
- Judge success by profitable sales: purchase count, revenue/conversion value, CPA, and ROAS against the North Star of as many profitable sales as possible at about `650% ROAS`. Impressions, clicks, CTR, CPC, ad strength, and quality score are diagnostic signals, not the final win condition.
- Results/action mandate: if an operator sees a mistake, broken state, underperforming campaign, mismatched landing, weak keyword set, supplier leak, feed/catalog blocker, bad product fit, or obvious improvement, the operator must act. Fix it immediately when local/read-only or covered by current approval; if it needs unapproved live writes, produce the smallest exact approval packet and move another safe lane forward.
- Monitor loops are not an outcome. Every monitor/readback must end with one of: `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- Starting 2026-05-14, treat every day without sales growth, usable learning, or a sales-moving improvement as a failure signal that requires a same-day next action. Tomorrow's check must answer sales, revenue, CPA, ROAS, and what changed.
- When `spend_authorization.md` says `APPROVED_ACTIVE`, Head of Growth and assigned operators are responsible for proactive monitoring and green-gated bounded actions inside the approved caps. Do not wait for the owner when the action is clearly inside authority, quality gates pass, evidence is fresh, and the row is green.
- Do not use bounded authority as a shortcut around quality: check bid strategy, keywords/search terms, Quality Score or quality-column gaps, ad/RSA quality, photos/product fit, landing page, measurement, blockers, and sales/ROAS path before live action.
- Keyword ownership is continuous. Operators must explain why keywords were selected, whether data proves they are smart, what expansions are justified, and what negatives are evidence-supported. A watchlist is not an upload list.
- Keyword universe rule: build the keyword universe as large as possible locally, but never upload the whole universe live. Score candidates with `keyword_scoring_rubric.md`; promote only small `GREEN` batches from `keyword_universe.csv` after fresh readback, landing proof, `$0.15` CPC validation, reviewer pass, exact row scope, and after-state plan.
- Market-language rule: US is the primary market and must not be omitted. Adapt language by market before any keyword packet: US `mom/mommy/family photos/family pictures/vacation`, GB `mum/mummy/holiday/pyjamas`, CA English `mom/mommy/family pictures/Canada`, AU `mum/mummy/holiday/beach/pyjamas`. Keep French-Canada separate until native review.
- Apply `expert_growth_playbook_2026.md` before keyword, negative, bid, budget, campaign, creative, landing, or channel recommendations. High-intent and low-waste beats cheap-but-unqualified traffic; do not cannibalize query intent across campaigns, ad groups, countries, languages, Search, Shopping, Pinterest, or remarketing.
- Zero impressions after 24 hours is a same-day action trigger: diagnose serving/auction entry and evaluate high-buyer-intent long-tail exact/phrase alternatives instead of waiting passively.
- If an active keyword lane is eligible but too narrow or low-search-volume, prepare or execute a green-gated repair using `5-20` closely related exact/phrase long-tail rows. Do not repair no-impression campaigns by bidding up expensive obvious terms or jumping straight to broad match.
- Every live Search session must end with one of: serving repair, negative keyword action, keyword expansion, hold/kill/scale decision, or exact blocker/unblock action. A session cannot call "monitoring" progress unless `daily_scorecard.md` has spend, impressions, clicks, purchases, revenue, ROAS, and next decision updated.
- Agents must operate from their expert persona in `team_registry.md`: senior specialist judgment, source-backed strategy, current evidence, clear decision clocks, and proactive improvement toward `650% ROAS`.
- Decide for each active lane: `scale`, `hold`, `pause/reduce`, `fix blocker`, `build paused`, or `needs owner approval`.
- Make only evidence-backed low-risk changes covered by current approval.
- Record every decision in `decision_log.md` and every queue movement in `action_queue.md`.
- Keep `blocker_board.md` aligned with `ops/PROBLEM_TRACKER.md`; the tracker remains the detailed problem ledger.
- End with `ops/AGENT_WORKLOG.md` anchor and the next closest sales-moving action.

## Human Handoff Requirements

Before stopping, compacting, or handing off, update `operator_cockpit.md` and regenerate `operator_cockpit.html` so a human can see:

- What was checked.
- What changed locally.
- What changed live.
- What remains blocked.
- Next 3 tasks.
- Assumptions and evidence.
- Risks and approvals needed.
- For active Google Ads or Pinterest lanes: what is running, when it became active, today/yesterday metrics or explicit fresh-readback gap, exact active objects, bid strategy and why it was chosen, keyword selection criteria, negative-keyword criteria, daily optimization owner, continuous-improvement loop, keywords/targeting, ad/creative quality, quality score or missing quality-score readback, landing-page/photo/product fit, success measurement against sales/ROAS/CPA, strategy/reasoning, assumptions being tested, improvement/pause/scale triggers, deadline/next decision, and evidence.
- For keyword or targeting decisions: high-intent/low-waste criteria, anti-cannibalization owner, current query/search-term evidence, negative-keyword evidence, and source-backed strategy standard.
- For keyword universe decisions: local universe size, how many `GREEN` rows exist by market, which rows are blocked by landing/CPC/native review, and the next exact live-promotion gate.

Record important assumptions in `assumption_log.md` as soon as they affect a decision, not after they become confusing.

Rendering command:

```bash
python3.13 ops/scripts/render_marketing_cockpit.py
```

Render and open command:

```bash
python3.13 ops/scripts/open_marketing_cockpit.py
```

## Spend And Write Boundaries

- The default state is no live spend authority unless `spend_authorization.md` says `APPROVED_ACTIVE`.
- `spend_authorization.md` must explicitly say `APPROVED_ACTIVE` before bounded standing authority can be used.
- Even with bounded authority, fresh approval is still required for billing, conversion goals, PMax, unresolved remarketing, Merchant feed/source/product-scope changes, Shopify product/price/discount/policy changes, unreviewed native-language ads, or spend above caps.
- Head of Growth may only enable or change green-gated rows in `action_queue.md` when the authority file says the action is approved.
- When authority is active, Head of Growth owns proactive follow-through: monitor daily, diagnose zero-learning tests by deadline, execute safe bounded improvements when quality gates pass, and log before/after readbacks.
- Pausing/reducing clear waste and adding exact negatives require search-term/spend evidence and must be logged before and after.

## Agent Rules

- Use project-scoped Codex agents in `.codex/agents/` for execution lanes when subagents are explicitly requested or the active prompt authorizes parallel paid-growth work.
- Parent/head-of-growth owns approvals, live writes, final integration, and the final report.
- Operators own disjoint surfaces only. No operator may mutate another operator's lane.
- One browser/account tab per surface. Stop on login, CAPTCHA, billing, account switch, policy, approval, or unsaved-change prompts.
- Account access failures must use the recovery labels in `ops/ACCOUNT_ACCESS_PROTOCOL.md`; do not reopen a P0 access blocker until existing tabs/sessions, connectors/local secure credential sources, direct account navigation, and current-session credentials have been checked without persisting secrets.

## Non-Negotiables

- Do not turn stale repo evidence into a current live decision.
- Do not create a competing `AI_Team/` state system.
- Do not let audits become the deliverable. The deliverable is a sales-moving decision, build, fix, approval packet, or blocker removal.
- Do not leave an obvious fix or improvement as commentary. If it can be done safely now, do it and verify; if it cannot, write the exact action-time approval packet and continue another sales-moving lane.
- Do not update this command layer without also updating the detailed repo memory when required by `ops/MEMORY_CONTINUITY_PROTOCOL.md`.
