#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
DEFAULT_PYTHON="/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
PYTHON_BIN="${DLM_PYTHON_BIN:-$DEFAULT_PYTHON}"
TRANSLATION_PYTHON="${DLM_TRANSLATION_PYTHON:-/usr/bin/python3}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi
if [[ ! -x "$TRANSLATION_PYTHON" ]]; then
  echo "Translation Python runtime not executable: $TRANSLATION_PYTHON" >&2
  exit 1
fi
export SHOPIFY_STORE_DOMAIN SHOPIFY_ADMIN_ACCESS_TOKEN PYTHON_BIN

"$PYTHON_BIN" - <<'PY'
from __future__ import annotations

import csv
import hashlib
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
import uuid
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]
PYTHON_BIN = Path(os.environ["PYTHON_BIN"])
PREFLIGHT_ONLY = os.environ.get("DLM_PREFLIGHT_ONLY", "0") == "1"

HANDLE = "rosewater-ombre-mommy-and-me-dresses"
TITLE = "Rosewater Ombre Mommy and Me Dresses — Pleated Maxi"
SEO_TITLE = "Pink Ombre Mommy and Me Maxi Dresses | Dress Like Mommy"
SEO_DESCRIPTION = "Pleated pink ombre maxi dresses for mom + daughter. Chart-backed sizes Child 2Y–10Y and Mother S–2XL for beach days and family photos."
PRINT_NAME = "Rosewater Ombre"
COLOR_NAME = "Pink Ombre"
SHORTCODE = "RSOM"
COLOR_TOKEN = "PINK"
OFFER_ID = "815482441394"
LISTING_MODE = "Mommy and Me"
PRIMARY_CATEGORY = "Dresses"
PRODUCT_TYPE = "Matching Family Dresses"
VENDOR = "dresslikemommy.com"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-4"
EXPECTED_TAXONOMY = "Apparel & Accessories > Clothing > Dresses"
CHILD_PRICE = "31.99"
MOTHER_PRICE = "34.99"
CHILD_COMPARE = "36.99"
MOTHER_COMPARE = "40.99"
EXPECTED_IMAGE_SHA256 = "2e6ecd6cc9a108fecb49d1bf9bcf603031ef7b92111f371ef96d24d2cbc520ba"
EXPECTED_CHART_SHA256 = "b8b2a1837f9be7f12de2143acf79e8d37f42f44df55bc28e958d962797b97b52"

SCRIPT_PATH = ROOT / "ops/scripts/create-rsom-rosewater-ombre-mommy-and-me-dresses.sh"
UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / "01-rosewater-ombre-mommy-and-me-dresses.png"
SOURCE_CHART = UPLOAD_DIR / "source-size-chart-rosewater-ombre-mommy-and-me-dresses.png"
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
PREFLIGHT_JSON_OUT = ROOT / "ops/listings" / f"preflight-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"
EXPECTED_MEDIA_ALT = "Mother and daughter wearing pink-to-white ombre pleated matching dresses outdoors."

SIZE_METAOBJECTS = {
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
}

AGE_GROUP_METAOBJECTS = {
    "gid://shopify/Metaobject/128116523105": "Kids",
    "gid://shopify/Metaobject/128116490337": "Adults",
}
COLOR_PATTERN_METAOBJECTS = {
    "gid://shopify/Metaobject/69963645025": "Pink",
    "gid://shopify/Metaobject/69639733345": "White",
}
TARGET_GENDER_METAOBJECTS = {
    "gid://shopify/Metaobject/129971617889": "Female",
}
DRESS_OCCASION_METAOBJECTS = {
    "gid://shopify/Metaobject/69622169697": "Beach outings",
    "gid://shopify/Metaobject/69622202465": "family vacations",
}
DRESS_STYLE_METAOBJECTS = {
    "gid://shopify/Metaobject/130282520673": "A-line",
}
DRESS_LENGTH_METAOBJECTS = {
    "gid://shopify/Metaobject/69622300769": "Maxi",
}
SLEEVE_LENGTH_METAOBJECTS = {
    "gid://shopify/Metaobject/69622268001": "Sleeveless",
}

SIZE_CHART: list[dict[str, Any]] = [
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90/2码","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"7.5-11","height":"80-90","chest_cm":50,"hip_cm":54,"waist_cm":50,"length_cm":54,"skirt_cm":54,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100/4码","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"11-15","height":"90-100","chest_cm":54,"hip_cm":58,"waist_cm":54,"length_cm":59,"skirt_cm":59,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110/6码","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-19","height":"100-110","chest_cm":58,"hip_cm":62,"waist_cm":58,"length_cm":62,"skirt_cm":62,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120/8码","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19-22.5","height":"110-120","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":66,"skirt_cm":66,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130/10码","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"22.5-27.5","height":"120-130","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":70,"skirt_cm":70,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140/12码","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5","height":"130-140","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":74,"skirt_cm":74,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150/14码","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-40","height":"140-150","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":78,"skirt_cm":78,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, chest, recommended weight, and recommended height are chart values. Waist equals chest and hip equals chest plus 4 cm under the canonical child-dress rule."},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S/160","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"40-50","height":"155-160","chest_cm":"-","hip_cm":"-","waist_cm":88,"length_cm":97,"skirt_cm":97,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, waist, recommended weight, and recommended height are chart values. Chest/bust and hip are unavailable and were not guessed."},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M/165","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5","height":"155-160","chest_cm":"-","hip_cm":"-","waist_cm":92,"length_cm":102,"skirt_cm":102,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, waist, recommended weight, and recommended height are chart values. Chest/bust and hip are unavailable and were not guessed."},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L/170","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"57.5-65","height":"155-165","chest_cm":"-","hip_cm":"-","waist_cm":96,"length_cm":107,"skirt_cm":107,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, waist, recommended weight, and recommended height are chart values. Chest/bust and hip are unavailable and were not guessed."},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL/175","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"65-72.5","height":"165-170","chest_cm":"-","hip_cm":"-","waist_cm":100,"length_cm":112,"skirt_cm":112,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, waist, recommended weight, and recommended height are chart values. Chest/bust and hip are unavailable and were not guessed."},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL/180","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"72.5-80","height":"170-175","chest_cm":"-","hip_cm":"-","waist_cm":104,"length_cm":117,"skirt_cm":117,"sleeve_cm":"-","pant_cm":"-","source_note":"Dress length, waist, recommended weight, and recommended height are chart values. Chest/bust and hip are unavailable and were not guessed."},
]


def gql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            output = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode()) from exc
    if output.get("errors"):
        raise RuntimeError(json.dumps(output["errors"], indent=2))
    return output


def require_no_user_errors(output: dict[str, Any], path: list[str]) -> None:
    current: Any = output
    for key in path:
        current = current[key]
    if current:
        raise RuntimeError(json.dumps(current, indent=2))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def compare_at(price: str) -> str:
    threshold = Decimal(price) * Decimal("1.15")
    candidate = Decimal(math.floor(float(threshold))) + Decimal("0.99")
    if candidate < threshold:
        candidate += Decimal("1.00")
    return money(candidate)


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def price_for(row: dict[str, Any]) -> str:
    return MOTHER_PRICE if row["audience"] == "mother" else CHILD_PRICE


def role_token(row: dict[str, Any]) -> str:
    return "MOM" if row["audience"] == "mother" else "GRL"


def sku_for(row: dict[str, Any]) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row)}-{row['sku_suffix']}-{COLOR_TOKEN}"


def tags() -> list[str]:
    values = [
        "Mommy and Me",
        "Matching Family Dresses",
        "Matching Mommy and Me Dresses",
        "Mother Daughter Matching Dress",
        "Girl Dress",
        "Mother Dress",
        "Dresses",
        "Maxi Dresses",
        "Pleated Dress",
        "Sleeveless Dress",
        "Spaghetti Strap Dress",
        "A-Line Dress",
        "Ombre",
        "Gradient",
        "Pink Ombre",
        "Pink",
        "White",
        PRINT_NAME,
        "Beach",
        "Resort",
        "Vacation",
        "Summer",
        "Family Photos",
        "Photo Ready",
        "Child 2yr",
        "Child 3yr",
        "Child 4yr",
        "Child 5yr",
        "Child 6-7yr",
        "Child 8yr",
        "Child 9-10yr",
        "Mom Size S",
        "Mom Size M",
        "Mom Size L",
        "Mom Size XL",
        "Mom Size 2XL",
    ]
    return sorted(dict.fromkeys(values))


def fmt_num(value: Decimal | int | float | str) -> str:
    number = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if number == number.to_integral():
        return str(int(number))
    return str(number).rstrip("0").rstrip(".")


def metric_cell(value: Any, unit: str) -> str:
    if value in (None, "", "-", 0, 0.0):
        return "-"
    if isinstance(value, str) and "-" in value:
        numbers = re.findall(r"\d+(?:\.\d+)?", value)
        if len(numbers) >= 2:
            return f"{fmt_num(numbers[0])}-{fmt_num(numbers[1])} {unit}"
    return f"{fmt_num(value)} {unit}"


def build_body() -> str:
    headers = [
        "Size",
        "Age",
        "Weight (kg)",
        "Height (cm)",
        "Chest/Bust (cm)",
        "Skirt Length (cm)",
        "Pant/Short or - (cm)",
        "Hip (cm)",
        "Waist (cm)",
        "Garment Length (cm)",
    ]
    rendered_rows = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "-",
            metric_cell(row["weight"], "kg"),
            metric_cell(row["height"], "cm"),
            metric_cell(row["chest_cm"], "cm"),
            metric_cell(row["skirt_cm"], "cm"),
            "-",
            metric_cell(row["hip_cm"], "cm"),
            metric_cell(row["waist_cm"], "cm"),
            metric_cell(row["length_cm"], "cm"),
        ]
        rendered_rows.append(
            "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"
        )
    return "\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight-looking pleated fabric shown in the supplied image; exact fiber content is not supplied.</li>",
        "<li><strong>Family story:</strong> A coordinated mom-and-daughter maxi-dress look for vacations, outdoor celebrations, and family photos.</li>",
        f"<li><strong>Color:</strong> {PRINT_NAME} fades from soft pink to white.</li>",
        "<li><strong>Design details:</strong> Slim shoulder straps, a softly gathered neckline, allover pleats, and a flowing A-line maxi silhouette.</li>",
        "<li><strong>Care:</strong> Follow the sewn-in garment label; an exact care method is not supplied.</li>",
        "<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years and Mother S through Mother 2XL.</li>",
        "</ul>",
        "",
        "<h3>Size Chart - Dress</h3>",
        '<table id="size-chart" class="size-chart">',
        "<thead><tr>",
        *[f"<th>{header}</th>" for header in headers],
        "</tr></thead>",
        "<tbody>",
        *rendered_rows,
        "</tbody>",
        "</table>",
        "",
        "<p>Rosewater Ombre gives mom-and-daughter dressing a soft, flowing finish with the same pink-to-white fade and fine pleated texture across both dress choices. Select each child or mother size separately to build the matching combination you need.</p>",
        "",
        "<p>Each dress is sold separately. The cardigan, bags, shoes, and other styling accessories shown in the image are not included. Every available variant maps to one row in the attached size chart.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Mom + daughter match:</strong> Coordinated child and mother dresses in one ombre colorway.</li>",
        "<li><strong>Pink-to-white fade:</strong> A soft gradient keeps the matching look light and photo-ready.</li>",
        "<li><strong>Pleated maxi shape:</strong> Fine vertical pleats and a flowing A-line silhouette are visible on both dresses.</li>",
        "<li><strong>Chart-backed sizing:</strong> Seven child rows and five mother rows are transcribed from the supplied chart.</li>",
        "<li><strong>Separate selections:</strong> Add the child and mother sizes you want; this is not a bundled set.</li>",
        "</ul>",
        "",
        "<p>Choose the sizes you need for a softly coordinated Rosewater Ombre moment.</p>",
    ])


def build_derived() -> dict[str, Any]:
    variants: list[dict[str, Any]] = []
    recap: list[dict[str, Any]] = []
    for row in SIZE_CHART:
        price = price_for(row)
        compare = MOTHER_COMPARE if row["audience"] == "mother" else CHILD_COMPARE
        sku = sku_for(row)
        variants.append({
            "price": price,
            "compareAtPrice": compare,
            "taxable": True,
            "inventoryPolicy": "DENY",
            "optionValues": [
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": COLOR_NAME},
            ],
            "inventoryItem": {
                "sku": sku,
                "cost": cost_for(price),
                "tracked": True,
                "requiresShipping": True,
            },
        })
        size_gid, catalog_label = SIZE_METAOBJECTS[row["picker_label"]]
        recap.append({
            **row,
            "sku": sku,
            "price": price,
            "compare_at_price": compare,
            "cost": cost_for(price),
            "color": COLOR_NAME,
            "shopify_size_gid": size_gid,
            "catalog_label": catalog_label,
        })
    size_values = list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART))
    return {
        "option_names": ["Size", "Color"],
        "option_axes": [
            {"name": "Size", "values": size_values},
            {"name": "Color", "values": [COLOR_NAME]},
        ],
        "product_options": [
            {"name": "Size", "values": [{"name": value} for value in size_values]},
            {"name": "Color", "values": [{"name": COLOR_NAME}]},
        ],
        "variants": variants,
        "recap": recap,
        "tags": tags(),
        "expected_pairs": [[row["picker_label"], COLOR_NAME] for row in SIZE_CHART],
        "expected_skus": sorted(variant["inventoryItem"]["sku"] for variant in variants),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def table_shape(body: str) -> tuple[list[str], list[int], list[int]]:
    tables = re.findall(r"<table\b[^>]*>.*?</table>", body, re.I | re.S)
    ids = [match.group(1) for match in (re.search(r'\bid="([^"]+)"', table, re.I) for table in tables) if match]
    headers = [len(re.findall(r"<th\b", table, re.I)) for table in tables]
    rows = []
    for table in tables:
        tbody = re.search(r"<tbody\b[^>]*>(.*?)</tbody>", table, re.I | re.S)
        rows.append(len(re.findall(r"<tr\b", tbody.group(1), re.I)) if tbody else 0)
    return ids, headers, rows


def validate_local_preflight(body: str, derived: dict[str, Any]) -> dict[str, Any]:
    required = {
        "audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix",
        "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm",
        "skirt_cm", "sleeve_cm", "pant_cm", "source_note",
    }
    errors: list[str] = []
    if len(SIZE_CHART) != 12 or len(derived["variants"]) != 12:
        errors.append(f"expected 12 chart rows and variants, got {len(SIZE_CHART)} and {len(derived['variants'])}")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        if row["picker_label"] not in SIZE_METAOBJECTS:
            errors.append(f"missing size metaobject for {row['picker_label']}")
        if row["audience"] == "child":
            if row["waist_cm"] != row["chest_cm"] or row["hip_cm"] != row["chest_cm"] + 4:
                errors.append(f"child derivation mismatch for {row['picker_label']}")
        elif row["chest_cm"] != "-" or row["hip_cm"] != "-":
            errors.append(f"mother chest/hip must remain unavailable for {row['picker_label']}")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate role/picker row")
    if len(set(derived["expected_skus"])) != len(derived["expected_skus"]):
        errors.append("duplicate SKU")
    ids, header_counts, row_counts = table_shape(body)
    if ids != ["size-chart"] or header_counts != [10] or row_counts != [12]:
        errors.append(f"size table shape mismatch: ids={ids} headers={header_counts} rows={row_counts}")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        errors.append(
            f"title/SEO length guard failed: {len(TITLE)}/{len(SEO_TITLE)}/{len(SEO_DESCRIPTION)}"
        )
    if CHILD_COMPARE != compare_at(CHILD_PRICE) or MOTHER_COMPARE != compare_at(MOTHER_PRICE):
        errors.append("compare-at price rule mismatch")
    for variant in derived["variants"]:
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append(f"50 percent cost mismatch for {variant['inventoryItem']['sku']}")
    if not PRODUCT_IMAGE.is_file() or not SOURCE_CHART.is_file():
        errors.append("required product image or source chart is missing")
    else:
        if sha256(PRODUCT_IMAGE) != EXPECTED_IMAGE_SHA256:
            errors.append("product image checksum mismatch")
        if sha256(SOURCE_CHART) != EXPECTED_CHART_SHA256:
            errors.append("source size-chart checksum mismatch")
    if not CSV_HEADER_SOURCE.is_file():
        errors.append(f"CSV header source is missing: {CSV_HEADER_SOURCE}")
    customer_blob = json.dumps({
        "title": TITLE,
        "seo_title": SEO_TITLE,
        "seo_description": SEO_DESCRIPTION,
        "tags": derived["tags"],
        "body": body,
    }, ensure_ascii=False).lower()
    source_markers = ["16" + "88", "ali" + "baba", "detail" + ".", OFFER_ID]
    leaked = [marker for marker in source_markers if marker in customer_blob]
    if leaked:
        errors.append(f"customer-facing source marker leak: {leaked}")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))
    return {
        "chart_rows": len(SIZE_CHART),
        "variants": len(derived["variants"]),
        "title_chars": len(TITLE),
        "seo_title_chars": len(SEO_TITLE),
        "seo_description_chars": len(SEO_DESCRIPTION),
        "table_ids": ids,
        "table_header_counts": header_counts,
        "table_row_counts": row_counts,
        "product_image_sha256": sha256(PRODUCT_IMAGE),
        "source_chart_sha256": sha256(SOURCE_CHART),
    }


def run_variant_model_guard(derived: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="rsom-variant-model-") as temp_dir:
        work = Path(temp_dir)
        chart_path = work / "size-chart.json"
        derived_path = work / "derived.json"
        evidence_path = work / "evidence.json"
        chart_path.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
        derived_path.write_text(json.dumps(derived, indent=2), encoding="utf-8")
        evidence_path.write_text(json.dumps({
            "title": "Pink-to-white pleated mother-daughter dresses",
            "raw_detail_text": "The authorized scope contains the matching girl dress and mother dress only.",
            "notes": "Out-of-scope male rows are excluded. One dress garment in one ombre colorway remains, so the axes are Size and Color.",
        }), encoding="utf-8")
        subprocess.run([
            str(PYTHON_BIN),
            str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart_path),
            "--derived", str(derived_path),
            "--vendor-evidence", str(evidence_path),
            "--primary-category", PRIMARY_CATEGORY,
            "--tags", ",".join(derived["tags"]),
        ], check=True)


def expected_metaobjects() -> dict[str, str]:
    rows = {gid: label for gid, label in SIZE_METAOBJECTS.values()}
    for group in (
        AGE_GROUP_METAOBJECTS,
        COLOR_PATTERN_METAOBJECTS,
        TARGET_GENDER_METAOBJECTS,
        DRESS_OCCASION_METAOBJECTS,
        DRESS_STYLE_METAOBJECTS,
        DRESS_LENGTH_METAOBJECTS,
        SLEEVE_LENGTH_METAOBJECTS,
    ):
        rows.update(group)
    return rows


def verify_reference_nodes() -> dict[str, Any]:
    expected = expected_metaobjects()
    output = gql(
        """
        query ReferencePreflight($categoryId: ID!, $metaobjectIds: [ID!]!) {
          category: node(id: $categoryId) {
            ... on TaxonomyCategory { id fullName isLeaf }
          }
          metaobjects: nodes(ids: $metaobjectIds) {
            ... on Metaobject { id displayName type }
          }
        }
        """,
        {"categoryId": TAXONOMY_GID, "metaobjectIds": list(expected)},
    )
    category = output["data"]["category"]
    if not category or category.get("fullName") != EXPECTED_TAXONOMY or category.get("isLeaf") is not True:
        raise RuntimeError(f"taxonomy reference guard failed: {category}")
    nodes = {node["id"]: node for node in output["data"]["metaobjects"] if node and node.get("id")}
    missing = sorted(set(expected) - set(nodes))
    mismatched = {
        gid: {"expected": expected[gid], "actual": nodes[gid].get("displayName")}
        for gid in sorted(set(expected) & set(nodes))
        if nodes[gid].get("displayName") != expected[gid]
    }
    if missing or mismatched:
        raise RuntimeError(
            "Shopify reference guard failed: " + json.dumps({"missing": missing, "mismatched": mismatched}, indent=2)
        )
    return {
        "taxonomy": category,
        "metaobjects_checked": len(expected),
        "metaobject_types": sorted({node["type"] for node in nodes.values()}),
    }


def verify_price_precedent() -> dict[str, Any]:
    output = gql(
        """
        query PricePrecedent($first: Int!, $query: String!) {
          products(first: $first, query: $query, sortKey: UPDATED_AT, reverse: true) {
            nodes {
              id handle title status productType
              variants(first: 100) { nodes { sku price } }
            }
          }
        }
        """,
        {"first": 50, "query": 'status:active product_type:"Matching Family Dresses"'},
    )
    products = [
        product for product in output["data"]["products"]["nodes"]
        if product.get("status") == "ACTIVE" and product.get("productType") == PRODUCT_TYPE
    ]
    child_matches = []
    mother_matches = []
    child_distribution: dict[str, int] = {}
    mother_distribution: dict[str, int] = {}
    for product in products:
        for variant in product["variants"]["nodes"]:
            sku = variant.get("sku") or ""
            price = variant.get("price") or ""
            if "-GRL-" in sku:
                child_distribution[price] = child_distribution.get(price, 0) + 1
                if price == CHILD_PRICE:
                    child_matches.append(product["handle"])
            if "-MOM-" in sku:
                mother_distribution[price] = mother_distribution.get(price, 0) + 1
                if price == MOTHER_PRICE:
                    mother_matches.append(product["handle"])
    if not child_matches or not mother_matches:
        raise RuntimeError(
            "fresh price precedent guard failed: "
            + json.dumps({
                "products": len(products),
                "child_distribution": child_distribution,
                "mother_distribution": mother_distribution,
            }, indent=2)
        )
    return {
        "active_products_checked": len(products),
        "child_price": CHILD_PRICE,
        "child_price_rows": child_distribution.get(CHILD_PRICE, 0),
        "mother_price": MOTHER_PRICE,
        "mother_price_rows": mother_distribution.get(MOTHER_PRICE, 0),
        "sample_child_handles": sorted(set(child_matches))[:3],
        "sample_mother_handles": sorted(set(mother_matches))[:3],
    }


def fetch_existing() -> dict[str, Any] | None:
    output = gql(
        """
        query ExistingProduct($handle: String!) {
          productByHandle(handle: $handle) {
            id handle title status publishedAt onlineStoreUrl
            options { id name position values }
            variants(first: 100) {
              nodes { id sku selectedOptions { name value } }
            }
            resourcePublicationsV2(first: 20) {
              nodes { isPublished publication { id name } }
            }
          }
        }
        """,
        {"handle": HANDLE},
    )
    return output["data"]["productByHandle"]


def verify_unique_title(existing_id: str | None = None) -> None:
    output = gql(
        """
        query DuplicateTitle($first: Int!, $query: String!) {
          products(first: $first, query: $query) { nodes { id handle title status } }
        }
        """,
        {"first": 25, "query": f'title:"{TITLE}"'},
    )
    duplicates = [
        product for product in output["data"]["products"]["nodes"]
        if product.get("title") == TITLE and product.get("id") != existing_id
    ]
    if duplicates:
        raise RuntimeError("exact-title duplicate guard failed: " + json.dumps(duplicates, indent=2))


def product_input(body: str) -> dict[str, Any]:
    return {
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


def guard_existing(existing: dict[str, Any] | None, expected_skus: list[str]) -> None:
    if existing is None:
        return
    published = [
        node for node in existing["resourcePublicationsV2"]["nodes"] if node["isPublished"]
    ]
    if existing["status"] != "DRAFT" or existing.get("publishedAt") is not None or published:
        raise RuntimeError(
            "existing product is not a clean unpublished draft; refusing mutation: "
            + json.dumps({
                "id": existing["id"],
                "status": existing["status"],
                "publishedAt": existing.get("publishedAt"),
                "published": published,
            }, indent=2)
        )
    option_names = [option["name"] for option in existing["options"]]
    if option_names != ["Size", "Color"]:
        raise RuntimeError(f"existing draft option axes are {option_names}; expected Size / Color")
    live_skus = [node.get("sku") or "" for node in existing["variants"]["nodes"]]
    unexpected = sorted(set(sku for sku in live_skus if sku) - set(expected_skus))
    if unexpected:
        raise RuntimeError(f"existing draft has unexpected SKUs: {unexpected}")


def ensure_product(body: str, derived: dict[str, Any]) -> tuple[str, bool]:
    existing = fetch_existing()
    guard_existing(existing, derived["expected_skus"])
    verify_unique_title(existing["id"] if existing else None)
    if existing is None:
        output = gql(
            """
            mutation ProductCreate($input: ProductInput!) {
              productCreate(input: $input) {
                product { id handle title status }
                userErrors { field message }
              }
            }
            """,
            {"input": {**product_input(body), "productOptions": derived["product_options"]}},
        )
        require_no_user_errors(output, ["data", "productCreate", "userErrors"])
        product_id = output["data"]["productCreate"]["product"]["id"]
        created = True
    else:
        product_id = existing["id"]
        created = False
    output = gql(
        """
        mutation ProductUpdate($product: ProductUpdateInput!) {
          productUpdate(product: $product) {
            product { id handle title status }
            userErrors { field message }
          }
        }
        """,
        {"product": {"id": product_id, **product_input(body)}},
    )
    require_no_user_errors(output, ["data", "productUpdate", "userErrors"])
    return product_id, created


def sync_variants(product_id: str, derived: dict[str, Any]) -> None:
    existing = fetch_existing()
    if existing is None or existing["id"] != product_id:
        raise RuntimeError("product missing after create/update")
    guard_existing(existing, derived["expected_skus"])
    live_skus = {node.get("sku") or "" for node in existing["variants"]["nodes"]}
    missing_skus = set(derived["expected_skus"]) - live_skus
    if missing_skus:
        missing_variants = [
            variant for variant in derived["variants"]
            if variant["inventoryItem"]["sku"] in missing_skus
        ]
        output = gql(
            """
            mutation BulkCreateVariants(
              $productId: ID!,
              $variants: [ProductVariantsBulkInput!]!,
              $strategy: ProductVariantsBulkCreateStrategy
            ) {
              productVariantsBulkCreate(
                productId: $productId,
                variants: $variants,
                strategy: $strategy
              ) {
                productVariants { id sku title price compareAtPrice inventoryPolicy }
                userErrors { field message }
              }
            }
            """,
            {
                "productId": product_id,
                "variants": missing_variants,
                "strategy": "REMOVE_STANDALONE_VARIANT",
            },
        )
        require_no_user_errors(output, ["data", "productVariantsBulkCreate", "userErrors"])
        time.sleep(1)
        existing = fetch_existing()
        if existing is None:
            raise RuntimeError("product missing after variant creation")
    by_sku = {node.get("sku") or "": node for node in existing["variants"]["nodes"]}
    missing_after = sorted(set(derived["expected_skus"]) - set(by_sku))
    if missing_after:
        raise RuntimeError(f"variants remain missing after create: {missing_after}")
    updates = []
    for variant in derived["variants"]:
        sku = variant["inventoryItem"]["sku"]
        updates.append({
            "id": by_sku[sku]["id"],
            "price": variant["price"],
            "compareAtPrice": variant["compareAtPrice"],
            "taxable": True,
            "inventoryPolicy": "DENY",
            "inventoryItem": variant["inventoryItem"],
        })
    output = gql(
        """
        mutation BulkUpdateVariants($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
          productVariantsBulkUpdate(
            productId: $productId,
            variants: $variants,
            allowPartialUpdates: false
          ) {
            productVariants {
              id sku title price compareAtPrice taxable inventoryPolicy
              inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
            }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "variants": updates},
    )
    require_no_user_errors(output, ["data", "productVariantsBulkUpdate", "userErrors"])


def metafield_inputs(product_id: str) -> list[dict[str, str]]:
    size_refs = list(dict.fromkeys(SIZE_METAOBJECTS[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId":product_id,"namespace":"custom","key":"category1","type":"single_line_text_field","value":LISTING_MODE},
        {"ownerId":product_id,"namespace":"custom","key":"subcategory","type":"single_line_text_field","value":"Dresses"},
        {"ownerId":product_id,"namespace":"custom","key":"subcategory2","type":"single_line_text_field","value":"Maxi"},
        {"ownerId":product_id,"namespace":"custom","key":"pattern","type":"single_line_text_field","value":"Ombre"},
        {"ownerId":product_id,"namespace":"custom","key":"style","type":"single_line_text_field","value":"Pleated Maxi Dress"},
        {"ownerId":product_id,"namespace":"custom","key":"type","type":"single_line_text_field","value":"Dress"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_product","type":"boolean","value":"false"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"gender","type":"single_line_text_field","value":"female"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"age_group","type":"single_line_text_field","value":"adult"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"condition","type":"single_line_text_field","value":"new"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_label_0","type":"single_line_text_field","value":LISTING_MODE},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_label_1","type":"single_line_text_field","value":PRINT_NAME},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_label_2","type":"single_line_text_field","value":"Summer"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_label_3","type":"single_line_text_field","value":"Pleated Maxi Dress"},
        {"ownerId":product_id,"namespace":"mm-google-shopping","key":"custom_label_4","type":"single_line_text_field","value":"Two-Role Matching"},
        {"ownerId":product_id,"namespace":"shopify","key":"age-group","type":"list.metaobject_reference","value":json.dumps(list(AGE_GROUP_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"color-pattern","type":"list.metaobject_reference","value":json.dumps(list(COLOR_PATTERN_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"dress-occasion","type":"list.metaobject_reference","value":json.dumps(list(DRESS_OCCASION_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"dress-style","type":"list.metaobject_reference","value":json.dumps(list(DRESS_STYLE_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"size","type":"list.metaobject_reference","value":json.dumps(size_refs)},
        {"ownerId":product_id,"namespace":"shopify","key":"skirt-dress-length-type","type":"list.metaobject_reference","value":json.dumps(list(DRESS_LENGTH_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"sleeve-length-type","type":"list.metaobject_reference","value":json.dumps(list(SLEEVE_LENGTH_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"shopify","key":"target-gender","type":"list.metaobject_reference","value":json.dumps(list(TARGET_GENDER_METAOBJECTS))},
        {"ownerId":product_id,"namespace":"global","key":"title_tag","type":"single_line_text_field","value":SEO_TITLE},
        {"ownerId":product_id,"namespace":"global","key":"description_tag","type":"single_line_text_field","value":SEO_DESCRIPTION},
    ]


def set_metafields(product_id: str) -> None:
    rows = metafield_inputs(product_id)
    for start in range(0, len(rows), 25):
        output = gql(
            """
            mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
              metafieldsSet(metafields: $metafields) {
                metafields { namespace key type value }
                userErrors { field message }
              }
            }
            """,
            {"metafields": rows[start:start + 25]},
        )
        require_no_user_errors(output, ["data", "metafieldsSet", "userErrors"])


def delete_unsupported_metafields(product_id: str) -> None:
    unsupported = {
        "fabric", "neckline", "care-instructions", "top-length-type",
        "pants-length-type", "waist-rise",
    }
    product = gql(
        """
        query ShopifyMetafields($id: ID!) {
          product(id: $id) { metafields(first: 100, namespace: "shopify") { nodes { namespace key } } }
        }
        """,
        {"id": product_id},
    )["data"]["product"]
    rows = [
        {"ownerId": product_id, "namespace": node["namespace"], "key": node["key"]}
        for node in product["metafields"]["nodes"]
        if node["key"] in unsupported
    ]
    if not rows:
        return
    output = gql(
        """
        mutation MetafieldsDelete($metafields: [MetafieldIdentifierInput!]!) {
          metafieldsDelete(metafields: $metafields) {
            deletedMetafields { ownerId namespace key }
            userErrors { field message }
          }
        }
        """,
        {"metafields": rows},
    )
    require_no_user_errors(output, ["data", "metafieldsDelete", "userErrors"])


def multipart_upload(target: dict[str, Any], path: Path, mime_type: str) -> None:
    boundary = "----DLM" + uuid.uuid4().hex
    chunks: list[bytes] = []
    for parameter in target["parameters"]:
        chunks.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{parameter["name"]}"\r\n\r\n{parameter["value"]}\r\n'.encode()
        )
    chunks.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\nContent-Type: {mime_type}\r\n\r\n'.encode()
        + path.read_bytes()
        + b"\r\n"
    )
    chunks.append(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        target["url"],
        data=b"".join(chunks),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request) as response:
        response.read()


def attach_media(product_id: str) -> None:
    existing = gql(
        """
        query ProductMedia($id: ID!) {
          product(id: $id) { media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } } }
        }
        """,
        {"id": product_id},
    )["data"]["product"]["media"]["nodes"]
    if EXPECTED_MEDIA_ALT in {node.get("alt") for node in existing}:
        return
    mime_type = mimetypes.guess_type(PRODUCT_IMAGE.name)[0] or "image/png"
    staged = gql(
        """
        mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
        """,
        {"input": [{
            "filename": PRODUCT_IMAGE.name,
            "mimeType": mime_type,
            "resource": "IMAGE",
            "httpMethod": "POST",
        }]},
    )
    require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    multipart_upload(target, PRODUCT_IMAGE, mime_type)
    created = gql(
        """
        mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id alt } }
            userErrors { field message }
          }
        }
        """,
        {"productId": product_id, "media": [{
            "originalSource": target["resourceUrl"],
            "mediaContentType": "IMAGE",
            "alt": EXPECTED_MEDIA_ALT,
        }]},
    )
    require_no_user_errors(created, ["data", "productCreateMedia", "userErrors"])


def fetch_verification(product_id: str) -> dict[str, Any]:
    return gql(
        """
        query VerifyProduct($id: ID!) {
          product(id: $id) {
            id title handle vendor productType status publishedAt onlineStoreUrl descriptionHtml tags
            seo { title description }
            category { id fullName }
            options { name position values optionValues { id name hasVariants } }
            variants(first: 100) {
              nodes {
                id sku title price compareAtPrice taxable inventoryPolicy inventoryQuantity
                selectedOptions { name value }
                inventoryItem { id tracked requiresShipping unitCost { amount currencyCode } }
              }
            }
            media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } }
            collections(first: 50) { nodes { title handle } }
            metafields(first: 150) { nodes { namespace key type value } }
            resourcePublicationsV2(first: 20) {
              nodes { isPublished publishDate publication { id name } }
            }
          }
        }
        """,
        {"id": product_id},
    )["data"]["product"]


def normalize_metafield_value(row: dict[str, Any]) -> Any:
    if row["type"] == "list.metaobject_reference":
        return json.loads(row["value"])
    return row["value"]


def normalize_shopify_html(value: str) -> str:
    """Ignore Shopify's whitespace-only rich-text serialization changes."""
    return re.sub(r">\s+<", "><", value.strip())


def verify_product(product: dict[str, Any], body: str, derived: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    variants = product["variants"]["nodes"]
    spec_by_sku = {row["sku"]: row for row in derived["recap"]}
    live_by_sku = {row["sku"]: row for row in variants}
    published = [
        node["publication"]["name"]
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    ]
    expected_pairs = {tuple(pair) for pair in derived["expected_pairs"]}
    live_pairs = {
        tuple({option["name"]: option["value"] for option in row["selectedOptions"]}[name] for name in derived["option_names"])
        for row in variants
    }
    expected_mfs = {
        (row["namespace"], row["key"]): normalize_metafield_value(row)
        for row in metafield_inputs(product["id"])
    }
    live_mfs = {
        (row["namespace"], row["key"]): normalize_metafield_value(row)
        for row in product["metafields"]["nodes"]
    }
    unsupported = {
        ("shopify", key) for key in (
            "fabric", "neckline", "care-instructions", "top-length-type",
            "pants-length-type", "waist-rise",
        )
    }
    customer_blob = json.dumps({
        "title": product["title"],
        "description": product["descriptionHtml"],
        "tags": product["tags"],
        "seo": product["seo"],
        "productType": product["productType"],
        "metafields": {
            f"{namespace}.{key}": value
            for (namespace, key), value in live_mfs.items()
            if namespace in {"custom", "mm-google-shopping", "global"}
        },
    }, ensure_ascii=False).lower()
    source_markers = ["16" + "88", "ali" + "baba", "detail" + ".", OFFER_ID]
    source_leaks = [marker for marker in source_markers if marker in customer_blob]

    variant_errors: list[str] = []
    price_rows: list[dict[str, Any]] = []
    for sku, spec in spec_by_sku.items():
        live = live_by_sku.get(sku)
        if live is None:
            variant_errors.append(f"missing {sku}")
            continue
        unit_cost = ((live.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        row_ok = (
            live["price"] == spec["price"]
            and live["compareAtPrice"] == spec["compare_at_price"]
            and money(unit_cost) == spec["cost"]
            and live["taxable"] is True
            and live["inventoryPolicy"] == "DENY"
            and live["inventoryQuantity"] == 0
            and live["inventoryItem"]["tracked"] is True
            and live["inventoryItem"]["requiresShipping"] is True
        )
        if not row_ok:
            variant_errors.append(f"variant field mismatch {sku}")
        price_rows.append({
            "sku": sku,
            "live_price": live["price"],
            "live_compare_at": live["compareAtPrice"],
            "live_cost": unit_cost,
            "inventory_quantity": live["inventoryQuantity"],
            "expected_price": spec["price"],
            "expected_compare_at": spec["compare_at_price"],
            "expected_cost": spec["cost"],
            "match": row_ok,
        })

    ids, header_counts, row_counts = table_shape(product["descriptionHtml"])
    checks: list[tuple[str, bool, Any]] = [
        ("identity", product["handle"] == HANDLE and product["title"] == TITLE, {"handle": product["handle"], "title": product["title"]}),
        ("vendor", product["vendor"] == VENDOR, product["vendor"]),
        ("product type", product["productType"] == PRODUCT_TYPE, product["productType"]),
        ("draft status", product["status"] == "DRAFT", product["status"]),
        ("publishedAt null", product["publishedAt"] is None, product["publishedAt"]),
        ("onlineStoreUrl null", product["onlineStoreUrl"] is None, product["onlineStoreUrl"]),
        ("no live publications", not published, published),
        ("taxonomy", product["category"] == {"id": TAXONOMY_GID, "fullName": EXPECTED_TAXONOMY}, product["category"]),
        ("SEO exact", product["seo"] == {"title": SEO_TITLE, "description": SEO_DESCRIPTION}, product["seo"]),
        ("body semantic parity", normalize_shopify_html(product["descriptionHtml"]) == normalize_shopify_html(body), {"live_chars": len(product["descriptionHtml"]), "spec_chars": len(body)}),
        ("tags exact", sorted(product["tags"]) == sorted(derived["tags"]), len(product["tags"])),
        ("option axes", [option["name"] for option in product["options"]] == ["Size", "Color"], [option["name"] for option in product["options"]]),
        ("variant count", len(variants) == 12, len(variants)),
        ("SKU parity", sorted(live_by_sku) == derived["expected_skus"], sorted(live_by_sku)),
        ("Size x Color parity", live_pairs == expected_pairs, sorted(live_pairs)),
        ("variant fields", not variant_errors, variant_errors),
        ("size table shape", ids == ["size-chart"] and header_counts == [10] and row_counts == [12], {"ids": ids, "headers": header_counts, "rows": row_counts}),
        ("metafields exact", all(live_mfs.get(key) == value for key, value in expected_mfs.items()), sorted(f"{key[0]}.{key[1]}" for key, value in expected_mfs.items() if live_mfs.get(key) != value)),
        ("unsupported metafields absent", not (unsupported & set(live_mfs)), sorted(f"{key[0]}.{key[1]}" for key in unsupported & set(live_mfs))),
        ("product image present", EXPECTED_MEDIA_ALT in {node.get("alt") for node in product["media"]["nodes"]}, [node.get("alt") for node in product["media"]["nodes"]]),
        ("size chart not uploaded", not any("size chart" in (node.get("alt") or "").lower() for node in product["media"]["nodes"]), [node.get("alt") for node in product["media"]["nodes"]]),
        ("no customer source leak", not source_leaks, source_leaks),
    ]
    errors = [f"{label}: {detail}" for label, ok, detail in checks if not ok]
    return [
        {"check": label, "status": "PASS" if ok else "FAIL", "detail": detail}
        for label, ok, detail in checks
    ] + [{"price_rows": price_rows}], errors


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(body: str, derived: dict[str, Any]) -> None:
    with CSV_HEADER_SOURCE.open(newline="", encoding="utf-8") as source:
        header = next(csv.reader(source))
    rows: list[dict[str, str]] = []
    size_names = ", ".join(row["picker_label"] for row in SIZE_CHART)
    for index, recap in enumerate(derived["recap"]):
        row = {column: "" for column in header}

        def put(field: str, value: Any, *, first_only: bool = False) -> None:
            if field in row and (not first_only or index == 0):
                row[field] = str(value)

        put("Handle", HANDLE)
        put("Title", TITLE, first_only=True)
        put("Body (HTML)", body, first_only=True)
        put("Vendor", VENDOR, first_only=True)
        put("Product Category", EXPECTED_TAXONOMY, first_only=True)
        put("Type", PRODUCT_TYPE, first_only=True)
        put("Tags", ", ".join(derived["tags"]), first_only=True)
        put("Published", "FALSE")
        put("Option1 Name", "Size")
        put("Option1 Value", recap["picker_label"])
        put("Option2 Name", "Color")
        put("Option2 Value", COLOR_NAME)
        put("Variant SKU", recap["sku"])
        put("Variant Grams", "0")
        put("Variant Inventory Tracker", "shopify")
        put("Variant Inventory Policy", "deny")
        put("Variant Fulfillment Service", "manual")
        put("Variant Price", recap["price"])
        put("Variant Compare At Price", recap["compare_at_price"])
        put("Variant Requires Shipping", "TRUE")
        put("Variant Taxable", "TRUE")
        put("Gift Card", "FALSE", first_only=True)
        put("SEO Title", SEO_TITLE, first_only=True)
        put("SEO Description", SEO_DESCRIPTION, first_only=True)
        put("Google Shopping / Gender", "female", first_only=True)
        put("Google Shopping / Age Group", "adult", first_only=True)
        put("Google Shopping / Condition", "new", first_only=True)
        put("Google Shopping / Custom Product", "FALSE", first_only=True)
        put("Google Shopping / Custom Label 0", LISTING_MODE, first_only=True)
        put("Google Shopping / Custom Label 1", PRINT_NAME, first_only=True)
        put("Google Shopping / Custom Label 2", "Summer", first_only=True)
        put("Google Shopping / Custom Label 3", "Pleated Maxi Dress", first_only=True)
        put("Google Shopping / Custom Label 4", "Two-Role Matching", first_only=True)
        put("Category1 (product.metafields.custom.category1)", LISTING_MODE, first_only=True)
        put("Pattern (product.metafields.custom.pattern)", "Ombre", first_only=True)
        put("Style (product.metafields.custom.style)", "Pleated Maxi Dress", first_only=True)
        put("SubCategory (product.metafields.custom.subcategory)", "Dresses", first_only=True)
        put("SubCategory2 (product.metafields.custom.subcategory2)", "Maxi", first_only=True)
        put("Type (product.metafields.custom.type)", "Dress", first_only=True)
        put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false", first_only=True)
        put("Age group (product.metafields.shopify.age-group)", "Kids, Adults", first_only=True)
        put("Color (product.metafields.shopify.color-pattern)", "Pink, White", first_only=True)
        put("Dress occasion (product.metafields.shopify.dress-occasion)", "Beach outings, family vacations", first_only=True)
        put("Dress style (product.metafields.shopify.dress-style)", "A-line", first_only=True)
        put("Size (product.metafields.shopify.size)", size_names, first_only=True)
        put("Skirt/Dress length type (product.metafields.shopify.skirt-dress-length-type)", "Maxi", first_only=True)
        put("Sleeve length type (product.metafields.shopify.sleeve-length-type)", "Sleeveless", first_only=True)
        put("Cost per item", recap["cost"])
        put("Status", "draft")
        rows.append(row)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(
    product: dict[str, Any],
    derived: dict[str, Any],
    verification: list[dict[str, Any]],
    price_evidence: dict[str, Any],
) -> None:
    product_id = product["id"]
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    checks = [row for row in verification if "check" in row]
    price_rows = next(row["price_rows"] for row in verification if "price_rows" in row)
    collection_names = sorted(node["title"] for node in product["collections"]["nodes"])
    metafield_names = sorted(
        f"{node['namespace']}.{node['key']}"
        for node in product["metafields"]["nodes"]
        if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}
    )
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| Source offer ID | `{OFFER_ID}` (URL omitted under repository source-hygiene policy) |",
        "| SIZE_CHART_SOURCE | owner-attached image |",
        "| LISTING_MODE | Mommy and Me |",
        "| PRIMARY_CATEGORY | Dress -> Dresses |",
        "| DESIGNS_TO_LIST | Girl Dress and Mother Dress |",
        "| EXCLUDE_ITEMS | male-child and father shirt rows |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | `{SHORTCODE}` |",
        f"| COLOR_TOKEN | `{COLOR_TOKEN}` |",
        "",
        "## Source Evidence Status",
        "The exact offer page could not be inspected because the browser site-safety gate rejected access. The owner-attached product and chart images are therefore the authoritative listing evidence. A repository-known search card for this offer reports a pink vacation-style family design, but its earlier sourcing review was rejected because supplier tenure, availability, one-piece support, and fulfillment timing were not verified. Those remain publication-time gates.",
        "",
        "## Pricing",
        f"A fresh read of `{price_evidence['active_products_checked']}` active `{PRODUCT_TYPE}` products found `{price_evidence['child_price_rows']}` child rows at `{CHILD_PRICE}` and `{price_evidence['mother_price_rows']}` mother rows at `{MOTHER_PRICE}`. FORCE_SPEC_PRICES applies those values. Compare-at prices are `{CHILD_COMPARE}` and `{MOTHER_COMPARE}`; unit costs are exactly 50 percent at `{cost_for(CHILD_PRICE)}` and `{cost_for(MOTHER_PRICE)}`.",
        "",
        "## Derivations and exclusions",
        "- The black girl and mother tables are in scope. Blue male-child and father shirt rows are excluded because the requested mode is Mommy and Me and the product image shows the mother-daughter dresses.",
        "- Child chart labels map 90/2码 through 150/14码 to Child 2 Years through Child 9-10 Years.",
        "- Mother chart labels S/160 through 2XL/180 map to Mother S through Mother 2XL.",
        "- Recommended weights were converted from jin at exactly 0.5 kg per jin.",
        "- Child chest, dress length, height, and weight are source-transcribed; the canonical child-dress rule derives waist = chest and hip = chest + 4 cm.",
        "- Mother waist, dress length, height, and weight are source-transcribed. The mother table does not publish chest/bust or hip, so those cells remain `-` rather than being guessed.",
        "- The chart's dress-length value is shown in both the skirt-length and garment-length columns because both canonical table columns refer to the same source measurement for this maxi dress.",
        "- Product options are `Size` and `Color`; one colorway across 12 chart rows produces 12 variants.",
        "",
        "## Title and SEO",
        "| Field | Value | Chars |",
        "|---|---|---:|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor row | Picker label | Color | SKU | Price | Compare-at | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---:|---|",
    ]
    for row in derived["recap"]:
        lines.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['color']} | "
            f"`{row['sku']}` | {row['price']} | {row['compare_at_price']} | {row['cost']} | "
            f"`{row['shopify_size_gid']}` ({row['catalog_label']}) |"
        )
    lines.extend([
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ])
    for row in checks:
        detail = json.dumps(row["detail"], ensure_ascii=False) if isinstance(row["detail"], (dict, list)) else str(row["detail"])
        lines.append(f"| {row['check']} | {row['status']} | {detail.replace('|', '/')} |")
    lines.extend([
        "",
        "## Price / inventory parity",
        "| SKU | Live price | Compare-at | Cost | Inventory | Match |",
        "|---|---:|---:|---:|---:|---|",
    ])
    for row in price_rows:
        lines.append(
            f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | "
            f"{row['inventory_quantity']} | {'PASS' if row['match'] else 'FAIL'} |"
        )
    lines.extend([
        "",
        "## Localized Size-Chart Gate",
        "<!-- LOCALIZATION_CLOSEOUT_START -->",
        "Pending synchronous finalizer. The listing is not complete until the closeout report passes with 0 missing / 0 planned / 0 errors.",
        "<!-- LOCALIZATION_CLOSEOUT_END -->",
        "",
        "## Metafields Written",
        *[f"- `{name}`" for name in metafield_names],
        "",
        "## Metafields Skipped",
        "- `shopify.fabric`: exact fiber composition is not supplied.",
        "- `shopify.care-instructions`: an exact care method is not supplied.",
        "- `shopify.neckline`: no exact supported neckline value was selected for the softly gathered slim-strap neckline.",
        "- `shopify.top-length-type`, `shopify.pants-length-type`, and `shopify.waist-rise`: not applicable to this dress-only listing.",
        "",
        "## Smart Collections",
        ", ".join(collection_names) if collection_names else "Collection indexing may wait while the product remains an unpublished draft.",
        "",
        "## Publication and residual gates",
        "- Product is an unpublished Shopify draft with zero inventory quantities. No publish or inventory-quantity mutation was called.",
        "- Supplier tenure, current availability, one-piece support, fulfillment timing, fiber composition, and exact care method remain unverified. Do not publish until the owner reviews those gates.",
        "- The supplied lifestyle image needs owner visual approval before any separate publication request.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SOURCE_CHART}`",
        f"- `{PRODUCT_IMAGE}`",
        "",
    ])
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def verify_repo_source_hygiene() -> None:
    forbidden_urls = ["https://detail" + ".1688", "http://detail" + ".1688"]
    findings: dict[str, list[str]] = {}
    for path in (SCRIPT_PATH, LISTING_MD, CSV_OUT, SIZE_CHART_OUT, BODY_HTML_OUT, VERIFY_JSON_OUT, PREFLIGHT_JSON_OUT):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        hits = [marker for marker in forbidden_urls if marker in text]
        if hits:
            findings[str(path)] = hits
    if findings:
        raise RuntimeError("repository source-URL hygiene failed: " + json.dumps(findings, indent=2))


def main() -> None:
    LISTING_MD.parent.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    derived = build_derived()
    local = validate_local_preflight(body, derived)
    run_variant_model_guard(derived)
    references = verify_reference_nodes()
    prices = verify_price_precedent()
    existing = fetch_existing()
    guard_existing(existing, derived["expected_skus"])
    verify_unique_title(existing["id"] if existing else None)

    write_json(SIZE_CHART_OUT, SIZE_CHART)
    BODY_HTML_OUT.write_text(body + "\n", encoding="utf-8")
    write_csv(body, derived)
    write_json(PREFLIGHT_JSON_OUT, {
        "status": "passed",
        "handle": HANDLE,
        "preflight_only": PREFLIGHT_ONLY,
        "local": local,
        "references": references,
        "price_evidence": prices,
        "existing_product": None if existing is None else {
            "id": existing["id"], "status": existing["status"], "publishedAt": existing.get("publishedAt")
        },
    })
    verify_repo_source_hygiene()
    if PREFLIGHT_ONLY:
        print(json.dumps({
            "status": "PREFLIGHT_PASS",
            "handle": HANDLE,
            "variants": len(derived["variants"]),
            "existing_product": None if existing is None else existing["id"],
            "preflight": str(PREFLIGHT_JSON_OUT),
        }, indent=2))
        return

    product_id, created = ensure_product(body, derived)
    sync_variants(product_id, derived)
    set_metafields(product_id)
    delete_unsupported_metafields(product_id)
    attach_media(product_id)
    time.sleep(3)

    # Re-assert draft identity after every product-owned mutation; this runner never publishes.
    update = gql(
        """
        mutation FinalDraftGuard($product: ProductUpdateInput!) {
          productUpdate(product: $product) {
            product { id handle status publishedAt }
            userErrors { field message }
          }
        }
        """,
        {"product": {"id": product_id, **product_input(body)}},
    )
    require_no_user_errors(update, ["data", "productUpdate", "userErrors"])

    product = fetch_verification(product_id)
    verification, errors = verify_product(product, body, derived)
    write_json(VERIFY_JSON_OUT, {
        "handle": HANDLE,
        "product_id": product_id,
        "created": created,
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "verification": verification,
        "product": product,
    })
    if errors:
        raise RuntimeError("SHOPIFY VERIFY FAILED:\n- " + "\n- ".join(errors))
    write_listing(product, derived, verification, prices)
    verify_repo_source_hygiene()
    print(json.dumps({
        "status": "SHOPIFY_DRAFT_VERIFIED",
        "handle": HANDLE,
        "product_id": product_id,
        "created": created,
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "variants": len(product["variants"]["nodes"]),
        "publishedAt": product["publishedAt"],
        "onlineStoreUrl": product["onlineStoreUrl"],
        "listing": str(LISTING_MD),
        "verify": str(VERIFY_JSON_OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
PY

if [[ "${DLM_PREFLIGHT_ONLY:-0}" == "1" ]]; then
  exit 0
fi

"$PYTHON_BIN" "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" \
  --handles "rosewater-ombre-mommy-and-me-dresses" \
  --python "$TRANSLATION_PYTHON"
