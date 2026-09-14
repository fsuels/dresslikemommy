#!/usr/bin/env python3
"""Build exact current repair artifacts for the remaining parent-outfit gate.

This is a local artifact builder only. It performs no Merchant, Shopify,
Google & YouTube, Google Ads, budget, bid, status, product-group, conversion,
billing, publication, inventory, price, title, handle, SEO, broad-sync, or
source-reset write.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKET_DIR = Path(__file__).resolve().parent
SPEC_CSV = PACKET_DIR / "merchant_label_update_spec.csv"
READY_LABEL = "us_parent_outfit_ready_v20260520"


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def latest_path(pattern: str) -> Path:
    paths = sorted(PACKET_DIR.glob(pattern))
    if not paths:
        raise FileNotFoundError(f"No files matched {pattern}")
    return paths[-1]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str], delimiter: str = ",") -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=delimiter, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def labels_blank(row: dict[str, str]) -> bool:
    return all(not row.get(f"custom_label_{index}", "").strip() for index in range(5))


def labels_ready(row: dict[str, str]) -> bool:
    return row.get("custom_label_4") == READY_LABEL


def overlay_row(spec: dict[str, str]) -> dict[str, str]:
    return {
        "id": spec["item_id"],
        "item_group_id": spec["proposed_item_group_id"],
        "image_link": spec["proposed_image_link"],
        "custom_label_0": spec["proposed_custom_label_0"],
        "custom_label_1": spec["proposed_custom_label_1"],
        "custom_label_2": spec["proposed_custom_label_2"],
        "custom_label_3": spec["proposed_custom_label_3"],
        "custom_label_4": spec["proposed_custom_label_4"],
    }


def report_markdown(payload: dict[str, Any]) -> str:
    files = payload["files"]
    counts = payload["counts"]
    return f"""# Google Shopping Parent-Outfit Remaining Eligibility Repair Artifacts

Generated: `{payload['generated_at_utc']}`

Mode: local artifact build only. No external write occurred.

## Current Scope

- Approved source spec rows: `{counts['included_spec_rows']}`
- Ads-visible non-ready rows: `{counts['ads_visible_non_ready_rows']}`
- Ads-visible blank-label repair rows: `{counts['blank_label_repair_rows']}`
- Ads-absent presence repair rows: `{counts['ads_absent_presence_repair_rows']}`
- Out-of-stock holdout rows: `{counts['out_of_stock_holdout_rows']}`
- Strict spec after only out-of-stock holdout: `{counts['strict_spec_after_oos_holdout_rows']}`

## Row Split

- Blank-label rows by parent: `{payload['blank_label_rows_by_parent']}`
- Missing rows by parent: `{payload['missing_rows_by_parent']}`
- Out-of-stock rows by parent: `{payload['out_of_stock_rows_by_parent']}`

## Files

- Blank-label TSV overlay: `{files['blank_label_overlay_tsv']}`
- Blank-label CSV evidence: `{files['blank_label_repair_csv']}`
- Ads-absent presence CSV evidence: `{files['ads_absent_presence_csv']}`
- Out-of-stock holdout CSV: `{files['out_of_stock_holdout_csv']}`
- Strict spec excluding only out-of-stock rows: `{files['strict_spec_after_oos_holdout_csv']}`
- JSON summary: `{files['json']}`

## Guardrails

- All Shopping campaigns remain paused.
- No activation discussion is allowed from this artifact.
- The out-of-stock holdout does not change Shopify inventory.
- The blank-label TSV contains only current Ads-visible blank-label rows.
- The Ads-absent file is evidence for the narrow presence repair lane; it is not a broad sync authorization.
"""


def main() -> int:
    generated_at = stamp()
    present_csv = latest_path("google_shopping_parent_outfit_eligibility_present_rows_*.csv")
    missing_csv = latest_path("google_shopping_parent_outfit_eligibility_missing_rows_*.csv")
    diagnostic_json = latest_path("google_shopping_parent_outfit_eligibility_diagnostic_*.json")

    spec_rows = load_csv(SPEC_CSV)
    included_spec = [row for row in spec_rows if row.get("decision") == "INCLUDE"]
    spec_by_id = {row["item_id"]: row for row in included_spec}
    present_rows = load_csv(present_csv)
    missing_rows = load_csv(missing_csv)

    non_ready_rows = [row for row in present_rows if row.get("has_ready_label") == "false"]
    blank_label_rows = [row for row in non_ready_rows if labels_blank(row)]
    non_blank_non_ready = [row for row in non_ready_rows if not labels_blank(row)]
    out_of_stock_rows = [row for row in present_rows if row.get("availability") == "OUT_OF_STOCK"]

    missing_ids = {row["item_id"] for row in missing_rows}
    blank_ids = {row["item_id"] for row in blank_label_rows}
    out_of_stock_ids = {row["item_id"] for row in out_of_stock_rows}

    unknown_ids = (missing_ids | blank_ids | out_of_stock_ids) - set(spec_by_id)
    if unknown_ids:
        raise RuntimeError(f"Current repair rows outside included spec: {sorted(unknown_ids)[:20]}")
    if non_blank_non_ready:
        raise RuntimeError(f"Found non-ready rows with non-blank labels: {len(non_blank_non_ready)}")

    blank_overlay_rows = [overlay_row(spec_by_id[row["item_id"]]) for row in blank_label_rows]
    strict_spec_after_oos = []
    for row in spec_rows:
        next_row = dict(row)
        if row.get("decision") == "INCLUDE" and row.get("item_id") in out_of_stock_ids:
            next_row["decision"] = "EXCLUDE"
            next_row["reason"] = "EXCLUDE_OUT_OF_STOCK_HOLDOUT_20260521"
        strict_spec_after_oos.append(next_row)

    prefix = f"20260521T{generated_at[9:15]}Z"
    blank_tsv = PACKET_DIR / f"google_shopping_parent_outfit_blank_label_overlay_{prefix}.tsv"
    blank_csv = PACKET_DIR / f"google_shopping_parent_outfit_blank_label_repair_scope_{prefix}.csv"
    missing_out = PACKET_DIR / f"google_shopping_parent_outfit_ads_absent_presence_repair_scope_{prefix}.csv"
    oos_out = PACKET_DIR / f"google_shopping_parent_outfit_out_of_stock_holdout_scope_{prefix}.csv"
    reduced_spec = PACKET_DIR / f"merchant_label_update_spec_excluding_oos_holdout_{prefix}.csv"
    output_json = PACKET_DIR / f"google_shopping_parent_outfit_remaining_eligibility_repair_artifacts_{prefix}.json"
    report_md = PACKET_DIR / f"GOOGLE_SHOPPING_PARENT_OUTFIT_REMAINING_ELIGIBILITY_REPAIR_ARTIFACTS_{prefix}.md"

    overlay_fields = ["id", "item_group_id", "image_link", "custom_label_0", "custom_label_1", "custom_label_2", "custom_label_3", "custom_label_4"]
    write_csv(blank_tsv, blank_overlay_rows, overlay_fields, delimiter="\t")
    write_csv(blank_csv, blank_label_rows, list(blank_label_rows[0].keys()) if blank_label_rows else list(present_rows[0].keys()))
    write_csv(missing_out, missing_rows, list(missing_rows[0].keys()) if missing_rows else [])
    write_csv(oos_out, out_of_stock_rows, list(out_of_stock_rows[0].keys()) if out_of_stock_rows else list(present_rows[0].keys()))
    write_csv(reduced_spec, strict_spec_after_oos, list(spec_rows[0].keys()))

    payload: dict[str, Any] = {
        "generated_at_utc": generated_at,
        "mode": "local_artifact_build_only",
        "inputs": {
            "spec_csv": SPEC_CSV.name,
            "present_csv": present_csv.name,
            "missing_csv": missing_csv.name,
            "diagnostic_json": diagnostic_json.name,
        },
        "counts": {
            "included_spec_rows": len(included_spec),
            "ads_visible_non_ready_rows": len(non_ready_rows),
            "blank_label_repair_rows": len(blank_label_rows),
            "ads_absent_presence_repair_rows": len(missing_rows),
            "out_of_stock_holdout_rows": len(out_of_stock_rows),
            "strict_spec_after_oos_holdout_rows": sum(1 for row in strict_spec_after_oos if row.get("decision") == "INCLUDE"),
        },
        "blank_label_rows_by_parent": dict(Counter(row["parent_product_id"] for row in blank_label_rows).most_common()),
        "missing_rows_by_parent": dict(Counter(row["parent_product_id"] for row in missing_rows).most_common()),
        "out_of_stock_rows_by_parent": dict(Counter(row["parent_product_id"] for row in out_of_stock_rows).most_common()),
        "files": {
            "blank_label_overlay_tsv": blank_tsv.name,
            "blank_label_repair_csv": blank_csv.name,
            "ads_absent_presence_csv": missing_out.name,
            "out_of_stock_holdout_csv": oos_out.name,
            "strict_spec_after_oos_holdout_csv": reduced_spec.name,
            "json": output_json.name,
            "report_md": report_md.name,
        },
        "guardrails": [
            "No external write occurred.",
            "No campaign, budget, bid, status, product-group, conversion, billing, or activation change.",
            "No Shopify product, publication, inventory, price, title, handle, body, or SEO change.",
            "No broad Google & YouTube sync, source reset, or product recreation.",
        ],
    }
    write_json(output_json, payload)
    report_md.write_text(report_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
