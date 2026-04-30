#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"

python3 - "$ROOT" "$ENV_FILE" <<'PY'
import csv
import html
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(sys.argv[1])
ENV_FILE = Path(sys.argv[2])
if ENV_FILE.exists():
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip().removeprefix("export "), value.strip().strip('"').strip("'"))

STORE = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("SHOPIFY_ADMIN_ACCESS_TOKEN not set")

API = f"https://{STORE}/admin/api/2025-01/graphql.json"

HANDLE = "midnight-rose-family-matching-set"
TITLE = "Midnight Rose Family Matching Set - Dress & Shirt"
SEO_TITLE = "Midnight Rose Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Black rose family matching set with dresses and collared shirts for mom, dad, girls and boys. Sizes 1-2Y-10Y, Mother S-2XL, Father S-4XL."
PRINT_NAME = "Midnight Rose"
SHORTCODE = "MDRO"
COLOR_TOKEN = "ROSE"
COLOR_NAME = "Black Rose Floral"
LISTING_MODE = "Family Matching"
CATEGORY = "FamilySet"
PRODUCT_TYPE = "Matching Family Sets"
CUSTOM_TYPE = "Two-Piece Set"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
MERCH_SUBCATEGORY = "Set"
MERCH_SUBCATEGORY2 = "Summer Family Matching Set"
MERCH_STYLE = "Matching Family Set"
MERCH_TYPE = "Two-Piece Set"
MERCH_COLLECTION_TAG = "Matching Family Set"
SEASON = "Summer"
VENDOR_URL = "https://detail.1688.com/offer/938601981390.html"
VENDOR = "dresslikemommy.com"
CHILD_PRICE = "28.99"
ADULT_PRICE = "31.99"
PRICE_NEIGHBOR_HANDLE = "sunlit-floral-family-matching-set"
SIZE_NEIGHBOR_HANDLE = "sunlit-floral-family-matching-set"

SCRIPT_PATH = ROOT / "ops/scripts/create-mdro-midnight-rose-family-matching-set.sh"
UPLOAD_DIR = ROOT / f"uploads/{HANDLE}"
LISTING_MD = ROOT / f"ops/listings/{HANDLE}-listing.md"
CSV_OUT = ROOT / f"ops/listings/{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / f"ops/listings/verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / f"ops/listings/size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / f"ops/listings/body-{HANDLE}.html"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
LISTING_MD.parent.mkdir(parents=True, exist_ok=True)


def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    parsed = json.loads(body)
    if parsed.get("errors"):
        raise SystemExit(f"GraphQL errors: {json.dumps(parsed['errors'], ensure_ascii=False)}")
    return parsed


def user_errors(response, path):
    value = response
    for key in path:
        value = value.get(key, {})
    errors = value or []
    if errors:
        raise SystemExit(f"Shopify userErrors: {json.dumps(errors, ensure_ascii=False)}")


def compare_at(price):
    value = Decimal(price) * Decimal("1.15")
    dollars = value.to_integral_value(rounding=ROUND_FLOOR)
    candidate = dollars + Decimal("0.99")
    if candidate < value:
        candidate = dollars + Decimal("1.99")
    return f"{candidate:.2f}"


def half_cost(price):
    return f"{(Decimal(price) * Decimal('0.50')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


CHILD_COMPARE = compare_at(CHILD_PRICE)
ADULT_COMPARE = compare_at(ADULT_PRICE)

size_rows = [
    ("80码", "Child 1-2 Years", "KID12Y", "1-2", "8.5-11 kg", "75-85 cm"),
    ("90码", "Child 2 Years", "KID2Y", "2", "11-14 kg", "85-95 cm"),
    ("100码", "Child 3 Years", "KID3Y", "3", "14-16.5 kg", "95-105 cm"),
    ("110码", "Child 4 Years", "KID4Y", "4", "16.5-20 kg", "105-115 cm"),
    ("120码", "Child 5 Years", "KID5Y", "5", "18.5-24 kg", "115-125 cm"),
    ("130码", "Child 6-7 Years", "KID67Y", "6-7", "24-27.5 kg", "125-130 cm"),
    ("140码", "Child 8 Years", "KID8Y", "8", "27.5-32.5 kg", "130-140 cm"),
    ("150码", "Child 9-10 Years", "KID910Y", "9-10", "32.5-37.5 kg", "140-150 cm"),
]
mother_rows = [
    ("妈妈S码", "Mother S", "S", "42.5-50 kg", "155-160 cm"),
    ("妈妈M码", "Mother M", "M", "50-57.5 kg", "160-165 cm"),
    ("妈妈L码", "Mother L", "L", "59-69 kg", "160-170 cm"),
    ("妈妈XL码", "Mother XL", "XL", "70-80 kg", "160-175 cm"),
    ("妈妈2XL码", "Mother 2XL", "2XL", "80-92.5 kg", "160-175 cm"),
]
father_rows = [
    ("爸爸S码", "Father S", "S", "42.5-50 kg", "160-165 cm"),
    ("爸爸M码", "Father M", "M", "50-57.5 kg", "165-170 cm"),
    ("爸爸L码", "Father L", "L", "57.5-67.5 kg", "168-173 cm"),
    ("爸爸XL码", "Father XL", "XL", "69-79 kg", "170-178 cm"),
    ("爸爸2XL码", "Father 2XL", "2XL", "80-89 kg", "175-180 cm"),
    ("爸爸3XL码", "Father 3XL", "3XL", "87.5-97.5 kg", "175-188 cm"),
    ("爸爸4XL码", "Father 4XL", "4XL", "97.5-115 kg", "178-195 cm"),
]


def blank_measure_row(audience, role, garment, vendor_label, picker_label, sku_suffix, age, weight, height):
    return {
        "audience": audience,
        "role": role,
        "garment": garment,
        "vendor_label": vendor_label,
        "picker_label": picker_label,
        "sku_suffix": sku_suffix,
        "age": age,
        "weight": weight,
        "height": height,
        "chest_cm": 0,
        "hip_cm": 0,
        "waist_cm": 0,
        "length_cm": 0,
        "skirt_cm": 0,
        "shoulder_cm": 0,
        "sleeve_cm": 0,
        "pant_cm": 0,
        "source_note": "The attached vendor chart only publishes body height and weight guidance; garment measurements were not invented.",
    }


chart = []
for vendor, picker, suffix, age, weight, height in size_rows:
    chart.append(blank_measure_row("child", "Girl Dress", "Dress", vendor, picker, suffix, age, weight, height))
for vendor, picker, suffix, weight, height in mother_rows:
    chart.append(blank_measure_row("mother", "Mother Dress", "Dress", vendor, picker, suffix, "—", weight, height))
for vendor, picker, suffix, age, weight, height in size_rows:
    chart.append(blank_measure_row("child", "Boy Shirt", "Shirt", vendor, picker, suffix, age, weight, height))
for vendor, picker, suffix, weight, height in father_rows:
    chart.append(blank_measure_row("father", "Father Shirt", "Shirt", vendor, picker, suffix, "—", weight, height))

size_metaobject_map = [
    {"picker_label": "Child 1-2 Years", "gid": "gid://shopify/Metaobject/129972797537", "catalog_label": "12-18 months", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 2 Years", "gid": "gid://shopify/Metaobject/129972863073", "catalog_label": "2-3 years", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 3 Years", "gid": "gid://shopify/Metaobject/129972895841", "catalog_label": "3-4 years", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 4 Years", "gid": "gid://shopify/Metaobject/129972928609", "catalog_label": "4-5 years", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 5 Years", "gid": "gid://shopify/Metaobject/129972961377", "catalog_label": "5-6 years", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 6-7 Years", "gid": "gid://shopify/Metaobject/139840323681", "catalog_label": "6-7 years", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 8 Years", "gid": "gid://shopify/Metaobject/129973026913", "catalog_label": "8", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Child 9-10 Years", "gid": "gid://shopify/Metaobject/129971552353", "catalog_label": "10", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Mother S", "gid": "gid://shopify/Metaobject/129975255137", "catalog_label": "S", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Mother M", "gid": "gid://shopify/Metaobject/129975222369", "catalog_label": "M", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Mother L", "gid": "gid://shopify/Metaobject/129975189601", "catalog_label": "L", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Mother XL", "gid": "gid://shopify/Metaobject/129975287905", "catalog_label": "XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Mother 2XL", "gid": "gid://shopify/Metaobject/129975156833", "catalog_label": "2XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father S", "gid": "gid://shopify/Metaobject/129975255137", "catalog_label": "S", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father M", "gid": "gid://shopify/Metaobject/129975222369", "catalog_label": "M", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father L", "gid": "gid://shopify/Metaobject/129975189601", "catalog_label": "L", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father XL", "gid": "gid://shopify/Metaobject/129975287905", "catalog_label": "XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father 2XL", "gid": "gid://shopify/Metaobject/129975156833", "catalog_label": "2XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father 3XL", "gid": "gid://shopify/Metaobject/139840421985", "catalog_label": "3XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
    {"picker_label": "Father 4XL", "gid": "gid://shopify/Metaobject/139840716897", "catalog_label": "4XL", "source_handle": SIZE_NEIGHBOR_HANDLE},
]
size_map = {row["picker_label"]: row for row in size_metaobject_map}

role_tokens = {"Girl Dress": "GRL", "Mother Dress": "MOM", "Boy Shirt": "BOY", "Father Shirt": "DAD"}
size_tokens = {
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
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Father S": "S",
    "Father M": "M",
    "Father L": "L",
    "Father XL": "XL",
    "Father 2XL": "2XL",
    "Father 3XL": "3XL",
    "Father 4XL": "4XL",
}

errors = []
seen_pairs = set()
for row in chart:
    for field in ("audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm"):
        if row.get(field) in (None, ""):
            errors.append(f"{row.get('vendor_label')} missing {field}")
    pair = (row["role"], row["picker_label"])
    if pair in seen_pairs:
        errors.append(f"duplicate role/picker pair {pair}")
    seen_pairs.add(pair)
    if row["role"] not in role_tokens:
        errors.append(f"unknown role token {row['role']}")
    if row["picker_label"] not in size_tokens:
        errors.append(f"unknown size token {row['picker_label']}")
    if row["picker_label"] not in size_map:
        errors.append(f"missing shopify.size map {row['picker_label']}")
if len(TITLE) > 70:
    errors.append("title too long")
if len(SEO_TITLE) > 60:
    errors.append("SEO title too long")
if len(SEO_DESCRIPTION) > 155:
    errors.append("SEO description too long")
if errors:
    raise SystemExit("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))

garments = []
size_values = []
seen_sizes = set()
for row in chart:
    if row["garment"] not in garments:
        garments.append(row["garment"])
    if row["picker_label"] not in seen_sizes:
        seen_sizes.add(row["picker_label"])
        size_values.append({"name": row["picker_label"]})
option_axes = [{"name": "Type", "values": garments}, {"name": "Size", "values": [row["name"] for row in size_values]}]
product_options = [{"name": axis["name"], "values": [{"name": value} for value in axis["values"]]} for axis in option_axes]


def sku_for(row):
    return f"DLM-{SHORTCODE}-{role_tokens[row['role']]}-{size_tokens[row['picker_label']]}-{COLOR_TOKEN}"


variants = []
recap = []
expected_variant_option_pairs = []
for row in chart:
    price = CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE
    compare = CHILD_COMPARE if row["audience"] == "child" else ADULT_COMPARE
    options = [row["garment"], row["picker_label"]]
    sku = sku_for(row)
    variants.append({
        "price": price,
        "compareAtPrice": compare,
        "taxable": True,
        "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": sku, "cost": half_cost(price), "tracked": True, "requiresShipping": True},
        "optionValues": [{"optionName": name, "name": value} for name, value in zip(["Type", "Size"], options)],
    })
    expected_variant_option_pairs.append(options)
    recap.append({
        **row,
        "sku": sku,
        "price": price,
        "compare_at_price": compare,
        "cost": half_cost(price),
        "shopify_size_gid": size_map[row["picker_label"]]["gid"],
        "catalog_label": size_map[row["picker_label"]]["catalog_label"],
        "option1_value": options[0],
        "option2_value": options[1],
    })


def dec(value):
    return Decimal(str(value))


def fmt_decimal(value):
    value = dec(value)
    return str(int(value)) if value == value.to_integral_value() else f"{value.normalize():f}"


def dual_range(text, metric, imperial, multiplier):
    if not text or text in {"—", "-", "--"}:
        return "&mdash;"
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*" + re.escape(metric), text)
    if match:
        low, high = dec(match.group(1)), dec(match.group(2))
        low_i = (low * dec(multiplier)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        high_i = (high * dec(multiplier)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return f"{fmt_decimal(low)}-{fmt_decimal(high)} {metric} / {fmt_decimal(low_i)}-{fmt_decimal(high_i)} {imperial}"
    return html.escape(text)


def cm_in(value):
    if not value:
        return "&mdash;"
    inches = (dec(value) / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{fmt_decimal(value)} cm / {fmt_decimal(inches)} in"


def li(label, text):
    return f"<li><strong>{label}:</strong> {html.escape(text)}</li>"


def table_row(row):
    return (
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{dual_range(row['weight'], 'kg', 'lbs', '2.20462')}</td>"
        f"<td>{dual_range(row['height'], 'cm', 'in', '0.3937007874')}</td>"
        f"<td>{cm_in(row['chest_cm'])}</td>"
        f"<td>{cm_in(row.get('skirt_cm') or row.get('shoulder_cm') or row.get('sleeve_cm') or 0)}</td>"
        f"<td>{cm_in(row['pant_cm'])}</td>"
        f"<td>{cm_in(row['hip_cm'])}</td>"
        f"<td>{cm_in(row['waist_cm'])}</td>"
        f"<td>{cm_in(row['length_cm'])}</td>"
        "</tr>"
    )


size_phrase = "Girls and boys 1-2Y through 10Y; Mother S-2XL; Father S-4XL"
dress_rows = [table_row(row) for row in chart if row["garment"] == "Dress"]
shirt_rows = [table_row(row) for row in chart if row["garment"] == "Shirt"]
body_html = "\n".join([
    "<ul>",
    li("Fabric", "Lightweight woven fabric with a breezy warm-weather feel; exact fiber content should be reconfirmed when the vendor page is readable."),
    li("Family story", "A coordinated four-role look for moms, dads, girls, and boys, made for vacations, family photos, birthdays, and easy summer outings."),
    li("Print", "Midnight Rose pairs bright pink rose clusters with a black ground for a bold, polished floral look."),
    li("Design details", "Girls and moms wear the black rose shoulder-strap dress, while boys and dads wear the matching short-sleeve collared button-front shirt. Black shorts shown in the supplied image are styling only and are not included."),
    li("Care", "Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed."),
    li("Size range", size_phrase + "."),
    "</ul>",
    "",
    "<h3>Size Chart - Dress</h3>",
    "<table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Skirt Length (cm/in)</th><th>Pant/Short or &mdash; (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody>",
    *dress_rows,
    "</tbody></table>",
    "",
    "<h3>Size Chart - Shirt</h3>",
    "<table id=\"size-chart-shirt\"><thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Shoulder or &mdash; (cm/in)</th><th>Pant/Short or &mdash; (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody>",
    *shirt_rows,
    "</tbody></table>",
    "",
    "<p>Midnight Rose gives the family matching look a little drama while keeping the silhouettes easy to wear. The women and girls dress carries the print in a breezy shoulder-strap shape, while the dad and boy shirt brings the same rose pattern into a relaxed collared style.</p>",
    "",
    "<p>The result is coordinated without feeling identical on everyone. Pair the shirts with black or linen shorts, and let the dresses carry the same bright floral story for resort dinners, family portraits, and warm weekend plans.</p>",
    "",
    "<h3>Key Features:</h3>",
    "<ul>",
    li("Four-role coordination", "One draft covers girl dress, mother dress, boy shirt, and father shirt sizes."),
    li("Bold rose print", "Pink florals over black create a photo-ready contrast that works beautifully outdoors."),
    li("Dress and shirt model", "The Type option separates the actual purchasable garments so shoppers can choose honest pieces."),
    li("Source-backed sizing", "Every variant is backed by a row from the attached height-and-weight vendor reference chart."),
    li("Styling note", "Shorts shown in the supplied image are styling only and not part of this listing."),
    "</ul>",
    "",
    "<p>Choose the dress and shirt sizes your family needs, then build a coordinated rose-print look that feels polished, sunny, and ready for photos.</p>",
])

tags = sorted(dict.fromkeys([
    "Family Matching", "Mommy and Me", "Daddy and Me", "Sets", "Matching Family Set",
    "Matching Family Outfits", "Matching Family Dress", "Matching Family Shirt",
    "Dress & Shirt", "Summer", "Vacation", "Resort", "Beach", "Midnight Rose",
    "Black Rose", "Rose Floral", "Pink Floral", "Black", "Pink", "Floral",
    "Shoulder Strap Dress", "Sleeveless Dress", "Short Sleeve Shirt", "Button Front Shirt",
    "Collared Shirt", "Girl Dress", "Mother Dress", "Boy Shirt", "Father Shirt",
    "Four-Role Matching", "Child 1-2 Years", "Child 2 Years", "Child 3 Years",
    "Child 4 Years", "Child 5 Years", "Child 6-7 Years", "Child 8 Years",
    "Child 9-10 Years", "Mother S", "Mother M", "Mother L", "Mother XL",
    "Mother 2XL", "Father S", "Father M", "Father L", "Father XL", "Father 2XL",
    "Father 3XL", "Father 4XL", VENDOR_URL,
]))

derived = {
    "use_type_option": True,
    "product_options": product_options,
    "option_axes": option_axes,
    "option_names": ["Type", "Size"],
    "size_values": size_values,
    "expected_variant_option_pairs": expected_variant_option_pairs,
    "variants": variants,
    "row_count": len(chart),
    "derived_skus_sorted": sorted(row["inventoryItem"]["sku"] for row in variants),
    "shopify_size_refs": list(dict.fromkeys(size_map[row["picker_label"]]["gid"] for row in chart)),
    "size_phrase": size_phrase,
    "tags": tags,
    "recap": recap,
}

SIZE_CHART_OUT.write_text(json.dumps(chart, indent=2, ensure_ascii=False), encoding="utf-8")
BODY_HTML_OUT.write_text(body_html, encoding="utf-8")

with tempfile.TemporaryDirectory() as tmp:
    tmpdir = Path(tmp)
    size_chart_tmp = tmpdir / "size-chart.json"
    derived_tmp = tmpdir / "derived.json"
    evidence_tmp = tmpdir / "vendor-evidence.json"
    size_chart_tmp.write_text(json.dumps(chart, ensure_ascii=False), encoding="utf-8")
    derived_tmp.write_text(json.dumps(derived, ensure_ascii=False), encoding="utf-8")
    evidence_tmp.write_text(json.dumps({
        "title": "Family matching black pink rose floral strap dress and collared short-sleeve shirt",
        "notes": "Attached product image shows mother/girl dresses and father shirt. Shorts are styling only.",
        "raw_detail_text": "童装尺码 婴儿爬服 成人尺码 妈妈 爸爸 dress shirt",
    }, ensure_ascii=False), encoding="utf-8")
    subprocess.run([
        "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
        "--size-chart", str(size_chart_tmp),
        "--derived", str(derived_tmp),
        "--vendor-evidence", str(evidence_tmp),
        "--primary-category", CATEGORY,
        "--tags", ",".join(tags),
    ], check=True, cwd=ROOT)

taxonomy = gql("query TaxonomyNode($id: ID!) { node(id: $id) { ... on TaxonomyCategory { id fullName } } }", {"id": TAXONOMY_GID})
taxonomy_full_name = taxonomy["data"]["node"]["fullName"]
if taxonomy_full_name != EXPECTED_TAXONOMY_FULL_NAME:
    raise SystemExit(f"Taxonomy mismatch: {taxonomy_full_name}")

try:
    req = urllib.request.Request(VENDOR_URL, headers={"User-Agent": "Mozilla/5.0"})
    direct_page = urllib.request.urlopen(req, timeout=20).read(2000).decode("utf-8", "ignore")
    vendor_fetch_status = "blocked" if "_____tmd_____" in direct_page or "punish" in direct_page.lower() or "captcha" in direct_page.lower() else "readable"
except (urllib.error.URLError, TimeoutError) as exc:
    vendor_fetch_status = f"blocked: {exc}"

existing_query = """
query ExistingProduct($handle: String!) {
  productByHandle(handle: $handle) {
    id handle status publishedAt
    options { id name values optionValues { id name hasVariants } }
    variants(first: 100) {
      nodes {
        id sku price compareAtPrice inventoryPolicy taxable
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
      }
    }
  }
}
"""
existing = gql(existing_query, {"handle": HANDLE})
product = existing["data"]["productByHandle"]
create_new = product is None
if product and (product["status"] != "DRAFT" or product["publishedAt"] is not None):
    raise SystemExit(f"Existing handle {HANDLE} is not an unpublished draft; refusing to alter publish state.")

if create_new:
    create = gql("""
    mutation ProductCreate($input: ProductInput!) {
      productCreate(input: $input) { product { id handle title status } userErrors { field message } }
    }
    """, {"input": {
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body_html,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": tags,
        "status": "DRAFT",
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
        "productOptions": product_options,
    }})
    user_errors(create, ["data", "productCreate", "userErrors"])
    product_id = create["data"]["productCreate"]["product"]["id"]
else:
    product_id = product["id"]

update = gql("""
mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) { product { id handle title status } userErrors { field message } }
}
""", {"product": {
    "id": product_id,
    "handle": HANDLE,
    "title": TITLE,
    "descriptionHtml": body_html,
    "vendor": VENDOR,
    "productType": PRODUCT_TYPE,
    "tags": tags,
    "status": "DRAFT",
    "category": TAXONOMY_GID,
    "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
}})
user_errors(update, ["data", "productUpdate", "userErrors"])

existing = gql(existing_query, {"handle": HANDLE})
product = existing["data"]["productByHandle"]
live_variants = product["variants"]["nodes"]
live_skus = sorted([row.get("sku") or "" for row in live_variants if row.get("sku")])
derived_skus = derived["derived_skus_sorted"]
should_create = False
should_update = False
if create_new or not live_variants or (len(live_variants) == 1 and not live_variants[0].get("sku")):
    should_create = True
elif len(live_variants) == len(chart) and live_skus == derived_skus:
    should_update = True
else:
    raise SystemExit(f"Existing draft handle {HANDLE} has unexpected variants; refusing to create duplicates.")

if should_create:
    response = gql("""
    mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
      productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
        productVariants { id sku }
        userErrors { field message }
      }
    }
    """, {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
    user_errors(response, ["data", "productVariantsBulkCreate", "userErrors"])

if should_update:
    by_sku = {row["inventoryItem"]["sku"]: row for row in variants}
    updates = []
    for node in live_variants:
        spec = dict(by_sku[node["sku"]])
        spec["id"] = node["id"]
        updates.append(spec)
    response = gql("""
    mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
      productVariantsBulkUpdate(productId: $productId, variants: $variants) {
        productVariants { id sku }
        userErrors { field message }
      }
    }
    """, {"productId": product_id, "variants": updates})
    user_errors(response, ["data", "productVariantsBulkUpdate", "userErrors"])

metafields = [
    {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": MERCH_SUBCATEGORY},
    {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": MERCH_SUBCATEGORY2},
    {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": "Midnight Rose Floral"},
    {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": MERCH_STYLE},
    {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": MERCH_TYPE},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Midnight Rose"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress & Shirt"},
    {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
    {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69943132257", "gid://shopify/Metaobject/69963645025", "gid://shopify/Metaobject/129971519585"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(derived["shopify_size_refs"])},
    {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
    {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
    {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
]
for index in range(0, len(metafields), 25):
    response = gql("""
    mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) { metafields { namespace key type value } userErrors { field message } }
    }
    """, {"metafields": metafields[index:index + 25]})
    user_errors(response, ["data", "metafieldsSet", "userErrors"])

media = gql("""
query ProductMedia($id: ID!) {
  product(id: $id) { media(first: 50) { nodes { ... on MediaImage { id alt image { url } } } } }
}
""", {"id": product_id})
existing_alts = {node.get("alt") or "" for node in media["data"]["product"]["media"]["nodes"]}


def multipart_post(url, fields, file_path, mime_type):
    boundary = "----DLM" + uuid.uuid4().hex
    body = bytearray()
    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'.encode())
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode())
    body.extend(file_path.read_bytes())
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(url, data=bytes(body), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        resp.read()


for image_path in sorted([p for p in UPLOAD_DIR.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]):
    alt_text = "Midnight Rose family matching dress and shirt set for moms, dads, girls, and boys."
    if alt_text in existing_alts:
        continue
    mime_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
    staged = gql("""
    mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } }
    }
    """, {"input": [{"filename": image_path.name, "mimeType": mime_type, "resource": "IMAGE", "httpMethod": "POST"}]})
    user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    multipart_post(target["url"], [(row["name"], row["value"]) for row in target["parameters"]], image_path, mime_type)
    created = gql("""
    mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
      productCreateMedia(productId: $productId, media: $media) { media { ... on MediaImage { id alt } } userErrors { field message } }
    }
    """, {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt_text}]})
    user_errors(created, ["data", "productCreateMedia", "userErrors"])

time.sleep(2)
verify = gql("""
query VerifyProduct($id: ID!) {
  product(id: $id) {
    id title handle status publishedAt onlineStoreUrl descriptionHtml tags
    seo { title description }
    category { id fullName }
    options { id name position values optionValues { id name hasVariants } }
    variants(first: 100) {
      nodes {
        id sku title price compareAtPrice inventoryPolicy taxable
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
      }
    }
    media(first: 50) { nodes { ... on MediaImage { alt image { url } } } }
    collections(first: 50) { nodes { title handle } }
    metafields(first: 100) { nodes { namespace key type value } }
    resourcePublicationsV2(first: 20) { nodes { isPublished publishDate publication { id name } } }
  }
}
""", {"id": product_id})
VERIFY_JSON_OUT.write_text(json.dumps(verify, indent=2, ensure_ascii=False), encoding="utf-8")
product = verify["data"]["product"]
live_variants = product["variants"]["nodes"]
metafield_keys = {(node["namespace"], node["key"]) for node in product["metafields"]["nodes"]}
live_skus_sorted = sorted(row["sku"] for row in live_variants)
option_names = derived["option_names"]
live_option_names = [row["name"] for row in product["options"]]
expected_pairs = {tuple(row) for row in derived["expected_variant_option_pairs"]}
live_pairs = set()
for variant in live_variants:
    option_map = {row["name"]: row["value"] for row in variant["selectedOptions"]}
    live_pairs.add(tuple(option_map.get(name) for name in option_names))
table_blocks = re.findall(r"<table[^>]*>(.*?)</table>", product["descriptionHtml"], re.S)
header_counts = [len(re.findall(r"<th>", block)) for block in table_blocks]
tbody_rows = []
for tbody in re.findall(r"<tbody>(.*?)</tbody>", product["descriptionHtml"], re.S):
    tbody_rows.extend(re.findall(r"<tr>(.*?)</tr>", tbody, re.S))
first_cells = []
for row_html in tbody_rows:
    cell = re.search(r"<td>(.*?)</td>", row_html, re.S)
    first_cells.append(re.sub(r"<.*?>", "", cell.group(1)).strip() if cell else "")
published_ids = [node["publication"]["id"] for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
required_written = {
    ("custom", "category1"), ("custom", "subcategory"), ("custom", "subcategory2"), ("custom", "pattern"), ("custom", "style"), ("custom", "type"),
    ("mm-google-shopping", "custom_product"), ("mm-google-shopping", "gender"), ("mm-google-shopping", "age_group"), ("mm-google-shopping", "condition"),
    ("mm-google-shopping", "custom_label_0"), ("mm-google-shopping", "custom_label_1"), ("mm-google-shopping", "custom_label_2"), ("mm-google-shopping", "custom_label_3"), ("mm-google-shopping", "custom_label_4"),
    ("shopify", "age-group"), ("shopify", "care-instructions"), ("shopify", "color-pattern"), ("shopify", "size"), ("shopify", "target-gender"),
    ("global", "title_tag"), ("global", "description_tag"),
}

checks = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("SEO description <= 155 chars", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("Live variant count matches SIZE_CHART", len(live_variants) == len(chart), f"{len(live_variants)} vs {len(chart)}"),
    ("Live SKUs match derived SKUs", live_skus_sorted == derived["derived_skus_sorted"], ", ".join(live_skus_sorted)),
    ("Live option axes match derived axes", live_option_names == option_names, " / ".join(live_option_names)),
    ("Every Type x Size combination exists", live_pairs == expected_pairs, str(sorted(live_pairs))),
    ("Size table first column matches picker labels", first_cells == [row["picker_label"] for row in chart], " | ".join(first_cells)),
    ("Each size table has 10 headers", header_counts and all(count == 10 for count in header_counts), str(header_counts)),
    ("Table row count matches SIZE_CHART", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("Vendor measurement omissions remain blank", all(row["waist_cm"] == 0 and row["chest_cm"] == 0 for row in chart), "height/weight-only chart"),
    ("Product status is DRAFT", product["status"] == "DRAFT", product["status"]),
    ("publishedAt is null", product["publishedAt"] is None, str(product["publishedAt"])),
    ("No sales-channel publication is live", not published_ids, str(sorted(published_ids))),
    ("Taxonomy category is set", product["category"]["id"] == TAXONOMY_GID, product["category"]["id"]),
    ("Taxonomy category full name matches expected leaf", product["category"]["fullName"] == EXPECTED_TAXONOMY_FULL_NAME, product["category"]["fullName"]),
    ("Family-set merchandising tag is present", MERCH_COLLECTION_TAG in product["tags"], ", ".join(product["tags"])),
    ("Applicable metafields are written", required_written.issubset(metafield_keys), str(sorted(required_written - metafield_keys))),
]

spec_by_sku = {row["sku"]: row for row in recap}
price_rows = []
price_drift = False
for variant in live_variants:
    spec = spec_by_sku[variant["sku"]]
    unit_cost = ((variant.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
    ok = (
        variant["price"] == spec["price"]
        and variant["compareAtPrice"] == spec["compare_at_price"]
        and unit_cost is not None
        and Decimal(unit_cost) == Decimal(spec["cost"])
        and variant["inventoryPolicy"] == "DENY"
        and variant["inventoryItem"]["tracked"] is True
        and variant["inventoryItem"]["requiresShipping"] is True
        and variant["taxable"] is True
    )
    price_drift = price_drift or not ok
    price_rows.append({
        "sku": variant["sku"], "live_price": variant["price"], "live_compare": variant["compareAtPrice"],
        "live_cost": f"{Decimal(unit_cost):.2f}" if unit_cost is not None else "",
        "spec_price": spec["price"], "spec_compare": spec["compare_at_price"], "spec_cost": spec["cost"],
        "match": "yes" if ok else "no",
    })

header = []
if CSV_HEADER_SOURCE.exists():
    with CSV_HEADER_SOURCE.open(newline="", encoding="utf-8") as fh:
        header = next(csv.reader(fh))
if not header:
    header = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Cost per item", "SEO Title", "SEO Description", "Status"]

csv_rows = []
for row in recap:
    record = {field: "" for field in header}
    def put(field, value):
        if field in record:
            record[field] = value
    put("Handle", HANDLE)
    put("Title", TITLE)
    put("Body (HTML)", product["descriptionHtml"])
    put("Vendor", VENDOR)
    put("Product Category", EXPECTED_TAXONOMY_FULL_NAME)
    put("Type", PRODUCT_TYPE)
    put("Tags", ", ".join(product["tags"]))
    put("Published", "FALSE")
    put("Option1 Name", "Type")
    put("Option1 Value", row["option1_value"])
    put("Option2 Name", "Size")
    put("Option2 Value", row["option2_value"])
    put("Variant SKU", row["sku"])
    put("Variant Grams", "0")
    put("Variant Inventory Tracker", "shopify")
    put("Variant Inventory Policy", "deny")
    put("Variant Fulfillment Service", "manual")
    put("Variant Price", row["price"])
    put("Variant Compare At Price", row["compare_at_price"])
    put("Variant Requires Shipping", "TRUE")
    put("Variant Taxable", "TRUE")
    put("Cost per item", row["cost"])
    put("SEO Title", SEO_TITLE)
    put("SEO Description", SEO_DESCRIPTION)
    put("Google Shopping / Gender", "unisex")
    put("Google Shopping / Age Group", "adult")
    put("Google Shopping / Condition", "new")
    put("Google Shopping / Custom Product", "FALSE")
    put("Google Shopping / Custom Label 0", "Family Matching")
    put("Google Shopping / Custom Label 1", "Midnight Rose")
    put("Google Shopping / Custom Label 2", "Summer")
    put("Google Shopping / Custom Label 3", "Dress & Shirt")
    put("Google Shopping / Custom Label 4", "Four-Role Matching")
    put("Category1 (product.metafields.custom.category1)", "Family Matching")
    put("Pattern (product.metafields.custom.pattern)", "Midnight Rose Floral")
    put("Style (product.metafields.custom.style)", MERCH_STYLE)
    put("SubCategory (product.metafields.custom.subcategory)", MERCH_SUBCATEGORY)
    put("SubCategory2 (product.metafields.custom.subcategory2)", MERCH_SUBCATEGORY2)
    put("Type (product.metafields.custom.type)", MERCH_TYPE)
    put("Color (product.metafields.shopify.color-pattern)", "Black, Pink, Floral")
    put("Size (product.metafields.shopify.size)", ", ".join(x["name"] for x in size_values))
    put("Target Gender (product.metafields.shopify.target-gender)", "Female, Male")
    put("Status", "draft")
    csv_rows.append(record)
with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writeheader()
    writer.writerows(csv_rows)

admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
skipped_metafields = {
    "shopify.clothing-features": "No current store catalog value honestly describes this lightweight summer family set.",
    "shopify.fabric": "The direct 1688 page was CAPTCHA-blocked and the attached chart/image do not confirm one exact fiber.",
    "shopify.dress-occasion": "The honest Shopify taxonomy is Outfit Sets, not Dresses.",
    "shopify.dress-style": "The product mixes dresses and shirts under Outfit Sets.",
    "shopify.fit": "No reliable writable standard Shopify metafield definition is available for this mixed outfit-set product.",
    "shopify.neckline": "The product-level neckline would be misleading across both dresses and collared shirts.",
    "shopify.pants-length-type": "Shorts are styling only and not included.",
    "shopify.skirt-dress-length-type": "The listing mixes dresses and shirts, so a dress-only length field would overstate scope.",
    "shopify.sleeve-length-type": "The listing mixes sleeveless dresses and short-sleeve shirts.",
    "shopify.top-length-type": "No single product-level top length is honest across dresses and shirts.",
    "shopify.waist-rise": "The vendor chart omits waist and garment measurements entirely; no product-level waist attribute was written.",
}
written = [node for node in product["metafields"]["nodes"] if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}]

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
    "| PRIMARY_CATEGORY | auto -> FamilySet (Shopify taxonomy: Outfit Sets) |",
    "| DESIGNS_TO_LIST | Dress, Shirt |",
    "| EXCLUDE_ITEMS | infant crawler rows excluded because Family Matching allowed roles are Girl, Mother, Boy, Father and the product image does not evidence a baby romper; shorts are styling only because no shorts rows exist |",
    f"| SHORTCODE | auto -> `{SHORTCODE}` |",
    f"| COLOR_TOKEN | auto -> `{COLOR_TOKEN}` |",
    "| FORCE_SPEC_PRICES | true |", "",
    "## Vendor fetch status",
    f"Direct 1688 fetch status: `{vendor_fetch_status}`. The attached size-chart image and supplied product image were used as authoritative evidence. The chart publishes only height and weight guidance, so chest, waist, hip, garment length, sleeve/shoulder, and pant/short measurements are intentionally blank instead of fabricated.", "",
    "## Title & SEO",
    "| | Value | Chars |", "|---|---|---|",
    f"| Product Title | `{product['title']}` | {len(product['title'])} |",
    f"| SEO Title | `{product['seo']['title']}` | {len(product['seo']['title'])} |",
    f"| SEO Description | `{product['seo']['description']}` | {len(product['seo']['description'])} |", "",
    "## SIZE_CHART recap",
    "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
    "|---|---|---|---|---|---|---|---|",
]
for row in recap:
    lines.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['option1_value']} | `{row['sku']}` | {row['price']} | {row['cost']} | `{row['shopify_size_gid']}` ({row['catalog_label']}) |")
lines.extend([
    "",
    "### Derivations and exclusions",
    "- Vendor weight guidance was converted from jin to kg, then rendered as kg/lbs in the storefront table.",
    "- The chart is a body size reference table only; garment measurements remain blank by design.",
    "- 80码 was mapped to Child 1-2 Years using the existing store size metaobject.",
    "- 90/100/110/120/130/140/150 mapped to Child 2/3/4/5/6-7/8/9-10 Years.",
    "- Mother S/M/L/XL/2XL and Father S/M/L/XL/2XL/3XL/4XL mapped directly.",
    "- Infant crawler rows 66/73/80/90 were excluded from this product because the allowed roles and supplied product image do not support a baby romper listing.",
    "",
    "## Option axes & variants",
])
for index, axis in enumerate(option_axes, start=1):
    lines.append(f"- Option {index}: `{axis['name']}` -> " + ", ".join(f"`{value}`" for value in axis["values"]))
lines.extend([f"- Variants live: **{len(live_variants)}**", "", "## Verify pass table", "| Check | Result | Detail |", "|---|---|---|"])
for label, ok, detail in checks:
    lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines.extend(["", "## Price and cost parity", "| SKU | Live Price | Live Cmp | Live Cost | Spec Price | Spec Cmp | Spec Cost | Match |", "|---|---|---|---|---|---|---|---|"])
for row in price_rows:
    lines.append(f"| {row['sku']} | {row['live_price']} | {row['live_compare']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare']} | {row['spec_cost']} | {row['match']} |")
lines.extend(["", "## Metafields written", "| Namespace.Key | Type | Value |", "|---|---|---|"])
for node in sorted(written, key=lambda row: (row["namespace"], row["key"])):
    value = node["value"]
    if len(value) > 90:
        value = value[:87] + "..."
    lines.append(f"| {node['namespace']}.{node['key']} | {node['type']} | `{value}` |")
lines.extend(["", "## Metafields skipped", "| Namespace.Key | Reason |", "|---|---|"])
for key, reason in skipped_metafields.items():
    lines.append(f"| {key} | {reason} |")
lines.extend([
    "",
    f"## Tags written ({len(product['tags'])})",
    "`" + ", ".join(product["tags"]) + "`",
    "",
    "## Publication",
    "- Product remains DRAFT.",
    "- Live URL: not published.",
    "- Sales-channel publication check: no live publication IDs returned.",
    "",
    "## Smart collections",
])
if product["collections"]["nodes"]:
    for collection in product["collections"]["nodes"]:
        lines.append(f"- {collection['title']} (`/{collection['handle']}`)")
else:
    lines.append("- No smart collection attachment is expected while the product remains an unpublished draft; Shopify indexing may attach collections later.")
lines.extend([
    "",
    "## Manual follow-ups",
    "- Replace or retouch the supplied product image before publication if the small source thumbnail/collage is not acceptable as storefront media.",
    "- Confirm exact fabric composition if the vendor page becomes readable later; `shopify.fabric` was intentionally skipped.",
    "- Request a garment-measurement chart before publication if chest, waist, hip, or length values are required on the PDP.",
    "- Inventory quantities and grams still need operator stock values.",
    "",
    "## Files saved",
    f"- `{SCRIPT_PATH}`",
    f"- `{LISTING_MD}`",
    f"- `{CSV_OUT}`",
    f"- `{VERIFY_JSON_OUT}`",
    f"- `{SIZE_CHART_OUT}`",
    f"- `{BODY_HTML_OUT}`",
    f"- `{UPLOAD_DIR}`",
    "",
    "## Sources",
    "- Attached size chart image from operator request.",
    "- Attached product image from operator request.",
    f"- Neighbor pricing: `{PRICE_NEIGHBOR_HANDLE}`.",
    f"- Size metaobject map: `{SIZE_NEIGHBOR_HANDLE}` and existing live size metaobjects.",
])
LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

failed = [label for label, ok, _detail in checks if not ok]
if price_drift:
    failed.append("Price/cost parity")
if failed:
    raise SystemExit("VERIFY FAILED: " + ", ".join(failed))

print(f"Admin URL: {admin_url}")
print("Live URL: not published")
print(f"Listing log: {LISTING_MD}")
print(f"CSV backup: {CSV_OUT}")
print(f"Variant count: {len(live_variants)}")
PY
