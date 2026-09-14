#!/usr/bin/env python3
"""Offline regressions for the persistent multi-lane Opportunity Scout."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_dashboard.py"
DETAIL_ENRICH_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_detail_enrich.py"
CATEGORIES_PATH = REPO_ROOT / "ops" / "sourcing" / "sourcing-categories.json"


def load_dashboard():
    spec = importlib.util.spec_from_file_location("sourcing_opportunity_scout_test", DASHBOARD_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {DASHBOARD_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_detail_enricher():
    spec = importlib.util.spec_from_file_location("sourcing_detail_enrich_test", DETAIL_ENRICH_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {DETAIL_ENRICH_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verified_fixture(years: str) -> dict[str, object]:
    return {
        "key": "900000000001",
        "title": "2026 family matching resort set",
        "display_title": "2026 family matching resort set",
        "category_id": "family-matching",
        "observed_at": "2026-09-02T12:00:00+00:00",
        "review_stage": "detail",
        "verdict": "Test",
        "decision": "",
        "vendor_name": "Established supplier",
        "rating": "4.8",
        "years_on_1688": years,
        "years_on_1688_scope": "supplier_context_phrase",
        "years_on_1688_label": f"{years}年诚信通" if years else "",
        "dropship_supported": "yes",
        "availability": "in stock",
        "service_flags": "ready stock | dispatch 48 hours",
        "size_chart": "adult and child size chart",
        "vendor_image_urls": "local-image-1 | local-image-2",
        "evidence": {
            "detail_evidence_path": "ops/sourcing/detail-enrichment/900000000001/detail-evidence.json",
            "detail_verdict": "Test",
            "dropship_confirmed": "yes",
            "dispatch_confirmed": "48 hours",
            "supplier_confirmed": "Established supplier | 4.8 rating",
            "size_chart_source": "detail page",
            "vendor_images_path": "ops/sourcing/image-cache/900000000001",
        },
        "score": 82,
        "category_match": "5",
        "moq": "1",
        "ip_risk_flags": "",
        "concerns": [],
    }


def main() -> None:
    dashboard = load_dashboard()
    detail_enricher = load_detail_enricher()
    assert not dashboard.exact_relationship_fit(
        {"title": "2026 Response formal dress", "display_title": "", "category_id": "daddy-and-me"}
    ), "son inside Response must not satisfy Daddy & Me"
    assert not dashboard.exact_relationship_fit(
        {"title": "2026 women formal dress", "display_title": "", "category_id": "couples"}
    ), "men inside women must not satisfy Couples"
    assert not dashboard.exact_relationship_fit(
        {"title": "2026 couples lingerie matching set", "display_title": "", "category_id": "couples"}
    ), "obvious lingerie must fail even when a relationship word is present"
    assert dashboard.exact_relationship_fit(
        {"title": "2026 father-son matching suits", "display_title": "", "category_id": "daddy-and-me"}
    )
    assert not dashboard.exact_relationship_fit(
        {"title": "2026 maternity formal dress", "display_title": "", "category_id": "maternity"}
    ), "Maternity must also prove a matching-family relationship"
    assert dashboard.exact_relationship_fit(
        {"title": "2026 maternity mother-daughter matching dresses", "display_title": "", "category_id": "maternity"}
    )
    assert detail_enricher.validated_supplier_tenure(
        {
            "years_on_1688": "5",
            "years_on_1688_scope": "supplier_context_phrase",
            "years_on_1688_label": "适合5年儿童的兄妹同款套装",
        }
    ) == ("", "", ""), "a product-age phrase must never become supplier tenure"
    assert detail_enricher.validated_supplier_tenure(
        {
            "years_on_1688": "1",
            "years_on_1688_scope": "supplier_context_phrase",
            "years_on_1688_label": "1年诚信通",
        }
    ) == ("1", "1年诚信通", "supplier_context_phrase")
    assert detail_enricher.validated_supplier_tenure(
        {
            "years_on_1688": "5",
            "years_on_1688_scope": "supplier_context_phrase",
            "years_on_1688_label": "经营年限：5年",
        }
    ) == ("5", "经营年限：5年", "supplier_context_phrase")
    parser_base = {
        "title": "2025 Autumn Couple Outfits Matching Dress Set One Piece Dropshipping",
        "vendor_name": "",
        "moq": "1",
        "raw_card_text": "2025 Autumn Couple Outfits Matching Dress Set MOQ 1",
        "ip_risk_flags": "",
    }
    parser_detail = {
        "page_title": "2025 Autumn Couple Outfits Matching Dress Set - 阿里巴巴",
        "title": "广州市宜馨雅贸易有限公司",
        "vendor_name": "广州市宜馨雅贸易有限公司",
        "moq": "60",
        "raw_detail_text": "商品 1件起批 60天老客价 平台说明不保证相同品牌",
        "ip_risk_flags": "品牌",
        "image_urls": [],
    }
    parsed = detail_enricher.enriched_row(
        parser_base,
        parser_detail,
        Path("ops/sourcing/vendor-images/test"),
        Path("ops/sourcing/detail-enrichment/test/detail-evidence.json"),
    )
    assert parsed["title"] == "2025 Autumn Couple Outfits Matching Dress Set"
    assert parsed["moq"] == "1", "60-day loyalty pricing must not become MOQ 60"
    assert parsed["raw_card_text"] == parser_base["raw_card_text"]
    assert parsed["ip_risk_flags"] == "", "generic platform legal copy must not become a brand-risk flag"
    assert detail_enricher.dispatch_evidence_label("代发") == "", "dropshipping alone must not prove dispatch speed"
    assert detail_enricher.dispatch_evidence_label("代发 | 48小时发货") == "代发 | 48小时发货"
    with tempfile.TemporaryDirectory(prefix="dlm-opportunity-scout-") as temporary:
        root = Path(temporary)
        dashboard.REPO_ROOT = root
        dashboard.SOURCING_ROOT = root / "ops" / "sourcing"
        dashboard.CATEGORIES_PATH = CATEGORIES_PATH
        dashboard.SCOUT_STATE_PATH = dashboard.SOURCING_ROOT / "state" / "opportunity-scout.json"
        dashboard.SEARCH_HISTORY_PATH = dashboard.SOURCING_ROOT / "state" / "search-history.json"
        dashboard.launch_scout_worker = lambda _job_id: None

        catalog = dashboard.search_term_catalog()
        assert "siblings-matching" in catalog
        assert len(catalog["siblings-matching"]) >= 30
        first_term = catalog["siblings-matching"][0]
        assert first_term["english"]
        assert first_term["chinese"]
        assert first_term["id"] == 0

        config = dashboard.normalize_scout_config(
            {
                "category_ids": ["mommy-and-me", "siblings-matching"],
                "market_targets": ["us", "eu"],
                "query_selections": {"mommy-and-me": [2, 4], "siblings-matching": [1]},
            }
        )
        lanes = dashboard.scout_lane_plan(config)
        assert [lane["id"] for lane in lanes] == [
            "mommy-and-me:us",
            "mommy-and-me:eu",
            "siblings-matching:us",
            "siblings-matching:eu",
        ]
        assert lanes[0]["query_indexes"] == [2, 4]
        assert lanes[0]["queries_planned"] == 2
        assert lanes[2]["query_indexes"] == [1]

        schedule = dashboard.save_scout_schedule(config)
        assert schedule["query_selections"]["mommy-and-me"] == [2, 4]
        assert schedule["minimum_supplier_years"] == 5
        assert not schedule["enabled"]
        assert not schedule["plan_preview"]["execution_allowed"]
        persisted = json.loads(dashboard.SCOUT_STATE_PATH.read_text(encoding="utf-8"))
        assert persisted["schedule"]["query_selections"]["siblings-matching"] == [1]

        reviewed = dashboard.confirm_scout_plan_review(config)
        assert reviewed["plan"]["execution_allowed"]
        assert not reviewed["schedule"]["enabled"]
        assert not json.loads(dashboard.SCOUT_STATE_PATH.read_text(encoding="utf-8"))["jobs"]
        job = dashboard.start_scout_job(reviewed["schedule"])
        assert job["status"] == "queued"
        assert [lane["id"] for lane in job["lanes"]] == ["mommy-and-me:shared", "siblings-matching:shared"]
        assert all(lane["market_target"] == "balanced" for lane in job["lanes"])
        assert all(lane["market_targets"] == ["us", "eu"] for lane in job["lanes"])
        assert job["lanes"][0]["query_indexes"] == []
        assert len(job["lanes"][0]["exact_queries"]) >= 1
        assert job["search_plan"]["plan_hash"]
        reloaded = dashboard.scout_snapshot()
        assert reloaded["active_job"]["id"] == job["id"]
        assert reloaded["active_job"]["config"]["query_selections"]["mommy-and-me"] == [2, 4]
        frozen_queries = [row["chinese"] for row in reloaded["active_job"]["lanes"][0]["exact_queries"]]

        collection_calls: list[tuple[str, str, str]] = []
        dashboard.chrome_browser_status = lambda: {"ok": True, "running": True, "message": "ready"}
        dashboard.scout_collection_once = lambda category_id, market_target, **kwargs: (
            collection_calls.append((category_id, market_target, str(kwargs.get("exact_query") or "")))
            or {
                "status": "complete",
                "message": "fixture search complete",
                "run_dirs": [f"ops/sourcing/fixture-{category_id}-{market_target}"],
                "summary": {"queries": 1},
            }
        )
        dashboard.candidates_for_run_dirs = lambda _run_dirs, _limit: ["900000000001"]
        dashboard.scout_detail_once = lambda _key: {
            "status": "complete",
            "tier": "verified",
            "message": "fixture verified",
            "supplier_years": 5,
            "evidence_confidence": 100,
        }
        dashboard.run_scout_job(job["id"])
        completed = dashboard.scout_snapshot()["active_job"]
        assert completed["status"] == "complete"
        assert all(lane["status"] == "complete" for lane in completed["lanes"])
        assert completed["verified_keys"] == ["900000000001"]
        assert all(call[2] for call in collection_calls)
        assert {call[:2] for call in collection_calls} == {
            ("mommy-and-me", "balanced"),
            ("siblings-matching", "balanced"),
        }

        waiting_payload = {
            "category_ids": ["siblings-matching"],
            "market_targets": ["us"],
            "query_selections": {"siblings-matching": [3]},
            "enabled": False,
        }
        waiting_review = dashboard.confirm_scout_plan_review(waiting_payload)
        waiting_job = dashboard.start_scout_job(waiting_review["schedule"])
        dashboard.chrome_browser_status = lambda: {"ok": False, "running": True, "message": "login required"}
        dashboard.run_scout_job(waiting_job["id"])
        waiting = dashboard.scout_snapshot()["active_job"]
        assert waiting["status"] == "waiting_for_user"
        assert waiting["cursor"]["lane_index"] == 0
        waiting_queries = [row["chinese"] for row in waiting["lanes"][0]["exact_queries"]]
        dashboard.chrome_browser_status = lambda: {"ok": True, "running": True, "message": "ready"}
        dashboard.run_scout_job(waiting_job["id"])
        resumed = dashboard.scout_snapshot()["active_job"]
        assert resumed["status"] == "complete"
        assert [row["chinese"] for row in resumed["lanes"][0]["exact_queries"]] == waiting_queries
        assert frozen_queries, "the exact term batch must be stored before execution"

        young = dashboard.opportunity_assessment(verified_fixture("1"))
        assert young["tier"] == "rejected"
        assert "minimum is 5" in young["reason"]
        four_year = dashboard.opportunity_assessment(verified_fixture("4"))
        assert four_year["tier"] == "rejected"
        assert "only 4 verified years; minimum is 5" in four_year["reason"]
        established = dashboard.opportunity_assessment(verified_fixture("5"))
        assert established["tier"] == "verified"
        assert established["supplier_years"] == 5

        pending = verified_fixture("")
        pending["review_stage"] = "search"
        pending["evidence"] = {}
        pending["verdict"] = "Test"
        assert dashboard.opportunity_assessment(pending)["tier"] == "promising"
        search_age_claim = verified_fixture("5")
        search_age_claim["review_stage"] = "search"
        search_age_claim["evidence"] = {}
        search_age_claim["verdict"] = "Test"
        search_age_assessment = dashboard.opportunity_assessment(search_age_claim)
        assert search_age_assessment["tier"] == "promising"
        assert not search_age_assessment["confirmed"]["supplier_age"]
        assert search_age_assessment["supplier_years_label"] == "Not verified"
        assert dashboard.valid_supplier_rating({"rating": "50"}) is None
        assert not dashboard.explicit_yes("not supported")
        assert not dashboard.explicit_yes("unsupported")
        assert not dashboard.explicit_yes("不支持")

        dashboard.write_json(
            dashboard.SEARCH_HISTORY_PATH,
            {"version": 1, "updated_at": "", "categories": {"mommy-and-me": {"next_query_index": 7}}},
        )
        dashboard.cdp_pages = lambda: [{"id": "tab-1", "type": "page", "url": "https://www.1688.com/", "webSocketDebuggerUrl": "ws://unused"}]
        dashboard.reusable_1688_page = lambda pages: pages[0]
        dashboard.navigate_existing_cdp_tab = lambda _page, _url: True
        dashboard.close_duplicate_1688_search_tabs = lambda _keep: None
        dashboard.open_1688_helper_browser("mommy-and-me", 2, "balanced")
        history = json.loads(dashboard.SEARCH_HISTORY_PATH.read_text(encoding="utf-8"))
        assert history["categories"]["mommy-and-me"]["next_query_index"] == 7, "opening a saved term must not rotate it"

    print("ok")


if __name__ == "__main__":
    main()
