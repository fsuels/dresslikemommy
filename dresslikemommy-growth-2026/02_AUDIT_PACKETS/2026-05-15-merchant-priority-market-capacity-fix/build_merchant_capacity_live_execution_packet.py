#!/usr/bin/env python3.13
"""Build the exact live-execution approval packet for Merchant capacity cleanup.

This stays local/read-only. It joins the Merchant feed-group acceptance file and
the Shopify International region prune preview into the smallest action-time
packet a future authenticated operator needs before any Save/Apply/Sync.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
MERCHANT_GUARD_JSON = BASE / "merchant_capacity_execution_guard_summary.json"
SHOPIFY_REGION_JSON = BASE / "shopify_international_region_prune_summary.json"
MERCHANT_ACCEPTANCE_CSV = BASE / "merchant_capacity_platform_preview_acceptance.csv"
SHOPIFY_REGION_CSV = BASE / "shopify_international_region_prune_preview.csv"
SUMMARY_JSON = BASE / "merchant_capacity_live_execution_packet_summary.json"
CHECKLIST_CSV = BASE / "merchant_capacity_live_execution_checklist.csv"
PACKET_MD = BASE / "MERCHANT_CAPACITY_LIVE_EXECUTION_APPROVAL_PACKET.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def write_checklist(summary: dict) -> None:
    rows = [
        {
            "phase": "approval",
            "check": "exact approval phrase is present in current session",
            "required_result": "approval phrase matches packet wording before live cleanup starts",
        },
        {
            "phase": "pre_save",
            "check": "Merchant/feed-country preview reconciles to merchant_capacity_platform_preview_acceptance.csv",
            "required_result": "41 exact remove rows selected or disabled from Google/Merchant publishing scope only",
        },
        {
            "phase": "pre_save",
            "check": "Shopify Markets preview reconciles to shopify_international_region_prune_preview.csv",
            "required_result": "52 International regions selected; no whole-market removal; CA/AU duplicates and hold-review rows untouched",
        },
        {
            "phase": "pre_save",
            "check": "priority groups preserved",
            "required_result": "USA English 5491 rows and USA Spanish 5412 rows remain enabled/unselected for removal",
        },
        {
            "phase": "pre_save",
            "check": "future priority markets are not overclaimed",
            "required_result": "Canada English/French and GB English remain not Shopping-build-ready until fresh export rows exist",
        },
        {
            "phase": "post_save",
            "check": "fresh Merchant all-products export captured after cleanup",
            "required_result": "after-export guard passes with 0 first-pass removal rows remaining and protected USA counts not reduced",
        },
    ]
    with CHECKLIST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    merchant = load_json(MERCHANT_GUARD_JSON)
    shopify = load_json(SHOPIFY_REGION_JSON)

    candidate = merchant["candidate_summary"]
    source = merchant["source_export_summary"]
    summary = {
        "mode": "local_readonly_no_external_writes",
        "merchant_exact_preview_rows": count_csv_rows(MERCHANT_ACCEPTANCE_CSV),
        "merchant_remove_group_count": candidate["candidate_group_count"],
        "expected_first_pass_removal_rows": candidate["expected_remove_rows"],
        "expected_after_first_pass_floor": merchant["expected_after_first_pass_rows"],
        "protected_usa_english_rows": source["priority_counts"]["USA English"],
        "protected_usa_spanish_rows": source["priority_counts"]["USA Spanish"],
        "current_canada_english_rows": source["enable_after_cleanup_counts"]["Canada English"],
        "current_canada_french_rows": source["enable_after_cleanup_counts"]["Canada French"],
        "current_gb_english_rows": source["enable_after_cleanup_counts"]["GB English"],
        "shopify_international_regions": shopify["international_region_count"],
        "shopify_first_pass_remove_regions": shopify["first_pass_remove_region_count"],
        "shopify_hold_or_preserve_regions": shopify["action_counts"]["do_not_select_for_first_pass"],
        "approval_phrase": (
            "I approve the Merchant priority-market capacity cleanup execution: "
            "remove or disable from Google/Merchant publishing scope only the exact "
            "non-priority groups in merchant_capacity_platform_preview_acceptance.csv "
            "and, if Shopify Markets is the control surface, only the International "
            "regions marked remove in shopify_international_region_prune_preview.csv; "
            "preserve USA English, USA Spanish, Canada, United Kingdom, Eurozone, "
            "Australia, Europe-later groups, CA/AU duplicate hold rows, and all "
            "hold-review regions; do not delete products or change titles, prices, "
            "vendors, variants, feed labels, campaigns, product groups, bids, "
            "budgets, statuses, conversion settings, billing, or credentials; then "
            "capture a fresh Merchant all-products export and run the after-export guard."
        ),
        "hard_stops": [
            "no Save/Apply/Sync/Upload if the authenticated preview cannot reconcile to both CSVs",
            "no whole Shopify market removal",
            "no product deletion or Shopify product data mutation",
            "no Merchant capacity request, Shopping campaign, product-group, bid, budget, status, or conversion write",
            "no Canada/GB Shopping build until fresh after-cleanup export rows exist",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_checklist(summary)

    packet = f"""# Merchant Capacity Live Execution Approval Packet

Mode: local/read-only approval and readback packet. No Merchant, Shopify, Google
Ads, Pinterest, feed, product, product-group, bid, budget, status, capacity,
billing, credential, or conversion writes were made.

## Purpose

Move the current P0 Merchant capacity lane from scattered prep into one
action-time packet. This packet does not authorize live changes by itself; it
defines the exact approval phrase, before-save reconciliation, and after-export
readback required before Canada/French-Canada/GB Shopping can be considered.

## Exact Approval Phrase

`{summary['approval_phrase']}`

## Before-State From Current Evidence

- Current Merchant all-products rows: `{source['total_rows']}`.
- Merchant first-pass remove groups: `{candidate['candidate_group_count']}`.
- Expected first-pass row removal: `{candidate['expected_remove_rows']}`.
- Expected after-first-pass row floor: `{merchant['expected_after_first_pass_rows']}`.
- Protected USA English rows: `{source['priority_counts']['USA English']}`.
- Protected USA Spanish rows: `{source['priority_counts']['USA Spanish']}`.
- Current Canada English rows: `{source['enable_after_cleanup_counts']['Canada English']}`.
- Current Canada French rows: `{source['enable_after_cleanup_counts']['Canada French']}`.
- Current GB English rows: `{source['enable_after_cleanup_counts']['GB English']}`.
- Shopify `International` regions: `{shopify['international_region_count']}`.
- Shopify first-pass removal regions: `{shopify['first_pass_remove_region_count']}`.
- Shopify preserve/hold-review regions: `{shopify['action_counts']['do_not_select_for_first_pass']}`.

## Live Pre-Save Reconciliation

Before any Save, Apply, Sync, Upload, or equivalent platform action:

1. Reconcile the Merchant/feed-country preview to
   `merchant_capacity_platform_preview_acceptance.csv`.
2. If Shopify Markets is the control surface, reconcile the region preview to
   `shopify_international_region_prune_preview.csv`.
3. Confirm the selected live preview removes only the non-priority publishing
   scope, not products.
4. Confirm USA English and USA Spanish stay enabled and unselected for removal.
5. Confirm separate `Canada`, `United Kingdom`, `Eurozone`, and `Australia`
   markets are preserved; duplicate `CA` and `AU` rows inside `International`
   are not removed in this first pass.
6. Stop if the UI/API preview cannot match both CSVs.

## After-State Readback

After a live cleanup, capture a fresh Merchant all-products export and run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/build_merchant_capacity_execution_guard.py --after-export /path/to/fresh_export.csv
```

Pass criteria:

- `0` first-pass removal rows remain.
- USA English rows do not drop below `{source['priority_counts']['USA English']}`.
- USA Spanish rows do not drop below `{source['priority_counts']['USA Spanish']}`.
- Canada English/French and GB English are not called Shopping-build-ready until
  fresh export rows exist.

## Hard Stops

- No whole-market removal.
- No product deletion.
- No product title, price, variant, vendor, inventory, feed-label, campaign,
  product-group, bid, budget, status, conversion, billing, credential, or
  capacity-request mutation.
- No save if either CSV cannot be reconciled.
- No Canada/GB Shopping build until the after-export proof exists.

## Files

- `merchant_capacity_live_execution_checklist.csv`
- `merchant_capacity_live_execution_packet_summary.json`
- `merchant_capacity_platform_preview_acceptance.csv`
- `shopify_international_region_prune_preview.csv`
- `MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`
- `MERCHANT_SHOPIFY_MARKETS_REGION_PRUNE_PREVIEW.md`
"""
    PACKET_MD.write_text(packet, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
