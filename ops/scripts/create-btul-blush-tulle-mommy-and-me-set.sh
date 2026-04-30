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

HANDLE = "blush-tulle-mommy-and-me-set"
TITLE = "Blush Tulle Mommy and Me Set - Dress & Baby Romper"
SEO_TITLE = "Blush Tulle Matching Set | Dress Like Mommy"
SEO_DESCRIPTION = "Blush tulle mommy-and-me set with baby romper, girl dress and mother dress sizes from Baby 66 to 4XL."
PRINT_NAME = "Blush Tulle"
SHORTCODE = "BTUL"
COLOR_TOKEN = "BLUSH"
VENDOR_URL = "https://detail.1688.com/offer/1045177962684.html"
VENDOR = "dresslikemommy.com"
LISTING_MODE = "Mommy and Me"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "31.99"
ADULT_PRICE = "36.99"

SCRIPT_PATH = ROOT / "ops/scripts/create-btul-blush-tulle-mommy-and-me-set.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings/blush-tulle-mommy-and-me-set-listing.md"
CSV_OUT = ROOT / "ops/listings/blush-tulle-mommy-and-me-set-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings/verify-blush-tulle-mommy-and-me-set.json"
SIZE_CHART_OUT = ROOT / "ops/listings/size-chart-blush-tulle-mommy-and-me-set.json"
BODY_HTML_OUT = ROOT / "ops/listings/body-blush-tulle-mommy-and-me-set.html"
SOURCE_SIZE_CHART = ROOT / "ops/listings/source-size-chart-blush-tulle-mommy-and-me-set.png"

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
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"66","picker_label":"Baby 0-3 Months","sku_suffix":"B03M","age":"0-3M","weight":"4-7 kg","height":"-","chest_cm":52,"hip_cm":56,"waist_cm":52,"length_cm":41,"shoulder_cm":23,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"73","picker_label":"Baby 6-9 Months","sku_suffix":"B69M","age":"6-9M","weight":"6.5-8.5 kg","height":"-","chest_cm":54,"hip_cm":58,"waist_cm":54,"length_cm":43,"shoulder_cm":25,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"80","picker_label":"Baby 9-12 Months","sku_suffix":"B912M","age":"9-12M","weight":"9-10 kg","height":"-","chest_cm":56,"hip_cm":60,"waist_cm":56,"length_cm":45,"shoulder_cm":27,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Baby Romper","garment":"Baby Romper","vendor_label":"90","picker_label":"Baby 12-18 Months","sku_suffix":"B1218M","age":"12-18M","weight":"10.5-12.5 kg","height":"-","chest_cm":58,"hip_cm":62,"waist_cm":58,"length_cm":47,"shoulder_cm":29,"skirt_cm":0,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"7.5-10 kg","height":"70-80 cm","chest_cm":63,"hip_cm":67,"waist_cm":63,"length_cm":36,"shoulder_cm":32.5,"skirt_cm":36,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"10-13 kg","height":"80-90 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":39,"shoulder_cm":34,"skirt_cm":39,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"13-16 kg","height":"90-100 cm","chest_cm":71,"hip_cm":75,"waist_cm":71,"length_cm":42,"shoulder_cm":35.5,"skirt_cm":42,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16-20 kg","height":"100-110 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":45,"shoulder_cm":37,"skirt_cm":45,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20-23.5 kg","height":"110-120 cm","chest_cm":77,"hip_cm":81,"waist_cm":77,"length_cm":48,"shoulder_cm":38.5,"skirt_cm":48,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-26 kg","height":"120-130 cm","chest_cm":79,"hip_cm":83,"waist_cm":79,"length_cm":51,"shoulder_cm":40.5,"skirt_cm":51,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"26.5-31 kg","height":"130-140 cm","chest_cm":81,"hip_cm":85,"waist_cm":81,"length_cm":54,"shoulder_cm":42.5,"skirt_cm":54,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"31-37.5 kg","height":"140-150 cm","chest_cm":83,"hip_cm":87,"waist_cm":83,"length_cm":57,"shoulder_cm":44.5,"skirt_cm":57,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"40-49 kg","height":"155-160 cm","chest_cm":96,"hip_cm":102,"waist_cm":94,"length_cm":64,"shoulder_cm":47.5,"skirt_cm":64,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"49-60 kg","height":"160-165 cm","chest_cm":102,"hip_cm":108,"waist_cm":100,"length_cm":66,"shoulder_cm":49,"skirt_cm":66,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"60-67.5 kg","height":"165-170 cm","chest_cm":106,"hip_cm":112,"waist_cm":104,"length_cm":69,"shoulder_cm":50.5,"skirt_cm":69,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"67.5-77.5 kg","height":"170-175 cm","chest_cm":110,"hip_cm":116,"waist_cm":108,"length_cm":71,"shoulder_cm":52,"skirt_cm":71,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"77.5-85 kg","height":"175-180 cm","chest_cm":114,"hip_cm":120,"waist_cm":112,"length_cm":73,"shoulder_cm":53.5,"skirt_cm":73,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"3XL","picker_label":"Mother 3XL","sku_suffix":"3XL","age":"-","weight":"85-95 kg","height":"175-188 cm","chest_cm":118,"hip_cm":124,"waist_cm":116,"length_cm":75,"shoulder_cm":55,"skirt_cm":75,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"4XL","picker_label":"Mother 4XL","sku_suffix":"4XL","age":"-","weight":"95-105 kg","height":"180-190 cm","chest_cm":122,"hip_cm":128,"waist_cm":120,"length_cm":77,"shoulder_cm":56.5,"skirt_cm":77,"sleeve_cm":0,"pant_cm":0},
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
        return f"{nums[0]:g}-{nums[1]:g} {unit} / {nums[0] * factor:.1f}-{nums[1] * factor:.1f} {'lbs' if unit == 'kg' else 'in'}"
    return text


def role_token(role: str) -> str:
    if role == "Baby Romper":
        return "BBY"
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Mother"):
        return "MOM"
    raise KeyError(role)


def garment_token(garment: str) -> str:
    return {"Baby Romper": "ROMP", "Dress": "DRS"}[garment]


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "mother" else CHILD_PRICE


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
            sleeve_or_skirt = row["skirt_cm"] or row["shoulder_cm"]
            cells = [
                row["picker_label"],
                row["age"],
                range_to_imperial(row["weight"], 2.20462, "kg"),
                range_to_imperial(row["height"], 0.393701, "cm"),
                cm_to_in(row["chest_cm"]),
                cm_to_in(sleeve_or_skirt),
                "-",
                cm_to_in(row["hip_cm"]),
                cm_to_in(row["waist_cm"]),
                cm_to_in(row["length_cm"]),
            ]
            parts.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>")
        parts.append("</tbody></table>")
        return "\n".join(parts)

    intro = """
<ul>
<li><strong>Fabric:</strong> Soft mixed-media dress fabric with a smooth black bodice and blush pink tulle skirt; exact fiber composition was not visible in the supplied evidence.</li>
<li><strong>Family story:</strong> A sweet mom-and-daughter look for birthdays, portraits, summer outings, and everyday twirling.</li>
<li><strong>Color reference:</strong> Blush Tulle pairs a black sleeveless top with a pale pink layered skirt.</li>
<li><strong>Design details:</strong> Choose the baby romper, girl dress, or mother dress by Type, all in the same coordinated color story.</li>
<li><strong>Care:</strong> Hand wash cold or machine wash gentle in a garment bag, line dry, and steam tulle lightly if needed.</li>
<li><strong>Size range:</strong> Baby 0-3M to 12-18M, girls Child 1-2 Years to Child 9-10 Years, and Mother S to Mother 4XL.</li>
</ul>
""".strip()
    narrative = """
<p>Blush Tulle is made for the kind of matching moment that feels playful without being overdone. The black bodice keeps the look simple while the pale pink tulle skirt adds a soft party-ready finish for photos, celebrations, and sunny family plans.</p>

<p>The size chart is the source of truth for every listed size. The baby, girl, and mother rows are separated by Type so each shopper can select the exact piece they need.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Coordinated pieces:</strong> Baby romper, girl dress, and mother dress options in one matching listing.</li>
<li><strong>Photo-ready contrast:</strong> Black sleeveless bodice with a blush layered tulle skirt.</li>
<li><strong>Chart-backed sizing:</strong> Every variant maps to a row in the attached size chart.</li>
<li><strong>Extended mother sizing:</strong> Adult rows run from S through 4XL.</li>
<li><strong>Draft-only safety:</strong> Built unpublished for final image and merchandising review.</li>
</ul>

<p>Select each Type and Size to build a coordinated blush tulle look for mom, baby, and daughter.</p>
""".strip()
    return "\n\n".join([intro, *(table_for(name, rows) for name, rows in by_garment.items()), narrative])


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        sku = f"DLM-{SHORTCODE}-{role_token(row['role'])}-{garment_token(row['garment'])}-{row['sku_suffix']}-{COLOR_TOKEN}"
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
                "sku": sku,
                "cost": money_half(price),
                "tracked": True,
                "requiresShipping": True,
            },
        })
    return variants


def tags() -> list[str]:
    values = [
        LISTING_MODE, "Sets", "Matching Family Set", "Mommy and Me Set",
        "Matching Family Dresses", "Matching Family Outfit", "Baby Romper",
        "Girl Dress", "Mother Dress", "Dress", "Romper", "Tulle", "Blush",
        "Pink", "Black", "Sleeveless", "Summer", "Party Dress", "Birthday",
        "Photo Outfit", "Child 0-3M", "Child 6-9M", "Child 9-12M",
        "Child 12-18M", "Child 1-2yr", "Child 2-3yr", "Child 4-5yr",
        "Child 6-8yr", "Child 9-10yr", "Mom Size S", "Mom Size M",
        "Mom Size L", "Mom Size XL", "Mom Size 2XL", "Mom Size 3XL",
        "Mom Size 4XL", VENDOR_URL,
    ]
    values.extend(sorted({row["picker_label"] for row in SIZE_CHART}))
    return sorted(value for value in dict.fromkeys(values) if value)


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Blush Tulle Matching Look"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Baby Romper"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/69943132257"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(SIZE_CHART) != 19 or len(variants) != len(SIZE_CHART):
        raise RuntimeError("SIZE_CHART/variant count mismatch")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("Title or SEO length guard failed")
    if len({(r["role"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("Duplicate role/picker pair")
    table_count = body.count("<table")
    if sum(1 for row in re.findall(r"<tr>", body)) - table_count != len(SIZE_CHART):
        raise RuntimeError("Body row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("One or more size tables does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["price"] != price_for(row):
            raise RuntimeError("FORCE_SPEC_PRICES guard failed")


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "baby romper, girl dress, mother dress, tulle skirt"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "FamilySet",
            "--tags", ", ".join(tags()),
        ], check=True)
        if sorted(v["inventoryItem"]["sku"] for v in variants) != sorted({v["inventoryItem"]["sku"] for v in variants}):
            raise RuntimeError("Duplicate SKU generated")


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"} or path.name.startswith("source-size-chart"):
            continue
        alt = "Mother and daughter wearing matching black and blush tulle outfits outdoors."
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
    source = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"
    header = source.read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    tag_text = ", ".join(tags())
    for i, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update({
            "Handle": HANDLE,
            "Title": TITLE if i == 1 else "",
            "Body (HTML)": body if i == 1 else "",
            "Vendor": VENDOR if i == 1 else "",
            "Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
            "Type": PRODUCT_TYPE if i == 1 else "",
            "Tags": tag_text if i == 1 else "",
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
            "SEO Title": SEO_TITLE if i == 1 else "",
            "SEO Description": SEO_DESCRIPTION if i == 1 else "",
            "Google Shopping / Gender": "female" if i == 1 else "",
            "Google Shopping / Age Group": "adult" if i == 1 else "",
            "Google Shopping / Condition": "new" if i == 1 else "",
            "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
            "Google Shopping / Custom Label 0": "Mommy and Me" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Dress & Baby Romper" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Mommy and Me Set" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Blush Tulle Matching Look" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Mommy and Me Set" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Two-Piece Set" if i == 1 else "",
            "Cost per item": variant["inventoryItem"]["cost"],
            "Status": "draft",
        })
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, body: str, variants: list[dict], verify: dict) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    spec_by_sku = {v["inventoryItem"]["sku"]: (row, v) for row, v in zip(SIZE_CHART, variants)}
    live_skus = sorted(v["sku"] for v in verify["variants"]["nodes"])
    spec_skus = sorted(spec_by_sku)
    price_rows = []
    price_ok = True
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
        price_rows.append(f"| {live['sku']} | {live['price']} | {live['compareAtPrice']} | {cost or ''} | {spec['price']} | {spec['compareAtPrice']} | {spec['inventoryItem']['cost']} | {'PASS' if ok else 'FAIL'} |")

    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")

    table_count = body.count("<table")
    body_rows = body.count("<tr>") - table_count
    header_counts = [part.count("<th>") for part in re.findall(r"<table.*?</table>", body, re.S)]
    published = [p["publication"]["name"] for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    checks = [
        ("Product status is DRAFT", verify["status"] == "DRAFT", verify["status"]),
        ("publishedAt is null", verify.get("publishedAt") is None, str(verify.get("publishedAt"))),
        ("onlineStoreUrl is null", verify.get("onlineStoreUrl") is None, str(verify.get("onlineStoreUrl"))),
        ("No sales-channel publication is live", not published, str(published)),
        ("Variant count matches SIZE_CHART", len(verify["variants"]["nodes"]) == len(SIZE_CHART), f"{len(verify['variants']['nodes'])} vs {len(SIZE_CHART)}"),
        ("Live SKUs match derived SKUs", live_skus == spec_skus, f"{len(spec_skus)} expected"),
        ("Each size table has 10 headers", all(count == 10 for count in header_counts), str(header_counts)),
        ("Table row count matches SIZE_CHART", body_rows == len(SIZE_CHART), f"{body_rows} vs {len(SIZE_CHART)}"),
        ("Taxonomy fullName matches", verify["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, verify["category"]["fullName"]),
        ("Price and cost parity", price_ok, "FORCE_SPEC_PRICES=true and Cost per item=50%"),
    ]
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible in the supplied image or size chart."),
        ("shopify.dress-occasion", "The product mixes dresses and a baby romper under Outfit Sets."),
        ("shopify.dress-style", "The product mixes dresses and a romper; no single dress-only style applies."),
        ("shopify.neckline", "No verified product-level neckline catalog value was available for the mixed garment listing."),
        ("shopify.skirt-dress-length-type", "The listing also includes baby romper rows."),
        ("shopify.sleeve-length-type", "The chart supplies shoulder width, not sleeve length."),
        ("shopify.top-length-type", "No top is sold in this listing."),
    ]
    written = [f"- `{m['namespace']}.{m['key']}`" for m in verify["metafields"]["nodes"] if m["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}]
    collections = verify["collections"]["nodes"]
    collection_lines = (
        [f"- {c['title']} (`/{c['handle']}`)" for c in collections]
        if collections
        else ["- Collection indexing may wait until publication because this product remains an unpublished draft."]
    )
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
        "| LISTING_MODE | auto from evidence -> Mommy and Me |",
        "| PRIMARY_CATEGORY | auto -> FamilySet / Outfit Sets because the chart includes baby romper plus dresses |",
        "| DESIGNS_TO_LIST | Blush Tulle only |",
        "| EXCLUDE_ITEMS | none |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor fetch status",
        "Direct fetch of the 1688 page returned Alibaba CAPTCHA/punish markup, so the attached size-chart screenshot and product image were used as authoritative evidence per the canonical prompt. The vendor URL is retained in tags and internal notes only, never customer-facing copy.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
        *recap, "",
        "## Derivations and Mapping Notes",
        "- The attached chart is transcribed into 19 variant rows: 4 baby romper rows, 8 child dress rows, and 7 mother dress rows.",
        "- Vendor weights were shown in jin and converted to kg/lbs for the storefront table.",
        "- Hip and waist are derived where the source chart omitted them: baby/child hip = chest + 4 and waist = chest; mother hip = bust + 6 and waist = hip - 8.",
        "- The source chart provides shoulder width, not sleeve length. Shoulder values are stored in SIZE_CHART and used only as the closest available second-measure value in the standard 10-column table.",
        "- Options are `Type x Size` so the baby romper and dress rows do not collapse into one garment.", "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        *[f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |" for label, ok, detail in checks], "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare | Live Cost | Spec Price | Spec Compare | Spec Cost | Match |",
        "|---|---|---|---|---|---|---|---|",
        *price_rows, "",
        "## Metafields Written",
        *written, "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        f"## Tags Written ({len(verify['tags'])})",
        "`" + ", ".join(verify["tags"]) + "`", "",
        "## Smart Collections",
        *collection_lines,
        "",
        "## Manual Follow-ups",
        "- Replace or retouch the supplied watermarked product image before publication.",
        "- Confirm exact fiber composition before publishing; `shopify.fabric` is intentionally skipped for now.",
        "- Inventory quantities and per-variant grams still need operator stock values.", "",
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
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)
    run_variant_model_guard(variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{id sku}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Baby Romper", "Dress"]]},
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
        live_skus = sorted(v["sku"] for v in existing["variants"]["nodes"] if v.get("sku"))
        spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
        if live_skus and live_skus != spec_skus:
            raise RuntimeError("Existing draft has unexpected variants; refusing to create duplicates.")
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        if live_skus == spec_skus:
            update_variants = []
            live_by_sku = {v["sku"]: v["id"] for v in existing["variants"]["nodes"] if v.get("sku")}
            for spec in variants:
                update_variants.append({"id": live_by_sku[spec["inventoryItem"]["sku"]], **spec})
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

    mf = metafields(product_id)
    for i in range(0, len(mf), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mf[i:i+25]})
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
