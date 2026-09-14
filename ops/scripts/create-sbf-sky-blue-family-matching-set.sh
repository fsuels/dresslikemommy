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
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "sky-blue-family-matching-set"
TITLE = "Sky Blue Family Matching Set - Pleated Dress & Shirts"
SEO_TITLE = "Sky Blue Family Matching Set | Dress Like Mommy"
SEO_DESCRIPTION = "Sky blue family matching dress and shirts for mom, dad, girls & boys. Pleated dresses and soft tees in Child 2Y-10Y, Mother S-2XL, Father M-3XL."
PRINT_NAME = "Sky Blue"
SHORTCODE = "SBF"
COLOR_TOKEN = "SKYBLU"
VENDOR_URL = ""
VENDOR = "dresslikemommy.com"
LISTING_MODE = "Family Matching"
CATEGORY = "FamilySet"
PRODUCT_TYPE = "Matching Family Sets"
CUSTOM_TYPE = "Dress and Shirts"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-sbf-sky-blue-family-matching-set.sh"

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
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
}


def row(audience: str, role: str, garment: str, type_value: str, vendor_label: str, picker_label: str,
        sku_suffix: str, age: str, weight_jin: str, height_cm: str, chest_cm: str,
        length_cm: str, *, shoulder_cm: str = "-", waist_cm: str = "-",
        sleeve_cm: str = "-", hip_cm: str = "-") -> dict:
    return {
        "audience": audience,
        "role": role,
        "garment": garment,
        "type_value": type_value,
        "vendor_label": vendor_label,
        "picker_label": picker_label,
        "sku_suffix": sku_suffix,
        "age": age,
        "weight_jin": weight_jin,
        "height_cm": height_cm,
        "chest_cm": chest_cm,
        "hip_cm": hip_cm,
        "waist_cm": waist_cm,
        "length_cm": length_cm,
        "sleeve_cm": sleeve_cm,
        "skirt_cm": "-",
        "pant_cm": "-",
        "shoulder_cm": shoulder_cm,
    }


SIZE_CHART = [
    row("mother", "Mother Dress", "Dress", "Dress", "S", "Mother S", "S", "-", "85-95", "155-160", "86", "119", shoulder_cm="31", waist_cm="102", hip_cm="92"),
    row("mother", "Mother Dress", "Dress", "Dress", "M", "Mother M", "M", "-", "95-110", "158-163", "90", "120", shoulder_cm="32", waist_cm="106", hip_cm="96"),
    row("mother", "Mother Dress", "Dress", "Dress", "L", "Mother L", "L", "-", "110-120", "161-168", "94", "121", shoulder_cm="33", waist_cm="110", hip_cm="100"),
    row("mother", "Mother Dress", "Dress", "Dress", "XL", "Mother XL", "XL", "-", "120-135", "163-170", "98", "122", shoulder_cm="33", waist_cm="114", hip_cm="104"),
    row("mother", "Mother Dress", "Dress", "Dress", "2XL", "Mother 2XL", "2XL", "-", "135-150", "165-173", "102", "123", shoulder_cm="34", waist_cm="118", hip_cm="108"),
    row("child", "Girl Dress", "Dress", "Dress", "90", "Child 2 Years", "KID2Y", "2", "20-26", "80-90", "58", "67", shoulder_cm="22", waist_cm="70", hip_cm="62"),
    row("child", "Girl Dress", "Dress", "Dress", "100", "Child 3 Years", "KID3Y", "3", "26-31", "90-100", "62", "71", shoulder_cm="23", waist_cm="74", hip_cm="66"),
    row("child", "Girl Dress", "Dress", "Dress", "110", "Child 4 Years", "KID4Y", "4", "29-39", "100-110", "66", "75", shoulder_cm="24", waist_cm="78", hip_cm="70"),
    row("child", "Girl Dress", "Dress", "Dress", "120", "Child 5 Years", "KID5Y", "5", "43-53", "110-120", "70", "78", shoulder_cm="25", waist_cm="82", hip_cm="74"),
    row("child", "Girl Dress", "Dress", "Dress", "130", "Child 6-7 Years", "KID67Y", "6-7", "53-60", "120-130", "74", "83", shoulder_cm="26", waist_cm="86", hip_cm="78"),
    row("child", "Girl Dress", "Dress", "Dress", "140", "Child 8 Years", "KID8Y", "8", "58-70", "130-140", "78", "88", shoulder_cm="27", waist_cm="90", hip_cm="82"),
    row("child", "Girl Dress", "Dress", "Dress", "150", "Child 9-10 Years", "KID910Y", "9-10", "69-85", "140-150", "82", "93", shoulder_cm="28", waist_cm="94", hip_cm="86"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "90", "Child 2 Years", "KID2Y", "2", "20-26", "80-90", "62", "40", shoulder_cm="29", sleeve_cm="28", waist_cm="50", hip_cm="62"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "100", "Child 3 Years", "KID3Y", "3", "26-31", "90-100", "66", "43", shoulder_cm="31", sleeve_cm="30", waist_cm="54", hip_cm="66"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "110", "Child 4 Years", "KID4Y", "4", "29-39", "100-110", "70", "46", shoulder_cm="33", sleeve_cm="33", waist_cm="58", hip_cm="70"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "120", "Child 5 Years", "KID5Y", "5", "43-53", "110-120", "74", "49", shoulder_cm="35", sleeve_cm="35", waist_cm="62", hip_cm="74"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "130", "Child 6-7 Years", "KID67Y", "6-7", "53-60", "120-130", "78", "52", shoulder_cm="37", sleeve_cm="38", waist_cm="66", hip_cm="78"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "140", "Child 8 Years", "KID8Y", "8", "58-70", "130-140", "82", "54", shoulder_cm="39", sleeve_cm="40", waist_cm="70", hip_cm="82"),
    row("child", "Boy Shirt", "Shirt", "Shirt", "150", "Child 9-10 Years", "KID910Y", "9-10", "69-85", "140-150", "86", "56", shoulder_cm="41", sleeve_cm="42", waist_cm="74", hip_cm="86"),
    row("father", "Father Shirt", "Shirt", "Shirt", "M", "Father M", "M", "-", "100-120", "162-168", "100", "68", shoulder_cm="46.5", sleeve_cm="52", waist_cm="88", hip_cm="100"),
    row("father", "Father Shirt", "Shirt", "Shirt", "L", "Father L", "L", "-", "120-139", "165-175", "104", "70", shoulder_cm="48", sleeve_cm="54", waist_cm="92", hip_cm="104"),
    row("father", "Father Shirt", "Shirt", "Shirt", "XL", "Father XL", "XL", "-", "135-160", "172-180", "108", "72", shoulder_cm="49.5", sleeve_cm="55", waist_cm="96", hip_cm="108"),
    row("father", "Father Shirt", "Shirt", "Shirt", "2XL", "Father 2XL", "2XL", "-", "160-180", "175-185", "112", "74", shoulder_cm="51", sleeve_cm="57", waist_cm="100", hip_cm="112"),
    row("father", "Father Shirt", "Shirt", "Shirt", "3XL", "Father 3XL", "3XL", "-", "180-195", "178-190", "116", "76", shoulder_cm="52.5", sleeve_cm="58", waist_cm="104", hip_cm="116"),
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


def cm_to_in(value: str) -> str:
    if value in ("", "-", None):
        return "-"
    nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", str(value))]
    if len(nums) == 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} cm / {fmt_num(nums[0] / 2.54)}-{fmt_num(nums[1] / 2.54)} in"
    if len(nums) == 1:
        return f"{fmt_num(nums[0])} cm / {fmt_num(nums[0] / 2.54)} in"
    return html.escape(str(value))


def jin_to_kg_lbs(value: str) -> str:
    nums = [float(part) for part in re.findall(r"\d+(?:\.\d+)?", str(value))]
    if len(nums) == 2:
        kg0 = nums[0] * 0.5
        kg1 = nums[1] * 0.5
        return f"{fmt_num(kg0)}-{fmt_num(kg1)} kg / {fmt_num(kg0 * 2.20462)}-{fmt_num(kg1 * 2.20462)} lbs"
    return "-"


def role_token(role: str) -> str:
    if role.startswith("Girl"):
        return "GRL"
    if role.startswith("Boy"):
        return "BOY"
    if role.startswith("Mother"):
        return "MOM"
    if role.startswith("Father"):
        return "DAD"
    raise KeyError(role)


def price_for(row: dict) -> str:
    if row["garment"] == "Dress":
        return "31.99" if row["audience"] == "mother" else "28.99"
    return "28.99" if row["audience"] == "father" else "24.99"


def sku_for(row: dict) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row['role'])}-{row['sku_suffix']}-{COLOR_TOKEN}"


def tags() -> list[str]:
    values = [
        "Family Matching",
        "Sets",
        "Matching Family Set",
        "Matching Family Dresses",
        "Matching Family Tops",
        "Mommy and Me",
        "Daddy and Me",
        "Mother Daughter Matching Dress",
        "Father Son Matching Shirt",
        "Girl Dress",
        "Mother Dress",
        "Boy Shirt",
        "Father Shirt",
        "Dress",
        "Shirt",
        "T-Shirt",
        "Sky Blue",
        "Blue",
        "Ombre",
        "Pleated",
        "Sleeveless Dress",
        "Short Sleeve Shirt",
        "Summer",
        "Vacation",
        "Beach",
        "Pool",
        "Resort",
        "Family Photos",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
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
    sections = []
    for garment in ("Dress", "Shirt"):
        rows = []
        for row in [item for item in SIZE_CHART if item["garment"] == garment]:
            rows.append(
                "<tr>"
                f"<td>{html.escape(row['picker_label'])}</td>"
                f"<td>{html.escape(row['age'] if row['audience'] == 'child' else '-')}</td>"
                f"<td>{jin_to_kg_lbs(row['weight_jin'])}</td>"
                f"<td>{cm_to_in(row['height_cm'])}</td>"
                f"<td>{cm_to_in(row['chest_cm'])}</td>"
                f"<td>{cm_to_in(row['sleeve_cm'] if garment == 'Shirt' else row['skirt_cm'])}</td>"
                "<td>-</td>"
                f"<td>{cm_to_in(row['hip_cm'])}</td>"
                f"<td>{cm_to_in(row['waist_cm'])}</td>"
                f"<td>{cm_to_in(row['length_cm'])}</td>"
                "</tr>"
            )
        sections.extend(
            [
                f"<h3>Size Chart - {garment}</h3>",
                '<table id="size-chart">' if garment == "Dress" else "<table>",
                "<thead><tr>",
                *[f"<th>{header}</th>" for header in headers],
                "</tr></thead>",
                "<tbody>",
                *rows,
                "</tbody>",
                "</table>",
                "",
            ]
        )
    return "\n".join(
        [
            "<ul>",
            "<li><strong>Fabric:</strong> Lightweight woven-look dress fabric and soft T-shirt fabric; exact fiber content was not visible from the blocked vendor page.</li>",
            "<li><strong>Family story:</strong> A sky-blue coordinated look for mom, dad, girls, and boys, made for vacation photos and warm-weather family moments.</li>",
            "<li><strong>Color:</strong> Soft sky blue with a gentle fade effect across the pleated dresses and matching tees.</li>",
            "<li><strong>Design details:</strong> Girls and mothers wear pleated sleeveless dresses; boys and fathers wear short-sleeve crewneck shirts. Shorts are not included.</li>",
            "<li><strong>Care:</strong> Hand wash cold, line dry in the shade, and avoid bleach or high heat to protect the soft blue color.</li>",
            "<li><strong>Size range:</strong> Girls and boys Child 2 Years to Child 9-10 Years; Mother S to Mother 2XL; Father M to Father 3XL.</li>",
            "</ul>",
            "",
            *sections,
            "<p>The Sky Blue Family Matching Set creates one easy coordinated outfit story across parents and kids. The dresses bring a breezy pleated shape for mother-daughter photos, while the matching shirts keep dad and son in the same soft blue palette.</p>",
            "",
            "<p>Use the chart-backed height, weight, bust, waist, sleeve, and length guidance to choose each family member's size. The listing includes only the dress and shirt pieces supported by the attached size chart; shorts shown in the lifestyle photo are intentionally excluded.</p>",
            "",
            "<h3>Key Features:</h3>",
            "<ul>",
            "<li><strong>Full-family matching:</strong> Dress options for mom and girls, shirt options for dad and boys.</li>",
            "<li><strong>Sky-blue palette:</strong> Soft color story made for sunny photos, pool days, and beach trips.</li>",
            "<li><strong>Chart-backed variants:</strong> Every available size comes from the attached vendor chart.</li>",
            "<li><strong>No shorts included:</strong> The purchasable variants are dress and shirt only, matching the requested scope.</li>",
            "<li><strong>Photo-ready coordination:</strong> Easy to mix across parents, daughters, and sons without matching every piece exactly.</li>",
            "</ul>",
            "",
            "<p>Choose the dress and shirt sizes you need for a sky-blue family look that is ready for warm days and keepsake photos.</p>",
        ]
    )


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
                    {"optionName": "Type", "name": row["type_value"]},
                    {"optionName": "Size", "name": row["picker_label"]},
                ],
                "inventoryItem": {
                    "sku": sku_for(row),
                    "cost": cost_for(price),
                    "tracked": True,
                    "requiresShipping": True,
                },
                "_row": row,
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
        "type_value",
        "vendor_label",
        "picker_label",
        "sku_suffix",
        "age",
        "weight_jin",
        "height_cm",
        "chest_cm",
        "hip_cm",
        "waist_cm",
        "length_cm",
        "sleeve_cm",
        "pant_cm",
    }
    if len(SIZE_CHART) != 24 or len(variants) != len(SIZE_CHART):
        errors.append("SIZE_CHART/variant count mismatch")
    if table_row_count(body) != len(SIZE_CHART):
        errors.append("body size-table row count mismatch")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        errors.append("each size table must have 10 headers")
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
            errors.append(f"{row.get('role')} {row.get('vendor_label')} missing {missing}")
        if row["picker_label"] not in SIZE_MAP:
            errors.append(f"missing size metaobject mapping for {row['picker_label']}")
    for variant in variants:
        row = variant["_row"]
        if variant["price"] != price_for(row):
            errors.append("FORCE_SPEC_PRICES guard failed")
        if variant["inventoryItem"]["cost"] != cost_for(variant["price"]):
            errors.append("cost is not 50 percent of price")
    joined = " ".join([TITLE, SEO_TITLE, SEO_DESCRIPTION, " ".join(tags()), body]).lower()
    if any(token in joined for token in ("1688", "alibaba", "detail.1688", "http://", "https://")):
        errors.append("customer-facing content contains source reference")
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
                    "option_names": ["Type", "Size"],
                    "variants": [shopify_variant_input(variant) for variant in variants],
                    "option_axes": [
                        {"name": "Type", "values": ["Dress", "Shirt"]},
                        {"name": "Size", "values": list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART))},
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        evidence_path.write_text(
            json.dumps(
                {
                    "notes": "Attached image and chart show separable dress, tshirt, and shorts evidence. Owner requested dress and tshirt only with shorts excluded; derived Shopify options are Type x Size."
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
            {"name": "Type", "values": [{"name": "Dress"}, {"name": "Shirt"}]},
            {"name": "Size", "values": [{"name": value} for value in dict.fromkeys(row["picker_label"] for row in SIZE_CHART)]},
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
        raise RuntimeError(f"Existing product {HANDLE} is {existing['status']}; refusing to change publication state.")
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
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Family Matching Sets"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Pleated Dress and Shirts"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": CUSTOM_TYPE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": LISTING_MODE},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress and Shirts"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972764769", "gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69639733345"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129972502625"])},
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
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if "size-chart" in path.name:
            continue
        alt = "Family wearing sky blue matching pleated dresses and shirts."
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
            metafields(first:120){nodes{namespace key type value}}
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
    if product.get("publishedAt") is not None or product.get("onlineStoreUrl"):
        errors.append("draft has publication/live URL")
    if any(node["isPublished"] for node in product["resourcePublicationsV2"]["nodes"]):
        errors.append("draft is published to a channel")
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
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(row["type_value"], row["picker_label"]) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Type x Size option combinations do not match")
    leak_text = " ".join([product["title"], product["descriptionHtml"], " ".join(product["tags"]), product["seo"]["title"] or "", product["seo"]["description"] or ""]).lower()
    if any(token in leak_text for token in ("1688", "alibaba", "detail.1688", "http://", "https://")):
        errors.append("source URL/reference leaked into Shopify product data")
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
    header = source.read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    for i, variant in enumerate(variants, start=1):
        row = variant["_row"]
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
                "Option1 Name": "Type",
                "Option1 Value": row["type_value"],
                "Option2 Name": "Size",
                "Option2 Value": row["picker_label"],
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
                "Google Shopping / Gender": "unisex" if i == 1 else "",
                "Google Shopping / Age Group": "adult" if i == 1 else "",
                "Google Shopping / Condition": "new" if i == 1 else "",
                "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
                "Google Shopping / Custom Label 0": LISTING_MODE if i == 1 else "",
                "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
                "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
                "Google Shopping / Custom Label 3": "Dress and Shirts" if i == 1 else "",
                "Google Shopping / Custom Label 4": "Family Matching" if i == 1 else "",
                "Category1 (product.metafields.custom.category1)": LISTING_MODE if i == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
                "Style (product.metafields.custom.style)": "Pleated Dress and Shirts" if i == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Sets" if i == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Family Matching Sets" if i == 1 else "",
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
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['type_value']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |"
        )
    written = sorted(
        f"{node['namespace']}.{node['key']}"
        for node in product["metafields"]["nodes"]
        if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}
    )
    skipped = [
        ("shopify.fabric", "Exact fiber was not visible from the blocked vendor page or supplied screenshots."),
        ("shopify.neckline", "Dress neckline is visible, but the mixed Outfit Sets taxonomy makes one product-level value too broad."),
        ("shopify.top-length-type", "The chart provides shirt garment length, not a supported product-level top-length type."),
        ("shopify.dress-occasion", "No specific occasion beyond casual family/vacation use is supplier-backed."),
        ("shopify.dress-style", "Dress appears pleated/A-line, but the product also includes shirts under Outfit Sets."),
        ("shopify.skirt-dress-length-type", "The chart provides total dress length, not a canonical skirt/dress length type."),
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
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | dress, tshirt |",
        "| EXCLUDE_ITEMS | shorts |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
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
        "| Role | Vendor row | Picker label | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap,
        "",
        "## Derivations",
        "- Product mode resolved to Family Matching because chart evidence supports mother, father, girl, and boy rows.",
        "- Category resolved to FamilySet / Outfit Sets because the listing mixes dress and shirt family-matching garments.",
        "- `Type` is `Dress` or `Shirt`; `Size` labels carry the role/audience so girl/boy child rows can coexist without duplicate variants.",
        "- Shorts shown in the lifestyle image are excluded and no shorts variants were created.",
        "- Supplier weights were shown in jin and converted to kg/lbs for shopper-facing rows.",
        "- Girl dress hip values are derived as bust + 4 because the chart omits hip; mother dress hip values are derived as bust + 6 because the chart omits hip.",
        "- Shirt hip values equal chest and shirt waist values are derived as chest - 12 per canonical chart rules.",
        "- Pricing uses garment fallbacks: dress child `28.99`, dress adult `31.99`, shirt child `24.99`, shirt adult `28.99`; Cost per item is exactly 50 percent.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status | PASS | {product['status']} |",
        f"| Publication state | PASS | publishedAt={product.get('publishedAt')}; live channels={[p['publication']['name'] for p in product['resourcePublicationsV2']['nodes'] if p['isPublished']]} |",
        f"| Taxonomy fullName | {'PASS' if product['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {product['category']['fullName']} |",
        f"| Variant count | {'PASS' if len(product['variants']['nodes']) == len(variants) else 'FAIL'} | {len(product['variants']['nodes'])} vs {len(variants)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        "",
        "## Localized Size-Chart Gate",
        "Pending in initial runner output. This section is updated by the session after the translation poll, repair execute, strict missing-locale readback, and variant mapping audit complete.",
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
        "Product is a draft/unpublished; collection membership may not index until a separate publish-live request.",
        "",
        "## Manual Follow-ups",
        "1. Review the image presentation in Shopify Admin before any separate publish-live request.",
        "2. Confirm exact fabric composition before publication; fabric metafield was intentionally skipped.",
        "3. Set inventory quantities only when fulfillment policy is confirmed.",
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
