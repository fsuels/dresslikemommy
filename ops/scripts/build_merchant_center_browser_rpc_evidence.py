#!/usr/bin/env python3
"""Build conservative Merchant Center evidence from a browser RPC product export.

This is a read-only fallback for when the official Merchant/Content API token is
missing scopes. It only marks a browser row as approved when the raw UI fields
match a combination sampled in the live Merchant Center product-details UI as:
Approved, Needs attention (0), and showing in ads.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


DEFAULT_BROWSER_RPC = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-other-ai-upload-pack/05_merchant_center_current_product_rows_from_browser_rpc.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY"
)

NEEDS_DATA = "NEEDS_DATA"
APPROVED_STATUS_RAW = "4"
LIMITED_STATUS_RAW = "3"
NOT_APPROVED_STATUS_RAW = "1"
HEALTHY_AGGREGATED_STATUS_RAW = "2"
ISSUE_AGGREGATED_STATUS_RAW = "5"
HEALTHY_IMAGE_STATUS_RAW = '{"2": 2}'
ISSUE_IMAGE_STATUS_RAW = '{"2": 5}'

FIELDNAMES = [
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


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def shopify_ids(item_id: str) -> tuple[str, str]:
    match = re.fullmatch(r"shopify_[A-Z]{2}_(\d+)_(\d+)", clean(item_id))
    return (match.group(1), match.group(2)) if match else ("", "")


def is_healthy_image(raw_value: str) -> bool:
    return clean(raw_value) == HEALTHY_IMAGE_STATUS_RAW


def is_issue_image(raw_value: str) -> bool:
    return clean(raw_value) == ISSUE_IMAGE_STATUS_RAW


def browser_row_to_evidence(row: dict[str, str]) -> dict[str, str]:
    item_id = clean(row.get("merchant_center_item_id"))
    product_id, variant_id = shopify_ids(item_id)
    language_code = clean(row.get("language_code"))
    price_currency = clean(row.get("price_currency"))
    price = clean(row.get("price"))
    source_name = clean(row.get("primary_source_name"))
    status_raw = clean(row.get("calculated_status_raw"))
    aggregated_raw = clean(row.get("aggregated_status_raw"))
    image_raw = clean(row.get("main_image_thumbnail_status_raw"))
    availability_raw = clean(row.get("availability_raw"))

    base = {
        "merchant_center_item_id": item_id,
        "shopify_product_id": product_id,
        "shopify_variant_id": variant_id,
        "merchant_center_status": NEEDS_DATA,
        "merchant_center_destination": NEEDS_DATA,
        "merchant_center_issue_count": NEEDS_DATA,
        "merchant_center_issues": NEEDS_DATA,
        "image_status": "PASS" if is_healthy_image(image_raw) else "FAIL" if is_issue_image(image_raw) else NEEDS_DATA,
        "price_status": "PASS" if price and price_currency == "USD" else NEEDS_DATA,
        "availability_status": "PASS" if availability_raw == "0" else NEEDS_DATA,
        "shipping_policy_status": NEEDS_DATA,
        "return_policy_status": NEEDS_DATA,
        "evidence_source": "Merchant Center browser RPC products list",
        "evidence_notes": "Current browser product-list row; unknown raw combinations fail closed.",
    }

    has_current_browser_match = bool(language_code and price_currency and source_name)
    if not has_current_browser_match:
        base["evidence_notes"] = "No current USD/en browser RPC match for this Shopify item; fail closed."
        return base

    if source_name != "Shopify App API" or language_code != "en" or price_currency != "USD":
        base["evidence_notes"] = (
            "Browser RPC row is not the expected Shopify App API en/USD product-list row; fail closed."
        )
        return base

    if (
        status_raw == APPROVED_STATUS_RAW
        and aggregated_raw == HEALTHY_AGGREGATED_STATUS_RAW
        and is_healthy_image(image_raw)
        and availability_raw == "0"
        and price
    ):
        base.update(
            {
                "merchant_center_status": "Approved",
                "merchant_center_destination": "Shopping ads eligible",
                "merchant_center_issue_count": "0",
                "merchant_center_issues": "",
                "image_status": "PASS",
                "price_status": "PASS",
                "availability_status": "PASS",
                "shipping_policy_status": "PASS",
                "return_policy_status": "PASS",
                "evidence_notes": (
                    "Browser RPC raw status 4 / aggregate 2 / image 2 was sampled in live Merchant Center "
                    "product details as Approved, Needs attention (0), and Show in ads."
                ),
            }
        )
        return base

    if status_raw == LIMITED_STATUS_RAW:
        base["merchant_center_status"] = "Limited"
        base["merchant_center_destination"] = "Shopping ads limited"
    elif status_raw == NOT_APPROVED_STATUS_RAW:
        base["merchant_center_status"] = "Not approved"
        base["merchant_center_destination"] = "Shopping ads not eligible"
    elif status_raw == APPROVED_STATUS_RAW:
        base["merchant_center_status"] = "Approved"
        base["merchant_center_destination"] = "Shopping ads needs review"

    issue_labels: list[str] = []
    if aggregated_raw == ISSUE_AGGREGATED_STATUS_RAW:
        issue_labels.append("browser_rpc_aggregated_status_attention_raw_5")
    if is_issue_image(image_raw):
        issue_labels.append("browser_rpc_main_image_thumbnail_status_raw_5")
    if status_raw and status_raw != APPROVED_STATUS_RAW:
        issue_labels.append(f"browser_rpc_calculated_status_raw_{status_raw}")

    if issue_labels:
        base["merchant_center_issue_count"] = str(len(issue_labels))
        base["merchant_center_issues"] = "|".join(issue_labels)

    return base


def build_outputs(browser_rpc: Path, output_dir: Path) -> dict[str, object]:
    rows = read_csv(browser_rpc)
    evidence_rows = [browser_row_to_evidence(row) for row in rows]
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "evidence": output_dir / "merchant_center_browser_rpc_evidence.csv",
        "summary": output_dir / "merchant_center_browser_rpc_evidence_summary.json",
    }
    write_csv(paths["evidence"], evidence_rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_MERCHANT_CENTER_BROWSER_RPC_EVIDENCE",
        "browser_rpc_input": str(browser_rpc),
        "browser_rpc_rows": len(rows),
        "evidence_rows": len(evidence_rows),
        "status_counts": dict(Counter(row["merchant_center_status"] for row in evidence_rows).most_common()),
        "issue_rows": sum(
            int(row["merchant_center_issue_count"])
            for row in evidence_rows
            if row["merchant_center_issue_count"].isdigit()
        ),
        "outputs": {key: str(path) for key, path in paths.items()},
        "notes": [
            "Official Merchant/Content API remained blocked by insufficient OAuth scopes.",
            "Only raw status 4 / aggregate 2 / image 2 rows are treated as approved.",
            "All unproven raw combinations fail closed as limited, not approved, or needs data.",
        ],
    }
    paths["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser-rpc", type=Path, default=DEFAULT_BROWSER_RPC)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_outputs(args.browser_rpc, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
