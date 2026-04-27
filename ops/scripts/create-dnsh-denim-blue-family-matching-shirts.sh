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

SETTINGS_JSON=$(cat <<'JSON'
{
  "root": "/Users/fsuels/Projects/dresslikemommy",
  "handle": "denim-blue-family-matching-shirts",
  "title": "Denim Blue Family Matching Tops - Long Sleeve Shirt",
  "seo_title": "Denim Family Matching Shirts | Dress Like Mommy",
  "seo_description": "Relaxed denim family matching shirts for mom, dad, girls and boys. Long-sleeve button-up tops in Child 1-2Y-9-10Y and Adult S-3XL.",
  "print_name": "Denim Blue",
  "shortcode": "DNSH",
  "color_token": "DENIM",
  "color_name": "Denim Blue",
  "listing_mode": "Family Matching",
  "category": "Tops",
  "category_word": "Tops",
  "product_type": "Matching Family Tops",
  "custom_type": "Top",
  "taxonomy_gid": "gid://shopify/TaxonomyCategory/aa-1-13-7",
  "expected_taxonomy_full_name": "Apparel & Accessories > Clothing > Clothing Tops > Shirts",
  "taxonomy_path": "Apparel & Accessories > Clothing > Clothing Tops > Shirts",
  "google_product_category": "Apparel & Accessories > Clothing > Clothing Tops > Shirts",
  "merch_subcategory": "Tops",
  "merch_subcategory2": "Family Matching Tops",
  "merch_style": "Matching Family Top",
  "merch_type": "Top",
  "season": "Spring/Summer",
  "vendor_url": "https://detail.1688.com/offer/824522939285.html",
  "vendor": "dresslikemommy.com",
  "force_spec_prices": true,
  "child_price": "24.99",
  "adult_price": "28.99",
  "price_neighbor_handle": "blue-apricot-letter-family-matching-tops",
  "size_neighbor_handle": "shopify--size metaobjects",
  "script_path": "/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-dnsh-denim-blue-family-matching-shirts.sh",
  "upload_dir": "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-shirts",
  "listing_md": "/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-shirts-listing.md",
  "csv_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-shirts-shopify-import.csv",
  "verify_json_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-denim-blue-family-matching-shirts.json",
  "size_chart_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-denim-blue-family-matching-shirts.json",
  "body_html_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/body-denim-blue-family-matching-shirts.html",
  "csv_header_source": "/Users/fsuels/Projects/dresslikemommy/bird-chirping-mommy-and-me-pajamas-shopify-import.csv",
  "age_group_gids": [
    "gid://shopify/Metaobject/128116523105",
    "gid://shopify/Metaobject/128116490337"
  ],
  "color_pattern_gids": [
    "gid://shopify/Metaobject/69639766113"
  ],
  "fabric_gids": [
    "gid://shopify/Metaobject/69669748833"
  ],
  "target_gender_gids": [
    "gid://shopify/Metaobject/129972502625"
  ],
  "fit_report": [
    {"role": "Boy", "height_cm": 110, "weight_jin": 33, "tried_size": "110", "note": "Loose fit"},
    {"role": "Girl", "height_cm": 113, "weight_jin": 37, "tried_size": "110", "note": "Close fit"},
    {"role": "Mom", "height_cm": 164, "weight_jin": 88, "tried_size": "S", "note": "Loose fit"},
    {"role": "Dad", "height_cm": 183, "weight_jin": 156, "tried_size": "XXL", "note": "Loose fit"}
  ],
  "product_image_sources": [
    "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-shirts/look-1.png",
    "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-shirts/look-2.png"
  ],
  "size_chart_source": "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-shirts/source-size-chart.png",
  "required_tags": [
    "Family Matching",
    "Tops",
    "Matching Family Top",
    "Matching Family Tops",
    "Denim",
    "Denim Blue",
    "Button-Up Shirt",
    "Long Sleeve Shirt",
    "Adult S",
    "Adult M",
    "Adult L",
    "Adult XL",
    "Adult 2XL",
    "Adult 3XL",
    "Child 1-2 Years",
    "Child 2 Years",
    "Child 3 Years",
    "Child 4 Years",
    "Child 5 Years",
    "Child 6-7 Years",
    "Child 8 Years",
    "Child 9-10 Years",
    "https://detail.1688.com/offer/824522939285.html"
  ]
}
JSON
)

SIZE_CHART_JSON=$(cat <<'JSON'
[
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":36,"sleeve_cm":28,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":39,"sleeve_cm":31,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":42,"sleeve_cm":34,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":45,"sleeve_cm":37,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":48,"sleeve_cm":40,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":51,"sleeve_cm":43,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":54,"sleeve_cm":46,"pant_cm":0},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":94,"hip_cm":98,"waist_cm":94,"length_cm":57,"sleeve_cm":49,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"-","weight":"47.5-57.5 kg","height":"-","chest_cm":98,"hip_cm":98,"waist_cm":86,"length_cm":63,"sleeve_cm":53,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"-","weight":"58-62.5 kg","height":"-","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":65,"sleeve_cm":54,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"-","weight":"63-69.5 kg","height":"-","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":67,"sleeve_cm":55,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"-","weight":"70-77.5 kg","height":"-","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":69,"sleeve_cm":56,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"XXL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"-","weight":"78-85 kg","height":"-","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":71,"sleeve_cm":58,"pant_cm":0},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"-","weight":"85.5-95 kg","height":"-","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":73,"sleeve_cm":60,"pant_cm":0}
]
JSON
)

SIZE_METAOBJECT_MAP_JSON=$(cat <<'JSON'
[
  {"picker_label":"Child 1-2 Years","gid":"gid://shopify/Metaobject/129972797537","catalog_label":"12-18 months","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 8 Years","gid":"gid://shopify/Metaobject/129973026913","catalog_label":"8","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 9-10 Years","gid":"gid://shopify/Metaobject/129971552353","catalog_label":"10","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"shopify--size metaobjects"}
]
JSON
)

mkdir -p "${ROOT}/ops/listings" "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-shirts"

export SETTINGS_JSON SIZE_CHART_JSON SIZE_METAOBJECT_MAP_JSON SHOPIFY_STORE_DOMAIN SHOPIFY_ADMIN_ACCESS_TOKEN

python3 - <<'PY'
import csv
import html
import json
import math
import mimetypes
import os
import re
import time
from pathlib import Path

import requests

settings = json.loads(os.environ["SETTINGS_JSON"])
size_chart = json.loads(os.environ["SIZE_CHART_JSON"])
size_map_rows = json.loads(os.environ["SIZE_METAOBJECT_MAP_JSON"])
size_map = {row["picker_label"]: row for row in size_map_rows}

listing_md_path = Path(settings["listing_md"])
csv_out_path = Path(settings["csv_out"])
verify_json_path = Path(settings["verify_json_out"])
size_chart_out_path = Path(settings["size_chart_out"])
body_html_out_path = Path(settings["body_html_out"])
upload_dir = Path(settings["upload_dir"])
csv_header_source = Path(settings["csv_header_source"])

api = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
token = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]
headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}


def gql(query, variables=None):
    response = requests.post(api, headers=headers, json={"query": query, "variables": variables or {}}, timeout=90)
    response.raise_for_status()
    data = response.json()
    if data.get("errors"):
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], ensure_ascii=False)}")
    return data


def compare_at(price_text):
    value = float(price_text) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def format_num(value):
    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.1f}".rstrip("0").rstrip(".")


def strip_unit(text, unit):
    text = str(text or "").strip()
    if not text or text in {"-", "--"}:
        return "-"
    suffix = f" {unit}"
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def cm_cell(value):
    if value in (None, "", 0):
        return "-"
    return format_num(value)


def title_length_ok(text, limit):
    if len(text) > limit:
        raise RuntimeError(f"{text!r} exceeds {limit} characters ({len(text)})")


child_price = settings["child_price"]
adult_price = settings["adult_price"]
child_compare = compare_at(child_price)
adult_compare = compare_at(adult_price)

title_length_ok(settings["title"], 70)
title_length_ok(settings["seo_title"], 60)
title_length_ok(settings["seo_description"], 155)

taxonomy_data = gql(
    """
    query TaxonomyCategory($id: ID!) {
      node(id: $id) {
        __typename
        ... on TaxonomyCategory { id fullName isLeaf }
      }
    }
    """,
    {"id": settings["taxonomy_gid"]},
)
taxonomy_node = taxonomy_data["data"]["node"]
if (
    taxonomy_node.get("__typename") != "TaxonomyCategory"
    or taxonomy_node.get("id") != settings["taxonomy_gid"]
    or taxonomy_node.get("fullName") != settings["expected_taxonomy_full_name"]
    or taxonomy_node.get("isLeaf") is not True
):
    raise RuntimeError("Taxonomy guard failed: " + json.dumps(taxonomy_node, ensure_ascii=False))

role_tokens = {"Child Shirt": "KID", "Adult Shirt": "ADT"}
size_tokens = {
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
}

required_fields = [
    "audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix",
    "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm",
    "sleeve_cm", "pant_cm",
]

errors = []
seen_picker_labels = set()
for row in size_chart:
    missing = [field for field in required_fields if row.get(field) in (None, "")]
    if missing:
        errors.append(f"row {row.get('vendor_label')} missing {', '.join(missing)}")
    if row.get("picker_label") in seen_picker_labels:
        errors.append(f"duplicate picker_label: {row['picker_label']}")
    seen_picker_labels.add(row.get("picker_label"))
    if row.get("role") not in role_tokens:
        errors.append(f"missing role token mapping for {row.get('role')}")
    if row.get("picker_label") not in size_tokens:
        errors.append(f"missing size token mapping for {row.get('picker_label')}")
    if row.get("picker_label") not in size_map:
        errors.append(f"missing size metaobject mapping for {row.get('picker_label')}")
    if row.get("waist_cm") in (None, ""):
        errors.append(f"row {row.get('vendor_label')} missing waist_cm")
if errors:
    raise RuntimeError("Preflight failed:\n- " + "\n- ".join(errors))


def sku_for(row):
    return f"DLM-{settings['shortcode']}-{role_tokens[row['role']]}-{size_tokens[row['picker_label']]}-{settings['color_token']}"


size_values = [row["picker_label"] for row in size_chart]
product_options = [
    {"name": "Size", "values": [{"name": value} for value in size_values]},
    {"name": "Color", "values": [{"name": settings["color_name"]}]},
]

variants = []
recap = []
for row in size_chart:
    price = child_price if row["audience"] == "child" else adult_price
    compare = child_compare if row["audience"] == "child" else adult_compare
    sku = sku_for(row)
    variants.append(
        {
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {"sku": sku, "tracked": True, "requiresShipping": True},
            "optionValues": [
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": settings["color_name"]},
            ],
        }
    )
    recap.append(
        {
            **row,
            "sku": sku,
            "price": price,
            "compare_at_price": compare,
            "shopify_size_gid": size_map[row["picker_label"]]["gid"],
            "catalog_label": size_map[row["picker_label"]]["catalog_label"],
        }
    )

derived_skus = sorted(item["inventoryItem"]["sku"] for item in variants)

table_rows = []
for row in size_chart:
    table_rows.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(strip_unit(row['weight'], 'kg'))}</td>"
        f"<td>{html.escape(strip_unit(row['height'], 'cm'))}</td>"
        f"<td>{cm_cell(row['chest_cm'])}</td>"
        f"<td>{cm_cell(row['sleeve_cm'])}</td>"
        f"<td>{cm_cell(row['pant_cm'])}</td>"
        f"<td>{cm_cell(row['hip_cm'])}</td>"
        f"<td>{cm_cell(row['waist_cm'])}</td>"
        f"<td>{cm_cell(row['length_cm'])}</td>"
        "</tr>"
    )

body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Denim fabric in a soft blue wash, based on the vendor imagery and the attached size-chart source.</li>",
        "<li><strong>Family story:</strong> A relaxed matching shirt for moms, dads, girls, and boys that feels easy for everyday photos and casual outings.</li>",
        "<li><strong>Print reference:</strong> Denim Blue keeps the outfit simple and versatile, with a classic collared shirt shape and visible pocket detail.</li>",
        "<li><strong>Design details:</strong> Long sleeves, button front, relaxed fit, collared neckline, chest pockets, and an easy overshirt silhouette. White tees, pants, shoes, and hats shown in photos are styling only.</li>",
        "<li><strong>Care:</strong> Machine wash cold, turn inside out, line dry or tumble low, and avoid bleach. This is conservative care guidance because the blocked vendor page did not expose wash instructions.</li>",
        "<li><strong>Size range:</strong> Child 1-2Y through Child 9-10Y and Adult S through Adult 3XL.</li>",
        "</ul>",
        "",
        "<h3>Size Chart</h3>",
        "<table id=\"size-chart\">",
        "  <thead>",
        "    <tr>",
        "      <th>Size</th>",
        "      <th>Age</th>",
        "      <th>Weight (kg)</th>",
        "      <th>Height (cm)</th>",
        "      <th>Chest/Bust (cm)</th>",
        "      <th>Sleeve (cm)</th>",
        "      <th>Pant/Short or - (cm)</th>",
        "      <th>Hip (cm)</th>",
        "      <th>Waist (cm)</th>",
        "      <th>Garment Length (cm)</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        *table_rows,
        "  </tbody>",
        "</table>",
        "",
        "<p>Denim Blue is a laid-back family matching top with enough structure to look polished in photos and enough ease for real family days. The shirt works as a light overshirt over a tee, with a button front, relaxed body, and soft denim-blue color that coordinates across kids and adults without feeling overly formal.</p>",
        "",
        "<p>The attached vendor chart publishes one child ladder and one adult ladder rather than separate girl, boy, mom, and dad tables, so this draft keeps the variant structure honest with Child and Adult size labels instead of inventing unsupported role-specific rows. Chest is doubled from the source half-chest column; hip and waist are derived because the source omits them; and the try-on report supports the relaxed fit language across both kids and adults.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>One coordinated shirt:</strong> Same denim-blue button-up look for children and adults.</li>",
        "<li><strong>Photo-ready denim wash:</strong> Soft blue color, chest pockets, and a casual overshirt shape.</li>",
        "<li><strong>Relaxed family fit:</strong> Vendor try-on notes show loose fits for the boy, mom, and dad testers.</li>",
        "<li><strong>Easy styling:</strong> Layer over white tees with casual pants for a clean family look.</li>",
        "<li><strong>Chart-backed variants:</strong> Every size option is backed by the attached vendor size chart.</li>",
        "</ul>",
        "",
        "<p>Choose the child and adult sizes you need to build an easy matching denim look for family photos, travel days, and everyday outings.</p>",
    ]
)

tags = sorted(
    {
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Tops",
        "Matching Family Top",
        "Matching Family Tops",
        "Matching Family Outfits",
        "Denim",
        "Denim Blue",
        "Blue",
        "Button-Up Shirt",
        "Long Sleeve Shirt",
        "Collared Shirt",
        "Overshirt",
        "Relaxed Fit",
        "Spring",
        "Summer",
        "Family Photos",
        "Adult S",
        "Adult M",
        "Adult L",
        "Adult XL",
        "Adult 2XL",
        "Adult 3XL",
        "Child 1-2 Years",
        "Child 2 Years",
        "Child 3 Years",
        "Child 4 Years",
        "Child 5 Years",
        "Child 6-7 Years",
        "Child 8 Years",
        "Child 9-10 Years",
        settings["vendor_url"],
    }
)

size_chart_out_path.write_text(json.dumps(size_chart, indent=2), encoding="utf-8")
body_html_out_path.write_text(body_html, encoding="utf-8")

existing_data = gql(
    """
    query ExistingProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        status
        publishedAt
        onlineStoreUrl
        variants(first: 100) {
          nodes {
            id
            sku
            selectedOptions { name value }
          }
        }
        media(first: 50) {
          nodes {
            ... on MediaImage { id alt image { url } }
          }
        }
      }
    }
    """,
    {"handle": settings["handle"]},
)
existing_product = existing_data["data"]["productByHandle"]
product_id = existing_product["id"] if existing_product else ""
if existing_product and existing_product.get("publishedAt"):
    raise RuntimeError("Existing product is already published; refusing to alter publish state in draft workflow.")

if not product_id:
    create_result = gql(
        """
        mutation ProductCreate($input: ProductInput!) {
          productCreate(input: $input) {
            product { id handle title }
            userErrors { field message }
          }
        }
        """,
        {
            "input": {
                "handle": settings["handle"],
                "title": settings["title"],
                "descriptionHtml": body_html,
                "vendor": settings["vendor"],
                "productType": settings["product_type"],
                "tags": tags,
                "status": "DRAFT",
                "category": settings["taxonomy_gid"],
                "seo": {"title": settings["seo_title"], "description": settings["seo_description"]},
                "productOptions": product_options,
            }
        },
    )
    user_errors = create_result["data"]["productCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
    product_id = create_result["data"]["productCreate"]["product"]["id"]

update_result = gql(
    """
    mutation ProductUpdate($product: ProductUpdateInput!) {
      productUpdate(product: $product) {
        product { id handle title status }
        userErrors { field message }
      }
    }
    """,
    {
        "product": {
            "id": product_id,
            "handle": settings["handle"],
            "title": settings["title"],
            "descriptionHtml": body_html,
            "vendor": settings["vendor"],
            "productType": settings["product_type"],
            "tags": tags,
            "status": "DRAFT",
            "category": settings["taxonomy_gid"],
            "seo": {"title": settings["seo_title"], "description": settings["seo_description"]},
        }
    },
)
if update_result["data"]["productUpdate"]["userErrors"]:
    raise RuntimeError(f"productUpdate userErrors: {json.dumps(update_result['data']['productUpdate']['userErrors'], ensure_ascii=False)}")

existing_data = gql(
    """
    query ExistingProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        variants(first: 100) {
          nodes {
            id
            sku
            selectedOptions { name value }
          }
        }
        media(first: 50) {
          nodes {
            ... on MediaImage { id alt image { url } }
          }
        }
      }
    }
    """,
    {"handle": settings["handle"]},
)
existing_product = existing_data["data"]["productByHandle"]
live_variants = existing_product["variants"]["nodes"]
expected_option_pairs = {(row["picker_label"], settings["color_name"]) for row in size_chart}
live_option_pairs = {tuple(option["value"] for option in variant["selectedOptions"]) for variant in live_variants}

if not live_variants or (len(live_variants) == 1 and not live_variants[0]["sku"]):
    create_variants_result = gql(
        """
        mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
          productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
            productVariants { id sku title }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
    )
    user_errors = create_variants_result["data"]["productVariantsBulkCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productVariantsBulkCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
else:
    if len(live_variants) != len(size_chart) or live_option_pairs != expected_option_pairs:
        raise RuntimeError("Existing product has unexpected variant shape; refusing destructive variant changes.")
    live_by_pair = {tuple(option["value"] for option in variant["selectedOptions"]): variant for variant in live_variants}
    variant_update_payload = []
    for spec in variants:
        pair = tuple(value["name"] for value in spec["optionValues"])
        live_variant = live_by_pair[pair]
        variant_update_payload.append(
            {
                "id": live_variant["id"],
                "price": spec["price"],
                "compareAtPrice": spec["compareAtPrice"],
                "inventoryPolicy": "DENY",
                "optionValues": spec["optionValues"],
                "inventoryItem": spec["inventoryItem"],
            }
        )
    update_variants_result = gql(
        """
        mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
          productVariantsBulkUpdate(productId: $productId, variants: $variants) {
            productVariants { id sku title }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "variants": variant_update_payload},
    )
    user_errors = update_variants_result["data"]["productVariantsBulkUpdate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productVariantsBulkUpdate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": settings["merch_subcategory"]},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": settings["merch_subcategory2"]},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": settings["print_name"]},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": settings["merch_style"]},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": settings["merch_type"]},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": settings["print_name"]},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": settings["season"]},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Long Sleeve Shirt"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Top"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(settings["age_group_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(settings["color_pattern_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "fabric", "type": "list.metaobject_reference", "value": json.dumps(settings["fabric_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps([size_map[row["picker_label"]]["gid"] for row in size_chart])},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(settings["target_gender_gids"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": settings["seo_title"]},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": settings["seo_description"]},
]
metafields_result = gql(
    """
    mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { namespace key type value }
        userErrors { field message }
      }
    }
    """,
    {"metafields": metafields},
)
if metafields_result["data"]["metafieldsSet"]["userErrors"]:
    raise RuntimeError(f"metafieldsSet userErrors: {json.dumps(metafields_result['data']['metafieldsSet']['userErrors'], ensure_ascii=False)}")

media_lookup = gql(
    """
    query ProductMedia($id: ID!) {
      product(id: $id) {
        media(first: 50) {
          nodes {
            ... on MediaImage { id alt image { url } }
          }
        }
      }
    }
    """,
    {"id": product_id},
)
existing_media = media_lookup["data"]["product"]["media"]["nodes"]
existing_media_alts = {item.get("alt") or "" for item in existing_media}
media_files = sorted([path for path in upload_dir.iterdir() if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and not path.name.startswith("source-")])
alt_by_name = {
    "look-1.png": "Family wearing denim blue matching long-sleeve button-up shirts.",
    "look-2.png": "Mom, dad, and child in denim blue family matching shirts.",
}
for image_path in media_files:
    alt_text = alt_by_name.get(image_path.name, f"{settings['title']} lifestyle image")
    if alt_text in existing_media_alts:
        continue
    mime_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
    staged_upload = gql(
        """
        mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
        """,
        {"input": [{"filename": image_path.name, "mimeType": mime_type, "resource": "IMAGE", "httpMethod": "POST"}]},
    )
    user_errors = staged_upload["data"]["stagedUploadsCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"stagedUploadsCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
    staged_target = staged_upload["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    form_data = {param["name"]: param["value"] for param in staged_target["parameters"]}
    with image_path.open("rb") as file_handle:
        upload_response = requests.post(staged_target["url"], data=form_data, files={"file": (image_path.name, file_handle, mime_type)}, timeout=120)
        upload_response.raise_for_status()
    create_media = gql(
        """
        mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id alt } }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "media": [{"originalSource": staged_target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt_text}]},
    )
    if create_media["data"]["productCreateMedia"]["userErrors"]:
        raise RuntimeError(f"productCreateMedia userErrors: {json.dumps(create_media['data']['productCreateMedia']['userErrors'], ensure_ascii=False)}")

time.sleep(2)

verify_data = gql(
    """
    query VerifyProduct($id: ID!) {
      product(id: $id) {
        id title handle status publishedAt onlineStoreUrl tags descriptionHtml
        seo { title description }
        options { name position values }
        category { id fullName }
        variants(first: 100) {
          nodes {
            sku title price compareAtPrice inventoryPolicy
            selectedOptions { name value }
            inventoryItem { tracked requiresShipping }
          }
        }
        media(first: 50) {
          nodes { ... on MediaImage { alt image { url } } }
        }
        collections(first: 50) {
          nodes { title handle ruleSet { appliedDisjunctively rules { column relation condition } } }
        }
        metafields(first: 100) {
          nodes { namespace key type value }
        }
        resourcePublicationsV2(first: 20) {
          nodes { isPublished publishDate publication { id name } }
        }
      }
    }
    """,
    {"id": product_id},
)
verify_json_path.write_text(json.dumps(verify_data, indent=2), encoding="utf-8")
product = verify_data["data"]["product"]

table_match = re.search(r"(<table id=\"size-chart\">.*?</table>)", product["descriptionHtml"], re.S)
table_html = table_match.group(1) if table_match else ""
thead_count = len(re.findall(r"<th\b", table_html))
tbody_match = re.search(r"<tbody>(.*?)</tbody>", table_html, re.S)
tbody_html = tbody_match.group(1) if tbody_match else ""
tbody_rows = re.findall(r"<tr>(.*?)</tr>", tbody_html, re.S)
row_cells = [[re.sub(r"<[^>]+>", "", cell).strip() for cell in re.findall(r"<td>(.*?)</td>", row_html, re.S)] for row_html in tbody_rows]
first_cells = [cells[0] for cells in row_cells if cells]

live_skus = sorted(variant["sku"] for variant in product["variants"]["nodes"])
expected_by_sku = {item["sku"]: item for item in recap}
variant_checks = []
for variant in product["variants"]["nodes"]:
    expected = expected_by_sku[variant["sku"]]
    variant_checks.append(
        variant["price"] == expected["price"]
        and variant["compareAtPrice"] == expected["compare_at_price"]
        and variant["inventoryPolicy"] == "DENY"
        and variant["inventoryItem"]["tracked"] is True
        and variant["inventoryItem"]["requiresShipping"] is True
    )

written_metafields = {f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"]}
expected_metafields = {
    "custom.category1", "custom.subcategory", "custom.subcategory2", "custom.pattern",
    "custom.style", "custom.type", "mm-google-shopping.custom_product",
    "mm-google-shopping.gender", "mm-google-shopping.age_group",
    "mm-google-shopping.condition", "mm-google-shopping.custom_label_0",
    "mm-google-shopping.custom_label_1", "mm-google-shopping.custom_label_2",
    "mm-google-shopping.custom_label_3", "mm-google-shopping.custom_label_4",
    "shopify.age-group", "shopify.color-pattern", "shopify.fabric",
    "shopify.size", "shopify.target-gender", "global.title_tag",
    "global.description_tag",
}
publication_nodes = product["resourcePublicationsV2"]["nodes"]
live_publications = [node for node in publication_nodes if node.get("isPublished") is True]
single_unit_cells_ok = all("/" not in cell for cells in row_cells for cell in cells[1:])
picker_ok = [row["picker_label"] for row in size_chart] == first_cells
options_ok = [option["name"] for option in product["options"]] == ["Size", "Color"]
required_tags_ok = set(settings["required_tags"]).issubset(set(product["tags"]))

verification_rows = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"] or "") <= 60, str(len(product["seo"]["title"] or ""))),
    ("SEO description <= 155 chars", len(product["seo"]["description"] or "") <= 155, str(len(product["seo"]["description"] or ""))),
    ("Product options are Size / Color", options_ok, ", ".join(option["name"] for option in product["options"])),
    ("Live variant count matches SIZE_CHART", len(product["variants"]["nodes"]) == len(size_chart), f"{len(product['variants']['nodes'])} vs {len(size_chart)}"),
    ("Live SKUs match derived SKUs", live_skus == derived_skus, "match" if live_skus == derived_skus else "mismatch"),
    ("Every variant tracked + DENY + priced", all(variant_checks), "all variants verified" if all(variant_checks) else "one or more variants failed"),
    ("Product status is DRAFT", product["status"] == "DRAFT", product["status"]),
    ("publishedAt is null", product["publishedAt"] is None, str(product["publishedAt"])),
    ("onlineStoreUrl is not published", product["onlineStoreUrl"] is None, str(product["onlineStoreUrl"])),
    ("No sales-channel publications are live", not live_publications, json.dumps(live_publications)),
    ("Taxonomy category set", (product["category"] or {}).get("id") == settings["taxonomy_gid"], (product["category"] or {}).get("id") or "missing"),
    ("Taxonomy category full name matches expected leaf", (product["category"] or {}).get("fullName") == settings["expected_taxonomy_full_name"], (product["category"] or {}).get("fullName") or "missing"),
    ("Size-chart table has 10 columns", thead_count == 10, str(thead_count)),
    ("Size-chart table row count matches SIZE_CHART", len(tbody_rows) == len(size_chart), str(len(tbody_rows))),
    ("Picker labels match first size-table column", picker_ok, "exact order match" if picker_ok else "mismatch"),
    ("Size-chart cells use metric units only", single_unit_cells_ok, "no slash-separated values in table cells" if single_unit_cells_ok else "found dual-unit cell"),
    ("Required tags present", required_tags_ok, "all required tags present" if required_tags_ok else "missing required tags"),
    ("Applicable metafields written", expected_metafields.issubset(written_metafields), "all expected metafields present" if expected_metafields.issubset(written_metafields) else "missing metafields"),
]
failures = [row for row in verification_rows if not row[1]]
if failures:
    raise RuntimeError("Verification failed:\n- " + "\n- ".join(f"{label}: {detail}" for label, _, detail in failures))

product_numeric_id = product["id"].split("/")[-1]
admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_numeric_id}"

with csv_header_source.open("r", encoding="utf-8", newline="") as handle:
    csv_header = next(csv.reader(handle))

media_nodes = product["media"]["nodes"]
size_csv = ", ".join(row["picker_label"] for row in size_chart)
rows = []
for index, row in enumerate(recap, start=1):
    record = {column: "" for column in csv_header}
    values = {
        "Handle": settings["handle"],
        "Title": settings["title"],
        "Body (HTML)": body_html,
        "Vendor": settings["vendor"],
        "Product Category": settings["taxonomy_path"],
        "Type": settings["product_type"],
        "Tags": ", ".join(tags),
        "Published": "FALSE",
        "Option1 Name": "Size",
        "Option1 Value": row["picker_label"],
        "Option2 Name": "Color",
        "Option2 Value": settings["color_name"],
        "Variant SKU": row["sku"],
        "Variant Inventory Tracker": "shopify",
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": row["price"],
        "Variant Compare At Price": row["compare_at_price"],
        "Variant Requires Shipping": "TRUE",
        "Variant Taxable": "TRUE",
        "Gift Card": "FALSE",
        "SEO Title": settings["seo_title"],
        "SEO Description": settings["seo_description"],
        "Google Shopping / Google Product Category": settings["google_product_category"],
        "Google Shopping / Gender": "unisex",
        "Google Shopping / Age Group": "adult",
        "Google Shopping / MPN": row["sku"],
        "Google Shopping / Condition": "new",
        "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "Family Matching",
        "Google Shopping / Custom Label 1": settings["print_name"],
        "Google Shopping / Custom Label 2": settings["season"],
        "Google Shopping / Custom Label 3": "Long Sleeve Shirt",
        "Google Shopping / Custom Label 4": "Unisex Family Top",
        "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": settings["print_name"],
        "Style (product.metafields.custom.style)": settings["merch_style"],
        "SubCategory (product.metafields.custom.subcategory)": settings["merch_subcategory"],
        "SubCategory2 (product.metafields.custom.subcategory2)": settings["merch_subcategory2"],
        "Type (product.metafields.custom.type)": settings["merch_type"],
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "FALSE",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": "Blue",
        "Fabric (product.metafields.shopify.fabric)": "Denim",
        "Size (product.metafields.shopify.size)": size_csv,
        "Status": "draft",
    }
    for key, value in values.items():
        if key in record:
            record[key] = value
    if index <= len(media_nodes):
        record["Image Src"] = media_nodes[index - 1]["image"]["url"]
        record["Image Position"] = str(index)
        record["Image Alt Text"] = media_nodes[index - 1]["alt"] or ""
    rows.append(record)

csv_out_path.parent.mkdir(parents=True, exist_ok=True)
with csv_out_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=csv_header)
    writer.writeheader()
    writer.writerows(rows)

smart_collections = [node for node in product["collections"]["nodes"] if node.get("ruleSet") is not None]
smart_collection_lines = [f"- {node['title']} (`/{node['handle']}`)" for node in smart_collections] or ["- None returned immediately; draft products may not index into smart collections until publication."]
fit_report_lines = [f"- {row['role']}: {row['height_cm']} cm / {row['weight_jin']} jin tried `{row['tried_size']}` - {row['note']}" for row in settings["fit_report"]]
size_recap_lines = [f"| {row['vendor_label']} | {row['picker_label']} | {row['sku']} | ${row['price']} | {row['shopify_size_gid']} ({row['catalog_label']}) |" for row in recap]
verification_lines = [f"| {label} | {'PASS' if result else 'FAIL'} | {detail} |" for label, result, detail in verification_rows]

metafield_lines = [
    "- custom.category1 = `Family Matching`",
    f"- custom.subcategory = `{settings['merch_subcategory']}`",
    f"- custom.subcategory2 = `{settings['merch_subcategory2']}`",
    f"- custom.pattern = `{settings['print_name']}`",
    f"- custom.style = `{settings['merch_style']}`",
    f"- custom.type = `{settings['merch_type']}`",
    "- mm-google-shopping.custom_product = `false`",
    "- mm-google-shopping.gender = `unisex`",
    "- mm-google-shopping.age_group = `adult`",
    "- mm-google-shopping.condition = `new`",
    "- mm-google-shopping.custom_label_0 = `Family Matching`",
    f"- mm-google-shopping.custom_label_1 = `{settings['print_name']}`",
    f"- mm-google-shopping.custom_label_2 = `{settings['season']}`",
    "- mm-google-shopping.custom_label_3 = `Long Sleeve Shirt`",
    "- mm-google-shopping.custom_label_4 = `Unisex Family Top`",
    "- shopify.age-group -> `Kids`, `Adults`",
    "- shopify.color-pattern -> `Blue`",
    "- shopify.fabric -> `Denim`",
    "- shopify.size -> 14 catalog metaobject references in chart order",
    "- shopify.target-gender -> `Unisex`",
    "- global.title_tag = SEO title",
    "- global.description_tag = SEO description",
]
skipped_metafields = [
    ("shopify.clothing-features", "No honest standard clothing-features entry is needed for this denim family shirt."),
    ("shopify.fit", "The Shirts & Tops taxonomy may expose fit, but no reliable writable standard Shopify metafield definition is available in this store."),
    ("shopify.neckline", "A collared neckline is visible, but no reliable owner-subtype-safe standard neckline write was confirmed for this store."),
    ("shopify.top-length-type", "The chart exposes garment length but does not map cleanly to one standard top-length type."),
    ("shopify.sleeve-length-type", "The images and chart support long sleeves, but the store's writable standard sleeve-length value was not confirmed in this run."),
    ("shopify.pants-length-type", "Not applicable because pants are styling only and are not included."),
    ("shopify.dress-occasion", "Not applicable because this is a Tops listing."),
    ("shopify.dress-style", "Not applicable because this is a Tops listing."),
]

listing_md = "\n".join(
    [
        f"# {settings['title']}",
        "",
        "**Status:** Draft (DRAFT, not published)",
        f"**Admin URL:** {admin_url}",
        "**Live URL:** not published",
        f"**Product ID:** {product['id']}",
        f"**Handle:** {settings['handle']}",
        f"**Vendor (storefront):** {settings['vendor']}",
        f"**Vendor source URL (tags only):** {settings['vendor_url']}",
        "",
        "## Title & SEO",
        f"- **Title ({len(settings['title'])}/70):** {settings['title']}",
        f"- **SEO title ({len(settings['seo_title'])}/60):** {settings['seo_title']}",
        f"- **SEO description ({len(settings['seo_description'])}/155):** {settings['seo_description']}",
        "",
        "## Pricing",
        "| Audience | Price | Compare-at |",
        "|---|---|---|",
        f"| Child | ${child_price} | ${child_compare} |",
        f"| Adult | ${adult_price} | ${adult_compare} |",
        "",
        "## Vendor source-of-truth",
        f"- Direct workflow source: `{settings['vendor_url']}`.",
        "- The direct 1688 page was not used as a shopper-facing source; the attached size chart and supplied product images are treated as authoritative for this draft.",
        "- The supplied images show one denim-blue long-sleeve button-up shirt/overshirt for child and adult roles. Pants, white tees, hats, shoes, and office styling props are excluded.",
        "- Size-chart columns transcribed: Size, Garment Length, half chest, sleeve length, recommended height, recommended weight.",
        "- `chest_cm` values were derived by doubling the source half-chest column.",
        "- `hip_cm` and `waist_cm` were derived because the vendor chart omits them: child shirts use `hip = chest + 4` and `waist = chest`; adult shirts use `hip = chest` and `waist = chest - 12`.",
        "- Adult height guidance is blank in the vendor size table; the attached try-on report is preserved below instead of inventing a full adult height ladder.",
        "- Fit report preserved from the screenshot:",
        *fit_report_lines,
        "- Care guidance in the body copy is a conservative inference because the blocked vendor page did not expose wash instructions.",
        "- Product media used for upload:",
        *[f"- `{path}`" for path in settings["product_image_sources"]],
        "",
        "## SIZE_CHART recap",
        "| Vendor row | Picker label | SKU | Price | shopify.size GID |",
        "|---|---|---|---|---|",
        *size_recap_lines,
        "",
        "## Notes on mapping",
        "- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the draft uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.",
        "- `80` maps to `Child 1-2 Years` and uses the closest honest live `shopify.size` metaobject `12-18 months`.",
        "- `XXL` maps to `Adult 2XL` so the picker stays consistent with the store's standard adult size naming.",
        f"- Price pattern used the Tops fallback and is compatible with nearby family-top pricing; anchor noted as `{settings['price_neighbor_handle']}`.",
        "",
        "## Tags written",
        "`" + ", ".join(tags) + "`",
        "",
        "## Metafields written",
        *metafield_lines,
        "",
        "## Metafields skipped",
        *[f"- `{key}` - {reason}" for key, reason in skipped_metafields],
        "",
        "## Phase 6 verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        *verification_lines,
        "",
        "## Publication",
        "- Product remains `DRAFT`.",
        "- No sales-channel publications are live.",
        "- Live URL: not published.",
        "",
        "## Smart collections",
        *smart_collection_lines,
        "",
        "## Manual follow-ups",
        "- Inventory quantities and per-variant grams remain unset / zero and still need operator stock values.",
        "- If the vendor page becomes directly readable later, confirm exact fiber composition and washing instructions.",
        "- If Shopify exposes owner-subtype-safe values for sleeve length or neckline in this store, the runner can be extended to write those standard metafields.",
        "",
        "## Files",
        f"- `{settings['listing_md']}`",
        f"- `{settings['csv_out']}`",
        f"- `{settings['verify_json_out']}`",
        f"- `{settings['size_chart_out']}`",
        f"- `{settings['body_html_out']}`",
        f"- `{settings['script_path']}`",
        f"- `{settings['upload_dir']}`",
    ]
)
listing_md_path.write_text(listing_md + "\n", encoding="utf-8")

print(json.dumps({
    "admin_url": admin_url,
    "live_url": "not published",
    "handle": settings["handle"],
    "product_id": product["id"],
    "status": product["status"],
    "variant_count": len(product["variants"]["nodes"]),
    "published_at": product["publishedAt"],
    "live_publications": live_publications,
    "listing_md": str(listing_md_path),
    "csv": str(csv_out_path),
    "verify": str(verify_json_path),
}, indent=2))
PY
