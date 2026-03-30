#!/usr/bin/env python3
"""Export scoped apparel fix candidates from live Merchant Center issue rows.

This bridges the reconciled Merchant Center diagnostics export and the existing
Shopify apparel attribute fill script. It keeps only live Google-published
Shopify offers with current apparel-field issues, then emits one candidate row
per affected product using the audit schema expected by
`fill_shopify_apparel_attributes.py`.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


DEFAULT_RECONCILIATION_CSV = Path(
    "ops/feed-engineering/2026-03-29-phase-3r-mc-issue-reconciliation/merchant_center_issue_reconciliation.csv"
)
DEFAULT_AUDIT_CSV = Path(
    "ops/feed-engineering/2026-03-29-phase-3e-apparel-attribute-audit/apparel_attribute_audit_all.csv"
)
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3s-live-mc-apparel-fix-candidates")

ISSUE_TO_FIELD = {
    "Missing gender": "gender",
    "Missing age group": "age_group",
    "Missing color": "color",
    "Missing size": "size",
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_pipe(values: list[str]) -> str:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        token = " ".join((value or "").split())
        if not token:
            continue
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(token)
    return "|".join(ordered)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export live MC apparel issue candidates for Shopify fills.")
    parser.add_argument("--reconciliation-csv", default=str(DEFAULT_RECONCILIATION_CSV))
    parser.add_argument("--audit-csv", default=str(DEFAULT_AUDIT_CSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    reconciliation_rows = load_csv(Path(args.reconciliation_csv))
    audit_rows = load_csv(Path(args.audit_csv))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    issue_rows_by_handle: dict[str, list[dict[str, str]]] = defaultdict(list)
    issue_counts = Counter()

    for row in reconciliation_rows:
        if row.get("classification") != "live_google_published_shopify_offer":
            continue
        issue_title = row.get("Issue title", "")
        field = ISSUE_TO_FIELD.get(issue_title)
        if not field:
            continue
        handle = (row.get("matched_handle") or row.get("shopify_handle") or "").strip()
        if not handle:
            continue
        issue_rows_by_handle[handle].append(row)
        issue_counts[issue_title] += 1

    audit_by_handle = {row["handle"].strip(): row for row in audit_rows if row.get("handle", "").strip()}

    candidate_rows: list[dict[str, str]] = []
    missing_audit_handles: list[str] = []
    non_apparel_live_issue_rows: list[dict[str, str]] = []
    per_handle_summary_rows: list[dict[str, str]] = []

    for handle in sorted(issue_rows_by_handle):
        audit_row = audit_by_handle.get(handle)
        live_rows = issue_rows_by_handle[handle]
        issue_titles = [row["Issue title"] for row in live_rows]
        live_fields = [ISSUE_TO_FIELD[row["Issue title"]] for row in live_rows if row["Issue title"] in ISSUE_TO_FIELD]
        offer_ids = [row.get("Item ID", "") for row in live_rows]

        if not audit_row:
            missing_audit_handles.append(handle)
            continue

        row = dict(audit_row)
        row["missing_attributes"] = normalize_pipe(live_fields)
        row["live_mc_issues"] = normalize_pipe(issue_titles)
        row["live_mc_offer_ids"] = normalize_pipe(offer_ids)
        row["live_mc_issue_row_count"] = str(len(live_rows))
        candidate_rows.append(row)

        per_handle_summary_rows.append(
            {
                "handle": handle,
                "title": audit_row.get("title", ""),
                "live_mc_issues": row["live_mc_issues"],
                "live_mc_issue_fields": row["missing_attributes"],
                "live_mc_issue_row_count": row["live_mc_issue_row_count"],
                "audit_missing_attributes": audit_row.get("missing_attributes", ""),
                "candidate_gender_confidence": audit_row.get("candidate_gender_confidence", ""),
                "candidate_age_group_confidence": audit_row.get("candidate_age_group_confidence", ""),
                "candidate_color_confidence": audit_row.get("candidate_color_confidence", ""),
                "candidate_size_confidence": audit_row.get("candidate_size_confidence", ""),
            }
        )

    for row in reconciliation_rows:
        if row.get("classification") != "live_google_published_shopify_offer":
            continue
        if row.get("Issue title") in ISSUE_TO_FIELD:
            continue
        non_apparel_live_issue_rows.append(
            {
                "Item ID": row.get("Item ID", ""),
                "Title": row.get("Title", ""),
                "Issue title": row.get("Issue title", ""),
                "matched_handle": row.get("matched_handle", ""),
                "matched_product_id": row.get("matched_product_id", ""),
                "matched_variant_id": row.get("matched_variant_id", ""),
            }
        )

    audit_fieldnames = list(candidate_rows[0].keys()) if candidate_rows else []
    if audit_fieldnames:
        write_csv(output_dir / "live_mc_issue_apparel_candidates.csv", candidate_rows, audit_fieldnames)

    write_csv(
        output_dir / "live_mc_issue_handle_summary.csv",
        per_handle_summary_rows,
        [
            "handle",
            "title",
            "live_mc_issues",
            "live_mc_issue_fields",
            "live_mc_issue_row_count",
            "audit_missing_attributes",
            "candidate_gender_confidence",
            "candidate_age_group_confidence",
            "candidate_color_confidence",
            "candidate_size_confidence",
        ],
    )

    write_csv(
        output_dir / "live_mc_non_apparel_issues.csv",
        non_apparel_live_issue_rows,
        ["Item ID", "Title", "Issue title", "matched_handle", "matched_product_id", "matched_variant_id"],
    )

    summary = {
        "reconciliation_csv": str(Path(args.reconciliation_csv)),
        "audit_csv": str(Path(args.audit_csv)),
        "candidate_products": len(candidate_rows),
        "candidate_issue_rows": sum(len(rows) for rows in issue_rows_by_handle.values()),
        "candidate_issue_counts": dict(issue_counts),
        "missing_audit_handles": missing_audit_handles,
        "non_apparel_live_issue_rows": len(non_apparel_live_issue_rows),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
