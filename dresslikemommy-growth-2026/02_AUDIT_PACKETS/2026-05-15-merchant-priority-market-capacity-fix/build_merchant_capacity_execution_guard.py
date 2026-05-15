#!/usr/bin/env python3
"""Build a no-write execution guard for the Merchant capacity cleanup lane.

The guard turns the local removal-candidate packet into deterministic acceptance
criteria for a future account-capable operator. It can also validate a fresh
after-export when one exists.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


PACKET_DIR = Path(__file__).resolve().parent
SOURCE_EXPORT = (
    PACKET_DIR.parent
    / "2026-05-15-merchant-source-eligibility-browser-rpc-export"
    / "merchant_all_products_browser_rpc_sanitized.csv"
)
CANDIDATE_GROUPS = PACKET_DIR / "merchant_capacity_removal_candidate_groups.csv"
SUMMARY_PATH = PACKET_DIR / "merchant_capacity_execution_guard_summary.json"
PREVIEW_CHECKLIST_CSV = PACKET_DIR / "merchant_capacity_platform_preview_acceptance.csv"
REPORT_PATH = PACKET_DIR / "MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md"

REMOVE_BUCKETS = {
    "REMOVE_AFRICA",
    "REMOVE_ASIA_MIDDLE_EAST",
    "REMOVE_NON_US_USD_REVIEW_FIRST",
    "REMOVE_SOUTH_AMERICA",
}
PROTECTED_PRIORITY_GROUPS = {
    ("US", "en", "USD"): "USA English",
    ("US", "es", "USD"): "USA Spanish",
}
ENABLE_AFTER_CLEANUP_GROUPS = {
    ("CA", "en", "CAD"): "Canada English",
    ("CA", "fr", "CAD"): "Canada French",
    ("GB", "en", "GBP"): "GB English",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("feed_label", ""),
        row.get("language_code", ""),
        row.get("currency", ""),
    )


def summarize_export(rows: list[dict[str, str]]) -> dict[str, object]:
    group_counts: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in rows)
    source_counts: Counter[str] = Counter(row.get("source_id", "") for row in rows)
    priority_counts = {
        label: group_counts.get(key, 0) for key, label in PROTECTED_PRIORITY_GROUPS.items()
    }
    enable_counts = {
        label: group_counts.get(key, 0) for key, label in ENABLE_AFTER_CLEANUP_GROUPS.items()
    }
    return {
        "total_rows": len(rows),
        "priority_counts": priority_counts,
        "enable_after_cleanup_counts": enable_counts,
        "source_counts": dict(sorted(source_counts.items())),
    }


def summarize_candidates(rows: list[dict[str, str]]) -> dict[str, object]:
    bucket_counts: Counter[str] = Counter()
    rows_by_group: list[dict[str, object]] = []
    for row in rows:
        bucket = row["owner_priority_bucket"]
        count = int(row["rows"])
        bucket_counts[bucket] += count
        feed_label, language_code, currency = row["feed_language_currency"].split("|")
        rows_by_group.append(
            {
                "feed_label": feed_label,
                "language_code": language_code,
                "currency": currency,
                "owner_priority_bucket": bucket,
                "expected_rows": count,
            }
        )
    return {
        "candidate_group_count": len(rows),
        "expected_remove_rows": sum(bucket_counts.values()),
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "rows_by_group": rows_by_group,
    }


def validate_after_export(
    after_rows: list[dict[str, str]],
    candidate_groups: list[dict[str, object]],
    before_priority_counts: dict[str, int],
) -> dict[str, object]:
    after_group_counts: Counter[tuple[str, str, str]] = Counter(group_key(row) for row in after_rows)
    remaining_remove_rows = 0
    remaining_by_group: dict[str, int] = {}
    for row in candidate_groups:
        key = (
            str(row["feed_label"]),
            str(row["language_code"]),
            str(row["currency"]),
        )
        count = after_group_counts.get(key, 0)
        if count:
            remaining_by_group["|".join(key)] = count
            remaining_remove_rows += count

    after_priority = {
        label: after_group_counts.get(key, 0) for key, label in PROTECTED_PRIORITY_GROUPS.items()
    }
    protected_failures = {
        label: {"before": before_priority_counts[label], "after": after_priority[label]}
        for label in before_priority_counts
        if after_priority[label] < before_priority_counts[label]
    }
    return {
        "after_total_rows": len(after_rows),
        "remaining_remove_rows": remaining_remove_rows,
        "remaining_remove_groups": remaining_by_group,
        "after_priority_counts": after_priority,
        "protected_failures": protected_failures,
        "passed": remaining_remove_rows == 0 and not protected_failures,
    }


def write_preview_csv(rows_by_group: list[dict[str, object]]) -> None:
    fieldnames = [
        "check_type",
        "feed_label",
        "language_code",
        "currency",
        "expected_rows",
        "required_result_before_save",
    ]
    with PREVIEW_CHECKLIST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows_by_group:
            writer.writerow(
                {
                    "check_type": "remove_exact_group",
                    "feed_label": row["feed_label"],
                    "language_code": row["language_code"],
                    "currency": row["currency"],
                    "expected_rows": row["expected_rows"],
                    "required_result_before_save": "selected_for_removal_or_disabled_from_google_publishing_scope",
                }
            )
        for key, label in PROTECTED_PRIORITY_GROUPS.items():
            writer.writerow(
                {
                    "check_type": "protect_priority_group",
                    "feed_label": key[0],
                    "language_code": key[1],
                    "currency": key[2],
                    "expected_rows": "",
                    "required_result_before_save": f"must_remain_enabled_for_{label.replace(' ', '_')}",
                }
            )
        for key, label in ENABLE_AFTER_CLEANUP_GROUPS.items():
            writer.writerow(
                {
                    "check_type": "enable_after_capacity_cleanup",
                    "feed_label": key[0],
                    "language_code": key[1],
                    "currency": key[2],
                    "expected_rows": "0_currently_absent",
                    "required_result_before_save": f"do_not_build_shopping_until_{label.replace(' ', '_')}_rows_export",
                }
            )


def write_report(summary: dict[str, object], after_validation: dict[str, object] | None) -> None:
    candidate = summary["candidate_summary"]
    source = summary["source_export_summary"]
    bucket_counts = candidate["bucket_counts"]
    after_text = "No after-export was supplied; this run generated preflight acceptance criteria only."
    if after_validation is not None:
        status = "PASSED" if after_validation["passed"] else "FAILED"
        after_text = (
            f"After-export validation: `{status}`. Remaining removal rows: "
            f"`{after_validation['remaining_remove_rows']}`. Protected failures: "
            f"`{len(after_validation['protected_failures'])}`."
        )

    report = f"""# Merchant Priority Market Capacity Execution Guard

Mode: local/read-only guardrail for the Merchant capacity cleanup lane. No Merchant,
Shopify, Google Ads, Pinterest, feed, product, product-group, bid, budget, status,
capacity, billing, credential, or conversion writes were made.

## Purpose

The live capacity cleanup may proceed only if an authenticated platform preview can
match the exact non-priority removal groups from the packet and preserve the priority
USA English and USA Spanish groups. This guard converts the packet into runnable
acceptance criteria so the future live operator does not remove the wrong market.

## Current Before-State

- Current all-products rows: `{source['total_rows']}`.
- Expected first-pass removal rows: `{candidate['expected_remove_rows']}`.
- Expected after-removal row floor if only this first pass is removed: `{summary['expected_after_first_pass_rows']}`.
- Candidate group count: `{candidate['candidate_group_count']}`.
- Protected USA English rows: `{source['priority_counts']['USA English']}`.
- Protected USA Spanish rows: `{source['priority_counts']['USA Spanish']}`.
- Canada English rows now: `{source['enable_after_cleanup_counts']['Canada English']}`.
- Canada French rows now: `{source['enable_after_cleanup_counts']['Canada French']}`.
- GB English rows now: `{source['enable_after_cleanup_counts']['GB English']}`.

## Removal Buckets

| Bucket | Rows |
|---|---:|
| REMOVE_ASIA_MIDDLE_EAST | `{bucket_counts.get('REMOVE_ASIA_MIDDLE_EAST', 0)}` |
| REMOVE_AFRICA | `{bucket_counts.get('REMOVE_AFRICA', 0)}` |
| REMOVE_SOUTH_AMERICA | `{bucket_counts.get('REMOVE_SOUTH_AMERICA', 0)}` |
| REMOVE_NON_US_USD_REVIEW_FIRST | `{bucket_counts.get('REMOVE_NON_US_USD_REVIEW_FIRST', 0)}` |

## Before-Save Acceptance Criteria

Use `merchant_capacity_platform_preview_acceptance.csv` against the authenticated
Merchant/Shopify/Google publishing control surface before any Save, Apply, Sync, or
Upload:

1. Every `remove_exact_group` row is selected only for removal or disablement from
   Google/Merchant publishing scope.
2. `US|en|USD` and `US|es|USD` remain enabled and unselected for removal.
3. Europe-later groups are not part of the first pass.
4. Canada English/French and GB English are not treated as ready; current export rows
   are `0`, so they require enablement and a fresh export after capacity cleanup.
5. The action is market/feed-country publishing cleanup only, not product deletion.

Stop if the platform preview cannot be reconciled to the CSV.

## After-Export Validation

Run this guard again with `--after-export /path/to/fresh_export.csv` after the live
cleanup. It will fail closed if any first-pass removal group remains or if USA
English/Spanish row counts drop below the current before-state.

{after_text}

## Files

- `merchant_capacity_platform_preview_acceptance.csv`
- `merchant_capacity_execution_guard_summary.json`
- `merchant_capacity_removal_candidate_groups.csv`
- `merchant_priority_market_capacity_fix_summary.json`
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--after-export", type=Path)
    args = parser.parse_args()

    source_rows = read_csv(SOURCE_EXPORT)
    candidate_rows = read_csv(CANDIDATE_GROUPS)
    source_summary = summarize_export(source_rows)
    candidate_summary = summarize_candidates(candidate_rows)
    expected_after = source_summary["total_rows"] - candidate_summary["expected_remove_rows"]

    after_validation = None
    if args.after_export:
        after_validation = validate_after_export(
            read_csv(args.after_export),
            candidate_summary["rows_by_group"],
            source_summary["priority_counts"],
        )

    write_preview_csv(candidate_summary["rows_by_group"])
    summary = {
        "mode": "local_readonly_no_external_writes",
        "source_export": str(SOURCE_EXPORT.relative_to(Path.cwd())),
        "candidate_groups": str(CANDIDATE_GROUPS.relative_to(Path.cwd())),
        "source_export_summary": source_summary,
        "candidate_summary": {
            key: value
            for key, value in candidate_summary.items()
            if key != "rows_by_group"
        },
        "expected_after_first_pass_rows": expected_after,
        "after_validation": after_validation,
        "preview_acceptance_csv": str(PREVIEW_CHECKLIST_CSV.relative_to(Path.cwd())),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summary, after_validation)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
