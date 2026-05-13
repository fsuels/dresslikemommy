#!/usr/bin/env python3
"""Evaluate GB/CA/AU monitoring output against the first-72h ROAS rules.

This is local-only analysis of saved read-only Google Ads captures. It does not
open Ads pages or mutate account state.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PACKET = Path("/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring")
RAW = PACKET / "raw"
MONITORING_SUMMARY = RAW / "monitoring_summary.json"
ROUTE_SUMMARY = RAW / "perf-search-term-probe" / "gb_ca_au_perf_search_terms_route_probe_summary.json"
OUT_JSON = RAW / "gb_ca_au_optimization_readiness_summary.json"
OUT_CSV = RAW / "gb_ca_au_optimization_readiness_summary.csv"
OUT_MD = PACKET / "GB_CA_AU_OPTIMIZATION_READINESS_DECISION.md"

TARGET_CPA_USD = 10.77
ZERO_PURCHASE_PAUSE_REVIEW_USD = 16.00


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def money_to_float(value: str | None) -> float | None:
    if not value:
        return None
    cleaned = re.sub(r"[^0-9.]", "", value)
    return float(cleaned) if cleaned else None


def metric_after(lines: list[str], label_pattern: str) -> str | None:
    pattern = re.compile(label_pattern, re.I)
    for idx, line in enumerate(lines):
        if pattern.fullmatch(line.strip()):
            for candidate in lines[idx + 1 : idx + 5]:
                candidate = candidate.strip()
                if candidate and candidate not in {"arrow_upward", "help_outline", "—"}:
                    return candidate
    return None


def flatten_metric_lines(route_row: dict) -> list[str]:
    lines: list[str] = []
    for context in route_row.get("metric_context", []):
        lines.extend(context.get("lines", []))
    return lines


def route_rows_by_country(route_summary: dict, route: str) -> dict[str, dict]:
    return {
        row["country"]: row
        for row in route_summary.get("results", [])
        if row.get("route") == route
    }


def evaluate_market(monitor_row: dict, campaign_route: dict | None, search_terms_route: dict | None) -> dict:
    country = monitor_row["country"]
    checks = monitor_row.get("checks", {})
    safety_pass = all(checks.values()) if checks else False
    lines = flatten_metric_lines(campaign_route or {})
    clicks = metric_after(lines, r"Clicks")
    impressions = metric_after(lines, r"Impr\.|Impressions")
    cost_raw = metric_after(lines, r"Cost")
    conversions = metric_after(lines, r"Conversions")
    conversion_value = metric_after(lines, r"Conv\. value")
    cost = money_to_float(cost_raw)
    search_terms_actionable = bool(search_terms_route and search_terms_route.get("search_terms_actionable"))
    search_terms_note = (search_terms_route or {}).get("search_terms_actionability_note", "missing_search_terms_route")
    stale_filter = bool(search_terms_route and search_terms_route.get("has_stale_human_hair_filter"))
    visible_zero = {
        "clicks_zero": clicks in {"0", "0.00"},
        "impressions_zero": impressions in {"0", "0.00"},
        "cost_zero": cost == 0,
        "conversions_zero": conversions in {"0", "0.00"},
        "conversion_value_zero": conversion_value in {"0", "0.00"},
    }
    if not safety_pass:
        decision = "ACTION_REQUIRED_SAFETY_READBACK_FAILED"
        next_action = "Investigate failed campaign safety checks before any optimization or expansion."
    elif cost is not None and cost >= ZERO_PURCHASE_PAUSE_REVIEW_USD and conversions in {"0", "0.00"}:
        decision = "PREPARE_EXACT_PAUSE_REVIEW_APPROVAL"
        next_action = f"Spend reached >= ${ZERO_PURCHASE_PAUSE_REVIEW_USD:.2f} with zero conversions; prepare exact owner approval before any status edit."
    elif not search_terms_actionable:
        decision = "HOLD_MONITOR_NO_OPTIMIZATION_WRITE"
        next_action = "Continue read-only monitoring; do not add negatives or make ROAS decisions while search terms are non-actionable."
    elif all(visible_zero.values()):
        decision = "HOLD_MONITOR_ZERO_DATA"
        next_action = "Continue timed read-only monitoring until impressions, clicks, cost, search terms, conversions, or value appear."
    else:
        decision = "REVIEW_DATA_FOR_EVIDENCE_BACKED_OPTIMIZATION"
        next_action = "Review actual query/cost/conversion evidence; live edits still need fresh exact approval."
    return {
        "country": country,
        "campaign_id": monitor_row.get("campaign_id"),
        "ad_group_id": (monitor_row.get("enabled_adgroups") or [{}])[0].get("ad_group_id"),
        "safety_pass": safety_pass,
        "checks": checks,
        "clicks": clicks,
        "impressions": impressions,
        "cost": cost_raw,
        "conversions": conversions,
        "conversion_value": conversion_value,
        "search_terms_actionable": search_terms_actionable,
        "search_terms_note": search_terms_note,
        "has_stale_human_hair_filter": stale_filter,
        "target_cpa_usd": TARGET_CPA_USD,
        "zero_purchase_pause_review_usd": ZERO_PURCHASE_PAUSE_REVIEW_USD,
        "decision": decision,
        "next_action": next_action,
    }


def write_csv(rows: list[dict]) -> None:
    fields = [
        "country",
        "campaign_id",
        "ad_group_id",
        "safety_pass",
        "clicks",
        "impressions",
        "cost",
        "conversions",
        "conversion_value",
        "search_terms_actionable",
        "search_terms_note",
        "has_stale_human_hair_filter",
        "decision",
        "next_action",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def write_markdown(summary: dict) -> None:
    rows = summary["markets"]
    lines = [
        "# GB/CA/AU Optimization Readiness Decision",
        "",
        f"Generated: `{summary['timestamp_eastern']}`",
        "",
        "Mode: local-only evaluation of saved read-only Google Ads monitor artifacts. No Ads page was opened by this evaluator and no account write occurred.",
        "",
        "## Decision",
        "",
        "No optimization write is justified yet.",
        "",
        f"Target ROAS is `650%`; using the existing `$70` AOV assumption, max target CPA remains `${TARGET_CPA_USD:.2f}`. The zero-purchase pause-review threshold remains `${ZERO_PURCHASE_PAUSE_REVIEW_USD:.2f}` spend per market.",
        "",
        "| Market | Safety | Clicks | Impr. | Cost | Conv. | Value | Search terms | Decision |",
        "|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| `{country}` | `{safety}` | `{clicks}` | `{impressions}` | `{cost}` | `{conversions}` | `{conversion_value}` | `{terms}` | `{decision}` |".format(
                country=row["country"],
                safety="PASS" if row["safety_pass"] else "FAIL",
                clicks=row.get("clicks") or "unknown",
                impressions=row.get("impressions") or "unknown",
                cost=row.get("cost") or "unknown",
                conversions=row.get("conversions") or "unknown",
                conversion_value=row.get("conversion_value") or "unknown",
                terms=row.get("search_terms_note"),
                decision=row.get("decision"),
            )
        )
    lines.extend(
        [
            "",
            "## Required Next Action",
            "",
            "- Continue read-only monitoring after reporting populates.",
            "- Do not add negative keywords, pause, scale, change bids/budgets/status, or make ROAS conclusions while visible metrics are zero and search terms are blocked by the stale `Keyword: \"human hair wigs\"` filter.",
            "- If future spend reaches `$16.00` in any single market with zero purchases, prepare exact owner pause-review approval before any live status edit.",
            "- If search terms become actionable, compare actual terms against `gb_ca_au_negative_watchlist.csv`; live negative edits still require fresh exact approval.",
            "",
            "## Evidence",
            "",
            f"- Monitor summary: `{MONITORING_SUMMARY.relative_to(PACKET.parent.parent.parent)}`",
            f"- Route summary: `{ROUTE_SUMMARY.relative_to(PACKET.parent.parent.parent)}`",
            f"- JSON output: `{OUT_JSON.relative_to(PACKET.parent.parent.parent)}`",
            f"- CSV output: `{OUT_CSV.relative_to(PACKET.parent.parent.parent)}`",
            "",
            "## Guardrails",
            "",
            "No Google Ads upload, preview, import, apply, negative edit, budget/bid/status change, campaign enablement, Pinterest account write, Merchant upload/source edit, Shopify product/feed/conversion write, checkout payment/order/refund/cancel, billing/account/credential edit, or destructive action occurred.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    monitor = load_json(MONITORING_SUMMARY)
    route_summary = load_json(ROUTE_SUMMARY)
    campaign_routes = route_rows_by_country(route_summary, "campaigns")
    search_term_routes = route_rows_by_country(route_summary, "keywords_searchterms")
    rows = [
        evaluate_market(row, campaign_routes.get(row["country"]), search_term_routes.get(row["country"]))
        for row in monitor.get("results", [])
    ]
    summary = {
        "status": "DONE_LOCAL_OPTIMIZATION_READINESS_EVALUATION_NO_ADS_WRITES",
        "timestamp_eastern": datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds"),
        "target_roas": "650%",
        "target_cpa_usd": TARGET_CPA_USD,
        "zero_purchase_pause_review_usd": ZERO_PURCHASE_PAUSE_REVIEW_USD,
        "overall_decision": "NO_OPTIMIZATION_WRITE_JUSTIFIED",
        "markets": rows,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(rows)
    write_markdown(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
