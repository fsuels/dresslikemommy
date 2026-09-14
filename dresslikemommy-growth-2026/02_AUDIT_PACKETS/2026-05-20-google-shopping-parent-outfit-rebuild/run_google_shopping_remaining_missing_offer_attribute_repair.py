#!/usr/bin/env python3
"""Narrow Google & YouTube attribute repair for remaining missing offers.

Scope is intentionally limited to the 8 approved Mommy & Me parent products
and the 141 missing expected offer IDs from the parent-outfit gate. The script
plans or writes only ProductVariant metafields in the `mm-google-shopping`
namespace for `age_group` and `size`.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
PACKET_DIR = Path(__file__).resolve().parent
MISSING_ROWS_CSV = PACKET_DIR / "google_shopping_parent_outfit_missing_expected_rows_20260521T070231Z.csv"
MISSING_PARENT_SUMMARY_CSV = PACKET_DIR / "google_shopping_parent_outfit_missing_expected_parent_summary_20260521T070231Z.csv"
TIMEOUT_SECONDS = 120
ALLOWED_AGE_GROUPS = {"newborn", "infant", "toddler", "kids", "adult"}


VARIANTS_QUERY = """
query Variants($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on ProductVariant {
      id
      legacyResourceId
      title
      sku
      selectedOptions {
        name
        value
      }
      ageGroup: metafield(namespace: "mm-google-shopping", key: "age_group") {
        id
        type
        value
      }
      googleSize: metafield(namespace: "mm-google-shopping", key: "size") {
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
        resourcePublications(first: 100) {
          edges {
            node {
              isPublished
              publication {
                id
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

PRODUCT_FEEDBACK_QUERY = """
query Product($id: ID!) {
  product(id: $id) {
    id
    legacyResourceId
    handle
    feedback {
      summary
      details {
        messages {
          field
          message
        }
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
            req = request.Request(self.endpoint, data=payload, headers=headers, method="POST")
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


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def chunks(values: list[Any], size: int) -> list[list[Any]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize(value: Any) -> str:
    return clean(value).lower()


def age_from_months(text: str) -> str:
    ranges = [(int(start), int(end)) for start, end in re.findall(r"\b(\d{1,2})\s*[-/]\s*(\d{1,2})\s*(?:m|mo|mos|month|months)\b", text)]
    if ranges:
        max_month = max(end for _start, end in ranges)
        return "newborn" if max_month <= 3 else "infant" if max_month <= 12 else "toddler"
    months = [int(value) for value in re.findall(r"\b(\d{1,2})\s*(?:m|mo|mos|month|months)\b", text)]
    if months:
        max_month = max(months)
        return "newborn" if max_month <= 3 else "infant" if max_month <= 12 else "toddler"
    return ""


def age_from_years(text: str) -> str:
    ranges = [(int(start), int(end)) for start, end in re.findall(r"\b(\d{1,2})\s*[-/]\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)?\b", text)]
    if ranges:
        max_age = max(end for _start, end in ranges)
        return "toddler" if max_age <= 5 else "kids"
    years = [int(value) for value in re.findall(r"\b(\d{1,2})\s*(?:t|y|yr|yrs|year|years)\b", text)]
    if years:
        max_age = max(years)
        return "toddler" if max_age <= 5 else "kids"
    return ""


def has_token(text: str, tokens: tuple[str, ...]) -> bool:
    return any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", text) for token in tokens)


def infer_age_group(variant: dict[str, Any]) -> tuple[str, str]:
    option_text = " ".join(clean(option.get("value")) for option in variant.get("selectedOptions") or [])
    text = normalize(" ".join([clean(variant.get("title")), clean(variant.get("sku")), option_text]))
    adult_tokens = ("mother", "mom", "mommy", "women", "woman", "adult", "s", "m", "l", "xl", "xxl")
    if has_token(text, ("newborn", "nb")):
        return "newborn", "variant_newborn_token"
    month_age = age_from_months(text)
    if month_age:
        return month_age, "variant_month_size"
    year_age = age_from_years(text)
    if year_age:
        return year_age, "variant_year_size"
    if has_token(text, ("baby", "infant")):
        return "infant", "variant_baby_token"
    if has_token(text, ("toddler",)):
        return "toddler", "variant_toddler_token"
    if has_token(text, adult_tokens):
        return "adult", "variant_adult_role_or_alpha_size"
    if has_token(text, ("child", "children", "kid", "kids", "girl", "girls", "boy", "boys")):
        return "kids", "variant_child_role_token"
    return "", "unresolved_variant_text"


def infer_size(variant: dict[str, Any]) -> tuple[str, str]:
    options = variant.get("selectedOptions") or []
    for option in options:
        name = normalize(option.get("name"))
        value = clean(option.get("value"))
        if value and ("size" in name or "age" in name):
            return value, f"selected_option:{name}"
    for option in options:
        value = clean(option.get("value"))
        if not value:
            continue
        text = normalize(value)
        if has_token(text, ("mother", "mom", "mommy", "child", "kid", "kids", "baby")) or re.search(r"\b(?:xxs|xs|s|m|l|xl|xxl|2xl|3xl|\d{1,2}\s*[-/]\s*\d{1,2}\s*(?:years?|yrs?|y)?|\d{1,2}\s*(?:years?|yrs?|y))\b", text):
            return value, "selected_option_value_pattern"
    return clean(variant.get("title")), "variant_title_fallback"


def google_publication_is_published(product: dict[str, Any]) -> bool:
    for edge in product["resourcePublications"]["edges"]:
        node = edge["node"]
        publication = node.get("publication") or {}
        if publication.get("name") == "Google & YouTube":
            return bool(node.get("isPublished"))
    return False


def build_scope() -> tuple[dict[str, dict[str, str]], list[str], dict[str, set[str]]]:
    parent_summary = read_csv(MISSING_PARENT_SUMMARY_CSV)
    missing_rows = read_csv(MISSING_ROWS_CSV)
    parent_by_id = {row["parent_product_id"]: row for row in parent_summary}
    missing_by_parent: dict[str, set[str]] = {parent_id: set() for parent_id in parent_by_id}
    variant_ids: list[str] = []
    for row in missing_rows:
        parts = row["item_id"].split("_")
        if len(parts) < 4:
            raise RuntimeError(f"Unexpected Merchant item_id shape: {row['item_id']}")
        parent_id = row["parent_product_id"]
        variant_id = parts[-1]
        if parent_id not in parent_by_id:
            raise RuntimeError(f"Missing row parent {parent_id} is outside approved parent summary.")
        missing_by_parent[parent_id].add(variant_id)
        variant_ids.append(variant_id)
    if len(parent_by_id) != 8:
        raise RuntimeError(f"Expected exactly 8 approved parent products, found {len(parent_by_id)}.")
    if len(set(variant_ids)) != 141:
        raise RuntimeError(f"Expected exactly 141 approved missing offer IDs, found {len(set(variant_ids))}.")
    return parent_by_id, sorted(set(variant_ids)), missing_by_parent


def fetch_variants(client: ShopifyClient, variant_ids: list[str], batch_size: int) -> dict[str, dict[str, Any]]:
    variants: dict[str, dict[str, Any]] = {}
    gids = [f"gid://shopify/ProductVariant/{variant_id}" for variant_id in variant_ids]
    for batch in chunks(gids, batch_size):
        nodes = client.graphql(VARIANTS_QUERY, {"ids": batch})["nodes"]
        for node in nodes:
            if node:
                variants[str(node["legacyResourceId"])] = node
    return variants


def fetch_feedback(client: ShopifyClient, parent_ids: list[str]) -> list[dict[str, Any]]:
    readbacks: list[dict[str, Any]] = []
    for parent_id in parent_ids:
        product = client.graphql(PRODUCT_FEEDBACK_QUERY, {"id": f"gid://shopify/Product/{parent_id}"})["product"]
        feedback = product.get("feedback")
        messages: list[str] = []
        if feedback:
            for detail in feedback.get("details") or []:
                for message in detail.get("messages") or []:
                    messages.append(clean(message.get("message")))
        readbacks.append(
            {
                "parent_product_id": parent_id,
                "handle": product["handle"],
                "feedback_summary": feedback.get("summary") if feedback else None,
                "feedback_messages": messages,
            }
        )
    return readbacks


def build_plan(parent_by_id: dict[str, dict[str, str]], variants: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for variant_id, variant in sorted(variants.items()):
        product = variant["product"]
        parent_id = str(product["legacyResourceId"])
        parent = parent_by_id[parent_id]
        desired_age, age_source = infer_age_group(variant)
        desired_size, size_source = infer_size(variant)
        current_age = normalize(((variant.get("ageGroup") or {}).get("value")))
        current_size = clean(((variant.get("googleSize") or {}).get("value")))
        google_published = google_publication_is_published(product)
        planned_fields: list[str] = []
        blockers: list[str] = []
        if product["status"] != "ACTIVE":
            blockers.append(f"product_not_active:{product['status']}")
        if not google_published:
            blockers.append("product_not_google_published")
        if parent_id not in parent_by_id:
            blockers.append("product_outside_scope")
        if desired_age not in ALLOWED_AGE_GROUPS:
            blockers.append(f"unresolved_age_group:{age_source}")
        if not desired_size:
            blockers.append("unresolved_size")
        if not blockers:
            if current_age != desired_age:
                planned_fields.append("age_group")
            if current_size != desired_size:
                planned_fields.append("size")
        plan.append(
            {
                "parent_product_id": parent_id,
                "handle": product["handle"],
                "subgroup": parent.get("subgroup", ""),
                "variant_id": variant_id,
                "variant_gid": variant["id"],
                "variant_title": variant["title"],
                "selected_options": " | ".join(f"{clean(option.get('name'))}={clean(option.get('value'))}" for option in variant.get("selectedOptions") or []),
                "current_age_group": current_age,
                "desired_age_group": desired_age,
                "age_group_source": age_source,
                "current_size": current_size,
                "desired_size": desired_size,
                "size_source": size_source,
                "google_published": "true" if google_published else "false",
                "live_product_status": product["status"],
                "planned_fields": ",".join(planned_fields),
                "status": "plan" if planned_fields and not blockers else "skip",
                "reason": "needs_google_attribute_repair" if planned_fields and not blockers else (";".join(blockers) if blockers else "already_correct"),
            }
        )
    missing_live = sorted(set(parent_by_id) - {row["parent_product_id"] for row in plan})
    if missing_live:
        raise RuntimeError(f"Unexpected parent readback gap: {missing_live}")
    return plan


def apply_plan(client: ShopifyClient, plan: list[dict[str, Any]], batch_size: int, pause_ms: int) -> dict[str, Any]:
    updates: list[dict[str, str]] = []
    for row in plan:
        if row["status"] != "plan":
            continue
        fields = set(row["planned_fields"].split(","))
        if "age_group" in fields:
            updates.append(
                {
                    "ownerId": row["variant_gid"],
                    "namespace": "mm-google-shopping",
                    "key": "age_group",
                    "type": "single_line_text_field",
                    "value": row["desired_age_group"],
                }
            )
        if "size" in fields:
            updates.append(
                {
                    "ownerId": row["variant_gid"],
                    "namespace": "mm-google-shopping",
                    "key": "size",
                    "type": "single_line_text_field",
                    "value": row["desired_size"],
                }
            )
    execution: dict[str, Any] = {"attempted_metafield_updates": len(updates), "applied_batches": 0, "user_errors": []}
    for batch in chunks(updates, batch_size):
        data = client.graphql(METAFIELDS_SET_MUTATION, {"metafields": batch})["metafieldsSet"]
        user_errors = data.get("userErrors") or []
        if user_errors:
            execution["user_errors"].append({"batch_owner_ids": [item["ownerId"] for item in batch], "userErrors": user_errors})
        else:
            execution["applied_batches"] += 1
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)
    return execution


def summarize(plan: list[dict[str, Any]], *, apply_requested: bool, execution: dict[str, Any] | None = None) -> dict[str, Any]:
    planned_rows = [row for row in plan if row["status"] == "plan"]
    return {
        "apply_requested": apply_requested,
        "scoped_variant_rows": len(plan),
        "planned_variant_rows": len(planned_rows),
        "planned_metafield_updates": sum(len(row["planned_fields"].split(",")) for row in planned_rows if row["planned_fields"]),
        "planned_fields": dict(Counter(field for row in planned_rows for field in row["planned_fields"].split(",") if field)),
        "desired_age_group_counts": dict(Counter(row["desired_age_group"] for row in planned_rows)),
        "reason_counts": dict(Counter(row["reason"] for row in plan)),
        "execution": execution or {"execute": False},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply the approved narrow variant Google attribute repair.")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--output-prefix", default="")
    parser.add_argument("--query-batch-size", type=int, default=100)
    parser.add_argument("--write-batch-size", type=int, default=25)
    parser.add_argument("--pause-ms", type=int, default=200)
    args = parser.parse_args()

    parent_by_id, variant_ids, _missing_by_parent = build_scope()
    client = ShopifyClient(resolve_store_domain(args.store_domain), load_access_token())
    stamp = args.output_prefix or now_stamp()

    before_variants = fetch_variants(client, variant_ids, max(args.query_batch_size, 1))
    if len(before_variants) != 141:
        raise RuntimeError(f"Expected 141 live Shopify variants, found {len(before_variants)}.")
    before_plan = build_plan(parent_by_id, before_variants)
    fieldnames = [
        "parent_product_id",
        "handle",
        "subgroup",
        "variant_id",
        "variant_gid",
        "variant_title",
        "selected_options",
        "current_age_group",
        "desired_age_group",
        "age_group_source",
        "current_size",
        "desired_size",
        "size_source",
        "google_published",
        "live_product_status",
        "planned_fields",
        "status",
        "reason",
    ]
    before_plan_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_attribute_plan_{stamp}.csv"
    write_csv(before_plan_path, before_plan, fieldnames)

    execution = apply_plan(client, before_plan, max(args.write_batch_size, 1), max(args.pause_ms, 0)) if args.apply else {"execute": False}

    after_plan_path = None
    feedback_path = None
    if args.apply:
        after_variants = fetch_variants(client, variant_ids, max(args.query_batch_size, 1))
        after_plan = build_plan(parent_by_id, after_variants)
        after_plan_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_attribute_after_{stamp}.csv"
        write_csv(after_plan_path, after_plan, fieldnames)
        feedback_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_attribute_feedback_{stamp}.json"
        write_json(feedback_path, {"timestamp_utc": stamp, "product_feedback": fetch_feedback(client, sorted(parent_by_id))})

    summary = summarize(before_plan, apply_requested=args.apply, execution=execution)
    summary.update(
        {
            "timestamp_utc": stamp,
            "approved_scope": {
                "parent_products": len(parent_by_id),
                "missing_expected_offer_ids": len(variant_ids),
                "changed_namespace": "mm-google-shopping",
                "changed_keys": ["age_group", "size"],
            },
            "before_plan_path": str(before_plan_path),
            "after_plan_path": str(after_plan_path) if after_plan_path else None,
            "feedback_path": str(feedback_path) if feedback_path else None,
            "mutation_user_error_count": sum(len(item.get("userErrors") or []) for item in execution.get("user_errors", [])),
        }
    )
    summary_path = PACKET_DIR / f"google_shopping_remaining_missing_offer_attribute_repair_summary_{stamp}.json"
    write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if summary["mutation_user_error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
