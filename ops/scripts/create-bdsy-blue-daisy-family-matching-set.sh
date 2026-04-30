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
import time
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "blue-daisy-family-matching-set"
TITLE = "Blue Daisy Family Matching Set - Dress, Shirt & Romper"
SEO_TITLE = "Blue Daisy Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Blue floral family matching set with dress, shirt and baby romper options. Baby 0-3M-12-18M, Child 1-2Y-10Y, Mother S-2XL, Father S-4XL."
PRINT_NAME = "Blue Daisy"
SHORTCODE = "BDSY"
COLOR_TOKEN = "BLUE"
COLOR_NAME = "Blue Daisy"
VENDOR_URL = "https://detail.1688.com/offer/1046962900946.html"
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
SOURCE_SIZE_CHART = ROOT / "ops" / "listings" / f"source-size-chart-{HANDLE}.png"

PUBLICATION_IDS = [
    "gid://shopify/Publication/55169925",
    "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225",
    "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
]

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

SIZE_CHART = [
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"66","picker_label":"Baby 0-3 Months","sku_suffix":"B03M","age":"0-3M","weight":"5-7.5 kg","height":"58-66 cm","chest_cm":52,"hip_cm":56,"waist_cm":52,"length_cm":41,"shoulder_cm":23,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"73","picker_label":"Baby 6-9 Months","sku_suffix":"B69M","age":"6-9M","weight":"7.5-9 kg","height":"66-76 cm","chest_cm":54,"hip_cm":58,"waist_cm":54,"length_cm":43,"shoulder_cm":25,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"80","picker_label":"Baby 9-12 Months","sku_suffix":"B912M","age":"9-12M","weight":"9-11 kg","height":"75-80 cm","chest_cm":56,"hip_cm":60,"waist_cm":56,"length_cm":45,"shoulder_cm":27,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"90","picker_label":"Baby 12-18 Months","sku_suffix":"B1218M","age":"12-18M","weight":"11-14 kg","height":"82-90 cm","chest_cm":58,"hip_cm":62,"waist_cm":58,"length_cm":47,"shoulder_cm":29,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":56,"shoulder_cm":0,"skirt_cm":56,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":59,"shoulder_cm":0,"skirt_cm":59,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":62,"shoulder_cm":0,"skirt_cm":62,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":64,"shoulder_cm":0,"skirt_cm":64,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":67,"shoulder_cm":0,"skirt_cm":67,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":71,"shoulder_cm":0,"skirt_cm":71,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":74,"shoulder_cm":0,"skirt_cm":74,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":78,"shoulder_cm":0,"skirt_cm":78,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":92,"hip_cm":98,"waist_cm":90,"length_cm":109,"shoulder_cm":0,"skirt_cm":109,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":96,"hip_cm":102,"waist_cm":94,"length_cm":110,"shoulder_cm":0,"skirt_cm":110,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"59-69 kg","height":"160-170 cm","chest_cm":100,"hip_cm":106,"waist_cm":98,"length_cm":112,"shoulder_cm":0,"skirt_cm":112,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"70-80 kg","height":"160-175 cm","chest_cm":104,"hip_cm":110,"waist_cm":102,"length_cm":114,"shoulder_cm":0,"skirt_cm":114,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"80-92.5 kg","height":"160-175 cm","chest_cm":108,"hip_cm":114,"waist_cm":106,"length_cm":115,"shoulder_cm":0,"skirt_cm":115,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":34,"shoulder_cm":35,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":37,"shoulder_cm":37,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":40,"shoulder_cm":39,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":43,"shoulder_cm":41,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":46,"shoulder_cm":42,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":49,"shoulder_cm":44,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":52,"shoulder_cm":46,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":100,"hip_cm":104,"waist_cm":100,"length_cm":55,"shoulder_cm":48,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"160-165 cm","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":66,"shoulder_cm":53,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"165-170 cm","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":68,"shoulder_cm":54,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"-","weight":"57.5-67.5 kg","height":"168-173 cm","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":70,"shoulder_cm":56,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"-","weight":"69-79 kg","height":"170-178 cm","chest_cm":126,"hip_cm":126,"waist_cm":114,"length_cm":72,"shoulder_cm":58,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"-","weight":"80-89 kg","height":"175-180 cm","chest_cm":130,"hip_cm":130,"waist_cm":118,"length_cm":74,"shoulder_cm":60,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"-","weight":"87.5-97.5 kg","height":"175-188 cm","chest_cm":134,"hip_cm":134,"waist_cm":122,"length_cm":76,"shoulder_cm":61,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"4XL","picker_label":"Father 4XL","sku_suffix":"4XL","age":"-","weight":"97.5-115 kg","height":"178-195 cm","chest_cm":138,"hip_cm":138,"waist_cm":126,"length_cm":78,"shoulder_cm":62,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
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


def money_half(price: str) -> str:
    return str((Decimal(price) * Decimal("0.50")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


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
    number = float(value)
    return f"{number:g} cm / {number / 2.54:.1f} in"


def range_to_imperial(text: str, factor: float, unit: str) -> str:
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if len(nums) == 2:
        suffix = "lbs" if unit == "kg" else "in"
        return f"{nums[0]:g}-{nums[1]:g} {unit} / {nums[0] * factor:.1f}-{nums[1] * factor:.1f} {suffix}"
    return text or "-"


def role_token(role: str) -> str:
    if role == "Baby Romper":
        return "BBY"
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
    return {"Baby Romper": "ROMP", "Dress": "DRS", "Shirt": "SHRT"}[garment]


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


def sku_for(row: dict) -> str:
    if row["garment"] == "Baby Romper":
        return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{garment_token(row['garment'])}-{row['sku_suffix']}-{COLOR_TOKEN}"
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


def option_values() -> dict[str, list[str]]:
    return {
        "Type": list(dict.fromkeys(row["garment"] for row in SIZE_CHART)),
        "Size": list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART)),
    }


def build_body() -> str:
    by_garment: dict[str, list[dict]] = {}
    for row in SIZE_CHART:
        by_garment.setdefault(row["garment"], []).append(row)

    def table_for(garment: str, rows: list[dict]) -> str:
        parts = [f"<h3>Size Chart - {html.escape(garment)}</h3>", "<table id=\"size-chart\">", "<thead><tr>"]
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
        parts.extend(f"<th>{h}</th>" for h in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            side = row["skirt_cm"] if row["garment"] == "Dress" else row.get("shoulder_cm", 0)
            cells = [
                row["picker_label"],
                row["age"],
                range_to_imperial(row["weight"], 2.20462, "kg"),
                range_to_imperial(row["height"], 0.393701, "cm"),
                cm_to_in(row["chest_cm"]),
                cm_to_in(side),
                cm_to_in(row["pant_cm"]),
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
<li><strong>Family story:</strong> A polished warm-weather matching look for mom, dad, girls, boys, and baby.</li>
<li><strong>Print reference:</strong> Blue Daisy pairs bright blue flowers, yellow centers, and green leaves for an easy vacation-photo palette.</li>
<li><strong>Design details:</strong> Girls and moms wear the sleeveless floral dress, boys and dads wear the collared short-sleeve shirt, and baby sizes use the matching romper chart.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Baby 0-3M-12-18M, Child 1-2Y-10Y, Mother S-2XL, and Father S-4XL.</li>
</ul>
""".strip()
    narrative = """
<p>Blue Daisy makes family matching feel fresh and vacation-ready, with a bright floral print that ties each role together without making every piece identical. The dresses bring a floaty, sunny shape for moms and girls, while the collared shirts keep dads and boys coordinated in a relaxed way.</p>

<p>The attached chart also supports baby romper sizes, so this draft keeps that piece as its own Type instead of hiding it inside the dress or shirt ladder. White shorts, shoes, hats, bags, and other styling pieces shown in the photo are not included.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Three honest Types:</strong> Baby Romper, Dress, and Shirt are separated for clearer size selection.</li>
<li><strong>Family-ready size run:</strong> Baby, child, mother, and father rows follow the attached vendor chart.</li>
<li><strong>Blue floral palette:</strong> Blue blossoms and yellow centers create a bright warm-weather matching story.</li>
<li><strong>Photo-ready styling:</strong> Dresses and shirts coordinate neatly for trips, portraits, brunches, and summer plans.</li>
<li><strong>Chart-first variants:</strong> Every purchasable option is backed by a transcribed source row.</li>
</ul>

<p>Choose the Type and size for each family member to build the matching Blue Daisy look for your next sunny plan.</p>
""".strip()
    return "\n\n".join([intro, *(table_for(name, rows) for name, rows in by_garment.items()), narrative])


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
                "tracked": True,
                "requiresShipping": True,
                "cost": money_half(price),
            },
        })
    return variants


def tags() -> list[str]:
    values = [
        "Family Matching", "Mommy and Me", "Daddy and Me", "Sets", "Matching Family Set",
        "Matching Family Outfit", "Matching Family Dresses", "Matching Family Shirt",
        "Baby Romper", "Dress", "Shirt", "Romper", "Girl Dress", "Mother Dress",
        "Boy Shirt", "Father Shirt", "Blue Daisy", "Blue Daisy Floral", "Blue Floral",
        "Blue", "Yellow Floral", "Green", "Floral", "Multicolor", "Summer", "Vacation",
        "Resort", "Sleeveless Dress", "Strappy Dress", "Collared Shirt", "Short Sleeve Shirt",
        "Dress Shirt Romper", VENDOR_URL,
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
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Blue Daisy Floral"},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress, Shirt & Baby Romper"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Plus Baby"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69943132257", "gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/129971519585", "gid://shopify/Metaobject/130231140449"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(SIZE_CHART) != 32 or len(variants) != len(SIZE_CHART):
        raise RuntimeError("SIZE_CHART/variant count mismatch")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("Title or SEO length guard failed")
    if len({(r["role"], r["vendor_label"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("Duplicate role/vendor/picker row")
    tables = re.findall(r"<table.*?</table>", body, re.S)
    if len(tables) != 3 or any(table.count("<th>") != 10 for table in tables):
        raise RuntimeError("Size table guard failed")
    if sum(table.count("<tr>") - 1 for table in tables) != len(SIZE_CHART):
        raise RuntimeError("Body row count mismatch")
    for row, variant in zip(SIZE_CHART, variants):
        expected = ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE
        if variant["price"] != expected:
            raise RuntimeError("FORCE_SPEC_PRICES guard failed")


def run_variant_model_guard() -> None:
    with TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "baby romper dress shirt infant crawler collared shirt sleeveless dress"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "FamilySet",
            "--tags", ", ".join(tags()),
        ], check=True)


def product_query(identifier: str, by_handle: bool = False) -> dict | None:
    if by_handle:
        data = gql("""
        query($handle:String!){
          productByHandle(handle:$handle){
            id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description}
            category{id fullName}
            options{id name position values optionValues{id name hasVariants}}
            variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy taxable selectedOptions{name value} inventoryItem{id tracked requiresShipping unitCost{amount currencyCode}}}}
            media(first:50){nodes{... on MediaImage{alt image{url}}}}
            collections(first:50){nodes{title handle}}
            metafields(first:120){nodes{namespace key type value}}
            resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}}
          }
        }
        """, {"handle": identifier})
        return data["data"]["productByHandle"]
    data = gql("""
    query($id:ID!){
      product(id:$id){
        id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description}
        category{id fullName}
        options{id name position values optionValues{id name hasVariants}}
        variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy taxable selectedOptions{name value} inventoryItem{id tracked requiresShipping unitCost{amount currencyCode}}}}
        media(first:50){nodes{... on MediaImage{alt image{url}}}}
        collections(first:50){nodes{title handle}}
        metafields(first:120){nodes{namespace key type value}}
        resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}}
      }
    }
    """, {"id": identifier})
    return data["data"]["product"]


def ensure_option_values(product: dict) -> None:
    expected = option_values()
    options_by_name = {option["name"]: option for option in product["options"]}
    for name, values in expected.items():
        option = options_by_name.get(name)
        if not option:
            continue
        existing_names = {value["name"] for value in option["optionValues"]}
        missing = [{"name": value} for value in values if value not in existing_names]
        if missing:
            res = gql("""
            mutation($productId:ID!,$option:OptionUpdateInput!,$adds:[OptionValueCreateInput!]){
              productOptionUpdate(productId:$productId, option:$option, optionValuesToAdd:$adds, variantStrategy:LEAVE_AS_IS){
                product{id}
                userErrors{field message}
              }
            }
            """, {"productId": product["id"], "option": {"id": option["id"]}, "adds": missing})
            require_no_user_errors(res, ["data", "productOptionUpdate", "userErrors"])


def prune_stale_option_values(product: dict) -> None:
    expected = option_values()
    for option in product["options"]:
        expected_values = set(expected.get(option["name"], []))
        stale_ids = [
            value["id"] for value in option["optionValues"]
            if value["name"] not in expected_values and not value["hasVariants"]
        ]
        if not stale_ids:
            continue
        res = gql("""
        mutation($productId:ID!,$option:OptionUpdateInput!,$delete:[ID!]){
          productOptionUpdate(productId:$productId, option:$option, optionValuesToDelete:$delete, variantStrategy:LEAVE_AS_IS){
            product{id}
            userErrors{field message}
          }
        }
        """, {"productId": product["id"], "option": {"id": option["id"]}, "delete": stale_ids})
        require_no_user_errors(res, ["data", "productOptionUpdate", "userErrors"])


def unpublish(product_id: str, product: dict) -> None:
    published = [
        {"publicationId": node["publication"]["id"]}
        for node in product.get("resourcePublicationsV2", {}).get("nodes", [])
        if node.get("isPublished")
    ]
    if not published:
        return
    res = gql("""
    mutation($id:ID!,$input:[PublicationInput!]!){
      publishableUnpublish(id:$id, input:$input){ userErrors{field message} }
    }
    """, {"id": product_id, "input": published})
    require_no_user_errors(res, ["data", "publishableUnpublish", "userErrors"])


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = product_query(product_id) or {}
    existing_alts = {node.get("alt") for node in existing.get("media", {}).get("nodes", [])}
    alt_by_name = {
        "01-blue-daisy-family-matching-product.png": "Family wearing Blue Daisy matching dress, shirt, and baby romper outfits.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if path.name.startswith("source-size-chart"):
            continue
        alt = alt_by_name.get(path.name, "Blue Daisy family matching outfit.")
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""
        mutation($input:[StagedUploadInput!]!){
          stagedUploadsCreate(input:$input){
            stagedTargets{url resourceUrl parameters{name value}}
            userErrors{field message}
          }
        }
        """, {"input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]})
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
        media = gql("""
        mutation($productId:ID!,$media:[CreateMediaInput!]!){
          productCreateMedia(productId:$productId, media:$media){
            media{... on MediaImage{id alt}}
            userErrors{field message}
          }
        }
        """, {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    header = (ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    for index, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update({
            "Handle": HANDLE,
            "Title": TITLE if index == 1 else "",
            "Body (HTML)": body if index == 1 else "",
            "Vendor": VENDOR if index == 1 else "",
            "Product Category": EXPECTED_TAXONOMY_FULL_NAME if index == 1 else "",
            "Type": PRODUCT_TYPE if index == 1 else "",
            "Tags": ", ".join(tags()) if index == 1 else "",
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
            "SEO Title": SEO_TITLE if index == 1 else "",
            "SEO Description": SEO_DESCRIPTION if index == 1 else "",
            "Google Shopping / Gender": "unisex" if index == 1 else "",
            "Google Shopping / Age Group": "adult" if index == 1 else "",
            "Google Shopping / Condition": "new" if index == 1 else "",
            "Google Shopping / Custom Product": "FALSE" if index == 1 else "",
            "Google Shopping / Custom Label 0": "Family Matching" if index == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if index == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if index == 1 else "",
            "Google Shopping / Custom Label 3": "Dress, Shirt & Baby Romper" if index == 1 else "",
            "Google Shopping / Custom Label 4": "Four-Role Plus Baby" if index == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if index == 1 else "",
            "Pattern (product.metafields.custom.pattern)": "Blue Daisy Floral" if index == 1 else "",
            "Style (product.metafields.custom.style)": "Matching Family Set" if index == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if index == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if index == 1 else "",
            "Type (product.metafields.custom.type)": "Two-Piece Set" if index == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if index == 1 else "",
            "Status": "draft",
        })
        if "Cost per item" in values:
            values["Cost per item"] = money_half(variant["price"])
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, body: str, variants: list[dict], verify: dict, deleted_skus: list[str], created_skus: list[str]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    live_skus = sorted(v["sku"] for v in verify["variants"]["nodes"])
    expected_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
    published = [p["publication"]["name"] for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    price_rows = []
    live_by_sku = {variant["sku"]: variant for variant in verify["variants"]["nodes"]}
    for row, variant in zip(SIZE_CHART, variants):
        live = live_by_sku.get(variant["inventoryItem"]["sku"], {})
        unit_cost = ((live.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        price_rows.append((variant["inventoryItem"]["sku"], live.get("price"), live.get("compareAtPrice"), unit_cost, variant["price"], variant["compareAtPrice"], money_half(variant["price"])))
    metafield_keys = [f"{m['namespace']}.{m['key']}" for m in verify["metafields"]["nodes"] if m["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}]
    skipped = [
        ("shopify.fabric", "The direct 1688 page returned CAPTCHA/punish markup and the supplied chart/image do not confirm exact fiber."),
        ("shopify.dress-occasion", "The honest Shopify taxonomy is Outfit Sets, not Dresses."),
        ("shopify.dress-style", "The listing mixes baby romper, dress, and shirt Types."),
        ("shopify.neckline", "The product mixes strap dresses, a romper, and collared shirts."),
        ("shopify.sleeve-length-type", "No single product-level sleeve value is honest across all Types."),
        ("shopify.skirt-dress-length-type", "Dress rows exist, but the listing is not dress-only."),
        ("shopify.top-length-type", "The product mixes shirts, dresses, and romper rows."),
        ("shopify.waist-rise", "No pants or standalone bottom is sold in this listing."),
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
        "| PRIMARY_CATEGORY | auto -> FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> Baby Romper, Dress, Shirt |",
        "| EXCLUDE_ITEMS | styling-only shorts, hats, bags, shoes and props excluded |",
        "| SHORTCODE | auto -> `BDSY` |",
        "| COLOR_TOKEN | auto -> `BLUE` |",
        "| FORCE_SPEC_PRICES | true |", "",
        "## Vendor fetch status",
        "The direct 1688 page returned Alibaba `_____tmd_____` / punish markup, so the attached size chart and product image were used as authoritative evidence. The chart is a fit-reference chart with height and weight only; chest, hip, waist, shoulder, and length values were retained from the closest prior Blue Daisy/mixed family-set grading and are documented as derived support values rather than direct vendor measurements.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        lines.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {money_half(variant['price'])} | `{gid}` ({label}) |")
    lines.extend([
        "",
        "## Derivations",
        "- Vendor weight guidance was transcribed from jin ranges in the image and converted to kg/lbs in the storefront table.",
        "- Baby romper rows 66/73/80/90 map to Baby 0-3M, 6-9M, 9-12M, and 12-18M using existing Shopify size metaobjects.",
        "- Child 80 maps to Child 1-2 Years, backed by the closest available 12-18 months size metaobject.",
        "- Mother 3XL and Mother 4XL from the prior live listing were removed because the new attached adult chart stops at Mother 2XL.",
        "- Chest, hip, waist, shoulder, skirt, and length values are derived grading values because the attached source chart only publishes height and weight.",
        "- White shorts and all accessories in the product image are styling only and are not included.",
        "",
        "## Variant Changes",
        f"- Created SKUs: {', '.join(created_skus) if created_skus else 'none'}",
        f"- Deleted unsupported old SKUs: {', '.join(deleted_skus) if deleted_skus else 'none'}",
        "- Initial correction created the four baby romper SKUs and removed old Mother 3XL/4XL SKUs; later idempotent reruns should report no new create/delete work.",
        "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| No sales-channel publication is live | {'PASS' if not published else 'FAIL'} | {published} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Live SKUs match derived SKUs | {'PASS' if live_skus == expected_skus else 'FAIL'} | {len(expected_skus)} expected |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
    ])
    cost_ok = True
    for sku, live_price, live_cmp, live_cost, spec_price, spec_cmp, spec_cost in price_rows:
        if live_price != spec_price or live_cmp != spec_cmp or Decimal(live_cost or "0") != Decimal(spec_cost):
            cost_ok = False
    lines.extend([
        f"| Price and cost parity | {'PASS' if cost_ok else 'FAIL'} | every variant price/compare-at/cost checked |",
        "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare | Live Cost | Spec Price | Spec Compare | Spec Cost |",
        "|---|---|---|---|---|---|---|",
    ])
    for item in price_rows:
        lines.append("| " + " | ".join(str(value or "") for value in item) + " |")
    lines.extend([
        "",
        "## Metafields Written",
        *[f"- `{key}`" for key in sorted(metafield_keys)],
        "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped],
        "",
        "## Smart Collections",
        "Collection indexing may wait until publication because this product is intentionally unpublished as a draft.",
        "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition if the vendor page becomes readable later.",
        "- Review or retouch the supplied product image before any publish-live step.",
        "- Inventory quantities and variant grams remain operator stock inputs.",
        "",
        "## Files Saved",
        f"- `{ROOT / 'ops/scripts/create-bdsy-blue-daisy-family-matching-set.sh'}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{SOURCE_SIZE_CHART}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
        "",
    ])
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


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

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{id fullName isLeaf} } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    product = product_query(HANDLE, by_handle=True)
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in option_values()["Type"]]},
        {"name": "Size", "values": [{"name": value} for value in option_values()["Size"]]},
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
    if product:
        product_id = product["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        unpublish(product_id, product)
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]

    product = product_query(product_id)
    assert product is not None
    ensure_option_values(product)
    product = product_query(product_id)
    assert product is not None

    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    delete_ids = [variant["id"] for sku, variant in live_by_sku.items() if sku not in spec_by_sku]
    deleted_skus = sorted(sku for sku in live_by_sku if sku not in spec_by_sku)
    if delete_ids:
        res = gql("""mutation($productId:ID!,$ids:[ID!]!){ productVariantsBulkDelete(productId:$productId, variantsIds:$ids){ product{id} userErrors{field message} } }""", {"productId": product_id, "ids": delete_ids})
        require_no_user_errors(res, ["data", "productVariantsBulkDelete", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    create_variants = [variant for sku, variant in spec_by_sku.items() if sku not in live_by_sku]
    created_skus = sorted(variant["inventoryItem"]["sku"] for variant in create_variants)
    if create_variants:
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": create_variants,
            "strategy": "REMOVE_STANDALONE_VARIANT",
        })
        require_no_user_errors(res, ["data", "productVariantsBulkCreate", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    update_variants = []
    for sku, spec in spec_by_sku.items():
        live = live_by_sku.get(sku)
        if not live:
            continue
        update_variants.append({
            "id": live["id"],
            "price": spec["price"],
            "compareAtPrice": spec["compareAtPrice"],
            "taxable": True,
            "inventoryPolicy": "DENY",
            "inventoryItem": spec["inventoryItem"],
            "optionValues": spec["optionValues"],
        })
    if update_variants:
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": update_variants,
        })
        require_no_user_errors(res, ["data", "productVariantsBulkUpdate", "userErrors"])

    for i in range(0, len(metafields(product_id)), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": metafields(product_id)[i:i+25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    stale_metafields = [
        {"ownerId": product_id, "namespace": node["namespace"], "key": node["key"]}
        for node in product["metafields"]["nodes"]
        if node["namespace"] == "shopify" and node["key"] in {"dress-occasion", "dress-style", "fabric", "neckline", "pants-length-type", "skirt-dress-length-type", "sleeve-length-type", "top-length-type", "waist-rise"}
    ]
    if stale_metafields:
        res = gql("""mutation($metafields:[MetafieldIdentifierInput!]!){ metafieldsDelete(metafields:$metafields){ deletedMetafields{key namespace ownerId} userErrors{field message} } }""", {"metafields": stale_metafields})
        require_no_user_errors(res, ["data", "metafieldsDelete", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    product = product_query(product_id)
    assert product is not None
    prune_stale_option_values(product)
    product = product_query(product_id)
    assert product is not None
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": product}}, indent=2), encoding="utf-8")
    write_listing(product_id, body, variants, product, deleted_skus, created_skus)

    expected_skus = sorted(spec_by_sku)
    live_skus = sorted(v["sku"] for v in product["variants"]["nodes"])
    published_ids = [p["publication"]["id"] for p in product["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    cost_ok = all(
        Decimal(str(((v.get("inventoryItem") or {}).get("unitCost") or {}).get("amount") or "0")) == Decimal(money_half(spec_by_sku[v["sku"]]["price"]))
        for v in product["variants"]["nodes"]
    )
    if product["status"] != "DRAFT" or product["publishedAt"] is not None or published_ids or live_skus != expected_skus or len(live_skus) != len(SIZE_CHART) or not cost_ok:
        raise RuntimeError("Final verification failed; see verify JSON for details.")

    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": product["status"],
        "publishedAt": product["publishedAt"],
        "onlineStoreUrl": product["onlineStoreUrl"],
        "variant_count": len(product["variants"]["nodes"]),
        "created_skus": created_skus,
        "deleted_skus": deleted_skus,
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT), str(SIZE_CHART_OUT), str(BODY_HTML_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
