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

python3.13 - <<'PY'
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
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "shine-tropical-family-matching-set"
TITLE = "Shine Tropical Family Matching Set - Dress & Shorts"
SEO_TITLE = "Shine Tropical Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Bright tropical family matching set with dresses plus shirt-and-shorts outfits for mom, dad, girls & boys. Child 2Y-12Y and adult S-5XL."
PRINT_NAME = "Shine Tropical"
SHORTCODE = "SHTR"
COLOR_TOKEN = "TROP"
VENDOR_REFERENCE = "redacted supplier URL from current request"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
CURRENT_MEDIA_ITEMS = [
    (UPLOAD_DIR / "01-family-look.png", "Shine tropical family matching dress and shirt-and-shorts product image"),
]
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-shtr-shine-tropical-family-matching-set.sh"

SIZE_MAP: dict[str, tuple[str | None, str]] = {
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
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
    "Father 5XL": (None, "no 5XL size metaobject match"),
}


def lb(kg: Decimal | float | int) -> str:
    value = (Decimal(str(kg)) * Decimal("2.20462")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{value}"


def up_to_weight(kg: Decimal | float | int) -> str:
    return f"up to {kg} kg / up to {lb(kg)} lbs"


def height_copy(cm: int) -> str:
    inches = (Decimal(cm) / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{cm} cm / {inches} in"


SIZE_CHART: list[dict] = []


def add_row(
    *,
    audience: str,
    role: str,
    garment: str,
    vendor_label: str,
    picker_label: str,
    sku_suffix: str,
    age: str,
    weight: str,
    height: str,
    chest_cm: int,
    hip_cm: int,
    waist_cm: int,
    length_cm: int,
    skirt_cm: int = 0,
    pant_cm: int = 0,
    source_note: str,
) -> None:
    SIZE_CHART.append(
        {
            "audience": audience,
            "role": role,
            "garment": garment,
            "vendor_label": vendor_label,
            "picker_label": picker_label,
            "sku_suffix": sku_suffix,
            "age": age,
            "weight": weight,
            "height": height,
            "chest_cm": chest_cm,
            "hip_cm": hip_cm,
            "waist_cm": waist_cm,
            "length_cm": length_cm,
            "sleeve_cm": 0,
            "skirt_cm": skirt_cm,
            "pant_cm": pant_cm,
            "source_note": source_note,
        }
    )


CHILD_LABELS = [
    ("90", "Child 2 Years", "KID2Y", "2-3", 90),
    ("100", "Child 3 Years", "KID3Y", "3-4", 100),
    ("110", "Child 4 Years", "KID4Y", "4-5", 110),
    ("120", "Child 5 Years", "KID5Y", "6-7", 120),
    ("130", "Child 6-7 Years", "KID67Y", "7-8", 130),
    ("140", "Child 8 Years", "KID8Y", "9-10", 140),
    ("150", "Child 9-10 Years", "KID910Y", "10-11", 150),
    ("160", "Child 12 Years", "KID12Y", "12-13", 155),
]
CHILD_WEIGHTS = [15, 17.5, 20, 25, 30, 35, 39, Decimal("42.5")]

GIRL_DRESS_ROWS = [
    (54, 58),
    (58, 61),
    (62, 65),
    (65, 69),
    (70, 73),
    (75, 77),
    (80, 81),
    (85, 85),
]
for (vendor, picker, suffix, age, height_cm), weight_kg, (skirt, chest) in zip(CHILD_LABELS, CHILD_WEIGHTS, GIRL_DRESS_ROWS):
    add_row(
        audience="child",
        role="Girl Dress",
        garment="Dress",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age=age,
        weight=up_to_weight(weight_kg),
        height=height_copy(height_cm),
        chest_cm=chest,
        hip_cm=chest + 4,
        waist_cm=chest,
        length_cm=skirt,
        skirt_cm=skirt,
        source_note="Girl table publishes skirt/dress length and chest; waist and hip are derived by the kids dress rule.",
    )

MOTHER_DRESS_ROWS = [
    ("S", "Mother S", "S", 93, 88, 158, 50),
    ("M", "Mother M", "M", 96, 92, 162, 55),
    ("L", "Mother L", "L", 99, 96, 165, 60),
    ("XL", "Mother XL", "XL", 102, 100, 170, 65),
    ("XXL", "Mother 2XL", "2XL", 105, 104, 175, 70),
    ("3XL", "Mother 3XL", "3XL", 107, 108, 175, 75),
    ("4XL", "Mother 4XL", "4XL", 109, 112, 175, Decimal("82.5")),
]
for vendor, picker, suffix, skirt, chest, height_cm, weight_kg in MOTHER_DRESS_ROWS:
    hip = chest + 6
    add_row(
        audience="mother",
        role="Mother Dress",
        garment="Dress",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age="-",
        weight=up_to_weight(weight_kg),
        height=height_copy(height_cm),
        chest_cm=chest,
        hip_cm=hip,
        waist_cm=hip - 8,
        length_cm=skirt,
        skirt_cm=skirt,
        source_note="Mother table publishes skirt/dress length, chest, height and weight guidance; waist and hip are derived by the mother dress rule.",
    )

BOY_SET_ROWS = [
    (38, 58, 25, 65),
    (41, 61, 26, 69),
    (44, 65, 27, 73),
    (47, 69, 29, 77),
    (50, 73, 30, 81),
    (53, 77, 32, 85),
    (56, 81, 34, 89),
    (58, 85, 35, 93),
]
for (vendor, picker, suffix, age, height_cm), weight_kg, (shirt_len, chest, short_len, hip) in zip(CHILD_LABELS, CHILD_WEIGHTS, BOY_SET_ROWS):
    add_row(
        audience="child",
        role="Boy Shirt & Shorts Set",
        garment="Shirt & Shorts Set",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age=age,
        weight=up_to_weight(weight_kg),
        height=height_copy(height_cm),
        chest_cm=chest,
        hip_cm=hip,
        waist_cm=max(hip - 14, 0),
        length_cm=shirt_len,
        pant_cm=short_len,
        source_note="Boy table combines shirt length/chest with shorts length/hip; waist is derived from hip because no waist column is published.",
    )

FATHER_SET_ROWS = [
    ("M", "Father M", "M", 67, 96, 52, 112, 168, Decimal("62.5")),
    ("L", "Father L", "L", 69, 100, 54, 116, 173, Decimal("72.5")),
    ("XL", "Father XL", "XL", 71, 104, 56, 120, 178, Decimal("82.5")),
    ("XXL", "Father 2XL", "2XL", 73, 108, 58, 125, 182, Decimal("92.5")),
    ("XXXL", "Father 3XL", "3XL", 75, 112, 60, 130, 185, 100),
    ("4XL", "Father 4XL", "4XL", 77, 116, 62, 134, 190, 110),
    ("5XL", "Father 5XL", "5XL", 79, 120, 64, 138, 195, 120),
]
for vendor, picker, suffix, shirt_len, chest, short_len, hip, height_cm, weight_kg in FATHER_SET_ROWS:
    add_row(
        audience="father",
        role="Father Shirt & Shorts Set",
        garment="Shirt & Shorts Set",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age="-",
        weight=up_to_weight(weight_kg),
        height=height_copy(height_cm),
        chest_cm=chest,
        hip_cm=hip,
        waist_cm=max(hip - 14, 0),
        length_cm=shirt_len,
        pant_cm=short_len,
        source_note="Father table combines shirt length/chest with shorts length/hip; waist is derived from hip because no waist column is published.",
    )


def gql(query: str, variables: dict | None = None) -> dict:
    request = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read())
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload


def require_no_user_errors(payload: dict, path: list[str]) -> None:
    node = payload
    for part in path:
        node = node.get(part, {})
    if node:
        raise RuntimeError(node)


def compare_at(price: str) -> str:
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def cost_for(price: str) -> str:
    return str((Decimal(price) * Decimal("0.50")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] in {"mother", "father"} else CHILD_PRICE


def sku_for(row: dict) -> str:
    role_token = {
        "Girl Dress": "GRL",
        "Mother Dress": "MOM",
        "Boy Shirt & Shorts Set": "BOY",
        "Father Shirt & Shorts Set": "DAD",
    }[row["role"]]
    type_token = {"Dress": "DRS", "Shirt & Shorts Set": "SET"}[row["garment"]]
    return f"DLM-{SHORTCODE}-{role_token}-{type_token}-{row['sku_suffix']}-{COLOR_TOKEN}"


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
                    {"optionName": "Type", "name": row["garment"]},
                    {"optionName": "Size", "name": row["picker_label"]},
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


def tags() -> list[str]:
    values = [
        "Family Matching",
        "Mommy and Me",
        "Daddy and Me",
        "Matching Family Set",
        "Matching Family Outfits",
        "Matching Family Dress",
        "Matching Family Shorts Set",
        "Dress & Shorts",
        "Shirt & Shorts Set",
        "Sets",
        "Girl Dress",
        "Mother Dress",
        "Boy Shirt & Shorts Set",
        "Father Shirt & Shorts Set",
        "Four-Role Matching",
        "Shine Tropical",
        "Tropical Print",
        "Color Pop",
        "Floral",
        "Resort",
        "Beach",
        "Vacation",
        "Summer",
        "White",
        "Red",
        "Pink",
        "Blue",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = [gid for gid, _label in dict.fromkeys(SIZE_MAP[row["picker_label"]] for row in SIZE_CHART) if gid]
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Tropical Family Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress & Shirt-Shorts Set"},
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
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69963645025", "gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/70220546145"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def cm_in(value: int | str) -> str:
    if value in {0, "", "-"}:
        return "-"
    inches = (Decimal(str(value)) / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{value} cm / {inches} in"


def row_to_tr(row: dict) -> str:
    cells = [
        row["picker_label"],
        row["age"],
        row["weight"],
        row["height"],
        cm_in(row["chest_cm"]),
        cm_in(row["skirt_cm"] if row["garment"] == "Dress" else 0),
        cm_in(row["pant_cm"] if row["garment"] == "Shirt & Shorts Set" else 0),
        cm_in(row["hip_cm"]),
        cm_in(row["waist_cm"]),
        cm_in(row["length_cm"]),
    ]
    return "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"


def size_table(garment: str) -> str:
    rows = "\n".join(row_to_tr(row) for row in SIZE_CHART if row["garment"] == garment)
    table_id = "shirt-shorts-set" if garment == "Shirt & Shorts Set" else garment.lower()
    return f"""<h3>Size Chart - {garment}</h3>
<table id="size-chart-{table_id}">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Weight (kg/lbs)</th>
      <th>Height (cm/in)</th>
      <th>Chest/Bust (cm/in)</th>
      <th>Sleeve or Skirt (cm/in)</th>
      <th>Pant/Short or - (cm/in)</th>
      <th>Hip (cm/in)</th>
      <th>Waist (cm/in)</th>
      <th>Garment Length (cm/in)</th>
    </tr>
  </thead>
  <tbody>
{rows}
  </tbody>
</table>"""


def build_body() -> str:
    return f"""<ul>
<li><strong>Fabric &amp; feel:</strong> Lightweight warm-weather woven fabric; exact fiber content was not visible from the blocked supplier page.</li>
<li><strong>Family story:</strong> A bright coordinated look for mom, dad, girls, and boys in one tropical vacation print.</li>
<li><strong>Print:</strong> Colorful red, pink, blue, and white tropical graphics with a sporty Shine tee detail on the boys' and dads' side.</li>
<li><strong>Design details:</strong> Girls and moms wear the sleeveless dress; boys and dads wear the white graphic shirt with matching tropical shorts. Sunglasses, hats, watches, and shoes are styling only.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Child 2 Years through Child 12 Years, Mother S-4XL, and Father M-5XL.</li>
</ul>

{size_table("Dress")}

{size_table("Shirt & Shorts Set")}

<p>The Shine Tropical Family Matching Set is made for bright resort days, poolside photos, cruises, and sunny family weekends. The dress side keeps the girls' and moms' look easy and photo-ready, while the boys' and dads' shirt-and-shorts set gives the outfit a relaxed vacation finish.</p>

<p>This draft follows the attached chart closely: dress variants are created for girls and mothers, and shirt-and-shorts set variants are created for boys and fathers because the male rows publish shirt measurements and shorts measurements together. Every selectable size is backed by a visible source row, with derived waist values called out in the local listing notes.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Coordinated family options:</strong> Dress and shirt-and-shorts set choices are grouped in one family matching product.</li>
<li><strong>Vacation-ready print:</strong> Bright tropical colors make the look stand out in beach, resort, and poolside photos.</li>
<li><strong>Role-bearing sizes:</strong> Size labels clearly separate Child, Mother, and Father rows.</li>
<li><strong>Chart-backed draft:</strong> Only rows visible in the supplied size chart are included as variants.</li>
<li><strong>Wide father range:</strong> Father sizes run from M through 5XL based on the source chart.</li>
</ul>

<p>Choose the Type and Size for each family member, then build a bright matching look for vacations, family photos, and sunny days together.</p>"""


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(TITLE) > 70:
        raise RuntimeError("title too long")
    if len(SEO_TITLE) > 60:
        raise RuntimeError("seo title too long")
    if len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("seo description too long")
    if len(variants) != len(SIZE_CHART):
        raise RuntimeError("variant count does not match size chart")
    if table_row_count(body) != len(SIZE_CHART):
        raise RuntimeError("body table rows do not match size chart")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("size table must have exactly 10 headers")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("duplicate role/picker row")
    for row in SIZE_CHART:
        if row["picker_label"] not in SIZE_MAP:
            raise RuntimeError(f"missing shopify.size decision for {row['picker_label']}")
        if row["waist_cm"] in {0, "", "-"}:
            raise RuntimeError(f"missing waist value for {row['role']} {row['picker_label']}")
    joined = json.dumps({"title": TITLE, "seo": SEO_TITLE, "body": body, "tags": tags()}, ensure_ascii=False).lower()
    if "1688" in joined or "alibaba" in joined or "detail." in joined:
        raise RuntimeError("source token leaked into generated product data")


def run_variant_model_guard(body: str, variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"], "variants": variants}), encoding="utf-8")
        evidence.write_text(
            json.dumps(
                {
                    "title": "family matching tropical dress shirt shorts set",
                    "notes": "Attached evidence shows dresses plus shirt-and-shorts rows, including dress, shirt, and shorts garment evidence.",
                }
            ),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "python3",
                str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
                "--size-chart",
                str(chart),
                "--derived",
                str(derived),
                "--vendor-evidence",
                str(evidence),
                "--primary-category",
                "FamilySet",
                "--tags",
                ", ".join(tags()),
            ],
            check=True,
        )


def product_query(product_id_or_handle: str, *, by_handle: bool = False) -> dict | None:
    fragment = """id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{id alt image{url}}}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:50){nodes{isPublished publishDate publication{id name}}} collections(first:50){nodes{title handle}}"""
    if by_handle:
        return gql(f"""query($handle:String!){{ productByHandle(handle:$handle){{ {fragment} }} }}""", {"handle": product_id_or_handle})["data"]["productByHandle"]
    return gql(f"""query($id:ID!){{ product(id:$id){{ {fragment} }} }}""", {"id": product_id_or_handle})["data"]["product"]


def upload_media(product_id: str, existing_media: list[dict]) -> None:
    existing_alts = {node.get("alt") for node in existing_media}
    for path, alt in CURRENT_MEDIA_ITEMS:
        if not path.exists() or alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        staged = gql(
            """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""",
            {"input": [{"filename": path.name, "mimeType": mime, "httpMethod": "POST", "resource": "IMAGE"}]},
        )
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        args = ["curl", "-sS", "-X", "POST", target["url"]]
        for param in target["parameters"]:
            args += ["-F", f"{param['name']}={param['value']}"]
        args += ["-F", f"file=@{path}"]
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
        media = gql(
            """mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""",
            {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]},
        )
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    header = (ROOT / "ops/listings/blush-garden-mommy-and-me-swimsuits-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    tags_text = ", ".join(tags())
    for index, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update(
            {
                "Handle": HANDLE,
                "Title": TITLE if index == 1 else "",
                "Body (HTML)": body if index == 1 else "",
                "Vendor": VENDOR if index == 1 else "",
                "Product Category": EXPECTED_TAXONOMY_FULL_NAME if index == 1 else "",
                "Type": PRODUCT_TYPE if index == 1 else "",
                "Tags": tags_text if index == 1 else "",
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
                "Google Shopping / Custom Label 3": "Dress & Shorts" if index == 1 else "",
                "Google Shopping / Custom Label 4": "Four-Role Matching" if index == 1 else "",
                "Category1 (product.metafields.custom.category1)": "Family Matching" if index == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if index == 1 else "",
                "Style (product.metafields.custom.style)": "Tropical Family Set" if index == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Set" if index == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if index == 1 else "",
                "Type (product.metafields.custom.type)": "Dress & Shirt-Shorts Set" if index == 1 else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if index == 1 else "",
                "Age group (product.metafields.shopify.age-group)": "Kids, Adults" if index == 1 else "",
                "Color (product.metafields.shopify.color-pattern)": "Red, Pink, Blue" if index == 1 else "",
                "Size (product.metafields.shopify.size)": ", ".join(dict.fromkeys(row["picker_label"] for row in SIZE_CHART if SIZE_MAP[row["picker_label"]][0])) if index == 1 else "",
                "Target gender (product.metafields.shopify.target-gender)": "Female, Male" if index == 1 else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def verify_product(product: dict, variants: list[dict]) -> tuple[list[str], list[dict]]:
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    errors: list[str] = []
    price_rows: list[dict] = []
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
    joined_product_data = json.dumps(
        {
            "title": product["title"],
            "descriptionHtml": product["descriptionHtml"],
            "tags": product["tags"],
            "seo": product["seo"],
            "metafields": product["metafields"]["nodes"],
        },
        ensure_ascii=False,
    ).lower()
    if "1688" in joined_product_data or "alibaba" in joined_product_data or "detail." in joined_product_data:
        errors.append("source URL token leaked into Shopify product data")
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
        price_rows.append(
            {
                "sku": node["sku"],
                "live_price": node["price"],
                "live_compare_at": node["compareAtPrice"],
                "live_cost": unit_cost,
                "spec_price": spec["price"],
                "spec_compare_at": spec["compareAtPrice"],
                "spec_cost": spec["inventoryItem"]["cost"],
                "match": match,
            }
        )
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict], created_skus: list[str]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        size_ref = f"`{gid}` ({label})" if gid else f"skipped ({label})"
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | {size_ref} |"
        )
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    live_publications = [node["publication"]["name"] for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    skipped = {
        "shopify.fabric": "Exact fiber composition was not visible in the supplied evidence.",
        "shopify.size Father 5XL": "The Father 5XL variant is chart-backed and created, but the store returned no honest 5XL size metaobject to reference.",
        "shopify.sleeve-length-type": "The product mixes sleeveless dresses and shirt-and-shorts sets; one product-level sleeve value would mislead.",
        "shopify.neckline": "The product mixes dresses and shirt-and-shorts sets; one product-level neckline does not apply.",
        "shopify.top-length-type": "The product mixes dresses with shirt-and-shorts sets, so one top-length value is too broad.",
        "shopify.dress-occasion": "The product is not a dress-only listing.",
        "shopify.dress-style": "The product mixes dresses and shirt-and-shorts sets, so one dress style would not describe every variant.",
        "shopify.skirt-dress-length-type": "The product mixes dresses and shirt-and-shorts sets, so one skirt/dress length value would not describe every variant.",
    }
    collections = sorted(node["handle"] for node in verify["collections"]["nodes"]) or ["collection indexing may wait until publication"]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_REFERENCE}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_REFERENCE} |",
        "| SIZE_CHART_SOURCE | attached size-chart image plus attached product image |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | Dress and Shorts; male chart rows resolved as Shirt & Shorts Set because shirt and shorts measurements are in the same source rows |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor Fetch Status",
        "The public supplier URL returned anti-bot interception markup in this shell. The attached product image and attached size chart were used as authoritative evidence per the canonical workflow. The supplier URL is intentionally redacted from repo artifacts and Shopify product data.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap,
        "",
        "## Derivations",
        "- Girl and mother dress waist/hip values are derived where the vendor chart omits them; the source publishes skirt/dress length, chest, height, and weight guidance.",
        "- Boy and father rows are listed as Shirt & Shorts Set because the source row combines shirt length/chest with shorts length/hip.",
        "- Boy and father set waist values are derived from the hip column because the source omits a waist column.",
        "- The 160 child row is mapped to Child 12 Years using the store's existing 160cm size convention.",
        "- Father 5XL is retained as a real variant because the size chart publishes it; it is skipped only from product-level shopify.size references because no honest 5XL metaobject was found.",
        "- Pricing follows nearby family-matching set patterns: child variants 28.99 and adult variants 31.99; Cost per item is exactly 50%.",
        "- No source/vendor URL or source marketplace token is written to Shopify product title, body, tags, SEO, or metafields.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| No sales-channel publications live | {'PASS' if not live_publications else 'FAIL'} | {live_publications} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Created SKUs | INFO | {', '.join(created_skus) if created_skus else 'none'} |",
        "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[
            f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |"
            for row in price_rows
        ],
        "",
        "## Metafields Written",
        *[f"- `{key}`" for key in written],
        "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped.items()],
        "",
        "## Smart Collections",
        ", ".join(collections),
        "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition if the supplier page becomes fully readable later.",
        "- Inventory quantities and variant grams remain operator stock inputs.",
        "- Review the product image crop before any separate publish-live request.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard(body, variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{id fullName isLeaf} } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Dress", "Shirt & Shorts Set"]]},
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

    product = product_query(HANDLE, by_handle=True)
    if product and product["status"] == "DRAFT":
        raise RuntimeError(f"Existing product {HANDLE} is ACTIVE; refusing draft-only update")
    if product:
        product_id = product["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]

    product = product_query(product_id)
    assert product is not None
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    live_skus = sorted(live_by_sku)
    spec_skus = sorted(spec_by_sku)
    if live_skus and live_skus != spec_skus:
        if not (len(product["variants"]["nodes"]) == 1 and not product["variants"]["nodes"][0].get("sku")):
            raise RuntimeError(f"existing draft has unexpected SKUs: {live_skus}")

    create_variants = [variant for sku, variant in spec_by_sku.items() if sku not in live_by_sku]
    created_skus = sorted(variant["inventoryItem"]["sku"] for variant in create_variants)
    if create_variants:
        res = gql(
            """mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""",
            {"productId": product_id, "variants": create_variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
        )
        require_no_user_errors(res, ["data", "productVariantsBulkCreate", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    update_variants = []
    for sku, spec in spec_by_sku.items():
        live = live_by_sku.get(sku)
        if not live:
            continue
        update_variants.append(
            {
                "id": live["id"],
                "price": spec["price"],
                "compareAtPrice": spec["compareAtPrice"],
                "taxable": True,
                "inventoryPolicy": "DENY",
                "inventoryItem": spec["inventoryItem"],
                "optionValues": spec["optionValues"],
            }
        )
    if update_variants:
        res = gql(
            """mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""",
            {"productId": product_id, "variants": update_variants},
        )
        require_no_user_errors(res, ["data", "productVariantsBulkUpdate", "userErrors"])

    mfs = metafields(product_id)
    for i in range(0, len(mfs), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mfs[i:i + 25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    upload_media(product_id, product["media"]["nodes"])
    time.sleep(2)
    verify = product_query(product_id)
    assert verify is not None
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    errors, price_rows = verify_product(verify, variants)
    write_listing(product_id, verify, variants, price_rows, created_skus)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(
        json.dumps(
            {
                "product_id": product_id,
                "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
                "handle": HANDLE,
                "status": verify["status"],
                "publishedAt": verify.get("publishedAt"),
                "onlineStoreUrl": verify.get("onlineStoreUrl"),
                "variant_count": len(verify["variants"]["nodes"]),
                "created_skus": created_skus,
                "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT), str(SIZE_CHART_OUT), str(BODY_HTML_OUT)],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
PY
