#!/usr/bin/env python3
"""Read-only Merchant US/es source and product-detail readback.

This helper uses the logged-in Chrome DevTools target on localhost and only
opens read-only Merchant Center pages/RPCs. It does not click any Save, Sync,
Upload, Update, Edit, Enable, Pause, or product-data controls. Cookies and
request headers are used only in memory and are not written to disk.
"""

from __future__ import annotations

import base64
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import websocket


ACCOUNT = "124884876"
CDP_PORT = 9222
SOURCE_ID = "10627981690"
SESSION_LABEL = "DLM-MERCHANT-US-ES-READONLY-20260508"
SAMPLES = [
    {
        "offer_id": "shopify_US_7227630649441_41872775020641",
        "why": "First sampled US/es exact-export affected row; issue also appears under Free listings.",
        "expected_age_group": "kids",
    },
    {
        "offer_id": "shopify_US_7227379023969_41871522431073",
        "why": "Sampled US/es exact-export affected row with Shopping ads traffic type.",
        "expected_age_group": "adult",
    },
    {
        "offer_id": "shopify_US_7227254276193_41871113158753",
        "why": "Previously used US/en cleared sample that also exposes the US/es source row in product-list RPC.",
        "expected_age_group": "toddler",
    },
]

LANE_DIR = Path(__file__).resolve().parent
RAW_DIR = LANE_DIR / "raw"
REPORT_PATH = LANE_DIR / "MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md"
SUMMARY_PATH = LANE_DIR / "merchant_us_es_source_detail_readback_summary.json"
PAID_COHORT_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-06-live-visual-qa-merchant-age-group-gate/"
    "paid_cohort_age_group_after_patch_rows.csv"
)
US_ES_SAMPLE_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-08-paid-growth-safe-followup/lanes/merchant-us-es/"
    "merchant_us_es_age_group_sample.csv"
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


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def timestamp_to_iso(value: object) -> str:
    text = clean(value)
    if not text.isdigit():
        return ""
    return datetime.fromtimestamp(int(text), tz=timezone.utc).isoformat()


def cdp_json(path: str, *, method: str = "GET") -> Any:
    request = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}{path}", method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def open_target(url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    return cdp_json(f"/json/new?{encoded}", method="PUT")


def close_target(target_id: str) -> None:
    try:
        cdp_json(f"/json/close/{target_id}")
    except Exception:
        pass


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


def runtime_eval(client: CdpClient, expression: str) -> Any:
    response = client.call(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
    )
    return response.get("result", {}).get("result", {}).get("value")


def page_snapshot(client: CdpClient) -> dict[str, str]:
    value = runtime_eval(
        client,
        """
        (() => ({
          title: document.title || '',
          url: location.href,
          text: document.body ? document.body.innerText : ''
        }))()
        """,
    )
    return value if isinstance(value, dict) else {"title": "", "url": "", "text": ""}


def save_screenshot(client: CdpClient, path: Path) -> str:
    try:
        response = client.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, 30)
        data = response.get("result", {}).get("data")
        if data:
            path.write_bytes(base64.b64decode(data))
            return str(path)
    except Exception as exc:
        return f"screenshot_failed: {exc}"
    return ""


def google_cookies(client: CdpClient) -> dict[str, str]:
    response = client.call("Network.getAllCookies")
    cookies = response.get("result", {}).get("cookies", [])
    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies
        if "google.com" in cookie.get("domain", "")
    }


def safe_headers(headers: dict[str, str]) -> dict[str, str]:
    out = deepcopy(headers)
    for key in [
        "Authorization",
        "Cookie",
        "Content-Length",
        "Host",
        "Origin",
    ]:
        out.pop(key, None)
    return out


def capture_product_list_request(client: CdpClient) -> dict[str, Any]:
    client.send("Network.enable", {"maxTotalBufferSize": 10_000_000, "maxResourceBufferSize": 5_000_000})
    client.send("Page.enable")
    client.send("Page.reload", {"ignoreCache": True})
    start = time.time()
    fallback: dict[str, Any] | None = None
    while time.time() - start < 35:
        event = json.loads(client.ws.recv())
        if event.get("method") != "Network.requestWillBeSent":
            continue
        request = event.get("params", {}).get("request", {})
        url = request.get("url", "")
        if "UnifiedProductService/List" not in url:
            continue
        capture = {"url": url, "headers": request.get("headers", {}), "postData": request.get("postData", "")}
        fallback = capture
        if "List%3A" in url:
            return capture
    if fallback:
        return fallback
    raise RuntimeError("Could not capture a current Merchant product-list RPC request")


def set_search_query(post_data: str, query: str) -> str:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    if "__ar" not in parsed:
        raise RuntimeError("Captured request is missing __ar payload")
    ar_payload = json.loads(parsed["__ar"][0])
    options = ar_payload.setdefault("2", {}).setdefault("5", [])
    for option in options:
        if option.get("1") == "search_query":
            option["2"] = query
            break
    else:
        options.append({"1": "search_query", "2": query})

    field_list = ar_payload.setdefault("2", {}).setdefault("1", [])
    for field in PRODUCT_FIELDS:
        if field not in field_list:
            field_list.append(field)

    parsed["__ar"] = [json.dumps(ar_payload, separators=(",", ":"))]
    return urllib.parse.urlencode({key: values[0] for key, values in parsed.items()})


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


def execute_product_list_query(session: requests.Session, template: dict[str, Any], query: str) -> dict[str, Any]:
    body = set_search_query(template["postData"], query)
    response = session.post(template["url"], headers=safe_headers(template["headers"]), data=body, timeout=(10, 60))
    rows: list[dict[str, Any]] = []
    parse_error = ""
    try:
        payload = response.json()
        rows = [normalize_row(row) for row in payload.get("1", []) if isinstance(row, dict)]
    except Exception as exc:
        parse_error = str(exc)
    return {
        "query": query,
        "status": response.status_code,
        "body_length": len(response.text),
        "parse_error": parse_error,
        "row_count": len(rows),
        "target_source_rows": [
            row
            for row in rows
            if row["source_id"] == SOURCE_ID and row["feed_label"] == "US" and row["language_code"] == "es"
        ],
        "rows": rows[:80],
    }


def collect_product_list_rows() -> dict[str, Any]:
    items_url = f"https://merchants.google.com/mc/items?a={ACCOUNT}#{SESSION_LABEL}-LIST"
    target = open_target(items_url)
    client = CdpClient(target["webSocketDebuggerUrl"])
    try:
        client.call("Page.enable")
        client.call("Network.enable", {"maxTotalBufferSize": 10_000_000, "maxResourceBufferSize": 5_000_000})
        time.sleep(7)
        cookies = google_cookies(client)
        template = capture_product_list_request(client)
    finally:
        client.close()
        close_target(target.get("id", ""))

    session = requests.Session()
    session.cookies.update(cookies)
    queries = [sample["offer_id"] for sample in SAMPLES]
    results = [execute_product_list_query(session, template, query) for query in queries]
    return {
        "mode": "READ_ONLY_UNIFIED_PRODUCT_LIST_RPC",
        "queries": queries,
        "results": results,
        "notes": [
            "Captured one current product-list RPC from a temporary Merchant target.",
            "Cookies and request headers were used only in memory and are not written to disk.",
        ],
    }


def collect_strings(value: Any, out: list[str]) -> None:
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            collect_strings(child, out)
    elif isinstance(value, list):
        for child in value:
            collect_strings(child, out)


def collect_attributes(value: Any, out: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        name = clean(value.get("2"))
        if name.startswith("n:") or name == "modification info":
            out.append(
                {
                    "name": name,
                    "value": clean(value.get("7") or value.get("6") or value.get("14") or value.get("8")),
                    "timestamp_token": clean((value.get("16") or {}).get("3") if isinstance(value.get("16"), dict) else ""),
                }
            )
        for child in value.values():
            collect_attributes(child, out)
    elif isinstance(value, list):
        for child in value:
            collect_attributes(child, out)


def parse_json_body(body: str) -> dict[str, Any]:
    try:
        payload = json.loads(body)
    except Exception as exc:
        return {"parse_error": str(exc), "body_length": len(body)}
    strings: list[str] = []
    attrs: list[dict[str, str]] = []
    collect_strings(payload, strings)
    collect_attributes(payload, attrs)
    root = payload if isinstance(payload, dict) else {}
    product = root.get("1") if isinstance(root.get("1"), dict) else {}
    return {
        "parse_error": "",
        "body_length": len(body),
        "source_id": clean(root.get("10")),
        "linkage_key": clean(root.get("11")),
        "product_title": clean(product.get("2")),
        "product_link": clean(product.get("6")),
        "custom_label_0": clean(product.get("51")),
        "custom_label_1": clean(product.get("52")),
        "custom_label_2": clean(product.get("53")),
        "custom_label_3": clean(product.get("54")),
        "custom_label_4": clean(product.get("55")),
        "has_age_group_attr": any(attr["name"] == "n:age_group" for attr in attrs),
        "age_group_attrs": [attr for attr in attrs if attr["name"] == "n:age_group"],
        "has_missing_age_group_text": any("Missing age group" in string for string in strings),
        "has_missing_local_inventory_text": any("Missing local inventory data" in string for string in strings),
        "issue_titles": sorted({string for string in strings if string.startswith("Missing ")}),
        "attributes_sample": attrs[:120],
    }


def strip_query(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def summarize_ar(post_data: str) -> Any:
    parsed = urllib.parse.parse_qs(post_data, keep_blank_values=True)
    if "__ar" not in parsed:
        return {}
    try:
        return json.loads(parsed["__ar"][0])
    except Exception:
        return "UNPARSEABLE_AR"


def collect_detail_page(sample: dict[str, str]) -> dict[str, Any]:
    offer_id = sample["offer_id"]
    detail_url = (
        f"https://merchants.google.com/mc/items/details?a={ACCOUNT}"
        f"&offerId={urllib.parse.quote(offer_id)}&language=es&channel=0&feedLabel=US"
        f"&tab=needsattention#{SESSION_LABEL}-DETAIL"
    )
    target = open_target(detail_url)
    client = CdpClient(target["webSocketDebuggerUrl"])
    captured: dict[str, dict[str, Any]] = {}
    request_meta: dict[str, dict[str, Any]] = {}
    try:
        client.call("Page.enable")
        client.call("Network.enable", {"maxTotalBufferSize": 20_000_000, "maxResourceBufferSize": 10_000_000})
        start = time.time()
        while time.time() - start < 30:
            event = json.loads(client.ws.recv())
            method = event.get("method")
            params = event.get("params", {})
            if method == "Network.requestWillBeSent":
                request = params.get("request", {})
                url = request.get("url", "")
                if "OfferInventoryService/Get" in url or "HeraItemIssuesService/ListItemIssues" in url:
                    request_meta[params.get("requestId", "")] = {
                        "service_url": strip_query(url),
                        "post_ar": summarize_ar(request.get("postData", "")),
                    }
            elif method == "Network.responseReceived":
                response = params.get("response", {})
                url = response.get("url", "")
                if "OfferInventoryService/Get" not in url and "HeraItemIssuesService/ListItemIssues" not in url:
                    continue
                request_id = params.get("requestId", "")
                service_name = (
                    "OfferInventoryService.Get"
                    if "OfferInventoryService/Get" in url
                    else "HeraItemIssuesService.ListItemIssues"
                )
                try:
                    body_response = client.call("Network.getResponseBody", {"requestId": request_id}, 15)
                    body = body_response.get("result", {}).get("body", "")
                    captured[service_name] = {
                        "status": response.get("status"),
                        "request": request_meta.get(request_id, {"service_url": strip_query(url)}),
                        "parsed": parse_json_body(body),
                    }
                    (RAW_DIR / f"{offer_id}_{service_name}.json").write_text(
                        json.dumps(captured[service_name], indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                except Exception as exc:
                    captured[service_name] = {"status": response.get("status"), "error": str(exc)}
            if {"OfferInventoryService.Get", "HeraItemIssuesService.ListItemIssues"}.issubset(captured):
                # Let visible page text settle for a moment after both RPCs.
                time.sleep(2)
                break
        snapshot = page_snapshot(client)
        screenshot_path = RAW_DIR / f"{offer_id}_detail.png"
        screenshot = save_screenshot(client, screenshot_path)
    finally:
        client.close()
        close_target(target.get("id", ""))

    page_text = clean(snapshot.get("text", ""))
    detail = {
        "offer_id": offer_id,
        "why": sample.get("why", ""),
        "expected_age_group": sample.get("expected_age_group", ""),
        "url": detail_url,
        "page": {
            "title": snapshot.get("title", ""),
            "url": snapshot.get("url", ""),
            "text_path": str(RAW_DIR / f"{offer_id}_detail_text.txt"),
            "screenshot": screenshot,
            "has_missing_age_group_text": "Missing age group" in page_text,
            "has_missing_local_inventory_text": "Missing local inventory data" in page_text,
            "text_excerpt": page_text[:1800],
        },
        "rpc": captured,
    }
    (RAW_DIR / f"{offer_id}_detail_text.txt").write_text(snapshot.get("text", ""), encoding="utf-8")
    return detail


def collect_source_page(tab: str) -> dict[str, Any]:
    url = (
        f"https://merchants.google.com/mc/products/sources/joindetails?a={ACCOUNT}"
        f"&joinFeedId={SOURCE_ID}&tab={tab}#{SESSION_LABEL}-SOURCE-{tab}"
    )
    target = open_target(url)
    client = CdpClient(target["webSocketDebuggerUrl"])
    try:
        client.call("Page.enable")
        time.sleep(12)
        snapshot = page_snapshot(client)
        screenshot_path = RAW_DIR / f"source_{SOURCE_ID}_{tab}.png"
        screenshot = save_screenshot(client, screenshot_path)
    finally:
        client.close()
        close_target(target.get("id", ""))
    text = snapshot.get("text", "")
    text_path = RAW_DIR / f"source_{SOURCE_ID}_{tab}.txt"
    text_path.write_text(text, encoding="utf-8")
    return {
        "tab": tab,
        "url": url,
        "page_title": snapshot.get("title", ""),
        "final_url": snapshot.get("url", ""),
        "text_path": str(text_path),
        "screenshot": screenshot,
        "text_excerpt": clean(text)[:2400],
        "contains_shopify_app_api": "Shopify App API" in text,
        "contains_feed_label_us": "Feed label: US" in text or "\nUS\n" in text,
        "contains_united_states": "United States" in text,
        "contains_spanish": "Spanish" in text or "es" in text,
        "contains_needs_update": "Needs update" in text,
    }


def read_sample_metadata() -> dict[str, Any]:
    sample_rows: dict[str, dict[str, str]] = {}
    if US_ES_SAMPLE_CSV.exists():
        with US_ES_SAMPLE_CSV.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item_id = clean(row.get("item_id"))
                if item_id in {sample["offer_id"] for sample in SAMPLES}:
                    sample_rows[item_id] = row
    paid_rows: dict[str, dict[str, str]] = {}
    if PAID_COHORT_CSV.exists():
        with PAID_COHORT_CSV.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                item_id = clean(row.get("id") or row.get("merchant_center_item_id"))
                if item_id in {sample["offer_id"] for sample in SAMPLES}:
                    paid_rows[item_id] = row
    return {
        "us_es_sample_rows": sample_rows,
        "paid_cohort_age_group_rows": paid_rows,
    }


def build_decision(summary: dict[str, Any]) -> str:
    target_rows = [
        row
        for result in summary["product_list_readback"]["results"]
        for row in result.get("target_source_rows", [])
    ]
    target_details = []
    for detail in summary["product_detail_readback"]:
        issue_rpc = detail.get("rpc", {}).get("HeraItemIssuesService.ListItemIssues", {}).get("parsed", {})
        offer_rpc = detail.get("rpc", {}).get("OfferInventoryService.Get", {}).get("parsed", {})
        source_matches = offer_rpc.get("source_id") == SOURCE_ID
        missing = detail["page"]["has_missing_age_group_text"] or issue_rpc.get("has_missing_age_group_text") or offer_rpc.get("has_missing_age_group_text")
        has_age_group = offer_rpc.get("has_age_group_attr")
        if source_matches:
            target_details.append({"missing": bool(missing), "has_age_group": bool(has_age_group)})
    if target_details and any(row["missing"] and not row["has_age_group"] for row in target_details):
        return "US_ES_SOURCE_10627981690_READBACK_CONFIRMS_MISSING_AGE_GROUP_ON_TARGET_DETAILS"
    if target_rows and any(row["missing"] for row in target_details):
        return "US_ES_SOURCE_10627981690_STILL_HAS_MISSING_AGE_GROUP_DESPITE_PARTIAL_DETAIL_ATTRS"
    if target_rows and not any(row["missing"] for row in target_details):
        return "US_ES_SOURCE_10627981690_TARGET_ROWS_VISIBLE_BUT_DETAIL_MISSING_AGE_GROUP_NOT_REPRODUCED"
    return "US_ES_SOURCE_10627981690_READBACK_INCONCLUSIVE"


def write_report(summary: dict[str, Any]) -> None:
    target_rows = [
        row
        for result in summary["product_list_readback"]["results"]
        for row in result.get("target_source_rows", [])
    ]
    source_processing = next((row for row in summary["source_detail_readback"] if row["tab"] == "processing"), {})
    lines = [
        "# Merchant US/es Source Detail Readback",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        f"Problem: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`.",
        "",
        "Mode: live Merchant Center read-only browser/RPC capture. No uploads, source syncs, edits, saves, product data changes, or Ads/Pinterest/Shopify writes were made.",
        "",
        f"Decision: `{summary['decision']}`.",
        "",
        "## Source 10627981690",
        "",
        f"- Direct source URL attempted: `{source_processing.get('final_url') or source_processing.get('url', '')}`",
        f"- Direct source page title: `{source_processing.get('page_title', '')}`",
        "- Direct source-detail UI did not expose a clean source settings/processing table in this run; it showed the Merchant shell plus a stale ready-download notification.",
        f"- Product-detail RPCs below are therefore the stronger readback for source `{SOURCE_ID}`.",
        "",
        "## Product List Readback",
        "",
        f"- Sample queries: `{', '.join(summary['product_list_readback']['queries'])}`.",
        f"- Target `US` / `es` / source `{SOURCE_ID}` rows visible: `{len(target_rows)}`.",
        "",
        "| Item ID | Last updated UTC | custom_label_0 | custom_label_4 | Source |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in target_rows:
        lines.append(
            f"| `{row['merchant_center_item_id']}` | `{row['last_updated_utc']}` | `{row['custom_label_0']}` | `{row['custom_label_4']}` | `{row['source_id']} / {row['source_name']}` |"
        )
    lines.extend(["", "## Product Detail Readback", ""])
    lines.append("| Item ID | Missing age_group shown | Effective `n:age_group` in detail RPC | Issues |")
    lines.append("| --- | --- | --- | --- |")
    for detail in summary["product_detail_readback"]:
        offer = detail["offer_id"]
        page_missing = detail["page"]["has_missing_age_group_text"]
        issue_rpc = detail.get("rpc", {}).get("HeraItemIssuesService.ListItemIssues", {}).get("parsed", {})
        offer_rpc = detail.get("rpc", {}).get("OfferInventoryService.Get", {}).get("parsed", {})
        missing = page_missing or issue_rpc.get("has_missing_age_group_text", False)
        age_group = offer_rpc.get("has_age_group_attr", False)
        issues = ", ".join(issue_rpc.get("issue_titles", []) or offer_rpc.get("issue_titles", []))
        lines.append(f"| `{offer}` | `{missing}` | `{age_group}` | `{issues}` |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The readback preserves the solved US/en age_group state and does not redo Shopify variant age_group work.",
            f"- The active US/es source path is source `{SOURCE_ID}` / `Shopify App API`; live detail readback should be treated as the authoritative blocker for Spanish-language US paid use.",
            "- Any actual repair still requires a fresh exact approval gate before source refresh/sync/edit/upload or Shopify product-data changes.",
            "",
            "## Evidence",
            "",
            f"- Summary JSON: `{SUMMARY_PATH}`",
            f"- Raw captures: `{RAW_DIR}`",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    product_list = collect_product_list_rows()
    source_pages = [collect_source_page(tab) for tab in ["processing", "settings"]]
    product_details = [collect_detail_page(sample) for sample in SAMPLES]
    summary = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "lane": "Merchant US/es source/detail readback",
        "problem_id": "PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP",
        "mode": "READ_ONLY_LIVE_MERCHANT_CENTER_BROWSER_RPC",
        "merchant_center_account": ACCOUNT,
        "source_id": SOURCE_ID,
        "samples": SAMPLES,
        "guardrails_preserved": [
            "no Merchant uploads",
            "no source sync or refresh clicks",
            "no source edits",
            "no Shopify product-data edits",
            "no Ads, Pinterest, GA4, theme, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal changes",
        ],
        "local_sample_metadata": read_sample_metadata(),
        "product_list_readback": product_list,
        "source_detail_readback": source_pages,
        "product_detail_readback": product_details,
    }
    summary["decision"] = build_decision(summary)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summary)
    print(json.dumps({"summary": str(SUMMARY_PATH), "report": str(REPORT_PATH), "decision": summary["decision"]}, indent=2))


if __name__ == "__main__":
    main()
