#!/usr/bin/env python3
"""Correct the shopper-facing child 170 label for the nine 2026-08-31 shirts.

The vendor size code and existing SKU stay unchanged. This script deliberately
does not send variant, price, cost, media, status, publication, inventory, or
taxonomy mutations. It renames the existing option value, corrects only the
affected English body/SEO/tag fields, and proves all unrelated live state stayed
the same before writing verification artifacts.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]
API_VERSION = "2025-01"
STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
API = f"https://{STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

OLD_LABEL = "Child 170"
NEW_LABEL = "Child 14 Years"
REPORT_PATH = ROOT / "ops/listings/nine-family-shirt-child-170-correction.json"

PRODUCTS = [
    ("sunlit-tropical-bloom-family-matching-tops", "7670674391137", "create-stbl-sunlit-tropical-bloom-family-matching-tops.sh"),
    ("blue-monstera-citrus-family-matching-tops", "7670683762785", "create-bmct-blue-monstera-citrus-family-matching-tops.sh"),
    ("midnight-palm-blossom-family-matching-tops", "7670695526497", "create-mpbl-midnight-palm-blossom-family-matching-tops.sh"),
    ("monochrome-palm-family-matching-tops", "7670724329569", "create-mnpl-monochrome-palm-family-matching-tops.sh"),
    ("coastal-banana-leaf-family-matching-tops", "7670738223201", "create-cblf-coastal-banana-leaf-family-matching-tops.sh"),
    ("sky-daisy-doodle-family-matching-tops", "7670742777953", "create-sdsy-sky-daisy-doodle-family-matching-tops.sh"),
    ("midnight-paint-splash-family-matching-tops", "7670743498849", "create-mpsh-midnight-paint-splash-family-matching-tops.sh"),
    ("bright-paint-splash-family-matching-tops", "7670744842337", "create-bpsh-bright-paint-splash-family-matching-tops.sh"),
    ("playful-cat-parade-family-matching-tops", "7670746775649", "create-pcat-playful-cat-parade-family-matching-tops.sh"),
]

PRODUCT_QUERY = """
query ProductForChildSizeCorrection($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    title
    vendor
    productType
    status
    publishedAt
    onlineStoreUrl
    descriptionHtml
    tags
    seo { title description }
    category { id fullName }
    options {
      id
      name
      values
      optionValues { id name hasVariants }
    }
    variants(first: 100) {
      nodes {
        id
        title
        sku
        price
        compareAtPrice
        taxable
        inventoryPolicy
        inventoryQuantity
        selectedOptions { name value }
        inventoryItem {
          id
          tracked
          requiresShipping
          unitCost { amount currencyCode }
        }
      }
    }
    media(first: 50) {
      nodes {
        id
        status
        alt
        ... on MediaImage { image { url } }
      }
    }
    metafields(first: 120) { nodes { id namespace key type value } }
    resourcePublicationsV2(first: 50) {
      nodes { isPublished publishDate publication { id name } }
    }
  }
}
"""

RENAME_OPTION_VALUE_MUTATION = """
mutation RenameProductOptionValue(
  $productId: ID!
  $option: OptionUpdateInput!
  $optionValuesToUpdate: [OptionValueUpdateInput!]!
) {
  productOptionUpdate(
    productId: $productId
    option: $option
    optionValuesToUpdate: $optionValuesToUpdate
  ) {
    product { id }
    userErrors { field message code }
  }
}
"""

UPDATE_PRODUCT_COPY_MUTATION = """
mutation UpdateCorrectedChildSizeCopy($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id }
    userErrors { field message }
  }
}
"""


def gql(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        API,
        data=payload,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", errors="replace")) from exc
    if result.get("errors"):
        raise RuntimeError(json.dumps(result["errors"], indent=2, ensure_ascii=False))
    return result["data"]


def require_no_user_errors(payload: Dict[str, Any], mutation_name: str) -> None:
    errors = payload[mutation_name].get("userErrors") or []
    if errors:
        raise RuntimeError(json.dumps(errors, indent=2, ensure_ascii=False))


def fetch_product(handle: str) -> Dict[str, Any]:
    product = gql(PRODUCT_QUERY, {"handle": handle}).get("productByHandle")
    if not product:
        raise RuntimeError(f"Missing Shopify product for handle {handle}")
    return product


def corrected_body(body: str) -> str:
    value = body.replace(OLD_LABEL, NEW_LABEL)
    value = re.sub(
        r"(<td>\s*Child 14 Years\s*</td>\s*<td>)(?:—|&mdash;|-)(</td>)",
        r"\g<1>14\2",
        value,
    )
    return value


def corrected_seo(description: str) -> str:
    value = description or ""
    replacements = {
        "Child 4 Years-170": "Child 4–14 Years",
        "Child 4 Years–170": "Child 4–14 Years",
        "Child 4Y-170": "Child 4–14 Years",
        "Child 4Y–170": "Child 4–14 Years",
        OLD_LABEL: NEW_LABEL,
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def normalized_label(value: str) -> str:
    return "__CORRECTED_CHILD_SIZE__" if value in {OLD_LABEL, NEW_LABEL} else value


def invariant_fingerprint(product: Dict[str, Any]) -> Dict[str, Any]:
    variants = []
    for variant in sorted(product["variants"]["nodes"], key=lambda item: item["id"]):
        variants.append(
            {
                "id": variant["id"],
                "sku": variant.get("sku"),
                "price": variant.get("price"),
                "compareAtPrice": variant.get("compareAtPrice"),
                "taxable": variant.get("taxable"),
                "inventoryPolicy": variant.get("inventoryPolicy"),
                "inventoryQuantity": variant.get("inventoryQuantity"),
                "selectedOptions": [
                    {"name": option["name"], "value": normalized_label(option["value"])}
                    for option in variant.get("selectedOptions") or []
                ],
                "inventoryItem": variant.get("inventoryItem"),
            }
        )
    options = []
    for option in product["options"]:
        options.append(
            {
                "id": option["id"],
                "name": option["name"],
                "values": [normalized_label(value) for value in option.get("values") or []],
                "optionValues": [
                    {
                        "id": value["id"],
                        "name": normalized_label(value["name"]),
                        "hasVariants": value["hasVariants"],
                    }
                    for value in option.get("optionValues") or []
                ],
            }
        )
    publications = sorted(
        (
            item["isPublished"],
            item.get("publishDate"),
            item["publication"]["id"],
            item["publication"]["name"],
        )
        for item in product["resourcePublicationsV2"]["nodes"]
    )
    media = sorted(
        (
            {
                "id": item["id"],
                "status": item.get("status"),
                "alt": item.get("alt"),
            }
            for item in product["media"]["nodes"]
        ),
        key=lambda item: item["id"],
    )
    metafields = sorted(
        (
            {
                "id": item["id"],
                "namespace": item["namespace"],
                "key": item["key"],
                "type": item["type"],
                "value": item["value"],
            }
            for item in product["metafields"]["nodes"]
            if not (item["namespace"] == "global" and item["key"] == "description_tag")
        ),
        key=lambda item: (item["namespace"], item["key"], item["id"]),
    )
    return {
        "id": product["id"],
        "handle": product["handle"],
        "title": product["title"],
        "vendor": product["vendor"],
        "productType": product["productType"],
        "status": product["status"],
        "publishedAt": product.get("publishedAt"),
        "onlineStoreUrl": product.get("onlineStoreUrl"),
        "seoTitle": product.get("seo", {}).get("title"),
        "category": product.get("category"),
        "tagsExceptCorrectedSize": sorted(
            tag for tag in product.get("tags") or [] if tag not in {OLD_LABEL, NEW_LABEL}
        ),
        "options": options,
        "variants": variants,
        "media": media,
        "metafieldsExceptSeoDescription": metafields,
        "publications": publications,
    }


def find_size_option(product: Dict[str, Any]) -> Dict[str, Any]:
    matches = [option for option in product["options"] if option["name"] == "Size"]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Size option for {product['handle']}; found {len(matches)}")
    return matches[0]


def validate_local_sources() -> None:
    errors: List[str] = []
    for handle, _product_id, runner_name in PRODUCTS:
        paths = [
            ROOT / "ops/scripts" / runner_name,
            ROOT / "ops/listings" / f"{handle}-listing.md",
            ROOT / "ops/listings" / f"{handle}-shopify-import.csv",
            ROOT / "ops/listings" / f"body-{handle}.html",
            ROOT / "ops/listings" / f"size-chart-{handle}.json",
        ]
        for path in paths:
            if not path.is_file():
                errors.append(f"missing local source: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            if OLD_LABEL in text:
                errors.append(f"legacy label remains in {path}")
            if NEW_LABEL not in text:
                errors.append(f"corrected label missing from {path}")
        chart_path = ROOT / "ops/listings" / f"size-chart-{handle}.json"
        if chart_path.is_file():
            rows = json.loads(chart_path.read_text(encoding="utf-8"))
            target = [
                row
                for row in rows
                if row.get("audience") == "child" and row.get("vendor_label") == "170"
            ]
            if len(target) != 1 or (
                target[0].get("picker_label"),
                target[0].get("age"),
                target[0].get("sku_suffix"),
                target[0].get("height"),
                target[0].get("weight"),
            ) != (NEW_LABEL, "14", "KID170", "150-155 cm", "35-42.5 kg"):
                errors.append(f"incorrect local 170 row in {chart_path}")
    if errors:
        raise RuntimeError("LOCAL PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def summary(product: Dict[str, Any]) -> Dict[str, Any]:
    size_option = find_size_option(product)
    target_variants = [
        variant
        for variant in product["variants"]["nodes"]
        if "KID170" in (variant.get("sku") or "")
    ]
    return {
        "id": product["id"],
        "handle": product["handle"],
        "status": product["status"],
        "publishedAt": product.get("publishedAt"),
        "onlineStoreUrl": product.get("onlineStoreUrl"),
        "livePublications": sorted(
            item["publication"]["name"]
            for item in product["resourcePublicationsV2"]["nodes"]
            if item["isPublished"]
        ),
        "variantCount": len(product["variants"]["nodes"]),
        "sizeOptionId": size_option["id"],
        "correctedOptionValues": [
            item for item in size_option["optionValues"] if item["name"] == NEW_LABEL
        ],
        "legacyOptionValues": [
            item for item in size_option["optionValues"] if item["name"] == OLD_LABEL
        ],
        "targetVariants": [
            {
                "id": item["id"],
                "sku": item["sku"],
                "price": item["price"],
                "compareAtPrice": item.get("compareAtPrice"),
                "cost": ((item.get("inventoryItem") or {}).get("unitCost") or {}).get("amount"),
                "selectedOptions": item["selectedOptions"],
            }
            for item in target_variants
        ],
        "mediaIds": sorted(item["id"] for item in product["media"]["nodes"]),
        "bodyLegacyCount": product["descriptionHtml"].count(OLD_LABEL),
        "bodyCorrectedCount": product["descriptionHtml"].count(NEW_LABEL),
        "seoDescription": product["seo"].get("description"),
        "legacyTags": [tag for tag in product["tags"] if tag == OLD_LABEL],
        "correctedTags": [tag for tag in product["tags"] if tag == NEW_LABEL],
    }


def correct_one(handle: str, expected_legacy_id: str) -> Dict[str, Any]:
    before = fetch_product(handle)
    if before["id"] != f"gid://shopify/Product/{expected_legacy_id}":
        raise RuntimeError(f"Unexpected product ID for {handle}: {before['id']}")
    if len(before["variants"]["nodes"]) != 14:
        raise RuntimeError(f"Unexpected variant count for {handle}")
    target_variants = [
        variant
        for variant in before["variants"]["nodes"]
        if "KID170" in (variant.get("sku") or "")
    ]
    if len(target_variants) != 1:
        raise RuntimeError(f"Expected one preserved KID170 variant for {handle}")

    size_option = find_size_option(before)
    old_values = [value for value in size_option["optionValues"] if value["name"] == OLD_LABEL]
    new_values = [value for value in size_option["optionValues"] if value["name"] == NEW_LABEL]
    if len(old_values) + len(new_values) != 1:
        raise RuntimeError(f"Unexpected old/new option-value state for {handle}")

    before_fingerprint = invariant_fingerprint(before)
    body = corrected_body(before["descriptionHtml"])
    seo_description = corrected_seo(before["seo"].get("description") or "")
    tags = [NEW_LABEL if tag == OLD_LABEL else tag for tag in before["tags"]]

    actions: List[str] = []
    if old_values:
        mutation = gql(
            RENAME_OPTION_VALUE_MUTATION,
            {
                "productId": before["id"],
                "option": {"id": size_option["id"]},
                "optionValuesToUpdate": [{"id": old_values[0]["id"], "name": NEW_LABEL}],
            },
        )
        require_no_user_errors(mutation, "productOptionUpdate")
        actions.append("renamed_option_value")

    if (
        body != before["descriptionHtml"]
        or seo_description != (before["seo"].get("description") or "")
        or tags != before["tags"]
    ):
        mutation = gql(
            UPDATE_PRODUCT_COPY_MUTATION,
            {
                "product": {
                    "id": before["id"],
                    "descriptionHtml": body,
                    "tags": tags,
                    "seo": {
                        "title": before["seo"].get("title"),
                        "description": seo_description,
                    },
                }
            },
        )
        require_no_user_errors(mutation, "productUpdate")
        actions.append("corrected_body_seo_tags")

    after = fetch_product(handle)
    if invariant_fingerprint(after) != before_fingerprint:
        raise RuntimeError(f"Unrelated live state changed while correcting {handle}")
    after_size = find_size_option(after)
    if any(value["name"] == OLD_LABEL for value in after_size["optionValues"]):
        raise RuntimeError(f"Legacy option value remains for {handle}")
    if len([value for value in after_size["optionValues"] if value["name"] == NEW_LABEL]) != 1:
        raise RuntimeError(f"Corrected option value missing or duplicated for {handle}")
    if after["descriptionHtml"] != body or OLD_LABEL in after["descriptionHtml"]:
        raise RuntimeError(f"Corrected body did not persist for {handle}")
    if not re.search(r"<td>\s*Child 14 Years\s*</td>\s*<td>14</td>", after["descriptionHtml"]):
        raise RuntimeError(f"Corrected age cell did not persist for {handle}")
    if after["seo"].get("description") != seo_description or "170" in re.sub(
        r"(?:1[5-9]\d|2\d\d)(?:-|–)(?:1[5-9]\d|2\d\d)",
        "",
        after["seo"].get("description") or "",
    ):
        raise RuntimeError(f"Legacy child SEO range remains for {handle}")
    if OLD_LABEL in after["tags"] or NEW_LABEL not in after["tags"]:
        raise RuntimeError(f"Corrected size tag did not persist for {handle}")
    global_description = next(
        (
            item["value"]
            for item in after["metafields"]["nodes"]
            if item["namespace"] == "global" and item["key"] == "description_tag"
        ),
        None,
    )
    if global_description != seo_description:
        raise RuntimeError(f"SEO description metafield did not persist for {handle}")

    verify_path = ROOT / "ops/listings" / f"verify-{handle}.json"
    verify_path.write_text(
        json.dumps({"data": {"product": after}}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "handle": handle,
        "actions": actions or ["already_corrected"],
        "before": summary(before),
        "after": summary(after),
        "invariantsPreserved": True,
        "verificationPath": str(verify_path),
    }


def main() -> int:
    if not TOKEN:
        print("SHOPIFY_ADMIN_ACCESS_TOKEN is not set", file=sys.stderr)
        return 2
    validate_local_sources()
    results = []
    for handle, product_id, _runner in PRODUCTS:
        result = correct_one(handle, product_id)
        results.append(result)
        print(
            json.dumps(
                {
                    "handle": handle,
                    "actions": result["actions"],
                    "status": result["after"]["status"],
                    "correctedOptionValues": len(result["after"]["correctedOptionValues"]),
                    "bodyLegacyCount": result["after"]["bodyLegacyCount"],
                    "invariantsPreserved": result["invariantsPreserved"],
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    report = {
        "problemId": "PROB-2026-09-02-FAMILY-SHIRT-CHILD-170-LABEL",
        "oldLabel": OLD_LABEL,
        "newLabel": NEW_LABEL,
        "vendorSizeCode": "170",
        "recommendedHeight": "150-155 cm",
        "recommendedWeight": "35-42.5 kg",
        "status": "live_product_correction_verified_localization_pending",
        "productCount": len(results),
        "results": results,
        "scopeNote": (
            "Variant prices, costs, SKUs, media, inventory, taxonomy, status, and publications "
            "were preserved exactly; localization closeouts run separately after this mutation."
        ),
    }
    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
