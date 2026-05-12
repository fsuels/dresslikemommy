#!/usr/bin/env python3
import asyncio
import base64
import json
import re
import urllib.parse
import urllib.request
import websockets
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
CDP_BASE = "http://127.0.0.1:9222"
ADS_BULK_URL = "https://ads.google.com/aw/bulk/uploads?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493&__c=9710510557&authuser=0"
COUNTRY_FILENAMES = {
    "RO": "RO_intl_search_paused_draft_web_bulk.csv",
    "PT": "PT_intl_search_paused_draft_web_bulk.csv",
    "GR": "GR_intl_search_paused_draft_web_bulk.csv",
    "FR": "FR_intl_search_paused_draft_web_bulk.csv",
    "BE": "BE_intl_search_paused_draft_web_bulk.csv",
}


class CDP:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.next_id = 1
        self.pending = {}
        self.events = asyncio.Queue()

    async def __aenter__(self):
        self.ws = await websockets.connect(self.ws_url, max_size=32 * 1024 * 1024)
        self.reader = asyncio.create_task(self._reader())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.reader.cancel()
        await self.ws.close()

    async def _reader(self):
        async for raw in self.ws:
            msg = json.loads(raw)
            if "id" in msg and msg["id"] in self.pending:
                fut = self.pending.pop(msg["id"])
                if "error" in msg:
                    fut.set_exception(RuntimeError(json.dumps(msg["error"])))
                else:
                    fut.set_result(msg.get("result", {}))
            elif "method" in msg:
                await self.events.put(msg)

    async def send(self, method, params=None, timeout=30):
        msg_id = self.next_id
        self.next_id += 1
        fut = asyncio.get_event_loop().create_future()
        self.pending[msg_id] = fut
        await self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        return await asyncio.wait_for(fut, timeout)


def json_get(path):
    with urllib.request.urlopen(f"{CDP_BASE}{path}", timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def find_or_create_ads_target():
    pages = json_get("/json/list")
    for page in pages:
        if page.get("type") == "page" and "ads.google.com" in page.get("url", ""):
            return page, False
    req = urllib.request.Request(f"{CDP_BASE}/json/new?{urllib.parse.quote(ADS_BULK_URL, safe='')}", method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8")), True
    except Exception:
        with urllib.request.urlopen(f"{CDP_BASE}/json/new?{urllib.parse.quote(ADS_BULK_URL, safe='')}", timeout=20) as response:
            return json.loads(response.read().decode("utf-8")), True


async def wait(seconds):
    await asyncio.sleep(seconds)


def classify_filename(body, filename):
    if filename not in body:
        return "NOT_VISIBLE"
    lower = body.lower()
    if re.search(r"Error count\s*0", body) and re.search(r"success\s*88", body, re.I):
        if "preview is complete" in lower or "预览已完成" in body:
            return "VISIBLE_PREVIEW_COMPLETE_88_OK"
        if "preview is in progress" in lower or "预览正在进行" in body:
            return "VISIBLE_PREVIEW_IN_PROGRESS_ERROR_0"
    if re.search(r"Error count\s*[1-9]", body):
        return "VISIBLE_WITH_ERRORS"
    return "VISIBLE_UNCLASSIFIED"


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    target, created = find_or_create_ads_target()
    async with CDP(target["webSocketDebuggerUrl"]) as cdp:
        await cdp.send("Page.enable")
        await cdp.send("Runtime.enable")
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1440,
            "height": 1000,
            "deviceScaleFactor": 1,
            "mobile": False,
        })
        await cdp.send("Page.navigate", {"url": ADS_BULK_URL})
        await wait(12)
        result = await cdp.send("Runtime.evaluate", {
            "expression": """(() => ({
              url: location.href,
              title: document.title,
              bodyText: document.body?.innerText || "",
              readyState: document.readyState
            }))()""",
            "returnByValue": True,
            "awaitPromise": True,
        })
        data = result.get("result", {}).get("value", {})
        shot = await cdp.send("Page.captureScreenshot", {"format": "png"})
    body = data.get("bodyText", "")
    statuses = {country: classify_filename(body, filename) for country, filename in COUNTRY_FILENAMES.items()}
    throttle_terms = [
        "too many simultaneous uploads",
        "too many recent spreadsheets",
        "simultaneous uploads",
        "recent spreadsheets",
        "uploads are currently limited",
        "正在处理",
        "过多",
    ]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only_google_ads_bulk_upload_page_probe",
        "target_created": created,
        "url": data.get("url", ""),
        "title": data.get("title", ""),
        "bodyTextLength": len(body),
        "country_filename_statuses": statuses,
        "throttle_hints_found": [term for term in throttle_terms if term.lower() in body.lower()],
        "login_hint": bool(re.search(r"sign in|log in", body, re.I)),
        "writes_made": "No Google Ads upload/preview/apply/campaign/budget/bid/status change; read-only page text and screenshot only.",
    }
    (OUT / "google_ads_bulk_upload_readonly_probe.txt").write_text(body, encoding="utf-8")
    (OUT / "google_ads_bulk_upload_readonly_probe.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (OUT / "google_ads_bulk_upload_readonly_probe.png").write_bytes(base64.b64decode(shot["data"]))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
