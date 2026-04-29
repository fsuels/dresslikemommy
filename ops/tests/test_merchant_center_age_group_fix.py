#!/usr/bin/env python3
"""Tests for Merchant Center age_group supplemental feed inference."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_merchant_center_age_group_fix import build_rows, infer_age_group


def check(row: dict[str, str], expected_age_group: str) -> None:
    actual, source = infer_age_group(row)
    assert actual == expected_age_group, (row, actual, source)


def test_infer_age_group_from_variant_titles() -> None:
    check({"variant_title": "Newborn / White"}, "newborn")
    check({"variant_title": "Baby 0-3 Months / Pink"}, "newborn")
    check({"variant_title": "Baby 6-9 Months / Pink"}, "infant")
    check({"variant_title": "Child 4-5 years / Black"}, "toddler")
    check({"variant_title": "Child 6-8 years / Black"}, "kids")
    check({"variant_title": "Mother XL / Floral"}, "adult")
    check({"variant_title": "S / Blue", "product_title": "Maternity Wrap Dress"}, "adult")


def test_build_rows_preserves_paid_status_and_supported_values() -> None:
    rows = [
        {
            "merchant_center_id": "shopify_US_1_10",
            "product_id": "1",
            "variant_id": "10",
            "handle": "mommy-and-me",
            "product_title": "Mommy and Me Dresses",
            "variant_title": "Mother S / Pink",
            "sku": "",
        },
        {
            "merchant_center_id": "shopify_US_1_11",
            "product_id": "1",
            "variant_id": "11",
            "handle": "mommy-and-me",
            "product_title": "Mommy and Me Dresses",
            "variant_title": "Child 2-3 years / Pink",
            "sku": "",
        },
    ]
    upload_rows, review_rows, summary = build_rows(
        rows,
        {
            "shopify_US_1_10": "FIX_BEFORE_PAID",
            "shopify_US_1_11": "EXCLUDE_PAID",
        },
    )

    assert upload_rows == [
        {"id": "shopify_US_1_10", "custom_label_4": "FIX_BEFORE_PAID", "age_group": "adult"},
        {"id": "shopify_US_1_11", "custom_label_4": "EXCLUDE_PAID", "age_group": "toddler"},
    ]
    assert {row["status"] for row in review_rows} == {"upload"}
    assert summary["manual_review_rows"] == 0
    assert summary["excluded_offer_does_not_exist_rows"] == 0
    assert summary["custom_label_4_counts"] == {"FIX_BEFORE_PAID": 1, "EXCLUDE_PAID": 1}


def test_build_rows_excludes_known_missing_offers() -> None:
    rows = [
        {
            "merchant_center_id": "shopify_US_1_10",
            "product_id": "1",
            "variant_id": "10",
            "handle": "mommy-and-me",
            "product_title": "Mommy and Me Dresses",
            "variant_title": "Mother S / Pink",
            "sku": "",
        },
        {
            "merchant_center_id": "shopify_US_1_11",
            "product_id": "1",
            "variant_id": "11",
            "handle": "mommy-and-me",
            "product_title": "Mommy and Me Dresses",
            "variant_title": "Child 2-3 years / Pink",
            "sku": "",
        },
    ]
    upload_rows, review_rows, summary = build_rows(
        rows,
        {
            "shopify_US_1_10": "FIX_BEFORE_PAID",
            "shopify_US_1_11": "FIX_BEFORE_PAID",
        },
        {"shopify_US_1_11"},
    )

    assert upload_rows == [
        {"id": "shopify_US_1_10", "custom_label_4": "FIX_BEFORE_PAID", "age_group": "adult"},
    ]
    assert [row["status"] for row in review_rows] == ["upload", "excluded_offer_does_not_exist"]
    assert summary["upload_rows"] == 1
    assert summary["excluded_offer_does_not_exist_rows"] == 1


if __name__ == "__main__":
    test_infer_age_group_from_variant_titles()
    test_build_rows_preserves_paid_status_and_supported_values()
    test_build_rows_excludes_known_missing_offers()
