"""Normalize the preserved shipping readback locally. This script makes no requests."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
MARKETS = HERE / "../markets/market_readback.json"
PRIOR = HERE / "../../../2026-09-09-merchant-expert-audit/market_inventory.json"
checks = []


def check(name, condition, detail):
    checks.append({"name": name, "result": "PASS" if condition else "FAIL", "detail": detail})
    if not condition:
        raise ValueError(f"{name}: {detail}")


def read(path):
    return json.loads(path.read_text())


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def connection_nodes(connection, name):
    check(f"complete_pagination:{name}", connection["pageInfo"]["hasNextPage"] is False,
          f"{len(connection['nodes'])} returned nodes; hasNextPage=false required")
    return connection["nodes"]


def prior_comparable(profiles):
    """Compare only the fields returned in both dated sources; discard cursors/order."""
    output = []
    for profile in profiles:
        groups = []
        for group in profile["profileLocationGroups"]:
            zones = []
            for entry in group["locationGroupZones"]["nodes"]:
                countries = [{"code": c["code"], "provinces": sorted(p["code"] for p in c["provinces"])}
                             for c in entry["zone"]["countries"]]
                methods = []
                for method in entry["methodDefinitions"]["nodes"]:
                    methods.append({key: method[key] for key in
                                    ["id", "name", "active", "rateProvider", "methodConditions"]})
                zones.append({"id": entry["zone"]["id"], "name": entry["zone"]["name"],
                              "countries": sorted(countries, key=lambda c: c["code"]["countryCode"] or ""),
                              "methods": sorted(methods, key=lambda m: m["id"])})
            groups.append({"id": group["locationGroup"]["id"], "zones": sorted(zones, key=lambda z: z["id"])})
        output.append({"id": profile["id"], "name": profile["name"], "default": profile["default"],
                       "groups": sorted(groups, key=lambda g: g["id"])})
    return sorted(output, key=lambda p: p["id"])


raw = read(HERE / "provider_response.json")
metadata = read(HERE / "capture_metadata.json")
market = read(MARKETS)
prior = read(PRIOR)["observations"]["shipping"]
source_hashes = {"provider_response.json": digest(HERE / "provider_response.json"),
                 "capture_metadata.json": digest(HERE / "capture_metadata.json"),
                 "query.graphql": digest(HERE / "query.graphql"),
                 "../markets/market_readback.json": digest(MARKETS),
                 "../../../2026-09-09-merchant-expert-audit/market_inventory.json": digest(PRIOR)}
check("provider_success", raw.get("isError") is False and not raw["structuredContent"].get("errors"),
      "Structured connector returned data without a tool or GraphQL error")
data = raw["structuredContent"]["data"]
check("shop_identity", data["shop"]["id"] == market["shop"]["id"] == "gid://shopify/Shop/15571635"
      and data["shop"]["myshopifyDomain"] == market["shop"]["myshopifyDomain"],
      "Fresh shipping and same-session market sources identify the same shop")
profiles = connection_nodes(data["deliveryProfiles"], "deliveryProfiles")
check("one_default_profile", len(profiles) == 1 and profiles[0]["default"],
      "Exactly one profile returned; it is the default profile")
profile = profiles[0]
zones, rates = [], []
for group in profile["profileLocationGroups"]:
    entries = connection_nodes(group["locationGroupZones"], group["locationGroup"]["id"])
    for entry in entries:
        methods = connection_nodes(entry["methodDefinitions"], entry["zone"]["id"])
        zones.append({"profile_id": profile["id"], "location_group_id": group["locationGroup"]["id"],
                      **entry["zone"], "methods": methods})
        for method in methods:
            provider = method["rateProvider"]
            price = provider.get("price", {})
            rates.append({"profile_id": profile["id"], "zone_id": entry["zone"]["id"],
                          "zone_name": entry["zone"]["name"], "method_id": method["id"],
                          "method_name": method["name"], "active": method["active"],
                          "provider_type": provider["__typename"],
                          "rate_class": "STATIC" if provider["__typename"] == "DeliveryRateDefinition" else "DYNAMIC_OR_OTHER",
                          "base_amount": price.get("amount", "UNKNOWN"),
                          "base_currency": price.get("currencyCode", "UNKNOWN"),
                          "description": method["description"],
                          "conditions_json": json.dumps(method["methodConditions"], sort_keys=True),
                          "numeric_delivery_time": "NOT_EXPOSED_IN_QUERIED_SCHEMA",
                          "actual_checkout_acceptance": "NOT_RUN"})
check("methods_reconcile", sum(r["active"] for r in rates) == profile["activeMethodDefinitionsCount"] == 4,
      "Four returned active method definitions equal profile activeMethodDefinitionsCount")
check("static_rates", all(r["provider_type"] == "DeliveryRateDefinition" for r in rates),
      "All returned providers are static rates; no carrier calculation was requested or tested")

product = data["product"]
variants = connection_nodes(product["variants"], product["id"] + "/variants")
assigned = [v for v in variants if v["deliveryProfile"] and v["deliveryProfile"]["id"] == profile["id"]]
check("bounded_product_assignment", len(variants) == len(assigned) == len({v['id'] for v in variants}) == 98,
      "All 98 unique variants returned for Together Heart link to this profile; no other product was sampled")

countries = market["active_countries"]
check("active_country_inventory", len(countries) == len({c['country_code'] for c in countries}) == 65,
      "Complete same-session active-country inventory supplies exactly 65 unique rows")
ships_to = set(data["shop"]["shipsToCountries"])
explicit_zones = {}
rest_zones = []
for zone in zones:
    for country in zone["countries"]:
        if country["code"]["restOfWorld"]:
            rest_zones.append(zone)
        else:
            explicit_zones.setdefault(country["code"]["countryCode"], []).append((zone, country))
rows = []
expected_weight_conditions = {
    ("TOTAL_WEIGHT", "GREATER_THAN_OR_EQUAL_TO", "Weight", 0, "POUNDS"),
    ("TOTAL_WEIGHT", "LESS_THAN_OR_EQUAL_TO", "Weight", 5, "POUNDS"),
}
for country in countries:
    code = country["country_code"]
    candidates = explicit_zones.get(code, [])
    basis = "EXPLICIT_COUNTRY" if candidates else "REST_OF_WORLD_FALLBACK"
    options = [z for z, _ in candidates] if candidates else rest_zones
    check(f"unambiguous_country_mapping:{code}", len(options) == 1,
          "Exactly one applicable country-level zone in the sole returned profile")
    zone = options[0]
    standard = [m for m in zone["methods"] if m["name"] == "Free Standard Shipping" and m["active"]]
    priority = [m for m in zone["methods"] if m["name"] == "Priority Shipping" and m["active"]]
    check(f"unconditional_standard:{code}", len(standard) == 1 and not standard[0]["methodConditions"]
          and standard[0]["rateProvider"]["price"] == {"amount": "0.0", "currencyCode": "USD"},
          "One active static USD 0 standard rate with no returned method conditions")
    check(f"priority_conditions:{code}", len(priority) == 1 and {
        (c["field"], c["operator"], c["conditionCriteria"]["__typename"],
         c["conditionCriteria"].get("value"), c["conditionCriteria"].get("unit"))
        for c in priority[0]["methodConditions"]} == expected_weight_conditions
        and priority[0]["rateProvider"]["price"] == {"amount": "12.99", "currencyCode": "USD"},
        "One active USD 12.99 priority rate with inclusive 0–5 POUNDS total weight bounds")
    provinces = sorted(p["code"] for p in candidates[0][1]["provinces"]) if candidates else []
    rows.append({"country_code": code, "country_name": country["country_name"],
                 "market_ids": "|".join(country["market_ids"]),
                 "market_handles": "|".join(country["market_handles"]),
                 "market_configured_currency": country["configured_currency"],
                 "profile_id": profile["id"], "zone_id": zone["id"], "zone_name": zone["name"],
                 "configured_zone_mapping": "PRESENT", "coverage_basis": basis,
                 "shop_ships_to_countries_contains_code": code in ships_to,
                 "explicit_province_codes_count": len(provinces), "explicit_province_codes": "|".join(provinces),
                 "province_address_acceptance": "NOT_RUN",
                 "standard_base_amount": "0.0", "standard_base_currency": "USD",
                 "standard_method_conditions": "NONE_RETURNED",
                 "priority_base_amount": "12.99", "priority_base_currency": "USD",
                 "priority_weight_min_inclusive": 0, "priority_weight_max_inclusive": 5,
                 "priority_weight_unit": "POUNDS", "order_price_conditions": "NONE_RETURNED",
                 "dynamic_rate_providers_in_applicable_zone": 0,
                 "checkout_presentment_rate_and_currency": "NOT_RUN",
                 "actual_checkout_acceptance": "NOT_RUN", "numeric_delivery_time": "UNKNOWN",
                 "sampled_product_variant_profile_assignment": "98_OF_98_TOGETHER_HEART_ONLY",
                 "merchant_shipping_import": "UNKNOWN", "google_targeted": "UNKNOWN"})
check("shop_country_confirmation", all(r["shop_ships_to_countries_contains_code"] for r in rows),
      "All 65 active country codes are independently present in shop.shipsToCountries")
bases = Counter(r["coverage_basis"] for r in rows)
check("country_count_reconciliation", bases == {"EXPLICIT_COUNTRY": 7, "REST_OF_WORLD_FALLBACK": 58},
      "7 explicit active countries plus 58 Rest of world mappings equals 65")
comparison_equal = prior_comparable(profiles) == prior_comparable(prior["deliveryProfiles"]["nodes"])
check("prior_configuration_comparison", comparison_equal,
      "Names, IDs, countries, province codes, active flags, rate providers and conditions match Sep 9 source")

limitations = [
    "Country-level configuration mapping is derived from the explicit zone or Rest of world wildcard and confirmed by shop.shipsToCountries. It is not buyer checkout acceptance.",
    "Province filters are preserved exactly. No province/address completeness, payment, cart, checkout or customer tests were performed.",
    "Rate definitions use USD. Actual converted rates, checkout currency, rounding and market resolution were not read; Romania market currency is RON and Netherlands EUR.",
    "No carrier-calculated provider was returned in the complete profile read. This does not verify actual supplier fulfillment, carrier serviceability or delivery times.",
    "Rate descriptions are blank. The queried method/rate schema does not expose numeric transit times; absence here does not prove native shipping estimates are absent.",
    "General profile productVariantsCount is 500 with AT_LEAST precision, not an exact catalog count. Only Together Heart's 98 variants were explicitly mapped.",
    "originLocationCount=2 is technical configuration, not evidence of physical inventory or owned locations. No location/address fields were requested.",
    "shop.shipsToCountries has 237 unique codes; zoneCountryCount=244 is a distinct aggregate including wildcard semantics. Neither count means that many current active markets or tested checkouts.",
    "Existing market catalog exclusions remain a separate Merchant-owned finding from prior evidence, not a newly proved shipping defect. Google targeting and Merchant shipping import were not queried.",
    "No purchase, revenue, CPA, ROAS or contribution-profit conclusion follows from shipping configuration. No broad sales queries were repeated.",
]
normalized = {
    "artifact_type": "GENERATED_EVIDENCE_NOT_AUTHORITY", "status": "LIVE_CONFIGURATION_VERIFIED__CHECKOUT_ACCEPTANCE_OPEN",
    "captured": metadata["captured"], "source": metadata["source"],
    "shop": data["shop"], "market_source": "../markets/market_readback.json",
    "market_source_captured": market["captured"]["market_inventory"],
    "counts": {"delivery_profiles": len(profiles), "location_groups": len(profile["profileLocationGroups"]),
               "zones": len(zones), "active_static_rates": sum(r["active"] for r in rates),
               "dynamic_rate_providers_returned": 0, "active_countries": len(rows),
               "explicit_active_country_mappings": bases["EXPLICIT_COUNTRY"],
               "rest_of_world_active_country_mappings": bases["REST_OF_WORLD_FALLBACK"],
               "active_countries_missing_configured_zone_or_shop_shipping_code": 0,
               "shop_ships_to_countries_unique_codes": len(ships_to),
               "sampled_product_variants": len(variants), "sampled_variants_assigned_to_profile": len(assigned)},
    "profile_metadata": {k: v for k, v in profile.items() if k != "profileLocationGroups"},
    "zones": zones, "country_coverage": rows,
    "product_assignment_sample": {"id": product["id"], "handle": product["handle"], "status": product["status"],
                                  "variants": variants, "complete": True, "catalog_generalization": "NOT_SUPPORTED"},
    "comparison": {"prior_source": str(PRIOR.relative_to(HERE)), "prior_observed_at": prior["observedAt"],
                   "common_shipping_fields_equal": comparison_equal,
                   "excluded_from_comparison": ["newly queried metadata", "cursors", "descriptions", "product assignment"]},
    "findings": [{"severity": "NONE_PROVEN", "scope": "active-country static rate configuration",
                  "conclusion": "No missing country-level rate or conflicting price/weight rule was demonstrated.",
                  "decision": "NO_SHIPPING_CONFIGURATION_REPAIR_JUSTIFIED"},
                 {"severity": "LIMITATION", "scope": "RO and NL checkout drop-off",
                  "conclusion": "Both map to Rest of world and its active rates. This read does not identify a shipping-configuration cause for zero completed checkouts.",
                  "decision": "Continue existing localized buyer-route and measurement work; keep live checkout acceptance separately gated."}],
    "limitations": limitations, "source_sha256": source_hashes,
    "official_documentation": [
        "https://shopify.dev/docs/api/admin-graphql/2026-07/objects/DeliveryProfile",
        "https://shopify.dev/docs/apps/build/purchase-options/deferred/delivery-and-deferment/build-delivery-profiles"],
    "external_writes": 0, "public_http_requests": 0, "browser_actions": 0,
}
write("shipping_coverage.json", normalized)
write_csv("country_shipping_coverage.csv", rows)
write_csv("rates.csv", rates)
check("retained_source_hashes", all(digest(HERE / path) == expected for path, expected in source_hashes.items()),
      "All input sources retain their original SHA-256 hashes")
with (HERE / "country_shipping_coverage.csv").open(newline="") as handle:
    roundtrip = list(csv.DictReader(handle))
check("country_csv_roundtrip", len(roundtrip) == 65 and {r["country_code"] for r in roundtrip} == {r["country_code"] for r in rows},
      "65 unique countries survive CSV serialization with exact inventory membership")
write("VALIDATION.json", {"status": "PASS", "method": "Offline normalization of preserved structured sources; no network calls",
                          "scope": "Data integrity, pagination, join, source comparison and serialization; not buyer acceptance",
                          "checks_count": len(checks), "checks": checks})
print(json.dumps({"status": "PASS", "checks": len(checks), "counts": normalized["counts"]}, sort_keys=True))
