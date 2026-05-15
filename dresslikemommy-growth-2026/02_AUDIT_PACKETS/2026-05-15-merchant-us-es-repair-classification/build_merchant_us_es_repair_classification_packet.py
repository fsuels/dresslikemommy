#!/usr/bin/env python3
"""Build a no-write Merchant US/es issue classification packet."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback"
OUT_DIR = Path(__file__).resolve().parent
ISSUE_ROWS = SOURCE_DIR / "merchant_shopping_target_issue_rows.csv"


ISSUE_ACTIONS = {
    "Over capacity for Shopping ads (outside of CSS program)": (
        "capacity_scope_decision_required",
        "Do not remove products or request capacity from this export alone; first capture full source/all-products proof and owner decision.",
    ),
    "Missing age group": (
        "attribute_repair_candidate",
        "Candidate for source/product attribute repair only after full source export proves exact rows and owner approves feed/product changes.",
    ),
    "Missing color": (
        "attribute_repair_candidate",
        "Candidate for source/product attribute repair only after full source export proves exact rows and owner approves feed/product changes.",
    ),
    "Missing gender": (
        "attribute_repair_candidate",
        "Candidate for source/product attribute repair only after full source export proves exact rows and owner approves feed/product changes.",
    ),
    "Missing size": (
        "attribute_repair_candidate",
        "Candidate for source/product attribute repair only after full source export proves exact rows and owner approves feed/product changes.",
    ),
    "Product page unavailable": (
        "landing_or_product_status_recheck_required",
        "Public/admin product availability must be rechecked before any product/feed repair decision.",
    ),
    "Missing product image": (
        "image_or_feed_recheck_required",
        "Product/image source must be rechecked before any image/feed repair decision.",
    ),
}


def read_rows() -> list[dict[str, str]]:
    with ISSUE_ROWS.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def unique_join(values: list[str]) -> str:
    return " | ".join(sorted({value for value in values if value}))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    rows = read_rows()
    item_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_issue: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        item_rows[row["item_id"]].append(row)
        by_issue[row["issue_title"]].append(row)

    issue_summary = []
    for issue_title, issue_rows in sorted(by_issue.items()):
        item_ids = {row["item_id"] for row in issue_rows}
        paid_item_ids = {row["item_id"] for row in issue_rows if row["in_paid_cohort"] == "yes"}
        statuses = Counter(row["item_status"] for row in issue_rows)
        severities = Counter(row["issue_severity"] for row in issue_rows)
        traffic_types = Counter(row["traffic_type"] for row in issue_rows)
        action_class, repair_gate = ISSUE_ACTIONS.get(
            issue_title,
            ("manual_review_required", "Classify manually before any external write."),
        )
        issue_summary.append(
            {
                "issue_title": issue_title,
                "issue_rows": len(issue_rows),
                "unique_items": len(item_ids),
                "paid_cohort_items": len(paid_item_ids),
                "traffic_types": " | ".join(f"{key}: {value}" for key, value in sorted(traffic_types.items())),
                "statuses": " | ".join(f"{key}: {value}" for key, value in sorted(statuses.items())),
                "severities": " | ".join(f"{key}: {value}" for key, value in sorted(severities.items())),
                "action_class": action_class,
                "repair_gate": repair_gate,
            }
        )

    paid_item_summaries = []
    for item_id, item_issue_rows in sorted(item_rows.items()):
        if not any(row["in_paid_cohort"] == "yes" for row in item_issue_rows):
            continue
        issues = [row["issue_title"] for row in item_issue_rows]
        paid_item_summaries.append(
            {
                "item_id": item_id,
                "title": item_issue_rows[0]["title"],
                "issue_count": len(item_issue_rows),
                "unique_issue_titles": unique_join(issues),
                "shopping_ads_rows": sum(1 for row in item_issue_rows if row["traffic_type"] == "Shopping ads"),
                "dynamic_remarketing_rows": sum(1 for row in item_issue_rows if row["traffic_type"] == "Dynamic remarketing"),
                "free_listings_rows": sum(1 for row in item_issue_rows if row["traffic_type"] == "Free listings"),
                "item_statuses": unique_join([row["item_status"] for row in item_issue_rows]),
                "severities": unique_join([row["issue_severity"] for row in item_issue_rows]),
                "next_gate": "full_source_export_then_owner_approval_before_repair",
            }
        )

    issue_summary_path = OUT_DIR / "merchant_us_es_repair_scope_by_issue.csv"
    paid_items_path = OUT_DIR / "merchant_us_es_paid_cohort_priority_items.csv"
    summary_path = OUT_DIR / "merchant_us_es_repair_classification_summary.json"
    report_path = OUT_DIR / "MERCHANT_US_ES_NO_WRITE_REPAIR_CLASSIFICATION_PACKET.md"

    write_csv(
        issue_summary_path,
        [
            "issue_title",
            "issue_rows",
            "unique_items",
            "paid_cohort_items",
            "traffic_types",
            "statuses",
            "severities",
            "action_class",
            "repair_gate",
        ],
        issue_summary,
    )
    write_csv(
        paid_items_path,
        [
            "item_id",
            "title",
            "issue_count",
            "unique_issue_titles",
            "shopping_ads_rows",
            "dynamic_remarketing_rows",
            "free_listings_rows",
            "item_statuses",
            "severities",
            "next_gate",
        ],
        paid_item_summaries,
    )

    attribute_issue_titles = ["Missing age group", "Missing color", "Missing gender", "Missing size"]
    attribute_paid_items = sorted(
        {
            row["item_id"]
            for title in attribute_issue_titles
            for row in by_issue.get(title, [])
            if row["in_paid_cohort"] == "yes"
        }
    )
    blocked_paid_items = sorted({row["item_id"] for row in rows if row["in_paid_cohort"] == "yes"})
    summary = {
        "action": "NO_WRITE_REPAIR_CLASSIFICATION_PACKET",
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "input_issue_rows": str(ISSUE_ROWS),
        "market": "US",
        "language": "es",
        "issue_rows": len(rows),
        "unique_items": len(item_rows),
        "paid_cohort_issue_items": len(blocked_paid_items),
        "paid_cohort_attribute_repair_candidates": len(attribute_paid_items),
        "issue_titles": {row["issue_title"]: int(row["issue_rows"]) for row in issue_summary},
        "outputs": {
            "issue_scope_csv": str(issue_summary_path),
            "paid_cohort_items_csv": str(paid_items_path),
            "report": str(report_path),
        },
        "guardrails": [
            "No Merchant upload, source sync, source edit, product edit, capacity request, campaign build, budget, bid, status, product-group, product-scope, title/feed, conversion, billing, Shopify Admin, Pinterest, or live theme write occurred.",
            "Full all-products/source export is required before any repair/build decision because the issue export lacks source_id.",
            "Owner approval is required before any feed/product/source/capacity action.",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    top_paid = paid_item_summaries[:15]
    issue_table = "\n".join(
        f"| {row['issue_title']} | {row['issue_rows']} | {row['unique_items']} | {row['paid_cohort_items']} | {row['action_class']} |"
        for row in issue_summary
    )
    paid_table = "\n".join(
        f"| `{row['item_id']}` | {row['issue_count']} | {row['unique_issue_titles']} |"
        for row in top_paid
    )
    report = f"""# Merchant US/es No-Write Repair Classification Packet

Generated: `{summary['generated_at']}`

Mode: local/read-only classification from the current Merchant issue export. No external write occurred.

## Source

- Current classified issue rows: `{ISSUE_ROWS}`
- Prior readback packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md`

## Summary

- Market/language: `US` / `es`
- Issue rows classified: `{len(rows)}`
- Unique issue items: `{len(item_rows)}`
- Paid-cohort issue items: `{len(blocked_paid_items)}`
- Paid-cohort attribute-repair candidates: `{len(attribute_paid_items)}`

## Repair Scope By Issue

| Issue | Rows | Unique items | Paid-cohort items | Action class |
|---|---:|---:|---:|---|
{issue_table}

## Paid-Cohort Priority Items

Top rows below are the first `{len(top_paid)}` paid-cohort items from the current issue export. Use the full CSV for exact row handling.

| Item ID | Issue rows | Issue titles |
|---|---:|---|
{paid_table}

## Decision

`US/es` is not Shopping-build-ready. The current issue export proves live blockers, but it is not safe repair authority because it lacks `source_id` and full active approved-product state.

Do not repair by stale May 8 files, sample-clear rows, or concept copy. The next safe step is a current full all-products/source export for source `10627981690`, with country, language, feed label, currency, product status, active/approved state, paid-cohort intersection, and source timestamp.

## Approval Packet For Future Repair

Use this only after the full source/all-products export confirms exact affected rows:

`I approve a no-spend Merchant US/es repair preflight for source 10627981690 limited to the exact current paid-cohort rows proven by the full export, covering only age_group, color, gender, size, page/image availability, and capacity decision analysis. Do not change campaign status, budget, bids, product groups, feed scope, source scope, conversion settings, billing, Shopify customer-visible copy, or Pinterest/Google Ads campaign objects. Save before/after readbacks and stop on any additional approval, account, policy, or destructive prompt.`

## Output Files

- `{issue_summary_path}`
- `{paid_items_path}`
- `{summary_path}`
"""
    report_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
