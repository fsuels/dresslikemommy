#!/usr/bin/env python3
"""Read-only Google Ads performance/search-term route probe for GB/CA/AU.

This opens reporting pages only. It does not click controls, save, apply,
download, enable, pause, or mutate any Google Ads entity.
"""

from __future__ import annotations

import base64
import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websocket


PACKET = Path("/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring")
RAW = PACKET / "raw" / "perf-search-term-probe"
CDP_BASE = "http://127.0.0.1:9222"
CUSTOMER_ID = "220823493"
AUTH_PARAMS = "ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493&__c=9710510557&authuser=0"

TARGETS = [
    {"country": "GB", "campaign_id": "23838895360", "ad_group_id": "194138528537", "name": "DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"},
    {"country": "CA", "campaign_id": "23834423669", "ad_group_id": "196679079575", "name": "DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"},
    {"country": "AU", "campaign_id": "23834424182", "ad_group_id": "198852670520", "name": "DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"},
]

ROUTES = [
    ("campaigns", "/aw/campaigns?{auth}&campaignId={campaign_id}"),
    ("adgroups", "/aw/adgroups?{auth}&campaignId={campaign_id}"),
    ("keywords", "/aw/keywords?{auth}&campaignId={campaign_id}&adGroupId={ad_group_id}"),
    ("searchterms", "/aw/searchterms?{auth}&campaignId={campaign_id}&adGroupId={ad_group_id}"),
    ("keywords_searchterms", "/aw/keywords/searchterms?{auth}&campaignId={campaign_id}&adGroupId={ad_group_id}"),
    ("search_terms_hyphen", "/aw/search-terms?{auth}&campaignId={campaign_id}&adGroupId={ad_group_id}"),
]

STALE_FILTER_PATTERNS = [
    re.compile(r'Keyword:\s*"human hair wigs"', re.I),
]


class CDP:
    def __init__(self, ws_url: str) -> None:
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
        response = self.call("Runtime.evaluate", {"expression": expression, "awaitPromise": True, "returnByValue": True})
        return response.get("result", {}).get("value")

    def close(self) -> None:
        self.ws.close()


def cdp_json(path: str, *, method: str = "GET"):
    with urllib.request.urlopen(urllib.request.Request(f"{CDP_BASE}{path}", method=method), timeout=20) as response:
        return json.load(response)


def new_tab(url: str) -> dict:
    return cdp_json(f"/json/new?{urllib.parse.quote(url, safe='')}", method="PUT")


def close_tab(target_id: str) -> None:
    try:
        cdp_json(f"/json/close/{target_id}")
    except Exception:
        pass


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def clean_lines(text: str) -> list[str]:
    return [line.strip() for line in re.split(r"\n+", text or "") if line.strip()]


def filter_lines(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if "filter" in line.lower() or re.match(r'^(Keyword|Search term|Campaign|Ad group):', line, re.I)
    ]


def stale_filter_hits(lines: list[str]) -> list[str]:
    hits = []
    for line in lines:
        if any(pattern.search(line) for pattern in STALE_FILTER_PATTERNS):
            hits.append(line)
    return hits


def capture_route(target: dict, route_label: str, route_template: str) -> dict:
    relative = route_template.format(auth=AUTH_PARAMS, campaign_id=target["campaign_id"], ad_group_id=target["ad_group_id"])
    url = f"https://ads.google.com{relative}"
    tab = new_tab(url)
    cdp = CDP(tab["webSocketDebuggerUrl"])
    out_dir = RAW / target["country"] / route_label
    try:
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Page.bringToFront")
        time.sleep(9)
        data = cdp.eval(
            """
(() => {
  const text = document.body ? document.body.innerText : '';
  const lines = text.split(/\\n+/).map(s => s.trim()).filter(Boolean);
  return {
    title: document.title || '',
    url: location.href,
    readyState: document.readyState,
    timestamp: new Date().toISOString(),
    textLength: text.length,
    bodyText: text,
    lines: lines.slice(0, 500),
    hasSearchTermWords: /search terms?|搜索字词|searches/i.test(text),
    hasMetricsWords: /(Clicks|Impr\\.|Impressions|Cost|Conversions|Conv\\. value|Original conv\\. value)/i.test(text),
    hasNoDataWords: /(No data|No statistics|没有数据|0\\s+rows|There are no|Nothing to show)/i.test(text),
    is404: /Error 404|Not Found/i.test(document.title + '\\n' + text)
  };
})()
"""
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        save_json(out_dir / "capture.json", data)
        (out_dir / "visible_text.txt").write_text(data.get("bodyText", ""), encoding="utf-8")
        try:
            shot = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
            if shot.get("data"):
                (out_dir / "screenshot.png").write_bytes(base64.b64decode(shot["data"]))
        except Exception as exc:
            (out_dir / "screenshot_error.txt").write_text(str(exc), encoding="utf-8")

        lines = data.get("lines") or []
        active_filter_lines = filter_lines(lines)
        stale_filters = stale_filter_hits(lines)
        metric_context = []
        for idx, line in enumerate(lines):
            if re.search(r"Clicks|Impr\.|Impressions|Cost|Conversions|Conv\. value|Original conv\. value|Avg\. CPC", line, re.I):
                metric_context.append({"index": idx, "lines": lines[max(0, idx - 5): idx + 24]})
        target_context = []
        for idx, line in enumerate(lines):
            if target["name"] in line or target["campaign_id"] in line:
                target_context.append({"index": idx, "lines": lines[max(0, idx - 10): idx + 40]})
        return {
            "country": target["country"],
            "route": route_label,
            "requested_url": url,
            "final_url": data.get("url"),
            "title": data.get("title"),
            "text_length": data.get("textLength"),
            "is_404": data.get("is404"),
            "has_search_term_words": data.get("hasSearchTermWords"),
            "has_metrics_words": data.get("hasMetricsWords"),
            "has_no_data_words": data.get("hasNoDataWords"),
            "active_filter_lines": active_filter_lines[:20],
            "has_stale_human_hair_filter": bool(stale_filters),
            "stale_filter_hits": stale_filters[:10],
            "search_terms_actionable": route_label == "keywords_searchterms" and not stale_filters and not data.get("is404"),
            "search_terms_actionability_note": (
                "blocked_by_stale_human_hair_filter"
                if route_label == "keywords_searchterms" and stale_filters
                else "route_not_search_terms" if route_label != "keywords_searchterms"
                else "search_terms_route_available_no_known_stale_filter"
            ),
            "metric_context": metric_context[:4],
            "target_context": target_context[:3],
            "evidence_dir": str(out_dir),
        }
    finally:
        cdp.close()
        close_tab(tab["id"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only GB/CA/AU Google Ads performance/search-term route probe.")
    parser.add_argument(
        "--routes",
        default=",".join(label for label, _ in ROUTES),
        help="Comma-separated route labels to probe. Example: --routes keywords_searchterms",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested_routes = {route.strip() for route in args.routes.split(",") if route.strip()}
    selected_routes = [(label, template) for label, template in ROUTES if label in requested_routes]
    all_route_labels = [label for label, _ in ROUTES]
    unknown_routes = sorted(requested_routes.difference(label for label, _ in ROUTES))
    if unknown_routes:
        raise SystemExit(f"Unknown route label(s): {', '.join(unknown_routes)}")
    timestamp = datetime.now(ZoneInfo("America/New_York")).isoformat(timespec="seconds")
    results = []
    for target in TARGETS:
        for route_label, route_template in selected_routes:
            results.append(capture_route(target, route_label, route_template))
            time.sleep(2)
    summary = {
        "status": "DONE_READONLY_ROUTE_PROBE_NO_ADS_WRITES",
        "timestamp_eastern": timestamp,
        "route_labels": [label for label, _ in selected_routes],
        "guardrails": [
            "read-only page opens only",
            "no Save/Apply/Enable/Pause clicks",
            "no budget, bid, status, product, feed, Merchant, Pinterest, Shopify, or conversion-goal changes",
        ],
        "results": results,
    }
    if [label for label, _ in selected_routes] == all_route_labels:
        summary_path = RAW / "gb_ca_au_perf_search_terms_route_probe_summary.json"
    else:
        route_slug = "-".join(label for label, _ in selected_routes)
        summary_path = RAW / f"gb_ca_au_perf_search_terms_route_probe_summary__{route_slug}.json"
    summary["summary_path"] = str(summary_path)
    save_json(summary_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
