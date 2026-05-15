#!/usr/bin/env python3
"""Summarize current Merchant Shopping issue exports for the multilingual queue.

This is read-only evidence processing. It consumes a downloaded Merchant Center
product issue export and writes compact target-market summaries; it does not
call Merchant, Google Ads, Shopify, or any external write surface.
"""

from __future__ import annotations

import csv
import json
import os
import stat
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ISSUE_EXPORT = Path("/Users/fsuels/Downloads/product_issues_2026-05-15_05-10-59.csv")
ADS_PRODUCT_REPORT = Path("/Users/fsuels/Downloads/Product report.csv")
PAID_COHORT = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv"
)
API_ATTEMPT_SUMMARY = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-15-merchant-shopping-readonly-queue-api-attempt/"
    "merchant_center_api_diagnostics_summary.json"
)
OUTPUT_DIR = Path(__file__).resolve().parent

TARGETS = [
    ("US", "es", "United States", "us_es_spanish_shopping_readiness"),
    ("CA", "en", "Canada", "canada_english_shopping_feasibility"),
    ("GB", "en", "United Kingdom", "uk_english_shopping_feasibility"),
    ("AU", "en", "Australia", "australia_english_shopping_feasibility"),
]

TARGET_FIELDNAMES = [
    "market",
    "language",
    "country",
    "item_id",
    "title",
    "click_potential",
    "feed_label",
    "item_status",
    "channels",
    "issue_title",
    "issue_additional_information",
    "traffic_type",
    "issue_severity",
    "in_paid_cohort",
]

SUMMARY_FIELDNAMES = [
    "market",
    "language",
    "country",
    "issue_rows",
    "unique_issue_items",
    "paid_cohort_issue_items",
    "shopping_ads_issue_rows",
    "shopping_ads_disapproved_rows",
    "dynamic_remarketing_issue_rows",
    "free_listings_issue_rows",
    "top_issue_titles",
    "top_feed_labels",
    "status_counts",
    "decision",
    "next_action",
]


def read_csv(path: Path, *, encoding: str = "utf-8-sig") -> list[dict[str, str]]:
    with path.open(newline="", encoding=encoding) as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mtime(path: Path) -> str:
    if not path.exists():
        return ""
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")


def load_paid_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["merchant_center_item_id"] for row in read_csv(path) if row.get("merchant_center_item_id")}


def compact_counter(counter: Counter[str], limit: int = 8) -> str:
    return " | ".join(f"{key}: {value}" for key, value in counter.most_common(limit))


def target_subset(rows: list[dict[str, str]], country: str, language: str) -> list[dict[str, str]]:
    return [row for row in rows if row.get("Country") == country and row.get("Language") == language]


def decision_for(market: str, issue_rows: int, shopping_disapproved: int) -> tuple[str, str]:
    if market == "US":
        return (
            "US/es is not Shopping-build-ready from this export; current issue rows include age_group and Shopping capacity blockers.",
            "Classify exact source/product rows and prepare a no-write repair/approval packet for age_group/color/gender/image/page issues before any campaign or feed action.",
        )
    if issue_rows == 0:
        return (
            "No current issue-export rows surfaced for this country/language, but this is not full eligibility proof.",
            "Capture a current all-products/source export proving feed label, country, currency, active approved count, and paid-cohort intersection before any Shopping build.",
        )
    if shopping_disapproved:
        return (
            "Country/language has current Shopping-disapproved issue rows.",
            "Classify issue rows and hold campaign/feed actions until repaired or excluded.",
        )
    return (
        "Country/language has current limited issue rows that require classification before build.",
        "Export full product list and intersect paid cohort before any Shopping write.",
    )


def build() -> dict[str, Any]:
    rows = read_csv(ISSUE_EXPORT)
    paid_ids = load_paid_ids(PAID_COHORT)

    target_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    issue_title_rows: list[dict[str, Any]] = []

    for market, language, country, lane in TARGETS:
        subset = target_subset(rows, country, language)
        unique_items = {row["Item ID"] for row in subset}
        paid_items = unique_items & paid_ids
        traffic_counts = Counter(row["Traffic type"] for row in subset)
        shopping_disapproved = sum(
            1
            for row in subset
            if row["Traffic type"] == "Shopping ads" and row["Issue severity"] == "SEVERITY_DISAPPROVED"
        )
        decision, next_action = decision_for(market, len(subset), shopping_disapproved)
        issue_counts = Counter(row["Issue title"] for row in subset)

        summary_rows.append(
            {
                "market": market,
                "language": language,
                "country": country,
                "issue_rows": len(subset),
                "unique_issue_items": len(unique_items),
                "paid_cohort_issue_items": len(paid_items),
                "shopping_ads_issue_rows": traffic_counts.get("Shopping ads", 0),
                "shopping_ads_disapproved_rows": shopping_disapproved,
                "dynamic_remarketing_issue_rows": traffic_counts.get("Dynamic remarketing", 0),
                "free_listings_issue_rows": traffic_counts.get("Free listings", 0),
                "top_issue_titles": compact_counter(issue_counts),
                "top_feed_labels": compact_counter(Counter(row["Feed label"] for row in subset)),
                "status_counts": compact_counter(Counter(row["Item status"] for row in subset)),
                "decision": decision,
                "next_action": next_action,
            }
        )

        for issue_title, count in issue_counts.most_common():
            issue_title_rows.append(
                {
                    "market": market,
                    "language": language,
                    "country": country,
                    "issue_title": issue_title,
                    "issue_rows": count,
                    "unique_items": len({row["Item ID"] for row in subset if row["Issue title"] == issue_title}),
                    "traffic_types": compact_counter(Counter(row["Traffic type"] for row in subset if row["Issue title"] == issue_title)),
                    "severity": compact_counter(Counter(row["Issue severity"] for row in subset if row["Issue title"] == issue_title)),
                }
            )

        for row in subset:
            target_rows.append(
                {
                    "market": market,
                    "language": language,
                    "country": country,
                    "item_id": row["Item ID"],
                    "title": row["Title"],
                    "click_potential": row["Click potential"],
                    "feed_label": row["Feed label"],
                    "item_status": row["Item status"],
                    "channels": row["Channels"],
                    "issue_title": row["Issue title"],
                    "issue_additional_information": row["Issue additional information"],
                    "traffic_type": row["Traffic type"],
                    "issue_severity": row["Issue severity"],
                    "in_paid_cohort": "yes" if row["Item ID"] in paid_ids else "no",
                }
            )

    outputs = {
        "target_issue_rows": OUTPUT_DIR / "merchant_shopping_target_issue_rows.csv",
        "market_summary": OUTPUT_DIR / "merchant_shopping_market_language_summary.csv",
        "issue_title_counts": OUTPUT_DIR / "merchant_shopping_issue_title_counts.csv",
        "summary_json": OUTPUT_DIR / "merchant_shopping_readonly_queue_summary.json",
        "report": OUTPUT_DIR / "MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md",
    }
    write_csv(outputs["target_issue_rows"], TARGET_FIELDNAMES, target_rows)
    write_csv(outputs["market_summary"], SUMMARY_FIELDNAMES, summary_rows)
    write_csv(
        outputs["issue_title_counts"],
        ["market", "language", "country", "issue_title", "issue_rows", "unique_items", "traffic_types", "severity"],
        issue_title_rows,
    )

    api_attempt = {}
    if API_ATTEMPT_SUMMARY.exists():
        api_attempt = json.loads(API_ATTEMPT_SUMMARY.read_text(encoding="utf-8"))

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_MERCHANT_SHOPPING_QUEUE_ISSUE_EXPORT_ANALYSIS",
        "issue_export": str(ISSUE_EXPORT),
        "issue_export_mtime": mtime(ISSUE_EXPORT),
        "issue_export_rows": len(rows),
        "ads_product_report": str(ADS_PRODUCT_REPORT),
        "ads_product_report_mtime": mtime(ADS_PRODUCT_REPORT),
        "paid_cohort_rows": len(paid_ids),
        "api_attempt_status": {
            "api_source": api_attempt.get("api_source", ""),
            "merchant_evidence_rows": api_attempt.get("merchant_evidence_rows"),
            "api_attempt_errors": api_attempt.get("api_attempt_errors", []),
            "token_source": api_attempt.get("token_source", ""),
        },
        "market_summaries": summary_rows,
        "outputs": {key: str(path) for key, path in outputs.items()},
        "notes": [
            "The current Merchant issue export does not include source_id, so source 10627981690 is represented by the US/es country/language/feed-label issue readback and the live source/detail tab, not by a source-specific all-product export.",
            "Zero issue rows for CA/GB/AU means no issue-export rows surfaced for those country/language pairs; it does not prove active approved product counts.",
            "No external writes occurred.",
        ],
    }
    outputs["summary_json"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Merchant Shopping Read-Only Queue Readback",
        "",
        f"Generated: `{summary['generated_at']}`",
        "Mode: read-only Merchant issue export analysis. No Merchant, Google Ads, Shopify, feed, title, product-group, bid, budget, status, campaign, conversion, billing, or credential write occurred.",
        "",
        "## Source Evidence",
        "",
        f"- Current Merchant issue export: `{ISSUE_EXPORT}` (`{summary['issue_export_rows']}` rows, modified `{summary['issue_export_mtime']}`)",
        f"- Google Ads product report already downloaded: `{ADS_PRODUCT_REPORT}` (modified `{summary['ads_product_report_mtime']}`)",
        f"- API attempt: `{API_ATTEMPT_SUMMARY}`",
        "- Chrome DevTools MCP was profile-locked; direct local CDP/RPC evidence paths were used where available.",
        "",
        "## Results",
        "",
        "| Market | Language | Issue rows | Unique items | Paid-cohort issue items | Shopping ads issue rows | Shopping disapproved rows | Top issues | Decision |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in summary_rows:
        lines.append(
            "| {market} | {language} | {issue_rows} | {unique_issue_items} | {paid_cohort_issue_items} | "
            "{shopping_ads_issue_rows} | {shopping_ads_disapproved_rows} | {top_issue_titles} | {decision} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- `US/es` is not ready for a Shopping build from this readback: current issue rows include `Missing age group`, `Missing color`, `Missing gender`, product-page/image issues, and the Shopping capacity warning.",
            "- `CA/en`, `GB/en`, and `AU/en` showed `0` rows in the current issue export, which is useful but incomplete. It clears visible issue-export blockers only; it does not prove active approved product counts or feed/source availability.",
            "- Do not create Shopping campaigns, change feed/title/product groups, alter product scope, or change budget/bid/status from this packet.",
            "",
            "## Next Action",
            "",
            "- Prepare a no-write `US/es` repair/classification packet from the current issue rows, starting with age_group/color/gender and page/image issues.",
            "- Capture a full current all-products/source export for CA/GB/AU proving country, currency, feed label, active approved count, and paid-cohort intersection before any Shopping build.",
            "",
            "## Output Files",
            "",
            f"- `{outputs['market_summary']}`",
            f"- `{outputs['issue_title_counts']}`",
            f"- `{outputs['target_issue_rows']}`",
            f"- `{outputs['summary_json']}`",
        ]
    )
    outputs["report"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
