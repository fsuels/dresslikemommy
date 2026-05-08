#!/usr/bin/env python3
"""Refresh local-only international Search final URLs with country-qualified PDP URLs."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse


LANE_DIR = Path(__file__).resolve().parent
SOURCE_PACKET = (
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/"
)

COUNTRY_LOCALES = {
    "ES": "es",
    "IT": "it",
    "RO": "ro",
    "PT": "pt",
}

THEME_PRODUCT_HANDLES = {
    "Mommy & Me Dresses": "elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits",
    "Family Matching": "elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer",
    "Vacation Family": "matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set",
    "Matching Pajamas": "cute-matching-mom-and-daughter-cartoon-pajama-set-fun-and-cozy-sleepwear",
    "Matching Swimwear": "chic-pink-mermaid-scales-tankini-set-for-mother-and-daughter",
    "Daddy & Me": "daddy-and-me-matching-floral-shirts-black-rose-print-short-sleeve-button-up-set",
}

PROHIBITED_ROW_PATTERNS = (
    "pmax",
    "performance max",
    "standard shopping",
    "shopping",
    "product scope",
    "feed label",
    "product group",
    "conversion goal",
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def country_code_from_campaign(campaign: str) -> str:
    match = re.match(r"DLM_([A-Z]{2})_", campaign)
    if not match:
        raise ValueError(f"cannot derive country code from campaign: {campaign}")
    return match.group(1)


def theme_from_ad_group(ad_group: str) -> str:
    if ad_group.endswith(" - Exact"):
        return ad_group.removesuffix(" - Exact")
    if ad_group.endswith(" - Phrase"):
        return ad_group.removesuffix(" - Phrase")
    raise ValueError(f"cannot derive theme from ad group: {ad_group}")


def final_url(country_code: str, theme: str) -> str:
    handle = THEME_PRODUCT_HANDLES[theme]
    locale = COUNTRY_LOCALES.get(country_code)
    prefix = f"/{locale}" if locale else ""
    return f"https://www.dresslikemommy.com{prefix}/products/{handle}?country={country_code}"


def refresh_urls(path: Path) -> dict[str, int]:
    fields, rows = read_csv(path)
    changed = 0
    by_country = Counter()
    for row in rows:
        if not row.get("Final URL"):
            continue
        campaign = row.get("Campaign", "")
        ad_group = row.get("Ad group", "")
        country_code = country_code_from_campaign(campaign)
        theme = theme_from_ad_group(ad_group)
        new_url = final_url(country_code, theme)
        if row["Final URL"] != new_url:
            row["Final URL"] = new_url
            changed += 1
            by_country[country_code] += 1
    write_csv(path, fields, rows)
    return {"changed": changed, **{f"changed_{k}": v for k, v in sorted(by_country.items())}}


def update_manifest(path: Path, summary: dict[str, object]) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "packet": str(LANE_DIR),
            "source_packet": SOURCE_PACKET,
            "refresh_date": "2026-05-08",
            "url_refresh": {
                "strategy": "Country-qualified product final URLs; ES/IT/RO/PT use proven localized route plus country parameter; other English-only shells use base product route plus country parameter.",
                "localized_country_params_proven": COUNTRY_LOCALES,
                "theme_product_handles": THEME_PRODUCT_HANDLES,
                "keyword_final_urls_changed": summary["keyword_url_changes"],
                "rsa_final_urls_changed": summary["rsa_url_changes"],
                "web_bulk_final_urls_changed": summary["web_bulk_url_changes"],
            },
        }
    )
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_final_url_mapping() -> None:
    fields = ["Country code", "Locale path", "Theme", "Product handle", "Final URL template"]
    rows = []
    campaign_fields, campaigns = read_csv(LANE_DIR / "campaign_structure.csv")
    del campaign_fields
    for campaign in campaigns:
        country_code = campaign["Code"]
        for theme, handle in THEME_PRODUCT_HANDLES.items():
            rows.append(
                {
                    "Country code": country_code,
                    "Locale path": f"/{COUNTRY_LOCALES[country_code]}" if country_code in COUNTRY_LOCALES else "(base English route)",
                    "Theme": theme,
                    "Product handle": handle,
                    "Final URL template": final_url(country_code, theme),
                }
            )
    write_csv(LANE_DIR / "final_url_mapping.csv", fields, rows)


def validate() -> dict[str, object]:
    paths = {
        "campaigns": LANE_DIR / "campaign_structure.csv",
        "keywords": LANE_DIR / "keyword_plan.csv",
        "negatives": LANE_DIR / "negative_keyword_plan.csv",
        "rsas": LANE_DIR / "rsa_copy_pack.csv",
        "web_bulk": LANE_DIR / "web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv",
    }
    campaign_fields, campaign_rows = read_csv(paths["campaigns"])
    keyword_fields, keyword_rows = read_csv(paths["keywords"])
    negative_fields, negative_rows = read_csv(paths["negatives"])
    rsa_fields, rsa_rows = read_csv(paths["rsas"])
    web_fields, web_rows = read_csv(paths["web_bulk"])

    del campaign_fields, keyword_fields, negative_fields, rsa_fields, web_fields

    errors: list[str] = []
    counts = {
        "campaigns": len(campaign_rows),
        "ad_groups": sum(1 for row in web_rows if row.get("Row Type") == "Ad group"),
        "keywords": len(keyword_rows),
        "negatives": len(negative_rows),
        "rsas": len(rsa_rows),
        "web_bulk_rows": len(web_rows),
    }

    for row in campaign_rows:
        if row.get("Status") != "Paused":
            errors.append(f"campaign not paused: {row.get('Campaign')}")
        if Decimal(row.get("Default max CPC", "0")) > Decimal("0.20"):
            errors.append(f"campaign CPC > 0.20: {row.get('Campaign')}")
        if row.get("Campaign type") != "Search":
            errors.append(f"non-Search campaign row: {row.get('Campaign')}")

    for row in keyword_rows:
        if row.get("Status") != "Paused":
            errors.append(f"keyword not paused: {row.get('Campaign')} / {row.get('Keyword')}")
        if row.get("Match type") not in {"Exact match", "Phrase match"}:
            errors.append(f"invalid keyword match type: {row.get('Match type')}")
        if Decimal(row.get("Max CPC cap", "0")) > Decimal("0.20"):
            errors.append(f"keyword CPC > 0.20: {row.get('Campaign')} / {row.get('Keyword')}")
        validate_final_url(row.get("Final URL", ""), country_code_from_campaign(row.get("Campaign", "")), errors)

    for row in negative_rows:
        if row.get("Status") != "Paused import row":
            errors.append(f"negative row unexpected status: {row.get('Campaign')} / {row.get('Negative keyword')}")

    for row in rsa_rows:
        if row.get("Status") != "Paused":
            errors.append(f"RSA not paused: {row.get('Campaign')} / {row.get('Ad group')}")
        validate_final_url(row.get("Final URL", ""), country_code_from_campaign(row.get("Campaign", "")), errors)

    for row in web_rows:
        row_text = " ".join(str(value).lower() for value in row.values() if value)
        if any(pattern in row_text for pattern in PROHIBITED_ROW_PATTERNS):
            # "Shopping" is allowed only inside negative keywords, not as a campaign/product edit row.
            if row.get("Row Type") not in {"Negative keyword"}:
                errors.append(f"prohibited row text in {row.get('Row Type')}: {row.get('Campaign')}")
        if row.get("Row Type") == "Campaign" and row.get("Campaign status") != "Paused":
            errors.append(f"web campaign not paused: {row.get('Campaign')}")
        if row.get("Row Type") == "Ad group":
            if row.get("Ad group status") != "Paused":
                errors.append(f"web ad group not paused: {row.get('Campaign')} / {row.get('Ad group')}")
            if Decimal(row.get("Default max. CPC", "0")) > Decimal("0.20"):
                errors.append(f"web ad group CPC > 0.20: {row.get('Campaign')} / {row.get('Ad group')}")
        if row.get("Row Type") == "Keyword":
            if row.get("Keyword status") != "Paused":
                errors.append(f"web keyword not paused: {row.get('Campaign')} / {row.get('Keyword')}")
            if row.get("Type") not in {"Exact", "Phrase", "Exact match", "Phrase match"}:
                errors.append(f"web keyword invalid match type: {row.get('Type')}")
            validate_final_url(row.get("Final URL", ""), country_code_from_campaign(row.get("Campaign", "")), errors)
        if row.get("Row Type") == "Ad":
            if row.get("Ad status") != "Paused":
                errors.append(f"web ad not paused: {row.get('Campaign')} / {row.get('Ad group')}")
            validate_final_url(row.get("Final URL", ""), country_code_from_campaign(row.get("Campaign", "")), errors)

    countries = sorted({country_code_from_campaign(row["Campaign"]) for row in campaign_rows})
    web_row_types = Counter(row.get("Row Type", "") for row in web_rows)
    final_url_counts = count_final_urls(keyword_rows, rsa_rows, web_rows)

    return {
        "validation_status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "counts": counts,
        "countries": countries,
        "web_row_types": dict(sorted(web_row_types.items())),
        "final_url_counts": final_url_counts,
        "max_cpc_maximum": str(max(Decimal(row["Max CPC cap"]) for row in keyword_rows)),
        "localized_country_mappings": COUNTRY_LOCALES,
        "theme_product_handles": THEME_PRODUCT_HANDLES,
        "guardrails": {
            "local_only": True,
            "live_ads_ui_or_api_touched": False,
            "requires_owner_approval_before_import": True,
            "all_importable_entities_paused": not errors,
            "positive_keyword_match_types": ["Exact match", "Phrase match"],
            "max_cpc_limit": "0.20",
            "preferred_existing_max_cpc_retained": "0.15 or lower",
            "prohibited_google_ads_surfaces_present": False,
        },
    }


def validate_final_url(url: str, country_code: str, errors: list[str]) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "www.dresslikemommy.com":
        errors.append(f"invalid final URL host: {url}")
    if "/products/" not in parsed.path:
        errors.append(f"final URL is not a product URL: {url}")
    if f"country={country_code}" not in parsed.query.split("&"):
        errors.append(f"final URL missing country={country_code}: {url}")
    locale = COUNTRY_LOCALES.get(country_code)
    if locale and not parsed.path.startswith(f"/{locale}/products/"):
        errors.append(f"localized market URL missing /{locale}/ prefix: {url}")
    if country_code in COUNTRY_LOCALES and re.fullmatch(rf"/{COUNTRY_LOCALES[country_code]}/products/[^?]+", parsed.path) and not parsed.query:
        errors.append(f"bare language-only URL found: {url}")


def count_final_urls(keyword_rows: list[dict[str, str]], rsa_rows: list[dict[str, str]], web_rows: list[dict[str, str]]) -> dict[str, object]:
    by_country: dict[str, Counter[str]] = defaultdict(Counter)
    for row in keyword_rows + rsa_rows:
        by_country[country_code_from_campaign(row["Campaign"])][row["Final URL"]] += 1
    for row in web_rows:
        if row.get("Final URL"):
            by_country[country_code_from_campaign(row["Campaign"])][row["Final URL"]] += 1
    return {country: dict(counter) for country, counter in sorted(by_country.items())}


def main() -> None:
    keyword_changes = refresh_urls(LANE_DIR / "keyword_plan.csv")
    rsa_changes = refresh_urls(LANE_DIR / "rsa_copy_pack.csv")
    web_bulk_changes = refresh_urls(LANE_DIR / "web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv")
    change_summary = {
        "keyword_url_changes": keyword_changes,
        "rsa_url_changes": rsa_changes,
        "web_bulk_url_changes": web_bulk_changes,
    }
    update_manifest(LANE_DIR / "manifest.json", change_summary)
    write_final_url_mapping()
    summary = {
        **change_summary,
        **validate(),
    }
    (LANE_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if summary["validation_status"] != "PASS":
        raise SystemExit("validation failed; see summary.json")


if __name__ == "__main__":
    main()
