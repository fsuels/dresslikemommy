#!/usr/bin/env python3
"""Build the approved Merchant label-precedence repair overlay.

This prepares the replacement file for Merchant supplemental source
10626787326 / supplemental_feed_pilot.txt. It preserves the existing
non-parent rows and age_group values from the last repo-backed source file,
then changes only approved parent-outfit offer IDs to the parent-outfit label
contract.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
BASE_SOURCE_CSV = (
    PACKET_DIR.parents[0]
    / "2026-04-29-merchant-clean-label-upload"
    / "upload_matched_full_clean_labels_with_age_group.csv"
)
SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
OUTPUT_CSV = PACKET_DIR / "google_shopping_parent_outfit_label_precedence_repair_10626787326.csv"
OUTPUT_TSV = PACKET_DIR / "google_shopping_parent_outfit_label_precedence_repair_10626787326.txt"
SUMMARY_JSON = PACKET_DIR / "google_shopping_parent_outfit_label_precedence_repair_10626787326_summary.json"

FIELDNAMES = [
    "id",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
    "age_group",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_rows(path: Path, rows: list[dict[str, str]], delimiter: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    base_rows = read_csv(BASE_SOURCE_CSV)
    spec_rows = [row for row in read_csv(SPEC_CSV) if row["decision"] == "INCLUDE"]
    spec_by_id = {row["item_id"]: row for row in spec_rows}
    base_by_id = {row["id"]: row for row in base_rows}

    output_by_id: dict[str, dict[str, str]] = {}
    changed_existing = 0
    preserved_existing_parent = 0
    preserved_non_parent = 0

    for row in base_rows:
        item_id = row["id"]
        next_row = {field: row.get(field, "") for field in FIELDNAMES}
        if item_id in spec_by_id:
            spec = spec_by_id[item_id]
            before = {field: next_row[field] for field in FIELDNAMES}
            next_row.update(
                {
                    "custom_label_0": spec["proposed_custom_label_0"],
                    "custom_label_1": spec["proposed_custom_label_1"],
                    "custom_label_2": spec["proposed_custom_label_2"],
                    "custom_label_3": spec["proposed_custom_label_3"],
                    "custom_label_4": spec["proposed_custom_label_4"],
                }
            )
            changed_existing += before != next_row
            preserved_existing_parent += before == next_row
        else:
            preserved_non_parent += 1
        output_by_id[item_id] = next_row

    added_parent_rows = 0
    for item_id, spec in spec_by_id.items():
        if item_id in output_by_id:
            continue
        output_by_id[item_id] = {
            "id": item_id,
            "custom_label_0": spec["proposed_custom_label_0"],
            "custom_label_1": spec["proposed_custom_label_1"],
            "custom_label_2": spec["proposed_custom_label_2"],
            "custom_label_3": spec["proposed_custom_label_3"],
            "custom_label_4": spec["proposed_custom_label_4"],
            # No age_group value is known from source 10626787326 for newly
            # added rows, so do not synthesize one.
            "age_group": "",
        }
        added_parent_rows += 1

    rows = [output_by_id[item_id] for item_id in sorted(output_by_id)]
    write_rows(OUTPUT_CSV, rows, ",")
    write_rows(OUTPUT_TSV, rows, "\t")

    parent_ids = set(spec_by_id)
    summary: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "MERCHANT_LABEL_PRECEDENCE_REPAIR_PREPARED",
        "target_merchant_center_account": "124884876",
        "target_source_id": "10626787326",
        "target_source_name": "supplemental_feed_pilot.txt",
        "base_source_csv": str(BASE_SOURCE_CSV),
        "approved_spec_csv": str(SPEC_CSV),
        "output_csv": str(OUTPUT_CSV),
        "output_txt": str(OUTPUT_TSV),
        "base_rows": len(base_rows),
        "approved_parent_rows": len(spec_rows),
        "output_rows": len(rows),
        "approved_parent_rows_already_in_base": len(parent_ids & set(base_by_id)),
        "approved_parent_rows_added_to_source": added_parent_rows,
        "base_non_parent_rows_preserved": preserved_non_parent,
        "base_parent_rows_changed": changed_existing,
        "base_parent_rows_already_matching": preserved_existing_parent,
        "blank_age_group_rows": sum(1 for row in rows if not row["age_group"]),
        "blank_age_group_approved_parent_rows": sum(1 for row in rows if row["id"] in parent_ids and not row["age_group"]),
        "custom_label_0_counts": dict(sorted(Counter(row["custom_label_0"] for row in rows).items())),
        "custom_label_1_counts": dict(sorted(Counter(row["custom_label_1"] for row in rows).items())),
        "custom_label_2_counts": dict(sorted(Counter(row["custom_label_2"] for row in rows).items())),
        "custom_label_3_counts": dict(sorted(Counter(row["custom_label_3"] for row in rows).items())),
        "custom_label_4_counts": dict(sorted(Counter(row["custom_label_4"] for row in rows).items())),
        "age_group_counts": dict(sorted(Counter(row["age_group"] for row in rows).items())),
        "guardrails": [
            "Local file preparation only.",
            "No Merchant upload in this script.",
            "No Google Ads campaign, budget, bid, status, product-group, conversion, or billing change.",
            "No Shopify title, price, handle, body, SEO, inventory, or publication change.",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
