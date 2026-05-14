#!/usr/bin/env python3
"""Build and public-readback the canonical-url GB/CA/AU CPC packet."""

from __future__ import annotations

import csv
import json
import re
import ssl
import time
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = Path(__file__).resolve().parent
SOURCE_CSV = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    / "2026-05-14-automation-swim-route-unblock/"
    / "gb_ca_au_36_clean_route_cpc_validation_rows.csv"
)
CANONICAL_CSV = PACKET_DIR / "gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv"
READBACK_CSV = PACKET_DIR / "gb_ca_au_36_canonical_url_public_readback_rows.csv"
SUMMARY_JSON = PACKET_DIR / "gb_ca_au_36_canonical_url_packet_summary.json"
REPORT_MD = PACKET_DIR / "GB_CA_AU_36_ROW_CPC_CANONICAL_URL_PACKET.md"

TIMESTAMP = "2026-05-14 14:57 EDT"
HEADER_VARIANTS = (
    ("text_html", "text/html,application/xhtml+xml"),
    ("star_cache_bust", "*/*"),
)
LEAK_PATTERNS = (
    "detail.1688.com",
    "1688.com",
    "alibaba.com",
    "aliexpress.com",
    'data-analytics-vendor="http',
    'data-item-brand="http',
)
STALE_OR_TRUST_PATTERNS = (
    "Christmas",
    "Santa",
    "Xmas",
    "local inventory",
    "warehouse",
    "retail store",
)


def canonicalize_url(url: str) -> str:
    return url.replace("/collections/family-matching", "/collections/matching-outfits")


def canonicalize_route(route: str) -> str:
    if route == "/collections/family-matching":
        return "/collections/matching-outfits"
    return route


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth canonical URL readback",
        },
    )
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")


def cache_bust_url(url: str) -> str:
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}_dlm_cb={int(time.time())}"


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def build_canonical_rows() -> tuple[list[dict[str, str]], int]:
    with SOURCE_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    changed = 0
    for row in rows:
        original_route = row["landing_route"]
        original_url = row["final_url_to_validate"]
        row["landing_route"] = canonicalize_route(original_route)
        row["final_url_to_validate"] = canonicalize_url(original_url)
        if row["landing_route"] != original_route or row["final_url_to_validate"] != original_url:
            changed += 1

    with CANONICAL_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return rows, changed


def unique_routes(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    routes: dict[tuple[str, str, str], dict[str, object]] = {}
    for row in rows:
        key = (row["market"], row["landing_route"], row["final_url_to_validate"])
        routes.setdefault(
            key,
            {
                "market": row["market"],
                "landing_route": row["landing_route"],
                "url": row["final_url_to_validate"],
                "keywords": [],
            },
        )
        routes[key]["keywords"].append(row["keyword"])
    return list(routes.values())


def readback(routes: list[dict[str, object]]) -> list[dict[str, object]]:
    results = []
    for route in sorted(routes, key=lambda item: (item["market"], item["landing_route"])):
        for variant_name, accept in HEADER_VARIANTS:
            url = str(route["url"])
            fetch_url = cache_bust_url(url) if variant_name == "star_cache_bust" else url
            status, effective_url, html = fetch(fetch_url, accept)
            lower = html.lower()
            leak_counts = {pattern: html.count(pattern) for pattern in LEAK_PATTERNS}
            stale_counts = {pattern: html.count(pattern) for pattern in STALE_OR_TRUST_PATTERNS}
            results.append(
                {
                    "market": route["market"],
                    "landing_route": route["landing_route"],
                    "header_variant": variant_name,
                    "url": fetch_url,
                    "effective_url": effective_url,
                    "redirected": effective_url != fetch_url,
                    "status": status,
                    "supplier_or_url_brand_hits": sum(leak_counts.values()),
                    "stale_or_trust_hits": sum(stale_counts.values()),
                    "product_url_count": len(set(re.findall(r"/products/[-a-z0-9]+", html))),
                    "has_shipping_signal": "ships to" in lower or "shipping" in lower,
                    "title": page_title(html),
                    "keyword_count": len(route["keywords"]),
                    "keywords": route["keywords"],
                }
            )
    return results


def write_readback_csv(results: list[dict[str, object]]) -> None:
    fields = [
        "market",
        "landing_route",
        "header_variant",
        "url",
        "effective_url",
        "redirected",
        "status",
        "supplier_or_url_brand_hits",
        "stale_or_trust_hits",
        "product_url_count",
        "has_shipping_signal",
        "keyword_count",
        "title",
        "keywords",
    ]
    with READBACK_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for result in results:
            row = {field: result[field] for field in fields}
            row["keywords"] = "; ".join(result["keywords"])
            writer.writerow(row)


def write_report(summary: dict[str, object]) -> None:
    route_lines = []
    for result in summary["route_results"]:
        route_lines.append(
            "| {market} | `{landing_route}` | {header_variant} | `{status}` | {redirected} | `{supplier_or_url_brand_hits}` | `{stale_or_trust_hits}` | `{product_url_count}` | {has_shipping_signal} | `{title}` |".format(
                **result
            )
        )
    counts = summary["keyword_counts_by_market"]
    report = f"""# GB/CA/AU 36-Row CPC Canonical URL Packet

Timestamp: {TIMESTAMP}

Scope: repo-local canonical copy plus public/read-only route readback for the existing GB/CA/AU 36-row CPC validation packet. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

The packet is now ready for authenticated CPC validation without redirect cleanup:

- Source rows: `{summary['source_row_count']}`
- Rows canonicalized from `/collections/family-matching` to `/collections/matching-outfits`: `{summary['canonicalized_row_count']}`
- Unique market/route URLs: `{summary['unique_route_count']}`
- Public route fetches: `{summary['route_fetch_count']}`
- Non-200 route fetches: `{summary['non_200_count']}`
- Redirected fetches: `{summary['redirect_count']}`
- Supplier/source-domain or URL-brand hits: `{summary['supplier_hit_total']}`
- Stale seasonal/local-inventory trust hits: `{summary['stale_hit_total']}`

Rows by market:

- GB: `{counts.get('GB', 0)}`
- CA: `{counts.get('CA', 0)}`
- AU: `{counts.get('AU', 0)}`

The authenticated `$0.15` CPC/auction-entry gate remains open. This packet does not authorize upload/apply/add keyword/bid/status/budget/negative changes.

## Route Readback

| Market | Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Title |
|---|---|---|---:|---|---:|---:|---:|---|---|
{chr(10).join(route_lines)}

## Exact Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for `gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv` at max CPC `$0.15`. Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass, fresh before-state Ads readback, and after-state readback.

## Files

- Canonical validation CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv`
- Public route readback rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_canonical_url_public_readback_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_canonical_url_packet_summary.json`
"""
    REPORT_MD.write_text(report, encoding="utf-8")


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    rows, changed = build_canonical_rows()
    routes = unique_routes(rows)
    results = readback(routes)
    summary = {
        "timestamp": TIMESTAMP,
        "source_csv": str(SOURCE_CSV.relative_to(ROOT)),
        "canonical_csv": str(CANONICAL_CSV.relative_to(ROOT)),
        "source_row_count": len(rows),
        "canonicalized_row_count": changed,
        "unique_route_count": len(routes),
        "route_fetch_count": len(results),
        "non_200_count": sum(1 for result in results if result["status"] != 200),
        "redirect_count": sum(1 for result in results if result["redirected"]),
        "supplier_hit_total": sum(int(result["supplier_or_url_brand_hits"]) for result in results),
        "stale_hit_total": sum(int(result["stale_or_trust_hits"]) for result in results),
        "keyword_counts_by_market": dict(Counter(row["market"] for row in rows)),
        "route_results": results,
        "auth_cpc_gate": {
            "status": "AUTOMATION_CAPABILITY_MISMATCH",
            "reason": "Authenticated Google Ads/Keyword Planner validation is required; this unattended runtime is already recorded as not having an account-capable Ads path.",
            "next_action": "Validate canonical CSV at max CPC $0.15; no upload/apply/add keyword/bid/status/budget/negative action until pass rows, fresh readback, reviewer pass, and after-state plan exist.",
        },
    }
    write_readback_csv(results)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_report(summary)

    if summary["non_200_count"] or summary["redirect_count"] or summary["supplier_hit_total"] or summary["stale_hit_total"]:
        raise SystemExit("CANONICAL_URL_PACKET_HAS_BLOCKERS")

    print(
        json.dumps(
            {
                "source_row_count": summary["source_row_count"],
                "canonicalized_row_count": summary["canonicalized_row_count"],
                "unique_route_count": summary["unique_route_count"],
                "route_fetch_count": summary["route_fetch_count"],
                "redirect_count": summary["redirect_count"],
                "supplier_hit_total": summary["supplier_hit_total"],
                "stale_hit_total": summary["stale_hit_total"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
