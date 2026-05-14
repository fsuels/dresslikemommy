# Marketing Command Layer Migration Trace

Last seeded: 2026-05-14

Purpose: make the root `AGENTS.md` compaction auditable. Critical operational memory was either kept in the short root bootstrap or moved/preserved in the named continuity files below.

| Critical content | Destination after compaction | Notes |
|---|---|---|
| External-write approval boundaries | Root `AGENTS.md`; `ops/marketing/AGENTS.md`; `ops/marketing/spend_authorization.md`; `ops/AGENT_COORDINATION.md` | Root keeps the hard no-write boundary; spend authority remains `PENDING_OWNER_APPROVAL`. |
| Paid-growth North Star | Root `AGENTS.md`; `ops/GROWTH_NORTH_STAR.md`; `ops/marketing/current_marketing_state.md`; canonical paid-growth prompt | Root points to the North Star and command layer; detailed goal remains in existing continuity files. |
| Dropshipping/no physical inventory claims | Root `AGENTS.md`; `ops/GROWTH_NORTH_STAR.md`; `ops/prompts/paid-growth-ai-army-continuation-prompt.md` | Root now explicitly preserves the no-store/no-owned-inventory claim boundary. |
| No PMax / no Merchant / no conversion-goal / no Shopify product-data changes without approval | Root `AGENTS.md`; `ops/marketing/spend_authorization.md`; `ops/GOOGLE_ADS_CONTINUITY.md`; `ops/AGENT_COORDINATION.md` | Specific campaign/feed details remain in Google Ads continuity and command state. |
| Standard Shopping guardrails | Root `AGENTS.md`; `ops/GOOGLE_ADS_CONTINUITY.md`; `ops/marketing/current_marketing_state.md`; `ops/marketing/action_queue.md` | Root keeps no-change guardrail; state file marks current live state as readback-required. |
| Pinterest access blocker | `ops/marketing/current_marketing_state.md`; `ops/marketing/blocker_board.md`; `ops/PROBLEM_TRACKER.md` | Command layer marks current live state as readback/access-required, not live-true. |
| GB/CA/AU repo-known state | `ops/marketing/current_marketing_state.md`; `ops/marketing/daily_scorecard.md`; `ops/marketing/action_queue.md`; worklog | State file separates `REPO_KNOWN` from `LIVE_READBACK_REQUIRED`. |
| Problem tracker discipline | Root `AGENTS.md`; `ops/MEMORY_CONTINUITY_PROTOCOL.md`; `ops/PROBLEM_SOLVING_PROTOCOL.md`; `ops/PROBLEM_TRACKER.md` | No detailed tracker history was moved out of the tracker. |
| Coordination locks | Root `AGENTS.md`; `ops/AGENT_COORDINATION.md`; `ops/BROWSER_SUBAGENT_COORDINATION.md`; `ops/marketing/team_registry.md` | Root keeps one-writer rule and points to detailed coordination files. |
| Shopify credential safety | Root `AGENTS.md`; prior credential paths preserved there; existing continuity files | Credentials remain outside repo/worklog/theme files. |
| Canonical prompt policy | Root `AGENTS.md`; `ops/prompts/paid-growth-ai-army-continuation-prompt.md`; `ops/marketing/prompt_log.md` | Root preserves single canonical prompt policy. |

## Size Evidence

- Old root `AGENTS.md` size is available from `git show HEAD:AGENTS.md | wc -c` before this diff is committed.
- New root `AGENTS.md` size is available from `wc -c AGENTS.md`.

## Validation Additions

- `grep -R "PENDING_OWNER_APPROVAL" ops/marketing/spend_authorization.md` must show bounded authority is not active.
- `ops/marketing/current_marketing_state.md` must use `REPO_KNOWN`, `LIVE_READBACK_REQUIRED`, `LIVE_VERIFIED`, and `STALE_OR_SUPERSEDED`.
