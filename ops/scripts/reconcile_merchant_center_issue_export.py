#!/usr/bin/env python3
"""Reconcile a Merchant Center diagnostics export against live Shopify data."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_feed_engineering_pilot import (  # noqa: E402
    ProductRecord,
    ShopifyClient,
    VariantRecord,
    fetch_products,
    merchant_center_offer_id,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3q-mc-issue-reconciliation")
SHOPIFY_OFFER_PATTERN = re.compile(r"^shopify_([A-Z]{2})_(\d+)_(\d+)$")

OFFER_ID_COLUMNS = (
    "offer id",
    "offer_id",
    "id",
    "item id",
    "product id",
    "product_id",
)
TITLE_COLUMNS = (
    "title",
    "product title",
    "item title",
    "product_title",
)
ISSUE_COLUMNS = (
    "issue",
    "issue title",
    "issue_title",
    "problem",
    "status details",
)
URL_COLUMNS = (
    "landing page",
    "landing page url",
    "page url",
    "product page",
    "link",
    "url",
)
SOURCE_COLUMNS = (
    "source",
    "data source",
    "feed",
    "channel",
)


@dataclass
class IndexedVariant:
    offer_id: str
    product: ProductRecord
    variant: VariantRecord


def clean(value: Any) -> str:
    return str(value or "").strip()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", clean(value)).lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", required=True, help="Merchant Center issue export CSV.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for reconciliation artifacts.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    return parser.parse_args()


def find_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str:
    normalized = {normalize_text(name): name for name in fieldnames}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return ""


def build_indexes(products: list[ProductRecord]) -> tuple[dict[str, IndexedVariant], dict[str, IndexedVariant], dict[str, ProductRecord], dict[str, ProductRecord]]:
    active_google_offer_index: dict[str, IndexedVariant] = {}
    any_offer_index: dict[str, IndexedVariant] = {}
    url_index: dict[str, ProductRecord] = {}
    title_index: dict[str, ProductRecord] = {}

    for product in products:
        if product.online_store_url:
            url_index[normalize_text(product.online_store_url)] = product
        title_key = normalize_text(product.title)
        if title_key and title_key not in title_index:
            title_index[title_key] = product

        for variant in product.variants:
            offer_id = merchant_center_offer_id(product, variant)
            indexed = IndexedVariant(offer_id=offer_id, product=product, variant=variant)
            any_offer_index[offer_id] = indexed
            if product.status == "ACTIVE" and product.google_published:
                active_google_offer_index[offer_id] = indexed

    return active_google_offer_index, any_offer_index, url_index, title_index


def classify_row(
    row: dict[str, str],
    *,
    active_google_offer_index: dict[str, IndexedVariant],
    any_offer_index: dict[str, IndexedVariant],
    url_index: dict[str, ProductRecord],
    title_index: dict[str, ProductRecord],
    offer_id_key: str,
    title_key: str,
    url_key: str,
) -> dict[str, str]:
    offer_id = clean(row.get(offer_id_key, ""))
    title = clean(row.get(title_key, ""))
    url = clean(row.get(url_key, ""))

    classification = "unmatched"
    reason = ""
    matched_product = None
    matched_variant = None

    if offer_id:
        if offer_id in active_google_offer_index:
            match = active_google_offer_index[offer_id]
            classification = "live_google_published_shopify_offer"
            reason = "Offer ID matches a current active Google-published Shopify variant."
            matched_product = match.product
            matched_variant = match.variant
        elif offer_id in any_offer_index:
            match = any_offer_index[offer_id]
            classification = "shopify_offer_not_currently_google_published"
            reason = "Offer ID matches Shopify, but the product is not currently active and Google-published."
            matched_product = match.product
            matched_variant = match.variant
        elif SHOPIFY_OFFER_PATTERN.match(offer_id):
            classification = "shopify_pattern_offer_not_found"
            reason = "Offer ID uses the Shopify Content API pattern but does not match any current Shopify variant."
        elif offer_id.isdigit():
            classification = "opaque_non_shopify_offer_id"
            reason = "Offer ID is opaque/numeric and does not use the current Shopify Content API join pattern."
        else:
            classification = "unknown_offer_id_format"
            reason = "Offer ID does not match the known Shopify Content API pattern."

    if matched_product is None and url:
        url_match = url_index.get(normalize_text(url))
        if url_match:
            matched_product = url_match
            if classification == "opaque_non_shopify_offer_id":
                classification = "opaque_offer_matches_live_product_by_url"
                reason = "Opaque offer ID matched a live Shopify product by URL."
            elif classification == "unmatched":
                classification = "matched_live_product_by_url"
                reason = "Row matched a live Shopify product by URL."

    if matched_product is None and title:
        title_match = title_index.get(normalize_text(title))
        if title_match:
            matched_product = title_match
            if classification == "opaque_non_shopify_offer_id":
                classification = "opaque_offer_matches_live_product_by_title"
                reason = "Opaque offer ID matched a live Shopify product by exact title."
            elif classification == "unmatched":
                classification = "matched_live_product_by_title"
                reason = "Row matched a live Shopify product by exact title."

    return {
        "classification": classification,
        "classification_reason": reason,
        "matched_product_id": clean(getattr(matched_product, "product_id", "")),
        "matched_handle": clean(getattr(matched_product, "handle", "")),
        "matched_title": clean(getattr(matched_product, "title", "")),
        "matched_status": clean(getattr(matched_product, "status", "")),
        "matched_google_published": "true" if getattr(matched_product, "google_published", False) else "false",
        "matched_online_store_url": clean(getattr(matched_product, "online_store_url", "")),
        "matched_variant_id": clean(getattr(matched_variant, "variant_id", "")),
        "matched_variant_title": clean(getattr(matched_variant, "title", "")),
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    products = fetch_products(client)
    active_google_offer_index, any_offer_index, url_index, title_index = build_indexes(products)

    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if not fieldnames:
            raise RuntimeError(f"No headers found in {input_csv}.")

        offer_id_key = find_column(fieldnames, OFFER_ID_COLUMNS)
        title_key = find_column(fieldnames, TITLE_COLUMNS)
        issue_key = find_column(fieldnames, ISSUE_COLUMNS)
        url_key = find_column(fieldnames, URL_COLUMNS)
        source_key = find_column(fieldnames, SOURCE_COLUMNS)
        if not offer_id_key and not title_key and not url_key:
            raise RuntimeError("Could not identify any offer/title/url column in the Merchant Center export.")

        reconciled_rows: list[dict[str, str]] = []
        classification_counts: dict[str, int] = {}

        for row in reader:
            extras = classify_row(
                row,
                active_google_offer_index=active_google_offer_index,
                any_offer_index=any_offer_index,
                url_index=url_index,
                title_index=title_index,
                offer_id_key=offer_id_key,
                title_key=title_key,
                url_key=url_key,
            )
            merged = dict(row)
            merged.update(
                {
                    "normalized_offer_id": clean(row.get(offer_id_key, "")) if offer_id_key else "",
                    "normalized_title": clean(row.get(title_key, "")) if title_key else "",
                    "normalized_issue": clean(row.get(issue_key, "")) if issue_key else "",
                    "normalized_url": clean(row.get(url_key, "")) if url_key else "",
                    "normalized_source": clean(row.get(source_key, "")) if source_key else "",
                    **extras,
                }
            )
            reconciled_rows.append(merged)
            classification = extras["classification"]
            classification_counts[classification] = classification_counts.get(classification, 0) + 1

    output_fieldnames = list(reconciled_rows[0].keys()) if reconciled_rows else (
        fieldnames
        + [
            "normalized_offer_id",
            "normalized_title",
            "normalized_issue",
            "normalized_url",
            "normalized_source",
            "classification",
            "classification_reason",
            "matched_product_id",
            "matched_handle",
            "matched_title",
            "matched_status",
            "matched_google_published",
            "matched_online_store_url",
            "matched_variant_id",
            "matched_variant_title",
        ]
    )

    write_csv(output_dir / "merchant_center_issue_reconciliation.csv", reconciled_rows, output_fieldnames)

    summary = {
        "input_csv": str(input_csv),
        "output_dir": str(output_dir),
        "rows_scanned": len(reconciled_rows),
        "offer_id_column": offer_id_key,
        "title_column": title_key,
        "issue_column": issue_key,
        "url_column": url_key,
        "source_column": source_key,
        "classification_counts": classification_counts,
        "live_active_google_offer_count": len(active_google_offer_index),
        "total_shopify_offer_count": len(any_offer_index),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
