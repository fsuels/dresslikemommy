#!/usr/bin/env python3
"""Read-only Merchant Center product-issues export and paid-cohort reconciliation.

This helper opens a dedicated Chrome DevTools target for Merchant diagnostics,
sets Chrome's download path to this packet, and clicks only the diagnostics
product-issues download control. It performs no Merchant uploads, source
updates, syncs, product edits, or account writes.
"""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import websocket


ACCOUNT = "124884876"
CDP_PORT = 9222
SESSION_LABEL = "DLM-MERCHANT-EXACT-AGE-GROUP-EXPORT-20260508"
SAMPLE_OFFER_ID = "shopify_US_7227254276193_41871113158753"
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

PACKET_DIR = Path(__file__).resolve().parent
RAW_DIR = PACKET_DIR / "raw"
DOWNLOAD_DIR = RAW_DIR / "product-issues-browser-export"
RECON_DIR = PACKET_DIR / "reconciliation"


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def cdp_json(path: str, *, method: str = "GET") -> Any:
    req = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}{path}", method=method)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def open_target(url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    return cdp_json(f"/json/new?{encoded}", method="PUT")


def close_target(target_id: str) -> None:
    if not target_id:
        return
    try:
        cdp_json(f"/json/close/{target_id}")
    except Exception:
        pass


def activate_target(target_id: str) -> None:
    if not target_id:
        return
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


def runtime_text(client: CdpClient) -> str:
    response = client.call(
        "Runtime.evaluate",
        {"expression": "document.body ? document.body.innerText : ''", "returnByValue": True},
    )
    return response.get("result", {}).get("result", {}).get("value", "")


def click_by_rect(client: CdpClient, result: dict[str, Any]) -> None:
    rect = result["rect"]
    x = rect["x"] + rect["w"] / 2
    y = rect["y"] + rect["h"] / 2
    client.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y, "button": "none"})
    client.call(
        "Input.dispatchMouseEvent",
        {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1},
    )
    client.call(
        "Input.dispatchMouseEvent",
        {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1},
    )


def click_product_issues_download(client: CdpClient) -> dict[str, Any]:
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
    return {clicked: false, candidates: candidates.slice(0, 100)};
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
    if result.get("clicked"):
        click_by_rect(client, result)
    return result


def click_view_all_issues(client: CdpClient) -> dict[str, Any]:
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
    /^View all issues$/i.test(item.text)
  );
  if (!target) {
    return {clicked: false, candidates: candidates.slice(0, 100)};
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
    if result.get("clicked"):
        click_by_rect(client, result)
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
    return {clicked: false, body_has_ready_to_download: /Ready to download/i.test(bodyText), candidates: candidates.slice(0, 100)};
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
    if result.get("clicked"):
        click_by_rect(client, result)
    return result


def latest_csv_since(start_time: float) -> Path | None:
    csvs = sorted(DOWNLOAD_DIR.glob("product_issues_*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    for path in csvs:
        if path.stat().st_mtime >= start_time - 2:
            return path
    return None


def run_download_attempt(priority_fixes: bool) -> tuple[dict[str, Any], Path | None]:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for old_partial in DOWNLOAD_DIR.glob("*.crdownload"):
        try:
            old_partial.unlink()
        except OSError:
            pass

    url = (
        f"https://merchants.google.com/mc/products/diagnostics?a={ACCOUNT}"
        "&marketingMethod=16"
        f"{'&priorityFixes=true' if priority_fixes else ''}"
        f"#{SESSION_LABEL}-{'priority' if priority_fixes else 'all'}"
    )
    target = open_target(url)
    activate_target(target.get("id", ""))
    client = CdpClient(target["webSocketDebuggerUrl"])
    start = time.time()
    clicked: dict[str, Any] = {"clicked": False}
    view_all_clicked: dict[str, Any] = {"clicked": False}
    ready_clicked: dict[str, Any] = {"clicked": False}
    csv_path: Path | None = None
    text = ""
    try:
        client.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(DOWNLOAD_DIR.resolve())})
        client.call("Page.enable")
        client.call("Runtime.enable")
        time.sleep(12)
        for _ in range(12):
            text = runtime_text(client)
            if any(marker in text for marker in ["All products that need attention", "Show all fixes", "Great"]):
                break
            time.sleep(3)
        if "View all issues" in text and "All products that need attention" not in text:
            view_all_clicked = click_view_all_issues(client)
            if view_all_clicked.get("clicked"):
                for _ in range(15):
                    time.sleep(1)
                    text = runtime_text(client)
                    if "All products that need attention" in text:
                        break
        suffix = "priority" if priority_fixes else "all"
        (DOWNLOAD_DIR / f"diagnostics_page_text_before_download_{suffix}.txt").write_text(text, encoding="utf-8")
        clicked = click_product_issues_download(client)
        if clicked.get("clicked"):
            for _ in range(40):
                time.sleep(1)
                ready_clicked = click_ready_download_notification(client)
                if ready_clicked.get("clicked"):
                    break
            stable_size = -1
            stable_seen = 0
            for _ in range(100):
                candidate = latest_csv_since(start)
                if candidate and candidate.exists():
                    size = candidate.stat().st_size
                    if size > 0 and size == stable_size:
                        stable_seen += 1
                    else:
                        stable_size = size
                        stable_seen = 0
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
        "mode": "READ_ONLY_MERCHANT_DIAGNOSTICS_DOWNLOAD_BUTTON_EXPORT",
        "priority_fixes": priority_fixes,
        "browser_session_label": SESSION_LABEL,
        "download_dir": str(DOWNLOAD_DIR),
        "page_id": target.get("id"),
        "page_url": url,
        "download_behavior": "set_via_Browser.setDownloadBehavior",
        "pre_text_contains_missing_age_group": "Missing age group" in text,
        "pre_text_contains_missing_local_inventory_data": "Missing local inventory data" in text,
        "pre_text_contains_all_prioritized_resolved": "Great, all your prioritized fixes are resolved" in text,
        "clicked": clicked,
        "view_all_issues_clicked": view_all_clicked,
        "ready_download_clicked": ready_clicked,
        "files": files,
        "notes": [
            "Clicked only the diagnostics table download button if found.",
            "No upload, sync, source refresh, product edit, save, apply, enable, or spend action was performed.",
        ],
    }
    (DOWNLOAD_DIR / f"download_attempt_summary_{'priority' if priority_fixes else 'all'}.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary, csv_path


def load_paid_ids() -> set[str]:
    with PAID_COHORT_CSV.open(newline="", encoding="utf-8") as handle:
        return {
            clean(row.get("merchant_center_item_id"))
            for row in csv.DictReader(handle)
            if clean(row.get("merchant_center_item_id"))
        }


def previous_missing_count() -> int | None:
    if not PREVIOUS_SUMMARY.exists():
        return None
    payload = json.loads(PREVIOUS_SUMMARY.read_text(encoding="utf-8"))
    value = payload.get("paid_missing_age_group_unique_item_ids_us_en_united_states")
    return int(value) if isinstance(value, int) or str(value).isdigit() else None


def parse_product_issues(csv_path: Path) -> dict[str, Any]:
    RECON_DIR.mkdir(parents=True, exist_ok=True)
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
    traffic_counter = Counter()

    for row in rows:
        item_id = clean(row.get("Item ID"))
        issue = clean(row.get("Issue title"))
        unique_by_issue.setdefault(issue, set()).add(item_id)
        if item_id not in paid_ids:
            continue
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

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    rows_path = RECON_DIR / f"merchant-product-issues-paid-us-en-missing-age-group-rows-{stamp}.csv"
    ids_path = RECON_DIR / f"merchant-product-issues-paid-us-en-missing-age-group-ids-{stamp}.txt"
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
        "delta_vs_previous_paid_us_en_missing_age_group_unique_items": None
        if previous is None
        else len(paid_age_ids) - previous,
        "sample_item_in_current_paid_us_en_missing_age_group": SAMPLE_OFFER_ID in paid_age_ids,
        "outputs": {
            "paid_missing_age_group_rows": str(rows_path),
            "paid_missing_age_group_ids": str(ids_path),
        },
    }
    summary_path = RECON_DIR / f"merchant-product-issues-summary-{stamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    attempts: list[dict[str, Any]] = []
    csv_path: Path | None = None
    for priority_fixes in (True, False):
        summary, candidate = run_download_attempt(priority_fixes)
        attempts.append(summary)
        if candidate:
            csv_path = candidate
            break
    reconciliation = parse_product_issues(csv_path) if csv_path else {"status": "BLOCKED_NO_CSV_DOWNLOADED"}
    result = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "EXPORT_RECONCILED" if csv_path else "BLOCKED_NO_CSV_DOWNLOADED",
        "attempts": attempts,
        "download_csv": str(csv_path) if csv_path else "",
        "reconciliation": reconciliation,
    }
    (PACKET_DIR / "merchant_exact_product_issues_export_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
