#!/usr/bin/env python3
"""Regression checks for the Google Ads purchase conversion-value gate."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_google_ads_conversion_value_gate_packet import (  # noqa: E402
    DEFAULT_TARGET_CONVERSION_NAME,
    evaluate_gate,
    google_timestamp_to_iso,
    render_report,
)


REFERENCE_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)
RECENT_REQUEST_RAW = "1777161354592430"


def capture(
    purchase_results: float = 0.0,
    value_setting: str = "",
    last_received_request_time_raw: str = RECENT_REQUEST_RAW,
) -> dict[str, object]:
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
                "last_received_request_time_raw": last_received_request_time_raw,
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
                "last_received_request_time_raw": "0",
            },
        ],
        "tracking_implementation_evidence": {
            "google_ads_tag_ids": ["AW-853411529"],
            "conversion_send_to_ids": ["AW-853411529/UbkpCN-fhogBEMmN-JYD"],
            "ga4_measurement_ids": ["G-N4EQNK0MMB"],
            "manual_snippet_default_value_zero": True,
            "manual_snippet_blank_transaction_id": True,
        },
    }


def main() -> None:
    assert google_timestamp_to_iso(RECENT_REQUEST_RAW).startswith("2026-04-25T23:55:54")

    blocked = evaluate_gate(
        capture(last_received_request_time_raw="0"),
        DEFAULT_TARGET_CONVERSION_NAME,
        now=REFERENCE_NOW,
    )
    assert blocked["purchase_conversion_value_gate_passed"] is False
    assert blocked["purchase_conversion_value_gate_status"] == "BLOCKED_PURCHASE_CONVERSION_VALUE_TRACKING_NOT_VERIFIED"
    assert blocked["purchase_goal_active"] is True
    assert blocked["purchase_goal_results"] == 0.0
    assert blocked["primary_account_level_purchase_action_count"] == 1
    assert blocked["target_is_primary_account_level_purchase_action"] is True
    assert blocked["target_value_evidence_present"] is True
    assert blocked["target_recent_request_present"] is False
    assert blocked["campaign_enable_allowed"] is False
    assert blocked["blockers"] == ["Target purchase action has no received request within the last 7 days."]
    assert "Visible Purchase results are 0" in blocked["advisories"][0]

    tracking_verified = evaluate_gate(
        capture(),
        DEFAULT_TARGET_CONVERSION_NAME,
        now=REFERENCE_NOW,
    )
    assert tracking_verified["purchase_conversion_value_gate_passed"] is True
    assert (
        tracking_verified["purchase_conversion_value_gate_status"]
        == "PASS_PURCHASE_CONVERSION_VALUE_TRACKING_VERIFIED__NO_CURRENT_AD_ATTRIBUTION"
    )
    assert tracking_verified["current_purchase_results_passed"] is False
    assert tracking_verified["target_historical_value_present_in_raw_stats"] is True
    assert tracking_verified["target_last_received_request_time_iso"].startswith("2026-04-25T23:55:54")

    attributed_pass = evaluate_gate(
        capture(1.0, "Use different values. If there's no value, use 0."),
        DEFAULT_TARGET_CONVERSION_NAME,
        now=REFERENCE_NOW,
    )
    assert attributed_pass["purchase_conversion_value_gate_passed"] is True
    assert (
        attributed_pass["purchase_conversion_value_gate_status"]
        == "PASS_PURCHASE_CONVERSION_VALUE_RECORDING_WITH_CURRENT_AD_ATTRIBUTION"
    )

    report = render_report(
        {
            "generated_at": "2026-04-29T00:00:00",
            "gate": tracking_verified,
            "capture": capture(),
        }
    )
    assert "PASS_PURCHASE_CONVERSION_VALUE_TRACKING_VERIFIED__NO_CURRENT_AD_ATTRIBUTION" in report
    assert "Purchase results in visible date range: `0.0`" in report
    assert "Target recent request present: `True`" in report
    assert "Campaign enable allowed by this packet: `False`" in report
    assert "AW-853411529/UbkpCN-fhogBEMmN-JYD" in report
    assert "Visible Purchase results are 0" in report

    print("ok")


if __name__ == "__main__":
    main()
