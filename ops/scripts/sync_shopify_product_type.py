#!/usr/bin/env python3
"""Audit and sync Shopify productType values from existing product taxonomy signals.

Default mode is dry-run and writes audit artifacts only.

Live updates are intentionally limited to products whose Shopify `productType`
is blank but whose `custom.type` metafield is already populated, which is the
highest-confidence source available in this store today.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
PRODUCT_PAGE_SIZE = 50
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3d-product-type-sync")

PRODUCTS_QUERY = """
query Products($first: Int!, $after: String, $query: String) {
  products(
    first: $first
    after: $after
    query: $query
    sortKey: INVENTORY_TOTAL
    reverse: true
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      legacyResourceId
      handle
      title
      vendor
      status
      totalInventory
      productType
      onlineStoreUrl
      tags
      collections(first: 15) {
        nodes {
          handle
          title
        }
      }
      typeField: metafield(namespace: "custom", key: "type") {
        value
      }
      styleField: metafield(namespace: "custom", key: "style") {
        value
      }
      patternField: metafield(namespace: "custom", key: "pattern") {
        value
      }
    }
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      productType
    }
    userErrors {
      field
      message
    }
  }
}
"""

COLLECTION_TYPE_RULES = [
    ("pajama", "Pajamas"),
    ("loungewear", "Pajamas"),
    ("swimsuit", "Swimwear"),
    ("swimwear", "Swimwear"),
    ("trunks", "Swimwear"),
    ("dress", "Dresses"),
    ("maxi-dresses", "Dresses"),
    ("midi-dresses", "Dresses"),
    ("tops", "Tops"),
    ("shirts", "Tops"),
    ("tshirts", "Tops"),
    ("t-shirts", "Tops"),
    ("sweater", "Sweaters"),
    ("cardigan", "Sweaters"),
    ("hoodie", "Sweaters"),
    ("set", "Sets"),
    ("family-sets", "Sets"),
    ("jumpsuit", "Jumpsuits"),
    ("romper", "Jumpsuits"),
    ("coat", "Coats"),
    ("outerwear", "Coats"),
]

TEXT_TYPE_RULES = [
    ("pajama", "Pajamas"),
    ("sleepwear", "Pajamas"),
    ("nightgown", "Pajamas"),
    ("loungewear", "Pajamas"),
    ("swim trunk", "Swimwear"),
    ("swimwear", "Swimwear"),
    ("swimsuit", "Swimwear"),
    ("bathing suit", "Swimwear"),
    ("tankini", "Swimwear"),
    ("bikini", "Swimwear"),
    ("one-piece", "Swimwear"),
    ("one piece", "Swimwear"),
    ("dress", "Dresses"),
    ("gown", "Dresses"),
    ("sundress", "Dresses"),
    ("jumpsuit", "Jumpsuits"),
    ("romper", "Jumpsuits"),
    ("shirt", "Tops"),
    ("t-shirt", "Tops"),
    ("t shirt", "Tops"),
    ("tee", "Tops"),
    ("top", "Tops"),
    ("blouse", "Tops"),
    ("sweater", "Sweaters"),
    ("sweatshirt", "Sweaters"),
    ("cardigan", "Sweaters"),
    ("hoodie", "Sweaters"),
    ("pullover", "Sweaters"),
    ("set", "Sets"),
    ("outfit", "Sets"),
    ("matching set", "Sets"),
    ("jacket", "Coats"),
    ("coat", "Coats"),
    ("parka", "Coats"),
]


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalized(value: Any) -> str:
    return clean(value).lower()


@dataclass
class ProductTypeRecord:
    product_id: str
    product_gid: str
    handle: str
    title: str
    vendor: str
    status: str
    total_inventory: int
    product_type: str
    custom_type: str
    custom_style: str
    custom_pattern: str
    online_store_url: str
    tags: list[str]
    collection_handles: list[str]
    collection_titles: list[str]


@dataclass
class PlannedUpdate:
    record: ProductTypeRecord
    target_type: str
    confidence: str
    source: str


@dataclass
class MismatchDecision:
    record: ProductTypeRecord
    target_type: str
    confidence: str
    source: str
    review_reason: str
    disposition: str


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.store_domain = store_domain
        self.access_token = access_token
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        req = request.Request(
            self.endpoint,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            },
        )
        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc

        if body.get("errors"):
            raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
        return body["data"]

    def iter_active_products(self) -> list[ProductTypeRecord]:
        output: list[ProductTypeRecord] = []
        after: str | None = None
        while True:
            data = self.graphql(
                PRODUCTS_QUERY,
                {"first": PRODUCT_PAGE_SIZE, "after": after, "query": "status:active"},
            )["products"]
            for node in data["nodes"]:
                output.append(
                    ProductTypeRecord(
                        product_id=clean(node.get("legacyResourceId")),
                        product_gid=clean(node.get("id")),
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        vendor=clean(node.get("vendor")),
                        status=clean(node.get("status")),
                        total_inventory=int(node.get("totalInventory") or 0),
                        product_type=clean(node.get("productType")),
                        custom_type=clean((node.get("typeField") or {}).get("value")),
                        custom_style=clean((node.get("styleField") or {}).get("value")),
                        custom_pattern=clean((node.get("patternField") or {}).get("value")),
                        online_store_url=clean(node.get("onlineStoreUrl")),
                        tags=[clean(tag) for tag in node.get("tags") or [] if clean(tag)],
                        collection_handles=[
                            clean(item.get("handle"))
                            for item in (node.get("collections") or {}).get("nodes") or []
                            if clean(item.get("handle"))
                        ],
                        collection_titles=[
                            clean(item.get("title"))
                            for item in (node.get("collections") or {}).get("nodes") or []
                            if clean(item.get("title"))
                        ],
                    )
                )
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return output

    def update_product_type(self, product_gid: str, product_type: str) -> tuple[str, list[str]]:
        data = self.graphql(
            PRODUCT_UPDATE_MUTATION,
            {"product": {"id": product_gid, "productType": product_type}},
        )["productUpdate"]
        errors = [" / ".join(part for part in err.get("field") or []) + ": " + err.get("message", "") for err in data.get("userErrors", [])]
        product = data.get("product") or {}
        return clean(product.get("productType")), errors


def derive_type_from_signals(record: ProductTypeRecord) -> tuple[str, str, str]:
    if record.custom_type:
        return record.custom_type, "high", "custom.type"

    collection_blob = " ".join(record.collection_handles + record.collection_titles)
    for token, value in COLLECTION_TYPE_RULES:
        if token in normalized(collection_blob):
            return value, "medium", f"collection:{token}"

    text_blob = " ".join(
        [
            record.title,
            record.handle.replace("-", " "),
            " ".join(record.tags),
            " ".join(record.collection_titles),
        ]
    )
    for token, value in TEXT_TYPE_RULES:
        if token in normalized(text_blob):
            return value, "medium", f"text:{token}"

    return "", "low", ""


def build_record_text_blob(record: ProductTypeRecord) -> str:
    return normalized(
        " ".join(
            [
                record.title,
                record.handle.replace("-", " "),
                " ".join(record.tags),
                " ".join(record.collection_titles),
                record.custom_style,
                record.custom_pattern,
            ]
        )
    )


def contains_any(text: str, tokens: list[str]) -> bool:
    return any(token in text for token in tokens)


def collect_signal_sources(record: ProductTypeRecord, tokens: list[str]) -> list[str]:
    signal_sources: list[str] = []
    title_blob = normalized(" ".join([record.title, record.handle.replace("-", " "), " ".join(record.tags)]))
    style_blob = normalized(" ".join([record.custom_style, record.custom_pattern]))
    collection_blob = normalized(" ".join(record.collection_handles + record.collection_titles))

    if contains_any(title_blob, tokens):
        signal_sources.append("title_handle_tags")
    if contains_any(style_blob, tokens):
        signal_sources.append("custom_style_pattern")
    if contains_any(collection_blob, tokens):
        signal_sources.append("collections")

    return signal_sources


def classify_records(
    records: list[ProductTypeRecord],
) -> tuple[list[ProductTypeRecord], list[PlannedUpdate], list[PlannedUpdate], list[ProductTypeRecord]]:
    missing: list[ProductTypeRecord] = []
    high_confidence_updates: list[PlannedUpdate] = []
    fallback_updates: list[PlannedUpdate] = []
    mismatches: list[ProductTypeRecord] = []

    for record in records:
        current_type = normalized(record.product_type)
        custom_type = normalized(record.custom_type)

        if not current_type:
            missing.append(record)
            target, confidence, source = derive_type_from_signals(record)
            if not target:
                continue
            planned = PlannedUpdate(record=record, target_type=target, confidence=confidence, source=source)
            if confidence == "high":
                high_confidence_updates.append(planned)
            else:
                fallback_updates.append(planned)
            continue

        if custom_type and current_type != custom_type:
            mismatches.append(record)

    return missing, high_confidence_updates, fallback_updates, mismatches


def classify_mismatch(record: ProductTypeRecord) -> MismatchDecision:
    current_type = normalized(record.product_type)
    custom_type = normalized(record.custom_type)

    if current_type == "swimsuits" and custom_type == "swimwear":
        return MismatchDecision(
            record=record,
            target_type=record.custom_type,
            confidence="high",
            source="canonical_pair:swimsuits->swimwear",
            review_reason="Synonym normalization to the store taxonomy label already used in custom.type.",
            disposition="auto_fix_candidate",
        )

    if current_type == "women jumpsuits" and custom_type == "jumpsuits":
        return MismatchDecision(
            record=record,
            target_type=record.custom_type,
            confidence="high",
            source="canonical_pair:women-jumpsuits->jumpsuits",
            review_reason="Removes audience prefix and aligns to the normalized custom.type taxonomy.",
            disposition="auto_fix_candidate",
        )

    if current_type in {"family matching", "couples"} and custom_type in {"tops", "sets", "swimwear"}:
        return MismatchDecision(
            record=record,
            target_type="",
            confidence="manual",
            source="cross_axis_taxonomy",
            review_reason="Current productType encodes audience grouping while custom.type encodes garment category; needs taxonomy policy decision before changing.",
            disposition="manual_review",
        )

    if current_type == "sweaters" and custom_type == "tops":
        return MismatchDecision(
            record=record,
            target_type="",
            confidence="manual",
            source="specificity_conflict",
            review_reason="Current productType is more specific than custom.type; do not auto-overwrite without an approved specificity rule.",
            disposition="manual_review",
        )

    jumpsuit_signals = collect_signal_sources(record, ["jumpsuit", "romper"])
    if current_type == "dresses" and custom_type in {"jumpsuits", "swimwear"}:
        return MismatchDecision(
            record=record,
            target_type="",
            confidence="manual",
            source="conflicting_category_signals",
            review_reason=(
                "Category conflict exists; leave for human review even if supporting signals are present"
                + (f" ({', '.join(jumpsuit_signals)})." if jumpsuit_signals else ".")
            ),
            disposition="manual_review",
        )

    return MismatchDecision(
        record=record,
        target_type="",
        confidence="manual",
        source="unclassified_mismatch",
        review_reason="No deterministic normalization rule has been approved for this mismatch pair yet.",
        disposition="manual_review",
    )


def split_mismatch_decisions(records: list[ProductTypeRecord]) -> tuple[list[MismatchDecision], list[MismatchDecision]]:
    auto_fix_candidates: list[MismatchDecision] = []
    manual_review: list[MismatchDecision] = []

    for record in records:
        decision = classify_mismatch(record)
        if decision.disposition == "auto_fix_candidate":
            auto_fix_candidates.append(decision)
        else:
            manual_review.append(decision)

    return auto_fix_candidates, manual_review


def build_planned_mismatch_updates(decisions: list[MismatchDecision]) -> list[PlannedUpdate]:
    return [
        PlannedUpdate(
            record=item.record,
            target_type=item.target_type,
            confidence=item.confidence,
            source=item.source,
        )
        for item in decisions
        if item.target_type
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_missing_rows(records: list[ProductTypeRecord], top_limit: int = 50) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for rank, record in enumerate(records[:top_limit], start=1):
        target, confidence, source = derive_type_from_signals(record)
        output.append(
            {
                "rank": rank,
                "product_id": record.product_id,
                "handle": record.handle,
                "title": record.title,
                "vendor": record.vendor,
                "total_inventory": record.total_inventory,
                "current_product_type": record.product_type,
                "custom_type": record.custom_type,
                "derived_target_type": target,
                "confidence": confidence,
                "source": source,
                "collection_handles": "|".join(record.collection_handles),
                "tags": "|".join(record.tags[:15]),
                "online_store_url": record.online_store_url,
            }
        )
    return output


def build_planned_rows(updates: list[PlannedUpdate]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in updates:
        rows.append(
            {
                "product_id": item.record.product_id,
                "handle": item.record.handle,
                "title": item.record.title,
                "vendor": item.record.vendor,
                "total_inventory": item.record.total_inventory,
                "current_product_type": item.record.product_type,
                "target_product_type": item.target_type,
                "custom_type": item.record.custom_type,
                "confidence": item.confidence,
                "source": item.source,
                "collection_handles": "|".join(item.record.collection_handles),
                "online_store_url": item.record.online_store_url,
            }
        )
    return rows


def build_mismatch_rows(records: list[ProductTypeRecord]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        rows.append(
            {
                "product_id": record.product_id,
                "handle": record.handle,
                "title": record.title,
                "vendor": record.vendor,
                "total_inventory": record.total_inventory,
                "current_product_type": record.product_type,
                "custom_type": record.custom_type,
                "custom_style": record.custom_style,
                "custom_pattern": record.custom_pattern,
                "collection_handles": "|".join(record.collection_handles),
                "online_store_url": record.online_store_url,
            }
        )
    return rows


def build_mismatch_decision_rows(decisions: list[MismatchDecision]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in decisions:
        rows.append(
            {
                "product_id": item.record.product_id,
                "handle": item.record.handle,
                "title": item.record.title,
                "vendor": item.record.vendor,
                "total_inventory": item.record.total_inventory,
                "current_product_type": item.record.product_type,
                "target_product_type": item.target_type,
                "custom_type": item.record.custom_type,
                "custom_style": item.record.custom_style,
                "custom_pattern": item.record.custom_pattern,
                "confidence": item.confidence,
                "source": item.source,
                "review_reason": item.review_reason,
                "collection_handles": "|".join(item.record.collection_handles),
                "online_store_url": item.record.online_store_url,
            }
        )
    return rows


def build_custom_type_rows(records: list[ProductTypeRecord], top_limit: int = 20) -> list[dict[str, Any]]:
    counts = Counter(record.custom_type or "(blank)" for record in records)
    rows: list[dict[str, Any]] = []
    for rank, (label, count) in enumerate(counts.most_common(top_limit), start=1):
        rows.append({"rank": rank, "custom_type": label, "count": count})
    return rows


def write_summary(
    path: Path,
    *,
    total_active: int,
    records: list[ProductTypeRecord],
    missing: list[ProductTypeRecord],
    high_confidence_updates: list[PlannedUpdate],
    fallback_updates: list[PlannedUpdate],
    mismatches: list[ProductTypeRecord],
    auto_fix_candidates: list[MismatchDecision],
    manual_review: list[MismatchDecision],
    missing_execution: dict[str, Any],
    mismatch_execution: dict[str, Any],
) -> None:
    top_50 = missing[:50]
    missing_distribution = Counter(record.custom_type or "(blank)" for record in missing)
    mismatch_pairs = Counter((record.product_type, record.custom_type) for record in mismatches)
    custom_type_counts = Counter(record.custom_type or "(blank)" for record in records)
    summary = {
        "total_active_products": total_active,
        "missing_product_type_active_products": len(missing),
        "top_50_missing_real_products": sum(1 for record in top_50 if record.title and record.vendor),
        "top_50_missing_blank_title": sum(1 for record in top_50 if not record.title),
        "top_50_missing_blank_vendor": sum(1 for record in top_50 if not record.vendor),
        "missing_product_type_distribution_by_custom_type": [
            {"custom_type": label, "count": count}
            for label, count in missing_distribution.most_common()
        ],
        "high_confidence_missing_updates": len(high_confidence_updates),
        "fallback_missing_updates": len(fallback_updates),
        "product_type_vs_custom_type_mismatches": len(mismatches),
        "mismatch_auto_fix_candidates": len(auto_fix_candidates),
        "mismatch_manual_review": len(manual_review),
        "mismatch_pair_counts": [
            {"current_product_type": pair[0], "custom_type": pair[1], "count": count}
            for pair, count in mismatch_pairs.most_common()
        ],
        "top_custom_type_values": [
            {"custom_type": label, "count": count}
            for label, count in custom_type_counts.most_common(20)
        ],
        "missing_execution": missing_execution,
        "mismatch_execution": mismatch_execution,
    }
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def execute_updates(
    client: ShopifyClient,
    updates: list[PlannedUpdate],
    *,
    execute: bool,
    limit: int,
    pause_ms: int,
) -> dict[str, Any]:
    planned = updates[: limit] if limit > 0 else updates
    summary = {
        "execute": bool(execute),
        "planned_updates": len(planned),
        "applied_updates": 0,
        "errors": [],
    }

    if not execute:
        return summary

    for item in planned:
        updated_type, errors = client.update_product_type(item.record.product_gid, item.target_type)
        if errors:
            summary["errors"].append(
                {
                    "handle": item.record.handle,
                    "target_type": item.target_type,
                    "errors": errors,
                }
            )
        elif normalized(updated_type) == normalized(item.target_type):
            summary["applied_updates"] += 1
        else:
            summary["errors"].append(
                {
                    "handle": item.record.handle,
                    "target_type": item.target_type,
                    "errors": [f"unexpected_response:{updated_type}"],
                }
            )
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and sync Shopify productType values.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    parser.add_argument("--execute", action="store_true", help="Apply high-confidence missing productType updates live.")
    parser.add_argument(
        "--execute-canonical-mismatch-fixes",
        action="store_true",
        help="Apply exact canonical/synonym mismatch fixes live.",
    )
    parser.add_argument("--limit", type=int, default=0, help="Only apply the first N high-confidence missing updates.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live updates.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)

    records = client.iter_active_products()
    missing, high_confidence_updates, fallback_updates, mismatches = classify_records(records)
    auto_fix_candidates, manual_review = split_mismatch_decisions(mismatches)
    canonical_mismatch_updates = build_planned_mismatch_updates(auto_fix_candidates)

    write_csv(
        output_dir / "missing_product_type_top50_audit.csv",
        build_missing_rows(missing, top_limit=50),
        [
            "rank",
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "custom_type",
            "derived_target_type",
            "confidence",
            "source",
            "collection_handles",
            "tags",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "missing_product_type_updates.csv",
        build_planned_rows(high_confidence_updates + fallback_updates),
        [
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "target_product_type",
            "custom_type",
            "confidence",
            "source",
            "collection_handles",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "product_type_mismatch_review.csv",
        build_mismatch_rows(mismatches),
        [
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "custom_type",
            "custom_style",
            "custom_pattern",
            "collection_handles",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "product_type_mismatch_auto_fix_candidates.csv",
        build_mismatch_decision_rows(auto_fix_candidates),
        [
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "target_product_type",
            "custom_type",
            "custom_style",
            "custom_pattern",
            "confidence",
            "source",
            "review_reason",
            "collection_handles",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "product_type_mismatch_canonical_auto_fix.csv",
        build_planned_rows(canonical_mismatch_updates),
        [
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "target_product_type",
            "custom_type",
            "confidence",
            "source",
            "collection_handles",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "product_type_mismatch_manual_review.csv",
        build_mismatch_decision_rows(manual_review),
        [
            "product_id",
            "handle",
            "title",
            "vendor",
            "total_inventory",
            "current_product_type",
            "target_product_type",
            "custom_type",
            "custom_style",
            "custom_pattern",
            "confidence",
            "source",
            "review_reason",
            "collection_handles",
            "online_store_url",
        ],
    )
    write_csv(
        output_dir / "active_custom_type_top20.csv",
        build_custom_type_rows(records, top_limit=20),
        ["rank", "custom_type", "count"],
    )

    missing_execution = execute_updates(
        client,
        high_confidence_updates,
        execute=args.execute,
        limit=args.limit,
        pause_ms=max(args.pause_ms, 0),
    )
    mismatch_execution = execute_updates(
        client,
        canonical_mismatch_updates,
        execute=args.execute_canonical_mismatch_fixes,
        limit=args.limit,
        pause_ms=max(args.pause_ms, 0),
    )
    write_summary(
        output_dir / "summary.json",
        total_active=len(records),
        records=records,
        missing=missing,
        high_confidence_updates=high_confidence_updates,
        fallback_updates=fallback_updates,
        mismatches=mismatches,
        auto_fix_candidates=auto_fix_candidates,
        manual_review=manual_review,
        missing_execution=missing_execution,
        mismatch_execution=mismatch_execution,
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "total_active_products": len(records),
                "missing_product_type_active_products": len(missing),
                "high_confidence_missing_updates": len(high_confidence_updates),
                "fallback_missing_updates": len(fallback_updates),
                "mismatch_review_rows": len(mismatches),
                "mismatch_auto_fix_candidates": len(auto_fix_candidates),
                "mismatch_manual_review": len(manual_review),
                "missing_execution": missing_execution,
                "mismatch_execution": mismatch_execution,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
