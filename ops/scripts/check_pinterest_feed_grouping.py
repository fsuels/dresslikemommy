#!/usr/bin/env python3.13
"""
Pinterest feed grouping guardrail.

Purpose: prevent the variant-as-product duplication mistake from ever
silently returning across any market or any category.

Wired into: ops/scripts/check_continuity_integrity.py --strict

Behavior:

This script scans every relevant feed snapshot in the repo and verifies
that variants of the same parent product are grouped via item_group_id.
It fails CLOSED with a non-zero exit code if it detects per-variant
submission without item_group_id.

Feed snapshot inputs (auto-discovered):

1. Path-B generator output:
   dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_<market>.tsv
   -> Must have item_group_id on EVERY row.

2. Pinterest product-group import CSVs (the kind Pinterest's UI exports/imports):
   dresslikemommy-growth-2026/02_AUDIT_PACKETS/**/pinterest_*item_id_import*.csv
   -> Diagnostic only: warn if duplicates per parent exist without an
      accompanying item_group_id column.

3. Merchant Center all-products sanitized CSVs (Shopify -> Pinterest uses
   the same item-ID emission rules):
   dresslikemommy-growth-2026/02_AUDIT_PACKETS/**/merchant_all_products_*sanitized.csv
   -> If the same `shopify_<market>_<parent>` prefix appears across >= 2
      rows in the same (feed_label, language_code) bucket, the underlying
      feed is in per-variant mode. This is the recurring-mistake signal.

Exit codes:
  0  PASS  All inspected feed snapshots either have item_group_id on every
           row, or have no duplicate-parent patterns.
  1  FAIL  At least one snapshot shows per-variant submission without
           item_group_id.
  2  ERROR Input parsing problem (so the strict gate also fails closed).

Idempotent: re-run any time.

Note: this guardrail intentionally permits the older Merchant snapshot
located at 2026-05-15-merchant-post-shopify-region-prune-export/ to fail
ONLY in `--report-only` mode; in `--strict` mode it must be remediated.
The Pinterest -> Shopify channel fix collapses that snapshot's variant
ratio at the next re-sync, at which point the check passes naturally.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from glob import glob
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

PATH_B_GLOB = str(
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
      "2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_*.tsv"
)
PIN_IMPORT_GLOB = str(
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/**/pinterest_*item_id_import*.csv"
)
MERCHANT_GLOB = str(
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/**/merchant_all_products_*sanitized.csv"
)

SHOPIFY_VARIANT_ITEM_ID_RE = re.compile(r"^shopify_(\w+)_(\d+)_(\d+)$")

RESULTS_HEADER = "# Pinterest Feed Grouping Guardrail\n"


def scan_path_b_feed(path: Path) -> dict:
    """Path-B generator output must have item_group_id on every row."""
    info = {
        "kind": "path_b_generated_feed",
        "path": str(path.relative_to(REPO_ROOT)),
        "rows": 0,
        "rows_missing_item_group_id": 0,
        "unique_item_group_ids": 0,
        "verdict": "PASS",
        "reason": "",
    }
    item_groups: set[str] = set()
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        if "item_group_id" not in (r.fieldnames or []):
            info["verdict"] = "FAIL"
            info["reason"] = "TSV missing item_group_id column entirely"
            return info
        for row in r:
            info["rows"] += 1
            igid = (row.get("item_group_id") or "").strip()
            if not igid:
                info["rows_missing_item_group_id"] += 1
            else:
                item_groups.add(igid)
    info["unique_item_group_ids"] = len(item_groups)
    if info["rows"] == 0:
        # Allow empty (dry-run) snapshots.
        info["reason"] = "empty (dry-run) snapshot"
    elif info["rows_missing_item_group_id"]:
        info["verdict"] = "FAIL"
        info["reason"] = (
            f"{info['rows_missing_item_group_id']} of {info['rows']} rows missing item_group_id"
        )
    return info


def scan_pinterest_import_csv(path: Path) -> dict:
    """Pinterest product-group import CSV: warn if duplicates per parent exist
    without an item_group_id column."""
    info = {
        "kind": "pinterest_product_group_import",
        "path": str(path.relative_to(REPO_ROOT)),
        "rows": 0,
        "duplicate_parent_clusters": 0,
        "max_variants_per_parent": 0,
        "verdict": "PASS",
        "reason": "",
    }
    parents = Counter()
    has_item_group_col = False
    with open(path, newline="", encoding="utf-8") as f:
        # These CSVs are large free-text payloads (Pinterest filter export);
        # be forgiving about parsing and just scan text for variant item IDs.
        text = f.read()
    has_item_group_col = "item_group_id" in text.lower()
    matches = re.findall(r"shopify_\w+_(\d+)_(\d+)", text)
    info["rows"] = len(matches)
    for pid, _ in matches:
        parents[pid] += 1
    if parents:
        info["max_variants_per_parent"] = max(parents.values())
        info["duplicate_parent_clusters"] = sum(1 for c in parents.values() if c > 1)
    if info["duplicate_parent_clusters"] and not has_item_group_col:
        # This is the diagnostic signal that the feed upstream is in per-variant
        # mode. We DO NOT mark this PASS because the underlying feed needs the fix.
        info["verdict"] = "FAIL"
        info["reason"] = (
            f"{info['duplicate_parent_clusters']} parents have multiple variant rows "
            f"and the CSV exposes no item_group_id column; upstream feed is per-variant"
        )
    return info


def scan_merchant_export(path: Path) -> dict:
    info = {
        "kind": "merchant_all_products_export",
        "path": str(path.relative_to(REPO_ROOT)),
        "rows": 0,
        "buckets_with_duplicate_parents": 0,
        "worst_bucket_variants_per_parent": 0,
        "verdict": "PASS",
        "reason": "",
    }
    per_bucket_parents: dict[tuple[str, str, str], Counter] = defaultdict(Counter)
    try:
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            r = csv.DictReader(f)
            for row in r:
                info["rows"] += 1
                iid = (row.get("merchant_center_item_id") or "").strip()
                m = SHOPIFY_VARIANT_ITEM_ID_RE.match(iid)
                if not m:
                    continue
                market, pid, _vid = m.group(1), m.group(2), m.group(3)
                fl = row.get("feed_label") or ""
                lc = row.get("language_code") or ""
                per_bucket_parents[(market, fl, lc)][pid] += 1
    except Exception as exc:  # pragma: no cover
        info["verdict"] = "ERROR"
        info["reason"] = f"parse failure: {exc}"
        return info
    bad_buckets = 0
    worst = 0
    for _bucket, parents in per_bucket_parents.items():
        if parents:
            mx = max(parents.values())
            if mx > 1:
                bad_buckets += 1
                worst = max(worst, mx)
    info["buckets_with_duplicate_parents"] = bad_buckets
    info["worst_bucket_variants_per_parent"] = worst
    if bad_buckets:
        info["verdict"] = "FAIL"
        info["reason"] = (
            f"{bad_buckets} market x language buckets have multiple variant rows per "
            f"parent (worst: {worst}x). Underlying feed is per-variant; apply the "
            f"Pinterest sales-channel grouping fix or upload Path-B feed."
        )
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Fail non-zero on any FAIL across any feed snapshot.",
    )
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="Print findings and return 0 even on FAIL (use during fix-in-progress windows).",
    )
    ap.add_argument(
        "--market",
        default=None,
        help="Restrict scan to a single market handle (for per-market readbacks).",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON only; suppress markdown report.",
    )
    args = ap.parse_args()

    results: list[dict] = []

    for p in sorted(glob(PATH_B_GLOB, recursive=True)):
        path = Path(p)
        if args.market and f"pinterest_{args.market}." not in path.name:
            continue
        results.append(scan_path_b_feed(path))

    for p in sorted(glob(PIN_IMPORT_GLOB, recursive=True)):
        results.append(scan_pinterest_import_csv(Path(p)))

    for p in sorted(glob(MERCHANT_GLOB, recursive=True)):
        results.append(scan_merchant_export(Path(p)))

    fails = [r for r in results if r["verdict"] == "FAIL"]
    errors = [r for r in results if r["verdict"] == "ERROR"]

    if args.json:
        print(json.dumps({"results": results, "fails": len(fails), "errors": len(errors)}, indent=2))
    else:
        print(RESULTS_HEADER)
        for r in results:
            line = f"- {r['verdict']:<5} {r['kind']:<35} {r['path']}"
            if r.get("reason"):
                line += f"  -> {r['reason']}"
            print(line)
        print()
        print(f"summary: {len(results)} snapshots scanned, {len(fails)} FAIL, {len(errors)} ERROR")

    if errors:
        return 2
    if fails and args.strict and not args.report_only:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
