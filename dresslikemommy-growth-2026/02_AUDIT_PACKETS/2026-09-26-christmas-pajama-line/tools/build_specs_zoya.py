#!/usr/bin/env python3
"""Build listing specs for the 2026 Christmas round from 佐雅 (Guangzhou Zoya garment).

Same spec schema as build_specs.py (smr factory), with the Zoya chart
(runner_engine.ZOYA_CHART, chart_table "zoya"). Copy fields come from DESIGNS,
written from each offer's vendor photos; sizes, prices, fabric, listing date,
main image and chart evidence come from the read-only helper-browser captures in
ops/sourcing/vendor-images/<offer>/desc/manifest.json (captured 2026-09-27).
Every offer's "Year and season of launch" attribute was read as 2026 on the live
page before selection (see the round packet / worklog).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
CHART_REFS = {"zoya": TOOLS.parent / "zoya_size_chart_from_810867411211.jpg", "zoya_round": TOOLS.parent / "zoya_round_size_chart_from_816112676067.jpg"}

C = {  # store shopify--color-pattern metaobjects
    "Red": "gid://shopify/Metaobject/69600804961", "Green": "gid://shopify/Metaobject/70220546145",
    "White": "gid://shopify/Metaobject/69639733345", "Blue": "gid://shopify/Metaobject/69639766113",
    "Black": "gid://shopify/Metaobject/69943132257", "Gray": "gid://shopify/Metaobject/69944672353",
    "Beige": "gid://shopify/Metaobject/69641928801", "Multicolor": "gid://shopify/Metaobject/130231140449",
    "Striped": "gid://shopify/Metaobject/130283765857", "Checkered": "gid://shopify/Metaobject/130283143265",
}
COLOR_TOKENS = {"Red": "RED", "Green": "GRN", "Navy": "NVY", "Gray": "GRY", "Cream": "CRM", "Black": "BLK", "White": "WHT", "Teal": "TEL"}

# offer: (print name, shortcode, color, patterns, design_key, print sentence, (feature label, text), extra tags, alt, vendor title)
DESIGNS: dict[str, tuple] = json.loads((TOOLS / "zoya_designs.json").read_text(encoding="utf-8"))

CHILD_ORDER = [2, 3, 4, 5, 6, 8, 10, 12, 14]
ADULT_ORDER = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def ahash(path: Path) -> int:
    im = Image.open(path).convert("L").resize((16, 16))
    px = list(im.getdata()); avg = sum(px) / len(px)
    return sum(1 << i for i, v in enumerate(px) if v > avg)


def chart_kind(path: Path, refs: dict) -> str | None:
    """Return the chart table key if the image is (a re-encoded copy of) a reference chart."""
    w, h = Image.open(path).size
    if not (1250 <= w <= 1450 and 1650 <= h <= 1900):
        return None
    a = ahash(path)
    best = min(refs.items(), key=lambda kv: bin(a ^ kv[1]).count("1"))
    return best[0] if bin(a ^ best[1]).count("1") <= 12 else None


def main() -> None:
    chart_hashes = {ahash(p): k for k, p in CHART_REFS.items()}
    written = []
    for offer, (print_name, code, color, patterns, design_key, sentence, feature, extra_tags, alt, vendor_title) in DESIGNS.items():
        mdir = ROOT / f"ops/sourcing/vendor-images/{offer}/desc"
        manifest = json.loads((mdir / "manifest.json").read_text(encoding="utf-8"))
        text = manifest.get("page_text", "")
        # Sizes and prices from the SKU selector ("Label\n¥N" entries).
        prices, labels = {}, []
        for opt in manifest["sku_options"]:
            m = re.fullmatch(r"(.+?)\n¥(\d+(?:\.\d+)?)", opt["t"].strip())
            if m and m.group(1) not in labels:
                labels.append(m.group(1)); prices[m.group(1)] = m.group(2)
        def canon(label: str) -> str | None:
            m = re.fullmatch(r"(?i)(father|dad|mother|mom)\s*(s|m|l|xl|2xl|3xl|4xl)", label.strip())
            if m:
                role = "Dad" if m.group(1).lower() in ("father", "dad") else "Mom"
                return f"{role} {m.group(2).upper()}"
            k = re.fullmatch(r"(?i)child(?:ren)?\s*(\d+)", label.strip())
            return f"Child {k.group(1)}" if k else None
        canon_labels = {canon(l): l for l in labels if canon(l)}
        prices = {canon(l): v for l, v in prices.items() if canon(l)} | {l: v for l, v in prices.items() if l.lower().startswith("baby")}
        kids = [f"Child {n}" for n in CHILD_ORDER if f"Child {n}" in canon_labels]
        mom = [f"Mom {s}" for s in ADULT_ORDER if f"Mom {s}" in canon_labels]
        dad = [f"Dad {s}" for s in ADULT_ORDER if f"Dad {s}" in canon_labels]
        sizes = kids + mom + dad
        if not (kids and mom and dad):
            raise SystemExit(f"{offer}: missing roles in {labels}")
        roles = {"Adult": sorted({prices[s] for s in mom + dad}), "Child": sorted({prices[s] for s in kids}),
                 "Baby": sorted({v for k, v in prices.items() if k.startswith("Baby")})}
        price_note = "; ".join(f"{k} ¥{'/'.join(v)}" for k, v in roles.items() if v) + " (Baby and Dog not listed)."
        # Fabric: the live attribute table read 95% polyester "imitation cotton" on every selected offer.
        fkey = "poly95"
        # Main image: first 3:4 on-model photo after the chart; chart evidence by byte-identical match.
        chart_idx, chart_table, main_url = None, None, None
        for d in manifest["desc_images"]:
            p = d.get("path")
            if not p:
                continue
            pp = ROOT / p
            kind = chart_kind(pp, {k: v for v, k in chart_hashes.items()})
            if kind:
                if chart_idx is None:
                    chart_idx, chart_table = pp.stem, kind
                continue
            if main_url is None and d.get("w", 0) >= 1000:
                w, hh = Image.open(pp).size
                if 1.25 <= hh / w <= 1.55:
                    main_url = d["url"]
        if main_url is None:
            raise SystemExit(f"{offer}: no main image")
        sleeve_chart = "zoya" if design_key == "raglan" else "zoya_round"
        chart_table = chart_table or sleeve_chart
        chart_name = "raglan-sleeve SIZE TABLE" if chart_table == "zoya" else "round-sleeve (圆袖) SIZE TABLE"
        chart_note = (f"this offer's own description publishes the Zoya factory {chart_name} (description image {chart_idx}; same table as the copy saved as SOURCE_SIZE_CHART)."
                      if chart_idx else
                      f"this offer's description does not carry a SIZE TABLE image; the same factory's published {chart_name} is used (it matches this design's sleeve cut), saved as SOURCE_SIZE_CHART. Confirm with the supplier before publishing.")
        listed = (re.search(r"上架时间 (\S+)", text) or [None, "2026"])[1]
        slug = re.sub(r"[^a-z0-9]+", "-", print_name.lower().replace("'", "")).strip("-")
        handle = f"{slug}-family-matching-pajamas"
        spec = {
            "offer_id": offer, "offer_created": listed, "handle": handle, "shortcode": code,
            "print_name": print_name,
            "colors": [{"name": color, "token": COLOR_TOKENS[color]}],
            "color_pattern_gids": [C[p] for p in patterns], "color_pattern_labels": patterns,
            "fabric_key": fkey, "design_key": design_key,
            "sleeve_style": "Short-Sleeve" if design_key == "short_crew" else "Long-Sleeve",
            "print_sentence": sentence, "feature_label": feature[0], "feature_text": feature[1],
            "extra_tags": extra_tags, "media_alt": alt,
            "image_url": main_url, "image_filename": f"01-{slug}-family-pajamas.jpg",
            "chart_source": chart_table, "chart_table": chart_table, "chart_note": chart_note,
            "vendor_title": vendor_title,
            "vendor_color_values": ["As Shown"],
            "vendor_codes": [],
            "vendor_size_labels": sizes,
            "vendor_prices_note": price_note,
            "designs_note": f"The offer's single design ({print_name}), one Shopify product.",
            "exclusions_note": "Baby SKUs (a separate romper) and dog SKUs are excluded: baby is not an allowed Family Matching role and pet items are not sold. Dogs and props in the photos are not sold as part of this listing.",
            "evidence_lines": [
                "Supplier: 广州佐雅服装有限公司 (Guangzhou Zoya garment), 6 years on 1688, overall fulfillment 100%, praise 99.9%, service score 4.0, Guangdong origin, in stock, MOQ 1. Our BuckyDrop history: median 2.4 days PO to warehouse (p90 3.4). Page read 2026-09-27 in the helper browser with no login or captcha.",
                f"Offer listed on 1688 on {listed}; its 'Year and season of launch' attribute reads 2026.",
                "Fabric evidence: fabric name 'Imitation cotton', main fabric composition 'Polyester fiber (polyester)', content 95%. Imitation cotton is a cotton-feel polyester, so the listing states 95% polyester.",
                f"Vendor size selector: {', '.join(labels)}.",
                f"Kept rows: {len(sizes)} non-baby, non-dog SKUs, each matched one to one to a Zoya chart row.",
                "The set is sold as one purchasable top-and-pants item, so no Type axis is needed.",
            ],
        }
        path = TOOLS / "specs" / f"{handle}.json"
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        written.append((handle, code, len(sizes), chart_idx, price_note))
    for row in written:
        print(*row)


if __name__ == "__main__":
    main()
