#!/usr/bin/env python3
"""Regression checks for the Shopify variant cost sync rule."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.sync_shopify_variant_costs import (  # noqa: E402
    build_plan_rows,
    costs_match,
    desired_cost_from_price,
    money,
)


def variant(price: str, current_cost: str = "", status: str = "ACTIVE") -> dict:
    return {
        "id": "gid://shopify/ProductVariant/1",
        "legacyResourceId": "1",
        "title": "Mother M",
        "sku": "TEST-M",
        "price": price,
        "inventoryItem": {
            "id": "gid://shopify/InventoryItem/1",
            "legacyResourceId": "1",
            "unitCost": {"amount": current_cost, "currencyCode": "USD"} if current_cost else None,
        },
        "product": {
            "id": "gid://shopify/Product/1",
            "legacyResourceId": "1",
            "title": "Test Product",
            "handle": "test-product",
            "status": status,
        },
    }


def main() -> None:
    assert money(Decimal("10")) == "10.00"
    assert desired_cost_from_price("20.00") == Decimal("10.00")
    assert desired_cost_from_price("19.99") == Decimal("10.00")
    assert desired_cost_from_price("") is None
    assert costs_match("10", Decimal("10.00"))
    assert not costs_match("", Decimal("10.00"))

    missing_cost = build_plan_rows([variant("20.00")], cost_ratio=Decimal("0.50"), only_missing=False)[0]
    assert missing_cost["desired_unit_cost"] == "10.00"
    assert missing_cost["action"] == "update_cost"
    assert missing_cost["reason"] == "missing_cost"
    assert missing_cost["paid_eligible"] == "FALSE"
    assert missing_cost["paid_eligible_after_sync"] == "TRUE"

    wrong_cost = build_plan_rows([variant("20.00", "9.99")], cost_ratio=Decimal("0.50"), only_missing=False)[0]
    assert wrong_cost["action"] == "update_cost"
    assert wrong_cost["reason"] == "cost_not_50pct_of_price"
    assert wrong_cost["paid_eligible"] == "FALSE"

    existing_cost_only_missing = build_plan_rows(
        [variant("20.00", "9.99")], cost_ratio=Decimal("0.50"), only_missing=True
    )[0]
    assert existing_cost_only_missing["action"] == "skip_existing_cost"

    synced = build_plan_rows([variant("20.00", "10.00")], cost_ratio=Decimal("0.50"), only_missing=False)[0]
    assert synced["action"] == "skip_already_synced"
    assert synced["paid_eligible"] == "TRUE"

    no_price = build_plan_rows([variant("")], cost_ratio=Decimal("0.50"), only_missing=False)[0]
    assert no_price["action"] == "cannot_calculate"
    assert no_price["paid_eligible"] == "FALSE"

    print("ok")


if __name__ == "__main__":
    main()
