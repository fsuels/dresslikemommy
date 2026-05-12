#!/usr/bin/env python3
"""Read-only GA4 report URL probe for event-level purchase dimensions.

This uses the existing logged-in Chrome DevTools session and navigates to GA4
report URLs only. It does not create or save an Exploration, edit settings,
export data, touch checkout, submit payment, or create an order.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import websocket


DEFAULT_CDP_PORT = 9222
DEFAULT_OUTPUT_DIR = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-measurement-safe-lanes/ga4_readonly_probe")


URLS = {
    "events_purchase_with_event_dims": (
        "https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?"
        "params=_r.explorerCard..selmet%3D%5B%22eventCount%22%2C%22totalRevenue%22%5D"
        "%26_r.explorerCard..seldim%3D%5B%22eventName%22%2C%22dateHourMinute%22%2C%22country%22%2C%22currency%22%2C%22transactionId%22%5D"
        "%26_r.explorerCard..startRow%3D0&r=top-events"
    ),
    "monetization_purchases_purchase_event": (
        "https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?"
        "params=_r.explorerCard..selmet%3D%5B%22ecommercePurchases%22%2C%22purchaseRevenue%22%2C%22totalRevenue%22%5D"
        "%26_r.explorerCard..seldim%3D%5B%22transactionId%22%2C%22dateHourMinute%22%2C%22country%22%2C%22currency%22%5D"
        "&r=ecommerce-purchases"
    ),
    "transaction_id_report_direct": (
        "https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?"
        "params=_r.explorerCard..selmet%3D%5B%22purchaseRevenue%22%2C%22totalRevenue%22%2C%22eventCount%22%5D"
        "%26_r.explorerCard..seldim%3D%5B%22transactionId%22%2C%22eventName%22%2C%22dateHourMinute%22%2C%22country%22%2C%22currency%22%5D"
        "&r=transaction-id-report"
    ),
}

CANDIDATE_PATTERNS = [
    r"\bDKK\b",
    r"\bGBP\b",
    r"\bCHF\b",
    r"\b201(?:\.0|\.00)?\b",
    r"\b434(?:\.0|\.00)?\b",
    r"\b259(?:\.0|\.00)?\b",
    r"\b427(?:\.0|\.00)?\b",
    r"\b24(?:\.0|\.00)?\b",
    r"\b34(?:\.0|\.00)?\b",
]


class CdpClient:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(websocket_url, timeout=30, suppress_origin=True)
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def call(self, method: str, params: dict[str, Any] | None = None, timeout_seconds: int = 30) -> dict[str, Any]:
        message_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        start = time.time()
        while time.time() - start < timeout_seconds:
            event = json.loads(self.ws.recv())
            if event.get("id") == message_id:
                return event
        raise TimeoutError(f"Timed out waiting for CDP response {message_id} ({method})")


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def open_page(cdp_port: int, url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    request = urllib.request.Request(f"http://127.0.0.1:{cdp_port}/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def find_or_open_ga4_page(cdp_port: int, url: str) -> dict[str, Any]:
    pages = get_json(f"http://127.0.0.1:{cdp_port}/json/list")
    for page in pages:
        if page.get("type") == "page" and "analytics.google.com/analytics/web" in page.get("url", ""):
            return page
    return open_page(cdp_port, url)


def evaluate(client: CdpClient, expression: str, timeout: int = 30) -> Any:
    result = client.call(
        "Runtime.evaluate",
        {"expression": expression, "awaitPromise": True, "returnByValue": True},
        timeout_seconds=timeout,
    )
    return result.get("result", {}).get("result", {}).get("value")


def page_text(client: CdpClient) -> str:
    value = evaluate(client, "document.body ? document.body.innerText : ''")
    return re.sub(r"\s+", " ", value or "").strip()


def capture_screenshot(client: CdpClient, path: Path) -> None:
    result = client.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, timeout_seconds=30)
    data = result.get("result", {}).get("data")
    if data:
        path.write_bytes(base64.b64decode(data))


def probe_url(cdp_port: int, name: str, url: str, output_dir: Path) -> dict[str, Any]:
    page = find_or_open_ga4_page(cdp_port, url)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        client.call("Page.enable")
        client.call("Page.navigate", {"url": url})
        time.sleep(12)
        text = page_text(client)
        location = evaluate(client, "location.href")
        title = evaluate(client, "document.title")
        screenshot = output_dir / f"{name}.png"
        capture_screenshot(client, screenshot)
        return {
            "name": name,
            "url_after_load": location,
            "title": title,
            "purchase_visible": "purchase" in text.lower(),
            "transaction_visible": bool(re.search(r"transaction", text, re.I)),
            "currency_visible": bool(re.search(r"\b(DKK|GBP|CHF|EUR|USD|currency)\b", text, re.I)),
            "candidate_pattern_hits": [pattern for pattern in CANDIDATE_PATTERNS if re.search(pattern, text)],
            "body_excerpt": text[:10000],
            "screenshot": screenshot.name,
        }
    finally:
        client.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results = [probe_url(args.cdp_port, name, url, args.output_dir) for name, url in URLS.items()]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "GA4_EVENT_LEVEL_DIMENSION_READONLY_URL_PROBE",
        "guardrail": "Read-only GA4 report URL navigation via existing Chrome CDP; no Explore save/create, settings edit, export, checkout, payment, order, refund, cancelation, or account write.",
        "results": results,
    }
    path = args.output_dir / "ga4_event_level_dimension_probe_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2)[:6000])


if __name__ == "__main__":
    main()
