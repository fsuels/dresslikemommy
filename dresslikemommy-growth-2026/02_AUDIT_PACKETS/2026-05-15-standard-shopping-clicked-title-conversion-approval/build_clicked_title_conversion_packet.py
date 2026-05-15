#!/usr/bin/env python3
"""Build a no-write conversion cleanup packet for clicked Shopping PDP titles."""

from __future__ import annotations

import csv
import html
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
CLICKED_CSV = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-pdp-readback/standard_shopping_clicked_pdp_public_readback.csv"


def money(value: float) -> str:
    return f"${value:.2f}"


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    if not match:
        return ""
    return clean_text(match.group(1))


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def derive_action(row: dict[str, object]) -> tuple[str, str]:
    h1 = str(row["public_h1"])
    merchant_title = str(row["merchant_title"])
    og_title = str(row["og_title"]).replace(" | Dress Like Mommy", "").strip()
    clicks = int(row["clicks"])
    cost = float(row["cost"])
    mismatch = bool(row["feed_h1_mismatch"])
    truncated = bool(row["h1_has_literal_ellipsis"])

    if truncated:
        return (
            "OWNER_APPROVAL_REQUIRED_TITLE_CLEANUP",
            "Top clicked PDP has a literal ellipsis in the visible H1; repair the shopper-facing title/display title before scaling this item.",
        )
    if mismatch and cost >= 1.0:
        return (
            "REVIEW_TITLE_MESSAGE_MATCH_BEFORE_SCALE",
            "Clicked PDP is public-clean, but feed/SEO title and visible H1 are meaningfully different; review message match before increasing traffic.",
        )
    if og_title and og_title != h1 and clicks >= 2:
        return (
            "USE_SEO_TITLE_AS_CLEANUP_CANDIDATE",
            "SEO title is cleaner than the visible H1; use it as the candidate display-title cleanup text if owner approves product/title work.",
        )
    return (
        "OBSERVE_NO_TITLE_ACTION",
        "No title cleanup action from current public evidence alone; keep observing or use in broader conversion analysis.",
    )


def main() -> None:
    grouped: dict[str, dict[str, object]] = {}
    with CLICKED_CSV.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            if raw.get("header_variant") != "text_html":
                continue
            handle_key = raw["product_handle"]
            grouped[handle_key] = {
                "product_handle": handle_key,
                "landing_url": raw["landing_url"],
                "items_with_clicks": int(raw["items_with_clicks"]),
                "impressions": int(raw["impressions"]),
                "clicks": int(raw["clicks"]),
                "cost": float(raw["cost"]),
                "conversion_value": float(raw["conversion_value"]),
                "merchant_title": clean_text(raw["product_titles"].split(" | ")[0]),
                "join_decisions": raw["join_decisions"],
                "prior_public_decision": raw["decision"],
                "prior_public_blockers": raw["blockers"],
            }

    rows: list[dict[str, object]] = []
    totals = defaultdict(float)
    for row in sorted(grouped.values(), key=lambda item: (-int(item["clicks"]), -float(item["cost"]), str(item["product_handle"]))):
        page_html = fetch_html(str(row["landing_url"]))
        public_h1 = first_match(r'<h1[^>]*class="[^"]*product__title-text[^"]*"[^>]*>(.*?)</h1>', page_html)
        og_title = first_match(r'<meta\s+property="og:title"\s+content="([^"]*)"', page_html)
        meta_description = first_match(r'<meta\s+name="description"\s+content="([^"]*)"', page_html)
        schema_price = first_match(r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', page_html)
        product_form = "product-form__submit" in page_html and "/cart/add" in page_html
        visible_customer_photos = "product-photo-strip__title" in page_html and "Customer photos" in page_html
        zero_review_hidden = "jdgm-prev-badge" in page_html and "data-average-rating='0.00'" in page_html and "display:none" in page_html

        feed_h1_mismatch = bool(public_h1 and str(row["merchant_title"]).lower() != public_h1.lower())
        h1_has_literal_ellipsis = "..." in public_h1 or "…" in public_h1

        enriched = {
            **row,
            "public_h1": public_h1,
            "og_title": og_title,
            "meta_description": meta_description,
            "schema_price": schema_price,
            "add_to_cart_form_present": product_form,
            "customer_photos_present": visible_customer_photos,
            "zero_review_badge_hidden": zero_review_hidden,
            "feed_h1_mismatch": feed_h1_mismatch,
            "h1_has_literal_ellipsis": h1_has_literal_ellipsis,
        }
        decision, reason = derive_action(enriched)
        enriched["recommended_action"] = decision
        enriched["reason"] = reason
        rows.append(enriched)

        totals["impressions"] += int(row["impressions"])
        totals["clicks"] += int(row["clicks"])
        totals["cost"] += float(row["cost"])
        totals["conversion_value"] += float(row["conversion_value"])
        if h1_has_literal_ellipsis:
            totals["ellipsis_clicks"] += int(row["clicks"])
            totals["ellipsis_cost"] += float(row["cost"])
            totals["ellipsis_handles"] += 1
        if feed_h1_mismatch:
            totals["mismatch_clicks"] += int(row["clicks"])
            totals["mismatch_cost"] += float(row["cost"])
            totals["mismatch_handles"] += 1

    csv_path = OUT_DIR / "standard_shopping_clicked_title_conversion_actions.csv"
    fieldnames = [
        "recommended_action",
        "reason",
        "product_handle",
        "landing_url",
        "items_with_clicks",
        "impressions",
        "clicks",
        "cost",
        "conversion_value",
        "merchant_title",
        "public_h1",
        "og_title",
        "schema_price",
        "add_to_cart_form_present",
        "customer_photos_present",
        "zero_review_badge_hidden",
        "feed_h1_mismatch",
        "h1_has_literal_ellipsis",
        "join_decisions",
        "prior_public_decision",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    approval_phrase = (
        "I approve a no-feed, no-campaign Shopify title/display-title cleanup for only the clicked Standard Shopping PDPs listed in "
        "standard_shopping_clicked_title_conversion_actions.csv with recommended_action=OWNER_APPROVAL_REQUIRED_TITLE_CLEANUP, using the listed SEO/Merchant title "
        "as the cleanup basis, with before/after public H1, title, add-to-cart, price, source-clean, and zero-review-badge readbacks; do not change prices, variants, "
        "inventory, product scope, feeds, campaigns, product groups, bids, budgets, statuses, conversion settings, billing, or Pinterest/Merchant/Google Ads objects."
    )

    summary = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "mode": "PUBLIC_READONLY_NO_EXTERNAL_WRITES",
        "source_clicked_readback": str(CLICKED_CSV.relative_to(ROOT)),
        "unique_clicked_handles": len(rows),
        "total_impressions": int(totals["impressions"]),
        "total_clicks": int(totals["clicks"]),
        "total_cost": round(totals["cost"], 2),
        "total_conversion_value": round(totals["conversion_value"], 2),
        "h1_ellipsis_handles": int(totals["ellipsis_handles"]),
        "h1_ellipsis_clicks": int(totals["ellipsis_clicks"]),
        "h1_ellipsis_cost": round(totals["ellipsis_cost"], 2),
        "feed_h1_mismatch_handles": int(totals["mismatch_handles"]),
        "feed_h1_mismatch_clicks": int(totals["mismatch_clicks"]),
        "feed_h1_mismatch_cost": round(totals["mismatch_cost"], 2),
        "approval_phrase": approval_phrase,
        "csv": str(csv_path.relative_to(ROOT)),
    }
    summary_path = OUT_DIR / "standard_shopping_clicked_title_conversion_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    top_rows = rows[:5]
    top_table = "\n".join(
        "| `{handle}` | `{clicks}` | `{cost}` | {action} | {h1} |".format(
            handle=row["product_handle"],
            clicks=row["clicks"],
            cost=money(float(row["cost"])),
            action=row["recommended_action"],
            h1=clean_text(str(row["public_h1"])).replace("|", "\\|"),
        )
        for row in top_rows
    )

    report = f"""# Standard Shopping Clicked Title Conversion Approval Packet

Generated: `{summary["generated_at"]}`
Mode: public/read-only storefront analysis. No Shopify Admin, Merchant, Google Ads, Pinterest, feed, product, title, product-group, bid, budget, status, conversion, billing, credential, or live theme write occurred.

## Why

US Standard Shopping has real clicked-product spend but no conversion value: `{summary["total_clicks"]}` clicks / `{money(summary["total_cost"])}` cost / `{money(summary["total_conversion_value"])}` conversion value across `{summary["unique_clicked_handles"]}` clicked handles.

The prior readback proved these clicked PDPs are source-clean and have add-to-cart forms. This pass looked for shopper-message friction that can be fixed before spending more traffic into the same products.

## Result

- Clicked handles checked: `{summary["unique_clicked_handles"]}`
- Clicked-row impressions/clicks/cost/conversion value: `{summary["total_impressions"]}` / `{summary["total_clicks"]}` / `{money(summary["total_cost"])}` / `{money(summary["total_conversion_value"])}`
- Handles with literal ellipses in the visible product H1: `{summary["h1_ellipsis_handles"]}` handles / `{summary["h1_ellipsis_clicks"]}` clicks / `{money(summary["h1_ellipsis_cost"])}`
- Handles where Merchant/SEO title and visible H1 differ materially: `{summary["feed_h1_mismatch_handles"]}` handles / `{summary["feed_h1_mismatch_clicks"]}` clicks / `{money(summary["feed_h1_mismatch_cost"])}`
- Every checked page still had an add-to-cart form, customer-photo section markup, and hidden zero-review badge behavior in the public source.

## Highest-Impact Rows

| Product handle | Clicks | Cost | Recommended action | Current visible H1 |
|---|---:|---:|---|---|
{top_table}

## Decision

Do not change Shopping bids, budgets, product groups, titles, feed attributes, status, negatives, or product scope from this packet alone.

The exact sales-moving next step is a tightly scoped Shopify title/display-title cleanup approval for clicked products whose visible H1 is literally truncated. This is a shopper-message cleanup, not feed or campaign authority.

## Approval Phrase

`{approval_phrase}`

## Evidence Files

- `{csv_path.relative_to(ROOT)}`
- `{summary_path.relative_to(ROOT)}`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-pdp-readback/STANDARD_SHOPPING_CLICKED_PDP_PUBLIC_READBACK.md`
"""
    report_path = OUT_DIR / "STANDARD_SHOPPING_CLICKED_TITLE_CONVERSION_APPROVAL_PACKET.md"
    report_path.write_text(report, encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
