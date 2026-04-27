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
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "seaside-blue-plaid-family-matching-set"
TITLE = "Seaside Blue Plaid Family Matching Set - Dress, Shirt & Romper"
SEO_TITLE = "Seaside Blue Plaid Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "95% cotton family matching set in blue plaid for mom, dad, girls, boys & babies. Sizes baby 0-3M-3Y, child 1-10Y, Mother S-XL, Father M-4XL."
PRINT_NAME = "Seaside Blue Plaid"
SHORTCODE = "SBPL"
COLOR_TOKEN = "BLUE"
COLOR_NAME = "Blue Plaid"
VENDOR_URL = "https://detail.1688.com/offer/816988376831.html"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops" / "listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops" / "listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops" / "listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops" / "listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops" / "listings" / f"body-{HANDLE}.html"

SIZE_MAP = {
    "Baby 0-3 Months": ("gid://shopify/Metaobject/129972535393", "0-3 months"),
    "Baby 6-9 Months": ("gid://shopify/Metaobject/129972666465", "6-9 months"),
    "Baby 9-12 Months": ("gid://shopify/Metaobject/129972699233", "9-12 months"),
    "Baby 12-18 Months": ("gid://shopify/Metaobject/129972797537", "12-18 months"),
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
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":60,"hip_cm":64,"waist_cm":60,"length_cm":58,"skirt_cm":58,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":65,"skirt_cm":65,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":64,"hip_cm":68,"waist_cm":64,"length_cm":72,"skirt_cm":72,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":78,"skirt_cm":78,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":84,"skirt_cm":84,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":88,"skirt_cm":88,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":92,"skirt_cm":92,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":96,"skirt_cm":96,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":86,"hip_cm":92,"waist_cm":84,"length_cm":109,"skirt_cm":109,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":90,"hip_cm":96,"waist_cm":88,"length_cm":112,"skirt_cm":112,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"59-69 kg","height":"160-170 cm","chest_cm":94,"hip_cm":100,"waist_cm":92,"length_cm":115,"skirt_cm":115,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"70-80 kg","height":"160-175 cm","chest_cm":98,"hip_cm":104,"waist_cm":96,"length_cm":118,"skirt_cm":118,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":34,"sleeve_cm":13,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":37,"sleeve_cm":14,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":40,"sleeve_cm":15,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":43,"sleeve_cm":16,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":46,"sleeve_cm":17,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":49,"sleeve_cm":18,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":52,"sleeve_cm":19,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":100,"hip_cm":104,"waist_cm":100,"length_cm":55,"sleeve_cm":20,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"50-57.5 kg","height":"165-170 cm","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":68,"sleeve_cm":23,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"57.5-67.5 kg","height":"168-173 cm","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":70,"sleeve_cm":24,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"65-79 kg","height":"170-178 cm","chest_cm":126,"hip_cm":126,"waist_cm":114,"length_cm":72,"sleeve_cm":25,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"80-89 kg","height":"175-180 cm","chest_cm":130,"hip_cm":130,"waist_cm":118,"length_cm":74,"sleeve_cm":26,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"87.5-97.5 kg","height":"175-188 cm","chest_cm":134,"hip_cm":134,"waist_cm":122,"length_cm":76,"sleeve_cm":27,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"4XL","picker_label":"Father 4XL","sku_suffix":"4XL","age":"—","weight":"97.5-115 kg","height":"178-195 cm","chest_cm":138,"hip_cm":138,"waist_cm":126,"length_cm":78,"sleeve_cm":28,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Romper","vendor_label":"66","picker_label":"Baby 0-3 Months","sku_suffix":"B03M","age":"0-3M","weight":"5-7.5 kg","height":"58-66 cm","chest_cm":59.5,"hip_cm":63.5,"waist_cm":59.5,"length_cm":48,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Romper","vendor_label":"73","picker_label":"Baby 6-9 Months","sku_suffix":"B69M","age":"6-9M","weight":"7.5-9 kg","height":"66-76 cm","chest_cm":62.5,"hip_cm":66.5,"waist_cm":62.5,"length_cm":51,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Romper","vendor_label":"80","picker_label":"Baby 9-12 Months","sku_suffix":"B912M","age":"9-12M","weight":"9-11 kg","height":"75-80 cm","chest_cm":65.5,"hip_cm":69.5,"waist_cm":65.5,"length_cm":55,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Romper","vendor_label":"90","picker_label":"Baby 12-18 Months","sku_suffix":"B1218M","age":"12-18M","weight":"11-14 kg","height":"82-90 cm","chest_cm":68.5,"hip_cm":72.5,"waist_cm":68.5,"length_cm":59,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Romper","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":71.5,"hip_cm":75.5,"waist_cm":71.5,"length_cm":63,"sleeve_cm":0,"pant_cm":0},
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


def cm_to_in(value):
    if not value:
        return "—"
    return f"{value:g} cm / {float(value) / 2.54:.1f} in"


def kg_to_lb(text: str) -> str:
    if not text or text == "—":
        return "—"
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) == 2:
        return f"{nums[0]:g}-{nums[1]:g} kg / {nums[0]*2.20462:.1f}-{nums[1]*2.20462:.1f} lbs"
    if len(nums) == 1:
        return f"{nums[0]:g} kg / {nums[0]*2.20462:.1f} lbs"
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
    return "BABY"


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


def build_body() -> str:
    by_garment: dict[str, list[dict]] = {}
    for row in SIZE_CHART:
        by_garment.setdefault(row["garment"], []).append(row)

    def table_for(garment: str, rows: list[dict]) -> str:
        measure = "Skirt Length" if garment == "Dress" else "Sleeve" if garment == "Shirt" else "Sleeve or —"
        parts = [f"<h3>Size Chart - {html.escape(garment)}</h3>", "<table id=\"size-chart\">", "<thead><tr>"]
        headers = ["Size", "Age", "Weight (kg/lbs)", "Height (cm/in)", "Chest/Bust (cm/in)", f"{measure} (cm/in)", "Pant/Short or — (cm/in)", "Hip (cm/in)", "Waist (cm/in)", "Garment Length (cm/in)"]
        parts.extend(f"<th>{h}</th>" for h in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            side = row.get("skirt_cm") if garment == "Dress" else row.get("sleeve_cm")
            cells = [
                row["picker_label"],
                row["age"],
                kg_to_lb(row["weight"]),
                cm_to_in(row["height"].replace(" cm", "")) if re.fullmatch(r"[\d.]+-[\d.]+ cm", row["height"]) is None else f"{row['height']} / " + "-".join(f"{float(n)/2.54:.1f}" for n in re.findall(r"[\d.]+", row["height"])) + " in",
                cm_to_in(row["chest_cm"]),
                cm_to_in(side),
                "—",
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            parts.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>")
        parts.append("</tbody></table>")
        return "\n".join(parts)

    intro = """
<ul>
<li><strong>Fabric:</strong> 95% cotton with a soft treated finish, based on the vendor's detail-page composition and Class A safety note.</li>
<li><strong>Family story:</strong> A full family matching look for mom, dad, girls, boys, and the littlest sibling in the same sunny blue plaid.</li>
<li><strong>Print:</strong> Seaside Blue Plaid mixes bright sky-blue gingham, soft cream checks, and small red button accents for vacation-ready photos.</li>
<li><strong>Design details:</strong> Moms and girls wear sleeveless plaid dresses, dads and boys wear short-sleeve button shirts, and babies get a coordinating sleeveless romper.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Baby 0-3M-3Y; girls and boys 1-2Y-10Y; Mother S-XL; Father M-4XL.</li>
</ul>
""".strip()
    tables = "\n\n".join(table_for(name, rows) for name, rows in by_garment.items())
    narrative = """
<p>Seaside Blue Plaid is made for relaxed family photos, beach walks, summer birthdays, and easy vacation mornings. The blue gingham keeps everyone coordinated while still letting each role feel natural: flowy dresses for moms and girls, crisp collared shirts for dads and boys, and a sweet romper for baby.</p>

<p>The look is polished without feeling precious. Red buttons add a small cheerful accent, the cotton-rich fabric keeps the mood breathable, and the matching pieces make it simple to build a family set across several ages.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Five-role coordination:</strong> Dress, shirt, and romper options cover moms, dads, girls, boys, and babies.</li>
<li><strong>Cotton-rich fabric:</strong> Vendor evidence lists 95% cotton with a soft-treatment finish.</li>
<li><strong>Blue plaid palette:</strong> Bright gingham-style checks photograph beautifully for beach and resort moments.</li>
<li><strong>Baby romper included:</strong> The attached romper chart supports baby sizes from 66 cm through 100 cm.</li>
<li><strong>Draft-only safety:</strong> Created as an unpublished Shopify draft pending operator review.</li>
</ul>

<p>Choose each role and size you need to build a cheerful family matching look for the next sunny memory.</p>
""".strip()
    return "\n\n".join([intro, tables, narrative])


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        sku = f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}"
        variants.append({
            "price": price,
            "compareAtPrice": compare_at(price),
            "inventoryPolicy": "DENY",
            "optionValues": [
                {"optionName": "Type", "name": row["garment"]},
                {"optionName": "Size", "name": row["picker_label"]},
            ],
            "inventoryItem": {
                "sku": sku,
                "tracked": True,
                "requiresShipping": True,
            },
        })
    return variants


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(SIZE_CHART) != len(variants):
        raise RuntimeError("SIZE_CHART/variant count mismatch")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("Title or SEO length guard failed")
    if len({(r["role"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("Duplicate role/picker pair")
    if body.count("<tr>") - 3 != len(SIZE_CHART):
        raise RuntimeError("Body row count mismatch")
    if any(body_part.count("<th>") != 10 for body_part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("One or more size tables does not have 10 headers")


def tags() -> list[str]:
    values = [
        "Family Matching", "Mommy and Me", "Daddy and Me", "Sets", "Summer Family Matching Set",
        "Matching Family Outfits", "Matching Family Set", "Matching Family Dress", "Matching Family Shirt",
        "Matching Family Romper", "Dress & Shirt", "Romper", "Summer", "Beach", "Resort", "Vacation",
        PRINT_NAME, "Blue", "White", "Plaid", "Gingham", "Blue Plaid", "Seaside", "Cotton",
        "Girl Dress", "Mother Dress", "Boy Shirt", "Father Shirt", "Baby Romper", "Five-Role Matching",
        VENDOR_URL,
    ]
    values.extend(sorted({row["picker_label"] for row in SIZE_CHART}))
    values.extend(sorted({row["role"] for row in SIZE_CHART}))
    return sorted(dict.fromkeys(values))


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
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress, Shirt & Romper"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Five-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69639733345","gid://shopify/Metaobject/130283143265"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "fabric", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622399073"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889","gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    alt_by_prefix = {
        "01": "Family in seaside blue plaid matching dress and shirt set.",
        "02": "Mother and daughter in seaside blue plaid sleeveless matching dresses.",
        "03": "Father and daughter in seaside blue plaid shirt and dress.",
        "04": "Family of four in seaside blue plaid matching outfits.",
        "05": "Baby in seaside blue plaid sleeveless romper.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        alt = alt_by_prefix.get(path.name[:2], "Seaside Blue Plaid family matching set.")
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
    header = (ROOT / "ops" / "listings" / "fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text().splitlines()[0].split(",")
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
            "Google Shopping / Custom Label 3": "Dress, Shirt & Romper" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Five-Role Matching" if i == 1 else "",
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


def write_listing(product: dict, body: str, variants: list[dict], verify: dict) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product['id'].split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | `{gid}` ({label}) |")
    skipped = [
        ("shopify.sleeve-length-type", "Mixed sleeveless dresses/romper and short-sleeve shirts; one product-level value would mislead."),
        ("shopify.dress-occasion", "Product taxonomy is Outfit Sets and includes shirts plus a romper, not dress-only."),
        ("shopify.dress-style", "Mixed garment listing under Outfit Sets."),
        ("shopify.skirt-dress-length-type", "Mixed garment listing; dress-only length would overstate scope."),
        ("shopify.neckline", "Different necklines across dress, shirt, and romper."),
        ("shopify.top-length-type", "Mixed garment listing; no single honest top-length value applies."),
    ]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product['id']}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached images plus logged-in 1688 detail text |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> Dress, Shirt, Romper in Blue Plaid |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor fetch status",
        "Logged-in detail enrichment succeeded. The page shows a Summer 2026 blue plaid family listing, 95% cotton, Class A safety language, one-piece dropship support, a 10-year factory, and 1件起批. The sourcing scorer still marked the candidate Reject because the page also contains high-MOQ/sold-text ambiguity and a generic brand-risk token; this product was therefore created as a Shopify draft only.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | shopify.size GID |",
        "|---|---|---|---|---|---|---|",
        *recap,
        "",
        "## Derivations",
        "- Adult and child weight guidance was converted from vendor 斤 ranges into kg/lbs in the shopper-facing table.",
        "- Dress and shirt garment measurements beyond height/weight were filled from the nearest live family-matching plaid/stripe grading already used in this catalog, then waist/hip were derived by the canonical dress/shirt rules.",
        "- Romper rows use the attached garment table directly for length and chest; romper hip and waist are derived from the canonical child garment rules.",
        "- Baby 66/73/80/90 rows were mapped to the closest live baby size metaobjects; child 80 keeps the catalog's established closest `12-18 months` size reference.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Publications not live | {'PASS' if not any(p['isPublished'] for p in verify['resourcePublicationsV2']['nodes']) else 'FAIL'} | {[p['publication']['name'] for p in verify['resourcePublicationsV2']['nodes'] if p['isPublished']]} |",
        "",
        "## Metafields Written",
        *[f"- `{m['namespace']}.{m['key']}`" for m in verify["metafields"]["nodes"] if m["namespace"] not in {"judgeme"}],
        "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped],
        "",
        "## Smart Collections",
        "Collection indexing may wait until publication because the product is an unpublished draft.",
        "",
        "## Manual Follow-ups",
        "- Review the high-MOQ/sourcing Reject risk before publishing.",
        "- Inventory quantities and per-variant weights still need operator stock values.",
        "- Consider excluding the baby romper later if merchandising wants only four-role family sets.",
        "",
        "## Files saved",
        f"- `{ROOT / 'ops' / 'scripts' / 'create-sbpl-seaside-blue-plaid-family-matching-set.sh'}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
        "",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    (ROOT / "ops" / "listings").mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{sku}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Dress", "Shirt", "Romper"]]},
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
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        live_skus = sorted(v["sku"] for v in existing["variants"]["nodes"] if v.get("sku"))
        spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
        if live_skus and live_skus != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create duplicates.")
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
    write_listing({"id": product_id}, body, variants, verify)
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
