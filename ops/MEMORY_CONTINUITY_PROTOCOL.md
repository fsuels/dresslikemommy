# Memory Continuity Protocol

Purpose: prevent future agents from forgetting completed work, duplicating fixes, or wasting time re-solving problems that already have evidence and handoff notes.

This protocol applies to every session.

## Files And Roles

- `AGENTS.md`: automatic bootstrap memory. Store durable, high-level rules, current critical state, persistent guardrails, North Star, and pointers to deeper files.
- `ops/AGENT_WORKLOG.md`: chronological session log. Store every completed/deferred workstream, evidence packet, commands, readbacks, blockers, and `AGENT_CONTINUITY_ANCHOR`.
- `ops/AGENT_COORDINATION.md`: active and completed coordination registry. Store write claims, locks, blocked actions, and handoff status for shared/external surfaces.
- `ops/PROBLEM_SOLVING_PROTOCOL.md`: required workflow for turning a discovered problem into attempts, learning, solution, readback, and closure.
- `ops/PROBLEM_TRACKER.md`: active problem ledger. Store problem status, priority, owner, exact symptom, fixed criteria, attempt log, failed paths, gates, and next action.
- `ops/GOOGLE_ADS_CONTINUITY.md`: durable paid-media memory for Google Ads, Merchant Center, conversion tracking, and paid-launch state.
- `ops/BROWSER_SUBAGENT_COORDINATION.md`: how multiple agents use logged-in Atlas/in-app browser tabs without conflict.
- `ops/GROWTH_NORTH_STAR.md`: the promise-land goal and definition of done for paid growth.
- `ops/prompts/*.md`: reusable continuation prompts and operator workflows.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`: evidence packets, screenshots, downloads, reports, and readback summaries.

## Start-Of-Session Checklist

Every session must:

1. Read `AGENTS.md`.
2. Read `ops/PROBLEM_SOLVING_PROTOCOL.md` and `ops/PROBLEM_TRACKER.md` when the task involves any known issue, failed readback, blocker, diagnostic, regression, or repeated uncertainty.
3. Read the latest entries at the bottom of `ops/AGENT_WORKLOG.md`.
4. Read `ops/AGENT_COORDINATION.md` before touching external systems or shared surfaces.
5. For paid-media work, read `ops/GOOGLE_ADS_CONTINUITY.md`.
6. For multi-agent/browser work, read `ops/BROWSER_SUBAGENT_COORDINATION.md`.
7. For growth strategy, read `ops/GROWTH_NORTH_STAR.md`.
8. Search for relevant prior anchors/surfaces before fixing:
   - campaign name or ID
   - product/cohort ID
   - Merchant source/feed ID
   - theme ID
   - pixel/tag name
   - file path
   - exact issue text

## Before Fixing Anything

Before attempting a fix, the agent must answer:

- Was this already fixed or attempted?
- Is this already tracked in `ops/PROBLEM_TRACKER.md`?
- What evidence proved it was fixed?
- Did a later readback show it regressed or did not clear?
- Is the current task a new blocker, a verification, or a duplicate request?
- Does the work require owner approval or a coordination write claim?

If a fix appears already completed, do not redo it blindly. First do a readback or targeted verification. If readback passes, report it as already fixed and move to the next blocker.

If a problem is not already tracked, create an `ops/PROBLEM_TRACKER.md` entry before or during the first repair attempt. Do not wait until the end of the session to make the problem visible.

## What Must Be Written To Memory

Every session that changes code, theme files, Shopify data, ads, feeds, pixels, campaigns, prompts, scripts, or durable strategy must update `ops/AGENT_WORKLOG.md` with:

- Date and short title.
- `AGENT_CONTINUITY_ANCHOR`.
- Why the work happened.
- What changed.
- What was verified.
- Evidence packet path.
- Guardrails preserved.
- Remaining blockers.
- Next best action.

Update `ops/AGENT_COORDINATION.md` when:

- A write claim starts.
- A write claim finishes.
- A surface is blocked.
- Ownership transfers.
- A completed workstream changes status after a recheck.

Update `ops/PROBLEM_TRACKER.md` when:

- A real issue, failed readback, stale diagnostic, regression, or repeated blocker is discovered.
- A repair attempt starts or finishes.
- An attempted path fails or is ruled out.
- A problem becomes gated by approval, credentials, or platform refresh.
- A problem is solved, disproven, superseded, or reopened.
- The next concrete action changes.

Update `AGENTS.md` when the new state is durable bootstrap memory, such as:

- A major workflow or protocol is created.
- A persistent guardrail changes.
- A critical external-system state changes.
- A repeated blocker or "do not redo this" instruction must be visible to every future agent.
- The North Star, continuation rule, or subagent orchestration model changes.

Do not put noisy one-off details in `AGENTS.md`; put those in `ops/AGENT_WORKLOG.md` and evidence packets, then link or summarize only durable conclusions in `AGENTS.md`.

## End-Of-Session Checklist

Before final response, every agent must:

1. Confirm no needed command/session is still running.
2. Run the narrowest relevant verification.
3. Review diff for accidental scope creep.
4. Update `ops/AGENT_WORKLOG.md`.
5. Update `ops/PROBLEM_TRACKER.md` for any problem touched, including attempts, failed paths, current status, evidence, and next action.
6. Update `ops/AGENT_COORDINATION.md` if a shared/external surface was claimed or rechecked.
7. Update `AGENTS.md` only if durable bootstrap memory changed.
8. Provide a continuation prompt when the work is part of a longer sprint.

The continuation prompt must include:

- Latest `AGENT_CONTINUITY_ANCHOR`.
- What is already done and should not be repeated.
- What remains blocked and why.
- The exact next approval gate, if needed.
- Which subagents should run next and which tabs/surfaces they own.
- The closest next path to the North Star.

## Duplicate-Fix Prevention Rule

If the next agent sees a task like "fix X" and `X` appears in `AGENTS.md`, `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, or `ops/AGENT_COORDINATION.md` as already done:

1. Verify current state with a targeted readback.
2. If still fixed, do not reapply the fix.
3. If not fixed, document the regression and repair only the regressed part.
4. Link the prior anchor and the new anchor in the worklog.

## Required Final Response Shape

Final responses for work sessions must include:

- `Confidence: H|M|L`
- What changed.
- Files touched.
- Commands/tools run.
- Results/readbacks.
- Problem tracker updates, when any issue/blocker was involved.
- Residual risks.
- Next best action.
- Continuation prompt if the sprint continues.
