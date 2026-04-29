#!/usr/bin/env python3
"""Build a Merchant Center supplemental upload for missing age_group fixes."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_ELIGIBILITY_CSV = Path(
    "dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/"
    "2026-04-28-other-ai-clean-subset_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv"
)
DEFAULT_PAID_STATUS_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-merchant-paid-status-upload/upload_paid_status_only_custom_label_4.csv"
)
DEFAULT_UNMATCHED_REPORT_CSV = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-merchant-paid-status-upload/post_upload_download_report.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-merchant-age-group-fix"
)
SUPPORTED_AGE_GROUPS = {"newborn", "infant", "toddler", "kids", "adult"}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize(value: object) -> str:
    return clean(value).lower()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str], *, delimiter: str = ",") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
            delimiter=delimiter,
        )
        writer.writeheader()
        writer.writerows(rows)


def age_from_months(text: str) -> str:
    range_matches = [
        (int(start), int(end))
        for start, end in re.findall(
            r"\b(\d{1,2})\s*[-/]\s*(\d{1,2})\s*(?:m|mo|mos|month|months)\b",
            text,
        )
    ]
    if range_matches:
        max_month = max(end for _start, end in range_matches)
        return "newborn" if max_month <= 3 else "infant" if max_month <= 12 else "toddler"

    month_matches = [
        int(month)
        for month in re.findall(r"\b(\d{1,2})\s*(?:m|mo|mos|month|months)\b", text)
    ]
    if month_matches:
        max_month = max(month_matches)
        return "newborn" if max_month <= 3 else "infant" if max_month <= 12 else "toddler"

    return ""


def age_from_years(text: str) -> str:
    range_matches = [
        (int(start), int(end))
        for start, end in re.findall(
            r"\b(\d{1,2})\s*[-/]\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)?\b",
            text,
        )
    ]
    if range_matches:
        max_age = max(end for _start, end in range_matches)
        return "toddler" if max_age <= 5 else "kids"

    year_matches = [
        int(year)
        for year in re.findall(r"\b(\d{1,2})\s*(?:t|y|yr|yrs|year|years)\b", text)
    ]
    if year_matches:
        max_age = max(year_matches)
        return "toddler" if max_age <= 5 else "kids"

    return ""


def age_from_height_cm(text: str) -> str:
    cm_matches = [int(value) for value in re.findall(r"\b(6[0-9]|7[0-9]|8[0-9]|9[0-9]|1[0-6]0)\s*cm\b", text)]
    if not cm_matches:
        return ""
    max_cm = max(cm_matches)
    if max_cm <= 80:
        return "infant"
    return "toddler" if max_cm <= 110 else "kids"


def has_token(text: str, tokens: tuple[str, ...]) -> bool:
    return any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", text) for token in tokens)


def infer_age_group(row: dict[str, str]) -> tuple[str, str]:
    """Infer Google age_group from variant-level text.

    The upload is variant-keyed, so variant title and SKU are favored over
    product-level fallback tokens.
    """

    variant_text = normalize(" ".join([row.get("variant_title", ""), row.get("sku", "")]))
    product_text = normalize(
        " ".join(
            [
                row.get("product_title", ""),
                row.get("handle", "").replace("-", " "),
                row.get("product_type", ""),
                row.get("tags", ""),
                row.get("collections", ""),
            ]
        )
    )
    combined = f"{variant_text} {product_text}".strip()

    if has_token(variant_text, ("newborn", "nb")):
        return "newborn", "variant_newborn_token"

    month_age = age_from_months(variant_text)
    if month_age:
        return month_age, "variant_month_size"

    year_age = age_from_years(variant_text)
    if year_age:
        return year_age, "variant_year_size"

    cm_age = age_from_height_cm(variant_text)
    if cm_age:
        return cm_age, "variant_height_cm"

    if has_token(variant_text, ("baby", "infant")):
        return "infant", "variant_baby_token"
    if has_token(variant_text, ("toddler",)):
        return "toddler", "variant_toddler_token"
    if has_token(variant_text, ("child", "children", "kid", "kids", "girl", "girls", "boy", "boys")):
        return "kids", "variant_child_role_token"

    adult_tokens = (
        "mother",
        "mom",
        "mommy",
        "father",
        "dad",
        "daddy",
        "women",
        "woman",
        "men",
        "man",
        "adult",
        "maternity",
        "wife",
        "husband",
        "queen",
        "king",
    )
    if has_token(variant_text, adult_tokens):
        return "adult", "variant_adult_role_token"

    # Most role-free alpha sizes in this catalog are adult apparel variants.
    if re.search(r"\b(?:xxs|xs|s|m|l|xl|xxl|xxxl|2xl|3xl|4xl|5xl)\b", variant_text):
        return "adult", "variant_alpha_size_fallback"

    if has_token(product_text, ("newborn",)):
        return "newborn", "product_newborn_token"

    product_month_age = age_from_months(product_text)
    if product_month_age:
        return product_month_age, "product_month_size"

    product_year_age = age_from_years(product_text)
    if product_year_age:
        return product_year_age, "product_year_size"

    if has_token(product_text, ("baby", "infant")):
        return "infant", "product_baby_token"
    if has_token(product_text, ("toddler",)):
        return "toddler", "product_toddler_token"
    if has_token(product_text, adult_tokens):
        return "adult", "product_adult_role_token"
    if has_token(product_text, ("child", "children", "kid", "kids", "girl", "girls", "boy", "boys", "family")):
        return "kids", "product_child_family_token"

    if combined:
        return "", "unresolved_from_text"
    return "", "unresolved_blank_text"


def paid_status_by_id(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    rows = read_csv(path)
    return {clean(row.get("id")): clean(row.get("custom_label_4")) for row in rows if clean(row.get("id"))}


def load_unmatched_offer_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()

    unmatched: set[str] = set()
    in_issue_table = False
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue
            if clean(row[0]) == "Item Id":
                in_issue_table = True
                continue
            if not in_issue_table:
                continue
            item_id = clean(row[0])
            message = clean(row[2] if len(row) > 2 else "")
            if item_id and message == "Offer does not exist":
                unmatched.add(item_id)
    return unmatched


def build_rows(
    eligibility_rows: list[dict[str, str]],
    paid_labels: dict[str, str],
    unmatched_offer_ids: set[str] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, Any]]:
    upload_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    counters: Counter[str] = Counter()
    unmatched_offer_ids = unmatched_offer_ids or set()

    seen_ids: set[str] = set()
    for row in eligibility_rows:
        item_id = clean(row.get("merchant_center_id"))
        if not item_id or item_id in seen_ids:
            counters["skipped_missing_or_duplicate_id"] += 1
            continue
        seen_ids.add(item_id)

        age_group, source = infer_age_group(row)
        custom_label_4 = paid_labels.get(item_id, clean(row.get("paid_status") or row.get("current_google_custom_label_4")))
        if item_id in unmatched_offer_ids:
            status = "excluded_offer_does_not_exist"
        else:
            status = "upload" if age_group in SUPPORTED_AGE_GROUPS else "manual_review"
        if status == "upload":
            upload_rows.append(
                {
                    "id": item_id,
                    "custom_label_4": custom_label_4,
                    "age_group": age_group,
                }
            )

        review_rows.append(
            {
                "id": item_id,
                "product_id": clean(row.get("product_id")),
                "variant_id": clean(row.get("variant_id")),
                "handle": clean(row.get("handle")),
                "product_title": clean(row.get("product_title")),
                "variant_title": clean(row.get("variant_title")),
                "sku": clean(row.get("sku")),
                "custom_label_4": custom_label_4,
                "age_group": age_group,
                "inference_source": source,
                "status": status,
            }
        )
        counters[f"status_{status}"] += 1
        counters[f"age_group_{age_group or 'blank'}"] += 1
        counters[f"source_{source}"] += 1

    summary = {
        "eligibility_rows": len(eligibility_rows),
        "unique_ids_seen": len(seen_ids),
        "upload_rows": len(upload_rows),
        "manual_review_rows": sum(1 for row in review_rows if row["status"] == "manual_review"),
        "excluded_offer_does_not_exist_rows": sum(
            1 for row in review_rows if row["status"] == "excluded_offer_does_not_exist"
        ),
        "age_group_counts": {
            age_group: counters.get(f"age_group_{age_group}", 0)
            for age_group in sorted(SUPPORTED_AGE_GROUPS)
        },
        "upload_age_group_counts": dict(Counter(row["age_group"] for row in upload_rows)),
        "status_counts": {
            "upload": counters.get("status_upload", 0),
            "manual_review": counters.get("status_manual_review", 0),
            "excluded_offer_does_not_exist": counters.get("status_excluded_offer_does_not_exist", 0),
        },
        "inference_source_counts": {
            key.removeprefix("source_"): value
            for key, value in sorted(counters.items())
            if key.startswith("source_")
        },
        "custom_label_4_counts": dict(Counter(row["custom_label_4"] for row in upload_rows)),
    }
    return upload_rows, review_rows, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Merchant Center age_group supplemental upload.")
    parser.add_argument("--eligibility-csv", type=Path, default=DEFAULT_ELIGIBILITY_CSV)
    parser.add_argument("--paid-status-csv", type=Path, default=DEFAULT_PAID_STATUS_CSV)
    parser.add_argument("--unmatched-report-csv", type=Path, default=DEFAULT_UNMATCHED_REPORT_CSV)
    parser.add_argument(
        "--include-unmatched",
        action="store_true",
        help="Include rows reported by Merchant Center as Offer does not exist.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    eligibility_rows = read_csv(args.eligibility_csv)
    paid_labels = paid_status_by_id(args.paid_status_csv)
    unmatched_offer_ids = set() if args.include_unmatched else load_unmatched_offer_ids(args.unmatched_report_csv)
    upload_rows, review_rows, summary = build_rows(eligibility_rows, paid_labels, unmatched_offer_ids)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    upload_path = output_dir / "upload_matched_age_group_with_paid_status.csv"
    upload_txt_path = output_dir / "upload_matched_age_group_with_paid_status.txt"
    review_path = output_dir / "age_group_inference_review.csv"
    rollback_path = output_dir / "rollback_paid_status_only_custom_label_4.csv"
    excluded_path = output_dir / "excluded_offer_does_not_exist_ids.csv"
    summary_path = output_dir / "summary.json"

    write_csv(upload_path, upload_rows, ["id", "custom_label_4", "age_group"])
    write_csv(upload_txt_path, upload_rows, ["id", "custom_label_4", "age_group"], delimiter="\t")
    write_csv(
        excluded_path,
        [{"id": item_id, "exclusion_reason": "Offer does not exist"} for item_id in sorted(unmatched_offer_ids)],
        ["id", "exclusion_reason"],
    )
    write_csv(
        review_path,
        review_rows,
        [
            "id",
            "product_id",
            "variant_id",
            "handle",
            "product_title",
            "variant_title",
            "sku",
            "custom_label_4",
            "age_group",
            "inference_source",
            "status",
        ],
    )
    write_csv(
        rollback_path,
        [{"id": row["id"], "custom_label_4": row["custom_label_4"]} for row in upload_rows],
        ["id", "custom_label_4"],
    )

    summary.update(
        {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "input_eligibility_csv": str(args.eligibility_csv),
            "input_paid_status_csv": str(args.paid_status_csv),
            "input_unmatched_report_csv": str(args.unmatched_report_csv),
            "upload_file": str(upload_path),
            "upload_file_tab_delimited": str(upload_txt_path),
            "review_file": str(review_path),
            "excluded_offer_ids_file": str(excluded_path),
            "rollback_file": str(rollback_path),
            "target_merchant_center_account": "124884876",
            "target_source_id": "10626787326",
            "target_source_name": "supplemental_feed_pilot.txt",
            "write_scope": "Merchant Center supplemental source upload; preserve custom_label_4 and add age_group",
            "supported_age_groups": sorted(SUPPORTED_AGE_GROUPS),
            "notes": [
                "Upload file intentionally includes custom_label_4 so the current paid-status override is not removed when the source is replaced.",
                "Rows reported by Merchant Center as Offer does not exist are excluded from the default upload to clear the supplemental source processing issue.",
                "Rollback file restores the paid-status-only source shape from the last upload packet.",
                "No Shopify, Google Ads, budget, or campaign status changes are included.",
            ],
        }
    )
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
