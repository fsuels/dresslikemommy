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
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "ruffle-hem-mommy-and-me-dresses"
TITLE = "Ruffle Hem Mommy and Me Dresses - Tulle Sundress"
SEO_TITLE = "Ruffle Hem Matching Sundress | Dress Like Mommy"
SEO_DESCRIPTION = "Lightweight woven mommy-and-me tulle dresses for mom + daughter. Girls 2Y-10Y and Mom M-3XL in pink or purple with ruffle hems."
VENDOR_URL = "attached-image-only"
PRODUCT_TYPE = "Matching Family Dresses"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-4"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Dresses"
SHORTCODE = "RRFL"
PRINT_NAME = "Ruffle Hem"
CHILD_PRICE = "31.99"
MOTHER_PRICE = "34.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-rrfl-ruffle-hem-mommy-and-me-dresses.sh"
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
MOTHER_COMPARE = compare_at(MOTHER_PRICE)

SIZE_TOKENS = {
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother M": "M",
    "Mother L": "L",
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Mother 3XL": "3XL",
}

SIZE_METAOBJECT_MAP = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}

COLORWAYS = [
    {"name": "Purple", "token": "PURPLE", "gid": "gid://shopify/Metaobject/130284126305"},
    {"name": "Pink", "token": "PINK", "gid": "gid://shopify/Metaobject/69963645025"},
]


def kg_lbs_from_jin(low, high):
    kg_low = low / 2
    kg_high = high / 2
    lb_low = kg_low * 2.20462
    lb_high = kg_high * 2.20462
    return f"{kg_low:g}-{kg_high:g} kg / {lb_low:.1f}-{lb_high:.1f} lbs"


chart = []


def add_child(vendor_label, picker_label, age, length, chest, height, weight_jin):
    low, high = weight_jin
    chart.append(
        {
            "audience": "child",
            "role": "Girl Dress",
            "garment": "Dress",
            "vendor_label": vendor_label,
            "picker_label": picker_label,
            "sku_suffix": SIZE_TOKENS[picker_label],
            "age": age,
            "weight": kg_lbs_from_jin(low, high),
            "height": f"{height[0]}-{height[1]} cm / {height[0] / 2.54:.1f}-{height[1] / 2.54:.1f} in",
            "chest_cm": chest,
            "hip_cm": chest + 4,
            "waist_cm": chest,
            "length_cm": length,
            "skirt_cm": length,
            "pant_cm": 0,
        }
    )


def add_mother(vendor_label, picker_label, length, chest, height, weight_jin):
    low, high = weight_jin
    hip = chest + 6
    chart.append(
        {
            "audience": "mother",
            "role": "Mother Dress",
            "garment": "Dress",
            "vendor_label": vendor_label,
            "picker_label": picker_label,
            "sku_suffix": SIZE_TOKENS[picker_label],
            "age": "-",
            "weight": kg_lbs_from_jin(low, high),
            "height": f"{height[0]}-{height[1]} cm / {height[0] / 2.54:.1f}-{height[1] / 2.54:.1f} in",
            "chest_cm": chest,
            "hip_cm": hip,
            "waist_cm": hip - 8,
            "length_cm": length,
            "skirt_cm": length,
            "pant_cm": 0,
        }
    )


for row in [
    ("90", "Child 2 Years", "2", 53, 60, (85, 95), (20, 26)),
    ("100", "Child 3 Years", "3", 57.5, 64, (95, 105), (26, 34)),
    ("110", "Child 4 Years", "4", 62, 68, (105, 115), (34, 42)),
    ("120", "Child 5 Years", "5", 66.5, 72, (115, 125), (42, 52)),
    ("130", "Child 6-7 Years", "6-7", 71, 76, (125, 135), (52, 65)),
    ("140", "Child 8 Years", "8", 75.5, 80, (135, 145), (62, 75)),
    ("150", "Child 9-10 Years", "9-10", 80, 84, (145, 155), (75, 90)),
]:
    add_child(*row)

for row in [
    ("M", "Mother M", 84, 92, (155, 160), (82, 105)),
    ("L", "Mother L", 85, 96, (160, 165), (106, 120)),
    ("XL", "Mother XL", 86, 100, (165, 170), (121, 135)),
    ("XXL", "Mother 2XL", 87, 104, (170, 175), (136, 150)),
    ("XXXL", "Mother 3XL", 88, 108, (175, 180), (151, 165)),
]:
    add_mother(*row)

SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2) + "\n")


def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(
        API,
        data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
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


def number(value):
    parsed = float(value)
    return str(int(parsed)) if parsed.is_integer() else f"{parsed:g}"


def cm_in(value):
    if not value:
        return "-"
    return f"{number(value)} cm / {float(value) / 2.54:.1f} in"


def render_table(rows):
    body_rows = []
    for row in rows:
        values = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "",
            row["weight"],
            row["height"],
            cm_in(row["chest_cm"]),
            cm_in(row["skirt_cm"]),
            "-",
            cm_in(row["hip_cm"]),
            cm_in(row["waist_cm"]),
            cm_in(row["length_cm"]),
        ]
        body_rows.append("<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in values) + "</tr>")
    return (
        '<h3>Size Chart - Dress</h3>\n'
        '<table id="size-chart">\n<thead><tr>'
        "<th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        "<th>Chest/Bust (cm/in)</th><th>Skirt Length (cm/in)</th>"
        "<th>Pant/Short or - (cm/in)</th><th>Hip (cm/in)</th>"
        "<th>Waist (cm/in)</th><th>Garment Length (cm/in)</th>"
        "</tr></thead>\n<tbody>\n"
        + "\n".join(body_rows)
        + "\n</tbody></table>"
    )


body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven polyester with airy tulle overlay; exact fiber content was inferred from store dress precedent because the source is an image-only request.</li>",
        "<li><strong>Family story:</strong> A dreamy matching dress moment for mom and daughter, made for portraits, birthdays, garden parties, and vacation evenings.</li>",
        "<li><strong>Print reference:</strong> Ruffle Hem comes in soft Purple and Pink colorways with a romantic solid-color tulle finish.</li>",
        "<li><strong>Design details:</strong> Sleeveless round neckline, floaty overlay, high-low dress shape, and layered ruffle hem with petal-like texture.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle in a mesh bag, line dry, do not bleach, and steam lightly if needed.</li>",
        "<li><strong>Size range:</strong> Girls Child 2 Years to Child 9-10 Years; Mother M to Mother 3XL.</li>",
        "</ul>",
        render_table(chart),
        "<p>The Ruffle Hem Mommy and Me Dresses bring a soft, portrait-ready look to matching family style. The floaty tulle overlay and layered hem create gentle movement, while the pink and purple color choices make it easy to match the mood of the occasion.</p>",
        "<p>The supplied chart supports girls' sizes 90-150 and mother sizes M-3XL for this dress. Each size row is carried into the picker, and the two requested colorways share the same chart so both colors stay together in one clean product.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Two soft colors:</strong> Choose Purple or Pink in the same mother-daughter silhouette.</li>",
        "<li><strong>Layered ruffle hem:</strong> Petal-like tiers add texture and a dressed-up finish for photos and celebrations.</li>",
        "<li><strong>Floaty tulle overlay:</strong> The airy outer layer gives both dresses a light, romantic drape.</li>",
        "<li><strong>Sleeveless sundress shape:</strong> A round neckline and easy fit keep the look comfortable for warm days.</li>",
        "<li><strong>Chart-backed sizing:</strong> Girls and mother sizes are derived directly from the attached vendor size chart.</li>",
        "</ul>",
        "<p>Choose your sizes and favorite color to create a matching ruffle dress moment for birthdays, portraits, vacations, and special days together.</p>",
    ]
)
BODY_HTML_OUT.write_text(body_html + "\n")

node = gql(
    "query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName isLeaf}}}",
    {"id": TAXONOMY_GID},
)["data"]["node"]
if not node or node["fullName"] != EXPECTED_TAXONOMY or not node["isLeaf"]:
    raise SystemExit(f"taxonomy mismatch: {node}")

size_values = [row["picker_label"] for row in chart]
color_values = [color["name"] for color in COLORWAYS]
options = [
    {"name": "Size", "values": [{"name": value} for value in size_values]},
    {"name": "Color", "values": [{"name": value} for value in color_values]},
]

ROLE_TOKENS = {"Girl Dress": "GRL", "Mother Dress": "MOM"}


def sku(row, color):
    return f"DLM-{SHORTCODE}-{ROLE_TOKENS[row['role']]}-{row['sku_suffix']}-{color['token']}"


variants = []
recap = []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else MOTHER_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else MOTHER_COMPARE
    gid, catalog_label = SIZE_METAOBJECT_MAP[row["picker_label"]]
    for color in COLORWAYS:
        variants.append(
            {
                "price": price,
                "compareAtPrice": compare,
                "inventoryPolicy": "DENY",
                "inventoryItem": {"sku": sku(row, color), "tracked": True, "requiresShipping": True},
                "optionValues": [
                    {"optionName": "Size", "name": row["picker_label"]},
                    {"optionName": "Color", "name": color["name"]},
                ],
            }
        )
        recap.append({**row, "color": color["name"], "sku": sku(row, color), "price": price, "compare": compare, "size_gid": gid, "catalog_label": catalog_label})

tags = sorted(
    set(
        [
            "Mommy and Me",
            "Dresses",
            "Matching Family Dresses",
            "Matching Family Dress",
            "Girl Dress",
            "Mother Dress",
            "Sleeveless Dress",
            "Tulle Dress",
            "Ruffle Dress",
            "Ruffle Hem",
            "Sundress",
            "Sundresses",
            "High Low Dress",
            "Summer",
            "Birthday",
            "Portrait",
            "Vacation",
            "Pink",
            "Purple",
            "Pastel",
            "Mom Size M",
            "Mom Size L",
            "Mom Size XL",
            "Mom Size 2XL",
            "Mom Size 3XL",
            "Child 2-3yr",
            "Child 4-5yr",
            "Child 6-8yr",
            "Child 9-10yr",
            VENDOR_URL,
        ]
    )
)

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

existing = gql(
    "query($handle:String!){productByHandle(handle:$handle){id options{name values} variants(first:100){nodes{id sku selectedOptions{name value}}}}}",
    {"handle": HANDLE},
)["data"]["productByHandle"]

if existing:
    product_id = existing["id"]
    output = gql(
        "mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id} userErrors{field message}}}",
        {"product": {"id": product_id, **product_input}},
    )
    user_errors(output, "data.productUpdate.userErrors")
    live_skus = sorted([variant["sku"] for variant in existing["variants"]["nodes"] if variant.get("sku")])
    spec_skus = sorted([variant["inventoryItem"]["sku"] for variant in variants])
    if live_skus and live_skus != spec_skus:
        raise SystemExit(f"existing product has unexpected SKUs: {live_skus}")
    if live_skus == spec_skus:
        by_sku = {variant["sku"]: variant["id"] for variant in existing["variants"]["nodes"]}
        updates = [
            {
                "id": by_sku[variant["inventoryItem"]["sku"]],
                "price": variant["price"],
                "compareAtPrice": variant["compareAtPrice"],
                "inventoryPolicy": "DENY",
            }
            for variant in variants
        ]
        output = gql(
            "mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$productId,variants:$variants){userErrors{field message}}}",
            {"productId": product_id, "variants": updates},
        )
        user_errors(output, "data.productVariantsBulkUpdate.userErrors")
    else:
        output = gql(
            "mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}",
            {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
        )
        user_errors(output, "data.productVariantsBulkCreate.userErrors")
else:
    output = gql(
        "mutation($input:ProductInput!){productCreate(input:$input){product{id} userErrors{field message}}}",
        {"input": {**product_input, "productOptions": options}},
    )
    user_errors(output, "data.productCreate.userErrors")
    product_id = output["data"]["productCreate"]["product"]["id"]
    output = gql(
        "mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}",
        {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
    )
    user_errors(output, "data.productVariantsBulkCreate.userErrors")

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Dresses"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Dresses"},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Solid Pastel"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Ruffle Hem Tulle Sundress"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Ruffle Hem Tulle Sundress"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps([color["gid"] for color in COLORWAYS])},
    {"ownerId": product_id, "namespace": "shopify", "key": "dress-occasion", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622169697", "gid://shopify/Metaobject/69622202465"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "dress-style", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130282520673"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "fabric", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622366305"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "neckline", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972469857"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(list(dict.fromkeys(SIZE_METAOBJECT_MAP[row["picker_label"]][0] for row in chart)))},
    {"ownerId": product_id, "namespace": "shopify", "key": "skirt-dress-length-type", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130282487905"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
]

for index in range(0, len(metafields), 25):
    output = gql(
        "mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){userErrors{field message}}}",
        {"metafields": metafields[index : index + 25]},
    )
    user_errors(output, "data.metafieldsSet.userErrors")

publications = [
    {"publicationId": "gid://shopify/Publication/55169925"},
    {"publicationId": "gid://shopify/Publication/21969633377"},
    {"publicationId": "gid://shopify/Publication/29172400225"},
    {"publicationId": "gid://shopify/Publication/76582879329"},
    {"publicationId": "gid://shopify/Publication/76604768353"},
]
output = gql(
    "mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}",
    {"id": product_id, "input": publications},
)
user_errors(output, "data.publishablePublish.userErrors")

media = gql(
    "query($id:ID!){product(id:$id){media(first:50){nodes{... on MediaImage{id alt image{url}}}}}}",
    {"id": product_id},
)["data"]["product"]["media"]["nodes"]
existing_alts = {item.get("alt") for item in media}
media_alts = {
    "01-pink-ruffle-hem-mommy-and-me-dresses.png": "Mother and daughter wearing matching pink ruffle-hem tulle dresses by the water.",
    "02-purple-ruffle-hem-mommy-and-me-dresses.png": "Mother and daughter wearing matching purple ruffle-hem tulle dresses by the water.",
}
for image_path in sorted(UPLOAD_DIR.glob("*.png")):
    if image_path.name == "source-size-chart.png":
        continue
    alt = media_alts.get(image_path.name, "Ruffle Hem mommy-and-me tulle dress product image.")
    if alt in existing_alts:
        continue
    mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
    output = gql(
        "mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}",
        {"input": [{"filename": image_path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]},
    )
    user_errors(output, "data.stagedUploadsCreate.userErrors")
    target = output["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    args = ["curl", "-sS", "-X", "POST", target["url"]]
    for parameter in target["parameters"]:
        args += ["-F", f"{parameter['name']}={parameter['value']}"]
    args += ["-F", f"file=@{image_path}"]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    output = gql(
        "mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){userErrors{field message}}}",
        {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]},
    )
    user_errors(output, "data.productCreateMedia.userErrors")

time.sleep(3)
verify = gql(
    """
    query($id:ID!){
      product(id:$id){
        id title handle status publishedAt onlineStoreUrl descriptionHtml tags
        seo{title description}
        category{id fullName}
        options{name position values}
        variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}}
        media(first:50){nodes{... on MediaImage{id alt image{url}}}}
        collections(first:50){nodes{title handle}}
        metafields(first:100){nodes{namespace key type value}}
        resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}}
      }
    }
    """,
    {"id": product_id},
)
VERIFY_JSON_OUT.write_text(json.dumps(verify, indent=2) + "\n")
product = verify["data"]["product"]
live_variants = product["variants"]["nodes"]
live_skus = sorted(variant["sku"] for variant in live_variants)
spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
live_pairs = {
    tuple({opt["name"]: opt["value"] for opt in variant["selectedOptions"]}[name] for name in ["Size", "Color"])
    for variant in live_variants
}
spec_pairs = {(row["picker_label"], color["name"]) for row in chart for color in COLORWAYS}
tbody_match = re.search(r"<tbody>(.*?)</tbody>", product["descriptionHtml"], re.S)
tbody_rows = re.findall(r"<tr>", tbody_match.group(1), re.S) if tbody_match else []
th_count = len(re.findall(r"<th>", product["descriptionHtml"]))

checks = [
    ("title length", len(product["title"]) <= 70, str(len(product["title"]))),
    ("seo title length", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("seo description length", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("variant count", len(live_variants) == len(variants), f"{len(live_variants)} vs {len(variants)}"),
    ("sku parity", live_skus == spec_skus, ", ".join(live_skus)),
    ("Size x Color parity", live_pairs == spec_pairs, str(sorted(live_pairs))),
    ("size table row count", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("size table headers", th_count == 10, str(th_count)),
    ("taxonomy", product["category"]["fullName"] == EXPECTED_TAXONOMY, product["category"]["fullName"]),
    ("published", bool(product["publishedAt"]), str(product["publishedAt"])),
    ("online url", bool(product["onlineStoreUrl"]), str(product["onlineStoreUrl"])),
]
price_ok = all(
    variant["price"] == next(item["price"] for item in variants if item["inventoryItem"]["sku"] == variant["sku"])
    and variant["compareAtPrice"] == next(item["compareAtPrice"] for item in variants if item["inventoryItem"]["sku"] == variant["sku"])
    and variant["inventoryPolicy"] == "DENY"
    and variant["inventoryItem"]["tracked"]
    and variant["inventoryItem"]["requiresShipping"]
    for variant in live_variants
)
checks.append(("price and inventory parity", price_ok, "FORCE_SPEC_PRICES true"))
published_ids = sorted(
    node["publication"]["id"]
    for node in product["resourcePublicationsV2"]["nodes"]
    if node["isPublished"]
)
required_publication_ids = sorted(item["publicationId"] for item in publications)
checks.append(("required publications", published_ids == required_publication_ids, ", ".join(published_ids)))

if not all(check[1] for check in checks):
    raise SystemExit("verification failed: " + repr(checks))

with CSV_HEADER_SOURCE.open(newline="") as handle:
    header = next(csv.reader(handle))
rows = []
for row in recap:
    csv_row = {column: "" for column in header}
    values = {
        "Handle": HANDLE,
        "Title": TITLE,
        "Body (HTML)": body_html,
        "Vendor": "dresslikemommy.com",
        "Product Category": EXPECTED_TAXONOMY,
        "Type": PRODUCT_TYPE,
        "Tags": ", ".join(product["tags"]),
        "Published": "TRUE",
        "Option1 Name": "Size",
        "Option1 Value": row["picker_label"],
        "Option2 Name": "Color",
        "Option2 Value": row["color"],
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
        "Google Shopping / Gender": "female",
        "Google Shopping / Age Group": "adult",
        "Google Shopping / Condition": "new",
        "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "Mommy and Me",
        "Google Shopping / Custom Label 1": PRINT_NAME,
        "Google Shopping / Custom Label 2": "Summer",
        "Google Shopping / Custom Label 3": "Ruffle Hem Tulle Sundress",
        "Google Shopping / Custom Label 4": "Two-Role Matching",
        "Category1 (product.metafields.custom.category1)": "Mommy and Me",
        "Pattern (product.metafields.custom.pattern)": "Solid Pastel",
        "Style (product.metafields.custom.style)": "Ruffle Hem Tulle Sundress",
        "SubCategory (product.metafields.custom.subcategory)": "Dresses",
        "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Dresses",
        "Type (product.metafields.custom.type)": "Dress",
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": "Purple, Pink",
        "Size (product.metafields.shopify.size)": ", ".join(size_values),
        "Status": "active",
    }
    for key, value in values.items():
        if key in csv_row:
            csv_row[key] = value
    rows.append(csv_row)

with CSV_OUT.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

written = sorted(
    f"{field['namespace']}.{field['key']}"
    for field in product["metafields"]["nodes"]
    if field["namespace"] in ["custom", "global", "mm-google-shopping", "shopify"]
)
skipped = {
    "shopify.clothing-features": "The available catalog value was not specific or useful for this ruffle tulle dress.",
    "shopify.sleeve-length-type": "The source images show a sleeveless dress, but the available reference tested during the run did not belong to this store's sleeve-length definition, so the metafield was skipped instead of forcing a bad GID.",
    "shopify.top-length-type": "Dress length is rendered per size row; this metafield does not apply to the Dresses taxonomy.",
}

lines = [
    f"# {TITLE}",
    "",
    "## Links",
    f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
    f"- **Live:** {product['onlineStoreUrl']}",
    "- **Vendor:** attached images only; no vendor URL supplied in request",
    f"- **Product GID:** `{product_id}`",
    f"- **Handle:** `{HANDLE}`",
    "",
    "## Inputs (resolved)",
    "| Field | Value |",
    "|---|---|",
    "| VENDOR_URL | blank in request; recorded internally as `attached-image-only` tag |",
    "| SIZE_CHART_SOURCE | attached image |",
    "| LISTING_MODE | Mommy and Me |",
    "| PRIMARY_CATEGORY | Dresses |",
    "| DESIGNS_TO_LIST | one listing with Color options: Purple, Pink |",
    "| FORCE_SPEC_PRICES | true |",
    "| SHORTCODE | auto -> `RRFL` |",
    "| COLOR_TOKEN | per color -> `PURPLE`, `PINK` |",
    "",
    "## Source Status",
    "No direct vendor URL was supplied, so the attached product images and size-chart screenshot were treated as authoritative. Only Girl Dress and Mother Dress rows were used because the request is Mommy and Me; boys and fathers from the chart were excluded from this listing.",
    "",
    "## Option Axes",
    "- Option 1: Size",
    "- Option 2: Color -> Purple, Pink",
    f"- SIZE_CHART rows: {len(chart)}",
    f"- Variants live: {len(live_variants)}",
    "",
    "## SIZE_CHART / Variant Recap",
    "| Role | Vendor | Picker | Color | SKU | Price | Compare-at | shopify.size GID |",
    "|---|---|---|---|---|---|---|---|",
]
for row in recap:
    lines.append(
        f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['color']} | `{row['sku']}` | {row['price']} | {row['compare']} | `{row['size_gid']}` ({row['catalog_label']}) |"
    )
lines += [
    "",
    "## Derivations",
    "- Vendor weights were listed in jin; they were converted to kg/lbs in the saved SIZE_CHART and shopper-facing table.",
    "- The chart publishes chest/bust and dress length but not waist or hip. Per the master prompt, child hip = chest + 4 and child waist = chest; mother hip = bust + 6 and mother waist = hip - 8.",
    "- Child labels map 90 -> Child 2 Years, 100 -> Child 3 Years, 110 -> Child 4 Years, 120 -> Child 5 Years, 130 -> Child 6-7 Years, 140 -> Child 8 Years, 150 -> Child 9-10 Years.",
    "- Mother labels map M, L, XL, XXL, XXXL -> Mother M, Mother L, Mother XL, Mother 2XL, Mother 3XL.",
    "- Pricing follows nearby live mommy-and-me dress precedent with FORCE_SPEC_PRICES: girl variants 31.99 / 36.99 and mother variants 34.99 / 40.99.",
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
    "- If a supplier URL becomes available later, confirm exact fiber composition and any care guidance against the vendor page.",
]
LISTING_MD.write_text("\n".join(lines) + "\n")

print(
    json.dumps(
        {
            "product_id": product_id,
            "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
            "live_url": product["onlineStoreUrl"],
            "variants": len(live_variants),
            "collections": sorted(collection["handle"] for collection in product["collections"]["nodes"]),
            "listing": str(LISTING_MD),
            "csv": str(CSV_OUT),
            "checks": checks,
        },
        indent=2,
    )
)
PYRUN
