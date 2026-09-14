"""Reproduce market and funnel inventories from sanitized read-only provider receipts.

Writes only beside this script. No credentials, network access or account mutations.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import unicodedata
from collections import defaultdict
from pathlib import Path


BASE = Path(__file__).resolve().parent
CHECKS = []


def check(name, passed, detail=None):
    CHECKS.append({"check": name, "pass": bool(passed), "detail": detail})
    if not passed:
        raise ValueError(f"Readback validation failed: {name}: {detail}")


def read(name):
    return json.loads((BASE / name).read_text())


def write_json(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_csv(name, rows):
    check(f"{name} nonempty", bool(rows))
    with (BASE / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def canonical_name(value):
    return unicodedata.normalize("NFC", value).strip().casefold()


def pagination_complete(label, connection):
    check(label, connection["pageInfo"]["hasNextPage"] is False)


market_raw = read("provider_markets_response.json")
presence_raw = read("provider_web_presences_response.json")
funnel_raw = read("provider_country_funnel_response.json")
meta = read("capture_metadata.json")
for name, receipt in [("markets", market_raw), ("web presences", presence_raw), ("funnel", funnel_raw)]:
    check(f"{name} provider succeeded", not receipt.get("isError", False))
    check(f"{name} has no GraphQL errors", not receipt["structuredContent"].get("errors"))

data = market_raw["structuredContent"]["data"]
presences = presence_raw["structuredContent"]["data"]["webPresences"]
funnel = funnel_raw["structuredContent"]
shop = data["shop"]
check("exact Shopify domain", shop["myshopifyDomain"] == "dresslikemommy-com.myshopify.com")
check("public domain identity", shop["primaryDomain"]["url"] == "https://www.dresslikemommy.com")
check("funnel shop matches", funnel["shopDomain"] == shop["myshopifyDomain"])
check("fixed window", "SINCE 2026-06-13 UNTIL 2026-09-10" in funnel["query"])
pagination_complete("complete market pagination", data["markets"])
pagination_complete("complete shared web presence pagination", presences)

market_rows = []
country_memberships = defaultdict(list)
markets = data["markets"]["nodes"]
for market in markets:
    code = market["handle"]
    condition = market["conditions"]["regionsCondition"]
    check(f"{code} is a specified regional market", market["type"] == "REGION" and condition["applicationLevel"] == "SPECIFIED")
    pagination_complete(f"{code} complete regions", condition["regions"])
    pagination_complete(f"{code} complete web presences", market["webPresences"])
    for region in condition["regions"]["nodes"]:
        check(f"{code}/{region['name']} is a country", region["__typename"] == "MarketRegionCountry")
        row = {
            "market_id": market["id"], "market_handle": code,
            "market_name": market["name"], "market_status": market["status"],
            "country_code": region["code"], "country_name": region["name"],
            "region_id": region["id"], "country_currency": region["currency"]["currencyCode"],
            "country_currency_enabled": region["currency"]["enabled"],
            "market_base_currency": market["currencySettings"]["baseCurrency"]["currencyCode"],
            "local_currencies_enabled": market["currencySettings"]["localCurrencies"],
            "rounding_enabled": market["currencySettings"]["roundingEnabled"],
            "google_targeted": "UNKNOWN", "merchant_approved": "UNKNOWN",
            "public_buying_acceptance": "NOT_RUN", "product_sellability": "UNKNOWN",
        }
        market_rows.append(row)
        if market["status"] == "ACTIVE":
            country_memberships[region["code"]].append(row)

countries = []
for code, memberships in sorted(country_memberships.items()):
    currencies = sorted({r["country_currency"] for r in memberships})
    names = sorted({r["country_name"] for r in memberships})
    check(f"{code} membership names agree", len(names) == 1)
    check(f"{code} membership currencies agree", len(currencies) == 1)
    check(f"{code} country currency is enabled", all(r["country_currency_enabled"] for r in memberships))
    check(f"{code} currency in shop presentment list", currencies[0] in shop["enabledPresentmentCurrencies"])
    countries.append({
        "country_code": code, "country_name": names[0],
        "market_ids": [r["market_id"] for r in memberships],
        "market_handles": [r["market_handle"] for r in memberships],
        "membership_count": len(memberships), "configured_currency": currencies[0],
        "overlapping_conditions": len(memberships) > 1,
        "runtime_market_resolution": "NOT_RUN", "google_targeted": "UNKNOWN",
        "merchant_approved": "UNKNOWN", "product_sellability": "UNKNOWN",
        "shipping_and_checkout_acceptance": "NOT_RUN",
    })

country_names = {canonical_name(r["country_name"]): r for r in countries}
check("country names uniquely join", len(country_names) == len(countries))
locales = data["shopLocales"]
check("locale codes unique", len({r["locale"] for r in locales}) == len(locales))
presence_ids = {p["id"] for p in presences["nodes"]}
routes = []
for presence in presences["nodes"]:
    pagination_complete(f"{presence['id']} complete market association pagination", presence["markets"])
    allowed = {r["locale"] for r in [presence["defaultLocale"], *presence["alternateLocales"]] if r["published"]}
    check("root URLs cover published presence locales", {r["locale"] for r in presence["rootUrls"]} == allowed)
    for route in presence["rootUrls"]:
        routes.append({"locale": route["locale"], "root_url": route["url"], "web_presence_id": presence["id"], "source": "LIVE_SHOPIFY_CONFIGURATION", "render_and_translation_acceptance": "NOT_RUN"})
for locale in locales:
    check(f"{locale['locale']} presence reference resolves", all(p["id"] in presence_ids for p in locale["marketWebPresences"]))
check("all published locales have a root", {r["locale"] for r in locales if r["published"]} == {r["locale"] for r in routes})
check("shared presence route model applies", len(presences["nodes"]) == 1 and all(not m["webPresences"]["nodes"] for m in markets))

columns = [c["name"] for c in funnel["columns"]]
check("all funnel rows have correct shape", all(len(r) == len(columns) for r in funnel["rows"]))
check("funnel rowCount equals rows", funnel["rowCount"] == len(funnel["rows"]))
check("funnel below requested limit", funnel["rowCount"] < 1000)
metrics = ["sessions", "sessions_with_cart_additions", "sessions_that_reached_checkout", "sessions_that_completed_checkout"]
funnel_rows = []
for raw in funnel["rows"]:
    row = dict(zip(columns, raw))
    country = country_names.get(canonical_name(row["session_country"]))
    normalized = {"session_country": row["session_country"], "country_code": country["country_code"] if country else "", "current_active_market_name_match": bool(country), "current_market_handles": "|".join(country["market_handles"]) if country else ""}
    for metric in metrics:
        normalized[metric] = int(row[metric])
    normalized["conversion_rate_fraction"] = float(row["conversion_rate"])
    check(f"{row['session_country']} rate math", math.isclose(normalized["conversion_rate_fraction"], normalized["sessions_that_completed_checkout"] / normalized["sessions"], rel_tol=1e-10, abs_tol=1e-12))
    normalized["window_start"] = "2026-06-13"
    normalized["window_end"] = "2026-09-10"
    normalized["paid_attribution"] = "UNKNOWN"
    funnel_rows.append(normalized)

check("funnel countries unique", len({r["session_country"] for r in funnel_rows}) == len(funnel_rows))
totals = {m: sum(r[m] for r in funnel_rows) for m in metrics}
for metric in metrics:
    supplied = {dict(zip(columns, r))[f"{metric}__totals"] for r in funnel["rows"]}
    check(f"{metric} reconciles provider totals", supplied == {str(totals[metric])})
overall_rate = totals["sessions_that_completed_checkout"] / totals["sessions"]
check("aggregate rate reconciles", all(math.isclose(float(dict(zip(columns, r))["conversion_rate__totals"]), overall_rate, rel_tol=1e-10) for r in funnel["rows"]))
grouped_funnel = {}
for label, member in [("current_active_country_name_match", True), ("no_exact_current_active_country_name_match", False)]:
    included = [r for r in funnel_rows if r["current_active_market_name_match"] is member]
    grouped_funnel[label] = {"country_rows": len(included), **{m: sum(r[m] for r in included) for m in metrics}}

source_files = ["provider_markets_response.json", "provider_web_presences_response.json", "provider_country_funnel_response.json", "query.graphql", "query_web_presences.graphql", "capture_metadata.json"]
source_hashes = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in source_files}
sales_path = BASE.parents[2] / "2026-09-11-google-ads-cold-start-research/EVIDENCE.json"
sales_receipt = json.loads(sales_path.read_text())
sales_report = sales_receipt["shopify_analytics"][0]
check("reused sales report has same fixed window", "SINCE 2026-06-13 UNTIL 2026-09-10" in sales_report["query"])
check("reused sales report has same shop", sales_report["shopDomain"] == shop["myshopifyDomain"])
sales_metrics = dict(zip([c["name"] for c in sales_report["columns"]], sales_report["rows"][0]))
sales_source = os.path.relpath(sales_path, BASE)
source_hashes[sales_source] = hashlib.sha256(sales_path.read_bytes()).hexdigest()
counts = {
    "markets": len(markets), "active_markets": sum(m["status"] == "ACTIVE" for m in markets),
    "country_assignments": len(market_rows), "unique_active_countries": len(countries),
    "countries_with_overlapping_conditions": sum(c["overlapping_conditions"] for c in countries),
    "published_locales": sum(l["published"] for l in locales),
    "enabled_presentment_currencies": len(shop["enabledPresentmentCurrencies"]),
    "shared_web_presences": len(presences["nodes"]), "shared_locale_roots": len(routes),
    "country_locale_qa_candidates": len(countries) * len(routes),
}
limitations = [
    "ACTIVE market is configuration only; it does not prove shipping, current product sellability, payment success or public buyer acceptance.",
    "Published locale and root URL do not prove complete, correct or native-reviewed product translations.",
    "Country-locale QA candidates are the derived Cartesian test scope using shared presence configuration, not independently verified market-language assignments or a paid targeting plan.",
    "AU, CA and GB occur in two market condition sets. Exact public market selection was not tested; do not double-count countries or remove overlaps without understanding resolution.",
    "Shared presence has no direct market associations returned. Schema documents primary-domain country-selector fallback when a market has no separate presence; runtime acceptance is still NOT_RUN.",
    "Country currencies describe current Shopify settings, not proof of Google conversion currency/value correctness.",
    "Country funnel is all-channel session data for 90 complete shop-local dates, not paid purchases, incremental sales, transaction-level receipt or revenue.",
    "Current market membership is joined to a historical funnel by exact normalized country name. Unmatched names are flagged explicitly; historical membership and possible aliases were not established.",
    "No device/referrer segmentation in this bounded query. Traffic outside configured markets may include noncommercial or automated sessions; it is not proof of paid waste.",
    "Google campaign targeting, Merchant offer approval, paid spend, CPA, ROAS and retained profit remain UNKNOWN in this inventory.",
]
readback = {
    "artifact_type": "GENERATED_EVIDENCE_NOT_AUTHORITY", "status": "LIVE_CONFIGURATION_VERIFIED__BUYER_AND_PAID_ACCEPTANCE_OPEN",
    "captured": {k: meta[k] for k in ["market_inventory", "web_presences", "country_funnel"]},
    "shop": shop, "counts": counts, "markets": markets, "active_countries": countries,
    "shop_locales": locales, "shared_web_presences": presences["nodes"], "locale_roots": routes,
    "country_funnel": {"source": "provider_country_funnel_response.json", "query": funnel["query"], "window": {"start": "2026-06-13", "end": "2026-09-10", "dates": 90, "timezone": shop["ianaTimezone"], "partial_dates": False}, "row_count": len(funnel_rows), "totals": totals, "conversion_rate_fraction": overall_rate, "current_membership_join": grouped_funnel},
    "reused_sales_context": {"source": sales_source, "source_checked_clock_utc": sales_receipt["checked_clock_utc"], "window_start": "2026-06-13", "window_end": "2026-09-10", "orders_reported": int(sales_metrics["orders"]), "net_sales_usd": float(sales_metrics["net_sales"]), "total_sales_usd": float(sales_metrics["total_sales"]), "source_level": "REPO_KNOWN_SAME_DAY_CONNECTOR_READBACK_NOT_REFETCHED", "limit": "Separate all-channel sales aggregate; not a current paid/order-level reconciliation. The completed-checkout session count and reported order count use different metric scopes and must not be treated as a tracking mismatch by subtraction."},
    "recommendation": "Reconcile exact live Google location and language scope to the65country inventory and select a narrowly qualified first cohort. Prioritize US buyer and measurement acceptance by observed volume; investigate Romania/Netherlands checkout progression before expansion. Do not scale country cohorts from tiny conversion-rate samples.",
    "limitations": limitations, "source_sha256": source_hashes,
}
write_json("market_readback.json", readback)
write_csv("market_country_assignments.csv", sorted(market_rows, key=lambda r: (r["market_handle"], r["country_code"])))
country_csv = [{**r, "market_ids": "|".join(r["market_ids"]), "market_handles": "|".join(r["market_handles"])} for r in countries]
write_csv("active_country_inventory.csv", country_csv)
write_csv("locale_routes.csv", sorted(routes, key=lambda r: r["locale"]))
write_csv("country_funnel.csv", funnel_rows)
qa_rows = [{"country_code": c["country_code"], "country_name": c["country_name"], "market_handles": "|".join(c["market_handles"]), "configured_currency": c["configured_currency"], "locale": r["locale"], "configured_shared_root_url": r["root_url"], "scope_basis": "DERIVED_SHARED_PRESENCE_QA_CANDIDATE", "country_context_selection": "REQUIRED_NOT_TESTED", "public_translation_quality": "NOT_RUN", "product_and_shipping_sellability": "NOT_RUN", "conversion_value_currency_acceptance": "NOT_RUN", "google_campaign_targeting": "UNKNOWN", "merchant_approval": "UNKNOWN"} for c in countries for r in routes]
write_csv("country_locale_qa_matrix.csv", qa_rows)
check("QA matrix unique country-locale pairs", len({(r["country_code"], r["locale"]) for r in qa_rows}) == len(qa_rows))
write_json("VALIDATION.json", {"status": "PASS", "checks_passed": len(CHECKS), "checks": CHECKS, "source_sha256": source_hashes, "external_writes": 0, "scope": "Local data integrity and complete configuration/report pagination; no browser, buyer or paid acceptance claim."})
print(json.dumps({"counts": counts, "funnel_totals": totals, "funnel_current_country_match": grouped_funnel, "validation_checks": len(CHECKS)}, indent=2))
