#!/usr/bin/env python3
"""Regression checks for the 1688 sourcing score detail-stage Gold gate."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORER_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_score.py"


def load_scorer():
    spec = importlib.util.spec_from_file_location("sourcing_score", SCORER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load scorer from {SCORER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def base_candidate_fields() -> dict[str, str]:
    return {
        "candidate_id": "detail-gate",
        "product_url": "https://detail.1688.com/offer/900000000001.html",
        "image_url": "https://img.example.com/main.jpg",
        "title": "2026 new mommy and me matching floral dress parent-child family outfits",
        "category_id": "mommy-and-me",
        "category_match": "5",
        "style_fit": "5",
        "image_quality": "5",
        "moq": "1",
        "monthly_sales": "260",
        "repurchase_rate_pct": "45%",
        "rating": "4.9",
        "years_on_1688": "6",
        "badges": "实力商家 买家保障 品质保障",
        "service_flags": "一件代发 24小时发货 官方物流 响应快",
        "raw_card_text": "2026新款 母女 亲子 现货 一件代发 买家保障 品质保障",
        "ip_risk_flags": "",
    }


def assert_contains_all(values: list[str], expected: list[str]) -> None:
    for item in expected:
        assert item in values, f"missing {item!r} from {values!r}"


def main() -> None:
    scorer = load_scorer()
    Candidate = scorer.Candidate

    search_stage = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert search_stage.verdict == "Test"
    assert search_stage.review_stage == "search"
    assert "size chart not confirmed" in search_stage.concerns

    new_offer_without_year = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "product_url": "https://detail.1688.com/offer/917144772330.html",
                "title": "in stock French Mother and Daughter family matching floral holiday dress",
                "raw_card_text": "母女 亲子 现货 MOQ 1 回头率 86% 2000 sold",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert new_offer_without_year.verdict == "Test"
    assert "no visible 2025/2026 freshness signal on search card" not in new_offer_without_year.concerns
    assert "freshness not visible on search card; detail page must prove current availability" in new_offer_without_year.concerns

    american_market_good = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "american-market-good",
                "product_url": "https://detail.1688.com/offer/917144772334.html",
                "title": "2026 US market mommy and me resort matching dress",
                "raw_card_text": "母女 亲子 欧美 美国站 外贸 跨境 2026新款 MOQ 1 月销 120 实力商家 买家保障 一件代发 24小时发货",
                "search_query": "母女沙滩裙 2026 夏季 新款 度假 欧美 美国站 跨境 外贸 一件代发",
                "market_target": "us",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert american_market_good.verdict == "Test"
    assert american_market_good.market_target == "us"
    assert "American market search focus" in american_market_good.positive_signals
    assert "American market style/cross-border signal on product card" in american_market_good.positive_signals

    american_market_weak_vendor = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "american-market-weak-vendor",
                "product_url": "https://detail.1688.com/offer/917144772335.html",
                "title": "2026 US market mommy and me resort matching dress",
                "raw_card_text": "母女 亲子 欧美 美国站 外贸 跨境 2026新款 MOQ 1 一件代发",
                "search_query": "母女沙滩裙 2026 夏季 新款 度假 欧美 美国站 跨境 外贸 一件代发",
                "market_target": "us",
                "monthly_sales": "",
                "repurchase_rate_pct": "",
                "rating": "",
                "years_on_1688": "",
                "badges": "",
                "service_flags": "一件代发",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert american_market_weak_vendor.verdict == "Reject"
    assert "American market focus requires reputable-vendor or demand proof on the search card" in american_market_weak_vendor.concerns

    european_market_old_offer = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "european-market-old-offer",
                "product_url": "https://detail.1688.com/offer/810000000001.html",
                "title": "2026 European mother daughter formal dress",
                "raw_card_text": "母女 亲子 欧洲站 欧美 法式 外贸 跨境 2026新款 MOQ 1 月销 120 实力商家 买家保障 一件代发",
                "search_query": "母女礼服裙 2026 春夏 新款 蕾丝 欧洲站 欧美 跨境 外贸 一件代发",
                "market_target": "eu",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert european_market_old_offer.verdict == "Reject"
    assert any("older 1688 offer ID" in concern for concern in european_market_old_offer.concerns)

    query_category_fit = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "query-fit",
                "product_url": "https://detail.1688.com/offer/917144772331.html",
                "title": "Summer resort men shirt and women dress matching set",
                "raw_card_text": "MOQ 1 回头率 45% 500 sold 一件代发 现货",
                "search_query": "情侣装 2026 夏季 一件代发",
                "category_id": "couples",
                "category_match": "",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert query_category_fit.verdict == "Test"
    assert query_category_fit.category_match == "4"

    ordinary_maternity = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "ordinary-maternity",
                "product_url": "https://detail.1688.com/offer/917144772332.html",
                "title": "2026 summer maternity nursing dress loose casual Korean maternity wear",
                "raw_card_text": "孕妇 夏季 连衣裙 宽松 2026新款 MOQ 1 回头率 55% 一件代发",
                "search_query": "孕妇拍照服装 2026 春夏 新款 影楼 一件代发",
                "category_id": "maternity",
                "category_match": "",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert ordinary_maternity.verdict == "Reject"
    assert ordinary_maternity.category_match == "3"
    assert "ordinary maternity item; missing photoshoot/studio/gown signal" in ordinary_maternity.concerns

    photoshoot_maternity = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "candidate_id": "photoshoot-maternity",
                "product_url": "https://detail.1688.com/offer/917144772333.html",
                "title": "Studio photo shoot ultra-fairy white maternity gown for pregnant moms",
                "raw_card_text": "孕妇写真 影楼 礼服 白纱裙 2026新款 MOQ 1 回头率 55% 一件代发",
                "search_query": "孕妇写真裙 2026 春夏 新款 唯美 仙女 一件代发",
                "category_id": "maternity",
                "category_match": "",
                "vendor_name": "",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "availability": "",
            }
        ),
        review_stage="search",
    )

    assert photoshoot_maternity.verdict == "Test"
    assert photoshoot_maternity.category_match == "5"
    assert "maternity photoshoot/studio gown signal" in photoshoot_maternity.positive_signals

    detail_missing_proof = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "vendor_name": "",
                "vendor_url": "",
                "vendor_location": "",
                "badges": "买家保障 品质保障",
                "service_flags": "官方物流 响应快",
                "raw_card_text": "2026新款 母女 亲子 买家保障 品质保障",
                "size_chart": "",
                "dropship_supported": "",
                "vendor_image_urls": "",
                "vendor_images_path": "",
                "availability": "",
                "image_quality": "3",
            }
        ),
        review_stage="detail",
    )

    assert detail_missing_proof.verdict != "Gold"
    assert detail_missing_proof.review_stage == "detail"
    assert_contains_all(
        detail_missing_proof.concerns,
        [
            "supplier proof not captured on detail page",
            "size chart not confirmed on detail page",
            "dropship/one-piece support not confirmed on detail page",
            "dispatch speed or ready-stock proof not captured on detail page",
            "usable vendor image set not captured on detail page",
        ],
    )

    detail_with_proof = scorer.score_candidate(
        Candidate(
            **{
                **base_candidate_fields(),
                "vendor_name": "Guangzhou Bright Apparel Co.",
                "vendor_url": "https://shop.1688.com/example",
                "vendor_location": "Guangzhou",
                "size_chart": "yes",
                "dropship_supported": "yes",
                "vendor_image_urls": ",".join(
                    [
                        "https://img.example.com/1.jpg",
                        "https://img.example.com/2.jpg",
                        "https://img.example.com/3.jpg",
                        "https://img.example.com/4.jpg",
                    ]
                ),
                "availability": "ready stock / ships within 24 hours",
                "detail_evidence_path": "ops/sourcing/evidence/900000000001.json",
            }
        ),
        review_stage="detail",
    )

    assert detail_with_proof.verdict == "Gold"
    assert detail_with_proof.review_stage == "detail"
    assert detail_with_proof.score >= 78
    assert detail_with_proof.concerns == []
    assert "size chart confirmed" in detail_with_proof.positive_signals
    assert "one-piece/dropship signal" in detail_with_proof.positive_signals
    assert "24h dispatch signal" in detail_with_proof.positive_signals
    assert "vendor image set captured (4)" in detail_with_proof.positive_signals

    print("ok")


if __name__ == "__main__":
    main()
