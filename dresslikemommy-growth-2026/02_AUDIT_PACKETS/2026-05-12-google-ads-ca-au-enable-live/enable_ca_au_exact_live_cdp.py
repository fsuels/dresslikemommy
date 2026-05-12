#!/usr/bin/env python3
"""Enable the approved CA/AU Search first-test units through Google Ads CDP RPC.

Scope is intentionally tiny:
- campaign 23834423669 / ad group "Mommy & Me Dresses - Exact"
- campaign 23834424182 / ad group "Mommy & Me Dresses - Exact"
- status only: each campaign Paused -> Enabled, one ad group Paused -> Enabled

No budget, bid, product/feed, conversion, Merchant, Shopify, Pinterest, or other
ad-group changes are sent.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-ca-au-enable-live"
SPLIT_DIR = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"
AD_GROUP_NAME = "Mommy & Me Dresses - Exact"
APPROVAL = (
    "APPROVE ENABLE CA AND AU SEARCH CAMPAIGNS ONLY: ENABLE CAMPAIGN 23834423669 "
    "AD GROUP Mommy & Me Dresses - Exact AND CAMPAIGN 23834424182 AD GROUP Mommy & Me Dresses - Exact; "
    "KEEP EXISTING BUDGETS, BIDS, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, AND CONVERSION GOALS UNCHANGED; "
    "DO NOT ENABLE ANY OTHER CAMPAIGNS OR AD GROUPS."
)

TARGETS = [
    {
        "country": "CA",
        "campaign_id": "23834423669",
        "campaign_name": "DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "budget_micros": "2000000",
        "split_csv": SPLIT_DIR / "CA_intl_search_paused_draft_web_bulk.csv",
    },
    {
        "country": "AU",
        "campaign_id": "23834424182",
        "campaign_name": "DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "budget_micros": "2000000",
        "split_csv": SPLIT_DIR / "AU_intl_search_paused_draft_web_bulk.csv",
    },
]

CAMPAIGN_STATUS = {3: "ENABLED", 5: "PAUSED", 7: "REMOVED"}
ADGROUP_STATUS = {1: "ENABLED", 2: "PAUSED", 3: "REMOVED"}
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


def campaign_status_mutate_request(campaign_id: str, status_code: int) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = [
        {
            "1": 3,
            "2": ["status"],
            "3": {"1": CUSTOMER_ID, "2": campaign_id, "12": status_code},
        }
    ]
    return request


def adgroup_status_mutate_request(campaign_id: str, adgroup_id: str, status_code: int) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = [
        {
            "1": 3,
            "2": ["status"],
            "3": {"1": CUSTOMER_ID, "2": campaign_id, "3": adgroup_id, "14": status_code},
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


def read_campaign(cdp: CDP, target: dict, label: str) -> dict:
    country = target["country"]
    campaign_id = target["campaign_id"]
    request = campaign_list_request(campaign_id)
    response = rpc(cdp, "CampaignService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_campaign(campaign_id, raw)
    save_json(PACKET / f"raw/{label}/{country}/campaign_{campaign_id}_request.json", request)
    save_json(PACKET / f"raw/{label}/{country}/campaign_{campaign_id}_response.json", response)
    save_json(PACKET / f"raw/{label}/{country}/campaign_{campaign_id}_summary.json", summary)
    return summary


def read_adgroups(cdp: CDP, target: dict, label: str) -> list[dict]:
    country = target["country"]
    campaign_id = target["campaign_id"]
    request = adgroup_list_request(campaign_id)
    response = rpc(cdp, "AdGroupService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_adgroups(raw)
    save_json(PACKET / f"raw/{label}/{country}/adgroups_{campaign_id}_request.json", request)
    save_json(PACKET / f"raw/{label}/{country}/adgroups_{campaign_id}_response.json", response)
    save_json(PACKET / f"raw/{label}/{country}/adgroups_{campaign_id}_summary.json", summary)
    return summary


def read_conversion_config(cdp: CDP, target: dict, label: str) -> dict:
    country = target["country"]
    campaign_id = target["campaign_id"]
    request = conversion_config_request(campaign_id)
    response = rpc(cdp, "ConversionGoalCampaignConfigService", "List", request)
    raw = json.loads(response["text"])
    save_json(PACKET / f"raw/{label}/{country}/conversion_goal_campaign_config_request.json", request)
    save_json(PACKET / f"raw/{label}/{country}/conversion_goal_campaign_config_response.json", response)
    save_json(PACKET / f"raw/{label}/{country}/conversion_goal_campaign_config_raw.json", raw)
    return raw


def split_csv_safety_summary(target: dict) -> dict:
    rows = list(csv.DictReader(target["split_csv"].open(newline="", encoding="utf-8-sig")))
    target_keywords = [
        row
        for row in rows
        if row.get("Row Type") == "Keyword" and row.get("Ad group") == AD_GROUP_NAME
    ]
    target_ads = [
        row
        for row in rows
        if row.get("Row Type") == "Ad" and row.get("Ad group") == AD_GROUP_NAME
    ]
    return {
        "source": str(target["split_csv"]),
        "country": target["country"],
        "target_ad_group": AD_GROUP_NAME,
        "keyword_count": len(target_keywords),
        "keywords": [
            {
                "keyword": row["Keyword"],
                "match_type": row["Type"],
                "status": row["Keyword status"],
                "final_url": row["Final URL"],
            }
            for row in target_keywords
        ],
        "ad_count": len(target_ads),
        "ads": [
            {
                "status": row["Ad status"],
                "final_url": row["Final URL"],
                "headline_1": row["Headline 1"],
                "headline_2": row["Headline 2"],
                "headline_3": row["Headline 3"],
                "description_1": row["Description 1"],
                "description_2": row["Description 2"],
            }
            for row in target_ads
        ],
        "all_keywords_exact": all(row["Type"] == "Exact match" for row in target_keywords),
        "all_keywords_paused": all(row["Keyword status"] == "Paused" for row in target_keywords),
        "all_ads_paused": all(row["Ad status"] == "Paused" for row in target_ads),
        "all_final_urls_country": all(f"?country={target['country']}" in row["Final URL"] for row in target_keywords + target_ads),
    }


def target_adgroup(target: dict, adgroups: list[dict]) -> dict:
    rows = [row for row in adgroups if row["ad_group_name"] == AD_GROUP_NAME]
    if len(rows) != 1:
        raise RuntimeError(f"Expected exactly one target ad group named {AD_GROUP_NAME} for {target['country']}, got {rows}")
    return rows[0]


def validate_pre(target: dict, campaign: dict, adgroups: list[dict], split: dict, conversion_config: dict) -> str:
    target_group = target_adgroup(target, adgroups)
    checks = {
        "campaign_id": campaign["campaign_id"] == target["campaign_id"],
        "campaign_name": campaign["campaign_name"] == target["campaign_name"],
        "campaign_paused": campaign["campaign_status_code"] == 5,
        "search": campaign["advertising_channel_type_code"] == 1,
        "budget_expected": campaign["budget_micros"] == target["budget_micros"],
        "content_off": campaign["target_content_network"] is False,
        "youtube_off": campaign["target_youtube_video"] is False,
        "google_search_on": campaign["target_google_search"] is True,
        "positive_presence": campaign["geo_target_type_setting_raw"].get("16") == 18,
        "negative_presence": campaign["geo_target_type_setting_raw"].get("17") == 18,
        "target_adgroup_paused": target_group["ad_group_status_code"] == 2,
        "all_adgroups_paused": all(row["ad_group_status_code"] == 2 for row in adgroups),
        "split_keywords_exact": split["all_keywords_exact"],
        "split_keywords_paused": split["all_keywords_paused"],
        "split_ads_paused": split["all_ads_paused"],
        "split_urls_country": split["all_final_urls_country"],
        "no_campaign_conversion_override": (
            len(conversion_config.get("1", [])) == 1
            and conversion_config["1"][0].get("3") is False
        ),
    }
    save_json(PACKET / f"raw/pre-enable-readback/{target['country']}/pre_enable_gate_checks.json", checks)
    if not all(checks.values()):
        raise RuntimeError(json.dumps({"country": target["country"], "checks": checks, "campaign": campaign, "adgroups": adgroups, "split": split, "conversion_config": conversion_config}, indent=2, ensure_ascii=False))
    return target_group["ad_group_id"]


def validate_post(target: dict, adgroup_id: str, pre_campaign: dict, pre_adgroups: list[dict], post_campaign: dict, post_adgroups: list[dict], post_conversion: dict):
    pre_by_id = {row["ad_group_id"]: row for row in pre_adgroups}
    post_by_id = {row["ad_group_id"]: row for row in post_adgroups}
    exact_delta = {
        "campaign_enabled": post_campaign["campaign_status_code"] == 3,
        "budget_unchanged": post_campaign["budget_micros"] == pre_campaign["budget_micros"] == target["budget_micros"],
        "network_unchanged": (
            post_campaign["target_content_network"] == pre_campaign["target_content_network"] is False
            and post_campaign["target_youtube_video"] == pre_campaign["target_youtube_video"] is False
            and post_campaign["target_google_search"] == pre_campaign["target_google_search"] is True
        ),
        "geo_unchanged": post_campaign["geo_target_type_setting_raw"] == pre_campaign["geo_target_type_setting_raw"] == {"16": 18, "17": 18},
        "target_adgroup_enabled": post_by_id[adgroup_id]["ad_group_status_code"] == 1,
        "other_adgroups_paused": all(
            row["ad_group_status_code"] == 2
            for group_id, row in post_by_id.items()
            if group_id != adgroup_id
        ),
        "adgroup_set_unchanged": sorted(pre_by_id) == sorted(post_by_id),
        "no_campaign_conversion_override": (
            len(post_conversion.get("1", [])) == 1
            and post_conversion["1"][0].get("3") is False
        ),
    }
    save_json(PACKET / f"raw/post-enable-readback/{target['country']}/post_enable_delta_checks.json", exact_delta)
    if not all(exact_delta.values()):
        raise RuntimeError(json.dumps({"country": target["country"], "post_enable_delta_checks": exact_delta, "pre_campaign": pre_campaign, "post_campaign": post_campaign, "pre_adgroups": pre_adgroups, "post_adgroups": post_adgroups, "post_conversion": post_conversion}, indent=2, ensure_ascii=False))


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
        adgroup_id = item["adgroup_id"]
        try:
            mutate_status(cdp, target, "AdGroupService", adgroup_status_mutate_request(target["campaign_id"], adgroup_id, 2), "rollback_adgroup_pause")
            mutate_status(cdp, target, "CampaignService", campaign_status_mutate_request(target["campaign_id"], 5), "rollback_campaign_pause")
            time.sleep(2)
            save_json(rollback_dir / f"{target['country']}_campaign_after_rollback.json", read_campaign(cdp, target, "rollback"))
            save_json(rollback_dir / f"{target['country']}_adgroups_after_rollback.json", read_adgroups(cdp, target, "rollback"))
        except Exception as exc:
            (rollback_dir / f"{target['country']}_rollback_failure.txt").write_text(repr(exc) + "\n", encoding="utf-8")
            raise


def main() -> int:
    page = get_ads_page()
    cdp = CDP(page["webSocketDebuggerUrl"])
    cdp.call("Runtime.enable")
    touched: list[dict] = []
    final = []
    try:
        (PACKET / "raw/enable-action/approval_phrase.txt").parent.mkdir(parents=True, exist_ok=True)
        (PACKET / "raw/enable-action/approval_phrase.txt").write_text(APPROVAL + "\n", encoding="utf-8")
        timestamp = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="seconds")
        (PACKET / "raw/enable-action/enable_action_timestamp.txt").write_text(timestamp + "\n", encoding="utf-8")

        pre_state = {}
        for target in TARGETS:
            split = split_csv_safety_summary(target)
            save_json(PACKET / f"raw/pre-enable-readback/{target['country']}/split_csv_target_adgroup_summary.json", split)
            pre_campaign = read_campaign(cdp, target, "pre-enable-readback")
            pre_adgroups = read_adgroups(cdp, target, "pre-enable-readback")
            pre_conversion = read_conversion_config(cdp, target, "pre-enable-readback")
            adgroup_id = validate_pre(target, pre_campaign, pre_adgroups, split, pre_conversion)
            pre_state[target["country"]] = {
                "target": target,
                "adgroup_id": adgroup_id,
                "pre_campaign": pre_campaign,
                "pre_adgroups": pre_adgroups,
                "pre_conversion": pre_conversion,
                "split": split,
            }

        for target in TARGETS:
            state = pre_state[target["country"]]
            adgroup_id = state["adgroup_id"]
            mutate_status(cdp, target, "AdGroupService", adgroup_status_mutate_request(target["campaign_id"], adgroup_id, 1), "adgroup_enable_updateop3")
            time.sleep(2)
            mutate_status(cdp, target, "CampaignService", campaign_status_mutate_request(target["campaign_id"], 3), "campaign_enable_updateop3")
            touched.append({"target": target, "adgroup_id": adgroup_id})
            time.sleep(4)

            post_campaign = read_campaign(cdp, target, "post-enable-readback")
            post_adgroups = read_adgroups(cdp, target, "post-enable-readback")
            post_conversion = read_conversion_config(cdp, target, "post-enable-readback")
            validate_post(target, adgroup_id, state["pre_campaign"], state["pre_adgroups"], post_campaign, post_adgroups, post_conversion)
            final.append(
                {
                    "country": target["country"],
                    "campaign_id": target["campaign_id"],
                    "campaign_name": target["campaign_name"],
                    "campaign_status": post_campaign["campaign_status"],
                    "campaign_status_code": post_campaign["campaign_status_code"],
                    "target_adgroup_id": adgroup_id,
                    "target_adgroup_name": AD_GROUP_NAME,
                    "target_adgroup_status": [row for row in post_adgroups if row["ad_group_id"] == adgroup_id][0]["ad_group_status"],
                    "budget_micros": post_campaign["budget_micros"],
                    "budget_usd": post_campaign["budget_usd"],
                    "currency": post_campaign["currency"],
                    "target_google_search": post_campaign["target_google_search"],
                    "target_content_network": post_campaign["target_content_network"],
                    "target_youtube_video": post_campaign["target_youtube_video"],
                    "geo_target_type_setting_raw": post_campaign["geo_target_type_setting_raw"],
                    "enabled_adgroups": [
                        {
                            "ad_group_id": row["ad_group_id"],
                            "ad_group_name": row["ad_group_name"],
                            "status_code": row["ad_group_status_code"],
                        }
                        for row in post_adgroups
                        if row["ad_group_status_code"] == 1
                    ],
                    "paused_adgroups": [
                        {
                            "ad_group_id": row["ad_group_id"],
                            "ad_group_name": row["ad_group_name"],
                            "status_code": row["ad_group_status_code"],
                        }
                        for row in post_adgroups
                        if row["ad_group_status_code"] == 2
                    ],
                }
            )

        save_json(
            PACKET / "raw/post-enable-readback/final_success_summary.json",
            {
                "status": "DONE_LIVE_ENABLE_CA_AU_RPC_READBACK_PASSED",
                "approval_phrase": APPROVAL,
                "enable_timestamp_pacific": timestamp,
                "results": final,
            },
        )
        print(json.dumps({"status": "DONE_LIVE_ENABLE_CA_AU_RPC_READBACK_PASSED", "timestamp_pacific": timestamp}, indent=2))
        return 0
    except Exception as exc:
        error_path = PACKET / "raw/enable-action/enable_error.txt"
        error_path.parent.mkdir(parents=True, exist_ok=True)
        error_path.write_text(repr(exc) + "\n", encoding="utf-8")
        rollback(cdp, touched, f"CA/AU enable failed or post-readback delta invalid: {exc!r}")
        raise
    finally:
        cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
