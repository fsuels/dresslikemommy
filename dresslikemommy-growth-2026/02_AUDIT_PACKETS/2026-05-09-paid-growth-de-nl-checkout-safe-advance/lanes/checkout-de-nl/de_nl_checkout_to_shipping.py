#!/usr/bin/env python3
"""DE/NL isolated-browser checkout-to-shipping QA.

Launches a fresh Chrome profile and drives the public storefront only until
delivery/shipping rates are visible. It never enters payment data, never clicks
Pay/Place order, and never touches Shopify Admin or any ads/catalog surfaces.
"""

from __future__ import annotations

import base64
import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import websocket


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_URL = "https://www.dresslikemommy.com"
HANDLE = "elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits"
VARIANT_ID = "41878479831137"
LANE_DIR = Path(__file__).resolve().parent
RAW_DIR = LANE_DIR / "raw"
SCREENSHOT_DIR = LANE_DIR / "screenshots"
SUMMARY_PATH = LANE_DIR / "de_nl_checkout_to_shipping_summary.json"
REPORT_PATH = LANE_DIR / "DE_NL_CHECKOUT_TO_SHIPPING.md"

MARKETS = {
    "DE": {
        "name": "Germany",
        "currency": "EUR",
        "province": "",
        "city": "Berlin",
        "postal_code": "10115",
        "address1": "Invalidenstrasse 1",
        "phone": "030 123456",
    },
    "NL": {
        "name": "Netherlands",
        "currency": "EUR",
        "province": "",
        "city": "Amsterdam",
        "postal_code": "1012 JS",
        "address1": "Dam 1",
        "phone": "020 123 4567",
    },
}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def redacted_url(url: str) -> str:
    text = str(url or "")
    text = re.sub(r"/checkouts/(cn/)?[^/?#]+", "/checkouts/REDACTED", text)
    text = re.sub(r"/checkout/[^/?#]+", "/checkout/REDACTED", text)
    text = re.sub(r"([?&](?:key|token|_r|_mcs|_cs|tracking_[^=]+)=)[^&#]+", r"\1REDACTED", text)
    return text


def redact_sensitive_text(text: str) -> str:
    redacted = str(text or "")
    redacted = re.sub(r'("token"\s*:\s*")[^"]+', r"\1REDACTED", redacted)
    redacted = re.sub(r'("key"\s*:\s*")[^"]+', r"\1REDACTED", redacted)
    redacted = re.sub(r"((?:token|key)=)[^&\"'\\\s]+", r"\1REDACTED", redacted)
    redacted = re.sub(r"(\d{8,}):[0-9a-f]{12,}", r"\1:REDACTED", redacted)
    return redacted


def sanitize_json(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, child in value.items():
            if str(key).lower() in {"token", "key"}:
                sanitized[key] = "REDACTED"
            else:
                sanitized[key] = sanitize_json(child)
        return sanitized
    if isinstance(value, list):
        return [sanitize_json(child) for child in value]
    if isinstance(value, str):
        return redact_sensitive_text(value)
    return value


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def cdp_json(port: int, path: str, *, method: str = "GET") -> Any:
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}", method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_cdp(port: int) -> None:
    deadline = time.time() + 25
    last_error = ""
    while time.time() < deadline:
        try:
            cdp_json(port, "/json/version")
            return
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.5)
    raise RuntimeError(f"Chrome CDP did not start on port {port}: {last_error}")


def open_target(port: int, url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    return cdp_json(port, f"/json/new?{encoded}", method="PUT")


def close_target(port: int, target_id: str) -> None:
    try:
        cdp_json(port, f"/json/close/{target_id}")
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

    def recv(self, timeout: int = 30) -> dict[str, Any]:
        old_timeout = self.ws.gettimeout()
        self.ws.settimeout(timeout)
        try:
            return json.loads(self.ws.recv())
        finally:
            self.ws.settimeout(old_timeout)

    def recv_until_id(self, message_id: int, timeout_seconds: int = 20) -> dict[str, Any]:
        start = time.time()
        while time.time() - start < timeout_seconds:
            event = self.recv(max(1, int(timeout_seconds - (time.time() - start))))
            if event.get("id") == message_id:
                return event
        raise TimeoutError(f"Timed out waiting for CDP response {message_id}")

    def call(self, method: str, params: dict[str, Any] | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
        return self.recv_until_id(self.send(method, params), timeout_seconds)


def runtime_eval(client: CdpClient, expression: str, timeout: int = 30) -> Any:
    response = client.call(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
        timeout,
    )
    if response.get("result", {}).get("exceptionDetails"):
        return {
            "runtime_exception": clean(response["result"]["exceptionDetails"].get("text")),
            "exception_description": clean(
                response["result"]["exceptionDetails"].get("exception", {}).get("description")
            ),
        }
    result = response.get("result", {}).get("result", {})
    if "value" in result:
        return result["value"]
    if "description" in result:
        return result["description"]
    return None


def wait_for_load(client: CdpClient, timeout: int = 35) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            state = runtime_eval(client, "document.readyState", timeout=5)
            if state in {"interactive", "complete"}:
                time.sleep(2)
                return
        except Exception:
            pass
        time.sleep(0.5)


def navigate(client: CdpClient, url: str, timeout: int = 45) -> None:
    client.call("Page.navigate", {"url": url}, 20)
    wait_for_load(client, timeout)


def snapshot(client: CdpClient) -> dict[str, Any]:
    value = runtime_eval(
        client,
        """
        (() => {
          const metaCurrency = document.querySelector('meta[property="og:price:currency"]')?.content || '';
          return {
            title: document.title || '',
            url: location.href,
            html_lang: document.documentElement.lang || '',
            text: document.body ? document.body.innerText : '',
            currency_meta: metaCurrency,
            country_select_value: document.querySelector('select[name*="country"], select[id*="country"]')?.value || '',
          };
        })()
        """,
        20,
    )
    return value if isinstance(value, dict) else {"title": "", "url": "", "html_lang": "", "text": ""}


def save_screenshot(client: CdpClient, name: str) -> str:
    path = SCREENSHOT_DIR / name
    try:
        response = client.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, 30)
        data = response.get("result", {}).get("data")
        if data:
            path.write_bytes(base64.b64decode(data))
            return str(path)
    except Exception as exc:
        return f"screenshot_failed: {exc}"
    return ""


def page_fetch(client: CdpClient, path: str, options: dict[str, Any] | None = None, timeout: int = 45) -> dict[str, Any]:
    js = f"""
    (async () => {{
      const response = await fetch({json.dumps(path)}, {json.dumps(options or {})});
      const text = await response.text();
      let json = null;
      try {{ json = JSON.parse(text); }} catch (err) {{}}
      return {{
        status: response.status,
        ok: response.ok,
        url: response.url,
        redirected: response.redirected,
        text_excerpt: text.slice(0, 1000),
        json
      }};
    }})()
    """
    value = runtime_eval(client, js, timeout)
    if not isinstance(value, dict):
        return {"status": None, "ok": False, "text_excerpt": redact_sensitive_text(clean(value))}
    return {
        **value,
        "url": redacted_url(value.get("url", "")),
        "text_excerpt": redact_sensitive_text(value.get("text_excerpt", "")),
        "json": sanitize_json(value.get("json")),
    }


def cart_probe(client: CdpClient, market: dict[str, str]) -> dict[str, Any]:
    clear = page_fetch(client, "/cart/clear.js", {"method": "POST", "credentials": "include"}, 45)
    add = page_fetch(
        client,
        "/cart/add.js",
        {
            "method": "POST",
            "credentials": "include",
            "headers": {"Content-Type": "application/json", "Accept": "application/json"},
            "body": json.dumps({"id": VARIANT_ID, "quantity": 1}),
        },
        45,
    )
    cart = page_fetch(client, "/cart.js", {"method": "GET", "credentials": "include"}, 45)
    rates_query = urllib.parse.urlencode(
        {
            "shipping_address[country]": market["name"],
            "shipping_address[province]": market["province"],
            "shipping_address[city]": market["city"],
            "shipping_address[zip]": market["postal_code"],
        }
    )
    rates = page_fetch(client, f"/cart/shipping_rates.json?{rates_query}", {"method": "GET", "credentials": "include"}, 45)
    return {"clear": clear, "add": add, "cart": cart, "shipping_rates_api": rates}


def click_checkout(client: CdpClient) -> dict[str, Any]:
    return runtime_eval(
        client,
        """
        (() => {
          const blocked = /(pay|place order|complete order|pagar|comprar|submit order)/i;
          const candidates = [...document.querySelectorAll('a,button,input[type="submit"]')].map((el, index) => ({
            index,
            text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim(),
            href: el.href || '',
            visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
          })).filter(row => row.visible);
          const match = candidates.find(row => /checkout/i.test(row.text + ' ' + row.href) && !blocked.test(row.text));
          if (match) {
            const el = [...document.querySelectorAll('a,button,input[type="submit"]')][match.index];
            el.click();
            return {clicked: true, match};
          }
          location.href = '/checkout';
          return {clicked: false, navigated: '/checkout', candidates: candidates.slice(0, 20)};
        })()
        """,
        20,
    )


def fill_checkout(client: CdpClient, country_code: str, market: dict[str, str]) -> dict[str, Any]:
    data = {
        "email": f"dlm-{country_code.lower()}-readonly-{int(time.time())}@example.com",
        "firstName": "Readonly",
        "lastName": "QA",
        "address1": market["address1"],
        "city": market["city"],
        "postalCode": market["postal_code"],
        "phone": market["phone"],
        "country": market["name"],
        "province": market["province"],
    }
    expression = r"""
        (async () => {
          const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
          const data = __DATA__;
          const events = [];
          const all = () => [...document.querySelectorAll('input, textarea, select')];
          const labelFor = el => {
            const label = el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`) : null;
            return [
              el.name, el.id, el.autocomplete, el.placeholder, el.getAttribute('aria-label'),
              label?.innerText
            ].filter(Boolean).join(' ').toLowerCase();
          };
          const setValue = (el, value) => {
            if (!el) return false;
            el.focus();
            const setter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value')?.set;
            if (setter) setter.call(el, value); else el.value = value;
            el.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: value}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
            el.blur();
            return true;
          };
          const fill = (tokens, value) => {
            const tokenList = Array.isArray(tokens) ? tokens : [tokens];
            const el = all().find(input => tokenList.some(token => labelFor(input).includes(token)) && input.type !== 'hidden');
            const ok = setValue(el, value);
            events.push({tokens: tokenList, ok, tag: el?.tagName || '', name: el?.name || '', id: el?.id || ''});
            return ok;
          };
          const selectByText = (tokens, value) => {
            const tokenList = Array.isArray(tokens) ? tokens : [tokens];
            const el = all().find(input => input.tagName === 'SELECT' && tokenList.some(token => labelFor(input).includes(token)));
            if (!el) {
              events.push({tokens: tokenList, ok: false, tag: '', select_text: value});
              return false;
            }
            const option = [...el.options].find(opt => (opt.textContent || '').toLowerCase().includes(value.toLowerCase()) || opt.value.toLowerCase().includes(value.toLowerCase()));
            const ok = setValue(el, option ? option.value : value);
            events.push({tokens: tokenList, ok, tag: el.tagName, name: el.name || '', id: el.id || '', select_text: value, selected: el.value});
            return ok;
          };

          fill(['email'], data.email);
          fill(['first name', 'given-name', 'firstname'], data.firstName);
          fill(['last name', 'family-name', 'lastname'], data.lastName);
          fill(['address1', 'address line 1', 'address-line1', 'address'], data.address1);
          fill(['city', 'locality'], data.city);
          fill(['postal', 'zip', 'postcode', 'postal-code'], data.postalCode);
          fill(['phone', 'tel'], data.phone);
          selectByText(['country'], data.country);
          if (data.province) selectByText(['province', 'state', 'zone'], data.province);
          await sleep(3000);

          const safeContinue = [...document.querySelectorAll('button, input[type="submit"]')].find(el => {
            const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
            return /(continue|shipping|delivery)/i.test(text) && !/(pay|place order|complete|pagar|comprar)/i.test(text) && !el.disabled;
          });
          if (safeContinue) {
            safeContinue.click();
            events.push({clicked_safe_continue: (safeContinue.innerText || safeContinue.value || '').trim()});
            await sleep(6000);
          }
          return {
            events,
            url: location.href,
            title: document.title,
            html_lang: document.documentElement.lang || '',
            text: document.body ? document.body.innerText.slice(0, 5000) : ''
          };
        })()
        """.replace("__DATA__", json.dumps(data))
    return runtime_eval(
        client,
        expression,
        90,
    )


def checkout_state(client: CdpClient, currency: str) -> dict[str, Any]:
    expression = r"""
        (() => {
          const text = document.body ? document.body.innerText : '';
          const currency = __CURRENCY__;
          const moneyPattern = new RegExp('(' + currency + '|EUR|€|CHF|DKK|kr|USD|GBP|CAD|AUD|\\\\$|free|gratis)', 'i');
          const rates = text.split(/\n+/).filter(line => /(standard|express|delivery|shipping)/i.test(line) || moneyPattern.test(line)).slice(0, 80);
          const buttons = [...document.querySelectorAll('button, input[type="submit"]')].map(el => ({
            text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim(),
            disabled: !!el.disabled,
            visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
          })).filter(row => row.visible).slice(0, 40);
          const inputs = [...document.querySelectorAll('input, select, textarea')].map(el => ({
            tag: el.tagName,
            name: el.name || '',
            id: el.id || '',
            autocomplete: el.autocomplete || '',
            value: el.tagName === 'SELECT' ? (el.options[el.selectedIndex]?.textContent || el.value || '') : (el.value || ''),
            visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
          })).filter(row => row.visible).slice(0, 80);
          return {
            title: document.title || '',
            url: location.href,
            html_lang: document.documentElement.lang || '',
            text_excerpt: text.slice(0, 7000),
            rates_lines: rates,
            buttons,
            visible_inputs: inputs,
            has_standard: /standard/i.test(text),
            has_express: /express/i.test(text),
            has_currency: new RegExp('\\\\b' + currency + '\\\\b|EUR|€\\\\s*\\\\d|CHF|DKK|kr|\\\\$\\\\s*\\\\d|£\\\\s*\\\\d', 'i').test(text),
            has_pay_now: /(pay now|place order|complete order|pagar agora)/i.test(text),
            has_order_confirmation: /\/thank_you|\/orders\//i.test(location.href) || /(thank you for your purchase|your order is confirmed|order confirmed)/i.test(text)
          };
        })()
        """.replace("__CURRENCY__", json.dumps(currency))
    return runtime_eval(
        client,
        expression,
        20,
    )


def launch_chrome(port: int, profile_dir: Path) -> subprocess.Popen[str]:
    if profile_dir.exists():
        shutil.rmtree(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)
    args = [
        CHROME,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--disable-features=Translate,OptimizationHints",
        "--new-window",
        "about:blank",
    ]
    env = os.environ.copy()
    return subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True, env=env)


def build_summary(client: CdpClient, country_code: str) -> dict[str, Any]:
    market = MARKETS[country_code]
    product_url = f"{BASE_URL}/products/{HANDLE}?variant={VARIANT_ID}&country={country_code}"
    network_events: list[dict[str, Any]] = []
    client.call("Page.enable")
    client.call("Runtime.enable")
    client.call("Network.enable", {"maxTotalBufferSize": 20_000_000, "maxResourceBufferSize": 10_000_000})

    navigate(client, product_url)
    product = snapshot(client)
    product["screenshot"] = save_screenshot(client, f"{country_code.lower()}-product.png")
    product["url"] = redacted_url(product.get("url", ""))

    cart_api = cart_probe(client, market)
    network_events.append({"step": "cart_api_probe", "data": cart_api})
    navigate(client, f"{BASE_URL}/cart")
    cart = snapshot(client)
    cart["screenshot"] = save_screenshot(client, f"{country_code.lower()}-cart-before-checkout.png")
    cart["url"] = redacted_url(cart.get("url", ""))

    checkout_click = click_checkout(client)
    time.sleep(8)
    wait_for_load(client, 45)
    checkout_entry = snapshot(client)
    checkout_entry["screenshot"] = save_screenshot(client, f"{country_code.lower()}-checkout-entry.png")
    checkout_entry["url"] = redacted_url(checkout_entry.get("url", ""))

    fill_result = fill_checkout(client, country_code, market)
    time.sleep(8)
    state = checkout_state(client, market["currency"])
    if not isinstance(state, dict) or state.get("runtime_exception"):
        fallback = snapshot(client)
        fallback_lines = [
            clean(line)
            for line in str(fallback.get("text", "")).splitlines()
            if re.search(r"(standard|express|delivery|shipping|chf|dkk|kr|\$|free|gratis)", line, re.I)
        ][:80]
        state = {
            "runtime_state_error": state,
            "title": fallback.get("title", ""),
            "url": fallback.get("url", ""),
            "html_lang": fallback.get("html_lang", ""),
            "text_excerpt": clean(fallback.get("text", ""))[:7000],
            "rates_lines": fallback_lines,
            "buttons": [],
            "has_standard": bool(re.search(r"standard", fallback.get("text", ""), re.I)),
            "has_express": bool(re.search(r"express", fallback.get("text", ""), re.I)),
            "has_currency": bool(re.search(r"\\b(EUR|CHF|DKK)\\b|€\\s*\\d|\\bkr\\b|\\$\\s*\\d", fallback.get("text", ""), re.I)),
            "has_pay_now": bool(re.search(r"(pay now|place order|complete order|pagar agora)", fallback.get("text", ""), re.I)),
            "has_order_confirmation": bool(
                re.search(r"(/thank_you|/orders/)", fallback.get("url", ""), re.I)
                or re.search(r"(thank you for your purchase|your order is confirmed|order confirmed)", fallback.get("text", ""), re.I)
            ),
        }
    state["screenshot"] = save_screenshot(client, f"{country_code.lower()}-checkout-shipping-rates.png")
    state["url"] = redacted_url(state.get("url", ""))

    cart_json = cart_api.get("cart", {}).get("json") if isinstance(cart_api.get("cart"), dict) else {}
    rates_json = cart_api.get("shipping_rates_api", {}).get("json") if isinstance(cart_api.get("shipping_rates_api"), dict) else {}
    rates = rates_json.get("shipping_rates") if isinstance(rates_json, dict) else None
    blocked = any(
        "Verifying your connection" in clean(step.get("text_excerpt"))
        for step in [cart_api.get("add", {}), cart_api.get("cart", {}), cart_api.get("shipping_rates_api", {})]
        if isinstance(step, dict)
    )
    shipping_ui_pass = bool(state.get("has_standard") and state.get("has_express") and state.get("has_currency") and not state.get("has_order_confirmation"))
    api_rates_pass = bool(rates)
    decision = (
        f"{country_code}_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER"
        if shipping_ui_pass or api_rates_pass
        else f"{country_code}_CHECKOUT_STILL_BLOCKED_OR_RATES_NOT_VISIBLE"
    )
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "lane": "DE/NL isolated-browser checkout-to-shipping QA",
        "country_code": country_code,
        "problem_id": "PROB-2026-05-09-DE-NL-CHECKOUT-QA",
        "mode": "PUBLIC_STOREFRONT_ISOLATED_CHROME_NO_PAYMENT_NO_ORDER",
        "product_url": product_url,
        "variant_id": VARIANT_ID,
        "address": {
            "country": market["name"],
            "province": market["province"],
            "city": market["city"],
            "postal_code": market["postal_code"],
        },
        "guardrails_preserved": [
            "no payment data entered",
            "no Pay Now / Place order click",
            "no order creation",
            "no Shopify Admin, theme, product data, Merchant, Google Ads, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal writes",
        ],
        "product": product,
        "cart_api_probe": cart_api,
        "cart": cart,
        "checkout_click": checkout_click,
        "checkout_entry": checkout_entry,
        "fill_result": {
            **{key: value for key, value in fill_result.items() if key != "text"},
            "text_excerpt": clean(fill_result.get("text", ""))[:1800] if isinstance(fill_result, dict) else "",
            "url": redacted_url(fill_result.get("url", "")) if isinstance(fill_result, dict) else "",
        },
        "checkout_shipping_state": state,
        "network_events": network_events,
        "api_rates": rates or [],
        "cart_currency": cart_json.get("currency") if isinstance(cart_json, dict) else "",
        "cart_item_count": cart_json.get("item_count") if isinstance(cart_json, dict) else None,
        "blocked_by_verification_text": blocked or "Verifying your connection" in clean(product.get("text")) or "Verifying your connection" in clean(state.get("text_excerpt")),
        "shipping_ui_pass": shipping_ui_pass,
        "api_rates_pass": api_rates_pass,
        "payment_or_order_created": bool(state.get("has_order_confirmation")),
        "decision": decision,
    }


def write_report(summaries: list[dict[str, Any]]) -> None:
    lines = [
        "# DE/NL Checkout To Shipping Readback",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Mode: public storefront isolated Chrome profile. No payment data was entered, no pay/place-order button was clicked, and no order was created.",
        "",
    ]
    for summary in summaries:
        product = summary["product"]
        cart_api = summary["cart_api_probe"]
        state = summary["checkout_shipping_state"]
        rates = summary.get("api_rates") or []
        lines.extend(
            [
                f"## {summary['country_code']}",
                "",
                f"Decision: `{summary['decision']}`.",
                "",
                "### Product And Cart",
                "",
                f"- Product URL: `{summary['product_url']}`",
                f"- Product page title: `{product.get('title', '')}`",
                f"- Product `html lang`: `{product.get('html_lang', '')}`",
                f"- Product currency meta: `{product.get('currency_meta', '')}`",
                f"- Cart add HTTP status: `{cart_api.get('add', {}).get('status')}`",
                f"- Cart read HTTP status: `{cart_api.get('cart', {}).get('status')}`",
                f"- Cart currency: `{summary.get('cart_currency')}`",
                f"- Cart item count: `{summary.get('cart_item_count')}`",
                f"- Shipping-rates API HTTP status: `{cart_api.get('shipping_rates_api', {}).get('status')}`",
                "",
                "### Shipping Rates",
                "",
            ]
        )
        if rates:
            lines.extend(["| Rate | Price | Currency |", "| --- | --- | --- |"])
            for rate in rates:
                lines.append(f"| `{rate.get('name') or rate.get('presentment_name')}` | `{rate.get('price')}` | `{rate.get('currency')}` |")
        else:
            lines.append("- No rates returned from the API probe.")
        lines.extend(
            [
                "",
                "### Checkout UI",
                "",
                f"- Checkout URL redacted: `{state.get('url', '')}`",
                f"- Checkout `html lang`: `{state.get('html_lang', '')}`",
                f"- UI contains Standard: `{state.get('has_standard')}`",
                f"- UI contains Express: `{state.get('has_express')}`",
                f"- UI contains currency / money signal: `{state.get('has_currency')}`",
                f"- Pay-now button visible: `{state.get('has_pay_now')}`",
                f"- Order confirmation text found: `{state.get('has_order_confirmation')}`",
                f"- Blocked by verification text: `{summary.get('blocked_by_verification_text')}`",
                "",
                "Relevant checkout lines:",
                "",
            ]
        )
        for line in state.get("rates_lines", [])[:60]:
            lines.append(f"- `{clean(line)}`")
        lines.append("")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- Summary JSON: `{SUMMARY_PATH}`",
            f"- Screenshots: `{SCREENSHOT_DIR}`",
            "- The temporary isolated Chrome profile is deleted after each run so storefront cookies/session data are not persisted in the repo.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_country(country_code: str) -> dict[str, Any]:
    profile_dir = RAW_DIR / f"chrome-{country_code.lower()}-isolated-profile"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    port = free_port()
    proc = launch_chrome(port, profile_dir)
    target_id = ""
    try:
        wait_for_cdp(port)
        target = open_target(port, "about:blank")
        target_id = target.get("id", "")
        client = CdpClient(target["webSocketDebuggerUrl"])
        try:
            return build_summary(client, country_code)
        finally:
            client.close()
    finally:
        if target_id:
            close_target(port, target_id)
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        if profile_dir.exists():
            shutil.rmtree(profile_dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--countries", nargs="+", choices=sorted(MARKETS), default=["DE"])
    args = parser.parse_args()
    summaries: list[dict[str, Any]] = []
    if SUMMARY_PATH.exists():
        try:
            existing = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            summaries = [
                summary
                for summary in existing.get("summaries", [])
                if isinstance(summary, dict) and summary.get("country_code") not in set(args.countries)
            ]
        except Exception:
            summaries = []
    for country_code in args.countries:
        summary = run_country(country_code)
        summaries.append(summary)
        if summary.get("blocked_by_verification_text") or summary.get("payment_or_order_created"):
            break
    SUMMARY_PATH.write_text(json.dumps({"summaries": summaries}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summaries)
    print(
        json.dumps(
            {
                "summary": str(SUMMARY_PATH),
                "report": str(REPORT_PATH),
                "decisions": [summary["decision"] for summary in summaries],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
