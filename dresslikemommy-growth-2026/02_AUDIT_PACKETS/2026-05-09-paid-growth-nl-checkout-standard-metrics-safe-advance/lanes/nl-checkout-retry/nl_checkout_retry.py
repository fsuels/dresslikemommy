#!/usr/bin/env python3
"""NL isolated-browser checkout-to-shipping cooldown retry.

Public storefront only. The runner stops on the first HTTP 429, verification
wall, unexpected order signal, or payment/order risk. It never enters payment
data and never clicks Pay Now / Place Order.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any


LANE_DIR = Path(__file__).resolve().parent
REPO_ROOT = LANE_DIR.parents[4]
TEMPLATE_PATH = (
    REPO_ROOT
    / "dresslikemommy-growth-2026"
    / "02_AUDIT_PACKETS"
    / "2026-05-09-paid-growth-de-nl-checkout-safe-advance"
    / "lanes"
    / "checkout-de-nl"
    / "de_nl_checkout_to_shipping.py"
)
RAW_DIR = LANE_DIR / "raw"
SCREENSHOT_DIR = LANE_DIR / "screenshots"
SUMMARY_PATH = LANE_DIR / "nl_checkout_retry_summary.json"
COMPACT_SUMMARY_PATH = LANE_DIR / "summary.json"
REPORT_PATH = LANE_DIR / "NL_CHECKOUT_RETRY_TO_SHIPPING.md"

COUNTRY_CODE = "NL"
MARKET = {
    "name": "Netherlands",
    "currency": "EUR",
    "province": "",
    "city": "Amsterdam",
    "postal_code": "1012 JS",
    "address1": "Dam 1",
    "phone": "020 123 4567",
}


def load_template() -> Any:
    spec = importlib.util.spec_from_file_location("dlm_de_nl_checkout_template", TEMPLATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import checkout template: {TEMPLATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.LANE_DIR = LANE_DIR
    module.RAW_DIR = RAW_DIR
    module.SCREENSHOT_DIR = SCREENSHOT_DIR
    module.SUMMARY_PATH = SUMMARY_PATH
    module.REPORT_PATH = REPORT_PATH
    return module


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def has_verification_text(value: object) -> bool:
    text = clean(value)
    return bool(re.search(r"verifying your connection|protected by hcaptcha|captcha|checking your browser", text, re.I))


def status_of(step: dict[str, Any] | None) -> int | None:
    status = (step or {}).get("status")
    return int(status) if isinstance(status, int) else None


def stop_reason_for(step_name: str, step: dict[str, Any]) -> str | None:
    status = status_of(step)
    if status == 429:
        return f"STOP_HTTP_429_AT_{step_name.upper()}"
    if has_verification_text(step.get("text_excerpt", "")):
        return f"STOP_VERIFICATION_TEXT_AT_{step_name.upper()}"
    return None


def page_contains_stop_signal(snapshot: dict[str, Any]) -> str | None:
    text = clean(snapshot.get("text", ""))
    url = str(snapshot.get("url", ""))
    if has_verification_text(text):
        return "STOP_VERIFICATION_TEXT_ON_PAGE"
    if re.search(r"/thank_you|/orders/", url, re.I) or re.search(
        r"thank you for your purchase|your order is confirmed|order confirmed", text, re.I
    ):
        return "STOP_ORDER_CONFIRMATION_SIGNAL"
    if re.search(r"pay now|place order|complete order", text, re.I):
        return "STOP_PAYMENT_STEP_VISIBLE_BEFORE_ALLOWED"
    return None


def redacted_snapshot(template: Any, client: Any, screenshot_name: str) -> dict[str, Any]:
    snap = template.snapshot(client)
    snap["screenshot"] = template.save_screenshot(client, screenshot_name)
    snap["url"] = template.redacted_url(snap.get("url", ""))
    return snap


def fetch_step(template: Any, client: Any, name: str, path: str, options: dict[str, Any], timeout: int = 45) -> dict[str, Any]:
    result = template.page_fetch(client, path, options, timeout)
    result["step"] = name
    return result


def safe_checkout_state(template: Any, client: Any, fill_result: dict[str, Any] | None = None) -> dict[str, Any]:
    state = template.checkout_state(client, MARKET["currency"])
    if not isinstance(state, dict) or state.get("runtime_exception"):
        fallback = template.snapshot(client)
        state = {
            "runtime_state_error": state,
            "title": fallback.get("title", ""),
            "url": fallback.get("url", ""),
            "html_lang": fallback.get("html_lang", ""),
            "text_excerpt": clean(fallback.get("text", ""))[:7000],
            "rates_lines": [
                clean(line)
                for line in str(fallback.get("text", "")).splitlines()
                if re.search(r"(standard|express|delivery|shipping|eur|\u20ac|free|gratis)", line, re.I)
            ][:80],
            "buttons": [],
            "has_standard": bool(re.search(r"standard", fallback.get("text", ""), re.I)),
            "has_express": bool(re.search(r"express", fallback.get("text", ""), re.I)),
            "has_currency": bool(re.search(r"\bEUR\b|\u20ac\s*\d|free|gratis", fallback.get("text", ""), re.I)),
            "has_pay_now": bool(re.search(r"(pay now|place order|complete order)", fallback.get("text", ""), re.I)),
            "has_order_confirmation": bool(
                re.search(r"(/thank_you|/orders/)", fallback.get("url", ""), re.I)
                or re.search(r"(thank you for your purchase|your order is confirmed|order confirmed)", fallback.get("text", ""), re.I)
            ),
        }
    if fill_result:
        state["fill_result"] = {
            **{key: value for key, value in fill_result.items() if key != "text"},
            "text_excerpt": clean(fill_result.get("text", ""))[:1800],
            "url": template.redacted_url(fill_result.get("url", "")),
        }
    state["screenshot"] = template.save_screenshot(client, "nl-checkout-shipping-rates.png")
    state["url"] = template.redacted_url(state.get("url", ""))
    return state


def summarize_decision(summary: dict[str, Any]) -> str:
    if summary.get("payment_or_order_created"):
        return "NL_STOP_ORDER_RISK_DETECTED"
    if summary.get("stop_reason") == "STOP_PAYMENT_STEP_VISIBLE_BEFORE_ALLOWED" and summary.get("api_rates_pass"):
        return "NL_API_RATES_PASS_CHECKOUT_REACHED_NL_SELECTION_NOT_CONFIRMED_NO_PAYMENT_NO_ORDER"
    if summary.get("stop_reason"):
        return str(summary["stop_reason"])
    if summary.get("blocked_by_verification_text"):
        return "NL_STOP_VERIFICATION_NO_BYPASS"
    if summary.get("shipping_ui_pass") and summary.get("api_rates_pass"):
        return "NL_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER"
    if summary.get("api_rates_pass"):
        return "NL_API_RATES_PASS_CHECKOUT_UI_NOT_CONFIRMED"
    return "NL_CHECKOUT_STILL_BLOCKED_OR_RATES_NOT_VISIBLE"


def build_summary(template: Any, client: Any) -> dict[str, Any]:
    product_url = f"{template.BASE_URL}/products/{template.HANDLE}?variant={template.VARIANT_ID}&country={COUNTRY_CODE}"
    network_events: list[dict[str, Any]] = []
    stop_reason = ""

    client.call("Page.enable")
    client.call("Runtime.enable")
    client.call("Network.enable", {"maxTotalBufferSize": 20_000_000, "maxResourceBufferSize": 10_000_000})

    template.navigate(client, product_url)
    product = redacted_snapshot(template, client, "nl-product.png")
    stop_reason = page_contains_stop_signal(product) or ""

    cart_api: dict[str, Any] = {}
    cart: dict[str, Any] = {}
    checkout_click: dict[str, Any] = {}
    checkout_entry: dict[str, Any] = {}
    fill_result: dict[str, Any] = {}
    checkout_shipping_state: dict[str, Any] = {}

    if not stop_reason:
        add = fetch_step(
            template,
            client,
            "cart_add",
            "/cart/add.js",
            {
                "method": "POST",
                "credentials": "include",
                "headers": {"Content-Type": "application/json", "Accept": "application/json"},
                "body": json.dumps({"id": template.VARIANT_ID, "quantity": 1}),
            },
        )
        cart_api["add"] = add
        network_events.append({"step": "cart_add", "data": add})
        stop_reason = stop_reason_for("cart_add", add) or ""

    if not stop_reason:
        cart_read = fetch_step(template, client, "cart_read", "/cart.js", {"method": "GET", "credentials": "include"})
        cart_api["cart"] = cart_read
        network_events.append({"step": "cart_read", "data": cart_read})
        stop_reason = stop_reason_for("cart_read", cart_read) or ""

    if not stop_reason:
        rates_query = urllib.parse.urlencode(
            {
                "shipping_address[country]": MARKET["name"],
                "shipping_address[province]": MARKET["province"],
                "shipping_address[city]": MARKET["city"],
                "shipping_address[zip]": MARKET["postal_code"],
            }
        )
        rates = fetch_step(
            template,
            client,
            "shipping_rates_api",
            f"/cart/shipping_rates.json?{rates_query}",
            {"method": "GET", "credentials": "include"},
        )
        cart_api["shipping_rates_api"] = rates
        network_events.append({"step": "shipping_rates_api", "data": rates})
        stop_reason = stop_reason_for("shipping_rates_api", rates) or ""

    if not stop_reason:
        template.navigate(client, f"{template.BASE_URL}/cart")
        cart = redacted_snapshot(template, client, "nl-cart-before-checkout.png")
        stop_reason = page_contains_stop_signal(cart) or ""

    if not stop_reason:
        checkout_click = template.click_checkout(client)
        time.sleep(8)
        template.wait_for_load(client, 45)
        checkout_entry = redacted_snapshot(template, client, "nl-checkout-entry.png")
        stop_reason = page_contains_stop_signal(checkout_entry) or ""

    if not stop_reason:
        fill_result = template.fill_checkout(client, COUNTRY_CODE, MARKET)
        time.sleep(8)
        checkout_shipping_state = safe_checkout_state(template, client, fill_result)
        stop_reason = page_contains_stop_signal(
            {
                "url": checkout_shipping_state.get("url", ""),
                "text": checkout_shipping_state.get("text_excerpt", ""),
            }
        ) or ""

    if stop_reason and not checkout_shipping_state:
        checkout_shipping_state = redacted_snapshot(template, client, "nl-stop-page.png")
        checkout_shipping_state = {
            "title": checkout_shipping_state.get("title", ""),
            "url": checkout_shipping_state.get("url", ""),
            "html_lang": checkout_shipping_state.get("html_lang", ""),
            "text_excerpt": clean(checkout_shipping_state.get("text", ""))[:7000],
            "rates_lines": [
                clean(line)
                for line in str(checkout_shipping_state.get("text", "")).splitlines()
                if re.search(r"(standard|express|delivery|shipping|eur|\u20ac|free|gratis|verifying|captcha)", line, re.I)
            ][:80],
            "screenshot": checkout_shipping_state.get("screenshot", ""),
            "has_standard": False,
            "has_express": False,
            "has_currency": bool(re.search(r"\bEUR\b|\u20ac", checkout_shipping_state.get("text", ""), re.I)),
            "has_pay_now": False,
            "has_order_confirmation": False,
        }

    cart_json = cart_api.get("cart", {}).get("json") if isinstance(cart_api.get("cart"), dict) else {}
    rates_json = cart_api.get("shipping_rates_api", {}).get("json") if isinstance(cart_api.get("shipping_rates_api"), dict) else {}
    rates = rates_json.get("shipping_rates") if isinstance(rates_json, dict) else []
    blocked = any(
        has_verification_text(step.get("text_excerpt", ""))
        for step in cart_api.values()
        if isinstance(step, dict)
    ) or has_verification_text(product.get("text", "")) or has_verification_text(checkout_shipping_state.get("text_excerpt", ""))
    payment_or_order_created = bool(checkout_shipping_state.get("has_order_confirmation"))
    shipping_ui_pass = bool(
        checkout_shipping_state.get("has_standard")
        and checkout_shipping_state.get("has_express")
        and checkout_shipping_state.get("has_currency")
        and not payment_or_order_created
        and not stop_reason
    )
    summary = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "lane": "NL isolated-browser checkout-to-shipping cooldown retry",
        "problem_id": "PROB-2026-05-09-NL-CHECKOUT-429-RETRY",
        "mode": "PUBLIC_STOREFRONT_ISOLATED_CHROME_NO_PAYMENT_NO_ORDER_STOP_ON_429",
        "product_url": product_url,
        "variant_id": template.VARIANT_ID,
        "address": {
            "country": MARKET["name"],
            "province": MARKET["province"],
            "city": MARKET["city"],
            "postal_code": MARKET["postal_code"],
        },
        "guardrails_preserved": [
            "single low-volume NL public storefront retry",
            "isolated Chrome profile",
            "stopped on first HTTP 429 or verification signal",
            "no CAPTCHA or verification bypass",
            "no payment data entered",
            "no Pay Now / Place Order click",
            "no order creation",
            "no Shopify Admin, theme, product data, Merchant, Google Ads, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal writes",
        ],
        "stop_reason": stop_reason,
        "product": product,
        "cart_api_probe": cart_api,
        "cart": cart,
        "checkout_click": checkout_click,
        "checkout_entry": checkout_entry,
        "fill_result": {
            **{key: value for key, value in fill_result.items() if key != "text"},
            "text_excerpt": clean(fill_result.get("text", ""))[:1800] if fill_result else "",
            "url": template.redacted_url(fill_result.get("url", "")) if fill_result else "",
        },
        "checkout_shipping_state": checkout_shipping_state,
        "network_events": network_events,
        "api_rates": rates or [],
        "cart_currency": cart_json.get("currency") if isinstance(cart_json, dict) else "",
        "cart_item_count": cart_json.get("item_count") if isinstance(cart_json, dict) else None,
        "blocked_by_verification_text": blocked,
        "shipping_ui_pass": shipping_ui_pass,
        "api_rates_pass": bool(rates),
        "payment_or_order_created": payment_or_order_created,
    }
    summary["decision"] = summarize_decision(summary)
    return summary


def write_compact_summary(summary: dict[str, Any]) -> None:
    rates = summary.get("api_rates") or []
    checkout_text = " ".join(
        [
            str(summary.get("checkout_entry", {}).get("text", "")),
            str(summary.get("checkout_shipping_state", {}).get("text_excerpt", "")),
        ]
    )
    selected_netherlands_confirmed = bool(
        re.search(r"Country/Region\s+Netherlands|Netherlands\s+---|Netherlands\s+\+31", checkout_text, re.I)
    )
    compact = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "problem_id": summary.get("problem_id"),
        "packet": str(LANE_DIR),
        "decision": summary.get("decision"),
        "stop_reason": summary.get("stop_reason"),
        "country_code": COUNTRY_CODE,
        "product_reached": bool(summary.get("product")),
        "cart_add_status": status_of(summary.get("cart_api_probe", {}).get("add")),
        "cart_read_status": status_of(summary.get("cart_api_probe", {}).get("cart")),
        "shipping_rates_status": status_of(summary.get("cart_api_probe", {}).get("shipping_rates_api")),
        "checkout_reached": bool(summary.get("checkout_entry")),
        "selected_netherlands_confirmed_in_checkout": selected_netherlands_confirmed,
        "payment_action_guardrail_triggered": summary.get("stop_reason") == "STOP_PAYMENT_STEP_VISIBLE_BEFORE_ALLOWED",
        "checkout_shipping_ui_pass": summary.get("shipping_ui_pass"),
        "cart_currency": summary.get("cart_currency"),
        "blocked_by_verification_text": summary.get("blocked_by_verification_text"),
        "payment_or_order_created": summary.get("payment_or_order_created"),
        "api_rates": [
            {
                "name": rate.get("name") or rate.get("presentment_name"),
                "price": rate.get("price"),
                "currency": rate.get("currency"),
            }
            for rate in rates
        ],
    }
    COMPACT_SUMMARY_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(summary: dict[str, Any]) -> None:
    product = summary.get("product", {})
    cart_api = summary.get("cart_api_probe", {})
    state = summary.get("checkout_shipping_state", {})
    rates = summary.get("api_rates") or []
    checkout_text = " ".join(
        [
            str(summary.get("checkout_entry", {}).get("text", "")),
            str(state.get("text_excerpt", "")),
        ]
    )
    selected_netherlands_confirmed = bool(
        re.search(r"Country/Region\s+Netherlands|Netherlands\s+---|Netherlands\s+\+31", checkout_text, re.I)
    )
    product_presentment_ok = bool(
        re.search(r"Netherlands\s*\|\s*EUR|EUR\s*\u20ac|\u20ac", product.get("text", ""), re.I)
    )
    lines = [
        "# NL Checkout Retry To Shipping Readback",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Mode: single public storefront Netherlands cooldown retry in an isolated Chrome profile. No payment data was entered, no Pay Now/Place Order button was clicked, no order was created, and no CAPTCHA or verification bypass was attempted.",
        "",
        "## Result",
        "",
        f"- Decision: `{summary.get('decision')}`",
        f"- Stop reason: `{summary.get('stop_reason') or 'none'}`",
        f"- Product reached: `{bool(product)}`",
        f"- Cart add HTTP status: `{status_of(cart_api.get('add'))}`",
        f"- Cart read HTTP status: `{status_of(cart_api.get('cart'))}`",
        f"- Shipping-rates API HTTP status: `{status_of(cart_api.get('shipping_rates_api'))}`",
        f"- Checkout reached: `{bool(summary.get('checkout_entry'))}`",
        f"- Selected Netherlands confirmed in checkout UI: `{selected_netherlands_confirmed}`",
        f"- Payment-action guardrail triggered: `{summary.get('stop_reason') == 'STOP_PAYMENT_STEP_VISIBLE_BEFORE_ALLOWED'}`",
        f"- Checkout shipping UI pass: `{summary.get('shipping_ui_pass')}`",
        f"- Blocked by verification text: `{summary.get('blocked_by_verification_text')}`",
        f"- Payment/order created: `{summary.get('payment_or_order_created')}`",
        "- Live-spend-ready non-US markets remain `0`; this lane is paused-infrastructure QA only.",
        "- Note: this single retry was not repeated. It cleared the prior NL `429` on cart/rates, then stopped at checkout entry before address fill because the conservative guardrail detected payment-action text on the checkout page.",
        "",
        "## Product And Cart",
        "",
        f"- Product URL: `{summary.get('product_url')}`",
        f"- Product page title: `{product.get('title', '')}`",
        f"- Product `html lang`: `{product.get('html_lang', '')}`",
        f"- Product currency meta: `{product.get('currency_meta', '')}`",
        f"- Product presentment text includes Netherlands/EUR: `{product_presentment_ok}`",
        f"- Cart currency: `{summary.get('cart_currency')}`",
        f"- Cart item count: `{summary.get('cart_item_count')}`",
        "",
        "## Shipping Rates",
        "",
    ]
    if rates:
        lines.extend(["| Rate | Price | Currency |", "| --- | --- | --- |"])
        for rate in rates:
            lines.append(f"| `{rate.get('name') or rate.get('presentment_name')}` | `{rate.get('price')}` | `{rate.get('currency')}` |")
    else:
        excerpt = clean((cart_api.get("shipping_rates_api") or {}).get("text_excerpt", ""))
        lines.append(f"- No rates returned. Excerpt: `{excerpt[:300]}`")
    lines.extend(
        [
            "",
            "## Checkout UI",
            "",
            f"- Checkout URL redacted: `{state.get('url', '')}`",
            f"- Checkout `html lang`: `{state.get('html_lang', '')}`",
            f"- UI contains Standard: `{state.get('has_standard')}`",
            f"- UI contains Express: `{state.get('has_express')}`",
            f"- UI contains currency / money signal: `{state.get('has_currency')}`",
            f"- Pay-now button visible: `{state.get('has_pay_now')}`",
            f"- Order confirmation text found: `{state.get('has_order_confirmation')}`",
            "",
            "Relevant visible lines:",
            "",
        ]
    )
    for line in state.get("rates_lines", [])[:60]:
        lines.append(f"- `{clean(line)}`")
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            f"- Detailed summary JSON: `{SUMMARY_PATH}`",
            f"- Compact summary JSON: `{COMPACT_SUMMARY_PATH}`",
            f"- Screenshots: `{SCREENSHOT_DIR}`",
            "- Temporary isolated Chrome profile was deleted after the run.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def normalize_existing_summary(summary: dict[str, Any]) -> dict[str, Any]:
    state = summary.get("checkout_shipping_state")
    if isinstance(state, dict):
        text = " ".join([str(state.get("text_excerpt", "")), " ".join(str(line) for line in state.get("rates_lines", []))])
        state["has_standard"] = bool(re.search(r"standard", text, re.I))
        state["has_express"] = bool(re.search(r"express", text, re.I))
        state["has_currency"] = bool(re.search(r"\bEUR\b|\u20ac|free|gratis", text, re.I))
        state["has_order_confirmation"] = bool(
            state.get("has_order_confirmation")
            or re.search(r"(/thank_you|/orders/)", str(state.get("url", "")), re.I)
            or re.search(r"(thank you for your purchase|your order is confirmed|order confirmed)", text, re.I)
        )
    summary["payment_or_order_created"] = bool(summary.get("payment_or_order_created") or (state or {}).get("has_order_confirmation"))
    summary["decision"] = summarize_decision(summary)
    return summary


def run() -> dict[str, Any]:
    template = load_template()
    profile_dir = RAW_DIR / "chrome-nl-isolated-profile"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    port = template.free_port()
    proc = template.launch_chrome(port, profile_dir)
    target_id = ""
    try:
        template.wait_for_cdp(port)
        target = template.open_target(port, "about:blank")
        target_id = target.get("id", "")
        client = template.CdpClient(target["webSocketDebuggerUrl"])
        try:
            return build_summary(template, client)
        finally:
            client.close()
    finally:
        if target_id:
            template.close_target(port, target_id)
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        if profile_dir.exists():
            shutil.rmtree(profile_dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-only", action="store_true", help="rewrite reports from existing summary without a browser run")
    args = parser.parse_args()
    if args.output_only:
        existing = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        summary = existing["summaries"][0]
    else:
        summary = run()
    summary = normalize_existing_summary(summary)
    SUMMARY_PATH.write_text(json.dumps({"summaries": [summary]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_compact_summary(summary)
    write_report(summary)
    print(
        json.dumps(
            {
                "summary": str(SUMMARY_PATH),
                "compact_summary": str(COMPACT_SUMMARY_PATH),
                "report": str(REPORT_PATH),
                "decision": summary.get("decision"),
                "stop_reason": summary.get("stop_reason"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
