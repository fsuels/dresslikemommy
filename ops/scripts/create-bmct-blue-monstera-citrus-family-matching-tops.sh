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

python3 - <<'PY'
from __future__ import annotations

import csv
import html
import json
import mimetypes
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path


ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "blue-monstera-citrus-family-matching-tops"
TITLE = "Blue Monstera Citrus Family Matching Tops — Button-Up Shirt"
SEO_TITLE = "Blue Monstera Citrus Family Shirts | Dress Like Mommy"
SEO_DESCRIPTION = (
    "Blue monstera family matching shirts in lightweight woven-look fabric for "
    "mom, dad, girls & boys. Child 4–14 Years and Adult M-5XL."
)
PRINT_NAME = "Blue Monstera Citrus"
SHORTCODE = "BMCT"
COLOR_TOKEN = "BLUE"
COLOR_NAME = "Blue Monstera Citrus"
VENDOR_URL = ""
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Tops"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-7-2"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Clothing Tops > Shirts > Dress Shirts"
CHILD_PRICE = "24.99"
ADULT_PRICE = "27.99"
FORCE_SPEC_PRICES = True
PRICE_NEIGHBOR_HANDLE = "blue-stripe-family-matching-shirts"

SCRIPT_PATH = ROOT / "ops/scripts/create-bmct-blue-monstera-citrus-family-matching-tops.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
SOURCE_IMAGE = UPLOAD_DIR / "01-blue-monstera-citrus-shirt.png"
SHARED_SIZE_CHART = ROOT / "ops/listings/source-size-chart-family-matching-casual-shirts.png"
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

SIZE_MAP = {
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Child 12 Years": ("gid://shopify/Metaobject/129971650657", "12"),
    "Adult M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Adult L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Adult XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Adult 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Adult 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Adult 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "12.5-20 kg",
        "height": "95-110 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "15-25 kg",
        "height": "110-120 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "20-27.5 kg",
        "height": "120-130 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "25-32.5 kg",
        "height": "130-138 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "30-35 kg",
        "height": "138-145 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "160",
        "picker_label": "Child 12 Years",
        "sku_suffix": "KID12Y",
        "age": "11-12",
        "weight": "32.5-40 kg",
        "height": "145-150 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "child",
        "role": "Child Shirt",
        "garment": "Shirt",
        "vendor_label": "170",
        "picker_label": "Child 14 Years",
        "sku_suffix": "KID170",
        "age": "14",
        "weight": "35-42.5 kg",
        "height": "150-155 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "M",
        "picker_label": "Adult M",
        "sku_suffix": "M",
        "age": "—",
        "weight": "42.5-52.5 kg",
        "height": "155-165 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "L",
        "picker_label": "Adult L",
        "sku_suffix": "L",
        "age": "—",
        "weight": "52.5-60 kg",
        "height": "165-175 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "XL",
        "picker_label": "Adult XL",
        "sku_suffix": "XL",
        "age": "—",
        "weight": "60-65 kg",
        "height": "165-178 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "2XL",
        "picker_label": "Adult 2XL",
        "sku_suffix": "2XL",
        "age": "—",
        "weight": "65-72.5 kg",
        "height": "168-180 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "3XL",
        "picker_label": "Adult 3XL",
        "sku_suffix": "3XL",
        "age": "—",
        "weight": "72.5-82.5 kg",
        "height": "170-180 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "4XL",
        "picker_label": "Adult 4XL",
        "sku_suffix": "4XL",
        "age": "—",
        "weight": "82.5-90 kg",
        "height": "170-182 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "5XL",
        "picker_label": "Adult 5XL",
        "sku_suffix": "5XL",
        "age": "—",
        "weight": "90-100 kg",
        "height": "170-185 cm",
        "chest_cm": "—",
        "hip_cm": "—",
        "waist_cm": "—",
        "length_cm": "—",
        "sleeve_cm": "—",
        "pant_cm": "—",
    },
]

SIZE_TOKENS = {row["picker_label"]: row["sku_suffix"] for row in SIZE_CHART}
ROLE_TOKENS = {"Child Shirt": "KID", "Adult Shirt": "ADT"}
UNAVAILABLE_MEASUREMENT_FIELDS = (
    "chest_cm",
    "hip_cm",
    "waist_cm",
    "length_cm",
    "sleeve_cm",
    "pant_cm",
)
DESIRED_MEDIA_ALT = (
    "Blue Monstera Citrus family matching short-sleeve button-up shirt on a white background."
)


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(
        API,
        data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode()) from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False, indent=2))
    return data


def require_no_user_errors(data: dict, path: list[str]) -> None:
    current = data
    for key in path:
        current = current[key]
    if current:
        raise RuntimeError(json.dumps(current, ensure_ascii=False, indent=2))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def compare_at(price: str) -> str:
    value = Decimal(price) * Decimal("1.15")
    dollars = value.to_integral_value(rounding=ROUND_FLOOR)
    candidate = dollars + Decimal("0.99")
    if candidate < value:
        candidate = dollars + Decimal("1.99")
    return money(candidate)


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def price_for(row: dict) -> str:
    return CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE


def sku_for(row: dict) -> str:
    return (
        f"DLM-{SHORTCODE}-{ROLE_TOKENS[row['role']]}-"
        f"{SIZE_TOKENS[row['picker_label']]}-{COLOR_TOKEN}"
    )


def metric_value(value: str, unit: str) -> str:
    value = str(value).strip()
    if value in {"", "-", "—", "--"}:
        return "&mdash;"
    suffix = f" {unit}"
    if value.endswith(suffix):
        value = value[: -len(suffix)]
    return html.escape(value)


def measurement_value(value: object) -> str:
    value = str(value).strip()
    return "&mdash;" if value in {"", "-", "—", "--"} else html.escape(value)


def build_body() -> str:
    headers = [
        "Size",
        "Age",
        "Weight (kg)",
        "Height (cm)",
        "Chest/Bust (cm)",
        "Sleeve (cm)",
        "Pant/Short (cm)",
        "Hip (cm)",
        "Waist (cm)",
        "Garment Length (cm)",
    ]
    rows = []
    for row in SIZE_CHART:
        cells = [
            html.escape(row["picker_label"]),
            "&mdash;" if row["age"] in {"-", "—"} else html.escape(row["age"]),
            metric_value(row["weight"], "kg"),
            metric_value(row["height"], "cm"),
            measurement_value(row["chest_cm"]),
            measurement_value(row["sleeve_cm"]),
            measurement_value(row["pant_cm"]),
            measurement_value(row["hip_cm"]),
            measurement_value(row["waist_cm"]),
            measurement_value(row["length_cm"]),
        ]
        rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")

    return "\n".join(
        [
            "<ul>",
            "<li><strong>Fabric:</strong> Lightweight woven-look fabric; exact fiber composition was not available in the supplied evidence.</li>",
            "<li><strong>Family story:</strong> One coordinated unisex button-up shirt for children and adults, ready for vacations, family photos, and sunny days together.</li>",
            "<li><strong>Print reference:</strong> Blue Monstera Citrus combines a white ground, vivid blue monstera leaves, pale blue fronds, orange fruit, and small winged-insect accents.</li>",
            "<li><strong>Design details:</strong> Short sleeves, pointed collar, and front buttons. The white undershirt and hanger shown are styling only and are not included.</li>",
            "<li><strong>Care:</strong> Check the sewn-in care label before washing; exact wash instructions were not available in the supplied evidence.</li>",
            "<li><strong>Size range:</strong> Child 4 Years through Child 14 Years, plus Adult M through Adult 5XL.</li>",
            "</ul>",
            "",
            "<h3>Size Chart - Shirt</h3>",
            "<table id=\"size-chart\">",
            "<thead><tr>",
            *[f"<th>{header}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *rows,
            "</tbody></table>",
            "",
            "<p>Blue Monstera Citrus brings a crisp tropical palette to matching family style. Saturated blue leaves, airy pale-blue fronds, orange fruit, and small winged accents keep the white-ground shirt bright and distinctive without changing the easy button-up silhouette.</p>",
            "",
            "<p>The supplied chart provides recommended height and body-weight ranges for seven child sizes and seven adult sizes. It does not provide chest, sleeve, hip, waist, or garment-length measurements, so those table cells remain marked with an em dash rather than estimated values.</p>",
            "",
            "<h3>Key Features:</h3>",
            "<ul>",
            "<li><strong>One family silhouette:</strong> The same unisex collared button-up style is offered across the child and adult size rows.</li>",
            "<li><strong>Tropical blue print:</strong> Vivid monstera leaves and pale fronds stand out against the clean white ground.</li>",
            "<li><strong>Orange accents:</strong> Fruit motifs add warm contrast throughout the blue botanical pattern.</li>",
            "<li><strong>Warm-weather details:</strong> Short sleeves and a button front make the shirt easy to layer or wear on its own.</li>",
            "<li><strong>Single-shirt clarity:</strong> Each selected variant is one shirt; the undershirt, hanger, and accessories are not included.</li>",
            "</ul>",
            "",
            "<p>Choose one size for each family member and build a bright matching look for the next trip, gathering, or photo day.</p>",
        ]
    )


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        variants.append(
            {
                "price": price,
                "compareAtPrice": compare_at(price),
                "taxable": True,
                "inventoryPolicy": "DENY",
                "optionValues": [
                    {"optionName": "Size", "name": row["picker_label"]},
                    {"optionName": "Color", "name": COLOR_NAME},
                ],
                "inventoryItem": {
                    "sku": sku_for(row),
                    "cost": cost_for(price),
                    "tracked": True,
                    "requiresShipping": True,
                },
            }
        )
    return variants


def tags() -> list[str]:
    values = [
        "Family Matching",
        "Tops",
        "Matching Family Tops",
        "Matching Family Shirts",
        "Child Shirt",
        "Adult Shirt",
        "Unisex Family Shirt",
        "Button-Up Shirt",
        "Short Sleeve Shirt",
        "Collared Shirt",
        "Blue Monstera Citrus",
        "Monstera",
        "Tropical Leaf",
        "Orange Fruit",
        "Winged-Insect Accents",
        "Blue",
        "Pale Blue",
        "White",
        "Orange",
        "Summer",
        "Vacation",
        "Family Photos",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(
        dict.fromkeys(
            SIZE_MAP[row["picker_label"]][0]
            for row in SIZE_CHART
            if row["picker_label"] in SIZE_MAP
        )
    )
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Matching Family Shirts"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Tropical Button-Up Shirt"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Short Sleeve Button-Up Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Child & Adult"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "sleeve-length-type", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971486817"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972502625"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def source_leaks(values: list[str]) -> list[str]:
    return ["external URL"] if any(re.search(r"https?://|\bwww\.", str(value), re.I) for value in values) else []


def parse_size_table(body: str) -> tuple[list[str], list[list[str]], int]:
    match = re.search(r"<table id=\"size-chart\">(.*?)</table>", body, re.S)
    table = match.group(1) if match else ""
    rows_match = re.search(r"<tbody>(.*?)</tbody>", table, re.S)
    row_html = re.findall(r"<tr>(.*?)</tr>", rows_match.group(1) if rows_match else "", re.S)
    rows = []
    for fragment in row_html:
        cells = [
            html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()
            for cell in re.findall(r"<td>(.*?)</td>", fragment, re.S)
        ]
        rows.append(cells)
    return [row[0] for row in rows if row], rows, len(re.findall(r"<th\b", table))


def validate_preflight(body: str, variants: list[dict]) -> None:
    required = {
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
        "sleeve_cm",
        "pant_cm",
    }
    errors = []
    if not FORCE_SPEC_PRICES:
        errors.append("FORCE_SPEC_PRICES must be true")
    if len(SIZE_CHART) != 14 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART and variant count must both equal 14")
    for row in SIZE_CHART:
        missing = [field for field in required if field not in row or row[field] in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing fields: {missing}")
        if row.get("role") not in ROLE_TOKENS:
            errors.append(f"missing role token for {row.get('role')}")
        if row.get("picker_label") not in SIZE_TOKENS:
            errors.append(f"missing size token for {row.get('picker_label')}")
        for field in UNAVAILABLE_MEASUREMENT_FIELDS:
            if row.get(field) not in {"-", "—"}:
                errors.append(
                    f"{row.get('vendor_label')} {field} must remain unavailable, not inferred"
                )
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label) pair")
    if len({row["picker_label"] for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate Size option value")
    missing_size_maps = {
        row["picker_label"] for row in SIZE_CHART if row["picker_label"] not in SIZE_MAP
    }
    if missing_size_maps != {"Child 14 Years", "Adult 5XL"}:
        errors.append(f"unexpected shopify.size mapping gaps: {sorted(missing_size_maps)}")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"SEO title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"SEO description too long: {len(SEO_DESCRIPTION)}")
    first_cells, table_rows, header_count = parse_size_table(body)
    if first_cells != [row["picker_label"] for row in SIZE_CHART]:
        errors.append("size-table first cells do not exactly match picker labels")
    if len(table_rows) != len(SIZE_CHART):
        errors.append("size-table row count does not match SIZE_CHART")
    if header_count != 10:
        errors.append(f"size table has {header_count} headers instead of 10")
    if any(len(row) != 10 for row in table_rows):
        errors.append("one or more size-table rows does not have 10 cells")
    if any(cell != "—" for row in table_rows for cell in row[4:10]):
        errors.append("unavailable garment-measurement cells must remain em dashes")
    first_list = re.search(r"<ul>(.*?)</ul>", body, re.S)
    if not first_list or len(re.findall(r"<li>", first_list.group(1))) != 6:
        errors.append("canonical opening list must contain exactly six bullets")
    if body.count("<p>") != 3 or "<h3>Key Features:</h3>" not in body:
        errors.append("body must contain two narrative paragraphs, Key Features, and one CTA")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["inventoryItem"]["sku"] != sku_for(row):
            errors.append(f"SKU derivation failed for {row['picker_label']}")
        if variant["price"] != price_for(row):
            errors.append(f"FORCE_SPEC_PRICES failed for {row['picker_label']}")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append(f"cost is not 50 percent for {row['picker_label']}")
    if len({variant["inventoryItem"]["sku"] for variant in variants}) != len(variants):
        errors.append("SKUs are not unique")
    leaks = source_leaks(
        [TITLE, SEO_TITLE, SEO_DESCRIPTION, body, VENDOR, PRODUCT_TYPE, *tags()]
    )
    if leaks:
        errors.append(f"customer-visible source leak: {leaks}")
    if not SHARED_SIZE_CHART.is_file():
        errors.append(f"missing shared size chart: {SHARED_SIZE_CHART}")
    media_files = sorted(
        path
        for path in UPLOAD_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ) if UPLOAD_DIR.is_dir() else []
    if media_files != [SOURCE_IMAGE]:
        errors.append(f"upload directory must contain only {SOURCE_IMAGE.name}: {media_files}")
    if PRICE_NEIGHBOR_HANDLE != "blue-stripe-family-matching-shirts":
        errors.append("pricing precedent handle drifted")
    if VENDOR_URL:
        errors.append("vendor_url must remain empty")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory(prefix="bmct-variant-model-") as temp_dir:
        temp = Path(temp_dir)
        chart_path = temp / "size-chart.json"
        derived_path = temp / "derived.json"
        evidence_path = temp / "detail-evidence.json"
        chart_path.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived_path.write_text(
            json.dumps({"option_names": ["Size", "Color"], "variants": variants}),
            encoding="utf-8",
        )
        evidence_path.write_text(
            json.dumps(
                {
                    "title": "Family matching short-sleeve casual shirts",
                    "notes": "One unisex collared button-up shirt across child and adult sizes.",
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "python3",
                str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
                "--size-chart",
                str(chart_path),
                "--derived",
                str(derived_path),
                "--vendor-evidence",
                str(evidence_path),
                "--primary-category",
                "Tops",
                "--tags",
                ", ".join(tags()),
            ],
            check=True,
        )


def write_csv(body: str, variants: list[dict]) -> None:
    with CSV_HEADER_SOURCE.open("r", encoding="utf-8", newline="") as source:
        header = next(csv.reader(source))
    size_csv = ", ".join(row["picker_label"] for row in SIZE_CHART)
    records = []
    for index, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        first = index == 1
        record = {column: "" for column in header}
        record.update(
            {
                "Handle": HANDLE,
                "Title": TITLE if first else "",
                "Body (HTML)": body if first else "",
                "Vendor": VENDOR if first else "",
                "Product Category": EXPECTED_TAXONOMY_FULL_NAME if first else "",
                "Type": PRODUCT_TYPE if first else "",
                "Tags": ", ".join(tags()) if first else "",
                "Published": "FALSE",
                "Option1 Name": "Size",
                "Option1 Value": row["picker_label"],
                "Option2 Name": "Color",
                "Option2 Value": COLOR_NAME,
                "Variant SKU": variant["inventoryItem"]["sku"],
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": variant["price"],
                "Variant Compare At Price": variant["compareAtPrice"],
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "Gift Card": "FALSE",
                "SEO Title": SEO_TITLE if first else "",
                "SEO Description": SEO_DESCRIPTION if first else "",
                "Google Shopping / Google Product Category": EXPECTED_TAXONOMY_FULL_NAME if first else "",
                "Google Shopping / Gender": "unisex" if first else "",
                "Google Shopping / Age Group": "adult" if first else "",
                "Google Shopping / MPN": variant["inventoryItem"]["sku"],
                "Google Shopping / Condition": "new" if first else "",
                "Google Shopping / Custom Product": "FALSE" if first else "",
                "Google Shopping / Custom Label 0": "Family Matching" if first else "",
                "Google Shopping / Custom Label 1": PRINT_NAME if first else "",
                "Google Shopping / Custom Label 2": "Summer" if first else "",
                "Google Shopping / Custom Label 3": "Short Sleeve Button-Up Shirt" if first else "",
                "Google Shopping / Custom Label 4": "Unisex Child & Adult" if first else "",
                "Category1 (product.metafields.custom.category1)": "Family Matching" if first else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if first else "",
                "Style (product.metafields.custom.style)": "Tropical Button-Up Shirt" if first else "",
                "SubCategory (product.metafields.custom.subcategory)": "Tops" if first else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Matching Family Shirts" if first else "",
                "Type (product.metafields.custom.type)": "Shirt" if first else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if first else "",
                "Age group (product.metafields.shopify.age-group)": "kids, adults" if first else "",
                "Color (product.metafields.shopify.color-pattern)": "Blue, White" if first else "",
                "Size (product.metafields.shopify.size)": size_csv if first else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
        records.append(record)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=header)
        writer.writeheader()
        writer.writerows(records)


def taxonomy_guard() -> None:
    node = gql(
        """
        query($id: ID!) {
          node(id: $id) {
            __typename
            ... on TaxonomyCategory { id fullName isLeaf }
          }
        }
        """,
        {"id": TAXONOMY_GID},
    )["data"]["node"]
    if (
        node.get("__typename") != "TaxonomyCategory"
        or node.get("id") != TAXONOMY_GID
        or node.get("fullName") != EXPECTED_TAXONOMY_FULL_NAME
        or node.get("isLeaf") is not True
    ):
        raise RuntimeError(f"Taxonomy guard failed: {node}")


def existing_product() -> dict | None:
    return gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            handle
            status
            publishedAt
            onlineStoreUrl
            options { name values }
            variants(first: 100) {
              nodes {
                id
                sku
                selectedOptions { name value }
              }
            }
            resourcePublicationsV2(first: 20) {
              nodes { isPublished publication { id name } }
            }
          }
        }
        """,
        {"handle": HANDLE},
    )["data"]["productByHandle"]


def upload_media(product_id: str) -> None:
    media = gql(
        """
        query($id: ID!) {
          product(id: $id) {
            media(first: 50) {
              nodes { ... on MediaImage { id alt } }
            }
          }
        }
        """,
        {"id": product_id},
    )["data"]["product"]["media"]["nodes"]
    if DESIRED_MEDIA_ALT in {node.get("alt") or "" for node in media}:
        return

    mime = mimetypes.guess_type(SOURCE_IMAGE.name)[0] or "application/octet-stream"
    staged = gql(
        """
        mutation($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
        """,
        {
            "input": [
                {
                    "filename": SOURCE_IMAGE.name,
                    "mimeType": mime,
                    "resource": "IMAGE",
                    "httpMethod": "POST",
                }
            ]
        },
    )
    require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----DLMBMCTBOUNDARY"
    chunks = []
    for parameter in target["parameters"]:
        chunks.append(
            (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"{parameter['name']}\"\r\n\r\n"
                f"{parameter['value']}\r\n"
            ).encode()
        )
    chunks.append(
        (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{SOURCE_IMAGE.name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n"
        ).encode()
        + SOURCE_IMAGE.read_bytes()
        + b"\r\n"
    )
    chunks.append(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        target["url"],
        data=b"".join(chunks),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        response.read()
    created = gql(
        """
        mutation($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id alt } }
            userErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "media": [
                {
                    "originalSource": target["resourceUrl"],
                    "mediaContentType": "IMAGE",
                    "alt": DESIRED_MEDIA_ALT,
                }
            ],
        },
    )
    require_no_user_errors(created, ["data", "productCreateMedia", "userErrors"])


def verify_product(product: dict, variants: list[dict]) -> tuple[list[str], list[dict]]:
    errors = []
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    if product["handle"] != HANDLE:
        errors.append(f"handle is {product['handle']}")
    if product["title"] != TITLE:
        errors.append("title does not match spec")
    if product["vendor"] != VENDOR:
        errors.append("vendor does not match spec")
    if product["productType"] != PRODUCT_TYPE:
        errors.append("product type does not match spec")
    if product["status"] != "DRAFT":
        errors.append(f"status is {product['status']}, expected DRAFT")
    if product.get("publishedAt"):
        errors.append(f"publishedAt is {product['publishedAt']}, expected null")
    publications = [
        node["publication"]["name"]
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    ]
    if publications:
        errors.append(f"sales-channel publications are live: {publications}")
    if (product.get("category") or {}).get("id") != TAXONOMY_GID:
        errors.append("taxonomy GID does not match")
    if (product.get("category") or {}).get("fullName") != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append("taxonomy fullName does not match")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    live_skus = sorted(node["sku"] for node in live_variants)
    if live_skus != sorted(spec_by_sku):
        errors.append("live SKUs do not match derived SKUs")
    expected_pairs = {
        (row["picker_label"], COLOR_NAME)
        for row in SIZE_CHART
    }
    live_pairs = {
        tuple(option["value"] for option in node["selectedOptions"])
        for node in live_variants
    }
    if live_pairs != expected_pairs:
        errors.append("live Size x Color combinations do not match")
    if [option["name"] for option in product["options"]] != ["Size", "Color"]:
        errors.append("option axes are not Size / Color")
    elif set(product["options"][0]["values"]) != {
        row["picker_label"] for row in SIZE_CHART
    } or product["options"][1]["values"] != [COLOR_NAME]:
        errors.append("option values do not match SIZE_CHART and color spec")

    parity_rows = []
    for node in live_variants:
        spec = spec_by_sku.get(node["sku"])
        unit_cost = ((node.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        match = bool(spec) and all(
            [
                node["price"] == spec["price"],
                node["compareAtPrice"] == spec["compareAtPrice"],
                node["inventoryPolicy"] == "DENY",
                node["taxable"] is True,
                node["inventoryItem"]["tracked"] is True,
                node["inventoryItem"]["requiresShipping"] is True,
                unit_cost is not None,
                unit_cost is not None
                and Decimal(unit_cost) == Decimal(spec["inventoryItem"]["cost"]),
            ]
        )
        if not match:
            errors.append(f"variant parity failed for {node['sku']}")
        parity_rows.append(
            {
                "sku": node["sku"],
                "live_price": node["price"],
                "live_compare_at": node["compareAtPrice"],
                "live_cost": money(unit_cost) if unit_cost is not None else "",
                "spec_price": spec["price"] if spec else "",
                "spec_compare_at": spec["compareAtPrice"] if spec else "",
                "spec_cost": spec["inventoryItem"]["cost"] if spec else "",
                "match": match,
            }
        )

    first_cells, table_rows, header_count = parse_size_table(product["descriptionHtml"])
    if first_cells != [row["picker_label"] for row in SIZE_CHART]:
        errors.append("live size-table first cells do not match picker labels")
    if len(table_rows) != len(SIZE_CHART):
        errors.append("live size-table row count does not match SIZE_CHART")
    if header_count != 10:
        errors.append(f"live size table has {header_count} headers")
    if any(cell != "—" for row in table_rows for cell in row[4:10]):
        errors.append("live unknown garment measurements are not all em dashes")
    if any(
        any(token in cell.lower() for token in ("lbs", " in", "kg/", "cm/"))
        for row in table_rows
        for cell in row[1:]
    ):
        errors.append("live size table is not metric-only")

    expected_tags = set(tags())
    if not expected_tags.issubset(set(product["tags"])):
        errors.append("required tags are missing")
    written_metafields = {
        f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"]
    }
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
        "shopify.sleeve-length-type",
        "shopify.target-gender",
        "global.title_tag",
        "global.description_tag",
    }
    if not expected_metafields.issubset(written_metafields):
        errors.append(
            f"metafields missing: {sorted(expected_metafields - written_metafields)}"
        )
    if "shopify.fabric" in written_metafields:
        errors.append("unsupported shopify.fabric metafield is present")
    media_alts = [node.get("alt") or "" for node in product["media"]["nodes"]]
    if DESIRED_MEDIA_ALT not in media_alts:
        errors.append("owned product image was not attached with the expected alt text")
    visible_values = [
        product["title"],
        product["descriptionHtml"],
        product["vendor"],
        product["productType"],
        product["seo"]["title"] or "",
        product["seo"]["description"] or "",
        *product["tags"],
        *media_alts,
        *[
            node["value"]
            for node in product["metafields"]["nodes"]
            if f"{node['namespace']}.{node['key']}" in expected_metafields
        ],
    ]
    leaks = source_leaks(visible_values)
    if leaks:
        errors.append(f"live customer/feed fields contain source tokens: {leaks}")
    return errors, parity_rows


def write_listing(
    product_id: str,
    product: dict,
    variants: list[dict],
    parity_rows: list[dict],
    verify_errors: list[str],
) -> None:
    admin_url = (
        "https://admin.shopify.com/store/dresslikemommy/products/"
        + product_id.split("/")[-1]
    )
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    recap = []
    for row in SIZE_CHART:
        variant = spec_by_sku[sku_for(row)]
        if row["picker_label"] in SIZE_MAP:
            gid, label = SIZE_MAP[row["picker_label"]]
            size_reference = f"`{gid}` ({label})"
        else:
            size_reference = "skipped - no compatible standard size metaobject"
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | "
            f"{COLOR_NAME} | `{variant['inventoryItem']['sku']}` | "
            f"${variant['price']} | ${variant['inventoryItem']['cost']} | {size_reference} |"
        )

    published = [
        node["publication"]["name"]
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    ]
    metafield_nodes = [
        node for node in product["metafields"]["nodes"] if node["namespace"] != "judgeme"
    ]
    collections = product["collections"]["nodes"]
    skipped = [
        ("shopify.fabric", "Exact fiber composition is unknown; lightweight woven-look fabric is the narrow supported description."),
        ("shopify.care-instructions", "The supplied evidence did not include verified wash instructions."),
        ("shopify.neckline", "A collar is visible, but no verified writable collar/neckline catalog GID was established for this run."),
        ("shopify.top-length-type", "The chart does not publish garment length, so no top-length classification was inferred."),
        ("shopify.color-pattern Orange", "Orange fruit is visible in the print, but no exact verified Orange catalog GID was available; Blue and White references were written."),
        ("shopify.size Child 14 Years", "Vendor size code 170 maps to Child 14 Years; no compatible standard size metaobject is currently available."),
        ("shopify.size Adult 5XL", "The vendor row is preserved as a variant, but there is no honest 5XL catalog size match in the local map."),
        ("shopify.dress-occasion", "Not applicable to a shirt taxonomy."),
        ("shopify.dress-style", "Not applicable to a shirt taxonomy."),
        ("shopify.skirt-dress-length-type", "Not applicable to a shirt taxonomy."),
    ]
    lines = [
        f"# {TITLE}",
        "",
        f"**Status:** {'VERIFIED DRAFT' if not verify_errors else 'FAILED VERIFICATION'}",
        f"**Admin URL:** {admin_url}",
        "**Live URL:** not published",
        f"**Product GID:** `{product_id}`",
        f"**Handle:** `{HANDLE}`",
        "",
        "## Request Resolution",
        "| Field | Resolved value |",
        "|---|---|",
        "| Listing mode | Family Matching |",
        "| Primary category | Tops |",
        "| Product type | Matching Family Tops |",
        "| Taxonomy | Apparel & Accessories > Clothing > Clothing Tops > Shirts > Dress Shirts |",
        "| Variant model | Size x Color; one unisex Shirt across child and adult sizes |",
        "| Force spec prices | true |",
        "",
        "## Title and SEO",
        "| Field | Value | Characters |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## Pricing Source",
        f"A fresh Shopify readback of the current nearby active handle `{PRICE_NEIGHBOR_HANDLE}` supports child `${CHILD_PRICE}` and adult `${ADULT_PRICE}` for a Family Matching button-up shirt. FORCE_SPEC_PRICES is true, compare-at prices follow the canonical 15-percent round-up rule, and Cost per item is exactly 50 percent of each final price.",
        "",
        "## Source-of-Truth Notes",
        "- The supplied product image and shared size chart are authoritative for this draft; no unsupported source details are stored in the package.",
        "- The image visibly supports a white ground, vivid blue monstera leaves, pale blue fronds, orange fruit, and small winged-insect accents. No insect species is asserted.",
        "- Exact fiber composition is unavailable, so copy stays at `lightweight woven-look fabric` and `shopify.fabric` is skipped.",
        "- The image shows one short-sleeve collared button-up shirt. The white undershirt and hanger are styling only and are not included.",
        f"- Size-chart source: `{SHARED_SIZE_CHART}`.",
        f"- Product-image source: `{SOURCE_IMAGE}`.",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
        *recap,
        "",
        "## Size Mapping Notes",
        "- All 14 vendor rows are retained: seven child rows (`110`-`170`) and seven adult rows (`M`-`5XL`).",
        "- The source chart publishes recommended wearer height and body-weight ranges only. Chest, sleeve, pant/short, hip, waist, and garment-length values remain em dashes rather than estimates.",
        "- `160` maps to `Child 12 Years` and the supplied exact `shopify.size` GID.",
        "- Vendor size `170` maps to `Child 14 Years` using its 150-155 cm recommendation and the store's established age-label progression.",
        "- `Adult 5XL` remains a variant, but the product-level `shopify.size` list omits it because no honest 5XL GID is available.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if product['status'] == 'DRAFT' else 'FAIL'} | {product['status']} |",
        f"| publishedAt is null | {'PASS' if not product.get('publishedAt') else 'FAIL'} | {product.get('publishedAt')} |",
        f"| No sales-channel publication is live | {'PASS' if not published else 'FAIL'} | {published or 'none'} |",
        f"| Variant count is 14 | {'PASS' if len(product['variants']['nodes']) == 14 else 'FAIL'} | {len(product['variants']['nodes'])} |",
        f"| Price, compare-at, inventory, and 50-percent cost parity | {'PASS' if all(row['match'] for row in parity_rows) else 'FAIL'} | 14 derived variants |",
        f"| Final verification | {'PASS' if not verify_errors else 'FAIL'} | {'all local and Shopify readback gates passed' if not verify_errors else '; '.join(verify_errors)} |",
        "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---|---|---|---|---|---|---|",
        *[
            f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'NO'} |"
            for row in parity_rows
        ],
        "",
        "## Metafields Written",
        "| Namespace.Key | Type | Value |",
        "|---|---|---|",
        *[
            f"| `{node['namespace']}.{node['key']}` | {node['type']} | `{node['value'][:120]}{'...' if len(node['value']) > 120 else ''}` |"
            for node in metafield_nodes
        ],
        "",
        "## Metafields Skipped",
        "| Namespace.Key | Reason |",
        "|---|---|",
        *[f"| `{key}` | {reason} |" for key, reason in skipped],
        "",
        "## Tags Written",
        f"`{', '.join(product['tags'])}`",
        "",
        "## Smart Collections",
        *(
            [f"- {collection['title']} (`/{collection['handle']}`)" for collection in collections]
            if collections
            else ["- Collection indexing may wait until publication because the product is an unpublished draft."]
        ),
        "",
        "## Publication",
        "- Product remains DRAFT and unpublished.",
        "- No sales-channel publish mutation is present in this runner.",
        "- Localization is not complete until the runner footer exits zero and the handle-specific localization closeout report says `status=passed`.",
        "",
        "## Manual Follow-ups",
        "- Confirm exact fiber composition and care instructions if better source evidence becomes available before publication.",
        "- Inventory quantities and shipping weight remain unset; body-weight guidance in the chart must not be used as product shipping weight.",
        "- The corrected `Child 14 Years` shopper label is backed by vendor size 170's 150-155 cm recommendation.",
        "",
        "## Files",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{SHARED_SIZE_CHART}`",
        f"- `{SOURCE_IMAGE}`",
    ]
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard(variants)

    SIZE_CHART_OUT.write_text(
        json.dumps(SIZE_CHART, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    BODY_HTML_OUT.write_text(body + "\n", encoding="utf-8")
    write_csv(body, variants)

    taxonomy_guard()
    product_options = [
        {
            "name": "Size",
            "values": [{"name": row["picker_label"]} for row in SIZE_CHART],
        },
        {"name": "Color", "values": [{"name": COLOR_NAME}]},
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

    existing = existing_product()
    standalone_variant = False
    if existing:
        if existing["status"] != "DRAFT":
            raise RuntimeError(
                f"Existing product status is {existing['status']}; refusing to change publication state."
            )
        if existing.get("publishedAt") or any(
            node["isPublished"] for node in existing["resourcePublicationsV2"]["nodes"]
        ):
            raise RuntimeError("Existing product is published; refusing to mutate it in the draft-only runner.")
        if [option["name"] for option in existing["options"]] != ["Size", "Color"]:
            raise RuntimeError("Existing draft has unexpected option axes; refusing to mutate it.")
        expected_size_values = {row["picker_label"] for row in SIZE_CHART}
        if (
            set(existing["options"][0]["values"]) != expected_size_values
            or existing["options"][1]["values"] != [COLOR_NAME]
        ):
            raise RuntimeError("Existing draft has unexpected option values; refusing to mutate it.")
        live_nodes = existing["variants"]["nodes"]
        standalone_variant = len(live_nodes) == 1 and not (live_nodes[0].get("sku") or "").strip()
        if not standalone_variant:
            live_skus = {node["sku"] for node in live_nodes}
            expected_skus = {variant["inventoryItem"]["sku"] for variant in variants}
            live_pairs = {
                tuple(option["value"] for option in node["selectedOptions"])
                for node in live_nodes
            }
            expected_pairs = {
                tuple(option["name"] for option in variant["optionValues"])
                for variant in variants
            }
            if live_skus != expected_skus or live_pairs != expected_pairs:
                raise RuntimeError("Existing draft has unexpected variants; refusing to add, delete, or duplicate rows.")
        product_id = existing["id"]
        updated = gql(
            """
            mutation($product: ProductUpdateInput!) {
              productUpdate(product: $product) {
                product { id handle title status }
                userErrors { field message }
              }
            }
            """,
            {"product": {"id": product_id, **product_input}},
        )
        require_no_user_errors(updated, ["data", "productUpdate", "userErrors"])
    else:
        created = gql(
            """
            mutation($input: ProductInput!) {
              productCreate(input: $input) {
                product { id handle title status }
                userErrors { field message }
              }
            }
            """,
            {"input": {**product_input, "productOptions": product_options}},
        )
        require_no_user_errors(created, ["data", "productCreate", "userErrors"])
        product_id = created["data"]["productCreate"]["product"]["id"]
        standalone_variant = True

    if standalone_variant:
        variant_result = gql(
            """
            mutation(
              $productId: ID!,
              $variants: [ProductVariantsBulkInput!]!,
              $strategy: ProductVariantsBulkCreateStrategy
            ) {
              productVariantsBulkCreate(
                productId: $productId,
                variants: $variants,
                strategy: $strategy
              ) {
                productVariants {
                  id sku title price compareAtPrice inventoryPolicy
                  inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
                }
                userErrors { field message }
              }
            }
            """,
            {
                "productId": product_id,
                "variants": variants,
                "strategy": "REMOVE_STANDALONE_VARIANT",
            },
        )
        require_no_user_errors(
            variant_result, ["data", "productVariantsBulkCreate", "userErrors"]
        )
    else:
        live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"]}
        updates = []
        for variant in variants:
            sku = variant["inventoryItem"]["sku"]
            updates.append({"id": live_by_sku[sku]["id"], **variant})
        variant_result = gql(
            """
            mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
              productVariantsBulkUpdate(productId: $productId, variants: $variants) {
                productVariants {
                  id sku title price compareAtPrice inventoryPolicy
                  inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
                }
                userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": updates},
        )
        require_no_user_errors(
            variant_result, ["data", "productVariantsBulkUpdate", "userErrors"]
        )

    product_metafields = metafields(product_id)
    for offset in range(0, len(product_metafields), 25):
        result = gql(
            """
            mutation($metafields: [MetafieldsSetInput!]!) {
              metafieldsSet(metafields: $metafields) {
                metafields { namespace key type value }
                userErrors { field message }
              }
            }
            """,
            {"metafields": product_metafields[offset : offset + 25]},
        )
        require_no_user_errors(result, ["data", "metafieldsSet", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    product = gql(
        """
        query($id: ID!) {
          product(id: $id) {
            id
            title
            handle
            vendor
            productType
            status
            publishedAt
            onlineStoreUrl
            descriptionHtml
            tags
            seo { title description }
            category { id fullName }
            options { name values }
            variants(first: 100) {
              nodes {
                id
                sku
                title
                price
                compareAtPrice
                taxable
                inventoryPolicy
                selectedOptions { name value }
                inventoryItem {
                  tracked
                  requiresShipping
                  unitCost { amount currencyCode }
                }
              }
            }
            media(first: 50) {
              nodes { ... on MediaImage { id alt image { url } } }
            }
            collections(first: 50) { nodes { title handle } }
            metafields(first: 120) { nodes { namespace key type value } }
            resourcePublicationsV2(first: 20) {
              nodes { isPublished publishDate publication { id name } }
            }
          }
        }
        """,
        {"id": product_id},
    )["data"]["product"]
    VERIFY_JSON_OUT.write_text(
        json.dumps({"data": {"product": product}}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    errors, parity_rows = verify_product(product, variants)
    write_listing(product_id, product, variants, parity_rows, errors)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(
        json.dumps(
            {
                "admin_url": (
                    "https://admin.shopify.com/store/dresslikemommy/products/"
                    + product_id.split("/")[-1]
                ),
                "status": product["status"],
                "publishedAt": product["publishedAt"],
                "onlineStoreUrl": product["onlineStoreUrl"],
                "variant_count": len(product["variants"]["nodes"]),
                "price_cost_parity": all(row["match"] for row in parity_rows),
                "localization": "pending mandatory runner footer",
                "files": [
                    str(LISTING_MD),
                    str(CSV_OUT),
                    str(VERIFY_JSON_OUT),
                    str(SIZE_CHART_OUT),
                    str(BODY_HTML_OUT),
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
PY

/usr/bin/python3 "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" --handles "blue-monstera-citrus-family-matching-tops"
