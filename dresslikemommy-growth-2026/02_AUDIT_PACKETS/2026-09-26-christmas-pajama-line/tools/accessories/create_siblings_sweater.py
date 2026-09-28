#!/usr/bin/env python3
"""Create a siblings (brother & sister) matching kids' Christmas sweater listing as a DRAFT.
Standalone productSet listing like create_xmas_knit_hats.py (the engine has no kids-only role).

Source: 1688 store 深圳市宝安区腾云鸽服装商行 (brand TYG Kids), gate read 2026-09-28 from its
creditdetail: 14 years on 1688, 48h pickup 99.80%, overall fulfillment 99.8%, service 5.0, repeat 65%,
ships from 广东中山. Offer page: "48-Hour Shipping" (deliveryLimit 2), 1件起批 (MOQ 1).
Owner rules checked: release attribute "Autumn 2026" and listed 2026-06; no licensed characters;
fabric from the supplier's product-info panel: 67% cotton, 33% polyester.
Size chart transcribed from the offer's own 尺寸说明 (half chest doubled).

Pricing (owner rule: landed <= 50% of price on a single-item order):
landed = (cost + ¥3 + ¥45.4 + ¥8.2/100 g) / 7.11; price >= 2.06 x landed, rounded up to .99.
Compare-at = price + $10. Cost per item = the landed cost.

Usage: create_siblings_sweater.py <design-key> [--dry-run | --update-body]
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai_images"))
import attach_images as A  # noqa: E402  (gql helper + token)

G = {  # store metaobjects (color-pattern, fabric, age-group, target-gender, size)
    "Red": "gid://shopify/Metaobject/69600804961", "Green": "gid://shopify/Metaobject/70220546145",
    "White": "gid://shopify/Metaobject/69639733345", "Beige": "gid://shopify/Metaobject/69641928801",
    "Blue": "gid://shopify/Metaobject/69639766113",
    "Cotton": "gid://shopify/Metaobject/69622399073", "Polyester": "gid://shopify/Metaobject/69622366305",
    "child": "gid://shopify/Metaobject/128116523105", "unisex": "gid://shopify/Metaobject/129972502625",
}
# Vendor size -> (shopper label, recommended height cm, store size metaobject, sku suffix)
SIZES = [
    ("100", "2T", 90, "gid://shopify/Metaobject/129972863073", "2T"),
    ("110", "3-4 Years", 100, "gid://shopify/Metaobject/129972895841", "34Y"),
    ("120", "4-5 Years", 110, "gid://shopify/Metaobject/129972928609", "45Y"),
    ("130", "6 Years", 120, "gid://shopify/Metaobject/129972994145", "6Y"),
    ("140", "7-8 Years", 130, "gid://shopify/Metaobject/129973026913", "78Y"),
]
TYG_CHART = {  # vendor size: (length, half chest, shoulder, sleeve) cm, from the offer's size chart image
    "100": (39, 31, 25, 34), "110": (41.5, 33, 26.5, 36.5), "120": (44, 35, 28, 39),
    "130": (46.5, 37, 29.5, 41.5), "140": (49, 39, 31, 44),
}
DESIGNS = {
    "teddy-bear": {
        "offer": "1060255226703", "item": "3214", "cost_cny": 27.5, "grams": 250, "code": "SBTB",
        "handle": "teddy-bear-siblings-christmas-sweaters",
        "title": "Teddy Bear Siblings Christmas Sweaters — Kids Fair Isle Knit",
        "seo_title": "Teddy Bear Siblings Christmas Sweaters | Dress Like Mommy",
        "seo_desc": "Matching Christmas sweaters for brothers and sisters: cream Fair Isle knit with teddy bears in Santa hats, trees and snowflakes. Kids 2T to 8 years.",
        "lead": ("Matching Christmas sweaters for brothers and sisters: a cream Fair Isle knit with teddy bears "
                 "in red Santa hats, little green Christmas trees and red snowflake bands, finished with a red "
                 "ribbed hem and cuffs."),
        "colors": ["Beige", "Red", "Green"],
        "tags": ["Teddy Bear", "Fair Isle", "Christmas Tree", "Snowflake", "Cream", "Red", "Green"],
        "print": "Teddy Bear Fair Isle",
    },
    "red-truck": {  # vendor colour 宝蓝色 (royal blue); photos read dark blue, so copy says dark blue
        "offer": "1060255226364", "item": "3210", "cost_cny": 27.5, "grams": 250, "code": "SBRT",
        "handle": "red-truck-siblings-christmas-sweaters",
        "title": "Red Truck Siblings Christmas Sweaters — Kids Fair Isle Knit",
        "seo_title": "Red Truck Siblings Christmas Sweaters | Dress Like Mommy",
        "seo_desc": "Matching Christmas sweaters for brothers and sisters: dark blue Fair Isle knit with red trucks carrying trees, and snowflakes. Kids 2T to 8 years.",
        "lead": ("Matching Christmas sweaters for brothers and sisters: a dark blue Fair Isle knit with little red "
                 "trucks carrying Christmas trees, a row of green trees, white snowflakes and red-and-white dot "
                 "bands, finished with a ribbed hem and cuffs."),
        "colors": ["Blue", "Red", "Green", "White"],
        "tags": ["Red Truck", "Fair Isle", "Christmas Tree", "Snowflake", "Blue", "Red", "Green"],
        "print": "Red Truck Fair Isle",
    },
    "nordic-hearts": {  # vendor item 3225, 杏白 (apricot white); reindeer heads are beige, no red noses
        "offer": "1060266274215", "item": "3225", "cost_cny": 27.5, "grams": 250, "code": "SBNH",
        "handle": "nordic-hearts-siblings-christmas-sweaters",
        "title": "Nordic Hearts Siblings Christmas Sweaters — Kids Fair Isle Knit",
        "seo_title": "Nordic Hearts Siblings Christmas Sweaters | Dress Like Mommy",
        "seo_desc": "Matching Christmas sweaters for brothers and sisters: cream Fair Isle knit with reindeer, red snowflakes and hearts. Kids 2T to 8 years.",
        "lead": ("Matching Christmas sweaters for brothers and sisters: a cream Fair Isle knit with little beige "
                 "reindeer, bright red snowflakes, red and pink hearts and zigzag bands, finished with a cream "
                 "ribbed hem and cuffs."),
        "colors": ["Beige", "Red"],
        "tags": ["Nordic Hearts", "Fair Isle", "Reindeer", "Snowflake", "Hearts", "Cream", "Red"],
        "print": "Nordic Hearts Fair Isle",
    },
}
BLOCKED = ("1688", "alibaba", "taobao", "supplier", "vendor", "grinch", "stitch", "disney", "rudolph", "season")


def price_for(cost: float, grams: int) -> tuple[str, str]:
    landed = (cost + 3 + 45.4 + 8.2 * grams / 100) / 7.11
    return f"{math.ceil(2.06 * landed - 0.99) + 0.99:.2f}", f"{landed:.2f}"


def inch(cm: float) -> str:
    return f"{cm / 2.54:.1f}"


def body(d: dict) -> str:
    ages = {"2T": "2", "3-4 Years": "3-4", "4-5 Years": "4-5", "6 Years": "6", "7-8 Years": "7-8"}
    rows = "".join(
        f"<tr><td>{lab}</td><td>{ages[lab]}</td><td>{h} cm</td><td>{TYG_CHART[v][1] * 2} cm</td>"
        f"<td>{TYG_CHART[v][3]} cm</td><td>{TYG_CHART[v][0]} cm</td></tr>"
        for v, lab, h, _, _ in SIZES)
    return (
        f"<p>{d['lead']}</p>"
        "<ul>"
        "<li><strong>Matching look:</strong> Brothers and sisters wear the same design. Pick a size for each child.</li>"
        "<li><strong>Fabric:</strong> 67% cotton, 33% polyester in a soft, thick knit.</li>"
        "<li><strong>Style:</strong> Crew-neck pullover with long sleeves and ribbed hem and cuffs.</li>"
        "<li><strong>Sizes:</strong> Five kids' sizes from 2T to 7-8 years. Choose by height using the chart below.</li>"
        "<li><strong>Care:</strong> Follow the care label sewn into each sweater.</li>"
        "</ul>"
        "<h3>Size Chart - Sweater</h3>"
        '<table id="size-chart" class="size-chart"><thead><tr><th>Size</th><th>Age</th><th>Height (cm)</th>'
        "<th>Chest/Bust (cm)</th><th>Sleeve (cm)</th><th>Garment Length (cm)</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "<p>Height is the recommended child height. Chest is the sweater measured flat and doubled; allow 1-2 cm difference.</p>"
        "<p>Pair them with our matching family Christmas pajamas and sweaters for tree trimming, "
        "Christmas morning and family photos.</p>"
    )


def update_body(key: str) -> None:
    d = DESIGNS[key]
    p = A.gql("query($h:String!){productByHandle(handle:$h){id}}", {"h": d["handle"]})["productByHandle"]
    r = A.gql("mutation($i:ProductUpdateInput!){productUpdate(product:$i){product{id} userErrors{field message}}}",
              {"i": {"id": p["id"], "descriptionHtml": body(d)}})["productUpdate"]
    print("body updated", p["id"], r["userErrors"])


def main(key: str, dry: bool) -> None:
    d = DESIGNS[key]
    price, landed = price_for(d["cost_cny"], d["grams"])
    b = body(d)
    tags = sorted(dict.fromkeys(["Siblings", "Siblings Matching", "Brother and Sister", "Kids", "Kids Sweater",
                                 "Christmas", "Christmas Sweaters", "Kids Christmas Sweater", "Sweaters", "Knit Sweater",
                                 "Long Sleeve Top", "Tops", "Winter", "Family Photos", d["print"], *d["tags"],
                                 *[lab for _, lab, _, _, _ in SIZES]]))
    payload = " ".join([d["title"], d["seo_title"], d["seo_desc"], b, *tags]).lower()
    bad = [w for w in BLOCKED if re.search(rf"\b{re.escape(w)}\b", payload)]
    if bad or len(d["title"]) > 70 or len(d["seo_title"]) > 60 or len(d["seo_desc"]) > 155:
        raise SystemExit(f"copy check failed: {bad} {len(d['title'])} {len(d['seo_title'])} {len(d['seo_desc'])}")
    if float(landed) > float(price) / 2:
        raise SystemExit(f"margin rule failed: landed {landed} > 50% of {price}")
    cmp_ = f"{float(price) + 10:.2f}"
    variants = [{
        "optionValues": [{"optionName": "Size", "name": lab}],
        "price": price, "compareAtPrice": cmp_, "sku": f"DLM-{d['code']}-KID-{suf}",
        "inventoryPolicy": "DENY", "taxable": True,
        "inventoryItem": {"cost": landed, "tracked": True, "requiresShipping": True},
    } for _, lab, _, _, suf in SIZES]
    text, refs = "single_line_text_field", "list.metaobject_reference"
    mfs = [
        ("custom", "category1", text, "Siblings"), ("custom", "subcategory", text, "Sweaters"),
        ("custom", "subcategory2", text, "Christmas Sweaters"), ("custom", "pattern", text, d["print"]),
        ("custom", "style", text, "Crewneck Sweater"), ("custom", "type", text, "Knit Sweater"),
        ("mm-google-shopping", "custom_product", "boolean", "false"), ("mm-google-shopping", "gender", text, "unisex"),
        ("mm-google-shopping", "age_group", text, "kids"), ("mm-google-shopping", "condition", text, "new"),
        ("mm-google-shopping", "custom_label_0", text, "Siblings"), ("mm-google-shopping", "custom_label_1", text, d["print"]),
        ("mm-google-shopping", "custom_label_2", text, "Christmas"), ("mm-google-shopping", "custom_label_3", text, "Crewneck Sweater"),
        ("mm-google-shopping", "custom_label_4", text, "Siblings Matching Sweaters"),
        ("shopify", "age-group", refs, json.dumps([G["child"]])),
        ("shopify", "color-pattern", refs, json.dumps([G[c] for c in d["colors"]])),
        ("shopify", "fabric", refs, json.dumps([G["Cotton"], G["Polyester"]])),
        ("shopify", "size", refs, json.dumps([s[3] for s in SIZES])),
        ("shopify", "target-gender", refs, json.dumps([G["unisex"]])),
    ]
    inp = {
        "title": d["title"], "handle": d["handle"], "status": "DRAFT", "vendor": "dresslikemommy.com",
        "productType": "Siblings Matching Sweaters", "descriptionHtml": b, "tags": tags,
        "category": "gid://shopify/TaxonomyCategory/aa-1-13-12",
        "seo": {"title": d["seo_title"], "description": d["seo_desc"]},
        "productOptions": [{"name": "Size", "values": [{"name": lab} for _, lab, _, _, _ in SIZES]}],
        "variants": variants,
        "metafields": [{"namespace": n, "key": k, "type": t, "value": v} for n, k, t, v in mfs],
    }
    if dry:
        print(price, cmp_, landed, len(tags)); print(b[:600]); return
    existing = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": d["handle"]})["productByHandle"]
    if existing:
        if existing["status"] != "DRAFT":
            raise SystemExit("exists and not DRAFT; refusing")
        inp["id"] = existing["id"]
    r = A.gql("""mutation($i:ProductSetInput!){productSet(synchronous:true,input:$i){
        product{id handle status variants(first:20){nodes{sku price compareAtPrice}}} userErrors{field message}}}""", {"i": inp})["productSet"]
    if r["userErrors"]:
        raise SystemExit(r["userErrors"])
    p = r["product"]
    print(p["id"], p["handle"], p["status"], [(v["sku"], v["price"]) for v in p["variants"]["nodes"]])


if __name__ == "__main__":
    if "--update-body" in sys.argv:
        update_body(sys.argv[1])
    else:
        main(sys.argv[1], "--dry-run" in sys.argv)
