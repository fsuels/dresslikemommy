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
- `expert_growth_playbook_2026.md`: source-backed paid-growth strategy, keyword economics, anti-cannibalization rules, channel standards, and agent personas.
- `assumption_log.md`: important assumptions that affect marketing decisions, especially stale or gated facts.
- `reviewer_checklist.md`: safety checklist for risky decisions and recommendations.
- `review_log.md`: concise record of reviewer outcomes or simulated checklist runs.
- `dream_consolidation_prompt.md`: periodic consolidation prompt to keep this command layer sharp.

## Required First Loop

1. If the session starts from the owner prompt `/goal Continue the Dress Like Mommy paid-growth command layer from the latest AGENT_CONTINUITY_ANCHOR`, immediately run `python3.13 ops/scripts/open_marketing_cockpit.py` so the human cockpit opens in the browser.
2. Read root `AGENTS.md`, this file, `operator_cockpit.md`, `expert_growth_playbook_2026.md`, `current_marketing_state.md`, `spend_authorization.md`, `action_queue.md`, `daily_scorecard.md`, `blocker_board.md`, `assumption_log.md`, `reviewer_checklist.md`, and `team_registry.md`.
3. Read `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/PROBLEM_SOLVING_PROTOCOL.md`, `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the canonical paid-growth prompt.
4. Reconcile repo-known state against the latest worklog and problem tracker before acting.
5. For live marketing execution, run read-only live reconciliation first: enabled, eligible, serving, spending, converting, ROAS, search terms, catalog/feed health, Pinterest access, and blockers.
6. Update the command-layer files after any material readback, decision, gate change, or owner approval.

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
- Starting 2026-05-14, treat every day without sales growth, usable learning, or a sales-moving improvement as a failure signal that requires a same-day next action. Tomorrow's check must answer sales, revenue, CPA, ROAS, and what changed.
- When `spend_authorization.md` says `APPROVED_ACTIVE`, Head of Growth and assigned operators are responsible for proactive monitoring and green-gated bounded actions inside the approved caps. Do not wait for the owner when the action is clearly inside authority, quality gates pass, evidence is fresh, and the row is green.
- Do not use bounded authority as a shortcut around quality: check bid strategy, keywords/search terms, Quality Score or quality-column gaps, ad/RSA quality, photos/product fit, landing page, measurement, blockers, and sales/ROAS path before live action.
- Keyword ownership is continuous. Operators must explain why keywords were selected, whether data proves they are smart, what expansions are justified, and what negatives are evidence-supported. A watchlist is not an upload list.
- Apply `expert_growth_playbook_2026.md` before keyword, negative, bid, budget, campaign, creative, landing, or channel recommendations. High-intent and low-waste beats cheap-but-unqualified traffic; do not cannibalize query intent across campaigns, ad groups, countries, languages, Search, Shopping, Pinterest, or remarketing.
- Zero impressions after 24 hours is a same-day action trigger: diagnose serving/auction entry and evaluate high-buyer-intent long-tail exact/phrase alternatives instead of waiting passively.
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

## Non-Negotiables

- Do not turn stale repo evidence into a current live decision.
- Do not create a competing `AI_Team/` state system.
- Do not let audits become the deliverable. The deliverable is a sales-moving decision, build, fix, approval packet, or blocker removal.
- Do not update this command layer without also updating the detailed repo memory when required by `ops/MEMORY_CONTINUITY_PROTOCOL.md`.
