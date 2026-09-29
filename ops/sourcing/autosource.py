#!/usr/bin/env python3
"""Single entry point for the unattended product-sourcing loop (scheduled task "autosource").

Every shell step of a sourcing round goes through this one script so the scheduled run needs exactly one
pre-approved command shape: /usr/bin/python3 ops/sourcing/autosource.py <subcommand> ...
Runbook and rules: ops/sourcing/AUTOSOURCE_RUNBOOK.md (read first).

1688 reads use the owner's logged-in helper Chrome on CDP port 9333, in a DEDICATED tab this script opens
and closes (never the owner's own tabs). Read-only. A CAPTCHA/login page => exit code 3, stop the round.

Subcommands
  lock acquire|release                 run lock (stale after 150 min)
  next                                 this round's category (rotates through ROTATION) and the command to run
  elapsed                              minutes since this run took the lock (continue categories until 50)
  recent [HOURS]                       audit: products this job built recently + live readback + QA sheets
  unpublish HANDLE "<reason>"          audit: set an autosource-built product back to DRAFT
  seen                                 print how many offer ids were already screened
  search "<中文 keywords>"             1688 keyword search -> family-titled 2026 offer ids (+titles), unseen only
  scan ID[,ID..]                       offer pages: release season, 48h promise (deliveryLimit), fabric, supplier
  gate ID[,ID..]                       store creditdetail stats + automatic owner-rule verdict
  catalog HOST                         a passing store's 2026 offers (store listing, not search)
  dupcheck "<english words>"           duplicate check: store products (any status) whose title has ALL the words, e.g. dupcheck "heart hoodie"
  capture ID                           description images + manifest (ops/sourcing/vendor-images/<id>/desc/)
  skus ID                              per-SKU prices/stock -> ops/sourcing/state/skus/<id>.json
  spec RECIPE.json                     write engine spec from a recipe (family_sweatshirt engine path)
  build HANDLE                         generate runner, preflight, create DRAFT, stock 100/variant
  translate HANDLE                     Codex design translations + size strings + register (shared-file lock)
  images HANDLE                        build image job + ChatGPT-app Codex photos (4 images)
  review HANDLE                        write QA sheet /tmp/autosource/<handle>_review.jpg (inspect with Read)
  finish HANDLE                        attach -> localization closeout (must PASS) -> activate -> readback
  standalone RECIPE.json               siblings/couples/maternity DRAFT (no engine mode) + stage photo job
  standalone-finish HANDLE             attach -> Codex translations -> closeout -> activate -> readback
  commit "<message>"                   commit + push this round's repo files from a clean worktree
"""
from __future__ import annotations

import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
STATE = ROOT / "ops/sourcing/state"
SEEN = STATE / "autosource_seen.json"
LOCK = STATE / "AUTOSOURCE_LOCK"
I18N_LOCK = Path("/tmp/dlm_i18n.lock")
WORK = Path("/tmp/autosource")
WT = Path("/tmp/autosource-wt")
PY = "/usr/bin/python3"
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
LOCALES = "ar cs da de el es fi fr he hi it ja ko nl no pl pt-BR ro ru sv".split()
FAMILY_RE = re.compile(r"亲子|一家|母女|父子|母子|全家|家庭|情侣|兄妹|姐弟|孕妇|family|Family|parent|Parent|mother|Mother|couple|Couple|matern|Matern|sibling|Sibling")
WORK.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- helpers
def sh(cmd: list[str], cwd: Path = ROOT, env: dict | None = None, check: bool = True, timeout: int = 3600) -> str:
    e = dict(os.environ, **(env or {}))
    p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout or "") + (p.stderr or "")
    out = "\n".join(l for l in out.splitlines() if "NotOpenSSLWarning" not in l and "warnings.warn" not in l)
    if check and p.returncode not in (0,):
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(cmd)}\n{out[-3000:]}")
    return out


def load_seen() -> dict:
    try:
        return json.loads(SEEN.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_seen(d: dict) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def known_offer_ids() -> set[str]:
    ids = set(load_seen())
    for f in (T / "specs").glob("*.json"):
        try:
            ids.add(str(json.loads(f.read_text(encoding="utf-8")).get("offer_id", "")))
        except Exception:
            pass
    txt = (ROOT / "ops/sourcing/TRUSTED-SUPPLIERS.md").read_text(encoding="utf-8")
    ids |= set(re.findall(r"\b1\d{12}\b", txt))
    return ids


class Tab:
    """A dedicated tab in the helper Chrome (CDP 9333); closed on exit."""

    def __init__(self, port: int = 9333):
        import websocket  # type: ignore
        base = f"http://127.0.0.1:{port}"
        req = urllib.request.Request(f"{base}/json/new?about:blank", method="PUT")
        try:
            t = json.load(urllib.request.urlopen(req, timeout=8))
        except Exception:
            t = json.load(urllib.request.urlopen(f"{base}/json/new?about:blank", timeout=8))
        self.base, self.id = base, t["id"]
        self.ws = websocket.create_connection(t["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.n = 0

    def call(self, method: str, params: dict | None = None, timeout: int = 40) -> dict:
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        end = time.time() + timeout
        while time.time() < end:
            m = json.loads(self.ws.recv())
            if m.get("id") == mid:
                return m
        raise TimeoutError(method)

    def go(self, url: str, wait: float = 5) -> None:
        self.call("Page.navigate", {"url": url})
        time.sleep(wait)

    def js(self, expr: str):
        r = self.call("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True}, timeout=60)
        return r.get("result", {}).get("result", {}).get("value")

    def scroll(self, n: int = 4, dy: int = 900, pause: float = 0.5) -> None:
        for _ in range(n):
            self.js(f"window.scrollBy(0,{dy})")
            time.sleep(pause)

    def blocked(self) -> bool:
        s = self.js("JSON.stringify([location.href, document.title, (document.body&&document.body.innerText||'').length])")
        u, t, n = json.loads(s)
        return bool(re.search(r"captcha|punish|验证|login|_____tmd_____", u + t, re.I)) or n < 300

    def close(self) -> None:
        try:
            self.ws.close()
            urllib.request.urlopen(f"{self.base}/json/close/{self.id}", timeout=8)
        except Exception:
            pass


def stop_blocked(tab: Tab, what: str) -> None:
    tab.close()
    print(f"BLOCKED: 1688 shows a CAPTCHA/login page during {what}. Stop the round (never bypass).")
    sys.exit(3)


# ---------------------------------------------------------------- 1688 read steps
def cmd_search(kw: str) -> None:
    q = urllib.parse.quote(kw.encode("gbk"))
    tab = Tab()
    tab.go(f"https://s.1688.com/selloffer/offer_search.htm?keywords={q}", 6)
    if tab.blocked():
        stop_blocked(tab, "search")
    tab.scroll(10, 1200, 0.7)
    raw = tab.js(r"""(()=>{const out={}; document.querySelectorAll('a[href*="offer/"], [data-renderkey]').forEach(a=>{const h=a.href||''; let m=h.match(/offer\/(\d{13})/); let id=m&&m[1]; if(!id){const k=a.getAttribute('data-renderkey')||''; const mm=k.match(/(\d{13})$/); id=mm&&mm[1];} if(!id) return; const t=(a.innerText||'').replace(/\s+/g,' ').trim(); if(t.length>(out[id]||'').length) out[id]=t.slice(0,90);}); return JSON.stringify(out);})()""")
    tab.close()
    res = json.loads(raw or "{}")
    known = known_offer_ids()
    fam = {i: t for i, t in res.items() if i > "1040000000000" and FAMILY_RE.search(t) and i not in known}
    (WORK / "last_search.json").write_text(json.dumps(fam, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"results {len(res)}; new family-titled 2026 offers {len(fam)}")
    for i, t in fam.items():
        print(i, "|", t[:70])
    print("IDS", ",".join(fam))


SCAN_JS = r"""(()=>{const t=(document.body.innerText||'').replace(/\s+/g,' ');const h=document.documentElement.innerHTML;
const g=k=>{const m=t.match(new RegExp('('+k+')\\s*(.{0,120})'));return m?m[2]:''};
const imgs=[...new Set([...document.querySelectorAll('img')].map(i=>i.src).filter(s=>/cbu01\.alicdn\.com\/img\/ibank/.test(s)))];
return JSON.stringify({title:document.title.slice(0,90),company:(h.match(/"companyName":"([^"]+)"/)||[])[1]||'',
host:(h.match(/"sellerWinportUrl"\s*:\s*"https?:\/\/([a-z0-9-]+\.1688\.com)/)||[])[1]||'',
release:g('Year and season of (?:release|launch)|上市年份/?季节'),published:g('商品发布时间'),
fabric:g('Fabric name|面料名称'),main:g('Main fabric composition|主面料成分'),
dl:(h.match(/"deliveryLimit":(\d+)/)||[])[1]||'',dlt:(h.match(/"deliveryLimitText":"([^"]+)"/)||[])[1]||'',
moq:(t.match(/(\d+)\s*件起批/)||[])[1]||'',img:imgs[0]||''})})()"""


def season_ok(r: str) -> bool:
    return "2026" in r and bool(re.search(r"Fall|Autumn|Winter|秋|冬", r))


def cmd_scan(ids: str, gap: float = 35) -> None:
    seen = load_seen()
    tab = Tab()
    try:
        for oid in [i for i in ids.split(",") if i]:
            tab.go(f"https://detail.1688.com/offer/{oid}.html", 5)
            if tab.blocked():
                save_seen(seen)
                stop_blocked(tab, f"scan {oid}")
            tab.scroll()
            r = json.loads(tab.js(SCAN_JS))
            ok = r["dl"] in ("1", "2") and season_ok(r["release"])
            r["pass_ship_season"] = ok
            r["scanned"] = time.strftime("%Y-%m-%d")
            seen[oid] = {k: r[k] for k in ("title", "company", "host", "release", "dl", "main", "moq", "pass_ship_season", "scanned")}
            save_seen(seen)
            print(("PASS " if ok else "fail ") + oid, "| dl", r["dl"], "|", r["release"][:14], "|", r["company"][:16], "| fabric:", r["fabric"][:40], "| composition:", r["main"][:90], "|", r["title"][:60], flush=True)
            time.sleep(gap)
    finally:
        tab.close()


CREDIT_JS = r"""JSON.stringify((document.body.innerText||'').replace(/\s+/g,' '))"""


def credit(tab: Tab, host: str) -> dict:
    tab.go(f"https://{host}/page/creditdetail.htm", 7)
    if tab.blocked():
        stop_blocked(tab, f"creditdetail {host}")
    tab.scroll(5, 800, 0.8)
    b = json.loads(tab.js(CREDIT_JS))
    g = lambda p: (re.search(p, b) or [None, ""])[1]
    d = {
        "company": g(r"^([一-龥（）()]{4,30}?(?:有限公司|厂|商行|店|经营部|工商户）))"),
        "years": g(r"入驻(\d+)年") or g(r"(\d+)\s*years? on 1688"),
        "established": g(r"(\d{4}\.\d{2})成立") or g(r"Established in\s*([A-Za-z]+ \d{4})"),
        "pickup48": g(r"48[Hh]揽收率\s*([\d.]+)%") or g(r"48h collection rate[^%]{0,40}?([\d.]+)%"),
        "fulfill48": g(r"48[Hh]履约率\s*([\d.]+)%") or g(r"48h fulfillment rate[^%]{0,40}?([\d.]+)%"),
        "quality_return": g(r"品质退货率\s*([\d.]+)%") or g(r"Quality return rate[^%]{0,40}?([\d.]+)%"),
        "dispute": g(r"纠纷率\s*([\d.]+)%") or g(r"Dispute rate[^%]{0,40}?([\d.]+)%"),
        "service": g(r"服务分\s*([\d.]+)") or g(r"Service points\s*([\d.]+)"),
        "orders30": g(r"最近30天支付订单数\s*(\d+)") or g(r"orders in the last 30 days\s*(\d+)"),
        "warehouse": g(r"仓库地址\s*(\S{2,14})"),
    }
    if not d["years"] and d["established"]:
        # English UI shows only the founding date ("Established in april 2018" / "2018.04成立"); use it as the tenure fallback.
        est = d["established"].strip()
        m = re.match(r"(\d{4})\.(\d{2})", est)
        if m:
            y, mo = int(m.group(1)), int(m.group(2))
        else:
            mm = re.match(r"([A-Za-z]+)\s+(\d{4})", est)
            months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            y, mo = (int(mm.group(2)), months.index(mm.group(1)[:3].lower()) + 1) if mm and mm.group(1)[:3].lower() in months else (0, 0)
        if y:
            now = time.localtime()
            d["years"] = str(int(((now.tm_year - y) * 12 + now.tm_mon - mo) // 12))
            d["years_source"] = "founding date"
    return d


def verdict(d: dict) -> tuple[bool, str]:
    f = lambda k: float(d.get(k) or 0)
    y = f("years")
    why = []
    if f("pickup48") < 95: why.append(f"48h pickup {d.get('pickup48') or '?'}% < 95")
    if f("fulfill48") and f("fulfill48") < 97: why.append(f"fulfillment {d['fulfill48']}% < 97")
    if f("service") and f("service") < 4.0: why.append(f"service {d['service']} < 4.0")
    if y < 3: why.append(f"{d.get('years') or '?'} years < 3")
    elif y < 5:  # owner 2026-09-28: 3-4 years only with strict stats
        if f("pickup48") < 97: why.append("3-4y needs pickup ≥97")
        if f("fulfill48") < 97: why.append("3-4y needs fulfillment ≥97")
        if d.get("quality_return") and f("quality_return") > 1: why.append("3-4y needs quality returns ≤1%")
        if d.get("dispute") and f("dispute") > 0.5: why.append("3-4y needs disputes ≈0")
        if f("orders30") < 500: why.append(f"3-4y needs 500+ orders/30d (has {d.get('orders30') or '?'})")
    return (not why, "; ".join(why) or "passes every supplier rule")


def cmd_gate(ids: str) -> None:
    seen = load_seen()
    tab = Tab()
    hosts: dict[str, dict] = {}
    try:
        for oid in [i for i in ids.split(",") if i]:
            host = (seen.get(oid) or {}).get("host", "")
            if not host:
                tab.go(f"https://detail.1688.com/offer/{oid}.html", 5)
                if tab.blocked():
                    stop_blocked(tab, f"gate {oid}")
                host = json.loads(tab.js(SCAN_JS))["host"]
            if not host:
                print("?", oid, "no store host found"); continue
            if host not in hosts:
                hosts[host] = credit(tab, host)
                time.sleep(20)
            d = hosts[host]
            ok, why = verdict(d)
            seen.setdefault(oid, {}).update({"host": host, "gate": d, "gate_pass": ok, "gate_why": why})
            save_seen(seen)
            print(("PASS " if ok else "fail ") + oid, host, d["company"], "| y", d["years"], "est", d["established"], "| pick", d["pickup48"],
                  "ful", d["fulfill48"], "ret", d["quality_return"], "disp", d["dispute"], "svc", d["service"], "ord", d["orders30"], "|", why, flush=True)
    finally:
        tab.close()


def cmd_catalog(host: str, since: str = "2026-06-01") -> None:
    tab = Tab()
    try:
        tab.go(f"https://{host}/page/offerlist.htm", 6)
        if tab.blocked():
            stop_blocked(tab, f"catalog {host}")
        js = r"""(async()=>{const h=document.documentElement.innerHTML; const mid=(h.match(/b2b-[0-9a-z]{8,24}/)||[])[0]; const all=[];
for(let p=1;p<=10;p++){ const r=await Promise.race([lib.mtop.request({api:'mtop.alibaba.alisite.cbu.server.moduleasyncservice',v:'1.0',type:'POST',data:{componentKey:'Wp_pc_common_offerlist',params:JSON.stringify({memberId:mid,appdata:{sortType:'timedown',pageNum:p,count:30}})}}),new Promise((_,j)=>setTimeout(()=>j('to'),9000))]).catch(e=>null);
 if(!r)break; const l=r.data.content.offerList||[]; all.push(...l); if(l.length<30)break;}
return JSON.stringify(all.map(o=>[String(o.id),+o.gmtCreate,o.offerPrice,o.subject]));})()"""
        rows = json.loads(tab.js(js) or "[]")
    finally:
        tab.close()
    cut = time.mktime(time.strptime(since, "%Y-%m-%d")) * 1000
    known = known_offer_ids()
    keep = [r for r in rows if r[1] >= cut and FAMILY_RE.search(r[3] or "")]
    print(f"{host}: {len(rows)} offers; {len(keep)} family offers since {since}")
    for r in keep:
        print(("seen " if r[0] in known else "NEW  ") + r[0], time.strftime("%Y-%m-%d", time.gmtime(r[1] / 1000)), r[2], "|", (r[3] or "")[:40])
    print("IDS", ",".join(r[0] for r in keep if r[0] not in known))


def cmd_capture(oid: str) -> None:
    tab = Tab()
    try:
        tab.go(f"https://detail.1688.com/offer/{oid}.html", 6)
        if tab.blocked():
            stop_blocked(tab, f"capture {oid}")
        tab.scroll(40, 900, 0.6)
        time.sleep(2)
        js = r"""(()=>{const out={desc:[],sku:[]}; const seen=new Set();
const dh=document.querySelector('.html-description'); const root=dh&&dh.shadowRoot;
if(root) root.querySelectorAll('img').forEach(im=>{let s=im.getAttribute('data-lazyload-src')||im.getAttribute('data-src')||im.src||''; if(!s||s.startsWith('data:'))return; if(s.startsWith('//'))s='https:'+s; if(seen.has(s))return; seen.add(s); out.desc.push({s,w:im.naturalWidth,h:im.naturalHeight});});
document.querySelectorAll('img').forEach(im=>{let s=im.getAttribute('data-lazyload-src')||im.currentSrc||im.src||''; if(!s||s.startsWith('data:'))return; if(s.startsWith('//'))s='https:'+s; if(!/alicdn/.test(s)||seen.has(s))return; seen.add(s); if((im.naturalWidth||0)>=500) out.desc.push({s,w:im.naturalWidth,h:im.naturalHeight});});
document.querySelectorAll('[class*=sku] [class*=item], [class*=prop-item], [class*=sku-item]').forEach(el=>{const t=(el.innerText||'').trim().slice(0,60); if(t) out.sku.push({t});});
out.page_text=(document.body.innerText||'').replace(/\s+/g,' ').slice(0,20000);
return JSON.stringify(out);})()"""
        r = json.loads(tab.js(js))
    finally:
        tab.close()
    d = ROOT / f"ops/sourcing/vendor-images/{oid}/desc"
    d.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, x in enumerate(r["desc"][:60]):
        u = re.sub(r"_\d+x\d+.*$", "", x["s"]).replace(".jpg_.webp", ".jpg")
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://detail.1688.com/"}), timeout=20).read()
            ext = ".png" if data[:4] == b"\x89PNG" else ".jpg"
            p = d / f"{i:02d}{ext}"
            p.write_bytes(data)
            saved.append({"path": str(p.relative_to(ROOT)), "url": u, "w": x["w"], "h": x["h"]})
        except Exception as e:
            saved.append({"url": u, "error": str(e)})
    (d / "manifest.json").write_text(json.dumps({"offer": oid, "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "desc_images": saved,
                                                 "sku_options": r["sku"], "page_text": r["page_text"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(oid, "desc images", sum(1 for s in saved if "path" in s), "->", d.relative_to(ROOT))
    # contact sheet for fast visual review
    try:
        from PIL import Image, ImageDraw
        ims = []
        for s in saved:
            if "path" in s:
                im = Image.open(ROOT / s["path"]).convert("RGB")
                ims.append(im.resize((180, max(1, int(im.height * 180 / im.width)))))
        cols = 10
        rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
        H = [min(max(i.height for i in r), 360) for r in rows]
        c = Image.new("RGB", (180 * cols, sum(H) + 18 * len(rows)), "white")
        dr = ImageDraw.Draw(c); y = 0; n = 0
        for rr, h in zip(rows, H):
            for j, im in enumerate(rr):
                c.paste(im.crop((0, 0, 180, min(im.height, h))), (j * 180, y + 18)); dr.text((j * 180 + 3, y + 2), f"{n:02d}", fill="black"); n += 1
            y += h + 18
        out = WORK / f"sheet_{oid}.jpg"
        c.save(out)
        print("contact sheet:", out)
    except Exception as e:
        print("sheet error", e)


def cmd_skus(oid: str) -> None:
    tab = Tab()
    try:
        tab.go(f"https://detail.1688.com/offer/{oid}.html", 6)
        if tab.blocked():
            stop_blocked(tab, f"skus {oid}")
        js = r"""JSON.stringify((()=>{const t=[...document.scripts].map(s=>s.textContent).find(x=>/"skuProps"/.test(x))||'';
function grab(key){const i=t.indexOf('"'+key+'":');if(i<0)return null;let j=t.indexOf(':',i)+1;while(t[j]===' ')j++;const open=t[j],close=open==='['?']':'}';let d=0,k=j;for(;k<t.length;k++){if(t[k]===open)d++;else if(t[k]===close){d--;if(!d)break;}}try{return JSON.parse(t.slice(j,k+1))}catch(e){return null}}
return {props:grab('skuProps'),map:grab('skuInfoMap')};})())"""
        r = json.loads(tab.js(js))
    finally:
        tab.close()
    m = r.get("map") or {}
    names = [v.get("name") for p in (r.get("props") or []) for v in p.get("value", [])]
    out = {"props": names, "prices": {html.unescape(k): (v.get("discountPrice") or v.get("price")) for k, v in m.items()},
           "stock": {html.unescape(k): v.get("canBookCount") for k, v in m.items()}}
    (STATE / "skus").mkdir(parents=True, exist_ok=True)
    (STATE / "skus" / f"{oid}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(oid, "sku props:", names)
    print("prices:", sorted(set(out["prices"].values()))[:10], "| skus", len(out["prices"]))


# ---------------------------------------------------------------- build steps
def price(cost: float, grams: int) -> float:
    landed = (cost + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def cmd_spec(recipe_path: str) -> None:
    """Recipe -> engine spec (family_sweatshirt path: everyday/Christmas sweatshirts, family knits, Mommy/Daddy & Me knits).
    See the runbook for the recipe schema."""
    rc = json.loads(Path(recipe_path).read_text(encoding="utf-8"))
    oid = rc["offer_id"]
    sk = json.loads((STATE / "skus" / f"{oid}.json").read_text(encoding="utf-8"))
    prices, stock = sk["prices"], sk["stock"]
    kid = adult = 0.0
    for c in rc["colors"]:
        for label, row in rc["sizes"].items():
            key = f"{c['vendor_value']}>{row['vendor_size']}"
            if key not in prices or (stock.get(key) or 0) < 40:
                raise SystemExit(f"missing/low-stock SKU {key} ({stock.get(key)})")
            if label.startswith("Child"):
                kid = max(kid, float(prices[key]))
            else:
                adult = max(adult, float(prices[key]))
    cp = price(kid, rc.get("child_grams", 250)) if kid else 0
    ap = price(adult, rc.get("adult_grams", 450)) if adult else 0
    handle = rc["handle"]
    if (T / "specs" / f"{handle}.json").exists() and not rc.get("overwrite"):
        raise SystemExit(f"spec for {handle} already exists")
    codes = {json.loads(f.read_text(encoding="utf-8")).get("shortcode") for f in (T / "specs").glob("*.json")}
    if rc["shortcode"] in codes or list((ROOT / "ops/scripts").glob(f"create-{rc['shortcode'].lower()}-*.sh")):
        if not rc.get("overwrite"):
            raise SystemExit(f"shortcode {rc['shortcode']} already used")
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{oid}/desc/manifest.json").read_text(encoding="utf-8"))
    hero = rc["hero_image"]
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = f"01-{handle[:40]}.jpg"
    shutil.copy(ROOT / f"ops/sourcing/vendor-images/{oid}/desc/{hero}", up / fname)
    rows = {k: [v["chart_label"], v["picker"], v["suffix"], v["age"], v["length"], v["chest"], v.get("sleeve", "-"), "-", "-", "-"] for k, v in rc["sizes"].items()}
    fit = {k: [v.get("height", "-"), v.get("weight", "-")] for k, v in rc["sizes"].items()}
    spec = {
        "mode": "family_sweatshirt", "title_variant": rc.get("title_variant", "everyday"),
        **({"garment": rc["garment"]} if rc.get("garment") else {}), **({"knit_role": rc["knit_role"]} if rc.get("knit_role") else {}),
        **({"chart_no_sleeve": True} if rc.get("chart_no_sleeve") else {}),
        "offer_id": oid, "offer_created": rc.get("offer_created", "2026"), "handle": handle, "shortcode": rc["shortcode"], "print_name": rc["print_name"],
        "colors": [{"name": c["name"], "token": c["token"]} for c in rc["colors"]],
        "color_pattern_gids": [f"gid://shopify/Metaobject/{g}" for g in rc["color_pattern_ids"]], "color_pattern_labels": rc["color_pattern_labels"],
        "fabric_key": rc["fabric_key"], "design_key": rc["design_key"], "sleeve_style": "Long-Sleeve",
        "print_sentence": rc["print_sentence"], "feature_label": rc["feature_label"], "feature_text": rc["feature_text"],
        "extra_tags": rc["extra_tags"], "media_alt": rc["media_alt"],
        "image_url": next((x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/" + hero)), ""),
        "image_filename": fname, "ai_refs": rc.get("ai_refs", [hero]),
        "chart_source": f"auto_{rc['shortcode'].lower()}", "chart_table": f"auto_{rc['shortcode'].lower()}",
        "chart_rows": rows, "fit_rows": fit, "chart_image": f"ops/sourcing/vendor-images/{oid}/desc/{rc['chart_image']}",
        "chart_note": rc["chart_note"],
        "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
        "vendor_title": rc.get("vendor_title", ""), "vendor_color_values": [c["vendor_value"] for c in rc["colors"]], "vendor_codes": [],
        "vendor_size_labels": list(rc["sizes"]),
        "vendor_prices_note": f"Child ¥{kid:g}; Adult ¥{adult:g}.",
        "designs_note": rc.get("designs_note", "One design as one Shopify product."),
        "exclusions_note": rc.get("exclusions_note", ""),
        "evidence_lines": rc["evidence_lines"],
    }
    (T / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (STATE / "recipes").mkdir(parents=True, exist_ok=True)
    shutil.copy(recipe_path, STATE / "recipes" / f"{handle}.json")
    print(handle, f"child ${cp:.2f} (¥{kid:g})", f"adult ${ap:.2f} (¥{adult:g})", "-> spec written")


def cmd_build(handle: str) -> None:
    spec = json.loads((T / "specs" / f"{handle}.json").read_text(encoding="utf-8"))
    print(sh([PY, "generate_runner.py", f"specs/{handle}.json"], cwd=T)[-300:])
    run = ROOT / f"ops/scripts/create-{spec['shortcode'].lower()}-{handle}.sh"
    out = sh(["bash", str(run)], env={"LISTING_PREFLIGHT_ONLY": "1"})
    if "preflight_passed" not in out:
        raise SystemExit("PREFLIGHT FAILED\n" + out[-2500:])
    print("preflight_passed")
    p = subprocess.run(["bash", str(run)], cwd=ROOT, env=dict(os.environ, LISTING_DEFER_CLOSEOUT="1"), capture_output=True, text=True, timeout=3600)
    if p.returncode != 3:
        raise SystemExit(f"CREATE FAILED rc={p.returncode}\n" + (p.stdout + p.stderr)[-3000:])
    print("DRAFT verified (rc=3)")
    print(sh([PY, "set_inventory_100.py", handle], cwd=T).strip().splitlines()[-1])


def i18n_lock() -> None:
    t0 = time.time()
    while True:
        try:
            I18N_LOCK.mkdir()
            return
        except FileExistsError:
            if time.time() - I18N_LOCK.stat().st_mtime > 3 * 3600:
                I18N_LOCK.rmdir()
                continue
            if time.time() - t0 > 3 * 3600:
                raise SystemExit("i18n lock busy for 3h")
            time.sleep(15)


def codex(dirpath: Path, prompt: str, timeout: int = 2400) -> None:
    (dirpath / "prompt.txt").write_text(prompt, encoding="utf-8")
    with open(dirpath / "prompt.txt", encoding="utf-8") as f, open(dirpath / "codex.log", "w") as log:
        subprocess.run([CODEX, "exec", "--skip-git-repo-check", "-C", str(dirpath), "-s", "workspace-write", "-"], stdin=f, stdout=log, stderr=log, cwd=dirpath, timeout=timeout)


def add_size_strings(handle: str) -> None:
    sys.path.insert(0, str(T))
    import seed_cache  # noqa
    ns = seed_cache.load(T / "specs" / f"{handle}.json")
    key = ns["size_key"]()
    en = {"size_text": ns["size_range_phrase"](), "kf5_text": ns["counts_phrase"](), "size_short": ns["size_short"]()}
    src = json.loads((T / "i18n/en_source.json").read_text(encoding="utf-8"))
    if key in src["size_variants"]:
        return
    d = WORK / f"sizes_{handle}"
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    (d / "source_en.json").write_text(json.dumps({v: v for v in en.values()}, ensure_ascii=False, indent=1), encoding="utf-8")
    ex = {l: next(iter(json.loads((T / f"i18n/tr_{l}.json").read_text(encoding="utf-8"))["size_variants"].values())) for l in ("de", "fr", "ja")}
    codex(d, "You are a professional e-commerce translator for Dress Like Mommy (matching family outfits).\n"
             f"TASK: source_en.json maps English size sentences to themselves. For each locale ({', '.join(LOCALES)}) write ./out/<locale>.json (create ./out) with the same keys and the translated sentence as value.\n"
             "RULES: keep S, M, L, XL, 2XL, 3XL, 4XL and all numbers exactly; natural shop wording; never leave English.\n"
             f"Match the style of these existing translations:\n{json.dumps(ex, ensure_ascii=False, indent=1)}\nDo not ask questions; write all files, then reply DONE.")
    src["size_variants"][key] = en
    (T / "i18n/en_source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for l in LOCALES:
        t = json.loads((d / "out" / f"{l}.json").read_text(encoding="utf-8"))
        p = T / f"i18n/tr_{l}.json"
        tr = json.loads(p.read_text(encoding="utf-8"))
        tr["size_variants"][key] = {k: t[v] for k, v in en.items()}
        p.write_text(json.dumps(tr, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("added size strings for", key)


def cmd_translate(handle: str) -> None:
    spec = json.loads((T / "specs" / f"{handle}.json").read_text(encoding="utf-8"))
    code = spec["shortcode"].lower()
    src = T / f"i18n/{code}_designs_en.json"
    src.write_text(json.dumps({handle: {"print": spec["print_name"], "print_sentence": spec["print_sentence"],
                                        "feature_label": spec["feature_label"], "feature_text": spec["feature_text"]}}, ensure_ascii=False, indent=1), encoding="utf-8")
    i18n_lock()
    try:
        add_size_strings(handle)
        shutil.rmtree("/tmp/dlm-codex/codex_i18n/out", ignore_errors=True)  # codex_translate_designs.py work dir
        print(sh([PY, "i18n/codex_translate_designs.py", "run", str(src.relative_to(T))], cwd=T, timeout=3000).strip().splitlines()[-1])
        print(sh([PY, "i18n/codex_translate_designs.py", "merge", str(src.relative_to(T))], cwd=T).strip().splitlines()[-1])
        out = sh([PY, "register_direct.py", handle], cwd=T)
        print(out.strip().splitlines()[-1])
        if "missing: []" not in out:
            raise SystemExit("REGISTER incomplete:\n" + out[-1500:])
    finally:
        try:
            I18N_LOCK.rmdir()
        except Exception:
            pass


def cmd_images(handle: str) -> None:
    if (T / "specs" / f"{handle}.json").exists():
        print(sh([PY, "ai_images/build_image_jobs.py", handle], cwd=T).strip()[-300:])
    print("prompt:", ROOT / "uploads" / handle / "ai/prompt.txt")
    print(sh(["bash", "ai_images/run_image_jobs.sh", handle], cwd=T, timeout=4 * 3600)[-400:])


def cmd_review(handle: str) -> None:
    out = WORK / f"{handle}_review.jpg"
    sh([PY, "ai_images/review_sheet.py", handle, str(out)], cwd=T)
    print("QA sheet:", out, "(open it with the Read tool and compare every image with the vendor photo)")


def cmd_finish(handle: str) -> None:
    print(sh([PY, "ai_images/attach_images.py", handle], cwd=T).strip().splitlines()[-1])
    ok = False
    for attempt in (1, 2):
        p = subprocess.run([PY, "ops/scripts/finalize_shopify_listing_localization.py", "--handles", handle], cwd=ROOT, capture_output=True, text=True, timeout=3600)
        last = (p.stdout + p.stderr).strip().splitlines()[-1]
        print(last)
        if p.returncode == 0:
            ok = True
            break
        time.sleep(20)
    if not ok:
        raise SystemExit(f"CLOSEOUT FAILED {handle} — not activated. Evidence: ops/listings/{handle}-localization-closeout.json")
    print(sh([PY, "activate_listing.py", handle], cwd=T).strip().splitlines()[-1])
    time.sleep(8)
    p = json.load(urllib.request.urlopen(f"https://www.dresslikemommy.com/products/{handle}.js?x={int(time.time())}", timeout=30))
    print("LIVE", p["title"], "| vendor", p.get("vendor"), "| imgs", len(p["images"]), "| avail", sum(v["available"] for v in p["variants"]), "/", len(p["variants"]),
          "| price", min(v["price"] for v in p["variants"]) / 100, max(v["price"] for v in p["variants"]) / 100)


# ---------------------------------------------------------------- standalone path (siblings / couples / maternity)
BLOCKED_WORDS = ("1688", "alibaba", "taobao", "supplier", "vendor", "grinch", "stitch", "disney", "rudolph", "season")
GID = lambda n: f"gid://shopify/Metaobject/{n}"
AGE_GIDS = {"kids": ["128116523105"], "adults": ["128116490337"], "women": ["128116490337"]}
TGENDER = {"unisex": "129972502625", "female": "129971617889", "male": "130231107681"}


def st_body(rc: dict) -> str:
    cols = [("Size", "label"), ("Age", "age"), ("Height (cm)", "height"), ("Weight (kg)", "weight"), ("Chest/Bust (cm)", "chest"),
            ("Sleeve (cm)", "sleeve"), ("Garment Length (cm)", "length")]
    cols = [(h, k) for h, k in cols if any(str(s.get(k, "")).strip() not in ("", "-") for s in rc["sizes"])]
    fmt = lambda k, v: (f"{v} cm" if k in ("height", "chest", "sleeve", "length") else f"{v} kg" if k == "weight" else str(v)) if str(v) not in ("", "-") else "-"
    head = "".join(f"<th>{h}</th>" for h, _ in cols)
    rows = "".join("<tr>" + "".join(f"<td>{fmt(k, s.get(k, '-'))}</td>" for _, k in cols) + "</tr>" for s in rc["sizes"])
    bullets = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in rc["bullets"])
    return (f"<p>{rc['lead']}</p><ul>{bullets}</ul>"
            f"<h3>Size Chart - {rc.get('chart_garment', 'Top')}</h3>"
            f'<table id="size-chart" class="size-chart"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'
            f"<p>{rc.get('chart_footnote', 'Measurements are taken with the garment laid flat; allow 1-2 cm difference.')}</p>"
            f"<p>{rc.get('closing', '')}</p>")


def cmd_standalone(recipe_path: str) -> None:
    """Create a DRAFT for a listing the engine has no mode for (kids-only siblings, adults-only couples, maternity),
    stock 100/variant, and stage the photo job. Then run: images HANDLE, review HANDLE, standalone-finish HANDLE."""
    sys.path.insert(0, str(T / "ai_images"))
    import attach_images as A  # noqa
    rc = json.loads(Path(recipe_path).read_text(encoding="utf-8"))
    oid, h = rc["offer_id"], rc["handle"]
    sk = json.loads((STATE / "skus" / f"{oid}.json").read_text(encoding="utf-8"))
    colors = rc.get("colors") or [{"name": None, "vendor_value": rc.get("vendor_color", "")}]
    cost = 0.0
    for c in colors:
        for s in rc["sizes"]:
            key = f"{c['vendor_value']}>{s['vendor_size']}" if c["vendor_value"] else s["vendor_size"]
            if key not in sk["prices"] or (sk["stock"].get(key) or 0) < 40:
                raise SystemExit(f"missing/low-stock SKU {key}")
            cost = max(cost, float(sk["prices"][key]))
    grams = rc.get("grams", 300)
    landed = (cost + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    pr = math.ceil(2.06 * landed - 0.99) + 0.99
    body = st_body(rc)
    payload = " ".join([rc["title"], rc["seo_title"], rc["seo_desc"], body, *rc["tags"]]).lower()
    bad = [w for w in BLOCKED_WORDS if re.search(rf"\b{re.escape(w)}\b", payload)]
    if bad or len(rc["title"]) > 70 or len(rc["seo_title"]) > 60 or len(rc["seo_desc"]) > 155:
        raise SystemExit(f"copy check failed: {bad} title {len(rc['title'])} seo {len(rc['seo_title'])} desc {len(rc['seo_desc'])}")
    if landed > pr / 2:
        raise SystemExit("margin rule failed")
    opts = [{"name": "Size", "values": [{"name": s["label"]} for s in rc["sizes"]]}]
    if colors[0]["name"]:
        opts.insert(0, {"name": "Color", "values": [{"name": c["name"]} for c in colors]})
    variants = []
    for c in colors:
        for s in rc["sizes"]:
            ov = ([{"optionName": "Color", "name": c["name"]}] if c["name"] else []) + [{"optionName": "Size", "name": s["label"]}]
            variants.append({"optionValues": ov, "price": f"{pr:.2f}", "compareAtPrice": f"{pr + 10:.2f}",
                             "sku": f"DLM-{rc['code']}-{(c.get('token') or 'STD')}-{s['suffix']}", "inventoryPolicy": "DENY", "taxable": True,
                             "inventoryItem": {"cost": f"{landed:.2f}", "tracked": True, "requiresShipping": True}})
    text, refs = "single_line_text_field", "list.metaobject_reference"
    mfs = [("custom", "category1", text, rc["category1"]), ("custom", "subcategory", text, rc["subcategory"]),
           ("custom", "subcategory2", text, rc["subcategory2"]), ("custom", "pattern", text, rc["print_name"]),
           ("custom", "style", text, rc["style"]), ("custom", "type", text, rc["type"]),
           ("mm-google-shopping", "custom_product", "boolean", "false"), ("mm-google-shopping", "gender", text, rc["google_gender"]),
           ("mm-google-shopping", "age_group", text, "kids" if rc["audience"] == "kids" else "adult"), ("mm-google-shopping", "condition", text, "new"),
           ("mm-google-shopping", "custom_label_0", text, rc["category1"]), ("mm-google-shopping", "custom_label_1", text, rc["print_name"]),
           ("mm-google-shopping", "custom_label_2", text, rc.get("label2", "Fall")), ("mm-google-shopping", "custom_label_3", text, rc["style"]),
           ("mm-google-shopping", "custom_label_4", text, rc["product_type"]),
           ("shopify", "age-group", refs, json.dumps([GID(x) for x in AGE_GIDS[rc["audience"]]])),
           ("shopify", "color-pattern", refs, json.dumps([GID(x) for x in rc["color_pattern_ids"]])),
           ("shopify", "fabric", refs, json.dumps([GID(x) for x in rc["fabric_ids"]])),
           ("shopify", "target-gender", refs, json.dumps([GID(TGENDER[rc["google_gender"]])]))]
    if all(s.get("size_gid") for s in rc["sizes"]):
        mfs.append(("shopify", "size", refs, json.dumps(list(dict.fromkeys(GID(s["size_gid"]) for s in rc["sizes"])))))
    inp = {"title": rc["title"], "handle": h, "status": "DRAFT", "vendor": "Dress Like Mommy", "productType": rc["product_type"],
           "descriptionHtml": body, "tags": sorted(set(rc["tags"] + [s["label"] for s in rc["sizes"]])), "category": rc["taxonomy_gid"],
           "seo": {"title": rc["seo_title"], "description": rc["seo_desc"]}, "productOptions": opts, "variants": variants,
           "metafields": [{"namespace": n, "key": k, "type": t, "value": v} for n, k, t, v in mfs]}
    ex = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": h})["productByHandle"]
    if ex:
        if ex["status"] != "DRAFT":
            raise SystemExit("exists and not DRAFT; refusing")
        inp["id"] = ex["id"]
    r = A.gql("mutation($i:ProductSetInput!){productSet(synchronous:true,input:$i){product{id handle status} userErrors{field message}}}", {"i": inp})["productSet"]
    if r["userErrors"]:
        raise SystemExit(r["userErrors"])
    print(r["product"]["id"], h, "DRAFT", f"price ${pr:.2f} (landed ${landed:.2f})", len(variants), "variants")
    print(sh([PY, "set_inventory_100.py", h], cwd=T).strip().splitlines()[-1])
    ai = ROOT / "uploads" / h / "ai"
    ai.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(rc["ai_refs"][:3], 1):
        shutil.copy(ROOT / f"ops/sourcing/vendor-images/{oid}/desc/{f}", ai / f"ref{i}.jpg")
    (ai / "prompt.txt").write_text(rc["image_prompt"], encoding="utf-8")
    (STATE / "recipes").mkdir(parents=True, exist_ok=True)
    shutil.copy(recipe_path, STATE / "recipes" / f"{h}.json")
    print("photo job staged:", ai / "prompt.txt", "-> next: images", h)


def cmd_standalone_finish(handle: str) -> None:
    sys.path.insert(0, str(T / "ai_images"))
    import attach_images as A  # noqa
    rc = json.loads((STATE / "recipes" / f"{handle}.json").read_text(encoding="utf-8"))
    p = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": handle})["productByHandle"]
    have = [n["alt"] for n in A.media_nodes(p["id"])]
    for f, alt in zip(("image1.png", "image3.png", "image5.png", "image6.png"), rc["alts"]):
        if alt not in have:
            A.upload(p["id"], ROOT / "uploads" / handle / "ai" / f, alt)
    for _ in range(30):
        if all(n["status"] == "READY" for n in A.media_nodes(p["id"])):
            break
        time.sleep(3)
    ts = T / "accessories/translate_standalone.py"
    extra = rc.get("translation_note", "- The print name is a product style name.")
    print(sh([PY, str(ts), handle, "source", extra], cwd=T / "accessories").strip().splitlines()[-1])
    print(sh([PY, str(ts), handle, "run"], cwd=T / "accessories", timeout=3000).strip().splitlines()[-1])
    print(sh([PY, str(ts), handle, "register"], cwd=T / "accessories").strip().splitlines()[-1])
    ok = False
    for _ in (1, 2):
        q = subprocess.run([PY, "ops/scripts/finalize_shopify_listing_localization.py", "--handles", handle], cwd=ROOT, capture_output=True, text=True, timeout=3600)
        print((q.stdout + q.stderr).strip().splitlines()[-1])
        if q.returncode == 0:
            ok = True; break
        print(sh([PY, str(ts), handle, "register"], cwd=T / "accessories").strip().splitlines()[-1])
    if not ok:
        raise SystemExit(f"CLOSEOUT FAILED {handle} — left DRAFT")
    print(sh([PY, "activate_listing.py", handle], cwd=T).strip().splitlines()[-1])
    time.sleep(8)
    j = json.load(urllib.request.urlopen(f"https://www.dresslikemommy.com/products/{handle}.js?x={int(time.time())}", timeout=30))
    print("LIVE", j["title"], "| imgs", len(j["images"]), "| avail", sum(v["available"] for v in j["variants"]), "/", len(j["variants"]),
          "| price", min(v["price"] for v in j["variants"]) / 100)


# ---------------------------------------------------------------- commit
COMMIT_PATHS = [
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/i18n",
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/runner_engine.py",
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/ai_images/build_image_jobs.py",
    "ops/sourcing/TRUSTED-SUPPLIERS.md", "ops/sourcing/AUTOSOURCE_RUNBOOK.md", "ops/sourcing/autosource.py",
    "ops/sourcing/state/autosource_seen.json", "ops/sourcing/state/autosource_rotation.json", "ops/sourcing/state/recipes",
    "ops/sourcing/state/skus", "ops/AGENT_WORKLOG.md",
]


def cmd_commit(message: str) -> None:
    sh(["git", "fetch", "-q", "origin"])
    if not (WT / ".git").exists():
        shutil.rmtree(WT, ignore_errors=True)
        sh(["git", "worktree", "add", "--detach", str(WT), "origin/main"])
    sh(["git", "checkout", "-q", "--detach", "origin/main"], cwd=WT)
    sh(["git", "reset", "-q", "--hard", "origin/main"], cwd=WT)
    for rel in COMMIT_PATHS:
        src, dst = ROOT / rel, WT / rel
        if not src.exists():
            continue
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("codex_*", "out", "*.log"))
        elif rel == "ops/AGENT_WORKLOG.md":
            # append only this run's new anchor block (text after the marker file), never overwrite peers' history
            blk = WORK / "worklog_append.md"
            if blk.exists():
                with open(dst, "a", encoding="utf-8") as f:
                    f.write("\n" + blk.read_text(encoding="utf-8").strip() + "\n")
                blk.unlink()
        elif rel == "ops/sourcing/TRUSTED-SUPPLIERS.md":
            blk = WORK / "suppliers_append.md"
            if blk.exists():
                with open(dst, "a", encoding="utf-8") as f:
                    f.write("\n" + blk.read_text(encoding="utf-8").strip() + "\n")
                blk.unlink()
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    sh(["git", "add", "-A"], cwd=WT)
    diff = sh(["git", "diff", "--cached"], cwd=WT)
    if re.search(r"alicdn\.com|detail\.1688\.com/offer|https?://shop[0-9a-z]+\.1688\.com", diff):
        raise SystemExit("REFUSED: staged diff contains vendor/source URLs")
    if not diff.strip():
        print("nothing to commit"); return
    sh(["git", "diff", "--cached", "--check"], cwd=WT)
    sh(["git", "commit", "-q", "-m", message + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], cwd=WT)
    for _ in range(3):
        p = subprocess.run(["git", "push", "-q", "origin", "HEAD:main"], cwd=WT, capture_output=True, text=True)
        if p.returncode == 0:
            print("pushed", sh(["git", "log", "--oneline", "-1"], cwd=WT).strip()); return
        r = subprocess.run(["git", "pull", "-q", "--rebase", "origin", "main"], cwd=WT, capture_output=True, text=True)
        if r.returncode != 0:  # append-only files: keep both sides
            for f in ("ops/AGENT_WORKLOG.md", "ops/sourcing/TRUSTED-SUPPLIERS.md"):
                pth = WT / f
                s = pth.read_text(encoding="utf-8")
                if "<<<<<<<" in s:
                    s = re.sub(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", lambda m: m.group(1).rstrip("\n") + "\n\n" + m.group(2).lstrip("\n"), s, flags=re.S)
                    pth.write_text(s, encoding="utf-8")
                    sh(["git", "add", f], cwd=WT)
            sh(["git", "-c", "core.editor=true", "rebase", "--continue"], cwd=WT, check=False)
    raise SystemExit("PUSH FAILED after 3 attempts")


# ---------------------------------------------------------------- category rotation
ROTATION = [
    ("search", "亲子装 卫衣 2026秋冬 一家三口", "family sweatshirts"),
    ("catalog", "shop859424j2546y8.1688.com", "辰承 (Dongguan, 48h) new designs"),
    ("search", "母女装 2026秋冬 卫衣", "Mommy & Me sweatshirts"),
    ("search", "亲子装 毛衣 2026秋冬", "family sweaters"),
    ("catalog", "tygtzd.1688.com", "TYG Kids (siblings knits) new designs"),
    ("search", "父子装 卫衣 2026秋冬", "Daddy & Me"),
    ("search", "亲子装 圣诞 卫衣 2026", "Christmas family sweatshirts"),
    ("catalog", "shop2j8l6k6928792.1688.com", "格莱美 (Dongguan, 48h) new designs"),
    ("search", "兄妹装 秋冬 2026", "siblings"),
    ("search", "母女装 毛衣 开衫 2026秋冬", "Mommy & Me knits"),
    ("catalog", "chentian1788.1688.com", "野狼魅力 (48h) new designs"),
    ("search", "情侣卫衣 2026秋冬", "couples sweatshirts"),
    ("search", "孕妇毛衣 2026秋冬", "maternity"),
    ("search", "亲子装 马甲 2026秋冬", "family vests"),
    ("search", "亲子 帽子围巾 2026冬", "matching family accessories"),
    ("search", "情侣毛衣 圣诞 2026", "couples Christmas knits"),
    ("search", "孕妇卫衣 2026秋冬", "maternity sweatshirts"),
    ("search", "亲子装 外套 2026秋冬", "family jackets"),
]
ROT_FILE = STATE / "autosource_rotation.json"


def cmd_next() -> None:
    try:
        i = json.loads(ROT_FILE.read_text())["next"]
    except Exception:
        i = 0
    kind, arg, label = ROTATION[i % len(ROTATION)]
    ROT_FILE.write_text(json.dumps({"next": (i + 1) % len(ROTATION), "last": label, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
    print(f"THIS ROUND: {label}")
    print(f"RUN: /usr/bin/python3 ops/sourcing/autosource.py {kind} \"{arg}\"")


# ---------------------------------------------------------------- lock
def cmd_lock(action: str) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    now = time.time()
    if action == "acquire":
        if LOCK.exists():
            try:
                age = now - float(LOCK.read_text().split()[0])
            except Exception:
                age = 1e9
            if age < 150 * 60:
                print(f"LOCKED: another sourcing round started {int(age/60)} min ago. Stop this run.")
                sys.exit(4)
        LOCK.write_text(f"{now} {time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
        print("lock acquired")
    else:
        LOCK.unlink(missing_ok=True)
        print("lock released")


def cmd_elapsed() -> None:
    try:
        start = float(LOCK.read_text().split()[0])
    except Exception:
        print("no active lock"); return
    mins = int((time.time() - start) / 60)
    print(f"ELAPSED {mins} min —", "CONTINUE with `next`" if mins < 50 else "STOP: write the worklog append, commit, release the lock")


def cmd_recent(hours: float = 26) -> None:
    """Products this job built recently (recipes touched in the last N hours) with a live readback, for the audit."""
    cut = time.time() - hours * 3600
    for f in sorted((STATE / "recipes").glob("*.json"), key=lambda p: p.stat().st_mtime):
        if f.stat().st_mtime < cut:
            continue
        h = f.stem
        try:
            j = json.load(urllib.request.urlopen(f"https://www.dresslikemommy.com/products/{h}.js?x={int(time.time())}", timeout=30))
            live = f"LIVE imgs {len(j['images'])} avail {sum(v['available'] for v in j['variants'])}/{len(j['variants'])} ${min(v['price'] for v in j['variants'])/100}"
        except Exception:
            live = "not live (draft or missing)"
        qa = WORK / f"{h}_review.jpg"
        if (ROOT / "uploads" / h / "ai" / "image1.png").exists() and not qa.exists():
            try:
                sh([PY, "ai_images/review_sheet.py", h, str(qa)], cwd=T)
            except SystemExit:
                pass
        print(h, "|", live, "| QA sheet:", qa if qa.exists() else "-", "| vendor sheet:", WORK / f"sheet_{json.loads(f.read_text())['offer_id']}.jpg")


def cmd_dupcheck(words: str) -> None:
    """Rule 6 helper: list store products (active, draft or archived) whose title contains every word."""
    sys.path.insert(0, str(T / "ai_images"))
    import attach_images as A  # noqa
    terms = [w for w in re.findall(r"[A-Za-z0-9']+", words) if len(w) > 1]
    if not terms:
        raise SystemExit('usage: dupcheck "<english words>"')
    q = " AND ".join(f"title:*{w}*" for w in terms)
    nodes = A.gql("query($q:String!){products(first:50,query:$q){nodes{handle title status featuredImage{url}}}}", {"q": q})["products"]["nodes"]
    print(f"{len(nodes)} store products match {terms}")
    for n in nodes:
        print(n["status"], "|", n["handle"], "|", n["title"][:80], "|", (n.get("featuredImage") or {}).get("url", "")[:120])


def cmd_unpublish(handle: str, reason: str) -> None:
    """Audit action: set a listing this job built back to DRAFT (reversible) and log why."""
    if not (STATE / "recipes" / f"{handle}.json").exists():
        raise SystemExit("refused: only products built by autosource can be unpublished by the audit")
    sys.path.insert(0, str(T / "ai_images"))
    import attach_images as A  # noqa
    p = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": handle})["productByHandle"]
    r = A.gql("mutation($i:ProductUpdateInput!){productUpdate(product:$i){product{status} userErrors{message}}}", {"i": {"id": p["id"], "status": "DRAFT"}})["productUpdate"]
    print(handle, p["status"], "->", (r["product"] or {}).get("status"), r["userErrors"], "| reason:", reason)


def main() -> None:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    c = a[0]
    if c == "lock": cmd_lock(a[1])
    elif c == "seen": print(len(load_seen()), "offers screened;", len(known_offer_ids()), "known ids")
    elif c == "next": cmd_next()
    elif c == "elapsed": cmd_elapsed()
    elif c == "recent": cmd_recent(float(a[1]) if len(a) > 1 else 26)
    elif c == "unpublish": cmd_unpublish(a[1], a[2] if len(a) > 2 else "audit")
    elif c == "search": cmd_search(a[1])
    elif c == "scan": cmd_scan(a[1], float(a[2]) if len(a) > 2 else 35)
    elif c == "gate": cmd_gate(a[1])
    elif c == "catalog": cmd_catalog(a[1], a[2] if len(a) > 2 else "2026-06-01")
    elif c == "dupcheck": cmd_dupcheck(a[1])
    elif c == "capture": cmd_capture(a[1])
    elif c == "skus": cmd_skus(a[1])
    elif c == "spec": cmd_spec(a[1])
    elif c == "build": cmd_build(a[1])
    elif c == "translate": cmd_translate(a[1])
    elif c == "images": cmd_images(a[1])
    elif c == "review": cmd_review(a[1])
    elif c == "finish": cmd_finish(a[1])
    elif c == "standalone": cmd_standalone(a[1])
    elif c == "standalone-finish": cmd_standalone_finish(a[1])
    elif c == "commit": cmd_commit(a[1])
    else:
        print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
