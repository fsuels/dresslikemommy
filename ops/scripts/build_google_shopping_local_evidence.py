#!/usr/bin/env python3
"""Build local Merchant Center and PDP evidence CSVs for Shopping review.

This script is read-only against external systems. It converts existing local
exports into the evidence shape consumed by
build_google_shopping_us_clean_subset.py. Absence from an issue export is not
treated as Merchant Center approval, and an accessibility-only PDP check is not
treated as a full PDP pass.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_INPUT = Path(
    "dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/"
    "2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv"
)
DEFAULT_MERCHANT_CENTER_ISSUES = Path(
    "ops/feed-engineering/2026-03-30-phase-4a-mc-issue-reconciliation/"
    "merchant_center_issue_reconciliation.csv"
)
DEFAULT_PDP_ACCESSIBILITY = Path(
    "ops/feed-engineering/2026-03-29-phase-3z-google-page-accessibility-audit/"
    "google_product_page_accessibility_audit.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY"
)
NEEDS_DATA = "NEEDS_DATA"

MERCHANT_EVIDENCE_FIELDNAMES = [
    "merchant_center_item_id",
    "shopify_product_id",
    "shopify_variant_id",
    "merchant_center_status",
    "merchant_center_destination",
    "merchant_center_issue_count",
    "merchant_center_issues",
    "image_status",
    "price_status",
    "availability_status",
    "shipping_policy_status",
    "return_policy_status",
    "evidence_source",
    "evidence_notes",
]

PDP_EVIDENCE_FIELDNAMES = [
    "merchant_center_item_id",
    "shopify_product_id",
    "shopify_variant_id",
    "handle",
    "product_url",
    "pdp_status",
    "desktop_http_status",
    "mobile_http_status",
    "desktop_blocked_reasons",
    "mobile_blocked_reasons",
    "desktop_error",
    "mobile_error",
    "pdp_evidence_source",
    "pdp_notes",
]


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", clean(value).lower()).strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def merchant_item_id(row: dict[str, str]) -> str:
    for key in ("merchant_center_id", "merchant_center_item_id", "Item ID", "normalized_offer_id"):
        value = clean(row.get(key))
        if value:
            return value
    product_id = clean(row.get("product_id") or row.get("shopify_product_id"))
    variant_id = clean(row.get("variant_id") or row.get("shopify_variant_id"))
    if product_id and variant_id:
        return f"shopify_US_{product_id}_{variant_id}"
    return ""


def is_us_country(value: str) -> bool:
    return normalize(value) in {"united_states", "us", "usa", "united_states_of_america"}


def issue_status_bucket(issue_title: str, bucket_name: str) -> bool:
    title = normalize(issue_title)
    if bucket_name == "image":
        return "image" in title
    if bucket_name == "price":
        return "price" in title
    if bucket_name == "availability":
        return "availability" in title or "stock" in title
    if bucket_name == "shipping":
        return "shipping" in title
    if bucket_name == "return":
        return "return" in title
    return False


def status_for_issue_bucket(issues: list[str], bucket_name: str) -> str:
    return "FAIL" if any(issue_status_bucket(issue, bucket_name) for issue in issues) else NEEDS_DATA


def build_merchant_evidence_rows(
    current_rows: list[dict[str, str]],
    issue_rows: list[dict[str, str]],
    *,
    source_path: Path,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    current_by_item_id = {merchant_item_id(row): row for row in current_rows if merchant_item_id(row)}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    scanned_rows = 0
    for row in issue_rows:
        scanned_rows += 1
        item_id = merchant_item_id(row)
        if not item_id or item_id not in current_by_item_id:
            continue
        if not is_us_country(row.get("Country", "")):
            continue
        grouped[item_id].append(row)

    evidence_rows: list[dict[str, str]] = []
    issue_title_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    issue_rows_for_current_us = 0

    for item_id in sorted(grouped):
        rows = grouped[item_id]
        current = current_by_item_id[item_id]
        issues = sorted({clean(row.get("Issue title")) for row in rows if clean(row.get("Issue title"))})
        statuses = sorted({clean(row.get("Item status")) for row in rows if clean(row.get("Item status"))})
        issue_rows_for_current_us += len(rows)
        issue_title_counts.update(issues)
        status_counts.update(statuses)

        evidence_rows.append(
            {
                "merchant_center_item_id": item_id,
                "shopify_product_id": clean(current.get("product_id") or current.get("shopify_product_id")),
                "shopify_variant_id": clean(current.get("variant_id") or current.get("shopify_variant_id")),
                "merchant_center_status": "|".join(statuses) if statuses else NEEDS_DATA,
                "merchant_center_destination": NEEDS_DATA,
                "merchant_center_issue_count": str(len(rows)),
                "merchant_center_issues": "|".join(issues) if issues else NEEDS_DATA,
                "image_status": status_for_issue_bucket(issues, "image"),
                "price_status": status_for_issue_bucket(issues, "price"),
                "availability_status": status_for_issue_bucket(issues, "availability"),
                "shipping_policy_status": status_for_issue_bucket(issues, "shipping"),
                "return_policy_status": status_for_issue_bucket(issues, "return"),
                "evidence_source": str(source_path),
                "evidence_notes": "US issue-export rows found; this is not a full approval diagnostics export.",
            }
        )

    summary = {
        "merchant_issue_export_rows_scanned": scanned_rows,
        "merchant_issue_rows_for_current_us": issue_rows_for_current_us,
        "merchant_evidence_rows": len(evidence_rows),
        "merchant_issue_title_counts_us": dict(issue_title_counts.most_common(20)),
        "merchant_status_counts_us": dict(status_counts.most_common(20)),
    }
    return evidence_rows, summary


def accessibility_pdp_status(row: dict[str, str]) -> str:
    desktop_status = clean(row.get("desktop_http_status"))
    mobile_status = clean(row.get("mobile_http_status"))
    blocked = normalize(row.get("blocked_on_either")) in {"true", "1", "yes"}
    errors = any(clean(row.get(key)) for key in ("desktop_error", "mobile_error"))
    blocked_reasons = any(
        clean(row.get(key)) for key in ("desktop_blocked_reasons", "mobile_blocked_reasons")
    )
    if blocked or errors or blocked_reasons or desktop_status != "200" or mobile_status != "200":
        return "FAIL"
    return NEEDS_DATA


def accessibility_notes(row: dict[str, str], status: str) -> str:
    if status == "FAIL":
        parts = [
            clean(row.get("desktop_blocked_reasons")),
            clean(row.get("mobile_blocked_reasons")),
            clean(row.get("desktop_error")),
            clean(row.get("mobile_error")),
        ]
        details = "; ".join(part for part in parts if part)
        return details or "Accessibility audit did not pass on both desktop and mobile."
    return "Accessibility check passed on desktop/mobile, but full PDP Shopping QA is still required."


def build_pdp_evidence_rows(
    current_rows: list[dict[str, str]],
    accessibility_rows: list[dict[str, str]],
    *,
    source_path: Path,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    current_by_product_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in current_rows:
        product_id = clean(row.get("product_id") or row.get("shopify_product_id"))
        if product_id:
            current_by_product_id[product_id].append(row)

    matched_products = 0
    evidence_rows: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()

    for access_row in accessibility_rows:
        product_id = clean(access_row.get("product_id"))
        variants = current_by_product_id.get(product_id, [])
        if not variants:
            continue
        matched_products += 1
        status = accessibility_pdp_status(access_row)
        status_counts.update([status])
        notes = accessibility_notes(access_row, status)

        for current in variants:
            evidence_rows.append(
                {
                    "merchant_center_item_id": merchant_item_id(current),
                    "shopify_product_id": product_id,
                    "shopify_variant_id": clean(current.get("variant_id") or current.get("shopify_variant_id")),
                    "handle": clean(access_row.get("handle") or current.get("handle")),
                    "product_url": clean(access_row.get("online_store_url")),
                    "pdp_status": status,
                    "desktop_http_status": clean(access_row.get("desktop_http_status")),
                    "mobile_http_status": clean(access_row.get("mobile_http_status")),
                    "desktop_blocked_reasons": clean(access_row.get("desktop_blocked_reasons")),
                    "mobile_blocked_reasons": clean(access_row.get("mobile_blocked_reasons")),
                    "desktop_error": clean(access_row.get("desktop_error")),
                    "mobile_error": clean(access_row.get("mobile_error")),
                    "pdp_evidence_source": str(source_path),
                    "pdp_notes": notes,
                }
            )

    summary = {
        "pdp_accessibility_products_scanned": len(accessibility_rows),
        "pdp_accessibility_current_products_matched": matched_products,
        "pdp_evidence_rows": len(evidence_rows),
        "pdp_status_counts": dict(status_counts.most_common()),
    }
    return evidence_rows, summary


def build_outputs(
    input_eligibility: Path,
    merchant_center_issue_export: Path,
    pdp_accessibility_export: Path,
    output_dir: Path,
) -> dict[str, object]:
    current_rows = read_csv(input_eligibility)
    issue_rows = read_csv(merchant_center_issue_export)
    accessibility_rows = read_csv(pdp_accessibility_export)

    merchant_rows, merchant_summary = build_merchant_evidence_rows(
        current_rows,
        issue_rows,
        source_path=merchant_center_issue_export,
    )
    pdp_rows, pdp_summary = build_pdp_evidence_rows(
        current_rows,
        accessibility_rows,
        source_path=pdp_accessibility_export,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "merchant_center_evidence": output_dir / "merchant_center_diagnostics_evidence.csv",
        "pdp_evidence": output_dir / "pdp_evidence.csv",
        "summary": output_dir / "local_evidence_build_summary.json",
    }
    write_csv(paths["merchant_center_evidence"], MERCHANT_EVIDENCE_FIELDNAMES, merchant_rows)
    write_csv(paths["pdp_evidence"], PDP_EVIDENCE_FIELDNAMES, pdp_rows)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_LOCAL_EXPORT_CONVERSION",
        "input_eligibility": str(input_eligibility),
        "merchant_center_issue_export": str(merchant_center_issue_export),
        "pdp_accessibility_export": str(pdp_accessibility_export),
        "current_variant_rows_scanned": len(current_rows),
        **merchant_summary,
        **pdp_summary,
        "important_limits": [
            "Merchant Center issue export is not a full approval diagnostics export.",
            "Products absent from the issue export remain NEEDS_DATA, not approved.",
            "PDP accessibility pass is not full PDP paid-readiness proof.",
        ],
        "outputs": {key: str(path) for key, path in paths.items()},
    }
    paths["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-eligibility", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--merchant-center-issue-export", type=Path, default=DEFAULT_MERCHANT_CENTER_ISSUES)
    parser.add_argument("--pdp-accessibility-export", type=Path, default=DEFAULT_PDP_ACCESSIBILITY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_outputs(
        args.input_eligibility,
        args.merchant_center_issue_export,
        args.pdp_accessibility_export,
        args.output_dir,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
