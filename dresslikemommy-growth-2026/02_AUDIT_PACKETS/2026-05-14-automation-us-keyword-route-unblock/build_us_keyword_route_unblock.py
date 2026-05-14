#!/usr/bin/env python3
"""Reroute US keyword-universe rows away from dirty/broken collection routes.

This is a repo-local/public-readback action only. It does not create or upload
Google Ads rows and does not touch Shopify Admin, Merchant, Pinterest, GA4/GTM,
campaign budgets, bids, statuses, product data, feeds, or live themes.
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

REPORT_MD = PACKET_DIR / "US_KEYWORD_ROUTE_UNBLOCK_PACKET.md"
SUMMARY_JSON = PACKET_DIR / "us_keyword_route_unblock_summary.json"
REROUTE_ROWS_CSV = PACKET_DIR / "us_keyword_route_unblock_rows.csv"
ROUTE_READBACK_CSV = PACKET_DIR / "us_keyword_route_unblock_public_route_readback.csv"

BASE_URL = "https://www.dresslikemommy.com"
BAD_OR_RISKY_ROUTES = {
    "/collections/vacation",
    "/collections/matching-dresses",
    "/collections/swimsuits",
    "/collections/daddy-and-me",
}
LEAK_PATTERNS = (
    "detail.1688.com",
    "1688.com",
    "alibaba.com",
    "aliexpress.com",
    'data-analytics-vendor="http',
    'data-item-brand="http',
)
REPUTATION_PATTERNS = ("Christmas", "Santa", "Xmas", "local inventory", "warehouse", "retail store")


def destination_for(row: dict[str, str]) -> tuple[str, str]:
    route = row["landing_route"]
    category = row["category"].lower()
    keyword = row["keyword"].lower()

    if route == "/collections/swimsuits":
        return (
            "/collections/family-swimsuits",
            "rerouted_us_from_supplier_leaking_swimsuits_to_clean_family_swimsuits_route_product_proof_required",
        )
    if route == "/collections/matching-dresses":
        return (
            "/collections/mommy-and-me",
            "rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required",
        )
    if route == "/collections/daddy-and-me":
        return (
            "/collections/matching-outfits",
            "rerouted_us_from_daddy_route_to_clean_family_matching_route_product_proof_required",
        )
    if route == "/collections/vacation":
        if any(token in category or token in keyword for token in ("tropical", "hawaiian", "cruise", "resort", "vacation")):
            return (
                "/collections/matching-outfits",
                "rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required",
            )
        return (
            "/collections/matching-outfits",
            "rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required",
        )
    raise ValueError(f"no destination rule for {route}")


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth US route unblock readback",
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


def public_route_readbacks(routes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    variants = (
        ("text_html", "text/html,application/xhtml+xml"),
        ("star_cache_busted", "*/*"),
    )
    for route in routes:
        for variant, accept in variants:
            suffix = "?country=US"
            if variant == "star_cache_busted":
                suffix = f"?country=US&_dlm_cb={int(time.time())}"
            url = f"{BASE_URL}{route}{suffix}"
            status, final_url, page = fetch(url, accept)
            leak_counts = {pattern: page.count(pattern) for pattern in LEAK_PATTERNS}
            reputation_counts = {pattern: page.count(pattern) for pattern in REPUTATION_PATTERNS}
            rows.append(
                {
                    "route": route,
                    "variant": variant,
                    "url": url,
                    "final_url": final_url,
                    "status": status,
                    "redirected": final_url.split("?", 1)[0] != f"{BASE_URL}{route}",
                    "title": page_title(page),
                    "supplier_or_url_brand_hits": sum(leak_counts.values()),
                    "reputation_hits": sum(reputation_counts.values()),
                    "product_url_count": len(set(re.findall(r"/products/[-a-z0-9]+", page))),
                    "decision": "route_clean_for_us_local_validation" if status == 200 and sum(leak_counts.values()) == 0 and sum(reputation_counts.values()) == 0 else "hold_route",
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_keyword_universe(rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with KEYWORD_UNIVERSE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(summary: dict[str, object]) -> None:
    reroute_rows = summary["reroute_rows"]
    readback_rows = summary["route_readbacks"]
    reroute_counts = summary["reroute_count_by_destination"]

    reroute_lines = [
        "| {row_number} | `{keyword}` | {threshold} | `{old_route}` | `{new_route}` | `{new_live_action}` |".format(**row)
        for row in reroute_rows
    ]
    readback_lines = [
        "| {route} | {variant} | `{status}` | `{redirected}` | `{supplier_or_url_brand_hits}` | `{reputation_hits}` | `{product_url_count}` | `{decision}` |".format(**row)
        for row in readback_rows
    ]

    markdown = f"""# US Keyword Route Unblock Packet

Timestamp: 2026-05-14 automation run

Scope: repo-local update to `ops/marketing/keyword_universe.csv` plus public/read-only storefront source checks for replacement US routes. No Google Ads upload/apply/import/add keyword/bid/budget/status/negative action occurred. No Shopify Admin product/vendor/source edit, live theme push, Merchant, Pinterest, GA4/GTM, billing, product-scope, product-group, feed, or conversion write occurred.

## Result

Rerouted `{summary['rerouted_row_count']}` US keyword-universe rows away from broken or supplier-risk routes:

- `/collections/vacation`: broken/held route.
- `/collections/matching-dresses`: supplier-source risk from automatic Shopify product JSON.
- `/collections/swimsuits`: supplier-source risk from automatic Shopify product JSON.
- `/collections/daddy-and-me`: conservative reroute away from the previously flagged seasonal-metadata route before future paid use.

Replacement destinations:

- `/collections/matching-outfits`: `{reroute_counts.get('/collections/matching-outfits', 0)}` rows.
- `/collections/mommy-and-me`: `{reroute_counts.get('/collections/mommy-and-me', 0)}` rows.
- `/collections/family-swimsuits`: `{reroute_counts.get('/collections/family-swimsuits', 0)}` rows.

Public US readback on the replacement routes returned `200` with `0` supplier/source-domain or URL-brand hits and `0` stale seasonal/local-inventory trust hits across both header variants. These rows are still local-only; they need active-product proof, authenticated CPC/search validation, reviewer pass, and a fresh action-queue `GREEN` row before any live Search use.

## Public Replacement Route Readback

| Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URL count | Decision |
|---|---|---:|---|---:|---:|---:|---|
{chr(10).join(readback_lines)}

## Rerouted Keyword Rows

| CSV row | Keyword | Threshold | Old route | New route | New action |
|---:|---|---|---|---|---|
{chr(10).join(reroute_lines)}

## Decision

This closes the local dirty-route gap for US keyword-universe planning. It does not make the US rows live-ready. The next US paid action remains:

1. Run authenticated Standard Shopping item-level export for campaign `23802638621` and join it to the public-clean scope.
2. For future US Search, build a small validation packet from these rerouted rows only after active-product fit and `$0.15` CPC/search feasibility are proved.
3. Keep the original dirty collection routes excluded until product/vendor source cleanup is approved and read back clean.
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")


def main() -> None:
    with KEYWORD_UNIVERSE.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    reroute_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=2):
        if row["market"] != "US" or row["landing_route"] not in BAD_OR_RISKY_ROUTES:
            continue
        old_route = row["landing_route"]
        new_route, new_action = destination_for(row)
        row["landing_route"] = new_route
        row["live_action"] = new_action
        reroute_rows.append(
            {
                "row_number": index,
                "market": row["market"],
                "category": row["category"],
                "keyword": row["keyword"],
                "threshold": row["threshold"],
                "promotion_status": row["promotion_status"],
                "old_route": old_route,
                "new_route": new_route,
                "new_live_action": new_action,
                "total_score": row["total_score"],
            }
        )

    if not reroute_rows:
        raise SystemExit("No US rows required rerouting")

    routes = sorted({str(row["new_route"]) for row in reroute_rows})
    readbacks = public_route_readbacks(routes)
    failures = [
        row for row in readbacks
        if row["status"] != 200 or row["supplier_or_url_brand_hits"] != 0 or row["reputation_hits"] != 0
    ]
    if failures:
        raise SystemExit(f"Replacement route readback failed: {failures}")

    write_keyword_universe(rows, fieldnames)
    write_csv(REROUTE_ROWS_CSV, reroute_rows)
    write_csv(ROUTE_READBACK_CSV, readbacks)

    summary = {
        "source": str(KEYWORD_UNIVERSE.relative_to(ROOT)),
        "rerouted_row_count": len(reroute_rows),
        "reroute_count_by_old_route": dict(Counter(str(row["old_route"]) for row in reroute_rows)),
        "reroute_count_by_destination": dict(Counter(str(row["new_route"]) for row in reroute_rows)),
        "route_readback_count": len(readbacks),
        "route_readback_failures": 0,
        "route_readbacks": readbacks,
        "reroute_rows": reroute_rows,
        "guardrails": [
            "repo_local_keyword_universe_only",
            "public_storefront_readback_only",
            "no_google_ads_upload_or_keyword_write",
            "no_shopify_admin_or_live_theme_write",
            "no_merchant_pinterest_ga4_gtm_billing_feed_product_conversion_write",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_report(summary)
    print(json.dumps({k: summary[k] for k in ("rerouted_row_count", "reroute_count_by_old_route", "reroute_count_by_destination", "route_readback_count")}, indent=2))


if __name__ == "__main__":
    main()
