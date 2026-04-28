#!/usr/bin/env python3
"""Plan/apply Shopify fixes for Pinterest Warning 188.

Default mode is dry-run only. Live writes require explicit apply flags plus
--approved so the generated CSV can be reviewed first.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-04"
TIMEOUT_SECONDS = 90
VARIANT_PAGE_SIZE = 250
PRODUCT_PAGE_SIZE = 100
VARIANT_MUTATION_BATCH_SIZE = 100
DEFAULT_OUTPUT_PREFIX = Path("ops/reports/pinterest-warning-188-2026-04-28")
BODY_HTML_FILTER_QUERY = "body_html:>10000"

PRICE_CHANGE_FIELDS = [
    "variant_id",
    "product_title",
    "old_price",
    "old_cap",
    "new_cap",
    "reason",
]

PRODUCT_VARIANTS_QUERY = """
query ProductVariants(
  $first: Int!,
  $after: String,
  $onlinePublicationId: ID!,
  $pinterestPublicationId: ID!
) {
  productVariants(first: $first, after: $after) {
    nodes {
      id
      price
      compareAtPrice
      product {
        id
        title
        handle
        status
        onlineStorePublished: publishedOnPublication(publicationId: $onlinePublicationId)
        pinterestPublished: publishedOnPublication(publicationId: $pinterestPublicationId)
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

DISCOVER_PUBLICATIONS_QUERY = """
query DiscoverPublications {
  publications(first: 50) {
    nodes {
      id
      name
    }
  }
}
"""

UPDATE_VARIANTS_MUTATION = """
mutation UpdateCompareAtPrices($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(
    productId: $productId,
    variants: $variants,
    allowPartialUpdates: false
  ) {
    product {
      id
      title
      handle
    }
    productVariants {
      id
      price
      compareAtPrice
    }
    userErrors {
      field
      message
    }
  }
}
"""

PRODUCTS_COUNT_QUERY = """
query ProductsCount($query: String!) {
  productsCount(query: $query) {
    count
  }
}
"""

PRODUCTS_QUERY = """
query Products($first: Int!, $after: String) {
  products(first: $first, after: $after, sortKey: ID) {
    nodes {
      id
      handle
      title
      descriptionHtml
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

UPDATE_PRODUCT_BODY_MUTATION = """
mutation UpdateProductBody($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      title
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
class VariantRecord:
    variant_id: str
    product_id: str
    product_handle: str
    product_title: str
    product_status: str
    online_store_published: bool
    pinterest_published: bool
    price: Decimal
    compare_at_price: Decimal | None


@dataclass
class PriceChange:
    variant_id: str
    product_title: str
    old_price: str
    old_cap: str
    new_cap: str
    reason: str
    product_id: str
    product_handle: str
    product_status: str
    online_store_published: bool
    pinterest_published: bool

    def csv_row(self) -> dict[str, str]:
        return {field: getattr(self, field) for field in PRICE_CHANGE_FIELDS}


@dataclass
class BodyHtmlPlan:
    product_id: str
    handle: str
    title: str
    old_body_html_length: int
    new_body_html_length: int
    removed_chars: int
    output_html_path: str
    reason: str


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str, api_version: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
        self.access_token = access_token

    def graphql_raw(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(7):
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 6:
                    time.sleep(min(20.0, (1.7**attempt) + random.uniform(0.2, 0.8)))
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {response_body}") from exc

            errors = body.get("errors") or []
            error_codes = {item.get("extensions", {}).get("code") for item in errors}
            if "THROTTLED" in error_codes and attempt < 6:
                time.sleep(min(20.0, (1.7**attempt) + random.uniform(0.2, 0.8)))
                continue
            if errors:
                raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(errors, ensure_ascii=False)}")
            return body

        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.graphql_raw(query, variables).get("data") or {}


def clean(value: Any) -> str:
    return str(value or "").strip()


def parse_money(value: Any) -> Decimal | None:
    text = clean(value)
    if not text:
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        raise ValueError(f"Could not parse Shopify money value: {value!r}") from None


def format_money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"


def chunked(items: list[Any], size: int) -> Iterable[list[Any]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def resolve_publication_ids(client: ShopifyClient) -> dict[str, str]:
    nodes = client.graphql(DISCOVER_PUBLICATIONS_QUERY)["publications"].get("nodes") or []
    by_name = {clean(node.get("name")): clean(node.get("id")) for node in nodes}
    missing = [name for name in ("Online Store", "Pinterest") if not by_name.get(name)]
    if missing:
        raise RuntimeError(f"Could not find Shopify publication IDs for: {', '.join(missing)}")
    return {
        "online_store": by_name["Online Store"],
        "pinterest": by_name["Pinterest"],
    }


def iter_variants(
    client: ShopifyClient,
    *,
    online_publication_id: str,
    pinterest_publication_id: str,
    limit: int = 0,
) -> Iterable[VariantRecord]:
    after: str | None = None
    seen = 0
    while True:
        data = client.graphql(
            PRODUCT_VARIANTS_QUERY,
            {
                "first": VARIANT_PAGE_SIZE,
                "after": after,
                "onlinePublicationId": online_publication_id,
                "pinterestPublicationId": pinterest_publication_id,
            },
        )["productVariants"]
        for node in data.get("nodes") or []:
            product = node.get("product") or {}
            price = parse_money(node.get("price"))
            if price is None:
                continue
            yield VariantRecord(
                variant_id=clean(node.get("id")),
                product_id=clean(product.get("id")),
                product_handle=clean(product.get("handle")),
                product_title=clean(product.get("title")),
                product_status=clean(product.get("status")),
                online_store_published=bool(product.get("onlineStorePublished")),
                pinterest_published=bool(product.get("pinterestPublished")),
                price=price,
                compare_at_price=parse_money(node.get("compareAtPrice")),
            )
            seen += 1
            if limit and seen >= limit:
                return
        page_info = data.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            return
        after = clean(page_info.get("endCursor"))


def is_target_publication_variant(variant: VariantRecord) -> bool:
    return (
        variant.product_status == "ACTIVE"
        and variant.online_store_published
        and variant.pinterest_published
    )


def plan_price_changes(
    variants: Iterable[VariantRecord],
    *,
    include_archived_products: bool,
) -> tuple[list[PriceChange], dict[str, Any]]:
    changes: list[PriceChange] = []
    stats: Counter[str] = Counter()
    skipped_product_ids: set[str] = set()
    for variant in variants:
        stats["scanned_variants"] += 1
        cap = variant.compare_at_price
        if cap is None or cap > variant.price:
            continue
        stats["invalid_compare_at_price_variants"] += 1

        if not include_archived_products and not is_target_publication_variant(variant):
            stats["skipped_out_of_scope_invalid_variants"] += 1
            skipped_product_ids.add(variant.product_id)
            continue

        if cap == variant.price:
            new_cap = ""
            reason = "clear_equal_compare_at_price"
        elif cap <= Decimal("0.01"):
            new_cap = ""
            reason = "clear_near_zero_compare_at_price"
        elif variant.price > 0 and ((variant.price - cap) / variant.price) < Decimal("0.30"):
            new_cap = format_money(variant.price * Decimal("1.35"))
            reason = "raise_close_lower_compare_at_price_to_price_times_1_35"
        else:
            new_cap = ""
            reason = "clear_probable_wholesale_cost_compare_at_price"

        changes.append(
            PriceChange(
                variant_id=variant.variant_id,
                product_title=variant.product_title,
                old_price=format_money(variant.price),
                old_cap=format_money(cap),
                new_cap=new_cap,
                reason=reason,
                product_id=variant.product_id,
                product_handle=variant.product_handle,
                product_status=variant.product_status,
                online_store_published=variant.online_store_published,
                pinterest_published=variant.pinterest_published,
            )
        )
    stats["target_invalid_variant_changes"] = len(changes)
    return changes, {
        **dict(stats),
        "skipped_out_of_scope_product_count": len(skipped_product_ids),
        "scope": (
            "all products including archived"
            if include_archived_products
            else "ACTIVE products published to both Online Store and Pinterest"
        ),
    }


def write_price_outputs(changes: list[PriceChange], output_prefix: Path) -> tuple[Path, Path]:
    csv_path = output_prefix.with_name(f"{output_prefix.name}-price-changes.csv")
    json_path = output_prefix.with_name(f"{output_prefix.name}-price-plan.json")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PRICE_CHANGE_FIELDS)
        writer.writeheader()
        writer.writerows(change.csv_row() for change in changes)
    json_path.write_text(
        json.dumps([asdict(change) for change in changes], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return csv_path, json_path


def apply_price_changes(client: ShopifyClient, changes: list[PriceChange]) -> dict[str, Any]:
    by_product: dict[str, list[PriceChange]] = defaultdict(list)
    for change in changes:
        by_product[change.product_id].append(change)

    product_results: list[dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    for product_id, product_changes in sorted(by_product.items()):
        for batch in chunked(product_changes, VARIANT_MUTATION_BATCH_SIZE):
            variants = [
                {
                    "id": change.variant_id,
                    "compareAtPrice": change.new_cap or None,
                }
                for change in batch
            ]
            data = client.graphql(
                UPDATE_VARIANTS_MUTATION,
                {"productId": product_id, "variants": variants},
            )["productVariantsBulkUpdate"]
            user_errors = data.get("userErrors") or []
            if user_errors:
                failure_count += len(batch)
            else:
                success_count += len(batch)
            product_results.append(
                {
                    "product_id": product_id,
                    "product_handle": batch[0].product_handle if batch else "",
                    "batch_size": len(batch),
                    "updated_variant_ids": [item.get("id") for item in data.get("productVariants") or []],
                    "userErrors": user_errors,
                }
            )
            time.sleep(0.1)

    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "product_batches": product_results,
    }


def products_count_probe(client: ShopifyClient) -> dict[str, Any]:
    raw = client.graphql_raw(PRODUCTS_COUNT_QUERY, {"query": BODY_HTML_FILTER_QUERY})
    return {
        "query": BODY_HTML_FILTER_QUERY,
        "count": ((raw.get("data") or {}).get("productsCount") or {}).get("count"),
        "search_extensions": (raw.get("extensions") or {}).get("search") or [],
    }


def iter_products(client: ShopifyClient, limit: int = 0) -> Iterable[dict[str, Any]]:
    after: str | None = None
    seen = 0
    while True:
        data = client.graphql(PRODUCTS_QUERY, {"first": PRODUCT_PAGE_SIZE, "after": after})["products"]
        for node in data.get("nodes") or []:
            yield node
            seen += 1
            if limit and seen >= limit:
                return
        page_info = data.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            return
        after = clean(page_info.get("endCursor"))


def remove_bottom_boilerplate(html: str) -> tuple[str, list[str]]:
    markers = [
        r"<h[1-6][^>]*>\s*(?:Shipping|Delivery|Processing|Returns?|Refunds?|Customer Service|Notes?)\b.*?</h[1-6]>",
        r"<p[^>]*>\s*(?:Shipping|Delivery|Processing|Returns?|Refunds?|Customer Service|Notes?)\b",
    ]
    lowered = html.lower()
    cut_at: int | None = None
    for marker in markers:
        for match in re.finditer(marker, html, flags=re.IGNORECASE | re.DOTALL):
            if match.start() > len(html) * 0.45:
                cut_at = match.start() if cut_at is None else min(cut_at, match.start())
    if cut_at is None:
        return html, []
    return html[:cut_at].rstrip(), ["removed_bottom_shipping_or_policy_boilerplate"]


def remove_tail_after_last_table(html: str) -> tuple[str, list[str]]:
    last_table_end = html.lower().rfind("</table>")
    if last_table_end < 0:
        return html, []
    tail = html[last_table_end + len("</table>") :].strip()
    if not tail:
        return html, []
    if re.search(r"<h[1-6][^>]*>\s*Key Features:?\s*</h[1-6]>", tail, flags=re.IGNORECASE) or len(tail) > 500:
        return html[: last_table_end + len("</table>")].rstrip(), ["removed_repeated_marketing_copy_after_size_charts"]
    return html, []


def remove_duplicate_size_chart_tables(html: str) -> tuple[str, list[str]]:
    pattern = re.compile(
        r"(?P<section><h[1-6][^>]*>\s*(?P<title>Size\s+Chart[^<]*)</h[1-6]>\s*<table\b.*?</table>)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    seen_titles: set[str] = set()
    remove_spans: list[tuple[int, int]] = []
    for match in pattern.finditer(html):
        title = re.sub(r"\s+", " ", match.group("title")).strip().lower()
        if title in seen_titles:
            remove_spans.append(match.span("section"))
        else:
            seen_titles.add(title)
    if not remove_spans:
        return html, []
    pieces: list[str] = []
    last = 0
    for start, end in remove_spans:
        pieces.append(html[last:start])
        last = end
    pieces.append(html[last:])
    return "".join(pieces).strip(), ["removed_duplicate_size_chart_tables"]


def remove_trailing_size_chart_sections(html: str, target_length: int) -> tuple[str, list[str]]:
    reasons: list[str] = []
    pattern = re.compile(
        r"<h[1-6][^>]*>\s*Size\s+Chart[^<]*</h[1-6]>\s*<table\b.*?</table>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    working = html
    while len(working) > target_length:
        matches = list(pattern.finditer(working))
        if len(matches) <= 1:
            break
        match = matches[-1]
        working = (working[: match.start()] + working[match.end() :]).rstrip()
        reasons.append("removed_trailing_size_chart_table_to_meet_length")
    return working, reasons


def trim_to_block_boundary(html: str, target_length: int) -> tuple[str, list[str]]:
    if len(html) <= target_length:
        return html, []
    boundary_tags = ("</table>", "</ul>", "</ol>", "</p>", "</div>", "</section>")
    lower_html = html.lower()
    best_index = -1
    for tag in boundary_tags:
        index = lower_html.rfind(tag, 0, target_length)
        if index >= 0:
            best_index = max(best_index, index + len(tag))
    if best_index < 0:
        best_index = target_length
    return html[:best_index].rstrip(), ["truncated_at_safe_html_block_boundary"]


def trim_description_html(html: str, target_length: int) -> tuple[str, str]:
    working = html.strip()
    reasons: list[str] = []

    for transform in (remove_bottom_boilerplate, remove_tail_after_last_table, remove_duplicate_size_chart_tables):
        working, transform_reasons = transform(working)
        reasons.extend(transform_reasons)

    working, transform_reasons = remove_trailing_size_chart_sections(working, target_length)
    reasons.extend(transform_reasons)

    working, transform_reasons = trim_to_block_boundary(working, target_length)
    reasons.extend(transform_reasons)

    return working.strip(), "; ".join(reasons or ["trimmed_to_body_html_length_target"])


def plan_body_html_changes(
    products: Iterable[dict[str, Any]],
    output_prefix: Path,
    *,
    min_length: int,
    target_length: int,
    handle_filter: set[str],
) -> list[BodyHtmlPlan]:
    output_dir = output_prefix.with_name(f"{output_prefix.name}-body-html")
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale_html in output_dir.glob("*.html"):
        stale_html.unlink()
    plans: list[BodyHtmlPlan] = []
    for product in products:
        handle = clean(product.get("handle"))
        if handle_filter and handle not in handle_filter:
            continue
        body_html = clean(product.get("descriptionHtml"))
        if len(body_html) <= target_length:
            continue
        if len(body_html) <= min_length and not handle_filter:
            continue
        trimmed, reason = trim_description_html(body_html, target_length)
        if trimmed == body_html:
            continue
        html_path = output_dir / f"{handle}.html"
        html_path.write_text(trimmed, encoding="utf-8")
        plans.append(
            BodyHtmlPlan(
                product_id=clean(product.get("id")),
                handle=handle,
                title=clean(product.get("title")),
                old_body_html_length=len(body_html),
                new_body_html_length=len(trimmed),
                removed_chars=len(body_html) - len(trimmed),
                output_html_path=str(html_path),
                reason=reason,
            )
        )
    return plans


def write_body_outputs(plans: list[BodyHtmlPlan], output_prefix: Path) -> Path:
    csv_path = output_prefix.with_name(f"{output_prefix.name}-body-html-changes.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "product_id",
            "handle",
            "title",
            "old_body_html_length",
            "new_body_html_length",
            "removed_chars",
            "output_html_path",
            "reason",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(plan) for plan in plans)
    return csv_path


def apply_body_html_changes(client: ShopifyClient, plans: list[BodyHtmlPlan]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    success_count = 0
    failure_count = 0
    for plan in plans:
        new_html = Path(plan.output_html_path).read_text(encoding="utf-8")
        data = client.graphql(
            UPDATE_PRODUCT_BODY_MUTATION,
            {"product": {"id": plan.product_id, "descriptionHtml": new_html}},
        )["productUpdate"]
        user_errors = data.get("userErrors") or []
        if user_errors:
            failure_count += 1
        else:
            success_count += 1
        results.append(
            {
                "product_id": plan.product_id,
                "handle": plan.handle,
                "old_body_html_length": plan.old_body_html_length,
                "new_body_html_length": plan.new_body_html_length,
                "userErrors": user_errors,
            }
        )
        time.sleep(0.1)
    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "product_results": results,
    }


def parse_handles(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run/apply Shopify fixes for Pinterest Warning 188.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--api-version", default=API_VERSION, help="Shopify Admin API version.")
    parser.add_argument("--output-prefix", default=str(DEFAULT_OUTPUT_PREFIX), help="Report path prefix.")
    parser.add_argument("--apply-prices", action="store_true", help="Apply compare_at_price changes live.")
    parser.add_argument("--apply-body-html", action="store_true", help="Apply body_html trims live.")
    parser.add_argument("--approved", action="store_true", help="Required guard for live write modes.")
    parser.add_argument("--skip-prices", action="store_true", help="Skip variant price dry-run planning.")
    parser.add_argument("--skip-body-html", action="store_true", help="Skip body_html dry-run planning.")
    parser.add_argument(
        "--include-archived-products",
        action="store_true",
        help="Include archived/out-of-channel products in the compare_at_price plan.",
    )
    parser.add_argument("--body-min-length", type=int, default=10000, help="Minimum live body_html length to plan.")
    parser.add_argument("--body-target-length", type=int, default=8000, help="Target body_html length after trimming.")
    parser.add_argument("--body-handles", default="", help="Comma-separated handles to plan, regardless of length.")
    parser.add_argument("--limit-variants", type=int, default=0, help="Debug limit for variants fetched.")
    parser.add_argument("--limit-products", type=int, default=0, help="Debug limit for products fetched.")
    args = parser.parse_args()

    if (args.apply_prices or args.apply_body_html) and not args.approved:
        raise SystemExit("Live writes require --approved after reviewing the dry-run CSV artifacts.")

    output_prefix = Path(args.output_prefix)
    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token, args.api_version)

    summary: dict[str, Any] = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "store_domain": store_domain,
        "api_version": args.api_version,
        "dry_run": not (args.apply_prices or args.apply_body_html),
        "publication_ids": None,
        "price_changes": None,
        "body_html_changes": None,
        "apply_results": {},
    }

    price_changes: list[PriceChange] = []
    if not args.skip_prices:
        publication_ids = resolve_publication_ids(client)
        summary["publication_ids"] = publication_ids
        price_changes, price_stats = plan_price_changes(
            iter_variants(
                client,
                online_publication_id=publication_ids["online_store"],
                pinterest_publication_id=publication_ids["pinterest"],
                limit=args.limit_variants,
            ),
            include_archived_products=args.include_archived_products,
        )
        price_csv_path, price_json_path = write_price_outputs(price_changes, output_prefix)
        price_reason_counts: dict[str, int] = defaultdict(int)
        product_ids: set[str] = set()
        for change in price_changes:
            price_reason_counts[change.reason] += 1
            product_ids.add(change.product_id)
        summary["price_changes"] = {
            "variant_change_count": len(price_changes),
            "product_count": len(product_ids),
            "reason_counts": dict(sorted(price_reason_counts.items())),
            "scan_stats": price_stats,
            "csv": str(price_csv_path),
            "json": str(price_json_path),
        }
        if args.apply_prices:
            summary["apply_results"]["prices"] = apply_price_changes(client, price_changes)

    body_plans: list[BodyHtmlPlan] = []
    if not args.skip_body_html:
        count_probe = products_count_probe(client)
        body_plans = plan_body_html_changes(
            iter_products(client, args.limit_products),
            output_prefix,
            min_length=args.body_min_length,
            target_length=args.body_target_length,
            handle_filter=parse_handles(args.body_handles),
        )
        body_csv_path = write_body_outputs(body_plans, output_prefix)
        summary["body_html_changes"] = {
            "products_count_probe": count_probe,
            "product_change_count": len(body_plans),
            "csv": str(body_csv_path),
            "html_output_dir": str(output_prefix.with_name(f"{output_prefix.name}-body-html")),
            "old_total_chars": sum(plan.old_body_html_length for plan in body_plans),
            "new_total_chars": sum(plan.new_body_html_length for plan in body_plans),
        }
        if args.apply_body_html:
            summary["apply_results"]["body_html"] = apply_body_html_changes(client, body_plans)

    summary_path = output_prefix.with_name(f"{output_prefix.name}-summary.json")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary["summary_json"] = str(summary_path)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
