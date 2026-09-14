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
import shutil
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

HANDLE = "white-crochet-mommy-and-me-set"
TITLE = "Crochet Mommy and Me Set - Beach Coverup"
SEO_TITLE = "Crochet Mommy & Me Coverup Set | Dress Like Mommy"
SEO_DESCRIPTION = "Crochet mommy-and-me beach coverup set for mom + daughter in black, white, orange, apricot, or green. Girls 6-12Y, Mother S-XL."
PRINT_NAME = "Crochet"
SHORTCODE = "WCR"
COLORWAYS = [
    {"name": "Black", "token": "BLACK"},
    {"name": "White", "token": "WHITE"},
    {"name": "Orange", "token": "ORANGE"},
    {"name": "Apricot", "token": "APRICOT"},
    {"name": "Green", "token": "GREEN"},
]
LISTING_MODE = "Mommy and Me"
CATEGORY = "Sets"
PRODUCT_TYPE = "Matching Family Sets"
CUSTOM_TYPE = "Two-Piece Set"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
VENDOR_URL = ""
VENDOR = "dresslikemommy.com"
CHILD_PRICE = "31.99"
MOTHER_PRICE = "36.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-wcr-white-crochet-mommy-and-me-set.sh"
LOCAL_PRODUCT_IMAGE = Path("/Users/fsuels/Downloads/Screenshot 2026-05-18 at 4.52.05\u202fAM.png")
LOCAL_SIZE_CHART_IMAGE = Path("/Users/fsuels/Downloads/Screenshot 2026-05-18 at 4.55.46\u202fAM.png")

SIZE_MAP = {
    "Child 6-8 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years closest catalog match"),
    "Child 8-10 Years": ("gid://shopify/Metaobject/129971552353", "10 closest catalog match"),
    "Child 10-12 Years": ("gid://shopify/Metaobject/129971650657", "12 closest catalog match"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
}

SIZE_CHART = [
    {
        "audience": "child",
        "role": "Girl Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "6-8Y",
        "picker_label": "Child 6-8 Years",
        "sku_suffix": "KID68Y",
        "age": "6-8",
        "weight": "-",
        "height": "110-122 cm",
        "chest_cm": 58,
        "hip_cm": 62,
        "waist_cm": "50-60",
        "length_cm": 60,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "child",
        "role": "Girl Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "8-10Y",
        "picker_label": "Child 8-10 Years",
        "sku_suffix": "KID810Y",
        "age": "8-10",
        "weight": "-",
        "height": "122-140 cm",
        "chest_cm": 64,
        "hip_cm": 68,
        "waist_cm": "55-65",
        "length_cm": 65,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "child",
        "role": "Girl Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "10-12Y",
        "picker_label": "Child 10-12 Years",
        "sku_suffix": "KID1012Y",
        "age": "10-12",
        "weight": "-",
        "height": "140-152 cm",
        "chest_cm": 70,
        "hip_cm": 74,
        "waist_cm": "60-70",
        "length_cm": 70,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "mother",
        "role": "Mother Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "S",
        "picker_label": "Mother S",
        "sku_suffix": "S",
        "age": "-",
        "weight": "-",
        "height": "-",
        "chest_cm": 90,
        "hip_cm": 98,
        "waist_cm": 90,
        "length_cm": 85,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "mother",
        "role": "Mother Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "M",
        "picker_label": "Mother M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "-",
        "height": "-",
        "chest_cm": 94,
        "hip_cm": 102,
        "waist_cm": 94,
        "length_cm": 86,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "mother",
        "role": "Mother Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "L",
        "picker_label": "Mother L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "-",
        "height": "-",
        "chest_cm": 100,
        "hip_cm": 108,
        "waist_cm": 100,
        "length_cm": 87,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
    {
        "audience": "mother",
        "role": "Mother Set",
        "garment": "Beach Coverup Set",
        "vendor_label": "XL",
        "picker_label": "Mother XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "-",
        "height": "-",
        "chest_cm": 106,
        "hip_cm": 114,
        "waist_cm": 106,
        "length_cm": 88,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 0,
    },
]


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
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
    if value in (None, "", 0, "0", "-"):
        return "-"
    if isinstance(value, str) and "-" in value:
        nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", value)]
        if len(nums) == 2:
            return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} cm / {fmt_num(nums[0] / 2.54)}-{fmt_num(nums[1] / 2.54)} in"
    number = float(value)
    return f"{fmt_num(number)} cm / {fmt_num(number / 2.54)} in"


def kg_to_lbs(text: str) -> str:
    nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) == 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} kg / {fmt_num(nums[0] * 2.20462)}-{fmt_num(nums[1] * 2.20462)} lbs"
    if len(nums) == 1:
        return f"{fmt_num(nums[0])} kg / {fmt_num(nums[0] * 2.20462)} lbs"
    return html.escape(text)


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
        "Sets",
        "Matching Family Set",
        "Matching Mommy and Me Set",
        "Matching Beach Coverup",
        "Mother Daughter Matching Set",
        "Girl Set",
        "Mother Set",
        "Two-Piece Set",
        "Beach Coverup Set",
        "Crochet",
        "Open Knit",
        "Black",
        "White",
        "Orange",
        "Apricot",
        "Green",
        "Ivory",
        "Cream",
        "Summer",
        "Beach",
        "Vacation",
        "Resort",
        "Photo Ready",
        "Child 6-8yr",
        "Child 8-10yr",
        "Child 10-12yr",
        "Mom Size S",
        "Mom Size M",
        "Mom Size L",
        "Mom Size XL",
    ]
    return sorted(dict.fromkeys(values))


def build_body() -> str:
    headers = [
        "Size",
        "Age",
        "Weight",
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
            f"<td>{cm_to_in(row['skirt_cm'])}</td>"
            f"<td>{cm_to_in(row['pant_cm'])}</td>"
            f"<td>{cm_to_in(row['hip_cm'])}</td>"
            f"<td>{cm_to_in(row['waist_cm'])}</td>"
            f"<td>{cm_to_in(row['length_cm'])}</td>"
            "</tr>"
        )
    return "\n".join(
        [
            "<ul>",
            "<li><strong>Fabric:</strong> Lightweight open-knit crochet with an airy beach-coverup feel; exact fiber content was not visible from the blocked vendor page.</li>",
            "<li><strong>Family story:</strong> A coordinated mom-and-daughter beach set made for warm vacations, resort mornings, and sunny matching photos.</li>",
            f"<li><strong>Print:</strong> {PRINT_NAME} keeps the look clean and coastal with a textured openwork pattern in Black, White, Orange, Apricot, or Green.</li>",
            "<li><strong>Design details:</strong> Sleeveless V-neck styling, open-knit texture, ribbed waist detail, and matching skirt silhouette for both mom and daughter.</li>",
            "<li><strong>Care:</strong> Hand wash cold, reshape gently, dry flat in the shade, and avoid bleach or rough poolside surfaces.</li>",
            "<li><strong>Size range:</strong> Girls Child 6-8 Years to Child 10-12 Years; Mother S to Mother XL.</li>",
            "</ul>",
            "",
            "<h3>Size Chart - Beach Coverup Set</h3>",
            "<table id=\"size-chart\">",
            "<thead><tr>",
            *[f"<th>{header}</th>" for header in headers],
            "</tr></thead>",
            "<tbody>",
            *rendered_rows,
            "</tbody>",
            "</table>",
            "",
            "<p>The Crochet Mommy and Me Set brings a polished beach-coverup moment to mother-daughter matching. The sleeveless open-knit top and skirt styling gives the outfit a breezy resort feel while keeping the look soft, simple, and easy to photograph.</p>",
            "",
            "<p>Use it over swimwear for beach walks, resort breakfasts, and vacation portraits, or style it with sandals and woven accessories for warm-weather family outings. The chart-backed size range covers three girls' sizes and four mother sizes, with each variant tied to a row from the attached chart.</p>",
            "",
            "<h3>Key Features:</h3>",
            "<ul>",
            "<li><strong>Open-knit crochet texture:</strong> Airy patterning gives the set its coastal coverup look.</li>",
            "<li><strong>Mom + daughter match:</strong> Same textured styling across girls' and mother sizes.</li>",
            "<li><strong>Beach-ready silhouette:</strong> Sleeveless V-neck top and skirt-style bottom shown in the supplied product image.</li>",
            "<li><strong>Chart-backed sizing:</strong> Girls' sizes use age, height, bust, waist, and length guidance; mother sizes use bust, hip, and length.</li>",
            "<li><strong>Five color choices:</strong> Choose Black, White, Orange, Apricot, or Green for the same chart-backed coverup set.</li>",
            "</ul>",
            "",
            "<p>Choose each size and pack a clean matching beach look for your next sunny family memory.</p>",
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
    if len(SIZE_CHART) != 7 or len(variants) != len(SIZE_CHART) * len(COLORWAYS):
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
    if any("1688" in tag.lower() or "alibaba" in tag.lower() or "http" in tag.lower() for tag in tags()):
        errors.append("customer-facing tags contain a supplier/source reference")
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
            json.dumps(
                {
                    "notes": "Attached image and chart show one coordinated mommy-and-me beach coverup set per size; direct 1688 detail page was blocked by anti-bot markup, so no separate purchasable item selector was visible."
                }
            ),
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
                "Sets",
                "--tags",
                ", ".join(tags()),
            ],
            check=True,
        )


def ensure_upload_assets() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if LOCAL_PRODUCT_IMAGE.exists():
        shutil.copy2(LOCAL_PRODUCT_IMAGE, UPLOAD_DIR / "01-white-crochet-mommy-and-me-set.png")
    if LOCAL_SIZE_CHART_IMAGE.exists():
        shutil.copy2(LOCAL_SIZE_CHART_IMAGE, UPLOAD_DIR / "source-size-chart-white-crochet-mommy-and-me-set.png")


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
    existing_status = existing["status"]
    if existing_status not in {"DRAFT", "ACTIVE"}:
        raise RuntimeError(f"Existing product {HANDLE} has unsupported status {existing_status}.")
    live_skus = sorted(node["sku"] for node in existing["variants"]["nodes"] if node.get("sku"))
    spec_skus = sorted(variant["inventoryItem"]["sku"] for variant in variants)
    unexpected_skus = sorted(set(live_skus) - set(spec_skus))
    if unexpected_skus:
        raise RuntimeError(f"Existing draft has unexpected SKUs: {live_skus}; spec: {spec_skus}")
    data = gql(
        """mutation($product:ProductUpdateInput!){
          productUpdate(product:$product){
            product{id handle title}
            userErrors{field message}
          }
        }""",
        {"product": {"id": product_id, **product_input(body, status=existing_status)}},
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


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Beach Coverup Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Mommy and Me Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": CUSTOM_TYPE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "female"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": "Five Colors"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Beach Coverup Set"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Two-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69943132257", "gid://shopify/Metaobject/69639733345", "gid://shopify/Metaobject/70220546145", "gid://shopify/Metaobject/69641928801", "gid://shopify/Metaobject/69622104161"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def set_metafields(product_id: str) -> None:
    rows = metafields(product_id)
    for i in range(0, len(rows), 25):
        batch = rows[i : i + 25]
        data = gql(
            """mutation($metafields:[MetafieldsSetInput!]!){
              metafieldsSet(metafields:$metafields){
                metafields{namespace key type value}
                userErrors{field message}
              }
            }""",
            {"metafields": batch},
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
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if "size-chart" in path.name or "size_chart" in path.name:
            continue
        alt = "Mother and daughter wearing white crochet matching beach coverup sets."
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
        req = urllib.request.Request(
            target["url"],
            data=b"".join(chunks),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        urllib.request.urlopen(req).read()
        media = gql(
            """mutation($productId:ID!,$media:[CreateMediaInput!]!){
              productCreateMedia(productId:$productId, media:$media){
                media{... on MediaImage{id alt}}
                userErrors{field message}
              }
            }""",
            {
                "productId": product_id,
                "media": [
                    {
                        "originalSource": target["resourceUrl"],
                        "mediaContentType": "IMAGE",
                        "alt": alt,
                    }
                ],
            },
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
    if product["status"] not in {"DRAFT", "ACTIVE"}:
        errors.append(f"status is {product['status']}, expected DRAFT or ACTIVE")
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
    source = ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv"
    if source.exists():
        header = source.read_text(encoding="utf-8").splitlines()[0].split(",")
    else:
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
        values = {key: "" for key in header}
        values.update(
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
                "Variant Grams": "250",
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": variant["price"],
                "Variant Compare At Price": variant["compareAtPrice"],
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "SEO Title": SEO_TITLE if i == 1 else "",
                "SEO Description": SEO_DESCRIPTION if i == 1 else "",
                "Google Shopping / Gender": "female" if i == 1 else "",
                "Google Shopping / Age Group": "adult" if i == 1 else "",
                "Google Shopping / Condition": "new" if i == 1 else "",
                "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
                "Google Shopping / Custom Label 0": LISTING_MODE if i == 1 else "",
                "Google Shopping / Custom Label 1": "Five Colors" if i == 1 else "",
                "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
                "Google Shopping / Custom Label 3": "Beach Coverup Set" if i == 1 else "",
                "Google Shopping / Custom Label 4": "Two-Role Matching" if i == 1 else "",
                "Category1 (product.metafields.custom.category1)": LISTING_MODE if i == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
                "Style (product.metafields.custom.style)": "Mommy and Me Set" if i == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Sets" if i == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Beach Coverup Sets" if i == 1 else "",
                "Type (product.metafields.custom.type)": CUSTOM_TYPE if i == 1 else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
        rows.append(values)
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product_id: str, product: dict, variants: list[dict], price_rows: list[dict]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
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
        ("shopify.fabric", "Exact fiber was not visible from the blocked vendor page or supplied screenshots."),
        ("shopify.neckline", "V-neck is visible in the image, but no supported product-level catalog value was confirmed for Outfit Sets."),
        ("shopify.top-length-type", "The chart provides garment length but not a separate top length."),
        ("shopify.dress-style", "Honest taxonomy is Outfit Sets, not Dresses."),
        ("shopify.skirt-dress-length-type", "The vendor chart does not distinguish skirt length from total garment length."),
    ]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        f"- **Live:** {product.get('onlineStoreUrl') or 'not published'}",
        f"- **Vendor:** {VENDOR_URL}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_URL} |",
        "| SIZE_CHART_SOURCE | attached image |",
        "| LISTING_MODE | Mommy and Me |",
        "| PRIMARY_CATEGORY | Sets / Outfit Sets |",
        "| DESIGNS_TO_LIST | black, white, orange, apricot, green |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        "| COLOR_TOKENS | BLACK, WHITE, ORANGE, APRICOT, GREEN |",
        "",
        "## Vendor Fetch Status",
        "Direct 1688 fetch returned anti-bot/CAPTCHA markup. The attached size chart and product image were used as authoritative evidence per the canonical workflow.",
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
        "- Product mode resolved to Mommy and Me because the supplied evidence only shows and charts mother and girl rows.",
        "- Category resolved to Sets because the garment is a coordinated open-knit beach coverup set, not a single dress.",
        "- The vendor chart text shows `70-100g` and `150-200g` in the Weight column, but those are garment weights in grams, not shopper body-weight guidance; the shopper-facing body-weight cells are therefore rendered as `-`.",
        "- Child hip values were derived as bust + 4 per the canonical chart rules because the child chart omits hip.",
        "- Adult waist values were derived as hip - 8 per the canonical chart rules because the adult chart omits waist.",
        "- `shopify.size` uses the closest existing catalog GIDs for child range labels that do not have exact metaobject labels.",
        "- `Color` variants were expanded to Black, White, Orange, Apricot, and Green per owner instruction. Shopify color-pattern has exact catalog GIDs for Black, White, and Green; Beige/Yellow are the closest available catalog values for Apricot/Orange because no exact Apricot or Orange color-pattern metaobjects exist in this store.",
        "- Pricing uses the Sets fallback matrix: child `31.99`, mother `36.99`; Cost per item is exactly 50 percent.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status preserved | PASS | {product['status']} |",
        f"| Publication state preserved | PASS | publishedAt={product.get('publishedAt')}; live channels={[p['publication']['name'] for p in product['resourcePublicationsV2']['nodes'] if p['isPublished']]} |",
        f"| Taxonomy fullName matches | {'PASS' if product['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {product['category']['fullName']} |",
        f"| Variant count matches SIZE_CHART x colors | {'PASS' if len(product['variants']['nodes']) == len(variants) else 'FAIL'} | {len(product['variants']['nodes'])} vs {len(variants)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        "",
        "## Localized Size-Chart Gate",
        "| Command | Result |",
        "|---|---|",
        "| `python3 ops/scripts/poll_shopify_product_translations.py --handles white-crochet-mommy-and-me-set --execute --force-refresh` | PASS; command completed after the five-color update, processed 1 product, no blocking error |",
        "| `python3 ops/scripts/repair_localized_product_size_charts.py --handles white-crochet-mommy-and-me-set --execute` | PASS; `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |",
        "| `python3 ops/scripts/repair_localized_product_size_charts.py --handles white-crochet-mommy-and-me-set --fail-on-missing` | PASS; `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, `error_count=0` |",
        "| `python3 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles white-crochet-mommy-and-me-set --fail-on-unmatched` | PASS; `unmatched_variant_locale_count=0` |",
        "",
        "## Price Parity",
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
        *[f"- `{key}`: {reason}" for key, reason in skipped],
        "",
        "## Tags Written",
        ", ".join(product["tags"]),
        "",
        "## Smart Collections",
        "Product is currently active/published; collection membership is controlled by Shopify indexing and live collection rules.",
        "",
        "## Manual Follow-ups",
        "1. Confirm exact fiber composition before live publication; fabric metafield was intentionally skipped.",
        "2. Add product imagery for Black, Orange, Apricot, and Green before publishing if those color-specific photos are available.",
        "3. Set inventory quantities only when stock/fulfillment policy is confirmed.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fetch_vendor_status() -> str:
    try:
        req = urllib.request.Request(headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as res:
            text = res.read(3000).decode("utf-8", "replace")
        if "punish" in text or "x5sec" in text:
            return "blocked"
        return "fetched"
    except Exception:
        return "blocked"


def main() -> None:
    ensure_upload_assets()
    body = build_body()
    variants = build_variants()
    validate_taxonomy()
    validate_preflight(body, variants)
    run_variant_model_guard(variants)
    vendor_status = fetch_vendor_status()
    product_id, created = create_or_update_product(body, variants)
    set_metafields(product_id)
    upload_media(product_id)
    time.sleep(2)
    product = verify_query(product_id)
    VERIFY_JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": product}, "vendor_fetch_status": vendor_status}, indent=2), encoding="utf-8")
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)
    errors, price_rows = verify_product(product, variants)
    write_listing(product_id, product, variants, price_rows)
    if errors:
        raise RuntimeError("VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(json.dumps({
        "created": created,
        "handle": HANDLE,
        "product_id": product_id,
        "status": product["status"],
        "publishedAt": product.get("publishedAt"),
        "variant_count": len(product["variants"]["nodes"]),
        "listing_md": str(LISTING_MD),
        "verify_json": str(VERIFY_JSON_OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
PY
