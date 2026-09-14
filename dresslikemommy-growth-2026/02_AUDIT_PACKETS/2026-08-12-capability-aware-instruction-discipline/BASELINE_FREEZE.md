# Capability-Aware Handoff Baseline Freeze

Date: 2026-08-12

Scope: repo-local instruction and handoff evaluation only. No external-system read or write occurred.

## Frozen Before Root-Instruction Change

- Criteria implementation SHA-256 (`ops/scripts/score_paid_growth_handoff.py`): `1834fbda4a75545aefd0a40bfd28c0f45de0a3b3167ec4327e2462f78f0bafe0`
- Regression/comparison test SHA-256 (`ops/tests/test_score_paid_growth_handoff.py`): `a310ea8d1ca362f4661d80bad67871d306aebf259fd18d9daba6d88fa6716244`
- Scenario contract SHA-256 (`EVALUATION_SCENARIOS.md`): `9cbd0dab0b48c5ccaadf42246c648b0a0ff1aac0631f9095b31a3fec97cca715`
- Routine holdout SHA-256: `083580210495efbeb6b1f00f5986a221b42e1f5b8c1f0dee0f4985ac9a1432ad`
- Material-rule baseline SHA-256: `b1c4e4122e676e647c151bfee96a46fdacd24bb18e7bea3b64d52681039368d7`
- Stale-marketing baseline SHA-256: `682bb38e0608bfb2bb1606c41be3186a35bdc151f627b2aa752e91c80b519881`
- Pre-change `AGENTS.md` SHA-256: `7a1af56bc158a99f056c5f0ac18687ed945c020a433adb863a6d6583d66d3726`
- Pre-change `CLAUDE.md` SHA-256: `7a1af56bc158a99f056c5f0ac18687ed945c020a433adb863a6d6583d66d3726`

The root guides were byte-identical and unchanged while the criteria, examples, holdout, and baseline were frozen.

## Baseline Result

- Stale-marketing validation: `9/12`; only the three new criteria failed.
- Material-rule validation: `9/12`; only the three new criteria failed.
- Unchanged routine-local holdout: `12/12`.
- Combined baseline: `30/36`.
- Existing nine criteria: `27/27` across all three examples.

The generated criterion-by-criterion result is in `BASELINE_HANDOFF_SCORECARD.md`.

## Baseline Commands

```bash
python3.13 -m py_compile ops/scripts/score_paid_growth_handoff.py ops/tests/test_score_paid_growth_handoff.py
python3.13 ops/tests/test_score_paid_growth_handoff.py
```

The requested `python3.13` binary was not installed in this shell, so that first attempt stopped with `command not found` before either file ran. The same compile and direct test were then run with the bundled workspace Python 3.12.13 runtime:

```bash
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m py_compile ops/scripts/score_paid_growth_handoff.py ops/tests/test_score_paid_growth_handoff.py
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ops/tests/test_score_paid_growth_handoff.py
```

Result: `baseline frozen at 30/36; candidate fixtures not created yet` and `ok`.

The baseline scorecard was generated with the same bundled Python runtime and the three frozen fixture paths. It intentionally omitted `--fail-on-issues` because two baseline examples were expected to fail the three newly frozen criteria.
