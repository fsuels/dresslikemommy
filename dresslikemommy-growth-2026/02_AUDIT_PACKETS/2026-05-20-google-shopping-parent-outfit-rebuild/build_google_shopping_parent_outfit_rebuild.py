#!/usr/bin/env python3
"""Build a no-write parent-outfit Google Shopping rebuild packet.

This script uses the current collection-intent grouped US feed as the source of
truth for parent products, item_group_id, collection lane, subcategory, URL, and
hero image. It writes local planning artifacts only.
"""

from __future__ import annotations

import csv
import json
import re
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
PACKET = Path(__file__).resolve().parent
INPUT_FEED = (
    REPO
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-shopify-collection-mapping/feeds/pinterest_us_collection_intent.tsv"
)
OLD_SHOPPING_AUDIT = (
    REPO
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-campaign-hierarchy-audit/google_shopping_parent_rollup.csv"
)

LANE_ORDER = ["mommy_and_me", "family_matching", "daddy_and_me"]
LANE_CAMPAIGNS = {
    "mommy_and_me": "DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2",
    "family_matching": "DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2",
    "daddy_and_me": "DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2",
}
LANE_LABELS = {
    "mommy_and_me": "Mommy & Me",
    "family_matching": "Family Matching",
    "daddy_and_me": "Daddy & Me",
}
SUBCATEGORY_LABELS = {
    "dresses": "Dresses",
    "swimwear": "Swimwear",
    "pajamas": "Pajamas",
    "tops_shirts": "Tops & Shirts",
    "sets": "Sets",
    "sweaters_outerwear": "Sweaters & Outerwear",
}
AD_GROUP_ORDER = [
    "dresses",
    "swimwear",
    "pajamas",
    "tops_shirts",
    "sets",
    "sweaters_outerwear",
]
LABEL_VERSION = "us_parent_outfit_ready_v20260520"
PROPOSED_PARENT_LABEL = "custom_label_1"
PROPOSED_SUBCATEGORY_LABEL = "custom_label_2"

KNOWN_ARCHIVED_DADDY_TARGETS = [
    {
        "handle": "daddy-me-my-best-lady-my-best-man",
        "reason": "ARCHIVED_UNPUBLISHED_NO_ONLINE_STORE_URL",
    },
    {
        "handle": "father-and-child-pilot-co-pilot-matching-t-shirt-set-perfect-for-daddy-me-outfits",
        "reason": "ARCHIVED_UNPUBLISHED_NO_ONLINE_STORE_URL",
    },
]


def read_csv(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def public_status(url: str) -> tuple[int, str]:
    if not url:
        return 0, "missing_url"
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, url
    except Exception as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def normalize_subcategory(product_type: str, title: str) -> str:
    text = f"{product_type} {title}".lower()
    if any(term in text for term in ["pajama", "sleepwear"]):
        return "pajamas"
    if any(term in text for term in ["swim", "bikini", "tankini", "trunk", "beachwear"]):
        return "swimwear"
    if any(term in text for term in ["sweater", "cardigan", "outerwear", "jacket", "coat"]):
        return "sweaters_outerwear"
    if any(term in text for term in ["t-shirt", "tee", "shirt", "top"]):
        return "tops_shirts"
    if "dress" in text:
        return "dresses"
    return "sets"


def parent_title(title: str) -> str:
    return re.sub(r"\s+\(Size:.*$", "", title).strip()


def source_parent_rows(feed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_parent: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in feed_rows:
        by_parent[row["item_group_id"]].append(row)

    rows: list[dict[str, Any]] = []
    for parent_id, variants in sorted(by_parent.items()):
        first = variants[0]
        lane = first.get("custom_label_2", "")
        subcategory = normalize_subcategory(first.get("product_type", ""), first.get("title", ""))
        status, effective_url = public_status(first.get("link", ""))
        # The grouped feed is generated from active/public Shopify data. Public
        # storefront probes can return 403 after repeated automated requests, so
        # treat explicit 404 as a hard exclusion and preserve 403 as a warning.
        include = lane in LANE_ORDER and status != 404 and bool(first.get("image_link")) and bool(parent_id)
        reason = "INCLUDED_PARENT_OUTFIT"
        if lane not in LANE_ORDER:
            reason = "EXCLUDED_NOT_IN_MAIN_PARENT_LANES"
        elif status == 404:
            reason = f"EXCLUDED_PUBLIC_URL_STATUS_{status}"
        elif not first.get("image_link"):
            reason = "EXCLUDED_MISSING_PARENT_HERO_IMAGE"
        elif not parent_id:
            reason = "EXCLUDED_MISSING_ITEM_GROUP_ID"

        rows.append(
            {
                "decision": "INCLUDE" if include else "EXCLUDE",
                "reason": reason,
                "parent_product_id": parent_id,
                "item_group_id": parent_id,
                "handle": first.get("link", "").rstrip("/").rsplit("/", 1)[-1],
                "parent_title": parent_title(first.get("title", "")),
                "lane": lane,
                "lane_label": LANE_LABELS.get(lane, lane),
                "subcategory": subcategory,
                "subcategory_label": SUBCATEGORY_LABELS.get(subcategory, subcategory),
                "variant_rows": len(variants),
                "link": first.get("link", ""),
                "effective_url": effective_url,
                "public_status": status,
                "hero_image_link": first.get("image_link", ""),
                "product_type": first.get("product_type", ""),
                "current_custom_label_0": first.get("custom_label_0", ""),
                "current_custom_label_1": first.get("custom_label_1", ""),
                "current_custom_label_2": first.get("custom_label_2", ""),
                "current_custom_label_3": first.get("custom_label_3", ""),
                "current_custom_label_4": first.get("custom_label_4", ""),
                "proposed_custom_label_0": "paid_eligible" if include else "",
                "proposed_custom_label_1": lane if include else "",
                "proposed_custom_label_2": subcategory if include else "",
                "proposed_custom_label_3": "parent_outfit" if include else "",
                "proposed_custom_label_4": LABEL_VERSION if include else "",
            }
        )
    return rows


def variant_label_rows(feed_rows: list[dict[str, str]], parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parents = {row["item_group_id"]: row for row in parent_rows}
    rows: list[dict[str, Any]] = []
    for row in feed_rows:
        parent = parents[row["item_group_id"]]
        include = parent["decision"] == "INCLUDE"
        rows.append(
            {
                "decision": parent["decision"],
                "reason": parent["reason"],
                "item_id": row["id"],
                "item_group_id": row["item_group_id"],
                "parent_product_id": parent["parent_product_id"],
                "handle": parent["handle"],
                "variant_title": row["title"],
                "link": row["link"],
                "image_link": row["image_link"],
                "proposed_item_group_id": row["item_group_id"] if include else "",
                "proposed_image_link": parent["hero_image_link"] if include else "",
                "proposed_custom_label_0": "paid_eligible" if include else "",
                "proposed_custom_label_1": parent["lane"] if include else "",
                "proposed_custom_label_2": parent["subcategory"] if include else "",
                "proposed_custom_label_3": "parent_outfit" if include else "",
                "proposed_custom_label_4": LABEL_VERSION if include else "",
            }
        )
    return rows


def campaign_blueprint(parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    included = [row for row in parent_rows if row["decision"] == "INCLUDE"]
    by_lane = Counter(row["lane"] for row in included)
    rows: list[dict[str, Any]] = []
    for lane in LANE_ORDER:
        rows.append(
            {
                "campaign_name": LANE_CAMPAIGNS[lane],
                "status_if_imported": "PAUSED",
                "channel": "Standard Shopping",
                "country": "US",
                "feed_label": "US",
                "bidding": "approval_required_recommend_start_with_manual_cpc_or_maximize_clicks_cap_review",
                "budget": "approval_required_no_live_budget_write_in_this_packet",
                "inventory_scope": f"custom_label_0=paid_eligible AND custom_label_1={lane} AND custom_label_4={LABEL_VERSION}",
                "top_level_lane": lane,
                "expected_parent_outfits": by_lane.get(lane, 0),
                "catchall_policy": "exclude_everything_else_at_campaign_and_ad_group_product_group_levels",
            }
        )
    return rows


def ad_group_blueprint(parent_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    included = [row for row in parent_rows if row["decision"] == "INCLUDE"]
    count_by_key = Counter((row["lane"], row["subcategory"]) for row in included)
    variant_count_by_key: Counter[tuple[str, str]] = Counter()
    for row in included:
        variant_count_by_key[(row["lane"], row["subcategory"])] += int(row["variant_rows"])

    rows: list[dict[str, Any]] = []
    for lane in LANE_ORDER:
        for subcategory in AD_GROUP_ORDER:
            parent_count = count_by_key.get((lane, subcategory), 0)
            if not parent_count:
                continue
            rows.append(
                {
                    "campaign_name": LANE_CAMPAIGNS[lane],
                    "ad_group_name": f"{LANE_LABELS[lane]} - {SUBCATEGORY_LABELS[subcategory]}",
                    "status_if_imported": "PAUSED",
                    "lane": lane,
                    "subcategory": subcategory,
                    "parent_outfits": parent_count,
                    "variant_rows": variant_count_by_key[(lane, subcategory)],
                    "ad_group_inventory_scope": f"custom_label_1={lane} AND custom_label_2={subcategory} AND custom_label_4={LABEL_VERSION}",
                    "product_group_include": f"{PROPOSED_PARENT_LABEL}={lane} > {PROPOSED_SUBCATEGORY_LABEL}={subcategory}",
                    "catchall_policy": "exclude_everything_else",
                }
            )
    return rows


def product_group_tree(ad_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ad_group in ad_groups:
        rows.append(
            {
                "campaign_name": ad_group["campaign_name"],
                "ad_group_name": ad_group["ad_group_name"],
                "level": 1,
                "dimension": PROPOSED_PARENT_LABEL,
                "value": ad_group["lane"],
                "action": "SUBDIVIDE",
                "status_if_imported": "PAUSED",
                "bid": "approval_required",
            }
        )
        rows.append(
            {
                "campaign_name": ad_group["campaign_name"],
                "ad_group_name": ad_group["ad_group_name"],
                "level": 2,
                "dimension": PROPOSED_SUBCATEGORY_LABEL,
                "value": ad_group["subcategory"],
                "action": "INCLUDE_UNIT",
                "status_if_imported": "PAUSED",
                "bid": "approval_required",
            }
        )
        rows.append(
            {
                "campaign_name": ad_group["campaign_name"],
                "ad_group_name": ad_group["ad_group_name"],
                "level": 2,
                "dimension": PROPOSED_SUBCATEGORY_LABEL,
                "value": "Everything else",
                "action": "EXCLUDE_UNIT",
                "status_if_imported": "EXCLUDED",
                "bid": "",
            }
        )
    for lane in LANE_ORDER:
        rows.append(
            {
                "campaign_name": LANE_CAMPAIGNS[lane],
                "ad_group_name": "ALL_AD_GROUPS",
                "level": 1,
                "dimension": PROPOSED_PARENT_LABEL,
                "value": "Everything else",
                "action": "EXCLUDE_UNIT",
                "status_if_imported": "EXCLUDED",
                "bid": "",
            }
        )
    return rows


def old_404_exclusions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not OLD_SHOPPING_AUDIT.exists():
        return rows
    for row in read_csv(OLD_SHOPPING_AUDIT):
        if row.get("image_match_feed_vs_shopify_first") == "UNKNOWN_NO_IMAGE":
            rows.append(
                {
                    "handle": row.get("handle", ""),
                    "parent_product_id": row.get("parent_product_id", ""),
                    "reason": "HISTORICALLY_SERVED_URL_UNAVAILABLE_404_CONFIRMED_20260520",
                    "historic_clicks": row.get("clicks", "0"),
                    "historic_impressions": row.get("impressions", "0"),
                    "historic_cost_usd": row.get("cost_usd", "0"),
                    "landing_url": row.get("landing_url", ""),
                }
            )
    return rows


def write_report(
    parent_rows: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    campaigns: list[dict[str, Any]],
    ad_groups: list[dict[str, Any]],
    exclusions: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    lines = [
        "# Google Shopping Parent-Outfit Rebuild Packet",
        "",
        f"Generated: `{date.today().isoformat()}`",
        "",
        "Mode: local/no-write rebuild packet. No Google Ads, Merchant, Shopify, Pinterest, feed, product, product-group, budget, bid, status, conversion, billing, or theme write occurred.",
        "",
        "## Decision",
        "",
        "- Keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.",
        "- Do not reuse its mixed product-group tree.",
        "- Rebuild around parent outfits: three top-level Shopping lanes, subgroups underneath, shared `item_group_id`, parent hero images, no catchall leakage, and no 404/archived products.",
        "",
        "## Proposed Paused Structure",
        "",
        "| Campaign | Parent lane | Parent outfits | Status if imported | Inventory scope |",
        "|---|---|---:|---|---|",
    ]
    for row in campaigns:
        lines.append(
            f"| `{row['campaign_name']}` | `{row['top_level_lane']}` | {row['expected_parent_outfits']} | `{row['status_if_imported']}` | `{row['inventory_scope']}` |"
        )
    lines.extend(
        [
            "",
            "## Subgroup Ad Groups",
            "",
            "| Campaign | Ad group | Parent outfits | Variant rows | Scope |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in ad_groups:
        lines.append(
            f"| `{row['campaign_name']}` | `{row['ad_group_name']}` | {row['parent_outfits']} | {row['variant_rows']} | `{row['ad_group_inventory_scope']}` |"
        )
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Included parent outfits: `{summary['included_parent_outfits']}`.",
            f"- Included variant rows: `{summary['included_variant_rows']}`.",
            f"- Parent lane counts: `{json.dumps(summary['included_parent_counts_by_lane'], sort_keys=True)}`.",
            f"- Subcategory counts: `{json.dumps(summary['included_parent_counts_by_subcategory'], sort_keys=True)}`.",
            f"- Public URL hard failures (`404`) inside proposed included scope: `{summary['included_public_url_404_failures']}`.",
            f"- Public URL non-200 probe warnings inside proposed included scope: `{summary['included_public_url_non_200_probe_warnings']}`; these are not hard exclusions because the current-active feed is the active-product source and automated storefront probes can return `403`.",
            f"- Missing `item_group_id` inside proposed included scope: `{summary['included_missing_item_group_id']}`.",
            f"- Missing hero image inside proposed included scope: `{summary['included_missing_hero_image']}`.",
            f"- Excluded current-feed parents: `{summary['excluded_current_feed_parents']}`.",
            f"- Historic 404 Shopping parents held out: `{summary['historic_404_held_out']}`.",
            f"- Known archived Daddy & Me targets held out: `{summary['known_archived_daddy_targets_held_out']}`.",
            "",
            "Daddy & Me is `34` active/feed-mapped parent outfits right now, not `36`; two Daddy & Me t-shirt products are archived/unpublished and must stay out until restored and reverified.",
            "",
            "## Label Contract",
            "",
            "| Field | Proposed use |",
            "|---|---|",
            "| `item_group_id` | Shopify parent product ID, shared by every size/color variant of the same outfit |",
            "| `image_link` | Parent/collection hero image for every variant in the same outfit |",
            "| `custom_label_0` | `paid_eligible` inclusion gate |",
            "| `custom_label_1` | parent collection lane: `mommy_and_me`, `family_matching`, `daddy_and_me` |",
            "| `custom_label_2` | subgroup: `dresses`, `swimwear`, `pajamas`, `tops_shirts`, `sets`, `sweaters_outerwear` |",
            "| `custom_label_3` | `parent_outfit` |",
            f"| `custom_label_4` | `{LABEL_VERSION}` readiness/version gate |",
            "",
            "## Approval Boundary",
            "",
            "This packet is not a live approval to upload Merchant labels or create Google Ads campaigns. Creating even paused Shopping campaigns, changing product groups, changing feed labels, or uploading feed changes is a live external write and needs fresh action-time approval plus before/after readback.",
            "",
            "Exact approval phrase for the next live step, if accepted later:",
            "",
            "> Approve the Google Shopping parent-outfit paused rebuild only: keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused, create/import only paused V2 Shopping structures from the packet, do not enable spend, do not change budgets/bids/statuses beyond paused draft requirements, do not include catchalls, and read back counts/images before any activation discussion.",
            "",
            "## Files",
            "",
            "- `shopping_parent_outfit_manifest.csv`: parent outfit inclusion/exclusion manifest.",
            "- `merchant_label_update_spec.csv`: per-variant feed label/image/item_group_id specification.",
            "- `shopping_campaign_blueprint.csv`: three paused top-level Shopping lanes.",
            "- `shopping_ad_group_blueprint.csv`: subgroup ad groups under each lane.",
            "- `shopping_product_group_tree.csv`: no-catchall product group tree spec.",
            "- `excluded_products_do_not_advertise.csv`: 404/archived/current-feed excluded products.",
            "- `google_shopping_parent_outfit_rebuild_summary.json`: machine-readable summary.",
        ]
    )
    (PACKET / "GOOGLE_SHOPPING_PARENT_OUTFIT_REBUILD_PACKET.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    feed_rows = read_csv(INPUT_FEED, delimiter="\t")
    parents = source_parent_rows(feed_rows)
    variant_rows = variant_label_rows(feed_rows, parents)
    campaigns = campaign_blueprint(parents)
    ad_groups = ad_group_blueprint(parents)
    tree = product_group_tree(ad_groups)

    historic_404 = old_404_exclusions()
    archived = [
        {
            "handle": row["handle"],
            "parent_product_id": "",
            "reason": row["reason"],
            "historic_clicks": "",
            "historic_impressions": "",
            "historic_cost_usd": "",
            "landing_url": f"https://www.dresslikemommy.com/products/{row['handle']}",
        }
        for row in KNOWN_ARCHIVED_DADDY_TARGETS
    ]
    current_feed_excluded = [
        {
            "handle": row["handle"],
            "parent_product_id": row["parent_product_id"],
            "reason": row["reason"],
            "historic_clicks": "",
            "historic_impressions": "",
            "historic_cost_usd": "",
            "landing_url": row["link"],
        }
        for row in parents
        if row["decision"] == "EXCLUDE"
    ]
    exclusions = sorted(historic_404 + archived + current_feed_excluded, key=lambda row: (row["reason"], row["handle"]))

    included_parents = [row for row in parents if row["decision"] == "INCLUDE"]
    included_variants = [row for row in variant_rows if row["decision"] == "INCLUDE"]
    summary = {
        "generated": date.today().isoformat(),
        "mode": "local_no_write",
        "input_feed": str(INPUT_FEED.relative_to(REPO)),
        "included_parent_outfits": len(included_parents),
        "included_variant_rows": len(included_variants),
        "included_parent_counts_by_lane": dict(sorted(Counter(row["lane"] for row in included_parents).items())),
        "included_parent_counts_by_subcategory": dict(
            sorted(Counter(row["subcategory"] for row in included_parents).items())
        ),
        "included_parent_counts_by_lane_subcategory": {
            f"{lane}:{subcategory}": count
            for (lane, subcategory), count in sorted(
                Counter((row["lane"], row["subcategory"]) for row in included_parents).items()
            )
        },
        "included_public_url_404_failures": sum(1 for row in included_parents if int(row["public_status"]) == 404),
        "included_public_url_non_200_probe_warnings": sum(
            1 for row in included_parents if int(row["public_status"]) not in {200, 404}
        ),
        "included_missing_item_group_id": sum(1 for row in included_parents if not row["item_group_id"]),
        "included_missing_hero_image": sum(1 for row in included_parents if not row["hero_image_link"]),
        "excluded_current_feed_parents": sum(1 for row in parents if row["decision"] == "EXCLUDE"),
        "historic_404_held_out": len(historic_404),
        "known_archived_daddy_targets_held_out": len(archived),
        "campaigns": campaigns,
        "ad_group_count": len(ad_groups),
        "guardrails": [
            "No live external writes.",
            "No catchall include rows.",
            "No 404/archived products in proposed included scope.",
            "Every included row has item_group_id and hero image.",
        ],
    }

    write_csv(PACKET / "shopping_parent_outfit_manifest.csv", parents)
    write_csv(PACKET / "merchant_label_update_spec.csv", variant_rows)
    write_csv(PACKET / "shopping_campaign_blueprint.csv", campaigns)
    write_csv(PACKET / "shopping_ad_group_blueprint.csv", ad_groups)
    write_csv(PACKET / "shopping_product_group_tree.csv", tree)
    write_csv(PACKET / "excluded_products_do_not_advertise.csv", exclusions)
    (PACKET / "google_shopping_parent_outfit_rebuild_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(parents, variant_rows, campaigns, ad_groups, exclusions, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
