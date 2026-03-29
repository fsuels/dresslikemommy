#!/usr/bin/env python3
"""Rank manual productType review rows by Shopify order revenue."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
ORDER_PAGE_SIZE = 25
LINE_ITEM_PAGE_SIZE = 100
DEFAULT_INPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3d-product-type-sync")
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR
DEFAULT_START_DATE = "2024-01-01"

ORDERS_QUERY = """
query Orders($first: Int!, $after: String, $query: String) {
  orders(
    first: $first
    after: $after
    query: $query
    sortKey: PROCESSED_AT
    reverse: true
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      name
      processedAt
      lineItems(first: 100) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          quantity
          discountedTotalSet {
            shopMoney {
              amount
              currencyCode
            }
          }
          product {
            legacyResourceId
          }
        }
      }
    }
  }
}
"""

ORDER_LINE_ITEMS_QUERY = """
query OrderLineItems($id: ID!, $first: Int!, $after: String) {
  order(id: $id) {
    lineItems(first: $first, after: $after) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        quantity
        discountedTotalSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        product {
          legacyResourceId
        }
      }
    }
  }
}
"""


def clean(value: Any) -> str:
    return str(value or "").strip()


def money_amount(payload: dict[str, Any] | None) -> float:
    try:
        return float(((payload or {}).get("shopMoney") or {}).get("amount") or 0.0)
    except (TypeError, ValueError):
        return 0.0


@dataclass
class ManualReviewRow:
    product_id: str
    handle: str
    title: str
    vendor: str
    current_product_type: str
    custom_type: str
    custom_style: str
    custom_pattern: str
    confidence: str
    source: str
    review_reason: str
    collection_handles: str
    online_store_url: str


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        req = request.Request(
            self.endpoint,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            },
        )
        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc

        if body.get("errors"):
            raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
        return body["data"]

    def iter_orders(self, query_string: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        after: str | None = None
        while True:
            data = self.graphql(
                ORDERS_QUERY,
                {"first": ORDER_PAGE_SIZE, "after": after, "query": query_string},
            )["orders"]
            rows.extend(data["nodes"])
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return rows

    def fetch_order_line_items(self, order_id: str, after: str | None = None) -> dict[str, Any]:
        return self.graphql(
            ORDER_LINE_ITEMS_QUERY,
            {"id": order_id, "first": LINE_ITEM_PAGE_SIZE, "after": after},
        )["order"]["lineItems"]


def load_manual_review_rows(path: Path) -> dict[str, ManualReviewRow]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = {
            clean(row["product_id"]): ManualReviewRow(
                product_id=clean(row["product_id"]),
                handle=clean(row["handle"]),
                title=clean(row["title"]),
                vendor=clean(row["vendor"]),
                current_product_type=clean(row["current_product_type"]),
                custom_type=clean(row["custom_type"]),
                custom_style=clean(row["custom_style"]),
                custom_pattern=clean(row["custom_pattern"]),
                confidence=clean(row["confidence"]),
                source=clean(row["source"]),
                review_reason=clean(row["review_reason"]),
                collection_handles=clean(row["collection_handles"]),
                online_store_url=clean(row["online_store_url"]),
            )
            for row in reader
            if clean(row.get("product_id"))
        }
    return rows


def collect_revenue(
    client: ShopifyClient,
    manual_rows: dict[str, ManualReviewRow],
    *,
    start_date: str,
    sleep_ms: int,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    query_string = f"processed_at:>={start_date}"
    orders = client.iter_orders(query_string)
    aggregates: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"discounted_revenue": 0.0, "units": 0, "line_item_rows": 0, "orders": set(), "currency_codes": Counter()}
    )
    orders_scanned = 0
    nested_line_item_pages = 0

    for order in orders:
        orders_scanned += 1
        line_items = order.get("lineItems") or {}
        nodes = list(line_items.get("nodes") or [])
        for node in nodes:
            product = node.get("product") or {}
            product_id = clean(product.get("legacyResourceId"))
            if product_id not in manual_rows:
                continue
            aggregates[product_id]["discounted_revenue"] += money_amount(node.get("discountedTotalSet"))
            aggregates[product_id]["units"] += int(node.get("quantity") or 0)
            aggregates[product_id]["line_item_rows"] += 1
            aggregates[product_id]["orders"].add(clean(order.get("name")))
            currency = clean((((node.get("discountedTotalSet") or {}).get("shopMoney") or {}).get("currencyCode")))
            if currency:
                aggregates[product_id]["currency_codes"][currency] += 1

        after = line_items.get("pageInfo", {}).get("endCursor")
        while line_items.get("pageInfo", {}).get("hasNextPage"):
            nested_line_item_pages += 1
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)
            line_items = client.fetch_order_line_items(clean(order.get("id")), after=after)
            for node in line_items.get("nodes") or []:
                product = node.get("product") or {}
                product_id = clean(product.get("legacyResourceId"))
                if product_id not in manual_rows:
                    continue
                aggregates[product_id]["discounted_revenue"] += money_amount(node.get("discountedTotalSet"))
                aggregates[product_id]["units"] += int(node.get("quantity") or 0)
                aggregates[product_id]["line_item_rows"] += 1
                aggregates[product_id]["orders"].add(clean(order.get("name")))
                currency = clean((((node.get("discountedTotalSet") or {}).get("shopMoney") or {}).get("currencyCode")))
                if currency:
                    aggregates[product_id]["currency_codes"][currency] += 1
            after = line_items.get("pageInfo", {}).get("endCursor")

        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

    summary = {
        "start_date": start_date,
        "orders_scanned": orders_scanned,
        "nested_line_item_pages": nested_line_item_pages,
        "manual_review_products": len(manual_rows),
        "manual_review_products_with_revenue": sum(1 for item in aggregates.values() if item["discounted_revenue"] > 0),
    }
    return aggregates, summary


def build_rows(
    manual_rows: dict[str, ManualReviewRow],
    aggregates: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for product_id, row in manual_rows.items():
        aggregate = aggregates.get(product_id) or {}
        currency_codes = aggregate.get("currency_codes") or Counter()
        rows.append(
            {
                "product_id": row.product_id,
                "handle": row.handle,
                "title": row.title,
                "vendor": row.vendor,
                "current_product_type": row.current_product_type,
                "custom_type": row.custom_type,
                "discounted_revenue": f"{aggregate.get('discounted_revenue', 0.0):.2f}",
                "units": aggregate.get("units", 0),
                "line_item_rows": aggregate.get("line_item_rows", 0),
                "order_count": len(aggregate.get("orders", set())),
                "currency_codes": "|".join(sorted(currency_codes)),
                "custom_style": row.custom_style,
                "custom_pattern": row.custom_pattern,
                "source": row.source,
                "review_reason": row.review_reason,
                "collection_handles": row.collection_handles,
                "online_store_url": row.online_store_url,
            }
        )
    rows.sort(key=lambda item: (-float(item["discounted_revenue"]), item["handle"]))
    for rank, row in enumerate(rows, start=1):
        row["revenue_rank"] = rank
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export manual productType review rows ranked by revenue.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing manual review CSV.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory to write revenue ranking artifacts.")
    parser.add_argument("--start-date", default=DEFAULT_START_DATE, help="Inclusive processed_at lower bound (YYYY-MM-DD).")
    parser.add_argument("--top-limit", type=int, default=20, help="Number of top-revenue manual review rows to export.")
    parser.add_argument("--sleep-ms", type=int, default=50, help="Pause between paginated API requests.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manual_rows = load_manual_review_rows(input_dir / "product_type_mismatch_manual_review.csv")
    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)

    aggregates, summary = collect_revenue(
        client,
        manual_rows,
        start_date=args.start_date,
        sleep_ms=max(args.sleep_ms, 0),
    )
    all_rows = build_rows(manual_rows, aggregates)

    fieldnames = [
        "revenue_rank",
        "product_id",
        "handle",
        "title",
        "vendor",
        "current_product_type",
        "custom_type",
        "discounted_revenue",
        "units",
        "line_item_rows",
        "order_count",
        "currency_codes",
        "custom_style",
        "custom_pattern",
        "source",
        "review_reason",
        "collection_handles",
        "online_store_url",
    ]
    write_csv(output_dir / "product_type_mismatch_manual_review_revenue_all.csv", all_rows, fieldnames)
    write_csv(output_dir / "product_type_mismatch_manual_review_top20_by_revenue.csv", all_rows[: args.top_limit], fieldnames)

    pair_revenue = Counter()
    for row in all_rows:
        pair_revenue[(row["current_product_type"], row["custom_type"])] += float(row["discounted_revenue"])

    summary["pair_discounted_revenue"] = [
        {
            "current_product_type": pair[0],
            "custom_type": pair[1],
            "discounted_revenue": round(amount, 2),
        }
        for pair, amount in pair_revenue.most_common()
    ]
    summary["top_20_handles"] = [row["handle"] for row in all_rows[: args.top_limit]]
    (output_dir / "product_type_mismatch_manual_review_revenue_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "manual_review_products": len(manual_rows),
                "manual_review_products_with_revenue": summary["manual_review_products_with_revenue"],
                "orders_scanned": summary["orders_scanned"],
                "top_limit": args.top_limit,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
