#!/usr/bin/env python3.13
"""Regression checks for the weekly dream review generator."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/generate_weekly_dream_review.py"


def load_module():
    spec = importlib.util.spec_from_file_location("generate_weekly_dream_review", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def event_source(module, text: str):
    lines = text.splitlines()
    return module.SourceReadback(
        path="ops/AGENT_WORKLOG.md",
        exists=True,
        total_lines=len(lines),
        included_lines=len(lines),
        anchor_count=len(module.ANCHOR_RE.findall(text)),
        text=text,
        role="EVENT_LOG",
        precedence=60,
        signal_eligible=True,
    )


def valid_control(action: str = "READ_ONLY_MARKETING_RECONCILIATION") -> str:
    return f"""
<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->
- `control_as_of`: `2026-08-12`
- `source_live_evidence_as_of`: `2026-08-12`
- `live_state_mode`: `STALE_READBACK_REQUIRED`
- `live_readback_fresh_until`: `EXPIRED`
- `autonomous_action_ready`: `false`
- `effective_approval_policy`: `FRESH_ACTION_TIME_APPROVAL_REQUIRED`
- `approved_external_scope`: `NONE`
- `next_best_action`: `{action}`
- `supersedes_execution_readiness_below`: `true`
<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->
"""


def test_repeated_mentions_in_one_event_do_not_qualify() -> None:
    module = load_module()
    text = """
## One event
AGENT_CONTINUITY_ANCHOR: one
Summary:
- Monitoring is not progress. Monitoring is not progress.
- Avoid monitoring as the deliverable and circular monitor loops.
Next best action:
- Monitoring is not progress.
"""
    signals = module.score_events(module.extract_review_events(event_source(module, text)))
    result = next(signal for signal in signals if signal.key == "monitor_only_drift")
    assert result.event_count == 1
    assert result.mention_count >= 4
    assert result.count == 1
    assert result.qualifies is False


def test_two_independent_observed_events_qualify_with_line_exemplars() -> None:
    module = load_module()
    text = """
## First event
AGENT_CONTINUITY_ANCHOR: first
Outcome:
- Monitoring is not progress when it creates no decision.
Next best action:
- Do more monitoring.

## Second event
AGENT_CONTINUITY_ANCHOR: second
Verification:
- We stopped monitoring as the deliverable and prepared the exact fix.
Continuation prompt:
- Ignore this monitoring as the deliverable phrase.
"""
    signals = module.score_events(module.extract_review_events(event_source(module, text)))
    result = next(signal for signal in signals if signal.key == "monitor_only_drift")
    assert result.event_count == 2
    assert result.qualifies is True
    assert len(result.exemplars) == 2
    assert result.exemplars[0].startswith("ops/AGENT_WORKLOG.md:")


def test_duplicate_anchor_uses_only_newest_event() -> None:
    module = load_module()
    text = """
## Old copy
AGENT_CONTINUITY_ANCHOR: duplicate
Summary:
- Monitoring is not progress.

## Independent event
AGENT_CONTINUITY_ANCHOR: independent
Summary:
- Monitoring is not progress.

## New copy
AGENT_CONTINUITY_ANCHOR: duplicate
Summary:
- No matching signal in this corrected record.
"""
    events = module.extract_review_events(event_source(module, text))
    assert [event.event_id for event in events] == ["independent", "duplicate"]
    signals = module.score_events(events)
    result = next(signal for signal in signals if signal.key == "monitor_only_drift")
    assert result.event_count == 1
    assert result.qualifies is False


def test_renamed_copy_of_same_outcome_counts_once() -> None:
    module = load_module()
    text = """
## Original event
AGENT_CONTINUITY_ANCHOR: original
Outcome:
- Monitoring is not progress when it creates no decision.

## Renamed copied event
AGENT_CONTINUITY_ANCHOR: copied-under-a-new-id
Outcome:
- Monitoring is not progress when it creates no decision.
"""
    events = module.extract_review_events(event_source(module, text))
    assert [event.event_id for event in events] == ["copied-under-a-new-id"]
    signals = module.score_events(events)
    result = next(signal for signal in signals if signal.key == "monitor_only_drift")
    assert result.event_count == 1
    assert result.qualifies is False


def test_context_sources_are_not_recurrence_evidence() -> None:
    module = load_module()
    source = module.SourceReadback(
        path="ops/prompts/example.md",
        exists=True,
        total_lines=5,
        included_lines=5,
        anchor_count=2,
        text="""
AGENT_CONTINUITY_ANCHOR: first
Summary:
- Monitoring is not progress.
AGENT_CONTINUITY_ANCHOR: second
Summary:
- Monitoring is not progress.
""",
        role="CONTEXT",
        precedence=10,
        signal_eligible=False,
    )
    assert module.extract_review_events(source) == []


def test_authoritative_next_action_overrides_historical_keywords() -> None:
    module = load_module()
    control = module.parse_authoritative_control(valid_control())
    signals = module.score_signals("Pinterest Phase 1 paused replacement setup")
    chosen = module.choose_next_action(
        "Pinterest Phase 1 paused replacement setup", signals, control
    )
    assert "READ_ONLY_MARKETING_RECONCILIATION" in chosen
    assert "Pinterest Phase 1" not in chosen


def test_malformed_or_duplicate_authority_fails_closed() -> None:
    module = load_module()
    malformed = module.parse_authoritative_control(
        valid_control().replace(
            "<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->",
            "- `next_best_action`: `PINTEREST_PHASE_1`\n"
            "<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->",
        )
    )
    assert malformed["valid"] is False
    assert malformed["next_best_action"] == module.FAIL_CLOSED_NEXT_ACTION
    chosen = module.choose_next_action("", [], malformed)
    assert module.FAIL_CLOSED_NEXT_ACTION in chosen


def test_latest_anchors_are_ordered() -> None:
    module = load_module()
    text = """
    AGENT_CONTINUITY_ANCHOR: first
    AGENT_CONTINUITY_ANCHOR: second
    AGENT_CONTINUITY_ANCHOR: third
    """
    assert module.latest_anchors(text, 2) == ["second", "third"]


def test_worklog_tail_expands_to_complete_event() -> None:
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "AGENT_WORKLOG.md"
        path.write_text(
            "## Complete event\n"
            "AGENT_CONTINUITY_ANCHOR: complete\n"
            "Summary:\n"
            "- Monitoring is not progress.\n"
            + "- filler\n" * 8,
            encoding="utf-8",
        )
        source = module.read_source(
            path,
            tail_lines=3,
            spec=module.SourceSpec(
                str(path), "EVENT_LOG", 60, True
            ),
        )
        events = module.extract_review_events(source)
        assert [event.event_id for event in events] == ["complete"]
        assert events[0].outcome_lines


def test_default_source_roles_and_precedence() -> None:
    module = load_module()
    specs = {spec.path: spec for spec in module.DEFAULT_SOURCE_SPECS}
    assert specs["ops/marketing/current_marketing_state.md"].role == "AUTHORITY"
    assert specs["ops/AGENT_WORKLOG.md"].signal_eligible is True
    assert specs["ops/marketing/dream_consolidation_prompt.md"].signal_eligible is False
    assert (
        specs["ops/marketing/current_marketing_state.md"].precedence
        > specs["ops/AGENT_WORKLOG.md"].precedence
    )


def test_cli_preserves_keys_and_uses_authoritative_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        fixture = tmpdir / "fixture.md"
        report = tmpdir / "report.md"
        fixture.write_text(
            """\
AGENT_CONTINUITY_ANCHOR: 2026-07-09-paid-growth-handoff-self-improvement-pilot

Summary:
- Monitoring is not progress. Use one best next action.
- Fresh explicit approval is required before live spend.
- score_paid_growth_handoff.py remains local-only.
""",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--as-of",
                "2026-07-09",
                "--source",
                str(fixture),
                "--write-report",
                str(report),
                "--json",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        payload = json.loads(proc.stdout)
        assert payload["local_only"] is True
        assert payload["external_writes"] is False
        assert payload["sources"][0]["exists"] is True
        assert payload["latest_anchors"]
        assert payload["signals"]
        assert payload["authoritative_control"]["valid"] is True
        assert "READ_ONLY_MARKETING_RECONCILIATION" in payload["recommended_next_action"]
        assert payload["signal_provenance"]["independent_event_threshold"] == 2
        assert payload["signal_provenance"]["event_deduplication"] == [
            "newest_exact_anchor_id",
            "newest_normalized_observed_result_fingerprint",
        ]
        assert report.exists()
        report_text = report.read_text(encoding="utf-8")
        assert "Integration status: `GENERATED`" in report_text
        assert "No Shopify Admin" in report_text
        assert "READ_ONLY_MARKETING_RECONCILIATION" in report_text


def main() -> None:
    test_repeated_mentions_in_one_event_do_not_qualify()
    test_two_independent_observed_events_qualify_with_line_exemplars()
    test_duplicate_anchor_uses_only_newest_event()
    test_renamed_copy_of_same_outcome_counts_once()
    test_context_sources_are_not_recurrence_evidence()
    test_authoritative_next_action_overrides_historical_keywords()
    test_malformed_or_duplicate_authority_fails_closed()
    test_latest_anchors_are_ordered()
    test_worklog_tail_expands_to_complete_event()
    test_default_source_roles_and_precedence()
    test_cli_preserves_keys_and_uses_authoritative_action()


if __name__ == "__main__":
    main()
    print("ok")
