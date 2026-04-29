#!/usr/bin/env python3
"""Regression checks for the Google Ads campaign gate packet."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_google_shopping_campaign_gate_packet import (  # noqa: E402
    POST_GATE_ADS_STRUCTURE,
    render_report,
)


def main() -> None:
    summary = {
        "generated_at": "2026-04-29T00:00:00",
        "paid_cohort_rows": 780,
        "paid_unique_shopify_products": 81,
        "paid_unique_proposed_item_groups": 131,
        "all_master_rows_reviewed": 7324,
        "excluded_rows": 6544,
        "paid_products_with_mixed_eligible_and_excluded_variants": 80,
        "paid_product_feed_structure_counts": {"A_TRUE_VARIANT_GROUP": 39},
        "paid_role_counts": {"mother": 429},
        "paid_family_counts": {"mommy_me": 214},
        "live_merchant_label_gate": "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE",
        "live_merchant_campaign_filter_gate": "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE",
        "live_merchant_full_label_gate": "BLOCKED_FULL_LABEL_MISMATCH",
        "campaign_filter_creation_allowed": True,
        "label_1_2_3_subdivision_allowed": False,
        "merchant_supplemental_label_join_gate": "BLOCKED_FULL_LABEL_MISMATCH",
        "merchant_supplemental_label_join_allowed": False,
        "purchase_conversion_value_gate": "BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY",
        "purchase_conversion_value_gate_passed": False,
        "purchase_conversion_value_detail": {
            "gate": {
                "purchase_conversion_value_gate_status": "BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY",
                "purchase_goal_active": True,
                "purchase_goal_results": 0.0,
                "target_conversion_action": "Google Shopping App Purchase",
                "target_is_primary_account_level_purchase_action": True,
                "target_last_conversion_date_raw": "20260128",
            },
            "source_artifact": "conversion-test-artifact.json",
        },
        "ads_dry_run_actionable_allowed": False,
        "ads_dry_run_actionable_blockers": [
            "Merchant Center supplemental label join is not fully visible for custom_label_1..3.",
            "Visible Purchase results are 0 for the current Google Ads date range.",
        ],
        "decision": "DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__MERCHANT_LABEL_JOIN_OR_PURCHASE_VALUE_BLOCKED",
        "live_merchant_label_detail": {
            "gate_status": "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE",
            "observed_us_en_rows": [],
            "observed_sample_label_mismatches": [],
            "source_artifact": "test-artifact.json",
        },
        "post_gate_ads_structure": POST_GATE_ADS_STRUCTURE,
    }

    report = render_report(summary)
    assert "DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__MERCHANT_LABEL_JOIN_OR_PURCHASE_VALUE_BLOCKED" in report
    assert "Campaign filter gate: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`" in report
    assert "Full label gate: `BLOCKED_FULL_LABEL_MISMATCH`" in report
    assert "Label 1-3 subdivision allowed: `False`" in report
    assert "Ads dry-run actionable allowed: `False`" in report
    assert "Purchase results in captured range: `0.0`" in report
    assert "Visible Purchase results are 0" in report
    assert "It is not actionable while `ads_dry_run_actionable_allowed` is false." in report
    assert "Do not restart Google Ads yet. This is a dry-run structure" in report
    assert "Brand Search — USA" in report
    assert "Standard Shopping — USA eligible products" in report
    assert "PMax — USA eligible products" in report
    assert "Non-brand Search" in report
    assert "Remarketing" in report
    assert "Exclude UNKNOWN_MARGIN, FIX_BEFORE_PAID, limited, and not-approved products." in report
    assert "URL expansion off unless an approved landing-page map exists." in report
    assert "Exclude pages not READY_FOR_PAID." in report
    assert "Do not use current limited ads." in report

    print("ok")


if __name__ == "__main__":
    main()
