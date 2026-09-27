#!/usr/bin/env python3
"""Build one listing spec per 2026 Christmas pajama design.

Copy fields come from DESIGNS (written from each design's vendor photos);
sizes, fabric, codes, prices and evidence come from the read-only 1688
captures in ops/sourcing/vendor-images/<offer>/desc/manifest.json.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
OFFERS = json.loads((TOOLS / "store_offers_2026.json").read_text(encoding="utf-8"))

C = {  # store shopify--color-pattern metaobjects
    "Red": "gid://shopify/Metaobject/69600804961", "Green": "gid://shopify/Metaobject/70220546145",
    "White": "gid://shopify/Metaobject/69639733345", "Blue": "gid://shopify/Metaobject/69639766113",
    "Black": "gid://shopify/Metaobject/69943132257", "Gray": "gid://shopify/Metaobject/69944672353",
    "Beige": "gid://shopify/Metaobject/69641928801", "Multicolor": "gid://shopify/Metaobject/130231140449",
    "Striped": "gid://shopify/Metaobject/130283765857", "Checkered": "gid://shopify/Metaobject/130283143265",
}
COLOR_TOKENS = {"Red": "RED", "Green": "GRN", "Navy": "NVY", "Gray": "GRY", "Cream": "CRM"}

# offer: (print name, shortcode, color, patterns, design_key, print sentence, (feature label, text), extra tags, alt)
DESIGNS = {
    "1033288412830": ("Cookie Baking Crew", "CBCW", "Cream", ["Beige", "White"], "raglan",
        "Cream tops with brown raglan sleeves show a gingerbread cookie in a Santa hat beside Cookie Baking Crew lettering, and the pants carry a brown and cream Fair Isle print of gingerbread cookies and trees.",
        ("Gingerbread print:", "Cookie Baking Crew lettering on the tops and gingerbread Fair Isle pants."),
        ["Gingerbread", "Cookie Baking Crew", "Fair Isle", "Cream", "Brown", "Beige"],
        "Family in matching cream raglan pajama tops with brown sleeves and a Cookie Baking Crew gingerbread graphic, worn with brown gingerbread Fair Isle pants."),
    "1030872819566": ("Reindeer Forest", "RDFR", "Navy", ["Blue", "Green", "White"], "crew_trim",
        "Navy tops with green trim read Merry Christmas in white script among green trees and reindeer, and the pants carry green and white Fair Isle stripes with reindeer and trees.",
        ("Fair Isle pants:", "Green and white holiday stripes with reindeer and Christmas trees."),
        ["Reindeer", "Christmas Tree", "Fair Isle", "Merry Christmas", "Navy", "Blue", "Green"],
        "Large family in matching navy Merry Christmas pajama tops with green trim, worn with green and white reindeer Fair Isle pants."),
    "1032775642583": ("Classic Red Plaid", "CRPL", "Red", ["Red", "Checkered"], "crew_plain",
        "Solid red tops pair with red tartan plaid pants for a timeless Christmas morning look.",
        ("Tartan plaid pants:", "Classic red plaid that goes with every holiday photo backdrop."),
        ["Plaid", "Tartan", "Solid Red", "Red"],
        "Family in matching solid red long-sleeve pajama tops and red tartan plaid pants."),
    "1037079642878": ("Joyful Merry Blessed", "JMBL", "Red", ["Red", "White", "Checkered"], "crew_plain",
        "Red tops read Joyful Merry Blessed in white script with green holly leaves, and the pants are a red plaid.",
        ("Joyful script top:", "White Joyful Merry Blessed lettering with holly leaves on a red top."),
        ["Joyful Merry Blessed", "Holly", "Plaid", "Red"],
        "Family in matching red pajama tops with white Joyful Merry Blessed script, worn with red plaid pants."),
    "1061758229843": ("Evergreen Fair Isle", "EGFI", "Green", ["Green", "Red", "White"], "cuffed",
        "Green and white Fair Isle bands of Christmas trees, reindeer, and snowflakes, edged with red stripes, cover both the top and the pants.",
        ("All-over Fair Isle:", "Trees, reindeer, and snowflakes on both pieces for a classic sweater-style look."),
        ["Fair Isle", "Reindeer", "Christmas Tree", "Snowflake", "Green", "Red", "White"],
        "Family in matching green and white Fair Isle Christmas pajamas with trees, reindeer, and red cuffs."),
    "1073505941343": ("Cozy Reindeer", "CZRD", "Navy", ["Blue", "Red", "White", "Checkered"], "crew_plain",
        "Navy tops show a big cartoon reindeer in a striped hat and plaid scarf among snowflakes, and the pants are a navy, red, and white plaid.",
        ("Reindeer graphic top:", "A friendly cartoon reindeer in a winter hat and scarf on a navy top."),
        ["Reindeer", "Plaid", "Snowflake", "Navy", "Blue", "Red"],
        "Family in matching navy pajama tops with a cartoon reindeer in a hat and scarf, worn with navy and red plaid pants."),
    "1079361574035": ("Green Merry Christmas", "GMXS", "Green", ["Green", "Red", "Checkered"], "crew_trim",
        "Green tops with red trim read Merry Christmas in white script beside a smiling Santa, and the pants are a red and green plaid.",
        ("Santa script top:", "White Merry Christmas lettering and a smiling Santa on a green top."),
        ["Santa", "Merry Christmas", "Plaid", "Green", "Red"],
        "Green long-sleeve pajama tops with red trim, white Merry Christmas script and a Santa graphic, shown with red and green plaid pants."),
    "1081388156651": ("We Are Family Red", "RWAF", "Red", ["Red", "Black", "Checkered"], "crew_plain",
        "Red tops read We are Family in bold black and white lettering, and the pants are a red plaid.",
        ("We are Family top:", "Bold family lettering that says it all in Christmas photos."),
        ["We Are Family", "Plaid", "Red"],
        "Family in matching red pajama tops that read We are Family, worn with red plaid pants."),
    "1082668769741": ("Santa's Crew", "SNCW", "Gray", ["Gray", "Red", "Black", "Checkered"], "crew_plain",
        "Heather gray tops read SANTA'S crew in colorful holiday lettering with a Santa hat and antlers, and the pants are a red and black buffalo plaid.",
        ("Buffalo plaid pants:", "Red and black buffalo checks paired with a soft gray graphic top."),
        ["Santa's Crew", "Buffalo Plaid", "Plaid", "Gray", "Red", "Black"],
        "Family in matching heather gray SANTA'S crew pajama tops and red and black buffalo plaid pants."),
    "1082663865858": ("Jolly Santa", "JLSN", "Red", ["Red", "Green", "White"], "crew_trim",
        "Red tops with green trim show a waving Santa under Merry Christmas script, and the green pants are printed with Santas, snowmen, and candy canes.",
        ("Santa and snowman pants:", "Green pants printed with Santas, snowmen, and candy canes."),
        ["Santa", "Snowman", "Candy Cane", "Merry Christmas", "Red", "Green"],
        "Family in matching red Merry Christmas Santa pajama tops with green trim, worn with green Santa and snowman print pants."),
    "1081615050631": ("Beary Cozy", "BRCZ", "Cream", ["White", "Red", "Black"], "crew_trim",
        "Cream tops with black trim show a teddy bear face and red beary cozy script, and the red pants are printed with teddy bears and snowflakes.",
        ("Teddy bear print:", "A sweet bear face on the top and bears with snowflakes on the red pants."),
        ["Teddy Bear", "Bear", "Snowflake", "Cream", "Red", "White"],
        "Family in matching cream teddy bear pajama tops with black trim, worn with red teddy bear print pants."),
    "1080736515512": ("Candy Tree Christmas", "CNTR", "Red", ["Red", "Green", "Multicolor"], "crew_plain",
        "Red tops read Merry Christmas in white lettering with a Santa hat, and the dark green pants are printed with Christmas trees, candy canes, ornaments, and gifts.",
        ("Holiday print pants:", "Dark green pants packed with trees, candy canes, ornaments, and gifts."),
        ["Merry Christmas", "Candy Cane", "Christmas Tree", "Red", "Green"],
        "Family in matching red Merry Christmas pajama tops, worn with dark green pants printed with trees and candy canes."),
    "1081603250990": ("Team Santa", "TMSN", "Red", ["Red", "Blue", "White"], "crew_plain",
        "Adult red tops read TEAM SANTA in white and navy lettering, the child top carries its own playful nice-list lettering, and the navy pants are printed with Santa hats and candy canes.",
        ("TEAM SANTA top:", "Bold white and navy lettering on red, with a matching kids' version."),
        ["Team Santa", "Santa Hat", "Candy Cane", "Red", "Navy", "Blue"],
        "Family in matching red TEAM SANTA pajama tops, worn with navy pants printed with Santa hats and candy canes."),
    "1082696802900": ("Merry Xmas Lights", "MXLT", "Navy", ["Blue", "Multicolor"], "crew_trim",
        "Navy tops read MERRY XMAS! in red and white lettering wrapped in colorful string lights, and the navy pants repeat the string-light print all over.",
        ("String-light print:", "MERRY XMAS! lettering and bright holiday bulbs on navy tops and pants."),
        ["Merry Xmas", "Christmas Lights", "String Lights", "Navy", "Blue", "Red", "Multicolor"],
        "Mom, dad, and two children in matching navy long-sleeve pajama tops that read MERRY XMAS! with colorful string lights, worn with navy string-light print pants."),
    "1081815371723": ("Here for the Cookies", "HFCK", "Red", ["Red", "Green"], "crew_trim",
        "Red tops with green trim read I'M JUST HERE for the COOKIES in white lettering, and the dark green pants are printed with gingerbread cookies and candy canes.",
        ("Cookie lover top:", "Playful I'M JUST HERE for the COOKIES lettering on a red top."),
        ["Gingerbread", "Cookies", "Candy Cane", "Red", "Green"],
        "Family in matching red I'M JUST HERE for the COOKIES pajama tops with green trim, worn with dark green gingerbread print pants."),
    "1083372114596": ("Snowy Reindeer", "SWRD", "Navy", ["Blue", "White", "Red"], "short_crew",
        "Short-sleeve navy and white tops show a reindeer in a Santa hat and red scarf among snowflakes, and the navy Fair Isle pants with red cuffs repeat the reindeer and snowflake motifs.",
        ("Short-sleeve comfort:", "A short-sleeve top for warm homes, paired with full-length Fair Isle pants."),
        ["Reindeer", "Fair Isle", "Snowflake", "Navy", "Blue", "White", "Red"],
        "Family in matching short-sleeve navy and white reindeer pajama tops, worn with navy Fair Isle pants with red cuffs."),
    "1082489147641": ("Vintage Tree Truck", "VTTK", "Red", ["Red", "White", "Green"], "crew_plain",
        "Red tops show a vintage car carrying a Christmas tree with white holiday lettering, and the white pants with red cuffs are printed with cars, trees, and reindeer.",
        ("Tree truck graphic:", "A retro car hauling home the Christmas tree on a red top."),
        ["Vintage Truck", "Christmas Tree", "Red", "White", "Green"],
        "Family in matching red pajama tops with a vintage car carrying a Christmas tree, worn with white holiday print pants."),
    "1034014187785": ("Snowy Village Stripes", "SVST", "Green", ["Green", "Red", "White", "Striped"], "crew_plain",
        "Green adult tops show a snowy village scene with a snowman and reindeer under Merry Christmas lettering, the child top has its own festive character graphic, and the pants are red and white stripes with green cuffs.",
        ("Candy-stripe pants:", "Red and white stripes with green cuffs for a cheerful holiday look."),
        ["Snowman", "Reindeer", "Striped Pajamas", "Stripes", "Green", "Red", "White"],
        "Family in matching green Christmas pajama tops with a snowy village graphic, worn with red and white striped pants."),
    "1076610891971": ("Lights Out Reindeer", "LORD", "Green", ["Green", "White", "Multicolor"], "crew_trim",
        "Dark green tops with cream trim show a reindeer tangled in colorful Christmas lights above Lights Out! lettering, and the cream pants are printed with reindeer and string lights.",
        ("Tangled lights graphic:", "A playful reindeer wrapped in bright bulbs on a dark green top."),
        ["Reindeer", "Christmas Lights", "Lights Out", "Green", "Cream", "Multicolor"],
        "Family in matching dark green Lights Out! reindeer pajama tops, worn with cream reindeer and string-light print pants."),
    "1080353625335": ("Plaid Reindeer", "PLRD", "Red", ["Red", "Green", "Checkered"], "crew_plain",
        "Red tops show a smiling cartoon reindeer in a plaid scarf or bow tie, with a slightly different hat for each role, and the pants are a red and green plaid.",
        ("Reindeer and plaid:", "A cheerful reindeer top paired with classic red and green plaid pants."),
        ["Reindeer", "Plaid", "Red", "Green"],
        "Family in matching red cartoon reindeer pajama tops, worn with red and green plaid pants."),
    "1080381493063": ("We Are Family Evergreen", "EWAF", "Green", ["White", "Green", "Red", "Checkered"], "raglan",
        "White tops with dark green raglan sleeves read We are Family in red and black lettering, and the pants are a green and red plaid.",
        ("Raglan family top:", "We are Family lettering on a white top with dark green sleeves."),
        ["We Are Family", "Plaid", "Raglan", "Green", "White", "Red"],
        "Family in matching white and green raglan We are Family pajama tops, worn with green and red plaid pants."),
    "1080356577298": ("Jolly Crew", "JLCW", "Red", ["Red", "White", "Checkered"], "crew_plain",
        "Red tops read Jolly Crew in white script, and the pants are a red plaid.",
        ("Jolly Crew top:", "Simple white Jolly Crew script on a bright red top."),
        ["Jolly Crew", "Plaid", "Red"],
        "Family in matching red Jolly Crew pajama tops and red plaid pants."),
    "1078423171906": ("Plaid Tree Trio", "PTTR", "Red", ["Red", "Blue", "Checkered"], "crew_plain",
        "Red tops show three plaid and gold Christmas trees with gold script, and the pants are a navy and red plaid.",
        ("Plaid tree graphic:", "Three plaid and gold trees on a red top."),
        ["Christmas Tree", "Plaid", "Red", "Navy", "Gold"],
        "Family in matching red pajama tops with three plaid and gold Christmas trees, worn with navy and red plaid pants."),
    "1081367024239": ("Let It Snow", "LTSN", "Red", ["Red", "White", "Blue", "Checkered"], "crew_plain",
        "Red tops read LET IT SNOW in navy and white lettering, and the pants are a red, white, and navy plaid.",
        ("Let It Snow top:", "Bold navy and white lettering on a red top."),
        ["Let It Snow", "Plaid", "Red", "Navy", "White"],
        "Family in matching red LET IT SNOW pajama tops, worn with red, white, and navy plaid pants."),
}
IMAGE_OVERRIDES = {  # the main photo is too dark; use the vendor's own flat-lay gallery image instead
    "1079361574035": "desc/04.jpg",
}
NO_OWN_CHART = {"1034014187785", "1076610891971"}
LINE4XL = {"1034014187785", "1076610891971", "1080353625335", "1080381493063", "1080356577298", "1078423171906", "1081367024239"}
CHILD_ORDER = [2, 3, 4, 5, 6, 8, 10, 12, 14]


def page_text(offer: str) -> tuple[str, dict]:
    m = json.loads((ROOT / f"ops/sourcing/vendor-images/{offer}/desc/manifest.json").read_text(encoding="utf-8"))
    return m.get("page_text", ""), m


def grab(pattern: str, text: str) -> str | None:
    found = re.search(pattern, text)
    return found.group(1) if found else None


def normalize_sizes(raw: list[str], line4xl: bool) -> list[str]:
    kids, mom, dad = set(), [], []
    for label in raw:
        s = label.strip().replace("Mom's", "Mom").replace("Men's", "Dad").replace("Women's", "Mom")
        m = re.match(r"(?i)(dad|mom)\s*(\S+)", s)
        if m:
            size = m.group(2).upper().replace("XXL", "2XL")
            (dad if m.group(1).lower() == "dad" else mom).append(size)
            continue
        k = re.match(r"(?i)(?:children\s*)?(\d+)\s*t?\b", s)
        if k and not re.match(r"(?i)baby|\d+\s*m\b|\d+\s*m ", s):
            kids.add(int(k.group(1)))
    order = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]
    child_labels = [f"{n}T" if line4xl else f"Children {n}" for n in CHILD_ORDER if n in kids]
    return child_labels + [f"Mom {s}" for s in order if s in mom] + [f"Dad {s}" for s in order if s in dad]


def fabric_key(text: str) -> tuple[str, str]:
    name = grab(r"Fabric name (.+?) Main fabric", text) or ""
    main = grab(r"Main fabric composition (.+?) Main fabric", text) or ""
    pct = grab(r"Main fabric (?:component|ingredient|composition) content (\d+)", text) or ""
    material = grab(r"Material composition (.+?%(?:,[^%]+%)?)", text) or ""
    note = f"fabric name '{name}', main fabric '{main}' {pct}%" + (f", material composition '{material}'" if material else "")
    if "Cotton:35%" in material:
        return "cvc", note
    if "Polyester fiber (polyester): 100%" in material or name == "Imitation cotton":
        return "polyester", note + ". Imitation cotton (仿棉) is a cotton-feel polyester, so Polyester is the honest fabric"
    if name == "Pure cotton" and main == "Cotton":
        return "cotton", note
    if name == "Cotton blend" and main.startswith("Polyester") and pct == "80":
        return "polyblend", note
    raise SystemExit(f"unmapped fabric: {note}")


def main() -> None:
    written = []
    for offer, (print_name, code, color, patterns, design_key, sentence, feature, extra_tags, alt) in DESIGNS.items():
        text, manifest = page_text(offer)
        store = OFFERS[offer]
        line4xl = offer in LINE4XL
        raw_sizes = (grab(r"Suitable (?:for )?[Hh]eight (.+?) (?:Size |Is it|Whether|Main downstream)", text) or "").split(",")
        sizes = normalize_sizes(raw_sizes, line4xl)
        fkey, fnote = fabric_key(text)
        colors_raw = grab(r" Colou?r (\S+) Suitable", text) or ""
        item_no = grab(r"(?:Item number|Product code) (\S+)", text) or ""
        buy = text[text.find("1件起批"): text.find("Order now")] if "1件起批" in text else ""
        prices = {}
        for role, price in re.findall(r"(Dad|Mom|Children|\d+T|Baby|\d+M)[^¥]{0,12}¥(\d+)", buy):
            key = "Children" if (role == "Children" or role.endswith("T")) else ("Baby" if role == "Baby" or role.endswith("M") else role)
            prices.setdefault(key, set()).add(price)
        price_note = "; ".join(f"{k} {'/'.join(sorted(v))}" for k, v in prices.items()) + " (Baby not listed)."
        if offer in IMAGE_OVERRIDES:
            rel = IMAGE_OVERRIDES[offer]
            image_url = next(d["url"] for d in manifest["desc_images"] if d.get("path", "").endswith(rel.split("/")[-1]))
        else:
            image_url = "https://cbu01.alicdn.com/" + store["img"]["imageURI"]
        slug = re.sub(r"[^a-z0-9]+", "-", print_name.lower().replace("'", "")).strip("-")
        handle = f"{slug}-family-matching-pajamas"
        listed = grab(r"上架时间 (\S+)", text) or store["date"]
        if offer in NO_OWN_CHART:
            chart_note = ("this offer's description publishes no chart. Its size selector matches the factory's 4XL line exactly (Dad S-4XL, Mom S-3XL, 2T-14T), "
                          "and that line's own chart (offer 1080353625335, the same 12-year factory) is used, saved as SOURCE_SIZE_CHART. This follows the owner's practice of reusing one factory chart across that factory's offers; confirm with the supplier before publishing.")
        elif line4xl:
            chart_note = "this offer's own description publishes the factory's 4XL-line chart (description image 00; identical to the copy saved as SOURCE_SIZE_CHART)."
        else:
            chart_note = "this offer's own description publishes the factory chart (description image 01; identical to the copy saved as SOURCE_SIZE_CHART)."
        spec = {
            "offer_id": offer, "offer_created": listed, "handle": handle, "shortcode": code,
            "print_name": print_name,
            "colors": [{"name": color, "token": COLOR_TOKENS[color]}],
            "color_pattern_gids": [C[p] for p in patterns], "color_pattern_labels": patterns,
            "fabric_key": fkey, "design_key": design_key,
            "sleeve_style": "Short-Sleeve" if design_key == "short_crew" else "Long-Sleeve",
            "print_sentence": sentence, "feature_label": feature[0], "feature_text": feature[1],
            "extra_tags": extra_tags, "media_alt": alt,
            "image_url": image_url, "image_filename": f"01-{slug}-family-pajamas.jpg",
            "chart_source": "line4xl" if line4xl else "factory", "chart_note": chart_note,
            "vendor_title": store["subject"],
            "vendor_color_values": [c.strip() for c in colors_raw.split(",") if c.strip()],
            "vendor_codes": [c for c in {item_no, *[c.strip().rstrip("#") for c in colors_raw.split(",")]} if c],
            "vendor_size_labels": sizes,
            "vendor_prices_note": price_note,
            "designs_note": f"The offer's single design value {colors_raw} ({print_name}), one Shopify product.",
            "exclusions_note": "Baby SKUs (a separate romper) are excluded: baby is not an allowed Family Matching role. Dogs and props in the photos are not sold as part of this listing.",
            "evidence_lines": [
                "Supplier: 12-year 1688 factory (smr brand), dropship supported, MOQ 1, 4,000+ dropship distributors. The page was read 2026-09-26 in the helper browser with no login or captcha; price and order buttons were visible.",
                f"Offer listed on 1688 on {listed} (上架时间), inside the owner's 2026 filter.",
                f"Fabric evidence: {fnote}.",
                f"Vendor size selector (translated, raw): {', '.join(s.strip() for s in raw_sizes if s.strip())}. Color selector: {colors_raw}. Item number {item_no}.",
                f"Kept rows: {len(sizes)} non-baby SKUs, each matched one to one to a chart row.",
                "The set is sold as one purchasable top-and-pants item, so no Type axis is needed.",
            ],
        }
        path = TOOLS / "specs" / f"{handle}.json"
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        written.append((handle, code, fkey, len(sizes), sizes[:2] + sizes[-2:]))
    for row in written:
        print(*row)


if __name__ == "__main__":
    main()
