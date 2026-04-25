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
import csv, html, json, math, mimetypes, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]
HANDLE = "ocean-dot-family-matching-set"
TITLE = "Ocean Dot Family Matching Set - Dress, Top, Shirt & Shorts"
SEO_TITLE = "Ocean Dot Family Matching Set | Dress Like Mommy"
SEO_DESCRIPTION = "Ocean-blue dot family matching pieces for mom, dad, girls & boys. Dress, top, shirt, and shorts sizes 2Y-10Y, Mother S-3XL, Father S-4XL."
VENDOR_URL = "https://detail.1688.com/offer/1027490923984.html?"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Outfit Sets"
SHORTCODE = "ODOT"
COLOR_NAME = "Ocean Blue"
COLOR_TOKEN = "BLUE"
CHILD_PRICE = "26.99"
ADULT_PRICE = "29.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-odot-ocean-dot-family-matching-set.sh"
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

size_tokens = {
    "Child 2 Years": "KID2Y", "Child 3 Years": "KID3Y", "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y", "Child 6-7 Years": "KID67Y", "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y", "Mother S": "S", "Mother M": "M", "Mother L": "L",
    "Mother XL": "XL", "Mother 2XL": "2XL", "Mother 3XL": "3XL", "Father S": "S",
    "Father M": "M", "Father L": "L", "Father XL": "XL", "Father 2XL": "2XL",
    "Father 3XL": "3XL", "Father 4XL": "4XL",
}
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

chart = []
def add(audience, role, garment, vendor, picker, age, weight, height, chest, length, shoulder=0, sleeve=0, pant=0, waist=0, hip=0, source_note=""):
    if not hip:
        if garment == "Shorts" and waist:
            hip = waist + 14
        elif audience == "child":
            hip = chest + 4 if chest else 0
        else:
            hip = chest if chest else 0
    if not waist:
        if garment in ("Dress", "Top"):
            waist = chest if audience == "child" else max(chest - 12, 0)
        elif garment == "Shirt":
            waist = chest if audience == "child" else max(chest - 12, 0)
        elif garment == "Shorts" and hip:
            waist = max(hip - 14, 0)
    chart.append({
        "audience": audience, "role": role, "garment": garment, "vendor_label": vendor,
        "picker_label": picker, "sku_suffix": size_tokens[picker], "age": age, "weight": weight,
        "height": height, "chest_cm": chest, "hip_cm": hip, "waist_cm": waist, "length_cm": length,
        "shoulder_cm": shoulder, "sleeve_cm": sleeve, "skirt_cm": 0, "pant_cm": pant,
        "source_note": source_note,
    })

child_rows = [
    ("90", "Child 2 Years", "2", "85-95 cm"), ("100", "Child 3 Years", "3", "95-105 cm"),
    ("110", "Child 4 Years", "4", "106-115 cm"), ("120", "Child 5 Years", "5", "116-125 cm"),
    ("130", "Child 6-7 Years", "6-7", "126-135 cm"), ("140", "Child 8 Years", "8", "136-143 cm"),
    ("150", "Child 9-10 Years", "9-10", "143-152 cm"),
]
boy_rows = [(42,80,39,34,40),(45,86,40,36,43),(48,90,41,38,46),(51,94,42,40,49),(54,98,43,42,52),(58,102,44,44,55),(62,106,45,46,58)]
girl_dress_rows = [(59,72),(62,76),(64,80),(67,84),(71,88),(74,92),(78,96)]
for (vendor, picker, age, height), (length, chest, shoulder, pant, waist) in zip(child_rows, boy_rows):
    add("child", "Boy Shirt", "Shirt", vendor, picker, age, "—", height, chest, length, shoulder=shoulder, waist=waist, source_note="Vendor boy table omits sleeve and hip/seat values.")
    add("child", "Boy Shorts", "Shorts", vendor, picker, age, "—", height, 0, pant, pant=pant, waist=waist, source_note="Shorts row derived from the vendor boy set pant/waist columns; hip/seat omitted by vendor.")
for (vendor, picker, age, height), (length, chest) in zip(child_rows, girl_dress_rows):
    add("child", "Girl Dress", "Dress", vendor, picker, age, "—", height, chest, length, source_note="Vendor girl table labels length/chest only; treated as a sleeveless dress from the girl image and skirt-length chart label.")

mother_rows = [
    ("S", "Mother S", "37.5-45 kg", 109, 92), ("M", "Mother M", "45.5-52.5 kg", 110, 96),
    ("L", "Mother L", "53-60 kg", 112, 100), ("XL", "Mother XL", "60.5-67.5 kg", 114, 104),
    ("XXL", "Mother 2XL", "68-72.5 kg", 115, 108), ("3XL定制", "Mother 3XL", "73-80 kg", 115, 108),
]
for vendor, picker, weight, length, chest in mother_rows:
    add("mother", "Mother Top", "Top", vendor, picker, "—", weight, "—", chest, length, source_note="Vendor women's table omits waist/hip; 3XL is marked custom in source.")

father_rows = [
    ("S", "Father S", "40-49 kg", 67,104,46,19,46,54), ("M", "Father M", "49-57.5 kg", 69,108,47,20,48,56),
    ("L", "Father L", "58-65 kg", 71,112,48,21,49,58), ("XL", "Father XL", "65.5-72.5 kg", 73,116,49,22,51,62),
    ("XXL", "Father 2XL", "73-80 kg", 75,120,50,23,52,66), ("3XL", "Father 3XL", "82.5-90 kg", 77,124,51,24,54,70),
    ("4XL", "Father 4XL", "90-110 kg", 79,128,52,24,56,74),
]
for vendor, picker, weight, length, chest, shoulder, sleeve, pant, waist in father_rows:
    add("father", "Father Shirt", "Shirt", vendor, picker, "—", weight, "—", chest, length, shoulder=shoulder, sleeve=sleeve, waist=waist, source_note="Vendor father table omits hip/seat values.")
    add("father", "Father Shorts", "Shorts", vendor, picker, "—", weight, "—", 0, pant, pant=pant, waist=waist, source_note="Shorts row derived from the vendor men table pant/waist columns; hip/seat omitted by vendor.")

required = ["audience","role","garment","vendor_label","picker_label","sku_suffix","age","weight","height","chest_cm","hip_cm","waist_cm","length_cm","sleeve_cm","skirt_cm","pant_cm"]
for row in chart:
    missing = [key for key in required if key not in row]
    if missing:
        raise SystemExit(f"missing fields for {row}: {missing}")
    if row["picker_label"] not in size_map:
        raise SystemExit(f"missing size GID for {row['picker_label']}")

role_tokens = {"Girl Dress": "GRL", "Mother Top": "MOM", "Boy Shirt": "BOY", "Boy Shorts": "BOY", "Father Shirt": "DAD", "Father Shorts": "DAD"}
def sku(row):
    type_token = {"Dress": "DRS", "Top": "TOP", "Shirt": "SHRT", "Shorts": "SHRTS"}[row["garment"]]
    return f"DLM-{SHORTCODE}-{role_tokens[row['role']]}-{type_token}-{row['sku_suffix']}-{COLOR_TOKEN}"

def num(value):
    try:
        f = float(value)
        return str(int(f)) if f.is_integer() else f"{f:g}"
    except Exception:
        return str(value)

def cm_in(value):
    if not value:
        return "—"
    return f"{num(value)} cm / {num(float(value) / 2.54)} in"

def range_convert(text, unit, multiplier, out_unit):
    if text in ("—", "-", ""):
        return "—"
    match = re.match(r"([\d.]+)-([\d.]+) " + re.escape(unit), text)
    if not match:
        return html.escape(text)
    low, high = map(float, match.groups())
    return f"{num(low)}-{num(high)} {unit} / {num(low * multiplier)}-{num(high * multiplier)} {out_unit}"

def table(rows, garment):
    measure_header = "Sleeve or Skirt (cm/in)"
    body_rows = []
    for row in rows:
        body_rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in [
            html.escape(row["picker_label"]), html.escape(row["age"]), range_convert(row["weight"], "kg", 2.20462, "lbs"),
            range_convert(row["height"], "cm", 1 / 2.54, "in"), cm_in(row["chest_cm"]),
            cm_in(row["sleeve_cm"] if garment == "Shirt" else 0), cm_in(row["pant_cm"]),
            cm_in(row["hip_cm"]), cm_in(row["waist_cm"]), cm_in(row["length_cm"]),
        ]) + "</tr>")
    return (
        f"<h3>Size Chart - {garment}</h3>\n"
        f"<table id=\"size-chart-{garment.lower()}\"><thead><tr>"
        "<th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        f"<th>Chest/Bust (cm/in)</th><th>{measure_header}</th><th>Pant/Short or — (cm/in)</th>"
        "<th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th>"
        "</tr></thead><tbody>\n" + "\n".join(body_rows) + "\n</tbody></table>"
    )

body = "\n".join([
    "<ul>",
    "<li><strong>Fabric:</strong> Lightweight soft woven blue-dot fabric; exact fiber content was not visible from the blocked vendor page.</li>",
    "<li><strong>Family story:</strong> A clean family matching look for moms, dads, girls, and boys in ocean-blue polka dots.</li>",
    "<li><strong>Print:</strong> Ocean-blue polka dots styled with white bottoms in the supplied imagery.</li>",
    "<li><strong>Design details:</strong> Girls wear the sleeveless dress, moms wear the sleeveless top, and boys and dads wear the short-sleeve shirt or matching shorts. Hats, jewelry, bags, sunglasses, and shoes are styling only.</li>",
    "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and steam or cool iron inside-out if needed.</li>",
    "<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S-3XL, and Father S-4XL.</li>",
    "</ul>",
    table([row for row in chart if row["garment"] == "Dress"], "Dress"),
    table([row for row in chart if row["garment"] == "Top"], "Top"),
    table([row for row in chart if row["garment"] == "Shirt"], "Shirt"),
    table([row for row in chart if row["garment"] == "Shorts"], "Shorts"),
    "<h3>Fit Guide</h3>",
    "<p>Kids sizes are based on the child's actual height: 90cm is about ages 1-2, 100cm about ages 2-3, 110cm about ages 4-5, 120cm about ages 5-6, 130cm about ages 7-8, 140cm about ages 9-10, and 150cm about ages 11-12. Adult sizing follows typical 1688 Asian sizing and tends to run small, so we recommend sizing up one from your usual US/EU size.</p>",
    "<p>Adult fit estimate: S fits about 155-160cm / 45-50kg, M fits 160-165cm / 50-55kg, L fits 165-170cm / 55-62kg, XL fits 170-175cm / 62-70kg, 2XL fits 175-178cm / 70-78kg, 3XL fits 178-182cm / 78-88kg, and 4XL fits 180-185cm / 88-95kg where that adult size is available.</p>",
    "<p>Ocean Dot keeps family dressing relaxed and bright, with separates that look polished for vacation photos, resort dinners, and sunny weekends. The dress and top options are chart-backed for girls and moms, while shirts and shorts are chart-backed for boys and dads.</p>",
    "<p>Choose the Type and Size for each family member to build the exact matching look you need. Every live variant is backed by the attached vendor size chart, and styling-only accessories are intentionally excluded.</p>",
    "<h3>Key Features:</h3>",
    "<ul>",
    "<li><strong>Four garment options:</strong> Dress, Top, Shirt, and Shorts in one coordinated family listing.</li>",
    "<li><strong>Ocean-blue dot palette:</strong> Easy to style for beach, cruise, and warm-weather family photos.</li>",
    "<li><strong>Role-bearing sizing:</strong> Size labels clearly separate child, mother, and father rows.</li>",
    "<li><strong>Chart-backed variants:</strong> Only size rows visible in the supplied chart were created.</li>",
    "<li><strong>Lightweight feel:</strong> Soft woven texture gives the pieces an airy summer finish.</li>",
    "</ul>",
    "<p>Select each dress, top, shirt, or shorts size to create a crisp matching moment for the whole family.</p>",
])

BODY_HTML_OUT.write_text(body)
SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2))

variants, recap = [], []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    variant = {
        "price": price, "compareAtPrice": compare, "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": sku(row), "tracked": True, "requiresShipping": True},
        "optionValues": [{"optionName": "Type", "name": row["garment"]}, {"optionName": "Size", "name": row["picker_label"]}],
    }
    variants.append(variant)
    gid, catalog_label = size_map[row["picker_label"]]
    recap.append({**row, "sku": sku(row), "price": price, "compare": compare, "size_gid": gid, "catalog_label": catalog_label})

type_values = ["Dress", "Top", "Shirt", "Shorts"]
size_values = []
for row in chart:
    if row["picker_label"] not in size_values:
        size_values.append(row["picker_label"])
options = [{"name": "Type", "values": [{"name": value} for value in type_values]}, {"name": "Size", "values": [{"name": value} for value in size_values]}]
tags = sorted(set([
    "Family Matching", "Mommy and Me", "Daddy and Me", "Matching Family Set", "Matching Family Outfits",
    "Matching Family Dress", "Matching Family Shirt", "Matching Family Shorts", "Dress, Top, Shirt & Shorts",
    "Sets", "Summer", "Beach", "Vacation", "Resort", "Cruise", "Ocean Blue", "Slate Blue", "Blue", "Polka Dot",
    "Soft Woven", "Sleeveless Top", "Short Sleeve Shirt", "Short Sleeve Shirt", "Shorts", "Four-Role Matching",
    "Girl Dress", "Mother Top", "Boy Shirt", "Boy Shorts", "Father Shirt", "Father Shorts", VENDOR_URL,
] + size_values + ["Mother S","Mother M","Mother L","Mother XL","Mother 2XL","Mother 3XL","Father S","Father M","Father L","Father XL","Father 2XL","Father 3XL","Father 4XL"]))

def gql(query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(API, data=data, headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        output = json.loads(response.read())
    if output.get("errors"):
        raise SystemExit(output["errors"])
    return output

def user_errors(output, path):
    current = output
    for part in path.split("."):
        if part:
            current = current.get(part, {})
    if current:
        raise SystemExit(current)

node = gql("query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName}}}", {"id": TAXONOMY_GID})["data"]["node"]
if node["fullName"] != EXPECTED_TAXONOMY:
    raise SystemExit(f"taxonomy mismatch: {node['fullName']}")

product_input = {
    "handle": HANDLE, "title": TITLE, "descriptionHtml": body, "vendor": "dresslikemommy.com",
    "productType": PRODUCT_TYPE, "tags": tags, "status": "ACTIVE", "category": TAXONOMY_GID,
    "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
}
existing = gql("query($handle:String!){productByHandle(handle:$handle){id variants(first:100){nodes{id sku}}}}", {"handle": HANDLE})["data"]["productByHandle"]
if existing:
    product_id = existing["id"]
    output = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id} userErrors{field message}}}", {"product": {"id": product_id, **product_input}})
    user_errors(output, "data.productUpdate.userErrors")
    live_skus = sorted([variant["sku"] for variant in existing["variants"]["nodes"] if variant.get("sku")])
    spec_skus = sorted([variant["inventoryItem"]["sku"] for variant in variants])
    if live_skus and live_skus != spec_skus:
        raise SystemExit(f"existing product has unexpected SKUs: {live_skus}")
    if live_skus == spec_skus:
        variant_ids = {variant["sku"]: variant["id"] for variant in existing["variants"]["nodes"]}
        updates = [{"id": variant_ids[variant["inventoryItem"]["sku"]], "price": variant["price"], "compareAtPrice": variant["compareAtPrice"], "inventoryPolicy": "DENY", "optionValues": variant["optionValues"]} for variant in variants]
        output = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$productId,variants:$variants){userErrors{field message}}}", {"productId": product_id, "variants": updates})
        user_errors(output, "data.productVariantsBulkUpdate.userErrors")
    else:
        output = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
        user_errors(output, "data.productVariantsBulkCreate.userErrors")
else:
    output = gql("mutation($input:ProductInput!){productCreate(input:$input){product{id} userErrors{field message}}}", {"input": {**product_input, "productOptions": options}})
    user_errors(output, "data.productCreate.userErrors")
    product_id = output["data"]["productCreate"]["product"]["id"]
    output = gql("mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}", {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
    user_errors(output, "data.productVariantsBulkCreate.userErrors")

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Polka Dot Ocean Blue"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Ocean Dot"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress Top Shirt Shorts"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/70220546145","gid://shopify/Metaobject/69639733345"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(list(dict.fromkeys(size_map[row["picker_label"]][0] for row in chart)))},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889","gid://shopify/Metaobject/130231107681"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
]
for index in range(0, len(metafields), 25):
    output = gql("mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){userErrors{field message}}}", {"metafields": metafields[index:index + 25]})
    user_errors(output, "data.metafieldsSet.userErrors")

publications = [{"publicationId": publication_id} for publication_id in [
    "gid://shopify/Publication/55169925", "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225", "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
]]
output = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id status} userErrors{field message}}}", {"product": {"id": product_id, "status": "ACTIVE"}})
user_errors(output, "data.productUpdate.userErrors")
output = gql("mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}", {"id": product_id, "input": publications})
user_errors(output, "data.publishablePublish.userErrors")

media = gql("query($id:ID!){product(id:$id){media(first:50){nodes{... on MediaImage{id alt image{url}}}}}}", {"id": product_id})["data"]["product"]["media"]["nodes"]
existing_alts = {item.get("alt") for item in media}
for image_path in sorted(list(UPLOAD_DIR.glob("*.png")) + list(UPLOAD_DIR.glob("*.jpg")) + list(UPLOAD_DIR.glob("*.jpeg")) + list(UPLOAD_DIR.glob("*.webp"))):
    alt = "Family wearing ocean-blue dot matching dress, top, shirt, and shorts set."
    if alt in existing_alts:
        continue
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    output = gql("mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}", {"input": [{"filename": image_path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]})
    user_errors(output, "data.stagedUploadsCreate.userErrors")
    target = output["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    args = ["curl", "-sS", "-X", "POST", target["url"]]
    for param in target["parameters"]:
        args += ["-F", f"{param['name']}={param['value']}"]
    args += ["-F", f"file=@{image_path}"]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    output = gql("mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){userErrors{field message}}}", {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})
    user_errors(output, "data.productCreateMedia.userErrors")

output = gql("mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id status} userErrors{field message}}}", {"product": {"id": product_id, "status": "ACTIVE"}})
user_errors(output, "data.productUpdate.userErrors")
output = gql("mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}", {"id": product_id, "input": publications})
user_errors(output, "data.publishablePublish.userErrors")

time.sleep(3)
verify = gql("query($id:ID!){product(id:$id){id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}} collections(first:50){nodes{title handle}} metafields(first:100){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}} media(first:20){nodes{... on MediaImage{id alt image{url}}}}}}", {"id": product_id})
VERIFY_JSON_OUT.write_text(json.dumps(verify, indent=2))
product = verify["data"]["product"]
live_variants = product["variants"]["nodes"]
live_skus = sorted(variant["sku"] for variant in live_variants)
spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
checks = [
    ("title length", len(product["title"]) <= 70, str(len(product["title"]))),
    ("seo title length", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("seo description length", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("variant count", len(live_variants) == len(variants), f"{len(live_variants)} vs {len(variants)}"),
    ("sku parity", live_skus == spec_skus, ", ".join(live_skus)),
    ("taxonomy", product["category"]["fullName"] == EXPECTED_TAXONOMY, product["category"]["fullName"]),
    ("status active", product["status"] == "ACTIVE", product["status"]),
    ("published", bool(product["publishedAt"]), str(product["publishedAt"])),
    ("online url", bool(product["onlineStoreUrl"]), str(product["onlineStoreUrl"])),
]
price_ok = all(
    variant["price"] == next(spec["price"] for spec in variants if spec["inventoryItem"]["sku"] == variant["sku"])
    and variant["compareAtPrice"] == next(spec["compareAtPrice"] for spec in variants if spec["inventoryItem"]["sku"] == variant["sku"])
    and variant["inventoryPolicy"] == "DENY"
    and variant["inventoryItem"]["tracked"]
    and variant["inventoryItem"]["requiresShipping"]
    for variant in live_variants
)
checks.append(("price/inventory parity", price_ok, "FORCE_SPEC_PRICES true"))
header_count_ok = all(fragment.count("<th>") == 10 for fragment in re.findall(r"<table.*?</table>", body, re.S))
checks.append(("size table headers", header_count_ok, "10 headers per table"))
row_count_ok = body.count("<tr>") - 4 == len(chart)
checks.append(("size table row count", row_count_ok, f"{body.count(chr(60)+chr(116)+chr(114)+chr(62)) - 4} vs {len(chart)}"))
if not all(check[1] for check in checks):
    raise SystemExit(f"verification failed: {checks}")

with CSV_HEADER_SOURCE.open(newline="") as handle:
    header = next(csv.reader(handle))
rows = []
for item in recap:
    row = {field: "" for field in header}
    values = {
        "Handle": HANDLE, "Title": TITLE, "Body (HTML)": body, "Vendor": "dresslikemommy.com",
        "Product Category": EXPECTED_TAXONOMY, "Type": PRODUCT_TYPE, "Tags": ", ".join(product["tags"]),
        "Published": "TRUE", "Option1 Name": "Type", "Option1 Value": item["garment"],
        "Option2 Name": "Size", "Option2 Value": item["picker_label"], "Variant SKU": item["sku"],
        "Variant Grams": "0", "Variant Inventory Tracker": "shopify", "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual", "Variant Price": item["price"], "Variant Compare At Price": item["compare"],
        "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE", "SEO Title": SEO_TITLE,
        "SEO Description": SEO_DESCRIPTION, "Google Shopping / Gender": "unisex", "Google Shopping / Age Group": "adult",
        "Google Shopping / Condition": "new", "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "Family Matching", "Google Shopping / Custom Label 1": "Ocean Dot",
        "Google Shopping / Custom Label 2": "Summer", "Google Shopping / Custom Label 3": "Dress Top Shirt Shorts",
        "Google Shopping / Custom Label 4": "Four-Role Matching", "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": "Polka Dot Ocean Blue", "Style (product.metafields.custom.style)": "Matching Family Set",
        "SubCategory (product.metafields.custom.subcategory)": "Set", "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set",
        "Type (product.metafields.custom.type)": "Two-Piece Set", "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults", "Color (product.metafields.shopify.color-pattern)": "Ocean Blue, Blue",
        "Size (product.metafields.shopify.size)": ", ".join(size_values), "Status": "active",
    }
    for key, value in values.items():
        if key in row:
            row[key] = value
    rows.append(row)
with CSV_OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

written = sorted([f"{field['namespace']}.{field['key']}" for field in product["metafields"]["nodes"] if field["namespace"] in ["custom","mm-google-shopping","shopify","global"]])
skipped = {
    "shopify.fabric": "Vendor page was captcha-blocked and supplied screenshots do not confirm exact fiber content.",
    "shopify.dress-occasion": "The product is a mixed family separates listing, not a dress-only taxonomy product.",
    "shopify.dress-style": "The product mixes dress, top, shirt, and shorts variants, so one product-level dress style would be misleading.",
    "shopify.fit": "No reliable store catalog value was confirmed for this specific soft woven separates fit.",
    "shopify.neckline": "Sleeveless top/dress and short-sleeve shirt necklines do not map to one honest product-level neckline.",
    "shopify.pants-length-type": "Shorts are included, but the product also sells dresses, tops, and shirts, so one product-level pants length would be misleading.",
    "shopify.skirt-dress-length-type": "A girl dress is included, but the product also sells tops, shirts, and shorts, so one product-level dress length would be misleading.",
    "shopify.sleeve-length-type": "Sleeveless dresses/tops and short-sleeve shirts share one product, so one sleeve value would be misleading.",
    "shopify.top-length-type": "The listing mixes dresses, tops, shirts, and shorts, so one top-length value is not honest for the whole product.",
}
lines = [
    f"# {TITLE}", "", "## Links",
    f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    f"- **Live:** {product['onlineStoreUrl']}", f"- **Vendor:** {VENDOR_URL}",
    f"- **Product GID:** `{product_id}`", f"- **Handle:** `{HANDLE}`", "",
    "## Inputs (resolved)", "| Field | Value |", "|---|---|",
    f"| VENDOR_URL | {VENDOR_URL} |", "| SIZE_CHART_SOURCE | attached image |",
    "| LISTING_MODE | Family Matching |", "| PRIMARY_CATEGORY | FamilySet (Shopify taxonomy: Outfit Sets) |",
    "| DESIGNS_TO_LIST | auto -> one blue dot colorway from supplied imagery |",
    "| OPERATOR CATEGORY NOTE | one listing with Type options Dress, Top, Shirt, Shorts |",
    "| FORCE_SPEC_PRICES | true |", "| SHORTCODE | auto -> `ODOT` |", "| COLOR_TOKEN | auto -> `BLUE` |", "",
    "## Vendor fetch status",
    "The direct 1688 page returned Alibaba anti-bot/captcha markup, so the attached size-chart image and supplied product photo were used as authoritative. The chart supports girl dress and mother top rows, boy/father shirt rows, and boy/father shorts rows. Women/girls shorts appear in styling imagery but were not created as separate variants because no chart-backed shorts table was provided for those roles.",
    "",
    "## Option axes", "- Option 1: Type -> Dress, Top, Shirt, Shorts", "- Option 2: Size -> role-bearing size labels",
    f"- Variants live: {len(live_variants)}", "",
    "## SIZE_CHART / Variant Recap", "| Role | Vendor | Picker | Type | SKU | Price | shopify.size GID |", "|---|---|---|---|---|---|---|",
]
for item in recap:
    lines.append(f"| {item['role']} | {item['vendor_label']} | {item['picker_label']} | {item['garment']} | `{item['sku']}` | {item['price']} | `{item['size_gid']}` ({item['catalog_label']}) |")
lines += [
    "", "## Derivations",
    "- Adult weight guidance was published in Chinese domestic `斤` and converted to kg for the saved SIZE_CHART/body table.",
    "- Girl dress and mother top waist and hip were derived where omitted by the vendor using the canonical dress/top derivation rules.",
    "- Boy/father shirt hip values were derived where the vendor omitted seat/hip measurements.",
    "- Boy/father shorts hip values were derived as waist + 14 cm because the vendor omitted seat/hip values for shorts; this is flagged for future replacement if a fuller chart appears.",
    "- Boy shirt sleeve values are blank in the source chart and are displayed as `—`; father shirt sleeve values come from the adult table.",
    "- The vendor `3XL定制` women's row was mapped to `Mother 3XL` and kept because the row is chart-backed.",
    "- Added operator-supplied fit guidance to the PDP body: kids map to actual height labels 90-150cm, and adult Asian/1688 sizing is presented with a size-up recommendation.",
    "",
    "## Verification", "| Check | Result | Detail |", "|---|---|---|",
]
for name, ok, detail in checks:
    lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines += ["", "## Metafields Written"] + [f"- `{field}`" for field in written]
lines += ["", "## Metafields Skipped"] + [f"- `{key}`: {value}" for key, value in skipped.items()]
lines += [
    "", "## Tags Written", "`" + ", ".join(product["tags"]) + "`",
    "", "## Smart Collections", ", ".join(sorted(collection["handle"] for collection in product["collections"]["nodes"])) or "Pending smart collection propagation.",
    "", "## Publications", ", ".join(sorted(node["publication"]["name"] for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"])),
    "", "## Saved Files", f"- `{SCRIPT_PATH}`", f"- `{LISTING_MD}`", f"- `{CSV_OUT}`", f"- `{SIZE_CHART_OUT}`", f"- `{BODY_HTML_OUT}`", f"- `{VERIFY_JSON_OUT}`",
    "", "## Manual Follow-ups", "- Inventory quantities and per-variant grams still need operator stock values.", "- Re-check supplier fiber composition if the vendor page becomes readable later; `shopify.fabric` is intentionally skipped rather than guessed.",
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
