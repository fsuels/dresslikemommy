#!/usr/bin/env python3
"""Read-only monitor for the live GB/CA/AU first Search cohort.

Captures Google Ads RPC status readbacks plus visible UI campaign text. It does
not click Save/Apply/Enable/Pause or mutate any Ads setting.
"""

from __future__ import annotations

import base64
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring"
RAW = PACKET / "raw"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"
AD_GROUP_NAME = "Mommy & Me Dresses - Exact"

TARGETS = [
    {
        "country": "GB",
        "campaign_id": "23838895360",
        "campaign_name": "DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "target_adgroup_id": "194138528537",
        "budget_micros": "2000000",
    },
    {
        "country": "CA",
        "campaign_id": "23834423669",
        "campaign_name": "DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "target_adgroup_id": "196679079575",
        "budget_micros": "2000000",
    },
    {
        "country": "AU",
        "campaign_id": "23834424182",
        "campaign_name": "DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507",
        "target_adgroup_id": "198852670520",
        "budget_micros": "2000000",
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


def json_put_new_tab(url: str) -> dict:
    with urllib.request.urlopen(
        urllib.request.Request(f"{CDP_BASE}/json/new?{urllib.parse.quote(url, safe='')}", method="PUT"),
        timeout=20,
    ) as response:
        return json.load(response)


def close_tab(target_id: str):
    try:
        with urllib.request.urlopen(f"{CDP_BASE}/json/close/{target_id}", timeout=10):
            pass
    except Exception:
        pass


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


def parse_campaign(raw: dict) -> dict:
    row = raw.get("1", [])[0]
    geo = row.get("43", {})
    return {
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
    }


def parse_adgroups(raw: dict) -> list[dict]:
    return [
        {
            "campaign_id": row.get("2"),
            "ad_group_id": row.get("3"),
            "ad_group_name": row.get("11"),
            "ad_group_status_code": row.get("14"),
            "ad_group_status": ADGROUP_STATUS.get(row.get("14"), f"UNKNOWN_{row.get('14')}"),
            "ad_group_type_code": row.get("26"),
        }
        for row in raw.get("1", [])
    ]


def read_rpc_state(cdp: CDP, target: dict) -> dict:
    country = target["country"]
    campaign_response = rpc(cdp, "CampaignService", "List", campaign_list_request(target["campaign_id"]))
    adgroup_response = rpc(cdp, "AdGroupService", "List", adgroup_list_request(target["campaign_id"]))
    conversion_response = rpc(cdp, "ConversionGoalCampaignConfigService", "List", conversion_config_request(target["campaign_id"]))
    campaign_raw = json.loads(campaign_response["text"])
    adgroups_raw = json.loads(adgroup_response["text"])
    conversion_raw = json.loads(conversion_response["text"])
    campaign = parse_campaign(campaign_raw)
    adgroups = parse_adgroups(adgroups_raw)
    save_json(RAW / "rpc" / country / "campaign_response.json", campaign_response)
    save_json(RAW / "rpc" / country / "adgroups_response.json", adgroup_response)
    save_json(RAW / "rpc" / country / "conversion_goal_campaign_config_raw.json", conversion_raw)
    return {"campaign": campaign, "adgroups": adgroups, "conversion_config": conversion_raw}


def capture_campaign_ui(target: dict) -> dict:
    url = (
        "https://ads.google.com/aw/campaigns"
        f"?ocid={CUSTOMER_ID}&euid=228618707&__u=2136917243&uscid={CUSTOMER_ID}"
        f"&__c=9710510557&authuser=0&campaignId={target['campaign_id']}"
    )
    tab = json_put_new_tab(url)
    cdp = CDP(tab["webSocketDebuggerUrl"])
    try:
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Page.bringToFront")
        time.sleep(8)
        data = cdp.eval(
            r"""
(() => {
  const text = document.body ? document.body.innerText : "";
  const lines = text.split(/\n+/).map(s => s.trim()).filter(Boolean);
  return {
    title: document.title,
    url: location.href,
    timestamp: new Date().toISOString(),
    bodyTextLength: text.length,
    bodyText: text,
    lines: lines.slice(0, 400),
  };
})()
"""
        )
        country = target["country"]
        save_json(RAW / "ui" / country / "campaign_page_capture.json", data)
        (RAW / "ui" / country / "campaign_page_text.txt").parent.mkdir(parents=True, exist_ok=True)
        (RAW / "ui" / country / "campaign_page_text.txt").write_text(data.get("bodyText", ""), encoding="utf-8")
        shot = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
        if "data" in shot:
            (RAW / "ui" / country / "campaign_page.png").write_bytes(base64.b64decode(shot["data"]))
        lines = data.get("lines", [])
        snippets = []
        for idx, line in enumerate(lines):
            if target["campaign_name"] in line or target["campaign_id"] in line:
                snippets.append({"index": idx, "lines": lines[max(0, idx - 8) : idx + 28]})
        return {
            "url": data.get("url"),
            "title": data.get("title"),
            "bodyTextLength": data.get("bodyTextLength"),
            "campaign_snippets": snippets,
        }
    finally:
        cdp.close()
        close_tab(tab["id"])


def main() -> int:
    page = get_ads_page()
    rpc_cdp = CDP(page["webSocketDebuggerUrl"])
    rpc_cdp.call("Runtime.enable")
    try:
        timestamp = datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds")
        results = []
        for target in TARGETS:
            rpc_state = read_rpc_state(rpc_cdp, target)
            ui_state = capture_campaign_ui(target)
            campaign = rpc_state["campaign"]
            adgroups = rpc_state["adgroups"]
            enabled = [row for row in adgroups if row["ad_group_status_code"] == 1]
            target_enabled = [
                row
                for row in enabled
                if row["ad_group_id"] == target["target_adgroup_id"]
                and row["ad_group_name"] == AD_GROUP_NAME
            ]
            checks = {
                "campaign_enabled": campaign["campaign_status_code"] == 3,
                "budget_unchanged_2_usd": campaign["budget_micros"] == target["budget_micros"],
                "search_only": campaign["target_google_search"] is True
                and campaign["target_content_network"] is False
                and campaign["target_youtube_video"] is False,
                "presence_only": campaign["geo_target_type_setting_raw"] == {"16": 18, "17": 18},
                "only_target_adgroup_enabled": len(enabled) == 1 and len(target_enabled) == 1,
                "no_campaign_conversion_override": (
                    len(rpc_state["conversion_config"].get("1", [])) == 1
                    and rpc_state["conversion_config"]["1"][0].get("3") is False
                ),
            }
            save_json(RAW / "checks" / target["country"] / "monitor_checks.json", checks)
            results.append(
                {
                    "country": target["country"],
                    "campaign_id": target["campaign_id"],
                    "campaign_name": target["campaign_name"],
                    "campaign_status": campaign["campaign_status"],
                    "budget_usd": campaign["budget_usd"],
                    "enabled_adgroups": enabled,
                    "paused_adgroup_count": len([row for row in adgroups if row["ad_group_status_code"] == 2]),
                    "checks": checks,
                    "ui": ui_state,
                }
            )
        summary = {
            "status": "DONE_READONLY_GB_CA_AU_MONITORING_PASSED" if all(all(r["checks"].values()) for r in results) else "READONLY_GB_CA_AU_MONITORING_CHECK_FAILED",
            "timestamp_eastern": timestamp,
            "note": "Immediate monitor pass is mostly status/safety readback; fresh performance metrics may lag just after enablement.",
            "results": results,
        }
        save_json(RAW / "monitoring_summary.json", summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0 if summary["status"] == "DONE_READONLY_GB_CA_AU_MONITORING_PASSED" else 2
    finally:
        rpc_cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
