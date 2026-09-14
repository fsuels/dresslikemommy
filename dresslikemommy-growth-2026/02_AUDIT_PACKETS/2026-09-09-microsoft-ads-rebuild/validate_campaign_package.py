#!/usr/bin/env python3
"""Validate local Microsoft campaign specs without contacting an external service."""
import argparse
import csv
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

def norm(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w]+", " ", value).split())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-readiness", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    names = {
        "campaigns": "campaigns.csv", "ad_groups": "ad_groups.csv",
        "keywords": "keywords.csv", "negative_keywords": "negative_keywords.csv",
        "responsive_search_ads": "responsive_search_ads.csv",
    }
    tables = {}
    errors = []
    checks = 0
    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(message)
    for kind, filename in names.items():
        with (base / filename).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            check(bool(reader.fieldnames), f"{filename}: header missing")
            check(len(set(reader.fieldnames or [])) == len(reader.fieldnames or []),
                  f"{filename}: duplicate header")
            check(bool(rows), f"{filename}: no rows")
            for index, row in enumerate(rows, 2):
                check(None not in row, f"{filename}:{index}: extra columns")
                check(all(v is not None for v in row.values()), f"{filename}:{index}: missing cells")
            tables[kind] = rows
    readiness_path = base / "market_readiness.json"
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    campaigns = {r["campaign_key"]: r for r in tables["campaigns"]}
    groups = {r["ad_group_key"]: r for r in tables["ad_groups"]}
    for kind, key in (("campaigns", "campaign_key"), ("ad_groups", "ad_group_key"),
                      ("keywords", "keyword_key"), ("responsive_search_ads", "ad_key")):
        rows = tables[kind]
        check(len({r[key] for r in rows}) == len(rows), f"{kind}: duplicate local key")
    locales = {r["locale"]: r for r in readiness["published_languages"]}
    country_codes = {r["country"] for r in readiness["market_memberships"]
                     if r["market_status"] == "ACTIVE" and r["currency_enabled"]}
    check(len(locales) == readiness["statistics"]["published_locales"], "Locale count mismatch")
    check(len(country_codes) == readiness["statistics"]["distinct_countries"], "Country count mismatch")
    check(len(readiness["market_memberships"]) == readiness["statistics"]["country_memberships"],
          "Country membership count mismatch")
    for c in campaigns.values():
        label = c["campaign_key"]
        check(c["status"] == "Paused", f"{label}: campaign is not Paused")
        check(c["account_id"] == "477439" and c["customer_id"] == "770182",
              f"{label}: wrong Microsoft account/customer")
        check(c["account_currency"] == "USD", f"{label}: wrong currency")
        check(c["country_code"] in country_codes, f"{label}: country unavailable in current configuration")
        check(c["shopify_locale"] in locales and locales[c["shopify_locale"]]["published"],
              f"{label}: locale is not published")
        check(c["budget_authorized"] == "false" and c["bid_cap_current_account_verified"] == "false",
              f"{label}: unsupported live authority/cap claim")
        check(c["location_intent"] == "People in your targeted locations",
              f"{label}: physical-presence intent missing")
        check(c["proposed_bid_strategy"] == "MaxClicks", f"{label}: unexpected bid strategy")
        check(float(c["proposed_max_cpc_usd"]) == 0.15 and
              float(c["proposed_max_cpc_account_currency"]) == 0.15,
              f"{label}: incorrect proposed CPC assumption")
        check(float(c["proposed_daily_budget_usd"]) > 0 and
              float(c["proposed_daily_budget_usd"]) == float(c["proposed_daily_budget_account_currency"]),
              f"{label}: invalid or unconverted budget")
        check(not c["start_date"] and not c["end_date"], f"{label}: unapproved live dates")
    for g in groups.values():
        c = campaigns.get(g["campaign_key"])
        check(c is not None, f"{g['ad_group_key']}: missing campaign")
        if c is None:
            continue
        check(g["status"] == "Paused", f"{g['ad_group_key']}: group is not Paused")
        check(g["type"] == "SearchStandard", f"{g['ad_group_key']}: not SearchStandard")
        check(g["language"] == "", f"{g['ad_group_key']}: unexpected language override")
        check(g["required_buyer_country"] == c["country_code"], f"{g['ad_group_key']}: wrong buyer country")
        resource_path = ("collections/mommy-and-me" if g["intent"] == "dresses"
                         else "products/sunshine-stripe-family-matching-tops")
        expected = locales[c["shopify_locale"]]["language_root"] + resource_path
        check(g["final_url"] == expected, f"{g['ad_group_key']}: wrong locale/intent destination")
        check(g["rendered_buyer_path_verified"] == "false", f"{g['ad_group_key']}: unsupported buyer proof")
        check(g["keyword_bid"] == "", f"{g['ad_group_key']}: misleading keyword cap")
    positive_keys = set()
    for k in tables["keywords"]:
        g = groups.get(k["ad_group_key"])
        check(g is not None, f"{k['keyword_key']}: missing ad group")
        if g is None:
            continue
        check(k["campaign_key"] == g["campaign_key"], f"{k['keyword_key']}: wrong campaign")
        check(k["status"] == "Paused", f"{k['keyword_key']}: keyword is not Paused")
        check(k["match_type"] in {"Exact", "Phrase"}, f"{k['keyword_key']}: unsupported match")
        check(k["final_url"] == g["final_url"], f"{k['keyword_key']}: landing mismatch")
        check(not any(ch in k["keyword"] for ch in "[]+"), f"{k['keyword_key']}: match syntax in text")
        check(k["keyword_bid"] == "" and k["demand_and_cpc_status"] == "UNMEASURED" and
              not k["observed_current_avg_cpc"] and not k["observed_current_volume"],
              f"{k['keyword_key']}: unsupported numeric evidence")
        if k["match_type"] == "Phrase":
            check(k["local_activation"] == "PHRASE_RESERVE_AFTER_TERMS_REVIEW",
                  f"{k['keyword_key']}: phrase row not reserved")
        key = (k["campaign_key"], norm(k["keyword"]), k["match_type"])
        check(key not in positive_keys, f"{k['keyword_key']}: duplicate normalized campaign keyword")
        positive_keys.add(key)
    negative_keys = set()
    for n in tables["negative_keywords"]:
        check(n["campaign_key"] in campaigns, "Negative references missing campaign")
        check(n["scope"] in {"Campaign", "AdGroup"}, "Negative has unsupported scope")
        check(n["match_type"] in {"Exact", "Phrase"}, "Negative has unsupported match")
        check(n["local_state"] in {"PROPOSED_ONLY", "HOLD_SEMANTIC_REVIEW"},
              "Negative has an unsupported execution/review state")
        if n["scope"] == "AdGroup":
            check(n["ad_group_key"] in groups, "Negative references missing group")
            check(n["local_state"] == "HOLD_SEMANTIC_REVIEW" and
                  n["local_staging_state"] == "EXCLUDED_FROM_STAGING",
                  "Unreviewed cross-garment negative may not enter staging")
        else:
            check(not n["ad_group_key"], "Campaign negative has ad-group key")
            check(n["local_state"] == "PROPOSED_ONLY", "Strong intent seed unexpectedly reclassified")
        key = (n["campaign_key"], n["ad_group_key"], norm(n["negative_keyword"]), n["match_type"])
        check(key not in negative_keys, "Duplicate normalized negative in same scope")
        negative_keys.add(key)
    for k in tables["keywords"]:
        positives = " " + norm(k["keyword"]) + " "
        for n in tables["negative_keywords"]:
            if n["local_state"] == "HOLD_SEMANTIC_REVIEW":
                continue
            if n["campaign_key"] != k["campaign_key"]:
                continue
            if n["ad_group_key"] and n["ad_group_key"] != k["ad_group_key"]:
                continue
            negative = norm(n["negative_keyword"])
            blocked = (norm(k["keyword"]) == negative if n["match_type"] == "Exact"
                       else " " + negative + " " in positives)
            check(not blocked, f"Positive/negative conflict: {k['keyword_key']} / {n['negative_keyword']}")
    headline_lengths, description_lengths, path_lengths = [], [], []
    disallowed_claims = re.compile(
        r"free shipping|30.day returns|in stock|warehouse|bestsell|lowest price|guaranteed delivery|"
        r"envío gratis|livraison gratuite|versandkostenfrei|spedizione gratuita", re.I)
    for ad in tables["responsive_search_ads"]:
        g = groups.get(ad["ad_group_key"])
        check(g is not None, f"{ad['ad_key']}: missing group")
        if g is None:
            continue
        check(ad["campaign_key"] == g["campaign_key"], f"{ad['ad_key']}: wrong campaign")
        check(ad["status"] == "Paused", f"{ad['ad_key']}: ad is not Paused")
        check(ad["ad_type"] == "ResponsiveSearchAd", f"{ad['ad_key']}: wrong ad type")
        check(ad["final_url"] == g["final_url"], f"{ad['ad_key']}: landing mismatch")
        check(ad["native_review"] == "PENDING" and ad["editorial_review"] == "NOT_SUBMITTED",
              f"{ad['ad_key']}: unsupported review claim")
        check(ad["import_schema"] == "LOCAL_REVIEW_TABLE_NOT_MICROSOFT_BULK",
              f"{ad['ad_key']}: misleading import label")
        headlines = [v for k, v in ad.items() if k.startswith("headline_") and v]
        descriptions = [v for k, v in ad.items() if k.startswith("description_") and v]
        check(3 <= len(headlines) <= 15, f"{ad['ad_key']}: headline count")
        check(2 <= len(descriptions) <= 4, f"{ad['ad_key']}: description count")
        check(len(set(headlines)) == len(headlines), f"{ad['ad_key']}: duplicate headline")
        for value in headlines:
            headline_lengths.append(len(value))
            check(len(value) <= 30, f"{ad['ad_key']}: headline over 30: {value}")
        for value in descriptions:
            description_lengths.append(len(value))
            check(len(value) <= 90, f"{ad['ad_key']}: description over 90: {value}")
        for field in ("path_1", "path_2"):
            path_lengths.append(len(ad[field]))
            check(len(ad[field]) <= 15, f"{ad['ad_key']}: display path over 15")
        parsed = urlparse(ad["final_url"])
        check(parsed.scheme == "https" and parsed.netloc == "www.dresslikemommy.com",
              f"{ad['ad_key']}: unsafe destination")
        check(not parsed.query and not parsed.fragment, f"{ad['ad_key']}: unverified URL parameter")
        params = parse_qs(ad["final_url_suffix"])
        check(params.get("utm_source") == ["bing"] and params.get("utm_medium") == ["cpc"]
              and params.get("utm_campaign") == [ad["campaign_key"]],
              f"{ad['ad_key']}: attribution suffix mismatch")
        check(not disallowed_claims.search(" ".join(headlines + descriptions)),
              f"{ad['ad_key']}: unsupported shipping/stock/promo claim")
    stage = readiness["proposed_initial_stage"]
    expected_campaigns = {"ms_us_en_202609", "ms_de_de_202609"}
    expected_groups = {key + "_dresses" for key in expected_campaigns}
    expected_keywords = {key + "_exact_" + str(i) for key in expected_groups for i in (1, 2, 3)}
    expected_ads = {key + "_rsa_1" for key in expected_groups}
    check(set(stage["staging_campaign_keys"]) == expected_campaigns,
          "Readiness minimal staging must be exactly US-English and Germany-German")
    check(set(stage["staging_ad_group_keys"]) == expected_groups,
          "Readiness minimal staging groups must be the same two dress groups")
    check(set(stage["staging_keyword_keys"]) == expected_keywords,
          "Readiness staging keyword set differs from the six frozen exact candidates")
    check(set(stage["staging_ad_keys"]) == expected_ads, "Readiness staging ads differ")
    check({c["campaign_key"] for c in campaigns.values()
           if c["local_staging_state"] == "MINIMAL_PAUSED_STAGE"} == expected_campaigns,
          "CSV minimal staging campaigns disagree with frozen stage")
    check({g["ad_group_key"] for g in groups.values()
           if g["local_staging_state"] == "MINIMAL_PAUSED_STAGE"} == expected_groups,
          "CSV minimal staging groups disagree with frozen stage")
    check({g["ad_group_key"] for g in groups.values()
           if g["eligible_for_initial_test"] == "candidate_after_gates"} == expected_groups,
          "Initial launch proposal differs from the two-country stage")
    check({k["keyword_key"] for k in tables["keywords"]
           if k["local_staging_state"] == "MINIMAL_PAUSED_STAGE"} == expected_keywords,
          "CSV minimal staging keywords disagree with frozen stage")
    check({a["ad_key"] for a in tables["responsive_search_ads"]
           if a["local_staging_state"] == "MINIMAL_PAUSED_STAGE"} == expected_ads,
          "CSV minimal staging ads disagree with frozen stage")
    staged_negatives = [n for n in tables["negative_keywords"]
                        if n["local_staging_state"] == "MINIMAL_PAUSED_STAGE_PROPOSAL"]
    check(len(staged_negatives) == stage["staging_negative_proposal_count"],
          "Staged negative proposal count disagrees")
    check(all(n["campaign_key"] in expected_campaigns and n["scope"] == "Campaign"
              and n["local_state"] == "PROPOSED_ONLY" for n in staged_negatives),
          "Held or out-of-stage negative leaked into staging")
    check(stage["next_paused_reserve"] == "ms_us_es_202609_dresses" and
          groups["ms_us_es_202609_dresses"]["local_staging_state"] == "NEXT_PAUSED_RESERVE",
          "U.S. Spanish next-reserve scope disagrees")
    check(set(stage["local_reserve_campaign_keys"]) == set(campaigns) - expected_campaigns,
          "Remaining campaign designs must stay local reserves")
    check(stage["us_daily_budget"] == 5 and stage["germany_daily_budget"] == 3 and
          stage["nominal_total"] == 24 and stage["approved"] is False,
          "Two-country budget proposal changed or incorrectly claimed approved")
    for country in readiness["selected_campaign_markets"]:
        campaign = next(c for c in campaigns.values()
                        if c["country_code"] == country["country"]
                        and c["shopify_locale"] == country["locale"])
        check(country["stage"] == campaign["local_stage"], "Market/campaign staging disagrees")
    photo_candidate = next(k for k in tables["keywords"]
                           if k["keyword_key"] == "ms_us_en_202609_dresses_exact_4")
    check(photo_candidate["keyword"] == "mommy and me dresses for pictures" and
          photo_candidate["local_activation"] == "PHOTO_INTENT_FORECAST_REVIEW" and
          photo_candidate["local_staging_state"] == "LOCAL_RESERVE",
          "Photo-intent reserve was lost or silently promoted")
    for k in tables["keywords"]:
        if k["ad_group_key"] == "ms_us_en_202609_dresses" and k["keyword_key"] in expected_keywords:
            check("not tested low-CPC long-tail" in k["intent_evidence_note"],
                  "Close-synonym U.S. exacts lack the performance-evidence caveat")
    plan = (base / "campaign_plan.md").read_text(encoding="utf-8")
    for prefix, expected in (
            ("Minimal paused staging campaign keys:", expected_campaigns),
            ("Minimal paused staging ad group keys:", expected_groups)):
        lines = [line for line in plan.splitlines() if line.startswith(prefix)]
        check(len(lines) == 1, "Plan has missing or ambiguous minimal-stage declaration")
        if len(lines) == 1:
            check(set(re.findall(chr(96) + r"(.*?)" + chr(96), lines[0])) == expected,
                  "Plan/readiness/CSV minimal-stage disagreement")
    held_offers = readiness["collection"]["known_unqualified_offers"]
    check(any(o["product_id"] == "7607764287585" and o["status"] == "NOT_QUALIFIED_FOR_PAID"
              for o in held_offers), "Coral Blossom observed paid hold missing")
    check(readiness["collection"]["paid_qualification_status"] ==
          "HOLD_COLLECTION_AND_SELECTED_OFFER_QUALIFICATION", "Collection qualification hold missing")
    buyer = readiness["buyer_readback"]["buyer"]
    check(buyer["selected_country"] == "Spain" and buyer["currency"] == "EUR"
          and buyer["selected_option"] == "Mother S" and buyer["cart_quantity"] == 1
          and buyer["checkout_reached"] is True and buyer["checkout_displayed_total"] == 30.95,
          "Original Spain single-adult checkout-entry scope changed")
    check(buyer["payment_or_order_submitted"] is False and
          buyer["shipping_rate_and_duties_verified"] is False and
          buyer["purchase_event_verified"] is False, "Spain buyer evidence was overpromoted")
    daughter = readiness["buyer_readback"]["subsequent_root_findings"]["daughter_probe"]
    check(daughter["paired_basket_proven"] is False and daughter["store_add_defect_proven"] is False,
          "Daughter locator timeout was misrepresented as pair or store-defect proof")
    check(readiness["bulk"]["import_ready"] is False, "No platform import validation exists")
    check(readiness["proposed_initial_stage"]["all_rows_paused"] is True, "Initial-state claim mismatch")
    result = {
        "status": "PASS" if not errors else "FAIL",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "counts": {k: len(v) for k, v in tables.items()},
        "max_headline_characters": max(headline_lengths),
        "max_description_characters": max(description_lengths),
        "max_display_path_characters": max(path_lengths),
        "minimal_paused_stage_campaigns": sorted(expected_campaigns),
        "minimal_paused_stage_ad_groups": sorted(expected_groups),
        "minimal_paused_stage_keywords": len(expected_keywords),
        "minimal_paused_stage_ads": len(expected_ads),
        "staging_negative_proposals": len(staged_negatives),
        "held_semantic_negatives": sum(n["local_state"] == "HOLD_SEMANTIC_REVIEW"
                                       for n in tables["negative_keywords"]),
        "errors": errors,
        "limitations": [
            "No Microsoft import, editorial, geographic-ID or live-state validation.",
            "Literal normalized negative checks do not certify semantic close-variant behavior.",
            "No native-language certification, CPC forecast, full U.S./German buyer checkout or profit proof; Spain evidence is limited to one adult checkout entry.",
        ],
        "independent_verifier": "Root integration pending.",
    }
    if args.write_readiness:
        readiness["local_validation"] = result
        readiness["independent_review_corrections"]["status"] = (
            "IMPLEMENTED_LOCAL_VALIDATION_PASS" if not errors else "IMPLEMENTED_VALIDATION_FAILED")
        readiness["generated_at_utc"] = result["checked_at_utc"]
        readiness["evidence_as_of_utc"].pop("shopify_read_window", None)
        readiness["evidence_as_of_utc"]["shopify_read_date"] = "2026-09-09"
        readiness["evidence_as_of_utc"]["shopify_latest_checkpoint"] = "2026-09-09T16:40:35Z"
        readiness_path.write_text(json.dumps(readiness, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
