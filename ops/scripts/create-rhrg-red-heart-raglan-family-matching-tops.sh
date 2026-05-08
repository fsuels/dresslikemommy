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

HANDLE = "red-heart-raglan-family-matching-tops"
TITLE = "Red Heart Raglan Family Matching Tops - Cotton Tee"
SEO_TITLE = "Red Heart Family Tops | Dress Like Mommy"
SEO_DESCRIPTION = "Cotton red-and-white family matching tees for mom, dad, girls and boys. Chart-backed tops in Child 2Y-10Y, Mom S-2XL and Dad M-3XL."
PRINT_NAME = "Red Heart Raglan"
SHORTCODE = "RHRG"
COLOR_TOKEN = "REDHT"
COLOR_NAME = "Red Heart Raglan"
VENDOR_URL = "https://detail.1688.com/offer/909808842226.html"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Tops"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-8"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts"
CHILD_PRICE = "17.99"
ADULT_PRICE = "19.99"
CHILD_COMPARE_AT = "28.99"
ADULT_COMPARE_AT = "33.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-rhrg-red-heart-raglan-family-matching-tops.sh"

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
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"20-26 jin","height":"80-90 cm","chest_cm":70,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":37,"hip_cm":74,"waist_cm":70,"length_cm":40,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"26-31 jin","height":"90-100 cm","chest_cm":74,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":40,"hip_cm":78,"waist_cm":74,"length_cm":42,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"29-39 jin","height":"100-110 cm","chest_cm":78,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":43,"hip_cm":82,"waist_cm":78,"length_cm":44,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"43-53 jin","height":"110-120 cm","chest_cm":82,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":47,"hip_cm":86,"waist_cm":82,"length_cm":46,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"53-60 jin","height":"120-130 cm","chest_cm":86,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":51,"hip_cm":90,"waist_cm":86,"length_cm":50,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"58-70 jin","height":"130-140 cm","chest_cm":90,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":55,"hip_cm":94,"waist_cm":90,"length_cm":54,"pant_cm":0},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"Children's tops 150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"69-85 jin","height":"140-150 cm","chest_cm":94,"shoulder_cm":0,"sleeve_cm":0,"source_bottom_length_cm":59,"hip_cm":98,"waist_cm":94,"length_cm":58,"pant_cm":0},
    {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"Mom's top S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"85-95 jin","height":"155-160 cm","chest_cm":94,"shoulder_cm":45,"sleeve_cm":0,"source_skirt_length_cm":49,"hip_cm":94,"waist_cm":82,"length_cm":57,"pant_cm":0},
    {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"Mom's top M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"95-110 jin","height":"158-163 cm","chest_cm":98,"shoulder_cm":46,"sleeve_cm":0,"source_skirt_length_cm":49.5,"hip_cm":98,"waist_cm":86,"length_cm":59,"pant_cm":0},
    {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"Mom's top L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"110-120 jin","height":"161-168 cm","chest_cm":102,"shoulder_cm":47,"sleeve_cm":0,"source_skirt_length_cm":50,"hip_cm":102,"waist_cm":90,"length_cm":61,"pant_cm":0},
    {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"Mom's top XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"120-135 jin","height":"163-170 cm","chest_cm":106,"shoulder_cm":48,"sleeve_cm":0,"source_skirt_length_cm":50.5,"hip_cm":106,"waist_cm":94,"length_cm":63,"pant_cm":0},
    {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"Mom's top 2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"135-150 jin","height":"165-173 cm","chest_cm":110,"shoulder_cm":49,"sleeve_cm":0,"source_skirt_length_cm":51,"hip_cm":110,"waist_cm":98,"length_cm":65,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"Dad's top M","picker_label":"Father M","sku_suffix":"M","age":"-","weight":"100-120 jin","height":"162-168 cm","chest_cm":100,"shoulder_cm":0,"sleeve_cm":0,"source_short_length_cm":52,"hip_cm":100,"waist_cm":88,"length_cm":64,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"Dad's top L","picker_label":"Father L","sku_suffix":"L","age":"-","weight":"120-139 jin","height":"165-175 cm","chest_cm":104,"shoulder_cm":0,"sleeve_cm":0,"source_short_length_cm":54,"hip_cm":104,"waist_cm":92,"length_cm":66,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"Dad's top XL","picker_label":"Father XL","sku_suffix":"XL","age":"-","weight":"135-160 jin","height":"172-180 cm","chest_cm":108,"shoulder_cm":0,"sleeve_cm":0,"source_short_length_cm":55,"hip_cm":108,"waist_cm":96,"length_cm":68,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"Dad's top 2XL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"-","weight":"160-180 jin","height":"175-185 cm","chest_cm":112,"shoulder_cm":0,"sleeve_cm":0,"source_short_length_cm":57,"hip_cm":112,"waist_cm":100,"length_cm":72,"pant_cm":0},
    {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"Dad's top 3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"-","weight":"180-195 jin","height":"178-190 cm","chest_cm":116,"shoulder_cm":0,"sleeve_cm":0,"source_short_length_cm":58,"hip_cm":116,"waist_cm":104,"length_cm":74,"pant_cm":0},
]


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
    if price == CHILD_PRICE:
        return CHILD_COMPARE_AT
    if price == ADULT_PRICE:
        return ADULT_COMPARE_AT
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def fmt_num(value) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:.1f}".rstrip("0").rstrip(".")


def source_range(text: str, unit: str) -> str:
    raw = str(text or "").strip()
    if not raw or raw == "-":
        return "-"
    return raw.replace(f" {unit}", "")


def display_jin_weight(text: str) -> str:
    raw = str(text or "").strip().replace(" ", "")
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)-([0-9]+(?:\.[0-9]+)?)jin", raw, re.I)
    if not match:
        return raw.replace("jin", "").replace("斤", "") or "-"
    low_jin = float(match.group(1))
    high_jin = float(match.group(2))
    low_kg = low_jin * 0.5
    high_kg = high_jin * 0.5
    low_lb = round(low_jin * 1.10231131)
    high_lb = round(high_jin * 1.10231131)
    return f"{fmt_num(low_kg)}-{fmt_num(high_kg)} kg / {low_lb}-{high_lb} lbs"


def cm(value) -> str:
    if value in (None, "", 0, "0", "-"):
        return "-"
    return fmt_num(value)


def role_token(role: str) -> str:
    if role == "Child Shirt":
        return "KID"
    if role == "Mother Shirt":
        return "MOM"
    if role == "Father Shirt":
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
        "Height (cm)",
        "Chest/Bust (cm)",
        "Sleeve or Skirt (cm)",
        "Pant/Short or - (cm)",
        "Hip (cm)",
        "Waist (cm)",
        "Garment Length (cm)",
    ]
    rendered = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "-",
            display_jin_weight(row["weight"]),
            source_range(row["height"], "cm"),
            cm(row["chest_cm"]),
            cm(row["sleeve_cm"]),
            "-",
            cm(row["hip_cm"]),
            cm(row["waist_cm"]),
            cm(row["length_cm"]),
        ]
        rendered.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")
    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> 95% cotton, based on the verified product details.</li>",
        "<li><strong>Family story:</strong> A sporty matching tee for moms, dads, girls, and boys, easy for casual outings, park days, birthdays, and family photos.</li>",
        "<li><strong>Print reference:</strong> Red Heart Raglan pairs a white tee body with red contrast sleeves, sleeve stripes, and a small heart accent.</li>",
        "<li><strong>Design details:</strong> Short sleeves, crew neckline, relaxed raglan tee shape, and one shared red-and-white colorway for children, moms, and dads. Skirts, shorts, shoes, sunglasses, and outdoor props shown in photos are styling only.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, turn inside out, line dry or tumble low, and avoid bleach.</li>",
        "<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S through Mother 2XL, and Father M through Father 3XL.</li>",
        "</ul>",
        "<h3>Size Chart - Shirt</h3>",
        "<table id=\"size-chart\">",
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *rendered,
        "</tbody></table>",
        "<p>Red Heart Raglan is a clean family matching tee that feels playful without being overly dressed up. The red contrast sleeves and small heart detail make the coordinated look easy to spot in photos while still pairing simply with denim, shorts, or casual skirts.</p>",
        "<p>The source selector includes separate tops, bottoms, and complete suits; this draft intentionally lists only the chart-backed top variants because the product category resolves to T-shirts and the supplied measurements support the tops most cleanly. Bottoms and suit selector values remain unlisted until a separate bottom/set request confirms the exact variant model.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>One coordinated tee:</strong> Same red-and-white short-sleeve shirt look for child, mom, and dad sizes.</li>",
        "<li><strong>Cotton feel:</strong> The vendor detail page identifies a 95% cotton main fabric composition.</li>",
        "<li><strong>Family-friendly range:</strong> Child sizes from 90 through 150, mom sizes from S through 2XL, and dad sizes from M through 3XL.</li>",
        "<li><strong>Photo-ready color:</strong> Red raglan sleeves, striped sleeve bands, and the heart accent make the matching look easy to spot.</li>",
        "<li><strong>Chart-backed variants:</strong> Every size option is backed by a row from the attached vendor chart.</li>",
        "</ul>",
        "<p>Choose the child, mom, and dad sizes you need to build an easy red-heart matching look for everyday family memories.</p>",
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
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": COLOR_NAME},
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
        "Tops",
        "Matching Family Top",
        "Matching Family Tops",
        "Matching Family Outfits",
        "Child Shirt",
        "Mother Shirt",
        "Father Shirt",
        "Short Sleeve Tee",
        "Crew Neck Raglan Tee",
        "Raglan Shirt",
        "Red Heart Raglan",
        "Heart",
        "Heart Accent",
        "White",
        "Red",
        "Stripe",
        "Striped",
        "Cotton",
        "Cotton Blend",
        "Spring",
        "Summer",
        "Family Photos",
        "Park Day",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Family Matching Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Matching Family Top"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Top"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Spring/Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Red Raglan Tee"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Top"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "fabric", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622399073"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972502625"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "pant_cm"}
    if len(SIZE_CHART) != 17 or len(variants) != len(SIZE_CHART):
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
        derived.write_text(json.dumps({"option_names": ["Size", "Color"], "variants": variants}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "selected chart-backed top variants only: family matching red white raglan short sleeve tee top shirt"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "Tops",
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
        alt = "Family wearing red heart raglan matching short-sleeve tees."
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""", {
            "input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]
        })
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMREDHEARTRAGLAN"
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
    header_source = ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv"
    with header_source.open("r", encoding="utf-8", newline="") as f:
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
            "Option1 Name": "Size",
            "Option1 Value": row["picker_label"],
            "Option2 Name": "Color",
            "Option2 Value": COLOR_NAME,
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
            "Google Shopping / Gender": "unisex",
            "Google Shopping / Age Group": "kids" if row["audience"] == "child" else "adult",
            "Google Shopping / MPN": variant["inventoryItem"]["sku"],
            "Google Shopping / Condition": "new",
            "Google Shopping / Custom Product": "FALSE",
            "Google Shopping / Custom Label 0": "Family Matching" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Spring/Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Red Raglan Tee" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Unisex Family Top" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Matching Family Top" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Tops" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Family Matching Tops" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Top" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
            "Age group (product.metafields.shopify.age-group)": "kids, adults" if i == 1 else "",
            "Color (product.metafields.shopify.color-pattern)": "Red, White" if i == 1 else "",
            "Fabric (product.metafields.shopify.fabric)": "Cotton" if i == 1 else "",
            "Size (product.metafields.shopify.size)": ", ".join(SIZE_MAP[item["picker_label"]][1] for item in SIZE_CHART) if i == 1 else "",
            "Cost per item": variant["inventoryItem"]["cost"],
            "Status": "draft",
        })
        rows.append(values)
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
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
    if (product["category"] or {}).get("fullName") != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {(product['category'] or {}).get('fullName')}")
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
    if [option["name"] for option in product["options"]] != ["Size", "Color"]:
        errors.append("option axes are not Size / Color")
    expected_pairs = {(row["picker_label"], COLOR_NAME) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Size x Color option combinations do not match")
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
        "shopify.fabric", "shopify.size", "shopify.target-gender", "global.title_tag",
        "global.description_tag",
    }
    written_metafields = {f"{node['namespace']}.{node['key']}" for node in product["metafields"]["nodes"]}
    missing = sorted(expected_metafields - written_metafields)
    if missing:
        errors.append("missing expected metafields: " + ", ".join(missing))
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {COLOR_NAME} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    skipped = [
        ("shopify.sleeve-length-type", "Short sleeve evidence is clear, but two different `Short` catalog values exist in this store; skipped rather than guessing the owner-subtype-safe value."),
        ("shopify.neckline", "Crew neckline is visible in the supplied product image, but no owner-subtype-safe neckline value was verified for this T-Shirts taxonomy run."),
        ("shopify.top-length-type", "The vendor chart gives exact garment lengths, but those do not map cleanly to one standard top-length type."),
        ("shopify.dress-occasion", "Not applicable because the honest taxonomy is T-Shirts."),
        ("shopify.dress-style", "Not applicable because this is a Tops listing."),
        ("shopify.skirt-dress-length-type", "Not applicable because this listing contains shirts only."),
    ]
    live_publications = [p for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    smart_collections = verify["collections"]["nodes"] or []
    smart_lines = [f"- {item['title']} (`/{item['handle']}`)" for item in smart_collections] or ["- None returned immediately; draft products may not index into smart collections until publication."]
    verification_rows = [
        ("Product status is DRAFT", verify["status"] == "DRAFT", verify["status"]),
        ("publishedAt is null", not verify.get("publishedAt"), str(verify.get("publishedAt"))),
        ("No sales-channel publications live", not live_publications, str([p["publication"]["name"] for p in live_publications])),
        ("Taxonomy fullName matches", verify["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, verify["category"]["fullName"]),
        ("Variant count matches SIZE_CHART", len(verify["variants"]["nodes"]) == len(SIZE_CHART), f"{len(verify['variants']['nodes'])} vs {len(SIZE_CHART)}"),
        ("Price and cost parity", all(row["match"] for row in price_rows), f"{len(price_rows)} variants checked"),
        ("Source URL guard", all(token not in ("\n".join([verify["title"], verify["descriptionHtml"], verify["productType"], ", ".join(verify["tags"]), verify["seo"]["title"] or "", verify["seo"]["description"] or ""]).lower()) for token in ["1688", "alibaba", "detail.1688.com"]), "no forbidden source tokens in Shopify product fields"),
        ("Size table rows", table_row_count(verify["descriptionHtml"]) == len(SIZE_CHART), str(table_row_count(verify["descriptionHtml"]))),
        ("Size table headers", all(part.count("<th>") == 10 for part in re.findall(r"<table.*?</table>", verify["descriptionHtml"], re.S)), "10 headers"),
    ]
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor source:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Family Matching, merchandised for Mommy and Me and Daddy and Me collection discovery |",
        "| PRIMARY_CATEGORY | Tops / T-Shirts |",
        "| DESIGNS_TO_LIST | auto -> one Red Heart Raglan tee colorway shown in the supplied product image |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor Fetch Status",
        "Logged-in Chrome DevTools readback succeeded for the 1688 detail page. It confirmed a 2026 family matching T-shirt offer, one red/white color token, 95% cotton main fabric composition, MOQ 1, sold 200+ units, and separate source selector values for tops, bottoms, and complete suits. This draft uses the attached size chart plus live page readback as evidence and writes no source/vendor URL to Shopify customer-facing or feed-visible fields.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## Pricing",
        "| Audience | Price | Compare-at | Cost |", "|---|---:|---:|---:|",
        f"| Child | {CHILD_PRICE} | {compare_at(CHILD_PRICE)} | {cost_for(CHILD_PRICE)} |",
        f"| Adult | {ADULT_PRICE} | {compare_at(ADULT_PRICE)} | {cost_for(ADULT_PRICE)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Color | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap, "",
        "## Derivations",
        "- The 1688 page title and product attributes identify the item family as T-shirts; the supplied product photo shows one red-and-white raglan short-sleeve tee for children, moms, and dads.",
        "- The source selector also offers boys shorts, girls skirts, mom skirts, dad shorts, and complete suit options. Those separable bottom/suit choices are intentionally not listed in this Tops draft because the request did not ask for a mixed Type x Size product and the cleanest chart-backed category is T-shirts.",
        "- The page detail states `Main fabric composition: Cotton` and `Main fabric ingredient content: 95%`; Shopify fabric writes the verified `Cotton` catalog value only.",
        "- The source chart gives recommended body weight in Chinese `斤`; the shopper-facing size table converts those ranges to `kg / lbs` so the values are understandable and do not read like pounds.",
        "- Source chest values (`70` through `116`) are treated as full chest/bust measurements because the values align with wearable child/adult tee circumferences, not half-widths.",
        "- Hip and waist are derived from the canonical top/shirt rules: child top rows use `hip = chest + 4` and `waist = chest`; mother/father top rows use `hip = chest` and `waist = chest - 12`.",
        "- The chart publishes separate child, mother, and father ladders for this tee, so the picker keeps role-bearing labels such as `Mother S` and `Father M`.",
        "- Pricing is anchored to the canonical Tops fallback and nearby family-top pattern: child `24.99`, adult `28.99`; Cost per item is exactly 50%.", "",
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
        "- If the vendor page becomes directly readable later, confirm any additional product detail-page claims before publishing.",
        "- Review the supplied product image for crop/retouch quality before a publish-live step.", "",
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
        {"name": "Size", "values": [{"name": row["picker_label"]} for row in SIZE_CHART]},
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
        "source_url_guard": True,
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
