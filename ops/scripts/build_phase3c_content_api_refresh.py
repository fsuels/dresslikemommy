#!/usr/bin/env python3
"""Build a replacement Merchant Center supplemental file after full-upload analysis.

This refresh file:
- excludes known stale Shopify product IDs that Merchant Center reported as unmatched
- emits partial rows when at least one attribute can be set confidently
- keeps ambiguous fields blank instead of withholding the entire row
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_feed_engineering_pilot import (  # noqa: E402
    CANONICAL_BRAND,
    COLOR_MAP,
    ProductRecord,
    ShopifyClient,
    VariantRecord,
    extract_size_value,
    fetch_products,
    infer_age_group,
    infer_color,
    infer_gender,
    merchant_center_offer_id,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-28-phase-3c-refresh")
DEFAULT_STALE_IDS_CSV = Path("ops/feed-engineering/2026-03-28-phase-3c-scaleup/known_stale_shopify_product_ids.csv")

EXPLICIT_PAIR_PATTERN = re.compile(r"(mom|mommy|mother|dad|daddy|father|couple|maternity|breastfeeding|wife|husband)", re.IGNORECASE)
GENERIC_FAMILY_PATTERN = re.compile(r"(family|parents-and-kids|whole-family|unisex)", re.IGNORECASE)
NEUTRAL_APPAREL_PATTERN = re.compile(r"(t-shirt|shirt|sweater|hoodie|cardigan|pullover|knit|tee|jacket)", re.IGNORECASE)
ROLE_SIZE_PATTERN = re.compile(r"(girl|boy|mother|father|mom|dad|women|men|lady|ladies|wife|husband|son|daughter)", re.IGNORECASE)
MULTICOLOR_TITLE_PATTERN = re.compile(r"(rainbow|colorful|ombre|tie-dye|tie dye|gradient|multicolor|multi color|tropical|floral|polka)", re.IGNORECASE)
GENERIC_CHILD_PATTERN = re.compile(r"(baby|child|kid|kids|infant|toddler|\b\d{1,2}\s*(?:m|mo|month|months|t|year|years)\b)", re.IGNORECASE)
CHILD_MALE_PATTERN = re.compile(r"(boy|boys|son|sons|best man)", re.IGNORECASE)
CHILD_FEMALE_PATTERN = re.compile(r"(girl|girls|daughter|daughters|best lady|princess)", re.IGNORECASE)
FEMININE_GARMENT_PATTERN = re.compile(r"(jumpsuit|dress|gown|maxi|maternity|breastfeeding|tankini|bikini|swimsuit|one-piece)", re.IGNORECASE)
PATTERN_COLOR_MAP = {
    "tie-dye": "Tie-Dye",
    "tie dye": "Tie-Dye",
    "floral": "Floral",
    "polka dot": "Polka Dot",
    "polka dots": "Polka Dot",
    "striped": "Striped",
    "stripe": "Striped",
    "leopard": "Leopard",
    "paisley": "Paisley",
}
VARIANT_COLOR_MAP = {
    "multi color": "Multicolor",
    "multi-color": "Multicolor",
    "multicolor": "Multicolor",
    "rainbow color": "Multicolor",
    "photo color": "Multicolor",
    "stripes": "Striped",
    "stripe": "Striped",
    "champagne": "Champagne",
}
STYLE_SEGMENTS = {"pullover", "cardigan", "set", "default title"}


def looks_like_alpha_size(value: str) -> bool:
    return bool(re.fullmatch(r"(xxs|xs|s|m|l|xl|xxl|xxxl|2xl|3xl|4xl|5xl)", value.strip().lower()))


def generic_child_gender(product_text: str, size_value: str) -> str:
    if not GENERIC_CHILD_PATTERN.search(size_value):
        return ""
    has_female_child_signal = CHILD_FEMALE_PATTERN.search(product_text) is not None
    has_male_child_signal = CHILD_MALE_PATTERN.search(product_text) is not None
    if has_female_child_signal and not has_male_child_signal:
        return "female"
    if has_male_child_signal and not has_female_child_signal:
        return "male"
    if has_female_child_signal and has_male_child_signal:
        return "unisex"
    if NEUTRAL_APPAREL_PATTERN.search(product_text) and (GENERIC_FAMILY_PATTERN.search(product_text) or EXPLICIT_PAIR_PATTERN.search(product_text)):
        return "unisex"
    return ""


def infer_age_group_refresh(product: ProductRecord, variant: VariantRecord, size_value: str) -> str:
    inferred = infer_age_group(product, variant, size_value)
    if inferred:
        return inferred

    product_text = f"{product.title} {product.handle.replace('-', ' ')} {' '.join(product.tags)}"
    if looks_like_alpha_size(size_value) and FEMININE_GARMENT_PATTERN.search(product_text) and not GENERIC_CHILD_PATTERN.search(product_text):
        return "adult"
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_stale_product_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["product_id"].strip() for row in csv.DictReader(handle) if row.get("product_id")}


def distinct_color_candidates(product: ProductRecord, variant: VariantRecord) -> set[str]:
    values: list[str] = [product.title, product.handle.replace("-", " "), " ".join(product.tags)]
    for option in product.options:
        values.extend(option.get("values", []))
    for option in variant.selected_options:
        values.append(option["value"])

    matches: set[str] = set()
    for value in values:
        lowered = value.lower()
        for raw, normalized in COLOR_MAP.items():
            if re.search(rf"(?<![a-z]){re.escape(raw)}(?![a-z])", lowered):
                matches.add(normalized)
    return matches


def infer_gender_refresh(product: ProductRecord, variant: VariantRecord, size_value: str) -> str:
    inferred = infer_gender(product, variant)
    if inferred:
        return inferred

    title_handle = f"{product.title} {product.handle.replace('-', ' ')}"
    child_gender = generic_child_gender(title_handle, size_value)
    if child_gender:
        return child_gender

    if looks_like_alpha_size(size_value) and FEMININE_GARMENT_PATTERN.search(title_handle) and not EXPLICIT_PAIR_PATTERN.search(title_handle):
        return "female"

    if not GENERIC_FAMILY_PATTERN.search(title_handle):
        return ""
    if not NEUTRAL_APPAREL_PATTERN.search(title_handle):
        return ""
    if ROLE_SIZE_PATTERN.search(size_value):
        return ""
    return "unisex"


def extract_variant_color_candidate(variant: VariantRecord) -> str:
    segments = [segment.strip() for segment in variant.title.split("/") if segment.strip()]
    for segment in reversed(segments):
        lowered = segment.lower()
        if lowered in STYLE_SEGMENTS:
            continue
        if lowered in VARIANT_COLOR_MAP:
            return VARIANT_COLOR_MAP[lowered]
        if lowered == "mermaid":
            return "Multicolor"
        if single_color := single_segment_color(segment):
            return single_color
    return ""


def single_segment_color(value: str) -> str:
    lowered = value.lower().strip()
    if not lowered or lowered in STYLE_SEGMENTS:
        return ""
    for raw, normalized in COLOR_MAP.items():
        if re.search(rf"(?<![a-z]){re.escape(raw)}(?![a-z])", lowered):
            return normalized
    return ""


def infer_color_refresh(product: ProductRecord, variant: VariantRecord) -> str:
    inferred = infer_color(product, variant)
    if inferred:
        return inferred

    variant_color = extract_variant_color_candidate(variant)
    if variant_color:
        return variant_color

    combined_text = " ".join([product.title, product.handle.replace("-", " "), " ".join(product.tags)]).lower()
    for raw, normalized in PATTERN_COLOR_MAP.items():
        if raw in combined_text:
            return normalized

    option_names = " ".join(option["name"] for option in variant.selected_options).lower()
    style_like = any(token in option_names for token in ("style", "pattern", "design"))
    color_candidates = distinct_color_candidates(product, variant)
    has_multicolor_signal = (
        "multi color" in combined_text
        or "multicolor" in combined_text
        or MULTICOLOR_TITLE_PATTERN.search(combined_text) is not None
        or len(color_candidates) > 1
    )
    if style_like and has_multicolor_signal:
        return "Multicolor"
    if has_multicolor_signal and "color" not in option_names:
        return "Multicolor"
    return ""


def build_refresh_rows(products: list[ProductRecord], stale_product_ids: set[str]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    refresh_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    metrics: Counter[str] = Counter()

    for product in products:
        if product.status != "ACTIVE":
            continue
        if not product.google_published:
            continue
        if product.product_id in stale_product_ids:
            metrics["excluded_stale_products"] += 1
            metrics["excluded_stale_variants"] += len(product.variants)
            continue

        metrics["eligible_products"] += 1
        for variant in product.variants:
            metrics["eligible_variants"] += 1
            size_value, _size_required = extract_size_value(product, variant)
            brand_value = CANONICAL_BRAND if product.house_brand_confident else ""
            age_group = infer_age_group_refresh(product, variant, size_value)
            gender = infer_gender_refresh(product, variant, size_value)
            color = infer_color_refresh(product, variant)

            row = {
                "id": merchant_center_offer_id(product, variant),
                "brand": brand_value,
                "age_group": age_group,
                "gender": gender,
                "color": color,
                "size": size_value,
                "manual_review_reason": "",
            }

            populated_fields = [field for field in ("brand", "age_group", "gender", "color", "size") if row[field]]
            if not populated_fields:
                metrics["dropped_no_confident_fields"] += 1
                review_rows.append(
                    {
                        "product_id": product.product_id,
                        "variant_id": variant.variant_id,
                        "id": row["id"],
                        "handle": product.handle,
                        "title": product.title,
                        "issue": "no_confident_fields",
                        "details": "No attribute could be set confidently for this row.",
                    }
                )
                continue

            metrics["refresh_rows"] += 1
            for field in populated_fields:
                metrics[f"rows_with_{field}"] += 1
            if not color:
                metrics["rows_with_blank_color"] += 1
            if not gender:
                metrics["rows_with_blank_gender"] += 1
            if not age_group:
                metrics["rows_with_blank_age_group"] += 1
            if not brand_value:
                metrics["rows_with_blank_brand"] += 1
            refresh_rows.append(row)

            if any(not row[field] for field in ("brand", "age_group", "gender", "color")):
                review_rows.append(
                    {
                        "product_id": product.product_id,
                        "variant_id": variant.variant_id,
                        "id": row["id"],
                        "handle": product.handle,
                        "title": product.title,
                        "issue": "; ".join(
                            field for field in ("brand", "age_group", "gender", "color") if not row[field]
                        ),
                        "details": "Partial refresh row generated; blank fields remain intentionally unresolved.",
                    }
                )

    return refresh_rows, review_rows, dict(metrics)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Merchant Center refresh supplemental file after unmatched-ID analysis.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory.")
    parser.add_argument("--stale-product-ids", default=str(DEFAULT_STALE_IDS_CSV), help="CSV file of known stale Shopify product IDs.")
    args = parser.parse_args()

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    stale_ids_path = Path(args.stale_product_ids)
    output_dir = Path(args.output_dir)

    client = ShopifyClient(store_domain, access_token)
    products = fetch_products(client)
    stale_product_ids = load_stale_product_ids(stale_ids_path)
    refresh_rows, review_rows, metrics = build_refresh_rows(products, stale_product_ids)

    write_csv(
        output_dir / "supplemental_feed_refresh.csv",
        refresh_rows,
        ["id", "brand", "age_group", "gender", "color", "size", "manual_review_reason"],
    )
    write_csv(
        output_dir / "refresh_partial_review_queue.csv",
        review_rows,
        ["product_id", "variant_id", "id", "handle", "title", "issue", "details"],
    )

    summary = {
        "artifact_dir": str(output_dir),
        "stale_product_ids_csv": str(stale_ids_path),
        "known_stale_product_ids": len(stale_product_ids),
        "refresh_row_count": len(refresh_rows),
        "partial_review_row_count": len(review_rows),
        "metrics": metrics,
        "merchant_center_primary_offer_id_pattern": "shopify_US_{product_id}_{variant_id}",
        "notes": [
            "This file is intended to replace the current supplemental source content, not append to it.",
            "Known stale Shopify product IDs from the Merchant Center unmatched report are excluded.",
            "Rows are included when any attribute can be set confidently; blank fields remain intentionally blank.",
        ],
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
