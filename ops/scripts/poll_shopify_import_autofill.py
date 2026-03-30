#!/usr/bin/env python3
"""Poll Shopify for newly created products and autofill missing metafields automatically.

This worker is designed for local background automation on macOS via launchd.
It intentionally initializes from "now" on first run unless told otherwise, so it
only automates future imports by default.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.autofill_shopify_import_product import ShopifyClient, clean, run_autofill  # noqa: E402
from ops.scripts.shopify_admin_config import (  # noqa: E402
    DEFAULT_CONFIG_DIR,
    load_access_token,
    resolve_store_domain,
)


RECENT_PRODUCTS_QUERY = """
query RecentProducts($first: Int!, $after: String, $reverse: Boolean!) {
  products(first: $first, after: $after, sortKey: CREATED_AT, reverse: $reverse) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      cursor
      node {
        id
        legacyResourceId
        handle
        title
        vendor
        status
        createdAt
        tags
      }
    }
  }
}
"""

DEFAULT_STATE_PATH = DEFAULT_CONFIG_DIR / "shopify-import-autofill-state.json"
DEFAULT_LOG_PATH = Path.home() / "Library" / "Logs" / "dresslikemommy" / "shopify-import-autofill.jsonl"


@dataclass
class RecentProduct:
    product_gid: str
    product_id: str
    handle: str
    title: str
    vendor: str
    status: str
    created_at: str
    tags: list[str]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(clean(value).replace("Z", "+00:00"))


def isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "created_at_cursor": "",
            "processed_ids_at_cursor": [],
            "initialized_at": "",
            "last_run_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_log(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def should_include_product(
    product: RecentProduct,
    *,
    vendor_contains: str,
    required_tag: str,
) -> tuple[bool, str]:
    if clean(product.status).upper() == "ARCHIVED":
        return False, "archived"
    if vendor_contains and vendor_contains.lower() not in clean(product.vendor).lower():
        return False, "vendor_filter_miss"
    if required_tag:
        tags = {clean(tag).lower() for tag in product.tags}
        if required_tag.lower() not in tags:
            return False, "required_tag_missing"
    if "skip-autofill" in {clean(tag).lower() for tag in product.tags}:
        return False, "skip_tag_present"
    return True, "eligible"


def fetch_recent_products(client: ShopifyClient, max_pages: int, page_size: int) -> list[RecentProduct]:
    rows: list[RecentProduct] = []
    after: str | None = None
    for _ in range(max_pages):
        data = client.graphql(
            RECENT_PRODUCTS_QUERY,
            {"first": page_size, "after": after, "reverse": True},
        )["products"]
        for edge in data.get("edges") or []:
            node = edge.get("node") or {}
            rows.append(
                RecentProduct(
                    product_gid=clean(node.get("id")),
                    product_id=clean(node.get("legacyResourceId")),
                    handle=clean(node.get("handle")),
                    title=clean(node.get("title")),
                    vendor=clean(node.get("vendor")),
                    status=clean(node.get("status")),
                    created_at=clean(node.get("createdAt")),
                    tags=[clean(tag) for tag in node.get("tags") or [] if clean(tag)],
                )
            )
        if not data.get("pageInfo", {}).get("hasNextPage"):
            break
        after = clean(data.get("pageInfo", {}).get("endCursor"))
    return rows


def is_newer_than_cursor(product: RecentProduct, state: dict[str, Any]) -> bool:
    cursor = clean(state.get("created_at_cursor"))
    if not cursor:
        return True
    if product.created_at > cursor:
        return True
    if product.created_at == cursor and product.product_id not in set(state.get("processed_ids_at_cursor") or []):
        return True
    return False


def update_cursor_state(state: dict[str, Any], finalized: list[RecentProduct]) -> None:
    if not finalized:
        return

    current_cursor = clean(state.get("created_at_cursor"))
    current_ids = set(state.get("processed_ids_at_cursor") or [])
    newest_created_at = finalized[-1].created_at

    if newest_created_at > current_cursor:
        state["created_at_cursor"] = newest_created_at
        state["processed_ids_at_cursor"] = [item.product_id for item in finalized if item.created_at == newest_created_at]
        return

    if newest_created_at == current_cursor:
        for item in finalized:
            if item.created_at == current_cursor:
                current_ids.add(item.product_id)
        state["processed_ids_at_cursor"] = sorted(current_ids)


def initialize_state(
    path: Path,
    *,
    initialize_now: bool,
    bootstrap_hours: int,
) -> dict[str, Any]:
    state = load_state(path)
    if clean(state.get("initialized_at")):
        return state

    if initialize_now or bootstrap_hours <= 0:
        cursor_time = utc_now()
    else:
        cursor_time = utc_now() - timedelta(hours=max(bootstrap_hours, 0))

    state["created_at_cursor"] = isoformat_utc(cursor_time)
    state["processed_ids_at_cursor"] = []
    state["initialized_at"] = isoformat_utc(utc_now())
    state["last_run_at"] = ""
    save_state(path, state)
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="Persistent worker state path.")
    parser.add_argument("--jsonl-log", default=str(DEFAULT_LOG_PATH), help="Append-only JSONL log path.")
    parser.add_argument("--vendor-contains", default="", help="Optional case-insensitive vendor filter.")
    parser.add_argument("--required-tag", default="", help="Optional required tag filter.")
    parser.add_argument("--min-age-seconds", type=int, default=180, help="Only process products older than this.")
    parser.add_argument("--page-size", type=int, default=25, help="Recent products page size.")
    parser.add_argument("--max-pages", type=int, default=4, help="Maximum recent-products pages per run.")
    parser.add_argument("--max-products-per-run", type=int, default=10, help="Cap processed products per worker run.")
    parser.add_argument("--min-confidence", default="high", choices=["high", "medium"], help="Minimum apparel autofill confidence.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live product writes.")
    parser.add_argument("--execute", action="store_true", help="Apply changes live instead of dry-run.")
    parser.add_argument("--initialize-now", action="store_true", help="Initialize first-run cursor to now.")
    parser.add_argument("--bootstrap-hours", type=int, default=0, help="On first run only, process products this many hours back.")
    args = parser.parse_args()

    state_path = Path(args.state_path).expanduser()
    log_path = Path(args.jsonl_log).expanduser() if args.jsonl_log else None
    state = initialize_state(
        state_path,
        initialize_now=args.initialize_now,
        bootstrap_hours=args.bootstrap_hours,
    )

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)

    recent_products = fetch_recent_products(client, max_pages=max(args.max_pages, 1), page_size=max(args.page_size, 1))
    eligible_new: list[RecentProduct] = []
    for product in recent_products:
        if not is_newer_than_cursor(product, state):
            continue
        eligible_new.append(product)

    eligible_new.sort(key=lambda item: (item.created_at, item.product_id))

    finalized: list[RecentProduct] = []
    processed_count = 0
    blocked_by_error = False
    min_age_delta = timedelta(seconds=max(args.min_age_seconds, 0))

    for product in eligible_new:
        if processed_count >= max(args.max_products_per_run, 1):
            break

        created_at_dt = parse_iso8601(product.created_at)
        if utc_now() - created_at_dt < min_age_delta:
            append_log(
                log_path,
                {
                    "event": "deferred",
                    "reason": "product_too_new",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            continue

        included, reason = should_include_product(
            product,
            vendor_contains=args.vendor_contains,
            required_tag=args.required_tag,
        )
        if not included:
            finalized.append(product)
            processed_count += 1
            append_log(
                log_path,
                {
                    "event": "skipped",
                    "reason": reason,
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            continue

        try:
            summary = run_autofill(
                store_domain=store_domain,
                access_token=access_token,
                product_id=product.product_id,
                output_dir=None,
                min_confidence=args.min_confidence,
                execute=args.execute,
                pause_ms=args.pause_ms,
            )
            finalized.append(product)
            processed_count += 1
            append_log(
                log_path,
                {
                    "event": "processed",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "execute": bool(args.execute),
                    "summary": summary,
                },
            )
        except Exception as exc:  # noqa: BLE001
            blocked_by_error = True
            append_log(
                log_path,
                {
                    "event": "error",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "error": str(exc),
                },
            )
            break

    update_cursor_state(state, finalized)
    state["last_run_at"] = isoformat_utc(utc_now())
    save_state(state_path, state)

    print(
        json.dumps(
            {
                "state_path": str(state_path),
                "created_at_cursor": state.get("created_at_cursor"),
                "processed_ids_at_cursor": state.get("processed_ids_at_cursor", []),
                "new_products_seen": len(eligible_new),
                "finalized_this_run": len(finalized),
                "blocked_by_error": blocked_by_error,
                "execute": bool(args.execute),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
