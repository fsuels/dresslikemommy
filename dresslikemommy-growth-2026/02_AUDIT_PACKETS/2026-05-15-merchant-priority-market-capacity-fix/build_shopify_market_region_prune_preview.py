#!/usr/bin/env python3.13
"""Build a local/read-only Shopify Markets region prune preview.

This does not call Shopify or Merchant Center. It classifies the sanitized
Shopify Markets readback into a conservative operator checklist so the live
operator can avoid disabling priority markets while reducing non-priority
Merchant row multiplication.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
REGION_INPUT = BASE / "shopify_markets_regions_sanitized.csv"
PREVIEW_CSV = BASE / "shopify_international_region_prune_preview.csv"
SUMMARY_JSON = BASE / "shopify_international_region_prune_summary.json"
REPORT_MD = BASE / "MERCHANT_SHOPIFY_MARKETS_REGION_PRUNE_PREVIEW.md"

ASIA_MIDDLE_EAST = {
    "AE",
    "AM",
    "AZ",
    "BH",
    "BN",
    "BT",
    "GE",
    "HK",
    "ID",
    "IL",
    "IN",
    "IO",
    "JO",
    "JP",
    "KG",
    "KR",
    "KW",
    "KZ",
    "LB",
    "LK",
    "MN",
    "MO",
    "MV",
    "MY",
    "OM",
    "PH",
    "QA",
    "SA",
    "SG",
    "TH",
    "TR",
    "TW",
    "VN",
}

AFRICA = {
    "AC",
    "BW",
    "CI",
    "CV",
    "EG",
    "MA",
    "MU",
    "SC",
    "SH",
    "ST",
    "SZ",
    "TA",
    "TN",
    "ZA",
}

SOUTH_AMERICA = {"CL", "CO", "FK", "GS", "PE"}

PRIORITY_OR_SEPARATE_MARKET = {
    "AU": "separate Australia market; hold unless later capacity pass needs it",
    "CA": "separate Canada priority market; do not remove Canada coverage blindly",
}

HOLD_REVIEW = {
    "AI",
    "BL",
    "BM",
    "BS",
    "CK",
    "FJ",
    "GL",
    "KY",
    "MF",
    "MX",
    "NZ",
    "PM",
    "SV",
    "TC",
    "TV",
    "UM",
    "VG",
    "WF",
    "WS",
}


def classify_region(code: str) -> tuple[str, str, str]:
    if code in PRIORITY_OR_SEPARATE_MARKET:
        return (
            "PRESERVE_PRIORITY_OR_SEPARATE_MARKET",
            "do_not_select_for_first_pass",
            PRIORITY_OR_SEPARATE_MARKET[code],
        )
    if code in ASIA_MIDDLE_EAST:
        return (
            "REMOVE_ASIA_MIDDLE_EAST",
            "remove_from_international_only_if_platform_preview_preserves_priority_markets",
            "owner-directed non-priority geography for capacity cleanup",
        )
    if code in AFRICA:
        return (
            "REMOVE_AFRICA",
            "remove_from_international_only_if_platform_preview_preserves_priority_markets",
            "owner-directed non-priority geography for capacity cleanup",
        )
    if code in SOUTH_AMERICA:
        return (
            "REMOVE_SOUTH_AMERICA",
            "remove_from_international_only_if_platform_preview_preserves_priority_markets",
            "owner-directed non-priority geography for capacity cleanup",
        )
    if code in HOLD_REVIEW:
        return (
            "HOLD_REVIEW_NOT_FIRST_PASS",
            "do_not_select_for_first_pass",
            "not explicitly named by owner; review only after first pass if capacity remains blocked",
        )
    return (
        "UNKNOWN_HOLD_REVIEW",
        "do_not_select_for_first_pass",
        "unclassified by conservative local map; needs authenticated preview review",
    )


def load_rows() -> list[dict[str, str]]:
    with REGION_INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f"No rows found in {REGION_INPUT}")
    return rows


def main() -> None:
    rows = load_rows()
    active_markets = sorted({row["market_handle"] for row in rows if row["status"] == "ACTIVE"})
    required_markets = {"us", "canada", "united-kingdom", "eu", "international"}
    missing = sorted(required_markets - set(active_markets))
    if missing:
        raise SystemExit(f"Missing expected active market handles: {missing}")

    preview_rows: list[dict[str, str]] = []
    for row in rows:
        if row["market_handle"] != "international":
            continue
        code = row["region_code"].strip().upper()
        bucket, action, reason = classify_region(code)
        preview_rows.append(
            {
                "market_handle": row["market_handle"],
                "market_name": row["market_name"],
                "region_code": code,
                "bucket": bucket,
                "recommended_preview_action": action,
                "reason": reason,
            }
        )

    if not preview_rows:
        raise SystemExit("No International market regions found")

    preview_rows.sort(key=lambda r: (r["bucket"], r["region_code"]))
    bucket_counts = Counter(row["bucket"] for row in preview_rows)
    action_counts = Counter(row["recommended_preview_action"] for row in preview_rows)
    first_pass_remove_count = sum(
        1
        for row in preview_rows
        if row["recommended_preview_action"]
        == "remove_from_international_only_if_platform_preview_preserves_priority_markets"
    )

    with PREVIEW_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(preview_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(preview_rows)

    summary = {
        "mode": "local_readonly_no_external_writes",
        "source_regions_csv": str(REGION_INPUT.relative_to(Path.cwd())),
        "preview_csv": str(PREVIEW_CSV.relative_to(Path.cwd())),
        "international_region_count": len(preview_rows),
        "first_pass_remove_region_count": first_pass_remove_count,
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "action_counts": dict(sorted(action_counts.items())),
        "active_market_handles_seen": active_markets,
        "required_active_market_handles_present": sorted(required_markets),
        "hard_stop": [
            "do not remove whole International market blindly",
            "do not remove separate United States, Canada, United Kingdom, Eurozone, or Australia markets",
            "do not delete products",
            "do not save/apply/sync unless authenticated preview preserves priority markets",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = f"""# Merchant Shopify Markets Region Prune Preview

Mode: local/read-only preview from the sanitized Shopify Markets readback. No
Merchant, Shopify, Google Ads, Pinterest, feed, product, product-group, bid,
budget, status, capacity, billing, credential, or conversion writes were made.

## Purpose

The feed-group execution guard identifies the Merchant row groups to remove. This
region preview translates the likely Shopify Markets control surface into a
conservative first-pass checklist so the live operator does not disable a
priority market or remove products.

## Current Readback Shape

- Active market handles present: `{', '.join(active_markets)}`.
- International market regions: `{len(preview_rows)}`.
- First-pass high-confidence regions to remove from `International` only if the
  authenticated preview preserves priority markets: `{first_pass_remove_count}`.

## Region Buckets

| Bucket | Regions |
|---|---:|
"""
    for bucket, count in sorted(bucket_counts.items()):
        report += f"| `{bucket}` | `{count}` |\n"

    report += """
## Before-Save Rules

Use `shopify_international_region_prune_preview.csv` together with
`merchant_capacity_platform_preview_acceptance.csv` before any Save, Apply, Sync,
Upload, or equivalent live action:

1. Remove only regions classified as `REMOVE_ASIA_MIDDLE_EAST`, `REMOVE_AFRICA`,
   or `REMOVE_SOUTH_AMERICA` from the `International` publishing surface.
2. Do not remove the separate `United States`, `Canada`, `United Kingdom`,
   `Eurozone`, or `Australia` markets.
3. Do not remove `CA` or `AU` just because they appear inside `International`;
   treat duplicate coverage as a preview reconciliation issue, not a blind first
   pass.
4. Keep `HOLD_REVIEW_NOT_FIRST_PASS` and `UNKNOWN_HOLD_REVIEW` rows untouched in
   the first pass.
5. Do not delete Shopify products or change titles, variants, prices, inventory,
   vendors, product types, feed labels, campaigns, product groups, budgets, bids,
   statuses, or conversion settings.

Stop if the authenticated UI/API preview cannot show region-level changes that
preserve the priority market handles and reconcile to the Merchant feed-group
acceptance file.

## Files

- `shopify_international_region_prune_preview.csv`
- `shopify_international_region_prune_summary.json`
- `merchant_capacity_platform_preview_acceptance.csv`
"""
    REPORT_MD.write_text(report, encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
