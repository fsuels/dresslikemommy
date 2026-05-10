#!/usr/bin/env python3
"""Local-only QA for the held non-US Search CSV.

The script reads the already-generated held bulk upload file and writes a
summary JSON into this lane only. It does not call any external service.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not find repo root containing AGENTS.md")


REPO_ROOT = find_repo_root()
CSV_PATH = REPO_ROOT / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/"
    "google-ads-url-hold/web_bulk_upload/"
    "00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv"
)
OUTPUT_PATH = Path(__file__).resolve().with_name("creative_url_copy_qa_summary.json")

EXPECTED_COUNTRIES = [
    "GB",
    "CA",
    "AU",
    "CH",
    "DK",
    "DE",
    "NL",
    "SE",
    "FR",
    "BE",
    "ES",
    "IT",
    "PL",
    "CZ",
    "RO",
    "GR",
    "PT",
]
LOCALIZED_COUNTRIES = {"ES": "/es/products/", "IT": "/it/products/", "RO": "/ro/products/", "PT": "/pt/products/"}
BAD_HANDLE = "matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set"
BAD_PRODUCT_ID = "7227378892897"

AD_COPY_FIELDS = [
    *[f"Headline {i}" for i in range(1, 16)],
    *[f"Description {i}" for i in range(1, 5)],
    "Path 1",
    "Path 2",
    "Website description",
]
TARGETING_FIELDS = ["Keyword", "Negative keyword", "Ad group", "Campaign", "Final URL"]

CLAIM_PATTERNS = {
    "shipping_speed": [
        r"\bfast shipping\b",
        r"\brush shipping\b",
        r"\bquick delivery\b",
        r"\bsame[- ]day\b",
        r"\bnext[- ]day\b",
        r"\bguaranteed delivery\b",
    ],
    "physical_inventory": [
        r"\bwarehouse\b",
        r"\blocal stock\b",
        r"\bstocked inventory\b",
        r"\bnearby inventory\b",
        r"\bstore pickup\b",
        r"\bon[- ]hand stock\b",
    ],
    "availability_guarantee": [
        r"\bguaranteed inventory\b",
        r"\bguaranteed availability\b",
        r"\balways available\b",
        r"\bin stock now\b",
    ],
    "reviews_ratings": [
        r"\b\d+(\.\d+)?\s*stars?\b",
        r"\breviews?\b",
        r"\brated\b",
        r"\btop[- ]rated\b",
    ],
    "promotions": [
        r"\bsale\b",
        r"\bdiscount\b",
        r"\bcoupon\b",
        r"\bpromo code\b",
        r"\blimited[- ]time\b",
        r"\bfree gift\b",
        r"\bfree shipping\b",
        r"\bfree delivery\b",
        r"\b\d+%\s*off\b",
    ],
    "popularity_social_proof": [
        r"\bbest[- ]?seller\b",
        r"\bmost popular\b",
        r"\bviral\b",
        r"\btrending\b",
        r"\bcustomer favorite\b",
    ],
}


def campaign_country(campaign: str) -> str | None:
    match = re.match(r"DLM_([A-Z]{2})_SEARCH_", campaign or "")
    return match.group(1) if match else None


def collect_hits(rows: list[dict[str, str]], fields: list[str], patterns: dict[str, list[str]]) -> dict[str, list[dict[str, str]]]:
    hits: dict[str, list[dict[str, str]]] = defaultdict(list)
    compiled = {
        category: [(pattern, re.compile(pattern, re.IGNORECASE)) for pattern in pattern_list]
        for category, pattern_list in patterns.items()
    }
    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            value = (row.get(field) or "").strip()
            if not value:
                continue
            for category, pattern_list in compiled.items():
                for raw_pattern, pattern in pattern_list:
                    if pattern.search(value):
                        hits[category].append(
                            {
                                "row_number": row_number,
                                "row_type": row.get("Row Type", ""),
                                "campaign": row.get("Campaign", ""),
                                "ad_group": row.get("Ad group", ""),
                                "field": field,
                                "pattern": raw_pattern,
                                "value": value,
                            }
                        )
    return dict(hits)


def main() -> int:
    with CSV_PATH.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    row_counts = Counter(row["Row Type"] for row in rows)
    campaigns = sorted({row["Campaign"] for row in rows if row.get("Campaign")})
    countries = sorted({country for campaign in campaigns if (country := campaign_country(campaign))})
    country_counts = Counter(country for campaign in campaigns if (country := campaign_country(campaign)))
    campaign_rows = [
        {
            "country": campaign_country(row.get("Campaign", "")),
            "campaign": row.get("Campaign", ""),
            "campaign_status": row.get("Campaign status", ""),
            "campaign_type": row.get("Campaign type", ""),
            "networks": row.get("Networks", ""),
            "budget": row.get("Budget", ""),
            "bid_strategy_type": row.get("Bid strategy type", ""),
            "language": row.get("Language", ""),
            "location": row.get("Location", ""),
        }
        for row in rows
        if row.get("Row Type") == "Campaign"
    ]

    final_url_rows = []
    country_url_counts: Counter[str] = Counter()
    final_url_country_mismatches = []
    localized_path_mismatches = []
    missing_country_params = []
    bare_language_urls = []

    for row_number, row in enumerate(rows, start=2):
        final_url = (row.get("Final URL") or "").strip()
        if not final_url:
            continue
        campaign = row.get("Campaign", "")
        expected_country = campaign_country(campaign)
        parsed = urlparse(final_url)
        query_country = (parse_qs(parsed.query).get("country") or [""])[0]
        final_url_rows.append(final_url)
        if query_country:
            country_url_counts[query_country] += 1
        else:
            missing_country_params.append({"row_number": row_number, "campaign": campaign, "final_url": final_url})
        if expected_country and query_country != expected_country:
            final_url_country_mismatches.append(
                {
                    "row_number": row_number,
                    "campaign": campaign,
                    "expected_country": expected_country,
                    "query_country": query_country,
                    "final_url": final_url,
                }
            )
        path = parsed.path
        if expected_country in LOCALIZED_COUNTRIES and not path.startswith(LOCALIZED_COUNTRIES[expected_country]):
            localized_path_mismatches.append(
                {"row_number": row_number, "campaign": campaign, "expected_prefix": LOCALIZED_COUNTRIES[expected_country], "path": path}
            )
        if expected_country not in LOCALIZED_COUNTRIES and re.match(r"^/(es|it|ro|pt)/products/", path):
            localized_path_mismatches.append(
                {"row_number": row_number, "campaign": campaign, "expected_prefix": "/products/", "path": path}
            )
        if re.match(r"^/(es|it|ro|pt)/products/", path) and not query_country:
            bare_language_urls.append({"row_number": row_number, "campaign": campaign, "final_url": final_url})

    all_fields_blob = "\n".join(
        " || ".join(str(row.get(field, "") or "") for field in row.keys())
        for row in rows
    )
    stale_blocker_hits = {
        "bad_handle": len(re.findall(re.escape(BAD_HANDLE), all_fields_blob, flags=re.IGNORECASE)),
        "bad_product_id": len(re.findall(re.escape(BAD_PRODUCT_ID), all_fields_blob, flags=re.IGNORECASE)),
        "vacation_family_exact_phrase": len(re.findall(r"\bVacation Family\b", all_fields_blob, flags=re.IGNORECASE)),
        "christmas": len(re.findall(r"\bChristmas\b|\bXmas\b", all_fields_blob, flags=re.IGNORECASE)),
    }

    ad_copy_hits = collect_hits(rows, AD_COPY_FIELDS, CLAIM_PATTERNS)
    targeting_hits = collect_hits(rows, TARGETING_FIELDS, CLAIM_PATTERNS)

    headline_lengths = {
        field: max((len(row.get(field, "") or "") for row in rows), default=0)
        for field in [f"Headline {i}" for i in range(1, 16)]
    }
    description_lengths = {
        field: max((len(row.get(field, "") or "") for row in rows), default=0)
        for field in [f"Description {i}" for i in range(1, 5)]
    }

    failures = []
    if countries != sorted(EXPECTED_COUNTRIES):
        failures.append("country_coverage_mismatch")
    if any(count != 1 for count in country_counts.values()):
        failures.append("campaign_country_duplicates")
    if missing_country_params:
        failures.append("missing_country_params")
    if final_url_country_mismatches:
        failures.append("final_url_country_mismatches")
    if localized_path_mismatches:
        failures.append("localized_path_mismatches")
    if bare_language_urls:
        failures.append("bare_language_urls")
    if any(stale_blocker_hits.values()):
        failures.append("stale_or_held_vacation_family_hits")
    if ad_copy_hits:
        failures.append("unsupported_claim_hits_in_customer_facing_ad_copy")
    if any(length > 30 for length in headline_lengths.values()):
        failures.append("headline_length_over_30")
    if any(length > 90 for length in description_lengths.values()):
        failures.append("description_length_over_90")

    summary = {
        "source_csv": str(CSV_PATH.relative_to(REPO_ROOT)),
        "row_count": len(rows),
        "row_counts": dict(row_counts),
        "campaign_count": len(campaigns),
        "campaign_rows": campaign_rows,
        "campaign_languages": dict(Counter(row["language"] for row in campaign_rows)),
        "countries": countries,
        "expected_countries": EXPECTED_COUNTRIES,
        "country_coverage_pass": countries == sorted(EXPECTED_COUNTRIES) and all(count == 1 for count in country_counts.values()),
        "final_url_rows": len(final_url_rows),
        "unique_final_urls": len(set(final_url_rows)),
        "country_url_counts": dict(sorted(country_url_counts.items())),
        "missing_country_params": missing_country_params,
        "final_url_country_mismatches": final_url_country_mismatches,
        "localized_path_mismatches": localized_path_mismatches,
        "bare_language_urls": bare_language_urls,
        "stale_blocker_hits": stale_blocker_hits,
        "unsupported_claim_hits_in_customer_facing_ad_copy": ad_copy_hits,
        "unsupported_claim_hits_in_targeting_or_url_fields": targeting_hits,
        "headline_max_lengths": headline_lengths,
        "description_max_lengths": description_lengths,
        "overall_result": "PASS_LOCAL_ONLY_APPROVAL_GATED" if not failures else "FAIL_REVIEW_REQUIRED",
        "failures": failures,
    }

    OUTPUT_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
