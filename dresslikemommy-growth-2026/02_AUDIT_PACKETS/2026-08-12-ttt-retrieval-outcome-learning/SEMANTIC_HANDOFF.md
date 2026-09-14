# TTT Semantic Handoff

AGENT_CONTINUITY_ANCHOR: 2026-08-12-ttt-retrieval-outcome-learning-prompt-compaction

Canonical prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`

## Retrieved Context

- `control_as_of`: `2026-07-23`
- `source_live_evidence_as_of`: `2026-06-01`
- `live_state_mode`: `STALE_READBACK_REQUIRED`
- `live_readback_fresh_until`: `EXPIRED`
- `autonomous_action_ready`: `false`
- `effective_approval_policy`: `FRESH_ACTION_TIME_APPROVAL_REQUIRED`
- `approved_external_scope`: `NONE`
- `supersedes_execution_readiness_below`: `true`
- `next_best_action`: `READ_ONLY_MARKETING_RECONCILIATION`
- `evidence_grade`: `LIVE_READBACK_REQUIRED`
- `task_stage`: `HANDOFF`

## Decision Discipline

- `decision_depends_on_uncertain_state`: `true`
- `decision_changing_evidence`: A fresh same-window read-only reconciliation of paid sales, revenue, spend, CPA, ROAS, serving status, feed/catalog health, and measurement blockers.
- `if_evidence_supports_recommendation`: Update the existing command-layer files from the same evidence window, then choose one bounded sales-moving action only if the refreshed authority gates allow it.
- `if_evidence_opposes_recommendation`: Preserve fail-closed authority, record the contradiction, and prepare the smallest exact unblock or approval packet without a live write.
- `material_decision`: `MATERIAL`
- `independent_verifier`: `marketing_safety_reviewer`
- `verifier_independence`: `DID_NOT_BUILD_OR_EXECUTE`

## What Changed

The local TTT adaptation fixed task-relevant retrieval, outcome-only weekly recurrence, semantic handoff consistency, forward-only decision/outcome memory, and prompt bloat while preserving the existing command layer and frozen legacy scorer contract.

## Gate And Boundaries

The next gate is a fresh read-only reconciliation. Fresh explicit action-time approval is still required where the refreshed authority demands it. Until then: no live spend, no campaign enablement, no budget/bid/status changes, no product-scope changes, no feed-label changes, no conversion-goal changes, no Merchant upload, no Shopify live product-data write, and do not publish.

Recommended next action: Run `READ_ONLY_MARKETING_RECONCILIATION` across the existing paid-growth truth surfaces, then update only the owning command-layer files from the same evidence window. It goes first because current state is intentionally stale and no safe paid-growth decision can rely on historical readiness.

