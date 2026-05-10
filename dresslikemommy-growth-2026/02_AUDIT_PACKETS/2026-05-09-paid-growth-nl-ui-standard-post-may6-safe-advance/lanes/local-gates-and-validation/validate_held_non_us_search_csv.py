#!/usr/bin/env python3
"""Validate the held non-US Google Search web-bulk CSV.

This is intentionally local-only. It reads the held CSV and writes a JSON
summary in this lane path; it does not touch any external account.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import parse_qs, urlparse


REPO_ROOT = Path(__file__).resolve().parents[5]
LANE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = REPO_ROOT / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-08-paid-growth-url-hold-checkout-safe-advance/"
    "lanes/google-ads-url-hold/web_bulk_upload/"
    "00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv"
)
DEFAULT_OUT = LANE_DIR / "held_non_us_search_csv_validation.json"

EXPECTED_ROW_TYPES = {"Campaign", "Ad group", "Keyword", "Negative keyword", "Ad"}
IMPORTABLE_STATUS_FIELDS = {
    "Campaign": "Campaign status",
    "Ad group": "Ad group status",
    "Keyword": "Keyword status",
    "Ad": "Ad status",
}
EXPECTED_LOCATIONS = {
    "Australia",
    "Belgium",
    "Canada",
    "Czechia",
    "Denmark",
    "France",
    "Germany",
    "Greece",
    "Italy",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Spain",
    "Sweden",
    "Switzerland",
    "United Kingdom",
}
ID_COLUMNS = ["Campaign ID", "Ad group ID", "Keyword ID", "Ad ID"]
CPC_COLUMNS = ["Default max. CPC", "Max CPC Bid Limit for Target IS"]

FORBIDDEN_PATTERNS = {
    "bad_beach_handle": re.compile(
        r"matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set",
        re.I,
    ),
    "bad_product_id_7227378892897": re.compile(r"\b7227378892897\b"),
    "vacation_family": re.compile(r"\bVacation Family\b", re.I),
    "us_campaign_23827590655": re.compile(r"\b23827590655\b"),
    "pmax": re.compile(r"\bPMax\b", re.I),
    "performance_max": re.compile(r"\bPerformance Max\b", re.I),
    "standard_shopping": re.compile(r"\bStandard Shopping\b", re.I),
    "shopping_ads": re.compile(r"\bShopping ads\b", re.I),
    "product_scope": re.compile(r"\bproduct[_ -]?scope\b", re.I),
    "product_group": re.compile(r"\bproduct[_ -]?group\b", re.I),
    "feed_label": re.compile(r"\bfeed[_ -]?label\b", re.I),
    "standalone_feed": re.compile(r"\bfeed\b", re.I),
    "conversion_goal": re.compile(r"\bconversion[_ -]?goal\b", re.I),
    "merchant_row": re.compile(r"\bMerchant\b", re.I),
}


def decimal_from_raw(raw: str) -> Decimal | None:
    cleaned = raw.strip().replace("$", "").replace(",", "")
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def row_text(row: dict[str, str]) -> str:
    return " | ".join(row.get(key, "") for key in row)


def validate(csv_path: Path) -> dict:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    row_type_counts = Counter(row.get("Row Type", "") for row in rows)
    action_counts = Counter(row.get("Action", "") for row in rows)
    status_counts: dict[str, Counter] = defaultdict(Counter)
    campaigns: dict[str, dict] = {}
    campaign_row_counts: dict[str, Counter] = defaultdict(Counter)
    campaign_status_rows = []
    id_nonblank = []
    status_not_paused = []
    final_url_rows = []
    final_url_missing_country = []
    cpc_values: list[str] = []
    cpc_failures = []
    cpc_invalid = []
    forbidden_hits: dict[str, list[dict]] = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        entity = row.get("Row Type", "")
        campaign = row.get("Campaign", "")
        campaign_row_counts[campaign][entity] += 1

        if entity == "Campaign":
            campaigns[campaign] = {
                "location": row.get("Location", ""),
                "status": row.get("Campaign status", ""),
                "budget": row.get("Budget", ""),
                "type": row.get("Campaign type", ""),
                "networks": row.get("Networks", ""),
            }

        status_field = IMPORTABLE_STATUS_FIELDS.get(entity)
        if status_field:
            status = row.get(status_field, "")
            status_counts[entity][status] += 1
            if status != "Paused":
                status_not_paused.append(
                    {
                        "line": index,
                        "row_type": entity,
                        "campaign": campaign,
                        "ad_group": row.get("Ad group", ""),
                        "status_field": status_field,
                        "status": status,
                    }
                )

        for column in ID_COLUMNS:
            if row.get(column, "").strip():
                id_nonblank.append(
                    {
                        "line": index,
                        "row_type": entity,
                        "campaign": campaign,
                        "column": column,
                        "value": row[column],
                    }
                )

        for column in CPC_COLUMNS:
            raw = row.get(column, "")
            parsed = decimal_from_raw(raw)
            if raw.strip() and parsed is None:
                cpc_invalid.append(
                    {
                        "line": index,
                        "row_type": entity,
                        "campaign": campaign,
                        "column": column,
                        "value": raw,
                    }
                )
            elif parsed is not None:
                cpc_values.append(str(parsed))
                if parsed > Decimal("0.20"):
                    cpc_failures.append(
                        {
                            "line": index,
                            "row_type": entity,
                            "campaign": campaign,
                            "column": column,
                            "value": str(parsed),
                        }
                    )

        final_url = row.get("Final URL", "").strip()
        if final_url:
            parsed = urlparse(final_url)
            params = parse_qs(parsed.query)
            final_url_rows.append(
                {
                    "line": index,
                    "campaign": campaign,
                    "ad_group": row.get("Ad group", ""),
                    "url": final_url,
                    "country": params.get("country", [""])[0],
                }
            )
            if not params.get("country"):
                final_url_missing_country.append(
                    {
                        "line": index,
                        "campaign": campaign,
                        "ad_group": row.get("Ad group", ""),
                        "url": final_url,
                    }
                )

        text = row_text(row)
        for name, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                forbidden_hits[name].append(
                    {
                        "line": index,
                        "row_type": entity,
                        "campaign": campaign,
                        "ad_group": row.get("Ad group", ""),
                    }
                )

        campaign_status = row.get("Campaign status", "")
        ad_group_status = row.get("Ad group status", "")
        keyword_status = row.get("Keyword status", "")
        ad_status = row.get("Ad status", "")
        if any(
            value in {"Enabled", "Active", "Eligible"}
            for value in [campaign_status, ad_group_status, keyword_status, ad_status]
        ):
            campaign_status_rows.append(
                {
                    "line": index,
                    "row_type": entity,
                    "campaign": campaign,
                    "campaign_status": campaign_status,
                    "ad_group_status": ad_group_status,
                    "keyword_status": keyword_status,
                    "ad_status": ad_status,
                }
            )

    locations = Counter(data["location"] for data in campaigns.values())
    unexpected_locations = sorted(set(locations) - EXPECTED_LOCATIONS)
    missing_locations = sorted(EXPECTED_LOCATIONS - set(locations))
    us_like_campaign_names = sorted(
        name for name in campaigns if name.startswith("DLM_US") or "_US_" in name
    )
    campaign_locations = [
        {
            "campaign": campaign,
            "location": data["location"],
            "budget": data["budget"],
            "status": data["status"],
            "rows": dict(campaign_row_counts[campaign]),
        }
        for campaign, data in sorted(campaigns.items())
    ]

    final_url_country_counts = Counter(item["country"] for item in final_url_rows)
    unique_cpc_values = sorted({Decimal(value) for value in cpc_values})

    gates = {
        "csv_row_count_1496": len(rows) == 1496,
        "all_actions_add": set(action_counts) == {"Add"},
        "allowed_row_types_only": set(row_type_counts) <= EXPECTED_ROW_TYPES,
        "expected_17_non_us_campaigns": len(campaigns) == 17
        and not unexpected_locations
        and not missing_locations
        and not us_like_campaign_names,
        "all_importable_entities_paused": not status_not_paused,
        "negative_keywords_counted_separately": row_type_counts.get("Negative keyword", 0)
        == 629,
        "all_existing_id_columns_blank": not id_nonblank,
        "no_enablement_status_hits": not campaign_status_rows,
        "cpc_at_or_below_0_20": not cpc_failures and not cpc_invalid,
        "all_final_urls_country_qualified": bool(final_url_rows)
        and not final_url_missing_country,
        "no_forbidden_patterns": all(not hits for hits in forbidden_hits.values()),
    }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_csv": str(csv_path),
        "overall_result": "PASS" if all(gates.values()) else "FAIL",
        "gates": gates,
        "summary": {
            "data_rows": len(rows),
            "header_columns": len(fieldnames),
            "row_type_counts": dict(row_type_counts),
            "action_counts": dict(action_counts),
            "campaign_count": len(campaigns),
            "location_count": len(locations),
            "locations": dict(sorted(locations.items())),
            "budget_values": sorted(
                {data["budget"] for data in campaigns.values() if data["budget"]}
            ),
            "status_counts": {
                entity: dict(counter) for entity, counter in sorted(status_counts.items())
            },
            "final_url_rows": len(final_url_rows),
            "final_url_country_counts": dict(sorted(final_url_country_counts.items())),
            "cpc_values": [str(value) for value in unique_cpc_values],
            "max_cpc": str(max(unique_cpc_values)) if unique_cpc_values else None,
            "id_nonblank_count": len(id_nonblank),
            "status_not_paused_count": len(status_not_paused),
            "forbidden_hit_counts": {
                name: len(forbidden_hits.get(name, []))
                for name in sorted(FORBIDDEN_PATTERNS)
            },
        },
        "details": {
            "campaign_locations": campaign_locations,
            "unexpected_locations": unexpected_locations,
            "missing_locations": missing_locations,
            "us_like_campaign_names": us_like_campaign_names,
            "status_not_paused": status_not_paused,
            "id_nonblank": id_nonblank,
            "cpc_failures": cpc_failures,
            "cpc_invalid": cpc_invalid,
            "final_url_missing_country": final_url_missing_country,
            "enablement_status_hits": campaign_status_rows,
            "forbidden_hits": {
                name: forbidden_hits.get(name, []) for name in sorted(FORBIDDEN_PATTERNS)
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    result = validate(args.csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_result": result["overall_result"], **result["summary"]}, indent=2))
    return 0 if result["overall_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
