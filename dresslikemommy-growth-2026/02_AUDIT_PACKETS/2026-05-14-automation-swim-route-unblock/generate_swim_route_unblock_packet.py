#!/usr/bin/env python3
"""Build the GB/CA/AU swim-route unblock packet.

This is a public/read-only storefront check plus a local keyword-universe
reroute. It does not touch Google Ads, Shopify Admin, Merchant, Pinterest, or
any live account surface.
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
KEYWORD_UNIVERSE = ROOT / "ops/marketing/keyword_universe.csv"
VALIDATION_CSV = PACKET_DIR / "gb_ca_au_36_clean_route_cpc_validation_rows.csv"
SUMMARY_JSON = PACKET_DIR / "gb_ca_au_swim_route_unblock_summary.json"
REPORT_MD = PACKET_DIR / "GB_CA_AU_SWIM_ROUTE_UNBLOCK_AND_36_ROW_CPC_PACKET.md"

MARKETS = ("GB", "CA", "AU")
ROUTE = "/collections/family-swimsuits"
BASE_URL = "https://www.dresslikemommy.com"
LEAK_PATTERNS = (
    "detail.1688.com",
    "1688.com",
    "alibaba.com",
    "aliexpress.com",
    'data-analytics-vendor="http',
    'data-item-brand="http',
)
REPUTATION_PATTERNS = ("Christmas", "local inventory", "warehouse", "retail store")
CAMPAIGN_MAP = {
    "GB": {
        "campaign_id": "23838895360",
        "ad_group_id": "194138528537",
        "campaign_name_hint": "GB_intl_search",
    },
    "CA": {
        "campaign_id": "23834423669",
        "ad_group_id": "196679079575",
        "campaign_name_hint": "CA_intl_search",
    },
    "AU": {
        "campaign_id": "23834424182",
        "ad_group_id": "198852670520",
        "campaign_name_hint": "AU_intl_search",
    },
}


def fetch(url: str, accept: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "Mozilla/5.0 DLM paid-growth route readback",
        },
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=30, context=context) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def check_route() -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    variants = (
        ("text/html", "text/html,application/xhtml+xml"),
        ("star", "*/*"),
    )
    for market in MARKETS:
        for variant_name, accept in variants:
            suffix = f"?country={market}"
            if variant_name == "star":
                suffix = f"?country={market}&_dlm_cb={int(time.time())}"
            url = f"{BASE_URL}{ROUTE}{suffix}"
            status, html = fetch(url, accept)
            lower = html.lower()
            leak_counts = {pattern: html.count(pattern) for pattern in LEAK_PATTERNS}
            reputation_counts = {pattern: html.count(pattern) for pattern in REPUTATION_PATTERNS}
            product_urls = len(set(re.findall(r"/products/[-a-z0-9]+", html)))
            checks.append(
                {
                    "market": market,
                    "variant": variant_name,
                    "url": url,
                    "status": status,
                    "title": page_title(html),
                    "supplier_or_url_brand_hits": sum(leak_counts.values()),
                    "leak_counts": leak_counts,
                    "reputation_counts": reputation_counts,
                    "product_url_count": product_urls,
                    "has_family_swim_copy": "family swim" in lower
                    or "matching family swimsuit" in lower
                    or "family-swimsuits" in lower,
                    "has_ships_to_signal": "ships to" in lower,
                }
            )
    return checks


def load_keyword_rows() -> tuple[list[dict[str, str]], list[str]]:
    with KEYWORD_UNIVERSE.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def update_keyword_universe(rows: list[dict[str, str]], fieldnames: list[str]) -> list[dict[str, str]]:
    changed: list[dict[str, str]] = []
    for row in rows:
        if (
            row["market"] in MARKETS
            and row["threshold"] == "GREEN"
            and row["category"] == "Swimsuits"
            and row["landing_route"] == "/collections/swimsuits"
        ):
            row["landing_route"] = ROUTE
            row["live_action"] = (
                "rerouted_from_supplier_leaking_swimsuits_to_clean_family_swimsuits_"
                "route_cpc_validation_required"
            )
            changed.append(dict(row))

    with KEYWORD_UNIVERSE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return changed


def validation_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        if row["market"] not in MARKETS:
            continue
        if row["threshold"] != "GREEN":
            continue
        if "cpc_validation_required" not in row["live_action"]:
            continue

        campaign = CAMPAIGN_MAP[row["market"]]
        out.append(
            {
                "market": row["market"],
                "language": row["language"],
                "campaign_id": campaign["campaign_id"],
                "ad_group_id": campaign["ad_group_id"],
                "campaign_name_hint": campaign["campaign_name_hint"],
                "ad_group_name": "Mommy & Me Dresses - Exact",
                "keyword": row["keyword"],
                "match_candidate": row["match_candidate"],
                "landing_route": row["landing_route"],
                "final_url_to_validate": f"{BASE_URL}{row['landing_route']}?country={row['market']}",
                "total_score": row["total_score"],
                "category": row["category"],
                "live_action": row["live_action"],
                "validation_required": "keyword_planner_or_keyword_ui_max_cpc_0.15_no_upload",
                "pass_gate": (
                    "Eligible/forecast auction entry at max CPC <= $0.15 with no "
                    "below-first-page warning and no policy/destination issue"
                ),
                "fail_gate": (
                    "First-page/top-of-page/forecast CPC > $0.15, low search volume/no auction entry, "
                    "policy/destination issue, duplicate/cannibalized intent, or landing mismatch"
                ),
                "if_pass": "candidate_for_small_exact_phrase_batch_after_fresh_ads_readback_and_reviewer_pass",
                "if_fail": "keep_local_do_not_upload; note reason in action_queue_and_scorecard",
            }
        )
    return sorted(out, key=lambda item: (item["market"], -int(item["total_score"]), item["keyword"]))


def write_validation_csv(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError("No validation rows generated")
    with VALIDATION_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(summary: dict[str, object]) -> None:
    checks = summary["route_checks"]
    changed = summary["rerouted_rows"]
    counts = summary["validation_counts_by_market"]

    route_lines = []
    for check in checks:
        route_lines.append(
            "| {market} | {variant} | `{status}` | `{supplier_or_url_brand_hits}` | `{product_url_count}` | {family} | `{title}` |".format(
                market=check["market"],
                variant=check["variant"],
                status=check["status"],
                supplier_or_url_brand_hits=check["supplier_or_url_brand_hits"],
                product_url_count=check["product_url_count"],
                family=str(check["has_family_swim_copy"]),
                title=check["title"],
            )
        )

    row_lines = []
    for row in changed:
        row_lines.append(
            f"| {row['market']} | `{row['keyword']}` | `{row['landing_route']}` | `{row['total_score']}` |"
        )

    markdown = f"""# GB/CA/AU Swim Route Unblock And 36-Row CPC Packet

Timestamp: 2026-05-14 automation run

Scope: public/read-only storefront readback plus repo-local keyword-universe reroute. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

`/collections/family-swimsuits` is a cleaner, product-relevant route for the five held GB/CA/AU swimwear keyword rows. It returned `200` in GB, CA, and AU across both public header variants and showed `0` supplier/source-domain or URL-like brand hits.

Updated `ops/marketing/keyword_universe.csv` so the five GB/CA/AU swimwear rows now route to `/collections/family-swimsuits` and require authenticated `$0.15` CPC validation instead of staying blocked on `/collections/swimsuits`.

The exact authenticated validation packet is now `{summary['validation_row_count']}` rows:

- GB: `{counts.get('GB', 0)}`
- CA: `{counts.get('CA', 0)}`
- AU: `{counts.get('AU', 0)}`

## Route Readback

Leak-hit check counted `detail.1688.com`, `1688.com`, `alibaba.com`, `aliexpress.com`, `data-analytics-vendor=\"http`, and `data-item-brand=\"http`.

| Market | Header variant | Status | Supplier/url-brand hits | Product URL count | Family swim copy | Title |
|---|---|---:|---:|---:|---|---|
{chr(10).join(route_lines)}

## Rerouted Rows

| Market | Keyword | New route | Score |
|---|---|---|---:|
{chr(10).join(row_lines)}

## Exact Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for `gb_ca_au_36_clean_route_cpc_validation_rows.csv` at max CPC `$0.15`. This packet does not authorize upload/apply/add keyword/bid/status/budget/negative changes.

If a row passes, it can become a candidate for a small exact/phrase batch only after fresh Ads readback, Marketing Safety Reviewer pass, exact action-queue row, and after-state readback plan. If it fails, keep it local and record the reason.

## Files

- Row CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_swim_route_unblock_summary.json`
- Generator: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/generate_swim_route_unblock_packet.py`
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    route_checks = check_route()
    if any(check["status"] != 200 for check in route_checks):
        raise RuntimeError("family-swimsuits route did not return 200 in every check")
    if any(check["supplier_or_url_brand_hits"] != 0 for check in route_checks):
        raise RuntimeError("family-swimsuits route still has supplier/url-brand hits")

    rows, fieldnames = load_keyword_rows()
    changed = update_keyword_universe(rows, fieldnames)
    rows, _ = load_keyword_rows()
    candidates = validation_rows(rows)
    write_validation_csv(candidates)

    counts = Counter(row["market"] for row in candidates)
    summary = {
        "generated_at": "2026-05-14",
        "route": ROUTE,
        "route_checks": route_checks,
        "rerouted_row_count": len(changed),
        "rerouted_rows": changed,
        "validation_row_count": len(candidates),
        "validation_counts_by_market": dict(counts),
        "validation_csv": str(VALIDATION_CSV.relative_to(ROOT)),
        "keyword_universe": str(KEYWORD_UNIVERSE.relative_to(ROOT)),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
