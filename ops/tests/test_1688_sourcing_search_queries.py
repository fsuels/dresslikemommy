#!/usr/bin/env python3
"""Regression checks for the 1688 sourcing search query bank."""

from __future__ import annotations

import importlib.util
import sys
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
        assert all("2026" in query for query in queries)
        assert all("新款" in query for query in queries)
        assert all("一件代发" in query for query in queries)
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
        assert all("美国站" in query and "跨境" in query and "外贸" in query for query in us_queries)
        assert all("欧洲站" in query and "跨境" in query and "外贸" in query for query in eu_queries)
        for phrase in expected["phrases"]:
            assert any(phrase in query for query in queries), f"missing {category_id} search phrase: {phrase}"

    sample = "母女晚礼服 2026 春夏 新款 高端 气质 一件代发"
    url = collector.search_url(sample, page=2)
    assert decoded_keywords(url) == sample
    assert collector.decoded_search_keywords(url) == sample
    assert collector.search_page_matches(url, url)
    plus_url = url.replace("%20", "+")
    assert collector.search_page_matches(url, plus_url)
    mismatch_url = collector.search_url("孕妇写真裙 2026 春夏 新款 影楼 一件代发")
    assert not collector.search_page_matches(url, mismatch_url)
    assert "beginPage=2" in url
    assert collector.search_history_key("mommy-and-me", "us") == "mommy-and-me:us"
    assert collector.search_history_key("mommy-and-me", "balanced") == "mommy-and-me"

    print("ok")


if __name__ == "__main__":
    main()
