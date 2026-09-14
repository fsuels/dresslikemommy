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

HANDLE = "together-heart-family-matching-sweaters"
TITLE = "Together Heart Family Matching Sweaters — Crewneck Tops"
SEO_TITLE = "Together Heart Family Sweaters | Dress Like Mommy"
SEO_DESCRIPTION = (
    "Together heart family sweaters in 7 colors for adults and kids. "
    "Crewneck knit-look tops in Child 2–10 Years and Adult S–4XL."
)
BUYER_PARAGRAPHS = [
    "A long-sleeve crewneck sweater with a Together heart graphic, in child and adult sizes.",
    "Each selection includes one sweater. Choose a size and color for each person; the other pictured garments and accessories are not included.",
    "Compare the chest, sleeve and garment-length measurements with a sweater that fits. Hip and waist measurements are unavailable.",
]
PRINT_NAME = "Together Heart"
SHORTCODE = "THRT"
COLORS = [
    {
        "name": "White",
        "token": "WHT",
        "gid": "gid://shopify/Metaobject/69639733345",
    },
    {
        "name": "Pink",
        "token": "PNK",
        "gid": "gid://shopify/Metaobject/69963645025",
    },
    {
        "name": "Black",
        "token": "BLK",
        "gid": "gid://shopify/Metaobject/69943132257",
    },
    {
        "name": "Blue",
        "token": "BLU",
        "gid": "gid://shopify/Metaobject/69639766113",
    },
    {
        "name": "Yellow",
        "token": "YLW",
        "gid": "gid://shopify/Metaobject/69622104161",
    },
    {
        "name": "Red",
        "token": "RED",
        "gid": "gid://shopify/Metaobject/69600804961",
    },
    {
        "name": "Green",
        "token": "GRN",
        "gid": "gid://shopify/Metaobject/70220546145",
    },
]
COLOR_NAMES = [item["name"] for item in COLORS]
COLOR_TOKEN_BY_NAME = {item["name"]: item["token"] for item in COLORS}
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sweaters"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-12"
EXPECTED_TAXONOMY_FULL_NAME = (
    "Apparel & Accessories > Clothing > Clothing Tops > Sweaters"
)
FORCE_SPEC_PRICES = True
CHILD_PRICE = "24.99"
ADULT_PRICE = "26.99"
PRICE_PRECEDENT_HANDLE = "owner-price-override"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / "01-together-heart-family-sweaters.png"
SOURCE_SIZE_CHART = (
    ROOT
    / "ops/listings/source-size-chart-together-heart-family-matching-sweaters.png"
)
SOURCE_SIZE_SELECTOR = (
    ROOT
    / "ops/listings/source-size-selector-together-heart-family-matching-sweaters.png"
)
SELLER_SELECTABLE_SIZES = [
    "90",
    "100",
    "110",
    "120",
    "130",
    "140",
    "150",
    "S",
    "M",
    "L",
    "XL",
    "2XL",
    "3XL",
    "4XL",
]
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = (
    ROOT
    / "ops/scripts/create-thrt-together-heart-family-matching-sweatshirts.sh"
)
LOCALIZATION_CLOSEOUT = ROOT / "ops/listings" / f"{HANDLE}-localization-closeout.json"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

MEDIA_ALT = (
    "Family of four wearing Together heart graphic crewneck sweaters in "
    "blue, yellow, red, and black by the beach."
)

AGE_GROUP_GIDS = {
    "child": "gid://shopify/Metaobject/128116523105",
    "adult": "gid://shopify/Metaobject/128116490337",
}
COLOR_PATTERN_GIDS = [item["gid"] for item in COLORS]
TARGET_GENDER_GIDS = ["gid://shopify/Metaobject/129972502625"]

SIZE_MAP = {
    "Child 2 Years": (
        "gid://shopify/Metaobject/129972863073",
        "2-3 years",
    ),
    "Child 3 Years": (
        "gid://shopify/Metaobject/129972895841",
        "3-4 years",
    ),
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
    "Adult S": (
        "gid://shopify/Metaobject/129975255137",
        "S",
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
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "90",
        "picker_label": "Child 2 Years",
        "sku_suffix": "KID2Y",
        "age": "2",
        "weight": "10-12.5 kg",
        "height": "75-90 cm",
        "chest_cm": 74,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 39,
        "shoulder_cm": 36,
        "sleeve_cm": 29,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "100",
        "picker_label": "Child 3 Years",
        "sku_suffix": "KID3Y",
        "age": "3",
        "weight": "12.5-15 kg",
        "height": "90-105 cm",
        "chest_cm": 78,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 42,
        "shoulder_cm": 38,
        "sleeve_cm": 32,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "15-20 kg",
        "height": "105-115 cm",
        "chest_cm": 82,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 45,
        "shoulder_cm": 40,
        "sleeve_cm": 35,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "20-25 kg",
        "height": "115-125 cm",
        "chest_cm": 86,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 48,
        "shoulder_cm": 41,
        "sleeve_cm": 38,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "22.5-27.5 kg",
        "height": "125-135 cm",
        "chest_cm": 90,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 51,
        "shoulder_cm": 43,
        "sleeve_cm": 41,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "27.5-32.5 kg",
        "height": "135-145 cm",
        "chest_cm": 94,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 54,
        "shoulder_cm": 45,
        "sleeve_cm": 44,
        "pant_cm": "-",
    },
    {
        "audience": "child",
        "role": "Child Sweater",
        "garment": "Sweater",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "32.5-37.5 kg",
        "height": "145-155 cm",
        "chest_cm": 98,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 57,
        "shoulder_cm": 47,
        "sleeve_cm": 47,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "S/160",
        "picker_label": "Adult S",
        "sku_suffix": "S",
        "age": "—",
        "weight": "40-50 kg",
        "height": "150-160 cm",
        "chest_cm": 102,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 64,
        "shoulder_cm": 50,
        "sleeve_cm": 52,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "M/165",
        "picker_label": "Adult M",
        "sku_suffix": "M",
        "age": "—",
        "weight": "50-60 kg",
        "height": "155-165 cm",
        "chest_cm": 106,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 66,
        "shoulder_cm": 51,
        "sleeve_cm": 54,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "L/170",
        "picker_label": "Adult L",
        "sku_suffix": "L",
        "age": "—",
        "weight": "57.5-67.5 kg",
        "height": "160-170 cm",
        "chest_cm": 110,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 68,
        "shoulder_cm": 53,
        "sleeve_cm": 56,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "XL/175",
        "picker_label": "Adult XL",
        "sku_suffix": "XL",
        "age": "—",
        "weight": "65-72.5 kg",
        "height": "170-180 cm",
        "chest_cm": 114,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 70,
        "shoulder_cm": 55,
        "sleeve_cm": 58,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "2XL/180",
        "picker_label": "Adult 2XL",
        "sku_suffix": "2XL",
        "age": "—",
        "weight": "70-80 kg",
        "height": "175-185 cm",
        "chest_cm": 118,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 72,
        "shoulder_cm": 57,
        "sleeve_cm": 60,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "3XL/185",
        "picker_label": "Adult 3XL",
        "sku_suffix": "3XL",
        "age": "—",
        "weight": "80-100 kg",
        "height": "180-190 cm",
        "chest_cm": 122,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 74,
        "shoulder_cm": 59,
        "sleeve_cm": 61,
        "pant_cm": "-",
    },
    {
        "audience": "adult",
        "role": "Adult Sweater",
        "garment": "Sweater",
        "vendor_label": "4XL/190",
        "picker_label": "Adult 4XL",
        "sku_suffix": "4XL",
        "age": "—",
        "weight": "95-110 kg",
        "height": "185-195 cm",
        "chest_cm": 126,
        "hip_cm": "-",
        "waist_cm": "-",
        "length_cm": 76,
        "shoulder_cm": 60,
        "sleeve_cm": 63,
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
    return {
        "Child Sweater": "KID",
        "Adult Sweater": "ADT",
    }[role]


def price_for(row: dict) -> str:
    return CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE


def sku_for(row: dict, color_name: str) -> str:
    return (
        f"DLM-{SHORTCODE}-{role_token(row['role'])}-"
        f"{row['sku_suffix']}-{COLOR_TOKEN_BY_NAME[color_name]}"
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
        "Family Sweaters",
        "Sweaters",
        "Matching Family Sweaters",
        "Matching Family Outfits",
        "Child Sweater",
        "Adult Sweater",
        "Unisex Sweater",
        "Long Sleeve Top",
        "Crewneck Sweater",
        "Together Heart",
        "Heart Graphic",
        "Graphic Sweater",
        "Fall",
        "Family Photos",
    ]
    values.extend(COLOR_NAMES)
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
            f"<p>{html.escape(BUYER_PARAGRAPHS[0])}</p>",
            f"<p>{html.escape(BUYER_PARAGRAPHS[1])}</p>",
            "<h3>Size Chart — Sweater</h3>",
            "<table id=\"size-chart\">",
            "<thead><tr>",
            *[f"<th>{header}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *rendered_rows,
            "</tbody></table>",
            f"<p>{html.escape(BUYER_PARAGRAPHS[2])}</p>",
        ]
    )


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        for color_name in COLOR_NAMES:
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
                            "name": color_name,
                        },
                    ],
                    "inventoryItem": {
                        "sku": sku_for(row, color_name),
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
            "value": "Family Sweaters",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "subcategory2",
            "type": "single_line_text_field",
            "value": "Sweaters",
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
            "value": "Heart Graphic Crewneck Sweater",
        },
        {
            "ownerId": product_id,
            "namespace": "custom",
            "key": "type",
            "type": "single_line_text_field",
            "value": "Sweater",
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
            "value": "Fall",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_3",
            "type": "single_line_text_field",
            "value": "Heart Graphic Crewneck Sweater",
        },
        {
            "ownerId": product_id,
            "namespace": "mm-google-shopping",
            "key": "custom_label_4",
            "type": "single_line_text_field",
            "value": "Unisex Family Sweater",
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
            "namespace": "shopify",
            "key": "neckline",
            "type": "list.metaobject_reference",
            "value": json.dumps(
                ["gid://shopify/Metaobject/129973387361"]
            ),
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
        "shoulder_cm",
        "sleeve_cm",
        "pant_cm",
    }
    expected_variant_count = len(SIZE_CHART) * len(COLORS)
    if len(SIZE_CHART) != 14 or len(variants) != expected_variant_count:
        errors.append(
            "SIZE_CHART must have 14 rows and variants must have "
            f"{expected_variant_count} Size x Color combinations"
        )
    if COLOR_NAMES != [
        "White",
        "Pink",
        "Black",
        "Blue",
        "Yellow",
        "Red",
        "Green",
    ]:
        errors.append("color list/order differs from the owner override")
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
        if row["garment"] != "Sweater":
            errors.append(
                f"non-sweater garment row: {row['vendor_label']}"
            )
        if row["audience"] not in {"child", "adult"}:
            errors.append(f"invalid audience: {row['audience']}")
        for field in (
            "chest_cm",
            "length_cm",
            "shoulder_cm",
            "sleeve_cm",
        ):
            if not isinstance(row[field], (int, float)) or row[field] <= 0:
                errors.append(
                    f"{row['vendor_label']} lacks positive source {field}"
                )
        if row["pant_cm"] != "-":
            errors.append(
                f"{row['vendor_label']} invents a pant measurement"
            )
        # Product-only source-truth exception: PROB-2026-09-10-TOGETHER-HEART-DERIVED-SIZING.
        # The supplied chart omits hip and waist; the older top formula is superseded.
        for field in ("hip_cm", "waist_cm"):
            if row[field] != "-":
                errors.append(
                    f"{row['vendor_label']} invents a source-omitted {field}"
                )
        if not str(row["weight"]).endswith(" kg"):
            errors.append(f"{row['vendor_label']} weight is not metric")
        if not str(row["height"]).endswith(" cm"):
            errors.append(f"{row['vendor_label']} height is not metric")

    if len(
        {(row["role"], row["picker_label"]) for row in SIZE_CHART}
    ) != len(SIZE_CHART):
        errors.append("duplicate role/picker pair")
    if len({row["picker_label"] for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate Size option value")
    if [row["vendor_label"].split("/", 1)[0] for row in SIZE_CHART] != SELLER_SELECTABLE_SIZES:
        errors.append(
            "SIZE_CHART rows do not exactly match the seller's selectable sweater sizes"
        )
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"SEO title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"SEO description too long: {len(SEO_DESCRIPTION)}")
    if not FORCE_SPEC_PRICES:
        errors.append("FORCE_SPEC_PRICES must be true")

    expected_skus = [
        sku_for(row, color_name)
        for row in SIZE_CHART
        for color_name in COLOR_NAMES
    ]
    actual_skus = [
        variant["inventoryItem"]["sku"] for variant in variants
    ]
    if (
        len(set(actual_skus)) != expected_variant_count
        or sorted(actual_skus) != sorted(expected_skus)
    ):
        errors.append("SKUs are not the unique values derived from SIZE_CHART")

    row_by_label = {row["picker_label"]: row for row in SIZE_CHART}
    expected_pairs = {
        (row["picker_label"], color_name)
        for row in SIZE_CHART
        for color_name in COLOR_NAMES
    }
    actual_pairs = {
        tuple(item["name"] for item in variant["optionValues"])
        for variant in variants
    }
    if actual_pairs != expected_pairs:
        errors.append("Size x Color variant combinations do not match")

    for variant in variants:
        option_pair = tuple(
            item["name"] for item in variant["optionValues"]
        )
        row = row_by_label.get(option_pair[0])
        if row is None:
            errors.append(f"unknown size option pair: {option_pair}")
            continue
        expected_price = price_for(row)
        if variant["price"] != expected_price:
            errors.append(f"price mismatch for {option_pair}")
        if variant["compareAtPrice"] != compare_at(expected_price):
            errors.append(f"compare-at mismatch for {option_pair}")
        if variant["inventoryItem"]["cost"] != cost_for(expected_price):
            errors.append(f"cost mismatch for {option_pair}")

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
    if any(row[7:9] != ["—", "—"] for row in table_rows):
        errors.append("size-table hip and waist cells must mark unavailable measurements")
    paragraphs = [
        html.unescape(re.sub(r"<[^>]+>", "", value)).strip()
        for value in re.findall(r"<p>(.*?)</p>", body, re.S)
    ]
    if paragraphs != BUYER_PARAGRAPHS or "<li>" in body:
        errors.append("body must contain only the three approved buyer paragraphs and size chart")
    if "Hip and waist measurements are unavailable." not in body:
        errors.append("body lacks the unavailable hip/waist disclosure")
    if any(
        text in body.lower()
        for text in (
            "source chart", "supplied product image", "chart-backed",
            "derived", "formula", "jin", "requested colors", "seller",
        )
    ):
        errors.append("body contains internal source or measurement-derivation prose")

    missing_size_refs = {
        row["picker_label"] for row in SIZE_CHART
    } - set(SIZE_MAP)
    if missing_size_refs:
        errors.append(
            "missing honest size metaobject mappings: "
            + ", ".join(sorted(missing_size_refs))
        )
    preflight_metafields = build_metafields("gid://shopify/Product/0")
    if any(
        item["namespace"] == "shopify" and item["key"] == "fabric"
        for item in preflight_metafields
    ):
        errors.append("shopify.fabric must be skipped")
    if not any(
        item["namespace"] == "shopify" and item["key"] == "neckline"
        for item in preflight_metafields
    ):
        errors.append("supported crew neckline metafield is missing")

    if not SOURCE_SIZE_CHART.is_file():
        errors.append(f"missing source size chart: {SOURCE_SIZE_CHART}")
    if not SOURCE_SIZE_SELECTOR.is_file():
        errors.append(f"missing seller size-selector evidence: {SOURCE_SIZE_SELECTOR}")
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
                    "title": "Together heart family matching sweater",
                    "notes": (
                        "one unisex crewneck sweater across child and adult "
                        "sizes in seven colors; the seller selector explicitly "
                        "offers only child 90 through 150 and adult S through 4XL"
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
                "Sweaters",
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
    unsupported_shopify_keys = {
        "fabric",
        "dress-occasion",
        "dress-style",
        "skirt-dress-length-type",
    }
    if any(
        node["namespace"] == "shopify"
        and node["key"] in unsupported_shopify_keys
        for node in existing["metafields"]["nodes"]
    ):
        raise RuntimeError(
            "Existing draft has an unsupported fabric/dress metafield; "
            "manual review required"
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
            "Existing draft variant shape/SKUs differ from the 98-variant spec; "
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
            "values": [{"name": name} for name in COLOR_NAMES],
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
        "Variant count is 98",
        len(live_variants) == 98,
        str(len(live_variants)),
    )
    add(
        "SKUs are unique",
        len(set(live_skus)) == len(live_skus) == 98,
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
        (row["picker_label"], color_name)
        for row in SIZE_CHART
        for color_name in COLOR_NAMES
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
    expected_tags = build_tags()
    add(
        "Tags match the sweater specification exactly",
        product["tags"] == expected_tags,
        f"{len(product['tags'])} actual / {len(expected_tags)} expected",
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
        "shopify.size uses 14 honest references",
        actual_size_refs == expected_size_refs
        and len(actual_size_refs) == 14,
        str(len(actual_size_refs)),
    )
    actual_color_node = actual_metafields.get(("shopify", "color-pattern"))
    actual_color_refs = (
        json.loads(actual_color_node["value"])
        if actual_color_node
        else []
    )
    add(
        "shopify.color-pattern uses the 7 requested colors",
        actual_color_refs == COLOR_PATTERN_GIDS,
        str(len(actual_color_refs)),
    )
    add(
        "shopify.fabric is absent",
        ("shopify", "fabric") not in actual_metafields,
        "skipped because exact fiber is unknown",
    )
    unsupported_dress_keys = {
        ("shopify", "dress-occasion"),
        ("shopify", "dress-style"),
        ("shopify", "skirt-dress-length-type"),
    }
    add(
        "Dress-only Shopify metafields are absent",
        unsupported_dress_keys.isdisjoint(actual_metafields),
        "sweater listing must not inherit dress classification metadata",
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

    chart_by_label = {
        row["picker_label"]: row for row in SIZE_CHART
    }
    for index, variant in enumerate(variants, start=1):
        options = {
            value["optionName"]: value["name"]
            for value in variant["optionValues"]
        }
        chart_row = chart_by_label[options["Size"]]
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
        put("Option2 Value", options["Color"])
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
            "Fall" if first else "",
        )
        put(
            "Google Shopping / Custom Label 3",
            "Heart Graphic Crewneck Sweater" if first else "",
        )
        put(
            "Google Shopping / Custom Label 4",
            "Unisex Family Sweater" if first else "",
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
            "Heart Graphic Crewneck Sweater" if first else "",
        )
        put(
            "SubCategory (product.metafields.custom.subcategory)",
            "Family Sweaters" if first else "",
        )
        put(
            "SubCategory2 (product.metafields.custom.subcategory2)",
            "Sweaters" if first else "",
        )
        put(
            "Type (product.metafields.custom.type)",
            "Sweater" if first else "",
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
            ", ".join(COLOR_NAMES) if first else "",
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
    variants_by_pair = {
        tuple(value["name"] for value in variant["optionValues"]): variant
        for variant in variants
    }
    for row in SIZE_CHART:
        mapping = SIZE_MAP.get(row["picker_label"])
        mapped = (
            f"{mapping[0]} ({mapping[1]})"
            if mapping
            else "skipped — no compatible standard size metaobject"
        )
        for color_name in COLOR_NAMES:
            variant = variants_by_pair[(row["picker_label"], color_name)]
            recap.append(
                "| "
                + " | ".join(
                    [
                        row["role"],
                        row["vendor_label"],
                        row["picker_label"],
                        color_name,
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
            "Skipped because the image supports a soft-knit sweater appearance but no exact fiber composition or honest fabric metaobject.",
        ),
        (
            "shopify.sleeve-length-type",
            "Long sleeves are visible and charted, but no owner-subtype-safe Long sleeve metaobject was returned by the live store lookup.",
        ),
        (
            "shopify.top-length-type",
            "Exact garment lengths are charted, but they do not map the full size range to one honest standard top-length category.",
        ),
        (
            "shopify.dress-occasion",
            "Not applicable to a Sweaters listing.",
        ),
        (
            "shopify.dress-style",
            "Not applicable to a Sweaters listing.",
        ),
        (
            "shopify.skirt-dress-length-type",
            "Not applicable because every variant is a sweater.",
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
        "| Primary category | Sweaters |",
        "| Product type | Matching Family Sweaters |",
        "| Taxonomy | Apparel & Accessories > Clothing > Clothing Tops > Sweaters |",
        "| Variant model | Size x Color; one unisex sweater in seven requested colors |",
        "| Force spec prices | true |",
        f"| Shortcode | {SHORTCODE} |",
        "| Color tokens | WHT, PNK, BLK, BLU, YLW, RED, GRN |",
        "",
        "## Evidence and assumptions",
        "- The supplied product image and attached size chart are the authoritative local evidence; direct vendor-page access was blocked by browser site-safety policy.",
        "- The supplied image shows a family of four in long-sleeve crewneck sweaters with a Together heart back graphic.",
        "- Pants, skirts, hats, glasses, shoes, and accessories shown in the image are styling only and are not included.",
        "- The sweater sub-table provides garment length, chest, shoulder, sleeve, recommended height, and recommended weight for seven child and seven adult rows.",
        "- Source weight ranges were converted from jin to kilograms using 1 jin = 0.5 kg.",
        "- Source truth correction, 2026-09-10: the chart provides no hip or waist measurements. All 28 corresponding values are stored as '-' and rendered as '—'; no measurements are derived.",
        "- Superseded history, 2026-09-02: the original listing used the shared top formula for hip and waist. This product-specific source-truth repair overrides that formula without changing the shared listing workflow or the 56 supplied length/chest/shoulder/sleeve measurements.",
        "- The owner confirmed the item is sweaters, and the supplied seller selector lists only child 90 through 150 and adult S through 4XL. The separate infant-romper reference rows are therefore not sold for this item and are excluded.",
        "- The owner's explicit color override is the source of truth for White, Pink, Black, Blue, Yellow, Red, and Green; the supplied image visibly demonstrates four of those colors.",
        "",
        "## Title and SEO",
        f"- Product title ({len(TITLE)}/70): {TITLE}",
        f"- SEO title ({len(SEO_TITLE)}/60): {SEO_TITLE}",
        f"- SEO description ({len(SEO_DESCRIPTION)}/155): {SEO_DESCRIPTION}",
        "",
        "## Pricing",
        "- Exact owner price override applied with FORCE_SPEC_PRICES=true.",
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
        "- Exact fiber composition remains unknown; replace the broad knit-appearance disclosure only if better supplier evidence is obtained.",
        "- Review the image crop and confirm that one shared lifestyle image is sufficient for all seven color variants before any separate, explicitly approved publication step.",
        f"- Localization closeout must pass at {LOCALIZATION_CLOSEOUT} before this listing is marked complete.",
        "",
        "## Files",
        f"- {SCRIPT_PATH}",
        f"- {PRODUCT_IMAGE}",
        f"- {SOURCE_SIZE_CHART}",
        f"- {SOURCE_SIZE_SELECTOR}",
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

    if os.environ.get("LISTING_PREFLIGHT_ONLY") == "1":
        print(
            json.dumps(
                {
                    "status": "preflight_passed",
                    "handle": HANDLE,
                    "size_chart_rows": len(SIZE_CHART),
                    "color_count": len(COLORS),
                    "variant_count": len(variants),
                    "child_price": CHILD_PRICE,
                    "adult_price": ADULT_PRICE,
                    "source_size_chart": str(SOURCE_SIZE_CHART),
                    "seller_size_selector": str(SOURCE_SIZE_SELECTOR),
                    "product_image": str(PRODUCT_IMAGE),
                },
                indent=2,
            )
        )
        return

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

if [[ "${LISTING_PREFLIGHT_ONLY:-0}" == "1" ]]; then
  exit 0
fi

/usr/bin/python3 "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" --handles "together-heart-family-matching-sweaters"
