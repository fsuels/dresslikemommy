#!/usr/bin/env python3
"""Read-only click-through probe for the GA4 purchase event row."""

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
DEFAULT_OUTPUT_DIR = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/ga4_ui_readonly_probe")
GA4_PURCHASE_ROW_URL = "https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?params=_r.explorerCard..selmet%3D%5B%22eventCount%22,%22totalRevenue%22%5D%26_r.explorerCard..seldim%3D%5B%22eventName%22%5D%26_r.explorerCard..startRow%3D10&r=top-events"


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


def find_or_open_ga4_page(cdp_port: int) -> dict[str, Any]:
    pages = get_json(f"http://127.0.0.1:{cdp_port}/json/list")
    for page in pages:
        if page.get("type") == "page" and "analytics.google.com/analytics/web" in page.get("url", ""):
            return page
    return open_page(cdp_port, GA4_PURCHASE_ROW_URL)


def evaluate(client: CdpClient, expression: str) -> Any:
    result = client.call("Runtime.evaluate", {
        "expression": expression,
        "awaitPromise": True,
        "returnByValue": True,
    }, timeout_seconds=30)
    return result.get("result", {}).get("result", {}).get("value")


def page_text(client: CdpClient) -> str:
    value = evaluate(client, "document.body ? document.body.innerText : ''")
    return re.sub(r"\s+", " ", value or "").strip()


def capture_screenshot(client: CdpClient, path: Path) -> None:
    result = client.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, timeout_seconds=30)
    data = result.get("result", {}).get("data")
    if data:
        path.write_bytes(base64.b64decode(data))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    page = find_or_open_ga4_page(args.cdp_port)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        client.call("Page.enable")
        client.call("Page.navigate", {"url": GA4_PURCHASE_ROW_URL})
        time.sleep(8)
        before_text = page_text(client)
        click_result = evaluate(client, """
(() => {
  const nodes = Array.from(document.querySelectorAll('*')).filter(el => (el.innerText || '').trim() === 'purchase');
  const target = nodes.find(el => el.offsetParent !== null) || nodes[0];
  if (!target) return {clicked:false, reason:'purchase node not found'};
  target.click();
  return {clicked:true, tag:target.tagName, text:(target.innerText || '').trim()};
})()
""")
        time.sleep(6)
        after_text = page_text(client)
        title = evaluate(client, "document.title")
        url = evaluate(client, "location.href")
        screenshot_path = args.output_dir / "ga4_purchase_detail_readonly_probe.png"
        capture_screenshot(client, screenshot_path)
        combined = f"{before_text}\n\n---AFTER_CLICK---\n\n{after_text}"
        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "GA4_PURCHASE_DETAIL_READONLY_PROBE",
            "url": url,
            "title": title,
            "click_result": click_result,
            "purchase_visible_before": "purchase" in before_text.lower(),
            "purchase_visible_after": "purchase" in after_text.lower(),
            "currency_visible": bool(re.search(r"\b(DKK|GBP|CHF|EUR|USD)\b", combined)),
            "transaction_visible": bool(re.search(r"transaction", combined, re.I)),
            "candidate_amount_visible": bool(re.search(r"\b(201|434|24|34)\b", combined)),
            "body_excerpt_before": before_text[:6000],
            "body_excerpt_after": after_text[:10000],
            "screenshot": str(screenshot_path.name),
            "guardrail": "Read-only GA4 purchase row click only; no Explore creation, settings edit, export, checkout, payment, order, or account write.",
        }
        (args.output_dir / "ga4_purchase_detail_readonly_probe_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2)[:5000])
    finally:
        client.close()


if __name__ == "__main__":
    main()
