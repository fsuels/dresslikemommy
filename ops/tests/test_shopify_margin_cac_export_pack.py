#!/usr/bin/env python3
"""Regression checks for the read-only Shopify margin/CAC packet builder."""

from __future__ import annotations

import sys
import tempfile
import zipfile
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_shopify_margin_cac_export_pack import (  # noqa: E402
    DEFAULT_AOV_BENCHMARK,
    tier_for_product,
    write_xlsx,
)


def main() -> None:
    tier, reason = tier_for_product(
        sales_orders=2,
        observed_aov=Decimal("80.00"),
        refund_rate=Decimal("0"),
        contribution_after_max_marketing=Decimal("28.00"),
        missing_unit_cost_variants=0,
        sellable_variant_count=3,
        aov_benchmark=DEFAULT_AOV_BENCHMARK,
    )
    assert tier == "A"
    assert reason == "CANDIDATE_FOR_PAUSED_BUILDOUT_REVIEW"

    tier, reason = tier_for_product(
        sales_orders=0,
        observed_aov=Decimal("0"),
        refund_rate=Decimal("0"),
        contribution_after_max_marketing=Decimal("0"),
        missing_unit_cost_variants=0,
        sellable_variant_count=2,
        aov_benchmark=DEFAULT_AOV_BENCHMARK,
    )
    assert tier == "D"
    assert reason == "NEEDS_ORDER_DATA"

    tier, reason = tier_for_product(
        sales_orders=3,
        observed_aov=Decimal("90.00"),
        refund_rate=Decimal("0"),
        contribution_after_max_marketing=Decimal("30.00"),
        missing_unit_cost_variants=1,
        sellable_variant_count=2,
        aov_benchmark=DEFAULT_AOV_BENCHMARK,
    )
    assert tier == "D"
    assert reason == "NEEDS_COST_DATA"

    with tempfile.TemporaryDirectory() as tmp:
        workbook_path = Path(tmp) / "check.xlsx"
        write_xlsx(
            workbook_path,
            [
                ("Command_Center", [["Metric", "Value"], ["Target ROAS", "6.6667"]]),
                ("Product_CAC_Model", [["handle", "tier"], ["example", "A"]]),
            ],
        )
        with zipfile.ZipFile(workbook_path) as zf:
            names = set(zf.namelist())
            assert "[Content_Types].xml" in names
            assert "xl/workbook.xml" in names
            assert "xl/worksheets/sheet1.xml" in names
            assert "xl/worksheets/sheet2.xml" in names
            zf.testzip() is None

    print("ok")


if __name__ == "__main__":
    main()
