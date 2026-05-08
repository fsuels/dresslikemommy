#!/usr/bin/env python3
"""Tests for the paused nonbrand Search rebuild packet."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/build_google_ads_nonbrand_paused_search_rebuild.py"

spec = importlib.util.spec_from_file_location("nonbrand_rebuild", SCRIPT_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(builder)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    manifest = builder.build_packet()
    output_dir = builder.OUTPUT_DIR
    bulk_path = output_dir / "web_bulk_upload/00_nonbrand_search_paused_rebuild_web_bulk.csv"
    rows = read_rows(bulk_path)

    assert manifest["campaign"] == builder.CAMPAIGN
    assert manifest["status"] == "Paused only"
    assert manifest["blocked_live_spend"] is True
    assert manifest["budget"] == "2.00"
    assert manifest["max_cpc"] == "0.15"

    campaign_rows = [row for row in rows if row["Row Type"] == "Campaign"]
    assert len(campaign_rows) == 1
    assert campaign_rows[0]["Campaign status"] == "Paused"
    assert campaign_rows[0]["Campaign type"] == "Search"
    assert campaign_rows[0]["Networks"] == "Google search"
    assert campaign_rows[0]["Budget"] == "2.00"
    assert campaign_rows[0]["Bid strategy type"] == "Manual CPC"
    assert campaign_rows[0]["Language"] == "en"
    assert campaign_rows[0]["Location"] == "United States"

    ad_group_rows = [row for row in rows if row["Row Type"] == "Ad group"]
    assert len(ad_group_rows) == len(builder.THEMES) * 2
    assert {row["Ad group status"] for row in ad_group_rows} == {"Paused"}
    assert {row["Default max. CPC"] for row in ad_group_rows} == {"0.15"}

    keyword_rows = [row for row in rows if row["Row Type"] == "Keyword"]
    assert len(keyword_rows) == manifest["keywords"]
    assert {row["Keyword status"] for row in keyword_rows} == {"Paused"}
    assert {row["Type"] for row in keyword_rows} == {"Exact match", "Phrase match"}
    assert "Broad match" not in {row["Type"] for row in keyword_rows}

    negative_rows = [row for row in rows if row["Row Type"] == "Negative keyword"]
    assert len(negative_rows) == manifest["campaign_negative_keywords"]
    assert {row["Level"] for row in negative_rows} == {"Campaign"}

    ad_rows = [row for row in rows if row["Row Type"] == "Ad"]
    assert len(ad_rows) == manifest["responsive_search_ads"]
    assert {row["Ad status"] for row in ad_rows} == {"Paused"}
    assert {row["Ad type"] for row in ad_rows} == {"Responsive search ad"}

    copy = " ".join(
        " ".join(row.get(f"Headline {i}", "") for i in range(1, 16))
        + " "
        + " ".join(row.get(f"Description {i}", "") for i in range(1, 5))
        for row in ad_rows
    ).lower()
    for forbidden in ("free shipping", "fast shipping", "free returns", "30-day"):
        assert forbidden not in copy

    assert all(len(row[f"Headline {i}"]) <= 30 for row in ad_rows for i in range(1, 16))
    assert all(len(row[f"Description {i}"]) <= 90 for row in ad_rows for i in range(1, 5))

    print("ok")


if __name__ == "__main__":
    main()
