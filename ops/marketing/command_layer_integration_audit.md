# Marketing Command Layer Integration Audit

Integration status: `GENERATED`

Last generated: 2026-05-14 11:45

Purpose: identify command-layer files that risk becoming side documents nobody uses.

## Summary

- Tracked files: `25`
- Integrated/generated/archive files: `25`
- Side-document risks: `0`

A side-document risk means a file is missing from the source registry, has too few command-loop references, or is not connected to an action surface.

## Required Rule

No new `ops/marketing/` artifact counts as done unless it is either:

- registered in `ops/marketing/AGENTS.md`,
- linked from an action surface such as `action_queue.md`, `current_marketing_state.md`, `daily_scorecard.md`, `blocker_board.md`, `operator_cockpit.md`, or `ops/PROBLEM_TRACKER.md`,
- logged in continuity files such as `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, `decision_log.md`, `review_log.md`, `assumption_log.md`, or `memory_digest.md`,
- or explicitly marked as `Integration status: ARCHIVE_REFERENCE` or `Integration status: GENERATED`.

## File Results

| File | Status | Registered | Ref count | Action surface | Fix |
|---|---|---:|---:|---:|---|
| `ops/marketing/AGENTS.md` | `PASS_CORE` | `true` | `11` | `true` | none |
| `ops/marketing/action_queue.md` | `PASS_CORE` | `true` | `6` | `true` | none |
| `ops/marketing/assumption_log.md` | `PASS_CORE` | `true` | `3` | `false` | none |
| `ops/marketing/blocker_board.md` | `PASS_CORE` | `true` | `5` | `true` | none |
| `ops/marketing/campaign_explorer.json` | `PASS_CORE` | `true` | `10` | `true` | none |
| `ops/marketing/command_layer_integration_audit.md` | `PASS_GENERATED` | `true` | `9` | `true` | generated integration audit |
| `ops/marketing/current_marketing_state.md` | `PASS_CORE` | `true` | `9` | `true` | none |
| `ops/marketing/daily_scorecard.md` | `PASS_CORE` | `true` | `5` | `true` | none |
| `ops/marketing/decision_log.md` | `PASS_CORE` | `true` | `3` | `false` | none |
| `ops/marketing/dream_consolidation_prompt.md` | `PASS_INTEGRATED` | `true` | `4` | `true` | none |
| `ops/marketing/expert_growth_playbook_2026.md` | `PASS_INTEGRATED` | `true` | `14` | `true` | none |
| `ops/marketing/keyword_factory_015_cpc_criteria.md` | `PASS_INTEGRATED` | `true` | `11` | `true` | none |
| `ops/marketing/keyword_scoring_rubric.md` | `PASS_INTEGRATED` | `true` | `14` | `true` | none |
| `ops/marketing/keyword_strategy.md` | `PASS_INTEGRATED` | `true` | `13` | `true` | none |
| `ops/marketing/keyword_universe.csv` | `PASS_INTEGRATED` | `true` | `14` | `true` | none |
| `ops/marketing/memory_digest.md` | `PASS_CORE` | `true` | `2` | `false` | none |
| `ops/marketing/migration_trace.md` | `PASS_ARCHIVE_REFERENCE` | `true` | `4` | `true` | none |
| `ops/marketing/operator_cockpit.html` | `PASS_GENERATED` | `true` | `9` | `true` | generated cockpit |
| `ops/marketing/operator_cockpit.md` | `PASS_CORE` | `true` | `5` | `true` | none |
| `ops/marketing/prompt_log.md` | `PASS_CORE` | `true` | `2` | `false` | none |
| `ops/marketing/review_log.md` | `PASS_CORE` | `true` | `3` | `false` | none |
| `ops/marketing/reviewer_checklist.md` | `PASS_CORE` | `true` | `4` | `false` | none |
| `ops/marketing/spend_authorization.md` | `PASS_CORE` | `true` | `12` | `true` | none |
| `ops/marketing/team_registry.md` | `PASS_CORE` | `true` | `3` | `false` | none |
| `ops/marketing/us_primary_keyword_lane.md` | `PASS_INTEGRATED` | `true` | `11` | `true` | none |

## Risks To Fix

- None.

## Command

```bash
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
```
