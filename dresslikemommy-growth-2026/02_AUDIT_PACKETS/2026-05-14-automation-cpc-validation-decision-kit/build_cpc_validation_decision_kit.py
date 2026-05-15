#!/usr/bin/env python3
"""Build a no-upload decision kit for the GB/CA/AU $0.15 CPC gate."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PACKET = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-14-automation-36-row-cpc-canonical-url-packet/"
    "gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv"
)
PACKET_DIR = Path(__file__).resolve().parent
MAX_CPC = 0.15


def read_source_rows() -> list[dict[str, str]]:
    with SOURCE_PACKET.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_keyword_planner_inputs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["market"]].append(row)

    for market, market_rows in sorted(grouped.items()):
        market_rows = sorted(market_rows, key=lambda r: (r["total_score"], r["keyword"]), reverse=True)
        exact_keywords = [r["keyword"].strip() for r in market_rows]
        phrase_keywords = [r["keyword"].strip() for r in market_rows]

        write_text(PACKET_DIR / f"keyword_planner_input_{market.lower()}_exact.txt", "\n".join(exact_keywords) + "\n")
        write_text(PACKET_DIR / f"keyword_planner_input_{market.lower()}_phrase.txt", "\n".join(phrase_keywords) + "\n")

        for row in market_rows:
            output_rows.append(
                {
                    "market": row["market"],
                    "language": row["language"],
                    "campaign_id": row["campaign_id"],
                    "ad_group_id": row["ad_group_id"],
                    "keyword": row["keyword"],
                    "match_type_to_validate": "exact",
                    "max_cpc_usd": f"{MAX_CPC:.2f}",
                    "final_url": row["final_url_to_validate"],
                    "source_total_score": row["total_score"],
                    "source_category": row["category"],
                    "validation_status": "AUTH_EXPORT_REQUIRED",
                }
            )
            output_rows.append(
                {
                    "market": row["market"],
                    "language": row["language"],
                    "campaign_id": row["campaign_id"],
                    "ad_group_id": row["ad_group_id"],
                    "keyword": row["keyword"],
                    "match_type_to_validate": "phrase",
                    "max_cpc_usd": f"{MAX_CPC:.2f}",
                    "final_url": row["final_url_to_validate"],
                    "source_total_score": row["total_score"],
                    "source_category": row["category"],
                    "validation_status": "AUTH_EXPORT_REQUIRED",
                }
            )

    return output_rows


def build_forecast_template(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    template_rows: list[dict[str, str]] = []
    for row in rows:
        template_rows.append(
            {
                "market": row["market"],
                "keyword": row["keyword"],
                "match_type": "",
                "avg_cpc": "",
                "first_page_cpc": "",
                "top_of_page_cpc": "",
                "forecast_clicks": "",
                "forecast_impressions": "",
                "policy_status": "",
                "auction_status": "",
                "notes": "",
            }
        )
    return template_rows


def report(rows: list[dict[str, str]], validation_rows: list[dict[str, str]]) -> str:
    by_market = Counter(row["market"] for row in rows)
    by_route = Counter(row["landing_route"] for row in rows)
    lines = [
        "# GB/CA/AU CPC Validation Decision Kit",
        "",
        f"Timestamp: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "Scope: repo-local Keyword Planner input and future forecast-export parser prep for the existing canonical 36-row GB/CA/AU CPC validation packet. No Google Ads upload/apply/add keyword/bid/budget/status/negative action occurred.",
        "",
        "## Result",
        "",
        f"- Source rows: `{len(rows)}`",
        f"- Markets: `{dict(sorted(by_market.items()))}`",
        f"- Keyword Planner validation rows: `{len(validation_rows)}` (`exact` plus `phrase` for each source row)",
        f"- Hard max CPC gate: `${MAX_CPC:.2f}`",
        "- Decision state: `AUTHENTICATED_FORECAST_EXPORT_REQUIRED`",
        "",
        "## Generated Inputs",
        "",
        "- `keyword_planner_input_au_exact.txt` and `keyword_planner_input_au_phrase.txt`",
        "- `keyword_planner_input_ca_exact.txt` and `keyword_planner_input_ca_phrase.txt`",
        "- `keyword_planner_input_gb_exact.txt` and `keyword_planner_input_gb_phrase.txt`",
        "- `gb_ca_au_36_keyword_planner_validation_matrix.csv`",
        "- `keyword_planner_forecast_export_template.csv`",
        "- `validate_keyword_planner_forecast_export.py`",
        "- `run_google_ads_api_cpc_forecast.py`",
        "- `GOOGLE_ADS_API_CPC_FORECAST_RETRY_HARNESS.md`",
        "",
        "## Route Scope",
        "",
    ]
    for route, count in sorted(by_route.items()):
        lines.append(f"- `{route}`: `{count}` source rows")
    lines.extend(
        [
            "",
            "## Exact Next Gate",
            "",
            "In an authenticated Google Ads / Keyword Planner session, validate these keywords at max CPC `$0.15`. Export the forecast/readback columns into a CSV shaped like `keyword_planner_forecast_export_template.csv`, then run:",
            "",
            "```bash",
            "python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/validate_keyword_planner_forecast_export.py --forecast-csv /path/to/authenticated-forecast-export.csv",
            "```",
            "",
            "If the UI cannot produce explicit GB/CA/AU, exact/phrase, max `$0.15`, keyword-level rows, use the read-only Google Ads API harness instead:",
            "",
            "```bash",
            "python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py --customer-id 3990976848",
            "python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/validate_keyword_planner_forecast_export.py --forecast-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/google_ads_api_cpc_forecast_rows.csv",
            "```",
            "",
            "Only rows classified `PASS_015_CPC_GATE` may become a fresh `GREEN` action-queue row, and only after fresh Ads before-state readback, reviewer pass, anti-cannibalization check, and after-state readback plan. Rows classified `FAIL_015_CPC_GATE`, `LOW_VOLUME_OR_NO_AUCTION`, `POLICY_OR_DESTINATION_BLOCK`, or `MISSING_REQUIRED_FORECAST_DATA` must stay local and must not be uploaded.",
            "",
            "## Guardrails",
            "",
            "- This kit is not an upload file.",
            "- Do not raise bids above `$0.15`.",
            "- Do not upload head or close-head variants that already failed the hard CPC economics.",
            "- Do not add negatives, change budgets, change statuses, alter conversion settings, or mutate feeds/products from this packet.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = read_source_rows()
    validation_rows = build_keyword_planner_inputs(rows)
    validation_fieldnames = [
        "market",
        "language",
        "campaign_id",
        "ad_group_id",
        "keyword",
        "match_type_to_validate",
        "max_cpc_usd",
        "final_url",
        "source_total_score",
        "source_category",
        "validation_status",
    ]
    write_csv(PACKET_DIR / "gb_ca_au_36_keyword_planner_validation_matrix.csv", validation_rows, validation_fieldnames)

    template_rows = build_forecast_template(rows)
    write_csv(
        PACKET_DIR / "keyword_planner_forecast_export_template.csv",
        template_rows,
        [
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
        ],
    )

    summary = {
        "source_csv": str(SOURCE_PACKET.relative_to(ROOT)),
        "source_row_count": len(rows),
        "validation_row_count": len(validation_rows),
        "markets": dict(sorted(Counter(row["market"] for row in rows).items())),
        "routes": dict(sorted(Counter(row["landing_route"] for row in rows).items())),
        "max_cpc_usd": MAX_CPC,
        "decision_state": "AUTHENTICATED_FORECAST_EXPORT_REQUIRED",
    }
    write_text(PACKET_DIR / "gb_ca_au_cpc_validation_decision_kit_summary.json", json.dumps(summary, indent=2) + "\n")
    write_text(PACKET_DIR / "GB_CA_AU_CPC_VALIDATION_DECISION_KIT.md", report(rows, validation_rows))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
