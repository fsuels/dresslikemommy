# Self-Improvement Pilot Loop

Purpose: improve agent handoffs, prompts, and checklists without letting the agent rewrite live business systems or weaken approval boundaries.

Use this loop when the same type of agent mistake repeats, such as circular paid-growth monitoring, vague next steps, source/supplier leakage, weak listing handoffs, localization misses, feed grouping drift, or skipped UI verification.

Do not use this loop for live external writes. It may prepare local drafts, scorecards, reports, and approval packets only.

## Fit For This Repo

This loop is useful here because Dress Like Mommy already has clear scorecards:

- Paid-growth work must name one best next action, not several competing paths.
- Monitoring is not progress unless it produces a fix, bounded action, approval packet, reroute, or evidence-backed hold.
- Live spend, campaign status, budgets, bids, feeds, product data, conversion goals, billing, and publication changes stay approval-gated.
- Listing and localization work must avoid source leaks, unsupported inventory claims, size-chart guesses, and mixed-language PDPs.
- Pinterest and Merchant feed work must preserve grouped parent/variant behavior and run the existing guards.

## First Pilot: Paid-Growth Handoffs

The first local pilot is paid-growth handoff quality, because a bad handoff can waste the next session before any sales-moving work starts.

Use:

```bash
python3.13 ops/scripts/score_paid_growth_handoff.py path/to/handoff.md --fail-on-issues --write-report /tmp/paid-growth-handoff-scorecard.md
```

The handoff passes only when it:

- names the latest `AGENT_CONTINUITY_ANCHOR`;
- has exactly one `Next best action:` or `Recommended next action:`;
- points back to `ops/prompts/paid-growth-ai-army-continuation-prompt.md`;
- preserves fresh approval boundaries for live-risk changes;
- names a sales-moving outcome, repair, reroute, approval packet, or evidence-backed hold;
- names the blocker, gate, or next approval step;
- does not make monitoring the deliverable;
- does not include non-Dress-Like-Mommy URL-like source strings;
- does not imply a physical store, warehouse, local pickup, or owned on-hand stock.
- names the authoritative evidence date, execution mode, effective approval policy, and approved external scope, or explicitly marks authority context `NOT_APPLICABLE`;
- explicitly classifies whether the recommendation depends on uncertain state and, when it does, names the decision-changing evidence plus distinct actions for both possible outcomes;
- marks the decision `NOT_MATERIAL`, or names an independent verifier who did not build or execute the material action.

Use the exact machine-readable field names emitted by the scorecard. `NOT_APPLICABLE` and `NOT_MATERIAL` are valid only when the handoff truly does not depend on live authority or a material decision; they are not shortcuts around freshness, review, or approval gates.

For continuity-sensitive paid-growth handoffs, enable the optional semantic gate:

```bash
python3.13 ops/scripts/score_paid_growth_handoff.py path/to/handoff.md \
  --task-query "Continue PROB-or-exact-campaign-ID" \
  --task-entity PROB-or-exact-campaign-ID \
  --task-kind paid-growth \
  --fail-on-issues
```

This calls `ops/scripts/compile_task_context.py` and adds five cross-file checks: the handoff must name the task-relevant anchor, match current authority fields exactly with no duplicates, match the canonical next-action ID, use the authority-consistent evidence grade, and match a non-unknown task stage. Legacy invocations keep the frozen 12-criterion score unchanged. New anchors should carry `task_entities`, `task_stage`, and, when one exists, `next_action_id` as defined by `ops/MEMORY_CONTINUITY_PROTOCOL.md`.

## How To Improve A Prompt Safely

1. Pick one narrow recurring failure.
2. Collect three to five raw examples: a mix of passing and failing handoffs.
3. Score the current prompt or handoff style with the local script.
4. Make one small prompt or checklist change.
5. Score the same examples again.
6. Keep the change only if the fixed examples improve and the passing examples do not regress.
7. Human promotion is required before changing the canonical prompt or any live operating rule.

The scorecard must stay outside the prompt being improved. Agents may see the pass/fail result, but they must not edit the scoring script as part of the same prompt-improvement attempt.

## Weekly Review Layer

Use `docs/agent-loops/weekly-dream-review-loop.md` when the goal is broader than one handoff. That loop reads recent continuity and command-layer files, then writes a local review packet with recurring signals, proposed checklist rules, and one recommended next action.

Use:

```bash
python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md
```

The weekly review is advisory only. It may suggest prompt or checklist changes, but it must not promote them automatically or authorize live writes.

## Other Worthwhile Uses

Product listings:
- Use this loop to tighten listing prompts when drafts miss size-chart truth, make unsupported shipping/inventory claims, or leak source/supplier details.
- Keep validation tied to `ops/prompts/START-HERE.md`, the listing prompt, source-leak scans, and localized size-chart gates.

Localized PDPs:
- Use this loop to improve repair instructions when public localized pages keep leaking English or raw translation keys.
- Keep validation tied to `ops/scripts/audit_localized_pdp_language_leakage.py` plus desktop/mobile browser readback.

Feeds:
- Use this loop when feed handoffs repeatedly miss parent grouping, image parity, apparel attributes, or source hygiene.
- Keep validation tied to `ops/scripts/check_pinterest_feed_grouping.py`, `scripts/validateFeed/`, and the feed integrity loop.

Storefront QA:
- Use this loop when agents miss mobile layout, PDP builder, cart, collection, or localization checks.
- Keep validation tied to `docs/agent-loops/ui-browser-verification-loop.md`.

## Stop Rules

Stop and report instead of mutating further when:

- the scorecard itself seems wrong;
- a prompt change weakens approval boundaries;
- a candidate requires live external writes to prove value;
- the same candidate only gets shorter but drops Dress Like Mommy-specific safety details;
- results do not improve after two different small changes.

The next safe move after a failed pilot is to keep the old prompt, record the failed candidate, and pick a narrower failure pattern.
