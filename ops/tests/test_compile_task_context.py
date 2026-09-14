#!/usr/bin/env python3.13
"""Focused regression checks for retrieval-first task-context compilation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "ops/scripts"
sys.path.insert(0, str(SCRIPTS))

from compile_task_context import (  # noqa: E402
    compile_task_context,
    contains_exact_entity,
    extract_entities,
)


CURRENT_STATE = """\
# Current Marketing State

## Authoritative Execution Control

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


def write_fixture_set(tmpdir: Path, worklog: str, current_state: str = CURRENT_STATE):
    worklog_path = tmpdir / "AGENT_WORKLOG.md"
    current_state_path = tmpdir / "current_marketing_state.md"
    problem_path = tmpdir / "PROBLEM_TRACKER.md"
    coordination_path = tmpdir / "AGENT_COORDINATION.md"
    worklog_path.write_text(worklog, encoding="utf-8")
    current_state_path.write_text(current_state, encoding="utf-8")
    problem_path.write_text("# Problems\n", encoding="utf-8")
    coordination_path.write_text("# Coordination\n", encoding="utf-8")
    return worklog_path, current_state_path, problem_path, coordination_path


def compile_fixture(
    tmpdir: Path,
    worklog: str,
    query: str,
    *,
    current_state: str = CURRENT_STATE,
    entities: tuple[str, ...] = (),
):
    paths = write_fixture_set(tmpdir, worklog, current_state)
    return compile_task_context(
        query,
        explicit_entities=entities,
        worklog_path=paths[0],
        current_state_path=paths[1],
        problem_tracker_path=paths[2],
        coordination_path=paths[3],
    )


def assert_exact_entity_extraction() -> None:
    entities = extract_entities(
        "Continue AGENT_CONTINUITY_ANCHOR: 2026-07-23-paid-growth for "
        "PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS using "
        "ops/marketing/current_marketing_state.md and action "
        "READ_ONLY_MARKETING_RECONCILIATION for product 7607762845793."
    )
    assert "2026-07-23-paid-growth" in entities
    assert "PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS" in entities
    assert "ops/marketing/current_marketing_state.md" in entities
    assert "READ_ONLY_MARKETING_RECONCILIATION" in entities
    assert "7607762845793" in entities
    assert "Continue" not in entities


def assert_repeated_entity_selects_newest(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: 2026-07-01-old-pinterest-diagnosis
- `task_entities`: `PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS`
- `task_stage`: `DIAGNOSE`
Old diagnosis for PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS.
---
AGENT_CONTINUITY_ANCHOR: 2026-07-23-new-pinterest-diagnosis
- `task_entities`: `PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS`
- `task_stage`: `DIAGNOSE`
- `next_action_id`: `READ_ONLY_MARKETING_RECONCILIATION`
New diagnosis for PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS.
---
"""
    payload = compile_fixture(
        tmpdir,
        worklog,
        "Continue PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS diagnosis",
    )
    assert payload["diagnostics"]["status"] == "OK"
    assert payload["selected_anchor"]["anchor_id"] == "2026-07-23-new-pinterest-diagnosis"
    assert payload["task_stage"] == "DIAGNOSE"
    assert payload["next_action"]["id"] == "READ_ONLY_MARKETING_RECONCILIATION"


def assert_duplicate_anchor_dedupes_to_newest(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: repeated-anchor
First PROB-2026-01-01-EXAMPLE record.
---
AGENT_CONTINUITY_ANCHOR: repeated-anchor
- `task_stage`: `VERIFY`
Newest PROB-2026-01-01-EXAMPLE record.
---
"""
    payload = compile_fixture(
        tmpdir,
        worklog,
        "Verify PROB-2026-01-01-EXAMPLE",
    )
    assert payload["diagnostics"]["status"] == "OK"
    assert payload["diagnostics"]["duplicate_anchor_ids"] == ["repeated-anchor"]
    assert payload["selected_anchor"]["start_line"] == 4
    assert payload["task_stage"] == "VERIFY"


def assert_explicit_entity_recency_beats_prose(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: older-account-instructions
- `task_entities`: `330266838`
- `task_stage`: `DIAGNOSE`
Continue reconnect Google Analytics property330266838 purchase tracking conversion mapping.
Exclude the old Merchant account.
---
AGENT_CONTINUITY_ANCHOR: newer-account-repair
- `task_entities`: `330266838`
- `task_stage`: `HANDOFF`
- `next_action_id`: `READ_ONLY_MARKETING_RECONCILIATION`
The owner selected that Merchant account; the two repairs are verified.
---
AGENT_CONTINUITY_ANCHOR: unrelated-latest
- `task_entities`: `549756244483`
- `task_stage`: `BUILD`
Continue reconnect Google Analytics purchase tracking conversion mapping research.
---
"""
    for query in (
        "Continue Analytics 330266838 purchase tracking",
        "Reconnect Google Analytics 330266838 purchase tracking",
        "Verify Analytics property330266838 purchase conversion mapping",
    ):
        payload = compile_fixture(tmpdir, worklog, query, entities=("330266838",))
        assert payload["diagnostics"]["status"] == "OK"
        assert payload["selected_anchor"]["anchor_id"] == "newer-account-repair"
        assert payload["authority"]["fields"]["approved_external_scope"] == "NONE"

    contradictory = worklog.replace(
        "`next_action_id`: `READ_ONLY_MARKETING_RECONCILIATION`",
        "`next_action_id`: `LAUNCH_PINTEREST`",
    )
    payload = compile_fixture(
        tmpdir, contradictory, "Continue Analytics purchase tracking", entities=("330266838",)
    )
    assert payload["selected_anchor"]["anchor_id"] == "newer-account-repair"
    assert payload["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "selected anchor next_action_id contradicts authoritative control" in payload["diagnostics"]["errors"]

    implicit = compile_fixture(
        tmpdir, worklog, "Continue Analytics 330266838 purchase tracking"
    )
    assert implicit["selected_anchor"]["anchor_id"] == "older-account-instructions"


def assert_explicit_entity_recency_preserves_scope(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: full-required-scope
- `task_entities`: `330266838`, `513542500`, `PROB-2026-01-01-ALPHA`
- `task_stage`: `HANDOFF`
Compare detailed purchase tracking diagnosis for this property and Merchant.
---
AGENT_CONTINUITY_ANCHOR: newer-partial-scope
- `task_entities`: `330266838`
- `task_stage`: `DIAGNOSE`
Compare detailed purchase tracking diagnosis for this property.
---
AGENT_CONTINUITY_ANCHOR: newest-other-problem
- `task_entities`: `330266838`, `PROB-2026-01-01-BETA`
- `task_stage`: `DIAGNOSE`
Other issue.
---
"""
    intersection = compile_fixture(
        tmpdir, worklog, "Continue property work", entities=("330266838", "513542500")
    )
    assert intersection["diagnostics"]["status"] == "OK"
    assert intersection["selected_anchor"]["anchor_id"] == "full-required-scope"

    different_hit_set = compile_fixture(
        tmpdir,
        worklog,
        "Compare detailed purchase tracking diagnosis for PROB-2026-01-01-ALPHA and PROB-2026-01-01-BETA",
        entities=("330266838",),
    )
    assert different_hit_set["diagnostics"]["status"] == "OK"
    assert different_hit_set["selected_anchor"]["anchor_id"] == "full-required-scope"


def assert_no_global_fallback_or_ambiguous_guess(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: first-anchor
Alpha beta result.
---
AGENT_CONTINUITY_ANCHOR: second-anchor
Alpha beta result.
---
AGENT_CONTINUITY_ANCHOR: globally-newest-anchor
Unrelated gamma delta result.
---
"""
    no_match = compile_fixture(tmpdir, worklog, "quartz narwhal")
    assert no_match["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "NO_RELEVANT_ANCHOR" in no_match["diagnostics"]["errors"]
    assert no_match["selected_anchor"] is None

    ambiguous = compile_fixture(tmpdir, worklog, "alpha beta")
    assert ambiguous["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "AMBIGUOUS_RELEVANT_ANCHOR" in ambiguous["diagnostics"]["errors"]
    assert ambiguous["selected_anchor"] is None

    entity_ambiguous_worklog = """\
AGENT_CONTINUITY_ANCHOR: alpha-problem
Work for PROB-2026-01-01-ALPHA.
---
AGENT_CONTINUITY_ANCHOR: beta-problem
Work for PROB-2026-01-01-BETA.
---
"""
    entity_ambiguous = compile_fixture(
        tmpdir,
        entity_ambiguous_worklog,
        "Compare PROB-2026-01-01-ALPHA and PROB-2026-01-01-BETA",
    )
    assert entity_ambiguous["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "AMBIGUOUS_RELEVANT_ANCHOR" in entity_ambiguous["diagnostics"]["errors"]

    asymmetric_partial_worklog = """\
AGENT_CONTINUITY_ANCHOR: alpha-heavy
Work for PROB-2026-01-01-ALPHA with compare detailed evidence and repeated context.
---
AGENT_CONTINUITY_ANCHOR: beta-light
Work for PROB-2026-01-01-BETA.
---
"""
    required_intersection = compile_fixture(
        tmpdir,
        asymmetric_partial_worklog,
        "Compare detailed evidence for alpha and beta",
        entities=("PROB-2026-01-01-ALPHA", "PROB-2026-01-01-BETA"),
    )
    assert required_intersection["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "REQUIRED_ENTITIES_NOT_COLOCATED" in required_intersection["diagnostics"]["errors"]
    assert required_intersection["selected_anchor"] is None

    shared_required_worklog = entity_ambiguous_worklog.replace(
        "Work for", "Property 330266838. Work for"
    )
    distinct_hit_sets = compile_fixture(
        tmpdir,
        shared_required_worklog,
        "Compare PROB-2026-01-01-ALPHA and PROB-2026-01-01-BETA",
        entities=("330266838",),
    )
    assert distinct_hit_sets["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "AMBIGUOUS_RELEVANT_ANCHOR" in distinct_hit_sets["diagnostics"]["errors"]
    assert distinct_hit_sets["selected_anchor"] is None


def assert_authority_is_exact_and_fail_closed(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: authority-anchor
- `task_stage`: `HANDOFF`
Authority contract reconciliation.
---
"""
    good = compile_fixture(tmpdir, worklog, "authority contract reconciliation")
    assert good["diagnostics"]["status"] == "OK"
    assert good["authority"]["fields"] == {
        "approved_external_scope": "NONE",
        "autonomous_action_ready": "false",
        "control_as_of": "2026-07-23",
        "effective_approval_policy": "FRESH_ACTION_TIME_APPROVAL_REQUIRED",
        "live_readback_fresh_until": "EXPIRED",
        "live_state_mode": "STALE_READBACK_REQUIRED",
        "next_best_action": "READ_ONLY_MARKETING_RECONCILIATION",
        "source_live_evidence_as_of": "2026-06-01",
        "supersedes_execution_readiness_below": "true",
    }

    duplicate = CURRENT_STATE.replace(
        "- `approved_external_scope`: `NONE`",
        "- `approved_external_scope`: `NONE`\n- `approved_external_scope`: `ALL`",
    )
    bad = compile_fixture(
        tmpdir,
        worklog,
        "authority contract reconciliation",
        current_state=duplicate,
    )
    assert bad["diagnostics"]["status"] == "FAILED_CLOSED"
    assert any(
        "duplicate authoritative field(s)" in error
        for error in bad["diagnostics"]["errors"]
    )

    missing = CURRENT_STATE.replace(
        "- `approved_external_scope`: `NONE`\n",
        "",
    )
    missing_payload = compile_fixture(
        tmpdir,
        worklog,
        "authority contract reconciliation",
        current_state=missing,
    )
    assert missing_payload["diagnostics"]["status"] == "FAILED_CLOSED"
    assert any(
        "missing authoritative field(s)" in error
        for error in missing_payload["diagnostics"]["errors"]
    )


def assert_anchor_metadata_contradiction_fails_closed(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: contradictory-next-action
- `task_stage`: `HANDOFF`
- `next_action_id`: `LAUNCH_PINTEREST`
Marketing reconciliation contract.
---
"""
    payload = compile_fixture(
        tmpdir,
        worklog,
        "Marketing reconciliation contract",
    )
    assert payload["diagnostics"]["status"] == "FAILED_CLOSED"
    assert (
        "selected anchor next_action_id contradicts authoritative control"
        in payload["diagnostics"]["errors"]
    )


def assert_stale_evidence_labels_and_determinism(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: stale-live-anchor
- `task_stage`: `VERIFY`
LIVE_VERIFIED historical live readback for PROB-2026-02-02-STALE.
---
"""
    first = compile_fixture(
        tmpdir,
        worklog,
        "Monitor PROB-2026-02-02-STALE",
    )
    second = compile_fixture(
        tmpdir,
        worklog,
        "Monitor PROB-2026-02-02-STALE",
    )
    assert first == second
    assert "timestamp" not in json.dumps(first).casefold()
    assert first["authority"]["evidence_grade"] == "LIVE_READBACK_REQUIRED"
    anchor_evidence = [
        item
        for item in first["evidence"]
        if item["source_path"].endswith("AGENT_WORKLOG.md")
    ]
    assert anchor_evidence[0]["evidence_grade"] == "STALE_OR_SUPERSEDED"
    assert all(item["evidence_grade"] != "LIVE_VERIFIED" for item in first["evidence"])


def assert_local_task_does_not_require_marketing_authority(tmpdir: Path) -> None:
    worklog = tmpdir / "AGENT_WORKLOG.md"
    tracker = tmpdir / "PROBLEM_TRACKER.md"
    coordination = tmpdir / "AGENT_COORDINATION.md"
    worklog.write_text(
        "AGENT_CONTINUITY_ANCHOR: local-build\n"
        "- `task_entities`: `PROB-2026-08-12-LOCAL-CONTEXT`\n"
        "- `task_stage`: `BUILD`\n"
        "- `next_action_id`: `RUN_LOCAL_TESTS`\n"
        "Built the local context for PROB-2026-08-12-LOCAL-CONTEXT.\n---\n",
        encoding="utf-8",
    )
    tracker.write_text("# Problems\n", encoding="utf-8")
    coordination.write_text("# Coordination\n", encoding="utf-8")
    payload = compile_task_context(
        "Build PROB-2026-08-12-LOCAL-CONTEXT",
        worklog_path=worklog,
        current_state_path=tmpdir / "missing-current-state.md",
        problem_tracker_path=tracker,
        coordination_path=coordination,
        task_kind="local",
    )
    assert payload["diagnostics"]["status"] == "OK"
    assert payload["authority"]["context"] == "NOT_APPLICABLE"
    assert payload["next_action"]["id"] == "RUN_LOCAL_TESTS"
    assert payload["task_stage"] == "BUILD"
    assert payload["task_kind"] == "local"


COMPACT_MS_UET_WORKLOG = """\
AGENT_CONTINUITY_ANCHOR: 2026-01-01-ms-uet-spaced-history
task_entities: 654321,76543210
task_stage: DIAGNOSE
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
Historical Microsoft account 654321 and UET tag 76543210 receiver diagnosis.
---
AGENT_CONTINUITY_ANCHOR: 2026-01-03-ms-uet-compact-current
task_entities: Microsoft654321,UET76543210
task_stage: VERIFY
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
Current receiver checkpoint; preserve the unresolved acceptance gate and existing owner.
---
"""


def assert_compact_ms_uet_extraction() -> None:
    cases = (
        ("Microsoft654321", "654321"),
        ("mIcRoSoFt7654321", "7654321"),
        ("UET76543210", "76543210"),
        ("uet7654321", "7654321"),
        ("Microsoft20260914", "20260914"),
        ("UET20260914", "20260914"),
    )
    for text, expected in cases:
        entities = extract_entities(text)
        assert expected in entities, (text, entities)
        assert all(isinstance(entity, str) for entity in entities)
    assert extract_entities("Microsoft654321 UET76543210") == ["654321", "76543210"]


def assert_compact_ms_uet_exact_matching() -> None:
    for text, expected in (
        ("Microsoft654321", "654321"),
        ("microsoft7654321", "7654321"),
        ("UET76543210", "76543210"),
        ("uet7654321", "7654321"),
        ("Microsoft654321/customer123456; UET76543210/APP123456789", "654321"),
        ("Microsoft654321/customer123456; UET76543210/APP123456789", "76543210"),
        ("(Microsoft654321), `UET76543210`.", "654321"),
        ("(Microsoft654321), `UET76543210`.", "76543210"),
        ("Microsoft20260914", "20260914"),
        ("UET20260914", "20260914"),
    ):
        assert contains_exact_entity(text, expected), (text, expected)


def assert_compact_ms_uet_current_coordination(tmpdir: Path) -> None:
    paths = write_fixture_set(tmpdir, COMPACT_MS_UET_WORKLOG)
    coordination = """\
# Coordination
## Active Workstreams
| Workstream | Surface | Status | Owner / Agent | Allowed Actions | Blocked Actions | Last Evidence / Handoff | Notes |
|---|---|---|---|---|---|---|---|
| Current Microsoft receiver | Microsoft654321/customer123456; UET76543210/APP123456789 | RECEIVER_ACCEPTANCE_GATED | current-fixture-owner | Read own receiver | No paid or campaign write | 2026-01-03-current-receipt.json | Preserve the present owner and unresolved receipt gate. |
| Historical Microsoft setup | Microsoft account 654321; UET tag 76543210 | HISTORICAL_SETUP | historical-fixture-owner | Historical context only | No current scope | 2026-01-01-old-receipt.json | Older spaced identity is not the current claim. |
"""
    paths[3].write_text(coordination, encoding="utf-8")
    for required in (("654321",), ("76543210",), ("654321", "76543210")):
        payload = compile_task_context(
            "Continue Microsoft receiver",
            explicit_entities=required,
            worklog_path=paths[0], current_state_path=paths[1],
            problem_tracker_path=paths[2], coordination_path=paths[3],
        )
        claims = [item for item in payload["evidence"] if Path(item["source_path"]).resolve() == paths[3].resolve()]
        assert claims, required
        assert claims[0]["fields"]["Owner / Agent"] == "current-fixture-owner", (required, claims)
        assert set(required) <= set(claims[0]["matched_entities"])
        assert claims[0]["text"] == coordination.splitlines()[4]
        assert claims[0]["start_line"] == claims[0]["end_line"] == 5
        assert payload["authority"]["fields"]["approved_external_scope"] == "NONE"


def assert_compact_ms_uet_multi_identity_recency(tmpdir: Path) -> None:
    worklog = COMPACT_MS_UET_WORKLOG + """\
AGENT_CONTINUITY_ANCHOR: 2026-01-04-different-uet
task_entities: Microsoft654321,UET76543211
task_stage: HANDOFF
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
Later record has the same account but a different tag; it is not the required pair.
---
"""
    for query in ("Continue Microsoft receiver", "Continue Microsoft654321 UET76543210 receiver"):
        payload = compile_fixture(tmpdir, worklog, query, entities=("654321", "76543210"))
        assert payload["diagnostics"]["status"] == "OK"
        assert payload["selected_anchor"]["anchor_id"] == "2026-01-03-ms-uet-compact-current"
        assert set(payload["selected_anchor"]["entity_hits"]) == {"654321", "76543210"}
        assert payload["task_stage"] == "VERIFY"


def assert_compact_ms_uet_whole_identity_boundaries() -> None:
    for prefix, number in (("Microsoft", "654321"), ("UET", "76543210")):
        for text in (
            f"{prefix}1{number}", f"{prefix}{number}0",
            f"Other{prefix}{number}", f"_{prefix}{number}",
            f"{prefix}{number}x", f"{prefix}{number}_",
        ):
            assert number not in extract_entities(text), (text, number)
            assert not contains_exact_entity(text, number), (text, number)
    for text, number in (("Microsoft65432", "65432"), ("UET654321", "654321")):
        assert number not in extract_entities(text)
        assert not contains_exact_entity(text, number)
    assert "654321" not in extract_entities("654321")
    assert contains_exact_entity("Microsoft account 654321", "654321")
    assert contains_exact_entity("UET tag 76543210", "76543210")


def assert_compact_legacy_threshold_and_date_account_holdouts() -> None:
    legacy_prefixes = (
        "Merchant", "GA4", "property", "Ads", "manager", "Shopify", "Product",
        "campaign", "source", "theme", "advertiser", "tag", "pixel", "variant", "Purchase",
    )
    for prefix in legacy_prefixes:
        assert "654321" not in extract_entities(f"{prefix}654321"), prefix
        assert not contains_exact_entity(f"{prefix}654321", "654321"), prefix
        for number in ("7654321", "20260914"):
            assert number in extract_entities(f"{prefix}{number}"), prefix
            assert contains_exact_entity(f"{prefix}{number}", number), prefix
    assert "20260914" in extract_entities("20260914")
    assert contains_exact_entity("20260914", "20260914")
    assert "7760272273" in extract_entities("Purchase7760272273")
    assert contains_exact_entity("Purchase7760272273", "7760272273")


def assert_compact_ms_uet_split_scope_fails_closed(tmpdir: Path) -> None:
    worklog = """\
AGENT_CONTINUITY_ANCHOR: account-only
task_entities: Microsoft654321
task_stage: DIAGNOSE
Only this account is present.
---
AGENT_CONTINUITY_ANCHOR: tag-only
task_entities: UET76543210
task_stage: VERIFY
Only this tag is present.
---
"""
    payload = compile_fixture(
        tmpdir, worklog, "Continue Microsoft654321 UET76543210 receiver",
        entities=("654321", "76543210"),
    )
    assert payload["diagnostics"]["status"] == "FAILED_CLOSED"
    assert "REQUIRED_ENTITIES_NOT_COLOCATED" in payload["diagnostics"]["errors"]
    assert payload["selected_anchor"] is None


def run_compact_ms_uet_checks() -> None:
    assert_compact_ms_uet_extraction()
    assert_compact_ms_uet_exact_matching()
    assert_compact_ms_uet_whole_identity_boundaries()
    assert_compact_legacy_threshold_and_date_account_holdouts()
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        assert_compact_ms_uet_current_coordination(tmpdir)
        assert_compact_ms_uet_multi_identity_recency(tmpdir)
        assert_compact_ms_uet_split_scope_fails_closed(tmpdir)


def main() -> None:
    assert_exact_entity_extraction()
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        assert_repeated_entity_selects_newest(tmpdir)
        assert_duplicate_anchor_dedupes_to_newest(tmpdir)
        assert_explicit_entity_recency_beats_prose(tmpdir)
        assert_explicit_entity_recency_preserves_scope(tmpdir)
        assert_no_global_fallback_or_ambiguous_guess(tmpdir)
        assert_authority_is_exact_and_fail_closed(tmpdir)
        assert_anchor_metadata_contradiction_fails_closed(tmpdir)
        assert_stale_evidence_labels_and_determinism(tmpdir)
        assert_local_task_does_not_require_marketing_authority(tmpdir)
    run_compact_ms_uet_checks()
    print("ok")


if __name__ == "__main__":
    main()
