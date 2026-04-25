#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"
export SHOPIFY_STORE_DOMAIN SHOPIFY_ADMIN_ACCESS_TOKEN

python3 - <<'PYRUN'
import csv
import html
import json
import math
import mimetypes
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "picnic-plaid-family-matching-set"
TITLE = "Picnic Plaid Family Matching Set - Dress & Shirt"
SEO_TITLE = "Picnic Plaid Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Lightweight plaid family matching set in blue or red for mom, dad, girls & boys. Dress sizes 2Y-3XL and shirt sizes 2Y-4XL."
VENDOR_URL = "https://detail.1688.com/offer/914314067847.html"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Outfit Sets"
SHORTCODE = "PPLA"
COLORWAYS = [("Blue", "BLUE"), ("Red", "RED")]
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-ppla-picnic-plaid-family-matching-set.sh"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"
for path in [LISTING_MD.parent, UPLOAD_DIR]:
    path.mkdir(parents=True, exist_ok=True)


def compare_at(price):
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


CHILD_COMPARE = compare_at(CHILD_PRICE)
ADULT_COMPARE = compare_at(ADULT_PRICE)


def kg(jin_range):
    lo, hi = [float(x) for x in re.split(r"[-–]", jin_range)]
    return f"{lo / 2:g}-{hi / 2:g} kg"


size_token = {
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
    "Mother L": "L",
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Mother 3XL": "3XL",
    "Father S": "S",
    "Father M": "M",
    "Father L": "L",
    "Father XL": "XL",
    "Father 2XL": "2XL",
    "Father 3XL": "3XL",
    "Father 4XL": "4XL",
}


def child_row(vendor, picker, height):
    age_map = {
        "Child 2 Years": "2",
        "Child 3 Years": "3",
        "Child 4 Years": "4",
        "Child 5 Years": "5",
        "Child 6-7 Years": "6-7",
        "Child 8 Years": "8",
        "Child 9-10 Years": "9-10",
    }
    weight_map = {
        "Child 2 Years": "12-14.5 kg",
        "Child 3 Years": "15-17.5 kg",
        "Child 4 Years": "18-20 kg",
        "Child 5 Years": "20.5-22.5 kg",
        "Child 6-7 Years": "23-25 kg",
        "Child 8 Years": "25.5-30 kg",
        "Child 9-10 Years": "30.5-40 kg",
    }
    return vendor, picker, age_map[picker], weight_map[picker], height


chart = []


def add_dress(audience, role, vendor, picker, age, weight, height, chest, length, source_note):
    hip = chest + 4 if audience == "child" else chest + 6
    waist = chest if audience == "child" else hip - 8
    chart.append({
        "audience": audience,
        "role": role,
        "garment": "Dress",
        "vendor_label": vendor,
        "picker_label": picker,
        "sku_suffix": size_token[picker],
        "age": age,
        "weight": weight,
        "height": height,
        "chest_cm": chest,
        "hip_cm": hip,
        "waist_cm": waist,
        "length_cm": length,
        "skirt_cm": length,
        "sleeve_cm": 0,
        "pant_cm": 0,
        "source_note": source_note,
    })


def add_shirt(audience, role, vendor, picker, age, weight, height, chest, length, shoulder, sleeve, source_note):
    waist = chest if audience == "child" else chest - 12
    chart.append({
        "audience": audience,
        "role": role,
        "garment": "Shirt",
        "vendor_label": vendor,
        "picker_label": picker,
        "sku_suffix": size_token[picker],
        "age": age,
        "weight": weight,
        "height": height,
        "chest_cm": chest,
        "hip_cm": chest,
        "waist_cm": waist,
        "length_cm": length,
        "skirt_cm": 0,
        "sleeve_cm": sleeve,
        "shoulder_cm": shoulder,
        "pant_cm": 0,
        "source_note": source_note,
    })


child_sizes = [
    child_row("90", "Child 2 Years", "85-95 cm"),
    child_row("100", "Child 3 Years", "95-105 cm"),
    child_row("110", "Child 4 Years", "106-115 cm"),
    child_row("120", "Child 5 Years", "116-125 cm"),
    child_row("130", "Child 6-7 Years", "126-135 cm"),
    child_row("140", "Child 8 Years", "136-143 cm"),
    child_row("150", "Child 9-10 Years", "143-152 cm"),
]

for row, (length, chest) in zip(child_sizes, [(58, 60), (61, 64), (64, 68), (67, 72), (70, 76), (73, 80), (76, 84)]):
    add_dress("child", "Girl Dress", *row, chest, length, "Vendor girls dress table publishes skirt length, chest, and height; hip/waist derived by dress rules.")

for vendor, picker, length, chest, weight, note in [
    ("S", "Mother S", 106, 92, kg("75-90"), "Vendor adult dress table publishes length, chest, and weight; hip/waist derived by mother dress rules."),
    ("M", "Mother M", 108, 96, kg("91-105"), "Vendor adult dress table publishes length, chest, and weight; hip/waist derived by mother dress rules."),
    ("L", "Mother L", 110, 100, kg("106-120"), "Vendor adult dress table publishes length, chest, and weight; hip/waist derived by mother dress rules."),
    ("XL", "Mother XL", 112, 104, kg("121-135"), "Vendor adult dress table publishes length, chest, and weight; hip/waist derived by mother dress rules."),
    ("XXL", "Mother 2XL", 114, 108, kg("136-145"), "Vendor adult dress table publishes length, chest, and weight; hip/waist derived by mother dress rules."),
    ("3XL定制", "Mother 3XL", 116, 112, kg("146-160"), "Vendor publishes 3XL custom with weight only; length/chest are extended from the visible grading to preserve the published size row."),
]:
    add_dress("mother", "Mother Dress", vendor, picker, "—", weight, "—", chest, length, note)

for row, (length, chest, shoulder) in zip(child_sizes, [(42, 80, 39), (45, 86, 40), (48, 90, 41), (51, 94, 42), (54, 98, 43), (58, 102, 44), (62, 106, 45)]):
    add_shirt("child", "Boy Shirt", *row, chest, length, shoulder, 0, "Vendor boys table includes shirt length, chest, shoulder, plus pants columns; pants columns excluded because Type is Shirt.")

for vendor, picker, length, chest, shoulder, sleeve, weight in [
    ("S", "Father S", 67, 104, 46, 19, kg("80-98")),
    ("M", "Father M", 69, 108, 47, 20, kg("98-115")),
    ("L", "Father L", 71, 112, 48, 21, kg("116-130")),
    ("XL", "Father XL", 73, 116, 49, 22, kg("131-145")),
    ("XXL", "Father 2XL", 75, 120, 50, 23, kg("146-160")),
    ("3XL", "Father 3XL", 77, 124, 51, 24, kg("165-180")),
    ("4XL", "Father 4XL", 79, 128, 52, 24, kg("180-220")),
]:
    add_shirt("father", "Father Shirt", vendor, picker, "—", weight, "—", chest, length, shoulder, sleeve, "Vendor adult shirt table includes shirt length, chest, shoulder, sleeve, weight, plus pants columns; pants columns excluded because Type is Shirt.")

size_map = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}
role_token = {"Girl Dress": "GRL", "Mother Dress": "MOM", "Boy Shirt": "BOY", "Father Shirt": "DAD"}


def gql(query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(API, data=data, headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        out = json.loads(response.read())
    if out.get("errors"):
        raise SystemExit(out["errors"])
    return out


def user_errors(out, path):
    cursor = out
    for part in path.split("."):
        if part:
            cursor = cursor.get(part, {})
    if cursor:
        raise SystemExit(cursor)


def sku(row, color_token):
    return f"DLM-{SHORTCODE}-{role_token[row['role']]}-{row['sku_suffix']}-{color_token}"


def nice_num(value):
    try:
        number = float(value)
        return str(int(number)) if number.is_integer() else f"{number:g}"
    except Exception:
        return str(value)


def cm_in(value):
    if not value:
        return "—"
    return f"{nice_num(value)} cm / {nice_num(float(value) / 2.54)} in"


def dual_range(text, unit, multiplier, out_unit):
    if text in ["—", "-"]:
        return "—"
    match = re.match(r"([\d.]+)-([\d.]+) " + re.escape(unit), text)
    if not match:
        return html.escape(text)
    lo, hi = map(float, match.groups())
    return f"{nice_num(lo)}-{nice_num(hi)} {unit} / {nice_num(lo * multiplier)}-{nice_num(hi * multiplier)} {out_unit}"


def table(rows, garment):
    length_header = "Skirt Length (cm/in)" if garment == "Dress" else "Sleeve Length (cm/in)"
    trs = []
    for row in rows:
        cells = [
            html.escape(row["picker_label"]),
            html.escape(row["age"]),
            html.escape(dual_range(row["weight"], "kg", 2.20462, "lbs")),
            html.escape(dual_range(row["height"], "cm", 1 / 2.54, "in")),
            cm_in(row["chest_cm"]),
            cm_in(row["skirt_cm"] if garment == "Dress" else row["sleeve_cm"]),
            "—",
            cm_in(row["hip_cm"]),
            cm_in(row["waist_cm"]),
            cm_in(row["length_cm"]),
        ]
        trs.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    return (
        f"<h3>Size Chart - {garment}</h3>\n"
        f'<table id="size-chart-{garment.lower()}"><thead><tr>'
        "<th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        f"<th>Chest/Bust (cm/in)</th><th>{length_header}</th><th>Pant/Short or — (cm/in)</th>"
        "<th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th>"
        "</tr></thead><tbody>" + "\n".join(trs) + "</tbody></table>"
    )


body = "\n".join([
    "<ul>",
    "<li><strong>Fabric:</strong> Lightweight woven fabric with a soft warm-weather drape; exact fiber composition was not visible from the vendor evidence.</li>",
    "<li><strong>Family story:</strong> A four-role family matching plaid look for moms, dads, girls, and boys.</li>",
    "<li><strong>Print:</strong> Picnic Plaid comes in Blue or Red gingham-style checks for a coordinated summer photo palette.</li>",
    "<li><strong>Design details:</strong> Girls and moms wear the strappy plaid dress with white lace-panel skirt detail; boys and dads wear the matching short-sleeve plaid shirt.</li>",
    "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and use a cool iron inside-out if needed.</li>",
    "<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S-3XL, and Father S-4XL.</li>",
    "</ul>",
    table([row for row in chart if row["garment"] == "Dress"], "Dress"),
    table([row for row in chart if row["garment"] == "Shirt"], "Shirt"),
    "<p>Picnic Plaid keeps the matching look crisp and easy: a lace-trimmed plaid dress for moms and girls, plus a clean short-sleeve shirt for dads and boys. The two colorways share the same vendor size chart, so families can choose Blue, Red, or mix both tones in one coordinated order.</p>",
    "<p>Use the Type, Size, and Color selectors to build the exact set for each family member. The listing includes the dress and shirt garments only; pants, shorts, bags, hats, shoes, and jewelry shown in vendor imagery are styling props.</p>",
    "<h3>Key Features:</h3>",
    "<ul>",
    "<li><strong>Two garment choices:</strong> Dress for girls and moms, shirt for boys and dads.</li>",
    "<li><strong>Two plaid colors:</strong> Blue and Red colorways share one product listing.</li>",
    "<li><strong>Role-bearing sizes:</strong> Size labels make family ordering clearer across kids and adults.</li>",
    "<li><strong>Photo-ready details:</strong> Lace panels and gingham checks feel polished for vacations, picnics, and portraits.</li>",
    "<li><strong>Chart-backed sizing:</strong> Every live variant is derived from the attached vendor size chart.</li>",
    "</ul>",
    "<p>Choose each family member's garment, size, and plaid color to create a cheerful matching set for the next sunny outing.</p>",
])

BODY_HTML_OUT.write_text(body)
SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2))

node = gql("query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName isLeaf}}}", {"id": TAXONOMY_GID})["data"]["node"]
if not node or node["fullName"] != EXPECTED_TAXONOMY or not node["isLeaf"]:
    raise SystemExit(f"taxonomy guard failed: {node}")

required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm"}
for row in chart:
    missing = [key for key in required if key not in row]
    if missing:
        raise SystemExit(f"missing required fields for {row}: {missing}")
if len({(row["role"], row["picker_label"]) for row in chart}) != len(chart):
    raise SystemExit("duplicate role/picker rows detected")
if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
    raise SystemExit("title or SEO length guard failed")

size_values = []
for row in chart:
    if row["picker_label"] not in size_values:
        size_values.append(row["picker_label"])

variants = []
recap = []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    for color_name, color_token in COLORWAYS:
        variant = {
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {"sku": sku(row, color_token), "tracked": True, "requiresShipping": True},
            "optionValues": [
                {"optionName": "Type", "name": row["garment"]},
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": color_name},
            ],
        }
        variants.append(variant)
        gid, catalog_label = size_map[row["picker_label"]]
        recap.append({**row, "color": color_name, "sku": sku(row, color_token), "price": price, "compare": compare, "size_gid": gid, "catalog_label": catalog_label})

if len(variants) != len(chart) * len(COLORWAYS):
    raise SystemExit("variant cartesian count guard failed")

options = [
    {"name": "Type", "values": [{"name": "Dress"}, {"name": "Shirt"}]},
    {"name": "Size", "values": [{"name": value} for value in size_values]},
    {"name": "Color", "values": [{"name": value[0]} for value in COLORWAYS]},
]
tags = sorted(set([
    "Family Matching", "Mommy and Me", "Daddy and Me", "Matching Family Set", "Matching Family Outfits",
    "Matching Family Dress", "Matching Family Shirt", "Sets", "Summer", "Beach", "Vacation", "Resort",
    "Picnic Plaid", "Plaid", "Gingham", "Checkered", "Blue", "Red", "White", "Lace Panel Dress",
    "Girl Dress", "Mother Dress", "Boy Shirt", "Father Shirt", "Short Sleeve Shirt", "Strappy Dress",
    "Four-Role Matching", VENDOR_URL, *size_values,
    "Mother S", "Mother M", "Mother L", "Mother XL", "Mother 2XL", "Mother 3XL",
    "Father S", "Father M", "Father L", "Father XL", "Father 2XL", "Father 3XL", "Father 4XL",
]))

product_input = {
    "handle": HANDLE,
    "title": TITLE,
    "descriptionHtml": body,
    "vendor": "dresslikemommy.com",
    "productType": PRODUCT_TYPE,
    "tags": tags,
    "status": "ACTIVE",
    "category": TAXONOMY_GID,
    "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
}

existing = gql("query($handle:String!){productByHandle(handle:$handle){id variants(first:100){nodes{id sku}}}}", {"handle": HANDLE})["data"]["productByHandle"]
if existing:
    product_id = existing["id"]
    live_skus = sorted(v["sku"] for v in existing["variants"]["nodes"] if v.get("sku"))
    spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
    if live_skus and live_skus != spec_skus:
        raise SystemExit(f"existing product has unexpected SKUs: {live_skus}")
    out = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id} userErrors{field message}}}", {"product": {"id": product_id, **product_input}})
    user_errors(out, "data.productUpdate.userErrors")
    if live_skus == spec_skus:
        by_sku = {v["sku"]: v["id"] for v in existing["variants"]["nodes"]}
        updates = [{"id": by_sku[v["inventoryItem"]["sku"]], **v} for v in variants]
        out = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$productId,variants:$variants){userErrors{field message}}}", {"productId": product_id, "variants": updates})
    else:
        out = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
    user_errors(out, "data.productVariantsBulkUpdate.userErrors" if live_skus == spec_skus else "data.productVariantsBulkCreate.userErrors")
else:
    out = gql("mutation($input:ProductInput!){productCreate(input:$input){product{id} userErrors{field message}}}", {"input": {**product_input, "productOptions": options}})
    user_errors(out, "data.productCreate.userErrors")
    product_id = out["data"]["productCreate"]["product"]["id"]
    out = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
    user_errors(out, "data.productVariantsBulkCreate.userErrors")

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Picnic Plaid"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Picnic Plaid"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Shirt"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/69639733345"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(list(dict.fromkeys(size_map[row["picker_label"]][0] for row in chart)))},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
]
for start in range(0, len(metafields), 25):
    out = gql("mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){userErrors{field message}}}", {"metafields": metafields[start:start + 25]})
    user_errors(out, "data.metafieldsSet.userErrors")

publications = [{"publicationId": gid} for gid in [
    "gid://shopify/Publication/55169925",
    "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225",
    "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
]]
out = gql("mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}", {"id": product_id, "input": publications})
user_errors(out, "data.publishablePublish.userErrors")

existing_media = gql("query($id:ID!){product(id:$id){media(first:100){nodes{... on MediaImage{id alt image{url}}}}}}", {"id": product_id})["data"]["product"]["media"]["nodes"]
existing_alts = {node.get("alt") for node in existing_media}
for image_path in sorted([p for p in UPLOAD_DIR.iterdir() if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"] and not p.name.startswith("source-size-chart")]):
    if image_path.name.startswith("01"):
        alt = "Family wearing red Picnic Plaid matching dress and shirt set."
    elif image_path.name.startswith("02"):
        alt = "Family wearing blue Picnic Plaid matching dress and shirt set."
    else:
        alt = "Picnic Plaid family matching dress and shirt set."
    if alt in existing_alts:
        continue
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    out = gql("mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}", {"input": [{"filename": image_path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]})
    user_errors(out, "data.stagedUploadsCreate.userErrors")
    target = out["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    args = ["curl", "-sS", "-X", "POST", target["url"]]
    for parameter in target["parameters"]:
        args += ["-F", f"{parameter['name']}={parameter['value']}"]
    args += ["-F", f"file=@{image_path}"]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    out = gql("mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){userErrors{field message}}}", {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})
    user_errors(out, "data.productCreateMedia.userErrors")

time.sleep(3)
verify = gql("query($id:ID!){product(id:$id){id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}} collections(first:50){nodes{title handle}} metafields(first:100){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}}}}", {"id": product_id})
VERIFY_JSON_OUT.write_text(json.dumps(verify, indent=2))
product = verify["data"]["product"]
live_variants = product["variants"]["nodes"]
live_skus = sorted(v["sku"] for v in live_variants)
spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
body_tables = re.findall(r"<table\b.*?</table>", product["descriptionHtml"], re.S)
table_headers = [len(re.findall(r"<th\b", table_html)) for table_html in body_tables]
table_rows = sum(len(re.findall(r"<tr\b", table_html)) - 1 for table_html in body_tables)
published_ids = {node["publication"]["id"] for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"]}
expected_publications = {p["publicationId"] for p in publications}
price_ok = all(
    live["price"] == next(v["price"] for v in variants if v["inventoryItem"]["sku"] == live["sku"])
    and live["compareAtPrice"] == next(v["compareAtPrice"] for v in variants if v["inventoryItem"]["sku"] == live["sku"])
    and live["inventoryPolicy"] == "DENY"
    and live["inventoryItem"]["tracked"]
    and live["inventoryItem"]["requiresShipping"]
    for live in live_variants
)
checks = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("SEO description <= 155 chars", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("Live variant count matches derived variants", len(live_variants) == len(variants), f"{len(live_variants)} vs {len(variants)}"),
    ("Live SKUs match derived SKUs", live_skus == spec_skus, ", ".join(live_skus)),
    ("Size table rows match SIZE_CHART", table_rows == len(chart), f"{table_rows} vs {len(chart)}"),
    ("Each size table has 10 headers", table_headers == [10, 10], str(table_headers)),
    ("Forced price/inventory parity", price_ok, "FORCE_SPEC_PRICES true"),
    ("Taxonomy fullName matches", product["category"]["fullName"] == EXPECTED_TAXONOMY, product["category"]["fullName"]),
    ("Required publications are live", expected_publications.issubset(published_ids), str(sorted(published_ids))),
    ("Online store URL populated", bool(product["onlineStoreUrl"]), product["onlineStoreUrl"] or ""),
]
if not all(ok for _label, ok, _detail in checks):
    raise SystemExit("verification failed: " + repr(checks))

with CSV_HEADER_SOURCE.open(newline="") as fh:
    header = next(csv.reader(fh))
rows = []
for row in recap:
    csv_row = {field: "" for field in header}
    values = {
        "Handle": HANDLE,
        "Title": TITLE,
        "Body (HTML)": body,
        "Vendor": "dresslikemommy.com",
        "Product Category": EXPECTED_TAXONOMY,
        "Type": PRODUCT_TYPE,
        "Tags": ", ".join(product["tags"]),
        "Published": "TRUE",
        "Option1 Name": "Type",
        "Option1 Value": row["garment"],
        "Option2 Name": "Size",
        "Option2 Value": row["picker_label"],
        "Option3 Name": "Color",
        "Option3 Value": row["color"],
        "Variant SKU": row["sku"],
        "Variant Grams": "0",
        "Variant Inventory Tracker": "shopify",
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": row["price"],
        "Variant Compare At Price": row["compare"],
        "Variant Requires Shipping": "TRUE",
        "Variant Taxable": "TRUE",
        "SEO Title": SEO_TITLE,
        "SEO Description": SEO_DESCRIPTION,
        "Google Shopping / Gender": "unisex",
        "Google Shopping / Age Group": "adult",
        "Google Shopping / Condition": "new",
        "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "Family Matching",
        "Google Shopping / Custom Label 1": "Picnic Plaid",
        "Google Shopping / Custom Label 2": "Summer",
        "Google Shopping / Custom Label 3": "Dress & Shirt",
        "Google Shopping / Custom Label 4": "Four-Role Matching",
        "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": "Picnic Plaid",
        "Style (product.metafields.custom.style)": "Matching Family Set",
        "SubCategory (product.metafields.custom.subcategory)": "Set",
        "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set",
        "Type (product.metafields.custom.type)": "Two-Piece Set",
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": "Blue, Red, White",
        "Size (product.metafields.shopify.size)": ", ".join(size_values),
        "Status": "active",
    }
    for key, value in values.items():
        if key in csv_row:
            csv_row[key] = value
    rows.append(csv_row)
with CSV_OUT.open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

written_metafields = sorted(f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"] if node["namespace"] in ["custom", "mm-google-shopping", "shopify", "global"])
lines = [
    f"# {TITLE}",
    "",
    "## Links",
    f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    f"- **Live:** {product['onlineStoreUrl']}",
    f"- **Vendor:** {VENDOR_URL}",
    f"- **Product GID:** `{product_id}`",
    f"- **Handle:** `{HANDLE}`",
    "",
    "## Inputs (resolved)",
    "| Field | Value |",
    "|---|---|",
    f"| VENDOR_URL | {VENDOR_URL} |",
    "| SIZE_CHART_SOURCE | attached image |",
    "| LISTING_MODE | Family Matching |",
    "| PRIMARY_CATEGORY | Sets -> FamilySet (Shopify taxonomy: Outfit Sets) |",
    "| DESIGNS_TO_LIST | Color: Blue, Red; Type: Dress, Shirt |",
    "| FORCE_SPEC_PRICES | true |",
    f"| SHORTCODE | auto -> `{SHORTCODE}` |",
    "| COLOR_TOKEN | Blue -> `BLUE`; Red -> `RED` |",
    "",
    "## Vendor fetch status",
    "The direct 1688 page was unreachable from this shell during the run, so the attached product photos and attached size-chart image were used as authoritative evidence. The chart publishes child/adult dress and shirt tables; pants/short columns shown inside shirt tables were excluded because the requested Type values are Shirt and Dress only.",
    "",
    "## Option axes",
    "- Option 1: Type -> Dress, Shirt",
    "- Option 2: Size -> role-bearing size labels",
    "- Option 3: Color -> Blue, Red",
    f"- Variants live: {len(live_variants)} ({len(chart)} size rows x {len(COLORWAYS)} colors)",
    "",
    "## SIZE_CHART / Variant Recap",
    "| Role | Vendor | Picker | Color | Type | SKU | Price | shopify.size GID |",
    "|---|---|---|---|---|---|---|---|",
]
for row in recap:
    lines.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['color']} | {row['garment']} | `{row['sku']}` | {row['price']} | `{row['size_gid']}` ({row['catalog_label']}) |")
lines += [
    "",
    "## Derivations",
    "- Vendor adult weights were listed in `斤` and converted to kg in the saved SIZE_CHART and shopper-facing table.",
    "- Dress hip/waist values were derived where the vendor omitted them: child hip = chest + 4, child waist = chest; adult dress hip = bust + 6, waist = hip - 8.",
    "- Mother 3XL custom row is preserved from the chart; chest and length are extended from the visible adult-dress grading because the row only shows a weight recommendation.",
    "- Shirt waist/hip values were derived where omitted: child hip/waist = chest; adult shirt hip = chest, waist = chest - 12.",
    "- Pants/shorts, bags, hats, shoes, jewelry, and styling shorts are excluded from the sellable variant set.",
    "",
    "## Verification",
    "| Check | Result | Detail |",
    "|---|---|---|",
]
for label, ok, detail in checks:
    lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines += [
    "",
    "## Metafields Written",
    *[f"- `{key}`" for key in written_metafields],
    "",
    "## Metafields Skipped",
    "- `shopify.fabric`: source evidence does not confirm exact fiber composition.",
    "- `shopify.sleeve-length-type`: dress is strappy while shirts are short sleeve; one product-level value would be misleading.",
    "- `shopify.dress-style`, `shopify.dress-occasion`, `shopify.skirt-dress-length-type`: product taxonomy is Outfit Sets and includes shirts.",
    "",
    "## Smart Collections",
    ", ".join(sorted(collection["handle"] for collection in product["collections"]["nodes"])) or "Pending smart collection propagation.",
    "",
    "## Publications",
    ", ".join(sorted(node["publication"]["name"] for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"])),
    "",
    "## Saved Files",
    f"- `{SCRIPT_PATH}`",
    f"- `{LISTING_MD}`",
    f"- `{CSV_OUT}`",
    f"- `{SIZE_CHART_OUT}`",
    f"- `{BODY_HTML_OUT}`",
    f"- `{VERIFY_JSON_OUT}`",
    f"- `{UPLOAD_DIR}`",
    "",
    "## Manual Follow-ups",
    "- Inventory quantities and per-variant weights still need operator stock values.",
    "- Re-check exact fiber composition if the vendor page becomes directly readable later.",
]
LISTING_MD.write_text("\n".join(lines) + "\n")

print(json.dumps({
    "product_id": product_id,
    "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    "live_url": product["onlineStoreUrl"],
    "variants": len(live_variants),
    "checks": checks,
    "listing": str(LISTING_MD),
    "csv": str(CSV_OUT),
}, indent=2))
PYRUN
