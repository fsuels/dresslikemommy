#!/usr/bin/env python3
"""Build the Phase 7 final launch gate packet.

This is a read-only aggregator over the existing launch evidence. It fails
closed unless every required gate has explicit YES proof.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path("dresslikemommy-growth-2026")
OUTPUT_DIR = ROOT / "02_AUDIT_PACKETS/2026-04-29-final-launch-gate"

PAID_COHORT_LOCAL = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/"
    / "google_shopping_us_clean_subset_paid_eligible.csv"
)
PAID_COHORT_EXACT = (
    ROOT
    / "02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/"
    / "paid_cohort_exact_780_rows.csv"
)
GOOGLE_CAMPAIGN_GATE = (
    ROOT / "02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/summary.json"
)
PINTEREST_GATE = (
    ROOT / "02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/summary.json"
)
MARGIN_CAC_PACKET = (
    ROOT / "02_AUDIT_PACKETS/2026-04-29-shopify-margin-cac-export-pack/summary.json"
)
NEEDS_DATA_ECONOMICS = (
    ROOT / "02_AUDIT_PACKETS/2026-04-29-needs-data-economics-reconciliation/summary.json"
)
MERCHANT_CLEAN_LABEL_UPLOAD = (
    ROOT / "02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/summary.json"
)
LOCALIZATION_DEFECTS = (
    ROOT / "03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_localization_defects.csv"
)
PUBLIC_THEME_VALIDATION = (
    ROOT / "03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_public_theme_validation.json"
)


GATE_REQUIREMENTS = [
    {
        "gate": "Measurement >=85",
        "required_proof": (
            "Purchase events record transaction_id, value, currency; no duplicates; "
            "Google Ads/Pinterest conversion health verified."
        ),
    },
    {
        "gate": "Feed >=85",
        "required_proof": (
            "Item-level diagnostics clean for target products; country eligibility verified."
        ),
    },
    {
        "gate": "Website >=80",
        "required_proof": "Target landing pages READY_FOR_PAID.",
    },
    {
        "gate": "Localization >=85",
        "required_proof": "Target country/language passes rendered QA.",
    },
    {
        "gate": "Product economics",
        "required_proof": (
            "Unit cost, margin tier, inventory, feed status, and paid_status known."
        ),
    },
    {
        "gate": "Country economics",
        "required_proof": (
            "Country revenue, conversion, shipping/returns, localization, and paid "
            "eligibility proven."
        ),
    },
    {
        "gate": "Paid efficiency",
        "required_proof": "ROAS >= 6.67 and CAC <= AOV x 0.15.",
    },
    {
        "gate": "Blended spend",
        "required_proof": "Total marketing spend <= 15% of revenue.",
    },
]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def decimal_or_zero(value: object) -> Decimal:
    try:
        return Decimal(clean(value) or "0")
    except InvalidOperation:
        return Decimal("0")


def money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def source_list(paths: list[Path]) -> str:
    return "; ".join(str(path) for path in paths)


def gate_result(
    gate: str,
    answer: str,
    current_status: str,
    evidence: str,
    blocking_gap: str,
    next_best_action: str,
    source_artifacts: list[Path],
) -> dict[str, object]:
    requirement = next(item for item in GATE_REQUIREMENTS if item["gate"] == gate)
    return {
        "gate": gate,
        "required_proof": requirement["required_proof"],
        "answer": answer,
        "current_status": current_status,
        "evidence": evidence,
        "blocking_gap": blocking_gap,
        "next_best_action": next_best_action,
        "source_artifacts": source_list(source_artifacts),
    }


def all_rows_have(rows: list[dict[str, str]], field: str) -> bool:
    return bool(rows) and all(clean(row.get(field)) for row in rows)


def count_not_equal(rows: list[dict[str, str]], field: str, expected: str) -> int:
    return sum(1 for row in rows if clean(row.get(field)) != expected)


def product_economics_result(
    paid_local_rows: list[dict[str, str]],
    paid_exact_rows: list[dict[str, str]],
) -> tuple[str, str, str, str]:
    missing = {
        "unit_cost": sum(1 for row in paid_exact_rows if not clean(row.get("unit_cost"))),
        "margin_tier": sum(1 for row in paid_exact_rows if not clean(row.get("margin_tier"))),
        "inventory": sum(1 for row in paid_exact_rows if not clean(row.get("inventory"))),
        "paid_status": count_not_equal(paid_local_rows, "custom_label_4", "us_test_ready"),
        "merchant_center_status": count_not_equal(paid_local_rows, "merchant_center_status", "Approved"),
        "merchant_center_destination": count_not_equal(
            paid_local_rows, "merchant_center_destination", "Shopping ads eligible"
        ),
    }
    answer = "YES" if paid_local_rows and paid_exact_rows and all(value == 0 for value in missing.values()) else "NO"
    status = "PASS_LOCAL_PAID_COHORT" if answer == "YES" else "BLOCKED_PRODUCT_ECONOMICS_GAPS"
    evidence = (
        f"{len(paid_exact_rows)} target offer rows checked; missing counts: "
        + ", ".join(f"{key}={value}" for key, value in missing.items())
        + "."
    )
    blocking_gap = (
        "None for the current local paid cohort. This does not override the feed, "
        "measurement, country, or live-label gates."
        if answer == "YES"
        else "One or more target offer rows are missing economics/feed fields."
    )
    next_action = (
        "Keep using the exact target cohort; rerun this packet after feed or product changes."
        if answer == "YES"
        else "Backfill missing cost, margin, inventory, feed, and paid-status fields, then rebuild."
    )
    return answer, status, evidence, blocking_gap, next_action


def build() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    google_gate = read_json(GOOGLE_CAMPAIGN_GATE)
    pinterest_gate = read_json(PINTEREST_GATE)
    margin_packet = read_json(MARGIN_CAC_PACKET)
    economics_packet = read_json(NEEDS_DATA_ECONOMICS)
    merchant_upload = read_json(MERCHANT_CLEAN_LABEL_UPLOAD)
    public_theme_validation = read_json(PUBLIC_THEME_VALIDATION)
    paid_local_rows = read_csv(PAID_COHORT_LOCAL)
    paid_exact_rows = read_csv(PAID_COHORT_EXACT)
    localization_rows = read_csv(LOCALIZATION_DEFECTS)

    pinterest_events = pinterest_gate.get("event_test_summary") or {}
    pinterest_event_counts = pinterest_events.get("event_counts") or {}
    google_label_gate = clean(google_gate.get("live_merchant_label_gate") or "UNKNOWN")
    ad_spend_status = economics_packet.get("ad_spend_status") or {}
    remaining_economics_blockers = economics_packet.get("remaining_hard_blockers") or []
    localization_severity_counts = Counter(clean(row.get("severity")) for row in localization_rows)

    local_feed_pass_rows = sum(
        1
        for row in paid_local_rows
        if row.get("merchant_center_status") == "Approved"
        and row.get("merchant_center_destination") == "Shopping ads eligible"
        and row.get("market") == "US"
        and all(
            row.get(field) == "PASS"
            for field in (
                "image_status",
                "price_status",
                "availability_status",
                "shipping_policy_status",
                "return_policy_status",
                "pdp_status",
            )
        )
    )
    local_pdp_pass_rows = sum(1 for row in paid_local_rows if row.get("pdp_status") == "PASS")

    product_answer, product_status, product_evidence, product_gap, product_next = product_economics_result(
        paid_local_rows, paid_exact_rows
    )

    revenue = decimal_or_zero(margin_packet.get("observed_total_revenue"))
    cap_rate = decimal_or_zero(margin_packet.get("marketing_cap_rate"))
    blended_cap = revenue * cap_rate

    gate_rows = [
        gate_result(
            "Measurement >=85",
            "NO",
            "BLOCKED_PURCHASE_PROOF_MISSING",
            (
                f"Pinterest controlled test rows={pinterest_events.get('rows', 0)} with event counts "
                f"{dict(pinterest_event_counts)}; controlled stop="
                f"{clean(pinterest_events.get('controlled_test_stop')) or 'not captured'}. "
                "Google Ads purchase value/transaction proof is not present in repo evidence."
            ),
            (
                "No captured purchase/payment event proves transaction_id, value, and currency; "
                "deduplication proof is also absent."
            ),
            (
                "Capture Google Ads and Pinterest conversion health through payment/purchase events "
                "and prove event/CAPI or tag dedupe before launch."
            ),
            [PINTEREST_GATE, NEEDS_DATA_ECONOMICS],
        ),
        gate_result(
            "Feed >=85",
            "NO",
            "BLOCKED_LIVE_ITEM_READBACK_MISSING",
            (
                f"Local clean cohort has {local_feed_pass_rows}/{len(paid_local_rows)} US rows passing "
                f"local feed/PDP fields; Merchant clean-label upload prepared "
                f"{merchant_upload.get('upload_rows', 0)} matched rows. Google live label gate is "
                f"{google_label_gate}; Pinterest item-level catalog readback is still required."
            ),
            (
                "Exact live item-level diagnostics and country eligibility are not fully proven for "
                "the target Google/Pinterest launch set."
            ),
            (
                "Finish Merchant Center label join/readback and export exact Pinterest catalog item "
                "status for target offer IDs."
            ),
            [PAID_COHORT_LOCAL, GOOGLE_CAMPAIGN_GATE, PINTEREST_GATE, MERCHANT_CLEAN_LABEL_UPLOAD],
        ),
        gate_result(
            "Website >=80",
            "NO",
            "BLOCKED_READY_FOR_PAID_ARTIFACT_MISSING",
            (
                f"Local clean cohort has {local_pdp_pass_rows}/{len(paid_local_rows)} PDP rows marked "
                "PASS, but there is no final target landing-page artifact marking pages READY_FOR_PAID."
            ),
            "Target landing pages are not explicitly approved as READY_FOR_PAID.",
            (
                "Run rendered landing-page QA for the exact target URLs and write a READY_FOR_PAID "
                "allowlist before enabling paid traffic."
            ),
            [PAID_COHORT_LOCAL, PUBLIC_THEME_VALIDATION],
        ),
        gate_result(
            "Localization >=85",
            "NO",
            "BLOCKED_RENDERED_LOCALIZATION_QA_MISSING",
            (
                f"Localization defect export has severity counts {dict(localization_severity_counts)} "
                "and prior public validation found live translation-missing text on a Spanish PDP. "
                f"Rendered QA artifact present={bool(public_theme_validation)}."
            ),
            "Target country/language rendered QA has not passed; published locale defects remain high.",
            (
                "Restrict paid launch to locales with rendered QA proof, or fix/verify target locale "
                "translations before launch."
            ),
            [LOCALIZATION_DEFECTS, PUBLIC_THEME_VALIDATION],
        ),
        gate_result(
            "Product economics",
            product_answer,
            product_status,
            product_evidence,
            product_gap,
            product_next,
            [PAID_COHORT_EXACT, PAID_COHORT_LOCAL, MARGIN_CAC_PACKET],
        ),
        gate_result(
            "Country economics",
            "NO",
            "BLOCKED_COUNTRY_ECONOMICS_INCOMPLETE",
            (
                f"Known remaining hard blockers: {remaining_economics_blockers}. "
                f"Ad spend status: {ad_spend_status}."
            ),
            (
                "Country revenue/conversion, actual shipping/returns cost, localization, and paid "
                "eligibility are not all proven together."
            ),
            (
                "Collect full Google Ads/GA4/Meta exports plus actual shipping/returns costs and "
                "country-level paid eligibility proof."
            ),
            [NEEDS_DATA_ECONOMICS, MARGIN_CAC_PACKET],
        ),
        gate_result(
            "Paid efficiency",
            "NO",
            "BLOCKED_ROAS_CAC_NOT_COMPUTABLE",
            (
                f"Target ROAS floor={clean(margin_packet.get('target_roas_floor')) or 'unknown'}; "
                f"observed AOV={clean(margin_packet.get('observed_aov')) or 'unknown'}; "
                f"max CAC={clean(margin_packet.get('max_cac_observed_aov')) or 'unknown'}. "
                f"Ad spend status: {ad_spend_status}."
            ),
            "Paid conversion value and spend exports are incomplete, so ROAS/CAC cannot be proven.",
            (
                "Import complete platform spend and conversion-value exports, then compute ROAS and "
                "CAC against the 6.67 / AOV x 0.15 guardrails."
            ),
            [MARGIN_CAC_PACKET, NEEDS_DATA_ECONOMICS],
        ),
        gate_result(
            "Blended spend",
            "NO",
            "BLOCKED_TOTAL_MARKETING_SPEND_INCOMPLETE",
            (
                f"Observed revenue={money(revenue)}; 15% blended marketing cap={money(blended_cap)}. "
                f"Spend evidence is incomplete: {ad_spend_status}."
            ),
            "Total marketing spend is not fully exported across all platforms.",
            (
                "Collect all paid platform spend for the same revenue window and verify total spend "
                "is at or below 15% of revenue."
            ),
            [MARGIN_CAC_PACKET, NEEDS_DATA_ECONOMICS],
        ),
    ]

    answer_counts = Counter(clean(row["answer"]) for row in gate_rows)
    launch_allowed = all(row["answer"] == "YES" for row in gate_rows)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "PHASE7_FINAL_LAUNCH_GATE_READ_ONLY",
        "launch_allowed": launch_allowed,
        "launch_decision": "APPROVED" if launch_allowed else "BLOCKED",
        "rule": "Launch is blocked unless every gate answer is YES.",
        "answer_counts": dict(answer_counts),
        "gates_required": len(GATE_REQUIREMENTS),
        "gates_yes": answer_counts.get("YES", 0),
        "gates_no": answer_counts.get("NO", 0),
        "target_offer_rows": len(paid_exact_rows),
        "local_clean_feed_pass_rows": local_feed_pass_rows,
        "source_files": {
            "paid_cohort_local": str(PAID_COHORT_LOCAL),
            "paid_cohort_exact": str(PAID_COHORT_EXACT),
            "google_campaign_gate": str(GOOGLE_CAMPAIGN_GATE),
            "pinterest_gate": str(PINTEREST_GATE),
            "margin_cac_packet": str(MARGIN_CAC_PACKET),
            "needs_data_economics": str(NEEDS_DATA_ECONOMICS),
            "merchant_clean_label_upload": str(MERCHANT_CLEAN_LABEL_UPLOAD),
            "localization_defects": str(LOCALIZATION_DEFECTS),
            "public_theme_validation": str(PUBLIC_THEME_VALIDATION),
        },
        "gate_results": gate_rows,
    }

    files = {
        "summary": OUTPUT_DIR / "summary.json",
        "checklist": OUTPUT_DIR / "phase7_launch_gate_checklist.csv",
        "report": OUTPUT_DIR / "phase7_final_launch_gate_report.md",
    }
    summary["files"] = {key: str(path) for key, path in files.items()}
    write_csv(
        files["checklist"],
        [
            "gate",
            "required_proof",
            "answer",
            "current_status",
            "evidence",
            "blocking_gap",
            "next_best_action",
            "source_artifacts",
        ],
        gate_rows,
    )
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files["report"].write_text(render_report(summary), encoding="utf-8")
    return summary


def render_report(summary: dict[str, object]) -> str:
    lines = [
        "# Phase 7 Final Launch Gate",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Launch Decision",
        "",
        f"Launch decision: `{summary['launch_decision']}`",
        "",
        "Launch is blocked unless every gate answer is `YES`.",
        "",
        f"- YES gates: `{summary['gates_yes']}`",
        f"- NO gates: `{summary['gates_no']}`",
        f"- Target offer rows checked: `{summary['target_offer_rows']}`",
        f"- Local clean feed/PDP pass rows: `{summary['local_clean_feed_pass_rows']}`",
        "",
        "## Gate Results",
        "",
        "| Gate | Answer | Current status | Required proof | Blocking gap |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in summary["gate_results"]:
        lines.append(
            "| {gate} | {answer} | {status} | {proof} | {gap} |".format(
                gate=row["gate"],
                answer=row["answer"],
                status=row["current_status"],
                proof=row["required_proof"],
                gap=row["blocking_gap"],
            )
        )
    lines.extend(["", "## Next Actions", ""])
    for row in summary["gate_results"]:
        if row["answer"] != "YES":
            lines.append(f"- `{row['gate']}`: {row['next_best_action']}")
    lines.extend(["", "## Output Files", ""])
    for label, path in sorted(summary["files"].items()):
        lines.append(f"- `{label}`: `{path}`")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, sort_keys=True))
