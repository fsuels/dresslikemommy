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
  "handle": "red-stripe-family-matching-tops",
  "title": "Red Stripe Family Matching Tops - Heart Pocket Tee",
  "seo_title": "Red Stripe Family Tops | Dress Like Mommy",
  "seo_description": "Red striped family matching tees for mom, dad, girls and boys. Short-sleeve tops in Child 2Y-9-10Y and Adult S-3XL.",
  "print_name": "Red Stripe",
  "shortcode": "RSTR",
  "color_token": "REDSTR",
  "color_name": "Red Stripe",
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
  "merch_subcategory2": "Family Matching Tops",
  "merch_style": "Matching Family Top",
  "merch_type": "Top",
  "season": "Spring/Summer",
  "vendor_url": "https://detail.1688.com/offer/1041045173122.html",
  "vendor": "dresslikemommy.com",
  "force_spec_prices": true,
  "child_price": "24.99",
  "adult_price": "28.99",
  "price_neighbor_handle": "blue-apricot-letter-family-matching-tops",
  "size_neighbor_handle": "shopify--size metaobjects",
  "script_path": "/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-rstr-red-stripe-family-matching-tops.sh",
  "upload_dir": "/Users/fsuels/Projects/dresslikemommy/uploads/red-stripe-family-matching-tops",
  "listing_md": "/Users/fsuels/Projects/dresslikemommy/ops/listings/red-stripe-family-matching-tops-listing.md",
  "csv_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/red-stripe-family-matching-tops-shopify-import.csv",
  "verify_json_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-red-stripe-family-matching-tops.json",
  "size_chart_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-red-stripe-family-matching-tops.json",
  "body_html_out": "/Users/fsuels/Projects/dresslikemommy/ops/listings/body-red-stripe-family-matching-tops.html",
  "csv_header_source": "/Users/fsuels/Projects/dresslikemommy/bird-chirping-mommy-and-me-pajamas-shopify-import.csv",
  "age_group_gids": [
    "gid://shopify/Metaobject/128116523105",
    "gid://shopify/Metaobject/128116490337"
  ],
  "color_pattern_gids": [
    "gid://shopify/Metaobject/69600804961",
    "gid://shopify/Metaobject/69639733345"
  ],
  "fabric_gids": [],
  "target_gender_gids": [
    "gid://shopify/Metaobject/129972502625"
  ],
  "fit_report": [
    {"role": "Girl", "height_cm": 134, "weight_jin": 50, "tried_size": "140", "note": "Loose fit"},
    {"role": "Mom", "height_cm": 164, "weight_jin": 88, "tried_size": "S", "note": "Loose fit"}
  ],
  "product_image_sources": [
    "/Users/fsuels/Projects/dresslikemommy/uploads/red-stripe-family-matching-tops/look-1.png",
    "/Users/fsuels/Projects/dresslikemommy/uploads/red-stripe-family-matching-tops/look-2.png"
  ],
  "size_chart_source": "/Users/fsuels/Projects/dresslikemommy/uploads/red-stripe-family-matching-tops/source-size-chart.png",
  "required_tags": [
    "Family Matching",
    "Tops",
    "Matching Family Top",
    "Matching Family Tops",
    "Stripe",
    "Red Stripe",
    "Short Sleeve Tee",
    "Heart Pocket Tee",
    "Adult S",
    "Adult M",
    "Adult L",
    "Adult XL",
    "Adult 2XL",
    "Adult 3XL",
    "Child 2 Years",
    "Child 3 Years",
    "Child 4 Years",
    "Child 5 Years",
    "Child 6-7 Years",
    "Child 8 Years",
    "Child 9-10 Years",
    "https://detail.1688.com/offer/1041045173122.html"
  ]
}
JSON
)

SIZE_CHART_JSON=$(cat <<'JSON'
[
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"18-25 jin","height":"80-90 cm","length_cm":38.5,"shoulder_cm":31,"chest_cm":64},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"20-28 jin","height":"90-100 cm","length_cm":41.5,"shoulder_cm":33,"chest_cm":68},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"28-38 jin","height":"100-110 cm","length_cm":44.5,"shoulder_cm":35,"chest_cm":72},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"38-48 jin","height":"110-120 cm","length_cm":48.5,"shoulder_cm":37,"chest_cm":77},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"48-58 jin","height":"120-130 cm","length_cm":52.5,"shoulder_cm":39,"chest_cm":82},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"58-68 jin","height":"130-140 cm","length_cm":56.5,"shoulder_cm":41,"chest_cm":87},
  {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"68-78 jin","height":"140-150 cm","length_cm":60.5,"shoulder_cm":43,"chest_cm":92},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"-","weight":"80-100 jin","height":"155-163 cm","length_cm":62,"shoulder_cm":44.5,"chest_cm":100},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"-","weight":"100-120 jin","height":"160-168 cm","length_cm":65,"shoulder_cm":46.5,"chest_cm":104},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"-","weight":"120-140 jin","height":"165-173 cm","length_cm":68,"shoulder_cm":48.5,"chest_cm":109},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"-","weight":"140-160 jin","height":"170-178 cm","length_cm":72,"shoulder_cm":50.5,"chest_cm":112},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"-","weight":"160-180 jin","height":"175-183 cm","length_cm":74.5,"shoulder_cm":53,"chest_cm":117},
  {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"-","weight":"180-195 jin","height":"180-185 cm","length_cm":77,"shoulder_cm":55.5,"chest_cm":122}
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
  {"picker_label":"Adult 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"shopify--size metaobjects"}
]
JSON
)

mkdir -p "${ROOT}/ops/listings" "/Users/fsuels/Projects/dresslikemommy/uploads/red-stripe-family-matching-tops"

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
    "age", "weight", "height", "length_cm", "shoulder_cm", "chest_cm",
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
        f"<td>{cm_cell(row['length_cm'])}</td>"
        f"<td>{cm_cell(row['shoulder_cm'])}</td>"
        f"<td>{cm_cell(row['chest_cm'])}</td>"
        f"<td>{html.escape(strip_unit(row['height'], 'cm'))}</td>"
        f"<td>{html.escape(strip_unit(row['weight'], 'jin'))}</td>"
        "</tr>"
    )

body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Soft knit-look tee fabric with red horizontal stripes, based on the vendor imagery and the attached size-chart source.</li>",
        "<li><strong>Family story:</strong> A relaxed matching top for moms, dads, girls, and boys that feels easy for everyday photos and casual outings.</li>",
        "<li><strong>Print reference:</strong> Red Stripe keeps the outfit simple and versatile, with a classic crew-neck tee shape, horizontal stripes, and visible heart patch detail.</li>",
        "<li><strong>Design details:</strong> Short sleeves, crew neckline, relaxed fit, small heart chest patch, and an easy tee silhouette. White pants, shoes, hat, tote, and outdoor props shown in photos are styling only.</li>",
        "<li><strong>Care:</strong> Machine wash cold, turn inside out, line dry or tumble low, and avoid bleach. This is conservative care guidance because the blocked vendor page did not expose wash instructions.</li>",
        "<li><strong>Size range:</strong> Child 2Y through Child 9-10Y and Adult S through Adult 3XL.</li>",
        "</ul>",
        "",
        "<h3>Size Chart</h3>",
        "<table id=\"size-chart\">",
        "  <thead>",
        "    <tr>",
        "      <th>Size</th>",
        "      <th>Top Length (cm)</th>",
        "      <th>Shoulder (cm)</th>",
        "      <th>Chest (cm)</th>",
        "      <th>Suggested Height (cm)</th>",
        "      <th>Suggested Weight (jin)</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        *table_rows,
        "  </tbody>",
        "</table>",
        "",
        "<p>Red Stripe is a laid-back family matching top with enough polish for photos and enough ease for real family days. The tee has a crew neckline, relaxed body, and soft red-stripe color that coordinates across kids and adults without feeling overly formal.</p>",
        "",
        "<p>The attached vendor chart publishes one child top ladder and one adult top ladder rather than separate girl, boy, mom, and dad tables, so this draft keeps the variant structure honest with Child and Adult size labels instead of inventing unsupported role-specific rows. The vendor's top table is transcribed directly with top length, shoulder, chest, suggested height, and suggested weight. The separate pants table is excluded because this listing is for the Heart Pocket Tee.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>One coordinated top:</strong> Same red-stripe tee look for children and adults.</li>",
        "<li><strong>Photo-ready stripe:</strong> Soft red color, horizontal striping, small heart chest patch, and a casual tee shape.</li>",
        "<li><strong>Easy family fit:</strong> Vendor try-on notes show loose fits for the charted girl and mom examples.</li>",
        "<li><strong>Easy styling:</strong> Pair with casual pants for a clean family look.</li>",
        "<li><strong>Chart-backed variants:</strong> Every size option is backed by the attached vendor size chart.</li>",
        "</ul>",
        "",
        "<p>Choose the child and adult sizes you need to build an easy matching red striped look for family photos, travel days, and everyday outings.</p>",
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
        "Stripe",
        "Red Stripe",
        "Red",
        "Short Sleeve Tee",
        "Striped Shirt",
        "Heart Pocket Tee",
        "Crew Neck Tee",
        "Tee",
        "Easy Fit",
        "Spring",
        "Summer",
        "Family Photos",
        "Adult S",
        "Adult M",
        "Adult L",
        "Adult XL",
        "Adult 2XL",
        "Adult 3XL",
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
    live_by_pair = {tuple(option["value"] for option in variant["selectedOptions"]): variant for variant in live_variants}
    variant_specs_by_pair = {
        tuple(value["name"] for value in spec["optionValues"]): spec
        for spec in variants
    }
    obsolete_variant_ids = [
        live_by_pair[pair]["id"]
        for pair in sorted(live_option_pairs - expected_option_pairs)
    ]
    missing_variants = [
        variant_specs_by_pair[pair]
        for pair in sorted(expected_option_pairs - live_option_pairs)
    ]
    common_pairs = sorted(expected_option_pairs & live_option_pairs)
    variant_update_payload = []
    for pair in common_pairs:
        spec = variant_specs_by_pair[pair]
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
    if variant_update_payload:
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
    if missing_variants:
        create_variants_result = gql(
            """
            mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
              productVariantsBulkCreate(productId: $productId, variants: $variants) {
                productVariants { id sku title }
                userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": missing_variants},
        )
        user_errors = create_variants_result["data"]["productVariantsBulkCreate"]["userErrors"]
        if user_errors:
            raise RuntimeError(f"productVariantsBulkCreate userErrors: {json.dumps(user_errors, ensure_ascii=False)}")
    if obsolete_variant_ids:
        delete_variants_result = gql(
            """
            mutation ProductVariantsBulkDelete($productId: ID!, $variantsIds: [ID!]!) {
              productVariantsBulkDelete(productId: $productId, variantsIds: $variantsIds) {
                product { id }
                userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variantsIds": obsolete_variant_ids},
        )
        user_errors = delete_variants_result["data"]["productVariantsBulkDelete"]["userErrors"]
        if user_errors:
            raise RuntimeError(f"productVariantsBulkDelete userErrors: {json.dumps(user_errors, ensure_ascii=False)}")

option_lookup = gql(
    """
    query ProductOptionsForReorder($id: ID!) {
      product(id: $id) {
        options {
          id
          name
          values
          optionValues { id name }
        }
      }
    }
    """,
    {"id": product_id},
)
option_nodes = option_lookup["data"]["product"]["options"]
size_option = next((option for option in option_nodes if option["name"] == "Size"), None)
color_option = next((option for option in option_nodes if option["name"] == "Color"), None)
if size_option and color_option:
    size_values_by_name = {value["name"]: value for value in size_option["optionValues"]}
    color_values_by_name = {value["name"]: value for value in color_option["optionValues"]}
    reorder_options = [
        {
            "id": size_option["id"],
            "values": [
                {"id": size_values_by_name[row["picker_label"]]["id"]}
                for row in size_chart
                if row["picker_label"] in size_values_by_name
            ],
        },
        {
            "id": color_option["id"],
            "values": [
                {"id": color_values_by_name[settings["color_name"]]["id"]}
            ] if settings["color_name"] in color_values_by_name else [],
        },
    ]
    reorder_result = gql(
        """
        mutation ProductOptionsReorder($productId: ID!, $options: [OptionReorderInput!]!) {
          productOptionsReorder(productId: $productId, options: $options) {
            product { id }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "options": reorder_options},
    )
    user_errors = reorder_result["data"]["productOptionsReorder"]["userErrors"]
    if user_errors:
        raise RuntimeError(f"productOptionsReorder userErrors: {json.dumps(user_errors, ensure_ascii=False)}")

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
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Heart Pocket Tee"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Top"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(settings["age_group_gids"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(settings["color_pattern_gids"])},
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
    "look-1.png": "Family wearing red stripe matching short-sleeve tee shirts.",
    "look-2.png": "Mom, dad, and child in red stripe family matching shirts.",
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
    "shopify.age-group", "shopify.color-pattern",
    "shopify.size", "shopify.target-gender", "global.title_tag",
    "global.description_tag",
}
publication_nodes = product["resourcePublicationsV2"]["nodes"]
live_publications = [node for node in publication_nodes if node.get("isPublished") is True]
single_unit_cells_ok = all("/" not in cell for cells in row_cells for cell in cells[1:])
picker_ok = [row["picker_label"] for row in size_chart] == first_cells
options_ok = [option["name"] for option in product["options"]] == ["Size", "Color"]
option_values_ok = (
    len(product["options"]) == 2
    and product["options"][0]["values"] == [row["picker_label"] for row in size_chart]
    and product["options"][1]["values"] == [settings["color_name"]]
)
required_tags_ok = set(settings["required_tags"]).issubset(set(product["tags"]))

verification_rows = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"] or "") <= 60, str(len(product["seo"]["title"] or ""))),
    ("SEO description <= 155 chars", len(product["seo"]["description"] or "") <= 155, str(len(product["seo"]["description"] or ""))),
    ("Product options are Size / Color", options_ok, ", ".join(option["name"] for option in product["options"])),
    ("Product option values match vendor tee sizes", option_values_ok, json.dumps([option["values"] for option in product["options"]])),
    ("Live variant count matches SIZE_CHART", len(product["variants"]["nodes"]) == len(size_chart), f"{len(product['variants']['nodes'])} vs {len(size_chart)}"),
    ("Live SKUs match derived SKUs", live_skus == derived_skus, "match" if live_skus == derived_skus else "mismatch"),
    ("Every variant tracked + DENY + priced", all(variant_checks), "all variants verified" if all(variant_checks) else "one or more variants failed"),
    ("Product status is DRAFT", product["status"] == "DRAFT", product["status"]),
    ("publishedAt is null", product["publishedAt"] is None, str(product["publishedAt"])),
    ("onlineStoreUrl is not published", product["onlineStoreUrl"] is None, str(product["onlineStoreUrl"])),
    ("No sales-channel publications are live", not live_publications, json.dumps(live_publications)),
    ("Taxonomy category set", (product["category"] or {}).get("id") == settings["taxonomy_gid"], (product["category"] or {}).get("id") or "missing"),
    ("Taxonomy category full name matches expected leaf", (product["category"] or {}).get("fullName") == settings["expected_taxonomy_full_name"], (product["category"] or {}).get("fullName") or "missing"),
    ("Size-chart table has 6 columns", thead_count == 6, str(thead_count)),
    ("Size-chart table row count matches SIZE_CHART", len(tbody_rows) == len(size_chart), str(len(tbody_rows))),
    ("Picker labels match first size-table column", picker_ok, "exact order match" if picker_ok else "mismatch"),
    ("Size-chart cells avoid mixed-unit slashes", single_unit_cells_ok, "no slash-separated values in table cells" if single_unit_cells_ok else "found dual-unit cell"),
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
        "Google Shopping / Custom Label 3": "Heart Pocket Tee",
        "Google Shopping / Custom Label 4": "Unisex Family Top",
        "Category1 (product.metafields.custom.category1)": "Family Matching",
        "Pattern (product.metafields.custom.pattern)": settings["print_name"],
        "Style (product.metafields.custom.style)": settings["merch_style"],
        "SubCategory (product.metafields.custom.subcategory)": settings["merch_subcategory"],
        "SubCategory2 (product.metafields.custom.subcategory2)": settings["merch_subcategory2"],
        "Type (product.metafields.custom.type)": settings["merch_type"],
        "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "FALSE",
        "Age group (product.metafields.shopify.age-group)": "kids, adults",
        "Color (product.metafields.shopify.color-pattern)": "Red, White",
        "Fabric (product.metafields.shopify.fabric)": "",
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
    "- mm-google-shopping.custom_label_3 = `Heart Pocket Tee`",
    "- mm-google-shopping.custom_label_4 = `Unisex Family Top`",
    "- shopify.age-group -> `Kids`, `Adults`",
    "- shopify.color-pattern -> `Red`, `White`",
    "- shopify.size -> 13 catalog metaobject references in chart order",
    "- shopify.target-gender -> `Unisex`",
    "- global.title_tag = SEO title",
    "- global.description_tag = SEO description",
]
skipped_metafields = [
    ("shopify.clothing-features", "No honest standard clothing-features entry is needed for this red striped family tee."),
    ("shopify.fabric", "Skipped because the source supports a soft knit-look tee, but it does not confirm exact fiber composition."),
    ("shopify.fit", "The Shirts & Tops taxonomy may expose fit, but no reliable writable standard Shopify metafield definition is available in this store."),
    ("shopify.neckline", "A crew-neck neckline is visible, but no reliable owner-subtype-safe standard neckline write was confirmed for this store."),
    ("shopify.top-length-type", "The chart exposes garment length but does not map cleanly to one standard top-length type."),
    ("shopify.sleeve-length-type", "The images and chart support short sleeves, but the store's writable standard sleeve-length value was not confirmed in this run."),
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
        "- The supplied images show one red striped short-sleeve tee for child and adult roles. White pants, hat, tote, shoes, and outdoor styling props are excluded.",
        "- Source conflict documented: the attached chart title includes a sleeveless halter A-line skirt/dress phrase, but the supplied product photos and request support a striped family top. This draft lists only the visible striped top and keeps all measurement rows chart-backed.",
        "- Size-chart columns transcribed from the vendor top table: Size, top length, shoulder, chest, suggested height, and suggested weight.",
        "- The vendor screenshot also includes pants tables; those rows are intentionally excluded because this listing is for the Heart Pocket Tee / top only.",
        "- Weight guidance is preserved in the vendor's `jin` unit instead of converting to kg, so the storefront table matches the source chart.",
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
        "- The vendor chart publishes one child top ladder and one adult top ladder, not separate girl/boy or mom/dad tables, so the draft uses `Child ...` and `Adult ...` size labels instead of inventing unsupported role-specific variants.",
        "- Vendor top size `90` maps to `Child 2 Years`; the prior unsupported `80 / Child 1-2 Years` row was removed.",
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
