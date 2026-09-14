#!/usr/bin/env python3
"""Read-only multimarket Google Search forecast and duplicate audit.

No Google Ads objects are created or changed. The script:
- reads the live Google Ads Search account structure
- builds one deduplicated candidate matrix per market/language
- runs Google Ads API historical metrics and single-keyword forecasts
- joins results to existing live keywords/campaigns so future packets reuse or
  repair existing structures instead of duplicating them
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
ROOT = PACKET_DIR.parents[2]
SECURE_CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
CUSTOMER_ID = "3990976848"
MAX_CPC_MICROS = 150_000
MAX_CPC_USD = MAX_CPC_MICROS / 1_000_000

KEYWORD_UNIVERSE = ROOT / "ops/marketing/keyword_universe.csv"
NATIVE_MASTER = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade/google_ads_native_language_keyword_master.csv"
)


GEO = {
    "AU": "2036",
    "BE": "2056",
    "CA": "2124",
    "CH": "2756",
    "CZ": "2203",
    "DE": "2276",
    "DK": "2208",
    "ES": "2724",
    "FR": "2250",
    "GB": "2826",
    "GR": "2300",
    "IT": "2380",
    "NL": "2528",
    "PL": "2616",
    "PT": "2620",
    "RO": "2642",
    "SE": "2752",
    "US": "2840",
}


LANG = {
    "cs": "1021",
    "da": "1009",
    "de": "1001",
    "el": "1022",
    "en": "1000",
    "es": "1003",
    "fr": "1002",
    "it": "1004",
    "nl": "1010",
    "pl": "1030",
    "pt": "1014",
    "ro": "1032",
    "sv": "1015",
}


NATIVE_MARKET_MAP = {
    ("BE", "fr-BE"): ("BE_FR", "BE", "fr", "French Belgium"),
    ("BE", "nl-BE"): ("BE_NL", "BE", "nl", "Dutch Belgium"),
    ("CZ", "cs-CZ"): ("CZ_CS", "CZ", "cs", "Czech Czechia"),
    ("DE", "de-DE"): ("DE_DE", "DE", "de", "German Germany"),
    ("DK", "da-DK"): ("DK_DA", "DK", "da", "Danish Denmark"),
    ("ES", "es-ES"): ("ES_ES", "ES", "es", "Spanish Spain"),
    ("FR", "fr-FR"): ("FR_FR", "FR", "fr", "French France"),
    ("GR", "el-GR"): ("GR_EL", "GR", "el", "Greek Greece"),
    ("IT", "it-IT"): ("IT_IT", "IT", "it", "Italian Italy"),
    ("NL", "nl-NL"): ("NL_NL", "NL", "nl", "Dutch Netherlands"),
    ("PL", "pl-PL"): ("PL_PL", "PL", "pl", "Polish Poland"),
    ("PT", "pt-PT"): ("PT_PT", "PT", "pt", "Portuguese Portugal"),
    ("RO", "ro-RO"): ("RO_RO", "RO", "ro", "Romanian Romania"),
    ("SE", "sv-SE"): ("SE_SV", "SE", "sv", "Swedish Sweden"),
}


DERIVED_NATIVE_MARKETS = [
    ("US_ES", "US", "es", "Spanish United States", "ES", "es-ES"),
    ("CA_FR", "CA", "fr", "French Canada", "FR", "fr-FR"),
    ("CH_DE", "CH", "de", "German Switzerland", "DE", "de-DE"),
    ("CH_FR", "CH", "fr", "French Switzerland", "FR", "fr-FR"),
    ("CH_IT", "CH", "it", "Italian Switzerland", "IT", "it-IT"),
]


ENGLISH_MARKETS = {
    "GB": ("GB_EN", "GB", "en", "English United Kingdom"),
    "CA": ("CA_EN", "CA", "en", "English Canada"),
    "AU": ("AU_EN", "AU", "en", "English Australia"),
}


def normalize_customer_id(value: str) -> str:
    return value.replace("-", "").strip()


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_client(config_path: str | None):
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ModuleNotFoundError as exc:
        raise SystemExit("google-ads client library is not installed in this runtime") from exc
    candidates = []
    if config_path:
        candidates.append(Path(config_path).expanduser())
    if os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH"):
        candidates.append(Path(os.environ["GOOGLE_ADS_CONFIGURATION_FILE_PATH"]).expanduser())
    candidates.append(SECURE_CONFIG_PATH)
    for candidate in candidates:
        if candidate.exists():
            return GoogleAdsClient.load_from_storage(str(candidate))
    raise SystemExit(f"Google Ads API config missing; checked {', '.join(map(str, candidates))}")


def enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def micros_to_usd(value: int | None) -> str:
    if not value:
        return "0.000000"
    return f"{value / 1_000_000:.6f}"


def competition_name(value: Any) -> str:
    if value in ("", None):
        return ""
    mapping = {2: "LOW", 3: "MEDIUM", 4: "HIGH"}
    if isinstance(value, int):
        return mapping.get(value, str(value))
    raw = str(value)
    if raw.isdigit():
        return mapping.get(int(raw), raw)
    return raw.rsplit(".", 1)[-1] if "." in raw else raw


def month_name(month_enum_value: Any) -> str:
    by_value = {
        2: "january",
        3: "february",
        4: "march",
        5: "april",
        6: "may",
        7: "june",
        8: "july",
        9: "august",
        10: "september",
        11: "november",
        12: "december",
        13: "december",
    }
    if isinstance(month_enum_value, int):
        return by_value.get(month_enum_value, str(month_enum_value))
    raw = str(month_enum_value)
    if raw.isdigit():
        return by_value.get(int(raw), raw)
    return raw.rsplit(".", 1)[-1].lower() if "." in raw else raw.lower()


def match_type_enum(client: Any, value: str):
    return getattr(client.enums.KeywordMatchTypeEnum, value.strip().upper())


def search(client: Any, customer_id: str, query: str) -> list[Any]:
    service = client.get_service("GoogleAdsService")
    return list(service.search(customer_id=customer_id, query=query))


def fetch_live_inventory(client: Any, customer_id: str) -> dict[str, list[dict[str, Any]]]:
    inventory: dict[str, list[dict[str, Any]]] = {
        "campaigns": [],
        "campaign_criteria": [],
        "ad_groups": [],
        "keywords": [],
        "metrics": [],
    }
    campaign_query = """
        SELECT
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
          campaign.manual_cpc.enhanced_cpc_enabled,
          campaign.geo_target_type_setting.positive_geo_target_type,
          campaign.ai_max_setting.enable_ai_max,
          campaign_budget.amount_micros,
          campaign_budget.period
        FROM campaign
        WHERE campaign.status != REMOVED
        ORDER BY campaign.name
    """
    for row in search(client, customer_id, campaign_query):
        c = row.campaign
        inventory["campaigns"].append(
            {
                "campaign_id": c.id,
                "campaign": c.name,
                "status": enum_name(c.status),
                "primary_status": enum_name(c.primary_status),
                "channel": enum_name(c.advertising_channel_type),
                "bidding_strategy": enum_name(c.bidding_strategy_type),
                "budget_resource": c.campaign_budget,
                "budget_micros": row.campaign_budget.amount_micros,
                "budget_period": enum_name(row.campaign_budget.period),
                "target_google_search": c.network_settings.target_google_search,
                "target_search_network": c.network_settings.target_search_network,
                "target_content_network": c.network_settings.target_content_network,
                "target_partner_search_network": c.network_settings.target_partner_search_network,
                "enhanced_cpc_enabled": c.manual_cpc.enhanced_cpc_enabled,
                "positive_geo_target_type": enum_name(c.geo_target_type_setting.positive_geo_target_type),
                "ai_max_enabled": c.ai_max_setting.enable_ai_max,
            }
        )

    criteria_query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign_criterion.type,
          campaign_criterion.status,
          campaign_criterion.negative,
          campaign_criterion.location.geo_target_constant,
          campaign_criterion.language.language_constant,
          campaign_criterion.keyword.text,
          campaign_criterion.keyword.match_type
        FROM campaign_criterion
        WHERE campaign.status != REMOVED AND campaign_criterion.status != REMOVED
        ORDER BY campaign.name, campaign_criterion.type
    """
    for row in search(client, customer_id, criteria_query):
        cc = row.campaign_criterion
        inventory["campaign_criteria"].append(
            {
                "campaign_id": row.campaign.id,
                "campaign": row.campaign.name,
                "campaign_status": enum_name(row.campaign.status),
                "criterion_type": enum_name(cc.type_),
                "criterion_status": enum_name(cc.status),
                "negative": cc.negative,
                "geo_target_constant": cc.location.geo_target_constant,
                "language_constant": cc.language.language_constant,
                "keyword": cc.keyword.text,
                "keyword_match_type": enum_name(cc.keyword.match_type),
            }
        )

    ad_group_query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          ad_group.id,
          ad_group.name,
          ad_group.status,
          ad_group.type,
          ad_group.cpc_bid_micros
        FROM ad_group
        WHERE campaign.status != REMOVED AND ad_group.status != REMOVED
        ORDER BY campaign.name, ad_group.name
    """
    for row in search(client, customer_id, ad_group_query):
        ag = row.ad_group
        inventory["ad_groups"].append(
            {
                "campaign_id": row.campaign.id,
                "campaign": row.campaign.name,
                "campaign_status": enum_name(row.campaign.status),
                "ad_group_id": ag.id,
                "ad_group": ag.name,
                "ad_group_status": enum_name(ag.status),
                "ad_group_type": enum_name(ag.type_),
                "cpc_bid_micros": ag.cpc_bid_micros,
            }
        )

    keyword_query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          ad_group.id,
          ad_group.name,
          ad_group.status,
          ad_group_criterion.criterion_id,
          ad_group_criterion.status,
          ad_group_criterion.negative,
          ad_group_criterion.keyword.text,
          ad_group_criterion.keyword.match_type,
          ad_group_criterion.cpc_bid_micros,
          ad_group_criterion.final_urls
        FROM ad_group_criterion
        WHERE campaign.status != REMOVED
          AND ad_group.status != REMOVED
          AND ad_group_criterion.type = KEYWORD
          AND ad_group_criterion.status != REMOVED
        ORDER BY campaign.name, ad_group.name, ad_group_criterion.negative, ad_group_criterion.keyword.text
    """
    for row in search(client, customer_id, keyword_query):
        kw = row.ad_group_criterion
        inventory["keywords"].append(
            {
                "campaign_id": row.campaign.id,
                "campaign": row.campaign.name,
                "campaign_status": enum_name(row.campaign.status),
                "ad_group_id": row.ad_group.id,
                "ad_group": row.ad_group.name,
                "ad_group_status": enum_name(row.ad_group.status),
                "criterion_id": kw.criterion_id,
                "keyword_status": enum_name(kw.status),
                "negative": kw.negative,
                "keyword": kw.keyword.text,
                "match_type": enum_name(kw.keyword.match_type),
                "cpc_bid_micros": kw.cpc_bid_micros,
                "final_urls": "|".join(kw.final_urls),
            }
        )

    metrics_query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value
        FROM campaign
        WHERE campaign.status != REMOVED
          AND segments.date DURING LAST_30_DAYS
        ORDER BY campaign.name
    """
    for row in search(client, customer_id, metrics_query):
        inventory["metrics"].append(
            {
                "campaign_id": row.campaign.id,
                "campaign": row.campaign.name,
                "campaign_status": enum_name(row.campaign.status),
                "last_30d_impressions": row.metrics.impressions,
                "last_30d_clicks": row.metrics.clicks,
                "last_30d_cost_usd": f"{row.metrics.cost_micros / 1_000_000:.6f}",
                "last_30d_conversions": row.metrics.conversions,
                "last_30d_conversion_value": row.metrics.conversions_value,
            }
        )
    return inventory


def campaign_scope_maps(inventory: dict[str, list[dict[str, Any]]]) -> tuple[dict[int, set[str]], dict[int, set[str]]]:
    campaign_geos: dict[int, set[str]] = defaultdict(set)
    campaign_langs: dict[int, set[str]] = defaultdict(set)
    for row in inventory["campaign_criteria"]:
        if row["criterion_type"] == "LOCATION" and row["geo_target_constant"]:
            campaign_geos[int(row["campaign_id"])].add(row["geo_target_constant"].split("/")[-1])
        if row["criterion_type"] == "LANGUAGE" and row["language_constant"]:
            campaign_langs[int(row["campaign_id"])].add(row["language_constant"].split("/")[-1])
    return campaign_geos, campaign_langs


def add_candidate(candidates: dict[tuple[str, str, str], dict[str, Any]], row: dict[str, Any]) -> None:
    key = (row["market_key"], row["keyword"].strip().lower(), row["match_type"].upper())
    if key in candidates:
        prior = candidates[key]
        prior["source_refs"] = "|".join(sorted(set(prior["source_refs"].split("|") + [row["source_ref"]])))
        if row.get("theme") and row["theme"] not in prior["theme"].split("|"):
            prior["theme"] += f"|{row['theme']}"
        return
    row["match_type"] = row["match_type"].upper()
    row["max_cpc_bid_micros"] = str(MAX_CPC_MICROS)
    row["max_cpc_usd"] = f"{MAX_CPC_USD:.2f}"
    row["geo_target_id"] = GEO[row["country"]]
    row["language_id"] = LANG[row["language_code"]]
    candidates[key] = row


def build_candidate_matrix(inventory: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    candidates: dict[tuple[str, str, str], dict[str, Any]] = {}

    for row in read_csv(KEYWORD_UNIVERSE):
        if row["market"] not in ENGLISH_MARKETS:
            continue
        if row["match_candidate"] not in {"exact", "phrase"}:
            continue
        if not row["promotion_status"].startswith("LOCAL_ONLY_VALIDATE"):
            continue
        market_key, country, language_code, market_label = ENGLISH_MARKETS[row["market"]]
        add_candidate(
            candidates,
            {
                "market_key": market_key,
                "country": country,
                "language_code": language_code,
                "market_label": market_label,
                "theme": row["category"],
                "keyword": row["keyword"],
                "match_type": row["match_candidate"],
                "source_ref": "ops/marketing/keyword_universe.csv",
                "landing_route": row["landing_route"],
                "candidate_note": row["live_action"],
            },
        )

    native_rows = read_csv(NATIVE_MASTER)
    for row in native_rows:
        mapped = NATIVE_MARKET_MAP.get((row["market"], row["locale"]))
        if mapped:
            market_key, country, language_code, market_label = mapped
            add_candidate(
                candidates,
                {
                    "market_key": market_key,
                    "country": country,
                    "language_code": language_code,
                    "market_label": market_label,
                    "theme": row["theme"],
                    "keyword": row["keyword"],
                    "match_type": row["match_type"],
                    "source_ref": f"{NATIVE_MASTER.name}:{row['market']}:{row['locale']}",
                    "landing_route": "NEEDS_LOCALIZED_LANDING_REVIEW",
                    "candidate_note": row["review_gate"],
                },
            )
    for market_key, country, language_code, market_label, source_market, source_locale in DERIVED_NATIVE_MARKETS:
        for row in native_rows:
            if row["market"] == source_market and row["locale"] == source_locale:
                add_candidate(
                    candidates,
                    {
                        "market_key": market_key,
                        "country": country,
                        "language_code": language_code,
                        "market_label": market_label,
                        "theme": row["theme"],
                        "keyword": row["keyword"],
                        "match_type": row["match_type"],
                        "source_ref": f"derived_from_{source_market}_{source_locale}",
                        "landing_route": "NEEDS_LOCALIZED_LANDING_REVIEW",
                        "candidate_note": f"Derived from {source_market} native set; requires native/local market review.",
                    },
                )

    campaign_geos, campaign_langs = campaign_scope_maps(inventory)
    campaign_lookup: dict[tuple[str, str], list[str]] = defaultdict(list)
    for campaign in inventory["campaigns"]:
        if campaign["channel"] != "SEARCH":
            continue
        cid = int(campaign["campaign_id"])
        for geo in campaign_geos.get(cid, set()):
            for lang in campaign_langs.get(cid, set()):
                campaign_lookup[(geo, lang)].append(f"{campaign['campaign_id']}:{campaign['campaign']}:{campaign['status']}")

    existing_keywords: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    campaign_scope_by_id = {
        int(c["campaign_id"]): (campaign_geos.get(int(c["campaign_id"]), set()), campaign_langs.get(int(c["campaign_id"]), set()))
        for c in inventory["campaigns"]
    }
    for row in inventory["keywords"]:
        if row["negative"] or not row["keyword"]:
            continue
        geos, langs = campaign_scope_by_id.get(int(row["campaign_id"]), (set(), set()))
        for geo in geos:
            for lang in langs:
                key = (geo, lang, row["keyword"].strip().lower(), row["match_type"].upper())
                existing_keywords[key].append(
                    f"{row['campaign_id']}:{row['campaign']}:{row['ad_group']}:{row['campaign_status']}:{row['ad_group_status']}:{row['keyword_status']}"
                )

    output = []
    for row in candidates.values():
        existing_key = (row["geo_target_id"], row["language_id"], row["keyword"].strip().lower(), row["match_type"])
        same_scope_campaigns = campaign_lookup.get((row["geo_target_id"], row["language_id"]), [])
        existing_refs = existing_keywords.get(existing_key, [])
        row["existing_campaigns_same_geo_language"] = "|".join(same_scope_campaigns)
        row["existing_keyword_refs"] = "|".join(existing_refs)
        row["duplicate_status"] = "EXISTS_IN_ACCOUNT_DO_NOT_DUPLICATE" if existing_refs else "NEW_TO_SCOPE"
        row["structure_action"] = "REUSE_EXISTING_CAMPAIGN_SCOPE" if same_scope_campaigns else "NEW_LANGUAGE_CAMPAIGN_PACKET_NEEDED"
        output.append(row)
    return sorted(output, key=lambda item: (item["country"], item["language_code"], item["theme"], item["keyword"], item["match_type"]))


def fetch_historical_metrics(
    client: Any,
    customer_id: str,
    rows: list[dict[str, Any]],
    delay: float,
    max_retries: int,
) -> list[dict[str, Any]]:
    google_ads_service = client.get_service("GoogleAdsService")
    service = client.get_service("KeywordPlanIdeaService")
    out: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["geo_target_id"], row["language_id"])].append(row)
    grouped_items = list(grouped.items())
    for group_index, ((geo_id, language_id), group_rows) in enumerate(grouped_items):
        request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
        request.customer_id = customer_id
        request.language = google_ads_service.language_constant_path(language_id)
        request.geo_target_constants.append(google_ads_service.geo_target_constant_path(geo_id))
        request.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        request.keywords.extend(sorted({row["keyword"] for row in group_rows}))
        response = None
        for attempt in range(max_retries + 1):
            try:
                response = service.generate_keyword_historical_metrics(request=request)
                break
            except Exception as exc:
                retryable = "Retry in" in str(exc) or exc.__class__.__name__ == "ResourceExhausted"
                if attempt >= max_retries or not retryable:
                    for row in group_rows:
                        out.append(
                            {
                                "market_key": row["market_key"],
                                "country": row["country"],
                                "language_code": row["language_code"],
                                "geo_target_id": geo_id,
                                "language_id": language_id,
                                "keyword": row["keyword"],
                                "match_type": row["match_type"],
                                "historical_error": f"{exc.__class__.__name__}: {exc}",
                            }
                        )
                    response = None
                    break
                time.sleep(max(delay, 5.0))
        if response is None:
            continue
        by_keyword = {result.text.lower(): result for result in response.results}
        for row in group_rows:
            result = by_keyword.get(row["keyword"].lower())
            metrics = getattr(result, "keyword_metrics", None) if result else None
            monthly: dict[str, str] = {}
            if metrics:
                for volume in metrics.monthly_search_volumes:
                    monthly[f"searches_{volume.year}_{month_name(volume.month)}"] = str(volume.monthly_searches)
            out.append(
                {
                    "market_key": row["market_key"],
                    "country": row["country"],
                    "language_code": row["language_code"],
                    "geo_target_id": geo_id,
                    "language_id": language_id,
                    "keyword": row["keyword"],
                    "match_type": row["match_type"],
                    "avg_monthly_searches": str(getattr(metrics, "avg_monthly_searches", "") or "") if metrics else "",
                    "competition": competition_name(getattr(metrics, "competition", "") if metrics else ""),
                    "competition_index": str(getattr(metrics, "competition_index", "") or "") if metrics else "",
                    "low_top_of_page_bid_usd": micros_to_usd(getattr(metrics, "low_top_of_page_bid_micros", 0) if metrics else 0),
                    "high_top_of_page_bid_usd": micros_to_usd(getattr(metrics, "high_top_of_page_bid_micros", 0) if metrics else 0),
                    "monthly_search_volumes_json": json.dumps(monthly, sort_keys=True),
                    "historical_match_type_note": "Historical endpoint is keyword-level only; requested match type is retained for joining.",
                }
            )
        if delay > 0 and group_index < len(grouped_items) - 1:
            time.sleep(delay)
    return out


def build_campaign_to_forecast(client: Any, google_ads_service: Any, row: dict[str, Any]):
    campaign = client.get_type("CampaignToForecast")
    campaign.bidding_strategy.manual_cpc_bidding_strategy.max_cpc_bid_micros = MAX_CPC_MICROS
    campaign.geo_target_constants.append(google_ads_service.geo_target_constant_path(row["geo_target_id"]))
    campaign.language_constants.append(google_ads_service.language_constant_path(row["language_id"]))
    forecast_ad_group = client.get_type("ForecastAdGroup")
    keyword = client.get_type("KeywordInfo")
    keyword.text = row["keyword"]
    keyword.match_type = match_type_enum(client, row["match_type"])
    forecast_ad_group.keywords.append(keyword)
    campaign.ad_groups.append(forecast_ad_group)
    return campaign


def fetch_forecast_metrics(
    client: Any,
    customer_id: str,
    rows: list[dict[str, Any]],
    forecast_days: int,
    delay: float,
    max_retries: int,
) -> list[dict[str, Any]]:
    google_ads_service = client.get_service("GoogleAdsService")
    service = client.get_service("KeywordPlanIdeaService")
    tomorrow = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=forecast_days)
    out: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        request = client.get_type("GenerateKeywordForecastMetricsRequest")
        request.customer_id = customer_id
        request.campaign = build_campaign_to_forecast(client, google_ads_service, row)
        request.forecast_period.start_date = tomorrow.strftime("%Y-%m-%d")
        request.forecast_period.end_date = end_date.strftime("%Y-%m-%d")
        response = None
        for attempt in range(max_retries + 1):
            try:
                response = service.generate_keyword_forecast_metrics(request=request)
                break
            except Exception as exc:
                retryable = "Retry in" in str(exc) or exc.__class__.__name__ == "ResourceExhausted"
                if attempt >= max_retries or not retryable:
                    out.append(
                        {
                            "market_key": row["market_key"],
                            "country": row["country"],
                            "language_code": row["language_code"],
                            "geo_target_id": row["geo_target_id"],
                            "language_id": row["language_id"],
                            "keyword": row["keyword"],
                            "match_type": row["match_type"],
                            "max_cpc_bid_micros": str(MAX_CPC_MICROS),
                            "forecast_error": f"{exc.__class__.__name__}: {exc}",
                        }
                    )
                    response = None
                    break
                time.sleep(max(delay, 5.0))
        if response is not None:
            metrics = response.campaign_forecast_metrics
            avg_cpc = getattr(metrics, "average_cpc_micros", 0) or 0
            cost = getattr(metrics, "cost_micros", 0) or 0
            avg_cpa = getattr(metrics, "average_cpa_micros", 0) or 0
            out.append(
                {
                    "market_key": row["market_key"],
                    "country": row["country"],
                    "language_code": row["language_code"],
                    "geo_target_id": row["geo_target_id"],
                    "language_id": row["language_id"],
                    "keyword": row["keyword"],
                    "match_type": row["match_type"],
                    "max_cpc_bid_micros": str(MAX_CPC_MICROS),
                    "max_cpc_usd": f"{MAX_CPC_USD:.2f}",
                    "forecast_start_date": request.forecast_period.start_date,
                    "forecast_end_date": request.forecast_period.end_date,
                    "forecast_clicks": str(getattr(metrics, "clicks", "") or 0),
                    "forecast_cost_usd": micros_to_usd(cost),
                    "forecast_average_cpc_usd": micros_to_usd(avg_cpc),
                    "forecast_conversions": str(getattr(metrics, "conversions", "") or 0),
                    "forecast_average_cpa_usd": micros_to_usd(avg_cpa),
                    "forecast_note": "Single-keyword read-only forecast at explicit max_cpc_bid_micros=150000.",
                }
            )
        if delay > 0 and index < len(rows) - 1:
            time.sleep(delay)
    return out


def join_decisions(
    candidates: list[dict[str, Any]],
    historical: list[dict[str, Any]],
    forecasts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hist_by_key = {(r["market_key"], r["keyword"].lower(), r["match_type"].upper()): r for r in historical}
    forecast_by_key = {(r["market_key"], r["keyword"].lower(), r["match_type"].upper()): r for r in forecasts}
    rows = []
    for row in candidates:
        key = (row["market_key"], row["keyword"].lower(), row["match_type"].upper())
        hist = hist_by_key.get(key, {})
        fc = forecast_by_key.get(key, {})
        clicks = float(fc.get("forecast_clicks") or 0)
        avg_cpc = float(fc.get("forecast_average_cpc_usd") or 0)
        low_top = float(hist.get("low_top_of_page_bid_usd") or 0)
        avg_searches = int(float(hist.get("avg_monthly_searches") or 0))
        if row["duplicate_status"] == "EXISTS_IN_ACCOUNT_DO_NOT_DUPLICATE":
            decision = "existing_keyword_repair_or_hold_no_duplicate"
        elif clicks > 0:
            decision = "launch_candidate_after_landing_native_review"
        elif avg_searches > 0:
            decision = "hold_historical_demand_but_zero_click_forecast_at_015"
        else:
            decision = "hold_no_demand_seen_at_015"
        if low_top and low_top <= MAX_CPC_USD:
            cpc_gate = "low_top_of_page_at_or_below_015"
        elif avg_cpc and avg_cpc <= MAX_CPC_USD and clicks > 0:
            cpc_gate = "forecast_clicks_at_015_but_top_of_page_likely_higher"
        else:
            cpc_gate = "not_proven_cheap_enough_for_live"
        rows.append(
            {
                **row,
                **{f"historical_{k}": v for k, v in hist.items() if k not in {"market_key", "keyword", "match_type", "country", "language_code", "geo_target_id", "language_id"}},
                **{f"forecast_{k}": v for k, v in fc.items() if k not in {"market_key", "keyword", "match_type", "country", "language_code", "geo_target_id", "language_id"}},
                "decision": decision,
                "cpc_gate": cpc_gate,
            }
        )
    return rows


def summarize(inventory: dict[str, list[dict[str, Any]]], candidates: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, Any]:
    by_market: dict[str, dict[str, Any]] = {}
    for market, rows in defaultdict(list, {m: [r for r in decisions if r["market_key"] == m] for m in {r["market_key"] for r in decisions}}).items():
        by_market[market] = {
            "candidate_rows": len(rows),
            "new_to_scope": sum(1 for r in rows if r["duplicate_status"] == "NEW_TO_SCOPE"),
            "existing_keywords": sum(1 for r in rows if r["duplicate_status"] == "EXISTS_IN_ACCOUNT_DO_NOT_DUPLICATE"),
            "forecast_click_rows": sum(1 for r in rows if float(r.get("forecast_forecast_clicks") or 0) > 0),
            "low_top_at_or_below_015": sum(1 for r in rows if r["cpc_gate"] == "low_top_of_page_at_or_below_015"),
            "launch_candidates": sum(1 for r in rows if r["decision"] == "launch_candidate_after_landing_native_review"),
        }
    campaign_counter = Counter(row["status"] for row in inventory["campaigns"] if row["channel"] == "SEARCH")
    return {
        "generated_at_utc": now_stamp(),
        "guardrail": "read_only_google_ads_api_forecast_and_inventory_no_mutations",
        "max_cpc_bid_micros": MAX_CPC_MICROS,
        "max_cpc_usd": f"{MAX_CPC_USD:.2f}",
        "live_search_campaign_status_counts": dict(campaign_counter),
        "live_campaign_rows": len(inventory["campaigns"]),
        "live_keyword_rows": len(inventory["keywords"]),
        "candidate_rows": len(candidates),
        "decision_rows": len(decisions),
        "markets": by_market,
    }


def write_report(path: Path, summary: dict[str, Any]) -> None:
    market_lines = []
    for market, stats in sorted(summary["markets"].items()):
        market_lines.append(
            f"| `{market}` | {stats['candidate_rows']} | {stats['new_to_scope']} | {stats['existing_keywords']} | {stats['forecast_click_rows']} | {stats['low_top_at_or_below_015']} | {stats['launch_candidates']} |"
        )
    text = f"""# Multimarket Search Forecast And Duplicate Audit

Generated UTC: `{summary['generated_at_utc']}`

Guardrail: `{summary['guardrail']}`

Max CPC tested: `{summary['max_cpc_usd']}` (`{summary['max_cpc_bid_micros']}` micros)

## What This Proves

- This is read-only Google Ads API evidence, not a live build.
- Existing campaign and keyword scope was read before building expansion rows.
- Candidate rows are separated by country and language so future approval packets can reuse existing campaigns where appropriate and create new language campaigns only where no matching scope exists.

## Live Account Inventory Summary

- Live campaign rows read: `{summary['live_campaign_rows']}`
- Live keyword rows read: `{summary['live_keyword_rows']}`
- Search campaign status counts: `{summary['live_search_campaign_status_counts']}`

## Forecast Summary By Market/Language

| Market | Rows | New To Scope | Existing Keywords | Rows With Forecast Clicks | Low Top Bid <= $0.15 | Launch Candidates After Review |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(market_lines)}

## Files

- `live_campaign_inventory.csv`
- `live_campaign_criteria_inventory.csv`
- `live_ad_group_inventory.csv`
- `live_keyword_inventory.csv`
- `live_campaign_metrics_last_30d.csv`
- `multimarket_keyword_candidate_matrix.csv`
- `multimarket_historical_rows.csv`
- `multimarket_forecast_rows.csv`
- `multimarket_joined_decision_rows.csv`
- `multimarket_forecast_summary.json`

## Next Use

Use `multimarket_joined_decision_rows.csv` to build small market/language-specific approval packets. Do not upload duplicate keywords; rows marked `EXISTS_IN_ACCOUNT_DO_NOT_DUPLICATE` should repair or hold the existing structure instead.
"""
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer-id", default=CUSTOMER_ID)
    parser.add_argument("--config-path")
    parser.add_argument("--forecast-days", type=int, default=30)
    parser.add_argument("--historical-delay-seconds", type=float, default=5.0)
    parser.add_argument("--historical-max-retries", type=int, default=4)
    parser.add_argument("--forecast-delay-seconds", type=float, default=0.15)
    parser.add_argument("--forecast-max-retries", type=int, default=3)
    parser.add_argument("--markets", default="", help="Comma-separated market_key filter, e.g. US_ES,CA_FR,GB_EN")
    parser.add_argument("--output-prefix", default="multimarket", help="Prefix for generated forecast/decision files")
    parser.add_argument("--reuse-historical", action="store_true", help="Reuse existing multimarket_historical_rows.csv")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-forecast", action="store_true")
    args = parser.parse_args()

    customer_id = normalize_customer_id(args.customer_id)
    client = load_client(args.config_path)
    inventory = fetch_live_inventory(client, customer_id)
    write_csv(PACKET_DIR / "live_campaign_inventory.csv", inventory["campaigns"])
    write_csv(PACKET_DIR / "live_campaign_criteria_inventory.csv", inventory["campaign_criteria"])
    write_csv(PACKET_DIR / "live_ad_group_inventory.csv", inventory["ad_groups"])
    write_csv(PACKET_DIR / "live_keyword_inventory.csv", inventory["keywords"])
    write_csv(PACKET_DIR / "live_campaign_metrics_last_30d.csv", inventory["metrics"])

    all_candidates = build_candidate_matrix(inventory)
    write_csv(PACKET_DIR / "multimarket_keyword_candidate_matrix.csv", all_candidates)
    candidates = all_candidates
    market_filter = {item.strip() for item in args.markets.split(",") if item.strip()}
    if market_filter:
        candidates = [row for row in candidates if row["market_key"] in market_filter]
        write_csv(PACKET_DIR / f"{args.output_prefix}_keyword_candidate_matrix.csv", candidates)

    if args.dry_run:
        summary = {
            "mode": "dry_run",
            "guardrail": "read_only_inventory_and_candidate_generation_no_forecast",
            "candidate_rows": len(candidates),
        "markets": dict(Counter(row["market_key"] for row in candidates)),
        "market_filter": sorted(market_filter),
        }
        write_json(PACKET_DIR / "multimarket_forecast_summary.json", summary)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    if args.skip_forecast:
        historical: list[dict[str, Any]] = []
        forecasts: list[dict[str, Any]] = []
    else:
        if args.reuse_historical and (PACKET_DIR / "multimarket_historical_rows.csv").exists():
            historical = [
                row
                for row in read_csv(PACKET_DIR / "multimarket_historical_rows.csv")
                if not market_filter or row["market_key"] in market_filter
            ]
        else:
            historical = fetch_historical_metrics(
                client,
                customer_id,
                candidates,
                args.historical_delay_seconds,
                args.historical_max_retries,
            )
            write_csv(PACKET_DIR / "multimarket_historical_rows.csv", historical)
        forecasts = fetch_forecast_metrics(
            client,
            customer_id,
            candidates,
            args.forecast_days,
            args.forecast_delay_seconds,
            args.forecast_max_retries,
        )
        forecast_path = PACKET_DIR / f"{args.output_prefix}_forecast_rows.csv"
        write_csv(forecast_path, forecasts)

    decisions = join_decisions(candidates, historical, forecasts)
    decision_path = PACKET_DIR / f"{args.output_prefix}_joined_decision_rows.csv"
    write_csv(decision_path, decisions)
    summary = summarize(inventory, candidates, decisions)
    summary["market_filter"] = sorted(market_filter)
    summary["forecast_rows_file"] = str(PACKET_DIR / f"{args.output_prefix}_forecast_rows.csv")
    summary["decision_rows_file"] = str(decision_path)
    write_json(PACKET_DIR / f"{args.output_prefix}_forecast_summary.json", summary)
    write_report(PACKET_DIR / f"{args.output_prefix.upper()}_SEARCH_FORECAST_AND_DUPLICATE_AUDIT.md", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
