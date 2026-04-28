#!/usr/bin/env python3
"""Regression checks for the Google Shopping clean-subset builder."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_google_shopping_us_clean_subset import (  # noqa: E402
    Evidence,
    build_master_row,
    derive_product_family,
)


def base_row(**overrides: str) -> dict[str, str]:
    row = {
        "merchant_center_id": "shopify_US_1_2",
        "product_id": "1",
        "variant_id": "2",
        "handle": "mommy-and-me-floral-dresses",
        "product_title": "Mommy and Me Floral Dresses",
        "variant_title": "Mother M",
        "sku": "MOM-M",
        "barcode": "1234567890123",
        "price": "40.00",
        "unit_cost": "20.00",
        "inventory_quantity": "5",
        "marketing_product_set_type": "set",
    }
    row.update(overrides)
    return row


def passing_merchant() -> Evidence:
    return Evidence(
        {
            "merchant_center_status": "Approved",
            "merchant_center_destination": "Shopping ads eligible",
            "merchant_center_issue_count": "0",
            "merchant_center_issues": "",
            "image_status": "processed",
            "price_status": "pass",
            "availability_status": "pass",
            "shipping_policy_status": "configured",
            "return_policy_status": "configured",
            "image_url": "https://example.com/image.jpg",
        }
    )


def main() -> None:
    assert derive_product_family(base_row(handle="family-matching-pajamas")) == "pajamas"
    assert derive_product_family(base_row(handle="daddy-and-me-shirt")) == "daddy_me"
    assert derive_product_family(base_row(handle="mother-daughter-swimsuit")) == "swimsuits"

    needs_data = build_master_row(
        base_row(),
        None,
        None,
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )
    assert needs_data["paid_eligible"] == "FALSE"
    assert needs_data["fix_before_paid"] == "TRUE"
    assert needs_data["custom_label_0"] == "exclude_feed_issue"
    assert needs_data["custom_label_1"] == "margin_medium"
    assert needs_data["custom_label_2"] == "mommy_me"
    assert needs_data["custom_label_3"] == "aov_medium"
    assert needs_data["custom_label_4"] == "us_fix_before_paid"
    assert "needs_merchant_center_status" in needs_data["exclusion_reason"]
    assert "needs_pdp_verification" in needs_data["exclusion_reason"]

    local_blocker = build_master_row(
        base_row(sku="", barcode="", inventory_quantity="0"),
        passing_merchant(),
        Evidence({"pdp_status": "PASS"}),
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )
    assert local_blocker["paid_eligible"] == "FALSE"
    assert "exclude_missing_sku" in local_blocker["exclusion_reason"]
    assert "exclude_missing_gtin" in local_blocker["exclusion_reason"]
    assert "exclude_out_of_stock" in local_blocker["exclusion_reason"]

    clean = build_master_row(
        base_row(),
        passing_merchant(),
        Evidence({"pdp_status": "PASS"}),
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )
    assert clean["paid_eligible"] == "TRUE"
    assert clean["fix_before_paid"] == "FALSE"
    assert clean["custom_label_0"] == "paid_eligible"
    assert clean["custom_label_4"] == "us_test_ready"

    print("ok")


if __name__ == "__main__":
    main()
