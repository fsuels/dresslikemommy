#!/usr/bin/env python3
"""Run Dress Like Mommy US Search keyword historical + forecast export.

This script is read-only. It calls Google Ads API KeywordPlanIdeaService for
historical metrics and single-keyword forecast metrics. It does not create,
upload, mutate, enable, pause, or delete any Google Ads object.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
DEFAULT_MATRIX_CSV = PACKET_DIR / "keyword_source_matrix.csv"
DEFAULT_FORECAST_CSV = PACKET_DIR / "google_ads_api_us_search_forecast_rows.csv"
DEFAULT_HISTORICAL_CSV = PACKET_DIR / "google_ads_api_us_search_historical_rows.csv"
DEFAULT_SUMMARY_JSON = PACKET_DIR / "google_ads_api_us_search_keyword_summary.json"
SECURE_CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
DEFAULT_CONFIG_PATH = Path.home() / "google-ads.yaml"

US_GEO_TARGET_ID = "2840"
ENGLISH_LANGUAGE_ID = "1000"
MAX_CPC_USD = 0.20
MAX_CPC_MICROS = int(MAX_CPC_USD * 1_000_000)


def normalize_customer_id(value: str) -> str:
    return value.replace("-", "").strip()


def read_matrix(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {"ad_group", "keyword", "requested_match_type"}
    missing = required - set(rows[0] if rows else {})
    if missing:
        raise SystemExit(f"MATRIX_SCHEMA_MISMATCH: missing columns {sorted(missing)} in {path}")
    return rows


def discover_config_path(config_path: str | None) -> Path | None:
    candidates: list[Path] = []
    if config_path:
        candidates.append(Path(config_path).expanduser())
    if os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH"):
        candidates.append(Path(os.environ["GOOGLE_ADS_CONFIGURATION_FILE_PATH"]).expanduser())
    candidates.extend([SECURE_CONFIG_PATH, DEFAULT_CONFIG_PATH])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_client(config_path: str | None):
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "AUTOMATION_CAPABILITY_MISMATCH: google.ads.googleads is not installed; "
            "use the account-capable runtime with the official google-ads Python client."
        ) from exc

    discovered_config_path = discover_config_path(config_path)
    if not discovered_config_path:
        raise SystemExit(
            "GOOGLE_ADS_API_CONFIG_MISSING: no Google Ads API config file found. "
            f"Checked GOOGLE_ADS_CONFIGURATION_FILE_PATH, {SECURE_CONFIG_PATH}, and {DEFAULT_CONFIG_PATH}."
        )
    return GoogleAdsClient.load_from_storage(path=str(discovered_config_path))


def match_type_enum(client: Any, value: str):
    match = value.strip().upper()
    if match == "EXACT":
        return client.enums.KeywordMatchTypeEnum.EXACT
    if match == "PHRASE":
        return client.enums.KeywordMatchTypeEnum.PHRASE
    raise ValueError(f"unsupported match type for strict gate: {value}")


def month_name(month_enum_value: Any) -> str:
    month_by_enum_value = {
        2: "january",
        3: "february",
        4: "march",
        5: "april",
        6: "may",
        7: "june",
        8: "july",
        9: "august",
        10: "september",
        11: "october",
        12: "november",
        13: "december",
    }
    if isinstance(month_enum_value, int):
        return month_by_enum_value.get(month_enum_value, str(month_enum_value))
    raw = str(month_enum_value)
    if raw.isdigit():
        return month_by_enum_value.get(int(raw), raw)
    if "." in raw:
        return raw.rsplit(".", 1)[-1].lower()
    return raw.lower()


def micros_to_usd(value: int | None) -> str:
    if not value:
        return ""
    return f"{value / 1_000_000:.6f}"


def competition_name(value: Any) -> str:
    competition_by_enum_value = {
        2: "LOW",
        3: "MEDIUM",
        4: "HIGH",
    }
    if value in ("", None):
        return ""
    if isinstance(value, int):
        return competition_by_enum_value.get(value, str(value))
    raw = str(value)
    if raw.isdigit():
        return competition_by_enum_value.get(int(raw), raw)
    if "." in raw:
        return raw.rsplit(".", 1)[-1]
    return raw


def build_campaign_to_forecast(client: Any, google_ads_service: Any, row: dict[str, str]):
    campaign = client.get_type("CampaignToForecast")
    campaign.bidding_strategy.manual_cpc_bidding_strategy.max_cpc_bid_micros = MAX_CPC_MICROS
    campaign.geo_target_constants.append(google_ads_service.geo_target_constant_path(US_GEO_TARGET_ID))
    campaign.language_constants.append(google_ads_service.language_constant_path(ENGLISH_LANGUAGE_ID))

    forecast_ad_group = client.get_type("ForecastAdGroup")
    keyword = client.get_type("KeywordInfo")
    keyword.text = row["keyword"]
    keyword.match_type = match_type_enum(client, row["requested_match_type"])
    forecast_ad_group.keywords.append(keyword)
    campaign.ad_groups.append(forecast_ad_group)
    return campaign


def dry_run_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "mode": "dry_run",
        "source_rows": len(rows),
        "unique_keywords": len({row["keyword"] for row in rows}),
        "ad_groups": dict(sorted(Counter(row["ad_group"] for row in rows).items())),
        "match_types": dict(sorted(Counter(row["requested_match_type"] for row in rows).items())),
        "geo_target_id": US_GEO_TARGET_ID,
        "language_id": ENGLISH_LANGUAGE_ID,
        "keyword_plan_network": "GOOGLE_SEARCH",
        "max_cpc_bid_micros": MAX_CPC_MICROS,
        "guardrail": "read_only_keyword_plan_export_only_no_google_ads_mutation",
    }


def google_ads_exception_summary(exc: Exception) -> dict[str, Any]:
    request_id = getattr(exc, "request_id", "")
    failure = getattr(exc, "failure", None)
    errors: list[dict[str, str]] = []
    if failure:
        for error in getattr(failure, "errors", []):
            errors.append(
                {
                    "error_code": str(getattr(error, "error_code", "")),
                    "message": str(getattr(error, "message", "")),
                }
            )
    return {
        "status": "blocked",
        "request_id": request_id,
        "errors": errors,
        "exception_class": exc.__class__.__name__,
        "exception_message": str(exc),
        "guardrail": "read_only_keyword_plan_export_only_no_google_ads_mutation",
    }


def fetch_historical_metrics(client: Any, customer_id: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    google_ads_service = client.get_service("GoogleAdsService")
    service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = customer_id
    request.language = google_ads_service.language_constant_path(ENGLISH_LANGUAGE_ID)
    request.geo_target_constants.append(google_ads_service.geo_target_constant_path(US_GEO_TARGET_ID))
    request.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    request.keywords.extend(sorted({row["keyword"] for row in rows}))
    response = service.generate_keyword_historical_metrics(request=request)

    by_keyword: dict[str, Any] = {result.text.lower(): result for result in response.results}
    output: list[dict[str, str]] = []
    for row in rows:
        result = by_keyword.get(row["keyword"].lower())
        metrics = getattr(result, "keyword_metrics", None) if result else None
        monthly: dict[str, str] = {}
        if metrics:
            for volume in metrics.monthly_search_volumes:
                monthly[f"searches_{volume.year}_{month_name(volume.month).lower()}"] = str(
                    volume.monthly_searches
                )
        output.append(
            {
                "ad_group": row["ad_group"],
                "keyword": row["keyword"],
                "requested_match_type": row["requested_match_type"],
                "historical_match_type_note": (
                    "GenerateKeywordHistoricalMetricsRequest has no match_type field; "
                    "match_type is retained from the source table for joining only."
                ),
                "avg_monthly_searches": str(getattr(metrics, "avg_monthly_searches", "") or "")
                if metrics
                else "",
                "competition": competition_name(getattr(metrics, "competition", "") if metrics else ""),
                "competition_index": str(getattr(metrics, "competition_index", "") or "")
                if metrics
                else "",
                "low_top_of_page_bid_usd": micros_to_usd(
                    getattr(metrics, "low_top_of_page_bid_micros", 0) if metrics else 0
                ),
                "high_top_of_page_bid_usd": micros_to_usd(
                    getattr(metrics, "high_top_of_page_bid_micros", 0) if metrics else 0
                ),
                "monthly_search_volumes_json": json.dumps(monthly, sort_keys=True),
                "geo_target_id": US_GEO_TARGET_ID,
                "language_id": ENGLISH_LANGUAGE_ID,
                "keyword_plan_network": "GOOGLE_SEARCH",
            }
        )
    return output


def fetch_forecast_metrics(
    client: Any,
    customer_id: str,
    rows: list[dict[str, str]],
    forecast_days: int,
    request_delay_seconds: float,
    max_retries: int,
) -> list[dict[str, str]]:
    google_ads_service = client.get_service("GoogleAdsService")
    service = client.get_service("KeywordPlanIdeaService")
    output: list[dict[str, str]] = []
    tomorrow = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=forecast_days)
    for row_index, row in enumerate(rows):
        request = client.get_type("GenerateKeywordForecastMetricsRequest")
        request.customer_id = customer_id
        request.campaign = build_campaign_to_forecast(client, google_ads_service, row)
        request.forecast_period.start_date = tomorrow.strftime("%Y-%m-%d")
        request.forecast_period.end_date = end_date.strftime("%Y-%m-%d")
        for attempt in range(max_retries + 1):
            try:
                response = service.generate_keyword_forecast_metrics(request=request)
                break
            except Exception as exc:
                is_last_attempt = attempt >= max_retries
                retryable_quota = "Retry in 5 seconds" in str(exc) or exc.__class__.__name__ == "ResourceExhausted"
                if is_last_attempt or not retryable_quota:
                    raise
                time.sleep(max(request_delay_seconds, 5.0))
        metrics = response.campaign_forecast_metrics
        average_cpc_micros = getattr(metrics, "average_cpc_micros", 0) or 0
        average_cpa_micros = getattr(metrics, "average_cpa_micros", 0) or 0
        cost_micros = getattr(metrics, "cost_micros", 0) or 0
        output.append(
            {
                "ad_group": row["ad_group"],
                "keyword": row["keyword"],
                "match_type": row["requested_match_type"],
                "max_cpc_bid_micros": str(MAX_CPC_MICROS),
                "max_cpc_usd": f"{MAX_CPC_USD:.2f}",
                "forecast_start_date": request.forecast_period.start_date,
                "forecast_end_date": request.forecast_period.end_date,
                "forecast_clicks": str(getattr(metrics, "clicks", "") or 0),
                "forecast_impressions": "",
                "forecast_impressions_note": (
                    "GenerateKeywordForecastMetricsResponse v24 does not return impressions; "
                    "use clicks, cost, average CPC, conversions, and average CPA from this endpoint."
                ),
                "forecast_cost_usd": f"{cost_micros / 1_000_000:.6f}" if cost_micros else "0.000000",
                "forecast_average_cpc_usd": f"{average_cpc_micros / 1_000_000:.6f}"
                if average_cpc_micros
                else "0.000000",
                "forecast_conversions": str(getattr(metrics, "conversions", "") or 0),
                "forecast_average_cpa_usd": f"{average_cpa_micros / 1_000_000:.6f}"
                if average_cpa_micros
                else "0.000000",
                "geo_target_id": US_GEO_TARGET_ID,
                "language_id": ENGLISH_LANGUAGE_ID,
                "keyword_plan_network": "GOOGLE_SEARCH",
                "notes": "Single-keyword read-only forecast at explicit max_cpc_bid_micros=200000",
            }
        )
        if request_delay_seconds > 0 and row_index < len(rows) - 1:
            time.sleep(request_delay_seconds)
    return output


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> dict[str, Any]:
    rows = read_matrix(args.matrix_csv)
    if args.dry_run:
        summary = dry_run_summary(rows)
        args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return summary

    customer_id = normalize_customer_id(args.customer_id or os.environ.get("GOOGLE_ADS_CUSTOMER_ID", ""))
    if not customer_id:
        raise SystemExit("GOOGLE_ADS_CUSTOMER_ID_REQUIRED: supply --customer-id or GOOGLE_ADS_CUSTOMER_ID.")

    try:
        client = load_client(args.config_path)
        historical_rows = fetch_historical_metrics(client, customer_id, rows)
    except Exception as exc:
        summary = dry_run_summary(rows)
        summary.update(google_ads_exception_summary(exc))
        summary["mode"] = "api_historical_attempt_blocked"
        args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return summary

    write_csv(args.historical_csv, historical_rows)

    try:
        forecast_rows = fetch_forecast_metrics(
            client,
            customer_id,
            rows,
            args.forecast_days,
            args.forecast_request_delay_seconds,
            args.forecast_max_retries,
        )
    except Exception as exc:
        summary = dry_run_summary(rows)
        summary.update(google_ads_exception_summary(exc))
        summary.update(
            {
                "mode": "api_historical_complete_forecast_blocked",
                "status": "partial",
                "historical_rows": len(historical_rows),
                "historical_csv": str(args.historical_csv),
                "forecast_rows": 0,
                "forecast_error_stage": "GenerateKeywordForecastMetrics",
            }
        )
        args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return summary

    write_csv(args.forecast_csv, forecast_rows)
    summary = {
        "mode": "api_historical_and_forecast",
        "source_rows": len(rows),
        "historical_rows": len(historical_rows),
        "forecast_rows": len(forecast_rows),
        "historical_csv": str(args.historical_csv),
        "forecast_csv": str(args.forecast_csv),
        "forecast_days": args.forecast_days,
        "geo_target_id": US_GEO_TARGET_ID,
        "language_id": ENGLISH_LANGUAGE_ID,
        "keyword_plan_network": "GOOGLE_SEARCH",
        "max_cpc_bid_micros": MAX_CPC_MICROS,
        "match_types": dict(sorted(Counter(row["requested_match_type"] for row in rows).items())),
        "guardrail": "read_only_keyword_plan_export_only_no_google_ads_mutation",
        "status": "complete",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-csv", type=Path, default=DEFAULT_MATRIX_CSV)
    parser.add_argument("--historical-csv", type=Path, default=DEFAULT_HISTORICAL_CSV)
    parser.add_argument("--forecast-csv", type=Path, default=DEFAULT_FORECAST_CSV)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON)
    parser.add_argument("--customer-id")
    parser.add_argument("--config-path")
    parser.add_argument("--forecast-days", type=int, default=30)
    parser.add_argument("--forecast-max-retries", type=int, default=3)
    parser.add_argument("--forecast-request-delay-seconds", type=float, default=6.0)
    parser.add_argument("--dry-run", action="store_true")
    run(parser.parse_args())
    return 0


if __name__ == "__main__":
    sys.exit(main())
