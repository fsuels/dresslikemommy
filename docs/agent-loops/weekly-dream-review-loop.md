# Weekly Dream Review Loop

Purpose: turn recent agent sessions into a local review packet that helps future agents avoid repeated mistakes, without giving the review authority to change live systems.

Use this loop after substantial paid-growth, listing, localization, feed, or prompt/handoff work when the repo has enough recent evidence to learn from.

Do not use this loop for Shopify Admin writes, ads changes, feed/source changes, product changes, campaign changes, billing, credentials, or live theme deployment. It may only read local repo files and write a local report.

## What This Means Here

For Dress Like Mommy, a "dream review" is not a new AI on the storefront. It is a local outcome-learning pass that reads deduplicated recent worklog events, current authority/status, linked decision outcomes, and supporting context, then answers:

- What mistake or blocker appears in at least two independent outcome events?
- Which checklist or prompt should be tightened?
- Which existing loop should future agents use first?
- What is the single next action closest to sales while staying inside approval boundaries?

The review can propose changes, but it must not promote them automatically. Human review is required before changing canonical prompts, live operating rules, or any live business surface. A valid authoritative `next_best_action` always outranks keyword frequency; missing or malformed authority fails closed to read-only reconciliation.

## Run

```bash
python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md
```

The script reads only local files. Sources have explicit roles and precedence:

1. `AUTHORITY`: `ops/marketing/current_marketing_state.md` supplies the current next action and effective authority.
2. `CURRENT_STATUS`: `ops/marketing/action_queue.md` and `ops/PROBLEM_TRACKER.md` corroborate open, done, blocked, or superseded state.
3. `OUTCOME_LOG`: `ops/marketing/decision_log.md` supplies linked decisions and observed outcomes.
4. `EVENT_LOG`: `ops/AGENT_WORKLOG.md` supplies candidate events identified by exact anchor declarations. The generator keeps the newest exact anchor and also fingerprints normalized observed-result content so a renamed copy cannot become another independent event.
5. `COORDINATION`: `ops/AGENT_COORDINATION.md` supplies ownership only.
6. `CONTEXT`: digests, prompts, and loop docs provide interpretation but never recurrence evidence.

Only observed-result sections in deduplicated worklog events count toward recurring signals. Repeated policy text, continuation prompts, next-action text, copied anchor references, copied observed results under a different anchor name, and ten mentions inside one event still count as zero or one event, never as independent outcomes.

## Review The Packet

Use the generated packet to decide whether to:

- keep the current prompts/checklists unchanged;
- make one small local checklist or prompt improvement;
- run an existing validation script before the next handoff;
- prepare an approval packet for a live-risk business action;
- leave a blocker alone because the exact next action is already clear.

The review is useful only when it improves the next agent's behavior. It is not progress by itself unless it produces a safer prompt/checklist, a clearer handoff, a validated report, or a sharper approval packet.

## Safe Promotion Rule

If the packet suggests a prompt or checklist change:

1. Pick one narrow failure pattern supported by two independent outcome events, or one high-severity event involving spend, customer truth, publication, credentials, destructive action, or approval scope.
2. Freeze three to five failing examples plus at least one passing holdout and define binary criteria before editing.
3. Score the current behavior where a local scorecard exists.
4. Make one small local change; do not edit the evaluator and evaluated prompt together.
5. Re-run the same examples, holdout, and repo continuity checks.
6. Keep the change only if failures improve without weakening approval boundaries, customer truth, or passing behavior.
7. Promote at most one durable rule per review. Otherwise record `NO_CHANGE`.

## Required Checks

After changing this loop, the dream prompt, scorecards, command-layer memory, or continuity logs, run:

```bash
python3.13 -m py_compile ops/scripts/generate_weekly_dream_review.py
python3.13 ops/tests/test_generate_weekly_dream_review.py
python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
python3.13 ops/scripts/check_continuity_integrity.py --strict
git diff --check
```

## Stop Rules

Stop and report instead of applying a suggestion when:

- the packet asks for live Shopify, ads, Pinterest, Merchant, GA4/GTM, feed, product, publication, budget, bid, status, billing, or credential changes;
- the suggested prompt change weakens approval boundaries;
- the suggestion creates a second paid-growth command layer;
- the packet repeats a solved issue without checking the latest worklog and tracker;
- the review cannot name one best next action;
- fewer than two independent outcome events support a routine recurring lesson and no single high-severity exception applies.
