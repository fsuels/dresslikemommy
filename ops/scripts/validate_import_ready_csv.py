#!/usr/bin/env python3
"""Validate Shopify import-ready product CSVs before import."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

ROW_HANDLE = "Handle"
ROW_STATUS = "Status"
ROW_PUBLISHED = "Published"
ROW_TAGS = "Tags"
ROW_IMAGE_SRC = "Image Src"
ROW_IMAGE_ALT = "Image Alt Text"
ROW_IMAGE_POSITION = "Image Position"
ROW_VARIANT_IMAGE = "Variant Image"
ROW_OPTION1_VALUE = "Option1 Value"
ROW_OPTION2_VALUE = "Option2 Value"
ROW_OPTION3_VALUE = "Option3 Value"
ROW_VARIANT_SKU = "Variant SKU"
ROW_VARIANT_BARCODE = "Variant Barcode"
ROW_GOOGLE_MPN = "Google Shopping / MPN"
ROW_GOOGLE_CUSTOM_PRODUCT = "Google Shopping / Custom Product"
ROW_GOOGLE_CONDITION = "Google Shopping / Condition"
ROW_GOOGLE_GENDER = "Google Shopping / Gender"
ROW_GOOGLE_AGE_GROUP = "Google Shopping / Age Group"

PRODUCT_SEO_TITLE = "SEO Title"
PRODUCT_SEO_DESCRIPTION = "SEO Description"
PRODUCT_GOOGLE_CATEGORY = "Google Shopping / Google Product Category"
PRODUCT_CATEGORY1 = "Category1 (product.metafields.custom.category1)"
PRODUCT_SUBCATEGORY = "SubCategory (product.metafields.custom.subcategory)"
PRODUCT_SUBCATEGORY2 = "SubCategory2 (product.metafields.custom.subcategory2)"
PRODUCT_TYPE = "Type (product.metafields.custom.type)"
PRODUCT_STYLE = "Style (product.metafields.custom.style)"
PRODUCT_PATTERN = "Pattern (product.metafields.custom.pattern)"
PRODUCT_DISCOVERY_COMPLEMENTARY = (
    "Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products)"
)
PRODUCT_DISCOVERY_RELATED_SETTINGS = (
    "Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display)"
)
PRODUCT_DISCOVERY_RELATED = (
    "Related products (product.metafields.shopify--discovery--product_recommendation.related_products)"
)
PRODUCT_SEARCH_BOOSTS = (
    "Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries)"
)
PRODUCT_GOOGLE_CUSTOM_METAFIELD = (
    "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)"
)
PRODUCT_SHOPIFY_AGE_GROUP = "Age group (product.metafields.shopify.age-group)"
PRODUCT_SHOPIFY_COLOR = "Color (product.metafields.shopify.color-pattern)"

ACTIVE_STATUS = "active"
REQUIRED_TAG_PREFIXES = (
    "category1:",
    "subcategory:",
    "subcategory2:",
    "type:",
    "style:",
    "pattern:",
)
VALID_RELATED_SETTINGS = {"only manual", "manual", "automatic"}
VALID_GTIN_LENGTHS = {8, 12, 13, 14}
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
VALID_GENDER_VALUES = {"female", "male", "unisex"}
VALID_AGE_GROUP_VALUES = {"newborn", "infant", "toddler", "kids", "adult"}
HANDLE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    samples: Sequence[str]


def clean(value: str) -> str:
    return (value or "").strip()


def normalized_key(value: str) -> str:
    return clean(value).lower()


def parse_bool_true(value: str) -> bool:
    return normalized_key(value) in {"true", "1", "yes", "y"}


def is_variant_row(row: Dict[str, str]) -> bool:
    return bool(
        clean(row.get(ROW_VARIANT_SKU, ""))
        or clean(row.get(ROW_OPTION1_VALUE, ""))
        or clean(row.get(ROW_OPTION2_VALUE, ""))
        or clean(row.get(ROW_OPTION3_VALUE, ""))
    )


def split_csv_tokens(value: str) -> List[str]:
    tokens: List[str] = []
    seen = set()
    for raw in clean(value).split(","):
        token = clean(raw)
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        tokens.append(token)
    return tokens


def first_non_blank(rows: Sequence[Dict[str, str]], column: str) -> str:
    for row in rows:
        value = clean(row.get(column, ""))
        if value:
            return value
    return ""


def image_extension_from_url(url: str) -> str:
    raw = clean(url)
    if not raw:
        return ""
    base = raw.split("?", 1)[0].lower()
    name = base.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return f".{name.rsplit('.', 1)[-1]}"


def is_supported_image_url(url: str) -> bool:
    extension = image_extension_from_url(url)
    return bool(extension and extension in SUPPORTED_IMAGE_EXTENSIONS)


def collect_target_handles(rows: Sequence[Dict[str, str]], all_statuses: bool) -> List[str]:
    statuses_by_handle: Dict[str, str] = {}
    for row in rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if not handle:
            continue
        incoming = clean(row.get(ROW_STATUS, ""))
        existing = statuses_by_handle.get(handle, "")
        if normalized_key(existing) == ACTIVE_STATUS:
            continue
        statuses_by_handle[handle] = incoming or existing

    if all_statuses:
        return sorted(statuses_by_handle.keys())

    return sorted(
        handle
        for handle, status in statuses_by_handle.items()
        if normalized_key(status) == ACTIVE_STATUS
    )


def add_finding(
    findings: List[Finding],
    severity: str,
    code: str,
    message: str,
    samples: Iterable[str],
    max_samples: int,
) -> None:
    sample_list = [sample for sample in samples if clean(sample)]
    if len(sample_list) > max_samples:
        sample_list = sample_list[:max_samples]
    findings.append(
        Finding(
            severity=severity,
            code=code,
            message=message,
            samples=sample_list,
        )
    )


def write_report(
    path: Path,
    input_path: Path,
    row_count: int,
    target_handles: Sequence[str],
    findings: Sequence[Finding],
) -> None:
    errors = [finding for finding in findings if finding.severity == "ERROR"]
    warnings = [finding for finding in findings if finding.severity == "WARN"]

    lines: List[str] = []
    lines.append("# Import-Ready CSV Validation Report")
    lines.append("")
    lines.append(f"Input file: `{input_path}`")
    lines.append(f"Total rows: `{row_count}`")
    lines.append(f"Target handles: `{len(target_handles)}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Errors: `{len(errors)}`")
    lines.append(f"- Warnings: `{len(warnings)}`")
    lines.append("")

    if not findings:
        lines.append("No issues found.")
    else:
        lines.append("## Findings")
        lines.append("")
        for finding in findings:
            lines.append(f"- [{finding.severity}] `{finding.code}`: {finding.message}")
            if finding.samples:
                lines.append(f"  Samples: {', '.join(finding.samples)}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Shopify import-ready CSV")
    parser.add_argument(
        "--input",
        default="products_export_1 2_IMPORT_READY.csv",
        help="Input CSV path (default: products_export_1 2_IMPORT_READY.csv)",
    )
    parser.add_argument(
        "--output",
        default="ops/import_ready_validation_report.md",
        help="Output markdown report path (default: ops/import_ready_validation_report.md)",
    )
    parser.add_argument(
        "--all-statuses",
        action="store_true",
        help="Validate all handles regardless of Status. Default is active only.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=10,
        help="Max sample items per finding (default: 10)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row")
        fieldnames = list(reader.fieldnames)

    required_columns = (
        ROW_HANDLE,
        ROW_STATUS,
        ROW_PUBLISHED,
        ROW_TAGS,
        ROW_IMAGE_SRC,
        ROW_IMAGE_ALT,
        ROW_IMAGE_POSITION,
        ROW_VARIANT_IMAGE,
        ROW_VARIANT_SKU,
        ROW_VARIANT_BARCODE,
        ROW_GOOGLE_MPN,
        ROW_GOOGLE_CUSTOM_PRODUCT,
        ROW_GOOGLE_CONDITION,
        ROW_GOOGLE_GENDER,
        ROW_GOOGLE_AGE_GROUP,
        PRODUCT_SEO_TITLE,
        PRODUCT_SEO_DESCRIPTION,
        PRODUCT_GOOGLE_CATEGORY,
        PRODUCT_SHOPIFY_AGE_GROUP,
        PRODUCT_SHOPIFY_COLOR,
        PRODUCT_CATEGORY1,
        PRODUCT_SUBCATEGORY,
        PRODUCT_SUBCATEGORY2,
        PRODUCT_TYPE,
        PRODUCT_STYLE,
        PRODUCT_PATTERN,
        PRODUCT_DISCOVERY_COMPLEMENTARY,
        PRODUCT_DISCOVERY_RELATED_SETTINGS,
        PRODUCT_DISCOVERY_RELATED,
        PRODUCT_SEARCH_BOOSTS,
        PRODUCT_GOOGLE_CUSTOM_METAFIELD,
    )
    for required in required_columns:
        if required not in fieldnames:
            raise ValueError(f"Missing expected CSV column: {required}")

    target_handles = collect_target_handles(rows, all_statuses=args.all_statuses)
    target_set = set(target_handles)

    rows_by_handle: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    all_handles: Set[str] = set()
    for row in rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if not handle:
            continue
        rows_by_handle[handle].append(row)
        all_handles.add(handle)

    findings: List[Finding] = []

    required_product_fields = (
        PRODUCT_SEO_TITLE,
        PRODUCT_SEO_DESCRIPTION,
        PRODUCT_GOOGLE_CATEGORY,
        PRODUCT_CATEGORY1,
        PRODUCT_SUBCATEGORY,
        PRODUCT_SUBCATEGORY2,
        PRODUCT_TYPE,
        PRODUCT_STYLE,
        PRODUCT_PATTERN,
        PRODUCT_DISCOVERY_COMPLEMENTARY,
        PRODUCT_DISCOVERY_RELATED_SETTINGS,
        PRODUCT_DISCOVERY_RELATED,
        PRODUCT_SEARCH_BOOSTS,
    )

    for field in required_product_fields:
        missing_handles: List[str] = []
        for handle in target_handles:
            handle_rows = rows_by_handle.get(handle, [])
            if not handle_rows:
                missing_handles.append(handle)
                continue
            value = first_non_blank(handle_rows, field)
            if not value:
                missing_handles.append(handle)

        if missing_handles:
            add_finding(
                findings,
                "ERROR",
                "missing_product_field",
                f"{field} missing for {len(missing_handles)} handles",
                missing_handles,
                args.max_samples,
            )

    recommended_product_fields = (
        PRODUCT_SHOPIFY_AGE_GROUP,
        PRODUCT_SHOPIFY_COLOR,
    )
    for field in recommended_product_fields:
        missing_handles: List[str] = []
        for handle in target_handles:
            handle_rows = rows_by_handle.get(handle, [])
            if not handle_rows:
                continue
            value = first_non_blank(handle_rows, field)
            if not value:
                missing_handles.append(handle)
        if missing_handles:
            add_finding(
                findings,
                "WARN",
                "missing_recommended_product_field",
                f"{field} missing for {len(missing_handles)} handles",
                missing_handles,
                args.max_samples,
            )

    unpublished_target_handles: List[str] = []
    for handle in target_handles:
        published_value = first_non_blank(rows_by_handle.get(handle, []), ROW_PUBLISHED)
        if not parse_bool_true(published_value):
            unpublished_target_handles.append(handle)
    if unpublished_target_handles:
        add_finding(
            findings,
            "WARN",
            "target_handle_unpublished",
            f"Found {len(unpublished_target_handles)} target handles with Published != TRUE",
            unpublished_target_handles,
            args.max_samples,
        )

    missing_prefix_handles: Dict[str, List[str]] = {prefix: [] for prefix in REQUIRED_TAG_PREFIXES}
    for handle in target_handles:
        tags = first_non_blank(rows_by_handle.get(handle, []), ROW_TAGS)
        lowered = normalized_key(tags)
        for prefix in REQUIRED_TAG_PREFIXES:
            if prefix not in lowered:
                missing_prefix_handles[prefix].append(handle)

    for prefix, handles in missing_prefix_handles.items():
        if handles:
            add_finding(
                findings,
                "ERROR",
                "missing_taxonomy_tag_prefix",
                f"Tag prefix '{prefix}' missing for {len(handles)} handles",
                handles,
                args.max_samples,
            )

    invalid_complementary_refs: List[str] = []
    self_complementary_refs: List[str] = []
    duplicate_complementary_handles: List[str] = []

    invalid_related_refs: List[str] = []
    self_related_refs: List[str] = []
    duplicate_related_handles: List[str] = []

    invalid_related_settings_handles: List[str] = []
    missing_related_settings_handles: List[str] = []

    missing_search_boost_handles: List[str] = []
    duplicate_search_boost_handles: List[str] = []

    for handle in target_handles:
        handle_rows = rows_by_handle.get(handle, [])
        complementary = split_csv_tokens(first_non_blank(handle_rows, PRODUCT_DISCOVERY_COMPLEMENTARY))
        related = split_csv_tokens(first_non_blank(handle_rows, PRODUCT_DISCOVERY_RELATED))
        related_settings = normalized_key(first_non_blank(handle_rows, PRODUCT_DISCOVERY_RELATED_SETTINGS))
        search_boosts = split_csv_tokens(first_non_blank(handle_rows, PRODUCT_SEARCH_BOOSTS))

        if len(complementary) > 10:
            duplicate_complementary_handles.append(f"{handle} ({len(complementary)})")
        if len(related) > 12:
            duplicate_related_handles.append(f"{handle} ({len(related)})")

        if not related_settings:
            missing_related_settings_handles.append(handle)
        elif related_settings not in VALID_RELATED_SETTINGS:
            invalid_related_settings_handles.append(f"{handle} ({related_settings})")

        if not search_boosts:
            missing_search_boost_handles.append(handle)
        elif len(search_boosts) != len(split_csv_tokens(",".join([token.lower() for token in search_boosts]))):
            duplicate_search_boost_handles.append(handle)

        for token in complementary:
            if token == handle:
                self_complementary_refs.append(handle)
            if token not in all_handles:
                invalid_complementary_refs.append(f"{handle}->{token}")
            if not HANDLE_PATTERN.match(token):
                invalid_complementary_refs.append(f"{handle}->{token}")

        for token in related:
            if token == handle:
                self_related_refs.append(handle)
            if token not in all_handles:
                invalid_related_refs.append(f"{handle}->{token}")
            if not HANDLE_PATTERN.match(token):
                invalid_related_refs.append(f"{handle}->{token}")

    if invalid_complementary_refs:
        add_finding(
            findings,
            "ERROR",
            "invalid_complementary_reference",
            f"Found {len(invalid_complementary_refs)} invalid complementary references",
            invalid_complementary_refs,
            args.max_samples,
        )
    if self_complementary_refs:
        add_finding(
            findings,
            "ERROR",
            "self_complementary_reference",
            f"Found {len(self_complementary_refs)} self-referencing complementary values",
            self_complementary_refs,
            args.max_samples,
        )
    if duplicate_complementary_handles:
        add_finding(
            findings,
            "WARN",
            "complementary_limit_exceeded",
            f"Found {len(duplicate_complementary_handles)} handles with >10 complementary products",
            duplicate_complementary_handles,
            args.max_samples,
        )

    if invalid_related_refs:
        add_finding(
            findings,
            "ERROR",
            "invalid_related_reference",
            f"Found {len(invalid_related_refs)} invalid related references",
            invalid_related_refs,
            args.max_samples,
        )
    if self_related_refs:
        add_finding(
            findings,
            "ERROR",
            "self_related_reference",
            f"Found {len(self_related_refs)} self-referencing related values",
            self_related_refs,
            args.max_samples,
        )
    if duplicate_related_handles:
        add_finding(
            findings,
            "WARN",
            "related_limit_exceeded",
            f"Found {len(duplicate_related_handles)} handles with >12 related products",
            duplicate_related_handles,
            args.max_samples,
        )

    if missing_related_settings_handles:
        add_finding(
            findings,
            "ERROR",
            "missing_related_settings",
            f"Related settings missing for {len(missing_related_settings_handles)} handles",
            missing_related_settings_handles,
            args.max_samples,
        )
    if invalid_related_settings_handles:
        add_finding(
            findings,
            "WARN",
            "invalid_related_settings",
            f"Unexpected related settings value on {len(invalid_related_settings_handles)} handles",
            invalid_related_settings_handles,
            args.max_samples,
        )

    if missing_search_boost_handles:
        add_finding(
            findings,
            "ERROR",
            "missing_search_boosts",
            f"Search boosts missing for {len(missing_search_boost_handles)} handles",
            missing_search_boost_handles,
            args.max_samples,
        )
    if duplicate_search_boost_handles:
        add_finding(
            findings,
            "WARN",
            "duplicate_search_boosts",
            f"Duplicate search boost terms on {len(duplicate_search_boost_handles)} handles",
            duplicate_search_boost_handles,
            args.max_samples,
        )

    rows_alt_without_src: List[str] = []
    rows_position_without_src: List[str] = []
    unsupported_image_rows: List[str] = []

    malformed_gtin_rows: List[str] = []
    missing_custom_product_rows: List[str] = []
    missing_custom_metafield_rows: List[str] = []
    missing_mpn_rows: List[str] = []
    conflicting_custom_product_rows: List[str] = []
    missing_gender_rows: List[str] = []
    invalid_gender_rows: List[str] = []
    missing_age_group_rows: List[str] = []
    invalid_age_group_rows: List[str] = []
    missing_condition_rows: List[str] = []

    for index, row in enumerate(rows, start=2):
        handle = clean(row.get(ROW_HANDLE, ""))
        if not handle:
            continue
        if handle not in target_set:
            continue

        image_src = clean(row.get(ROW_IMAGE_SRC, ""))
        variant_image = clean(row.get(ROW_VARIANT_IMAGE, ""))
        image_alt = clean(row.get(ROW_IMAGE_ALT, ""))
        image_position = clean(row.get(ROW_IMAGE_POSITION, ""))

        if image_alt and not image_src:
            rows_alt_without_src.append(f"row {index} ({handle})")
        if image_position and not image_src:
            rows_position_without_src.append(f"row {index} ({handle})")
        if image_src and not is_supported_image_url(image_src):
            unsupported_image_rows.append(f"row {index} ({handle}:{image_src})")
        if variant_image and not is_supported_image_url(variant_image):
            unsupported_image_rows.append(f"row {index} ({handle}:{variant_image})")

        if not is_variant_row(row):
            continue

        barcode_raw = clean(row.get(ROW_VARIANT_BARCODE, ""))
        barcode_normalized = re.sub(r"[^0-9]", "", barcode_raw)
        custom_product = parse_bool_true(row.get(ROW_GOOGLE_CUSTOM_PRODUCT, ""))
        custom_metafield = parse_bool_true(row.get(PRODUCT_GOOGLE_CUSTOM_METAFIELD, ""))
        mpn = clean(row.get(ROW_GOOGLE_MPN, ""))
        gender = normalized_key(row.get(ROW_GOOGLE_GENDER, ""))
        age_group = normalized_key(row.get(ROW_GOOGLE_AGE_GROUP, ""))
        condition = normalized_key(row.get(ROW_GOOGLE_CONDITION, ""))

        if not gender:
            missing_gender_rows.append(f"row {index} ({handle})")
        elif gender not in VALID_GENDER_VALUES:
            invalid_gender_rows.append(f"row {index} ({handle}:{gender})")

        if not age_group:
            missing_age_group_rows.append(f"row {index} ({handle})")
        elif age_group not in VALID_AGE_GROUP_VALUES:
            invalid_age_group_rows.append(f"row {index} ({handle}:{age_group})")

        if not condition:
            missing_condition_rows.append(f"row {index} ({handle})")

        if barcode_raw:
            if barcode_normalized != barcode_raw or len(barcode_normalized) not in VALID_GTIN_LENGTHS:
                malformed_gtin_rows.append(f"row {index} ({handle}:{barcode_raw})")
            if custom_product or custom_metafield:
                conflicting_custom_product_rows.append(f"row {index} ({handle})")
        else:
            if not custom_product:
                missing_custom_product_rows.append(f"row {index} ({handle})")
            if not custom_metafield:
                missing_custom_metafield_rows.append(f"row {index} ({handle})")
            if not mpn:
                missing_mpn_rows.append(f"row {index} ({handle})")

    if rows_alt_without_src:
        add_finding(
            findings,
            "ERROR",
            "image_alt_without_src",
            f"Found {len(rows_alt_without_src)} rows with Image Alt Text but no Image Src",
            rows_alt_without_src,
            args.max_samples,
        )
    if rows_position_without_src:
        add_finding(
            findings,
            "WARN",
            "image_position_without_src",
            f"Found {len(rows_position_without_src)} rows with Image Position but no Image Src",
            rows_position_without_src,
            args.max_samples,
        )
    if unsupported_image_rows:
        add_finding(
            findings,
            "WARN",
            "unsupported_image_type",
            f"Found {len(unsupported_image_rows)} rows with unsupported image URL extension",
            unsupported_image_rows,
            args.max_samples,
        )
    if missing_gender_rows:
        add_finding(
            findings,
            "WARN",
            "missing_google_gender",
            f"Found {len(missing_gender_rows)} variant rows missing Google Shopping / Gender",
            missing_gender_rows,
            args.max_samples,
        )
    if invalid_gender_rows:
        add_finding(
            findings,
            "WARN",
            "invalid_google_gender",
            f"Found {len(invalid_gender_rows)} variant rows with invalid Google Shopping / Gender value",
            invalid_gender_rows,
            args.max_samples,
        )
    if missing_age_group_rows:
        add_finding(
            findings,
            "WARN",
            "missing_google_age_group",
            f"Found {len(missing_age_group_rows)} variant rows missing Google Shopping / Age Group",
            missing_age_group_rows,
            args.max_samples,
        )
    if invalid_age_group_rows:
        add_finding(
            findings,
            "WARN",
            "invalid_google_age_group",
            f"Found {len(invalid_age_group_rows)} variant rows with invalid Google Shopping / Age Group value",
            invalid_age_group_rows,
            args.max_samples,
        )
    if missing_condition_rows:
        add_finding(
            findings,
            "WARN",
            "missing_google_condition",
            f"Found {len(missing_condition_rows)} variant rows missing Google Shopping / Condition",
            missing_condition_rows,
            args.max_samples,
        )

    if malformed_gtin_rows:
        add_finding(
            findings,
            "WARN",
            "malformed_gtin",
            f"Found {len(malformed_gtin_rows)} rows with malformed GTIN/barcode format",
            malformed_gtin_rows,
            args.max_samples,
        )
    if missing_custom_product_rows:
        add_finding(
            findings,
            "ERROR",
            "missing_custom_product_flag",
            f"Found {len(missing_custom_product_rows)} rows missing custom product flag for barcode-less variants",
            missing_custom_product_rows,
            args.max_samples,
        )
    if missing_custom_metafield_rows:
        add_finding(
            findings,
            "ERROR",
            "missing_custom_product_metafield",
            f"Found {len(missing_custom_metafield_rows)} rows missing Google custom_product metafield for barcode-less variants",
            missing_custom_metafield_rows,
            args.max_samples,
        )
    if missing_mpn_rows:
        add_finding(
            findings,
            "WARN",
            "missing_mpn_for_barcode_less",
            f"Found {len(missing_mpn_rows)} rows missing MPN for barcode-less variants",
            missing_mpn_rows,
            args.max_samples,
        )
    if conflicting_custom_product_rows:
        add_finding(
            findings,
            "WARN",
            "custom_product_with_barcode",
            f"Found {len(conflicting_custom_product_rows)} rows with barcode but custom product flagged TRUE",
            conflicting_custom_product_rows,
            args.max_samples,
        )

    write_report(
        path=output_path,
        input_path=input_path,
        row_count=len(rows),
        target_handles=target_handles,
        findings=findings,
    )

    errors = [finding for finding in findings if finding.severity == "ERROR"]
    warnings = [finding for finding in findings if finding.severity == "WARN"]

    print(f"Validation report written: {output_path}")
    print(f"Target handles: {len(target_handles)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
