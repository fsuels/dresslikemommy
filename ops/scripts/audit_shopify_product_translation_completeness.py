#!/usr/bin/env python3
"""Audit Shopify product translations for missing, stale, or source-language content."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.audit_localized_pdp_language_leakage import (  # noqa: E402
    AuditTarget,
    audit_text,
    visible_text,
)
from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    RecentProduct,
    ResourceSnapshot,
    ShopifyClient,
    clean,
    collect_resource_snapshots,
    parse_iso8601,
    resolve_target_locales,
    should_translate_field,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", visible_text(value or "")).strip().casefold()


def source_equality_is_issue(resource_type: str, key: str, source_value: str, translated_value: str) -> bool:
    source = normalized_text(source_value)
    translated = normalized_text(translated_value)
    if not source or source != translated:
        return False

    alphabetic = re.findall(r"[A-Za-z]", source)
    if resource_type == "Product" and key == "body_html":
        return len(alphabetic) >= 40
    if resource_type == "Product" and key in {"title", "product_type", "meta_title", "meta_description"}:
        return len(alphabetic) >= 18
    if resource_type == "Metafield" and key == "value":
        return len(alphabetic) >= 30
    return False


def body_language_issues(handle: str, locale: str, value: str, max_snippets: int) -> list[dict[str, str]]:
    return audit_text(
        AuditTarget(handle=handle, locale=locale, url=f"shopify-admin://products/{handle}"),
        visible_text(value),
        context_chars=100,
        heuristic=True,
        max_snippets=max(max_snippets, 0),
    )


def audit_product_snapshots(
    product: RecentProduct,
    snapshots: list[ResourceSnapshot],
    locales: list[str],
    *,
    max_snippets_per_body: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    issues: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()

    for snapshot in snapshots:
        for item in snapshot.translatable_content:
            key = clean(item.get("key"))
            source_value = item.get("value") or ""
            if not should_translate_field(snapshot.resource_type, key, source_value):
                continue

            for locale in locales:
                counters["eligible_translation_slots"] += 1
                existing = snapshot.existing_translations.get((locale, key))
                translated_value = existing.value if existing else ""
                base = {
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "status": product.status,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                    "locale": locale,
                    "resource_id": snapshot.resource_id,
                    "resource_type": snapshot.resource_type,
                    "key": key,
                }

                if not clean(translated_value):
                    counters["missing_count"] += 1
                    issues.append({**base, "issue_type": "missing_translation", "detail": "", "snippets": []})
                    continue

                if existing and existing.outdated:
                    counters["outdated_count"] += 1
                    issues.append({**base, "issue_type": "outdated_translation", "detail": "", "snippets": []})

                if source_equality_is_issue(snapshot.resource_type, key, source_value, translated_value):
                    counters["source_equal_count"] += 1
                    issues.append(
                        {
                            **base,
                            "issue_type": "translation_matches_source",
                            "detail": normalized_text(source_value)[:240],
                            "snippets": [],
                        }
                    )

                if snapshot.resource_type == "Product" and key == "body_html":
                    language_issues = body_language_issues(
                        product.handle,
                        locale,
                        translated_value,
                        max_snippets_per_body,
                    )
                    if language_issues:
                        counters["body_language_issue_count"] += 1
                        issues.append(
                            {
                                **base,
                                "issue_type": "body_source_language_leakage",
                                "detail": f"{len(language_issues)} English/source-language findings",
                                "snippets": [
                                    {
                                        "issue_type": row["issue_type"],
                                        "phrase": row["phrase"],
                                        "snippet": row["snippet"],
                                    }
                                    for row in language_issues
                                ],
                            }
                        )

    return issues, dict(counters)


def selected_products(
    client: ShopifyClient,
    *,
    handles: list[str],
    created_since: str,
    max_pages: int,
    page_size: int,
) -> list[RecentProduct]:
    if handles:
        products = client.products_by_handles(handles)
    else:
        if not created_since:
            raise SystemExit("Provide --handles or --created-since.")
        since = parse_iso8601(created_since)
        products = [
            product
            for product in client.recent_products(max_pages=max(max_pages, 1), page_size=max(page_size, 1))
            if parse_iso8601(product.created_at) >= since
        ]
    return sorted(
        (product for product in products if clean(product.status).upper() != "ARCHIVED"),
        key=lambda product: (product.created_at, product.product_id),
    )


def write_reports(payload: dict[str, Any], report_json: str, report_csv: str) -> None:
    if report_json:
        json_path = Path(report_json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if report_csv:
        csv_path = Path(report_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "product_id",
                    "handle",
                    "status",
                    "created_at",
                    "updated_at",
                    "locale",
                    "resource_id",
                    "resource_type",
                    "key",
                    "issue_type",
                    "detail",
                ],
            )
            writer.writeheader()
            for issue in payload["issues"]:
                writer.writerow({key: issue.get(key, "") for key in writer.fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--handles", default="", help="Comma-separated product handles.")
    parser.add_argument("--created-since", default="", help="Include products created on/after this ISO timestamp.")
    parser.add_argument("--locales", default="", help="Defaults to all published non-primary Shopify locales.")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--max-nested-resources", type=int, default=100)
    parser.add_argument("--max-snippets-per-body", type=int, default=20)
    parser.add_argument("--report-json", default="")
    parser.add_argument("--report-csv", default="")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    client = ShopifyClient(store_domain, load_access_token(args.access_token))
    locales = resolve_target_locales(client, args.locales)
    if not locales:
        raise SystemExit("No published non-primary locales found.")

    handles = [item.strip() for item in args.handles.split(",") if item.strip()]
    products = selected_products(
        client,
        handles=handles,
        created_since=clean(args.created_since),
        max_pages=args.max_pages,
        page_size=args.page_size,
    )

    all_issues: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    product_rows = []
    for product in products:
        snapshots = collect_resource_snapshots(
            client,
            product.product_gid,
            locales,
            max(args.max_nested_resources, 1),
        )
        issues, counters = audit_product_snapshots(
            product,
            snapshots,
            locales,
            max_snippets_per_body=max(args.max_snippets_per_body, 0),
        )
        all_issues.extend(issues)
        totals.update(counters)
        product_rows.append(
            {
                "product_id": product.product_id,
                "handle": product.handle,
                "status": product.status,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
                "resource_count": len(snapshots),
                "issue_count": len(issues),
            }
        )

    summary = {
        "store_domain": store_domain,
        "products_checked": len(products),
        "locales_checked": len(locales),
        "locales": locales,
        "eligible_translation_slots": totals["eligible_translation_slots"],
        "missing_count": totals["missing_count"],
        "outdated_count": totals["outdated_count"],
        "source_equal_count": totals["source_equal_count"],
        "body_language_issue_count": totals["body_language_issue_count"],
        "issue_count": len(all_issues),
        "products_with_issues": sum(1 for row in product_rows if row["issue_count"] > 0),
        "products": product_rows,
    }
    payload = {"summary": summary, "issues": all_issues}
    write_reports(payload, args.report_json, args.report_csv)
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if args.fail_on_issues and all_issues:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
