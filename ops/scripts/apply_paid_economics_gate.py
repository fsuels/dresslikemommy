#!/usr/bin/env python3
"""Apply the paid-spend economics gate to local Shopify eligibility artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


DEFAULT_AOV_BENCHMARK = Decimal("63.25")
GATE_FIELDNAMES = [
    "aov_benchmark",
    "product_set_type",
    "marketing_margin_tier",
    "reliable_cost_basis",
    "paid_eligible",
    "economics_gate_status",
    "economics_gate_reasons",
    "economics_gate_exceptions",
]


@dataclass(frozen=True)
class ProductGateEvidence:
    product_set_type: str = ""
    marketing_margin_tier: str = ""


@dataclass(frozen=True)
class GateResult:
    paid_status: str
    gate_status: str
    reasons: tuple[str, ...]
    exceptions: tuple[str, ...]
    reliable_cost_basis: bool
    paid_eligible: bool


def parse_money(value: str | None) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def metafield_value(product: dict, namespace: str, key: str) -> str:
    nodes = (product.get("metafields") or {}).get("nodes", [])
    for metafield in nodes:
        if metafield.get("namespace") == namespace and metafield.get("key") == key:
            return str(metafield.get("value") or "")
    return ""


def load_product_gate_evidence(raw_export_path: Path) -> dict[str, ProductGateEvidence]:
    data = json.loads(raw_export_path.read_text(encoding="utf-8"))
    evidence: dict[str, ProductGateEvidence] = {}
    for product in data.get("products", []):
        product_id = str(product.get("legacyResourceId") or "")
        if not product_id:
            continue
        evidence[product_id] = ProductGateEvidence(
            product_set_type=normalize_text(
                metafield_value(product, "marketing", "product_set_type")
            ),
            marketing_margin_tier=normalize_text(
                metafield_value(product, "marketing", "margin_tier")
            ),
        )
    return evidence


def paid_gate_for_row(
    row: dict[str, str],
    evidence: ProductGateEvidence,
    aov_benchmark: Decimal = DEFAULT_AOV_BENCHMARK,
) -> GateResult:
    price = parse_money(row.get("price"))
    unit_cost = parse_money(row.get("unit_cost"))
    reliable_cost_basis = unit_cost is not None
    bundled_aov_basis = evidence.product_set_type == "set"
    repriced_aov_basis = price is not None and price >= aov_benchmark

    reasons: list[str] = []
    if price is None:
        reasons.append("UNKNOWN_PRICE")
    if not reliable_cost_basis:
        reasons.append("UNKNOWN_COST_NO_RELIABLE_COST_BASIS")
    if (price is None or price < aov_benchmark) and not (
        bundled_aov_basis or repriced_aov_basis or reliable_cost_basis
    ):
        reasons.append("LOW_AOV_NO_BUNDLE_REPRICE_OR_COST_BASIS")

    exceptions: list[str] = []
    if bundled_aov_basis:
        exceptions.append("BUNDLED_AOV_BASIS")
    if repriced_aov_basis:
        exceptions.append("REPRICED_AT_OR_ABOVE_AOV")
    if reliable_cost_basis:
        exceptions.append("RELIABLE_COST_BASIS")

    if reasons:
        return GateResult(
            paid_status="EXCLUDE_PAID",
            gate_status="BLOCKED",
            reasons=tuple(reasons),
            exceptions=tuple(exceptions),
            reliable_cost_basis=reliable_cost_basis,
            paid_eligible=False,
        )

    return GateResult(
        paid_status=row.get("paid_status") or "FIX_BEFORE_PAID",
        gate_status="PASSED_WITH_EXCEPTION" if exceptions else "PASSED",
        reasons=(),
        exceptions=tuple(exceptions),
        reliable_cost_basis=reliable_cost_basis,
        paid_eligible=True,
    )


def append_paid_reason(existing: str, gate_reasons: tuple[str, ...]) -> str:
    if not gate_reasons:
        return existing
    gate_reason = f"ECONOMICS_GATE:{'|'.join(gate_reasons)}"
    parts = [part for part in (existing or "").split(";") if part]
    parts = [part for part in parts if not part.startswith("ECONOMICS_GATE:")]
    return ";".join([gate_reason, *parts])


def apply_gate_to_eligibility_rows(
    rows: list[dict[str, str]],
    evidence_by_product_id: dict[str, ProductGateEvidence],
    aov_benchmark: Decimal = DEFAULT_AOV_BENCHMARK,
) -> list[dict[str, str]]:
    gated_rows: list[dict[str, str]] = []
    for row in rows:
        clean_row = {key: value for key, value in row.items() if key not in GATE_FIELDNAMES}
        evidence = evidence_by_product_id.get(clean_row.get("product_id", ""), ProductGateEvidence())
        gate = paid_gate_for_row(clean_row, evidence, aov_benchmark)
        clean_row["paid_status"] = gate.paid_status
        clean_row["paid_status_reasons"] = append_paid_reason(
            clean_row.get("paid_status_reasons", ""), gate.reasons
        )
        clean_row.update(
            {
                "aov_benchmark": str(aov_benchmark),
                "product_set_type": evidence.product_set_type,
                "marketing_margin_tier": evidence.marketing_margin_tier,
                "reliable_cost_basis": "TRUE" if gate.reliable_cost_basis else "FALSE",
                "paid_eligible": "TRUE" if gate.paid_eligible else "FALSE",
                "economics_gate_status": gate.gate_status,
                "economics_gate_reasons": "|".join(gate.reasons),
                "economics_gate_exceptions": "|".join(gate.exceptions),
            }
        )
        gated_rows.append(clean_row)
    return gated_rows


def update_custom_labels_rows(
    custom_label_rows: list[dict[str, str]],
    eligibility_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    status_by_variant = {
        row.get("variant_id", ""): row.get("paid_status", "")
        for row in eligibility_rows
        if row.get("variant_id")
    }
    updated: list[dict[str, str]] = []
    for row in custom_label_rows:
        updated_row = dict(row)
        variant_id = updated_row.get("variant_id", "")
        if variant_id in status_by_variant:
            updated_row["custom_label_4_paid_status"] = status_by_variant[variant_id]
        updated.append(updated_row)
    return updated


def write_artifact_custom_labels(
    path: Path,
    custom_label_rows: list[dict[str, str]],
) -> None:
    fieldnames = [
        "product_id",
        "handle",
        "variant_id",
        "sku",
        "custom_label_0",
        "custom_label_1",
        "custom_label_2",
        "custom_label_3",
        "custom_label_4",
    ]
    artifact_rows = []
    for row in custom_label_rows:
        artifact_rows.append(
            {
                "product_id": row.get("product_id", ""),
                "handle": row.get("handle", ""),
                "variant_id": row.get("variant_id", ""),
                "sku": row.get("sku", ""),
                "custom_label_0": row.get("custom_label_0_margin_tier", ""),
                "custom_label_1": row.get("custom_label_1_sales_velocity", ""),
                "custom_label_2": row.get("custom_label_2_inventory_status", ""),
                "custom_label_3": row.get("custom_label_3_price_bucket", ""),
                "custom_label_4": row.get("custom_label_4_paid_status", ""),
            }
        )
    write_csv(path, fieldnames, artifact_rows)


def build_exclude_rows(eligibility_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    exclude_rows = []
    for row in eligibility_rows:
        paid_status = row.get("paid_status", "")
        if paid_status in {"SCALE_PAID", "TEST_PAID", "ORGANIC_ONLY"}:
            continue
        exclude_rows.append(
            {
                "type": "product_variant",
                "handle": row.get("handle", ""),
                "variant_id": row.get("variant_id", ""),
                "reason": f"{paid_status}:{row.get('paid_status_reasons', '')}",
            }
        )
    return exclude_rows


def update_analysis_json(
    path: Path,
    eligibility_rows: list[dict[str, str]],
    custom_label_rows: list[dict[str, str]],
    aov_benchmark: Decimal,
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    eligibility_counts = Counter(row.get("paid_status", "") for row in eligibility_rows)
    data["eligibility_counts"] = dict(sorted(eligibility_counts.items()))

    data.setdefault("hard_financial_rules", {})
    data["hard_financial_rules"].update(
        {
            "aov_benchmark": str(aov_benchmark),
            "low_aov_policy": (
                "Products below the AOV benchmark are excluded from spend unless "
                "they are bundled, repriced, or backed by a reliable cost basis."
            ),
            "reliable_cost_basis_policy": (
                "Reliable cost basis means Shopify inventoryItem.unitCost is present. "
                "Product margin tiers are descriptive labels, not cost substitutes."
            ),
            "unknown_cost_policy": (
                "Unknown-cost variants are EXCLUDE_PAID and paid_eligible=FALSE."
            ),
        }
    )

    custom_label_counts: dict[str, dict[str, int]] = {}
    for fieldname in [
        "custom_label_0_margin_tier",
        "custom_label_1_sales_velocity",
        "custom_label_2_inventory_status",
        "custom_label_3_price_bucket",
        "custom_label_4_paid_status",
    ]:
        custom_label_counts[fieldname] = dict(
            sorted(Counter(row.get(fieldname, "") for row in custom_label_rows).items())
        )
    data["custom_label_counts"] = custom_label_counts

    data["economics_gate_counts"] = {
        "aov_benchmark": str(aov_benchmark),
        "blocked_variant_rows": sum(
            1 for row in eligibility_rows if row.get("economics_gate_status") == "BLOCKED"
        ),
        "passed_with_exception_variant_rows": sum(
            1
            for row in eligibility_rows
            if row.get("economics_gate_status") == "PASSED_WITH_EXCEPTION"
        ),
        "reliable_cost_basis_variant_rows": sum(
            1 for row in eligibility_rows if row.get("reliable_cost_basis") == "TRUE"
        ),
        "paid_eligible_variant_rows": sum(
            1 for row in eligibility_rows if row.get("paid_eligible") == "TRUE"
        ),
        "reason_counts": dict(
            sorted(
                Counter(
                    reason
                    for row in eligibility_rows
                    for reason in row.get("economics_gate_reasons", "").split("|")
                    if reason
                ).items()
            )
        ),
        "exception_counts": dict(
            sorted(
                Counter(
                    exception
                    for row in eligibility_rows
                    for exception in row.get("economics_gate_exceptions", "").split("|")
                    if exception
                ).items()
            )
        ),
    }

    limitation = (
        "Paid eligibility/custom-label artifacts apply the 2026-04-28 economics gate: "
        "unknown-cost variants are EXCLUDE_PAID with paid_eligible=FALSE, and "
        "low-AOV variants require bundled, repriced, or reliable-cost-basis evidence."
    )
    data.setdefault("limitations", [])
    if limitation not in data["limitations"]:
        data["limitations"].append(limitation)

    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def apply_paid_economics_gate(
    growth_root: Path,
    raw_export_path: Path,
    aov_benchmark: Decimal,
    dry_run: bool = False,
) -> dict[str, Counter]:
    analysis_dir = growth_root / "03_LOCAL_ANALYSIS"
    artifact_dir = growth_root / "02_AUDIT_PACKETS" / "2026-04-28_LOCAL_SHOPIFY_ARTIFACTS"
    eligibility_path = analysis_dir / "2026-04-28_LOCAL_SHOPIFY_product_eligibility.csv"
    custom_labels_path = analysis_dir / "2026-04-28_LOCAL_SHOPIFY_custom_labels.csv"
    exclude_paid_path = analysis_dir / "2026-04-28_LOCAL_SHOPIFY_exclude_from_paid.csv"
    analysis_json_path = analysis_dir / "2026-04-28_LOCAL_SHOPIFY_ANALYSIS_v1.json"
    artifact_custom_labels_path = artifact_dir / "custom_labels.csv"

    evidence = load_product_gate_evidence(raw_export_path)
    eligibility_fields, eligibility_rows = read_csv(eligibility_path)
    custom_label_fields, custom_label_rows = read_csv(custom_labels_path)

    gated_eligibility_rows = apply_gate_to_eligibility_rows(
        eligibility_rows, evidence, aov_benchmark
    )
    gated_custom_label_rows = update_custom_labels_rows(
        custom_label_rows, gated_eligibility_rows
    )
    exclude_rows = build_exclude_rows(gated_eligibility_rows)

    before = Counter(row.get("paid_status", "") for row in eligibility_rows)
    after = Counter(row.get("paid_status", "") for row in gated_eligibility_rows)
    gate_reasons = Counter(
        reason
        for row in gated_eligibility_rows
        for reason in row.get("economics_gate_reasons", "").split("|")
        if reason
    )

    if not dry_run:
        base_fields = [field for field in eligibility_fields if field not in GATE_FIELDNAMES]
        write_csv(eligibility_path, [*base_fields, *GATE_FIELDNAMES], gated_eligibility_rows)
        write_csv(custom_labels_path, custom_label_fields, gated_custom_label_rows)
        write_csv(
            exclude_paid_path,
            ["type", "handle", "variant_id", "reason"],
            exclude_rows,
        )
        write_artifact_custom_labels(artifact_custom_labels_path, gated_custom_label_rows)
        update_analysis_json(
            analysis_json_path,
            gated_eligibility_rows,
            gated_custom_label_rows,
            aov_benchmark,
        )

    return {"before": before, "after": after, "gate_reasons": gate_reasons}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply the paid-spend economics gate to local Shopify CSV artifacts."
    )
    parser.add_argument(
        "--growth-root",
        type=Path,
        default=Path("dresslikemommy-growth-2026"),
        help="Growth workspace root.",
    )
    parser.add_argument(
        "--raw-export",
        type=Path,
        default=Path(
            "dresslikemommy-growth-2026/01_EXPORTS_RAW/SHOPIFY/"
            "2026-04-28_LOCAL_SHOPIFY_EXPORT_raw.json"
        ),
        help="Raw Shopify export JSON with product marketing metafields.",
    )
    parser.add_argument(
        "--aov-benchmark",
        default=str(DEFAULT_AOV_BENCHMARK),
        help="AOV benchmark used for low-AOV gating.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    aov_benchmark = Decimal(str(args.aov_benchmark))
    result = apply_paid_economics_gate(
        growth_root=args.growth_root,
        raw_export_path=args.raw_export,
        aov_benchmark=aov_benchmark,
        dry_run=args.dry_run,
    )
    print("before", dict(sorted(result["before"].items())))
    print("after", dict(sorted(result["after"].items())))
    print("gate_reasons", dict(sorted(result["gate_reasons"].items())))


if __name__ == "__main__":
    main()
