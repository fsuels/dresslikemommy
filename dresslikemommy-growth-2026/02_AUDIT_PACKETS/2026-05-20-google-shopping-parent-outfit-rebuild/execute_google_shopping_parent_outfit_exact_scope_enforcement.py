#!/usr/bin/env python3
"""Enforce the reduced parent-outfit Shopping scope with exact item-ID units.

This script keeps the already-built V2 Shopping campaigns paused. It replaces
each included subgroup UNIT with a subgroup SUBDIVISION, then adds exact
product_item_id UNIT children for the reduced candidate rows and an excluded
item catchall below each subgroup. This prevents held rows with the same
parent/subgroup labels from entering delivery later.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.api_core import exceptions as google_api_exceptions
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


PACKET_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
CUSTOMER_ID = "3990976848"
OLD_CAMPAIGN_NAME = "DLM_US_STANDARD_SHOPPING_TEST_PAID_READY"
READY_LABEL = "us_parent_outfit_ready_v20260520"
APPROVAL_PHRASE = (
    "Build paused exact-scope Google Shopping product-group enforcement only: "
    "keep all V2 Shopping campaigns and DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused, "
    "validate-only first, then if validation passes replace only the V2 included subgroup "
    "units with exact product_item_id subdivisions for the 4370 reduced-scope candidate "
    "rows from GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_20260521T132011Z.md, "
    "exclude item-level catchalls, preserve budgets/bids/statuses/conversions/billing, "
    "do not change Merchant/Shopify/Google & YouTube/feed/source/product data, and read back "
    "that included item units equal the candidate IDs with zero held IDs before any activation."
)

CAMPAIGN_NAMES = [
    "DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2",
    "DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2",
    "DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2",
]
LANE_TO_CAMPAIGN = {
    "daddy_and_me": "DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2",
    "family_matching": "DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2",
    "mommy_and_me": "DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2",
}
AD_GROUP_BY_LANE_SUBGROUP = {
    ("daddy_and_me", "sets"): "Daddy & Me - Sets",
    ("daddy_and_me", "tops_shirts"): "Daddy & Me - Tops & Shirts",
    ("family_matching", "dresses"): "Family Matching - Dresses",
    ("family_matching", "sets"): "Family Matching - Sets",
    ("family_matching", "sweaters_outerwear"): "Family Matching - Sweaters & Outerwear",
    ("family_matching", "tops_shirts"): "Family Matching - Tops & Shirts",
    ("mommy_and_me", "dresses"): "Mommy & Me - Dresses",
    ("mommy_and_me", "pajamas"): "Mommy & Me - Pajamas",
    ("mommy_and_me", "sets"): "Mommy & Me - Sets",
    ("mommy_and_me", "sweaters_outerwear"): "Mommy & Me - Sweaters & Outerwear",
    ("mommy_and_me", "swimwear"): "Mommy & Me - Swimwear",
    ("mommy_and_me", "tops_shirts"): "Mommy & Me - Tops & Shirts",
}

CANDIDATES_CSV = PACKET_DIR / "google_shopping_parent_outfit_reduced_activation_review_candidates_20260521T132011Z.csv"
UNRESOLVED_CSV = PACKET_DIR / "google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv"
OUT_OF_STOCK_CSV = PACKET_DIR / "google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def normalize_customer_id(customer_id: str) -> str:
    return customer_id.replace("-", "").strip()


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def quote_sql(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def campaign_names_filter(names: list[str]) -> str:
    return ", ".join(f"'{quote_sql(name)}'" for name in names)


def get_client(config_path: Path) -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(str(config_path))


def google_ads_error_payload(exc: GoogleAdsException) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    for error in exc.failure.errors:
        field_path = []
        if error.location:
            for field_path_element in error.location.field_path_elements:
                field_path.append(field_path_element.field_name)
        errors.append(
            {
                "message": error.message,
                "error_code": str(error.error_code),
                "field_path": field_path,
                "trigger": str(error.trigger) if error.trigger else None,
            }
        )
    return {"request_id": exc.request_id, "failure": errors}


def generic_error_payload(exc: Exception) -> dict[str, Any]:
    return {
        "type": type(exc).__name__,
        "message": str(exc),
    }


def search_rows(client: GoogleAdsClient, customer_id: str, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=customer_id, query=query))


def criterion_id_from_resource(resource_name: str) -> int:
    return int(resource_name.rsplit("~", 1)[1])


def ad_group_id_from_resource(resource_name: str) -> int:
    return int(resource_name.rsplit("/", 1)[1].split("~", 1)[0])


def ad_group_criterion_resource(customer_id: str, ad_group_id: int, criterion_id: int) -> str:
    return f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"


def case_dimension(case_value: Any) -> dict[str, str]:
    which = case_value._pb.WhichOneof("dimension")
    if which == "product_custom_attribute":
        attr = case_value.product_custom_attribute
        return {"dimension": "product_custom_attribute", "index": enum_name(attr.index), "value": attr.value}
    if which == "product_item_id":
        return {"dimension": "product_item_id", "index": "", "value": case_value.product_item_id.value}
    return {"dimension": which or "", "index": "", "value": ""}


def readback_campaigns(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.id,
          campaign.resource_name,
          campaign.name,
          campaign.status,
          campaign.primary_status,
          campaign.advertising_channel_type,
          campaign.shopping_setting.feed_label,
          campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.name IN ({campaign_names_filter(CAMPAIGN_NAMES + [OLD_CAMPAIGN_NAME])})
        ORDER BY campaign.name
    """
    rows = []
    for row in search_rows(client, customer_id, query):
        rows.append(
            {
                "id": row.campaign.id,
                "resource_name": row.campaign.resource_name,
                "name": row.campaign.name,
                "status": enum_name(row.campaign.status),
                "primary_status": enum_name(row.campaign.primary_status),
                "advertising_channel_type": enum_name(row.campaign.advertising_channel_type),
                "feed_label": row.campaign.shopping_setting.feed_label,
                "budget_amount_micros": row.campaign_budget.amount_micros,
            }
        )
    return rows


def readback_ad_groups(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.id,
          ad_group.resource_name,
          ad_group.name,
          ad_group.status,
          ad_group.cpc_bid_micros
        FROM ad_group
        WHERE campaign.name IN ({campaign_names_filter(CAMPAIGN_NAMES)})
        ORDER BY campaign.name, ad_group.name
    """
    rows = []
    for row in search_rows(client, customer_id, query):
        rows.append(
            {
                "campaign": row.campaign.name,
                "id": row.ad_group.id,
                "resource_name": row.ad_group.resource_name,
                "name": row.ad_group.name,
                "status": enum_name(row.ad_group.status),
                "cpc_bid_micros": row.ad_group.cpc_bid_micros,
            }
        )
    return rows


def readback_product_ads(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.name,
          ad_group_ad.resource_name,
          ad_group_ad.status,
          ad_group_ad.ad.type
        FROM ad_group_ad
        WHERE campaign.name IN ({campaign_names_filter(CAMPAIGN_NAMES)})
        ORDER BY campaign.name, ad_group.name
    """
    rows = []
    for row in search_rows(client, customer_id, query):
        rows.append(
            {
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "resource_name": row.ad_group_ad.resource_name,
                "status": enum_name(row.ad_group_ad.status),
                "ad_type": enum_name(row.ad_group_ad.ad.type_),
            }
        )
    return rows


def readback_listing_groups(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.name,
          ad_group_criterion.resource_name,
          ad_group_criterion.criterion_id,
          ad_group_criterion.status,
          ad_group_criterion.negative,
          ad_group_criterion.cpc_bid_micros,
          ad_group_criterion.listing_group.type,
          ad_group_criterion.listing_group.parent_ad_group_criterion,
          ad_group_criterion.listing_group.case_value.product_custom_attribute.index,
          ad_group_criterion.listing_group.case_value.product_custom_attribute.value,
          ad_group_criterion.listing_group.case_value.product_item_id.value
        FROM ad_group_criterion
        WHERE campaign.name IN ({campaign_names_filter(CAMPAIGN_NAMES)})
          AND ad_group_criterion.type = LISTING_GROUP
        ORDER BY campaign.name, ad_group.name, ad_group_criterion.criterion_id
    """
    rows = []
    for row in search_rows(client, customer_id, query):
        criterion = row.ad_group_criterion
        listing_group = criterion.listing_group
        dim = case_dimension(listing_group.case_value)
        rows.append(
            {
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "resource_name": criterion.resource_name,
                "criterion_id": criterion.criterion_id,
                "status": enum_name(criterion.status),
                "negative": criterion.negative,
                "cpc_bid_micros": criterion.cpc_bid_micros,
                "listing_group_type": enum_name(listing_group.type_),
                "parent_ad_group_criterion": listing_group.parent_ad_group_criterion,
                "case_dimension": dim["dimension"],
                "case_index": dim["index"],
                "case_value": dim["value"],
            }
        )
    return rows


def full_readback(client: GoogleAdsClient, customer_id: str) -> dict[str, Any]:
    return {
        "campaigns": readback_campaigns(client, customer_id),
        "ad_groups": readback_ad_groups(client, customer_id),
        "product_ads": readback_product_ads(client, customer_id),
        "listing_groups": readback_listing_groups(client, customer_id),
    }


def validate_inputs(candidate_rows: list[dict[str, str]], unresolved_rows: list[dict[str, str]], out_of_stock_rows: list[dict[str, str]]) -> dict[str, Any]:
    issues = []
    candidate_ids = [row["item_id"] for row in candidate_rows]
    if len(candidate_ids) != 4370:
        issues.append(f"Expected 4370 candidate rows, found {len(candidate_ids)}")
    if len(set(candidate_ids)) != len(candidate_ids):
        issues.append("Candidate rows contain duplicate item IDs")
    held_ids = {row["item_id"] for row in unresolved_rows + out_of_stock_rows}
    overlap = sorted(set(candidate_ids) & held_ids)
    if overlap:
        issues.append(f"Candidate IDs overlap held IDs: {overlap[:5]}")
    missing_routes = sorted({(row["lane"], row["subgroup"]) for row in candidate_rows} - set(AD_GROUP_BY_LANE_SUBGROUP))
    if missing_routes:
        issues.append(f"Candidate rows have unexpected lane/subgroup routes: {missing_routes}")
    bad_labels = [
        row["item_id"]
        for row in candidate_rows
        if row["custom_label_0"] != "paid_eligible"
        or row["custom_label_1"] != row["lane"]
        or row["custom_label_2"] != row["subgroup"]
        or row["custom_label_3"] != "parent_outfit"
        or row["custom_label_4"] != READY_LABEL
        or row["availability"] != "IN_STOCK"
        or row["labels_match_spec"] != "true"
        or row["image_matches_spec"] != "true"
    ]
    if bad_labels:
        issues.append(f"Candidate rows fail label/image/in-stock checks: {bad_labels[:5]}")
    if issues:
        raise ValueError("Input validation failed:\n- " + "\n- ".join(issues))
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in candidate_rows:
        grouped[(row["lane"], row["subgroup"])].append(row["item_id"])
    return {
        "candidate_rows": len(candidate_rows),
        "candidate_unique_item_ids": len(set(candidate_ids)),
        "held_unresolved_rows": len(unresolved_rows),
        "held_out_of_stock_rows": len(out_of_stock_rows),
        "group_counts": {f"{lane}/{subgroup}": len(ids) for (lane, subgroup), ids in sorted(grouped.items())},
    }


def find_existing_tree(before: dict[str, Any], grouped_ids: dict[tuple[str, str], list[str]]) -> dict[tuple[str, str], dict[str, Any]]:
    listing_groups = before["listing_groups"]
    by_resource = {row["resource_name"]: row for row in listing_groups}
    ad_groups_by_name = {row["name"]: row for row in before["ad_groups"]}
    existing: dict[tuple[str, str], dict[str, Any]] = {}
    for key in sorted(grouped_ids):
        lane, subgroup = key
        ad_group_name = AD_GROUP_BY_LANE_SUBGROUP[key]
        ad_group = ad_groups_by_name.get(ad_group_name)
        if not ad_group:
            raise RuntimeError(f"Missing V2 ad group for {key}: {ad_group_name}")
        matching = [
            row
            for row in listing_groups
            if row["ad_group"] == ad_group_name
            and row["listing_group_type"] == "UNIT"
            and not row["negative"]
            and row["case_dimension"] == "product_custom_attribute"
            and row["case_index"] == "INDEX2"
            and row["case_value"] == subgroup
        ]
        if not matching:
            exact_existing = [
                row
                for row in listing_groups
                if row["ad_group"] == ad_group_name
                and row["case_dimension"] == "product_item_id"
                and row["case_value"] in set(grouped_ids[key])
            ]
            if exact_existing:
                continue
            raise RuntimeError(f"Missing included subgroup unit for {key}: {ad_group_name}")
        if len(matching) != 1:
            raise RuntimeError(f"Expected one included subgroup unit for {key}, found {len(matching)}")
        subgroup_unit = matching[0]
        lane_parent = by_resource.get(subgroup_unit["parent_ad_group_criterion"])
        if not lane_parent:
            raise RuntimeError(f"Missing lane parent for {key}")
        existing[key] = {"ad_group": ad_group, "subgroup_unit": subgroup_unit, "lane_parent": lane_parent}
    return existing


def set_custom_label_case(client: GoogleAdsClient, criterion: Any, index: int, value: str | None) -> None:
    criterion.listing_group.case_value.product_custom_attribute.index = getattr(client.enums.ProductCustomAttributeIndexEnum, f"INDEX{index}")
    if value is not None:
        criterion.listing_group.case_value.product_custom_attribute.value = value


def set_item_id_case(client: GoogleAdsClient, criterion: Any, item_id: str | None) -> None:
    if item_id is None:
        criterion._pb.listing_group.case_value.product_item_id.SetInParent()
    else:
        criterion.listing_group.case_value.product_item_id.value = item_id


def build_operations(
    client: GoogleAdsClient,
    customer_id: str,
    before: dict[str, Any],
    candidate_rows: list[dict[str, str]],
) -> tuple[list[Any], list[tuple[str, list[Any]]], dict[str, Any]]:
    grouped_ids: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in candidate_rows:
        grouped_ids[(row["lane"], row["subgroup"])].append(row["item_id"])
    existing = find_existing_tree(before, grouped_ids)

    operations = []
    operation_batches: list[tuple[str, list[Any]]] = []
    temp_id = -100000

    def next_id() -> int:
        nonlocal temp_id
        value = temp_id
        temp_id -= 1
        return value

    for key, item_ids in sorted(grouped_ids.items()):
        lane, subgroup = key
        batch_ops: list[Any] = []
        current = existing[key]
        subgroup_unit = current["subgroup_unit"]
        lane_parent = current["lane_parent"]
        ad_group = current["ad_group"]
        ad_group_id = ad_group["id"]
        subgroup_bid = subgroup_unit["cpc_bid_micros"] or ad_group["cpc_bid_micros"]

        remove_op = client.get_type("MutateOperation")
        remove_op.ad_group_criterion_operation.remove = subgroup_unit["resource_name"]
        operations.append(remove_op)
        batch_ops.append(remove_op)

        subgroup_subdivision_resource = ad_group_criterion_resource(customer_id, ad_group_id, next_id())
        subgroup_op = client.get_type("MutateOperation")
        subgroup_criterion = subgroup_op.ad_group_criterion_operation.create
        subgroup_criterion.resource_name = subgroup_subdivision_resource
        subgroup_criterion.ad_group = ad_group["resource_name"]
        subgroup_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        subgroup_criterion.listing_group.type_ = client.enums.ListingGroupTypeEnum.SUBDIVISION
        subgroup_criterion.listing_group.parent_ad_group_criterion = lane_parent["resource_name"]
        set_custom_label_case(client, subgroup_criterion, 2, subgroup)
        operations.append(subgroup_op)
        batch_ops.append(subgroup_op)

        for item_id in sorted(item_ids):
            item_op = client.get_type("MutateOperation")
            item_criterion = item_op.ad_group_criterion_operation.create
            item_criterion.ad_group = ad_group["resource_name"]
            item_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            item_criterion.cpc_bid_micros = subgroup_bid
            item_criterion.listing_group.type_ = client.enums.ListingGroupTypeEnum.UNIT
            item_criterion.listing_group.parent_ad_group_criterion = subgroup_subdivision_resource
            set_item_id_case(client, item_criterion, item_id)
            operations.append(item_op)
            batch_ops.append(item_op)

        item_catchall_op = client.get_type("MutateOperation")
        item_catchall = item_catchall_op.ad_group_criterion_operation.create
        item_catchall.ad_group = ad_group["resource_name"]
        item_catchall.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        item_catchall.negative = True
        item_catchall.listing_group.type_ = client.enums.ListingGroupTypeEnum.UNIT
        item_catchall.listing_group.parent_ad_group_criterion = subgroup_subdivision_resource
        set_item_id_case(client, item_catchall, None)
        operations.append(item_catchall_op)
        batch_ops.append(item_catchall_op)
        operation_batches.append((f"{lane}/{subgroup}", batch_ops))

    return operations, operation_batches, {
        "operation_count": len(operations),
        "batch_count": len(operation_batches),
        "batch_operation_counts": {name: len(batch) for name, batch in operation_batches},
        "removed_subgroup_units": len(existing),
        "created_subgroup_subdivisions": len(existing),
        "created_exact_item_units": len(candidate_rows),
        "created_item_catchall_exclusions": len(existing),
        "shape": "existing root/lane/subgroup tree -> subgroup subdivision -> exact product_item_id units + excluded product_item_id catchall",
    }


def mutate(client: GoogleAdsClient, customer_id: str, operations: list[Any], validate_only: bool) -> dict[str, Any]:
    service = client.get_service("GoogleAdsService")
    request = client.get_type("MutateGoogleAdsRequest")
    request.customer_id = customer_id
    request.mutate_operations.extend(operations)
    request.partial_failure = False
    request.validate_only = validate_only
    response = service.mutate(request=request)
    return {
        "validate_only": validate_only,
        "result_count": len(response.mutate_operation_responses),
        "response_types": [
            response_item._pb.WhichOneof("response")
            for response_item in response.mutate_operation_responses
        ],
    }


def mutate_batches(
    client: GoogleAdsClient,
    customer_id: str,
    operation_batches: list[tuple[str, list[Any]]],
    validate_only: bool,
) -> dict[str, Any]:
    results = []
    for name, operations in operation_batches:
        result = mutate(client, customer_id, operations, validate_only=validate_only)
        result["batch"] = name
        results.append(result)
    return {
        "validate_only": validate_only,
        "batch_count": len(results),
        "result_count": sum(result["result_count"] for result in results),
        "batches": results,
    }


def validate_readback(
    after: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    unresolved_rows: list[dict[str, str]],
    out_of_stock_rows: list[dict[str, str]],
) -> dict[str, Any]:
    candidate_ids = {row["item_id"] for row in candidate_rows}
    held_ids = {row["item_id"] for row in unresolved_rows + out_of_stock_rows}
    campaigns = [row for row in after["campaigns"] if row["name"] in CAMPAIGN_NAMES]
    old = [row for row in after["campaigns"] if row["name"] == OLD_CAMPAIGN_NAME]
    ad_groups = after["ad_groups"]
    product_ads = after["product_ads"]
    listing_groups = after["listing_groups"]
    item_units = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT"
        and not row["negative"]
        and row["case_dimension"] == "product_item_id"
        and row["case_value"]
    ]
    item_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT"
        and row["negative"]
        and row["case_dimension"] == "product_item_id"
        and not row["case_value"]
        and row["parent_ad_group_criterion"]
    ]
    included_subgroup_units = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT"
        and not row["negative"]
        and row["case_dimension"] == "product_custom_attribute"
        and row["case_index"] == "INDEX2"
        and row["case_value"]
    ]
    item_ids = {row["case_value"] for row in item_units}
    missing_candidate_ids = sorted(candidate_ids - item_ids)
    extra_item_ids = sorted(item_ids - candidate_ids)
    held_item_ids = sorted(item_ids & held_ids)
    issues = []
    if len(campaigns) != 3 or any(row["status"] != "PAUSED" for row in campaigns):
        issues.append("V2 campaigns are not exactly 3 paused campaigns")
    if not old or old[0]["status"] != "PAUSED":
        issues.append("Old test campaign is not paused")
    if len(ad_groups) != 12 or any(row["status"] != "PAUSED" for row in ad_groups):
        issues.append("V2 ad groups are not exactly 12 paused ad groups")
    if len(product_ads) != 12 or any(row["status"] != "PAUSED" for row in product_ads):
        issues.append("V2 product ads are not exactly 12 paused product ads")
    if missing_candidate_ids:
        issues.append(f"Missing candidate item units: {missing_candidate_ids[:5]}")
    if extra_item_ids:
        issues.append(f"Unexpected item units outside candidate scope: {extra_item_ids[:5]}")
    if held_item_ids:
        issues.append(f"Held item IDs included: {held_item_ids[:5]}")
    if included_subgroup_units:
        issues.append(f"Included subgroup units remain: {len(included_subgroup_units)}")
    return {
        "passed": not issues,
        "issues": issues,
        "campaign_count": len(campaigns),
        "old_campaign_status": old[0]["status"] if old else "NOT_FOUND",
        "ad_group_count": len(ad_groups),
        "product_ad_count": len(product_ads),
        "listing_group_count": len(listing_groups),
        "included_exact_item_units": len(item_units),
        "unique_included_item_ids": len(item_ids),
        "item_catchall_exclusion_units": len(item_catchalls),
        "included_subgroup_units_remaining": len(included_subgroup_units),
        "missing_candidate_ids": len(missing_candidate_ids),
        "extra_item_ids": len(extra_item_ids),
        "held_item_ids_included": len(held_item_ids),
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    validation = payload.get("after_validation") or {}
    report = [
        "# Google Shopping Parent-Outfit Exact-Scope Product-Group Enforcement",
        "",
        f"UTC timestamp: `{payload['timestamp_utc']}`",
        "",
        "## Mode",
        "",
        f"- Mode: `{payload['mode']}`",
        f"- Validate-only passed: `{payload.get('validate_only_passed')}`",
        f"- Executed: `{payload.get('executed')}`",
        "",
        "## Scope",
        "",
        f"- Candidate rows: `{payload['input_summary']['candidate_rows']}`",
        f"- Held unresolved rows: `{payload['input_summary']['held_unresolved_rows']}`",
        f"- Held out-of-stock rows: `{payload['input_summary']['held_out_of_stock_rows']}`",
        "",
        "## Operation Plan",
        "",
        f"- Operation count: `{payload['operation_metadata']['operation_count']}`",
        f"- Removed subgroup units: `{payload['operation_metadata']['removed_subgroup_units']}`",
        f"- Created subgroup subdivisions: `{payload['operation_metadata']['created_subgroup_subdivisions']}`",
        f"- Created exact item units: `{payload['operation_metadata']['created_exact_item_units']}`",
        f"- Created item catchall exclusions: `{payload['operation_metadata']['created_item_catchall_exclusions']}`",
        "",
        "## Readback",
        "",
        f"- Validation passed: `{validation.get('passed')}`",
        f"- Campaigns: `{validation.get('campaign_count')}`",
        f"- Old campaign status: `{validation.get('old_campaign_status')}`",
        f"- Ad groups: `{validation.get('ad_group_count')}`",
        f"- Product ads: `{validation.get('product_ad_count')}`",
        f"- Listing groups: `{validation.get('listing_group_count')}`",
        f"- Included exact item units: `{validation.get('included_exact_item_units')}`",
        f"- Unique included item IDs: `{validation.get('unique_included_item_ids')}`",
        f"- Item catchall exclusions: `{validation.get('item_catchall_exclusion_units')}`",
        f"- Included subgroup units remaining: `{validation.get('included_subgroup_units_remaining')}`",
        f"- Missing candidate IDs: `{validation.get('missing_candidate_ids')}`",
        f"- Extra item IDs: `{validation.get('extra_item_ids')}`",
        f"- Held item IDs included: `{validation.get('held_item_ids_included')}`",
        "",
        "## Guardrails",
        "",
        "- All V2 campaigns, ad groups, and product ads must remain paused.",
        "- The old test campaign must remain paused.",
        "- No activation, budget, bid, conversion, billing, Merchant, Shopify, Google & YouTube, feed/source, broad sync, source reset, or product recreation write is authorized by this script.",
        "",
        "## Files",
        "",
        f"- Before JSON: `{payload['before_file']}`",
        f"- After JSON: `{payload.get('after_file')}`",
    ]
    if validation.get("issues"):
        report.extend(["", "## Issues", ""])
        report.extend(f"- {issue}" for issue in validation["issues"])
    path.write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--customer-id", default=CUSTOMER_ID)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    customer_id = normalize_customer_id(args.customer_id)
    timestamp = now_stamp()
    candidate_rows = load_csv(CANDIDATES_CSV)
    unresolved_rows = load_csv(UNRESOLVED_CSV)
    out_of_stock_rows = load_csv(OUT_OF_STOCK_CSV)
    input_summary = validate_inputs(candidate_rows, unresolved_rows, out_of_stock_rows)
    grouped_ids: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in candidate_rows:
        grouped_ids[(row["lane"], row["subgroup"])].append(row["item_id"])

    client = get_client(Path(args.config))
    before = full_readback(client, customer_id)
    before_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_exact_scope_before_{timestamp}.json"
    write_json(before_file, {"timestamp_utc": timestamp, "readback": before})
    operations, operation_batches, operation_metadata = build_operations(client, customer_id, before, candidate_rows)
    payload: dict[str, Any] = {
        "timestamp_utc": timestamp,
        "mode": "execute" if args.execute else "validate_only" if args.validate_only else "dry_run",
        "approval_phrase": APPROVAL_PHRASE,
        "input_summary": input_summary,
        "operation_metadata": operation_metadata,
        "before_file": str(before_file),
        "executed": False,
        "validate_only_passed": False,
    }

    if args.validate_only or args.execute:
        try:
            payload["validate_only_response"] = mutate_batches(client, customer_id, operation_batches, validate_only=True)
            payload["validate_only_passed"] = True
        except GoogleAdsException as exc:
            payload["validate_only_error"] = google_ads_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_EXACT_SCOPE_ENFORCEMENT_{timestamp}.md"
            payload["report_file"] = str(report_file)
            payload["after_validation"] = validate_readback(before, candidate_rows, unresolved_rows, out_of_stock_rows)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1
        except google_api_exceptions.GoogleAPICallError as exc:
            payload["validate_only_error"] = generic_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_EXACT_SCOPE_ENFORCEMENT_{timestamp}.md"
            payload["report_file"] = str(report_file)
            payload["after_validation"] = validate_readback(before, candidate_rows, unresolved_rows, out_of_stock_rows)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    if args.execute:
        try:
            payload["execute_response"] = mutate_batches(client, customer_id, operation_batches, validate_only=False)
            payload["executed"] = True
        except GoogleAdsException as exc:
            payload["execute_error"] = google_ads_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_EXACT_SCOPE_ENFORCEMENT_{timestamp}.md"
            payload["report_file"] = str(report_file)
            payload["after_validation"] = validate_readback(before, candidate_rows, unresolved_rows, out_of_stock_rows)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1
        except google_api_exceptions.GoogleAPICallError as exc:
            payload["execute_error"] = generic_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_EXACT_SCOPE_ENFORCEMENT_{timestamp}.md"
            payload["report_file"] = str(report_file)
            payload["after_validation"] = validate_readback(before, candidate_rows, unresolved_rows, out_of_stock_rows)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    after = full_readback(client, customer_id)
    after_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_exact_scope_after_{timestamp}.json"
    write_json(after_file, {"timestamp_utc": timestamp, "readback": after})
    payload["after_file"] = str(after_file)
    payload["after_validation"] = validate_readback(after, candidate_rows, unresolved_rows, out_of_stock_rows)
    report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_EXACT_SCOPE_ENFORCEMENT_{timestamp}.md"
    payload["report_file"] = str(report_file)
    write_report(report_file, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.execute:
        return 0 if payload["after_validation"]["passed"] else 1
    return 0 if payload["validate_only_passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
