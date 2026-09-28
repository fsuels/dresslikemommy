#!/usr/bin/env python3
"""Create the Christmas knit family hats listing as a DRAFT (accessory sets; not an engine listing).

Source: 1688 offer 1070411224313, 洛阳戴姿容服饰有限公司 (store nanmuxiu). Gate read 2026-09-27:
7 years on 1688, 48h pickup 100%, 48h fulfillment 100%, quality returns 0%, disputes 0%,
service 4.5; listed 2026-07-24, release attribute 2026年秋季; polyester knit; elastic brim.
Vendor SKUs: 成人/儿童/亲子套 × 圣诞树款 (Tree Stripe) / 圣诞彩球款 (Garland);
adult ¥7.6, child ¥7.2, parent-child set ¥14.6 (2 hats). Family Set of 4 = 2 parent-child sets.

Pricing (owner rule: landed <= 50% of price on a single-item order; ~100 g per hat):
landed = (cost + ¥3 + ¥45.4 + ¥8.2/100 g) / 7.11; price >= 2.06 x landed, rounded up to .99.
Adult ¥7.6 -> $18.99; child ¥7.2 -> $18.99; set ¥14.6/200 g -> $23.99; set of 4 ¥29.2/400 g -> $32.99.
Compare-at = price + $10. Cost per item = 50% of price (store bookkeeping default).

Usage: create_xmas_knit_hats.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai_images"))
import attach_images as A  # noqa: E402  (gql helper + token)

HANDLE = "christmas-knit-family-matching-hats"
TITLE = "Christmas Knit Family Matching Hats — Pom-Pom Elf Hats"
SEO_TITLE = "Christmas Family Matching Hats | Dress Like Mommy"
SEO_DESC = "Matching Christmas knit elf hats for moms, dads and kids: adult and child hats, parent and child sets, and family sets of 4."
STYLES = [("Tree Stripe", "TRE"), ("Garland", "GAR")]
SETS = [("Adult Hat", "ADT", "18.99"), ("Child Hat", "KID", "18.99"),
        ("Parent & Child Set", "PC", "23.99"), ("Family Set of 4", "F4", "32.99")]
BODY = (
    "<p>Matching Christmas knit hats for the whole family: long elf-style beanies with a red pom-pom tail, "
    "little yellow pom-poms around the brim, and a cozy red ribbed band.</p>"
    "<ul>"
    "<li><strong>Styles:</strong> Tree Stripe (red and green bands with little Christmas trees) or Garland "
    "(green with white garland loops and red dots).</li>"
    "<li><strong>Sets:</strong> Adult Hat, Child Hat, Parent &amp; Child Set (1 adult hat + 1 child hat), "
    "or Family Set of 4 (2 adult hats + 2 child hats).</li>"
    "<li><strong>Size:</strong> Adult hat about 42 cm long; child hat about 37 cm long; stretchy knit brim.</li>"
    "<li><strong>Fabric:</strong> Soft polyester knit.</li>"
    "<li><strong>Care:</strong> Follow the care label sewn into each hat.</li>"
    "<li><strong>Safety:</strong> Not for children under 3 years (small decorative pom-poms).</li>"
    "</ul>"
    "<p>Pair them with our matching family Christmas pajamas and sweaters for tree trimming, "
    "Christmas morning, and family photos.</p>"
)
TAGS = ["Family Matching", "Christmas", "Christmas Hats", "Christmas Accessories", "Accessories", "Hats",
        "Winter Hats", "Knit Hat", "Matching Family Outfits", "Family Photos",
        "Tree Stripe", "Garland", "Red", "Green", "Pom-Pom"]
BLOCKED = ("1688", "alibaba", "taobao", "supplier", "vendor", "grinch", "stitch", "disney", "rudolph", "season")


def main(dry: bool) -> None:
    payload = " ".join([TITLE, SEO_TITLE, SEO_DESC, BODY, *TAGS]).lower()
    bad = [w for w in BLOCKED if re.search(rf"\b{re.escape(w)}\b", payload)]
    if bad or len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESC) > 155:
        raise SystemExit(f"copy check failed: {bad} {len(TITLE)} {len(SEO_TITLE)} {len(SEO_DESC)}")
    variants = []
    for sname, stok in STYLES:
        for setname, settok, price in SETS:
            cmp_ = f"{float(price) + 10:.2f}"
            variants.append({
                "optionValues": [{"optionName": "Style", "name": sname}, {"optionName": "Set", "name": setname}],
                "price": price, "compareAtPrice": cmp_, "sku": f"DLM-XHAT-{stok}-{settok}",
                "inventoryPolicy": "DENY", "taxable": True,
                "inventoryItem": {"cost": f"{float(price) / 2:.2f}", "tracked": True, "requiresShipping": True},
            })
    text, refs = "single_line_text_field", "list.metaobject_reference"
    mfs = [
        ("custom", "category1", text, "Family Matching"), ("custom", "subcategory", text, "Accessories"),
        ("custom", "subcategory2", text, "Christmas Hats"), ("custom", "type", text, "Knit Hat"),
        ("mm-google-shopping", "custom_product", "boolean", "false"), ("mm-google-shopping", "gender", text, "unisex"),
        ("mm-google-shopping", "age_group", text, "adult"), ("mm-google-shopping", "condition", text, "new"),
        ("mm-google-shopping", "custom_label_0", text, "Family Matching"), ("mm-google-shopping", "custom_label_2", text, "Christmas"),
        ("mm-google-shopping", "custom_label_3", text, "Knit Hat"),
        ("shopify", "age-group", refs, json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])),
        ("shopify", "color-pattern", refs, json.dumps(["gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/70220546145"])),
        ("shopify", "fabric", refs, json.dumps(["gid://shopify/Metaobject/69622366305"])),
        ("shopify", "target-gender", refs, json.dumps(["gid://shopify/Metaobject/129972502625"])),
    ]
    inp = {
        "title": TITLE, "handle": HANDLE, "status": "DRAFT", "vendor": "Dress Like Mommy",
        "productType": "Family Matching Accessories", "descriptionHtml": BODY, "tags": TAGS,
        "category": "gid://shopify/TaxonomyCategory/aa-2-17-16",
        "seo": {"title": SEO_TITLE, "description": SEO_DESC},
        "productOptions": [{"name": "Style", "values": [{"name": s} for s, _ in STYLES]},
                           {"name": "Set", "values": [{"name": s} for s, _, _ in SETS]}],
        "variants": variants,
        "metafields": [{"namespace": n, "key": k, "type": t, "value": v} for n, k, t, v in mfs],
    }
    if dry:
        print(json.dumps(inp, ensure_ascii=False)[:1500]); return
    existing = A.gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": HANDLE})["productByHandle"]
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
    main("--dry-run" in sys.argv)
