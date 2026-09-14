#!/usr/bin/env python3
"""Read-only Merchant/feed gate for paused Google Shopping parent-outfit V2.

This script does not mutate Google Ads, Merchant Center, Shopify, feeds,
products, budgets, bids, statuses, conversions, or billing. It reads:
- current Google Ads campaign/listing-group state for the paused V2 structures
- current Shopping product attributes exposed through Google Ads API
- whether the stricter Merchant Content API readback scope is available

The gate fails closed unless live product rows prove the parent-outfit label and
hero-image contract.
"""

from __future__ import annotations

import csv
import json
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import google.auth.transport.requests
import yaml
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.oauth2.credentials import Credentials


PACKET_DIR = Path(__file__).resolve().parent
CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
CUSTOMER_ID = "3990976848"
MERCHANT_ID = 124884876
FEED_LABEL = "US"
READY_LABEL = "us_parent_outfit_ready_v20260520"
OLD_TEST_CAMPAIGN = "DLM_US_STANDARD_SHOPPING_TEST_PAID_READY"
V2_CAMPAIGNS = [
    "DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2",
    "DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2",
    "DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2",
]
ALL_CAMPAIGNS = V2_CAMPAIGNS + [OLD_TEST_CAMPAIGN]
MERCHANT_SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
SUMMARY_JSON = PACKET_DIR / "google_shopping_parent_outfit_rebuild_summary.json"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def quote_sql(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def campaign_names_filter(names: list[str]) -> str:
    return ", ".join(f"'{quote_sql(name)}'" for name in names)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_client() -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(str(CONFIG_PATH))


def search_rows(client: GoogleAdsClient, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=CUSTOMER_ID, query=query))


def google_ads_error(exc: GoogleAdsException) -> dict[str, Any]:
    return {
        "request_id": exc.request_id,
        "errors": [
            {
                "message": error.message,
                "error_code": str(error.error_code),
                "trigger": str(error.trigger) if error.trigger else None,
            }
            for error in exc.failure.errors
        ],
    }


def read_campaigns(client: GoogleAdsClient) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.primary_status,
          campaign.advertising_channel_type,
          campaign.bidding_strategy_type,
          campaign.shopping_setting.merchant_id,
          campaign.shopping_setting.feed_label,
          campaign.shopping_setting.campaign_priority,
          campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.name IN ({campaign_names_filter(ALL_CAMPAIGNS)})
        ORDER BY campaign.name
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, query):
        rows.append(
            {
                "id": row.campaign.id,
                "name": row.campaign.name,
                "status": enum_name(row.campaign.status),
                "primary_status": enum_name(row.campaign.primary_status),
                "advertising_channel_type": enum_name(row.campaign.advertising_channel_type),
                "bidding_strategy_type": enum_name(row.campaign.bidding_strategy_type),
                "merchant_id": row.campaign.shopping_setting.merchant_id,
                "feed_label": row.campaign.shopping_setting.feed_label,
                "campaign_priority": row.campaign.shopping_setting.campaign_priority,
                "budget_amount_micros": row.campaign_budget.amount_micros,
            }
        )
    return rows


def read_listing_groups(client: GoogleAdsClient) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.name,
          ad_group_criterion.status,
          ad_group_criterion.negative,
          ad_group_criterion.listing_group.type,
          ad_group_criterion.listing_group.case_value.product_custom_attribute.index,
          ad_group_criterion.listing_group.case_value.product_custom_attribute.value
        FROM ad_group_criterion
        WHERE campaign.name IN ({campaign_names_filter(V2_CAMPAIGNS)})
          AND ad_group_criterion.type = LISTING_GROUP
        ORDER BY campaign.name, ad_group.name
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, query):
        criterion = row.ad_group_criterion
        attr = criterion.listing_group.case_value.product_custom_attribute
        rows.append(
            {
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "status": enum_name(criterion.status),
                "negative": criterion.negative,
                "listing_group_type": enum_name(criterion.listing_group.type_),
                "case_index": enum_name(attr.index),
                "case_value": attr.value,
            }
        )
    return rows


def shopping_product_query(where_clause: str) -> str:
    return f"""
        SELECT
          shopping_product.item_id,
          shopping_product.title,
          shopping_product.status,
          shopping_product.availability,
          shopping_product.feed_label,
          shopping_product.merchant_center_id,
          shopping_product.custom_attribute0,
          shopping_product.custom_attribute1,
          shopping_product.custom_attribute2,
          shopping_product.custom_attribute3,
          shopping_product.custom_attribute4,
          shopping_product.product_image_uri
        FROM shopping_product
        WHERE shopping_product.merchant_center_id = {MERCHANT_ID}
          AND shopping_product.feed_label = '{FEED_LABEL}'
          {where_clause}
        ORDER BY shopping_product.item_id
    """


def read_products(client: GoogleAdsClient, where_clause: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, shopping_product_query(where_clause)):
        product = row.shopping_product
        rows.append(
            {
                "item_id": product.item_id,
                "title": product.title,
                "status": enum_name(product.status),
                "availability": enum_name(product.availability),
                "feed_label": product.feed_label,
                "merchant_center_id": product.merchant_center_id,
                "custom_label_0": product.custom_attribute0,
                "custom_label_1": product.custom_attribute1,
                "custom_label_2": product.custom_attribute2,
                "custom_label_3": product.custom_attribute3,
                "custom_label_4": product.custom_attribute4,
                "product_image_uri": product.product_image_uri,
            }
        )
    return rows


def label_tuple(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        row.get("custom_label_0", ""),
        row.get("custom_label_1", ""),
        row.get("custom_label_2", ""),
        row.get("custom_label_3", ""),
        row.get("custom_label_4", ""),
    )


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
        req = urllib.request.Request(
            f"https://shoppingcontent.googleapis.com/content/v2.1/{MERCHANT_ID}/products?maxResults=1",
            headers={"Authorization": f"Bearer {creds.token}"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return {"available": True, "status": response.status}
    except urllib.error.HTTPError as exc:
        body = exc.read(800).decode("utf-8", "replace")
        return {"available": False, "error_type": "http_error", "status": exc.code, "body_snippet": body}
    except Exception as exc:  # noqa: BLE001 - diagnostic only, secrets never printed
        return {"available": False, "error_type": type(exc).__name__, "message": str(exc)[:500]}


def summarize_gate(
    spec_rows: list[dict[str, str]],
    campaigns: list[dict[str, Any]],
    listing_groups: list[dict[str, Any]],
    ready_products: list[dict[str, Any]],
    old_products: list[dict[str, Any]],
    merchant_scope: dict[str, Any],
) -> dict[str, Any]:
    include_rows = [row for row in spec_rows if row["decision"] == "INCLUDE"]
    expected_by_item = {row["item_id"]: row for row in include_rows}
    expected_parent_counts = Counter(row["proposed_custom_label_1"] for row in {r["proposed_item_group_id"]: r for r in include_rows}.values())

    ready_by_item = {row["item_id"]: row for row in ready_products}
    matching_ready_ids = set(expected_by_item) & set(ready_by_item)
    unexpected_ready_ids = set(ready_by_item) - set(expected_by_item)
    missing_expected_ids = set(expected_by_item) - set(ready_by_item)

    label_mismatches: list[dict[str, Any]] = []
    image_mismatches: list[dict[str, Any]] = []
    missing_images: list[str] = []
    ready_parent_counts: dict[str, set[str]] = defaultdict(set)

    for item_id in matching_ready_ids:
        expected = expected_by_item[item_id]
        live = ready_by_item[item_id]
        expected_labels = (
            expected["proposed_custom_label_0"],
            expected["proposed_custom_label_1"],
            expected["proposed_custom_label_2"],
            expected["proposed_custom_label_3"],
            expected["proposed_custom_label_4"],
        )
        if label_tuple(live) != expected_labels:
            label_mismatches.append(
                {
                    "item_id": item_id,
                    "expected": expected_labels,
                    "live": label_tuple(live),
                }
            )
        if not live["product_image_uri"]:
            missing_images.append(item_id)
        elif live["product_image_uri"] != expected["proposed_image_link"]:
            image_mismatches.append(
                {
                    "item_id": item_id,
                    "expected_image": expected["proposed_image_link"],
                    "live_image": live["product_image_uri"],
                }
            )
        ready_parent_counts[expected["proposed_custom_label_1"]].add(expected["proposed_item_group_id"])

    campaign_status_ok = all(
        row["name"] == OLD_TEST_CAMPAIGN or (row["name"] in V2_CAMPAIGNS and row["status"] == "PAUSED" and row["primary_status"] == "PAUSED")
        for row in campaigns
    ) and {row["name"] for row in campaigns} == set(ALL_CAMPAIGNS)
    old_campaign_paused = any(
        row["name"] == OLD_TEST_CAMPAIGN and row["status"] == "PAUSED" and row["primary_status"] == "PAUSED"
        for row in campaigns
    )

    # Google Ads represents "Everything else" listing-group units as an empty
    # case value under the active subdivision dimension. In this tree, every
    # empty UNIT must be negative/excluded.
    bad_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["negative"] and row["case_value"] == ""
    ]
    excluded_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and row["negative"] and row["case_value"] == ""
    ]
    included_units = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["negative"] and row["case_value"] != "Everything else"
    ]

    old_matching_expected = set(row["item_id"] for row in old_products) & set(expected_by_item)
    old_label_counts = Counter(label_tuple(row) for row in old_products)

    expected_counts_clean = dict(sorted(expected_parent_counts.items()))
    live_parent_counts = {lane: len(values) for lane, values in sorted(ready_parent_counts.items())}
    strict_live_product_pass = (
        len(ready_products) == len(include_rows)
        and len(missing_expected_ids) == 0
        and len(unexpected_ready_ids) == 0
        and not label_mismatches
        and not image_mismatches
        and not missing_images
        and live_parent_counts == expected_counts_clean
    )
    gate_passed = bool(campaign_status_ok and old_campaign_paused and not bad_catchalls and strict_live_product_pass)

    return {
        "gate_passed": gate_passed,
        "activation_discussion_allowed": False,
        "reason": "PASS" if gate_passed else "FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE",
        "campaign_status_ok": campaign_status_ok,
        "old_campaign_paused": old_campaign_paused,
        "campaigns": campaigns,
        "listing_group_summary": {
            "total": len(listing_groups),
            "included_units": len(included_units),
            "excluded_catchall_units": len(excluded_catchalls),
            "bad_catchall_units": len(bad_catchalls),
        },
        "expected_spec": {
            "included_variant_rows": len(include_rows),
            "expected_parent_counts_by_lane": expected_counts_clean,
            "missing_item_group_id_in_spec": sum(1 for row in include_rows if not row["proposed_item_group_id"]),
            "missing_hero_image_in_spec": sum(1 for row in include_rows if not row["proposed_image_link"]),
        },
        "live_ready_products": {
            "rows_with_ready_label": len(ready_products),
            "matching_expected_rows": len(matching_ready_ids),
            "missing_expected_rows": len(missing_expected_ids),
            "unexpected_ready_rows": len(unexpected_ready_ids),
            "live_parent_counts_by_lane_from_spec_join": live_parent_counts,
            "label_mismatches": len(label_mismatches),
            "image_mismatches": len(image_mismatches),
            "missing_live_images": len(missing_images),
            "sample_ready_products": ready_products[:10],
            "sample_label_mismatches": label_mismatches[:10],
            "sample_image_mismatches": image_mismatches[:10],
        },
        "old_test_ready_context": {
            "rows_with_paid_eligible_us_test_ready": len(old_products),
            "old_rows_matching_new_expected_item_ids": len(old_matching_expected),
            "label_tuple_counts": [
                {"labels": list(labels), "rows": count}
                for labels, count in old_label_counts.most_common(20)
            ],
            "sample_old_products": old_products[:10],
        },
        "item_group_id_readback": {
            "google_ads_shopping_product_field_available": False,
            "merchant_content_api_scope_probe": merchant_scope,
            "live_item_group_id_proven": False,
            "note": "Google Ads shopping_product exposes labels and product_image_uri but not item_group_id; Merchant Content API scope is required for strict live item_group_id proof.",
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if rows:
        fieldnames = list(rows[0].keys())
    else:
        fieldnames = [
            "item_id",
            "title",
            "status",
            "availability",
            "feed_label",
            "merchant_center_id",
            "custom_label_0",
            "custom_label_1",
            "custom_label_2",
            "custom_label_3",
            "custom_label_4",
            "product_image_uri",
        ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, payload: dict[str, Any], timestamp: str) -> None:
    live = payload["live_ready_products"]
    expected = payload["expected_spec"]
    listing = payload["listing_group_summary"]
    item_group = payload["item_group_id_readback"]
    lines = [
        "# Google Shopping Parent-Outfit Merchant / Feed Gate Readback",
        "",
        f"UTC timestamp: `{timestamp}`",
        "",
        "## Verdict",
        "",
        f"- Gate passed: `{payload['gate_passed']}`",
        f"- Reason: `{payload['reason']}`",
        f"- Activation discussion allowed: `{payload['activation_discussion_allowed']}`",
        "",
        "## Ads Structure Safety Readback",
        "",
        f"- Campaign status ok: `{payload['campaign_status_ok']}`",
        f"- Old test campaign paused: `{payload['old_campaign_paused']}`",
        f"- Listing groups: `{listing['total']}`",
        f"- Included subgroup units: `{listing['included_units']}`",
        f"- Excluded catchall units: `{listing['excluded_catchall_units']}`",
        f"- Bad catchall units: `{listing['bad_catchall_units']}`",
        "",
        "## Live Product / Image Readback",
        "",
        f"- Expected included variant rows: `{expected['included_variant_rows']}`",
        f"- Expected parent counts by lane: `{expected['expected_parent_counts_by_lane']}`",
        f"- Live rows with `custom_label_4={READY_LABEL}`: `{live['rows_with_ready_label']}`",
        f"- Live rows matching expected item IDs: `{live['matching_expected_rows']}`",
        f"- Missing expected rows: `{live['missing_expected_rows']}`",
        f"- Unexpected ready-label rows: `{live['unexpected_ready_rows']}`",
        f"- Live parent counts by lane from spec join: `{live['live_parent_counts_by_lane_from_spec_join']}`",
        f"- Label mismatches: `{live['label_mismatches']}`",
        f"- Image mismatches: `{live['image_mismatches']}`",
        f"- Missing live images: `{live['missing_live_images']}`",
        "",
        "## Item Group Proof",
        "",
        f"- Google Ads `shopping_product` item_group_id field available: `{item_group['google_ads_shopping_product_field_available']}`",
        f"- Merchant Content API scope available: `{item_group['merchant_content_api_scope_probe'].get('available')}`",
        f"- Live item_group_id proven: `{item_group['live_item_group_id_proven']}`",
        f"- Note: {item_group['note']}",
        "",
        "## Existing Old-Label Context",
        "",
        f"- Rows with old `paid_eligible` + `us_test_ready`: `{payload['old_test_ready_context']['rows_with_paid_eligible_us_test_ready']}`",
        f"- Old-label rows matching the new expected item IDs: `{payload['old_test_ready_context']['old_rows_matching_new_expected_item_ids']}`",
        "",
        "## Conclusion",
        "",
        "The paused V2 campaign shells remain safe, but the Merchant/feed product gate fails closed because the new parent-outfit readiness label is not live on Shopping products. Do not activate or discuss activation until a separate feed/Merchant update and after-state readback proves the expected parent counts, hero images, and item grouping live.",
        "",
        "## Output Files",
        "",
        f"- JSON: `google_shopping_parent_outfit_merchant_feed_gate_{timestamp}.json`",
        f"- Ready products CSV: `google_shopping_parent_outfit_ready_products_{timestamp}.csv`",
        f"- Old-label context CSV: `google_shopping_parent_outfit_old_us_test_ready_products_{timestamp}.csv`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    timestamp = now_stamp()
    spec_rows = load_csv(MERCHANT_SPEC_CSV)
    client = load_client()

    try:
        campaigns = read_campaigns(client)
        listing_groups = read_listing_groups(client)
        ready_products = read_products(
            client,
            f"AND shopping_product.custom_attribute4 = '{READY_LABEL}'",
        )
        old_products = read_products(
            client,
            "AND shopping_product.custom_attribute0 = 'paid_eligible' "
            "AND shopping_product.custom_attribute4 = 'us_test_ready'",
        )
    except GoogleAdsException as exc:
        payload = {
            "timestamp_utc": timestamp,
            "gate_passed": False,
            "reason": "FAIL_CLOSED__GOOGLE_ADS_READBACK_ERROR",
            "google_ads_error": google_ads_error(exc),
        }
        write_json(PACKET_DIR / f"google_shopping_parent_outfit_merchant_feed_gate_{timestamp}.json", payload)
        return 2

    merchant_scope = merchant_content_scope_probe()
    payload = summarize_gate(spec_rows, campaigns, listing_groups, ready_products, old_products, merchant_scope)
    payload["timestamp_utc"] = timestamp
    payload["guardrails"] = [
        "Read-only Google Ads Shopping product readback.",
        "No Google Ads mutate operations.",
        "No Merchant Center write.",
        "No Shopify write.",
        "No feed upload or product data write.",
        "No budget, bid, status, conversion, billing, or activation change.",
    ]

    write_json(PACKET_DIR / f"google_shopping_parent_outfit_merchant_feed_gate_{timestamp}.json", payload)
    write_csv(PACKET_DIR / f"google_shopping_parent_outfit_ready_products_{timestamp}.csv", ready_products)
    write_csv(PACKET_DIR / f"google_shopping_parent_outfit_old_us_test_ready_products_{timestamp}.csv", old_products)
    write_report(
        PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_{timestamp}.md",
        payload,
        timestamp,
    )

    print(json.dumps({
        "timestamp_utc": timestamp,
        "gate_passed": payload["gate_passed"],
        "reason": payload["reason"],
        "campaign_status_ok": payload["campaign_status_ok"],
        "old_campaign_paused": payload["old_campaign_paused"],
        "ready_rows": payload["live_ready_products"]["rows_with_ready_label"],
        "expected_rows": payload["expected_spec"]["included_variant_rows"],
        "bad_catchall_units": payload["listing_group_summary"]["bad_catchall_units"],
        "merchant_content_api_available": merchant_scope.get("available"),
    }, indent=2, sort_keys=True))
    return 0 if payload["gate_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
