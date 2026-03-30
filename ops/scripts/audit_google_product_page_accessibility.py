#!/usr/bin/env python3
"""Audit live storefront accessibility for active Google-published products."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib import error, parse, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402
from ops.scripts.shopify_catalog_cleanup import ShopifyClient, discover_publications, fetch_products  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3z-google-page-accessibility-audit")
DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
TIMEOUT_SECONDS = 30
HTML_LIMIT_BYTES = 250_000


@dataclass
class FetchResult:
    requested_url: str
    final_url: str
    http_status: int
    content_type: str
    x_robots_tag: str
    meta_robots: str
    title: str
    blocked_reasons: list[str]
    fetched: bool
    error: str


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def extract_meta_robots(html_text: str) -> str:
    match = re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
        html_text,
        flags=re.IGNORECASE,
    )
    return clean(unescape(match.group(1))) if match else ""


def extract_title(html_text: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    return clean(unescape(match.group(1))) if match else ""


def classify_blockers(*, requested_url: str, final_url: str, status: int, x_robots_tag: str, meta_robots: str, html_text: str) -> list[str]:
    blockers: list[str] = []
    requested_host = parse.urlparse(requested_url).netloc.lower()
    final_parsed = parse.urlparse(final_url)
    final_host = final_parsed.netloc.lower()

    if status != 200:
        blockers.append(f"http_status:{status}")
    if final_host and final_host != requested_host:
        blockers.append(f"redirect_off_domain:{final_host}")
    if "/password" in final_parsed.path:
        blockers.append("password_page")

    x_robots_lower = x_robots_tag.lower()
    meta_robots_lower = meta_robots.lower()
    if "noindex" in x_robots_lower or "none" in x_robots_lower:
        blockers.append(f"x_robots:{x_robots_tag}")
    if "noindex" in meta_robots_lower or "none" in meta_robots_lower:
        blockers.append(f"meta_robots:{meta_robots}")

    lowered_html = html_text.lower()
    if "opening soon" in lowered_html:
        blockers.append("opening_soon")
    if "store unavailable" in lowered_html:
        blockers.append("store_unavailable")
    if "sorry, this page is not available" in lowered_html:
        blockers.append("page_not_available_text")

    deduped: list[str] = []
    seen: set[str] = set()
    for blocker in blockers:
        if blocker not in seen:
            seen.add(blocker)
            deduped.append(blocker)
    return deduped


def fetch_url(url: str, user_agent: str) -> FetchResult:
    req = request.Request(url, headers={"User-Agent": user_agent})
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            final_url = response.geturl()
            status = getattr(response, "status", 200)
            content_type = clean(response.headers.get("Content-Type", ""))
            x_robots = clean(response.headers.get("X-Robots-Tag", ""))
            body = response.read(HTML_LIMIT_BYTES)
    except error.HTTPError as exc:
        return FetchResult(
            requested_url=url,
            final_url=exc.geturl() or url,
            http_status=exc.code,
            content_type=clean(exc.headers.get("Content-Type", "")) if exc.headers else "",
            x_robots_tag=clean(exc.headers.get("X-Robots-Tag", "")) if exc.headers else "",
            meta_robots="",
            title="",
            blocked_reasons=[f"http_status:{exc.code}"],
            fetched=False,
            error=clean(exc.reason),
        )
    except Exception as exc:  # noqa: BLE001
        return FetchResult(
            requested_url=url,
            final_url=url,
            http_status=0,
            content_type="",
            x_robots_tag="",
            meta_robots="",
            title="",
            blocked_reasons=[f"fetch_error:{exc.__class__.__name__}"],
            fetched=False,
            error=clean(str(exc)),
        )

    html_text = body.decode("utf-8", errors="replace") if "html" in content_type.lower() else ""
    meta_robots = extract_meta_robots(html_text)
    title = extract_title(html_text)
    blockers = classify_blockers(
        requested_url=url,
        final_url=final_url,
        status=status,
        x_robots_tag=x_robots,
        meta_robots=meta_robots,
        html_text=html_text,
    )
    return FetchResult(
        requested_url=url,
        final_url=final_url,
        http_status=status,
        content_type=content_type,
        x_robots_tag=x_robots,
        meta_robots=meta_robots,
        title=title,
        blocked_reasons=blockers,
        fetched=True,
        error="",
    )


def write_csv(path: Path, rows: Iterable[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit page accessibility for active Google-published Shopify products.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for audit artifacts.")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for product rows.")
    parser.add_argument("--pause-ms", type=int, default=100, help="Pause between product fetches.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    publications = discover_publications(client)
    products = [
        product
        for product in fetch_products(client, publications)
        if product.status == "ACTIVE" and product.google_published
    ]
    if args.limit > 0:
        products = products[: args.limit]

    rows: list[dict[str, str]] = []
    blocked_counts = {"desktop": 0, "mobile": 0, "either": 0}
    blocked_handles: list[str] = []

    for index, product in enumerate(products, start=1):
        desktop = fetch_url(product.online_store_url, DESKTOP_UA)
        mobile = fetch_url(product.online_store_url, MOBILE_UA)
        desktop_blocked = bool(desktop.blocked_reasons)
        mobile_blocked = bool(mobile.blocked_reasons)
        either_blocked = desktop_blocked or mobile_blocked
        if desktop_blocked:
            blocked_counts["desktop"] += 1
        if mobile_blocked:
            blocked_counts["mobile"] += 1
        if either_blocked:
            blocked_counts["either"] += 1
            blocked_handles.append(product.handle)

        rows.append(
            {
                "product_id": product.product_id,
                "handle": product.handle,
                "title": product.title,
                "online_store_url": product.online_store_url,
                "desktop_http_status": str(desktop.http_status),
                "desktop_final_url": desktop.final_url,
                "desktop_x_robots_tag": desktop.x_robots_tag,
                "desktop_meta_robots": desktop.meta_robots,
                "desktop_title": desktop.title,
                "desktop_blocked_reasons": "|".join(desktop.blocked_reasons),
                "desktop_error": desktop.error,
                "mobile_http_status": str(mobile.http_status),
                "mobile_final_url": mobile.final_url,
                "mobile_x_robots_tag": mobile.x_robots_tag,
                "mobile_meta_robots": mobile.meta_robots,
                "mobile_title": mobile.title,
                "mobile_blocked_reasons": "|".join(mobile.blocked_reasons),
                "mobile_error": mobile.error,
                "blocked_on_either": "true" if either_blocked else "false",
            }
        )
        if args.pause_ms > 0 and index < len(products):
            time.sleep(args.pause_ms / 1000.0)

    fieldnames = [
        "product_id",
        "handle",
        "title",
        "online_store_url",
        "desktop_http_status",
        "desktop_final_url",
        "desktop_x_robots_tag",
        "desktop_meta_robots",
        "desktop_title",
        "desktop_blocked_reasons",
        "desktop_error",
        "mobile_http_status",
        "mobile_final_url",
        "mobile_x_robots_tag",
        "mobile_meta_robots",
        "mobile_title",
        "mobile_blocked_reasons",
        "mobile_error",
        "blocked_on_either",
    ]
    write_csv(output_dir / "google_product_page_accessibility_audit.csv", rows, fieldnames)

    blocked_rows = [row for row in rows if row["blocked_on_either"] == "true"]
    write_csv(output_dir / "google_product_page_accessibility_blocked.csv", blocked_rows, fieldnames)

    summary = {
        "audited_google_published_active_products": len(products),
        "blocked_counts": blocked_counts,
        "blocked_handles": blocked_handles,
        "output_dir": str(output_dir),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
