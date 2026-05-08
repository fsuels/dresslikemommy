#!/usr/bin/env python3
"""Build a paused Google Ads nonbrand Search rebuild import packet."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = (
    ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-06-aggressive-controlled-growth-build/nonbrand_search_paused_rebuild"
)

CAMPAIGN = "DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506"
BUDGET = "2.00"
MAX_CPC = "0.15"

NEGATIVES = [
    ("free", "Broad"),
    ("diy", "Broad"),
    ("pattern", "Broad"),
    ("patterns", "Broad"),
    ("sewing", "Broad"),
    ("sew", "Broad"),
    ("how to sew", "Phrase"),
    ("sewing pattern", "Phrase"),
    ("crochet", "Broad"),
    ("knitting", "Broad"),
    ("template", "Broad"),
    ("wholesale", "Broad"),
    ("bulk", "Broad"),
    ("amazon", "Exact"),
    ("walmart", "Exact"),
    ("target", "Exact"),
    ("shein", "Exact"),
    ("temu", "Exact"),
    ("used", "Broad"),
    ("secondhand", "Broad"),
    ("second hand", "Phrase"),
    ("costume", "Broad"),
    ("rental", "Broad"),
    ("pdf", "Broad"),
    ("clipart", "Broad"),
    ("coloring page", "Phrase"),
    ("doll", "Broad"),
    ("roblox", "Exact"),
    ("sims", "Exact"),
    ("maternity", "Broad"),
    ("sexy", "Broad"),
    ("adult costume", "Phrase"),
    ("aliexpress", "Exact"),
    ("alibaba", "Exact"),
    ("1688", "Exact"),
    ("fabric", "Broad"),
    ("tutorial", "Broad"),
]

THEMES = [
    {
        "theme": "Mommy & Me Dresses",
        "path_1": "mommy-me",
        "path_2": "dresses",
        "url": "https://www.dresslikemommy.com/collections/mother-daughter-matching-dresses",
        "exact": [
            "mommy and me dresses",
            "mother daughter dresses",
            "mom and daughter matching outfits",
        ],
        "phrase": [
            "mommy and me dresses",
            "mother daughter matching dresses",
            "mommy and me outfits",
        ],
        "headlines": [
            "Mommy & Me Dresses",
            "Mother Daughter Dresses",
            "Mom Daughter Outfits",
            "Matching Dresses",
            "Sweet Twinning Looks",
            "Photo Ready Dresses",
            "Vacation Dress Looks",
            "Birthday Dress Ideas",
            "Shop Dress Like Mommy",
            "Mommy And Me Outfits",
            "Coordinated Dresses",
            "Cute Matching Styles",
            "Dresses For Mom & Girl",
            "Family Photo Dresses",
            "Dress Like Mommy",
        ],
        "descriptions": [
            "Shop mother daughter matching dresses for photos, birthdays and vacations.",
            "Choose a size for each person and build a coordinated mommy and me look.",
            "Browse sweet dress styles for mom and girl from Dress Like Mommy.",
            "Find picture-ready matching dresses for special days and everyday moments.",
        ],
    },
    {
        "theme": "Family Matching",
        "path_1": "family",
        "path_2": "matching",
        "url": "https://www.dresslikemommy.com/collections/matching-outfits",
        "exact": [
            "family matching outfits",
            "matching family outfits",
            "family photo outfits",
        ],
        "phrase": [
            "family matching outfits",
            "matching family clothes",
            "coordinated family outfits",
        ],
        "headlines": [
            "Family Matching Outfits",
            "Matching Family Outfits",
            "Family Photo Outfits",
            "Coordinated Family Sets",
            "Matching Looks For All",
            "Mom Dad Kids Outfits",
            "Picture Ready Looks",
            "Shop Family Matching",
            "Dress Like Mommy",
            "Cute Family Outfits",
            "Matching Clothes",
            "Family Outfit Ideas",
            "Easy Coordinated Looks",
            "Outfits For Photos",
            "Family Matching Styles",
        ],
        "descriptions": [
            "Shop matching outfits for moms, dads, kids and family photo moments.",
            "Create a coordinated family look with separate sizes for each person.",
            "Browse family matching styles for vacations, birthdays and portraits.",
            "Make group photos feel pulled together with easy matching outfit ideas.",
        ],
    },
    {
        "theme": "Vacation Family",
        "path_1": "vacation",
        "path_2": "family",
        "url": "https://www.dresslikemommy.com/collections/matching-family-vacation-outfits",
        "exact": [
            "matching family vacation outfits",
            "family vacation outfits",
            "beach family outfits",
        ],
        "phrase": [
            "matching family vacation outfits",
            "beach family outfits",
            "resort family outfits",
        ],
        "headlines": [
            "Vacation Family Outfits",
            "Matching Vacation Sets",
            "Beach Family Outfits",
            "Resort Family Looks",
            "Family Trip Outfits",
            "Tropical Family Styles",
            "Vacation Photo Looks",
            "Matching Beach Looks",
            "Dress Like Mommy",
            "Family Vacation Looks",
            "Pack Matching Outfits",
            "Family Resort Outfits",
            "Coordinated Trip Looks",
            "Outfits For Vacation",
            "Beach Photo Outfits",
        ],
        "descriptions": [
            "Shop coordinated family vacation outfits for beach trips and resort photos.",
            "Build a matching look for mom, dad, kids and baby before the trip.",
            "Browse vacation-ready family outfits with tropical and photo-friendly styles.",
            "Plan picture-ready matching outfits for beach days, dinners and portraits.",
        ],
    },
    {
        "theme": "Matching Pajamas",
        "path_1": "family",
        "path_2": "pajamas",
        "url": "https://www.dresslikemommy.com/collections/family-pajamas",
        "exact": [
            "matching family pajamas",
            "mommy and me pajamas",
            "family pajama sets",
        ],
        "phrase": [
            "matching family pajamas",
            "mommy and me pajamas",
            "mother daughter pajamas",
        ],
        "headlines": [
            "Matching Family Pajamas",
            "Mommy & Me Pajamas",
            "Family Pajama Sets",
            "Mother Daughter Pajamas",
            "Cozy Matching Pajamas",
            "Family Sleepwear",
            "Pajamas For Photos",
            "Shop Matching Pajamas",
            "Dress Like Mommy",
            "Cute Pajama Sets",
            "Mom And Kids Pajamas",
            "Coordinated Pajamas",
            "Holiday Pajama Looks",
            "Family Morning Looks",
            "Matching Sleepwear",
        ],
        "descriptions": [
            "Shop matching family pajamas for cozy mornings, holidays and photos.",
            "Choose separate sizes for mom, kids and family members in one place.",
            "Browse mommy and me pajamas and coordinated family sleepwear styles.",
            "Find comfy matching pajama ideas for snapshots, weekends and holidays.",
        ],
    },
    {
        "theme": "Matching Swimwear",
        "path_1": "family",
        "path_2": "swimwear",
        "url": "https://www.dresslikemommy.com/collections/family-swimsuits",
        "exact": [
            "matching family swimsuits",
            "mommy and me swimsuits",
            "family swimwear",
        ],
        "phrase": [
            "matching family swimsuits",
            "mommy and me swimsuits",
            "matching swimsuits family",
        ],
        "headlines": [
            "Matching Family Swimwear",
            "Mommy & Me Swimsuits",
            "Family Swimsuits",
            "Matching Beach Swim",
            "Pool Day Family Looks",
            "Beach Family Swimwear",
            "Swim Looks For Photos",
            "Shop Matching Swim",
            "Dress Like Mommy",
            "Mother Daughter Swim",
            "Family Beach Looks",
            "Coordinated Swimwear",
            "Vacation Swim Styles",
            "Matching Pool Outfits",
            "Cute Family Swimwear",
        ],
        "descriptions": [
            "Shop matching family swimwear for beach days, pool trips and vacations.",
            "Browse mommy and me swimsuits and coordinated swim looks for family photos.",
            "Choose swim sizes for each family member and build a matching beach look.",
            "Find picture-ready family swimsuits for sunny trips and pool moments.",
        ],
    },
    {
        "theme": "Daddy & Me",
        "path_1": "daddy-me",
        "path_2": "outfits",
        "url": "https://www.dresslikemommy.com/collections/daddy-and-me",
        "exact": [
            "daddy and me outfits",
            "father son matching outfits",
            "dad and son matching outfits",
        ],
        "phrase": [
            "daddy and me outfits",
            "father son matching shirts",
            "dad and son matching outfits",
        ],
        "headlines": [
            "Daddy & Me Outfits",
            "Father Son Matching",
            "Dad And Son Outfits",
            "Daddy And Me Shirts",
            "Matching Dad Kid Looks",
            "Father Child Outfits",
            "Family Photo Looks",
            "Shop Daddy & Me",
            "Dress Like Mommy",
            "Dad Matching Outfits",
            "Cute Dad Kid Looks",
            "Matching Shirts",
            "Daddy Me Styles",
            "Father Son Shirts",
            "Dad And Kid Outfits",
        ],
        "descriptions": [
            "Shop daddy and me outfits for father-child photos, trips and special days.",
            "Browse matching dad and kid styles that coordinate with family outfits.",
            "Choose sizes for dad and child to build an easy matching look.",
            "Find father-son shirts and daddy and me outfit ideas from Dress Like Mommy.",
        ],
    },
]


WEB_FIELDS = [
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
    "Ad group status",
    "Ad group ID",
    "Ad group",
    "Ad group type",
    "Ad rotation",
    "Default max. CPC",
    "CPC%",
    "Max. CPM",
    "Max. CPV",
    "Target CPM",
    "TrueView target CPV",
    "Keyword status",
    "Keyword ID",
    "Keyword",
    "Type",
    "Final URL",
    "Mobile final URL",
    "Level",
    "Negative keyword",
    "Ad status",
    "Ad ID",
    "Ad type",
]
for idx in range(1, 16):
    WEB_FIELDS.append(f"Headline {idx}")
for idx in range(1, 5):
    WEB_FIELDS.append(f"Description {idx}")
for idx in range(1, 16):
    WEB_FIELDS.append(f"Headline {idx} position")
for idx in range(1, 5):
    WEB_FIELDS.append(f"Description {idx} position")
WEB_FIELDS.extend(["Path 1", "Path 2"])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ad_group_name(theme: str, match: str) -> str:
    return f"{theme} - {match}"


def match_label(match: str) -> str:
    return "Exact match" if match == "Exact" else "Phrase match"


def validate() -> None:
    seen_ad_groups: set[str] = set()
    for theme in THEMES:
        assert len(theme["headlines"]) == 15
        assert len(theme["descriptions"]) == 4
        for headline in theme["headlines"]:
            if len(headline) > 30:
                raise ValueError(f"headline too long ({len(headline)}): {headline}")
        for description in theme["descriptions"]:
            if len(description) > 90:
                raise ValueError(
                    f"description too long ({len(description)}): {description}"
                )
        copy = " ".join(theme["headlines"] + theme["descriptions"]).lower()
        for forbidden in ("free shipping", "fast shipping", "free returns", "30-day"):
            if forbidden in copy:
                raise ValueError(f"unsupported claim in ad copy: {forbidden}")
        for match in ("Exact", "Phrase"):
            name = ad_group_name(theme["theme"], match)
            if name in seen_ad_groups:
                raise ValueError(f"duplicate ad group: {name}")
            seen_ad_groups.add(name)


def build_web_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = [
        {
            "Row Type": "Campaign",
            "Action": "Add",
            "Campaign status": "Paused",
            "Campaign": CAMPAIGN,
            "Campaign type": "Search",
            "Networks": "Google search",
            "Budget": BUDGET,
            "Delivery method": "Standard",
            "Budget type": "Daily",
            "Bid strategy type": "Manual CPC",
            "Language": "en",
            "Location": "United States",
            "EU political ads": "No",
        }
    ]

    for theme in THEMES:
        for match in ("Exact", "Phrase"):
            rows.append(
                {
                    "Row Type": "Ad group",
                    "Action": "Add",
                    "Campaign": CAMPAIGN,
                    "Ad group status": "Paused",
                    "Ad group": ad_group_name(theme["theme"], match),
                    "Ad group type": "Standard",
                    "Ad rotation": "Optimize",
                    "Default max. CPC": MAX_CPC,
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
                        "Campaign": CAMPAIGN,
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
                "Campaign": CAMPAIGN,
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
                "Campaign": CAMPAIGN,
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


def build_packet() -> dict[str, object]:
    validate()

    import_dir = OUTPUT_DIR / "web_bulk_upload"
    qa_dir = OUTPUT_DIR / "manual_qa"

    web_rows = build_web_rows()
    write_csv(import_dir / "00_nonbrand_search_paused_rebuild_web_bulk.csv", web_rows, WEB_FIELDS)

    ad_groups = [
        {
            "Campaign": CAMPAIGN,
            "Ad group": ad_group_name(theme["theme"], match),
            "Status": "Paused",
            "Default max. CPC": MAX_CPC,
            "Landing page": theme["url"],
        }
        for theme in THEMES
        for match in ("Exact", "Phrase")
    ]
    write_csv(
        OUTPUT_DIR / "01_ad_group_map.csv",
        ad_groups,
        ["Campaign", "Ad group", "Status", "Default max. CPC", "Landing page"],
    )

    qa_rows = [
        {
            "Check": "Campaign status",
            "Required result": "Paused",
            "Why": "No nonbrand live spend in this approval.",
        },
        {
            "Check": "Campaign type and networks",
            "Required result": "Search, Google Search only",
            "Why": "No Display/Search Partner expansion.",
        },
        {
            "Check": "Bidding",
            "Required result": f"Manual CPC with bids at or below ${MAX_CPC}",
            "Why": "Low-CPC control for the owner's margin model.",
        },
        {
            "Check": "Locations",
            "Required result": "United States, presence-only if the UI asks",
            "Why": "No international live spend in this approval.",
        },
        {
            "Check": "Keywords",
            "Required result": "Exact and phrase only; no broad keywords",
            "Why": "Tight cold-search control.",
        },
        {
            "Check": "Conversion goals",
            "Required result": "No edits; inherit account-default Purchases",
            "Why": "Conversion-goal changes were explicitly blocked.",
        },
    ]
    write_csv(qa_dir / "nonbrand_rebuild_post_import_qa.csv", qa_rows, ["Check", "Required result", "Why"])

    manifest = {
        "campaign": CAMPAIGN,
        "output_dir": str(OUTPUT_DIR.relative_to(ROOT)),
        "bulk_upload_file": str(
            (import_dir / "00_nonbrand_search_paused_rebuild_web_bulk.csv").relative_to(ROOT)
        ),
        "status": "Paused only",
        "budget": BUDGET,
        "max_cpc": MAX_CPC,
        "bid_strategy": "Manual CPC",
        "themes": [theme["theme"] for theme in THEMES],
        "ad_groups": len(THEMES) * 2,
        "keywords": sum(len(theme["exact"]) + len(theme["phrase"]) for theme in THEMES),
        "campaign_negative_keywords": len(NEGATIVES),
        "responsive_search_ads": len(THEMES) * 2,
        "blocked_live_spend": True,
    }
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    readme = "\n".join(
        [
            "# Nonbrand Search Paused Rebuild",
            "",
            f"Campaign: `{CAMPAIGN}`",
            "",
            "This packet is built for the 2026-05-06 aggressive controlled growth approval.",
            "It is paused-only, US-English, exact/phrase-only, and uses Manual CPC control.",
            "",
            "Live-spend launch is intentionally blocked. Before any future enablement, read back campaign status, networks, locations, bid caps, conversion goals, negatives, ad strength, and all policy statuses.",
            "",
        ]
    )
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    return manifest


def main() -> None:
    print(json.dumps(build_packet(), indent=2))


if __name__ == "__main__":
    main()
