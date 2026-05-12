#!/usr/bin/env python3
"""Fill synthetic UK delivery data to expose checkout shipping/tax precheck.

Stops before entering payment-card data or clicking Pay now.
"""

from __future__ import annotations

import base64
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import websocket


OUT = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-controlled-measurement-pinterest-build/measurement")


class Cdp:
    def __init__(self, ws_url: str) -> None:
        self.ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def call(self, method: str, params: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
        msg_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        start = time.time()
        while time.time() - start < timeout:
            event = json.loads(self.ws.recv())
            if event.get("id") == msg_id:
                return event
        raise TimeoutError(method)


def current_checkout_page() -> dict[str, Any]:
    pages = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=10))
    candidates = [
        p for p in pages
        if p.get("type") == "page" and (
            "dresslikemommy.com/checkouts" in p.get("url", "") or "shop.app/checkout" in p.get("url", "")
        )
    ]
    if not candidates:
        raise SystemExit("No checkout page found on CDP port 9222")
    return candidates[0]


def evaluate(cdp: Cdp, expr: str, timeout: int = 30) -> Any:
    res = cdp.call("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True}, timeout=timeout)
    return res.get("result", {}).get("result", {}).get("value")


def body_text(cdp: Cdp) -> str:
    value = evaluate(cdp, "document.body ? document.body.innerText : ''")
    return re.sub(r"\s+", " ", value or "").strip()


def screenshot(cdp: Cdp, path: Path) -> None:
    res = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, timeout=30)
    data = res.get("result", {}).get("data")
    if data:
        path.write_bytes(base64.b64decode(data))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    page = current_checkout_page()
    cdp = Cdp(page["webSocketDebuggerUrl"])
    try:
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        if "shop.app/checkout" in page.get("url", ""):
            # Return from Shop Pay login to merchant checkout if needed.
            evaluate(cdp, "history.back()")
            time.sleep(5)

        script = r"""
        (async () => {
          const set = (selector, value) => {
            const el = document.querySelector(selector);
            if (!el) return false;
            const setter = Object.getOwnPropertyDescriptor(el.__proto__, 'value')?.set;
            if (setter) setter.call(el, value); else el.value = value;
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
            el.dispatchEvent(new Event('blur', {bubbles:true}));
            return true;
          };
          const check = (selector, wanted) => {
            const el = document.querySelector(selector);
            if (!el) return false;
            el.checked = wanted;
            el.dispatchEvent(new Event('change', {bubbles:true}));
            return true;
          };
          const result = {
            email: set('input[name="email"]', 'measurement-test@dresslikemommy.com'),
            country: set('select[name="countryCode"]', 'GB'),
            firstName: set('input[name="firstName"]:not([id^="autofill"])', 'Measurement'),
            lastName: set('input[name="lastName"]:not([id^="autofill"])', 'Test'),
            address1: set('input[name="address1"]:not([id^="autofill"])', '10 Downing Street'),
            city: set('input[name="city"]:not([id^="autofill"])', 'London'),
            postalCode: set('input[name="postalCode"]:not([id^="autofill"])', 'SW1A 2AA'),
            phone: set('input[name="phone"]:not([id^="autofill"])', '02000000000'),
            marketingOff: check('input[name="marketing_opt_in"]', false),
            smsOff: check('input[name="sms_marketing_opt_in"]', false)
          };
          await new Promise(r => setTimeout(r, 6000));
          return result;
        })()
        """
        fill_result = evaluate(cdp, script, timeout=30)
        time.sleep(8)
        text = body_text(cdp)
        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "guardrail": "Synthetic checkout contact/address data only; no payment data entered; Pay now not clicked.",
            "synthetic_data_used": {
                "email": "measurement-test@dresslikemommy.com",
                "name": "Measurement Test",
                "country": "GB",
                "address_city_postcode": "10 Downing Street, London SW1A 2AA",
                "phone": "02000000000",
            },
            "fill_result": fill_result,
            "url": evaluate(cdp, "location.href"),
            "title": evaluate(cdp, "document.title"),
            "shipping_method_visible": bool(re.search(r"\b(Standard|Express|Shipping method|FREE|£|GBP)\b", text, re.I)),
            "pay_now_visible": "Pay now" in text,
            "payment_entered": False,
            "pay_now_clicked": False,
            "text_excerpt": text[:12000],
        }
        screenshot(cdp, OUT / "checkout_shipping_precheck_after_address.png")
        (OUT / "checkout_shipping_precheck_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2)[:8000])
    finally:
        cdp.close()


if __name__ == "__main__":
    main()
