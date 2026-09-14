#!/usr/bin/env python3.13
"""
Build a parent-only Pinterest paid catalog feed from the verified US
collection-intent grouped feed.

This script is local/deterministic. It does not call Shopify, Pinterest,
Cloudflare, Merchant, Google Ads, or any external API. It takes the already
verified variant feed where each Shopify parent has shared `item_group_id`,
then emits exactly one row per active parent product in the paid lanes:

- mommy_and_me
- family_matching
- daddy_and_me

The goal is to make Pinterest product-group selector counts match the owner's
storefront collection inventory counts while preserving the parent product's
hero image and PDP link.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-20-pinterest-shopify-collection-mapping"
)
DEFAULT_INPUT = PACKET_DIR / "feeds/pinterest_us_collection_intent.tsv"
DEFAULT_OUTPUT = PACKET_DIR / "feeds/pinterest_us_paid_parent_collection_intent.tsv"
DEFAULT_PARENT_READBACK = PACKET_DIR / "pinterest_us_paid_parent_feed_readback.csv"
LABEL_VERSION = "collection_intent_parent_v20260520"
PAID_LANES = ("mommy_and_me", "family_matching", "daddy_and_me")
EXPECTED_PARENT_COUNTS = {
    "mommy_and_me": 99,
    "family_matching": 77,
    "daddy_and_me": 34,
}
SUPPLIER_BLOCK_HOSTS = (
    "alibaba.com",
    "aliexpress.com",
    "1688.com",
    "taobao.com",
    "tmall.com",
)

COLUMNS = [
    "id",
    "item_group_id",
    "title",
    "description",
    "link",
    "image_link",
    "additional_image_link",
    "availability",
    "price",
    "sale_price",
    "brand",
    "condition",
    "google_product_category",
    "product_type",
    "gtin",
    "identifier_exists",
    "mpn",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
]


def money_value(value: str) -> tuple[Decimal, str]:
    raw = (value or "").strip()
    match = re.search(r"\d+(?:[.,]\d+)?", raw)
    if not match:
        return Decimal("999999"), raw
    try:
        return Decimal(match.group(0).replace(",", ".")), raw
    except InvalidOperation:
        return Decimal("999999"), raw


def strip_variant_suffix(title: str) -> str:
    title = re.sub(r"\s*\((?:Size|Color|Type):.*\)\s*$", "", title or "").strip()
    return title[:150]


def choose_subgroup(lane: str, title: str, product_type: str) -> str:
    haystack = f"{title or ''} {product_type or ''}".lower()
    if lane == "daddy_and_me":
        return "daddy_shirts_tshirts"
    if "pajama" in haystack or "sleep" in haystack:
        return "pajamas"
    if "swim" in haystack or "tankini" in haystack or "bikini" in haystack:
        return "swimwear"
    if "dress" in haystack or "sundress" in haystack or "maxi" in haystack:
        return "dresses"
    if "cardigan" in haystack or "sweater" in haystack or "knit" in haystack or "outerwear" in haystack:
        return "sweaters_outerwear"
    if "shirt" in haystack or "tee" in haystack or "top" in haystack or "blouse" in haystack:
        return "tops_shirts"
    return "outfit_sets"


def supplier_hit(row: dict[str, str]) -> bool:
    haystack = "\t".join(str(v or "").lower() for v in row.values())
    return any(host in haystack for host in SUPPLIER_BLOCK_HOSTS)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def choose_parent_row(rows: list[dict[str, str]]) -> dict[str, str]:
    in_stock_rows = [r for r in rows if (r.get("availability") or "").strip().lower() == "in stock"]
    candidates = in_stock_rows or rows
    chosen = sorted(
        candidates,
        key=lambda r: (
            money_value(r.get("price", ""))[0],
            r.get("id", ""),
        ),
    )[0]
    parent_id = chosen["item_group_id"].strip()
    lane = chosen["custom_label_2"].strip()
    row = {key: chosen.get(key, "") for key in COLUMNS}
    row["id"] = f"shopify_us_parent_{parent_id}"
    row["item_group_id"] = parent_id
    row["title"] = strip_variant_suffix(chosen.get("title", ""))
    row["availability"] = "in stock" if in_stock_rows else "out of stock"
    row["custom_label_0"] = "us"
    row["custom_label_1"] = "primary_paid_lane"
    row["custom_label_2"] = lane
    row["custom_label_3"] = choose_subgroup(lane, row["title"], chosen.get("product_type", ""))
    row["custom_label_4"] = LABEL_VERSION
    return row


def build_parent_feed(input_path: Path, output_path: Path, parent_readback_path: Path) -> dict:
    if not input_path.exists():
        raise SystemExit(f"FATAL: missing input feed: {input_path}")

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            raise SystemExit("FATAL: input feed header does not match expected Pinterest feed schema")
        for row in reader:
            lane = (row.get("custom_label_2") or "").strip()
            parent_id = (row.get("item_group_id") or "").strip()
            if lane not in PAID_LANES:
                continue
            if not parent_id:
                raise SystemExit(f"FATAL: paid row missing item_group_id: {row.get('id')}")
            groups[parent_id].append(row)

    rows = [choose_parent_row(groups[parent_id]) for parent_id in sorted(groups)]
    rows.sort(key=lambda r: (r["custom_label_2"], r["custom_label_3"], r["title"], r["item_group_id"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=COLUMNS,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    with parent_readback_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "item_group_id",
            "lane",
            "subgroup",
            "title",
            "link",
            "image_link",
            "availability",
            "price",
            "variant_rows_collapsed",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "item_group_id": row["item_group_id"],
                    "lane": row["custom_label_2"],
                    "subgroup": row["custom_label_3"],
                    "title": row["title"],
                    "link": row["link"],
                    "image_link": row["image_link"],
                    "availability": row["availability"],
                    "price": row["price"],
                    "variant_rows_collapsed": len(groups[row["item_group_id"]]),
                }
            )

    lane_counts = Counter(row["custom_label_2"] for row in rows)
    subgroup_counts: dict[str, dict[str, int]] = {}
    for lane in PAID_LANES:
        subgroup_counts[lane] = dict(
            sorted(Counter(row["custom_label_3"] for row in rows if row["custom_label_2"] == lane).items())
        )

    duplicate_ids = [item_id for item_id, count in Counter(row["id"] for row in rows).items() if count > 1]
    missing_required = {
        field: sum(1 for row in rows if not (row.get(field) or "").strip())
        for field in ("id", "item_group_id", "title", "link", "image_link", "price", "availability")
    }
    supplier_hits = sum(1 for row in rows if supplier_hit(row))
    label_versions = sorted(set(row["custom_label_4"] for row in rows))
    digest = sha256_file(output_path)

    summary = {
        "mode": "pinterest_paid_parent_only_feed",
        "input": str(input_path.relative_to(REPO_ROOT)),
        "output": str(output_path.relative_to(REPO_ROOT)),
        "parent_readback": str(parent_readback_path.relative_to(REPO_ROOT)),
        "sha256": digest,
        "row_count": len(rows),
        "unique_parent_count": len({row["item_group_id"] for row in rows}),
        "counts_by_paid_lane": dict(sorted(lane_counts.items())),
        "expected_parent_counts": EXPECTED_PARENT_COUNTS,
        "counts_match_expected": dict(lane_counts) == EXPECTED_PARENT_COUNTS,
        "subgroup_counts_by_paid_lane": subgroup_counts,
        "custom_label_4_values": label_versions,
        "duplicate_id_count": len(duplicate_ids),
        "missing_required_counts": missing_required,
        "supplier_source_host_hit_count": supplier_hits,
        "guardrail_unique_ids": not duplicate_ids,
        "guardrail_required_fields_present": all(count == 0 for count in missing_required.values()),
        "guardrail_supplier_source_clean": supplier_hits == 0,
        "not_live_upload_authority": True,
    }
    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.with_suffix(".sha256").write_text(f"{digest}  {output_path.name}\n", encoding="utf-8")

    failures = []
    if not summary["counts_match_expected"]:
        failures.append(f"counts mismatch: {dict(lane_counts)} != {EXPECTED_PARENT_COUNTS}")
    if duplicate_ids:
        failures.append(f"{len(duplicate_ids)} duplicate IDs")
    if not summary["guardrail_required_fields_present"]:
        failures.append(f"missing required fields: {missing_required}")
    if supplier_hits:
        failures.append(f"{supplier_hits} supplier/source host hits")
    if failures:
        raise SystemExit("FATAL: " + "; ".join(failures))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--parent-readback", type=Path, default=DEFAULT_PARENT_READBACK)
    args = parser.parse_args()

    summary = build_parent_feed(args.input, args.output, args.parent_readback)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
