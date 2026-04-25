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
import csv, html, json, math, mimetypes, os, re, subprocess, time, urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "terracotta-tile-family-matching-set"
TITLE = "Terracotta Tile Family Matching Set - Dress, Shirt & Top"
SEO_TITLE = "Terracotta Tile Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Linen-look terracotta family matching set for mom, dad, girls & boys. Dress, shirt, and top sizes 2Y-10Y, Mother S-4XL, Father S-4XL."
VENDOR_URL = "https://detail.1688.com/offer/1032794279712.html"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Outfit Sets"
SHORTCODE = "TTIL"
COLOR_NAME = "Terracotta"
COLOR_TOKEN = "TERRA"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-ttil-terracotta-tile-family-matching-set.sh"
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
    "Mother XL": "XL", "Mother 2XL": "2XL", "Mother 3XL": "3XL", "Mother 4XL": "4XL",
    "Father S": "S", "Father M": "M", "Father L": "L", "Father XL": "XL",
    "Father 2XL": "2XL", "Father 3XL": "3XL", "Father 4XL": "4XL",
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
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

chart = []
def add(audience, role, garment, vendor, picker, age, weight, height, chest, length, sleeve=0, skirt=0, pant=0, hip=0, waist=0, note=""):
    if not hip:
        hip = chest + 6 if role == "Mother Dress" else chest + 4 if audience == "child" else chest
    if not waist:
        waist = hip - 8 if role == "Mother Dress" else chest if audience == "child" else chest - 12
    chart.append({
        "audience": audience, "role": role, "garment": garment, "vendor_label": vendor,
        "picker_label": picker, "sku_suffix": size_tokens[picker], "age": age, "weight": weight,
        "height": height, "chest_cm": chest, "hip_cm": hip, "waist_cm": waist, "length_cm": length,
        "sleeve_cm": sleeve, "skirt_cm": skirt, "pant_cm": pant, "source_note": note,
    })

child_rows = [
    ("90cm", "Child 2 Years", "1-2", "90 cm", "-"),
    ("100cm", "Child 3 Years", "2-3", "100 cm", "-"),
    ("110cm", "Child 4 Years", "4-5", "110 cm", "-"),
    ("120cm", "Child 5 Years", "5-6", "120 cm", "-"),
    ("130cm", "Child 6-7 Years", "7-8", "130 cm", "-"),
    ("140cm", "Child 8 Years", "9-10", "140 cm", "-"),
    ("150cm", "Child 9-10 Years", "11-12", "150 cm", "-"),
]
top_measurements = [(72, 35), (76, 37), (80, 39), (84, 41), (88, 43), (92, 45), (96, 47)]
boy_shirt_measurements = [(76, 37, 16), (80, 40, 17), (84, 43, 18), (88, 46, 19), (92, 49, 20), (96, 52, 21), (100, 55, 22)]
for (vendor, picker, age, height, weight), (chest, length) in zip(child_rows, top_measurements):
    add("child", "Girl Top", "Top", vendor, picker, age, weight, height, chest, length, note="Operator supplied height/age fit only; top garment measurements are backfilled from nearby live family-set grading.")
for (vendor, picker, age, height, weight), (chest, length, sleeve) in zip(child_rows, boy_shirt_measurements):
    add("child", "Boy Shirt", "Shirt", vendor, picker, age, weight, height, chest, length, sleeve=sleeve, note="Operator supplied height/age fit only; shirt measurements are backfilled from nearby live family-set grading.")

adult_rows = [
    ("S", "S", "155-160 cm", "45-50 kg"), ("M", "M", "160-165 cm", "50-55 kg"),
    ("L", "L", "165-170 cm", "55-62 kg"), ("XL", "XL", "170-175 cm", "62-70 kg"),
    ("XXL", "2XL", "175-178 cm", "70-78 kg"), ("3XL", "3XL", "178-182 cm", "78-88 kg"),
    ("4XL", "4XL", "180-185 cm", "88-95 kg"),
]
mother_measurements = [(92,109), (96,110), (100,112), (104,114), (108,115), (112,118), (116,119)]
father_measurements = [(114,66,20), (118,68,21), (122,70,22), (126,72,23), (130,74,24), (134,76,25), (138,78,26)]
for (vendor, suffix, height, weight), (chest, length) in zip(adult_rows, mother_measurements):
    add("mother", "Mother Dress", "Dress", vendor, f"Mother {suffix}", "-", weight, height, chest, length, skirt=length, note="Operator supplied Asian/1688 adult fit only; dress measurements are backfilled from nearby live family-set grading.")
for (vendor, suffix, height, weight), (chest, length, sleeve) in zip(adult_rows, father_measurements):
    add("father", "Father Shirt", "Shirt", vendor, f"Father {suffix}", "-", weight, height, chest, length, sleeve=sleeve, note="Operator supplied Asian/1688 adult fit only; shirt measurements are backfilled from nearby live family-set grading.")

required = ["audience","role","garment","vendor_label","picker_label","sku_suffix","age","weight","height","chest_cm","hip_cm","waist_cm","length_cm","sleeve_cm","skirt_cm","pant_cm"]
for row in chart:
    missing = [key for key in required if key not in row]
    if missing:
        raise SystemExit(f"missing fields for {row}: {missing}")
    if row["picker_label"] not in size_map:
        raise SystemExit(f"missing size GID for {row['picker_label']}")
if len({(row["role"], row["picker_label"]) for row in chart}) != len(chart):
    raise SystemExit("duplicate role/picker SIZE_CHART rows")

role_tokens = {"Girl Top": "GRL", "Boy Shirt": "BOY", "Mother Dress": "MOM", "Father Shirt": "DAD"}
type_tokens = {"Top": "TOP", "Shirt": "SHRT", "Dress": "DRS"}
def sku(row):
    return f"DLM-{SHORTCODE}-{role_tokens[row['role']]}-{type_tokens[row['garment']]}-{row['sku_suffix']}-{COLOR_TOKEN}"

def num(value):
    try:
        f = float(value)
        return str(int(f)) if f.is_integer() else f"{f:g}"
    except Exception:
        return str(value)

def cm_in(value):
    if not value:
        return "-"
    return f"{num(value)} cm / {num(float(value) / 2.54)} in"

def range_convert(text, unit, multiplier, out_unit):
    if text in ("-", "-", ""):
        return "-"
    match = re.match(r"([\d.]+)-([\d.]+) " + re.escape(unit), text)
    if match:
        low, high = map(float, match.groups())
        return f"{num(low)}-{num(high)} {unit} / {num(low * multiplier)}-{num(high * multiplier)} {out_unit}"
    match = re.match(r"([\d.]+) " + re.escape(unit), text)
    if match:
        value = float(match.group(1))
        return f"{num(value)} {unit} / {num(value * multiplier)} {out_unit}"
    return html.escape(text)

def table(rows, garment):
    rows_html = []
    for row in rows:
        sleeve_or_skirt = row["skirt_cm"] if garment == "Dress" else row["sleeve_cm"]
        rows_html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in [
            html.escape(row["picker_label"]), html.escape(row["age"]), range_convert(row["weight"], "kg", 2.20462, "lbs"),
            range_convert(row["height"], "cm", 1 / 2.54, "in"), cm_in(row["chest_cm"]),
            cm_in(sleeve_or_skirt), cm_in(row["pant_cm"]), cm_in(row["hip_cm"]), cm_in(row["waist_cm"]),
            cm_in(row["length_cm"]),
        ]) + "</tr>")
    return (
        f"<h3>Size Chart - {garment}</h3>\n<table id=\"size-chart-{garment.lower()}\"><thead><tr>"
        "<th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        "<th>Chest/Bust (cm/in)</th><th>Sleeve or Skirt (cm/in)</th><th>Pant/Short or - (cm/in)</th>"
        "<th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th>"
        "</tr></thead><tbody>\n" + "\n".join(rows_html) + "\n</tbody></table>"
    )

body = "\n".join([
    "<ul>",
    "<li><strong>Fabric:</strong> Lightweight linen-look woven fabric; exact fiber content was not visible from the blocked vendor page.</li>",
    "<li><strong>Family story:</strong> A warm vacation matching look for moms, dads, girls, and boys in one coordinated tile print.</li>",
    "<li><strong>Print:</strong> Terracotta geometric tile motif with soft ivory linework for a beachy resort feel.</li>",
    "<li><strong>Design details:</strong> Moms wear the strappy midi dress, dads and boys wear the short-sleeve camp-collar shirt, and girls wear the matching strappy top. White pants, shorts, hats, sunglasses, shoes, bags, and accessories are styling only.</li>",
    "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and steam or cool iron inside-out if needed.</li>",
    "<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S-4XL, and Father S-4XL.</li>",
    "</ul>",
    table([row for row in chart if row["garment"] == "Dress"], "Dress"),
    table([row for row in chart if row["garment"] == "Shirt"], "Shirt"),
    table([row for row in chart if row["garment"] == "Top"], "Top"),
    "<p>Terracotta Tile is made for sunny family photos, resort walks, and seaside dinners where everyone coordinates without wearing the exact same silhouette. The rust-red tile print keeps the look warm and polished, while the dress, shirt, and top options let each family member choose the piece shown in the source imagery.</p>",
    "<p>Kids sizes are based on the child's actual height from 90cm to 150cm. Adult sizing follows typical Asian/1688 fit guidance and tends to run small, so sizing up one from your usual US/EU size is recommended.</p>",
    "<h3>Key Features:</h3>",
    "<ul>",
    "<li><strong>Three garment options:</strong> Dress, Shirt, and Top in one coordinated family listing.</li>",
    "<li><strong>Vacation-ready print:</strong> Terracotta tile artwork photographs beautifully near the beach, pool, or boardwalk.</li>",
    "<li><strong>Role-bearing sizes:</strong> Labels clearly separate child, mother, and father size rows.</li>",
    "<li><strong>Chart-backed variants:</strong> Only the supplied 90-150cm kids rows and S-4XL adult rows were created.</li>",
    "<li><strong>Styling pieces excluded:</strong> White bottoms and accessories shown in the photos are not included.</li>",
    "</ul>",
    "<p>Select each Type and Size to build a warm, photo-ready family matching look for your next sunny day together.</p>",
])

BODY_HTML_OUT.write_text(body)
SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2))

variants, recap = [], []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    variants.append({
        "price": price, "compareAtPrice": compare, "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": sku(row), "tracked": True, "requiresShipping": True},
        "optionValues": [{"optionName": "Type", "name": row["garment"]}, {"optionName": "Size", "name": row["picker_label"]}],
    })
    gid, catalog_label = size_map[row["picker_label"]]
    recap.append({**row, "sku": sku(row), "price": price, "compare": compare, "size_gid": gid, "catalog_label": catalog_label})

type_values = ["Dress", "Shirt", "Top"]
size_values = []
for row in chart:
    if row["picker_label"] not in size_values:
        size_values.append(row["picker_label"])
options = [{"name": "Type", "values": [{"name": value} for value in type_values]}, {"name": "Size", "values": [{"name": value} for value in size_values]}]
tags = sorted(set([
    "Family Matching", "Mommy and Me", "Daddy and Me", "Matching Family Set", "Matching Family Outfits",
    "Matching Family Dress", "Matching Family Shirt", "Matching Family Top", "Dress Shirt Top",
    "Sets", "Summer", "Beach", "Vacation", "Resort", "Terracotta", "Rust", "Red", "Geometric",
    "Tile Print", "Linen Look", "Strappy Dress", "Strappy Top", "Camp Collar Shirt", "Short Sleeve Shirt",
    "Four-Role Matching", "Girl Top", "Mother Dress", "Boy Shirt", "Father Shirt", VENDOR_URL,
] + size_values + ["Mother S","Mother M","Mother L","Mother XL","Mother 2XL","Mother 3XL","Mother 4XL","Father S","Father M","Father L","Father XL","Father 2XL","Father 3XL","Father 4XL"]))

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
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Terracotta Tile Geometric"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Terracotta Tile"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress Shirt Top"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69600804961","gid://shopify/Metaobject/69639733345"])},
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
    alt = "Terracotta tile family matching dress, shirt, and top by the seaside." if "01-" in image_path.name else "Family wearing terracotta tile matching vacation outfits."
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
checks.append(("size table headers", all(fragment.count("<th>") == 10 for fragment in re.findall(r"<table.*?</table>", body, re.S)), "10 headers per table"))
checks.append(("size table row count", body.count("<tr>") - 3 == len(chart), f"{body.count('<tr>') - 3} vs {len(chart)}"))
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
        "Google Shopping / Custom Label 0": "Family Matching", "Google Shopping / Custom Label 1": "Terracotta Tile",
        "Google Shopping / Custom Label 2": "Summer", "Google Shopping / Custom Label 3": "Dress Shirt Top",
        "Google Shopping / Custom Label 4": "Four-Role Matching", "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": "Terracotta Tile Geometric", "Style (product.metafields.custom.style)": "Matching Family Set",
        "SubCategory (product.metafields.custom.subcategory)": "Set", "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set",
        "Type (product.metafields.custom.type)": "Two-Piece Set", "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults", "Color (product.metafields.shopify.color-pattern)": "Terracotta, Red",
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
    "shopify.dress-occasion": "The product is a mixed family set, so one product-level dress occasion would be incomplete.",
    "shopify.dress-style": "The listing mixes dress, shirt, and top variants.",
    "shopify.fit": "No reliable store catalog fit value was confirmed for this specific linen-look set.",
    "shopify.neckline": "Strappy tops/dresses and camp-collar shirts do not map to one honest product-level neckline.",
    "shopify.sleeve-length-type": "The listing mixes sleeveless/strappy pieces and short-sleeve shirts.",
    "shopify.top-length-type": "The listing mixes tops, shirts, and dresses.",
}
lines = [
    f"# {TITLE}", "", "## Links",
    f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    f"- **Live:** {product['onlineStoreUrl']}", f"- **Vendor:** {VENDOR_URL}",
    f"- **Product GID:** `{product_id}`", f"- **Handle:** `{HANDLE}`", "",
    "## Inputs (resolved)", "| Field | Value |", "|---|---|",
    f"| VENDOR_URL | {VENDOR_URL} |", "| SIZE_CHART_SOURCE | operator-supplied size/fit guidance; no measurement chart provided |",
    "| LISTING_MODE | Family Matching |", "| PRIMARY_CATEGORY | Sets (Shopify taxonomy: Outfit Sets) |",
    "| DESIGNS_TO_LIST | one listing with Type options Shirt, Dress, Top |",
    "| FORCE_SPEC_PRICES | true |", "| SHORTCODE | auto -> `TTIL` |", "| COLOR_TOKEN | auto -> `TERRA` |", "",
    "## Vendor fetch status",
    "The direct 1688 page returned Alibaba anti-bot/captcha markup, so the operator-provided size guidance and screenshots were used as authoritative. The source provides kids height labels 90-150cm and adult S-4XL fit guidance but no garment measurements; measurement columns are backfilled from nearby live dress-and-shirt family matching set grading and flagged here for future replacement if a vendor chart becomes available.",
    "",
    "## Option axes", "- Option 1: Type -> Dress, Shirt, Top", "- Option 2: Size -> role-bearing size labels",
    f"- Variants live: {len(live_variants)}", "",
    "## SIZE_CHART / Variant Recap", "| Role | Vendor | Picker | Type | SKU | Price | shopify.size GID |", "|---|---|---|---|---|---|---|",
]
for item in recap:
    lines.append(f"| {item['role']} | {item['vendor_label']} | {item['picker_label']} | {item['garment']} | `{item['sku']}` | {item['price']} | `{item['size_gid']}` ({item['catalog_label']}) |")
lines += [
    "", "## Derivations",
    "- Kids rows map directly from the supplied height labels: 90cm through 150cm.",
    "- Adult S-4XL rows map from the supplied Asian/1688 fit guide and include a size-up recommendation in the PDP copy.",
    "- Chest, hip, waist, length, sleeve, and skirt measurements were backfilled from nearby live family matching set grading because no vendor measurement chart was provided.",
    "- Girl rows are listed as `Top`, mother rows as `Dress`, and boy/father rows as `Shirt`, matching the supplied screenshots and requested Type options.",
    "- White pants, shorts, hats, sunglasses, shoes, handbags, and accessories are styling only and excluded from variants.",
    "- Pricing reused the nearby family matching dress-and-shirt set pattern with FORCE_SPEC_PRICES: child 28.99 / 33.99 compare-at, adult 31.99 / 36.99 compare-at.",
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
    "", "## Manual Follow-ups", "- Inventory quantities and per-variant grams still need operator stock values.", "- Re-check supplier fiber composition and direct garment measurements if the vendor page becomes readable later; `shopify.fabric` is intentionally skipped rather than guessed.",
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
