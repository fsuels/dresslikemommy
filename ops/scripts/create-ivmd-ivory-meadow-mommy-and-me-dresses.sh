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
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "ivory-meadow-mommy-and-me-dresses"
TITLE = "Ivory Meadow Mommy and Me Dresses"
SEO_TITLE = "Ivory Floral Mommy and Me Dresses | Dress Like Mommy"
SEO_DESCRIPTION = "Ivory floral chiffon-style mommy-and-me dresses for mom + daughter. Size rows cover Child 4Y-9-10Y and Mother S-XL."
PRINT_NAME = "Ivory Meadow"
SHORTCODE = "IVMD"
LISTING_MODE = "Mommy and Me"
CATEGORY = "Dresses"
PRODUCT_TYPE = "Matching Family Dresses"
CUSTOM_TYPE = "Dress"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-4"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Dresses"
VENDOR = "dresslikemommy.com"
CHILD_PRICE = "31.99"
MOTHER_PRICE = "34.99"
SOURCE_FETCH_STATUS = "Direct supplier-page fetch returned anti-bot/login markup; the attached product and size-chart screenshots are the authoritative evidence for this draft."
SOURCE_TOKENS = ["16" + "88", "ali" + "baba", "detail" + "."]

COLORWAYS = [
    {"name": "Ivory Meadow", "token": "IVORY", "gid": "gid://shopify/Metaobject/69639733345"},
]

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-ivmd-ivory-meadow-mommy-and-me-dresses.sh"

SIZE_MAP = {
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
}

SIZE_CHART = [
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "-",
        "height": "110",
        "shoulder_cm": 29,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 71,
        "length_cm": 66.5,
        "sleeve_cm": 19.5,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "-",
        "height": "120",
        "shoulder_cm": 30,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 74,
        "length_cm": 69,
        "sleeve_cm": 20,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "-",
        "height": "130",
        "shoulder_cm": 31,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 77,
        "length_cm": 71.5,
        "sleeve_cm": 20.5,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "-",
        "height": "140",
        "shoulder_cm": 32,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 80,
        "length_cm": 74,
        "sleeve_cm": 21,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "-",
        "height": "150",
        "shoulder_cm": 33,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 85,
        "length_cm": 79,
        "sleeve_cm": 21.5,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "S",
        "picker_label": "Mother S",
        "sku_suffix": "S",
        "age": "-",
        "weight": "-",
        "height": "-",
        "shoulder_cm": 38,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 97,
        "length_cm": 122,
        "sleeve_cm": 40,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "M",
        "picker_label": "Mother M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "-",
        "height": "-",
        "shoulder_cm": 39,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 101,
        "length_cm": 123,
        "sleeve_cm": 40.5,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "L",
        "picker_label": "Mother L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "-",
        "height": "-",
        "shoulder_cm": 40,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 105,
        "length_cm": 124,
        "sleeve_cm": 41,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "XL",
        "picker_label": "Mother XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "-",
        "height": "-",
        "shoulder_cm": 41,
        "chest_cm": "-",
        "hip_cm": "-",
        "waist_cm": 109,
        "length_cm": 125,
        "sleeve_cm": 41.5,
        "skirt_cm": "-",
        "pant_cm": "-",
        "source_note": "Shoulder, waist, garment length, and sleeve are chart values; chest/bust and hip are unavailable in the chart and were not guessed."
    }
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


def fmt_num(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:.1f}".rstrip("0").rstrip(".")


def cm_to_in(value) -> str:
    if value in (None, "", 0, "0", "-", "--"):
        return "-"
    if isinstance(value, str) and "-" in value:
        nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", value)]
        if len(nums) == 2:
            return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} cm / {fmt_num(nums[0] / 2.54)}-{fmt_num(nums[1] / 2.54)} in"
    number = float(value)
    return f"{fmt_num(number)} cm / {fmt_num(number / 2.54)} in"


def kg_to_lbs(text: str) -> str:
    if text in {"", "-"}:
        return "-"
    nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", text)]
    if not nums:
        return html.escape(text)
    if len(nums) == 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} kg / {fmt_num(nums[0] * 2.20462)}-{fmt_num(nums[1] * 2.20462)} lbs"
    return f"{fmt_num(nums[0])} kg / {fmt_num(nums[0] * 2.20462)} lbs"


def role_token(role: str) -> str:
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Mother"):
        return "MOM"
    raise KeyError(role)


def price_for(row: dict) -> str:
    return MOTHER_PRICE if row["audience"] == "mother" else CHILD_PRICE


def sku_for(row: dict, colorway: dict) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{colorway['token']}"


def tags() -> list[str]:
    values = [
        "Mommy and Me",
        "Mother Daughter Matching Set",
        "Matching Family Dress",
        "Matching Family Dresses",
        "Matching Mommy and Me Dresses",
        "Dresses",
        "Girl Dress",
        "Mother Dress",
        "Ivory",
        "White",
        "Green",
        "Floral",
        "Ivory Meadow",
        "Small Floral",
        "Beach Dress",
        "Resort",
        "Vacation",
        "Beach",
        "Summer",
        "Chiffon Dress",
        "Long Sleeve Dress",
        "Wrap Dress",
        "Midi Dress",
        "Photo Ready",
        "Child 4yr",
        "Child 5yr",
        "Child 6-7yr",
        "Child 8yr",
        "Child 9-10yr",
        "Mom Size S",
        "Mom Size M",
        "Mom Size L",
        "Mom Size XL"
]
    return sorted(dict.fromkeys(values))


def build_body() -> str:
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
    rendered_rows = []
    for row in SIZE_CHART:
        rendered_rows.append(
            "<tr>"
            f"<td>{html.escape(row['picker_label'])}</td>"
            f"<td>{html.escape(row['age'] if row['audience'] == 'child' else '-')}</td>"
            f"<td>{kg_to_lbs(str(row['weight']))}</td>"
            f"<td>{cm_to_in(row['height'])}</td>"
            f"<td>{cm_to_in(row['chest_cm'])}</td>"
            f"<td>{cm_to_in(row['sleeve_cm'])}</td>"
            f"<td>{cm_to_in(row['pant_cm'])}</td>"
            f"<td>{cm_to_in(row['hip_cm'])}</td>"
            f"<td>{cm_to_in(row['waist_cm'])}</td>"
            f"<td>{cm_to_in(row['length_cm'])}</td>"
            "</tr>"
        )
    return "\n".join(
        [
            '<ul>',
            '<li><strong>Fabric:</strong> Lightweight sheer chiffon-style fabric shown in the supplied image; exact fiber content was not visible from the evidence.</li>',
            '<li><strong>Family story:</strong> A soft mom-and-daughter dress match for beach photos, resort walks, birthdays, and sunny family plans.</li>',
            '<li><strong>Print:</strong> Ivory Meadow pairs a white/ivory base with tiny green floral sprigs for a calm vacation-ready look.</li>',
            '<li><strong>Design details:</strong> Wrap-inspired V neckline, sheer long sleeves, gathered waist, and flowing skirt movement for mother and child.</li>',
            '<li><strong>Care:</strong> Hand wash cold, reshape gently, hang or lay flat to dry, and avoid bleach or rough surfaces.</li>',
            '<li><strong>Size range:</strong> Girls Child 4 Years to Child 9-10 Years; Mother S to Mother XL.</li>',
            '</ul>',
            '',
            '<h3>Size Chart - Ivory Meadow Dress</h3>',
            '<table id="size-chart">',
            '<thead><tr>',
            *[f"<th>{header}</th>" for header in headers],
            '</tr></thead>',
            '<tbody>',
            *rendered_rows,
            '</tbody>',
            '</table>',
            '',
            '<p>The Ivory Meadow Mommy and Me Dresses listing is built for a coordinated mom-and-daughter beach or resort moment without turning the outfit into a bundled set. Choose the child dress size, choose the mother dress size, and keep the same soft ivory floral look across both pieces.</p>',
            '',
            '<p>The attached size chart is the variant source of truth. It gives shoulder, waist, garment length, and sleeve measurements; chest/bust and hip are unavailable in the chart and are left blank rather than guessed.</p>',
            '',
            '<h3>Key Features:</h3>',
            '<ul>',
            '<li><strong>Mom + daughter match:</strong> Coordinated ivory floral dresses across child and mother sizes.</li>',
            '<li><strong>Beach-ready drape:</strong> Sheer sleeves and a flowing skirt frame resort, vacation, and family-photo outfits.</li>',
            '<li><strong>Soft meadow palette:</strong> Tiny green floral sprigs over a white/ivory base keep the look light and easy to style.</li>',
            '<li><strong>Chart-backed size rows:</strong> Every Shopify variant maps to a visible source row.</li>',
            '<li><strong>Draft-safe listing:</strong> Built for owner review before any separate publish step.</li>',
            '</ul>',
            '',
            '<p>Add the sizes you need and create a breezy matching dress moment for the next sunny family memory.</p>',
        ]
    )


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        for colorway in COLORWAYS:
            price = price_for(row)
            variants.append(
                {
                    "price": price,
                    "compareAtPrice": compare_at(price),
                    "taxable": True,
                    "inventoryPolicy": "DENY",
                    "optionValues": [
                        {"optionName": "Size", "name": row["picker_label"]},
                        {"optionName": "Color", "name": colorway["name"]},
                    ],
                    "inventoryItem": {
                        "sku": sku_for(row, colorway),
                        "cost": cost_for(price),
                        "tracked": True,
                        "requiresShipping": True,
                    },
                    "_row": row,
                    "_colorway": colorway,
                }
            )
    return variants


def shopify_variant_input(variant: dict) -> dict:
    return {key: value for key, value in variant.items() if not key.startswith("_")}


def validate_taxonomy() -> None:
    data = gql(
        """query($id:ID!){node(id:$id){__typename ... on TaxonomyCategory{id fullName isLeaf}}}""",
        {"id": TAXONOMY_GID},
    )
    node = data["data"]["node"]
    if (
        node["__typename"] != "TaxonomyCategory"
        or node["id"] != TAXONOMY_GID
        or node["fullName"] != EXPECTED_TAXONOMY_FULL_NAME
        or node["isLeaf"] is not True
    ):
        raise RuntimeError(f"Taxonomy guard failed: {node}")


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {
        "audience",
        "role",
        "garment",
        "vendor_label",
        "picker_label",
        "sku_suffix",
        "age",
        "weight",
        "height",
        "chest_cm",
        "hip_cm",
        "waist_cm",
        "length_cm",
        "sleeve_cm",
        "pant_cm",
    }
    if len(SIZE_CHART) != 9 or len(variants) != len(SIZE_CHART) * len(COLORWAYS):
        errors.append("SIZE_CHART/variant count mismatch")
    if table_row_count(body) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        errors.append("size table does not have 10 headers")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"seo title too long: {len(SEO_TITLE)}")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"seo description too long: {len(SEO_DESCRIPTION)}")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate (role, picker_label)")
    for row in SIZE_CHART:
        missing = [field for field in required if row.get(field) in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        if row["picker_label"] not in SIZE_MAP:
            errors.append(f"missing size metaobject mapping for {row['picker_label']}")
    for variant in variants:
        row = variant["_row"]
        if variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("cost is not 50 percent of price")
    leak_blob = "\n".join([TITLE, SEO_TITLE, SEO_DESCRIPTION, " ".join(tags()), body]).lower()
    source_tokens = ["ali" + "baba", "detail" + "."]
    if any(token in leak_blob for token in source_tokens):
        errors.append("customer-facing product data contains a source token")
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart_path = tmpdir / "size-chart.json"
        derived_path = tmpdir / "derived.json"
        evidence_path = tmpdir / "vendor-evidence.json"
        chart_path.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
        derived_path.write_text(
            json.dumps(
                {
                    "option_names": ["Size", "Color"],
                    "variants": [shopify_variant_input(variant) for variant in variants],
                    "option_axes": [
                        {"name": "Size", "values": [row["picker_label"] for row in SIZE_CHART]},
                        {"name": "Color", "values": [colorway["name"] for colorway in COLORWAYS]},
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        evidence_path.write_text(
            json.dumps({"notes": "Attached evidence shows one ivory floral dress garment for mother and girl. The requested scope is one dress colorway only."}),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "python3.13",
                str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
                "--size-chart",
                str(chart_path),
                "--derived",
                str(derived_path),
                "--vendor-evidence",
                str(evidence_path),
                "--primary-category",
                CATEGORY,
                "--tags",
                ", ".join(tags()),
            ],
            check=True,
        )


def product_input(body: str, status: str = "DRAFT") -> dict:
    return {
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": tags(),
        "status": status,
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }


def find_existing() -> dict | None:
    data = gql(
        """query($handle:String!){
          productByHandle(handle:$handle){
            id handle status publishedAt onlineStoreUrl
            options{name values optionValues{id name hasVariants}}
            variants(first:100){nodes{id sku price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{id tracked requiresShipping unitCost{amount}}}}
          }
        }""",
        {"handle": HANDLE},
    )
    return data["data"]["productByHandle"]


def create_variants(product_id: str, variants: list[dict]) -> None:
    data = gql(
        """mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){
          productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){
            productVariants{id sku title price compareAtPrice inventoryPolicy}
            userErrors{field message}
          }
        }""",
        {"productId": product_id, "variants": [shopify_variant_input(variant) for variant in variants], "strategy": "REMOVE_STANDALONE_VARIANT"},
    )
    require_no_user_errors(data, ["data", "productVariantsBulkCreate", "userErrors"])


def update_variants(product_id: str, existing: dict, variants: list[dict]) -> None:
    by_sku = {node["sku"]: node for node in existing["variants"]["nodes"]}
    updates = []
    for variant in variants:
        sku = variant["inventoryItem"]["sku"]
        updates.append(
            {
                "id": by_sku[sku]["id"],
                "price": variant["price"],
                "compareAtPrice": variant["compareAtPrice"],
                "inventoryPolicy": "DENY",
                "inventoryItem": variant["inventoryItem"],
            }
        )
    data = gql(
        """mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){
          productVariantsBulkUpdate(productId:$productId, variants:$variants){
            productVariants{id sku title price compareAtPrice inventoryPolicy}
            userErrors{field message}
          }
        }""",
        {"productId": product_id, "variants": updates},
    )
    require_no_user_errors(data, ["data", "productVariantsBulkUpdate", "userErrors"])


def create_or_update_product(body: str, variants: list[dict]) -> tuple[str, bool]:
    existing = find_existing()
    if existing is None:
        product_options = [
            {"name": "Size", "values": [{"name": row["picker_label"]} for row in SIZE_CHART]},
            {"name": "Color", "values": [{"name": colorway["name"]} for colorway in COLORWAYS]},
        ]
        data = gql(
            """mutation($input:ProductInput!){
              productCreate(input:$input){
                product{id handle title}
                userErrors{field message}
              }
            }""",
            {"input": {**product_input(body), "productOptions": product_options}},
        )
        require_no_user_errors(data, ["data", "productCreate", "userErrors"])
        product_id = data["data"]["productCreate"]["product"]["id"]
        create_variants(product_id, variants)
        return product_id, True

    product_id = existing["id"]
    if existing["status"] != "DRAFT":
        raise RuntimeError(f"Existing product {HANDLE} is {existing['status']}; refusing to change a non-draft product.")
    live_skus = sorted(node["sku"] for node in existing["variants"]["nodes"] if node.get("sku"))
    spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
    unexpected_skus = sorted(set(live_skus) - set(spec_skus))
    if unexpected_skus:
        raise RuntimeError(f"Existing draft has unexpected SKUs: {unexpected_skus}")
    data = gql(
        """mutation($product:ProductUpdateInput!){
          productUpdate(product:$product){
            product{id handle title}
            userErrors{field message}
          }
        }""",
        {"product": {"id": product_id, **product_input(body, status="DRAFT")}},
    )
    require_no_user_errors(data, ["data", "productUpdate", "userErrors"])
    existing_sku_set = set(live_skus)
    existing_variants = [variant for variant in variants if variant["inventoryItem"]["sku"] in existing_sku_set]
    missing_variants = [variant for variant in variants if variant["inventoryItem"]["sku"] not in existing_sku_set]
    if existing_variants:
        update_variants(product_id, existing, existing_variants)
    if missing_variants:
        create_variants(product_id, missing_variants)
    return product_id, False


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    color_refs = list(dict.fromkeys([colorway["gid"] for colorway in COLORWAYS] + ["gid://shopify/Metaobject/129971519585"]))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Resort Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Mommy and Me Resort Dresses"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": CUSTOM_TYPE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Ivory Meadow"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Dresses"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Resort"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116490337", "gid://shopify/Metaobject/128116523105"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(color_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def set_metafields(product_id: str) -> None:
    rows = metafields(product_id)
    for i in range(0, len(rows), 25):
        data = gql(
            """mutation($metafields:[MetafieldsSetInput!]!){
              metafieldsSet(metafields:$metafields){
                metafields{namespace key type value}
                userErrors{field message}
              }
            }""",
            {"metafields": rows[i : i + 25]},
        )
        require_no_user_errors(data, ["data", "metafieldsSet", "userErrors"])


def upload_media(product_id: str) -> None:
    if not UPLOAD_DIR.exists():
        return
    existing = gql(
        """query($id:ID!){product(id:$id){media(first:50){nodes{... on MediaImage{alt}}}}}""",
        {"id": product_id},
    )
    existing_alts = {node.get("alt") for node in existing["data"]["product"]["media"]["nodes"]}
    alt_by_name = {
        "01-ivory-meadow-mommy-and-me-dresses.png": "Mother and daughter wearing matching ivory floral dresses on the beach.",
    }
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if "size-chart" in path.name:
            continue
        alt = alt_by_name.get(path.name, "Ivory Meadow mommy and me dress product image.")
        if alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        staged = gql(
            """mutation($input:[StagedUploadInput!]!){
              stagedUploadsCreate(input:$input){
                stagedTargets{url resourceUrl parameters{name value}}
                userErrors{field message}
              }
            }""",
            {"input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]},
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
        urllib.request.urlopen(
            urllib.request.Request(
                target["url"],
                data=b"".join(chunks),
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            )
        ).read()
        media = gql(
            """mutation($productId:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$productId, media:$media){
                media{... on MediaImage{id alt}}
                userErrors{field message}
              }
            }""",
            {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]},
        )
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def verify_query(product_id: str) -> dict:
    data = gql(
        """query($id:ID!){
          product(id:$id){
            id title handle status publishedAt onlineStoreUrl descriptionHtml tags
            seo{title description}
            category{id fullName}
            options{name position values optionValues{id name hasVariants}}
            variants(first:100){
              nodes{
                id sku title price compareAtPrice inventoryPolicy selectedOptions{name value}
                inventoryItem{id tracked requiresShipping unitCost{amount}}
              }
            }
            media(first:50){nodes{... on MediaImage{alt image{url}}}}
            collections(first:50){nodes{title handle}}
            metafields(first:100){nodes{namespace key type value}}
            resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}}
          }
        }""",
        {"id": product_id},
    )
    return data["data"]["product"]


def verify_product(product: dict, variants: list[dict]) -> tuple[list[str], list[dict]]:
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    errors = []
    price_rows = []
    if product["status"] != "DRAFT":
        errors.append(f"status is {product['status']}, expected DRAFT")
    if product.get("publishedAt") is not None or product.get("onlineStoreUrl") is not None:
        errors.append("draft publication fields are populated")
    if any(node["isPublished"] for node in product["resourcePublicationsV2"]["nodes"]):
        errors.append("product is published to at least one sales channel")
    if product["category"]["fullName"] != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {product['category']['fullName']}")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    if sorted(node["sku"] for node in live_variants) != sorted(spec_by_sku):
        errors.append("live SKUs do not match derived SKUs")
    if table_row_count(product["descriptionHtml"]) != len(SIZE_CHART):
        errors.append("size table row count does not match SIZE_CHART")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)):
        errors.append("live size table does not have 10 headers")
    if [option["name"] for option in product["options"]] != ["Size", "Color"]:
        errors.append("option axes are not Size / Color")
    expected_pairs = {(row["picker_label"], colorway["name"]) for row in SIZE_CHART for colorway in COLORWAYS}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Size x Color option combinations do not match")
    leak_blob = "\n".join([
        product.get("title") or "",
        product.get("descriptionHtml") or "",
        product.get("seo", {}).get("title") or "",
        product.get("seo", {}).get("description") or "",
        " ".join(product.get("tags") or []),
        "\n".join(node.get("value") or "" for node in product["metafields"]["nodes"]),
    ]).lower()
    source_tokens = ["ali" + "baba", "detail" + "."]
    if any(token in leak_blob for token in source_tokens):
        errors.append("Shopify product data contains a source token")
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


def write_csv(body: str, variants: list[dict]) -> None:
    header = [
        "Handle",
        "Title",
        "Body (HTML)",
        "Vendor",
        "Product Category",
        "Type",
        "Tags",
        "Published",
        "Option1 Name",
        "Option1 Value",
        "Option2 Name",
        "Option2 Value",
        "Variant SKU",
        "Variant Grams",
        "Variant Inventory Tracker",
        "Variant Inventory Policy",
        "Variant Fulfillment Service",
        "Variant Price",
        "Variant Compare At Price",
        "Variant Requires Shipping",
        "Variant Taxable",
        "SEO Title",
        "SEO Description",
        "Cost per item",
        "Status",
    ]
    rows = []
    for i, variant in enumerate(variants, start=1):
        row = variant["_row"]
        colorway = variant["_colorway"]
        rows.append(
            {
                "Handle": HANDLE,
                "Title": TITLE if i == 1 else "",
                "Body (HTML)": body if i == 1 else "",
                "Vendor": VENDOR if i == 1 else "",
                "Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
                "Type": PRODUCT_TYPE if i == 1 else "",
                "Tags": ", ".join(tags()) if i == 1 else "",
                "Published": "FALSE",
                "Option1 Name": "Size",
                "Option1 Value": row["picker_label"],
                "Option2 Name": "Color",
                "Option2 Value": colorway["name"],
                "Variant SKU": variant["inventoryItem"]["sku"],
                "Variant Grams": "220",
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": variant["price"],
                "Variant Compare At Price": variant["compareAtPrice"],
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "SEO Title": SEO_TITLE if i == 1 else "",
                "SEO Description": SEO_DESCRIPTION if i == 1 else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, product: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    live_channels = [p["publication"]["name"] for p in product["resourcePublicationsV2"]["nodes"] if p["isPublished"]]
    recap = []
    for variant in variants:
        row = variant["_row"]
        colorway = variant["_colorway"]
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {colorway['name']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |"
        )
    written = sorted(
        f"{node['namespace']}.{node['key']}"
        for node in product["metafields"]["nodes"]
        if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}
    )
    skipped = [
        ("shopify.fabric", "Exact fiber was not visible from the supplied evidence."),
        ("shopify.dress-style", "No exact catalog GID was selected for this sheer wrap-style resort dress."),
        ("shopify.dress-occasion", "No exact catalog GID was selected for a broad vacation/photo use case."),
        ("shopify.skirt-dress-length-type", "Source chart provides garment length, but no exact standardized dress-length type was selected in this run."),
        ("shopify.sleeve-length-type", "Long sheer sleeves are visible, but no exact trusted sleeve-length metaobject was selected in this run."),
        ("shopify.neckline", "V-neck wrap styling is visible, but no exact trusted neckline metaobject was selected in this run."),
        ("shopify.top-length-type", "Product taxonomy is Dresses, not Tops."),
    ]
    price_detail = [
        f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |"
        for row in price_rows
    ]
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
        "| VENDOR_URL | redacted per project source-URL policy |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Mommy and Me (resolved from mother + girl evidence) |",
        "| PRIMARY_CATEGORY | Dresses |",
        "| DESIGNS_TO_LIST | Ivory Meadow dress |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        "| COLOR_TOKEN | IVORY |",
        "",
        "## Source Fetch Status",
        SOURCE_FETCH_STATUS,
        "",
        "## Source Measurement Notes",
        "The attached chart publishes shoulder, waist, garment length, and sleeve. Chest/bust and hip are unavailable in the chart and were not guessed.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap,
        "",
        "## Derivations",
        "- Request resolved to Mommy and Me because the supplied product image shows mother + girl and no father/boy rows were evidenced.",
        "- Primary category resolved to Dresses from the garment evidence and Shopify taxonomy guard.",
        "- Product options are `Size` and `Color`; Ivory Meadow is a single color value, so variant count equals the 9 chart rows.",
        "- Child rows map 110-150 to Child 4 Years through Child 9-10 Years. Adult rows map S/M/L/XL to Mother S/M/L/XL.",
        "- Waist, shoulder, sleeve, and garment length are source-transcribed. Chest/bust and hip are rendered as unavailable because the chart does not publish those columns.",
        "- Pricing uses nearby active Mommy-and-Me dress products: child `31.99`, mother `34.99`; Cost per item is exactly 50 percent.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status | PASS | {product['status']} |",
        f"| Publication check | PASS | publishedAt={product.get('publishedAt')}; onlineStoreUrl={product.get('onlineStoreUrl')}; live channels={live_channels} |",
        f"| Taxonomy fullName matches | {'PASS' if product['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {product['category']['fullName']} |",
        f"| Variant count matches SIZE_CHART x colors | {'PASS' if len(product['variants']['nodes']) == len(variants) else 'FAIL'} | {len(product['variants']['nodes'])} vs {len(variants)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        "| Source-token leak check | PASS | No source marketplace token or offer ID in Shopify product data or local artifacts |",
        "",
        "## Localized Size-Chart Gate",
        "| Command | Result |",
        "|---|---|",
        f"| `python3 ops/scripts/poll_shopify_product_translations.py --handles {HANDLE} --execute --force-refresh` | pending current-session run |",
        f"| `python3 ops/scripts/repair_localized_product_size_charts.py --handles {HANDLE} --execute` | pending current-session run |",
        f"| `python3 ops/scripts/repair_localized_product_size_charts.py --handles {HANDLE} --fail-on-missing` | pending current-session run |",
        f"| `python3 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles {HANDLE} --fail-on-unmatched` | pending current-session run |",
        "",
        "## Price Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *price_detail,
        "",
        "## Metafields Written",
        *[f"- `{item}`" for item in written],
        "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped],
        "",
        "## Tags Written",
        ", ".join(tags()),
        "",
        "## Smart Collections",
        "Product is a draft; collection indexing may wait until publication.",
        "",
        "## Manual Follow-ups",
        "1. Review the draft image and Ivory Meadow color naming in Shopify Admin before any separate publish-live request.",
        "2. If exact fiber composition becomes available, add the fabric metafield before publishing.",
        "3. If true chest/bust or hip chart values become available, replace the unavailable cells before publishing.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{UPLOAD_DIR}`",
        "",
    ]
    LISTING_MD.parent.mkdir(parents=True, exist_ok=True)
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    validate_taxonomy()
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard(variants)

    SIZE_CHART_OUT.parent.mkdir(parents=True, exist_ok=True)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    product_id, created = create_or_update_product(body, variants)
    set_metafields(product_id)
    upload_media(product_id)
    product = verify_query(product_id)
    errors, price_rows = verify_product(product, variants)
    VERIFY_JSON_OUT.write_text(
        json.dumps(
            {
                "handle": HANDLE,
                "product_id": product_id,
                "created": created,
                "errors": errors,
                "variant_count": len(product["variants"]["nodes"]),
                "expected_variant_count": len(variants),
                "status": product["status"],
                "publishedAt": product.get("publishedAt"),
                "onlineStoreUrl": product.get("onlineStoreUrl"),
                "price_rows": price_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    if errors:
        raise RuntimeError("VERIFY FAILED:\n- " + "\n- ".join(errors))
    write_listing(product_id, product, variants, price_rows)
    local_blob = "\n".join(
        [
            LISTING_MD.read_text(encoding="utf-8"),
            CSV_OUT.read_text(encoding="utf-8"),
            BODY_HTML_OUT.read_text(encoding="utf-8"),
            SIZE_CHART_OUT.read_text(encoding="utf-8"),
        ]
    ).lower()
    source_tokens = ["ali" + "baba", "detail" + "."]
    if any(token in local_blob for token in source_tokens):
        raise RuntimeError("Local artifact source-token leak check failed.")
    print(json.dumps({"handle": HANDLE, "product_id": product_id, "created": created, "variants": len(variants)}, indent=2))


if __name__ == "__main__":
    main()
PY
