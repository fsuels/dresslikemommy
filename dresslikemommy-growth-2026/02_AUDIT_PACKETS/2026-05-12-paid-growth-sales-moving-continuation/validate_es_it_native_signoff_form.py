#!/usr/bin/env python3
"""Validate the ES/IT Golden Daisy native review signoff form.

This is local-only. It does not upload or mutate Google Ads.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation")
FORM = BASE / "ES_IT_GOLDEN_DAISY_NATIVE_REVIEW_SIGNOFF_FORM.csv"
SUMMARY = BASE / "es_it_golden_daisy_native_review_signoff_validation_summary.json"

ALLOWED_VERDICTS = {
    "PENDING_NATIVE_REVIEW",
    "APPROVED_NATIVE",
    "APPROVED_WITH_EDITS",
    "REJECTED_REWRITE_REQUIRED",
}
READY_VERDICTS = {"APPROVED_NATIVE", "APPROVED_WITH_EDITS"}
EXPECTED_ROW_IDS = {
    "ES-KW-01",
    "ES-KW-02",
    "ES-KW-03",
    "ES-RSA-01",
    "IT-KW-01",
    "IT-KW-02",
    "IT-KW-03",
    "IT-RSA-01",
}


def main() -> int:
    rows = list(csv.DictReader(FORM.open(newline="", encoding="utf-8")))
    row_ids = {row["row_id"] for row in rows}
    checks = []

    def check(name: str, passed: bool, observed, expected) -> None:
        checks.append({"check": name, "status": "PASS" if passed else "FAIL", "observed": observed, "expected": expected})

    check("row_count", len(rows) == 8, len(rows), 8)
    check("row_ids", row_ids == EXPECTED_ROW_IDS, sorted(row_ids), sorted(EXPECTED_ROW_IDS))
    check("markets", {row["market"] for row in rows} == {"ES", "IT"}, sorted({row["market"] for row in rows}), ["ES", "IT"])
    check("asset_types", {row["asset_type"] for row in rows} == {"keyword", "rsa"}, sorted({row["asset_type"] for row in rows}), ["keyword", "rsa"])
    invalid_verdicts = sorted({row["reviewer_verdict"] for row in rows}.difference(ALLOWED_VERDICTS))
    check("allowed_verdicts", not invalid_verdicts, invalid_verdicts, sorted(ALLOWED_VERDICTS))
    edit_rows_missing_replacement = [
        row["row_id"]
        for row in rows
        if row["reviewer_verdict"] == "APPROVED_WITH_EDITS" and not row["replacement_text"].strip()
    ]
    check("approved_with_edits_have_replacement", not edit_rows_missing_replacement, edit_rows_missing_replacement, [])
    rejected_rows_missing_notes = [
        row["row_id"]
        for row in rows
        if row["reviewer_verdict"] == "REJECTED_REWRITE_REQUIRED" and not row["reviewer_notes"].strip()
    ]
    check("rejected_rows_have_notes", not rejected_rows_missing_notes, rejected_rows_missing_notes, [])

    pending_rows = [row["row_id"] for row in rows if row["reviewer_verdict"] == "PENDING_NATIVE_REVIEW"]
    rejected_rows = [row["row_id"] for row in rows if row["reviewer_verdict"] == "REJECTED_REWRITE_REQUIRED"]
    platform_use_ready = (
        not pending_rows
        and not rejected_rows
        and all(row["reviewer_verdict"] in READY_VERDICTS for row in rows)
        and all(check["status"] == "PASS" for check in checks)
    )

    if platform_use_ready:
        status = "NATIVE_SIGNOFF_COMPLETE_REVIEW_ONLY_READY_FOR_OWNER_APPROVAL"
    elif any(check["status"] == "FAIL" for check in checks):
        status = "SIGNOFF_FORM_INVALID"
    else:
        status = "PENDING_NATIVE_REVIEW"

    summary = {
        "status": status,
        "platform_use_ready": platform_use_ready,
        "pending_rows": pending_rows,
        "rejected_rows": rejected_rows,
        "checks": checks,
        "guardrail": "This validator does not authorize Google Ads platform use; exact owner action-time approval is still required.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if status != "SIGNOFF_FORM_INVALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
