#!/usr/bin/env python3
"""Specs for two 2026 family knit sweaters from 东莞市森大服饰有限公司 (1688 store
senda831, Dongguan, Guangdong). New Tier B vendor; passes every gate on 2026-09-27:
9 years on 1688, 48h pickup 97.64%, 48h fulfillment 99.70%, quality returns 0%,
disputes 0%, repeat buyers 82%, service 4.5, 843 paid orders in 30 days.
Offers listed 2026-09-22/23; release attribute 2026年秋季; fabric listed as modal
(莫代尔), thick. Mode "family_sweatshirt" with garment "sweater" (knit variant).

Pricing (owner rule: landed <= 50% of price on a single-item order): max colour cost
+ ¥3 domestic + YunExpress US ≈ ¥45.4 + ¥8.2/100 g (knit child 350 g, adult 650 g),
/7.11; price >= 2.06 x landed rounded up to .99; compare-at +$10.
"""
import html
import json
import math
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
G = {"Red": "69600804961", "White": "69639733345", "Beige": "69641928801", "Black": "69943132257", "Gray": "69944672353"}
KIDS = ["80", "90", "100", "110", "120", "130", "140", "150", "160"]
ADULTS = {"S": "S", "M": "M", "L": "L", "XL": "XL", "2XL": "XXL", "3XL": "3XL", "4XL": "4XL"}
DESIGNS = [
    dict(offer="1084384863476", listed="2026-09-23", name="Nordic Yoke", code="NDYK",
         colors=[("Cream", "CRM", "米白色", ["Beige", "Black"]), ("Gray", "GRY", "灰色", ["Gray", "Black", "White"])],
         sentence="A Nordic-style knit yoke in black and white circles the shoulders of the cream or gray sweater, with small diamond and dot bands.",
         feature=("Nordic yoke:", "A classic patterned knit yoke that looks great in cozy family photos."),
         tags=["Fair Isle", "Nordic", "Christmas Sweaters", "Cream", "Gray"],
         alt="Family in matching cream and gray knit sweaters with a black and white Nordic patterned yoke.",
         main="02.jpg", refs=["01.jpg", "06.jpg"], title_cn="2026新款秋冬加厚亲子装毛衣圆领长袖针织衫洋气童装情侣装家庭装"),
    dict(offer="1086122061333", listed="2026-09-22", name="Pom-Pom Star", code="PPST",
         colors=[("Red", "RED", "酒红色", ["Red", "White"])],
         sentence="A big fuzzy cream star outline with little red pom-poms at its points sits on the front of the red knit sweater, with the word \"STAR\" embroidered inside and a small star on one shoulder.",
         feature=("Fuzzy star:", "A soft, textured cream star with red pom-poms for a playful holiday look."),
         tags=["Star", "Pom-Pom", "Christmas Sweaters", "Red"],
         alt="Family in matching red knit sweaters with a big fuzzy cream star and red pom-poms on the front.",
         main="00.jpg", refs=["20.jpg", "06.jpg"], title_cn="秋冬新款加厚喜庆红色亲子装毛衣长袖圆领套头童装情侣装家庭装"),
]


def price(cost_cny: float, grams: int) -> float:
    landed = (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def main():
    cap = json.loads((SCRATCH / "knit_designs.json").read_text(encoding="utf-8"))
    for d in DESIGNS:
        o = d["offer"]
        prices = {html.unescape(k): float(v) for k, v in cap[o]["prices"].items()}
        stock = {html.unescape(k): v for k, v in cap[o]["stock"].items()}
        kid_cost = adult_cost = 0.0
        for _, _, vc, _ in d["colors"]:
            for s in KIDS + list(ADULTS.values()):
                key = f"{vc}>{s}码"
                if key not in prices or (stock.get(key) or 0) < 50:
                    raise SystemExit(f"{o}: missing or low stock {key} {stock.get(key)}")
                if s in KIDS:
                    kid_cost = max(kid_cost, prices[key])
                else:
                    adult_cost = max(adult_cost, prices[key])
        cp, ap = price(kid_cost, 350), price(adult_cost, 650)
        slug = d["name"].lower().replace(" ", "-")
        handle = f"{slug}-family-matching-sweaters"
        up = ROOT / "uploads" / handle
        up.mkdir(parents=True, exist_ok=True)
        fname = f"01-{slug}-family-sweaters.jpg"
        (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{o}/desc/{d['main']}").read_bytes())
        man = json.loads((ROOT / f"ops/sourcing/vendor-images/{o}/desc/manifest.json").read_text(encoding="utf-8"))
        patterns = list(dict.fromkeys(p for c in d["colors"] for p in c[3]))
        spec = {
            "mode": "family_sweatshirt", "garment": "sweater",
            "offer_id": o, "offer_created": d["listed"], "handle": handle, "shortcode": d["code"], "print_name": d["name"],
            "colors": [{"name": c[0], "token": c[1]} for c in d["colors"]],
            "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in patterns],
            "color_pattern_labels": patterns,
            "fabric_key": "modal_knit", "design_key": "crew_knit", "sleeve_style": "Long-Sleeve",
            "print_sentence": d["sentence"], "feature_label": d["feature"][0], "feature_text": d["feature"][1],
            "extra_tags": d["tags"], "media_alt": d["alt"],
            "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/" + d["main"])),
            "image_filename": fname, "ai_refs": d["refs"],
            "chart_source": "sd_knit", "chart_table": "sd_knit",
            "chart_note": "the offer's own description publishes the supplier's 尺码展示 (description image 12), saved as SOURCE_SIZE_CHART; half chest doubled to a full chest, weight converted from jin to kg; adult heights are not published.",
            "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
            "vendor_title": d["title_cn"],
            "vendor_color_values": [c[2] for c in d["colors"]], "vendor_codes": [],
            "vendor_size_labels": [f"Child {s}" for s in KIDS] + [f"Adult {s}" for s in ADULTS],
            "vendor_prices_note": f"Child up to ¥{kid_cost:g}; Adult up to ¥{adult_cost:g}.",
            "designs_note": f"One design in {len(d['colors'])} color(s) as one Shopify product.",
            "exclusions_note": "Props, bags and trousers in the vendor photos are not sold.",
            "evidence_lines": [
                "Supplier: 东莞市森大服饰有限公司 (1688 store senda831, Dongguan), 9 years on 1688, 48h pickup 97.64%, 48h fulfillment 99.70%, quality returns 0%, disputes 0%, repeat buyers 82%, service 4.5 (creditdetail read 2026-09-27). New Tier B vendor.",
                f"New-design gate: offer listed {d['listed']}; release attribute 2026年秋季; checked against the store's 22 active sweaters and archived knits for duplicates; no logos or licensed characters.",
                "Fabric evidence: attribute table lists fabric name and main fabric as modal (莫代尔), thick; the listing says the main fabric is listed as modal.",
                f"Sizes 80-160 and S-4XL; stock >= 50 per SKU ({', '.join(c[2] for c in d['colors'])}).",
            ],
        }
        (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(handle, f"child ${cp:.2f} (¥{kid_cost:g})", f"adult ${ap:.2f} (¥{adult_cost:g})")


if __name__ == "__main__":
    main()
