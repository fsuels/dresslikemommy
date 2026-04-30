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
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "blue-gingham-picnic-family-matching-set"
TITLE = "Blue Gingham Picnic Family Matching Set - Skirt & Short Set"
SEO_TITLE = "Blue Gingham Picnic Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Blue gingham family set with skirt looks for mom + girls and tee-and-shorts looks for dad + boys. Child 2Y-10Y, Mother S-2XL, Father S-4XL."
PRINT_NAME = "Blue Gingham Picnic"
SHORTCODE = "BGPC"
COLOR_TOKEN = "BLUE"
VENDOR_URL = "https://detail.1688.com/offer/919618605678.html"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"

SIZE_MAP = {
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
    {"audience":"mother","role":"Mother Set","garment":"Top & Skirt Set","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"44.5-49 kg","height":"155-160 cm","chest_cm":96,"hip_cm":102,"waist_cm":94,"length_cm":64,"skirt_cm":106,"pant_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Top & Skirt Set","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"49-60 kg","height":"160-165 cm","chest_cm":102,"hip_cm":108,"waist_cm":100,"length_cm":65,"skirt_cm":108,"pant_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Top & Skirt Set","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"60-67.5 kg","height":"165-170 cm","chest_cm":106,"hip_cm":112,"waist_cm":104,"length_cm":69,"skirt_cm":110,"pant_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Top & Skirt Set","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"67.5-77.5 kg","height":"170-175 cm","chest_cm":110,"hip_cm":116,"waist_cm":108,"length_cm":71,"skirt_cm":112,"pant_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Top & Skirt Set","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"77.5-85 kg","height":"175-180 cm","chest_cm":114,"hip_cm":120,"waist_cm":112,"length_cm":73,"skirt_cm":114,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"9-12.5 kg","height":"80-90 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":39,"skirt_cm":51,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"11.5-15 kg","height":"90-100 cm","chest_cm":71,"hip_cm":75,"waist_cm":71,"length_cm":42,"skirt_cm":54,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-19 kg","height":"100-110 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":45,"skirt_cm":58,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19-23.5 kg","height":"110-120 cm","chest_cm":77,"hip_cm":81,"waist_cm":77,"length_cm":48,"skirt_cm":62,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-26 kg","height":"120-130 cm","chest_cm":79,"hip_cm":83,"waist_cm":79,"length_cm":51,"skirt_cm":66,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"26.5-31 kg","height":"130-140 cm","chest_cm":81,"hip_cm":85,"waist_cm":81,"length_cm":54,"skirt_cm":69,"pant_cm":0},
    {"audience":"child","role":"Girl Set","garment":"Top & Skirt Set","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"31-37.5 kg","height":"140-150 cm","chest_cm":83,"hip_cm":87,"waist_cm":83,"length_cm":57,"skirt_cm":73,"pant_cm":0},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"9-12.5 kg","height":"80-90 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":39,"skirt_cm":0,"pant_cm":24.8},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"11.5-15 kg","height":"90-100 cm","chest_cm":71,"hip_cm":75,"waist_cm":71,"length_cm":42,"skirt_cm":0,"pant_cm":26.3},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-19 kg","height":"100-110 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":45,"skirt_cm":0,"pant_cm":27.8},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19-23.5 kg","height":"110-120 cm","chest_cm":77,"hip_cm":81,"waist_cm":77,"length_cm":48,"skirt_cm":0,"pant_cm":29.3},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-26 kg","height":"120-130 cm","chest_cm":79,"hip_cm":83,"waist_cm":79,"length_cm":51,"skirt_cm":0,"pant_cm":31.3},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"26.5-31 kg","height":"130-140 cm","chest_cm":81,"hip_cm":85,"waist_cm":81,"length_cm":54,"skirt_cm":0,"pant_cm":33.3},
    {"audience":"child","role":"Boy Set","garment":"T-Shirt & Shorts Set","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"31-37.5 kg","height":"140-150 cm","chest_cm":83,"hip_cm":87,"waist_cm":83,"length_cm":57,"skirt_cm":0,"pant_cm":35.3},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"-","weight":"44.5-49 kg","height":"155-160 cm","chest_cm":96,"hip_cm":96,"waist_cm":84,"length_cm":64,"skirt_cm":0,"pant_cm":49},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"-","weight":"49-60 kg","height":"160-165 cm","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":65,"skirt_cm":0,"pant_cm":50.5},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"-","weight":"60-67.5 kg","height":"165-170 cm","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":69,"skirt_cm":0,"pant_cm":51.5},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"-","weight":"67.5-77.5 kg","height":"170-175 cm","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":71,"skirt_cm":0,"pant_cm":52.5},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"-","weight":"77.5-85 kg","height":"175-180 cm","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":73,"skirt_cm":0,"pant_cm":53.5},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"-","weight":"85-95 kg","height":"175-188 cm","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":75,"skirt_cm":0,"pant_cm":54.5},
    {"audience":"father","role":"Father Set","garment":"T-Shirt & Shorts Set","vendor_label":"4XL","picker_label":"Father 4XL","sku_suffix":"4XL","age":"-","weight":"95-105 kg","height":"180-190 cm","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":77,"skirt_cm":0,"pant_cm":55.5},
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


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def fmt_num(value) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:.1f}".rstrip("0").rstrip(".")


def cm_to_in(value) -> str:
    if value in (None, "", 0, "0", "-", "-"):
        return "-"
    number = float(value)
    return f"{fmt_num(number)} cm / {fmt_num(number / 2.54)} in"


def dual_range(text: str, metric_unit: str, imperial_unit: str, factor: float) -> str:
    nums = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if len(nums) >= 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} {metric_unit} / {fmt_num(nums[0] * factor)}-{fmt_num(nums[1] * factor)} {imperial_unit}"
    if len(nums) == 1:
        return f"{fmt_num(nums[0])} {metric_unit} / {fmt_num(nums[0] * factor)} {imperial_unit}"
    return html.escape(text)


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


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


def build_body() -> str:
    headers = [
        "Size",
        "Age",
        "Weight (kg/lbs)",
        "Height (cm/in)",
        "Chest/Bust (cm/in)",
        "Sleeve or Skirt (cm/in)",
        "Pant/Short or - (cm/in)",
        "Hip (cm/in)",
        "Waist (cm/in)",
        "Garment Length (cm/in)",
    ]

    def table_for(garment: str) -> str:
        rows = [row for row in SIZE_CHART if row["garment"] == garment]
        rendered = []
        for row in rows:
            cells = [
                row["picker_label"],
                row["age"] if row["audience"] == "child" else "-",
                dual_range(row["weight"], "kg", "lbs", 2.20462),
                dual_range(row["height"], "cm", "in", 1 / 2.54),
                cm_to_in(row["chest_cm"]),
                cm_to_in(row["skirt_cm"]),
                cm_to_in(row["pant_cm"]),
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            rendered.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
        return "\n".join([
            f"<h3>Size Chart - {html.escape(garment)}</h3>",
            "<table id=\"size-chart\">",
            "<thead><tr>",
            *[f"<th>{header}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *rendered,
            "</tbody></table>",
        ])

    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven-look summer fabric; exact fiber composition was not visible in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> A bright blue gingham matching look for mom, dad, girls, and boys, made for vacations, portraits, and sunny family plans.</li>",
        "<li><strong>Print:</strong> Blue Gingham Picnic pairs crisp blue-and-white checks with white skirt styling and easy white tee details.</li>",
        "<li><strong>Design details:</strong> Moms and girls wear the sleeveless blue gingham top with a white skirt, while dads and boys wear the coordinating white tee and shorts set with blue gingham panel detail.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>",
        "<li><strong>Size range:</strong> Girls and Boys Child 2 Years through Child 9-10 Years, Mother S through 2XL, and Father S through 4XL.</li>",
        "</ul>",
        table_for("Top & Skirt Set"),
        table_for("T-Shirt & Shorts Set"),
        "<p>Blue Gingham Picnic keeps the whole family coordinated without making every outfit identical. The blue gingham top-and-skirt look gives moms and girls a breezy photo-ready shape, while the white tee-and-shorts set keeps dads and boys relaxed and easy to style.</p>",
        "<p>The supplied chart supports two shopper-facing Type choices, so this draft keeps the skirt set and shorts set separate in the picker. Every listed size is backed by a row from the attached vendor chart; adult 3XL and 4XL are listed for the shorts set only because the chart does not show skirt lengths for those rows.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Four-role matching:</strong> Includes girl, boy, mother, and father rows from the attached chart.</li>",
        "<li><strong>Blue gingham coordination:</strong> A crisp checked pattern keeps the family look bright and picnic-ready.</li>",
        "<li><strong>Two Type choices:</strong> Select Top &amp; Skirt Set or T-Shirt &amp; Shorts Set before choosing size.</li>",
        "<li><strong>Sunny-day styling:</strong> Lightweight silhouettes are suited to vacations, warm-weather photos, and casual family outings.</li>",
        "<li><strong>Draft-only review:</strong> Created unpublished so merchandising can confirm fabric and stock details before launch.</li>",
        "</ul>",
        "<p>Choose each family member's Type and Size to build a coordinated blue gingham look for the next sunny memory.</p>",
    ])


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        variants.append({
            "price": price,
            "compareAtPrice": compare_at(price),
            "taxable": True,
            "inventoryPolicy": "DENY",
            "optionValues": [
                {"optionName": "Type", "name": row["garment"]},
                {"optionName": "Size", "name": row["picker_label"]},
            ],
            "inventoryItem": {
                "sku": sku_for(row),
                "cost": cost_for(price),
                "tracked": True,
                "requiresShipping": True,
            },
        })
    return variants


def tags() -> list[str]:
    values = [
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Sets",
        "Matching Family Set",
        "Matching Family Outfits",
        "Matching Family Shirt",
        "Matching Family Skirt Set",
        "Summer Family Matching Set",
        "Top & Skirt Set",
        "T-Shirt & Shorts Set",
        "Girl Set",
        "Boy Set",
        "Mother Set",
        "Father Set",
        "Blue",
        "White",
        "Plaid",
        "Blue Gingham",
        "Checkered",
        "Blue Gingham Picnic",
        "Sleeveless Top",
        "White Skirt",
        "T-Shirt",
        "Shorts Set",
        "Summer",
        "Vacation",
        "Resort",
        VENDOR_URL,
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
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
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Skirt & Short Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/130283143265"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm"}
    if len(SIZE_CHART) != 26 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        if row["picker_label"] not in SIZE_MAP:
            errors.append(f"missing shopify.size mapping for {row['picker_label']}")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label) pair")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"seo title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"seo description too long: {len(SEO_DESCRIPTION)}")
    if table_row_count(body) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        errors.append("one or more size tables does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("cost is not 50 percent of price")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"], "variants": variants}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "上衣 裙子 裤子 tee t-shirt shorts skirt family matching blue gingham plaid"}), encoding="utf-8")
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
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if "size-chart" in path.name or "size_chart" in path.name:
            continue
        alt = "Family wearing Blue Gingham Picnic matching skirt and short sets."
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
        for param in target["parameters"]:
            chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{param['name']}\"\r\n\r\n{param['value']}\r\n".encode())
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
    header = (ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
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
            "Google Shopping / Custom Label 3": "Skirt & Short Set" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Four-Role Matching" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Matching Family Set" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Two-Piece Set" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
            "Cost per item": variant["inventoryItem"]["cost"],
            "Status": "draft",
        })
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def verify_product(product: dict, variants: list[dict]) -> tuple[list[str], list[dict]]:
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    errors = []
    price_rows = []
    if product["status"] != "DRAFT":
        errors.append(f"status is {product['status']}, expected DRAFT")
    if product.get("publishedAt"):
        errors.append(f"publishedAt is {product['publishedAt']}, expected null")
    if any(node["isPublished"] for node in product["resourcePublicationsV2"]["nodes"]):
        errors.append("one or more sales-channel publications is live")
    if product["category"]["fullName"] != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {product['category']['fullName']}")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    live_skus = sorted(node["sku"] for node in live_variants)
    spec_skus = sorted(spec_by_sku)
    if live_skus != spec_skus:
        errors.append("live SKUs do not match derived SKUs")
    if table_row_count(product["descriptionHtml"]) != len(SIZE_CHART):
        errors.append("size table row count does not match SIZE_CHART")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)):
        errors.append("one or more live size table does not have 10 headers")
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(row["garment"], row["picker_label"]) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Type x Size option combinations do not match")
    for node in live_variants:
        spec = spec_by_sku.get(node["sku"])
        unit_cost = ((node.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        cost_ok = unit_cost is not None and Decimal(unit_cost) == Decimal(spec["inventoryItem"]["cost"])
        match = (
            spec is not None
            and node["price"] == spec["price"]
            and node["compareAtPrice"] == spec["compareAtPrice"]
            and node["inventoryPolicy"] == "DENY"
            and node["inventoryItem"]["tracked"]
            and node["inventoryItem"]["requiresShipping"]
            and cost_ok
        )
        if not match:
            errors.append(f"variant mismatch for {node['sku']}")
        price_rows.append({
            "sku": node["sku"],
            "live_price": node["price"],
            "live_compare_at": node["compareAtPrice"],
            "live_cost": unit_cost,
            "spec_price": spec["price"],
            "spec_compare_at": spec["compareAtPrice"],
            "spec_cost": spec["inventoryItem"]["cost"],
            "match": match,
        })
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible in the direct vendor proof or attached screenshots."),
        ("shopify.sleeve-length-type", "Product mixes sleeveless tops with tee/shorts sets; one product-level sleeve value would mislead."),
        ("shopify.neckline", "The skirt-set top and tee set do not share one reliable neckline value."),
        ("shopify.top-length-type", "Mixed outfit-set product; no single top-length value applies across both Types."),
        ("shopify.dress-occasion", "Honest Shopify taxonomy is Outfit Sets, not Dresses."),
        ("shopify.dress-style", "Mixed outfit-set listing, not a dress-only product."),
        ("shopify.skirt-dress-length-type", "Skirt rows exist, but the product also includes shorts-set rows."),
    ]
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> primary blue gingham family set shown in the attached image |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned Alibaba anti-bot/CAPTCHA markup, so the attached product and size-chart images were used as authoritative evidence per the canonical workflow. Existing blue/plaid family listings use different offer IDs or size charts, so this run created a separate draft handle and did not touch them.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
        *recap, "",
        "## Derivations",
        "- Vendor weight ranges were shown in jin and converted to kg/lbs for the shopper-facing table.",
        "- The vendor's chart publishes chest, top length, skirt length, pant length, height, and weight; hip and waist were derived from the canonical chart rules because the attached chart does not publish hip or waist.",
        "- Adult skirt lengths are visible through 2XL only, so Mother 3XL and Mother 4XL were not created; Father 3XL and Father 4XL remain backed by the pant-length rows.",
        "- The `Type` option is required because the chart contains separate skirt-set and shorts-set measurements.",
        "- Pricing was anchored to the nearby live family-set pattern from `fresh-blue-plaid-family-matching-set`: child `28.99`, adult `31.99`; Cost per item is exactly 50%.", "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| No sales-channel publications live | {'PASS' if not any(p['isPublished'] for p in verify['resourcePublicationsV2']['nodes']) else 'FAIL'} | {[p['publication']['name'] for p in verify['resourcePublicationsV2']['nodes'] if p['isPublished']]} |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |", "",
        "## Price Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |" for row in price_rows], "",
        "## Metafields Written",
        *[f"- `{key}`" for key in written], "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        "## Smart Collections",
        "Collection indexing may wait until publication because this product is an unpublished draft.", "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition before any publish-live step.",
        "- Inventory quantities and per-variant grams still need operator stock values.",
        "- Review/retouch the supplied product image before publication if needed.", "",
        "## Files saved",
        f"- `{ROOT / 'ops/scripts/create-bgpc-blue-gingham-picnic-family-matching-set.sh'}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
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
    run_variant_model_guard(variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Top & Skirt Set", "T-Shirt & Shorts Set"]]},
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

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status onlineStoreUrl variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    if existing:
        if existing["status"] == "ACTIVE":
            raise RuntimeError(f"Existing product {HANDLE} is ACTIVE; refusing to change publish state: {existing.get('onlineStoreUrl')}")
        product_id = existing["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
        spec_skus = {variant["inventoryItem"]["sku"] for variant in variants}
        if set(live_by_sku) != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create duplicates.")
        update_inputs = []
        for variant in variants:
            sku = variant["inventoryItem"]["sku"]
            update_inputs.append({
                "id": live_by_sku[sku]["id"],
                "price": variant["price"],
                "compareAtPrice": variant["compareAtPrice"],
                "taxable": True,
                "inventoryPolicy": "DENY",
                "inventoryItem": variant["inventoryItem"],
                "optionValues": variant["optionValues"],
            })
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": update_inputs,
        })
        require_no_user_errors(res, ["data", "productVariantsBulkUpdate", "userErrors"])
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        })
        require_no_user_errors(res, ["data", "productVariantsBulkCreate", "userErrors"])

    mf = metafields(product_id)
    for i in range(0, len(mf), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mf[i:i + 25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    errors, price_rows = verify_product(verify, variants)
    write_listing(product_id, verify, variants, price_rows)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "onlineStoreUrl": verify["onlineStoreUrl"],
        "variant_count": len(verify["variants"]["nodes"]),
        "price_cost_parity": all(row["match"] for row in price_rows),
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
