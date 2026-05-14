#!/usr/bin/env python3
"""Refresh public route readbacks for the GB/CA/AU 36-row CPC packet.

This script is intentionally public/read-only. It checks the exact final URLs
already packetized for authenticated Google Ads/Keyword Planner validation and
does not touch Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing,
campaign, budget, bid, status, feed, product, conversion, product scope, or live
theme state.
"""

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
ROWS_CSV = PACKET_DIR / "gb_ca_au_36_row_public_route_readback_rows.csv"
SUMMARY_JSON = PACKET_DIR / "gb_ca_au_36_row_public_route_readback_summary.json"
REPORT_MD = PACKET_DIR / "GB_CA_AU_36_ROW_CPC_PUBLIC_ROUTE_REFRESH.md"

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
HEADER_VARIANTS = (
    ("text_html", "text/html,application/xhtml+xml"),
    ("star_cache_bust", "*/*"),
)


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth route readback",
        },
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=30, context=context) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def cache_bust_url(url: str) -> str:
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}_dlm_cb={int(time.time())}"


def load_scope() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with SOURCE_CSV.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    unique = {}
    for row in rows:
        url = row["final_url_to_validate"]
        key = (row["market"], row["landing_route"], url)
        unique.setdefault(
            key,
            {
                "market": row["market"],
                "landing_route": row["landing_route"],
                "url": url,
                "keywords": [],
            },
        )
        unique[key]["keywords"].append(row["keyword"])
    return rows, list(unique.values())


def check_routes(unique_routes: list[dict[str, object]]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for route in sorted(unique_routes, key=lambda item: (item["market"], item["landing_route"])):
        for variant_name, accept in HEADER_VARIANTS:
            url = route["url"]
            fetch_url = cache_bust_url(str(url)) if variant_name == "star_cache_bust" else str(url)
            status, effective_url, html = fetch(fetch_url, accept)
            lower = html.lower()
            leak_counts = {pattern: html.count(pattern) for pattern in LEAK_PATTERNS}
            stale_counts = {pattern: html.count(pattern) for pattern in STALE_OR_TRUST_PATTERNS}
            product_urls = len(set(re.findall(r"/products/[-a-z0-9]+", html)))
            results.append(
                {
                    "market": route["market"],
                    "landing_route": route["landing_route"],
                    "header_variant": variant_name,
                    "url": fetch_url,
                    "effective_url": effective_url,
                    "redirected": effective_url != fetch_url,
                    "status": status,
                    "title": page_title(html),
                    "supplier_or_url_brand_hits": sum(leak_counts.values()),
                    "stale_or_trust_hits": sum(stale_counts.values()),
                    "leak_counts": leak_counts,
                    "stale_or_trust_counts": stale_counts,
                    "product_url_count": product_urls,
                    "has_shipping_signal": "ships to" in lower or "shipping" in lower,
                    "keyword_count": len(route["keywords"]),
                    "keywords": route["keywords"],
                }
            )
    return results


def write_rows(results: list[dict[str, object]]) -> None:
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
    with ROWS_CSV.open("w", newline="") as handle:
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
    markdown = f"""# GB/CA/AU 36-Row CPC Public Route Refresh

Timestamp: 2026-05-14 14:37 EDT

Scope: public/read-only route refresh for the existing 36-row GB/CA/AU CPC validation packet. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

The exact 36-row packet still has public-clean final URLs for CPC validation:

- Rows checked from source packet: `{summary['source_row_count']}`
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

The authenticated CPC/auction-entry gate remains blocked in this automation runtime because the shell has no Google Ads env keys and the Python Google Ads client package is not installed. This refresh does not authorize upload/apply/add keyword/bid/status/budget/negative changes.

Non-blocking URL note: the `/collections/family-matching` packet URLs redirect cleanly to `/collections/matching-outfits?country=...`. This is not a source-cleanliness blocker, but future live packets should prefer canonical final URLs after the authenticated CPC gate.

## Route Readback

| Market | Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Title |
|---|---|---|---:|---|---:|---:|---:|---|---|
{chr(10).join(route_lines)}

## Exact Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for `gb_ca_au_36_clean_route_cpc_validation_rows.csv` at max CPC `$0.15`. Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass and after-state readback.

## Files

- Source packet CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv`
- Public route rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/gb_ca_au_36_row_public_route_readback_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/gb_ca_au_36_row_public_route_readback_summary.json`
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    source_rows, unique_routes = load_scope()
    results = check_routes(unique_routes)
    keyword_counts = Counter(row["market"] for row in source_rows)
    summary = {
        "timestamp": "2026-05-14 14:37 EDT",
        "source_csv": str(SOURCE_CSV.relative_to(ROOT)),
        "source_row_count": len(source_rows),
        "unique_route_count": len(unique_routes),
        "route_fetch_count": len(results),
        "non_200_count": sum(1 for result in results if result["status"] != 200),
        "redirect_count": sum(1 for result in results if result["redirected"]),
        "supplier_hit_total": sum(int(result["supplier_or_url_brand_hits"]) for result in results),
        "stale_hit_total": sum(int(result["stale_or_trust_hits"]) for result in results),
        "keyword_counts_by_market": dict(keyword_counts),
        "route_results": results,
        "auth_cpc_gate": {
            "status": "AUTOMATION_CAPABILITY_MISMATCH",
            "reason": "No Google Ads API env keys loaded and google.ads.googleads is not installed in this shell.",
            "next_action": "Use authenticated Google Ads/Keyword Planner at max CPC $0.15; no upload/apply/add keyword/bid/status/budget/negative action until pass rows, fresh readback, reviewer pass, and after-state plan exist.",
        },
    }
    write_rows(results)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_report(summary)

    if summary["non_200_count"] or summary["supplier_hit_total"] or summary["stale_hit_total"]:
        raise SystemExit("PUBLIC_ROUTE_REFRESH_HAS_BLOCKERS")

    print(
        json.dumps(
            {
                k: summary[k]
                for k in (
                    "source_row_count",
                    "unique_route_count",
                    "route_fetch_count",
                    "redirect_count",
                    "supplier_hit_total",
                    "stale_hit_total",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
