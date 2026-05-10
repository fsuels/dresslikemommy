#!/usr/bin/env python3
"""NL checkout UI country/rates confirmation.

Single low-volume public storefront pass in an isolated Chrome profile. The
runner fills only non-payment contact/delivery fields, never enters payment
data, never clicks Pay Now / Place Order / Complete Order, and stops on 429,
verification, CAPTCHA, payment-risk, or order-risk signals.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import time
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
SUMMARY_PATH = LANE_DIR / "nl_ui_country_confirmation_summary.json"
COMPACT_SUMMARY_PATH = LANE_DIR / "summary.json"
REPORT_PATH = LANE_DIR / "NL_UI_COUNTRY_CONFIRMATION.md"

COUNTRY_CODE = "NL"
PRODUCT_URL = (
    "https://www.dresslikemommy.com/products/"
    "elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits"
    "?variant=41878479831137&country=NL"
)
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
    spec = importlib.util.spec_from_file_location("dlm_checkout_template", TEMPLATE_PATH)
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
    return bool(
        re.search(
            r"verifying your connection|protected by hcaptcha|hcaptcha|captcha|checking your browser|are you human",
            clean(value),
            re.I,
        )
    )


def has_order_signal(url: object, text: object) -> bool:
    return bool(
        re.search(r"/thank_you|/orders/", str(url or ""), re.I)
        or re.search(r"thank you for your purchase|your order is confirmed|order confirmed", clean(text), re.I)
    )


def status_of(step: dict[str, Any] | None) -> int | None:
    status = (step or {}).get("status")
    return int(status) if isinstance(status, int) else None


def fetch_step(template: Any, client: Any, name: str, path: str, options: dict[str, Any], timeout: int = 45) -> dict[str, Any]:
    result = template.page_fetch(client, path, options, timeout)
    result["step"] = name
    return result


def redacted_snapshot(template: Any, client: Any, screenshot_name: str) -> dict[str, Any]:
    snap = template.snapshot(client)
    snap["screenshot"] = template.save_screenshot(client, screenshot_name)
    snap["url"] = template.redacted_url(snap.get("url", ""))
    return snap


def stop_reason_for_step(step_name: str, step: dict[str, Any]) -> str | None:
    if status_of(step) == 429:
        return f"STOP_HTTP_429_AT_{step_name.upper()}"
    if has_verification_text(step.get("text_excerpt", "")):
        return f"STOP_VERIFICATION_TEXT_AT_{step_name.upper()}"
    return None


def stop_reason_for_snapshot(label: str, snapshot: dict[str, Any]) -> str | None:
    if has_verification_text(snapshot.get("text", "") or snapshot.get("text_excerpt", "")):
        return f"STOP_VERIFICATION_TEXT_ON_{label.upper()}"
    if has_order_signal(snapshot.get("url", ""), snapshot.get("text", "") or snapshot.get("text_excerpt", "")):
        return f"STOP_ORDER_CONFIRMATION_SIGNAL_ON_{label.upper()}"
    return None


def fill_non_payment_checkout_fields(template: Any, client: Any) -> dict[str, Any]:
    data = {
        "email": f"dlm-nl-ui-readonly-{int(time.time())}@example.com",
        "first_name": "Readonly",
        "last_name": "QA",
        "address1": MARKET["address1"],
        "city": MARKET["city"],
        "postal_code": MARKET["postal_code"],
        "phone": MARKET["phone"],
        "country_name": MARKET["name"],
        "country_code": COUNTRY_CODE,
    }
    expression = r"""
      (async () => {
        const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
        const data = __DATA__;
        const events = [];
        const all = () => [...document.querySelectorAll('input, textarea, select')];
        const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
        const labelFor = el => {
          const label = el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`) : null;
          return [
            el.name, el.id, el.autocomplete, el.placeholder, el.getAttribute('aria-label'),
            el.getAttribute('data-testid'), label?.innerText
          ].filter(Boolean).join(' ').toLowerCase();
        };
        const isPayment = el => {
          const label = labelFor(el);
          return /(card|cc-|credit|debit|expiration|expiry|security code|cvv|cvc|payment|name on card|paypal|shop pay|crypto|klarna)/i.test(label);
        };
        const allowedTextInput = el => {
          const type = (el.type || '').toLowerCase();
          return visible(el) && !el.disabled && !el.readOnly && !isPayment(el)
            && !['hidden', 'checkbox', 'radio', 'submit', 'button', 'password'].includes(type);
        };
        const setValue = (el, value) => {
          if (!el) return false;
          el.scrollIntoView({block: 'center', inline: 'nearest'});
          el.focus();
          const setter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value')?.set;
          if (setter) setter.call(el, value); else el.value = value;
          el.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: value}));
          el.dispatchEvent(new Event('change', {bubbles: true}));
          el.blur();
          return true;
        };
        const fill = (name, predicate, value) => {
          const el = all().find(candidate => allowedTextInput(candidate) && predicate(candidate, labelFor(candidate)));
          const ok = setValue(el, value);
          events.push({field: name, ok, tag: el?.tagName || '', type: el?.type || '', name_attr: el?.name || '', id: el?.id || '', autocomplete: el?.autocomplete || ''});
          return ok;
        };
        const countrySelect = all().find(el => el.tagName === 'SELECT' && visible(el) && !el.disabled && /country|region/i.test(labelFor(el)));
        let countrySelectedText = '';
        if (countrySelect) {
          const option = [...countrySelect.options].find(opt => {
            const text = (opt.textContent || '').trim();
            return text.toLowerCase() === data.country_name.toLowerCase() || opt.value.toLowerCase() === data.country_code.toLowerCase();
          });
          const ok = setValue(countrySelect, option ? option.value : data.country_code);
          countrySelectedText = countrySelect.options[countrySelect.selectedIndex]?.textContent || countrySelect.value || '';
          events.push({field: 'country', ok, tag: 'SELECT', name_attr: countrySelect.name || '', id: countrySelect.id || '', selected_value: countrySelect.value || '', selected_text: countrySelectedText});
          await sleep(1500);
        } else {
          events.push({field: 'country', ok: false, reason: 'country_select_not_found'});
        }

        fill('email', (el, label) => el.autocomplete === 'email' || /\bemail\b/.test(label), data.email);
        fill('first_name', (el, label) => /given-name|first name|firstname/.test(label), data.first_name);
        fill('last_name', (el, label) => /family-name|last name|lastname/.test(label), data.last_name);
        fill('address1', (el, label) => /address-line1|address1|address line 1|\baddress\b/.test(label), data.address1);
        fill('postal_code', (el, label) => /postal-code|postal|postcode|zip/.test(label), data.postal_code);
        fill('city', (el, label) => /address-level2|\bcity\b|locality/.test(label), data.city);
        fill('phone', (el, label) => (el.autocomplete === 'tel' || /\bphone\b|\btel\b/.test(label)) && !/\bemail\b/.test(label), data.phone);
        await sleep(8000);

        const text = document.body ? document.body.innerText : '';
        const paymentFieldsWithValue = all().filter(el => {
          const type = (el.type || '').toLowerCase();
          return visible(el) && isPayment(el) && !['radio', 'checkbox', 'hidden', 'submit', 'button'].includes(type) && String(el.value || '').trim();
        }).map(el => ({
          tag: el.tagName,
          name_attr: el.name || '',
          id: el.id || '',
          autocomplete: el.autocomplete || '',
          value_length: String(el.value || '').length
        }));
        return {
          events,
          url: location.href,
          title: document.title || '',
          html_lang: document.documentElement.lang || '',
          text,
          country_selected_text: countrySelectedText,
          payment_fields_with_value: paymentFieldsWithValue,
          clicked_buttons: []
        };
      })()
    """.replace("__DATA__", json.dumps(data))
    result = template.runtime_eval(client, expression, 90)
    return result if isinstance(result, dict) else {"runtime_result": result}


def collect_checkout_state(template: Any, client: Any) -> dict[str, Any]:
    expression = r"""
      (() => {
        const text = document.body ? document.body.innerText : '';
        const lines = text.split(/\n+/).map(line => line.trim()).filter(Boolean);
        const moneyPattern = /(EUR|€\s*\d|FREE|GRATIS)/i;
        const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
        const labelFor = el => {
          const label = el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`) : null;
          return [
            el.name, el.id, el.autocomplete, el.placeholder, el.getAttribute('aria-label'),
            el.getAttribute('data-testid'), label?.innerText
          ].filter(Boolean).join(' ').toLowerCase();
        };
        const visibleInputs = [...document.querySelectorAll('input, select, textarea')].filter(visible).map(el => ({
          tag: el.tagName,
          type: el.type || '',
          name: el.name || '',
          id: el.id || '',
          autocomplete: el.autocomplete || '',
          label: labelFor(el),
          value: el.tagName === 'SELECT' ? (el.options[el.selectedIndex]?.textContent || el.value || '') : (el.value ? '[FILLED]' : ''),
          raw_value: el.tagName === 'SELECT' ? (el.value || '') : '',
          disabled: !!el.disabled
        })).slice(0, 100);
        const countryFields = visibleInputs.filter(row => /country|region/.test(row.label));
        const rates = [];
        for (let i = 0; i < lines.length; i++) {
          if (/(standard|express).*delivery/i.test(lines[i])) {
            let price = '';
            for (let j = i + 1; j < Math.min(lines.length, i + 5); j++) {
              if (moneyPattern.test(lines[j])) {
                price = lines[j];
                break;
              }
            }
            rates.push({name: lines[i], price});
          }
        }
        const buttons = [...document.querySelectorAll('button, input[type="submit"]')].filter(visible).map(el => ({
          text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim(),
          disabled: !!el.disabled
        })).slice(0, 50);
        return {
          title: document.title || '',
          url: location.href,
          html_lang: document.documentElement.lang || '',
          text_excerpt: text.slice(0, 9000),
          rates_lines: lines.filter(line => /(standard|express|delivery|shipping|EUR|€|FREE|GRATIS|country\/region|netherlands)/i.test(line)).slice(0, 100),
          parsed_rates: rates,
          buttons,
          visible_inputs: visibleInputs,
          country_fields: countryFields,
          selected_netherlands_confirmed: countryFields.some(row => /netherlands/i.test(row.value) || /^NL$/i.test(row.raw_value)),
          has_standard: /standard delivery/i.test(text),
          has_express: /express delivery/i.test(text),
          has_currency: /\bEUR\b|€\s*\d|FREE|GRATIS/i.test(text),
          has_pay_now: /(pay now|place order|complete order)/i.test(text),
          has_order_confirmation: /\/thank_you|\/orders\//i.test(location.href) || /(thank you for your purchase|your order is confirmed|order confirmed)/i.test(text),
          has_verification_text: /(verifying your connection|protected by hcaptcha|hcaptcha|captcha|checking your browser|are you human)/i.test(text)
        };
      })()
    """
    state = template.runtime_eval(client, expression, 30)
    if not isinstance(state, dict):
        state = {"runtime_state_result": state}
    state["url"] = template.redacted_url(state.get("url", ""))
    state["screenshot"] = template.save_screenshot(client, "nl-checkout-country-rates-confirmed.png")
    return state


def summarize_decision(summary: dict[str, Any]) -> str:
    if summary.get("payment_or_order_created"):
        return "NL_UI_STOP_ORDER_RISK_DETECTED"
    if summary.get("payment_text_fields_with_value_count", summary.get("payment_fields_with_value_count")):
        return "NL_UI_STOP_PAYMENT_FIELD_VALUE_DETECTED"
    if summary.get("blocked_by_verification_text"):
        return "NL_UI_STOP_VERIFICATION_NO_BYPASS"
    if summary.get("stop_reason"):
        return str(summary["stop_reason"])
    state = summary.get("checkout_shipping_state", {})
    if (
        summary.get("checkout_reached")
        and state.get("selected_netherlands_confirmed")
        and state.get("has_standard")
        and state.get("has_express")
        and state.get("has_currency")
    ):
        return "NL_UI_COUNTRY_AND_SHIPPING_RATES_CONFIRMED_NO_PAYMENT_NO_ORDER"
    if summary.get("checkout_reached"):
        return "NL_UI_CHECKOUT_REACHED_COUNTRY_OR_RATES_NOT_CONFIRMED"
    return "NL_UI_CHECKOUT_NOT_REACHED"


def build_summary(template: Any, client: Any) -> dict[str, Any]:
    stop_reason = ""
    cart_api: dict[str, Any] = {}
    product: dict[str, Any] = {}
    cart: dict[str, Any] = {}
    checkout_click: dict[str, Any] = {}
    checkout_entry: dict[str, Any] = {}
    fill_result: dict[str, Any] = {}
    checkout_state: dict[str, Any] = {}

    client.call("Page.enable")
    client.call("Runtime.enable")
    client.call("Network.enable", {"maxTotalBufferSize": 20_000_000, "maxResourceBufferSize": 10_000_000})

    template.navigate(client, PRODUCT_URL)
    product = redacted_snapshot(template, client, "nl-product.png")
    stop_reason = stop_reason_for_snapshot("product", product) or ""

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
        stop_reason = stop_reason_for_step("cart_add", add) or ""

    if not stop_reason:
        cart_read = fetch_step(template, client, "cart_read", "/cart.js", {"method": "GET", "credentials": "include"})
        cart_api["cart"] = cart_read
        stop_reason = stop_reason_for_step("cart_read", cart_read) or ""

    if not stop_reason:
        template.navigate(client, f"{template.BASE_URL}/cart")
        cart = redacted_snapshot(template, client, "nl-cart-before-checkout.png")
        stop_reason = stop_reason_for_snapshot("cart", cart) or ""

    if not stop_reason:
        checkout_click = template.click_checkout(client)
        time.sleep(8)
        template.wait_for_load(client, 45)
        checkout_entry = redacted_snapshot(template, client, "nl-checkout-entry.png")
        stop_reason = stop_reason_for_snapshot("checkout_entry", checkout_entry) or ""

    if not stop_reason:
        fill_result = fill_non_payment_checkout_fields(template, client)
        time.sleep(8)
        checkout_state = collect_checkout_state(template, client)
        stop_reason = stop_reason_for_snapshot("checkout_state", checkout_state) or ""

    if stop_reason and not checkout_state:
        checkout_state = collect_checkout_state(template, client) if checkout_entry else {
            "screenshot": template.save_screenshot(client, "nl-stop-page.png"),
            "url": template.redacted_url((cart or product).get("url", "")),
            "text_excerpt": clean((cart or product).get("text", ""))[:9000],
        }

    cart_json = cart_api.get("cart", {}).get("json") if isinstance(cart_api.get("cart"), dict) else {}
    fill_text = fill_result.get("text", "") if isinstance(fill_result, dict) else ""
    checkout_text = checkout_state.get("text_excerpt", "") if isinstance(checkout_state, dict) else ""
    payment_fields_with_value = fill_result.get("payment_fields_with_value", []) if isinstance(fill_result, dict) else []
    payment_text_fields_with_value = [
        field
        for field in payment_fields_with_value
        if not (str(field.get("name_attr", "")) == "basic" and str(field.get("id", "")).startswith("basic-"))
    ]
    payment_or_order_created = has_order_signal(checkout_state.get("url", ""), checkout_text) or bool(
        checkout_state.get("has_order_confirmation")
    )
    blocked = any(
        has_verification_text(step.get("text_excerpt", ""))
        for step in cart_api.values()
        if isinstance(step, dict)
    ) or any(
        has_verification_text(value)
        for value in [product.get("text", ""), cart.get("text", ""), checkout_entry.get("text", ""), fill_text, checkout_text]
    )

    summary = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "lane": "Worker NL-UI isolated public checkout country confirmation",
        "mode": "SINGLE_PUBLIC_STOREFRONT_ISOLATED_CHROME_NON_PAYMENT_FIELDS_ONLY",
        "product_url": PRODUCT_URL,
        "variant_id": template.VARIANT_ID,
        "address": {
            "country": MARKET["name"],
            "province": MARKET["province"],
            "city": MARKET["city"],
            "postal_code": MARKET["postal_code"],
        },
        "guardrails_preserved": [
            "exactly one low-volume public Netherlands checkout UI confirmation pass",
            "isolated Chrome profile",
            "no account tabs",
            "no CAPTCHA or verification bypass",
            "only non-payment checkout address/contact fields filled",
            "no payment data entered",
            "no Pay Now / Place Order / Complete Order click",
            "no order creation",
            "no Shopify Admin, theme, product data, Google Ads, Merchant, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal writes",
        ],
        "stop_reason": stop_reason,
        "product": product,
        "cart_api_probe": cart_api,
        "cart": cart,
        "checkout_click": checkout_click,
        "checkout_entry": checkout_entry,
        "fill_result": {
            **{key: value for key, value in fill_result.items() if key != "text"},
            "text_excerpt": clean(fill_text)[:2000],
            "url": template.redacted_url(fill_result.get("url", "")) if isinstance(fill_result, dict) else "",
        },
        "checkout_shipping_state": checkout_state,
        "cart_currency": cart_json.get("currency") if isinstance(cart_json, dict) else "",
        "cart_item_count": cart_json.get("item_count") if isinstance(cart_json, dict) else None,
        "checkout_reached": bool(checkout_entry),
        "blocked_by_verification_text": blocked,
        "payment_fields_with_value_count": len(payment_fields_with_value),
        "payment_text_fields_with_value_count": len(payment_text_fields_with_value),
        "payment_method_default_values_count": len(payment_fields_with_value) - len(payment_text_fields_with_value),
        "payment_or_order_created": payment_or_order_created,
    }
    summary["decision"] = summarize_decision(summary)
    return summary


def compact_summary(summary: dict[str, Any]) -> dict[str, Any]:
    state = summary.get("checkout_shipping_state", {})
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "packet": str(LANE_DIR),
        "decision": summary.get("decision"),
        "stop_reason": summary.get("stop_reason"),
        "country_code": COUNTRY_CODE,
        "product_reached": bool(summary.get("product")),
        "cart_add_status": status_of(summary.get("cart_api_probe", {}).get("add")),
        "cart_read_status": status_of(summary.get("cart_api_probe", {}).get("cart")),
        "cart_currency": summary.get("cart_currency"),
        "cart_item_count": summary.get("cart_item_count"),
        "checkout_reached": summary.get("checkout_reached"),
        "checkout_html_lang": state.get("html_lang"),
        "selected_netherlands_confirmed_in_checkout": state.get("selected_netherlands_confirmed"),
        "checkout_shipping_ui_pass": bool(state.get("has_standard") and state.get("has_express") and state.get("has_currency")),
        "ui_rates": state.get("parsed_rates", []),
        "pay_now_visible_but_not_clicked": state.get("has_pay_now"),
        "payment_fields_with_value_count": summary.get("payment_fields_with_value_count"),
        "payment_text_fields_with_value_count": summary.get(
            "payment_text_fields_with_value_count", summary.get("payment_fields_with_value_count")
        ),
        "payment_method_default_values_count": summary.get("payment_method_default_values_count", 0),
        "payment_or_order_created": summary.get("payment_or_order_created"),
        "blocked_by_verification_text": summary.get("blocked_by_verification_text"),
        "screenshots": {
            "product": summary.get("product", {}).get("screenshot"),
            "cart": summary.get("cart", {}).get("screenshot"),
            "checkout_entry": summary.get("checkout_entry", {}).get("screenshot"),
            "checkout_rates": state.get("screenshot"),
        },
    }


def write_outputs(summary: dict[str, Any]) -> None:
    SUMMARY_PATH.write_text(json.dumps({"summaries": [summary]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = compact_summary(summary)
    COMPACT_SUMMARY_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summary, compact)


def write_report(summary: dict[str, Any], compact: dict[str, Any]) -> None:
    product = summary.get("product", {})
    cart_api = summary.get("cart_api_probe", {})
    state = summary.get("checkout_shipping_state", {})
    fill_result = summary.get("fill_result", {})
    product_presentment_ok = bool(re.search(r"Netherlands\s*\|\s*EUR|EUR\s*€|€", product.get("text", ""), re.I))
    lines = [
        "# NL UI Country Confirmation",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Mode: exactly one low-volume public Netherlands checkout UI confirmation pass in an isolated Chrome profile. Only non-payment checkout address/contact fields were filled. No account tabs were used, no payment data was entered, no Pay Now / Place Order / Complete Order button was clicked, no order was created, and no CAPTCHA or verification bypass was attempted.",
        "",
        "## Decision",
        "",
        f"- Decision: `{summary.get('decision')}`",
        f"- Stop reason: `{summary.get('stop_reason') or 'none'}`",
        f"- Blocked by verification text/CAPTCHA: `{summary.get('blocked_by_verification_text')}`",
        f"- Payment/order created: `{summary.get('payment_or_order_created')}`",
        f"- Payment text/card fields with value after fill: `{compact.get('payment_text_fields_with_value_count')}`",
        f"- Payment-method default radio values observed: `{compact.get('payment_method_default_values_count')}`",
        f"- Pay Now visible but not clicked: `{compact.get('pay_now_visible_but_not_clicked')}`",
        "",
        "## Exact Statuses",
        "",
        f"- Product reached: `{compact.get('product_reached')}`",
        f"- Cart add HTTP status: `{compact.get('cart_add_status')}`",
        f"- Cart read HTTP status: `{compact.get('cart_read_status')}`",
        f"- Cart item count: `{compact.get('cart_item_count')}`",
        f"- Cart currency: `{compact.get('cart_currency')}`",
        f"- Checkout reached: `{compact.get('checkout_reached')}`",
        f"- Checkout `html lang`: `{compact.get('checkout_html_lang')}`",
        f"- Selected Netherlands confirmed in checkout UI: `{compact.get('selected_netherlands_confirmed_in_checkout')}`",
        f"- Checkout shipping UI pass: `{compact.get('checkout_shipping_ui_pass')}`",
        "",
        "## Product And Checkout Context",
        "",
        f"- Product URL: `{summary.get('product_url')}`",
        f"- Product page title: `{product.get('title', '')}`",
        f"- Product `html lang`: `{product.get('html_lang', '')}`",
        f"- Product currency meta: `{product.get('currency_meta', '')}`",
        f"- Product presentment includes Netherlands/EUR signal: `{product_presentment_ok}`",
        f"- Checkout URL redacted: `{state.get('url', '')}`",
        "",
        "## Filled Non-Payment Fields",
        "",
    ]
    for event in fill_result.get("events", []):
        lines.append(
            f"- `{event.get('field')}` ok=`{event.get('ok')}` tag=`{event.get('tag', '')}` autocomplete=`{event.get('autocomplete', '')}` selected=`{event.get('selected_text', '')}`"
        )
    lines.extend(["", "## Rates Visible In Checkout UI", ""])
    rates = compact.get("ui_rates") or []
    if rates:
        lines.extend(["| Rate | UI price |", "| --- | --- |"])
        for rate in rates:
            lines.append(f"| `{rate.get('name')}` | `{rate.get('price')}` |")
    else:
        lines.append("- No UI rates parsed.")
    lines.extend(["", "Relevant visible lines:", ""])
    for line in state.get("rates_lines", [])[:80]:
        lines.append(f"- `{clean(line)}`")
    lines.extend(
        [
            "",
            "## No-Payment / No-Order Proof",
            "",
            "- The fill routine targets only `country`, `email`, `first_name`, `last_name`, `address1`, `postal_code`, `city`, and `phone`.",
            "- The runner records `clicked_buttons: []`; it does not click Continue, Pay Now, Place Order, Complete Order, wallet buttons, or payment methods.",
            f"- Payment text/card fields with values after the fill: `{compact.get('payment_text_fields_with_value_count')}`.",
            f"- Shopify payment-method radio/default values observed but not clicked/changed: `{compact.get('payment_method_default_values_count')}`.",
            f"- Order confirmation URL/text detected: `{summary.get('payment_or_order_created')}`.",
            f"- CAPTCHA/verification text detected: `{summary.get('blocked_by_verification_text')}`.",
            "",
            "## Evidence",
            "",
            f"- Detailed summary JSON: `{SUMMARY_PATH}`",
            f"- Compact summary JSON: `{COMPACT_SUMMARY_PATH}`",
            f"- Screenshots directory: `{SCREENSHOT_DIR}`",
            "- Temporary isolated Chrome profile was deleted after the run.",
            "",
            "## Residual Risks",
            "",
            "- This is one low-volume public UI pass at one point in time; Shopify/checkout caching, payment-provider rendering, and market settings can change later.",
            "- No live settings were changed and no payment attempt was made, so this confirms UI country/rate visibility only, not end-to-end order completion.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_browser_pass() -> dict[str, Any]:
    template = load_template()
    profile_dir = RAW_DIR / "chrome-nl-ui-isolated-profile"
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


def normalize_summary(summary: dict[str, Any]) -> dict[str, Any]:
    fill_result = summary.get("fill_result", {})
    payment_fields = fill_result.get("payment_fields_with_value", []) if isinstance(fill_result, dict) else []
    payment_text_fields = [
        field
        for field in payment_fields
        if not (str(field.get("name_attr", "")) == "basic" and str(field.get("id", "")).startswith("basic-"))
    ]
    summary["payment_fields_with_value_count"] = len(payment_fields)
    summary["payment_text_fields_with_value_count"] = len(payment_text_fields)
    summary["payment_method_default_values_count"] = len(payment_fields) - len(payment_text_fields)
    summary["decision"] = summarize_decision(summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-only", action="store_true", help="rewrite reports from existing summary without browser traffic")
    args = parser.parse_args()
    if args.output_only:
        existing = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
        summary = existing["summaries"][0]
    else:
        summary = run_browser_pass()
    summary = normalize_summary(summary)
    write_outputs(summary)
    print(json.dumps(compact_summary(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
