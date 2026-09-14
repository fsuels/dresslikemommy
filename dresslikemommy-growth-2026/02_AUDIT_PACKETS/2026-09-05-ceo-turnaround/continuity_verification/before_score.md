# Paid-Growth Handoff Scorecard

Integration status: `GENERATED`

Purpose: local-only scorecard for paid-growth continuation handoffs. It does not perform external writes.

## Summary

- Files checked: `1`
- Files passing: `0`
- Files failing: `1`

## Results

### `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/LOCAL_VERIFICATION_AND_HANDOFF.md`

- Score: `8/17`
- Passed: `false`

| Criterion | Pass | Detail |
|---|---:|---|
| `latest_anchor_named` | `false` | missing AGENT_CONTINUITY_ANCHOR |
| `one_next_action` | `false` | found 0 next-action label(s) |
| `canonical_prompt_reused` | `true` | mentions ops/prompts/paid-growth-ai-army-continuation-prompt.md |
| `approval_boundary_preserved` | `false` | missing approval language or blocked live-surface reminder |
| `sales_moving_outcome` | `true` | handoff names an action, approval packet, repair, reroute, or evidence-backed hold |
| `blocker_or_gate_named` | `true` | names a blocker/gate/approval and a next step |
| `not_monitor_only` | `true` | monitoring is tied to action |
| `no_source_or_supplier_url` | `true` | no non-Dress-Like-Mommy URL-like source found |
| `no_physical_inventory_claim` | `true` | no positive physical-store, warehouse, local-pickup, or on-hand-stock claim |
| `authoritative_execution_context` | `false` | missing or placeholder: source_live_evidence_as_of, approved_external_scope; source_live_evidence_as_of must be YYYY-MM-DD |
| `uncertainty_outcome_branches` | `true` | names decision-changing evidence and distinct actions for both outcomes |
| `independent_material_decision_verifier` | `true` | names a verifier who did not build or execute the material action |
| `semantically_relevant_anchor` | `false` | handoff must name exactly the unique task-relevant compiled anchor |
| `authority_matches_current_control` | `false` | compiled context is fail-closed |
| `next_action_matches_current_control` | `false` | next_best_action must occur once and match current control |
| `evidence_grade_matches_current_control` | `false` | evidence_grade must be a canonical label matching current control |
| `task_stage_matches_retrieved_anchor` | `false` | task_stage must occur once, be non-UNKNOWN, and match the retrieved anchor |
