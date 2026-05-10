#!/usr/bin/env python3
"""Read back and, when needed, repair approved paused non-US Search campaign targeting.

This is scoped to the owner-approved paused non-US Search TEST BUILD. The only
write it can perform is setting geo_target_type_setting to presence-only for a
new paused DLM_* campaign that was just imported from the approved split files.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved"
SPLIT_DIR = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"
CAMPAIGN_PREFIX = "DLM_{country}_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"

COUNTRIES = ["CA", "AU", "CH", "DK", "DE", "NL", "SE", "FR", "BE", "ES", "IT", "PL", "CZ", "RO", "PT", "GR", "GB"]
STATUS = {5: "PAUSED"}
CHANNEL = {1: "SEARCH"}
GEO = {
    16: "DONT_CARE",
    17: "AREA_OF_INTEREST",
    18: "LOCATION_OF_PRESENCE",
}


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
        self.ws = websocket.create_connection(ws_url, timeout=20, suppress_origin=True)
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


def json_get(path: str):
    with urllib.request.urlopen(f"{CDP_BASE}{path}", timeout=20) as response:
        return json.load(response)


def get_ads_page() -> dict:
    pages = json_get("/json/list")
    for page in pages:
        if page.get("type") == "page" and "ads.google.com" in page.get("url", ""):
            return page
    raise RuntimeError("No logged-in Google Ads CDP page found")


def rpc(cdp: CDP, service: str, method: str, request: dict) -> dict:
    endpoint = f"https://ads.google.com/aw_cm/editing/_/rpc/{service}/{method}?authuser=0&xt=awn&rpcTrackingId={urllib.parse.quote(service + '.' + method + ':1')}"
    expression = f"""
(async () => {{
  const token = window.$acx && window.$acx.xsrfToken;
  if (!token) return {{status: 0, ok: false, tokenLen: 0, text: 'missing xsrf token'}};
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
        raise RuntimeError(json.dumps(response, ensure_ascii=False, indent=2))
    return response


def campaign_list_request() -> dict:
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
        "2": [],
    }
    return request


def mutate_presence_request(campaign_id: str) -> dict:
    request = dict(BASE_CONTEXT)
    request["2"] = [
        {
            "1": 5,
            "2": ["geo_target_type_setting"],
            "3": {
                "1": CUSTOMER_ID,
                "2": campaign_id,
                "43": {"16": 18, "17": 18},
            },
        }
    ]
    return request


def parse_campaign(raw: dict, name: str) -> dict | None:
    matches = [row for row in raw.get("1", []) if row.get("11") == name]
    if not matches:
        return None
    if len(matches) > 1:
        raise RuntimeError(f"Expected one {name} campaign, found {len(matches)}")
    row = matches[0]
    geo = row.get("43", {})
    return {
        "customer_id": row.get("1"),
        "campaign_id": row.get("2"),
        "campaign_name": row.get("11"),
        "campaign_status_code": row.get("12"),
        "campaign_status_interpreted": STATUS.get(row.get("12"), f"UNKNOWN_{row.get('12')}"),
        "advertising_channel_type_code": row.get("15"),
        "advertising_channel_type_interpreted": CHANNEL.get(row.get("15"), f"UNKNOWN_{row.get('15')}"),
        "budget_micros": row.get("17"),
        "budget_usd": int(row["17"]) / 1_000_000 if row.get("17") and row["17"].isdigit() else None,
        "currency": row.get("31", {}).get("9"),
        "target_content_network": row.get("20"),
        "target_google_search": row.get("21"),
        "target_search_network": row.get("22"),
        "target_youtube_video": row.get("23"),
        "geo_target_type_setting_raw": geo,
        "positive_geo_target_type_interpreted": GEO.get(geo.get("16"), f"UNKNOWN_{geo.get('16')}"),
        "negative_geo_target_type_interpreted": GEO.get(geo.get("17"), f"UNKNOWN_{geo.get('17')}"),
        "languages": row.get("50"),
        "raw": row,
    }


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")


def read_campaign(cdp: CDP, country: str, label: str) -> tuple[dict, dict, dict | None]:
    name = CAMPAIGN_PREFIX.format(country=country)
    request = campaign_list_request()
    response = rpc(cdp, "CampaignService", "List", request)
    raw = json.loads(response["text"])
    summary = parse_campaign(raw, name)
    out_dir = PACKET / f"raw/after-readbacks/{country}_campaign_rpc"
    save_json(out_dir / f"{label}_request.json", request)
    save_json(out_dir / f"{label}_response.json", response)
    save_json(out_dir / f"{label}_summary.json", summary or {"campaign_name": name, "found": False})
    return request, response, summary


def validate_summary(summary: dict):
    expected_budget_micros = expected_budget_for_country(summary["campaign_name"].split("_")[1])
    checks = {
        "campaign_status": summary["campaign_status_code"] == 5,
        "channel": summary["advertising_channel_type_code"] == 1,
        "budget": summary["budget_micros"] == expected_budget_micros,
        "search": summary["target_google_search"] is True,
        "content": summary["target_content_network"] is False,
        "youtube": summary["target_youtube_video"] is False,
        "positive_presence": summary["geo_target_type_setting_raw"].get("16") == 18,
        "negative_presence": summary["geo_target_type_setting_raw"].get("17") == 18,
    }
    if not all(checks.values()):
        raise RuntimeError(json.dumps({"checks": checks, "summary": summary}, indent=2, ensure_ascii=False))


def expected_budget_for_country(country: str) -> str:
    csv_path = SPLIT_DIR / f"{country}_intl_search_paused_draft_web_bulk.csv"
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        row = next(csv.DictReader(handle))
    return str(int(round(float(row["Budget"]) * 1_000_000)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("country", choices=COUNTRIES)
    parser.add_argument("--expect-absent", action="store_true")
    parser.add_argument("--repair-presence", action="store_true")
    args = parser.parse_args()

    page = get_ads_page()
    cdp = CDP(page["webSocketDebuggerUrl"])
    cdp.call("Runtime.enable")
    try:
        _, _, summary = read_campaign(cdp, args.country, "initial")
        if args.expect_absent:
            if summary:
                raise RuntimeError(f"{args.country} campaign already exists: {summary['campaign_id']}")
            print(f"[{args.country}] campaign absent before import")
            return 0
        if not summary:
            raise RuntimeError(f"{args.country} campaign not found")

        if args.repair_presence and (
            summary["geo_target_type_setting_raw"].get("16") != 18
            or summary["geo_target_type_setting_raw"].get("17") != 18
        ):
            request = mutate_presence_request(summary["campaign_id"])
            response = rpc(cdp, "CampaignService", "Mutate", request)
            out_dir = PACKET / f"raw/after-readbacks/{args.country}_campaign_rpc"
            save_json(out_dir / "presence_repair_request.json", request)
            save_json(out_dir / "presence_repair_response.json", response)
            time.sleep(2)
            _, _, summary = read_campaign(cdp, args.country, "post_presence_repair")

        validate_summary(summary)
        final = dict(summary)
        final.pop("raw", None)
        save_json(PACKET / f"raw/after-readbacks/{args.country}_campaign_rpc/final_validated_summary.json", final)
        print(json.dumps(final, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    finally:
        cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
