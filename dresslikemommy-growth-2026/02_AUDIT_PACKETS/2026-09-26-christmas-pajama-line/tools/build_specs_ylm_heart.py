#!/usr/bin/env python3
"""Scribble Heart (rainbow graffiti heart) family crewneck sweatshirt from 合肥野狼魅力制衣有限公司 (1688 offer 1085930330528).

Gate read 2026-09-28 (store creditdetail): 13 years on 1688, 48h pickup 99.56%, 48h fulfillment 99.56%,
service 4.0, 18,276 orders in 30 days. Offer: "48-Hour Shipping" (owner's 24-48h rule), release
2026年秋季, fabric 棉 100% (content 100), MOQ 1, ships from Hefei. Standard (春秋款) weight only: the
fleece-lined (加绒款) versions and the sweatpants are not listed. Sizes 100-160 cm and M-4XL
(5XL has no store size metaobject and is left out).
Chart: the offer's own 尺码信息 (description image 04): full chest as published; kids' weights from the
age strip (jin -> kg), adult weights from the table (jin -> kg).
Pricing per the owner's 50%-landed rule (child 250 g, adult 450 g), compare-at +$10.
"""
import html
import json
import math
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
OFFER = "1085930330528"
COLORS = {"White": ("(春秋款)-白色", "WHT", "White"), "Pink": ("(春秋款)-粉色", "PNK", "Pink"),
          "Light Blue": ("(春秋款)-浅蓝", "LBL", "Blue"), "Red": ("(春秋款)-红色", "RED", "Red")}
G = {"White": "69639733345", "Pink": "69963645025", "Blue": "69639766113", "Red": "69600804961"}
# vendor size: (chart label, picker, suffix, age, length, chest, sleeve, pant, waist, hip)
ROWS = {
    "Child 100": ("100 (90-100 cm)", "Child 2-3 Years", "KID23Y", "2-3", 40, 70, 30, "-", "-", "-"),
    "Child 110": ("110 (100-110 cm)", "Child 4 Years", "KID4Y", "4", 43, 74, 33, "-", "-", "-"),
    "Child 120": ("120 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 46, 78, 35, "-", "-", "-"),
    "Child 130": ("130 (120-130 cm)", "Child 6-7 Years", "KID67Y", "6-7", 49, 82, 39, "-", "-", "-"),
    "Child 140": ("140 (130-140 cm)", "Child 9-10 Years", "KID910Y", "9-10", 52, 86, 41, "-", "-", "-"),
    "Child 150": ("150 (140-150 cm)", "Child 11-12 Years", "KID1112Y", "11-12", 56, 90, 44, "-", "-", "-"),
    "Child 160": ("160 (150-160 cm)", "Child 13-14 Years", "KID1314Y", "13-14", 59, 96, 48, "-", "-", "-"),
    "Adult M": ("Adult M", "Adult M", "M", "—", 63, 96, 53, "-", "-", "-"),
    "Adult L": ("Adult L", "Adult L", "L", "—", 65, 100, 55, "-", "-", "-"),
    "Adult XL": ("Adult XL", "Adult XL", "XL", "—", 67, 104, 57, "-", "-", "-"),
    "Adult 2XL": ("Adult 2XL", "Adult 2XL", "2XL", "—", 69, 108, 58, "-", "-", "-"),
    "Adult 3XL": ("Adult 3XL", "Adult 3XL", "3XL", "—", 71, 112, 59, "-", "-", "-"),
    "Adult 4XL": ("Adult 4XL", "Adult 4XL", "4XL", "—", 73, 116, 60, "-", "-", "-"),
}
FIT = {  # (height cm, weight kg)
    "Child 100": ("90-100", "12.5-15"), "Child 110": ("100-110", "15-18.5"), "Child 120": ("110-120", "18.5-22.5"),
    "Child 130": ("120-130", "22.5-28"), "Child 140": ("130-140", "28-34"), "Child 150": ("140-150", "34-40"),
    "Child 160": ("150-160", "40-50"), "Adult M": ("155-165", "42.5-47.5"), "Adult L": ("165-170", "47.5-55"),
    "Adult XL": ("170-175", "55-62.5"), "Adult 2XL": ("175-180", "62.5-70"), "Adult 3XL": ("180-185", "70-77.5"),
    "Adult 4XL": ("185-190", "77.5-85"),
}


def price(cost_cny: float, grams: int) -> float:
    landed = (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def main():
    cap = json.loads((SCRATCH / "heart_designs.json").read_text(encoding="utf-8"))[OFFER]
    prices = {html.unescape(k): float(v) for k, v in cap["prices"].items()}
    stock = {html.unescape(k): v for k, v in cap["stock"].items()}
    kid = adult = 0.0
    for _, (vc, _, _) in COLORS.items():
        for lab in ROWS:
            key = f"{vc}>{lab.replace('Child ', '') + 'cm' if lab.startswith('Child') else lab.replace('Adult ', '')}"
            if key not in prices or (stock.get(key) or 0) < 40:
                raise SystemExit(f"missing/low {key} {stock.get(key)}")
            if lab.startswith("Child"):
                kid = max(kid, prices[key])
            else:
                adult = max(adult, prices[key])
    cp, ap = price(kid, 250), price(adult, 450)
    handle = "scribble-heart-family-matching-sweatshirts"
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = "01-scribble-heart-family-sweatshirts.jpg"
    (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/00.jpg").read_bytes())
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/manifest.json").read_text(encoding="utf-8"))
    pats = list(dict.fromkeys(v[2] for v in COLORS.values()))
    spec = {
        "mode": "family_sweatshirt", "title_variant": "everyday",
        "offer_id": OFFER, "offer_created": "2026-09", "handle": handle, "shortcode": "SCHT", "print_name": "Scribble Heart",
        "colors": [{"name": c, "token": v[1]} for c, v in COLORS.items()],
        "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in pats], "color_pattern_labels": pats,
        "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
        "print_sentence": "A big rainbow scribble heart is printed on the chest of a soft cotton crewneck sweatshirt in white, pink, light blue or red.",
        "feature_label": "Scribble heart:", "feature_text": "A bright hand-drawn heart in rainbow colors that pops in family photos.",
        "extra_tags": ["Scribble Heart", "Heart", "Rainbow", "White", "Pink", "Light Blue", "Red"],
        "media_alt": "Family in matching white crewneck sweatshirts with a big rainbow scribble heart on the chest.",
        "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/00.jpg")),
        "image_filename": fname, "ai_refs": ["00.jpg", "05.jpg"],
        "chart_source": "ylm_heart", "chart_table": "ylm_heart",
        "chart_rows": {k: list(v) for k, v in ROWS.items()}, "fit_rows": {k: list(v) for k, v in FIT.items()},
        "chart_image": f"ops/sourcing/vendor-images/{OFFER}/desc/04.jpg",
        "chart_note": "the offer's own description publishes the supplier's 尺码信息 (description image 04, kids and adult tables with an age strip), saved as SOURCE_SIZE_CHART; full chest as published; weights converted from jin to kg.",
        "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
        "vendor_title": "儿童涂鸦爱心印花卫衣亲子装2026新款秋冬圆领男女同款情侣上衣潮",
        "vendor_color_values": [v[0] for v in COLORS.values()], "vendor_codes": [],
        "vendor_size_labels": list(ROWS),
        "vendor_prices_note": f"Child ¥{kid:g}; Adult ¥{adult:g} (standard weight).",
        "designs_note": "One design (graffiti heart) in four colours as one Shopify product.",
        "exclusions_note": "Fleece-lined versions, the other four colours, sweatpants and size 5XL are not listed; props are not sold.",
        "evidence_lines": [
            "Supplier: 合肥野狼魅力制衣有限公司, 13 years on 1688, 48h pickup 99.56%, 48h fulfillment 99.56%, service 4.0, 18,276 orders/30d (creditdetail read 2026-09-28).",
            "Owner 24-48h rule: offer page shows '48-Hour Shipping' (deliveryLimit 2); MOQ 1.",
            "Fresh-and-in-season gate: release attribute 2026年秋季; offer id 1085930330528 is a September 2026 listing.",
            "Fabric evidence: main fabric 棉, content 100 (100% cotton).",
            "Vendor sizes 100-160 cm and M-5XL in each colour; stock 1000 per SKU; 5XL not listed.",
        ],
    }
    (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(handle, f"child ${cp:.2f} (¥{kid:g})", f"adult ${ap:.2f} (¥{adult:g})")


if __name__ == "__main__":
    main()
