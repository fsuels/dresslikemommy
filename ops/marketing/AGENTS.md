# Marketing Command Layer Guide

Scope: `ops/marketing/` is the compact daily execution layer for Dress Like Mommy paid growth. Historical detail stays in the worklog, problem tracker, coordination registry, and evidence packets.

## Source Of Truth

- Control: `current_marketing_state.md`, `action_queue.md`, `spend_authorization.md`, `daily_scorecard.md`, `blocker_board.md`.
- Memory/review: `decision_log.md`, `assumption_log.md`, `review_log.md`, `reviewer_checklist.md`, `prompt_log.md`, `memory_digest.md`.
- UI/team: `operator_cockpit.md`, generated `operator_cockpit.html`, `campaign_explorer.json`, `team_registry.md`.
- Strategy: `expert_growth_playbook_2026.md`, `keyword_factory_015_cpc_criteria.md`, `keyword_strategy.md`, `keyword_scoring_rubric.md`, `keyword_universe.csv`, `us_primary_keyword_lane.md`.
- Loops: `self-improvement-pilot-loop.md` / `score_paid_growth_handoff.py`; `weekly-dream-review-loop.md` / `generate_weekly_dream_review.py`.
- Guards/reference: generated `command_layer_integration_audit.md`, `audit_marketing_command_integration.py`, `check_continuity_integrity.py`, `dream_consolidation_prompt.md`; `migration_trace.md` is `ARCHIVE_REFERENCE`.

`decision_log.md` is forward-only and outcome-linked. `current_marketing_state.md`'s marked control supersedes all older readiness/approval text for present action.

## Required First Loop

1. For the canonical `/goal Continue ... latest AGENT_CONTINUITY_ANCHOR`, first run `python3.13 ops/scripts/open_marketing_cockpit.py`.
2. Read root `AGENTS.md` and this guide. Read `current_marketing_state.md`'s `Authoritative Execution Control` first. If it says `STALE_READBACK_REQUIRED`, the only valid execution step is read-only reconciliation.
3. Resolve the latest relevant anchor. Search worklog, tracker, and coordination by exact task IDs; use `compile_task_context.py` when needed. Never substitute an unrelated global-latest anchor.
4. Retrieve the matching decision and observed outcome in `decision_log.md`, then the current queue/blocker row. Historical predictions or copied packets are context, not current proof.
5. Then read only task-specific control, strategy, continuity, protocol, prompt, and evidence files.
6. Before live execution, run exact-surface read-only reconciliation for enabled, eligible, serving, spending, converting, ROAS, search terms, feed/catalog health, access, and blockers. Update all owning records from the same evidence window.

## Decision And Action Loop

- Optimize for profitable sales at about `650% ROAS`: purchases, revenue/value, CPA, and ROAS. Treat impressions, clicks, CTR, CPC, ad strength, and quality scores as diagnostics.
- Monitoring must end in `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- Fix safe local/read-only defects now. For unapproved live work, prepare the smallest exact approval packet and continue another safe lane.
- Apply `expert_growth_playbook_2026.md`; intent, landing fit, economics, measurement, and anti-cannibalization outrank cheap traffic.
- Zero impressions after 24 hours triggers same-day serving/auction diagnosis and `5-20` tightly related high-intent exact/phrase long-tail candidates, not broad match or blind bid escalation.
- Build a large local keyword universe, but promote only small `GREEN` batches after current search-term/CPC, active-product, landing, native-language, reviewer, authority, and after-state gates.
- Give each material decision a stable `decision_id`; freeze baseline/options/prediction/success/kill/window/authority, then append a linked outcome record when it matures. Never rewrite the prediction.
- Keep blockers aligned with `ops/PROBLEM_TRACKER.md`; finish with a worklog anchor and the closest sales-moving action.

## Authority And Safety Gate

Run the read-only safety reviewer/checklist before non-ops edits, external writes, blocker reclassification, or live-risk recommendations. Log meaningful verdicts. Material actions need an independent verifier.

`APPROVED_ACTIVE` is necessary but not sufficient. Bounded standing authority exists only when:

1. `spend_authorization.md` says `APPROVED_ACTIVE`.
2. Authoritative control is unexpired `LIVE_CURRENT` with `autonomous_action_ready=true`.
3. The exact `approved_external_scope` value appears backticked in a `GREEN` action-queue row.
4. Fresh evidence, quality, review, coordination, before-state, after-state, and rollback gates pass.

Otherwise no live action is authorized. Fresh approval always remains required for billing, conversion goals, PMax, remarketing, Merchant source/product scope, Shopify customer-visible data, unreviewed native ads, or spend above caps.

Before clicking Save, Apply, Publish, Upload, Enable, Pause, Remove, Delete, Sync, or Submit, confirm the active claim, exact authority/approval, before-state, after-state plan, and smallest rollback. Stop on login, CAPTCHA, account switch, billing, permission, policy, schema drift, or unexpected destructive prompts. Complete the account-access recovery ladder before calling access blocked.

Never treat historical `APPROVED_ACTIVE`, `LIVE_VERIFIED`, `GREEN`, readiness, or packet approval as current authority. Tool access and reasoning do not broaden scope.

## Multi-Agent And Handoff

Parent owns authority, writes, frame, integration, and report. Operators use disjoint surfaces/tabs; blocked lanes trigger rerouting.

Before stopping, update `operator_cockpit.md` and regenerate `operator_cockpit.html`. Show:

- one owner-facing next action/approval and why it goes first;
- `Next 3 Tasks` as the separate prioritized internal queue;
- local/live changes, blockers, current metrics/readback gaps, assumptions, evidence, risks, approvals, active objects, strategy, ownership, success/kill triggers, and next decision time.

Use only `ops/prompts/paid-growth-ai-army-continuation-prompt.md` for continuation. Packet prompts point to it and add the relevant anchor, blockers, gate, and one action; they do not become competing prompts.

## Integration And Closeout

A new command-layer artifact counts only if it is registered here, linked from an action surface, continuity-logged, or explicitly marked `ARCHIVE_REFERENCE`/`GENERATED`. After material command-layer work run:

```bash
python3.13 ops/scripts/render_marketing_cockpit.py
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
python3.13 ops/scripts/check_continuity_integrity.py --strict
```

Do not create another `AI_Team/` state system, rewrite historical evidence, allow audits to become the outcome, or leave a safe obvious fix as commentary.
