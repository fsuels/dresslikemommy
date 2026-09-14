# Paid-Growth Handoff Scorecard

Integration status: `GENERATED`

Purpose: local-only scorecard for paid-growth continuation handoffs. It does not perform external writes.

## Summary

- Files checked: `3`
- Files passing: `3`
- Files failing: `0`

## Results

### `ops/tests/fixtures/paid_growth_handoff_capability/validation_stale_marketing_candidate.md`

- Score: `12/12`
- Passed: `true`

| Criterion | Pass | Detail |
|---|---:|---|
| `latest_anchor_named` | `true` | names an AGENT_CONTINUITY_ANCHOR |
| `one_next_action` | `true` | found 1 next-action label(s) |
| `canonical_prompt_reused` | `true` | mentions ops/prompts/paid-growth-ai-army-continuation-prompt.md |
| `approval_boundary_preserved` | `true` | approval language and blocked live surfaces are present |
| `sales_moving_outcome` | `true` | handoff names an action, approval packet, repair, reroute, or evidence-backed hold |
| `blocker_or_gate_named` | `true` | names a blocker/gate/approval and a next step |
| `not_monitor_only` | `true` | monitoring is tied to action |
| `no_source_or_supplier_url` | `true` | no non-Dress-Like-Mommy URL-like source found |
| `no_physical_inventory_claim` | `true` | no positive physical-store, warehouse, local-pickup, or on-hand-stock claim |
| `authoritative_execution_context` | `true` | names evidence date, execution mode, effective authority, and approved external scope |
| `uncertainty_outcome_branches` | `true` | names decision-changing evidence and distinct actions for both outcomes |
| `independent_material_decision_verifier` | `true` | names a verifier who did not build or execute the material action |

### `ops/tests/fixtures/paid_growth_handoff_capability/validation_material_rule_candidate.md`

- Score: `12/12`
- Passed: `true`

| Criterion | Pass | Detail |
|---|---:|---|
| `latest_anchor_named` | `true` | names an AGENT_CONTINUITY_ANCHOR |
| `one_next_action` | `true` | found 1 next-action label(s) |
| `canonical_prompt_reused` | `true` | mentions ops/prompts/paid-growth-ai-army-continuation-prompt.md |
| `approval_boundary_preserved` | `true` | approval language and blocked live surfaces are present |
| `sales_moving_outcome` | `true` | handoff names an action, approval packet, repair, reroute, or evidence-backed hold |
| `blocker_or_gate_named` | `true` | names a blocker/gate/approval and a next step |
| `not_monitor_only` | `true` | monitoring is tied to action |
| `no_source_or_supplier_url` | `true` | no non-Dress-Like-Mommy URL-like source found |
| `no_physical_inventory_claim` | `true` | no positive physical-store, warehouse, local-pickup, or on-hand-stock claim |
| `authoritative_execution_context` | `true` | authority context is explicitly NOT_APPLICABLE |
| `uncertainty_outcome_branches` | `true` | names decision-changing evidence and distinct actions for both outcomes |
| `independent_material_decision_verifier` | `true` | names a verifier who did not build or execute the material action |

### `ops/tests/fixtures/paid_growth_handoff_capability/holdout_routine_local.md`

- Score: `12/12`
- Passed: `true`

| Criterion | Pass | Detail |
|---|---:|---|
| `latest_anchor_named` | `true` | names an AGENT_CONTINUITY_ANCHOR |
| `one_next_action` | `true` | found 1 next-action label(s) |
| `canonical_prompt_reused` | `true` | mentions ops/prompts/paid-growth-ai-army-continuation-prompt.md |
| `approval_boundary_preserved` | `true` | approval language and blocked live surfaces are present |
| `sales_moving_outcome` | `true` | handoff names an action, approval packet, repair, reroute, or evidence-backed hold |
| `blocker_or_gate_named` | `true` | names a blocker/gate/approval and a next step |
| `not_monitor_only` | `true` | monitoring is tied to action |
| `no_source_or_supplier_url` | `true` | no non-Dress-Like-Mommy URL-like source found |
| `no_physical_inventory_claim` | `true` | no positive physical-store, warehouse, local-pickup, or on-hand-stock claim |
| `authoritative_execution_context` | `true` | authority context is explicitly NOT_APPLICABLE |
| `uncertainty_outcome_branches` | `true` | decision explicitly does not depend on uncertain state |
| `independent_material_decision_verifier` | `true` | decision is explicitly NOT_MATERIAL |
