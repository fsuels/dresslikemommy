#!/usr/bin/env python3
"""Remap plaid flannel variants to the exact single-color product media where available."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3ag-plaid-media-fix")
TARGET_HANDLE = "matching-mommy-me-plaid-flannel-shirts-cozy-button-up-jackets-for-fall"

PRODUCT_QUERY = """
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    media(first: 20) {
      nodes {
        __typename
        ... on MediaImage {
          id
          alt
          image {
            url
          }
        }
      }
    }
    variants(first: 80) {
      nodes {
        id
        legacyResourceId
        title
        selectedOptions {
          name
          value
        }
        media(first: 5) {
          nodes {
            __typename
            ... on MediaImage {
              id
              alt
              image {
                url
              }
            }
          }
        }
      }
    }
  }
}
"""

VARIANTS_BULK_UPDATE_MUTATION = """
mutation UpdateVariantMedia($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    product {
      id
    }
    productVariants {
      id
      title
      media(first: 5) {
        nodes {
          ... on MediaImage {
            id
            alt
          }
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


@dataclass
class PlannedVariantMediaFix:
    product_id: str
    product_gid: str
    variant_id: str
    variant_gid: str
    variant_title: str
    current_media_id: str
    current_media_alt: str
    target_media_id: str
    target_media_alt: str
    status: str


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
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc
            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def fetch_product(self, handle: str) -> dict[str, Any]:
        return self.graphql(PRODUCT_QUERY, {"handle": handle})["productByHandle"]

    def update_variant_media(self, product_gid: str, variants: list[dict[str, str]]) -> list[str]:
        data = self.graphql(VARIANTS_BULK_UPDATE_MUTATION, {"productId": product_gid, "variants": variants})[
            "productVariantsBulkUpdate"
        ]
        errors = []
        for item in data.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {item.get('message', '')}" if prefix else item.get("message", "Unknown error"))
        return errors


def clean(value: Any) -> str:
    return str(value or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Remap the brown plaid variants to the correct media image.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for artifacts.")
    parser.add_argument("--execute", action="store_true", help="Apply the media updates live.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    product = client.fetch_product(TARGET_HANDLE)
    if not product:
        raise RuntimeError(f"Product `{TARGET_HANDLE}` not found.")

    target_media_by_color: dict[str, dict[str, Any]] = {}
    media_nodes = product.get("media", {}).get("nodes") or []
    for node in media_nodes:
        if node.get("__typename") != "MediaImage":
            continue
        alt = clean(node.get("alt")).lower()
        if "red, brown, pink, and green" in alt:
            continue
        if "red plaid" in alt:
            target_media_by_color["red"] = node
        elif "brown plaid" in alt:
            target_media_by_color["brown"] = node
        elif "pink plaid" in alt:
            target_media_by_color["pink"] = node
        elif "green plaid" in alt:
            target_media_by_color["green"] = node
    missing = [color for color in ("red", "brown", "pink", "green") if color not in target_media_by_color]
    if missing:
        raise RuntimeError(f"Could not find media nodes for: {', '.join(missing)}.")

    planned: list[PlannedVariantMediaFix] = []
    variant_inputs: list[dict[str, str]] = []
    for variant in product.get("variants", {}).get("nodes") or []:
        title = clean(variant.get("title"))
        color_value = ""
        for option in variant.get("selectedOptions") or []:
            if clean(option.get("name")).lower() == "color":
                color_value = clean(option.get("value")).lower()
                break
        if color_value not in target_media_by_color:
            continue
        target_media = target_media_by_color[color_value]
        current_media_nodes = variant.get("media", {}).get("nodes") or []
        current_media = current_media_nodes[0] if current_media_nodes else {}
        current_media_id = clean(current_media.get("id"))
        status = "plan" if current_media_id != clean(target_media.get("id")) else "already_target"
        planned.append(
            PlannedVariantMediaFix(
                product_id=clean(product.get("legacyResourceId")),
                product_gid=clean(product.get("id")),
                variant_id=clean(variant.get("legacyResourceId")),
                variant_gid=clean(variant.get("id")),
                variant_title=title,
                current_media_id=current_media_id,
                current_media_alt=clean(current_media.get("alt")),
                target_media_id=clean(target_media.get("id")),
                target_media_alt=clean(target_media.get("alt")),
                status=status,
            )
        )
        if status == "plan":
            variant_inputs.append({"id": clean(variant.get("id")), "mediaId": clean(target_media.get("id"))})

    execution = {"execute": bool(args.execute), "planned_updates": len(variant_inputs), "applied_updates": 0, "errors": []}
    if args.execute and variant_inputs:
        errors = client.update_variant_media(clean(product.get("id")), variant_inputs)
        if errors:
            execution["errors"] = errors
        else:
            execution["applied_updates"] = len(variant_inputs)
        time.sleep(0.25)

    with (output_dir / "planned_variant_media_fixes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "product_id",
                "product_gid",
                "variant_id",
                "variant_gid",
                "variant_title",
                "current_media_id",
                "current_media_alt",
                "target_media_id",
                "target_media_alt",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(asdict(item) for item in planned)

    summary = {"planned_variants": len(planned), "execution": execution}
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
