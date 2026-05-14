#!/usr/bin/env python3
"""Classify authenticated Keyword Planner forecast rows against the $0.15 gate."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


MAX_CPC = 0.15
PACKET_DIR = Path(__file__).resolve().parent
SOURCE_MATRIX = PACKET_DIR / "gb_ca_au_36_keyword_planner_validation_matrix.csv"


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def normalize_keyword(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("[]\"'").lower())


def parse_money(value: str) -> float | None:
    cleaned = value.strip().replace("$", "").replace(",", "")
    if not cleaned or cleaned in {"-", "—", "n/a", "N/A"}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def read_csv_normalized(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []
        field_map = {field: normalize_header(field) for field in reader.fieldnames}
        return [{field_map[key]: value for key, value in row.items()} for row in reader]


def row_value(row: dict[str, str], *names: str) -> str:
    for name in names:
        key = normalize_header(name)
        if key in row and row[key].strip():
            return row[key].strip()
    return ""


def load_source_matrix() -> dict[tuple[str, str, str], dict[str, str]]:
    with SOURCE_MATRIX.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    matrix: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in source_rows:
        key = (row["market"].upper(), normalize_keyword(row["keyword"]), row["match_type_to_validate"].lower())
        matrix[key] = row
    return matrix


def classify(row: dict[str, str], source: dict[str, str] | None) -> tuple[str, str]:
    policy = row_value(row, "policy_status", "policy", "status")
    auction = row_value(row, "auction_status", "auction", "keyword_status")
    policy_text = f"{policy} {auction}".lower()
    if any(token in policy_text for token in ["disapproved", "limited", "destination", "policy"]):
        return "POLICY_OR_DESTINATION_BLOCK", "policy/status text indicates a block or limitation"

    cpc_values = [
        parse_money(row_value(row, "avg_cpc", "average_cpc", "avg_cpc_usd")),
        parse_money(row_value(row, "first_page_cpc", "est_first_page_bid", "first_page_bid")),
        parse_money(row_value(row, "top_of_page_cpc", "est_top_of_page_bid", "top_page_bid")),
    ]
    present_cpc_values = [value for value in cpc_values if value is not None]
    if not present_cpc_values:
        return "MISSING_REQUIRED_FORECAST_DATA", "no CPC value was parseable"
    if any(value > MAX_CPC for value in present_cpc_values):
        return "FAIL_015_CPC_GATE", f"one or more CPC values exceed ${MAX_CPC:.2f}"

    clicks = parse_money(row_value(row, "forecast_clicks", "clicks"))
    impressions = parse_money(row_value(row, "forecast_impressions", "impressions", "impr"))
    low_volume_text = row_value(row, "notes", "auction_status", "keyword_status").lower()
    if "low search volume" in low_volume_text or "no auction" in low_volume_text:
        return "LOW_VOLUME_OR_NO_AUCTION", "forecast/status says low search volume or no auction entry"
    if clicks == 0 and impressions == 0:
        return "LOW_VOLUME_OR_NO_AUCTION", "forecast has zero clicks and zero impressions"

    if source is None:
        return "MISSING_REQUIRED_FORECAST_DATA", "row did not match the canonical validation matrix"
    return "PASS_015_CPC_GATE", "all supplied CPC values are at or below the hard gate"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forecast-csv", required=True, type=Path)
    parser.add_argument("--output-csv", type=Path, default=PACKET_DIR / "keyword_planner_forecast_decisions.csv")
    parser.add_argument("--summary-json", type=Path, default=PACKET_DIR / "keyword_planner_forecast_decision_summary.json")
    args = parser.parse_args()

    source_matrix = load_source_matrix()
    forecast_rows = read_csv_normalized(args.forecast_csv)
    decisions: list[dict[str, str]] = []
    for row in forecast_rows:
        market = row_value(row, "market", "country").upper()
        keyword = normalize_keyword(row_value(row, "keyword", "search_term"))
        match_type = row_value(row, "match_type", "match type").lower() or "exact"
        source = source_matrix.get((market, keyword, match_type))
        decision, reason = classify(row, source)
        decisions.append(
            {
                "market": market,
                "keyword": keyword,
                "match_type": match_type,
                "decision": decision,
                "reason": reason,
                "avg_cpc": row_value(row, "avg_cpc", "average_cpc", "avg_cpc_usd"),
                "first_page_cpc": row_value(row, "first_page_cpc", "est_first_page_bid", "first_page_bid"),
                "top_of_page_cpc": row_value(row, "top_of_page_cpc", "est_top_of_page_bid", "top_page_bid"),
                "forecast_clicks": row_value(row, "forecast_clicks", "clicks"),
                "forecast_impressions": row_value(row, "forecast_impressions", "impressions", "impr"),
                "final_url": source["final_url"] if source else "",
                "campaign_id": source["campaign_id"] if source else "",
                "ad_group_id": source["ad_group_id"] if source else "",
            }
        )

    fieldnames = [
        "market",
        "keyword",
        "match_type",
        "decision",
        "reason",
        "avg_cpc",
        "first_page_cpc",
        "top_of_page_cpc",
        "forecast_clicks",
        "forecast_impressions",
        "final_url",
        "campaign_id",
        "ad_group_id",
    ]
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(decisions)

    summary = {
        "forecast_csv": str(args.forecast_csv),
        "decision_rows": len(decisions),
        "decision_counts": dict(sorted(Counter(row["decision"] for row in decisions).items())),
        "pass_rows": sum(1 for row in decisions if row["decision"] == "PASS_015_CPC_GATE"),
        "max_cpc_usd": MAX_CPC,
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
