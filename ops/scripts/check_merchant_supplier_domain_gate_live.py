#!/usr/bin/env python3
"""Read the live Merchant Center supplier-domain safety gate.

This uses the logged-in Merchant Center browser RPC session on the local Chrome
DevTools port. It is read-only and writes sanitized evidence: no cookies,
request headers, or credentials are saved.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.check_merchant_center_clean_labels_live import (
    CdpClient,
    capture_product_list_request,
    execute_query,
    find_items_page,
    google_cookies,
)


DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-01-standard-shopping-reactivation-readback/"
    "merchant-supplier-domain-gate-live"
)
DEFAULT_QUERIES = "1688.com,detail.1688.com,alibaba.com,aliexpress.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--queries", default=DEFAULT_QUERIES)
    parser.add_argument("--output-name", default="merchant_supplier_domain_gate_live.json")
    return parser.parse_args()


def product_id_from_offer_id(offer_id: str) -> str:
    parts = offer_id.split("_")
    if len(parts) >= 4 and parts[0] == "shopify":
        return parts[2]
    return ""


def main() -> int:
    args = parse_args()
    queries = [item.strip() for item in args.queries.split(",") if item.strip()]

    page = find_items_page(args.cdp_port)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        cookies = google_cookies(client)
        request_template = capture_product_list_request(client)
    finally:
        client.close()

    session = requests.Session()
    session.cookies.update(cookies)
    query_results = [execute_query(session, request_template, query) for query in queries]
    row_counts = {result["query"]: result["row_count"] for result in query_results}
    products_by_query = {
        result["query"]: sorted(
            {
                product_id
                for row in result["rows"]
                if (product_id := product_id_from_offer_id(row["merchant_center_item_id"]))
            }
        )
        for result in query_results
    }
    gate_passed = all(count == 0 for count in row_counts.values())

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_LIVE_MERCHANT_CENTER_SUPPLIER_DOMAIN_GATE",
        "source_page_title": page.get("title"),
        "source_page_url": page.get("url"),
        "row_counts": row_counts,
        "products_by_query": products_by_query,
        "supplier_domain_gate_status": (
            "PASS_ZERO_SUPPLIER_DOMAIN_ROWS"
            if gate_passed
            else "BLOCKED_SUPPLIER_DOMAIN_ROWS_STILL_VISIBLE"
        ),
        "query_results": query_results,
        "notes": [
            "Read-only browser RPC check; no Merchant Center or Google Ads changes were made.",
            "Cookies and request headers were used only in memory and are not written to disk.",
            "Standard Shopping may not move to approval review until all supplier-domain row counts are 0.",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / args.output_name
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(out_path),
                "supplier_domain_gate_status": report["supplier_domain_gate_status"],
                "row_counts": row_counts,
                "products_by_query": products_by_query,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if gate_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
