#!/usr/bin/env python3
"""Build a paused-only Google Ads Editor import packet for Brand Search."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-google-ads-brand-paused-editor-import"
)
NEGATIVE_SOURCE = ROOT / "negative-keywords-import.txt"

CAMPAIGN = "DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429"
FINAL_URL = "https://www.dresslikemommy.com/"

EXACT_KEYWORDS = [
    "dress like mommy",
    "dresslikemommy",
    "dresslikemommy.com",
    "dress like mommy store",
    "dress like mommy shop",
    "dlm dresses",
    "dress like mommy outfits",
    "dress like mommy matching",
]

PHRASE_KEYWORDS = [
    "dress like mommy",
    "dresslikemommy",
    "dress like mommy store",
    "dress like mommy shop",
]

HEADLINES = [
    "Dress Like Mommy Official",
    "Mommy and Me Outfits",
    "Matching Family Outfits",
    "Mother Daughter Dresses",
    "Family Matching Styles",
    "Shop Matching Outfits",
    "Dress Like Mommy Store",
    "Matching Dresses",
    "Matching Swimwear",
    "Family Pajamas",
    "New Styles Weekly",
    "Mom And Daughter Looks",
    "Daddy And Me Outfits",
    "Secure Checkout",
    "Official Online Store",
]

DESCRIPTIONS = [
    "Official Dress Like Mommy shop for coordinated family outfits, dresses, and swim styles.",
    "Shop mommy and me, daddy and me, and family matching looks in one place.",
    "Find matching styles for photos, vacations, birthdays, and everyday family moments.",
    "Browse curated matching outfits by family role, size, and occasion.",
]


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def union_fieldnames(named_fields: list[list[str]]) -> list[str]:
    fields: list[str] = []
    seen: set[str] = set()
    for group in named_fields:
        for field in group:
            if field not in seen:
                fields.append(field)
                seen.add(field)
    return fields


def parse_negative_keyword(line: str) -> tuple[str, str]:
    value = line.strip()
    if not value:
        raise ValueError("blank negative keyword")
    if value.startswith("[") and value.endswith("]"):
        return value[1:-1], "Exact"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1], "Phrase"
    return value, "Broad"


def load_negative_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in NEGATIVE_SOURCE.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        keyword, match_type = parse_negative_keyword(value)
        rows.append(
            {
                "Campaign": CAMPAIGN,
                "Keyword": keyword,
                "Match type": match_type,
                "Type": "Campaign negative",
                "Comment": "Master Negatives - DLM import row.",
            }
        )
    return rows


def normalize_negative_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Return the campaign-level negatives actually safe for Ads Editor posting.

    Google Ads Editor's campaign-negative bulk tool dedupes exact row repeats.
    It also flags exact+phrase pairs for the same term as near duplicates. For
    negative keywords, phrase already covers the exact single-term query, so the
    narrower exact duplicate is removed before the final paused post packet.
    """

    deduped_rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    duplicate_rows_removed = 0
    for row in rows:
        key = (row["Keyword"].strip().lower(), row["Match type"].strip())
        if key in seen:
            duplicate_rows_removed += 1
            continue
        seen.add(key)
        deduped_rows.append(row)

    match_types_by_keyword: dict[str, set[str]] = {}
    for row in deduped_rows:
        match_types_by_keyword.setdefault(row["Keyword"].strip().lower(), set()).add(
            row["Match type"].strip()
        )

    final_rows: list[dict[str, str]] = []
    redundant_exact_rows_removed = 0
    for row in deduped_rows:
        keyword_key = row["Keyword"].strip().lower()
        if (
            row["Match type"].strip() == "Exact"
            and "Phrase" in match_types_by_keyword.get(keyword_key, set())
        ):
            redundant_exact_rows_removed += 1
            continue
        final_rows.append(row)

    return final_rows, {
        "negative_source_rows": len(rows),
        "duplicate_rows_removed": duplicate_rows_removed,
        "redundant_exact_rows_removed": redundant_exact_rows_removed,
        "negative_rows_ready_for_editor": len(final_rows),
    }


def validate_copy() -> None:
    for headline in HEADLINES:
        if len(headline) > 30:
            raise ValueError(f"headline too long: {headline!r}")
    for description in DESCRIPTIONS:
        if len(description) > 90:
            raise ValueError(f"description too long: {description!r}")
    forbidden = ("free shipping", "free return", "free returns", "30-day return")
    copy = " ".join(HEADLINES + DESCRIPTIONS).lower()
    for phrase in forbidden:
        if phrase in copy:
            raise ValueError(f"unsupported claim in ad copy: {phrase}")


def build_packet() -> dict[str, object]:
    validate_copy()

    auto_dir = OUTPUT_DIR / "auto_import_safe_paused_core"
    web_dir = OUTPUT_DIR / "web_bulk_preview_templates"
    qa_dir = OUTPUT_DIR / "manual_qa_and_rollback"

    campaign_settings = [
        {
            "Campaign": CAMPAIGN,
            "Campaign type": "Search",
            "Campaign status": "Paused",
            "Campaign daily budget": "10.00",
            "Bid strategy type": "Maximize conversion value",
            "Networks": "Google Search",
            "Languages": "en",
            "Comment": (
                "Paused-only Brand Search shell. Do not post from Google Ads Editor unless "
                "campaign, ad groups, keywords, and ads all remain Paused."
            ),
        }
    ]
    write_csv(
        auto_dir / "01_campaign_settings.csv",
        campaign_settings,
        [
            "Campaign",
            "Campaign type",
            "Campaign status",
            "Campaign daily budget",
            "Bid strategy type",
            "Networks",
            "Languages",
            "Comment",
        ],
    )

    locations = [
        {
            "Campaign": CAMPAIGN,
            "Location ID": "2840",
            "Location": "United States",
            "Type": "",
            "Bid adjustment": "",
            "Comment": "United States only. Verify location option is people in or regularly in targeted locations.",
        }
    ]
    write_csv(
        auto_dir / "02_campaign_locations.csv",
        locations,
        ["Campaign", "Location ID", "Location", "Type", "Bid adjustment", "Comment"],
    )

    ad_groups = [
        {
            "Campaign": CAMPAIGN,
            "Ad group": "Brand - Exact",
            "Ad group status": "Paused",
            "Max. CPC": "",
            "Comment": "Paused exact-brand ad group.",
        },
        {
            "Campaign": CAMPAIGN,
            "Ad group": "Brand - Phrase",
            "Ad group status": "Paused",
            "Max. CPC": "",
            "Comment": "Paused phrase-brand ad group.",
        },
    ]
    write_csv(
        auto_dir / "03_ad_groups.csv",
        ad_groups,
        ["Campaign", "Ad group", "Ad group status", "Max. CPC", "Comment"],
    )

    keyword_rows: list[dict[str, str]] = []
    for keyword in EXACT_KEYWORDS:
        keyword_rows.append(
            {
                "Campaign": CAMPAIGN,
                "Ad group": "Brand - Exact",
                "Keyword": keyword,
                "Match type": "Exact",
                "Status": "Paused",
                "Final URL": FINAL_URL,
                "Max. CPC": "",
                "Comment": "Paused Brand Search exact keyword.",
            }
        )
    for keyword in PHRASE_KEYWORDS:
        keyword_rows.append(
            {
                "Campaign": CAMPAIGN,
                "Ad group": "Brand - Phrase",
                "Keyword": keyword,
                "Match type": "Phrase",
                "Status": "Paused",
                "Final URL": FINAL_URL,
                "Max. CPC": "",
                "Comment": "Paused Brand Search phrase keyword.",
            }
        )
    write_csv(
        auto_dir / "04_keywords.csv",
        keyword_rows,
        [
            "Campaign",
            "Ad group",
            "Keyword",
            "Match type",
            "Status",
            "Final URL",
            "Max. CPC",
            "Comment",
        ],
    )

    negative_source_rows = load_negative_source_rows()
    negative_rows, negative_stats = normalize_negative_rows(negative_source_rows)
    write_csv(
        auto_dir / "05_campaign_negative_keywords_reference.csv",
        negative_rows,
        ["Campaign", "Keyword", "Match type", "Type", "Comment"],
    )
    write_tsv(
        auto_dir / "05_campaign_negative_keywords_editor_bulk_paste.tsv",
        [{"Keyword": row["Keyword"], "Type": row["Match type"]} for row in negative_rows],
        ["Keyword", "Type"],
    )

    ad_fieldnames = [
        "Campaign",
        "Ad group",
        "Ad type",
        "Status",
        "Final URL",
        "Path 1",
        "Path 2",
    ]
    for idx in range(1, 16):
        ad_fieldnames.extend([f"Headline {idx}", f"Headline {idx} position"])
    for idx in range(1, 5):
        ad_fieldnames.extend([f"Description {idx}", f"Description {idx} position"])
    ad_fieldnames.append("Comment")

    ad_rows: list[dict[str, str]] = []
    for ad_group in ("Brand - Exact", "Brand - Phrase"):
        row = {
            "Campaign": CAMPAIGN,
            "Ad group": ad_group,
            "Ad type": "Responsive search ad",
            "Status": "Paused",
            "Final URL": FINAL_URL,
            "Path 1": "matching",
            "Path 2": "outfits",
            "Comment": "Paused RSA. Verify Headline 1 is pinned to position 1 after import.",
        }
        for idx, headline in enumerate(HEADLINES, start=1):
            row[f"Headline {idx}"] = headline
            row[f"Headline {idx} position"] = "1" if idx == 1 else ""
        for idx, description in enumerate(DESCRIPTIONS, start=1):
            row[f"Description {idx}"] = description
            row[f"Description {idx} position"] = ""
        ad_rows.append(row)
    write_csv(auto_dir / "06_responsive_search_ads.csv", ad_rows, ad_fieldnames)

    web_campaign_rows = [
        {
            "Row Type": "Campaign",
            "Action": "Add",
            "Campaign status": "Paused",
            "Campaign ID": "",
            "Campaign": CAMPAIGN,
            "Campaign type": "Search",
            "Networks": "Google search",
            "Budget": "10.00",
            "Delivery method": "Standard",
            "Budget type": "Daily",
            "Bid strategy type": "Maximize Conversion Value",
            "Bid strategy": "",
            "Campaign start date": "",
            "Campaign end date": "",
            "Language": "English",
            "Location": "United States",
            "Exclusion": "",
            "Devices": "",
            "Label": "",
            "Target CPA": "",
            "Target ROAS": "",
            "Display URL option": "",
            "Website description": "",
            "Target Impression Share": "",
            "Max CPC Bid Limit for Target IS": "",
            "Location Goal for Target IS": "",
            "Tracking template": "",
            "Final URL suffix": "",
            "Custom parameter": "",
            "Inventory type": "",
            "Campaign subtype": "",
            "Video ad formats": "",
            "EU political ads": "",
        }
    ]
    web_campaign_fields = [
        "Row Type",
        "Action",
        "Campaign status",
        "Campaign ID",
        "Campaign",
        "Campaign type",
        "Networks",
        "Budget",
        "Delivery method",
        "Budget type",
        "Bid strategy type",
        "Bid strategy",
        "Campaign start date",
        "Campaign end date",
        "Language",
        "Location",
        "Exclusion",
        "Devices",
        "Label",
        "Target CPA",
        "Target ROAS",
        "Display URL option",
        "Website description",
        "Target Impression Share",
        "Max CPC Bid Limit for Target IS",
        "Location Goal for Target IS",
        "Tracking template",
        "Final URL suffix",
        "Custom parameter",
        "Inventory type",
        "Campaign subtype",
        "Video ad formats",
        "EU political ads",
    ]
    write_csv(web_dir / "01_campaign_web_bulk.csv", web_campaign_rows, web_campaign_fields)

    web_ad_group_rows = [
        {
            "Row Type": "Ad group",
            "Action": "Add",
            "Ad group status": row["Ad group status"],
            "Campaign ID": "",
            "Campaign": CAMPAIGN,
            "Ad group ID": "",
            "Ad group": row["Ad group"],
            "Ad group type": "Standard",
            "Ad rotation": "Optimize",
            "Default max. CPC": "",
            "CPC%": "",
            "Max. CPM": "",
            "Max. CPV": "",
            "Target CPA": "",
            "Target CPM": "",
            "TrueView target CPV": "",
            "Label": "",
            "Tracking template": "",
            "Final URL suffix": "",
            "Custom parameter": "",
            "Target ROAS": "",
        }
        for row in ad_groups
    ]
    web_ad_group_fields = [
        "Row Type",
        "Action",
        "Ad group status",
        "Campaign ID",
        "Campaign",
        "Ad group ID",
        "Ad group",
        "Ad group type",
        "Ad rotation",
        "Default max. CPC",
        "CPC%",
        "Max. CPM",
        "Max. CPV",
        "Target CPA",
        "Target CPM",
        "TrueView target CPV",
        "Label",
        "Tracking template",
        "Final URL suffix",
        "Custom parameter",
        "Target ROAS",
    ]
    write_csv(web_dir / "02_ad_groups_web_bulk.csv", web_ad_group_rows, web_ad_group_fields)

    web_keyword_rows = [
        {
            "Row Type": "Keyword",
            "Action": "Add",
            "Keyword status": row["Status"],
            "Campaign ID": "",
            "Campaign": CAMPAIGN,
            "Ad group ID": "",
            "Ad group": row["Ad group"],
            "Keyword ID": "",
            "Keyword": row["Keyword"],
            "Type": f"{row['Match type']} match",
            "Label": "",
            "Default max. CPC": "",
            "Max. CPV": "",
            "Final URL": row["Final URL"],
            "Mobile final URL": "",
            "Final URL suffix": "",
            "Tracking template": "",
            "Custom parameter": "",
        }
        for row in keyword_rows
    ]
    web_keyword_fields = [
        "Row Type",
        "Action",
        "Keyword status",
        "Campaign ID",
        "Campaign",
        "Ad group ID",
        "Ad group",
        "Keyword ID",
        "Keyword",
        "Type",
        "Label",
        "Default max. CPC",
        "Max. CPV",
        "Final URL",
        "Mobile final URL",
        "Final URL suffix",
        "Tracking template",
        "Custom parameter",
    ]
    write_csv(web_dir / "03_keywords_web_bulk.csv", web_keyword_rows, web_keyword_fields)

    web_negative_rows = [
        {
            "Row Type": "Negative keyword",
            "Action": "Add",
            "Keyword status": "Paused",
            "Level": "Campaign",
            "Campaign ID": "",
            "Campaign": row["Campaign"],
            "Ad group ID": "",
            "Ad group": "",
            "Keyword ID": "",
            "Negative keyword": row["Keyword"],
            "Type": f"{row['Match type']} match",
        }
        for row in negative_rows
    ]
    web_negative_fields = [
        "Row Type",
        "Action",
        "Keyword status",
        "Level",
        "Campaign ID",
        "Campaign",
        "Ad group ID",
        "Ad group",
        "Keyword ID",
        "Negative keyword",
        "Type",
    ]
    write_csv(web_dir / "04_campaign_negative_keywords_web_bulk.csv", web_negative_rows, web_negative_fields)

    web_ad_fields = [
        "Row Type",
        "Action",
        "Ad status",
        "Campaign ID",
        "Campaign",
        "Ad group ID",
        "Ad group",
        "Ad ID",
        "Ad type",
        "Label",
    ]
    for idx in range(1, 16):
        web_ad_fields.append(f"Headline {idx}")
    for idx in range(1, 5):
        web_ad_fields.append(f"Description {idx}")
    for idx in range(1, 16):
        web_ad_fields.append(f"Headline {idx} position")
    for idx in range(1, 5):
        web_ad_fields.append(f"Description {idx} position")
    web_ad_fields.extend(
        [
            "Path 1",
            "Path 2",
            "Final URL",
            "Mobile final URL",
            "Tracking template",
            "Final URL suffix",
            "Custom parameter",
        ]
    )

    web_ad_rows: list[dict[str, str]] = []
    for row in ad_rows:
        web_row = {
            "Row Type": "Ad",
            "Action": "Add",
            "Ad status": row["Status"],
            "Campaign ID": "",
            "Campaign": row["Campaign"],
            "Ad group ID": "",
            "Ad group": row["Ad group"],
            "Ad ID": "",
            "Ad type": row["Ad type"],
            "Label": "",
            "Path 1": row["Path 1"],
            "Path 2": row["Path 2"],
            "Final URL": row["Final URL"],
            "Mobile final URL": "",
            "Tracking template": "",
            "Final URL suffix": "",
            "Custom parameter": "",
        }
        for idx in range(1, 16):
            web_row[f"Headline {idx}"] = row[f"Headline {idx}"]
            web_row[f"Headline {idx} position"] = row[f"Headline {idx} position"]
        for idx in range(1, 5):
            web_row[f"Description {idx}"] = row[f"Description {idx}"]
            web_row[f"Description {idx} position"] = row[f"Description {idx} position"]
        web_ad_rows.append(web_row)
    write_csv(web_dir / "05_responsive_search_ads_web_bulk.csv", web_ad_rows, web_ad_fields)

    combined_web_fields = union_fieldnames(
        [
            web_campaign_fields,
            web_ad_group_fields,
            web_keyword_fields,
            web_negative_fields,
            web_ad_fields,
        ]
    )
    combined_web_rows = (
        web_campaign_rows
        + web_ad_group_rows
        + web_keyword_rows
        + web_negative_rows
        + web_ad_rows
    )
    write_csv(
        web_dir / "00_brand_search_paused_combined_web_bulk.csv",
        combined_web_rows,
        combined_web_fields,
    )

    checklist_rows = [
        {
            "Check": "Campaign status",
            "Required result": "Paused",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "Ad group, keyword, and ad statuses",
            "Required result": "Paused",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "Networks",
            "Required result": "Google Search only; Search partners off; Display off",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "Location",
            "Required result": "United States only",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "Negatives",
            "Required result": "Campaign-level negatives pasted as campaign-level negatives from Master Negatives - DLM",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "EU political ads declaration",
            "Required result": "No, does not have EU political ads",
            "Status": "Required before posting/import apply",
        },
        {
            "Check": "Launch gate",
            "Required result": "Do not enable; final launch gate remains blocked",
            "Status": "Blocked",
        },
    ]
    write_csv(
        qa_dir / "paused_import_qa_checklist.csv",
        checklist_rows,
        ["Check", "Required result", "Status"],
    )

    manifest = {
        "generated": "2026-04-29",
        "mode": "PAUSED_ONLY_GOOGLE_ADS_EDITOR_IMPORT_PACKET",
        "campaign": CAMPAIGN,
        "source_guide": "Google-Ads-Campaign-Setup-Guide.md",
        "shopping_baseline_campaign": "DLM_US_STANDARD_SHOPPING_TEST_PAID_READY",
        "shopping_baseline_campaign_id": "23802638621",
        "negative_source": str(NEGATIVE_SOURCE.relative_to(ROOT)),
        **negative_stats,
        "negative_rows": len(negative_rows),
        "keyword_rows": len(keyword_rows),
        "rsa_rows": len(ad_rows),
        "all_imported_statuses": "Paused",
        "live_launch_allowed": False,
        "auto_import_files": [
            "auto_import_safe_paused_core/01_campaign_settings.csv",
            "auto_import_safe_paused_core/02_campaign_locations.csv",
            "auto_import_safe_paused_core/03_ad_groups.csv",
            "auto_import_safe_paused_core/04_keywords.csv",
            "auto_import_safe_paused_core/05_campaign_negative_keywords_editor_bulk_paste.tsv",
            "auto_import_safe_paused_core/05_campaign_negative_keywords_reference.csv",
            "auto_import_safe_paused_core/06_responsive_search_ads.csv",
        ],
        "web_bulk_preview_files": [
            "web_bulk_preview_templates/00_brand_search_paused_combined_web_bulk.csv",
            "web_bulk_preview_templates/01_campaign_web_bulk.csv",
            "web_bulk_preview_templates/02_ad_groups_web_bulk.csv",
            "web_bulk_preview_templates/03_keywords_web_bulk.csv",
            "web_bulk_preview_templates/04_campaign_negative_keywords_web_bulk.csv",
            "web_bulk_preview_templates/05_responsive_search_ads_web_bulk.csv",
        ],
        "qa_files": ["manual_qa_and_rollback/paused_import_qa_checklist.csv"],
    }

    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Google Ads Brand Search Paused Editor Import",
                "",
                f"Campaign: `{CAMPAIGN}`",
                "Mode: `PAUSED_ONLY`; do not enable live spend.",
                "",
                "This packet is the safe Brand Search path when Google Ads web draft creation only exposes `Publish campaign`.",
                "Import through Google Ads Editor, review the proposed changes, and post only if every campaign, ad group, keyword, and ad row remains paused.",
                "",
                "The packet intentionally uses a unique campaign name so it cannot restore or mutate the removed legacy `Search - Brand` campaign.",
                "",
                "Import order:",
                "",
                "Google Ads Editor files:",
                "1. `auto_import_safe_paused_core/01_campaign_settings.csv`",
                "2. `auto_import_safe_paused_core/02_campaign_locations.csv`",
                "3. `auto_import_safe_paused_core/03_ad_groups.csv`",
                "4. `auto_import_safe_paused_core/04_keywords.csv`",
                "5. Select the new campaign in Editor, open `Keywords & targeting > Keywords, Negative`, click `Make multiple changes`, choose `Use selected destinations` and `Add as campaign-level negative keywords`, then paste `auto_import_safe_paused_core/05_campaign_negative_keywords_editor_bulk_paste.tsv`.",
                "6. `auto_import_safe_paused_core/06_responsive_search_ads.csv`",
                "",
                "`auto_import_safe_paused_core/05_campaign_negative_keywords_reference.csv` is audit evidence only; use the TSV with Editor's campaign-negative bulk flow.",
                "",
                "Google Ads web bulk-preview files:",
                "- Preferred single-file preview: `web_bulk_preview_templates/00_brand_search_paused_combined_web_bulk.csv`",
                "- Split-file fallback:",
                "  1. `web_bulk_preview_templates/01_campaign_web_bulk.csv`",
                "  2. `web_bulk_preview_templates/02_ad_groups_web_bulk.csv`",
                "  3. `web_bulk_preview_templates/03_keywords_web_bulk.csv`",
                "  4. `web_bulk_preview_templates/04_campaign_negative_keywords_web_bulk.csv`",
                "  5. `web_bulk_preview_templates/05_responsive_search_ads_web_bulk.csv`",
                "",
                "Required readback before posting/applying:",
                "- Campaign status is `Paused`.",
                "- Both ad groups are `Paused`.",
                "- All keywords are `Paused`.",
                "- Both responsive search ads are `Paused`.",
                "- Networks show Google Search only; Search partners and Display are off.",
                "- Location is United States only.",
                "- Campaign-level negatives imported from `Master Negatives - DLM`.",
                "- EU political ads is set to `No, does not have EU political ads`.",
                "",
                "Do not enable the campaign until the final launch gate passes and the operator explicitly approves live spend.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return manifest


def main() -> None:
    manifest = build_packet()
    print(json.dumps({"output_dir": str(OUTPUT_DIR), **manifest}, indent=2))


if __name__ == "__main__":
    main()
