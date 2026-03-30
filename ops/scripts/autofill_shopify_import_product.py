#!/usr/bin/env python3
"""Autofill missing Shopify product taxonomy and apparel metafields for one imported product.

This is intended for post-import automation after a BukitDrop (or similar)
product lands in Shopify. Default mode is dry-run.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.audit_shopify_apparel_attributes import (  # noqa: E402
    Candidate,
    ProductRecord as ApparelProductRecord,
    VariantRecord,
    derive_age_group_candidate,
    derive_color_candidate,
    derive_gender_candidate,
    derive_size_candidate,
    join_collections,
    metafield_present as apparel_metafield_present,
    option_summary,
)
from ops.scripts.backfill_product_metadata import (  # noqa: E402
    normalize_category1,
    normalize_pattern,
    normalize_style,
    normalize_subcategory,
    normalize_subcategory2,
    normalize_type,
)
from ops.scripts.fill_shopify_apparel_attributes import (  # noqa: E402
    MetaobjectRef,
    ShopifyClient as ApparelMetafieldClient,
    metafield_present,
    resolve_field_references,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
PRODUCT_PAGE_SIZE = 50
DEFAULT_OUTPUT_DIR = Path("ops/import-automation/2026-03-30-bukitdrop-product-autofill")
SUPPORTED_APPAREL_FIELDS = ("gender", "age_group", "size", "color")
GENERIC_CATEGORY_FULL_NAMES = {
    "",
    "Apparel & Accessories > Clothing",
    "Apparel & Accessories > Clothing > Baby & Toddler Clothing",
}
STATIC_CATEGORY_FALLBACKS = {
    "dresses": (
        "gid://shopify/TaxonomyCategory/aa-1-4",
        "Apparel & Accessories > Clothing > Dresses",
    ),
    "sets": (
        "gid://shopify/TaxonomyCategory/aa-1-11",
        "Apparel & Accessories > Clothing > Outfit Sets",
    ),
    "t-shirts": (
        "gid://shopify/TaxonomyCategory/aa-1-13-8",
        "Apparel & Accessories > Clothing > Clothing Tops > T-Shirts",
    ),
    "tops": (
        "gid://shopify/TaxonomyCategory/aa-1-13-7",
        "Apparel & Accessories > Clothing > Clothing Tops > Shirts",
    ),
    "sweaters": (
        "gid://shopify/TaxonomyCategory/aa-1-13-12",
        "Apparel & Accessories > Clothing > Clothing Tops > Sweaters",
    ),
    "swimwear": (
        "gid://shopify/TaxonomyCategory/aa-1-20",
        "Apparel & Accessories > Clothing > Swimwear",
    ),
    "trunks": (
        "gid://shopify/TaxonomyCategory/aa-1-20",
        "Apparel & Accessories > Clothing > Swimwear",
    ),
}
CUSTOM_FIELD_ORDER = (
    "category1",
    "subcategory",
    "subcategory2",
    "type",
    "style",
    "pattern",
)
PRODUCT_QUERY_BY_HANDLE = """
query ProductByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    ...ImportAutofillProduct
  }
}

fragment ImportAutofillProduct on Product {
  id
  legacyResourceId
  handle
  title
  vendor
  status
  productType
  descriptionHtml
  tags
  onlineStoreUrl
  category {
    id
    fullName
  }
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
  category1Field: metafield(namespace: "custom", key: "category1") {
    value
  }
  subcategoryField: metafield(namespace: "custom", key: "subcategory") {
    value
  }
  subcategory2Field: metafield(namespace: "custom", key: "subcategory2") {
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
  genderField: metafield(namespace: "shopify", key: "target-gender") {
    value
    references(first: 20) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  ageGroupField: metafield(namespace: "shopify", key: "age-group") {
    value
    references(first: 20) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  sizeField: metafield(namespace: "shopify", key: "size") {
    value
    references(first: 50) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  colorField: metafield(namespace: "shopify", key: "color-pattern") {
    value
    references(first: 30) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
}
"""
PRODUCT_QUERY_BY_ID = """
query ProductById($id: ID!) {
  product(id: $id) {
    ...ImportAutofillProduct
  }
}

fragment ImportAutofillProduct on Product {
  id
  legacyResourceId
  handle
  title
  vendor
  status
  productType
  descriptionHtml
  tags
  onlineStoreUrl
  category {
    id
    fullName
  }
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
  category1Field: metafield(namespace: "custom", key: "category1") {
    value
  }
  subcategoryField: metafield(namespace: "custom", key: "subcategory") {
    value
  }
  subcategory2Field: metafield(namespace: "custom", key: "subcategory2") {
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
  genderField: metafield(namespace: "shopify", key: "target-gender") {
    value
    references(first: 20) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  ageGroupField: metafield(namespace: "shopify", key: "age-group") {
    value
    references(first: 20) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  sizeField: metafield(namespace: "shopify", key: "size") {
    value
    references(first: 50) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
      }
    }
  }
  colorField: metafield(namespace: "shopify", key: "color-pattern") {
    value
    references(first: 30) {
      nodes {
        ... on Metaobject {
          id
          handle
          displayName
        }
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
PEER_PRODUCTS_QUERY = """
query PeerProducts($first: Int!, $after: String, $query: String!) {
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
      status
      productType
      category {
        id
        fullName
      }
      subcategoryField: metafield(namespace: "custom", key: "subcategory") {
        value
      }
      typeField: metafield(namespace: "custom", key: "type") {
        value
      }
    }
  }
}
"""
PRODUCT_UPDATE_MUTATION = """
mutation UpdateProduct($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      productType
      category {
        id
        fullName
      }
      category1Field: metafield(namespace: "custom", key: "category1") {
        value
      }
      subcategoryField: metafield(namespace: "custom", key: "subcategory") {
        value
      }
      subcategory2Field: metafield(namespace: "custom", key: "subcategory2") {
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
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class ProductDetails:
    product_id: str
    product_gid: str
    handle: str
    title: str
    vendor: str
    status: str
    product_type: str
    description_html: str
    tags: list[str]
    online_store_url: str
    category_id: str
    category_full_name: str
    collections: list[dict[str, str]]
    options: list[dict[str, Any]]
    variants: list[VariantRecord]
    custom_category1: str
    custom_subcategory: str
    custom_subcategory2: str
    custom_type: str
    custom_style: str
    custom_pattern: str
    shopify_gender_raw: str
    shopify_age_group_raw: str
    shopify_size_raw: str
    shopify_color_raw: str
    shopify_gender_refs: list[MetaobjectRef]
    shopify_age_group_refs: list[MetaobjectRef]
    shopify_size_refs: list[MetaobjectRef]
    shopify_color_refs: list[MetaobjectRef]


@dataclass
class PeerProduct:
    handle: str
    title: str
    product_type: str
    category_id: str
    category_full_name: str
    custom_subcategory: str
    custom_type: str


@dataclass
class CategoryChoice:
    category_id: str
    category_full_name: str
    confidence: str
    source: str


@dataclass
class ProductUpdatePlan:
    category_id: str = ""
    category_full_name: str = ""
    category_source: str = ""
    product_type: str = ""
    custom_values: dict[str, str] | None = None


@dataclass
class ApparelFieldPlan:
    field: str
    status: str
    reason: str
    candidate_value: str
    candidate_confidence: str
    candidate_source: str
    normalized_labels: str
    reference_ids: str
    reference_labels: str


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_text(value: str) -> str:
    return clean(value).lower()


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return clean(text)


def is_blank(value: str) -> bool:
    return not clean(value)


def current_category_is_generic(product: ProductDetails) -> bool:
    return clean(product.category_full_name) in GENERIC_CATEGORY_FULL_NAMES


def parse_refs(nodes: list[dict[str, Any]] | None) -> list[MetaobjectRef]:
    refs: list[MetaobjectRef] = []
    for node in nodes or []:
        refs.append(
            MetaobjectRef(
                id=clean(node.get("id")),
                handle=clean(node.get("handle")),
                display_name=clean(node.get("displayName")),
            )
        )
    return refs


class ShopifyClient(ApparelMetafieldClient):
    def fetch_product(self, *, handle: str = "", product_gid: str = "") -> ProductDetails:
        if bool(handle) == bool(product_gid):
            raise RuntimeError("Pass exactly one of --handle or --product-id.")

        if product_gid and not product_gid.startswith("gid://shopify/Product/"):
            product_gid = f"gid://shopify/Product/{clean(product_gid)}"

        if handle:
            node = self.graphql(PRODUCT_QUERY_BY_HANDLE, {"handle": handle})["productByHandle"]
        else:
            node = self.graphql(PRODUCT_QUERY_BY_ID, {"id": product_gid})["product"]

        if not node:
            selector = handle or product_gid
            raise RuntimeError(f"Product not found for `{selector}`.")

        variants = [
            VariantRecord(
                variant_id=clean(item.get("legacyResourceId")),
                variant_gid=clean(item.get("id")),
                title=clean(item.get("title")),
                sku=clean(item.get("sku")),
                selected_options=item.get("selectedOptions") or [],
            )
            for item in (node.get("variants") or {}).get("nodes") or []
        ]
        variant_page = (node.get("variants") or {}).get("pageInfo") or {}
        if variant_page.get("hasNextPage"):
            variants.extend(self.fetch_more_variants(clean(node.get("id")), clean(variant_page.get("endCursor"))))

        return ProductDetails(
            product_id=clean(node.get("legacyResourceId")),
            product_gid=clean(node.get("id")),
            handle=clean(node.get("handle")),
            title=clean(node.get("title")),
            vendor=clean(node.get("vendor")),
            status=clean(node.get("status")),
            product_type=clean(node.get("productType")),
            description_html=clean(node.get("descriptionHtml")),
            tags=[clean(tag) for tag in node.get("tags") or [] if clean(tag)],
            online_store_url=clean(node.get("onlineStoreUrl")),
            category_id=clean(((node.get("category") or {}).get("id"))),
            category_full_name=clean(((node.get("category") or {}).get("fullName"))),
            collections=[
                {"handle": clean(item.get("handle")), "title": clean(item.get("title"))}
                for item in (node.get("collections") or {}).get("nodes") or []
            ],
            options=node.get("options") or [],
            variants=variants,
            custom_category1=clean(((node.get("category1Field") or {}).get("value"))),
            custom_subcategory=clean(((node.get("subcategoryField") or {}).get("value"))),
            custom_subcategory2=clean(((node.get("subcategory2Field") or {}).get("value"))),
            custom_type=clean(((node.get("typeField") or {}).get("value"))),
            custom_style=clean(((node.get("styleField") or {}).get("value"))),
            custom_pattern=clean(((node.get("patternField") or {}).get("value"))),
            shopify_gender_raw=clean(((node.get("genderField") or {}).get("value"))),
            shopify_age_group_raw=clean(((node.get("ageGroupField") or {}).get("value"))),
            shopify_size_raw=clean(((node.get("sizeField") or {}).get("value"))),
            shopify_color_raw=clean(((node.get("colorField") or {}).get("value"))),
            shopify_gender_refs=parse_refs((((node.get("genderField") or {}).get("references") or {}).get("nodes"))),
            shopify_age_group_refs=parse_refs((((node.get("ageGroupField") or {}).get("references") or {}).get("nodes"))),
            shopify_size_refs=parse_refs((((node.get("sizeField") or {}).get("references") or {}).get("nodes"))),
            shopify_color_refs=parse_refs((((node.get("colorField") or {}).get("references") or {}).get("nodes"))),
        )

    def fetch_more_variants(self, product_gid: str, after: str) -> list[VariantRecord]:
        variants: list[VariantRecord] = []
        cursor = after
        while cursor:
            data = self.graphql(MORE_VARIANTS_QUERY, {"id": product_gid, "first": 100, "after": cursor})["product"]["variants"]
            variants.extend(
                VariantRecord(
                    variant_id=clean(node.get("legacyResourceId")),
                    variant_gid=clean(node.get("id")),
                    title=clean(node.get("title")),
                    sku=clean(node.get("sku")),
                    selected_options=node.get("selectedOptions") or [],
                )
                for node in data.get("nodes") or []
            )
            if not data.get("pageInfo", {}).get("hasNextPage"):
                break
            cursor = clean(data.get("pageInfo", {}).get("endCursor"))
        return variants

    def fetch_active_peers(self) -> list[PeerProduct]:
        rows: list[PeerProduct] = []
        after: str | None = None
        while True:
            data = self.graphql(
                PEER_PRODUCTS_QUERY,
                {"first": PRODUCT_PAGE_SIZE, "after": after, "query": "status:active"},
            )["products"]
            for node in data.get("nodes") or []:
                rows.append(
                    PeerProduct(
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        product_type=clean(node.get("productType")),
                        category_id=clean(((node.get("category") or {}).get("id"))),
                        category_full_name=clean(((node.get("category") or {}).get("fullName"))),
                        custom_subcategory=clean(((node.get("subcategoryField") or {}).get("value"))),
                        custom_type=clean(((node.get("typeField") or {}).get("value"))),
                    )
                )
            if not data.get("pageInfo", {}).get("hasNextPage"):
                break
            after = clean(data.get("pageInfo", {}).get("endCursor"))
        return rows

    def update_product(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.graphql(PRODUCT_UPDATE_MUTATION, {"product": payload})["productUpdate"]


def build_taxonomy_blob(product: ProductDetails) -> str:
    description_text = strip_html(product.description_html)
    parts = [
        product.title,
        product.handle.replace("-", " "),
        product.vendor,
        description_text,
        " ".join(product.tags),
        product.product_type,
        product.custom_category1,
        product.custom_subcategory,
        product.custom_subcategory2,
        product.custom_type,
        product.custom_style,
        product.custom_pattern,
        join_collections(
            ApparelProductRecord(
                product_id=product.product_id,
                product_gid=product.product_gid,
                handle=product.handle,
                title=product.title,
                vendor=product.vendor,
                status=product.status,
                total_inventory=0,
                product_type=product.product_type,
                tags=product.tags,
                online_store_url=product.online_store_url,
                collections=product.collections,
                options=product.options,
                variants=product.variants,
                custom_category1=product.custom_category1,
                custom_subcategory=product.custom_subcategory,
                custom_type=product.custom_type,
                custom_style=product.custom_style,
                custom_pattern=product.custom_pattern,
                shopify_gender_raw=product.shopify_gender_raw,
                shopify_age_group_raw=product.shopify_age_group_raw,
                shopify_size_raw=product.shopify_size_raw,
                shopify_color_raw=product.shopify_color_raw,
            )
        ),
        option_summary(
            ApparelProductRecord(
                product_id=product.product_id,
                product_gid=product.product_gid,
                handle=product.handle,
                title=product.title,
                vendor=product.vendor,
                status=product.status,
                total_inventory=0,
                product_type=product.product_type,
                tags=product.tags,
                online_store_url=product.online_store_url,
                collections=product.collections,
                options=product.options,
                variants=product.variants,
                custom_category1=product.custom_category1,
                custom_subcategory=product.custom_subcategory,
                custom_type=product.custom_type,
                custom_style=product.custom_style,
                custom_pattern=product.custom_pattern,
                shopify_gender_raw=product.shopify_gender_raw,
                shopify_age_group_raw=product.shopify_age_group_raw,
                shopify_size_raw=product.shopify_size_raw,
                shopify_color_raw=product.shopify_color_raw,
            )
        ),
    ]
    return normalize_text(" ".join(part for part in parts if part))


def infer_custom_taxonomy(product: ProductDetails) -> dict[str, str]:
    blob = build_taxonomy_blob(product)
    category1 = product.custom_category1 or normalize_category1(product.custom_category1, blob)
    subcategory = product.custom_subcategory or normalize_subcategory(product.custom_subcategory, blob)
    custom_type = product.custom_type or normalize_type(product.product_type or product.custom_type, subcategory, blob)
    style = product.custom_style or normalize_style(product.custom_style, blob)
    pattern = product.custom_pattern or normalize_pattern(product.custom_pattern, blob)
    subcategory2 = product.custom_subcategory2 or normalize_subcategory2(product.custom_subcategory2, subcategory, blob)
    return {
        "category1": category1,
        "subcategory": subcategory,
        "subcategory2": subcategory2,
        "type": custom_type,
        "style": style,
        "pattern": pattern,
    }


def build_category_index(peers: list[PeerProduct]) -> dict[str, Counter[tuple[str, str]]]:
    index: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    for peer in peers:
        if clean(peer.category_full_name) in GENERIC_CATEGORY_FULL_NAMES:
            continue
        category_key = (clean(peer.category_id), clean(peer.category_full_name))
        sub_key = normalize_text(peer.custom_subcategory)
        type_key = normalize_text(peer.custom_type or peer.product_type)
        if sub_key and type_key:
            index[f"subcategory_type:{sub_key}|{type_key}"][category_key] += 1
        if sub_key:
            index[f"subcategory:{sub_key}"][category_key] += 1
        if type_key:
            index[f"type:{type_key}"][category_key] += 1
    return index


def choose_peer_category(
    *,
    subcategory: str,
    custom_type: str,
    category_index: dict[str, Counter[tuple[str, str]]],
) -> CategoryChoice | None:
    keys = [
        (f"subcategory_type:{normalize_text(subcategory)}|{normalize_text(custom_type)}", "high"),
        (f"subcategory:{normalize_text(subcategory)}", "medium"),
        (f"type:{normalize_text(custom_type)}", "medium"),
    ]
    for key, confidence in keys:
        if key not in category_index or not category_index[key]:
            continue
        (category_id, category_full_name), count = category_index[key].most_common(1)[0]
        return CategoryChoice(
            category_id=category_id,
            category_full_name=category_full_name,
            confidence=confidence,
            source=f"peer_index:{key}:count={count}",
        )
    return None


def choose_static_category(subcategory: str, custom_type: str) -> CategoryChoice | None:
    for token in (normalize_text(subcategory), normalize_text(custom_type)):
        if token in STATIC_CATEGORY_FALLBACKS:
            category_id, category_full_name = STATIC_CATEGORY_FALLBACKS[token]
            return CategoryChoice(
                category_id=category_id,
                category_full_name=category_full_name,
                confidence="medium",
                source=f"static_map:{token}",
            )
    return None


def infer_category_choice(
    product: ProductDetails,
    *,
    custom_values: dict[str, str],
    category_index: dict[str, Counter[tuple[str, str]]],
) -> CategoryChoice | None:
    if not current_category_is_generic(product):
        return None
    choice = choose_peer_category(
        subcategory=custom_values["subcategory"],
        custom_type=custom_values["type"],
        category_index=category_index,
    )
    if choice:
        return choice
    return choose_static_category(custom_values["subcategory"], custom_values["type"])


def build_apparel_product(product: ProductDetails, custom_values: dict[str, str]) -> ApparelProductRecord:
    return ApparelProductRecord(
        product_id=product.product_id,
        product_gid=product.product_gid,
        handle=product.handle,
        title=product.title,
        vendor=product.vendor,
        status=product.status,
        total_inventory=0,
        product_type=product.product_type or custom_values["type"],
        tags=product.tags,
        online_store_url=product.online_store_url,
        collections=product.collections,
        options=product.options,
        variants=product.variants,
        custom_category1=custom_values["category1"],
        custom_subcategory=custom_values["subcategory"],
        custom_type=custom_values["type"],
        custom_style=custom_values["style"],
        custom_pattern=custom_values["pattern"],
        shopify_gender_raw=product.shopify_gender_raw,
        shopify_age_group_raw=product.shopify_age_group_raw,
        shopify_size_raw=product.shopify_size_raw,
        shopify_color_raw=product.shopify_color_raw,
    )


def normalize_age_group_candidate(raw_value: str) -> str:
    tokens = []
    for token in [clean(part) for part in raw_value.split("|") if clean(part)]:
        key = normalize_text(token)
        if key in {"newborn", "infant"}:
            tokens.append("infant")
        else:
            tokens.append(key)
    deduped: list[str] = []
    for token in tokens:
        if token and token not in deduped:
            deduped.append(token)
    return "|".join(deduped)


def plan_product_update(
    product: ProductDetails,
    *,
    custom_values: dict[str, str],
    category_choice: CategoryChoice | None,
) -> ProductUpdatePlan:
    plan = ProductUpdatePlan(custom_values={})

    if category_choice and current_category_is_generic(product):
        plan.category_id = category_choice.category_id
        plan.category_full_name = category_choice.category_full_name
        plan.category_source = category_choice.source

    if is_blank(product.product_type) and custom_values["type"]:
        plan.product_type = custom_values["type"]

    for field in CUSTOM_FIELD_ORDER:
        current_value = getattr(product, f"custom_{field}")
        target_value = clean(custom_values[field])
        if is_blank(current_value) and target_value:
            plan.custom_values[field] = target_value

    return plan


def plan_apparel_updates(
    product: ProductDetails,
    *,
    custom_values: dict[str, str],
    refs_by_field: dict[str, list[MetaobjectRef]],
    min_confidence: str,
) -> list[ApparelFieldPlan]:
    apparel_product = build_apparel_product(product, custom_values)
    candidates = {
        "size": derive_size_candidate(apparel_product),
        "color": derive_color_candidate(apparel_product),
    }
    candidates["gender"] = derive_gender_candidate(apparel_product, candidates["size"])
    candidates["age_group"] = derive_age_group_candidate(apparel_product, candidates["size"])

    current_raw = {
        "gender": product.shopify_gender_raw,
        "age_group": product.shopify_age_group_raw,
        "size": product.shopify_size_raw,
        "color": product.shopify_color_raw,
    }
    current_refs = {
        "gender": product.shopify_gender_refs,
        "age_group": product.shopify_age_group_refs,
        "size": product.shopify_size_refs,
        "color": product.shopify_color_refs,
    }
    threshold_rank = {"low": 1, "medium": 2, "high": 3}
    rows: list[ApparelFieldPlan] = []

    for field in SUPPORTED_APPAREL_FIELDS:
        candidate = candidates[field]
        status = "skip"
        reason = ""
        normalized_labels = ""
        reference_ids = ""
        reference_labels = ""

        if metafield_present(current_raw[field], current_refs[field]):
            reason = "field_already_present_live"
        elif not candidate.value:
            reason = "candidate_blank"
        elif threshold_rank.get(candidate.confidence, 0) < threshold_rank.get(min_confidence, 0):
            reason = f"confidence_below_threshold:{candidate.confidence}"
        else:
            candidate_value = candidate.value
            if field == "age_group":
                candidate_value = normalize_age_group_candidate(candidate_value)
            labels, refs, unresolved = resolve_field_references(
                field=field,
                raw_value=candidate_value,
                refs_by_field=refs_by_field,
            )
            if unresolved:
                reason = "|".join(unresolved)
            elif not refs:
                reason = "no_reference_ids_resolved"
            else:
                status = "plan"
                reason = "ready"
                normalized_labels = "|".join(labels)
                reference_ids = "|".join(ref.id for ref in refs)
                reference_labels = "|".join(ref.display_name for ref in refs)

        rows.append(
            ApparelFieldPlan(
                field=field,
                status=status,
                reason=reason,
                candidate_value=candidate.value,
                candidate_confidence=candidate.confidence,
                candidate_source=candidate.source,
                normalized_labels=normalized_labels,
                reference_ids=reference_ids,
                reference_labels=reference_labels,
            )
        )
    return rows


def build_product_update_payload(product: ProductDetails, plan: ProductUpdatePlan) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": product.product_gid}
    if plan.category_id:
        payload["category"] = plan.category_id
    if plan.product_type:
        payload["productType"] = plan.product_type
    metafields = []
    for key, value in (plan.custom_values or {}).items():
        metafields.append(
            {
                "namespace": "custom",
                "key": key,
                "type": "single_line_text_field",
                "value": value,
            }
        )
    if metafields:
        payload["metafields"] = metafields
    return payload


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def execute(
    client: ShopifyClient,
    *,
    product: ProductDetails,
    product_update_plan: ProductUpdatePlan,
    apparel_plans: list[ApparelFieldPlan],
    execute: bool,
    pause_ms: int,
) -> dict[str, Any]:
    summary = {
        "execute": bool(execute),
        "product_update_attempted": False,
        "product_update_applied": False,
        "product_update_errors": [],
        "apparel_updates_attempted": 0,
        "apparel_updates_applied": 0,
        "apparel_update_errors": [],
    }
    if not execute:
        return summary

    payload = build_product_update_payload(product, product_update_plan)
    if len(payload) > 1:
        summary["product_update_attempted"] = True
        response = client.update_product(payload)
        errors = []
        for item in response.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {clean(item.get('message'))}" if prefix else clean(item.get("message")))
        if errors:
            summary["product_update_errors"] = errors
        else:
            summary["product_update_applied"] = True
            if pause_ms > 0:
                time.sleep(pause_ms / 1000.0)

    for item in apparel_plans:
        if item.status != "plan":
            continue
        summary["apparel_updates_attempted"] += 1
        errors = client.set_metafield_references(
            product_gid=product.product_gid,
            key={
                "gender": "target-gender",
                "age_group": "age-group",
                "size": "size",
                "color": "color-pattern",
            }[item.field],
            reference_ids=[part for part in item.reference_ids.split("|") if part],
        )
        if errors:
            summary["apparel_update_errors"].append({"field": item.field, "errors": errors})
        else:
            summary["apparel_updates_applied"] += 1
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--handle", default="", help="Target product handle.")
    parser.add_argument("--product-id", default="", help="Target Shopify product ID or gid.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for dry-run and execution artifacts.")
    parser.add_argument("--min-confidence", default="high", choices=["high", "medium"], help="Minimum apparel candidate confidence.")
    parser.add_argument("--execute", action="store_true", help="Apply the planned changes live.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live updates.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    product = client.fetch_product(handle=args.handle, product_gid=args.product_id)
    peers = client.fetch_active_peers()
    category_index = build_category_index(peers)
    custom_values = infer_custom_taxonomy(product)
    category_choice = infer_category_choice(product, custom_values=custom_values, category_index=category_index)
    product_update_plan = plan_product_update(product, custom_values=custom_values, category_choice=category_choice)
    refs_by_field = {
        "gender": client.fetch_metaobjects("shopify--target-gender"),
        "age_group": client.fetch_metaobjects("shopify--age-group"),
        "size": client.fetch_metaobjects("shopify--size"),
        "color": client.fetch_metaobjects("shopify--color-pattern"),
    }
    apparel_plans = plan_apparel_updates(
        product,
        custom_values=custom_values,
        refs_by_field=refs_by_field,
        min_confidence=args.min_confidence,
    )
    execution = execute(
        client,
        product=product,
        product_update_plan=product_update_plan,
        apparel_plans=apparel_plans,
        execute=args.execute,
        pause_ms=max(args.pause_ms, 0),
    )

    plan_rows = [
        {
            "handle": product.handle,
            "title": product.title,
            "current_product_type": product.product_type,
            "target_product_type": product_update_plan.product_type,
            "current_category_full_name": product.category_full_name,
            "target_category_full_name": product_update_plan.category_full_name,
            "target_category_source": product_update_plan.category_source,
            "current_category1": product.custom_category1,
            "target_category1": (product_update_plan.custom_values or {}).get("category1", ""),
            "current_subcategory": product.custom_subcategory,
            "target_subcategory": (product_update_plan.custom_values or {}).get("subcategory", ""),
            "current_subcategory2": product.custom_subcategory2,
            "target_subcategory2": (product_update_plan.custom_values or {}).get("subcategory2", ""),
            "current_type": product.custom_type,
            "target_type": (product_update_plan.custom_values or {}).get("type", ""),
            "current_style": product.custom_style,
            "target_style": (product_update_plan.custom_values or {}).get("style", ""),
            "current_pattern": product.custom_pattern,
            "target_pattern": (product_update_plan.custom_values or {}).get("pattern", ""),
        }
    ]
    apparel_rows = [asdict(item) for item in apparel_plans]
    write_csv(
        output_dir / "product_update_plan.csv",
        plan_rows,
        [
            "handle",
            "title",
            "current_product_type",
            "target_product_type",
            "current_category_full_name",
            "target_category_full_name",
            "target_category_source",
            "current_category1",
            "target_category1",
            "current_subcategory",
            "target_subcategory",
            "current_subcategory2",
            "target_subcategory2",
            "current_type",
            "target_type",
            "current_style",
            "target_style",
            "current_pattern",
            "target_pattern",
        ],
    )
    write_csv(
        output_dir / "apparel_field_plan.csv",
        apparel_rows,
        [
            "field",
            "status",
            "reason",
            "candidate_value",
            "candidate_confidence",
            "candidate_source",
            "normalized_labels",
            "reference_ids",
            "reference_labels",
        ],
    )

    summary = {
        "handle": product.handle,
        "product_id": product.product_id,
        "product_update_payload": build_product_update_payload(product, product_update_plan),
        "planned_custom_updates": len(product_update_plan.custom_values or {}),
        "planned_apparel_updates": sum(1 for item in apparel_plans if item.status == "plan"),
        "execution": execution,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
