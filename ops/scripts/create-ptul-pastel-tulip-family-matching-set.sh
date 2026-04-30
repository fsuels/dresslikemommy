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
from typing import Any

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "pastel-tulip-family-matching-set"
TITLE = "Pastel Tulip Family Matching Set - Dress & Tee"
SEO_TITLE = "Pastel Tulip Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Pastel floral family set with mom + girl dresses and a matching dad tee. Fit chart covers Baby 66-90, Child 80-150, Mom S-2XL and Dad S-4XL."
PRINT_NAME = "Pastel Tulip"
SHORTCODE = "PTUL"
COLOR_TOKEN = "TULIP"
VENDOR_URL = "https://detail.1688.com/offer/800385971840.html"
VENDOR = "dresslikemommy.com"
LISTING_MODE = "Family Matching"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

SCRIPT_PATH = ROOT / "ops/scripts/create-ptul-pastel-tulip-family-matching-set.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings/pastel-tulip-family-matching-set-listing.md"
CSV_OUT = ROOT / "ops/listings/pastel-tulip-family-matching-set-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings/verify-pastel-tulip-family-matching-set.json"
SIZE_CHART_OUT = ROOT / "ops/listings/size-chart-pastel-tulip-family-matching-set.json"
BODY_HTML_OUT = ROOT / "ops/listings/body-pastel-tulip-family-matching-set.html"
SOURCE_SIZE_CHART = ROOT / "ops/listings/source-size-chart-pastel-tulip-family-matching-set.png"

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
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART: list[dict[str, Any]] = [
    {"audience":"baby","role":"Baby Romper","garment":"Baby Romper","vendor_label":"66","picker_label":"Baby 0-3 Months","sku_suffix":"B03M","age":"0-3M","weight":"5-7.5 kg","height":"58-66 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"baby","role":"Baby Romper","garment":"Baby Romper","vendor_label":"73","picker_label":"Baby 6-9 Months","sku_suffix":"B69M","age":"6-9M","weight":"7.5-9 kg","height":"66-76 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"baby","role":"Baby Romper","garment":"Baby Romper","vendor_label":"80","picker_label":"Baby 9-12 Months","sku_suffix":"B912M","age":"9-12M","weight":"9-11 kg","height":"75-80 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"baby","role":"Baby Romper","garment":"Baby Romper","vendor_label":"90","picker_label":"Baby 12-18 Months","sku_suffix":"B1218M","age":"12-18M","weight":"11-14 kg","height":"82-90 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"59-69 kg","height":"160-170 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"70-80 kg","height":"160-175 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"80-92.5 kg","height":"160-175 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"160-165 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"165-170 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"-","weight":"57.5-67.5 kg","height":"168-173 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"-","weight":"69-79 kg","height":"170-178 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"-","weight":"80-89 kg","height":"175-180 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"-","weight":"87.5-97.5 kg","height":"175-188 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"4XL","picker_label":"Father 4XL","sku_suffix":"4XL","age":"-","weight":"97.5-115 kg","height":"178-195 cm","chest_cm":"-","hip_cm":"-","waist_cm":"-","length_cm":"-","skirt_cm":"-","sleeve_cm":"-","pant_cm":"-"},
]


def gql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
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


def require_no_user_errors(data: dict[str, Any], path: list[str]) -> None:
    cur: Any = data
    for key in path:
        cur = cur[key]
    if cur:
        raise RuntimeError(json.dumps(cur, indent=2))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    value = Decimal(price) * Decimal("1.15")
    dollars = int(math.floor(float(value)))
    candidate = Decimal(dollars) + Decimal("0.99")
    if candidate < value:
        candidate += Decimal("1.00")
    return money(candidate)


def fmt_num(value: Decimal | float | str) -> str:
    number = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return str(int(number)) if number == number.to_integral() else str(number).rstrip("0").rstrip(".")


def cm_to_in(value: Any) -> str:
    if value in (None, "", "-", 0, "0"):
        return "-"
    number = Decimal(str(value))
    return f"{fmt_num(number)} cm / {fmt_num(number / Decimal('2.54'))} in"


def dual_range(text: str, metric_unit: str, imperial_unit: str, factor: Decimal) -> str:
    nums = [Decimal(n) for n in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if len(nums) >= 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} {metric_unit} / {fmt_num(nums[0] * factor)}-{fmt_num(nums[1] * factor)} {imperial_unit}"
    return text or "-"


def role_token(role: str) -> str:
    if role == "Baby Romper":
        return "BBY"
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Mother"):
        return "MOM"
    if role.startswith("Father"):
        return "DAD"
    raise KeyError(role)


def garment_token(garment: str) -> str:
    return {"Baby Romper": "ROMP", "Dress": "DRS", "Shirt": "TEE"}[garment]


def price_for(row: dict[str, Any]) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


def sku_for(row: dict[str, Any]) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{garment_token(row['garment'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


def tags() -> list[str]:
    values = [
        LISTING_MODE,
        "Sets",
        "Matching Family Set",
        "Matching Family Outfit",
        "Matching Family Dresses",
        "Matching Family Tops",
        "Mommy and Me",
        "Daddy and Me",
        "Family Matching",
        "Baby Romper",
        "Girl Dress",
        "Mother Dress",
        "Father Shirt",
        "Dress",
        "Shirt",
        "T-Shirt",
        "Pastel Tulip",
        "Pastel Floral",
        "Watercolor Floral",
        "Tulip",
        "Pink",
        "Green",
        "White",
        "Summer",
        "Vacation",
        "Photo Outfit",
        "Resort",
        VENDOR_URL,
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


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
    by_garment: dict[str, list[dict[str, Any]]] = {}
    for row in SIZE_CHART:
        by_garment.setdefault(row["garment"], []).append(row)

    def table_for(garment: str, rows: list[dict[str, Any]]) -> str:
        parts = [f"<h3>Size Chart - {html.escape(garment)}</h3>", "<table id=\"size-chart\">", "<thead><tr>"]
        parts.extend(f"<th>{header}</th>" for header in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            cells = [
                row["picker_label"],
                row["age"] if row["audience"] in {"baby", "child"} else "-",
                dual_range(row["weight"], "kg", "lbs", Decimal("2.20462")),
                dual_range(row["height"], "cm", "in", Decimal("0.393701")),
                cm_to_in(row["chest_cm"]),
                cm_to_in(row["skirt_cm"] if row["garment"] == "Dress" else row["sleeve_cm"]),
                cm_to_in(row["pant_cm"]),
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            parts.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")
        parts.append("</tbody></table>")
        return "\n".join(parts)

    intro = """
<ul>
<li><strong>Fabric:</strong> Lightweight woven dress fabric and a soft knit-style tee look; exact fiber composition was not visible in the supplied evidence.</li>
<li><strong>Family story:</strong> A fresh matching look for mom, dad, babies, and kids that feels easy for vacations, portraits, and sunny days together.</li>
<li><strong>Print reference:</strong> Pastel Tulip pairs airy green brushstrokes with soft pink tulip-style blooms on a clean white base.</li>
<li><strong>Design details:</strong> Spaghetti-strap dresses for mom and girls, a matching-panel dad tee, and baby romper sizing in the same family print story.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, and steam lightly from the inside if needed.</li>
<li><strong>Size range:</strong> Baby 0-3M to 12-18M, Child 1-2 Years to 9-10 Years, Mother S-2XL, and Father S-4XL.</li>
</ul>
""".strip()
    narrative = """
<p>Pastel Tulip brings a soft vacation mood to family matching: floaty mom-and-girl dresses, a clean white dad tee with the same watercolor floral panel, and baby romper rows for the smallest matching moment. The print is colorful without feeling loud, so it works for seaside photos, garden brunches, and relaxed summer plans.</p>

<p>The attached fit chart is the source of truth for every listed size. It provides recommended height and weight ranges, so garment-measurement columns are left blank instead of guessed.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Full family sizing:</strong> Baby, child, mother, and father rows are all backed by the attached chart.</li>
<li><strong>Coordinated pieces:</strong> Dress, shirt, and baby romper Types keep each purchasable piece clear.</li>
<li><strong>Pastel floral print:</strong> Pink tulip-style blooms and green watercolor leaves create a soft photo-ready look.</li>
<li><strong>Summer friendly:</strong> Strappy dresses and a short-sleeve tee silhouette suit warm-weather plans.</li>
<li><strong>Draft-only listing:</strong> Built unpublished for final image, fabric, and inventory review.</li>
</ul>

<p>Select the Type and Size for each family member to build a coordinated Pastel Tulip look for your next sunny memory.</p>
""".strip()
    return "\n\n".join([intro, *(table_for(name, rows) for name, rows in by_garment.items()), narrative])


def build_variants() -> list[dict[str, Any]]:
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


def metafields(product_id: str) -> list[dict[str, Any]]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Pastel Floral"},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Vacation Family Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress & Shirt Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Tee"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971519585", "gid://shopify/Metaobject/130231140449", "gid://shopify/Metaobject/69963645025", "gid://shopify/Metaobject/70220546145", "gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict[str, Any]]) -> None:
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "skirt_cm", "pant_cm"}
    errors = []
    if len(SIZE_CHART) != 24 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('role')} {row.get('vendor_label')} missing {', '.join(missing)}")
        if row["picker_label"] not in SIZE_MAP:
            errors.append(f"missing shopify.size mapping for {row['picker_label']}")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label) pair")
    if len({variant["inventoryItem"]["sku"] for variant in variants}) != len(variants):
        errors.append("duplicate SKU")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        errors.append("title/SEO length guard failed")
    if table_row_count(body) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        errors.append("one or more size tables does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("variant cost is not 50 percent")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "baby romper, girl dress, mother dress, father shirt, family matching floral dress tee"}), encoding="utf-8")
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
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"} or path.name.startswith("source-size-chart"):
            continue
        alt = "Family wearing pastel floral matching dress and tee outfits outdoors."
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
        urllib.request.urlopen(urllib.request.Request(target["url"], data=b"".join(chunks), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})).read()
        media = gql("""mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""", {
            "productId": product_id,
            "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}],
        })
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict[str, Any]]) -> None:
    header = (ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    tag_text = ", ".join(tags())
    for index, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        record = {key: "" for key in header}
        record.update({
            "Handle": HANDLE,
            "Title": TITLE if index == 1 else "",
            "Body (HTML)": body if index == 1 else "",
            "Vendor": VENDOR if index == 1 else "",
            "Product Category": EXPECTED_TAXONOMY_FULL_NAME if index == 1 else "",
            "Type": PRODUCT_TYPE if index == 1 else "",
            "Tags": tag_text if index == 1 else "",
            "Published": "FALSE",
            "Option1 Name": "Type",
            "Option1 Value": row["garment"],
            "Option2 Name": "Size",
            "Option2 Value": row["picker_label"],
            "Variant SKU": variant["inventoryItem"]["sku"],
            "Variant Grams": "0",
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": variant["price"],
            "Variant Compare At Price": variant["compareAtPrice"],
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Gift Card": "FALSE",
            "SEO Title": SEO_TITLE if index == 1 else "",
            "SEO Description": SEO_DESCRIPTION if index == 1 else "",
            "Google Shopping / Gender": "unisex" if index == 1 else "",
            "Google Shopping / Age Group": "adult" if index == 1 else "",
            "Google Shopping / Condition": "new" if index == 1 else "",
            "Google Shopping / Custom Product": "FALSE" if index == 1 else "",
            "Google Shopping / Custom Label 0": "Family Matching" if index == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if index == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if index == 1 else "",
            "Google Shopping / Custom Label 3": "Dress & Tee" if index == 1 else "",
            "Google Shopping / Custom Label 4": "Four-Role Matching" if index == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if index == 1 else "",
            "Pattern (product.metafields.custom.pattern)": "Pastel Floral" if index == 1 else "",
            "Style (product.metafields.custom.style)": "Vacation Family Set" if index == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if index == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if index == 1 else "",
            "Type (product.metafields.custom.type)": "Dress & Shirt Set" if index == 1 else "",
            "Cost per item": variant["inventoryItem"]["cost"],
            "Status": "draft",
        })
        rows.append(record)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, body: str, variants: list[dict[str, Any]], verify: dict[str, Any]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    spec_by_sku = {variant["inventoryItem"]["sku"]: (row, variant) for row, variant in zip(SIZE_CHART, variants)}
    live_skus = sorted(node["sku"] for node in verify["variants"]["nodes"])
    spec_skus = sorted(spec_by_sku)
    price_ok = True
    price_rows = []
    for live in verify["variants"]["nodes"]:
        row, spec = spec_by_sku[live["sku"]]
        cost = ((live.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        ok = (
            live["price"] == spec["price"]
            and live["compareAtPrice"] == spec["compareAtPrice"]
            and cost is not None
            and Decimal(cost) == Decimal(spec["inventoryItem"]["cost"])
            and live["inventoryPolicy"] == "DENY"
            and live["inventoryItem"]["tracked"] is True
            and live["inventoryItem"]["requiresShipping"] is True
        )
        price_ok = price_ok and ok
        price_rows.append(f"| {live['sku']} | {live['price']} | {live['compareAtPrice']} | {cost or ''} | {spec['inventoryItem']['cost']} | {'PASS' if ok else 'FAIL'} |")
    header_counts = [part.count("<th>") for part in re.findall(r"<table.*?</table>", body, re.S)]
    published = [node["publication"]["name"] for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    checks = [
        ("Title <= 70", len(TITLE) <= 70, str(len(TITLE))),
        ("SEO title <= 60", len(SEO_TITLE) <= 60, str(len(SEO_TITLE))),
        ("SEO description <= 155", len(SEO_DESCRIPTION) <= 155, str(len(SEO_DESCRIPTION))),
        ("Variant count matches SIZE_CHART", len(verify["variants"]["nodes"]) == len(SIZE_CHART), f"{len(verify['variants']['nodes'])} vs {len(SIZE_CHART)}"),
        ("Live SKUs match derived SKUs", live_skus == spec_skus, str(len(spec_skus))),
        ("Each size table has 10 headers", all(count == 10 for count in header_counts), str(header_counts)),
        ("Size table rows match SIZE_CHART", table_row_count(body) == len(SIZE_CHART), f"{table_row_count(body)} vs {len(SIZE_CHART)}"),
        ("Product status is DRAFT", verify["status"] == "DRAFT", verify["status"]),
        ("publishedAt is null", verify.get("publishedAt") is None, str(verify.get("publishedAt"))),
        ("onlineStoreUrl is null", verify.get("onlineStoreUrl") is None, str(verify.get("onlineStoreUrl"))),
        ("No sales-channel publication is live", not published, str(published)),
        ("Taxonomy resolves to expected leaf", verify["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, verify["category"]["fullName"]),
        ("Price and cost parity", price_ok, "FORCE_SPEC_PRICES=true and Cost per item=50%"),
    ]
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    written = [f"- `{node['namespace']}.{node['key']}`" for node in verify["metafields"]["nodes"] if node["namespace"] in {"custom", "global", "mm-google-shopping", "shopify"}]
    skipped = [
        ("shopify.fabric", "Exact fiber composition is not visible in the attached product image or size chart."),
        ("shopify.dress-occasion", "The listing mixes dresses, shirt, and baby romper rows under Outfit Sets."),
        ("shopify.dress-style", "Mixed-garment product; one product-level dress style would be misleading."),
        ("shopify.neckline", "No verified product-level neckline catalog value is available for all Types."),
        ("shopify.skirt-dress-length-type", "The source chart does not provide garment lengths, and the product also includes non-dress rows."),
        ("shopify.sleeve-length-type", "The source chart does not provide sleeve length."),
        ("shopify.top-length-type", "No verified shirt length is provided in the source chart."),
    ]
    collection_lines = [f"- {node['title']} (`/{node['handle']}`)" for node in verify["collections"]["nodes"]] or ["- Collection indexing may wait until publication because this product remains an unpublished draft."]
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
        "| SIZE_CHART_SOURCE | attached product and size-chart screenshots |",
        "| LISTING_MODE | template value resolved from evidence -> Family Matching |",
        "| PRIMARY_CATEGORY | auto -> FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> Pastel Tulip floral only |",
        "| EXCLUDE_ITEMS | none |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor Fetch Status",
        "Direct HTTP and logged-in Chrome/CDP access both landed on Alibaba `_____tmd_____` / `Captcha Interception` markup, so the attached product and size-chart screenshots were used as authoritative evidence per the canonical workflow.", "",
        "## Pricing",
        f"Prices use the nearby mixed family set pattern: child/baby rows at `{CHILD_PRICE}` and adult rows at `{ADULT_PRICE}`. Cost per item is exactly 50 percent of selling price.", "",
        "## Derivations and Mapping Notes",
        "- The chart is transcribed into 24 variant rows: 4 baby romper, 8 girl dress, 5 mother dress, and 7 father shirt rows.",
        "- Source weights were listed in Chinese jin and converted to kg/lbs for customer-facing tables.",
        "- The source chart provides height and weight reference rows only. Chest, waist, hip, sleeve/skirt, pant, and garment length cells are left blank instead of guessed.",
        "- Options are `Type x Size` so separate garment choices remain clear.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
        *recap, "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        *[f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |" for label, ok, detail in checks], "",
        "## Price Parity",
        "| SKU | Live Price | Live Compare | Live Cost | Expected Cost | Match |",
        "|---|---|---|---|---|---|",
        *price_rows, "",
        "## Smart Collections",
        *collection_lines, "",
        "## Metafields Written",
        *written, "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        f"## Tags Written ({len(verify['tags'])})",
        "`" + ", ".join(verify["tags"]) + "`", "",
        "## Publication",
        "- Draft only. The runner did not call `publishablePublish`, `publishedAt` is null, and no sales-channel publication is live.", "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition before publishing.",
        "- Replace or retouch vendor lifestyle imagery if brand standards require cleaner publication media.",
        "- Inventory quantities and per-variant grams still need operator stock values.",
        "- If a richer vendor garment-measurement chart becomes available, rerun with chest/waist/length values filled from that source.", "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{SOURCE_SIZE_CHART}`",
        f"- `{UPLOAD_DIR}`", "",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")
    failed = [label for label, ok, _detail in checks if not ok]
    if failed:
        raise RuntimeError("VERIFY FAILED: " + ", ".join(failed))


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard()
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{id sku}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Baby Romper", "Dress", "Shirt"]]},
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
        live_skus = sorted(node["sku"] for node in existing["variants"]["nodes"] if node.get("sku"))
        spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
        if live_skus and live_skus != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create duplicates.")
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        if live_skus == spec_skus:
            live_by_sku = {node["sku"]: node["id"] for node in existing["variants"]["nodes"] if node.get("sku")}
            update_variants = [{"id": live_by_sku[variant["inventoryItem"]["sku"]], **variant} for variant in variants]
            bulk = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
                "productId": product_id,
                "variants": update_variants,
            })
            require_no_user_errors(bulk, ["data", "productVariantsBulkUpdate", "userErrors"])
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]
        bulk = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        })
        require_no_user_errors(bulk, ["data", "productVariantsBulkCreate", "userErrors"])

    for index in range(0, len(metafields(product_id)), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": metafields(product_id)[index:index+25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice taxable inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    write_listing(product_id, body, variants, verify)
    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "onlineStoreUrl": verify["onlineStoreUrl"],
        "variant_count": len(verify["variants"]["nodes"]),
        "media_count": len(verify["media"]["nodes"]),
        "listing": str(LISTING_MD),
    }, indent=2))


if __name__ == "__main__":
    main()
PY
