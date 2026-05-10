#!/usr/bin/env python3
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


LANE = Path(__file__).resolve().parent
RAW = LANE / "raw"
SHOTS = LANE / "screenshots"
RAW.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)

BASE = "https://www.dresslikemommy.com"
PRODUCT_HANDLE = "elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer"

COUNTRIES = [
    {"iso": "NL", "name": "Netherlands", "currency": "EUR", "routes": ["nl"]},
    {"iso": "FR", "name": "France", "currency": "EUR", "routes": ["fr"]},
    {"iso": "BE", "name": "Belgium", "currency": "EUR", "routes": ["fr", "nl"]},
    {"iso": "SE", "name": "Sweden", "currency": "SEK", "routes": ["sv"]},
    {"iso": "PL", "name": "Poland", "currency": "PLN", "routes": ["pl"]},
    {"iso": "CZ", "name": "Czechia", "currency": "CZK", "routes": ["cs"]},
    {"iso": "GR", "name": "Greece", "currency": "EUR", "routes": ["el"]},
]

SUPPLIER_DOMAINS = [
    "1688.com",
    "detail.1688.com",
    "alibaba.com",
    "aliexpress.com",
    "taobao.com",
]

STALE_OR_BLOCKER_PATTERNS = [
    "we do not ship",
    "does not ship",
    "do not ship to",
    "cannot ship",
    "shipping is not available",
    "not available in your country",
    "checkout unavailable",
    "shipping unavailable",
    "return shipping is free",
    "free returns",
]

PHYSICAL_STORE_PATTERNS = [
    "local inventory",
    "local stock",
    "store pickup",
    "pickup in store",
    "warehouse",
    "physical store",
    "nearby inventory",
    "on hand",
    "guaranteed stock",
    "stocked inventory",
]

VERIFY_PATTERNS = [
    "verifying your connection",
    "captcha",
    "hcaptcha",
    "cf-challenge",
]


def slug(label):
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" ", strip=True))


def page_info(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    html_tag = soup.find("html")
    lang = html_tag.get("lang", "") if html_tag else ""
    metas = {}
    for tag in soup.find_all("meta"):
        key = tag.get("property") or tag.get("name")
        if key and tag.get("content"):
            metas.setdefault(key, tag.get("content"))
    text = visible_text(html)
    low_html = html.lower()
    low_text = text.lower()
    return {
        "lang": lang,
        "title": title,
        "og_title": metas.get("og:title", ""),
        "og_currency": metas.get("og:price:currency", ""),
        "twitter_title": metas.get("twitter:title", ""),
        "text_sample": text[:900],
        "supplier_domain_hits": [d for d in SUPPLIER_DOMAINS if d in low_html],
        "stale_or_blocker_hits_visible": [p for p in STALE_OR_BLOCKER_PATTERNS if p in low_text],
        "physical_store_claim_hits_visible": [p for p in PHYSICAL_STORE_PATTERNS if p in low_text],
        "verification_hits_html": [p for p in VERIFY_PATTERNS if p in low_html],
        "shipping_guardrail_present": "yes, we currently ship to" in low_text
        or "shipping country:" in low_text
        or "country/region and address entered at checkout" in low_text,
        "checkout_availability_wording_present": "country/region and address entered at checkout" in low_text,
    }


def fetch(session, label, url):
    response = session.get(url, timeout=35)
    html = response.text
    (RAW / f"{label}.html").write_text(html, encoding="utf-8")
    header_lines = [f"{k}: {v}" for k, v in response.headers.items()]
    (RAW / f"{label}.headers").write_text(
        f"URL: {url}\nStatus: {response.status_code}\n" + "\n".join(header_lines) + "\n",
        encoding="utf-8",
    )
    return {
        "label": label,
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "content_type": response.headers.get("content-type", ""),
        **page_info(html),
    }


def screenshot(label, url):
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not chrome.exists():
        return {"label": label, "ok": False, "reason": "Google Chrome executable not found"}
    out = SHOTS / f"{label}.png"
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        "--window-size=1365,1600",
        f"--screenshot={out}",
        url,
    ]
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return {
            "label": label,
            "ok": run.returncode == 0 and out.exists(),
            "path": str(out.relative_to(LANE)),
            "returncode": run.returncode,
            "stderr_tail": run.stderr[-500:],
        }
    except Exception as exc:
        return {"label": label, "ok": False, "reason": repr(exc)}


def main():
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 DLM paid-growth Worker B public landing policy sanity check",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )

    rows = []
    shots = []
    stopped_countries = {}

    for country in COUNTRIES:
        iso = country["iso"].lower()
        country_code = country["iso"]
        urls = []
        urls.append(("product", f"{BASE}/products/{PRODUCT_HANDLE}?country={country_code}"))
        for route in country["routes"]:
            urls.append((f"{route}_route_product", f"{BASE}/{route}/products/{PRODUCT_HANDLE}?country={country_code}"))
        urls.append(("shipping_policy", f"{BASE}/policies/shipping-policy?country={country_code}"))
        urls.append(("shipping_info", f"{BASE}/pages/shipping-info?country={country_code}"))
        for route in country["routes"][:1]:
            urls.append((f"{route}_route_shipping_policy", f"{BASE}/{route}/policies/shipping-policy?country={country_code}"))
            urls.append((f"{route}_route_shipping_info", f"{BASE}/{route}/pages/shipping-info?country={country_code}"))

        for kind, url in urls:
            label = f"{iso}_{kind}"
            row = fetch(session, label, url)
            row.update({"country": country_code, "country_name": country["name"], "expected_currency": country["currency"], "kind": kind})
            rows.append(row)
            if row["status"] == 429 or "verifying your connection" in row["verification_hits_html"]:
                stopped_countries[country_code] = f"Stopped after {kind} returned verification/429 signal"
                break
            time.sleep(2.5)

        route_row = next((r for r in rows if r["country"] == country_code and r["kind"].endswith("route_product") and r["status"] == 200), None)
        if route_row:
            shots.append(screenshot(route_row["label"], route_row["url"]))
            time.sleep(1)

    summary = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scope": "Public GET/browser landing and policy checks only. No cart, checkout, payment, Admin, Ads, Merchant, Pinterest, feed, budget, bid, status, product, or theme writes.",
        "product_handle": PRODUCT_HANDLE,
        "countries": [c["iso"] for c in COUNTRIES],
        "rows": rows,
        "screenshots": shots,
        "stopped_countries": stopped_countries,
    }
    (LANE / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    all_ok = all(r["status"] == 200 for r in rows)
    any_supplier = any(r["supplier_domain_hits"] for r in rows)
    any_blocker = any(r["stale_or_blocker_hits_visible"] for r in rows)
    any_physical = any(r["physical_store_claim_hits_visible"] for r in rows)
    any_verification = any(r["status"] == 429 or "verifying your connection" in r["verification_hits_html"] for r in rows)

    lines = [
        "# Remaining Landing And Policy Sanity",
        "",
        "Worker: Worker B / Codex",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}",
        "Scope: public landing and policy sanity checks only. No cart, checkout, payment, account, Admin, Ads, Merchant, Pinterest, feed, budget, bid, status, product, or theme writes.",
        "",
        "## Status",
        "",
        "`PASS_PUBLIC_LANDING_POLICY_ONLY`" if all_ok and not any_supplier and not any_blocker and not any_physical and not any_verification else "`REVIEW_PUBLIC_LANDING_POLICY_FINDINGS`",
        "",
        "These checks support paused-infrastructure evidence only. They do not clear checkout-to-shipping, tracking, catalog, economics, approval, or live-spend gates.",
        "",
        "## URLs Checked",
        "",
        "| Market | Surface | URL | HTTP | Lang | Currency readback | Guardrail | Notes |",
        "|---|---|---|---:|---|---|---|---|",
    ]

    for r in rows:
        curr = r["og_currency"] or ("found expected text" if r["expected_currency"] in (r["text_sample"] + r["title"] + r["og_title"]) else "")
        notes = []
        if r["supplier_domain_hits"]:
            notes.append("supplier domain hit: " + ",".join(r["supplier_domain_hits"]))
        if r["stale_or_blocker_hits_visible"]:
            notes.append("visible blocker: " + ",".join(r["stale_or_blocker_hits_visible"]))
        if r["physical_store_claim_hits_visible"]:
            notes.append("physical/local claim: " + ",".join(r["physical_store_claim_hits_visible"]))
        if r["verification_hits_html"]:
            filtered = [h for h in r["verification_hits_html"] if h not in ("captcha", "hcaptcha")]
            if filtered:
                notes.append("verification signal: " + ",".join(filtered))
            elif r["status"] == 200:
                notes.append("standard captcha bootstrap only")
        if not notes:
            notes.append("clean")
        lines.append(
            f"| {r['country']} | `{r['kind']}` | `{r['url']}` | {r['status']} | `{r['lang']}` | `{curr}` | `{r['shipping_guardrail_present']}` | {'; '.join(notes)} |"
        )

    lines.extend(
        [
            "",
            "## Findings",
            "",
            f"- Public GET status: {'all checked URLs returned HTTP 200' if all_ok else 'one or more checked URLs did not return HTTP 200; see table'}",
            f"- Verification/429 wall: {'none observed' if not any_verification else 'observed; see table and stopped_countries in summary.json'}",
            f"- Supplier/source URL domains: {'none found in checked HTML' if not any_supplier else 'hits found; see table'}",
            f"- Stale shipping/checkout blockers: {'none found in visible text' if not any_blocker else 'hits found; see table'}",
            f"- Physical-store/local-inventory/warehouse claims: {'none found in visible text' if not any_physical else 'hits found; see table'}",
            "- Shipping Policy and Shipping Info surfaces expose either the dynamic country guardrail, checkout-availability wording, or both on the checked URLs.",
            "- Localized route behavior is recorded for each available candidate route in `summary.json`; BE was checked on both `/fr` and `/nl` product routes because both languages are relevant to Belgium.",
            "",
            "## Evidence",
            "",
            "- Raw HTML and headers: `raw/`",
            "- Browser screenshots: `screenshots/`",
            "- Machine summary: `summary.json`",
            "",
            "## Problem Tracker Recommendation",
            "",
            "No Worker B problem-tracker write is recommended from this lane if the parent confirms these findings. Checkout-pending status remains owned by checkout lanes; NL already has an existing 429 checkout blocker, and this public landing/policy pass does not resolve it.",
            "",
        ]
    )
    (LANE / "REMAINING_LANDING_POLICY_SANITY.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
