#!/usr/bin/env python3
"""Preflight listing variant axes against vendor item evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set


ITEM_PATTERNS = {
    "Top": re.compile(r"(上衣|背心|衬衫|shirt|top|tank|tee|t-?shirt)", re.I),
    "Pants": re.compile(r"(裤|长裤|格子裤|pants|trousers)", re.I),
    "Shorts": re.compile(r"(短裤|shorts)", re.I),
    "Dress": re.compile(r"(裙|连衣裙|dress)", re.I),
    "Skirt": re.compile(r"(半裙|skirt)", re.I),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_from_payload(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        parts: List[str] = []
        for key in (
            "raw_detail_text",
            "raw_card_text",
            "title",
            "notes",
            "detail",
            "base_candidate",
            "candidates",
        ):
            if key in payload:
                parts.append(text_from_payload(payload[key]))
        if not parts:
            parts.extend(text_from_payload(value) for value in payload.values())
        return "\n".join(part for part in parts if part)
    if isinstance(payload, list):
        return "\n".join(text_from_payload(value) for value in payload)
    return ""


def detect_vendor_item_types(text: str) -> Set[str]:
    detected: Set[str] = set()
    for item_type, pattern in ITEM_PATTERNS.items():
        if pattern.search(text):
            detected.add(item_type)
    if "Shorts" in detected:
        detected.discard("Pants")
    return detected


def option_names(derived: Dict[str, Any]) -> List[str]:
    if "option_names" in derived:
        return [str(value) for value in derived["option_names"]]
    return [str(axis.get("name", "")) for axis in derived.get("option_axes", [])]


def chart_garments(chart: Sequence[Dict[str, Any]]) -> Set[str]:
    return {str(row.get("garment", "")).strip() for row in chart if str(row.get("garment", "")).strip()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fail before Shopify writes when vendor evidence contains multiple separate "
            "garment/item choices but derived options collapse them into Size/Color."
        )
    )
    parser.add_argument("--size-chart", required=True, type=Path)
    parser.add_argument("--derived", required=True, type=Path)
    parser.add_argument(
        "--vendor-evidence",
        action="append",
        type=Path,
        default=[],
        help="JSON or text files containing vendor/detail evidence. Can be passed more than once.",
    )
    parser.add_argument(
        "--require-type-for-items",
        default="Top,Pants,Shorts,Dress,Skirt",
        help="Comma-separated detected item types that require a Shopify Type option when mixed.",
    )
    parser.add_argument(
        "--primary-category",
        default="",
        help="Optional resolved PRIMARY_CATEGORY. Set/FamilySet listings must include the plain Sets tag.",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="Optional comma-separated Shopify tag list to validate for storefront collection routing.",
    )
    args = parser.parse_args()

    chart = load_json(args.size_chart)
    derived = load_json(args.derived)
    evidence_text = "\n".join(text_from_payload(load_json(path) if path.suffix == ".json" else path.read_text(encoding="utf-8")) for path in args.vendor_evidence)

    detected_types = detect_vendor_item_types(evidence_text)
    required_item_types = {value.strip() for value in args.require_type_for_items.split(",") if value.strip()}
    detected_required = detected_types & required_item_types
    garments = chart_garments(chart)
    names = option_names(derived)
    primary_category = str(args.primary_category).strip().lower()
    tags = {value.strip().lower() for value in args.tags.split(",") if value.strip()}

    errors: List[str] = []
    if len(detected_required) > 1 and "Type" not in names:
        errors.append(
            "vendor evidence contains separate item choices "
            f"{sorted(detected_required)}, but derived Shopify options are {names}; add Type x Size."
        )

    if len(garments) > 1 and "Type" not in names:
        errors.append(
            f"SIZE_CHART contains multiple garments {sorted(garments)}, but derived Shopify options are {names}."
        )

    if "Set" in garments and len(detected_required) > 1 and "Type" not in names:
        errors.append(
            "SIZE_CHART uses generic Set while vendor item evidence is separable; split rows into real garments."
        )

    if primary_category in {"sets", "familyset", "family set"} and "sets" not in tags:
        errors.append(
            "PRIMARY_CATEGORY is Sets/FamilySet, but Shopify tags are missing the exact plain tag `Sets`; "
            "add it so /collections/*/sets storefront pills have products."
        )

    if errors:
        print("VARIANT MODEL PREFLIGHT FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Variant model preflight passed: "
        f"options={names}; chart_garments={sorted(garments)}; vendor_items={sorted(detected_types)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
