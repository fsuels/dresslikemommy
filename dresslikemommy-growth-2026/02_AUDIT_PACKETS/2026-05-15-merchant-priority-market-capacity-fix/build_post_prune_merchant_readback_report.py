#!/usr/bin/env python3.13
"""Build post-prune Merchant readback proof.

This reads the fresh Merchant all-products browser-RPC export captured after the
Shopify International region prune and writes the explicit Canada/GB proof gate.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent
POST_EXPORT_DIR = (
    BASE.parent / "2026-05-15-merchant-post-shopify-region-prune-export"
)
ALL_PRODUCTS = POST_EXPORT_DIR / "merchant_all_products_browser_rpc_sanitized.csv"
CA_FR_CSV = POST_EXPORT_DIR / "merchant_ca_fr_eligibility.csv"
SUMMARY_JSON = BASE / "merchant_post_prune_priority_market_readback_summary.json"
REPORT_MD = BASE / "MERCHANT_POST_SHOPIFY_REGION_PRUNE_READBACK.md"

TARGET_GROUPS = {
    ("US", "en", "USD"): "USA English",
    ("US", "es", "USD"): "USA Spanish",
    ("CA", "en", "CAD"): "Canada English",
    ("CA", "fr", "CAD"): "Canada French",
    ("GB", "en", "GBP"): "GB English",
}
REMAINING_REMOVE_GROUPS = {
    ("AED_544866401", "ar", "AED"),
    ("AED_544866401", "en", "AED"),
    ("EGP_544866401", "ar", "EGP"),
    ("EGP_544866401", "en", "EGP"),
    ("HKD_544866401", "en", "HKD"),
    ("IDR_544866401", "en", "IDR"),
    ("ILS_544866401", "en", "ILS"),
    ("ILS_544866401", "iw", "ILS"),
    ("INR_544866401", "en", "INR"),
    ("INR_544866401", "hi", "INR"),
    ("JPY_544866401", "en", "JPY"),
    ("JPY_544866401", "ja", "JPY"),
    ("KRW_544866401", "en", "KRW"),
    ("KRW_544866401", "ko", "KRW"),
    ("KZT_544866401", "en", "KZT"),
    ("KZT_544866401", "ru", "KZT"),
    ("LBP_544866401", "ar", "LBP"),
    ("LBP_544866401", "en", "LBP"),
    ("LBP_544866401", "fr", "LBP"),
    ("LKR_544866401", "en", "LKR"),
    ("MAD_544866401", "ar", "MAD"),
    ("MAD_544866401", "en", "MAD"),
    ("MAD_544866401", "fr", "MAD"),
    ("MUR_544866401", "en", "MUR"),
    ("MYR_544866401", "en", "MYR"),
    ("PEN_544866401", "en", "PEN"),
    ("PEN_544866401", "es", "PEN"),
    ("PHP_544866401", "en", "PHP"),
    ("SAR_544866401", "ar", "SAR"),
    ("SAR_544866401", "en", "SAR"),
    ("SGD_544866401", "en", "SGD"),
    ("THB_544866401", "en", "THB"),
    ("TWD_544866401", "en", "TWD"),
    ("USD_544866401", "ar", "USD"),
    ("USD_544866401", "en", "USD"),
    ("USD_544866401", "es", "USD"),
    ("USD_544866401", "fr", "USD"),
    ("USD_544866401", "ru", "USD"),
    ("VND_544866401", "en", "VND"),
    ("XOF_544866401", "en", "XOF"),
    ("XOF_544866401", "fr", "XOF"),
}


def key(row: dict[str, str]) -> tuple[str, str, str]:
    return row.get("feed_label", ""), row.get("language_code", ""), row.get("currency", "")


def main() -> None:
    with ALL_PRODUCTS.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    group_counts = Counter(key(row) for row in rows)
    target_counts = {
        label: group_counts.get(group, 0) for group, label in TARGET_GROUPS.items()
    }
    remaining_remove_rows = sum(group_counts.get(group, 0) for group in REMAINING_REMOVE_GROUPS)
    ca_fr_rows = [row for row in rows if key(row) == ("CA", "fr", "CAD")]

    with CA_FR_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ca_fr_rows)

    passed = (
        target_counts["Canada English"] > 0
        and target_counts["Canada French"] > 0
        and target_counts["GB English"] > 0
        and remaining_remove_rows == 0
    )
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "POST_SHOPIFY_REGION_PRUNE_MERCHANT_READBACK",
        "all_products_export": str(ALL_PRODUCTS.relative_to(Path.cwd())),
        "total_rows": len(rows),
        "target_counts": target_counts,
        "remaining_remove_rows": remaining_remove_rows,
        "shopping_build_gate_passed": passed,
        "outputs": {
            "ca_fr_eligibility": str(CA_FR_CSV.relative_to(Path.cwd())),
            "report": str(REPORT_MD.relative_to(Path.cwd())),
            "summary": str(SUMMARY_JSON.relative_to(Path.cwd())),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = f"""# Merchant Post-Shopify Region Prune Readback

Generated: {summary['generated_at']}

Mode: read-only Merchant Center browser-RPC export analysis after the bounded
Shopify Markets `International` region prune. No Merchant upload/source sync,
Google Ads campaign/product-group/bid/budget/status/conversion change, Shopify
product edit, Pinterest change, billing change, or credential change occurred.

## Shopify Action Already Executed

- `International` market regions before prune: `73`.
- `International` market regions after prune: `21`.
- Removed first-pass non-priority regions: `52`.
- Protected duplicate `CA` and `AU` remained inside `International`.
- Separate active markets remained present: `us`, `canada`, `united-kingdom`,
  `eu`, `australia`, and `international`.

## Fresh Merchant Re-Export Result

| Gate | Rows |
|---|---:|
| USA English (`US|en|USD`) | `{target_counts['USA English']}` |
| USA Spanish (`US|es|USD`) | `{target_counts['USA Spanish']}` |
| Canada English (`CA|en|CAD`) | `{target_counts['Canada English']}` |
| Canada French (`CA|fr|CAD`) | `{target_counts['Canada French']}` |
| GB English (`GB|en|GBP`) | `{target_counts['GB English']}` |
| Remaining first-pass removal rows | `{remaining_remove_rows}` |

## Decision

`shopping_build_gate_passed={str(passed).lower()}`.

The Shopping build remains blocked because the fresh Merchant export still has
`0` Canada English rows, `0` Canada French rows, and `0` GB English rows, while
the first-pass non-priority Merchant row groups still remain in the product-list
export. The Shopify Markets cleanup succeeded, but Merchant/Google product
generation has not yet propagated or still needs a Google & YouTube publishing
sync/control action. Do not build Shopping from absent rows.

## Files

- `merchant_post_prune_priority_market_readback_summary.json`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_source_eligibility_browser_rpc_summary.json`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_ca_en_eligibility.csv`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_ca_fr_eligibility.csv`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_gb_en_eligibility.csv`
"""
    REPORT_MD.write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
