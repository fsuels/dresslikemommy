# Capability-Aware Instruction Readback

Date: 2026-08-12

Scope: local instruction, scorer, fixtures, evidence, and continuity records only. No external-system read or write occurred.

## Result

Keep decision: `KEEP`.

- Frozen baseline: `30/36`.
- Candidate with the unchanged holdout: `36/36`.
- Existing nine criteria: `27/27` before and after.
- Unchanged routine holdout: `12/12` before and after.
- Independent safety review: `PASS`; no high or medium findings.

The candidate was retained because the failing validation examples improved, the passing holdout and previous criteria did not regress, the root guides remain byte-identical, and approval/customer-truth/external-write guardrails were not weakened.

## Freeze And Separate-Change Evidence

`BASELINE_FREEZE.md` records the criteria, tests, scenarios, baseline examples, holdout, and their SHA-256 hashes before either root guide changed. Those hashes remain unchanged after the candidate run.

- Pre-change guide hash: `7a1af56bc158a99f056c5f0ac18687ed945c020a433adb863a6d6583d66d3726`.
- Candidate guide hash: `dafc25ae704c88779b448759cb0556fe05ee3e5f1dd0eca27766e89c0907941b`.
- Removing only the inserted `Capability-Aware Decision Discipline` section from the candidate reproduces the pre-change hash.
- Current guide mirror: byte-for-byte identical.

The scorer and test were not modified after candidate results were seen. The candidate validation files reuse the same two frozen scenario IDs, and the original holdout file is reused unchanged.

## Frozen Comparison

| Scenario | Baseline | Candidate | Regression status |
|---|---:|---:|---|
| Stale marketing reconciliation | `9/12` | `12/12` | Improved; old `9/9` preserved |
| Material durable-rule decision | `9/12` | `12/12` | Improved; old `9/9` preserved |
| Routine local holdout | `12/12` | `12/12` | Unchanged |
| Combined | `30/36` | `36/36` | Improved by `6`; no old-criterion or holdout regression |

The three added binary criteria are:

1. `authoritative_execution_context`.
2. `uncertainty_outcome_branches`.
3. `independent_material_decision_verifier`.

## Independent Review

A separate read-only `marketing_safety_reviewer` who did not build or execute the change independently reran the scorer and hash checks and returned `PASS`.

The reviewer confirmed:

- no approval, freshness, inventory-truth, customer-truth, or external-write boundary was weakened;
- no competing command or state layer was introduced;
- deliberation and backtracking are bounded rather than open-ended;
- private chain-of-thought is neither required nor exposed; and
- the missing tracked `ops/marketing/operator_cockpit.html` is unrelated to this candidate.

## Verification Readback

- Direct scorer test: `PASS` — `candidate improved 30/36 -> 36/36 with unchanged holdout`; `ok`.
- Candidate scorer run with `--fail-on-issues`: `PASS` — `3/3` files, each `12/12`.
- Marketing decision fixtures: `PASS` — `6` frozen fixtures.
- Marketing command-layer integration audit: `PASS` — `24/24` integrated/generated/archive files; `0` risks.
- Guide mirror check: `PASS`.
- Full and touched-scope `git diff --check`: `PASS`.
- Strict continuity: `PARTIAL / PRE-EXISTING GATE` — all relevant candidate/marketing/feed/listing/mirror gates pass, but the command returns nonzero because tracked `ops/marketing/operator_cockpit.html` is already missing, which fails cockpit presence and freshness. The unrelated deletion was preserved.

The requested `python3.13` executable was not installed in this shell. After the failed lookup, all Python checks were run with the bundled workspace Python `3.12.13` runtime at `/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

## Residual Risk

The binary scorer proves that required fields are explicit; it does not prove their claims are current or true. Canonical source readbacks, semantic-freshness checks, owner approval, and real independent verification remain the authority for material or external action.

## Next Action

Keep this local instruction change. Resolve the unrelated cockpit deletion only in a separately scoped local task, or leave it intact if the deletion is intentional. For paid growth, the first operational action remains a fresh same-window read-only reconciliation before historical readiness can become current authority.
