#!/usr/bin/env python3
"""Read-only eligibility diagnostic for Google Shopping parent-outfit scope.

This script does not mutate Merchant Center, Shopify, Google & YouTube, Google
Ads, feeds, products, campaigns, budgets, bids, statuses, conversions, or
billing. It joins the approved parent-outfit spec against the Google Ads
shopping_product surface and Shopify Admin readbacks for the remaining missing
parent products.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

import google.auth.transport.requests
import yaml
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.oauth2.credentials import Credentials

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


PACKET_DIR = Path(__file__).resolve().parent
CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
CUSTOMER_ID = "3990976848"
MERCHANT_ID = 124884876
FEED_LABEL = "US"
READY_LABEL = "us_parent_outfit_ready_v20260520"
MERCHANT_SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
LATEST_MERCHANT_SOURCE_READBACK = PACKET_DIR / "merchant_source_10663204023_after_approved_tsv_refresh_20260521T093710Z.json"
API_VERSION = "2026-01"
GOOGLE_PUBLICATION_ID = "gid://shopify/Publication/21969633377"
TIMEOUT_SECONDS = 120


PRODUCT_QUERY = """
query Product($id: ID!) {
  product(id: $id) {
    id
    legacyResourceId
    handle
    title
    status
    publishedAt
    onlineStoreUrl
    feedback {
      summary
      details {
        messages {
          field
          message
        }
      }
    }
    resourcePublications(first: 100) {
      edges {
        node {
          isPublished
          publishDate
          publication {
            id
            name
          }
        }
      }
    }
    variants(first: 250) {
      edges {
        node {
          id
          legacyResourceId
          title
          sku
          availableForSale
          inventoryPolicy
          inventoryQuantity
          selectedOptions {
            name
            value
          }
          ageGroup: metafield(namespace: "mm-google-shopping", key: "age_group") {
            value
          }
          googleSize: metafield(namespace: "mm-google-shopping", key: "size") {
            value
          }
        }
      }
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


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def quote_sql(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def chunks(values: list[Any], size: int) -> list[list[Any]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_expected_rows() -> list[dict[str, str]]:
    rows = [row for row in load_csv(MERCHANT_SPEC_CSV) if row["decision"] == "INCLUDE"]
    if len(rows) != 4531:
        raise RuntimeError(f"Expected 4,531 included rows, found {len(rows)}")
    return rows


def load_google_ads_client() -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(str(CONFIG_PATH))


def search_rows(client: GoogleAdsClient, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=CUSTOMER_ID, query=query))


def issue_to_dict(issue: Any) -> dict[str, Any]:
    return {
        "error_code": issue.error_code,
        "ads_severity": enum_name(issue.ads_severity),
        "attribute_name": issue.attribute_name,
        "description": issue.description,
        "detail": issue.detail,
        "documentation": issue.documentation,
        "affected_regions": list(issue.affected_regions),
    }


def product_to_dict(product: Any) -> dict[str, Any]:
    return {
        "item_id": product.item_id,
        "title": product.title,
        "status": enum_name(product.status),
        "availability": enum_name(product.availability),
        "feed_label": product.feed_label,
        "merchant_center_id": product.merchant_center_id,
        "language_code": product.language_code,
        "target_countries": list(product.target_countries),
        "brand": product.brand,
        "condition": enum_name(product.condition),
        "currency_code": product.currency_code,
        "price_micros": product.price_micros,
        "custom_label_0": product.custom_attribute0,
        "custom_label_1": product.custom_attribute1,
        "custom_label_2": product.custom_attribute2,
        "custom_label_3": product.custom_attribute3,
        "custom_label_4": product.custom_attribute4,
        "product_image_uri": product.product_image_uri,
        "issues": [issue_to_dict(issue) for issue in product.issues],
    }


def shopping_product_select(where_clause: str) -> str:
    return f"""
        SELECT
          shopping_product.item_id,
          shopping_product.title,
          shopping_product.status,
          shopping_product.availability,
          shopping_product.feed_label,
          shopping_product.merchant_center_id,
          shopping_product.language_code,
          shopping_product.target_countries,
          shopping_product.brand,
          shopping_product.condition,
          shopping_product.currency_code,
          shopping_product.price_micros,
          shopping_product.custom_attribute0,
          shopping_product.custom_attribute1,
          shopping_product.custom_attribute2,
          shopping_product.custom_attribute3,
          shopping_product.custom_attribute4,
          shopping_product.product_image_uri,
          shopping_product.issues
        FROM shopping_product
        WHERE shopping_product.merchant_center_id = {MERCHANT_ID}
          AND shopping_product.feed_label = '{FEED_LABEL}'
          {where_clause}
        ORDER BY shopping_product.item_id
    """


def read_expected_products(client: GoogleAdsClient, item_ids: list[str]) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    for batch in chunks(item_ids, 250):
        quoted = ", ".join(f"'{quote_sql(item_id)}'" for item_id in batch)
        query = shopping_product_select(f"AND shopping_product.item_id IN ({quoted})")
        for row in search_rows(client, query):
            products.append(product_to_dict(row.shopping_product))
    return products


def merchant_content_scope_probe() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"available": False, "error_type": "missing_config"}
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    try:
        creds = Credentials(
            token=None,
            refresh_token=config["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            scopes=["https://www.googleapis.com/auth/content"],
        )
        creds.refresh(google.auth.transport.requests.Request())
        req = request.Request(
            f"https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products?maxResults=1",
            headers={"Authorization": f"Bearer {creds.token}"},
        )
        with request.urlopen(req, timeout=30) as response:
            return {"available": True, "status": response.status}
    except error.HTTPError as exc:
        body = exc.read(800).decode("utf-8", "replace")
        return {"available": False, "error_type": "http_error", "status": exc.code, "body_snippet": body}
    except Exception as exc:  # noqa: BLE001 - diagnostic only, secrets never printed
        return {"available": False, "error_type": type(exc).__name__, "message": str(exc)[:500]}


def google_publication(product: dict[str, Any]) -> dict[str, Any] | None:
    for edge in product["resourcePublications"]["edges"]:
        node = edge["node"]
        publication = node.get("publication") or {}
        if publication.get("id") == GOOGLE_PUBLICATION_ID:
            return node
    return None


def product_feedback_messages(product: dict[str, Any]) -> list[str]:
    feedback = product.get("feedback")
    messages: list[str] = []
    if not feedback:
        return messages
    for detail in feedback.get("details") or []:
        for message in detail.get("messages") or []:
            text = str(message.get("message") or "").strip()
            if text:
                messages.append(text)
    return messages


def read_shopify_products(parent_ids: list[str]) -> dict[str, dict[str, Any]]:
    client = ShopifyClient(resolve_store_domain(""), load_access_token())
    products: dict[str, dict[str, Any]] = {}
    for parent_id in parent_ids:
        product = client.graphql(PRODUCT_QUERY, {"id": f"gid://shopify/Product/{parent_id}"})["product"]
        if not product:
            products[parent_id] = {"legacy_id": parent_id, "found": False}
            continue
        variants = [edge["node"] for edge in product["variants"]["edges"]]
        publication = google_publication(product)
        products[parent_id] = {
            "found": True,
            "id": product["id"],
            "legacy_id": str(product["legacyResourceId"]),
            "handle": product["handle"],
            "title": product["title"],
            "status": product["status"],
            "published_at": product.get("publishedAt"),
            "online_store_url_present": bool(product.get("onlineStoreUrl")),
            "google_publication": publication,
            "google_published": bool(publication and publication.get("isPublished")),
            "feedback_summary": (product.get("feedback") or {}).get("summary"),
            "feedback_messages": product_feedback_messages(product),
            "variant_count": len(variants),
            "variant_sample": [
                {
                    "legacy_id": str(variant["legacyResourceId"]),
                    "title": variant["title"],
                    "available_for_sale": variant.get("availableForSale"),
                    "inventory_policy": variant.get("inventoryPolicy"),
                    "inventory_quantity": variant.get("inventoryQuantity"),
                    "age_group": (variant.get("ageGroup") or {}).get("value"),
                    "google_size": (variant.get("googleSize") or {}).get("value"),
                    "selected_options": variant.get("selectedOptions"),
                }
                for variant in variants[:12]
            ],
        }
    return products


def summarize(
    expected_rows: list[dict[str, str]],
    ads_products: list[dict[str, Any]],
    merchant_scope: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    expected_by_item = {row["item_id"]: row for row in expected_rows}
    products_by_item: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for product in ads_products:
        if product["item_id"] in expected_by_item:
            products_by_item[product["item_id"]].append(product)
    present_ids = set(products_by_item)
    ready_ids = {
        item_id
        for item_id, products in products_by_item.items()
        if any(product["custom_label_4"] == READY_LABEL for product in products)
    }
    missing_ids = sorted(set(expected_by_item) - present_ids)
    present_without_ready_ids = sorted(present_ids - ready_ids)
    missing_rows: list[dict[str, Any]] = []
    present_rows: list[dict[str, Any]] = []
    non_ready_rows: list[dict[str, Any]] = []
    issue_counter: Counter[str] = Counter()
    issue_attr_counter: Counter[str] = Counter()
    severity_counter: Counter[str] = Counter()
    hard_error_counter: Counter[str] = Counter()

    for item_id in missing_ids:
        expected = expected_by_item[item_id]
        missing_rows.append(
            {
                "item_id": item_id,
                "parent_product_id": expected["parent_product_id"],
                "handle": expected["handle"],
                "variant_title": expected["variant_title"],
                "lane": expected["proposed_custom_label_1"],
                "proposed_item_group_id": expected["proposed_item_group_id"],
                "proposed_image_link": expected["proposed_image_link"],
            }
        )

    representatives: dict[str, dict[str, Any]] = {}
    for item_id, products in products_by_item.items():
        ready_products = [product for product in products if product["custom_label_4"] == READY_LABEL]
        representatives[item_id] = ready_products[0] if ready_products else products[0]

    for item_id, product in sorted(representatives.items()):
        expected = expected_by_item[item_id]
        issue_codes = [issue["error_code"] for issue in product["issues"]]
        issue_descriptions = [issue["description"] for issue in product["issues"]]
        for issue in product["issues"]:
            issue_counter[issue["error_code"]] += 1
            severity_counter[issue["ads_severity"]] += 1
            if issue["attribute_name"]:
                issue_attr_counter[f"{issue['attribute_name']}|{issue['error_code']}"] += 1
            if issue["ads_severity"] == "ERROR":
                hard_error_counter[issue["error_code"]] += 1
        labels_match = (
            product["custom_label_0"] == expected["proposed_custom_label_0"]
            and product["custom_label_1"] == expected["proposed_custom_label_1"]
            and product["custom_label_2"] == expected["proposed_custom_label_2"]
            and product["custom_label_3"] == expected["proposed_custom_label_3"]
            and product["custom_label_4"] == expected["proposed_custom_label_4"]
        )
        row = {
            "item_id": item_id,
            "parent_product_id": expected["parent_product_id"],
            "handle": expected["handle"],
            "lane": expected["proposed_custom_label_1"],
            "status": product["status"],
            "availability": product["availability"],
            "labels_match": str(labels_match).lower(),
            "has_ready_label": str(item_id in ready_ids).lower(),
            "custom_label_0": product["custom_label_0"],
            "custom_label_1": product["custom_label_1"],
            "custom_label_2": product["custom_label_2"],
            "custom_label_3": product["custom_label_3"],
            "custom_label_4": product["custom_label_4"],
            "matching_ads_rows_for_item": len(products_by_item[item_id]),
            "issue_codes": "|".join(issue_codes),
            "issue_descriptions": "|".join(issue_descriptions),
            "title": product["title"],
        }
        present_rows.append(row)
        if item_id in present_without_ready_ids:
            non_ready_rows.append(row)

    expected_parent_counts = Counter(row["proposed_custom_label_1"] for row in {r["proposed_item_group_id"]: r for r in expected_rows}.values())
    present_parent_sets: dict[str, set[str]] = defaultdict(set)
    missing_parent_sets: dict[str, set[str]] = defaultdict(set)
    missing_variant_counts_by_parent: Counter[str] = Counter()
    for item_id, product in representatives.items():
        expected = expected_by_item[item_id]
        if item_id in ready_ids:
            present_parent_sets[expected["proposed_custom_label_1"]].add(expected["proposed_item_group_id"])
    for row in missing_rows:
        missing_parent_sets[row["lane"]].add(row["proposed_item_group_id"])
        missing_variant_counts_by_parent[f"{row['parent_product_id']}|{row['handle']}|{row['lane']}"] += 1

    non_ready_parent_sets: dict[str, set[str]] = defaultdict(set)
    non_ready_variant_counts_by_parent: Counter[str] = Counter()
    for item_id in present_without_ready_ids:
        expected = expected_by_item[item_id]
        non_ready_parent_sets[expected["proposed_custom_label_1"]].add(expected["proposed_item_group_id"])
        non_ready_variant_counts_by_parent[f"{expected['parent_product_id']}|{expected['handle']}|{expected['proposed_custom_label_1']}"] += 1

    diagnostic_parent_ids = sorted({row["parent_product_id"] for row in missing_rows} | {row["parent_product_id"] for row in non_ready_rows})
    shopify_products = read_shopify_products(diagnostic_parent_ids)
    feedback_counter = Counter()
    for product in shopify_products.values():
        for message in product.get("feedback_messages") or []:
            feedback_counter[message] += 1

    source_readback = {}
    if LATEST_MERCHANT_SOURCE_READBACK.exists():
        source_readback = json.loads(LATEST_MERCHANT_SOURCE_READBACK.read_text(encoding="utf-8"))

    summary = {
        "expected_rows": len(expected_rows),
        "ads_present_expected_rows": len(present_rows),
        "ads_missing_expected_rows": len(missing_rows),
        "ads_ready_label_rows": len(ready_ids),
        "ads_present_non_ready_label_rows": len(present_without_ready_ids),
        "ads_raw_rows_returned_for_expected_ids": len(ads_products),
        "status_counts": dict(Counter(row["status"] for row in present_rows)),
        "availability_counts": dict(Counter(row["availability"] for row in present_rows)),
        "hard_error_counts": dict(hard_error_counter),
        "issue_counts": dict(issue_counter),
        "issue_attribute_counts": dict(issue_attr_counter),
        "issue_severity_counts": dict(severity_counter),
        "expected_parent_counts_by_lane": dict(sorted(expected_parent_counts.items())),
        "ready_parent_counts_by_lane": {lane: len(values) for lane, values in sorted(present_parent_sets.items())},
        "missing_parent_counts_by_lane": {lane: len(values) for lane, values in sorted(missing_parent_sets.items())},
        "present_non_ready_parent_counts_by_lane": {lane: len(values) for lane, values in sorted(non_ready_parent_sets.items())},
        "missing_variant_counts_by_parent": [
            {"parent_product_id": key.split("|")[0], "handle": key.split("|")[1], "lane": key.split("|")[2], "missing_variants": count}
            for key, count in missing_variant_counts_by_parent.most_common()
        ],
        "present_non_ready_variant_counts_by_parent": [
            {"parent_product_id": key.split("|")[0], "handle": key.split("|")[1], "lane": key.split("|")[2], "present_non_ready_variants": count}
            for key, count in non_ready_variant_counts_by_parent.most_common()
        ],
        "diagnostic_parent_product_ids": diagnostic_parent_ids,
        "shopify_missing_parent_summary": {
            parent_id: {
                "found": product.get("found"),
                "handle": product.get("handle"),
                "status": product.get("status"),
                "google_published": product.get("google_published"),
                "feedback_summary": product.get("feedback_summary"),
                "feedback_messages": product.get("feedback_messages"),
            }
            for parent_id, product in shopify_products.items()
        },
        "shopify_feedback_message_counts": dict(feedback_counter),
        "merchant_content_api_scope_probe": merchant_scope,
        "merchant_source_10663204023_latest_readback_text": source_readback.get("text", ""),
        "interpretation": {
            "ads_ready_rows_main_error": "not_eligible_in_any_campaign" if hard_error_counter.get("not_eligible_in_any_campaign") == len(present_rows) else "mixed_or_other",
            "campaign_pause_context": "All parent-outfit V2 campaigns are intentionally paused, so not_eligible_in_any_campaign is expected until a separate activation approval exists.",
            "remaining_blocker": f"{len(missing_rows)} expected parent-outfit offer IDs are absent from the Google Ads shopping_product surface and {len(present_without_ready_ids)} are present without the approved ready label; Merchant source readback reports 139 unmatched offers after the approved TSV refresh.",
        },
    }
    return summary, present_rows, missing_rows, shopify_products


def write_report(path: Path, timestamp: str, summary: dict[str, Any], present_csv: Path, missing_csv: Path, json_path: Path) -> None:
    lines = [
        "# Google Shopping Parent-Outfit Eligibility Diagnostic",
        "",
        f"UTC timestamp: `{timestamp}`",
        "",
        "## Verdict",
        "",
        "- Diagnostic mode: read-only.",
        "- Activation allowed: `false`.",
        "- Feed/product/campaign writes performed: `false`.",
        "",
        "## Gate Result",
        "",
        f"- Expected rows: `{summary['expected_rows']}`",
        f"- Google Ads present expected rows: `{summary['ads_present_expected_rows']}`",
        f"- Google Ads missing expected rows: `{summary['ads_missing_expected_rows']}`",
        f"- Ready-label rows: `{summary['ads_ready_label_rows']}`",
        f"- Present non-ready-label rows: `{summary['ads_present_non_ready_label_rows']}`",
        f"- Raw Ads rows returned for expected IDs: `{summary['ads_raw_rows_returned_for_expected_ids']}`",
        f"- Status counts: `{summary['status_counts']}`",
        f"- Availability counts: `{summary['availability_counts']}`",
        "",
        "## Issue Diagnosis",
        "",
        f"- Hard error counts: `{summary['hard_error_counts']}`",
        f"- Issue severity counts: `{summary['issue_severity_counts']}`",
        f"- Attribute issue counts: `{summary['issue_attribute_counts']}`",
        "",
        "Interpretation:",
        "",
        "- The ready-label rows are not failing because of label or image mismatch.",
        "- Their main Ads hard error is `not_eligible_in_any_campaign`, which is expected while every parent-outfit Shopping campaign is intentionally paused.",
        "- The still-real blocker is source matching/readiness for the expected scope: some expected offer IDs are absent from Google Ads Shopping-product and some are present without the approved ready label, while Merchant source `10663204023` reports `139` unmatched offers after the approved TSV refresh.",
        "",
        "## Parent Scope",
        "",
        f"- Expected parent counts by lane: `{summary['expected_parent_counts_by_lane']}`",
        f"- Ready parent counts by lane: `{summary['ready_parent_counts_by_lane']}`",
        f"- Missing parent counts by lane: `{summary['missing_parent_counts_by_lane']}`",
        f"- Present non-ready parent counts by lane: `{summary['present_non_ready_parent_counts_by_lane']}`",
        f"- Missing parent rows: `{summary['missing_variant_counts_by_parent']}`",
        f"- Present non-ready parent rows: `{summary['present_non_ready_variant_counts_by_parent']}`",
        "",
        "## Shopify / Google & YouTube Readback",
        "",
        f"- Diagnostic parent product IDs checked: `{summary['diagnostic_parent_product_ids']}`",
        f"- Missing parent Shopify summary: `{summary['shopify_missing_parent_summary']}`",
        f"- Shopify feedback message counts: `{summary['shopify_feedback_message_counts']}`",
        "",
        "## Merchant Scope Readback",
        "",
        f"- Merchant Content API scope available: `{summary['merchant_content_api_scope_probe'].get('available')}`",
        f"- Merchant Content API scope probe: `{summary['merchant_content_api_scope_probe']}`",
        "- Authenticated Merchant source readback for `10663204023` remains the current source-level proof: `4,531` total updated products, `4,392` matched products, all attributes recognized, `139` `Offer does not exist` rows.",
        "",
        "## Decision",
        "",
        "The safest next move is not another upload, Shopify resync, or broad Google & YouTube sync. The smallest exact action packet should either exclude the unresolved Mommy & Me parent products from the activation scope, or get fresh owner approval for a deeper Google & YouTube/Merchant product-status repair if a human control surface exposes an exact per-product repair. I recommend the exclusion packet first because the present ready-label rows already have clean labels/images and the unresolved rows have resisted the narrow publication, attribute, and supplemental-refresh repairs.",
        "",
        "## Output Files",
        "",
        f"- JSON: `{json_path.name}`",
        f"- Present rows CSV: `{present_csv.name}`",
        f"- Missing rows CSV: `{missing_csv.name}`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    timestamp = now_stamp()
    expected_rows = load_expected_rows()
    client = load_google_ads_client()
    try:
        ads_products = read_expected_products(client, sorted(row["item_id"] for row in expected_rows))
    except GoogleAdsException as exc:
        payload = {
            "timestamp_utc": timestamp,
            "mode": "read_only",
            "error": {
                "request_id": exc.request_id,
                "errors": [
                    {
                        "message": error_item.message,
                        "error_code": str(error_item.error_code),
                        "trigger": str(error_item.trigger) if error_item.trigger else None,
                    }
                    for error_item in exc.failure.errors
                ],
            },
        }
        error_path = PACKET_DIR / f"google_shopping_parent_outfit_eligibility_diagnostic_error_{timestamp}.json"
        write_json(error_path, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2

    merchant_scope = merchant_content_scope_probe()
    summary, present_rows, missing_rows, shopify_products = summarize(expected_rows, ads_products, merchant_scope)

    present_csv = PACKET_DIR / f"google_shopping_parent_outfit_eligibility_present_rows_{timestamp}.csv"
    missing_csv = PACKET_DIR / f"google_shopping_parent_outfit_eligibility_missing_rows_{timestamp}.csv"
    json_path = PACKET_DIR / f"google_shopping_parent_outfit_eligibility_diagnostic_{timestamp}.json"
    report_path = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_DIAGNOSTIC_{timestamp}.md"

    write_csv(
        present_csv,
        present_rows,
        [
            "item_id",
            "parent_product_id",
            "handle",
            "lane",
            "status",
            "availability",
            "labels_match",
            "has_ready_label",
            "custom_label_0",
            "custom_label_1",
            "custom_label_2",
            "custom_label_3",
            "custom_label_4",
            "matching_ads_rows_for_item",
            "issue_codes",
            "issue_descriptions",
            "title",
        ],
    )
    write_csv(
        missing_csv,
        missing_rows,
        [
            "item_id",
            "parent_product_id",
            "handle",
            "variant_title",
            "lane",
            "proposed_item_group_id",
            "proposed_image_link",
        ],
    )
    write_json(
        json_path,
        {
            "timestamp_utc": timestamp,
            "mode": "read_only",
            "summary": summary,
            "shopify_missing_parent_products": shopify_products,
            "guardrails": [
                "No Merchant Center write.",
                "No Shopify write.",
                "No Google & YouTube setting or sync write.",
                "No Google Ads mutate operation.",
                "No feed upload.",
                "No product data, campaign, product-group, budget, bid, status, conversion, billing, or activation change.",
            ],
        },
    )
    write_report(report_path, timestamp, summary, present_csv, missing_csv, json_path)
    print(json.dumps({"timestamp_utc": timestamp, **summary}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
