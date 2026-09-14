#!/usr/bin/env python3
"""Create/read back the approved Dress Like Mommy US Search exact CPC test.

This script is intentionally packet-local and guarded:
- default mode is read-only/dry-run
- live mutation requires --execute
- duplicate campaign names are refused unless --allow-existing-readback is used
- account-scope CSV negatives are applied to this campaign only, not account-wide
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
CAMPAIGN_NAME = "DLM_US_SEARCH_EXACT_020_TEST_20260519"
BUDGET_MICROS = 5_000_000
MAX_CPC_BID_MICROS = 200_000
CUSTOMER_ID = "3990976848"
US_GEO_TARGET = "geoTargetConstants/2840"
EN_LANGUAGE = "languageConstants/1000"

KEYWORDS_CSV = PACKET_DIR / "us_search_exact_020_launch_keywords.csv"
NEGATIVES_CSV = PACKET_DIR / "us_search_exact_020_negative_keywords.csv"
RSA_CSV = PACKET_DIR / "us_search_exact_020_rsa_assets.csv"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def normalize_customer_id(customer_id: str) -> str:
    return customer_id.replace("-", "").strip()


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


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
    return {
        "request_id": exc.request_id,
        "failure": errors,
    }


def get_client(config_path: Path) -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(str(config_path))


def search_rows(client: GoogleAdsClient, customer_id: str, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=customer_id, query=query))


def validate_inputs(keyword_rows: list[dict[str, str]], negative_rows: list[dict[str, str]], rsa_rows: list[dict[str, str]]) -> dict[str, Any]:
    issues: list[str] = []

    if not keyword_rows:
        issues.append("No launch keyword rows found.")
    if not negative_rows:
        issues.append("No negative keyword rows found.")
    if not rsa_rows:
        issues.append("No RSA rows found.")

    ad_groups = {row["ad_group"] for row in keyword_rows}
    rsa_ad_groups = {row["ad_group"] for row in rsa_rows}
    missing_rsa = sorted(ad_groups - rsa_ad_groups)
    if missing_rsa:
        issues.append(f"Missing RSA rows for ad groups: {missing_rsa}")

    for row in keyword_rows:
        if row["campaign"] != CAMPAIGN_NAME:
            issues.append(f"Unexpected campaign in keyword CSV: {row['campaign']}")
        if row["match_type"].lower() != "exact":
            issues.append(f"Launch keyword is not exact match: {row['keyword']}")
        if int(row["max_cpc_bid_micros"]) != MAX_CPC_BID_MICROS:
            issues.append(f"Keyword CPC is not 200000 micros: {row['keyword']}")
        if not row["final_url"].startswith("https://www.dresslikemommy.com/"):
            issues.append(f"Unexpected final URL domain: {row['final_url']}")

    for row in rsa_rows:
        headlines = [item.strip() for item in row["headlines"].split("|") if item.strip()]
        descriptions = [item.strip() for item in row["descriptions"].split("|") if item.strip()]
        if not (3 <= len(headlines) <= 15):
            issues.append(f"RSA headline count invalid for {row['ad_group']}: {len(headlines)}")
        if not (2 <= len(descriptions) <= 4):
            issues.append(f"RSA description count invalid for {row['ad_group']}: {len(descriptions)}")
        for headline in headlines:
            if len(headline) > 30:
                issues.append(f"RSA headline exceeds 30 chars for {row['ad_group']}: {headline}")
        for description in descriptions:
            if len(description) > 90:
                issues.append(f"RSA description exceeds 90 chars for {row['ad_group']}: {description}")

    if issues:
        raise ValueError("Input validation failed:\n- " + "\n- ".join(issues))

    scoped_account_negatives = sum(1 for row in negative_rows if row["scope"] == "account")
    campaign_negatives = sum(1 for row in negative_rows if row["scope"] in {"account", "campaign"})
    ad_group_negatives = sum(1 for row in negative_rows if row["scope"] == "ad_group")

    return {
        "keyword_count": len(keyword_rows),
        "ad_group_count": len(ad_groups),
        "rsa_count": len(rsa_rows),
        "negative_count": len(negative_rows),
        "campaign_scoped_negative_count": campaign_negatives,
        "ad_group_negative_count": ad_group_negatives,
        "account_scope_rows_scoped_to_campaign": scoped_account_negatives,
    }


def existing_campaigns(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = f"""
        SELECT
          campaign.resource_name,
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.primary_status,
          campaign.advertising_channel_type,
          campaign.bidding_strategy_type,
          campaign.campaign_budget,
          campaign.network_settings.target_google_search,
          campaign.network_settings.target_search_network,
          campaign.network_settings.target_content_network,
          campaign.network_settings.target_partner_search_network,
          campaign.geo_target_type_setting.positive_geo_target_type,
          campaign.manual_cpc.enhanced_cpc_enabled,
          campaign.ai_max_setting.enable_ai_max
        FROM campaign
        WHERE campaign.name = '{CAMPAIGN_NAME}'
        LIMIT 20
    """
    results = []
    for row in search_rows(client, customer_id, query):
        campaign = row.campaign
        results.append(
            {
                "resource_name": campaign.resource_name,
                "id": campaign.id,
                "name": campaign.name,
                "status": enum_name(campaign.status),
                "primary_status": enum_name(campaign.primary_status),
                "advertising_channel_type": enum_name(campaign.advertising_channel_type),
                "bidding_strategy_type": enum_name(campaign.bidding_strategy_type),
                "campaign_budget": campaign.campaign_budget,
                "network_settings": {
                    "target_google_search": campaign.network_settings.target_google_search,
                    "target_search_network": campaign.network_settings.target_search_network,
                    "target_content_network": campaign.network_settings.target_content_network,
                    "target_partner_search_network": campaign.network_settings.target_partner_search_network,
                },
                "positive_geo_target_type": enum_name(campaign.geo_target_type_setting.positive_geo_target_type),
                "enhanced_cpc_enabled": campaign.manual_cpc.enhanced_cpc_enabled,
                "ai_max_enabled": campaign.ai_max_setting.enable_ai_max,
            }
        )
    return results


def conversion_action_readback(client: GoogleAdsClient, customer_id: str) -> list[dict[str, Any]]:
    query = """
        SELECT
          conversion_action.id,
          conversion_action.name,
          conversion_action.status,
          conversion_action.category,
          conversion_action.primary_for_goal,
          conversion_action.include_in_conversions_metric,
          conversion_action.value_settings.default_value,
          conversion_action.value_settings.always_use_default_value
        FROM conversion_action
        WHERE conversion_action.category = PURCHASE
        ORDER BY conversion_action.id
    """
    rows: list[dict[str, Any]] = []
    try:
        for row in search_rows(client, customer_id, query):
            action = row.conversion_action
            rows.append(
                {
                    "id": action.id,
                    "name": action.name,
                    "status": enum_name(action.status),
                    "category": enum_name(action.category),
                    "primary_for_goal": action.primary_for_goal,
                    "include_in_conversions_metric": action.include_in_conversions_metric,
                    "default_value": action.value_settings.default_value,
                    "always_use_default_value": action.value_settings.always_use_default_value,
                }
            )
    except GoogleAdsException as exc:
        rows.append({"query_failed": google_ads_error_payload(exc)})
    return rows


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


def campaign_detail_readback(client: GoogleAdsClient, customer_id: str) -> dict[str, Any]:
    readback: dict[str, Any] = {
        "campaigns": existing_campaigns(client, customer_id),
        "budgets": [],
        "campaign_criteria": [],
        "ad_groups": [],
        "ad_group_criteria": [],
        "ads": [],
        "query_errors": [],
    }

    queries = {
        "budgets": f"""
            SELECT
              campaign_budget.resource_name,
              campaign_budget.id,
              campaign_budget.name,
              campaign_budget.amount_micros,
              campaign_budget.period,
              campaign_budget.delivery_method,
              campaign_budget.explicitly_shared,
              campaign.name
            FROM campaign_budget
            WHERE campaign.name = '{CAMPAIGN_NAME}'
            ORDER BY campaign_budget.id
        """,
        "campaign_criteria": f"""
            SELECT
              campaign_criterion.criterion_id,
              campaign_criterion.type,
              campaign_criterion.status,
              campaign_criterion.negative,
              campaign_criterion.keyword.text,
              campaign_criterion.keyword.match_type,
              campaign_criterion.location.geo_target_constant,
              campaign_criterion.language.language_constant,
              campaign.name
            FROM campaign_criterion
            WHERE campaign.name = '{CAMPAIGN_NAME}'
            ORDER BY campaign_criterion.type, campaign_criterion.criterion_id
        """,
        "ad_groups": f"""
            SELECT
              ad_group.resource_name,
              ad_group.id,
              ad_group.name,
              ad_group.status,
              ad_group.type,
              ad_group.cpc_bid_micros,
              campaign.name
            FROM ad_group
            WHERE campaign.name = '{CAMPAIGN_NAME}'
            ORDER BY ad_group.name
        """,
        "ad_group_criteria": f"""
            SELECT
              ad_group.name,
              ad_group_criterion.criterion_id,
              ad_group_criterion.type,
              ad_group_criterion.status,
              ad_group_criterion.negative,
              ad_group_criterion.keyword.text,
              ad_group_criterion.keyword.match_type,
              ad_group_criterion.cpc_bid_micros,
              ad_group_criterion.final_urls
            FROM ad_group_criterion
            WHERE campaign.name = '{CAMPAIGN_NAME}'
            ORDER BY ad_group.name, ad_group_criterion.negative, ad_group_criterion.keyword.text
        """,
        "ads": f"""
            SELECT
              ad_group.name,
              ad_group_ad.resource_name,
              ad_group_ad.status,
              ad_group_ad.ad.id,
              ad_group_ad.ad.type,
              ad_group_ad.ad.final_urls,
              ad_group_ad.ad.responsive_search_ad.headlines,
              ad_group_ad.ad.responsive_search_ad.descriptions
            FROM ad_group_ad
            WHERE campaign.name = '{CAMPAIGN_NAME}'
            ORDER BY ad_group.name, ad_group_ad.ad.id
        """,
    }

    for key, query in queries.items():
        try:
            for row in search_rows(client, customer_id, query):
                if key == "budgets":
                    budget = row.campaign_budget
                    readback[key].append(
                        {
                            "resource_name": budget.resource_name,
                            "id": budget.id,
                            "name": budget.name,
                            "amount_micros": budget.amount_micros,
                            "period": enum_name(budget.period),
                            "delivery_method": enum_name(budget.delivery_method),
                            "explicitly_shared": budget.explicitly_shared,
                        }
                    )
                elif key == "campaign_criteria":
                    criterion = row.campaign_criterion
                    readback[key].append(
                        {
                            "criterion_id": criterion.criterion_id,
                            "type": enum_name(criterion.type_),
                            "status": enum_name(criterion.status),
                            "negative": criterion.negative,
                            "keyword_text": criterion.keyword.text,
                            "keyword_match_type": enum_name(criterion.keyword.match_type),
                            "location_geo_target_constant": criterion.location.geo_target_constant,
                            "language_constant": criterion.language.language_constant,
                        }
                    )
                elif key == "ad_groups":
                    ad_group = row.ad_group
                    readback[key].append(
                        {
                            "resource_name": ad_group.resource_name,
                            "id": ad_group.id,
                            "name": ad_group.name,
                            "status": enum_name(ad_group.status),
                            "type": enum_name(ad_group.type_),
                            "cpc_bid_micros": ad_group.cpc_bid_micros,
                        }
                    )
                elif key == "ad_group_criteria":
                    criterion = row.ad_group_criterion
                    readback[key].append(
                        {
                            "ad_group": row.ad_group.name,
                            "criterion_id": criterion.criterion_id,
                            "type": enum_name(criterion.type_),
                            "status": enum_name(criterion.status),
                            "negative": criterion.negative,
                            "keyword_text": criterion.keyword.text,
                            "keyword_match_type": enum_name(criterion.keyword.match_type),
                            "cpc_bid_micros": criterion.cpc_bid_micros,
                            "final_urls": list(criterion.final_urls),
                        }
                    )
                elif key == "ads":
                    ad = row.ad_group_ad.ad
                    rsa = ad.responsive_search_ad
                    readback[key].append(
                        {
                            "ad_group": row.ad_group.name,
                            "resource_name": row.ad_group_ad.resource_name,
                            "status": enum_name(row.ad_group_ad.status),
                            "ad_id": ad.id,
                            "type": enum_name(ad.type_),
                            "final_urls": list(ad.final_urls),
                            "headline_count": len(rsa.headlines),
                            "description_count": len(rsa.descriptions),
                            "headlines": [asset.text for asset in rsa.headlines],
                            "descriptions": [asset.text for asset in rsa.descriptions],
                        }
                    )
        except GoogleAdsException as exc:
            readback["query_errors"].append({"section": key, "error": google_ads_error_payload(exc)})

    return readback


def build_operations(
    client: GoogleAdsClient,
    customer_id: str,
    keyword_rows: list[dict[str, str]],
    negative_rows: list[dict[str, str]],
    rsa_rows: list[dict[str, str]],
) -> tuple[list[Any], dict[str, Any]]:
    enums = client.enums
    operations: list[Any] = []
    metadata: dict[str, Any] = {
        "account_scope_negative_rows_applied_as_campaign_negatives": [],
        "campaign_negative_keywords": [],
        "ad_group_negative_keywords": [],
    }

    budget_resource = f"customers/{customer_id}/campaignBudgets/-1"
    campaign_resource = f"customers/{customer_id}/campaigns/-2"

    budget_op = client.get_type("MutateOperation")
    budget = budget_op.campaign_budget_operation.create
    budget.resource_name = budget_resource
    budget.name = f"{CAMPAIGN_NAME} Budget"
    budget.amount_micros = BUDGET_MICROS
    budget.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    budget.period = enums.BudgetPeriodEnum.DAILY
    budget.explicitly_shared = False
    operations.append(budget_op)

    campaign_op = client.get_type("MutateOperation")
    campaign = campaign_op.campaign_operation.create
    campaign.resource_name = campaign_resource
    campaign.name = CAMPAIGN_NAME
    campaign.status = enums.CampaignStatusEnum.ENABLED
    campaign.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.campaign_budget = budget_resource
    campaign.manual_cpc.enhanced_cpc_enabled = False
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
    campaign.network_settings.target_youtube = False
    campaign.network_settings.target_google_tv_network = False
    campaign.geo_target_type_setting.positive_geo_target_type = enums.PositiveGeoTargetTypeEnum.PRESENCE
    campaign.geo_target_type_setting.negative_geo_target_type = enums.NegativeGeoTargetTypeEnum.PRESENCE
    campaign.ai_max_setting.enable_ai_max = False
    campaign.contains_eu_political_advertising = enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    for automation_type in [
        enums.AssetAutomationTypeEnum.TEXT_ASSET_AUTOMATION,
        enums.AssetAutomationTypeEnum.FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION,
    ]:
        setting = client.get_type("Campaign.AssetAutomationSetting")
        setting.asset_automation_type = automation_type
        setting.asset_automation_status = enums.AssetAutomationStatusEnum.OPTED_OUT
        campaign.asset_automation_settings.append(setting)
    operations.append(campaign_op)

    for criterion_type, resource_name in [("location", US_GEO_TARGET), ("language", EN_LANGUAGE)]:
        op = client.get_type("MutateOperation")
        criterion = op.campaign_criterion_operation.create
        criterion.campaign = campaign_resource
        criterion.status = enums.CampaignCriterionStatusEnum.ENABLED
        if criterion_type == "location":
            criterion.location.geo_target_constant = resource_name
        else:
            criterion.language.language_constant = resource_name
        operations.append(op)

    ad_group_temp_resources: dict[str, str] = {}
    for index, ad_group_name in enumerate(sorted({row["ad_group"] for row in keyword_rows}), start=3):
        resource = f"customers/{customer_id}/adGroups/-{index}"
        ad_group_temp_resources[ad_group_name] = resource
        op = client.get_type("MutateOperation")
        ad_group = op.ad_group_operation.create
        ad_group.resource_name = resource
        ad_group.name = ad_group_name
        ad_group.campaign = campaign_resource
        ad_group.status = enums.AdGroupStatusEnum.ENABLED
        ad_group.type_ = enums.AdGroupTypeEnum.SEARCH_STANDARD
        ad_group.cpc_bid_micros = MAX_CPC_BID_MICROS
        operations.append(op)

    for row in keyword_rows:
        op = client.get_type("MutateOperation")
        criterion = op.ad_group_criterion_operation.create
        criterion.ad_group = ad_group_temp_resources[row["ad_group"]]
        criterion.status = enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = row["keyword"]
        criterion.keyword.match_type = enums.KeywordMatchTypeEnum.EXACT
        criterion.cpc_bid_micros = int(row["max_cpc_bid_micros"])
        criterion.final_urls.append(row["final_url"])
        operations.append(op)

    for row in negative_rows:
        match_type = getattr(enums.KeywordMatchTypeEnum, row["match_type"].upper())
        if row["scope"] in {"account", "campaign"}:
            op = client.get_type("MutateOperation")
            criterion = op.campaign_criterion_operation.create
            criterion.campaign = campaign_resource
            criterion.negative = True
            criterion.keyword.text = row["negative_keyword"]
            criterion.keyword.match_type = match_type
            operations.append(op)
            metadata["campaign_negative_keywords"].append(row["negative_keyword"])
            if row["scope"] == "account":
                metadata["account_scope_negative_rows_applied_as_campaign_negatives"].append(row["negative_keyword"])
        elif row["scope"] == "ad_group":
            op = client.get_type("MutateOperation")
            criterion = op.ad_group_criterion_operation.create
            criterion.ad_group = ad_group_temp_resources[row["ad_group"]]
            criterion.negative = True
            criterion.keyword.text = row["negative_keyword"]
            criterion.keyword.match_type = match_type
            operations.append(op)
            metadata["ad_group_negative_keywords"].append({"ad_group": row["ad_group"], "keyword": row["negative_keyword"]})
        else:
            raise ValueError(f"Unsupported negative scope: {row['scope']}")

    for row in sorted(rsa_rows, key=lambda item: item["ad_group"]):
        op = client.get_type("MutateOperation")
        ad_group_ad = op.ad_group_ad_operation.create
        ad_group_ad.ad_group = ad_group_temp_resources[row["ad_group"]]
        ad_group_ad.status = enums.AdGroupAdStatusEnum.ENABLED
        ad_group_ad.ad.final_urls.append(row["final_url"])
        rsa = ad_group_ad.ad.responsive_search_ad
        for headline in [item.strip() for item in row["headlines"].split("|") if item.strip()]:
            asset = client.get_type("AdTextAsset")
            asset.text = headline
            rsa.headlines.append(asset)
        for description in [item.strip() for item in row["descriptions"].split("|") if item.strip()]:
            asset = client.get_type("AdTextAsset")
            asset.text = description
            rsa.descriptions.append(asset)
        operations.append(op)

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
        "resource_names": [
            response_item._pb.WhichOneof("response")
            for response_item in response.mutate_operation_responses
        ],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, payload: dict[str, Any]) -> None:
    before_count = len(payload["before"]["campaigns"])
    after = payload.get("after", {})
    after_campaigns = after.get("campaigns", [])
    campaign = after_campaigns[0] if after_campaigns else {}
    ad_group_count = len(after.get("ad_groups", []))
    live_keywords = [
        item
        for item in after.get("ad_group_criteria", [])
        if not item.get("negative") and item.get("type") == "KEYWORD"
    ]
    campaign_negatives = [
        item
        for item in after.get("campaign_criteria", [])
        if item.get("negative") and item.get("type") == "KEYWORD"
    ]
    ad_group_negatives = [
        item
        for item in after.get("ad_group_criteria", [])
        if item.get("negative") and item.get("type") == "KEYWORD"
    ]
    ads = after.get("ads", [])
    report = [
        "# Google Ads API Live Launch Execution Report",
        "",
        f"UTC timestamp: `{payload['timestamp_utc']}`",
        "",
        "## Approval",
        "",
        payload["approval_phrase"],
        "",
        "## Before-State Readback",
        "",
        f"- Existing campaign count for `{CAMPAIGN_NAME}` before mutation: `{before_count}`",
        f"- Customer: `{payload['customer'].get('descriptive_name')}` (`{payload['customer'].get('id')}`), currency `{payload['customer'].get('currency_code')}`",
        "",
        "## Execution Result",
        "",
        f"- Mode: `{payload['mode']}`",
        f"- Validate-only passed: `{payload.get('validate_only_passed')}`",
        f"- Live mutate executed: `{payload.get('executed')}`",
        f"- Operation count: `{payload.get('operation_metadata', {}).get('operation_count')}`",
        f"- CSV account-scope negatives applied only to this campaign: `{len(payload.get('operation_metadata', {}).get('account_scope_negative_rows_applied_as_campaign_negatives', []))}`",
        "",
        "## After-State Readback",
        "",
        f"- Campaign status: `{campaign.get('status')}`",
        f"- Campaign primary status: `{campaign.get('primary_status')}`",
        f"- Campaign type: `{campaign.get('advertising_channel_type')}`",
        f"- Bidding strategy type: `{campaign.get('bidding_strategy_type')}`",
        f"- Google Search: `{campaign.get('network_settings', {}).get('target_google_search')}`",
        f"- Search Partners/Search Network: `{campaign.get('network_settings', {}).get('target_search_network')}`",
        f"- Display/content network: `{campaign.get('network_settings', {}).get('target_content_network')}`",
        f"- Partner search network: `{campaign.get('network_settings', {}).get('target_partner_search_network')}`",
        f"- Presence-only location targeting: `{campaign.get('positive_geo_target_type')}`",
        f"- Enhanced CPC enabled: `{campaign.get('enhanced_cpc_enabled')}`",
        f"- AI Max enabled: `{campaign.get('ai_max_enabled')}`",
        f"- Ad groups: `{ad_group_count}`",
        f"- Exact positive keywords: `{len(live_keywords)}`",
        f"- Campaign-scoped negative keywords: `{len(campaign_negatives)}`",
        f"- Ad-group negative keywords: `{len(ad_group_negatives)}`",
        f"- RSAs: `{len(ads)}`",
        "",
        "## Files",
        "",
        f"- Before JSON: `{payload['before_file']}`",
        f"- After JSON: `{payload.get('after_file')}`",
        "",
    ]
    path.write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to google-ads.yaml")
    parser.add_argument("--customer-id", default=CUSTOMER_ID, help="Google Ads customer ID")
    parser.add_argument("--execute", action="store_true", help="Execute the approved live mutation")
    parser.add_argument("--validate-only", action="store_true", help="Send the mutate request with validate_only=true")
    parser.add_argument("--allow-existing-readback", action="store_true", help="Only read back if campaign already exists")
    args = parser.parse_args()

    customer_id = normalize_customer_id(args.customer_id)
    timestamp = now_stamp()
    approval_phrase = (
        "Approve enabling the Google Ads Search campaign DLM_US_SEARCH_EXACT_020_TEST_20260519 exactly as specified in "
        "US_SEARCH_EXACT_020_LAUNCH_APPROVAL_PACKET.md: Google Search only, United States, English, exact match only, "
        "$5/day max budget, $0.20 max CPC, purchase-only conversion, no broad match, no AI Max, no PMax, no Search Partners, "
        "no Display, and no changes outside this packet."
    )

    keyword_rows = load_csv(KEYWORDS_CSV)
    negative_rows = load_csv(NEGATIVES_CSV)
    rsa_rows = load_csv(RSA_CSV)
    input_summary = validate_inputs(keyword_rows, negative_rows, rsa_rows)

    client = get_client(Path(args.config))
    customer = customer_readback(client, customer_id)
    before = campaign_detail_readback(client, customer_id)
    before_file = PACKET_DIR / f"google_ads_api_live_before_readback_{timestamp}.json"
    write_json(
        before_file,
        {
            "timestamp_utc": timestamp,
            "customer": customer,
            "conversion_actions_purchase_readback": conversion_action_readback(client, customer_id),
            "campaign_detail": before,
        },
    )

    operations, operation_metadata = build_operations(client, customer_id, keyword_rows, negative_rows, rsa_rows)
    payload: dict[str, Any] = {
        "timestamp_utc": timestamp,
        "mode": "execute" if args.execute else "validate_only" if args.validate_only else "dry_run",
        "approval_phrase": approval_phrase,
        "customer": customer,
        "input_summary": input_summary,
        "before": before,
        "before_file": str(before_file),
        "operation_metadata": operation_metadata,
        "executed": False,
        "validate_only_passed": False,
    }

    if before["campaigns"] and not args.allow_existing_readback:
        payload["refused"] = "Campaign with packet name already exists; refusing duplicate create."
        report_file = PACKET_DIR / f"google_ads_api_live_execution_report_{timestamp}.md"
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
            report_file = PACKET_DIR / f"google_ads_api_live_execution_report_{timestamp}.md"
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
            report_file = PACKET_DIR / f"google_ads_api_live_execution_report_{timestamp}.md"
            payload["report_file"] = str(report_file)
            write_report(report_file, payload)
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    after = campaign_detail_readback(client, customer_id)
    after_file = PACKET_DIR / f"google_ads_api_live_after_readback_{timestamp}.json"
    write_json(
        after_file,
        {
            "timestamp_utc": timestamp,
            "customer": customer,
            "conversion_actions_purchase_readback": conversion_action_readback(client, customer_id),
            "campaign_detail": after,
        },
    )
    payload["after"] = after
    payload["after_file"] = str(after_file)

    report_file = PACKET_DIR / f"google_ads_api_live_execution_report_{timestamp}.md"
    payload["report_file"] = str(report_file)
    write_report(report_file, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
