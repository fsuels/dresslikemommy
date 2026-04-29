#!/usr/bin/env python3
"""Regression checks for the Google Ads purchase conversion-value gate."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_google_ads_conversion_value_gate_packet import (  # noqa: E402
    DEFAULT_TARGET_CONVERSION_NAME,
    evaluate_gate,
    render_report,
)


def capture(purchase_results: float = 0.0, value_setting: str = "") -> dict[str, object]:
    return {
        "list_page": {
            "title": "Conversion actions - dresslikemommy.com - Google Ads",
            "url": "https://ads.google.com/aw/conversions?ocid=220823493",
            "date_range": {"label": "Last 7 days", "start": "Apr 22, 2026", "end": "Apr 28, 2026"},
            "purchase_goal": {
                "purchase_goal_active": True,
                "purchase_goal_campaigns": "73 of 73",
                "purchase_goal_primary_conversion_actions": 1,
                "purchase_goal_results": purchase_results,
            },
        },
        "target_detail_page": {
            "settings": {
                "conversion_name": DEFAULT_TARGET_CONVERSION_NAME,
                "action_optimization": "Purchases, Primary action",
                "value_setting": value_setting,
                "source": "Website",
                "count": "Every conversion",
                "click_through_conversion_window": "90 days",
            }
        },
        "purchase_conversion_actions": [
            {
                "conversion_action_id": "285315039",
                "conversion_action": DEFAULT_TARGET_CONVERSION_NAME,
                "conversion_source": "Website",
                "action_optimization": "Primary",
                "count": "Every",
                "included_in_account_level_goals": True,
                "category_id": 1,
                "currency": "XXX",
                "last_conversion_date_raw": "20260128",
                "all_conversions_raw": 5.0,
                "all_conversion_value_raw": 193.9,
            },
            {
                "conversion_action_id": "996917005",
                "conversion_action": "dresslikemommy.com - GA4 (web) purchase",
                "conversion_source": "Website (Google Analytics (GA4))",
                "action_optimization": "Secondary",
                "count": "Every",
                "included_in_account_level_goals": False,
                "category_id": 1,
                "currency": "USD",
                "last_conversion_date_raw": "20260128",
                "all_conversions_raw": 16.5,
                "all_conversion_value_raw": 1300.12,
            },
        ],
    }


def main() -> None:
    blocked = evaluate_gate(capture(), DEFAULT_TARGET_CONVERSION_NAME)
    assert blocked["purchase_conversion_value_gate_passed"] is False
    assert blocked["purchase_conversion_value_gate_status"] == "BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY"
    assert blocked["purchase_goal_active"] is True
    assert blocked["purchase_goal_results"] == 0.0
    assert blocked["primary_account_level_purchase_action_count"] == 1
    assert blocked["target_is_primary_account_level_purchase_action"] is True
    assert blocked["target_value_evidence_present"] is True
    assert blocked["blockers"] == ["Visible Purchase results are 0 for the current Google Ads date range."]

    passed = evaluate_gate(
        capture(1.0, "Use different values. If there's no value, use 0."),
        DEFAULT_TARGET_CONVERSION_NAME,
    )
    assert passed["purchase_conversion_value_gate_passed"] is True
    assert passed["purchase_conversion_value_gate_status"] == "PASS_PURCHASE_CONVERSION_VALUE_RECORDING"

    report = render_report(
        {
            "generated_at": "2026-04-29T00:00:00",
            "gate": blocked,
            "capture": capture(),
        }
    )
    assert "BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY" in report
    assert "Purchase results in visible date range: `0.0`" in report
    assert "Visible Purchase results are 0" in report

    print("ok")


if __name__ == "__main__":
    main()
