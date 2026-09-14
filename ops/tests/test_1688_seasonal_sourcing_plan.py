#!/usr/bin/env python3
"""Offline regressions for the date-aware, frozen 1688 sourcing brief."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_dashboard.py"
CATEGORIES_PATH = REPO_ROOT / "ops" / "sourcing" / "sourcing-categories.json"
SEASONAL_RULES_PATH = REPO_ROOT / "ops" / "sourcing" / "seasonal-sourcing.json"
STUDIO_PATH = REPO_ROOT / "ops" / "sourcing" / "sourcing-studio.html"


def load_dashboard():
    spec = importlib.util.spec_from_file_location("sourcing_seasonal_plan_test", DASHBOARD_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {DASHBOARD_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    dashboard = load_dashboard()
    september = dt.date(2026, 9, 4)
    recommendation = dashboard.seasonal_recommendation(september)
    assert recommendation["as_of_date"] == "2026-09-04"
    assert recommendation["season_ids"] == ["fall", "winter", "holiday"]
    assert [item["phase"] for item in recommendation["entries"]] == ["sell_now", "source_ahead", "source_ahead"]
    assert any(item["season_id"] == "summer" for item in recommendation["excluded"])

    payload = {
        "category_ids": ["mommy-and-me", "family-matching"],
        "market_targets": ["us", "eu"],
        "plan_as_of": september.isoformat(),
        "sourcing_brief": {
            "season_mode": "recommended",
            "product_type_ids": ["dresses", "sets"],
            "occasion_ids": ["casual", "formal"],
            "excluded_query_ids": [],
            "max_queries_per_lane": 6,
        },
    }
    config = dashboard.normalize_scout_config(payload, as_of=september)
    first = dashboard.build_sourcing_plan(config, september)
    second = dashboard.build_sourcing_plan(config, september)
    assert first == second, "the same brief and date must produce an identical plan"
    assert first["plan_hash"] == second["plan_hash"]
    assert first["summary"]["lane_count"] == 2
    assert first["summary"]["query_count"] == 6
    assert all("夏季" not in row["chinese"] for row in first["queries"])
    forbidden_query_stuffing = ("2026", "新款", "现货", "一件代发", "实力商家", "欧美", "美国站", "欧洲站", "跨境", "外贸")
    assert all(not any(term in row["chinese"] for term in forbidden_query_stuffing) for row in first["queries"])
    assert all(row["query_term_count"] <= 4 for row in first["queries"])
    assert all(row["query_character_count"] <= 18 for row in first["queries"])
    assert len({row["chinese"] for row in first["queries"]}) == len(first["queries"]), "US/Europe must share one discovery search"
    assert all(row["market_target"] == "balanced" for row in first["queries"])
    assert all(row["market_targets"] == ["us", "eu"] for row in first["queries"])
    assert first["queries"][0]["english"] == "Mother-daughter matching outfits · Long-sleeve dresses · Fall"
    assert first["queries"][0]["chinese"] == "母女亲子装 长袖连衣裙 秋季"
    assert "秋季" in first["queries"][0]["chinese"]
    assert "长袖连衣裙" in first["queries"][0]["chinese"]
    assert first["queries"][0]["chinese"].startswith("母女亲子装 ")
    holiday = next(row for row in first["queries"] if row["season_id"] == "holiday")
    assert holiday["occasion_id"] == "formal"
    assert holiday["chinese"] == "母女亲子装 圣诞卫衣"
    assert not first["execution_allowed"]
    assert first["review"]["status"] == "owner_review_required"
    smart_payload = {**payload, "category_ids": ["daddy-and-me", "siblings-matching"]}
    smart_plan = dashboard.build_sourcing_plan(
        dashboard.normalize_scout_config(smart_payload, as_of=september),
        september,
    )
    daddy_dress = next(row for row in smart_plan["queries"] if row["category_id"] == "daddy-and-me" and row["product_type_id"] == "dresses")
    assert daddy_dress["chinese"] == "父子亲子装 长袖T恤 秋季"
    siblings_dress = next(row for row in smart_plan["queries"] if row["category_id"] == "siblings-matching" and row["product_type_id"] == "dresses")
    assert "姐妹装" in siblings_dress["chinese"]

    full_payload = {
        **payload,
        "category_ids": [
            "mommy-and-me",
            "daddy-and-me",
            "siblings-matching",
            "family-matching",
            "couples",
            "maternity",
        ],
    }
    full_plan = dashboard.build_sourcing_plan(
        dashboard.normalize_scout_config(full_payload, as_of=september),
        september,
    )
    assert full_plan["summary"]["lane_count"] == 5
    assert full_plan["summary"]["query_count"] == 15
    assert full_plan["summary"]["replacement_count"] == 12
    assert full_plan["summary"]["control_count"] == 3
    assert full_plan["summary"]["deferred_count"] == 3
    assert len(full_plan["queries"]) == 18
    expected_relationship_prefixes = {
        "mommy-and-me": ("母女亲子装",),
        "daddy-and-me": ("父女亲子装", "父子亲子装"),
        "siblings-matching": ("姐妹装", "兄弟装", "兄妹装"),
        "family-matching": ("全家亲子装",),
        "couples": ("情侣装", "情侣卫衣"),
        "maternity": ("孕妇亲子装",),
    }
    for row in (row for row in full_plan["queries"] if not row["deferred"]):
        assert row["chinese"].startswith(expected_relationship_prefixes[row["category_id"]])
    assert all("情侣装 套装" not in row["chinese"] for row in full_plan["queries"])
    assert full_plan["query_strategy"]["search_once_for_selected_markets"]
    expected_active_queries = [
        "母女亲子装 长袖连衣裙 秋季",
        "母女亲子装 卫衣 冬季",
        "母女亲子装 圣诞卫衣",
        "父子亲子装 长袖T恤 秋季",
        "父子亲子装 毛衣 冬季",
        "父子亲子装 圣诞毛衣",
        "姐妹装 连衣裙 秋季",
        "兄妹装 卫衣 冬季",
        "兄妹装 圣诞卫衣",
        "全家亲子装 卫衣 秋季",
        "全家亲子装 卫衣 冬季",
        "全家亲子装 圣诞睡衣",
        "情侣装 连衣裙 秋季",
        "情侣装 礼服 冬季",
        "情侣卫衣 圣诞",
    ]
    assert [row["chinese"] for row in full_plan["queries"] if row["included"]] == expected_active_queries
    assert [row["chinese"] for row in full_plan["queries"] if row["search_role"] == "control"] == [
        "姐妹装 连衣裙 秋季",
        "情侣装 连衣裙 秋季",
        "情侣装 礼服 冬季",
    ]
    assert [row["chinese"] for row in full_plan["queries"] if row["deferred"]] == [
        "孕妇亲子装 连衣裙 秋季",
        "孕妇亲子装 礼服 冬季",
        "孕妇亲子装 礼服 圣诞",
    ]
    assert not full_plan["execution_allowed"]

    manual_payload = {
        **payload,
        "sourcing_brief": {
            "season_mode": "manual",
            "season_ids": ["summer"],
            "product_type_ids": ["swimwear"],
            "occasion_ids": ["vacation"],
            "excluded_query_ids": [],
            "max_queries_per_lane": 6,
        },
    }
    manual_config = dashboard.normalize_scout_config(manual_payload, as_of=september)
    manual = dashboard.build_sourcing_plan(manual_config, september)
    assert manual["summary"]["seasons"] == ["Summer 2026"]
    assert all("夏季" in row["chinese"] and "泳装" in row["chinese"] and "度假" in row["chinese"] for row in manual["queries"])
    assert all("秋季" not in row["chinese"] for row in manual["queries"])
    assert all(row["query_term_count"] <= 4 and row["query_character_count"] <= 18 for row in manual["queries"])

    excluded_id = first["queries"][0]["id"]
    excluded_payload = json.loads(json.dumps(payload))
    excluded_payload["sourcing_brief"]["excluded_query_ids"] = [excluded_id]
    excluded_config = dashboard.normalize_scout_config(excluded_payload, as_of=september)
    excluded_plan = dashboard.build_sourcing_plan(excluded_config, september)
    excluded_row = next(row for row in excluded_plan["queries"] if row["id"] == excluded_id)
    assert not excluded_row["included"]
    assert excluded_plan["summary"]["query_count"] == 5

    with tempfile.TemporaryDirectory(prefix="dlm-seasonal-plan-") as temporary:
        root = Path(temporary)
        dashboard.REPO_ROOT = root
        dashboard.SOURCING_ROOT = root / "ops" / "sourcing"
        dashboard.CATEGORIES_PATH = CATEGORIES_PATH
        dashboard.SEASONAL_RULES_PATH = SEASONAL_RULES_PATH
        dashboard.SCOUT_STATE_PATH = dashboard.SOURCING_ROOT / "state" / "opportunity-scout.json"
        dashboard.SEARCH_HISTORY_PATH = dashboard.SOURCING_ROOT / "state" / "search-history.json"
        dashboard.launch_scout_worker = lambda _job_id: None
        try:
            dashboard.start_scout_job(payload)
        except ValueError as exc:
            assert "review-only" in str(exc)
        else:
            raise AssertionError("an unreviewed plan must not start")
        state_before_review = dashboard.load_scout_state()
        assert not state_before_review["jobs"], "review gating must not create a queued job"
        spoofed_payload = json.loads(json.dumps(payload))
        spoofed_payload["reviewed_plan_hash"] = first["plan_hash"]
        try:
            dashboard.start_scout_job(spoofed_payload)
        except ValueError as exc:
            assert "review-only" in str(exc)
        else:
            raise AssertionError("a caller-supplied hash must not bypass persisted review")
        assert not dashboard.load_scout_state()["jobs"]
        review = dashboard.confirm_scout_plan_review(payload)
        assert review["plan"]["execution_allowed"]
        assert review["schedule"]["reviewed_plan_hash"] == first["plan_hash"]
        assert not review["schedule"]["enabled"], "review acknowledgement must not enable automation"
        assert not dashboard.load_scout_state()["jobs"], "review acknowledgement must not start a job"
        job = dashboard.start_scout_job(review["schedule"])
        assert job["search_plan"]["plan_hash"] == first["plan_hash"]
        assert all(lane["exact_queries"] for lane in job["lanes"])
        frozen = [row["chinese"] for lane in job["lanes"] for row in lane["exact_queries"]]
        assert frozen == [row["chinese"] for row in first["queries"] if row["included"]]
        later = dashboard.build_sourcing_plan(
            dashboard.normalize_scout_config({**payload, "plan_as_of": "2026-11-04"}, as_of=dt.date(2026, 11, 4)),
            dt.date(2026, 11, 4),
        )
        assert later["plan_hash"] != job["search_plan"]["plan_hash"]
        reloaded = dashboard.scout_snapshot()["active_job"]
        assert reloaded["search_plan"]["plan_hash"] == first["plan_hash"]
        assert [row["chinese"] for lane in reloaded["lanes"] for row in lane["exact_queries"]] == frozen

        captured_commands: list[list[str]] = []

        class Completed:
            returncode = 0
            stdout = "reviewable=0 total=0 queries=1 browser_errors=0\n"
            stderr = ""

        dashboard.subprocess.run = lambda command, **_kwargs: captured_commands.append(command) or Completed()
        result = dashboard.scout_collection_once(
            "mommy-and-me",
            "us",
            query_index=0,
            max_queries=1,
            pages_per_query=1,
            exact_query=frozen[0],
        )
        assert result["status"] == "complete"
        assert captured_commands and "--exact-query" in captured_commands[0]
        exact_index = captured_commands[0].index("--exact-query")
        assert captured_commands[0][exact_index + 1] == frozen[0]

    studio = STUDIO_PATH.read_text(encoding="utf-8")
    for required in (
        "Build this season's search plan",
        "Recommended for today",
        "Product type",
        "Occasion",
        "Short Chinese searches",
        "No random rotation",
        "Run this reviewed search plan",
        "5+ verified years",
        "Current plan",
        "Review and choose exact searches",
        "Search first. Prove second.",
        "Review required before any run",
        "I reviewed these exact searches",
        "deferred rows cannot be enabled",
        "has not run",
    ):
        assert required in studio

    print("ok")


if __name__ == "__main__":
    main()
