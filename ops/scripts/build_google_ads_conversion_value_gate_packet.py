#!/usr/bin/env python3
"""Build a read-only Google Ads purchase conversion-value gate packet.

The packet is intentionally conservative. It records only sanitized browser
evidence from the logged-in Google Ads conversion screens and blocks Ads work
unless the account has current proof that purchase conversions are recording
with non-zero value.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any

import websocket


ROOT = Path("dresslikemommy-growth-2026")
DEFAULT_OUTPUT_DIR = ROOT / "02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate"
DEFAULT_CDP_PORT = 9222
DEFAULT_CUSTOMER_ID = "220823493"
DEFAULT_TARGET_CONVERSION_NAME = "Google Shopping App Purchase"

PURCHASE_CATEGORY_ID = 1
SOURCE_NAMES = {
    1: "Website",
    2: "Website (Google Analytics (UA))",
    21: "App",
    32: "Website (Google Analytics (GA4))",
}


class CdpClient:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(websocket_url, timeout=30, suppress_origin=True)
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def call(self, method: str, params: dict[str, Any] | None = None, timeout_seconds: int = 30) -> dict[str, Any]:
        message_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        start = time.time()
        while time.time() - start < timeout_seconds:
            event = json.loads(self.ws.recv())
            if event.get("id") == message_id:
                return event
        raise TimeoutError(f"Timed out waiting for CDP response {message_id} ({method})")


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def decimal_value(value: object) -> float:
    text = clean(value).replace(",", "")
    if not text:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def open_page(cdp_port: int, url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe="")
    request = urllib.request.Request(f"http://127.0.0.1:{cdp_port}/json/new?{encoded}", method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def find_or_open_ads_page(cdp_port: int, customer_id: str) -> dict[str, Any]:
    pages = get_json(f"http://127.0.0.1:{cdp_port}/json/list")
    for page in pages:
        if page.get("type") == "page" and "ads.google.com" in page.get("url", ""):
            return page
    return open_page(cdp_port, f"https://ads.google.com/aw/conversions?ocid={customer_id}")


def runtime_value(client: CdpClient, expression: str, timeout_seconds: int = 30) -> Any:
    response = client.call(
        "Runtime.evaluate",
        {"expression": expression, "returnByValue": True, "awaitPromise": True},
        timeout_seconds=timeout_seconds,
    )
    result = response.get("result", {}).get("result", {})
    if "value" in result:
        return result["value"]
    return None


def capture_page(client: CdpClient) -> dict[str, Any]:
    expression = """
(() => {
  const parseJson = (value) => {
    if (!value) return null;
    try { return JSON.parse(value); } catch (error) { return null; }
  };
  return {
    url: location.href,
    title: document.title,
    text: document.body ? document.body.innerText : "",
    allEnabledConversions: parseJson(window.conversions_data && window.conversions_data.ALL_ENABLED_CONVERSIONS),
    automaticConversionGoal: parseJson(window.conversions_data && window.conversions_data.AUTOMATIC_CONVERSION_GOAL)
  };
})()
"""
    return runtime_value(client, expression, timeout_seconds=60) or {}


def wait_for_text(client: CdpClient, required: list[str], timeout_seconds: int = 45) -> dict[str, Any]:
    start = time.time()
    latest: dict[str, Any] = {}
    while time.time() - start < timeout_seconds:
        latest = capture_page(client)
        text = latest.get("text", "")
        if all(item in text for item in required):
            return latest
        time.sleep(2)
    return latest


def navigate(client: CdpClient, url: str) -> None:
    client.call("Page.enable")
    client.call("Runtime.enable")
    client.call("Page.navigate", {"url": url}, timeout_seconds=10)


def sanitize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    keep = []
    for key in ("ocid", "ctId"):
        if key in query:
            keep.append((key, query[key][0]))
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(keep)))


def sanitize_text_excerpt(text: str, max_chars: int = 1500) -> str:
    text = re.sub(r"[\w.+-]+@[\w.-]+\.\w+", "[redacted-email]", text)
    text = re.sub(r"(__u|__c|euid|uscid|authuser)=[^&\s]+", r"\1=[redacted]", text)
    return text[:max_chars]


def parse_date_range(text: str) -> dict[str, str]:
    match = re.search(
        r"Last\s+7\s+days\s+([A-Za-z]{3,9}\s+\d{1,2})\s*[\u2013-]\s*(\d{1,2}),\s*(\d{4})",
        text,
    )
    if not match:
        return {"label": "", "start": "", "end": ""}
    month_day, end_day, year = match.groups()
    start_text = f"{month_day}, {year}"
    end_month = month_day.split()[0]
    end_text = f"{end_month} {end_day}, {year}"
    return {"label": "Last 7 days", "start": start_text, "end": end_text}


def parse_purchase_goal(text: str) -> dict[str, object]:
    normalized = clean(text)
    purchase_results = None
    match = re.search(r"Group 3 goals Results ([0-9,.]+) Purchases ([0-9,.]+)", normalized)
    if match:
        purchase_results = decimal_value(match.group(2))
    active = bool(
        re.search(
            r"Account-default\s+.*?Purchase\s+Campaigns\s+73 of 73\s+"
            r"Primary conversion actions\s+1\s+Status\s+.*?Active",
            normalized,
        )
    )
    return {
        "purchase_goal_active": active,
        "purchase_goal_campaigns": "73 of 73" if "Campaigns 73 of 73" in normalized else "",
        "purchase_goal_primary_conversion_actions": 1 if "Primary conversion actions 1" in normalized else None,
        "purchase_goal_results": purchase_results,
    }


def stats_from_row(row: dict[str, Any]) -> dict[str, object]:
    raw_values = []
    stats = row.get("200")
    if isinstance(stats, dict):
        raw_values = stats.get("1") or []
    return {
        "last_conversion_date_raw": clean(raw_values[0]) if len(raw_values) > 0 else "",
        "all_conversions_raw": decimal_value(raw_values[1]) if len(raw_values) > 1 else 0.0,
        "all_conversion_value_raw": decimal_value(raw_values[2]) if len(raw_values) > 2 else 0.0,
        "last_received_request_time_raw": clean(raw_values[3]) if len(raw_values) > 3 else "",
    }


def normalize_conversion_row(row: dict[str, Any]) -> dict[str, object]:
    source_id = row.get("11")
    return {
        "conversion_action_id": clean(row.get("1")),
        "conversion_action": clean(row.get("3")),
        "conversion_source": SOURCE_NAMES.get(source_id, f"raw_source_{source_id}"),
        "action_optimization": "Primary" if row.get("9") is True else "Secondary",
        "count": "Every" if row.get("7") == 1 else clean(row.get("7")),
        "included_in_account_level_goals": bool(row.get("77")),
        "category_id": row.get("10"),
        "currency": clean(row.get("28")),
        **stats_from_row(row),
    }


def purchase_rows(payload: dict[str, Any]) -> list[dict[str, object]]:
    rows = payload.get("1", []) if isinstance(payload, dict) else []
    out = [
        normalize_conversion_row(row)
        for row in rows
        if isinstance(row, dict) and row.get("10") == PURCHASE_CATEGORY_ID
    ]
    return sorted(out, key=lambda row: clean(row["conversion_action"]))


def parse_setting(lines: list[str], label: str) -> str:
    try:
        start = lines.index(label) + 1
    except ValueError:
        return ""
    ignored = {"", "Not editable"}
    values = []
    for line in lines[start:]:
        if line in ignored:
            continue
        if line in {
            "Conversion name",
            "Date created",
            "Action optimization",
            "Value",
            "Source",
            "Count",
            "Click-through conversion window",
            "Engaged-view conversion window",
            "View-through conversion window",
            "Attribution",
            "Enhanced Conversions",
            "Tag setup",
        }:
            break
        values.append(line)
        if values:
            break
    return clean(" ".join(values))


def parse_detail_settings(text: str) -> dict[str, str]:
    lines = [line.strip() for line in text.splitlines()]
    return {
        "conversion_name": parse_setting(lines, "Conversion name"),
        "date_created": parse_setting(lines, "Date created"),
        "action_optimization": parse_setting(lines, "Action optimization"),
        "value_setting": parse_setting(lines, "Value"),
        "source": parse_setting(lines, "Source"),
        "count": parse_setting(lines, "Count"),
        "click_through_conversion_window": parse_setting(lines, "Click-through conversion window"),
        "engaged_view_conversion_window": parse_setting(lines, "Engaged-view conversion window"),
        "view_through_conversion_window": parse_setting(lines, "View-through conversion window"),
        "attribution": parse_setting(lines, "Attribution"),
        "enhanced_conversions": parse_setting(lines, "Enhanced Conversions"),
    }


def capture_from_cdp(cdp_port: int, customer_id: str, target_conversion_name: str) -> dict[str, Any]:
    page = find_or_open_ads_page(cdp_port, customer_id)
    client = CdpClient(page["webSocketDebuggerUrl"])
    try:
        list_url = f"https://ads.google.com/aw/conversions?ocid={customer_id}"
        navigate(client, list_url)
        list_capture = wait_for_text(
            client,
            ["Conversions", "Last 7 days", "All your goals", "Group 3 goals", "Account-default"],
            timeout_seconds=60,
        )
        rows = purchase_rows(list_capture.get("allEnabledConversions") or {})
        target_rows = [row for row in rows if row["conversion_action"] == target_conversion_name]
        target_id = clean(target_rows[0]["conversion_action_id"]) if target_rows else ""
        detail_capture: dict[str, Any] = {}
        if target_id:
            detail_url = (
                f"https://ads.google.com/aw/conversions/detail?ocid={customer_id}&ctId={target_id}"
                "&showWebpagesTab=true&showDiagnosticsTab=true&showStoreDiagnosticsTab=false"
            )
            navigate(client, detail_url)
            detail_capture = wait_for_text(
                client,
                ["Conversion name", target_conversion_name, "Use different values", "Every conversion"],
                timeout_seconds=90,
            )
        return {
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "source": "READ_ONLY_GOOGLE_ADS_BROWSER_CDP",
            "list_page": {
                "url": sanitize_url(clean(list_capture.get("url"))),
                "title": clean(list_capture.get("title")),
                "date_range": parse_date_range(list_capture.get("text", "")),
                "purchase_goal": parse_purchase_goal(list_capture.get("text", "")),
                "sanitized_visible_text_excerpt": sanitize_text_excerpt(list_capture.get("text", "")),
            },
            "target_detail_page": {
                "url": sanitize_url(clean(detail_capture.get("url"))),
                "title": clean(detail_capture.get("title")),
                "settings": parse_detail_settings(detail_capture.get("text", "")),
                "sanitized_visible_text_excerpt": sanitize_text_excerpt(detail_capture.get("text", "")),
            },
            "purchase_conversion_actions": rows,
        }
    finally:
        client.close()


def evaluate_gate(capture: dict[str, Any], target_conversion_name: str) -> dict[str, object]:
    purchase_goal = capture.get("list_page", {}).get("purchase_goal", {})
    rows = capture.get("purchase_conversion_actions", [])
    target_rows = [
        row
        for row in rows
        if row.get("conversion_action") == target_conversion_name
    ]
    primary_account_level_purchase_rows = [
        row
        for row in rows
        if row.get("action_optimization") == "Primary" and row.get("included_in_account_level_goals") is True
    ]
    target = target_rows[0] if target_rows else {}
    purchase_results = purchase_goal.get("purchase_goal_results")
    current_purchase_results_passed = isinstance(purchase_results, (int, float)) and purchase_results > 0
    target_value_raw = decimal_value(target.get("all_conversion_value_raw")) if target else 0.0
    target_conversions_raw = decimal_value(target.get("all_conversions_raw")) if target else 0.0
    historical_value_present = target_conversions_raw > 0 and target_value_raw > 0
    settings = capture.get("target_detail_page", {}).get("settings", {})
    value_setting = clean(settings.get("value_setting"))
    variable_value_setting = "Use different values" in value_setting
    target_value_evidence_present = variable_value_setting or historical_value_present

    gate_passed = bool(
        purchase_goal.get("purchase_goal_active")
        and len(primary_account_level_purchase_rows) == 1
        and target_rows
        and target.get("action_optimization") == "Primary"
        and target.get("included_in_account_level_goals") is True
        and target_value_evidence_present
        and current_purchase_results_passed
    )
    blockers: list[str] = []
    if not purchase_goal.get("purchase_goal_active"):
        blockers.append("Purchase goal is not proven Active in the visible Google Ads summary.")
    if len(primary_account_level_purchase_rows) != 1:
        blockers.append("Exactly one primary account-level purchase action is not proven.")
    if not target_rows:
        blockers.append(f"Target purchase action `{target_conversion_name}` was not found.")
    elif target.get("action_optimization") != "Primary" or target.get("included_in_account_level_goals") is not True:
        blockers.append(f"Target purchase action `{target_conversion_name}` is not the primary account-level action.")
    if not target_value_evidence_present:
        blockers.append("No target purchase action value setting or historical value evidence is proven.")
    if not current_purchase_results_passed:
        blockers.append("Visible Purchase results are 0 for the current Google Ads date range.")

    return {
        "purchase_conversion_value_gate_status": (
            "PASS_PURCHASE_CONVERSION_VALUE_RECORDING"
            if gate_passed
            else "BLOCKED_PURCHASE_CONVERSION_VALUE_NOT_RECORDING_RECENTLY"
        ),
        "purchase_conversion_value_gate_passed": gate_passed,
        "target_conversion_action": target_conversion_name,
        "purchase_goal_active": bool(purchase_goal.get("purchase_goal_active")),
        "purchase_goal_results": purchase_results,
        "primary_account_level_purchase_action_count": len(primary_account_level_purchase_rows),
        "target_is_primary_account_level_purchase_action": bool(
            target
            and target.get("action_optimization") == "Primary"
            and target.get("included_in_account_level_goals") is True
        ),
        "target_variable_value_setting_proven": variable_value_setting,
        "target_value_evidence_present": target_value_evidence_present,
        "target_historical_value_present_in_raw_stats": historical_value_present,
        "target_last_conversion_date_raw": target.get("last_conversion_date_raw", ""),
        "target_all_conversions_raw": target_conversions_raw,
        "target_all_conversion_value_raw": target_value_raw,
        "current_purchase_results_passed": current_purchase_results_passed,
        "blockers": blockers,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def render_report(summary: dict[str, Any]) -> str:
    gate = summary["gate"]
    capture = summary["capture"]
    list_page = capture.get("list_page", {})
    detail_settings = capture.get("target_detail_page", {}).get("settings", {})
    rows = capture.get("purchase_conversion_actions", [])
    lines = [
        "# Google Ads Purchase Conversion-Value Gate",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Decision",
        "",
        f"`{gate['purchase_conversion_value_gate_status']}`",
        "",
        "No Google Ads settings were changed. This packet is read-only evidence for whether Ads work can become actionable.",
        "",
        "## Current Evidence",
        "",
        f"- Source page: `{list_page.get('title', '')}`",
        f"- Source URL: `{list_page.get('url', '')}`",
        f"- Date range: `{list_page.get('date_range', {})}`",
        f"- Purchase goal active: `{gate['purchase_goal_active']}`",
        f"- Purchase results in visible date range: `{gate['purchase_goal_results']}`",
        f"- Primary account-level purchase actions: `{gate['primary_account_level_purchase_action_count']}`",
        f"- Target action primary/account-level: `{gate['target_is_primary_account_level_purchase_action']}`",
        f"- Target value setting proves dynamic values: `{gate['target_variable_value_setting_proven']}`",
        f"- Target value evidence present: `{gate['target_value_evidence_present']}`",
        f"- Target raw historical conversions/value present: `{gate['target_historical_value_present_in_raw_stats']}`",
        f"- Target raw last conversion date: `{gate['target_last_conversion_date_raw']}`",
        "",
        "## Target Action Settings",
        "",
        f"- Conversion name: `{detail_settings.get('conversion_name', '')}`",
        f"- Action optimization: `{detail_settings.get('action_optimization', '')}`",
        f"- Value: `{detail_settings.get('value_setting', '')}`",
        f"- Source: `{detail_settings.get('source', '')}`",
        f"- Count: `{detail_settings.get('count', '')}`",
        f"- Click-through window: `{detail_settings.get('click_through_conversion_window', '')}`",
        "",
        "## Purchase Conversion Actions",
        "",
        "| Conversion action | Source | Optimization | Included in account goals | Raw last conversion | Raw all conv. | Raw all conv. value |",
        "| --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.get('conversion_action', '')} | "
            f"{row.get('conversion_source', '')} | "
            f"{row.get('action_optimization', '')} | "
            f"{row.get('included_in_account_level_goals', '')} | "
            f"{row.get('last_conversion_date_raw', '')} | "
            f"{row.get('all_conversions_raw', '')} | "
            f"{row.get('all_conversion_value_raw', '')} |"
        )
    lines.extend(
        [
            "",
            "## Blockers",
            "",
            *(f"- {blocker}" for blocker in gate.get("blockers", [])),
            "",
            "## Gate Rule",
            "",
            "The gate passes only when the Purchase goal is active, exactly one primary account-level purchase action is present, the target purchase action uses transaction-specific values, and current Google Ads evidence shows non-zero purchase results/value. Historical raw value is useful context but is not enough to restart or build actionable Ads work.",
            "",
        ]
    )
    return "\n".join(lines)


def build_packet(capture: dict[str, Any], output_dir: Path, target_conversion_name: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    gate = evaluate_gate(capture, target_conversion_name)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_GOOGLE_ADS_PURCHASE_CONVERSION_VALUE_GATE",
        "target_conversion_action": target_conversion_name,
        "current_date": date.today().isoformat(),
        "gate": gate,
        "capture": capture,
    }
    files = {
        "summary": output_dir / "google_ads_conversion_value_gate_summary.json",
        "capture": output_dir / "sanitized_google_ads_conversion_capture.json",
        "purchase_rows": output_dir / "purchase_conversion_actions.csv",
        "report": output_dir / "google_ads_conversion_value_gate_report.md",
    }
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files["capture"].write_text(json.dumps(capture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = capture.get("purchase_conversion_actions", [])
    write_csv(
        files["purchase_rows"],
        [
            "conversion_action_id",
            "conversion_action",
            "conversion_source",
            "action_optimization",
            "count",
            "included_in_account_level_goals",
            "category_id",
            "currency",
            "last_conversion_date_raw",
            "all_conversions_raw",
            "all_conversion_value_raw",
            "last_received_request_time_raw",
        ],
        rows,
    )
    files["report"].write_text(render_report(summary), encoding="utf-8")
    summary["files"] = {key: str(path) for key, path in files.items()}
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    parser.add_argument("--customer-id", default=DEFAULT_CUSTOMER_ID)
    parser.add_argument("--target-conversion-name", default=DEFAULT_TARGET_CONVERSION_NAME)
    parser.add_argument("--input-capture", type=Path, help="Use a sanitized capture JSON instead of reading Chrome CDP.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.input_capture:
        capture = json.loads(args.input_capture.read_text(encoding="utf-8"))
    else:
        capture = capture_from_cdp(args.cdp_port, args.customer_id, args.target_conversion_name)
    summary = build_packet(capture, args.output_dir, args.target_conversion_name)
    print(
        json.dumps(
            {
                "output": summary["files"]["summary"],
                **summary["gate"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
