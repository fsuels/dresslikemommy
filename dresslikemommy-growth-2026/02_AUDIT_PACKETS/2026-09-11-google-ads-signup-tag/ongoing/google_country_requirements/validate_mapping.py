"""Validate local requirements mapping; write only sibling VALIDATION.json."""
from pathlib import Path
from urllib.parse import urlparse
import collections
import csv
import datetime
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
MARKETS = HERE.parent / "markets"


def rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


canonical_paths = [ROOT / "ops/marketing" / name for name in
                   ["keyword_strategy.md", "keyword_factory_015_cpc_criteria.md",
                    "keyword_scoring_rubric.md", "us_primary_keyword_lane.md", "keyword_universe.csv"]]
before = {str(f): sha(f) for f in canonical_paths}
countries = rows(HERE / "country_requirements_65.csv")
locales = rows(HERE / "locale_requirements_21.csv")
currencies = rows(HERE / "currency_requirements_20.csv")
input_countries = rows(MARKETS / "active_country_inventory.csv")
input_locales = rows(MARKETS / "locale_routes.csv")
market = json.loads((MARKETS / "market_readback.json").read_text())
facts = json.loads((HERE / "official_source_facts.json").read_text())
sources = json.loads((HERE / "sources.json").read_text())
evidence = json.loads((HERE / "LOCAL_EVIDENCE.json").read_text())
by_country = {r["country_code"]: r for r in countries}
checks = {}
checks["65_unique_country_codes_exact_input_set"] = len(countries) == len(by_country) == 65 and set(by_country) == {r["country_code"] for r in input_countries}
checks["country_names_currency_and_market_identity_preserved"] = all(
    all(by_country[r["country_code"]][a] == r[b] for a, b in
        [("country_name", "country_name"), ("configured_currency", "configured_currency"),
         ("shopify_market_handles", "market_handles")]) for r in input_countries)
checks["21_locales_and_roots_exact"] = len(locales) == 21 and {
    (r["shopify_locale"], r["shopify_configured_root"]) for r in locales} == {
    (r["locale"], r["root_url"]) for r in input_locales}
checks["20_currencies_exact_enabled_set"] = len(currencies) == 20 and {
    r["shopify_enabled_currency"] for r in currencies} == set(market["shop"]["enabledPresentmentCurrencies"])
checks["all_21_languages_documented"] = len(facts["merchant_supported_language_names"]) == 21 and all(
    r["google_merchant_language_name"] in facts["merchant_supported_language_names"] and
    r["merchant_language_support"] == "LISTED_SUPPORTED_LANGUAGE" for r in locales)
checks["country_table_counts_26_1_9_29"] = collections.Counter(r["google_general_country_listing"] for r in countries) == {
    "LISTED_STANDARD": 26, "LISTED_BETA": 1,
    "NOT_LISTED_IN_OPENED_GENERAL_TABLES": 9, "NOT_LISTED_IN_OPENED_TABLES": 29}
checks["36_app_country_rows"] = sum(r["google_app_sync_listing"] == "LISTED" for r in countries) == len(facts["app_sync_relevant_rows"]) == 36
checks["nine_doc_scope_differences_explicit"] = {r["country_code"] for r in countries if
    r["shopping_ads_platform_gate"] == "UNKNOWN_DOCUMENTATION_SCOPE_DIFFERENCE"} == set("BG CY HR LT LU LV MT RS SI".split())
checks["russia_paid_pause_separate_from_table_and_free_listings"] = (
    by_country["RU"]["google_general_country_listing"] == "LISTED_STANDARD" and
    by_country["RU"]["shopping_ads_platform_gate"] == by_country["RU"]["google_search_serving_gate"] == "PAUSED_BY_GOOGLE_TO_USERS_IN_RUSSIA" and
    by_country["RU"]["free_listing_account_approval"].startswith("UNKNOWN"))
checks["territory_codes_never_replaced_with_parent"] = all(r["country_code_substitution"].startswith("NONE") for r in countries)
checks["france_exception_not_global_country_rejection"] = all(
    by_country[c]["fr_metropole_exception"] == "FR target expressly excludes French overseas; no FR remap" and
    by_country[c]["shopping_ads_platform_gate"] == "UNKNOWN_TARGET_SUPPORT"
    for c in "BL GF GP MF MQ PM RE TF WF YT".split())
checks["mexico_norway_conversion_not_unsupported"] = all(
    by_country[c]["currency_evidence_gate"] == "SUPPORTED_SOURCE_CURRENCY_CONVERSION_PATH_RUNTIME_UNKNOWN"
    for c in ["MX", "NO"])
checks["twelve_currency_table_matches_eight_unresolved"] = sum(
    r["google_general_table_currency_presence"] == "LISTED" for r in currencies) == 12 and {
    r["shopify_enabled_currency"] for r in currencies if r["google_general_table_currency_presence"] != "LISTED"
    } == set("BSD FJD ISK KYD RSD WST XCD XPF".split())
checks["no_account_offer_or_runtime_approval_inferred"] = all(
    r["actual_offer_approval"] == r["actual_ads_targeting"] == "UNKNOWN" and
    r["storefront_and_checkout_test"].startswith("NOT_RUN") for r in countries)
checks["search_eligibility_not_derived_from_merchant_list"] = all(
    r["google_search_serving_gate"] == "UNKNOWN_NOT_INFERRED_FROM_MERCHANT_TABLE" for r in countries if r["country_code"] != "RU")
checks["source_ids_and_official_urls_resolve"] = len({r["source_id"] for r in sources}) == len(sources) and all(
    set(r["source_ids"].split(";")) <= {s["source_id"] for s in sources} for r in countries + locales + currencies) and all(
    urlparse(s["url"]).scheme == "https" and urlparse(s["url"]).netloc == "support.google.com" for s in sources)
checks["checked_dates_current_task_date"] = all(r["checked_date"] == "2026-09-11" for r in countries + locales + currencies) and all(s["checked_at_utc"].startswith("2026-09-11T") for s in sources)
checks["source_snapshots_unchanged"] = all(sha(ROOT / rel) == v["sha256"] for rel, v in evidence["local_source_hashes"].items())
checks["five_applied_canonical_files_untouched_during_check"] = all(sha(Path(rel)) == digest for rel, digest in before.items())
links = re.findall(r"\]\(([^)]+)\)", (HERE / "README.md").read_text())
checks["local_document_links_resolve"] = all(link.startswith("https://") or Path(link).exists() or
    Path(link) == HERE / "VALIDATION.json" for link in links)
checks["no_trailing_spaces_in_packet"] = all(not any(line.endswith((" ", "\t")) for line in
    f.read_text().splitlines()) for f in HERE.iterdir() if f.is_file() and f.suffix in {".md", ".json", ".csv", ".py"})
result = {"checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status": "PASS_LOCAL_MAPPING" if all(checks.values()) else "FAILED",
          "checks": checks, "country_rows": len(countries), "locale_rows": len(locales),
          "currency_rows": len(currencies), "live_account_validation": "NOT RUN",
          "storefront_HTTP": "NOT RUN; hold respected", "external_changes": "NONE",
          "canonical_changes_by_this_lane": "NONE", "canonical_hashes_observed": before,
          "scope": "Source-bound documentation and local data joins; neither eligibility nor approval certification."}
(HERE / "VALIDATION.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": result["status"], "passed": sum(checks.values()), "total": len(checks),
                  "failed": [k for k, v in checks.items() if not v]}, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
