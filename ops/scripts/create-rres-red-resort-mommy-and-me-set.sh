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

HANDLE = "red-resort-mommy-and-me-set"
TITLE = "Red Resort Mommy and Me Set - Tee and Skirt"
SEO_TITLE = "Red Mommy and Me Outfit | Dress Like Mommy"
SEO_DESCRIPTION = "Red mom and daughter two-piece set with short-sleeve tops and white skirts. Sizes Child 4Y-10Y and Mother S-2XL."
PRINT_NAME = "Red Resort"
SHORTCODE = "RRES"
COLOR_TOKEN = "REDWHT"
COLOR_NAME = "Red and White"
VENDOR_URL = "https://detail.1688.com/offer/1042663719852.html"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-rres-red-resort-mommy-and-me-set.sh"
EXPECTED_STATUS = "DRAFT"
EXPECT_PUBLISHED_NULL = True
ALLOW_LIVE_PUBLICATIONS = False

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
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Girl Set","garment":"Two-Piece Set","vendor_label":"Set 110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"25-30 jin","height":"95-105 cm","source_chest_width_cm":36.5,"chest_cm":73,"shoulder_cm":34,"sleeve_cm":11,"skirt_cm":29.5,"hip_cm":0,"waist_cm":46,"length_cm":44,"pant_cm":0,"top_length_cm":44,"top_waist_cm":73,"skirt_waist_cm":46,"skirt_source_height":"106-115 cm","waistband_height_cm":3.5},
    {"audience":"child","role":"Girl Set","garment":"Two-Piece Set","vendor_label":"Set 120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"30-35 jin","height":"105-115 cm","source_chest_width_cm":39.5,"chest_cm":79,"shoulder_cm":37,"sleeve_cm":12,"skirt_cm":31,"hip_cm":0,"waist_cm":49,"length_cm":47,"pant_cm":0,"top_length_cm":47,"top_waist_cm":79,"skirt_waist_cm":49,"skirt_source_height":"116-125 cm","waistband_height_cm":3.5},
    {"audience":"child","role":"Girl Set","garment":"Two-Piece Set","vendor_label":"Set 130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"35-40 jin","height":"115-125 cm","source_chest_width_cm":40.5,"chest_cm":81,"shoulder_cm":38,"sleeve_cm":13,"skirt_cm":32.5,"hip_cm":0,"waist_cm":52,"length_cm":49,"pant_cm":0,"top_length_cm":49,"top_waist_cm":81,"skirt_waist_cm":52,"skirt_source_height":"126-135 cm","waistband_height_cm":3.5},
    {"audience":"child","role":"Girl Set","garment":"Two-Piece Set","vendor_label":"Set 140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"45-55 jin","height":"125-135 cm","source_chest_width_cm":43.5,"chest_cm":87,"shoulder_cm":41,"sleeve_cm":14,"skirt_cm":34,"hip_cm":0,"waist_cm":55,"length_cm":54,"pant_cm":0,"top_length_cm":54,"top_waist_cm":87,"skirt_waist_cm":55,"skirt_source_height":"136-145 cm","waistband_height_cm":3.5},
    {"audience":"child","role":"Girl Set","garment":"Two-Piece Set","vendor_label":"Set 150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"55-65 jin","height":"135-145 cm","source_chest_width_cm":45,"chest_cm":90,"shoulder_cm":42,"sleeve_cm":15,"skirt_cm":35.5,"hip_cm":0,"waist_cm":58,"length_cm":57,"pant_cm":0,"top_length_cm":57,"top_waist_cm":90,"skirt_waist_cm":58,"skirt_source_height":"145-155 cm","waistband_height_cm":3.5},
    {"audience":"mother","role":"Mother Set","garment":"Two-Piece Set","vendor_label":"Set S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"75-90 jin","height":"145-155 cm","source_chest_width_cm":48,"chest_cm":96,"shoulder_cm":40,"sleeve_cm":19.5,"skirt_cm":0,"hip_cm":0,"waist_cm":0,"length_cm":63,"pant_cm":0,"top_length_cm":63,"top_waist_cm":84,"skirt_waist_cm":0,"skirt_source_height":"-","waistband_height_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Two-Piece Set","vendor_label":"Set M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"90-105 jin","height":"160-165 cm","source_chest_width_cm":50,"chest_cm":100,"shoulder_cm":41,"sleeve_cm":20,"skirt_cm":0,"hip_cm":0,"waist_cm":0,"length_cm":64,"pant_cm":0,"top_length_cm":64,"top_waist_cm":88,"skirt_waist_cm":0,"skirt_source_height":"-","waistband_height_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Two-Piece Set","vendor_label":"Set L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"105-115 jin","height":"165-170 cm","source_chest_width_cm":52,"chest_cm":104,"shoulder_cm":43,"sleeve_cm":21,"skirt_cm":0,"hip_cm":0,"waist_cm":0,"length_cm":67,"pant_cm":0,"top_length_cm":67,"top_waist_cm":92,"skirt_waist_cm":0,"skirt_source_height":"-","waistband_height_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Two-Piece Set","vendor_label":"Set XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"115-130 jin","height":"170-175 cm","source_chest_width_cm":54,"chest_cm":108,"shoulder_cm":44,"sleeve_cm":21,"skirt_cm":0,"hip_cm":0,"waist_cm":0,"length_cm":68,"pant_cm":0,"top_length_cm":68,"top_waist_cm":96,"skirt_waist_cm":0,"skirt_source_height":"-","waistband_height_cm":0},
    {"audience":"mother","role":"Mother Set","garment":"Two-Piece Set","vendor_label":"Set 2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"130-145 jin","height":"175-180 cm","source_chest_width_cm":56,"chest_cm":112,"shoulder_cm":46,"sleeve_cm":21.5,"skirt_cm":0,"hip_cm":0,"waist_cm":0,"length_cm":70,"pant_cm":0,"top_length_cm":70,"top_waist_cm":100,"skirt_waist_cm":0,"skirt_source_height":"-","waistband_height_cm":0},
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


def cm(value) -> str:
    if value in (None, "", 0, "0", "-"):
        return "-"
    return fmt_num(value)


def source_range(text: str, unit: str) -> str:
    raw = str(text or "").strip()
    if not raw or raw == "-":
        return "-"
    return raw.replace(f" {unit}", "")


def display_jin_weight(text: str) -> str:
    raw = str(text or "").strip().replace(" ", "")
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)-([0-9]+(?:\.[0-9]+)?)jin", raw, re.I)
    if not match:
        return "-" if raw in {"", "-"} else raw.replace("jin", "").replace("斤", "")
    low_jin = float(match.group(1))
    high_jin = float(match.group(2))
    low_kg = low_jin * 0.5
    high_kg = high_jin * 0.5
    low_lb = round(low_jin * 1.10231131)
    high_lb = round(high_jin * 1.10231131)
    return f"{fmt_num(low_kg)}-{fmt_num(high_kg)} kg / {low_lb}-{high_lb} lbs"


def role_token(role: str) -> str:
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Mother"):
        return "MOM"
    raise KeyError(role)


def type_token(garment: str) -> str:
    return {"Two-Piece Set": "SET"}[garment]


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{type_token(row['garment'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


def render_table() -> str:
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
        detail = cm(row["skirt_cm"])
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "-",
            display_jin_weight(row["weight"]),
            source_range(row["height"], "cm"),
            cm(row["chest_cm"]),
            detail,
            "-",
            cm(row["hip_cm"]),
            cm(row["waist_cm"]),
            cm(row["top_length_cm"]),
        ]
        cells[8] = cm(row["skirt_waist_cm"])
        rendered.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")
    return "\n".join([
        "<h3>Size Chart - Two-Piece Set</h3>",
        "<table id=\"size-chart\">",
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *rendered,
        "</tbody></table>",
    ])


def build_body() -> str:
    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Exact fiber composition was not visible in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> A bright mom-and-daughter look for resort days, beach photos, warm weekends, and easy matching moments.</li>",
        "<li><strong>Print reference:</strong> Red Resort pairs a vivid red short-sleeve tee with a crisp white pleated skirt.</li>",
        "<li><strong>Design details:</strong> Complete red short-sleeve top plus white pleated skirt set; hats, bags, sunglasses, and shoes are styling props only.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, turn inside out, line dry, and cool iron if needed.</li>",
        "<li><strong>Size range:</strong> Complete sets run Child 4 Years through Child 9-10 Years and Mother S-2XL.</li>",
        "</ul>",
        render_table(),
        "<p>Red Resort is a clean, cheerful mommy-and-me outfit built around a red tee and white pleated skirt. The look feels polished in photos while staying casual enough for sunny walks, park days, and vacation memories.</p>",
        "<p>The vendor evidence provides a top measurement chart, a skirt measurement chart for numeric skirt sizes, and a seller selector showing the complete set sizes. The skirt chart rows 110-150 are shown where they match the selector; adult skirt measurements are left unavailable because no S-2XL skirt chart was supplied.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Complete outfit:</strong> Each size includes both the red top and the white pleated skirt.</li>",
        "<li><strong>Mother-daughter styling:</strong> The attached product image supports girls and mothers only, so the draft resolves to Mommy and Me.</li>",
        "<li><strong>Chart-backed rows:</strong> Every variant is backed by the seller selector; skirt measurements appear only where the supplied skirt chart matches the selector size.</li>",
        "<li><strong>Photo-ready palette:</strong> Bright red and clean white are simple to coordinate for beach and resort outfits.</li>",
        "<li><strong>Draft-first setup:</strong> Created unpublished for fabric, inventory, and final image review before launch.</li>",
        "</ul>",
        "<p>Choose the set sizes you need to build a matching red-and-white outfit for your next sunny day together.</p>",
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


def tags() -> list[str]:
    values = [
        "Mommy and Me",
        "Sets",
        "Matching Family Sets",
        "Matching Family Outfits",
        "Mommy and Me Set",
        "Mommy and Me Outfit",
        "Mother Daughter Matching",
        "Mother Daughter Set",
        "Girl Set",
        "Mother Set",
        "Two-Piece Set",
        "Tee",
        "Short Sleeve Tee",
        "Pleated Skirt",
        "Summer",
        "Beach",
        "Vacation",
        "Resort",
        "Red",
        "White",
        PRINT_NAME,
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Two-Piece Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "draft_review"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "not_paid_ready"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69600804961", "gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "waist_cm", "length_cm", "sleeve_cm", "skirt_cm", "pant_cm"}
    if len(SIZE_CHART) != 10 or len(variants) != len(SIZE_CHART):
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
        errors.append("one or more size tables does not have 10 headers")
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
        derived.write_text(json.dumps({"option_names": ["Type", "Size"], "variants": variants}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "red mother daughter short sleeve top and white pleated skirt sold together as a complete two-piece set"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "Sets",
            "--tags", ", ".join(tags()),
        ], check=True)


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    alt_by_name = {
        "01-family-look.png": "Mother and daughter wearing Red Resort red tops and white pleated skirts.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if "size-chart" in path.name:
            continue
        alt = alt_by_name.get(path.name, "Red Resort mommy and me red and white outfit.")
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""", {
            "input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]
        })
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMREDRESORT"
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
            "Option1 Name": "Type",
            "Option1 Value": row["garment"],
            "Option2 Name": "Size",
            "Option2 Value": row["picker_label"],
            "Variant SKU": variant["inventoryItem"]["sku"],
            "Variant Grams": "380",
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
            "Google Shopping / Gender": "female",
            "Google Shopping / Age Group": "kids" if row["audience"] == "child" else "adult",
            "Google Shopping / MPN": variant["inventoryItem"]["sku"],
            "Google Shopping / Condition": "new",
            "Google Shopping / Custom Product": "FALSE",
            "Google Shopping / Custom Label 0": "draft_review" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Mommy and Me Set" if i == 1 else "",
            "Google Shopping / Custom Label 4": "not_paid_ready" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Mommy and Me Set" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Mommy and Me Set" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Two-Piece Set" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false",
            "Age group (product.metafields.shopify.age-group)": "kids, adults" if i == 1 else "",
            "Color (product.metafields.shopify.color-pattern)": "Red, White" if i == 1 else "",
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
    if product["status"] != EXPECTED_STATUS:
        errors.append(f"status is {product['status']}, expected {EXPECTED_STATUS}")
    if EXPECT_PUBLISHED_NULL and product.get("publishedAt"):
        errors.append(f"publishedAt is {product['publishedAt']}, expected null")
    if not ALLOW_LIVE_PUBLICATIONS and any(node["isPublished"] for node in product["resourcePublicationsV2"]["nodes"]):
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
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(row["garment"], row["picker_label"]) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Type x Size option combinations do not match")
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
        "shopify.size", "shopify.target-gender", "global.title_tag", "global.description_tag",
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
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |")
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible in the attached charts or product image."),
        ("shopify.sleeve-length-type", "Top sleeve lengths are charted, but no owner-subtype-safe sleeve-length catalog value was verified for this Outfit Sets taxonomy run."),
        ("shopify.neckline", "The red top neckline is visible, but no catalog GID was verified for the exact tee neckline in this product subtype."),
        ("shopify.top-length-type", "The vendor chart gives exact top lengths, but those do not map cleanly to one standard top-length type."),
        ("shopify.dress-occasion", "Not applicable because this is not a dress listing."),
        ("shopify.dress-style", "Not applicable because the garment is a top and skirt outfit, not a dress."),
        ("shopify.skirt-dress-length-type", "Skirt lengths are charted, but no owner-subtype-safe skirt-length catalog value was verified for this Outfit Sets taxonomy run."),
    ]
    live_publications = [p for p in verify["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    smart_collections = verify["collections"]["nodes"] or []
    smart_lines = [f"- {item['title']} (`/{item['handle']}`)" for item in smart_collections] or ["- None returned immediately; draft products may not index into smart collections until publication."]
    shopify_visible = "\n".join([verify["title"], verify["descriptionHtml"], verify["productType"], ", ".join(verify["tags"]), verify["seo"]["title"] or "", verify["seo"]["description"] or ""]).lower()
    source_guard_ok = all(token not in shopify_visible for token in ["1688", "alibaba", "detail.1688.com"])
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        f"- **Live:** {verify.get('onlineStoreUrl') or 'not published'}",
        f"- **Vendor source:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Mommy and Me |",
        "| PRIMARY_CATEGORY | Sets / Outfit Sets |",
        "| DESIGNS_TO_LIST | auto -> complete red short-sleeve top plus white pleated skirt set shown in the attached image and vendor selector |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned Alibaba anti-bot/CAPTCHA punish markup (`_____tmd_____`), so the attached product and size-chart images were used as authoritative evidence per the canonical workflow. The source URL is preserved only in local operator notes and was not written to Shopify-visible fields.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## Pricing",
        "| Audience | Set price | Compare-at | Cost |", "|---|---:|---:|---:|",
        f"| Girl | {CHILD_PRICE} | {compare_at(CHILD_PRICE)} | {cost_for(CHILD_PRICE)} |",
        f"| Mother | {ADULT_PRICE} | {compare_at(ADULT_PRICE)} | {cost_for(ADULT_PRICE)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap, "",
        "## Derivations",
        "- `LISTING_MODE` resolved to Mommy and Me because the attached product image supports mother/daughter styling only; no father or boy product image evidence was supplied.",
        "- Owner clarified the top and skirt are sold together, so the Shopify option model is one complete `Two-Piece Set` Type per size.",
        "- Top source `胸围` values are flat garment widths, so they were doubled into wearable `chest_cm` values. Top hips/waists follow the canonical top derivation rules.",
        "- Skirt source `全腰围` values were copied into waist only for selector sizes 110-150. Skirt hip cells are left unavailable because the source chart does not publish them.",
        "- The seller selector screenshot confirms set sizes 110, 120, 130, 140, 150, S, M, L, XL, and 2XL; all are listed as complete-set variants.",
        "- The skirt measurement screenshot includes rows 160 and 170, but those do not match the adult selector labels S-2XL, so they are not mapped to Mother S/M. Adult skirt measurements are shown as unavailable rather than converted incorrectly.",
        "- Pricing follows nearby Mommy and Me complete-set precedent: girl `28.99`, mother `31.99`; Cost per item is exactly 50%.", "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        f"| Product status preserved | {'PASS' if verify['status'] == EXPECTED_STATUS else 'FAIL'} | {verify['status']} |",
        f"| Publication timestamp policy | {'PASS' if (not EXPECT_PUBLISHED_NULL or not verify.get('publishedAt')) else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| Sales-channel publication policy | {'PASS' if (ALLOW_LIVE_PUBLICATIONS or not live_publications) else 'FAIL'} | {[p['publication']['name'] for p in live_publications]} |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        f"| Source URL guard | {'PASS' if source_guard_ok else 'FAIL'} | no forbidden source tokens in Shopify product fields |",
        f"| Size table rows | {'PASS' if table_row_count(verify['descriptionHtml']) == len(SIZE_CHART) else 'FAIL'} | {table_row_count(verify['descriptionHtml'])} |",
        f"| Size table headers | {'PASS' if all(part.count('<th>') == 10 for part in re.findall(r'<table.*?</table>', verify['descriptionHtml'], re.S)) else 'FAIL'} | 10 headers per table |", "",
        "## Price Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |" for row in price_rows], "",
        "## Metafields Written",
        *[f"- `{key}`" for key in written], "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        "## Smart Collections",
        *smart_lines, "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition before any publish-live step.",
        "- Inventory quantities and per-variant grams still need operator stock values.",
        "- Confirm whether the vendor can provide adult S-2XL skirt measurements before publication.",
        "- Consider a cleaner final photoshoot image set before launch.", "",
        "## Files saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    global EXPECTED_STATUS, EXPECT_PUBLISHED_NULL, ALLOW_LIVE_PUBLICATIONS
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
        {"name": "Type", "values": [{"name": "Two-Piece Set"}]},
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

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status onlineStoreUrl variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    if existing:
        if existing["status"] == "ACTIVE":
            EXPECTED_STATUS = "ACTIVE"
            EXPECT_PUBLISHED_NULL = False
            ALLOW_LIVE_PUBLICATIONS = True
        product_id = existing["id"]
        update_product_input = {"id": product_id, **product_input, "status": existing["status"]}
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": update_product_input})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
        spec_skus = {variant["inventoryItem"]["sku"] for variant in variants}
        create_variants = [variant for variant in variants if variant["inventoryItem"]["sku"] not in live_by_sku]
        if create_variants:
            res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {
                "productId": product_id,
                "variants": create_variants,
                "strategy": "REMOVE_STANDALONE_VARIANT",
            })
            require_no_user_errors(res, ["data", "productVariantsBulkCreate", "userErrors"])
            existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status onlineStoreUrl variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
            live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
        delete_ids = [node["id"] for sku, node in live_by_sku.items() if sku not in spec_skus]
        if delete_ids:
            res = gql("""mutation($productId:ID!,$ids:[ID!]!){ productVariantsBulkDelete(productId:$productId, variantsIds:$ids){ product{id} userErrors{field message} } }""", {"productId": product_id, "ids": delete_ids})
            require_no_user_errors(res, ["data", "productVariantsBulkDelete", "userErrors"])
            existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status onlineStoreUrl variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
            live_by_sku = {node["sku"]: node for node in existing["variants"]["nodes"] if node.get("sku")}
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

    current_mf = gql("""query($id:ID!){ product(id:$id){ metafields(first:120){nodes{namespace key}} } }""", {"id": product_id})["data"]["product"]["metafields"]["nodes"]
    stale_metafields = [
        {"ownerId": product_id, "namespace": node["namespace"], "key": node["key"]}
        for node in current_mf
        if node["namespace"] == "shopify" and node["key"] in {
            "dress-occasion",
            "dress-style",
            "fabric",
            "neckline",
            "skirt-dress-length-type",
            "sleeve-length-type",
            "top-length-type",
        }
    ]
    if stale_metafields:
        res = gql("""mutation($metafields:[MetafieldIdentifierInput!]!){ metafieldsDelete(metafields:$metafields){ deletedMetafields{key namespace ownerId} userErrors{field message} } }""", {"metafields": stale_metafields})
        require_no_user_errors(res, ["data", "metafieldsDelete", "userErrors"])

    upload_media(product_id)
    time.sleep(2)
    verify = gql("""query($id:ID!){ product(id:$id){ id title handle status publishedAt onlineStoreUrl descriptionHtml productType tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} collections(first:50){nodes{title handle}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}} } }""", {"id": product_id})["data"]["product"]
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
