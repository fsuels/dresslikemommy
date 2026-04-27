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
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "pastel-watercolor-mommy-and-me-dresses"
TITLE = "Pastel Watercolor Mommy and Me Dresses - Airy Layered Look"
SEO_TITLE = "Pastel Watercolor Matching Dress | Dress Like Mommy"
SEO_DESCRIPTION = "Lightweight pastel floral mommy-and-me dresses for mom + daughter. Size chart supports Child 1-2Y-10Y and Mother S-2XL."
PRINT_NAME = "Pastel Watercolor"
SHORTCODE = "PWAT"
COLOR_TOKEN = "PASTEL"
COLOR_NAME = "Pastel Watercolor"
VENDOR_URL = "not supplied"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Dresses"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-4"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Dresses"
CHILD_PRICE = "31.99"
ADULT_PRICE = "34.99"

SCRIPT_PATH = ROOT / "ops/scripts/create-pwat-pastel-watercolor-mommy-and-me-dresses.sh"
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
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
}

SIZE_CHART = [
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"80","picker_label":"Child 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"8.5-11 kg","height":"75-85 cm","chest_cm":63,"hip_cm":67,"waist_cm":63,"length_cm":58,"skirt_cm":58,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11-14 kg","height":"85-95 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":63,"skirt_cm":63,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14-16.5 kg","height":"95-105 cm","chest_cm":69,"hip_cm":73,"waist_cm":69,"length_cm":68,"skirt_cm":68,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16.5-20 kg","height":"105-115 cm","chest_cm":72,"hip_cm":76,"waist_cm":72,"length_cm":73,"skirt_cm":73,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"18.5-24 kg","height":"115-125 cm","chest_cm":75,"hip_cm":79,"waist_cm":75,"length_cm":78,"skirt_cm":78,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"24-27.5 kg","height":"125-130 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":83,"skirt_cm":83,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":81,"hip_cm":85,"waist_cm":81,"length_cm":88,"skirt_cm":88,"sleeve_cm":0,"pant_cm":0},
    {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-37.5 kg","height":"140-150 cm","chest_cm":84,"hip_cm":88,"waist_cm":84,"length_cm":93,"skirt_cm":93,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"-","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":86,"hip_cm":92,"waist_cm":84,"length_cm":100,"skirt_cm":100,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"50-57.5 kg","height":"160-165 cm","chest_cm":90,"hip_cm":96,"waist_cm":88,"length_cm":102,"skirt_cm":102,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"59-69 kg","height":"160-170 cm","chest_cm":94,"hip_cm":100,"waist_cm":92,"length_cm":104,"skirt_cm":104,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"70-80 kg","height":"160-175 cm","chest_cm":98,"hip_cm":104,"waist_cm":96,"length_cm":106,"skirt_cm":106,"sleeve_cm":0,"pant_cm":0},
    {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"80-92.5 kg","height":"160-175 cm","chest_cm":102,"hip_cm":108,"waist_cm":100,"length_cm":108,"skirt_cm":108,"sleeve_cm":0,"pant_cm":0},
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


def cm_to_in(value) -> str:
    if value in (None, "", 0, "-", "0"):
        return "-"
    number = float(value)
    return f"{number:g} cm / {number / 2.54:.1f} in"


def range_to_imperial(text: str, factor: float, unit: str) -> str:
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if len(nums) >= 2:
        left, right = nums[0], nums[1]
        return f"{left:g}-{right:g} {unit} / {left * factor:.1f}-{right * factor:.1f} {'lbs' if unit == 'kg' else 'in'}"
    return text


def role_token(role: str) -> str:
    return "GRL" if role.startswith("Girl") else "MOM"


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "mother" else CHILD_PRICE


def build_body() -> str:
    headers = ["Size", "Age", "Weight (kg/lbs)", "Height (cm/in)", "Chest/Bust (cm/in)", "Skirt Length (cm/in)", "Pant/Short or - (cm/in)", "Hip (cm/in)", "Waist (cm/in)", "Garment Length (cm/in)"]
    rows = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "",
            range_to_imperial(row["weight"], 2.20462, "kg"),
            range_to_imperial(row["height"], 1 / 2.54, "cm"),
            cm_to_in(row["chest_cm"]),
            cm_to_in(row["skirt_cm"]),
            "-",
            cm_to_in(row["hip_cm"]),
            cm_to_in(row["waist_cm"]),
            cm_to_in(row["length_cm"]),
        ]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>")

    return "\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight sheer layered polyester fabric; exact fiber composition was not visible in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> A soft mother-daughter dress moment for sunny photos, garden days, vacations, and weekend celebrations.</li>",
        "<li><strong>Print reference:</strong> Pastel Watercolor blends pink, peach, yellow, and green floral washes over an airy light ground.</li>",
        "<li><strong>Design details:</strong> Sleeveless gathered neckline, flowing overlay, and a layered skirt-style silhouette shown for both mom and daughter.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>",
        "<li><strong>Size range:</strong> Child 1-2 Years through Child 9-10 Years, plus Mother S through Mother 2XL.</li>",
        "</ul>",
        "",
        "<h3>Size Chart - Dress</h3>",
        "<table id=\"size-chart\">",
        "<thead><tr>",
        *[f"<th>{h}</th>" for h in headers],
        "</tr></thead><tbody>",
        *rows,
        "</tbody></table>",
        "",
        "<p>Pastel Watercolor brings mom and daughter into the same breezy floral story without making the look feel too formal. The soft layered shape, sleeveless neckline, and painterly colors make it easy for family photos, outdoor parties, and warm-weather trips.</p>",
        "",
        "<p>The attached chart is fit-reference-only, so the variants are anchored to the vendor's published height and weight rows while garment measurements are carried from the closest live Dress Like Mommy dress grading for an honest shopper table.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Mother-daughter sizing:</strong> Girl and Mother dress rows only, per the request.</li>",
        "<li><strong>Pastel floral palette:</strong> Pink, peach, yellow, and green tones coordinate softly for photos.</li>",
        "<li><strong>Airy layered look:</strong> Sleeveless overlay styling keeps the dress light and movement-friendly.</li>",
        "<li><strong>Chart-backed variants:</strong> Every live variant maps to a row from the attached size chart.</li>",
        "<li><strong>Draft-only review:</strong> Created unpublished so merchandising can review duplication and fabric details before launch.</li>",
        "</ul>",
        "",
        "<p>Choose your matching sizes and build a soft, photo-ready mommy-and-me dress look for the next sunny family plan.</p>",
    ])


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        variants.append({
            "price": price,
            "compareAtPrice": compare_at(price),
            "inventoryPolicy": "DENY",
            "optionValues": [
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": COLOR_NAME},
            ],
            "inventoryItem": {
                "sku": f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}",
                "tracked": True,
                "requiresShipping": True,
            },
        })
    return variants


def tags() -> list[str]:
    values = [
        "Mommy and Me", "Dresses", "Matching Family Dresses", "Matching Family Dress",
        "Girl Dress", "Mother Dress", "Sleeveless Dress", "Midi Dress", "Sundress",
        "Pastel", "Watercolor", "Floral", "Garden", "Pink", "Peach", "Yellow", "Green",
        "Summer", "Vacation", "Resort", "Mom Size S", "Mom Size M", "Mom Size L",
        "Mom Size XL", "Mom Size 2XL", "Child 1-2yr", "Child 2-3yr", "Child 4-5yr",
        "Child 6-8yr", "Child 9-10yr",
    ]
    if VENDOR_URL != "not supplied":
        values.append(VENDOR_URL)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Airy Layered Dress"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Sleeveless Dress"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "care-instructions", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130283503713"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971519585", "gid://shopify/Metaobject/130231140449", "gid://shopify/Metaobject/69639766113"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "dress-occasion", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622169697", "gid://shopify/Metaobject/69622202465"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "dress-style", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130282520673"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "neckline", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972469857"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "skirt-dress-length-type", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/130282487905"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "sleeve-length-type", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622268001"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def validate_preflight(body: str, variants: list[dict]) -> None:
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm"}
    if len(SIZE_CHART) != 13 or len(variants) != len(SIZE_CHART):
        raise RuntimeError("SIZE_CHART/variant count mismatch")
    for row in SIZE_CHART:
        missing = [key for key in required if row.get(key) in (None, "")]
        if missing:
            raise RuntimeError(f"Missing fields in {row['picker_label']}: {missing}")
    if len(TITLE) > 70 or len(SEO_TITLE) > 60 or len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("Title or SEO length guard failed")
    if len({(r["role"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("Duplicate role/picker pair")
    if body.count("<tr>") - 1 != len(SIZE_CHART):
        raise RuntimeError("Body row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("One or more size tables does not have 10 headers")
    for row, variant in zip(SIZE_CHART, variants):
        if variant["price"] != price_for(row):
            raise RuntimeError("FORCE_SPEC_PRICES guard failed")


def run_variant_model_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Size", "Color"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"raw_detail_text": "Pastel watercolor mother daughter sleeveless dress. 连衣裙"}), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(chart),
            "--derived", str(derived),
            "--vendor-evidence", str(evidence),
            "--primary-category", "Dresses",
            "--tags", ", ".join(tags()),
        ], check=True)


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql("""query($id:ID!){ product(id:$id){ media(first:50){ nodes{ ... on MediaImage{ alt } } } } }""", {"id": product_id})
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    alt_by_name = {
        "01-family-look.png": "Mother and daughter wearing pastel watercolor matching dresses.",
        "source-size-chart.png": "Vendor size chart for Pastel Watercolor mommy and me dresses.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        alt = alt_by_name.get(path.name, "Pastel Watercolor mommy and me dresses.")
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
    header = (ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text().splitlines()[0].split(",")
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
            "Google Shopping / Gender": "female" if i == 1 else "",
            "Google Shopping / Age Group": "adult" if i == 1 else "",
            "Google Shopping / Condition": "new" if i == 1 else "",
            "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
            "Google Shopping / Custom Label 0": "Mommy and Me" if i == 1 else "",
            "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
            "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Sleeveless Dress" if i == 1 else "",
            "Google Shopping / Custom Label 4": "Two-Role Matching" if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Airy Layered Dress" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Dresses" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Dresses" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Dress" if i == 1 else "",
            "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
            "Status": "draft",
        })
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, variants: list[dict], verify: dict) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {COLOR_NAME} | `{variant['inventoryItem']['sku']}` | {variant['price']} | `{gid}` ({label}) |")
    skipped = [
        ("shopify.fabric", "Exact fiber composition was not visible; dress copy uses lightweight sheer layered polyester as a conservative visual inference, but no fabric metafield was written."),
        ("shopify.top-length-type", "Does not apply to a dress listing."),
    ]
    live_skus = sorted(v["sku"] for v in verify["variants"]["nodes"])
    spec_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
    price_ok = all(v["price"] == next(spec["price"] for spec in variants if spec["inventoryItem"]["sku"] == v["sku"]) for v in verify["variants"]["nodes"])
    lines = [
        f"# {TITLE}", "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        "- **Vendor:** not supplied",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`", "",
        "## Inputs (resolved)",
        "| Field | Value |", "|---|---|",
        "| VENDOR_URL | not supplied |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Mommy and Me |",
        "| PRIMARY_CATEGORY | Dresses |",
        "| DESIGNS_TO_LIST | only dress |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |", "",
        "## Source Notes",
        "The attached product image and attached size-chart image were used as authoritative evidence because no vendor URL was supplied. The chart includes child rows, infant crawler rows, mother rows, and father rows; this listing includes only the child dress rows and mother dress rows requested for Mommy and Me. Infant crawler and father rows were excluded.",
        "",
        "The attached size chart is fit-reference-only: it publishes height and body-weight guidance but not garment chest, waist, hip, or length measurements. To keep the storefront size table complete and rerunnable, garment measurements were backfilled from the closest live `pastel-bloom-mommy-and-me-dresses` dress grading curve and extended for missing S/XL/2XL rows. The vendor height/weight rows remain the source of truth for which variants exist.",
        "",
        "A live product named `pastel-bloom-mommy-and-me-dresses` already exists and appears visually related. This run created a separate unpublished draft under a distinct handle to avoid altering a live product's publish state.", "",
        "## Title & SEO",
        "| Field | Value | Chars |", "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |", "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Color | SKU | Price | shopify.size GID |",
        "|---|---|---|---|---|---|---|",
        *recap, "",
        "## Verification",
        "| Check | Result | Detail |", "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Live SKUs match derived SKUs | {'PASS' if live_skus == spec_skus else 'FAIL'} | {len(spec_skus)} expected |",
        f"| Price parity | {'PASS' if price_ok else 'FAIL'} | FORCE_SPEC_PRICES=true |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Publications not live | {'PASS' if not any(p['isPublished'] for p in verify['resourcePublicationsV2']['nodes']) else 'FAIL'} | {[p['publication']['name'] for p in verify['resourcePublicationsV2']['nodes'] if p['isPublished']]} |", "",
        "## Metafields Written",
        *[f"- `{m['namespace']}.{m['key']}`" for m in verify["metafields"]["nodes"] if m["namespace"] not in {"judgeme"}], "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped], "",
        "## Smart Collections",
        "Collection indexing may wait until publication because the product is an unpublished draft.", "",
        "## Manual Follow-ups",
        "- Decide whether this draft should replace, merge into, or remain separate from the existing live Pastel Bloom listing.",
        "- Confirm exact fabric composition before publishing.",
        "- Inventory quantities and per-variant weights still need operator stock values.", "",
        "## Files saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`", "",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)
    run_variant_model_guard()

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    existing = gql("""query($handle:String!){ productByHandle(handle:$handle){ id status variants(first:100){nodes{id sku selectedOptions{name value}}} } }""", {"handle": HANDLE})["data"]["productByHandle"]
    product_options = [
        {"name": "Size", "values": [{"name": value} for value in list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART))]},
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
        live_by_pair = {
            tuple(option["value"] for option in variant["selectedOptions"]): variant
            for variant in existing["variants"]["nodes"]
        }
        update_payload = []
        for spec in variants:
            pair = tuple(value["name"] for value in spec["optionValues"])
            if pair not in live_by_pair:
                raise RuntimeError(f"Existing draft is missing expected variant option pair: {pair}")
            update_payload.append({
                "id": live_by_pair[pair]["id"],
                "price": spec["price"],
                "compareAtPrice": spec["compareAtPrice"],
                "inventoryPolicy": "DENY",
                "optionValues": spec["optionValues"],
                "inventoryItem": spec["inventoryItem"],
            })
        bulk_update = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy} userErrors{field message} } }""", {
            "productId": product_id,
            "variants": update_payload,
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
    write_listing(product_id, variants, verify)
    print(json.dumps({
        "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "onlineStoreUrl": verify["onlineStoreUrl"],
        "variant_count": len(verify["variants"]["nodes"]),
        "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
