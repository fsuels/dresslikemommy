# Paid-Growth Handoff Self-Improvement Pilot Readback

AGENT_CONTINUITY_ANCHOR: 2026-07-09-paid-growth-handoff-self-improvement-pilot

## Summary

Implemented a local-only self-improvement pilot for paid-growth handoff quality.

The pilot does not run an autonomous live loop. It gives agents a local scorecard before they change the canonical paid-growth prompt or hand off paid-growth work where circular monitoring, unclear next action, or approval-boundary drift is a risk.

## What Changed

- Added `docs/agent-loops/self-improvement-pilot-loop.md`.
- Added `ops/scripts/score_paid_growth_handoff.py`.
- Added `ops/tests/test_score_paid_growth_handoff.py`.
- Added this evidence packet and a sample handoff used to prove the scorecard.
- Linked the loop from `docs/agent-loops/README.md`, root `AGENTS.md` / `CLAUDE.md`, `ops/marketing/AGENTS.md`, and the canonical paid-growth prompt.

## Guardrails

- No Shopify Admin, Google Ads, Pinterest, Merchant Center, GA4/GTM, billing, campaign, budget, bid, status, feed/source, product, conversion, live theme, or product-publication write occurred.
- The scorecard is advisory evidence only.
- The scorecard cannot authorize live writes.
- The canonical prompt remains the single operating prompt.
- Human review is still required before promoting any prompt/checklist change.

## Verification

Commands run:

```bash
python3.13 -m py_compile ops/scripts/score_paid_growth_handoff.py
python3.13 ops/tests/test_score_paid_growth_handoff.py
python3.13 ops/scripts/score_paid_growth_handoff.py dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-07-09-paid-growth-handoff-self-improvement-pilot/sample_passing_paid_growth_handoff.md --json --fail-on-issues
python3.13 ops/scripts/score_paid_growth_handoff.py dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-07-09-paid-growth-handoff-self-improvement-pilot/sample_passing_paid_growth_handoff.md --fail-on-issues --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-07-09-paid-growth-handoff-self-improvement-pilot/paid_growth_handoff_scorecard_report.md
python3.13 ops/scripts/render_marketing_cockpit.py
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
python3.13 ops/scripts/check_continuity_integrity.py --strict
git diff --check
cmp -s AGENTS.md CLAUDE.md
```

Results:

- Script compile passed.
- Regression test passed.
- Sample handoff scored `9/9`.
- Generated report: `paid_growth_handoff_scorecard_report.md`.
- Marketing cockpit render passed.
- Marketing command-layer integration audit passed with `0` side-document risks.
- Strict continuity guard passed with `CONTINUITY_OK`.
- `git diff --check` passed.
- `AGENTS.md` and `CLAUDE.md` remain byte-for-byte identical.

Note:

- `python3.13 -m pytest ops/tests/test_score_paid_growth_handoff.py` could not run because this shell's Python environment does not have `pytest` installed. The direct Python regression test for the same file passed.

## Next Best Action

Use the scorecard before changing the canonical paid-growth prompt or before closing a paid-growth handoff that risks unclear next-action discipline. Keep actual revenue-moving work focused on the current top paid-growth gates; this pilot is a quality guard, not a replacement for campaign/feed/listing execution.
