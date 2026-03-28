#!/usr/bin/env python3
"""Audit and remediate Shopify catalog/publication mismatches for Google Shopping."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain


API_VERSION = "2026-01"
PAGE_SIZE = 50
MUTATION_DELAY_SECONDS = 0.05
DEFAULT_OUTPUT_DIR = Path(
    f"ops/catalog-cleanup/{datetime.now().strftime('%Y-%m-%d')}-phase-3-shopify-catalog-cleanup"
)

ONLINE_STORE_PUBLICATION_NAME = "Online Store"
GOOGLE_PUBLICATION_NAME = "Google & YouTube"
MARKET_CATALOG_TITLES = ("International", "Eurozone", "United States")
POLICY_SENSITIVE_TOKENS = ("maternity", "pregnancy", "pregnant", "photo shooting")

DISCOVER_PUBLICATIONS_QUERY = """
query DiscoverPublications {
  publications(first: 50) {
    nodes {
      id
      name
    }
  }
  catalogs(first: 20, type: MARKET) {
    nodes {
      __typename
      id
      title
      status
      ... on MarketCatalog {
        publication {
          id
          name
        }
      }
    }
  }
}
"""

PRODUCTS_QUERY = """
query Products(
  $first: Int!,
  $after: String,
  $onlinePublicationId: ID!,
  $googlePublicationId: ID!,
  $internationalPublicationId: ID!,
  $eurozonePublicationId: ID!,
  $unitedStatesPublicationId: ID!,
  $pointOfSalePublicationId: ID!,
  $pinterestPublicationId: ID!,
  $tiktokPublicationId: ID!
) {
  products(first: $first, after: $after, sortKey: ID) {
    edges {
      node {
        id
        legacyResourceId
        title
        handle
        status
        onlineStoreUrl
        totalVariants
        onlineStorePublished: publishedOnPublication(publicationId: $onlinePublicationId)
        googlePublished: publishedOnPublication(publicationId: $googlePublicationId)
        internationalCatalogPublished: publishedOnPublication(publicationId: $internationalPublicationId)
        eurozoneCatalogPublished: publishedOnPublication(publicationId: $eurozonePublicationId)
        unitedStatesCatalogPublished: publishedOnPublication(publicationId: $unitedStatesPublicationId)
        pointOfSalePublished: publishedOnPublication(publicationId: $pointOfSalePublicationId)
        pinterestPublished: publishedOnPublication(publicationId: $pinterestPublicationId)
        tiktokPublished: publishedOnPublication(publicationId: $tiktokPublicationId)
        variants(first: 100) {
          edges {
            node {
              legacyResourceId
              title
              price
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

PUBLISH_MUTATION = """
mutation PublishablePublish($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    publishable {
      ... on Product {
        id
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

UNPUBLISH_MUTATION = """
mutation PublishableUnpublish($id: ID!, $input: [PublicationInput!]!) {
  publishableUnpublish(id: $id, input: $input) {
    publishable {
      ... on Product {
        id
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class PublicationConfig:
    online_store: str
    google_youtube: str
    international: str
    eurozone: str
    united_states: str
    point_of_sale: str
    pinterest: str
    tiktok: str

    def as_dict(self) -> dict[str, str]:
        return {
            "online_store": self.online_store,
            "google_youtube": self.google_youtube,
            "international": self.international,
            "eurozone": self.eurozone,
            "united_states": self.united_states,
            "point_of_sale": self.point_of_sale,
            "pinterest": self.pinterest,
            "tiktok": self.tiktok,
        }


@dataclass
class ProductRecord:
    product_gid: str
    product_id: str
    title: str
    handle: str
    status: str
    online_store_url: str
    total_variants: int
    online_store_published: bool
    google_published: bool
    international_catalog_published: bool
    eurozone_catalog_published: bool
    united_states_catalog_published: bool
    point_of_sale_published: bool
    pinterest_published: bool
    tiktok_published: bool
    variant_prices: list[float]

    @property
    def market_catalog_count(self) -> int:
        return sum(
            (
                self.international_catalog_published,
                self.eurozone_catalog_published,
                self.united_states_catalog_published,
            )
        )

    @property
    def in_all_target_market_catalogs(self) -> bool:
        return self.market_catalog_count == 3

    @property
    def all_prices_positive(self) -> bool:
        return bool(self.variant_prices) and all(price > 0 for price in self.variant_prices)

    @property
    def title_has_dlm_suffix(self) -> bool:
        return " | DLM" in self.title

    @property
    def policy_sensitive_hint(self) -> bool:
        lowered = self.title.lower()
        return any(token in lowered for token in POLICY_SENSITIVE_TOKENS)

    def active_non_google_channel_names(self) -> list[str]:
        channel_names: list[str] = []
        if self.online_store_published:
            channel_names.append("Online Store")
        if self.point_of_sale_published:
            channel_names.append("Point of Sale")
        if self.pinterest_published:
            channel_names.append("Pinterest")
        if self.tiktok_published:
            channel_names.append("TikTok")
        return channel_names


@dataclass
class ActionRecord:
    product: ProductRecord
    action: str
    reason: str
    publication_ids_to_add: list[str]
    publication_ids_to_remove: list[str]
    publication_names_to_add: list[str]
    publication_names_to_remove: list[str]

    def to_row(self) -> dict[str, str]:
        product = self.product
        return {
            "product_id": product.product_id,
            "product_gid": product.product_gid,
            "handle": product.handle,
            "title": product.title,
            "status": product.status,
            "online_store_url": product.online_store_url,
            "online_store_published": bool_to_str(product.online_store_published),
            "google_published": bool_to_str(product.google_published),
            "international_catalog_published": bool_to_str(product.international_catalog_published),
            "eurozone_catalog_published": bool_to_str(product.eurozone_catalog_published),
            "united_states_catalog_published": bool_to_str(product.united_states_catalog_published),
            "point_of_sale_published": bool_to_str(product.point_of_sale_published),
            "pinterest_published": bool_to_str(product.pinterest_published),
            "tiktok_published": bool_to_str(product.tiktok_published),
            "total_variants": str(product.total_variants),
            "all_prices_positive": bool_to_str(product.all_prices_positive),
            "title_has_dlm_suffix": bool_to_str(product.title_has_dlm_suffix),
            "policy_sensitive_hint": bool_to_str(product.policy_sensitive_hint),
            "active_non_google_channels": ", ".join(product.active_non_google_channel_names()),
            "action": self.action,
            "reason": self.reason,
            "publication_ids_to_add": ", ".join(self.publication_ids_to_add),
            "publication_ids_to_remove": ", ".join(self.publication_ids_to_remove),
            "publication_names_to_add": ", ".join(self.publication_names_to_add),
            "publication_names_to_remove": ", ".join(self.publication_names_to_remove),
        }


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.store_domain = store_domain
        self.access_token = access_token
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(6):
            req = request.Request(self.endpoint, data=payload, headers=headers)
            try:
                with request.urlopen(req, timeout=120) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc

            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def bool_to_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def discover_publications(client: ShopifyClient) -> PublicationConfig:
    data = client.graphql(DISCOVER_PUBLICATIONS_QUERY)
    named_publications = {
        (node.get("name") or "").strip(): node["id"]
        for node in data["publications"]["nodes"]
        if node.get("name")
    }
    market_publications: dict[str, str] = {}
    for node in data["catalogs"]["nodes"]:
        if node.get("__typename") != "MarketCatalog":
            continue
        title = (node.get("title") or "").strip()
        publication = node.get("publication") or {}
        publication_id = publication.get("id") or ""
        if title and publication_id:
            market_publications[title] = publication_id

    missing = [
        name
        for name in (ONLINE_STORE_PUBLICATION_NAME, GOOGLE_PUBLICATION_NAME)
        if name not in named_publications
    ]
    missing.extend(title for title in MARKET_CATALOG_TITLES if title not in market_publications)
    if missing:
        raise RuntimeError(f"Missing required Shopify publications/catalogs: {', '.join(missing)}")

    return PublicationConfig(
        online_store=named_publications[ONLINE_STORE_PUBLICATION_NAME],
        google_youtube=named_publications[GOOGLE_PUBLICATION_NAME],
        international=market_publications["International"],
        eurozone=market_publications["Eurozone"],
        united_states=market_publications["United States"],
        point_of_sale=named_publications.get("Point of Sale", named_publications[ONLINE_STORE_PUBLICATION_NAME]),
        pinterest=named_publications.get("Pinterest", named_publications[ONLINE_STORE_PUBLICATION_NAME]),
        tiktok=named_publications.get("TikTok", named_publications[ONLINE_STORE_PUBLICATION_NAME]),
    )


def parse_price(raw_value: Any) -> float | None:
    if raw_value in (None, ""):
        return None
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


def build_product_record(node: dict[str, Any]) -> ProductRecord:
    prices = [
        parsed_price
        for edge in node["variants"]["edges"]
        if (parsed_price := parse_price(edge["node"].get("price"))) is not None
    ]
    return ProductRecord(
        product_gid=str(node["id"]),
        product_id=str(node["legacyResourceId"]),
        title=(node.get("title") or "").strip(),
        handle=(node.get("handle") or "").strip(),
        status=(node.get("status") or "").strip(),
        online_store_url=(node.get("onlineStoreUrl") or "").strip(),
        total_variants=int(node.get("totalVariants") or 0),
        online_store_published=bool(node.get("onlineStorePublished")),
        google_published=bool(node.get("googlePublished")),
        international_catalog_published=bool(node.get("internationalCatalogPublished")),
        eurozone_catalog_published=bool(node.get("eurozoneCatalogPublished")),
        united_states_catalog_published=bool(node.get("unitedStatesCatalogPublished")),
        point_of_sale_published=bool(node.get("pointOfSalePublished")),
        pinterest_published=bool(node.get("pinterestPublished")),
        tiktok_published=bool(node.get("tiktokPublished")),
        variant_prices=prices,
    )


def fetch_products(client: ShopifyClient, publications: PublicationConfig) -> list[ProductRecord]:
    variables = {
        "first": PAGE_SIZE,
        "after": None,
        "onlinePublicationId": publications.online_store,
        "googlePublicationId": publications.google_youtube,
        "internationalPublicationId": publications.international,
        "eurozonePublicationId": publications.eurozone,
        "unitedStatesPublicationId": publications.united_states,
        "pointOfSalePublicationId": publications.point_of_sale,
        "pinterestPublicationId": publications.pinterest,
        "tiktokPublicationId": publications.tiktok,
    }
    products: list[ProductRecord] = []
    while True:
        data = client.graphql(PRODUCTS_QUERY, variables)["products"]
        products.extend(build_product_record(edge["node"]) for edge in data["edges"])
        if not data["pageInfo"]["hasNextPage"]:
            break
        variables["after"] = data["pageInfo"]["endCursor"]
        time.sleep(MUTATION_DELAY_SECONDS)
    return products


def classify_products(products: list[ProductRecord], publications: PublicationConfig) -> tuple[list[ActionRecord], list[ActionRecord]]:
    actions: list[ActionRecord] = []
    manual_review: list[ActionRecord] = []
    market_publication_ids = [publications.international, publications.eurozone, publications.united_states]
    market_publication_names = ["International", "Eurozone", "United States"]

    for product in sorted(products, key=lambda item: int(item.product_id)):
        if product.status == "ARCHIVED":
            publication_ids_to_remove: list[str] = []
            publication_names_to_remove: list[str] = []
            if product.google_published:
                publication_ids_to_remove.append(publications.google_youtube)
                publication_names_to_remove.append(GOOGLE_PUBLICATION_NAME)
            if product.international_catalog_published:
                publication_ids_to_remove.append(publications.international)
                publication_names_to_remove.append("International")
            if product.eurozone_catalog_published:
                publication_ids_to_remove.append(publications.eurozone)
                publication_names_to_remove.append("Eurozone")
            if product.united_states_catalog_published:
                publication_ids_to_remove.append(publications.united_states)
                publication_names_to_remove.append("United States")
            if publication_ids_to_remove:
                actions.append(
                    ActionRecord(
                        product=product,
                        action="unpublish_google_and_market_catalogs",
                        reason="Archived product is still published to Google and/or target market catalogs.",
                        publication_ids_to_add=[],
                        publication_ids_to_remove=publication_ids_to_remove,
                        publication_names_to_add=[],
                        publication_names_to_remove=publication_names_to_remove,
                    )
                )
            continue

        if product.status != "ACTIVE":
            continue

        if product.market_catalog_count == 0:
            continue

        if not product.online_store_published:
            publication_ids_to_remove = []
            publication_names_to_remove = []
            if product.google_published:
                publication_ids_to_remove.append(publications.google_youtube)
                publication_names_to_remove.append(GOOGLE_PUBLICATION_NAME)
            for is_published, publication_id, publication_name in zip(
                (
                    product.international_catalog_published,
                    product.eurozone_catalog_published,
                    product.united_states_catalog_published,
                ),
                market_publication_ids,
                market_publication_names,
            ):
                if is_published:
                    publication_ids_to_remove.append(publication_id)
                    publication_names_to_remove.append(publication_name)
            actions.append(
                ActionRecord(
                    product=product,
                    action="remove_market_catalogs",
                    reason="Active product is not published to the Online Store, so market catalog membership creates crawlable dead or redirected product URLs.",
                    publication_ids_to_add=[],
                    publication_ids_to_remove=publication_ids_to_remove,
                    publication_names_to_add=[],
                    publication_names_to_remove=publication_names_to_remove,
                )
            )
            continue

        if product.google_published:
            continue

        if product.in_all_target_market_catalogs and product.online_store_url and product.all_prices_positive:
            actions.append(
                ActionRecord(
                    product=product,
                    action="publish_google_youtube",
                    reason="Active product is live on the Online Store, in all target market catalogs, and has positive variant prices.",
                    publication_ids_to_add=[publications.google_youtube],
                    publication_ids_to_remove=[],
                    publication_names_to_add=[GOOGLE_PUBLICATION_NAME],
                    publication_names_to_remove=[],
                )
            )
            continue

        manual_review.append(
            ActionRecord(
                product=product,
                action="manual_review",
                reason="Active product has an unexpected publication state and should be reviewed before mutation.",
                publication_ids_to_add=[],
                publication_ids_to_remove=[],
                publication_names_to_add=[],
                publication_names_to_remove=[],
            )
        )

    return actions, manual_review


def build_audit_rows(products: list[ProductRecord]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for product in sorted(products, key=lambda item: int(item.product_id)):
        rows.append(
            {
                "product_id": product.product_id,
                "product_gid": product.product_gid,
                "handle": product.handle,
                "title": product.title,
                "status": product.status,
                "online_store_url": product.online_store_url,
                "online_store_published": bool_to_str(product.online_store_published),
                "google_published": bool_to_str(product.google_published),
                "international_catalog_published": bool_to_str(product.international_catalog_published),
                "eurozone_catalog_published": bool_to_str(product.eurozone_catalog_published),
                "united_states_catalog_published": bool_to_str(product.united_states_catalog_published),
                "point_of_sale_published": bool_to_str(product.point_of_sale_published),
                "pinterest_published": bool_to_str(product.pinterest_published),
                "tiktok_published": bool_to_str(product.tiktok_published),
                "market_catalog_count": str(product.market_catalog_count),
                "total_variants": str(product.total_variants),
                "all_prices_positive": bool_to_str(product.all_prices_positive),
                "title_has_dlm_suffix": bool_to_str(product.title_has_dlm_suffix),
                "policy_sensitive_hint": bool_to_str(product.policy_sensitive_hint),
                "active_non_google_channels": ", ".join(product.active_non_google_channel_names()),
            }
        )
    return rows


def limit_actions(actions: list[ActionRecord], limit: int) -> list[ActionRecord]:
    if limit <= 0:
        return actions
    return actions[:limit]


def filter_actions(actions: list[ActionRecord], allowed_actions: set[str]) -> list[ActionRecord]:
    if not allowed_actions:
        return actions
    return [action for action in actions if action.action in allowed_actions]


def run_actions(
    client: ShopifyClient,
    actions: list[ActionRecord],
    *,
    execute_publish_google: bool,
    execute_remove_catalogs: bool,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for action in actions:
        should_execute = (
            (action.action == "publish_google_youtube" and execute_publish_google)
            or (action.action in {"remove_market_catalogs", "unpublish_google_and_market_catalogs"} and execute_remove_catalogs)
        )
        result: dict[str, Any] = {
            "product_id": action.product.product_id,
            "product_gid": action.product.product_gid,
            "handle": action.product.handle,
            "title": action.product.title,
            "action": action.action,
            "executed": should_execute,
            "success": False,
            "user_errors": [],
        }
        if not should_execute:
            results.append(result)
            continue

        variables = {
            "id": action.product.product_gid,
            "input": [
                {"publicationId": publication_id}
                for publication_id in (
                    action.publication_ids_to_add if action.action == "publish_google_youtube" else action.publication_ids_to_remove
                )
            ],
        }
        payload_key = "publishablePublish" if action.action == "publish_google_youtube" else "publishableUnpublish"
        mutation = PUBLISH_MUTATION if action.action == "publish_google_youtube" else UNPUBLISH_MUTATION
        data = client.graphql(mutation, variables)[payload_key]
        user_errors = data.get("userErrors") or []
        result["user_errors"] = user_errors
        result["success"] = not user_errors
        results.append(result)
        time.sleep(MUTATION_DELAY_SECONDS)
    return results


def summarize_actions(products: list[ProductRecord], actions: list[ActionRecord], manual_review: list[ActionRecord]) -> dict[str, Any]:
    action_counts: dict[str, int] = {}
    for action in actions:
        action_counts[action.action] = action_counts.get(action.action, 0) + 1

    return {
        "total_products": len(products),
        "status_counts": {
            "active": sum(1 for product in products if product.status == "ACTIVE"),
            "archived": sum(1 for product in products if product.status == "ARCHIVED"),
        },
        "active_products_in_all_three_market_catalogs_missing_google": sum(
            1
            for product in products
            if product.status == "ACTIVE" and product.in_all_target_market_catalogs and not product.google_published
        ),
        "active_catalog_only_products_not_on_online_store": sum(
            1
            for product in products
            if product.status == "ACTIVE" and product.market_catalog_count > 0 and not product.online_store_published
        ),
        "actions": action_counts,
        "manual_review_count": len(manual_review),
    }


def verify_counts(
    client: ShopifyClient,
    publications: PublicationConfig,
) -> dict[str, Any]:
    products = fetch_products(client, publications)
    actions, manual_review = classify_products(products, publications)
    return {
        "summary": summarize_actions(products, actions, manual_review),
        "remaining_actions": [action.to_row() for action in actions],
        "remaining_manual_review": [action.to_row() for action in manual_review],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Directory for audit, action, verification, and rollback artifacts. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap on the number of actions to include and execute, useful for smoke tests.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute both publish and unpublish actions after writing the dry-run artifacts.",
    )
    parser.add_argument(
        "--execute-publish-google",
        action="store_true",
        help="Execute only the publish-to-Google action bucket.",
    )
    parser.add_argument(
        "--execute-remove-market-catalogs",
        action="store_true",
        help="Execute only the market-catalog removal action bucket.",
    )
    parser.add_argument(
        "--action-filter",
        default="",
        help="Comma-separated action names to keep, for example: remove_market_catalogs,publish_google_youtube",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    store_domain = resolve_store_domain()
    access_token = load_access_token()
    client = ShopifyClient(store_domain, access_token)
    publications = discover_publications(client)
    products = fetch_products(client, publications)
    actions, manual_review = classify_products(products, publications)

    allowed_actions = {
        item.strip()
        for item in args.action_filter.split(",")
        if item.strip()
    }
    if allowed_actions:
        actions = filter_actions(actions, allowed_actions)
        manual_review = filter_actions(manual_review, allowed_actions)

    if args.limit:
        actions = limit_actions(actions, args.limit)
        manual_review = limit_actions(manual_review, args.limit)

    audit_rows = build_audit_rows(products)
    action_rows = [action.to_row() for action in actions]
    manual_review_rows = [action.to_row() for action in manual_review]
    rollback_rows = []
    for action in actions:
        rollback_rows.append(
            {
                "product_id": action.product.product_id,
                "product_gid": action.product.product_gid,
                "handle": action.product.handle,
                "title": action.product.title,
                "forward_action": action.action,
                "rollback_action": (
                    "unpublish_google_youtube"
                    if action.action == "publish_google_youtube"
                    else "restore_google_and_market_catalogs"
                    if action.action == "unpublish_google_and_market_catalogs"
                    else "restore_market_catalogs"
                ),
                "rollback_publication_ids": (
                    publications.google_youtube
                    if action.action == "publish_google_youtube"
                    else ", ".join(action.publication_ids_to_remove)
                ),
                "rollback_publication_names": (
                    GOOGLE_PUBLICATION_NAME
                    if action.action == "publish_google_youtube"
                    else ", ".join(action.publication_names_to_remove)
                ),
            }
        )

    audit_fieldnames = list(audit_rows[0].keys()) if audit_rows else []
    action_fieldnames = (
        list(action_rows[0].keys())
        if action_rows
        else list(manual_review_rows[0].keys())
        if manual_review_rows
        else [
            "product_id",
            "product_gid",
            "handle",
            "title",
            "status",
            "online_store_url",
            "online_store_published",
            "google_published",
            "international_catalog_published",
            "eurozone_catalog_published",
            "united_states_catalog_published",
            "point_of_sale_published",
            "pinterest_published",
            "tiktok_published",
            "total_variants",
            "all_prices_positive",
            "title_has_dlm_suffix",
            "policy_sensitive_hint",
            "active_non_google_channels",
            "action",
            "reason",
            "publication_ids_to_add",
            "publication_ids_to_remove",
            "publication_names_to_add",
            "publication_names_to_remove",
        ]
    )
    rollback_fieldnames = (
        list(rollback_rows[0].keys())
        if rollback_rows
        else [
            "product_id",
            "product_gid",
            "handle",
            "title",
            "forward_action",
            "rollback_action",
            "rollback_publication_ids",
            "rollback_publication_names",
        ]
    )

    write_csv(output_dir / "catalog_publication_audit.csv", audit_rows, audit_fieldnames)
    write_csv(output_dir / "catalog_cleanup_actions.csv", action_rows, action_fieldnames)
    write_csv(output_dir / "catalog_cleanup_manual_review.csv", manual_review_rows, action_fieldnames)
    write_csv(output_dir / "catalog_cleanup_rollback.csv", rollback_rows, rollback_fieldnames)

    summary = {
        "generated_at": datetime.now().isoformat(),
        "store_domain": store_domain,
        "publication_ids": publications.as_dict(),
        "summary": summarize_actions(products, actions, manual_review),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    execute_publish_google = args.execute or args.execute_publish_google
    execute_remove_catalogs = args.execute or args.execute_remove_market_catalogs
    execution_results = run_actions(
        client,
        actions,
        execute_publish_google=execute_publish_google,
        execute_remove_catalogs=execute_remove_catalogs,
    )
    (output_dir / "execution_results.json").write_text(json.dumps(execution_results, indent=2), encoding="utf-8")

    executed_any = execute_publish_google or execute_remove_catalogs
    if executed_any:
        verification = verify_counts(client, publications)
        (output_dir / "post_execution_verification.json").write_text(
            json.dumps(verification, indent=2),
            encoding="utf-8",
        )

    print(json.dumps(summary, indent=2))
    if executed_any:
        successful = sum(1 for result in execution_results if result["executed"] and result["success"])
        failed = sum(1 for result in execution_results if result["executed"] and not result["success"])
        print(
            json.dumps(
                {
                    "executed_publish_google": execute_publish_google,
                    "executed_remove_market_catalogs": execute_remove_catalogs,
                    "mutation_successes": successful,
                    "mutation_failures": failed,
                    "output_dir": str(output_dir),
                },
                indent=2,
            )
        )
    else:
        print(json.dumps({"dry_run": True, "output_dir": str(output_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
