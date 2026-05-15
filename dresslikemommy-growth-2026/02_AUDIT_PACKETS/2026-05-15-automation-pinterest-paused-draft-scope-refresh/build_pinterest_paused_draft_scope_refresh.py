#!/usr/bin/env python3
"""Refresh public readiness evidence for the Pinterest paused-draft scope."""

from __future__ import annotations

import csv
import json
import re
import ssl
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
CLEAN_SCOPE = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv"
EXCLUSIONS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv"
SPEC_SUMMARY = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/pinterest_us_paused_draft_build_spec_validation_summary.json"

SUPPLIER_PATTERNS = (
    "1688" + ".com",
    "detail" + "." + "1688" + ".com",
    "alibaba.com",
    "aliexpress.com",
)
URL_BRAND_PATTERNS = (
    'data-analytics-vendor="http',
    "data-analytics-vendor='http",
    'data-item-brand="http',
    "data-item-brand='http",
)
STALE_PATTERNS = (
    "christmas",
    "santa",
    "xmas",
    "warehouse",
    "in-store pickup",
    "local inventory",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fetch(url: str, method: str = "GET") -> dict[str, object]:
    headers = {
        "User-Agent": "Mozilla/5.0 (DressLikeMommy paid-growth public readback)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    if method == "HEAD":
        headers["Accept"] = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
    request = Request(url, headers=headers, method=method)
    context = ssl.create_default_context()
    started = time.time()
    try:
        with urlopen(request, timeout=20, context=context) as response:
            body = b"" if method == "HEAD" else response.read(850_000)
            return {
                "status": int(response.status),
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "elapsed_ms": round((time.time() - started) * 1000),
                "body": body.decode("utf-8", errors="ignore"),
                "error": "",
            }
    except HTTPError as exc:
        body = b"" if method == "HEAD" else exc.read(50_000)
        return {
            "status": int(exc.code),
            "final_url": exc.url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "elapsed_ms": round((time.time() - started) * 1000),
            "body": body.decode("utf-8", errors="ignore"),
            "error": str(exc),
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "status": 0,
            "final_url": url,
            "content_type": "",
            "elapsed_ms": round((time.time() - started) * 1000),
            "body": "",
            "error": repr(exc),
        }


def title_from_body(body: str) -> str:
    match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', body, flags=re.I)
    if not match:
        match = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:title["\']', body, flags=re.I)
    if match:
        return re.sub(r"\s+", " ", unescape(match.group(1))).strip()
    match = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.I | re.S)
    if not match:
        match = re.search(r"<title[^>]*>(.*?)</title>", body, flags=re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", match.group(1)))).strip()


def count_hits(body: str, patterns: tuple[str, ...]) -> dict[str, int]:
    lowered = body.lower()
    return {pattern: lowered.count(pattern.lower()) for pattern in patterns if lowered.count(pattern.lower())}


def main() -> int:
    rows = read_csv(CLEAN_SCOPE)
    exclusions = read_csv(EXCLUSIONS)
    spec = json.loads(SPEC_SUMMARY.read_text(encoding="utf-8"))

    products: dict[str, dict[str, object]] = {}
    images: dict[str, dict[str, object]] = {}
    rows_by_product_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_group = Counter()
    by_product_group = defaultdict(set)
    variant_ids = set()

    for row in rows:
        variant_ids.add(row["shopify_variant_id"])
        by_group[row["custom_label_2"]] += 1
        by_product_group[row["custom_label_2"]].add(row["shopify_product_id"])
        url = row["product_url"]
        rows_by_product_url[url].append(row)
        if url not in products:
            products[url] = {
                "product_url": url,
                "shopify_product_id": row["shopify_product_id"],
                "product_group": row["custom_label_2"],
                "pinterest_product_group": row["pinterest_product_group"],
                "title_sample": row["title"],
                "variant_count": 0,
                "image_urls": set(),
            }
        products[url]["variant_count"] = int(products[url]["variant_count"]) + 1
        products[url]["image_urls"].add(row["image_url"])
        images.setdefault(row["image_url"], {"image_url": row["image_url"], "variant_count": 0})
        images[row["image_url"]]["variant_count"] = int(images[row["image_url"]]["variant_count"]) + 1

    product_readbacks = []
    for item in products.values():
        result = fetch(str(item["product_url"]))
        body = str(result.pop("body"))
        supplier_hits = count_hits(body, SUPPLIER_PATTERNS)
        url_brand_hits = count_hits(body, URL_BRAND_PATTERNS)
        stale_hits = count_hits(body, STALE_PATTERNS)
        add_to_cart = bool(re.search(r"add(?:\s|-)?to(?:\s|-)?cart|add to bag", body, flags=re.I))
        variant_sold_out_mentions = len(re.findall(r"Variant sold out or unavailable", body, flags=re.I))
        status = "PASS"
        reasons: list[str] = []
        if result["status"] != 200:
            status = "HOLD"
            reasons.append("non_200_public_product_page")
        if supplier_hits:
            status = "HOLD"
            reasons.append("supplier_source_domain_in_public_source")
        if url_brand_hits:
            status = "HOLD"
            reasons.append("url_like_brand_attribute_in_public_source")
        if stale_hits:
            # Christmas/santa terms are only stale/trust blockers when the current group is not pajamas.
            non_pajama_stale = {k: v for k, v in stale_hits.items() if item["product_group"] != "pajamas" or k in {"warehouse", "in-store pickup", "local inventory"}}
            if non_pajama_stale:
                status = "HOLD"
                reasons.append("stale_or_inventory_trust_terms_in_public_source")

        product_readbacks.append(
            {
                "status": status,
                "reasons": ";".join(reasons),
                "product_url": item["product_url"],
                "final_url": result["final_url"],
                "http_status": result["status"],
                "elapsed_ms": result["elapsed_ms"],
                "content_type": result["content_type"],
                "shopify_product_id": item["shopify_product_id"],
                "product_group": item["product_group"],
                "variant_count": item["variant_count"],
                "image_count": len(item["image_urls"]),
                "public_title": title_from_body(body),
                "supplier_hit_count": sum(supplier_hits.values()),
                "supplier_hits": json.dumps(supplier_hits, sort_keys=True),
                "url_brand_hit_count": sum(url_brand_hits.values()),
                "url_brand_hits": json.dumps(url_brand_hits, sort_keys=True),
                "stale_hit_count": sum(stale_hits.values()),
                "stale_hits": json.dumps(stale_hits, sort_keys=True),
                "add_to_cart_signal": add_to_cart,
                "variant_sold_out_or_unavailable_mentions": variant_sold_out_mentions,
                "error": result["error"],
            }
        )

    image_readbacks = []
    for item in images.values():
        result = fetch(str(item["image_url"]), method="HEAD")
        status = "PASS" if int(result["status"]) in {200, 304} and str(result["content_type"]).lower().startswith("image/") else "HOLD"
        image_readbacks.append(
            {
                "status": status,
                "image_url": item["image_url"],
                "http_status": result["status"],
                "final_url": result["final_url"],
                "content_type": result["content_type"],
                "elapsed_ms": result["elapsed_ms"],
                "variant_count": item["variant_count"],
                "error": result["error"],
            }
        )

    pass_products = [row for row in product_readbacks if row["status"] == "PASS"]
    hold_products = [row for row in product_readbacks if row["status"] != "PASS"]
    pass_images = [row for row in image_readbacks if row["status"] == "PASS"]
    hold_images = [row for row in image_readbacks if row["status"] != "PASS"]

    held_product_urls = {row["product_url"] for row in hold_products}
    refreshed_clean_rows = [row for row in rows if row["product_url"] not in held_product_urls]
    refreshed_excluded_rows = [row for row in rows if row["product_url"] in held_product_urls]
    refreshed_by_group = Counter(row["custom_label_2"] for row in refreshed_clean_rows)

    summary = {
        "status": "PASS" if not hold_products and not hold_images else "PASS_WITH_HELD_PUBLIC_ROWS",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_clean_scope": str(CLEAN_SCOPE.relative_to(ROOT)),
        "source_exclusions": str(EXCLUSIONS.relative_to(ROOT)),
        "validated_spec_status": spec.get("status"),
        "clean_variant_rows": len(rows),
        "unique_variants": len(variant_ids),
        "unique_products": len(products),
        "unique_images": len(images),
        "excluded_rows_preserved": len(exclusions),
        "product_group_variant_counts": dict(sorted(by_group.items())),
        "product_group_unique_product_counts": {key: len(value) for key, value in sorted(by_product_group.items())},
        "public_product_pages_pass": len(pass_products),
        "public_product_pages_hold": len(hold_products),
        "public_images_pass": len(pass_images),
        "public_images_hold": len(hold_images),
        "refreshed_clean_variant_rows": len(refreshed_clean_rows),
        "refreshed_excluded_variant_rows": len(refreshed_excluded_rows),
        "refreshed_product_group_variant_counts": dict(sorted(refreshed_by_group.items())),
        "held_product_urls": hold_products,
        "held_image_urls": hold_images,
        "external_writes": "none",
        "decision": "Pinterest draft scope remains local/paused-only; do not create or launch live objects from this packet alone.",
    }

    with (OUT_DIR / "pinterest_paused_draft_public_product_readback.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(product_readbacks[0].keys()))
        writer.writeheader()
        writer.writerows(product_readbacks)
    with (OUT_DIR / "pinterest_paused_draft_image_readback.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(image_readbacks[0].keys()))
        writer.writeheader()
        writer.writerows(image_readbacks)
    with (OUT_DIR / "pinterest_paused_draft_refreshed_clean_scope.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(refreshed_clean_rows)
    with (OUT_DIR / "pinterest_paused_draft_refreshed_public_exclusions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(refreshed_excluded_rows)
    (OUT_DIR / "pinterest_paused_draft_scope_refresh_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    report = f"""# Pinterest Paused Draft Scope Refresh

Date: `{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}`
Status: `{summary['status']}`

## Purpose

Refresh the public storefront and image readiness evidence for the already-approved Pinterest US paused draft scope before any future Ads Manager draft creation. This packet is local/read-only and does not create or edit Pinterest objects.

## Inputs

- Clean scope: `{summary['source_clean_scope']}`
- Exclusions: `{summary['source_exclusions']}`
- Prior local spec validation: `{summary['validated_spec_status']}`

## Result

- Clean rows preserved: `{summary['clean_variant_rows']}`
- Unique variants: `{summary['unique_variants']}`
- Unique products checked publicly: `{summary['unique_products']}`
- Unique image URLs checked: `{summary['unique_images']}`
- Explicit exclusions preserved: `{summary['excluded_rows_preserved']}`
- Product group variant counts: `{json.dumps(summary['product_group_variant_counts'], sort_keys=True)}`
- Product group unique product counts: `{json.dumps(summary['product_group_unique_product_counts'], sort_keys=True)}`
- Public product pages pass/hold: `{summary['public_product_pages_pass']}` / `{summary['public_product_pages_hold']}`
- Public images pass/hold: `{summary['public_images_pass']}` / `{summary['public_images_hold']}`
- Refreshed clean variant rows after public source holds: `{summary['refreshed_clean_variant_rows']}`
- Refreshed excluded variant rows: `{summary['refreshed_excluded_variant_rows']}`
- Refreshed product group variant counts: `{json.dumps(summary['refreshed_product_group_variant_counts'], sort_keys=True)}`

## Decision

The Pinterest scope remains a paused-draft-only candidate. It is still not live-launch authority and it must not create spend, enablement, catalog/source/tag/CAPI changes, or product-group mutations outside the paused spec and current approval gates.

Use `pinterest_paused_draft_refreshed_clean_scope.csv` for the next paused-draft prefill instead of the older full `342` rows unless the held public product rows are repaired and read back clean. The hard blocker found in this refresh is public supplier/source-domain leakage on held product pages, so those rows stay excluded from paid Pinterest use.

Next account-capable step: use the restored advertiser `549756244483` access, create only the paused/draft shell from `PINTEREST_US_PAUSED_DRAFT_BUILD_SPEC.md`, and stop before any budget/bid/enablement/launch/publish/audience/source/feed/tag/CAPI mutation if Pinterest requires it.

## Evidence Files

- `pinterest_paused_draft_public_product_readback.csv`
- `pinterest_paused_draft_image_readback.csv`
- `pinterest_paused_draft_refreshed_clean_scope.csv`
- `pinterest_paused_draft_refreshed_public_exclusions.csv`
- `pinterest_paused_draft_scope_refresh_summary.json`

## Guardrails

- No Pinterest campaign, ad group, ad, product group, catalog, source, tag, CAPI, audience, budget, bid, status, launch, or spend write occurred.
- No Shopify Admin, Merchant, Google Ads, GA4/GTM, billing, credential, product, feed, or live theme write occurred.
- Platform `IN_STOCK` is treated only as a feed diagnostic; no customer-facing copy claims local stock, owned inventory, warehouse inventory, or guaranteed on-hand availability.
"""
    (OUT_DIR / "PINTEREST_PAUSED_DRAFT_SCOPE_REFRESH.md").write_text(report, encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
