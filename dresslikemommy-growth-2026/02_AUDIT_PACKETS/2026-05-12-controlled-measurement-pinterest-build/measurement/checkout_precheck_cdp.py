#!/usr/bin/env python3
"""Controlled checkout precheck via existing Chrome CDP.

This intentionally stops before typing customer/address/payment data or
submitting payment. It only creates a storefront cart from a cart permalink,
opens checkout if available, and captures the visible state needed for the
owner-approved measurement-test precheck.
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


DEFAULT_OUTPUT_DIR = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-controlled-measurement-pinterest-build/measurement")
DEFAULT_URL = "https://www.dresslikemommy.com/cart/41497061916769:1?country=GB"


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
        raise TimeoutError(f"Timed out waiting for {method}")


def open_page(cdp_port: int, url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    req = urllib.request.Request(f"http://127.0.0.1:{cdp_port}/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def evaluate(client: CdpClient, expression: str, timeout: int = 30) -> Any:
    result = client.call(
        "Runtime.evaluate",
        {"expression": expression, "awaitPromise": True, "returnByValue": True},
        timeout_seconds=timeout,
    )
    return result.get("result", {}).get("result", {}).get("value")


def text(client: CdpClient) -> str:
    value = evaluate(client, "document.body ? document.body.innerText : ''")
    return re.sub(r"\s+", " ", value or "").strip()


def screenshot(client: CdpClient, path: Path) -> None:
    result = client.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, timeout_seconds=30)
    data = result.get("result", {}).get("data")
    if data:
        path.write_bytes(base64.b64decode(data))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    page = open_page(args.cdp_port, args.url)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        client.call("Page.enable")
        client.call("Runtime.enable")
        time.sleep(5)
        before = {
            "url": evaluate(client, "location.href"),
            "title": evaluate(client, "document.title"),
            "text": text(client)[:6000],
        }
        screenshot(client, args.output_dir / "checkout_precheck_cart.png")

        clicked = evaluate(
            client,
            """
            (() => {
              const candidates = [
                'button[name="checkout"]',
                'input[name="checkout"]',
                'a[href*="/checkout"]',
                'button:has-text("Checkout")'
              ];
              for (const selector of candidates.slice(0, 3)) {
                const el = document.querySelector(selector);
                if (el) { el.click(); return selector; }
              }
              const all = [...document.querySelectorAll('button,a,input[type="submit"]')];
              const hit = all.find(el => /checkout|check out/i.test(el.innerText || el.value || el.getAttribute('aria-label') || ''));
              if (hit) { hit.click(); return 'text-match'; }
              return null;
            })()
            """,
        )
        time.sleep(10)
        after = {
            "clicked_checkout_selector": clicked,
            "url": evaluate(client, "location.href"),
            "title": evaluate(client, "document.title"),
            "text": text(client)[:10000],
            "guardrail": "Stopped before entering customer/address/payment data or submitting payment.",
        }
        screenshot(client, args.output_dir / "checkout_precheck_after_checkout_click.png")

        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "input_url": args.url,
            "candidate": {
                "country": "GB",
                "currency_target": "GBP",
                "variant_id": "41497061916769",
                "product_handle": "chic-pink-mermaid-scales-tankini-set-for-mother-and-daughter",
                "variant_title": "Child 2-3 years / Multi-Color",
                "base_price_usd": 14.99,
            },
            "before_checkout_click": before,
            "after_checkout_click": after,
        }
        out = args.output_dir / "checkout_precheck_summary.json"
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2)[:6000])
    finally:
        client.close()


if __name__ == "__main__":
    main()
