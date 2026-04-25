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
  "handle": "black-white-spelling-family-matching-tops",
  "title": "Black and White Spelling Family Matching Tops - Raglan Tee",
  "seo_title": "Black and White Family Tops | Dress Like Mommy",
  "seo_description": "Soft knit family matching raglan tops for parents and kids. Sizes Child 2Y-9-10Y and Adult S-4XL in black and white.",
  "print_name": "Black and White Spelling",
  "shortcode": "BWSP",
  "color_token": "BLACK",
  "color_name": "Black and White",
  "listing_mode": "Family Matching",
  "category": "Tops",
  "category_word": "Tops",
  "product_type": "Matching Family Tops",
  "custom_type": "Top",
  "taxonomy_gid": "gid://shopify/TaxonomyCategory/aa-1-13-8",
  "expected_taxonomy_full_name": "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts",
  "taxonomy_path": "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts",
  "google_product_category": "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts",
  "merch_subcategory": "Tops",
  "merch_subcategory2": "Matching Family T-Shirts",
  "merch_style": "Raglan Letter Tee",
  "merch_type": "Top",
  "season": "Summer",
  "vendor_url": "https://detail.1688.com/offer/903170078162.html?",
  "vendor": "dresslikemommy.com",
  "force_spec_prices": true,
  "child_price": "24.99",
  "adult_price": "28.99",
  "price_neighbor_handle": "fallback-tops-matrix",
  "size_neighbor_handle": "shopify--size metaobjects",
  "script_path": "/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-bwsp-black-white-spelling-family-matching-tops.sh",
  "upload_dir": "/Users/fsuels/Projects/dresslikemommy/uploads/black-white-spelling-family-matching-tops",
  "listing_md": "/Users/fsuels/Projects/dresslikemommy/ops/listings/black-white-spelling-family-matching-tops-listing.md",
  "csv_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/black-white-spelling-family-matching-tops-shopify-import.csv",
  "verify_json_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-black-white-spelling-family-matching-tops.json",
  "size_chart_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-black-white-spelling-family-matching-tops.json",
  "body_html_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/body-black-white-spelling-family-matching-tops.html",
  "csv_header_source": "/Users/fsuels/Projects/dresslikemommy/bird-chirping-mommy-and-me-pajamas-shopify-import.csv",
  "publications": [
    {"publicationId": "gid://shopify/Publication/55169925", "name": "Online Store"},
    {"publicationId": "gid://shopify/Publication/21969633377", "name": "Google & YouTube"},
    {"publicationId": "gid://shopify/Publication/29172400225", "name": "Facebook & Instagram"},
    {"publicationId": "gid://shopify/Publication/76582879329", "name": "Pinterest"},
    {"publicationId": "gid://shopify/Publication/76604768353", "name": "TikTok"}
  ],
  "age_group_gids": [
    "gid://shopify/Metaobject/128116523105",
    "gid://shopify/Metaobject/128116490337"
  ],
  "color_pattern_gids": [
    "gid://shopify/Metaobject/69943132257",
    "gid://shopify/Metaobject/69639733345",
    "gid://shopify/Metaobject/69963645025"
  ],
  "fabric_gids": [],
  "target_gender_gids": [
    "gid://shopify/Metaobject/129972502625"
  ],
  "product_info": {
    "evidence": "The direct vendor page was not readable from this shell; fabric is described only as soft knit tee fabric from the supplied photos, with no exact fiber claim.",
    "fabric_en": "Soft knit tee fabric",
    "color_en": "Black and White"
  },
  "fit_report": [],
  "product_image_sources": [
    "/Users/fsuels/Projects/dresslikemommy/uploads/black-white-spelling-family-matching-tops/look-1.png"
  ],
  "size_chart_source": "/Users/fsuels/Desktop/Screenshot 2026-04-24 at 9.32.37 AM.png",
  "required_tags": [
    "Family Matching",
    "Tops",
    "Matching Family Tops",
    "Matching Family T-Shirts",
    "Raglan Tee",
    "Short Sleeve Top",
    "Black and White Spelling",
    "Black",
    "White",
    "Pink",
    "Adult S",
    "Adult M",
    "Adult L",
    "Adult XL",
    "Adult 2XL",
    "Adult 3XL",
    "Adult 4XL",
    "Child 2 Years",
    "Child 3 Years",
    "Child 4 Years",
    "Child 5 Years",
    "Child 6-7 Years",
    "Child 8 Years",
    "Child 9-10 Years",
    "https://detail.1688.com/offer/903170078162.html?"
  ]
}
JSON
)

SIZE_CHART_JSON=$(cat <<'JSON'
[
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"10-12.5 kg","height":"85-95 cm","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":40,"shoulder_cm":32,"sleeve_cm":11,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"12.5-15 kg","height":"90-105 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":42,"shoulder_cm":34,"sleeve_cm":11.5,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-17.5 kg","height":"105-115 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":44,"shoulder_cm":36,"sleeve_cm":12,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"17.5-22.5 kg","height":"115-125 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":46,"shoulder_cm":38,"sleeve_cm":12.5,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"22.5-27.5 kg","height":"125-135 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":50,"shoulder_cm":40,"sleeve_cm":13,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"135-145 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":53,"shoulder_cm":42,"sleeve_cm":13.5,"pant_cm":0},
  {"audience":"child","role":"Child Top","garment":"Top","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"145-155 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":56,"shoulder_cm":44,"sleeve_cm":14,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"S/160","picker_label":"Adult S","sku_suffix":"S","age":"—","weight":"45-52.5 kg","height":"160-165 cm","chest_cm":92,"hip_cm":92,"waist_cm":80,"length_cm":61,"shoulder_cm":46,"sleeve_cm":19,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"M/165","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"52.5-57.5 kg","height":"165-170 cm","chest_cm":96,"hip_cm":96,"waist_cm":84,"length_cm":64,"shoulder_cm":50,"sleeve_cm":20,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"L/170","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"57.5-65 kg","height":"170-175 cm","chest_cm":100,"hip_cm":100,"waist_cm":88,"length_cm":67,"shoulder_cm":51,"sleeve_cm":20.5,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"XL/175","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"65-72.5 kg","height":"175-180 cm","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":69,"shoulder_cm":52,"sleeve_cm":20.5,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"2XL/180","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"72.5-80 kg","height":"180-185 cm","chest_cm":112,"hip_cm":112,"waist_cm":100,"length_cm":71,"shoulder_cm":53,"sleeve_cm":21,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"3XL/185","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"80-90 kg","height":"185-190 cm","chest_cm":116,"hip_cm":116,"waist_cm":104,"length_cm":73,"shoulder_cm":54,"sleeve_cm":21.5,"pant_cm":0},
  {"audience":"adult","role":"Adult Top","garment":"Top","vendor_label":"4XL/190","picker_label":"Adult 4XL","sku_suffix":"4XL","age":"—","weight":"90-100 kg","height":"190-195 cm","chest_cm":120,"hip_cm":120,"waist_cm":108,"length_cm":75,"shoulder_cm":55,"sleeve_cm":22,"pant_cm":0}
]
JSON
)

SIZE_METAOBJECT_MAP_JSON=$(cat <<'JSON'
[
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
  {"picker_label":"Adult 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult 4XL","gid":"gid://shopify/Metaobject/139840716897","catalog_label":"4XL","source_handle":"shopify--size metaobjects"}
]
JSON
)

mkdir -p "${ROOT}/ops/listings" "/Users/fsuels/Projects/dresslikemommy/uploads/black-white-spelling-family-matching-tops"

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

root = Path(settings["root"])
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
    response = requests.post(
        api,
        headers=headers,
        json={"query": query, "variables": variables or {}},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("errors"):
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], ensure_ascii=False)}")
    return data


def compare_at(price_text):
    price = float(price_text)
    value = price * 1.15
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


def metric_cell(text, unit):
    text = str(text or "").strip()
    if not text or text in {"—", "-", "--"}:
        return "—"
    suffix = f" {unit}"
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


def cm_cell(value):
    if value in (None, "", 0):
        return "—"
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
        ... on TaxonomyCategory {
          id
          fullName
          isLeaf
        }
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
    raise RuntimeError(
        "Taxonomy guard failed: "
        + json.dumps(taxonomy_node, ensure_ascii=False)
    )

role_tokens = {
    "Child Top": "KID",
    "Adult Top": "ADT",
}
size_tokens = {
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

required_fields = [
    "audience",
    "role",
    "garment",
    "vendor_label",
    "picker_label",
    "sku_suffix",
    "age",
    "weight",
    "height",
    "chest_cm",
    "hip_cm",
    "waist_cm",
    "length_cm",
    "pant_cm",
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

if errors:
    raise RuntimeError("Preflight failed:\n- " + "\n- ".join(errors))


def sku_for(row):
    return f"DLM-{settings['shortcode']}-{role_tokens[row['role']]}-{size_tokens[row['picker_label']]}-{settings['color_token']}"


size_values = [{"name": row["picker_label"]} for row in size_chart]
option_axes = [
    {"name": "Size", "values": [value["name"] for value in size_values]},
    {"name": "Color", "values": [settings["color_name"]]},
]
product_options = [
    {"name": axis["name"], "values": [{"name": value} for value in axis["values"]]}
    for axis in option_axes
]

variants = []
recap = []
for row in size_chart:
    price = child_price if row["audience"] == "child" else adult_price
    compare = child_compare if row["audience"] == "child" else adult_compare
    sku = sku_for(row)
    option_values = [row["picker_label"], settings["color_name"]]
    variants.append(
        {
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {
                "sku": sku,
                "tracked": True,
                "requiresShipping": True,
            },
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
            "shopify_size_gid": size_map.get(row["picker_label"], {}).get("gid", ""),
            "catalog_label": size_map.get(row["picker_label"], {}).get("catalog_label", "no catalog match"),
        }
    )

derived_skus = sorted(item["inventoryItem"]["sku"] for item in variants)

size_phrase = "Child 2Y-9-10Y and Adult S-4XL"
size_range_copy = "Children 2Y through 9-10Y and adults S through 4XL"

table_rows = []
for row in size_chart:
    table_rows.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(metric_cell(row['weight'], 'kg'))}</td>"
        f"<td>{html.escape(metric_cell(row['height'], 'cm'))}</td>"
        f"<td>{cm_cell(row['chest_cm'])}</td>"
        f"<td>{cm_cell(row.get('sleeve_cm', 0))}</td>"
        f"<td>{cm_cell(row['pant_cm'])}</td>"
        f"<td>{cm_cell(row['hip_cm'])}</td>"
        f"<td>{cm_cell(row['waist_cm'])}</td>"
        f"<td>{cm_cell(row['length_cm'])}</td>"
        "</tr>"
    )

body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Soft knit tee fabric based on the supplied photos; no exact fiber content was available from the blocked vendor page.</li>",
        "<li><strong>Family story:</strong> A playful matching raglan tee for parents and kids, made for casual family photos, vacation walks, birthdays, and everyday twinning.</li>",
        "<li><strong>Print reference:</strong> Black and White Spelling pairs a white tee body with black raglan sleeves and a soft pink heart-style graphic.</li>",
        "<li><strong>Design details:</strong> Short raglan sleeves, contrast neck trim, relaxed tee shape, adult letter graphics, and a child heart graphic. The shorts, books, and sneakers shown in the photo are styling only and not included.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, turn inside out, line dry or tumble low, and avoid bleach. This care line is a conservative inference because the blocked vendor page did not expose wash instructions.</li>",
        f"<li><strong>Size range:</strong> {size_range_copy}.</li>",
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
        "      <th>Sleeve / Skirt (cm)</th>",
        "      <th>Pant / Short (cm)</th>",
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
        "<p>Black and White Spelling keeps matching family style easy and bright with one relaxed tee silhouette across kids and adults. The black raglan sleeves, white body, and soft pink heart-style artwork make the set feel coordinated without being too formal.</p>",
        "",
        "<p>The attached chart publishes top measurements for child sizes 90-150 and adult sizes S-4XL. The supplied image shows tops only, and the shorts, books, and sneakers are styling only. The published variants therefore stay tightly tied to the vendor-backed top rows.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Coordinated raglan tee:</strong> Matching short-sleeve top for kids and adults in the same black, white, and pink palette.</li>",
        "<li><strong>Family-friendly graphics:</strong> Adult shirts carry letter artwork while the child top has a bold heart graphic for a sweet matching moment.</li>",
        "<li><strong>Easy warm-weather styling:</strong> The relaxed tee shape pairs naturally with shorts, jeans, skirts, or casual vacation outfits.</li>",
        "<li><strong>Wide adult size range:</strong> Adult sizing runs from S through 4XL based on the attached chart.</li>",
        "<li><strong>Honest single-garment scope:</strong> This listing covers the tops only; shorts, jeans, hats, and accessories are not included.</li>",
        "</ul>",
        "",
        "<p>Choose the sizes you need and build a casual matching family tee look for photos, trips, and everyday plans together.</p>",
    ]
)

tags = sorted(
    {
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Tops",
        "T-Shirts",
        "Matching Family Tops",
        "Matching Family T-Shirts",
        "Matching Family Outfits",
        "Raglan Tee",
        "Short Sleeve Top",
        "Letter Graphic",
        "Heart Graphic",
        "Black and White Spelling",
        "Black",
        "White",
        "Pink",
        "Black Sleeves",
        "Summer",
        "Vacation",
        "Family Photos",
        "Adult S",
        "Adult M",
        "Adult L",
        "Adult XL",
        "Adult 2XL",
        "Adult 3XL",
        "Adult 4XL",
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
        handle
        title
        options {
          name
          position
          values
        }
        variants(first: 100) {
          nodes {
            id
            sku
            price
            compareAtPrice
            inventoryPolicy
            selectedOptions {
              name
              value
            }
            inventoryItem {
              tracked
              requiresShipping
            }
          }
        }
        media(first: 50) {
          nodes {
            ... on MediaImage {
              id
              alt
              image {
                url
              }
            }
          }
        }
      }
    }
    """,
    {"handle": settings["handle"]},
)
existing_product = existing_data["data"]["productByHandle"]
product_id = existing_product["id"] if existing_product else ""
create_new_product = not product_id

if create_new_product:
    create_payload = {
        "input": {
            "handle": settings["handle"],
            "title": settings["title"],
            "descriptionHtml": body_html,
            "vendor": settings["vendor"],
            "productType": settings["product_type"],
            "tags": tags,
            "status": "ACTIVE",
            "category": settings["taxonomy_gid"],
            "seo": {
                "title": settings["seo_title"],
                "description": settings["seo_description"],
            },
            "productOptions": product_options,
        }
    }
    create_result = gql(
        """
        mutation ProductCreate($input: ProductInput!) {
          productCreate(input: $input) {
            product {
              id
              handle
              title
            }
            userErrors {
              field
              message
            }
          }
        }
        """,
        create_payload,
    )
    user_errors = create_result["data"]["productCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
    product_id = create_result["data"]["productCreate"]["product"]["id"]

update_result = gql(
    """
    mutation ProductUpdate($product: ProductUpdateInput!) {
      productUpdate(product: $product) {
        product {
          id
          handle
          title
        }
        userErrors {
          field
          message
        }
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
            "status": "ACTIVE",
            "category": settings["taxonomy_gid"],
            "seo": {
                "title": settings["seo_title"],
                "description": settings["seo_description"],
            },
        }
    },
)
if update_result["data"]["productUpdate"]["userErrors"]:
    raise RuntimeError(
        f"productUpdate userErrors: {json.dumps(update_result['data']['productUpdate']['userErrors'], ensure_ascii=False)}"
    )

existing_data = gql(
    """
    query ExistingProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        handle
        options {
          name
          position
          values
        }
        variants(first: 100) {
          nodes {
            id
            sku
            selectedOptions {
              name
              value
            }
          }
        }
        media(first: 50) {
          nodes {
            ... on MediaImage {
              id
              alt
              image {
                url
              }
            }
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
live_option_pairs = {
    tuple(option["value"] for option in variant["selectedOptions"])
    for variant in live_variants
}

if not live_variants or (len(live_variants) == 1 and not live_variants[0]["sku"]):
    create_variants_result = gql(
        """
        mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
          productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
            productVariants {
              id
              sku
              title
            }
            userErrors {
              field
              message
            }
          }
        }
        """,
        {
            "productId": product_id,
            "variants": variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        },
    )
    user_errors = create_variants_result["data"]["productVariantsBulkCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productVariantsBulkCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
else:
    if len(live_variants) != len(size_chart) or live_option_pairs != expected_option_pairs:
        raise RuntimeError(
            "Existing product has unexpected variant shape; refusing to create duplicates.\n"
            + json.dumps(live_variants, ensure_ascii=False, indent=2)
        )
    variant_update_payload = []
    live_by_pair = {
        tuple(option["value"] for option in variant["selectedOptions"]): variant
        for variant in live_variants
    }
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
            productVariants {
              id
              sku
              title
            }
            userErrors {
              field
              message
            }
          }
        }
        """,
        {
            "productId": product_id,
            "variants": variant_update_payload,
        },
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
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Raglan Letter Tee"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Top"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(settings["age_group_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(settings["color_pattern_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps([size_map[row["picker_label"]]["gid"] for row in size_chart if row["picker_label"] in size_map])},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(settings["target_gender_gids"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": settings["seo_title"]},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": settings["seo_description"]},
]

metafields_result = gql(
    """
    mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields {
          namespace
          key
          type
          value
        }
        userErrors {
          field
          message
        }
      }
    }
    """,
    {"metafields": metafields},
)
if metafields_result["data"]["metafieldsSet"]["userErrors"]:
    raise RuntimeError(
        f"metafieldsSet userErrors: {json.dumps(metafields_result['data']['metafieldsSet']['userErrors'], ensure_ascii=False)}"
    )

publish_result = gql(
    """
    mutation PublishablePublish($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) {
        publishable {
          availablePublicationsCount {
            count
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """,
    {
        "id": product_id,
        "input": [{"publicationId": item["publicationId"]} for item in settings["publications"]],
    },
)
if publish_result["data"]["publishablePublish"]["userErrors"]:
    raise RuntimeError(
        f"publishablePublish userErrors: {json.dumps(publish_result['data']['publishablePublish']['userErrors'], ensure_ascii=False)}"
    )

media_lookup = gql(
    """
    query ProductMedia($id: ID!) {
      product(id: $id) {
        media(first: 50) {
          nodes {
            ... on MediaImage {
              id
              alt
              image {
                url
              }
            }
          }
        }
      }
    }
    """,
    {"id": product_id},
)
existing_media = media_lookup["data"]["product"]["media"]["nodes"]
existing_media_alts = {item.get("alt") or "" for item in existing_media}

media_files = sorted(
    [
        path
        for path in upload_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
)

alt_by_name = {
    "look-1.png": "Parents and child wearing the black and white family matching raglan tops.",
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
            stagedTargets {
              url
              resourceUrl
              parameters {
                name
                value
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """,
        {
            "input": [
                {
                    "filename": image_path.name,
                    "mimeType": mime_type,
                    "resource": "IMAGE",
                    "httpMethod": "POST",
                }
            ]
        },
    )
    user_errors = staged_upload["data"]["stagedUploadsCreate"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"stagedUploadsCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
    staged_target = staged_upload["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    form_data = {param["name"]: param["value"] for param in staged_target["parameters"]}
    with image_path.open("rb") as file_handle:
        upload_response = requests.post(
            staged_target["url"],
            data=form_data,
            files={"file": (image_path.name, file_handle, mime_type)},
            timeout=120,
        )
        upload_response.raise_for_status()
    create_media = gql(
        """
        mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media {
              ... on MediaImage {
                id
                alt
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """,
        {
            "productId": product_id,
            "media": [
                {
                    "originalSource": staged_target["resourceUrl"],
                    "mediaContentType": "IMAGE",
                    "alt": alt_text,
                }
            ],
        },
    )
    if create_media["data"]["productCreateMedia"]["userErrors"]:
        raise RuntimeError(
            f"productCreateMedia userErrors: {json.dumps(create_media['data']['productCreateMedia']['userErrors'], ensure_ascii=False)}"
        )

time.sleep(2)

verify_data = gql(
    """
    query VerifyProduct($id: ID!) {
      product(id: $id) {
        id
        title
        handle
        status
        publishedAt
        onlineStoreUrl
        tags
        descriptionHtml
        seo {
          title
          description
        }
        options {
          name
          position
          values
        }
        category {
          id
          fullName
        }
        variants(first: 100) {
          nodes {
            sku
            title
            price
            compareAtPrice
            inventoryPolicy
            selectedOptions {
              name
              value
            }
            inventoryItem {
              tracked
              requiresShipping
            }
          }
        }
        media(first: 50) {
          nodes {
            ... on MediaImage {
              alt
              image {
                url
              }
            }
          }
        }
        collections(first: 50) {
          nodes {
            title
            handle
            ruleSet {
              appliedDisjunctively
              rules {
                column
                relation
                condition
              }
            }
          }
        }
        metafields(first: 100) {
          nodes {
            namespace
            key
            type
            value
          }
        }
        resourcePublicationsV2(first: 20) {
          nodes {
            isPublished
            publishDate
            publication {
              id
              name
            }
          }
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
row_cells = [
    [re.sub(r"<[^>]+>", "", cell).strip() for cell in re.findall(r"<td>(.*?)</td>", row_html, re.S)]
    for row_html in tbody_rows
]
first_cells = [cells[0] for cells in row_cells if cells]

live_skus = sorted(variant["sku"] for variant in product["variants"]["nodes"])
variant_checks = []
for variant in product["variants"]["nodes"]:
    expected = next(item for item in recap if item["sku"] == variant["sku"])
    variant_checks.append(
        variant["price"] == expected["price"]
        and variant["compareAtPrice"] == expected["compare_at_price"]
        and variant["inventoryPolicy"] == "DENY"
        and variant["inventoryItem"]["tracked"] is True
        and variant["inventoryItem"]["requiresShipping"] is True
    )

written_metafields = {f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"]}
expected_metafields = {
    "custom.category1",
    "custom.subcategory",
    "custom.subcategory2",
    "custom.pattern",
    "custom.style",
    "custom.type",
    "mm-google-shopping.custom_product",
    "mm-google-shopping.gender",
    "mm-google-shopping.age_group",
    "mm-google-shopping.condition",
    "mm-google-shopping.custom_label_0",
    "mm-google-shopping.custom_label_1",
    "mm-google-shopping.custom_label_2",
    "mm-google-shopping.custom_label_3",
    "mm-google-shopping.custom_label_4",
    "shopify.age-group",
    "shopify.color-pattern",
    "shopify.size",
    "shopify.target-gender",
    "global.title_tag",
    "global.description_tag",
}

publication_map = {
    node["publication"]["id"]: node
    for node in product["resourcePublicationsV2"]["nodes"]
}
all_publications_ok = all(
    publication_map.get(item["publicationId"], {}).get("isPublished") is True
    for item in settings["publications"]
)

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
    ("Published to all required channels", all_publications_ok, "all 5 target publications live" if all_publications_ok else "missing publication"),
    ("publishedAt not null", bool(product["publishedAt"]), product["publishedAt"] or "missing"),
    ("onlineStoreUrl populated", bool(product["onlineStoreUrl"]), product["onlineStoreUrl"] or "missing"),
    ("Taxonomy category set", (product["category"] or {}).get("id") == settings["taxonomy_gid"], (product["category"] or {}).get("id") or "missing"),
    ("Size-chart table has 10 columns", thead_count == 10, str(thead_count)),
    ("Size-chart table row count matches SIZE_CHART", len(tbody_rows) == len(size_chart), str(len(tbody_rows))),
    ("Picker labels match first size-table column", picker_ok, "exact order match" if picker_ok else "mismatch"),
    ("Size-chart cells use one unit at a time", single_unit_cells_ok, "no slash-separated values in table cells" if single_unit_cells_ok else "found dual-unit cell"),
    ("Required tags present", required_tags_ok, "all required tags present" if required_tags_ok else "missing required tags"),
    ("Applicable metafields written", expected_metafields.issubset(written_metafields), "all expected metafields present" if expected_metafields.issubset(written_metafields) else "missing metafields"),
  ]

failures = [row for row in verification_rows if not row[1]]
if failures:
    raise RuntimeError("Verification failed:\n- " + "\n- ".join(f"{label}: {detail}" for label, _, detail in failures))

product_numeric_id = product["id"].split("/")[-1]
admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_numeric_id}"
live_url = product["onlineStoreUrl"] or f"https://www.dresslikemommy.com/products/{settings['handle']}"

with csv_header_source.open("r", encoding="utf-8", newline="") as handle:
    reader = csv.reader(handle)
    csv_header = next(reader)

rows = []
media_nodes = product["media"]["nodes"]
size_csv = ", ".join(row["picker_label"] for row in size_chart)
for index, row in enumerate(recap, start=1):
    record = {column: "" for column in csv_header}
    record["Handle"] = settings["handle"]
    record["Title"] = settings["title"]
    record["Body (HTML)"] = body_html
    record["Vendor"] = settings["vendor"]
    record["Product Category"] = settings["taxonomy_path"]
    record["Type"] = settings["product_type"]
    record["Tags"] = ", ".join(tags)
    record["Published"] = "TRUE"
    record["Option1 Name"] = "Size"
    record["Option1 Value"] = row["picker_label"]
    record["Option2 Name"] = "Color"
    record["Option2 Value"] = settings["color_name"]
    record["Variant SKU"] = row["sku"]
    record["Variant Inventory Tracker"] = "shopify"
    record["Variant Inventory Policy"] = "deny"
    record["Variant Fulfillment Service"] = "manual"
    record["Variant Price"] = row["price"]
    record["Variant Compare At Price"] = row["compare_at_price"]
    record["Variant Requires Shipping"] = "TRUE"
    record["Variant Taxable"] = "TRUE"
    record["Gift Card"] = "FALSE"
    record["SEO Title"] = settings["seo_title"]
    record["SEO Description"] = settings["seo_description"]
    record["Google Shopping / Google Product Category"] = settings["google_product_category"]
    record["Google Shopping / Gender"] = "unisex"
    record["Google Shopping / Age Group"] = "adult"
    record["Google Shopping / MPN"] = row["sku"]
    record["Google Shopping / Condition"] = "new"
    record["Google Shopping / Custom Product"] = "FALSE"
    record["Google Shopping / Custom Label 0"] = "Family Matching"
    record["Google Shopping / Custom Label 1"] = settings["print_name"]
    record["Google Shopping / Custom Label 2"] = settings["season"]
    record["Google Shopping / Custom Label 3"] = "Raglan Letter Tee"
    record["Google Shopping / Custom Label 4"] = "Unisex Family Top"
    record["Category1 (product.metafields.custom.category1)"] = "Family Matching"
    record["Pattern (product.metafields.custom.pattern)"] = settings["print_name"]
    record["Style (product.metafields.custom.style)"] = settings["merch_style"]
    record["SubCategory (product.metafields.custom.subcategory)"] = settings["merch_subcategory"]
    record["SubCategory2 (product.metafields.custom.subcategory2)"] = settings["merch_subcategory2"]
    record["Type (product.metafields.custom.type)"] = settings["merch_type"]
    record["Google: Custom Product (product.metafields.mm-google-shopping.custom_product)"] = "FALSE"
    record["Age group (product.metafields.shopify.age-group)"] = "kids, adults"
    record["Color (product.metafields.shopify.color-pattern)"] = "Black, White, Pink"
    record["Size (product.metafields.shopify.size)"] = size_csv
    record["Status"] = "active"
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

sales_channels = []
for publication in settings["publications"]:
    live_publication = publication_map[publication["publicationId"]]
    sales_channels.append(
        f"- {publication['name']} - `{publication['publicationId']}` ({live_publication.get('publishDate') or 'date unavailable'})"
    )

smart_collections = [
    node for node in product["collections"]["nodes"] if node.get("ruleSet") is not None
]
smart_collection_lines = [f"- {node['title']} (`/{node['handle']}`)" for node in smart_collections]
if not smart_collection_lines:
    smart_collection_lines = ["- None returned immediately; rerun later if Shopify collection indexing is still catching up."]

fit_report_lines = [
    f"- {row['role']}: {row['height_cm']} cm / {row['weight_jin']} jin tried `{row['tried_size']}` - {row['note']}"
    for row in settings["fit_report"]
]

skipped_metafields = [
    ("shopify.clothing-features", "No honest standard clothing-features entry is needed for this black and white family top."),
    ("shopify.fit", "A reliable writable standard Shopify fit metafield definition was not available in this store for this top taxonomy."),
    ("shopify.fabric", "Not written because the source supports only a soft knit tee appearance, not an exact fiber metaobject."),
    ("shopify.neckline", "Not written because the photos show contrast crew trim, but no verified standard catalog GID was confirmed in this store."),
    ("shopify.sleeve-length-type", "Not written because the product is short sleeved, but no verified standard Shopify metaobject GID for that value was confirmed in this store."),
    ("shopify.top-length-type", "Not written because the chart provides garment length but not enough evidence to map this top to one precise standard top-length metaobject."),
    ("shopify.skirt-dress-length-type", "Not applicable because the honest taxonomy is Clothing Tops > T-Shirts."),
    ("shopify.dress-occasion", "Not applicable because the honest taxonomy is Clothing Tops > T-Shirts."),
    ("shopify.dress-style", "Not applicable because the honest taxonomy is Clothing Tops > T-Shirts.")
]

size_recap_lines = [
    f"| {row['vendor_label']} | {row['picker_label']} | {row['sku']} | ${row['price']} | {row['shopify_size_gid']} ({row['catalog_label']}) |"
    for row in recap
]

tag_line = "`" + ", ".join(tags) + "`"

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
    "- mm-google-shopping.custom_label_3 = `Raglan Letter Tee`",
    "- mm-google-shopping.custom_label_4 = `Unisex Family Top`",
    "- shopify.age-group -> `Kids`, `Adults`",
    "- shopify.color-pattern -> `Black`, `White`, `Pink`",
    "- shopify.size -> 14 catalog metaobject references in chart order",
    "- shopify.target-gender -> `Unisex`",
    "- global.title_tag = SEO title",
    "- global.description_tag = SEO description",
]

verification_lines = [
    f"| {label} | {'PASS' if result else 'FAIL'} | {detail} |"
    for label, result, detail in verification_rows
]

listing_md = "\n".join(
    [
        f"# {settings['title']}",
        "",
        "**Status:** Live (ACTIVE, published to all 5 required sales channels)",
        f"**Admin URL:** {admin_url}",
        f"**Live URL:** {live_url}",
        f"**Product ID:** {product['id']}",
        f"**Handle:** {settings['handle']}",
        f"**Vendor (storefront):** {settings['vendor']}",
        f"**Vendor source URL (tags only):** {settings['vendor_url']}",
        "",
        "## Request resolution",
        "| Input | Resolved |",
        "|---|---|",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | Tops -> T-Shirts taxonomy leaf (live taxonomy correction) |",
        "| Variant model | Size / Color with `Child ...` and `Adult ...` labels |",
        "| FORCE_SPEC_PRICES | true |",
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
        f"- Direct HTTP fetch of `{settings['vendor_url']}` returned 1688 anti-bot/login markup, so the attached size chart plus supplied product images were treated as the authoritative source of truth.",
        f"- **Photo-only fabric/color evidence:** {settings['product_info']['evidence']} The fabric copy is `{settings['product_info']['fabric_en']}` and the color story is `{settings['product_info']['color_en']}`.",
        "- **Size-chart source of truth:** the attached size-chart screenshot. The supported top rows were transcribed from the child and adult top tables.",
        "- **Rows excluded from variants:** none; every visible row in the attached top size chart is included.",
        "- **Chart columns preserved from the source:** Size, Garment Length, Chest, Shoulder, Sleeve, Recommended Height, Recommended Weight.",
        "- Source `推荐体重` values are shown as domestic jin ranges in the image and were converted to kg for the shopper-facing table.",
        "- `hip_cm` and `waist_cm` were derived because the vendor chart omits both values:",
        "  child rows use `hip = chest + 4` and `waist = chest`; adult rows use `hip = chest` and `waist = chest - 12`.",
        "- Sleeve values are direct from the vendor chart. Pant/short cells are rendered as `—` because this listing covers tops only.",
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
        "- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the live listing uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.",
        "- The supplied photo shows short-sleeve raglan tops with shorts, books, and sneakers. Because the chart only measures the tops, those styling items are not listed as included pieces.",
        "- `150` maps to `Child 9-10 Years` and uses the closest honest live `shopify.size` metaobject label `10`.",
        "- Adult `2XL/180` through `4XL/190` were kept because the vendor chart explicitly publishes them.",
        f"- Price pattern uses the canonical Tops fallback matrix because no reliable modern Family Matching Tops neighbor matched this source; child variants are `{child_price}` and adult variants are `{adult_price}`.",
        "",
        "## Tags written",
        tag_line,
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
        "## Sales channels published",
        *sales_channels,
        "",
        "## Smart collections",
        *smart_collection_lines,
        "",
        "## Manual follow-ups",
        "- Inventory quantities and per-variant grams remain unset / zero and still need operator stock values.",
        "- If the vendor page becomes directly readable later, confirm whether the offer is truly top-only or includes any extra coordinated pieces; the current copy treats the shorts, books, and sneakers shown in the photo as styling only.",
        "- If later source material exposes direct waist, hip, or exact fabric-composition specs, replace the current derived fields or broad soft-knit copy with the exact vendor evidence.",
        "",
        "## Files",
        f"- `{listing_md_path}`",
        f"- `{csv_out_path}`",
        f"- `{verify_json_path}`",
        f"- `{size_chart_out_path}`",
        f"- `{body_html_out_path}`",
        f"- `{settings['script_path']}`",
    ]
)

listing_md_path.write_text(listing_md + "\n", encoding="utf-8")
print(json.dumps({"admin_url": admin_url, "live_url": live_url, "product_gid": product["id"]}, ensure_ascii=False))
PY
