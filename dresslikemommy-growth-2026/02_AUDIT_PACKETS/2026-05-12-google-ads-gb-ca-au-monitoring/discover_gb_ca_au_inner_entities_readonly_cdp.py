#!/usr/bin/env python3
"""Read-only discovery of GB/CA/AU exact Search keyword/ad entity IDs.

No mutate RPCs are sent. This prepares the next exact approval gate by proving
the narrow inner entities that remain paused inside the already-enabled exact
ad groups.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"

TARGETS = [
    {"country": "GB", "campaign_id": "23838895360", "ad_group_id": "194138528537"},
    {"country": "CA", "campaign_id": "23834423669", "ad_group_id": "196679079575"},
    {"country": "AU", "campaign_id": "23834424182", "ad_group_id": "198852670520"},
]

CRITERION_STATUS = {2: "ENABLED", 3: "PAUSED", 4: "REMOVED"}
AD_STATUS = {1: "ENABLED", 2: "PAUSED", 3: "REMOVED"}

BASE_CONTEXT = {
    "1": {
        "3": {"1": CUSTOMER_ID},
        "6": "-25200000",
        "7": "1493889124247",
        "8": "{\"1\":[{\"1\":\"1000004\",\"2\":\"TREATMENT\"}]}",
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


def main() -> int:
    page = get_ads_page()
    cdp = CDP(page["webSocketDebuggerUrl"])
    cdp.call("Runtime.enable")
    results = []
    try:
        for target in TARGETS:
            country = target["country"]
            keyword_request = list_keywords_request(target["ad_group_id"])
            keyword_response = rpc(cdp, "AdGroupCriterionService", "List", keyword_request)
            keyword_raw = json.loads(keyword_response["text"])
            keywords = parse_keyword_rows(keyword_raw)

            ad_request = list_ads_request(target["ad_group_id"])
            ad_response = rpc(cdp, "AdGroupAdService", "List", ad_request)
            ad_raw = json.loads(ad_response["text"])
            ads = parse_ad_rows(ad_raw)

            save_json(PACKET / f"raw/inner-entity-discovery/{country}/keyword_request.json", keyword_request)
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/keyword_response.json", keyword_response)
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/keyword_rows.json", keywords)
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/ad_request.json", ad_request)
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/ad_response.json", ad_response)
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/ad_rows.json", ads)

            checks = {
                "three_keyword_criteria": len(keywords) == 3,
                "all_keyword_criteria_paused": all(row["status_code"] == 3 for row in keywords),
                "one_ad": len(ads) == 1,
                "ad_paused": len(ads) == 1 and ads[0]["status_code"] == 2,
                "all_urls_country_qualified": all(
                    f"?country={country}" in url
                    for row in keywords + ads
                    for url in row.get("final_urls", [])
                ),
            }
            save_json(PACKET / f"raw/inner-entity-discovery/{country}/inner_entity_checks.json", checks)

            results.append(
                {
                    "country": country,
                    "campaign_id": target["campaign_id"],
                    "ad_group_id": target["ad_group_id"],
                    "keyword_criteria": [
                        {
                            "criterion_id": row["criterion_id"],
                            "status": row["status"],
                            "status_code": row["status_code"],
                            "final_urls": row["final_urls"],
                        }
                        for row in keywords
                    ],
                    "ads": [
                        {
                            "ad_id": row["ad_id"],
                            "status": row["status"],
                            "status_code": row["status_code"],
                            "ad_type_code": row["ad_type_code"],
                            "final_urls": row["final_urls"],
                        }
                        for row in ads
                    ],
                    "checks": checks,
                }
            )

        summary = {
            "status": "DONE_READONLY_INNER_ENTITY_DISCOVERY",
            "note": "No mutate RPCs sent. Keyword text was validated by split-file evidence; RPC discovery provides entity IDs/status/final URLs.",
            "results": results,
        }
        save_json(PACKET / "raw/inner-entity-discovery/inner_entity_discovery_summary.json", summary)
        print(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    finally:
        cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
