# Problem Solving Protocol

Purpose: make every known problem visible, owned, actively worked, and closed only by evidence.

This protocol applies whenever an agent finds a real issue, failed readback, stale platform diagnostic, broken workflow, policy/account blocker, regression, or repeated uncertainty.

## Core Rule

A problem is not a note. It is a live work item until it is fixed, disproven, superseded by a safer solution, or blocked by an explicit owner/credential/destructive-action gate with the next concrete unblock action named.

Do not write "blocked" and stop. When a blocker appears:

1. Try the safest direct fix inside current approval.
2. Try or rule out at least one alternate grounded path.
3. If live action requires approval or credentials, build the approval packet, exact prompt, checklist, or credential request needed to unblock it.
4. Move another independent lane forward while the gate is waiting.
5. Keep updating the tracker until the problem reaches a terminal status with proof.

## Required Tracker

Use `ops/PROBLEM_TRACKER.md` as the active problem ledger.

Every problem entry must include:

- Problem ID.
- Priority: `P0`, `P1`, `P2`, or `P3`.
- Status.
- Owner/session.
- Surface.
- Exact symptom.
- Business impact.
- Definition of fixed.
- Attempt log with timestamp, action, result, and evidence.
- Failed or ruled-out paths.
- Current next action.
- Approval/credential/platform gates.
- Parallel work that should continue while this problem is gated.

## Statuses

- `ACTIVE_SOLVING`: Work is ongoing now.
- `ACTIVE_VERIFYING`: A fix was applied and readbacks are being collected.
- `OWNER_APPROVAL_REQUIRED`: Exact approval is needed for the next live action; the approval wording/checklist must be documented.
- `CREDENTIALS_REQUIRED`: Existing credentials/scopes are insufficient; the exact credential/scope needed must be documented.
- `PLATFORM_REFRESH_PENDING`: A live fix was applied, but the platform has a documented propagation delay; schedule/readback action must be documented.
- `SOLVED_READBACK_PASSED`: Fixed and confirmed with evidence.
- `FALSE_POSITIVE_OR_WRONG_SURFACE`: Proved not to require the originally implied fix; the correct interpretation/action must be documented.
- `SUPERSEDED_BY_SAFER_PATH`: The original path was replaced by a safer concrete solution; the safer path must be linked.
- `REGRESSED_REOPENED`: Previously solved, now failing again; link old and new evidence.

Avoid `BLOCKED` as a final status. If a gate exists, use one of the gated statuses above and include the next unblock action.

## Priority

- `P0`: Revenue, spend, trust, policy, checkout, tracking, account access, or customer-visible breakage that can cause immediate loss or harm.
- `P1`: Important growth/catalog/feed/listing problem that blocks launch, scale, or measurement.
- `P2`: Workflow/tooling problem that slows execution but has a workaround.
- `P3`: Cleanup, documentation, or optimization issue.

## Definition Of Fixed

Every problem needs a concrete closing test. Examples:

- Merchant issue count is `0` in a fresh export, or the exact issue is absent from the affected sample/details page.
- Campaign/ad/feed setting readback matches the intended state.
- Public storefront/browser QA passes on named URLs and viewports.
- API/readback confirms the object no longer has the failure state.
- If the issue was a wrong-surface diagnostic, the relevant feature/add-on/destination is disabled and the diagnostic no longer appears.

Close only after evidence is saved and linked.

## Attempt Log Rules

Each attempt must answer:

- What was tried?
- Why was it a reasonable path?
- What happened?
- What evidence proves the result?
- What changed because of what was learned?

Do not repeat a failed path unless new evidence makes it materially different.

## Multi-Agent Handling

For complex or parallel work, the parent/orchestrator owns the problem entry and final status. Subagents may own attempt rows or disjoint solution lanes, but they must report:

- Files/surfaces touched.
- Evidence path.
- Readback result.
- Next recommended attempt.

The parent must update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md` when shared/external surfaces are touched, and `ops/AGENT_WORKLOG.md` at the end of the session.

## When Approval Or Credentials Are Needed

If the next fix requires owner approval, credentials, or a destructive/live-spend action:

- Document the exact needed approval or credential/scope.
- Build the safest preflight/readback checklist.
- Prepare the local/paused/import-preview packet when possible.
- Keep non-dependent work moving.
- Resume the problem immediately once the gate clears.

## End Condition

A problem is done only when one of these is true:

- `SOLVED_READBACK_PASSED`.
- `FALSE_POSITIVE_OR_WRONG_SURFACE` with proof and any wrong surface disabled/ignored safely.
- `SUPERSEDED_BY_SAFER_PATH` with the safer path completed or actively tracked.

Anything else stays visible in `ops/PROBLEM_TRACKER.md`.
