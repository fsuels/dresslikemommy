#!/usr/bin/env python3
"""Build a no-upload US Search validation packet from public-active rows."""

from __future__ import annotations

import csv
import json
import re
import ssl
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = Path(__file__).resolve().parent
KEYWORD_UNIVERSE = ROOT / "ops/marketing/keyword_universe.csv"
ACTIVE_PRODUCT_ROWS = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    / "2026-05-14-automation-us-active-product-proof/us_active_product_sample_rows.csv"
)
VALIDATION_CSV = PACKET_DIR / "us_search_12_active_product_cpc_validation_rows.csv"
VALIDATION_MATRIX_CSV = PACKET_DIR / "us_search_12_active_product_cpc_validation_matrix.csv"
ROUTE_READBACK_CSV = PACKET_DIR / "us_search_active_product_route_readback.csv"
SUMMARY_JSON = PACKET_DIR / "us_search_active_product_validation_summary.json"
REPORT_MD = PACKET_DIR / "US_SEARCH_ACTIVE_PRODUCT_VALIDATION_PACKET.md"

TIMESTAMP = "2026-05-15 04:27 EDT"
MAX_BASE_ROWS = 12
HEADER_VARIANTS = (
    ("text_html", "text/html,application/xhtml+xml"),
    ("star_cache_bust", "*/*"),
)
LEAK_PATTERNS = (
    "1688" + ".com",
    "detail" + "." + "1688" + ".com",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def canonical_route(route: str) -> str:
    if route == "/collections/family-matching":
        return "/collections/matching-outfits"
    return route


def route_url(route: str) -> str:
    return f"https://www.dresslikemommy.com{canonical_route(route)}?country=US"


def active_product_counts() -> dict[str, Counter]:
    counts: dict[str, Counter] = defaultdict(Counter)
    for row in read_csv(ACTIVE_PRODUCT_ROWS):
        route = canonical_route(row["route"])
        counts[route][row["decision"]] += 1
    return counts


def select_keyword_rows() -> list[dict[str, str]]:
    counts = active_product_counts()
    candidates = []
    for row in read_csv(KEYWORD_UNIVERSE):
        route = canonical_route(row["landing_route"])
        if row["market"] != "US":
            continue
        if row["threshold"] != "GREEN":
            continue
        if row["promotion_status"] != "LOCAL_ONLY_VALIDATE_NOT_UPLOADED":
            continue
        if route == "/collections/family-swimsuits":
            continue
        if counts[route]["PUBLIC_ACTIVE_PRODUCT_PASS"] < 3:
            continue
        candidate = dict(row)
        candidate["landing_route"] = route
        candidate["final_url_to_validate"] = route_url(route)
        candidate["public_active_product_pass_count"] = str(counts[route]["PUBLIC_ACTIVE_PRODUCT_PASS"])
        candidate["public_active_product_hold_count"] = str(counts[route]["HOLD_FOR_REVIEW_OR_REPAIR"])
        candidates.append(candidate)

    candidates.sort(
        key=lambda row: (
            -int(row["total_score"]),
            row["category"],
            row["keyword"],
        )
    )

    selected: list[dict[str, str]] = []
    per_route = Counter()
    per_category = Counter()
    for row in candidates:
        route = row["landing_route"]
        category = row["category"]
        if per_route[route] >= 4:
            continue
        if per_category[category] >= 4:
            continue
        selected.append(row)
        per_route[route] += 1
        per_category[category] += 1
        if len(selected) == MAX_BASE_ROWS:
            break

    return selected


def write_base_rows(rows: list[dict[str, str]]) -> None:
    fields = [
        "market",
        "language",
        "category",
        "keyword",
        "source_match_candidate",
        "total_score",
        "threshold",
        "landing_route",
        "final_url_to_validate",
        "public_active_product_pass_count",
        "public_active_product_hold_count",
        "validation_status",
    ]
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "market": row["market"],
                    "language": row["language"],
                    "category": row["category"],
                    "keyword": row["keyword"],
                    "source_match_candidate": row["match_candidate"],
                    "total_score": row["total_score"],
                    "threshold": row["threshold"],
                    "landing_route": row["landing_route"],
                    "final_url_to_validate": row["final_url_to_validate"],
                    "public_active_product_pass_count": row["public_active_product_pass_count"],
                    "public_active_product_hold_count": row["public_active_product_hold_count"],
                    "validation_status": "AUTH_CPC_SEARCH_FEASIBILITY_REQUIRED_NO_UPLOAD",
                }
            )


def write_matrix(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    matrix = []
    for row in rows:
        for match_type in ("exact", "phrase"):
            matrix.append(
                {
                    "market": "US",
                    "geo_target": "United States",
                    "language": "en-US",
                    "keyword": row["keyword"],
                    "match_type": match_type,
                    "max_cpc": "0.15",
                    "landing_route": row["landing_route"],
                    "final_url_to_validate": row["final_url_to_validate"],
                    "source_total_score": row["total_score"],
                    "gate": "FORECAST_ONLY_NO_UPLOAD_UNTIL_PASS_015_CPC_GATE",
                }
            )

    fields = list(matrix[0].keys())
    with VALIDATION_MATRIX_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(matrix)
    return matrix


def cache_bust_url(url: str) -> str:
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}_dlm_cb={int(time.time())}"


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth US Search validation readback",
        },
    )
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def route_readbacks(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    routes: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        routes[row["landing_route"]].append(row["keyword"])

    results: list[dict[str, object]] = []
    for route, keywords in sorted(routes.items()):
        url = route_url(route)
        for variant_name, accept in HEADER_VARIANTS:
            fetch_url = cache_bust_url(url) if variant_name == "star_cache_bust" else url
            status, effective_url, html = fetch(fetch_url, accept)
            lower = html.lower()
            results.append(
                {
                    "market": "US",
                    "landing_route": route,
                    "header_variant": variant_name,
                    "url": fetch_url,
                    "effective_url": effective_url,
                    "redirected": effective_url != fetch_url,
                    "status": status,
                    "supplier_or_url_brand_hits": sum(html.count(pattern) for pattern in LEAK_PATTERNS),
                    "stale_or_trust_hits": sum(html.count(pattern) for pattern in STALE_OR_TRUST_PATTERNS),
                    "product_url_count": len(set(re.findall(r"/products/[-a-z0-9]+", html))),
                    "has_shipping_signal": "ships to" in lower or "shipping" in lower,
                    "keyword_count": len(keywords),
                    "title": page_title(html),
                    "keywords": keywords,
                }
            )
    return results


def write_route_readback(results: list[dict[str, object]]) -> None:
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
    with ROUTE_READBACK_CSV.open("w", newline="", encoding="utf-8") as handle:
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
            "| {landing_route} | {header_variant} | `{status}` | {redirected} | `{supplier_or_url_brand_hits}` | `{stale_or_trust_hits}` | `{product_url_count}` | {has_shipping_signal} | `{keyword_count}` | `{title}` |".format(
                **result
            )
        )
    category_counts = summary["keyword_counts_by_category"]
    route_counts = summary["keyword_counts_by_route"]
    report = f"""# US Search Active-Product Validation Packet

Timestamp: {TIMESTAMP}

Scope: repo-local, no-upload US Search validation input built only from `GREEN` US keyword-universe rows whose canonical route has public active-product proof. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

- Base keyword rows: `{summary['base_keyword_row_count']}`
- Exact/phrase forecast rows: `{summary['forecast_matrix_row_count']}`
- Unique canonical routes: `{summary['unique_route_count']}`
- Public route fetches: `{summary['route_fetch_count']}`
- Non-200 route fetches: `{summary['non_200_count']}`
- Redirected fetches: `{summary['redirect_count']}`
- Supplier/source-domain or URL-brand hits: `{summary['supplier_hit_total']}`
- Stale seasonal/local-inventory trust hits: `{summary['stale_hit_total']}`

Rows by route:

{chr(10).join(f'- `{route}`: `{count}`' for route, count in sorted(route_counts.items()))}

Rows by category:

{chr(10).join(f'- `{category}`: `{count}`' for category, count in sorted(category_counts.items()))}

This is a validation input only. It is not an upload file and does not create a `GREEN` live action row. The authenticated `$0.15` CPC/search-feasibility gate remains open.

## Route Readback

| Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Keyword count | Title |
|---|---|---:|---|---:|---:|---:|---|---:|---|
{chr(10).join(route_lines)}

## Exact Next Gate

After Google Ads API Basic Access approval, run this packet through the read-only forecast harness or a correctly scoped Keyword Planner export using United States, English, exact/phrase rows, and max CPC `$0.15`. Promote only rows that produce real `PASS_015_CPC_GATE` evidence, reviewer pass, fresh before-state Ads readback, and an after-state readback plan.

## Files

- Base validation CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_12_active_product_cpc_validation_rows.csv`
- Exact/phrase matrix: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_12_active_product_cpc_validation_matrix.csv`
- Public route readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_active_product_route_readback.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_active_product_validation_summary.json`
"""
    REPORT_MD.write_text(report, encoding="utf-8")


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    rows = select_keyword_rows()
    if len(rows) != MAX_BASE_ROWS:
        raise SystemExit(f"EXPECTED_{MAX_BASE_ROWS}_ROWS_GOT_{len(rows)}")

    write_base_rows(rows)
    matrix = write_matrix(rows)
    route_results = route_readbacks(rows)
    write_route_readback(route_results)

    summary = {
        "timestamp": TIMESTAMP,
        "base_keyword_row_count": len(rows),
        "forecast_matrix_row_count": len(matrix),
        "unique_route_count": len({row["landing_route"] for row in rows}),
        "route_fetch_count": len(route_results),
        "non_200_count": sum(1 for result in route_results if result["status"] != 200),
        "redirect_count": sum(1 for result in route_results if result["redirected"]),
        "supplier_hit_total": sum(int(result["supplier_or_url_brand_hits"]) for result in route_results),
        "stale_hit_total": sum(int(result["stale_or_trust_hits"]) for result in route_results),
        "keyword_counts_by_category": dict(Counter(row["category"] for row in rows)),
        "keyword_counts_by_route": dict(Counter(row["landing_route"] for row in rows)),
        "base_rows_csv": str(VALIDATION_CSV.relative_to(ROOT)),
        "forecast_matrix_csv": str(VALIDATION_MATRIX_CSV.relative_to(ROOT)),
        "route_readback_csv": str(ROUTE_READBACK_CSV.relative_to(ROOT)),
        "route_results": route_results,
        "next_action": "Run authenticated read-only US Search CPC/search-feasibility validation at max $0.15 after Google Ads API Basic Access approval; no upload/apply/add keyword/bid/status/budget/negative action until pass rows exist.",
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_report(summary)

    if summary["non_200_count"] or summary["redirect_count"] or summary["supplier_hit_total"] or summary["stale_hit_total"]:
        raise SystemExit("US_SEARCH_VALIDATION_PACKET_HAS_PUBLIC_ROUTE_BLOCKERS")

    print(
        json.dumps(
            {
                "base_keyword_row_count": summary["base_keyword_row_count"],
                "forecast_matrix_row_count": summary["forecast_matrix_row_count"],
                "unique_route_count": summary["unique_route_count"],
                "route_fetch_count": summary["route_fetch_count"],
                "supplier_hit_total": summary["supplier_hit_total"],
                "stale_hit_total": summary["stale_hit_total"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
