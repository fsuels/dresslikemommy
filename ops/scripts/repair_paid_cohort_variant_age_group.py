#!/usr/bin/env python3
"""Repair Google age_group at Shopify variant level for the paid cohort only.

The Google & YouTube channel exposes Google Shopping attributes as
ProductVariant metafields under `mm-google-shopping`. This script intentionally
touches only the `mm-google-shopping.age_group` variant metafield for variants
listed in the paid-cohort age-group packet.
"""

from __future__ import annotations

import argparse
import csv
import json
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
DEFAULT_INPUT = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-06-live-visual-qa-merchant-age-group-gate/"
    "paid_cohort_age_group_after_patch_rows.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-07-merchant-paid-cohort-age-group-recheck-repair/"
    "shopify-variant-age-group-repair"
)
ALLOWED_AGE_GROUPS = {"newborn", "infant", "toddler", "kids", "adult"}


VARIANTS_QUERY = """
query Variants($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on ProductVariant {
      id
      legacyResourceId
      title
      ageGroup: metafield(namespace: "mm-google-shopping", key: "age_group") {
        id
        type
        value
      }
      product {
        id
        legacyResourceId
        handle
        title
        status
        publishedAt
      }
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
      type
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


@dataclass(frozen=True)
class PaidRow:
    merchant_center_item_id: str
    product_id: str
    variant_id: str
    variant_gid: str
    handle: str
    title: str
    variant_title: str
    desired_age_group: str
    confidence: str
    source_size: str


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
                text = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {text}") from exc
            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def fetch_variants(self, variant_gids: list[str], *, batch_size: int) -> dict[str, dict[str, Any]]:
        variants: dict[str, dict[str, Any]] = {}
        for batch in chunks(variant_gids, batch_size):
            data = self.graphql(VARIANTS_QUERY, {"ids": batch})["nodes"]
            for node in data:
                if not node:
                    continue
                variants[str(node["id"])] = node
        return variants

    def set_age_groups(self, updates: list[dict[str, str]], *, batch_size: int, pause_ms: int) -> dict[str, Any]:
        summary = {"attempted_updates": len(updates), "applied_batches": 0, "errors": []}
        for batch in chunks(updates, batch_size):
            metafields = [
                {
                    "ownerId": item["variant_gid"],
                    "namespace": "mm-google-shopping",
                    "key": "age_group",
                    "type": "single_line_text_field",
                    "value": item["desired_age_group"],
                }
                for item in batch
            ]
            data = self.graphql(METAFIELDS_SET_MUTATION, {"metafields": metafields})["metafieldsSet"]
            user_errors = data.get("userErrors") or []
            if user_errors:
                summary["errors"].append({"batch_variant_ids": [item["variant_id"] for item in batch], "userErrors": user_errors})
            else:
                summary["applied_batches"] += 1
            if pause_ms > 0:
                time.sleep(pause_ms / 1000.0)
        return summary


def clean(value: Any) -> str:
    return str(value or "").strip()


def chunks(values: list[Any], size: int) -> list[list[Any]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def load_paid_rows(path: Path) -> list[PaidRow]:
    rows: list[PaidRow] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            variant_id = clean(row.get("variant_id"))
            if not variant_id or variant_id in seen:
                continue
            seen.add(variant_id)
            rows.append(
                PaidRow(
                    merchant_center_item_id=clean(row.get("merchant_center_item_id")),
                    product_id=clean(row.get("product_id")),
                    variant_id=variant_id,
                    variant_gid=f"gid://shopify/ProductVariant/{variant_id}",
                    handle=clean(row.get("handle")),
                    title=clean(row.get("title")),
                    variant_title=clean(row.get("variant_title")),
                    desired_age_group=clean(row.get("derived_age_group")).lower(),
                    confidence=clean(row.get("confidence")).lower(),
                    source_size=clean(row.get("source_size")),
                )
            )
    return rows


def load_id_set(path: str) -> set[str]:
    if not path:
        return set()
    candidate = Path(path)
    if not candidate.exists():
        raise RuntimeError(f"ID file not found: {candidate}")
    return {line.strip() for line in candidate.read_text(encoding="utf-8").splitlines() if line.strip()}


def build_plan(rows: list[PaidRow], live_variants: dict[str, dict[str, Any]], missing_ids: set[str]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for row in rows:
        live = live_variants.get(row.variant_gid)
        product = (live or {}).get("product") or {}
        current_age = clean(((live or {}).get("ageGroup") or {}).get("value")).lower()
        status = "skip"
        reason = ""

        if row.confidence != "high":
            reason = f"confidence_not_high:{row.confidence}"
        elif row.desired_age_group not in ALLOWED_AGE_GROUPS:
            reason = f"invalid_age_group:{row.desired_age_group}"
        elif not live:
            reason = "variant_not_found_live"
        elif clean(product.get("legacyResourceId")) != row.product_id:
            reason = "product_id_mismatch"
        elif clean(product.get("status")) != "ACTIVE":
            reason = f"product_not_active:{clean(product.get('status'))}"
        elif not clean(product.get("publishedAt")):
            reason = "product_not_published"
        elif current_age == row.desired_age_group:
            reason = "already_correct"
        else:
            status = "plan"
            reason = "blank_age_group" if not current_age else "different_age_group"

        plan.append(
            {
                "merchant_center_item_id": row.merchant_center_item_id,
                "product_id": row.product_id,
                "variant_id": row.variant_id,
                "variant_gid": row.variant_gid,
                "handle": row.handle,
                "title": row.title,
                "variant_title": row.variant_title,
                "source_size": row.source_size,
                "desired_age_group": row.desired_age_group,
                "confidence": row.confidence,
                "current_variant_age_group": current_age,
                "live_product_status": clean(product.get("status")),
                "live_product_published_at": clean(product.get("publishedAt")),
                "live_product_handle": clean(product.get("handle")),
                "in_latest_missing_age_group_export": "true" if row.merchant_center_item_id in missing_ids else "false",
                "status": status,
                "reason": reason,
            }
        )
    return plan


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(plan: list[dict[str, Any]], *, execute: bool, execution: dict[str, Any] | None = None) -> dict[str, Any]:
    reason_counts: dict[str, int] = {}
    planned_by_age_group: dict[str, int] = {}
    for row in plan:
        reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0) + 1
        if row["status"] == "plan":
            key = row["desired_age_group"]
            planned_by_age_group[key] = planned_by_age_group.get(key, 0) + 1
    return {
        "execute": execute,
        "target_paid_variant_rows": len(plan),
        "planned_updates": sum(1 for row in plan if row["status"] == "plan"),
        "skipped_rows": sum(1 for row in plan if row["status"] != "plan"),
        "planned_by_age_group": planned_by_age_group,
        "reason_counts": reason_counts,
        "execution": execution or {"execute": False},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Set Shopify variant Google age_group for the current paid cohort only.")
    parser.add_argument("--input-csv", default=str(DEFAULT_INPUT), help="Paid cohort age-group CSV.")
    parser.add_argument("--missing-ids-file", default="", help="Optional latest Merchant missing-age-group item ID list.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output artifact directory.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin access token.")
    parser.add_argument("--execute", action="store_true", help="Apply planned Shopify variant metafield updates.")
    parser.add_argument("--query-batch-size", type=int, default=100)
    parser.add_argument("--write-batch-size", type=int, default=25)
    parser.add_argument("--pause-ms", type=int, default=200)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_paid_rows(Path(args.input_csv))
    missing_ids = load_id_set(args.missing_ids_file)
    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    live_variants = client.fetch_variants([row.variant_gid for row in rows], batch_size=max(args.query_batch_size, 1))
    plan = build_plan(rows, live_variants, missing_ids)

    fieldnames = [
        "merchant_center_item_id",
        "product_id",
        "variant_id",
        "variant_gid",
        "handle",
        "title",
        "variant_title",
        "source_size",
        "desired_age_group",
        "confidence",
        "current_variant_age_group",
        "live_product_status",
        "live_product_published_at",
        "live_product_handle",
        "in_latest_missing_age_group_export",
        "status",
        "reason",
    ]
    write_csv(output_dir / "planned_variant_age_group_updates.csv", plan, fieldnames)

    updates = [
        {
            "variant_gid": row["variant_gid"],
            "variant_id": row["variant_id"],
            "desired_age_group": row["desired_age_group"],
        }
        for row in plan
        if row["status"] == "plan"
    ]
    execution = client.set_age_groups(updates, batch_size=max(args.write_batch_size, 1), pause_ms=max(args.pause_ms, 0)) if args.execute else {"execute": False}

    summary = summarize(plan, execute=args.execute, execution=execution)

    if args.execute:
        post_live = client.fetch_variants([row.variant_gid for row in rows], batch_size=max(args.query_batch_size, 1))
        post_plan = build_plan(rows, post_live, missing_ids)
        write_csv(output_dir / "post_write_variant_age_group_readback.csv", post_plan, fieldnames)
        summary["post_write"] = summarize(post_plan, execute=False)

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
