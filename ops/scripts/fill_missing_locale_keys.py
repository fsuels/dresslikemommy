#!/usr/bin/env python3
import argparse
from pathlib import Path

from translation_utils import get_path, read_shopify_json, set_path, TranslationBackend, write_shopify_json


ROOT = Path(__file__).resolve().parents[2]
LOCALES_DIR = ROOT / "locales"
EN_PATH = LOCALES_DIR / "en.default.json"
DEFAULT_CACHE = ROOT / "ops" / "content" / "theme-locale-key-cache.json"
DEFAULT_GLOSSARY = ROOT / "ops" / "content" / "translation_glossary.json"


ALIASES = {
    "general.breadcrumbs.home": ["sections.breadcrumbs.home"],
    "sections.breadcrumbs.home": ["general.breadcrumbs.home"],
    "shopify.page_titles.search": ["general.search.search"],
}


def flatten_missing_keys():
    _, en_data = read_shopify_json(EN_PATH)
    locale_paths = sorted(
        path for path in LOCALES_DIR.glob("*.json")
        if not path.name.endswith(".schema.json") and path.name != "en.default.json"
    )

    for path in locale_paths:
        header, data = read_shopify_json(path)
        missing = []
        for dotted in MISSING_KEYS:
            try:
                get_path(data, dotted)
            except KeyError:
                missing.append(dotted)
        yield path, header, data, en_data, missing


MISSING_KEYS = [
    "general.breadcrumbs.home",
    "products.product.select_size",
    "products.product.select_color",
    "products.product.size_required_message",
    "sections.cart.discount_code_toggle",
    "sections.cart.shipping_label",
    "sections.cart.shipping_free",
    "sections.breadcrumbs.home",
    "sections.breadcrumbs.cat_mommy_me",
    "sections.breadcrumbs.cat_daddy_me",
    "sections.breadcrumbs.cat_couples",
    "sections.breadcrumbs.cat_maternity",
    "sections.breadcrumbs.cat_family_matching",
    "sections.breadcrumbs.label_swimsuits",
    "sections.breadcrumbs.label_sets",
    "sections.breadcrumbs.label_tops",
    "sections.breadcrumbs.label_sweaters",
    "sections.breadcrumbs.label_pajamas",
    "sections.breadcrumbs.label_tshirts",
    "sections.breadcrumbs.label_trunks",
    "sections.breadcrumbs.label_daddy_tshirts",
    "sections.breadcrumbs.prefix_mother_daughter",
    "sections.breadcrumbs.prefix_mommy_me",
    "sections.breadcrumbs.prefix_matching",
    "sections.breadcrumbs.prefix_daddy_me",
    "sections.breadcrumbs.prefix_family_matching",
    "sections.collection.swimsuits_override",
    "shopify.page_titles.search",
]


def resolve_alias(data, dotted):
    for alias in ALIASES.get(dotted, []):
        try:
            return get_path(data, alias)
        except KeyError:
            continue
    raise KeyError(dotted)


def main():
    parser = argparse.ArgumentParser(description="Fill missing Shopify locale keys with translated values.")
    parser.add_argument("--cache", default=str(DEFAULT_CACHE))
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    parser.add_argument("--locales", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    translator = TranslationBackend(args.cache, args.glossary, batch_size=20, pause_seconds=0.15)
    updated_files = 0
    inserted_keys = 0
    allowed = {item.strip() for item in args.locales.split(",") if item.strip()}

    for path, header, data, en_data, missing in flatten_missing_keys():
        if allowed and path.stem not in allowed:
            continue
        if not missing:
            continue
        locale = path.stem
        file_updates = 0
        pending = {}

        for dotted in missing:
            try:
                value = resolve_alias(data, dotted)
                set_path(data, dotted, value)
                file_updates += 1
            except KeyError:
                pending[dotted] = get_path(en_data, dotted)

        if pending:
            translated = translator.translate_many(locale, list(dict.fromkeys(pending.values())))
            for dotted, source in pending.items():
                value = translated[source]
                set_path(data, dotted, value)
                file_updates += 1

        if file_updates:
            updated_files += 1
            inserted_keys += file_updates
            if not args.dry_run:
                write_shopify_json(path, header, data)
            print(f"{path.name}: inserted {file_updates} keys")

    print(f"updated_files={updated_files} inserted_keys={inserted_keys}")


if __name__ == "__main__":
    main()
