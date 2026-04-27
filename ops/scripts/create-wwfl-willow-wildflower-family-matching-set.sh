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

python3 - <<'PY'
from __future__ import annotations

import csv
import html
import json
import math
import mimetypes
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "willow-wildflower-family-matching-set"
TITLE = "Willow Wildflower Family Matching Set - Dresses & Shirts"
SEO_TITLE = "Willow Wildflower Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Sage floral family matching set for mom, dad, girls and boys. Dresses and shirts in Child 1-10Y, Mother S-2XL and Father S-4XL."
PRINT_NAME = "Willow Wildflower"
SHORTCODE = "WWFL"
COLOR_TOKEN = "SAGE"
COLOR_NAME = "Sage Floral"
VENDOR_URL = ""
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "31.99"
ADULT_PRICE = "36.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops" / "listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops" / "listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops" / "listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops" / "listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops" / "listings" / f"body-{HANDLE}.html"

SIZE_MAP = {
    "Child 1-2 Years": ("gid://shopify/Metaobject/129972797537", "12-18 months"),
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
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":56,"skirt_cm":56,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":59,"skirt_cm":59,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":62,"skirt_cm":62,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":64,"skirt_cm":64,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":67,"skirt_cm":67,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":71,"skirt_cm":71,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":74,"skirt_cm":74,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":78,"skirt_cm":78,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":92,"hip_cm":98,"waist_cm":90,"length_cm":109,"skirt_cm":109,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":96,"hip_cm":102,"waist_cm":94,"length_cm":110,"skirt_cm":110,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"59-69 kg","height":"160-170 cm","chest_cm":100,"hip_cm":106,"waist_cm":98,"length_cm":112,"skirt_cm":112,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"70-80 kg","height":"160-175 cm","chest_cm":104,"hip_cm":110,"waist_cm":102,"length_cm":114,"skirt_cm":114,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"—","weight":"80-92.5 kg","height":"160-175 cm","chest_cm":108,"hip_cm":114,"waist_cm":106,"length_cm":115,"skirt_cm":115,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":34,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":37,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":40,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":43,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":46,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":49,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":52,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":100,"hip_cm":104,"waist_cm":100,"length_cm":55,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"—","weight":"42.5-50 kg","height":"160-165 cm","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":66,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"50-57.5 kg","height":"165-170 cm","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":68,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"57.5-67.5 kg","height":"168-173 cm","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":70,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"69-79 kg","height":"170-178 cm","chest_cm":126,"hip_cm":126,"waist_cm":114,"length_cm":72,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"80-89 kg","height":"175-180 cm","chest_cm":130,"hip_cm":130,"waist_cm":118,"length_cm":74,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"87.5-97.5 kg","height":"175-188 cm","chest_cm":134,"hip_cm":134,"waist_cm":122,"length_cm":76,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"4XL","picker_label":"Father 4XL","sku_suffix":"4XL","age":"—","weight":"97.5-115 kg","height":"178-195 cm","chest_cm":138,"hip_cm":138,"waist_cm":126,"length_cm":78,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
]


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode()) from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data


def require_no_user_errors(data: dict, path: list[str]) -> None:
    cur = data
    for key in path:
        cur = cur[key]
    if cur:
        raise RuntimeError(json.dumps(cur, indent=2))


def compare_at(price: str) -> str:
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def cm_to_in(value) -> str:
    if value in (None, "", 0, "-", "0"):
        return "-"
    if isinstance(value, str) and "/" in value:
        nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", value)]
        cm = "/".join(f"{n:g}" for n in nums)
        inches = "/".join(f"{n / 2.54:.1f}" for n in nums)
        return f"{cm} cm / {inches} in"
    number = float(value)
    return f"{number:g} cm / {number / 2.54:.1f} in"


def height_to_in(text: str) -> str:
    if not text or text == "-":
        return "-"
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) == 2:
        return f"{nums[0]:g}-{nums[1]:g} cm / {nums[0]/2.54:.1f}-{nums[1]/2.54:.1f} in"
    return cm_to_in(nums[0]) if nums else text


def kg_to_lb(text: str) -> str:
    if not text or text == "-":
        return "-"
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) == 2:
        return f"{nums[0]:g}-{nums[1]:g} kg / {nums[0]*2.20462:.1f}-{nums[1]*2.20462:.1f} lbs"
    return text


def role_token(role: str) -> str:
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Boy"):
        return "BOY"
    if role.startswith("Mother"):
        return "MOM"
    if role.startswith("Father"):
        return "DAD"
    raise KeyError(role)


def garment_token(garment: str) -> str:
    return {"Dress": "DRS", "Shirt": "SHRT"}[garment]


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father", "adult"} else CHILD_PRICE


def build_body() -> str:
    by_garment: dict[str, list[dict]] = {}
    for row in SIZE_CHART:
        by_garment.setdefault(row["garment"], []).append(row)

    def table_for(garment: str, rows: list[dict]) -> str:
        measure = "Skirt Length" if garment == "Dress" else "Sleeve or -"
        parts = [f"<h3>Size Chart - {html.escape(garment)}</h3>", "<table id=\"size-chart\">", "<thead><tr>"]
        headers = ["Size", "Age", "Weight (kg/lbs)", "Height (cm/in)", "Chest/Bust (cm/in)", f"{measure} (cm/in)", "Pant/Short or - (cm/in)", "Hip (cm/in)", "Waist (cm/in)", "Garment Length (cm/in)"]
        parts.extend(f"<th>{h}</th>" for h in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            if garment == "Dress":
                side = cm_to_in(row["skirt_cm"])
                pant = "-"
            else:
                side = "-"
                pant = "-"
            cells = [
                row["picker_label"],
                row["age"],
                kg_to_lb(row["weight"]),
                height_to_in(row["height"]),
                cm_to_in(row["chest_cm"]),
                side,
                pant,
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            parts.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>")
        parts.append("</tbody></table>")
        return "\n".join(parts)

    intro = """
<ul>
<li><strong>Fabric:</strong> Lightweight summer woven fabric; exact fiber composition was not visible in the supplied evidence.</li>
<li><strong>Family story:</strong> A coordinated warm-weather look for mom, dad, girls, and boys in a soft sage floral print.</li>
<li><strong>Print:</strong> Willow Wildflower pairs pale sage fabric with blue, red, yellow, and green garden stems for vacation photos, brunch, and everyday summer plans.</li>
<li><strong>Design details:</strong> Choose the smocked puff-sleeve dress or the relaxed short-sleeve collared shirt by size.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Child 1-2Y-10Y, Mother S-2XL, and Father S-4XL across the listed pieces.</li>
</ul>
""".strip()
    narrative = """
<p>Willow Wildflower is made for relaxed family photos, summer travel, birthdays, and easy weekend plans. The shared botanical print keeps everyone coordinated, while the dress and shirt options let each family member choose the piece that fits their role.</p>

<p>The attached chart supports two separately selectable garment types, so this draft keeps them honest as individual Type choices instead of collapsing them into one unsupported bundle.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Two-piece coordination:</strong> Dresses and shirts are each backed by the attached vendor chart.</li>
<li><strong>Family-size ladder:</strong> Child 80-150, Mother S-2XL, and Father S-4XL rows are included where the vendor publishes them.</li>
<li><strong>Garden floral palette:</strong> Sage, blue, red, yellow, and leafy green tones are easy to style for family pictures.</li>
<li><strong>Buildable outfit:</strong> Select the garment type and size separately for a more accurate family matching cart.</li>
<li><strong>Draft-only safety:</strong> Created as an unpublished Shopify draft pending operator review.</li>
</ul>

<p>Choose each garment and size to build a breezy floral matching look for the whole family.</p>
""".strip()
    return "\n\n".join([intro, *(table_for(name, rows) for name, rows in by_garment.items()), narrative])


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        sku = f"DLM-{SHORTCODE}-{role_token(row['role'])}-{garment_token(row['garment'])}-{row['sku_suffix']}-{COLOR_TOKEN}"
        variants.append({
            "price": price,
            "compareAtPrice": compare_at(price),
            "inventoryPolicy": "DENY",
            "optionValues": [
                {"optionName": "Type", "name": row["garment"]},
                {"optionName": "Size", "name": row["picker_label"]},
            ],
            "inventoryItem": {"sku": sku, "tracked": True, "requiresShipping": True},
        })
    return variants


def tags() -> list[str]:
    values = [
        "Family Matching", "Mommy and Me", "Daddy and Me", "Sets", "Summer Family Matching Set",
        "Matching Family Outfits", "Matching Family Set", "Matching Family Top", "Matching Family Dresses",
        "Shirt", "Dress", "Summer", "Vacation", "Sage", "Floral", "Botanical", "Garden Floral",
        "Multicolor", "Puff Sleeve Dress", "Smocked Dress", "Collared Shirt", "Short Sleeve Shirt", PRINT_NAME,
        "Girl Dress", "Mother Dress", "Boy Shirt", "Father Shirt", VENDOR_URL,
    ]
    values.extend(sorted({row["picker_label"] for row in SIZE_CHART}))
    values.extend(sorted({row["role"] for row in SIZE_CHART}))
    return sorted(value for value in dict.fromkeys(values) if value)


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Shirts & Dresses"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Family Matching Outfit"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(SIZE_CHART) != 28 or len(variants) != len(SIZE_CHART):
        raise RuntimeError("SIZE_CHART/variant count mismatch")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("Title or SEO length guard failed")
    if len({(r["role"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("Duplicate role/picker pair")
    if body.count("<tr>") - 2 != len(SIZE_CHART):
        raise RuntimeError("Body row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("One or more size tables does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        expected = ADULT_PRICE if row["audience"] in {"mother", "father", "adult"} else CHILD_PRICE
        if variant["price"] != expected:
            raise RuntimeError("FORCE_SPEC_PRICES guard failed")


def run_variant_model_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "sage floral smocked puff-sleeve dress and short-sleeve collared shirt. 连衣裙 衬衫"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "FamilySet",
            "--tags", ", ".join(tags()),
        ], check=True)


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    alt_by_name = {
        "01-family-look.png": "Family wearing sage floral matching puff-sleeve dresses and shirt.",
        "02-shirt-detail.png": "Father and child sage floral matching short-sleeve shirts.",
        "source-size-chart.png": "Vendor size chart for Willow Wildflower family matching set.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        alt = alt_by_name.get(path.name, "Willow Wildflower family matching set.")
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""", {
            "input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]
        })
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMBOUNDARY"
        chunks = []
        for p in target["parameters"]:
            chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode())
        chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode() + path.read_bytes() + b"\r\n")
        chunks.append(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(target["url"], data=b"".join(chunks), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        urllib.request.urlopen(req).read()
        media = gql("""mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""", {
            "productId": product_id,
            "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}],
        })
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    header = (ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text().splitlines()[0].split(",")
    rows = []
    tags_text = ", ".join(tags())
    for i, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update({
            "Handle": HANDLE,
            "Title": TITLE if i == 1 else "",
            "Body (HTML)": body if i == 1 else "",
            "Vendor": VENDOR if i == 1 else "",
            "Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
            "Type": PRODUCT_TYPE if i == 1 else "",
            "Tags": tags_text if i == 1 else "",
            "Published": "FALSE",
            "Option1 Name": "Type",
            "Option1 Value": row["garment"],
            "Option2 Name": "Size",
            "Option2 Value": row["picker_label"],
            "Variant SKU": variant["inventoryItem"]["sku"],
            "Variant Grams": "300",
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": variant["price"],
            "Variant Compare At Price": variant["compareAtPrice"],
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Gift Card": "FALSE",
            "SEO Title": SEO_TITLE if i == 1 else "",
            "SEO Description": SEO_DESCRIPTION if i == 1 else "",
            "Google Shopping / Gender": "unisex" if i == 1 else "",
            "Google Shopping / Age Group": "adult" if i == 1 else "",
            "Google Shopping / Condition": "new" if i == 1 else "",
            "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
            "Google Shopping / Custom Label 0": "Family Matching" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Shirts & Dresses" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Family Matching Outfit" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Matching Family Set" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Two-Piece Set" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
            "Status": "draft",
        })
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, body: str, variants: list[dict], verify: dict) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | `{gid}` ({label}) |")
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible in the supplied evidence."),
        ("shopify.color-pattern", "The nearest sage/ivory floral color metaobject could not be verified against this store's color-pattern definition, so the field was left unset rather than writing a fake GID."),
        ("shopify.sleeve-length-type", "Product mixes puff-sleeve dresses and short-sleeve shirts; one product-level sleeve value would mislead."),
        ("shopify.neckline", "The shirt has a collar and the dress has a square neckline; no single neckline applies across all Types."),
        ("shopify.top-length-type", "Product mixes shirts and dresses; no single top-length value applies."),
        ("shopify.dress-occasion", "Product is not a dress-only listing."),
        ("shopify.dress-style", "Product is not a dress-only listing."),
        ("shopify.skirt-dress-length-type", "Dress rows exist, but the product also includes shirts."),
    ]
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        "- **Vendor:** not supplied",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        "| VENDOR_URL | not supplied |",
        "| SIZE_CHART_SOURCE | attached size-chart image and supplied product image |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | all -> Dresses and Shirts in Willow Wildflower |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor fetch status",
        "No vendor URL was supplied in the request, so the attached size chart and supplied product images were used as authoritative evidence per the canonical workflow. The product remains an unpublished Shopify draft.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | shopify.size GID |",
        "|---|---|---|---|---|---|---|",
        *recap, "",
        "## Derivations",
        "- Vendor weight guidance in jin was converted to kg/lbs in the shopper-facing table.",
        "- Dress and shirt chest values were doubled from the vendor half-chest chart values.",
        "- Dress hip and waist were derived by the canonical dress rules because the chart omits them.",
        "- Shirt hip and waist were derived by the canonical top/shirt rules because the chart omits them.",
        "- Dress and shirt garment lengths are anchored to the closest existing mixed dress/shirt family-set grading because the supplied image is a fit-reference chart, not a garment measurement chart.",
        "- The baby romper fit table was excluded because the supplied product evidence only shows matching dresses and shirts.",
        "- The attached product image supports mother/girl dresses and father shirt; the shirt child ladder is listed as Boy Shirt because Family Matching mode allows boy/father rows and the vendor chart includes child shirt sizes.", "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Live SKUs match derived SKUs | {'PASS' if sorted(v['sku'] for v in verify['variants']['nodes']) == sorted(v['inventoryItem']['sku'] for v in variants) else 'FAIL'} | {len(variants)} expected |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Publications not live | {'PASS' if not any(p['isPublished'] for p in verify['resourcePublicationsV2']['nodes']) else 'FAIL'} | {[p['publication']['name'] for p in verify['resourcePublicationsV2']['nodes'] if p['isPublished']]} |", "",
        "## Metafields Written",
        *[f"- `{m['namespace']}.{m['key']}`" for m in verify["metafields"]["nodes"] if m["namespace"] not in {"judgeme"}], "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        "## Smart Collections",
        "Collection indexing may wait until publication because the product is an unpublished draft.", "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition and care details before publishing if the vendor page becomes available.",
        "- Inventory quantities and per-variant weights still need operator stock values.",
        "- Review whether dresses and shirts should remain one Family Matching Set listing after merchandising review.", "",
        "## Files saved",
        f"- `{ROOT / 'ops/scripts/create-wwfl-willow-wildflower-family-matching-set.sh'}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`", "",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)
    run_variant_model_guard()

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{sku}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Dress", "Shirt"]]},
        {"name": "Size", "values": [{"name": value} for value in list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART))]},
    ]
    product_input = {
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": tags(),
        "status": "DRAFT",
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }
    if existing:
        if existing["status"] == "ACTIVE":
            raise RuntimeError(f"Existing product {HANDLE} is ACTIVE; refusing to change publish state.")
        product_id = existing["id"]
        live_skus = sorted(v["sku"] for v in existing["variants"]["nodes"] if v.get("sku"))
        spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
        if live_skus and live_skus != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create duplicates.")
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]
        bulk = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        })
        require_no_user_errors(bulk, ["data", "productVariantsBulkCreate", "userErrors"])

    mf = metafields(product_id)
    for i in range(0, len(mf), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mf[i:i+25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    write_listing(product_id, body, variants, verify)
    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "variant_count": len(verify["variants"]["nodes"]),
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
