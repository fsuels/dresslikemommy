#!/usr/bin/env python3
import argparse
from pathlib import Path

from translation_utils import TranslationBackend, read_shopify_json, write_shopify_json


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "locales" / "en.default.json"
DEFAULT_GLOSSARY = ROOT / "ops" / "content" / "translation_glossary.json"
DEFAULT_CONTENT_DIR = ROOT / "ops" / "content"
DEFAULT_LOCALES_DIR = ROOT / "locales"


def collect_strings(node, values):
    if isinstance(node, dict):
        for child in node.values():
            collect_strings(child, values)
        return
    if isinstance(node, list):
        for child in node:
            collect_strings(child, values)
        return
    if isinstance(node, str) and node:
        values.append(node)


def apply_translations(node, translations):
    if isinstance(node, dict):
        return {key: apply_translations(value, translations) for key, value in node.items()}
    if isinstance(node, list):
        return [apply_translations(value, translations) for value in node]
    if isinstance(node, str):
        return translations.get(node, node)
    return node


def main():
    parser = argparse.ArgumentParser(description="Build a full Shopify theme locale file from en.default.json.")
    parser.add_argument("--locales", required=True, help="Comma-separated locale list, e.g. ar,hi")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    parser.add_argument("--cache-dir", default=str(DEFAULT_CONTENT_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_LOCALES_DIR))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    source_path = Path(args.source)
    cache_dir = Path(args.cache_dir)
    output_dir = Path(args.output_dir)
    header, source_data = read_shopify_json(source_path)

    values = []
    collect_strings(source_data, values)
    unique_strings = list(dict.fromkeys(values))

    locales = [locale.strip() for locale in args.locales.split(",") if locale.strip()]
    for locale in locales:
        output_path = output_dir / f"{locale}.json"
        if output_path.exists() and not args.force:
            raise SystemExit(f"{output_path} already exists. Pass --force to overwrite.")

        cache_path = cache_dir / f"theme-locale-cache-{locale}.json"
        translator = TranslationBackend(
            cache_path,
            args.glossary,
            batch_size=60,
            pause_seconds=0.05,
            request_timeout=15,
            batch_char_limit=12000,
        )
        translated = translator.translate_many(locale, unique_strings)
        locale_data = apply_translations(source_data, translated)
        write_shopify_json(output_path, header, locale_data)
        print(f"{locale}: wrote {output_path} with {len(unique_strings)} translated strings")


if __name__ == "__main__":
    main()
