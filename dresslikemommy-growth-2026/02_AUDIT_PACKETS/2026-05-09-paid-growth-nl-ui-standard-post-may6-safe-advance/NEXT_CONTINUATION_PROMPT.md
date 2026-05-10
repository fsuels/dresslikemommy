# Next Continuation Pointer

Use the canonical owner-standard prompt below. Do not create a competing prompt.

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-09-paid-growth-nl-ui-standard-post-may6-safe-advance`

Already done; do not redo blindly:

- NL checkout UI selected-country confirmation is solved for paused infrastructure only.
- Standard Shopping post-May-6 metrics readback is solved read-only.
- Held `1496`-row non-US Search CSV revalidated as clean/local-only/paused/approval-gated.

Still gated:

- Paused non-US Google Search preview/import requires the exact `TEST BUILD` approval gate.
- Merchant US/es age_group source `10627981690` repair requires exact approval.
- Pinterest US paused drafts/Event Quality repair requires exact approval.
- Beach/Vacation Family Shopify SEO/social metadata repair requires exact approval, or keep using the held Ads CSV that excludes that URL/theme.
- Any Standard Shopping status/budget/bid/product-group/product-scope/feed-label/conversion-goal change requires fresh exact approval.

Next best action:

Request the paused non-US Google Search `TEST BUILD` approval if the owner wants the fastest next controlled infrastructure step; then preview/read back before and after, keeping all entities paused and all live spend blocked.

## Owner-Standard Prompt

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it, not just summarize it.

Act as the parent/orchestrator. Use parallel subagents wherever supported, with disjoint workstreams and separate browser/account tabs when needed.

Follow the problem-solving protocol and update `ops/PROBLEM_TRACKER.md` for every active problem, failed readback, blocker, attempt, result, approval gate, and solved status. Do not document known problems passively. Work the solution until fixed, disproven, superseded by a safer path, or gated with the exact next unblock action.

Guardrails: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, and no Shopify live product-data changes unless I give fresh explicit action-time approval.

Start now. Inspect, plan, split the work, execute safe read-only/local/paused-build work, verify, update evidence packets, update `ops/PROBLEM_TRACKER.md`, update `ops/AGENT_WORKLOG.md` with a new `AGENT_CONTINUITY_ANCHOR`, and finish with the next continuation prompt.
```
