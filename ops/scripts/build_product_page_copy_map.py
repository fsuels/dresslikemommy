#!/usr/bin/env python3
"""Regenerate the product-page fallback copy map from theme locale JSON files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
LOCALES_DIR = ROOT / "locales"
OUTPUT = ROOT / "snippets" / "product-page-copy-map.liquid"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from translation_utils import get_path, read_shopify_json  # noqa: E402


COPY_KEYS = [
    ("matching_set_heading", "products.product.matching_set.heading"),
    ("matching_set_copy", "products.product.matching_set.copy"),
    ("matching_set_empty", "products.product.matching_set.empty"),
    ("matching_set_add", "products.product.matching_set.add"),
    ("matching_set_success", "products.product.matching_set.success"),
    ("matching_set_error", "products.product.matching_set.error"),
    ("grouped_size_guide_label", "products.product.size_guide.compare_family_sizes"),
    ("compare_size_guide_label", "products.product.size_guide.compare_all_sizes"),
    ("single_size_guide_label", "products.product.size_guide.guide_and_fit"),
    ("selected_size_guide_label", "products.product.size_guide.your_size_details"),
    ("size_guide_compare_hint", "products.product.size_guide.compare_hint"),
    ("size_guide_unit_toggle_label", "products.product.size_guide.chart_units"),
    ("reviews_heading", "products.product.reviews.heading"),
    ("photo_heading", "products.product.reviews.photo_heading"),
    ("jump_to_reviews", "products.product.reviews.jump_to_reviews"),
    ("secure_checkout", "products.trust.secure_checkout"),
    ("returns", "products.trust.returns"),
    ("trusted_since", "products.trust.trusted_since"),
    ("assistance_note", "products.trust.assistance_note"),
    ("complete_the_look", "sections.cart.complete_the_look"),
    ("popular_with_families", "sections.cart.popular_with_families"),
    ("recently_viewed", "sections.cart.recently_viewed"),
    ("back_to_results", "sections.product_navigation.back_to_results"),
    ("back_to_context", "sections.product_navigation.back_to_context"),
    ("back_to_family_sets", "sections.product_navigation.back_to_family_sets"),
    ("back_to_search_results", "sections.product_navigation.back_to_search_results"),
    ("view_similar_styles", "sections.product_navigation.view_similar_styles"),
    ("view_similar_styles_in", "sections.product_navigation.view_similar_styles_in"),
    ("similar_styles", "sections.product_navigation.similar_styles"),
    ("browse_more_from", "sections.product_navigation.browse_more_from"),
    ("browse_similar_styles", "sections.product_navigation.browse_similar_styles"),
    ("compare_collection_copy", "sections.product_navigation.compare_collection_copy"),
    ("shipping_title", "products.additional_info.shipping_title"),
    ("free_shipping_label", "products.additional_info.free_shipping_label"),
    ("estimated_delivery", "products.additional_info.estimated_delivery"),
    ("standard_delivery_window", "products.additional_info.standard_delivery_window"),
    ("premium_delivery_window", "products.additional_info.premium_delivery_window"),
    ("faster_shipping_prefix", "products.additional_info.faster_shipping_prefix"),
    ("free_premium_shipping", "products.additional_info.free_premium_shipping"),
    ("return_policy_title", "products.additional_info.return_policy_title"),
    ("return_policy_line_1", "products.additional_info.return_policy_line_1"),
    ("return_policy_line_2", "products.additional_info.return_policy_line_2"),
    ("return_policy_line_3", "products.additional_info.return_policy_line_3"),
    ("return_policy_line_4", "products.additional_info.return_policy_line_4"),
    ("shopping_security_title", "products.additional_info.shopping_security_title"),
    ("safe_payment_options_title", "products.additional_info.safe_payment_options_title"),
    ("safe_payment_description", "products.additional_info.safe_payment_description"),
    ("secure_logistics_title", "products.additional_info.secure_logistics_title"),
    ("secure_logistics_line_1", "products.additional_info.secure_logistics_line_1"),
    ("secure_logistics_line_2", "products.additional_info.secure_logistics_line_2"),
    ("secure_privacy_title", "products.additional_info.secure_privacy_title"),
    ("secure_privacy_description", "products.additional_info.secure_privacy_description"),
    ("review_widget_heading_uppercase", "products.product.review_widget.heading_uppercase"),
    ("review_widget_heading", "products.product.review_widget.heading"),
    ("review_widget_empty", "products.product.review_widget.empty"),
    ("review_widget_write_review", "products.product.review_widget.write_review"),
    ("review_widget_write_review_title", "products.product.review_widget.write_review_title"),
    ("free_shipping_all_orders", "products.product.free_shipping_all_orders"),
    ("selected_size_label", "products.product.selected_size_label"),
    ("compare_at_price", "products.product.price.compare_at_price"),
    ("description_details_eyebrow", "products.product.description_sections.details_eyebrow"),
    ("description_highlights_heading", "products.product.description_sections.highlights_heading"),
    ("description_size_chart_heading", "products.product.description_sections.size_chart_heading"),
    ("description_product_details_heading", "products.product.description_sections.product_details_heading"),
    ("description_size_chart_meta", "products.product.description_sections.size_chart_meta"),
    ("description_product_details_meta", "products.product.description_sections.product_details_meta"),
]


def locale_code(path: Path) -> str:
    return "en" if path.name == "en.default.json" else path.stem


def locale_paths() -> list[Path]:
    return sorted(
        path
        for path in LOCALES_DIR.glob("*.json")
        if not path.name.endswith(".schema.json")
    )


def missing_or_raw(value: object) -> bool:
    text = str(value or "")
    return not text.strip() or "translation missing" in text.lower()


def build_map() -> dict[str, dict[str, str]]:
    _, en_data = read_shopify_json(LOCALES_DIR / "en.default.json")
    out: dict[str, dict[str, str]] = {}

    for path in locale_paths():
        _, data = read_shopify_json(path)
        locale_values: dict[str, str] = {}
        for output_key, dotted in COPY_KEYS:
            try:
                value = get_path(data, dotted)
            except KeyError:
                value = get_path(en_data, dotted)
            if missing_or_raw(value):
                value = get_path(en_data, dotted)
            locale_values[output_key] = str(value)
        out[locale_code(path)] = locale_values
    return out


def main() -> None:
    copy_map = build_map()
    payload = json.dumps(copy_map, indent=2, ensure_ascii=False)
    payload = re.sub(r"</script", r"<\\/script", payload, flags=re.I)
    OUTPUT.write_text(
        "{% comment %} Generated from locale JSONs for product-page fallback copy. {% endcomment %}\n"
        f"{payload}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT} with {len(copy_map)} locales")


if __name__ == "__main__":
    main()
