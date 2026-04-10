#!/usr/bin/env python3
"""Rewrite priority PDP copy into structured merch content.

Default mode is dry-run and writes artifacts only.
Use --execute to apply the description + SEO updates live in Shopify.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_DIR = Path("ops/content/pdp-audit/2026-04-10-priority-pdp-copy-fix")

PRODUCT_QUERY = """
query ProductByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    productType
    tags
    descriptionHtml
    seo {
      title
      description
    }
    options {
      name
      values
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

SIZE_CHART_TABLE_RE = re.compile(r"(<table[^>]*id=[\"']size-chart[\"'][^>]*>.*?</table>)", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class TargetCopy:
    seo_title: str
    seo_description: str
    intro: str
    included: list[str]
    fabric: list[str]
    fit: list[str]
    occasion: list[str]
    care: list[str]
    shipping: list[str]
    returns: list[str]


TARGETS: dict[str, TargetCopy] = {
    "elegant-black-ruffle-dress-chic-sleeveless-layered-dress-for-mother-and-daughter-perfect-for-parties-and-events": TargetCopy(
        seo_title="Mommy and Me Black Ruffle Dresses | Dress Like Mommy",
        seo_description="Black mommy-and-me ruffle dresses with a sleeveless silhouette, lightweight feel, and a size chart for mother and child sizing.",
        intro="A coordinated black ruffle dress look for moms and daughters who want an easy special-occasion option with a dressed-up finish.",
        included=[
            "Black ruffle dress styling offered in mother and child sizes from the same product page.",
            "Product imagery and prior merch copy show the look styled with coordinating mini crossbody bags.",
        ],
        fabric=[
            "Soft, lightweight, breathable fabric called out in the supplier-backed product copy.",
        ],
        fit=[
            "Sleeveless silhouette with layered ruffle tiers for movement and shape.",
            "Use the size chart to compare child height guidance and mother bust/length measurements before ordering.",
        ],
        occasion=[
            "Works well for parties, family gatherings, casual outings, and photo-ready moments.",
        ],
        care=[
            "Follow the garment care label before washing.",
        ],
        shipping=[
            "Free shipping on all orders.",
        ],
        returns=[
            "30-day returns under the store return policy.",
        ],
    ),
    "family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children": TargetCopy(
        seo_title="Family Matching Floral Shirt and Dress Set | Dress Like Mommy",
        seo_description="Family matching floral shirts and dresses in father, mother, girl, and boy sizes with cotton fabric and a role-based size chart.",
        intro="A floral family matching look that lets you choose the role and size you need from one coordinated product page.",
        included=[
            "Coordinating floral dress options for mother and girl sizes.",
            "Coordinating floral shirt options for father and boy sizes.",
            "Select the role and size you need rather than expecting a full family bundle in one purchase.",
        ],
        fabric=[
            "Cotton material is explicitly listed in the current live product details.",
        ],
        fit=[
            "Ruffled dress styling for the mother/girl options and matching shirts for the father/boy options.",
            "The inline size chart covers role-specific bust, shoulder, length, and height guidance.",
        ],
        occasion=[
            "Built for summer family photos, beach days, special events, and giftable matching moments.",
        ],
        care=[
            "Follow the garment care label before washing.",
        ],
        shipping=[
            "Free shipping on all orders.",
        ],
        returns=[
            "30-day returns under the store return policy.",
        ],
    ),
    "stylish-and-comfortable-family-matching-outfits": TargetCopy(
        seo_title="Green Floral Family Matching Shirt and Dress Set | Dress Like Mommy",
        seo_description="Green floral family matching shirts and dresses in 100% cotton with role-based sizing for dad, mom, boy, and girl options.",
        intro="A green-and-white floral family matching set with separate shirt and dress options across parent and child roles.",
        included=[
            "Choose the coordinating piece you need by role and size from the same product page.",
            "Dad and boy options are merchandised as shirts, while mom and girl options are merchandised as dresses.",
        ],
        fabric=[
            "100% cotton is stated in the supplier-backed product copy.",
            "The backfill merch notes also describe the fabric as lightweight and breathable for warm-weather wear.",
        ],
        fit=[
            "Father shirt is described as a relaxed fit and the son shirt as a regular fit.",
            "Mother dress is described as a long flowy maxi silhouette and the daughter dress as a knee-length silhouette.",
        ],
        occasion=[
            "A strong fit for beach days, cruises, spring and summer outings, and family event photos.",
        ],
        care=[
            "Follow the garment care label before washing.",
        ],
        shipping=[
            "Free shipping on all orders.",
        ],
        returns=[
            "30-day returns under the store return policy.",
        ],
    ),
}


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

    def fetch_product(self, handle: str) -> dict[str, Any] | None:
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


def extract_size_chart(description_html: str) -> str:
    match = SIZE_CHART_TABLE_RE.search(description_html or "")
    return match.group(1).strip() if match else ""


def render_list(items: list[str]) -> str:
    rendered_items = "".join(f"<li>{html.escape(item)}</li>" for item in items if clean(item))
    return f"<ul>{rendered_items}</ul>" if rendered_items else ""


def render_section(title: str, items: list[str]) -> str:
    if not items:
        return ""
    return f"<section><h3>{html.escape(title)}</h3>{render_list(items)}</section>"


def build_description(product: dict[str, Any], target: TargetCopy) -> str:
    description_parts = [
        f"<p>{html.escape(target.intro)}</p>",
        render_section("What's included", target.included),
        render_section("Fabric", target.fabric),
        render_section("Fit", target.fit),
        render_section("Occasion", target.occasion),
        render_section("Care", target.care),
        render_section("Shipping", target.shipping),
        render_section("Returns", target.returns),
    ]

    size_chart_html = extract_size_chart(clean(product.get("descriptionHtml")))
    if size_chart_html:
        description_parts.append(
            "<section><h3>Size Chart</h3>"
            "<p>Use the chart below to compare role-specific measurements before ordering.</p>"
            f"{size_chart_html}</section>"
        )

    return "".join(part for part in description_parts if part)


def build_summary_record(product: dict[str, Any], target: TargetCopy, updated_description: str) -> dict[str, Any]:
    current_seo = product.get("seo") or {}
    return {
        "product_id": clean(product.get("legacyResourceId")),
        "handle": clean(product.get("handle")),
        "title": clean(product.get("title")),
        "product_type": clean(product.get("productType")),
        "options": product.get("options") or [],
        "tags": product.get("tags") or [],
        "current_seo_title": clean(current_seo.get("title")),
        "current_seo_description": clean(current_seo.get("description")),
        "updated_seo_title": target.seo_title,
        "updated_seo_description": target.seo_description,
        "description_changed": clean(product.get("descriptionHtml")) != clean(updated_description),
        "size_chart_preserved": bool(extract_size_chart(clean(product.get("descriptionHtml")))),
    }


def write_artifacts(
    output_dir: Path,
    product: dict[str, Any],
    updated_description: str,
    summary_record: dict[str, Any],
) -> None:
    handle = clean(product.get("handle"))
    (output_dir / f"{handle}-before.html").write_text(clean(product.get("descriptionHtml")), encoding="utf-8")
    (output_dir / f"{handle}-after.html").write_text(updated_description, encoding="utf-8")
    (output_dir / f"{handle}-plan.json").write_text(json.dumps(summary_record, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rewrite priority PDP copy into structured merch content.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for dry-run/execution artifacts.")
    parser.add_argument("--execute", action="store_true", help="Apply the copy updates live.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )

    summary: dict[str, Any] = {
        "mode": "execute" if args.execute else "dry-run",
        "targets": [],
        "execution": [],
    }

    for handle, target in TARGETS.items():
        product = client.fetch_product(handle)
        if not product:
            raise RuntimeError(f"Product `{handle}` not found.")

        updated_description = build_description(product, target)
        summary_record = build_summary_record(product, target, updated_description)
        write_artifacts(output_dir, product, updated_description, summary_record)
        summary["targets"].append(summary_record)

        execution_record = {"handle": handle, "applied": False, "errors": []}
        if args.execute:
            errors = client.update_product_copy(
                product_gid=clean(product.get("id")),
                description_html=updated_description,
                seo_title=target.seo_title,
                seo_description=target.seo_description,
            )
            if errors:
                execution_record["errors"] = errors
            else:
                execution_record["applied"] = True
            time.sleep(0.25)
        summary["execution"].append(execution_record)

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
