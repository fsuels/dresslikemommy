#!/usr/bin/env python3.13
"""Semantic contract tests for the optional handoff task-context checks."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/score_paid_growth_handoff.py"

WORKLOG = """\
AGENT_CONTINUITY_ANCHOR: 2026-07-23-marketing-reconciliation-handoff
- `task_entities`: `PROB-2026-07-23-MARKETING-RECONCILIATION`
- `task_stage`: `HANDOFF`
- `next_action_id`: `READ_ONLY_MARKETING_RECONCILIATION`
Prepared the semantic paid-growth reconciliation handoff for PROB-2026-07-23-MARKETING-RECONCILIATION.
---
AGENT_CONTINUITY_ANCHOR: 2026-08-12-unrelated-newest-anchor
- `task_entities`: `PROB-2026-08-12-UNRELATED`
- `task_stage`: `BUILD`
Unrelated newest global anchor for PROB-2026-08-12-UNRELATED.
---
"""

CURRENT_STATE = """\
# Current Marketing State

<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->
- `control_as_of`: `2026-07-23`
- `source_live_evidence_as_of`: `2026-06-01`
- `live_state_mode`: `STALE_READBACK_REQUIRED`
- `live_readback_fresh_until`: `EXPIRED`
- `autonomous_action_ready`: `false`
- `effective_approval_policy`: `FRESH_ACTION_TIME_APPROVAL_REQUIRED`
- `approved_external_scope`: `NONE`
- `next_best_action`: `READ_ONLY_MARKETING_RECONCILIATION`
- `supersedes_execution_readiness_below`: `true`
<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->
"""

PASSING_HANDOFF = """\
AGENT_CONTINUITY_ANCHOR: 2026-07-23-marketing-reconciliation-handoff

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical prompt.

What changed:
- Prepared an exact approval packet after a read-only repair review.

Retrieved task contract:
- `control_as_of`: `2026-07-23`
- `source_live_evidence_as_of`: `2026-06-01`
- `live_state_mode`: `STALE_READBACK_REQUIRED`
- `live_readback_fresh_until`: `EXPIRED`
- `autonomous_action_ready`: `false`
- `effective_approval_policy`: `FRESH_ACTION_TIME_APPROVAL_REQUIRED`
- `approved_external_scope`: `NONE`
- `next_best_action`: `READ_ONLY_MARKETING_RECONCILIATION`
- `supersedes_execution_readiness_below`: `true`
- `evidence_grade`: `LIVE_READBACK_REQUIRED`
- `task_stage`: `HANDOFF`
- `decision_depends_on_uncertain_state`: `true`
- `decision_changing_evidence`: `A fresh same-window marketing reconciliation.`
- `if_evidence_supports_recommendation`: `Update the command layer and prepare the bounded action for review.`
- `if_evidence_opposes_recommendation`: `Keep fail-closed mode and reroute to a local sales-moving repair.`
- `material_decision`: `MATERIAL`
- `independent_verifier`: `marketing_safety_reviewer`
- `verifier_independence`: `DID_NOT_BUILD_OR_EXECUTE`

Guardrails:
- Fresh explicit action-time approval is required before any live change.
- No live spend, no campaign enablement, no budget/bid/status changes, no product-scope changes, no Merchant upload, and no Shopify live product-data changes.
- Dress Like Mommy has no physical store and no owned physical inventory.

Remaining blocker:
- The stale-evidence gate remains before any external write.

Next best action:
- Run the fresh read-only reconciliation, then follow the matching frozen outcome branch.
"""

SEMANTIC_CRITERIA = {
    "semantically_relevant_anchor",
    "authority_matches_current_control",
    "next_action_matches_current_control",
    "evidence_grade_matches_current_control",
    "task_stage_matches_retrieved_anchor",
}

LOCAL_HANDOFF = """\
AGENT_CONTINUITY_ANCHOR: local-context-anchor

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical prompt.

- `authority_context`: `NOT_APPLICABLE`
- `next_best_action`: `RUN_LOCAL_TESTS`
- `evidence_grade`: `REPO_KNOWN`
- `task_stage`: `BUILD`
- `decision_depends_on_uncertain_state`: `false`
- `material_decision`: `NOT_MATERIAL`

What changed:
- Prepared a local repair and fixed the scoped issue.

Guardrails:
- Fresh explicit action-time approval remains required for live work.
- No live spend, no campaign enablement, no budget/bid/status changes, no product-scope changes, no Merchant upload, and no Shopify live product-data changes.

Remaining gate:
- Run local verification before the next handoff.

Next best action:
- Run the local focused tests and hold with evidence if they fail.
"""


def write_context(tmpdir: Path) -> tuple[Path, Path, Path, Path]:
    worklog = tmpdir / "AGENT_WORKLOG.md"
    current_state = tmpdir / "current_marketing_state.md"
    tracker = tmpdir / "PROBLEM_TRACKER.md"
    coordination = tmpdir / "AGENT_COORDINATION.md"
    worklog.write_text(WORKLOG, encoding="utf-8")
    current_state.write_text(CURRENT_STATE, encoding="utf-8")
    tracker.write_text("# Problems\n", encoding="utf-8")
    coordination.write_text("# Coordination\n", encoding="utf-8")
    return worklog, current_state, tracker, coordination


def run_scorecard(
    tmpdir: Path, handoff_text: str, *, semantic: bool
) -> subprocess.CompletedProcess[str]:
    handoff = tmpdir / "handoff.md"
    handoff.write_text(handoff_text, encoding="utf-8")
    command = [sys.executable, str(SCRIPT), str(handoff), "--json", "--fail-on-issues"]
    if semantic:
        worklog, state, tracker, coordination = write_context(tmpdir)
        command.extend(
            [
                "--task-query",
                "Continue PROB-2026-07-23-MARKETING-RECONCILIATION",
                "--task-worklog",
                str(worklog),
                "--task-current-state",
                str(state),
                "--task-problem-tracker",
                str(tracker),
                "--task-coordination",
                str(coordination),
            ]
        )
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def parsed_result(completed: subprocess.CompletedProcess[str]):
    assert completed.stdout, completed.stderr
    payload = json.loads(completed.stdout)
    return payload, payload["results"][0]


def criterion_map(result: dict[str, object]) -> dict[str, bool]:
    return {
        item["name"]: item["passed"]  # type: ignore[index]
        for item in result["criteria"]  # type: ignore[index]
    }


def assert_legacy_mode_unchanged(tmpdir: Path) -> None:
    completed = run_scorecard(tmpdir, PASSING_HANDOFF, semantic=False)
    payload, result = parsed_result(completed)
    assert completed.returncode == 0, completed.stderr
    assert result["score"] == 12
    assert result["max_score"] == 12
    assert "task_context" not in payload
    assert not (SEMANTIC_CRITERIA & set(criterion_map(result)))


def assert_semantic_pass_and_relevant_not_global_latest(tmpdir: Path) -> None:
    completed = run_scorecard(tmpdir, PASSING_HANDOFF, semantic=True)
    payload, result = parsed_result(completed)
    assert completed.returncode == 0, (completed.stderr, result)
    assert result["score"] == 17
    assert result["max_score"] == 17
    criteria = criterion_map(result)
    assert all(criteria[name] for name in SEMANTIC_CRITERIA), criteria
    assert (
        payload["task_context"]["selected_anchor"]["anchor_id"]
        == "2026-07-23-marketing-reconciliation-handoff"
    )
    assert payload["task_context"]["task_stage"] == "HANDOFF"


def assert_each_semantic_mismatch_fails(tmpdir: Path) -> None:
    cases = {
        "semantically_relevant_anchor": PASSING_HANDOFF.replace(
            "AGENT_CONTINUITY_ANCHOR: 2026-07-23-marketing-reconciliation-handoff",
            "AGENT_CONTINUITY_ANCHOR: 2026-08-12-unrelated-newest-anchor",
        ),
        "authority_matches_current_control": PASSING_HANDOFF.replace(
            "- `approved_external_scope`: `NONE`",
            "- `approved_external_scope`: `ALL`",
        ),
        "next_action_matches_current_control": PASSING_HANDOFF.replace(
            "- `next_best_action`: `READ_ONLY_MARKETING_RECONCILIATION`",
            "- `next_best_action`: `LAUNCH_PINTEREST`",
        ),
        "evidence_grade_matches_current_control": PASSING_HANDOFF.replace(
            "- `evidence_grade`: `LIVE_READBACK_REQUIRED`",
            "- `evidence_grade`: `LIVE_VERIFIED`",
        ),
        "task_stage_matches_retrieved_anchor": PASSING_HANDOFF.replace(
            "- `task_stage`: `HANDOFF`",
            "- `task_stage`: `BUILD`",
        ),
    }
    for expected_failure, handoff in cases.items():
        case_dir = tmpdir / expected_failure
        case_dir.mkdir()
        completed = run_scorecard(case_dir, handoff, semantic=True)
        _, result = parsed_result(completed)
        assert completed.returncode == 1, expected_failure
        criteria = criterion_map(result)
        assert not criteria[expected_failure], (expected_failure, criteria)


def assert_duplicate_field_fails_even_when_last_value_is_correct(tmpdir: Path) -> None:
    handoff = PASSING_HANDOFF.replace(
        "- `approved_external_scope`: `NONE`",
        "- `approved_external_scope`: `ALL`\n- `approved_external_scope`: `NONE`",
    )
    completed = run_scorecard(tmpdir, handoff, semantic=True)
    _, result = parsed_result(completed)
    criteria = criterion_map(result)
    assert completed.returncode == 1
    assert not criteria["authority_matches_current_control"]


def assert_context_failure_propagates_to_semantic_score(tmpdir: Path) -> None:
    worklog, state, tracker, coordination = write_context(tmpdir)
    worklog.write_text(
        "AGENT_CONTINUITY_ANCHOR: unrelated\nNo matching task exists.\n---\n",
        encoding="utf-8",
    )
    handoff = tmpdir / "handoff.md"
    handoff.write_text(PASSING_HANDOFF, encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(handoff),
            "--json",
            "--fail-on-issues",
            "--task-query",
            "Continue PROB-2026-07-23-MARKETING-RECONCILIATION",
            "--task-worklog",
            str(worklog),
            "--task-current-state",
            str(state),
            "--task-problem-tracker",
            str(tracker),
            "--task-coordination",
            str(coordination),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload, result = parsed_result(completed)
    assert completed.returncode == 1
    assert payload["task_context"]["diagnostics"]["status"] == "FAILED_CLOSED"
    criteria = criterion_map(result)
    assert not criteria["semantically_relevant_anchor"]
    assert not criteria["authority_matches_current_control"]


def assert_unknown_legacy_stage_does_not_self_certify(tmpdir: Path) -> None:
    worklog, state, tracker, coordination = write_context(tmpdir)
    worklog.write_text(
        "AGENT_CONTINUITY_ANCHOR: 2026-07-23-marketing-reconciliation-handoff\n"
        "Semantic paid-growth reconciliation for "
        "PROB-2026-07-23-MARKETING-RECONCILIATION.\n---\n",
        encoding="utf-8",
    )
    handoff = tmpdir / "handoff.md"
    handoff.write_text(
        PASSING_HANDOFF.replace("- `task_stage`: `HANDOFF`", "- `task_stage`: `UNKNOWN`"),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(handoff),
            "--json",
            "--fail-on-issues",
            "--task-query",
            "Continue PROB-2026-07-23-MARKETING-RECONCILIATION",
            "--task-worklog",
            str(worklog),
            "--task-current-state",
            str(state),
            "--task-problem-tracker",
            str(tracker),
            "--task-coordination",
            str(coordination),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    _, result = parsed_result(completed)
    assert completed.returncode == 1
    assert not criterion_map(result)["task_stage_matches_retrieved_anchor"]


def assert_local_semantic_context_passes_without_marketing_state(tmpdir: Path) -> None:
    worklog = tmpdir / "AGENT_WORKLOG.md"
    tracker = tmpdir / "PROBLEM_TRACKER.md"
    coordination = tmpdir / "AGENT_COORDINATION.md"
    handoff = tmpdir / "handoff.md"
    worklog.write_text(
        "AGENT_CONTINUITY_ANCHOR: local-context-anchor\n"
        "- `task_entities`: `PROB-2026-08-12-LOCAL-CONTEXT`\n"
        "- `task_stage`: `BUILD`\n"
        "- `next_action_id`: `RUN_LOCAL_TESTS`\n"
        "Built PROB-2026-08-12-LOCAL-CONTEXT.\n---\n",
        encoding="utf-8",
    )
    tracker.write_text("# Problems\n", encoding="utf-8")
    coordination.write_text("# Coordination\n", encoding="utf-8")
    handoff.write_text(LOCAL_HANDOFF, encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(handoff),
            "--json",
            "--fail-on-issues",
            "--task-query",
            "Build PROB-2026-08-12-LOCAL-CONTEXT",
            "--task-kind",
            "local",
            "--task-worklog",
            str(worklog),
            "--task-current-state",
            str(tmpdir / "missing-current-state.md"),
            "--task-problem-tracker",
            str(tracker),
            "--task-coordination",
            str(coordination),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload, result = parsed_result(completed)
    assert completed.returncode == 0, (completed.stderr, result)
    assert payload["task_context"]["task_kind"] == "local"
    assert result["score"] == 17
    assert all(criterion_map(result)[name] for name in SEMANTIC_CRITERIA)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        legacy_case = tmpdir / "legacy"
        legacy_case.mkdir()
        assert_legacy_mode_unchanged(legacy_case)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        case = tmpdir / "semantic-pass"
        case.mkdir()
        assert_semantic_pass_and_relevant_not_global_latest(case)
        assert_each_semantic_mismatch_fails(tmpdir)
        duplicate_case = tmpdir / "duplicate"
        duplicate_case.mkdir()
        assert_duplicate_field_fails_even_when_last_value_is_correct(duplicate_case)
        failed_context_case = tmpdir / "failed-context"
        failed_context_case.mkdir()
        assert_context_failure_propagates_to_semantic_score(failed_context_case)
        unknown_stage_case = tmpdir / "unknown-stage"
        unknown_stage_case.mkdir()
        assert_unknown_legacy_stage_does_not_self_certify(unknown_stage_case)
        local_case = tmpdir / "local"
        local_case.mkdir()
        assert_local_semantic_context_passes_without_marketing_state(local_case)
    print("ok")


if __name__ == "__main__":
    main()
