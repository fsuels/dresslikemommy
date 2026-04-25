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

HANDLE = "ocean-marble-family-matching-set"
TITLE = "Ocean Marble Family Matching Set - Dress & Shirt Set"
SEO_TITLE = "Ocean Marble Family Matching Set | Dress Like Mommy"
SEO_DESCRIPTION = "Blue watercolor family matching set for mom, dad, girls & boys. Dress and shirt+shorts sizes 1-2Y to 10Y, Mom S-L, Dad S-3XL."
VENDOR_URL = "https://detail.1688.com/offer/1043342779774.html"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Outfit Sets"
SHORTCODE = "OMRB"
COLOR_TOKEN = "BLUE"
COLOR_NAME = "Blue"
CHILD_PRICE = "31.99"
ADULT_PRICE = "36.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-omrb-ocean-marble-family-matching-set.sh"
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


def kg_from_jin(text):
    lo, hi = [float(x) for x in re.split(r"[-–]", text)]
    return f"{lo / 2:g}-{hi / 2:g} kg"


SIZE_TOKEN = {
    "Child 2 Years": "KID2Y",
    "Child 1-2 Years": "KID12Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
    "Mother L": "L",
    "Father S": "S",
    "Father M": "M",
    "Father L": "L",
    "Father XL": "XL",
    "Father 2XL": "2XL",
    "Father 3XL": "3XL",
}

SIZE_METAOBJECT_MAP = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 1-2 Years": ("gid://shopify/Metaobject/129972797537", "12-18 months"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}

ROLE_TOKEN = {
    "Girl Dress": "GRL",
    "Mother Dress": "MOM",
    "Boy Shirt + Shorts": "BOY",
    "Father Shirt + Shorts": "DAD",
}

chart = []


def add_dress(audience, role, vendor_label, picker_label, age, weight, height, skirt_cm, half_bust_cm):
    chest_cm = half_bust_cm * 2
    hip_cm = chest_cm + 4 if audience == "child" else chest_cm + 6
    waist_cm = chest_cm if audience == "child" else hip_cm - 8
    chart.append({
        "audience": audience,
        "role": role,
        "garment": "Dress",
        "vendor_label": vendor_label,
        "picker_label": picker_label,
        "sku_suffix": SIZE_TOKEN[picker_label],
        "age": age,
        "weight": weight,
        "height": height,
        "chest_cm": chest_cm,
        "hip_cm": hip_cm,
        "waist_cm": waist_cm,
        "length_cm": skirt_cm,
        "sleeve_cm": 0,
        "skirt_cm": skirt_cm,
        "pant_cm": 0,
        "shoulder_cm": 0,
    })


def add_set(audience, role, vendor_label, picker_label, age, weight, height, shirt_len_cm, half_bust_cm, shoulder_cm, shorts_len_cm, waist_cm):
    chest_cm = half_bust_cm * 2
    hip_cm = chest_cm
    chart.append({
        "audience": audience,
        "role": role,
        "garment": "Shirt + Shorts",
        "vendor_label": vendor_label,
        "picker_label": picker_label,
        "sku_suffix": SIZE_TOKEN[picker_label],
        "age": age,
        "weight": weight,
        "height": height,
        "chest_cm": chest_cm,
        "hip_cm": hip_cm,
        "waist_cm": waist_cm,
        "length_cm": shirt_len_cm,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": shorts_len_cm,
        "shoulder_cm": shoulder_cm,
    })


child_base = [
    ("80", "Child 1-2 Years", "1-2", kg_from_jin("18-23"), "75-85 cm"),
    ("90", "Child 2 Years", "2", kg_from_jin("24-29"), "86-95 cm"),
    ("100", "Child 3 Years", "3", kg_from_jin("30-35"), "96-105 cm"),
    ("110", "Child 4 Years", "4", kg_from_jin("36-40"), "106-115 cm"),
    ("120", "Child 5 Years", "5", kg_from_jin("41-45"), "116-125 cm"),
    ("130", "Child 6-7 Years", "6-7", kg_from_jin("46-50"), "126-135 cm"),
    ("140", "Child 8 Years", "8", kg_from_jin("51-60"), "136-145 cm"),
]

for base, measurements in zip(child_base, [(53, 26), (59, 28), (65, 30), (71, 32), (77, 34), (83, 36), (89, 38)]):
    add_dress("child", "Girl Dress", *base, *measurements)

add_dress("child", "Girl Dress", "150", "Child 9-10 Years", "9-10", kg_from_jin("61-80"), "145-155 cm", 95, 39)

for row in [
    ("S", "Mother S", kg_from_jin("95-115"), "-", 106, 41),
    ("M", "Mother M", kg_from_jin("116-125"), "-", 107, 43),
    ("L", "Mother L", kg_from_jin("126-139"), "-", 108, 45),
]:
    vendor_label, picker_label, weight, height, skirt, half_bust = row
    add_dress("mother", "Mother Dress", vendor_label, picker_label, "-", weight, height, skirt, half_bust)

shirt_rows = [
    ("80", "Child 1-2 Years", "1-2", kg_from_jin("18-23"), "75-85 cm", 34, 36, 34, 29, 38),
    ("90", "Child 2 Years", "2", kg_from_jin("24-29"), "86-95 cm", 37, 38, 36, 32, 40),
    ("100", "Child 3 Years", "3", kg_from_jin("30-35"), "96-105 cm", 40, 40, 38, 35, 42),
    ("110", "Child 4 Years", "4", kg_from_jin("36-40"), "106-115 cm", 43, 42, 40, 38, 44),
    ("120", "Child 5 Years", "5", kg_from_jin("41-45"), "116-125 cm", 46, 44, 41, 41, 45),
    ("130", "Child 6-7 Years", "6-7", kg_from_jin("46-50"), "126-135 cm", 49, 46, 43, 44, 48),
    ("140", "Child 8 Years", "8", kg_from_jin("51-60"), "136-145 cm", 52, 48, 45, 47, 50),
    ("150", "Child 9-10 Years", "9-10", kg_from_jin("61-80"), "145-155 cm", 55, 50, 47, 50, 52),
]
for row in shirt_rows:
    add_set("child", "Boy Shirt + Shorts", *row)

for row in [
    ("S", "Father S", kg_from_jin("95-115"), "-", 66, 59, 52, 56, 54),
    ("M", "Father M", kg_from_jin("116-125"), "-", 68, 61, 53, 57, 56),
    ("L", "Father L", kg_from_jin("126-139"), "-", 70, 63, 55, 58, 58),
    ("XL", "Father XL", kg_from_jin("140-155"), "-", 72, 65, 57, 59, 60),
    ("XXL", "Father 2XL", kg_from_jin("156-170"), "-", 74, 68, 59, 60, 62),
    ("3XL", "Father 3XL", kg_from_jin("171-190"), "-", 77, 71, 61, 61, 64),
]:
    vendor_label, picker_label, weight, height, shirt_len, half_bust, shoulder, shorts_len, waist = row
    add_set("father", "Father Shirt + Shorts", vendor_label, picker_label, "-", weight, height, shirt_len, half_bust, shoulder, shorts_len, waist)


def sku(row):
    return f"DLM-{SHORTCODE}-{ROLE_TOKEN[row['role']]}-{row['sku_suffix']}-{COLOR_TOKEN}"


def num(value):
    if value in (0, "0", None, ""):
        return None
    value = float(value)
    return str(int(value)) if value.is_integer() else f"{value:.1f}".rstrip("0").rstrip(".")


def cm_in(value):
    if not value:
        return "-"
    return f"{num(value)} cm / {num(float(value) / 2.54)} in"


def dual_range(text, unit, factor, out_unit):
    if text in ["-", "--"]:
        return "-"
    match = re.match(r"([\d.]+)-([\d.]+) " + unit, text)
    if not match:
        return html.escape(text)
    lo, hi = map(float, match.groups())
    return f"{num(lo)}-{num(hi)} {unit} / {num(lo * factor)}-{num(hi * factor)} {out_unit}"


def esc(value):
    return html.escape(str(value))


def table(rows, garment):
    measure_header = "Skirt Length (cm/in)" if garment == "Dress" else "Sleeve or - (cm/in)"
    body_rows = []
    for row in rows:
        values = [
            esc(row["picker_label"]),
            esc(row["age"] if row["age"] != "-" else "-"),
            esc(dual_range(row["weight"], "kg", 2.20462, "lbs")),
            esc(dual_range(row["height"], "cm", 1 / 2.54, "in")),
            cm_in(row["chest_cm"]),
            cm_in(row["skirt_cm"] if garment == "Dress" else row["sleeve_cm"]),
            cm_in(row["pant_cm"]),
            cm_in(row["hip_cm"]),
            cm_in(row["waist_cm"]),
            cm_in(row["length_cm"]),
        ]
        body_rows.append("<tr>" + "".join(f"<td>{v}</td>" for v in values) + "</tr>")
    return (
        f"<h3>Size Chart - {garment}</h3>\n"
        f"<table id=\"size-chart-{garment.lower().replace(' + ', '-').replace(' ', '-')}\">"
        "<thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        f"<th>Chest/Bust (cm/in)</th><th>{measure_header}</th><th>Pant/Short or - (cm/in)</th>"
        "<th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody>"
        + "\n".join(body_rows)
        + "</tbody></table>"
    )


body_html = "\n".join([
    "<ul>",
    "<li><strong>Fabric:</strong> Lightweight summer woven fabric; exact fiber content was not visible from the vendor page.</li>",
    "<li><strong>Family story:</strong> A coordinated beach-ready look for moms, dads, girls, and boys.</li>",
    "<li><strong>Print:</strong> Blue watercolor marble with soft white space and small golden accent strokes.</li>",
    "<li><strong>Design details:</strong> Girls and moms wear the sleeveless dress; boys and dads wear the matching short-sleeve shirt with white shorts.</li>",
    "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>",
    "<li><strong>Size range:</strong> Child 1-2 Years through Child 9-10 Years, Mother S-L, and Father S-3XL.</li>",
    "</ul>",
    table([r for r in chart if r["garment"] == "Dress"], "Dress"),
    table([r for r in chart if r["garment"] == "Shirt + Shorts"], "Shirt + Shorts"),
    "<p>Ocean Marble is made for sunny family photos, resort days, and beach walks where everyone coordinates without feeling overly formal. The blue watercolor print ties the dresses and shirt sets together while the white shorts keep the boys' and dads' look crisp.</p>",
    "<p>Select Dress for moms and girls or Shirt + Shorts for dads and boys, then choose each role-bearing size from the chart-backed picker. Shoes, sunglasses, hats, bags, and other accessories shown in photos are styling only.</p>",
    "<h3>Key Features:</h3>",
    "<ul>",
    "<li><strong>Two outfit types:</strong> Dress for girls and moms, shirt + shorts set for boys and dads.</li>",
    "<li><strong>Blue watercolor print:</strong> Soft ocean-inspired pattern with golden accent details.</li>",
    "<li><strong>Four-role matching:</strong> Built for mom, dad, girls, and boys in one family listing.</li>",
    "<li><strong>Warm-weather styling:</strong> Sleeveless dresses and short-sleeve shirt sets are easy for vacation photos.</li>",
    "<li><strong>Chart-backed variants:</strong> Every size option is backed by the attached vendor chart.</li>",
    "</ul>",
    "<p>Choose each family member's type and size to create a polished matching look for your next beach day or summer memory.</p>",
])

BODY_HTML_OUT.write_text(body_html)
SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2))

variants = []
recap = []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    variants.append({
        "price": price,
        "compareAtPrice": compare,
        "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": sku(row), "tracked": True, "requiresShipping": True},
        "optionValues": [
            {"optionName": "Type", "name": row["garment"]},
            {"optionName": "Size", "name": row["picker_label"]},
        ],
    })
    size_gid, catalog_label = SIZE_METAOBJECT_MAP[row["picker_label"]]
    recap.append({**row, "sku": sku(row), "price": price, "compare": compare, "size_gid": size_gid, "catalog_label": catalog_label})

size_values = []
for row in chart:
    if row["picker_label"] not in size_values:
        size_values.append(row["picker_label"])

product_options = [
    {"name": "Type", "values": [{"name": "Dress"}, {"name": "Shirt + Shorts"}]},
    {"name": "Size", "values": [{"name": value} for value in size_values]},
]

tags = sorted(set([
    "Family Matching",
    "Mommy and Me",
    "Daddy and Me",
    "Matching Family Set",
    "Matching Family Outfits",
    "Matching Family Dress",
    "Matching Family Shirt",
    "Matching Shirt and Shorts",
    "Dress & Shirt Set",
    "Sets",
    "Summer",
    "Beach",
    "Vacation",
    "Resort",
    "Watercolor",
    "Marble",
    "Ocean",
    "Blue",
    "White",
    "Gold",
    "Ocean Marble",
    "Girls Dress",
    "Mother Dress",
    "Boy Shirt",
    "Boy Shorts",
    "Father Shirt",
    "Father Shorts",
    "Short Sleeve Shirt",
    "Sleeveless Dress",
    "Four-Role Matching",
    VENDOR_URL,
] + size_values + ["Mother S", "Mother M", "Mother L", "Father S", "Father M", "Father L", "Father XL", "Father 2XL", "Father 3XL"]))


def gql(query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(API, data=data, headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read())
    if result.get("errors"):
        raise SystemExit(result["errors"])
    return result


def user_errors(result, path):
    cursor = result
    for part in path.split("."):
        if part:
            cursor = cursor.get(part, {})
    if cursor:
        raise SystemExit(cursor)


def assert_preflight():
    assert len(chart) == 25, len(chart)
    assert len(variants) == len(chart), (len(variants), len(chart))
    assert len(TITLE) <= 70
    assert len(SEO_TITLE) <= 60
    assert len(SEO_DESCRIPTION) <= 155
    role_picker = [(row["role"], row["picker_label"], row["vendor_label"]) for row in chart]
    assert len(role_picker) == len(set(role_picker))
    variant_keys = [(value["name"], value["name"]) for variant in variants for value in variant["optionValues"][:1]]
    assert variant_keys
    assert all(row.get("waist_cm") for row in chart)
    assert all(row["role"] in ROLE_TOKEN for row in chart)
    assert all(row["picker_label"] in SIZE_METAOBJECT_MAP for row in chart)
    for variant in variants:
        expected = CHILD_PRICE if "-KID" in variant["inventoryItem"]["sku"] else ADULT_PRICE
        assert variant["price"] == expected


assert_preflight()

node = gql("query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName}}}", {"id": TAXONOMY_GID})["data"]["node"]
assert node["fullName"] == EXPECTED_TAXONOMY, node

existing = gql("query($handle:String!){productByHandle(handle:$handle){id variants(first:100){nodes{id sku}}}}", {"handle": HANDLE})["data"]["productByHandle"]
product_input = {
    "handle": HANDLE,
    "title": TITLE,
    "descriptionHtml": body_html,
    "vendor": "dresslikemommy.com",
    "productType": PRODUCT_TYPE,
    "tags": tags,
    "status": "ACTIVE",
    "category": TAXONOMY_GID,
    "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
}

if existing:
    product_id = existing["id"]
    result = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id} userErrors{field message}}}", {"product": {"id": product_id, **product_input}})
    user_errors(result, "data.productUpdate.userErrors")
    live_skus = sorted([variant["sku"] for variant in existing["variants"]["nodes"] if variant.get("sku")])
    spec_skus = sorted([variant["inventoryItem"]["sku"] for variant in variants])
    if live_skus and live_skus != spec_skus:
        raise SystemExit(f"Existing product has unexpected SKUs; refusing destructive variant replacement: {live_skus}")
    if live_skus == spec_skus:
        by_sku = {variant["sku"]: variant["id"] for variant in existing["variants"]["nodes"]}
        updates = [{
            "id": by_sku[variant["inventoryItem"]["sku"]],
            "price": variant["price"],
            "compareAtPrice": variant["compareAtPrice"],
            "inventoryPolicy": "DENY",
            "optionValues": variant["optionValues"],
        } for variant in variants]
        result = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$productId,variants:$variants){userErrors{field message}}}", {"productId": product_id, "variants": updates})
        user_errors(result, "data.productVariantsBulkUpdate.userErrors")
    else:
        result = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
        user_errors(result, "data.productVariantsBulkCreate.userErrors")
else:
    result = gql("mutation($input:ProductInput!){productCreate(input:$input){product{id} userErrors{field message}}}", {"input": {**product_input, "productOptions": product_options}})
    user_errors(result, "data.productCreate.userErrors")
    product_id = result["data"]["productCreate"]["product"]["id"]
    result = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
    user_errors(result, "data.productVariantsBulkCreate.userErrors")

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Blue Watercolor Marble"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Ocean Marble"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Shirt Set"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69639733345"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(list(dict.fromkeys(SIZE_METAOBJECT_MAP[row["picker_label"]][0] for row in chart)))},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
]
for offset in range(0, len(metafields), 25):
    result = gql("mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){userErrors{field message}}}", {"metafields": metafields[offset:offset + 25]})
    user_errors(result, "data.metafieldsSet.userErrors")

publications = [{"publicationId": value} for value in [
    "gid://shopify/Publication/55169925",
    "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225",
    "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
]]
result = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id status} userErrors{field message}}}", {"product": {"id": product_id, "status": "ACTIVE"}})
user_errors(result, "data.productUpdate.userErrors")
result = gql("mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}", {"id": product_id, "input": publications})
user_errors(result, "data.publishablePublish.userErrors")

media = gql("query($id:ID!){product(id:$id){media(first:50){nodes{... on MediaImage{id alt image{url}}}}}}", {"id": product_id})["data"]["product"]["media"]["nodes"]
existing_alts = {item.get("alt") for item in media}
for image_path in sorted(list(UPLOAD_DIR.glob("*.png")) + list(UPLOAD_DIR.glob("*.jpg")) + list(UPLOAD_DIR.glob("*.jpeg")) + list(UPLOAD_DIR.glob("*.webp"))):
    alt = "Family wearing Ocean Marble blue watercolor matching dress and shirt set." if image_path.name.startswith("01") else "Ocean Marble blue watercolor boys shirt and white shorts set."
    if alt in existing_alts:
        continue
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    result = gql("mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}", {"input": [{"filename": image_path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]})
    user_errors(result, "data.stagedUploadsCreate.userErrors")
    target = result["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    args = ["curl", "-sS", "-X", "POST", target["url"]]
    for parameter in target["parameters"]:
        args += ["-F", f"{parameter['name']}={parameter['value']}"]
    args += ["-F", f"file=@{image_path}"]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    result = gql("mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){userErrors{field message}}}", {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})
    user_errors(result, "data.productCreateMedia.userErrors")

time.sleep(3)
verify = gql("query($id:ID!){product(id:$id){id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}} collections(first:50){nodes{title handle}} metafields(first:100){nodes{namespace key type value}} media(first:20){nodes{... on MediaImage{id alt image{url}}}} resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}}}}", {"id": product_id})
VERIFY_JSON_OUT.write_text(json.dumps(verify, indent=2))
p = verify["data"]["product"]
live_variants = p["variants"]["nodes"]
live_skus = sorted(variant["sku"] for variant in live_variants)
spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
checks = [
    ("title length", len(p["title"]) <= 70, len(p["title"])),
    ("seo title length", len(p["seo"]["title"]) <= 60, len(p["seo"]["title"])),
    ("seo description length", len(p["seo"]["description"]) <= 155, len(p["seo"]["description"])),
    ("variant count", len(live_variants) == len(variants), f"{len(live_variants)} vs {len(variants)}"),
    ("sku parity", live_skus == spec_skus, ", ".join(live_skus)),
    ("taxonomy", p["category"]["fullName"] == EXPECTED_TAXONOMY, p["category"]["fullName"]),
    ("status active", p["status"] == "ACTIVE", p["status"]),
    ("published", bool(p["publishedAt"]), p["publishedAt"]),
    ("online url", bool(p["onlineStoreUrl"]), p["onlineStoreUrl"]),
    ("media count", len(p["media"]["nodes"]) >= 2, len(p["media"]["nodes"])),
]
expected_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
price_ok = all(
    variant["price"] == expected_by_sku[variant["sku"]]["price"]
    and variant["compareAtPrice"] == expected_by_sku[variant["sku"]]["compareAtPrice"]
    and variant["inventoryPolicy"] == "DENY"
    and variant["inventoryItem"]["tracked"]
    and variant["inventoryItem"]["requiresShipping"]
    for variant in live_variants
)
checks.append(("price/inventory parity", price_ok, "FORCE_SPEC_PRICES true"))
if not all(check[1] for check in checks):
    raise SystemExit("verification failed " + repr(checks))

with CSV_HEADER_SOURCE.open(newline="") as fh:
    header = next(csv.reader(fh))
rows = []
for item in recap:
    row = {column: "" for column in header}
    values = {
        "Handle": HANDLE,
        "Title": TITLE,
        "Body (HTML)": body_html,
        "Vendor": "dresslikemommy.com",
        "Product Category": EXPECTED_TAXONOMY,
        "Type": PRODUCT_TYPE,
        "Tags": ", ".join(p["tags"]),
        "Published": "TRUE",
        "Option1 Name": "Type",
        "Option1 Value": item["garment"],
        "Option2 Name": "Size",
        "Option2 Value": item["picker_label"],
        "Variant SKU": item["sku"],
        "Variant Grams": "0",
        "Variant Inventory Tracker": "shopify",
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": item["price"],
        "Variant Compare At Price": item["compare"],
        "Variant Requires Shipping": "TRUE",
        "Variant Taxable": "TRUE",
        "SEO Title": SEO_TITLE,
        "SEO Description": SEO_DESCRIPTION,
        "Google Shopping / Gender": "unisex",
        "Google Shopping / Age Group": "adult",
        "Google Shopping / Condition": "new",
        "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "Family Matching",
        "Google Shopping / Custom Label 1": "Ocean Marble",
        "Google Shopping / Custom Label 2": "Summer",
        "Google Shopping / Custom Label 3": "Dress & Shirt Set",
        "Google Shopping / Custom Label 4": "Four-Role Matching",
        "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": "Blue Watercolor Marble",
        "Style (product.metafields.custom.style)": "Matching Family Set",
        "SubCategory (product.metafields.custom.subcategory)": "Set",
        "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set",
        "Type (product.metafields.custom.type)": "Two-Piece Set",
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": COLOR_NAME,
        "Size (product.metafields.shopify.size)": ", ".join(size_values),
        "Status": "active",
    }
    for key, value in values.items():
        if key in row:
            row[key] = value
    rows.append(row)
with CSV_OUT.open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

written = sorted([f"{m['namespace']}.{m['key']}" for m in p["metafields"]["nodes"] if m["namespace"] in ["custom", "mm-google-shopping", "shopify", "global"]])
skipped = {
    "shopify.fabric": "Vendor page was not reliable enough to confirm exact fiber composition.",
    "shopify.dress-occasion": "Mixed outfit-set taxonomy; dress-only occasion would overstate the product.",
    "shopify.dress-style": "Mixed dress and shirt+shorts product under Outfit Sets.",
    "shopify.neckline": "Dress and shirt set do not share one honest product-level neckline.",
    "shopify.skirt-dress-length-type": "Mixed product under Outfit Sets, not dress-only taxonomy.",
    "shopify.sleeve-length-type": "Dress is sleeveless while the shirt set is short sleeved; one product-level value would be misleading.",
    "shopify.top-length-type": "Mixed dresses and shirt+shorts sets; no single top-length value is honest.",
}

lines = [
    f"# {TITLE}",
    "",
    "## Links",
    f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    f"- **Live:** {p['onlineStoreUrl']}",
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
    "| PRIMARY_CATEGORY | Sets (Shopify taxonomy: Outfit Sets) |",
    "| DESIGNS_TO_LIST | Dress, Shirt + Shorts |",
    "| FORCE_SPEC_PRICES | true |",
    f"| SHORTCODE | auto -> `{SHORTCODE}` |",
    f"| COLOR_TOKEN | auto -> `{COLOR_TOKEN}` |",
    "",
    "## Vendor fetch status",
    "A direct fetch of the 1688 page returned Alibaba anti-bot/punish markup, so the attached size chart image was used as the authoritative source of truth. The vendor page was not used for customer-facing claims beyond the supplied product imagery and chart evidence.",
    "",
    "## Option axes",
    "- Option 1: Type -> Dress, Shirt + Shorts",
    "- Option 2: Size -> role-bearing size labels",
    "- Color is a single blue watercolor print and is encoded in SKU/tag/metafields, not exposed as a one-value option.",
    f"- Variants live: {len(live_variants)} ({len(chart)} SIZE_CHART rows)",
    "",
    "## SIZE_CHART / Variant Recap",
    "| Role | Vendor | Picker | Type | SKU | Price | shopify.size GID |",
    "|---|---|---|---|---|---|---|",
]
for item in recap:
    lines.append(f"| {item['role']} | {item['vendor_label']} | {item['picker_label']} | {item['garment']} | `{item['sku']}` | {item['price']} | `{item['size_gid']}` ({item['catalog_label']}) |")
lines += [
    "",
    "## Derivations",
    "- Vendor weights were listed in `jin` and converted to kg in the saved SIZE_CHART and shopper-facing table.",
    "- The vendor `80` child row was mapped to `Child 1-2 Years`; its `shopify.size` reference uses the closest honest catalog size metaobject `12-18 months` because the store has no exact `1-2 years` size metaobject.",
    "- Dress chest used the chart's half-bust column doubled to full circumference.",
    "- Shirt chest used the chart's half-bust column doubled to full circumference.",
    "- Dress hip and waist were derived where the vendor omitted them: child hip = chest + 4, child waist = chest; adult dress hip = bust + 6, waist = hip - 8.",
    "- Shirt + shorts hip was derived from shirt chest because the shorts chart omits hip; waist and short length come directly from the shorts table.",
    "- Hats, sunglasses, bags, jewelry, sandals, and other accessories are styling only and excluded from variants.",
    "",
    "## Verification",
    "| Check | Result | Detail |",
    "|---|---|---|",
]
for name, ok, detail in checks:
    lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines += [
    "",
    "## Metafields Written",
    *[f"- `{item}`" for item in written],
    "",
    "## Metafields Skipped",
    *[f"- `{key}`: {value}" for key, value in skipped.items()],
    "",
    "## Smart Collections",
    ", ".join(sorted(collection["handle"] for collection in p["collections"]["nodes"])) or "Pending smart collection propagation.",
    "",
    "## Publications",
    ", ".join(sorted(node["publication"]["name"] for node in p["resourcePublicationsV2"]["nodes"] if node["isPublished"])),
    "",
    "## Saved Files",
    f"- `{SCRIPT_PATH}`",
    f"- `{LISTING_MD}`",
    f"- `{CSV_OUT}`",
    f"- `{SIZE_CHART_OUT}`",
    f"- `{BODY_HTML_OUT}`",
    f"- `{VERIFY_JSON_OUT}`",
    f"- `{ROOT / 'ops/listings/source-ocean-marble-family-matching-set-size-chart.png'}`",
    f"- `{UPLOAD_DIR}`",
    "",
    "## Manual Follow-ups",
    "- Inventory quantities and per-variant package weights still need operator stock values.",
    "- Re-check exact fabric composition if the vendor page becomes directly readable later; `shopify.fabric` is intentionally skipped rather than guessed.",
]
LISTING_MD.write_text("\n".join(lines) + "\n")

print(json.dumps({
    "product_id": product_id,
    "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    "live_url": p["onlineStoreUrl"],
    "variants": len(live_variants),
    "checks": checks,
    "listing": str(LISTING_MD),
    "csv": str(CSV_OUT),
}, indent=2))
PYRUN
