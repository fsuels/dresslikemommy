#!/usr/bin/env python3
"""Build a public-readback cleanup packet for remaining dirty collection routes.

This does not use Shopify Admin, Google Ads, Merchant, Pinterest, or any live
write surface. It reads public storefront HTML and turns dirty collection routes
into exact repair/exclusion gates for future paid traffic decisions.
"""

from __future__ import annotations

import csv
import html
import json
import re
import ssl
import time
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = Path(__file__).resolve().parent
KEYWORD_UNIVERSE = ROOT / "ops/marketing/keyword_universe.csv"
REPORT_MD = PACKET_DIR / "COLLECTION_SOURCE_CLEANUP_APPROVAL_PACKET.md"
SUMMARY_JSON = PACKET_DIR / "collection_source_cleanup_approval_summary.json"
ROUTE_ROWS_CSV = PACKET_DIR / "collection_source_cleanup_route_rows.csv"
PRODUCT_ROWS_CSV = PACKET_DIR / "collection_source_cleanup_product_rows.csv"

BASE_URL = "https://www.dresslikemommy.com"
MARKETS = ("US", "GB", "CA", "AU")
ROUTES = (
    "/collections/swimsuits",
    "/collections/matching-dresses",
)
LEAK_PATTERNS = (
    "detail.1688.com",
    "1688.com",
    "alibaba.com",
    "aliexpress.com",
    'data-analytics-vendor="http',
    'data-item-brand="http',
)
REPUTATION_PATTERNS = ("Christmas", "Santa", "Xmas", "local inventory", "warehouse", "retail store")


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth public route readback",
        },
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=30, context=context) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")


def page_title(page: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", page, re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()


def unescape_jsonish(value: str) -> str:
    return (
        value.replace("\\/", "/")
        .replace("\\u0026", "&")
        .replace('\\"', '"')
        .replace("\\'", "'")
    )


def find_source_products(page: str) -> list[dict[str, str]]:
    products: dict[tuple[str, str], dict[str, str]] = {}
    chunks = re.split(r'\},\{\\"price\\"', page)
    for chunk in chunks:
        if "detail.1688.com" not in chunk:
            continue
        title_match = re.search(r'\\"title\\":\\"(?P<title>.*?)\\"', chunk)
        vendor_match = re.search(r'\\"vendor\\":\\"(?P<vendor>https:\\/\\/detail\.1688\.com\\/offer\\/[^\\"]+?\.html)\\"', chunk)
        id_match = re.search(r'\\"id\\":\\"(?P<id>\d+)\\"', chunk)
        url_match = re.search(r'\\"url\\":\\"(?P<url>\\/products\\/[^\\"]+)\\"', chunk)
        type_match = re.search(r'\\"type\\":\\"(?P<type>.*?)\\"', chunk)
        if not vendor_match or not url_match:
            continue
        product_url = unescape_jsonish(url_match.group("url"))
        handle = product_url.rsplit("/", 1)[-1]
        vendor = unescape_jsonish(vendor_match.group("vendor"))
        key = (handle, vendor)
        products[key] = {
            "handle": handle,
            "product_url": product_url,
            "product_id": id_match.group("id") if id_match else "",
            "title": unescape_jsonish(title_match.group("title")) if title_match else "",
            "type": unescape_jsonish(type_match.group("type")) if type_match else "",
            "source_domain": "detail.1688.com",
            "recommended_action": "owner_approved_shopify_vendor_source_cleanup_or_keep_route_excluded",
        }
    return sorted(products.values(), key=lambda row: (row["handle"], row["source_domain"]))


def route_checks() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    checks: list[dict[str, object]] = []
    products: dict[tuple[str, str, str], dict[str, str]] = {}
    variants = (
        ("text/html", "text/html,application/xhtml+xml"),
        ("star", "*/*"),
    )
    for route in ROUTES:
        for market in MARKETS:
            for variant, accept in variants:
                suffix = f"?country={market}"
                if variant == "star":
                    suffix = f"?country={market}&_dlm_cb={int(time.time())}"
                url = f"{BASE_URL}{route}{suffix}"
                status, final_url, page = fetch(url, accept)
                leak_counts = {pattern: page.count(pattern) for pattern in LEAK_PATTERNS}
                reputation_counts = {pattern: page.count(pattern) for pattern in REPUTATION_PATTERNS}
                source_products = find_source_products(page)
                for product in source_products:
                    products[(route, product["handle"], product["source_domain"])] = {
                        "route": route,
                        **product,
                    }
                checks.append(
                    {
                        "route": route,
                        "market": market,
                        "variant": variant,
                        "url": url,
                        "final_url": final_url,
                        "status": status,
                        "title": page_title(page),
                        "supplier_or_url_brand_hits": sum(leak_counts.values()),
                        "leak_counts": leak_counts,
                        "reputation_counts": reputation_counts,
                        "source_product_count": len(source_products),
                        "product_url_count": len(set(re.findall(r"/products/[-a-z0-9]+", page))),
                        "decision": "keep_excluded_until_product_vendor_source_clean" if source_products else "route_clean_on_this_readback",
                    }
                )
    return checks, sorted(products.values(), key=lambda row: (row["route"], row["handle"], row["source_domain"]))


def keyword_rows_for_routes() -> list[dict[str, str]]:
    with KEYWORD_UNIVERSE.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if row["landing_route"] in ROUTES:
                rows.append(
                    {
                        "market": row["market"],
                        "category": row["category"],
                        "keyword": row["keyword"],
                        "threshold": row["threshold"],
                        "promotion_status": row["promotion_status"],
                        "landing_route": row["landing_route"],
                        "live_action": row["live_action"],
                    }
                )
    return rows


def write_csv(path: Path, rows: list[dict[str, object | str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(summary: dict[str, object]) -> None:
    route_checks = summary["route_checks"]
    product_rows = summary["source_products"]
    keyword_rows = summary["keyword_rows"]
    route_counts = summary["dirty_product_count_by_route"]
    keyword_counts = summary["keyword_count_by_route"]

    route_lines = []
    for check in route_checks:
        route_lines.append(
            "| {route} | {market} | {variant} | `{status}` | `{hits}` | `{source_products}` | `{product_urls}` | `{decision}` |".format(
                route=check["route"],
                market=check["market"],
                variant=check["variant"],
                status=check["status"],
                hits=check["supplier_or_url_brand_hits"],
                source_products=check["source_product_count"],
                product_urls=check["product_url_count"],
                decision=check["decision"],
            )
        )

    product_lines = []
    for product in product_rows:
        product_lines.append(
            f"| `{product['route']}` | `{product['handle']}` | `{product['product_id']}` | `{product['type']}` | `{product['source_domain']}` | `{product['recommended_action']}` |"
        )

    keyword_lines = []
    for row in keyword_rows:
        keyword_lines.append(
            f"| {row['market']} | `{row['keyword']}` | `{row['threshold']}` | `{row['landing_route']}` | `{row['live_action']}` |"
        )

    markdown = f"""# Collection Source Cleanup Approval Packet

Timestamp: 2026-05-14 15:38 EDT automation run

Scope: public/read-only storefront source readback for the remaining supplier-leaking collection routes in the paid-growth keyword universe. No Shopify Admin, Google Ads, Merchant, Pinterest, GA4/GTM, billing, feed, product, campaign, budget, bid, status, conversion, product-scope, or live theme write occurred.

## Result

`/collections/swimsuits` and `/collections/matching-dresses` still expose supplier-source URLs through Shopify automatic product JSON in public collection HTML. This is not the already-sanitized theme `data-analytics-*` attribute path.

Keep both routes excluded from paid traffic until one of these happens:

- exact owner-approved Shopify product/vendor source cleanup is performed for the product rows below and public source readback returns `0` supplier hits, or
- future paid keyword rows continue to use clean alternate routes such as `/collections/family-swimsuits`, `/collections/mommy-and-me`, or `/collections/matching-outfits`.

Dirty product counts by route:

- `/collections/swimsuits`: `{route_counts.get('/collections/swimsuits', 0)}`
- `/collections/matching-dresses`: `{route_counts.get('/collections/matching-dresses', 0)}`

Keyword-universe rows still pointing at these dirty routes:

- `/collections/swimsuits`: `{keyword_counts.get('/collections/swimsuits', 0)}`
- `/collections/matching-dresses`: `{keyword_counts.get('/collections/matching-dresses', 0)}`

## Public Route Readback

Leak-hit check counted `detail.1688.com`, `1688.com`, `alibaba.com`, `aliexpress.com`, `data-analytics-vendor=\"http`, and `data-item-brand=\"http`.

| Route | Market | Header variant | Status | Supplier/url-brand hits | Source-product count | Product URL count | Decision |
|---|---|---|---:|---:|---:|---:|---|
{chr(10).join(route_lines)}

## Product Rows Requiring Cleanup Or Exclusion

The raw source URL is intentionally not stored in this packet. Product handles, IDs, source domain, and public source counts are enough for cleanup approval without committing source URLs.

| Route | Product handle | Product ID | Type | Source domain | Required action |
|---|---|---:|---|---|---|
{chr(10).join(product_lines)}

## Keyword Rows Still On Dirty Routes

These are not live upload rows. They remain local-only until rerouted or the product/vendor source cleanup is approved and read back clean.

| Market | Keyword | Threshold | Landing route | Current action |
|---|---|---|---|---|
{chr(10).join(keyword_lines)}

## Exact Approval Packet If Owner Wants Cleanup

Approval phrase:

`Approve Shopify product/vendor source cleanup for the product handles in COLLECTION_SOURCE_CLEANUP_APPROVAL_PACKET.md. Do not change prices, status, publications, product scope, feeds, campaigns, budgets, bids, or conversion settings. After cleanup, run public source readbacks on /collections/swimsuits and /collections/matching-dresses for US/GB/CA/AU and keep rows excluded unless supplier hits are 0.`

Before-state readback:

- Save public source counts for both routes across `US`, `GB`, `CA`, and `AU` with `Accept: text/html` and `Accept: */*`.
- Confirm affected product handles are the same rows listed here.

After-state pass criteria:

- both routes return `200` for all four markets and both header variants,
- `detail.1688.com`, `1688.com`, `alibaba.com`, and `aliexpress.com` counts are `0`,
- URL-like analytics vendor or item brand hits are `0`,
- no local-inventory, warehouse, retail-store, or stale seasonal blocker is introduced.

## Guardrails

- This packet is not approval to edit Shopify Admin or product data.
- This packet is not Google Ads, Merchant, feed, title, product-group, bid, budget, status, or keyword-upload authority.
- Keep the current GB/CA/AU 36-row CPC validation packet on its clean canonical routes; do not move it back to these dirty routes.

## Files

- Route rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_route_rows.csv`
- Product rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_product_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_approval_summary.json`
- Generator: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/build_collection_source_cleanup_approval.py`
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    checks, products = route_checks()
    keyword_rows = keyword_rows_for_routes()
    dirty_counts = Counter(product["route"] for product in products)
    keyword_counts = Counter(row["landing_route"] for row in keyword_rows)
    summary: dict[str, object] = {
        "generated_at": "2026-05-14 15:38 EDT",
        "scope": "public_readonly_collection_source_cleanup_approval_packet",
        "routes": list(ROUTES),
        "markets": list(MARKETS),
        "route_checks": checks,
        "source_products": products,
        "keyword_rows": keyword_rows,
        "dirty_product_count_by_route": dict(dirty_counts),
        "keyword_count_by_route": dict(keyword_counts),
        "guardrail": "no_external_writes_no_upload_authority",
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_csv(ROUTE_ROWS_CSV, checks)
    write_csv(PRODUCT_ROWS_CSV, products)
    write_report(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
