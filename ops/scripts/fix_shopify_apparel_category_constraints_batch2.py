#!/usr/bin/env python3
"""Fix clearly miscategorized products that blocked deterministic apparel writes."""

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
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3aa-category-constraint-fix-batch-2")

CATEGORY_FIXES = [
    {
        "handle": "family-matching-hawaiian-shirt-and-floral-dress",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Family dress-and-shirt set is currently generic Clothing; peer family matching set products accept apparel fields under Outfit Sets.",
    },
    {
        "handle": "tropical-vibes-matching-family-hawaiian-shirt-and-floral-dress",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Family Hawaiian shirt + floral dress set is miscategorized under Baby & Toddler Clothing; set taxonomy should be Outfit Sets.",
    },
    {
        "handle": "family-matching-outfits-the-perfect-way-to-show-your-aloha-spirit",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Family matching set product with matching-set signals should use Outfit Sets instead of generic Clothing.",
    },
    {
        "handle": "boho-chic-family-matching-outfit-flowy-skirts-and-paisley-shirts",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Family set currently sits under Baby & Toddler Clothing; mixed family outfit set should use Outfit Sets.",
    },
    {
        "handle": "family-matching-dress-and-t-shirt-set-summer-fun-for-the-whole-family",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Dress-and-T-shirt family set should be categorized as Outfit Sets to accept structured apparel family attributes.",
    },
    {
        "handle": "family-matching-beach-dress-and-shirt-set-light-blue-floral-hawaiian-print",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Mixed beach dress + shirt family set is currently generic Clothing; Outfit Sets is the correct peer category.",
    },
    {
        "handle": "family-matching-outfits-floral-dresses-and-shorts-with-a-touch-of-fun",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Family dresses-and-shorts set belongs under Outfit Sets rather than Baby & Toddler Clothing.",
    },
    {
        "handle": "family-matching-outfits-ruffled-sleeve-dress-t-shirt",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Ruffled-sleeve dress and T-shirt family set is uncategorized; Outfit Sets is the consistent family-set taxonomy.",
    },
    {
        "handle": "tropical-family-matching-outfits",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Tropical family matching sets are currently under Baby & Toddler Clothing; family outfit set taxonomy should be Outfit Sets.",
    },
    {
        "handle": "vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-11",
        "target_category_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
        "reason": "Explicit family overalls-and-T-shirt set should be categorized as Outfit Sets, not generic Clothing.",
    },
    {
        "handle": "mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter",
        "target_category_id": "gid://shopify/TaxonomyCategory/aa-1-4",
        "target_category_full_name": "Apparel & Accessories > Clothing > Dresses",
        "reason": "Maxi dress product is uncategorized; peer mommy-and-me dresses with accepted apparel fields use Dresses.",
    },
]

PRODUCT_QUERY = """
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    productType
    category {
      id
      fullName
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
      category {
        id
        fullName
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
class PlannedCategoryFix:
    product_id: str
    product_gid: str
    handle: str
    title: str
    current_category_id: str
    current_category_full_name: str
    target_category_id: str
    target_category_full_name: str
    reason: str
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

    def update_category(self, product_gid: str, category_id: str) -> list[str]:
        data = self.graphql(PRODUCT_UPDATE_MUTATION, {"product": {"id": product_gid, "category": category_id}})[
            "productUpdate"
        ]
        errors = []
        for item in data.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {item.get('message', '')}" if prefix else item.get("message", "Unknown error"))
        return errors


def clean(value: Any) -> str:
    return str(value or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix a second batch of category-constrained apparel products.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for artifacts.")
    parser.add_argument("--execute", action="store_true", help="Apply the planned category fixes live.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live updates.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )

    planned: list[PlannedCategoryFix] = []
    for item in CATEGORY_FIXES:
        product = client.fetch_product(item["handle"])
        if not product:
            raise RuntimeError(f"Product `{item['handle']}` not found.")
        category = product.get("category") or {}
        current_id = clean(category.get("id"))
        current_full_name = clean(category.get("fullName"))
        status = "plan"
        if current_id == item["target_category_id"]:
            status = "already_target"
        planned.append(
            PlannedCategoryFix(
                product_id=clean(product.get("legacyResourceId")),
                product_gid=clean(product.get("id")),
                handle=clean(product.get("handle")),
                title=clean(product.get("title")),
                current_category_id=current_id,
                current_category_full_name=current_full_name,
                target_category_id=item["target_category_id"],
                target_category_full_name=item["target_category_full_name"],
                reason=item["reason"],
                status=status,
            )
        )

    execution = {
        "execute": bool(args.execute),
        "planned_category_updates": sum(1 for item in planned if item.status == "plan"),
        "applied_category_updates": 0,
        "errors": [],
    }

    if args.execute:
        for item in planned:
            if item.status != "plan":
                continue
            errors = client.update_category(item.product_gid, item.target_category_id)
            if errors:
                execution["errors"].append({"handle": item.handle, "errors": errors})
            else:
                execution["applied_category_updates"] += 1
            if args.pause_ms > 0:
                time.sleep(args.pause_ms / 1000.0)

    rows = [asdict(item) for item in planned]
    with (output_dir / "planned_category_fixes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "product_id",
                "product_gid",
                "handle",
                "title",
                "current_category_id",
                "current_category_full_name",
                "target_category_id",
                "target_category_full_name",
                "reason",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "planned_products": len(planned),
        "planned_category_updates": execution["planned_category_updates"],
        "execution": execution,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
