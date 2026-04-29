#!/usr/bin/env python3
"""Build a read-only Phase 5 country/admin/checkout validation packet.

This script intentionally does not modify Shopify Admin, Google Ads, Merchant
Center, markets, shipping, policies, products, or theme files. The storefront
checkout probe uses an anonymous cart session and stops at shipping-rate lookup;
it never submits payment.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib import error, parse, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain
from ops.scripts.sync_shopify_variant_costs import API_VERSION, ShopifyClient


DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-country-checkout-admin-validation"
)
DEFAULT_STOREFRONT = "https://www.dresslikemommy.com"
DEFAULT_PAID_COHORT = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv"
)
DEFAULT_COUNTRY_EXCLUSIONS = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-merchant-diagnostics-priority-triage/"
    "shopping_ads_us_only_country_exclusions_UPLOAD_APPROVED.csv"
)

CHECKOUT_ADDRESSES = {
    "US": {
        "country": "United States",
        "province": "California",
        "zip": "90210",
        "city": "Beverly Hills",
    },
    "GB": {
        "country": "United Kingdom",
        "province": "",
        "zip": "SW1A 1AA",
        "city": "London",
    },
    "CA": {
        "country": "Canada",
        "province": "Ontario",
        "zip": "M5V 2T6",
        "city": "Toronto",
    },
    "AU": {
        "country": "Australia",
        "province": "New South Wales",
        "zip": "2000",
        "city": "Sydney",
    },
    "UA": {
        "country": "Ukraine",
        "province": "Kyiv",
        "zip": "01001",
        "city": "Kyiv",
    },
}

MARKETS_QUERY = """
query MarketsReadback($after: String) {
  markets(first: 50, after: $after) {
    nodes {
      id
      name
      handle
      enabled
      currencySettings { baseCurrency { currencyCode } }
      regions(first: 250) {
        nodes {
          __typename
          ... on MarketRegionCountry { code name }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

LOCALES_QUERY = """
query LocaleReadback {
  shopLocales {
    locale
    name
    primary
    published
  }
}
"""

DELIVERY_PROFILES_QUERY = """
query DeliveryReadback {
  deliveryProfiles(first: 25) {
    nodes {
      id
      name
      profileLocationGroups {
        locationGroupZones(first: 100) {
          nodes {
            zone {
              id
              name
              countries {
                name
                code { countryCode restOfWorld }
              }
            }
            methodDefinitions(first: 25) {
              nodes {
                id
                name
                active
                rateProvider {
                  __typename
                  ... on DeliveryRateDefinition {
                    price { amount currencyCode }
                  }
                  ... on DeliveryParticipant {
                    fixedFee { amount currencyCode }
                    percentageOfRateFee
                  }
                }
              }
            }
          }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
  }
}
"""


def utcish_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def admin_rest_get(store_domain: str, access_token: str, path: str) -> dict[str, Any]:
    url = f"https://{store_domain}/admin/api/{API_VERSION}/{path.lstrip('/')}"
    req = request.Request(
        url,
        headers={
            "Accept": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
    )
    with request.urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_markets(client: ShopifyClient) -> list[dict[str, Any]]:
    markets: list[dict[str, Any]] = []
    after = None
    while True:
        data = client.graphql(MARKETS_QUERY, {"after": after})
        page = data["markets"]
        markets.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return markets


def fetch_delivery_profiles(client: ShopifyClient) -> list[dict[str, Any]]:
    data = client.graphql(DELIVERY_PROFILES_QUERY)
    return data["deliveryProfiles"]["nodes"]


def fetch_locales(client: ShopifyClient) -> list[dict[str, Any]]:
    return client.graphql(LOCALES_QUERY)["shopLocales"]


def fetch_policies(store_domain: str, access_token: str) -> list[dict[str, Any]]:
    data = admin_rest_get(store_domain, access_token, "policies.json")
    policies = []
    for policy in data.get("policies", []):
        body = policy.get("body") or ""
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        text = clean(text)
        policies.append(
            {
                "handle": policy.get("handle"),
                "title": policy.get("title"),
                "url": policy.get("url"),
                "updated_at": policy.get("updated_at"),
                "body_length": len(body),
                "plain_text_excerpt": text[:700],
                "has_shipping_language": "shipping" in text.lower(),
                "has_return_language": any(token in text.lower() for token in ("return", "refund")),
            }
        )
    return policies


def paid_country_evidence(
    paid_cohort_path: Path,
    country_exclusions_path: Path,
) -> dict[str, Any]:
    paid_rows = read_csv(paid_cohort_path)
    paid_markets: dict[str, int] = defaultdict(int)
    non_us_paid_rows = []
    for row in paid_rows:
        item_id = clean(row.get("merchant_center_item_id") or row.get("id"))
        match = re.search(r"\bshopify_([A-Z]{2})_\d+_\d+\b", item_id)
        market = match.group(1) if match else clean(row.get("market") or row.get("country") or "UNKNOWN")
        paid_markets[market] += 1
        if market != "US":
            non_us_paid_rows.append(item_id or row)

    exclusion_rows = read_csv(country_exclusions_path)
    excluded_countries: set[str] = set()
    us_exclusion_rows = []
    for row in exclusion_rows:
        countries = [
            value.strip().upper()
            for value in clean(row.get("shopping_ads_excluded_country")).split(",")
            if value.strip()
        ]
        excluded_countries.update(countries)
        if "US" in countries:
            us_exclusion_rows.append(row.get("id"))

    return {
        "policy": "US_ONLY_PAID_TRAFFIC",
        "intentional_allowlist_expansion": False,
        "non_us_expansion_rule": (
            "Exclude every non-US country from paid until localization, shipping, "
            "returns, country conversion, and margin pass."
        ),
        "paid_cohort_path": str(paid_cohort_path),
        "paid_cohort_rows": len(paid_rows),
        "paid_cohort_markets": dict(sorted(paid_markets.items())),
        "non_us_paid_rows": len(non_us_paid_rows),
        "country_exclusions_path": str(country_exclusions_path),
        "country_exclusion_rows": len(exclusion_rows),
        "excluded_country_count": len(excluded_countries),
        "excluded_countries": sorted(excluded_countries),
        "us_exclusion_rows": len(us_exclusion_rows),
        "us_exclusion_examples": us_exclusion_rows[:20],
        "paid_gate_status": (
            "PASS_US_ONLY" if not non_us_paid_rows and not us_exclusion_rows else "FAIL_REVIEW_REQUIRED"
        ),
    }


def country_maps(
    markets: list[dict[str, Any]],
    delivery_profiles: list[dict[str, Any]],
) -> tuple[
    dict[str, str],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    bool,
]:
    names: dict[str, str] = {}
    market_by_country: dict[str, list[dict[str, Any]]] = defaultdict(list)
    shipping_by_country: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rest_of_world_shipping = False

    for market in markets:
        currency = (
            (market.get("currencySettings") or {}).get("baseCurrency") or {}
        ).get("currencyCode")
        for region in ((market.get("regions") or {}).get("nodes") or []):
            code = clean(region.get("code")).upper()
            if not code:
                continue
            names.setdefault(code, clean(region.get("name")))
            market_by_country[code].append(
                {
                    "market": market.get("name"),
                    "handle": market.get("handle"),
                    "enabled": bool(market.get("enabled")),
                    "currency": currency,
                }
            )

    for profile in delivery_profiles:
        for group in profile.get("profileLocationGroups") or []:
            zones = ((group.get("locationGroupZones") or {}).get("nodes") or [])
            for zone_node in zones:
                zone = zone_node.get("zone") or {}
                methods = []
                for method in ((zone_node.get("methodDefinitions") or {}).get("nodes") or []):
                    rate_provider = method.get("rateProvider") or {}
                    price = rate_provider.get("price") or rate_provider.get("fixedFee") or {}
                    methods.append(
                        {
                            "name": method.get("name"),
                            "active": bool(method.get("active")),
                            "provider_type": rate_provider.get("__typename"),
                            "price": price.get("amount"),
                            "currency": price.get("currencyCode"),
                        }
                    )
                for country in zone.get("countries") or []:
                    code_obj = country.get("code") or {}
                    if code_obj.get("restOfWorld"):
                        rest_of_world_shipping = True
                        continue
                    code = clean(code_obj.get("countryCode")).upper()
                    if not code:
                        continue
                    names.setdefault(code, clean(country.get("name")))
                    shipping_by_country[code].append(
                        {
                            "profile": profile.get("name"),
                            "zone": zone.get("name"),
                            "methods": methods,
                        }
                    )
    return names, market_by_country, shipping_by_country, rest_of_world_shipping


def find_checkout_variant(paid_cohort_path: Path) -> tuple[str, dict[str, str]]:
    for row in read_csv(paid_cohort_path):
        variant_id = clean(row.get("shopify_variant_id") or row.get("variant_id"))
        if variant_id:
            return variant_id, row
    raise RuntimeError(f"No Shopify variant ID found in {paid_cohort_path}")


def storefront_request(
    opener: request.OpenerDirector,
    url: str,
    *,
    data: dict[str, str] | None = None,
    timeout: int = 60,
) -> tuple[int, str, str]:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "DressLikeMommyOps/1.0 (+read-only checkout validation)",
    }
    payload = parse.urlencode(data or {}).encode("utf-8") if data is not None else None
    req = request.Request(
        url,
        data=payload,
        method="POST" if data is not None else "GET",
        headers=headers,
    )
    try:
        with opener.open(req, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="replace"), ""
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        blocker = ""
        if exc.code == 429 or "Verifying your connection" in body:
            blocker = "SHOPIFY_STOREFRONT_BOT_PROTECTION_429"
        return exc.code, body, blocker


def init_checkout_cart(
    opener: request.OpenerDirector,
    storefront_base_url: str,
    variant_id: str,
) -> tuple[bool, list[dict[str, Any]]]:
    evidence = []
    for endpoint, data in (
        ("/cart/clear.js", {}),
        ("/cart/add.js", {"id": variant_id, "quantity": "1"}),
    ):
        url = storefront_base_url.rstrip("/") + endpoint
        status, body, blocker = storefront_request(opener, url, data=data)
        evidence.append(
            {
                "endpoint": endpoint,
                "http_status": status,
                "blocker": blocker,
                "body_excerpt": body[:500],
            }
        )
        if blocker or status >= 400:
            return False, evidence
        time.sleep(2)
    return True, evidence


def rate_result_from_body(code: str, address: dict[str, str], status: int, body: str, blocker: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "country_code": code,
        "address": address,
        "validation_level": "LIVE_CART_SHIPPING_RATES_NO_PAYMENT",
        "http_status": status,
        "blocker": blocker,
        "rates": [],
        "status": "BLOCKED" if blocker else "FAILED",
        "rate_class": "NO_RATES",
        "body_excerpt": body[:800],
    }
    if blocker or status >= 400:
        return result
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        result["status"] = "FAILED_NON_JSON"
        return result
    rates = data.get("shipping_rates") or []
    result["rates"] = [
        {
            "name": rate.get("name"),
            "price": rate.get("price"),
            "currency": rate.get("currency"),
            "source": rate.get("source"),
        }
        for rate in rates
    ]
    if rates:
        prices = []
        for rate in rates:
            try:
                prices.append(float(rate.get("price") or 0))
            except (TypeError, ValueError):
                pass
        result["status"] = "RATES_AVAILABLE"
        result["rate_class"] = "FREE_AND_PAID" if any(price == 0 for price in prices) else "PAID_ONLY"
    else:
        result["status"] = "NO_RATES_RETURNED"
    return result


def live_checkout_rate_checks(
    storefront_base_url: str,
    paid_cohort_path: Path,
    checkout_country_codes: list[str],
    delay_seconds: float,
) -> dict[str, Any]:
    variant_id, variant_row = find_checkout_variant(paid_cohort_path)
    opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))
    cart_ok, cart_evidence = init_checkout_cart(opener, storefront_base_url, variant_id)

    results: list[dict[str, Any]] = []
    if not cart_ok:
        blocker = next((entry["blocker"] for entry in cart_evidence if entry.get("blocker")), "CART_INIT_FAILED")
        for code in checkout_country_codes:
            results.append(
                {
                    "country_code": code,
                    "address": CHECKOUT_ADDRESSES.get(code, {"country": code}),
                    "validation_level": "LIVE_CART_SHIPPING_RATES_NO_PAYMENT",
                    "http_status": "",
                    "blocker": blocker,
                    "rates": [],
                    "status": "BLOCKED",
                    "rate_class": "NO_RATES",
                    "body_excerpt": "Cart initialization failed before shipping-rate lookup.",
                }
            )
        return {
            "status": "BLOCKED",
            "blocker": blocker,
            "variant_id": variant_id,
            "variant_product": {
                "product_title": variant_row.get("product_title"),
                "variant_title": variant_row.get("variant_title"),
                "product_url": variant_row.get("link") or variant_row.get("product_url"),
            },
            "cart_evidence": cart_evidence,
            "countries": results,
        }

    blocked = ""
    for index, code in enumerate(checkout_country_codes):
        address = CHECKOUT_ADDRESSES.get(code)
        if not address:
            results.append(
                {
                    "country_code": code,
                    "address": {"country": code},
                    "validation_level": "LIVE_CART_SHIPPING_RATES_NO_PAYMENT",
                    "http_status": "",
                    "blocker": "NO_TEST_ADDRESS_CONFIGURED",
                    "rates": [],
                    "status": "BLOCKED",
                    "rate_class": "NO_RATES",
                    "body_excerpt": "",
                }
            )
            continue
        if blocked:
            results.append(
                {
                    "country_code": code,
                    "address": address,
                    "validation_level": "LIVE_CART_SHIPPING_RATES_NO_PAYMENT",
                    "http_status": "",
                    "blocker": blocked,
                    "rates": [],
                    "status": "BLOCKED",
                    "rate_class": "NO_RATES",
                    "body_excerpt": "Skipped after prior storefront blocker.",
                }
            )
            continue
        if index:
            time.sleep(delay_seconds)
        params = {
            "shipping_address[country]": address["country"],
            "shipping_address[zip]": address.get("zip", ""),
        }
        if address.get("province"):
            params["shipping_address[province]"] = address["province"]
        url = storefront_base_url.rstrip() + "/cart/shipping_rates.json?" + parse.urlencode(params)
        status, body, blocker = storefront_request(opener, url)
        result = rate_result_from_body(code, address, status, body, blocker)
        results.append(result)
        if blocker:
            blocked = blocker

    return {
        "status": "COMPLETE" if not blocked else "BLOCKED_PARTIAL",
        "blocker": blocked,
        "variant_id": variant_id,
        "variant_product": {
            "product_title": variant_row.get("product_title"),
            "variant_title": variant_row.get("variant_title"),
            "product_url": variant_row.get("link") or variant_row.get("product_url"),
        },
        "cart_evidence": cart_evidence,
        "countries": results,
    }


def build_country_matrix(
    country_names: dict[str, str],
    market_by_country: dict[str, list[dict[str, Any]]],
    shipping_by_country: dict[str, list[dict[str, Any]]],
    rest_of_world_shipping: bool,
    paid_evidence: dict[str, Any],
    checkout_results: dict[str, Any],
    policies: list[dict[str, Any]],
    locales: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checkout_by_country = {
        row["country_code"]: row
        for row in checkout_results.get("countries", [])
        if row.get("country_code")
    }
    policy_handles = {policy.get("handle") for policy in policies}
    has_policy_admin_readback = bool(policies)
    published_locale_codes = sorted(locale["locale"] for locale in locales if locale.get("published"))

    all_codes = set(country_names) | set(market_by_country) | set(shipping_by_country)
    all_codes.update(paid_evidence.get("excluded_countries") or [])
    all_codes.update(checkout_by_country)
    all_codes.add("US")

    rows: list[dict[str, str]] = []
    for code in sorted(all_codes):
        markets = market_by_country.get(code, [])
        enabled_markets = [market for market in markets if market.get("enabled")]
        shipping_entries = shipping_by_country.get(code, [])
        checkout = checkout_by_country.get(code, {})
        currencies = sorted({clean(market.get("currency")) for market in markets if clean(market.get("currency"))})
        market_names = sorted({clean(market.get("market")) for market in markets if clean(market.get("market"))})
        shipping_methods = sorted(
            {
                clean(method.get("name"))
                for entry in shipping_entries
                for method in entry.get("methods", [])
                if method.get("active") and clean(method.get("name"))
            }
        )
        non_us = code != "US"
        rows.append(
            {
                "country_code": code,
                "country_name": country_names.get(code) or CHECKOUT_ADDRESSES.get(code, {}).get("country", ""),
                "market_enabled": "TRUE" if enabled_markets else "FALSE",
                "market_names": "; ".join(market_names),
                "market_currencies": "; ".join(currencies),
                "admin_shipping_configured": "TRUE" if shipping_entries or rest_of_world_shipping else "FALSE",
                "shipping_zones": "; ".join(
                    sorted({clean(entry.get("zone")) for entry in shipping_entries if clean(entry.get("zone"))})
                ),
                "shipping_methods": "; ".join(shipping_methods),
                "checkout_live_status": checkout.get("status", "NOT_RUN_THIS_PASS"),
                "checkout_live_rate_class": checkout.get("rate_class", ""),
                "checkout_live_blocker": checkout.get("blocker", ""),
                "checkout_rates": "; ".join(
                    f"{rate.get('name')} {rate.get('price')} {rate.get('currency')}"
                    for rate in checkout.get("rates", [])
                ),
                "localized_locale_evidence": ",".join(published_locale_codes),
                "policy_admin_evidence": (
                    "POLICIES_READ:" + ",".join(sorted(str(handle) for handle in policy_handles if handle))
                    if has_policy_admin_readback
                    else "POLICIES_NOT_READ"
                ),
                "localization_pass": "NOT_VALIDATED_COUNTRY_SPECIFIC" if non_us else "US_PRIMARY",
                "shipping_pass": (
                    "LIVE_RATE_PASS"
                    if checkout.get("status") == "RATES_AVAILABLE"
                    else ("ADMIN_CONFIGURED_ONLY" if shipping_entries or rest_of_world_shipping else "NO_ADMIN_SHIPPING")
                ),
                "returns_pass": "NOT_VALIDATED_COUNTRY_SPECIFIC" if non_us else "US_PRIMARY",
                "country_conversion_pass": "NOT_VALIDATED_COUNTRY_SPECIFIC" if non_us else "US_PRIMARY",
                "margin_pass": "NOT_VALIDATED_COUNTRY_SPECIFIC" if non_us else "US_PRIMARY",
                "paid_allowlist_decision": (
                    "EXCLUDE_FROM_PAID_UNTIL_ALL_PHASE5_GATES_PASS"
                    if non_us
                    else "US_ONLY_PRIMARY_PAID_MARKET"
                ),
            }
        )
    return rows


def build_report(
    *,
    output_dir: Path,
    paid_evidence: dict[str, Any],
    markets: list[dict[str, Any]],
    delivery_profiles: list[dict[str, Any]],
    locales: list[dict[str, Any]],
    policies: list[dict[str, Any]],
    checkout_results: dict[str, Any],
    matrix_rows: list[dict[str, str]],
) -> str:
    non_us_rows = [row for row in matrix_rows if row["country_code"] != "US"]
    active_non_us_markets = [
        row for row in non_us_rows if row["market_enabled"] == "TRUE"
    ]
    live_pass_rows = [
        row for row in non_us_rows if row["checkout_live_status"] == "RATES_AVAILABLE"
    ]
    blocked_rows = [
        row for row in non_us_rows if row["checkout_live_status"] == "BLOCKED"
    ]
    market_names = ", ".join(market.get("name", "") for market in markets)
    locale_codes = ", ".join(sorted(locale["locale"] for locale in locales if locale.get("published")))
    shipping_profiles = ", ".join(profile.get("name", "") for profile in delivery_profiles)
    policy_titles = ", ".join(policy.get("title", "") for policy in policies)

    lines = [
        "# Phase 5 Country Checkout/Admin Validation",
        "",
        f"Generated: {utcish_now()}",
        "",
        "## Decision",
        "",
        "- Paid traffic remains US-only.",
        "- No non-US country was added to the paid allowlist.",
        "- Non-US paid expansion remains blocked until localization, shipping, returns, country conversion, and margin pass country by country.",
        "",
        "## Admin Readback",
        "",
        f"- Markets read: {len(markets)} ({market_names})",
        f"- Delivery profiles read: {len(delivery_profiles)} ({shipping_profiles})",
        f"- Published locales read: {locale_codes}",
        f"- Policies read through Admin REST: {len(policies)} ({policy_titles})",
        "",
        "## Paid Gate Evidence",
        "",
        f"- Paid cohort rows: {paid_evidence['paid_cohort_rows']}",
        f"- Paid cohort markets: {paid_evidence['paid_cohort_markets']}",
        f"- Non-US paid rows found: {paid_evidence['non_us_paid_rows']}",
        f"- Country-exclusion upload rows: {paid_evidence['country_exclusion_rows']}",
        f"- Excluded country count: {paid_evidence['excluded_country_count']}",
        f"- US exclusion rows found: {paid_evidence['us_exclusion_rows']}",
        f"- Paid gate status: {paid_evidence['paid_gate_status']}",
        "",
        "## Live Checkout Probe",
        "",
        "- Method: anonymous storefront cart shipping-rate lookup; no payment step and no order creation.",
        f"- Probe status: {checkout_results.get('status')}",
        f"- Probe blocker: {checkout_results.get('blocker') or 'none'}",
        f"- Countries with live rates in this packet: {len(live_pass_rows)} non-US",
        f"- Countries blocked in this packet: {len(blocked_rows)} non-US",
        "",
        "## Country Matrix",
        "",
        f"- Countries/regions in matrix: {len(matrix_rows)}",
        f"- Non-US rows in matrix: {len(non_us_rows)}",
        f"- Non-US active market rows: {len(active_non_us_markets)}",
        "- Full details: `country_validation_matrix.csv`",
        "",
        "## Files",
        "",
        "- `markets_admin_readback.json`",
        "- `shipping_admin_readback.json`",
        "- `locales_admin_readback.json`",
        "- `policies_admin_readback.json`",
        "- `paid_us_only_evidence.json`",
        "- `checkout_shipping_rate_validation.json`",
        "- `country_validation_matrix.csv`",
        "- `summary.json`",
    ]
    report = "\n".join(lines) + "\n"
    (output_dir / "country_checkout_admin_validation_report.md").write_text(report, encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--storefront", default=DEFAULT_STOREFRONT)
    parser.add_argument("--paid-cohort", type=Path, default=DEFAULT_PAID_COHORT)
    parser.add_argument("--country-exclusions", type=Path, default=DEFAULT_COUNTRY_EXCLUSIONS)
    parser.add_argument(
        "--checkout-countries",
        default="US,GB,CA,AU,UA",
        help="Comma-separated ISO codes to test with live cart shipping rates.",
    )
    parser.add_argument(
        "--skip-checkout",
        action="store_true",
        help="Skip live storefront cart shipping-rate checks.",
    )
    parser.add_argument("--checkout-delay-seconds", type=float, default=8.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    store_domain = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token()
    client = ShopifyClient(store_domain, access_token, API_VERSION)

    markets = fetch_markets(client)
    delivery_profiles = fetch_delivery_profiles(client)
    locales = fetch_locales(client)
    policies = fetch_policies(store_domain, access_token)
    paid_evidence = paid_country_evidence(args.paid_cohort, args.country_exclusions)
    checkout_country_codes = [
        clean(value).upper()
        for value in args.checkout_countries.split(",")
        if clean(value)
    ]
    if args.skip_checkout:
        checkout_results = {
            "status": "SKIPPED",
            "blocker": "SKIPPED_BY_OPERATOR",
            "countries": [
                {
                    "country_code": code,
                    "status": "NOT_RUN_THIS_PASS",
                    "blocker": "SKIPPED_BY_OPERATOR",
                    "rates": [],
                    "rate_class": "",
                }
                for code in checkout_country_codes
            ],
        }
    else:
        checkout_results = live_checkout_rate_checks(
            args.storefront,
            args.paid_cohort,
            checkout_country_codes,
            args.checkout_delay_seconds,
        )

    country_names, market_by_country, shipping_by_country, rest_of_world_shipping = country_maps(
        markets,
        delivery_profiles,
    )
    matrix_rows = build_country_matrix(
        country_names,
        market_by_country,
        shipping_by_country,
        rest_of_world_shipping,
        paid_evidence,
        checkout_results,
        policies,
        locales,
    )

    matrix_fields = [
        "country_code",
        "country_name",
        "market_enabled",
        "market_names",
        "market_currencies",
        "admin_shipping_configured",
        "shipping_zones",
        "shipping_methods",
        "checkout_live_status",
        "checkout_live_rate_class",
        "checkout_live_blocker",
        "checkout_rates",
        "localized_locale_evidence",
        "policy_admin_evidence",
        "localization_pass",
        "shipping_pass",
        "returns_pass",
        "country_conversion_pass",
        "margin_pass",
        "paid_allowlist_decision",
    ]

    write_json(output_dir / "markets_admin_readback.json", {"generated_at": utcish_now(), "markets": markets})
    write_json(
        output_dir / "shipping_admin_readback.json",
        {
            "generated_at": utcish_now(),
            "delivery_profiles": delivery_profiles,
            "rest_of_world_shipping_detected": rest_of_world_shipping,
        },
    )
    write_json(output_dir / "locales_admin_readback.json", {"generated_at": utcish_now(), "locales": locales})
    write_json(output_dir / "policies_admin_readback.json", {"generated_at": utcish_now(), "policies": policies})
    write_json(output_dir / "paid_us_only_evidence.json", {"generated_at": utcish_now(), **paid_evidence})
    write_json(
        output_dir / "checkout_shipping_rate_validation.json",
        {"generated_at": utcish_now(), **checkout_results},
    )
    write_csv(output_dir / "country_validation_matrix.csv", matrix_fields, matrix_rows)

    non_us_rows = [row for row in matrix_rows if row["country_code"] != "US"]
    summary = {
        "generated_at": utcish_now(),
        "admin_api_version": API_VERSION,
        "store_domain": store_domain,
        "storefront": args.storefront,
        "decision": "KEEP_PAID_TRAFFIC_US_ONLY",
        "intentional_allowlist_expansion": False,
        "paid_gate_status": paid_evidence["paid_gate_status"],
        "country_matrix_rows": len(matrix_rows),
        "non_us_country_rows": len(non_us_rows),
        "non_us_active_market_rows": sum(1 for row in non_us_rows if row["market_enabled"] == "TRUE"),
        "non_us_live_checkout_rate_pass_rows": sum(
            1 for row in non_us_rows if row["checkout_live_status"] == "RATES_AVAILABLE"
        ),
        "checkout_probe_status": checkout_results.get("status"),
        "checkout_probe_blocker": checkout_results.get("blocker"),
        "outputs": {
            "report": str(output_dir / "country_checkout_admin_validation_report.md"),
            "country_matrix": str(output_dir / "country_validation_matrix.csv"),
        },
    }
    write_json(output_dir / "summary.json", summary)
    build_report(
        output_dir=output_dir,
        paid_evidence=paid_evidence,
        markets=markets,
        delivery_profiles=delivery_profiles,
        locales=locales,
        policies=policies,
        checkout_results=checkout_results,
        matrix_rows=matrix_rows,
    )

    print(json.dumps(summary, indent=2))
    return 0 if paid_evidence["paid_gate_status"] == "PASS_US_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
