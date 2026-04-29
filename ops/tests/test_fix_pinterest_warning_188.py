#!/usr/bin/env python3
"""Regression checks for Pinterest catalog warning fixes."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.fix_pinterest_warning_188 import VariantRecord, plan_price_changes  # noqa: E402


def variant(price: str, compare_at_price: str | None, *, active: bool = True) -> VariantRecord:
    return VariantRecord(
        variant_id="gid://shopify/ProductVariant/1",
        product_id="gid://shopify/Product/1",
        product_handle="test-product",
        product_title="Test Product",
        product_status="ACTIVE" if active else "DRAFT",
        online_store_published=active,
        pinterest_published=active,
        price=Decimal(price),
        compare_at_price=Decimal(compare_at_price) if compare_at_price is not None else None,
    )


def test_clear_mode_removes_all_invalid_compare_at_values() -> None:
    changes, stats = plan_price_changes(
        [
            variant("19.99", "19.99"),
            variant("19.99", "18.99"),
            variant("19.99", "0.00"),
            variant("19.99", "24.99"),
            variant("19.99", None),
        ],
        include_archived_products=False,
    )

    assert [change.new_cap for change in changes] == ["", "", ""]
    assert {change.reason for change in changes} == {"clear_invalid_compare_at_price"}
    assert stats["target_invalid_variant_changes"] == 3
    assert stats["invalid_compare_at_mode"] == "clear"


def test_out_of_scope_invalid_variants_are_not_changed() -> None:
    changes, stats = plan_price_changes(
        [variant("19.99", "18.99", active=False)],
        include_archived_products=False,
    )

    assert changes == []
    assert stats["skipped_out_of_scope_invalid_variants"] == 1


if __name__ == "__main__":
    test_clear_mode_removes_all_invalid_compare_at_values()
    test_out_of_scope_invalid_variants_are_not_changed()
    print("ok")
