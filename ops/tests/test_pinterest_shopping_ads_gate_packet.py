#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/build_pinterest_shopping_ads_gate_packet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_pinterest_shopping_ads_gate_packet", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_pinterest_gate_packet_fails_closed_and_scopes_groups():
    module = load_module()
    summary = module.build()
    readback_exists = module.PINTEREST_ITEM_READBACK.exists()
    expected_item_gate = (
        "PASS_EXACT_EN_US_IN_STOCK_READBACK"
        if readback_exists
        else "BLOCKED_UNTIL_EXACT_PINTEREST_CATALOG_READBACK"
    )

    assert summary["decision"] == "DO_NOT_CREATE_PINTEREST_ADS_OR_PRODUCT_GROUPS_YET"
    assert summary["campaign_creation_allowed"] is False
    assert set(summary["candidate_family_counts"]) == {"mommy_me", "family_matching", "pajamas"}
    assert summary["candidate_family_counts"] == {
        "family_matching": 103,
        "mommy_me": 214,
        "pajamas": 29,
    }

    manifest = read_csv(ROOT / summary["files"]["product_group_manifest"])
    assert [row["user_facing_group"] for row in manifest] == ["Mommy & Me", "Family Matching", "Pajamas"]
    assert {row["target_country"] for row in manifest} == {"US_ONLY"}
    assert {row["campaign_status"] for row in manifest} == {"DO_NOT_CREATE_OR_LAUNCH_YET"}
    assert {row["pinterest_item_level_gate"] for row in manifest} == {expected_item_gate}
    if readback_exists:
        assert summary["pinterest_item_readback_summary"]["status_counts"] == {"FOUND_EN_US_IN_STOCK": 346}
        assert {row["pinterest_item_readback_fail_rows"] for row in manifest} == {"0"}


def test_pinterest_candidate_rows_all_pass_clean_local_gate():
    module = load_module()
    summary = module.build()
    candidates = read_csv(ROOT / summary["files"]["candidate_offer_rows"])
    readback_exists = module.PINTEREST_ITEM_READBACK.exists()
    expected_item_status = "FOUND_EN_US_IN_STOCK" if readback_exists else "NEEDS_PINTEREST_EXPORT_OR_UI_READBACK"

    assert len(candidates) == 346
    for row in candidates:
        assert row["market"] == "US"
        assert row["cost"]
        assert row["custom_label_0"] == "paid_eligible"
        assert row["custom_label_4"] == "us_test_ready"
        assert row["merchant_center_status"] == "Approved"
        assert row["merchant_center_destination"] == "Shopping ads eligible"
        assert row["pdp_status"] == "PASS"
        assert row["availability_status"] == "PASS"
        assert row["pinterest_item_level_status"] == expected_item_status
        if readback_exists:
            assert row["pinterest_en_us_pin_id"]
            assert row["pinterest_en_us_feed_profile_id"]
            assert row["pinterest_en_us_locale"] == "en-US"
            assert row["pinterest_en_us_availability"] == "IN_STOCK"
        assert row["review_only_launch_status"] == "CANDIDATE_ONLY_NOT_LAUNCH_APPROVED"


if __name__ == "__main__":
    test_pinterest_gate_packet_fails_closed_and_scopes_groups()
    test_pinterest_candidate_rows_all_pass_clean_local_gate()
