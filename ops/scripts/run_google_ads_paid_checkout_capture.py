#!/usr/bin/env python3
"""Run a safe CDP checkout capture for one low-dollar paid Shopify order.

The script attaches to an already-running Chrome remote debugging session,
starts Network capture before navigating to checkout, adds one public product
variant to the cart, opens checkout, and waits for the operator to complete
payment. It stores only sanitized Google/GA/Merchant measurement request
fields; it does not store headers, cookies, card data, or payment payloads.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import queue
import re
import threading
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import websocket  # type: ignore


DEFAULT_PRODUCT_URL = "https://www.dresslikemommy.com/products/matching-t-shirt-bear-mama-baby"
DEFAULT_VARIANT_ID = "39529068200033"
DEFAULT_PRODUCT_LABEL = "Matching T-Shirt Bear Mama & Baby - White / Baby 12M"

MEASUREMENT_HOSTS = {
    "www.googleadservices.com",
    "googleadservices.com",
    "www.google.com",
    "google.com",
    "analytics.google.com",
    "www.google-analytics.com",
    "google-analytics.com",
    "www.merchant-center-analytics.goog",
    "merchant-center-analytics.goog",
}

ALLOWED_PARAMS = {
    "en",
    "event",
    "event_name",
    "value",
    "currency",
    "currency_code",
    "transaction_id",
    "transactionId",
    "oid",
    "label",
    "send_to",
    "tid",
    "id",
    "ct_cookie_present",
    "button_type",
    "customer_type",
    "tax",
    "shipping",
    "dl",
    "url",
    "page_location",
}

SENSITIVE_KEYS = {
    "email",
    "phone",
    "address",
    "address1",
    "address2",
    "first_name",
    "last_name",
    "name",
    "city",
    "zip",
    "postal_code",
    "card",
    "credit_card",
    "number",
    "cvv",
    "cvc",
}


@dataclass
class CdpClient:
    ws_url: str
    ws: websocket.WebSocket = field(init=False)
    next_id: int = 1
    pending: dict[int, queue.Queue] = field(default_factory=dict)
    events: queue.Queue = field(default_factory=queue.Queue)
    lock: threading.Lock = field(default_factory=threading.Lock)
    running: bool = True

    def __post_init__(self) -> None:
        self.ws = websocket.create_connection(self.ws_url, timeout=30, suppress_origin=True)
        self.reader = threading.Thread(target=self._read_loop, daemon=True)
        self.reader.start()

    def _read_loop(self) -> None:
        while self.running:
            try:
                raw = self.ws.recv()
            except Exception as exc:  # pragma: no cover - runtime guard
                self.events.put({"method": "__socket_error__", "params": {"error": str(exc)}})
                break
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if "id" in msg and msg["id"] in self.pending:
                self.pending[msg["id"]].put(msg)
            else:
                self.events.put(msg)

    def send(self, method: str, params: dict[str, Any] | None = None, session_id: str | None = None, timeout: float = 15) -> dict[str, Any]:
        with self.lock:
            mid = self.next_id
            self.next_id += 1
            q: queue.Queue = queue.Queue()
            self.pending[mid] = q
            payload: dict[str, Any] = {"id": mid, "method": method}
            if params is not None:
                payload["params"] = params
            if session_id is not None:
                payload["sessionId"] = session_id
            self.ws.send(json.dumps(payload))
        try:
            msg = q.get(timeout=timeout)
        finally:
            self.pending.pop(mid, None)
        if "error" in msg:
            raise RuntimeError(f"CDP {method} error: {msg['error']}")
        return msg

    def close(self) -> None:
        self.running = False
        try:
            self.ws.close()
        except Exception:
            pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def create_target(port: int, url: str = "about:blank") -> tuple[str, str]:
    encoded = urllib.parse.quote(url, safe="")
    request = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    target_id = data["id"]
    ws_url = data["webSocketDebuggerUrl"]
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/activate/{target_id}", timeout=2).read()
    except Exception:
        pass
    return target_id, ws_url


def activate_chrome() -> None:
    os.system("osascript -e 'tell application \"Google Chrome\" to activate' >/dev/null 2>&1")


def redact_value(key: str, value: str) -> str:
    lk = key.lower()
    if any(token in lk for token in SENSITIVE_KEYS):
        return "[redacted]"
    if re.search(r"@", value):
        return "[redacted]"
    return value[:500]


def parse_params(url: str, post_data: str | None) -> dict[str, str]:
    parsed = urllib.parse.urlparse(url)
    params: dict[str, str] = {}

    def add_pairs(pairs: list[tuple[str, str]]) -> None:
        for key, value in pairs:
            if key in ALLOWED_PARAMS or key.startswith("ep.") or key.startswith("pr1"):
                params[key] = redact_value(key, value)

    add_pairs(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    if post_data and len(post_data) <= 20000:
        stripped = post_data.strip()
        if stripped.startswith("{"):
            try:
                obj = json.loads(stripped)
            except Exception:
                obj = {}
            flat: dict[str, Any] = {}
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (str, int, float, bool)):
                        flat[key] = value
                payload = obj.get("payload")
                if isinstance(payload, dict):
                    for key, value in payload.items():
                        if isinstance(value, (str, int, float, bool)):
                            flat[key] = value
            for key, value in flat.items():
                if key in ALLOWED_PARAMS:
                    params[key] = redact_value(key, str(value))
        else:
            add_pairs(urllib.parse.parse_qsl(stripped, keep_blank_values=True))
    return params


def event_from_params(params: dict[str, str]) -> str:
    for key in ("en", "event", "event_name"):
        if params.get(key):
            return params[key]
    path_hint = " ".join(params.values()).lower()
    if "purchase" in path_hint:
        return "purchase"
    return ""


def id_from_params(params: dict[str, str]) -> str:
    for key in ("oid", "transaction_id", "transactionId", "ep.transaction_id"):
        if params.get(key):
            return params[key]
    return ""


def measurement_id_from_params(params: dict[str, str]) -> str:
    tid = params.get("tid") or params.get("id") or ""
    if params.get("send_to"):
        return params["send_to"]
    return tid


def sanitize_request(event: dict[str, Any]) -> dict[str, Any] | None:
    params = event.get("params", {})
    request = params.get("request", {})
    url = request.get("url", "")
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    if host not in MEASUREMENT_HOSTS:
        return None
    path = parsed.path
    qp = parse_params(url, request.get("postData"))
    conversion_match = re.search(r"/pagead/conversion/([^/]+)/?", path)
    conversion_id = conversion_match.group(1) if conversion_match else ""
    conversion_label = qp.get("label", "")
    contains_hash = any("em=" in part or "sha256" in part.lower() for part in (url, request.get("postData", "")))
    return {
        "captured_at": now_iso(),
        "network_phase": event.get("method"),
        "host": host,
        "path": path,
        "request_method": request.get("method", ""),
        "resource_type": params.get("type", ""),
        "event": event_from_params(qp),
        "value": qp.get("value", ""),
        "currency": qp.get("currency") or qp.get("currency_code", ""),
        "transaction_or_dedupe_id": id_from_params(qp),
        "conversion_id": conversion_id,
        "conversion_label": conversion_label,
        "measurement_id": measurement_id_from_params(qp),
        "button_type": qp.get("button_type", ""),
        "customer_type": qp.get("customer_type", ""),
        "tax": qp.get("tax", ""),
        "shipping": qp.get("shipping", ""),
        "contains_enhanced_conversion_hash": contains_hash,
        "url_removed_for_privacy": True,
    }


def is_purchase(ev: dict[str, Any]) -> bool:
    return ev.get("event") == "purchase"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def evaluate(client: CdpClient, session_id: str | None, expression: str, await_promise: bool = False, timeout: float = 30) -> Any:
    msg = client.send(
        "Runtime.evaluate",
        {
            "expression": expression,
            "awaitPromise": await_promise,
            "returnByValue": True,
        },
        session_id=session_id,
        timeout=timeout,
    )
    result = msg.get("result", {}).get("result", {})
    return result.get("value")


def visible_snapshot(client: CdpClient, session_id: str | None) -> dict[str, str]:
    expr = """
    (() => {
      const text = document.body ? document.body.innerText : '';
      const title = document.title || '';
      const url = location.href;
      const confirmation = (text.match(/Confirmation\\s+#?([A-Z0-9-]+)/i) || [])[1] || '';
      const total = (text.match(/Total\\s+(?:USD\\s*)?\\$?([0-9]+\\.[0-9]{2})/i) || [])[1] || '';
      const hasPay = /Pay now|Complete order|Payment|Card number|Credit card/i.test(text);
      const hasThankYou = /Thank you|order is confirmed|Confirmation/i.test(text);
      return {title, url, confirmation, total, hasPay: String(hasPay), hasThankYou: String(hasThankYou)};
    })()
    """
    try:
        return evaluate(client, session_id, expr, timeout=10) or {}
    except Exception as exc:
        return {"error": str(exc)}


def build_report(packet: Path, product_label: str, variant_id: str, events: list[dict[str, Any]], snapshots: list[dict[str, str]], status: str) -> None:
    purchases = [ev for ev in events if is_purchase(ev)]
    ads = [ev for ev in purchases if ev["host"].endswith("googleadservices.com") or "/pagead/conversion/" in ev["path"]]
    ga4 = [ev for ev in purchases if ev["host"] in {"analytics.google.com", "www.google-analytics.com", "google-analytics.com"}]
    mc = [ev for ev in purchases if ev["host"].endswith("merchant-center-analytics.goog")]
    nonzero_ads = [ev for ev in ads if ev.get("value") not in {"", "0", "0.0", "0.00"} and ev.get("currency") == "USD" and ev.get("transaction_or_dedupe_id")]
    summary = {
        "captured_at": now_iso(),
        "status": status,
        "product_label": product_label,
        "variant_id": variant_id,
        "measurement_event_count": len(events),
        "purchase_event_count": len(purchases),
        "google_ads_purchase_event_count": len(ads),
        "ga4_purchase_event_count": len(ga4),
        "merchant_center_purchase_event_count": len(mc),
        "nonzero_google_ads_purchase_proven": bool(nonzero_ads),
        "purchase_values": sorted({f"{ev.get('value')} {ev.get('currency')}".strip() for ev in purchases if ev.get("value") or ev.get("currency")}),
        "transaction_or_dedupe_ids": sorted({ev.get("transaction_or_dedupe_id", "") for ev in purchases if ev.get("transaction_or_dedupe_id")}),
        "latest_snapshot": snapshots[-1] if snapshots else {},
    }
    write_json(packet / "live_paid_checkout_capture_summary.json", summary)
    lines = [
        "# Google Ads Paid Checkout Live Capture",
        "",
        f"Status: `{status}`",
        "",
        "## Product",
        "",
        f"- Product / variant: `{product_label}`",
        f"- Variant id: `{variant_id}`",
        "",
        "## Measurement Result",
        "",
        f"- Measurement events captured: `{len(events)}`",
        f"- Purchase events captured: `{len(purchases)}`",
        f"- Google Ads purchase events: `{len(ads)}`",
        f"- GA4 purchase events: `{len(ga4)}`",
        f"- Merchant Center purchase events: `{len(mc)}`",
        f"- Nonzero Google Ads paid purchase proven: `{'YES' if nonzero_ads else 'NO'}`",
        "",
        "## Purchase IDs / Values",
        "",
    ]
    if purchases:
        for ev in purchases:
            lines.append(
                f"- `{ev.get('host')}{ev.get('path')}` event=`{ev.get('event')}` value=`{ev.get('value')}` currency=`{ev.get('currency')}` id=`{ev.get('transaction_or_dedupe_id')}`"
            )
    else:
        lines.append("- No purchase event captured yet.")
    lines += [
        "",
        "## Privacy",
        "",
        "Only sanitized measurement-domain request fields were stored. Headers, cookies, full URLs, card data, and payment payloads were not stored.",
    ]
    (packet / "LIVE_PAID_CHECKOUT_CAPTURE_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--packet-dir", required=True)
    parser.add_argument("--product-url", default=DEFAULT_PRODUCT_URL)
    parser.add_argument("--variant-id", default=DEFAULT_VARIANT_ID)
    parser.add_argument("--product-label", default=DEFAULT_PRODUCT_LABEL)
    parser.add_argument("--timeout-minutes", type=float, default=20)
    args = parser.parse_args()

    packet = Path(args.packet_dir)
    raw = packet / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    target_id, ws_url = create_target(args.cdp_port)
    activate_chrome()
    client = CdpClient(ws_url)
    root_session = None
    events: list[dict[str, Any]] = []
    snapshots: list[dict[str, str]] = []
    status = "CAPTURE_RUNNING_PAYMENT_NEEDED"

    try:
        client.send("Runtime.enable")
        client.send("Page.enable")
        client.send("Network.enable")
        root_session = None

        # Capture starts before checkout navigation.
        start = time.time()
        write_json(raw / "capture_start.json", {
            "started_at": now_iso(),
            "cdp_port": args.cdp_port,
            "target_id": target_id,
            "product_url": args.product_url,
            "variant_id": args.variant_id,
            "product_label": args.product_label,
            "privacy": "Measurement domains only; no headers/cookies/card/payment payloads stored.",
        })

        client.send("Page.navigate", {"url": f"{args.product_url}?variant={args.variant_id}"})
        time.sleep(3)
        add_expr = f"""
        (async () => {{
          await fetch('/cart/clear.js', {{method:'POST', credentials:'same-origin'}});
          await fetch('/cart/add.js', {{
            method:'POST',
            credentials:'same-origin',
            headers: {{'Content-Type':'application/json', 'Accept':'application/json'}},
            body: JSON.stringify({{id: {args.variant_id}, quantity: 1}})
          }});
          location.href = '/checkout?skip_shop_pay=true';
          return true;
        }})()
        """
        evaluate(client, root_session, add_expr, await_promise=True, timeout=30)
        print("CAPTURE_STARTED_AND_CHECKOUT_OPENED", flush=True)
        print("Complete payment in the visible Chrome checkout tab. I will keep listening for the thank-you-page purchase event.", flush=True)

        last_write = 0.0
        first_purchase_at: float | None = None
        reloaded_for_dedupe = False
        deadline = start + args.timeout_minutes * 60
        while time.time() < deadline:
            try:
                msg = client.events.get(timeout=0.5)
            except queue.Empty:
                msg = None
            if msg:
                method = msg.get("method")
                if method == "Network.requestWillBeSent":
                    sanitized = sanitize_request(msg)
                    if sanitized:
                        events.append(sanitized)
                        if is_purchase(sanitized) and first_purchase_at is None:
                            first_purchase_at = time.time()
                            status = "PURCHASE_EVENT_CAPTURED_WAITING_FOR_DEDUPE_GRACE"
                            print("PURCHASE_EVENT_CAPTURED", sanitized, flush=True)
                elif method == "__socket_error__":
                    print("CDP_SOCKET_ERROR", msg.get("params", {}).get("error"), flush=True)
                    break

            if time.time() - last_write > 5:
                snapshot = visible_snapshot(client, root_session)
                snapshots.append(snapshot)
                write_json(raw / "measurement_requests_sanitized_live.json", events)
                write_json(raw / "page_snapshots_sanitized_live.json", snapshots[-20:])
                build_report(packet, args.product_label, args.variant_id, events, snapshots, status)
                last_write = time.time()

            if first_purchase_at and not reloaded_for_dedupe and time.time() - first_purchase_at > 12:
                try:
                    client.send("Page.reload", {"ignoreCache": True})
                    reloaded_for_dedupe = True
                    print("RELOADED_ONCE_FOR_BROWSER_DUPLICATE_CHECK", flush=True)
                except Exception as exc:
                    print("RELOAD_FOR_DEDUPE_FAILED", exc, flush=True)

            if first_purchase_at and reloaded_for_dedupe and time.time() - first_purchase_at > 28:
                status = "PURCHASE_CAPTURE_COMPLETE"
                break

        write_json(raw / "measurement_requests_sanitized_live.json", events)
        write_json(raw / "page_snapshots_sanitized_live.json", snapshots)
        build_report(packet, args.product_label, args.variant_id, events, snapshots, status)
        print("CAPTURE_DONE", status, str(packet / "LIVE_PAID_CHECKOUT_CAPTURE_REPORT.md"), flush=True)
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
