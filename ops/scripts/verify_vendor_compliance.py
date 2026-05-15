#!/usr/bin/env python3.13
"""Read-only verification that every active product on the Dress Like Mommy
Shopify store has vendor == 'Dress Like Mommy'.

No mutations. Safe to run anytime. Prints a compact summary and writes a
report to dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-vendor-brand-auto-fix-execution/.
"""

from __future__ import annotations

import json
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

import apply_vendor_backfill as backfill  # local import for shared helpers

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026"
    / "02_AUDIT_PACKETS"
    / "2026-05-15-vendor-brand-auto-fix-execution"
)

COUNT_QUERY = """
query VendorCount($after: String) {
  products(first: 50, after: $after, query: "status:active AND NOT vendor:\\"Dress Like Mommy\\"") {
    pageInfo { hasNextPage endCursor }
    edges { node { id vendor } }
  }
}
""".strip()

TOTAL_ACTIVE = """
query TotalActive {
  productsCount(query: "status:active") { count }
}
""".strip()


def main() -> None:
    domain, token, version = backfill.load_credentials()
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    # Count non-compliant
    non_compliant: list[dict] = []
    after = None
    while True:
        data = backfill.graphql(domain, token, version, COUNT_QUERY, {"after": after})["data"][
            "products"
        ]
        for edge in data["edges"]:
            non_compliant.append(edge["node"])
        if not data["pageInfo"]["hasNextPage"]:
            break
        after = data["pageInfo"]["endCursor"]

    total = backfill.graphql(domain, token, version, TOTAL_ACTIVE, {})["data"]["productsCount"][
        "count"
    ]

    report = {
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "active_products_total": total,
        "non_compliant_count": len(non_compliant),
        "non_compliant_sample": non_compliant[:20],
        "verdict": "PASS" if not non_compliant else "FAIL",
    }
    out = EVIDENCE_DIR / "vendor_compliance_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if non_compliant:
        sys.exit(1)


if __name__ == "__main__":
    main()
