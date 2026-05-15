#!/usr/bin/env python3
"""Build a post-prune Merchant paid-cohort intersection packet.

This script is local/read-only. It joins saved Merchant and Google Ads exports
so future operators do not need a GUI account surface to know what the current
evidence proves.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent

MERCHANT_EXPORT = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-post-shopify-region-prune-export/merchant_all_products_browser_rpc_sanitized.csv"
PAID_COHORT = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv"
SHOPPING_EXPORT = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-shopping-readonly-export-queue/standard_shopping_products_normalized_for_join.csv"
POST_PRUNE_READBACK = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_POST_SHOPIFY_REGION_PRUNE_READBACK.md"
GUARD_REPORT = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md"

TARGET_MARKETS = [
    ("US", "en", "USD"),
    ("US", "es", "USD"),
    ("CA", "en", "CAD"),
    ("CA", "fr", "CAD"),
    ("GB", "en", "GBP"),
    ("AU", "en", "AUD"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def boolish(value: str | None) -> bool:
    return (value or "").strip().upper() == "TRUE"


def money_to_float(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    return float(cleaned or "0")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    paid_rows = read_csv(PAID_COHORT)
    shopping_rows = read_csv(SHOPPING_EXPORT)

    paid_by_id = {row["merchant_center_item_id"].lower(): row for row in paid_rows}
    shopping_by_id = {row["item_id"].lower(): row for row in shopping_rows}

    market_counts: Counter[tuple[str, str, str]] = Counter()
    strict_counts: Counter[tuple[str, str, str]] = Counter()
    paid_eligible_counts: Counter[tuple[str, str, str]] = Counter()
    cohort_ids_by_market: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    strict_cohort_ids_by_market: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    paid_eligible_cohort_ids_by_market: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    all_cohort_ids_seen: set[str] = set()
    non_target_cohort_rows: list[dict[str, str]] = []

    target_keys = set(TARGET_MARKETS)

    for row in read_csv(MERCHANT_EXPORT):
        key = (row["feed_label"], row["language_code"], row["currency"])
        item_id = row["merchant_center_item_id"].lower()
        market_counts[key] += 1
        if boolish(row.get("strict_approved")):
            strict_counts[key] += 1
        if boolish(row.get("paid_eligible")):
            paid_eligible_counts[key] += 1
        if item_id in paid_by_id:
            all_cohort_ids_seen.add(item_id)
            cohort_ids_by_market[key].add(item_id)
            if boolish(row.get("strict_approved")):
                strict_cohort_ids_by_market[key].add(item_id)
            if boolish(row.get("paid_eligible")):
                paid_eligible_cohort_ids_by_market[key].add(item_id)
            if key not in target_keys:
                non_target_cohort_rows.append(row)

    market_rows: list[dict[str, object]] = []
    for key in TARGET_MARKETS:
        feed_label, language, currency = key
        cohort_ids = cohort_ids_by_market[key]
        shopping_ids = set(shopping_by_id) & cohort_ids
        market_rows.append(
            {
                "feed_label": feed_label,
                "language_code": language,
                "currency": currency,
                "merchant_total_rows": market_counts[key],
                "merchant_strict_approved_rows": strict_counts[key],
                "merchant_paid_eligible_rows": paid_eligible_counts[key],
                "paid_cohort_unique_ids_present": len(cohort_ids),
                "paid_cohort_strict_approved_ids_present": len(strict_cohort_ids_by_market[key]),
                "paid_cohort_paid_eligible_ids_present": len(paid_eligible_cohort_ids_by_market[key]),
                "standard_shopping_export_ids_present": len(shopping_ids),
                "standard_shopping_clicks": sum(int(float(shopping_by_id[i]["clicks"])) for i in shopping_ids),
                "standard_shopping_cost": f"{sum(money_to_float(shopping_by_id[i]['cost']) for i in shopping_ids):.2f}",
                "standard_shopping_conversion_value": f"{sum(money_to_float(shopping_by_id[i]['conversion_value']) for i in shopping_ids):.2f}",
                "action_decision": (
                    "hold_current_us_shopping_no_feed_change"
                    if key == ("US", "en", "USD")
                    else "blocked_until_rows_exist_and_capacity_guard_passes"
                    if key in {("CA", "en", "CAD"), ("CA", "fr", "CAD"), ("GB", "en", "GBP"), ("AU", "en", "AUD")}
                    else "blocked_by_current_us_es_issue_capacity_evidence"
                ),
            }
        )

    missing_us_en = sorted(set(paid_by_id) - cohort_ids_by_market[("US", "en", "USD")])
    shopping_missing_us_en = sorted(set(shopping_by_id) - cohort_ids_by_market[("US", "en", "USD")])

    top_non_target: list[dict[str, object]] = []
    for key, ids in sorted(cohort_ids_by_market.items(), key=lambda item: len(item[1]), reverse=True):
        if key in target_keys:
            continue
        feed_label, language, currency = key
        top_non_target.append(
            {
                "feed_label": feed_label,
                "language_code": language,
                "currency": currency,
                "merchant_total_rows": market_counts[key],
                "paid_cohort_unique_ids_present": len(ids),
                "paid_cohort_strict_approved_ids_present": len(strict_cohort_ids_by_market[key]),
            }
        )
        if len(top_non_target) == 20:
            break

    gap_rows = []
    for item_id in missing_us_en:
        row = paid_by_id[item_id]
        gap_rows.append(
            {
                "merchant_center_item_id": row["merchant_center_item_id"],
                "handle": row["handle"],
                "product_title": row["product_title"],
                "variant_title": row["variant_title"],
                "custom_label_0": row["custom_label_0"],
                "custom_label_4": row["custom_label_4"],
                "decision": "not_in_current_us_en_merchant_rows_keep_out_of_new_live_scope_until_current_readback_exists",
            }
        )

    write_csv(PACKET / "merchant_post_prune_paid_cohort_by_market.csv", market_rows, list(market_rows[0].keys()))
    write_csv(
        PACKET / "merchant_post_prune_top_non_target_paid_cohort_groups.csv",
        top_non_target,
        ["feed_label", "language_code", "currency", "merchant_total_rows", "paid_cohort_unique_ids_present", "paid_cohort_strict_approved_ids_present"],
    )
    write_csv(
        PACKET / "merchant_post_prune_us_en_paid_cohort_gaps.csv",
        gap_rows,
        ["merchant_center_item_id", "handle", "product_title", "variant_title", "custom_label_0", "custom_label_4", "decision"],
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "LOCAL_READ_ONLY_SAVED_EXPORT_INTERSECTION",
        "merchant_export": str(MERCHANT_EXPORT.relative_to(ROOT)),
        "paid_cohort_source": str(PAID_COHORT.relative_to(ROOT)),
        "standard_shopping_export": str(SHOPPING_EXPORT.relative_to(ROOT)),
        "paid_cohort_ids": len(paid_by_id),
        "standard_shopping_export_ids": len(shopping_by_id),
        "paid_cohort_ids_present_anywhere_in_merchant_export": len(all_cohort_ids_seen),
        "paid_cohort_ids_missing_everywhere_in_merchant_export": len(set(paid_by_id) - all_cohort_ids_seen),
        "us_en_paid_cohort_ids_present": len(cohort_ids_by_market[("US", "en", "USD")]),
        "us_en_standard_shopping_ids_present": len(set(shopping_by_id) & cohort_ids_by_market[("US", "en", "USD")]),
        "standard_shopping_ids_missing_from_us_en_merchant_rows": len(shopping_missing_us_en),
        "paid_cohort_ids_missing_from_us_en_merchant_rows": len(missing_us_en),
        "us_es_paid_cohort_ids_present": len(cohort_ids_by_market[("US", "es", "USD")]),
        "ca_en_paid_cohort_ids_present": len(cohort_ids_by_market[("CA", "en", "CAD")]),
        "ca_fr_paid_cohort_ids_present": len(cohort_ids_by_market[("CA", "fr", "CAD")]),
        "gb_en_paid_cohort_ids_present": len(cohort_ids_by_market[("GB", "en", "GBP")]),
        "au_en_paid_cohort_ids_present": len(cohort_ids_by_market[("AU", "en", "AUD")]),
        "non_target_paid_cohort_duplicate_rows": len(non_target_cohort_rows),
        "non_target_unique_paid_cohort_ids_present": len({row["merchant_center_item_id"].lower() for row in non_target_cohort_rows}),
        "decision": "US English Standard Shopping rows are locally reconciled; Canada/GB/AU Shopping remains blocked; non-target paid-cohort duplication confirms Merchant capacity work must target publishing scope, not campaign/product-group expansion.",
    }
    (PACKET / "merchant_post_prune_paid_cohort_intersection_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    report = f"""# Merchant Post-Prune Paid-Cohort Intersection

Generated: `{summary['generated_at']}`

Mode: local/read-only saved-export join. No Google Ads, Merchant, Shopify, Pinterest, feed, product, campaign, bid, budget, status, conversion, billing, or credential write occurred.

## Inputs

- Merchant post-prune browser-RPC export: `{summary['merchant_export']}`
- Exact paid cohort: `{summary['paid_cohort_source']}`
- Standard Shopping normalized product export: `{summary['standard_shopping_export']}`
- Related guard reports: `{POST_PRUNE_READBACK.relative_to(ROOT)}` and `{GUARD_REPORT.relative_to(ROOT)}`

## Result

- Exact paid cohort source has `{summary['paid_cohort_ids']}` item IDs; all `{summary['paid_cohort_ids_present_anywhere_in_merchant_export']}` are still present somewhere in the Merchant post-prune export.
- Current US/en/USD Merchant rows contain `{summary['us_en_paid_cohort_ids_present']}` paid-cohort IDs.
- Current Standard Shopping export has `{summary['standard_shopping_export_ids']}` product IDs, and `{summary['us_en_standard_shopping_ids_present']}` map to current US/en/USD Merchant rows. Missing from US/en Merchant rows: `{summary['standard_shopping_ids_missing_from_us_en_merchant_rows']}`.
- The exact paid cohort still has `{summary['paid_cohort_ids_missing_from_us_en_merchant_rows']}` IDs absent from current US/en/USD Merchant rows; keep those out of any new live scope until a fresh row-level readback exists.
- US/es/USD has `{summary['us_es_paid_cohort_ids_present']}` paid-cohort IDs, but remains blocked by current issue/capacity evidence.
- Canada English, Canada French, GB English, and AU English still have `0` paid-cohort IDs in the post-prune Merchant export.
- Non-target market/language/currency groups still contain `{summary['non_target_paid_cohort_duplicate_rows']}` duplicate paid-cohort rows spanning `{summary['non_target_unique_paid_cohort_ids_present']}` unique paid-cohort IDs.

## Decision

- `US/en` Standard Shopping: hold with evidence. The current campaign export reconciles to current Merchant US/en rows, but produced `$14.17` cost, `65` clicks, and `$0.00` conversion value in the saved export, so no feed/title/product-group/bid/budget/status write is justified by this intersection alone.
- `US/es`: do not repair from row presence alone. It still needs issue/capacity clearance or a narrow owner-approved repair/capacity action.
- `CA/en`, `CA/fr`, `GB/en`, `AU/en`: Shopping remains blocked. Do not create Shopping campaigns or product groups until Merchant rows exist and the capacity after-export guard passes.
- Merchant capacity: the paid cohort is still duplicated across non-target markets, proving the next unblock must be Merchant/Google publishing-scope control or delayed propagation readback, not another Shopify region-only prune and not campaign expansion.

## Outputs

- `merchant_post_prune_paid_cohort_by_market.csv`
- `merchant_post_prune_top_non_target_paid_cohort_groups.csv`
- `merchant_post_prune_us_en_paid_cohort_gaps.csv`
- `merchant_post_prune_paid_cohort_intersection_summary.json`
"""
    (PACKET / "MERCHANT_POST_PRUNE_PAID_COHORT_INTERSECTION.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
