#!/usr/bin/env python3
"""Qualified-shopper conversion rate for the owner scorecard.

Total-session conversion is diluted by traffic that never buys (mostly US desktop
direct sessions with zero completed checkouts). The headline store conversion
metric is therefore computed on the qualified-shopper segment:

    mobile sessions  OR  Google search-referred sessions (any device)

Total-session conversion stays as a diagnostic row only. The excluded remainder is
described as low-intent or unverified traffic; it is not a proven bot diagnosis.

The local Admin token lacks `read_reports`, so the ShopifyQL queries run through
the authenticated Shopify connector. Workflow:

    python3 ops/scripts/qualified_shopper_conversion.py queries --since 2026-08-25 --until 2026-09-23
    # run both queries in the Shopify connector; save {"total": <result>, "qualified": <result>}
    python3 ops/scripts/qualified_shopper_conversion.py report --input evidence.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

METRICS = (
    "sessions",
    "sessions_with_cart_additions",
    "sessions_that_reached_checkout",
    "sessions_that_completed_checkout",
)
QUALIFIED_WHERE = (
    "session_device_type = 'mobile' OR "
    "(referrer_source = 'search' AND referrer_name = 'google')"
)
SEGMENT_LABEL = "mobile OR Google search"
# Below this many qualified completions the rate is directional, not a baseline.
MIN_COMPLETIONS_FOR_BASELINE = 30


def build_queries(since: str, until: str) -> Dict[str, str]:
    show = ", ".join(METRICS)
    window = f"SINCE {since} UNTIL {until}"
    return {
        "total": f"FROM sessions SHOW {show} {window}",
        "qualified": f"FROM sessions SHOW {show} WHERE {QUALIFIED_WHERE} {window}",
    }


def read_single_row(result: Dict) -> Dict[str, int]:
    rows = result.get("rows") or []
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one ungrouped row, got {len(rows)}: {result.get('query', '')}")
    names = [column["name"] for column in result["columns"]]
    values = dict(zip(names, rows[0]))
    missing = [metric for metric in METRICS if metric not in values]
    if missing:
        raise ValueError(f"Missing metrics {missing} in: {result.get('query', '')}")
    return {metric: int(values[metric]) for metric in METRICS}


def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def funnel(counts: Dict[str, int]) -> Dict[str, float]:
    sessions = counts["sessions"]
    return {
        **counts,
        "cart_rate": rate(counts["sessions_with_cart_additions"], sessions),
        "checkout_rate": rate(counts["sessions_that_reached_checkout"], sessions),
        "conversion_rate": rate(counts["sessions_that_completed_checkout"], sessions),
    }


def compute_report(evidence: Dict) -> Dict:
    total = read_single_row(evidence["total"])
    qualified = read_single_row(evidence["qualified"])
    for metric in METRICS:
        if qualified[metric] > total[metric]:
            raise ValueError(f"Qualified {metric} exceeds total; queries likely used different windows")
    excluded = {metric: total[metric] - qualified[metric] for metric in METRICS}

    warnings: List[str] = []
    if excluded["sessions_that_completed_checkout"] > 0:
        warnings.append(
            "Excluded segment contains completed checkouts; the qualified definition is "
            "dropping real buyers and must be reviewed before use as the headline."
        )
    if qualified["sessions_that_completed_checkout"] < MIN_COMPLETIONS_FOR_BASELINE:
        warnings.append(
            f"Only {qualified['sessions_that_completed_checkout']} qualified completions "
            f"(<{MIN_COMPLETIONS_FOR_BASELINE}); treat the rate as directional."
        )

    return {
        "segment": SEGMENT_LABEL,
        "qualified_where": QUALIFIED_WHERE,
        "headline_conversion_rate": rate(
            qualified["sessions_that_completed_checkout"], qualified["sessions"]
        ),
        "qualified": funnel(qualified),
        "total_diagnostic": funnel(total),
        "excluded_low_intent_or_unverified": funnel(excluded),
        "excluded_session_share": rate(excluded["sessions"], total["sessions"]),
        "warnings": warnings,
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def format_markdown(report: Dict, window: str) -> str:
    q = report["qualified"]
    t = report["total_diagnostic"]
    x = report["excluded_low_intent_or_unverified"]
    lines = [
        f"| Segment ({window}) | Sessions | Carts | Checkouts | Purchases | Conversion |",
        "|---|---:|---:|---:|---:|---:|",
        f"| **Qualified shoppers — {report['segment']} (headline)** | {q['sessions']:,} | "
        f"{q['sessions_with_cart_additions']:,} | {q['sessions_that_reached_checkout']:,} | "
        f"{q['sessions_that_completed_checkout']:,} | **{pct(q['conversion_rate'])}** |",
        f"| Excluded low-intent/unverified ({pct(report['excluded_session_share'])} of sessions) | "
        f"{x['sessions']:,} | {x['sessions_with_cart_additions']:,} | "
        f"{x['sessions_that_reached_checkout']:,} | {x['sessions_that_completed_checkout']:,} | "
        f"{pct(x['conversion_rate'])} |",
        f"| All sessions (diagnostic only) | {t['sessions']:,} | {t['sessions_with_cart_additions']:,} | "
        f"{t['sessions_that_reached_checkout']:,} | {t['sessions_that_completed_checkout']:,} | "
        f"{pct(t['conversion_rate'])} |",
    ]
    lines.extend(f"\nWarning: {warning}" for warning in report["warnings"])
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    queries_parser = sub.add_parser("queries", help="Print the ShopifyQL queries to run in the Shopify connector")
    queries_parser.add_argument("--since", required=True)
    queries_parser.add_argument("--until", required=True)
    report_parser = sub.add_parser("report", help="Compute the scorecard from saved connector results")
    report_parser.add_argument("--input", required=True, type=Path)
    report_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    if args.command == "queries":
        print(json.dumps(build_queries(args.since, args.until), indent=2))
        return 0

    evidence = json.loads(args.input.read_text(encoding="utf-8"))
    report = compute_report(evidence)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(format_markdown(report, evidence.get("window", "window unstated")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
