#!/usr/bin/env python3
"""Read-only Chrome DevTools helper for Google Ads evidence captures.

This script opens/uses a Chrome remote-debugging tab and records DOM text,
metadata, screenshots, and optional UI probes. It does not click Google Ads
Save/Apply controls for campaign/account settings.
"""

from __future__ import annotations

import base64
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


PORT = 9222
BASE = f"http://127.0.0.1:{PORT}"
OUT = Path(__file__).resolve().parent / "raw"
CAMPAIGN_URL = (
    "https://ads.google.com/aw/campaigns"
    "?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493"
    "&__c=9710510557&authuser=0&campaignId=23802638621"
)
ROUTES = {
    "campaigns": "https://ads.google.com/aw/campaigns",
    "productgroups": "https://ads.google.com/aw/productgroups",
    "products": "https://ads.google.com/aw/products",
    "searchterms": "https://ads.google.com/aw/keywords/searchterms",
}


def route_url(route: str) -> str:
    base = ROUTES.get(route, ROUTES["campaigns"])
    return (
        f"{base}?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493"
        "&__c=9710510557&authuser=0&campaignId=23802638621"
    )


class CDP:
    def __init__(self, ws_url: str) -> None:
        self.ws = websocket.create_connection(ws_url, timeout=20, suppress_origin=True)
        self.next_id = 1

    def call(self, method: str, params: dict | None = None, timeout: float = 20) -> dict:
        msg_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            raw = self.ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise RuntimeError(f"{method} failed: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(f"Timed out waiting for {method}")

    def close(self) -> None:
        self.ws.close()


def http_json(path: str, method: str = "GET") -> dict | list:
    req = urllib.request.Request(BASE + path, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def new_tab(url: str) -> dict:
    quoted = urllib.parse.quote(url, safe="")
    return http_json(f"/json/new?{quoted}", method="PUT")  # type: ignore[return-value]


def close_tab(target_id: str) -> None:
    try:
        http_json(f"/json/close/{target_id}")
    except Exception:
        pass


def wait_for_loaded(cdp: CDP, seconds: float = 18) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        state = cdp.call(
            "Runtime.evaluate",
            {"expression": "document.readyState", "returnByValue": True},
            timeout=5,
        )
        if state.get("result", {}).get("value") == "complete":
            time.sleep(4)
            return
        time.sleep(0.5)
    time.sleep(4)


def eval_json(cdp: CDP, expression: str, timeout: float = 20) -> object:
    result = cdp.call(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
        timeout=timeout,
    )
    return result.get("result", {}).get("value")


def capture(cdp: CDP, prefix: str) -> dict:
    meta_expr = r"""
(() => {
  const text = document.body ? document.body.innerText : "";
  const controls = Array.from(document.querySelectorAll('button,[role="button"],a,input,[aria-label]'))
    .slice(0, 500)
    .map((el, i) => ({
      i,
      tag: el.tagName,
      role: el.getAttribute('role') || '',
      type: el.getAttribute('type') || '',
      text: (el.innerText || el.value || el.getAttribute('aria-label') || el.title || '').trim().slice(0, 160),
      aria: (el.getAttribute('aria-label') || '').slice(0, 160),
      title: (el.title || '').slice(0, 160),
      disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true',
      rect: (() => {
        const r = el.getBoundingClientRect();
        return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
      })(),
    }))
    .filter(x => x.text || x.aria || x.title);
  return {
    title: document.title,
    url: location.href,
    timestamp: new Date().toISOString(),
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    bodyTextLength: text.length,
    bodyText: text,
    controls,
  };
})()
"""
    data = eval_json(cdp, meta_expr)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{prefix}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    text = data.get("bodyText", "") if isinstance(data, dict) else ""
    (OUT / f"{prefix}.txt").write_text(text, encoding="utf-8")
    shot = cdp.call(
        "Page.captureScreenshot",
        {"format": "png", "captureBeyondViewport": False},
        timeout=20,
    )
    if "data" in shot:
        (OUT / f"{prefix}.png").write_bytes(base64.b64decode(shot["data"]))
    return data if isinstance(data, dict) else {}


def click_by_text(cdp: CDP, patterns: list[str]) -> bool:
    expr = json.dumps(patterns)
    script = f"""
(() => {{
  const patterns = {expr}.map(s => s.toLowerCase());
  const els = Array.from(document.querySelectorAll('button,[role="button"],a,input,[aria-label]'));
  for (const el of els) {{
    const label = ((el.innerText || el.value || el.getAttribute('aria-label') || el.title || '') + '').trim();
    const lower = label.toLowerCase();
    if (!label || el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    if (patterns.some(p => lower.includes(p))) {{
      el.scrollIntoView({{block: 'center', inline: 'center'}});
      el.click();
      return {{clicked: true, label}};
    }}
  }}
  return {{clicked: false}};
}})()
"""
    result = eval_json(cdp, script)
    print(json.dumps({"click_by_text": patterns, "result": result}, ensure_ascii=False))
    return bool(isinstance(result, dict) and result.get("clicked"))


def fill_visible_dates(cdp: CDP, start: str, end: str) -> object:
    script = f"""
(() => {{
  const start = {json.dumps(start)};
  const end = {json.dumps(end)};
  const dialogs = Array.from(document.querySelectorAll('[role="dialog"]'));
  const dialog = dialogs.find(el => {{
    const label = (el.getAttribute('aria-label') || '') + ' ' + (el.innerText || '');
    return label.includes('日期范围选择器') || label.toLowerCase().includes('date range');
  }});
  const root = dialog || document;
  const inputs = Array.from(root.querySelectorAll('input')).filter(el => {{
    const r = el.getBoundingClientRect();
    return r.width > 20 && r.height > 10 && !el.disabled && el.type !== 'hidden';
  }});
  const before = inputs.map((el, i) => ({{i, value: el.value, aria: el.getAttribute('aria-label') || '', placeholder: el.getAttribute('placeholder') || ''}}));
  const dateInputs = inputs.filter(el => /[年/]/.test(el.value || '')).slice(-2);
  if (dateInputs.length >= 2) {{
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    dateInputs[0].focus();
    nativeInputValueSetter.call(dateInputs[0], start);
    dateInputs[0].dispatchEvent(new Event('input', {{bubbles: true}}));
    dateInputs[0].dispatchEvent(new Event('change', {{bubbles: true}}));
    dateInputs[1].focus();
    nativeInputValueSetter.call(dateInputs[1], end);
    dateInputs[1].dispatchEvent(new Event('input', {{bubbles: true}}));
    dateInputs[1].dispatchEvent(new Event('change', {{bubbles: true}}));
  }}
  const after = inputs.map((el, i) => ({{i, value: el.value, aria: el.getAttribute('aria-label') || '', placeholder: el.getAttribute('placeholder') || ''}}));
  return {{count: inputs.length, dateInputCount: dateInputs.length, before, after}};
}})()
"""
    return eval_json(cdp, script)


def click_date_picker_apply(cdp: CDP) -> object:
    script = r"""
(() => {
  const dialogs = Array.from(document.querySelectorAll('[role="dialog"]'));
  const dialog = dialogs.find(el => {
    const label = (el.getAttribute('aria-label') || '') + ' ' + (el.innerText || '');
    return label.includes('日期范围选择器') || label.toLowerCase().includes('date range');
  });
  if (!dialog) return {clicked: false, reason: 'date picker dialog not found'};
  const buttons = Array.from(dialog.querySelectorAll('button,[role="button"],material-button'));
  const apply = buttons.find(el => {
    const label = ((el.innerText || el.getAttribute('aria-label') || el.title || '') + '').trim();
    return label === '应用' || label.toLowerCase() === 'apply';
  });
  if (!apply) {
    return {
      clicked: false,
      reason: 'date picker apply not found',
      buttons: buttons.map(el => ((el.innerText || el.getAttribute('aria-label') || el.title || '') + '').trim()).filter(Boolean)
    };
  }
  apply.click();
  return {clicked: true, label: ((apply.innerText || apply.getAttribute('aria-label') || apply.title || '') + '').trim()};
})()
"""
    return eval_json(cdp, script)


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "capture"
    route = sys.argv[2] if len(sys.argv) > 2 else "campaigns"
    target = new_tab(route_url(route))
    target_id = target["id"]
    cdp = CDP(target["webSocketDebuggerUrl"])
    try:
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Page.bringToFront")
        wait_for_loaded(cdp)
        initial_prefix = f"01_{route}_initial" if route != "campaigns" else "01_campaign_initial"
        capture(cdp, initial_prefix)

        if mode in {"open-date", "custom-date"}:
            opened = click_by_text(
                cdp,
                [
                    "All time",
                    "2017年5月4日",
                    "2026年5月9日",
                    "May 4, 2017",
                    "Date range",
                ],
            )
            time.sleep(2)
            stage_prefix = "" if route == "campaigns" else f"{route}_"
            capture(cdp, f"02_{stage_prefix}after_date_control_click")
            if mode == "open-date":
                print(json.dumps({"opened_date_control": opened}, ensure_ascii=False))
                return 0
            if opened:
                custom_clicked = click_by_text(cdp, ["Custom", "自定义", "Custom range"])
                time.sleep(1)
                capture(cdp, f"03_{stage_prefix}after_custom_click")
                fill_result = fill_visible_dates(cdp, "2026年5月6日", "2026年5月9日")
                print(json.dumps({"fill_visible_dates": fill_result}, ensure_ascii=False))
                capture(cdp, f"04_{stage_prefix}after_fill_dates")
                applied = click_date_picker_apply(cdp)
                time.sleep(6)
                capture(cdp, f"05_{stage_prefix}after_readonly_date_apply")
                print(json.dumps({"custom_clicked": custom_clicked, "applied": applied}, ensure_ascii=False))

        return 0
    finally:
        cdp.close()
        close_tab(target_id)


if __name__ == "__main__":
    raise SystemExit(main())
