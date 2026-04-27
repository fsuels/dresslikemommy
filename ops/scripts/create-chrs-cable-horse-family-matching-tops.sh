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

HANDLE = "cable-horse-family-matching-tops"
TITLE = "Cable Horse Family Matching Sweaters - Cozy Sweater"
SEO_TITLE = "Cable Horse Family Sweaters | Dress Like Mommy"
SEO_DESCRIPTION = "Cable-knit family matching sweaters in cream for mom, dad, girls & boys. Sizes 1-2Y-10Y and Adult S-4XL."
VENDOR_URL = "https://detail.1688.com/offer/1007389194841.html"
PRODUCT_TYPE = "Matching Family Sweaters"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-12"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Clothing Tops > Sweaters"
SHORTCODE = "CHRS"
COLOR_NAME = "Cream"
COLOR_TOKEN = "CREAM"
CHILD_PRICE = "24.99"
ADULT_PRICE = "28.99"

LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
SCRIPT_PATH = ROOT / "ops/scripts/create-chrs-cable-horse-family-matching-tops.sh"
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


def kg_from_jin(value):
    lo, hi = [float(part) for part in re.split(r"[-–]", value)]
    return f"{lo / 2:g}-{hi / 2:g} kg"


SIZE_TOKENS = {
    "Child 1-2 Years": "KID12Y",
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Adult S": "S",
    "Adult M": "M",
    "Adult L": "L",
    "Adult XL": "XL",
    "Adult 2XL": "2XL",
    "Adult 3XL": "3XL",
    "Adult 4XL": "4XL",
}

SIZE_METAOBJECT_MAP = {
    "Child 1-2 Years": ("gid://shopify/Metaobject/129972797537", "12-18 months"),
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Adult S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Adult M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Adult L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Adult XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Adult 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Adult 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Adult 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

chart = []


def add_row(audience, role, vendor_label, picker_label, age, weight, height, length, chest, sleeve, shoulder):
    # Sweater sizing proxy: hip = chest, waist = chest for kids; adult waist = chest - 12.
    waist = chest if audience == "child" else chest - 12
    chart.append(
        {
            "audience": audience,
            "role": role,
            "garment": "Sweater",
            "vendor_label": vendor_label,
            "picker_label": picker_label,
            "sku_suffix": SIZE_TOKENS[picker_label],
            "age": age,
            "weight": weight,
            "height": height,
            "chest_cm": chest,
            "hip_cm": chest,
            "waist_cm": waist,
            "length_cm": length,
            "sleeve_cm": sleeve,
            "shoulder_cm": shoulder,
            "pant_cm": 0,
        }
    )


for args in [
    ("child", "Child Sweater", "80", "Child 1-2 Years", "1-2", "7.5-10 kg", "75-85 cm", 34, 70, 26, 33),
    ("child", "Child Sweater", "90", "Child 2 Years", "2", "10-13.5 kg", "85-95 cm", 37, 74, 28, 35),
    ("child", "Child Sweater", "100", "Child 3 Years", "3", "13.5-17 kg", "95-105 cm", 41, 78, 30, 37),
    ("child", "Child Sweater", "110", "Child 4 Years", "4", "17-20.5 kg", "105-115 cm", 44, 82, 32, 39),
    ("child", "Child Sweater", "120", "Child 5 Years", "5", "20.5-24 kg", "115-125 cm", 47, 86, 34, 41),
    ("child", "Child Sweater", "130", "Child 6-7 Years", "6-7", "24-27.5 kg", "125-135 cm", 50, 90, 36, 43),
    ("child", "Child Sweater", "140", "Child 8 Years", "8", "27.5-32.5 kg", "135-145 cm", 53, 94, 38, 45),
    ("child", "Child Sweater", "150", "Child 9-10 Years", "9-10", "32.5-37.5 kg", "145-155 cm", 56, 98, 40, 47),
    ("adult", "Adult Sweater", "S", "Adult S", "-", "40-50 kg", "150-160 cm", 58, 104, 57, 41),
    ("adult", "Adult Sweater", "M", "Adult M", "-", "50-60 kg", "155-165 cm", 61, 106, 59, 43),
    ("adult", "Adult Sweater", "L", "Adult L", "-", "60-70 kg", "160-170 cm", 64, 112, 61, 48),
    ("adult", "Adult Sweater", "XL", "Adult XL", "-", "70-80 kg", "165-175 cm", 67, 116, 63, 50),
    ("adult", "Adult Sweater", "XXL", "Adult 2XL", "-", "80-90 kg", "170-180 cm", 71, 120, 65, 51),
    ("adult", "Adult Sweater", "3XL", "Adult 3XL", "-", "90-100 kg", "175-185 cm", 74, 122, 67, 52),
    ("adult", "Adult Sweater", "4XL", "Adult 4XL", "-", "100-110 kg", "175-185 cm", 77, 124, 69, 53),
]:
    add_row(*args)

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
    try:
        parsed = float(value)
    except Exception:
        return str(value)
    if parsed.is_integer():
        return str(int(parsed))
    return f"{parsed:.2f}".rstrip("0").rstrip(".")


def cm_in(value):
    if not value:
        return "-"
    return f"{number(value)} cm / {number(float(value) / 2.54)} in"


def range_dual(value, unit, multiplier, output_unit):
    if value in ["-", "--"]:
        return "-"
    match = re.match(r"([\d.]+)-([\d.]+) " + re.escape(unit), value)
    if not match:
        return html.escape(value)
    lo, hi = [float(part) for part in match.groups()]
    return f"{number(lo)}-{number(hi)} {unit} / {number(lo * multiplier)}-{number(hi * multiplier)} {output_unit}"


def table(rows):
    body_rows = []
    for row in rows:
        values = [
            row["picker_label"],
            row["age"] if row["age"] != "-" else "-",
            range_dual(row["weight"], "kg", 2.20462, "lbs"),
            range_dual(row["height"], "cm", 1 / 2.54, "in"),
            cm_in(row["chest_cm"]),
            cm_in(row["sleeve_cm"]),
            "-",
            cm_in(row["hip_cm"]),
            cm_in(row["waist_cm"]),
            cm_in(row["length_cm"]),
        ]
        body_rows.append("<tr>" + "".join(f"<td>{html.escape(str(value))}</td>" for value in values) + "</tr>")
    return (
        '<h3>Size Chart - Sweater</h3>\n'
        '<table id="size-chart">\n<thead><tr>'
        "<th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th>"
        "<th>Chest/Bust (cm/in)</th><th>Sleeve or Skirt (cm/in)</th>"
        "<th>Pant/Short or - (cm/in)</th><th>Hip (cm/in)</th>"
        "<th>Waist (cm/in)</th><th>Garment Length (cm/in)</th>"
        "</tr></thead>\n<tbody>\n"
        + "\n".join(body_rows)
        + "\n</tbody></table>"
    )


body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Soft knit sweater fabric with a textured cable pattern; exact fiber content was not visible from the blocked vendor page.</li>",
        "<li><strong>Family story:</strong> A cozy cream matching sweater for moms, dads, girls, and boys, made for cool-weather photos and family outings.</li>",
        "<li><strong>Print reference:</strong> Cable Horse pairs an ivory cable knit with a small red horse patch at the chest.</li>",
        "<li><strong>Design details:</strong> Long sleeves, crew neckline, ribbed trim, cable texture, and a relaxed pullover sweater shape. Pants, boots, scarves, hats, and accessories are styling only.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, turn inside out, line dry flat, do not bleach, and use a cool iron only if needed.</li>",
        "<li><strong>Size range:</strong> Children 1-2Y through 9-10Y and adults S through 4XL.</li>",
        "</ul>",
        table(chart),
        "<p>Cable Horse brings a polished winter-family look into one easy sweater silhouette. The cream cable knit keeps the outfit classic, while the red horse patch gives every size a playful shared detail that reads clearly in family photos.</p>",
        "<p>The attached chart publishes sweater measurements for child sizes 80-150 and adult sizes S-4XL. Baby romper rows from the same chart are excluded from this sweater listing, and the styled pants, boots, scarf, hats, and accessories are not included.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Cozy matching sweater:</strong> One cream cable-knit pullover for children and adults.</li>",
        "<li><strong>Photo-ready chest patch:</strong> The red horse motif keeps the family set coordinated without feeling too loud.</li>",
        "<li><strong>Cool-weather styling:</strong> Long sleeves and ribbed trim make it easy for fall, winter, travel, and holiday photos.</li>",
        "<li><strong>Wide adult range:</strong> Adult sizes run from S through 4XL based on the attached vendor chart.</li>",
        "<li><strong>Honest product scope:</strong> This listing covers the sweaters only; baby rompers and styled bottoms are excluded.</li>",
        "</ul>",
        "<p>Choose each family member's size and build a cozy matching look for portraits, trips, and everyday cold-weather plans together.</p>",
    ]
)
BODY_HTML_OUT.write_text(body_html + "\n")

node = gql(
    "query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName}}}",
    {"id": TAXONOMY_GID},
)["data"]["node"]
if not node or node["fullName"] != EXPECTED_TAXONOMY:
    raise SystemExit(f"taxonomy mismatch: {node}")

size_values = [row["picker_label"] for row in chart]
options = [
    {"name": "Size", "values": [{"name": value} for value in size_values]},
    {"name": "Color", "values": [{"name": COLOR_NAME}]},
]


def sku(row):
    return f"DLM-{SHORTCODE}-{row['sku_suffix']}-{COLOR_TOKEN}"


variants = []
recap = []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    gid, catalog_label = SIZE_METAOBJECT_MAP[row["picker_label"]]
    variants.append(
        {
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {"sku": sku(row), "tracked": True, "requiresShipping": True},
            "optionValues": [
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": COLOR_NAME},
            ],
        }
    )
    recap.append({**row, "sku": sku(row), "price": price, "compare": compare, "size_gid": gid, "catalog_label": catalog_label})

tags = sorted(
    set(
        [
            "Family Matching",
            "Mommy and Me",
            "Daddy and Me",
            "Matching Family Outfits",
            "Family Sweaters",
            "Sweaters",
            "Cable Knit",
            "Cable Horse",
            "Horse Patch",
            "Cream",
            "Ivory",
            "Red",
            "Fall",
            "Winter",
            "Holiday",
            "Long Sleeve",
            "Crewneck Sweater",
            "Adult Sweater",
            "Child Sweater",
            VENDOR_URL,
        ]
        + size_values
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
    "query($handle:String!){productByHandle(handle:$handle){id variants(first:100){nodes{id sku}}}}",
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
                "optionValues": variant["optionValues"],
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
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Family Sweaters"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Sweaters"},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Cable Horse"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Sweater"},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Sweater"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Cable Horse"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Winter"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Sweater"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Family Sweaters"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/69622104161"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(list(dict.fromkeys(SIZE_METAOBJECT_MAP[row["picker_label"]][0] for row in chart)))},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
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
    "01-family-yacht.png": "Family wearing cream cable-knit matching sweaters with red horse patches on a boat.",
    "02-family-deck.png": "Parents and children in Cable Horse family matching sweaters in cream knit.",
}
for image_path in sorted(UPLOAD_DIR.glob("*.png")):
    if image_path.name == "source-size-chart.png":
        continue
    alt = media_alts.get(image_path.name, "Cable Horse family matching sweater product image.")
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
        options{name values}
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

checks = [
    ("title length", len(product["title"]) <= 70, str(len(product["title"]))),
    ("seo title length", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("seo description length", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("variant count", len(live_variants) == len(variants), f"{len(live_variants)} vs {len(variants)}"),
    ("sku parity", live_skus == spec_skus, ", ".join(live_skus)),
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
        "Option2 Value": COLOR_NAME,
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
        "Google Shopping / Custom Label 1": "Cable Horse",
        "Google Shopping / Custom Label 2": "Winter",
        "Google Shopping / Custom Label 3": "Sweater",
        "Google Shopping / Custom Label 4": "Family Sweaters",
        "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": "Cable Horse",
        "Style (product.metafields.custom.style)": "Matching Family Sweater",
        "SubCategory (product.metafields.custom.subcategory)": "Family Sweaters",
        "SubCategory2 (product.metafields.custom.subcategory2)": "Sweaters",
        "Type (product.metafields.custom.type)": "Sweater",
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": "Cream, Red",
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
    "shopify.fabric": "Vendor page was blocked and screenshots/size chart do not confirm one exact fiber composition.",
    "shopify.sleeve-length-type": "The store taxonomy/metafield requirements were not reliable enough for this sweater category during the run; sleeve measurements remain in the chart.",
    "shopify.neckline": "Crewneck is visible, but no verified writable neckline value was required for the Sweaters category during this run.",
    "shopify.top-length-type": "The chart provides garment lengths directly; no single catalog top-length value was necessary.",
}

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
    "| PRIMARY_CATEGORY | Sweaters |",
    "| DESIGNS_TO_LIST | auto -> cream cable-knit sweater with red horse patch |",
    "| EXCLUDE_ITEMS | baby romper/crawler rows excluded from the sweater listing; styled pants, boots, scarves, hats, and accessories excluded |",
    "| FORCE_SPEC_PRICES | true |",
    "| SHORTCODE | auto -> `CHRS` |",
    "| COLOR_TOKEN | auto -> `CREAM` |",
    "",
    "## Vendor Fetch Status",
    "The direct 1688 page returned Alibaba captcha/punish markup, so the attached size-chart image and supplied product photos were used as the authoritative source. The chart publishes baby romper rows, child sweater rows, and adult sweater rows; this listing uses the child and adult sweater rows only so the product remains an honest family matching sweater listing.",
    "",
    "## Option Axes",
    "- Option 1: Size",
    "- Option 2: Color -> Cream",
    f"- Variants live: {len(live_variants)}",
    "",
    "## SIZE_CHART / Variant Recap",
    "| Role | Vendor | Picker | Color | SKU | Price | Compare-at | shopify.size GID |",
    "|---|---|---|---|---|---|---|---|",
]
for row in recap:
    lines.append(
        f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {COLOR_NAME} | `{row['sku']}` | {row['price']} | {row['compare']} | `{row['size_gid']}` ({row['catalog_label']}) |"
    )
lines += [
    "",
    "## Derivations",
    "- Vendor weights were listed in jin; they were converted to kg in the saved SIZE_CHART and shopper-facing table.",
    "- Hip and waist values were derived because the vendor chart only publishes length, chest, sleeve, shoulder, height, and weight guidance. Child hip/waist = chest; adult hip = chest and waist = chest - 12.",
    "- Vendor adult labels are unisex in the supplied chart, so picker labels use Adult S-4XL instead of duplicating mother/father variants from the same row.",
    "- The baby romper/crawler sub-table was transcribed as excluded scope, not published as variants.",
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
    "",
    "## Manual Follow-ups",
    "- Inventory quantities and per-variant weights still need operator stock values.",
    "- Re-check exact fiber composition if the vendor page becomes directly readable later; `shopify.fabric` is intentionally skipped rather than guessed.",
]
LISTING_MD.write_text("\n".join(lines) + "\n")

print(
    json.dumps(
        {
            "product_id": product_id,
            "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
            "live_url": product["onlineStoreUrl"],
            "variants": len(live_variants),
            "listing": str(LISTING_MD),
            "csv": str(CSV_OUT),
            "checks": checks,
        },
        indent=2,
    )
)
PYRUN
