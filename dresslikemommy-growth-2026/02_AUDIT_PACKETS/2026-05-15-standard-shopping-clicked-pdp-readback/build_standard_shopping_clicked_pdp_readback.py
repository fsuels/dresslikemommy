#!/usr/bin/env python3
"""Public-readback clicked Standard Shopping PDPs from the read-only export."""

from __future__ import annotations

import csv
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
EXPORT = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-shopping-readonly-export-queue/standard_shopping_products_normalized_for_join.csv"
JOINED = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/us_shopping_auth_export_joined_decisions.csv"

SUPPLIER_PATTERNS = (
    "1688" + ".com",
    "detail" + "." + "1688" + ".com",
    "alibaba.com",
    "aliexpress.com",
)
TRUST_PATTERNS = ("warehouse", "retail store", "in stock at", "local pickup", "same day delivery")
SEASONAL_PATTERNS = ("christmas", "santa", "xmas", "reindeer")


def fetch(url: str, accept: str) -> tuple[int, str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 DLM paid-growth public readback",
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=20) as res:
            final_url = res.geturl()
            raw = res.read()
            encoding = res.headers.get_content_charset() or "utf-8"
            return res.status, final_url, raw.decode(encoding, errors="replace")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, url, body
    except URLError as exc:
        return 0, url, str(exc)


def text_between(pattern: str, html: str) -> str:
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        return ""
    return re.sub(r"\s+", " ", unescape(match.group(1))).strip()


def count_hits(html: str, patterns: tuple[str, ...]) -> int:
    lower = html.lower()
    return sum(lower.count(pattern) for pattern in patterns)


def load_join_decisions() -> dict[str, str]:
    if not JOINED.exists():
        return {}
    decisions: dict[str, str] = {}
    with JOINED.open(newline="") as handle:
        for row in csv.DictReader(handle):
            decisions[row["item_id"].lower()] = row["decision"]
    return decisions


def read_clicked_items() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    decisions = load_join_decisions()
    with EXPORT.open(newline="") as handle:
        for row in csv.DictReader(handle):
            clicks = float(row.get("clicks") or 0)
            if clicks <= 0:
                continue
            row = dict(row)
            row["join_decision"] = decisions.get((row.get("item_id") or "").lower(), "UNJOINED")
            rows.append(row)
    rows.sort(key=lambda r: (float(r.get("clicks") or 0), float(r.get("cost") or 0)), reverse=True)
    return rows


def main() -> int:
    clicked = read_clicked_items()
    by_handle: dict[str, dict[str, object]] = {}
    for row in clicked:
        handle = row.get("candidate_handle") or ""
        if not handle:
            continue
        entry = by_handle.setdefault(
            handle,
            {
                "product_handle": handle,
                "landing_url": row.get("landing_url") or "",
                "items": 0,
                "clicks": 0.0,
                "impressions": 0.0,
                "cost": 0.0,
                "conversion_value": 0.0,
                "titles": set(),
                "join_decisions": set(),
                "statuses": set(),
                "issues": set(),
            },
        )
        entry["items"] = int(entry["items"]) + 1
        entry["clicks"] = float(entry["clicks"]) + float(row.get("clicks") or 0)
        entry["impressions"] = float(entry["impressions"]) + float(row.get("impressions") or 0)
        entry["cost"] = float(entry["cost"]) + float(row.get("cost") or 0)
        entry["conversion_value"] = float(entry["conversion_value"]) + float(row.get("conversion_value") or 0)
        entry["titles"].add(row.get("product_title") or "")
        entry["join_decisions"].add(row.get("join_decision") or "")
        entry["statuses"].add(row.get("status") or "")
        if row.get("issues"):
            entry["issues"].add(row["issues"].replace("\n", " / "))

    readback_rows: list[dict[str, object]] = []
    header_variants = [("text_html", "text/html"), ("star", "*/*")]
    for entry in sorted(by_handle.values(), key=lambda e: (float(e["clicks"]), float(e["cost"])), reverse=True):
        url = str(entry["landing_url"])
        combined = {
            "product_handle": entry["product_handle"],
            "landing_url": url,
            "items_with_clicks": entry["items"],
            "impressions": int(entry["impressions"]),
            "clicks": int(entry["clicks"]),
            "cost": round(float(entry["cost"]), 2),
            "conversion_value": round(float(entry["conversion_value"]), 2),
            "product_titles": " | ".join(sorted(t for t in entry["titles"] if t)),
            "join_decisions": " | ".join(sorted(d for d in entry["join_decisions"] if d)),
            "statuses": " | ".join(sorted(s for s in entry["statuses"] if s)),
            "issues": " | ".join(sorted(i for i in entry["issues"] if i)),
        }
        for label, accept in header_variants:
            status, final_url, html = fetch(url, accept)
            h1 = text_between(r"<h1[^>]*>(.*?)</h1>", html)
            title = text_between(r"<title[^>]*>(.*?)</title>", html)
            supplier_hits = count_hits(html, SUPPLIER_PATTERNS)
            trust_hits = count_hits(html, TRUST_PATTERNS)
            seasonal_hits = count_hits(html, SEASONAL_PATTERNS)
            raw_source_url_hits = len(re.findall(r"https?://[^\"'<>\s]*(?:1688|alibaba|aliexpress)[^\"'<>\s]*", html, flags=re.I))
            html_lower = html.lower()
            variant_picker_present = "product-form" in html_lower or "name=\"id\"" in html_lower
            add_to_cart_present = "add to cart" in html_lower or "add to bag" in html_lower
            price_present = "$" in html or "price" in html_lower
            decision = "PUBLIC_CLICKED_PDP_PASS"
            blockers = []
            if status != 200:
                blockers.append("non_200")
            if supplier_hits or raw_source_url_hits:
                blockers.append("supplier_source_hit")
            if trust_hits:
                blockers.append("trust_copy_review")
            if seasonal_hits and "christmas" in str(entry["product_handle"]).lower() and "swim" in str(entry["product_titles"]).lower():
                blockers.append("seasonal_title_mismatch")
            if not variant_picker_present:
                blockers.append("variant_picker_not_detected")
            if not add_to_cart_present:
                blockers.append("add_to_cart_not_detected")
            if blockers:
                decision = "PUBLIC_CLICKED_PDP_REVIEW"
            readback_rows.append(
                {
                    **combined,
                    "header_variant": label,
                    "status": status,
                    "final_url": final_url,
                    "h1": h1,
                    "page_title": title,
                    "supplier_hits": supplier_hits,
                    "raw_source_url_hits": raw_source_url_hits,
                    "trust_hits": trust_hits,
                    "seasonal_hits": seasonal_hits,
                    "variant_picker_present": variant_picker_present,
                    "add_to_cart_present": add_to_cart_present,
                    "price_present": price_present,
                    "decision": decision,
                    "blockers": " | ".join(blockers),
                }
            )
            time.sleep(0.15)

    csv_path = OUT_DIR / "standard_shopping_clicked_pdp_public_readback.csv"
    fieldnames = list(readback_rows[0].keys()) if readback_rows else []
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(readback_rows)

    total_clicks = sum(float(r["clicks"]) for r in by_handle.values())
    total_cost = sum(float(r["cost"]) for r in by_handle.values())
    handles = len(by_handle)
    review_handles = sorted({str(r["product_handle"]) for r in readback_rows if r["decision"] != "PUBLIC_CLICKED_PDP_PASS"})
    source_blocked = sorted({str(r["product_handle"]) for r in readback_rows if r["supplier_hits"] or r["raw_source_url_hits"]})
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "PUBLIC_READBACK_NO_EXTERNAL_WRITES",
        "source_export": str(EXPORT.relative_to(ROOT)),
        "clicked_export_rows": len(clicked),
        "unique_clicked_handles": handles,
        "public_fetches": len(readback_rows),
        "total_clicked_impressions": int(sum(float(r["impressions"]) for r in by_handle.values())),
        "total_clicked_clicks": int(total_clicks),
        "total_clicked_cost": round(total_cost, 2),
        "total_clicked_conversion_value": round(sum(float(r["conversion_value"]) for r in by_handle.values()), 2),
        "pass_fetches": sum(1 for r in readback_rows if r["decision"] == "PUBLIC_CLICKED_PDP_PASS"),
        "review_fetches": sum(1 for r in readback_rows if r["decision"] != "PUBLIC_CLICKED_PDP_PASS"),
        "review_handles": review_handles,
        "source_blocked_handles": source_blocked,
        "csv": str(csv_path.relative_to(ROOT)),
    }
    (OUT_DIR / "standard_shopping_clicked_pdp_public_readback_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    report = [
        "# Standard Shopping Clicked PDP Public Readback",
        "",
        f"Generated: `{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}`",
        "Mode: public/storefront readback only. No Google Ads, Merchant, Shopify Admin, feed, title, product-group, bid, budget, status, conversion, Pinterest, GA4/GTM, billing, credential, or live theme write occurred.",
        "",
        "## Result",
        "",
        f"- Clicked export rows checked: `{len(clicked)}`",
        f"- Unique clicked product handles: `{handles}`",
        f"- Public fetches: `{len(readback_rows)}`",
        f"- Clicked-row impressions/clicks/cost/conversion value: `{summary['total_clicked_impressions']}` / `{summary['total_clicked_clicks']}` / `${summary['total_clicked_cost']:.2f}` / `${summary['total_clicked_conversion_value']:.2f}`",
        f"- Pass fetches: `{summary['pass_fetches']}`",
        f"- Review fetches: `{summary['review_fetches']}`",
        f"- Source-blocked handles: `{len(source_blocked)}`",
        "",
        "## Decision",
        "",
        "The clicked Standard Shopping export proves the campaign has produced product-level learning, but not purchases. The public readback should be used to separate clean clicked PDPs from landing blockers before any title/feed/product-group decision.",
        "",
        "Do not edit titles, feed attributes, product groups, bids, budgets, statuses, negatives, or product scope from this packet alone. Use it to prioritize the next narrow read-only or approval-gated action.",
        "",
        "## Next Action",
        "",
        "- Keep clean clicked PDPs eligible for Shopping observation and product-fit analysis.",
        "- For source-blocked or stale/trust-review handles, keep them out of new paid expansions until the exact product/vendor or theme repair packet is approved and public readback passes.",
        "- Continue the multilingual Shopping queue with current Merchant `US/es` source `10627981690` and CA/GB/AU English eligibility readbacks.",
        "",
        "## Evidence Files",
        "",
        f"- `{csv_path.relative_to(ROOT)}`",
        f"- `{(OUT_DIR / 'standard_shopping_clicked_pdp_public_readback_summary.json').relative_to(ROOT)}`",
    ]
    (OUT_DIR / "STANDARD_SHOPPING_CLICKED_PDP_PUBLIC_READBACK.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
