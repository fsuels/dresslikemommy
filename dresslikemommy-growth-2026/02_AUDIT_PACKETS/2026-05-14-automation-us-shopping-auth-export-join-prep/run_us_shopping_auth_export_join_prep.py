#!/usr/bin/env python3.13
"""Prepare and optionally validate the US Shopping authenticated export join.

This script does not call Google Ads, Merchant Center, Shopify Admin, or any
external account surface. It packages the next authenticated export step so a
future account-capable session can drop in a read-only product/item export and
get an immediate, auditable join against the public-clean scope.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

PUBLIC_CLEAN_SCOPE = ROOT / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-14-automation-us-shopping-public-pdp-fit-preflight/"
    "us_shopping_auth_export_public_clean_scope.csv"
)
HELD_ROWS = ROOT / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-14-automation-us-shopping-held-pdp-repair-packet/"
    "us_shopping_held_pdp_repair_rows.csv"
)

OUT_TEMPLATE = OUT_DIR / "us_shopping_authenticated_item_export_template.csv"
OUT_SCOPE = OUT_DIR / "us_shopping_public_clean_scope_by_handle.csv"
OUT_JOINED = OUT_DIR / "us_shopping_auth_export_joined_decisions.csv"
OUT_SUMMARY = OUT_DIR / "us_shopping_auth_export_join_prep_summary.json"
OUT_REPORT = OUT_DIR / "US_SHOPPING_AUTH_EXPORT_JOIN_PREP.md"

EXPECTED_EXPORT_HEADERS = [
    "item_id",
    "product_title",
    "product_group",
    "custom_label_0",
    "custom_label_4",
    "search_term",
    "query",
    "impressions",
    "clicks",
    "cost",
    "conversion_value",
    "landing_url",
]

URL_COLUMNS = [
    "landing_url",
    "final_url",
    "url",
    "product_url",
    "destination_url",
    "link",
]

NUMERIC_COLUMNS = ["impressions", "clicks", "cost", "conversion_value"]

BUYER_TERM_GROUPS = {
    "family_photo": {"family", "photo", "photos", "picture", "pictures", "outfit", "outfits"},
    "mommy_me": {"mommy", "mom", "mother", "daughter", "me"},
    "wedding_guest": {"wedding", "guest", "dress", "dresses"},
    "swim": {"swim", "swimsuit", "swimwear", "beach", "pool"},
    "pajamas": {"pajama", "pajamas", "pyjama", "pyjamas"},
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_google_export_csv(path: Path) -> list[dict[str, str]]:
    """Read Google Ads exports that may include title/date preamble rows."""
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))

    header_index = 0
    for idx, row in enumerate(rows):
        normalized = {normalize_key(cell) for cell in row if cell}
        if {"title", "item_id"} <= normalized:
            header_index = idx
            break

    if header_index:
        rows = rows[header_index:]

    if not rows:
        return []

    fieldnames = rows[0]
    return [
        dict(zip(fieldnames, row))
        for row in rows[1:]
        if any((cell or "").strip() for cell in row)
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def product_handle_from_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlparse(value)
    path = parsed.path or value
    match = re.search(r"/products/([^/?#]+)", path)
    return match.group(1).strip() if match else ""


def normalize_key(value: str) -> str:
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def normalize_export_row(row: dict[str, str]) -> dict[str, str]:
    normalized = {normalize_key(k): (v or "").strip() for k, v in row.items()}
    for key in list(normalized):
        if key.startswith("conv_value"):
            normalized.setdefault("conversion_value", normalized[key])
        if key in {"search_terms", "search_term_query", "query_search_term"}:
            normalized.setdefault("search_term", normalized[key])
        if key in {"title", "item_title", "product"}:
            normalized.setdefault("product_title", normalized[key])
        if key in {"item_id_merchant_center", "offer_id", "id"}:
            normalized.setdefault("item_id", normalized[key])
        if key in {"impr", "impr_", "imps"}:
            normalized.setdefault("impressions", normalized[key])
    return normalized


def title_join_key(value: str) -> str:
    if not value:
        return ""
    base = re.split(r"\s+[A-Za-z0-9][A-Za-z0-9 -]*\s*/\s*", value, maxsplit=1)[0]
    base = re.sub(r"\s+", " ", base.replace("| Dress Like Mommy", "")).strip().lower()
    return re.sub(r"[^a-z0-9]+", " ", base).strip()


def parse_number(value: str) -> float:
    if not value:
        return 0.0
    cleaned = re.sub(r"[^0-9.\-]+", "", value)
    if cleaned in {"", ".", "-", "-."}:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def title_needs_for_query(search_term: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", search_term.lower()))
    needed: set[str] = set()
    for group, group_tokens in BUYER_TERM_GROUPS.items():
        if tokens & group_tokens:
            needed.add(group)
    return needed


def has_title_signal(title: str, needed_group: str) -> bool:
    tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
    group_tokens = BUYER_TERM_GROUPS.get(needed_group, set())
    return bool(tokens & group_tokens)


def build_scope_rows(public_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in public_rows:
        grouped[row.get("candidate_handle", "")].append(row)

    scope_rows: list[dict[str, object]] = []
    for handle, rows in sorted(grouped.items()):
        search_terms = sorted({row.get("search_term", "") for row in rows if row.get("search_term")})
        landing_urls = sorted({row.get("landing_url", "") for row in rows if row.get("landing_url")})
        public_titles = sorted({row.get("public_title", "") for row in rows if row.get("public_title")})
        query_fits = sorted({row.get("query_fit", "") for row in rows if row.get("query_fit")})
        scope_rows.append(
            {
                "candidate_handle": handle,
                "search_terms": " | ".join(search_terms),
                "public_clean_rows": len(rows),
                "landing_url": landing_urls[0] if landing_urls else "",
                "public_title": public_titles[0] if public_titles else "",
                "query_fit_values": " | ".join(query_fits),
                "join_status": "PUBLIC_CLEAN_AUTH_EXPORT_SCOPE",
            }
        )
    return scope_rows


def create_template() -> None:
    instruction_row = {
        "item_id": "READ_ONLY_EXPORT_ONLY__DO_NOT_UPLOAD",
        "product_title": "Drop authenticated Google Ads/Merchant product-item export rows here",
        "product_group": "us_test_ready or visible product group/custom label where available",
        "custom_label_0": "paid_eligible where available",
        "custom_label_4": "us_test_ready where available",
        "search_term": "query/search term if export exposes it",
        "query": "alternate query column if needed",
        "impressions": "0",
        "clicks": "0",
        "cost": "0",
        "conversion_value": "0",
        "landing_url": "https://www.dresslikemommy.com/products/example-handle?country=US",
    }
    write_csv(OUT_TEMPLATE, EXPECTED_EXPORT_HEADERS, [instruction_row])


def join_export(export_path: Path, public_rows: list[dict[str, str]], held_rows: list[dict[str, str]]) -> dict[str, object]:
    raw_export = read_google_export_csv(export_path)
    public_by_handle = defaultdict(list)
    public_by_title = defaultdict(list)
    for row in public_rows:
        public_by_handle[row.get("candidate_handle", "")].append(row)
        public_by_title[title_join_key(row.get("public_title", ""))].append(row)

    held_by_handle = defaultdict(list)
    held_by_title = defaultdict(list)
    for row in held_rows:
        held_by_handle[row.get("candidate_handle", "")].append(row)
        held_by_title[title_join_key(row.get("public_title", ""))].append(row)

    joined_rows: list[dict[str, object]] = []
    export_missing_join_key = 0
    export_public_clean_matches = 0
    export_held_matches = 0
    export_unmatched = 0
    proof_rows_with_impressions = 0
    likely_title_packet_candidates = 0
    totals_by_public_decision = defaultdict(lambda: {"rows": 0, "impressions": 0.0, "clicks": 0.0, "cost": 0.0, "conversion_value": 0.0})
    totals_by_join_decision = defaultdict(lambda: {"rows": 0, "impressions": 0.0, "clicks": 0.0, "cost": 0.0, "conversion_value": 0.0})

    for raw_row in raw_export:
        row = normalize_export_row(raw_row)
        handle = ""
        for url_col in URL_COLUMNS:
            handle = product_handle_from_url(row.get(url_col, ""))
            if handle:
                break
        if not handle and row.get("candidate_handle"):
            handle = row["candidate_handle"]

        title_key = title_join_key(row.get("product_title", ""))
        title_public_matches = public_by_title.get(title_key, [])
        title_held_matches = held_by_title.get(title_key, [])
        if not handle and title_public_matches:
            handle = title_public_matches[0].get("candidate_handle", "")
        if not handle and title_held_matches:
            handle = title_held_matches[0].get("candidate_handle", "")

        if not handle:
            export_missing_join_key += 1

        public_matches = public_by_handle.get(handle, []) or title_public_matches
        held_matches = held_by_handle.get(handle, []) or title_held_matches

        impressions = parse_number(row.get("impressions", ""))
        clicks = parse_number(row.get("clicks", ""))
        cost = parse_number(row.get("cost", ""))
        conversion_value = parse_number(row.get("conversion_value", ""))
        proof_rows_with_impressions += 1 if impressions > 0 else 0

        search_term = row.get("search_term") or row.get("query") or ""
        product_title = row.get("product_title", "")
        needed_groups = title_needs_for_query(search_term)
        missing_title_groups = sorted(group for group in needed_groups if not has_title_signal(product_title, group))

        if public_matches:
            export_public_clean_matches += 1
            if impressions > 0 and missing_title_groups:
                decision = "REVIEW_FOR_NARROW_TITLE_FEED_APPROVAL_PACKET"
                likely_title_packet_candidates += 1
            elif impressions > 0:
                decision = "ITEM_LEVEL_PROOF_PUBLIC_CLEAN_NO_TITLE_ACTION_YET"
            else:
                decision = "PUBLIC_CLEAN_MATCH_NO_IMPRESSION_PROOF"
            matched_search_terms = sorted({m.get("search_term", "") for m in public_matches if m.get("search_term")})
            public_decision = "PUBLIC_CLEAN"
            hold_reason = ""
        elif held_matches:
            export_held_matches += 1
            decision = "HOLD_FROM_TITLE_FEED_DECISIONS_UNTIL_REPAIRED_OR_PROVEN_EXCEPTION"
            matched_search_terms = sorted({m.get("search_term", "") for m in held_matches if m.get("search_term")})
            public_decision = "HELD_SCOPE"
            hold_reason = " | ".join(sorted({m.get("repair_reason", "") for m in held_matches if m.get("repair_reason")}))
        else:
            export_unmatched += 1
            decision = "UNMATCHED_TO_PUBLIC_CLEAN_SCOPE_REVIEW_BEFORE_USE"
            matched_search_terms = []
            public_decision = "UNMATCHED"
            hold_reason = ""

        for totals in (totals_by_public_decision[public_decision], totals_by_join_decision[decision]):
            totals["rows"] += 1
            totals["impressions"] += impressions
            totals["clicks"] += clicks
            totals["cost"] += cost
            totals["conversion_value"] += conversion_value

        joined_rows.append(
            {
                "decision": decision,
                "public_decision": public_decision,
                "item_id": row.get("item_id", ""),
                "product_handle": handle,
                "product_title": product_title,
                "export_search_term": search_term,
                "public_scope_search_terms": " | ".join(matched_search_terms),
                "impressions": impressions,
                "clicks": clicks,
                "cost": cost,
                "conversion_value": conversion_value,
                "missing_title_signal_groups": " | ".join(missing_title_groups),
                "hold_reason": hold_reason,
                "landing_url": next((row.get(col, "") for col in URL_COLUMNS if row.get(col)), ""),
            }
        )

    joined_fields = [
        "decision",
        "public_decision",
        "item_id",
        "product_handle",
        "product_title",
        "export_search_term",
        "public_scope_search_terms",
        "impressions",
        "clicks",
        "cost",
        "conversion_value",
        "missing_title_signal_groups",
        "hold_reason",
        "landing_url",
    ]
    write_csv(OUT_JOINED, joined_fields, joined_rows)

    return {
        "export_path": str(export_path),
        "export_rows": len(raw_export),
        "export_missing_join_key": export_missing_join_key,
        "export_public_clean_matches": export_public_clean_matches,
        "export_held_matches": export_held_matches,
        "export_unmatched": export_unmatched,
        "proof_rows_with_impressions": proof_rows_with_impressions,
        "likely_title_packet_candidates": likely_title_packet_candidates,
        "totals_by_public_decision": dict(sorted(totals_by_public_decision.items())),
        "totals_by_join_decision": dict(sorted(totals_by_join_decision.items())),
        "joined_decisions_csv": str(OUT_JOINED.relative_to(ROOT)),
    }


def render_report(summary: dict[str, object], export_summary: dict[str, object] | None) -> None:
    lines = [
        "# US Shopping Auth Export Join Prep",
        "",
        f"Generated: `{summary['generated_at']}`",
        "",
        "## Purpose",
        "",
        "- Package the next authenticated read-only Standard Shopping export step for campaign `23802638621`.",
        "- Force the future item-level export to join against the `18` public-clean US Shopping candidate rows first.",
        "- Keep held PDP rows out of title/feed/product decisions unless their exact repair gate is cleared or item-level proof warrants the one documented weak-fit exception.",
        "- Avoid product/feed/title/product-group/bid/budget/status writes from local hypotheses.",
        "",
        "## Current Local Result",
        "",
        f"- Public-clean candidate rows loaded: `{summary['public_clean_rows']}`.",
        f"- Public-clean unique handles: `{summary['public_clean_unique_handles']}`.",
        f"- Held/review rows loaded for exclusion gates: `{summary['held_rows']}`.",
        f"- Export template: `{OUT_TEMPLATE.relative_to(ROOT)}`.",
        f"- Handle-level scope: `{OUT_SCOPE.relative_to(ROOT)}`.",
        "",
        "## Required Authenticated Export Columns",
        "",
        "- Required if available: `item_id`, `product_title`, `product_group`, `custom_label_0`, `custom_label_4`, `search_term` or `query`, `impressions`, `clicks`, `cost`, `conversion_value`, and `landing_url` or another product URL column.",
        "- The join key is the Shopify product handle parsed from a product URL. If the export cannot include URLs, add the handle manually from the visible destination URL before using it for decisions.",
        "",
        "## Decision Rules",
        "",
        "- `PUBLIC_CLEAN_MATCH_NO_IMPRESSION_PROOF`: no title/feed action; no item-level demand proof.",
        "- `ITEM_LEVEL_PROOF_PUBLIC_CLEAN_NO_TITLE_ACTION_YET`: item received impressions and is public-clean, but the title does not obviously miss the observed buyer intent.",
        "- `REVIEW_FOR_NARROW_TITLE_FEED_APPROVAL_PACKET`: item received impressions and the exported title appears to miss one or more buyer-intent signal groups. This is a review candidate only, not approval to edit.",
        "- `HOLD_FROM_TITLE_FEED_DECISIONS_UNTIL_REPAIRED_OR_PROVEN_EXCEPTION`: the row matched a held PDP gate and must stay out of decisions unless the repair/readback condition is met.",
        "- `UNMATCHED_TO_PUBLIC_CLEAN_SCOPE_REVIEW_BEFORE_USE`: the export row did not match the public-clean scope; review before using it.",
        "",
    ]

    if export_summary:
        public_totals = export_summary.get("totals_by_public_decision", {})
        join_totals = export_summary.get("totals_by_join_decision", {})
        lines.extend(
            [
                "## Optional Export Join Result",
                "",
                f"- Export rows joined: `{export_summary['export_rows']}`.",
                f"- Public-clean matches: `{export_summary['export_public_clean_matches']}`.",
                f"- Held-scope matches: `{export_summary['export_held_matches']}`.",
                f"- Unmatched rows: `{export_summary['export_unmatched']}`.",
                f"- Rows with impressions: `{export_summary['proof_rows_with_impressions']}`.",
                f"- Review-only title/feed packet candidates: `{export_summary['likely_title_packet_candidates']}`.",
                f"- Joined decision CSV: `{export_summary['joined_decisions_csv']}`.",
                "",
                "Performance by joined scope:",
                "",
                "| Scope | Rows | Impr. | Clicks | Cost | Conversion value |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for scope in ["PUBLIC_CLEAN", "HELD_SCOPE", "UNMATCHED"]:
            totals = public_totals.get(scope, {"rows": 0, "impressions": 0, "clicks": 0, "cost": 0, "conversion_value": 0})
            lines.append(
                f"| `{scope}` | `{totals['rows']:.0f}` | `{totals['impressions']:.0f}` | `{totals['clicks']:.0f}` | `${totals['cost']:.2f}` | `${totals['conversion_value']:.2f}` |"
            )
        lines.extend(
            [
                "",
                "Decision totals:",
                "",
                "| Decision | Rows | Impr. | Clicks | Cost | Conversion value |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for decision, totals in sorted(join_totals.items()):
            lines.append(
                f"| `{decision}` | `{totals['rows']:.0f}` | `{totals['impressions']:.0f}` | `{totals['clicks']:.0f}` | `${totals['cost']:.2f}` | `${totals['conversion_value']:.2f}` |"
            )
        lines.extend(
            [
                "",
                "Export decision:",
                "",
                "- The authenticated export produced no narrow title/feed approval candidates.",
                "- Held-scope matches had negligible exposure and no clicks, so they are not the current spend leak.",
                "- Most export rows remain outside the public-clean query/title packet, so the next safe action is broader unmatched-row/query attribution review before any product/feed/product-group change.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Optional Export Join Result",
                "",
                "- No authenticated export was supplied in this automation run.",
                "- This is expected in the unattended runtime because authenticated Google Ads/account surfaces are already gated as `AUTOMATION_CAPABILITY_MISMATCH`.",
                "",
            ]
        )

    lines.extend(
        [
            "## Guardrails",
            "",
            "- No Google Ads upload/apply/import/add keyword/bid/budget/status/negative/product-group write occurred.",
            "- No Merchant feed/source/product/title edit occurred.",
            "- No Shopify Admin product/title/feed-visible edit and no live Shopify theme push occurred.",
            "- No Pinterest, GA4/GTM, billing, conversion, credential, or destructive filesystem write occurred.",
            "",
            "## Next Action",
            "",
            "If no export has been joined yet, run the authenticated read-only product-item export in a Google Ads/Merchant-capable session, save it outside secrets-bearing paths, then run:",
            "",
            "```bash",
            f"python3.13 {Path(__file__).relative_to(ROOT)} --export-csv /path/to/authenticated-export.csv",
            "```",
            "",
            "For this joined export, do not prepare a title/feed repair packet yet. First inspect unmatched item rows and query/product-group attribution because the clean/held packet did not surface a proven title mismatch and held rows are not spending.",
            "",
        ]
    )
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--export-csv", type=Path, help="Optional authenticated read-only item export to join.")
    args = parser.parse_args()

    public_rows = read_csv(PUBLIC_CLEAN_SCOPE)
    held_rows = read_csv(HELD_ROWS)
    scope_rows = build_scope_rows(public_rows)
    write_csv(
        OUT_SCOPE,
        [
            "candidate_handle",
            "search_terms",
            "public_clean_rows",
            "landing_url",
            "public_title",
            "query_fit_values",
            "join_status",
        ],
        scope_rows,
    )
    create_template()

    export_summary = None
    if args.export_csv:
        export_summary = join_export(args.export_csv, public_rows, held_rows)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "public_clean_scope": str(PUBLIC_CLEAN_SCOPE.relative_to(ROOT)),
        "held_rows_scope": str(HELD_ROWS.relative_to(ROOT)),
        "public_clean_rows": len(public_rows),
        "public_clean_unique_handles": len({row.get("candidate_handle", "") for row in public_rows}),
        "held_rows": len(held_rows),
        "held_unique_handles": len({row.get("candidate_handle", "") for row in held_rows}),
        "template_csv": str(OUT_TEMPLATE.relative_to(ROOT)),
        "scope_by_handle_csv": str(OUT_SCOPE.relative_to(ROOT)),
        "export_join": export_summary,
        "status": "AUTH_EXPORT_TEMPLATE_READY" if not export_summary else "AUTH_EXPORT_JOIN_COMPLETED",
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    render_report(summary, export_summary)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
