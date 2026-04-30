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

HANDLE = "french-garden-mommy-and-me-set"
TITLE = "French Garden Mommy and Me Set - Dress & Cardigan"
SEO_TITLE = "French Garden Mommy and Me Set | Dress Like Mommy"
SEO_DESCRIPTION = "Ivory floral mommy-and-me dress and cardigan pieces for mom + daughter. Fit chart supports Child 1-2Y-10Y and Mother S-L."
PRINT_NAME = "French Garden"
SHORTCODE = "FGDN"
COLOR_TOKEN = "GARDEN"
COLOR_NAME = "Ivory Floral"
LISTING_MODE = "Mommy and Me"
CATEGORY = "Sets"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
VENDOR_URL = "https://detail.1688.com/offer/1045719394654.html"
VENDOR = "dresslikemommy.com"
CHILD_PRICE = "31.99"
ADULT_PRICE = "36.99"
CHILD_COMPARE = "36.99"
ADULT_COMPARE = "42.99"
PRICE_SOURCE = "nearby mixed-piece family set pattern (lavender-hydrangea-family-matching-set)"

SCRIPT_PATH = ROOT / "ops/scripts/create-fgdn-french-garden-mommy-and-me-set.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SOURCE_CHART = ROOT / "ops/listings/source-size-chart-french-garden-mommy-and-me-set.png"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

SIZE_METAOBJECT_MAP = {
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
}

SIZE_CHART: list[dict[str, Any]] = [
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":54,"hip_cm":58,"waist_cm":54,"length_cm":54,"skirt_cm":54,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":58,"hip_cm":62,"waist_cm":58,"length_cm":60,"skirt_cm":60,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":66,"skirt_cm":66,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":72,"skirt_cm":72,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":78,"skirt_cm":78,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":84,"skirt_cm":84,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":90,"skirt_cm":90,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":95,"skirt_cm":95,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"47.5-57.5 kg","height":"-","chest_cm":82,"hip_cm":88,"waist_cm":80,"length_cm":106,"skirt_cm":106,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"58-62.5 kg","height":"-","chest_cm":86,"hip_cm":92,"waist_cm":84,"length_cm":107,"skirt_cm":107,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"63-69.5 kg","height":"-","chest_cm":90,"hip_cm":96,"waist_cm":88,"length_cm":108,"skirt_cm":108,"sleeve_cm":0,"pant_cm":0,"shoulder_cm":0},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":60,"hip_cm":64,"waist_cm":60,"length_cm":32,"skirt_cm":0,"sleeve_cm":35,"pant_cm":0,"shoulder_cm":25},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":64,"hip_cm":68,"waist_cm":64,"length_cm":34,"skirt_cm":0,"sleeve_cm":37,"pant_cm":0,"shoulder_cm":26},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":68,"hip_cm":72,"waist_cm":68,"length_cm":36,"skirt_cm":0,"sleeve_cm":39,"pant_cm":0,"shoulder_cm":27},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":38,"skirt_cm":0,"sleeve_cm":41,"pant_cm":0,"shoulder_cm":28},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":41,"skirt_cm":0,"sleeve_cm":44,"pant_cm":0,"shoulder_cm":29},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":80,"hip_cm":84,"waist_cm":80,"length_cm":44,"skirt_cm":0,"sleeve_cm":47,"pant_cm":0,"shoulder_cm":30},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":47,"skirt_cm":0,"sleeve_cm":50,"pant_cm":0,"shoulder_cm":31},
    {"audience":"child","role":"Girl Cardigan","garment":"Cardigan","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":50,"skirt_cm":0,"sleeve_cm":53,"pant_cm":0,"shoulder_cm":32},
    {"audience":"mother","role":"Mother Cardigan","garment":"Cardigan","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"45-55 kg","height":"-","chest_cm":92,"hip_cm":92,"waist_cm":80,"length_cm":48,"skirt_cm":0,"sleeve_cm":57,"pant_cm":0,"shoulder_cm":33},
    {"audience":"mother","role":"Mother Cardigan","garment":"Cardigan","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"55.5-65 kg","height":"-","chest_cm":98,"hip_cm":98,"waist_cm":86,"length_cm":51,"skirt_cm":0,"sleeve_cm":59,"pant_cm":0,"shoulder_cm":35},
]

ROLE_TOKENS = {
    "Girl Dress": ("GRL", "DRS"),
    "Mother Dress": ("MOM", "DRS"),
    "Girl Cardigan": ("GRL", "CDG"),
    "Mother Cardigan": ("MOM", "CDG"),
}

SIZE_TOKENS = {
    "Child 1-2 Years": "KID12Y",
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
    "Mother L": "L",
}


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
    return str(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def compare_at(price: str) -> str:
    value = Decimal(price) * Decimal("1.15")
    dollars = int(math.floor(float(value)))
    candidate = Decimal(dollars) + Decimal("0.99")
    if candidate < value:
        candidate += Decimal("1.00")
    return money(candidate)


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def format_num(value: float | int | str | Decimal) -> str:
    number = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if number == number.to_integral():
        return str(int(number))
    return str(number).rstrip("0").rstrip(".")


def cm_in(value: Any) -> str:
    if value in (None, "", "-", 0, 0.0):
        return "-"
    number = Decimal(str(value))
    return f"{format_num(number)} cm / {format_num(number / Decimal('2.54'))} in"


def metric_range(value: str, source_unit: str, target_unit: str, factor: Decimal) -> str:
    if not value or value == "-":
        return "-"
    numbers = [Decimal(n) for n in re.findall(r"\d+(?:\.\d+)?", value)]
    if len(numbers) >= 2:
        left, right = numbers[0], numbers[1]
        return (
            f"{format_num(left)}-{format_num(right)} {source_unit} / "
            f"{format_num(left * factor)}-{format_num(right * factor)} {target_unit}"
        )
    return value


def price_for(row: dict[str, Any]) -> str:
    return ADULT_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict[str, Any]) -> str:
    role_token, garment_token = ROLE_TOKENS[row["role"]]
    return f"DLM-{SHORTCODE}-{role_token}-{garment_token}-{SIZE_TOKENS[row['picker_label']]}-{COLOR_TOKEN}"


def build_derived() -> dict[str, Any]:
    required = [
        "audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix",
        "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm",
        "sleeve_cm", "skirt_cm", "pant_cm",
    ]
    errors: list[str] = []
    seen_role_picker: set[tuple[str, str]] = set()
    seen_skus: set[str] = set()
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('role')} {row.get('vendor_label')} missing {', '.join(missing)}")
        pair = (row["role"], row["picker_label"])
        if pair in seen_role_picker:
            errors.append(f"duplicate role/picker pair: {pair}")
        seen_role_picker.add(pair)
        if row["role"] not in ROLE_TOKENS:
            errors.append(f"missing role token for {row['role']}")
        if row["picker_label"] not in SIZE_TOKENS:
            errors.append(f"missing size token for {row['picker_label']}")
        if row["picker_label"] not in SIZE_METAOBJECT_MAP:
            errors.append(f"missing size metaobject for {row['picker_label']}")
        sku = sku_for(row)
        if sku in seen_skus:
            errors.append(f"duplicate SKU: {sku}")
        seen_skus.add(sku)

    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"SEO title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"SEO description too long: {len(SEO_DESCRIPTION)}")
    if CHILD_COMPARE != compare_at(CHILD_PRICE) or ADULT_COMPARE != compare_at(ADULT_PRICE):
        errors.append("compare-at prices do not match prompt rule")
    if errors:
        raise SystemExit("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))

    type_values: list[str] = []
    size_values: list[str] = []
    for row in SIZE_CHART:
        if row["garment"] not in type_values:
            type_values.append(row["garment"])
        if row["picker_label"] not in size_values:
            size_values.append(row["picker_label"])

    option_axes = [
        {"name": "Type", "values": type_values},
        {"name": "Size", "values": size_values},
    ]
    product_options = [
        {"name": axis["name"], "values": [{"name": value} for value in axis["values"]]}
        for axis in option_axes
    ]

    variants: list[dict[str, Any]] = []
    recap: list[dict[str, Any]] = []
    expected_option_pairs: list[list[str]] = []
    for row in SIZE_CHART:
        price = price_for(row)
        compare = ADULT_COMPARE if row["audience"] == "mother" else CHILD_COMPARE
        sku = sku_for(row)
        option_values = [row["garment"], row["picker_label"]]
        variants.append({
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {
                "sku": sku,
                "tracked": True,
                "requiresShipping": True,
            },
            "optionValues": [
                {"optionName": "Type", "name": row["garment"]},
                {"optionName": "Size", "name": row["picker_label"]},
            ],
        })
        expected_option_pairs.append(option_values)
        size_gid, catalog_label = SIZE_METAOBJECT_MAP[row["picker_label"]]
        recap.append({
            **row,
            "sku": sku,
            "price": price,
            "compare_at_price": compare,
            "cost": cost_for(price),
            "shopify_size_gid": size_gid,
            "catalog_label": catalog_label,
            "option1_value": option_values[0],
            "option2_value": option_values[1],
        })

    tags = list(dict.fromkeys([
        "Mommy and Me",
        "Sets",
        "Matching Family Sets",
        "Matching Family Set",
        "Girl Dress",
        "Mother Dress",
        "Girl Cardigan",
        "Mother Cardigan",
        "Dress",
        "Cardigan",
        "Summer Cardigan",
        "Sundress",
        "Floral Dress",
        "Ivory Floral",
        "French Garden",
        "Ivory",
        "Cream",
        "Purple Floral",
        "Summer",
        "Vacation",
        "Resort",
        "Child 1-2yr",
        "Child 2-3yr",
        "Child 4-5yr",
        "Child 6-8yr",
        "Child 9-10yr",
        "Mom Size S",
        "Mom Size M",
        "Mom Size L",
        VENDOR_URL,
    ]))

    return {
        "product_options": product_options,
        "option_axes": option_axes,
        "option_names": ["Type", "Size"],
        "expected_variant_option_pairs": expected_option_pairs,
        "variants": variants,
        "recap": recap,
        "row_count": len(SIZE_CHART),
        "derived_skus_sorted": sorted(v["inventoryItem"]["sku"] for v in variants),
        "shopify_size_refs": [r["shopify_size_gid"] for r in recap],
        "tags": tags,
        "size_phrase": "Child 1-2 Years through Child 9-10 Years, Mother S-L for dress, and Mother S-M for cardigan",
    }


def table_for(garment: str, rows: list[dict[str, Any]]) -> str:
    detail_col = "Skirt Length (cm/in)" if garment == "Dress" else "Sleeve Length (cm/in)"
    body_rows = []
    for row in rows:
        detail_value = row["skirt_cm"] if garment == "Dress" else row["sleeve_cm"]
        age = row["age"] if row["audience"] == "child" else "-"
        body_rows.append(
            "<tr>"
            f"<td>{html.escape(row['picker_label'])}</td>"
            f"<td>{html.escape(age)}</td>"
            f"<td>{html.escape(metric_range(row['weight'], 'kg', 'lbs', Decimal('2.20462')))}</td>"
            f"<td>{html.escape(metric_range(row['height'], 'cm', 'in', Decimal('0.3937007874')))}</td>"
            f"<td>{cm_in(row['chest_cm'])}</td>"
            f"<td>{cm_in(detail_value)}</td>"
            f"<td>{cm_in(row['pant_cm'])}</td>"
            f"<td>{cm_in(row['hip_cm'])}</td>"
            f"<td>{cm_in(row['waist_cm'])}</td>"
            f"<td>{cm_in(row['length_cm'])}</td>"
            "</tr>"
        )
    return "\n".join([
        f"<h3>Size Chart - {html.escape(garment)}</h3>",
        "<table>",
        "<thead><tr>",
        "<th>Size</th>",
        "<th>Age</th>",
        "<th>Weight (kg/lbs)</th>",
        "<th>Height (cm/in)</th>",
        "<th>Chest/Bust (cm/in)</th>",
        f"<th>{detail_col}</th>",
        "<th>Pant/Short or - (cm/in)</th>",
        "<th>Hip (cm/in)</th>",
        "<th>Waist (cm/in)</th>",
        "<th>Garment Length (cm/in)</th>",
        "</tr></thead>",
        "<tbody>",
        *body_rows,
        "</tbody>",
        "</table>",
    ])


def build_body() -> str:
    dress_rows = [row for row in SIZE_CHART if row["garment"] == "Dress"]
    cardigan_rows = [row for row in SIZE_CHART if row["garment"] == "Cardigan"]
    return "\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven fabric with a soft, airy feel; exact fiber composition should be confirmed before publication.</li>",
        "<li><strong>Family story:</strong> A photo-ready mom and daughter look with matching floral dresses and an optional breezy cardigan layer.</li>",
        "<li><strong>Print:</strong> French Garden pairs an ivory base with soft pastel floral accents for a gentle summer look.</li>",
        "<li><strong>Design details:</strong> Tiered strap dress with a relaxed shape plus a long-sleeve open cardigan for light coverage.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and use a cool iron inside-out if needed.</li>",
        "<li><strong>Size range:</strong> Girls Child 1-2 Years to Child 9-10 Years; Mother S-L for the dress and Mother S-M for the cardigan.</li>",
        "</ul>",
        "",
        table_for("Dress", dress_rows),
        "",
        table_for("Cardigan", cardigan_rows),
        "",
        "<p>The French Garden Mommy and Me Set is made for soft summer days, family photos, and easy mother-daughter dressing. Choose the floral strap dress for the main matching moment, then add the lightweight cardigan when you want a little extra coverage without losing the airy look.</p>",
        "",
        "<p>The ivory floral palette keeps the outfit sweet and wearable, while the tiered dress shape and open cardigan layer give each size a relaxed, graceful fit. Each garment is selected separately by Type and Size so families can build the exact matching look they need.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Two coordinated pieces:</strong> Select the Dress or Cardigan by Type for mom and daughter.</li>",
        "<li><strong>Soft floral look:</strong> Ivory base with delicate pastel garden florals.</li>",
        "<li><strong>Layer-ready styling:</strong> Wear the dress alone or pair it with the matching cardigan.</li>",
        "<li><strong>Family photo friendly:</strong> Gentle colors and flowing lines work beautifully for summer portraits.</li>",
        "<li><strong>Chart-backed sizing:</strong> Every variant comes from the supplied size chart.</li>",
        "</ul>",
        "",
        "<p>Choose Dress or Cardigan, then pick each size to create a French Garden matching look for mom and mini.</p>",
    ])


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def ensure_dirs() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def fetch_existing() -> dict[str, Any] | None:
    data = gql("""
      query Existing($handle: String!) {
        productByHandle(handle: $handle) {
          id
          handle
          options { id name position values optionValues { id name hasVariants } }
          variants(first: 100) {
            nodes {
              id
              sku
              price
              compareAtPrice
              inventoryPolicy
              selectedOptions { name value }
              inventoryItem { id tracked requiresShipping unitCost { amount currencyCode } }
            }
          }
        }
      }
    """, {"handle": HANDLE})
    return data["data"]["productByHandle"]


def ensure_product(derived: dict[str, Any], body_html: str) -> tuple[str, bool]:
    existing = fetch_existing()
    create_new = existing is None
    if create_new:
        data = gql("""
          mutation ProductCreate($input: ProductInput!) {
            productCreate(input: $input) {
              product { id handle title }
              userErrors { field message }
            }
          }
        """, {"input": {
            "handle": HANDLE,
            "title": TITLE,
            "descriptionHtml": body_html,
            "vendor": VENDOR,
            "productType": PRODUCT_TYPE,
            "tags": derived["tags"],
            "status": "DRAFT",
            "category": TAXONOMY_GID,
            "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
            "productOptions": derived["product_options"],
        }})
        require_no_user_errors(data, ["data", "productCreate", "userErrors"])
        product_id = data["data"]["productCreate"]["product"]["id"]
    else:
        product_id = existing["id"]

    data = gql("""
      mutation ProductUpdate($product: ProductUpdateInput!) {
        productUpdate(product: $product) {
          product { id handle title }
          userErrors { field message }
        }
      }
    """, {"product": {
        "id": product_id,
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body_html,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": derived["tags"],
        "status": "DRAFT",
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }})
    require_no_user_errors(data, ["data", "productUpdate", "userErrors"])
    return product_id, create_new


def sync_variants(product_id: str, create_new: bool, derived: dict[str, Any]) -> None:
    existing = fetch_existing()
    if existing is None:
        raise RuntimeError("product missing after create")
    live_variants = existing["variants"]["nodes"]
    live_skus = sorted(v["sku"] for v in live_variants if v.get("sku"))
    derived_skus = derived["derived_skus_sorted"]
    should_create = create_new or not live_skus

    if should_create:
        data = gql("""
          mutation BulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
            productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
              productVariants { id sku }
              userErrors { field message }
            }
          }
        """, {
            "productId": product_id,
            "variants": derived["variants"],
            "strategy": "REMOVE_STANDALONE_VARIANT",
        })
        require_no_user_errors(data, ["data", "productVariantsBulkCreate", "userErrors"])
    else:
        if live_skus != derived_skus:
            raise RuntimeError(
                "existing product has unexpected SKUs; refusing destructive variant rewrite\n"
                f"live={live_skus}\nderived={derived_skus}"
            )
        id_by_sku = {variant["sku"]: variant["id"] for variant in live_variants}
        updates = []
        for variant in derived["variants"]:
            sku = variant["inventoryItem"]["sku"]
            updates.append({
                "id": id_by_sku[sku],
                "price": variant["price"],
                "compareAtPrice": variant["compareAtPrice"],
                "inventoryPolicy": "DENY",
                "inventoryItem": variant["inventoryItem"],
                "optionValues": variant["optionValues"],
            })
        data = gql("""
          mutation BulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
            productVariantsBulkUpdate(productId: $productId, variants: $variants) {
              productVariants { id sku }
              userErrors { field message }
            }
          }
        """, {"productId": product_id, "variants": updates})
        require_no_user_errors(data, ["data", "productVariantsBulkUpdate", "userErrors"])

    time.sleep(1)
    existing = fetch_existing()
    item_by_sku = {
        variant["sku"]: variant["inventoryItem"]["id"]
        for variant in existing["variants"]["nodes"]
    }
    for variant in derived["variants"]:
        sku = variant["inventoryItem"]["sku"]
        data = gql("""
          mutation InventoryItemUpdate($id: ID!, $input: InventoryItemInput!) {
            inventoryItemUpdate(id: $id, input: $input) {
              inventoryItem { id unitCost { amount currencyCode } tracked }
              userErrors { field message }
            }
          }
        """, {"id": item_by_sku[sku], "input": {"cost": cost_for(variant["price"]), "tracked": True}})
        require_no_user_errors(data, ["data", "inventoryItemUpdate", "userErrors"])


def set_metafields(product_id: str, derived: dict[str, Any]) -> list[dict[str, str]]:
    size_refs = json.dumps(list(dict.fromkeys(derived["shopify_size_refs"])))
    metafields = [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Ivory Floral"},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Layered Summer Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress & Cardigan"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "French Garden"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Cardigan"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": size_refs},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]
    for start in range(0, len(metafields), 25):
        data = gql("""
          mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
            metafieldsSet(metafields: $metafields) {
              metafields { namespace key type value }
              userErrors { field message }
            }
          }
        """, {"metafields": metafields[start:start + 25]})
        require_no_user_errors(data, ["data", "metafieldsSet", "userErrors"])
    return [{k: str(m[k]) for k in ("namespace", "key", "type", "value")} for m in metafields]


def attach_media(product_id: str) -> None:
    data = gql("""
      query Media($id: ID!) {
        product(id: $id) {
          media(first: 50) {
            nodes {
              ... on MediaImage { id alt image { url } }
            }
          }
        }
      }
    """, {"id": product_id})
    existing_alts = {
        node.get("alt") for node in data["data"]["product"]["media"]["nodes"] if node.get("alt")
    }
    media_files = sorted(
        path for path in UPLOAD_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        and "size-chart" not in path.name.lower()
    )
    for path in media_files:
        alt = "Mother and daughter wearing French Garden ivory floral dresses with matching cardigans."
        if alt in existing_alts:
            continue
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql("""
          mutation Staged($input: [StagedUploadInput!]!) {
            stagedUploadsCreate(input: $input) {
              stagedTargets { url resourceUrl parameters { name value } }
              userErrors { field message }
            }
          }
        """, {"input": [{"filename": path.name, "mimeType": mime_type, "resource": "IMAGE", "httpMethod": "POST"}]})
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        args = ["curl", "-sS", "-X", "POST", target["url"]]
        for param in target["parameters"]:
            args.extend(["-F", f"{param['name']}={param['value']}"])
        args.extend(["-F", f"file=@{path}"])
        subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
        created = gql("""
          mutation CreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
            productCreateMedia(productId: $productId, media: $media) {
              media { ... on MediaImage { id alt } }
              userErrors { field message }
            }
          }
        """, {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]})
        require_no_user_errors(created, ["data", "productCreateMedia", "userErrors"])


def verify_product(product_id: str) -> dict[str, Any]:
    data = gql("""
      query Verify($id: ID!) {
        product(id: $id) {
          id
          title
          handle
          status
          publishedAt
          onlineStoreUrl
          descriptionHtml
          tags
          seo { title description }
          category { id fullName }
          options { name position values optionValues { id name hasVariants } }
          variants(first: 100) {
            nodes {
              id
              sku
              title
              price
              compareAtPrice
              inventoryPolicy
              selectedOptions { name value }
              inventoryItem { id tracked requiresShipping unitCost { amount currencyCode } }
            }
          }
          media(first: 50) {
            nodes { ... on MediaImage { alt image { url } } }
          }
          collections(first: 50) {
            nodes { title handle }
          }
          metafields(first: 100) {
            nodes { namespace key type value }
          }
          resourcePublicationsV2(first: 20) {
            nodes { isPublished publishDate publication { id name } }
          }
        }
      }
    """, {"id": product_id})
    write_json(VERIFY_JSON_OUT, data)
    return data


def validate_variant_model(derived: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart_path = tmpdir / "size-chart.json"
        derived_path = tmpdir / "derived.json"
        evidence_path = tmpdir / "vendor-evidence.json"
        write_json(chart_path, SIZE_CHART)
        write_json(derived_path, derived)
        write_json(evidence_path, {
            "title": "French Garden mommy and me strap dress and sun-protection cardigan",
            "raw_detail_text": "26B076 strap dress; 26B097 sun-protection cardigan; dress cardigan skirt shirt top",
            "notes": "Attached chart contains separate dress and cardigan tables, so options are Type x Size.",
        })
        subprocess.run([
            "python3",
            str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart_path),
            "--derived", str(derived_path),
            "--vendor-evidence", str(evidence_path),
            "--primary-category", CATEGORY,
            "--tags", ",".join(derived["tags"]),
        ], check=True)


def write_csv(derived: dict[str, Any], product: dict[str, Any]) -> None:
    with CSV_HEADER_SOURCE.open(newline="") as fh:
        header = next(csv.reader(fh))
    rows = []
    for recap in derived["recap"]:
        row = {name: "" for name in header}

        def put(field: str, value: Any) -> None:
            if field in row:
                row[field] = str(value)

        put("Handle", HANDLE)
        put("Title", TITLE)
        put("Body (HTML)", product["descriptionHtml"])
        put("Vendor", VENDOR)
        put("Product Category", EXPECTED_TAXONOMY_FULL_NAME)
        put("Type", PRODUCT_TYPE)
        put("Tags", ", ".join(product["tags"]))
        put("Published", "FALSE")
        put("Option1 Name", "Type")
        put("Option1 Value", recap["option1_value"])
        put("Option2 Name", "Size")
        put("Option2 Value", recap["option2_value"])
        put("Variant SKU", recap["sku"])
        put("Variant Grams", "0")
        put("Variant Inventory Tracker", "shopify")
        put("Variant Inventory Policy", "deny")
        put("Variant Fulfillment Service", "manual")
        put("Variant Price", recap["price"])
        put("Variant Compare At Price", recap["compare_at_price"])
        put("Variant Requires Shipping", "TRUE")
        put("Variant Taxable", "TRUE")
        put("SEO Title", SEO_TITLE)
        put("SEO Description", SEO_DESCRIPTION)
        put("Google Shopping / Gender", "female")
        put("Google Shopping / Age Group", "adult")
        put("Google Shopping / Condition", "new")
        put("Google Shopping / Custom Product", "FALSE")
        put("Google Shopping / Custom Label 0", "Mommy and Me")
        put("Google Shopping / Custom Label 1", "French Garden")
        put("Google Shopping / Custom Label 2", "Summer")
        put("Google Shopping / Custom Label 3", "Dress & Cardigan")
        put("Google Shopping / Custom Label 4", "Two-Role Matching")
        put("Category1 (product.metafields.custom.category1)", "Mommy and Me")
        put("Pattern (product.metafields.custom.pattern)", "Ivory Floral")
        put("Style (product.metafields.custom.style)", "Layered Summer Set")
        put("SubCategory (product.metafields.custom.subcategory)", "Set")
        put("SubCategory2 (product.metafields.custom.subcategory2)", "Summer Mommy and Me Set")
        put("Type (product.metafields.custom.type)", "Dress & Cardigan")
        put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
        put("Age group (product.metafields.shopify.age-group)", "Toddlers, Kids, Adults")
        put("Color (product.metafields.shopify.color-pattern)", "White")
        put("Size (product.metafields.shopify.size)", ", ".join(dict.fromkeys(r["picker_label"] for r in derived["recap"])))
        put("Target Gender (product.metafields.shopify.target-gender)", "Female")
        put("Cost per item", recap["cost"])
        put("Status", "draft")
        rows.append(row)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing_md(derived: dict[str, Any], verify: dict[str, Any], metafields_written: list[dict[str, str]]) -> None:
    product = verify["data"]["product"]
    variants = product["variants"]["nodes"]
    spec_by_sku = {row["sku"]: row for row in derived["recap"]}
    option_names = derived["option_names"]
    live_pairs = {
        tuple({opt["name"]: opt["value"] for opt in variant["selectedOptions"]}.get(name) for name in option_names)
        for variant in variants
    }
    expected_pairs = {tuple(pair) for pair in derived["expected_variant_option_pairs"]}
    tables = re.findall(r"<table>(.*?)</table>", product["descriptionHtml"], re.S)
    table_header_counts = [len(re.findall(r"<th>", table)) for table in tables]
    table_row_counts = [len(re.findall(r"<tr>", re.search(r"<tbody>(.*?)</tbody>", table, re.S).group(1))) for table in tables]
    expected_row_counts = [sum(1 for row in SIZE_CHART if row["garment"] == garment) for garment in ("Dress", "Cardigan")]
    live_skus = sorted(v["sku"] for v in variants)
    published = [node for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    metafield_keys = {(node["namespace"], node["key"]) for node in product["metafields"]["nodes"]}

    price_rows = []
    cost_ok = True
    for variant in variants:
        spec = spec_by_sku[variant["sku"]]
        unit_cost = (variant["inventoryItem"]["unitCost"] or {}).get("amount")
        expected_cost = spec["cost"]
        unit_cost_norm = money(unit_cost) if unit_cost is not None else None
        row_ok = (
            variant["price"] == spec["price"]
            and variant["compareAtPrice"] == spec["compare_at_price"]
            and variant["inventoryPolicy"] == "DENY"
            and variant["inventoryItem"]["tracked"] is True
            and variant["inventoryItem"]["requiresShipping"] is True
            and unit_cost_norm == expected_cost
        )
        cost_ok = cost_ok and unit_cost_norm == expected_cost
        price_rows.append((variant["sku"], variant["price"], variant["compareAtPrice"], unit_cost_norm, expected_cost, row_ok))

    required_meta = {
        ("custom", "category1"),
        ("custom", "subcategory"),
        ("custom", "subcategory2"),
        ("custom", "pattern"),
        ("custom", "style"),
        ("custom", "type"),
        ("mm-google-shopping", "custom_product"),
        ("mm-google-shopping", "gender"),
        ("mm-google-shopping", "age_group"),
        ("mm-google-shopping", "condition"),
        ("mm-google-shopping", "custom_label_0"),
        ("mm-google-shopping", "custom_label_1"),
        ("mm-google-shopping", "custom_label_2"),
        ("mm-google-shopping", "custom_label_3"),
        ("mm-google-shopping", "custom_label_4"),
        ("shopify", "age-group"),
        ("shopify", "care-instructions"),
        ("shopify", "color-pattern"),
        ("shopify", "size"),
        ("shopify", "target-gender"),
        ("global", "title_tag"),
        ("global", "description_tag"),
    }
    checks = [
        ("Title <= 70", len(product["title"]) <= 70, len(product["title"])),
        ("SEO title <= 60", len(product["seo"]["title"]) <= 60, len(product["seo"]["title"])),
        ("SEO description <= 155", len(product["seo"]["description"]) <= 155, len(product["seo"]["description"])),
        ("Variant count matches SIZE_CHART", len(variants) == len(SIZE_CHART), f"{len(variants)} vs {len(SIZE_CHART)}"),
        ("Live SKUs match derived SKUs", live_skus == derived["derived_skus_sorted"], len(live_skus)),
        ("Every Type x Size combination exists", live_pairs == expected_pairs, len(live_pairs)),
        ("Each size table has 10 headers", table_header_counts == [10, 10], table_header_counts),
        ("Size table row counts match SIZE_CHART", table_row_counts == expected_row_counts, table_row_counts),
        ("Waist populated for every row", all(row["waist_cm"] for row in SIZE_CHART), "all rows"),
        ("Product status is DRAFT", product["status"] == "DRAFT", product["status"]),
        ("publishedAt is null", product["publishedAt"] is None, product["publishedAt"]),
        ("No sales-channel publications are live", len(published) == 0, published),
        ("Taxonomy resolves to expected leaf", product["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, product["category"]["fullName"]),
        ("Applicable metafields are written", required_meta.issubset(metafield_keys), sorted(required_meta - metafield_keys)),
        ("Cost per item equals 50 percent", cost_ok, "paid_eligible=true" if cost_ok else "paid_eligible=false"),
    ]

    product_id_num = product["id"].split("/")[-1]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{product_id_num}",
        f"- **Live:** {product['onlineStoreUrl'] or 'not published'}",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product['id']}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | auto -> Mommy and Me |",
        "| PRIMARY_CATEGORY | auto -> Sets |",
        "| DESIGNS_TO_LIST | auto -> French Garden dress and cardigan |",
        "| EXCLUDE_ITEMS | none |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | auto -> `{SHORTCODE}` |",
        f"| COLOR_TOKEN | auto -> `{COLOR_TOKEN}` |",
        "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned Alibaba anti-bot punish markup, so the attached product image and attached size-chart image were used as the authoritative evidence per the canonical workflow.",
        "",
        "## Pricing",
        f"Prices use {PRICE_SOURCE}: child rows at `{CHILD_PRICE}` and mother rows at `{ADULT_PRICE}`. Cost per item is exactly 50 percent: `{cost_for(CHILD_PRICE)}` child and `{cost_for(ADULT_PRICE)}` mother.",
        "",
        "## Derivations",
        "- The chart has separate item codes/tables for the strap dress and cardigan, so variants use `Type x Size` instead of a collapsed set SKU.",
        "- The source chest columns are half-chest style measurements, so they were doubled before writing `chest_cm`.",
        "- Dress hip/waist and cardigan hip/waist were derived from the canonical prompt rules because the vendor chart omits those fields.",
        "- Adult recommended height is blank in the vendor chart and is rendered as `-`; adult sizing is anchored to vendor weight rows and the attached fit report.",
        "- A garment token (`DRS` or `CDG`) was added to SKUs because the same role and size can exist for both Dress and Cardigan in this Type listing.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{product['title']}` | {len(product['title'])} |",
        f"| SEO title | `{product['seo']['title']}` | {len(product['seo']['title'])} |",
        f"| SEO description | `{product['seo']['description']}` | {len(product['seo']['description'])} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for recap in derived["recap"]:
        lines.append(
            f"| {recap['role']} | {recap['vendor_label']} | {recap['picker_label']} | {recap['garment']} | "
            f"`{recap['sku']}` | {recap['price']} | {recap['cost']} | `{recap['shopify_size_gid']}` ({recap['catalog_label']}) |"
        )
    lines.extend([
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ])
    for label, ok, detail in checks:
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines.extend([
        "",
        "## Price Parity",
        "| SKU | Live Price | Live Compare | Live Cost | Expected Cost | Match |",
        "|---|---|---|---|---|---|",
    ])
    for sku, price, cmp_price, unit_cost, expected_cost, ok in price_rows:
        lines.append(f"| `{sku}` | {price} | {cmp_price} | {unit_cost} | {expected_cost} | {'PASS' if ok else 'FAIL'} |")
    lines.extend([
        "",
        "## Smart Collections",
    ])
    collections = product["collections"]["nodes"]
    if collections:
        for collection in collections:
            lines.append(f"- {collection['title']} (`/{collection['handle']}`)")
    else:
        lines.append("- Collection indexing may wait until publication because the product is an unpublished draft.")
    lines.extend([
        "",
        "## Metafields Written",
    ])
    for node in sorted(product["metafields"]["nodes"], key=lambda item: (item["namespace"], item["key"])):
        if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}:
            value = node["value"]
            if len(value) > 90:
                value = value[:87] + "..."
            lines.append(f"- `{node['namespace']}.{node['key']}` ({node['type']}): `{value}`")
    lines.extend([
        "",
        "## Metafields Skipped",
        "- `shopify.fabric`: exact fiber is not confirmed by the attached evidence.",
        "- `shopify.dress-occasion`, `shopify.dress-style`, `shopify.neckline`, `shopify.skirt-dress-length-type`, `shopify.sleeve-length-type`, and `shopify.top-length-type`: product mixes Dress and Cardigan, so one product-level garment attribute would be misleading.",
        "- `shopify.clothing-features`: no supported, specific clothing-feature metaobject was needed for the supplied evidence.",
        "",
        "## Publication",
        "- Draft only. The runner did not call `publishablePublish`, `publishedAt` is null, and no sales-channel publication is live.",
        "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition before publishing.",
        "- Inventory quantities and per-variant grams still need operator stock values.",
        "- The product image is vendor/lifestyle evidence; replace or retouch if brand standards require cleaner publication media.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SOURCE_CHART}`",
        f"- `{UPLOAD_DIR}`",
    ])
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    failed = [label for label, ok, _ in checks if not ok]
    if failed:
        raise RuntimeError("verification failed: " + ", ".join(failed))


def main() -> None:
    ensure_dirs()
    derived = build_derived()
    body_html = build_body()
    validate_variant_model(derived)
    write_json(SIZE_CHART_OUT, SIZE_CHART)
    BODY_HTML_OUT.write_text(body_html + "\n", encoding="utf-8")
    product_id, create_new = ensure_product(derived, body_html)
    sync_variants(product_id, create_new, derived)
    metafields_written = set_metafields(product_id, derived)
    attach_media(product_id)
    time.sleep(2)
    verify = verify_product(product_id)
    write_csv(derived, verify["data"]["product"])
    write_listing_md(derived, verify, metafields_written)
    print(f"Runner complete: {SCRIPT_PATH}")
    print(f"Admin: https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}")
    print(f"Listing: {LISTING_MD}")
    print(f"Verify: {VERIFY_JSON_OUT}")


if __name__ == "__main__":
    main()
PY
