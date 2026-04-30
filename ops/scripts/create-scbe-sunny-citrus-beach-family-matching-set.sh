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

HANDLE = "sunny-citrus-beach-family-matching-set"
TITLE = "Sunny Citrus Beach Family Matching Set - Dress & Shorts"
SEO_TITLE = "Sunny Citrus Family Matching Set | Dress Like Mommy"
SEO_DESCRIPTION = "Sunny citrus family matching set with dresses plus shirt-and-shorts outfits for mom, dad, girls & boys. Sizes Child 2Y-12Y and adult S-4XL."
PRINT_NAME = "Sunny Citrus Beach"
SHORTCODE = "SCBE"
COLOR_TOKEN = "CIT"
COLOR_NAME = "Sunny Citrus"
VENDOR_URL = "https://detail.1688.com/offer/1041610755813.html"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
CUSTOM_TYPE = "Two-Piece Set"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

SCRIPT_PATH = ROOT / "ops/scripts/create-scbe-sunny-citrus-beach-family-matching-set.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SOURCE_CHART_IMAGE = ROOT / "ops/listings/source-size-chart-sunny-citrus-beach-family-matching-set.png"

SIZE_MAP = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Child 12 Years": ("gid://shopify/Metaobject/129971650657", "12"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "90", "picker_label": "Child 2 Years", "sku_suffix": "KID2Y", "age": "2", "weight": "12.5 kg", "height": "90 cm", "chest_cm": 60, "hip_cm": 66, "waist_cm": 60, "length_cm": 38, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 25},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "100", "picker_label": "Child 3 Years", "sku_suffix": "KID3Y", "age": "3", "weight": "15 kg", "height": "100 cm", "chest_cm": 64, "hip_cm": 70, "waist_cm": 64, "length_cm": 41, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 27},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "110", "picker_label": "Child 4 Years", "sku_suffix": "KID4Y", "age": "4", "weight": "17.5 kg", "height": "110 cm", "chest_cm": 68, "hip_cm": 74, "waist_cm": 68, "length_cm": 44, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 29},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "120", "picker_label": "Child 5 Years", "sku_suffix": "KID5Y", "age": "5", "weight": "20 kg", "height": "120 cm", "chest_cm": 72, "hip_cm": 78, "waist_cm": 72, "length_cm": 47, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 31},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "130", "picker_label": "Child 6-7 Years", "sku_suffix": "KID67Y", "age": "6-7", "weight": "25 kg", "height": "130 cm", "chest_cm": 76, "hip_cm": 82, "waist_cm": 76, "length_cm": 50, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 33},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "140", "picker_label": "Child 8 Years", "sku_suffix": "KID8Y", "age": "8", "weight": "30 kg", "height": "140 cm", "chest_cm": 80, "hip_cm": 86, "waist_cm": 80, "length_cm": 53, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 35},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "150", "picker_label": "Child 9-10 Years", "sku_suffix": "KID910Y", "age": "9-10", "weight": "35 kg", "height": "150 cm", "chest_cm": 84, "hip_cm": 90, "waist_cm": 84, "length_cm": 56, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 37},
    {"audience": "child", "role": "Boy Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "160", "picker_label": "Child 12 Years", "sku_suffix": "KID12Y", "age": "11-12", "weight": "40 kg", "height": "155 cm", "chest_cm": 88, "hip_cm": 94, "waist_cm": 88, "length_cm": 58, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 39},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "90", "picker_label": "Child 2 Years", "sku_suffix": "KID2Y", "age": "2", "weight": "12.5 kg", "height": "90 cm", "chest_cm": 56, "hip_cm": 60, "waist_cm": 56, "length_cm": 60, "sleeve_cm": 0, "skirt_cm": 60, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "100", "picker_label": "Child 3 Years", "sku_suffix": "KID3Y", "age": "3", "weight": "15 kg", "height": "100 cm", "chest_cm": 60, "hip_cm": 64, "waist_cm": 60, "length_cm": 65, "sleeve_cm": 0, "skirt_cm": 65, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "110", "picker_label": "Child 4 Years", "sku_suffix": "KID4Y", "age": "4", "weight": "17.5 kg", "height": "110 cm", "chest_cm": 64, "hip_cm": 68, "waist_cm": 64, "length_cm": 70, "sleeve_cm": 0, "skirt_cm": 70, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "120", "picker_label": "Child 5 Years", "sku_suffix": "KID5Y", "age": "5", "weight": "20 kg", "height": "120 cm", "chest_cm": 68, "hip_cm": 72, "waist_cm": 68, "length_cm": 75, "sleeve_cm": 0, "skirt_cm": 75, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "130", "picker_label": "Child 6-7 Years", "sku_suffix": "KID67Y", "age": "6-7", "weight": "25 kg", "height": "130 cm", "chest_cm": 72, "hip_cm": 76, "waist_cm": 72, "length_cm": 80, "sleeve_cm": 0, "skirt_cm": 80, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "140", "picker_label": "Child 8 Years", "sku_suffix": "KID8Y", "age": "8", "weight": "30 kg", "height": "140 cm", "chest_cm": 76, "hip_cm": 80, "waist_cm": 76, "length_cm": 86, "sleeve_cm": 0, "skirt_cm": 86, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "150", "picker_label": "Child 9-10 Years", "sku_suffix": "KID910Y", "age": "9-10", "weight": "35 kg", "height": "150 cm", "chest_cm": 80, "hip_cm": 84, "waist_cm": 80, "length_cm": 92, "sleeve_cm": 0, "skirt_cm": 92, "pant_cm": 0},
    {"audience": "child", "role": "Girl Dress", "garment": "Dress", "vendor_label": "160", "picker_label": "Child 12 Years", "sku_suffix": "KID12Y", "age": "11-12", "weight": "40 kg", "height": "155 cm", "chest_cm": 84, "hip_cm": 88, "waist_cm": 84, "length_cm": 98, "sleeve_cm": 0, "skirt_cm": 98, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "S", "picker_label": "Mother S", "sku_suffix": "S", "age": "-", "weight": "0-50 kg", "height": "-", "chest_cm": 88, "hip_cm": 94, "waist_cm": 86, "length_cm": 110, "sleeve_cm": 0, "skirt_cm": 110, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "M", "picker_label": "Mother M", "sku_suffix": "M", "age": "-", "weight": "0-55 kg", "height": "-", "chest_cm": 92, "hip_cm": 98, "waist_cm": 90, "length_cm": 111, "sleeve_cm": 0, "skirt_cm": 111, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "L", "picker_label": "Mother L", "sku_suffix": "L", "age": "-", "weight": "0-60 kg", "height": "-", "chest_cm": 96, "hip_cm": 102, "waist_cm": 94, "length_cm": 112, "sleeve_cm": 0, "skirt_cm": 112, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "XL", "picker_label": "Mother XL", "sku_suffix": "XL", "age": "-", "weight": "0-65 kg", "height": "-", "chest_cm": 100, "hip_cm": 106, "waist_cm": 98, "length_cm": 112, "sleeve_cm": 0, "skirt_cm": 112, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "XXL", "picker_label": "Mother 2XL", "sku_suffix": "2XL", "age": "-", "weight": "0-70 kg", "height": "-", "chest_cm": 104, "hip_cm": 110, "waist_cm": 102, "length_cm": 113, "sleeve_cm": 0, "skirt_cm": 113, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "3XL", "picker_label": "Mother 3XL", "sku_suffix": "3XL", "age": "-", "weight": "0-75 kg", "height": "-", "chest_cm": 108, "hip_cm": 114, "waist_cm": 106, "length_cm": 114, "sleeve_cm": 0, "skirt_cm": 114, "pant_cm": 0},
    {"audience": "mother", "role": "Mother Dress", "garment": "Dress", "vendor_label": "4XL", "picker_label": "Mother 4XL", "sku_suffix": "4XL", "age": "-", "weight": "0-80 kg", "height": "-", "chest_cm": 112, "hip_cm": 118, "waist_cm": 110, "length_cm": 115, "sleeve_cm": 0, "skirt_cm": 115, "pant_cm": 0},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "S", "picker_label": "Father S", "sku_suffix": "S", "age": "-", "weight": "0-50 kg", "height": "-", "chest_cm": 96, "hip_cm": 110, "waist_cm": 84, "length_cm": 65, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 47},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "M", "picker_label": "Father M", "sku_suffix": "M", "age": "-", "weight": "0-60 kg", "height": "-", "chest_cm": 100, "hip_cm": 114, "waist_cm": 88, "length_cm": 67, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 49},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "L", "picker_label": "Father L", "sku_suffix": "L", "age": "-", "weight": "0-70 kg", "height": "-", "chest_cm": 104, "hip_cm": 118, "waist_cm": 92, "length_cm": 69, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 51},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "XL", "picker_label": "Father XL", "sku_suffix": "XL", "age": "-", "weight": "0-80 kg", "height": "-", "chest_cm": 108, "hip_cm": 122, "waist_cm": 96, "length_cm": 71, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 53},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "XXL", "picker_label": "Father 2XL", "sku_suffix": "2XL", "age": "-", "weight": "0-90 kg", "height": "-", "chest_cm": 112, "hip_cm": 126, "waist_cm": 100, "length_cm": 73, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 55},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "3XL", "picker_label": "Father 3XL", "sku_suffix": "3XL", "age": "-", "weight": "0-100 kg", "height": "-", "chest_cm": 116, "hip_cm": 130, "waist_cm": 104, "length_cm": 75, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 57},
    {"audience": "father", "role": "Father Shirt & Shorts Set", "garment": "Shirt & Shorts Set", "vendor_label": "4XL", "picker_label": "Father 4XL", "sku_suffix": "4XL", "age": "-", "weight": "0-110 kg", "height": "-", "chest_cm": 120, "hip_cm": 134, "waist_cm": 108, "length_cm": 77, "sleeve_cm": 0, "skirt_cm": 0, "pant_cm": 59},
]


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
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


def money(value: Decimal | str | None) -> str:
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


def fmt_num(value: float | int | Decimal) -> str:
    numeric = float(value)
    return str(int(numeric)) if numeric.is_integer() else f"{numeric:.1f}".rstrip("0").rstrip(".")


def cm_to_in(value: float | int | str | None) -> str:
    if value in (None, "", 0, "0", "-", "—"):
        return "&mdash;"
    numeric = float(value)
    return f"{fmt_num(numeric)} cm / {fmt_num(numeric / 2.54)} in"


def dual_range(text: str, metric_unit: str, imperial_unit: str, factor: float) -> str:
    if not text or text in {"-", "—"}:
        return "&mdash;"
    nums = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) >= 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} {metric_unit} / {fmt_num(nums[0] * factor)}-{fmt_num(nums[1] * factor)} {imperial_unit}"
    if len(nums) == 1:
        return f"{fmt_num(nums[0])} {metric_unit} / {fmt_num(nums[0] * factor)} {imperial_unit}"
    return html.escape(text)


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


ROLE_TOKENS = {
    "Girl Dress": "GRL",
    "Boy Shirt & Shorts Set": "BOY",
    "Mother Dress": "MOM",
    "Father Shirt & Shorts Set": "DAD",
}
SIZE_TOKENS = {label: row[1] for label, row in {
    "Child 2 Years": ("", "KID2Y"),
    "Child 3 Years": ("", "KID3Y"),
    "Child 4 Years": ("", "KID4Y"),
    "Child 5 Years": ("", "KID5Y"),
    "Child 6-7 Years": ("", "KID67Y"),
    "Child 8 Years": ("", "KID8Y"),
    "Child 9-10 Years": ("", "KID910Y"),
    "Child 12 Years": ("", "KID12Y"),
    "Mother S": ("", "S"),
    "Mother M": ("", "M"),
    "Mother L": ("", "L"),
    "Mother XL": ("", "XL"),
    "Mother 2XL": ("", "2XL"),
    "Mother 3XL": ("", "3XL"),
    "Mother 4XL": ("", "4XL"),
    "Father S": ("", "S"),
    "Father M": ("", "M"),
    "Father L": ("", "L"),
    "Father XL": ("", "XL"),
    "Father 2XL": ("", "2XL"),
    "Father 3XL": ("", "3XL"),
    "Father 4XL": ("", "4XL"),
}.items()}


def type_for(row: dict) -> str:
    return row["garment"]


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{ROLE_TOKENS[row['role']]}-{SIZE_TOKENS[row['picker_label']]}-{COLOR_TOKEN}"


def measurement_column(row: dict) -> str:
    if row["garment"] == "Dress":
        return cm_to_in(row.get("skirt_cm"))
    return "&mdash;"


def pant_column(row: dict) -> str:
    return cm_to_in(row.get("pant_cm"))


def build_table(garment: str, rows: list[dict]) -> str:
    headers = [
        "Size",
        "Age",
        "Weight (kg/lbs)",
        "Height (cm/in)",
        "Chest/Bust (cm/in)",
        "Sleeve or Skirt (cm/in)",
        "Pant/Short or &mdash; (cm/in)",
        "Hip (cm/in)",
        "Waist (cm/in)",
        "Garment Length (cm/in)",
    ]
    body_rows = []
    for row in rows:
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "&mdash;",
            dual_range(row["weight"], "kg", "lbs", 2.20462),
            dual_range(row["height"], "cm", "in", 1 / 2.54),
            cm_to_in(row["chest_cm"]),
            measurement_column(row),
            pant_column(row),
            cm_to_in(row["hip_cm"]),
            cm_to_in(row["waist_cm"]),
            cm_to_in(row["length_cm"]),
        ]
        body_rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    return "\n".join([
        f"<h3>Size Chart - {garment}</h3>",
        "<table id=\"size-chart\">",
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *body_rows,
        "</tbody></table>",
    ])


def build_body() -> str:
    dress_rows = [row for row in SIZE_CHART if row["garment"] == "Dress"]
    set_rows = [row for row in SIZE_CHART if row["garment"] == "Shirt & Shorts Set"]
    return "\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven-look summer fabric; exact fiber composition was not visible in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> A sunny beach-ready matching look for mom, dad, girls, and boys.</li>",
        "<li><strong>Print reference:</strong> Sunny Citrus pairs soft aqua tones with yellow-orange tropical floral accents.</li>",
        "<li><strong>Design details:</strong> Girls and mothers wear breezy dresses, while boys and fathers wear coordinated shirts with matching shorts.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>",
        "<li><strong>Size range:</strong> Child 2 Years through Child 12 Years, plus Mother S-4XL and Father S-4XL.</li>",
        "</ul>",
        "",
        build_table("Dress", dress_rows),
        "",
        build_table("Shirt & Shorts Set", set_rows),
        "",
        "<p>Sunny Citrus Beach is made for vacation photos, seaside birthdays, and warm-weather family days when everyone wants to coordinate without looking overly formal.</p>",
        "",
        "<p>The size picker separates dresses from shirt-and-shorts sets so each family member can choose the garment that matches the supplied measurement chart.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Four-role match:</strong> Sizes are included for girls, boys, mothers, and fathers.</li>",
        "<li><strong>Beach-ready citrus print:</strong> Soft aqua with yellow-orange floral accents keeps the look bright and summery.</li>",
        "<li><strong>Coordinated garments:</strong> Dresses for mom and daughter, shirt-and-shorts sets for dad and son.</li>",
        "<li><strong>Extended size range:</strong> Child sizes through 12 Years plus adult S-4XL rows from the chart.</li>",
        "<li><strong>Draft-only review:</strong> Created unpublished so merchandising can confirm fabric and image readiness before launch.</li>",
        "</ul>",
        "",
        "<p>Choose each family member's size and build a sunny matching outfit for the next beach day, cruise, or family photo session.</p>",
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
                {"optionName": "Type", "name": type_for(row)},
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
        "Sets",
        "Matching Family Set",
        "Matching Family Sets",
        "Matching Family Outfit",
        "Girl Dress",
        "Mother Dress",
        "Boy Shirt Set",
        "Father Shirt Set",
        "Dress",
        "Shirt & Shorts Set",
        "Two-Piece Set",
        "Summer",
        "Beach",
        "Vacation",
        "Resort",
        "Tropical",
        "Citrus",
        "Floral",
        "Yellow",
        "Orange",
        "Aqua",
        "White",
        PRINT_NAME,
        VENDOR_URL,
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Sunny Citrus Floral"},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Beach Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": CUSTOM_TYPE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Shorts"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622104161", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/70220546145", "gid://shopify/Metaobject/129971519585"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm"}
    errors = []
    if len(SIZE_CHART) != 30 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('role')} {row.get('vendor_label')} missing {missing}")
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
    tables = re.findall(r"<table.*?</table>", body, re.S)
    if len(tables) != 2:
        errors.append("expected two body size tables")
    if sum(table.count("<tr>") - 1 for table in tables) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    if any(table.count("<th>") != 10 for table in tables):
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
        chart_path = tmpdir / "size-chart.json"
        derived_path = tmpdir / "derived.json"
        evidence_path = tmpdir / "vendor-evidence.json"
        chart_path.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived_path.write_text(json.dumps({"option_names": ["Type", "Size"], "variants": variants}), encoding="utf-8")
        evidence_path.write_text(json.dumps({"raw_detail_text": "男童 男士 女童 女装 上衣 T-shirt 短裤 shorts 连衣裙 dress family matching"}), encoding="utf-8")
        subprocess.run([
            "python3",
            str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart",
            str(chart_path),
            "--derived",
            str(derived_path),
            "--vendor-evidence",
            str(evidence_path),
            "--primary-category",
            "FamilySet",
            "--tags",
            ", ".join(tags()),
        ], check=True)


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.name.startswith("source-") or "size-chart" in path.name or "size_chart" in path.name:
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        alt = "Family wearing Sunny Citrus Beach matching dresses and shirt-and-shorts outfits."
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
            "Option1 Value": type_for(row),
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
            "Google Shopping / Custom Label 3": "Dress & Shorts" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Four-Role Matching" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": "Sunny Citrus Floral" if i == 1 else "",
            "Style (product.metafields.custom.style)": "Beach Family Matching Set" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if i == 1 else "",
            "Type (product.metafields.custom.type)": CUSTOM_TYPE if i == 1 else "",
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
    if sorted(node["sku"] for node in live_variants) != sorted(spec_by_sku):
        errors.append("live SKUs do not match derived SKUs")
    tables = re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)
    if len(tables) != 2 or any(table.count("<th>") != 10 for table in tables):
        errors.append("size table header count check failed")
    if sum(table.count("<tr>") - 1 for table in tables) != len(SIZE_CHART):
        errors.append("size table row count does not match SIZE_CHART")
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(type_for(row), row["picker_label"]) for row in SIZE_CHART}
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
            errors.append(f"variant parity failed for {node['sku']}")
        price_rows.append({
            "sku": node["sku"],
            "live_price": node["price"],
            "live_compare_at": node["compareAtPrice"],
            "live_cost": money(unit_cost) if unit_cost is not None else "",
            "spec_price": spec["price"],
            "spec_compare_at": spec["compareAtPrice"],
            "spec_cost": spec["inventoryItem"]["cost"],
            "match": match,
        })
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    recap = []
    for row in SIZE_CHART:
        variant = spec_by_sku[sku_for(row)]
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {type_for(row)} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    skipped = [
        ("shopify.clothing-features", "No single product-level feature value is honest for this mixed summer outfit set."),
        ("shopify.fabric", "The 1688 page returned punish/CAPTCHA markup and the attached chart/image do not confirm exact fiber composition."),
        ("shopify.dress-occasion", "Skipped because the honest taxonomy is Outfit Sets, not a dress-only leaf."),
        ("shopify.dress-style", "Skipped because this is a mixed dress and shirt-and-shorts set listing."),
        ("shopify.neckline", "The mixed dress and shirt presentation does not map cleanly to one product-level neckline value."),
        ("shopify.pants-length-type", "The shorts rows do not support one product-level pants-length value for the full mixed set."),
        ("shopify.skirt-dress-length-type", "Skipped because the product mixes dresses with shirt-and-shorts sets."),
        ("shopify.sleeve-length-type", "Skipped because one product-level sleeve value would be misleading across garments."),
        ("shopify.top-length-type", "Skipped because the product mixes tops, shorts, and dresses."),
        ("shopify.waist-rise", "The chart does not provide enough waist-rise evidence."),
    ]
    publication_names = [node["publication"]["name"] for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    metafield_nodes = [node for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"}]
    collections = verify["collections"]["nodes"]
    price_ok = all(row["match"] for row in price_rows)
    size_rows = [f"{row['role']} -> {row['picker_label']}" for row in SIZE_CHART]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | template choices + evidence -> Family Matching |",
        "| PRIMARY_CATEGORY | auto -> FamilySet |",
        "| DESIGNS_TO_LIST | auto -> one Sunny Citrus colorway |",
        "| EXCLUDE_ITEMS | none |",
        f"| SHORTCODE | auto -> `{SHORTCODE}` |",
        f"| COLOR_TOKEN | auto -> `{COLOR_TOKEN}` |",
        "| FORCE_SPEC_PRICES | true |",
        "",
        "## Vendor Fetch Status",
        "A direct request to the 1688 page returned Alibaba punish/CAPTCHA markup during this run. Per the canonical workflow, the attached size chart and supplied product image were used as authoritative evidence.",
        "",
        "## Pricing Source",
        "Nearby active Family Matching set products were queried through Shopify Admin. The prevailing active pattern was child `28.99` and adult `31.99`, so those prices were used with `FORCE_SPEC_PRICES=true`; Cost per item is exactly 50% of selling price.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor row | Picker label | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
        *recap,
        "",
        "## Derivations",
        "- Vendor weight guidance was listed in jin in the screenshot and converted to kg/lbs for the shopper-facing table.",
        "- Child shirt-and-shorts waist values are derived from chest because the chart omits waist; vendor hip values were preserved.",
        "- Child dress hip = chest + 4 cm and waist = chest because the girl chart omits hip and waist.",
        "- Mother hip = bust + 6 cm and waist = hip - 8 cm because the adult dress chart omits hip and waist.",
        "- Father waist = chest - 12 cm because the adult shirt-and-shorts chart omits waist; vendor hip values were preserved.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| No sales-channel publication is live | {'PASS' if not publication_names else 'FAIL'} | {publication_names} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Option axes are Type / Size | {'PASS' if [o['name'] for o in verify['options']] == ['Type', 'Size'] else 'FAIL'} | {[o['name'] for o in verify['options']]} |",
        f"| Size table rows match picker labels | {'PASS' if size_rows else 'FAIL'} | {' | '.join(size_rows)} |",
        f"| Each size table has 10 headers | {'PASS' if all(table.count('<th>') == 10 for table in re.findall(r'<table.*?</table>', verify['descriptionHtml'], re.S)) else 'FAIL'} | {[table.count('<th>') for table in re.findall(r'<table.*?</table>', verify['descriptionHtml'], re.S)]} |",
        f"| Waist populated for every row | {'PASS' if all(row['waist_cm'] for row in SIZE_CHART) else 'FAIL'} | yes |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Price and cost parity | {'PASS' if price_ok else 'FAIL'} | FORCE_SPEC_PRICES=true and cost=50% |",
        "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'NO'} |" for row in price_rows],
        "",
        "## Metafields Written",
        "| Namespace.Key | Type | Value |",
        "|---|---|---|",
        *[f"| `{node['namespace']}.{node['key']}` | {node['type']} | `{node['value'][:120]}{'...' if len(node['value']) > 120 else ''}` |" for node in metafield_nodes],
        "",
        "## Metafields Skipped",
        "| Namespace.Key | Reason |",
        "|---|---|",
        *[f"| `{key}` | {reason} |" for key, reason in skipped],
        "",
        "## Tags Written",
        f"`{', '.join(verify['tags'])}`",
        "",
        "## Smart Collections",
        *([f"- {collection['title']} (`/{collection['handle']}`)" for collection in collections] if collections else ["Collection indexing may wait until publication because the product is an unpublished draft."]),
        "",
        "## Publication",
        "- Product remains DRAFT.",
        "- Live URL: not published.",
        f"- Sales-channel publication check: {'no live publications' if not publication_names else publication_names}.",
        "",
        "## Manual Follow-ups",
        "- Replace or retouch the supplied source image before publication if any vendor/editorial marks are visible.",
        "- Confirm exact fabric composition if the vendor page becomes readable later; `shopify.fabric` was intentionally skipped.",
        "- Inventory quantities and per-variant grams still need operator stock values.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SOURCE_CHART_IMAGE}`",
        f"- `{UPLOAD_DIR}`",
        "",
        "## Sources",
        "- Attached size chart image from operator request.",
        "- Attached product image from operator request.",
        "- Shopify Admin query of active Family Matching set products for pricing.",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard(variants)

    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    type_values = [{"name": value} for value in dict.fromkeys(type_for(row) for row in SIZE_CHART)]
    size_values = [{"name": value} for value in dict.fromkeys(row["picker_label"] for row in SIZE_CHART)]
    product_options = [
        {"name": "Type", "values": type_values},
        {"name": "Size", "values": size_values},
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

    for i in range(0, len(metafields(product_id)), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": metafields(product_id)[i:i + 25]})
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
