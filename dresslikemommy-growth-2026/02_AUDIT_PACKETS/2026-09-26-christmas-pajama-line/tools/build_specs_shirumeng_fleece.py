#!/usr/bin/env python3
"""Build Mommy & Me coral-fleece listing specs for 诗茹梦 (Shenzhen Shirumeng) 2026 winter velvet
button-up pajamas (offer 1080921462408; mode "mommy_me", chart "shirumeng").

Gate (read 2026-09-27): offer created 2026-09-07, "Year and season of release"
Winter 2026, 100% polyester DeRong (brushed velvet), MOQ 1, 500 in stock per SKU,
supplier fulfillment 99.6%, 6 years, Guangdong. Designs were screened for licensed
characters (vendor-pixelated pockets and character prints excluded) and checked
against the store's active and archived Mommy & Me pajamas for duplicates.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
OFFER = None  # per design
C = {
    "Red": "gid://shopify/Metaobject/69600804961", "Green": "gid://shopify/Metaobject/70220546145",
    "White": "gid://shopify/Metaobject/69639733345", "Blue": "gid://shopify/Metaobject/69639766113",
    "Black": "gid://shopify/Metaobject/69943132257", "Gray": "gid://shopify/Metaobject/69944672353",
    "Multicolor": "gid://shopify/Metaobject/130231140449", "Checkered": "gid://shopify/Metaobject/130283143265",
    "Pink": "gid://shopify/Metaobject/69963645025", "Yellow": "gid://shopify/Metaobject/69622104161",
    "Striped": "gid://shopify/Metaobject/130283765857", "Beige": "gid://shopify/Metaobject/69641928801",
}
TOKENS = {"Pink": "PNK", "Yellow": "YLW", "Blue": "BLU", "Gray": "GRY", "White": "WHT"}
SIZES = ["Child 10", "Child 12", "Child 14", "Child 16", "Mom S", "Mom M", "Mom L", "Mom XL"]
VENDOR_LABEL = {"Child 10": "Children's size 10", "Child 12": "Children's size 12", "Child 14": "Children's size 14",
                "Child 16": "Children's size 16", "Mom S": "S size", "Mom M": "M size", "Mom L": "L size", "Mom XL": "XL"}


def main() -> None:
    designs = json.loads((TOOLS / "shirumeng_fleece_designs.json").read_text(encoding="utf-8"))
    allcap = json.loads((SCRATCH / "srm_designs.json").read_text(encoding="utf-8"))
    for code, d in designs.items():
        OFFER = d["offer"]
        cap = allcap[OFFER]
        rows = {html.unescape(k).split(">", 1)[1]: v for k, v in cap["prices"].items() if k.startswith(code)}
        stock = {html.unescape(k).split(">", 1)[1]: v for k, v in cap["stock"].items() if k.startswith(code)}
        prices = {}
        for canon in SIZES:
            hit = [lab for lab in rows if VENDOR_LABEL[canon] in lab]
            if len(hit) != 1:
                raise SystemExit(f"{code}: {canon} maps to {hit}")
            prices[canon] = float(rows[hit[0]])
            if (stock.get(hit[0]) or 0) < 100:
                raise SystemExit(f"{code}: {canon} stock {stock.get(hit[0])}")
        img = next(x["img"] for x in cap["designs"] if x["name"].startswith(code))
        slug = re.sub(r"[^a-z0-9]+", "-", d["print_name"].lower()).strip("-")
        handle = f"{slug}-mommy-and-me-pajamas"
        up = ROOT / "uploads" / handle
        up.mkdir(parents=True, exist_ok=True)
        fname = f"01-{slug}-mommy-and-me-pajamas.jpg"
        shutil.copyfile(SCRATCH / f"cf_{code}.jpg", up / fname)
        kid = sorted({prices[s] for s in SIZES if s.startswith("Child")})
        adult = sorted({prices[s] for s in SIZES if s.startswith("Mom")})
        spec = {
            "mode": "mommy_me", "offer_id": OFFER, "offer_created": {"1083898601268": "2026-09-14", "1084574812798": "2026-09-13"}[OFFER], "design_code": code,
            "handle": handle, "shortcode": d["code"], "print_name": d["print_name"],
            "colors": [{"name": d["color"], "token": TOKENS[d["color"]]}],
            "color_pattern_gids": [C[p] for p in d["patterns"]], "color_pattern_labels": d["patterns"],
            "fabric_key": "coral_fleece", "title_variant": "fleece", "design_key": d["design_key"], "sleeve_style": "Long-Sleeve",
            "print_sentence": d["sentence"], "feature_label": d["feature"][0], "feature_text": d["feature"][1],
            "extra_tags": d["tags"] + ["Fleece", "Coral Fleece"], "media_alt": d["alt"],
            "image_url": img if img.startswith("http") else "https:" + img, "image_filename": fname,
            "ai_refs": [], "skip_ref_images": [],
            "chart_source": d["chart"], "chart_table": d["chart"],
            "chart_note": ("the offer publishes one 尺码展示 table per cut; this design uses the "
                           + ("zip stand-collar table (half chest doubled)" if d["chart"] == "srm_cf_zip" else "button-front table (full chest)")
                           + ", saved as SOURCE_SIZE_CHART; heights and weights come from the SKU labels; hip and waist are not published."),
            "child_price": "45.99", "adult_price": "52.99",
            "vendor_title": "珊瑚绒亲子睡衣 冬季加厚 (诗茹梦)",
            "vendor_color_values": [code], "vendor_codes": [code],
            "vendor_size_labels": SIZES,
            "vendor_prices_note": f"Child ¥{'/'.join(f'{x:g}' for x in kid)}; Women ¥{'/'.join(f'{x:g}' for x in adult)}.",
            "designs_note": f"Design {code} ({d['print_name']}) of the multi-design offer, one Shopify product.",
            "exclusions_note": "Size 8 and XXL appear in the size table but are not sold on this offer, so they are not listed.",
            "evidence_lines": [
                "Supplier: 深圳市诗茹梦制衣有限公司 (Shenzhen Shirumeng), 6 years on 1688, fulfillment 99.6%, 10,000+ dropship resellers, Guangdong origin, MOQ 1, 500 in stock per SKU. Page read 2026-09-27 in the helper browser with no login or captcha.",
                f"New-design gate: offer created {'2026-09-14' if OFFER == '1083898601268' else '2026-09-13'}; 'Year and season of release' Winter 2026;"
                " design screened for licensed characters and checked against the store's active and archived Mommy & Me pajamas.",
                "Fabric evidence: fabric name coral fleece, composition polyester fiber (content not stated), thickness thickened, function keep warm, season winter.",
                f"Vendor sizes kept: {', '.join(VENDOR_LABEL[s] for s in SIZES)} for design {code}.",
                "Each SKU is the matching top-and-pants set, so no Type axis is needed.",
            ],
        }
        (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(handle, d["code"], spec["vendor_prices_note"])


if __name__ == "__main__":
    main()
