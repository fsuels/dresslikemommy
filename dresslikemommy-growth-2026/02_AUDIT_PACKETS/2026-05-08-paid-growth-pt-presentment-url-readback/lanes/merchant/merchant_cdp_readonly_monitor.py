#!/usr/bin/env python3
"""Lane-local read-only Merchant Center monitor for the PT URL packet.

This helper opens its own Chrome DevTools targets, captures only sanitized
Merchant evidence, and clicks only the product-issues download control.
It intentionally performs no uploads, syncs, edits, toggles, or saves.
"""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import websocket


ACCOUNT = "124884876"
CDP_PORT = 9222
SESSION_LABEL = "DLM-MERCHANT-US-SourceRefresh-PT-URL-20260508"
SAMPLE_OFFER_ID = "shopify_US_7227254276193_41871113158753"
EXPECTED_LABELS_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-merchant-clean-label-upload/"
    "upload_matched_full_clean_labels_with_age_group.csv"
)
PAID_COHORT_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-06-live-visual-qa-merchant-age-group-gate/"
    "paid_cohort_age_group_after_patch_rows.csv"
)
PREVIOUS_SUMMARY = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/"
    "merchant-product-issues-summary-2026-05-07-2357.json"
)

LANE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = LANE_DIR / "browser-source-readback"
DOWNLOAD_DIR = LANE_DIR / "product-issues-browser-export"

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
    req = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}{path}", method=method)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def open_target(url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    return cdp_json(f"/json/new?{encoded}", method="PUT")


def close_target(target_id: str) -> None:
    try:
        cdp_json(f"/json/close/{target_id}")
    except Exception:
        pass


def activate_target(target_id: str) -> None:
    try:
        cdp_json(f"/json/activate/{target_id}")
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


def google_cookies(client: CdpClient) -> dict[str, str]:
    response = client.call("Network.getAllCookies")
    cookies = response.get("result", {}).get("cookies", [])
    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies
        if "google.com" in cookie.get("domain", "")
    }


def read_expected_labels(path: Path, sample_offer_id: str) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if clean(row.get("id")) == sample_offer_id:
                return {f"custom_label_{idx}": clean(row.get(f"custom_label_{idx}")) for idx in range(5)}
    return {}


def capture_product_list_request(client: CdpClient) -> dict[str, Any]:
    client.send("Network.enable", {"maxTotalBufferSize": 10_000_000, "maxResourceBufferSize": 5_000_000})
    client.send("Page.enable")
    client.send("Page.reload", {"ignoreCache": True})
    start = time.time()
    fallback: dict[str, Any] | None = None
    while time.time() - start < 30:
        event = json.loads(client.ws.recv())
        if event.get("method") != "Network.requestWillBeSent":
            continue
        request = event.get("params", {}).get("request", {})
        url = request.get("url", "")
        if "UnifiedProductService/List" not in url:
            continue
        capture = {"url": url, "headers": request.get("headers", {}), "postData": request.get("postData", "")}
        fallback = capture
        if "List%3A4" in url:
            return capture
    if fallback:
        return fallback
    raise RuntimeError("Could not capture a current Merchant Center product-list RPC request in own target")


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


def execute_query(session: requests.Session, request_template: dict[str, Any], query: str) -> dict[str, Any]:
    body = set_search_query(request_template["postData"], query)
    response = session.post(request_template["url"], headers=safe_headers(request_template["headers"]), data=body, timeout=(10, 60))
    text = response.text
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


def run_source_readback() -> dict[str, Any]:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    items_url = (
        f"https://merchants.google.com/mc/items?a={ACCOUNT}"
        "&timePeriod=2026-04-10%2C2026-05-08&marketingMethod=1"
        f"#{SESSION_LABEL}"
    )
    target = open_target(items_url)
    activate_target(target.get("id", ""))
    client = CdpClient(target["webSocketDebuggerUrl"])
    try:
        time.sleep(8)
        cookies = google_cookies(client)
        request_template = capture_product_list_request(client)
    finally:
        client.close()
        close_target(target.get("id", ""))

    session = requests.Session()
    session.cookies.update(cookies)
    queries = [SAMPLE_OFFER_ID, "paid_eligible", "us_test_ready"]
    results = [execute_query(session, request_template, query) for query in queries]

    sample_rows = results[0]["rows"]
    us_en_rows = [
        row
        for row in sample_rows
        if row["merchant_center_item_id"] == SAMPLE_OFFER_ID
        and row["feed_label"] == "US"
        and row["language_code"] == "en"
    ]
    expected_labels = read_expected_labels(EXPECTED_LABELS_CSV, SAMPLE_OFFER_ID)
    campaign_filter_rows = [
        row for row in us_en_rows if row["custom_label_0"] == "paid_eligible" and row["custom_label_4"] == "us_test_ready"
    ]
    full_label_rows = []
    if expected_labels:
        full_label_rows = [
            row for row in us_en_rows if all(row.get(label_key) == expected_value for label_key, expected_value in expected_labels.items())
        ]
    observed_mismatches = []
    if expected_labels and us_en_rows:
        observed = us_en_rows[0]
        for label_key, expected_value in expected_labels.items():
            observed_value = observed.get(label_key, "")
            if observed_value != expected_value:
                observed_mismatches.append({"label": label_key, "expected": expected_value, "observed": observed_value})

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_LIVE_MERCHANT_CENTER_CLEAN_LABEL_GATE_OWN_TARGET",
        "browser_session_label": SESSION_LABEL,
        "merchant_center_account": ACCOUNT,
        "sample_paid_offer_id": SAMPLE_OFFER_ID,
        "source_page_title": target.get("title"),
        "source_page_url": items_url,
        "expected_labels_csv": str(EXPECTED_LABELS_CSV),
        "expected_sample_labels": expected_labels,
        "expected_custom_label_0": "paid_eligible",
        "expected_custom_label_4": "us_test_ready",
        "gate_status": "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE" if campaign_filter_rows else "BLOCKED_CAMPAIGN_FILTER_LABELS_NOT_VISIBLE",
        "campaign_filter_gate_status": "PASS_CAMPAIGN_FILTER_LABELS_VISIBLE" if campaign_filter_rows else "BLOCKED_CAMPAIGN_FILTER_LABELS_NOT_VISIBLE",
        "full_label_gate_status": (
            "PASS_ALL_EXPECTED_LABELS_VISIBLE"
            if full_label_rows
            else "BLOCKED_FULL_LABEL_MISMATCH"
            if expected_labels
            else "BLOCKED_EXPECTED_LABEL_SOURCE_MISSING"
        ),
        "campaign_creation_allowed": bool(campaign_filter_rows),
        "all_expected_labels_visible": bool(full_label_rows) if expected_labels else False,
        "observed_sample_label_mismatches": observed_mismatches,
        "observed_us_en_rows": [
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
        ],
        "query_results": results,
        "notes": [
            "Read-only browser RPC check in this subagent's own CDP target.",
            "Cookies and request headers were used only in memory and are not written to disk.",
            "No Merchant upload, source sync/refresh, product edit, Google & YouTube toggle, or local inventory action occurred.",
        ],
    }
    out_path = SOURCE_DIR / "merchant_exact_label_readback_refresh_check.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def runtime_text(client: CdpClient) -> str:
    response = client.call(
        "Runtime.evaluate",
        {
            "expression": "document.body ? document.body.innerText : ''",
            "returnByValue": True,
        },
    )
    return response.get("result", {}).get("result", {}).get("value", "")


def click_download_button(client: CdpClient) -> dict[str, Any]:
    expression = r"""
(() => {
  const nodes = Array.from(document.querySelectorAll('button, [role="button"], a'));
  const candidates = nodes.map((el, index) => {
    const rect = el.getBoundingClientRect();
    return {
      index,
      text: (el.innerText || '').trim(),
      aria: el.getAttribute('aria-label') || '',
      title: el.getAttribute('title') || '',
      visible: rect.width > 0 && rect.height > 0,
      rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height}
    };
  });
  const target = candidates.find(item =>
    item.visible &&
    /Download a file containing all the currently filtered product issues/i.test(item.aria + ' ' + item.title)
  ) || candidates.find(item =>
    item.visible &&
    /file_download/i.test(item.text + ' ' + item.aria + ' ' + item.title)
  );
  if (!target) {
    return {clicked: false, candidates: candidates.slice(0, 80)};
  }
  const el = nodes[target.index];
  el.scrollIntoView({block: 'center', inline: 'center'});
  const rect = el.getBoundingClientRect();
  return {
    clicked: true,
    index: target.index,
    text: target.text,
    aria: target.aria,
    title: target.title,
    rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height}
  };
})()
"""
    response = client.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
    result = response.get("result", {}).get("result", {}).get("value") or {}
    if not result.get("clicked"):
        return result
    rect = result["rect"]
    x = rect["x"] + rect["w"] / 2
    y = rect["y"] + rect["h"] / 2
    client.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y, "button": "none"})
    client.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    client.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
    return result


def click_ready_download_notification(client: CdpClient) -> dict[str, Any]:
    expression = r"""
(() => {
  const bodyText = document.body ? document.body.innerText || '' : '';
  const nodes = Array.from(document.querySelectorAll('button, [role="button"], a'));
  const candidates = nodes.map((el, index) => {
    const rect = el.getBoundingClientRect();
    return {
      index,
      text: (el.innerText || '').trim(),
      aria: el.getAttribute('aria-label') || '',
      title: el.getAttribute('title') || '',
      visible: rect.width > 0 && rect.height > 0,
      rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height}
    };
  });
  const target = candidates.find(item =>
    item.visible &&
    /^Download$/i.test(item.text) &&
    /Ready to download/i.test(bodyText)
  );
  if (!target) {
    return {clicked: false, body_has_ready_to_download: /Ready to download/i.test(bodyText), candidates: candidates.slice(0, 80)};
  }
  const el = nodes[target.index];
  el.scrollIntoView({block: 'center', inline: 'center'});
  const rect = el.getBoundingClientRect();
  return {
    clicked: true,
    index: target.index,
    text: target.text,
    aria: target.aria,
    title: target.title,
    rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height},
    body_has_ready_to_download: true
  };
})()
"""
    response = client.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
    result = response.get("result", {}).get("result", {}).get("value") or {}
    if not result.get("clicked"):
        return result
    rect = result["rect"]
    x = rect["x"] + rect["w"] / 2
    y = rect["y"] + rect["h"] / 2
    client.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y, "button": "none"})
    client.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    client.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
    return result


def latest_csv_since(start_time: float) -> Path | None:
    csvs = sorted(DOWNLOAD_DIR.glob("product_issues_*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    for path in csvs:
        if path.stat().st_mtime >= start_time - 2:
            return path
    return None


def run_product_issues_download() -> tuple[dict[str, Any], Path | None]:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for old_partial in DOWNLOAD_DIR.glob("*.crdownload"):
        try:
            old_partial.unlink()
        except OSError:
            pass
    diagnostics_url = (
        f"https://merchants.google.com/mc/products/diagnostics?a={ACCOUNT}"
        "&marketingMethod=16&priorityFixes=true"
        f"#{SESSION_LABEL}"
    )
    target = open_target(diagnostics_url)
    activate_target(target.get("id", ""))
    client = CdpClient(target["webSocketDebuggerUrl"])
    download_start = time.time()
    clicked: dict[str, Any] = {"clicked": False}
    ready_download_clicked: dict[str, Any] = {"clicked": False}
    text = ""
    csv_path: Path | None = None
    try:
        client.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(DOWNLOAD_DIR)})
        client.call("Page.enable")
        client.call("Runtime.enable")
        time.sleep(12)
        for _ in range(10):
            text = runtime_text(client)
            if "Missing age group" in text or "Missing local inventory data" in text:
                break
            time.sleep(3)
        (DOWNLOAD_DIR / "diagnostics_page_text_before_download.txt").write_text(text, encoding="utf-8")
        clicked = click_download_button(client)
        if clicked.get("clicked"):
            for _ in range(30):
                time.sleep(1)
                ready_download_clicked = click_ready_download_notification(client)
                if ready_download_clicked.get("clicked"):
                    break
            stable_size = -1
            stable_seen = 0
            for _ in range(80):
                candidate = latest_csv_since(download_start)
                if candidate and candidate.exists():
                    size = candidate.stat().st_size
                    if size > 0 and size == stable_size:
                        stable_seen += 1
                    else:
                        stable_seen = 0
                        stable_size = size
                    if stable_seen >= 2 and not list(DOWNLOAD_DIR.glob("*.crdownload")):
                        csv_path = candidate
                        break
                time.sleep(1)
    finally:
        client.close()
        close_target(target.get("id", ""))

    files = [
        {
            "name": path.name,
            "size": path.stat().st_size,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        }
        for path in sorted(DOWNLOAD_DIR.glob("*"))
        if path.is_file()
    ]
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_MERCHANT_DIAGNOSTICS_DOWNLOAD_BUTTON_EXPORT_OWN_TARGET",
        "browser_session_label": SESSION_LABEL,
        "download_dir": str(DOWNLOAD_DIR),
        "page_id": target.get("id"),
        "page_url": diagnostics_url,
        "download_behavior": "set_via_Browser.setDownloadBehavior",
        "pre_text_contains_missing_age_group": "Missing age group" in text,
        "pre_text_contains_missing_local_inventory_data": "Missing local inventory data" in text,
        "clicked": clicked,
        "ready_download_clicked": ready_download_clicked,
        "files": files,
        "notes": [
            "Clicked only the diagnostics table download button if found.",
            "No upload, sync, source refresh, product edit, save, or apply action was performed.",
        ],
    }
    (DOWNLOAD_DIR / "download_attempt_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary, csv_path


def load_paid_ids() -> set[str]:
    with PAID_COHORT_CSV.open(newline="", encoding="utf-8") as handle:
        return {clean(row.get("merchant_center_item_id")) for row in csv.DictReader(handle) if clean(row.get("merchant_center_item_id"))}


def previous_missing_count() -> int | None:
    if not PREVIOUS_SUMMARY.exists():
        return None
    payload = json.loads(PREVIOUS_SUMMARY.read_text(encoding="utf-8"))
    value = payload.get("paid_missing_age_group_unique_item_ids_us_en_united_states")
    return int(value) if isinstance(value, int) or str(value).isdigit() else None


def parse_product_issues(csv_path: Path) -> dict[str, Any]:
    paid_ids = load_paid_ids()
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        for row in reader:
            rows.append(row)

    issue_counts = Counter(clean(row.get("Issue title")) for row in rows)
    unique_by_issue: dict[str, set[str]] = {}
    paid_unique_by_issue: dict[str, set[str]] = {}
    paid_issue_counts = Counter()
    paid_age_rows: list[dict[str, str]] = []
    paid_age_ids: set[str] = set()
    paid_local_inventory_ids: set[str] = set()
    traffic_counter = Counter()

    for row in rows:
        item_id = clean(row.get("Item ID"))
        issue = clean(row.get("Issue title"))
        unique_by_issue.setdefault(issue, set()).add(item_id)
        if item_id in paid_ids:
            paid_issue_counts[issue] += 1
            paid_unique_by_issue.setdefault(issue, set()).add(item_id)
            is_us_en = (
                clean(row.get("Feed label")) == "US"
                and clean(row.get("Language")) == "en"
                and clean(row.get("Country")) == "United States"
            )
            if is_us_en and issue == "Missing age group":
                paid_age_rows.append(row)
                paid_age_ids.add(item_id)
                traffic_counter[clean(row.get("Traffic type"))] += 1
            if is_us_en and issue == "Missing local inventory data":
                paid_local_inventory_ids.add(item_id)

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    rows_path = LANE_DIR / f"merchant-product-issues-paid-us-en-missing-age-group-rows-{stamp}.csv"
    ids_path = LANE_DIR / f"merchant-product-issues-paid-us-en-missing-age-group-ids-{stamp}.txt"
    if paid_age_rows:
        with rows_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(paid_age_rows[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(paid_age_rows)
    else:
        rows_path.write_text("", encoding="utf-8")
    ids_path.write_text("\n".join(sorted(paid_age_ids)) + ("\n" if paid_age_ids else ""), encoding="utf-8")

    previous = previous_missing_count()
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_BROWSER_PRODUCT_ISSUES_EXPORT_RECONCILIATION",
        "download_file": str(csv_path),
        "download_rows": len(rows),
        "fieldnames": fieldnames,
        "paid_cohort_input": str(PAID_COHORT_CSV),
        "paid_cohort_size": len(paid_ids),
        "issue_counts": {key: issue_counts[key] for key in sorted(issue_counts)},
        "unique_item_ids_by_issue": {key: len(value) for key, value in sorted(unique_by_issue.items())},
        "paid_issue_counts_by_row": {key: paid_issue_counts[key] for key in sorted(paid_issue_counts)},
        "paid_unique_item_ids_by_issue": {key: len(value) for key, value in sorted(paid_unique_by_issue.items())},
        "paid_missing_age_group_unique_item_ids_us_en_united_states": len(paid_age_ids),
        "paid_missing_age_group_us_en_rows_by_traffic_type": {key: traffic_counter[key] for key in sorted(traffic_counter)},
        "previous_paid_missing_age_group_unique_item_ids_us_en_united_states": previous,
        "delta_vs_previous_paid_us_en_missing_age_group_unique_items": None if previous is None else len(paid_age_ids) - previous,
        "sample_item_in_current_paid_us_en_missing_age_group": SAMPLE_OFFER_ID in paid_age_ids,
        "paid_missing_local_inventory_unique_item_ids_us_en_united_states": len(paid_local_inventory_ids),
        "dropshipping_note": (
            "Missing local inventory data is not a product-data fix target for this no-physical-store "
            "dropshipping business."
        ),
        "outputs": {"paid_missing_age_group_rows": str(rows_path), "paid_missing_age_group_ids": str(ids_path)},
    }
    summary_path = LANE_DIR / f"merchant-product-issues-summary-{stamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    source = run_source_readback()
    download_summary, csv_path = run_product_issues_download()
    product_issues = parse_product_issues(csv_path) if csv_path else {"status": "BLOCKED_NO_CSV_DOWNLOADED"}
    print(
        json.dumps(
            {
                "source_output": str(SOURCE_DIR / "merchant_exact_label_readback_refresh_check.json"),
                "source_observed_us_en_rows": source.get("observed_us_en_rows"),
                "download_clicked": download_summary.get("clicked", {}).get("clicked"),
                "download_csv": str(csv_path) if csv_path else "",
                "product_issues_summary": product_issues,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
