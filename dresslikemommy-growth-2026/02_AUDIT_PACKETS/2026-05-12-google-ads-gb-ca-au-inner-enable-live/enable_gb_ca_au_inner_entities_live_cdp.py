#!/usr/bin/env python3
"""Enable the exact approved GB/CA/AU inner Search entities.

Scope is intentionally tiny:
- GB/CA/AU campaign + exact ad groups are already enabled.
- Enable only the 3 exact-match keyword criteria and 1 RSA ad in each named
  "Mommy & Me Dresses - Exact" ad group.

No budget, bid, product/feed, conversion, Merchant, Shopify, Pinterest, PMax,
Standard Shopping, campaign, or ad-group changes are sent.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-inner-enable-live"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"
AD_GROUP_NAME = "Mommy & Me Dresses - Exact"
APPROVAL = (
    "APPROVE ENABLE GB CA AU EXACT SEARCH INNER ENTITIES ONLY: IN CAMPAIGN 23838895360 "
    "AD GROUP Mommy & Me Dresses - Exact, CAMPAIGN 23834423669 AD GROUP Mommy & Me Dresses - Exact, "
    "AND CAMPAIGN 23834424182 AD GROUP Mommy & Me Dresses - Exact, ENABLE ONLY THE 3 EXACT-MATCH "
    "KEYWORDS mommy and me dresses, mother daughter dresses, mom and daughter matching outfits AND "
    "THE 1 RESPONSIVE SEARCH AD IN EACH NAMED AD GROUP; KEEP ALL OTHER AD GROUPS, ADS, KEYWORDS, "
    "CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, CONVERSION GOALS, PMAX, "
    "STANDARD SHOPPING, SHOPIFY PRODUCT DATA, AND BILLING UNCHANGED."
)

TARGETS = [
    {
        "country": "GB",
        "campaign_id": "23838895360",
        "campaign_name": "DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "ad_group_id": "194138528537",
        "budget_micros": "2000000",
        "keyword_criterion_ids": ["299141671628", "301154335636", "301154336396"],
        "ad_id": "808406712704",
    },
    {
        "country": "CA",
        "campaign_id": "23834423669",
        "campaign_name": "DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "ad_group_id": "196679079575",
        "budget_micros": "2000000",
        "keyword_criterion_ids": ["299141671628", "301154335636", "301154336396"],
        "ad_id": "808294804728",
    },
    {
        "country": "AU",
        "campaign_id": "23834424182",
        "campaign_name": "DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "ad_group_id": "198852670520",
        "budget_micros": "2000000",
        "keyword_criterion_ids": ["299141671628", "301154335636", "301154336396"],
        "ad_id": "808328767090",
    },
]

CAMPAIGN_STATUS = {3: "ENABLED", 5: "PAUSED", 7: "REMOVED"}
ADGROUP_STATUS = {1: "ENABLED", 2: "PAUSED", 3: "REMOVED"}
CRITERION_STATUS = {1: "ENABLED", 3: "PAUSED", 4: "REMOVED"}
AD_STATUS = {1: "ENABLED", 2: "PAUSED", 3: "REMOVED"}
GEO = {16: "DONT_CARE", 17: "AREA_OF_INTEREST", 18: "LOCATION_OF_PRESENCE"}

BASE_CONTEXT = {
    "1": {
        "3": {"1": CUSTOMER_ID},
        "6": "-25200000",
        "7": "1493889124247",
        "8": "{\"1\":[{\"1\":\"1000004\",\"2\":\"TREATMENT\"},{\"1\":\"1000033\",\"2\":\"TREATMENT\"},{\"1\":\"1000052\",\"2\":\"CONTROL\"},{\"1\":\"1000058\",\"2\":\"TREATMENT\"},{\"1\":\"1000069\",\"2\":\"TREATMENT\"},{\"1\":\"1090079\",\"2\":\"TREATMENT\"},{\"1\":\"1090088\",\"2\":\"TREATMENT\"}]}",
    }
}


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)
        self.next_id = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.next_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expression: str):
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True},
        )
        return result.get("result", {}).get("value")

    def close(self):
        self.ws.close()


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")


def json_get(path: str):
    with urllib.request.urlopen(f"{CDP_BASE}{path}", timeout=20) as response:
        return json.load(response)


def get_ads_page() -> dict:
    pages = json_get("/json/list")
    for page in pages:
        if page.get("type") == "page" and "ads.google.com" in page.get("url", ""):
            return page
    raise RuntimeError("No logged-in Google Ads CDP page found on 127.0.0.1:9222")


def rpc(cdp: CDP, service: str, method: str, request: dict) -> dict:
    endpoint = (
        f"https://ads.google.com/aw_cm/editing/_/rpc/{service}/{method}"
        f"?authuser=0&xt=awn&rpcTrackingId={urllib.parse.quote(service + '.' + method + ':1')}"
    )
    expression = f"""
(async () => {{
  const token = window.$acx && window.$acx.xsrfToken;
  if (!token) return {{status: 0, ok: false, text: 'missing xsrf token'}};
  const params = new URLSearchParams();
  params.set('hl', 'zh_CN');
  params.set('__lu', '228618707');
  params.set('__u', '2136917243');
  params.set('__c', '9710510557');
  params.set('ps', 'aw');
  params.set('__ar', JSON.stringify({json.dumps(request)}));
  const res = await fetch({json.dumps(endpoint)}, {{
    method: 'POST',
    credentials: 'include',
    headers: {{
      'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'x-framework-xsrf-token': token
    }},
    body: params.toString()
  }});
  const text = await res.text();
  return {{status: res.status, ok: res.ok, tokenLen: token.length, text}};
}})()
"""
    response = cdp.eval(expression)
    if not response or not response.get("ok"):
        raise RuntimeError(json.dumps({"service": service, "method": method, "response": response}, indent=2))
    return response


def campaign_list_request(campaign_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = {
        "1": [
            "campaign_id",
            "name",
            "status",
            "advertising_channel_type",
            "target_google_search",
            "target_search_network",
            "target_content_network",
            "target_youtube_video",
            "geo_target_type_setting",
            "languages",
            "budget_amount",
            "budget.currency_code",
            "budget.delivery_method",
            "bid_strategy_type",
            "serving_status",
        ],
        "2": [{"1": "campaign_id", "2": 1, "4": [{"3": campaign_id}]}],
    }
    return request


def adgroup_list_request(campaign_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = {
        "1": [
            "customer_id",
            "campaign_id",
            "ad_group_id",
            "name",
            "status",
            "type",
            "cpc_bid",
            "effective_cpc_bid",
            "campaign.name",
        ],
        "2": [{"1": "campaign_id", "2": 1, "4": [{"3": campaign_id}]}],
    }
    return request


def conversion_config_request(campaign_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = {
        "1": ["has_campaign_override_goals", "custom_conversion_goal_id"],
        "2": [{"1": "campaign_id", "2": 1, "4": [{"3": campaign_id}]}],
    }
    return request


def list_keywords_request(ad_group_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = {
        "1": [
            "customer_id",
            "campaign_id",
            "ad_group_id",
            "criterion_id",
            "status",
            "keyword.text",
            "keyword.match_type",
            "final_urls",
        ],
        "2": [{"1": "ad_group_id", "2": 1, "4": [{"3": ad_group_id}]}],
    }
    return request


def list_ads_request(ad_group_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = {
        "1": [
            "customer_id",
            "campaign_id",
            "ad_group_id",
            "ad_id",
            "status",
            "ad.type",
            "ad.final_urls",
            "responsive_search_ad.headlines",
            "responsive_search_ad.descriptions",
        ],
        "2": [{"1": "ad_group_id", "2": 1, "4": [{"3": ad_group_id}]}],
    }
    return request


def criterion_status_mutate_request(campaign_id: str, ad_group_id: str, criterion_id: str, status_code: int) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = [
        {
            "1": 3,
            "2": ["status"],
            "3": {
                "1": CUSTOMER_ID,
                "2": campaign_id,
                "3": ad_group_id,
                "4": criterion_id,
                "21": status_code,
            },
        }
    ]
    return request


def ad_status_mutate_request(campaign_id: str, ad_group_id: str, ad_id: str, status_code: int) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = [
        {
            "1": 3,
            "2": ["status"],
            "3": {
                "1": CUSTOMER_ID,
                "2": campaign_id,
                "3": ad_group_id,
                "4": ad_id,
                "5": status_code,
            },
        }
    ]
    return request


def parse_campaign(campaign_id: str, raw: dict) -> dict:
    rows = raw.get("1", [])
    if len(rows) != 1:
        raise RuntimeError(f"Expected one campaign row for {campaign_id}, got {len(rows)}")
    row = rows[0]
    geo = row.get("43", {})
    return {
        "customer_id": row.get("1"),
        "campaign_id": row.get("2"),
        "campaign_name": row.get("11"),
        "campaign_status_code": row.get("12"),
        "campaign_status": CAMPAIGN_STATUS.get(row.get("12"), f"UNKNOWN_{row.get('12')}"),
        "advertising_channel_type_code": row.get("15"),
        "budget_micros": row.get("17"),
        "budget_usd": int(row["17"]) / 1_000_000 if row.get("17") and str(row["17"]).isdigit() else None,
        "currency": row.get("31", {}).get("9"),
        "target_content_network": row.get("20"),
        "target_google_search": row.get("21"),
        "target_search_network": row.get("22"),
        "target_youtube_video": row.get("23"),
        "geo_target_type_setting_raw": geo,
        "positive_geo_target_type": GEO.get(geo.get("16"), f"UNKNOWN_{geo.get('16')}"),
        "negative_geo_target_type": GEO.get(geo.get("17"), f"UNKNOWN_{geo.get('17')}"),
        "languages": row.get("50"),
        "raw": row,
    }


def parse_adgroups(raw: dict) -> list[dict]:
    out = []
    for row in raw.get("1", []):
        out.append(
            {
                "customer_id": row.get("1"),
                "campaign_id": row.get("2"),
                "ad_group_id": row.get("3"),
                "ad_group_name": row.get("11"),
                "ad_group_status_code": row.get("14"),
                "ad_group_status": ADGROUP_STATUS.get(row.get("14"), f"UNKNOWN_{row.get('14')}"),
                "ad_group_type_code": row.get("26"),
                "raw": row,
            }
        )
    return out


def parse_keyword_rows(raw: dict) -> list[dict]:
    rows = []
    for row in raw.get("1", []):
        status_code = row.get("21")
        rows.append(
            {
                "customer_id": row.get("1"),
                "campaign_id": row.get("2"),
                "ad_group_id": row.get("3"),
                "criterion_id": row.get("4"),
                "status_code": status_code,
                "status": CRITERION_STATUS.get(status_code, f"UNKNOWN_{status_code}"),
                "final_urls": row.get("24", []),
                "raw": row,
            }
        )
    return rows


def parse_ad_rows(raw: dict) -> list[dict]:
    rows = []
    for row in raw.get("1", []):
        status_code = row.get("5")
        ad = row.get("13", {})
        rows.append(
            {
                "customer_id": row.get("1"),
                "campaign_id": row.get("2"),
                "ad_group_id": row.get("3"),
                "ad_id": row.get("4"),
                "status_code": status_code,
                "status": AD_STATUS.get(status_code, f"UNKNOWN_{status_code}"),
                "ad_type_code": ad.get("3"),
                "final_urls": ad.get("5", []),
                "raw": row,
            }
        )
    return rows


def read_campaign(cdp: CDP, target: dict, label: str) -> dict:
    request = campaign_list_request(target["campaign_id"])
    response = rpc(cdp, "CampaignService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_campaign(target["campaign_id"], raw)
    save_json(PACKET / f"raw/{label}/{target['country']}/campaign_request.json", request)
    save_json(PACKET / f"raw/{label}/{target['country']}/campaign_response.json", response)
    save_json(PACKET / f"raw/{label}/{target['country']}/campaign_summary.json", summary)
    return summary


def read_adgroups(cdp: CDP, target: dict, label: str) -> list[dict]:
    request = adgroup_list_request(target["campaign_id"])
    response = rpc(cdp, "AdGroupService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_adgroups(raw)
    save_json(PACKET / f"raw/{label}/{target['country']}/adgroups_request.json", request)
    save_json(PACKET / f"raw/{label}/{target['country']}/adgroups_response.json", response)
    save_json(PACKET / f"raw/{label}/{target['country']}/adgroups_summary.json", summary)
    return summary


def read_conversion_config(cdp: CDP, target: dict, label: str) -> dict:
    request = conversion_config_request(target["campaign_id"])
    response = rpc(cdp, "ConversionGoalCampaignConfigService", "List", request)
    raw = json.loads(response["text"])
    save_json(PACKET / f"raw/{label}/{target['country']}/conversion_goal_campaign_config_request.json", request)
    save_json(PACKET / f"raw/{label}/{target['country']}/conversion_goal_campaign_config_response.json", response)
    save_json(PACKET / f"raw/{label}/{target['country']}/conversion_goal_campaign_config_raw.json", raw)
    return raw


def read_keywords(cdp: CDP, target: dict, label: str) -> list[dict]:
    request = list_keywords_request(target["ad_group_id"])
    response = rpc(cdp, "AdGroupCriterionService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_keyword_rows(raw)
    save_json(PACKET / f"raw/{label}/{target['country']}/keywords_request.json", request)
    save_json(PACKET / f"raw/{label}/{target['country']}/keywords_response.json", response)
    save_json(PACKET / f"raw/{label}/{target['country']}/keywords_summary.json", summary)
    return summary


def read_ads(cdp: CDP, target: dict, label: str) -> list[dict]:
    request = list_ads_request(target["ad_group_id"])
    response = rpc(cdp, "AdGroupAdService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_ad_rows(raw)
    save_json(PACKET / f"raw/{label}/{target['country']}/ads_request.json", request)
    save_json(PACKET / f"raw/{label}/{target['country']}/ads_response.json", response)
    save_json(PACKET / f"raw/{label}/{target['country']}/ads_summary.json", summary)
    return summary


def target_adgroup(target: dict, adgroups: list[dict]) -> dict:
    rows = [row for row in adgroups if row["ad_group_id"] == target["ad_group_id"]]
    if len(rows) != 1:
        raise RuntimeError(f"Expected one target ad group {target['ad_group_id']}, got {rows}")
    return rows[0]


def validate_common(target: dict, campaign: dict, adgroups: list[dict], conversion_config: dict) -> dict:
    group = target_adgroup(target, adgroups)
    checks = {
        "campaign_id": campaign["campaign_id"] == target["campaign_id"],
        "campaign_name": campaign["campaign_name"] == target["campaign_name"],
        "campaign_enabled": campaign["campaign_status_code"] == 3,
        "target_adgroup_enabled": group["ad_group_status_code"] == 1 and group["ad_group_name"] == AD_GROUP_NAME,
        "only_one_adgroup_enabled": sum(1 for row in adgroups if row["ad_group_status_code"] == 1) == 1,
        "other_adgroups_paused": all(
            row["ad_group_status_code"] == 2
            for row in adgroups
            if row["ad_group_id"] != target["ad_group_id"]
        ),
        "search": campaign["advertising_channel_type_code"] == 1,
        "budget_expected": campaign["budget_micros"] == target["budget_micros"],
        "content_off": campaign["target_content_network"] is False,
        "youtube_off": campaign["target_youtube_video"] is False,
        "google_search_on": campaign["target_google_search"] is True,
        "positive_presence": campaign["geo_target_type_setting_raw"].get("16") == 18,
        "negative_presence": campaign["geo_target_type_setting_raw"].get("17") == 18,
        "no_campaign_conversion_override": (
            len(conversion_config.get("1", [])) == 1
            and conversion_config["1"][0].get("3") is False
        ),
    }
    return checks


def validate_inner(target: dict, keywords: list[dict], ads: list[dict], expected_keyword_status: int | set[int], expected_ad_status: int) -> dict:
    keyword_ids = sorted(row["criterion_id"] for row in keywords)
    expected_keyword_ids = sorted(target["keyword_criterion_ids"])
    expected_keyword_statuses = (
        expected_keyword_status if isinstance(expected_keyword_status, set) else {expected_keyword_status}
    )
    checks = {
        "exact_three_keyword_criteria": keyword_ids == expected_keyword_ids,
        "all_keywords_expected_status": all(row["status_code"] in expected_keyword_statuses for row in keywords),
        "exact_one_rsa_ad": len(ads) == 1 and ads[0]["ad_id"] == target["ad_id"] and ads[0]["ad_type_code"] == 102,
        "ad_expected_status": len(ads) == 1 and ads[0]["status_code"] == expected_ad_status,
        "urls_country_qualified": all(
            f"?country={target['country']}" in url
            for row in keywords + ads
            for url in row.get("final_urls", [])
        ),
    }
    return checks


def mutate_status(cdp: CDP, target: dict, service: str, request: dict, out_name: str):
    response = rpc(cdp, service, "Mutate", request)
    save_json(PACKET / f"raw/enable-action/{target['country']}/{out_name}_request.json", request)
    save_json(PACKET / f"raw/enable-action/{target['country']}/{out_name}_response.json", response)
    return response


def rollback(cdp: CDP, touched: list[dict], reason: str):
    rollback_dir = PACKET / "rollback"
    rollback_dir.mkdir(parents=True, exist_ok=True)
    (rollback_dir / "trigger_summary.txt").write_text(reason + "\n", encoding="utf-8")
    for item in reversed(touched):
        target = item["target"]
        if item["type"] == "keyword":
            mutate_status(
                cdp,
                target,
                "AdGroupCriterionService",
                criterion_status_mutate_request(target["campaign_id"], target["ad_group_id"], item["id"], 3),
                f"rollback_keyword_{item['id']}_pause",
            )
        elif item["type"] == "ad":
            mutate_status(
                cdp,
                target,
                "AdGroupAdService",
                ad_status_mutate_request(target["campaign_id"], target["ad_group_id"], item["id"], 2),
                f"rollback_ad_{item['id']}_pause",
            )
        time.sleep(1)


def main() -> int:
    page = get_ads_page()
    cdp = CDP(page["webSocketDebuggerUrl"])
    cdp.call("Runtime.enable")
    touched: list[dict] = []
    final_results = []
    try:
        (PACKET / "raw/enable-action/approval_phrase.txt").parent.mkdir(parents=True, exist_ok=True)
        (PACKET / "raw/enable-action/approval_phrase.txt").write_text(APPROVAL + "\n", encoding="utf-8")
        timestamp = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="seconds")
        (PACKET / "raw/enable-action/enable_action_timestamp.txt").write_text(timestamp + "\n", encoding="utf-8")

        pre_state = {}
        for target in TARGETS:
            campaign = read_campaign(cdp, target, "pre-enable-readback")
            adgroups = read_adgroups(cdp, target, "pre-enable-readback")
            conversion = read_conversion_config(cdp, target, "pre-enable-readback")
            keywords = read_keywords(cdp, target, "pre-enable-readback")
            ads = read_ads(cdp, target, "pre-enable-readback")
            checks = {
                **validate_common(target, campaign, adgroups, conversion),
                **validate_inner(target, keywords, ads, expected_keyword_status={1, 3}, expected_ad_status=2),
            }
            save_json(PACKET / f"raw/pre-enable-readback/{target['country']}/pre_enable_gate_checks.json", checks)
            if not all(checks.values()):
                raise RuntimeError(json.dumps({"country": target["country"], "checks": checks}, indent=2))
            pre_state[target["country"]] = {
                "campaign": campaign,
                "adgroups": adgroups,
                "conversion": conversion,
                "keywords": keywords,
                "ads": ads,
            }

        for target in TARGETS:
            for criterion_id in target["keyword_criterion_ids"]:
                mutate_status(
                    cdp,
                    target,
                    "AdGroupCriterionService",
                    criterion_status_mutate_request(target["campaign_id"], target["ad_group_id"], criterion_id, 1),
                    f"keyword_{criterion_id}_enable",
                )
                touched.append({"target": target, "type": "keyword", "id": criterion_id})
                time.sleep(1)
            mutate_status(
                cdp,
                target,
                "AdGroupAdService",
                ad_status_mutate_request(target["campaign_id"], target["ad_group_id"], target["ad_id"], 1),
                f"ad_{target['ad_id']}_enable",
            )
            touched.append({"target": target, "type": "ad", "id": target["ad_id"]})
            time.sleep(3)

            post_campaign = read_campaign(cdp, target, "post-enable-readback")
            post_adgroups = read_adgroups(cdp, target, "post-enable-readback")
            post_conversion = read_conversion_config(cdp, target, "post-enable-readback")
            post_keywords = read_keywords(cdp, target, "post-enable-readback")
            post_ads = read_ads(cdp, target, "post-enable-readback")
            post_checks = {
                **validate_common(target, post_campaign, post_adgroups, post_conversion),
                **validate_inner(target, post_keywords, post_ads, expected_keyword_status=1, expected_ad_status=1),
                "campaign_budget_unchanged": post_campaign["budget_micros"] == pre_state[target["country"]]["campaign"]["budget_micros"],
                "adgroup_set_unchanged": sorted(row["ad_group_id"] for row in post_adgroups)
                == sorted(row["ad_group_id"] for row in pre_state[target["country"]]["adgroups"]),
            }
            save_json(PACKET / f"raw/post-enable-readback/{target['country']}/post_enable_delta_checks.json", post_checks)
            if not all(post_checks.values()):
                raise RuntimeError(json.dumps({"country": target["country"], "post_checks": post_checks}, indent=2))
            final_results.append(
                {
                    "country": target["country"],
                    "campaign_id": target["campaign_id"],
                    "ad_group_id": target["ad_group_id"],
                    "enabled_keyword_criterion_ids": target["keyword_criterion_ids"],
                    "enabled_ad_id": target["ad_id"],
                    "post_keyword_statuses": [
                        {"criterion_id": row["criterion_id"], "status": row["status"], "status_code": row["status_code"]}
                        for row in post_keywords
                    ],
                    "post_ad_statuses": [
                        {"ad_id": row["ad_id"], "status": row["status"], "status_code": row["status_code"]}
                        for row in post_ads
                    ],
                    "campaign_status": post_campaign["campaign_status"],
                    "budget_micros": post_campaign["budget_micros"],
                    "enabled_adgroups": [
                        {"ad_group_id": row["ad_group_id"], "name": row["ad_group_name"], "status": row["ad_group_status"]}
                        for row in post_adgroups
                        if row["ad_group_status_code"] == 1
                    ],
                }
            )

        summary = {
            "status": "DONE_LIVE_ENABLE_GB_CA_AU_INNER_ENTITIES_READBACK_PASSED",
            "approval_phrase": APPROVAL,
            "enable_timestamp_pacific": timestamp,
            "results": final_results,
        }
        save_json(PACKET / "raw/post-enable-readback/final_success_summary.json", summary)
        print(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    except Exception as exc:
        error_path = PACKET / "raw/enable-action/enable_error.txt"
        error_path.parent.mkdir(parents=True, exist_ok=True)
        error_path.write_text(repr(exc) + "\n", encoding="utf-8")
        if touched:
            rollback(cdp, touched, repr(exc))
        raise
    finally:
        cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
