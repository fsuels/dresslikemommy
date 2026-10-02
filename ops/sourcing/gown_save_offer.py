#!/usr/bin/env python3
"""Save one 1688 offer read from the in-app (side) browser for ops/sourcing/gown_listing.py.

The owner's 1688 session lives in the Claude desktop app's browser pane, which scripts cannot drive. The agent runs a
read-only extraction in that tab (skuProps/skuInfoMap from the page scripts, the description images inside
.html-description's shadow root, deliveryLimitText, createDate, the attribute text), writes the result as JSON and
runs this script. Usage: gown_save_offer.py <offer>.json  (writes the contact sheet next to the JSON).

Save one 1688 offer read from the side browser: skus json (autosource format), images, contact sheets.
Input JSON: {oid, company, host, release, dl, dlt, created, weight_g, fabric, colors:[[name,img]], sizes:[...],
             price_default, prices_override:{"color>size":p}, stock_min, desc:[urls], main:[urls], attrs}"""
import json, sys, re, time, urllib.request
from pathlib import Path
ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
d = json.load(open(sys.argv[1]))
if isinstance(d, str):
    d = json.loads(d)
d["colors"] = [c for c in d.get("colors", []) if c[1] or len(d.get("colors", [])) == 1]
d["release"] = re.split(r" Color| 颜色", d.get("release", ""))[0].strip()
d.setdefault("weight_g", int((re.search(r"Weight \(g\) (\d+)", d.get("attrs", "")) or [0, 0])[1]))
oid = d["oid"]
colors = [c[0] for c in d["colors"]] or [""]
sizes = d["sizes"] or [""]
prices, stock = {}, {}
for c in colors:
    for s in sizes:
        k = ">".join(x for x in (c, s) if x)
        prices[k] = d.get("prices_override", {}).get(k, d["price_default"])
        stock[k] = d.get("stock", {}).get(k, d.get("stock_min", 100))
(ROOT / "ops/sourcing/state/skus").mkdir(parents=True, exist_ok=True)
(ROOT / f"ops/sourcing/state/skus/{oid}.json").write_text(json.dumps({"props": colors + sizes, "prices": prices, "stock": stock}, ensure_ascii=False, indent=1))
base = ROOT / f"ops/sourcing/vendor-images/{oid}"
def get(u, p):
    if not u.startswith("http"):
        u = "https://cbu01.alicdn.com/img/ibank/" + u
    u = re.sub(r"\.jpg_.*$", ".jpg", u)
    data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://detail.1688.com/"}), timeout=30).read()
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data); return p
files = []
for i, u in enumerate(d.get("desc", [])): files.append(("d%02d" % i, get(u, base / "desc" / f"{i:02d}.jpg")))
for i, u in enumerate(d.get("main", [])): files.append(("m%02d" % i, get(u, base / "main" / f"{i:02d}.jpg")))
d.setdefault("weight_g", 1000)
for i, (name, u) in enumerate(d["colors"]):
    if u: files.append((f"c{i}", get(u, base / "sku" / f"c{i}.jpg")))
meta = {k: d.get(k) for k in ("oid", "company", "host", "release", "dl", "dlt", "created", "weight_g", "fabric", "attrs", "store")}
meta["listed"] = time.strftime("%Y-%m-%d", time.gmtime(int(d["created"]) / 1000)) if d.get("created") else ""
meta["colors"] = d["colors"]; meta["sizes"] = sizes; meta["captured"] = time.strftime("%Y-%m-%dT%H:%M:%S")
(base / "manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
from PIL import Image, ImageDraw
ims = []
for lab, p in files:
    im = Image.open(p).convert("RGB"); ims.append((lab, im.resize((200, max(1, int(im.height * 200 / im.width))))))
cols = 8; rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
H = [min(max(i.height for _, i in r), 420) for r in rows]
c = Image.new("RGB", (200 * cols, sum(H) + 18 * len(rows)), "white"); dr = ImageDraw.Draw(c); y = 0
for rr, h in zip(rows, H):
    for j, (lab, im) in enumerate(rr):
        c.paste(im.crop((0, 0, 200, min(im.height, h))), (j * 200, y + 18)); dr.text((j * 200 + 3, y + 2), lab, fill="black")
    y += h + 18
out = Path(sys.argv[1]).with_suffix(".sheet.jpg"); c.save(out, quality=85)
print(oid, "skus", len(prices), "imgs", len(files), "sheet", out)
