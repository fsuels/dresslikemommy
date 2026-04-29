#!/usr/bin/env python3
"""Regression checks for the Phase 7 final launch gate packet."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/build_phase7_final_launch_gate_packet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_phase7_final_launch_gate_packet", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_phase7_final_gate_fails_closed_until_all_answers_are_yes() -> None:
    module = load_module()
    summary = module.build()

    assert summary["launch_allowed"] is False
    assert summary["launch_decision"] == "BLOCKED"
    assert summary["gates_required"] == 8
    assert summary["gates_yes"] == 1
    assert summary["gates_no"] == 7

    answers = {row["gate"]: row["answer"] for row in summary["gate_results"]}
    assert answers == {
        "Measurement >=85": "NO",
        "Feed >=85": "NO",
        "Website >=80": "NO",
        "Localization >=85": "NO",
        "Product economics": "YES",
        "Country economics": "NO",
        "Paid efficiency": "NO",
        "Blended spend": "NO",
    }


def test_phase7_final_gate_writes_operator_checklist_and_report() -> None:
    module = load_module()
    summary = module.build()

    checklist = read_csv(ROOT / summary["files"]["checklist"])
    assert len(checklist) == 8
    assert all(row["required_proof"] for row in checklist)
    assert all(row["source_artifacts"] for row in checklist)
    assert all(row["next_best_action"] for row in checklist)

    report = (ROOT / summary["files"]["report"]).read_text(encoding="utf-8")
    assert "Launch decision: `BLOCKED`" in report
    assert "Launch is blocked unless every gate answer is `YES`." in report
    assert "Product economics | YES" in report
    assert "Measurement >=85 | NO" in report


if __name__ == "__main__":
    test_phase7_final_gate_fails_closed_until_all_answers_are_yes()
    test_phase7_final_gate_writes_operator_checklist_and_report()
