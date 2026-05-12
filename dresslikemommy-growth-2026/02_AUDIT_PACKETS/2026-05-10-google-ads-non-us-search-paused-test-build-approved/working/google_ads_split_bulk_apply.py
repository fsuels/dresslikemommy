#!/usr/bin/env python3
"""Apply approved paused non-US Google Ads split CSVs through an existing CDP tab.

This helper is intentionally scoped to the owner-approved paused Search TEST BUILD.
It uses the logged-in Chrome remote-debugging session on 127.0.0.1:9222 and stops
unless each country file previews as 88/88 # OK before apply.
"""

from __future__ import annotations

import base64
import csv
import json
import os
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


REPO = Path("/Users/fsuels/Projects/dresslikemommy")
PACKET = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved"
SPLIT_DIR = REPO / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs"
STATE_PATH = PACKET / "working/google_ads_split_bulk_apply_state.json"
CDP_BASE = "http://127.0.0.1:9222"
ADS_BULK_URL = "https://ads.google.com/aw/bulk/uploads?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493&__c=9710510557&authuser=0"

EXPECTED_ROWS = 88
EXPECTED_ROW_TYPES = {
    "Campaign": 1,
    "Ad group": 10,
    "Keyword": 30,
    "Negative keyword": 37,
    "Ad": 10,
}
COUNTRIES = ["CA", "AU", "CH", "DK", "DE", "NL", "SE", "FR", "BE", "ES", "IT", "PL", "CZ", "RO", "PT", "GR"]
FORBIDDEN_TERMS = [
    "23827590655",
    "PMax",
    "Performance Max",
    "Standard Shopping",
    "Vacation Family",
    "matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set",
    "7227378892897",
    "Christmas",
    "Xmas",
]


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
        result = self.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        return result.get("result", {}).get("value")

    def close(self):
        self.ws.close()

    def recv_event(self, method: str, timeout: int = 10) -> dict | None:
        previous_timeout = self.ws.gettimeout()
        self.ws.settimeout(timeout)
        deadline = time.time() + timeout
        try:
            while time.time() < deadline:
                msg = json.loads(self.ws.recv())
                if msg.get("method") == method:
                    return msg.get("params", {})
        except Exception:
            return None
        finally:
            self.ws.settimeout(previous_timeout)
        return None


def json_get(path: str):
    with urllib.request.urlopen(f"{CDP_BASE}{path}", timeout=20) as response:
        return json.load(response)


def get_or_open_bulk_page() -> dict:
    pages = json_get("/json/list")
    for page in pages:
        if page.get("type") == "page" and "ads.google.com/aw/bulk/uploads" in page.get("url", ""):
            return page
    req = urllib.request.Request(
        f"{CDP_BASE}/json/new?{urllib.parse.quote(ADS_BULK_URL, safe='')}",
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def wait_for(cdp: CDP, predicate, timeout: int, label: str):
    start = time.time()
    last_body = ""
    while time.time() - start < timeout:
        body = cdp.eval("document.body ? document.body.innerText : ''") or ""
        last_body = body
        if predicate(body):
            return body
        time.sleep(1)
    raise RuntimeError(f"Timed out waiting for {label}. Last body tail:\n{last_body[-2000:]}")


def click_first_matching(cdp: CDP, js_filter: str, label: str, use_last: bool = False):
    expr = f"""
(() => {{
  const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
  const all = [...document.querySelectorAll('material-button,button,[role=button],a,div,material-fab,material-select-dropdown-item,[role=option],material-list')]
    .map((e, i) => ({{e, i, text:(e.innerText||e.textContent||'').trim(), aria:e.getAttribute('aria-label')||'', cls:String(e.className), visible:visible(e)}}))
    .filter(x => x.visible);
  const matches = all.filter(x => ({js_filter}));
  const m = { 'matches[matches.length - 1]' if use_last else 'matches[0]' };
  if (m) {{
    const r = m.e.getBoundingClientRect();
    m.e.dispatchEvent(new MouseEvent('mousedown', {{bubbles:true, button:0, clientX:r.x+r.width/2, clientY:r.y+r.height/2}}));
    m.e.dispatchEvent(new MouseEvent('mouseup', {{bubbles:true, button:0, clientX:r.x+r.width/2, clientY:r.y+r.height/2}}));
    m.e.click();
  }}
  return {{clicked: !!m, count: matches.length, clickedIndex: m && m.i, matches: matches.map(x => ({{i:x.i,text:x.text,aria:x.aria,cls:x.cls}})).slice(0,8)}};
}})()
"""
    result = cdp.eval(expr)
    if not result or not result.get("clicked"):
        raise RuntimeError(f"Could not click {label}: {result}")
    return result


def mouse_click_source_dropdown(cdp: CDP):
    clicked = cdp.eval(
        r"""
(() => {
  const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
  const candidates = [...document.querySelectorAll('div[role=button], material-dropdown-select, dropdown-button, div')]
    .filter(e => visible(e) && /选择来源|Select source|Choose source/.test((e.innerText||e.textContent||'').trim()));
  const el = candidates.find(e => e.getAttribute('role') === 'button')
    || candidates.find(e => e.tagName === 'MATERIAL-DROPDOWN-SELECT')
    || candidates[0];
  if (!el) return null;
  const r = el.getBoundingClientRect();
  el.dispatchEvent(new MouseEvent('mousedown', {bubbles:true, button:0, clientX:r.x+r.width/2, clientY:r.y+r.height/2}));
  el.dispatchEvent(new MouseEvent('mouseup', {bubbles:true, button:0, clientX:r.x+r.width/2, clientY:r.y+r.height/2}));
  el.click();
  return {clicked:true, x:r.x + r.width/2, y:r.y + r.height/2, text:(el.innerText||el.textContent||'').trim(), tag:el.tagName, role:el.getAttribute('role')};
})()
"""
    )
    if not clicked:
        raise RuntimeError("Could not find source dropdown")


def ensure_upload_form(cdp: CDP):
    body = cdp.eval("document.body.innerText") or ""
    if "Upload spreadsheet" not in body and "上传电子表格" not in body:
        click_first_matching(
            cdp,
            "x.aria.includes('新建上传操作') || /New upload/i.test(x.aria) || x.aria.includes('Create upload operation')",
            "new upload",
        )
        wait_for(cdp, lambda b: "Upload spreadsheet" in b or "上传电子表格" in b, 20, "upload form")
        wait_for(
            cdp,
            lambda _b: bool(cdp.eval(
                r"""
(() => {
  const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
  const el = [...document.querySelectorAll('div[role=button]')]
    .find(e => visible(e) && /选择来源|Select source|Choose source/.test((e.innerText||e.textContent||'').trim()));
  return !!el && el.getBoundingClientRect().height > 10;
})()
"""
            )),
            10,
            "active source dropdown",
        )

    body = cdp.eval("document.body ? document.body.innerText : ''") or ""
    source_is_upload_file = "从计算机选择文件" in body or "Choose file from computer" in body
    cdp.call("DOM.enable")
    if not source_is_upload_file or not file_input_node_ids(cdp):
        mouse_click_source_dropdown(cdp)
        wait_for(
            cdp,
            lambda _b: bool(cdp.eval(
                r"""
(() => [...document.querySelectorAll('material-select-dropdown-item,[role=option]')]
  .some(e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length)
    && (/上传文件|Upload File|Upload a file/.test((e.innerText||e.textContent||'').trim()))))()
"""
            )),
            10,
            "Upload File source option",
        )
        click_first_matching(
            cdp,
            "x.text === '上传文件' || x.text === 'Upload File' || x.text === 'Upload a file'",
            "Upload File source option",
        )
        wait_for(
            cdp,
            lambda b: (
                "从计算机选择文件" in b
                or "Choose file from computer" in b
                or "Select a file from your computer" in b
            ),
            10,
            "upload file source and file input",
        )


def navigate_bulk(cdp: CDP):
    cdp.call("Page.navigate", {"url": ADS_BULK_URL})
    wait_for(
        cdp,
        lambda b: (
            "Upload operation" in b
            or "Upload spreadsheet" in b
            or "Uploads" in b
            or "上传操作" in b
        )
        and ("Add filter" in b or "添加过滤" in b or "add" in b or "Create" in b),
        30,
        "bulk uploads page",
    )
    cdp.eval(
        r"""
(() => {
  for (const el of document.querySelectorAll('.ad-blocker-detected-overlay, .ad-blocker-detected-inner-warning')) {
    el.style.display = 'none';
    el.setAttribute('data-dlm-hidden-for-upload-ui-recovery', 'true');
  }
  return true;
})()
"""
    )
    time.sleep(1)


def file_input_node_ids(cdp: CDP) -> list[int]:
    def walk(node: dict, found: list[int]):
        attrs = node.get("attributes") or []
        attr_pairs = dict(zip(attrs[0::2], attrs[1::2]))
        if node.get("nodeName") == "INPUT" and attr_pairs.get("type") == "file":
            found.append(node["nodeId"])
        for child in node.get("children") or []:
            walk(child, found)
        for child in node.get("shadowRoots") or []:
            walk(child, found)
        for child in node.get("templateContent", {}).get("children") or []:
            walk(child, found)

    root = cdp.call("DOM.getDocument", {"depth": -1, "pierce": True})["root"]
    found: list[int] = []
    walk(root, found)
    return found


def set_file(cdp: CDP, file_path: Path):
    cdp.call("DOM.enable")
    cdp.eval(
        r"""
(() => {
  for (const el of document.querySelectorAll('.ad-blocker-detected-overlay, .ad-blocker-detected-inner-warning')) {
    el.style.display = 'none';
    el.setAttribute('data-dlm-hidden-for-file-picker-recovery', 'true');
  }
  return true;
})()
"""
    )
    nodes = file_input_node_ids(cdp)
    errors = []
    for node in nodes:
        try:
            cdp.call("DOM.setFileInputFiles", {"nodeId": node, "files": [str(file_path)]})
            wait_for(cdp, lambda b: file_path.name in b, 8, f"{file_path.name} selected")
            return
        except Exception as exc:
            errors.append(f"node {node}: {exc}")

    # Newer Google Ads renders a custom file-picker and opens a chooser lazily.
    # Intercept that chooser through CDP so no macOS UI interaction is needed.
    cdp.call("Page.setInterceptFileChooserDialog", {"enabled": True})
    rect = cdp.eval(
        r"""
(() => {
  const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
  const el = [...document.querySelectorAll('[role=button], local-file-picker, file-picker, div')]
    .find(e => visible(e) && /Select a file from your computer|Choose file from computer|从计算机选择文件/i.test((e.innerText || e.textContent || '').trim()));
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return {x: r.x + r.width / 2, y: r.y + r.height / 2, text: (el.innerText || el.textContent || '').trim()};
})()
"""
    )
    if rect:
        cdp.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": rect["x"], "y": rect["y"]})
        cdp.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
        cdp.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": rect["x"], "y": rect["y"], "button": "left", "clickCount": 1})
    else:
        click_first_matching(
            cdp,
            "/Select a file from your computer|Choose file from computer|从计算机选择文件/i.test(x.text)",
            "choose local file",
        )
    chooser = cdp.recv_event("Page.fileChooserOpened", timeout=10)
    if not chooser:
        raise RuntimeError("input[type=file] not found and file chooser did not open: " + " | ".join(errors))
    params = {"files": [str(file_path)]}
    if chooser.get("backendNodeId"):
        params["backendNodeId"] = chooser["backendNodeId"]
    cdp.call("DOM.setFileInputFiles", params)
    wait_for(cdp, lambda b: file_path.name in b, 8, f"{file_path.name} selected")


def screenshot(cdp: CDP, path: Path):
    data = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})["data"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(data))


def download_results(cdp: CDP, download_dir: Path, label: str, expected_name: str) -> Path:
    if download_dir.exists():
        shutil.rmtree(download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)
    cdp.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(download_dir), "eventsEnabled": True})
    click_first_matching(
        cdp,
        "x.text === 'Download results' || x.text === '下载结果'",
        f"download {label} results",
        use_last=True,
    )
    deadline = time.time() + 20
    while time.time() < deadline:
        files = [p for p in download_dir.iterdir() if p.is_file() and not p.name.endswith(".crdownload")]
        if files:
            result = files[0]
            if expected_name not in result.name:
                raise RuntimeError(f"Downloaded unexpected {label} file {result.name}, expected name to include {expected_name}")
            return result
        time.sleep(1)
    raise RuntimeError(f"No {label} result downloaded into {download_dir}")


def validate_results(path: Path, country: str, phase: str) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    summary = {
        "country": country,
        "phase": phase,
        "file": str(path.relative_to(REPO)),
        "rows": len(rows),
        "row_types": {},
        "statuses": {},
        "results": {},
        "bad_hits": [],
    }
    campaign_name = f"DLM_{country}_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"
    for line, row in enumerate(rows, 2):
        summary["row_types"][row.get("Row Type", "")] = summary["row_types"].get(row.get("Row Type", ""), 0) + 1
        if row.get("Results"):
            summary["results"][row["Results"]] = summary["results"].get(row["Results"], 0) + 1
        for col in ["Campaign status", "Ad group status", "Keyword status", "Ad status"]:
            if row.get(col):
                summary["statuses"].setdefault(col, {})
                summary["statuses"][col][row[col]] = summary["statuses"][col].get(row[col], 0) + 1
        blob = " | ".join(str(v) for v in row.values() if v)
        if campaign_name not in blob and row.get("Campaign"):
            summary["bad_hits"].append({"line": line, "reason": "unexpected_campaign", "snippet": blob[:300]})
        for term in FORBIDDEN_TERMS:
            if term in blob:
                summary["bad_hits"].append({"line": line, "reason": f"forbidden:{term}", "snippet": blob[:300]})
        if "Enabled" in blob:
            summary["bad_hits"].append({"line": line, "reason": "enabled_text", "snippet": blob[:300]})
    expected_statuses = {
        "Campaign status": {"Paused": 1},
        "Ad group status": {"Paused": 10},
        "Keyword status": {"Paused": 67},
        "Ad status": {"Paused": 10},
    }
    ok = (
        summary["rows"] == EXPECTED_ROWS
        and summary["row_types"] == EXPECTED_ROW_TYPES
        and summary["results"] == {"# OK": EXPECTED_ROWS}
        and summary["statuses"] == expected_statuses
        and not summary["bad_hits"]
    )
    summary["result"] = "PASS" if ok else "FAIL"
    if not ok:
        raise RuntimeError(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"completed": {"GB": {"note": "GB canary applied manually before automation"}}}


def save_state(state: dict):
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def run_country(cdp: CDP, country: str) -> dict:
    file_path = SPLIT_DIR / f"{country}_intl_search_paused_draft_web_bulk.csv"
    if not file_path.exists():
        raise RuntimeError(f"Missing split CSV: {file_path}")
    navigate_bulk(cdp)
    print(f"[{country}] opening upload form", flush=True)
    ensure_upload_form(cdp)
    print(f"[{country}] selecting {file_path.name}", flush=True)
    set_file(cdp, file_path)
    screenshot(cdp, PACKET / f"raw/preview/{country}_file_selected_before_preview.png")
    click_first_matching(cdp, "x.text === 'Preview' || x.text === '预览'", f"{country} preview")
    print(f"[{country}] preview started", flush=True)
    body = wait_for(
        cdp,
        lambda b: file_path.name in b
        and ("preview is complete" in b.lower() or "预览已完成" in b)
        and ("Error count\n0" in b or "错误数\n0" in b)
        and (f"success\n{EXPECTED_ROWS}" in b.lower() or f"成功\n{EXPECTED_ROWS}" in b),
        90,
        f"{country} preview completion",
    )
    (PACKET / f"raw/preview/{country}_preview_body.txt").write_text(body, encoding="utf-8")
    screenshot(cdp, PACKET / f"raw/preview/{country}_preview_result.png")
    preview_file = download_results(
        cdp,
        PACKET / f"raw/preview/downloads/{country}",
        "preview",
        f"{country}_intl_search_paused_draft_web_bulk_RESULTS.csv",
    )
    preview_summary = validate_results(preview_file, country, "preview")
    print(f"[{country}] preview validated 88/88 # OK", flush=True)
    click_first_matching(cdp, "x.text === 'application' || x.text === '应用' || x.text === 'Apply'", f"{country} apply", use_last=True)
    print(f"[{country}] apply started", flush=True)
    body = wait_for(
        cdp,
        lambda b: file_path.name in b
        and ("成功完成" in b or "successfully completed" in b.lower())
        and (f"{EXPECTED_ROWS} 处更改成功" in b or f"{EXPECTED_ROWS} successful" in b.lower()),
        120,
        f"{country} apply completion",
    )
    (PACKET / f"raw/after-readbacks/{country}_apply_body.txt").write_text(body, encoding="utf-8")
    screenshot(cdp, PACKET / f"raw/after-readbacks/{country}_apply_result.png")
    apply_file = download_results(
        cdp,
        PACKET / f"raw/after-readbacks/downloads/{country}",
        "apply",
        f"{country}_intl_search_paused_draft_web_bulk_RESULTS.csv",
    )
    apply_summary = validate_results(apply_file, country, "apply")
    print(f"[{country}] apply validated 88/88 # OK", flush=True)
    return {"preview": preview_summary, "apply": apply_summary}


def main() -> int:
    requested = sys.argv[1:] or COUNTRIES
    bad = [country for country in requested if country not in COUNTRIES]
    if bad:
        raise RuntimeError(f"Unsupported country argument(s): {bad}")
    page = get_or_open_bulk_page()
    cdp = CDP(page["webSocketDebuggerUrl"])
    cdp.call("Runtime.enable")
    cdp.call("Page.enable")
    time.sleep(2)
    account_body = cdp.eval("document.body ? document.body.innerText.slice(0,1000) : ''") or ""
    if "dresslikemommy.com" not in (cdp.eval("document.title") or ""):
        raise RuntimeError(f"Unexpected Google Ads account/tab title: {cdp.eval('document.title')}")
    state = load_state()
    state.setdefault("completed", {})
    state.setdefault("failures", {})
    state["account_title"] = cdp.eval("document.title")
    state["account_body_prefix"] = account_body
    save_state(state)
    try:
        for country in requested:
            if country in state["completed"]:
                print(f"[{country}] already completed, skipping", flush=True)
                continue
            result = run_country(cdp, country)
            state["completed"][country] = result
            save_state(state)
        print("[DONE] all requested countries completed", flush=True)
        return 0
    except Exception as exc:
        state["failures"][country] = {"error": str(exc), "time": time.strftime("%Y-%m-%d %H:%M:%S %Z")}
        save_state(state)
        print(f"[STOP] {country}: {exc}", file=sys.stderr, flush=True)
        return 1
    finally:
        cdp.close()


if __name__ == "__main__":
    raise SystemExit(main())
