#!/usr/bin/env python3
"""Capture read-only Merchant Center source/eligibility exports via browser RPC.

This exporter uses the existing authenticated Chrome DevTools session to
capture a current Merchant Center product-list RPC template, then replays that
read-only request with sanitized fields and pagination. It never writes cookies,
tokens, request headers, or Merchant Center mutations to disk.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import websocket


DEFAULT_ACCOUNT = "124884876"
DEFAULT_CDP_PORT = 9222
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-15-merchant-source-eligibility-browser-rpc-export"
)
DEFAULT_ELIGIBILITY = Path(
    "dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/"
    "2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv"
)

PRODUCT_FIELDS = [
    "product_id",
    "title",
    "last_updated_timestamp_seconds",
    "feed_label",
    "language_code",
    "prices",
    "calculated_status",
    "aggregated_status",
    "primary_source_info",
    "custom_attribute_0",
    "custom_attribute_1",
    "custom_attribute_2",
    "custom_attribute_3",
    "custom_attribute_4",
    "availability",
    "intended_countries",
    "intended_reporting_contexts",
    "channels",
    "doc_ids",
    "counting_product_id",
    "main_image_thumbnail_status",
]

FIELDNAMES = [
    "merchant_center_item_id",
    "title",
    "feed_label",
    "language_code",
    "source_id",
    "source_name",
    "price",
    "currency",
    "formatted_price",
    "raw_status",
    "raw_aggregate_status",
    "raw_availability",
    "raw_image_status",
    "strict_approved",
    "last_updated_utc",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
    "paid_cohort_match",
    "paid_eligible",
    "paid_status",
    "product_type_for_ads",
    "shopify_handle",
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

    def call(self, method: str, params: dict[str, Any] | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
        message_id = self.send(method, params)
        start = time.time()
        while time.time() - start < timeout_seconds:
            event = json.loads(self.ws.recv())
            if event.get("id") == message_id:
                return event
        raise TimeoutError(f"Timed out waiting for CDP response {message_id}")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def find_or_create_merchant_page(cdp_port: int, account: str) -> dict[str, Any]:
    pages = get_json(f"http://127.0.0.1:{cdp_port}/json/list")
    for page in pages:
        if page.get("type") == "page" and "merchants.google.com/mc/items" in page.get("url", ""):
            return page
    for page in pages:
        if page.get("type") == "page" and "merchants.google.com" in page.get("url", ""):
            return page
    raise RuntimeError(f"No authenticated Merchant Center page found on CDP port {cdp_port}")


def google_cookies(client: CdpClient) -> dict[str, str]:
    response = client.call("Network.getAllCookies")
    cookies = response.get("result", {}).get("cookies", [])
    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies
        if "google.com" in cookie.get("domain", "")
    }


def capture_product_list_request(client: CdpClient, account: str) -> dict[str, Any]:
    client.call("Network.enable", {"maxTotalBufferSize": 10_000_000, "maxResourceBufferSize": 5_000_000})
    client.send(
        "Page.navigate",
        {"url": f"https://merchants.google.com/mc/items?a={account}#DLM-MERCHANT-EXPORT-20260515"},
    )
    start = time.time()
    fallback: dict[str, Any] | None = None
    while time.time() - start < 40:
        event = json.loads(client.ws.recv())
        if event.get("method") != "Network.requestWillBeSent":
            continue
        request = event.get("params", {}).get("request", {})
        url = request.get("url", "")
        if "UnifiedProductService/List" not in url:
            continue
        fallback = {
            "url": url,
            "headers": request.get("headers", {}),
            "postData": request.get("postData", ""),
        }
        return fallback
    if fallback:
        return fallback
    raise RuntimeError("Could not capture a current Merchant Center product-list RPC request")


def safe_headers(headers: dict[str, str]) -> dict[str, str]:
    out = dict(headers)
    for key in ["Content-Length", "Host", "Origin"]:
        out.pop(key, None)
    return out


def build_body(post_data: str, offset: int, page_size: int) -> str:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    ar_payload = json.loads(parsed["__ar"][0])
    ar_payload.setdefault("2", {})["1"] = PRODUCT_FIELDS
    ar_payload["2"]["4"] = {"1": offset, "2": page_size}
    options = ar_payload["2"].setdefault("5", [])
    if not any(option.get("1") == "no_total_count" for option in options if isinstance(option, dict)):
        options.append({"1": "no_total_count", "2": "1"})
    parsed["__ar"] = [json.dumps(ar_payload, separators=(",", ":"))]
    return urllib.parse.urlencode({key: values[0] for key, values in parsed.items()})


def timestamp_to_iso(value: object) -> str:
    text = clean(value)
    if not text.isdigit():
        return ""
    return datetime.fromtimestamp(int(text), tz=timezone.utc).isoformat()


def price_parts(value: Any) -> tuple[str, str, str]:
    if not isinstance(value, dict):
        return "", "", ""
    node = value.get("2") if isinstance(value.get("2"), dict) else value
    units = clean(node.get("1") if isinstance(node, dict) else "")
    currency = clean(node.get("2") if isinstance(node, dict) else "")
    formatted = clean(node.get("3") if isinstance(node, dict) else "")
    price = ""
    if units.isdigit():
        price = f"{int(units) / 1000000:.2f}"
    return price, currency, formatted


def normalize_row(row: dict[str, Any], paid_by_item: dict[str, dict[str, str]]) -> dict[str, str]:
    source = row.get("43") if isinstance(row.get("43"), dict) else {}
    price, currency, formatted = price_parts(row.get("15"))
    item_id = clean(row.get("1"))
    paid = paid_by_item.get(item_id, {})
    raw_status = clean(row.get("17"))
    raw_aggregate = clean(row.get("41"))
    raw_image = json.dumps(row.get("50"), sort_keys=True) if row.get("50") is not None else ""
    return {
        "merchant_center_item_id": item_id,
        "title": clean(row.get("2")),
        "feed_label": clean(row.get("10")),
        "language_code": clean(row.get("11")),
        "source_id": clean(source.get("1") if isinstance(source, dict) else ""),
        "source_name": clean(source.get("3") if isinstance(source, dict) else ""),
        "price": price,
        "currency": currency,
        "formatted_price": formatted,
        "raw_status": raw_status,
        "raw_aggregate_status": raw_aggregate,
        "raw_availability": clean(row.get("16")),
        "raw_image_status": raw_image,
        "strict_approved": "TRUE" if raw_status == "4" and raw_aggregate == "2" else "FALSE",
        "last_updated_utc": timestamp_to_iso(row.get("7")),
        "custom_label_0": clean(row.get("27")),
        "custom_label_1": clean(row.get("28")),
        "custom_label_2": clean(row.get("29")),
        "custom_label_3": clean(row.get("30")),
        "custom_label_4": clean(row.get("31")),
        "paid_cohort_match": "TRUE" if paid else "FALSE",
        "paid_eligible": clean(paid.get("paid_eligible")),
        "paid_status": clean(paid.get("paid_status")),
        "product_type_for_ads": clean(paid.get("marketing_product_set_type")),
        "shopify_handle": clean(paid.get("handle")),
    }


def read_paid_cohort(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            clean(row.get("merchant_center_id")): row
            for row in csv.DictReader(handle)
            if clean(row.get("merchant_center_id"))
        }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def capture_rows(
    request_template: dict[str, Any],
    cookies: dict[str, str],
    page_size: int,
    max_pages: int,
) -> list[dict[str, Any]]:
    session = requests.Session()
    session.cookies.update(cookies)
    headers = safe_headers(request_template["headers"])
    rows: list[dict[str, Any]] = []
    seen_offsets: set[int] = set()
    for page_index in range(max_pages):
        offset = page_index * page_size
        seen_offsets.add(offset)
        body = build_body(request_template["postData"], offset, page_size)
        response = session.post(request_template["url"], headers=headers, data=body, timeout=(10, 90))
        if response.status_code != 200:
            raise RuntimeError(f"Product-list RPC returned HTTP {response.status_code} at offset {offset}")
        payload = response.json()
        page_rows = [row for row in payload.get("1", []) if isinstance(row, dict)]
        rows.extend(page_rows)
        if len(page_rows) < page_size:
            return rows
        if not page_rows:
            return rows
    raise RuntimeError(f"Stopped after max_pages={max_pages}; offsets attempted: {sorted(seen_offsets)[:5]}...")


def target_exports(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    return {
        "us_es_source_10627981690": [
            row
            for row in rows
            if row["feed_label"] == "US" and row["language_code"] == "es" and row["source_id"] == "10627981690"
        ],
        "ca_en_eligibility": [
            row
            for row in rows
            if row["language_code"] == "en" and row["currency"] == "CAD"
        ],
        "gb_en_eligibility": [
            row
            for row in rows
            if row["language_code"] == "en" and row["currency"] == "GBP"
        ],
        "au_en_eligibility": [
            row
            for row in rows
            if row["language_code"] == "en" and row["currency"] == "AUD"
        ],
    }


def summarize_export(name: str, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "export": name,
        "rows": len(rows),
        "strict_approved_rows": sum(1 for row in rows if row["strict_approved"] == "TRUE"),
        "paid_cohort_rows": sum(1 for row in rows if row["paid_cohort_match"] == "TRUE"),
        "paid_cohort_strict_approved_rows": sum(
            1 for row in rows if row["paid_cohort_match"] == "TRUE" and row["strict_approved"] == "TRUE"
        ),
        "feed_label_counts": dict(Counter(row["feed_label"] for row in rows).most_common()),
        "currency_counts": dict(Counter(row["currency"] for row in rows).most_common()),
        "language_counts": dict(Counter(row["language_code"] for row in rows).most_common()),
        "source_counts": dict(Counter(row["source_id"] for row in rows).most_common(12)),
        "raw_status_counts": dict(Counter(row["raw_status"] for row in rows).most_common()),
        "raw_aggregate_status_counts": dict(Counter(row["raw_aggregate_status"] for row in rows).most_common()),
    }


def build_outputs(args: argparse.Namespace) -> dict[str, Any]:
    page = find_or_create_merchant_page(args.cdp_port, args.account)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        cookies = google_cookies(client)
        request_template = capture_product_list_request(client, args.account)
    finally:
        client.close()

    paid_by_item = read_paid_cohort(args.input_eligibility)
    raw_rows = capture_rows(request_template, cookies, args.page_size, args.max_pages)
    normalized = [normalize_row(row, paid_by_item) for row in raw_rows]
    exports = target_exports(normalized)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    all_rows_path = args.output_dir / "merchant_all_products_browser_rpc_sanitized.csv"
    write_csv(all_rows_path, normalized)
    paths["all_products_sanitized"] = str(all_rows_path)
    for name, export_rows in exports.items():
        path = args.output_dir / f"merchant_{name}.csv"
        write_csv(path, export_rows)
        paths[name] = str(path)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_MERCHANT_CENTER_BROWSER_RPC_SOURCE_ELIGIBILITY_EXPORT",
        "merchant_center_account": args.account,
        "cdp_port": args.cdp_port,
        "source_page_title": page.get("title"),
        "source_page_url": page.get("url"),
        "global_rows_captured": len(normalized),
        "paid_cohort_input": str(args.input_eligibility),
        "paid_cohort_items_loaded": len(paid_by_item),
        "exports": {name: summarize_export(name, rows) for name, rows in exports.items()},
        "global_feed_language_currency_counts": {
            f"{row['feed_label']}|{row['language_code']}|{row['currency']}": count
            for (row, count) in []
        },
        "top_feed_language_currency_counts": dict(
            Counter(
                f"{row['feed_label']}|{row['language_code']}|{row['currency']}"
                for row in normalized
            ).most_common(30)
        ),
        "outputs": paths,
        "guardrails_preserved": [
            "no Merchant uploads",
            "no source refresh or sync",
            "no source/feed/product edits",
            "no product-group, campaign, bid, budget, status, or conversion changes",
            "cookies and request headers used only in memory and not written to disk",
        ],
        "notes": [
            "strict_approved is raw_status=4 and raw_aggregate_status=2 from Merchant Center product-list RPC.",
            "CA/en, GB/en, and AU/en exports are selected by English language plus CAD/GBP/AUD currency from the current product-list rows.",
            "US/es source export is selected by feed_label=US, language_code=es, and source_id=10627981690.",
        ],
    }
    summary_path = args.output_dir / "merchant_source_eligibility_browser_rpc_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    paths["summary"] = str(summary_path)

    report_path = args.output_dir / "MERCHANT_SOURCE_ELIGIBILITY_BROWSER_RPC_EXPORT.md"
    lines = [
        "# Merchant Source / Eligibility Browser RPC Export",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "Mode: read-only Merchant Center browser RPC export. No Merchant, Ads, Shopify, Pinterest, feed, product, product-group, bid, budget, status, capacity, or conversion writes were made.",
        "",
        "## Export Summary",
        "",
        "| Export | Rows | Strict approved | Paid-cohort rows | Paid-cohort strict approved | Key source/currency |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for name, export_summary in summary["exports"].items():
        source_or_currency = export_summary["source_counts"] or export_summary["currency_counts"]
        lines.append(
            f"| `{name}` | {export_summary['rows']} | {export_summary['strict_approved_rows']} | "
            f"{export_summary['paid_cohort_rows']} | {export_summary['paid_cohort_strict_approved_rows']} | "
            f"`{json.dumps(source_or_currency, sort_keys=True)}` |"
        )
    lines.extend(
        [
            "",
            "## Decision Boundary",
            "",
            "- This export is evidence only. It does not approve Merchant repair, capacity requests, Shopping campaign creation, feed/title changes, product-group changes, bid/budget/status changes, or conversion-goal changes.",
            "- Treat `US/es` source `10627981690` separately from CA/en, GB/en, and AU/en English currency eligibility.",
            "- Any live Merchant repair or paid-media mutation still needs an exact owner approval packet.",
            "",
            "## Files",
            "",
        ]
    )
    for key, value in paths.items():
        lines.append(f"- `{key}`: `{value}`")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths["report"] = str(report_path)
    summary["outputs"] = paths
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--input-eligibility", type=Path, default=DEFAULT_ELIGIBILITY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--page-size", type=int, default=500)
    parser.add_argument("--max-pages", type=int, default=1000)
    return parser.parse_args()


def main() -> None:
    try:
        summary = build_outputs(parse_args())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
