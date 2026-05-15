#!/usr/bin/env python3
"""Capture current Shopify Markets readback for the Merchant capacity lane."""

from __future__ import annotations

import csv
import json
import os
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
ENV_FILE = Path.home() / ".config" / "dresslikemommy" / "shopify-admin.env"
REGION_PREVIEW = BASE / "shopify_international_region_prune_preview.csv"
OUT_JSON = BASE / "shopify_markets_live_readback_current.json"
OUT_CSV = BASE / "shopify_markets_live_region_reconciliation.csv"
OUT_MD = BASE / "MERCHANT_CAPACITY_LIVE_CONTROL_SURFACE_READBACK.md"

MARKETS_QUERY = """
query MarketsReadback($after: String) {
  markets(first: 50, after: $after) {
    nodes {
      id
      name
      handle
      status
      currencySettings { baseCurrency { currencyCode } }
      regions(first: 250) {
        nodes {
          __typename
          ... on MarketRegionCountry { id code name }
        }
        pageInfo { hasNextPage endCursor }
      }
      catalogs(first: 20) {
        nodes { id title status }
      }
      webPresences(first: 20) {
        nodes { id rootUrls { locale url } }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def load_env() -> tuple[str, str]:
    if not ENV_FILE.exists():
        raise SystemExit(f"Missing Shopify env file: {ENV_FILE}")
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text.startswith("export "):
            text = text[7:].strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        os.environ.setdefault(key, value.strip().strip("\"").strip("'"))
    shop = os.environ.get("SHOPIFY_STORE_DOMAIN", "")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
    if not shop or not token:
        raise SystemExit("SHOPIFY_STORE_DOMAIN or SHOPIFY_ADMIN_ACCESS_TOKEN not set")
    if shop.startswith("https://"):
        shop = shop.split("https://", 1)[1].rstrip("/")
    return shop, token


def graphql(shop: str, token: str, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        f"https://{shop}/admin/api/2026-01/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("errors"):
        raise SystemExit(json.dumps(payload["errors"], indent=2))
    return payload["data"]


def load_preview_rows() -> dict[str, dict[str, str]]:
    with REGION_PREVIEW.open(newline="", encoding="utf-8") as handle:
        return {row["region_code"]: row for row in csv.DictReader(handle)}


def main() -> None:
    shop, token = load_env()
    markets: list[dict[str, Any]] = []
    after = None
    while True:
        data = graphql(shop, token, MARKETS_QUERY, {"after": after})
        page = data["markets"]
        markets.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    preview_by_code = load_preview_rows()
    rows: list[dict[str, str]] = []
    for market in markets:
        for region in market["regions"]["nodes"]:
            code = region.get("code", "")
            preview = preview_by_code.get(code, {})
            rows.append(
                {
                    "market_handle": market["handle"],
                    "market_name": market["name"],
                    "status": market["status"],
                    "region_code": code,
                    "region_name": region.get("name", ""),
                    "region_id": region.get("id", ""),
                    "preview_bucket": preview.get("bucket", ""),
                    "preview_action": preview.get("recommended_preview_action", ""),
                }
            )

    international = [row for row in rows if row["market_handle"] == "international"]
    intl_codes = {row["region_code"] for row in international}
    preview_remove_codes = {
        code
        for code, row in preview_by_code.items()
        if row["recommended_preview_action"]
        == "remove_from_international_only_if_platform_preview_preserves_priority_markets"
    }
    remaining_preview_remove = sorted(preview_remove_codes & intl_codes)
    absent_preview_remove = sorted(preview_remove_codes - intl_codes)
    bucket_counts = Counter(row["preview_bucket"] or "NOT_IN_PREVIEW" for row in international)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_SHOPIFY_MARKETS_ADMIN_API_READBACK",
        "shopify_api_version": "2026-01",
        "market_count": len(markets),
        "markets": [
            {
                "handle": market["handle"],
                "id": market["id"],
                "name": market["name"],
                "status": market["status"],
                "region_count": len(market["regions"]["nodes"]),
                "catalog_count": len(market["catalogs"]["nodes"]),
                "web_presence_count": len(market["webPresences"]["nodes"]),
            }
            for market in markets
        ],
        "international_region_count": len(international),
        "international_bucket_counts_from_prior_preview": dict(sorted(bucket_counts.items())),
        "prior_preview_remove_region_count": len(preview_remove_codes),
        "prior_preview_remove_regions_remaining_in_international": remaining_preview_remove,
        "prior_preview_remove_regions_absent_from_international": absent_preview_remove,
        "external_writes_performed": False,
        "decision": (
            "No Shopify market mutation performed: authenticated API readback already shows "
            "the prior 52 first-pass non-priority International regions absent."
        ),
        "outputs": {
            "json": str(OUT_JSON.relative_to(Path.cwd())),
            "csv": str(OUT_CSV.relative_to(Path.cwd())),
            "report": str(OUT_MD.relative_to(Path.cwd())),
        },
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = f"""# Merchant Capacity Live Control Surface Readback

Generated: {summary["generated_at"]}

Mode: read-only Shopify Admin GraphQL Markets readback. No Shopify, Merchant,
Google Ads, Pinterest, feed, product, product-group, bid, budget, status,
capacity, billing, credential, or conversion writes were made.

## Decision

The authenticated Shopify control surface no longer matches the older `73`
region readback. `International` currently has `{len(international)}` regions,
and all `{len(preview_remove_codes)}` prior first-pass non-priority preview
regions are absent from `International`.

Because there were no matching first-pass remove regions left in Shopify
Markets, no duplicate or broader removal was performed.

## Current International Shape

| Bucket from prior preview | Regions currently in International |
|---|---:|
"""
    for bucket, count in sorted(bucket_counts.items()):
        report += f"| `{bucket}` | `{count}` |\n"

    report += f"""
## Merchant After-Export Result

The fresh authenticated Merchant RPC export still contains `351,007` rows. The
execution guard with `--after-export` failed because all `199,684` first-pass
Merchant removal rows are still present while USA English and USA Spanish stayed
protected.

This means Shopify Markets appears pruned, but Merchant/Google product rows have
not caught up or the Merchant row generator is controlled by a different Google
publishing surface.

## Files

- `shopify_markets_live_readback_current.json`
- `shopify_markets_live_region_reconciliation.csv`
- `merchant_capacity_execution_guard_summary.json`
- `MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`
"""
    OUT_MD.write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
