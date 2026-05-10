#!/usr/bin/env python3
"""SE/PL/CZ/GR isolated-browser checkout-to-shipping QA.

Uses the existing CDP checkout helper from the prior FR/BE lane, but writes a
separate evidence packet for Sweden, Poland, Czechia, and Greece. It stops at
shipping-rate visibility, never enters payment data, never clicks Pay/Place
order, and never touches admin, ads, catalog, or campaign surfaces.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
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
    / "2026-05-09-paid-growth-fr-be-checkout-safe-advance"
    / "lanes"
    / "checkout-fr-be"
    / "fr_be_checkout_to_shipping.py"
)
RAW_DIR = LANE_DIR / "raw"
SCREENSHOT_DIR = LANE_DIR / "screenshots"
SUMMARY_PATH = LANE_DIR / "se_pl_cz_gr_checkout_to_shipping_summary.json"
COMPACT_SUMMARY_PATH = LANE_DIR / "summary.json"
REPORT_PATH = LANE_DIR / "SE_PL_CZ_GR_CHECKOUT_TO_SHIPPING.md"

MARKETS = {
    "SE": {
        "name": "Sweden",
        "currency": "SEK",
        "province": "",
        "city": "Stockholm",
        "postal_code": "111 30",
        "address1": "Drottninggatan 1",
        "phone": "08 123 456 78",
    },
    "PL": {
        "name": "Poland",
        "currency": "PLN",
        "province": "",
        "city": "Warsaw",
        "postal_code": "00-001",
        "address1": "Marszalkowska 1",
        "phone": "22 123 45 67",
    },
    "CZ": {
        "name": "Czechia",
        "currency": "CZK",
        "province": "",
        "city": "Prague",
        "postal_code": "110 00",
        "address1": "Vaclavske namesti 1",
        "phone": "601 123 456",
    },
    "GR": {
        "name": "Greece",
        "currency": "EUR",
        "province": "",
        "city": "Athens",
        "postal_code": "105 63",
        "address1": "Ermou 1",
        "phone": "21 0123 4567",
    },
}


def load_template() -> Any:
    spec = importlib.util.spec_from_file_location("dlm_checkout_template", TEMPLATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import checkout template: {TEMPLATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.MARKETS = MARKETS
    module.LANE_DIR = LANE_DIR
    module.RAW_DIR = RAW_DIR
    module.SCREENSHOT_DIR = SCREENSHOT_DIR
    module.SUMMARY_PATH = SUMMARY_PATH
    module.REPORT_PATH = REPORT_PATH
    return module


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def status_at(summary: dict[str, Any], key: str) -> int | None:
    value = summary.get("cart_api_probe", {}).get(key, {}).get("status")
    return int(value) if isinstance(value, int) else None


def strict_decision(summary: dict[str, Any]) -> str:
    code = str(summary.get("country_code", ""))
    state = summary.get("checkout_shipping_state", {})
    add_status = status_at(summary, "add")
    cart_status = status_at(summary, "cart")
    rates_status = status_at(summary, "shipping_rates_api")
    status_blocked = any(status == 429 for status in [add_status, cart_status, rates_status])
    blocked = bool(summary.get("blocked_by_verification_text")) or status_blocked
    api_rates = summary.get("api_rates") or []
    api_pass = rates_status == 200 and bool(api_rates)
    ui_pass = bool(
        state.get("has_standard")
        and state.get("has_express")
        and state.get("has_currency")
        and not state.get("has_order_confirmation")
    )
    cart_pass = add_status == 200 and cart_status == 200
    order_created = bool(summary.get("payment_or_order_created") or state.get("has_order_confirmation"))
    if cart_pass and api_pass and ui_pass and not blocked and not order_created:
        return f"{code}_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER"
    if blocked:
        return f"{code}_CHECKOUT_BLOCKED_BY_429_OR_VERIFICATION_NO_BYPASS"
    if order_created:
        return f"{code}_STOP_ORDER_RISK_DETECTED"
    if api_pass and not ui_pass:
        return f"{code}_API_RATES_PASS_CHECKOUT_UI_NOT_CONFIRMED"
    return f"{code}_CHECKOUT_STILL_BLOCKED_OR_RATES_NOT_VISIBLE"


def normalize_summary(summary: dict[str, Any]) -> dict[str, Any]:
    summary["lane"] = "SE/PL/CZ/GR isolated-browser checkout-to-shipping QA"
    summary["problem_id"] = "PROB-2026-05-09-SE-PL-CZ-GR-CHECKOUT-QA"
    summary["mode"] = "PUBLIC_STOREFRONT_ISOLATED_CHROME_NO_PAYMENT_NO_ORDER"
    summary["decision"] = strict_decision(summary)
    summary["guardrails_preserved"] = [
        "no payment data entered",
        "no Pay Now / Place order click",
        "no order creation",
        "no CAPTCHA or verification bypass",
        "no Shopify Admin, theme, product data, Merchant, Google Ads, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal writes",
    ]
    return summary


def money_signal(currency: str, state: dict[str, Any]) -> bool:
    text = " ".join(str(line) for line in state.get("rates_lines", []))
    return bool(re.search(rf"\b{re.escape(currency)}\b|FREE|Free|gratis|kr|z[lł]|K[cč]|EUR|€", text, re.I))


def write_compact_summary(summaries: list[dict[str, Any]], stopped_early: bool) -> None:
    compact = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "problem_id": "PROB-2026-05-09-SE-PL-CZ-GR-CHECKOUT-QA",
        "packet": str(LANE_DIR),
        "stopped_early": stopped_early,
        "markets": [
            {
                "country_code": summary.get("country_code"),
                "decision": summary.get("decision"),
                "cart_add_status": status_at(summary, "add"),
                "cart_read_status": status_at(summary, "cart"),
                "shipping_rates_status": status_at(summary, "shipping_rates_api"),
                "cart_currency": summary.get("cart_currency"),
                "api_rates_pass": summary.get("api_rates_pass"),
                "shipping_ui_pass": summary.get("shipping_ui_pass"),
                "blocked_by_verification_text": summary.get("blocked_by_verification_text"),
                "payment_or_order_created": summary.get("payment_or_order_created"),
                "api_rates": [
                    {
                        "name": rate.get("name") or rate.get("presentment_name"),
                        "price": rate.get("price"),
                        "currency": rate.get("currency"),
                    }
                    for rate in (summary.get("api_rates") or [])
                ],
            }
            for summary in summaries
        ],
    }
    COMPACT_SUMMARY_PATH.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(summaries: list[dict[str, Any]], stopped_early: bool) -> None:
    passed = [s for s in summaries if str(s.get("decision", "")).endswith("PASSED_READONLY_NO_PAYMENT_NO_ORDER")]
    blocked = [s for s in summaries if "BLOCKED" in str(s.get("decision", "")) or "NOT_CONFIRMED" in str(s.get("decision", ""))]
    lines = [
        "# SE/PL/CZ/GR Checkout To Shipping Readback",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Mode: public storefront isolated Chrome profile. No payment data was entered, no Pay Now/Place Order button was clicked, no order was created, and no CAPTCHA or verification bypass was attempted.",
        "",
        "## Result",
        "",
        f"- Markets attempted: `{', '.join(str(s.get('country_code')) for s in summaries)}`",
        f"- Passed checkout-to-shipping for paused infrastructure only: `{', '.join(str(s.get('country_code')) for s in passed) or 'none'}`",
        f"- Needs follow-up: `{', '.join(str(s.get('country_code')) for s in blocked) or 'none'}`",
        f"- Stopped early: `{stopped_early}`",
        "- Live-spend-ready non-US markets remain `0`; passing this lane supports paused infrastructure only.",
        "",
        "| Market | Product/cart presentment | Rates API | Checkout UI | Decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    for summary in summaries:
        state = summary.get("checkout_shipping_state", {})
        rates = summary.get("api_rates") or []
        rate_text = ", ".join(
            f"{rate.get('name') or rate.get('presentment_name')}: {rate.get('price')} {rate.get('currency')}"
            for rate in rates
        ) or "No rates"
        lines.append(
            "| {code} | Cart `{currency}`, add/read `{add}` / `{cart}`, items `{items}` | `{rate_status}`; {rates} | `{lang}`; Standard `{std}`, Express `{exp}`, currency `{cur}`, verification `{verify}`, order `{order}` | `{decision}` |".format(
                code=summary.get("country_code"),
                currency=summary.get("cart_currency"),
                add=status_at(summary, "add"),
                cart=status_at(summary, "cart"),
                items=summary.get("cart_item_count"),
                rate_status=status_at(summary, "shipping_rates_api"),
                rates=rate_text,
                lang=state.get("html_lang", ""),
                std=state.get("has_standard"),
                exp=state.get("has_express"),
                cur=state.get("has_currency") or money_signal(str(MARKETS.get(summary.get("country_code"), {}).get("currency", "")), state),
                verify=summary.get("blocked_by_verification_text"),
                order=summary.get("payment_or_order_created"),
                decision=summary.get("decision"),
            )
        )
    lines.extend(["", "## Details", ""])
    for summary in summaries:
        code = str(summary.get("country_code"))
        product = summary.get("product", {})
        cart_api = summary.get("cart_api_probe", {})
        state = summary.get("checkout_shipping_state", {})
        rates = summary.get("api_rates") or []
        lines.extend(
            [
                f"## {code}",
                "",
                f"Decision: `{summary.get('decision')}`.",
                "",
                "### Product And Cart",
                "",
                f"- Product URL: `{summary.get('product_url')}`",
                f"- Product page title: `{product.get('title', '')}`",
                f"- Product `html lang`: `{product.get('html_lang', '')}`",
                f"- Product currency meta: `{product.get('currency_meta', '')}`",
                f"- Cart clear HTTP status: `{cart_api.get('clear', {}).get('status')}`",
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
            excerpt = clean(cart_api.get("shipping_rates_api", {}).get("text_excerpt", ""))
            lines.append(f"- No rates returned from the API probe. Excerpt: `{excerpt[:300]}`")
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
            "## Evidence",
            "",
            f"- Detailed summary JSON: `{SUMMARY_PATH}`",
            f"- Compact summary JSON: `{COMPACT_SUMMARY_PATH}`",
            f"- Screenshots: `{SCREENSHOT_DIR}`",
            "- Temporary isolated Chrome profiles are deleted after each run so storefront cookies/session data are not persisted in the repo.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--countries", nargs="+", choices=sorted(MARKETS), default=["SE", "PL", "CZ", "GR"])
    parser.add_argument("--delay-seconds", type=int, default=20)
    args = parser.parse_args()
    checkout = load_template()
    summaries: list[dict[str, Any]] = []
    stopped_early = False
    for index, country_code in enumerate(args.countries):
        summary = normalize_summary(checkout.run_country(country_code))
        summaries.append(summary)
        risky = (
            "BLOCKED_BY_429_OR_VERIFICATION" in str(summary.get("decision"))
            or "STOP_ORDER_RISK" in str(summary.get("decision"))
            or bool(summary.get("payment_or_order_created"))
        )
        if risky:
            stopped_early = index < len(args.countries) - 1
            break
        if index < len(args.countries) - 1 and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)
    SUMMARY_PATH.write_text(json.dumps({"summaries": summaries}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_compact_summary(summaries, stopped_early)
    write_report(summaries, stopped_early)
    print(
        json.dumps(
            {
                "summary": str(SUMMARY_PATH),
                "compact_summary": str(COMPACT_SUMMARY_PATH),
                "report": str(REPORT_PATH),
                "stopped_early": stopped_early,
                "decisions": [summary["decision"] for summary in summaries],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
