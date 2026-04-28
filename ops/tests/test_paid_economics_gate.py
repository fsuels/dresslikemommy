#!/usr/bin/env python3
"""Regression checks for the paid-spend economics gate."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.apply_paid_economics_gate import (  # noqa: E402
    DEFAULT_AOV_BENCHMARK,
    ProductGateEvidence,
    paid_gate_for_row,
)


def base_row(**overrides: str) -> dict[str, str]:
    row = {
        "price": "24.99",
        "unit_cost": "",
        "paid_status": "FIX_BEFORE_PAID",
        "paid_status_reasons": "VARIANT_DEFECTS:unit_cost_missing",
    }
    row.update(overrides)
    return row


def main() -> None:
    unknown_set = paid_gate_for_row(
        base_row(),
        ProductGateEvidence(product_set_type="set", marketing_margin_tier=""),
        DEFAULT_AOV_BENCHMARK,
    )
    assert unknown_set.paid_status == "EXCLUDE_PAID"
    assert unknown_set.gate_status == "BLOCKED"
    assert unknown_set.paid_eligible is False
    assert "UNKNOWN_COST_NO_RELIABLE_COST_BASIS" in unknown_set.reasons
    assert "LOW_AOV_NO_BUNDLE_REPRICE_OR_COST_BASIS" not in unknown_set.reasons
    assert "BUNDLED_AOV_BASIS" in unknown_set.exceptions

    unknown_single = paid_gate_for_row(
        base_row(),
        ProductGateEvidence(product_set_type="single", marketing_margin_tier=""),
        DEFAULT_AOV_BENCHMARK,
    )
    assert unknown_single.paid_status == "EXCLUDE_PAID"
    assert unknown_single.paid_eligible is False
    assert "UNKNOWN_COST_NO_RELIABLE_COST_BASIS" in unknown_single.reasons
    assert "LOW_AOV_NO_BUNDLE_REPRICE_OR_COST_BASIS" in unknown_single.reasons

    known_set = paid_gate_for_row(
        base_row(unit_cost="5.25"),
        ProductGateEvidence(product_set_type="set", marketing_margin_tier=""),
        DEFAULT_AOV_BENCHMARK,
    )
    assert known_set.paid_status == "FIX_BEFORE_PAID"
    assert known_set.paid_eligible is True
    assert known_set.gate_status == "PASSED_WITH_EXCEPTION"
    assert known_set.reasons == ()
    assert "RELIABLE_COST_BASIS" in known_set.exceptions

    product_margin_label_without_cost = paid_gate_for_row(
        base_row(),
        ProductGateEvidence(product_set_type="single", marketing_margin_tier="high"),
        DEFAULT_AOV_BENCHMARK,
    )
    assert product_margin_label_without_cost.paid_status == "EXCLUDE_PAID"
    assert product_margin_label_without_cost.paid_eligible is False
    assert "UNKNOWN_COST_NO_RELIABLE_COST_BASIS" in product_margin_label_without_cost.reasons
    assert "RELIABLE_COST_BASIS" not in product_margin_label_without_cost.exceptions

    repriced_unknown = paid_gate_for_row(
        base_row(price="70.00"),
        ProductGateEvidence(product_set_type="single", marketing_margin_tier=""),
        DEFAULT_AOV_BENCHMARK,
    )
    assert repriced_unknown.paid_status == "EXCLUDE_PAID"
    assert repriced_unknown.paid_eligible is False
    assert repriced_unknown.reasons == ("UNKNOWN_COST_NO_RELIABLE_COST_BASIS",)
    assert "REPRICED_AT_OR_ABOVE_AOV" in repriced_unknown.exceptions

    print("ok")


if __name__ == "__main__":
    main()
