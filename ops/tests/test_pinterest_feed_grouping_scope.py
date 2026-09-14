#!/usr/bin/env python3.13
"""Regression checks for current-feed vs historical Pinterest grouping scope."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/check_pinterest_feed_grouping.py"


def run_guard(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> None:
    current_gate = run_guard("--strict", "--json")
    assert current_gate.returncode == 0, current_gate.stdout + current_gate.stderr
    payload = json.loads(current_gate.stdout)
    assert payload["fails"] == 0
    assert payload["warnings"] >= 1

    warnings = [row for row in payload["results"] if row["verdict"] == "WARN"]
    assert warnings
    assert {row["scope"] for row in warnings} == {"historical_diagnostic"}

    forensic = run_guard("--strict", "--fail-historical-diagnostics", "--json")
    assert forensic.returncode == 1
    forensic_payload = json.loads(forensic.stdout)
    assert forensic_payload["fails"] == payload["warnings"]


if __name__ == "__main__":
    main()
    print("ok")
