#!/usr/bin/env python3
"""Build Phase 3C scale-up artifacts after pilot validation."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_feed_engineering_pilot import (  # noqa: E402
    CANONICAL_BRAND,
    ProductRecord,
    ShopifyClient,
    VariantRecord,
    build_brand_cleanup,
    extract_size_value,
    fetch_products,
    infer_age_group,
    infer_color,
    infer_gender,
    merchant_center_offer_id,
    product_priority,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-28-phase-3c-scaleup")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def variant_feed_row(product: ProductRecord, variant: VariantRecord) -> tuple[dict[str, str], list[str]]:
    size_value, size_required = extract_size_value(product, variant)
    brand_value = CANONICAL_BRAND if product.house_brand_confident else ""
    age_group = infer_age_group(product, variant, size_value)
    gender = infer_gender(product, variant)
    color = infer_color(product, variant)

    reasons: list[str] = []
    if not brand_value:
        reasons.append("brand_uncertain")
    if not age_group:
        reasons.append("age_group_ambiguous")
    if not gender:
        reasons.append("gender_ambiguous")
    if not color:
        reasons.append("color_ambiguous")
    if size_required and not size_value:
        reasons.append("size_missing")

    row = {
        "id": merchant_center_offer_id(product, variant),
        "brand": brand_value,
        "age_group": age_group or "",
        "gender": gender or "",
        "color": color or "",
        "size": size_value,
        "manual_review_reason": "",
    }
    return row, reasons


def build_full_feed(products: list[ProductRecord]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    feed_rows: list[dict[str, str]] = []
    manual_rows: list[dict[str, str]] = []
    counters: Counter[str] = Counter()

    eligible_products = [
        product
        for product in products
        if product.status == "ACTIVE" and product.google_published
    ]

    for product in sorted(eligible_products, key=product_priority):
        counters["eligible_products"] += 1
        for variant in product.variants:
            counters["variants_seen"] += 1
            row, reasons = variant_feed_row(product, variant)
            if reasons:
                counters["manual_rows"] += 1
                for reason in reasons:
                    counters[f"manual_{reason}"] += 1
                manual_rows.append(
                    {
                        "queue_type": "supplemental_feed_full",
                        "product_id": product.product_id,
                        "variant_id": variant.variant_id,
                        "id": row["id"],
                        "handle": product.handle,
                        "title": product.title,
                        "current_vendor": product.vendor,
                        "status": product.status,
                        "google_youtube_published": "true",
                        "issue": "; ".join(reasons),
                        "details": "Full-scale supplemental row withheld because one or more fields could not be inferred confidently from current live data.",
                        "candidate_brand": row["brand"],
                        "candidate_age_group": row["age_group"],
                        "candidate_gender": row["gender"],
                        "candidate_color": row["color"],
                        "candidate_size": row["size"],
                    }
                )
                continue

            feed_rows.append(row)
            counters["full_rows"] += 1

    return feed_rows, manual_rows, dict(counters)


def build_vendor_artifacts(products: list[ProductRecord]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    cleanup_rows, manual_rows = build_brand_cleanup(products)
    product_map = {product.product_id: product for product in products}

    update_rows: list[dict[str, str]] = []
    rollback_rows: list[dict[str, str]] = []
    for row in cleanup_rows:
        product = product_map[row["product_id"]]
        update_rows.append(
            {
                "product_id": product.product_id,
                "product_gid": product.product_gid,
                "handle": product.handle,
                "status": product.status,
                "google_youtube_published": "true" if product.google_published else "false",
                "current_vendor": row["current_vendor"],
                "new_vendor": row["proposed_vendor"],
                "reason": row["reason"],
            }
        )
        rollback_rows.append(
            {
                "product_id": product.product_id,
                "product_gid": product.product_gid,
                "handle": product.handle,
                "status": product.status,
                "google_youtube_published": "true" if product.google_published else "false",
                "rollback_vendor": row["current_vendor"],
                "updated_vendor": row["proposed_vendor"],
            }
        )

    update_rows.sort(
        key=lambda row: (
            0 if row["status"] == "ACTIVE" else 1,
            0 if row["google_youtube_published"] == "true" else 1,
            row["handle"],
        )
    )
    rollback_rows.sort(
        key=lambda row: (
            0 if row["status"] == "ACTIVE" else 1,
            0 if row["google_youtube_published"] == "true" else 1,
            row["handle"],
        )
    )

    sample_rows = update_rows[:20]
    return update_rows, rollback_rows, sample_rows, manual_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase 3C full supplemental feed + vendor-update artifacts.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    args = parser.parse_args()

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    output_dir = Path(args.output_dir)

    client = ShopifyClient(store_domain, access_token)
    products = fetch_products(client)

    full_feed_rows, full_feed_manual_rows, feed_metrics = build_full_feed(products)
    vendor_update_rows, vendor_rollback_rows, vendor_sample_rows, vendor_manual_rows = build_vendor_artifacts(products)

    write_csv(
        output_dir / "supplemental_feed_full.csv",
        full_feed_rows,
        ["id", "brand", "age_group", "gender", "color", "size", "manual_review_reason"],
    )
    write_csv(
        output_dir / "manual_review_queue_full.csv",
        full_feed_manual_rows,
        [
            "queue_type",
            "product_id",
            "variant_id",
            "id",
            "handle",
            "title",
            "current_vendor",
            "status",
            "google_youtube_published",
            "issue",
            "details",
            "candidate_brand",
            "candidate_age_group",
            "candidate_gender",
            "candidate_color",
            "candidate_size",
        ],
    )
    write_csv(
        output_dir / "shopify_vendor_update.csv",
        vendor_update_rows,
        [
            "product_id",
            "product_gid",
            "handle",
            "status",
            "google_youtube_published",
            "current_vendor",
            "new_vendor",
            "reason",
        ],
    )
    write_csv(
        output_dir / "shopify_vendor_update_rollback.csv",
        vendor_rollback_rows,
        [
            "product_id",
            "product_gid",
            "handle",
            "status",
            "google_youtube_published",
            "rollback_vendor",
            "updated_vendor",
        ],
    )
    write_csv(
        output_dir / "shopify_vendor_update_sample.csv",
        vendor_sample_rows,
        [
            "product_id",
            "product_gid",
            "handle",
            "status",
            "google_youtube_published",
            "current_vendor",
            "new_vendor",
            "reason",
        ],
    )
    write_csv(
        output_dir / "shopify_vendor_manual_review.csv",
        vendor_manual_rows,
        [
            "queue_type",
            "product_id",
            "variant_id",
            "id",
            "handle",
            "title",
            "current_vendor",
            "status",
            "google_youtube_published",
            "issue",
            "details",
            "candidate_brand",
            "candidate_age_group",
            "candidate_gender",
            "candidate_color",
            "candidate_size",
        ],
    )

    summary = {
        "artifact_dir": str(output_dir),
        "catalog_products": len(products),
        "active_products": sum(1 for product in products if product.status == "ACTIVE"),
        "archived_products": sum(1 for product in products if product.status == "ARCHIVED"),
        "active_google_published_products": sum(
            1 for product in products if product.status == "ACTIVE" and product.google_published
        ),
        "full_feed_rows": len(full_feed_rows),
        "full_feed_manual_rows": len(full_feed_manual_rows),
        "vendor_update_rows": len(vendor_update_rows),
        "vendor_manual_review_rows": len(vendor_manual_rows),
        "vendor_sample_rows": len(vendor_sample_rows),
        "feed_metrics": feed_metrics,
        "manual_review_issue_counts": dict(Counter(row["issue"] for row in full_feed_manual_rows)),
        "merchant_center_primary_offer_id_pattern": "shopify_US_{product_id}_{variant_id}",
        "notes": [
            "supplemental_feed_full.csv is a fresh scale-up file built after the pilot upload succeeded.",
            "shopify_vendor_update.csv is a dry-run artifact only; no vendor updates were executed.",
            "Vendor rows in shopify_vendor_manual_review.csv remain intentionally excluded from automation.",
        ],
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
