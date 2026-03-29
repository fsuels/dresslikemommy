#!/usr/bin/env python3
"""Export a revenue-ranked size label inventory from the apparel audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.fill_shopify_apparel_attributes import (  # noqa: E402
    ShopifyClient,
    build_metaobject_index,
    canonicalize_size_token,
    clean,
    map_single_size_value,
    normalize_text,
    split_pipe,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_INPUT_CSV = Path("ops/feed-engineering/2026-03-29-phase-3e-apparel-attribute-audit/apparel_attribute_audit_all.csv")
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3h-size-label-inventory")
TOP_LIMIT = 20


@dataclass
class ProductSizeRow:
    product_id: str
    handle: str
    title: str
    discounted_revenue: float
    shopify_size_present: bool
    missing_attributes: list[str]
    candidate_size: list[str]
    candidate_size_source: str


@dataclass
class SizeLabelStats:
    raw_label: str
    canonical_token: str
    mapping_status: str = ""
    recommended_shopify_label: str = ""
    recommended_shopify_handle: str = ""
    mapped_via: str = ""
    products_with_label: set[str] = field(default_factory=set)
    missing_size_products_with_label: set[str] = field(default_factory=set)
    discounted_revenue_exposure: float = 0.0
    missing_size_revenue_exposure: float = 0.0
    source_examples: set[str] = field(default_factory=set)
    product_examples: list[tuple[float, str, str]] = field(default_factory=list)

    def add_row(self, row: ProductSizeRow) -> None:
        self.products_with_label.add(row.product_id)
        self.discounted_revenue_exposure += row.discounted_revenue
        if "size" in row.missing_attributes or not row.shopify_size_present:
            self.missing_size_products_with_label.add(row.product_id)
            self.missing_size_revenue_exposure += row.discounted_revenue
        if row.candidate_size_source:
            self.source_examples.add(row.candidate_size_source)
        self.product_examples.append((row.discounted_revenue, row.handle, row.title))

    def top_examples(self, limit: int = 5) -> str:
        ranked = sorted(self.product_examples, key=lambda item: (-item[0], item[1]))
        formatted = [f"{handle} (${revenue:.2f})" for revenue, handle, _title in ranked[:limit]]
        return " | ".join(formatted)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_rows(path: Path) -> list[ProductSizeRow]:
    rows: list[ProductSizeRow] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                ProductSizeRow(
                    product_id=clean(row["product_id"]),
                    handle=clean(row["handle"]),
                    title=clean(row["title"]),
                    discounted_revenue=float(row["discounted_revenue"] or 0.0),
                    shopify_size_present=clean(row["shopify_size_present"]).lower() == "true",
                    missing_attributes=split_pipe(row["missing_attributes"]),
                    candidate_size=split_pipe(row["candidate_size"]),
                    candidate_size_source=clean(row["candidate_size_source"]),
                )
            )
    return rows


def canonical_size_label_candidate(token: str) -> str:
    compact = normalize_text(token)
    if not compact:
        return ""
    if re.fullmatch(r"(xs|s|m|l|xl|2xl|3xl|4xl|5xl)", compact):
        return compact.upper().replace("2XL", "2XL").replace("3XL", "3XL").replace("4XL", "4XL").replace("5XL", "5XL")
    teen_range = re.fullmatch(r"(\d{1,2})\s*-\s*(\d{1,2})t", compact)
    if teen_range:
        return f"{teen_range.group(1)}-{teen_range.group(2)} years"
    toddler_single = re.fullmatch(r"(\d{1,2})t", compact)
    if toddler_single:
        value = int(toddler_single.group(1))
        if value in {2, 3, 4}:
            return f"{value}-{value + 1} years"
        if value in {6, 8, 10}:
            return str(value)
    if re.fullmatch(r"\d{1,2}\s*-\s*\d{1,2}\s*months", compact):
        digits = re.findall(r"\d{1,2}", compact)
        return f"{digits[0]}-{digits[1]} months"
    if re.fullmatch(r"\d{1,2}\s*-\s*\d{1,2}\s*years", compact):
        digits = re.findall(r"\d{1,2}", compact)
        return f"{digits[0]}-{digits[1]} years"
    if re.fullmatch(r"\d{1,2}\s*years", compact):
        digits = re.findall(r"\d{1,2}", compact)
        return digits[0]
    if re.fullmatch(r"\d{1,2}", compact):
        return compact
    return ""


def classify_label(
    raw_label: str,
    canonical_token: str,
    size_metaobject_index: dict[str, object],
    size_refs: list[object],
) -> tuple[str, str, str, str]:
    mapped_label, mapped_ref, problem = map_single_size_value(raw_label, size_refs)
    if mapped_ref:
        return "maps_to_existing_metaobject", mapped_label or clean(mapped_ref.display_name), clean(mapped_ref.handle), "current_mapping_rule"

    if canonical_token:
        direct_ref = size_metaobject_index.get(normalize_text(canonical_token)) or size_metaobject_index.get(
            normalize_text(canonical_token).replace(" ", "-")
        )
        if direct_ref:
            return (
                "canonical_token_matches_existing_metaobject",
                clean(direct_ref.display_name),
                clean(direct_ref.handle),
                "canonical_token_lookup",
            )

    canonical_candidate = canonical_size_label_candidate(canonical_token)
    if canonical_candidate:
        return (
            "needs_canonical_metaobject_or_rule",
            canonical_candidate,
            normalize_text(canonical_candidate).replace(" ", "-"),
            clean(problem) or "canonical_label_without_metaobject",
        )

    return "manual_review", "", "", clean(problem)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    rows = load_rows(args.input_csv)

    access_token = load_access_token()
    store_domain = resolve_store_domain()
    client = ShopifyClient(store_domain=store_domain, access_token=access_token)
    size_refs = client.fetch_metaobjects("shopify--size")
    size_index = build_metaobject_index(size_refs)

    total_missing_size_revenue = sum(row.discounted_revenue for row in rows if "size" in row.missing_attributes or not row.shopify_size_present)
    total_products_with_size_candidates = sum(1 for row in rows if row.candidate_size)
    total_products_missing_size = sum(1 for row in rows if "size" in row.missing_attributes or not row.shopify_size_present)

    stats_by_label: dict[str, SizeLabelStats] = {}
    for row in rows:
        for raw_label in row.candidate_size:
            canonical_token = canonicalize_size_token(raw_label)
            key = normalize_text(raw_label)
            stats = stats_by_label.get(key)
            if not stats:
                stats = SizeLabelStats(raw_label=clean(raw_label), canonical_token=clean(canonical_token))
                mapping_status, recommended_label, recommended_handle, mapped_via = classify_label(
                    stats.raw_label,
                    stats.canonical_token,
                    size_index,
                    size_refs,
                )
                stats.mapping_status = mapping_status
                stats.recommended_shopify_label = recommended_label
                stats.recommended_shopify_handle = recommended_handle
                stats.mapped_via = mapped_via
                stats_by_label[key] = stats
            stats.add_row(row)

    fieldnames = [
        "raw_size_label",
        "canonical_size_token",
        "mapping_status",
        "recommended_shopify_label",
        "recommended_shopify_handle",
        "mapped_via",
        "products_with_label",
        "missing_size_products_with_label",
        "discounted_revenue_exposure",
        "missing_size_revenue_exposure",
        "missing_size_revenue_share",
        "candidate_source_examples",
        "top_product_examples",
    ]

    inventory_rows: list[dict[str, str]] = []
    for stats in sorted(
        stats_by_label.values(),
        key=lambda item: (-item.missing_size_revenue_exposure, -item.discounted_revenue_exposure, normalize_text(item.raw_label)),
    ):
        share = 0.0
        if total_missing_size_revenue:
            share = stats.missing_size_revenue_exposure / total_missing_size_revenue
        inventory_rows.append(
            {
                "raw_size_label": stats.raw_label,
                "canonical_size_token": stats.canonical_token,
                "mapping_status": stats.mapping_status,
                "recommended_shopify_label": stats.recommended_shopify_label,
                "recommended_shopify_handle": stats.recommended_shopify_handle,
                "mapped_via": stats.mapped_via,
                "products_with_label": str(len(stats.products_with_label)),
                "missing_size_products_with_label": str(len(stats.missing_size_products_with_label)),
                "discounted_revenue_exposure": f"{stats.discounted_revenue_exposure:.2f}",
                "missing_size_revenue_exposure": f"{stats.missing_size_revenue_exposure:.2f}",
                "missing_size_revenue_share": f"{share:.6f}",
                "candidate_source_examples": " | ".join(sorted(stats.source_examples)),
                "top_product_examples": stats.top_examples(),
            }
        )

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory_csv = output_dir / "size_label_inventory.csv"
    top_inventory_csv = output_dir / "size_label_inventory_top20_by_missing_size_revenue.csv"
    metaobject_csv = output_dir / "shopify_size_metaobjects.csv"
    summary_json = output_dir / "summary.json"

    write_csv(inventory_csv, inventory_rows, fieldnames)
    write_csv(top_inventory_csv, inventory_rows[:TOP_LIMIT], fieldnames)

    metaobject_rows = [
        {"display_name": clean(ref.display_name), "handle": clean(ref.handle), "id": clean(ref.id)} for ref in sorted(size_refs, key=lambda item: normalize_text(item.display_name))
    ]
    write_csv(metaobject_csv, metaobject_rows, ["display_name", "handle", "id"])

    status_counter = Counter(row["mapping_status"] for row in inventory_rows)
    summary = {
        "input_csv": str(args.input_csv),
        "output_dir": str(output_dir),
        "products_scanned": len(rows),
        "products_with_size_candidates": total_products_with_size_candidates,
        "products_missing_size": total_products_missing_size,
        "total_missing_size_revenue_exposure": round(total_missing_size_revenue, 2),
        "unique_size_labels": len(inventory_rows),
        "mapping_status_counts": dict(status_counter),
        "top_mapping_gaps_by_missing_size_revenue": [
            {
                "raw_size_label": row["raw_size_label"],
                "canonical_size_token": row["canonical_size_token"],
                "mapping_status": row["mapping_status"],
                "recommended_shopify_label": row["recommended_shopify_label"],
                "missing_size_revenue_exposure": float(row["missing_size_revenue_exposure"]),
            }
            for row in inventory_rows
            if row["mapping_status"] != "maps_to_existing_metaobject"
        ][:TOP_LIMIT],
        "top_existing_mappable_labels_by_missing_size_revenue": [
            {
                "raw_size_label": row["raw_size_label"],
                "recommended_shopify_label": row["recommended_shopify_label"],
                "missing_size_revenue_exposure": float(row["missing_size_revenue_exposure"]),
            }
            for row in inventory_rows
            if row["mapping_status"] in {"maps_to_existing_metaobject", "canonical_token_matches_existing_metaobject"}
        ][:TOP_LIMIT],
        "shopify_size_metaobjects": len(size_refs),
    }
    summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
