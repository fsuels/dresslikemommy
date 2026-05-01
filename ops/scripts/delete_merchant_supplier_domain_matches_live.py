#!/usr/bin/env python3
"""Delete stale Merchant Center offers that still match supplier domains.

This uses the logged-in Merchant Center browser RPC session because the local
gcloud OAuth token does not have Content API write scopes. The script is guarded
for this incident: it only deletes rows whose Shopify product ID is in the
provided allowlist and whose offer ID is absent from the paid cohort CSV.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.check_merchant_center_clean_labels_live import (  # noqa: E402
    CdpClient,
    capture_product_list_request,
    find_items_page,
    google_cookies,
    normalize_row,
    safe_headers,
)


DEFAULT_PAID_COHORT = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--allowed-product-ids", required=True)
    parser.add_argument("--paid-cohort", type=Path, default=DEFAULT_PAID_COHORT)
    parser.add_argument("--queries", default="1688.com,detail.1688.com")
    parser.add_argument("--max-rows-per-query", type=int, default=300)
    parser.add_argument("--batches", type=int, default=1)
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--sleep", type=float, default=0.02)
    parser.add_argument("--chunk-size", type=int, default=1)
    parser.add_argument(
        "--allow-paid-cohort",
        action="store_true",
        help="Allow deleting offers present in the paid cohort CSV. Use only after a separate safety unpublish/removal decision.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def set_query_and_offset(post_data: str, query: str, offset: int, size: int = 50) -> str:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    ar_payload = json.loads(parsed["__ar"][0])
    options = ar_payload.setdefault("2", {}).setdefault("5", [])
    for option in options:
        if option.get("1") == "search_query":
            option["2"] = query
            break
    else:
        options.append({"1": "search_query", "2": query})
    ar_payload.setdefault("2", {})["4"] = {"1": offset, "2": size}
    parsed["__ar"] = [json.dumps(ar_payload, separators=(",", ":"))]
    return urllib.parse.urlencode({key: values[0] for key, values in parsed.items()})


def rpc(
    session: requests.Session,
    request_template: dict[str, Any],
    f_sid: str,
    service: str,
    method: str,
    ar_payload: dict[str, Any],
) -> requests.Response:
    url = (
        f"https://merchants.google.com/mc_products/_/rpc/{service}/{method}"
        f"?authuser=0&rpcTrackingId={service}.{method}%3Amanual"
        f"&f.sid={urllib.parse.quote(f_sid)}"
    )
    body = urllib.parse.urlencode(
        {
            "a": "124884876",
            "f.sid": f_sid,
            "__ar": json.dumps(ar_payload, separators=(",", ":")),
        }
    )
    return session.post(url, headers=safe_headers(request_template["headers"]), data=body, timeout=(10, 60))


def list_query(
    session: requests.Session,
    request_template: dict[str, Any],
    query: str,
    max_rows: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw_rows: list[dict[str, Any]] = []
    normalized_rows: list[dict[str, Any]] = []
    for offset in range(0, max_rows, 50):
        response = session.post(
            request_template["url"],
            headers=safe_headers(request_template["headers"]),
            data=set_query_and_offset(request_template["postData"], query, offset),
            timeout=(10, 60),
        )
        payload = response.json()
        page_rows = [row for row in payload.get("1", []) if isinstance(row, dict)]
        raw_rows.extend(page_rows)
        normalized_rows.extend(normalize_row(row) for row in page_rows)
        if len(page_rows) < 50:
            break
    return raw_rows, normalized_rows


def build_targets(
    raw_by_query: dict[str, list[dict[str, Any]]],
    allowed_product_ids: set[str],
    paid_cohort_text: str,
    *,
    allow_paid_cohort: bool,
) -> tuple[dict[tuple[str, str, str], dict[str, Any]], list[dict[str, str]]]:
    violations: list[dict[str, str]] = []
    targets: dict[tuple[str, str, str], dict[str, Any]] = {}
    for query, rows in raw_by_query.items():
        for row in rows:
            offer_id = str(row.get("1") or "").strip()
            feed_label = str(row.get("10") or "").strip()
            language = str(row.get("11") or "").strip()
            title = str(row.get("2") or "").strip()
            match = re.match(r"shopify_[A-Z]+_(\d+)_(\d+)", offer_id)
            if not match:
                violations.append({"query": query, "offer_id": offer_id, "reason": "unexpected_offer_id_shape"})
                continue
            product_id = match.group(1)
            if product_id not in allowed_product_ids:
                violations.append(
                    {
                        "query": query,
                        "offer_id": offer_id,
                        "product_id": product_id,
                        "reason": "product_not_in_allowed_supplier_match_set",
                    }
                )
                continue
            if offer_id in paid_cohort_text and not allow_paid_cohort:
                violations.append(
                    {
                        "query": query,
                        "offer_id": offer_id,
                        "product_id": product_id,
                        "reason": "offer_appears_in_paid_cohort",
                    }
                )
                continue
            if not feed_label or not language:
                violations.append(
                    {
                        "query": query,
                        "offer_id": offer_id,
                        "product_id": product_id,
                        "reason": "missing_feed_label_or_language",
                    }
                )
                continue

            key = (offer_id, feed_label, language)
            existing = targets.get(key, {"source_queries": []})
            targets[key] = {
                "offer_id": offer_id,
                "feed_label": feed_label,
                "language": language,
                "product_id": product_id,
                "title": title,
                "source_queries": sorted(set(existing.get("source_queries", []) + [query])),
            }
    return targets, violations


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    allowed_product_ids = {item.strip() for item in args.allowed_product_ids.split(",") if item.strip()}
    paid_cohort_text = args.paid_cohort.read_text(encoding="utf-8") if args.paid_cohort.exists() else ""
    queries = [item.strip() for item in args.queries.split(",") if item.strip()]

    page = find_items_page(args.cdp_port)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        cookies = google_cookies(client)
        request_template = capture_product_list_request(client)
    finally:
        client.close()

    parsed = urllib.parse.parse_qs(request_template["postData"], keep_blank_values=True)
    f_sid = parsed.get("f.sid", [""])[0]
    session = requests.Session()
    session.cookies.update(cookies)

    for batch_no in range(1, args.batches + 1):
        raw_by_query: dict[str, list[dict[str, Any]]] = {}
        normalized_counts: dict[str, int] = {}
        for query in queries:
            raw_rows, normalized_rows = list_query(session, request_template, query, args.max_rows_per_query)
            raw_by_query[query] = raw_rows
            normalized_counts[query] = len(normalized_rows)

        targets, violations = build_targets(
            raw_by_query,
            allowed_product_ids,
            paid_cohort_text,
            allow_paid_cohort=args.allow_paid_cohort,
        )
        if violations:
            out_path = args.output_dir / f"batch_{batch_no:02d}_aborted_violations.json"
            out_path.write_text(
                json.dumps(
                    {
                        "generated_at": datetime.now().isoformat(timespec="seconds"),
                        "batch": batch_no,
                        "query_counts": normalized_counts,
                        "violations": violations,
                    },
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            print(json.dumps({"batch": batch_no, "aborted": True, "output": str(out_path), "violations": len(violations)}))
            return 2

        if not targets:
            out_path = args.output_dir / f"batch_{batch_no:02d}_zero_targets.json"
            out_path.write_text(
                json.dumps(
                    {
                        "generated_at": datetime.now().isoformat(timespec="seconds"),
                        "batch": batch_no,
                        "query_counts": normalized_counts,
                        "target_count": 0,
                    },
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            print(json.dumps({"batch": batch_no, "zero_targets": True, "output": str(out_path)}))
            break

        delete_results: list[dict[str, Any]] = []
        sorted_targets = sorted(
            targets.values(), key=lambda item: (item["product_id"], item["feed_label"], item["language"], item["offer_id"])
        )
        chunk_size = max(1, args.chunk_size)
        for chunk_start in range(0, len(sorted_targets), chunk_size):
            chunk_targets = sorted_targets[chunk_start : chunk_start + chunk_size]
            offers = [
                {"1": target["offer_id"], "2": 2, "4": target["language"], "6": target["feed_label"]}
                for target in chunk_targets
            ]
            if args.dry_run:
                response_status = 0
                response_body = "DRY_RUN"
                success = True
            else:
                response = rpc(session, request_template, f_sid, "OfferInventoryService", "Delete", {"1": offers})
                response_status = response.status_code
                response_body = response.text[:500]
                success = response.status_code == 200 and response.text.strip() == "{}"
                time.sleep(args.sleep)
            for offset, target in enumerate(chunk_targets, start=1):
                delete_results.append(
                    {
                        **target,
                        "index": chunk_start + offset,
                        "request_offer": offers[offset - 1],
                        "request_chunk_size": len(offers),
                        "status": response_status,
                        "body": response_body,
                        "success": success,
                    }
                )
            deleted_count = min(chunk_start + len(chunk_targets), len(targets))
            if deleted_count % 50 == 0 or deleted_count == len(targets):
                print(json.dumps({"batch": batch_no, "deleted": deleted_count, "of": len(targets)}), flush=True)

        out_path = args.output_dir / f"batch_{batch_no:02d}_delete_results.json"
        out_path.write_text(
            json.dumps(
                {
                    "generated_at": datetime.now().isoformat(timespec="seconds"),
                    "batch": batch_no,
                    "dry_run": bool(args.dry_run),
                    "query_counts_before_delete": normalized_counts,
                    "target_count": len(targets),
                    "success_count": sum(1 for item in delete_results if item["success"]),
                    "failure_count": sum(1 for item in delete_results if not item["success"]),
                    "products": sorted({item["product_id"] for item in targets.values()}),
                    "delete_results": delete_results,
                },
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "batch": batch_no,
                    "output": str(out_path),
                    "target_count": len(targets),
                    "success_count": sum(1 for item in delete_results if item["success"]),
                    "failure_count": sum(1 for item in delete_results if not item["success"]),
                }
            ),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
