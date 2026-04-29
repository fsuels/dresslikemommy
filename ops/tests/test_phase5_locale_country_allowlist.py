#!/usr/bin/env python3
"""Regression checks for Phase 5 localization and US-only paid gates."""

from __future__ import annotations

import json
import re
import sys
import csv
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.build_google_shopping_us_clean_subset import (  # noqa: E402
    Evidence,
    build_master_row,
)
from ops.scripts.translation_utils import get_path, read_shopify_json  # noqa: E402


RAW_PLACEHOLDER_RE = re.compile(
    r"__DLM[A-Z]*TOK\d+_+|QZXTOKEN\d+QXZ|DLMTOKEN\d+XYZ|translation missing",
    re.I,
)

POLICY_HTML_KEYS = [
    "sections.cart.taxes_and_shipping_policy_at_checkout_html",
    "sections.cart.taxes_included_and_shipping_policy_html",
    "products.product.shipping_policy_html",
]

COPY_MAP_REQUIRED_KEYS = [
    "back_to_results",
    "back_to_context",
    "back_to_family_sets",
    "back_to_search_results",
    "view_similar_styles",
    "view_similar_styles_in",
    "similar_styles",
    "browse_more_from",
    "browse_similar_styles",
    "compare_collection_copy",
    "free_shipping_label",
    "standard_delivery_window",
    "premium_delivery_window",
]


def iter_theme_locale_paths() -> list[Path]:
    return sorted(
        path
        for path in (REPO_ROOT / "locales").glob("*.json")
        if not path.name.endswith(".schema.json")
    )


def walk_strings(node: object):
    if isinstance(node, dict):
        for value in node.values():
            yield from walk_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_strings(value)
    elif isinstance(node, str):
        yield node


def load_copy_map() -> dict[str, dict[str, str]]:
    raw = (REPO_ROOT / "snippets/product-page-copy-map.liquid").read_text(encoding="utf-8")
    raw = re.sub(r"^\{% comment %\}.*?\{% endcomment %\}\s*", "", raw, flags=re.S)
    return json.loads(raw)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_locale_files_have_no_raw_placeholder_tokens():
    for path in iter_theme_locale_paths():
        _header, data = read_shopify_json(path)
        for value in walk_strings(data):
            assert not RAW_PLACEHOLDER_RE.search(value), f"{path.name}: {value}"


def test_policy_html_keeps_shopify_link_and_balanced_anchor_markup():
    for path in iter_theme_locale_paths():
        _header, data = read_shopify_json(path)
        for key in POLICY_HTML_KEYS:
            value = get_path(data, key)
            assert value.count("<a") == value.count("</a>"), f"{path.name}:{key}"
            assert "{{ link }}" in value, f"{path.name}:{key}"


def test_product_page_copy_map_has_localized_navigation_and_policy_copy():
    copy_map = load_copy_map()
    assert "en" in copy_map
    assert len(copy_map) >= 35

    for locale, values in copy_map.items():
        for key in COPY_MAP_REQUIRED_KEYS:
            assert values.get(key), f"{locale}:{key}"
            assert not RAW_PLACEHOLDER_RE.search(values[key]), f"{locale}:{key}"


def test_non_us_market_rows_are_never_paid_eligible():
    row = {
        "merchant_center_id": "shopify_GB_1_2",
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
    merchant = Evidence(
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
    result = build_master_row(
        row,
        merchant,
        Evidence({"pdp_status": "PASS"}),
        aov=Decimal("63.25"),
        storefront_base_url="https://www.dresslikemommy.com",
    )

    assert result["market"] == "GB"
    assert result["paid_eligible"] == "FALSE"
    assert result["custom_label_0"] == "international_exclude"
    assert result["custom_label_4"] == "international_exclude"
    assert "international_exclude_gb" in result["exclusion_reason"]


def test_non_us_country_exclusion_upload_file_preserves_us():
    path = (
        REPO_ROOT
        / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
        / "2026-04-28-merchant-diagnostics-priority-triage/"
        / "shopping_ads_us_only_country_exclusions_UPLOAD_APPROVED.csv"
    )
    rows = read_csv(path)
    excluded_countries: set[str] = set()

    for row in rows:
        countries = [
            value.strip()
            for value in row["shopping_ads_excluded_country"].split(",")
            if value.strip()
        ]
        assert countries, row["id"]
        assert "US" not in countries, row["id"]
        excluded_countries.update(countries)

    assert len(rows) == 7063
    assert len(excluded_countries) == 42
    assert "US" not in excluded_countries


if __name__ == "__main__":
    test_locale_files_have_no_raw_placeholder_tokens()
    test_policy_html_keeps_shopify_link_and_balanced_anchor_markup()
    test_product_page_copy_map_has_localized_navigation_and_policy_copy()
    test_non_us_market_rows_are_never_paid_eligible()
    test_non_us_country_exclusion_upload_file_preserves_us()
    print("ok")
