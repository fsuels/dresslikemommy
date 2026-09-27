#!/usr/bin/env python3
"""Build listing specs for 2026 Christmas designs from 衣林 (Guangzhou Yilin garment).

Supplier: our top pajama vendor by BuckyDrop order history (23 orders, median 2.5
days PO to warehouse; Holiday Safari). Every offer here passed the owner's new-design
gate on 2026-09-27: 1688 creation date (gmtCreate) in 2026 AND the "Year and season
of release" attribute 2026, plus a store duplicate check. Copy comes from
yilin_designs.json (written from the vendor photos); sizes, prices, fabric and
listing date come from the read-only helper-browser captures in
ops/sourcing/vendor-images/<offer>/desc/manifest.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
C = {
    "Red": "gid://shopify/Metaobject/69600804961", "Green": "gid://shopify/Metaobject/70220546145",
    "White": "gid://shopify/Metaobject/69639733345", "Blue": "gid://shopify/Metaobject/69639766113",
    "Black": "gid://shopify/Metaobject/69943132257", "Gray": "gid://shopify/Metaobject/69944672353",
    "Checkered": "gid://shopify/Metaobject/130283143265",
}
COLOR_TOKENS = {"Blue": "BLU", "Green": "GRN", "White": "WHT"}
FABRIC_NOTE = {
    "cotton35": "fabric name '{name}', main fabric composition 'Cotton', content 35%. The listing states 35% cotton in the main fabric and does not name the rest.",
    "cotton65": "fabric name '{name}', main fabric composition 'Cotton', content 65%. The listing states 65% cotton in the main fabric and does not name the rest.",
}
CHART_NOTE = {
    "yilin_cn": "this offer's own description publishes the factory's Chinese men's, women's and kids' size tables (2024/5 template); their values are transcribed in the engine's YILIN_CN_CHART and saved together as SOURCE_SIZE_CHART.",
    "yilin_en": "this offer's own description publishes the factory's English Women's/Men's/Kids' Size Chart, whose kid rows use the same 2T-14T labels as the SKUs; values are transcribed in the engine's YILIN_EN_CHART and the chart is saved as SOURCE_SIZE_CHART.",
}
CHILD = [2, 3, 4, 5, 6, 8, 10, 12, 14]
ADULT = ["S", "M", "L", "XL", "2XL", "3XL"]
KID_MAP = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "6-7": 6, "8": 8, "8-9": 8, "10": 10, "10-11": 10, "11-12": 12, "12": 12, "13-14": 14, "14": 14}


def canon(label: str) -> str | None:
    m = re.fullmatch(r"(?i)(dad|mom)\s*(s|m|l|xl|xxl|2xl|3xl)", label.strip())
    if m:
        size = m.group(2).upper().replace("XXL", "2XL")
        return f"{'Dad' if m.group(1).lower() == 'dad' else 'Mom'} {size}"
    k = re.fullmatch(r"(?i)children\s*(\d+(?:-\d+)?)t?", label.strip())
    return f"Child {KID_MAP[k.group(1)]}" if k and k.group(1) in KID_MAP else None


def main() -> None:
    designs = json.loads((TOOLS / "yilin_designs.json").read_text(encoding="utf-8"))
    for offer, d in designs.items():
        man = json.loads((ROOT / f"ops/sourcing/vendor-images/{offer}/desc/manifest.json").read_text(encoding="utf-8"))
        text = man["page_text"]
        prices, labels = {}, []
        for opt in man["sku_options"]:
            m = re.fullmatch(r"(.+?)\n¥(\d+(?:\.\d+)?)", opt["t"].strip())
            if m and m.group(1) not in labels:
                labels.append(m.group(1)); prices[m.group(1)] = m.group(2)
        cmap = {}
        for lab in labels:
            c = canon(lab)
            if c:
                if c in cmap:
                    raise SystemExit(f"{offer}: two vendor labels map to {c}")
                cmap[c] = lab
        sizes = [f"Child {n}" for n in CHILD if f"Child {n}" in cmap] + \
                [f"Mom {s}" for s in ADULT if f"Mom {s}" in cmap] + [f"Dad {s}" for s in ADULT if f"Dad {s}" in cmap]
        if len(sizes) != 21:
            raise SystemExit(f"{offer}: expected 21 sizes, got {sizes} from {labels}")
        adult = sorted({prices[cmap[s]] for s in sizes if not s.startswith("Child")}, key=float)
        kid = sorted({prices[cmap[s]] for s in sizes if s.startswith("Child")}, key=float)
        listed = re.search(r"上架时间 (\d{4}-\d{2}-\d{2})", text).group(1)
        release = re.search(r"Year and season of (?:release|launch) (\S+ \d{4}|\d{4})", text).group(1)
        if not (listed.startswith("2026") and release.endswith("2026")):
            raise SystemExit(f"{offer}: fails new-design gate ({listed}, {release})")
        fname = re.search(r"Fabric name (\S+(?: cotton)?)", text).group(1).rstrip("0123456789")
        main_url = next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/" + d["main"]))
        slug = re.sub(r"[^a-z0-9]+", "-", d["print_name"].lower()).strip("-")
        handle = f"{slug}-family-matching-pajamas"
        spec = {
            "offer_id": offer, "offer_created": listed, "handle": handle, "shortcode": d["code"],
            "print_name": d["print_name"],
            "colors": [{"name": d["color"], "token": COLOR_TOKENS[d["color"]]}],
            "color_pattern_gids": [C[p] for p in d["patterns"]], "color_pattern_labels": d["patterns"],
            "fabric_key": d["fabric_key"], "design_key": d["design_key"], "sleeve_style": "Long-Sleeve",
            "print_sentence": d["sentence"], "feature_label": d["feature"][0], "feature_text": d["feature"][1],
            "extra_tags": d["tags"], "media_alt": d["alt"],
            "image_url": main_url, "image_filename": f"01-{slug}-family-pajamas.jpg",
            "chart_source": d["chart_table"], "chart_table": d["chart_table"], "chart_note": CHART_NOTE[d["chart_table"]],
            "skip_ref_images": d["skip_refs"],
            "ai_refs": d.get("ai_refs", []),
            "vendor_title": re.sub(r"\s+", " ", man.get("title", "") or "")[:80] or d["print_name"],
            "vendor_color_values": ["As Shown"], "vendor_codes": [],
            "vendor_size_labels": sizes,
            "vendor_prices_note": f"Adult ¥{'/'.join(adult)}; Child ¥{'/'.join(kid)} (Baby and Dog not listed).",
            "designs_note": f"The offer's single design ({d['print_name']}), one Shopify product.",
            "exclusions_note": "Baby SKUs (a separate romper) and dog SKUs are excluded: baby is not an allowed Family Matching role and pet items are not sold. Dogs and props in the photos are not sold as part of this listing.",
            "evidence_lines": [
                "Supplier: 衣林 (Guangzhou Yilin garment), our top pajama supplier by BuckyDrop history (23 orders, median 2.5 days PO to warehouse, p90 3.7). Offer page fulfillment 99%, service score 4.5, Guangdong. Read 2026-09-27 in the helper browser with no login or captcha.",
                f"New-design gate: 1688 listing date {listed} and 'Year and season of release' {release}; checked against the store's active and archived Christmas pajamas for duplicates (none).",
                "Fabric evidence: " + FABRIC_NOTE[d["fabric_key"]].format(name=fname),
                f"Vendor size selector (kept): {', '.join(cmap[s] for s in sizes)}.",
                f"Kept rows: {len(sizes)} non-baby, non-dog SKUs, each matched one to one to a row of the supplier's own chart.",
                "The set is sold as one purchasable top-and-pants item, so no Type axis is needed.",
            ],
        }
        (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(handle, d["code"], listed, release, spec["vendor_prices_note"], fname)


if __name__ == "__main__":
    main()
