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

HANDLE = "summer-plaid-family-matching-set"
TITLE = "Summer Plaid Family Matching Set - Hoodie, Tee & Shorts"
SEO_TITLE = "Summer Plaid Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Family matching summer set in beige plaid for mom, dad, girls and boys. Hooded shirt, graphic tee and cargo shorts in Child 1-2Y-10Y and Adult S-3XL."
PRINT_NAME = "Summer Plaid"
SHORTCODE = "SPLD"
COLOR_TOKEN = "PLAID"
COLOR_NAME = "Beige Plaid"
VENDOR_URL = "https://detail.1688.com/offer/1031073458269.html"
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
    "Adult S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Adult M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Adult L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Adult XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Adult 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Adult 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":36,"shoulder_cm":35,"sleeve_cm":25,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":39,"shoulder_cm":38,"sleeve_cm":28,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":42,"shoulder_cm":41,"sleeve_cm":31,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":45,"shoulder_cm":43,"sleeve_cm":34,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":48,"shoulder_cm":44,"sleeve_cm":36,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":50,"shoulder_cm":45,"sleeve_cm":39,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":52,"shoulder_cm":46,"sleeve_cm":42,"pant_cm":0},
    {"audience":"child","role":"Child Hooded Shirt","garment":"Hooded Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":55,"shoulder_cm":48,"sleeve_cm":45,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":104,"hip_cm":104,"waist_cm":92,"length_cm":65,"shoulder_cm":52,"sleeve_cm":50,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":66,"shoulder_cm":53,"sleeve_cm":52,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":67,"shoulder_cm":55,"sleeve_cm":54,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":69,"shoulder_cm":57,"sleeve_cm":55,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"XXL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":116,"hip_cm":116,"waist_cm":104,"length_cm":71,"shoulder_cm":59,"sleeve_cm":55,"pant_cm":0},
    {"audience":"adult","role":"Adult Hooded Shirt","garment":"Hooded Shirt","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":120,"hip_cm":120,"waist_cm":108,"length_cm":74,"shoulder_cm":61,"sleeve_cm":56,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":35,"shoulder_cm":28,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":38,"shoulder_cm":30,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":41,"shoulder_cm":32,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":44,"shoulder_cm":34,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":47,"shoulder_cm":36,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":50,"shoulder_cm":38,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":53,"shoulder_cm":40,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child T-Shirt","garment":"T-Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":56,"shoulder_cm":48,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":66,"shoulder_cm":45,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":68,"shoulder_cm":47,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":70,"shoulder_cm":49,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":72,"shoulder_cm":50,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"XXL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":74,"shoulder_cm":51,"sleeve_cm":0,"pant_cm":0},
    {"audience":"adult","role":"Adult T-Shirt","garment":"T-Shirt","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":76,"shoulder_cm":52,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":0,"hip_cm":80,"waist_cm":76,"length_cm":29,"sleeve_cm":0,"pant_cm":29},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":0,"hip_cm":84,"waist_cm":80,"length_cm":32,"sleeve_cm":0,"pant_cm":32},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":0,"hip_cm":84,"waist_cm":80,"length_cm":35,"sleeve_cm":0,"pant_cm":35},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":0,"hip_cm":88,"waist_cm":84,"length_cm":38,"sleeve_cm":0,"pant_cm":38},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":0,"hip_cm":92,"waist_cm":88,"length_cm":41,"sleeve_cm":0,"pant_cm":41},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":0,"hip_cm":96,"waist_cm":92,"length_cm":44,"sleeve_cm":0,"pant_cm":44},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":0,"hip_cm":100,"waist_cm":96,"length_cm":47,"sleeve_cm":0,"pant_cm":47},
    {"audience":"child","role":"Child Shorts","garment":"Shorts","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":0,"hip_cm":104,"waist_cm":100,"length_cm":50,"sleeve_cm":0,"pant_cm":50},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"S","picker_label":"Adult S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":0,"hip_cm":112,"waist_cm":108,"length_cm":56,"sleeve_cm":0,"pant_cm":56},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":0,"hip_cm":114,"waist_cm":110,"length_cm":57,"sleeve_cm":0,"pant_cm":57},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":0,"hip_cm":116,"waist_cm":112,"length_cm":58,"sleeve_cm":0,"pant_cm":58},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":0,"hip_cm":120,"waist_cm":116,"length_cm":59,"sleeve_cm":0,"pant_cm":59},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"XXL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":0,"hip_cm":124,"waist_cm":120,"length_cm":60,"sleeve_cm":0,"pant_cm":60},
    {"audience":"adult","role":"Adult Shorts","garment":"Shorts","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":0,"hip_cm":128,"waist_cm":124,"length_cm":61,"sleeve_cm":0,"pant_cm":61},
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
    if value in (None, "", 0, "—", "-"):
        return "—"
    number = float(value)
    shown = f"{number:g}"
    return f"{shown} cm / {number / 2.54:.1f} in"


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
    if role.startswith("Child"):
        return "KID"
    if role.startswith("Adult"):
        return "ADT"
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Boy"):
        return "BOY"
    if role.startswith("Mother"):
        return "MOM"
    if role.startswith("Father"):
        return "DAD"
    return "GEN"


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "adult" else CHILD_PRICE


def garment_token(garment: str) -> str:
    return {
        "Hooded Shirt": "HDY",
        "T-Shirt": "TEE",
        "Shorts": "SHT",
    }.get(garment, re.sub(r"[^A-Z0-9]", "", garment.upper())[:4])


def build_body() -> str:
    by_garment: dict[str, list[dict]] = {}
    for row in SIZE_CHART:
        by_garment.setdefault(row["garment"], []).append(row)

    def table_for(garment: str, rows: list[dict]) -> str:
        measure = "Pant/Short" if garment == "Shorts" else "Sleeve" if garment in {"Hooded Shirt", "T-Shirt", "Shirt"} else "Sleeve or —"
        parts = [f"<h3>Size Chart - {html.escape(garment)}</h3>", "<table id=\"size-chart\">", "<thead><tr>"]
        headers = ["Size", "Age", "Weight (kg/lbs)", "Height (cm/in)", "Chest/Bust (cm/in)", f"{measure} (cm/in)", "Pant/Short or — (cm/in)", "Hip (cm/in)", "Waist (cm/in)", "Garment Length (cm/in)"]
        parts.extend(f"<th>{h}</th>" for h in headers)
        parts.append("</tr></thead><tbody>")
        for row in rows:
            side = row.get("pant_cm") if garment == "Shorts" else row.get("sleeve_cm")
            cells = [
                row["picker_label"],
                row["age"],
                kg_to_lb(row["weight"]),
                cm_to_in(row["height"].replace(" cm", "")) if re.fullmatch(r"[\d.]+-[\d.]+ cm", row["height"]) is None else f"{row['height']} / " + "-".join(f"{float(n)/2.54:.1f}" for n in re.findall(r"[\d.]+", row["height"])) + " in",
                cm_to_in(row["chest_cm"]),
                "—" if garment == "Shorts" else cm_to_in(side),
                cm_to_in(side) if garment == "Shorts" else "—",
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            parts.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>")
        parts.append("</tbody></table>")
        return "\n".join(parts)

    intro = """
<ul>
<li><strong>Fabric:</strong> Lightweight summer woven and knit pieces; exact fiber content was not visible in the supplied evidence.</li>
<li><strong>Family story:</strong> A coordinated warm-weather outfit for mom, dad, girls, and boys, built from matching beige plaid and easy neutral layers.</li>
<li><strong>Print:</strong> Summer Plaid pairs soft beige checks with a cream graphic tee and muted gray-green cargo shorts.</li>
<li><strong>Design details:</strong> Choose the hooded plaid overshirt, short-sleeve graphic T-shirt, or cargo shorts by size to build each family member's look.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Child 1-2Y-10Y and Adult S-3XL across hooded shirts, T-shirts, and shorts.</li>
</ul>
""".strip()
    tables = "\n\n".join(table_for(name, rows) for name, rows in by_garment.items())
    narrative = """
<p>Summer Plaid is an easy family outfit for travel days, park dates, school-break photos, and casual weekend plans. The beige plaid hooded shirt gives the look its matching anchor, while the cream tee and cargo shorts keep the set relaxed and wearable.</p>

<p>The pieces are listed separately inside one family matching product so you can build the outfit honestly by person and garment. Pick the hooded shirt, T-shirt, or shorts in the child or adult size each family member needs.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Three-piece coordination:</strong> Hooded shirt, graphic tee, and cargo shorts are all supported by the attached vendor chart.</li>
<li><strong>Family-size ladder:</strong> Child 80-150 and adult S-3XL rows are included for every listed garment.</li>
<li><strong>Neutral summer palette:</strong> Beige plaid, cream, and gray-green tones are easy to photograph together.</li>
<li><strong>Buildable matching look:</strong> Mix the top and bottom pieces per family member instead of buying an unsupported bundle.</li>
<li><strong>Draft-only safety:</strong> Created as an unpublished Shopify draft pending operator review.</li>
</ul>

<p>Choose each garment and size to build a coordinated summer look for the whole family.</p>
""".strip()
    return "\n\n".join([intro, tables, narrative])


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
        "Matching Family Outfits", "Matching Family Set", "Matching Family Top", "Matching Family Bottoms",
        "Hooded Shirt", "T-Shirt", "Cargo Shorts", "Summer", "Resort", "Vacation",
        PRINT_NAME, "Beige", "Cream", "Plaid", "Gray Green", "Neutral Plaid",
        "Child Hooded Shirt", "Adult Hooded Shirt", "Child T-Shirt", "Adult T-Shirt", "Child Shorts", "Adult Shorts",
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
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Hoodie, Tee & Shorts"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Family Matching Outfit"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69639733345","gid://shopify/Metaobject/130283143265"])},
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
        "lo": "Family wearing summer plaid hooded shirts, graphic tees, and cargo shorts.",
        "so": "Vendor size chart for Summer Plaid family matching outfit.",
        "01": "Family wearing summer plaid hooded shirts, graphic tees, and cargo shorts.",
        "02": "Family styling the summer plaid matching hooded shirt and shorts.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.name.startswith("source-"):
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        alt = alt_by_prefix.get(path.name[:2], alt_by_prefix.get(path.name[:2].lower(), "Summer Plaid family matching set."))
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
            "Google Shopping / Custom Label 3": "Hoodie, Tee & Shorts" if i == 1 else "",
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


def write_listing(product: dict, body: str, variants: list[dict], verify: dict) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product['id'].split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | `{gid}` ({label}) |")
    skipped = [
        ("shopify.sleeve-length-type", "Mixed hooded overshirts, T-shirts, and shorts; one product-level sleeve value would mislead."),
        ("shopify.neckline", "Different necklines across hooded shirt and T-shirt."),
        ("shopify.top-length-type", "Mixed tops and bottoms; no single honest top-length value applies."),
        ("shopify.fabric", "Exact fiber composition was not visible in the supplied evidence, so fabric is documented in copy only."),
        ("shopify.dress-occasion", "Product is not a dress listing."),
        ("shopify.dress-style", "Product is not a dress listing."),
        ("shopify.skirt-dress-length-type", "Product is not a dress listing."),
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
        "| SIZE_CHART_SOURCE | attached size-chart image and supplied product photos |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> hooded shirt, T-shirt, and shorts in Summer Plaid |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor fetch status",
        "Direct public access to the 1688 offer can be anti-bot protected, so the attached size chart and supplied product photos were used as authoritative evidence per the canonical workflow. The draft remains unpublished for operator review.",
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
        "- Vendor 斤 guidance was converted to kg/lbs in the shopper-facing table.",
        "- Hooded shirt and T-shirt chest values were doubled from the vendor half-bust chart values; hip and waist follow the canonical shirt/top derivation.",
        "- Shorts waist values were treated as flat/half-waist chart values and doubled; hip was derived as waist + 4 cm.",
        "- The vendor publishes generic child/adult rows rather than separate mom/dad/girl/boy ladders, so variants use `Child ...` and `Adult ...` picker labels.",
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
        "- Confirm exact fabric composition and care details before publishing if the vendor page becomes available.",
        "- Inventory quantities and per-variant weights still need operator stock values.",
        "- Review whether the outfit should stay as three separately selectable pieces or be split into tops and bottoms later.",
        "",
        "## Files saved",
        f"- `{ROOT / 'ops' / 'scripts' / 'create-spld-summer-plaid-family-matching-set.sh'}`",
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

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Hooded Shirt", "T-Shirt", "Shorts"]]},
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
        live_by_options = {
            tuple((opt["name"], opt["value"]) for opt in v["selectedOptions"]): v
            for v in existing["variants"]["nodes"]
        }
        update_inputs = []
        for variant in variants:
            key = tuple((opt["optionName"], opt["name"]) for opt in variant["optionValues"])
            live = live_by_options.get(key)
            if not live:
                raise RuntimeError(f"Existing draft is missing variant options: {key}")
            update_inputs.append({
                "id": live["id"],
                "price": variant["price"],
                "compareAtPrice": variant["compareAtPrice"],
                "inventoryPolicy": variant["inventoryPolicy"],
                "inventoryItem": variant["inventoryItem"],
            })
        for i in range(0, len(update_inputs), 100):
            bulk_update = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku price compareAtPrice inventoryPolicy} userErrors{field message} } }""", {
                "productId": product_id,
                "variants": update_inputs[i:i+100],
            })
            require_no_user_errors(bulk_update, ["data", "productVariantsBulkUpdate", "userErrors"])
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
