#!/usr/bin/env python3
"""Restore missing Golden Daisy chart-backed variants without changing publish state."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "ops/scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "ops/scripts"))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


HANDLE = "golden-daisy-mommy-and-me-set"
PRODUCT_GID = "gid://shopify/Product/7546613530721"
SIZE_CHART_PATH = ROOT / "ops/listings/size-chart-golden-daisy-mommy-and-me-set.json"
REPORT_PATH = ROOT / "ops/listings/golden-daisy-top-restore-report.json"

SHORTCODE = "GDSY"
COLOR_TOKEN = "GOLDIV"
CHILD_PRICE = "28.99"
MOTHER_PRICE = "31.99"

TYPE_TOKEN = {"Top": "TOP", "Pants": "PNT"}
ROLE_TOKEN = {
    "Girl Top": "GRL",
    "Mother Top": "MOM",
    "Girl Pants": "GRL",
    "Mother Pants": "MOM",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Apply missing variant restore in Shopify.")
    parser.add_argument("--pause-ms", type=int, default=500, help="Pause between create and update calls.")
    return parser.parse_args()


def gql(api: str, token: str, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        api,
        data=payload,
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            data = json.loads(res.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode()) from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def require_no_user_errors(payload: dict[str, Any], path: list[str]) -> None:
    current: Any = payload
    for key in path:
        current = current[key]
    if current:
        raise RuntimeError(json.dumps(current, indent=2))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def price_for(row: dict[str, Any]) -> str:
    return MOTHER_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict[str, Any]) -> str:
    return f"DLM-{SHORTCODE}-{ROLE_TOKEN[row['role']]}-{TYPE_TOKEN[row['garment']]}-{row['sku_suffix']}-{COLOR_TOKEN}"


def spec_variant(row: dict[str, Any]) -> dict[str, Any]:
    price = price_for(row)
    return {
        "price": price,
        "compareAtPrice": compare_at(price),
        "taxable": True,
        "inventoryPolicy": "DENY",
        "optionValues": [
            {"optionName": "Type", "name": row["garment"]},
            {"optionName": "Size", "name": row["picker_label"]},
        ],
        "inventoryItem": {
            "sku": sku_for(row),
            "cost": cost_for(price),
            "tracked": True,
            "requiresShipping": True,
        },
    }


def unique_values(rows: list[dict[str, Any]], key: str) -> list[str]:
    values: list[str] = []
    for row in rows:
        value = row[key]
        if value not in values:
            values.append(value)
    return values


def product_query(api: str, token: str) -> dict[str, Any]:
    query = """
    query GoldenDaisyTopRestore($handle: String!) {
      productByHandle(handle: $handle) {
        id
        title
        handle
        status
        publishedAt
        onlineStoreUrl
        descriptionHtml
        tags
        seo { title description }
        options { id name position values }
        variants(first: 100) {
          nodes {
            id
            legacyResourceId
            title
            sku
            price
            compareAtPrice
            inventoryPolicy
            selectedOptions { name value }
            inventoryItem {
              id
              tracked
              requiresShipping
              unitCost { amount currencyCode }
            }
          }
        }
        resourcePublicationsV2(first: 20) {
          nodes { isPublished publication { name } }
        }
      }
    }
    """
    product = gql(api, token, query, {"handle": HANDLE})["productByHandle"]
    if not product:
        raise RuntimeError(f"Product not found: {HANDLE}")
    if product["id"] != PRODUCT_GID:
        raise RuntimeError(f"Unexpected product id for {HANDLE}: {product['id']}")
    return product


def create_missing_variants(api: str, token: str, product_id: str, variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not variants:
        return []
    mutation = """
    mutation GoldenDaisyCreateMissing($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
      productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
        productVariants {
          id
          sku
          title
          price
          compareAtPrice
          inventoryPolicy
          selectedOptions { name value }
          inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
        }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        api,
        token,
        mutation,
        {
            "productId": product_id,
            "variants": variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        },
    )
    require_no_user_errors(payload, ["productVariantsBulkCreate", "userErrors"])
    return payload["productVariantsBulkCreate"]["productVariants"] or []


def update_variants(api: str, token: str, product_id: str, variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not variants:
        return []
    mutation = """
    mutation GoldenDaisyUpdateRestored($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
      productVariantsBulkUpdate(productId: $productId, variants: $variants, allowPartialUpdates: false) {
        productVariants {
          id
          sku
          title
          price
          compareAtPrice
          inventoryPolicy
          selectedOptions { name value }
          inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
        }
        userErrors { field message }
      }
    }
    """
    payload = gql(api, token, mutation, {"productId": product_id, "variants": variants})
    require_no_user_errors(payload, ["productVariantsBulkUpdate", "userErrors"])
    return payload["productVariantsBulkUpdate"]["productVariants"] or []


def reorder_options(api: str, token: str, product_id: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutation = """
    mutation GoldenDaisyOptionOrder($productId: ID!, $options: [OptionReorderInput!]!) {
      productOptionsReorder(productId: $productId, options: $options) {
        product { id options { name position values } }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        api,
        token,
        mutation,
        {
            "productId": product_id,
            "options": [
                {"name": "Type", "values": [{"name": value} for value in unique_values(rows, "garment")]},
                {"name": "Size", "values": [{"name": value} for value in unique_values(rows, "picker_label")]},
            ],
        },
    )
    require_no_user_errors(payload, ["productOptionsReorder", "userErrors"])
    return payload["productOptionsReorder"]["product"]["options"] or []


def option_pair(variant: dict[str, Any]) -> tuple[str, str]:
    values = {item["name"]: item["value"] for item in variant.get("selectedOptions") or []}
    return (values.get("Type", ""), values.get("Size", ""))


def live_summary(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": product["status"],
        "published_at": product.get("publishedAt"),
        "online_store_url": product.get("onlineStoreUrl"),
        "options": [{"name": option["name"], "values": option["values"]} for option in product.get("options") or []],
        "variant_count": len(product["variants"]["nodes"]),
        "publications": sorted(
            node["publication"]["name"]
            for node in product["resourcePublicationsV2"]["nodes"]
            if node["isPublished"]
        ),
    }


def validation(product: dict[str, Any], spec_by_sku: dict[str, dict[str, Any]]) -> dict[str, Any]:
    live = product["variants"]["nodes"]
    live_by_sku = {variant["sku"]: variant for variant in live if variant.get("sku")}
    missing = sorted(set(spec_by_sku) - set(live_by_sku))
    extra = sorted(set(live_by_sku) - set(spec_by_sku))
    mismatches = []
    for sku, spec in spec_by_sku.items():
        variant = live_by_sku.get(sku)
        if not variant:
            continue
        expected_pair = tuple(item["name"] for item in spec["optionValues"])
        live_pair = option_pair(variant)
        cost = ((variant.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        mismatch = {
            "sku": sku,
            "price_ok": Decimal(variant["price"]) == Decimal(spec["price"]),
            "compare_at_ok": Decimal(variant["compareAtPrice"]) == Decimal(spec["compareAtPrice"]),
            "cost_ok": cost is not None and Decimal(cost) == Decimal(spec["inventoryItem"]["cost"]),
            "options_ok": live_pair == expected_pair,
            "inventory_policy_ok": variant["inventoryPolicy"] == "DENY",
            "tracked_ok": bool((variant.get("inventoryItem") or {}).get("tracked")),
            "requires_shipping_ok": bool((variant.get("inventoryItem") or {}).get("requiresShipping")),
            "live_options": live_pair,
            "expected_options": expected_pair,
        }
        if not all(value for key, value in mismatch.items() if key.endswith("_ok")):
            mismatches.append(mismatch)
    text = " ".join(
        str(value or "")
        for value in [
            product.get("title"),
            product.get("descriptionHtml"),
            product.get("seo", {}).get("title"),
            product.get("seo", {}).get("description"),
            " ".join(product.get("tags") or []),
        ]
    )
    return {
        "missing_skus": missing,
        "extra_skus": extra,
        "mismatches": mismatches,
        "top_variant_count": sum(1 for variant in live if option_pair(variant)[0] == "Top"),
        "pants_variant_count": sum(1 for variant in live if option_pair(variant)[0] == "Pants"),
        "forbidden_source_tokens": [
            token
            for token in ["1688", "Alibaba", "detail.1688.com"]
            if token.lower() in text.lower()
        ],
    }


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    token = load_access_token()
    api = f"https://{store_domain}/admin/api/2025-01/graphql.json"

    rows = json.loads(SIZE_CHART_PATH.read_text(encoding="utf-8"))
    variants = [spec_variant(row) for row in rows]
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    if len(spec_by_sku) != 21:
        raise RuntimeError(f"Expected 21 unique spec variants, got {len(spec_by_sku)}")

    before = product_query(api, token)
    before_by_sku = {variant["sku"]: variant for variant in before["variants"]["nodes"] if variant.get("sku")}
    missing_variants = [variant for variant in variants if variant["inventoryItem"]["sku"] not in before_by_sku]

    created: list[dict[str, Any]] = []
    updated: list[dict[str, Any]] = []
    reordered_options: list[dict[str, Any]] = []
    after = before
    if args.execute:
        created = create_missing_variants(api, token, before["id"], missing_variants)
        if args.pause_ms > 0:
            time.sleep(args.pause_ms / 1000)
        after_create = product_query(api, token)
        after_by_sku = {variant["sku"]: variant for variant in after_create["variants"]["nodes"] if variant.get("sku")}
        update_inputs = []
        for sku, spec in spec_by_sku.items():
            live_variant = after_by_sku.get(sku)
            if live_variant:
                update_inputs.append({"id": live_variant["id"], **spec})
        updated = update_variants(api, token, after_create["id"], update_inputs)
        reordered_options = reorder_options(api, token, after_create["id"], rows)
        after = product_query(api, token)

    report = {
        "execute": bool(args.execute),
        "store_domain": store_domain,
        "product_gid": PRODUCT_GID,
        "handle": HANDLE,
        "before": live_summary(before),
        "missing_before": sorted(variant["inventoryItem"]["sku"] for variant in missing_variants),
        "created_skus": sorted(variant["sku"] for variant in created),
        "updated_skus": sorted(variant["sku"] for variant in updated),
        "reordered_options": reordered_options,
        "after": live_summary(after),
        "validation": validation(after, spec_by_sku),
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
