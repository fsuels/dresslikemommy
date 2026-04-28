#!/usr/bin/env python3
"""Regression checks for conservative Merchant Center browser RPC evidence."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_merchant_center_browser_rpc_evidence import browser_row_to_evidence  # noqa: E402


def browser_row(**overrides: str) -> dict[str, str]:
    row = {
        "merchant_center_item_id": "shopify_US_1_2",
        "language_code": "en",
        "price_currency": "USD",
        "price": "$24.99",
        "primary_source_name": "Shopify App API",
        "calculated_status_raw": "4",
        "aggregated_status_raw": "2",
        "main_image_thumbnail_status_raw": '{"2": 2}',
        "availability_raw": "0",
    }
    row.update(overrides)
    return row


def main() -> None:
    approved = browser_row_to_evidence(browser_row())
    assert approved["merchant_center_status"] == "Approved"
    assert approved["merchant_center_destination"] == "Shopping ads eligible"
    assert approved["merchant_center_issue_count"] == "0"
    assert approved["image_status"] == "PASS"
    assert approved["shipping_policy_status"] == "PASS"

    limited = browser_row_to_evidence(browser_row(calculated_status_raw="3"))
    assert limited["merchant_center_status"] == "Limited"
    assert limited["merchant_center_destination"] == "Shopping ads limited"
    assert limited["merchant_center_issue_count"] == "1"

    image_issue = browser_row_to_evidence(
        browser_row(aggregated_status_raw="5", main_image_thumbnail_status_raw='{"2": 5}')
    )
    assert image_issue["merchant_center_status"] == "Approved"
    assert image_issue["merchant_center_destination"] == "Shopping ads needs review"
    assert image_issue["image_status"] == "FAIL"
    assert image_issue["merchant_center_issue_count"] == "2"

    missing = browser_row_to_evidence(browser_row(language_code="", price_currency="", primary_source_name=""))
    assert missing["merchant_center_status"] == "NEEDS_DATA"
    assert missing["merchant_center_issue_count"] == "NEEDS_DATA"

    print("ok")


if __name__ == "__main__":
    main()
