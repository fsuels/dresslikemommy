#!/usr/bin/env python3
"""Remove stale Shopify Google custom-label metafields for parent outfits.

This repair is intentionally narrow:
- read parent product IDs from this packet's Merchant label spec
- only target namespace mm-google-shopping keys custom_label_0..4
- do not touch titles, handles, body, SEO, prices, variants, inventory,
  publications, campaigns, budgets, bids, product groups, conversions, or billing
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "ops" / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "ops" / "scripts"))

from shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-04"
PACKET_DIR = Path(__file__).resolve().parent
SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
OUTPUT_PREFIX = "parent_outfit_shopify_google_label_metafield_repair"
TARGET_NAMESPACE = "mm-google-shopping"
TARGET_KEYS = {f"custom_label_{index}" for index in range(5)}


READ_PRODUCTS_QUERY = """
query ReadProducts($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on Product {
      id
      legacyResourceId
      title
      handle
      status
      metafields(first: 20, namespace: "mm-google-shopping") {
        nodes {
          id
          namespace
          key
          value
        }
      }
    }
  }
}
"""


DELETE_MUTATION = """
mutation DeleteGoogleCustomLabels($metafields: [MetafieldIdentifierInput!]!) {
  metafieldsDelete(metafields: $metafields) {
    deletedMetafields {
      ownerId
      namespace
      key
    }
    userErrors {
      field
      message
    }
  }
}
"""


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def clean(value: object) -> str:
    return str(value or "").strip()


def load_parent_product_ids() -> list[str]:
    parent_ids: set[str] = set()
    with SPEC_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if clean(row.get("decision")) != "INCLUDE":
                continue
            parent_id = clean(row.get("parent_product_id") or row.get("item_group_id"))
            if parent_id:
                parent_ids.add(parent_id)
    return sorted(parent_ids, key=lambda value: int(value) if value.isdigit() else value)


def product_gid(product_id: str) -> str:
    return f"gid://shopify/Product/{product_id}"


def chunked(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Shopify Admin HTTP {exc.code}: {body[:500]}") from exc
        if payload.get("errors"):
            raise RuntimeError(json.dumps(payload["errors"], indent=2))
        return payload["data"]


def read_products(client: ShopifyClient, product_ids: list[str]) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    for batch in chunked(product_ids, 50):
        ids = [product_gid(product_id) for product_id in batch]
        data = client.graphql(READ_PRODUCTS_QUERY, {"ids": ids})
        for node in data.get("nodes") or []:
            if not node:
                continue
            products.append(node)
        time.sleep(0.15)
    return products


def target_rows(products: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for product in products:
        product_id = clean(product.get("legacyResourceId"))
        for node in (product.get("metafields") or {}).get("nodes") or []:
            namespace = clean(node.get("namespace"))
            key = clean(node.get("key"))
            if namespace != TARGET_NAMESPACE or key not in TARGET_KEYS:
                continue
            rows.append(
                {
                    "shopify_product_id": product_id,
                    "shopify_product_gid": clean(product.get("id")),
                    "product_title": clean(product.get("title")),
                    "handle": clean(product.get("handle")),
                    "status": clean(product.get("status")),
                    "metafield_gid": clean(node.get("id")),
                    "namespace": namespace,
                    "key": key,
                    "old_value": clean(node.get("value")),
                }
            )
    return sorted(rows, key=lambda row: (row["shopify_product_id"], row["key"]))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def delete_targets(client: ShopifyClient, rows: list[dict[str, str]]) -> dict[str, Any]:
    deleted: list[dict[str, str]] = []
    errors: list[dict[str, Any]] = []
    for batch_index, batch in enumerate(chunked(rows, 25), start=1):
        variables = {
            "metafields": [
                {
                    "ownerId": row["shopify_product_gid"],
                    "namespace": row["namespace"],
                    "key": row["key"],
                }
                for row in batch
            ]
        }
        result = client.graphql(DELETE_MUTATION, variables)["metafieldsDelete"]
        deleted.extend(result.get("deletedMetafields") or [])
        for error in result.get("userErrors") or []:
            errors.append({"batch": batch_index, **error})
        time.sleep(0.2)
    return {
        "batches": len(chunked(rows, 25)),
        "deleted_count": len(deleted),
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    args = parser.parse_args()

    stamp = now_stamp()
    product_ids = load_parent_product_ids()
    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )

    before_products = read_products(client, product_ids)
    before_rows = target_rows(before_products)
    fields = [
        "shopify_product_id",
        "shopify_product_gid",
        "product_title",
        "handle",
        "status",
        "metafield_gid",
        "namespace",
        "key",
        "old_value",
    ]
    mode = "apply" if args.apply else "dry_run"
    before_csv = PACKET_DIR / f"{OUTPUT_PREFIX}_{mode}_before_{stamp}.csv"
    write_csv(before_csv, before_rows, fields)

    execution: dict[str, Any] = {"mode": "DRY_RUN_ONLY", "deleted_count": 0, "error_count": 0, "errors": []}
    after_rows: list[dict[str, str]] = []
    after_csv = ""
    if args.apply and before_rows:
        execution = {"mode": "APPLY_DELETE", **delete_targets(client, before_rows)}
        after_products = read_products(client, product_ids)
        after_rows = target_rows(after_products)
        after_path = PACKET_DIR / f"{OUTPUT_PREFIX}_apply_after_{stamp}.csv"
        write_csv(after_path, after_rows, fields)
        after_csv = str(after_path)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": execution["mode"],
        "scope": "Parent outfit products from merchant_label_update_spec.csv; delete only mm-google-shopping custom_label_0..4 product metafields.",
        "parent_product_count": len(product_ids),
        "products_read_before": len(before_products),
        "target_metafields_before": len(before_rows),
        "target_product_count_before": len({row["shopify_product_id"] for row in before_rows}),
        "target_key_counts_before": dict(Counter(row["key"] for row in before_rows)),
        "target_value_counts_before": dict(Counter(row["old_value"] for row in before_rows).most_common(30)),
        "before_csv": str(before_csv),
        "after_csv": after_csv,
        "remaining_target_metafields_after": len(after_rows),
        "remaining_target_product_count_after": len({row["shopify_product_id"] for row in after_rows}),
        "execution": execution,
        "blocked_fields": [
            "titles",
            "prices",
            "handles",
            "body",
            "seo",
            "inventory",
            "publications",
            "campaigns",
            "budgets",
            "bids",
            "statuses",
            "product_groups",
            "conversions",
            "billing",
        ],
    }
    summary_path = PACKET_DIR / f"{OUTPUT_PREFIX}_{mode}_summary_{stamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if execution.get("error_count") else 0


if __name__ == "__main__":
    raise SystemExit(main())
