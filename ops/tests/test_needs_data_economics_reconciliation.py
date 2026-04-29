#!/usr/bin/env python3
"""Regression checks for remaining economics-gap reconciliation."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.reconcile_needs_data_economics import build_gap_rows  # noqa: E402


def main() -> None:
    rows = build_gap_rows(
        shipping_rows=[
            {
                "shipping_charged": "12.99",
                "refund_shipping": "0.00",
            }
        ],
        payout_summary={"rows": 1},
        balance_summary={
            "rows": 2,
            "type_counts": {"CHARGE": 1, "TRANSFER": 1},
            "totals": {"fee": "2.10"},
        },
        dispute_rows=[],
        ad_rows=[
            {
                "platform": "Pinterest Ads",
                "status": "COLLECTED_ZERO_SPEND_365D",
                "spend": "0.00",
                "evidence": "pinterest.txt",
            },
            {
                "platform": "Google Ads",
                "status": "PARTIAL_VISIBLE_ZERO_SPEND",
                "spend": "0.00",
                "evidence": "google.md",
            },
            {
                "platform": "GA4",
                "status": "PARTIAL_ANALYTICS_IMPORTED",
                "conversions": "4 purchases visible",
                "evidence": "ga4.md",
            },
            {
                "platform": "Meta Ads",
                "status": "NEEDS_EXPORT",
                "evidence": "",
            },
        ],
        order_rows=[
            {
                "included_in_model": "TRUE",
                "payment_gateways": "shopify_payments",
            }
        ],
        order_line_rows=[
            {
                "included_in_model": "TRUE",
                "observed_payment_fee_allocated": "2.10",
            }
        ],
    )
    by_gap = {row["gap"]: row for row in rows}
    assert by_gap["Shipping label/carrier cost"]["new_status"] == "NEEDS_CARRIER_EXPORT"
    assert "ShopifyPayments shipping-label balance tx count 0" in by_gap["Shipping label/carrier cost"]["value"]
    assert by_gap["Payout/payment fees/adjustments"]["new_status"] == "COLLECTED_SHOPIFY_PAYMENTS_API"
    assert by_gap["Payout/payment fees/adjustments"]["remaining_blocker"] == ""
    assert by_gap["Pinterest ad spend"]["new_status"] == "COLLECTED_ZERO_SPEND_365D"
    assert by_gap["Google Ads ad spend"]["remaining_blocker"].startswith("Full 30/90/365")
    print("ok")


if __name__ == "__main__":
    main()
