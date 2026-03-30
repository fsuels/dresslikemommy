#!/usr/bin/env python3
"""Apply a targeted copy cleanup for the one live MC policy product."""

from __future__ import annotations

import argparse
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


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3af-live-policy-copy-fix")
TARGET_HANDLE = "mommy-and-me-matching-floral-long-sleeve-maxi-dresses-with-pockets"

PRODUCT_QUERY = """
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    descriptionHtml
    seo {
      title
      description
    }
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation UpdateProduct($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      descriptionHtml
      seo {
        title
        description
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""


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

    def update_product_copy(
        self, *, product_gid: str, description_html: str, seo_title: str, seo_description: str
    ) -> list[str]:
        data = self.graphql(
            PRODUCT_UPDATE_MUTATION,
            {
                "product": {
                    "id": product_gid,
                    "descriptionHtml": description_html,
                    "seo": {"title": seo_title, "description": seo_description},
                }
            },
        )["productUpdate"]
        errors = []
        for item in data.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {item.get('message', '')}" if prefix else item.get("message", "Unknown error"))
        return errors


def clean(value: Any) -> str:
    return str(value or "").strip()


def build_updated_description(current_html: str) -> str:
    updated = current_html
    replacements = {
        "Step into timeless elegance with these Mommy and Me matching floral maxi dresses. Designed with stunning floral patterns and featuring long sleeves, these dresses are perfect for any occasion, from family photoshoots to casual outings. The soft, flowy fabric ensures both comfort and style, while the convenient side pockets add a touch of practicality. Available in multiple vibrant colors, you and your little one will look effortlessly chic while twinning in style. The elastic waistband ensures a flattering fit, making these dresses the perfect choice for creating unforgettable memories together.": "Matching floral maxi dresses with long sleeves, side pockets, and an elastic waistband. The soft, flowy fabric is designed for a comfortable fit across the adult and child size range, with multiple color options available.",
        "Ideal for family photoshoots, special occasions, or casual outings": "Suitable for everyday wear and seasonal events",
        "Mom and daughter in matching peach floral maxi dresses, perfect for special occasions": "Adult and child wearing peach floral maxi dresses",
        "Matching black floral maxi dresses for mom and daughter, designed for a coordinated family look": "Adult and child wearing black floral maxi dresses",
        "Mommy and me green floral maxi dresses, ideal for family events and photoshoots": "Adult and child wearing green floral maxi dresses",
        "Mother and daughter wearing coordinated pink floral maxi dresses, styled for any occasion": "Adult and child wearing pink floral maxi dresses",
        "Mommy and me mint green floral maxi dresses, perfect for family events and twinning": "Adult and child wearing mint green floral maxi dresses",
        "Elegant matching floral maxi dresses for mom and daughter, styled for family outing": "Adult and child wearing black floral maxi dresses",
        "Mom and daughter in stylish matching white floral dresses, ideal for spring and summe": "Adult and child wearing white floral maxi dresses",
        "Coordinated navy blue floral maxi dresses for mother and daughter, perfect for casual and formal events": "Adult and child wearing navy floral maxi dresses",
    }
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a targeted policy-copy cleanup.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for artifacts.")
    parser.add_argument("--execute", action="store_true", help="Apply the copy update live.")
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

    current_description = clean(product.get("descriptionHtml"))
    current_seo = product.get("seo") or {}
    updated_description = build_updated_description(current_description)
    updated_seo_title = "Matching Floral Maxi Dresses with Pockets | Dress Like Mommy"
    updated_seo_description = "Matching floral maxi dresses with long sleeves, pockets, and multiple color options for adults and children."
    plan = {
        "product_id": clean(product.get("legacyResourceId")),
        "handle": clean(product.get("handle")),
        "title": clean(product.get("title")),
        "current_seo_title": clean(current_seo.get("title")),
        "current_seo_description": clean(current_seo.get("description")),
        "updated_seo_title": updated_seo_title,
        "updated_seo_description": updated_seo_description,
        "description_changed": updated_description != current_description,
    }
    (output_dir / "planned_policy_copy_fix.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")

    execution = {"execute": bool(args.execute), "applied": False, "errors": []}
    if args.execute:
        errors = client.update_product_copy(
            product_gid=clean(product.get("id")),
            description_html=updated_description,
            seo_title=updated_seo_title,
            seo_description=updated_seo_description,
        )
        if errors:
            execution["errors"] = errors
        else:
            execution["applied"] = True
        time.sleep(0.25)

    (output_dir / "summary.json").write_text(json.dumps({"plan": plan, "execution": execution}, indent=2), encoding="utf-8")
    print(json.dumps({"plan": plan, "execution": execution}, indent=2))


if __name__ == "__main__":
    main()
