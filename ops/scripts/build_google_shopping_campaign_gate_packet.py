#!/usr/bin/env python3
"""Build a campaign gate packet for the Google Shopping clean cohort.

The packet proves the exact paid cohort, maps variant rows back to Shopify
listings, and records why a live Google Ads build is blocked until the clean
labels are visible in Merchant Center/Google Ads.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path("dresslikemommy-growth-2026")
PAID_COHORT = ROOT / "02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/google_shopping_us_clean_subset_paid_eligible.csv"
MASTER = ROOT / "02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/google_shopping_us_clean_subset_master.csv"
SHOPIFY_VARIANTS = ROOT / "01_EXPORTS_RAW/SHOPIFY/2026-04-29-shopify-margin-cac-export-pack_active_variants_readonly_sanitized.json"
LIVE_LABEL_CAPTURE = ROOT / "02_AUDIT_PACKETS/2026-04-29-merchant-campaign-build-live-check/merchant_exact_label_readback.json"
LIVE_LABEL_CAPTURE_AFTER_SHOPIFY_CLEAR = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-29-merchant-campaign-build-live-check/merchant_exact_label_readback_after_shopify_clear.json"
)
LIVE_LABEL_CAPTURE_REFRESH_CHECK = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-29-merchant-campaign-build-live-check/merchant_exact_label_readback_refresh_check.json"
)
LIVE_LABEL_CAPTURE_GLOB_ROOT = ROOT / "02_AUDIT_PACKETS"
PURCHASE_CONVERSION_VALUE_GATE = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/"
    "google_ads_conversion_value_gate_summary.json"
)
PURCHASE_CONVERSION_VALUE_GATE_GLOB_ROOT = ROOT / "02_AUDIT_PACKETS"
OUTPUT_DIR = ROOT / "02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate"

POST_GATE_ADS_STRUCTURE = [
    {
        "campaign": "Brand Search — USA",
        "use_only_after": "Purchase conversion tracking records value correctly.",
        "required_exclusions": "Exclude if tracking is not recording.",
    },
    {
        "campaign": "Standard Shopping — USA eligible products",
        "use_only_after": "Merchant Center and product-margin gates pass.",
        "required_exclusions": "Exclude UNKNOWN_MARGIN, FIX_BEFORE_PAID, limited, and not-approved products.",
    },
    {
        "campaign": "PMax — USA eligible products",
        "use_only_after": "Only after feed, conversion, landing-page, and product-label gates pass.",
        "required_exclusions": "URL expansion off unless an approved landing-page map exists.",
    },
    {
        "campaign": "Non-brand Search",
        "use_only_after": "Search Console query/page exports prove commercial opportunity.",
        "required_exclusions": "Exclude pages not READY_FOR_PAID.",
    },
    {
        "campaign": "Remarketing",
        "use_only_after": "Policy-limited ads are fixed and tracking is deduped.",
        "required_exclusions": "Do not use current limited ads.",
    },
]


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "unknown"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def metafield_value(product: dict[str, Any], key: str) -> str:
    for node in product.get("googleShoppingMetafields", {}).get("nodes", []):
        if node.get("namespace") == "mm-google-shopping" and node.get("key") == key:
            return clean(node.get("value"))
    return ""


def publication_map(product: dict[str, Any]) -> dict[str, bool]:
    out: dict[str, bool] = {}
    for edge in product.get("resourcePublications", {}).get("edges", []):
        node = edge.get("node", {})
        name = node.get("publication", {}).get("name")
        if name:
            out[name] = bool(node.get("isPublished"))
    return out


def load_shopify_variants() -> dict[str, dict[str, Any]]:
    payload = json.loads(SHOPIFY_VARIANTS.read_text(encoding="utf-8"))
    return {clean(row.get("legacyResourceId")): row for row in payload.get("variants", [])}


def role_from_variant(variant_title: str, product_title: str = "") -> str:
    text = f"{variant_title} {product_title}".lower()
    if re.search(r"\b(father|dad|daddy|men|man|boyfriend|husband)\b", text):
        return "father"
    if re.search(r"\b(mother|mom|mommy|mama|women|woman|lady)\b", text):
        return "mother"
    if re.search(r"\b(child|kid|kids|girl|boy|toddler|baby|infant|newborn|years?|yrs?|[0-9]+t)\b", text):
        return "child"
    return "unclear"


def item_type_from_text(product_type: str, title: str) -> str:
    text = f"{product_type} {title}".lower()
    if "shirt" in text or "tee" in text or "top" in text:
        return "shirt_or_top"
    if "pajama" in text or "pyjama" in text or "sleep" in text:
        return "pajamas"
    if "swim" in text or "bikini" in text or "trunk" in text:
        return "swimwear"
    if "dress" in text or "gown" in text:
        return "dress"
    if "short" in text or "pants" in text or "bottom" in text:
        return "bottoms"
    return slug(product_type or "apparel")


def missing_fix(reason: str) -> str:
    mapping = {
        "missing_gtin": "Add valid barcode/GTIN or mark custom product where appropriate.",
        "merchant_center_status": "Resolve Merchant Center approval or limitation status.",
        "merchant_center_destination": "Make the offer eligible for Shopping ads.",
        "merchant_center_issues": "Fix Merchant Center item issues.",
        "image_status": "Fix product image eligibility.",
        "price_status": "Fix price/feed price match.",
        "availability_status": "Fix stock/availability feed match.",
        "shipping_policy_status": "Confirm shipping policy/readiness.",
        "return_policy_status": "Confirm return policy/readiness.",
        "pdp": "Pass landing-page QA.",
        "out_of_stock": "Restock the variant or keep it excluded.",
        "unknown_margin": "Set unit cost and margin evidence.",
        "low_aov": "Keep excluded unless bundle/order economics improve.",
        "duplicate_sku": "Make SKU unique before paid traffic.",
        "duplicate_gtin": "Make GTIN/barcode unique before paid traffic.",
    }
    for key, value in mapping.items():
        if key in reason:
            return value
    return "Review exclusion reason and fix the underlying feed/product evidence."


def live_label_status() -> dict[str, object]:
    candidates = [
        *LIVE_LABEL_CAPTURE_GLOB_ROOT.glob("2026-04-29-*/merchant_exact_label_readback_refresh_check.json"),
        LIVE_LABEL_CAPTURE_REFRESH_CHECK,
        LIVE_LABEL_CAPTURE_AFTER_SHOPIFY_CLEAR,
        LIVE_LABEL_CAPTURE,
    ]
    existing = [path for path in candidates if path.exists()]
    path = max(existing, key=lambda item: item.stat().st_mtime) if existing else LIVE_LABEL_CAPTURE
    if not path.exists():
        return {
            "status": "BLOCKED_NOT_CAPTURED",
            "detail": "Live Merchant Center exact-label readback artifact is missing.",
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["source_artifact"] = str(path)
    return payload


def purchase_conversion_value_status() -> dict[str, object]:
    candidates = [
        *PURCHASE_CONVERSION_VALUE_GATE_GLOB_ROOT.glob("2026-04-29-*/google_ads_conversion_value_gate_summary.json"),
        PURCHASE_CONVERSION_VALUE_GATE,
    ]
    existing = [path for path in candidates if path.exists()]
    path = max(existing, key=lambda item: item.stat().st_mtime) if existing else PURCHASE_CONVERSION_VALUE_GATE
    if not path.exists():
        return {
            "mode": "READ_ONLY_GOOGLE_ADS_PURCHASE_CONVERSION_VALUE_GATE",
            "gate": {
                "purchase_conversion_value_gate_status": "BLOCKED_NOT_CAPTURED",
                "purchase_conversion_value_gate_passed": False,
                "blockers": ["Google Ads purchase conversion-value gate artifact is missing."],
            },
            "source_artifact": str(path),
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["source_artifact"] = str(path)
    return payload


def build() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paid_rows = read_csv(PAID_COHORT)
    master_rows = read_csv(MASTER)
    shopify_by_variant = load_shopify_variants()

    proof_rows: list[dict[str, object]] = []
    product_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    family_groups: dict[str, list[dict[str, object]]] = defaultdict(list)

    for row in paid_rows:
        variant = shopify_by_variant.get(clean(row.get("shopify_variant_id")), {})
        product = variant.get("product", {})
        pubs = publication_map(product)
        role = role_from_variant(clean(variant.get("title")), clean(product.get("title") or row.get("title")))
        item_type = item_type_from_text(clean(product.get("productType")), clean(product.get("title") or row.get("title")))
        handle = clean(product.get("handle")) or row["product_url"].rstrip("/").split("/")[-1]
        proposed_item_group_id = f"dlm_{row['shopify_product_id']}_{role}_{item_type}"
        family_style_id = f"dlm_style_{row['shopify_product_id']}_{slug(handle)}"
        current_product_level_labels = {
            f"current_shopify_mm_google_custom_label_{idx}": metafield_value(product, f"custom_label_{idx}")
            for idx in range(5)
        }
        proof = {
            "shopify_product_id": row["shopify_product_id"],
            "shopify_variant_id": row["shopify_variant_id"],
            "handle": handle,
            "product_title": clean(product.get("title") or row.get("title")),
            "variant_title": clean(variant.get("title")),
            "sku": row["sku"],
            "barcode_gtin": row["gtin_or_barcode"],
            "merchant_center_item_id": row["merchant_center_item_id"],
            "current_item_group_id": f"shopify_US_{row['shopify_product_id']}",
            "current_item_group_id_evidence": "INFERRED_FROM_SHOPIFY_PRODUCT_ID; exact live MC item_group_id export not present locally",
            "proposed_item_group_id": proposed_item_group_id,
            "family_style_id": family_style_id,
            "role": role,
            "item_type": item_type,
            "shopify_product_type": clean(product.get("productType")),
            "product_type_for_ads": row["product_family"],
            "google_product_category": "NEEDS_MERCHANT_EXPORT",
            "image_link": row["image_url"],
            "link": row["product_url"],
            "price": row["price"],
            "availability": "in_stock" if int(variant.get("inventoryQuantity") or 0) > 0 else "out_of_stock",
            "unit_cost": row["cost"],
            "gross_margin_percent": row["gross_margin_percent"],
            "margin_tier": row["custom_label_1"],
            "inventory": variant.get("inventoryQuantity", ""),
            "custom_label_0": row["custom_label_0"],
            "custom_label_1": row["custom_label_1"],
            "custom_label_2": row["custom_label_2"],
            "custom_label_3": row["custom_label_3"],
            "custom_label_4": row["custom_label_4"],
            "online_store_published": pubs.get("Online Store", False),
            "google_youtube_published": pubs.get("Google & YouTube", False),
            **current_product_level_labels,
        }
        proof_rows.append(proof)
        product_groups[row["shopify_product_id"]].append(proof)
        family_groups[family_style_id].append(proof)

    listing_rows: list[dict[str, object]] = []
    for product_id, rows in sorted(product_groups.items()):
        roles = sorted({clean(row["role"]) for row in rows})
        all_master_for_product = [row for row in master_rows if row["shopify_product_id"] == product_id]
        defect_rows = [row for row in all_master_for_product if row["paid_eligible"] != "TRUE"]
        unknown_margin_rows = [row for row in all_master_for_product if "unknown_margin" in row["exclusion_reason"]]
        classification = "A_TRUE_VARIANT_GROUP" if len(roles) <= 1 else "B_FAMILY_STYLE_DIFFERENT_PHYSICAL_PRODUCTS"
        listing_rows.append(
            {
                "shopify_product_id": product_id,
                "handle": rows[0]["handle"],
                "listing_title": rows[0]["product_title"],
                "active_variant_count_in_paid_cohort": len(rows),
                "all_reviewed_variant_count": len(all_master_for_product),
                "role_count": len(roles),
                "roles": ";".join(roles),
                "total_inventory_paid_variants": sum(int(row.get("inventory") or 0) for row in rows),
                "known_margin_variant_count": sum(1 for row in all_master_for_product if clean(row.get("cost"))),
                "unknown_margin_variant_count": len(unknown_margin_rows),
                "feed_defect_count": len(defect_rows),
                "feed_structure_classification": classification,
                "recommended_paid_decision": "KEEP_VARIANT_ROWS; BID_BY_STYLE_CATEGORY_MARGIN_AFTER_LABELS_VERIFY",
            }
        )

    item_group_rows: list[dict[str, object]] = []
    item_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in proof_rows:
        item_groups[clean(row["proposed_item_group_id"])].append(row)
    for group_id, rows in sorted(item_groups.items()):
        role = clean(rows[0]["role"])
        item_type = clean(rows[0]["item_type"])
        item_group_rows.append(
            {
                "proposed_item_group_id": group_id,
                "included_variant_ids": ";".join(clean(row["shopify_variant_id"]) for row in rows),
                "merchant_center_item_ids": ";".join(clean(row["merchant_center_item_id"]) for row in rows),
                "role": role,
                "item_type": item_type,
                "reason": "Group sizes/colors of the same role/item for bidding; do not group mother/child/father as one Google item_group_id.",
                "risk": "Exact live item_group_id must be verified/exported before feed rewrite.",
            }
        )

    family_rows: list[dict[str, object]] = []
    for family_style_id, rows in sorted(family_groups.items()):
        related = sorted({clean(row["proposed_item_group_id"]) for row in rows})
        family_rows.append(
            {
                "family_style_id": family_style_id,
                "related_item_group_ids": ";".join(related),
                "collection_category": clean(rows[0]["product_type_for_ads"]),
                "recommended_google_ads_product_group": (
                    f"custom_label_4=us_test_ready > custom_label_0=paid_eligible > "
                    f"item_ids_for_{family_style_id}; add custom_label_1..3 subdivisions only after full-label readback passes"
                ),
                "paid_eligibility": "ELIGIBLE_FOR_VERIFIED_FILTERS_ONLY_UNTIL_FULL_LABEL_READBACK_PASSES",
                "paid_variant_count": len(rows),
            }
        )

    image_rows: list[dict[str, object]] = []
    for row in proof_rows:
        role = clean(row["role"])
        risk = "MEDIUM"
        recommendation = "Use role-specific image_link when available; keep family lifestyle image as additional_image_link."
        if role in {"child", "father"}:
            risk = "HIGH_IF_FULL_FAMILY_PHOTO_SHOWS_MORE_THAN_THE_SINGLE_ITEM"
        image_rows.append(
            {
                "shopify_variant_id": row["shopify_variant_id"],
                "merchant_center_item_id": row["merchant_center_item_id"],
                "role": role,
                "current_image": row["image_link"],
                "recommended_image_link": "ROLE_SPECIFIC_IMAGE_NEEDED_IF_AVAILABLE",
                "recommended_additional_image_link": row["image_link"],
                "risk_if_same_family_photo_is_used": risk,
                "recommendation": recommendation,
            }
        )

    exclusion_rows: list[dict[str, object]] = []
    for row in master_rows:
        if row["paid_eligible"] == "TRUE":
            continue
        reasons = [reason for reason in row["exclusion_reason"].split(";") if reason]
        primary = reasons[0] if reasons else "unknown"
        exclusion_rows.append(
            {
                "shopify_variant_id": row["shopify_variant_id"],
                "merchant_center_item_id": row["merchant_center_item_id"],
                "shopify_product_id": row["shopify_product_id"],
                "title": row["title"],
                "reason_for_exclusion": row["exclusion_reason"],
                "missing_fix": missing_fix(primary),
                "smallest_data_needed": "Fix/readback the listed reason, then rerun clean-subset builder.",
            }
        )

    live_status = live_label_status()
    campaign_filters_ready = bool(live_status.get("campaign_creation_allowed"))
    full_labels_ready = bool(live_status.get("all_expected_labels_visible"))
    conversion_status = purchase_conversion_value_status()
    conversion_gate = conversion_status.get("gate", {}) if isinstance(conversion_status, dict) else {}
    purchase_conversion_value_ready = bool(conversion_gate.get("purchase_conversion_value_gate_passed"))
    ads_dry_run_actionable_allowed = bool(campaign_filters_ready and full_labels_ready and purchase_conversion_value_ready)
    actionability_blockers: list[str] = []
    if not campaign_filters_ready:
        actionability_blockers.append("Merchant Center campaign filter labels are not visible.")
    if not full_labels_ready:
        actionability_blockers.append("Merchant Center supplemental label join is not fully visible for custom_label_1..3.")
    if not purchase_conversion_value_ready:
        actionability_blockers.extend(
            clean(blocker)
            for blocker in conversion_gate.get("blockers", ["Purchase conversion-value gate did not pass."])
        )

    if ads_dry_run_actionable_allowed:
        decision = "READY_FOR_PAUSED_ADS_DRY_RUN_BUILD_WITH_FULL_LABEL_JOIN_AND_PURCHASE_VALUE_PROOF"
        label_status_reason = (
            "Live Merchant Center readback shows all expected custom_label_0..4 values "
            "for the sampled paid US offer."
        )
    elif full_labels_ready and not purchase_conversion_value_ready:
        decision = "DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__PURCHASE_VALUE_BLOCKED"
        label_status_reason = (
            "Live Merchant Center readback shows all expected custom_label_0..4 values "
            "for the sampled paid US offer, but purchase conversion-value proof is still blocked."
        )
    elif campaign_filters_ready:
        decision = "DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__MERCHANT_LABEL_JOIN_OR_PURCHASE_VALUE_BLOCKED"
        label_status_reason = (
            "Live Merchant Center readback shows the two campaign filter labels, "
            "custom_label_0=paid_eligible and custom_label_4=us_test_ready, but "
            "custom_label_1..3 still do not match the clean-label source. Purchase conversion-value proof must "
            "also pass before any Ads dry-run build becomes actionable."
        )
    else:
        decision = "DRY_RUN_STRUCTURE_ONLY_NOT_ACTIONABLE__MERCHANT_FILTER_LABELS_NOT_VISIBLE"
        label_status_reason = (
            "Live Merchant Center readback has not shown the required campaign filter labels "
            "on the sampled paid US offer."
        )
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "CAMPAIGN_GATE_PACKET_NO_ADS_LAUNCH",
        "paid_cohort_rows": len(proof_rows),
        "paid_unique_shopify_products": len(product_groups),
        "paid_unique_proposed_item_groups": len(item_groups),
        "all_master_rows_reviewed": len(master_rows),
        "excluded_rows": len(exclusion_rows),
        "paid_products_with_mixed_eligible_and_excluded_variants": sum(
            1
            for product_id in product_groups
            if any(row["paid_eligible"] == "TRUE" for row in master_rows if row["shopify_product_id"] == product_id)
            and any(row["paid_eligible"] != "TRUE" for row in master_rows if row["shopify_product_id"] == product_id)
        ),
        "paid_product_feed_structure_counts": dict(Counter(row["feed_structure_classification"] for row in listing_rows)),
        "paid_role_counts": dict(Counter(row["role"] for row in proof_rows)),
        "paid_family_counts": dict(Counter(row["custom_label_2"] for row in proof_rows)),
        "live_merchant_label_gate": live_status.get("gate_status", live_status.get("status", "UNKNOWN")),
        "live_merchant_campaign_filter_gate": live_status.get("campaign_filter_gate_status", live_status.get("gate_status", "UNKNOWN")),
        "live_merchant_full_label_gate": live_status.get("full_label_gate_status", "UNKNOWN"),
        "campaign_filter_creation_allowed": campaign_filters_ready,
        "label_1_2_3_subdivision_allowed": full_labels_ready,
        "merchant_supplemental_label_join_gate": live_status.get("full_label_gate_status", "UNKNOWN"),
        "merchant_supplemental_label_join_allowed": full_labels_ready,
        "live_merchant_label_detail": live_status,
        "purchase_conversion_value_gate": conversion_gate.get("purchase_conversion_value_gate_status", "UNKNOWN"),
        "purchase_conversion_value_gate_passed": purchase_conversion_value_ready,
        "purchase_conversion_value_detail": conversion_status,
        "ads_dry_run_actionable_allowed": ads_dry_run_actionable_allowed,
        "ads_dry_run_actionable_blockers": actionability_blockers,
        "google_ads_restart_allowed": False,
        "post_gate_ads_structure_mode": "DRY_RUN_ONLY_DO_NOT_RESTART_GOOGLE_ADS",
        "post_gate_ads_structure": POST_GATE_ADS_STRUCTURE,
        "decision": decision,
        "why": [
            "The exact local paid cohort is 780 active/sellable variant offer rows across 81 Shopify product listings.",
            "Most paid listings have mixed eligible and excluded variants, so Shopify product-level custom-label writes would overinclude unsafe variants.",
            "Variant-level Merchant Center supplemental labels are the correct control surface for paid eligibility.",
            label_status_reason,
        ],
    }

    files = {
        "paid_cohort_exact_780_rows": OUTPUT_DIR / "paid_cohort_exact_780_rows.csv",
        "product_listing_summary": OUTPUT_DIR / "product_listing_summary.csv",
        "item_group_plan": OUTPUT_DIR / "item_group_plan.csv",
        "family_style_group_plan": OUTPUT_DIR / "family_style_group_plan.csv",
        "image_plan": OUTPUT_DIR / "image_plan.csv",
        "paid_exclusion_table": OUTPUT_DIR / "paid_exclusion_table.csv",
        "post_gate_google_ads_dry_run_structure": OUTPUT_DIR / "post_gate_google_ads_dry_run_structure.csv",
        "summary": OUTPUT_DIR / "summary.json",
        "campaign_gate_report": OUTPUT_DIR / "campaign_gate_report.md",
    }

    write_csv(files["paid_cohort_exact_780_rows"], list(proof_rows[0].keys()), proof_rows)
    write_csv(files["product_listing_summary"], list(listing_rows[0].keys()), listing_rows)
    write_csv(files["item_group_plan"], list(item_group_rows[0].keys()), item_group_rows)
    write_csv(files["family_style_group_plan"], list(family_rows[0].keys()), family_rows)
    write_csv(files["image_plan"], list(image_rows[0].keys()), image_rows)
    write_csv(files["paid_exclusion_table"], list(exclusion_rows[0].keys()), exclusion_rows)
    write_csv(
        files["post_gate_google_ads_dry_run_structure"],
        ["campaign", "use_only_after", "required_exclusions"],
        POST_GATE_ADS_STRUCTURE,
    )
    summary["files"] = {key: str(path) for key, path in files.items()}
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files["campaign_gate_report"].write_text(render_report(summary), encoding="utf-8")
    return summary


def render_ads_structure_table(rows: list[dict[str, str]]) -> list[str]:
    table = [
        "| Campaign | Use only after | Required exclusions |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        table.append(
            f"| {row['campaign']} | {row['use_only_after']} | {row['required_exclusions']} |"
        )
    return table


def render_report(summary: dict[str, object]) -> str:
    live_detail = summary["live_merchant_label_detail"]
    conversion_detail = summary.get("purchase_conversion_value_detail", {})
    conversion_gate = conversion_detail.get("gate", {}) if isinstance(conversion_detail, dict) else {}
    ads_structure = summary.get("post_gate_ads_structure", POST_GATE_ADS_STRUCTURE)
    observed_rows = live_detail.get("observed_us_en_rows", []) if isinstance(live_detail, dict) else []
    label_mismatches = live_detail.get("observed_sample_label_mismatches", []) if isinstance(live_detail, dict) else []
    source_artifact = live_detail.get("source_artifact", "") if isinstance(live_detail, dict) else ""
    conversion_artifact = conversion_detail.get("source_artifact", "") if isinstance(conversion_detail, dict) else ""
    actionability_blockers = summary.get("ads_dry_run_actionable_blockers", [])
    if summary.get("merchant_supplemental_label_join_allowed"):
        next_action = (
            "Do not build or restart Ads from this packet. Produce current purchase conversion-value proof "
            "with non-zero purchase results/value before the dry-run structure becomes actionable."
        )
    else:
        next_action = (
            "Do not build or restart Ads from this packet. First fix the full Merchant Center supplemental label "
            "join and produce current purchase conversion-value proof with non-zero purchase results/value."
        )
    return "\n".join(
        [
            "# Google Shopping Campaign Gate Report",
            "",
            f"Generated: {summary['generated_at']}",
            "",
            "## Decision",
            "",
            f"`{summary['decision']}`",
            "",
            "The local paid cohort is real and verified. Do not enable or restart Google Ads from this packet.",
            f"Ads dry-run actionable allowed: `{summary.get('ads_dry_run_actionable_allowed')}`",
            "",
            "## Verified Local Cohort",
            "",
            f"- Paid offer rows: `{summary['paid_cohort_rows']}`",
            f"- Shopify product listings: `{summary['paid_unique_shopify_products']}`",
            f"- Proposed role/item groups: `{summary['paid_unique_proposed_item_groups']}`",
            f"- Reviewed offer rows: `{summary['all_master_rows_reviewed']}`",
            f"- Excluded/fix-before-paid offer rows: `{summary['excluded_rows']}`",
            f"- Paid listings with mixed eligible/excluded variants: `{summary['paid_products_with_mixed_eligible_and_excluded_variants']}`",
            f"- Product feed structure counts: `{summary['paid_product_feed_structure_counts']}`",
            f"- Role counts: `{summary['paid_role_counts']}`",
            f"- Product family counts: `{summary['paid_family_counts']}`",
            "",
            "## Live Merchant Label Gate",
            "",
            f"- Gate: `{summary['live_merchant_label_gate']}`",
            f"- Campaign filter gate: `{summary['live_merchant_campaign_filter_gate']}`",
            f"- Full label gate: `{summary['live_merchant_full_label_gate']}`",
            f"- Campaign filter creation allowed: `{summary['campaign_filter_creation_allowed']}`",
            f"- Label 1-3 subdivision allowed: `{summary['label_1_2_3_subdivision_allowed']}`",
            f"- Supplemental label join allowed: `{summary.get('merchant_supplemental_label_join_allowed')}`",
            f"- Observed US/en sample rows: `{json.dumps(observed_rows, sort_keys=True)}`",
            f"- Sample label mismatches: `{json.dumps(label_mismatches, sort_keys=True)}`",
            f"- Evidence artifact: `{source_artifact}`",
            "",
            "## Purchase Conversion-Value Gate",
            "",
            f"- Gate: `{summary.get('purchase_conversion_value_gate')}`",
            f"- Gate passed: `{summary.get('purchase_conversion_value_gate_passed')}`",
            f"- Purchase goal active: `{conversion_gate.get('purchase_goal_active', '')}`",
            f"- Purchase results in captured range: `{conversion_gate.get('purchase_goal_results', '')}`",
            f"- Target action: `{conversion_gate.get('target_conversion_action', '')}`",
            f"- Target primary/account-level: `{conversion_gate.get('target_is_primary_account_level_purchase_action', '')}`",
            f"- Target raw last conversion date: `{conversion_gate.get('target_last_conversion_date_raw', '')}`",
            f"- Evidence artifact: `{conversion_artifact}`",
            "",
            "## Ads Dry-Run Actionability",
            "",
            f"- Actionable allowed: `{summary.get('ads_dry_run_actionable_allowed')}`",
            f"- Blockers: `{json.dumps(actionability_blockers, sort_keys=True)}`",
            "",
            "## Post-Gate Google Ads Structure",
            "",
            "Do not restart Google Ads yet. This is a dry-run structure for use only after the named gates pass. It is not actionable while `ads_dry_run_actionable_allowed` is false.",
            "",
            *render_ads_structure_table(ads_structure),
            "",
            "## Standard Shopping Build Details",
            "",
            "- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`",
            "- Type: Standard Shopping only, USA only, paused on creation if later approved.",
            "- Do not use All Products, international inventory, unknown-margin products, fix-before-paid products, Limited products, or Not approved products.",
            "- Include only `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible` after Ads picker/readback proves those labels exist.",
            "- Product groups: use `custom_label_4 > custom_label_0` first. Add `custom_label_1..3` subdivisions only after the full-label gate passes and Ads dry-run actionability is true; until then use item IDs, product type, or the local item-group plan for reporting/exclusions.",
            "- Keep variant rows in Merchant Center for price, size, availability, and eligibility accuracy.",
            "",
            "## Important Feed Note",
            "",
            "Do not solve this by writing one Shopify product-level paid label onto every product listing. In this cohort, most paid listings mix eligible and excluded variants. Product-level writes would include variants the local clean-subset intentionally excluded.",
            "",
            "## Next Action",
            "",
            next_action,
        ]
    ) + "\n"


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
