#!/usr/bin/env python3
"""Build Phase 3C feed-engineering pilot artifacts from live Shopify data."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain


API_VERSION = "2026-01"
TARGET_PILOT_ROWS = 100
PRODUCT_PAGE_SIZE = 50
VARIANT_PAGE_SIZE = 100
CANONICAL_BRAND = "Dress Like Mommy"
MERCHANT_CENTER_FEED_LABEL = "US"
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-27-phase-3c-pilot")

PRODUCTS_QUERY = """
query Products($first: Int!, $after: String) {
  products(first: $first, after: $after, sortKey: ID) {
    edges {
      node {
        id
        legacyResourceId
        handle
        title
        vendor
        status
        productType
        tags
        descriptionHtml
        onlineStoreUrl
        options {
          name
          values
        }
        resourcePublications(first: 20) {
          edges {
            node {
              isPublished
              publication {
                id
                name
              }
            }
          }
        }
        variants(first: 100) {
          pageInfo {
            hasNextPage
            endCursor
          }
          edges {
            node {
              id
              legacyResourceId
              title
              sku
              price
              inventoryPolicy
              inventoryQuantity
              availableForSale
              selectedOptions {
                name
                value
              }
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

MORE_VARIANTS_QUERY = """
query ProductVariants($id: ID!, $first: Int!, $after: String) {
  product(id: $id) {
    variants(first: $first, after: $after) {
      pageInfo {
        hasNextPage
        endCursor
      }
      edges {
        node {
          id
          legacyResourceId
          title
          sku
          price
          inventoryPolicy
          inventoryQuantity
          availableForSale
          selectedOptions {
            name
            value
          }
        }
      }
    }
  }
}
"""

COLOR_MAP = {
    "black": "Black",
    "white": "White",
    "blue": "Blue",
    "navy": "Blue",
    "royal blue": "Blue",
    "light blue": "Blue",
    "sky blue": "Blue",
    "pink": "Pink",
    "red": "Red",
    "green": "Green",
    "lime green": "Green",
    "yellow": "Yellow",
    "orange": "Orange",
    "purple": "Purple",
    "brown": "Brown",
    "beige": "Beige",
    "khaki": "Khaki",
    "gray": "Gray",
    "grey": "Gray",
    "silver": "Silver",
    "gold": "Gold",
    "floral": "Floral",
    "multicolor": "Multicolor",
    "multi color": "Multicolor",
    "multi-color": "Multicolor",
    "rainbow color": "Multicolor",
    "photo color": "Multicolor",
    "checkerboard": "Checkerboard",
    "checkered": "Checkered",
    "plaid": "Plaid",
    "striped": "Striped",
    "stripes": "Striped",
    "paisley": "Paisley",
    "tie-dye": "Tie-Dye",
    "tie dye": "Tie-Dye",
    "polka dot": "Polka Dot",
    "leopard": "Leopard",
    "camouflage": "Camouflage",
    "camo": "Camouflage",
    "champagne": "Champagne",
}

HOUSE_BRAND_KEYWORDS = {
    "matching",
    "mommy",
    "mother",
    "daughter",
    "family",
    "daddy",
    "father",
    "son",
    "couple",
    "maternity",
    "mom and me",
    "dad and me",
}

FEMALE_TOKENS = {
    "mom",
    "mommy",
    "mother",
    "women",
    "woman",
    "female",
    "lady",
    "ladies",
    "wife",
    "queen",
    "daughter",
    "girl",
    "girls",
    "princess",
    "maternity",
    "bride",
}

MALE_TOKENS = {
    "dad",
    "daddy",
    "father",
    "men",
    "man",
    "male",
    "husband",
    "king",
    "son",
    "boy",
    "boys",
    "groom",
}

ROLE_LIKE_VALUES = {
    "mom",
    "mommy",
    "mother",
    "dad",
    "daddy",
    "father",
    "girl",
    "girls",
    "boy",
    "boys",
    "women",
    "men",
    "adult",
    "child",
    "children",
    "kid",
    "kids",
    "family",
    "parent",
}

STYLE_LIKE_VALUES = {
    "pullover",
    "cardigan",
    "set",
    "default title",
}

GENERIC_BRAND_VALUES = {
    "",
    "n/a",
    "na",
    "brand new",
    "new design",
    "new comfortable feel",
    "new exclusive design",
    "new sense of fashionablity and class",
}


@dataclass
class VariantRecord:
    variant_id: str
    variant_gid: str
    title: str
    sku: str
    price: str
    inventory_policy: str
    inventory_quantity: int | None
    available_for_sale: bool
    selected_options: list[dict[str, str]]


@dataclass
class ProductRecord:
    product_id: str
    product_gid: str
    handle: str
    title: str
    vendor: str
    status: str
    product_type: str
    tags: list[str]
    description_html: str
    online_store_url: str
    options: list[dict[str, Any]]
    publications: list[str]
    variants: list[VariantRecord]
    vendor_kind: str = ""
    google_published: bool = False
    house_brand_confident: bool = False
    needs_brand_cleanup: bool = False
    brand_signals: list[str] | None = None


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.store_domain = store_domain
        self.access_token = access_token
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(6):
            req = request.Request(self.endpoint, data=payload, headers=headers)
            try:
                with request.urlopen(req, timeout=120) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 5:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {body}") from exc

            if body.get("errors"):
                raise RuntimeError(f"Shopify GraphQL errors: {body['errors']}")
            return body["data"]
        raise RuntimeError("Shopify GraphQL request failed after retries.")


def plain_text(raw_html: str) -> str:
    stripped = re.sub(r"<[^>]+>", " ", raw_html or "")
    return html.unescape(re.sub(r"\s+", " ", stripped)).strip()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def normalize_text(value: str) -> str:
    return normalize_space(value).lower()


def vendor_kind(vendor: str) -> str:
    clean_vendor = normalize_space(vendor)
    if clean_vendor == CANONICAL_BRAND:
        return "canonical"
    if clean_vendor == "dresslikemommy.com":
        return "domain_variant"
    if re.search(r"https?://", clean_vendor, re.IGNORECASE):
        return "url"
    return "other"


def extract_brand_signals(product: ProductRecord) -> list[str]:
    text = plain_text(product.description_html)
    if not text:
        return []
    matches = re.findall(
        r"Brand(?:\s+Name)?\s*:\s*([A-Za-z0-9][A-Za-z0-9 &+/\-]{0,60})",
        text,
        flags=re.IGNORECASE,
    )
    signals: list[str] = []
    for match in matches:
        cleaned = re.split(r"\b(?:Gender|Size|Material|Item Type|Type|Pattern|Support Type|Fit)\b", match)[0]
        cleaned = normalize_space(cleaned.strip(" .,:;|-"))
        lowered = cleaned.lower()
        if not cleaned or lowered in GENERIC_BRAND_VALUES:
            continue
        if lowered.startswith("new "):
            continue
        signals.append(cleaned)
    return signals


def has_house_brand_context(product: ProductRecord) -> bool:
    haystacks = [
        normalize_text(product.title),
        normalize_text(product.handle.replace("-", " ")),
        normalize_text(" ".join(product.tags)),
    ]
    if "| dlm" in haystacks[0]:
        return True
    for haystack in haystacks:
        for keyword in HOUSE_BRAND_KEYWORDS:
            if keyword in haystack:
                return True
    return False


def build_product_record(node: dict[str, Any]) -> ProductRecord:
    publications = [
        edge["node"]["publication"]["name"]
        for edge in node["resourcePublications"]["edges"]
        if edge["node"]["isPublished"]
    ]
    variants = [
        VariantRecord(
            variant_id=edge["node"]["legacyResourceId"],
            variant_gid=edge["node"]["id"],
            title=edge["node"]["title"],
            sku=edge["node"].get("sku") or "",
            price=edge["node"].get("price") or "",
            inventory_policy=edge["node"].get("inventoryPolicy") or "",
            inventory_quantity=edge["node"].get("inventoryQuantity"),
            available_for_sale=bool(edge["node"].get("availableForSale")),
            selected_options=edge["node"].get("selectedOptions") or [],
        )
        for edge in node["variants"]["edges"]
    ]
    product = ProductRecord(
        product_id=node["legacyResourceId"],
        product_gid=node["id"],
        handle=node["handle"],
        title=node["title"],
        vendor=normalize_space(node["vendor"]),
        status=node["status"],
        product_type=normalize_space(node.get("productType") or ""),
        tags=node.get("tags") or [],
        description_html=node.get("descriptionHtml") or "",
        online_store_url=node.get("onlineStoreUrl") or "",
        options=node.get("options") or [],
        publications=publications,
        variants=variants,
    )
    product.vendor_kind = vendor_kind(product.vendor)
    product.google_published = "Google & YouTube" in publications
    product.brand_signals = extract_brand_signals(product)
    product.house_brand_confident = (
        product.vendor_kind in {"canonical", "domain_variant"}
        or (
            product.vendor_kind == "url"
            and not product.brand_signals
            and has_house_brand_context(product)
        )
    )
    product.needs_brand_cleanup = product.vendor_kind in {"domain_variant", "url"} and product.house_brand_confident
    return product


def fetch_product_variants(client: ShopifyClient, product_gid: str, after: str) -> list[VariantRecord]:
    variants: list[VariantRecord] = []
    cursor = after
    while cursor:
        data = client.graphql(
            MORE_VARIANTS_QUERY,
            {"id": product_gid, "first": VARIANT_PAGE_SIZE, "after": cursor},
        )
        connection = data["product"]["variants"]
        variants.extend(
            VariantRecord(
                variant_id=edge["node"]["legacyResourceId"],
                variant_gid=edge["node"]["id"],
                title=edge["node"]["title"],
                sku=edge["node"].get("sku") or "",
                price=edge["node"].get("price") or "",
                inventory_policy=edge["node"].get("inventoryPolicy") or "",
                inventory_quantity=edge["node"].get("inventoryQuantity"),
                available_for_sale=bool(edge["node"].get("availableForSale")),
                selected_options=edge["node"].get("selectedOptions") or [],
            )
            for edge in connection["edges"]
        )
        if not connection["pageInfo"]["hasNextPage"]:
            break
        cursor = connection["pageInfo"]["endCursor"]
    return variants


def fetch_products(client: ShopifyClient) -> list[ProductRecord]:
    products: list[ProductRecord] = []
    after: str | None = None
    while True:
        data = client.graphql(PRODUCTS_QUERY, {"first": PRODUCT_PAGE_SIZE, "after": after})
        connection = data["products"]
        for edge in connection["edges"]:
            node = edge["node"]
            product = build_product_record(node)
            variant_page = node["variants"]["pageInfo"]
            if variant_page["hasNextPage"]:
                product.variants.extend(fetch_product_variants(client, product.product_gid, variant_page["endCursor"]))
            products.append(product)
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]
    return products


def single_color_match(values: list[str]) -> str | None:
    matches: list[str] = []
    for value in values:
        text = normalize_text(value)
        for key, normalized in COLOR_MAP.items():
            if re.search(rf"(?<![a-z]){re.escape(key)}(?![a-z])", text):
                matches.append(normalized)
    distinct = sorted(set(matches))
    if len(distinct) == 1:
        return distinct[0]
    return None


def looks_like_alpha_size(value: str) -> bool:
    return bool(re.fullmatch(r"(xxs|xs|s|m|l|xl|xxl|xxxl|2xl|3xl|4xl|5xl)", normalize_text(value)))


def looks_like_numeric_size(value: str) -> bool:
    text = normalize_text(value)
    if re.search(r"\b(\d{1,2})\s*(?:m|mo|month|months|t|y|yr|yrs|year|years)\b", text):
        return True
    if re.search(r"\b(\d{1,2})\s*-\s*(\d{1,2})\s*(?:m|mo|month|months|t|y|yr|yrs|year|years)?\b", text):
        return True
    if re.search(r"\b(1[0-6]0)\b", text):
        return True
    return False


def looks_like_size_value(value: str) -> bool:
    text = normalize_text(value)
    if not text or text in STYLE_LIKE_VALUES:
        return False
    if looks_like_alpha_size(text) or looks_like_numeric_size(text):
        return True
    size_tokens = {
        "mother",
        "father",
        "mom",
        "dad",
        "mommy",
        "daddy",
        "woman",
        "women",
        "man",
        "men",
        "adult",
        "baby",
        "child",
        "children",
        "kid",
        "kids",
        "girl",
        "girls",
        "boy",
        "boys",
        "infant",
        "toddler",
    }
    return any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", text) for token in size_tokens)


def looks_like_color_value(value: str) -> bool:
    text = normalize_text(value)
    if not text or text in ROLE_LIKE_VALUES or text in STYLE_LIKE_VALUES:
        return False
    return single_color_match([value]) is not None


def extract_size_value(product: ProductRecord, variant: VariantRecord) -> tuple[str, bool]:
    for option in variant.selected_options:
        option_name = normalize_text(option["name"])
        if "size" in option_name or "age" in option_name:
            return normalize_space(option["value"]), True
    if len(product.variants) == 1 and variant.title == "Default Title":
        return "", False
    if variant.title and variant.title != "Default Title":
        segments = [normalize_space(segment) for segment in variant.title.split("/") if normalize_space(segment)]
        if len(segments) >= 2:
            size_like_segments = [segment for segment in segments if looks_like_size_value(segment)]
            if len(size_like_segments) == 1:
                return size_like_segments[0], True
            first_segment, second_segment = segments[0], segments[1]
            if looks_like_color_value(first_segment) and looks_like_size_value(second_segment):
                return second_segment, True
        first_segment = segments[0] if segments else ""
        return first_segment, True
    return "", False


def variant_context_text(product: ProductRecord, variant: VariantRecord) -> str:
    parts = [
        product.title,
        product.handle.replace("-", " "),
        " ".join(product.tags),
        variant.title,
        variant.sku,
    ]
    for option in variant.selected_options:
        parts.append(option["name"])
        parts.append(option["value"])
    return normalize_text(" ".join(parts))


def infer_gender(product: ProductRecord, variant: VariantRecord) -> str | None:
    variant_text = normalize_text(" ".join([variant.title, variant.sku, *[v["value"] for v in variant.selected_options]]))
    product_text = variant_context_text(product, variant)

    female_variant = any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", variant_text) for token in FEMALE_TOKENS)
    male_variant = any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", variant_text) for token in MALE_TOKENS)
    if female_variant and not male_variant:
        return "female"
    if male_variant and not female_variant:
        return "male"

    female_product = any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", product_text) for token in FEMALE_TOKENS)
    male_product = any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", product_text) for token in MALE_TOKENS)
    if female_product and not male_product:
        return "female"
    if male_product and not female_product:
        return "male"
    return None


def infer_age_group(product: ProductRecord, variant: VariantRecord, size_value: str) -> str | None:
    size_only = normalize_text(size_value)
    option_values = normalize_text(" ".join(v["value"] for v in variant.selected_options))
    variant_only = normalize_text(" ".join([size_value, variant.title, variant.sku, option_values]))
    product_only = normalize_text(" ".join([product.title, product.handle.replace("-", " "), " ".join(product.tags)]))

    if re.search(r"\b(newborn|nb)\b", variant_only):
        return "newborn"

    adult_tokens = (
        "mother",
        "mom",
        "mommy",
        "father",
        "dad",
        "daddy",
        "women",
        "woman",
        "men",
        "man",
        "adult",
        "maternity",
        "wife",
        "husband",
        "queen",
        "king",
    )

    if any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", size_only) for token in adult_tokens):
        return "adult"

    month_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:m|mo|month|months)\b", size_only)]
    if month_matches:
        return "infant" if max(month_matches) <= 12 else "toddler"

    year_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:y|yr|yrs|year|years)\b", size_only)]
    t_matches = [int(match) for match in re.findall(r"\b(\d{1,2})t\b", size_only)]
    range_matches = [
        max(int(start), int(end))
        for start, end in re.findall(r"\b(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)?\b", size_only)
    ]
    numeric_child_sizes = [int(match) for match in re.findall(r"\b(1[0-6]0)\b", size_only)]
    if year_matches or t_matches or range_matches:
        max_age = max(year_matches + t_matches + range_matches)
        return "toddler" if max_age <= 5 else "kids"
    if numeric_child_sizes:
        return "kids"
    if re.search(r"\b(baby|infant)\b", size_only):
        return "infant"
    if re.search(r"\b(toddler)\b", size_only):
        return "toddler"
    if re.search(r"\b(child|kid|kids|girl|girls|boy|boys)\b", size_only):
        return "kids"

    month_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:m|mo|month|months)\b", variant_only)]
    if month_matches:
        return "infant" if max(month_matches) <= 12 else "toddler"

    year_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:y|yr|yrs|year|years)\b", variant_only)]
    t_matches = [int(match) for match in re.findall(r"\b(\d{1,2})t\b", variant_only)]
    range_matches = [
        max(int(start), int(end))
        for start, end in re.findall(r"\b(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)?\b", variant_only)
    ]
    numeric_child_sizes = [int(match) for match in re.findall(r"\b(1[0-6]0)\b", variant_only)]
    if year_matches or t_matches or range_matches:
        max_age = max(year_matches + t_matches + range_matches)
        return "toddler" if max_age <= 5 else "kids"
    if numeric_child_sizes:
        return "kids"

    if re.search(r"\b(baby|infant)\b", variant_only):
        return "infant"
    if re.search(r"\b(toddler)\b", variant_only):
        return "toddler"
    if re.search(r"\b(child|kid|kids|girl|girls|boy|boys)\b", variant_only):
        return "kids"
    if any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", variant_only) for token in adult_tokens):
        return "adult"
    if any(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", product_only) for token in adult_tokens):
        return "adult"
    return None


def infer_color(product: ProductRecord, variant: VariantRecord) -> str | None:
    option_candidates: list[str] = []
    for option in variant.selected_options:
        option_name = normalize_text(option["name"])
        option_value = normalize_space(option["value"])
        if "color" in option_name or "colour" in option_name:
            lowered = normalize_text(option_value)
            if lowered in ROLE_LIKE_VALUES:
                continue
            option_candidates.append(option_value)
    if option_candidates:
        matched = single_color_match(option_candidates)
        if matched:
            return matched

    product_option_colors: list[str] = []
    for option in product.options:
        option_name = normalize_text(option["name"])
        if "color" in option_name or "colour" in option_name:
            product_option_colors.extend(
                value for value in option.get("values", []) if normalize_text(value) not in ROLE_LIKE_VALUES
            )
    matched = single_color_match(product_option_colors)
    if matched:
        return matched

    matched = single_color_match(product.tags)
    if matched:
        return matched

    matched = single_color_match([product.title])
    if matched:
        return matched
    return None


def build_catalog_rows(products: list[ProductRecord]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for product in products:
        option_names = [option.get("name", "") for option in product.options]
        option_values = [", ".join(option.get("values", [])) for option in product.options]
        publication_names = ", ".join(product.publications)
        for variant in product.variants:
            selected_size, _size_required = extract_size_value(product, variant)
            offer_id = merchant_center_offer_id(product, variant)
            rows.append(
                {
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "title": product.title,
                    "status": product.status,
                    "vendor": product.vendor,
                    "vendor_kind": product.vendor_kind,
                    "product_type": product.product_type,
                    "google_youtube_published": "true" if product.google_published else "false",
                    "publication_names": publication_names,
                    "online_store_url": product.online_store_url,
                    "tags": " | ".join(product.tags),
                    "option_1_name": option_names[0] if len(option_names) > 0 else "",
                    "option_1_values": option_values[0] if len(option_values) > 0 else "",
                    "option_2_name": option_names[1] if len(option_names) > 1 else "",
                    "option_2_values": option_values[1] if len(option_values) > 1 else "",
                    "option_3_name": option_names[2] if len(option_names) > 2 else "",
                    "option_3_values": option_values[2] if len(option_values) > 2 else "",
                    "variant_id": variant.variant_id,
                    "merchant_center_offer_id": offer_id,
                    "variant_title": variant.title,
                    "variant_sku": variant.sku,
                    "variant_price": variant.price,
                    "variant_inventory_policy": variant.inventory_policy,
                    "variant_inventory_quantity": "" if variant.inventory_quantity is None else variant.inventory_quantity,
                    "variant_available_for_sale": "true" if variant.available_for_sale else "false",
                    "variant_selected_options": json.dumps(variant.selected_options, ensure_ascii=True),
                    "derived_size": selected_size,
                }
            )
    return rows


def product_priority(product: ProductRecord) -> tuple[int, int, int, str]:
    cleanup_rank = 0 if product.needs_brand_cleanup else 1
    confidence_rank = 0 if product.house_brand_confident else 1
    return (cleanup_rank, confidence_rank, -len(product.variants), product.handle)


def merchant_center_offer_id(product: ProductRecord, variant: VariantRecord) -> str:
    return f"shopify_{MERCHANT_CENTER_FEED_LABEL}_{product.product_id}_{variant.variant_id}"


def build_brand_cleanup(products: list[ProductRecord]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    cleanup_rows: list[dict[str, str]] = []
    manual_rows: list[dict[str, str]] = []
    for product in sorted(products, key=lambda item: (item.product_id, item.handle)):
        if product.vendor_kind == "domain_variant":
            cleanup_rows.append(
                {
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "current_vendor": product.vendor,
                    "proposed_vendor": CANONICAL_BRAND,
                    "reason": "Vendor uses the store-domain variant instead of the canonical house-brand name.",
                }
            )
            continue
        if product.vendor_kind != "url":
            continue
        if product.house_brand_confident:
            cleanup_rows.append(
                {
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "current_vendor": product.vendor,
                    "proposed_vendor": CANONICAL_BRAND,
                    "reason": "Vendor stores a supplier URL; no third-party brand signal was detected and the product matches core house-brand assortment patterns.",
                }
            )
        else:
            reason = "Vendor stores a supplier URL but the product lacks enough house-brand evidence for safe normalization."
            if product.brand_signals:
                reason = f"Vendor stores a supplier URL and the description includes third-party brand signal(s): {', '.join(product.brand_signals)}."
            manual_rows.append(
                {
                    "queue_type": "brand_cleanup",
                    "product_id": product.product_id,
                    "variant_id": "",
                    "id": "",
                    "handle": product.handle,
                    "title": product.title,
                    "current_vendor": product.vendor,
                    "status": product.status,
                    "google_youtube_published": "true" if product.google_published else "false",
                    "issue": "brand_manual_review",
                    "details": reason,
                    "candidate_brand": "",
                    "candidate_age_group": "",
                    "candidate_gender": "",
                    "candidate_color": "",
                    "candidate_size": "",
                }
            )
    return cleanup_rows, manual_rows


def build_feed_pilot(products: list[ProductRecord], target_rows: int) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    pilot_rows: list[dict[str, str]] = []
    manual_rows: list[dict[str, str]] = []

    eligible_products = [
        product
        for product in products
        if product.status == "ACTIVE" and product.google_published
    ]

    for product in sorted(eligible_products, key=product_priority):
        if len(pilot_rows) >= target_rows:
            return pilot_rows, manual_rows

        evaluations: list[tuple[tuple[int, int, int, int, str], dict[str, str], dict[str, str] | None]] = []
        for variant in product.variants:
            size_value, size_required = extract_size_value(product, variant)
            brand_value = CANONICAL_BRAND if product.house_brand_confident else ""
            age_group = infer_age_group(product, variant, size_value)
            gender = infer_gender(product, variant)
            color = infer_color(product, variant)
            offer_id = merchant_center_offer_id(product, variant)

            reasons: list[str] = []
            if not brand_value:
                reasons.append("brand_uncertain")
            if not age_group:
                reasons.append("age_group_ambiguous")
            if not gender:
                reasons.append("gender_ambiguous")
            if not color:
                reasons.append("color_ambiguous")
            if size_required and not size_value:
                reasons.append("size_missing")

            pilot_row = {
                "id": offer_id,
                "brand": brand_value,
                "age_group": age_group or "",
                "gender": gender or "",
                "color": color or "",
                "size": size_value,
                "manual_review_reason": "",
            }
            manual_row = None
            if reasons:
                manual_row = {
                    "queue_type": "supplemental_feed",
                    "product_id": product.product_id,
                    "variant_id": variant.variant_id,
                    "id": offer_id,
                    "handle": product.handle,
                    "title": product.title,
                    "current_vendor": product.vendor,
                    "status": product.status,
                    "google_youtube_published": "true",
                    "issue": "; ".join(reasons),
                    "details": (
                        "Representative pilot row withheld because one or more fields could not be inferred confidently from live title/options/SKU/tag data."
                    ),
                    "candidate_brand": brand_value,
                    "candidate_age_group": age_group or "",
                    "candidate_gender": gender or "",
                    "candidate_color": color or "",
                    "candidate_size": size_value,
                }
            evaluation_rank = (
                0 if not reasons else 1,
                0 if age_group and age_group != "adult" else 1,
                0 if size_value else 1,
                0 if color else 1,
                variant.variant_id,
            )
            evaluations.append((evaluation_rank, pilot_row, manual_row))

        best_rank, best_pilot_row, best_manual_row = sorted(evaluations, key=lambda item: item[0])[0]
        if best_manual_row is None:
            pilot_rows.append(best_pilot_row)
        else:
            manual_rows.append(best_manual_row)
    return pilot_rows, manual_rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_summary(products: list[ProductRecord], pilot_rows: list[dict[str, str]], manual_rows: list[dict[str, str]], brand_rows: list[dict[str, str]], output_dir: Path) -> dict[str, Any]:
    url_vendor_products = [product for product in products if product.vendor_kind == "url"]
    active_google_products = [product for product in products if product.status == "ACTIVE" and product.google_published]
    return {
        "artifact_dir": str(output_dir),
        "catalog_products": len(products),
        "active_products": sum(1 for product in products if product.status == "ACTIVE"),
        "archived_products": sum(1 for product in products if product.status == "ARCHIVED"),
        "active_google_published_products": len(active_google_products),
        "url_vendor_product_count": len(url_vendor_products),
        "url_vendor_product_count_active": sum(1 for product in url_vendor_products if product.status == "ACTIVE"),
        "url_vendor_product_count_google_published": sum(1 for product in url_vendor_products if product.google_published),
        "brand_cleanup_row_count": len(brand_rows),
        "supplemental_feed_pilot_rows": len(pilot_rows),
        "manual_review_rows": len(manual_rows),
        "merchant_center_primary_offer_id_pattern": "shopify_US_{product_id}_{variant_id}",
        "merchant_center_id_note": (
            "Browser Agent B2 confirmed that Shopify Content API offers in Merchant Center account 124884876 use the exact "
            "join key pattern shopify_US_{product_id}_{variant_id}. The pilot now emits that full offer ID format. "
            "Google auto-crawled products use opaque numeric IDs and are intentionally out of scope for this first pilot."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase 3C feed-engineering pilot artifacts.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    parser.add_argument("--target-pilot-rows", type=int, default=TARGET_PILOT_ROWS, help="Target count for upload-ready pilot rows.")
    args = parser.parse_args()

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    output_dir = Path(args.output_dir)

    client = ShopifyClient(store_domain, access_token)
    products = fetch_products(client)

    catalog_rows = build_catalog_rows(products)
    brand_rows, brand_manual_rows = build_brand_cleanup(products)
    pilot_rows, feed_manual_rows = build_feed_pilot(products, args.target_pilot_rows)
    manual_rows = brand_manual_rows + feed_manual_rows
    summary = build_summary(products, pilot_rows, manual_rows, brand_rows, output_dir)

    write_csv(
        output_dir / "shopify_catalog_export.csv",
        catalog_rows,
        [
            "product_id",
            "handle",
            "title",
            "status",
            "vendor",
            "vendor_kind",
            "product_type",
            "google_youtube_published",
            "publication_names",
            "online_store_url",
            "tags",
            "option_1_name",
            "option_1_values",
            "option_2_name",
            "option_2_values",
            "option_3_name",
            "option_3_values",
            "variant_id",
            "merchant_center_offer_id",
            "variant_title",
            "variant_sku",
            "variant_price",
            "variant_inventory_policy",
            "variant_inventory_quantity",
            "variant_available_for_sale",
            "variant_selected_options",
            "derived_size",
        ],
    )
    write_csv(
        output_dir / "brand_cleanup.csv",
        brand_rows,
        ["product_id", "handle", "current_vendor", "proposed_vendor", "reason"],
    )
    write_csv(
        output_dir / "supplemental_feed_pilot.csv",
        pilot_rows,
        ["id", "brand", "age_group", "gender", "color", "size", "manual_review_reason"],
    )
    write_csv(
        output_dir / "manual_review_queue.csv",
        manual_rows,
        [
            "queue_type",
            "product_id",
            "variant_id",
            "id",
            "handle",
            "title",
            "current_vendor",
            "status",
            "google_youtube_published",
            "issue",
            "details",
            "candidate_brand",
            "candidate_age_group",
            "candidate_gender",
            "candidate_color",
            "candidate_size",
        ],
    )
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
