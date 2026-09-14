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

HANDLE = "sunshine-daisy-family-matching-set"
TITLE = "Sunshine Daisy Family Matching Set - Dress & Shirt"
SEO_TITLE = "Sunshine Daisy Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Yellow daisy family matching dresses and shirts for mom, dad, girls & boys. Child 2Y-10Y, Mother S-3XL, Father M-4XL."
PRINT_NAME = "Sunshine Daisy"
SHORTCODE = "SNDY"
COLOR_TOKEN = "YELDAISY"
VENDOR_REFERENCE = "redacted supplier URL from current request"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
CURRENT_MEDIA_ITEMS = [
    (UPLOAD_DIR / "01-family-look.png", "Sunshine Daisy family matching yellow floral dress and shirt product image"),
]
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-sndy-sunshine-daisy-family-matching-set.sh"

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
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
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
    sleeve_cm: int = 0,
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
            "sleeve_cm": sleeve_cm,
            "skirt_cm": skirt_cm,
            "pant_cm": pant_cm,
            "source_note": source_note,
        }
    )


def kg_range_from_jin(text: str) -> str:
    left, right = [Decimal(part.strip()) * Decimal("0.5") for part in text.split("-")]
    return f"{left:g}-{right:g} kg / {lb(left)}-{lb(right)} lbs"


def height_range_copy(text: str) -> str:
    left, right = [Decimal(part.strip()) for part in text.split("-")]
    left_in = (left / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    right_in = (right / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{left:g}-{right:g} cm / {left_in}-{right_in} in"


GIRL_DRESS_ROWS = [
    ("90", "Child 2 Years", "KID2Y", "2-3", "80-90", "20-25", 57, 54),
    ("100", "Child 3 Years", "KID3Y", "3-4", "90-100", "25-30", 60, 58),
    ("110", "Child 4 Years", "KID4Y", "4-5", "100-110", "30-35", 63, 62),
    ("120", "Child 5 Years", "KID5Y", "5-6", "110-120", "35-45", 66, 66),
    ("130", "Child 6-7 Years", "KID67Y", "6-7", "120-130", "45-55", 70, 70),
    ("140", "Child 8 Years", "KID8Y", "8", "130-140", "55-65", 74, 74),
    ("150", "Child 9-10 Years", "KID910Y", "9-10", "140-150", "65-75", 78, 78),
]
for vendor, picker, suffix, age, height_cm, weight_jin, skirt, chest in GIRL_DRESS_ROWS:
    add_row(
        audience="child",
        role="Girl Dress",
        garment="Dress",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age=age,
        weight=kg_range_from_jin(weight_jin),
        height=height_range_copy(height_cm),
        chest_cm=chest,
        hip_cm=chest + 4,
        waist_cm=chest,
        length_cm=skirt,
        skirt_cm=skirt,
        source_note="Girl dress table publishes skirt/dress length, chest, height guidance, and jin weight guidance; waist and hip are derived by the kids dress rule.",
    )

MOTHER_DRESS_ROWS = [
    ("S", "Mother S", "S", "155-160", "85-100", 113, 82),
    ("M", "Mother M", "M", "160-165", "100-110", 115, 86),
    ("L", "Mother L", "L", "165-170", "110-120", 117, 90),
    ("XL", "Mother XL", "XL", "170-175", "120-130", 119, 94),
    ("2XL", "Mother 2XL", "2XL", "175-180", "130-145", 121, 98),
    ("3XL", "Mother 3XL", "3XL", "180-185", "145-160", 123, 102),
]
for vendor, picker, suffix, height_cm, weight_jin, skirt, chest in MOTHER_DRESS_ROWS:
    hip = chest + 6
    add_row(
        audience="mother",
        role="Mother Dress",
        garment="Dress",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age="-",
        weight=kg_range_from_jin(weight_jin),
        height=height_range_copy(height_cm),
        chest_cm=chest,
        hip_cm=hip,
        waist_cm=hip - 8,
        length_cm=skirt,
        skirt_cm=skirt,
        source_note="Mother dress table publishes skirt/dress length, chest, height guidance, and jin weight guidance; waist and hip are derived by the mother dress rule.",
    )

BOY_SET_ROWS = [
    ("90", "Child 2 Years", "KID2Y", "2-3", "80-90", "20-25", 40, 64, 11, Decimal("25.5")),
    ("100", "Child 3 Years", "KID3Y", "3-4", "90-100", "25-30", 43, 68, 12, 27),
    ("110", "Child 4 Years", "KID4Y", "4-5", "100-110", "30-35", 46, 72, 13, Decimal("28.5")),
    ("120", "Child 5 Years", "KID5Y", "5-6", "110-120", "35-45", 49, 76, 14, 30),
    ("130", "Child 6-7 Years", "KID67Y", "6-7", "120-130", "45-55", 52, 80, 15, Decimal("31.5")),
    ("140", "Child 8 Years", "KID8Y", "8", "130-140", "55-65", 55, 84, 16, 33),
    ("150", "Child 9-10 Years", "KID910Y", "9-10", "140-150", "65-75", 58, 88, 17, Decimal("34.5")),
]
for vendor, picker, suffix, age, height_cm, weight_jin, shirt_len, chest, sleeve, shoulder in BOY_SET_ROWS:
    add_row(
        audience="child",
        role="Boy Shirt",
        garment="Shirt",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age=age,
        weight=kg_range_from_jin(weight_jin),
        height=height_range_copy(height_cm),
        chest_cm=chest,
        hip_cm=chest,
        waist_cm=max(chest - 12, 0),
        length_cm=shirt_len,
        sleeve_cm=sleeve,
        source_note=f"Boy table publishes shirt length, chest, shoulder {shoulder:g} cm, sleeve, height guidance, and jin weight guidance; shorts columns are excluded per request, and hip/waist are derived by the shirt rule.",
    )

FATHER_SET_ROWS = [
    ("M", "Father M", "M", "160-165", "95-110", 68, 100, 19, 44),
    ("L", "Father L", "L", "165-170", "110-125", 70, 104, 20, 46),
    ("XL", "Father XL", "XL", "170-175", "125-145", 72, 108, 21, 48),
    ("2XL", "Father 2XL", "2XL", "175-180", "145-165", 74, 112, 22, 50),
    ("3XL", "Father 3XL", "3XL", "180-185", "165-195", 76, 116, 23, 52),
    ("4XL", "Father 4XL", "4XL", "185-190", "195-215", 78, 120, 24, 54),
]
for vendor, picker, suffix, height_cm, weight_jin, shirt_len, chest, sleeve, shoulder in FATHER_SET_ROWS:
    add_row(
        audience="father",
        role="Father Shirt",
        garment="Shirt",
        vendor_label=vendor,
        picker_label=picker,
        sku_suffix=suffix,
        age="-",
        weight=kg_range_from_jin(weight_jin),
        height=height_range_copy(height_cm),
        chest_cm=chest,
        hip_cm=chest,
        waist_cm=max(chest - 12, 0),
        length_cm=shirt_len,
        sleeve_cm=sleeve,
        source_note=f"Father table publishes shirt length, chest, shoulder {shoulder:g} cm, sleeve, height guidance, and jin weight guidance; shorts columns are excluded per request, and hip/waist are derived by the shirt rule.",
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
        "Boy Shirt": "BOY",
        "Father Shirt": "DAD",
    }[row["role"]]
    type_token = {"Dress": "DRS", "Shirt": "SHIRT"}[row["garment"]]
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
        "Matching Family Tops",
        "Dress & Shirt",
        "Shirt",
        "Sets",
        "Girl Dress",
        "Mother Dress",
        "Boy Shirt",
        "Father Shirt",
        "Four-Role Matching",
        "Sunshine Daisy",
        "Yellow Daisy",
        "Daisy",
        "Embroidered Daisy",
        "Floral",
        "Resort",
        "Beach",
        "Vacation",
        "Summer",
        "Yellow",
        "White",
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
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Daisy Beach Family Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress & Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress Shirt"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622104161", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/129971519585", "gid://shopify/Metaobject/130231140449"])},
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
        cm_in(row["skirt_cm"] if row["garment"] == "Dress" else row["sleeve_cm"]),
        "-",
        cm_in(row["hip_cm"]),
        cm_in(row["waist_cm"]),
        cm_in(row["length_cm"]),
    ]
    return "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"


def size_table(garment: str) -> str:
    rows = "\n".join(row_to_tr(row) for row in SIZE_CHART if row["garment"] == garment)
    table_id = garment.lower()
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
<li><strong>Fabric &amp; feel:</strong> Lightweight warm-weather woven fabric; exact fiber content was not visible in the supplied evidence.</li>
<li><strong>Family story:</strong> A bright coordinated beach look for mom, dad, girls, and boys in one yellow daisy story.</li>
<li><strong>Print:</strong> Sunshine-yellow fabric with white daisy embroidery and a soft vacation feel.</li>
<li><strong>Design details:</strong> Girls and moms wear the sleeveless ruffle-neck dress; boys and dads wear the short-sleeve button shirt. Shorts, hats, bags, shoes, and accessories are styling only.</li>
<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>
<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S-3XL, and Father M-4XL.</li>
</ul>

{size_table("Dress")}

{size_table("Shirt")}

<p>The Sunshine Daisy Family Matching Set is made for beach trips, sunny family photos, vacation dinners, and coordinated warm-weather celebrations. The dress side keeps the girls' and moms' look sweet and photo-ready, while the boys' and dads' shirt keeps the matching moment relaxed and easy.</p>

<p>This draft follows the attached chart closely: dress variants are created for girls and mothers, and shirt variants are created for boys and fathers. The source chart also publishes shorts measurements on the male rows, but shorts are excluded from this listing per the operator request.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Coordinated family options:</strong> Dress and shirt choices are grouped in one family matching product.</li>
<li><strong>Vacation-ready daisy look:</strong> Yellow floral styling makes the set stand out in beach and resort photos.</li>
<li><strong>Role-bearing sizes:</strong> Size labels clearly separate Child, Mother, and Father rows.</li>
<li><strong>Chart-backed draft:</strong> Only rows visible in the supplied size chart are included as variants.</li>
<li><strong>Shorts excluded:</strong> The white shorts shown in the image and chart are styling only and are not sold in this draft.</li>
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
                    "title": "family matching yellow daisy dress shirt beach set",
                    "notes": "Attached evidence shows dresses plus shirt rows; shorts are visible in the source chart but explicitly excluded by the operator request.",
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
                "Google Shopping / Custom Label 3": "Dress Shirt" if index == 1 else "",
                "Google Shopping / Custom Label 4": "Four-Role Matching" if index == 1 else "",
                "Category1 (product.metafields.custom.category1)": "Family Matching" if index == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if index == 1 else "",
                "Style (product.metafields.custom.style)": "Daisy Beach Family Set" if index == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Set" if index == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if index == 1 else "",
                "Type (product.metafields.custom.type)": "Dress & Shirt" if index == 1 else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if index == 1 else "",
                "Age group (product.metafields.shopify.age-group)": "Kids, Adults" if index == 1 else "",
                "Color (product.metafields.shopify.color-pattern)": "Yellow, White, Floral, Multicolor" if index == 1 else "",
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
        "shopify.sleeve-length-type": "The product mixes sleeveless dresses and short-sleeve shirts; one product-level sleeve value would mislead.",
        "shopify.neckline": "The product mixes ruffle-neck dresses and collared shirts; one product-level neckline does not apply.",
        "shopify.top-length-type": "The product mixes dresses with shirts, so one top-length value is too broad.",
        "shopify.dress-occasion": "The product is not a dress-only listing.",
        "shopify.dress-style": "The product mixes dresses and shirts, so one dress style would not describe every variant.",
        "shopify.skirt-dress-length-type": "The product mixes dresses and shirts, so one skirt/dress length value would not describe every variant.",
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
        "| DESIGNS_TO_LIST | Dress and shirt only; shorts explicitly excluded |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor Fetch Status",
        "The public supplier page confirmed a beach/vacation daisy family-matching dress and shirt product title. The attached product image and attached size chart were used as authoritative sizing and styling evidence per the canonical workflow. The supplier URL is intentionally redacted from repo artifacts and Shopify product data.",
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
        "- Boy and father shirt rows use the chart's shirt length, chest, sleeve, height guidance, and weight guidance; shorts columns are intentionally excluded.",
        "- Boy and father shirt hip/waist values are derived from chest because the source omits shirt hip and waist.",
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
        {"name": "Type", "values": [{"name": value} for value in ["Dress", "Shirt"]]},
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
