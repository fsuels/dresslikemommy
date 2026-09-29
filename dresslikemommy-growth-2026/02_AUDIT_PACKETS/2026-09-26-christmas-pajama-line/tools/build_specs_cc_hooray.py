#!/usr/bin/env python3
"""Hooray Sun family crewneck sweatshirt from 东莞市辰承服饰有限公司 (1688 offer 1081053551587).

Supplier gate (passed by the parent session): 9 years on 1688, 48h pickup 99.97%, service 4.5;
offer promises 承诺48小时发货; release attribute "Fall 2026" (listed 2026-09-11); MOQ 1; ships
from Guangdong. Fabric: main fabric cotton, content 95%; material composition cotton 95%,
spandex 5%.
Design: adult sweatshirts carry the word HOORAY in chunky multicolor letters; child sweatshirts
carry a rust-orange half sun with rays (no lettering). Standard (spring and autumn) weight only:
the fleece-lined versions, baby rompers / crawling suits and hats are not listed.
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
OFFER = "1081053551587"
# store colour name: (vendor colour value, token, colour-pattern label)
COLORS = {"Cream": ("Apricot color/spring and autumn", "CRM", "Beige"),
          "White": ("White/Spring and Autumn", "WHT", "White")}
G = {"Beige": "69641928801", "White": "69639733345"}
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
    handle = "hooray-sun-family-matching-sweatshirts"
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = "01-hooray-sun-family-sweatshirts.jpg"
    # Vendor hanger photo (adult HOORAY + child sun), cropped above the decor shelf.
    src = Image.open(ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/38.jpg").convert("RGB")
    src.crop((0, 0, src.width, 1560)).save(up / fname, quality=92)
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/manifest.json").read_text(encoding="utf-8"))
    pats = list(dict.fromkeys(v[2] for v in COLORS.values()))
    spec = {
        "mode": "family_sweatshirt", "title_variant": "everyday",
        "offer_id": OFFER, "offer_created": "2026-09", "handle": handle, "shortcode": "HRSN", "print_name": "Hooray Sun",
        "colors": [{"name": c, "token": v[1]} for c, v in COLORS.items()],
        "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in pats], "color_pattern_labels": pats,
        "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
        "print_sentence": "Adult sweatshirts spell HOORAY in chunky brown, gray and orange letters, and the kids' sweatshirts carry a matching rust-orange half sun with rays, on a soft cotton crewneck in cream or white.",
        "feature_label": "Hooray and sun:", "feature_text": "Grown-ups wear the word and kids wear the little sun, so the whole family reads as one happy set in photos.",
        "extra_tags": ["Hooray Sun", "Hooray", "Sun", "Cream", "White"],
        "media_alt": "Cream adult crewneck sweatshirt printed HOORAY hanging beside a child's sweatshirt with a rust-orange half sun.",
        "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/38.jpg")),
        "image_filename": fname, "ai_refs": ["40.jpg", "17.jpg"],
        "chart_source": "cc_hooray", "chart_table": "cc_hooray", "chart_no_sleeve": True,
        "chart_rows": {k: list(v) for k, v in ROWS.items()}, "fit_rows": {k: list(v) for k, v in FIT.items()},
        "chart_image": f"ops/sourcing/vendor-images/{OFFER}/desc/01.jpg",
        "chart_note": "the offer's own description publishes the supplier's 尺码表 (description image 01: kids 80-150, baby rompers, and unisex adult S-4XL), saved as SOURCE_SIZE_CHART; 胸围X2 half chest doubled to full chest; weights converted from jin to kg; the chart gives shoulder width but no sleeve length, so Sleeve is '-'.",
        "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
        "vendor_title": "Early autumn family matching outfits for a family of three or four, featuring fleece-lined sweaters for babies, mothers, and daughters, a high-end and trendy collection for 2026 (page title as captured in English)",
        "vendor_color_values": [v[0] for v in COLORS.values()], "vendor_codes": [],
        "vendor_size_labels": list(ROWS),
        "vendor_prices_note": f"Child ¥{kid:g}; Adult ¥{adult:g} (standard spring-and-autumn weight).",
        "designs_note": "One design (adult HOORAY lettering, child half sun) in two colours (cream = vendor apricot, white) as one Shopify product.",
        "exclusions_note": "Fleece-lined versions, baby rompers / crawling suits with hats and the hats are not listed; props are not sold.",
        "evidence_lines": [
            "Supplier: 东莞市辰承服饰有限公司, 9 years on 1688, 48h pickup 99.97%, service 4.5 (gate passed 2026-09-28).",
            "Owner 24-48h rule: offer promises 承诺48小时发货; MOQ 1; ships from Guangdong.",
            "Fresh-and-in-season gate: release attribute Fall 2026; offer listed 2026-09-11.",
            "Fabric evidence: main fabric cotton, content 95%; material composition cotton 95%, spandex 5%.",
            "Design evidence: adult sweatshirts print HOORAY; child sweatshirts print a half sun (description images 38, 40, 17).",
            "Vendor sizes 80-150 cm and adult S-4XL in each colour; stock 188 per SKU; rompers, fleece-lined and hats not listed.",
        ],
    }
    (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(handle, f"child ${cp:.2f} (¥{kid:g}, landed ${landed(kid, 250):.2f})",
          f"adult ${ap:.2f} (¥{adult:g}, landed ${landed(adult, 450):.2f})")


if __name__ == "__main__":
    main()
