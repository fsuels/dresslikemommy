#!/usr/bin/env python3
"""Build a matched-only Merchant Center full custom-label upload.

This keeps the current age_group supplemental fix while replacing the older
custom-label values with the clean Shopping test schema.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


DEFAULT_CLEAN_LABELS = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/"
    "google_shopping_us_clean_subset_supplemental_labels.csv"
)
DEFAULT_CURRENT_MATCHED = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-merchant-age-group-fix/upload_matched_age_group_with_paid_status.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-merchant-clean-label-upload"
)

UPLOAD_FIELDS = [
    "id",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
    "age_group",
]
ROLLBACK_FIELDS = ["id", "custom_label_4", "age_group"]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str], *, delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n", delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def build_outputs(clean_labels_path: Path, current_matched_path: Path, output_dir: Path) -> dict[str, object]:
    clean_rows = read_csv(clean_labels_path)
    current_rows = read_csv(current_matched_path)

    clean_by_id = {clean(row.get("id")): row for row in clean_rows if clean(row.get("id"))}
    current_by_id = {clean(row.get("id")): row for row in current_rows if clean(row.get("id"))}

    upload_rows: list[dict[str, str]] = []
    missing_from_clean: list[dict[str, str]] = []
    for item_id in sorted(current_by_id):
        clean_row = clean_by_id.get(item_id)
        current_row = current_by_id[item_id]
        if not clean_row:
            missing_from_clean.append({"id": item_id, "reason": "matched_current_source_id_missing_from_clean_label_plan"})
            continue
        upload_rows.append(
            {
                "id": item_id,
                "custom_label_0": clean(clean_row.get("custom_label_0")),
                "custom_label_1": clean(clean_row.get("custom_label_1")),
                "custom_label_2": clean(clean_row.get("custom_label_2")),
                "custom_label_3": clean(clean_row.get("custom_label_3")),
                "custom_label_4": clean(clean_row.get("custom_label_4")),
                "age_group": clean(current_row.get("age_group")),
            }
        )

    excluded_stale_rows = [
        {"id": item_id, "reason": "not_in_current_matched_source_rows"}
        for item_id in sorted(set(clean_by_id) - set(current_by_id))
    ]
    rollback_rows = [
        {
            "id": clean(row.get("id")),
            "custom_label_4": clean(row.get("custom_label_4")),
            "age_group": clean(row.get("age_group")),
        }
        for row in current_rows
        if clean(row.get("id"))
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    upload_csv = output_dir / "upload_matched_full_clean_labels_with_age_group.csv"
    upload_txt = output_dir / "upload_matched_full_clean_labels_with_age_group.txt"
    rollback_csv = output_dir / "rollback_restore_custom_label_4_age_group.csv"
    excluded_csv = output_dir / "excluded_stale_or_unmatched_ids.csv"
    missing_csv = output_dir / "matched_ids_missing_from_clean_label_plan.csv"
    summary_path = output_dir / "summary.json"

    write_csv(upload_csv, upload_rows, UPLOAD_FIELDS)
    write_csv(upload_txt, upload_rows, UPLOAD_FIELDS, delimiter="\t")
    write_csv(rollback_csv, rollback_rows, ROLLBACK_FIELDS)
    write_csv(excluded_csv, excluded_stale_rows, ["id", "reason"])
    write_csv(missing_csv, missing_from_clean, ["id", "reason"])

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "MERCHANT_CENTER_MATCHED_FULL_CLEAN_LABEL_UPLOAD_PREPARED",
        "target_merchant_center_account": "124884876",
        "target_source_id": "10626787326",
        "target_source_name": "supplemental_feed_pilot.txt",
        "write_scope": "Replace manual supplemental source with matched-only id, custom_label_0..4, age_group rows.",
        "clean_label_input": str(clean_labels_path),
        "current_matched_input": str(current_matched_path),
        "clean_label_rows": len(clean_rows),
        "current_matched_rows": len(current_rows),
        "upload_rows": len(upload_rows),
        "rollback_rows": len(rollback_rows),
        "excluded_stale_or_unmatched_rows": len(excluded_stale_rows),
        "matched_ids_missing_from_clean_label_plan": len(missing_from_clean),
        "upload_custom_label_0_counts": dict(Counter(row["custom_label_0"] for row in upload_rows)),
        "upload_custom_label_1_counts": dict(Counter(row["custom_label_1"] for row in upload_rows)),
        "upload_custom_label_2_counts": dict(Counter(row["custom_label_2"] for row in upload_rows)),
        "upload_custom_label_3_counts": dict(Counter(row["custom_label_3"] for row in upload_rows)),
        "upload_custom_label_4_counts": dict(Counter(row["custom_label_4"] for row in upload_rows)),
        "upload_age_group_counts": dict(Counter(row["age_group"] for row in upload_rows)),
        "files": {
            "upload_csv": str(upload_csv),
            "upload_txt": str(upload_txt),
            "rollback_csv": str(rollback_csv),
            "excluded_stale_or_unmatched_ids": str(excluded_csv),
            "matched_ids_missing_from_clean_label_plan": str(missing_csv),
            "summary": str(summary_path),
        },
        "notes": [
            "Use the tab-delimited .txt file for Merchant Center manual source upload.",
            "The upload intentionally excludes known unmatched/stale offers so source processing stays clean.",
            "Rollback restores the prior matched-only source shape: id, custom_label_4, age_group.",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean-labels", type=Path, default=DEFAULT_CLEAN_LABELS)
    parser.add_argument("--current-matched", type=Path, default=DEFAULT_CURRENT_MATCHED)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps(build_outputs(args.clean_labels, args.current_matched, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
