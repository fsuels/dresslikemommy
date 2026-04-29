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
    POST_GATE_ADS_STRUCTURE,
    build_master_row,
    build_rows,
    derive_product_family,
    render_ads_structure_table,
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

    non_us = build_master_row(
        base_row(merchant_center_id="shopify_CA_1_2"),
        passing_merchant(),
        Evidence({"pdp_status": "PASS"}),
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )
    assert non_us["market"] == "CA"
    assert non_us["paid_eligible"] == "FALSE"
    assert non_us["fix_before_paid"] == "FALSE"
    assert non_us["custom_label_0"] == "international_exclude"
    assert non_us["custom_label_4"] == "international_exclude"
    assert "international_exclude_ca" in non_us["exclusion_reason"]

    duplicate_rows = build_rows(
        [
            base_row(product_id="1", variant_id="2", merchant_center_id="shopify_US_1_2"),
            base_row(product_id="1", variant_id="3", merchant_center_id="shopify_US_1_3"),
        ],
        {
            "shopify_US_1_2": passing_merchant(),
            "shopify_US_1_3": passing_merchant(),
        },
        {
            "shopify_US_1_2": Evidence({"pdp_status": "PASS"}),
            "shopify_US_1_3": Evidence({"pdp_status": "PASS"}),
        },
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )
    assert all(row["paid_eligible"] == "FALSE" for row in duplicate_rows)
    assert all(row["fix_before_paid"] == "TRUE" for row in duplicate_rows)
    assert all("exclude_duplicate_sku" in row["exclusion_reason"] for row in duplicate_rows)
    assert all("exclude_duplicate_gtin" in row["exclusion_reason"] for row in duplicate_rows)

    ads_structure = render_ads_structure_table(POST_GATE_ADS_STRUCTURE)
    ads_structure_text = "\n".join(ads_structure)
    assert "Brand Search — USA" in ads_structure_text
    assert "Standard Shopping — USA eligible products" in ads_structure_text
    assert "PMax — USA eligible products" in ads_structure_text
    assert "Non-brand Search" in ads_structure_text
    assert "Remarketing" in ads_structure_text
    assert "Exclude UNKNOWN_MARGIN, FIX_BEFORE_PAID, limited, and not-approved products." in ads_structure_text
    assert "URL expansion off unless an approved landing-page map exists." in ads_structure_text
    assert "Exclude pages not READY_FOR_PAID." in ads_structure_text
    assert "Do not use current limited ads." in ads_structure_text

    print("ok")


if __name__ == "__main__":
    main()
