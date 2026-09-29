#!/usr/bin/env python3
"""Happy Faces family crewneck sweatshirt from 东莞市辰承服饰有限公司 (1688 offer 1079896638732).

Supplier gate (passed by the parent session): 9 years on 1688, 48h pickup 99.97%, service 4.5;
offer promises 承诺48小时发货; release attribute "Fall 2026" (listed 2026-09-04); MOQ 1; ships
from Guangdong. Fabric: main fabric cotton, content 95%; material composition cotton 95%,
spandex 5%.
Design (description images 32/33 adult close-ups, 29/31 child close-ups): a small cartoon face on
the left chest. The vendor colour axis carries a Girls/Boys version for every size:
  Girls = adult "HAPPY MOM" (girl with glasses and a bob, lettering arched above) and child
          "HAPPY BABY" pigtail girl with red bows;
  Boys  = adult "HAPPY DAD" (short-haired boy, lettering below) and child "HAPPY BABY"
          short-haired boy.
The print choice is therefore modelled as the colour value ("Cream – Mom & Girl" etc.), which
maps one-to-one onto the vendor SKU (colour x version) and is explained in the copy.
Standard (spring and autumn) weight only: fleece-lined versions, baby rompers / crawling suits
and hats are not listed.
Chart: the offer's own 尺码表 (description image 01). 胸围X2 is a half chest and is doubled;
建议体重 is in jin and halved to kg; heights as published. The chart publishes 肩宽 (shoulder)
but no sleeve length, so Sleeve is "-" (chart_no_sleeve).
Pricing per the owner's 50%-landed rule (child 250 g, adult 450 g), compare-at by the engine.
"""
import html
import json
import math
from pathlib import Path

from PIL import Image

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
OFFER = "1079896638732"
# store colour value: (vendor colour value, token, colour-pattern label)
# The store has no Brown colour-pattern metaobject, so only Beige (cream) is referenced.
COLORS = {"Cream – Mom & Girl": ("Apricot Spring/Autumn/Girls", "CRMMG", "Beige"),
          "Cream – Dad & Boy": ("Apricot Spring/Autumn/Boys", "CRMDB", "Beige"),
          "Brown – Mom & Girl": ("Brown Spring/Autumn/Girls", "BRNMG", None),
          "Brown – Dad & Boy": ("Brown Spring/Autumn/Boys", "BRNDB", None)}
G = {"Beige": "69641928801"}
# engine label -> vendor size value
VENDOR_SIZE = {
    "Child 80": "80cm", "Child 90": "90cm", "Child 100": "100cm", "Child 110": "110cm",
    "Child 120": "120cm", "Child 130": "130cm", "Child 140": "140cm", "Child 150": "150cm",
    "Adult S": "Adult size S", "Adult M": "Adult size M", "Adult L": "Adult size L",
    "Adult XL": "Adult XL size", "Adult 2XL": "Adult XXL size", "Adult 3XL": "Adult size 3XL",
    "Adult 4XL": "Adult size 4XL",
}
# (chart label, picker, suffix, age, length, full chest, sleeve, pant, waist, hip)
ROWS = {
    "Child 80": ("80 (70-80 cm)", "Child 6-12 Months", "KID612M", "6-12 mo", 37, 68, "-", "-", "-", "-"),
    "Child 90": ("90 (80-90 cm)", "Child 1-2 Years", "KID12Y", "1-2", 39, 72, "-", "-", "-", "-"),
    "Child 100": ("100 (90-100 cm)", "Child 2-3 Years", "KID23Y", "2-3", 40, 76, "-", "-", "-", "-"),
    "Child 110": ("110 (100-110 cm)", "Child 4 Years", "KID4Y", "4", 43, 80, "-", "-", "-", "-"),
    "Child 120": ("120 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 45, 84, "-", "-", "-", "-"),
    "Child 130": ("130 (120-130 cm)", "Child 7-8 Years", "KID78Y", "7-8", 47, 88, "-", "-", "-", "-"),
    "Child 140": ("140 (130-140 cm)", "Child 9-10 Years", "KID910Y", "9-10", 49, 92, "-", "-", "-", "-"),
    "Child 150": ("150 (140-150 cm)", "Child 11-12 Years", "KID1112Y", "11-12", 51, 96, "-", "-", "-", "-"),
    "Adult S": ("Adult S", "Adult S", "S", "—", 61, 110, "-", "-", "-", "-"),
    "Adult M": ("Adult M", "Adult M", "M", "—", 63, 114, "-", "-", "-", "-"),
    "Adult L": ("Adult L", "Adult L", "L", "—", 66, 118, "-", "-", "-", "-"),
    "Adult XL": ("Adult XL", "Adult XL", "XL", "—", 69, 122, "-", "-", "-", "-"),
    "Adult 2XL": ("Adult 2XL", "Adult 2XL", "2XL", "—", 71, 126, "-", "-", "-", "-"),
    "Adult 3XL": ("Adult 3XL", "Adult 3XL", "3XL", "—", 73, 130, "-", "-", "-", "-"),
    "Adult 4XL": ("Adult 4XL", "Adult 4XL", "4XL", "—", 75, 134, "-", "-", "-", "-"),
}
FIT = {  # (height cm, weight kg) as published (weights jin / 2)
    "Child 80": ("70-80", "7-11"), "Child 90": ("80-90", "10-13"), "Child 100": ("90-100", "13-16"),
    "Child 110": ("100-110", "16-20"), "Child 120": ("110-120", "20-25"), "Child 130": ("120-130", "25-30"),
    "Child 140": ("130-140", "30-35"), "Child 150": ("140-150", "35-40"),
    "Adult S": ("150-165", "42.5-55"), "Adult M": ("150-170", "55-65"), "Adult L": ("155-175", "65-75"),
    "Adult XL": ("160-180", "75-85"), "Adult 2XL": ("165-185", "85-95"), "Adult 3XL": ("170-190", "95-105"),
    "Adult 4XL": ("175-195", "105-115"),
}


def price(cost_cny: float, grams: int) -> float:
    landed = (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def landed(cost_cny: float, grams: int) -> float:
    return (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11


def main():
    cap = json.loads((SCRATCH / "cc_designs.json").read_text(encoding="utf-8"))[OFFER]
    prices = {html.unescape(k): float(v) for k, v in cap["prices"].items()}
    stock = {html.unescape(k): v for k, v in cap["stock"].items()}
    kid = adult = 0.0
    for _, (vc, _, _) in COLORS.items():
        for lab in ROWS:
            key = f"{vc}>{VENDOR_SIZE[lab]}"
            if key not in prices or (stock.get(key) or 0) < 40:
                raise SystemExit(f"missing/low {key} {stock.get(key)}")
            if lab.startswith("Child"):
                kid = max(kid, prices[key])
            else:
                adult = max(adult, prices[key])
    cp, ap = price(kid, 250), price(adult, 450)
    for cost, g, p in ((kid, 250, cp), (adult, 450, ap)):
        if landed(cost, g) > 0.5 * p:
            raise SystemExit(f"landed {landed(cost, g):.2f} > 50% of {p}")
    handle = "happy-faces-family-matching-sweatshirts"
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = "01-happy-faces-family-sweatshirts.jpg"
    # Vendor hanger photo (brown adult HAPPY DAD + cream child pigtail HAPPY BABY), cropped above the decor shelf.
    src = Image.open(ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/06.jpg").convert("RGB")
    src.crop((0, 0, src.width, 1370)).save(up / fname, quality=92)
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/manifest.json").read_text(encoding="utf-8"))
    pats = list(dict.fromkeys(v[2] for v in COLORS.values() if v[2]))
    spec = {
        "mode": "family_sweatshirt", "title_variant": "everyday",
        "offer_id": OFFER, "offer_created": "2026-09", "handle": handle, "shortcode": "HPFC", "print_name": "Happy Faces",
        "colors": [{"name": c, "token": v[1]} for c, v in COLORS.items()],
        "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in pats], "color_pattern_labels": pats,
        "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
        "print_sentence": "A small cartoon face sits on the left chest of a soft cotton crewneck in cream or brown: adult sizes say HAPPY MOM or HAPPY DAD, and kids' sizes show a HAPPY BABY girl with pigtails or a HAPPY BABY boy.",
        "feature_label": "Pick the face:", "feature_text": "The color choice also picks the face. Mom & Girl gives the HAPPY MOM face on adult sizes and the pigtail girl on kids' sizes; Dad & Boy gives the HAPPY DAD face on adult sizes and the short-haired boy on kids' sizes.",
        "extra_tags": ["Happy Faces", "Cartoon", "Happy Mom", "Happy Dad", "Cream", "Brown"],
        "media_alt": "Brown adult crewneck sweatshirt with a small HAPPY DAD cartoon face hanging beside a cream child's sweatshirt with a pigtail HAPPY BABY face.",
        "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/06.jpg")),
        "image_filename": fname, "ai_refs": ["33.jpg", "29.jpg"],
        "chart_source": "cc_roles", "chart_table": "cc_roles", "chart_no_sleeve": True,
        "chart_rows": {k: list(v) for k, v in ROWS.items()}, "fit_rows": {k: list(v) for k, v in FIT.items()},
        "chart_image": f"ops/sourcing/vendor-images/{OFFER}/desc/01.jpg",
        "chart_note": "the offer's own description publishes the supplier's 尺码表 (description image 01: kids 80-150, baby rompers, and unisex adult S-4XL), saved as SOURCE_SIZE_CHART; 胸围X2 half chest doubled to full chest; weights converted from jin to kg; the chart gives shoulder width but no sleeve length, so Sleeve is '-'.",
        "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
        "vendor_title": "爸爸妈妈弟弟妹妹 family matching sweatshirts (title as summarized by the parent session)",
        "vendor_color_values": [v[0] for v in COLORS.values()], "vendor_codes": [],
        "vendor_size_labels": list(ROWS),
        "vendor_prices_note": f"Child ¥{kid:g}; Adult ¥{adult:g} (standard spring-and-autumn weight).",
        "designs_note": "One design family (cartoon face patch: adult HAPPY MOM / HAPPY DAD, child HAPPY BABY girl / boy) in cream (vendor apricot) and brown; the vendor Girls/Boys version is the colour value (Mom & Girl / Dad & Boy), one Shopify product.",
        "exclusions_note": "Fleece-lined versions, baby rompers / crawling suits with hats and the hats are not listed; props are not sold.",
        "evidence_lines": [
            "Supplier: 东莞市辰承服饰有限公司, 9 years on 1688, 48h pickup 99.97%, service 4.5 (gate passed 2026-09-28).",
            "Owner 24-48h rule: offer promises 承诺48小时发货; MOQ 1; ships from Guangdong.",
            "Fresh-and-in-season gate: release attribute Fall 2026; offer listed 2026-09-04.",
            "Fabric evidence: main fabric cotton, content 95%; material composition cotton 95%, spandex 5%.",
            "Design evidence: adult HAPPY DAD / HAPPY MOM faces (description images 32, 33), child HAPPY BABY boy / pigtail girl (29, 31); Girls/Boys vendor versions for every size.",
            "Vendor sizes 80-150 cm and adult S-4XL in each colour/version; stock 88 per SKU; rompers, fleece-lined and hats not listed.",
        ],
    }
    (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(handle, f"child ${cp:.2f} (¥{kid:g}, landed ${landed(kid, 250):.2f})",
          f"adult ${ap:.2f} (¥{adult:g}, landed ${landed(adult, 450):.2f})")


if __name__ == "__main__":
    main()
