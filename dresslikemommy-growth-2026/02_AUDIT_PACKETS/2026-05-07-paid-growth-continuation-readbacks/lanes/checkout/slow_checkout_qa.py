#!/usr/bin/env python3
"""Slow, no-payment storefront checkout QA for selected countries.

This lane-local helper only reads the public storefront and Shopify cart
shipping-rate endpoint. It does not submit payment, create orders, change
checkout settings, or write Shopify data.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
from datetime import datetime
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib import error, parse, request


BASE_URL = "https://www.dresslikemommy.com"
DEFAULT_PAID_COHORT = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv"
)
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent

COUNTRIES: dict[str, dict[str, str]] = {
    "NL": {
        "name": "Netherlands",
        "locale": "nl",
        "language": "Dutch",
        "currency": "EUR",
        "zip": "1012 AB",
        "city": "Amsterdam",
        "province": "",
    },
    "ES": {
        "name": "Spain",
        "locale": "es",
        "language": "Spanish",
        "currency": "EUR",
        "zip": "28013",
        "city": "Madrid",
        "province": "Comunidad de Madrid",
    },
    "IT": {
        "name": "Italy",
        "locale": "it",
        "language": "Italian",
        "currency": "EUR",
        "zip": "00118",
        "city": "Rome",
        "province": "Roma",
    },
    "RO": {
        "name": "Romania",
        "locale": "ro",
        "language": "Romanian",
        "currency": "EUR",
        "zip": "010011",
        "city": "Bucharest",
        "province": "București",
    },
    "PT": {
        "name": "Portugal",
        "locale": "pt-BR",
        "language": "Portuguese (Brazil)",
        "currency": "EUR",
        "zip": "1100-148",
        "city": "Lisbon",
        "province": "Lisboa",
    },
}

POLICY_LIMIT_PATTERNS = (
    r"only\s+(?:to\s+)?(?:the\s+)?(?:united states|u\.s\.|canada|united kingdom|uk|australia)",
    r"currently\s+ship\s+(?:only\s+)?to",
    r"ship\s+to\s+the\s+united states,\s*canada,\s*the\s+united kingdom,\s*and\s*australia",
    r"united states,\s*canada,\s*united kingdom,\s*and\s*australia",
    r"familias\s+de\s+todo\s+el\s+mundo",
    r"a\s+d[oó]nde\s+enviamos\s+estados\s+unidos",
    r"no\s+encuentras\s+tu\s+pa[ií]s",
    r"famiglie\s+in\s+tutto\s+il\s+mondo",
    r"famiglie\s+di\s+tutto\s+il\s+mondo",
    r"attualmente\s+spediamo\s+a",
    r"non\s+(?:vedi|riesci\s+a\s+trovare)\s+il\s+tuo\s+paese",
    r"familiilor\s+din\s+(?:î|i)ntreaga\s+lume",
    r"familii\s+din\s+(?:î|i)ntreaga\s+lume",
    r"unde\s+livr[aă]m\s+statele\s+unite",
    r"(?:ț|t)ara\s+ta\s+nu\s+este\s+pe\s+list[aă]",
    r"fam[ií]lias\s+em\s+todo\s+o\s+mundo",
    r"para\s+onde\s+enviamos\s+estados\s+unidos",
    r"n[aã]o\s+v[eê]\s+seu\s+pa[ií]s",
)


def now_stamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def strip_html(body: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", body)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return clean(html.unescape(text))


def redact_cart_tokens(body: str) -> str:
    return re.sub(r'("token"\s*:\s*")[^"]+(")', r'\1[REDACTED_CART_TOKEN]\2', body or "")


def read_first_paid_variant(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            variant_id = clean(row.get("shopify_variant_id") or row.get("variant_id"))
            if variant_id:
                row["shopify_variant_id"] = variant_id
                return row
    raise RuntimeError(f"No variant ID found in {path}")


def request_url(
    opener: request.OpenerDirector,
    url: str,
    *,
    data: dict[str, str] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    headers = {
        "Accept": "application/json, text/html, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "DressLikeMommyOps/1.0 (+slow no-payment checkout QA)",
    }
    payload = parse.urlencode(data or {}).encode("utf-8") if data is not None else None
    req = request.Request(
        url,
        data=payload,
        method="POST" if data is not None else "GET",
        headers=headers,
    )
    try:
        with opener.open(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "url": url,
                "final_url": response.geturl(),
                "http_status": response.status,
                "headers": dict(response.headers),
                "body": body,
                "blocker": blocker_for(response.status, body),
            }
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "url": url,
            "final_url": exc.geturl(),
            "http_status": exc.code,
            "headers": dict(exc.headers),
            "body": body,
            "blocker": blocker_for(exc.code, body),
        }
    except Exception as exc:  # noqa: BLE001 - capture probe evidence, do not retry noisily.
        return {
            "url": url,
            "final_url": "",
            "http_status": "",
            "headers": {},
            "body": "",
            "blocker": f"REQUEST_EXCEPTION: {type(exc).__name__}: {exc}",
        }


def blocker_for(status: int | str, body: str) -> str:
    text = body[:8000].lower()
    if status == 429 or "verifying your connection" in text or "captcha" in text:
        return "SHOPIFY_STOREFRONT_BOT_PROTECTION_OR_429"
    return ""


def page_summary(country_code: str, kind: str, response: dict[str, Any]) -> dict[str, Any]:
    body = response.get("body") or ""
    text = strip_html(body)
    html_lang = ""
    title = ""
    currency = ""
    lang_match = re.search(r"<html[^>]+lang=[\"']([^\"']+)[\"']", body, flags=re.I)
    if lang_match:
        html_lang = clean(lang_match.group(1))
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", body)
    if title_match:
        title = clean(html.unescape(title_match.group(1)))
    currency_match = re.search(
        r'<meta\s+property=["\'](?:og:price:currency|product:price:currency)["\']\s+content=["\']([^"\']+)',
        body,
        flags=re.I,
    )
    if currency_match:
        currency = clean(currency_match.group(1)).upper()
    limit_hits = []
    lower_text = text.lower()
    for pattern in POLICY_LIMIT_PATTERNS:
        found = re.search(pattern, lower_text, flags=re.I)
        if found:
            start = max(0, found.start() - 120)
            end = min(len(text), found.end() + 220)
            limit_hits.append(clean(text[start:end]))
    return {
        "country_code": country_code,
        "kind": kind,
        "url": response.get("url"),
        "final_url": response.get("final_url"),
        "http_status": response.get("http_status"),
        "blocker": response.get("blocker"),
        "html_lang": html_lang,
        "title": title,
        "currency_meta": currency,
        "policy_limit_hits": limit_hits[:3],
        "text_excerpt": text[:700],
        "body_excerpt": body[:700],
    }


def build_locale_urls(country_code: str, product_path: str) -> list[tuple[str, str]]:
    locale = COUNTRIES[country_code]["locale"]
    prefix = "/" + locale
    urls = [
        ("home", BASE_URL + prefix),
        ("product", BASE_URL + prefix + product_path),
        ("shipping_info", BASE_URL + prefix + "/pages/shipping-info"),
        ("shipping_policy", BASE_URL + prefix + "/policies/shipping-policy"),
        ("refund_policy", BASE_URL + prefix + "/policies/refund-policy"),
    ]
    if country_code == "PT":
        urls.extend(
            [
                ("pt_home_fallback", BASE_URL + "/pt"),
                ("pt_shipping_info_fallback", BASE_URL + "/pt/pages/shipping-info"),
                ("pt_shipping_policy_fallback", BASE_URL + "/pt/policies/shipping-policy"),
            ]
        )
    return urls


def init_cart(opener: request.OpenerDirector, variant_id: str) -> tuple[bool, list[dict[str, Any]], str]:
    evidence = []
    for endpoint, data in (
        ("/cart/clear.js", {}),
        ("/cart/add.js", {"id": variant_id, "quantity": "1"}),
    ):
        response = request_url(opener, BASE_URL + endpoint, data=data)
        evidence.append(
            {
                "endpoint": endpoint,
                "http_status": response.get("http_status"),
                "blocker": response.get("blocker"),
                "body_excerpt": redact_cart_tokens(response.get("body") or "")[:700],
            }
        )
        if response.get("blocker"):
            return False, evidence, response["blocker"]
        if isinstance(response.get("http_status"), int) and response["http_status"] >= 400:
            return False, evidence, f"CART_INIT_HTTP_{response['http_status']}"
        time.sleep(3)
    return True, evidence, ""


def shipping_rate_probe(
    opener: request.OpenerDirector,
    country_code: str,
    country: dict[str, str],
) -> dict[str, Any]:
    params = {
        "shipping_address[country]": country["name"],
        "shipping_address[zip]": country["zip"],
        "shipping_address[city]": country["city"],
    }
    if country.get("province"):
        params["shipping_address[province]"] = country["province"]
    url = BASE_URL + "/cart/shipping_rates.json?" + parse.urlencode(params)
    response = request_url(opener, url)
    body = response.get("body") or ""
    result: dict[str, Any] = {
        "country_code": country_code,
        "country": country["name"],
        "address": {
            "country": country["name"],
            "city": country["city"],
            "zip": country["zip"],
            "province": country.get("province", ""),
        },
        "url": url,
        "http_status": response.get("http_status"),
        "blocker": response.get("blocker"),
        "status": "BLOCKED" if response.get("blocker") else "FAILED",
        "rates": [],
        "body_excerpt": body[:900],
    }
    if response.get("blocker"):
        return result
    if isinstance(response.get("http_status"), int) and response["http_status"] >= 400:
        return result
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        result["status"] = "FAILED_NON_JSON"
        return result
    rates = payload.get("shipping_rates") or []
    result["rates"] = [
        {
            "name": clean(rate.get("name")),
            "price": clean(rate.get("price")),
            "currency": clean(rate.get("currency")),
            "source": clean(rate.get("source")),
        }
        for rate in rates
    ]
    result["status"] = "RATES_AVAILABLE" if rates else "NO_RATES_RETURNED"
    return result


def markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# Checkout QA - NL / ES / IT / RO / PT",
        "",
        f"Generated: {data['generated_at']}",
        "",
        "## Scope",
        "",
        "- Lane: checkout storefront/checkout QA only.",
        "- Mode: anonymous storefront/cart reads; no payment, no order creation, no Shopify data or checkout setting changes.",
        f"- Delay between public probes: {data['delay_seconds']} seconds.",
        "- Stop rule: stop remaining probes immediately if Shopify storefront bot protection, CAPTCHA, or HTTP 429 appears.",
        "",
        "## Cart Product",
        "",
        f"- Variant ID: `{data['variant']['shopify_variant_id']}`",
        f"- Product: {data['variant'].get('product_title') or ''}",
        f"- Variant: {data['variant'].get('variant_title') or ''}",
        f"- URL: {data['variant'].get('link') or data['variant'].get('product_url') or ''}",
        "",
        "## Outbound Checkout Delivery Rate Results",
        "",
        "| Country | Test address | HTTP | Status | Rates | Blocker |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in data["shipping_rates"]:
        rates = "; ".join(
            f"{rate['name']} {rate['price']} {rate['currency']}".strip()
            for rate in row.get("rates", [])
        )
        address = row.get("address") or {}
        lines.append(
            "| {code} {country} | {city} {zip_code} | {http} | {status} | {rates} | {blocker} |".format(
                code=row["country_code"],
                country=row["country"],
                city=address.get("city", ""),
                zip_code=address.get("zip", ""),
                http=row.get("http_status", ""),
                status=row.get("status", ""),
                rates=rates or "-",
                blocker=row.get("blocker") or "-",
            )
        )
    lines.extend(["", "## Locale / Policy URLs", ""])
    for code, rows in data["pages_by_country"].items():
        country = COUNTRIES[code]
        lines.extend(
            [
                f"### {code} - {country['name']}",
                "",
                f"- Expected storefront language route: `{country['locale']}` ({country['language']})",
                f"- Expected market currency from admin packet: `{country['currency']}`",
                "",
                "| Page | HTTP | HTML lang | Currency meta | URL | Finding |",
                "| --- | ---: | --- | --- | --- | --- |",
            ]
        )
        for page in rows:
            finding_bits = []
            if page.get("blocker"):
                finding_bits.append(page["blocker"])
            if page.get("policy_limit_hits"):
                finding_bits.append("shipping-limited copy detected")
            if not finding_bits:
                finding_bits.append("readable")
            lines.append(
                "| {kind} | {http} | {lang} | {currency} | {url} | {finding} |".format(
                    kind=page["kind"],
                    http=page.get("http_status", ""),
                    lang=page.get("html_lang") or "-",
                    currency=page.get("currency_meta") or "-",
                    url=page.get("final_url") or page.get("url") or "",
                    finding="; ".join(finding_bits),
                )
            )
        limit_pages = [page for page in rows if page.get("policy_limit_hits")]
        if limit_pages:
            lines.extend(["", "Policy/shipping limitation snippets:"])
            for page in limit_pages:
                for hit in page["policy_limit_hits"]:
                    lines.append(f"- `{page['kind']}`: {hit}")
        lines.append("")
    lines.extend(
        [
            "## Findings",
            "",
        ]
    )
    for finding in data["findings"]:
        lines.append(f"- {finding}")
    lines.extend(
        [
            "",
            "## Next Safe Action",
            "",
            data["next_safe_action"],
            "",
            "## Artifacts",
            "",
            "- `slow_checkout_qa.py`",
            "- `checkout_probe_raw.json`",
            "- `CHECKOUT_QA.md`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--paid-cohort", type=Path, default=DEFAULT_PAID_COHORT)
    parser.add_argument("--delay-seconds", type=float, default=12.0)
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    variant = read_first_paid_variant(args.paid_cohort)
    product_url = variant.get("link") or variant.get("product_url") or ""
    product_path = parse.urlparse(product_url).path or "/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set"

    opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))
    pages_by_country: dict[str, list[dict[str, Any]]] = {}
    global_blocker = ""

    for code in COUNTRIES:
        pages_by_country[code] = []
        if global_blocker:
            pages_by_country[code].append(
                {
                    "country_code": code,
                    "kind": "skipped_after_blocker",
                    "url": "",
                    "final_url": "",
                    "http_status": "",
                    "blocker": global_blocker,
                    "html_lang": "",
                    "title": "",
                    "currency_meta": "",
                    "policy_limit_hits": [],
                    "text_excerpt": "Skipped after prior blocker.",
                    "body_excerpt": "",
                }
            )
            continue
        for kind, url in build_locale_urls(code, product_path):
            response = request_url(opener, url)
            summary = page_summary(code, kind, response)
            pages_by_country[code].append(summary)
            if response.get("blocker"):
                global_blocker = response["blocker"]
                break
            time.sleep(args.delay_seconds)

    shipping_rates: list[dict[str, Any]] = []
    cart_evidence: list[dict[str, Any]] = []
    if global_blocker:
        for code, country in COUNTRIES.items():
            shipping_rates.append(
                {
                    "country_code": code,
                    "country": country["name"],
                    "address": {"country": country["name"], "city": country["city"], "zip": country["zip"]},
                    "url": "",
                    "http_status": "",
                    "blocker": global_blocker,
                    "status": "BLOCKED_NOT_RUN",
                    "rates": [],
                    "body_excerpt": "Skipped because locale/page probing hit a storefront blocker.",
                }
            )
    else:
        cart_ok, cart_evidence, cart_blocker = init_cart(opener, variant["shopify_variant_id"])
        if not cart_ok:
            for code, country in COUNTRIES.items():
                shipping_rates.append(
                    {
                        "country_code": code,
                        "country": country["name"],
                        "address": {"country": country["name"], "city": country["city"], "zip": country["zip"]},
                        "url": "",
                        "http_status": "",
                        "blocker": cart_blocker,
                        "status": "BLOCKED_NOT_RUN",
                        "rates": [],
                        "body_excerpt": "Skipped because cart init failed.",
                    }
                )
        else:
            for index, (code, country) in enumerate(COUNTRIES.items()):
                if index:
                    time.sleep(args.delay_seconds)
                row = shipping_rate_probe(opener, code, country)
                shipping_rates.append(row)
                if row.get("blocker"):
                    for remaining_code in list(COUNTRIES)[index + 1 :]:
                        remaining = COUNTRIES[remaining_code]
                        shipping_rates.append(
                            {
                                "country_code": remaining_code,
                                "country": remaining["name"],
                                "address": {
                                    "country": remaining["name"],
                                    "city": remaining["city"],
                                    "zip": remaining["zip"],
                                },
                                "url": "",
                                "http_status": "",
                                "blocker": row["blocker"],
                                "status": "BLOCKED_NOT_RUN_AFTER_PRIOR_BLOCKER",
                                "rates": [],
                                "body_excerpt": "Skipped after prior storefront blocker.",
                            }
                        )
                    break

    rate_pass = [row for row in shipping_rates if row.get("status") == "RATES_AVAILABLE"]
    blocked = [row for row in shipping_rates if clean(row.get("blocker"))]
    no_rates = [row for row in shipping_rates if row.get("status") == "NO_RATES_RETURNED"]
    failed = [
        row
        for row in shipping_rates
        if row.get("status") not in {"RATES_AVAILABLE", "NO_RATES_RETURNED"}
        and not clean(row.get("blocker"))
    ]
    policy_hits = [
        (code, page["kind"])
        for code, rows in pages_by_country.items()
        for page in rows
        if page.get("policy_limit_hits")
    ]
    pt_failures = [
        page
        for page in pages_by_country.get("PT", [])
        if page.get("http_status") and page.get("http_status") != 200
    ]
    pt_failure_summary = ", ".join(
        f"{page['kind']} HTTP {page['http_status']}" for page in pt_failures
    ) or "none"
    policy_hit_summary = ", ".join(f"{code}:{kind}" for code, kind in policy_hits) or "none detected in probed pages"
    failed_summary = ", ".join(
        f"{row['country_code']} HTTP {row.get('http_status')}" for row in failed
    ) or "none"
    findings = [
        f"Live outbound checkout delivery-rate lookup returned rates for {len(rate_pass)} of {len(COUNTRIES)} target countries.",
        f"Countries blocked by storefront rate limit/bot protection: {', '.join(row['country_code'] for row in blocked) or 'none'}.",
        f"Countries with no rates returned: {', '.join(row['country_code'] for row in no_rates) or 'none'}.",
        f"Countries with checkout address/rate validation failures: {failed_summary}.",
        f"Policy/shipping pages with limited-country copy: {policy_hit_summary}.",
        f"Portugal route failures in this run: {pt_failure_summary}.",
    ]
    if rate_pass and not blocked and not no_rates and not failed and len(rate_pass) == len(COUNTRIES):
        shipping_decision = "outbound_checkout_delivery_rates_pass_for_target_countries"
    else:
        shipping_decision = "outbound_checkout_delivery_rates_not_clean_for_all_target_countries"
    if policy_hits:
        policy_decision = "policy_copy_still_blocks_live_paid_expansion"
    else:
        policy_decision = "policy_copy_not_blocked_in_probed_locale_pages"
    next_action = (
        "Keep NL/ES/IT/RO/PT out of live paid spend until the parent integrates this with policy-copy "
        "repair and localized landing-page review. If policy copy is repaired, rerun this lane once, slowly, "
        "and then perform a human browser checkout walkthrough through the shipping step only."
    )

    data = {
        "generated_at": now_stamp(),
        "mode": "READ_ONLY_NO_PAYMENT_CHECKOUT_QA",
        "delay_seconds": args.delay_seconds,
        "paid_cohort_path": str(args.paid_cohort),
        "variant": {
            "shopify_variant_id": variant.get("shopify_variant_id"),
            "product_title": variant.get("product_title"),
            "variant_title": variant.get("variant_title"),
            "link": product_url,
        },
        "countries": COUNTRIES,
        "cart_evidence": cart_evidence,
        "pages_by_country": pages_by_country,
        "shipping_rates": shipping_rates,
        "findings": findings,
        "decision": {
            "shipping": shipping_decision,
            "policy": policy_decision,
            "live_paid_readiness": "NOT_READY_FOR_LIVE_PAID_TRAFFIC",
        },
        "next_safe_action": next_action,
    }
    (output_dir / "checkout_probe_raw.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "CHECKOUT_QA.md").write_text(markdown_report(data), encoding="utf-8")
    print(json.dumps({"output_dir": str(output_dir), "decision": data["decision"], "findings": findings}, indent=2))


if __name__ == "__main__":
    main()
