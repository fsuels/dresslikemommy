#!/usr/bin/env python3
"""Repair Golden Daisy localized body translations with a live size-guide table."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "ops/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "ops/scripts"))

from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    RecentProduct,
    ShopifyClient,
    clean,
    collect_resource_snapshots,
    deterministic_option_translation,
    locale_root,
    repair_common_product_html_labels,
    translated_body_label,
    translated_garment,
    translated_role_size_label,
    translated_table_header,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402
from ops.scripts.sync_shopify_translations import DEFAULT_GLOSSARY  # noqa: E402
from ops.scripts.translation_utils import TranslationBackend  # noqa: E402


PRODUCT_GID = "gid://shopify/Product/7546613530721"
HANDLE = "golden-daisy-mommy-and-me-set"
SOURCE_BODY_PATH = ROOT / "ops/listings/body-golden-daisy-mommy-and-me-set.html"
REPORT_PATH = ROOT / "ops/listings/golden-daisy-localized-size-guide-repair-report.json"
CACHE_PATH = ROOT / "ops/content/shopify-product-translation-live-cache.json"
PRODUCT_CONTEXT = {
    "ambiguous_child_role": "girl",
    "has_girl_context": True,
    "has_boy_context": False,
}

SIZE_GUIDE_BLOCK_RE = re.compile(
    r"<h3[^>]*>[\s\S]*?</h3>\s*<table[^>]*(?:id=[\"']size-chart[\"']|class=[\"'][^\"']*size-chart[^\"']*[\"'])[\s\S]*?</table>",
    re.I,
)
SIZE_GUIDE_TABLE_RE = re.compile(
    r"<table[^>]*(?:id=[\"']size-chart[\"']|class=[\"'][^\"']*size-chart[^\"']*[\"'])[\s\S]*?</table>",
    re.I,
)
TH_RE = re.compile(r"<th[^>]*>(.*?)</th>", re.I | re.S)
TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.I | re.S)
TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


HEADER_OVERRIDES: dict[str, dict[str, str]] = {
    "es": {
        "Size": "Talla",
        "Age": "Edad",
        "Weight (kg)": "Peso (kg)",
        "Height (cm)": "Altura (cm)",
        "Top Chest/Bust (cm)": "Pecho/busto del top (cm)",
        "Top Length (cm)": "Largo del top (cm)",
        "Pants Length (cm)": "Largo del pantalón (cm)",
        "Top Hip (cm)": "Cadera del top (cm)",
        "Top Waist (cm)": "Cintura del top (cm)",
        "Pants Waist (cm)": "Cintura del pantalón (cm)",
    },
    "fr": {
        "Size": "Taille",
        "Age": "Âge",
        "Weight (kg)": "Poids (kg)",
        "Height (cm)": "Hauteur (cm)",
        "Top Chest/Bust (cm)": "Poitrine du haut (cm)",
        "Top Length (cm)": "Longueur du haut (cm)",
        "Pants Length (cm)": "Longueur du pantalon (cm)",
        "Top Hip (cm)": "Hanches du haut (cm)",
        "Top Waist (cm)": "Taille du haut (cm)",
        "Pants Waist (cm)": "Taille du pantalon (cm)",
    },
    "it": {
        "Size": "Taglia",
        "Age": "Età",
        "Weight (kg)": "Peso (kg)",
        "Height (cm)": "Altezza (cm)",
        "Top Chest/Bust (cm)": "Torace/busto del top (cm)",
        "Top Length (cm)": "Lunghezza del top (cm)",
        "Pants Length (cm)": "Lunghezza dei pantaloni (cm)",
        "Top Hip (cm)": "Fianchi del top (cm)",
        "Top Waist (cm)": "Vita del top (cm)",
        "Pants Waist (cm)": "Vita dei pantaloni (cm)",
    },
    "pt": {
        "Size": "Tamanho",
        "Age": "Idade",
        "Weight (kg)": "Peso (kg)",
        "Height (cm)": "Altura (cm)",
        "Top Chest/Bust (cm)": "Peito/busto do top (cm)",
        "Top Length (cm)": "Comprimento do top (cm)",
        "Pants Length (cm)": "Comprimento da calça (cm)",
        "Top Hip (cm)": "Quadril do top (cm)",
        "Top Waist (cm)": "Cintura do top (cm)",
        "Pants Waist (cm)": "Cintura da calça (cm)",
    },
    "ro": {
        "Size": "Mărime",
        "Age": "Vârstă",
        "Weight (kg)": "Greutate (kg)",
        "Height (cm)": "Înălțime (cm)",
        "Top Chest/Bust (cm)": "Piept/bust top (cm)",
        "Top Length (cm)": "Lungime top (cm)",
        "Pants Length (cm)": "Lungime pantaloni (cm)",
        "Top Hip (cm)": "Șold top (cm)",
        "Top Waist (cm)": "Talie top (cm)",
        "Pants Waist (cm)": "Talie pantaloni (cm)",
    },
    "de": {
        "Size": "Größe",
        "Age": "Alter",
        "Weight (kg)": "Gewicht (kg)",
        "Height (cm)": "Körpergröße (cm)",
        "Top Chest/Bust (cm)": "Brustweite des Tops (cm)",
        "Top Length (cm)": "Top-Länge (cm)",
        "Pants Length (cm)": "Hosenlänge (cm)",
        "Top Hip (cm)": "Hüftweite des Tops (cm)",
        "Top Waist (cm)": "Taillenweite des Tops (cm)",
        "Pants Waist (cm)": "Taillenweite der Hose (cm)",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locales", default="", help="Comma-separated locale list. Defaults to all published non-primary locales.")
    parser.add_argument("--execute", action="store_true", help="Apply translations to Shopify.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between translationRegister calls.")
    return parser.parse_args()


def text_from_cell(raw: str) -> str:
    return html.unescape(TAG_RE.sub("", raw)).strip()


def source_size_table(source_html: str) -> tuple[list[str], list[list[str]]]:
    table_match = SIZE_GUIDE_TABLE_RE.search(source_html)
    if not table_match:
        raise RuntimeError("Source body has no storefront-readable size-chart table.")
    table_html = table_match.group(0)
    headers = [text_from_cell(match.group(1)) for match in TH_RE.finditer(table_html)]
    rows: list[list[str]] = []
    for row_match in TR_RE.finditer(table_html):
        cells = [text_from_cell(match.group(1)) for match in TD_RE.finditer(row_match.group(0))]
        if cells:
            rows.append(cells)
    if not headers or not rows:
        raise RuntimeError("Source size-chart table is empty.")
    return headers, rows


def localized_header(source_header: str, locale: str) -> str:
    root = locale_root(locale)
    overrides = HEADER_OVERRIDES.get(locale) or HEADER_OVERRIDES.get(root) or {}
    if source_header in overrides:
        return overrides[source_header]

    if source_header == "Size":
        return translated_table_header("size", locale)
    if source_header == "Age":
        return translated_table_header("age", locale)
    if source_header == "Weight (kg)":
        return translated_table_header("weight (kg/lbs)", locale).split("(", 1)[0].strip() + " (kg)"
    if source_header == "Height (cm)":
        return translated_table_header("height (cm/in)", locale).split("(", 1)[0].strip() + " (cm)"

    garment = ""
    measurement = source_header
    if source_header.startswith("Top "):
        garment = translated_garment("Top", locale) or "Top"
        measurement = source_header.removeprefix("Top ")
    elif source_header.startswith("Pants "):
        garment = translated_garment("Pants", locale) or "Pants"
        measurement = source_header.removeprefix("Pants ")

    measurement_key = measurement.lower().replace(" (cm)", " (cm/in)")
    if measurement_key == "length (cm/in)":
        measurement_key = "garment length (cm/in)"
    translated_measurement = translated_table_header(measurement_key, locale)
    translated_measurement = translated_measurement.split("(", 1)[0].strip()
    return f"{garment} {translated_measurement} (cm)".strip()


def localized_size_label(source_label: str, locale: str) -> str:
    return translated_role_size_label(
        source_label,
        locale,
        product_context=PRODUCT_CONTEXT,
        table_child_role="girl",
    ) or source_label


def localized_size_guide_block(source_html: str, locale: str) -> str:
    headers, rows = source_size_table(source_html)
    top_label = translated_garment("Top", locale) or "Top"
    pants_label = translated_garment("Pants", locale) or "Pants"
    heading = f"{translated_body_label('size chart', locale)} - {top_label} + {pants_label}"

    html_rows = []
    for source_row in rows:
        localized_cells = [localized_size_label(source_row[0], locale), *source_row[1:]]
        html_rows.append("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in localized_cells) + "</tr>")

    return "\n".join(
        [
            f"<h3>{html.escape(heading)}</h3>",
            '<table id="size-chart" class="size-chart">',
            "<thead><tr>",
            *[f"<th>{html.escape(localized_header(header, locale))}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *html_rows,
            "</tbody></table>",
        ]
    )


def replace_size_guide_block(translated_html: str, source_html: str, locale: str) -> str:
    replacement = localized_size_guide_block(source_html, locale)
    if SIZE_GUIDE_BLOCK_RE.search(translated_html):
        repaired = SIZE_GUIDE_BLOCK_RE.sub(replacement, translated_html, count=1)
    elif "</ul>" in translated_html:
        repaired = translated_html.replace("</ul>", "</ul>\n" + replacement, 1)
    else:
        repaired = replacement + "\n" + translated_html
    return repair_common_product_html_labels(repaired, locale)


def body_html_digest(product_resource: dict[str, Any]) -> str:
    for row in product_resource.get("translatableContent") or []:
        if row.get("key") == "body_html":
            return clean(row.get("digest"))
    raise RuntimeError("Missing body_html translatableContent digest.")


def fetch_product_state(client: ShopifyClient) -> dict[str, Any]:
    query = """
    query GoldenDaisyLocalizedState($id: ID!) {
      shopLocales { locale primary published }
      product(id: $id) {
        id
        legacyResourceId
        handle
        title
        status
        publishedAt
        onlineStoreUrl
        createdAt
        updatedAt
        resourcePublicationsV2(first: 20) {
          nodes { isPublished publication { name } }
        }
      }
      translatableResource(resourceId: $id) {
        resourceId
        translatableContent { key value digest locale }
      }
    }
    """
    return client.graphql(query, {"id": PRODUCT_GID})


def selected_locales(rows: list[dict[str, Any]], requested: str) -> list[str]:
    if requested:
        return [item.strip() for item in requested.split(",") if item.strip()]
    return [
        clean(row.get("locale"))
        for row in rows
        if clean(row.get("locale")) and row.get("published") and not row.get("primary")
    ]


def register_in_chunks(client: ShopifyClient, resource_id: str, translations: list[dict[str, str]], pause_ms: int) -> int:
    count = 0
    for index in range(0, len(translations), 5):
        chunk = translations[index : index + 5]
        result = client.register_translations(resource_id, chunk)
        count += len(result.get("translations") or [])
        if pause_ms > 0 and index + 5 < len(translations):
            time.sleep(pause_ms / 1000)
    return count


def option_translation_payloads(client: ShopifyClient, product: RecentProduct, locales: list[str]) -> dict[str, list[dict[str, str]]]:
    snapshots = collect_resource_snapshots(client, PRODUCT_GID, locales, 100)
    payloads: dict[str, list[dict[str, str]]] = {}
    for snapshot in snapshots:
        if snapshot.resource_type not in {"ProductOption", "ProductOptionValue"}:
            continue
        for item in snapshot.translatable_content:
            key = clean(item.get("key"))
            value = item.get("value") or ""
            translated_by_locale = {}
            for locale in locales:
                translated = deterministic_option_translation(
                    snapshot.resource_type,
                    key,
                    value,
                    locale,
                    product_context=PRODUCT_CONTEXT,
                )
                if not translated:
                    continue
                existing = snapshot.existing_translations.get((locale, key))
                if existing and not existing.outdated and clean(existing.value) == clean(translated):
                    continue
                translated_by_locale[locale] = translated
            for locale, translated in translated_by_locale.items():
                payloads.setdefault(snapshot.resource_id, []).append(
                    {
                        "locale": locale,
                        "key": key,
                        "value": translated,
                        "translatableContentDigest": clean(item.get("digest")),
                    }
                )
    return payloads


def translation_checks(body_by_locale: dict[str, str]) -> dict[str, Any]:
    checks = {}
    for locale, body in body_by_locale.items():
        table_match = SIZE_GUIDE_TABLE_RE.search(body)
        table_html = table_match.group(0) if table_match else ""
        first_cells = [
            text_from_cell(match.group(1))
            for match in re.finditer(r"<tr>\s*<td[^>]*>(.*?)</td>", table_html, re.I | re.S)
        ]
        checks[locale] = {
            "has_size_chart": bool(table_match),
            "row_count": table_html.count("<tr>") - 1 if table_html else 0,
            "first_cells": first_cells,
            "header_count": len(list(TH_RE.finditer(table_html))),
            "length": len(body),
            "forbidden_source_tokens": [
                token
                for token in ["1688", "Alibaba", "detail.1688.com"]
                if token.lower() in body.lower()
            ],
        }
    return checks


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    client = ShopifyClient(store_domain, load_access_token())
    state = fetch_product_state(client)
    product_node = state["product"]
    if product_node["handle"] != HANDLE:
        raise RuntimeError(f"Unexpected product handle: {product_node['handle']}")

    locales = selected_locales(state["shopLocales"], args.locales)
    if not locales:
        raise RuntimeError("No target locales resolved.")

    source_html = SOURCE_BODY_PATH.read_text(encoding="utf-8")
    source_size_table(source_html)
    digest = body_html_digest(state["translatableResource"])
    translator = TranslationBackend(
        CACHE_PATH,
        DEFAULT_GLOSSARY,
        batch_size=60,
        pause_seconds=0.05,
        request_timeout=15,
        batch_char_limit=12000,
    )

    body_by_locale: dict[str, str] = {}
    for locale in locales:
        translated = translator.translate_many(locale, [source_html], progress_label=f"golden-daisy-body locale={locale}")[source_html]
        body_by_locale[locale] = replace_size_guide_block(translated or source_html, source_html, locale)

    body_translations = [
        {
            "locale": locale,
            "key": "body_html",
            "value": body,
            "translatableContentDigest": digest,
        }
        for locale, body in body_by_locale.items()
    ]

    product = RecentProduct(
        product_gid=PRODUCT_GID,
        product_id=clean(product_node.get("legacyResourceId")),
        handle=HANDLE,
        title=clean(product_node.get("title")),
        status=clean(product_node.get("status")),
        created_at=clean(product_node.get("createdAt")),
        updated_at=clean(product_node.get("updatedAt")),
    )
    option_payloads = option_translation_payloads(client, product, locales)

    registered = {"body_html": 0, "option_resources": {}}
    if args.execute:
        registered["body_html"] = register_in_chunks(client, PRODUCT_GID, body_translations, max(args.pause_ms, 0))
        for resource_id, translations in option_payloads.items():
            registered["option_resources"][resource_id] = register_in_chunks(client, resource_id, translations, max(args.pause_ms, 0))

    live_publications = sorted(
        node["publication"]["name"]
        for node in product_node["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    )
    report = {
        "execute": bool(args.execute),
        "store_domain": store_domain,
        "product_gid": PRODUCT_GID,
        "handle": HANDLE,
        "status": product_node["status"],
        "published_at": product_node["publishedAt"],
        "online_store_url": product_node["onlineStoreUrl"],
        "live_publications": live_publications,
        "locales": locales,
        "body_translation_count": len(body_translations),
        "option_resource_count": len(option_payloads),
        "option_translation_count": sum(len(rows) for rows in option_payloads.values()),
        "registered": registered,
        "checks": translation_checks(body_by_locale),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
