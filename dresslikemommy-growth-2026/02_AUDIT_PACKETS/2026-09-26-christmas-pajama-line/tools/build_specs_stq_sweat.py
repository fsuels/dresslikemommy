#!/usr/bin/env python3
"""Spec for the 斯蒂琪 (Shenzhen Sidiqi) family Christmas crewneck sweatshirt,
offer 1081522411618 (mode "family_sweatshirt", chart "stq_sweat").

Gate (read 2026-09-27): offer created 2026-09-13, "Year and season of release"
Fall 2026, fulfillment 97.6%, MOQ 1, 50 in stock per SKU, fabric listed as pure
cotton. Our BuckyDrop history with this supplier: median 2.6 days PO to warehouse.
Colours listed: the standard-weight red and green sweatshirts. The fleece-lined
versions, the khaki trousers (sold separately) and the baby romper ("Ha Yi") are not
listed. The print (gift boxes, Santa, snowman, reindeer, tree) is generic; the
vendor's props (a branded cap) are not part of the product.
"""
import html
import json
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
SCRATCH = Path("/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad")
OFFER = "1081522411618"
VENDOR = {"Child 80": "80cm", "Child 90": "90cm", "Child 100": "100cm", "Child 110": "110cm", "Child 120": "120cm",
          "Child 130": "130cm", "Child 140": "140cm", "Child 150": "150cm", "Adult S": "Adult S", "Adult M": "Adult M",
          "Adult L": "Adult L", "Adult XL": "Adult XL", "Adult 2XL": "Adult XXL", "Adult 3XL": "Adult 3XL", "Adult 4XL": "Adult 4XL"}
COLORS = {"Red": "red autumn outfit", "Green": "Green autumn clothing"}


def main():
    cap = json.loads((SCRATCH / "stq_designs.json").read_text(encoding="utf-8"))[OFFER]
    prices = {html.unescape(k): float(v) for k, v in cap["prices"].items()}
    stock = {html.unescape(k): v for k, v in cap["stock"].items()}
    for col, vcol in COLORS.items():
        for canon, lab in VENDOR.items():
            key = f"{vcol}>{lab}"
            if key not in prices or (stock.get(key) or 0) < 20:
                raise SystemExit(f"missing or low stock: {key} {stock.get(key)}")
    kid = sorted({prices[f"{v}>{VENDOR[s]}"] for v in COLORS.values() for s in VENDOR if s.startswith("Child")})
    adult = sorted({prices[f"{v}>{VENDOR[s]}"] for v in COLORS.values() for s in VENDOR if s.startswith("Adult")})
    handle = "santa-and-friends-family-matching-sweatshirts"
    up = ROOT / "uploads" / handle
    up.mkdir(parents=True, exist_ok=True)
    fname = "01-santa-and-friends-family-sweatshirts.jpg"
    (up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/04.jpg").read_bytes())
    man = json.loads((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/manifest.json").read_text(encoding="utf-8"))
    spec = {
        "mode": "family_sweatshirt", "offer_id": OFFER, "offer_created": "2026-09-13", "handle": handle,
        "shortcode": "SNFR", "print_name": "Santa and Friends",
        "colors": [{"name": "Red", "token": "RED"}, {"name": "Green", "token": "GRN"}],
        "color_pattern_gids": ["gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/70220546145",
                               "gid://shopify/Metaobject/130231140449"],
        "color_pattern_labels": ["Red", "Green", "Multicolor"],
        "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt", "sleeve_style": "Long-Sleeve",
        "print_sentence": "Red or green crewneck sweatshirts carry a row of little holiday friends across the chest: gift boxes, Santa, a snowman in a Santa hat, a reindeer, and a Christmas tree, with tiny gold stars.",
        "feature_label": "Holiday friends print:",
        "feature_text": "Santa, a snowman, a reindeer, and a tree lined up with gift boxes across the chest.",
        "extra_tags": ["Santa", "Snowman", "Reindeer", "Christmas Tree", "Red", "Green"],
        "media_alt": "Family in matching red and green Christmas crewneck sweatshirts with a row of Santa, snowman, reindeer, and tree prints.",
        "image_url": next(d["url"] for d in man["desc_images"] if d.get("path", "").endswith("/04.jpg")),
        "image_filename": fname, "ai_refs": ["02.jpg", "06.jpg"], "skip_ref_images": ["00.jpg", "07.jpg"],
        "chart_source": "stq_sweat", "chart_table": "stq_sweat",
        "chart_note": "the offer's own description publishes the supplier's 尺码表 (description image 00), saved as SOURCE_SIZE_CHART; half-chest doubled, weight converted from jin to kg.",
        "child_price": "32.99", "adult_price": "39.99",
        "vendor_title": "圣诞亲子装秋冬新款圆领卫衣一家三口四口家庭装母子母女",
        "vendor_color_values": list(COLORS.values()), "vendor_codes": [],
        "vendor_size_labels": list(VENDOR),
        "vendor_prices_note": f"Child ¥{'/'.join(f'{x:g}' for x in kid)}; Adult ¥{'/'.join(f'{x:g}' for x in adult)} (standard weight).",
        "designs_note": "One design in two colours (red, green) as one Shopify product with a Color option.",
        "exclusions_note": "Fleece-lined versions, the khaki trousers (sold separately) and the baby romper are not listed; props in the vendor photos are not sold.",
        "evidence_lines": [
            "Supplier: 深圳市斯蒂琪电子商务有限公司 (Shenzhen Sidiqi), fulfillment 97.6%, MOQ 1, 50 in stock per SKU; our BuckyDrop history: median 2.6 days PO to warehouse (p90 3.2). Page read 2026-09-27 in the helper browser with no login or captcha.",
            "New-design gate: offer created 2026-09-13; 'Year and season of release' Fall 2026; checked against the store's active and archived Christmas sweaters/sweatshirts for duplicates.",
            "Fabric evidence: fabric name 'Pure cotton', main fabric composition cotton (percentage not stated); the listing says cotton knit only.",
            f"Vendor sizes kept: {', '.join(VENDOR.values())} in {', '.join(COLORS.values())}.",
        ],
    }
    (TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(handle, spec["vendor_prices_note"])


if __name__ == "__main__":
    main()
