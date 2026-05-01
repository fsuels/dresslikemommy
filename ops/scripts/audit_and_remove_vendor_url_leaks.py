#!/usr/bin/env python3
"""Audit Shopify products for vendor/source URL leaks and remove bad tags.

The canonical listing flow uses 1688/vendor URLs as private sourcing evidence.
Those URLs must never be written into Shopify customer-visible or feed-visible
fields. This script scans live products and, with --apply, removes exact Shopify
tags that contain supplier/source domains such as 1688.com.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-04"
PAGE_SIZE = 100
DEFAULT_OUTPUT_ROOT = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS")
LEAK_RE = re.compile(
    r"(?:https?://|www\.)?[^\s,\"'<>]*(?:1688\.com|alibaba\.com|aliexpress\.com)[^\s,\"'<>]*",
    re.IGNORECASE,
)


PRODUCTS_QUERY = """
query ProductsForVendorUrlLeakAudit($first: Int!, $after: String) {
  products(first: $first, after: $after, sortKey: ID) {
    nodes {
      id
      legacyResourceId
      title
      handle
      status
      tags
      onlineStoreUrl
      descriptionHtml
      seo {
        title
        description
      }
      metafields(first: 100) {
        nodes {
          id
          namespace
          key
          type
          value
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


TAGS_REMOVE_MUTATION = """
mutation RemoveVendorUrlTags($id: ID!, $tags: [String!]!) {
  tagsRemove(id: $id, tags: $tags) {
    node {
      id
    }
    userErrors {
      field
      message
    }
  }
}
"""


def clean(value: object) -> str:
    return str(value or "").strip()


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def contains_vendor_url(value: object) -> bool:
    return bool(LEAK_RE.search(clean(value)))


def leaking_tags(tags: list[str]) -> list[str]:
    return [tag for tag in tags if contains_vendor_url(tag)]


def find_text_leaks(product: dict[str, Any]) -> list[str]:
    leaks: list[str] = []
    checks = {
        "title": product.get("title"),
        "descriptionHtml": product.get("descriptionHtml"),
        "seo.title": (product.get("seo") or {}).get("title"),
        "seo.description": (product.get("seo") or {}).get("description"),
    }
    for field, value in checks.items():
        if contains_vendor_url(value):
            leaks.append(field)

    for node in ((product.get("metafields") or {}).get("nodes") or []):
        namespace = clean(node.get("namespace"))
        key = clean(node.get("key"))
        value = node.get("value")
        if contains_vendor_url(value):
            leaks.append(f"metafield:{namespace}.{key}")
    return leaks


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(7):
            req = request.Request(self.endpoint, data=payload, headers=headers, method="POST")
            try:
                with request.urlopen(req, timeout=120) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 6:
                    time.sleep(min(20.0, (1.7**attempt) + random.uniform(0.2, 0.8)))
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {response_body}") from exc

            if body.get("errors"):
                throttled = any(
                    ((err.get("extensions") or {}).get("code") == "THROTTLED")
                    for err in body.get("errors", [])
                    if isinstance(err, dict)
                )
                if throttled and attempt < 6:
                    time.sleep(min(30.0, (2.0**attempt) + random.uniform(1.0, 3.0)))
                    continue
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")

            throttle = (body.get("extensions") or {}).get("cost", {}).get("throttleStatus", {})
            currently_available = float(throttle.get("currentlyAvailable", 1000))
            if currently_available < 200:
                time.sleep((200 - currently_available) / 100.0)

            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def fetch_products(client: ShopifyClient) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        data = client.graphql(PRODUCTS_QUERY, {"first": PAGE_SIZE, "after": after})
        connection = data["products"]
        products.extend(connection.get("nodes") or [])
        page_info = connection.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        after = page_info.get("endCursor")
    return products


def build_rows(products: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for product in products:
        tags = [clean(tag) for tag in product.get("tags") or [] if clean(tag)]
        bad_tags = leaking_tags(tags)
        text_leaks = find_text_leaks(product)
        if not bad_tags and not text_leaks:
            continue
        rows.append(
            {
                "product_gid": clean(product.get("id")),
                "product_id": clean(product.get("legacyResourceId")),
                "status": clean(product.get("status")),
                "title": clean(product.get("title")),
                "handle": clean(product.get("handle")),
                "online_store_url": clean(product.get("onlineStoreUrl")),
                "bad_tags": " | ".join(bad_tags),
                "bad_tag_count": str(len(bad_tags)),
                "other_leak_fields": " | ".join(text_leaks),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "product_gid",
        "product_id",
        "status",
        "title",
        "handle",
        "online_store_url",
        "bad_tags",
        "bad_tag_count",
        "other_leak_fields",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_bad_tags(client: ShopifyClient, rows: list[dict[str, str]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for row in rows:
        tags = [tag.strip() for tag in row["bad_tags"].split("|") if tag.strip()]
        if not tags:
            continue
        data = client.graphql(TAGS_REMOVE_MUTATION, {"id": row["product_gid"], "tags": tags})["tagsRemove"]
        user_errors = data.get("userErrors") or []
        if user_errors:
            errors.append({"product_id": row["product_id"], "handle": row["handle"], "errors": user_errors})
        results.append({"product_id": row["product_id"], "handle": row["handle"], "removed_tags": tags})
        time.sleep(0.15)
    return {"products_attempted": len(results), "removed": results, "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Remove exact leaking Shopify tags.")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_ROOT / f"{now_stamp()}-shopify-vendor-url-leak-cleanup"
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    products = fetch_products(client)
    rows = build_rows(products)
    report_csv = output_dir / ("post_cleanup_vendor_url_leak_scan.csv" if args.apply else "vendor_url_leak_scan.csv")
    write_csv(report_csv, rows)

    execution: dict[str, Any] | None = None
    if args.apply:
        execution = remove_bad_tags(client, rows)
        products_after = fetch_products(client)
        post_rows = build_rows(products_after)
        post_csv = output_dir / "post_cleanup_vendor_url_leak_scan.csv"
        write_csv(post_csv, post_rows)
        rows = post_rows

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "APPLY_REMOVE_BAD_TAGS" if args.apply else "DRY_RUN_ONLY",
        "products_scanned": len(products),
        "products_with_vendor_url_leaks_after_run": len(rows),
        "products_with_bad_tags_after_run": sum(1 for row in rows if row["bad_tags"]),
        "products_with_other_leak_fields_after_run": sum(1 for row in rows if row["other_leak_fields"]),
        "output_dir": str(output_dir),
        "report_csv": str(report_csv),
        "execution": execution,
    }
    summary_path = output_dir / ("execution_summary.json" if args.apply else "dry_run_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))

    if execution and execution.get("errors"):
        sys.exit(1)
    if args.apply and (summary["products_with_bad_tags_after_run"] or summary["products_with_other_leak_fields_after_run"]):
        sys.exit(2)


if __name__ == "__main__":
    main()
