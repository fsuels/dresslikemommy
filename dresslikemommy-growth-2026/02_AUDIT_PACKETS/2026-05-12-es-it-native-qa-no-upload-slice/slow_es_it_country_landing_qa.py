#!/usr/bin/env python3
"""Slow country-qualified ES/IT landing QA.

This checks public product landing pages only. It performs no checkout,
payment, order, admin, catalog, feed, or ads writes.
"""

from __future__ import annotations

import csv
import html
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


BASE = "https://www.dresslikemommy.com"
HANDLE = "golden-daisy-mommy-and-me-set"
PACKET = Path(__file__).resolve().parent
RAW = PACKET / "landing_qa_raw"
SUMMARY = PACKET / "es_it_country_landing_qa_summary.json"
CSV_OUT = PACKET / "es_it_country_landing_qa_summary.csv"
REPORT = PACKET / "ES_IT_COUNTRY_QUALIFIED_LANDING_QA.md"

TARGETS = [
    {
        "market": "ES",
        "locale": "es-ES",
        "path": f"/es/products/{HANDLE}?country=ES",
        "expected_currency": ["EUR", "€"],
        "expected_lang_prefix": "es",
        "expected_words": ["mamá", "hija", "vestido", "conjunto", "añadir", "carrito"],
    },
    {
        "market": "IT",
        "locale": "it-IT",
        "path": f"/it/products/{HANDLE}?country=IT",
        "expected_currency": ["EUR", "€"],
        "expected_lang_prefix": "it",
        "expected_words": ["mamma", "figlia", "abito", "coordinato", "aggiungi", "carrello"],
    },
]

FORBIDDEN = [
    "1688.com",
    "detail.1688.com",
    "alibaba.com",
    "aliexpress.com",
    "taobao.com",
]

VISIBLE_FORBIDDEN = [
    "supplier",
    "wholesale",
]

STALE_BLOCKERS = [
    "christmas",
    "xmas",
    "santa claus",
    "elf costume",
    "warehouse",
    "in-store pickup",
    "local inventory",
    "guaranteed in stock",
]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return html.unescape(clean(match.group(1))) if match else ""


def visible_text_from_html(body: str) -> str:
    without_scripts = re.sub(r"<(script|style|template)[^>]*>.*?</\1>", " ", body, flags=re.I | re.S)
    without_comments = re.sub(r"<!--.*?-->", " ", without_scripts, flags=re.S)
    return clean(re.sub(r"<[^>]+>", " ", without_comments))


def fetch(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "final_url": response.geturl(),
                "headers": dict(response.headers.items()),
                "elapsed_seconds": round(time.time() - started, 2),
                "body": body,
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "status": exc.code,
            "ok": False,
            "final_url": exc.geturl(),
            "headers": dict(exc.headers.items()),
            "elapsed_seconds": round(time.time() - started, 2),
            "body": body,
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "status": None,
            "ok": False,
            "final_url": url,
            "headers": {},
            "elapsed_seconds": round(time.time() - started, 2),
            "body": "",
            "error": str(exc),
        }


def evaluate(target: dict, response: dict) -> dict:
    body = response["body"]
    lower = body.lower()
    text_only = visible_text_from_html(body)
    visible_lower = text_only.lower()
    title = extract(r"<title[^>]*>(.*?)</title>", body)
    h1 = extract(r"<h1[^>]*>(.*?)</h1>", body)
    html_lang = extract(r"<html[^>]*\slang=[\"']?([^\"'\s>]+)", body)
    canonical = extract(r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"']([^\"']+)", body)
    og_currency = extract(r"<meta[^>]+property=[\"']og:price:currency[\"'][^>]+content=[\"']([^\"']+)", body)
    currency_hits = [token for token in target["expected_currency"] if token in body or token in text_only]
    expected_word_hits = [word for word in target["expected_words"] if word.lower() in visible_lower]
    source_forbidden_hits = [token for token in FORBIDDEN if token.lower() in lower]
    visible_forbidden_hits = [token for token in VISIBLE_FORBIDDEN if token.lower() in visible_lower]
    stale_hits = [token for token in STALE_BLOCKERS if token.lower() in visible_lower]
    verification_hits = [token for token in ["verifying your connection", "429 too many requests"] if token in visible_lower]
    country_param_preserved = f"country={target['market']}" in response["final_url"] or f"country={target['market']}" in target["path"]
    language_pass = html_lang.lower().startswith(target["expected_lang_prefix"]) or len(expected_word_hits) >= 2
    currency_pass = bool(currency_hits) or og_currency == "EUR"
    pass_checks = {
        "http_ok": response["ok"],
        "not_verification_or_429": response["status"] != 429 and not verification_hits,
        "country_qualified_url_used": country_param_preserved,
        "language_signal_present": language_pass,
        "currency_signal_present": currency_pass,
        "no_supplier_or_source_tokens": not source_forbidden_hits and not visible_forbidden_hits,
        "no_stale_paid_blocker_copy": not stale_hits,
    }
    return {
        "market": target["market"],
        "locale": target["locale"],
        "requested_url": f"{BASE}{target['path']}",
        "status": response["status"],
        "ok": response["ok"],
        "final_url": response["final_url"],
        "elapsed_seconds": response["elapsed_seconds"],
        "title": title,
        "h1": h1,
        "html_lang": html_lang,
        "canonical": canonical,
        "og_currency": og_currency,
        "currency_hits": currency_hits,
        "expected_word_hits": expected_word_hits,
        "forbidden_hits": source_forbidden_hits + visible_forbidden_hits,
        "source_forbidden_hits": source_forbidden_hits,
        "visible_forbidden_hits": visible_forbidden_hits,
        "stale_hits": stale_hits,
        "verification_hits": verification_hits,
        "checks": pass_checks,
        "decision": f"{target['market']}_COUNTRY_QUALIFIED_LANDING_QA_PASSED"
        if all(pass_checks.values())
        else f"{target['market']}_COUNTRY_QUALIFIED_LANDING_QA_NEEDS_REVIEW",
        "body_excerpt": text_only[:1200],
        "error": response["error"],
    }


def write_report(rows: list[dict]) -> None:
    lines = [
        "# ES/IT Country-Qualified Landing QA",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Mode: slow public landing-page GETs only. No checkout, payment, order, Ads, Merchant, Pinterest, Shopify product, feed, conversion-goal, budget, bid, or status write occurred.",
        "",
        "| Market | Decision | HTTP | Lang | Currency | Supplier tokens | Stale blockers |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['market']}` | `{row['decision']}` | `{row['status']}` | `{row['html_lang']}` | "
            f"`{', '.join(row['currency_hits']) or row['og_currency']}` | `{', '.join(row['forbidden_hits']) or 'none'}` | "
            f"`{', '.join(row['stale_hits']) or 'none'}` |"
        )
    lines.extend(["", "## Details", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['market']}",
                "",
                f"- Requested URL: `{row['requested_url']}`",
                f"- Final URL: `{row['final_url']}`",
                f"- Title: `{row['title']}`",
                f"- H1: `{row['h1']}`",
                f"- Expected-language word hits: `{', '.join(row['expected_word_hits']) or 'none'}`",
                f"- Checks: `{json.dumps(row['checks'], sort_keys=True)}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Evidence",
            "",
            f"- Summary JSON: `{SUMMARY}`",
            f"- Summary CSV: `{CSV_OUT}`",
            f"- Raw HTML directory: `{RAW}`",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, target in enumerate(TARGETS):
        if index:
            time.sleep(12)
        url = f"{BASE}{target['path']}"
        response = fetch(url)
        (RAW / f"{target['market'].lower()}_landing.html").write_text(response["body"], encoding="utf-8")
        row = evaluate(target, response)
        rows.append(row)
    SUMMARY.write_text(json.dumps({"generated_at": datetime.now().astimezone().isoformat(timespec="seconds"), "rows": rows}, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["market", "locale", "decision", "status", "final_url", "html_lang", "title", "h1", "currency_hits", "expected_word_hits", "forbidden_hits", "stale_hits"])
        writer.writeheader()
        for row in rows:
            writer.writerow({key: ", ".join(row[key]) if isinstance(row.get(key), list) else row.get(key, "") for key in writer.fieldnames})
    write_report(rows)
    print(json.dumps({"summary": str(SUMMARY), "report": str(REPORT), "decisions": [row["decision"] for row in rows]}, indent=2, ensure_ascii=False))
    return 0 if all(row["decision"].endswith("_PASSED") for row in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
