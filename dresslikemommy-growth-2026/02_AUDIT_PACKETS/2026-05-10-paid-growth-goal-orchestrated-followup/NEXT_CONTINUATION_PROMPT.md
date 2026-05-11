# Next Continuation Prompt Pointer

Use the canonical owner-standard prompt from:

`ops/prompts/paid-growth-ai-army-continuation-prompt.md`

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-goal-orchestrated-followup`

## Add This State When Resuming

- The fresh local/read-only packet is `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/`.
- Current Ads state is `12 built / 3 absent / 2 parked`.
- Built/read back clean and still paused: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, and `CZ`.
- Absent: `RO`, `PT`, and `GR`.
- Parked: `FR` and `BE`.
- Do not use `2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/` as current Ads state; it is stale and predates `IT`, `PL`, and `CZ` completion plus the later `RO` stale/not-visible readback.
- Before any non-US live enablement, close `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`.
- Next Ads action needs fresh owner direction: retry `RO` with a new one-country preview after no-in-progress/no-campaign readback, or skip/park `RO` and continue `PT`, then `GR` one country at a time.

## Owner-Standard Prompt

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it, not just summarize it.

Act as the parent/orchestrator. Use parallel subagents wherever supported, with disjoint workstreams and separate browser/account tabs when needed.

Follow the problem-solving protocol and update `ops/PROBLEM_TRACKER.md` for every active problem, failed readback, blocker, attempt, result, approval gate, and solved status. Do not document known problems passively. Work the solution until fixed, disproven, superseded by a safer path, or gated with the exact next unblock action.

Guardrails: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, and no Shopify live product-data changes unless I give fresh explicit action-time approval.

Start now. Inspect, plan, split the work, execute safe read-only/local/paused-build work, verify, update evidence packets, update `ops/PROBLEM_TRACKER.md`, update `ops/AGENT_WORKLOG.md` with a new `AGENT_CONTINUITY_ANCHOR`, and finish with the next continuation prompt.
```
