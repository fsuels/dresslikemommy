#!/usr/bin/env python3
"""Apply deterministic color-pattern fixes for the current live MC residue."""

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
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3ae-live-color-residue-fix")

TARGETS = [
    {
        "handle": "family-matching-swimwear-bathing-suit",
        "labels": ["Floral", "Multicolor"],
        "reason": "All product imagery and alt text show floral-print family swimwear, and the live tags include Multi Color plus Floral.",
    },
    {
        "handle": "make-a-splash-with-this-family-matching-floral-outfit",
        "labels": ["Yellow", "Floral"],
        "reason": "The product is a yellow floral family set by tags, imagery, and SEO copy.",
    },
    {
        "handle": "mother-daughter-trendy-knitted-sweater-style-for-fall",
        "labels": ["Rainbow", "Striped"],
        "reason": "All imagery and SEO signals describe a rainbow striped sweater/cardigan set.",
    },
]

PRODUCT_QUERY = """
query Product($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    color: metafield(namespace: "shopify", key: "color-pattern") {
      value
      references(first: 20) {
        nodes {
          ... on Metaobject {
            id
            handle
            displayName
          }
        }
      }
    }
  }
}
"""

METAOBJECTS_QUERY = """
query Metaobjects($type: String!, $first: Int!, $after: String) {
  metaobjects(type: $type, first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      handle
      displayName
    }
  }
}
"""

METAFIELDS_SET_MUTATION = """
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""


@dataclass
class MetaobjectRef:
    id: str
    handle: str
    display_name: str


@dataclass
class PlannedColorFix:
    product_id: str
    product_gid: str
    handle: str
    title: str
    current_labels: str
    target_labels: str
    target_reference_ids: str
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

    def fetch_color_metaobjects(self) -> list[MetaobjectRef]:
        refs: list[MetaobjectRef] = []
        after: str | None = None
        while True:
            data = self.graphql(METAOBJECTS_QUERY, {"type": "shopify--color-pattern", "first": 100, "after": after})[
                "metaobjects"
            ]
            refs.extend(
                MetaobjectRef(id=node["id"], handle=node["handle"], display_name=node["displayName"])
                for node in data["nodes"]
            )
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return refs

    def set_color_refs(self, product_gid: str, reference_ids: list[str]) -> list[str]:
        data = self.graphql(
            METAFIELDS_SET_MUTATION,
            {
                "metafields": [
                    {
                        "ownerId": product_gid,
                        "namespace": "shopify",
                        "key": "color-pattern",
                        "type": "list.metaobject_reference",
                        "value": json.dumps(reference_ids),
                    }
                ]
            },
        )["metafieldsSet"]
        errors = []
        for item in data.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {item.get('message', '')}" if prefix else item.get("message", "Unknown error"))
        return errors


def clean(value: Any) -> str:
    return str(value or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix deterministic color-pattern residue for live MC issues.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for artifacts.")
    parser.add_argument("--execute", action="store_true", help="Apply the planned fixes live.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live updates.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    color_refs = client.fetch_color_metaobjects()
    by_label = {ref.display_name.lower(): ref for ref in color_refs}

    planned: list[PlannedColorFix] = []
    for target in TARGETS:
        product = client.fetch_product(target["handle"])
        if not product:
            raise RuntimeError(f"Product `{target['handle']}` not found.")
        current_nodes = (((product.get("color") or {}).get("references") or {}).get("nodes")) or []
        current_labels = [clean(node.get("displayName")) for node in current_nodes if clean(node.get("displayName"))]
        target_refs: list[MetaobjectRef] = []
        for label in target["labels"]:
            ref = by_label.get(label.lower())
            if not ref:
                raise RuntimeError(f"Missing color metaobject for `{label}`.")
            target_refs.append(ref)
        status = "plan" if not current_labels else "skip_already_present"
        planned.append(
            PlannedColorFix(
                product_id=clean(product.get("legacyResourceId")),
                product_gid=clean(product.get("id")),
                handle=clean(product.get("handle")),
                title=clean(product.get("title")),
                current_labels="|".join(current_labels),
                target_labels="|".join(target["labels"]),
                target_reference_ids="|".join(ref.id for ref in target_refs),
                reason=target["reason"],
                status=status,
            )
        )

    execution = {"execute": bool(args.execute), "planned_updates": 0, "applied_updates": 0, "errors": []}
    for item in planned:
        if item.status == "plan":
            execution["planned_updates"] += 1
    if args.execute:
        for item in planned:
            if item.status != "plan":
                continue
            errors = client.set_color_refs(item.product_gid, item.target_reference_ids.split("|"))
            if errors:
                execution["errors"].append({"handle": item.handle, "errors": errors})
            else:
                execution["applied_updates"] += 1
            if args.pause_ms > 0:
                time.sleep(args.pause_ms / 1000.0)

    with (output_dir / "planned_color_fixes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "product_id",
                "product_gid",
                "handle",
                "title",
                "current_labels",
                "target_labels",
                "target_reference_ids",
                "reason",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(asdict(item) for item in planned)

    summary = {
        "planned_products": len(planned),
        "execution": execution,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
