#!/usr/bin/env python3
"""Run the GB/CA/AU $0.15 CPC gate through Google Ads API forecasts.

This script is read-only. It calls KeywordPlanIdeaService forecast APIs and
writes local CSV/JSON evidence; it does not create, upload, mutate, or enable
any Google Ads object.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


PACKET_DIR = Path(__file__).resolve().parent
MATRIX_CSV = PACKET_DIR / "gb_ca_au_36_keyword_planner_validation_matrix.csv"
DEFAULT_OUTPUT_CSV = PACKET_DIR / "google_ads_api_cpc_forecast_rows.csv"
DEFAULT_SUMMARY_JSON = PACKET_DIR / "google_ads_api_cpc_forecast_summary.json"
MAX_CPC_USD = 0.15
MAX_CPC_MICROS = int(MAX_CPC_USD * 1_000_000)
SECURE_CONFIG_PATH = Path.home() / ".config/dresslikemommy/google-ads-api/google-ads.yaml"
DEFAULT_CONFIG_PATH = Path.home() / "google-ads.yaml"

MARKET_GEO_TARGET_IDS = {
    "AU": "2036",
    "CA": "2124",
    "GB": "2826",
}
MARKET_LANGUAGE_IDS = {
    "AU": "1000",
    "CA": "1000",
    "GB": "1000",
}


def read_matrix(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_customer_id(value: str) -> str:
    return value.replace("-", "").strip()


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
            "install the official google-ads Python client in the account-capable runtime."
        ) from exc

    discovered_config_path = discover_config_path(config_path)
    if not discovered_config_path:
        raise SystemExit(
            "GOOGLE_ADS_API_CONFIG_MISSING: no Google Ads API config file found. "
            f"Checked GOOGLE_ADS_CONFIGURATION_FILE_PATH, {SECURE_CONFIG_PATH}, and {DEFAULT_CONFIG_PATH}. "
            "Run `python3.13 ops/scripts/check_google_ads_api_config.py --write-template`, then create "
            f"{SECURE_CONFIG_PATH} outside the repo with developer_token, client_id, client_secret, "
            "refresh_token, and optional login_customer_id."
        )
    return GoogleAdsClient.load_from_storage(path=str(discovered_config_path))


def match_type_enum(client, value: str):
    match = value.strip().upper()
    if match == "EXACT":
        return client.enums.KeywordMatchTypeEnum.EXACT
    if match == "PHRASE":
        return client.enums.KeywordMatchTypeEnum.PHRASE
    raise ValueError(f"unsupported match type for strict gate: {value}")


def build_campaign_to_forecast(client, google_ads_service, row: dict[str, str]):
    market = row["market"].upper()
    campaign = client.get_type("CampaignToForecast")
    campaign.bidding_strategy.manual_cpc_bidding_strategy.max_cpc_bid_micros = MAX_CPC_MICROS

    campaign.geo_target_constants.append(
        google_ads_service.geo_target_constant_path(MARKET_GEO_TARGET_IDS[market])
    )
    campaign.language_constants.append(
        google_ads_service.language_constant_path(MARKET_LANGUAGE_IDS[market])
    )

    forecast_ad_group = client.get_type("ForecastAdGroup")
    keyword = client.get_type("KeywordInfo")
    keyword.text = row["keyword"]
    keyword.match_type = match_type_enum(client, row["match_type_to_validate"])
    forecast_ad_group.keywords.append(keyword)
    campaign.ad_groups.append(forecast_ad_group)
    return campaign


def metrics_to_output_row(source_row: dict[str, str], metrics) -> dict[str, str]:
    average_cpc_micros = getattr(metrics, "average_cpc_micros", 0) or 0
    avg_cpc = average_cpc_micros / 1_000_000 if average_cpc_micros else 0
    return {
        "market": source_row["market"],
        "keyword": source_row["keyword"],
        "match_type": source_row["match_type_to_validate"],
        "avg_cpc": f"{avg_cpc:.6f}" if average_cpc_micros else "0.000000",
        "first_page_cpc": "",
        "top_of_page_cpc": "",
        "forecast_clicks": str(getattr(metrics, "clicks", "") or 0),
        "forecast_impressions": str(getattr(metrics, "impressions", "") or 0),
        "policy_status": "",
        "auction_status": "API_FORECAST",
        "notes": "Google Ads API single-keyword forecast at max CPC $0.15",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "market",
        "keyword",
        "match_type",
        "avg_cpc",
        "first_page_cpc",
        "top_of_page_cpc",
        "forecast_clicks",
        "forecast_impressions",
        "policy_status",
        "auction_status",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def dry_run_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    return {
        "mode": "dry_run",
        "matrix_csv": str(MATRIX_CSV),
        "source_rows": len(rows),
        "markets": dict(sorted(Counter(row["market"] for row in rows).items())),
        "match_types": dict(sorted(Counter(row["match_type_to_validate"] for row in rows).items())),
        "max_cpc_micros": MAX_CPC_MICROS,
        "geo_target_ids": MARKET_GEO_TARGET_IDS,
        "language_ids": MARKET_LANGUAGE_IDS,
        "guardrail": "read_only_forecast_only_no_google_ads_mutation",
    }


def run_forecasts(args: argparse.Namespace) -> dict[str, object]:
    rows = read_matrix(args.matrix_csv)
    if args.dry_run:
        summary = dry_run_summary(rows)
        args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2))
        return summary

    customer_id = normalize_customer_id(
        args.customer_id or os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "")
    )
    if not customer_id:
        raise SystemExit(
            "AUTOMATION_CAPABILITY_MISMATCH: GOOGLE_ADS_CUSTOMER_ID is unset and "
            "--customer-id was not supplied."
        )

    client = load_client(args.config_path)
    google_ads_service = client.get_service("GoogleAdsService")
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    output_rows: list[dict[str, str]] = []
    tomorrow = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=args.forecast_days)
    for row in rows:
        request = client.get_type("GenerateKeywordForecastMetricsRequest")
        request.customer_id = customer_id
        request.campaign = build_campaign_to_forecast(client, google_ads_service, row)
        request.forecast_period.start_date = tomorrow.strftime("%Y-%m-%d")
        request.forecast_period.end_date = end_date.strftime("%Y-%m-%d")
        response = keyword_plan_idea_service.generate_keyword_forecast_metrics(request=request)
        output_rows.append(metrics_to_output_row(row, response.campaign_forecast_metrics))

    write_csv(args.output_csv, output_rows)
    summary = {
        "mode": "api_forecast",
        "output_csv": str(args.output_csv),
        "source_rows": len(rows),
        "forecast_rows": len(output_rows),
        "markets": dict(sorted(Counter(row["market"] for row in rows).items())),
        "match_types": dict(sorted(Counter(row["match_type_to_validate"] for row in rows).items())),
        "max_cpc_micros": MAX_CPC_MICROS,
        "forecast_days": args.forecast_days,
        "next_command": (
            "python3.13 "
            "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/"
            "validate_keyword_planner_forecast_export.py --forecast-csv "
            f"{args.output_csv}"
        ),
        "guardrail": "read_only_forecast_only_no_google_ads_mutation",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-csv", type=Path, default=MATRIX_CSV)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON)
    parser.add_argument("--customer-id")
    parser.add_argument("--config-path")
    parser.add_argument("--forecast-days", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_forecasts(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
