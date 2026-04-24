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
  "handle": "denim-blue-family-matching-set",
  "title": "Denim Blue Family Matching Set - Short-Sleeve Shirt and Shorts",
  "seo_title": "Denim Shirt and Shorts Family Set | Dress Like Mommy",
  "seo_description": "Relaxed denim family matching shirt-and-shorts set for moms, dads, girls and boys. Sizes Child 1-2Y-8Y and Adult S-3XL in denim blue.",
  "print_name": "Denim Blue",
  "shortcode": "DNBL",
  "color_token": "DENIM",
  "color_name": "Denim Blue",
  "listing_mode": "Family Matching",
  "category": "FamilySet",
  "category_word": "Set",
  "product_type": "Matching Family Sets",
  "custom_type": "Two-Piece Set",
  "taxonomy_gid": "gid://shopify/TaxonomyCategory/aa-1-11",
  "expected_taxonomy_full_name": "Apparel & Accessories > Clothing > Outfit Sets",
  "taxonomy_path": "Apparel & Accessories > Clothing > Outfit Sets",
  "google_product_category": "Apparel & Accessories > Clothing > Outfit Sets",
  "merch_subcategory": "Set",
  "merch_subcategory2": "Summer Family Matching Set",
  "merch_style": "Matching Family Set",
  "merch_type": "Two-Piece Set",
  "season": "Summer",
  "vendor_url": "https://detail.1688.com/offer/708209996925.html",
  "vendor": "dresslikemommy.com",
  "force_spec_prices": true,
  "child_price": "28.99",
  "adult_price": "31.99",
  "price_neighbor_handle": "trail-plaid-family-matching-set",
  "size_neighbor_handle": "shopify--size metaobjects",
  "script_path": "/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-dnbl-denim-blue-family-matching-set.sh",
  "upload_dir": "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set",
  "listing_md": "/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-set-listing.md",
  "csv_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/denim-blue-family-matching-set-shopify-import.csv",
  "verify_json_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-denim-blue-family-matching-set.json",
  "size_chart_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-denim-blue-family-matching-set.json",
  "body_html_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/body-denim-blue-family-matching-set.html",
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
    "gid://shopify/Metaobject/69639766113"
  ],
  "fabric_gids": [
    "gid://shopify/Metaobject/69669748833"
  ],
  "target_gender_gids": [
    "gid://shopify/Metaobject/129972502625"
  ],
  "product_info": {
    "vendor_item": "23B007",
    "fabric_cn": "牛仔",
    "fabric_en": "Denim",
    "color_cn": "牛仔蓝",
    "color_en": "Denim Blue"
  },
  "fit_report": [
    {"role": "Boy", "height_cm": 115, "weight_jin": 40, "tried_size": "120", "note": "Loose fit"},
    {"role": "Girl", "height_cm": 113, "weight_jin": 35, "tried_size": "120", "note": "Loose fit"},
    {"role": "Mom", "height_cm": 164, "weight_jin": 88, "tried_size": "S", "note": "Loose fit"},
    {"role": "Dad", "height_cm": 182, "weight_jin": 146, "tried_size": "3XL", "note": "Loose fit"}
  ],
  "product_image_sources": [
    "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set/look-1.png",
    "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set/look-2.png"
  ],
  "size_chart_source": "/Users/fsuels/Desktop/Screenshot 2026-04-24 at 12.12.38 AM.png",
  "required_tags": [
    "Family Matching",
    "Sets",
    "Matching Family Set",
    "Denim",
    "Denim Blue",
    "Button-Up Shirt",
    "Shirt and Shorts Set",
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
    "https://detail.1688.com/offer/708209996925.html"
  ]
}
JSON
)

SIZE_CHART_JSON=$(cat <<'JSON'
[
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":74,"hip_cm":78,"waist_cm":34,"length_cm":38,"shoulder_cm":34,"pant_cm":29,"rise_cm":23},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":78,"hip_cm":82,"waist_cm":36,"length_cm":41,"shoulder_cm":36,"pant_cm":30,"rise_cm":23.5},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":82,"hip_cm":86,"waist_cm":38,"length_cm":44,"shoulder_cm":38,"pant_cm":31,"rise_cm":24},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":86,"hip_cm":90,"waist_cm":40,"length_cm":47,"shoulder_cm":40,"pant_cm":33,"rise_cm":25},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":90,"hip_cm":94,"waist_cm":42,"length_cm":50,"shoulder_cm":42,"pant_cm":36,"rise_cm":26},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":94,"hip_cm":98,"waist_cm":44,"length_cm":53,"shoulder_cm":43,"pant_cm":38,"rise_cm":27},
  {"audience":"child","role":"Child Set","garment":"Shirt and Shorts Set","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":98,"hip_cm":102,"waist_cm":46,"length_cm":56,"shoulder_cm":45,"pant_cm":40,"rise_cm":28},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"—","weight":"47.5-52.5 kg","height":"155-165 cm","chest_cm":110,"hip_cm":110,"waist_cm":50,"length_cm":65,"shoulder_cm":51,"pant_cm":50,"rise_cm":30},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"53-57.5 kg","height":"160-170 cm","chest_cm":112,"hip_cm":112,"waist_cm":54,"length_cm":67,"shoulder_cm":52,"pant_cm":50.5,"rise_cm":30.5},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"58-65 kg","height":"165-175 cm","chest_cm":114,"hip_cm":114,"waist_cm":58,"length_cm":69,"shoulder_cm":54,"pant_cm":52,"rise_cm":31},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"65.5-72.5 kg","height":"170-180 cm","chest_cm":118,"hip_cm":118,"waist_cm":60,"length_cm":71,"shoulder_cm":55,"pant_cm":52,"rise_cm":32},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"XXL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"73-80 kg","height":"175-185 cm","chest_cm":122,"hip_cm":122,"waist_cm":62,"length_cm":74,"shoulder_cm":57,"pant_cm":53,"rise_cm":33},
  {"audience":"adult","role":"Adult Set","garment":"Shirt and Shorts Set","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"80.5-90 kg","height":"180-190 cm","chest_cm":126,"hip_cm":126,"waist_cm":66,"length_cm":76,"shoulder_cm":59,"pant_cm":54,"rise_cm":33}
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
  {"picker_label":"Adult S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Adult 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"shopify--size metaobjects"}
]
JSON
)

mkdir -p "${ROOT}/ops/listings" "/Users/fsuels/Projects/dresslikemommy/uploads/denim-blue-family-matching-set"

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
    "Child Set": "KID",
    "Adult Set": "ADT",
}
size_tokens = {
    "Child 1-2 Years": "KID12Y",
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Adult S": "S",
    "Adult M": "M",
    "Adult L": "L",
    "Adult XL": "XL",
    "Adult 2XL": "2XL",
    "Adult 3XL": "3XL",
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
    if row.get("picker_label") not in size_map:
        errors.append(f"missing size metaobject mapping for {row.get('picker_label')}")
    if row.get("shoulder_cm") in (None, ""):
        errors.append(f"row {row.get('vendor_label')} missing shoulder_cm")

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
            "shopify_size_gid": size_map[row["picker_label"]]["gid"],
            "catalog_label": size_map[row["picker_label"]]["catalog_label"],
        }
    )

derived_skus = sorted(item["inventoryItem"]["sku"] for item in variants)

size_phrase = "Child 1-2Y-8Y and Adult S-3XL"
size_range_copy = "Children 1-2Y through 8Y and adults S through 3XL"

table_rows = []
for row in size_chart:
    table_rows.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(metric_cell(row['weight'], 'kg'))}</td>"
        f"<td>{html.escape(metric_cell(row['height'], 'cm'))}</td>"
        f"<td>{cm_cell(row['chest_cm'])}</td>"
        f"<td>{cm_cell(row['shoulder_cm'])}</td>"
        f"<td>{cm_cell(row['pant_cm'])}</td>"
        f"<td>{cm_cell(row['hip_cm'])}</td>"
        f"<td>{cm_cell(row['waist_cm'])}</td>"
        f"<td>{cm_cell(row['length_cm'])}</td>"
        "</tr>"
    )

body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> The attached product-info panel confirms denim fabric in a denim-blue wash, giving this set a structured yet easy everyday feel.</li>",
        "<li><strong>Family story:</strong> A relaxed matching set for moms, dads, girls, and boys built around one coordinated short-sleeve shirt-and-shorts silhouette.</li>",
        "<li><strong>Print reference:</strong> Denim Blue keeps the look clean and versatile, with contrast stitching that helps the set read photo-ready without feeling fussy.</li>",
        "<li><strong>Design details:</strong> Short-sleeve button-up shirt, roomy fit, contrast topstitching, patch-pocket detailing, and matching pull-on shorts. The white tee shown in the photos is styling only and is not included.</li>",
        "<li><strong>Care:</strong> Machine wash cold, turn inside out, line dry or tumble low, and avoid bleach. This care line is a conservative inference because the blocked vendor page did not expose wash instructions.</li>",
        f"<li><strong>Size range:</strong> {size_range_copy}.</li>",
        "</ul>",
        "",
        "<h3>Size Chart</h3>",
        "<table id=\"size-chart\">",
        "  <thead>",
        "    <tr>",
        "      <th>Size</th>",
        "      <th>Age</th>",
        "      <th>Weight (kg/lbs)</th>",
        "      <th>Height (cm/in)</th>",
        "      <th>Chest/Bust (cm/in)</th>",
        "      <th>Shoulder (cm/in)</th>",
        "      <th>Pant/Short Length (cm/in)</th>",
        "      <th>Hip (cm/in)</th>",
        "      <th>Waist (cm/in)</th>",
        "      <th>Garment Length (cm/in)</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        *table_rows,
        "  </tbody>",
        "</table>",
        "",
        "<p>Denim Blue is a clean, easy family look built around one short-sleeve shirt-and-shorts silhouette for both kids and adults. The deep blue wash, oversized patch pockets, and contrast stitching give the set a laid-back denim feel that works for everyday errands, vacation days, and casual photo moments. It reads coordinated without looking too dressy, which makes it useful for families who want one outfit everyone can wear together.</p>",
        "",
        "<p>The vendor chart publishes one child ladder and one adult ladder rather than splitting the product into separate mom, dad, girl, and boy tables, so this listing keeps the variant structure honest with Child and Adult size labels instead of inventing extra role-specific rows. Shirt length, chest, shoulder, shorts length, waist, and rise all come from the attached chart, while hip was derived because the source omitted it. The attached fit report supports the relaxed shape across the family: child 120 fit both the boy and girl testers loosely, mom wore S loosely, and dad wore 3XL loosely.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>One coordinated family silhouette:</strong> Matching shirt-and-shorts set for kids and adults in the same denim-blue story.</li>",
        "<li><strong>Contrast-stitch finish:</strong> Visible topstitching and pocket detail add structure and help the set photograph well.</li>",
        "<li><strong>Easy warm-weather shape:</strong> Short sleeves and shorts keep the set practical for summer travel, theme parks, brunches, and family photos.</li>",
        "<li><strong>Relaxed fit evidence:</strong> The attached fit report shows the published try-on sizes wearing with a loose, easy shape.</li>",
        "<li><strong>Honest two-piece scope:</strong> This listing covers the denim shirt and matching shorts only; the white tee shown in the photos is not included.</li>",
        "</ul>",
        "",
        "<p>Choose each size you need to build a relaxed family set that keeps everyone coordinated for sunny outings, travel days, and easy picture moments.</p>",
    ]
)

tags = sorted(
    {
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Sets",
        "Matching Family Set",
        "Matching Family Outfits",
        "Summer Family Matching Set",
        "Shirt and Shorts Set",
        "Denim",
        "Denim Blue",
        "Blue",
        "Button-Up Shirt",
        "Short Sleeve Shirt",
        "Matching Shorts",
        "Contrast Stitch",
        "Relaxed Fit",
        "Vacation",
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
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Short-Sleeve Shirt and Shorts"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Set"},
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
    "look-1.png": "Family wearing the denim blue family matching short-sleeve shirt and shorts set outdoors.",
    "look-2.png": "Kids wearing the denim blue family matching short-sleeve shirt and shorts set with contrast stitching.",
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
    "shopify.fabric",
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
    record["Google Shopping / Custom Label 3"] = "Short-Sleeve Shirt and Shorts"
    record["Google Shopping / Custom Label 4"] = "Unisex Family Set"
    record["Category1 (product.metafields.custom.category1)"] = "Family Matching"
    record["Pattern (product.metafields.custom.pattern)"] = settings["print_name"]
    record["Style (product.metafields.custom.style)"] = settings["merch_style"]
    record["SubCategory (product.metafields.custom.subcategory)"] = settings["merch_subcategory"]
    record["SubCategory2 (product.metafields.custom.subcategory2)"] = settings["merch_subcategory2"]
    record["Type (product.metafields.custom.type)"] = settings["merch_type"]
    record["Google: Custom Product (product.metafields.mm-google-shopping.custom_product)"] = "FALSE"
    record["Age group (product.metafields.shopify.age-group)"] = "kids, adults"
    record["Color (product.metafields.shopify.color-pattern)"] = "Blue"
    record["Fabric (product.metafields.shopify.fabric)"] = "Denim"
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
    ("shopify.clothing-features", "No honest standard clothing-features entry is needed for this denim shirt-and-shorts set."),
    ("shopify.fit", "The Outfit Sets taxonomy exposes fit, but no reliable writable standard Shopify metafield definition is available in this store."),
    ("shopify.neckline", "Not written because this is an Outfit Sets listing, not a neckline-specific dress or top listing."),
    ("shopify.sleeve-length-type", "Not written because the vendor chart does not publish sleeve length and the Outfit Sets subtype is stricter than the photo evidence alone."),
    ("shopify.skirt-dress-length-type", "Not written because the product is a shirt-and-shorts set, not a skirt or dress listing."),
    ("shopify.dress-occasion", "Not applicable because the honest taxonomy is Outfit Sets."),
    ("shopify.dress-style", "Not applicable because the honest taxonomy is Outfit Sets.")
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
    "- mm-google-shopping.custom_label_3 = `Short-Sleeve Shirt and Shorts`",
    "- mm-google-shopping.custom_label_4 = `Unisex Family Set`",
    "- shopify.age-group -> `Kids`, `Adults`",
    "- shopify.color-pattern -> `Blue`",
    "- shopify.fabric -> `Denim`",
    "- shopify.size -> 13 catalog metaobject references in chart order",
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
        f"- **Product info recovered from the attached screenshot:** vendor item `{settings['product_info']['vendor_item']}`, fabric `{settings['product_info']['fabric_cn']}` ({settings['product_info']['fabric_en']}), color `{settings['product_info']['color_cn']}` ({settings['product_info']['color_en']}).",
        "- **Size-chart source of truth:** the attached size-chart screenshot. All 13 vendor rows were transcribed directly from that image.",
        "- **Chart columns preserved from the source:** Size, Garment Length, Chest*2, Shoulder, Pant/Short Length, Waist*2, Rise/Crotch Depth, Recommended Height, Recommended Weight.",
        "- `chest_cm` values were derived by doubling the source `胸围*2` column to full circumference.",
        "- `waist_cm` values were derived by doubling the source `腰围*2` column to full circumference.",
        "- `hip_cm` was derived because the vendor chart omits hip:",
        "  child rows use `hip = chest + 4`; adult rows use `hip = chest`.",
        "- `rise_cm` from the vendor `档深` column is preserved in the saved size-chart JSON for rerun continuity but intentionally omitted from the shopper table so the storefront keeps the standard 10-column contract.",
        "- Adult height guidance was backfilled from the attached fit report plus the live family-set grading curve because the source chart only publishes adult weight bands.",
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
        "- The vendor chart publishes one child ladder and one adult ladder, not separate girl/boy or mom/dad tables, so the live listing uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.",
        "- `80` maps to `Child 1-2 Years` and uses the closest honest live `shopify.size` metaobject `12-18 months`.",
        "- `XXL` maps to `Adult 2XL` so the live picker stays consistent with the store's standard adult size naming.",
        "- The attached fit report confirms the set wears loosely on both kids and adults, supporting the relaxed merchandising copy.",
        f"- Price pattern was anchored to the live family-set neighbor `{settings['price_neighbor_handle']}`, preserving the current family-set ladder `28.99 / 31.99`.",
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
        "- If the vendor page becomes directly readable later, confirm whether the set includes any extra inner layer beyond the denim shirt and shorts; the current copy assumes the white tee shown in the photos is styling only.",
        "- If later source material exposes a direct hip or fabric-composition spec beyond plain denim, replace the derived hip values or broadened fabric copy with the exact vendor evidence.",
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
