#!/usr/bin/env python3
"""Regression checks for the 1688 sourcing search query bank."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import urllib.parse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTOR_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_cdp_collect.py"
DASHBOARD_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_dashboard.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def decoded_keywords(url: str) -> str:
    raw_query = urllib.parse.urlsplit(url).query
    raw_keywords = raw_query.split("keywords=", 1)[1].split("&", 1)[0]
    return urllib.parse.unquote_to_bytes(raw_keywords).decode("gbk")


def main() -> None:
    collector = load_module("sourcing_cdp_collect", COLLECTOR_PATH)
    dashboard = load_module("sourcing_dashboard", DASHBOARD_PATH)

    categories = collector.load_categories()
    expectations = {
        "mommy-and-me": {
            "minimum": 29,
            "identity_terms": ("母女", "亲子"),
            "phrases": [
                "母女晚礼服",
                "母女婚礼礼服",
                "母女生日礼服",
                "母女沙滩裙",
                "母女旗袍",
                "母女写真服",
                "母女圣诞裙",
            ],
        },
        "daddy-and-me": {
            "minimum": 24,
            "identity_terms": ("父", "爸爸", "亲子"),
            "phrases": [
                "父子装",
                "父女装",
                "爸爸儿子同款",
                "父子沙滩装",
                "父子西装",
                "父子新年装",
            ],
        },
        "siblings-matching": {
            "minimum": 30,
            "identity_terms": ("姐妹", "兄弟", "兄妹", "姐弟"),
            "phrases": [
                "姐妹装",
                "姐妹连衣裙",
                "姐妹沙滩裙",
                "兄弟同款童装",
                "兄弟西装",
                "兄妹度假装",
                "兄妹圣诞装",
                "姐弟同款童装",
                "姐弟新年装",
            ],
        },
        "family-matching": {
            "minimum": 21,
            "identity_terms": ("全家", "家庭", "亲子", "一家"),
            "phrases": [
                "全家装",
                "一家三口亲子装",
                "母女父子亲子装",
                "家庭沙滩装",
                "全家写真服",
                "家庭圣诞装",
            ],
        },
        "couples": {
            "minimum": 22,
            "identity_terms": ("情侣", "男女"),
            "phrases": [
                "情侣装",
                "男女同款",
                "情侣沙滩装",
                "情侣礼服",
                "情侣写真服",
                "情侣圣诞装",
            ],
        },
        "maternity": {
            "minimum": 33,
            "identity_terms": ("孕", "大肚"),
            "phrases": [
                "孕妇写真裙",
                "孕妇照礼服",
                "孕妇拍照服装",
                "孕妈写真服",
                "大肚照礼服",
                "大肚写真裙",
                "孕肚照服装",
                "影楼孕妇装",
                "新中式 孕妇照",
                "海边孕妇照",
                "情侣孕妇照",
                "孕妇晚礼服",
                "孕妇照婚纱礼服",
                "孕妇写真服",
                "冬季孕妇照礼服",
            ],
        },
    }

    for category_id, expected in expectations.items():
        category = categories[category_id]
        queries = collector.normalize_queries(category["queries"], category.get("search_defaults", {}))
        assert len(queries) >= expected["minimum"]
        assert any("夏季" in query for query in queries)
        assert any("冬季" in query for query in queries)
        assert all("2026" not in query and "新款" not in query and "一件代发" not in query for query in queries)
        assert all(len(query.split()) <= 4 and len(query.replace(" ", "")) <= 18 for query in queries)
        assert all(any(term in query for term in expected["identity_terms"]) for query in queries)
        assert dashboard.configured_queries(category_id) == queries
        us_queries = collector.normalize_queries(
            category["queries"],
            category.get("search_defaults", {}),
            collector.market_profile("us"),
        )
        eu_queries = collector.normalize_queries(
            category["queries"],
            category.get("search_defaults", {}),
            collector.market_profile("eu"),
        )
        assert dashboard.configured_queries(category_id, "us") == us_queries
        assert dashboard.configured_queries(category_id, "eu") == eu_queries
        assert us_queries == queries == eu_queries, "market fit is checked after one concise product search"
        assert all(not any(term in query for term in ("美国站", "欧洲站", "欧美", "跨境", "外贸")) for query in queries)
        for phrase in expected["phrases"]:
            assert any(phrase in query for query in queries), f"missing {category_id} search phrase: {phrase}"

    sample = "母女晚礼服 春夏"
    url = collector.search_url(sample, page=2)
    assert decoded_keywords(url) == sample
    assert collector.decoded_search_keywords(url) == sample
    assert collector.search_page_matches(url, url)
    plus_url = url.replace("%20", "+")
    assert collector.search_page_matches(url, plus_url)
    mismatch_url = collector.search_url("孕妇写真裙 春夏")
    assert not collector.search_page_matches(url, mismatch_url)
    assert "beginPage=2" in url
    assert collector.search_history_key("mommy-and-me", "us") == "mommy-and-me:us"
    assert collector.search_history_key("mommy-and-me", "balanced") == "mommy-and-me"

    assert (
        collector.category_match_score(
            {
                "title": "2026 brother and sister matching kids vacation shirt and dress set",
                "raw_card_text": "siblings coordinated outfits, in stock",
            },
            "siblings-matching",
        )
        == "5"
    )
    assert (
        collector.category_match_score(
            {"title": "2026 women's satin evening dress", "raw_card_text": "adult formalwear, in stock"},
            "siblings-matching",
        )
        == "2"
    )
    assert (
        collector.category_match_score(
            {"title": "women's sexy lingerie set", "raw_card_text": "intimates in stock"},
            "couples",
        )
        == "1"
    )
    assert (
        collector.category_match_score(
            {"title": "women's satin evening dress", "raw_card_text": "Response Rate 90%"},
            "couples",
        )
        == "2"
    )
    assert (
        collector.category_match_score(
            {"title": "women's satin evening dress", "raw_card_text": "Response Rate 90%"},
            "daddy-and-me",
        )
        == "2"
    ), "the letters 'son' inside 'Response' must not create a Daddy & Me match"
    assert (
        collector.category_match_score(
            {"title": "father and son matching winter suits", "raw_card_text": "coordinated outfits"},
            "daddy-and-me",
        )
        == "5"
    )
    assert (
        collector.category_match_score(
            {"title": "pregnant mom and daughter matching dresses", "raw_card_text": "maternity family outfit"},
            "maternity",
        )
        == "5"
    )
    assert (
        collector.category_match_score(
            {"title": "maternity evening gown", "raw_card_text": "pregnancy formalwear"},
            "maternity",
        )
        == "2"
    )

    original_history_path = collector.SEARCH_HISTORY_PATH
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            collector.SEARCH_HISTORY_PATH = Path(temp_dir) / "search-history.json"
            rotating_queries = ["q0", "q1", "q2", "q3"]
            first_batch = collector.queries_for_run(
                "siblings-matching",
                rotating_queries,
                query_index=-1,
                target_reviewable=4,
                max_queries=2,
            )
            assert first_batch == ["q0", "q1"]
            collector.update_search_history(
                category_id="siblings-matching",
                queries=rotating_queries,
                attempted_queries=first_batch,
                collected_pages=[],
                rows=[],
            )
            history = json.loads(collector.SEARCH_HISTORY_PATH.read_text(encoding="utf-8"))
            assert history["categories"]["siblings-matching"]["next_query_index"] == 2
            assert collector.queries_for_run(
                "siblings-matching",
                rotating_queries,
                query_index=-1,
                target_reviewable=4,
                max_queries=2,
            ) == ["q2", "q3"]
            assert collector.queries_for_run(
                "siblings-matching",
                rotating_queries,
                query_index=-1,
                target_reviewable=4,
                max_queries=0,
            ) == ["q2", "q3", "q0", "q1"]
    finally:
        collector.SEARCH_HISTORY_PATH = original_history_path

    print("ok")


if __name__ == "__main__":
    main()
