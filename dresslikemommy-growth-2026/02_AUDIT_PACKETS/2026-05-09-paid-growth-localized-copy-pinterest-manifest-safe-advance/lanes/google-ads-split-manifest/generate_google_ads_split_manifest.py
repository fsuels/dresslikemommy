#!/usr/bin/env python3
"""Generate local-only Google Ads split CSVs and an import-control manifest."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
SOURCE = REPO / (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/"
    "google-ads-url-hold/web_bulk_upload/"
    "00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv"
)
SPLIT_DIR = ROOT / "split_csvs"
CHECKSUM_FILE = ROOT / "SHA256SUMS.txt"
MANIFEST_FILE = ROOT / "manifest.json"
COUNTS_FILE = ROOT / "campaign_row_counts.csv"
REPORT_FILE = ROOT / "GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md"

COUNTRY_ORDER = [
    "GB",
    "CA",
    "AU",
    "CH",
    "DK",
    "DE",
    "NL",
    "SE",
    "FR",
    "BE",
    "ES",
    "IT",
    "PL",
    "CZ",
    "RO",
    "GR",
    "PT",
]
NON_US_CAMPAIGN_RE = re.compile(r"^DLM_([A-Z]{2})_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507$")
ID_FIELDS = ["Campaign ID", "Ad group ID", "Keyword ID", "Ad ID"]
FORBIDDEN_TERMS = {
    "us_campaign_id_23827590655": "23827590655",
    "bad_beach_product_7227378892897": "7227378892897",
    "bad_beach_handle": "matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set",
    "vacation_family": "vacation family",
    "pmax": "pmax",
    "performance_max": "performance max",
    "standard_shopping": "standard shopping",
    "shopping": "shopping",
    "product_scope": "product scope",
    "feed_label": "feed label",
    "product_group": "product group",
    "conversion_goal": "conversion goal",
    "enablement_enabled": "enabled",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_money(value: str) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    return float(value.replace("$", "").replace(",", ""))


def read_source() -> tuple[list[str], list[dict[str, str]]]:
    with SOURCE.open(newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def campaign_code(campaign: str) -> str:
    match = NON_US_CAMPAIGN_RE.match(campaign)
    return match.group(1) if match else ""


def row_text(row: dict[str, str]) -> str:
    return "\t".join(str(v) for v in row.values()).lower()


def validate(rows: list[dict[str, str]], campaigns: dict[str, list[dict[str, str]]]) -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []

    def add(name: str, passed: bool, detail: str, failures: list[int] | None = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "failure_rows": failures or [],
            }
        )

    add("source_rows", len(rows) == 1496, f"{len(rows)} data rows")
    add("action_add_only", all(r["Action"] == "Add" for r in rows), "all rows use Action=Add")

    id_failures = [
        i
        for i, r in enumerate(rows, start=2)
        if any((r.get(field) or "").strip() for field in ID_FIELDS)
    ]
    add("no_existing_ids", not id_failures, "Campaign/Ad group/Keyword/Ad IDs are blank", id_failures[:50])

    campaign_names = sorted(campaigns)
    codes = [campaign_code(c) for c in campaign_names]
    bad_campaign_names = [c for c in campaign_names if not campaign_code(c)]
    add(
        "seventeen_non_us_campaigns",
        len(campaign_names) == 17 and not bad_campaign_names and "US" not in codes,
        f"{len(campaign_names)} campaigns, codes={','.join(sorted(codes))}",
        [],
    )
    add("no_us_campaign_names", not any(c.startswith("DLM_US_") for c in campaign_names), "no campaign starts DLM_US_")

    campaign_rows = [r for r in rows if r["Row Type"] == "Campaign"]
    add(
        "campaigns_paused_search_only",
        len(campaign_rows) == 17
        and all(
            r["Campaign status"] == "Paused"
            and r["Campaign type"] == "Search"
            and r["Networks"] == "Google search"
            and r["Language"] == "en"
            for r in campaign_rows
        ),
        "campaign rows are Paused Search / Google search / en",
    )

    ad_group_failures = [
        i
        for i, r in enumerate(rows, start=2)
        if r["Row Type"] == "Ad group" and r["Ad group status"] != "Paused"
    ]
    keyword_failures = [
        i
        for i, r in enumerate(rows, start=2)
        if r["Row Type"] in {"Keyword", "Negative keyword"} and r["Keyword status"] != "Paused"
    ]
    ad_failures = [
        i
        for i, r in enumerate(rows, start=2)
        if r["Row Type"] == "Ad" and r["Ad status"] != "Paused"
    ]
    add(
        "all_importable_entities_paused",
        not ad_group_failures and not keyword_failures and not ad_failures,
        "Campaign/Ad group/Keyword/Negative keyword/Ad status fields are paused where applicable",
        (ad_group_failures + keyword_failures + ad_failures)[:50],
    )

    max_cpcs: list[float] = []
    cpc_failures: list[int] = []
    for i, row in enumerate(rows, start=2):
        for field in ["Default max. CPC", "Max CPC Bid Limit for Target IS"]:
            parsed = parse_money(row.get(field, ""))
            if parsed is not None:
                max_cpcs.append(parsed)
                if parsed > 0.15:
                    cpc_failures.append(i)
    add(
        "max_cpc_at_or_below_0_15",
        not cpc_failures and max(max_cpcs or [0.0]) <= 0.15,
        f"max CPC found={max(max_cpcs or [0.0]):.2f}",
        cpc_failures[:50],
    )

    forbidden_hits: dict[str, list[int]] = {}
    for key, term in FORBIDDEN_TERMS.items():
        hit_rows = [i for i, row in enumerate(rows, start=2) if term in row_text(row)]
        if hit_rows:
            forbidden_hits[key] = hit_rows[:50]
    add(
        "forbidden_text_scan",
        not forbidden_hits,
        "no US campaign id, bad beach URL/product, Vacation Family, PMax, Standard Shopping, product/feed/conversion/enablement terms",
        sorted({line for lines in forbidden_hits.values() for line in lines})[:50],
    )

    row_types = set(r["Row Type"] for r in rows)
    forbidden_row_types = sorted(
        rt
        for rt in row_types
        if any(term in rt.lower() for term in ["product", "feed", "conversion", "shopping", "asset group"])
    )
    add(
        "no_product_feed_conversion_row_types",
        not forbidden_row_types,
        f"row types={', '.join(sorted(row_types))}",
    )

    country_param_failures: list[int] = []
    for i, row in enumerate(rows, start=2):
        final_url = row.get("Final URL", "").strip()
        if not final_url:
            continue
        code = campaign_code(row["Campaign"])
        params = parse_qs(urlparse(final_url).query)
        if (params.get("country") or [""])[0] != code:
            country_param_failures.append(i)
    add(
        "final_urls_country_qualified",
        not country_param_failures,
        "every Final URL row carries country=<campaign country code>",
        country_param_failures[:50],
    )

    failed = [c["name"] for c in checks if c["status"] != "PASS"]
    return checks, failed


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    fieldnames, rows = read_source()
    SPLIT_DIR.mkdir(parents=True, exist_ok=True)

    campaigns: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        campaigns[row["Campaign"]].append(row)

    checks, failed = validate(rows, campaigns)
    if failed:
        raise SystemExit(f"Validation failed: {', '.join(failed)}")

    countries: list[dict[str, object]] = []
    checksum_lines = [f"{sha256(SOURCE)}  {SOURCE.relative_to(REPO)}"]
    for code in COUNTRY_ORDER:
        campaign = f"DLM_{code}_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"
        campaign_rows = campaigns[campaign]
        out = SPLIT_DIR / f"{code}_intl_search_paused_draft_web_bulk.csv"
        write_csv(out, fieldnames, campaign_rows)
        digest = sha256(out)
        checksum_lines.append(f"{digest}  {out.relative_to(REPO)}")

        row_type_counts = Counter(r["Row Type"] for r in campaign_rows)
        campaign_row = next(r for r in campaign_rows if r["Row Type"] == "Campaign")
        cpcs = [
            parse_money(r.get("Default max. CPC", ""))
            for r in campaign_rows
            if parse_money(r.get("Default max. CPC", "")) is not None
        ]
        final_url_count = sum(1 for r in campaign_rows if r.get("Final URL"))
        countries.append(
            {
                "country_code": code,
                "campaign": campaign,
                "location": campaign_row["Location"],
                "language": campaign_row["Language"],
                "rows": len(campaign_rows),
                "row_type_counts": dict(sorted(row_type_counts.items())),
                "final_url_rows": final_url_count,
                "max_default_cpc": max(cpcs or [0.0]),
                "split_csv": str(out.relative_to(ROOT)),
                "sha256": digest,
            }
        )

    CHECKSUM_FILE.write_text("\n".join(checksum_lines) + "\n")

    with COUNTS_FILE.open("w", newline="") as f:
        fieldnames_counts = [
            "country_code",
            "campaign",
            "location",
            "language",
            "total_rows",
            "campaign_rows",
            "ad_group_rows",
            "keyword_rows",
            "negative_keyword_rows",
            "ad_rows",
            "final_url_rows",
            "max_default_cpc",
            "split_csv",
            "sha256",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames_counts)
        writer.writeheader()
        for c in countries:
            counts = c["row_type_counts"]
            writer.writerow(
                {
                    "country_code": c["country_code"],
                    "campaign": c["campaign"],
                    "location": c["location"],
                    "language": c["language"],
                    "total_rows": c["rows"],
                    "campaign_rows": counts.get("Campaign", 0),
                    "ad_group_rows": counts.get("Ad group", 0),
                    "keyword_rows": counts.get("Keyword", 0),
                    "negative_keyword_rows": counts.get("Negative keyword", 0),
                    "ad_rows": counts.get("Ad", 0),
                    "final_url_rows": c["final_url_rows"],
                    "max_default_cpc": f"{c['max_default_cpc']:.2f}",
                    "split_csv": c["split_csv"],
                    "sha256": c["sha256"],
                }
            )

    manifest = {
        "status": "PASS_LOCAL_ONLY_APPROVAL_GATED",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "worker_lane": str(ROOT.relative_to(REPO)),
        "source_csv": str(SOURCE.relative_to(REPO)),
        "source_sha256": sha256(SOURCE),
        "total_rows": len(rows),
        "header_field_count": len(fieldnames),
        "campaign_count": len(countries),
        "row_type_counts": dict(sorted(Counter(r["Row Type"] for r in rows).items())),
        "action_counts": dict(sorted(Counter(r["Action"] for r in rows).items())),
        "max_default_cpc": max(
            parse_money(r.get("Default max. CPC", "")) or 0.0
            for r in rows
        ),
        "validation_checks": checks,
        "presence_targeting_caveat": (
            "CSV/web-bulk rows cannot prove Google Ads location option is "
            "Presence: People in or regularly in your included locations. "
            "That setting requires Google Ads preview/readback before any "
            "launch decision."
        ),
        "approval_gate": (
            "No Google Ads preview/import/build or live-system write is authorized "
            "by this artifact. Parent/orchestrator must obtain the exact canonical "
            "paused non-US Google Search TEST BUILD approval before opening a live "
            "Ads preview/import flow."
        ),
        "countries": countries,
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    report = render_report(manifest)
    REPORT_FILE.write_text(report)
    return 0


def render_report(manifest: dict[str, object]) -> str:
    countries = manifest["countries"]
    checks = manifest["validation_checks"]
    lines = [
        "# Google Ads Split Import-Control Manifest",
        "",
        f"Status: `{manifest['status']}`",
        "",
        "## Scope",
        "",
        "Worker A generated local-only split/import-control artifacts from the held non-US Search CSV. No Google Ads, Merchant Center, Shopify, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, or external-account writes were made.",
        "",
        f"Source CSV: `{manifest['source_csv']}`",
        f"Source SHA256: `{manifest['source_sha256']}`",
        "",
        "## Totals",
        "",
        f"- Total data rows: `{manifest['total_rows']}`",
        f"- Campaigns: `{manifest['campaign_count']}` non-US paused Search campaigns",
        f"- Row type counts: `{manifest['row_type_counts']}`",
        f"- Action counts: `{manifest['action_counts']}`",
        f"- Max default CPC: `${manifest['max_default_cpc']:.2f}`",
        "",
        "## Per-Country Split Files",
        "",
        "| Country | Location | Campaign | Rows | Campaign | Ad groups | Keywords | Negatives | Ads | Final URLs | Max CPC | Split CSV |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for country in countries:
        counts = country["row_type_counts"]
        lines.append(
            "| {code} | {location} | `{campaign}` | {rows} | {campaign_rows} | {ad_groups} | {keywords} | {negatives} | {ads} | {final_urls} | ${cpc:.2f} | `{split}` |".format(
                code=country["country_code"],
                location=country["location"],
                campaign=country["campaign"],
                rows=country["rows"],
                campaign_rows=counts.get("Campaign", 0),
                ad_groups=counts.get("Ad group", 0),
                keywords=counts.get("Keyword", 0),
                negatives=counts.get("Negative keyword", 0),
                ads=counts.get("Ad", 0),
                final_urls=country["final_url_rows"],
                cpc=country["max_default_cpc"],
                split=country["split_csv"],
            )
        )

    lines.extend(
        [
            "",
            "## Validation",
            "",
            "| Check | Status | Detail |",
            "|---|---:|---|",
        ]
    )
    for check in checks:
        lines.append(f"| `{check['name']}` | `{check['status']}` | {check['detail']} |")

    lines.extend(
        [
            "",
            "## Preview-Only Runbook",
            "",
            "1. Before any Google Ads UI, Editor, API, preview, or import action, the parent/orchestrator must obtain the exact canonical paused non-US Google Search `TEST BUILD` approval from the owner.",
            "2. Use the split file for the intended country or the full held CSV only in a preview/import validation flow. Do not enable campaigns, do not change budgets or bids, and do not touch PMax, Standard Shopping, product scope, feed labels, product groups, or conversion goals.",
            "3. Confirm the preview shows only new paused Search entities: one paused campaign per selected country, ten paused ad groups, thirty paused positive keywords, thirty-seven paused negatives, and ten paused RSAs per country.",
            "4. Confirm no existing campaign IDs or account entities are edited, especially US campaign `23827590655`.",
            "5. CSV rows alone cannot prove the Google Ads location option. In the live Ads preview/readback, verify `Presence: People in or regularly in your included locations` before any launch decision.",
            "6. After any approved paused import, perform just-in-time readbacks for status, budget, CPC, language, location, final URLs, exclusions, and conversion-goal inheritance before considering separate enablement approval.",
            "",
            "## Residual Gate",
            "",
            "These artifacts are import-control evidence only. They do not authorize live preview/import/build, live spend, campaign enablement, or any live-account write. Presence-only targeting remains a readback gate because it is not represented conclusively in the CSV.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
