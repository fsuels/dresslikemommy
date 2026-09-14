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

HANDLE = "playful-cat-parade-family-matching-tops"
TITLE = "Playful Cat Parade Family Matching Tops — Button-Up Shirt"
SEO_TITLE = "Playful Cat Parade Family Shirts | Dress Like Mommy"
PRINT_NAME = "Playful Cat Parade"
SHORTCODE = "PCAT"
COLOR_TOKEN = "CATPRD"
COLOR_NAME = "Playful Cat Parade"
VENDOR = "dresslikemommy.com"
VENDOR_URL = ""
PRODUCT_TYPE = "Matching Family Tops"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-7-2"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Clothing Tops > Shirts > Dress Shirts"
CHILD_PRICE = "24.99"
ADULT_PRICE = "27.99"
FORCE_SPEC_PRICES = True
PRICE_NEIGHBOR_HANDLE = "blue-stripe-family-matching-shirts"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-pcat-playful-cat-parade-family-matching-tops.sh"
SOURCE_SIZE_CHART = ROOT / "ops/listings/source-size-chart-family-matching-casual-shirts.png"
PRODUCT_IMAGE = UPLOAD_DIR / "01-playful-cat-parade-shirt.png"

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
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"12.5-20 kg","height":"95-110 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"15-25 kg","height":"110-120 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"20-27.5 kg","height":"120-130 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25-32.5 kg","height":"130-138 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30-35 kg","height":"138-145 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"160","picker_label":"Child 12 Years","sku_suffix":"KID12Y","age":"11-12","weight":"32.5-40 kg","height":"145-150 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"child","role":"Child Shirt","garment":"Shirt","vendor_label":"170","picker_label":"Child 14 Years","sku_suffix":"KID170","age":"14","weight":"35-42.5 kg","height":"150-155 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Adult M","sku_suffix":"M","age":"—","weight":"42.5-52.5 kg","height":"155-165 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Adult L","sku_suffix":"L","age":"—","weight":"52.5-60 kg","height":"165-175 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Adult XL","sku_suffix":"XL","age":"—","weight":"60-65 kg","height":"165-178 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"2XL","picker_label":"Adult 2XL","sku_suffix":"2XL","age":"—","weight":"65-72.5 kg","height":"168-180 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Adult 3XL","sku_suffix":"3XL","age":"—","weight":"72.5-82.5 kg","height":"170-180 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"4XL","picker_label":"Adult 4XL","sku_suffix":"4XL","age":"—","weight":"82.5-90 kg","height":"170-182 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
    {"audience":"adult","role":"Adult Shirt","garment":"Shirt","vendor_label":"5XL","picker_label":"Adult 5XL","sku_suffix":"5XL","age":"—","weight":"90-100 kg","height":"170-185 cm","chest_cm":"—","hip_cm":"—","waist_cm":"—","length_cm":"—","sleeve_cm":"—","pant_cm":"—"},
]

CHILD_ROWS = [row for row in SIZE_CHART if row["audience"] == "child"]
ADULT_ROWS = [row for row in SIZE_CHART if row["audience"] == "adult"]
SEO_SIZE_PHRASE = (
    f"Child {CHILD_ROWS[0]['age']}–{CHILD_ROWS[-1]['age']} Years "
    f"and Adult {ADULT_ROWS[0]['vendor_label']}–{ADULT_ROWS[-1]['vendor_label']}"
)
SEO_DESCRIPTION = (
    "Playful Cat Parade shirts for mom, dad, girls & boys in lightweight "
    f"woven-look fabric, sizes {SEO_SIZE_PHRASE}."
)
SIZE_RANGE_COPY = (
    f"{CHILD_ROWS[0]['picker_label']} through {CHILD_ROWS[-1]['picker_label']} "
    f"and {ADULT_ROWS[0]['picker_label']} through {ADULT_ROWS[-1]['picker_label']}"
)
EXPECTED_UNMAPPED_SIZE_LABELS = {"Child 14 Years", "Adult 5XL"}
COLOR_PATTERN_GIDS = [
    "gid://shopify/Metaobject/69943132257",  # Pink
    "gid://shopify/Metaobject/69639766113",  # Blue
    "gid://shopify/Metaobject/69639733345",  # White
    "gid://shopify/Metaobject/69641928801",  # Beige/Cream
    "gid://shopify/Metaobject/130231140449",  # Multicolor
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
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def fmt_num(value) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:.1f}".rstrip("0").rstrip(".")


def metric_range(text: str, unit: str) -> str:
    raw = str(text or "").strip()
    if not raw or raw in {"-", "—", "--"}:
        return "—"
    return raw.replace(f" {unit}", "")


def measurement(value) -> str:
    if value in (None, "", 0, "0", "-", "—", "--"):
        return "—"
    return fmt_num(value)


def role_token(role: str) -> str:
    if role == "Child Shirt":
        return "KID"
    if role == "Adult Shirt":
        return "ADT"
    raise KeyError(role)


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "adult" else CHILD_PRICE


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


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
    rendered = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            row["age"],
            metric_range(row["weight"], "kg"),
            metric_range(row["height"], "cm"),
            measurement(row["chest_cm"]),
            measurement(row["sleeve_cm"]),
            measurement(row["pant_cm"]),
            measurement(row["hip_cm"]),
            measurement(row["waist_cm"]),
            measurement(row["length_cm"]),
        ]
        rendered.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")
    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven-look fabric; exact fiber composition was not available in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> One coordinated short-sleeve shirt for children and adults, ready for family photos, vacations, celebrations, and relaxed warm-weather plans.</li>",
        "<li><strong>Print reference:</strong> Playful Cat Parade fills a soft pastel ground with a lively crowd of cartoon cats in pink, blue, cream, brown, gray, white, and red accents.</li>",
        "<li><strong>Design details:</strong> Collared neckline, button-up front, short sleeves, and one shared all-over cat print across child and adult sizes.</li>",
        "<li><strong>Care:</strong> Follow the garment care label. Exact washing instructions were not available in the supplied evidence.</li>",
        f"<li><strong>Size range:</strong> {SIZE_RANGE_COPY}.</li>",
        "</ul>",
        "<h3>Button-Up Shirt Size Chart</h3>",
        "<table id=\"size-chart\">",
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *rendered,
        "</tbody></table>",
        "<p>Playful Cat Parade brings a cheerful, storybook-like mood to family matching with a layered crowd of expressive cartoon cats in soft pink, sky blue, cream, brown, gray, white, and small red accents. The collared button-up silhouette keeps the playful print polished enough for coordinated outings, celebrations, and family photos.</p>",
        "<p>The supplied chart provides recommended body height and weight only; chest, sleeve, pant or short, hip, waist, and garment-length measurements are unavailable and remain marked as such. It publishes one shared child-and-adult size ladder rather than separate girl, boy, mom, and dad measurements, so the picker uses honest Child and Adult labels without inventing role-specific variants.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>One coordinated shirt:</strong> The same collared short-sleeve button-up look is offered across child and adult sizes.</li>",
        "<li><strong>Playful cat print:</strong> A varied crowd of cartoon cats gives every shirt a bright, whimsical family-photo look.</li>",
        "<li><strong>Easy warm-weather styling:</strong> The relaxed short-sleeve button-up shape works as a standalone top for casual plans.</li>",
        "<li><strong>Wide size ladder:</strong> Seven child rows and seven adult rows are preserved from the supplied chart.</li>",
        "<li><strong>Chart-backed variants:</strong> Every selectable size corresponds to one supplied chart row, with unavailable measurements left unguessed.</li>",
        "</ul>",
        "<p>Choose the child and adult sizes you need to create a coordinated Playful Cat Parade look for the next sunny family memory.</p>",
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
        "Matching Family Shirt",
        "Matching Family Shirts",
        "Matching Family Outfits",
        "Child Shirt",
        "Adult Shirt",
        "Button-Up Shirt",
        "Collared Shirt",
        "Short Sleeve Shirt",
        "Playful Cat Parade",
        "Cat Parade",
        "Cartoon Cat Print",
        "Playful Cat Print",
        "Animal Print",
        "Whimsical Print",
        "Pastel",
        "Multicolor",
        "Pink",
        "Blue",
        "White",
        "Cream",
        "Brown",
        "Gray",
        "Red",
        "Spring",
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
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Family Matching Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Playful Cat Button-Up Shirt"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Spring/Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Short Sleeve Button-Up Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Unisex Family Shirt"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(COLOR_PATTERN_GIDS)},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972502625"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def table_first_cells(body: str) -> list[str]:
    tbody = re.search(r"<tbody>(.*?)</tbody>", body, re.S)
    if not tbody:
        return []
    return [
        html.unescape(re.sub(r"<[^>]+>", "", match)).strip()
        for match in re.findall(r"<tr>\s*<td>(.*?)</td>", tbody.group(1), re.S)
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {
        "audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix",
        "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm",
        "length_cm", "sleeve_cm", "pant_cm",
    }
    if len(SIZE_CHART) != 14 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        if row["garment"] != "Shirt" or row["role"] not in {"Child Shirt", "Adult Shirt"}:
            errors.append(f"unsupported role/garment mapping for {row.get('vendor_label')}")
        if not str(row["weight"]).endswith(" kg") or not str(row["height"]).endswith(" cm"):
            errors.append(f"{row.get('vendor_label')} is missing metric height/weight units")
        for field in ("chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "pant_cm"):
            if row[field] != "—":
                errors.append(f"{row.get('vendor_label')} {field} must remain unavailable")
    unmapped_labels = {row["picker_label"] for row in SIZE_CHART if row["picker_label"] not in SIZE_MAP}
    if unmapped_labels != EXPECTED_UNMAPPED_SIZE_LABELS:
        errors.append(f"unexpected shopify.size gaps: {sorted(unmapped_labels)}")
    if len({SIZE_MAP[label][0] for label in SIZE_MAP}) != len(SIZE_MAP):
        errors.append("duplicate shopify.size GID")
    if [row["vendor_label"] for row in SIZE_CHART] != [
        "110", "120", "130", "140", "150", "160", "170",
        "M", "L", "XL", "2XL", "3XL", "4XL", "5XL",
    ]:
        errors.append("SIZE_CHART vendor row order changed")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label) pair")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"seo title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"seo description too long: {len(SEO_DESCRIPTION)}")
    if TITLE == SEO_TITLE:
        errors.append("SEO title must differ from product title")
    if VENDOR_URL:
        errors.append("vendor_url must remain empty")
    if SEO_SIZE_PHRASE not in SEO_DESCRIPTION:
        errors.append("SEO size phrase is not derived into the description")
    if table_row_count(body) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    tables = re.findall(r"<table.*?</table>", body, re.S)
    if len(tables) != 1 or tables[0].count("<th>") != 10:
        errors.append("body must contain one 10-column size table")
    if table_first_cells(body) != [row["picker_label"] for row in SIZE_CHART]:
        errors.append("size-table picker labels do not match SIZE_CHART")
    opening_list = body.split("</ul>", 1)[0]
    if opening_list.count("<li>") != 6:
        errors.append("opening product summary must contain exactly six bullets")
    for row, variant in zip(SIZE_CHART, variants):
        if not FORCE_SPEC_PRICES or variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("cost is not 50 percent of price")
        if not variant["inventoryItem"]["sku"].startswith("DLM-PCAT-"):
            errors.append("SKU prefix is not DLM-PCAT")
    if len({variant["inventoryItem"]["sku"] for variant in variants}) != 14:
        errors.append("derived SKUs are not unique")
    shopper_payload = "\n".join([TITLE, SEO_TITLE, SEO_DESCRIPTION, body, PRODUCT_TYPE, ", ".join(tags())]).lower()
    if re.search(r"(?:https?://|www\.)", shopper_payload):
        errors.append("URL-shaped source reference leaked into shopper/feed fields")
    if not SOURCE_SIZE_CHART.is_file():
        errors.append(f"missing authoritative size-chart image: {SOURCE_SIZE_CHART}")
    if not PRODUCT_IMAGE.is_file():
        errors.append(f"missing owned product image: {PRODUCT_IMAGE}")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "listing-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Size", "Color"], "variants": variants}), encoding="utf-8")
        evidence.write_text(
            json.dumps(
                {
                    "raw_detail_text": (
                        "family matching short sleeve casual collared button-up shirt; "
                        "one purchasable shirt only; no bundled bottoms are evidenced"
                    )
                }
            ),
            encoding="utf-8",
        )
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "Tops",
            "--tags", ", ".join(tags()),
        ], check=True)


def upload_media(product_id: str) -> None:
    if not PRODUCT_IMAGE.is_file():
        raise RuntimeError(f"Owned product image is missing: {PRODUCT_IMAGE}")
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    path = PRODUCT_IMAGE
    alt = "Playful Cat Parade short-sleeve button-up shirt with a pastel multicolor cartoon-cat crowd print."
    if alt in existing_alts:
        return
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    staged = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""", {
        "input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]
    })
    require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----DLMPCATMEDIA"
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
    header_source = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"
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
            "Google Shopping / Custom Label 3": "Short Sleeve Button-Up Shirt" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Unisex Family Shirt" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Playful Cat Button-Up Shirt" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Tops" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Family Matching Tops" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Shirt" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
            "Age group (product.metafields.shopify.age-group)": "kids, adults" if i == 1 else "",
            "Color (product.metafields.shopify.color-pattern)": "Pink, Blue, White, Beige, Multicolor" if i == 1 else "",
            "Size (product.metafields.shopify.size)": ", ".join(
                SIZE_MAP[item["picker_label"]][1]
                for item in SIZE_CHART
                if item["picker_label"] in SIZE_MAP
            ) if i == 1 else "",
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
    if product.get("publishedAt") is not None:
        errors.append(f"publishedAt is {product['publishedAt']}, expected null")
    if product.get("onlineStoreUrl") is not None:
        errors.append(f"onlineStoreUrl is {product['onlineStoreUrl']}, expected null")
    live_publications = [node for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    if live_publications:
        errors.append("one or more sales-channel publications is live")
    if product.get("handle") != HANDLE or product.get("title") != TITLE:
        errors.append("live handle/title does not match the listing spec")
    if product.get("productType") != PRODUCT_TYPE:
        errors.append(f"productType is {product.get('productType')}")
    if product.get("seo", {}).get("title") != SEO_TITLE or product.get("seo", {}).get("description") != SEO_DESCRIPTION:
        errors.append("live SEO fields do not match the listing spec")
    category = product.get("category") or {}
    if category.get("id") != TAXONOMY_GID or category.get("fullName") != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {category}")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    live_skus = sorted(node["sku"] for node in live_variants)
    spec_skus = sorted(spec_by_sku)
    if live_skus != spec_skus:
        errors.append("live SKUs do not match derived SKUs")
    if table_row_count(product["descriptionHtml"]) != len(SIZE_CHART):
        errors.append("size table row count does not match SIZE_CHART")
    live_tables = re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)
    if len(live_tables) != 1 or live_tables[0].count("<th>") != 10:
        errors.append("live body does not have one 10-column size table")
    if table_first_cells(product["descriptionHtml"]) != [row["picker_label"] for row in SIZE_CHART]:
        errors.append("live size-table picker labels do not match SIZE_CHART")
    if [option["name"] for option in product["options"]] != ["Size", "Color"]:
        errors.append("option axes are not Size / Color")
    expected_pairs = {(row["picker_label"], COLOR_NAME) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Size x Color option combinations do not match")
    payload = "\n".join([product["title"], product["descriptionHtml"], product["productType"], ", ".join(product["tags"]), product["seo"]["title"] or "", product["seo"]["description"] or ""]).lower()
    if re.search(r"(?:https?://|www\.)", payload):
        errors.append("URL-shaped source reference leaked into Shopify product data")
    if not set(tags()).issubset(set(product["tags"])):
        errors.append("one or more derived tags is missing")
    for node in live_variants:
        spec = spec_by_sku.get(node["sku"])
        unit_cost = ((node.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        cost_ok = (
            spec is not None
            and unit_cost is not None
            and Decimal(unit_cost) == Decimal(spec["inventoryItem"]["cost"])
        )
        match = (
            spec is not None
            and node["price"] == spec["price"]
            and node["compareAtPrice"] == spec["compareAtPrice"]
            and node["inventoryPolicy"] == "DENY"
            and node["taxable"] is True
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
            "spec_price": spec["price"] if spec else "missing",
            "spec_compare_at": spec["compareAtPrice"] if spec else "missing",
            "spec_cost": spec["inventoryItem"]["cost"] if spec else "missing",
            "match": match,
        })
    expected_metafields = {
        "custom.category1", "custom.subcategory", "custom.subcategory2", "custom.pattern",
        "custom.style", "custom.type", "mm-google-shopping.custom_product",
        "mm-google-shopping.gender", "mm-google-shopping.age_group", "mm-google-shopping.condition",
        "mm-google-shopping.custom_label_0", "mm-google-shopping.custom_label_1",
        "mm-google-shopping.custom_label_2", "mm-google-shopping.custom_label_3",
        "mm-google-shopping.custom_label_4", "shopify.age-group", "shopify.color-pattern",
        "shopify.size", "shopify.target-gender", "global.title_tag",
        "global.description_tag",
    }
    metafield_by_key = {
        f"{node['namespace']}.{node['key']}": node
        for node in product["metafields"]["nodes"]
    }
    written_metafields = set(metafield_by_key)
    missing = sorted(expected_metafields - written_metafields)
    if missing:
        errors.append("missing expected metafields: " + ", ".join(missing))
    expected_size_refs = list(
        dict.fromkeys(
            SIZE_MAP[row["picker_label"]][0]
            for row in SIZE_CHART
            if row["picker_label"] in SIZE_MAP
        )
    )
    size_metafield = metafield_by_key.get("shopify.size")
    if size_metafield and json.loads(size_metafield["value"]) != expected_size_refs:
        errors.append("shopify.size references do not match the 12 honest catalog mappings")
    if "shopify.fabric" in written_metafields:
        errors.append("shopify.fabric must be skipped because exact fiber evidence is unavailable")
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        size_match = SIZE_MAP.get(row["picker_label"])
        gid_text = f"`{size_match[0]}` ({size_match[1]})" if size_match else "— (no compatible standard size metaobject)"
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | "
            f"{COLOR_NAME} | `{variant['inventoryItem']['sku']}` | {variant['price']} | "
            f"{variant['inventoryItem']['cost']} | {gid_text} |"
        )
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    skipped = [
        ("shopify.fabric", "Exact fiber composition is absent, so no fabric metaobject is written; shopper copy stays at lightweight woven-look fabric."),
        ("shopify.sleeve-length-type", "Short sleeves are visible, but no owner-subtype-safe catalog value was verified for this Shirts taxonomy run."),
        ("shopify.neckline", "The garment has a shirt collar, and no owner-subtype-safe neckline value was verified for this Shirts taxonomy run."),
        ("shopify.top-length-type", "The supplied chart does not provide garment length, so no standard top-length type can be supported."),
        ("shopify.size Child 14 Years", "The vendor 170 row maps to Child 14 Years; no compatible standard size metaobject is currently available."),
        ("shopify.size Adult 5XL", "The 5XL row is preserved as a variant, but no compatible standard size metaobject is available."),
        ("shopify.color-pattern Brown/Gray/Red", "Brown, gray, and red accents remain in copy and tags; only verified Pink, Blue, White, Beige, and Multicolor catalog references are written."),
        ("shopify.dress-occasion", "Not applicable because the honest taxonomy is Shirts."),
        ("shopify.dress-style", "Not applicable because this is a Tops listing."),
        ("shopify.skirt-dress-length-type", "Not applicable because this listing contains shirts only."),
    ]
    live_publications = [p for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    smart_collections = verify["collections"]["nodes"] or []
    smart_lines = [f"- {item['title']} (`/{item['handle']}`)" for item in smart_collections] or ["- None returned immediately; draft products may not index into smart collections until publication."]
    customer_payload = "\n".join([
        verify["title"], verify["descriptionHtml"], verify["productType"],
        ", ".join(verify["tags"]), verify["seo"]["title"] or "",
        verify["seo"]["description"] or "",
    ]).lower()
    verification_rows = [
        ("Product status is DRAFT", verify["status"] == "DRAFT", verify["status"]),
        ("publishedAt is null", verify.get("publishedAt") is None, str(verify.get("publishedAt"))),
        ("No sales-channel publications", not live_publications, str([p["publication"]["name"] for p in live_publications])),
        ("Taxonomy fullName matches", verify["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, verify["category"]["fullName"]),
        ("Variant count matches SIZE_CHART", len(verify["variants"]["nodes"]) == len(SIZE_CHART), f"{len(verify['variants']['nodes'])} vs {len(SIZE_CHART)}"),
        ("Price and cost parity", all(row["match"] for row in price_rows), f"{len(price_rows)} variants checked"),
        ("Source-reference guard", not re.search(r"(?:https?://|www\.)", customer_payload), "no URL-shaped source reference in Shopify product fields"),
        ("Size table rows", table_row_count(verify["descriptionHtml"]) == len(SIZE_CHART), str(table_row_count(verify["descriptionHtml"]))),
        ("Size table headers", len(re.findall(r"<table.*?</table>", verify["descriptionHtml"], re.S)) == 1 and verify["descriptionHtml"].count("<th>") == 10, "10 headers"),
        ("Picker labels", table_first_cells(verify["descriptionHtml"]) == [row["picker_label"] for row in SIZE_CHART], "exact SIZE_CHART order"),
    ]
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        "| Evidence | supplied product image and shared authoritative size-chart image |",
        "| LISTING_MODE | Family Matching, merchandised for Mommy and Me and Daddy and Me collection discovery |",
        "| PRIMARY_CATEGORY | Tops / Shirts |",
        "| DESIGNS_TO_LIST | one Playful Cat Parade short-sleeve button-up shirt |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Evidence Status",
        "The supplied product image and shared size-chart image are the authoritative evidence for this draft. No supplier identifier or source link is stored in the runner, generated notes, or Shopify fields.", "",
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
        "- The supplied product image supports one unisex collared, short-sleeve button-up shirt with an all-over crowd of playful cartoon cats in pastel pink, blue, cream, brown, gray, white, and red accents. No licensed character or brand identity is claimed.",
        "- Exact fiber composition is unavailable. Body copy therefore uses only `lightweight woven-look fabric`, and `shopify.fabric` is intentionally skipped.",
        "- The chart publishes recommended body height and weight only. Chest, sleeve, pant or short, hip, waist, and garment length remain `—`; none are inferred.",
        "- Weight ranges were converted from jin to kg by dividing by two, preserving every published range endpoint.",
        "- The one child/adult ladder is kept as seven Child rows and seven Adult rows. Vendor size code 170 maps to Child 14 Years using the row's 150-155 cm recommendation and the store's established age-label progression.",
        "- Child 14 Years and Adult 5XL remain real variants but are omitted from `shopify.size` because no compatible standard size metaobject is currently available.",
        f"- Fresh nearby-handle precedent `{PRICE_NEIGHBOR_HANDLE}` sets child `24.99` and adult `27.99`; Cost per item is exactly 50%.", "",
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
        "- Confirm exact fiber composition and garment care instructions if new authoritative evidence becomes available.",
        "- Review the supplied product image for crop/retouch quality before a publish-live step.", "",
        "## Files saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SOURCE_SIZE_CHART}`",
        f"- `{PRODUCT_IMAGE}`",
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
    if (
        tax.get("__typename") != "TaxonomyCategory"
        or tax.get("id") != TAXONOMY_GID
        or tax.get("fullName") != EXPECTED_TAXONOMY_FULL_NAME
        or tax.get("isLeaf") is not True
    ):
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

    existing = gql(
        """query($handle:String!){
          productByHandle(handle:$handle){
            id status publishedAt onlineStoreUrl
            options{name values}
            variants(first:100){nodes{id sku selectedOptions{name value}}}
            resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}}
          }
        }""",
        {"handle": HANDLE},
    )["data"]["productByHandle"]
    if existing:
        live_publications = [
            node
            for node in existing["resourcePublicationsV2"]["nodes"]
            if node["isPublished"]
        ]
        if (
            existing["status"] != "DRAFT"
            or existing.get("publishedAt") is not None
            or existing.get("onlineStoreUrl") is not None
            or live_publications
        ):
            raise RuntimeError(
                "Existing product is not a clean unpublished draft; refusing any mutation."
            )
        product_id = existing["id"]
        live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
        spec_skus = {variant["inventoryItem"]["sku"] for variant in variants}
        expected_pairs = {
            (row["picker_label"], COLOR_NAME)
            for row in SIZE_CHART
        }
        live_pairs = {
            tuple(option["value"] for option in node["selectedOptions"])
            for node in existing["variants"]["nodes"]
        }
        if (
            set(live_by_sku) != spec_skus
            or live_pairs != expected_pairs
            or [option["name"] for option in existing["options"]] != ["Size", "Color"]
        ):
            raise RuntimeError("Existing draft has unexpected variants; refusing to create/delete variants automatically.")
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
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
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle productType status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy taxable selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
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
        "source_reference_guard": True,
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
/usr/bin/python3 "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" --handles "playful-cat-parade-family-matching-tops"
