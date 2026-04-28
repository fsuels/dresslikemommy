#!/usr/bin/env python3
"""Build read-only Google Shopping US clean-subset review files.

This script does not call Shopify, Merchant Center, Google Ads, or the public
storefront. It joins local CSV evidence only and fails closed whenever required
Merchant Center or PDP proof is missing.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


DEFAULT_AOV = Decimal("63.25")
DEFAULT_INPUT = Path(
    "dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/"
    "2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY"
)
DEFAULT_STOREFRONT = "https://www.dresslikemommy.com"
NEEDS_DATA = "NEEDS_DATA"
PASS_STATUSES = {"pass", "passed", "ok", "valid", "approved", "eligible", "processed", "configured"}
MC_APPROVED_STATUSES = {"approved"}
MC_DESTINATION_PASS_WORDS = ("shopping", "eligible")

MASTER_FIELDNAMES = [
    "shopify_product_id",
    "shopify_variant_id",
    "sku",
    "gtin_or_barcode",
    "merchant_center_item_id",
    "title",
    "product_url",
    "price",
    "cost",
    "gross_margin_amount",
    "gross_margin_percent",
    "max_marketing_allowed",
    "max_cac",
    "collection",
    "product_family",
    "image_url",
    "merchant_center_status",
    "merchant_center_destination",
    "merchant_center_issue_count",
    "merchant_center_issues",
    "image_status",
    "price_status",
    "availability_status",
    "shipping_policy_status",
    "return_policy_status",
    "pdp_status",
    "market",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
    "paid_eligible",
    "fix_before_paid",
    "exclusion_reason",
]


@dataclass(frozen=True)
class Evidence:
    values: dict[str, str]

    def get(self, *keys: str, default: str = NEEDS_DATA) -> str:
        for key in keys:
            value = self.values.get(key)
            if value is not None and str(value).strip():
                return clean(value)
        return default


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def parse_decimal(value: str | None) -> Decimal | None:
    value = clean(value)
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def money(value: Decimal | None) -> str:
    if value is None:
        return ""
    return str(value.quantize(Decimal("0.01")))


def percent(value: Decimal | None) -> str:
    if value is None:
        return ""
    return str((value * Decimal("100")).quantize(Decimal("0.01")))


def is_blank(value: str | None) -> bool:
    return not clean(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def evidence_join_key(row: dict[str, str]) -> str:
    for key in ("merchant_center_item_id", "merchant_center_id", "id"):
        value = clean(row.get(key))
        if value:
            return value
    product_id = clean(row.get("shopify_product_id") or row.get("product_id"))
    variant_id = clean(row.get("shopify_variant_id") or row.get("variant_id"))
    if product_id and variant_id:
        return f"{product_id}:{variant_id}"
    return ""


def load_evidence(path: Path | None) -> dict[str, Evidence]:
    if not path:
        return {}
    evidence: dict[str, Evidence] = {}
    for row in read_csv(path):
        key = evidence_join_key(row)
        if key:
            evidence[key] = Evidence(row)
    return evidence


def product_url(row: dict[str, str], storefront_base_url: str) -> str:
    handle = clean(row.get("handle"))
    if not handle:
        return ""
    return f"{storefront_base_url.rstrip('/')}/products/{handle}"


def derive_product_family(row: dict[str, str]) -> str:
    text = " ".join(
        [
            row.get("handle", ""),
            row.get("product_title", ""),
            row.get("variant_title", ""),
            row.get("marketing_product_set_type", ""),
        ]
    ).lower()
    if any(token in text for token in ("maternity", "pregnan")):
        return "maternity"
    if any(token in text for token in ("couple", "valentine")):
        return "couples"
    if any(token in text for token in ("daddy", "father", "dad ", "father-son", "father and")):
        return "daddy_me"
    if any(token in text for token in ("pajama", "pyjama", "sleepwear", "pjs")):
        return "pajamas"
    if any(token in text for token in ("swim", "bikini", "swimsuit", "trunks", "beach")):
        return "swimsuits"
    if any(token in text for token in ("mommy", "mother", "mom ", "mom-", "daughter")):
        return "mommy_me"
    if "family" in text:
        return "family_matching"
    if "dress" in text:
        return "dresses"
    return "other"


def supports_multi_item_order(row: dict[str, str], family: str) -> bool:
    set_type = normalize_key(row.get("marketing_product_set_type", ""))
    if set_type == "set":
        return True
    return family in {"mommy_me", "family_matching", "pajamas", "swimsuits", "daddy_me"}


def margin_tier(price: Decimal | None, cost: Decimal | None) -> str:
    if price is None or price <= 0 or cost is None:
        return "margin_unknown"
    gross_pct = (price - cost) / price
    if gross_pct >= Decimal("0.65"):
        return "margin_high"
    if gross_pct >= Decimal("0.35"):
        return "margin_medium"
    return "margin_low"


def aov_tier(price: Decimal | None, aov: Decimal, multi_item: bool) -> str:
    if price is None:
        return "aov_unknown"
    if price >= aov:
        return "aov_high"
    if multi_item or price >= (aov * Decimal("0.60")):
        return "aov_medium"
    return "aov_low"


def status_pass(value: str) -> bool:
    return normalize_key(value) in PASS_STATUSES


def merchant_status_pass(value: str) -> bool:
    return normalize_key(value) in MC_APPROVED_STATUSES


def destination_pass(value: str) -> bool:
    normalized = value.lower()
    return all(word in normalized for word in MC_DESTINATION_PASS_WORDS)


def issue_count(value: str) -> int | None:
    value = clean(value)
    if not value or value == NEEDS_DATA:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def first_label_group(reasons: list[str]) -> str:
    if not reasons:
        return "paid_eligible"
    if any("unknown_margin" in reason or "missing_cost" in reason for reason in reasons):
        return "exclude_unknown_margin"
    if any("low_aov" in reason for reason in reasons):
        return "exclude_low_aov"
    if any("international" in reason for reason in reasons):
        return "international_exclude"
    if any(
        reason.startswith(("needs_merchant_center", "needs_image", "needs_price", "needs_availability", "needs_shipping", "needs_return"))
        or "merchant_center" in reason
        or "missing_sku" in reason
        or "missing_gtin" in reason
        or "out_of_stock" in reason
        for reason in reasons
    ):
        return "exclude_feed_issue"
    if any("pdp" in reason for reason in reasons):
        return "exclude_pdp_issue"
    return "exclude_feed_issue"


def build_master_row(
    row: dict[str, str],
    merchant_evidence: Evidence | None,
    pdp_evidence: Evidence | None,
    *,
    aov: Decimal,
    storefront_base_url: str,
) -> dict[str, str]:
    price = parse_decimal(row.get("price"))
    cost = parse_decimal(row.get("unit_cost") or row.get("cost"))
    gross_amount = price - cost if price is not None and cost is not None else None
    gross_pct = (gross_amount / price) if gross_amount is not None and price and price > 0 else None
    max_marketing = price * Decimal("0.15") if price is not None else None

    family = derive_product_family(row)
    multi_item = supports_multi_item_order(row, family)
    market = "US"

    merchant = merchant_evidence or Evidence({})
    pdp = pdp_evidence or Evidence({})

    merchant_status = merchant.get("merchant_center_status", "status")
    merchant_destination = merchant.get("merchant_center_destination", "destination")
    merchant_issues = merchant.get(
        "merchant_center_issues",
        "issues",
        default="" if merchant_evidence else NEEDS_DATA,
    )
    merchant_issue_count = merchant.get("merchant_center_issue_count", "issue_count")
    image_status = merchant.get("image_status")
    price_status = merchant.get("price_status")
    availability_status = merchant.get("availability_status")
    shipping_status = merchant.get("shipping_policy_status")
    return_status = merchant.get("return_policy_status")
    image_url = merchant.get("image_url", default=NEEDS_DATA)
    pdp_status = pdp.get("pdp_status", "status")

    local_reasons: list[str] = []
    evidence_reasons: list[str] = []

    if price is None:
        local_reasons.append("exclude_unknown_price")
    if cost is None:
        local_reasons.append("exclude_unknown_margin_missing_cost")
    if gross_pct is None:
        local_reasons.append("exclude_unknown_margin")
    if is_blank(row.get("sku")):
        local_reasons.append("exclude_missing_sku")
    if is_blank(row.get("barcode")):
        local_reasons.append("exclude_missing_gtin")
    inventory_quantity = parse_decimal(row.get("inventory_quantity"))
    if inventory_quantity is None:
        local_reasons.append("exclude_inventory_needs_data")
    elif inventory_quantity <= 0:
        local_reasons.append("exclude_out_of_stock")
    if family in {"maternity", "couples"}:
        local_reasons.append(f"exclude_weak_initial_collection_{family}")
    if price is not None and price < aov and not multi_item:
        local_reasons.append("exclude_low_aov_no_multi_item_order")

    mc_count = issue_count(merchant_issue_count)
    if not merchant_status_pass(merchant_status):
        evidence_reasons.append(
            "needs_merchant_center_status"
            if merchant_status == NEEDS_DATA
            else f"exclude_merchant_center_status_{normalize_key(merchant_status)}"
        )
    if not destination_pass(merchant_destination):
        evidence_reasons.append(
            "needs_merchant_center_destination"
            if merchant_destination == NEEDS_DATA
            else "exclude_merchant_center_destination"
        )
    if mc_count is None:
        evidence_reasons.append("needs_merchant_center_issue_count")
    elif mc_count > 0:
        evidence_reasons.append("exclude_merchant_center_issues")
    if merchant_issues and merchant_issues != NEEDS_DATA and normalize_key(merchant_issues) not in {"none", "no_issues"}:
        evidence_reasons.append("exclude_merchant_center_issues")
    for status_name, status_value in [
        ("image_status", image_status),
        ("price_status", price_status),
        ("availability_status", availability_status),
        ("shipping_policy_status", shipping_status),
        ("return_policy_status", return_status),
    ]:
        if not status_pass(status_value):
            evidence_reasons.append(
                f"needs_{status_name}"
                if status_value == NEEDS_DATA
                else f"exclude_{status_name}_{normalize_key(status_value)}"
            )
    if not status_pass(pdp_status):
        evidence_reasons.append(
            "needs_pdp_verification"
            if pdp_status == NEEDS_DATA
            else f"exclude_pdp_status_{normalize_key(pdp_status)}"
        )

    reasons = list(dict.fromkeys([*local_reasons, *evidence_reasons]))
    paid_eligible = not reasons
    fix_before_paid = not paid_eligible and any(
        reason.startswith(("needs_", "exclude_missing_", "exclude_unknown_", "exclude_low_aov", "exclude_out_of_stock"))
        for reason in reasons
    )
    label_1 = margin_tier(price, cost)
    label_3 = aov_tier(price, aov, multi_item)

    return {
        "shopify_product_id": clean(row.get("product_id")),
        "shopify_variant_id": clean(row.get("variant_id")),
        "sku": clean(row.get("sku")),
        "gtin_or_barcode": clean(row.get("barcode")),
        "merchant_center_item_id": clean(row.get("merchant_center_id")) or clean(row.get("merchant_center_item_id")),
        "title": clean(row.get("product_title")),
        "product_url": product_url(row, storefront_base_url),
        "price": money(price),
        "cost": money(cost),
        "gross_margin_amount": money(gross_amount),
        "gross_margin_percent": percent(gross_pct),
        "max_marketing_allowed": money(max_marketing),
        "max_cac": money(max_marketing),
        "collection": family,
        "product_family": family,
        "image_url": image_url,
        "merchant_center_status": merchant_status,
        "merchant_center_destination": merchant_destination,
        "merchant_center_issue_count": merchant_issue_count,
        "merchant_center_issues": merchant_issues,
        "image_status": image_status,
        "price_status": price_status,
        "availability_status": availability_status,
        "shipping_policy_status": shipping_status,
        "return_policy_status": return_status,
        "pdp_status": pdp_status,
        "market": market,
        "custom_label_0": "paid_eligible" if paid_eligible else first_label_group(reasons),
        "custom_label_1": label_1,
        "custom_label_2": family,
        "custom_label_3": label_3,
        "custom_label_4": "us_test_ready" if paid_eligible else "us_fix_before_paid",
        "paid_eligible": "TRUE" if paid_eligible else "FALSE",
        "fix_before_paid": "TRUE" if fix_before_paid else "FALSE",
        "exclusion_reason": ";".join(reasons),
    }


def build_rows(
    eligibility_rows: list[dict[str, str]],
    merchant_evidence: dict[str, Evidence],
    pdp_evidence: dict[str, Evidence],
    *,
    aov: Decimal,
    storefront_base_url: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in eligibility_rows:
        key = evidence_join_key(row)
        fallback_key = f"{clean(row.get('product_id'))}:{clean(row.get('variant_id'))}"
        rows.append(
            build_master_row(
                row,
                merchant_evidence.get(key) or merchant_evidence.get(fallback_key),
                pdp_evidence.get(key) or pdp_evidence.get(fallback_key),
                aov=aov,
                storefront_base_url=storefront_base_url,
            )
        )
    rows.sort(
        key=lambda item: (
            item["paid_eligible"] != "TRUE",
            item["fix_before_paid"] != "TRUE",
            item["custom_label_2"],
            item["title"],
            item["shopify_variant_id"],
        )
    )
    return rows


def write_campaign_plan(path: Path, summary: dict[str, object]) -> None:
    paid_count = summary["paid_eligible_rows"]
    decision = summary["launch_decision"]
    path.write_text(
        "\n".join(
            [
                "# Google Ads Paused Standard Shopping Build Plan",
                "",
                "Status: review-only. Do not create or enable campaigns from this file without explicit owner approval.",
                "",
                f"Launch decision: `{decision}`",
                "",
                "## Campaign",
                "",
                "- Campaign name: `US | Standard Shopping | Clean Subset | Paid Eligible | Test`",
                "- Campaign type: Shopping",
                "- Subtype: Standard Shopping only",
                "- Merchant Center: Dresslikemommy / `124884876`",
                "- Country: United States",
                "- Inventory filter:",
                "  - `custom_label_0 = paid_eligible`",
                "  - `custom_label_4 = us_test_ready`",
                "- Status: Paused",
                "- Budget: tiny placeholder only, keep paused",
                "- Bidding: conservative Manual CPC or equivalent low-risk bidding",
                "- Networks: Google Search Network only if appropriate; do not enable Search Partners unless explicitly approved",
                "",
                "## Product Groups",
                "",
                "- Subdivide by `custom_label_2` product family.",
                "- Then subdivide by `custom_label_1` margin tier.",
                "- Include only rows where `paid_eligible = TRUE`.",
                "- Exclude everything else.",
                "",
                "## Explicit Exclusions",
                "",
                "- Performance Max",
                "- broad Search",
                "- Display",
                "- Dynamic Search Ads",
                "- international campaigns",
                "- all-products Shopping",
                "- unknown-margin products",
                "- products with feed issues",
                "- products with PDP issues",
                "- products not marked `paid_eligible = TRUE`",
                "",
                "## Current Review Counts",
                "",
                f"- Total variants reviewed: {summary['total_rows']}",
                f"- Merchant Center products matched with evidence: {summary['merchant_evidence_rows']}",
                f"- `paid_eligible = TRUE`: {paid_count}",
                f"- `fix_before_paid = TRUE`: {summary['fix_before_paid_rows']}",
                f"- excluded/not eligible rows: {summary['excluded_rows']}",
                "",
                "## Gate",
                "",
                "- If fewer than 20 clean products pass, keep `LAUNCH_BLOCKED`.",
                "- If products pass but tracking/PDP/feed evidence still needs review, use `READY_FOR_PAUSED_BUILDOUT` only.",
                "- Use `READY_FOR_LIMITED_TEST` only after measurement, feed status, margin, PDP, shipping, and return policy all pass.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def summarize(rows: list[dict[str, str]], merchant_evidence_rows: int, pdp_evidence_rows: int) -> dict[str, object]:
    reason_counts = Counter(
        reason
        for row in rows
        for reason in row["exclusion_reason"].split(";")
        if reason
    )
    family_counts = Counter(row["custom_label_2"] for row in rows)
    paid_family_counts = Counter(
        row["custom_label_2"] for row in rows if row["paid_eligible"] == "TRUE"
    )
    paid_count = sum(1 for row in rows if row["paid_eligible"] == "TRUE")
    launch_decision = "LAUNCH_BLOCKED" if paid_count < 20 else "READY_FOR_PAUSED_BUILDOUT"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_OWNER_REVIEW_FILES_ONLY",
        "launch_decision": launch_decision,
        "total_rows": len(rows),
        "merchant_evidence_rows": merchant_evidence_rows,
        "pdp_evidence_rows": pdp_evidence_rows,
        "paid_eligible_rows": paid_count,
        "fix_before_paid_rows": sum(1 for row in rows if row["fix_before_paid"] == "TRUE"),
        "excluded_rows": sum(1 for row in rows if row["paid_eligible"] != "TRUE"),
        "top_exclusion_reasons": dict(reason_counts.most_common(20)),
        "product_family_counts": dict(sorted(family_counts.items())),
        "paid_eligible_family_counts": dict(sorted(paid_family_counts.items())),
    }


def build_outputs(
    input_eligibility: Path,
    output_dir: Path,
    merchant_center_evidence: Path | None,
    pdp_evidence: Path | None,
    *,
    aov: Decimal,
    storefront_base_url: str,
) -> dict[str, object]:
    eligibility_rows = read_csv(input_eligibility)
    merchant_evidence = load_evidence(merchant_center_evidence)
    pdp = load_evidence(pdp_evidence)
    rows = build_rows(
        eligibility_rows,
        merchant_evidence,
        pdp,
        aov=aov,
        storefront_base_url=storefront_base_url,
    )
    paid_rows = [row for row in rows if row["paid_eligible"] == "TRUE"]
    excluded_rows = [row for row in rows if row["paid_eligible"] != "TRUE"]
    fix_rows = [row for row in rows if row["fix_before_paid"] == "TRUE"]

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "master": output_dir / "google_shopping_us_clean_subset_master.csv",
        "paid_eligible": output_dir / "google_shopping_us_clean_subset_paid_eligible.csv",
        "excluded": output_dir / "google_shopping_excluded_products_with_reasons.csv",
        "fix_before_paid": output_dir / "google_shopping_fix_before_paid.csv",
        "campaign_plan": output_dir / "google_ads_paused_standard_shopping_build_plan.md",
        "summary": output_dir / "summary.json",
    }
    write_csv(paths["master"], MASTER_FIELDNAMES, rows)
    write_csv(paths["paid_eligible"], MASTER_FIELDNAMES, paid_rows)
    write_csv(paths["excluded"], MASTER_FIELDNAMES, excluded_rows)
    write_csv(paths["fix_before_paid"], MASTER_FIELDNAMES, fix_rows)
    summary = summarize(rows, len(merchant_evidence), len(pdp))
    summary["input_eligibility"] = str(input_eligibility)
    summary["outputs"] = {key: str(path) for key, path in paths.items()}
    paths["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_campaign_plan(paths["campaign_plan"], summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build read-only owner-review files for a US Google Shopping clean subset."
    )
    parser.add_argument("--input-eligibility", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--merchant-center-evidence", type=Path, default=None)
    parser.add_argument("--pdp-evidence", type=Path, default=None)
    parser.add_argument("--aov-benchmark", default=str(DEFAULT_AOV))
    parser.add_argument("--storefront-base-url", default=DEFAULT_STOREFRONT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_outputs(
        args.input_eligibility,
        args.output_dir,
        args.merchant_center_evidence,
        args.pdp_evidence,
        aov=Decimal(str(args.aov_benchmark)),
        storefront_base_url=args.storefront_base_url,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
