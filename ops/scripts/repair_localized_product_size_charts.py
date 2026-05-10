#!/usr/bin/env python3
"""Audit and repair localized Shopify product body size-chart coverage.

This script is intentionally narrow: it only registers Product `body_html`
translations for active products whose English/source description has a
`size-chart` table and whose existing published-locale body translation is
missing that table.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    RecentProduct,
    ShopifyClient,
    clean,
    ensure_product_html_size_chart_coverage,
    has_complete_size_chart_table_coverage,
    has_size_chart_table,
    infer_product_context,
    rebuild_product_html_size_chart_tables_from_source,
    resolve_target_locales,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


ACTIVE_PRODUCTS_QUERY = """
query ActiveProducts($first: Int!, $after: String, $query: String!) {
  products(first: $first, after: $after, query: $query) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        legacyResourceId
        handle
        title
        status
        createdAt
        updatedAt
        descriptionHtml
      }
    }
  }
}
"""


def active_products(client: ShopifyClient, *, page_size: int, max_products: int, handles: list[str]) -> list[dict[str, Any]]:
    if handles:
        rows: list[dict[str, Any]] = []
        query = """
        query ProductByHandle($handle: String!) {
          productByHandle(handle: $handle) {
            id
            legacyResourceId
            handle
            title
            status
            createdAt
            updatedAt
            descriptionHtml
          }
        }
        """
        for handle in handles:
            product = client.graphql(query, {"handle": handle}).get("productByHandle")
            if product:
                rows.append(product)
        return rows

    rows = []
    after = None
    while True:
        page = client.graphql(
            ACTIVE_PRODUCTS_QUERY,
            {"first": max(1, page_size), "after": after, "query": "status:active"},
        )["products"]
        for edge in page.get("edges") or []:
            node = edge.get("node") or {}
            if clean(node.get("status")).upper() == "ACTIVE":
                rows.append(node)
            if max_products > 0 and len(rows) >= max_products:
                return rows

        if not page.get("pageInfo", {}).get("hasNextPage"):
            break
        after = clean(page.get("pageInfo", {}).get("endCursor"))

    return rows


def product_snapshot(product: dict[str, Any]) -> RecentProduct:
    return RecentProduct(
        product_gid=clean(product.get("id")),
        product_id=clean(product.get("legacyResourceId")),
        handle=clean(product.get("handle")),
        title=clean(product.get("title")),
        status=clean(product.get("status")),
        created_at=clean(product.get("createdAt")),
        updated_at=clean(product.get("updatedAt")),
    )


def body_item(snapshot: Any) -> dict[str, str] | None:
    for item in snapshot.translatable_content:
        if item.get("key") == "body_html":
            return item
    return None


def audit_product(
    client: ShopifyClient,
    product: dict[str, Any],
    locales: list[str],
    *,
    execute: bool,
    pause_ms: int,
    force_rebuild_size_chart_tables: bool,
) -> dict[str, Any]:
    source_html = product.get("descriptionHtml") or ""
    source_table_count = source_html.count("<table")
    source_has_size_chart = has_size_chart_table(source_html)
    row: dict[str, Any] = {
        "product_id": clean(product.get("legacyResourceId")),
        "product_gid": clean(product.get("id")),
        "handle": clean(product.get("handle")),
        "title": clean(product.get("title")),
        "status": clean(product.get("status")),
        "updated_at": clean(product.get("updatedAt")),
        "source_body_length": len(source_html),
        "source_table_count": source_table_count,
        "source_has_size_chart": source_has_size_chart,
        "locales_checked": len(locales),
        "missing_locales": [],
        "already_ok_locales": [],
        "fallback_source_locales": [],
        "planned_translation_count": 0,
        "registered_translation_count": 0,
        "errors": [],
    }
    if not source_has_size_chart:
        return row

    snapshot = client.fetch_resource(clean(product.get("id")), locales, 1)
    item = body_item(snapshot)
    if not item:
        row["errors"].append("missing_body_html_translatable_content")
        return row

    source_for_context = product_snapshot(product)
    context = infer_product_context(source_for_context, [snapshot])
    translations = []
    for locale in locales:
        existing = snapshot.existing_translations.get((locale, "body_html"))
        existing_value = existing.value if existing else ""
        if not clean(existing_value):
            repaired_value = ensure_product_html_size_chart_coverage(
                item["value"],
                item["value"],
                locale,
                product_context=context,
            )
            if not has_complete_size_chart_table_coverage(item["value"], repaired_value):
                row["errors"].append(f"{locale}:source_fallback_did_not_create_complete_size_chart_set")
                continue
            row["fallback_source_locales"].append(locale)
            row["missing_locales"].append(locale)
            translations.append(
                {
                    "locale": locale,
                    "key": "body_html",
                    "value": repaired_value,
                    "translatableContentDigest": item["digest"],
                }
            )
            continue
        if force_rebuild_size_chart_tables:
            repaired_value = rebuild_product_html_size_chart_tables_from_source(
                item["value"],
                existing_value,
                locale,
                product_context=context,
            )
            if not has_complete_size_chart_table_coverage(item["value"], repaired_value):
                row["errors"].append(f"{locale}:force_rebuild_did_not_create_complete_size_chart_set")
                continue
            if clean(repaired_value) == clean(existing_value):
                row["already_ok_locales"].append(locale)
                continue
            row["missing_locales"].append(locale)
            translations.append(
                {
                    "locale": locale,
                    "key": "body_html",
                    "value": repaired_value,
                    "translatableContentDigest": item["digest"],
                }
            )
            continue
        if has_complete_size_chart_table_coverage(item["value"], existing_value):
            row["already_ok_locales"].append(locale)
            continue

        repaired_value = ensure_product_html_size_chart_coverage(
            item["value"],
            existing_value,
            locale,
            product_context=context,
        )
        if not has_complete_size_chart_table_coverage(item["value"], repaired_value):
            row["errors"].append(f"{locale}:repair_did_not_create_complete_size_chart_set")
            continue
        if clean(repaired_value) == clean(existing_value):
            row["errors"].append(f"{locale}:repair_unchanged")
            continue

        row["missing_locales"].append(locale)
        translations.append(
            {
                "locale": locale,
                "key": "body_html",
                "value": repaired_value,
                "translatableContentDigest": item["digest"],
            }
        )

    row["planned_translation_count"] = len(translations)
    if execute and translations:
        try:
            result = client.register_translations(clean(product.get("id")), translations)
            row["registered_translation_count"] = len(result.get("translations") or [])
            if pause_ms > 0:
                time.sleep(pause_ms / 1000)
        except Exception as exc:  # noqa: BLE001
            row["errors"].append(f"register_failed:{exc}")

    return row


def write_reports(rows: list[dict[str, Any]], report_json: Path, report_csv: Path) -> dict[str, Any]:
    summary = {
        "products_scanned": len(rows),
        "products_with_source_size_chart": sum(1 for row in rows if row["source_has_size_chart"]),
        "products_with_missing_locale_size_chart": sum(1 for row in rows if row["missing_locales"]),
        "planned_translation_count": sum(int(row["planned_translation_count"]) for row in rows),
        "registered_translation_count": sum(int(row["registered_translation_count"]) for row in rows),
        "error_count": sum(len(row["errors"]) for row in rows),
    }
    payload = {"summary": summary, "rows": rows}
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report_csv.parent.mkdir(parents=True, exist_ok=True)
    with report_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "product_id",
                "handle",
                "title",
                "status",
                "source_has_size_chart",
                "missing_locales",
                "already_ok_locales",
                "fallback_source_locales",
                "planned_translation_count",
                "registered_translation_count",
                "errors",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "product_id": row["product_id"],
                    "handle": row["handle"],
                    "title": row["title"],
                    "status": row["status"],
                    "source_has_size_chart": row["source_has_size_chart"],
                    "missing_locales": ",".join(row["missing_locales"]),
                    "already_ok_locales": ",".join(row["already_ok_locales"]),
                    "fallback_source_locales": ",".join(row["fallback_source_locales"]),
                    "planned_translation_count": row["planned_translation_count"],
                    "registered_translation_count": row["registered_translation_count"],
                    "errors": " | ".join(row["errors"]),
                }
            )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--locales", default="", help="Comma-separated published non-primary locales. Defaults to all.")
    parser.add_argument("--handles", default="", help="Comma-separated handles to audit/repair instead of all active products.")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--max-products", type=int, default=0, help="0 means all active products.")
    parser.add_argument("--pause-ms", type=int, default=250)
    parser.add_argument("--execute", action="store_true", help="Register repaired body_html translations live.")
    parser.add_argument(
        "--force-rebuild-size-chart-tables",
        action="store_true",
        help="Replace localized size-chart tables from source while preserving the rest of the localized body.",
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit nonzero when any missing locale size chart or repair error remains after the audit.",
    )
    parser.add_argument(
        "--report-json",
        default="dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-repair/lanes/admin-audit/size_chart_translation_audit.json",
    )
    parser.add_argument(
        "--report-csv",
        default="dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-repair/lanes/admin-audit/size_chart_translation_audit.csv",
    )
    args = parser.parse_args()

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)
    locales = resolve_target_locales(client, args.locales)
    handles = [item.strip() for item in args.handles.split(",") if item.strip()]
    products = active_products(
        client,
        page_size=args.page_size,
        max_products=max(args.max_products, 0),
        handles=handles,
    )

    rows = []
    for index, product in enumerate(products, start=1):
        row = audit_product(
            client,
            product,
            locales,
            execute=args.execute,
            pause_ms=max(args.pause_ms, 0),
            force_rebuild_size_chart_tables=bool(args.force_rebuild_size_chart_tables),
        )
        rows.append(row)
        if index == 1 or index % 25 == 0 or index == len(products):
            print(
                f"[progress] {index}/{len(products)} scanned "
                f"planned={sum(int(item['planned_translation_count']) for item in rows)} "
                f"registered={sum(int(item['registered_translation_count']) for item in rows)}",
                flush=True,
            )

    summary = write_reports(rows, Path(args.report_json), Path(args.report_csv))
    summary.update(
        {
            "store_domain": store_domain,
            "locales": locales,
            "execute": bool(args.execute),
            "report_json": args.report_json,
            "report_csv": args.report_csv,
        }
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.fail_on_missing and (
        summary["products_with_missing_locale_size_chart"] > 0
        or summary["planned_translation_count"] > 0
        or summary["error_count"] > 0
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
