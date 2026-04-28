#!/usr/bin/env python3
"""Refresh paid-label eligibility artifacts from a fresh Shopify Admin read."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.apply_paid_economics_gate import (  # noqa: E402
    DEFAULT_AOV_BENCHMARK,
    ProductGateEvidence,
    paid_gate_for_row,
    parse_money,
)
from ops.scripts.shopify_admin_config import (  # noqa: E402
    load_access_token,
    resolve_store_domain,
)


API_VERSION = "2026-04"
PAGE_SIZE = 100
MERCHANT_CENTER_FEED_LABEL = "US"
CANONICAL_OUTPUT_PREFIX = "PAID_LABEL_FRESH_SHOPIFY"
RECOMMENDED_UPLOAD_DESTINATION = "merchant_center_supplemental_feed_paid_status_only"
VALID_UPLOAD_DESTINATIONS = {
    RECOMMENDED_UPLOAD_DESTINATION,
    "merchant_center_supplemental_feed_full_custom_labels",
    "shopify_product_metafields_mm-google-shopping",
}


PRODUCT_VARIANTS_QUERY = """
query ProductVariants($first: Int!, $after: String, $query: String!) {
  productVariants(first: $first, after: $after, query: $query, sortKey: ID) {
    nodes {
      id
      legacyResourceId
      title
      sku
      price
      compareAtPrice
      barcode
      inventoryQuantity
      inventoryPolicy
      inventoryItem {
        id
        legacyResourceId
        tracked
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
        productType
        vendor
        tags
        onlineStoreUrl
        totalInventory
        createdAt
        updatedAt
        publishedAt
        featuredImage {
          url
          altText
        }
        collections(first: 10) {
          nodes {
            handle
            title
          }
        }
        resourcePublications(first: 20) {
          edges {
            node {
              isPublished
              publication {
                name
              }
            }
          }
        }
        marketingMetafields: metafields(first: 20, namespace: "marketing") {
          nodes {
            id
            namespace
            key
            type
            value
          }
        }
        googleShoppingMetafields: metafields(first: 20, namespace: "mm-google-shopping") {
          nodes {
            id
            namespace
            key
            type
            value
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


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
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
                throttled = any(
                    ((err.get("extensions") or {}).get("code") == "THROTTLED")
                    for err in body.get("errors", [])
                    if isinstance(err, dict)
                )
                if throttled and attempt < 6:
                    time.sleep(min(30.0, (2.0**attempt) + random.uniform(1.0, 3.0)))
                    continue
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")

            throttle = (body.get("extensions") or {}).get("cost", {}).get("throttleStatus", {})
            currently_available = float(throttle.get("currentlyAvailable", 1000))
            if currently_available < 200:
                time.sleep((200 - currently_available) / 100.0)

            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def metafield_map(product: dict[str, Any], alias: str) -> dict[str, dict[str, str]]:
    nodes = ((product.get(alias) or {}).get("nodes")) or []
    return {node.get("key", ""): node for node in nodes}


def merchant_center_offer_id(product_id: str, variant_id: str) -> str:
    return f"shopify_{MERCHANT_CENTER_FEED_LABEL}_{product_id}_{variant_id}"


def unit_cost_amount(variant: dict[str, Any]) -> str:
    unit_cost = ((variant.get("inventoryItem") or {}).get("unitCost")) or {}
    return str(unit_cost.get("amount") or "")


def price_bucket(price: Decimal | None) -> str:
    if price is None:
        return "UNKNOWN_PRICE"
    if price < Decimal("25"):
        return "UNDER_25"
    if price < Decimal("50"):
        return "25_50"
    if price < Decimal("75"):
        return "50_75"
    return "75_PLUS"


def margin_label(price: Decimal | None, unit_cost: Decimal | None) -> str:
    if price is None or price <= 0 or unit_cost is None:
        return "UNKNOWN_MARGIN"
    gross_margin = (price - unit_cost) / price
    if gross_margin >= Decimal("0.65"):
        return "HIGH_MARGIN"
    if gross_margin >= Decimal("0.50"):
        return "GOOD_MARGIN"
    if gross_margin >= Decimal("0.35"):
        return "MID_MARGIN"
    return "LOW_MARGIN"


def product_collection_handles(product: dict[str, Any]) -> str:
    nodes = ((product.get("collections") or {}).get("nodes")) or []
    return "|".join(sorted({node.get("handle", "") for node in nodes if node.get("handle")}))


def product_publication_names(product: dict[str, Any]) -> str:
    names: list[str] = []
    edges = ((product.get("resourcePublications") or {}).get("edges")) or []
    for edge in edges:
        node = edge.get("node") or {}
        if not node.get("isPublished"):
            continue
        publication = node.get("publication") or {}
        name = (publication.get("name") or "").strip()
        if name:
            names.append(name)
    return "|".join(sorted(set(names)))


def primary_image_url(product: dict[str, Any]) -> str:
    image = product.get("featuredImage") or {}
    return image.get("url") or ""


def fetch_active_variants(client: ShopifyClient) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        data = client.graphql(
            PRODUCT_VARIANTS_QUERY,
            {
                "first": PAGE_SIZE,
                "after": after,
                "query": "product_status:active",
            },
        )
        page = data["productVariants"]
        variants.extend(page["nodes"])
        if len(variants) % 1000 == 0:
            print(f"fetched {len(variants)} active variants", file=sys.stderr)
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return variants


@dataclass
class BuildResult:
    raw_export_path: Path
    eligibility_path: Path
    custom_labels_path: Path
    supplemental_full_path: Path
    supplemental_paid_status_path: Path
    destination_approval_path: Path
    summary_path: Path


def build_rows(
    variants: list[dict[str, Any]],
    aov_benchmark: Decimal,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    eligibility_rows: list[dict[str, str]] = []
    custom_label_rows: list[dict[str, str]] = []
    supplemental_full_rows: list[dict[str, str]] = []
    supplemental_paid_status_rows: list[dict[str, str]] = []

    for variant in variants:
        product = variant["product"]
        product_id = str(product["legacyResourceId"])
        variant_id = str(variant["legacyResourceId"])
        marketing = metafield_map(product, "marketingMetafields")
        google = metafield_map(product, "googleShoppingMetafields")
        marketing_margin_tier = (marketing.get("margin_tier", {}).get("value") or "").strip().lower()
        product_set_type = (marketing.get("product_set_type", {}).get("value") or "").strip().lower()
        price = parse_money(variant.get("price"))
        unit_cost = parse_money(unit_cost_amount(variant))
        gate = paid_gate_for_row(
            {
                "price": str(variant.get("price") or ""),
                "unit_cost": unit_cost_amount(variant),
                "paid_status": "FIX_BEFORE_PAID",
                "paid_status_reasons": "",
            },
            ProductGateEvidence(
                product_set_type=product_set_type,
                marketing_margin_tier=marketing_margin_tier,
            ),
            aov_benchmark,
        )

        inventory_quantity = int(variant.get("inventoryQuantity") or 0)
        paid_status = gate.paid_status
        reasons = list(gate.reasons)
        if inventory_quantity <= 0:
            paid_status = "EXCLUDE_PAID"
            reasons.append("OUT_OF_STOCK")
        paid_eligible = not reasons

        paid_status_reasons = ";".join(reasons)
        offer_id = merchant_center_offer_id(product_id, variant_id)
        online_store_url = product.get("onlineStoreUrl") or ""
        published_channels = product_publication_names(product)
        online_store_published = bool(online_store_url)
        label_0 = google.get("custom_label_0", {}).get("value") or marketing_margin_tier
        label_1 = google.get("custom_label_1", {}).get("value") or product_set_type
        label_2 = google.get("custom_label_2", {}).get("value") or (
            marketing.get("best_seller", {}).get("value") or ""
        )
        label_3 = google.get("custom_label_3", {}).get("value") or (
            marketing.get("seasonality", {}).get("value") or ""
        )

        eligibility_rows.append(
            {
                "merchant_center_id": offer_id,
                "product_id": product_id,
                "product_gid": product["id"],
                "handle": product["handle"],
                "product_title": product["title"],
                "product_status": product["status"],
                "variant_id": variant_id,
                "variant_gid": variant["id"],
                "variant_title": variant["title"],
                "sku": variant.get("sku") or "",
                "barcode": variant.get("barcode") or "",
                "price": str(variant.get("price") or ""),
                "compare_at_price": str(variant.get("compareAtPrice") or ""),
                "unit_cost": unit_cost_amount(variant),
                "margin_label": margin_label(price, unit_cost),
                "inventory_tracked": str((variant.get("inventoryItem") or {}).get("tracked")),
                "inventory_quantity": str(inventory_quantity),
                "inventory_policy": variant.get("inventoryPolicy") or "",
                "product_type": product.get("productType") or "",
                "vendor": product.get("vendor") or "",
                "tags": "|".join(product.get("tags") or []),
                "collections": product_collection_handles(product),
                "primary_image_url": primary_image_url(product),
                "online_store_url": online_store_url,
                "online_store_published": "TRUE" if online_store_published else "FALSE",
                "published_sales_channels": published_channels,
                "market_availability": "online_store_available" if online_store_published else "not_online_store_available",
                "marketing_product_set_type": product_set_type,
                "marketing_margin_tier": marketing_margin_tier,
                "marketing_best_seller": marketing.get("best_seller", {}).get("value") or "",
                "marketing_seasonality": marketing.get("seasonality", {}).get("value") or "",
                "marketing_price_tier": marketing.get("price_tier", {}).get("value") or "",
                "current_google_custom_label_0": google.get("custom_label_0", {}).get("value") or "",
                "current_google_custom_label_1": google.get("custom_label_1", {}).get("value") or "",
                "current_google_custom_label_2": google.get("custom_label_2", {}).get("value") or "",
                "current_google_custom_label_3": google.get("custom_label_3", {}).get("value") or "",
                "current_google_custom_label_4": google.get("custom_label_4", {}).get("value") or "",
                "aov_benchmark": str(aov_benchmark),
                "reliable_cost_basis": "TRUE" if gate.reliable_cost_basis else "FALSE",
                "paid_eligible": "TRUE" if paid_eligible else "FALSE",
                "economics_gate_status": "BLOCKED" if reasons else gate.gate_status,
                "economics_gate_reasons": "|".join(reasons),
                "economics_gate_exceptions": "|".join(gate.exceptions),
                "paid_status": paid_status,
                "paid_status_reasons": paid_status_reasons,
            }
        )

        custom_label_rows.append(
            {
                "merchant_center_id": offer_id,
                "product_id": product_id,
                "handle": product["handle"],
                "variant_id": variant_id,
                "sku": variant.get("sku") or "",
                "custom_label_0_margin_tier": label_0,
                "custom_label_1_product_set_type": label_1,
                "custom_label_2_best_seller": label_2,
                "custom_label_3_seasonality": label_3,
                "custom_label_4_paid_status": paid_status,
            }
        )
        supplemental_full_rows.append(
            {
                "id": offer_id,
                "custom_label_0": label_0,
                "custom_label_1": label_1,
                "custom_label_2": label_2,
                "custom_label_3": label_3,
                "custom_label_4": paid_status,
            }
        )
        supplemental_paid_status_rows.append({"id": offer_id, "custom_label_4": paid_status})

    return eligibility_rows, custom_label_rows, supplemental_full_rows, supplemental_paid_status_rows


def write_destination_approval(path: Path, summary: dict[str, Any], result_paths: BuildResult) -> None:
    approved_destination = summary.get("approved_upload_destination") or ""
    if approved_destination:
        approval_lines = [
            f"Destination approved for a future writeback: `{approved_destination}`.",
            "",
            "Prepared locally only. Not uploaded. No Shopify, Merchant Center, feed, or ads write was performed.",
            "",
            "Rejected for this gate:",
            "",
            "- `merchant_center_supplemental_feed_full_custom_labels` because it would also override existing non-paid labels.",
            "- `shopify_product_metafields_mm-google-shopping` because those labels are product-level in this store and live `custom_label_4` currently stores price tier.",
        ]
    else:
        approval_lines = [
            "Prepared locally only. Not uploaded. No Shopify, Merchant Center, feed, or ads write was performed.",
            "",
            "Before upload, explicitly approve one destination:",
            "",
            f"- `{RECOMMENDED_UPLOAD_DESTINATION}`",
            "- `merchant_center_supplemental_feed_full_custom_labels`",
            "- `shopify_product_metafields_mm-google-shopping` (not recommended for this gate)",
        ]

    path.write_text(
        "\n".join(
            [
                "# Paid Label Upload Destination Approval",
                "",
                f"Generated: {summary['generated_at']}",
                "",
                "## Recommended Destination",
                "",
                "Use a Google Merchant Center supplemental feed keyed by Shopify item IDs",
                "(`shopify_US_<product_id>_<variant_id>`) for paid-status labels.",
                "",
                "Reason: the paid gate is variant-level. Shopify `mm-google-shopping.custom_label_*`",
                "metafields are product-level in this store, and live `custom_label_4` currently",
                "stores price tier. A supplemental feed can override or test paid-status labels",
                "without mutating Shopify product metafields first.",
                "",
                "## Prepared Upload Preview Files",
                "",
                f"- Full custom-label preview: `{result_paths.supplemental_full_path}`",
                f"- Paid-status-only preview: `{result_paths.supplemental_paid_status_path}`",
                "",
                "## Approval Status",
                "",
                *approval_lines,
                "",
                "## Current Counts",
                "",
                f"- Active variant rows: {summary['active_variant_rows']}",
                f"- Missing unit-cost rows: {summary['missing_unit_cost_rows']}",
                f"- Paid eligible rows: {summary['paid_eligible_rows']}",
                f"- Paid status counts: {json.dumps(summary['paid_status_counts'], sort_keys=True)}",
                f"- Gate reason counts: {json.dumps(summary['gate_reason_counts'], sort_keys=True)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def refresh_paid_label_export(
    output_root: Path,
    stamp: str,
    store_domain: str,
    access_token: str,
    aov_benchmark: Decimal,
    approved_upload_destination: str = "",
) -> BuildResult:
    client = ShopifyClient(store_domain, access_token, API_VERSION)
    variants = fetch_active_variants(client)

    raw_path = (
        output_root
        / "01_EXPORTS_RAW"
        / "SHOPIFY"
        / f"{stamp}_{CANONICAL_OUTPUT_PREFIX}_raw.json"
    )
    analysis_dir = output_root / "03_LOCAL_ANALYSIS"
    packet_dir = output_root / "02_AUDIT_PACKETS" / f"{stamp}_{CANONICAL_OUTPUT_PREFIX}_ARTIFACTS"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    packet_dir.mkdir(parents=True, exist_ok=True)

    raw_payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "store_domain": store_domain,
        "api_version": API_VERSION,
        "purpose": "Fresh read-only Shopify export before any feed/custom-label writeback.",
        "privacy_note": "No customer data, tokens, cookies, payment details, or order names are exported.",
        "active_variant_count": len(variants),
        "variants": variants,
    }
    raw_path.write_text(json.dumps(raw_payload, indent=2) + "\n", encoding="utf-8")

    (
        eligibility_rows,
        custom_label_rows,
        supplemental_full_rows,
        supplemental_paid_status_rows,
    ) = build_rows(variants, aov_benchmark)

    eligibility_path = analysis_dir / f"{stamp}_{CANONICAL_OUTPUT_PREFIX}_product_eligibility.csv"
    custom_labels_path = analysis_dir / f"{stamp}_{CANONICAL_OUTPUT_PREFIX}_custom_labels.csv"
    supplemental_full_path = packet_dir / "merchant_center_supplemental_full_custom_labels.csv"
    supplemental_paid_status_path = packet_dir / "merchant_center_supplemental_paid_status_only.csv"
    destination_path = packet_dir / "upload_destination_approval.md"
    summary_path = analysis_dir / f"{stamp}_{CANONICAL_OUTPUT_PREFIX}_summary.json"

    eligibility_fields = list(eligibility_rows[0].keys()) if eligibility_rows else []
    custom_label_fields = list(custom_label_rows[0].keys()) if custom_label_rows else []
    write_csv(eligibility_path, eligibility_fields, eligibility_rows)
    write_csv(custom_labels_path, custom_label_fields, custom_label_rows)
    write_csv(
        supplemental_full_path,
        ["id", "custom_label_0", "custom_label_1", "custom_label_2", "custom_label_3", "custom_label_4"],
        supplemental_full_rows,
    )
    write_csv(
        supplemental_paid_status_path,
        ["id", "custom_label_4"],
        supplemental_paid_status_rows,
    )

    paid_status_counts = Counter(row["paid_status"] for row in eligibility_rows)
    gate_reason_counts = Counter(
        reason
        for row in eligibility_rows
        for reason in row["economics_gate_reasons"].split("|")
        if reason
    )
    approval_status = (
        "DESTINATION_APPROVED_LOCAL_ONLY_NO_UPLOAD"
        if approved_upload_destination
        else "PENDING_OPERATOR_DESTINATION_APPROVAL"
    )
    summary = {
        "generated_at": raw_payload["generated_at"],
        "store_domain": store_domain,
        "api_version": API_VERSION,
        "raw_export": str(raw_path),
        "active_variant_rows": len(eligibility_rows),
        "active_product_count": len({row["product_id"] for row in eligibility_rows}),
        "aov_benchmark": str(aov_benchmark),
        "paid_status_counts": dict(sorted(paid_status_counts.items())),
        "gate_reason_counts": dict(sorted(gate_reason_counts.items())),
        "reliable_cost_basis_rows": sum(
            1 for row in eligibility_rows if row["reliable_cost_basis"] == "TRUE"
        ),
        "paid_eligible_rows": sum(
            1 for row in eligibility_rows if row["paid_eligible"] == "TRUE"
        ),
        "missing_unit_cost_rows": sum(1 for row in eligibility_rows if not row["unit_cost"]),
        "recommended_upload_destination": RECOMMENDED_UPLOAD_DESTINATION,
        "approved_upload_destination": approved_upload_destination,
        "approval_status": approval_status,
        "write_status": "NO_SHOPIFY_OR_FEED_WRITES",
        "files": {
            "product_eligibility": str(eligibility_path),
            "custom_labels": str(custom_labels_path),
            "merchant_center_supplemental_full_custom_labels": str(supplemental_full_path),
            "merchant_center_supplemental_paid_status_only": str(supplemental_paid_status_path),
            "upload_destination_approval": str(destination_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result_paths = BuildResult(
        raw_export_path=raw_path,
        eligibility_path=eligibility_path,
        custom_labels_path=custom_labels_path,
        supplemental_full_path=supplemental_full_path,
        supplemental_paid_status_path=supplemental_paid_status_path,
        destination_approval_path=destination_path,
        summary_path=summary_path,
    )
    write_destination_approval(destination_path, summary, result_paths)
    return result_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fresh Shopify read and paid-label artifact refresh. Read-only."
    )
    parser.add_argument("--output-root", type=Path, default=Path("dresslikemommy-growth-2026"))
    parser.add_argument("--stamp", default=now_stamp())
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--aov-benchmark", default=str(DEFAULT_AOV_BENCHMARK))
    parser.add_argument(
        "--approve-upload-destination",
        choices=sorted(VALID_UPLOAD_DESTINATIONS),
        default="",
        help="Record a local approval for the future upload destination. Does not upload.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(
        args.store_domain,
        fallback_domain="dresslikemommy-com.myshopify.com",
    )
    access_token = load_access_token(args.access_token)
    paths = refresh_paid_label_export(
        output_root=args.output_root,
        stamp=args.stamp,
        store_domain=store_domain,
        access_token=access_token,
        aov_benchmark=Decimal(str(args.aov_benchmark)),
        approved_upload_destination=args.approve_upload_destination,
    )
    print(f"raw_export={paths.raw_export_path}")
    print(f"summary={paths.summary_path}")
    print(f"destination_approval={paths.destination_approval_path}")


if __name__ == "__main__":
    main()
