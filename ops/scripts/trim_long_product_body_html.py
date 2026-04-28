#!/usr/bin/env python3
"""Trim overlong Shopify product descriptions for current source products."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

from bs4 import BeautifulSoup, NavigableString, Tag

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT = Path("ops/reports/product-body-html-trim-2026-04-28.json")
PRODUCT_BODY_QUERY = "body_html:>10000"
DEFAULT_THRESHOLD = 10_000
DEFAULT_MAX_LENGTH = 8_000
DEFAULT_EXPECTED_COUNT = 21
SOURCE_HANDLE_SUFFIX = "family-matching-set"
REQUESTED_HANDLES = {
    "fruit-green-family-matching-set",
    "blue-check-family-matching-set",
    "summer-plaid-family-matching-set",
    "geometric-blue-family-matching-set",
    "seaside-blue-family-matching-set",
    "willow-wildflower-family-matching-set",
}
POLICY_TEXT_RE = re.compile(
    r"\b("
    r"shipping|delivery|returns?|refund|exchange|processing time|standard shipping|"
    r"free shipping|orders? over|business days|tracking|policy|customs|duties"
    r")\b",
    re.I,
)
SIZE_CHART_RE = re.compile(r"\b(size|fit|measurement)s?\s+chart\b|\bsize\s+guide\b", re.I)


PRODUCTS_COUNT_QUERY = """
query ProductsCount($query: String!) {
  productsCount(query: $query) {
    count
    precision
  }
}
"""

PRODUCTS_QUERY = """
query Products($cursor: String) {
  products(first: 100, after: $cursor, sortKey: ID) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      legacyResourceId
      handle
      title
      status
      updatedAt
      descriptionHtml
    }
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      updatedAt
      descriptionHtml
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class ProductRecord:
    id: str
    legacy_resource_id: str
    handle: str
    title: str
    status: str
    updated_at: str
    description_html: str

    @property
    def length(self) -> int:
        return len(self.description_html or "")


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
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {response_body}") from exc

            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(body['errors'], indent=2)}")
            return body
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def products_count_probe(self) -> dict[str, Any]:
        return self.graphql(PRODUCTS_COUNT_QUERY, {"query": PRODUCT_BODY_QUERY})

    def fetch_products(self) -> list[ProductRecord]:
        products: list[ProductRecord] = []
        cursor: str | None = None
        while True:
            body = self.graphql(PRODUCTS_QUERY, {"cursor": cursor})
            connection = body["data"]["products"]
            for node in connection["nodes"]:
                products.append(
                    ProductRecord(
                        id=str(node.get("id") or ""),
                        legacy_resource_id=str(node.get("legacyResourceId") or ""),
                        handle=str(node.get("handle") or ""),
                        title=str(node.get("title") or ""),
                        status=str(node.get("status") or ""),
                        updated_at=str(node.get("updatedAt") or ""),
                        description_html=str(node.get("descriptionHtml") or ""),
                    )
                )
            if not connection["pageInfo"]["hasNextPage"]:
                break
            cursor = connection["pageInfo"]["endCursor"]
            time.sleep(0.05)
        return products

    def update_description(self, product_id: str, description_html: str) -> dict[str, Any]:
        body = self.graphql(
            PRODUCT_UPDATE_MUTATION,
            {"product": {"id": product_id, "descriptionHtml": description_html}},
        )
        payload = body["data"]["productUpdate"]
        if payload.get("userErrors"):
            raise RuntimeError(f"productUpdate userErrors: {json.dumps(payload['userErrors'], indent=2)}")
        return payload["product"]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_text(tag: Tag) -> str:
    return " ".join(tag.get_text(" ", strip=True).split())


def is_blank_string(node: Any) -> bool:
    return isinstance(node, NavigableString) and not str(node).strip()


def previous_content_sibling(node: Tag) -> Any:
    sibling = node.previous_sibling
    while sibling is not None and is_blank_string(sibling):
        sibling = sibling.previous_sibling
    return sibling


def next_content_sibling(node: Tag) -> Any:
    sibling = node.next_sibling
    while sibling is not None and is_blank_string(sibling):
        sibling = sibling.next_sibling
    return sibling


def remove_with_adjacent_whitespace(node: Tag) -> None:
    for sibling in (node.previous_sibling, node.next_sibling):
        if is_blank_string(sibling):
            sibling.extract()
    node.extract()


def table_looks_like_size_chart(table: Tag) -> bool:
    table_id = " ".join(
        str(value)
        for value in (
            table.get("id") or "",
            " ".join(table.get("class") or []),
            normalized_text(table)[:300],
        )
    )
    if SIZE_CHART_RE.search(table_id):
        return True
    previous = previous_content_sibling(table)
    return isinstance(previous, Tag) and SIZE_CHART_RE.search(normalized_text(previous))


def size_chart_sections(soup: BeautifulSoup) -> list[tuple[Tag | None, Tag]]:
    sections: list[tuple[Tag | None, Tag]] = []
    for table in soup.find_all("table"):
        if not table_looks_like_size_chart(table):
            continue
        heading = previous_content_sibling(table)
        if isinstance(heading, Tag) and heading.name in {"h2", "h3", "h4"} and SIZE_CHART_RE.search(
            normalized_text(heading)
        ):
            sections.append((heading, table))
        else:
            sections.append((None, table))
    return sections


def strip_trailing_policy_boilerplate(soup: BeautifulSoup) -> list[str]:
    removed: list[str] = []
    while True:
        body_children = [child for child in soup.contents if isinstance(child, Tag)]
        if not body_children:
            break
        candidate = body_children[-1]
        text = normalized_text(candidate)
        if not text or not POLICY_TEXT_RE.search(text):
            break
        removed.append(text[:180])
        remove_with_adjacent_whitespace(candidate)
    return removed


def trim_description_html(description_html: str, max_length: int) -> tuple[str, dict[str, Any]]:
    soup = BeautifulSoup(description_html or "", "html.parser")
    removed_policy = strip_trailing_policy_boilerplate(soup)
    removed_charts: list[str] = []

    def current_html() -> str:
        return soup.decode(formatter="html")

    while len(current_html()) > max_length:
        sections = size_chart_sections(soup)
        if len(sections) <= 1:
            break
        heading, table = sections[-1]
        label = normalized_text(heading) if heading else normalized_text(table)[:80]
        removed_charts.append(label)
        remove_with_adjacent_whitespace(table)
        if heading and heading.parent:
            remove_with_adjacent_whitespace(heading)

    while len(current_html()) > max_length:
        sections = size_chart_sections(soup)
        if not sections:
            break
        heading, table = sections[-1]
        label = normalized_text(heading) if heading else normalized_text(table)[:80]
        removed_charts.append(label)
        remove_with_adjacent_whitespace(table)
        if heading and heading.parent:
            remove_with_adjacent_whitespace(heading)

    remaining_charts = []
    for heading, table in size_chart_sections(soup):
        if heading:
            remaining_charts.append(normalized_text(heading))
        else:
            remaining_charts.append(normalized_text(table)[:80])

    while len(current_html()) > max_length:
        body_children = [child for child in soup.contents if isinstance(child, Tag)]
        if not body_children:
            break
        candidate = body_children[-1]
        text = normalized_text(candidate)
        if not text:
            remove_with_adjacent_whitespace(candidate)
            continue
        if candidate.name == "table":
            break
        removed_policy.append(f"tail:{text[:180]}")
        remove_with_adjacent_whitespace(candidate)

    trimmed_html = current_html().strip()
    return trimmed_html, {
        "removed_policy_or_tail_blocks": removed_policy,
        "removed_size_chart_sections": removed_charts,
        "remaining_size_chart_sections": remaining_charts,
        "final_table_count": len(soup.find_all("table")),
    }


def product_is_source_candidate(product: ProductRecord) -> bool:
    if product.status == "ARCHIVED":
        return False
    return product.handle.endswith(SOURCE_HANDLE_SUFFIX)


def select_targets(products: list[ProductRecord], threshold: int) -> list[ProductRecord]:
    targets = [
        product
        for product in products
        if product_is_source_candidate(product)
        and (product.length > threshold or product.handle in REQUESTED_HANDLES)
    ]
    return sorted(targets, key=lambda product: (-product.length, product.handle))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trim long current source product body_html values.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help="Initial long-body threshold.")
    parser.add_argument("--max-length", type=int, default=DEFAULT_MAX_LENGTH, help="Target maximum HTML length.")
    parser.add_argument("--expected-count", type=int, default=DEFAULT_EXPECTED_COUNT, help="Abort if target count differs.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="JSON report path.")
    parser.add_argument("--execute", action="store_true", help="Apply product description updates live.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    count_probe = client.products_count_probe()
    products = client.fetch_products()
    targets = select_targets(products, args.threshold)
    if len(targets) != args.expected_count:
        raise SystemExit(
            f"Expected {args.expected_count} targets, found {len(targets)}: "
            + ", ".join(product.handle for product in targets)
        )

    report_items: list[dict[str, Any]] = []
    for product in targets:
        trimmed_html, trim_info = trim_description_html(product.description_html, args.max_length)
        item = {
            "id": product.id,
            "legacy_resource_id": product.legacy_resource_id,
            "handle": product.handle,
            "title": product.title,
            "status": product.status,
            "before_updated_at": product.updated_at,
            "before_length": product.length,
            "after_length_planned": len(trimmed_html),
            "before_sha256": sha256_text(product.description_html),
            "after_sha256_planned": sha256_text(trimmed_html),
            "changed": trimmed_html != product.description_html,
            "requested_handle_below_threshold": product.handle in REQUESTED_HANDLES and product.length <= args.threshold,
            **trim_info,
        }
        if args.execute and item["changed"]:
            updated_product = client.update_description(product.id, trimmed_html)
            updated_html = str(updated_product.get("descriptionHtml") or "")
            item.update(
                {
                    "applied": True,
                    "after_updated_at": updated_product.get("updatedAt"),
                    "after_length_readback": len(updated_html),
                    "after_sha256_readback": sha256_text(updated_html),
                    "readback_matches_plan": updated_html == trimmed_html,
                }
            )
            time.sleep(0.15)
        else:
            item["applied"] = False
        report_items.append(item)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_version": API_VERSION,
        "execute": bool(args.execute),
        "selection": {
            "threshold": args.threshold,
            "max_length": args.max_length,
            "expected_count": args.expected_count,
            "source_handle_suffix": SOURCE_HANDLE_SUFFIX,
            "requested_handles": sorted(REQUESTED_HANDLES),
            "products_count_query": PRODUCT_BODY_QUERY,
            "products_count_probe": count_probe,
            "note": (
                "Shopify currently returns an invalid_field warning for the body_html productsCount "
                "search filter, so target selection is verified by direct descriptionHtml length reads."
            ),
        },
        "summary": {
            "total_products_read": len(products),
            "target_count": len(targets),
            "changed_count": sum(1 for item in report_items if item["changed"]),
            "applied_count": sum(1 for item in report_items if item.get("applied")),
            "max_after_length_planned": max(item["after_length_planned"] for item in report_items),
            "still_over_target_planned": [
                item["handle"] for item in report_items if item["after_length_planned"] > args.max_length
            ],
        },
        "products": report_items,
    }
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "execute": bool(args.execute),
                "target_count": len(targets),
                "changed_count": report["summary"]["changed_count"],
                "applied_count": report["summary"]["applied_count"],
                "max_after_length_planned": report["summary"]["max_after_length_planned"],
                "still_over_target_planned": report["summary"]["still_over_target_planned"],
                "output": str(output_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
