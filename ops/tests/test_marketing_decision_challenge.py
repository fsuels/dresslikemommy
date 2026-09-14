#!/usr/bin/env python3
"""Frozen binary regression fixtures for the marketing challenge pilot."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops" / "scripts" / "check_continuity_integrity.py"
RENDERER = ROOT / "ops" / "scripts" / "render_marketing_cockpit.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


continuity = load_module(SCRIPT, "continuity_integrity_under_test")
renderer = load_module(RENDERER, "marketing_cockpit_renderer_under_test")
TODAY = date(2026, 7, 23)


def state_text(
    *,
    reconciled: str,
    source_as_of: str,
    mode: str,
    fresh_until: str,
    ready: str = "false",
    policy: str = "FRESH_ACTION_TIME_APPROVAL_REQUIRED",
    scope: str = "NONE",
    next_action: str = "READ_ONLY_MARKETING_RECONCILIATION",
) -> str:
    return f"""# Current Marketing State

Last reconciled: {reconciled} 12:00 EDT

## Authoritative Execution Control

<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->
- `control_as_of`: `2026-07-23`
- `source_live_evidence_as_of`: `{source_as_of}`
- `live_state_mode`: `{mode}`
- `live_readback_fresh_until`: `{fresh_until}`
- `autonomous_action_ready`: `{ready}`
- `effective_approval_policy`: `{policy}`
- `approved_external_scope`: `{scope}`
- `next_best_action`: `{next_action}`
- `supersedes_execution_readiness_below`: `true`
<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->
"""


def queue_text(
    *,
    reconciled: str,
    status: str = "YELLOW",
    action: str = "Read back only",
) -> str:
    return f"""# Marketing Action Queue

Last reconciled: {reconciled} 12:00 EDT

| Priority | Status | Action |
|---|---|---|
| P0 | {status} | {action} |
"""


def scorecard_text(*, reconciled: str) -> str:
    return f"""# Daily Scorecard

Last reconciled: {reconciled} 12:00 EDT
"""


def evaluate(
    state: str,
    queue: str,
    scorecard: str,
    *,
    spend_status: str | None = None,
):
    return continuity.evaluate_marketing_semantic_freshness(
        state,
        queue,
        scorecard,
        today=TODAY,
        spend_status=spend_status,
    )


def test_stale_without_control_fails() -> None:
    result = evaluate(
        "# Current Marketing State\n\nLast reconciled: 2026-06-01 12:00 EDT\n",
        queue_text(reconciled="2026-06-01"),
        scorecard_text(reconciled="2026-05-29"),
    )
    assert not result.ok
    assert "missing authoritative marketing control block" in result.detail


def test_stale_fail_closed_control_passes() -> None:
    result = evaluate(
        state_text(
            reconciled="2026-06-01",
            source_as_of="2026-06-01",
            mode="STALE_READBACK_REQUIRED",
            fresh_until="EXPIRED",
        ),
        queue_text(reconciled="2026-06-01"),
        scorecard_text(reconciled="2026-05-29"),
    )
    assert result.ok, result.detail
    assert "explicitly fail-closed" in result.detail


def test_stale_control_rejects_green_queue_row() -> None:
    result = evaluate(
        state_text(
            reconciled="2026-06-01",
            source_as_of="2026-06-01",
            mode="STALE_READBACK_REQUIRED",
            fresh_until="EXPIRED",
        ),
        queue_text(reconciled="2026-06-01", status="GREEN"),
        scorecard_text(reconciled="2026-05-29"),
    )
    assert not result.ok
    assert "cannot coexist with a GREEN" in result.detail


def test_live_current_rejects_expired_readback() -> None:
    result = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-22",
            next_action="REVIEW_CURRENT_EVIDENCE",
        ),
        queue_text(reconciled="2026-07-23"),
        scorecard_text(reconciled="2026-07-23"),
    )
    assert not result.ok
    assert "readback expired" in result.detail

    overlong = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-08-31",
            next_action="REVIEW_CURRENT_EVIDENCE",
        ),
        queue_text(reconciled="2026-07-23"),
        scorecard_text(reconciled="2026-07-23"),
    )
    assert not overlong.ok
    assert "exceeds the evidence-age limit" in overlong.detail

    lagging_queue = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            next_action="REVIEW_CURRENT_EVIDENCE",
        ),
        queue_text(reconciled="2026-07-22"),
        scorecard_text(reconciled="2026-07-23"),
    )
    assert not lagging_queue.ok
    assert "command-layer date predates source evidence" in lagging_queue.detail


def test_live_current_fresh_readback_passes_without_action_authority() -> None:
    result = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            next_action="REVIEW_CURRENT_EVIDENCE",
        ),
        queue_text(reconciled="2026-07-23"),
        scorecard_text(reconciled="2026-07-23"),
    )
    assert result.ok, result.detail
    assert "autonomous_action_ready=false" in result.detail

    unauthorized = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            ready="true",
            policy="APPROVED_ACTIVE_WITHIN_CAPS",
            scope="campaign:example",
            next_action="EXECUTE_APPROVED_ACTION",
        ),
        queue_text(reconciled="2026-07-23", status="GREEN"),
        scorecard_text(reconciled="2026-07-23"),
        spend_status="PENDING_OWNER_APPROVAL",
    )
    assert not unauthorized.ok
    assert "requires spend_authorization Status APPROVED_ACTIVE" in unauthorized.detail

    no_green = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            ready="true",
            policy="APPROVED_ACTIVE_WITHIN_CAPS",
            scope="campaign:example",
            next_action="EXECUTE_APPROVED_ACTION",
        ),
        queue_text(reconciled="2026-07-23", status="YELLOW"),
        scorecard_text(reconciled="2026-07-23"),
        spend_status="APPROVED_ACTIVE",
    )
    assert not no_green.ok
    assert "requires at least one GREEN" in no_green.detail

    wrong_green_scope = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            ready="true",
            policy="APPROVED_ACTIVE_WITHIN_CAPS",
            scope="campaign:example",
            next_action="EXECUTE_APPROVED_ACTION",
        ),
        queue_text(reconciled="2026-07-23", status="GREEN"),
        scorecard_text(reconciled="2026-07-23"),
        spend_status="APPROVED_ACTIVE",
    )
    assert not wrong_green_scope.ok
    assert "must be named exactly in backticks in a GREEN" in wrong_green_scope.detail

    authorized = evaluate(
        state_text(
            reconciled="2026-07-23",
            source_as_of="2026-07-23",
            mode="LIVE_CURRENT",
            fresh_until="2026-07-30",
            ready="true",
            policy="APPROVED_ACTIVE_WITHIN_CAPS",
            scope="campaign:example",
            next_action="EXECUTE_APPROVED_ACTION",
        ),
        queue_text(
            reconciled="2026-07-23",
            status="GREEN",
            action="Execute `campaign:example` inside frozen gates",
        ),
        scorecard_text(reconciled="2026-07-23"),
        spend_status="APPROVED_ACTIVE",
    )
    assert authorized.ok, authorized.detail


def test_material_decision_contract_and_resolution_markers_exist() -> None:
    reviewer = (ROOT / "ops" / "marketing" / "reviewer_checklist.md").read_text(
        encoding="utf-8"
    )
    decision_log = (ROOT / "ops" / "marketing" / "decision_log.md").read_text(
        encoding="utf-8"
    )
    marketing_guide = (ROOT / "ops" / "marketing" / "AGENTS.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "## Material Decision Challenge Contract",
        "Evidence that would change the decision.",
        "A named verifier who did not build or execute the action.",
        "A decision remains `UNRESOLVED`",
    ):
        assert marker in reviewer, marker
    for marker in (
        "DLM-DEC-2026-05-20-PINTEREST-RESTART",
        "`RESOLVED_RETROSPECTIVE`",
        "separate read-only `marketing_safety_reviewer`",
        "does not prove which alternative would have produced sales",
    ):
        assert marker in decision_log, marker
    for marker in (
        "Read `current_marketing_state.md`'s `Authoritative Execution Control` first.",
        "`APPROVED_ACTIVE` is necessary but not sufficient",
        "exact `approved_external_scope` value appears backticked in a `GREEN` action-queue row",
    ):
        assert marker in marketing_guide, marker

    cockpit_html = renderer.build_html()
    for marker in (
        "State: STALE_READBACK_REQUIRED",
        "Effective authority: FRESH_ACTION_TIME_APPROVAL_REQUIRED",
        "Standing spend record: APPROVED_ACTIVE",
        "READ_ONLY_MARKETING_RECONCILIATION",
        "Historical readiness is not current action authority",
    ):
        assert marker in cockpit_html, marker
    assert ">Spend: APPROVED_ACTIVE<" not in cockpit_html


def main() -> int:
    tests = [
        test_stale_without_control_fails,
        test_stale_fail_closed_control_passes,
        test_stale_control_rejects_green_queue_row,
        test_live_current_rejects_expired_readback,
        test_live_current_fresh_readback_passes_without_action_authority,
        test_material_decision_contract_and_resolution_markers_exist,
    ]
    for test in tests:
        test()
    print(f"ok: {len(tests)} frozen marketing decision challenge fixtures passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
