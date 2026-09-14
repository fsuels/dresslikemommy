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
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import requests


ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "sunlit-tropical-bloom-family-matching-tops"
TITLE = "Sunlit Tropical Bloom Family Matching Tops — Button-Up Shirt"
SEO_TITLE = "Sunlit Tropical Bloom Shirts | Dress Like Mommy"
SEO_DESCRIPTION = (
    "Sunlit tropical family matching button-up shirts for mom, dad, girls & boys. "
    "Lightweight woven-look fabric in Child 4–14 Years and Adult M-5XL."
)
PRINT_NAME = "Sunlit Tropical Bloom"
SHORTCODE = "STBL"
COLOR_TOKEN = "BLOOM"
COLOR_NAME = "Sunlit Tropical Bloom"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Tops"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-7-2"
EXPECTED_TAXONOMY_FULL_NAME = (
    "Apparel & Accessories > Clothing > Clothing Tops > Shirts > Dress Shirts"
)
FORCE_SPEC_PRICES = True
CHILD_PRICE = "24.99"
ADULT_PRICE = "27.99"
PRICE_PRECEDENT_HANDLE = "blue-stripe-family-matching-shirts"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / "01-sunlit-tropical-bloom-shirt.png"
SOURCE_SIZE_CHART = (
    ROOT / "ops/listings/source-size-chart-family-matching-casual-shirts.png"
)
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-stbl-sunlit-tropical-bloom-family-matching-tops.sh"
LOCALIZATION_CLOSEOUT = ROOT / "ops/listings" / f"{HANDLE}-localization-closeout.json"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

MEDIA_ALT = (
    "Sunlit Tropical Bloom short-sleeve family matching button-up shirt on a "
    "warm white ground with green leaves, yellow flowers, and orange blossoms."
)

AGE_GROUP_GIDS = {
    "child": "gid://shopify/Metaobject/128116523105",
    "adult": "gid://shopify/Metaobject/128116490337",
}
COLOR_PATTERN_GIDS = [
    "gid://shopify/Metaobject/69639733345",
    "gid://shopify/Metaobject/129971519585",
    "gid://shopify/Metaobject/130231140449",
]
TARGET_GENDER_GIDS = ["gid://shopify/Metaobject/129972502625"]

SIZE_MAP = {
    "Child 4 Years": (
        "gid://shopify/Metaobject/129972928609",
        "4-5 years",
    ),
    "Child 5 Years": (
        "gid://shopify/Metaobject/129972961377",
        "5-6 years",
    ),
    "Child 6-7 Years": (
        "gid://shopify/Metaobject/139840323681",
        "6-7 years",
    ),
    "Child 8 Years": (
        "gid://shopify/Metaobject/129973026913",
        "8",
    ),
    "Child 9-10 Years": (
        "gid://shopify/Metaobject/129971552353",
        "10",
    ),
    "Child 12 Years": (
        "gid://shopify/Metaobject/129971650657",
        "12",
    ),
    "Adult M": (
        "gid://shopify/Metaobject/129975222369",
        "M",
    ),
    "Adult L": (
        "gid://shopify/Metaobject/129975189601",
        "L",
    ),
    "Adult XL": (
        "gid://shopify/Metaobject/129975287905",
        "XL",
    ),
    "Adult 2XL": (
        "gid://shopify/Metaobject/129975156833",
        "2XL",
    ),
    "Adult 3XL": (
        "gid://shopify/Metaobject/139840421985",
        "3XL",
    ),
    "Adult 4XL": (
        "gid://shopify/Metaobject/139840716897",
        "4XL",
    ),
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
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
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "M",
        "picker_label": "Adult M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "42.5-52.5 kg",
        "height": "155-165 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "L",
        "picker_label": "Adult L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "52.5-60 kg",
        "height": "165-175 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "XL",
        "picker_label": "Adult XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "60-65 kg",
        "height": "165-178 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "2XL",
        "picker_label": "Adult 2XL",
        "sku_suffix": "2XL",
        "age": "-",
        "weight": "65-72.5 kg",
        "height": "168-180 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "3XL",
        "picker_label": "Adult 3XL",
        "sku_suffix": "3XL",
        "age": "-",
        "weight": "72.5-82.5 kg",
        "height": "170-180 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "4XL",
        "picker_label": "Adult 4XL",
        "sku_suffix": "4XL",
        "age": "-",
        "weight": "82.5-90 kg",
        "height": "170-182 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Shirt",
        "garment": "Shirt",
        "vendor_label": "5XL",
        "picker_label": "Adult 5XL",
        "sku_suffix": "5XL",
        "age": "-",
        "weight": "90-100 kg",
        "height": "170-185 cm",
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": "-",
        "sleeve_cm": "-",
        "pant_cm": "-",
    },
]


def gql(query: str, variables: dict | None = None) -> dict:
    response = requests.post(
        API,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
        json={"query": query, "variables": variables or {}},
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("errors"):
        raise RuntimeError(
            "GraphQL errors: " + json.dumps(data["errors"], ensure_ascii=False)
        )
    return data


def require_no_user_errors(data: dict, path: list[str]) -> None:
    current = data
    for key in path:
        current = current[key]
    if current:
        raise RuntimeError(json.dumps(current, indent=2, ensure_ascii=False))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    value = Decimal(price) * Decimal("1.15")
    dollars = math.floor(value)
    candidate = Decimal(dollars) + Decimal("0.99")
    if candidate < value:
        candidate += Decimal("1.00")
    return money(candidate)


def display_measurement(value: str, unit: str = "") -> str:
    text = str(value or "").strip()
    if not text or text in {"-", "—", "--"}:
        return "—"
    suffix = f" {unit}"
    return text[: -len(suffix)] if unit and text.endswith(suffix) else text


def role_token(role: str) -> str:
    return {"Child Shirt": "KID", "Adult Shirt": "ADT"}[role]


def price_for(row: dict) -> str:
    return CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE


def sku_for(row: dict) -> str:
    return (
        f"DLM-{SHORTCODE}-{role_token(row['role'])}-"
        f"{row['sku_suffix']}-{COLOR_TOKEN}"
    )


def mapped_size_rows() -> list[tuple[str, str, str]]:
    return [
        (row["picker_label"], *SIZE_MAP[row["picker_label"]])
        for row in SIZE_CHART
        if row["picker_label"] in SIZE_MAP
    ]


def build_tags() -> list[str]:
    values = [
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Tops",
        "Matching Family Top",
        "Matching Family Tops",
        "Matching Family Shirts",
        "Matching Family Outfits",
        "Child Shirt",
        "Adult Shirt",
        "Unisex Shirt",
        "Short Sleeve Shirt",
        "Collared Shirt",
        "Button-Up Shirt",
        "Sunlit Tropical Bloom",
        "Tropical Floral",
        "Floral",
        "Warm White",
        "Green",
        "Yellow",
        "Orange",
        "Summer",
        "Vacation",
        "Family Photos",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


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
    rendered_rows = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            display_measurement(row["age"]),
            display_measurement(row["weight"], "kg"),
            display_measurement(row["height"], "cm"),
            display_measurement(row["chest_cm"]),
            display_measurement(row["sleeve_cm"]),
            display_measurement(row["pant_cm"]),
            display_measurement(row["hip_cm"]),
            display_measurement(row["waist_cm"]),
            display_measurement(row["length_cm"]),
        ]
        rendered_rows.append(
            "<tr>"
            + "".join(
                f"<td>{html.escape(str(cell))}</td>" for cell in cells
            )
            + "</tr>"
        )

    return "\n".join(
        [
            "<ul>",
            "<li><strong>Fabric:</strong> Lightweight woven-look fabric based on the supplied product image; exact fiber content was unavailable from the supplied evidence.</li>",
            "<li><strong>Family story:</strong> One cheerful unisex button-up shirt for children and adults, designed for coordinated vacations, warm-weather outings, and family photos.</li>",
            "<li><strong>Print reference:</strong> Sunlit Tropical Bloom layers green tropical leaves, yellow flowers, and orange blossoms over a warm white ground.</li>",
            "<li><strong>Design details:</strong> Short sleeves, a pointed collar, and a button front create an easy casual shirt silhouette. The white undershirt, hanger, and necklace shown in the image are styling only and are not included.</li>",
            "<li><strong>Care:</strong> Check the sewn-in care label first; when compatible, wash cold on gentle, use mild detergent, avoid bleach, and line dry.</li>",
            "<li><strong>Size range:</strong> Child 4 Years through Child 14 Years and Adult M through Adult 5XL, all backed by the attached source chart.</li>",
            "</ul>",
            "<h3>Size Chart — Shirt</h3>",
            "<table id=\"size-chart\">",
            "<thead><tr>",
            *[f"<th>{header}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *rendered_rows,
            "</tbody></table>",
            "<p>Sunlit Tropical Bloom brings a bright resort mood to one relaxed family shirt. The warm white ground keeps the dense foliage feeling light, while yellow flowers and orange blossoms add a sunny color story that coordinates easily across child and adult sizes.</p>",
            "<p>The source chart supplies recommended fit height and weight only. Chest/bust, sleeve, pant/short, hip, waist, and garment-length measurements were not provided, so those table cells remain unavailable rather than being estimated. Choose by the charted height and weight and size up when between ranges or when a roomier fit is preferred.</p>",
            "<h3>Key Features:</h3>",
            "<ul>",
            "<li><strong>One family print:</strong> The same tropical floral artwork coordinates child and adult shirts.</li>",
            "<li><strong>Warm-weather shape:</strong> Short sleeves, a collar, and a button front suit vacations, beach days, and casual celebrations.</li>",
            "<li><strong>Inclusive unisex sizing:</strong> Seven child rows and seven adult rows come directly from the source chart.</li>",
            "<li><strong>Honest fit guidance:</strong> Recommended height and weight are published in metric units without invented garment measurements.</li>",
            "<li><strong>Single-garment scope:</strong> This listing includes one shirt per selected variant; the undershirt, hanger, necklace, and other styling pieces are not included.</li>",
            "</ul>",
            "<p>Choose each family member's size and bring Sunlit Tropical Bloom along for your next photo day, getaway, or sunny plan together.</p>",
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
                    {
                        "optionName": "Size",
                        "name": row["picker_label"],
                    },
                    {
                        "optionName": "Color",
                        "name": COLOR_NAME,
                    },
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


def build_metafields(product_id: str) -> list[dict]:
    size_refs = [gid for _, gid, _ in mapped_size_rows()]
    age_refs = [
        AGE_GROUP_GIDS[audience]
        for audience in ("child", "adult")
        if any(row["audience"] == audience for row in SIZE_CHART)
    ]
    return [
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "category1",
            "type": "single_line_text_field",
            "value": "Family Matching",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "subcategory",
            "type": "single_line_text_field",
            "value": "Tops",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "subcategory2",
            "type": "single_line_text_field",
            "value": "Family Matching Shirts",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "pattern",
            "type": "single_line_text_field",
            "value": PRINT_NAME,
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "style",
            "type": "single_line_text_field",
            "value": "Tropical Button-Up Shirt",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "type",
            "type": "single_line_text_field",
            "value": "Top",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_product",
            "type": "boolean",
            "value": "false",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "gender",
            "type": "single_line_text_field",
            "value": "unisex",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "age_group",
            "type": "single_line_text_field",
            "value": "adult",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "condition",
            "type": "single_line_text_field",
            "value": "new",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_0",
            "type": "single_line_text_field",
            "value": "Family Matching",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_1",
            "type": "single_line_text_field",
            "value": PRINT_NAME,
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_2",
            "type": "single_line_text_field",
            "value": "Summer",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_3",
            "type": "single_line_text_field",
            "value": "Tropical Button-Up Shirt",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_4",
            "type": "single_line_text_field",
            "value": "Unisex Family Top",
        },
        {
            "ownerId": product_id,
            "namespace": "shopify",
            "key": "age-group",
            "type": "list.metaobject_reference",
            "value": json.dumps(age_refs),
        },
        {
            "ownerId": product_id,
            "namespace": "shopify",
            "key": "color-pattern",
            "type": "list.metaobject_reference",
            "value": json.dumps(COLOR_PATTERN_GIDS),
        },
        {
            "ownerId": product_id,
            "namespace": "shopify",
            "key": "size",
            "type": "list.metaobject_reference",
            "value": json.dumps(size_refs),
        },
        {
            "ownerId": product_id,
            "namespace": "shopify",
            "key": "target-gender",
            "type": "list.metaobject_reference",
            "value": json.dumps(TARGET_GENDER_GIDS),
        },
        {
            "ownerId": product_id,
            "namespace": "global",
            "key": "title_tag",
            "type": "single_line_text_field",
            "value": SEO_TITLE,
        },
        {
            "ownerId": product_id,
            "namespace": "global",
            "key": "description_tag",
            "type": "single_line_text_field",
            "value": SEO_DESCRIPTION,
        },
    ]


def table_parts(body: str) -> tuple[list[str], list[list[str]]]:
    table_match = re.search(
        r"<table id=\"size-chart\">.*?</table>",
        body,
        re.S,
    )
    table = table_match.group(0) if table_match else ""
    headers = [
        re.sub(r"<[^>]+>", "", value).strip()
        for value in re.findall(r"<th>(.*?)</th>", table, re.S)
    ]
    tbody_match = re.search(r"<tbody>(.*?)</tbody>", table, re.S)
    tbody = tbody_match.group(1) if tbody_match else ""
    rows = []
    for row_html in re.findall(r"<tr>(.*?)</tr>", tbody, re.S):
        rows.append(
            [
                html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()
                for cell in re.findall(r"<td>(.*?)</td>", row_html, re.S)
            ]
        )
    return headers, rows


def shopper_payload(
    body: str,
    tags: list[str],
    metafields: list[dict] | None = None,
) -> str:
    parts = [
        TITLE,
        SEO_TITLE,
        SEO_DESCRIPTION,
        body,
        PRODUCT_TYPE,
        VENDOR,
        ", ".join(tags),
    ]
    if metafields:
        parts.extend(item["value"] for item in metafields)
    return "\n".join(parts).lower()


def source_leak_errors(payload: str) -> list[str]:
    if re.search(r"(?:https?://|www\.)", payload, re.I):
        return ["URL-like text found in shopper/feed payload"]
    return []


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required_fields = {
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
    if len(SIZE_CHART) != 14 or len(variants) != 14:
        errors.append("SIZE_CHART and variant count must both equal 14")
    for row in SIZE_CHART:
        missing = [
            field
            for field in required_fields
            if field not in row or row[field] in (None, "")
        ]
        if missing:
            errors.append(
                f"{row.get('vendor_label', 'unknown')} missing {missing}"
            )
        if row["garment"] != "Shirt":
            errors.append(f"non-shirt garment row: {row['vendor_label']}")
        if row["audience"] not in {"child", "adult"}:
            errors.append(f"invalid audience: {row['audience']}")
        for field in (
            "chest_cm",
            "hip_cm",
            "waist_cm",
            "length_cm",
            "sleeve_cm",
            "pant_cm",
        ):
            if row[field] != "-":
                errors.append(
                    f"{row['vendor_label']} invents unavailable {field}"
                )

    if len(
        {(row["role"], row["picker_label"]) for row in SIZE_CHART}
    ) != len(SIZE_CHART):
        errors.append("duplicate role/picker pair")
    if len({row["picker_label"] for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate Size option value")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"SEO title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"SEO description too long: {len(SEO_DESCRIPTION)}")
    if not FORCE_SPEC_PRICES:
        errors.append("FORCE_SPEC_PRICES must be true")

    expected_skus = [sku_for(row) for row in SIZE_CHART]
    actual_skus = [
        variant["inventoryItem"]["sku"] for variant in variants
    ]
    if len(set(actual_skus)) != 14 or sorted(actual_skus) != sorted(expected_skus):
        errors.append("SKUs are not the unique values derived from SIZE_CHART")

    for row, variant in zip(SIZE_CHART, variants):
        expected_price = price_for(row)
        if variant["price"] != expected_price:
            errors.append(f"price mismatch for {row['picker_label']}")
        if variant["compareAtPrice"] != compare_at(expected_price):
            errors.append(f"compare-at mismatch for {row['picker_label']}")
        if variant["inventoryItem"]["cost"] != cost_for(expected_price):
            errors.append(f"cost mismatch for {row['picker_label']}")
        option_pair = tuple(
            item["name"] for item in variant["optionValues"]
        )
        if option_pair != (row["picker_label"], COLOR_NAME):
            errors.append(f"option mismatch for {row['picker_label']}")

    headers, table_rows = table_parts(body)
    if len(headers) != 10:
        errors.append(f"size table has {len(headers)} headers, expected 10")
    if len(table_rows) != 14:
        errors.append(
            f"size table has {len(table_rows)} rows, expected 14"
        )
    first_cells = [row[0] for row in table_rows if row]
    if first_cells != [row["picker_label"] for row in SIZE_CHART]:
        errors.append("size-table first column does not match picker labels")
    if any(len(row) != 10 for row in table_rows):
        errors.append("one or more size-table rows lacks 10 cells")
    lead = body.split("<h3>", 1)[0]
    if lead.count("<li>") != 6:
        errors.append("body must begin with exactly 6 bullets")
    if body.count("<p>") != 3:
        errors.append("body must contain two narrative paragraphs and one CTA")
    key_section = body.split("<h3>Key Features:</h3>", 1)
    if len(key_section) != 2 or key_section[1].count("<li>") != 5:
        errors.append("Key Features section must contain exactly 5 bullets")
    if "fit height and weight only" not in body:
        errors.append("body lacks the fit-height/weight limitation")
    if "were not provided" not in body:
        errors.append("body lacks unavailable-measurements disclosure")

    if "Child 14 Years" in SIZE_MAP or "Adult 5XL" in SIZE_MAP:
        errors.append("unsupported size metaobject mapping was invented")
    if SIZE_MAP.get("Child 12 Years", ("",))[0] != (
        "gid://shopify/Metaobject/129971650657"
    ):
        errors.append("Child 12 Years size GID mismatch")
    preflight_metafields = build_metafields("gid://shopify/Product/0")
    if any(
        item["namespace"] == "shopify" and item["key"] == "fabric"
        for item in preflight_metafields
    ):
        errors.append("shopify.fabric must be skipped")

    if not SOURCE_SIZE_CHART.is_file():
        errors.append(f"missing source size chart: {SOURCE_SIZE_CHART}")
    if not PRODUCT_IMAGE.is_file():
        errors.append(f"missing product image: {PRODUCT_IMAGE}")
    actual_uploads = sorted(
        path.name for path in UPLOAD_DIR.iterdir() if path.is_file()
    )
    if actual_uploads != [PRODUCT_IMAGE.name]:
        errors.append(
            "upload directory must contain only the owned product image: "
            + json.dumps(actual_uploads)
        )
    if not CSV_HEADER_SOURCE.is_file():
        errors.append(f"missing CSV header source: {CSV_HEADER_SOURCE}")

    errors.extend(
        source_leak_errors(
            shopper_payload(body, build_tags(), preflight_metafields)
        )
    )
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as temp:
        temp_dir = Path(temp)
        size_chart_path = temp_dir / "size-chart.json"
        derived_path = temp_dir / "derived.json"
        evidence_path = temp_dir / "vendor-evidence.json"
        size_chart_path.write_text(
            json.dumps(SIZE_CHART),
            encoding="utf-8",
        )
        derived_path.write_text(
            json.dumps(
                {
                    "option_names": ["Size", "Color"],
                    "variants": variants,
                }
            ),
            encoding="utf-8",
        )
        evidence_path.write_text(
            json.dumps(
                {
                    "title": "family matching short-sleeve casual shirt",
                    "notes": (
                        "one unisex collared button-up shirt across child "
                        "and adult sizes; styling accessories are not included"
                    ),
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "python3",
                str(
                    ROOT
                    / "ops/scripts/validate_listing_variant_model.py"
                ),
                "--size-chart",
                str(size_chart_path),
                "--derived",
                str(derived_path),
                "--vendor-evidence",
                str(evidence_path),
                "--primary-category",
                "Tops",
                "--tags",
                ", ".join(build_tags()),
            ],
            check=True,
        )


def assert_taxonomy() -> None:
    data = gql(
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
        {"id": TAXONOMY_GID},
    )
    node = data["data"]["node"]
    if (
        node.get("__typename") != "TaxonomyCategory"
        or node.get("id") != TAXONOMY_GID
        or node.get("fullName") != EXPECTED_TAXONOMY_FULL_NAME
        or node.get("isLeaf") is not True
    ):
        raise RuntimeError(
            "Taxonomy guard failed: "
            + json.dumps(node, ensure_ascii=False)
        )


def fetch_existing() -> dict | None:
    return gql(
        """
        query ExistingProduct($handle: String!) {
          productByHandle(handle: $handle) {
            id
            status
            publishedAt
            onlineStoreUrl
            options {
              name
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
                }
              }
            }
            metafields(first: 100) {
              nodes {
                namespace
                key
                value
              }
            }
            resourcePublicationsV2(first: 20) {
              nodes {
                isPublished
                publication {
                  id
                  name
                }
              }
            }
          }
        }
        """,
        {"handle": HANDLE},
    )["data"]["productByHandle"]


def assert_existing_is_safe(existing: dict, variants: list[dict]) -> str:
    if existing["status"] != "DRAFT":
        raise RuntimeError(
            f"Existing product is {existing['status']}; refusing to change it"
        )
    if existing.get("publishedAt"):
        raise RuntimeError(
            "Existing product has publishedAt; refusing draft workflow update"
        )
    if any(
        node.get("isPublished")
        for node in existing["resourcePublicationsV2"]["nodes"]
    ):
        raise RuntimeError(
            "Existing product is channel-published; refusing update"
        )
    if any(
        node["namespace"] == "shopify" and node["key"] == "fabric"
        for node in existing["metafields"]["nodes"]
    ):
        raise RuntimeError(
            "Existing draft has unsupported shopify.fabric; manual review required"
        )

    media_alts = [node.get("alt") or "" for node in existing["media"]["nodes"]]
    if any(alt != MEDIA_ALT for alt in media_alts):
        raise RuntimeError(
            "Existing draft has unexpected media; refusing destructive cleanup"
        )
    if media_alts.count(MEDIA_ALT) > 1:
        raise RuntimeError(
            "Existing draft has duplicate owned media; manual review required"
        )

    if [option["name"] for option in existing["options"]] != [
        "Size",
        "Color",
    ]:
        raise RuntimeError(
            "Existing draft option axes are not Size / Color"
        )

    live_variants = existing["variants"]["nodes"]
    if len(live_variants) == 1 and not live_variants[0].get("sku"):
        return "standalone"

    expected_by_pair = {
        tuple(value["name"] for value in spec["optionValues"]):
        spec["inventoryItem"]["sku"]
        for spec in variants
    }
    live_by_pair = {
        tuple(
            option["value"]
            for option in sorted(
                node["selectedOptions"],
                key=lambda item: 0 if item["name"] == "Size" else 1,
            )
        ): node["sku"]
        for node in live_variants
    }
    if live_by_pair != expected_by_pair:
        raise RuntimeError(
            "Existing draft variant shape/SKUs differ from the 14-row spec; "
            "refusing create/delete operations"
        )
    return "update"


def create_or_update_product(
    body: str,
    variants: list[dict],
) -> str:
    product_input = {
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": build_tags(),
        "status": "DRAFT",
        "category": TAXONOMY_GID,
        "seo": {
            "title": SEO_TITLE,
            "description": SEO_DESCRIPTION,
        },
    }
    product_options = [
        {
            "name": "Size",
            "values": [
                {"name": row["picker_label"]} for row in SIZE_CHART
            ],
        },
        {
            "name": "Color",
            "values": [{"name": COLOR_NAME}],
        },
    ]

    existing = fetch_existing()
    mode = "new"
    if existing:
        mode = assert_existing_is_safe(existing, variants)
        product_id = existing["id"]
        result = gql(
            """
            mutation ProductUpdate($product: ProductUpdateInput!) {
              productUpdate(product: $product) {
                product {
                  id
                  handle
                  status
                }
                userErrors {
                  field
                  message
                }
              }
            }
            """,
            {"product": {"id": product_id, **product_input}},
        )
        require_no_user_errors(
            result,
            ["data", "productUpdate", "userErrors"],
        )
    else:
        result = gql(
            """
            mutation ProductCreate($input: ProductInput!) {
              productCreate(input: $input) {
                product {
                  id
                  handle
                  status
                }
                userErrors {
                  field
                  message
                }
              }
            }
            """,
            {
                "input": {
                    **product_input,
                    "productOptions": product_options,
                }
            },
        )
        require_no_user_errors(
            result,
            ["data", "productCreate", "userErrors"],
        )
        product_id = result["data"]["productCreate"]["product"]["id"]

    if mode in {"new", "standalone"}:
        result = gql(
            """
            mutation ProductVariantsBulkCreate(
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
                  id
                  sku
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
        require_no_user_errors(
            result,
            ["data", "productVariantsBulkCreate", "userErrors"],
        )
    else:
        live_by_pair = {
            tuple(
                option["value"]
                for option in sorted(
                    node["selectedOptions"],
                    key=lambda item: (
                        0 if item["name"] == "Size" else 1
                    ),
                )
            ): node
            for node in existing["variants"]["nodes"]
        }
        update_inputs = []
        for spec in variants:
            pair = tuple(
                item["name"] for item in spec["optionValues"]
            )
            update_inputs.append(
                {
                    "id": live_by_pair[pair]["id"],
                    **spec,
                }
            )
        result = gql(
            """
            mutation ProductVariantsBulkUpdate(
              $productId: ID!,
              $variants: [ProductVariantsBulkInput!]!
            ) {
              productVariantsBulkUpdate(
                productId: $productId,
                variants: $variants
              ) {
                productVariants {
                  id
                  sku
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
                "variants": update_inputs,
            },
        )
        require_no_user_errors(
            result,
            ["data", "productVariantsBulkUpdate", "userErrors"],
        )
    return product_id


def write_metafields(product_id: str) -> None:
    values = build_metafields(product_id)
    for index in range(0, len(values), 25):
        result = gql(
            """
            mutation MetafieldsSet(
              $metafields: [MetafieldsSetInput!]!
            ) {
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
            {"metafields": values[index : index + 25]},
        )
        require_no_user_errors(
            result,
            ["data", "metafieldsSet", "userErrors"],
        )


def upload_owned_media(product_id: str) -> None:
    lookup = gql(
        """
        query ProductMedia($id: ID!) {
          product(id: $id) {
            media(first: 50) {
              nodes {
                ... on MediaImage {
                  id
                  alt
                }
              }
            }
          }
        }
        """,
        {"id": product_id},
    )
    alts = [
        node.get("alt") or ""
        for node in lookup["data"]["product"]["media"]["nodes"]
    ]
    if any(alt != MEDIA_ALT for alt in alts):
        raise RuntimeError(
            "Unexpected existing media; refusing destructive cleanup"
        )
    if alts.count(MEDIA_ALT) > 1:
        raise RuntimeError("Duplicate owned media already exists")
    if MEDIA_ALT in alts:
        return

    mime = (
        mimetypes.guess_type(PRODUCT_IMAGE.name)[0]
        or "application/octet-stream"
    )
    staged = gql(
        """
        mutation StagedUploadsCreate(
          $input: [StagedUploadInput!]!
        ) {
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
                    "filename": PRODUCT_IMAGE.name,
                    "mimeType": mime,
                    "resource": "IMAGE",
                    "httpMethod": "POST",
                }
            ]
        },
    )
    require_no_user_errors(
        staged,
        ["data", "stagedUploadsCreate", "userErrors"],
    )
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    form_data = {
        item["name"]: item["value"] for item in target["parameters"]
    }
    with PRODUCT_IMAGE.open("rb") as image_handle:
        response = requests.post(
            target["url"],
            data=form_data,
            files={
                "file": (
                    PRODUCT_IMAGE.name,
                    image_handle,
                    mime,
                )
            },
            timeout=120,
        )
        response.raise_for_status()

    created = gql(
        """
        mutation ProductCreateMedia(
          $productId: ID!,
          $media: [CreateMediaInput!]!
        ) {
          productCreateMedia(
            productId: $productId,
            media: $media
          ) {
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
                    "originalSource": target["resourceUrl"],
                    "mediaContentType": "IMAGE",
                    "alt": MEDIA_ALT,
                }
            ],
        },
    )
    require_no_user_errors(
        created,
        ["data", "productCreateMedia", "userErrors"],
    )


def fetch_verify(product_id: str) -> dict:
    return gql(
        """
        query VerifyProduct($id: ID!) {
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
            seo {
              title
              description
            }
            category {
              id
              fullName
            }
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
                taxable
                inventoryPolicy
                selectedOptions {
                  name
                  value
                }
                inventoryItem {
                  tracked
                  requiresShipping
                  unitCost {
                    amount
                    currencyCode
                  }
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
              }
            }
            metafields(first: 120) {
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
    )["data"]["product"]


def verify_product(
    product: dict,
    variants: list[dict],
) -> tuple[list[tuple[str, bool, str]], list[dict], list[str]]:
    checks = []

    def add(label: str, passed: bool, detail: str) -> None:
        checks.append((label, passed, detail))

    add("Handle matches", product["handle"] == HANDLE, product["handle"])
    add("Title matches", product["title"] == TITLE, product["title"])
    add("Vendor matches", product["vendor"] == VENDOR, product["vendor"])
    add(
        "Product type matches",
        product["productType"] == PRODUCT_TYPE,
        product["productType"],
    )
    add("Status is DRAFT", product["status"] == "DRAFT", product["status"])
    add(
        "publishedAt is null",
        product.get("publishedAt") is None,
        str(product.get("publishedAt")),
    )
    live_publications = [
        node
        for node in product["resourcePublicationsV2"]["nodes"]
        if node.get("isPublished")
    ]
    add(
        "No sales-channel publication is live",
        not live_publications,
        str(
            [
                node["publication"]["name"]
                for node in live_publications
            ]
        ),
    )
    add(
        "Taxonomy GID matches",
        (product["category"] or {}).get("id") == TAXONOMY_GID,
        (product["category"] or {}).get("id") or "missing",
    )
    add(
        "Taxonomy fullName matches",
        (product["category"] or {}).get("fullName")
        == EXPECTED_TAXONOMY_FULL_NAME,
        (product["category"] or {}).get("fullName") or "missing",
    )
    add(
        "Options are Size / Color",
        [option["name"] for option in product["options"]]
        == ["Size", "Color"],
        str([option["name"] for option in product["options"]]),
    )

    live_variants = product["variants"]["nodes"]
    spec_by_sku = {
        variant["inventoryItem"]["sku"]: variant
        for variant in variants
    }
    live_skus = [node["sku"] for node in live_variants]
    add(
        "Variant count is 14",
        len(live_variants) == 14,
        str(len(live_variants)),
    )
    add(
        "SKUs are unique",
        len(set(live_skus)) == len(live_skus) == 14,
        str(len(set(live_skus))),
    )
    add(
        "Live SKUs match derived SKUs",
        sorted(live_skus) == sorted(spec_by_sku),
        "exact match"
        if sorted(live_skus) == sorted(spec_by_sku)
        else "mismatch",
    )
    expected_pairs = {
        (row["picker_label"], COLOR_NAME) for row in SIZE_CHART
    }
    live_pairs = {
        tuple(
            option["value"]
            for option in sorted(
                node["selectedOptions"],
                key=lambda item: 0 if item["name"] == "Size" else 1,
            )
        )
        for node in live_variants
    }
    add(
        "Size x Color combinations match",
        live_pairs == expected_pairs,
        f"{len(live_pairs)} combinations",
    )

    price_rows = []
    variant_parity = True
    for live in live_variants:
        spec = spec_by_sku.get(live["sku"])
        unit_cost = (
            ((live.get("inventoryItem") or {}).get("unitCost") or {}).get(
                "amount"
            )
        )
        parity = (
            spec is not None
            and live["price"] == spec["price"]
            and live["compareAtPrice"] == spec["compareAtPrice"]
            and unit_cost is not None
            and Decimal(unit_cost)
            == Decimal(spec["inventoryItem"]["cost"])
            and live["inventoryPolicy"] == "DENY"
            and live["taxable"] is True
            and live["inventoryItem"]["tracked"] is True
            and live["inventoryItem"]["requiresShipping"] is True
        )
        variant_parity = variant_parity and parity
        price_rows.append(
            {
                "sku": live["sku"],
                "live_price": live["price"],
                "live_compare_at": live["compareAtPrice"],
                "live_cost": unit_cost,
                "spec_price": spec["price"] if spec else "",
                "spec_compare_at": (
                    spec["compareAtPrice"] if spec else ""
                ),
                "spec_cost": (
                    spec["inventoryItem"]["cost"] if spec else ""
                ),
                "match": parity,
            }
        )
    add(
        "Price, compare-at, cost, and inventory parity",
        variant_parity,
        f"{len(price_rows)} variants checked",
    )

    headers, rows = table_parts(product["descriptionHtml"])
    add("Size table has 10 headers", len(headers) == 10, str(len(headers)))
    add("Size table has 14 rows", len(rows) == 14, str(len(rows)))
    add(
        "Size table picker labels match",
        [row[0] for row in rows if row]
        == [item["picker_label"] for item in SIZE_CHART],
        "exact order match",
    )
    add(
        "Required tags are present",
        set(build_tags()).issubset(set(product["tags"])),
        "all required tags present",
    )

    media_nodes = product["media"]["nodes"]
    add(
        "Only the owned product image is attached",
        len(media_nodes) == 1
        and (media_nodes[0].get("alt") or "") == MEDIA_ALT,
        str([node.get("alt") for node in media_nodes]),
    )

    actual_metafields = {
        (node["namespace"], node["key"]): node
        for node in product["metafields"]["nodes"]
    }
    expected_metafields = build_metafields(product["id"])
    expected_keys = {
        (node["namespace"], node["key"])
        for node in expected_metafields
    }
    add(
        "Applicable metafields are written",
        expected_keys.issubset(actual_metafields),
        f"{len(expected_keys)} expected",
    )
    expected_size_refs = [
        gid for _, gid, _ in mapped_size_rows()
    ]
    actual_size_node = actual_metafields.get(("shopify", "size"))
    actual_size_refs = (
        json.loads(actual_size_node["value"])
        if actual_size_node
        else []
    )
    add(
        "shopify.size uses 12 honest references",
        actual_size_refs == expected_size_refs
        and len(actual_size_refs) == 12,
        str(len(actual_size_refs)),
    )
    add(
        "shopify.fabric is absent",
        ("shopify", "fabric") not in actual_metafields,
        "skipped because exact fiber is unknown",
    )

    verified_metafields = [
        node
        for key, node in actual_metafields.items()
        if key in expected_keys
    ]
    payload = shopper_payload(
        product["descriptionHtml"],
        product["tags"],
        verified_metafields,
    )
    leaks = source_leak_errors(payload)
    add(
        "Source-leak guard",
        not leaks,
        "no URLs in owned shopper/feed fields"
        if not leaks
        else "; ".join(leaks),
    )
    failures = [
        f"{label}: {detail}"
        for label, passed, detail in checks
        if not passed
    ]
    return checks, price_rows, failures


def write_csv(
    body: str,
    variants: list[dict],
    product: dict,
) -> None:
    with CSV_HEADER_SOURCE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as source:
        header = next(csv.reader(source))

    rows = []
    media_url = ""
    if product["media"]["nodes"]:
        media_url = (
            (product["media"]["nodes"][0].get("image") or {}).get("url")
            or ""
        )
    size_labels = ", ".join(
        label for label, _, _ in mapped_size_rows()
    )

    for index, (chart_row, variant) in enumerate(
        zip(SIZE_CHART, variants),
        start=1,
    ):
        record = {column: "" for column in header}

        def put(column: str, value: str) -> None:
            if column in record:
                record[column] = value

        first = index == 1
        put("Handle", HANDLE)
        put("Title", TITLE if first else "")
        put("Body (HTML)", body if first else "")
        put("Vendor", VENDOR if first else "")
        put(
            "Product Category",
            EXPECTED_TAXONOMY_FULL_NAME if first else "",
        )
        put("Type", PRODUCT_TYPE if first else "")
        put("Tags", ", ".join(build_tags()) if first else "")
        put("Published", "FALSE")
        put("Option1 Name", "Size")
        put("Option1 Value", chart_row["picker_label"])
        put("Option2 Name", "Color")
        put("Option2 Value", COLOR_NAME)
        put("Variant SKU", variant["inventoryItem"]["sku"])
        put("Variant Inventory Tracker", "shopify")
        put("Variant Inventory Policy", "deny")
        put("Variant Fulfillment Service", "manual")
        put("Variant Price", variant["price"])
        put("Variant Compare At Price", variant["compareAtPrice"])
        put("Variant Requires Shipping", "TRUE")
        put("Variant Taxable", "TRUE")
        put("Gift Card", "FALSE")
        put("SEO Title", SEO_TITLE if first else "")
        put("SEO Description", SEO_DESCRIPTION if first else "")
        put(
            "Google Shopping / Google Product Category",
            EXPECTED_TAXONOMY_FULL_NAME if first else "",
        )
        put("Google Shopping / Gender", "unisex")
        put(
            "Google Shopping / Age Group",
            "kids" if chart_row["audience"] == "child" else "adult",
        )
        put(
            "Google Shopping / MPN",
            variant["inventoryItem"]["sku"],
        )
        put("Google Shopping / Condition", "new")
        put("Google Shopping / Custom Product", "FALSE")
        put(
            "Google Shopping / Custom Label 0",
            "Family Matching" if first else "",
        )
        put(
            "Google Shopping / Custom Label 1",
            PRINT_NAME if first else "",
        )
        put(
            "Google Shopping / Custom Label 2",
            "Summer" if first else "",
        )
        put(
            "Google Shopping / Custom Label 3",
            "Tropical Button-Up Shirt" if first else "",
        )
        put(
            "Google Shopping / Custom Label 4",
            "Unisex Family Top" if first else "",
        )
        put(
            "Category1 (product.metafields.custom.category1)",
            "Family Matching" if first else "",
        )
        put(
            "Pattern (product.metafields.custom.pattern)",
            PRINT_NAME if first else "",
        )
        put(
            "Style (product.metafields.custom.style)",
            "Tropical Button-Up Shirt" if first else "",
        )
        put(
            "SubCategory (product.metafields.custom.subcategory)",
            "Tops" if first else "",
        )
        put(
            "SubCategory2 (product.metafields.custom.subcategory2)",
            "Family Matching Shirts" if first else "",
        )
        put(
            "Type (product.metafields.custom.type)",
            "Top" if first else "",
        )
        put(
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)",
            "false",
        )
        put(
            "Age group (product.metafields.shopify.age-group)",
            "kids, adults" if first else "",
        )
        put(
            "Color (product.metafields.shopify.color-pattern)",
            "White, Floral, Multicolor" if first else "",
        )
        put(
            "Size (product.metafields.shopify.size)",
            size_labels if first else "",
        )
        put("Cost per item", variant["inventoryItem"]["cost"])
        put("Status", "draft")
        if first and media_url:
            put("Image Src", media_url)
            put("Image Position", "1")
            put("Image Alt Text", MEDIA_ALT)
        put("Variant Image", media_url)
        rows.append(record)

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as output:
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(
    product: dict,
    checks: list[tuple[str, bool, str]],
    variants: list[dict],
    price_rows: list[dict],
) -> None:
    admin_url = (
        "https://admin.shopify.com/store/dresslikemommy/products/"
        + product["id"].split("/")[-1]
    )
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        mapping = SIZE_MAP.get(row["picker_label"])
        mapped = (
            f"{mapping[0]} ({mapping[1]})"
            if mapping
            else "skipped — no compatible standard size metaobject"
        )
        recap.append(
            "| "
            + " | ".join(
                [
                    row["role"],
                    row["vendor_label"],
                    row["picker_label"],
                    COLOR_NAME,
                    variant["inventoryItem"]["sku"],
                    variant["price"],
                    variant["compareAtPrice"],
                    variant["inventoryItem"]["cost"],
                    mapped,
                ]
            )
            + " |"
        )

    actual_metafields = sorted(
        f"{node['namespace']}.{node['key']}"
        for node in product["metafields"]["nodes"]
        if node["namespace"] != "judgeme"
    )
    skipped = [
        (
            "shopify.fabric",
            "Skipped because the supplied evidence supports only lightweight woven-look fabric, not an exact fiber or honest fabric metaobject.",
        ),
        (
            "shopify.size — Child 14 Years",
            "Vendor size code 170 maps to Child 14 Years from its 150-155 cm recommendation; no compatible standard size metaobject is currently available.",
        ),
        (
            "shopify.size — Adult 5XL",
            "The Adult 5XL variant is retained from the source chart, but no honest 5XL size metaobject is available.",
        ),
        (
            "shopify.sleeve-length-type",
            "Short sleeves are visible, but no owner-subtype-safe catalog value was verified for this Shirts taxonomy run.",
        ),
        (
            "shopify.neckline",
            "A collar is visible, but no owner-subtype-safe neckline value was verified.",
        ),
        (
            "shopify.top-length-type",
            "The source chart provides no garment length measurements.",
        ),
        (
            "shopify.dress-occasion",
            "Not applicable to a Shirts listing.",
        ),
        (
            "shopify.dress-style",
            "Not applicable to a Shirts listing.",
        ),
        (
            "shopify.skirt-dress-length-type",
            "Not applicable because every variant is a shirt.",
        ),
    ]
    smart_collections = product["collections"]["nodes"]
    collection_lines = [
        f"- {item['title']} (/{item['handle']})"
        for item in smart_collections
    ] or [
        "- None returned immediately; a draft may not enter smart collections until publication."
    ]

    lines = [
        f"# {TITLE}",
        "",
        "## Status and links",
        "- Status: DRAFT",
        f"- Admin: {admin_url}",
        "- Live: not published",
        f"- Product GID: {product['id']}",
        f"- Handle: {HANDLE}",
        f"- Vendor: {VENDOR}",
        "",
        "## Request resolution",
        "| Field | Resolved value |",
        "|---|---|",
        "| Listing mode | Family Matching |",
        "| Primary category | Tops |",
        "| Product type | Matching Family Tops |",
        "| Taxonomy | Apparel & Accessories > Clothing > Clothing Tops > Shirts > Dress Shirts |",
        "| Variant model | Size x Color; one unisex shirt and one Sunlit Tropical Bloom color value |",
        "| Force spec prices | true |",
        f"| Shortcode | {SHORTCODE} |",
        f"| Color token | {COLOR_TOKEN} |",
        "",
        "## Evidence and assumptions",
        "- The supplied product image and shared attached size chart are the authoritative local evidence; direct page access was blocked.",
        "- Page-title evidence supports a family matching short-sleeve casual shirt.",
        "- The supplied image shows a warm white shirt with green tropical leaves, yellow flowers, and orange blossoms.",
        "- The white undershirt, hanger, and necklace shown in the product image are styling only and are not included.",
        "- The source chart provides recommended fit height and body weight only. Chest/bust, hip, waist, sleeve, pant/short, and garment-length values remain unavailable rather than inferred.",
        "- Source weight ranges were converted from jin to kilograms using 1 jin = 0.5 kg.",
        "- Vendor size code 170 maps to Child 14 Years using its 150-155 cm recommendation and the store's established age-label progression.",
        "",
        "## Title and SEO",
        f"- Product title ({len(TITLE)}/70): {TITLE}",
        f"- SEO title ({len(SEO_TITLE)}/60): {SEO_TITLE}",
        f"- SEO description ({len(SEO_DESCRIPTION)}/155): {SEO_DESCRIPTION}",
        "",
        "## Pricing",
        f"- Exact nearby active precedent: {PRICE_PRECEDENT_HANDLE}.",
        "| Audience | Price | Compare-at | Cost |",
        "|---|---:|---:|---:|",
        f"| Child | {CHILD_PRICE} | {compare_at(CHILD_PRICE)} | {cost_for(CHILD_PRICE)} |",
        f"| Adult | {ADULT_PRICE} | {compare_at(ADULT_PRICE)} | {cost_for(ADULT_PRICE)} |",
        "- Cost per item is exactly 50% of the forced final variant price, rounded to cents.",
        "",
        "## SIZE_CHART and variant recap",
        "| Role | Vendor row | Picker label | Color | SKU | Price | Compare-at | Cost | shopify.size |",
        "|---|---|---|---|---|---:|---:|---:|---|",
        *recap,
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        *[
            f"| {label} | {'PASS' if passed else 'FAIL'} | {detail} |"
            for label, passed, detail in checks
        ],
        "",
        "## Price and cost parity",
        "| SKU | Live price | Live compare-at | Live cost | Spec price | Spec compare-at | Spec cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[
            "| "
            + " | ".join(
                [
                    row["sku"],
                    str(row["live_price"]),
                    str(row["live_compare_at"]),
                    str(row["live_cost"]),
                    str(row["spec_price"]),
                    str(row["spec_compare_at"]),
                    str(row["spec_cost"]),
                    "yes" if row["match"] else "no",
                ]
            )
            + " |"
            for row in price_rows
        ],
        "",
        "## Metafields written",
        *[f"- {key}" for key in actual_metafields],
        "",
        "## Metafields skipped",
        *[f"- {key}: {reason}" for key, reason in skipped],
        "",
        "## Tags written",
        ", ".join(product["tags"]),
        "",
        "## Smart collections",
        *collection_lines,
        "",
        "## Manual follow-ups",
        "- Inventory quantities remain unset and require an operator decision before any publish-live step.",
        "- Exact fiber composition and direct garment measurements remain unknown; replace broad fabric copy or unavailable cells only if better supplier evidence is obtained.",
        "- Review image crop and product presentation before any separate, explicitly approved publication step.",
        f"- Localization closeout must pass at {LOCALIZATION_CLOSEOUT} before this listing is marked complete.",
        "",
        "## Files",
        f"- {SCRIPT_PATH}",
        f"- {PRODUCT_IMAGE}",
        f"- {SOURCE_SIZE_CHART}",
        f"- {LISTING_MD}",
        f"- {CSV_OUT}",
        f"- {SIZE_CHART_OUT}",
        f"- {BODY_HTML_OUT}",
        f"- {VERIFY_JSON_OUT}",
        f"- {LOCALIZATION_CLOSEOUT}",
    ]
    LISTING_MD.parent.mkdir(parents=True, exist_ok=True)
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()

    validate_preflight(body, variants)
    run_variant_model_guard(variants)
    SIZE_CHART_OUT.write_text(
        json.dumps(SIZE_CHART, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    BODY_HTML_OUT.write_text(body + "\n", encoding="utf-8")

    assert_taxonomy()
    product_id = create_or_update_product(body, variants)
    write_metafields(product_id)
    upload_owned_media(product_id)
    time.sleep(3)

    product = fetch_verify(product_id)
    verify_payload = {"data": {"product": product}}
    VERIFY_JSON_OUT.write_text(
        json.dumps(verify_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    checks, price_rows, failures = verify_product(product, variants)
    write_csv(body, variants, product)
    write_listing(product, checks, variants, price_rows)

    if failures:
        raise RuntimeError(
            "FINAL VERIFY FAILED:\n- " + "\n- ".join(failures)
        )
    print(
        json.dumps(
            {
                "admin_url": (
                    "https://admin.shopify.com/store/dresslikemommy/products/"
                    + product_id.split("/")[-1]
                ),
                "live_url": "not published",
                "handle": HANDLE,
                "status": product["status"],
                "variant_count": len(product["variants"]["nodes"]),
                "published_at": product["publishedAt"],
                "live_publications": [],
                "price_cost_parity": all(
                    row["match"] for row in price_rows
                ),
                "listing_md": str(LISTING_MD),
                "csv": str(CSV_OUT),
                "verify": str(VERIFY_JSON_OUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
PY

/usr/bin/python3 "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" --handles "sunlit-tropical-bloom-family-matching-tops"
