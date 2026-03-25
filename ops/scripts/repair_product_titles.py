#!/usr/bin/env python3
"""Repair Shopify product titles from a clean reference export.

Default mode is dry-run. Live updates require:
  - SHOPIFY_STORE_DOMAIN (for example: dresslikemommy-com.myshopify.com)
  - SHOPIFY_ADMIN_ACCESS_TOKEN

The script is intentionally conservative:
  - it targets active products by default,
  - it only proposes updates when the current title shows corruption markers
    such as ``| DLM`` or ``...``,
  - it restores the title from a handle-matched reference export,
  - in execute mode it skips products whose live title no longer matches the
    expected broken title unless ``--force`` is supplied.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
from urllib import error, request


ROW_HANDLE = "Handle"
ROW_STATUS = "Status"
ROW_PUBLISHED = "Published"
ROW_TITLE = "Title"

DEFAULT_CURRENT_EXPORT = Path("products_export_1 2.csv")
DEFAULT_REFERENCE_EXPORT = Path("GPT/products_export_1.csv")
DEFAULT_API_VERSION = os.environ.get("SHOPIFY_ADMIN_API_VERSION", "2025-10")
DEFAULT_TIMEOUT_SECONDS = 30

ACTIVE_STATUS = "active"
TRUE_VALUES = {"1", "true", "yes", "y"}
BROKEN_TITLE_PATTERNS: Sequence[Tuple[str, re.Pattern[str]]] = (
    (
        "dlm_suffix",
        re.compile(r"\|\s*(dlm|dress like mommy)\b", flags=re.IGNORECASE),
    ),
    ("ellipsis", re.compile(r"\.{3,}")),
)

PRODUCT_BY_IDENTIFIER_QUERY = """
query ProductByIdentifier($identifier: ProductIdentifierInput!) {
  product: productByIdentifier(identifier: $identifier) {
    id
    handle
    title
    status
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation UpdateProductTitle($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      title
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass(frozen=True)
class ProductRecord:
    handle: str
    title: str
    status: str
    published: bool


@dataclass(frozen=True)
class PlannedRepair:
    handle: str
    current_title: str
    replacement_title: str
    reasons: Tuple[str, ...]
    status: str
    published: bool


@dataclass
class ExecutionResult:
    handle: str
    action: str
    reason: str
    live_title_before: str = ""
    live_title_after: str = ""


def clean(value: str) -> str:
    return (value or "").strip()


def normalized_key(value: str) -> str:
    return clean(value).lower()


def parse_bool(value: str) -> bool:
    return normalized_key(value) in TRUE_VALUES


def load_products(path: Path) -> Dict[str, ProductRecord]:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")

    products: Dict[str, ProductRecord] = {}
    for row in rows:
        handle_value = clean(row.get(ROW_HANDLE, ""))
        if not handle_value:
            continue

        record = ProductRecord(
            handle=handle_value,
            title=clean(row.get(ROW_TITLE, "")),
            status=normalized_key(row.get(ROW_STATUS, "")),
            published=parse_bool(row.get(ROW_PUBLISHED, "")),
        )

        existing = products.get(handle_value)
        if existing is None:
            products[handle_value] = record
            continue

        if existing.status != ACTIVE_STATUS and record.status == ACTIVE_STATUS:
            products[handle_value] = record
            continue

        if not existing.title and record.title:
            products[handle_value] = record

    return products


def broken_title_reasons(title: str) -> Tuple[str, ...]:
    reasons = [
        label for label, pattern in BROKEN_TITLE_PATTERNS if pattern.search(clean(title))
    ]
    return tuple(reasons)


def is_active(record: ProductRecord) -> bool:
    return record.status == ACTIVE_STATUS


def build_plan(
    current_products: Dict[str, ProductRecord],
    reference_products: Dict[str, ProductRecord],
    *,
    active_only: bool,
    published_only: bool,
    all_differences: bool,
) -> Tuple[List[PlannedRepair], Dict[str, int]]:
    plan: List[PlannedRepair] = []
    metrics = {
        "current_products": len(current_products),
        "reference_products": len(reference_products),
        "scanned": 0,
        "skipped_inactive": 0,
        "skipped_unpublished": 0,
        "skipped_clean": 0,
        "missing_reference": 0,
        "blank_reference": 0,
        "same_as_reference": 0,
        "planned_repairs": 0,
    }

    for handle in sorted(current_products.keys()):
        current = current_products[handle]
        if active_only and not is_active(current):
            metrics["skipped_inactive"] += 1
            continue
        if published_only and not current.published:
            metrics["skipped_unpublished"] += 1
            continue

        metrics["scanned"] += 1
        reasons = broken_title_reasons(current.title)
        if not all_differences and not reasons:
            metrics["skipped_clean"] += 1
            continue

        reference = reference_products.get(handle)
        if reference is None:
            metrics["missing_reference"] += 1
            continue

        replacement_title = clean(reference.title)
        if not replacement_title:
            metrics["blank_reference"] += 1
            continue

        if replacement_title == current.title:
            metrics["same_as_reference"] += 1
            continue

        if all_differences and not reasons:
            reasons = ("reference_diff",)

        plan.append(
            PlannedRepair(
                handle=handle,
                current_title=current.title,
                replacement_title=replacement_title,
                reasons=reasons,
                status=current.status,
                published=current.published,
            )
        )

    metrics["planned_repairs"] = len(plan)
    return plan, metrics


def write_plan_csv(path: Path, plan: Sequence[PlannedRepair]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "handle",
                "current_title",
                "replacement_title",
                "reasons",
                "status",
                "published",
            ],
        )
        writer.writeheader()
        for item in plan:
            writer.writerow(
                {
                    "handle": item.handle,
                    "current_title": item.current_title,
                    "replacement_title": item.replacement_title,
                    "reasons": ",".join(item.reasons),
                    "status": item.status,
                    "published": str(item.published).lower(),
                }
            )


def graphql_request(
    *,
    store_domain: str,
    access_token: str,
    api_version: str,
    query: str,
    variables: Dict[str, object],
    timeout_seconds: int,
) -> Dict[str, object]:
    url = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
    )

    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify API HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Shopify API request failed: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Shopify API returned invalid JSON") from exc

    if data.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {data['errors']}")

    return data


def fetch_live_product(
    *,
    store_domain: str,
    access_token: str,
    api_version: str,
    handle: str,
    timeout_seconds: int,
) -> Optional[Dict[str, object]]:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=PRODUCT_BY_IDENTIFIER_QUERY,
        variables={"identifier": {"handle": handle}},
        timeout_seconds=timeout_seconds,
    )
    return data.get("data", {}).get("product")


def update_live_product_title(
    *,
    store_domain: str,
    access_token: str,
    api_version: str,
    product_id: str,
    replacement_title: str,
    timeout_seconds: int,
) -> Tuple[Optional[Dict[str, object]], List[Dict[str, object]]]:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=PRODUCT_UPDATE_MUTATION,
        variables={"product": {"id": product_id, "title": replacement_title}},
        timeout_seconds=timeout_seconds,
    )
    payload = data.get("data", {}).get("productUpdate", {})
    product = payload.get("product")
    user_errors = payload.get("userErrors", [])
    return product, user_errors


def execute_plan(
    plan: Sequence[PlannedRepair],
    *,
    store_domain: str,
    access_token: str,
    api_version: str,
    timeout_seconds: int,
    pause_ms: int,
    force: bool,
    max_updates: Optional[int],
) -> List[ExecutionResult]:
    results: List[ExecutionResult] = []
    updates_applied = 0

    for item in plan:
        if max_updates is not None and updates_applied >= max_updates:
            results.append(
                ExecutionResult(
                    handle=item.handle,
                    action="skipped",
                    reason="max_updates_reached",
                )
            )
            continue

        live_product = fetch_live_product(
            store_domain=store_domain,
            access_token=access_token,
            api_version=api_version,
            handle=item.handle,
            timeout_seconds=timeout_seconds,
        )
        if live_product is None:
            results.append(
                ExecutionResult(
                    handle=item.handle,
                    action="error",
                    reason="product_not_found",
                )
            )
            continue

        live_title = clean(str(live_product.get("title") or ""))
        product_id = clean(str(live_product.get("id") or ""))
        live_reasons = broken_title_reasons(live_title)

        if live_title == item.replacement_title:
            results.append(
                ExecutionResult(
                    handle=item.handle,
                    action="skipped",
                    reason="already_matches_replacement",
                    live_title_before=live_title,
                    live_title_after=live_title,
                )
            )
            continue

        if not force and live_title not in {item.current_title, ""} and not live_reasons:
            results.append(
                ExecutionResult(
                    handle=item.handle,
                    action="skipped",
                    reason="live_title_drifted",
                    live_title_before=live_title,
                )
            )
            continue

        updated_product, user_errors = update_live_product_title(
            store_domain=store_domain,
            access_token=access_token,
            api_version=api_version,
            product_id=product_id,
            replacement_title=item.replacement_title,
            timeout_seconds=timeout_seconds,
        )
        if user_errors:
            results.append(
                ExecutionResult(
                    handle=item.handle,
                    action="error",
                    reason="; ".join(
                        clean(error_item.get("message", "")) for error_item in user_errors
                    ),
                    live_title_before=live_title,
                )
            )
            continue

        live_after = clean(str((updated_product or {}).get("title") or ""))
        updates_applied += 1
        results.append(
            ExecutionResult(
                handle=item.handle,
                action="updated",
                reason="updated",
                live_title_before=live_title,
                live_title_after=live_after,
            )
        )

        if pause_ms > 0:
            time.sleep(pause_ms / 1000)

    return results


def require_env(name: str) -> str:
    value = clean(os.environ.get(name, ""))
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def summarize_plan(metrics: Dict[str, int], plan: Sequence[PlannedRepair]) -> List[str]:
    lines = [
        f"Current export products: {metrics['current_products']}",
        f"Reference export products: {metrics['reference_products']}",
        f"Scanned products: {metrics['scanned']}",
        f"Planned repairs: {metrics['planned_repairs']}",
        f"Skipped inactive: {metrics['skipped_inactive']}",
        f"Skipped unpublished: {metrics['skipped_unpublished']}",
        f"Skipped clean: {metrics['skipped_clean']}",
        f"Missing reference: {metrics['missing_reference']}",
        f"Blank reference title: {metrics['blank_reference']}",
        f"Same as reference: {metrics['same_as_reference']}",
    ]

    reason_counts: Dict[str, int] = {}
    for item in plan:
        for reason in item.reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    if reason_counts:
        lines.append("Reasons:")
        for reason, count in sorted(reason_counts.items()):
            lines.append(f"  {reason}: {count}")
    return lines


def summarize_execution(results: Sequence[ExecutionResult]) -> List[str]:
    counts: Dict[str, int] = {}
    for item in results:
        counts[item.action] = counts.get(item.action, 0) + 1

    lines = ["Execution summary:"]
    for action, count in sorted(counts.items()):
        lines.append(f"  {action}: {count}")
    return lines


def print_sample_repairs(plan: Sequence[PlannedRepair], limit: int) -> None:
    if not plan:
        return
    sample = plan[:limit]
    print("")
    print(f"Sample repairs (showing {len(sample)} of {len(plan)}):")
    for item in sample:
        print(f"- {item.handle}")
        print(f"  current:     {item.current_title}")
        print(f"  replacement: {item.replacement_title}")
        print(f"  reasons:     {', '.join(item.reasons)}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--current-export",
        type=Path,
        default=DEFAULT_CURRENT_EXPORT,
        help=f"Current Shopify products export CSV (default: {DEFAULT_CURRENT_EXPORT})",
    )
    parser.add_argument(
        "--reference-export",
        type=Path,
        default=DEFAULT_REFERENCE_EXPORT,
        help=f"Reference export CSV with clean titles (default: {DEFAULT_REFERENCE_EXPORT})",
    )
    parser.add_argument(
        "--published-only",
        action="store_true",
        help="Limit planning to products marked Published=true in the current export.",
    )
    parser.add_argument(
        "--all-differences",
        action="store_true",
        help="Plan updates for any title differing from the reference export, not only corrupted titles.",
    )
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include non-active products from the current export.",
    )
    parser.add_argument(
        "--plan-csv",
        type=Path,
        help="Optional path to write the planned repairs as CSV.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=15,
        help="Number of planned repairs to print as examples (default: 15).",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute live Shopify Admin API updates. Dry-run is the default.",
    )
    parser.add_argument(
        "--store-domain",
        default=os.environ.get("SHOPIFY_STORE_DOMAIN", ""),
        help="Shopify myshopify domain. Falls back to SHOPIFY_STORE_DOMAIN.",
    )
    parser.add_argument(
        "--api-version",
        default=DEFAULT_API_VERSION,
        help=f"Shopify Admin API version (default: {DEFAULT_API_VERSION})",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--pause-ms",
        type=int,
        default=0,
        help="Optional pause between live updates in milliseconds.",
    )
    parser.add_argument(
        "--max-updates",
        type=int,
        help="Optional cap on live updates for staged rollouts.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="In execute mode, update even if the live title no longer looks corrupted.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    try:
        current_products = load_products(args.current_export)
        reference_products = load_products(args.reference_export)
        plan, metrics = build_plan(
            current_products,
            reference_products,
            active_only=not args.include_inactive,
            published_only=args.published_only,
            all_differences=args.all_differences,
        )
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for line in summarize_plan(metrics, plan):
        print(line)
    print_sample_repairs(plan, args.sample_limit)

    if args.plan_csv:
        write_plan_csv(args.plan_csv, plan)
        print("")
        print(f"Wrote plan CSV: {args.plan_csv}")

    if not args.execute:
        return 0

    try:
        store_domain = clean(args.store_domain) or require_env("SHOPIFY_STORE_DOMAIN")
        access_token = require_env("SHOPIFY_ADMIN_ACCESS_TOKEN")
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not plan:
        print("")
        print("No repairs to execute.")
        return 0

    results = execute_plan(
        plan,
        store_domain=store_domain,
        access_token=access_token,
        api_version=args.api_version,
        timeout_seconds=args.timeout_seconds,
        pause_ms=args.pause_ms,
        force=args.force,
        max_updates=args.max_updates,
    )

    print("")
    for line in summarize_execution(results):
        print(line)

    sample_results = [item for item in results if item.action != "skipped"][: args.sample_limit]
    if sample_results:
        print("")
        print(f"Execution details (showing {len(sample_results)}):")
        for item in sample_results:
            print(f"- {item.handle}: {item.action} ({item.reason})")
            if item.live_title_before:
                print(f"  before: {item.live_title_before}")
            if item.live_title_after:
                print(f"  after:  {item.live_title_after}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
