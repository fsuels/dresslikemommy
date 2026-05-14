#!/usr/bin/env python3.13
from __future__ import annotations

import csv
import json
import ssl
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "2026-05-14-automation-us-shopping-public-pdp-fit-preflight"
SOURCE_ROWS = PREVIOUS / "us_shopping_public_pdp_fit_preflight_rows.csv"

SUPPLIER_PATTERNS = ("detail.1688.com", "1688.com", "alibaba.com", "aliexpress.com")
STALE_PATTERNS = ("christmas", "xmas", "holiday santa", "reindeer")

HEADERS = {
    "browser": {
        "User-Agent": "Mozilla/5.0 DLM paid-growth public readback",
        "Accept": "text/html,application/xhtml+xml",
    },
    "generic": {
        "User-Agent": "curl/8.0 DLM paid-growth public readback",
        "Accept": "*/*",
    },
}


def fetch(url: str, headers: dict[str, str]) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers)
    context = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=25, context=context) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.status, body


def classify(row: dict[str, str], observed: dict[str, object]) -> tuple[str, str, str]:
    supplier_hits = int(row["supplier_hit_count"])
    stale_hits = int(row["stale_or_invalid_hit_count"])
    query_fit = row["query_fit"]
    handle = row["candidate_handle"]

    if supplier_hits:
        return (
            "EXCLUDE_FROM_AUTH_EXPORT_UNTIL_SOURCE_CLEAN",
            "Public source still contains supplier/source domain hits.",
            "Owner-approved Shopify/product-data or theme-safe repair, then public source readback shows zero supplier hits before any paid export/use.",
        )

    if stale_hits:
        return (
            "EXCLUDE_FROM_AUTH_EXPORT_UNTIL_STALE_COPY_CLEAN",
            "Public source contains stale seasonal copy that mismatches current swim/family query intent.",
            "Owner-approved narrow SEO/social/card metadata repair, or keep handle excluded from paid Shopping/Search traffic.",
        )

    if query_fit == "WEAK":
        return (
            "AUTH_EXPORT_ALLOWED_ONLY_IF_ITEM_LEVEL_IMPRESSIONS_PROVE_RELEVANCE",
            "Public page is source-clean but weak for the observed query intent.",
            "Run authenticated item export first; only consider title/feed repair if this exact item received meaningful impressions for the query.",
        )

    return (
        "NO_REPAIR_NEEDED_FROM_PUBLIC_READBACK",
        f"No public source/stale issue found for {handle}.",
        "Carry only through authenticated export if item-level evidence warrants it.",
    )


def main() -> None:
    with SOURCE_ROWS.open(newline="") as f:
        rows = list(csv.DictReader(f))

    target_rows = [
        row
        for row in rows
        if row["public_preflight_decision"] != "PUBLIC_LANDING_READY_FOR_AUTH_ITEM_EXPORT"
    ]
    handles = sorted({row["candidate_handle"] for row in target_rows})

    fetched: dict[str, dict[str, object]] = {}
    for handle in handles:
        sample = next(row for row in target_rows if row["candidate_handle"] == handle)
        url = sample["landing_url"]
        variants = {}
        for name, headers in HEADERS.items():
            status, body = fetch(url, headers)
            lowered = body.lower()
            variants[name] = {
                "status": status,
                "supplier_hits": {p: lowered.count(p.lower()) for p in SUPPLIER_PATTERNS},
                "stale_hits": {p: lowered.count(p.lower()) for p in STALE_PATTERNS},
            }
        fetched[handle] = {"url": url, "variants": variants}

    out_rows = []
    handle_actions = {}
    for row in target_rows:
        observed = fetched[row["candidate_handle"]]
        action, reason, next_action = classify(row, observed)
        out = dict(row)
        out["repair_packet_action"] = action
        out["repair_reason"] = reason
        out["next_unblock_action"] = next_action
        out_rows.append(out)
        handle_actions[row["candidate_handle"]] = {
            "action": action,
            "reason": reason,
            "next_action": next_action,
            "landing_url": row["landing_url"],
            "observed": observed,
        }

    csv_path = ROOT / "us_shopping_held_pdp_repair_rows.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_rows": str(SOURCE_ROWS),
        "held_or_review_rows": len(out_rows),
        "unique_handles": len(handles),
        "action_counts": Counter(row["repair_packet_action"] for row in out_rows),
        "handle_actions": handle_actions,
        "guardrails": [
            "public storefront GET only",
            "no Google Ads, Merchant, Shopify Admin, Pinterest, GA4/GTM, billing, product, feed, theme, or campaign write",
            "does not replace authenticated Standard Shopping item-level export",
        ],
    }
    summary["action_counts"] = dict(summary["action_counts"])
    summary_path = ROOT / "us_shopping_held_pdp_repair_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    rows_by_action = defaultdict(list)
    for row in out_rows:
        rows_by_action[row["repair_packet_action"]].append(row)

    report = [
        "# US Shopping Held PDP Repair Packet",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        "## Scope",
        "",
        "- Started from the held/review rows in the US Shopping public PDP fit preflight.",
        f"- Rows checked: `{len(out_rows)}` across `{len(handles)}` unique handles.",
        "- Re-fetched each affected public PDP with browser-like and generic headers.",
        "- No external account, Shopify Admin, Merchant, feed, Ads, product, campaign, budget, bid, status, or theme write occurred.",
        "",
        "## Result",
        "",
    ]
    for action, count in sorted(summary["action_counts"].items()):
        report.append(f"- `{action}`: `{count}` rows")

    report.extend(
        [
            "",
            "## Row Actions",
            "",
        ]
    )
    for row in out_rows:
        report.extend(
            [
                f"### `{row['candidate_handle']}`",
                "",
                f"- Search term: `{row['search_term']}`",
                f"- Landing URL: `{row['landing_url']}`",
                f"- Public title: `{row['public_title']}`",
                f"- Public H1: `{row['public_h1']}`",
                f"- Preflight decision: `{row['public_preflight_decision']}`",
                f"- Repair packet action: `{row['repair_packet_action']}`",
                f"- Reason: {row['repair_reason']}",
                f"- Next unblock action: {row['next_unblock_action']}",
                "",
            ]
        )

    report.extend(
        [
            "## Approval Packet If Repair Is Desired",
            "",
            "Use this only after deciding to repair the excluded public PDPs instead of keeping them out of paid traffic:",
            "",
            "`APPROVE NARROW US SHOPPING HELD PDP PUBLIC-LANDING REPAIR ONLY: review and repair only the specific handles named in the 2026-05-14 US Shopping held PDP repair packet so public source has zero supplier/source-domain hits and no stale seasonal mismatch before paid export/use; no Google Ads, Merchant feed/source/product-scope/product-group, budget, bid, status, conversion-goal, Pinterest, billing, discount, price, inventory, or unrelated Shopify product changes; read back public source before and after.`",
            "",
            "## Files",
            "",
            "- Rows: `us_shopping_held_pdp_repair_rows.csv`",
            "- Summary: `us_shopping_held_pdp_repair_summary.json`",
        ]
    )
    (ROOT / "US_SHOPPING_HELD_PDP_REPAIR_PACKET.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
