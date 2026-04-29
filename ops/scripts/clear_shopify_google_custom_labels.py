#!/usr/bin/env python3
"""Clear old product-level Google custom labels from Shopify.

Why this exists:
- The clean Shopping plan needs variant/offer-level labels from Merchant Center.
- The Shopify product-level mm-google-shopping.custom_label_* metafields are
  currently feeding old labels like high/set/true/summer/0-25 into Merchant.
- Many paid listings mix eligible and excluded variants, so product-level paid
  labels would be unsafe. Clearing product-level labels lets the supplemental
  offer-level feed become the targeting source after Google refreshes.

The script is reversible: it writes a rollback CSV before applying deletes.
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
from datetime import datetime
from pathlib import Path
from typing import Any

from shopify_admin_config import load_access_token, resolve_store_domain


API_VERSION = "2026-04"
ROOT = Path("dresslikemommy-growth-2026")
SHOPIFY_VARIANTS = ROOT / "01_EXPORTS_RAW/SHOPIFY/2026-04-29-shopify-margin-cac-export-pack_active_variants_readonly_sanitized.json"
MASTER = ROOT / "02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/google_shopping_us_clean_subset_master.csv"
OUTPUT_DIR = ROOT / "02_AUDIT_PACKETS/2026-04-29-shopify-google-custom-label-clear"
TARGET_NAMESPACE = "mm-google-shopping"
TARGET_KEYS = {f"custom_label_{index}" for index in range(5)}


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


READBACK_QUERY = """
query ProductGoogleLabels($id: ID!) {
  product(id: $id) {
    id
    legacyResourceId
    title
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
"""


def clean(value: object) -> str:
    return str(value or "").strip()


def read_master_product_ids(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {clean(row.get("shopify_product_id")) for row in csv.DictReader(handle) if clean(row.get("shopify_product_id"))}


def load_targets() -> tuple[list[dict[str, str]], dict[str, Any]]:
    scoped_product_ids = read_master_product_ids(MASTER)
    payload = json.loads(SHOPIFY_VARIANTS.read_text(encoding="utf-8"))
    by_product: dict[str, dict[str, Any]] = {}
    for variant in payload.get("variants", []):
        product = variant.get("product") or {}
        product_id = clean(product.get("legacyResourceId"))
        if product_id in scoped_product_ids and product_id not in by_product:
            by_product[product_id] = product

    targets: list[dict[str, str]] = []
    for product_id, product in sorted(by_product.items()):
        owner_id = clean(product.get("id"))
        for node in product.get("googleShoppingMetafields", {}).get("nodes", []):
            namespace = clean(node.get("namespace"))
            key = clean(node.get("key"))
            value = clean(node.get("value"))
            metafield_id = clean(node.get("id"))
            if namespace == TARGET_NAMESPACE and key in TARGET_KEYS and metafield_id:
                targets.append(
                    {
                        "shopify_product_id": product_id,
                        "shopify_product_gid": owner_id,
                        "product_title": clean(product.get("title")),
                        "handle": clean(product.get("handle")),
                        "metafield_gid": metafield_id,
                        "namespace": namespace,
                        "key": key,
                        "old_value": value,
                    }
                )
    summary = {
        "active_variant_export_rows": len(payload.get("variants", [])),
        "scoped_master_product_ids": len(scoped_product_ids),
        "scoped_products_found_in_shopify_export": len(by_product),
        "target_metafields": len(targets),
        "target_product_count": len({row["shopify_product_id"] for row in targets}),
        "target_key_counts": dict(Counter(row["key"] for row in targets)),
        "target_value_counts": dict(Counter(row["old_value"] for row in targets).most_common(20)),
    }
    return targets, summary


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Shopify Admin HTTP {exc.code}: {body[:500]}") from exc
        if payload.get("errors"):
            raise RuntimeError(json.dumps(payload["errors"], indent=2))
        return payload["data"]


def chunked(rows: list[dict[str, str]], size: int) -> list[list[dict[str, str]]]:
    return [rows[index : index + size] for index in range(0, len(rows), size)]


def apply_delete(client: ShopifyClient, targets: list[dict[str, str]]) -> dict[str, Any]:
    batches = chunked(targets, 25)
    deleted: list[dict[str, str]] = []
    errors: list[dict[str, Any]] = []
    for batch_index, batch in enumerate(batches, start=1):
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
        data = client.graphql(DELETE_MUTATION, variables)["metafieldsDelete"]
        deleted.extend(data.get("deletedMetafields") or [])
        for error in data.get("userErrors") or []:
            errors.append({"batch": batch_index, **error})
        time.sleep(0.2)
    return {"deleted": deleted, "errors": errors, "batches": len(batches)}


def readback_sample(client: ShopifyClient, targets: list[dict[str, str]], limit: int = 10) -> list[dict[str, Any]]:
    sample: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in targets:
        product_gid = row["shopify_product_gid"]
        if product_gid in seen:
            continue
        seen.add(product_gid)
        data = client.graphql(READBACK_QUERY, {"id": product_gid})["product"]
        nodes = data.get("metafields", {}).get("nodes", []) if data else []
        sample.append(
            {
                "shopify_product_id": row["shopify_product_id"],
                "product_title": row["product_title"],
                "remaining_mm_google_custom_labels": [
                    node for node in nodes if node.get("key") in TARGET_KEYS
                ],
            }
        )
        if len(sample) >= limit:
            break
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Actually delete the old product-level custom-label metafields.")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    args = parser.parse_args()

    targets, summary = load_targets()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rollback_path = OUTPUT_DIR / "rollback_mm_google_custom_labels.csv"
    plan_path = OUTPUT_DIR / "delete_plan_mm_google_custom_labels.csv"
    summary_path = OUTPUT_DIR / ("execution_summary.json" if args.apply else "dry_run_summary.json")
    write_csv(
        rollback_path,
        targets,
        ["shopify_product_id", "shopify_product_gid", "product_title", "handle", "metafield_gid", "namespace", "key", "old_value"],
    )
    write_csv(
        plan_path,
        targets,
        ["shopify_product_id", "shopify_product_gid", "product_title", "handle", "metafield_gid", "namespace", "key", "old_value"],
    )

    summary.update(
        {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "mode": "APPLY_DELETE" if args.apply else "DRY_RUN_ONLY",
            "scope": "Products present in the 7,324-row clean-subset master, deleting only mm-google-shopping custom_label_0..4 product metafields.",
            "rollback_csv": str(rollback_path),
            "delete_plan_csv": str(plan_path),
            "why": "Remove old product-level Google custom labels so variant-level Merchant Center supplemental labels can control paid targeting.",
        }
    )

    if args.apply:
        client = ShopifyClient(
            resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
            load_access_token(args.access_token),
        )
        execution = apply_delete(client, targets)
        summary["execution"] = execution
        summary["readback_sample"] = readback_sample(client, targets)
        if execution["errors"]:
            summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(json.dumps(summary, indent=2, sort_keys=True))
            sys.exit(1)

    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
