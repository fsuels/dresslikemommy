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

SETTINGS_JSON=$(cat <<'JSON'
{
  "root": "/Users/fsuels/Projects/dresslikemommy",
  "handle": "red-plaid-family-matching-tops",
  "title": "Red Plaid Family Matching Tops - Button-Up Shirt",
  "seo_title": "Red Plaid Family Tops | Dress Like Mommy",
  "seo_description": "Soft woven-look plaid button-up shirts for mom, dad, girls and boys. Sizes children 1-2Y-9-10Y and adults S-3XL.",
  "print_name": "Red Plaid",
  "shortcode": "RPLD",
  "color_token": "RED",
  "color_name": "Red Plaid",
  "listing_mode": "Family Matching",
  "category": "Tops",
  "category_word": "Tops",
  "product_type": "Matching Family Tops",
  "custom_type": "Top",
  "taxonomy_gid": "gid://shopify/TaxonomyCategory/aa-1-13-8",
  "expected_taxonomy_full_name": "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts",
  "merch_subcategory": "Tops",
  "merch_subcategory2": "Matching Family Button-Up Shirts",
  "merch_style": "Plaid Button-Up Shirt",
  "merch_type": "Top",
  "season": "Fall",
  "vendor_url": "https://detail.1688.com/offer/885251894864.html",
  "vendor": "dresslikemommy.com",
  "force_spec_prices": true,
  "child_price": "24.99",
  "adult_price": "28.99",
  "upload_dir": "/Users/fsuels/Projects/dresslikemommy/uploads/red-plaid-family-matching-tops",
  "listing_md": "/Users/fsuels/Projects/dresslikemommy/ops/listings/red-plaid-family-matching-tops-listing.md",
  "csv_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/red-plaid-family-matching-tops-shopify-import.csv",
  "verify_json_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-red-plaid-family-matching-tops.json",
  "size_chart_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-red-plaid-family-matching-tops.json",
  "body_html_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/body-red-plaid-family-matching-tops.html",
  "age_group_gids": ["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"],
  "color_pattern_gids": ["gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/70220546145", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/130283143265"],
  "target_gender_gids": ["gid://shopify/Metaobject/129972502625"],
  "product_image_sources": [
    "/Users/fsuels/Projects/dresslikemommy/uploads/red-plaid-family-matching-tops/look-1.png",
    "/Users/fsuels/Projects/dresslikemommy/uploads/red-plaid-family-matching-tops/look-2.png"
  ],
  "size_chart_source": "/Users/fsuels/Projects/dresslikemommy/uploads/red-plaid-family-matching-tops/size-chart.png"
}
JSON
)

SIZE_CHART_JSON=$(cat <<'JSON'
[
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Girl 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":36,"sleeve_cm":28,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Girl 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":39,"sleeve_cm":31,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Girl 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":42,"sleeve_cm":34,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Girl 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":45,"sleeve_cm":37,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Girl 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":48,"sleeve_cm":40,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Girl 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":51,"sleeve_cm":43,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Girl 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":54,"sleeve_cm":46,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Girl 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":94,"hip_cm":98,"waist_cm":94,"length_cm":57,"sleeve_cm":49,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Boy 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":36,"sleeve_cm":28,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Boy 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":39,"sleeve_cm":31,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Boy 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":42,"sleeve_cm":34,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Boy 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":45,"sleeve_cm":37,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Boy 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":48,"sleeve_cm":40,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Boy 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":51,"sleeve_cm":43,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Boy 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":54,"sleeve_cm":46,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Boy 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":94,"hip_cm":98,"waist_cm":94,"length_cm":57,"sleeve_cm":49,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":98,"hip_cm":98,"waist_cm":86,"length_cm":63,"sleeve_cm":53,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":65,"sleeve_cm":54,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":67,"sleeve_cm":55,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":69,"sleeve_cm":56,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"XXL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":71,"sleeve_cm":58,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Mother 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":73,"sleeve_cm":60,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":98,"hip_cm":98,"waist_cm":86,"length_cm":63,"sleeve_cm":53,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":65,"sleeve_cm":54,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":67,"sleeve_cm":55,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":69,"sleeve_cm":56,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XXL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":71,"sleeve_cm":58,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":73,"sleeve_cm":60,"pant_cm":0}
]
JSON
)

SIZE_METAOBJECT_MAP_JSON=$(cat <<'JSON'
[
  {"picker_label":"Girl 1-2 Years","gid":"gid://shopify/Metaobject/129972797537","catalog_label":"12-18 months"},
  {"picker_label":"Girl 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years"},
  {"picker_label":"Girl 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years"},
  {"picker_label":"Girl 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years"},
  {"picker_label":"Girl 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years"},
  {"picker_label":"Girl 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years"},
  {"picker_label":"Girl 8 Years","gid":"gid://shopify/Metaobject/139840356449","catalog_label":"7-8 years"},
  {"picker_label":"Girl 9-10 Years","gid":"gid://shopify/Metaobject/139840389217","catalog_label":"8-9 years closest match"},
  {"picker_label":"Boy 1-2 Years","gid":"gid://shopify/Metaobject/129972797537","catalog_label":"12-18 months"},
  {"picker_label":"Boy 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years"},
  {"picker_label":"Boy 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years"},
  {"picker_label":"Boy 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years"},
  {"picker_label":"Boy 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years"},
  {"picker_label":"Boy 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years"},
  {"picker_label":"Boy 8 Years","gid":"gid://shopify/Metaobject/139840356449","catalog_label":"7-8 years"},
  {"picker_label":"Boy 9-10 Years","gid":"gid://shopify/Metaobject/139840389217","catalog_label":"8-9 years closest match"},
  {"picker_label":"Mother S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S"},
  {"picker_label":"Mother M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M"},
  {"picker_label":"Mother L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L"},
  {"picker_label":"Mother XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL"},
  {"picker_label":"Mother 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL"},
  {"picker_label":"Mother 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL"},
  {"picker_label":"Father S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S"},
  {"picker_label":"Father M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M"},
  {"picker_label":"Father L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L"},
  {"picker_label":"Father XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL"},
  {"picker_label":"Father 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL"},
  {"picker_label":"Father 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL"}
]
JSON
)

export SETTINGS_JSON SIZE_CHART_JSON SIZE_METAOBJECT_MAP_JSON

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

api = f"https://{os.environ.get('SHOPIFY_STORE_DOMAIN', 'dresslikemommy-com.myshopify.com')}/admin/api/2025-01/graphql.json"
headers = {
    "X-Shopify-Access-Token": os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"],
    "Content-Type": "application/json",
}

listing_md_path = Path(settings["listing_md"])
csv_out_path = Path(settings["csv_out"])
verify_json_out_path = Path(settings["verify_json_out"])
size_chart_out_path = Path(settings["size_chart_out"])
body_html_out_path = Path(settings["body_html_out"])
upload_dir = Path(settings["upload_dir"])
for path in [listing_md_path, csv_out_path, verify_json_out_path, size_chart_out_path, body_html_out_path]:
    path.parent.mkdir(parents=True, exist_ok=True)


def gql(query, variables=None):
    response = requests.post(api, headers=headers, json={"query": query, "variables": variables or {}}, timeout=120)
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], ensure_ascii=False))
    return payload


def compare_at(price):
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def metric_cell(text, unit):
    text = str(text or "").strip()
    if not text or text in {"-", "—"}:
        return "—"
    suffix = f" {unit}"
    return text[:-len(suffix)] if text.endswith(suffix) else text


def cm_cell(value):
    if value in (None, "", 0):
        return "—"
    return str(int(value)) if float(value).is_integer() else str(value)


def role_root(role):
    return role.split()[0]


if len(settings["title"]) > 70:
    raise RuntimeError("Product title exceeds 70 characters")
if len(settings["seo_title"]) > 60:
    raise RuntimeError("SEO title exceeds 60 characters")
if len(settings["seo_description"]) > 155:
    raise RuntimeError("SEO description exceeds 155 characters")

taxonomy = gql(
    """
    query TaxonomyCategory($id: ID!) {
      node(id: $id) {
        __typename
        ... on TaxonomyCategory { id fullName isLeaf }
      }
    }
    """,
    {"id": settings["taxonomy_gid"]},
)["data"]["node"]
if not taxonomy or taxonomy.get("fullName") != settings["expected_taxonomy_full_name"] or taxonomy.get("isLeaf") is not True:
    raise RuntimeError(f"Taxonomy guard failed: {taxonomy}")

role_tokens = {"Girl": "GRL", "Boy": "BOY", "Mother": "MOM", "Father": "DAD"}
size_tokens = {
    "Girl 1-2 Years": "KID12Y", "Girl 2 Years": "KID2Y", "Girl 3 Years": "KID3Y", "Girl 4 Years": "KID4Y",
    "Girl 5 Years": "KID5Y", "Girl 6-7 Years": "KID67Y", "Girl 8 Years": "KID8Y", "Girl 9-10 Years": "KID910Y",
    "Boy 1-2 Years": "KID12Y", "Boy 2 Years": "KID2Y", "Boy 3 Years": "KID3Y", "Boy 4 Years": "KID4Y",
    "Boy 5 Years": "KID5Y", "Boy 6-7 Years": "KID67Y", "Boy 8 Years": "KID8Y", "Boy 9-10 Years": "KID910Y",
    "Mother S": "S", "Mother M": "M", "Mother L": "L", "Mother XL": "XL", "Mother 2XL": "2XL", "Mother 3XL": "3XL",
    "Father S": "S", "Father M": "M", "Father L": "L", "Father XL": "XL", "Father 2XL": "2XL", "Father 3XL": "3XL",
}
required_fields = ["audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "pant_cm"]
seen = set()
errors = []
for row in size_chart:
    missing = [field for field in required_fields if row.get(field) in (None, "")]
    if missing:
        errors.append(f"{row.get('vendor_label')} missing {', '.join(missing)}")
    pair = (row["role"], row["picker_label"])
    if pair in seen:
        errors.append(f"duplicate role/picker pair {pair}")
    seen.add(pair)
    if role_root(row["role"]) not in role_tokens:
        errors.append(f"no role token for {row['role']}")
    if row["picker_label"] not in size_tokens:
        errors.append(f"no size token for {row['picker_label']}")
    if row["picker_label"] not in size_map:
        errors.append(f"no shopify.size mapping for {row['picker_label']}")
if errors:
    raise RuntimeError("Preflight failed:\n- " + "\n- ".join(errors))

child_price = settings["child_price"]
adult_price = settings["adult_price"]
child_compare = compare_at(child_price)
adult_compare = compare_at(adult_price)

def sku_for(row):
    return f"DLM-{settings['shortcode']}-{role_tokens[role_root(row['role'])]}-{size_tokens[row['picker_label']]}-{settings['color_token']}"

variants = []
recap = []
for row in size_chart:
    is_child = row["audience"] == "child"
    price = child_price if is_child else adult_price
    compare = child_compare if is_child else adult_compare
    sku = sku_for(row)
    variants.append({
        "price": price,
        "compareAtPrice": compare,
        "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": sku, "tracked": True, "requiresShipping": True},
        "optionValues": [
            {"optionName": "Size", "name": row["picker_label"]},
            {"optionName": "Color", "name": settings["color_name"]},
        ],
    })
    recap.append({**row, "sku": sku, "price": price, "compare_at_price": compare, "shopify_size_gid": size_map[row["picker_label"]]["gid"], "catalog_label": size_map[row["picker_label"]]["catalog_label"]})

product_options = [
    {"name": "Size", "values": [{"name": row["picker_label"]} for row in size_chart]},
    {"name": "Color", "values": [{"name": settings["color_name"]}]},
]
derived_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
size_range_copy = "girls and boys 1-2Y through 9-10Y, mothers S-3XL, and fathers S-3XL"

rows_html = []
for row in size_chart:
    rows_html.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(metric_cell(row['weight'], 'kg'))}</td>"
        f"<td>{html.escape(metric_cell(row['height'], 'cm'))}</td>"
        f"<td>{cm_cell(row['chest_cm'])}</td>"
        f"<td>{cm_cell(row['sleeve_cm'])}</td>"
        f"<td>{cm_cell(row['pant_cm'])}</td>"
        f"<td>{cm_cell(row['hip_cm'])}</td>"
        f"<td>{cm_cell(row['waist_cm'])}</td>"
        f"<td>{cm_cell(row['length_cm'])}</td>"
        "</tr>"
    )

body_html = "\n".join([
    "<ul>",
    "<li><strong>Fabric:</strong> Soft woven-look shirt fabric based on the supplied photos; the blocked vendor page did not expose exact fiber content.</li>",
    "<li><strong>Family story:</strong> A relaxed red plaid button-up for mom, dad, girls, and boys, made for coordinated family photos, school days, weekend walks, and holiday plans.</li>",
    "<li><strong>Print reference:</strong> Red Plaid mixes red, green, and white checks for a warm matching look.</li>",
    "<li><strong>Design details:</strong> Collared button-front shirt, long sleeves, easy layering shape, and one shared plaid colorway. White tees, jeans, hats, bags, shoes, and bike props shown in the photos are styling only.</li>",
    "<li><strong>Care:</strong> Machine wash cold on gentle, wash with similar colors, line dry or tumble low, and avoid bleach. This care guidance is conservative because direct vendor care text was not available.</li>",
    f"<li><strong>Size range:</strong> {size_range_copy}.</li>",
    "</ul>",
    "<h3>Size Chart</h3>",
    "<table id=\"size-chart\">",
    "<thead><tr><th>Size</th><th>Age</th><th>Weight (kg)</th><th>Height (cm)</th><th>Chest/Bust (cm)</th><th>Sleeve / Skirt (cm)</th><th>Pant / Short (cm)</th><th>Hip (cm)</th><th>Waist (cm)</th><th>Garment Length (cm)</th></tr></thead>",
    "<tbody>",
    *rows_html,
    "</tbody></table>",
    "<p>Red Plaid brings the whole family into one coordinated shirt story without making the outfit feel too formal. Wear the shirts open over simple tees or buttoned up for a cleaner family photo look.</p>",
    "<p>The attached vendor chart publishes one shirt measurement ladder for children and one for adults. The fit report confirms boy, girl, mom, and dad try-ons, so the Shopify size picker keeps those role labels while every variant remains tied to a real vendor row.</p>",
    "<h3>Key Features:</h3>",
    "<ul>",
    "<li><strong>Four-role family match:</strong> Sizes are prepared for girls, boys, mothers, and fathers.</li>",
    "<li><strong>Classic plaid color story:</strong> Red, green, and white checks photograph warmly across seasons.</li>",
    "<li><strong>Layer-ready design:</strong> Button-front collared shirt works over tees, denim, skirts, or casual trousers.</li>",
    "<li><strong>Vendor-backed size range:</strong> Child 80-150 and adult S-3XL rows are transcribed from the attached chart.</li>",
    "<li><strong>Single included garment:</strong> This listing covers the plaid shirts only; all other styled items in the photos are not included.</li>",
    "</ul>",
    "<p>Choose each family member's size and create an easy matching plaid outfit for photos, holidays, and everyday memories.</p>",
])

tags = sorted({
    "Family Matching", "Mommy and Me", "Daddy and Me", "Tops", "Matching Family Tops", "Matching Family Shirts",
    "Button-Up Shirt", "Plaid Shirt", "Long Sleeve Top", "Red Plaid", "Red", "Green", "White", "Checkered",
    "Fall", "Holiday", "Family Photos", "Matching Family Outfits",
    "Girl Shirt", "Boy Shirt", "Mother Shirt", "Father Shirt",
    "Child 1-2yr", "Child 2-3yr", "Child 4-5yr", "Child 6-8yr", "Child 9-10yr",
    "Mother S", "Mother M", "Mother L", "Mother XL", "Mother 2XL", "Mother 3XL",
    "Father S", "Father M", "Father L", "Father XL", "Father 2XL", "Father 3XL",
    settings["vendor_url"],
})

size_chart_out_path.write_text(json.dumps(size_chart, indent=2), encoding="utf-8")
body_html_out_path.write_text(body_html, encoding="utf-8")

existing = gql(
    """
    query ExistingProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id handle status publishedAt
        variants(first: 100) { nodes { id sku selectedOptions { name value } } }
        media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } }
      }
    }
    """,
    {"handle": settings["handle"]},
)["data"]["productByHandle"]
product_id = existing["id"] if existing else ""
if existing and existing.get("status") != "DRAFT":
    raise RuntimeError(f"Existing product {settings['handle']} is {existing.get('status')}; refusing to alter publish state.")

if not product_id:
    created = gql(
        """
        mutation ProductCreate($input: ProductInput!) {
          productCreate(input: $input) {
            product { id handle title }
            userErrors { field message }
          }
        }
        """,
        {"input": {
            "handle": settings["handle"], "title": settings["title"], "descriptionHtml": body_html,
            "vendor": settings["vendor"], "productType": settings["product_type"], "tags": tags,
            "status": "DRAFT", "category": settings["taxonomy_gid"],
            "seo": {"title": settings["seo_title"], "description": settings["seo_description"]},
            "productOptions": product_options,
        }},
    )["data"]["productCreate"]
    if created["userErrors"]:
        raise RuntimeError(f"productCreate userErrors: {created['userErrors']}")
    product_id = created["product"]["id"]

updated = gql(
    """
    mutation ProductUpdate($product: ProductUpdateInput!) {
      productUpdate(product: $product) {
        product { id handle title }
        userErrors { field message }
      }
    }
    """,
    {"product": {
        "id": product_id, "handle": settings["handle"], "title": settings["title"], "descriptionHtml": body_html,
        "vendor": settings["vendor"], "productType": settings["product_type"], "tags": tags,
        "status": "DRAFT", "category": settings["taxonomy_gid"],
        "seo": {"title": settings["seo_title"], "description": settings["seo_description"]},
    }},
)["data"]["productUpdate"]
if updated["userErrors"]:
    raise RuntimeError(f"productUpdate userErrors: {updated['userErrors']}")

existing = gql(
    """
    query ExistingProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        variants(first: 100) { nodes { id sku selectedOptions { name value } } }
      }
    }
    """,
    {"handle": settings["handle"]},
)["data"]["productByHandle"]
live_variants = existing["variants"]["nodes"]
expected_pairs = {(row["picker_label"], settings["color_name"]) for row in size_chart}
live_pairs = {tuple(option["value"] for option in v["selectedOptions"]) for v in live_variants}
if not live_variants or (len(live_variants) == 1 and not live_variants[0].get("sku")):
    result = gql(
        """
        mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
          productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
            productVariants { id sku title }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
    )["data"]["productVariantsBulkCreate"]
    if result["userErrors"]:
        raise RuntimeError(f"productVariantsBulkCreate userErrors: {result['userErrors']}")
else:
    if len(live_variants) != len(size_chart) or live_pairs != expected_pairs:
        raise RuntimeError("Existing draft has an unexpected variant shape; refusing to duplicate variants.")
    by_pair = {tuple(option["value"] for option in v["selectedOptions"]): v for v in live_variants}
    update_payload = []
    for spec in variants:
        pair = tuple(value["name"] for value in spec["optionValues"])
        update_payload.append({"id": by_pair[pair]["id"], **spec})
    result = gql(
        """
        mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
          productVariantsBulkUpdate(productId: $productId, variants: $variants) {
            productVariants { id sku title }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "variants": update_payload},
    )["data"]["productVariantsBulkUpdate"]
    if result["userErrors"]:
        raise RuntimeError(f"productVariantsBulkUpdate userErrors: {result['userErrors']}")

unique_size_gids = []
for row in size_chart:
    gid = size_map[row["picker_label"]]["gid"]
    if gid not in unique_size_gids:
        unique_size_gids.append(gid)
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
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": settings["merch_style"]},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Top"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(settings["age_group_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(settings["color_pattern_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(unique_size_gids)},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(settings["target_gender_gids"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": settings["seo_title"]},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": settings["seo_description"]},
]
mf_result = gql(
    """
    mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { namespace key type value }
        userErrors { field message }
      }
    }
    """,
    {"metafields": metafields},
)["data"]["metafieldsSet"]
if mf_result["userErrors"]:
    raise RuntimeError(f"metafieldsSet userErrors: {mf_result['userErrors']}")

media_lookup = gql(
    """
    query ProductMedia($id: ID!) {
      product(id: $id) { media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } } }
    }
    """,
    {"id": product_id},
)["data"]["product"]["media"]["nodes"]
existing_alts = {item.get("alt") or "" for item in media_lookup}
alt_by_name = {
    "look-1.png": "Mom, dad, and child wearing the red plaid family matching button-up shirts.",
    "look-2.png": "Family wearing red plaid matching shirts styled with white tees and denim.",
}
for image_path in sorted(upload_dir.iterdir()):
    if image_path.name == "size-chart.png" or image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    alt = alt_by_name.get(image_path.name, f"{settings['title']} lifestyle image")
    if alt in existing_alts:
        continue
    mime_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
    staged = gql(
        """
        mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
        """,
        {"input": [{"filename": image_path.name, "mimeType": mime_type, "resource": "IMAGE", "httpMethod": "POST"}]},
    )["data"]["stagedUploadsCreate"]
    if staged["userErrors"]:
        raise RuntimeError(f"stagedUploadsCreate userErrors: {staged['userErrors']}")
    target = staged["stagedTargets"][0]
    form_data = {param["name"]: param["value"] for param in target["parameters"]}
    with image_path.open("rb") as fh:
        upload = requests.post(target["url"], data=form_data, files={"file": (image_path.name, fh, mime_type)}, timeout=120)
        upload.raise_for_status()
    created_media = gql(
        """
        mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id alt } }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]},
    )["data"]["productCreateMedia"]
    if created_media["userErrors"]:
        raise RuntimeError(f"productCreateMedia userErrors: {created_media['userErrors']}")

time.sleep(2)
verify = gql(
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
        metafields(first: 100) { nodes { namespace key type value } }
        media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } }
        resourcePublicationsV2(first: 20) { nodes { publication { id name } publishDate isPublished } }
      }
    }
    """,
    {"id": product_id},
)["data"]["product"]
verify_json_out_path.write_text(json.dumps(verify, indent=2), encoding="utf-8")

live_variants = verify["variants"]["nodes"]
live_skus = sorted(v["sku"] for v in live_variants)
live_pairs = {tuple(o["value"] for o in v["selectedOptions"]) for v in live_variants}
expected_pairs = {(row["picker_label"], settings["color_name"]) for row in size_chart}
th_count = len(re.findall(r"<th>", body_html))
tr_count = len(re.findall(r"<tr>", body_html)) - 1
published = [node for node in verify["resourcePublicationsV2"]["nodes"] if node.get("isPublished")]
price_ok = all(
    v["price"] == next(item["price"] for item in recap if item["sku"] == v["sku"])
    and (v.get("compareAtPrice") or "") == next(item["compare_at_price"] for item in recap if item["sku"] == v["sku"])
    for v in live_variants
)
verification_rows = [
    ("Title <= 70 chars", len(settings["title"]) <= 70, str(len(settings["title"]))),
    ("SEO title <= 60 chars", len(settings["seo_title"]) <= 60, str(len(settings["seo_title"]))),
    ("SEO description <= 155 chars", len(settings["seo_description"]) <= 155, str(len(settings["seo_description"]))),
    ("Draft status", verify["status"] == "DRAFT", verify["status"]),
    ("publishedAt is null", verify["publishedAt"] is None, str(verify["publishedAt"])),
    ("No sales-channel publications live", not published, json.dumps(published)),
    ("Variant count matches SIZE_CHART", len(live_variants) == len(size_chart), f"{len(live_variants)} vs {len(size_chart)}"),
    ("Live SKUs match derived SKUs", live_skus == derived_skus, "match" if live_skus == derived_skus else "mismatch"),
    ("Every Size x Color combination exists", live_pairs == expected_pairs, "match" if live_pairs == expected_pairs else "mismatch"),
    ("Each size table has 10 headers", th_count == 10, str(th_count)),
    ("Table row count matches SIZE_CHART", tr_count == len(size_chart), str(tr_count)),
    ("Waist populated for every row", all(row["waist_cm"] for row in size_chart), "all populated"),
    ("Every variant tracked, DENY, priced", all(v["inventoryPolicy"] == "DENY" and v["inventoryItem"]["tracked"] and v["inventoryItem"]["requiresShipping"] for v in live_variants), "checked"),
    ("Taxonomy category resolves", verify["category"] and verify["category"]["fullName"] == settings["expected_taxonomy_full_name"], verify["category"]["fullName"] if verify["category"] else "missing"),
    ("FORCE_SPEC_PRICES parity", price_ok, "match" if price_ok else "mismatch"),
]
failures = [row for row in verification_rows if not row[1]]
if failures:
    raise RuntimeError("Verification failed:\n- " + "\n- ".join(f"{label}: {detail}" for label, _, detail in failures))

metafields_written = sorted(f"{m['namespace']}.{m['key']}" for m in metafields)
skipped = [
    ("shopify.fabric", "Skipped because the source supports only a soft woven-look appearance, not an exact fiber metaobject."),
    ("shopify.neckline", "Skipped because the shirt collar is visible, but no verified writable standard neckline GID was confirmed for this taxonomy."),
    ("shopify.sleeve-length-type", "Skipped because the chart supports long sleeves, but no verified writable standard sleeve-length GID was confirmed for this taxonomy."),
    ("shopify.top-length-type", "Skipped because the chart gives garment length but not enough evidence to map one precise standard top-length value."),
    ("shopify.dress-occasion", "Not applicable to a Tops listing."),
    ("shopify.dress-style", "Not applicable to a Tops listing."),
    ("shopify.skirt-dress-length-type", "Not applicable to a Tops listing."),
]

with csv_out_path.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Variant SKU", "Variant Price", "Variant Compare At Price", "Variant Inventory Tracker", "Variant Inventory Policy", "Variant Requires Shipping", "Status"])
    for item in recap:
        writer.writerow([settings["handle"], settings["title"], body_html, settings["vendor"], settings["expected_taxonomy_full_name"], settings["product_type"], ", ".join(tags), "FALSE", "Size", item["picker_label"], "Color", settings["color_name"], item["sku"], item["price"], item["compare_at_price"], "shopify", "deny", "TRUE", "draft"])

recap_lines = [
    "| Role | Vendor | Picker | Color | SKU | Price | shopify.size GID |",
    "|---|---|---|---|---|---:|---|",
]
for item in recap:
    recap_lines.append(f"| {item['role']} | {item['vendor_label']} | {item['picker_label']} | {settings['color_name']} | `{item['sku']}` | ${item['price']} | `{item['shopify_size_gid']}` ({item['catalog_label']}) |")
verify_lines = ["| Check | Result | Detail |", "|---|---|---|"]
for label, ok, detail in verification_rows:
    verify_lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {str(detail).replace('|', '/')} |")
price_lines = ["| SKU | Live Price | Live Compare-at | Spec Price | Spec Compare-at | Match |", "|---|---:|---:|---:|---:|---|"]
recap_by_sku = {item["sku"]: item for item in recap}
for variant in sorted(live_variants, key=lambda v: v["sku"]):
    spec = recap_by_sku[variant["sku"]]
    match = variant["price"] == spec["price"] and (variant.get("compareAtPrice") or "") == spec["compare_at_price"]
    price_lines.append(f"| `{variant['sku']}` | {variant['price']} | {variant.get('compareAtPrice') or ''} | {spec['price']} | {spec['compare_at_price']} | {'PASS' if match else 'FAIL'} |")

listing_md = "\n".join([
    f"# {settings['title']}",
    "",
    f"**Status:** Draft (`{verify['status']}`), unpublished.",
    f"**Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/{product_id.rsplit('/', 1)[-1]}",
    "**Live URL:** not published",
    f"**Product ID:** `{product_id}`",
    f"**Handle:** `{settings['handle']}`",
    f"**Vendor source URL (tags only):** {settings['vendor_url']}",
    "",
    "## Request resolution",
    "| Input | Resolved |",
    "|---|---|",
    "| LISTING_MODE | Family Matching |",
    "| PRIMARY_CATEGORY | auto -> Tops |",
    "| DESIGNS_TO_LIST | auto -> one Red Plaid button-up shirt colorway |",
    "| Variant model | Size / Color; role-bearing Size labels keep mom/dad/girl/boy variants unique |",
    "| FORCE_SPEC_PRICES | true |",
    "",
    "## Vendor source-of-truth",
    "- Direct public access to the 1688 offer was blocked, so the attached size chart and product images were used as authoritative evidence.",
    "- The chart publishes shirt rows only: child 80-150 and adult S, M, L, XL, XXL, 3XL.",
    "- The fit report confirms boy, girl, mom, and dad try-ons, so rows are duplicated into honest role-bearing Shopify picker labels.",
    "- `胸围*2` is treated as half chest and doubled for full chest/bust.",
    "- `推荐体重` values are domestic jin ranges and were converted to kg.",
    "- Hip and waist are derived per the canonical shirt/top rules because the chart omits both: kids use hip=chest+4 and waist=chest; adults use hip=chest and waist=chest-12.",
    "- Product photos show white tees, denim, hats, bag, shoes, and bicycle props; those are styling only and not included.",
    "",
    "## Title & SEO",
    f"- Product title ({len(settings['title'])}/70): `{settings['title']}`",
    f"- SEO title ({len(settings['seo_title'])}/60): `{settings['seo_title']}`",
    f"- SEO description ({len(settings['seo_description'])}/155): `{settings['seo_description']}`",
    "",
    "## SIZE_CHART / Variant Recap",
    *recap_lines,
    "",
    "## Body HTML",
    "- 1 intro bullet list with 6 items.",
    "- 1 shirt size table with 10 headers and 28 rows.",
    "- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.",
    "",
    "## Metafields written",
    *[f"- `{key}`" for key in metafields_written],
    "",
    "## Metafields skipped",
    *[f"- `{key}` - {reason}" for key, reason in skipped],
    "",
    "## Verification",
    *verify_lines,
    "",
    "## Price parity",
    *price_lines,
    "",
    "## Smart collections",
    "- Product is a draft and unpublished, so smart collection indexing/public collection visibility may wait until an explicit publish-live step.",
    "",
    "## Manual follow-ups",
    "- Inventory quantities and weights remain unset/zero and need operator stock values later.",
    "- If the vendor page becomes readable later, confirm exact fabric content and replace the broad woven-look copy if needed.",
    "",
    "## Files",
    f"- `{listing_md_path}`",
    f"- `{csv_out_path}`",
    f"- `{verify_json_out_path}`",
    f"- `{size_chart_out_path}`",
    f"- `{body_html_out_path}`",
    f"- `{Path('/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-rpld-red-plaid-family-matching-tops.sh')}`",
])
listing_md_path.write_text(listing_md, encoding="utf-8")

print(json.dumps({
    "product_id": product_id,
    "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.rsplit('/', 1)[-1]}",
    "status": verify["status"],
    "publishedAt": verify["publishedAt"],
    "variant_count": len(live_variants),
    "media_count": len(verify["media"]["nodes"]),
    "listing_md": str(listing_md_path),
}, indent=2))
PY
