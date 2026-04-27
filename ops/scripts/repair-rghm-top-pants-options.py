#!/usr/bin/env python3
"""Repair Red Gingham variants so shoppers choose Top or Pants before Size."""

from __future__ import annotations

import json
import csv
import re
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from shopify_admin_config import load_access_token, resolve_store_domain


ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
PRODUCT_ID = "gid://shopify/Product/7537366597729"
HANDLE = "red-gingham-mommy-and-me-set"
VERIFY_OUT = ROOT / "ops/listings/verify-red-gingham-mommy-and-me-set.json"
LISTING_MD = ROOT / "ops/listings/red-gingham-mommy-and-me-set-listing.md"
BODY_HTML_OUT = ROOT / "ops/listings/body-red-gingham-mommy-and-me-set.html"
SIZE_CHART_OUT = ROOT / "ops/listings/size-chart-red-gingham-mommy-and-me-set.json"
CSV_OUT = ROOT / "ops/listings/red-gingham-mommy-and-me-set-shopify-import.csv"

SIZES = [
    ("Child 2 Years", "GRL", "KID2Y", "28.99", "33.99"),
    ("Child 3 Years", "GRL", "KID3Y", "28.99", "33.99"),
    ("Child 4 Years", "GRL", "KID4Y", "28.99", "33.99"),
    ("Child 5 Years", "GRL", "KID5Y", "28.99", "33.99"),
    ("Child 6-7 Years", "GRL", "KID67Y", "28.99", "33.99"),
    ("Child 8 Years", "GRL", "KID8Y", "28.99", "33.99"),
    ("Mother M", "MOM", "M", "31.99", "36.99"),
]
TYPE_SKU = {"Top": "TOP", "Pants": "PNT"}
PUBLICATIONS = [
    "gid://shopify/Publication/55169925",
    "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225",
    "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
]


def gql(query: str, variables: Dict[str, Any] | None = None) -> Dict[str, Any]:
    store = resolve_store_domain(fallback_domain="dresslikemommy-com.myshopify.com")
    token = load_access_token()
    request = urllib.request.Request(
        f"https://{store}/admin/api/2025-01/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload


def user_errors(payload: Dict[str, Any], path: List[str]) -> List[Dict[str, Any]]:
    node: Any = payload
    for key in path:
        node = node.get(key, {})
    return node.get("userErrors", []) or []


def require_no_user_errors(payload: Dict[str, Any], path: List[str], label: str) -> None:
    errors = user_errors(payload, path)
    if errors:
        raise RuntimeError(f"{label} userErrors: {json.dumps(errors, indent=2)}")


PRODUCT_QUERY = """
query ProductForRepair($id: ID!) {
  product(id: $id) {
    id
    title
    handle
    status
    publishedAt
    onlineStoreUrl
    descriptionHtml
    tags
    options {
      id
      name
      position
      values
      optionValues { id name hasVariants }
    }
    variants(first: 100) {
      nodes {
        id
        sku
        title
        price
        compareAtPrice
        inventoryPolicy
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping }
      }
    }
    seo { title description }
    category { id fullName }
    metafields(first: 100) { nodes { namespace key type value } }
    resourcePublicationsV2(first: 20) {
      nodes { isPublished publication { id name } }
    }
  }
}
"""


def fetch_product() -> Dict[str, Any]:
    return gql(PRODUCT_QUERY, {"id": PRODUCT_ID})["data"]["product"]


def option_names(product: Dict[str, Any]) -> List[str]:
    return [option["name"] for option in product["options"]]


def body_html() -> str:
    corrected_chart = corrected_size_chart()
    SIZE_CHART_OUT.write_text(json.dumps(corrected_chart, indent=2), encoding="utf-8")
    rows = []
    for type_name, measurement in [
        ("Top", ("Chest/Bust", "Garment Length")),
        ("Pants", ("Waist", "Pant Length")),
    ]:
        rows.append(f"<h3>Size Chart - {type_name}</h3>")
        rows.append(
            """<table id="size-chart">
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
  <tbody>"""
        )
        chart = [row for row in corrected_chart if row["garment"] == type_name]
        for row in chart:
            rows.append(
                "<tr>"
                f"<td>{row['picker_label']}</td>"
                f"<td>{row['age']}</td>"
                f"<td>{row['weight']}</td>"
                f"<td>{row['height']}</td>"
                f"<td>{row['chest_cm']} cm / {float(row['chest_cm']) / 2.54:.1f} in</td>"
                "<td>-</td>"
                f"<td>{row['pant_cm']} cm / {float(row['pant_cm']) / 2.54:.1f} in</td>"
                f"<td>{row['hip_cm']} cm / {float(row['hip_cm']) / 2.54:.1f} in</td>"
                f"<td>{row['waist_cm']} cm / {float(row['waist_cm']) / 2.54:.1f} in</td>"
                f"<td>{row['length_cm']} cm / {float(row['length_cm']) / 2.54:.1f} in</td>"
                "</tr>"
            )
        rows.append("  </tbody>\n</table>")
    return "\n".join(
        [
            "<ul>",
            "<li><strong>Fabric:</strong> Lightweight cotton-blend separates: a white sleeveless lace-trim top and red gingham pants.</li>",
            "<li><strong>Family story:</strong> Pick matching pieces for mom and daughter, or buy the top and pants together for the full picnic-ready look.</li>",
            "<li><strong>Print:</strong> Red Gingham pairs crisp white texture with cheerful red checked bottoms.</li>",
            "<li><strong>Design details:</strong> Choose the airy gathered top or the relaxed pull-on gingham pants in each available size.</li>",
            "<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and use a cool iron on the reverse if needed.</li>",
            "<li><strong>Size range:</strong> Girls Child 2 Years to Child 8 Years; Mother M.</li>",
            "</ul>",
            *rows,
            "<p>Build the Red Gingham Mommy and Me look one piece at a time. The white lace-trim top and red gingham pants are sold as separate choices, so each shopper can select the exact garment and size needed.</p>",
            "<p>Order both pieces for the full coordinated outfit, or choose a single top or pair of pants to mix with closet favorites for vacations, picnics, and summer photos.</p>",
            "<h3>Key Features:</h3>",
            "<ul>",
            "<li><strong>Separate item picker:</strong> Select Top or Pants before choosing the size.</li>",
            "<li><strong>Photo-ready contrast:</strong> White lace trim and red gingham create a classic picnic palette.</li>",
            "<li><strong>Easy matching:</strong> Mom and daughter sizes share the same coordinated styling.</li>",
            "<li><strong>Summer comfort:</strong> Lightweight cotton-blend fabric keeps the look breezy.</li>",
            "</ul>",
            "<p>Choose the piece, choose the size, and create the matching moment your family needs.</p>",
        ]
    )


def corrected_size_chart() -> List[Dict[str, Any]]:
    source_rows = json.loads(SIZE_CHART_OUT.read_text(encoding="utf-8"))
    by_picker: Dict[str, Dict[str, Any]] = {}
    for row in source_rows:
        by_picker.setdefault(row["picker_label"], row)

    corrected: List[Dict[str, Any]] = []
    for type_name in ("Top", "Pants"):
        for label, role_token, _size_token, _price, _compare in SIZES:
            row = dict(by_picker[label])
            audience = "mother" if role_token == "MOM" else "child"
            role_prefix = "Mother" if audience == "mother" else "Girl"
            row["audience"] = audience
            row["role"] = f"{role_prefix} {type_name}"
            row["garment"] = type_name
            row["sku_suffix"] = f"{TYPE_SKU[type_name]}-{row['sku_suffix']}"
            corrected.append(row)
    return corrected


def ensure_type_option() -> None:
    product = fetch_product()
    if "Type" in option_names(product):
        return
    mutation = """
    mutation AddType($productId: ID!, $options: [OptionCreateInput!]!, $variantStrategy: ProductOptionCreateVariantStrategy) {
      productOptionsCreate(productId: $productId, options: $options, variantStrategy: $variantStrategy) {
        product { id options { id name values optionValues { id name hasVariants } } }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        mutation,
        {
            "productId": PRODUCT_ID,
            "options": [{"name": "Type", "values": [{"name": "Top"}, {"name": "Pants"}]}],
            "variantStrategy": "CREATE",
        },
    )
    require_no_user_errors(payload, ["data", "productOptionsCreate"], "productOptionsCreate")


def delete_color_option_if_present() -> None:
    product = fetch_product()
    color_options = [option for option in product["options"] if option["name"] == "Color"]
    if not color_options:
        return
    mutation = """
    mutation DeleteColor($productId: ID!, $options: [ID!]!, $strategy: ProductOptionDeleteStrategy) {
      productOptionsDelete(productId: $productId, options: $options, strategy: $strategy) {
        deletedOptionsIds
        product { id options { id name values optionValues { id name hasVariants } } }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        mutation,
        {"productId": PRODUCT_ID, "options": [color_options[0]["id"]], "strategy": "NON_DESTRUCTIVE"},
    )
    require_no_user_errors(payload, ["data", "productOptionsDelete"], "productOptionsDelete")


def reorder_options() -> None:
    product = fetch_product()
    names = option_names(product)
    expected = ["Type", "Size"]
    if names == expected:
        return
    values_by_name = {option["name"]: option["values"] for option in product["options"]}
    mutation = """
    mutation Reorder($productId: ID!, $options: [OptionReorderInput!]!) {
      productOptionsReorder(productId: $productId, options: $options) {
        product { id options { id name position values optionValues { id name hasVariants } } }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        mutation,
        {
            "productId": PRODUCT_ID,
            "options": [
                {"name": "Type", "values": [{"name": value} for value in values_by_name["Type"]]},
                {"name": "Size", "values": [{"name": value} for value in values_by_name["Size"]]},
            ],
        },
    )
    require_no_user_errors(payload, ["data", "productOptionsReorder"], "productOptionsReorder")


def expected_sku(type_name: str, size_name: str) -> str:
    for label, role_token, size_token, _price, _compare in SIZES:
        if label == size_name:
            return f"DLM-RGHM-{TYPE_SKU[type_name]}-{role_token}-{size_token}-RED"
    raise ValueError(f"Unexpected size label: {size_name}")


def price_for_size(size_name: str) -> tuple[str, str]:
    for label, _role_token, _size_token, price, compare in SIZES:
        if label == size_name:
            return price, compare
    raise ValueError(f"Unexpected size label: {size_name}")


def update_product_and_variants() -> None:
    product = fetch_product()
    updates = []
    for variant in product["variants"]["nodes"]:
        selected = {item["name"]: item["value"] for item in variant["selectedOptions"]}
        type_name = selected.get("Type")
        size_name = selected.get("Size")
        if type_name not in TYPE_SKU or not size_name:
            raise RuntimeError(f"Unexpected variant options for {variant['id']}: {selected}")
        price, compare = price_for_size(size_name)
        updates.append(
            {
                "id": variant["id"],
                "price": price,
                "compareAtPrice": compare,
                "inventoryPolicy": "DENY",
                "inventoryItem": {
                    "sku": expected_sku(type_name, size_name),
                    "tracked": True,
                    "requiresShipping": True,
                },
                "optionValues": [
                    {"optionName": "Type", "name": type_name},
                    {"optionName": "Size", "name": size_name},
                ],
            }
        )

    body = body_html()
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    tags = [
        "Beach",
        "Checkered",
        "Child 2-3yr",
        "Child 4-5yr",
        "Child 6-8yr",
        "Cotton Blend",
        "Gingham",
        "Girl Pants",
        "Girl Top",
        "https://detail.1688.com/offer/1041874678820.html",
        "Lace Trim",
        "Matching Family Outfits",
        "Matching Family Separates",
        "Matching Family Set",
        "Mom Size M",
        "Mommy and Me",
        "Mother M",
        "Mother Pants",
        "Mother Top",
        "Pants",
        "Red",
        "Red Gingham",
        "Sleeveless Top",
        "Summer",
        "Top",
        "Vacation",
        "White",
        "Wide-Leg Pants",
        "category1:Mommy and Me",
        "subcategory:Sets",
        "subcategory2:Summer Matching Sets",
        "type:Two-Piece Separates",
        "style:Lace Top & Gingham Pants",
        "pattern:Red Gingham",
    ]
    product_mutation = """
    mutation UpdateProduct($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title handle status publishedAt options { name values } }
        userErrors { field message }
      }
    }
    """
    product_payload = gql(
        product_mutation,
        {
            "input": {
                "id": PRODUCT_ID,
                "title": "Red Gingham Mommy and Me Separates - Top or Pants",
                "descriptionHtml": body,
                "tags": tags,
                "status": "DRAFT",
                "seo": {
                    "title": "Red Gingham Mommy & Me Separates | Dress Like Mommy",
                    "description": "Mommy-and-me cotton-blend separates: choose the white lace-trim top or red gingham pants for mom + daughter. Sizes 2Y-8Y and Mom M.",
                },
            }
        },
    )
    require_no_user_errors(product_payload, ["data", "productUpdate"], "productUpdate")

    variant_mutation = """
    mutation UpdateVariants($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
      productVariantsBulkUpdate(productId: $productId, variants: $variants, allowPartialUpdates: false) {
        productVariants { id sku title price compareAtPrice selectedOptions { name value } }
        userErrors { field message }
      }
    }
    """
    variant_payload = gql(variant_mutation, {"productId": PRODUCT_ID, "variants": updates})
    require_no_user_errors(variant_payload, ["data", "productVariantsBulkUpdate"], "productVariantsBulkUpdate")
    write_csv_backup(body, tags)


def write_csv_backup(body: str, tags: List[str]) -> None:
    if CSV_OUT.exists():
        with CSV_OUT.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = list(reader)
        template = existing_rows[0] if existing_rows else {}
    else:
        header_source = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"
        with header_source.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            fieldnames = list(reader.fieldnames or [])
            template = {}

    rows: List[Dict[str, str]] = []
    for type_name in ("Top", "Pants"):
        for size_name, _role_token, _size_token, price, compare in SIZES:
            row = {field: template.get(field, "") for field in fieldnames}
            row.update(
                {
                    "Handle": HANDLE,
                    "Title": "Red Gingham Mommy and Me Separates - Top or Pants",
                    "Body (HTML)": body,
                    "Vendor": "dresslikemommy.com",
                    "Product Category": "Apparel & Accessories > Clothing > Outfit Sets",
                    "Type": "Matching Family Sets",
                    "Tags": ", ".join(tags),
                    "Published": "FALSE",
                    "Option1 Name": "Type",
                    "Option1 Value": type_name,
                    "Option2 Name": "Size",
                    "Option2 Value": size_name,
                    "Option3 Name": "",
                    "Option3 Value": "",
                    "Variant SKU": expected_sku(type_name, size_name),
                    "Variant Price": price,
                    "Variant Compare At Price": compare,
                    "Variant Inventory Policy": "deny",
                    "Variant Fulfillment Service": "manual",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                    "SEO Title": "Red Gingham Mommy & Me Separates | Dress Like Mommy",
                    "SEO Description": (
                        "Mommy-and-me cotton-blend separates: choose the white lace-trim top "
                        "or red gingham pants for mom + daughter. Sizes 2Y-8Y and Mom M."
                    ),
                    "Status": "draft",
                }
            )
            optional_updates = {
                "Style (product.metafields.custom.style)": "Lace Top & Gingham Pants",
                "Type (product.metafields.custom.type)": "Two-Piece Separates",
                "Google: Custom Label 3 (product.metafields.mm-google-shopping.custom_label_3)": "Lace Top & Gingham Pants",
                "Google: Custom Label 4 (product.metafields.mm-google-shopping.custom_label_4)": "Separate Top/Pants Picker",
                "Google Shopping / Google Product Category": "Apparel & Accessories > Clothing > Outfit Sets",
                "Google Shopping / MPN": expected_sku(type_name, size_name),
                "Google Shopping / Custom Product": "TRUE",
                "Google Shopping / Condition": "new",
                "Google Shopping / Gender": "female",
                "Google Shopping / Age Group": "adult",
                "Google Shopping / Custom Label 0": "Mommy and Me",
                "Google Shopping / Custom Label 1": "Red Gingham",
                "Google Shopping / Custom Label 2": "Summer",
                "Google Shopping / Custom Label 3": "Lace Top & Gingham Pants",
                "Google Shopping / Custom Label 4": "Separate Top/Pants Picker",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "true",
                "Size (product.metafields.shopify.size)": ", ".join(size for size, *_ in SIZES),
                "Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products)": "powder-blue-mommy-and-me-set, black-bow-mommy-and-me-set",
                "Related products (product.metafields.shopify--discovery--product_recommendation.related_products)": "powder-blue-mommy-and-me-set, black-bow-mommy-and-me-set",
                "Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display)": "only manual",
                "Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries)": "red gingham mommy and me, mommy and me pants, mommy and me top",
            }
            for key, value in optional_updates.items():
                if key in row:
                    row[key] = value
            rows.append(row)

    with CSV_OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def ensure_publications() -> None:
    mutation = """
    mutation Publish($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) {
        publishable { availablePublicationsCount { count } }
        userErrors { field message }
      }
    }
    """
    payload = gql(
        mutation,
        {"id": PRODUCT_ID, "input": [{"publicationId": publication_id} for publication_id in PUBLICATIONS]},
    )
    require_no_user_errors(payload, ["data", "publishablePublish"], "publishablePublish")


def verify() -> Dict[str, Any]:
    product = fetch_product()
    VERIFY_OUT.write_text(json.dumps({"data": {"product": product}}, indent=2), encoding="utf-8")
    names = option_names(product)
    variants = product["variants"]["nodes"]
    pairs = {
        tuple((option["name"], option["value"]) for option in variant["selectedOptions"])
        for variant in variants
    }
    expected_pairs = {
        (("Type", type_name), ("Size", label))
        for type_name in ("Top", "Pants")
        for label, *_rest in SIZES
    }
    skus = {variant["sku"] for variant in variants}
    expected_skus = {expected_sku(type_name, label) for type_name in ("Top", "Pants") for label, *_ in SIZES}
    checks = {
        "option_axes_are_type_size": names == ["Type", "Size"],
        "variant_count_is_14": len(variants) == 14,
        "all_type_size_pairs_exist": pairs == expected_pairs,
        "sku_set_matches_spec": skus == expected_skus,
        "product_is_draft": product["status"] == "DRAFT",
        "published_at_is_null": product["publishedAt"] is None,
        "no_required_publications_live": not set(PUBLICATIONS).intersection(
            {
                node["publication"]["id"]
                for node in product["resourcePublicationsV2"]["nodes"]
                if node["isPublished"]
            }
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(json.dumps(checks, indent=2))
    return checks


def append_worklog(checks: Dict[str, Any]) -> None:
    worklog_path = ROOT / "ops/AGENT_WORKLOG.md"
    current_worklog = worklog_path.read_text(encoding="utf-8")
    if "AGENT_CONTINUITY_ANCHOR: 2026-04-25-red-gingham-type-size-repair" in current_worklog:
        return
    entry = f"""

2026-04-25 — Repaired Red Gingham Mommy and Me variant model
AGENT_CONTINUITY_ANCHOR: 2026-04-25-red-gingham-type-size-repair

Why:
- Product `7537366597729` was live with only `Size x Color` options even though 1688 offer `1041874678820` sells separate item choices: `白色上衣` (white top) and `红色格子裤` (red gingham pants).

What changed:
- Added a `Type` option with `Top` and `Pants`.
- Removed the single-value `Color` option.
- Rebuilt variants as `Type x Size`: 14 variants total.
- Updated SKUs to include item tokens: `TOP` or `PNT`.
- Updated title, body copy, SEO description, and tags so the product is presented as separable top/pants choices.
- Added reusable preflight validator `ops/scripts/validate_listing_variant_model.py` to prevent future runners from collapsing vendor item choices into one set.

Verification:
- Repair script checks: `{json.dumps(checks, sort_keys=True)}`.
- Product is `DRAFT`; `publishedAt` is null; required sales-channel publications are not live.

Residual risks:
- Existing orders/cart references using old 7 SKUs may need manual awareness if any customer already selected the old variants before the repair.
"""
    worklog_path.write_text(current_worklog + entry, encoding="utf-8")


def main() -> None:
    ensure_type_option()
    delete_color_option_if_present()
    reorder_options()
    update_product_and_variants()
    checks = verify()
    append_worklog(checks)
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
