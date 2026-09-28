#!/usr/bin/env python3
"""Little Lamb family crewneck sweatshirt from 深圳市斯蒂琪 (proven supplier: 10 orders, median lead 2.6 days;
7 years on 1688, fulfillment 97.6%). One design in two colours sold as two offers:
  Light Blue = offer 1081613475540 (listed 2026-09-13, release Winter 2026), SKU colour "Autumn clothing";
  Cream      = offer 1079575361234 (listed 2026-08-30, release Fall 2026), SKU colour "Apricot-colored autumn clothing".
Only the standard-weight sweatshirt is listed: the fleece-lined versions, skirts, khaki trousers, shirts, the
three-stripe track pants (a sportswear-brand look-alike) and baby rompers are not. Chart: both offers publish the
same 尺寸表 as the stq_sweat table (half chest x2, weight jin -> kg).
Pricing per the owner's 50%-landed rule (child 250 g, adult 450 g), compare-at +$10.
"""
import html
import json
import math
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
OFFERS = {"Light Blue": ("1081613475540", "Autumn clothing", "LBL", ["Blue", "White"]),
          "Cream": ("1079575361234", "Apricot-colored autumn clothing", "CRM", ["Beige", "White"])}
G = {"Blue": "69639766113", "White": "69639733345", "Beige": "69641928801"}
SIZES = {"Child 80": "80cm", "Child 90": "90cm", "Child 100": "100cm", "Child 110": "110cm", "Child 120": "120cm",
         "Child 130": "130cm", "Child 140": "140cm", "Child 150": "150cm", "Adult S": "Adult S", "Adult M": "Adult M",
         "Adult L": "Adult L", "Adult XL": "Adult XL", "Adult 2XL": "Adult XXL", "Adult 3XL": "Adult 3XL", "Adult 4XL": "Adult 4XL"}


def price(cost_cny: float, grams: int) -> float:
    landed = (cost_cny + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return math.ceil(2.06 * landed - 0.99) + 0.99


def main():
    cap = json.loads((SCRATCH / "lamb_designs.json").read_text(encoding="utf-8"))
    kid = adult = 0.0
    for color, (o, vc, _, _) in OFFERS.items():
        prices = {html.unescape(k): float(v) for k, v in cap[o]["prices"].items()}
        stock = {html.unescape(k): v for k, v in cap[o]["stock"].items()}
        for canon, lab in SIZES.items():
            key = f"{vc}>{lab}"
            if key not in prices or (stock.get(key) or 0) < 40:
                raise SystemExit(f"missing/low {o} {key} {stock.get(key)}")
            if canon.startswith("Child"):
                kid = max(kid, prices[key])
            else:
                adult = max(adult, prices[key])
    cp, ap = price(kid, 250), price(adult, 450)
    handle = "little-lamb-family-matching-sweatshirts"
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = "01-little-lamb-family-sweatshirts.jpg"
    main_offer = "1081613475540"
    (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{main_offer}/desc/04.jpg").read_bytes())
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{main_offer}/desc/manifest.json").read_text(encoding="utf-8"))
    pats = list(dict.fromkeys(p for v in OFFERS.values() for p in v[3]))
    spec = {
        "mode": "family_sweatshirt", "title_variant": "everyday",
        "offer_id": main_offer, "offer_created": "2026-09-13", "handle": handle, "shortcode": "LLMB", "print_name": "Little Lamb",
        "colors": [{"name": c, "token": v[2]} for c, v in OFFERS.items()],
        "color_pattern_gids": [f"gid://shopify/Metaobject/{G[p]}" for p in pats], "color_pattern_labels": pats,
        "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
        "print_sentence": "A small fluffy white lamb patch sits on the chest of a soft light blue or cream crewneck sweatshirt.",
        "feature_label": "Lamb patch:", "feature_text": "A sweet little embroidered lamb that looks great in family photos.",
        "extra_tags": ["Lamb", "Minimalist", "Light Blue", "Cream"],
        "media_alt": "Family in matching light blue crewneck sweatshirts with a small white lamb patch on the chest.",
        "image_url": next(x["url"] for x in man["desc_images"] if x.get("path", "").endswith("/04.jpg")),
        "image_filename": fname, "ai_refs": ["14.jpg", "02.jpg"],
        "chart_source": "stq_sweat", "chart_table": "stq_sweat",
        "chart_note": "both offers publish the supplier's 尺寸表 (description image 00), identical to the stq_sweat table; half chest doubled, weight converted from jin to kg.",
        "child_price": f"{cp:.2f}", "adult_price": f"{ap:.2f}",
        "vendor_title": "亲子装春秋卫衣一家四口可爱小羊刺绣浅蓝圆领上衣母女父子全家冬",
        "vendor_color_values": [f"{v[0]}:{v[1]}" for v in OFFERS.values()], "vendor_codes": [],
        "vendor_size_labels": list(SIZES),
        "vendor_prices_note": f"Child ¥{kid:g}; Adult up to ¥{adult:g} (standard weight).",
        "designs_note": "One design in two colours (light blue offer 1081613475540, cream offer 1079575361234) as one Shopify product.",
        "exclusions_note": "Fleece-lined versions, skirts, trousers, shirts, striped track pants and baby rompers are not listed; props are not sold.",
        "evidence_lines": [
            "Supplier: 深圳市斯蒂琪电子商务有限公司, proven (10 orders, median 2.6 days PO to warehouse), 7 years on 1688, fulfillment 97.6%.",
            "Fresh-and-in-season gate: light blue listed 2026-09-13, release Winter 2026; cream listed 2026-08-30, release Fall 2026.",
            "Fabric evidence: attribute lists cotton main fabric (percentage not stated); the listing says cotton sweatshirt knit only.",
            "Vendor sizes 80-150 cm and Adult S-4XL in both colours; stock >= 40 per SKU.",
        ],
    }
    (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(handle, f"child ${cp:.2f} (¥{kid:g})", f"adult ${ap:.2f} (¥{adult:g})")


if __name__ == "__main__":
    main()
