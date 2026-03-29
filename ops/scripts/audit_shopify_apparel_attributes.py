#!/usr/bin/env python3
"""Dry-run audit of Shopify apparel attribute coverage and fill candidates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
PRODUCT_PAGE_SIZE = 50
VARIANT_PAGE_SIZE = 100
ORDER_PAGE_SIZE = 25
LINE_ITEM_PAGE_SIZE = 100
TIMEOUT_SECONDS = 120
DEFAULT_START_DATE = "2024-01-01"
DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3e-apparel-attribute-audit")

PRODUCTS_QUERY = """
query Products($first: Int!, $after: String, $query: String) {
  products(first: $first, after: $after, query: $query, sortKey: INVENTORY_TOTAL, reverse: true) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      legacyResourceId
      handle
      title
      vendor
      status
      totalInventory
      productType
      tags
      onlineStoreUrl
      collections(first: 20) {
        nodes {
          handle
          title
        }
      }
      options {
        name
        values
      }
      variants(first: 100) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          legacyResourceId
          title
          sku
          selectedOptions {
            name
            value
          }
        }
      }
      categoryField: metafield(namespace: "custom", key: "category1") {
        value
      }
      subcategoryField: metafield(namespace: "custom", key: "subcategory") {
        value
      }
      typeField: metafield(namespace: "custom", key: "type") {
        value
      }
      styleField: metafield(namespace: "custom", key: "style") {
        value
      }
      patternField: metafield(namespace: "custom", key: "pattern") {
        value
      }
      shopifyGenderField: metafield(namespace: "shopify", key: "target-gender") {
        value
      }
      shopifyAgeGroupField: metafield(namespace: "shopify", key: "age-group") {
        value
      }
      shopifySizeField: metafield(namespace: "shopify", key: "size") {
        value
      }
      shopifyColorField: metafield(namespace: "shopify", key: "color-pattern") {
        value
      }
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
      nodes {
        id
        legacyResourceId
        title
        sku
        selectedOptions {
          name
          value
        }
      }
    }
  }
}
"""

ORDERS_QUERY = """
query Orders($first: Int!, $after: String, $query: String) {
  orders(first: $first, after: $after, query: $query, sortKey: PROCESSED_AT, reverse: true) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      name
      processedAt
      lineItems(first: 100) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          quantity
          discountedTotalSet {
            shopMoney {
              amount
              currencyCode
            }
          }
          product {
            legacyResourceId
          }
        }
      }
    }
  }
}
"""

ORDER_LINE_ITEMS_QUERY = """
query OrderLineItems($id: ID!, $first: Int!, $after: String) {
  order(id: $id) {
    lineItems(first: $first, after: $after) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        quantity
        discountedTotalSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        product {
          legacyResourceId
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
    "rainbow": "Multicolor",
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

AGE_GROUP_ORDER = {
    "newborn": 1,
    "infant": 2,
    "toddler": 3,
    "kids": 4,
    "adult": 5,
}

ADULT_TOKENS = {
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
    "couple",
    "couples",
}

FEMALE_CONTEXT_PATTERNS = (
    "mommy and me",
    "mother daughter",
    "mother-daughter",
    "mom daughter",
    "mom-daughter",
)

MALE_CONTEXT_PATTERNS = (
    "daddy and me",
    "father son",
    "father-son",
    "dad son",
    "dad-son",
)

UNISEX_CONTEXT_PATTERNS = (
    "family matching",
    "matching family",
    "family set",
    "family sets",
    "couples",
    "couple",
)


@dataclass
class VariantRecord:
    variant_id: str
    variant_gid: str
    title: str
    sku: str
    selected_options: list[dict[str, str]]


@dataclass
class ProductRecord:
    product_id: str
    product_gid: str
    handle: str
    title: str
    vendor: str
    status: str
    total_inventory: int
    product_type: str
    tags: list[str]
    online_store_url: str
    collections: list[dict[str, str]]
    options: list[dict[str, Any]]
    variants: list[VariantRecord]
    custom_category1: str
    custom_subcategory: str
    custom_type: str
    custom_style: str
    custom_pattern: str
    shopify_gender_raw: str
    shopify_age_group_raw: str
    shopify_size_raw: str
    shopify_color_raw: str


@dataclass
class Candidate:
    value: str
    confidence: str
    source: str


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(6):
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
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

    def fetch_more_variants(self, product_gid: str, after: str) -> list[VariantRecord]:
        variants: list[VariantRecord] = []
        cursor = after
        while cursor:
            data = self.graphql(
                MORE_VARIANTS_QUERY,
                {"id": product_gid, "first": VARIANT_PAGE_SIZE, "after": cursor},
            )["product"]["variants"]
            variants.extend(
                VariantRecord(
                    variant_id=clean(node.get("legacyResourceId")),
                    variant_gid=clean(node.get("id")),
                    title=clean(node.get("title")),
                    sku=clean(node.get("sku")),
                    selected_options=node.get("selectedOptions") or [],
                )
                for node in data["nodes"]
            )
            if not data["pageInfo"]["hasNextPage"]:
                break
            cursor = data["pageInfo"]["endCursor"]
        return variants

    def fetch_active_products(self) -> list[ProductRecord]:
        rows: list[ProductRecord] = []
        after: str | None = None
        while True:
            data = self.graphql(
                PRODUCTS_QUERY,
                {"first": PRODUCT_PAGE_SIZE, "after": after, "query": "status:active"},
            )["products"]
            for node in data["nodes"]:
                variants = [
                    VariantRecord(
                        variant_id=clean(item.get("legacyResourceId")),
                        variant_gid=clean(item.get("id")),
                        title=clean(item.get("title")),
                        sku=clean(item.get("sku")),
                        selected_options=item.get("selectedOptions") or [],
                    )
                    for item in node["variants"]["nodes"]
                ]
                variant_page = node["variants"]["pageInfo"]
                if variant_page["hasNextPage"]:
                    variants.extend(self.fetch_more_variants(clean(node.get("id")), variant_page["endCursor"]))

                rows.append(
                    ProductRecord(
                        product_id=clean(node.get("legacyResourceId")),
                        product_gid=clean(node.get("id")),
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        vendor=clean(node.get("vendor")),
                        status=clean(node.get("status")),
                        total_inventory=int(node.get("totalInventory") or 0),
                        product_type=clean(node.get("productType")),
                        tags=[clean(tag) for tag in node.get("tags") or [] if clean(tag)],
                        online_store_url=clean(node.get("onlineStoreUrl")),
                        collections=[
                            {"handle": clean(item.get("handle")), "title": clean(item.get("title"))}
                            for item in (node.get("collections") or {}).get("nodes") or []
                        ],
                        options=node.get("options") or [],
                        variants=variants,
                        custom_category1=clean((node.get("categoryField") or {}).get("value")),
                        custom_subcategory=clean((node.get("subcategoryField") or {}).get("value")),
                        custom_type=clean((node.get("typeField") or {}).get("value")),
                        custom_style=clean((node.get("styleField") or {}).get("value")),
                        custom_pattern=clean((node.get("patternField") or {}).get("value")),
                        shopify_gender_raw=clean((node.get("shopifyGenderField") or {}).get("value")),
                        shopify_age_group_raw=clean((node.get("shopifyAgeGroupField") or {}).get("value")),
                        shopify_size_raw=clean((node.get("shopifySizeField") or {}).get("value")),
                        shopify_color_raw=clean((node.get("shopifyColorField") or {}).get("value")),
                    )
                )
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return rows

    def iter_orders(self, query_string: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        after: str | None = None
        while True:
            data = self.graphql(
                ORDERS_QUERY,
                {"first": ORDER_PAGE_SIZE, "after": after, "query": query_string},
            )["orders"]
            rows.extend(data["nodes"])
            if not data["pageInfo"]["hasNextPage"]:
                break
            after = data["pageInfo"]["endCursor"]
        return rows

    def fetch_order_line_items(self, order_gid: str, after: str | None = None) -> dict[str, Any]:
        return self.graphql(
            ORDER_LINE_ITEMS_QUERY,
            {"id": order_gid, "first": LINE_ITEM_PAGE_SIZE, "after": after},
        )["order"]["lineItems"]


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def normalize_text(value: str) -> str:
    return normalize_space(value).lower()


def metafield_present(value: str) -> bool:
    stripped = clean(value)
    return bool(stripped and stripped != "[]")


def uniq_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        key = normalize_text(value)
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(normalize_space(value))
    return output


def regex_token_present(text: str, token: str) -> bool:
    return bool(re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", text))


def option_name_matches(option_name: str, token: str) -> bool:
    return token in normalize_text(option_name).rstrip(":")


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
    return any(regex_token_present(text, token) for token in size_tokens)


def extract_variant_size(variant: VariantRecord) -> str:
    for option in variant.selected_options:
        option_name = normalize_text(option.get("name", ""))
        option_value = normalize_space(option.get("value", ""))
        if ("size" in option_name or "age" in option_name) and option_value:
            return option_value
    if not variant.title or variant.title == "Default Title":
        return ""
    segments = [normalize_space(segment) for segment in variant.title.split("/") if normalize_space(segment)]
    if len(segments) >= 2:
        size_like_segments = [segment for segment in segments if looks_like_size_value(segment)]
        if len(size_like_segments) == 1:
            return size_like_segments[0]
        first_segment, second_segment = segments[0], segments[1]
        if extract_color_terms(first_segment) and looks_like_size_value(second_segment):
            return second_segment
    first_segment = segments[0] if segments else ""
    return first_segment if looks_like_size_value(first_segment) else ""


def extract_color_terms(value: str) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []
    output: list[str] = []
    for token, canonical in COLOR_MAP.items():
        if regex_token_present(text, token) and canonical not in output:
            output.append(canonical)
    return output


def join_collections(product: ProductRecord) -> str:
    labels = [item["handle"] or item["title"] for item in product.collections if item["handle"] or item["title"]]
    return " | ".join(labels)


def option_summary(product: ProductRecord) -> str:
    chunks = []
    for option in product.options:
        values = [normalize_space(value) for value in option.get("values", []) if normalize_space(value)]
        chunks.append(f"{normalize_space(option.get('name', ''))}: {', '.join(values[:12])}")
    return " | ".join(chunks)


def product_context_blob(product: ProductRecord) -> str:
    parts = [
        product.title,
        product.handle.replace("-", " "),
        " ".join(product.tags),
        join_collections(product),
        product.product_type,
        product.custom_category1,
        product.custom_subcategory,
        product.custom_type,
        product.custom_style,
        product.custom_pattern,
        option_summary(product),
    ]
    return normalize_text(" ".join(part for part in parts if part))


def derive_size_candidate(product: ProductRecord) -> Candidate:
    explicit_values: list[str] = []
    explicit_sources: list[str] = []
    for option in product.options:
        option_name = normalize_space(option.get("name", ""))
        option_name_text = normalize_text(option_name)
        if "size" in option_name_text or "age" in option_name_text:
            values = [
                normalize_space(value)
                for value in option.get("values", [])
                if normalize_space(value) and normalize_text(value) != "default title"
            ]
            if values:
                explicit_values.extend(values)
                explicit_sources.append(f"option:{option_name}")
    explicit_values = uniq_preserve(explicit_values)
    if explicit_values:
        return Candidate("|".join(explicit_values[:30]), "high", "|".join(uniq_preserve(explicit_sources)))

    variant_values = uniq_preserve([extract_variant_size(variant) for variant in product.variants if extract_variant_size(variant)])
    if variant_values:
        return Candidate("|".join(variant_values[:30]), "medium", "variant:title_or_selected_options")

    tag_values = uniq_preserve([tag for tag in product.tags if looks_like_size_value(tag)])
    if tag_values:
        return Candidate("|".join(tag_values[:30]), "medium", "tags")

    return Candidate("", "low", "")


def derive_color_candidate(product: ProductRecord) -> Candidate:
    option_colors: list[str] = []
    option_sources: list[str] = []
    for option in product.options:
        option_name = normalize_space(option.get("name", ""))
        option_name_text = normalize_text(option_name)
        if "color" in option_name_text or "colour" in option_name_text:
            option_sources.append(f"option:{option_name}")
            for value in option.get("values", []):
                value_text = normalize_text(value)
                if value_text in ROLE_LIKE_VALUES:
                    continue
                option_colors.extend(extract_color_terms(value))
    option_colors = uniq_preserve(option_colors)
    if option_colors:
        return Candidate("|".join(option_colors[:12]), "high", "|".join(uniq_preserve(option_sources)))

    context_colors = uniq_preserve(extract_color_terms(" ".join(product.tags + [product.title, product.custom_pattern, product.custom_style])))
    if context_colors:
        return Candidate("|".join(context_colors[:12]), "medium", "tags|title|custom_pattern")

    return Candidate("", "low", "")


def derive_gender_candidate(product: ProductRecord, size_candidate: Candidate) -> Candidate:
    context = product_context_blob(product)
    size_blob = normalize_text(size_candidate.value.replace("|", " "))
    female_context = any(pattern in context for pattern in FEMALE_CONTEXT_PATTERNS)
    male_context = any(pattern in context for pattern in MALE_CONTEXT_PATTERNS)
    unisex_context = any(pattern in context for pattern in UNISEX_CONTEXT_PATTERNS)

    female_sources: list[str] = []
    male_sources: list[str] = []
    source_blobs = {
        "size_values": size_blob,
        "title_handle": normalize_text(f"{product.title} {product.handle.replace('-', ' ')}"),
        "tags": normalize_text(" ".join(product.tags)),
        "collections": normalize_text(join_collections(product)),
        "custom_taxonomy": normalize_text(" ".join([product.custom_category1, product.custom_subcategory, product.custom_style])),
    }
    for source, blob in source_blobs.items():
        if blob and any(regex_token_present(blob, token) for token in FEMALE_TOKENS):
            female_sources.append(source)
        if blob and any(regex_token_present(blob, token) for token in MALE_TOKENS):
            male_sources.append(source)

    if unisex_context and (male_sources or (female_sources and male_sources)):
        return Candidate("unisex", "high", "title|collections|tags:unisex_context")

    if female_context and not male_sources:
        return Candidate("female", "high", "title|collections|tags:female_context")

    if male_context and not female_sources:
        return Candidate("male", "high", "title|collections|tags:male_context")

    if unisex_context:
        return Candidate("unisex", "high", "title|collections|tags:unisex_context")

    if female_sources and male_sources:
        return Candidate("unisex", "high", "|".join(uniq_preserve(female_sources + male_sources)))
    if female_sources:
        return Candidate("female", "high", "|".join(uniq_preserve(female_sources)))
    if male_sources:
        return Candidate("male", "high", "|".join(uniq_preserve(male_sources)))

    return Candidate("", "low", "")


def classify_age_group_from_text(text: str) -> str:
    blob = normalize_text(text)
    if not blob:
        return ""
    if re.search(r"\b(newborn|nb)\b", blob):
        return "newborn"

    month_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:m|mo|month|months)\b", blob)]
    if month_matches:
        return "infant" if max(month_matches) <= 12 else "toddler"

    year_matches = [int(match) for match in re.findall(r"\b(\d{1,2})\s*(?:y|yr|yrs|year|years)\b", blob)]
    t_matches = [int(match) for match in re.findall(r"\b(\d{1,2})t\b", blob)]
    range_matches = [
        max(int(start), int(end))
        for start, end in re.findall(r"\b(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)?\b", blob)
    ]
    numeric_child_sizes = [int(match) for match in re.findall(r"\b(1[0-6]0)\b", blob)]

    if year_matches or t_matches or range_matches:
        max_age = max(year_matches + t_matches + range_matches)
        return "toddler" if max_age <= 5 else "kids"
    if numeric_child_sizes:
        return "kids"
    if re.search(r"\b(baby|infant)\b", blob):
        return "infant"
    if re.search(r"\b(toddler)\b", blob):
        return "toddler"
    if re.search(r"\b(child|kid|kids|girl|girls|boy|boys|daughter|son)\b", blob):
        return "kids"
    if any(regex_token_present(blob, token) for token in ADULT_TOKENS):
        return "adult"
    return ""


def sort_age_groups(values: list[str]) -> list[str]:
    unique = uniq_preserve(values)
    return sorted(unique, key=lambda item: AGE_GROUP_ORDER.get(item, 999))


def derive_age_group_candidate(product: ProductRecord, size_candidate: Candidate) -> Candidate:
    size_values = [value for value in size_candidate.value.split("|") if value]
    size_groups = [classify_age_group_from_text(value) for value in size_values]
    size_groups = [value for value in size_groups if value]
    if size_groups:
        return Candidate("|".join(sort_age_groups(size_groups)), "high", f"size_values:{size_candidate.source}")

    context_blobs = {
        "tags": " ".join(product.tags),
        "title_handle": f"{product.title} {product.handle.replace('-', ' ')}",
        "collections": join_collections(product),
        "option_values": option_summary(product),
    }
    context_groups: list[str] = []
    context_sources: list[str] = []
    for source, blob in context_blobs.items():
        age_group = classify_age_group_from_text(blob)
        if age_group:
            context_groups.append(age_group)
            context_sources.append(source)

    if context_groups:
        return Candidate("|".join(sort_age_groups(context_groups)), "medium", "|".join(uniq_preserve(context_sources)))

    return Candidate("", "low", "")


def money_amount(payload: dict[str, Any] | None) -> float:
    try:
        return float(((payload or {}).get("shopMoney") or {}).get("amount") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def collect_revenue(
    client: ShopifyClient,
    product_ids: set[str],
    *,
    start_date: str,
    sleep_ms: int,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    orders = client.iter_orders(f"processed_at:>={start_date}")
    aggregates: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"discounted_revenue": 0.0, "units": 0, "orders": set(), "currency_codes": Counter()}
    )
    orders_scanned = 0
    nested_line_item_pages = 0

    def apply_nodes(order_name: str, nodes: list[dict[str, Any]]) -> None:
        for node in nodes:
            product = node.get("product") or {}
            product_id = clean(product.get("legacyResourceId"))
            if product_id not in product_ids:
                continue
            aggregates[product_id]["discounted_revenue"] += money_amount(node.get("discountedTotalSet"))
            aggregates[product_id]["units"] += int(node.get("quantity") or 0)
            aggregates[product_id]["orders"].add(order_name)
            currency = clean((((node.get("discountedTotalSet") or {}).get("shopMoney") or {}).get("currencyCode")))
            if currency:
                aggregates[product_id]["currency_codes"][currency] += 1

    for order in orders:
        orders_scanned += 1
        line_items = order.get("lineItems") or {}
        apply_nodes(clean(order.get("name")), line_items.get("nodes") or [])
        after = line_items.get("pageInfo", {}).get("endCursor")
        while line_items.get("pageInfo", {}).get("hasNextPage"):
            nested_line_item_pages += 1
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)
            line_items = client.fetch_order_line_items(clean(order.get("id")), after)
            apply_nodes(clean(order.get("name")), line_items.get("nodes") or [])
            after = line_items.get("pageInfo", {}).get("endCursor")
        if sleep_ms > 0:
            time.sleep(sleep_ms / 1000.0)

    return aggregates, {
        "start_date": start_date,
        "orders_scanned": orders_scanned,
        "nested_line_item_pages": nested_line_item_pages,
    }


def build_audit_rows(products: list[ProductRecord], revenue: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for product in products:
        size_candidate = derive_size_candidate(product)
        color_candidate = derive_color_candidate(product)
        gender_candidate = derive_gender_candidate(product, size_candidate)
        age_group_candidate = derive_age_group_candidate(product, size_candidate)

        present = {
            "gender": metafield_present(product.shopify_gender_raw),
            "age_group": metafield_present(product.shopify_age_group_raw),
            "size": metafield_present(product.shopify_size_raw),
            "color": metafield_present(product.shopify_color_raw),
        }
        candidates = {
            "gender": gender_candidate,
            "age_group": age_group_candidate,
            "size": size_candidate,
            "color": color_candidate,
        }
        missing_attributes = [field for field, is_present in present.items() if not is_present]
        unresolved_attributes = [
            field
            for field in missing_attributes
            if candidates[field].confidence not in {"high", "medium"} or not candidates[field].value
        ]
        fully_high_confidence = bool(missing_attributes) and all(
            candidates[field].confidence == "high" and candidates[field].value for field in missing_attributes
        )

        aggregate = revenue.get(product.product_id) or {}
        rows.append(
            {
                "product_id": product.product_id,
                "handle": product.handle,
                "title": product.title,
                "vendor": product.vendor,
                "product_type": product.product_type,
                "custom_category1": product.custom_category1,
                "custom_subcategory": product.custom_subcategory,
                "custom_type": product.custom_type,
                "custom_style": product.custom_style,
                "custom_pattern": product.custom_pattern,
                "total_inventory": product.total_inventory,
                "discounted_revenue": f"{aggregate.get('discounted_revenue', 0.0):.2f}",
                "units": aggregate.get("units", 0),
                "order_count": len(aggregate.get("orders", set())),
                "currency_codes": "|".join(sorted(aggregate.get("currency_codes", Counter()))),
                "shopify_gender_present": "true" if present["gender"] else "false",
                "shopify_age_group_present": "true" if present["age_group"] else "false",
                "shopify_size_present": "true" if present["size"] else "false",
                "shopify_color_present": "true" if present["color"] else "false",
                "missing_attributes": "|".join(missing_attributes),
                "unresolved_attributes": "|".join(unresolved_attributes),
                "fully_high_confidence_fill_candidate": "true" if fully_high_confidence else "false",
                "candidate_gender": gender_candidate.value,
                "candidate_gender_confidence": gender_candidate.confidence,
                "candidate_gender_source": gender_candidate.source,
                "candidate_age_group": age_group_candidate.value,
                "candidate_age_group_confidence": age_group_candidate.confidence,
                "candidate_age_group_source": age_group_candidate.source,
                "candidate_size": size_candidate.value,
                "candidate_size_confidence": size_candidate.confidence,
                "candidate_size_source": size_candidate.source,
                "candidate_color": color_candidate.value,
                "candidate_color_confidence": color_candidate.confidence,
                "candidate_color_source": color_candidate.source,
                "collections": join_collections(product),
                "option_summary": option_summary(product),
                "tags": " | ".join(product.tags[:20]),
                "online_store_url": product.online_store_url,
            }
        )

    rows.sort(key=lambda item: (-float(item["discounted_revenue"]), item["handle"]))
    for rank, row in enumerate(rows, start=1):
        row["revenue_rank"] = rank
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def select_rows(rows: list[dict[str, Any]], predicate: Any, top_limit: int) -> list[dict[str, Any]]:
    filtered = [row for row in rows if predicate(row)]
    return filtered[:top_limit]


def write_summary(path: Path, rows: list[dict[str, Any]], revenue_summary: dict[str, Any]) -> None:
    missing_counts = Counter()
    unresolved_counts = Counter()
    high_confidence_counts = Counter()
    medium_confidence_counts = Counter()
    for row in rows:
        missing_fields = [value for value in row["missing_attributes"].split("|") if value]
        unresolved_fields = [value for value in row["unresolved_attributes"].split("|") if value]
        for field in missing_fields:
            missing_counts[field] += 1
            confidence = row[f"candidate_{field}_confidence"]
            if confidence == "high" and row[f"candidate_{field}"]:
                high_confidence_counts[field] += 1
            elif confidence == "medium" and row[f"candidate_{field}"]:
                medium_confidence_counts[field] += 1
        for field in unresolved_fields:
            unresolved_counts[field] += 1

    summary = {
        "total_active_products": len(rows),
        "products_missing_any_structured_attribute": sum(1 for row in rows if row["missing_attributes"]),
        "products_with_all_missing_attributes_high_confidence_fillable": sum(
            1 for row in rows if row["fully_high_confidence_fill_candidate"] == "true"
        ),
        "structured_field_presence_counts": {
            "gender": sum(1 for row in rows if row["shopify_gender_present"] == "true"),
            "age_group": sum(1 for row in rows if row["shopify_age_group_present"] == "true"),
            "size": sum(1 for row in rows if row["shopify_size_present"] == "true"),
            "color": sum(1 for row in rows if row["shopify_color_present"] == "true"),
        },
        "structured_field_missing_counts": dict(missing_counts),
        "high_confidence_candidate_counts_when_missing": dict(high_confidence_counts),
        "medium_confidence_candidate_counts_when_missing": dict(medium_confidence_counts),
        "unresolved_missing_counts": dict(unresolved_counts),
        "top_missing_products_by_revenue": [
            {
                "handle": row["handle"],
                "discounted_revenue": float(row["discounted_revenue"]),
                "missing_attributes": row["missing_attributes"],
            }
            for row in select_rows(rows, lambda item: bool(item["missing_attributes"]), 20)
        ],
        "top_high_confidence_fill_candidates_by_revenue": [
            {
                "handle": row["handle"],
                "discounted_revenue": float(row["discounted_revenue"]),
                "missing_attributes": row["missing_attributes"],
            }
            for row in select_rows(rows, lambda item: item["fully_high_confidence_fill_candidate"] == "true", 20)
        ],
        "revenue_summary": revenue_summary,
    }
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dry-run apparel attribute audit for Shopify products.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Artifact output directory.")
    parser.add_argument("--start-date", default=DEFAULT_START_DATE, help="Inclusive processed_at lower bound (YYYY-MM-DD).")
    parser.add_argument("--top-limit", type=int, default=50, help="Top-N rows to export in filtered revenue-ranked files.")
    parser.add_argument("--sleep-ms", type=int, default=50, help="Pause between paginated order requests.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    products = client.fetch_active_products()
    revenue, revenue_summary = collect_revenue(
        client,
        {product.product_id for product in products},
        start_date=args.start_date,
        sleep_ms=max(args.sleep_ms, 0),
    )
    rows = build_audit_rows(products, revenue)

    fieldnames = [
        "revenue_rank",
        "product_id",
        "handle",
        "title",
        "vendor",
        "product_type",
        "custom_category1",
        "custom_subcategory",
        "custom_type",
        "custom_style",
        "custom_pattern",
        "total_inventory",
        "discounted_revenue",
        "units",
        "order_count",
        "currency_codes",
        "shopify_gender_present",
        "shopify_age_group_present",
        "shopify_size_present",
        "shopify_color_present",
        "missing_attributes",
        "unresolved_attributes",
        "fully_high_confidence_fill_candidate",
        "candidate_gender",
        "candidate_gender_confidence",
        "candidate_gender_source",
        "candidate_age_group",
        "candidate_age_group_confidence",
        "candidate_age_group_source",
        "candidate_size",
        "candidate_size_confidence",
        "candidate_size_source",
        "candidate_color",
        "candidate_color_confidence",
        "candidate_color_source",
        "collections",
        "option_summary",
        "tags",
        "online_store_url",
    ]
    write_csv(output_dir / "apparel_attribute_audit_all.csv", rows, fieldnames)
    write_csv(
        output_dir / "products_missing_any_attribute_top20_by_revenue.csv",
        select_rows(rows, lambda row: bool(row["missing_attributes"]), 20),
        fieldnames,
    )
    write_csv(
        output_dir / "products_missing_any_attribute_top50_by_revenue.csv",
        select_rows(rows, lambda row: bool(row["missing_attributes"]), args.top_limit),
        fieldnames,
    )
    write_csv(
        output_dir / "high_confidence_attribute_fill_candidates_top20_by_revenue.csv",
        select_rows(rows, lambda row: row["fully_high_confidence_fill_candidate"] == "true", 20),
        fieldnames,
    )
    write_csv(
        output_dir / "high_confidence_attribute_fill_candidates_top50_by_revenue.csv",
        select_rows(rows, lambda row: row["fully_high_confidence_fill_candidate"] == "true", args.top_limit),
        fieldnames,
    )
    for attribute in ("gender", "age_group", "size", "color"):
        write_csv(
            output_dir / f"missing_{attribute}_top50_by_revenue.csv",
            select_rows(
                rows,
                lambda row, attribute=attribute: attribute in row["missing_attributes"].split("|"),
                args.top_limit,
            ),
            fieldnames,
        )

    write_summary(output_dir / "summary.json", rows, revenue_summary)

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "total_active_products": len(rows),
                "products_missing_any_structured_attribute": sum(1 for row in rows if row["missing_attributes"]),
                "products_with_all_missing_attributes_high_confidence_fillable": sum(
                    1 for row in rows if row["fully_high_confidence_fill_candidate"] == "true"
                ),
                "start_date": args.start_date,
                "orders_scanned": revenue_summary["orders_scanned"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
