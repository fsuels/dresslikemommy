#!/usr/bin/env python3
"""Build local-only paused international Search infrastructure artifacts."""

from __future__ import annotations

import csv
import importlib.util
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = Path(__file__).resolve().parent
US_TEMPLATE_SCRIPT = ROOT / "ops/scripts/build_google_ads_nonbrand_paused_search_rebuild.py"
US_EXISTING_CAMPAIGN_ID = "23827590655"
US_EXISTING_CAMPAIGN = "DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506"

spec = importlib.util.spec_from_file_location("us_nonbrand_template", US_TEMPLATE_SCRIPT)
us_template = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(us_template)

THEMES = us_template.THEMES
NEGATIVES = us_template.NEGATIVES
WEB_FIELDS = us_template.WEB_FIELDS

COUNTRIES = [
    {
        "code": "GB",
        "country": "United Kingdom",
        "tier": "Priority English",
        "readiness": "Import-ready after owner approval and action-time readbacks",
        "budget": "2.00",
        "max_cpc": "0.15",
        "language": "en",
        "landing_policy": "English collection pages only",
    },
    {
        "code": "CA",
        "country": "Canada",
        "tier": "Priority English",
        "readiness": "Import-ready after owner approval and action-time readbacks",
        "budget": "2.00",
        "max_cpc": "0.15",
        "language": "en",
        "landing_policy": "English collection pages only; French Canada deferred",
    },
    {
        "code": "AU",
        "country": "Australia",
        "tier": "Priority English",
        "readiness": "Import-ready after owner approval and action-time readbacks",
        "budget": "2.00",
        "max_cpc": "0.15",
        "language": "en",
        "landing_policy": "English collection pages only; delivery clarity required",
    },
    {
        "code": "CH",
        "country": "Switzerland",
        "tier": "High-value watchlist",
        "readiness": "Paused shell only; local-language variants deferred pending QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until German/French/Italian routes pass QA",
    },
    {
        "code": "DK",
        "country": "Denmark",
        "tier": "High-value watchlist",
        "readiness": "Paused shell only; local-language variants deferred pending QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until Danish route and shipping clarity pass QA",
    },
    {
        "code": "DE",
        "country": "Germany",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; German build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until German route, returns, and duties pass QA",
    },
    {
        "code": "NL",
        "country": "Netherlands",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; Dutch build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until Dutch route and checkout pass QA",
    },
    {
        "code": "SE",
        "country": "Sweden",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; Swedish build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until Swedish route and shipping clarity pass QA",
    },
    {
        "code": "FR",
        "country": "France",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; French build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until French route, returns, and duties pass QA",
    },
    {
        "code": "BE",
        "country": "Belgium",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; local-language variants deferred pending QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until French/Dutch route quality passes QA",
    },
    {
        "code": "ES",
        "country": "Spain",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; Spanish build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until Spanish route and checkout pass QA",
    },
    {
        "code": "IT",
        "country": "Italy",
        "tier": "Broader ecommerce test",
        "readiness": "Paused English shell only; Italian build held for localization QA",
        "budget": "1.00",
        "max_cpc": "0.12",
        "language": "en",
        "landing_policy": "English only until Italian route and checkout pass QA",
    },
    {
        "code": "PL",
        "country": "Poland",
        "tier": "Lower-CPC discovery",
        "readiness": "Paused English discovery shell only; Polish build held for QA",
        "budget": "1.00",
        "max_cpc": "0.10",
        "language": "en",
        "landing_policy": "English only until Polish route, returns, and duties pass QA",
    },
    {
        "code": "CZ",
        "country": "Czechia",
        "tier": "Lower-CPC discovery",
        "readiness": "Paused English discovery shell only; Czech build held for QA",
        "budget": "1.00",
        "max_cpc": "0.10",
        "language": "en",
        "landing_policy": "English only until Czech route and checkout pass QA",
    },
    {
        "code": "RO",
        "country": "Romania",
        "tier": "Lower-CPC discovery",
        "readiness": "Paused English discovery shell only; Romanian build held for QA",
        "budget": "1.00",
        "max_cpc": "0.10",
        "language": "en",
        "landing_policy": "English only until Romanian route and checkout pass QA",
    },
    {
        "code": "GR",
        "country": "Greece",
        "tier": "Lower-CPC discovery",
        "readiness": "Paused English discovery shell only; Greek build held for QA",
        "budget": "1.00",
        "max_cpc": "0.10",
        "language": "en",
        "landing_policy": "English only until Greek route, returns, and duties pass QA",
    },
    {
        "code": "PT",
        "country": "Portugal",
        "tier": "Lower-CPC discovery",
        "readiness": "Paused English discovery shell only; Portuguese build held for QA",
        "budget": "1.00",
        "max_cpc": "0.10",
        "language": "en",
        "landing_policy": "English only until Portuguese route and checkout pass QA",
    },
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def campaign_name(country: dict[str, str]) -> str:
    return f"DLM_{country['code']}_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"


def ad_group_name(theme: str, match: str) -> str:
    return f"{theme} - {match}"


def match_label(match: str) -> str:
    return "Exact match" if match == "Exact" else "Phrase match"


def validate() -> None:
    country_codes = [country["code"] for country in COUNTRIES]
    if len(country_codes) != len(set(country_codes)):
        raise ValueError("duplicate country code in plan")
    if "US" in country_codes:
        raise ValueError("US already has paused campaign 23827590655; do not duplicate it")
    for country in COUNTRIES:
        if Decimal(country["max_cpc"]) > Decimal("0.20"):
            raise ValueError(f"CPC cap too high for {country['code']}: {country['max_cpc']}")
        if Decimal(country["budget"]) > Decimal("2.00"):
            raise ValueError(f"paused shell budget too high for {country['code']}: {country['budget']}")
    for theme in THEMES:
        for headline in theme["headlines"]:
            if len(headline) > 30:
                raise ValueError(f"headline too long ({len(headline)}): {headline}")
        for description in theme["descriptions"]:
            if len(description) > 90:
                raise ValueError(f"description too long ({len(description)}): {description}")
        copy = " ".join(theme["headlines"] + theme["descriptions"]).lower()
        for forbidden in ("free shipping", "fast shipping", "free returns", "30-day"):
            if forbidden in copy:
                raise ValueError(f"unsupported claim in ad copy: {forbidden}")


def build_web_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for country in COUNTRIES:
        campaign = campaign_name(country)
        rows.append(
            {
                "Row Type": "Campaign",
                "Action": "Add",
                "Campaign status": "Paused",
                "Campaign": campaign,
                "Campaign type": "Search",
                "Networks": "Google search",
                "Budget": country["budget"],
                "Delivery method": "Standard",
                "Budget type": "Daily",
                "Bid strategy type": "Manual CPC",
                "Language": country["language"],
                "Location": country["country"],
                "EU political ads": "No",
            }
        )

        for theme in THEMES:
            for match in ("Exact", "Phrase"):
                rows.append(
                    {
                        "Row Type": "Ad group",
                        "Action": "Add",
                        "Campaign": campaign,
                        "Ad group status": "Paused",
                        "Ad group": ad_group_name(theme["theme"], match),
                        "Ad group type": "Standard",
                        "Ad rotation": "Optimize",
                        "Default max. CPC": country["max_cpc"],
                    }
                )

        for theme in THEMES:
            for match in ("Exact", "Phrase"):
                key = "exact" if match == "Exact" else "phrase"
                for keyword in theme[key]:
                    rows.append(
                        {
                            "Row Type": "Keyword",
                            "Action": "Add",
                            "Campaign": campaign,
                            "Ad group": ad_group_name(theme["theme"], match),
                            "Keyword status": "Paused",
                            "Keyword": keyword,
                            "Type": match_label(match),
                            "Final URL": theme["url"],
                        }
                    )

        for keyword, match in NEGATIVES:
            rows.append(
                {
                    "Row Type": "Negative keyword",
                    "Action": "Add",
                    "Campaign": campaign,
                    "Keyword status": "Paused",
                    "Type": f"{match} match",
                    "Level": "Campaign",
                    "Negative keyword": keyword,
                }
            )

        for theme in THEMES:
            for match in ("Exact", "Phrase"):
                row = {
                    "Row Type": "Ad",
                    "Action": "Add",
                    "Campaign": campaign,
                    "Ad group": ad_group_name(theme["theme"], match),
                    "Ad status": "Paused",
                    "Ad type": "Responsive search ad",
                    "Final URL": theme["url"],
                    "Path 1": theme["path_1"],
                    "Path 2": theme["path_2"],
                }
                for idx, headline in enumerate(theme["headlines"], start=1):
                    row[f"Headline {idx}"] = headline
                for idx, description in enumerate(theme["descriptions"], start=1):
                    row[f"Description {idx}"] = description
                rows.append(row)

    return rows


def build_country_tier_plan() -> list[dict[str, str]]:
    rows = [
        {
            "Country": "United States",
            "Code": "US",
            "Tier": "Existing controlled Search",
            "Campaign": US_EXISTING_CAMPAIGN,
            "Live campaign ID": US_EXISTING_CAMPAIGN_ID,
            "This packet action": "Do not duplicate; use as template only",
            "Language": "en",
            "Location": "United States",
            "Paused shell daily budget": "2.00",
            "Max CPC cap": "0.15",
            "Import readiness": "Already created paused; activation still approval-gated",
            "Landing policy": "Existing English landing-page set",
        }
    ]
    for country in COUNTRIES:
        rows.append(
            {
                "Country": country["country"],
                "Code": country["code"],
                "Tier": country["tier"],
                "Campaign": campaign_name(country),
                "Live campaign ID": "",
                "This packet action": "Local import draft only; no Ads UI/API action",
                "Language": country["language"],
                "Location": country["country"],
                "Paused shell daily budget": country["budget"],
                "Max CPC cap": country["max_cpc"],
                "Import readiness": country["readiness"],
                "Landing policy": country["landing_policy"],
            }
        )
    return rows


def build_campaign_structure() -> list[dict[str, str]]:
    rows = []
    for country in COUNTRIES:
        rows.append(
            {
                "Campaign": campaign_name(country),
                "Country": country["country"],
                "Code": country["code"],
                "Status": "Paused",
                "Campaign type": "Search",
                "Networks": "Google Search only",
                "Language": country["language"],
                "Location": country["country"],
                "Location option": "Presence only at action-time readback",
                "Bid strategy": "Manual CPC",
                "Paused shell daily budget": country["budget"],
                "Default max CPC": country["max_cpc"],
                "Conversion goals": "No edits; inherit account-default Purchases after readback",
                "Ad groups": str(len(THEMES) * 2),
                "Keywords": str(sum(len(theme["exact"]) + len(theme["phrase"]) for theme in THEMES)),
                "Campaign negatives": str(len(NEGATIVES)),
                "RSAs": str(len(THEMES) * 2),
            }
        )
    return rows


def build_keyword_plan() -> list[dict[str, str]]:
    rows = []
    for country in COUNTRIES:
        for theme in THEMES:
            for match in ("Exact", "Phrase"):
                key = "exact" if match == "Exact" else "phrase"
                for keyword in theme[key]:
                    rows.append(
                        {
                            "Campaign": campaign_name(country),
                            "Country": country["country"],
                            "Ad group": ad_group_name(theme["theme"], match),
                            "Theme": theme["theme"],
                            "Match type": match_label(match),
                            "Keyword": keyword,
                            "Final URL": theme["url"],
                            "Max CPC cap": country["max_cpc"],
                            "Status": "Paused",
                            "Language note": "English-only seed; local-language expansion requires landing QA",
                        }
                    )
    return rows


def build_negative_plan() -> list[dict[str, str]]:
    rows = []
    for country in COUNTRIES:
        for keyword, match in NEGATIVES:
            rows.append(
                {
                    "Campaign": campaign_name(country),
                    "Country": country["country"],
                    "Level": "Campaign",
                    "Negative keyword": keyword,
                    "Match type": f"{match} match",
                    "Status": "Paused import row",
                    "Purpose": "Block low-intent, DIY, marketplace, wholesale, IP-risk, and non-shopper searches",
                }
            )
    return rows


def build_rsa_copy_pack() -> list[dict[str, str]]:
    rows = []
    for country in COUNTRIES:
        for theme in THEMES:
            for match in ("Exact", "Phrase"):
                row = {
                    "Campaign": campaign_name(country),
                    "Country": country["country"],
                    "Ad group": ad_group_name(theme["theme"], match),
                    "Final URL": theme["url"],
                    "Path 1": theme["path_1"],
                    "Path 2": theme["path_2"],
                    "Status": "Paused",
                    "Claim policy": "No free/fast shipping, reviews, bestseller, discount, or return claims",
                }
                for idx, headline in enumerate(theme["headlines"], start=1):
                    row[f"Headline {idx}"] = headline
                for idx, description in enumerate(theme["descriptions"], start=1):
                    row[f"Description {idx}"] = description
                rows.append(row)
    fields = [
        "Campaign",
        "Country",
        "Ad group",
        "Final URL",
        "Path 1",
        "Path 2",
        "Status",
        "Claim policy",
    ]
    fields.extend([f"Headline {idx}" for idx in range(1, 16)])
    fields.extend([f"Description {idx}" for idx in range(1, 5)])
    write_csv(OUTPUT_DIR / "rsa_copy_pack.csv", rows, fields)
    return rows


def build_qa_rows() -> list[dict[str, str]]:
    return [
        {
            "Check": "Approval gate",
            "Required result": "Exact owner paused international build approval before Ads UI/API import",
            "Why": "Even paused campaign creation is a Google Ads write.",
        },
        {
            "Check": "US duplication",
            "Required result": f"Do not create another US nonbrand campaign; use existing {US_EXISTING_CAMPAIGN_ID}",
            "Why": "US paused rebuild already exists and should be governed/read back, not duplicated.",
        },
        {
            "Check": "Campaign status",
            "Required result": "Every proposed import row creates paused campaigns, ad groups, keywords, and RSAs",
            "Why": "No live spend until final readback and enable approval.",
        },
        {
            "Check": "Bidding",
            "Required result": "Manual CPC with all default max CPC caps at or below $0.20",
            "Why": "Protects the 650% ROAS learning posture.",
        },
        {
            "Check": "Locations",
            "Required result": "One country per campaign; presence-only setting confirmed after import",
            "Why": "Country-level ROAS and loser/winner decisions need clean segmentation.",
        },
        {
            "Check": "Languages",
            "Required result": "English-only initial shells; local-language variants only after page QA passes",
            "Why": "Language availability is not launch readiness.",
        },
        {
            "Check": "Networks",
            "Required result": "Google Search only; no Display, Search Partners, broad match, AI Max, or PMax",
            "Why": "Keeps tests controlled and query-readable.",
        },
        {
            "Check": "Conversion goals",
            "Required result": "No conversion-goal edits; read back account-default Purchases before import and before enable",
            "Why": "Conversion-goal changes are explicitly blocked.",
        },
        {
            "Check": "Activation",
            "Required result": "Separate explicit enable approval after policy, location, landing, Merchant/catalog, and economics gates",
            "Why": "Paused shell creation is not launch approval.",
        },
    ]


def write_markdown_report(manifest: dict[str, object]) -> None:
    lines = [
        "# Google Ads International Search Infrastructure Packet",
        "",
        "Date: 2026-05-07",
        "",
        "Scope: local-only planning and build artifacts for segmented paused country Search tests. No Google Ads UI/API, campaign creation, budget, bid, status, keyword, conversion-goal, Standard Shopping, PMax, Remarketing, Merchant, or Shopify writes were made.",
        "",
        "## Template Read",
        "",
        f"- Existing paused US nonbrand rebuild: `{US_EXISTING_CAMPAIGN}` / campaign `{US_EXISTING_CAMPAIGN_ID}`.",
        "- Template controls preserved: Search only, paused only, Manual CPC, exact/phrase keywords, shared campaign negatives, claim-safe RSAs.",
        "- This packet does not create or duplicate a US campaign; it clones the structure locally for non-US country shells.",
        "",
        "## Country Tier Plan",
        "",
        "- US: existing paused campaign remains the governed template; no duplicate build.",
        "- Priority English import candidates after owner approval and action-time readbacks: GB, CA, AU.",
        "- High-value watchlist paused shells: CH and DK, English-only until local route/shipping QA passes.",
        "- Broader ecommerce paused English shells: DE, NL, SE, FR, BE, ES, IT.",
        "- Lower-CPC discovery paused English shells: PL, CZ, RO, GR, PT.",
        "- Local-language keyword/RSA variants are intentionally held until the localization/shipping QA lane clears each route.",
        "",
        "## Build Summary",
        "",
        f"- Proposed non-US campaigns: `{manifest['campaigns']}`.",
        f"- Ad groups per campaign: `{manifest['ad_groups_per_campaign']}`.",
        f"- Keywords per campaign: `{manifest['keywords_per_campaign']}`.",
        f"- Campaign negatives per campaign: `{manifest['negative_keywords_per_campaign']}`.",
        f"- RSAs per campaign: `{manifest['rsas_per_campaign']}`.",
        f"- Total web-bulk rows: `{manifest['web_bulk_rows']}`.",
        "- Status everywhere: `Paused`.",
        "- Bid strategy: `Manual CPC`.",
        "- CPC caps: `$0.10` to `$0.15`; none above `$0.20`.",
        "- Networks: Google Search only.",
        "- Initial languages: `en` only.",
        "",
        "## Import Readiness",
        "",
        "These are local draft artifacts. Importing even paused campaigns is a live Google Ads write and needs the exact owner approval gate below. After any approved import, read back campaign status, location option/presence, networks, budget, bid caps, keywords, negatives, RSAs, policy/ad review, and conversion-goal inheritance before any enablement discussion.",
        "",
        "Exact approval gate required before live paused campaign creation:",
        "",
        "`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`",
        "",
        "## Files",
        "",
        "- `country_tier_plan.csv`",
        "- `campaign_structure.csv`",
        "- `keyword_plan.csv`",
        "- `negative_keyword_plan.csv`",
        "- `rsa_copy_pack.csv`",
        "- `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`",
        "- `manual_qa/intl_search_pre_import_qa.csv`",
        "- `manual_qa/approval_gate.md`",
        "- `manifest.json`",
        "",
        "## Residual Risks",
        "",
        "- English-only targeting outside English-first markets is conservative but may have limited reach and conversion quality.",
        "- Local-language campaigns need separate localized keyword and RSA packs after route, shipping, returns/duties, checkout, and catalog eligibility QA.",
        "- Google Ads bulk import field support can drift; first live step must be preview-only with zero-error readback before apply.",
        "- Presence-only location option may require UI/API confirmation after import because the template CSV does not encode it reliably.",
        "- Paused budgets are draft shell settings only; enablement requires a separate country-level economics decision.",
        "",
    ]
    (OUTPUT_DIR / "GOOGLE_ADS_INTL_SEARCH_INFRASTRUCTURE_PLAN.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_approval_gate() -> None:
    text = """# Approval Gate

Do not import, create, enable, upload, or edit anything in Google Ads from this packet until the owner gives this exact action-time approval:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

Required action-time readbacks before applying any paused import:

- Existing US nonbrand campaign `23827590655` still exists and remains paused.
- Standard Shopping is not touched.
- PMax and Remarketing are not touched.
- Conversion goals are not edited.
- Bulk upload preview returns zero errors.

Required post-import readbacks before any future enable approval:

- Campaigns, ad groups, keywords, and RSAs are paused.
- One country per campaign.
- Location option is presence-only.
- Google Search only; no Display/Search Partners.
- Manual CPC and every default max CPC is at or below `$0.20`.
- Exact/phrase keywords only; no broad keywords.
- Campaign negatives present.
- Policy/ad review is clean enough for controlled testing.
- Landing, shipping, checkout, Merchant/catalog, and economics gates pass for each country.
"""
    (OUTPUT_DIR / "manual_qa/approval_gate.md").write_text(text, encoding="utf-8")


def build_packet() -> dict[str, object]:
    validate()

    web_rows = build_web_rows()
    write_csv(
        OUTPUT_DIR / "web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv",
        web_rows,
        WEB_FIELDS,
    )
    write_csv(
        OUTPUT_DIR / "country_tier_plan.csv",
        build_country_tier_plan(),
        [
            "Country",
            "Code",
            "Tier",
            "Campaign",
            "Live campaign ID",
            "This packet action",
            "Language",
            "Location",
            "Paused shell daily budget",
            "Max CPC cap",
            "Import readiness",
            "Landing policy",
        ],
    )
    write_csv(
        OUTPUT_DIR / "campaign_structure.csv",
        build_campaign_structure(),
        [
            "Campaign",
            "Country",
            "Code",
            "Status",
            "Campaign type",
            "Networks",
            "Language",
            "Location",
            "Location option",
            "Bid strategy",
            "Paused shell daily budget",
            "Default max CPC",
            "Conversion goals",
            "Ad groups",
            "Keywords",
            "Campaign negatives",
            "RSAs",
        ],
    )
    write_csv(
        OUTPUT_DIR / "keyword_plan.csv",
        build_keyword_plan(),
        [
            "Campaign",
            "Country",
            "Ad group",
            "Theme",
            "Match type",
            "Keyword",
            "Final URL",
            "Max CPC cap",
            "Status",
            "Language note",
        ],
    )
    write_csv(
        OUTPUT_DIR / "negative_keyword_plan.csv",
        build_negative_plan(),
        [
            "Campaign",
            "Country",
            "Level",
            "Negative keyword",
            "Match type",
            "Status",
            "Purpose",
        ],
    )
    build_rsa_copy_pack()
    write_csv(
        OUTPUT_DIR / "manual_qa/intl_search_pre_import_qa.csv",
        build_qa_rows(),
        ["Check", "Required result", "Why"],
    )

    manifest = {
        "packet": str(OUTPUT_DIR.relative_to(ROOT)),
        "template_campaign": US_EXISTING_CAMPAIGN,
        "template_campaign_id": US_EXISTING_CAMPAIGN_ID,
        "campaigns": len(COUNTRIES),
        "countries": [country["code"] for country in COUNTRIES],
        "status": "Local draft only; paused-only if approved for import",
        "bid_strategy": "Manual CPC",
        "max_cpc_maximum": max(country["max_cpc"] for country in COUNTRIES),
        "ad_groups_per_campaign": len(THEMES) * 2,
        "keywords_per_campaign": sum(
            len(theme["exact"]) + len(theme["phrase"]) for theme in THEMES
        ),
        "negative_keywords_per_campaign": len(NEGATIVES),
        "rsas_per_campaign": len(THEMES) * 2,
        "web_bulk_rows": len(web_rows),
        "blocked_live_spend": True,
        "blocked_ads_api_or_ui": True,
        "requires_owner_approval_before_import": True,
    }
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown_report(manifest)
    write_approval_gate()
    return manifest


def main() -> None:
    print(json.dumps(build_packet(), indent=2))


if __name__ == "__main__":
    main()
