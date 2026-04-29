#!/usr/bin/env python3
"""Read live Merchant Center product labels through the logged-in browser.

The script uses the existing Chrome DevTools session on port 9222 to capture a
current Merchant Center product-list RPC request, then repeats that read-only
request for the clean-label gate queries. It stores only sanitized evidence:
no cookies, tokens, request headers, or account credentials are written.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import websocket


DEFAULT_ACCOUNT = "124884876"
DEFAULT_CDP_PORT = 9222
DEFAULT_SAMPLE_OFFER_ID = "shopify_US_7107978395745_41493652963425"
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-merchant-campaign-build-live-check"
)
DEFAULT_EXPECTED_LABELS_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-merchant-clean-label-upload/"
    "upload_matched_full_clean_labels_with_age_group.csv"
)

PRODUCT_FIELDS = [
    "calculated_visibility",
    "calculated_status",
    "thumbnail_link",
    "title",
    "availability",
    "product_id",
    "prices",
    "sale_price_suggestion",
    "availabilities",
    "primary_source_info",
    "last_updated_timestamp_seconds",
    "all_clicks",
    "approved_clicks",
    "tags",
    "feed_label",
    "language_code",
    "intended_countries",
    "intended_reporting_contexts",
    "channels",
    "edit",
    "aggregated_status",
    "is_ui_change_pending",
    "offer_visibility",
    "main_image_thumbnail_status",
    "custom_attribute_0",
    "custom_attribute_1",
    "custom_attribute_2",
    "custom_attribute_3",
    "custom_attribute_4",
    "sale_prices",
    "is_offer_value_pending",
    "doc_ids",
    "input_method_info",
    "counting_product_id",
]


class CdpClient:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(websocket_url, timeout=30, suppress_origin=True)
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def send(self, method: str, params: dict[str, Any] | None = None) -> int:
        message_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        return message_id

    def recv_until_id(self, message_id: int, timeout_seconds: int = 20) -> dict[str, Any]:
        start = time.time()
        while time.time() - start < timeout_seconds:
            event = json.loads(self.ws.recv())
            if event.get("id") == message_id:
                return event
        raise TimeoutError(f"Timed out waiting for CDP response {message_id}")

    def call(self, method: str, params: dict[str, Any] | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
        return self.recv_until_id(self.send(method, params), timeout_seconds)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def timestamp_to_iso(value: object) -> str:
    text = clean(value)
    if not text.isdigit():
        return ""
    return datetime.fromtimestamp(int(text), tz=timezone.utc).isoformat()


def read_expected_labels(path: Path, sample_offer_id: str) -> dict[str, str]:
    if not path.exists():
        return {}
    import csv

    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if clean(row.get("id")) != sample_offer_id:
                continue
            return {
                f"custom_label_{idx}": clean(row.get(f"custom_label_{idx}"))
                for idx in range(5)
            }
    return {}


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def find_items_page(cdp_port: int) -> dict[str, Any]:
    pages = get_json(f"http://127.0.0.1:{cdp_port}/json/list")
    for page in pages:
        if page.get("type") == "page" and "merchants.google.com/mc/items" in page.get("url", ""):
            return page
    raise RuntimeError(f"No live Merchant Center All products page found on CDP port {cdp_port}")


def google_cookies(client: CdpClient) -> dict[str, str]:
    response = client.call("Network.getAllCookies")
    cookies = response.get("result", {}).get("cookies", [])
    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies
        if "google.com" in cookie.get("domain", "")
    }


def capture_product_list_request(client: CdpClient) -> dict[str, Any]:
    client.send("Network.enable", {"maxTotalBufferSize": 10_000_000, "maxResourceBufferSize": 5_000_000})
    client.send("Page.reload", {"ignoreCache": True})

    start = time.time()
    fallback: dict[str, Any] | None = None
    while time.time() - start < 20:
        event = json.loads(client.ws.recv())
        if event.get("method") != "Network.requestWillBeSent":
            continue
        request = event.get("params", {}).get("request", {})
        url = request.get("url", "")
        if "UnifiedProductService/List" not in url:
            continue
        capture = {
            "url": url,
            "headers": request.get("headers", {}),
            "postData": request.get("postData", ""),
        }
        fallback = capture
        if "List%3A4" in url:
            return capture
    if fallback:
        return fallback
    raise RuntimeError("Could not capture a current Merchant Center product-list RPC request")


def set_search_query(post_data: str, query: str) -> str:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    if "__ar" not in parsed:
        raise RuntimeError("Captured request is missing __ar payload")
    ar_payload = json.loads(parsed["__ar"][0])
    options = ar_payload.setdefault("2", {}).setdefault("5", [])
    found = False
    for option in options:
        if option.get("1") == "search_query":
            option["2"] = query
            found = True
            break
    if not found:
        options.append({"1": "search_query", "2": query})

    field_list = ar_payload.setdefault("2", {}).setdefault("1", [])
    for field in PRODUCT_FIELDS:
        if field not in field_list:
            field_list.append(field)

    parsed["__ar"] = [json.dumps(ar_payload, separators=(",", ":"))]
    return urllib.parse.urlencode({key: values[0] for key, values in parsed.items()})


def safe_headers(headers: dict[str, str]) -> dict[str, str]:
    out = deepcopy(headers)
    for key in ["Content-Length", "Host", "Origin"]:
        out.pop(key, None)
    return out


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    source = row.get("43") or {}
    return {
        "merchant_center_item_id": clean(row.get("1")),
        "title": clean(row.get("2")),
        "last_updated_timestamp_seconds": clean(row.get("7")),
        "last_updated_utc": timestamp_to_iso(row.get("7")),
        "feed_label": clean(row.get("10")),
        "language_code": clean(row.get("11")),
        "custom_label_0": clean(row.get("27")),
        "custom_label_1": clean(row.get("28")),
        "custom_label_2": clean(row.get("29")),
        "custom_label_3": clean(row.get("30")),
        "custom_label_4": clean(row.get("31")),
        "source_id": clean(source.get("1") if isinstance(source, dict) else ""),
        "source_name": clean(source.get("3") if isinstance(source, dict) else ""),
        "raw_status": clean(row.get("17")),
        "raw_aggregate_status": clean(row.get("41")),
    }


def execute_query(
    session: requests.Session,
    request_template: dict[str, Any],
    query: str,
) -> dict[str, Any]:
    body = set_search_query(request_template["postData"], query)
    last_error = ""
    response = None
    for attempt in range(1, 4):
        try:
            response = session.post(
                request_template["url"],
                headers=safe_headers(request_template["headers"]),
                data=body,
                timeout=(10, 60),
            )
            break
        except requests.RequestException as exc:
            last_error = str(exc)
            if attempt == 3:
                return {
                    "query": query,
                    "status": "REQUEST_FAILED",
                    "body_length": 0,
                    "parse_error": last_error,
                    "row_count": 0,
                    "contains_paid_eligible": False,
                    "contains_us_test_ready": False,
                    "contains_old_custom_label_0_high": False,
                    "contains_old_custom_label_4_0_25": False,
                    "rows": [],
                    "body_excerpt": "",
                }
            time.sleep(attempt * 2)
    if response is None:
        raise RuntimeError(f"Merchant Center query failed without response: {last_error}")
    text = response.text
    rows: list[dict[str, Any]] = []
    parse_error = ""
    try:
        payload = response.json()
        rows = [normalize_row(row) for row in payload.get("1", []) if isinstance(row, dict)]
    except Exception as exc:  # pragma: no cover - evidence capture fallback
        parse_error = str(exc)

    return {
        "query": query,
        "status": response.status_code,
        "body_length": len(text),
        "parse_error": parse_error,
        "row_count": len(rows),
        "contains_paid_eligible": "paid_eligible" in text,
        "contains_us_test_ready": "us_test_ready" in text,
        "contains_old_custom_label_0_high": '"high"' in text,
        "contains_old_custom_label_4_0_25": '"0-25"' in text,
        "rows": rows[:100],
        "body_excerpt": text[:1500],
    }


def build_report(
    account: str,
    cdp_port: int,
    sample_offer_id: str,
    output_dir: Path,
    expected_labels_csv: Path,
) -> dict[str, Any]:
    page = find_items_page(cdp_port)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        cookies = google_cookies(client)
        request_template = capture_product_list_request(client)
    finally:
        client.close()

    session = requests.Session()
    session.cookies.update(cookies)
    queries = [sample_offer_id, "paid_eligible", "us_test_ready"]
    results = [execute_query(session, request_template, query) for query in queries]

    sample_result = results[0]
    sample_rows = sample_result["rows"]
    us_en_rows = [
        row
        for row in sample_rows
        if row["merchant_center_item_id"] == sample_offer_id
        and row["feed_label"] == "US"
        and row["language_code"] == "en"
    ]
    expected_labels = read_expected_labels(expected_labels_csv, sample_offer_id)
    campaign_filter_rows = [
        row
        for row in us_en_rows
        if row["custom_label_0"] == "paid_eligible" and row["custom_label_4"] == "us_test_ready"
    ]
    full_label_rows = []
    if expected_labels:
        full_label_rows = [
            row
            for row in us_en_rows
            if all(row.get(label_key) == expected_value for label_key, expected_value in expected_labels.items())
        ]
    observed_mismatches = []
    if expected_labels and us_en_rows:
        observed = us_en_rows[0]
        for label_key, expected_value in expected_labels.items():
            observed_value = observed.get(label_key, "")
            if observed_value != expected_value:
                observed_mismatches.append(
                    {
                        "label": label_key,
                        "expected": expected_value,
                        "observed": observed_value,
                    }
                )
    observed_us_en = [
        {
            "feed_label": row["feed_label"],
            "language_code": row["language_code"],
            "last_updated_utc": row["last_updated_utc"],
            "custom_label_0": row["custom_label_0"],
            "custom_label_1": row["custom_label_1"],
            "custom_label_2": row["custom_label_2"],
            "custom_label_3": row["custom_label_3"],
            "custom_label_4": row["custom_label_4"],
            "source_id": row["source_id"],
            "source_name": row["source_name"],
        }
        for row in us_en_rows
    ]

    campaign_filter_gate_passed = bool(campaign_filter_rows)
    full_label_gate_passed = bool(full_label_rows) if expected_labels else False
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_LIVE_MERCHANT_CENTER_CLEAN_LABEL_GATE",
        "merchant_center_account": account,
        "sample_paid_offer_id": sample_offer_id,
        "source_page_title": page.get("title"),
        "source_page_url": page.get("url"),
        "expected_labels_csv": str(expected_labels_csv),
        "expected_sample_labels": expected_labels,
        "expected_custom_label_0": "paid_eligible",
        "expected_custom_label_4": "us_test_ready",
        "gate_status": (
            "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE"
            if campaign_filter_gate_passed
            else "BLOCKED_CAMPAIGN_FILTER_LABELS_NOT_VISIBLE"
        ),
        "campaign_filter_gate_status": (
            "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE"
            if campaign_filter_gate_passed
            else "BLOCKED_CAMPAIGN_FILTER_LABELS_NOT_VISIBLE"
        ),
        "full_label_gate_status": (
            "PASS_ALL_EXPECTED_LABELS_VISIBLE"
            if full_label_gate_passed
            else "BLOCKED_FULL_LABEL_MISMATCH"
            if expected_labels
            else "BLOCKED_EXPECTED_LABEL_SOURCE_MISSING"
        ),
        "campaign_creation_allowed": campaign_filter_gate_passed,
        "all_expected_labels_visible": full_label_gate_passed,
        "observed_sample_label_mismatches": observed_mismatches,
        "observed_us_en_rows": observed_us_en,
        "query_results": results,
        "notes": [
            "Read-only browser RPC check; no Merchant Center or Google Ads changes were made.",
            "Cookies and request headers were used only in memory and are not written to disk.",
            "Campaign filters depend on custom_label_0=paid_eligible and custom_label_4=us_test_ready.",
            "Do not rely on custom_label_1..3 for campaign subdivision unless full_label_gate_status passes.",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "merchant_exact_label_readback_refresh_check.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(out_path),
                **{
                    k: report[k]
                    for k in [
                        "gate_status",
                        "campaign_filter_gate_status",
                        "full_label_gate_status",
                        "campaign_creation_allowed",
                        "all_expected_labels_visible",
                        "observed_sample_label_mismatches",
                        "observed_us_en_rows",
                    ]
                },
            },
            indent=2,
        )
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--sample-offer-id", default=DEFAULT_SAMPLE_OFFER_ID)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--expected-labels-csv", type=Path, default=DEFAULT_EXPECTED_LABELS_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        build_report(
            args.account,
            args.cdp_port,
            args.sample_offer_id,
            args.output_dir,
            args.expected_labels_csv,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
