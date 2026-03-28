#!/usr/bin/env python3
"""Apply prepared Shopify vendor normalization updates.

Default mode is dry-run. Execute mode updates only the vendor field for the
rows provided in the CSV input artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_INPUT = Path("ops/feed-engineering/2026-03-28-phase-3c-scaleup/shopify_vendor_update.csv")
DEFAULT_OUTPUT = Path("ops/feed-engineering/2026-03-28-phase-3c-scaleup/shopify_vendor_update_execution_results.csv")
API_VERSION = "2026-01"
TIMEOUT_SECONDS = 60

PRODUCT_BY_IDENTIFIER_QUERY = """
query ProductByHandle($identifier: ProductIdentifierInput!) {
  product: productByIdentifier(identifier: $identifier) {
    id
    handle
    title
    vendor
    status
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation UpdateVendor($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      vendor
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""


def graphql_request(store_domain: str, access_token: str, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    url = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": access_token},
    )
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify API HTTP {exc.code}: {body}") from exc

    if data.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {data['errors']}")
    return data["data"]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fetch_live_product(store_domain: str, access_token: str, handle: str) -> dict[str, Any] | None:
    data = graphql_request(
        store_domain,
        access_token,
        PRODUCT_BY_IDENTIFIER_QUERY,
        {"identifier": {"handle": handle}},
    )
    return data.get("product")


def update_live_vendor(store_domain: str, access_token: str, product_id: str, new_vendor: str) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    data = graphql_request(
        store_domain,
        access_token,
        PRODUCT_UPDATE_MUTATION,
        {"product": {"id": product_id, "vendor": new_vendor}},
    )
    payload = data.get("productUpdate", {})
    return payload.get("product"), payload.get("userErrors", [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply prepared Shopify vendor updates.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="CSV artifact with vendor updates.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Execution results CSV.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--execute", action="store_true", help="Apply updates live. Default is dry-run.")
    parser.add_argument("--limit", type=int, default=0, help="Limit rows processed.")
    parser.add_argument("--pause-ms", type=int, default=300, help="Pause between live mutations.")
    parser.add_argument("--force", action="store_true", help="Apply even if current vendor no longer matches expected.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    rows = load_rows(input_path)

    if args.limit > 0:
        rows = rows[: args.limit]

    results: list[dict[str, str]] = []
    for row in rows:
        live_product = fetch_live_product(store_domain, access_token, row["handle"])
        if live_product is None:
            results.append(
                {
                    "handle": row["handle"],
                    "action": "error",
                    "reason": "product_not_found",
                    "expected_current_vendor": row["current_vendor"],
                    "live_vendor_before": "",
                    "live_vendor_after": "",
                }
            )
            continue

        live_vendor = (live_product.get("vendor") or "").strip()
        if live_vendor == row["new_vendor"]:
            results.append(
                {
                    "handle": row["handle"],
                    "action": "skipped",
                    "reason": "already_updated",
                    "expected_current_vendor": row["current_vendor"],
                    "live_vendor_before": live_vendor,
                    "live_vendor_after": live_vendor,
                }
            )
            continue

        if not args.force and live_vendor != row["current_vendor"]:
            results.append(
                {
                    "handle": row["handle"],
                    "action": "skipped",
                    "reason": "live_vendor_mismatch",
                    "expected_current_vendor": row["current_vendor"],
                    "live_vendor_before": live_vendor,
                    "live_vendor_after": live_vendor,
                }
            )
            continue

        if not args.execute:
            results.append(
                {
                    "handle": row["handle"],
                    "action": "dry_run",
                    "reason": "ready",
                    "expected_current_vendor": row["current_vendor"],
                    "live_vendor_before": live_vendor,
                    "live_vendor_after": row["new_vendor"],
                }
            )
            continue

        product, user_errors = update_live_vendor(store_domain, access_token, live_product["id"], row["new_vendor"])
        if user_errors:
            results.append(
                {
                    "handle": row["handle"],
                    "action": "error",
                    "reason": "; ".join(error["message"] for error in user_errors),
                    "expected_current_vendor": row["current_vendor"],
                    "live_vendor_before": live_vendor,
                    "live_vendor_after": live_vendor,
                }
            )
            continue

        updated_vendor = (product.get("vendor") or "").strip() if product else ""
        results.append(
            {
                "handle": row["handle"],
                "action": "updated",
                "reason": "ok",
                "expected_current_vendor": row["current_vendor"],
                "live_vendor_before": live_vendor,
                "live_vendor_after": updated_vendor,
            }
        )
        time.sleep(max(args.pause_ms, 0) / 1000.0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "handle",
                "action",
                "reason",
                "expected_current_vendor",
                "live_vendor_before",
                "live_vendor_after",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    summary = {
        "input": str(input_path),
        "output": str(output_path),
        "processed_rows": len(results),
        "execute": bool(args.execute),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
