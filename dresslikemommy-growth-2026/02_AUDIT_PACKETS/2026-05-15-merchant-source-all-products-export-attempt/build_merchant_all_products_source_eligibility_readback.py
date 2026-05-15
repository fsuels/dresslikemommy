#!/usr/bin/env python3
"""Build read-only Merchant all-products/source eligibility evidence.

The source export is a Merchant Center browser download. It does not include a
source-id column, so source identity is handled conservatively: US/es source
10627981690 is inferred only from the adjacent live source/detail readbacks,
while this script proves country/language/feed/currency row presence from the
download itself.
"""

from __future__ import annotations

import csv
import json
import re
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


PACKET_DIR = Path(__file__).resolve().parent
ZIP_PATH = PACKET_DIR / "browser-all-products-ready-download" / "products_2026-05-15_05-37-44.zip"
ISSUE_SUMMARY_PATH = (
    PACKET_DIR.parent / "2026-05-15-merchant-shopping-readonly-queue-readback" / "merchant_shopping_readonly_queue_summary.json"
)
ISSUE_ROWS_PATH = (
    PACKET_DIR.parent / "2026-05-15-merchant-shopping-readonly-queue-readback" / "merchant_shopping_target_issue_rows.csv"
)
REPAIR_SUMMARY_PATH = (
    PACKET_DIR.parent / "2026-05-15-merchant-us-es-repair-classification" / "merchant_us_es_repair_classification_summary.json"
)
PAID_COHORT_PATH = (
    PACKET_DIR.parent / "2026-04-29-google-shopping-campaign-gate" / "paid_cohort_exact_780_rows.csv"
)

TARGETS = [
    ("US", "es", "USD", "US"),
    ("CA", "en", "CAD", ""),
    ("GB", "en", "GBP", ""),
    ("AU", "en", "AUD", ""),
]


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def price_currency(row: dict[str, str], link_currency: str) -> str:
    if link_currency:
        return link_currency
    match = re.search(r"\b([A-Z]{3})$", clean(row.get("price")))
    return match.group(1) if match else ""


def link_country_currency(link: str) -> tuple[str, str]:
    params = parse_qs(urlsplit(link).query)
    return clean((params.get("country") or [""])[0]), clean((params.get("currency") or [""])[0])


def read_paid_cohort_ids() -> set[str]:
    with PAID_COHORT_PATH.open(newline="", encoding="utf-8") as handle:
        return {clean(row.get("merchant_center_item_id")) for row in csv.DictReader(handle)}


def read_issue_item_ids() -> set[str]:
    if not ISSUE_ROWS_PATH.exists():
        return set()
    with ISSUE_ROWS_PATH.open(newline="", encoding="utf-8") as handle:
        return {clean(row.get("Item ID") or row.get("id") or row.get("item_id")) for row in csv.DictReader(handle)}


def target_key(country: str, language: str) -> str:
    return f"{country}/{language}"


def blank_summary(country: str, language: str, expected_currency: str, expected_feed_label: str) -> dict[str, object]:
    return {
        "market": country,
        "language": language,
        "expected_currency": expected_currency,
        "expected_feed_label": expected_feed_label,
        "rows": 0,
        "in_stock_rows": 0,
        "paid_cohort_rows": 0,
        "paid_cohort_issue_rows": 0,
        "unique_items": 0,
        "unique_paid_cohort_items": 0,
        "missing_age_group_rows": 0,
        "missing_color_rows": 0,
        "missing_gender_rows": 0,
        "missing_size_rows": 0,
        "top_feed_labels": "",
        "top_currencies": "",
        "decision": "",
        "next_action": "",
    }


def main() -> None:
    paid_ids = read_paid_cohort_ids()
    issue_ids = read_issue_item_ids()
    target_summaries = {
        target_key(country, language): blank_summary(country, language, currency, feed_label)
        for country, language, currency, feed_label in TARGETS
    }
    target_feed_counts: dict[str, Counter[str]] = {key: Counter() for key in target_summaries}
    target_currency_counts: dict[str, Counter[str]] = {key: Counter() for key in target_summaries}
    target_item_ids: dict[str, set[str]] = {key: set() for key in target_summaries}
    target_paid_item_ids: dict[str, set[str]] = {key: set() for key in target_summaries}
    country_counts: Counter[str] = Counter()
    currency_counts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    feed_label_counts: Counter[str] = Counter()
    paid_rows: list[dict[str, str]] = []
    total_rows = 0

    with zipfile.ZipFile(ZIP_PATH) as archive:
        member = archive.namelist()[0]
        with archive.open(member) as raw:
            text_rows = (line.decode("utf-8-sig", "replace") for line in raw)
            reader = csv.DictReader(text_rows, delimiter="\t")
            for row in reader:
                total_rows += 1
                country, link_cur = link_country_currency(row.get("link", ""))
                currency = price_currency(row, link_cur)
                language = clean(row.get("language"))
                feed_label = clean(row.get("feed label"))
                item_id = clean(row.get("id"))
                country_counts[country] += 1
                currency_counts[currency] += 1
                language_counts[language] += 1
                feed_label_counts[feed_label] += 1
                key = target_key(country, language)
                if key not in target_summaries:
                    continue
                summary = target_summaries[key]
                summary["rows"] = int(summary["rows"]) + 1
                if clean(row.get("availability")).lower() in {"in stock", "in_stock"}:
                    summary["in_stock_rows"] = int(summary["in_stock_rows"]) + 1
                if not clean(row.get("age group")):
                    summary["missing_age_group_rows"] = int(summary["missing_age_group_rows"]) + 1
                if not clean(row.get("color")):
                    summary["missing_color_rows"] = int(summary["missing_color_rows"]) + 1
                if not clean(row.get("gender")):
                    summary["missing_gender_rows"] = int(summary["missing_gender_rows"]) + 1
                if not clean(row.get("size")):
                    summary["missing_size_rows"] = int(summary["missing_size_rows"]) + 1
                target_feed_counts[key][feed_label] += 1
                target_currency_counts[key][currency] += 1
                target_item_ids[key].add(item_id)
                if item_id in paid_ids:
                    summary["paid_cohort_rows"] = int(summary["paid_cohort_rows"]) + 1
                    target_paid_item_ids[key].add(item_id)
                    paid_rows.append(
                        {
                            "market": country,
                            "language": language,
                            "currency": currency,
                            "feed_label": feed_label,
                            "id": item_id,
                            "title": clean(row.get("title")),
                            "availability": clean(row.get("availability")),
                            "price": clean(row.get("price")),
                            "link": clean(row.get("link")),
                            "has_issue_export_row": "yes" if item_id in issue_ids else "no",
                            "age_group": clean(row.get("age group")),
                            "color": clean(row.get("color")),
                            "gender": clean(row.get("gender")),
                            "size": clean(row.get("size")),
                            "custom_label_0": clean(row.get("custom label 0")),
                            "custom_label_4": clean(row.get("custom label 4")),
                        }
                    )
                    if item_id in issue_ids:
                        summary["paid_cohort_issue_rows"] = int(summary["paid_cohort_issue_rows"]) + 1

    for key, summary in target_summaries.items():
        summary["unique_items"] = len(target_item_ids[key])
        summary["unique_paid_cohort_items"] = len(target_paid_item_ids[key])
        summary["top_feed_labels"] = " | ".join(f"{label}: {count}" for label, count in target_feed_counts[key].most_common(5))
        summary["top_currencies"] = " | ".join(f"{label}: {count}" for label, count in target_currency_counts[key].most_common(5))
        market = summary["market"]
        if key == "US/es":
            summary["decision"] = (
                "Rows exist in the all-products export, but US/es stays blocked by current issue-export "
                "and over-capacity evidence; export lacks source_id so source 10627981690 remains inferred "
                "from source/detail readback."
            )
            summary["next_action"] = (
                "Do not repair or build Shopping yet; use the classification packet and obtain owner approval "
                "only after source/product proof is sufficient."
            )
        elif int(summary["rows"]) == 0:
            summary["decision"] = (
                f"No {market}/en rows appeared in the current all-products export; this market is not "
                "Shopping-build-ready from Merchant feed evidence."
            )
            summary["next_action"] = (
                "Fix/feed-enable/export the market first, or obtain a current source export that proves rows "
                "exist with the expected country, currency, and language before any Shopping build."
            )
        else:
            summary["decision"] = "Rows exist; still require approved-status/source proof before a build."
            summary["next_action"] = "Run a current status/source readback before any live Shopping action."

    issue_summary = json.loads(ISSUE_SUMMARY_PATH.read_text(encoding="utf-8")) if ISSUE_SUMMARY_PATH.exists() else {}
    repair_summary = json.loads(REPAIR_SUMMARY_PATH.read_text(encoding="utf-8")) if REPAIR_SUMMARY_PATH.exists() else {}
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_MERCHANT_ALL_PRODUCTS_EXPORT_ELIGIBILITY_READBACK",
        "zip_path": str(ZIP_PATH),
        "zip_member": zipfile.ZipFile(ZIP_PATH).namelist()[0],
        "total_export_rows": total_rows,
        "paid_cohort_rows_expected": len(paid_ids),
        "target_summaries": list(target_summaries.values()),
        "top_countries": dict(country_counts.most_common(40)),
        "top_currencies": dict(currency_counts.most_common(40)),
        "top_languages": dict(language_counts.most_common(20)),
        "top_feed_labels": dict(feed_label_counts.most_common(40)),
        "issue_summary": {
            "issue_export_rows": issue_summary.get("issue_export_rows"),
            "us_es_issue_rows": next(
                (row for row in issue_summary.get("market_summaries", []) if row.get("market") == "US" and row.get("language") == "es"),
                {},
            ),
        },
        "repair_summary": repair_summary,
        "guardrails": [
            "Read-only Merchant browser download only.",
            "No upload, source sync, source edit, product edit, campaign, budget, bid, status, product group, conversion, billing, Shopify Admin, Pinterest, or live theme write occurred.",
            "The export does not include source_id or approved/disapproved status columns; decisions fail closed.",
        ],
    }

    summary_path = PACKET_DIR / "merchant_all_products_source_eligibility_summary.json"
    summary_csv_path = PACKET_DIR / "merchant_all_products_target_eligibility_summary.csv"
    paid_rows_path = PACKET_DIR / "merchant_all_products_target_paid_cohort_rows.csv"
    report_path = PACKET_DIR / "MERCHANT_ALL_PRODUCTS_SOURCE_ELIGIBILITY_READBACK.md"

    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with summary_csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(target_summaries["US/es"].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary["target_summaries"])
    with paid_rows_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "market",
            "language",
            "currency",
            "feed_label",
            "id",
            "title",
            "availability",
            "price",
            "link",
            "has_issue_export_row",
            "age_group",
            "color",
            "gender",
            "size",
            "custom_label_0",
            "custom_label_4",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(paid_rows)

    lines = [
        "# Merchant All-Products Source Eligibility Readback",
        "",
        f"Generated: `{summary['generated_at']}`",
        "",
        "Mode: read-only Merchant Center browser download and local parsing. No external write occurred.",
        "",
        "## Export",
        "",
        f"- Downloaded zip: `{ZIP_PATH}`",
        f"- TSV member: `{summary['zip_member']}`",
        f"- Total product rows: `{total_rows}`",
        "- Source-id status: the TSV does not include `source_id`; `US/es` source `10627981690` remains tied by adjacent live source/detail readback, not by this TSV column.",
        "- Approval-status status: the TSV does not include approved/disapproved destination status; decisions below fail closed.",
        "",
        "## Target Market Summary",
        "",
        "| Market | Language | Expected currency | Rows | In stock | Paid-cohort rows | Issue-export paid rows | Top feed labels | Decision |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary["target_summaries"]:
        lines.append(
            f"| `{row['market']}` | `{row['language']}` | `{row['expected_currency']}` | "
            f"`{row['rows']}` | `{row['in_stock_rows']}` | `{row['paid_cohort_rows']}` | "
            f"`{row['paid_cohort_issue_rows']}` | `{row['top_feed_labels']}` | {row['decision']} |"
        )
    lines.extend(
        [
            "",
            "## Decisions",
            "",
            "- `US/es`: rows exist, but the market remains blocked by the current issue export and over-capacity evidence. Do not build or repair from this packet alone.",
            "- `CA/en`, `GB/en`, `AU/en`: no rows appeared in the current all-products export, and no CAD/GBP/AUD feed labels appeared. These markets are not Merchant Shopping-ready from current feed evidence.",
            "- The next safe action is not a Shopping campaign build; it is a feed/source availability unblock or another authoritative Merchant export proving target rows exist.",
            "",
            "## Outputs",
            "",
            f"- Summary JSON: `{summary_path}`",
            f"- Market summary CSV: `{summary_csv_path}`",
            f"- Target paid-cohort rows CSV: `{paid_rows_path}`",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path), "report": str(report_path), "rows": total_rows}, indent=2))


if __name__ == "__main__":
    main()
