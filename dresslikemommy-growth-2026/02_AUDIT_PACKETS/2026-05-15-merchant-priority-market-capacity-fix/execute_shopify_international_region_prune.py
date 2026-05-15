#!/usr/bin/env python3.13
"""Execute the bounded Shopify International region prune.

This script is intentionally narrow:
- reads only the local preview CSV for REMOVE_* International regions
- mutates only the Shopify Market with handle `international`
- deletes only region conditions by current Shopify region ID
- snapshots before/after sanitized market state

It does not touch Shopify products, Google Ads, Merchant Center feeds, campaigns,
budgets, bids, product groups, conversions, billing, or credentials.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
PREVIEW_CSV = BASE / "shopify_international_region_prune_preview.csv"
REPORT_MD = BASE / "SHOPIFY_INTERNATIONAL_REGION_PRUNE_EXECUTION_REPORT.md"
SUMMARY_JSON = BASE / "shopify_international_region_prune_execution_summary.json"
BEFORE_JSON = BASE / "shopify_markets_before_region_prune_sanitized.json"
AFTER_JSON = BASE / "shopify_markets_after_region_prune_sanitized.json"
BEFORE_CSV = BASE / "shopify_markets_before_region_prune_sanitized.csv"
AFTER_CSV = BASE / "shopify_markets_after_region_prune_sanitized.csv"

DEFAULT_ENV_PATH = Path.home() / ".config/dresslikemommy/shopify-admin.env"
REMOVE_BUCKETS = {
    "REMOVE_AFRICA",
    "REMOVE_ASIA_MIDDLE_EAST",
    "REMOVE_SOUTH_AMERICA",
}
REQUIRED_ACTIVE_MARKETS = {
    "us",
    "canada",
    "united-kingdom",
    "eu",
    "australia",
    "international",
}
PROTECTED_CODES_IN_INTERNATIONAL = {"CA", "AU"}


MARKETS_QUERY = """
query MarketsReadback {
  markets(first: 50) {
    nodes {
      id
      handle
      name
      status
      regions(first: 250) {
        nodes {
          ... on MarketRegionCountry {
            id
            code
            name
          }
        }
      }
    }
  }
}
"""


MARKET_UPDATE_MUTATION = """
mutation DeleteInternationalRegions($id: ID!, $input: MarketUpdateInput!) {
  marketUpdate(id: $id, input: $input) {
    market {
      id
      handle
      name
      status
      regions(first: 250) {
        nodes {
          ... on MarketRegionCountry {
            id
            code
            name
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def shopify_graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        raise RuntimeError("credentials not loaded in this shell")
    url = f"https://{domain}/admin/api/2026-04/graphql.json"
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body[:500]}") from exc


def preview_remove_codes() -> set[str]:
    with PREVIEW_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    codes = {
        row["region_code"].strip().upper()
        for row in rows
        if row.get("market_handle") == "international"
        and row.get("bucket") in REMOVE_BUCKETS
        and row.get("recommended_preview_action")
        == "remove_from_international_only_if_platform_preview_preserves_priority_markets"
    }
    if len(codes) != 52:
        raise RuntimeError(f"Expected exactly 52 first-pass remove codes, found {len(codes)}")
    blocked = sorted(codes & PROTECTED_CODES_IN_INTERNATIONAL)
    if blocked:
        raise RuntimeError(f"Protected duplicate International codes selected unexpectedly: {blocked}")
    return codes


def normalize_markets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if payload.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {payload['errors']}")
    markets = payload.get("data", {}).get("markets", {}).get("nodes", [])
    normalized: list[dict[str, Any]] = []
    for market in markets:
        regions = [
            {
                "id": region.get("id", ""),
                "code": region.get("code", ""),
                "name": region.get("name", ""),
            }
            for region in market.get("regions", {}).get("nodes", [])
            if region.get("code")
        ]
        normalized.append(
            {
                "id": market.get("id", ""),
                "handle": market.get("handle", ""),
                "name": market.get("name", ""),
                "status": market.get("status", ""),
                "region_count": len(regions),
                "regions": sorted(regions, key=lambda item: item["code"]),
            }
        )
    return sorted(normalized, key=lambda item: item["handle"])


def fetch_markets() -> list[dict[str, Any]]:
    return normalize_markets(shopify_graphql(MARKETS_QUERY))


def write_market_files(markets: list[dict[str, Any]], json_path: Path, csv_path: Path) -> None:
    json_path.write_text(json.dumps(markets, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows: list[dict[str, str]] = []
    for market in markets:
        for region in market["regions"]:
            rows.append(
                {
                    "market_handle": market["handle"],
                    "market_name": market["name"],
                    "market_status": market["status"],
                    "region_code": region["code"],
                    "region_name": region["name"],
                }
            )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["market_handle", "market_name", "market_status", "region_code", "region_name"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def market_by_handle(markets: list[dict[str, Any]], handle: str) -> dict[str, Any]:
    matches = [market for market in markets if market["handle"] == handle]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one market handle {handle!r}, found {len(matches)}")
    return matches[0]


def validate_before(markets: list[dict[str, Any]], remove_codes: set[str]) -> dict[str, Any]:
    active_handles = {market["handle"] for market in markets if market["status"] == "ACTIVE"}
    missing = sorted(REQUIRED_ACTIVE_MARKETS - active_handles)
    if missing:
        raise RuntimeError(f"Missing required active markets before prune: {missing}")

    international = market_by_handle(markets, "international")
    regions_by_code = {region["code"]: region for region in international["regions"]}
    missing_remove = sorted(remove_codes - set(regions_by_code))
    if missing_remove:
        raise RuntimeError(f"Remove codes absent from International before prune: {missing_remove}")
    protected_missing = sorted(PROTECTED_CODES_IN_INTERNATIONAL - set(regions_by_code))
    if protected_missing:
        raise RuntimeError(f"Protected duplicate codes absent before prune: {protected_missing}")

    return {
        "active_market_handles_before": sorted(active_handles),
        "international_region_count_before": international["region_count"],
        "region_ids_to_delete": [regions_by_code[code]["id"] for code in sorted(remove_codes)],
        "region_codes_to_delete": sorted(remove_codes),
        "protected_codes_present_before": sorted(PROTECTED_CODES_IN_INTERNATIONAL),
    }


def execute_delete(international_market_id: str, region_ids: list[str]) -> dict[str, Any]:
    variables = {
        "id": international_market_id,
        "input": {
            "conditions": {
                "conditionsToDelete": {
                    "regionsCondition": {
                        "regionIds": region_ids,
                    }
                }
            }
        },
    }
    response = shopify_graphql(MARKET_UPDATE_MUTATION, variables)
    if response.get("errors"):
        raise RuntimeError(f"Shopify GraphQL mutation errors: {response['errors']}")
    user_errors = response.get("data", {}).get("marketUpdate", {}).get("userErrors", [])
    if user_errors:
        raise RuntimeError(f"Shopify marketUpdate userErrors: {user_errors}")
    return response.get("data", {}).get("marketUpdate", {}).get("market", {})


def validate_after(
    before_markets: list[dict[str, Any]],
    after_markets: list[dict[str, Any]],
    remove_codes: set[str],
) -> dict[str, Any]:
    before_active = {market["handle"] for market in before_markets if market["status"] == "ACTIVE"}
    after_active = {market["handle"] for market in after_markets if market["status"] == "ACTIVE"}
    missing_after = sorted(REQUIRED_ACTIVE_MARKETS - after_active)
    if missing_after:
        raise RuntimeError(f"Missing required active markets after prune: {missing_after}")
    if before_active != after_active:
        raise RuntimeError(
            f"Active market handle set changed unexpectedly: before={sorted(before_active)} after={sorted(after_active)}"
        )

    before_international = market_by_handle(before_markets, "international")
    after_international = market_by_handle(after_markets, "international")
    before_codes = {region["code"] for region in before_international["regions"]}
    after_codes = {region["code"] for region in after_international["regions"]}
    remaining_removed = sorted(remove_codes & after_codes)
    if remaining_removed:
        raise RuntimeError(f"Selected remove codes still present after prune: {remaining_removed}")
    protected_missing = sorted(PROTECTED_CODES_IN_INTERNATIONAL - after_codes)
    if protected_missing:
        raise RuntimeError(f"Protected duplicate codes missing after prune: {protected_missing}")

    return {
        "active_market_handles_after": sorted(after_active),
        "international_region_count_before": before_international["region_count"],
        "international_region_count_after": after_international["region_count"],
        "removed_region_count": len(before_codes - after_codes),
        "removed_region_codes": sorted(before_codes - after_codes),
        "unexpected_removed_region_codes": sorted((before_codes - after_codes) - remove_codes),
        "remaining_selected_remove_codes": remaining_removed,
        "protected_codes_present_after": sorted(PROTECTED_CODES_IN_INTERNATIONAL),
        "passed": len(before_codes - after_codes) == len(remove_codes)
        and not remaining_removed
        and not sorted((before_codes - after_codes) - remove_codes),
    }


def write_report(summary: dict[str, Any]) -> None:
    status = "EXECUTED" if summary["execute"] else "DRY_RUN_ONLY"
    after = summary.get("after_validation") or {}
    lines = [
        "# Shopify International Region Prune Execution Report",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        f"Mode: `{status}`.",
        "",
        "Scope: bounded Shopify Markets publishing-scope cleanup. This removed only the approved first-pass non-priority `International` country regions from Shopify Markets. It did not delete products or change titles, prices, variants, inventory, vendors, product types, Merchant feeds, Google Ads, Pinterest, product groups, bids, budgets, statuses, conversions, billing, or credentials.",
        "",
        "## Result",
        "",
        f"- International region count before: `{summary['before_validation']['international_region_count_before']}`.",
        f"- Requested first-pass remove regions: `{len(summary['before_validation']['region_codes_to_delete'])}`.",
    ]
    if after:
        lines.extend(
            [
                f"- International region count after: `{after['international_region_count_after']}`.",
                f"- Removed region count: `{after['removed_region_count']}`.",
                f"- Remaining selected remove codes: `{len(after['remaining_selected_remove_codes'])}`.",
                f"- Unexpected removed codes: `{len(after['unexpected_removed_region_codes'])}`.",
                f"- Protected duplicate `CA` and `AU` still present inside International: `{', '.join(after['protected_codes_present_after'])}`.",
                f"- Required active markets still present: `{', '.join(after['active_market_handles_after'])}`.",
            ]
        )
    else:
        lines.append("- No mutation was executed.")
    lines.extend(
        [
            "",
            "## Removed Region Codes",
            "",
            "`" + ", ".join(summary["before_validation"]["region_codes_to_delete"]) + "`",
            "",
            "## Evidence Files",
            "",
            "- `shopify_markets_before_region_prune_sanitized.json`",
            "- `shopify_markets_before_region_prune_sanitized.csv`",
            "- `shopify_markets_after_region_prune_sanitized.json`",
            "- `shopify_markets_after_region_prune_sanitized.csv`",
            "- `shopify_international_region_prune_execution_summary.json`",
            "",
            "## Decision Boundary",
            "",
            "Before any Shopping build, re-export Merchant all-products/source eligibility and prove Canada English, Canada French, and GB English rows exist. If Merchant still shows zero rows after this Shopify Markets cleanup, treat that as a Google/YouTube channel publishing-sync blocker, not permission to build Shopping from stale or absent rows.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument("--execute", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_env(args.env_file)
    remove_codes = preview_remove_codes()
    before_markets = fetch_markets()
    write_market_files(before_markets, BEFORE_JSON, BEFORE_CSV)
    before_validation = validate_before(before_markets, remove_codes)

    after_validation = None
    mutation_market = None
    if args.execute:
        international = market_by_handle(before_markets, "international")
        mutation_market = execute_delete(international["id"], before_validation["region_ids_to_delete"])
        time.sleep(2)
        after_markets = fetch_markets()
        write_market_files(after_markets, AFTER_JSON, AFTER_CSV)
        after_validation = validate_after(before_markets, after_markets, remove_codes)
    else:
        after_markets = before_markets
        write_market_files(after_markets, AFTER_JSON, AFTER_CSV)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "execute": args.execute,
        "mode": "SHOPIFY_MARKETS_INTERNATIONAL_REGION_PRUNE",
        "preview_csv": str(PREVIEW_CSV.relative_to(Path.cwd())),
        "before_validation": {
            key: value for key, value in before_validation.items() if key != "region_ids_to_delete"
        },
        "after_validation": after_validation,
        "mutation_market_handle": mutation_market.get("handle") if isinstance(mutation_market, dict) else "",
        "bucket_counts": dict(Counter(code[:1] for code in sorted(remove_codes))),
        "guardrails_preserved": [
            "mutated only Shopify Market handle international",
            "deleted only exact current region IDs for the 52 REMOVE_* preview rows",
            "preserved active us, canada, united-kingdom, eu, australia, and international markets",
            "preserved duplicate CA and AU inside International for first pass",
            "no Shopify product data, Merchant feed, Google Ads, Pinterest, budget, bid, status, product group, conversion, billing, or credential changes",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
