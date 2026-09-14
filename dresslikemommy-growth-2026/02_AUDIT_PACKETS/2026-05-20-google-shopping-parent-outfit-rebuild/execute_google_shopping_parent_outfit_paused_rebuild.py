#!/usr/bin/env python3
"""Create/read back the approved paused Google Shopping parent-outfit rebuild.

Guardrails:
- default mode is read-only/dry-run
- live mutation requires --execute
- duplicate V2 campaign names are refused unless --allow-existing-readback is used
- creates only paused campaigns, paused ad groups, paused product ads, and listing
  groups that exclude catchalls
- does not edit Merchant Center, Shopify, feed labels, products, conversions,
  existing budgets, existing bids, existing campaigns, or the old paused test
  campaign
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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


PACKET_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
CUSTOMER_ID = "3990976848"
MERCHANT_ID = 124884876
FEED_LABEL = "US"
US_GEO_TARGET = "geoTargetConstants/2840"
OLD_CAMPAIGN_NAME = "DLM_US_STANDARD_SHOPPING_TEST_PAID_READY"
APPROVAL_PHRASE = (
    "Approve the Google Shopping parent-outfit paused rebuild only: keep "
    "DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused, create/import only paused V2 "
    "Shopping structures from the packet, do not enable spend, do not change "
    "budgets/bids/statuses beyond paused draft requirements, do not include "
    "catchalls, and read back counts/images before any activation discussion."
)

CAMPAIGN_CSV = PACKET_DIR / "shopping_campaign_blueprint.csv"
AD_GROUP_CSV = PACKET_DIR / "shopping_ad_group_blueprint.csv"
TREE_CSV = PACKET_DIR / "shopping_product_group_tree.csv"
MERCHANT_SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"

# Required placeholder values for paused draft creation. These are not activation
# recommendations; they simply let Google Ads accept the paused structures.
DRAFT_DAILY_BUDGET_MICROS = 1_000_000
DRAFT_CPC_BID_MICROS = 10_000


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


def search_rows(client: GoogleAdsClient, customer_id: str, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=customer_id, query=query))


def quote_sql(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def validate_packet_inputs(
    campaign_rows: list[dict[str, str]],
    ad_group_rows: list[dict[str, str]],
    tree_rows: list[dict[str, str]],
    merchant_rows: list[dict[str, str]],
) -> dict[str, Any]:
    issues: list[str] = []
    campaign_names = [row["campaign_name"] for row in campaign_rows]
    expected_campaigns = {
        "DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2",
        "DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2",
        "DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2",
    }
    if set(campaign_names) != expected_campaigns:
        issues.append(f"Unexpected campaign names: {campaign_names}")

    for row in campaign_rows:
        if row["status_if_imported"] != "PAUSED":
            issues.append(f"Campaign is not paused in blueprint: {row['campaign_name']}")
        if row["channel"] != "Standard Shopping":
            issues.append(f"Campaign is not Standard Shopping: {row['campaign_name']}")
        if row["feed_label"] != FEED_LABEL:
            issues.append(f"Unexpected feed label for {row['campaign_name']}: {row['feed_label']}")
        if row["catchall_policy"] != "exclude_everything_else_at_campaign_and_ad_group_product_group_levels":
            issues.append(f"Unexpected catchall policy for {row['campaign_name']}")

    ad_group_counts = Counter(row["campaign_name"] for row in ad_group_rows)
    if sum(ad_group_counts.values()) != 12:
        issues.append(f"Expected 12 ad groups, found {sum(ad_group_counts.values())}")

    bad_catchalls = [
        row
        for row in tree_rows
        if row["value"] == "Everything else" and row["action"] != "EXCLUDE_UNIT"
    ]
    if bad_catchalls:
        issues.append(f"Catchall rows not excluded: {bad_catchalls[:3]}")

    include_units = [row for row in tree_rows if row["action"] == "INCLUDE_UNIT"]
    if len(include_units) != 12:
        issues.append(f"Expected 12 include units, found {len(include_units)}")
    for row in include_units:
        if row["status_if_imported"] != "PAUSED":
            issues.append(f"Include unit not paused in tree: {row}")
        if row["bid"] != "approval_required":
            issues.append(f"Include unit bid not approval-gated in tree: {row}")

    included_merch = [row for row in merchant_rows if row["decision"] == "INCLUDE"]
    if not included_merch:
        issues.append("Merchant spec has no included rows.")
    missing_group = sum(1 for row in included_merch if not row["proposed_item_group_id"])
    missing_image = sum(1 for row in included_merch if not row["proposed_image_link"])
    bad_ready = sum(
        1
        for row in included_merch
        if row["proposed_custom_label_0"] != "paid_eligible"
        or row["proposed_custom_label_3"] != "parent_outfit"
        or row["proposed_custom_label_4"] != "us_parent_outfit_ready_v20260520"
    )
    if missing_group:
        issues.append(f"Included merchant rows missing item_group_id: {missing_group}")
    if missing_image:
        issues.append(f"Included merchant rows missing hero image: {missing_image}")
    if bad_ready:
        issues.append(f"Included merchant rows missing readiness labels: {bad_ready}")

    parent_by_lane = defaultdict(set)
    for row in included_merch:
        parent_by_lane[row["proposed_custom_label_1"]].add(row["proposed_item_group_id"])
    parent_counts = {lane: len(values) for lane, values in sorted(parent_by_lane.items())}
    expected_counts = {"daddy_and_me": 34, "family_matching": 77, "mommy_and_me": 99}
    if parent_counts != expected_counts:
        issues.append(f"Unexpected parent counts from merchant spec: {parent_counts}")

    if issues:
        raise ValueError("Packet validation failed:\n- " + "\n- ".join(issues))

    return {
        "campaign_count": len(campaign_rows),
        "ad_group_count": len(ad_group_rows),
        "tree_rows": len(tree_rows),
        "include_units": len(include_units),
        "merchant_rows": len(merchant_rows),
        "included_merchant_rows": len(included_merch),
        "expected_parent_counts_by_lane": expected_counts,
        "draft_daily_budget_micros": DRAFT_DAILY_BUDGET_MICROS,
        "draft_cpc_bid_micros": DRAFT_CPC_BID_MICROS,
    }


def customer_readback(client: GoogleAdsClient, customer_id: str) -> dict[str, Any]:
    query = """
        SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone
        FROM customer
        LIMIT 1
    """
    for row in search_rows(client, customer_id, query):
        return {
            "id": row.customer.id,
            "descriptive_name": row.customer.descriptive_name,
            "currency_code": row.customer.currency_code,
            "time_zone": row.customer.time_zone,
        }
    return {}


def campaign_names_filter(names: list[str]) -> str:
    return ", ".join(f"'{quote_sql(name)}'" for name in names)


def readback_campaigns(client: GoogleAdsClient, customer_id: str, names: list[str]) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.id,
          campaign.resource_name,
          campaign.name,
          campaign.status,
          campaign.primary_status,
          campaign.advertising_channel_type,
          campaign.bidding_strategy_type,
          campaign.campaign_budget,
          campaign.shopping_setting.merchant_id,
          campaign.shopping_setting.feed_label,
          campaign.shopping_setting.campaign_priority,
          campaign.shopping_setting.disable_product_feed,
          campaign_budget.id,
          campaign_budget.name,
          campaign_budget.amount_micros,
          campaign_budget.explicitly_shared
        FROM campaign
        WHERE campaign.name IN ({campaign_names_filter(names)})
        ORDER BY campaign.name
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        campaign = row.campaign
        budget = row.campaign_budget
        rows.append(
            {
                "id": campaign.id,
                "resource_name": campaign.resource_name,
                "name": campaign.name,
                "status": enum_name(campaign.status),
                "primary_status": enum_name(campaign.primary_status),
                "advertising_channel_type": enum_name(campaign.advertising_channel_type),
                "bidding_strategy_type": enum_name(campaign.bidding_strategy_type),
                "campaign_budget": campaign.campaign_budget,
                "budget_id": budget.id,
                "budget_name": budget.name,
                "budget_amount_micros": budget.amount_micros,
                "budget_explicitly_shared": budget.explicitly_shared,
                "merchant_id": campaign.shopping_setting.merchant_id,
                "feed_label": campaign.shopping_setting.feed_label,
                "campaign_priority": campaign.shopping_setting.campaign_priority,
                "disable_product_feed": campaign.shopping_setting.disable_product_feed,
            }
        )
    return rows


def readback_campaign_criteria(client: GoogleAdsClient, customer_id: str, names: list[str]) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          campaign_criterion.resource_name,
          campaign_criterion.criterion_id,
          campaign_criterion.type,
          campaign_criterion.status,
          campaign_criterion.negative,
          campaign_criterion.location.geo_target_constant,
          campaign_criterion.listing_scope.dimensions
        FROM campaign_criterion
        WHERE campaign.name IN ({campaign_names_filter(names)})
        ORDER BY campaign.name, campaign_criterion.criterion_id
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        criterion = row.campaign_criterion
        dimensions: list[dict[str, str]] = []
        for dimension in criterion.listing_scope.dimensions:
            attr = dimension.product_custom_attribute
            dimensions.append({"index": enum_name(attr.index), "value": attr.value})
        rows.append(
            {
                "campaign": row.campaign.name,
                "resource_name": criterion.resource_name,
                "criterion_id": criterion.criterion_id,
                "type": enum_name(criterion.type_),
                "status": enum_name(criterion.status),
                "negative": criterion.negative,
                "location": criterion.location.geo_target_constant,
                "listing_scope_dimensions": dimensions,
            }
        )
    return rows


def readback_ad_groups(client: GoogleAdsClient, customer_id: str, names: list[str]) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.id,
          ad_group.resource_name,
          ad_group.name,
          ad_group.status,
          ad_group.type,
          ad_group.cpc_bid_micros
        FROM ad_group
        WHERE campaign.name IN ({campaign_names_filter(names)})
        ORDER BY campaign.name, ad_group.name
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        ad_group = row.ad_group
        rows.append(
            {
                "campaign": row.campaign.name,
                "id": ad_group.id,
                "resource_name": ad_group.resource_name,
                "name": ad_group.name,
                "status": enum_name(ad_group.status),
                "type": enum_name(ad_group.type_),
                "cpc_bid_micros": ad_group.cpc_bid_micros,
            }
        )
    return rows


def readback_product_ads(client: GoogleAdsClient, customer_id: str, names: list[str]) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.name,
          ad_group.name,
          ad_group_ad.resource_name,
          ad_group_ad.status,
          ad_group_ad.ad.id,
          ad_group_ad.ad.type
        FROM ad_group_ad
        WHERE campaign.name IN ({campaign_names_filter(names)})
        ORDER BY campaign.name, ad_group.name
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        ad = row.ad_group_ad
        rows.append(
            {
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "resource_name": ad.resource_name,
                "status": enum_name(ad.status),
                "ad_id": ad.ad.id,
                "ad_type": enum_name(ad.ad.type_),
            }
        )
    return rows


def readback_listing_groups(client: GoogleAdsClient, customer_id: str, names: list[str]) -> list[dict[str, Any]]:
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
          ad_group_criterion.listing_group.case_value.product_custom_attribute.value
        FROM ad_group_criterion
        WHERE campaign.name IN ({campaign_names_filter(names)})
          AND ad_group_criterion.type = LISTING_GROUP
        ORDER BY campaign.name, ad_group.name, ad_group_criterion.criterion_id
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        criterion = row.ad_group_criterion
        listing_group = criterion.listing_group
        attr = listing_group.case_value.product_custom_attribute
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
                "case_index": enum_name(attr.index),
                "case_value": attr.value,
            }
        )
    return rows


def full_readback(client: GoogleAdsClient, customer_id: str, names: list[str]) -> dict[str, Any]:
    return {
        "campaigns": readback_campaigns(client, customer_id, names),
        "campaign_criteria": readback_campaign_criteria(client, customer_id, names),
        "ad_groups": readback_ad_groups(client, customer_id, names),
        "product_ads": readback_product_ads(client, customer_id, names),
        "listing_groups": readback_listing_groups(client, customer_id, names),
    }


def is_target_row(row: dict[str, Any], campaign_names: list[str]) -> bool:
    return row.get("campaign") in campaign_names or row.get("name") in campaign_names


def custom_label_index(enums: Any, index: str) -> Any:
    return getattr(enums.ProductCustomAttributeIndexEnum, f"INDEX{index}")


def add_campaign_scope_dimension(client: GoogleAdsClient, criterion: Any, index: int, value: str) -> None:
    dimension = client.get_type("ListingDimensionInfo")
    dimension.product_custom_attribute.index = custom_label_index(client.enums, str(index))
    dimension.product_custom_attribute.value = value
    criterion.listing_scope.dimensions.append(dimension)


def set_listing_case_value(client: GoogleAdsClient, criterion: Any, index: int, value: str | None) -> None:
    criterion.listing_group.case_value.product_custom_attribute.index = custom_label_index(client.enums, str(index))
    if value is not None:
        criterion.listing_group.case_value.product_custom_attribute.value = value


def build_operations(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_rows: list[dict[str, str]],
    ad_group_rows: list[dict[str, str]],
) -> tuple[list[Any], dict[str, Any]]:
    enums = client.enums
    operations: list[Any] = []
    metadata: dict[str, Any] = {
        "campaigns": [],
        "ad_groups": [],
        "listing_group_shape": "root subdivision -> custom_label_1 lane subdivision + excluded root catchall -> custom_label_2 subgroup unit + excluded subgroup catchall",
        "draft_daily_budget_micros": DRAFT_DAILY_BUDGET_MICROS,
        "draft_cpc_bid_micros": DRAFT_CPC_BID_MICROS,
    }
    temp_id = -1

    def next_id() -> int:
        nonlocal temp_id
        value = temp_id
        temp_id -= 1
        return value

    def resource(kind: str, resource_id: int) -> str:
        return f"customers/{customer_id}/{kind}/{resource_id}"

    def ad_group_criterion_resource(ad_group_id: int, criterion_id: int) -> str:
        return f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"

    ad_groups_by_campaign: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ad_group_rows:
        ad_groups_by_campaign[row["campaign_name"]].append(row)

    for campaign_row in campaign_rows:
        campaign_name = campaign_row["campaign_name"]
        campaign_id = next_id()
        budget_id = next_id()
        campaign_resource = resource("campaigns", campaign_id)
        budget_resource = resource("campaignBudgets", budget_id)

        budget_op = client.get_type("MutateOperation")
        budget = budget_op.campaign_budget_operation.create
        budget.resource_name = budget_resource
        budget.name = f"{campaign_name} Paused Draft Budget"
        budget.amount_micros = DRAFT_DAILY_BUDGET_MICROS
        budget.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
        budget.period = enums.BudgetPeriodEnum.DAILY
        budget.explicitly_shared = False
        operations.append(budget_op)

        campaign_op = client.get_type("MutateOperation")
        campaign = campaign_op.campaign_operation.create
        campaign.resource_name = campaign_resource
        campaign.name = campaign_name
        campaign.status = enums.CampaignStatusEnum.PAUSED
        campaign.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SHOPPING
        campaign.campaign_budget = budget_resource
        campaign.manual_cpc.enhanced_cpc_enabled = False
        campaign.shopping_setting.merchant_id = MERCHANT_ID
        campaign.shopping_setting.feed_label = FEED_LABEL
        campaign.shopping_setting.campaign_priority = 1
        campaign.geo_target_type_setting.positive_geo_target_type = enums.PositiveGeoTargetTypeEnum.PRESENCE
        campaign.geo_target_type_setting.negative_geo_target_type = enums.NegativeGeoTargetTypeEnum.PRESENCE
        campaign.contains_eu_political_advertising = enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
        operations.append(campaign_op)

        location_op = client.get_type("MutateOperation")
        location = location_op.campaign_criterion_operation.create
        location.campaign = campaign_resource
        location.status = enums.CampaignCriterionStatusEnum.ENABLED
        location.location.geo_target_constant = US_GEO_TARGET
        operations.append(location_op)

        scope_op = client.get_type("MutateOperation")
        scope = scope_op.campaign_criterion_operation.create
        scope.campaign = campaign_resource
        scope.status = enums.CampaignCriterionStatusEnum.ENABLED
        add_campaign_scope_dimension(client, scope, 0, "paid_eligible")
        add_campaign_scope_dimension(client, scope, 1, campaign_row["top_level_lane"])
        add_campaign_scope_dimension(client, scope, 4, "us_parent_outfit_ready_v20260520")
        operations.append(scope_op)

        metadata["campaigns"].append(
            {
                "name": campaign_name,
                "resource": campaign_resource,
                "status": "PAUSED",
                "inventory_scope": campaign_row["inventory_scope"],
            }
        )

        for ad_group_row in sorted(ad_groups_by_campaign[campaign_name], key=lambda item: item["ad_group_name"]):
            ad_group_id = next_id()
            root_id = next_id()
            lane_id = next_id()
            root_catchall_id = next_id()
            subgroup_id = next_id()
            subgroup_catchall_id = next_id()
            ad_group_resource = resource("adGroups", ad_group_id)
            root_resource = ad_group_criterion_resource(ad_group_id, root_id)
            lane_resource = ad_group_criterion_resource(ad_group_id, lane_id)
            root_catchall_resource = ad_group_criterion_resource(ad_group_id, root_catchall_id)
            subgroup_resource = ad_group_criterion_resource(ad_group_id, subgroup_id)
            subgroup_catchall_resource = ad_group_criterion_resource(ad_group_id, subgroup_catchall_id)

            ad_group_op = client.get_type("MutateOperation")
            ad_group = ad_group_op.ad_group_operation.create
            ad_group.resource_name = ad_group_resource
            ad_group.name = ad_group_row["ad_group_name"]
            ad_group.campaign = campaign_resource
            ad_group.status = enums.AdGroupStatusEnum.PAUSED
            ad_group.type_ = enums.AdGroupTypeEnum.SHOPPING_PRODUCT_ADS
            ad_group.cpc_bid_micros = DRAFT_CPC_BID_MICROS
            operations.append(ad_group_op)

            product_ad_op = client.get_type("MutateOperation")
            product_ad = product_ad_op.ad_group_ad_operation.create
            product_ad.ad_group = ad_group_resource
            product_ad.status = enums.AdGroupAdStatusEnum.PAUSED
            product_ad.ad.shopping_product_ad = client.get_type("ShoppingProductAdInfo")
            operations.append(product_ad_op)

            root_op = client.get_type("MutateOperation")
            root = root_op.ad_group_criterion_operation.create
            root.resource_name = root_resource
            root.ad_group = ad_group_resource
            root.status = enums.AdGroupCriterionStatusEnum.ENABLED
            root.listing_group.type_ = enums.ListingGroupTypeEnum.SUBDIVISION
            operations.append(root_op)

            lane_op = client.get_type("MutateOperation")
            lane = lane_op.ad_group_criterion_operation.create
            lane.resource_name = lane_resource
            lane.ad_group = ad_group_resource
            lane.status = enums.AdGroupCriterionStatusEnum.ENABLED
            lane.listing_group.type_ = enums.ListingGroupTypeEnum.SUBDIVISION
            lane.listing_group.parent_ad_group_criterion = root_resource
            set_listing_case_value(client, lane, 1, campaign_row["top_level_lane"])
            operations.append(lane_op)

            root_catchall_op = client.get_type("MutateOperation")
            root_catchall = root_catchall_op.ad_group_criterion_operation.create
            root_catchall.resource_name = root_catchall_resource
            root_catchall.ad_group = ad_group_resource
            root_catchall.status = enums.AdGroupCriterionStatusEnum.ENABLED
            root_catchall.negative = True
            root_catchall.listing_group.type_ = enums.ListingGroupTypeEnum.UNIT
            root_catchall.listing_group.parent_ad_group_criterion = root_resource
            set_listing_case_value(client, root_catchall, 1, None)
            operations.append(root_catchall_op)

            subgroup_op = client.get_type("MutateOperation")
            subgroup = subgroup_op.ad_group_criterion_operation.create
            subgroup.resource_name = subgroup_resource
            subgroup.ad_group = ad_group_resource
            subgroup.status = enums.AdGroupCriterionStatusEnum.ENABLED
            subgroup.cpc_bid_micros = DRAFT_CPC_BID_MICROS
            subgroup.listing_group.type_ = enums.ListingGroupTypeEnum.UNIT
            subgroup.listing_group.parent_ad_group_criterion = lane_resource
            set_listing_case_value(client, subgroup, 2, ad_group_row["subcategory"])
            operations.append(subgroup_op)

            subgroup_catchall_op = client.get_type("MutateOperation")
            subgroup_catchall = subgroup_catchall_op.ad_group_criterion_operation.create
            subgroup_catchall.resource_name = subgroup_catchall_resource
            subgroup_catchall.ad_group = ad_group_resource
            subgroup_catchall.status = enums.AdGroupCriterionStatusEnum.ENABLED
            subgroup_catchall.negative = True
            subgroup_catchall.listing_group.type_ = enums.ListingGroupTypeEnum.UNIT
            subgroup_catchall.listing_group.parent_ad_group_criterion = lane_resource
            set_listing_case_value(client, subgroup_catchall, 2, None)
            operations.append(subgroup_catchall_op)

            metadata["ad_groups"].append(
                {
                    "campaign": campaign_name,
                    "name": ad_group_row["ad_group_name"],
                    "status": "PAUSED",
                    "lane": campaign_row["top_level_lane"],
                    "subgroup": ad_group_row["subcategory"],
                    "product_ad_status": "PAUSED",
                    "catchalls": "excluded",
                }
            )

    metadata["operation_count"] = len(operations)
    return operations, metadata


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


def validate_after_readback(after: dict[str, Any], campaign_rows: list[dict[str, str]]) -> dict[str, Any]:
    expected_names = {row["campaign_name"] for row in campaign_rows}
    campaigns = [row for row in after["campaigns"] if row["name"] in expected_names]
    ad_groups = [row for row in after["ad_groups"] if row["campaign"] in expected_names]
    product_ads = [row for row in after["product_ads"] if row["campaign"] in expected_names]
    listing_groups = [row for row in after["listing_groups"] if row["campaign"] in expected_names]
    campaign_criteria = [row for row in after["campaign_criteria"] if row["campaign"] in expected_names]

    issues: list[str] = []
    if len(campaigns) != 3:
        issues.append(f"Expected 3 campaigns, found {len(campaigns)}")
    for campaign in campaigns:
        if campaign["status"] != "PAUSED":
            issues.append(f"Campaign not paused: {campaign['name']}={campaign['status']}")
        if campaign["advertising_channel_type"] != "SHOPPING":
            issues.append(f"Campaign not Shopping: {campaign['name']}")
        if campaign["merchant_id"] != MERCHANT_ID:
            issues.append(f"Campaign Merchant ID mismatch: {campaign['name']}")
        if campaign["feed_label"] != FEED_LABEL:
            issues.append(f"Campaign feed label mismatch: {campaign['name']}")

    if len(ad_groups) != 12:
        issues.append(f"Expected 12 ad groups, found {len(ad_groups)}")
    for ad_group in ad_groups:
        if ad_group["status"] != "PAUSED":
            issues.append(f"Ad group not paused: {ad_group['campaign']} / {ad_group['name']}")

    if len(product_ads) != 12:
        issues.append(f"Expected 12 product ads, found {len(product_ads)}")
    for ad in product_ads:
        if ad["status"] != "PAUSED":
            issues.append(f"Product ad not paused: {ad['campaign']} / {ad['ad_group']}")

    listing_counter = Counter(row["listing_group_type"] for row in listing_groups)
    if len(listing_groups) != 60:
        issues.append(f"Expected 60 listing groups, found {len(listing_groups)}")
    if listing_counter.get("SUBDIVISION") != 24:
        issues.append(f"Expected 24 subdivision listing groups, found {listing_counter.get('SUBDIVISION')}")
    if listing_counter.get("UNIT") != 36:
        issues.append(f"Expected 36 unit listing groups, found {listing_counter.get('UNIT')}")
    include_units = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["negative"] and row["case_index"] == "INDEX2" and row["case_value"]
    ]
    excluded_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and row["negative"] and not row["case_value"]
    ]
    bad_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["case_value"] and not row["negative"]
    ]
    if len(include_units) != 12:
        issues.append(f"Expected 12 included subgroup units, found {len(include_units)}")
    if len(excluded_catchalls) != 24:
        issues.append(f"Expected 24 excluded catchall units, found {len(excluded_catchalls)}")
    if bad_catchalls:
        issues.append(f"Found non-excluded catchall units: {bad_catchalls[:3]}")

    scopes = [row for row in campaign_criteria if row["type"] == "LISTING_SCOPE"]
    if len(scopes) != 3:
        issues.append(f"Expected 3 campaign listing scopes, found {len(scopes)}")
    for scope in scopes:
        dims = {(item["index"], item["value"]) for item in scope["listing_scope_dimensions"]}
        if ("INDEX0", "paid_eligible") not in dims or ("INDEX4", "us_parent_outfit_ready_v20260520") not in dims:
            issues.append(f"Campaign listing scope missing paid/readiness gate: {scope}")

    return {
        "passed": not issues,
        "issues": issues,
        "campaign_count": len(campaigns),
        "ad_group_count": len(ad_groups),
        "product_ad_count": len(product_ads),
        "listing_group_count": len(listing_groups),
        "included_subgroup_units": len(include_units),
        "excluded_catchall_units": len(excluded_catchalls),
        "bad_catchall_units": len(bad_catchalls),
        "campaign_listing_scope_count": len(scopes),
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    after_validation = payload.get("after_validation", {})
    report = [
        "# Google Shopping Parent-Outfit Paused Rebuild Execution Report",
        "",
        f"UTC timestamp: `{payload['timestamp_utc']}`",
        "",
        "## Approval",
        "",
        payload["approval_phrase"],
        "",
        "## Before-State Readback",
        "",
        f"- Existing V2 campaign count before mutation: `{len(payload['before'].get('campaigns', []))}`",
        f"- Old test campaign status: `{payload.get('old_campaign_status')}`",
        f"- Customer: `{payload['customer'].get('descriptive_name')}` (`{payload['customer'].get('id')}`), currency `{payload['customer'].get('currency_code')}`",
        "",
        "## Execution Result",
        "",
        f"- Mode: `{payload['mode']}`",
        f"- Validate-only passed: `{payload.get('validate_only_passed')}`",
        f"- Live mutate executed: `{payload.get('executed')}`",
        f"- Operation count: `{payload.get('operation_metadata', {}).get('operation_count')}`",
        f"- Paused draft daily budget micros per campaign: `{DRAFT_DAILY_BUDGET_MICROS}`",
        f"- Paused draft CPC bid micros: `{DRAFT_CPC_BID_MICROS}`",
        "",
        "## After-State Readback",
        "",
        f"- Validation passed: `{after_validation.get('passed')}`",
        f"- Campaigns: `{after_validation.get('campaign_count')}`",
        f"- Ad groups: `{after_validation.get('ad_group_count')}`",
        f"- Product ads: `{after_validation.get('product_ad_count')}`",
        f"- Listing groups: `{after_validation.get('listing_group_count')}`",
        f"- Included subgroup units: `{after_validation.get('included_subgroup_units')}`",
        f"- Excluded catchall units: `{after_validation.get('excluded_catchall_units')}`",
        f"- Bad catchall units: `{after_validation.get('bad_catchall_units')}`",
        f"- Campaign listing scopes: `{after_validation.get('campaign_listing_scope_count')}`",
        "",
        "## Counts / Images Boundary",
        "",
        "- Google Ads structure readback verifies the paused campaigns, ad groups, product ads, listing scopes, and no-catchall tree.",
        "- Merchant product count/image readback remains a separate feed-label/Merchant refresh gate; this script does not mutate Merchant/Shopify feed labels or product images.",
        "- Do not discuss activation until Merchant-side counts/images prove the parent-outfit labels and hero images are live.",
        "",
        "## Guardrails",
        "",
        "- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` was not edited and must remain paused.",
        "- No enablement, Merchant, Shopify, feed, product, conversion, existing campaign, existing budget, existing bid, or billing write occurred.",
        "",
        "## Files",
        "",
        f"- Before JSON: `{payload['before_file']}`",
        f"- After JSON: `{payload.get('after_file')}`",
    ]
    if after_validation.get("issues"):
        report.extend(["", "## Validation Issues", ""])
        report.extend(f"- {issue}" for issue in after_validation["issues"])
    path.write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to google-ads.yaml")
    parser.add_argument("--customer-id", default=CUSTOMER_ID, help="Google Ads customer ID")
    parser.add_argument("--execute", action="store_true", help="Execute the approved live mutation")
    parser.add_argument("--validate-only", action="store_true", help="Send the mutate request with validate_only=true")
    parser.add_argument("--allow-existing-readback", action="store_true", help="Only read back if campaigns already exist")
    args = parser.parse_args()

    customer_id = normalize_customer_id(args.customer_id)
    timestamp = now_stamp()
    campaign_rows = load_csv(CAMPAIGN_CSV)
    ad_group_rows = load_csv(AD_GROUP_CSV)
    tree_rows = load_csv(TREE_CSV)
    merchant_rows = load_csv(MERCHANT_SPEC_CSV)
    input_summary = validate_packet_inputs(campaign_rows, ad_group_rows, tree_rows, merchant_rows)
    campaign_names = [row["campaign_name"] for row in campaign_rows]
    all_names = campaign_names + [OLD_CAMPAIGN_NAME]

    client = get_client(Path(args.config))
    customer = customer_readback(client, customer_id)
    before_all = full_readback(client, customer_id, all_names)
    before = {
        key: [row for row in value if is_target_row(row, campaign_names)]
        for key, value in before_all.items()
    }
    old_campaigns = [row for row in before_all["campaigns"] if row["name"] == OLD_CAMPAIGN_NAME]
    old_campaign_status = old_campaigns[0]["status"] if old_campaigns else "NOT_FOUND"
    before_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_before_{timestamp}.json"
    write_json(
        before_file,
        {
            "timestamp_utc": timestamp,
            "customer": customer,
            "campaign_names": all_names,
            "readback": before_all,
        },
    )

    operations, operation_metadata = build_operations(client, customer_id, campaign_rows, ad_group_rows)
    payload: dict[str, Any] = {
        "timestamp_utc": timestamp,
        "mode": "execute" if args.execute else "validate_only" if args.validate_only else "dry_run",
        "approval_phrase": APPROVAL_PHRASE,
        "customer": customer,
        "input_summary": input_summary,
        "before": before,
        "old_campaign_status": old_campaign_status,
        "before_file": str(before_file),
        "operation_metadata": operation_metadata,
        "executed": False,
        "validate_only_passed": False,
    }

    if before["campaigns"] and not args.allow_existing_readback:
        payload["refused"] = "One or more V2 campaigns already exist; refusing duplicate create."
        after_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_after_{timestamp}.json"
        write_json(after_file, {"timestamp_utc": timestamp, "customer": customer, "readback": before_all})
        payload["after"] = before
        payload["after_file"] = str(after_file)
        payload["after_validation"] = validate_after_readback(before, campaign_rows)
        report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
        payload["report_file"] = str(report_file)
        write_report(report_file, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2

    if before["campaigns"] and args.allow_existing_readback:
        payload["mode"] = "existing_readback"
        payload["after"] = before
        after_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_after_{timestamp}.json"
        write_json(
            after_file,
            {
                "timestamp_utc": timestamp,
                "customer": customer,
                "campaign_names": all_names,
                "readback": before_all,
            },
        )
        payload["after_file"] = str(after_file)
        payload["after_validation"] = validate_after_readback(before, campaign_rows)
        report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
        payload["report_file"] = str(report_file)
        write_report(report_file, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["after_validation"]["passed"] else 1

    if old_campaign_status != "PAUSED":
        payload["refused"] = f"Old test campaign is not paused: {old_campaign_status}"
        report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
        payload["report_file"] = str(report_file)
        write_report(report_file, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2

    if args.validate_only or args.execute:
        try:
            payload["validate_only_response"] = mutate(client, customer_id, operations, validate_only=True)
            payload["validate_only_passed"] = True
        except GoogleAdsException as exc:
            payload["validate_only_error"] = google_ads_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
            payload["report_file"] = str(report_file)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    if args.execute:
        try:
            payload["execute_response"] = mutate(client, customer_id, operations, validate_only=False)
            payload["executed"] = True
        except GoogleAdsException as exc:
            payload["execute_error"] = google_ads_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
            payload["report_file"] = str(report_file)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    after_all = full_readback(client, customer_id, all_names)
    after = {
        key: [row for row in value if is_target_row(row, campaign_names)]
        for key, value in after_all.items()
    }
    after_file = PACKET_DIR / f"google_ads_shopping_parent_outfit_after_{timestamp}.json"
    write_json(
        after_file,
        {
            "timestamp_utc": timestamp,
            "customer": customer,
            "campaign_names": all_names,
            "readback": after_all,
        },
    )
    payload["after"] = after
    payload["after_file"] = str(after_file)
    payload["after_validation"] = validate_after_readback(after, campaign_rows)

    report_file = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_{timestamp}.md"
    payload["report_file"] = str(report_file)
    write_report(report_file, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["after_validation"]["passed"] or not args.execute else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
