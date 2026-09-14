#!/usr/bin/env python3
"""Create/read back the approved paused Google Shopping Shopify-sold retest.

Guardrails:
- default mode is read-only/dry-run
- live mutation requires --execute
- creates one paused Standard Shopping campaign, one paused ad group, one paused
  product ad, exact product-item listing units, and an excluded catchall
- does not enable spend
- does not edit Merchant Center, Shopify, feeds, products, conversions,
  existing campaigns, existing budgets, existing bids, or billing
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
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
CAMPAIGN_NAME = "DLM_US_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_20260521"
AD_GROUP_NAME = "Shopify Sold Products Exact Item IDs 20260521"
ITEM_SCOPE_CSV = PACKET_DIR / "google_ads_retest_candidate_item_scope_2026-05-21.csv"
APPROVAL_PHRASE = (
    "I approve creating the paused-ready Google Shopping Shopify-sold-products retest "
    "from the 2026-05-21 packet only: exact item IDs in "
    "google_ads_retest_candidate_item_scope_2026-05-21.csv, max CPC $0.15, daily cap $5, "
    "no PMax, no broad catchall, no Search Partners, no Display, no GA4 optimization, "
    "no Merchant/Shopify product/feed changes, and stop for readback before enabling spend."
)

DAILY_BUDGET_MICROS = 5_000_000
CPC_BID_MICROS = 150_000


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def normalize_customer_id(customer_id: str) -> str:
    return customer_id.replace("-", "").strip()


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_item_scope(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    item_ids: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            ids = [item.strip() for item in row["shopping_item_ids_pipe"].split("|") if item.strip()]
            for item_id in ids:
                if not item_id.startswith("shopify_us_"):
                    raise ValueError(f"Unexpected item ID format: {item_id}")
                item_ids.add(item_id)
            rows.append({**row, "item_ids": ids})
    if len(rows) != 8:
        raise ValueError(f"Expected 8 retest products, found {len(rows)}")
    if len(item_ids) != 19:
        raise ValueError(f"Expected 19 unique item IDs, found {len(item_ids)}")
    return rows


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


def name_filter(names: list[str]) -> str:
    return ", ".join(f"'{quote_sql(name)}'" for name in names)


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
          campaign.network_settings.target_google_search,
          campaign.network_settings.target_search_network,
          campaign.network_settings.target_content_network,
          campaign.network_settings.target_partner_search_network,
          campaign_budget.id,
          campaign_budget.name,
          campaign_budget.amount_micros,
          campaign_budget.explicitly_shared
        FROM campaign
        WHERE campaign.name IN ({name_filter(names)})
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
                "target_google_search": campaign.network_settings.target_google_search,
                "target_search_network": campaign.network_settings.target_search_network,
                "target_content_network": campaign.network_settings.target_content_network,
                "target_partner_search_network": campaign.network_settings.target_partner_search_network,
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
          campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign.name IN ({name_filter(names)})
        ORDER BY campaign.name, campaign_criterion.criterion_id
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        criterion = row.campaign_criterion
        rows.append(
            {
                "campaign": row.campaign.name,
                "resource_name": criterion.resource_name,
                "criterion_id": criterion.criterion_id,
                "type": enum_name(criterion.type_),
                "status": enum_name(criterion.status),
                "negative": criterion.negative,
                "location": criterion.location.geo_target_constant,
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
        WHERE campaign.name IN ({name_filter(names)})
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
        WHERE campaign.name IN ({name_filter(names)})
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
          ad_group_criterion.listing_group.case_value.product_item_id.value
        FROM ad_group_criterion
        WHERE campaign.name IN ({name_filter(names)})
          AND ad_group_criterion.type = LISTING_GROUP
        ORDER BY campaign.name, ad_group.name, ad_group_criterion.criterion_id
    """
    rows: list[dict[str, Any]] = []
    for row in search_rows(client, customer_id, query):
        criterion = row.ad_group_criterion
        listing_group = criterion.listing_group
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
                "product_item_id": listing_group.case_value.product_item_id.value,
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


def build_operations(client: GoogleAdsClient, customer_id: str, item_ids: list[str]) -> tuple[list[Any], dict[str, Any]]:
    enums = client.enums
    operations: list[Any] = []
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

    campaign_id = next_id()
    budget_id = next_id()
    ad_group_id = next_id()
    root_id = next_id()
    catchall_id = next_id()

    campaign_resource = resource("campaigns", campaign_id)
    budget_resource = resource("campaignBudgets", budget_id)
    ad_group_resource = resource("adGroups", ad_group_id)
    root_resource = ad_group_criterion_resource(ad_group_id, root_id)
    catchall_resource = ad_group_criterion_resource(ad_group_id, catchall_id)

    budget_op = client.get_type("MutateOperation")
    budget = budget_op.campaign_budget_operation.create
    budget.resource_name = budget_resource
    budget.name = f"{CAMPAIGN_NAME} Budget"
    budget.amount_micros = DAILY_BUDGET_MICROS
    budget.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    budget.period = enums.BudgetPeriodEnum.DAILY
    budget.explicitly_shared = False
    operations.append(budget_op)

    campaign_op = client.get_type("MutateOperation")
    campaign = campaign_op.campaign_operation.create
    campaign.resource_name = campaign_resource
    campaign.name = CAMPAIGN_NAME
    campaign.status = enums.CampaignStatusEnum.PAUSED
    campaign.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SHOPPING
    campaign.campaign_budget = budget_resource
    campaign.manual_cpc.enhanced_cpc_enabled = False
    campaign.shopping_setting.merchant_id = MERCHANT_ID
    campaign.shopping_setting.feed_label = FEED_LABEL
    campaign.shopping_setting.campaign_priority = 1
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
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

    ad_group_op = client.get_type("MutateOperation")
    ad_group = ad_group_op.ad_group_operation.create
    ad_group.resource_name = ad_group_resource
    ad_group.name = AD_GROUP_NAME
    ad_group.campaign = campaign_resource
    ad_group.status = enums.AdGroupStatusEnum.PAUSED
    ad_group.type_ = enums.AdGroupTypeEnum.SHOPPING_PRODUCT_ADS
    ad_group.cpc_bid_micros = CPC_BID_MICROS
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

    for item_id in item_ids:
        item_criterion_id = next_id()
        item_resource = ad_group_criterion_resource(ad_group_id, item_criterion_id)
        item_op = client.get_type("MutateOperation")
        item = item_op.ad_group_criterion_operation.create
        item.resource_name = item_resource
        item.ad_group = ad_group_resource
        item.status = enums.AdGroupCriterionStatusEnum.ENABLED
        item.cpc_bid_micros = CPC_BID_MICROS
        item.listing_group.type_ = enums.ListingGroupTypeEnum.UNIT
        item.listing_group.parent_ad_group_criterion = root_resource
        item.listing_group.case_value.product_item_id.value = item_id
        operations.append(item_op)

    catchall_op = client.get_type("MutateOperation")
    catchall = catchall_op.ad_group_criterion_operation.create
    catchall.resource_name = catchall_resource
    catchall.ad_group = ad_group_resource
    catchall.status = enums.AdGroupCriterionStatusEnum.ENABLED
    catchall.negative = True
    catchall.listing_group.type_ = enums.ListingGroupTypeEnum.UNIT
    catchall.listing_group.parent_ad_group_criterion = root_resource
    catchall.listing_group.case_value.product_item_id._pb.SetInParent()
    operations.append(catchall_op)

    return operations, {
        "campaign_name": CAMPAIGN_NAME,
        "ad_group_name": AD_GROUP_NAME,
        "operation_count": len(operations),
        "item_id_count": len(item_ids),
        "daily_budget_micros": DAILY_BUDGET_MICROS,
        "cpc_bid_micros": CPC_BID_MICROS,
        "listing_group_shape": "root subdivision -> 19 exact product_item_id units + one excluded product_item_id catchall",
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


def validate_after_readback(after: dict[str, Any], item_ids: list[str]) -> dict[str, Any]:
    campaigns = [row for row in after["campaigns"] if row["name"] == CAMPAIGN_NAME]
    ad_groups = [row for row in after["ad_groups"] if row["campaign"] == CAMPAIGN_NAME]
    product_ads = [row for row in after["product_ads"] if row["campaign"] == CAMPAIGN_NAME]
    listing_groups = [row for row in after["listing_groups"] if row["campaign"] == CAMPAIGN_NAME]
    criteria = [row for row in after["campaign_criteria"] if row["campaign"] == CAMPAIGN_NAME]

    issues: list[str] = []
    if len(campaigns) != 1:
        issues.append(f"Expected 1 campaign, found {len(campaigns)}")
    else:
        campaign = campaigns[0]
        if campaign["status"] != "PAUSED":
            issues.append(f"Campaign not paused: {campaign['status']}")
        if campaign["advertising_channel_type"] != "SHOPPING":
            issues.append(f"Campaign is not Shopping: {campaign['advertising_channel_type']}")
        if campaign["budget_amount_micros"] != DAILY_BUDGET_MICROS:
            issues.append(f"Budget micros mismatch: {campaign['budget_amount_micros']}")
        if campaign["merchant_id"] != MERCHANT_ID:
            issues.append(f"Merchant ID mismatch: {campaign['merchant_id']}")
        if campaign["feed_label"] != FEED_LABEL:
            issues.append(f"Feed label mismatch: {campaign['feed_label']}")
        if not campaign["target_google_search"]:
            issues.append("Google Search network is not targeted")
        if campaign["target_search_network"]:
            issues.append("Search Network is targeted but should be off")
        if campaign["target_content_network"]:
            issues.append("Display/content network is targeted but should be off")
        if campaign["target_partner_search_network"]:
            issues.append("Search Partners are targeted but should be off")

    if len(ad_groups) != 1:
        issues.append(f"Expected 1 ad group, found {len(ad_groups)}")
    else:
        ad_group = ad_groups[0]
        if ad_group["status"] != "PAUSED":
            issues.append(f"Ad group not paused: {ad_group['status']}")
        if ad_group["cpc_bid_micros"] != CPC_BID_MICROS:
            issues.append(f"Ad group CPC mismatch: {ad_group['cpc_bid_micros']}")

    if len(product_ads) != 1:
        issues.append(f"Expected 1 product ad, found {len(product_ads)}")
    else:
        if product_ads[0]["status"] != "PAUSED":
            issues.append(f"Product ad not paused: {product_ads[0]['status']}")

    included = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["negative"] and row["product_item_id"]
    ]
    excluded = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and row["negative"] and not row["product_item_id"]
    ]
    subdivisions = [row for row in listing_groups if row["listing_group_type"] == "SUBDIVISION"]
    bad_catchalls = [
        row
        for row in listing_groups
        if row["listing_group_type"] == "UNIT" and not row["product_item_id"] and not row["negative"]
    ]
    readback_item_ids = {row["product_item_id"] for row in included}
    expected_item_ids = set(item_ids)
    if len(subdivisions) != 1:
        issues.append(f"Expected 1 root subdivision, found {len(subdivisions)}")
    if readback_item_ids != expected_item_ids:
        issues.append(
            f"Item ID mismatch: missing={sorted(expected_item_ids - readback_item_ids)} "
            f"extra={sorted(readback_item_ids - expected_item_ids)}"
        )
    if len(excluded) != 1:
        issues.append(f"Expected 1 excluded catchall, found {len(excluded)}")
    if bad_catchalls:
        issues.append(f"Found non-excluded catchall units: {bad_catchalls}")
    for row in included:
        if row["cpc_bid_micros"] != CPC_BID_MICROS:
            issues.append(f"Item CPC mismatch for {row['product_item_id']}: {row['cpc_bid_micros']}")

    location_criteria = [row for row in criteria if row["type"] == "LOCATION"]
    if len(location_criteria) != 1:
        issues.append(f"Expected 1 location criterion, found {len(location_criteria)}")

    return {
        "passed": not issues,
        "issues": issues,
        "campaign_count": len(campaigns),
        "ad_group_count": len(ad_groups),
        "product_ad_count": len(product_ads),
        "listing_group_count": len(listing_groups),
        "included_item_units": len(included),
        "excluded_catchall_units": len(excluded),
        "bad_catchall_units": len(bad_catchalls),
        "location_criterion_count": len(location_criteria),
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    after_validation = payload.get("after_validation", {})
    report = [
        "# Google Shopping Shopify-Sold Product Retest Paused Setup Execution Report",
        "",
        f"UTC timestamp: `{payload['timestamp_utc']}`",
        "",
        "## Approval",
        "",
        payload["approval_phrase"],
        "",
        "## Before-State Readback",
        "",
        f"- Existing retest campaign count before mutation: `{len(payload['before'].get('campaigns', []))}`",
        f"- Old Standard Shopping campaign status: `{payload.get('old_campaign_status')}`",
        f"- Customer: `{payload['customer'].get('descriptive_name')}` (`{payload['customer'].get('id')}`), currency `{payload['customer'].get('currency_code')}`",
        "",
        "## Execution Result",
        "",
        f"- Mode: `{payload['mode']}`",
        f"- Validate-only passed: `{payload.get('validate_only_passed')}`",
        f"- Live mutate executed: `{payload.get('executed')}`",
        f"- Operation count: `{payload.get('operation_metadata', {}).get('operation_count')}`",
        f"- Daily cap budget micros: `{DAILY_BUDGET_MICROS}`",
        f"- Max CPC bid micros: `{CPC_BID_MICROS}`",
        "",
        "## After-State Readback",
        "",
        f"- Validation passed: `{after_validation.get('passed')}`",
        f"- Campaigns: `{after_validation.get('campaign_count')}`",
        f"- Ad groups: `{after_validation.get('ad_group_count')}`",
        f"- Product ads: `{after_validation.get('product_ad_count')}`",
        f"- Listing groups: `{after_validation.get('listing_group_count')}`",
        f"- Included exact item-ID units: `{after_validation.get('included_item_units')}`",
        f"- Excluded catchall units: `{after_validation.get('excluded_catchall_units')}`",
        f"- Bad catchall units: `{after_validation.get('bad_catchall_units')}`",
        f"- Location criteria: `{after_validation.get('location_criterion_count')}`",
        "",
        "## Guardrails",
        "",
        "- Campaign, ad group, and product ad must remain paused.",
        "- This setup does not enable spend. Stop before enabling spend.",
        "- No Merchant, Shopify, product/feed, conversion-goal, billing, PMax, Search Partners, Display, broad catchall, GA4 optimization, or existing campaign write occurred.",
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
    parser.add_argument("--execute", action="store_true", help="Execute the approved paused setup mutation")
    parser.add_argument("--validate-only", action="store_true", help="Send the mutate request with validate_only=true")
    parser.add_argument("--allow-existing-readback", action="store_true", help="Only read back if campaign already exists")
    args = parser.parse_args()

    customer_id = normalize_customer_id(args.customer_id)
    timestamp = now_stamp()
    scope_rows = load_item_scope(ITEM_SCOPE_CSV)
    item_ids = sorted({item_id for row in scope_rows for item_id in row["item_ids"]})
    names = [CAMPAIGN_NAME, OLD_CAMPAIGN_NAME]

    client = get_client(Path(args.config))
    customer = customer_readback(client, customer_id)
    before_all = full_readback(client, customer_id, names)
    before = {
        key: [row for row in value if row.get("campaign") == CAMPAIGN_NAME or row.get("name") == CAMPAIGN_NAME]
        for key, value in before_all.items()
    }
    old_campaigns = [row for row in before_all["campaigns"] if row["name"] == OLD_CAMPAIGN_NAME]
    old_campaign_status = old_campaigns[0]["status"] if old_campaigns else "NOT_FOUND"
    before_file = PACKET_DIR / f"google_ads_shopify_sold_retest_before_{timestamp}.json"
    write_json(
        before_file,
        {
            "timestamp_utc": timestamp,
            "customer": customer,
            "campaign_names": names,
            "readback": before_all,
            "item_scope": scope_rows,
        },
    )

    operations, operation_metadata = build_operations(client, customer_id, item_ids)
    payload: dict[str, Any] = {
        "timestamp_utc": timestamp,
        "mode": "execute" if args.execute else "validate_only" if args.validate_only else "dry_run",
        "approval_phrase": APPROVAL_PHRASE,
        "customer": customer,
        "item_id_count": len(item_ids),
        "item_ids": item_ids,
        "before": before,
        "old_campaign_status": old_campaign_status,
        "before_file": str(before_file),
        "operation_metadata": operation_metadata,
        "executed": False,
        "validate_only_passed": False,
    }

    if before["campaigns"] and not args.allow_existing_readback:
        payload["refused"] = "Retest campaign already exists; refusing duplicate create."
        after_file = PACKET_DIR / f"google_ads_shopify_sold_retest_after_{timestamp}.json"
        write_json(after_file, {"timestamp_utc": timestamp, "customer": customer, "readback": before_all})
        payload["after"] = before
        payload["after_file"] = str(after_file)
        payload["after_validation"] = validate_after_readback(before, item_ids)
        report_file = PACKET_DIR / f"GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_{timestamp}.md"
        payload["report_file"] = str(report_file)
        write_report(report_file, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2

    if before["campaigns"] and args.allow_existing_readback:
        payload["mode"] = "existing_readback"
        payload["after"] = before
        after_file = PACKET_DIR / f"google_ads_shopify_sold_retest_after_{timestamp}.json"
        write_json(after_file, {"timestamp_utc": timestamp, "customer": customer, "readback": before_all})
        payload["after_file"] = str(after_file)
        payload["after_validation"] = validate_after_readback(before, item_ids)
        report_file = PACKET_DIR / f"GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_{timestamp}.md"
        payload["report_file"] = str(report_file)
        write_report(report_file, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["after_validation"]["passed"] else 1

    if args.validate_only or args.execute:
        try:
            payload["validate_only_response"] = mutate(client, customer_id, operations, validate_only=True)
            payload["validate_only_passed"] = True
        except GoogleAdsException as exc:
            payload["validate_only_error"] = google_ads_error_payload(exc)
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_{timestamp}.md"
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
            report_file = PACKET_DIR / f"GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_{timestamp}.md"
            payload["report_file"] = str(report_file)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    after_all = full_readback(client, customer_id, names)
    after = {
        key: [row for row in value if row.get("campaign") == CAMPAIGN_NAME or row.get("name") == CAMPAIGN_NAME]
        for key, value in after_all.items()
    }
    after_file = PACKET_DIR / f"google_ads_shopify_sold_retest_after_{timestamp}.json"
    write_json(after_file, {"timestamp_utc": timestamp, "customer": customer, "readback": after_all})
    payload["after"] = after
    payload["after_file"] = str(after_file)
    payload["after_validation"] = validate_after_readback(after, item_ids)
    report_file = PACKET_DIR / f"GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_EXECUTION_{timestamp}.md"
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
