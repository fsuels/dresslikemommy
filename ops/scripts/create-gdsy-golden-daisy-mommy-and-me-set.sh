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

HANDLE = "golden-daisy-mommy-and-me-set"
TITLE = "Golden Daisy Mommy and Me Separates - Top or Pants"
SEO_TITLE = "Golden Daisy Mommy & Me Separates | Dress Like Mommy"
SEO_DESCRIPTION = "Golden daisy mommy-and-me separates: choose the yellow sleeveless top or ivory wide-leg pants. Sizes 1-2Y-10Y and Mom S-L."
PRINT_NAME = "Golden Daisy"
SHORTCODE = "GDSY"
COLOR_TOKEN = "GOLDIV"
COLOR_NAME = "Golden Daisy"
VENDOR_URL = "https://detail.1688.com/offer/942751267608.html?"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
MOTHER_PRICE = "31.99"
PRICE_NEIGHBOR = "red-gingham-mommy-and-me-set"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-gdsy-golden-daisy-mommy-and-me-set.sh"
CSV_HEADER_SOURCE = ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv"

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
}

SIZE_CHART = [
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","source_chest_width_cm":33.5,"chest_cm":67,"hip_cm":71,"waist_cm":67,"length_cm":37,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","source_chest_width_cm":35,"chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":40,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","source_chest_width_cm":36.5,"chest_cm":73,"hip_cm":77,"waist_cm":73,"length_cm":43,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","source_chest_width_cm":38,"chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":46,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","source_chest_width_cm":39.5,"chest_cm":79,"hip_cm":83,"waist_cm":79,"length_cm":49,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","source_chest_width_cm":41,"chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":52,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Top","garment":"Top","vendor_label":"YC8970 150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"146-155 cm","source_chest_width_cm":42.5,"chest_cm":85,"hip_cm":89,"waist_cm":85,"length_cm":55,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Top","garment":"Top","vendor_label":"YC8970 S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"155-160 cm","source_chest_width_cm":46,"chest_cm":92,"hip_cm":92,"waist_cm":80,"length_cm":64,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Top","garment":"Top","vendor_label":"YC8970 M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"160-165 cm","source_chest_width_cm":48,"chest_cm":96,"hip_cm":96,"waist_cm":84,"length_cm":66,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Top","garment":"Top","vendor_label":"YC8970 L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"57.5-65 kg","height":"165-170 cm","source_chest_width_cm":50,"chest_cm":100,"hip_cm":100,"waist_cm":88,"length_cm":68,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":0,"hip_cm":0,"waist_cm":40,"length_cm":42,"sleeve_cm":0,"pant_cm":42},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":0,"hip_cm":0,"waist_cm":42,"length_cm":46,"sleeve_cm":0,"pant_cm":46},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":0,"hip_cm":0,"waist_cm":44,"length_cm":50,"sleeve_cm":0,"pant_cm":50},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":0,"hip_cm":0,"waist_cm":46,"length_cm":55,"sleeve_cm":0,"pant_cm":55},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":0,"hip_cm":0,"waist_cm":48,"length_cm":60,"sleeve_cm":0,"pant_cm":60},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":0,"hip_cm":0,"waist_cm":50,"length_cm":65,"sleeve_cm":0,"pant_cm":65},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":0,"hip_cm":0,"waist_cm":52,"length_cm":70,"sleeve_cm":0,"pant_cm":70},
    {"audience":"child","role":"Girl Pants","garment":"Pants","vendor_label":"YC8971 150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"146-155 cm","chest_cm":0,"hip_cm":0,"waist_cm":54,"length_cm":75,"sleeve_cm":0,"pant_cm":75},
    {"audience":"mother","role":"Mother Pants","garment":"Pants","vendor_label":"YC8971 S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":0,"hip_cm":0,"waist_cm":62,"length_cm":96,"sleeve_cm":0,"pant_cm":96},
    {"audience":"mother","role":"Mother Pants","garment":"Pants","vendor_label":"YC8971 M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":0,"hip_cm":0,"waist_cm":64,"length_cm":99,"sleeve_cm":0,"pant_cm":99},
    {"audience":"mother","role":"Mother Pants","garment":"Pants","vendor_label":"YC8971 L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"57.5-65 kg","height":"165-170 cm","chest_cm":0,"hip_cm":0,"waist_cm":66,"length_cm":102,"sleeve_cm":0,"pant_cm":102},
]

TYPE_TOKEN = {"Top": "TOP", "Pants": "PNT"}
ROLE_TOKEN = {
    "Girl Top": "GRL",
    "Mother Top": "MOM",
    "Girl Pants": "GRL",
    "Mother Pants": "MOM",
}


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload, headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
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
    if value in (None, "", "-", 0, "0"):
        return "-"
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:.1f}".rstrip("0").rstrip(".")


def metric_range(text: str, unit: str) -> str:
    raw = str(text or "").strip()
    if not raw or raw == "-":
        return "-"
    return raw.replace(f" {unit}", "")


def cm(value) -> str:
    rendered = fmt_num(value)
    return "-" if rendered == "-" else rendered


def price_for(row: dict) -> str:
    return MOTHER_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{ROLE_TOKEN[row['role']]}-{TYPE_TOKEN[row['garment']]}-{row['sku_suffix']}-{COLOR_TOKEN}"


def size_values() -> list[str]:
    values: list[str] = []
    for row in SIZE_CHART:
        if row["picker_label"] not in values:
            values.append(row["picker_label"])
    return values


def type_values() -> list[str]:
    values: list[str] = []
    for row in SIZE_CHART:
        if row["garment"] not in values:
            values.append(row["garment"])
    return values


def rows_by_garment() -> dict[str, dict[str, dict]]:
    grouped: dict[str, dict[str, dict]] = {"Top": {}, "Pants": {}}
    for row in SIZE_CHART:
        grouped[row["garment"]][row["picker_label"]] = row
    return grouped


def expected_size_table_labels() -> list[str]:
    return size_values()


def expected_size_table_row_count() -> int:
    return len(expected_size_table_labels())


def build_storefront_size_table() -> str:
    grouped = rows_by_garment()
    headers = [
        "Size",
        "Age",
        "Weight (kg)",
        "Height (cm)",
        "Top Chest/Bust (cm)",
        "Top Length (cm)",
        "Pants Length (cm)",
        "Top Hip (cm)",
        "Top Waist (cm)",
        "Pants Waist (cm)",
    ]
    rows = []
    for label in expected_size_table_labels():
        top = grouped["Top"].get(label)
        pants = grouped["Pants"].get(label)
        guide = top or pants
        cells = [
            label,
            guide["age"] if guide and guide["audience"] == "child" else "-",
            metric_range(guide["weight"], "kg") if guide else "-",
            metric_range(guide["height"], "cm") if guide else "-",
            cm(top["chest_cm"]) if top else "-",
            cm(top["length_cm"]) if top else "-",
            cm(pants["pant_cm"]) if pants else "-",
            cm(top["hip_cm"]) if top else "-",
            cm(top["waist_cm"]) if top else "-",
            cm(pants["waist_cm"]) if pants else "-",
        ]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")
    return "\n".join([
        "<h3>Size Chart - Top and Pants</h3>",
        '<table id="size-chart" class="size-chart">',
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *rows,
        "</tbody></table>",
    ])


def build_body() -> str:
    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven-look fabric; exact fiber composition was not visible in the supplied chart or image.</li>",
        "<li><strong>Family story:</strong> A sunny mom-and-daughter look for garden walks, vacations, picnics, and warm-weather family photos.</li>",
        "<li><strong>Print reference:</strong> Golden Daisy pairs a mustard-yellow sleeveless top with white daisy embroidery and ivory wide-leg pants with tonal floral cutwork.</li>",
        "<li><strong>Design details:</strong> Choose the top or pants separately. The top has a relaxed sleeveless swing shape; the pants have a pull-on waist and easy wide-leg drape.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, turn inside out, line dry, and avoid bleach.</li>",
        "<li><strong>Size range:</strong> Top in Child 2 Years through Child 9-10 Years and Mother S-L; pants in Child 1-2 Years through Child 9-10 Years and Mother S-L.</li>",
        "</ul>",
        build_storefront_size_table(),
        "<p>Golden Daisy is a cheerful mommy-and-me outfit story built from two coordinated separates. The yellow sleeveless top brings the bright daisy moment, while the ivory pants add soft texture and an easy wide-leg silhouette for summer photos.</p>",
        "<p>The attached chart publishes YC8970 as the top and YC8971 as the pants, so this draft keeps the shopper picker honest with a Type choice. The size guide is keyed to the same child and mother size labels shoppers select, with dashes where a piece is not charted in that size.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Separate piece picker:</strong> Type options let shoppers choose the top or pants instead of assuming a bundled set.</li>",
        "<li><strong>Mother-daughter sizing:</strong> Chart-backed child and mother rows only; no dad or boy rows were invented.</li>",
        "<li><strong>Photo-ready palette:</strong> Mustard yellow and ivory make the matching look bright, soft, and easy to style.</li>",
        "<li><strong>Summer silhouettes:</strong> Sleeveless swing top and wide-leg pants keep the look breezy.</li>",
        "<li><strong>Chart-backed variants:</strong> Every Shopify variant maps back to a visible YC8970 or YC8971 size row.</li>",
        "</ul>",
        "<p>Choose the pieces and sizes you need to build a golden matching look for your next sunny day together.</p>",
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
        "Mommy and Me",
        "Matching Family Set",
        "Matching Family Sets",
        "Matching Family Outfits",
        "Sets",
        "Mommy and Me Set",
        "Mother Daughter Matching",
        "Girl Top",
        "Mother Top",
        "Girl Pants",
        "Mother Pants",
        "Top",
        "Pants",
        "Sleeveless Top",
        "Wide-Leg Pants",
        "Golden Daisy",
        "Daisy",
        "Floral",
        "Floral Embroidery",
        "Yellow",
        "Mustard Yellow",
        "Ivory",
        "White",
        "Summer",
        "Vacation",
        "Picnic",
        "Garden",
        "Mother S",
        "Mother M",
        "Mother L",
    ]
    values.extend(size_values())
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Matching Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Golden Daisy Floral"},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Top and Pants Separates"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Top and Pants"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Top and Pants Separates"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622104161", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/129971519585", "gid://shopify/Metaobject/130231140449"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def size_chart_table_count(body: str) -> int:
    return len(re.findall(r"<table[^>]*(?:id=[\"']size-chart[\"']|class=[\"'][^\"']*size-chart)", body, re.I))


def size_table_first_cells(body: str) -> list[str]:
    first_cells = []
    for tbody in re.findall(r"<tbody>(.*?)</tbody>", body, re.S):
        for row_html in re.findall(r"<tr>(.*?)</tr>", tbody, re.S):
            match = re.search(r"<td>(.*?)</td>", row_html, re.S)
            first_cells.append(re.sub(r"<.*?>", "", match.group(1)).strip() if match else "")
    return first_cells


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "pant_cm"}
    if len(SIZE_CHART) != 21 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        if row["picker_label"] not in SIZE_MAP:
            errors.append(f"missing shopify.size mapping for {row['picker_label']}")
        if row["garment"] == "Top" and row["chest_cm"] <= 0:
            errors.append(f"{row['vendor_label']} top row has no chest measurement")
        if row["garment"] == "Pants" and row["waist_cm"] <= 0:
            errors.append(f"{row['vendor_label']} pants row has no waist measurement")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label) pair")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"seo title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"seo description too long: {len(SEO_DESCRIPTION)}")
    if table_row_count(body) != expected_size_table_row_count():
        errors.append("body size-table row count mismatch")
    if size_chart_table_count(body) != 1:
        errors.append("body must contain exactly one storefront-readable size-chart table")
    if size_table_first_cells(body) != expected_size_table_labels():
        errors.append("body size-table first cells must match unique picker labels")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        errors.append("one or more size table does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("cost is not 50 percent of price")
    forbidden = ["1688", "Alibaba", "detail.1688.com", VENDOR_URL]
    shopper_payload = "\n".join([TITLE, SEO_TITLE, SEO_DESCRIPTION, body, PRODUCT_TYPE, ", ".join(tags())]).lower()
    for token in forbidden:
        if token.lower() in shopper_payload:
            errors.append(f"forbidden source token leaked into shopper/feed fields: {token}")
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
        evidence.write_text(json.dumps({"raw_detail_text": "YC8970 上衣 top sleeveless shirt; YC8971 裤 pants trousers"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "Sets",
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
        alt = "Mother and daughter wearing Golden Daisy matching top and ivory pants separates."
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""", {
            "input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]
        })
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMGOLDENDAISY"
        chunks = []
        for param in target["parameters"]:
            chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{param['name']}\"\r\n\r\n{param['value']}\r\n".encode())
        chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode() + path.read_bytes() + b"\r\n")
        chunks.append(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(target["url"], data=b"".join(chunks), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        urllib.request.urlopen(req, timeout=120).read()
        media = gql("""mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""", {
            "productId": product_id,
            "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}],
        })
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    with CSV_HEADER_SOURCE.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
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
            "Variant Grams": "200",
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
            "Google Shopping / Google Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
            "Google Shopping / Gender": "female",
            "Google Shopping / Age Group": "kids" if row["audience"] == "child" else "adult",
            "Google Shopping / MPN": variant["inventoryItem"]["sku"],
            "Google Shopping / Condition": "new",
            "Google Shopping / Custom Product": "FALSE",
            "Google Shopping / Custom Label 0": "Mommy and Me" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Top and Pants Separates" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Two-Role Matching" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": "Golden Daisy Floral" if i == 1 else "",
            "Style (product.metafields.custom.style)": "Top and Pants Separates" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Sets" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Matching Sets" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Top and Pants" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
            "Age group (product.metafields.shopify.age-group)": "kids, adults" if i == 1 else "",
            "Color (product.metafields.shopify.color-pattern)": "Yellow, White, Floral, Multicolor" if i == 1 else "",
            "Size (product.metafields.shopify.size)": ", ".join(SIZE_MAP[label][1] for label in size_values()) if i == 1 else "",
            "Cost per item": variant["inventoryItem"]["cost"],
            "Status": "draft",
        })
        rows.append(values)
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def verify_product(product: dict, variants: list[dict], expected_status: str, expected_published_at: str | None, expected_publications: list[str]) -> tuple[list[str], list[dict]]:
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    live_publications = sorted(node["publication"]["name"] for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"])
    errors = []
    price_rows = []
    if product["status"] != expected_status:
        errors.append(f"status is {product['status']}, expected preserved {expected_status}")
    if expected_status == "DRAFT":
        if product.get("publishedAt"):
            errors.append(f"publishedAt is {product['publishedAt']}, expected null")
        if live_publications:
            errors.append("one or more sales-channel publications is live")
    else:
        if expected_published_at and product.get("publishedAt") != expected_published_at:
            errors.append(f"publishedAt changed from {expected_published_at} to {product.get('publishedAt')}")
        if live_publications != sorted(expected_publications):
            errors.append(f"sales-channel publications changed from {sorted(expected_publications)} to {live_publications}")
        if expected_status == "ACTIVE" and not product.get("onlineStoreUrl"):
            errors.append("ACTIVE product is missing onlineStoreUrl")
    if (product["category"] or {}).get("fullName") != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {(product['category'] or {}).get('fullName')}")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    live_skus = sorted(node["sku"] for node in live_variants)
    spec_skus = sorted(spec_by_sku)
    if live_skus != spec_skus:
        errors.append("live SKUs do not match derived SKUs")
    if table_row_count(product["descriptionHtml"]) != expected_size_table_row_count():
        errors.append("size table row count does not match unique picker labels")
    if size_chart_table_count(product["descriptionHtml"]) != 1:
        errors.append("live product does not contain exactly one storefront-readable size-chart table")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)):
        errors.append("one or more live size table does not have 10 headers")
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(row["garment"], row["picker_label"]) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Type x Size option combinations do not match")
    first_cells = size_table_first_cells(product["descriptionHtml"])
    if first_cells != expected_size_table_labels():
        errors.append("size table first cells do not match unique picker labels")
    forbidden = ["1688", "Alibaba", "detail.1688.com"]
    payload = "\n".join([product["title"], product["descriptionHtml"], product["productType"], ", ".join(product["tags"]), product["seo"]["title"] or "", product["seo"]["description"] or ""]).lower()
    for token in forbidden:
        if token.lower() in payload:
            errors.append(f"forbidden source token leaked into Shopify product data: {token}")
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
    expected_metafields = {
        "custom.category1", "custom.subcategory", "custom.subcategory2", "custom.pattern",
        "custom.style", "custom.type", "mm-google-shopping.custom_product",
        "mm-google-shopping.gender", "mm-google-shopping.age_group", "mm-google-shopping.condition",
        "mm-google-shopping.custom_label_0", "mm-google-shopping.custom_label_1",
        "mm-google-shopping.custom_label_2", "mm-google-shopping.custom_label_3",
        "mm-google-shopping.custom_label_4", "shopify.age-group", "shopify.color-pattern",
        "shopify.size", "shopify.target-gender", "global.title_tag", "global.description_tag",
    }
    written_metafields = {f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"]}
    missing = sorted(expected_metafields - written_metafields)
    if missing:
        errors.append("missing expected metafields: " + ", ".join(missing))
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict], expected_status: str, expected_publications: list[str]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    live_url = verify.get("onlineStoreUrl") or "not published"
    recap = []
    variant_by_row = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    for row in SIZE_CHART:
        variant = variant_by_row[sku_for(row)]
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible in the attached chart or lifestyle image; skipped rather than guessing cotton, linen, rayon, or synthetic."),
        ("shopify.sleeve-length-type", "Top is sleeveless, but this Outfit Sets owner subtype has no confirmed writable sleeve-length standard value in this store."),
        ("shopify.neckline", "The neckline is partially visible but no owner-subtype-safe neckline value was verified for Outfit Sets."),
        ("shopify.top-length-type", "Top has exact chart lengths, but those do not map cleanly to one standard top-length type."),
        ("shopify.pants-length-type", "Pants are wide-leg/full-length visually, but no writable standard pants-length metafield definition was verified for this owner subtype."),
        ("shopify.dress-occasion", "Not applicable because the honest taxonomy is Outfit Sets."),
        ("shopify.dress-style", "Not applicable because this listing does not contain dresses."),
        ("shopify.skirt-dress-length-type", "Not applicable because this listing contains a top and pants, not a skirt or dress."),
    ]
    live_publications = sorted(p["publication"]["name"] for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"])
    smart_collections = verify["collections"]["nodes"] or []
    smart_lines = [f"- {item['title']} (`/{item['handle']}`)" for item in smart_collections] or ["- None returned immediately; draft products may not index into smart collections until publication."]
    verification_rows = [
        ("Product status preserved", verify["status"] == expected_status, f"{verify['status']} (expected {expected_status})"),
        ("PublishedAt guard", not verify.get("publishedAt") if expected_status == "DRAFT" else bool(verify.get("publishedAt")), str(verify.get("publishedAt"))),
        ("Sales-channel publications guard", not live_publications if expected_status == "DRAFT" else live_publications == sorted(expected_publications), ", ".join(live_publications) or "none"),
        ("Taxonomy fullName matches", verify["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, verify["category"]["fullName"]),
        ("Variant count matches SIZE_CHART", len(verify["variants"]["nodes"]) == len(SIZE_CHART), f"{len(verify['variants']['nodes'])} vs {len(SIZE_CHART)}"),
        ("Price and cost parity", all(row["match"] for row in price_rows), f"{len(price_rows)} variants checked"),
        ("Source URL guard", all(token not in ("\n".join([verify["title"], verify["descriptionHtml"], verify["productType"], ", ".join(verify["tags"]), verify["seo"]["title"] or "", verify["seo"]["description"] or ""]).lower()) for token in ["1688", "alibaba", "detail.1688.com"]), "no forbidden source tokens in Shopify product fields"),
        ("Size table rows", table_row_count(verify["descriptionHtml"]) == expected_size_table_row_count(), f"{table_row_count(verify['descriptionHtml'])} unique picker rows"),
        ("One storefront-readable size-chart table", size_chart_table_count(verify["descriptionHtml"]) == 1, str(size_chart_table_count(verify["descriptionHtml"]))),
        ("Size table picker keys", size_table_first_cells(verify["descriptionHtml"]) == expected_size_table_labels(), "first column matches Size option labels"),
        ("Size table headers", all(part.count("<th>") == 10 for part in re.findall(r"<table.*?</table>", verify["descriptionHtml"], re.S)), "10 headers per table"),
        ("Type x Size combinations", {tuple(option["value"] for option in node["selectedOptions"]) for node in verify["variants"]["nodes"]} == {(row["garment"], row["picker_label"]) for row in SIZE_CHART}, "Top/Pants x charted sizes"),
    ]
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        f"- **Live:** {live_url}",
        f"- **Vendor source:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Resolved to Mommy and Me because the supplied product image and chart support mother/daughter rows only; no father/boy rows were invented. |",
        "| PRIMARY_CATEGORY | auto -> Sets / Outfit Sets, with separable Top and Pants Type values |",
        "| DESIGNS_TO_LIST | both -> YC8970 top and YC8971 pants |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned Alibaba anti-bot/CAPTCHA punish markup, so the attached size-chart image and lifestyle product image were used as authoritative evidence per the canonical workflow. No source/vendor URL was written to Shopify customer-facing or feed-visible product fields.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## Pricing",
        "| Audience | Piece price | Compare-at | Cost |", "|---|---:|---:|---:|",
        f"| Girl | {CHILD_PRICE} | {compare_at(CHILD_PRICE)} | {cost_for(CHILD_PRICE)} |",
        f"| Mother | {MOTHER_PRICE} | {compare_at(MOTHER_PRICE)} | {cost_for(MOTHER_PRICE)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap, "",
        "## Derivations",
        "- The top table is labeled `YC8970` and the pants table is labeled `YC8971`, so the Shopify option model is `Type x Size`, not a Color option and not one bundled set variant per size.",
        "- Top vendor `80` has no visible top length/chest measurements, so no Top / Child 1-2 Years variant was created. Pants vendor `80` is chart-backed and was mapped to Child 1-2 Years using the store's closest honest `12-18 months` shopify.size metaobject.",
        "- Top `胸围` values are flat garment widths despite the simple column label, so they were doubled into wearable `chest_cm` values.",
        "- Top hips/waists follow the canonical top derivation rules: child top rows use `hip = chest + 4` and `waist = chest`; mother top rows use `hip = chest` and `waist = chest - 12`.",
        "- Pants waist and pant length use the vendor chart directly. Pants hip was left unavailable instead of guessed because the chart does not publish hip and the canonical derivation rules do not define a bottoms hip fallback.",
        "- Heights and weights are store-standard guidance because the attached chart does not publish height or weight guidance.",
        "- The storefront size-guide table intentionally uses one row per customer-visible Size picker label, with Top and Pants measurements side by side, because the theme resolves selected-size guidance from a single `size-chart` table keyed by the first cell.",
        f"- Pricing follows nearby Mommy and Me separable top/pants precedent from `{PRICE_NEIGHBOR}`: girl `28.99`, mother `31.99`; Cost per item is exactly 50%.", "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        *[f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |" for name, ok, detail in verification_rows], "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |" for row in price_rows], "",
        "## Metafields Written",
        *[f"- `{key}`" for key in written], "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        "## Tags Written",
        "`" + ", ".join(verify["tags"]) + "`", "",
        "## Smart Collections",
        *smart_lines, "",
        "## Manual Follow-ups",
        "- Inventory quantities remain unset / zero and need operator stock values before launch.",
        "- Confirm exact fabric composition if the vendor page becomes readable later; `shopify.fabric` is intentionally skipped for now.",
        "- Review/crop the supplied lifestyle image before a publish-live step if a cleaner product image becomes available.", "",
        "## Files saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.parent.mkdir(parents=True, exist_ok=True)
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
        {"name": "Type", "values": [{"name": value} for value in type_values()]},
        {"name": "Size", "values": [{"name": value} for value in size_values()]},
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

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status publishedAt onlineStoreUrl resourcePublicationsV2(first:20){nodes{isPublished publication{name}}} variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    if existing:
        expected_status = existing["status"]
        expected_published_at = existing.get("publishedAt")
        expected_publications = sorted(node["publication"]["name"] for node in existing["resourcePublicationsV2"]["nodes"] if node["isPublished"])
        product_input["status"] = expected_status
        product_id = existing["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
        spec_skus = {variant["inventoryItem"]["sku"] for variant in variants}
        if set(live_by_sku) != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create/delete variants automatically.")
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
        expected_status = "DRAFT"
        expected_published_at = None
        expected_publications = []
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
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle productType status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    errors, price_rows = verify_product(verify, variants, expected_status, expected_published_at, expected_publications)
    write_listing(product_id, verify, variants, price_rows, expected_status, expected_publications)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "onlineStoreUrl": verify["onlineStoreUrl"],
        "variant_count": len(verify["variants"]["nodes"]),
        "size_table_rows": table_row_count(verify["descriptionHtml"]),
        "price_cost_parity": all(row["match"] for row in price_rows),
        "source_url_guard": True,
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
