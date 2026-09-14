# Dream Consolidation Prompt

Use this periodically after substantial paid-growth work to keep the command layer from becoming another archive.

For the local report generator and safety loop, use `docs/agent-loops/weekly-dream-review-loop.md` and:

```bash
python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md
```

The generated packet is local advisory evidence only. It cannot change canonical prompts, command-layer rules, Shopify, ads, feeds, campaigns, billing, or product data without the normal review and approval gates.

Authority notice: follow `ops/marketing/AGENTS.md` `Required First Loop` instead of the historical file list below. The generator's source precedence and deduplicated outcome-event rules govern; copied policy or prompt text is never recurrence evidence.

```text
Consolidate the Dress Like Mommy paid-growth command layer.

Retrieve context through `ops/marketing/AGENTS.md` `Required First Loop`. Read current authority first, then deduplicated relevant worklog events, linked decision outcomes, current status, and only the supporting context needed for the review.

Task:
- Remove stale duplication from ops/marketing files.
- Preserve only current command decisions, active blockers, and exact next actions.
- Keep detailed historical evidence in worklog, problem tracker, and packets.
- Mark every platform fact as either fresh-readback-current or repo-known-stale.
- Ensure spend_authorization.md says PENDING_OWNER_APPROVAL unless the owner explicitly approved bounded authority.
- Ensure action_queue.md has a clear next sales-moving action.
- Count a routine recurring lesson only after two independent observed-outcome events. Repeated copies of one event do not count.
- Promote at most one durable rule per review; otherwise record NO_CHANGE.

Do not:
- Make external account writes.
- Create competing prompts or a second state tree.
- Rewrite historical evidence.

Done when:
- ops/marketing is compact enough for a new agent to start executing within minutes.
- Every active blocker maps to a tracker entry or exact approval gate.
- The next /goal is ready.
```
