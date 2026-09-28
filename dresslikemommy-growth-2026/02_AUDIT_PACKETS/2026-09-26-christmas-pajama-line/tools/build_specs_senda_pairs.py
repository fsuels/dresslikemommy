#!/usr/bin/env python3
"""Mommy & Me and Daddy & Me knit sweater pairs from 东莞市森大服饰 (1688 store senda831,
Tier B; gate read 2026-09-27: 9 years, 48h pickup 97.64%, fulfillment 99.70%, returns 0%).

Each offer sells two styles: a women's/girls' style (collar or cardigan, women S-3XL)
and a men's/boys' crew (men S-4XL), with one shared kids table (80-160). Each style is
listed on its own: the women's style as a Mommy & Me listing, the crew as Daddy & Me.
Charts are transcribed per offer from description image 12 (half chest doubled, weight
jin -> kg, adult heights not published). Offers listed 2026-08/09, release 2026年秋季,
fabric listed as modal-blend yarn (莫代尔纤绒纱).
"""
import html
import json
import math
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
G = {"Red": "69600804961", "White": "69639733345", "Blue": "69639766113", "Beige": "69641928801", "Gray": "69944672353"}
KIDS = ["80", "90", "100", "110", "120", "130", "140", "150", "160"]
KID_PICK = [("Child 6-12 Months", "KID612M", "6-12 mo", "70-80"), ("Child 1-2 Years", "KID12Y", "1-2", "80-90"),
            ("Child 2-3 Years", "KID23Y", "2-3", "90-100"), ("Child 4 Years", "KID4Y", "4", "100-110"),
            ("Child 5-6 Years", "KID56Y", "5-6", "110-120"), ("Child 7-8 Years", "KID78Y", "7-8", "120-130"),
            ("Child 9-10 Years", "KID910Y", "9-10", "130-140"), ("Child 11-12 Years", "KID1112Y", "11-12", "140-145"),
            ("Child 13-14 Years", "KID1314Y", "13-14", "145-155")]
KID_KG = ["7.5", "10", "15", "17.5", "22.5", "25", "30", "32.5", "37.5"]
ADULT = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]
ADULT_VENDOR = {"S": "S", "M": "M", "L": "L", "XL": "XL", "2XL": "XXL", "3XL": "3XL", "4XL": "4XL"}
ADULT_KG = ["40-50", "50-57.5", "57.5-67.5", "67.5-75", "75-85", "85-92.5", "92.5-105"]
KID_LEN = [36, 38, 41, 44, 47, 50, 53, 55, 57]
KID_SLV = [33, 35, 37, 39, 42, 45, 48, 51, 54]
KID_HALF_A = [31, 33, 35, 37, 39, 41, 43, 45, 47]  # 8274 / 3081
KID_HALF_B = [30, 32, 34, 36, 38, 40, 42, 44, 46]  # 3382 / 5832
# adult tables: (length, half chest, sleeve) per size
MEN_A = [(62, 50, 57), (64, 52, 58), (66, 54, 59), (68, 56, 60), (70, 58, 61), (72, 60, 62), (74, 62, 63)]
MEN_B = [(60, 48, 57), (62, 50, 58), (64, 52, 59), (66, 54, 60), (68, 56, 61), (70, 58, 62), (72, 60, 63)]
DESIGNS = [
    dict(offer="1085288498274", listed="2026-09-23", kids=KID_HALF_A, color=("Red", "RED", ["Red", "White"]),
         mommy=dict(style="女款翻领", name="Red Lace Bow", code="RLBW", women=[(55, 49, 56), (57, 51, 57), (59, 53, 58), (61, 55, 59), (63, 57, 60), (65, 59, 61)],
                    sentence="A red knit sweater with a pointed knit collar, a big white lace bow with little pearl accents at the neck, and white lace trim at the cuffs.",
                    feature=("Lace bow:", "A sweet white lace bow with pearl accents for a dressy mommy-and-me look."),
                    alt="Mom and daughter in matching red knit sweaters with white lace bows at the collar.", main="02.jpg", refs=["00.jpg", "11.jpg"],
                    tags=["Christmas Sweaters", "Red", "Bow"]),
         daddy=dict(style="男款圆领", name="Red Striped Cuff", code="RSCF", men=MEN_A,
                    sentence="A red crewneck knit sweater with thin cream stripes at the cuffs and hem.",
                    feature=("Striped trim:", "Classic cream tipping at the cuffs and hem."),
                    alt="Dad and son in matching red crewneck knit sweaters with cream striped cuffs and hem.", main="00.jpg", refs=["04.jpg", "11.jpg"],
                    tags=["Christmas Sweaters", "Red"])),
    dict(offer="1073329703081", listed="2026-08-14", kids=KID_HALF_A, color=("Charcoal", "CHR", ["Gray", "White"]),
         mommy=dict(style="女款翻领", name="Charcoal Cream Collar", code="CCCL", women=[(55, 47, 51), (57, 49, 52), (59, 51, 54), (61, 53, 55), (63, 55, 57), (65, 57, 58)],
                    sentence="A charcoal gray knit sweater with a wide scoop neckline over a cream knit collar insert, and a cream layered hem.",
                    feature=("Cream collar:", "A soft cream collar and hem that brighten the charcoal knit."),
                    alt="Mom and daughter in matching charcoal knit sweaters with cream collars.", main="00.jpg", refs=["09.jpg", "01.jpg"],
                    tags=["Gray", "Charcoal", "Collar"]),
         daddy=dict(style="男款圆领", name="Charcoal Layered", code="CHLY", men=MEN_A,
                    sentence="A charcoal gray crewneck knit sweater with a small cream shirt-style tab at the neck and a cream layered hem.",
                    feature=("Layered look:", "A cream collar tab and hem that look like a shirt underneath."),
                    alt="Dad and son in matching charcoal crewneck knit sweaters with cream layered hems.", main="00.jpg", refs=["02.jpg", "09.jpg"],
                    tags=["Gray", "Charcoal"])),
    dict(offer="1084175103382", listed="2026-09-22", kids=KID_HALF_B, color=("Red", "RED", ["Red", "Beige"]),
         mommy=dict(style="开衫", name="Red Cable Cardigan", code="RCCD", women=[(55, 45, 56), (57, 47, 57), (59, 49, 58), (61, 51, 59), (63, 53, 60), (65, 55, 61)],
                    sentence="A red cable-knit cardigan with a cream Peter Pan collar, gold buttons, and cream trim at the cuffs and hem.",
                    feature=("Peter Pan collar:", "A cream collar and gold buttons on a cozy cable knit."),
                    alt="Mom and daughter in matching red cable-knit cardigans with cream collars and gold buttons.", main="01.jpg", refs=["09.jpg", "00.jpg"],
                    tags=["Christmas Sweaters", "Red", "Cardigan", "Cable Knit"]),
         daddy=dict(style="圆领", name="Red Cable Crew", code="RCCR", men=MEN_B,
                    sentence="A red cable-knit crewneck sweater with cream trim at the neckline, cuffs, and hem.",
                    feature=("Cable knit:", "Classic cable texture with cream tipping."),
                    alt="Dad and son in matching red cable-knit crewneck sweaters with cream trim.", main="00.jpg", refs=["02.jpg", "09.jpg"],
                    tags=["Christmas Sweaters", "Red", "Cable Knit"])),
    dict(offer="1075113265832", listed="2026-08-14", kids=KID_HALF_B, color=("Navy", "NVY", ["Blue", "White"]),
         mommy=dict(style="藏青开衫", name="Navy Pearl Gingham", code="NPGM", women=[(51, 43, 59), (53, 45, 60), (55, 47, 61), (57, 49, 62), (59, 51, 63), (61, 53, 64)],
                    sentence="A navy cable-knit cardigan with a blue gingham ruffle collar edged in little faux pearls, pearl-look buttons, and gingham ruffles at the cuffs and hem.",
                    feature=("Gingham ruffles:", "Blue gingham ruffles and pearl details on a navy cable knit."),
                    alt="Mom and daughter in matching navy cable-knit cardigans with gingham ruffle collars and pearl details.", main="00.jpg", refs=["09.jpg", "02.jpg"],
                    tags=["Navy", "Cardigan", "Cable Knit", "Gingham"]),
         daddy=dict(style="藏青圆领", name="Navy Cable Crew", code="NVCC", men=MEN_B,
                    sentence="A navy cable-knit crewneck sweater with ribbed neckline, cuffs, and hem.",
                    feature=("Cable knit:", "A classic navy cable knit that goes with everything."),
                    alt="Dad and son in matching navy cable-knit crewneck sweaters.", main="00.jpg", refs=["02.jpg", "09.jpg"],
                    tags=["Navy", "Cable Knit"])),
    dict(offer="1074933693109", listed="2026-08-13", kids=KID_HALF_A, color=("Burgundy", "BUR", ["Red", "White"]),
         mommy=dict(style="酒红色开衫", name="Burgundy Ruffle", code="BRCD", women=[(55, 45, 56), (57, 47, 57), (59, 49, 58), (61, 51, 59), (63, 53, 60), (65, 55, 61)],
                    sentence="A burgundy knit cardigan with small buttons, a tie at the waist, and white lace ruffles at the cuffs and hem.",
                    feature=("Lace ruffles:", "Soft white lace ruffles at the cuffs and hem with a sweet tie waist."),
                    alt="Mom and daughter in matching burgundy knit cardigans with white lace ruffle cuffs and hems.", main="00.jpg", refs=["09.jpg", "02.jpg"],
                    tags=["Christmas Sweaters", "Burgundy", "Cardigan", "Ruffle"]),
         daddy=dict(style="酒红色圆领", name="Burgundy Trim Crew", code="BTCR", men=MEN_A,
                    sentence="A burgundy crewneck knit sweater with cream trim at the neckline and a cream layered hem.",
                    feature=("Cream trim:", "A cream neckline and layered hem that brighten the burgundy knit."),
                    alt="Dad and son in matching burgundy crewneck knit sweaters with cream trim.", main="00.jpg", refs=["02.jpg", "09.jpg"],
                    tags=["Christmas Sweaters", "Burgundy"])),
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
        man = json.loads((ROOT / f"ops/sourcing/vendor-images/{o}/desc/manifest.json").read_text(encoding="utf-8"))
        for role in ("mommy", "daddy"):
            r = d[role]
            adults = ADULT[:6] if role == "mommy" else ADULT
            table = r["women"] if role == "mommy" else r["men"]
            prefix, who = ("Mom", "Mother") if role == "mommy" else ("Dad", "Father")
            kid_cost = adult_cost = 0.0
            for s in KIDS + [ADULT_VENDOR[a] for a in adults]:
                key = f"{r['style']}>{s}码"
                if key not in prices or (stock.get(key) or 0) < 50:
                    raise SystemExit(f"{o}: missing or low stock {key}")
                if s in KIDS:
                    kid_cost = max(kid_cost, prices[key])
                else:
                    adult_cost = max(adult_cost, prices[key])
            rows, fit = {}, {}
            for i, k in enumerate(KIDS):
                pick, suf, age, h = KID_PICK[i]
                rows[f"Child {k}"] = [f"{k} ({h} cm)", pick, suf, age, KID_LEN[i], d["kids"][i] * 2, KID_SLV[i], "-", "-", "-"]
                fit[f"Child {k}"] = [h, KID_KG[i]]
            for i, a in enumerate(adults):
                ln, half, slv = table[i]
                rows[f"{prefix} {a}"] = [ADULT_VENDOR[a], f"{who} {a}", a, "—", ln, half * 2, slv, "-", "-", "-"]
                fit[f"{prefix} {a}"] = ["-", ADULT_KG[i]]
            cp, ap = price(kid_cost, 350), price(adult_cost, 650)
            slug = r["name"].lower().replace(" ", "-")
            handle = f"{slug}-{'mommy-and-me' if role == 'mommy' else 'daddy-and-me'}-sweaters"
            up = ROOT / "uploads" / handle
            up.mkdir(parents=True, exist_ok=True)
            fname = f"01-{slug}-sweaters.jpg"
            (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{o}/desc/{r['main']}").read_bytes())
            cname, ctok, pats = d["color"]
            spec = {
                "mode": "family_sweatshirt", "garment": "sweater", "knit_role": role,
                "offer_id": o, "offer_created": d["listed"], "handle": handle, "shortcode": r["code"], "print_name": r["name"],
                "colors": [{"name": cname, "token": ctok}],
                "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in pats], "color_pattern_labels": pats,
                "fabric_key": "modal_knit", "design_key": ("crew_knit" if role == "daddy" else "cardigan_knit" if "开衫" in r["style"] else "collar_knit"), "sleeve_style": "Long-Sleeve",
                "print_sentence": r["sentence"], "feature_label": r["feature"][0], "feature_text": r["feature"][1],
                "extra_tags": r["tags"], "media_alt": r["alt"],
                "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/" + r["main"])),
                "image_filename": fname, "ai_refs": r["refs"],
                "chart_source": "sd_pair", "chart_table": "sd_pair", "chart_rows": rows, "fit_rows": fit,
                "chart_image": f"ops/sourcing/vendor-images/{o}/desc/12.jpg",
                "chart_note": "the offer's own description publishes the supplier's 尺码展示 (description image 12: kids, men's and women's tables), saved as SOURCE_SIZE_CHART; half chest doubled, weight converted from jin to kg; adult heights are not published.",
                "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
                "vendor_title": f"森大 {o} {r['style']}",
                "vendor_color_values": [r["style"]], "vendor_codes": [],
                "vendor_size_labels": list(rows),
                "vendor_prices_note": f"Child up to ¥{kid_cost:g}; {who} up to ¥{adult_cost:g} ({r['style']}).",
                "designs_note": f"The offer's {r['style']} style only, one Shopify product (its other style is a separate listing).",
                "exclusions_note": "The offer's other style is listed separately; props and trousers in the vendor photos are not sold.",
                "evidence_lines": [
                    "Supplier: 东莞市森大服饰有限公司 (1688 store senda831, Dongguan), 9 years on 1688, 48h pickup 97.64%, 48h fulfillment 99.70%, quality returns 0%, disputes 0% (read 2026-09-27). Tier B.",
                    f"New-design gate: offer listed {d['listed']}; release attribute 2026年秋季; no logos or licensed characters; checked against live sweaters.",
                    "Fabric evidence: attribute table lists modal (莫代尔纤绒纱); the listing says the main fabric is listed as modal.",
                    f"Style {r['style']}: kids 80-160 and {who.lower()} {adults[0]}-{adults[-1]}; stock >= 50 per SKU.",
                ],
            }
            (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(handle, f"child ${cp:.2f} (¥{kid_cost:g})", f"{who.lower()} ${ap:.2f} (¥{adult_cost:g})")


if __name__ == "__main__":
    main()
