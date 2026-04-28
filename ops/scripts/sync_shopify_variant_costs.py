#!/usr/bin/env python3
"""Sync Shopify inventory-item costs to the store's 50% price rule."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import (  # noqa: E402
    load_access_token,
    resolve_store_domain,
)


API_VERSION = "2026-04"
PAGE_SIZE = 100
DEFAULT_COST_RATIO = Decimal("0.50")
CENT = Decimal("0.01")
DEFAULT_OUTPUT_ROOT = Path("dresslikemommy-growth-2026")


PRODUCT_VARIANTS_QUERY = """
query ProductVariantsForCostSync($first: Int!, $after: String, $query: String!) {
  shop {
    currencyCode
  }
  productVariants(first: $first, after: $after, query: $query, sortKey: ID) {
    nodes {
      id
      legacyResourceId
      title
      sku
      price
      inventoryItem {
        id
        legacyResourceId
        unitCost {
          amount
          currencyCode
        }
      }
      product {
        id
        legacyResourceId
        title
        handle
        status
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


PRODUCT_VARIANTS_BULK_UPDATE_MUTATION = """
mutation ProductVariantsCostSync($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(
    productId: $productId,
    variants: $variants,
    allowPartialUpdates: false
  ) {
    productVariants {
      id
      legacyResourceId
      inventoryItem {
        id
        unitCost {
          amount
          currencyCode
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def parse_decimal(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def money(value: Decimal) -> str:
    return format(value.quantize(CENT, rounding=ROUND_HALF_UP), "f")


def desired_cost_from_price(price: Any, ratio: Decimal = DEFAULT_COST_RATIO) -> Decimal | None:
    parsed_price = parse_decimal(price)
    if parsed_price is None or parsed_price <= 0:
        return None
    return (parsed_price * ratio).quantize(CENT, rounding=ROUND_HALF_UP)


def current_unit_cost(variant: dict[str, Any]) -> str:
    unit_cost = ((variant.get("inventoryItem") or {}).get("unitCost")) or {}
    return str(unit_cost.get("amount") or "")


def costs_match(current: str, desired: Decimal) -> bool:
    parsed_current = parse_decimal(current)
    return parsed_current is not None and parsed_current.quantize(CENT) == desired


def normalize_statuses(raw_statuses: str) -> list[str]:
    statuses = []
    for part in raw_statuses.replace(";", ",").split(","):
        status = part.strip().upper()
        if not status:
            continue
        if status not in {"ACTIVE", "DRAFT", "ARCHIVED"}:
            raise ValueError(f"Unsupported product status: {status}")
        statuses.append(status)
    return statuses or ["ACTIVE"]


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str, api_version: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(7):
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
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
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")

            throttle = (body.get("extensions") or {}).get("cost", {}).get("throttleStatus", {})
            currently_available = float(throttle.get("currentlyAvailable", 1000))
            if currently_available < 200:
                time.sleep((200 - currently_available) / 100.0)

            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def fetch_variants(client: ShopifyClient, statuses: list[str]) -> tuple[list[dict[str, Any]], str]:
    variants_by_gid: dict[str, dict[str, Any]] = {}
    currency_code = ""
    for status in statuses:
        after: str | None = None
        query = f"product_status:{status.lower()}"
        while True:
            data = client.graphql(
                PRODUCT_VARIANTS_QUERY,
                {"first": PAGE_SIZE, "after": after, "query": query},
            )
            currency_code = currency_code or data["shop"]["currencyCode"]
            page = data["productVariants"]
            for variant in page["nodes"]:
                variants_by_gid[variant["id"]] = variant
            if len(variants_by_gid) and len(variants_by_gid) % 1000 == 0:
                print(f"fetched {len(variants_by_gid)} variants", file=sys.stderr)
            if not page["pageInfo"]["hasNextPage"]:
                break
            after = page["pageInfo"]["endCursor"]
    return list(variants_by_gid.values()), currency_code


def build_plan_rows(
    variants: list[dict[str, Any]],
    *,
    cost_ratio: Decimal,
    only_missing: bool,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for variant in variants:
        product = variant["product"]
        inventory_item = variant.get("inventoryItem") or {}
        current_cost = current_unit_cost(variant)
        desired = desired_cost_from_price(variant.get("price"), cost_ratio)
        reason = ""
        action = "skip_already_synced"

        if desired is None:
            action = "cannot_calculate"
            reason = "missing_or_zero_price"
        elif not inventory_item.get("id"):
            action = "cannot_update"
            reason = "missing_inventory_item"
        elif only_missing and current_cost:
            action = "skip_existing_cost"
        elif not costs_match(current_cost, desired):
            action = "update_cost"
            reason = "missing_cost" if not current_cost else "cost_not_50pct_of_price"

        cost_rule_compliant = desired is not None and bool(current_cost) and costs_match(current_cost, desired)
        paid_eligible_after_cost_sync = desired is not None and inventory_item.get("id") is not None
        if action.startswith("cannot"):
            paid_eligible_after_cost_sync = False

        rows.append(
            {
                "product_id": str(product.get("legacyResourceId") or ""),
                "product_gid": product.get("id") or "",
                "product_status": product.get("status") or "",
                "handle": product.get("handle") or "",
                "product_title": product.get("title") or "",
                "variant_id": str(variant.get("legacyResourceId") or ""),
                "variant_gid": variant.get("id") or "",
                "variant_title": variant.get("title") or "",
                "sku": variant.get("sku") or "",
                "price": str(variant.get("price") or ""),
                "current_unit_cost": current_cost,
                "desired_unit_cost": money(desired) if desired is not None else "",
                "cost_rule": f"price_x_{cost_ratio}",
                "cost_rule_compliant": "TRUE" if cost_rule_compliant else "FALSE",
                "paid_eligible": "TRUE" if cost_rule_compliant else "FALSE",
                "paid_eligible_after_sync": "TRUE" if paid_eligible_after_cost_sync else "FALSE",
                "action": action,
                "reason": reason,
                "inventory_item_gid": inventory_item.get("id") or "",
            }
        )
    return rows


def group_updates_by_product(plan_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in plan_rows:
        if row["action"] == "update_cost":
            grouped[row["product_gid"]].append(row)
    return grouped


@dataclass
class SyncResult:
    applied_variant_ids: set[str]
    errors: list[dict[str, Any]]


def apply_updates(client: ShopifyClient, plan_rows: list[dict[str, str]]) -> SyncResult:
    applied_variant_ids: set[str] = set()
    errors: list[dict[str, Any]] = []
    grouped = group_updates_by_product(plan_rows)

    for index, (product_gid, product_rows) in enumerate(grouped.items(), start=1):
        variants_payload = [
            {
                "id": row["variant_gid"],
                "inventoryItem": {"cost": row["desired_unit_cost"]},
            }
            for row in product_rows
        ]
        data = client.graphql(
            PRODUCT_VARIANTS_BULK_UPDATE_MUTATION,
            {"productId": product_gid, "variants": variants_payload},
        )
        result = data["productVariantsBulkUpdate"]
        user_errors = result.get("userErrors") or []
        if user_errors:
            errors.append(
                {
                    "product_gid": product_gid,
                    "variant_ids": [row["variant_id"] for row in product_rows],
                    "user_errors": user_errors,
                }
            )
            continue
        for variant in result.get("productVariants") or []:
            applied_variant_ids.add(str(variant.get("legacyResourceId") or ""))
        if index % 25 == 0:
            print(f"updated {index}/{len(grouped)} products", file=sys.stderr)

    return SyncResult(applied_variant_ids=applied_variant_ids, errors=errors)


@dataclass
class CostSyncPaths:
    packet_dir: Path
    pre_plan_csv: Path
    post_plan_csv: Path
    before_json: Path
    after_json: Path
    summary_json: Path
    launchagent_template: Path


def result_paths(output_root: Path, stamp: str) -> CostSyncPaths:
    packet_dir = output_root / "02_AUDIT_PACKETS" / f"{stamp}_SHOPIFY_COST_SYNC_50PCT"
    return CostSyncPaths(
        packet_dir=packet_dir,
        pre_plan_csv=packet_dir / "cost_sync_pre_plan.csv",
        post_plan_csv=packet_dir / "cost_sync_post_readback.csv",
        before_json=packet_dir / "active_variants_before_cost_sync.json",
        after_json=packet_dir / "variants_after_cost_sync.json",
        summary_json=packet_dir / "summary.json",
        launchagent_template=Path("ops/shopify/com.dresslikemommy.shopify-cost-sync.plist"),
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def summarize_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "rows": len(rows),
        "action_counts": dict(sorted(Counter(row["action"] for row in rows).items())),
        "reason_counts": dict(sorted(Counter(row["reason"] for row in rows if row["reason"]).items())),
        "missing_unit_cost_rows": sum(1 for row in rows if not row["current_unit_cost"]),
        "paid_eligible_rows": sum(1 for row in rows if row["paid_eligible"] == "TRUE"),
    }


def run_cost_sync(
    *,
    output_root: Path,
    stamp: str,
    store_domain: str,
    access_token: str,
    statuses: list[str],
    cost_ratio: Decimal,
    only_missing: bool,
    execute: bool,
) -> CostSyncPaths:
    client = ShopifyClient(store_domain, access_token, API_VERSION)
    paths = result_paths(output_root, stamp)

    variants_before, currency_code = fetch_variants(client, statuses)
    pre_rows = build_plan_rows(
        variants_before,
        cost_ratio=cost_ratio,
        only_missing=only_missing,
    )
    fieldnames = list(pre_rows[0].keys()) if pre_rows else []
    write_csv(paths.pre_plan_csv, fieldnames, pre_rows)
    write_json(
        paths.before_json,
        {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "store_domain": store_domain,
            "api_version": API_VERSION,
            "statuses": statuses,
            "currency_code": currency_code,
            "cost_rule": f"unit_cost = variant.price * {cost_ratio}",
            "write_status": "PENDING_EXECUTION" if execute else "DRY_RUN_NO_SHOPIFY_WRITES",
            "variants": variants_before,
        },
    )

    sync_result = SyncResult(applied_variant_ids=set(), errors=[])
    if execute:
        sync_result = apply_updates(client, pre_rows)

    variants_after, _ = fetch_variants(client, statuses)
    post_rows = build_plan_rows(
        variants_after,
        cost_ratio=cost_ratio,
        only_missing=only_missing,
    )
    post_fieldnames = fieldnames or (list(post_rows[0].keys()) if post_rows else [])
    write_csv(paths.post_plan_csv, post_fieldnames, post_rows)
    write_json(
        paths.after_json,
        {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "store_domain": store_domain,
            "api_version": API_VERSION,
            "statuses": statuses,
            "currency_code": currency_code,
            "variants": variants_after,
        },
    )

    pre_summary = summarize_rows(pre_rows)
    post_summary = summarize_rows(post_rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "store_domain": store_domain,
        "api_version": API_VERSION,
        "statuses": statuses,
        "currency_code": currency_code,
        "cost_rule": f"unit_cost = variant.price * {cost_ratio}",
        "only_missing": only_missing,
        "execute": execute,
        "write_status": "SHOPIFY_WRITES_EXECUTED" if execute else "DRY_RUN_NO_SHOPIFY_WRITES",
        "pre_sync": pre_summary,
        "post_readback": post_summary,
        "applied_variant_rows": len(sync_result.applied_variant_ids),
        "error_count": len(sync_result.errors),
        "errors": sync_result.errors,
        "files": {
            "pre_plan_csv": str(paths.pre_plan_csv),
            "post_readback_csv": str(paths.post_plan_csv),
            "before_json": str(paths.before_json),
            "after_json": str(paths.after_json),
        },
    }
    write_json(paths.summary_json, summary)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Populate Shopify Cost per item as 50% of variant price."
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--stamp", default=now_stamp())
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument(
        "--statuses",
        default="ACTIVE",
        help="Comma-separated Shopify product statuses to scan. Default: ACTIVE.",
    )
    parser.add_argument("--cost-ratio", default=str(DEFAULT_COST_RATIO))
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only fill blank costs; leave existing cost values unchanged.",
    )
    parser.add_argument("--execute", action="store_true", help="Write cost updates to Shopify.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    statuses = normalize_statuses(args.statuses)
    store_domain = resolve_store_domain(
        args.store_domain,
        fallback_domain="dresslikemommy-com.myshopify.com",
    )
    access_token = load_access_token(args.access_token)
    paths = run_cost_sync(
        output_root=args.output_root,
        stamp=args.stamp,
        store_domain=store_domain,
        access_token=access_token,
        statuses=statuses,
        cost_ratio=Decimal(str(args.cost_ratio)),
        only_missing=args.only_missing,
        execute=args.execute,
    )
    print(f"packet_dir={paths.packet_dir}")
    print(f"summary={paths.summary_json}")


if __name__ == "__main__":
    main()
