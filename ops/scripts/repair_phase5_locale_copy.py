#!/usr/bin/env python3
"""Repair Phase 5 locale strings that affect paid-country readiness.

This script keeps the current English locale as the source of truth, refreshes
the translated storefront/policy strings that changed for the US-first paid
gate, and replaces older malformed placeholder tokens in Arabic locale values.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
LOCALES_DIR = ROOT / "locales"
DEFAULT_CACHE = ROOT / "ops" / "tmp" / "phase5-locale-cache.json"
DEFAULT_GLOSSARY = ROOT / "ops" / "content" / "translation_glossary.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from translation_utils import (  # noqa: E402
    TranslationBackend,
    get_path,
    read_shopify_json,
    set_path,
    write_shopify_json,
)


PHASE5_SYNC_KEYS = [
    "products.product.shipping_policy_html",
    "products.product.matching_set.copy",
    "products.product.matching_set.empty",
    "products.product.matching_set.add",
    "products.product.free_shipping_all_orders",
    "products.trust.returns",
    "products.trust.free_shipping",
    "products.additional_info.free_shipping_label",
    "products.additional_info.estimated_delivery",
    "products.additional_info.standard_delivery_window",
    "products.additional_info.premium_delivery_window",
    "products.additional_info.free_premium_shipping",
    "products.additional_info.secure_logistics_line_2",
    "sections.announcements.default_promo",
    "sections.cart.taxes_and_shipping_policy_at_checkout_html",
    "sections.cart.taxes_included_but_shipping_at_checkout",
    "sections.cart.taxes_included_and_shipping_policy_html",
    "sections.cart.taxes_and_shipping_at_checkout",
    "sections.cart.trust.free_shipping",
    "sections.cart.trust.returns",
    "sections.cart.trust.free_ship",
    "sections.cart.shipping_free",
]

AR_PLACEHOLDER_KEYS = [
    "blogs.article.comments.one",
    "blogs.article.comments.other",
    "products.facets.filters_selected.one",
    "products.facets.filters_selected.other",
    "products.facets.filter_selected_accessibility",
    "products.facets.max_price",
    "templates.search.results_with_count.other",
    "sections.featured_collection.view_all_label",
    "sections.collection_template.use_fewer_filters_html",
    "sections.quick_order_list.items_added.one",
    "sections.quick_order_list.items_added.other",
    "localization.country_results_count",
    "customer.order.cancelled_html",
    "customer.order.fulfilled_at_html",
]

EXTRA_DELIVERY_KEY_SOURCES = {
    "shopify.checkout.thank_you.standard_delivery_window": "products.additional_info.standard_delivery_window",
    "shopify.checkout.thank_you.premium_delivery_window": "products.additional_info.premium_delivery_window",
}


def locale_paths(locales: set[str]) -> list[Path]:
    paths = sorted(
        path
        for path in LOCALES_DIR.glob("*.json")
        if not path.name.endswith(".schema.json") and path.name != "en.default.json"
    )
    if not locales:
        return paths
    return [path for path in paths if path.stem in locales]


def path_exists(data: dict, dotted: str) -> bool:
    try:
        get_path(data, dotted)
    except KeyError:
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    parser.add_argument("--locales", default="", help="Optional comma-separated locale allowlist.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    _, en_data = read_shopify_json(LOCALES_DIR / "en.default.json")
    allowed = {value.strip() for value in args.locales.split(",") if value.strip()}
    translator = TranslationBackend(
        args.cache,
        args.glossary,
        batch_size=24,
        pause_seconds=0.05,
        request_timeout=20,
        batch_char_limit=7000,
    )

    updated_files = 0
    updated_keys = 0

    for path in locale_paths(allowed):
        locale = path.stem
        header, data = read_shopify_json(path)
        repairs: list[tuple[str, str]] = []

        for dotted in PHASE5_SYNC_KEYS:
            repairs.append((dotted, get_path(en_data, dotted)))

        if locale == "ar":
            for dotted in AR_PLACEHOLDER_KEYS:
                repairs.append((dotted, get_path(en_data, dotted)))

        for target_path, source_path in EXTRA_DELIVERY_KEY_SOURCES.items():
            if path_exists(data, target_path):
                repairs.append((target_path, get_path(en_data, source_path)))

        source_texts = list(dict.fromkeys(source for _, source in repairs))
        translated = translator.translate_many(locale, source_texts, progress_label=f"phase5:{locale}")

        file_updates = 0
        for dotted, source in repairs:
            value = translated.get(source) or source
            try:
                current = get_path(data, dotted)
            except KeyError:
                current = None
            if current == value:
                continue
            set_path(data, dotted, value)
            file_updates += 1

        if file_updates:
            updated_files += 1
            updated_keys += file_updates
            if not args.dry_run:
                write_shopify_json(path, header, data)
            print(f"{path.name}: repaired {file_updates} keys")

    print(f"updated_files={updated_files} updated_keys={updated_keys}")


if __name__ == "__main__":
    main()
