#!/usr/bin/env python3
"""Validate the held non-US Google Search TEST BUILD candidate CSV.

This is a local, read-only validator. It reads the held CSV from the prior
evidence packet and writes only lane-local summary artifacts.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import parse_qs, urlparse


REPO_ROOT = Path(__file__).resolve().parents[5]
LANE_DIR = Path(__file__).resolve().parent
SOURCE_CSV = (
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv"
)

EXPECTED_COUNTRIES = {
    "AU": "Australia",
    "BE": "Belgium",
    "CA": "Canada",
    "CH": "Switzerland",
    "CZ": "Czechia",
    "DE": "Germany",
    "DK": "Denmark",
    "ES": "Spain",
    "FR": "France",
    "GB": "United Kingdom",
    "GR": "Greece",
    "IT": "Italy",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
}

FORBIDDEN_PATTERNS = {
    "us_campaign_id_23827590655": "23827590655",
    "us_campaign_name": "DLM_US_",
    "united_states_location": "United States",
    "bad_beach_handle": "matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set",
    "bad_product_id_7227378892897": "7227378892897",
    "vacation_family": "Vacation Family",
    "pmax": "PMax",
    "performance_max": "Performance Max",
    "standard_shopping": "Standard Shopping",
    "shopping_ads": "Shopping ads",
    "product_scope": "product scope",
    "feed_label": "feed label",
    "product_group": "product group",
    "conversion_goal": "conversion goal",
    "merchant_center": "Merchant Center",
}

ID_COLUMNS = ["Campaign ID", "Ad group ID", "Keyword ID", "Ad ID"]
CPC_COLUMNS = ["Default max. CPC", "Max CPC Bid Limit for Target IS"]
STATUS_BY_ROW_TYPE = {
    "Campaign": "Campaign status",
    "Ad group": "Ad group status",
    "Keyword": "Keyword status",
    "Ad": "Ad status",
}
ALLOWED_ROW_TYPES = {"Campaign", "Ad group", "Keyword", "Negative keyword", "Ad"}


def as_decimal(raw: str) -> Decimal | None:
    raw = (raw or "").replace("$", "").strip()
    if not raw:
        return None
    try:
        return Decimal(raw)
    except InvalidOperation:
        return None


def campaign_iso(campaign_name: str) -> str:
    parts = campaign_name.split("_")
    return parts[1] if len(parts) > 1 else ""


def main() -> int:
    if not SOURCE_CSV.exists():
        raise SystemExit(f"Missing source CSV: {SOURCE_CSV}")

    with SOURCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        header = reader.fieldnames or []

    row_type_counts = Counter(row["Row Type"] for row in rows)
    action_counts = Counter(row["Action"] for row in rows)
    campaign_rows = [row for row in rows if row["Row Type"] == "Campaign"]
    final_url_rows = [row for row in rows if row.get("Final URL")]

    country_matrix: dict[str, dict[str, object]] = {}
    per_campaign_row_types: dict[str, Counter] = defaultdict(Counter)
    final_url_country_counts = Counter()
    bad_final_url_rows = []

    for row in rows:
        campaign = row.get("Campaign", "")
        if campaign:
            per_campaign_row_types[campaign][row["Row Type"]] += 1

    for row in campaign_rows:
        iso = campaign_iso(row["Campaign"])
        country_matrix[iso] = {
            "campaign": row["Campaign"],
            "location": row["Location"],
            "language": row["Language"],
            "budget": row["Budget"],
            "status": row["Campaign status"],
            "networks": row["Networks"],
            "bid_strategy_type": row["Bid strategy type"],
            "row_counts": dict(per_campaign_row_types[row["Campaign"]]),
        }

    for row in final_url_rows:
        iso = campaign_iso(row["Campaign"])
        country = parse_qs(urlparse(row["Final URL"]).query).get("country", [""])[0]
        final_url_country_counts[country] += 1
        if not country or country != iso:
            bad_final_url_rows.append(
                {
                    "campaign": row["Campaign"],
                    "ad_group": row["Ad group"],
                    "keyword": row["Keyword"],
                    "final_url": row["Final URL"],
                    "expected_country": iso,
                    "actual_country": country,
                }
            )

    cpc_values = set()
    cpc_over_guardrail = []
    for line_number, row in enumerate(rows, start=2):
        for column in CPC_COLUMNS:
            parsed = as_decimal(row.get(column, ""))
            if parsed is None:
                continue
            cpc_values.add(str(parsed))
            if parsed > Decimal("0.20"):
                cpc_over_guardrail.append(
                    {"line_number": line_number, "column": column, "value": str(parsed)}
                )

    forbidden_hits: dict[str, list[dict[str, object]]] = {}
    for name, pattern in FORBIDDEN_PATTERNS.items():
        hits = []
        needle = pattern.lower()
        for line_number, row in enumerate(rows, start=2):
            row_text = "\t".join(str(value) for value in row.values()).lower()
            if needle in row_text:
                hits.append({"line_number": line_number, "pattern": pattern})
        forbidden_hits[name] = hits[:10]

    id_populated_rows = []
    for line_number, row in enumerate(rows, start=2):
        for column in ID_COLUMNS:
            if row.get(column, "").strip():
                id_populated_rows.append(
                    {
                        "line_number": line_number,
                        "row_type": row["Row Type"],
                        "column": column,
                        "value": row[column],
                    }
                )

    non_paused_importable_rows = []
    status_counts = defaultdict(Counter)
    for line_number, row in enumerate(rows, start=2):
        row_type = row["Row Type"]
        status_column = STATUS_BY_ROW_TYPE.get(row_type)
        if not status_column:
            continue
        status = row.get(status_column, "")
        status_counts[row_type][status or "(blank)"] += 1
        if status != "Paused":
            non_paused_importable_rows.append(
                {
                    "line_number": line_number,
                    "row_type": row_type,
                    "status_column": status_column,
                    "status": status,
                }
            )

    expected_iso_set = set(EXPECTED_COUNTRIES)
    actual_iso_set = set(country_matrix)
    forbidden_counts = {key: len(value) for key, value in forbidden_hits.items()}
    max_cpc = max((Decimal(value) for value in cpc_values), default=Decimal("0"))

    gates = {
        "source_csv_exists": SOURCE_CSV.exists(),
        "data_row_count_1496": len(rows) == 1496,
        "allowed_row_types_only": set(row_type_counts) <= ALLOWED_ROW_TYPES,
        "all_actions_add": dict(action_counts) == {"Add": 1496},
        "expected_17_campaigns": len(campaign_rows) == 17,
        "expected_country_set": actual_iso_set == expected_iso_set,
        "campaign_locations_match_expected": all(
            country_matrix[iso]["location"] == expected
            for iso, expected in EXPECTED_COUNTRIES.items()
        ),
        "all_campaigns_search_google_search_network": all(
            row.get("Campaign type") == "Search" and row.get("Networks") == "Google search"
            for row in campaign_rows
        ),
        "all_importable_entities_paused": not non_paused_importable_rows,
        "all_existing_entity_ids_blank": not id_populated_rows,
        "max_cpc_at_or_below_0_20": max_cpc <= Decimal("0.20"),
        "all_final_urls_country_qualified": not bad_final_url_rows,
        "expected_final_url_count_680": len(final_url_rows) == 680,
        "expected_40_final_urls_per_country": all(
            final_url_country_counts.get(iso, 0) == 40 for iso in EXPECTED_COUNTRIES
        ),
        "no_forbidden_patterns": all(count == 0 for count in forbidden_counts.values()),
    }

    result = {
        "source_csv": str(SOURCE_CSV),
        "overall_result": "PASS" if all(gates.values()) else "FAIL",
        "gates": gates,
        "summary": {
            "data_rows": len(rows),
            "header_columns": len(header),
            "row_type_counts": dict(sorted(row_type_counts.items())),
            "action_counts": dict(sorted(action_counts.items())),
            "campaign_count": len(campaign_rows),
            "country_count": len(country_matrix),
            "country_isos": sorted(country_matrix),
            "budget_values": sorted(
                {row["Budget"] for row in campaign_rows if row.get("Budget")}
            ),
            "languages": sorted(
                {row["Language"] for row in campaign_rows if row.get("Language")}
            ),
            "status_counts": {
                row_type: dict(counter) for row_type, counter in sorted(status_counts.items())
            },
            "final_url_rows": len(final_url_rows),
            "final_url_country_counts": dict(sorted(final_url_country_counts.items())),
            "cpc_values": sorted(cpc_values, key=lambda value: Decimal(value)),
            "max_cpc": str(max_cpc),
            "id_populated_row_count": len(id_populated_rows),
            "non_paused_importable_row_count": len(non_paused_importable_rows),
            "forbidden_hit_counts": dict(sorted(forbidden_counts.items())),
        },
        "country_matrix": dict(sorted(country_matrix.items())),
        "samples": {
            "bad_final_url_rows": bad_final_url_rows[:10],
            "cpc_over_guardrail": cpc_over_guardrail[:10],
            "id_populated_rows": id_populated_rows[:10],
            "non_paused_importable_rows": non_paused_importable_rows[:10],
            "forbidden_hits": forbidden_hits,
        },
    }

    summary_path = LANE_DIR / "validation_summary.json"
    matrix_path = LANE_DIR / "country_matrix.csv"
    summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    with matrix_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "country_iso",
                "location",
                "campaign",
                "language",
                "budget",
                "campaign_status",
                "networks",
                "campaign_rows",
                "ad_group_rows",
                "positive_keyword_rows",
                "negative_keyword_rows",
                "ad_rows",
                "final_url_rows",
            ]
        )
        for iso, info in sorted(country_matrix.items()):
            counts = info["row_counts"]
            writer.writerow(
                [
                    iso,
                    info["location"],
                    info["campaign"],
                    info["language"],
                    info["budget"],
                    info["status"],
                    info["networks"],
                    counts.get("Campaign", 0),
                    counts.get("Ad group", 0),
                    counts.get("Keyword", 0),
                    counts.get("Negative keyword", 0),
                    counts.get("Ad", 0),
                    final_url_country_counts.get(iso, 0),
                ]
            )

    print(json.dumps(result["summary"], indent=2))
    print(f"overall_result={result['overall_result']}")
    print(f"wrote={summary_path}")
    print(f"wrote={matrix_path}")
    return 0 if result["overall_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
