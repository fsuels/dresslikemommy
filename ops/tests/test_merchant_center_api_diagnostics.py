#!/usr/bin/env python3
"""Regression checks for Merchant Center API diagnostics normalization."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.export_merchant_center_api_diagnostics import (  # noqa: E402
    bucket_status,
    content_product_status,
    evidence_row,
    extract_shopify_item_id,
    merchant_product_status,
)


def current_row() -> dict[str, str]:
    return {
        "merchant_center_id": "shopify_US_1_2",
        "product_id": "1",
        "variant_id": "2",
    }


def main() -> None:
    assert extract_shopify_item_id("online:en:US:shopify_US_1_2") == "shopify_US_1_2"

    status, destination, issues = merchant_product_status(
        {
            "productStatus": {
                "destinationStatuses": [
                    {"reportingContext": "SHOPPING_ADS", "approvedCountries": ["US"]}
                ],
                "itemLevelIssues": [],
            }
        }
    )
    assert status == "Approved"
    assert destination == "Shopping ads eligible"
    assert issues == []

    status, destination, _issues = content_product_status(
        {"destinationStatuses": [{"destination": "Shopping", "status": "disapproved"}]}
    )
    assert status == "Disapproved"
    assert destination == "Shopping ads not eligible"

    assert bucket_status([{"code": "image_link_pending_crawl"}], "image", approved=True) == "FAIL"
    assert bucket_status([], "image", approved=True) == "PASS"

    row = evidence_row(
        current_row(),
        status="Approved",
        destination="Shopping ads eligible",
        issues=[],
        source="unit",
    )
    assert row["merchant_center_issue_count"] == "0"
    assert row["image_status"] == "PASS"

    print("ok")


if __name__ == "__main__":
    main()
