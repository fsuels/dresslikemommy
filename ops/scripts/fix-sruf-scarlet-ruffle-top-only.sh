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
import os
import re
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "scarlet-ruffle-mommy-and-me-set"
TITLE = "Scarlet Ruffle Mommy and Me Tank Top - Breezy Beach Top"
SEO_TITLE = "Scarlet Mommy and Me Tank Top | Dress Like Mommy"
SEO_DESCRIPTION = "Red ruffle mommy-and-me tank tops for mom and daughter. Adjustable strap sizing in Child 3Y-9-10Y and Mother S-M."
PRINT_NAME = "Scarlet Ruffle"
PRODUCT_TYPE = "Matching Family Tops"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-13-9"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Clothing Tops > Tank Tops"
VENDOR = "dresslikemommy.com"
VENDOR_URL = "https://detail.1688.com/offer/1044710581583.html"

LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"

SIZE_CHART = [
    {"audience": "child", "role": "Girl Top", "vendor_label": "100", "picker_label": "Child 3 Years", "age": "3", "height": "96-105 cm", "strap_cm": 44, "hem_cm": 44},
    {"audience": "child", "role": "Girl Top", "vendor_label": "110", "picker_label": "Child 4 Years", "age": "4", "height": "106-115 cm", "strap_cm": 48, "hem_cm": 46},
    {"audience": "child", "role": "Girl Top", "vendor_label": "120", "picker_label": "Child 5 Years", "age": "5", "height": "116-125 cm", "strap_cm": 51, "hem_cm": 49},
    {"audience": "child", "role": "Girl Top", "vendor_label": "130", "picker_label": "Child 6-7 Years", "age": "6-7", "height": "126-135 cm", "strap_cm": 54, "hem_cm": 52},
    {"audience": "child", "role": "Girl Top", "vendor_label": "140", "picker_label": "Child 8 Years", "age": "8", "height": "136-145 cm", "strap_cm": 59, "hem_cm": 55},
    {"audience": "child", "role": "Girl Top", "vendor_label": "150", "picker_label": "Child 9-10 Years", "age": "9-10", "height": "145-155 cm", "strap_cm": 64, "hem_cm": 58},
    {"audience": "mother", "role": "Mother Top", "vendor_label": "S", "picker_label": "Mother S", "age": "-", "height": "-", "strap_cm": 72, "hem_cm": 65},
    {"audience": "mother", "role": "Mother Top", "vendor_label": "M", "picker_label": "Mother M", "age": "-", "height": "-", "strap_cm": 74, "hem_cm": 69},
]

SIZE_MAP = {
    "Child 3 Years": "gid://shopify/Metaobject/129972895841",
    "Child 4 Years": "gid://shopify/Metaobject/129972928609",
    "Child 5 Years": "gid://shopify/Metaobject/129972961377",
    "Child 6-7 Years": "gid://shopify/Metaobject/139840323681",
    "Child 8 Years": "gid://shopify/Metaobject/129973026913",
    "Child 9-10 Years": "gid://shopify/Metaobject/129971552353",
    "Mother S": "gid://shopify/Metaobject/129975255137",
    "Mother M": "gid://shopify/Metaobject/129975222369",
}


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


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def fmt_num(value) -> str:
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:.1f}".rstrip("0").rstrip(".")


def cm_to_in(value) -> str:
    number = float(value)
    return f"{fmt_num(number)} cm / {fmt_num(number / 2.54)} in"


def height_to_in(text: str) -> str:
    nums = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", text or "")]
    if len(nums) >= 2:
        return f"{fmt_num(nums[0])}-{fmt_num(nums[1])} cm / {fmt_num(nums[0] / 2.54)}-{fmt_num(nums[1] / 2.54)} in"
    return "-"


def build_body() -> str:
    headers = ["Size", "Age", "Height (cm/in)", "Adjustable Strap (cm/in)", "Hem/Body Opening (cm/in)"]
    rows = []
    for row in SIZE_CHART:
        cells = [
            row["picker_label"],
            row["age"] if row["audience"] == "child" else "-",
            height_to_in(row["height"]),
            cm_to_in(row["strap_cm"]),
            cm_to_in(row["hem_cm"]),
        ]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>")

    return "\n\n".join([
        "<ul>",
        "<li><strong>Fabric:</strong> Lightweight woven-look summer fabric; exact fiber composition was not visible in the supplied evidence.</li>",
        "<li><strong>Family story:</strong> A bright mom-and-daughter tank top for beach trips, resort photos, and sunny family days.</li>",
        "<li><strong>Print:</strong> Scarlet Ruffle is a vivid red ruffle tank top. Pants, bottoms, and accessories are not included.</li>",
        "<li><strong>Design details:</strong> Adjustable shoulder straps and soft layered ruffles create an easy warm-weather top.</li>",
        "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.</li>",
        "<li><strong>Size range:</strong> Child 3 Years through Child 9-10 Years and Mother S-M from the attached vendor chart.</li>",
        "</ul>",
        "<h3>Size Chart - Tank Top</h3>\n<table id=\"size-chart\">\n<thead><tr>\n" + "\n".join(f"<th>{header}</th>" for header in headers) + "\n</tr></thead>\n<tbody>\n" + "\n".join(rows) + "\n</tbody></table>",
        "<p>Scarlet Ruffle is made for cheerful mother-daughter moments, from beach photos to warm-weather brunches and vacation strolls. The vivid red ruffle tank top gives the look its bright focal point while staying easy to pair with your own shorts, skirts, or pants.</p>",
        "<p>This listing is for the tank top only. The size table uses the supplied strap and opening measurements; unavailable bust, hip, and total garment-length values are intentionally not estimated.</p>",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Tank top only:</strong> Includes the red ruffle top; bottoms and styling pieces shown in photos are not included.</li>",
        "<li><strong>Mother-daughter sizing:</strong> Includes girl and mother rows only where the vendor chart provides measurements.</li>",
        "<li><strong>Adjustable straps:</strong> Strap measurements are copied from the attached size chart.</li>",
        "<li><strong>Ruffle cami shape:</strong> Bright red layered ruffles create a photo-ready summer style.</li>",
        "<li><strong>Easy outfit pairing:</strong> Style it with your own beach pants, denim shorts, skirts, or vacation basics.</li>",
        "</ul>",
        "<p>Choose each size to build a coordinated red mommy-and-me top moment for the next sunny day together.</p>",
    ])


def corrected_tags(existing_tags: list[str]) -> list[str]:
    remove = {
        "Dresses", "Sets", "Matching Family Sets", "Mommy and Me Set",
        "Mother Daughter Set", "Girl Set", "Mother Set", "Two-Piece Set",
        "Wide Leg Pants",
    }
    add = {
        "Mommy and Me", "Mommy and Me Top", "Matching Family Tops", "Tank Top",
        "Girl Top", "Mother Top", "Ruffle Tank Top", "Summer", "Beach",
        "Vacation", "Resort", "Red", "Scarlet", "Scarlet Ruffle", "Tops",
    }
    tags = {tag for tag in existing_tags if tag not in remove and "Set" not in tag}
    tags.update(add)
    tags.update(row["picker_label"] for row in SIZE_CHART)
    tags.update(row["role"] for row in SIZE_CHART)
    return sorted(tags)


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def main() -> None:
    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{ id fullName isLeaf } } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    read_query = """query($handle:String!){
      productByHandle(handle:$handle){
        id title handle status publishedAt onlineStoreUrl productType tags descriptionHtml
        category{id fullName}
        seo{title description}
        options{name values}
        variants(first:100){nodes{id sku title price compareAtPrice selectedOptions{name value} inventoryPolicy inventoryItem{id tracked requiresShipping unitCost{amount currencyCode}}}}
        metafields(first:140){nodes{id namespace key type value}}
        resourcePublicationsV2(first:20){nodes{isPublished publishDate publication{id name}}}
      }
    }"""
    product = gql(read_query, {"handle": HANDLE})["data"]["productByHandle"]
    if not product:
        raise RuntimeError(f"Missing product for handle {HANDLE}")
    product_id = product["id"]
    publication_state = {
        "status": product["status"],
        "publishedAt": product["publishedAt"],
        "published_count": sum(1 for node in product["resourcePublicationsV2"]["nodes"] if node["isPublished"]),
    }

    body = build_body()
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")

    product_input = {
        "id": product_id,
        "title": TITLE,
        "descriptionHtml": body,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": corrected_tags(product["tags"]),
        "status": product["status"],
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }
    res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status productType category{id fullName}} userErrors{field message} } }""", {"product": product_input})
    require_no_user_errors(res, ["data", "productUpdate", "userErrors"])

    variants = []
    for node in product["variants"]["nodes"]:
        variants.append({
            "id": node["id"],
            "price": node["price"],
            "compareAtPrice": node["compareAtPrice"],
            "taxable": True,
            "inventoryPolicy": "DENY",
            "inventoryItem": {
                "sku": node["sku"],
                "cost": cost_for(node["price"]),
                "tracked": True,
                "requiresShipping": True,
            },
            "optionValues": [
                {"optionName": opt["name"], "name": opt["value"]}
                for opt in node["selectedOptions"]
            ],
        })
    res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price inventoryItem{unitCost{amount currencyCode}}} userErrors{field message} } }""", {"productId": product_id, "variants": variants})
    require_no_user_errors(res, ["data", "productVariantsBulkUpdate", "userErrors"])

    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]] for row in SIZE_CHART))
    mf = [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Mommy and Me"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Mommy and Me Tops"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Mommy and Me Top"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Tank Top"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Tank Top"},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
    ]
    res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mf})
    require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    stale_metafields = [
        {"ownerId": product_id, "namespace": node["namespace"], "key": node["key"]}
        for node in product["metafields"]["nodes"]
        if (node["namespace"], node["key"]) in {
            ("shopify", "dress-occasion"),
            ("shopify", "dress-style"),
            ("shopify", "skirt-dress-length-type"),
        }
    ]
    if stale_metafields:
        res = gql("""mutation($metafields:[MetafieldIdentifierInput!]!){ metafieldsDelete(metafields:$metafields){ deletedMetafields{key namespace ownerId} userErrors{field message} } }""", {"metafields": stale_metafields})
        require_no_user_errors(res, ["data", "metafieldsDelete", "userErrors"])

    verify = gql(read_query, {"handle": HANDLE})["data"]["productByHandle"]
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")

    header = (ROOT / "ops/listings/fresh-blue-plaid-family-matching-set-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    by_size = {row["picker_label"]: row for row in SIZE_CHART}
    rows = []
    for i, node in enumerate(verify["variants"]["nodes"], start=1):
        size = next((opt["value"] for opt in node["selectedOptions"] if opt["name"] == "Size"), "")
        chart = by_size.get(size, {})
        values = {key: "" for key in header}
        values.update({
            "Handle": HANDLE,
            "Title": TITLE if i == 1 else "",
            "Body (HTML)": body if i == 1 else "",
            "Vendor": VENDOR if i == 1 else "",
            "Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
            "Type": PRODUCT_TYPE if i == 1 else "",
            "Tags": ", ".join(verify["tags"]) if i == 1 else "",
            "Published": "TRUE" if verify["status"] == "ACTIVE" else "FALSE",
            "Option1 Name": "Type",
            "Option1 Value": "Tank Top",
            "Option2 Name": "Size",
            "Option2 Value": size,
            "Variant SKU": node["sku"],
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": node["price"],
            "Variant Compare At Price": node["compareAtPrice"],
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Gift Card": "FALSE",
            "SEO Title": SEO_TITLE if i == 1 else "",
            "SEO Description": SEO_DESCRIPTION if i == 1 else "",
            "Category1 (product.metafields.custom.category1)": "Mommy and Me" if i == 1 else "",
            "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
            "Style (product.metafields.custom.style)": "Mommy and Me Top" if i == 1 else "",
            "SubCategory (product.metafields.custom.subcategory)": "Tops" if i == 1 else "",
            "SubCategory2 (product.metafields.custom.subcategory2)": "Mommy and Me Tops" if i == 1 else "",
            "Type (product.metafields.custom.type)": "Tank Top" if i == 1 else "",
            "Google Shopping / Custom Label 3": "Tank Top" if i == 1 else "",
            "Cost per item": cost_for(node["price"]),
            "Status": verify["status"].lower(),
        })
        if chart:
            values["Variant Grams"] = "300"
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    mfs = {(node["namespace"], node["key"]): node["value"] for node in verify["metafields"]["nodes"]}
    price_rows = []
    errors = []
    if verify["status"] != publication_state["status"]:
        errors.append("publication status changed")
    if verify["publishedAt"] != publication_state["publishedAt"]:
        errors.append("publishedAt changed")
    if sum(1 for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]) != publication_state["published_count"]:
        errors.append("publication count changed")
    if verify["category"]["fullName"] != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"category is {verify['category']['fullName']}")
    if mfs.get(("custom", "subcategory")) != "Tops":
        errors.append("custom.subcategory is not Tops")
    if mfs.get(("custom", "type")) != "Tank Top":
        errors.append("custom.type is not Tank Top")
    if "Set" in " ".join([verify["title"], verify["descriptionHtml"], verify["seo"]["title"] or "", verify["seo"]["description"] or ""]):
        errors.append("shopper-facing title/body/SEO still contains Set")
    if table_row_count(verify["descriptionHtml"]) != len(SIZE_CHART):
        errors.append("size table row count mismatch")
    for node in verify["variants"]["nodes"]:
        live_cost = ((node["inventoryItem"] or {}).get("unitCost") or {}).get("amount")
        expected_cost = cost_for(node["price"])
        match = live_cost is not None and Decimal(live_cost) == Decimal(expected_cost)
        price_rows.append({"sku": node["sku"], "price": node["price"], "cost": live_cost, "expected_cost": expected_cost, "match": match})
        if not match:
            errors.append(f"cost mismatch for {node['sku']}")
        if any(opt["value"] == "Two-Piece Set" for opt in node["selectedOptions"]):
            errors.append(f"stale variant option for {node['sku']}")
    if VENDOR_URL in verify["descriptionHtml"] or VENDOR_URL in " ".join(verify["tags"]) or VENDOR_URL in json.dumps(verify["metafields"]["nodes"]):
        errors.append("source URL leaked to Shopify-visible fields")

    LISTING_MD.write_text("\n".join([
        f"# {TITLE}",
        "",
        "## Correction",
        "- Owner reported this product is the tank top only, not a set.",
        "- Updated Shopify taxonomy to `Clothing Tops > Tank Tops`.",
        "- Updated breadcrumb-driving metafields to `custom.subcategory = Tops` and `custom.type = Tank Top`.",
        "- Removed set/pants language from customer-facing title, body, SEO, and tags.",
        "- Preserved the existing handle, active status, publication timestamp, and sales-channel publications.",
        "- Preserved current variant prices and updated Cost per item to 50% of those current prices.",
        "",
        "## Verification",
        f"- Status: `{verify['status']}`",
        f"- Published at: `{verify['publishedAt']}`",
        f"- Online Store URL: `{verify['onlineStoreUrl']}`",
        f"- Category: `{verify['category']['fullName']}`",
        f"- Product type: `{verify['productType']}`",
        f"- Breadcrumb metafields: `custom.subcategory={mfs.get(('custom', 'subcategory'))}`, `custom.type={mfs.get(('custom', 'type'))}`",
        f"- Variant count: `{len(verify['variants']['nodes'])}`",
        f"- Price/cost parity: `{'PASS' if all(row['match'] for row in price_rows) else 'FAIL'}`",
        "",
        "## Price/Cost Rows",
        "| SKU | Price | Cost | Expected Cost | Match |",
        "|---|---:|---:|---:|---|",
        *[f"| `{row['sku']}` | {row['price']} | {row['cost']} | {row['expected_cost']} | {'yes' if row['match'] else 'no'} |" for row in price_rows],
        "",
        "## Residual Risks",
        "- Exact fabric composition remains unverified.",
        "- The original size-chart image also contains a pants-length column, but the owner clarified the Shopify listing should sell only the tank top. The customer-facing chart now uses only strap and opening measurements.",
        "- The handle still ends in `-set` to preserve the live URL supplied by the owner.",
    ]), encoding="utf-8")

    if errors:
        raise RuntimeError("VERIFY FAILED:\n- " + "\n- ".join(dict.fromkeys(errors)))

    print(json.dumps({
        "product_id": product_id,
        "status": verify["status"],
        "publishedAt": verify["publishedAt"],
        "onlineStoreUrl": verify["onlineStoreUrl"],
        "title": verify["title"],
        "productType": verify["productType"],
        "category": verify["category"]["fullName"],
        "custom_subcategory": mfs.get(("custom", "subcategory")),
        "custom_type": mfs.get(("custom", "type")),
        "price_cost_parity": all(row["match"] for row in price_rows),
        "files": [str(LISTING_MD), str(CSV_OUT), str(BODY_HTML_OUT), str(VERIFY_JSON_OUT)],
    }, indent=2))


if __name__ == "__main__":
    main()
PY
