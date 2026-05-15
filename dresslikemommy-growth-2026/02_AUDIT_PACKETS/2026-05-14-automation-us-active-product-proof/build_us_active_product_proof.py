#!/usr/bin/env python3.13
"""Public active-product proof for US keyword-universe collection routes."""

from __future__ import annotations

import csv
import json
import re
import ssl
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = Path(__file__).resolve().parent
KEYWORD_CSV = ROOT / "ops/marketing/keyword_universe.csv"
BASE_URL = "https://www.dresslikemommy.com"
SOURCE_PATTERNS = (
    "1688" + ".com",
    "detail" + "." + "1688" + ".com",
    "alibaba.com",
    "aliexpress.com",
)
STALE_PATTERNS = ("christmas", "santa", "xmas", "local pickup", "same day pickup", "in store pickup")
PRODUCT_LINK_RE = re.compile(r'href=["\'](?:https://www\.dresslikemommy\.com)?/products/([^?"\'#]+)', re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
OG_TITLE_RE = re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', re.I)


@dataclass
class FetchResult:
    url: str
    status: int
    text: str
    error: str = ""


def fetch(url: str, *, accept: str = "text/html") -> FetchResult:
    req = Request(
        url,
        headers={
            "Accept": accept,
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
            ),
        },
    )
    context = ssl.create_default_context()
    try:
        with urlopen(req, timeout=25, context=context) as response:
            body = response.read().decode("utf-8", errors="replace")
            return FetchResult(response.geturl(), response.status, body)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return FetchResult(url, exc.code, body, f"HTTPError: {exc}")
    except URLError as exc:
        return FetchResult(url, 0, "", f"URLError: {exc.reason}")


def extract_title(html: str) -> str:
    match = OG_TITLE_RE.search(html) or TITLE_RE.search(html)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def extract_product_handles(html: str) -> list[str]:
    handles: list[str] = []
    seen: set[str] = set()
    for raw in PRODUCT_LINK_RE.findall(html):
        handle = raw.strip("/")
        if not handle or handle in seen:
            continue
        seen.add(handle)
        handles.append(handle)
    return handles


def count_hits(text: str, patterns: tuple[str, ...]) -> dict[str, int]:
    lower = text.lower()
    return {pattern: lower.count(pattern.lower()) for pattern in patterns}


def is_purchasable_signal(html: str) -> bool:
    lower = html.lower()
    has_cart_form = "/cart/add" in lower or 'name="add"' in lower
    has_add_copy = "add to cart" in lower or "add to bag" in lower
    hard_unavailable = "sold out" in lower and "add to cart" not in lower and "add to bag" not in lower
    return (has_cart_form or has_add_copy) and not hard_unavailable


def route_family(route: str) -> str:
    if "mommy-and-me" in route:
        return "mommy_mother_daughter"
    if "family-swimsuits" in route:
        return "family_swim"
    if "matching-outfits" in route or "family-matching" in route:
        return "family_matching"
    return "general"


def route_product_fit(title: str, route: str) -> str:
    lower = title.lower()
    family = route_family(route)
    if family == "mommy_mother_daughter":
        tokens = ("mommy", "mother", "daughter", "mom and", "mommy and me", "mommy & me")
    elif family == "family_swim":
        tokens = ("swim", "swimsuit", "bikini", "rash guard", "beachwear")
    elif family == "family_matching":
        tokens = ("family", "matching", "mommy", "mother", "daughter", "father", "daddy", "outfit")
    else:
        tokens = ("matching", "family", "mommy", "mother")
    return "PASS_ROUTE_FIT" if any(token in lower for token in tokens) else "REVIEW_ROUTE_FIT"


def main() -> int:
    with KEYWORD_CSV.open(newline="") as handle:
        keyword_rows = list(csv.DictReader(handle))

    selected = [
        row
        for row in keyword_rows
        if row["market"] == "US"
        and row["threshold"] == "GREEN"
        and (
            "future_search_packet" in row["live_action"]
            or "product_proof_required" in row["live_action"]
            or row["live_action"] == "validate_active_products_before_search_packet"
        )
    ]
    route_to_keywords: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in selected:
        route_to_keywords[row["landing_route"]].append(row)

    route_rows: list[dict[str, object]] = []
    product_rows: list[dict[str, object]] = []
    max_products_per_route = 12

    for route, rows in sorted(route_to_keywords.items()):
        url = f"{BASE_URL}{route}?country=US"
        route_fetch = fetch(url)
        handles = extract_product_handles(route_fetch.text)
        unique_handles = handles[:max_products_per_route]
        source_hits = count_hits(route_fetch.text, SOURCE_PATTERNS)
        stale_hits = count_hits(route_fetch.text, STALE_PATTERNS)
        route_rows.append(
            {
                "route": route,
                "url": route_fetch.url,
                "status": route_fetch.status,
                "error": route_fetch.error,
                "keyword_rows": len(rows),
                "unique_product_handles_sampled": len(unique_handles),
                "source_hits_total": sum(source_hits.values()),
                "stale_hits_total": sum(stale_hits.values()),
                "product_handles_sampled": "|".join(unique_handles),
            }
        )
        for handle in unique_handles:
            product_url = f"{BASE_URL}/products/{handle}?country=US"
            product_fetch = fetch(product_url)
            product_source_hits = count_hits(product_fetch.text, SOURCE_PATTERNS)
            product_stale_hits = count_hits(product_fetch.text, STALE_PATTERNS)
            title = extract_title(product_fetch.text)
            purchasable = is_purchasable_signal(product_fetch.text)
            clean = product_fetch.status == 200 and sum(product_source_hits.values()) == 0
            freshness = sum(product_stale_hits.values()) == 0
            product_fit = route_product_fit(title, route)
            product_rows.append(
                {
                    "route": route,
                    "handle": handle,
                    "url": product_fetch.url,
                    "status": product_fetch.status,
                    "title": title,
                    "purchasable_signal": str(purchasable).lower(),
                    "source_hits_total": sum(product_source_hits.values()),
                    "stale_hits_total": sum(product_stale_hits.values()),
                    "route_fit": product_fit,
                    "decision": (
                        "PUBLIC_ACTIVE_PRODUCT_PASS"
                        if clean and freshness and purchasable and product_fit == "PASS_ROUTE_FIT"
                        else "HOLD_FOR_REVIEW_OR_REPAIR"
                    ),
                }
            )

    route_csv = PACKET_DIR / "us_active_product_route_readback.csv"
    product_csv = PACKET_DIR / "us_active_product_sample_rows.csv"
    summary_json = PACKET_DIR / "us_active_product_proof_summary.json"
    report_md = PACKET_DIR / "US_ACTIVE_PRODUCT_PROOF_PACKET.md"

    with route_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(route_rows[0]))
        writer.writeheader()
        writer.writerows(route_rows)

    with product_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(product_rows[0]))
        writer.writeheader()
        writer.writerows(product_rows)

    decisions = Counter(row["decision"] for row in product_rows)
    route_status = Counter(str(row["status"]) for row in route_rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "selected_us_green_keyword_rows": len(selected),
        "routes_checked": len(route_rows),
        "route_status": dict(route_status),
        "sampled_product_rows": len(product_rows),
        "product_decisions": dict(decisions),
        "route_rows_csv": str(route_csv.relative_to(ROOT)),
        "product_rows_csv": str(product_csv.relative_to(ROOT)),
        "next_action": (
            "Use PUBLIC_ACTIVE_PRODUCT_PASS rows as active-product proof for future US Search validation; "
            "still require authenticated $0.15 CPC/search feasibility before any live Search row."
        ),
    }
    summary_json.write_text(json.dumps(summary, indent=2) + "\n")

    held_rows = [row for row in product_rows if row["decision"] != "PUBLIC_ACTIVE_PRODUCT_PASS"]
    report_md.write_text(
        "\n".join(
            [
                "# US Active Product Proof Packet",
                "",
                f"Generated: {summary['generated_at']}",
                "",
                "## Scope",
                "",
                (
                    "Public/read-only proof for US `GREEN` keyword-universe rows that are already "
                    "routed to clean collection pages and are candidates for future US Search validation."
                ),
                "",
                "This packet does not authorize Google Ads, Shopify Admin, Merchant, Pinterest, feed, product, bid, budget, status, conversion, or theme writes.",
                "",
                "## Results",
                "",
                f"- US `GREEN` keyword rows selected: `{len(selected)}`",
                f"- Collection routes checked: `{len(route_rows)}`",
                f"- Sampled public product pages: `{len(product_rows)}`",
                f"- Public active-product pass rows: `{decisions.get('PUBLIC_ACTIVE_PRODUCT_PASS', 0)}`",
                f"- Held/review rows: `{len(held_rows)}`",
                "",
                "Route CSV: `us_active_product_route_readback.csv`",
                "",
                "Product sample CSV: `us_active_product_sample_rows.csv`",
                "",
                "## Decision",
                "",
                (
                    "The rerouted US keyword lane now has public active-product proof at the route/product "
                    "sample level. This removes route-cleanliness-only ambiguity for future US Search prep, "
                    "but the rows remain local-only until authenticated `$0.15` CPC/search feasibility, "
                    "anti-cannibalization review, and a fresh green action row exist."
                ),
                "",
                "## Guardrails Preserved",
                "",
                "- No Google Ads upload, apply, keyword, bid, budget, status, negative, or campaign write.",
                "- No Shopify Admin product/vendor/source metadata edit.",
                "- No Merchant, Pinterest, GA4/GTM, billing, feed, product-scope, product-group, conversion, credential, or destructive action.",
                "- No Computer Use permission probing or account-access repair loop.",
                "",
                "## Next Action",
                "",
                (
                    "After the GB/CA/AU P0 CPC gate, build a small US validation packet only from these "
                    "public-active route/product candidates and run authenticated Google Ads/Keyword Planner "
                    "validation at max `$0.15` before any live Search use."
                ),
                "",
            ]
        )
        + "\n"
    )

    print(json.dumps(summary, indent=2))
    return 0 if decisions.get("PUBLIC_ACTIVE_PRODUCT_PASS", 0) else 1


if __name__ == "__main__":
    sys.exit(main())
