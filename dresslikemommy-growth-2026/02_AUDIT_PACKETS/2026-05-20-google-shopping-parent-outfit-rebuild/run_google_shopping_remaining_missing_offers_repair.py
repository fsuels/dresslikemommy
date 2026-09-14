#!/usr/bin/env python3
"""Narrow Shopify Google & YouTube publication resync for remaining missing offers.

This script is scoped to the 8 approved Mommy & Me parent products and their
current missing expected offer IDs. It does not edit product fields, variants,
inventory, prices, SEO, campaigns, budgets, bids, billing, or Merchant sources.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
GOOGLE_PUBLICATION_ID = "gid://shopify/Publication/21969633377"
PACKET_DIR = Path(__file__).resolve().parent
MISSING_ROWS_CSV = PACKET_DIR / "google_shopping_parent_outfit_missing_expected_rows_20260521T070231Z.csv"
MISSING_PARENT_SUMMARY_CSV = (
    PACKET_DIR / "google_shopping_parent_outfit_missing_expected_parent_summary_20260521T070231Z.csv"
)
TIMEOUT_SECONDS = 120


PRODUCT_QUERY = """
query Product($id: ID!) {
  product(id: $id) {
    id
    legacyResourceId
    handle
    title
    status
    publishedAt
    onlineStoreUrl
    resourcePublications(first: 100) {
      edges {
        node {
          isPublished
          publishDate
          publication {
            id
            name
          }
        }
      }
    }
    variants(first: 100) {
      edges {
        node {
          id
          legacyResourceId
          title
          sku
          availableForSale
          inventoryPolicy
          inventoryQuantity
          selectedOptions {
            name
            value
          }
        }
      }
    }
  }
}
"""

PUBLISH_MUTATION = """
mutation PublishToGoogle($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    userErrors {
      field
      message
    }
  }
}
"""


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
        for attempt in range(6):
            req = request.Request(self.endpoint, data=payload, headers=headers, method="POST")
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                text = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {text}") from exc
            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def product_gid(legacy_id: str) -> str:
    return f"gid://shopify/Product/{legacy_id}"


def google_publication(product: dict[str, Any]) -> dict[str, Any] | None:
    for edge in product["resourcePublications"]["edges"]:
        node = edge["node"]
        publication = node.get("publication") or {}
        if publication.get("id") == GOOGLE_PUBLICATION_ID:
            return node
    return None


def summarize_product(product: dict[str, Any], missing_variant_ids: set[str]) -> dict[str, Any]:
    variants = [edge["node"] for edge in product["variants"]["edges"]]
    variant_ids = {str(variant["legacyResourceId"]) for variant in variants}
    missing_variants = [variant for variant in variants if str(variant["legacyResourceId"]) in missing_variant_ids]
    missing_absent_from_shopify = sorted(missing_variant_ids - variant_ids)
    publication = google_publication(product)
    return {
        "id": product["id"],
        "legacy_id": str(product["legacyResourceId"]),
        "handle": product["handle"],
        "title": product["title"],
        "status": product["status"],
        "published_at": product.get("publishedAt"),
        "online_store_url_present": bool(product.get("onlineStoreUrl")),
        "google_publication": publication,
        "google_published": bool(publication and publication.get("isPublished")),
        "variant_count": len(variants),
        "missing_expected_variant_count": len(missing_variant_ids),
        "missing_expected_variants_present_in_shopify": len(missing_variants),
        "missing_expected_variants_absent_from_shopify": missing_absent_from_shopify,
        "missing_variant_sample": [
            {
                "id": variant["id"],
                "legacy_id": str(variant["legacyResourceId"]),
                "title": variant["title"],
                "sku": variant.get("sku"),
                "available_for_sale": variant.get("availableForSale"),
                "inventory_policy": variant.get("inventoryPolicy"),
                "inventory_quantity": variant.get("inventoryQuantity"),
                "selected_options": variant.get("selectedOptions"),
            }
            for variant in missing_variants[:10]
        ],
    }


def build_scope() -> tuple[list[dict[str, str]], dict[str, set[str]]]:
    parent_summary = read_csv(MISSING_PARENT_SUMMARY_CSV)
    missing_rows = read_csv(MISSING_ROWS_CSV)
    missing_by_parent: dict[str, set[str]] = {row["parent_product_id"]: set() for row in parent_summary}
    for row in missing_rows:
        parts = row["item_id"].split("_")
        if len(parts) < 4:
            raise RuntimeError(f"Unexpected Merchant item_id shape: {row['item_id']}")
        parent_id = row["parent_product_id"]
        variant_id = parts[-1]
        if parent_id not in missing_by_parent:
            raise RuntimeError(f"Missing row parent {parent_id} is outside approved parent summary.")
        missing_by_parent[parent_id].add(variant_id)
    return parent_summary, missing_by_parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Run the approved narrow publishablePublish repair.")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--output-prefix", default="")
    args = parser.parse_args()

    parent_summary, missing_by_parent = build_scope()
    if len(parent_summary) != 8:
        raise RuntimeError(f"Expected exactly 8 approved parent products, found {len(parent_summary)}.")
    if sum(len(ids) for ids in missing_by_parent.values()) != 141:
        raise RuntimeError("Expected exactly 141 approved missing offer IDs.")

    client = ShopifyClient(resolve_store_domain(args.store_domain), load_access_token())
    stamp = args.output_prefix or now_stamp()

    products: list[dict[str, Any]] = []
    for parent in parent_summary:
        product = client.graphql(PRODUCT_QUERY, {"id": product_gid(parent["parent_product_id"])})["product"]
        if not product:
            raise RuntimeError(f"Shopify product not found: {parent['parent_product_id']}")
        products.append(summarize_product(product, missing_by_parent[parent["parent_product_id"]]))

    blocking_reasons: list[str] = []
    for product in products:
        if product["status"] != "ACTIVE":
            blocking_reasons.append(f"{product['legacy_id']} status is {product['status']}, not ACTIVE")
        if not product["google_published"]:
            blocking_reasons.append(f"{product['legacy_id']} is not published to Google & YouTube")
        if product["missing_expected_variants_absent_from_shopify"]:
            blocking_reasons.append(
                f"{product['legacy_id']} has missing expected variants absent from Shopify: "
                + ",".join(product["missing_expected_variants_absent_from_shopify"][:10])
            )

    before_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_shopify_before_{stamp}.json"
    write_json(
        before_path,
        {
            "timestamp_utc": stamp,
            "approved_scope": {
                "parent_products": len(parent_summary),
                "missing_expected_offer_ids": sum(len(ids) for ids in missing_by_parent.values()),
                "publication_id": GOOGLE_PUBLICATION_ID,
            },
            "products": products,
            "blocking_reasons": blocking_reasons,
            "apply_requested": args.apply,
        },
    )

    execution: dict[str, Any] = {
        "timestamp_utc": stamp,
        "apply_requested": args.apply,
        "repair_attempted": False,
        "repair_type": "shopify_publishablePublish_google_youtube_resync",
        "publication_id": GOOGLE_PUBLICATION_ID,
        "product_ids": [product["id"] for product in products],
        "results": [],
        "blocking_reasons": blocking_reasons,
    }

    if blocking_reasons:
        execution["stopped"] = True
        execution["stop_reason"] = "NARROW_REPAIR_PRECHECK_FAILED"
    elif args.apply:
        execution["repair_attempted"] = True
        for product in products:
            result = client.graphql(
                PUBLISH_MUTATION,
                {
                    "id": product["id"],
                    "input": [{"publicationId": GOOGLE_PUBLICATION_ID}],
                },
            )["publishablePublish"]
            execution["results"].append(
                {
                    "product_id": product["id"],
                    "legacy_id": product["legacy_id"],
                    "handle": product["handle"],
                    "user_errors": result.get("userErrors", []),
                }
            )
        execution["stopped"] = False
    else:
        execution["stopped"] = False
        execution["dry_run"] = True

    execution_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_repair_execution_{stamp}.json"
    write_json(execution_path, execution)

    after_products: list[dict[str, Any]] = []
    if args.apply and not blocking_reasons:
        for parent in parent_summary:
            product = client.graphql(PRODUCT_QUERY, {"id": product_gid(parent["parent_product_id"])})["product"]
            after_products.append(summarize_product(product, missing_by_parent[parent["parent_product_id"]]))
        after_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_shopify_after_{stamp}.json"
        write_json(
            after_path,
            {
                "timestamp_utc": stamp,
                "products": after_products,
                "mutation_user_error_count": sum(len(row["user_errors"]) for row in execution["results"]),
            },
        )
    else:
        after_path = None

    summary = {
        "timestamp_utc": stamp,
        "apply_requested": args.apply,
        "repair_attempted": execution["repair_attempted"],
        "blocking_reasons": blocking_reasons,
        "before_path": str(before_path),
        "execution_path": str(execution_path),
        "after_path": str(after_path) if after_path else None,
        "mutation_user_error_count": sum(len(row["user_errors"]) for row in execution["results"]),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 2 if blocking_reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
