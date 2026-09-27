#!/usr/bin/env python3
"""Specs for six 2026 family crewneck sweatshirts from 北京红旺博凯 (1688 store 225858),
the supplier behind the Together Heart sweater that sold on 2026-09-27 (order #9573).

Owner exception (2026-09-27, chat): list these 6 designs although the store fails the
48h pickup gate (86.4% vs 95%). Gate readings 2026-09-27: 13 years on 1688, repeat
buyers 95%, service 4.5, 30-day quality returns 0%, disputes 0%, AAA credit, warehouse
河南潢川. Every offer: listed 2026-08/09, release attribute Fall/Autumn 2026, fabric
54.4% cotton / 45.6% polyester brushed sweatshirt knit (description image 07).
Mode "family_sweatshirt" with title_variant "everyday" (no Christmas wording).

Pricing (owner rule: landed cost <= 50% of price on a single-item order): landed =
max colour cost + ¥3 domestic + YunExpress US ≈ ¥45.4 + ¥8.2/100 g (child 250 g,
adult 450 g), /7.11; price >= 2.06 x landed, rounded up to .99; compare-at +$10.
"""
import html
import json
import math
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
G = {"Red": "69600804961", "Yellow": "69622104161", "White": "69639733345", "Blue": "69639766113",
     "Beige": "69641928801", "Black": "69943132257", "Gray": "69944672353", "Pink": "69963645025",
     "Green": "70220546145", "Purple": "130284126305"}
# colour name -> (token, vendor key suffix without the 薄 prefix, pattern labels)
COLORS = {
    "Navy Raglan": ("NVR", "蓝杏拼", ["Blue", "Beige"]),
    "Red Raglan": ("RDR", "红杏拼", ["Red", "Beige"]),
    "Lilac Raglan": ("LLR", "灰紫拼", ["Purple", "Gray"]),
    "Cream": ("CRM", "杏色", ["Beige"]),
    "Pink": ("PNK", "粉色", ["Pink"]),
    "Light Blue": ("LBL", "蓝色", ["Blue"]),
    "Yellow": ("YLW", "黄色", ["Yellow"]),
    "Green": ("GRN", "果绿", ["Green"]),
    "Burgundy": ("BUR", "酒红色", ["Red"]),
    "Red": ("RED", "红色", ["Red"]),
    "Black": ("BLK", "黑色", ["Black"]),
    "White": ("WHT", "白色", ["White"]),
}
KIDS = ["90", "100", "110", "120", "130", "140", "150"]
ADULTS = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]
RAGLAN_NOTE = "Raglan colors have a cream body with contrast sleeves and neckline."
DESIGNS = [
    dict(offer="1076003819393", listed="2026-08-24", name="Smiley Heart", code="SMHT", chart="hw_sweat",
         colors=["Navy Raglan", "Red Raglan", "Lilac Raglan", "Cream", "Pink", "Light Blue", "Yellow"],
         sentence="A small red scribble heart with a smiling face sits on the left chest. " + RAGLAN_NOTE,
         feature=("Smiling heart print:", "A hand-drawn red heart with a happy face, small and sweet on the chest."),
         tags=["Heart", "Heart Graphic", "Smiley", "Raglan"],
         alt="Family in matching cream sweatshirts with navy or red raglan sleeves and a small smiling red heart on the chest.",
         main="17.jpg", refs=["18.jpg", "30.jpg"], title_cn="高级感一家四口亲子装卫衣甄选舒适面料百搭全家福出游氛围感穿搭"),
    dict(offer="1084313044599", listed="2026-09-12", name="Eternal Bliss Hearts", code="EBHT", chart="hw_sweat",
         colors=["Navy Raglan", "Red Raglan", "Lilac Raglan", "Cream", "Pink", "Light Blue", "Yellow"],
         sentence="Two outlined hearts in berry and pink hold the script \"Eternal bliss\" on the chest, with tiny stars. " + RAGLAN_NOTE,
         feature=("Double heart print:", "Two linked hearts with the words \"Eternal bliss\" for a sweet family look."),
         tags=["Heart", "Heart Graphic", "Double Heart", "Raglan"],
         alt="Family in matching cream raglan sweatshirts with navy or red sleeves and two outlined hearts with Eternal bliss script.",
         main="17.jpg", refs=["19.jpg", "32.jpg"], title_cn="爱心母女装2026秋冬新款圆领印花卫衣亲子装韩版套头衫打底上衣"),
    dict(offer="1086910652023", listed="2026-09-21", name="Little Heart", code="LHRT", chart="hw_gh",
         colors=["Burgundy", "Red", "Black", "Cream", "Pink", "Light Blue", "Green"],
         sentence="One small heart on the chest: a gold heart on the burgundy, red and black sweatshirts, and a red heart on the cream, pink, light blue and green ones.",
         feature=("Little heart print:", "A simple heart on the chest, gold on the dark colors and red on the light ones."),
         tags=["Heart", "Heart Graphic", "Minimalist", "Burgundy"],
         alt="Family in matching burgundy crewneck sweatshirts with a small gold heart on the chest.",
         main="00.jpg", refs=["01.jpg", "18.jpg"], title_cn="韩系氛围感母女装写真拍照出片红色上衣秋冬加绒亲子装打底卫衣"),
    dict(offer="1082179667858", listed="2026-09-15", name="Good Luck Smile", code="GLSM", chart="hw_sweat",
         colors=["Navy Raglan", "Lilac Raglan", "Red Raglan", "Cream", "Pink", "Yellow", "Light Blue"],
         sentence="A big smiley face fills the chest above the words \"GOOD LUCK\", in a tone that suits each color. " + RAGLAN_NOTE,
         feature=("Big smile print:", "A cheerful oversized smiley with GOOD LUCK lettering across the front."),
         tags=["Smiley", "Smiley Face", "Good Luck", "Raglan"],
         alt="Family in matching pink and light blue sweatshirts with a big smiley face and GOOD LUCK lettering.",
         main="10.jpg", refs=["11.jpg", "19.jpg"], title_cn="源头工厂批发亲子装2026秋冬新款加绒加厚全家服笑脸印花卫衣现货"),
    dict(offer="1074814309624", listed="2026-08-13", name="Moon and Star", code="MNST", chart="hw_sweat",
         colors=["Light Blue", "White", "Cream", "Pink", "Yellow", "Green", "Black"],
         sentence="Small line-art prints on the chest: a crescent moon over the water with a tiny star on the adult sweatshirts, and a small blue star over the water on the child sweatshirts.",
         feature=("Moon and star print:", "A little moon for the grown-ups and a little star for the kids."),
         tags=["Moon", "Star", "Minimalist"],
         alt="Family in matching light blue crewneck sweatshirts with a small moon print for parents and a star print for kids.",
         main="01.jpg", refs=["03.jpg", "27.jpg"], title_cn="秋季上新蓝色日月星氛围感亲子装卫衣一家三口旅游度假拍照上衣",
         vendor_kid="宝宝{}", vendor_adult="妈妈{}"),  # 日月星: 妈妈 SKUs carry the moon (爸爸 = sun); every adult size ships the moon print
    dict(offer="1083117200368", listed="2026-09-08", name="Starry Sky", code="STSK", chart="hw_sweat",
         colors=["Pink", "Red Raglan", "Yellow", "Green", "Cream", "Navy Raglan", "Lilac Raglan"],
         sentence="A bunch of hand-drawn stars in navy, red, green and yellow sits on the chest above the tiny script \"a sky full of stars\". " + RAGLAN_NOTE,
         feature=("Star cluster print:", "Colorful outlined stars with a little script line underneath."),
         tags=["Stars", "Star", "Raglan"],
         alt="Family in matching pink sweatshirts with a colorful cluster of hand-drawn stars on the chest.",
         main="16.jpg", refs=["17.jpg", "26.jpg"], title_cn="繁星闪印亲子装春秋圆领卫衣户外露营出游母女装情侣拍照百搭上衣"),
]


def price(cost_cny: float, grams: int) -> float:
    landed = (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def main():
    cap = json.loads((SCRATCH / "hw_designs.json").read_text(encoding="utf-8"))
    for d in DESIGNS:
        o = d["offer"]
        prices = {html.unescape(k): float(v) for k, v in cap[o]["prices"].items()}
        stock = {html.unescape(k): v for k, v in cap[o]["stock"].items()}
        plain = o == "1082179667858"  # this offer's keys carry no 薄 (standard-weight) prefix
        vk, va = d.get("vendor_kid", "{}"), d.get("vendor_adult", "{}")
        kid_cost, adult_cost = 0.0, 0.0
        for c in d["colors"]:
            key_c = ("" if plain else "薄") + COLORS[c][1]
            for s in KIDS + ADULTS:
                key = f"{key_c}>{(vk if s in KIDS else va).format(s)}"
                if key not in prices or (stock.get(key) or 0) < 50:
                    raise SystemExit(f"{o}: missing or low stock {key} {stock.get(key)}")
                if s in KIDS:
                    kid_cost = max(kid_cost, prices[key])
                else:
                    adult_cost = max(adult_cost, prices[key])
        cp, ap = price(kid_cost, 250), price(adult_cost, 450)
        slug = d["name"].lower().replace(" ", "-")
        handle = f"{slug}-family-matching-sweatshirts"
        up = ROOT / "uploads" / handle
        up.mkdir(parents=True, exist_ok=True)
        fname = f"01-{slug}-family-sweatshirts.jpg"
        (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{o}/desc/{d['main']}").read_bytes())
        man = json.loads((ROOT / f"ops/sourcing/vendor-images/{o}/desc/manifest.json").read_text(encoding="utf-8"))
        patterns = list(dict.fromkeys(p for c in d["colors"] for p in COLORS[c][2]))
        vendor_colors = [("" if plain else "薄") + COLORS[c][1] for c in d["colors"]]
        spec = {
            "mode": "family_sweatshirt", "title_variant": "everyday",
            "offer_id": o, "offer_created": d["listed"], "handle": handle, "shortcode": d["code"], "print_name": d["name"],
            "colors": [{"name": c, "token": COLORS[c][0]} for c in d["colors"]],
            "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in patterns],
            "color_pattern_labels": patterns,
            "fabric_key": "cotton_blend_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
            "print_sentence": d["sentence"], "feature_label": d["feature"][0], "feature_text": d["feature"][1],
            "extra_tags": d["tags"], "media_alt": d["alt"],
            "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/" + d["main"])),
            "image_filename": fname, "ai_refs": d["refs"],
            "chart_source": d["chart"], "chart_table": d["chart"],
            "chart_note": ("the offer's own description publishes the supplier's 卫衣尺码表 (description image "
                           + ("10" if d["chart"] == "hw_gh" else "08")
                           + "), saved as SOURCE_SIZE_CHART; full chest as published, weight converted from jin to kg."),
            "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
            "vendor_title": d["title_cn"],
            "vendor_color_values": vendor_colors, "vendor_codes": [],
            "vendor_size_labels": [f"Child {s}" for s in KIDS] + [f"Adult {s}" for s in ADULTS],
            "vendor_prices_note": f"Child up to ¥{kid_cost:g}; Adult up to ¥{adult_cost:g} (standard weight, chosen colors).",
            "designs_note": f"One design in {len(d['colors'])} colors as one Shopify product with a Color option.",
            "exclusions_note": "Fleece-lined (绒) versions, trousers sold separately and baby rompers are not listed; props, caps and sunglasses in the vendor photos are not sold.",
            "evidence_lines": [
                "Supplier: 北京红旺博凯商贸有限公司 (1688 store 225858), 13 years on 1688, repeat buyers 95%, service 4.5, 30-day 48h pickup 86.44% (owner exception 2026-09-27), quality returns 0%, disputes 0%. Source of the Together Heart sweater sold 2026-09-27.",
                f"New-design gate: offer listed {d['listed']}; release attribute Fall/Autumn 2026; checked against the store's sweaters, sweatshirts and tops for duplicates.",
                "Fabric evidence: description image 07 lists 54.4% cotton and 45.6% polyester; attribute table: cotton, 55% main fabric.",
                f"Colors kept: {', '.join(d['colors'])} ({', '.join(vendor_colors)}); sizes 90-150 and S-4XL, stock >= 50 per SKU.",
            ],
        }
        (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(handle, f"child ${cp:.2f} (¥{kid_cost:g})", f"adult ${ap:.2f} (¥{adult_cost:g})")


if __name__ == "__main__":
    main()
