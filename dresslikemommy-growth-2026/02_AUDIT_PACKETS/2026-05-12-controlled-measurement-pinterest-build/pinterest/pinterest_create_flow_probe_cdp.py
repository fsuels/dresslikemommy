#!/usr/bin/env python3
import asyncio
import base64
import json
import urllib.request
import websockets
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
CDP_PORT = 9222
ADVERTISER_ID = "549756244483"
CAMPAIGN_URL = (
    f"https://ads.pinterest.com/advertiser/{ADVERTISER_ID}/reporting/campaigns/"
    "?redirectSource=NONE&campaignFilter=RUNNING%2CPAUSED%2CNOT_STARTED%2CCOMPLETED%2CADVERTISER_DISABLED"
    "&campaignFilterUpdated=false&adGroupFilter=RUNNING%2CPAUSED%2CNOT_STARTED%2CCOMPLETED%2CADVERTISER_DISABLED"
    "&adGroupFilterUpdated=false&adFilter=APPROVED%2CPENDING%2CPAUSED%2CREJECTED%2CADVERTISER_DISABLED"
    "&adFilterUpdated=false&productGroupFilter=RUNNING%2CPAUSED%2CEXCLUDED&productGroupFilterUpdated=false"
    "&objectiveTypes=[AWARENESS,CONSIDERATION,CATALOG_SALES,WEB_CONVERSION,VIDEO_COMPLETION,VIDEO_VIEW]"
    "&objectiveTypesUpdated=false&customFilters=none&deliveryFilter=true&granularity=daily&attributionWindow=7%2F7%2F7"
    "&reportingViewId=-1&limit=10&bookmark=1"
)


class CDP:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.next_id = 1
        self.pending = {}
        self.events = asyncio.Queue()

    async def __aenter__(self):
        self.ws = await websockets.connect(self.ws_url, max_size=16 * 1024 * 1024)
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


def cdp_json(path):
    with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}{path}") as resp:
        return json.loads(resp.read().decode("utf-8"))


def create_target():
    quoted = urllib.request.quote("about:blank", safe="")
    req = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}/json/new?{quoted}", method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        with urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/new?{quoted}") as resp:
            return json.loads(resp.read().decode("utf-8"))


def close_target(target_id):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/close/{target_id}", timeout=2).read()
    except Exception:
        pass


async def wait_load(cdp, seconds=8):
    end = asyncio.get_event_loop().time() + seconds
    while asyncio.get_event_loop().time() < end:
        try:
            msg = await asyncio.wait_for(cdp.events.get(), timeout=0.5)
            if msg.get("method") == "Page.loadEventFired":
                await asyncio.sleep(2)
                return
        except asyncio.TimeoutError:
            pass
    await asyncio.sleep(2)


async def capture(cdp, label):
    expression = r"""(() => {
      const text = document.body?.innerText || "";
      const pick = (nodes) => [...nodes].slice(0, 120).map((el) => ({
        tag: el.tagName,
        text: (el.innerText || el.getAttribute("aria-label") || el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 180),
        aria: el.getAttribute("aria-label") || "",
        role: el.getAttribute("role") || "",
        disabled: !!el.disabled || el.getAttribute("aria-disabled") === "true"
      })).filter((x) => x.text || x.aria);
      return {
        url: location.href,
        title: document.title,
        readyState: document.readyState,
        timestamp: new Date().toISOString(),
        bodyText: text,
        bodyTextLength: text.length,
        blockerHints: {
          login: /log in|sign up|continue with/i.test(text),
          captcha: /captcha|recaptcha|verify you/i.test(text),
          billing: /billing|payment method/i.test(text),
          budget: /budget|daily spend|lifetime spend|bid/i.test(text),
          audience: /audience|retarget/i.test(text),
          paused: /paused|pause|not started/i.test(text),
          publishOrLaunch: /publish|launch|start campaign|promote/i.test(text)
        },
        buttons: pick(document.querySelectorAll("button,[role='button']")),
        links: pick(document.querySelectorAll("a[href]"))
      };
    })()"""
    result = await cdp.send("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
    data = result.get("result", {}).get("value", {})
    shot = await cdp.send("Page.captureScreenshot", {"format": "png"})
    (OUT / f"{label}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (OUT / f"{label}.txt").write_text(data.get("bodyText", ""), encoding="utf-8")
    (OUT / f"{label}.png").write_bytes(base64.b64decode(shot["data"]))
    return data


async def click_by_text(cdp, pattern):
    expression = f"""(() => {{
      const re = new RegExp({json.dumps(pattern)}, "i");
      const candidates = [...document.querySelectorAll("button,[role='button'],a[href]")];
      const el = candidates.find((node) => re.test((node.innerText || node.getAttribute("aria-label") || "").trim()));
      if (!el) return {{clicked: false, reason: "not_found"}};
      el.scrollIntoView({{block: "center", inline: "center"}});
      el.click();
      return {{clicked: true, text: (el.innerText || el.getAttribute("aria-label") || "").trim(), tag: el.tagName}};
    }})()"""
    result = await cdp.send("Runtime.evaluate", {"expression": expression, "returnByValue": True, "awaitPromise": True})
    return result.get("result", {}).get("value", {})


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before_pages = cdp_json("/json/list")
    target = create_target()
    try:
        async with CDP(target["webSocketDebuggerUrl"]) as cdp:
            await cdp.send("Page.enable")
            await cdp.send("Runtime.enable")
            await cdp.send("Network.enable")
            await cdp.send("Emulation.setDeviceMetricsOverride", {
                "width": 1440,
                "height": 1000,
                "deviceScaleFactor": 1,
                "mobile": False,
            })
            await cdp.send("Page.navigate", {"url": CAMPAIGN_URL})
            await wait_load(cdp, 20)
            before = await capture(cdp, "pinterest_before_campaign_manager")
            create_click = await click_by_text(cdp, r"^Create$")
            await asyncio.sleep(3)
            menu = await capture(cdp, "pinterest_create_menu_probe")
            next_click = {"clicked": False, "reason": "not_attempted"}
            if create_click.get("clicked"):
                # Probe only the first campaign-creation option if it is visible. Do not click any save/publish/launch control.
                next_click = await click_by_text(cdp, r"create campaign|campaign$")
                await asyncio.sleep(5)
            wizard = await capture(cdp, "pinterest_create_wizard_probe")
        after_pages = cdp_json("/json/list")
        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "before_readback_and_non_committal_create_flow_probe",
            "advertiser_id": ADVERTISER_ID,
            "approval_boundary": "paused US catalog/retargeting draft only; stop before budget/bid activation, audience changes, catalog/source/tag/feed changes, or launch/publish",
            "before_campaigns_text_hits": {
                "zero_campaigns": "0 campaigns" in before.get("bodyText", ""),
                "zero_serving": "0 currently being served" in before.get("bodyText", ""),
                "zero_spend": "$0.00" in before.get("bodyText", ""),
            },
            "create_click": create_click,
            "campaign_option_click": next_click,
            "wizard_blocker_hints": wizard.get("blockerHints", {}),
            "wizard_url": wizard.get("url", ""),
            "wizard_title": wizard.get("title", ""),
            "writes_made": "No Pinterest account object was saved/created; no campaign/ad group/ad/product group/budget/bid/audience/catalog/tag/source/feed setting was committed.",
            "pages_before_count": len([p for p in before_pages if p.get("type") == "page"]),
            "pages_after_count": len([p for p in after_pages if p.get("type") == "page"]),
        }
        (OUT / "pinterest_create_flow_probe_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2))
    finally:
        close_target(target["id"])


if __name__ == "__main__":
    asyncio.run(main())
