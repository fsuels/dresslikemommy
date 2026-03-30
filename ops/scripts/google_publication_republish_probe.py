#!/usr/bin/env python3
"""Run a single-product Google publication unpublish/republish probe."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402
from ops.scripts.shopify_catalog_cleanup import (  # noqa: E402
    PUBLISH_MUTATION,
    UNPUBLISH_MUTATION,
    ShopifyClient,
    discover_publications,
)


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3p-google-republish-probe")

PRODUCT_QUERY = """
query Product($handle: String!, $googlePublicationId: ID!, $onlinePublicationId: ID!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    status
    onlineStoreUrl
    totalInventory
    totalVariants
    googlePublished: publishedOnPublication(publicationId: $googlePublicationId)
    onlinePublished: publishedOnPublication(publicationId: $onlinePublicationId)
    category {
      id
      fullName
      name
    }
    variants(first: 100) {
      nodes {
        legacyResourceId
        title
        price
        availableForSale
      }
    }
  }
}
"""


@dataclass
class ProductState:
    product_gid: str
    product_id: str
    handle: str
    title: str
    status: str
    online_store_url: str
    total_inventory: int
    total_variants: int
    google_published: bool
    online_published: bool
    category_id: str
    category_name: str
    category_full_name: str
    variant_count: int
    all_prices_positive: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_gid": self.product_gid,
            "product_id": self.product_id,
            "handle": self.handle,
            "title": self.title,
            "status": self.status,
            "online_store_url": self.online_store_url,
            "total_inventory": self.total_inventory,
            "total_variants": self.total_variants,
            "google_published": self.google_published,
            "online_published": self.online_published,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_full_name": self.category_full_name,
            "variant_count": self.variant_count,
            "all_prices_positive": self.all_prices_positive,
        }


def clean(value: Any) -> str:
    return str(value or "").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handle", required=True, help="Product handle to use for the Google publication probe.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for dry-run and execution artifacts.")
    parser.add_argument("--execute", action="store_true", help="Run the unpublish/republish probe live.")
    parser.add_argument("--pause-seconds", type=float, default=2.0, help="Pause between unpublish and republish steps.")
    return parser.parse_args()


def fetch_product_state(client: ShopifyClient, *, handle: str, google_publication_id: str, online_publication_id: str) -> ProductState:
    data = client.graphql(
        PRODUCT_QUERY,
        {
            "handle": handle,
            "googlePublicationId": google_publication_id,
            "onlinePublicationId": online_publication_id,
        },
    )["productByHandle"]
    if not data:
        raise RuntimeError(f"Product `{handle}` not found.")
    category = data.get("category") or {}
    prices = [float(node["price"]) for node in (data.get("variants") or {}).get("nodes") or [] if node.get("price") not in (None, "")]
    return ProductState(
        product_gid=clean(data.get("id")),
        product_id=clean(data.get("legacyResourceId")),
        handle=clean(data.get("handle")),
        title=clean(data.get("title")),
        status=clean(data.get("status")),
        online_store_url=clean(data.get("onlineStoreUrl")),
        total_inventory=int(data.get("totalInventory") or 0),
        total_variants=int(data.get("totalVariants") or 0),
        google_published=bool(data.get("googlePublished")),
        online_published=bool(data.get("onlinePublished")),
        category_id=clean(category.get("id")),
        category_name=clean(category.get("name")),
        category_full_name=clean(category.get("fullName")),
        variant_count=len((data.get("variants") or {}).get("nodes") or []),
        all_prices_positive=bool(prices) and all(price > 0 for price in prices),
    )


def run_mutation(client: ShopifyClient, *, mutation: str, product_gid: str, publication_id: str, payload_key: str) -> list[dict[str, Any]]:
    data = client.graphql(
        mutation,
        {
            "id": product_gid,
            "input": [{"publicationId": publication_id}],
        },
    )[payload_key]
    return data.get("userErrors") or []


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    publications = discover_publications(client)
    before = fetch_product_state(
        client,
        handle=args.handle,
        google_publication_id=publications.google_youtube,
        online_publication_id=publications.online_store,
    )

    dry_run_checks = {
        "status_is_active": before.status == "ACTIVE",
        "currently_google_published": before.google_published,
        "currently_online_published": before.online_published,
        "has_online_store_url": bool(before.online_store_url),
        "all_prices_positive": before.all_prices_positive,
    }

    summary: dict[str, Any] = {
        "handle": args.handle,
        "output_dir": str(output_dir),
        "google_publication_id": publications.google_youtube,
        "online_store_publication_id": publications.online_store,
        "before": before.to_dict(),
        "dry_run_checks": dry_run_checks,
        "execution": {
            "execute": bool(args.execute),
            "unpublish_success": False,
            "publish_success": False,
            "unpublish_errors": [],
            "publish_errors": [],
            "after_unpublish": None,
            "after_republish": None,
        },
    }

    write_csv(
        output_dir / "probe_state.csv",
        [
            {"phase": "before", **before.to_dict()},
        ],
        [
            "phase",
            "product_gid",
            "product_id",
            "handle",
            "title",
            "status",
            "online_store_url",
            "total_inventory",
            "total_variants",
            "google_published",
            "online_published",
            "category_id",
            "category_name",
            "category_full_name",
            "variant_count",
            "all_prices_positive",
        ],
    )

    if args.execute:
        if not all(dry_run_checks.values()):
            raise RuntimeError(f"Probe preconditions failed for `{args.handle}`: {json.dumps(dry_run_checks, indent=2)}")

        unpublish_errors = run_mutation(
            client,
            mutation=UNPUBLISH_MUTATION,
            product_gid=before.product_gid,
            publication_id=publications.google_youtube,
            payload_key="publishableUnpublish",
        )
        summary["execution"]["unpublish_errors"] = unpublish_errors
        summary["execution"]["unpublish_success"] = not unpublish_errors
        after_unpublish = fetch_product_state(
            client,
            handle=args.handle,
            google_publication_id=publications.google_youtube,
            online_publication_id=publications.online_store,
        )
        summary["execution"]["after_unpublish"] = after_unpublish.to_dict()
        if args.pause_seconds > 0:
            time.sleep(args.pause_seconds)

        publish_errors = run_mutation(
            client,
            mutation=PUBLISH_MUTATION,
            product_gid=before.product_gid,
            publication_id=publications.google_youtube,
            payload_key="publishablePublish",
        )
        summary["execution"]["publish_errors"] = publish_errors
        summary["execution"]["publish_success"] = not publish_errors
        after_republish = fetch_product_state(
            client,
            handle=args.handle,
            google_publication_id=publications.google_youtube,
            online_publication_id=publications.online_store,
        )
        summary["execution"]["after_republish"] = after_republish.to_dict()

        write_csv(
            output_dir / "probe_state.csv",
            [
                {"phase": "before", **before.to_dict()},
                {"phase": "after_unpublish", **after_unpublish.to_dict()},
                {"phase": "after_republish", **after_republish.to_dict()},
            ],
            [
                "phase",
                "product_gid",
                "product_id",
                "handle",
                "title",
                "status",
                "online_store_url",
                "total_inventory",
                "total_variants",
                "google_published",
                "online_published",
                "category_id",
                "category_name",
                "category_full_name",
                "variant_count",
                "all_prices_positive",
            ],
        )

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
