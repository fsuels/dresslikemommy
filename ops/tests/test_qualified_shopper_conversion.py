#!/usr/bin/env python3
"""Regression checks for the qualified-shopper conversion scorecard."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "ops" / "scripts" / "qualified_shopper_conversion.py"


def load_module():
    spec = importlib.util.spec_from_file_location("qualified_shopper_conversion", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def result(sessions: int, carts: int, checkouts: int, completed: int) -> dict:
    return {
        "columns": [
            {"name": "sessions"},
            {"name": "sessions_with_cart_additions"},
            {"name": "sessions_that_reached_checkout"},
            {"name": "sessions_that_completed_checkout"},
            {"name": "conversion_rate"},
        ],
        "rows": [[str(sessions), str(carts), str(checkouts), str(completed), "0"]],
    }


def test_headline_uses_qualified_segment_not_total() -> None:
    module = load_module()
    report = module.compute_report({"total": result(5552, 131, 44, 9), "qualified": result(2342, 106, 22, 9)})
    assert round(report["headline_conversion_rate"], 6) == round(9 / 2342, 6)
    assert round(report["total_diagnostic"]["conversion_rate"], 6) == round(9 / 5552, 6)
    assert report["excluded_low_intent_or_unverified"]["sessions"] == 3210
    assert report["excluded_low_intent_or_unverified"]["sessions_that_completed_checkout"] == 0
    assert not any("dropping real buyers" in warning for warning in report["warnings"])
    assert any("directional" in warning for warning in report["warnings"])


def test_flags_excluded_buyers() -> None:
    module = load_module()
    report = module.compute_report({"total": result(1000, 50, 20, 10), "qualified": result(400, 30, 12, 6)})
    assert any("dropping real buyers" in warning for warning in report["warnings"])


def test_rejects_mismatched_windows() -> None:
    module = load_module()
    try:
        module.compute_report({"total": result(100, 5, 2, 1), "qualified": result(200, 5, 2, 1)})
    except ValueError:
        return
    raise AssertionError("qualified > total must fail")


def test_queries_share_one_window_and_segment() -> None:
    module = load_module()
    queries = module.build_queries("2026-08-25", "2026-09-23")
    assert all("SINCE 2026-08-25 UNTIL 2026-09-23" in query for query in queries.values())
    assert "WHERE" not in queries["total"]
    assert module.QUALIFIED_WHERE in queries["qualified"]


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_") and callable(test):
            test()
    print("PASS")
