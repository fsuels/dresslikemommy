#!/usr/bin/env python3.13
"""
Build one local Pinterest grouped-feed artifact from all active Shopify Markets.

Gate B-1 only:
- Calls generate_pinterest_feed_grouped.py for each configured market.
- Merges the per-market TSVs into pinterest_unified_all_markets.tsv.
- Adds audit columns: market_handle, country, language.
- Writes a deterministic SHA-256 checksum and summary JSON.

This script is read-only against Shopify Admin through the per-market generator.
It does not upload, publish, save, pause, sync, or mutate Shopify/Pinterest data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-15-pinterest-feed-grouping-all-markets-fix"
)
FEEDS_DIR = PACKET_DIR / "feeds"
GENERATOR = REPO_ROOT / "ops/scripts/generate_pinterest_feed_grouped.py"
UNIFIED_FEED = FEEDS_DIR / "pinterest_unified_all_markets.tsv"
SUMMARY_PATH = FEEDS_DIR / "pinterest_unified_all_markets.summary.json"
SHA256_PATH = FEEDS_DIR / "pinterest_unified_all_markets.sha256"

SUPPLIER_BLOCK_HOSTS = (
    "alibaba.com",
    "aliexpress.com",
    "1688.com",
    "taobao.com",
    "tmall.com",
)

MARKETS = [
    {"handle": "us", "country": "US", "language": "en"},
    {"handle": "canada", "country": "CA", "language": "en"},
    {"handle": "united-kingdom", "country": "GB", "language": "en"},
    # These are aggregate Shopify Markets, not a single Pinterest target country.
    # Keep them explicit for Gate B-3 mapping instead of inventing a country.
    {"handle": "eu", "country": "", "language": "en"},
    {"handle": "australia", "country": "AU", "language": "en"},
    {"handle": "international", "country": "", "language": "en"},
]


def run_generator(market: str, output: Path) -> None:
    output_arg = output
    try:
        output_arg = output.relative_to(REPO_ROOT)
    except ValueError:
        pass
    cmd = [
        sys.executable,
        str(GENERATOR),
        "--market",
        market,
        "--output",
        str(output_arg),
    ]
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def supplier_hit(row: dict[str, str]) -> bool:
    haystack = "\t".join(str(v or "").lower() for v in row.values())
    return any(host in haystack for host in SUPPLIER_BLOCK_HOSTS)


def build_unified(regenerate: bool) -> dict:
    FEEDS_DIR.mkdir(parents=True, exist_ok=True)

    per_market_summary: dict[str, dict] = {}
    unified_fields: list[str] | None = None
    row_count = 0
    ids = Counter()
    parent_images: dict[tuple[str, str], set[str]] = defaultdict(set)
    missing_item_group_id = 0
    missing_image_link = 0
    supplier_source_host_hits = 0

    with UNIFIED_FEED.open("w", newline="", encoding="utf-8") as out:
        writer: csv.DictWriter | None = None

        for market_meta in MARKETS:
            market = market_meta["handle"]
            feed_path = FEEDS_DIR / f"pinterest_{market}.tsv"
            if regenerate:
                run_generator(market, feed_path)
            if not feed_path.exists():
                raise SystemExit(f"FATAL: missing per-market feed: {feed_path}")

            market_rows = 0
            market_parents: set[str] = set()
            with feed_path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t")
                if not reader.fieldnames:
                    raise SystemExit(f"FATAL: missing header in {feed_path}")
                if unified_fields is None:
                    unified_fields = list(reader.fieldnames) + [
                        "market_handle",
                        "country",
                        "language",
                    ]
                    writer = csv.DictWriter(
                        out,
                        fieldnames=unified_fields,
                        delimiter="\t",
                        extrasaction="ignore",
                        lineterminator="\n",
                    )
                    writer.writeheader()
                elif list(reader.fieldnames) + ["market_handle", "country", "language"] != unified_fields:
                    raise SystemExit(f"FATAL: header drift in {feed_path}")

                assert writer is not None
                for row in reader:
                    row["market_handle"] = market
                    row["country"] = market_meta["country"]
                    row["language"] = market_meta["language"]
                    row_count += 1
                    market_rows += 1
                    item_id = (row.get("id") or "").strip()
                    item_group_id = (row.get("item_group_id") or "").strip()
                    image_link = (row.get("image_link") or "").strip()
                    ids[item_id] += 1
                    if item_group_id:
                        market_parents.add(item_group_id)
                        if image_link:
                            parent_images[(market, item_group_id)].add(image_link)
                    else:
                        missing_item_group_id += 1
                    if not image_link:
                        missing_image_link += 1
                    if supplier_hit(row):
                        supplier_source_host_hits += 1
                    writer.writerow(row)

            per_market_summary[market] = {
                "country": market_meta["country"],
                "language": market_meta["language"],
                "row_count": market_rows,
                "unique_parent_groups": len(market_parents),
            }

    duplicate_ids = sorted(item_id for item_id, count in ids.items() if count > 1)
    parent_image_drift = sorted(
        f"{market}:{item_group_id}"
        for (market, item_group_id), images in parent_images.items()
        if len(images) > 1
    )

    digest = sha256_file(UNIFIED_FEED)
    SHA256_PATH.write_text(f"{digest}  {UNIFIED_FEED.name}\n", encoding="utf-8")

    summary = {
        "mode": "gate_b1_local_readback_only",
        "output": str(UNIFIED_FEED.relative_to(REPO_ROOT)),
        "sha256": digest,
        "markets": per_market_summary,
        "row_count": row_count,
        "unique_item_ids": len(ids),
        "duplicate_item_id_count": len(duplicate_ids),
        "missing_item_group_id_count": missing_item_group_id,
        "missing_image_link_count": missing_image_link,
        "parent_groups_with_multiple_image_links": len(parent_image_drift),
        "supplier_source_host_hit_count": supplier_source_host_hits,
        "guardrail_item_group_id_present_on_every_row": missing_item_group_id == 0,
        "guardrail_image_link_present_on_every_row": missing_image_link == 0,
        "guardrail_parent_image_stable_per_market_group": not parent_image_drift,
        "guardrail_unique_item_ids": not duplicate_ids,
        "not_live_upload_authority": True,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    violations = []
    if missing_item_group_id:
        violations.append(f"{missing_item_group_id} rows missing item_group_id")
    if missing_image_link:
        violations.append(f"{missing_image_link} rows missing image_link")
    if parent_image_drift:
        violations.append(f"{len(parent_image_drift)} parent groups have multiple image_link values")
    if duplicate_ids:
        violations.append(f"{len(duplicate_ids)} duplicate item IDs")
    if supplier_source_host_hits:
        violations.append(f"{supplier_source_host_hits} supplier/source host hits")
    if violations:
        raise SystemExit("FATAL: " + "; ".join(violations))

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-regenerate",
        action="store_true",
        help="Merge existing per-market TSV files without calling Shopify Admin.",
    )
    args = parser.parse_args()

    summary = build_unified(regenerate=not args.skip_regenerate)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
