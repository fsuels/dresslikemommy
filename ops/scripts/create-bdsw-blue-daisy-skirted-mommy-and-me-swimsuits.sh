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
import time
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "blue-daisy-skirted-mommy-and-me-swimsuits"
TITLE = "Blue Daisy Mommy and Me Swimsuits - Skirted One-Piece"
SEO_TITLE = "Blue Daisy Mommy & Me Swim Dress | Dress Like Mommy"
SEO_DESCRIPTION = "Blue daisy mommy-and-me swim dresses for mom + daughter. Child 2Y-10Y and Mother M-3XL in a skirted one-piece style."
PRINT_NAME = "Blue Daisy"
SHORTCODE = "BDSW"
COLOR_TOKEN = "BDAISY"
COLOR_NAME = "Blue Daisy"
VENDOR_URL = ""
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Swimwear"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-20-17"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Swimwear > Swim Dresses"
CHILD_PRICE = "14.99"
ADULT_PRICE = "16.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / "01-product-image.png"
ADULT_SIZE_CHART_IMAGE = UPLOAD_DIR / "source-size-chart.png"
SELECTOR_SIZE_IMAGE = UPLOAD_DIR / "source-selector-child-sizes.png"
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"

SIZE_MAP = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}

SIZE_CHART = [
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children M",
        "picker_label": "Child 2 Years",
        "sku_suffix": "KID2Y",
        "age": "2-3",
        "weight": "7.5-12.5 kg / 16.5-27.6 lbs",
        "height": "80-100 cm / 31.5-39.4 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children S",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "12.5-17.5 kg / 27.6-38.6 lbs",
        "height": "100-110 cm / 39.4-43.3 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children XL",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "17.5-22.5 kg / 38.6-49.6 lbs",
        "height": "110-120 cm / 43.3-47.2 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children 2XL",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "22.5-27.5 kg / 49.6-60.6 lbs",
        "height": "120-130 cm / 47.2-51.2 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children 3XL",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "27.5-37.5 kg / 60.6-82.7 lbs",
        "height": "130-140 cm / 51.2-55.1 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "child",
        "role": "Girl Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Children 4XL",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "37.5-50 kg / 82.7-110.2 lbs",
        "height": "140-150 cm / 55.1-59.1 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "-",
        "length_display": "-",
    },
    {
        "audience": "mother",
        "role": "Mother Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Adult M",
        "picker_label": "Mother M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "up to 45 kg / up to 99.2 lbs",
        "height": "150-165 cm / 59.1-65.0 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "up to 66.7 cm / up to 26.2 in",
        "length_display": "-",
    },
    {
        "audience": "mother",
        "role": "Mother Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Adult L",
        "picker_label": "Mother L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "45-52.5 kg / 99.2-115.7 lbs",
        "height": "155-165 cm / 61.0-65.0 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "66.7-73.3 cm / 26.2-28.9 in",
        "length_display": "-",
    },
    {
        "audience": "mother",
        "role": "Mother Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Adult XL",
        "picker_label": "Mother XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "52.5-60 kg / 115.7-132.3 lbs",
        "height": "160-170 cm / 63.0-66.9 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "73.3-80.0 cm / 28.9-31.5 in",
        "length_display": "-",
    },
    {
        "audience": "mother",
        "role": "Mother Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Adult 2XL",
        "picker_label": "Mother 2XL",
        "sku_suffix": "2XL",
        "age": "-",
        "weight": "60-67.5 kg / 132.3-148.8 lbs",
        "height": "160-175 cm / 63.0-68.9 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "80.0-86.7 cm / 31.5-34.1 in",
        "length_display": "-",
    },
    {
        "audience": "mother",
        "role": "Mother Swimsuit",
        "garment": "Swimsuit",
        "vendor_label": "Adult 3XL",
        "picker_label": "Mother 3XL",
        "sku_suffix": "3XL",
        "age": "-",
        "weight": "67.5-75 kg / 148.8-165.3 lbs",
        "height": "165-175 cm / 65.0-68.9 in",
        "chest_display": "-",
        "skirt_display": "-",
        "pant_display": "-",
        "hip_display": "-",
        "waist_display": "86.7-90.0 cm / 34.1-35.4 in",
        "length_display": "-",
    },
]


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
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


def price_for(row: dict) -> str:
    return ADULT_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict) -> str:
    role_token = "MOM" if row["audience"] == "mother" else "GRL"
    return f"DLM-{SHORTCODE}-{role_token}-{row['sku_suffix']}-{COLOR_TOKEN}"


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
                    {"optionName": "Size", "name": row["picker_label"]},
                    {"optionName": "Color", "name": COLOR_NAME},
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
        "Mommy and Me",
        "Swimsuits",
        "Matching Family Swimwear",
        "Matching Swimwear",
        "Girl Swimsuit",
        "Mother Swimsuit",
        "Swim Dress",
        "Swim Dresses",
        "One-Piece Swimsuit",
        "Skirted Swimsuit",
        "Blue",
        "Daisy",
        "Floral",
        "Beach",
        "Pool",
        "Resort",
        "Summer",
        "Vacation",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Swimsuits"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Swim Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Skirted One-Piece"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Swimsuit"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Skirted One-Piece"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/69963645025"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "fabric", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69622366305"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def row_to_tr(row: dict) -> str:
    cells = [
        row["picker_label"],
        "" if row["audience"] == "mother" else row["age"],
        row["weight"],
        row["height"],
        row["chest_display"],
        row["skirt_display"],
        row["pant_display"],
        row["hip_display"],
        row["waist_display"],
        row["length_display"],
    ]
    return "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"


def build_body() -> str:
    rows = "\n".join(row_to_tr(row) for row in SIZE_CHART)
    return f"""<ul>
<li><strong>Fabric &amp; feel:</strong> Smooth stretch swim fabric with a skirted one-piece silhouette for an easy poolside fit.</li>
<li><strong>Family story:</strong> A coordinated mom-and-daughter swimsuit moment made for beach days, pool mornings, and vacation photos.</li>
<li><strong>Print:</strong> Blue daisy florals on a soft blue ground keep the matching look bright, sweet, and photo-ready.</li>
<li><strong>Design details:</strong> Halter-style neckline, skirt overlay, and coordinated daisy print shown for both mother and daughter styles.</li>
<li><strong>Care:</strong> Rinse after swimming, hand wash cold, line dry in the shade, and avoid bleach or rough poolside surfaces.</li>
<li><strong>Size range:</strong> Girls Child 2 Years to Child 9-10 Years; Mother M to Mother 3XL.</li>
</ul>

<h3>Size Chart - Swim Dress</h3>
<table id="size-chart">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Weight (kg/lbs)</th>
      <th>Height (cm/in)</th>
      <th>Chest/Bust (cm/in)</th>
      <th>Skirt Length (cm/in)</th>
      <th>Pant/Short or - (cm/in)</th>
      <th>Hip (cm/in)</th>
      <th>Waist (cm/in)</th>
      <th>Garment Length (cm/in)</th>
    </tr>
  </thead>
  <tbody>
{rows}
  </tbody>
</table>

<p>The Blue Daisy Mommy and Me Swimsuits bring a soft floral swim-dress look to mother-daughter matching. The daisy print feels cheerful for sunny photos, while the skirted one-piece shape keeps the set easy for pool days, resort mornings, and beach vacations.</p>

<p>The girls' and moms' suits coordinate through the same blue floral print and skirted silhouette. Use the chart-backed height and weight guidance for each swimmer, and keep unsupported garment measurements as a dash rather than guessing beyond the vendor evidence.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Blue daisy print:</strong> A fresh floral pattern that reads sweet, bright, and easy to match in family photos.</li>
<li><strong>Skirted one-piece shape:</strong> The swim-dress overlay gives the set a polished beachwear look.</li>
<li><strong>Mother-daughter sizing:</strong> Child rows come from the visible selector guidance and mother rows come from the attached adult chart.</li>
<li><strong>Vacation-ready match:</strong> Made for pool days, beach trips, resort photos, and coordinated summer memories.</li>
</ul>

<p>Choose the sizes you need and pack a matching daisy swim look for beach days, poolside photos, and sunny family memories.</p>"""


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
    for variant in variants:
        sku = variant["inventoryItem"]["sku"]
        if "1688" in sku.lower() or "alibaba" in sku.lower():
            raise RuntimeError("source URL token leaked into SKU")


def upload_media(product_id: str, existing_media: list[dict]) -> None:
    existing_alts = {node.get("alt") for node in existing_media}
    media_items = [
        (PRODUCT_IMAGE, "Blue Daisy Mommy and Me skirted swimsuit product image"),
    ]
    for path, alt in media_items:
        if not path.exists() or alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        staged = gql(
            """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""",
            {
                "input": [
                    {
                        "filename": path.name,
                        "mimeType": mime,
                        "httpMethod": "POST",
                        "resource": "IMAGE",
                    }
                ]
            },
        )
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMBOUNDARY"
        chunks = []
        for param in target["parameters"]:
            chunks.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{param['name']}\"\r\n\r\n{param['value']}\r\n".encode()
            )
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
            + path.read_bytes()
            + b"\r\n"
        )
        chunks.append(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(
            target["url"],
            data=b"".join(chunks),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        urllib.request.urlopen(req).read()
        media = gql(
            """mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""",
            {
                "productId": product_id,
                "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}],
            },
        )
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    header = (ROOT / "ops/listings/blush-garden-mommy-and-me-swimsuits-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    tags_text = ", ".join(tags())
    for i, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update(
            {
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
                "Variant Grams": "250",
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
                "Google Shopping / Custom Label 3": "Skirted One-Piece" if i == 1 else "",
                "Google Shopping / Custom Label 4": "Two-Role Matching" if i == 1 else "",
                "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
                "Style (product.metafields.custom.style)": "Skirted One-Piece" if i == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Swimsuits" if i == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Swim Dresses" if i == 1 else "",
                "Type (product.metafields.custom.type)": "Swimsuit" if i == 1 else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def product_query(product_id_or_handle: str, *, by_handle: bool = False) -> dict | None:
    fragment = """id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{alt image{url}}}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:50){nodes{isPublished publishDate publication{id name}}}"""
    if by_handle:
        data = gql(f"""query($handle:String!){{ productByHandle(handle:$handle){{ {fragment} }} }}""", {"handle": product_id_or_handle})
        return data["data"]["productByHandle"]
    data = gql(f"""query($id:ID!){{ product(id:$id){{ {fragment} }} }}""", {"id": product_id_or_handle})
    return data["data"]["product"]


def unpublish(product_id: str, product: dict) -> None:
    publications = [
        {"publicationId": node["publication"]["id"]}
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    ]
    if not publications:
        return
    res = gql(
        """mutation($id:ID!,$input:[PublicationInput!]!){ publishableUnpublish(id:$id,input:$input){ userErrors{field message} } }""",
        {"id": product_id, "input": publications},
    )
    require_no_user_errors(res, ["data", "publishableUnpublish", "userErrors"])


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict], created_skus: list[str], deleted_skus: list[str]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |"
        )
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    live_publications = [node["publication"]["name"] for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached adult chart plus attached selector screenshot with child rows |",
        "| LISTING_MODE | Mommy and Me |",
        "| PRIMARY_CATEGORY | Swimsuits -> Swim Dresses |",
        "| DESIGNS_TO_LIST | auto -> Blue floral print only |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned anti-bot/CAPTCHA markup, so the attached product image, adult chart, and selector screenshot were used as authoritative evidence per the canonical workflow.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---:|---:|---|",
        *recap,
        "",
        "## Derivations",
        "- The child rows come from the visible selector screenshot for the selected `Blue floral print`: Children M, S, XL, 2XL, 3XL, and 4XL.",
        "- The mother rows come from the attached adult chart. Adult 3XL is retained because the adult chart publishes it, even though the selector screenshot is scrolled after Adult 2XL.",
        "- This is a fit-recommendation table, not a garment-measurement table. Unsupported chest, hip, skirt, pant, and length cells are kept as `-` instead of being fabricated.",
        "- Pricing follows nearby live mommy-and-me swimsuit patterns: child `14.99`, mother `16.99`; Cost per item is exactly 50%.",
        "- The 1688 URL is kept only in local operator evidence, not in Shopify title/body/tags/metafields or CSV customer/feed-visible fields.",
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
        f"| Deleted stale SKUs | INFO | {', '.join(deleted_skus) if deleted_skus else 'none'} |",
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
        "## Smart Collections",
        "Collection indexing may wait until publication because this product is intentionally unpublished as a draft.",
        "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition if the vendor page becomes readable later.",
        "- Review or retouch the supplied product image before any publish-live step.",
        "- Inventory quantities and variant grams remain operator stock inputs.",
        "",
        "## Files Saved",
        f"- `{ROOT / 'ops/scripts/create-bdsw-blue-daisy-skirted-mommy-and-me-swimsuits.sh'}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


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
    if [option["name"] for option in product["options"]] != ["Size", "Color"]:
        errors.append("option axes are not Size / Color")
    expected_pairs = {(row["picker_label"], COLOR_NAME) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Size x Color option combinations do not match")
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
    if "1688" in joined_product_data or "alibaba" in joined_product_data or "detail.1688" in joined_product_data:
        errors.append("source URL leaked into Shopify product data")
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


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{id fullName isLeaf} } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

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

    product = product_query(HANDLE, by_handle=True)
    if product and product["status"] == "DRAFT":
        raise RuntimeError(f"Existing product {HANDLE} is ACTIVE; refusing draft-only update")
    if product:
        product_id = product["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        unpublish(product_id, product)
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]

    product = product_query(product_id)
    assert product is not None
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    delete_ids = [variant["id"] for sku, variant in live_by_sku.items() if sku not in spec_by_sku]
    deleted_skus = sorted(sku for sku in live_by_sku if sku not in spec_by_sku)
    if delete_ids:
        res = gql("""mutation($productId:ID!,$ids:[ID!]!){ productVariantsBulkDelete(productId:$productId, variantsIds:$ids){ product{id} userErrors{field message} } }""", {"productId": product_id, "ids": delete_ids})
        require_no_user_errors(res, ["data", "productVariantsBulkDelete", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    create_variants = [variant for sku, variant in spec_by_sku.items() if sku not in live_by_sku]
    created_skus = sorted(variant["inventoryItem"]["sku"] for variant in create_variants)
    if create_variants:
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {"productId": product_id, "variants": create_variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
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
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {"productId": product_id, "variants": update_variants})
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
    write_listing(product_id, verify, variants, price_rows, created_skus, deleted_skus)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(
        json.dumps(
            {
                "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
                "status": verify["status"],
                "publishedAt": verify["publishedAt"],
                "onlineStoreUrl": verify["onlineStoreUrl"],
                "variant_count": len(verify["variants"]["nodes"]),
                "price_cost_parity": all(row["match"] for row in price_rows),
                "source_url_leak_check": "pass",
                "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT), str(SIZE_CHART_OUT), str(BODY_HTML_OUT)],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
PY
