#!/usr/bin/env python3
"""Validate the local Pinterest US paused-draft build spec.

This script reads local evidence files only. It does not call Pinterest,
Shopify, Merchant Center, Google Ads, or any external API.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent
SPEC_PATH = LANE / "pinterest_us_paused_draft_build_spec.json"
SUMMARY_PATH = LANE / "pinterest_us_paused_draft_build_spec_validation_summary.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def rel_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def check(condition: bool, name: str, observed: object, expected: object, checks: list[dict[str, object]]) -> None:
    checks.append(
        {
            "check": name,
            "status": "PASS" if condition else "FAIL",
            "observed": observed,
            "expected": expected,
        }
    )


def main() -> int:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    clean_path = rel_path(spec["scope"]["clean_scope_path"])
    exclusions_path = rel_path(spec["scope"]["exclusions_path"])
    clean_rows = read_csv(clean_path)
    exclusion_rows = read_csv(exclusions_path)

    clean_variant_ids = [row["shopify_variant_id"] for row in clean_rows]
    exclusion_variant_ids = [row["shopify_variant_id"] for row in exclusion_rows]
    clean_variant_set = set(clean_variant_ids)
    exclusion_variant_set = set(exclusion_variant_ids)
    group_counts = Counter(row["custom_label_2"] for row in clean_rows)

    check(clean_path.exists(), "clean_scope_exists", str(clean_path), True, checks)
    check(exclusions_path.exists(), "exclusions_exists", str(exclusions_path), True, checks)
    check(len(clean_rows) == spec["scope"]["clean_rows"], "clean_row_count", len(clean_rows), spec["scope"]["clean_rows"], checks)
    check(
        len(clean_variant_set) == spec["scope"]["unique_shopify_variant_ids"],
        "clean_unique_variant_count",
        len(clean_variant_set),
        spec["scope"]["unique_shopify_variant_ids"],
        checks,
    )
    check(sha256(clean_path) == spec["scope"]["clean_scope_sha256"], "clean_scope_sha256", sha256(clean_path), spec["scope"]["clean_scope_sha256"], checks)
    check(len(exclusion_rows) == len(spec["scope"]["excluded_shopify_variant_ids"]), "exclusion_row_count", len(exclusion_rows), len(spec["scope"]["excluded_shopify_variant_ids"]), checks)
    check(
        sorted(exclusion_variant_ids) == sorted(spec["scope"]["excluded_shopify_variant_ids"]),
        "exclusion_variant_ids",
        sorted(exclusion_variant_ids),
        sorted(spec["scope"]["excluded_shopify_variant_ids"]),
        checks,
    )
    check(not clean_variant_set.intersection(exclusion_variant_set), "clean_exclusion_overlap", sorted(clean_variant_set.intersection(exclusion_variant_set)), [], checks)
    check(sha256(exclusions_path) == spec["scope"]["exclusions_sha256"], "exclusions_sha256", sha256(exclusions_path), spec["scope"]["exclusions_sha256"], checks)
    check(
        dict(sorted(group_counts.items())) == dict(sorted(spec["scope"]["required_product_group_counts"].items())),
        "product_group_counts",
        dict(sorted(group_counts.items())),
        dict(sorted(spec["scope"]["required_product_group_counts"].items())),
        checks,
    )

    common_required_values = {
        "custom_label_0": spec["product_group_filter_template"]["custom_label_0"],
        "custom_label_4": spec["product_group_filter_template"]["custom_label_4"],
        "pinterest_en_us_locale": spec["product_group_filter_template"]["locale"],
        "pinterest_en_us_availability": spec["product_group_filter_template"]["availability"],
        "pinterest_en_us_feed_profile_id": spec["catalog"]["allowed_feed_profile_id"],
        "market": "US",
        "review_only_launch_status": "CANDIDATE_ONLY_NOT_LAUNCH_APPROVED",
    }
    for field, expected in common_required_values.items():
        observed = sorted(set(row[field] for row in clean_rows))
        check(observed == [expected], f"clean_scope_{field}", observed, [expected], checks)

    campaign_names = [campaign["name"] for campaign in spec["campaigns"]]
    ad_group_names = [ad_group["name"] for campaign in spec["campaigns"] for ad_group in campaign["ad_groups"]]
    check(len(campaign_names) == 2 and len(set(campaign_names)) == 2, "campaign_name_count_unique", campaign_names, "2 unique", checks)
    check(len(ad_group_names) == 6 and len(set(ad_group_names)) == 6, "ad_group_name_count_unique", ad_group_names, "6 unique", checks)
    check(
        all(campaign["status_required"] == "paused_or_draft" for campaign in spec["campaigns"]),
        "campaign_status_required_paused_or_draft",
        [campaign["status_required"] for campaign in spec["campaigns"]],
        ["paused_or_draft"],
        checks,
    )
    check(
        all(ad_group["status_required"] == "paused_or_draft" for campaign in spec["campaigns"] for ad_group in campaign["ad_groups"]),
        "ad_group_status_required_paused_or_draft",
        [ad_group["status_required"] for campaign in spec["campaigns"] for ad_group in campaign["ad_groups"]],
        ["paused_or_draft"],
        checks,
    )

    summary = {
        "status": "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL",
        "spec": str(SPEC_PATH.relative_to(ROOT)),
        "clean_scope": str(clean_path.relative_to(ROOT)),
        "exclusions": str(exclusions_path.relative_to(ROOT)),
        "checks": checks,
        "writes_made": "local_validation_summary_only",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "summary": str(SUMMARY_PATH), "checks": len(checks)}, indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
