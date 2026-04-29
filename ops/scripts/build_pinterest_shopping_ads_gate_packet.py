#!/usr/bin/env python3
"""Build a review-only Pinterest Shopping Ads gate packet.

The packet turns the existing clean paid cohort into a Pinterest-specific
post-gate structure without creating campaigns, product groups, budgets, or
ads. It intentionally fails closed until Pinterest-side feed, event, country,
and ROAS gates are verified.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path("dresslikemommy-growth-2026")
PAID_COHORT = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/"
    / "google_shopping_us_clean_subset_paid_eligible.csv"
)
PINTEREST_PACKET = ROOT / "02_AUDIT_PACKETS/2026-04-28_PINTEREST_PACKET_v1.md"
PINTEREST_POST_INGESTION = ROOT / "02_AUDIT_PACKETS/2026-04-29_PINTEREST_POST_INGESTION_RECHECK.md"
PINTEREST_EVENT_PLAN = ROOT / "03_LOCAL_ANALYSIS/2026-04-29-pinterest-event-quality-action-plan.md"
PINTEREST_TEST_ROWS = (
    ROOT
    / "01_EXPORTS_RAW/PINTEREST/2026-04-29_test_events_official_integration/"
    / "pinterest_test_events_saved_pass_rows.json"
)
PINTEREST_TEST_SUMMARY = (
    ROOT
    / "01_EXPORTS_RAW/PINTEREST/2026-04-29_test_events_official_integration/"
    / "controlled_pass_summary_saved.json"
)
OUTPUT_DIR = ROOT / "02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate"


TARGET_GROUPS = {
    "mommy_me": {
        "name": "DLM_PIN_US_SHOPPING_MOMMY_AND_ME",
        "label": "Mommy & Me",
    },
    "family_matching": {
        "name": "DLM_PIN_US_SHOPPING_FAMILY_MATCHING",
        "label": "Family Matching",
    },
    "pajamas": {
        "name": "DLM_PIN_US_SHOPPING_PAJAMAS",
        "label": "Pajamas",
    },
}


REQUIRED_PASS_FIELDS = (
    "image_status",
    "price_status",
    "availability_status",
    "shipping_policy_status",
    "return_policy_status",
    "pdp_status",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def clean(value: object) -> str:
    return str(value or "").strip()


def row_is_clean_for_candidate_pool(row: dict[str, str]) -> bool:
    return (
        row.get("paid_eligible") == "TRUE"
        and row.get("fix_before_paid") == "FALSE"
        and row.get("market") == "US"
        and bool(clean(row.get("cost")))
        and row.get("merchant_center_status") == "Approved"
        and row.get("merchant_center_destination") == "Shopping ads eligible"
        and all(row.get(field) == "PASS" for field in REQUIRED_PASS_FIELDS)
    )


def summarize_test_events() -> dict[str, object]:
    if not PINTEREST_TEST_ROWS.exists():
        return {
            "status": "NOT_CAPTURED",
            "source_artifact": str(PINTEREST_TEST_ROWS),
        }
    rows = json.loads(PINTEREST_TEST_ROWS.read_text(encoding="utf-8"))
    event_rows = []
    for row in rows:
        cells = row.get("cells") or []
        if len(cells) < 7 or cells[1] == "Event name":
            continue
        event_rows.append(
            {
                "event_name": clean(cells[1]),
                "issues": clean(cells[2]),
                "event_id_present": bool(clean(cells[3])),
                "setup_method": clean(cells[5]),
                "time_received": clean(cells[6]),
            }
        )
    summary = {
        "status": "TEST_EVENTS_CAPTURED",
        "source_artifact": str(PINTEREST_TEST_ROWS),
        "rows": len(event_rows),
        "event_counts": dict(Counter(row["event_name"] for row in event_rows)),
        "rows_with_visible_issues": sum(1 for row in event_rows if row["issues"]),
        "event_ids_present": sum(1 for row in event_rows if row["event_id_present"]),
        "setup_methods": dict(Counter(row["setup_method"] for row in event_rows if row["setup_method"])),
    }
    if PINTEREST_TEST_SUMMARY.exists():
        payload = json.loads(PINTEREST_TEST_SUMMARY.read_text(encoding="utf-8"))
        summary["controlled_test_stop"] = payload.get("safety_stop")
        summary["controlled_test_artifact"] = str(PINTEREST_TEST_SUMMARY)
    return summary


def build() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_paid_rows = read_csv(PAID_COHORT)

    candidate_rows: list[dict[str, object]] = []
    excluded_rows: list[dict[str, object]] = []

    for row in all_paid_rows:
        in_target_group = row.get("custom_label_2") in TARGET_GROUPS
        clean_candidate = row_is_clean_for_candidate_pool(row)
        base = {
            "pinterest_product_group": TARGET_GROUPS.get(row.get("custom_label_2"), {}).get("name", ""),
            "pinterest_group_label": TARGET_GROUPS.get(row.get("custom_label_2"), {}).get("label", ""),
            "shopify_product_id": row.get("shopify_product_id"),
            "shopify_variant_id": row.get("shopify_variant_id"),
            "merchant_center_item_id": row.get("merchant_center_item_id"),
            "title": row.get("title"),
            "product_url": row.get("product_url"),
            "image_url": row.get("image_url"),
            "price": row.get("price"),
            "cost": row.get("cost"),
            "gross_margin_percent": row.get("gross_margin_percent"),
            "max_cac": row.get("max_cac"),
            "product_family": row.get("product_family"),
            "custom_label_0": row.get("custom_label_0"),
            "custom_label_1": row.get("custom_label_1"),
            "custom_label_2": row.get("custom_label_2"),
            "custom_label_3": row.get("custom_label_3"),
            "custom_label_4": row.get("custom_label_4"),
            "market": row.get("market"),
            "merchant_center_status": row.get("merchant_center_status"),
            "merchant_center_destination": row.get("merchant_center_destination"),
            "image_status": row.get("image_status"),
            "price_status": row.get("price_status"),
            "availability_status": row.get("availability_status"),
            "shipping_policy_status": row.get("shipping_policy_status"),
            "return_policy_status": row.get("return_policy_status"),
            "pdp_status": row.get("pdp_status"),
            "pinterest_item_level_status": "NEEDS_PINTEREST_EXPORT_OR_UI_READBACK",
            "review_only_launch_status": "CANDIDATE_ONLY_NOT_LAUNCH_APPROVED",
        }
        if in_target_group and clean_candidate:
            candidate_rows.append(base)
        else:
            reason = []
            if not in_target_group:
                reason.append("outside_requested_pinterest_product_groups")
            if not clean_candidate:
                reason.append("failed_clean_candidate_gate")
            excluded_rows.append({**base, "exclusion_reason": ";".join(reason)})

    group_rows: list[dict[str, object]] = []
    for family_key, meta in TARGET_GROUPS.items():
        rows = [row for row in candidate_rows if row["custom_label_2"] == family_key]
        group_rows.append(
            {
                "pinterest_product_group": meta["name"],
                "user_facing_group": meta["label"],
                "target_country": "US_ONLY",
                "campaign_status": "DO_NOT_CREATE_OR_LAUNCH_YET",
                "source_filter": f"custom_label_2={family_key}; custom_label_0=paid_eligible; custom_label_4=us_test_ready",
                "candidate_offer_rows": len(rows),
                "unique_shopify_products": len({row["shopify_product_id"] for row in rows}),
                "unique_product_urls": len({row["product_url"] for row in rows}),
                "known_margin_offer_rows": sum(1 for row in rows if row["cost"]),
                "min_gross_margin_percent": min((float(row["gross_margin_percent"]) for row in rows), default=0),
                "max_gross_margin_percent": max((float(row["gross_margin_percent"]) for row in rows), default=0),
                "pdp_pass_rows": sum(1 for row in rows if row["pdp_status"] == "PASS"),
                "feed_pass_rows": sum(
                    1
                    for row in rows
                    if row["merchant_center_status"] == "Approved"
                    and row["merchant_center_destination"] == "Shopping ads eligible"
                    and all(row[field] == "PASS" for field in REQUIRED_PASS_FIELDS)
                ),
                "pinterest_item_level_gate": "BLOCKED_UNTIL_EXACT_PINTEREST_CATALOG_READBACK",
                "notes": "Use exact included offer IDs or an equivalent Pinterest catalog filter; never All Products.",
            }
        )

    event_summary = summarize_test_events()
    family_counts = Counter(row["custom_label_2"] for row in candidate_rows)
    margin_counts = Counter(row["custom_label_1"] for row in candidate_rows)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "PINTEREST_SHOPPING_ADS_GATE_PACKET_REVIEW_ONLY",
        "decision": "DO_NOT_CREATE_PINTEREST_ADS_OR_PRODUCT_GROUPS_YET",
        "campaign_creation_allowed": False,
        "account_status_context": {
            "operator_reported": [
                "Merchant approved",
                "Shopify connected",
                "Event Quality Score = Good setup",
                "Organic Last 30: 12.4K impressions, 317 engagements, 31 saves",
            ],
            "local_evidence_note": "Operator-reported status is promising, but this packet still requires current item-level Pinterest feed, event/CAPI payload, USA targeting, and ROAS gates before any ad launch.",
        },
        "source_files": {
            "paid_cohort": str(PAID_COHORT),
            "pinterest_packet": str(PINTEREST_PACKET),
            "pinterest_post_ingestion": str(PINTEREST_POST_INGESTION),
            "pinterest_event_plan": str(PINTEREST_EVENT_PLAN),
        },
        "all_paid_cohort_rows_reviewed": len(all_paid_rows),
        "candidate_offer_rows": len(candidate_rows),
        "candidate_unique_shopify_products": len({row["shopify_product_id"] for row in candidate_rows}),
        "candidate_unique_product_urls": len({row["product_url"] for row in candidate_rows}),
        "candidate_family_counts": dict(family_counts),
        "candidate_margin_counts": dict(margin_counts),
        "excluded_paid_cohort_rows": len(excluded_rows),
        "event_test_summary": event_summary,
        "hard_gates_before_create_ad": [
            "Do not click Pinterest Create an ad until the operator explicitly approves that exact action.",
            "Export or read back exact Pinterest catalog item status for all candidate offer IDs and exclude any warning, not-approved, limited, out-of-stock, or stale landing-page rows.",
            "Confirm the campaign/ad group country targeting is United States only before saving any draft.",
            "Confirm event-level health for PageVisit, ViewCategory, Search, AddToCart, InitiateCheckout, AddPaymentInfo, and Checkout/Purchase, including CAPI/tag deduplication where Pinterest exposes it.",
            "Keep required ROAS at or above 6.67 under the current paid-spend economics model; pause or do not launch if early spend cannot support that guardrail.",
            "Use only the three review-only product groups in this packet: Mommy & Me, Family Matching, and Pajamas.",
        ],
        "post_gate_campaign_structure": {
            "campaign_name": "DLM_PIN_US_SHOPPING_TEST_PAID_READY",
            "objective": "Shopping/catalog sales only",
            "country_targeting": "United States only",
            "status_on_creation": "Paused or draft only, never live without explicit operator launch approval",
            "product_groups": [row["pinterest_product_group"] for row in group_rows],
            "exclusions": [
                "All Products",
                "international targeting",
                "unknown-cost products",
                "out-of-stock variants",
                "unverified landing pages",
                "rows without clean Pinterest item-level catalog proof",
            ],
        },
    }

    files = {
        "candidate_offer_rows": OUTPUT_DIR / "pinterest_paid_ready_candidate_offer_rows.csv",
        "product_group_manifest": OUTPUT_DIR / "pinterest_product_group_manifest_review_only.csv",
        "excluded_offer_rows": OUTPUT_DIR / "pinterest_excluded_paid_cohort_rows.csv",
        "summary": OUTPUT_DIR / "summary.json",
        "gate_report": OUTPUT_DIR / "pinterest_shopping_ads_gate_report.md",
    }

    candidate_fields = [
        "pinterest_product_group",
        "pinterest_group_label",
        "shopify_product_id",
        "shopify_variant_id",
        "merchant_center_item_id",
        "title",
        "product_url",
        "image_url",
        "price",
        "cost",
        "gross_margin_percent",
        "max_cac",
        "product_family",
        "custom_label_0",
        "custom_label_1",
        "custom_label_2",
        "custom_label_3",
        "custom_label_4",
        "market",
        "merchant_center_status",
        "merchant_center_destination",
        "image_status",
        "price_status",
        "availability_status",
        "shipping_policy_status",
        "return_policy_status",
        "pdp_status",
        "pinterest_item_level_status",
        "review_only_launch_status",
    ]
    write_csv(files["candidate_offer_rows"], candidate_fields, candidate_rows)
    write_csv(files["product_group_manifest"], list(group_rows[0].keys()), group_rows)
    write_csv(files["excluded_offer_rows"], candidate_fields + ["exclusion_reason"], excluded_rows)
    summary["files"] = {key: str(path) for key, path in files.items()}
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files["gate_report"].write_text(render_report(summary, group_rows), encoding="utf-8")
    return summary


def render_report(summary: dict[str, object], group_rows: list[dict[str, object]]) -> str:
    lines = [
        "# Pinterest Shopping Ads Gate Report",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Decision",
        "",
        "`DO NOT CLICK CREATE AN AD, CREATE PRODUCT GROUPS, OR LAUNCH PINTEREST SHOPPING ADS YET.`",
        "",
        "Pinterest status is promising, but the launch gate is still closed because paid campaign data, exact item-level Pinterest catalog status, full event/CAPI/deduplication proof, USA-only targeting proof, and ROAS evidence are not complete.",
        "",
        "## Current Evidence",
        "",
        "- Existing authenticated capture showed Pinterest catalog and conversion tracking active, 0 campaigns, 0 ads, and $0.00 spend across captured 30/90/365-day windows.",
        "- Post-ingestion recheck showed English Warning 188 cleared and Shopify-side active Pinterest scope clean for compare-at, long description, and the shallow category fix, while non-English feed rechecks still needed another completion window.",
        "- Controlled Test Events captured PageVisit, ViewCategory, Search, and AddToCart rows with visible event IDs and no visible issue text; the pass stopped at checkout start and did not trigger AddPaymentInfo or Checkout/Purchase.",
        "- Operator-reported current context: merchant approved, Shopify connected, Event Quality Score = Good setup, and organic Last 30 activity of 12.4K impressions, 317 engagements, and 31 saves.",
        "",
        "## Review-Only Product Groups",
        "",
        "| Product group | Candidate offer rows | Shopify products | Feed/PDP pass rows | Pinterest item gate |",
        "|---|---:|---:|---:|---|",
    ]
    for row in group_rows:
        lines.append(
            "| {group} | {rows} | {products} | {feed_rows} | {gate} |".format(
                group=row["user_facing_group"],
                rows=row["candidate_offer_rows"],
                products=row["unique_shopify_products"],
                feed_rows=row["feed_pass_rows"],
                gate=row["pinterest_item_level_gate"],
            )
        )
    lines.extend(
        [
            "",
            "## Post-Gate Structure",
            "",
            "- Campaign: `DLM_PIN_US_SHOPPING_TEST_PAID_READY`.",
            "- Objective: Shopping/catalog sales only.",
            "- Country targeting: United States only.",
            "- Status: paused or draft only at creation; live launch needs separate explicit approval.",
            "- Product groups: Mommy & Me, Family Matching, and Pajamas only.",
            "- Include only rows with known cost, clean feed/PDP status, in-stock availability, `custom_label_0=paid_eligible`, and `custom_label_4=us_test_ready`.",
            "- Exclude All Products, unknown-cost rows, out-of-stock rows, unverified landing pages, international targeting, and anything without exact Pinterest catalog proof.",
            "",
            "## Gates Still Required",
            "",
            "1. Export or read back exact Pinterest catalog item status for the candidate offer IDs.",
            "2. Verify event-level health through AddPaymentInfo and Checkout/Purchase without creating a real paid order, and confirm CAPI/tag deduplication if Pinterest exposes it.",
            "3. Confirm the ad setup UI can target USA only before any draft is saved.",
            "4. Keep required ROAS at or above `6.67`; there is no Pinterest paid ROAS yet because spend is `$0.00`.",
            "",
            "## Output Files",
            "",
        ]
    )
    for label, path in sorted(summary["files"].items()):
        lines.append(f"- `{label}`: `{path}`")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
