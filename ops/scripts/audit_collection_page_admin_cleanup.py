#!/usr/bin/env python3
"""Dry-run audit for collection-page admin cleanup.

This script stays read-only. It inspects Shopify CSV exports for:
- dirty / case-variant size labels that should be normalized before filter rebuilds,
- composite or suspicious color-pattern values that can leak into a Color filter,
- collection taxonomy / handle planning items that must be handled in Shopify Admin.

The default mode does not require Shopify credentials. If credentials are loaded
and ``--use-live-admin`` is passed, the script can optionally pull live collection
metadata for a read-only comparison, but it still never writes.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.fill_shopify_apparel_attributes import canonicalize_size_token, normalize_text  # noqa: E402
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
DEFAULT_INPUT_CSV = Path("GPT/products_export_1.csv")
DEFAULT_OUTPUT_DIR = Path(
    f"ops/catalog-cleanup/{datetime.now().strftime('%Y-%m-%d')}-collection-page-admin-cleanup-dry-run"
)

SIZE_COLUMNS = (
    "Option1 Value",
    "Option2 Value",
    "Option3 Value",
    "Size (product.metafields.shopify.size)",
)

COLOR_COLUMN = "Color (product.metafields.shopify.color-pattern)"

BASIC_COLOR_TOKENS = {
    "red",
    "blue",
    "green",
    "yellow",
    "black",
    "white",
    "pink",
    "purple",
    "orange",
    "gray",
    "grey",
    "brown",
    "beige",
    "navy",
    "gold",
    "silver",
    "multicolor",
    "multi color",
    "teal",
    "turquoise",
    "cream",
    "ivory",
    "khaki",
    "maroon",
    "burgundy",
    "lavender",
    "mint",
    "coral",
    "rose",
    "peach",
}

COLOR_PATTERN_HINTS = (
    "floral",
    "stripe",
    "striped",
    "plaid",
    "check",
    "polka",
    "animal",
    "leopard",
    "camo",
    "camouflage",
    "tie dye",
    "gradient",
    "print",
    "love",
    "santa",
    "reindeer",
    "snowflake",
    "gnome",
    "holiday",
    "picture",
)

COLLECTION_PLAN = [
    {
        "current_handle": "new-women-outfits",
        "current_label": "Home > Sets",
        "recommended_handle": "family-matching-outfits",
        "recommended_label": "Family Matching Outfits",
        "admin_action": "Rename handle only after redirects and internal links are mapped; update title/SEO first.",
        "reason": "Broad family-matching umbrella matches the keyword research and the existing theme-side SEO fallback language.",
        "priority": "high",
    },
    {
        "current_handle": "family-sets",
        "current_label": "Home > Sets",
        "recommended_handle": "family-vacation-outfits",
        "recommended_label": "Family Vacation Outfits",
        "admin_action": "Keep the existing handle until redirects are staged, then rename and update breadcrumbs/nav labels in Admin.",
        "reason": "Keyword research already maps matching family vacation intent to this collection; 'Sets' is too generic for shoppers.",
        "priority": "high",
    },
    {
        "current_handle": "family-swimsuits",
        "current_label": "Home > Mommy and Me",
        "recommended_handle": "family-swimsuits",
        "recommended_label": "Family Matching Swimsuits",
        "admin_action": "Keep handle, but align collection title and search listing copy to the exact-match swim intent.",
        "reason": "This already owns the strongest exact-match swim intent and should stay canonical.",
        "priority": "high",
    },
    {
        "current_handle": "mommy-and-me",
        "current_label": "Home > Mommy and Me",
        "recommended_handle": "mommy-and-me",
        "recommended_label": "Mommy and Me",
        "admin_action": "Preserve as the legacy brand hub unless a deliberate consolidation plan is approved.",
        "reason": "This is the broad parent hub; it should not be used as the breadcrumb label for Hawaiian or vacation-specific subclusters.",
        "priority": "medium",
    },
    {
        "current_handle": "daddy-me",
        "current_label": "Home > Daddy and Me",
        "recommended_handle": "daddy-me-t-shirts",
        "recommended_label": "Daddy and Me T-Shirts",
        "admin_action": "Consolidate the duplicate Daddy-and-Me family collection only after confirming the canonical handle and redirect target.",
        "reason": "Repo SEO research shows both `daddy-me` and `daddy-and-me` are live; taxonomy is cleaner if one canonical handle owns the intent.",
        "priority": "medium",
    },
]


@dataclass
class SizeVariantGroup:
    normalized_value: str
    canonical_display: str
    variant_values: list[str]
    product_handles: list[str]
    example_titles: list[str]
    source_columns: list[str]


@dataclass
class ColorAuditRow:
    raw_value: str
    classification: str
    product_handles: list[str]
    example_titles: list[str]
    reason: str


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def title_for_report(text: str) -> str:
    text = clean(text)
    if not text:
        return ""
    if re.fullmatch(r"(xs|s|m|l|xl|2xl|3xl|4xl|5xl)", text, flags=re.I):
        return text.upper()
    return text[:1].upper() + text[1:]


def choose_canonical_display(values: list[str]) -> str:
    if not values:
        return ""
    return sorted(
        values,
        key=lambda value: (
            normalize_text(value),
            -sum(1 for char in value if char.isupper()),
            len(value),
            value,
        ),
    )[0]


def looks_like_size_value(value: str) -> bool:
    text = clean(value)
    if not text:
        return False
    lowered = text.lower()
    if any(token in lowered for token in ("years", "months", "xs", "xl")):
        return True
    if re.fullmatch(r"(xxs|xs|s|m|l|xl|2xl|3xl|4xl|5xl)", lowered):
        return True
    if re.fullmatch(r"\d{1,2}(?:-\d{1,2})?\s*(?:years?|months?)", lowered):
        return True
    if re.fullmatch(r"\d{1,2}(?:-\d{1,2})?\s*[a-z]?t", lowered):
        return True
    if re.fullmatch(r"(girl|boy|child|baby|mom|mother|dad|father|adult)\s+\d.*", lowered):
        return True
    return False


def is_variant_row(row: dict[str, str]) -> bool:
    return any(clean(row.get(column, "")) for column in ("Option1 Value", "Option2 Value", "Option3 Value", "Variant SKU"))


def parse_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Missing header row in {path}")
        return list(reader)


def build_size_groups(rows: list[dict[str, str]]) -> list[SizeVariantGroup]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        handle = clean(row.get("Handle", ""))
        title = clean(row.get("Title", ""))
        for column in SIZE_COLUMNS:
            raw_value = clean(row.get(column, ""))
            if not raw_value or not looks_like_size_value(raw_value):
                continue
            canonical_token = canonicalize_size_token(raw_value)
            normalized = normalize_text(canonical_token or raw_value)
            bucket = grouped.setdefault(
                normalized,
                {
                    "values": [],
                    "handles": [],
                    "titles": [],
                    "columns": [],
                },
            )
            if raw_value not in bucket["values"]:
                bucket["values"].append(raw_value)
            if handle and handle not in bucket["handles"]:
                bucket["handles"].append(handle)
            if title and title not in bucket["titles"]:
                bucket["titles"].append(title)
            if column not in bucket["columns"]:
                bucket["columns"].append(column)

    groups: list[SizeVariantGroup] = []
    for normalized_value, bucket in grouped.items():
        if len({normalize_text(value) for value in bucket["values"]}) <= 1:
            continue
        groups.append(
            SizeVariantGroup(
                normalized_value=normalized_value,
                canonical_display=choose_canonical_display(bucket["values"]),
                variant_values=sorted(bucket["values"], key=lambda value: (normalize_text(value), value)),
                product_handles=sorted(bucket["handles"]),
                example_titles=sorted(bucket["titles"])[:5],
                source_columns=sorted(bucket["columns"]),
            )
        )

    return sorted(groups, key=lambda item: (-len(item.product_handles), item.normalized_value))


def classify_color_value(raw_value: str) -> tuple[str, str]:
    normalized = normalize_text(raw_value)
    if not normalized:
        return "blank", "No value present."
    if normalized in BASIC_COLOR_TOKENS:
        return "plain_color", "Safe plain color token."
    if any(hint in normalized for hint in COLOR_PATTERN_HINTS):
        return "pattern_like", "Pattern-like or merchandising phrase should not sit in a Color filter."
    if ";" in raw_value:
        parts = [normalize_text(part) for part in raw_value.split(";") if normalize_text(part)]
        if parts and all(part in BASIC_COLOR_TOKENS for part in parts):
            return "multi_color_combo", "Composite multi-color value; likely better treated as a deliberate filter rule decision."
        return "mixed_composite", "Composite value mixes color tokens with non-standard content."
    if "multi color" in normalized or "multicolor" in normalized:
        return "composite_color", "Composite color label should be normalized before filter rebuild."
    return "needs_review", "Not a plain color token."


def build_color_audit(rows: list[dict[str, str]]) -> list[ColorAuditRow]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        raw_value = clean(row.get(COLOR_COLUMN, ""))
        if not raw_value:
            continue
        classification, reason = classify_color_value(raw_value)
        if classification == "plain_color":
            continue
        bucket = grouped.setdefault(
            raw_value,
            {
                "classification": classification,
                "reason": reason,
                "handles": [],
                "titles": [],
            },
        )
        handle = clean(row.get("Handle", ""))
        title = clean(row.get("Title", ""))
        if handle and handle not in bucket["handles"]:
            bucket["handles"].append(handle)
        if title and title not in bucket["titles"]:
            bucket["titles"].append(title)

    return [
        ColorAuditRow(
            raw_value=raw_value,
            classification=payload["classification"],
            product_handles=sorted(payload["handles"]),
            example_titles=sorted(payload["titles"])[:5],
            reason=payload["reason"],
        )
        for raw_value, payload in sorted(grouped.items(), key=lambda item: (-len(item[1]["handles"]), item[0]))
    ]


def build_summary(
    rows: list[dict[str, str]],
    size_groups: list[SizeVariantGroup],
    color_rows: list[ColorAuditRow],
    input_csv: Path,
) -> dict[str, Any]:
    size_rows = sum(1 for row in rows if any(looks_like_size_value(clean(row.get(column, ""))) for column in SIZE_COLUMNS))
    color_rows_count = sum(1 for row in rows if clean(row.get(COLOR_COLUMN, "")))
    return {
        "source_csv": str(input_csv),
        "total_rows": len(rows),
        "variant_rows": sum(1 for row in rows if is_variant_row(row)),
        "size_rows_scanned": size_rows,
        "size_variant_groups_flagged": len(size_groups),
        "color_rows_scanned": color_rows_count,
        "color_values_flagged": len(color_rows),
        "collection_plan_items": len(COLLECTION_PLAN),
    }


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    path: Path,
    *,
    summary: dict[str, Any],
    size_groups: list[SizeVariantGroup],
    color_rows: list[ColorAuditRow],
    live_notes: list[str],
) -> None:
    lines: list[str] = []
    lines.append("# Collection Page Admin Cleanup Dry-Run")
    lines.append("")
    lines.append(f"Input CSV: `{summary['source_csv']}`")
    lines.append(f"Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total rows scanned: `{summary['total_rows']}`")
    lines.append(f"- Size variant groups flagged: `{summary['size_variant_groups_flagged']}`")
    lines.append(f"- Color values flagged: `{summary['color_values_flagged']}`")
    lines.append(f"- Collection plan items: `{summary['collection_plan_items']}`")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    if size_groups:
        top = size_groups[:10]
        lines.append("### Dirty size labels")
        lines.append("")
        lines.append(
            "These are case or phrasing variants that should be normalized in source product data before Search & Discovery is rebuilt."
        )
        lines.append("")
        for item in top:
            lines.append(f"- `{item.normalized_value}`: `{', '.join(item.variant_values)}`")
            lines.append(f"  Handles: {', '.join(item.product_handles[:5])}")
        if len(size_groups) > len(top):
            lines.append(f"- ... {len(size_groups) - len(top)} more groups in the CSV artifact")
        lines.append("")
    else:
        lines.append("- No dirty size label groups were detected in the input export.")
        lines.append("")
    if color_rows:
        lines.append("### Suspicious color values")
        lines.append("")
        lines.append(
            "The exported Color metafield contains composite or non-plain labels. That should be treated as a filter hygiene issue until Search & Discovery is rebuilt around a clean Color-only source."
        )
        lines.append("")
        for item in color_rows[:10]:
            lines.append(f"- `{item.raw_value}` ({item.classification})")
            lines.append(f"  Handles: {', '.join(item.product_handles[:5])}")
        if len(color_rows) > 10:
            lines.append(f"- ... {len(color_rows) - 10} more color values in the CSV artifact")
        lines.append("")
    else:
        lines.append("- No suspicious color values were detected in the input export.")
        lines.append("")
    lines.append("## Collection taxonomy plan")
    lines.append("")
    for item in COLLECTION_PLAN:
        lines.append(
            f"- `{item['current_handle']}` -> `{item['recommended_handle']}`: {item['recommended_label']} ({item['priority']})"
        )
        lines.append(f"  Current breadcrumb hint: {item['current_label']}")
        lines.append(f"  Action: {item['admin_action']}")
        lines.append(f"  Reason: {item['reason']}")
    lines.append("")
    lines.append("## Safety notes")
    lines.append("")
    lines.append("- This pass is dry-run only. No live Shopify writes were attempted.")
    lines.append("- The repository does not currently have Shopify credentials loaded in this shell, so live Admin reads were not performed.")
    for note in live_notes:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## Remaining operator steps")
    lines.append("")
    lines.append("1. Normalize the dirty size labels in source product data, then re-import or resync the catalog export.")
    lines.append("2. Rebuild the Search & Discovery filter configuration after the source data is clean.")
    lines.append("3. Decide whether the Color filter should point at a true color-only source or whether pattern-like entries need their own filter.")
    lines.append("4. In Shopify Admin, rename collection titles and handles in the order in this plan, staging redirects before any live handle change.")
    lines.append("5. Re-verify the collection breadcrumbs and nav labels after the Admin changes land, then QA the live collection pages again.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def maybe_fetch_live_collection(handle: str) -> dict[str, Any] | None:
    try:
        import json as _json
        from urllib import error, request
    except Exception:
        return None

    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token()
    endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
    query = """
query CollectionByHandle($handle: String!) {
  collectionByHandle(handle: $handle) {
    id
    title
    handle
    descriptionHtml
    seo {
      title
      description
    }
    products(first: 250) {
      nodes {
        handle
        title
      }
    }
  }
}
"""
    payload = _json.dumps({"query": query, "variables": {"handle": handle}}).encode("utf-8")
    req = request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
    )
    with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        body = _json.loads(response.read().decode("utf-8"))
    if body.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
    return body["data"]["collectionByHandle"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT_CSV, help="Shopify CSV export to audit.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for the audit artifacts.")
    parser.add_argument(
        "--use-live-admin",
        action="store_true",
        help="Attempt read-only Shopify Admin collection fetches if credentials are loaded in this shell.",
    )
    parser.add_argument(
        "--collection-handle",
        action="append",
        default=[],
        help="Collection handle to fetch in live-admin mode. Can be passed multiple times.",
    )
    args = parser.parse_args()

    rows = parse_rows(args.input_csv)
    size_groups = build_size_groups(rows)
    color_rows = build_color_audit(rows)
    summary = build_summary(rows, size_groups, color_rows, args.input_csv)
    live_notes: list[str] = []

    if args.use_live_admin and args.collection_handle:
        for handle in args.collection_handle:
            try:
                collection = maybe_fetch_live_collection(handle)
            except Exception as exc:  # pragma: no cover - best-effort read-only path
                live_notes.append(f"Live collection read failed for `{handle}`: {exc}")
                continue
            if not collection:
                live_notes.append(f"Live collection read returned no data for `{handle}`.")
                continue
            live_notes.append(
                f"Live collection `{handle}` fetched read-only with `{len(collection.get('products', {}).get('nodes', []))}` products."
            )

    args.output_dir.mkdir(parents=True, exist_ok=True)

    size_csv_rows = [
        {
            "normalized_size_key": item.normalized_value,
            "canonical_display": item.canonical_display,
            "variant_values": "|".join(item.variant_values),
            "product_handles": "|".join(item.product_handles),
            "example_titles": "|".join(item.example_titles),
            "source_columns": "|".join(item.source_columns),
        }
        for item in size_groups
    ]
    write_csv(
        args.output_dir / "size_label_normalization_plan.csv",
        size_csv_rows,
        [
            "normalized_size_key",
            "canonical_display",
            "variant_values",
            "product_handles",
            "example_titles",
            "source_columns",
        ],
    )

    color_csv_rows = [
        {
            "raw_value": item.raw_value,
            "classification": item.classification,
            "product_handles": "|".join(item.product_handles),
            "example_titles": "|".join(item.example_titles),
            "reason": item.reason,
        }
        for item in color_rows
    ]
    write_csv(
        args.output_dir / "color_filter_hygiene_audit.csv",
        color_csv_rows,
        ["raw_value", "classification", "product_handles", "example_titles", "reason"],
    )

    plan_rows = []
    for item in COLLECTION_PLAN:
        row = dict(item)
        plan_rows.append(row)
    write_csv(
        args.output_dir / "collection_taxonomy_plan.csv",
        plan_rows,
        [
            "current_handle",
            "current_label",
            "recommended_handle",
            "recommended_label",
            "admin_action",
            "reason",
            "priority",
        ],
    )

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write_report(
        args.output_dir / "collection_page_admin_cleanup_report.md",
        summary=summary,
        size_groups=size_groups,
        color_rows=color_rows,
        live_notes=live_notes,
    )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
