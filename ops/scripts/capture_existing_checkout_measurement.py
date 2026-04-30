#!/usr/bin/env python3
"""Attach to an already-open Shopify checkout and capture purchase measurement.

This is used when the operator is already on the payment page. It does not
navigate, add products, or submit payment. It polls Chrome DevTools targets,
attaches to checkout/web-pixel page and iframe targets, and records only
sanitized Google/GA/Merchant measurement requests.
"""

from __future__ import annotations

import argparse
import base64
import json
import queue
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from run_google_ads_paid_checkout_capture import (
    CdpClient,
    build_report,
    is_purchase,
    sanitize_request,
    visible_snapshot,
    write_json,
)


CHECKOUT_NEEDLES = (
    "dresslikemommy.com/checkouts",
    "dresslikemommy.com/web-pixels",
    "account.dresslikemommy.com/web-pixels",
    "checkout.shopify.com",
)


def list_targets(port: int) -> list[dict[str, Any]]:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def activate_target(port: int, target_id: str) -> None:
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/activate/{target_id}", timeout=2).read()
    except Exception:
        pass


def is_relevant(target: dict[str, Any]) -> bool:
    if target.get("type") not in {"page", "iframe"}:
        return False
    url = target.get("url", "")
    return any(needle in url for needle in CHECKOUT_NEEDLES)


def capture_png(client: CdpClient, out: Path) -> bool:
    try:
        client.send("Page.bringToFront", timeout=5)
        msg = client.send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False}, timeout=10)
        data = msg.get("result", {}).get("data")
        if not data:
            return False
        out.write_bytes(base64.b64decode(data))
        return True
    except Exception:
        return False


def attach_target(target: dict[str, Any]) -> CdpClient | None:
    ws_url = target.get("webSocketDebuggerUrl")
    if not ws_url:
        return None
    try:
        client = CdpClient(ws_url)
        for method in ("Page.enable", "Runtime.enable", "Network.enable"):
            try:
                client.send(method, timeout=5)
            except Exception:
                pass
        return client
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--packet-dir", required=True)
    parser.add_argument("--timeout-minutes", type=float, default=25)
    parser.add_argument("--product-label", default="Existing live checkout")
    parser.add_argument("--variant-id", default="")
    args = parser.parse_args()

    packet = Path(args.packet_dir)
    raw = packet / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    clients: dict[str, CdpClient] = {}
    events: list[dict[str, Any]] = []
    snapshots: list[dict[str, str]] = []
    status = "CAPTURE_RUNNING_PAYMENT_NEEDED"
    checkout_target_id = ""
    screenshot_path = packet / "checkout_payment_page_screenshot.png"

    start = time.time()
    deadline = start + args.timeout_minutes * 60
    first_purchase_at: float | None = None
    last_poll = 0.0
    last_write = 0.0

    try:
        while time.time() < deadline:
            if time.time() - last_poll > 1:
                for target in list_targets(args.cdp_port):
                    if not is_relevant(target) or target["id"] in clients:
                        continue
                    client = attach_target(target)
                    if not client:
                        continue
                    clients[target["id"]] = client
                    if target.get("type") == "page" and "dresslikemommy.com/checkouts" in target.get("url", ""):
                        checkout_target_id = target["id"]
                        activate_target(args.cdp_port, checkout_target_id)
                        capture_png(client, screenshot_path)
                        print(f"CHECKOUT_SCREENSHOT {screenshot_path}", flush=True)
                last_poll = time.time()

            for target_id, client in list(clients.items()):
                while True:
                    try:
                        msg = client.events.get_nowait()
                    except queue.Empty:
                        break
                    if msg.get("method") == "Network.requestWillBeSent":
                        sanitized = sanitize_request(msg)
                        if sanitized:
                            sanitized["target_id"] = target_id
                            events.append(sanitized)
                            if is_purchase(sanitized) and first_purchase_at is None:
                                first_purchase_at = time.time()
                                status = "PURCHASE_EVENT_CAPTURED_WAITING_FOR_GRACE"
                                print("PURCHASE_EVENT_CAPTURED", sanitized, flush=True)

            if time.time() - last_write > 5:
                if checkout_target_id in clients:
                    snapshots.append(visible_snapshot(clients[checkout_target_id], None))
                    capture_png(clients[checkout_target_id], screenshot_path)
                write_json(raw / "measurement_requests_sanitized_live.json", events)
                write_json(raw / "page_snapshots_sanitized_live.json", snapshots[-20:])
                write_json(raw / "attached_targets.json", [
                    {"id": tid, "attached": True} for tid in sorted(clients)
                ])
                build_report(packet, args.product_label, args.variant_id, events, snapshots, status)
                last_write = time.time()

            if first_purchase_at and time.time() - first_purchase_at > 20:
                status = "PURCHASE_CAPTURE_COMPLETE"
                break

            time.sleep(0.2)

        write_json(raw / "measurement_requests_sanitized_live.json", events)
        write_json(raw / "page_snapshots_sanitized_live.json", snapshots)
        build_report(packet, args.product_label, args.variant_id, events, snapshots, status)
        print("CAPTURE_DONE", status, str(packet / "LIVE_PAID_CHECKOUT_CAPTURE_REPORT.md"), flush=True)
    finally:
        for client in clients.values():
            client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
