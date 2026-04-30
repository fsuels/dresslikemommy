#!/usr/bin/env python3
"""Tests for the paused-only Google Ads Brand Search Editor packet."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/build_google_ads_brand_paused_editor_import.py"

spec = importlib.util.spec_from_file_location("brand_import_builder", SCRIPT_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(builder)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> None:
    manifest = builder.build_packet()
    output_dir = builder.OUTPUT_DIR
    auto_dir = output_dir / "auto_import_safe_paused_core"

    assert manifest["campaign"] == builder.CAMPAIGN
    assert manifest["all_imported_statuses"] == "Paused"
    assert manifest["live_launch_allowed"] is False

    campaign_rows = read_rows(auto_dir / "01_campaign_settings.csv")
    assert len(campaign_rows) == 1
    assert campaign_rows[0]["Campaign status"] == "Paused"
    assert campaign_rows[0]["Campaign daily budget"] == "10.00"
    assert campaign_rows[0]["Bid strategy type"] == "Maximize conversion value"
    assert campaign_rows[0]["Networks"] == "Google Search"

    ad_group_rows = read_rows(auto_dir / "03_ad_groups.csv")
    assert {row["Ad group status"] for row in ad_group_rows} == {"Paused"}
    assert {row["Ad group"] for row in ad_group_rows} == {"Brand - Exact", "Brand - Phrase"}

    keyword_rows = read_rows(auto_dir / "04_keywords.csv")
    assert len(keyword_rows) == len(builder.EXACT_KEYWORDS) + len(builder.PHRASE_KEYWORDS)
    assert {row["Status"] for row in keyword_rows} == {"Paused"}
    assert {row["Match type"] for row in keyword_rows} == {"Exact", "Phrase"}

    negative_rows = read_rows(auto_dir / "05_campaign_negative_keywords_reference.csv")
    negative_paste_rows = read_tsv_rows(
        auto_dir / "05_campaign_negative_keywords_editor_bulk_paste.tsv"
    )
    source_rows = [
        line.strip()
        for line in builder.NEGATIVE_SOURCE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert manifest["negative_source_rows"] == len(source_rows)
    assert manifest["duplicate_rows_removed"] == 2
    assert manifest["redundant_exact_rows_removed"] == 1
    assert len(negative_rows) == 253
    assert len(negative_paste_rows) == len(negative_rows)
    assert {row["Campaign"] for row in negative_rows} == {builder.CAMPAIGN}
    assert {row["Type"] for row in negative_rows} == {"Campaign negative"}
    assert set(negative_paste_rows[0].keys()) == {"Keyword", "Type"}
    assert len({(row["Keyword"].lower(), row["Match type"]) for row in negative_rows}) == len(
        negative_rows
    )
    phrase_keywords = {
        row["Keyword"].lower() for row in negative_rows if row["Match type"] == "Phrase"
    }
    redundant_exact = [
        row
        for row in negative_rows
        if row["Match type"] == "Exact" and row["Keyword"].lower() in phrase_keywords
    ]
    assert redundant_exact == []

    web_dir = output_dir / "web_bulk_preview_templates"
    combined_rows = read_rows(web_dir / "00_brand_search_paused_combined_web_bulk.csv")
    assert len(combined_rows) == 1 + 2 + len(keyword_rows) + len(negative_rows) + 2
    row_types = {row["Row Type"] for row in combined_rows}
    assert row_types == {"Campaign", "Ad group", "Keyword", "Negative keyword", "Ad"}
    assert {row["Campaign"] for row in combined_rows} == {builder.CAMPAIGN}
    assert {row["Action"] for row in combined_rows} == {"Add"}
    assert {row["Campaign status"] for row in combined_rows if row["Row Type"] == "Campaign"} == {
        "Paused"
    }
    assert {row["Ad group status"] for row in combined_rows if row["Row Type"] == "Ad group"} == {
        "Paused"
    }
    assert {row["Keyword status"] for row in combined_rows if row["Row Type"] == "Keyword"} == {
        "Paused"
    }
    assert {row["Ad status"] for row in combined_rows if row["Row Type"] == "Ad"} == {"Paused"}

    ad_rows = read_rows(auto_dir / "06_responsive_search_ads.csv")
    assert len(ad_rows) == 2
    assert {row["Status"] for row in ad_rows} == {"Paused"}
    assert {row["Headline 1"] for row in ad_rows} == {"Dress Like Mommy Official"}
    assert {row["Headline 1 position"] for row in ad_rows} == {"1"}
    joined_copy = " ".join(
        " ".join(row.get(f"Headline {i}", "") for i in range(1, 16))
        + " "
        + " ".join(row.get(f"Description {i}", "") for i in range(1, 5))
        for row in ad_rows
    ).lower()
    for forbidden in ("free shipping", "free return", "free returns", "30-day return"):
        assert forbidden not in joined_copy

    print("ok")


if __name__ == "__main__":
    main()
