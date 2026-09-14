# TTT Retrieval, Outcome Learning, And Prompt Compaction Readback

Date: `2026-08-12`

Status: `PASS_WITH_GATES__NO_UNRESOLVED_HIGH_OR_MEDIUM_FINDINGS`

## Objective

Apply the owner's TTT-inspired recommendations as a practical repo-local adaptation system: retrieve the minimum relevant context, keep changing state outside permanent prompts, learn only from observed outcomes, preserve decisions and later outcomes separately, and verify risky handoffs against current authority.

## Frozen Baseline

- Custom-instruction evaluation: `21/30` training and `13/18` validation.
- Canonical paid-growth prompt: `46,692` bytes.
- Weekly signal weakness: repeated mentions inside one continuity event could inflate a recurrence.
- Handoff weakness: the legacy scorecard checked explicit contract text but did not compare it with the task-relevant anchor and current authority.
- Instruction weakness: startup lists and dated execution state were duplicated across root, marketing, prompt, and historical memory surfaces.

## Implemented System

1. `ops/scripts/compile_task_context.py` deterministically retrieves a task-relevant anchor by exact entity or meaningful query terms, parses the authoritative paid-growth control block exactly, labels stale historical claims conservatively, and fails closed on missing or ambiguous context. Repo-local tasks can declare `authority_context=NOT_APPLICABLE`.
2. `ops/scripts/score_paid_growth_handoff.py` retains the frozen legacy 12-criterion contract and adds optional semantic checks for the retrieved anchor, exact current authority, canonical next action, evidence grade, and task stage.
3. `ops/scripts/generate_weekly_dream_review.py` counts only deduplicated worklog events and observed-result sections. It deduplicates both exact anchor IDs and identical normalized observed-result content under renamed anchors. A recurrence requires at least two independent events; current authority overrides historical keyword volume; malformed authority fails closed; at most one durable promotion is proposed per review.
4. `ops/marketing/decision_log.md` now separates frozen decisions from later outcomes. The reviewer checklist, memory digest, weekly loop, and prompt log carry the same forward-only learning rule.
5. Root and marketing instructions now contain stable retrieval, precedence, adaptive-effort, outcome-learning, and one-owner-action rules. Changing metrics, approvals, queues, and blockers stay in the existing command layer.
6. The canonical paid-growth continuation prompt now routes to the authoritative retrieval loop instead of embedding dated May state and fixed agent/tab queues.
7. `ops/scripts/check_continuity_integrity.py` guards the compact project-instruction budget as well as mirror parity.

## Measured Result

- Frozen custom-instruction evaluation: `30/30` training and `18/18` validation on run 2, followed by five unchanged perfect confirmation runs.
- Canonical paid-growth prompt: `8,741` bytes, down `37,951` bytes (`81.3%`).
- Root project guide: `9,049` bytes; paid-growth nested guide: `6,735` bytes; project root plus nested guide: `15,784` bytes.
- Current machine instruction chain: global `15,964` + root `9,049` + paid-growth nested `6,735` = `31,748` bytes, leaving `1,020` bytes under the documented default `32 KiB` project-instruction ceiling.
- Legacy handoff regression remains `30/36 -> 36/36` with unchanged holdout.
- Real task-context output selected the exact TTT anchor, preserved `READ_ONLY_MARKETING_RECONCILIATION`, and produced the same SHA-256 `fc0e1c0af8d215df6d2dc8f6676083bf2f5f94fbaeba434f46fe54b568fe6475` twice.
- Real semantic handoff scored `17/17`.
- Current weekly report reviewed `18` deduplicated events and kept current authority above historical signal volume.
- Focused task-context, semantic handoff, weekly-review, and material-decision tests pass.
- Marketing integration audit passes `25/25` with `0` side-document risks.
- Strict continuity returns `CONTINUITY_OK` after regenerating the local cockpit.

## Commands

The requested `python3.13` executable was unavailable. Equivalent local checks used bundled Python `3.12.13` at `/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

```bash
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m py_compile ops/scripts/compile_task_context.py ops/scripts/score_paid_growth_handoff.py ops/scripts/generate_weekly_dream_review.py ops/scripts/render_marketing_cockpit.py ops/scripts/check_continuity_integrity.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_compile_task_context.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_score_paid_growth_handoff.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_score_paid_growth_handoff_semantic.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_generate_weekly_dream_review.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_marketing_decision_challenge.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/scripts/render_marketing_cockpit.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/scripts/check_continuity_integrity.py --strict
```

## Safety Boundary

- This implementation is repo-local and reversible.
- It does not update model weights and does not turn inferred memory into authority.
- No Shopify, Google Ads, Pinterest, Merchant, GA4/GTM, campaign, budget, bid, status, feed, source, product, conversion, publication, billing, credential, infrastructure, or live-theme write occurred.
- Current paid-growth authority remains fail-closed at `READ_ONLY_MARKETING_RECONCILIATION` until a fresh same-window readback updates the command layer.

## Independent Verification And Closeout

- Independent verdict: `PASS_WITH_GATES`; no unresolved high or medium finding.
- Adversarial finding 1: the generator could count identical observed-result text under two differently named anchors. Resolution: deduplicate normalized observed-result fingerprints and retain only the newest copy; regression passes.
- Adversarial finding 2: repeated explicit task entities could act like alternatives when token scores differed. Resolution: every explicit entity is now a mandatory intersection constraint; missing co-location returns `REQUIRED_ENTITIES_NOT_COLOCATED`; asymmetric regression passes.
- The frozen decision remains unchanged. Its linked outcome record now carries measured results, the reviewer verdict, and the behavior-changing lessons.
- The active coordination claim is closed only after the final regenerated cockpit, integration audit, strict continuity, and diff checks pass.
