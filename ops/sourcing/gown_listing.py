#!/usr/bin/env python3
"""Maternity photoshoot gown listings (owner batch 2026-10-01), with a reviewed photo for EVERY colour.

Owner rules this adds on top of the autosource standalone path (ops/sourcing/AUTOSOURCE_RUNBOOK.md):
- rule 13 (CONTINUOUS-EXPANSION-WORKFLOW.md): every offered colour gets its own photo, linked to that colour's variants;
- rule 14: the owner-picked gown batch may ship in 7-15 days; each listing says honestly that it is made to order
  (custom.made_to_order_days moves the PDP delivery window, snippets/made-to-order-window.liquid).

Offer data comes from the side browser (1688 reads in the owner's session), saved by save_offer.py into
ops/sourcing/state/skus/<id>.json and ops/sourcing/vendor-images/<id>/{desc,main,sku}/.

Usage (run from the repo root):
  gown_listing.py create RECIPE.json   DRAFT + 100 stock/variant + stage the 4-image job and the colour jobs
  gown_listing.py images HANDLE        IMAGE 1/3/5/6, then one colour photo per extra colour (ChatGPT-app Codex)
  gown_listing.py review HANDLE        QA sheet /tmp/autosource/<handle>_review.jpg (main row + colour row)
  gown_listing.py finish HANDLE        attach + link colour media -> Codex translations -> closeout -> activate -> readback
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
STATE = ROOT / "ops/sourcing/state"
PY = "/usr/bin/python3"
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
WORK = Path("/tmp/autosource")
CODEX_WORK = Path("/tmp/dlm-codex/gown_colors")
sys.path.insert(0, str(T / "ai_images"))
import attach_images as A  # noqa: E402

BLOCKED_WORDS = ("1688", "alibaba", "taobao", "supplier", "vendor", "season")
GID = lambda n: f"gid://shopify/Metaobject/{n}"
FEMALE = "129971617889"
MAIN_FILES = ("image1.png", "image3.png", "image5.png", "image6.png")


def sh(cmd: list[str], cwd: Path = ROOT, timeout: int = 3600) -> str:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise SystemExit(f"FAILED {' '.join(cmd[:3])}: {(p.stdout + p.stderr)[-1500:]}")
    return p.stdout


def recipe(handle: str) -> dict:
    return json.loads((STATE / "recipes" / f"{handle}.json").read_text(encoding="utf-8"))


def body(rc: dict) -> str:
    cols = [("Size", "label"), ("Bust (cm)", "bust"), ("Waist (cm)", "waist"), ("Hips (cm)", "hips"), ("Hollow to Floor (cm)", "hollow")]
    cols = [(h, k) for h, k in cols if any(str(s.get(k, "")).strip() for s in rc["sizes"])]
    head = "".join(f"<th>{h}</th>" for h, _ in cols)
    rows = "".join("<tr>" + "".join(f"<td>{s.get(k, '-')}</td>" for _, k in cols) + "</tr>" for s in rc["sizes"])
    bullets = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in rc["bullets"])
    return (f"<p>{rc['lead']}</p><ul>{bullets}</ul>"
            f"<h3>Size Chart - Dress</h3>"
            f'<table id="size-chart" class="size-chart"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'
            f"<p>{rc.get('chart_footnote', 'Body measurements in cm. Choose the size that fits your bust today; the empire waist and full skirt leave room for the bump.')}</p>"
            f"<p>{rc.get('closing', '')}</p>")


def cmd_create(recipe_path: str) -> None:
    rc = json.loads(Path(recipe_path).read_text(encoding="utf-8"))
    oid, h = rc["offer_id"], rc["handle"]
    sk = json.loads((STATE / "skus" / f"{oid}.json").read_text(encoding="utf-8"))
    colors = rc["colors"]
    if rc["hero_color"] not in [c["token"] for c in colors]:
        raise SystemExit("hero_color must be one of the colour tokens")
    for c in colors:  # rule 13: a vendor photo of every colour must exist to build its own photo from
        if not (ROOT / f"ops/sourcing/vendor-images/{oid}/{c['ref']}").exists():
            raise SystemExit(f"no vendor colour reference for {c['name']}: {c['ref']}")
    cost = 0.0
    for c in colors:
        for s in rc["sizes"]:
            key = f"{c['vendor_value']}>{s['vendor_size']}"
            if key not in sk["prices"] or (sk["stock"].get(key) or 0) < 40:
                raise SystemExit(f"missing/low-stock SKU {key}")
            cost = max(cost, float(sk["prices"][key]))
    if len(colors) * len(rc["sizes"]) > 100:
        raise SystemExit("more than 100 variants")
    grams = rc["grams"]
    landed = (cost + 3 + 45.4 + 8.2 * grams / 100) / 7.11  # same freight model as autosource standalone
    pr = math.ceil(2.06 * landed - 0.99) + 0.99
    html = body(rc)
    payload = " ".join([rc["title"], rc["seo_title"], rc["seo_desc"], html, *rc["tags"]]).lower()
    bad = [w for w in BLOCKED_WORDS if re.search(rf"\b{re.escape(w)}\b", payload)]
    if bad or len(rc["title"]) > 70 or len(rc["seo_title"]) > 60 or len(rc["seo_desc"]) > 155:
        raise SystemExit(f"copy check failed: {bad} title {len(rc['title'])} seo {len(rc['seo_title'])} desc {len(rc['seo_desc'])}")
    if landed > pr / 2:
        raise SystemExit("margin rule failed")
    o1 = rc.get("option1", "Color")  # "Style" when the vendor's first option is a set choice, not a colour
    opts = [{"name": o1, "values": [{"name": c["name"]} for c in colors]},
            {"name": "Size", "values": [{"name": s["label"]} for s in rc["sizes"]]}]
    variants = [{"optionValues": [{"optionName": o1, "name": c["name"]}, {"optionName": "Size", "name": s["label"]}],
                 "price": f"{pr:.2f}", "compareAtPrice": f"{pr + 10:.2f}", "sku": f"DLM-{rc['code']}-{c['token']}-{s['suffix']}",
                 "inventoryPolicy": "DENY", "taxable": True,
                 "inventoryItem": {"cost": f"{landed:.2f}", "tracked": True, "requiresShipping": True}}
                for c in colors for s in rc["sizes"]]
    text, refs = "single_line_text_field", "list.metaobject_reference"
    mfs = [("custom", "category1", text, "Maternity"), ("custom", "subcategory", text, "Dresses"),
           ("custom", "subcategory2", text, "Maternity Photoshoot Dresses"), ("custom", "pattern", text, rc["print_name"]),
           ("custom", "style", text, rc["style"]), ("custom", "type", text, rc["type"]),
           ("custom", "made_to_order_days", "number_integer", str(int(rc["made_to_order_days"]))),
           ("mm-google-shopping", "custom_product", "boolean", "false"), ("mm-google-shopping", "gender", text, "female"),
           ("mm-google-shopping", "age_group", text, "adult"), ("mm-google-shopping", "condition", text, "new"),
           ("mm-google-shopping", "custom_label_0", text, "Maternity"), ("mm-google-shopping", "custom_label_1", text, rc["print_name"]),
           ("mm-google-shopping", "custom_label_2", text, "All Season"), ("mm-google-shopping", "custom_label_3", text, rc["style"]),
           ("mm-google-shopping", "custom_label_4", text, rc["product_type"]),
           ("shopify", "color-pattern", refs, json.dumps([GID(x) for x in dict.fromkeys(c["pattern_id"] for c in colors)])),
           ("shopify", "fabric", refs, json.dumps([GID(x) for x in rc["fabric_ids"]])),
           ("shopify", "target-gender", refs, json.dumps([GID(FEMALE)]))]
    inp = {"title": rc["title"], "handle": h, "status": "DRAFT", "vendor": "Dress Like Mommy", "productType": rc["product_type"],
           "descriptionHtml": html, "tags": sorted(set(rc["tags"] + ["Maternity", "Maternity Dresses", "Photoshoot"])),
           "category": rc.get("taxonomy_gid", "gid://shopify/TaxonomyCategory/aa-1-7-2"),
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
    print(r["product"]["id"], h, "DRAFT", f"price ${pr:.2f} (landed ${landed:.2f}, cost ¥{cost})", len(variants), "variants")
    print(sh([PY, "set_inventory_100.py", h], cwd=T).strip().splitlines()[-1])
    ai = ROOT / "uploads" / h / "ai"
    ai.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(rc["ai_refs"][:3], 1):
        shutil.copy(ROOT / f"ops/sourcing/vendor-images/{oid}/{f}", ai / f"ref{i}.jpg")
    for c in colors:
        shutil.copy(ROOT / f"ops/sourcing/vendor-images/{oid}/{c['ref']}", ai / f"vendor_{c['token']}.jpg")
    (ai / "prompt.txt").write_text(rc["image_prompt"], encoding="utf-8")
    (STATE / "recipes").mkdir(parents=True, exist_ok=True)
    shutil.copy(recipe_path, STATE / "recipes" / f"{h}.json")
    print("photo jobs staged:", ai, "-> next: images", h)


COLOR_PROMPT = """DRESS LIKE MOMMY — COLOUR PHOTO (automated run)
ref1 is our finished photo of a maternity photoshoot gown ({hero}). ref2 is the maker's photo of the SAME gown in another colour: {color}.
Create ONE new photo and save it in the current working directory as exactly {out}:
- the same woman, pose, setting, light and framing as ref1 (vertical 9:16, a single photo, no collage, no border);
- she wears the same gown, now in {color}, exactly as in ref2: {garment}
- keep every design detail identical (neckline, sleeves, fabric, dots/texture, skirt length and train); change only the colour;
- no text, no logos, no watermark. A natural, realistic photo of a pregnant European woman (the same woman as ref1).
STRICT CHECK before saving: regenerate if the colour does not match ref2, the gown design changed, it is not 9:16, or it looks fake.
Do not ask anything. When the file is saved, reply with one line: name, width x height."""


def color_jobs(h: str) -> None:
    rc = recipe(h)
    ai = ROOT / "uploads" / h / "ai"
    hero = next(c for c in rc["colors"] if c["token"] == rc["hero_color"])
    for c in rc["colors"]:
        if c["token"] == rc["hero_color"]:
            continue
        out = f"color_{c['token']}.png"
        if (ai / out).exists():
            print(out, "exists"); continue
        for attempt in (1, 2, 3):
            w = CODEX_WORK / f"{h[:40]}_{c['token']}"
            shutil.rmtree(w, ignore_errors=True); w.mkdir(parents=True)
            shutil.copy(ai / "image1.png", w / "ref1.png")
            shutil.copy(ai / f"vendor_{c['token']}.jpg", w / "ref2.jpg")
            (w / "prompt.txt").write_text(COLOR_PROMPT.format(hero=hero["name"], color=c["name"], out=out, garment=rc["garment_lock"]), encoding="utf-8")
            t0 = time.time()
            with open(w / "prompt.txt") as f, open(w / "codex.log", "w") as log:
                rcode = subprocess.run(["perl", "-e", "alarm shift; exec @ARGV", "1500", CODEX, "exec", "--skip-git-repo-check", "-C", str(w),
                                        "-s", "workspace-write", "-i", str(w / "ref1.png"), "-i", str(w / "ref2.jpg"), "-"],
                                       stdin=f, stdout=log, stderr=log, cwd=w).returncode
            ok = (w / out).exists()
            print(f"{time.strftime('%H:%M:%S')} {h} {c['name']} try{attempt} rc={rcode} ok={ok} secs={int(time.time() - t0)}", flush=True)
            if ok:
                shutil.copy(w / out, ai / out); break
            if re.search(r"rate limit|usage limit|quota|too many requests", (w / "codex.log").read_text(errors="ignore"), re.I):
                print("limit hit; pausing 30 min", flush=True); time.sleep(1800)


def cmd_images(h: str) -> None:
    ai = ROOT / "uploads" / h / "ai"
    if not all((ai / f).exists() for f in MAIN_FILES):
        print(sh(["bash", "ai_images/run_image_jobs.sh", h], cwd=T, timeout=4 * 3600)[-300:])
    if not all((ai / f).exists() for f in MAIN_FILES):
        raise SystemExit("main images missing")
    color_jobs(h)
    missing = [c["name"] for c in recipe(h)["colors"] if c["token"] != recipe(h)["hero_color"] and not (ai / f"color_{c['token']}.png").exists()]
    print("IMAGES DONE" if not missing else f"COLOUR PHOTOS MISSING: {missing}")


def cmd_review(h: str) -> None:
    from PIL import Image, ImageDraw
    rc = recipe(h)
    ai = ROOT / "uploads" / h / "ai"
    row1 = [("vendor ref1", ai / "ref1.jpg")] + [(f, ai / f) for f in MAIN_FILES]
    row2 = []
    for c in rc["colors"]:
        row2.append((f"vendor {c['name']}", ai / f"vendor_{c['token']}.jpg"))
        row2.append((f"OURS {c['name']}", ai / ("image1.png" if c["token"] == rc["hero_color"] else f"color_{c['token']}.png")))
    H = 520
    def strip(row):
        tiles = []
        for label, p in row:
            if p.exists():
                im = Image.open(p).convert("RGB"); size = im.size; im.thumbnail((H, H)); tiles.append((f"{label} {size[0]}x{size[1]}", im))
            else:
                tiles.append((f"{label} MISSING", Image.new("RGB", (290, H), "red")))
        return tiles
    rows = [strip(row1), strip(row2)]
    W = max(sum(t.width + 8 for _, t in r) for r in rows)
    sheet = Image.new("RGB", (W, (H + 26) * 2), "white"); dr = ImageDraw.Draw(sheet)
    for ri, r in enumerate(rows):
        x = 0
        for label, im in r:
            sheet.paste(im, (x, ri * (H + 26) + 22)); dr.text((x + 4, ri * (H + 26) + 4), label, fill="black"); x += im.width + 8
    out = WORK / f"{h}_review.jpg"; WORK.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=86)
    print("QA sheet:", out)


def activate(h: str) -> str:
    sys.path.insert(0, str(T))
    import activate_listing as AL  # noqa
    p = AL.gql("query($h:String!){productByHandle(handle:$h){id status totalInventory mediaCount{count}}}", {"h": h})["productByHandle"]
    need = 4 + len(recipe(h)["colors"]) - 1
    if p["mediaCount"]["count"] != need or p["totalInventory"] <= 0:
        return f"{h} SKIP not ready (media={p['mediaCount']['count']}/{need} inv={p['totalInventory']})"
    real = AL.activate.__globals__
    orig = real["gql"]
    def patched(q, v=None):  # reuse activate_listing.activate with its 4-media precondition widened to 4 + colour photos
        out = orig(q, v)
        if "mediaCount" in q and out.get("productByHandle"):
            out["productByHandle"]["mediaCount"]["count"] = 4
        return out
    real["gql"] = patched
    try:
        return AL.activate(h)
    finally:
        real["gql"] = orig


def cmd_finish(h: str) -> None:
    rc = recipe(h)
    ai = ROOT / "uploads" / h / "ai"
    p = A.gql("query($h:String!){productByHandle(handle:$h){id status variants(first:100){nodes{id selectedOptions{name value}}}}}", {"h": h})["productByHandle"]
    if p["status"] != "DRAFT":
        raise SystemExit("not a DRAFT")
    have = {n["alt"] for n in A.media_nodes(p["id"])}
    for f, alt in zip(MAIN_FILES, rc["alts"]):
        if alt not in have:
            A.upload(p["id"], ai / f, alt)
    color_alt = {c["token"]: f"{rc['title']} in {c['name']}" for c in rc["colors"]}
    for c in rc["colors"]:
        if c["token"] != rc["hero_color"] and color_alt[c["token"]] not in have:
            A.upload(p["id"], ai / f"color_{c['token']}.png", color_alt[c["token"]])
    for _ in range(40):
        nodes = A.media_nodes(p["id"])
        if all(n["status"] == "READY" for n in nodes):
            break
        time.sleep(3)
    by_alt = {n["alt"]: n["id"] for n in nodes}
    media_for = {c["name"]: by_alt[rc["alts"][0] if c["token"] == rc["hero_color"] else color_alt[c["token"]]] for c in rc["colors"]}
    vm = [{"variantId": v["id"], "mediaIds": [media_for[next(o["value"] for o in v["selectedOptions"] if o["name"] == rc.get("option1", "Color"))]]}
          for v in p["variants"]["nodes"]]
    r = A.gql("mutation($p:ID!,$vm:[ProductVariantAppendMediaInput!]!){productVariantAppendMedia(productId:$p,variantMedia:$vm){userErrors{field message}}}",
              {"p": p["id"], "vm": vm})["productVariantAppendMedia"]
    if r["userErrors"] and not all("already" in e["message"].lower() for e in r["userErrors"]):
        raise SystemExit(r["userErrors"])
    chk = A.gql("query($h:String!){productByHandle(handle:$h){variants(first:100){nodes{selectedOptions{name value} media(first:1){nodes{alt}}}}}}", {"h": h})
    wrong = [v for v in chk["productByHandle"]["variants"]["nodes"]
             if not v["media"]["nodes"] or v["media"]["nodes"][0]["alt"] not in (rc["alts"][0], *color_alt.values())]
    print("variant photos linked:", len(vm) - len(wrong), "/", len(vm))
    if wrong:
        raise SystemExit("variant media check failed")
    ts = T / "accessories/translate_standalone.py"
    extra = rc.get("translation_note", "")
    print(sh([PY, str(ts), h, "source", extra], cwd=T / "accessories").strip().splitlines()[-1])
    print(sh([PY, str(ts), h, "run"], cwd=T / "accessories", timeout=3000).strip().splitlines()[-1])
    print(sh([PY, str(ts), h, "register"], cwd=T / "accessories").strip().splitlines()[-1])
    ok = False
    for _ in (1, 2):
        q = subprocess.run([PY, "ops/scripts/finalize_shopify_listing_localization.py", "--handles", h], cwd=ROOT, capture_output=True, text=True, timeout=3600)
        print((q.stdout + q.stderr).strip().splitlines()[-1])
        if q.returncode == 0:
            ok = True; break
        print(sh([PY, str(ts), h, "register"], cwd=T / "accessories").strip().splitlines()[-1])
    if not ok:
        raise SystemExit(f"CLOSEOUT FAILED {h} — left DRAFT. Evidence: ops/listings/{h}-localization-closeout.json")
    act = activate(h)
    print(act)
    if " ACTIVE OK" not in act:
        raise SystemExit(f"NOT ACTIVATED {h}")
    time.sleep(8)
    j = json.load(urllib.request.urlopen(f"https://www.dresslikemommy.com/products/{h}.js?x={int(time.time())}", timeout=30))
    linked = sum(1 for v in j["variants"] if v.get("featured_image"))
    print("LIVE", j["title"], "| imgs", len(j["images"]), "| variants with photo", linked, "/", len(j["variants"]),
          "| avail", sum(v["available"] for v in j["variants"]), "| price", min(v["price"] for v in j["variants"]) / 100)


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"create": cmd_create, "images": cmd_images, "review": cmd_review, "finish": cmd_finish, "colors": color_jobs}
    if len(a) != 2 or a[0] not in cmds:
        raise SystemExit(__doc__)
    cmds[a[0]](a[1])
