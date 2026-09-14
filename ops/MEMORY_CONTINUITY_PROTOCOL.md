# Memory Continuity Protocol

Purpose: prevent future agents from forgetting completed work, duplicating fixes, or wasting time re-solving problems that already have evidence and handoff notes.

This protocol applies to every session.

## Files And Roles

- `AGENTS.md`: automatic bootstrap instructions. Store durable rules, guardrails, North Star and pointers; changing business state belongs in its canonical record.
- `ops/AGENT_WORKLOG.md`: chronological session log. Store every completed/deferred workstream, evidence packet, commands, readbacks, blockers, and `AGENT_CONTINUITY_ANCHOR`.
- `ops/AGENT_COORDINATION.md`: active and completed coordination registry. Store write claims, locks, blocked actions, and handoff status for shared/external surfaces.
- `ops/PROBLEM_SOLVING_PROTOCOL.md`: required workflow for turning a discovered problem into attempts, learning, solution, readback, and closure.
- `ops/PROBLEM_TRACKER.md`: active problem ledger. Store problem status, priority, owner, exact symptom, fixed criteria, attempt log, failed paths, gates, and next action.
- `ops/GOOGLE_ADS_CONTINUITY.md`: durable paid-media memory for Google Ads, Merchant Center, conversion tracking, and paid-launch state.
- `ops/marketing/`: compact paid-growth execution command layer. Store current repo-known/live-readback-needed marketing state, action queue, spend authority, scorecard, blocker board, decision log, prompt log, memory digest, and team registry here. Keep detailed historical evidence in the worklog, problem tracker, coordination file, and audit packets.
- `ops/BROWSER_SUBAGENT_COORDINATION.md`: how multiple agents use logged-in Atlas/in-app browser tabs without conflict.
- `ops/GROWTH_NORTH_STAR.md`: the promise-land goal and definition of done for paid growth.
- `ops/prompts/*.md`: reusable continuation prompts and operator workflows.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`: evidence packets, screenshots, downloads, reports, and readback summaries.

## Start-Of-Session Checklist

Use `AGENTS.md` for project routing. For paid growth, follow `ops/marketing/AGENTS.md` `Required First Loop`; it is the sole detailed retrieval sequence and begins with authoritative current control.

For every task:

1. Search the worklog, problem tracker, and coordination registry by exact campaign, product/cohort, feed/source, market, theme, pixel/tag, file, error, problem, or decision identifier.
2. Select the latest relevant anchor rather than the latest unrelated global anchor. Use `ops/scripts/compile_task_context.py` when semantic continuity matters.
3. Retrieve the matching decision and observed outcome before acting. A copied mention or historical prediction is not a new outcome.
4. Read only the owning workflow and narrowly relevant evidence unless targeted retrieval cannot resolve the task.
5. Before shared or external work, confirm the current coordination claim, authority, and approval boundary.

### Plain-language continuation in a new task

Open the new Codex task in this saved project using the same local checkout to read the current shared files. A separate worktree has its own snapshot; it does not automatically contain the latest uncommitted work or checkpoints. Separate conversations do not automatically share their complete chat history.

For a bare channel request such as "continue Google Ads", "continue Google Merchant", "continue Shopify" or "continue Google Analytics", run:

```bash
python3 ops/scripts/compile_task_context.py --query "continue Google Ads" --format brief
```

If a suitable Python interpreter is unavailable, use the configured bundled Python runtime located through the workspace-dependencies tool; missing PATH entries are not a continuity failure. This command is read-only unless an output file is explicitly requested.

Read the derived session brief and its cited canonical source lines. Explain the goal, already-completed work, current owner, remaining dependency and next action before proceeding. Broad Shopify requests may cover products, themes, feeds and tracking: show that inventory and resolve the workstream before choosing a write. A successful retrieval is not approval, a live account readback, or proof that a previous conversation completed all of its work.

The brief is built on demand from the existing command layer, worklog and coordination records; it is not a second state store. Omit `--format brief` to obtain the complete machine-readable JSON, optionally with `--output` to a local temporary file. Read conflicting source records and preserve the restrictive gate until the conflict is resolved. Use the detailed exact-entity path for a particular campaign/product/error. Do not substitute a global-latest anchor for missing relevant evidence.

If another task owns the requested workstream, retain its claim and offer independent read-only/local work or continuation in that existing task. Parallel tasks need disjoint ownership even when each has a separate browser. Checkpoint completed milestones, evidence and next steps in the owning canonical task record and worklog before handoff; unsaved reasoning in a chat is not recoverable project memory. Do not record tokens, cookies, passwords or personal browser content.

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

For every new anchor, also add compact retrieval metadata:

- `task_entities`: comma-separated stable product, campaign, feed, market, problem, error, file, or decision IDs; omit loose topic words.
- `task_stage`: one of `DIAGNOSE`, `BUILD`, `VERIFY`, `HANDOFF`, or `BLOCKED`.
- `next_action_id`: the canonical action ID when one exists. For paid growth it must not contradict `current_marketing_state.md`'s authoritative `next_best_action`.

Legacy anchors without these fields remain historical evidence; do not guess missing metadata. Use `ops/scripts/compile_task_context.py` to fail closed on missing, ambiguous, or contradictory task context.

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
- A durable routing rule changes; changing external state stays in the owning command record and worklog.
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
8. Run `python3.13 ops/scripts/check_continuity_integrity.py --strict` after any continuity, paid-growth command-layer, prompt, cockpit, spend-authority, worklog, or handoff change, and fix canonical files if it fails.
9. For paid-growth work, provide the single canonical owner-standard continuation prompt from `ops/prompts/paid-growth-ai-army-continuation-prompt.md`; do not create competing bespoke prompts. For non-paid-growth work, provide a continuation prompt when the work is part of a longer sprint.

The continuation handoff must include:

- Latest `AGENT_CONTINUITY_ANCHOR`.
- What is already done and should not be repeated.
- What remains blocked and why.
- The exact next approval gate, if needed.
- Which subagents should run next and which tabs/surfaces they own.
- The closest next path to the North Star.

Paid-growth special rule:

- The prompt text itself should remain the owner-standard reusable prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
- Packet `NEXT_CONTINUATION_PROMPT.md` files may exist as pointers, but they must not become alternate operating prompts.
- Future agents should recover the latest state by reading the canonical prompt, `AGENTS.md`, the bottom of `ops/AGENT_WORKLOG.md`, `ops/PROBLEM_TRACKER.md`, and `ops/AGENT_COORDINATION.md`.
- If a packet, digest, memory, or sidecar file names a stale latest anchor, the canonical worklog and command layer supersede it.

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
