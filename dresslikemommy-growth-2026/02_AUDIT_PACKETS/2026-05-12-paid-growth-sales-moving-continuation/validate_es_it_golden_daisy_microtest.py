#!/usr/bin/env python3
"""Validate the ES/IT Golden Daisy microtest review-only packet.

This script reads local evidence files only. It does not call Google Ads,
Shopify, Merchant Center, Pinterest, or any external API.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent
NATIVE_PACKET = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-es-it-native-qa-no-upload-slice"
KEYWORD_PATH = LANE / "es_it_golden_daisy_microtest_keywords_review_only.csv"
RSA_PATH = LANE / "es_it_golden_daisy_microtest_rsa_review_only.csv"
LANDING_QA_PATH = NATIVE_PACKET / "es_it_country_landing_qa_summary.json"
CHECKOUT_QA_PATH = LANE / "lanes/es-it-golden-daisy-checkout/es_it_golden_daisy_checkout_to_shipping_summary.json"
SUMMARY_PATH = LANE / "es_it_golden_daisy_microtest_validation_summary.json"

EXPECTED = {
    "ES": {
        "locale": "es-ES",
        "language": "Spanish",
        "url": "https://www.dresslikemommy.com/es/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=ES",
        "landing_decision": "ES_COUNTRY_QUALIFIED_LANDING_QA_PASSED",
        "checkout_decision": "ES_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER",
        "keywords": {
            "vestidos mamá e hija",
            "vestidos madre e hija",
            "vestidos madre hija a juego",
        },
    },
    "IT": {
        "locale": "it-IT",
        "language": "Italian",
        "url": "https://www.dresslikemommy.com/it/products/golden-daisy-mommy-and-me-set?variant=44197959499873&country=IT",
        "landing_decision": "IT_COUNTRY_QUALIFIED_LANDING_QA_PASSED",
        "checkout_decision": "IT_CHECKOUT_TO_SHIPPING_PASSED_READONLY_NO_PAYMENT_NO_ORDER",
        "keywords": {
            "abiti mamma e figlia",
            "vestiti mamma e figlia",
            "abiti madre e figlia",
        },
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def check(condition: bool, name: str, observed: object, expected: object, checks: list[dict[str, object]]) -> None:
    checks.append(
        {
            "check": name,
            "status": "PASS" if condition else "FAIL",
            "observed": observed,
            "expected": expected,
        }
    )


def main() -> int:
    checks: list[dict[str, object]] = []
    keyword_rows = read_csv(KEYWORD_PATH)
    rsa_rows = read_csv(RSA_PATH)
    source_keyword_rows = read_csv(NATIVE_PACKET / "es_it_native_keyword_replacements_review_only.csv")
    source_rsa_rows = read_csv(NATIVE_PACKET / "es_it_native_rsa_replacements_review_only.csv")
    landing_json = json.loads(LANDING_QA_PATH.read_text(encoding="utf-8"))
    landing_data = landing_json["rows"] if isinstance(landing_json, dict) else landing_json
    checkout_data = json.loads(CHECKOUT_QA_PATH.read_text(encoding="utf-8"))["summaries"]

    check(len(keyword_rows) == 6, "keyword_row_count", len(keyword_rows), 6, checks)
    check(len(rsa_rows) == 2, "rsa_row_count", len(rsa_rows), 2, checks)
    check({row["upload_status"] for row in keyword_rows} == {"REVIEW_ONLY_NOT_UPLOAD"}, "keyword_upload_status", sorted({row["upload_status"] for row in keyword_rows}), ["REVIEW_ONLY_NOT_UPLOAD"], checks)
    check({row["upload_status"] for row in rsa_rows} == {"REVIEW_ONLY_NOT_UPLOAD"}, "rsa_upload_status", sorted({row["upload_status"] for row in rsa_rows}), ["REVIEW_ONLY_NOT_UPLOAD"], checks)
    check({row["review_status"] for row in keyword_rows + rsa_rows} == {"NATIVE_REVIEW_REQUIRED"}, "review_status", sorted({row["review_status"] for row in keyword_rows + rsa_rows}), ["NATIVE_REVIEW_REQUIRED"], checks)
    check({row["match_type"] for row in keyword_rows} == {"Exact"}, "keyword_match_type", sorted({row["match_type"] for row in keyword_rows}), ["Exact"], checks)

    source_keyword_keys = {
        (row["market"], row["locale"], row["language"], row["theme"], row["match_type"], row["corrected_keyword"], row["upload_status"])
        for row in source_keyword_rows
    }
    source_rsa_keys = {
        (row["market"], row["locale"], row["language"], row["theme"], row["headlines"], row["descriptions"], row["upload_status"])
        for row in source_rsa_rows
    }
    landing_by_market = {row["market"]: row for row in landing_data}
    checkout_by_market = {row["country_code"]: row for row in checkout_data}

    for market, expected in EXPECTED.items():
        market_keywords = [row for row in keyword_rows if row["market"] == market]
        market_rsa = [row for row in rsa_rows if row["market"] == market]
        check(len(market_keywords) == 3, f"{market}_keyword_count", len(market_keywords), 3, checks)
        check(len(market_rsa) == 1, f"{market}_rsa_count", len(market_rsa), 1, checks)
        check({row["keyword"] for row in market_keywords} == expected["keywords"], f"{market}_keyword_set", sorted({row["keyword"] for row in market_keywords}), sorted(expected["keywords"]), checks)
        check({row["final_url"] for row in market_keywords + market_rsa} == {expected["url"]}, f"{market}_final_url", sorted({row["final_url"] for row in market_keywords + market_rsa}), [expected["url"]], checks)
        check({row["locale"] for row in market_keywords + market_rsa} == {expected["locale"]}, f"{market}_locale", sorted({row["locale"] for row in market_keywords + market_rsa}), [expected["locale"]], checks)
        check({row["language"] for row in market_keywords + market_rsa} == {expected["language"]}, f"{market}_language", sorted({row["language"] for row in market_keywords + market_rsa}), [expected["language"]], checks)

        missing_source_keywords = [
            row["keyword"]
            for row in market_keywords
            if (row["market"], row["locale"], row["language"], "Mommy & Me Dresses", row["match_type"], row["keyword"], row["upload_status"])
            not in source_keyword_keys
        ]
        check(not missing_source_keywords, f"{market}_keywords_exist_in_source_native_packet", missing_source_keywords, [], checks)

        rsa = market_rsa[0]
        check(rsa["headline_count"] == "15", f"{market}_rsa_headline_count", rsa["headline_count"], "15", checks)
        check(rsa["description_count"] == "4", f"{market}_rsa_description_count", rsa["description_count"], "4", checks)
        check(
            (rsa["market"], rsa["locale"], rsa["language"], "Mommy & Me Dresses", rsa["headlines"], rsa["descriptions"], rsa["upload_status"])
            in source_rsa_keys,
            f"{market}_rsa_exists_in_source_native_packet",
            "present" if (rsa["market"], rsa["locale"], rsa["language"], "Mommy & Me Dresses", rsa["headlines"], rsa["descriptions"], rsa["upload_status"]) in source_rsa_keys else "missing",
            "present",
            checks,
        )

        landing = landing_by_market.get(market, {})
        check(landing.get("decision") == expected["landing_decision"], f"{market}_landing_qa_decision", landing.get("decision"), expected["landing_decision"], checks)
        check(landing.get("status") == 200 or landing.get("status") == "200", f"{market}_landing_http_status", landing.get("status"), 200, checks)
        check(not landing.get("forbidden_hits"), f"{market}_landing_forbidden_hits", landing.get("forbidden_hits"), "", checks)
        check(not landing.get("stale_hits"), f"{market}_landing_stale_hits", landing.get("stale_hits"), "", checks)

        checkout = checkout_by_market.get(market, {})
        check(checkout.get("decision") == expected["checkout_decision"], f"{market}_checkout_decision", checkout.get("decision"), expected["checkout_decision"], checks)
        check(checkout.get("cart_currency") == "EUR", f"{market}_checkout_cart_currency", checkout.get("cart_currency"), "EUR", checks)
        check(checkout.get("shipping_ui_pass") is True, f"{market}_checkout_shipping_ui_pass", checkout.get("shipping_ui_pass"), True, checks)
        check(checkout.get("payment_or_order_created") is False, f"{market}_checkout_no_payment_or_order", checkout.get("payment_or_order_created"), False, checks)
        check(checkout.get("blocked_by_verification_text") is False, f"{market}_checkout_no_verification_wall", checkout.get("blocked_by_verification_text"), False, checks)

    summary = {
        "status": "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL",
        "checks": checks,
        "files": {
            "keywords": str(KEYWORD_PATH.relative_to(ROOT)),
            "rsas": str(RSA_PATH.relative_to(ROOT)),
            "landing_qa": str(LANDING_QA_PATH.relative_to(ROOT)),
            "checkout_qa": str(CHECKOUT_QA_PATH.relative_to(ROOT)),
        },
        "writes_made": "local_validation_summary_only",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "summary": str(SUMMARY_PATH), "checks": len(checks)}, indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
