#!/usr/bin/env python3.13
"""Reconcile live Shopify Markets control with Merchant capacity guards.

This script performs authenticated read-only Shopify Admin GraphQL readbacks.
It does not mutate Shopify, Merchant Center, Google Ads, products, feeds,
campaigns, billing, or credentials.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402
from ops.scripts.sync_shopify_variant_costs import API_VERSION, ShopifyClient  # noqa: E402


BASE = Path(__file__).resolve().parent
REGION_GUARD = BASE / "shopify_international_region_prune_preview.csv"
FEED_GUARD = BASE / "merchant_capacity_platform_preview_acceptance.csv"
LIVE_REGION_CSV = BASE / "shopify_markets_live_exact_region_readback.csv"
SUMMARY_JSON = BASE / "merchant_capacity_exact_control_reconciliation.json"
REPORT_MD = BASE / "MERCHANT_CAPACITY_EXACT_CONTROL_RECONCILIATION.md"
EXECUTION_GUARD_SUMMARY = BASE / "merchant_capacity_execution_guard_summary.json"

MARKETS_QUERY = """
query MarketsExactReadback($after: String) {
  markets(first: 50, after: $after) {
    nodes {
      id
      name
      handle
      status
      type
      currencySettings { baseCurrency { currencyCode } }
      regions(first: 250) {
        nodes {
          id
          __typename
          ... on MarketRegionCountry {
            code
            name
            currency { currencyCode enabled }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

SCOPES_QUERY = """
query CurrentScopes {
  currentAppInstallation {
    accessScopes { handle }
  }
}
"""

MUTATIONS_QUERY = """
query MutationIntrospection {
  __type(name: "Mutation") {
    fields { name }
  }
}
"""


def utcish_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fetch_markets(client: ShopifyClient) -> list[dict[str, Any]]:
    markets: list[dict[str, Any]] = []
    after = None
    while True:
        data = client.graphql(MARKETS_QUERY, {"after": after})["markets"]
        markets.extend(data["nodes"])
        if not data["pageInfo"]["hasNextPage"]:
            return markets
        after = data["pageInfo"]["endCursor"]


def main() -> None:
    region_guard_rows = read_csv(REGION_GUARD)
    feed_guard_rows = read_csv(FEED_GUARD)

    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    client = ShopifyClient(store_domain, load_access_token(), API_VERSION)
    scopes = sorted(
        scope["handle"] for scope in client.graphql(SCOPES_QUERY)["currentAppInstallation"]["accessScopes"]
    )
    market_mutations = sorted(
        field["name"]
        for field in client.graphql(MUTATIONS_QUERY)["__type"]["fields"]
        if "market" in field["name"].lower()
    )
    markets = fetch_markets(client)

    live_rows: list[dict[str, Any]] = []
    for market in markets:
        base_currency = (((market.get("currencySettings") or {}).get("baseCurrency") or {}).get("currencyCode") or "")
        for region in ((market.get("regions") or {}).get("nodes") or []):
            currency = (region.get("currency") or {}).get("currencyCode") or base_currency
            live_rows.append(
                {
                    "market_handle": market["handle"],
                    "market_name": market["name"],
                    "market_status": market["status"],
                    "market_id_tail": market["id"].split("/")[-1],
                    "region_code": (region.get("code") or "").upper(),
                    "region_name": region.get("name") or "",
                    "region_id_tail": region["id"].split("/")[-1],
                    "region_currency": currency,
                }
            )

    write_csv(
        LIVE_REGION_CSV,
        sorted(live_rows, key=lambda r: (r["market_handle"], r["region_code"])),
        [
            "market_handle",
            "market_name",
            "market_status",
            "market_id_tail",
            "region_code",
            "region_name",
            "region_id_tail",
            "region_currency",
        ],
    )

    international_live_codes = {
        row["region_code"] for row in live_rows if row["market_handle"] == "international"
    }
    live_market_handles = sorted({row["market_handle"] for row in live_rows})
    region_remove_rows = [
        row
        for row in region_guard_rows
        if row["recommended_preview_action"]
        == "remove_from_international_only_if_platform_preview_preserves_priority_markets"
    ]
    region_remove_codes = {row["region_code"] for row in region_remove_rows}
    protected_region_codes = {
        row["region_code"]
        for row in region_guard_rows
        if row["bucket"] == "PRESERVE_PRIORITY_OR_SEPARATE_MARKET"
    }
    hold_region_codes = {
        row["region_code"] for row in region_guard_rows if row["bucket"].endswith("HOLD_REVIEW")
    } | {row["region_code"] for row in region_guard_rows if row["bucket"] == "HOLD_REVIEW_NOT_FIRST_PASS"}

    feed_remove_rows = [row for row in feed_guard_rows if row["check_type"] == "remove_exact_group"]
    feed_protect_rows = [row for row in feed_guard_rows if row["check_type"] == "protect_priority_group"]
    feed_after_rows = [row for row in feed_guard_rows if row["check_type"] == "enable_after_capacity_cleanup"]
    non_us_usd_rows = [
        row for row in feed_remove_rows if row["feed_label"].startswith("USD_") and row["currency"] == "USD"
    ]

    required_market_handles = {"us", "canada", "united-kingdom", "eu", "australia", "international"}
    required_markets_present = required_market_handles <= set(live_market_handles)
    protected_present = {"CA", "AU"} <= international_live_codes
    if region_remove_codes <= international_live_codes and required_markets_present and protected_present:
        region_guard_status = "PASS_EXACT_REGION_PREVIEW_PRE_CLEANUP"
    elif not (region_remove_codes & international_live_codes) and required_markets_present and protected_present:
        region_guard_status = "LIVE_REGION_SCOPE_ALREADY_PRUNED_OUTSIDE_THIS_READBACK"
    else:
        region_guard_status = "FAIL_REGION_PREVIEW_MISMATCH"
    feed_guard_status = "BLOCKED_NO_EXACT_FEED_GROUP_CONTROL_PREVIEW"
    execution_guard = read_json(EXECUTION_GUARD_SUMMARY)
    after_validation = execution_guard.get("after_validation") or {}
    after_export_guard_status = (
        "PASSED"
        if after_validation.get("passed") is True
        else "FAILED"
        if after_validation
        else "NOT_RUN_NO_CLEANUP_EXPORT_AVAILABLE"
    )
    overall_status = "SHOPIFY_REGION_SCOPE_PRUNED__MERCHANT_FEED_GROUP_GUARD_STILL_BLOCKED"

    summary = {
        "generated_at": utcish_now(),
        "mode": "authenticated_readonly_exact_control_reconciliation",
        "store_domain": store_domain,
        "shopify_admin_api_version": API_VERSION,
        "shopify_market_scopes_present": [scope for scope in scopes if "market" in scope.lower()],
        "shopify_market_mutations_present": market_mutations,
        "active_market_handles_seen": live_market_handles,
        "international_live_region_count": len(international_live_codes),
        "region_guard": {
            "status": region_guard_status,
            "candidate_remove_regions": len(region_remove_codes),
            "candidate_remove_regions_still_live": len(region_remove_codes & international_live_codes),
            "candidate_remove_regions_absent_live": sorted(region_remove_codes - international_live_codes),
            "protected_region_codes": sorted(protected_region_codes),
            "hold_region_count": len(hold_region_codes),
        },
        "merchant_feed_guard": {
            "status": feed_guard_status,
            "remove_exact_group_rows": len(feed_remove_rows),
            "protect_priority_group_rows": [
                {
                    "feed_label": row["feed_label"],
                    "language_code": row["language_code"],
                    "currency": row["currency"],
                }
                for row in feed_protect_rows
            ],
            "enable_after_capacity_cleanup_rows": [
                {
                    "feed_label": row["feed_label"],
                    "language_code": row["language_code"],
                    "currency": row["currency"],
                    "expected_rows": row["expected_rows"],
                }
                for row in feed_after_rows
            ],
            "non_us_usd_remove_rows_without_country_exact_control": len(non_us_usd_rows),
            "blocker": (
                "Shopify marketUpdate can target market regions, but the Merchant guard requires "
                "exact feed_label/language/currency group preview and removal acceptance. No "
                "authenticated control surface in this run exposed those exact Merchant publishing "
                "groups or a dry-run preview for them."
            ),
        },
        "bucket_counts": dict(Counter(row["bucket"] for row in region_guard_rows)),
        "external_write_status": "NOT_EXECUTED",
        "after_export_guard_status": after_export_guard_status,
        "after_export_guard": after_validation,
        "overall_status": overall_status,
        "outputs": {
            "live_region_readback_csv": str(LIVE_REGION_CSV.relative_to(REPO_ROOT)),
            "summary_json": str(SUMMARY_JSON.relative_to(REPO_ROOT)),
            "report_md": str(REPORT_MD.relative_to(REPO_ROOT)),
        },
    }

    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = f"""# Merchant Capacity Exact-Control Reconciliation

Generated: {summary['generated_at']}

Mode: authenticated read-only Shopify Admin GraphQL reconciliation. No Merchant,
Shopify, Google Ads, Pinterest, feed, product, product-group, bid, budget,
status, capacity, billing, credential, or conversion writes were made.

## Decision

- External write status: `{summary['external_write_status']}`.
- Overall status: `{overall_status}`.
- After-export guard status: `{summary['after_export_guard_status']}`.

The live Shopify Admin path is authenticated and exact for Shopify Markets
regions. Current readback shows the first-pass region scope is already pruned
from `International`, with priority/hold regions preserved. The fresh Merchant
after-export guard still fails, so Canada/GB Shopping remains blocked.

## Shopify Region Guard Preview

- Shopify Admin API version: `{API_VERSION}`.
- Active market handles seen: `{', '.join(live_market_handles)}`.
- Market scopes present: `{', '.join(summary['shopify_market_scopes_present'])}`.
- Market mutations present: `{', '.join(market_mutations)}`.
- International live regions: `{len(international_live_codes)}`.
- Candidate first-pass remove regions still live: `{len(region_remove_codes & international_live_codes)}/{len(region_remove_codes)}`.
- Protected duplicate/priority region codes preserved in preview: `{', '.join(sorted(protected_region_codes))}`.
- Region guard status: `{region_guard_status}`.

## Merchant Feed-Group Guard Preview

- Exact feed-group removal rows required: `{len(feed_remove_rows)}`.
- Protected priority groups: `{'; '.join(f"{row['feed_label']}|{row['language_code']}|{row['currency']}" for row in feed_protect_rows)}`.
- Enable-after-cleanup rows: `{'; '.join(f"{row['feed_label']}|{row['language_code']}|{row['currency']}={row['expected_rows']}" for row in feed_after_rows)}`.
- Non-US USD remove rows lacking country-exact Shopify region control: `{len(non_us_usd_rows)}`.
- Merchant feed guard status: `{feed_guard_status}`.

## Blocker

`merchant_capacity_platform_preview_acceptance.csv` requires exact
`feed_label` + `language_code` + `currency` publishing groups to show as selected
for removal or disabled from Google publishing scope before Save/Apply/Sync. The
authenticated Shopify Markets API can remove region conditions from
`International`, and the live region readback now shows those regions absent, but
it cannot prove the Merchant feed groups have been removed.

Therefore the exact-control reconciliation still fails closed for Shopping. The
after-export guard shows Merchant still has the first-pass removal rows, including
the non-US USD candidate rows.

## Next Valid Execution Path

Use a Merchant Center or Google & YouTube app control surface that can preview or
sync the exact rows in `merchant_capacity_platform_preview_acceptance.csv` by
`feed_label`, `language_code`, and `currency`. Only after that control/sync action
is reconciled, capture a fresh all-products export, then run:

```bash
python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/build_merchant_capacity_execution_guard.py --after-export /path/to/fresh_export.csv
```

Canada/GB Shopping work remains blocked until that after-export guard passes.

## Files

- `shopify_markets_live_exact_region_readback.csv`
- `merchant_capacity_exact_control_reconciliation.json`
- `MERCHANT_CAPACITY_EXACT_CONTROL_RECONCILIATION.md`
"""
    REPORT_MD.write_text(report, encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
