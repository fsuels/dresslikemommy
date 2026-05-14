#!/usr/bin/env python3
"""Public PDP preflight for US Shopping query/title candidates.

This is a public storefront readback only. It does not authenticate, mutate
Shopify, Merchant Center, Google Ads, or feed/product data.
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path


GROWTH_DIR = Path(__file__).resolve().parents[2]
SOURCE_CANDIDATES = (
    GROWTH_DIR
    / "02_AUDIT_PACKETS"
    / "2026-05-14-automation-us-shopping-query-title-diagnosis"
    / "us_shopping_query_title_candidates.csv"
)
OUT_DIR = Path(__file__).resolve().parent
OUT_ROWS = OUT_DIR / "us_shopping_public_pdp_fit_preflight_rows.csv"
OUT_READY_ROWS = OUT_DIR / "us_shopping_auth_export_public_clean_scope.csv"
OUT_SUMMARY = OUT_DIR / "us_shopping_public_pdp_fit_preflight_summary.json"
OUT_REPORT = OUT_DIR / "US_SHOPPING_PUBLIC_PDP_FIT_PREFLIGHT.md"

SUPPLIER_PATTERNS = (
    "detail.1688.com",
    "1688.com",
    "alibaba.com",
    "aliexpress.com",
)
STALE_OR_INVALID_PATTERNS = (
    "christmas",
    "warehouse",
    "retail store",
    "local pickup",
    "same day delivery",
)
QUERY_TOKEN_GROUPS = {
    "family pictures outfits": {
        "required_any": (("family", "matching"), ("photo", "photos", "picture", "pictures", "outfit", "outfits")),
        "nice_any": (("dress", "dresses", "set", "sets"),),
    },
    "family same outfit": {
        "required_any": (("family", "matching"), ("outfit", "outfits", "set", "sets", "match")),
        "nice_any": (("parents", "kids", "mother", "daughter", "father", "son"),),
    },
    "mommy and me wedding guest dresses": {
        "required_any": (("mommy", "mother", "mom"), ("daughter", "me"), ("dress", "dresses")),
        "nice_any": (("wedding", "guest", "party", "parties", "event", "events", "elegant", "chiffon", "sequin"),),
    },
}


def load_candidates() -> list[dict[str, str]]:
    with SOURCE_CANDIDATES.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch(url: str, accept: str) -> tuple[int | None, str, str | None]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "DLM public paid-growth preflight/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return int(resp.status), body, None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body, str(exc)
    except Exception as exc:  # noqa: BLE001 - packet records exact readback error.
        return None, "", str(exc)


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        return ""
    return html.unescape(re.sub(r"\s+", " ", match.group(1)).strip())


def text_bits(body: str) -> dict[str, str]:
    title = first_match(r"<title[^>]*>(.*?)</title>", body)
    h1 = first_match(r'<div[^>]+class=["\'][^"\']*product__title[^"\']*["\'][^>]*>\s*<h1[^>]*>(.*?)</h1>', body)
    if not h1:
        h1 = first_match(r"<h1[^>]*>(.*?)</h1>", body)
    og_title = first_match(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)', body)
    if h1.lower() in {"shipping policy", "shipping info"} and og_title:
        h1 = og_title
    description = first_match(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', body)
    custom_bits = " ".join(
        html.unescape(m)
        for m in re.findall(r'<meta[^>]+name=["\']custom-[^"\']+["\'][^>]+content=["\']([^"\']*)', body, flags=re.I)
    )
    return {
        "title": title,
        "h1": h1,
        "description": description,
        "custom_bits": custom_bits,
    }


def normalize_text(*parts: str) -> str:
    text = " ".join(parts).lower()
    return re.sub(r"[^a-z0-9]+", " ", text)


def group_match(text: str, group: tuple[str, ...]) -> bool:
    words = set(text.split())
    return any(token in words or token in text for token in group)


def score_query_fit(search_term: str, combined_text: str) -> tuple[str, list[str]]:
    config = QUERY_TOKEN_GROUPS.get(search_term, {"required_any": (), "nice_any": ()})
    missing = []
    for group in config["required_any"]:
        if not group_match(combined_text, group):
            missing.append("/".join(group))
    nice_hits = sum(1 for group in config["nice_any"] if group_match(combined_text, group))
    if missing:
        return "WEAK", missing
    if nice_hits < len(config["nice_any"]):
        return "OK_LIMITED", missing
    return "STRONG", missing


def main() -> int:
    candidates = load_candidates()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        grouped[row["candidate_handle"]].append(row)

    rows: list[dict[str, object]] = []
    handle_summary: dict[str, dict[str, object]] = {}

    for handle, candidate_rows in sorted(grouped.items()):
        url = f"https://www.dresslikemommy.com/products/{handle}?country=US"
        status_text, body_text, err_text = fetch(url, "text/html")
        time.sleep(0.15)
        status_any, body_any, err_any = fetch(url, "*/*")
        primary_body = body_text or body_any
        bits = text_bits(primary_body)
        combined = normalize_text(
            bits["title"],
            bits["h1"],
            bits["description"],
            bits["custom_bits"],
            handle,
        )
        supplier_hits = sorted({p for p in SUPPLIER_PATTERNS if p in primary_body.lower()})
        stale_hits = sorted({p for p in STALE_OR_INVALID_PATTERNS if p in primary_body.lower()})
        url_brand_hits = len(re.findall(r'data-(?:analytics-vendor|item-brand)=["\']https?://', primary_body, flags=re.I))
        has_shipping = "ships to" in combined or "standard shipping included" in combined
        has_usd = "pricecurrency" in primary_body.lower() and "usd" in primary_body.lower()
        has_add_signal = bool(re.search(r"add (?:this piece|matching|to cart|to bag)", primary_body, flags=re.I))
        has_available_signal = "instock" in primary_body.lower() or '"available":true' in primary_body.lower()
        page_clean = (
            status_text == 200
            and status_any == 200
            and not supplier_hits
            and not stale_hits
            and url_brand_hits == 0
        )

        fit_scores = []
        for candidate in candidate_rows:
            fit, missing = score_query_fit(candidate["search_term"], combined)
            decision = (
                "PUBLIC_LANDING_READY_FOR_AUTH_ITEM_EXPORT"
                if page_clean and fit in {"STRONG", "OK_LIMITED"}
                else "PUBLIC_LANDING_REVIEW_BEFORE_TITLE_PACKET"
                if page_clean
                else "HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE"
            )
            out = {
                "search_term": candidate["search_term"],
                "candidate_handle": handle,
                "rank": candidate["rank"],
                "paid_cohort_label": candidate["paid_cohort_label"],
                "landing_url": url,
                "status_text_html": status_text,
                "status_any": status_any,
                "source_clean": page_clean,
                "supplier_hit_count": len(supplier_hits),
                "url_brand_hit_count": url_brand_hits,
                "stale_or_invalid_hit_count": len(stale_hits),
                "has_shipping_signal": has_shipping,
                "has_usd_signal": has_usd,
                "has_add_signal": has_add_signal,
                "has_available_signal": has_available_signal,
                "public_title": bits["title"],
                "public_h1": bits["h1"],
                "public_description": bits["description"],
                "query_fit": fit,
                "missing_fit_groups": "; ".join(missing),
                "public_preflight_decision": decision,
                "fetch_error": err_text or err_any or "",
            }
            rows.append(out)
            fit_scores.append(fit)

        handle_summary[handle] = {
            "landing_url": url,
            "status_text_html": status_text,
            "status_any": status_any,
            "source_clean": page_clean,
            "supplier_hits": supplier_hits,
            "url_brand_hit_count": url_brand_hits,
            "stale_or_invalid_hits": stale_hits,
            "title": bits["title"],
            "h1": bits["h1"],
            "query_fit_counts": {k: fit_scores.count(k) for k in sorted(set(fit_scores))},
        }

    fieldnames = list(rows[0].keys())
    with OUT_ROWS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    ready_rows = [
        row
        for row in rows
        if row["public_preflight_decision"] == "PUBLIC_LANDING_READY_FOR_AUTH_ITEM_EXPORT"
    ]
    with OUT_READY_ROWS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ready_rows)

    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "candidate_rows": len(candidates),
        "unique_handles": len(grouped),
        "public_preflight_rows": len(rows),
        "status_all_200_handles": sum(
            1 for h in handle_summary.values() if h["status_text_html"] == 200 and h["status_any"] == 200
        ),
        "source_clean_handles": sum(1 for h in handle_summary.values() if h["source_clean"]),
        "supplier_hit_handles": [h for h, data in handle_summary.items() if data["supplier_hits"]],
        "url_brand_hit_handles": [h for h, data in handle_summary.items() if data["url_brand_hit_count"]],
        "stale_or_invalid_hit_handles": [h for h, data in handle_summary.items() if data["stale_or_invalid_hits"]],
        "row_decision_counts": {
            decision: sum(1 for row in rows if row["public_preflight_decision"] == decision)
            for decision in sorted({str(row["public_preflight_decision"]) for row in rows})
        },
        "query_fit_counts": {
            fit: sum(1 for row in rows if row["query_fit"] == fit)
            for fit in sorted({str(row["query_fit"]) for row in rows})
        },
        "handle_summary": handle_summary,
        "guardrails": [
            "public storefront GET only",
            "no Google Ads, Merchant, Shopify Admin, Pinterest, GA4/GTM, billing, product, feed, or theme write",
            "does not replace authenticated Shopping item-level export",
        ],
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ready_row_count = summary["row_decision_counts"].get("PUBLIC_LANDING_READY_FOR_AUTH_ITEM_EXPORT", 0)
    report = [
        "# US Shopping Public PDP Fit Preflight",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- Public storefront readback for the 24 rows in `us_shopping_query_title_candidates.csv`.",
        "- Unique PDP handles checked: `10`.",
        "- This reduces landing/source/title ambiguity before the required authenticated Google Ads / Merchant item-level export.",
        "- It is not a product/feed/title change and not a live Ads action.",
        "",
        "## Result",
        "",
        f"- PDP handles returning `200` for both public header variants: `{summary['status_all_200_handles']}/10`.",
        f"- Source-clean handles: `{summary['source_clean_handles']}/10`.",
        f"- Public candidate rows ready to carry into the authenticated item export: `{ready_row_count}/24`.",
        f"- Query-fit counts: `{summary['query_fit_counts']}`.",
        "",
        "## Decisions",
        "",
        "- Continue with the authenticated read-only Standard Shopping item-level export; this packet does not prove which products actually received impressions.",
        "- Do not add negatives, edit product groups, change bids/budgets/status, or edit Shopify/Merchant titles from this public preflight alone.",
        "- If the authenticated export shows one of these clean PDPs received impressions but the feed title lacks the matching buyer intent, prepare a narrow owner approval packet for title/feed repair.",
        "",
        "## Files",
        "",
        f"- Rows: `{OUT_ROWS.name}`",
        f"- Auth-export clean scope: `{OUT_READY_ROWS.name}`",
        f"- Summary: `{OUT_SUMMARY.name}`",
    ]
    if summary["supplier_hit_handles"] or summary["url_brand_hit_handles"] or summary["stale_or_invalid_hit_handles"]:
        report.extend(
            [
                "",
                "## Holds",
                "",
                f"- Supplier/source hit handles: `{summary['supplier_hit_handles']}`",
                f"- URL-like brand hit handles: `{summary['url_brand_hit_handles']}`",
                f"- Stale/invalid copy hit handles: `{summary['stale_or_invalid_hit_handles']}`",
            ]
        )
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
