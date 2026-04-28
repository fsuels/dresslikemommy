#!/usr/bin/env python3
"""Regression checks for local Google Shopping evidence conversion."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_google_shopping_local_evidence import (  # noqa: E402
    NEEDS_DATA,
    accessibility_pdp_status,
    build_merchant_evidence_rows,
    build_pdp_evidence_rows,
)


def current_row() -> dict[str, str]:
    return {
        "merchant_center_id": "shopify_US_1_2",
        "product_id": "1",
        "variant_id": "2",
        "handle": "mommy-and-me-dress",
    }


def main() -> None:
    merchant_rows, merchant_summary = build_merchant_evidence_rows(
        [current_row()],
        [
            {
                "Item ID": "shopify_US_1_2",
                "Country": "United States",
                "Item status": "ELIGIBLE",
                "Issue title": "Missing image",
            },
            {
                "Item ID": "shopify_US_1_2",
                "Country": "United Kingdom",
                "Item status": "ELIGIBLE",
                "Issue title": "Missing gender",
            },
        ],
        source_path=Path("merchant.csv"),
    )
    assert len(merchant_rows) == 1
    assert merchant_rows[0]["merchant_center_issue_count"] == "1"
    assert merchant_rows[0]["merchant_center_issues"] == "Missing image"
    assert merchant_rows[0]["image_status"] == "FAIL"
    assert merchant_rows[0]["price_status"] == NEEDS_DATA
    assert merchant_summary["merchant_issue_rows_for_current_us"] == 1

    accessible = {
        "product_id": "1",
        "handle": "mommy-and-me-dress",
        "online_store_url": "https://example.com/products/mommy-and-me-dress",
        "desktop_http_status": "200",
        "mobile_http_status": "200",
        "blocked_on_either": "false",
    }
    assert accessibility_pdp_status(accessible) == NEEDS_DATA
    assert accessibility_pdp_status({**accessible, "blocked_on_either": "true"}) == "FAIL"

    pdp_rows, pdp_summary = build_pdp_evidence_rows(
        [current_row()],
        [accessible],
        source_path=Path("pdp.csv"),
    )
    assert len(pdp_rows) == 1
    assert pdp_rows[0]["pdp_status"] == NEEDS_DATA
    assert pdp_summary["pdp_accessibility_current_products_matched"] == 1

    print("ok")


if __name__ == "__main__":
    main()
