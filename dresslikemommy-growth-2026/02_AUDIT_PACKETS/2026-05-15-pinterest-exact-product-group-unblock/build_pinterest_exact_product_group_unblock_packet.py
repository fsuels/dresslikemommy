#!/usr/bin/env python3.13
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = Path(__file__).resolve().parent
SCOPE_CSV = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_refreshed_clean_scope.csv"
EXCLUSIONS_CSV = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_refreshed_public_exclusions.csv"
OUTPUT_MD = PACKET_DIR / "PINTEREST_EXACT_PRODUCT_GROUP_UNBLOCK_PACKET.md"
OUTPUT_SUMMARY = PACKET_DIR / "pinterest_exact_product_group_unblock_summary.json"
OUTPUT_GROUPS = PACKET_DIR / "pinterest_exact_category_group_requirements.csv"
OUTPUT_FATHER = PACKET_DIR / "pinterest_father_inclusive_probe.csv"


FATHER_PATTERN = re.compile(r"\b(dad|daddy|father|parents?)\b|mom-dad", re.IGNORECASE)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def unique_count(rows: list[dict[str, str]], key: str) -> int:
    return len({row.get(key, "") for row in rows if row.get(key, "")})


def status_pass_count(rows: list[dict[str, str]], key: str) -> int:
    return sum(1 for row in rows if row.get(key) == "PASS")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    scope_rows = read_csv(SCOPE_CSV)
    exclusion_rows = read_csv(EXCLUSIONS_CSV)

    by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scope_rows:
        by_group[row["custom_label_2"]].append(row)

    group_labels = {
        "mommy_me": "Mommy & Me",
        "family_matching": "Family Matching",
        "pajamas": "Pajamas",
    }
    exact_groups = []
    for key in ["mommy_me", "family_matching", "pajamas"]:
        rows = by_group[key]
        exact_groups.append(
            {
                "product_group_key": key,
                "product_group_label": group_labels[key],
                "filter_custom_label_0": "paid_eligible",
                "filter_custom_label_4": "us_test_ready",
                "filter_custom_label_2": key,
                "variants": len(rows),
                "products": unique_count(rows, "shopify_product_id"),
                "required_status": "exact_active_clean_only",
                "allowed_use": "catalog_sales_pin_clicks_custom_cpc_0_15_after_final_review",
            }
        )

    father_rows = []
    for row in scope_rows:
        text = " ".join([row.get("title", ""), row.get("product_url", ""), row.get("pinterest_group_label", "")])
        if FATHER_PATTERN.search(text):
            father_rows.append(row)

    father_products = {}
    for row in father_rows:
        product_id = row["shopify_product_id"]
        father_products.setdefault(
            product_id,
            {
                "shopify_product_id": product_id,
                "custom_label_2": row["custom_label_2"],
                "variants": 0,
                "title": row["title"],
                "product_url": row["product_url"],
            },
        )
        father_products[product_id]["variants"] += 1

    father_probe = sorted(father_products.values(), key=lambda row: (row["custom_label_2"], row["title"], row["shopify_product_id"]))

    write_csv(
        OUTPUT_GROUPS,
        [
            "product_group_key",
            "product_group_label",
            "filter_custom_label_0",
            "filter_custom_label_4",
            "filter_custom_label_2",
            "variants",
            "products",
            "required_status",
            "allowed_use",
        ],
        exact_groups,
    )
    write_csv(
        OUTPUT_FATHER,
        ["shopify_product_id", "custom_label_2", "variants", "title", "product_url"],
        father_probe,
    )

    checks = {
        "image_pass_rows": status_pass_count(scope_rows, "image_status"),
        "price_pass_rows": status_pass_count(scope_rows, "price_status"),
        "availability_pass_rows": status_pass_count(scope_rows, "availability_status"),
        "shipping_policy_pass_rows": status_pass_count(scope_rows, "shipping_policy_status"),
        "return_policy_pass_rows": status_pass_count(scope_rows, "return_policy_status"),
        "pdp_pass_rows": status_pass_count(scope_rows, "pdp_status"),
    }

    summary = {
        "generated_at": "2026-05-15T05:45:00-04:00",
        "mode": "repo_local_approval_packet_only_no_external_write",
        "advertiser_id": "549756244483",
        "campaign_name": "DLM_PIN_US_CATALOG_333_PAUSED_20260515",
        "clean_scope_rows": len(scope_rows),
        "clean_scope_products": unique_count(scope_rows, "shopify_product_id"),
        "held_exclusion_rows": len(exclusion_rows),
        "exact_groups": exact_groups,
        "father_inclusive_probe": {
            "variant_rows": len(father_rows),
            "products": len(father_probe),
            "category_counts": dict(Counter(row["custom_label_2"] for row in father_rows)),
            "status": "proof_only_do_not_create_separate_group_without_exact_owner_approval_and_platform_selector",
        },
        "row_quality_checks": checks,
        "required_approval": "I approve creating/exposing exact Pinterest product groups for advertiser 549756244483 from existing feed attributes only: paid_eligible + us_test_ready split by Mommy & Me, Family Matching, Pajamas, and any active clean Daddy & Me/father-inclusive rows that pass the same gates, excluding the 9 held variants, with no catalog source/feed source/tag/CAPI/billing/Shopify product changes, then launch only if final review shows max $5/day and max $0.15 CPC.",
        "external_write_status": "not_performed",
    }
    OUTPUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    md = f"""# Pinterest Exact Product-Group Unblock Packet

Generated: 2026-05-15 05:45 EDT

Mode: repo-local approval/build packet only. No Pinterest, Shopify, Merchant, Google Ads, GA4/GTM, tag, CAPI, catalog, feed, source, product, budget, bid, status, launch, publish, billing, or spend write occurred.

## Why This Exists

The approved Pinterest catalog sales launch reached a compliant CPC setup path, then stopped before publish because the live UI exposed only broad product groups. Broad groups would include products outside the refreshed active-clean whitelist.

This packet converts that blocker into the smallest exact approval/action surface: create or expose only exact product groups from existing feed attributes, then launch only after final review reconfirms the `333` clean scope, `$5/day` cap, and `$0.15` max CPC.

## Required Exact Groups

| Group | Feed filters | Variants | Products | Use |
|---|---|---:|---:|---|
"""
    for group in exact_groups:
        md += (
            f"| {group['product_group_label']} | `custom_label_0=paid_eligible`; "
            f"`custom_label_4=us_test_ready`; `custom_label_2={group['filter_custom_label_2']}` | "
            f"{group['variants']} | {group['products']} | Exact active-clean catalog sales group only |\n"
        )

    md += f"""
## Father-Inclusive Probe

The current clean scope contains `{len(father_rows)}` father/dad/parent-themed variant rows across `{len(father_probe)}` products. These rows are proof candidates, not launch authority for a separate Daddy & Me group.

| Product ID | Current group | Variants | Product |
|---|---|---:|---|
"""
    for row in father_probe:
        title = row["title"].replace("| DLM", "").strip()
        md += f"| `{row['shopify_product_id']}` | `{row['custom_label_2']}` | {row['variants']} | {title} |\n"

    md += f"""
## Row Quality Readback From Scope CSV

| Check | Passing rows |
|---|---:|
| Image status | {checks['image_pass_rows']} |
| Price status | {checks['price_pass_rows']} |
| Availability status | {checks['availability_pass_rows']} |
| Shipping policy status | {checks['shipping_policy_pass_rows']} |
| Return policy status | {checks['return_policy_pass_rows']} |
| Public PDP source-clean status | {checks['pdp_pass_rows']} |

Held exclusions remain excluded: `{len(exclusion_rows)}` variant rows across the public-source exclusion file.

## Approval Required

Exact phrase to unblock product-group creation/exposure:

`{summary['required_approval']}`

## Execution Checklist After Approval

1. Read back advertiser `549756244483`, account/domain, and current campaign count/spend before any write.
2. Create or expose exact groups only from existing feed attributes: `paid_eligible`, `us_test_ready`, and the named `custom_label_2` values.
3. Confirm each exact group count matches this packet or stop and record the mismatch.
4. Keep the `9` held variants excluded unless a separate approved cleanup/readback clears them.
5. Use `Catalog sales` + `Pin clicks` + `Custom` bidding because this is the known path that allows max CPC `$0.15`.
6. Final review before publish must confirm max `$5/day`, max `$0.15` CPC, exact product-group scope, and no catalog/source/feed/tag/CAPI/billing/Shopify mutation.
7. After publish, read back created object IDs, status, spend, serving, group counts, bid, budget, and no out-of-scope mutations.

## Stop Conditions

Stop before any save/publish if Pinterest requires broad groups, catalog/source/feed/tag/CAPI/billing changes, audience creation/edit, Performance+ bidding, CPC above `$0.15`, product rows outside the exact clean scope, account switch, permission, CAPTCHA, policy, or destructive confirmation.

## Decision

This is the closest Pinterest path to sales-moving execution. It avoids broad catalog waste, preserves the active-product/source-clean rule, and gives the owner one precise approval gate instead of another generic blocker.
"""
    OUTPUT_MD.write_text(md)


if __name__ == "__main__":
    main()
