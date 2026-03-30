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
from urllib.parse import urlsplit

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
    build_metaobject_index,
    choose_preferred_reference,
    metafield_present,
    resolve_field_references,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 120
PRODUCT_PAGE_SIZE = 50
DEFAULT_OUTPUT_DIR = Path("ops/import-automation/2026-03-30-bukitdrop-product-autofill")
SUPPORTED_APPAREL_FIELDS = ("gender", "age_group", "size", "color")
SHOPIFY_EXTRA_FIELD_CONFIG = {
    "fabric": {"key": "fabric", "metaobject_type": "shopify--fabric"},
    "care_instructions": {"key": "care-instructions", "metaobject_type": "shopify--care-instructions"},
    "clothing_features": {"key": "clothing-features", "metaobject_type": "shopify--clothing-features"},
    "dress_occasion": {"key": "dress-occasion", "metaobject_type": "shopify--dress-occasion"},
    "dress_style": {"key": "dress-style", "metaobject_type": "shopify--dress-style"},
    "neckline": {"key": "neckline", "metaobject_type": "shopify--neckline"},
    "skirt_dress_length_type": {
        "key": "skirt-dress-length-type",
        "metaobject_type": "shopify--skirt-dress-length-type",
    },
    "sleeve_length_type": {"key": "sleeve-length-type", "metaobject_type": "shopify--sleeve-length-type"},
    "top_length_type": {"key": "top-length-type", "metaobject_type": "shopify--top-length-type"},
}
SUPPORTED_EXTRA_CATEGORY_FIELDS = tuple(SHOPIFY_EXTRA_FIELD_CONFIG.keys())
GENERIC_CATEGORY_FULL_NAMES = {
    "",
    "Uncategorized",
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
EXTRA_FABRIC_RULES = (
    (("cotton", "cotton-silk", "cotton silk"), "Cotton"),
    (("polyester", "poly lining", "polyester lining"), "Polyester"),
    (("denim",), "Denim"),
    (("faux leather", "fake leather", "pu leather", "vegan leather"), "Faux leather"),
)
EXTRA_DRESS_STYLE_RULES = (
    (("a-line", "a line"), "A-line"),
    (("flared", "flare", "fit and flare"), "Flared"),
)
EXTRA_NECKLINE_RULES = (
    (("crew neck", "crewneck"), "Crew"),
    (("round neck", "round neckline", "round-neck"), "Round"),
    (("square neck", "square neckline", "square-neck"), "Square"),
)
EXTRA_SLEEVE_RULES = (
    (("sleeveless", "without sleeves"), "Sleeveless"),
    (("short sleeve", "short sleeves", "short-sleeve", "short sleeved", "short-sleeved"), "Short"),
)
EXTRA_LENGTH_RULES = (
    (("maxi",), "Maxi"),
    (("midi",), "Midi"),
)
EXTRA_DRESS_OCCASION_RULES = (
    (("beach", "boardwalk"), "Beach outings"),
    (("vacation", "vacations", "resort"), "family vacations"),
    (("summer", "brunch"), "casual summer events"),
    (("party", "birthday", "celebration"), "Party"),
    (("everyday", "daily wear", "day to day"), "Everyday"),
    (("casual",), "Casual"),
)
EXTRA_CLOTHING_FEATURE_RULES = (
    (("insulated", "puffer", "quilted padding"), "Insulated"),
)
EXTRA_TOP_LENGTH_RULES = (
    (("crop top", "cropped"), "Crop top"),
    (("longline", "long top"), "Long"),
    (("regular length", "medium length"), "Medium"),
)
GENERIC_MEDIA_FILENAME_TOKENS = (
    "pomelli-image",
    "o1cn0",
    "image_",
    "img_",
    "product-image",
    "untitled",
)
REPLACEABLE_SUBCATEGORY2_VALUES = {
    "",
    "Everyday Dresses",
    "Maxi Dresses",
    "Midi Dresses",
    "Mini Dresses",
    "Sundresses",
    "Formal Dresses",
}
CHILD_SIZE_TAG_MAP = {
    "90cm": "Child 1-2yr",
    "100cm": "Child 3-4yr",
    "110cm": "Child 5-6yr",
    "120cm": "Child 7-8yr",
    "130cm": "Child 9-10yr",
    "140cm": "Child 11-12yr",
    "150cm": "Child 13-14yr",
    "160cm": "Child 13-14yr",
    "1-2t": "Child 1-2yr",
    "2t": "Child 1-2yr",
    "3-4t": "Child 3-4yr",
    "4t": "Child 3-4yr",
    "5-6t": "Child 5-6yr",
    "6t": "Child 5-6yr",
    "7-8t": "Child 7-8yr",
    "8t": "Child 7-8yr",
    "9-10t": "Child 9-10yr",
    "10t": "Child 9-10yr",
    "11-12t": "Child 11-12yr",
    "12t": "Child 11-12yr",
    "13-14t": "Child 13-14yr",
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
  media(first: 50) {
    nodes {
      __typename
      ... on MediaImage {
        id
        alt
        image {
          url
        }
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
  fabricField: metafield(namespace: "shopify", key: "fabric") {
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
  careInstructionsField: metafield(namespace: "shopify", key: "care-instructions") {
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
  clothingFeaturesField: metafield(namespace: "shopify", key: "clothing-features") {
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
  dressOccasionField: metafield(namespace: "shopify", key: "dress-occasion") {
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
  dressStyleField: metafield(namespace: "shopify", key: "dress-style") {
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
  necklineField: metafield(namespace: "shopify", key: "neckline") {
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
  skirtDressLengthTypeField: metafield(namespace: "shopify", key: "skirt-dress-length-type") {
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
  sleeveLengthTypeField: metafield(namespace: "shopify", key: "sleeve-length-type") {
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
  topLengthTypeField: metafield(namespace: "shopify", key: "top-length-type") {
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
  media(first: 50) {
    nodes {
      __typename
      ... on MediaImage {
        id
        alt
        image {
          url
        }
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
  fabricField: metafield(namespace: "shopify", key: "fabric") {
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
  careInstructionsField: metafield(namespace: "shopify", key: "care-instructions") {
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
  clothingFeaturesField: metafield(namespace: "shopify", key: "clothing-features") {
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
  dressOccasionField: metafield(namespace: "shopify", key: "dress-occasion") {
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
  dressStyleField: metafield(namespace: "shopify", key: "dress-style") {
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
  necklineField: metafield(namespace: "shopify", key: "neckline") {
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
  skirtDressLengthTypeField: metafield(namespace: "shopify", key: "skirt-dress-length-type") {
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
  sleeveLengthTypeField: metafield(namespace: "shopify", key: "sleeve-length-type") {
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
  topLengthTypeField: metafield(namespace: "shopify", key: "top-length-type") {
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
FILE_UPDATE_MUTATION = """
mutation FileUpdate($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files {
      id
      alt
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""


@dataclass
class MediaImage:
    id: str
    alt: str
    url: str


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
    shopify_extra_raw: dict[str, str]
    shopify_extra_refs: dict[str, list[MetaobjectRef]]
    media: list[MediaImage]


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
    tags: list[str] | None = None


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


@dataclass
class ExtraCategoryFieldPlan:
    field: str
    status: str
    reason: str
    candidate_value: str
    candidate_confidence: str
    candidate_source: str
    normalized_labels: str
    reference_ids: str
    reference_labels: str


@dataclass
class MediaFieldPlan:
    media_id: str
    current_alt: str
    target_alt: str
    current_filename: str
    target_filename: str
    status: str
    reason: str


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_text(value: str) -> str:
    return clean(value).lower()


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return clean(text)


def is_blank(value: str) -> bool:
    return not clean(value)


def uniq_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        token = clean(value)
        key = normalize_text(token)
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(token)
    return output


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

        extra_raw: dict[str, str] = {}
        extra_refs: dict[str, list[MetaobjectRef]] = {}
        extra_aliases = {
            "fabric": "fabricField",
            "care_instructions": "careInstructionsField",
            "clothing_features": "clothingFeaturesField",
            "dress_occasion": "dressOccasionField",
            "dress_style": "dressStyleField",
            "neckline": "necklineField",
            "skirt_dress_length_type": "skirtDressLengthTypeField",
            "sleeve_length_type": "sleeveLengthTypeField",
            "top_length_type": "topLengthTypeField",
        }
        for field, alias in extra_aliases.items():
            metafield = node.get(alias) or {}
            extra_raw[field] = clean(metafield.get("value"))
            extra_refs[field] = parse_refs((((metafield.get("references") or {}).get("nodes"))))

        media = []
        for media_node in (node.get("media") or {}).get("nodes") or []:
            if clean(media_node.get("__typename")) != "MediaImage":
                continue
            media.append(
                MediaImage(
                    id=clean(media_node.get("id")),
                    alt=clean(media_node.get("alt")),
                    url=clean(((media_node.get("image") or {}).get("url"))),
                )
            )

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
            shopify_extra_raw=extra_raw,
            shopify_extra_refs=extra_refs,
            media=media,
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

    def update_files(self, files_payload: list[dict[str, str]]) -> dict[str, Any]:
        return self.graphql(FILE_UPDATE_MUTATION, {"files": files_payload})["fileUpdate"]


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


def collect_rule_labels(blob: str, rules: tuple[tuple[tuple[str, ...], str], ...]) -> list[str]:
    labels: list[str] = []
    for terms, label in rules:
        if any(term in blob for term in terms):
            labels.append(label)
    return uniq_preserve(labels)


def infer_extra_category_candidates(product: ProductDetails, custom_values: dict[str, str]) -> dict[str, Candidate]:
    blob = build_taxonomy_blob(product)
    description_text = normalize_text(strip_html(product.description_html))
    combined_blob = normalize_text(" ".join([blob, description_text, custom_values.get("subcategory", ""), custom_values.get("type", "")]))

    def candidate_from_labels(labels: list[str], *, source: str, confidence: str = "high") -> Candidate:
        return Candidate("|".join(uniq_preserve(labels)), confidence if labels else "low", source if labels else "")

    fabric_labels = collect_rule_labels(combined_blob, EXTRA_FABRIC_RULES)
    care_labels = ["Machine washable"] if any(token in combined_blob for token in ("machine washable", "machine wash", "machine-washable")) else []
    dress_style_labels = collect_rule_labels(combined_blob, EXTRA_DRESS_STYLE_RULES)
    neckline_labels = collect_rule_labels(combined_blob, EXTRA_NECKLINE_RULES)
    sleeve_labels = collect_rule_labels(combined_blob, EXTRA_SLEEVE_RULES)
    length_labels = collect_rule_labels(combined_blob, EXTRA_LENGTH_RULES)
    occasion_labels = collect_rule_labels(combined_blob, EXTRA_DRESS_OCCASION_RULES)
    clothing_feature_labels = collect_rule_labels(combined_blob, EXTRA_CLOTHING_FEATURE_RULES)
    top_length_labels = collect_rule_labels(combined_blob, EXTRA_TOP_LENGTH_RULES)

    return {
        "fabric": candidate_from_labels(fabric_labels, source="title|description|options"),
        "care_instructions": candidate_from_labels(care_labels, source="description"),
        "clothing_features": candidate_from_labels(clothing_feature_labels, source="title|description"),
        "dress_occasion": candidate_from_labels(occasion_labels, source="title|description"),
        "dress_style": candidate_from_labels(dress_style_labels, source="title|description"),
        "neckline": candidate_from_labels(neckline_labels, source="title|description"),
        "skirt_dress_length_type": candidate_from_labels(length_labels, source="title|description"),
        "sleeve_length_type": candidate_from_labels(sleeve_labels, source="title|description"),
        "top_length_type": candidate_from_labels(top_length_labels, source="title|description"),
    }


def infer_dress_subcategory2(product: ProductDetails, custom_values: dict[str, str]) -> str:
    if clean(custom_values.get("subcategory")) != "Dresses":
        return clean(custom_values.get("subcategory2", ""))

    current_length_refs = product.shopify_extra_refs.get("skirt_dress_length_type", [])
    if current_length_refs:
        label = clean(current_length_refs[0].display_name)
        if label:
            return label

    blob = build_taxonomy_blob(product)
    if "maxi" in blob:
        return "Maxi"
    if "midi" in blob:
        return "Midi"
    if "mini" in blob:
        return "Mini"
    return clean(custom_values.get("subcategory2", ""))


def infer_adult_role_prefix(product: ProductDetails, custom_values: dict[str, str] | None = None) -> str:
    category1 = clean((custom_values or {}).get("category1") or product.custom_category1)
    if category1 == "Mommy and Me":
        return "Mother"
    if category1 == "Daddy and Me":
        return "Father"

    gender_refs = [normalize_text(ref.display_name) for ref in product.shopify_gender_refs]
    if "female" in gender_refs:
        return "Mother"
    if "male" in gender_refs:
        return "Father"
    return "Adult"


def normalize_size_tag(raw_value: str, adult_prefix: str) -> str:
    text = normalize_text(raw_value)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    compact = text.replace(" ", "")
    if compact in CHILD_SIZE_TAG_MAP:
        return CHILD_SIZE_TAG_MAP[compact]

    cm_match = re.search(r"\b([6-9]\d|1\d{2}|2[0-2]\d)\s*cm\b", text)
    if cm_match:
        return CHILD_SIZE_TAG_MAP.get(f"{cm_match.group(1)}cm", "")

    child_range = re.search(r"\b(\d{1,2})\s*-\s*(\d{1,2})\s*t\b", text)
    if child_range:
        return CHILD_SIZE_TAG_MAP.get(f"{child_range.group(1)}-{child_range.group(2)}t", "")

    child_single = re.search(r"\b(\d{1,2})t\b", text)
    if child_single:
        return CHILD_SIZE_TAG_MAP.get(f"{child_single.group(1)}t", "")

    alpha_match = re.search(r"\b(xxs|xs|s|m|l|xl|xxl|xxxl|2xl|3xl|4xl|5xl)\b", text)
    if alpha_match:
        label = alpha_match.group(1).upper().replace("XXL", "2XL").replace("XXXL", "3XL")
        return f"{adult_prefix} {label}"

    return ""


def build_generated_tags(product: ProductDetails, custom_values: dict[str, str]) -> list[str]:
    tags: list[str] = []
    color_label = extract_primary_color_label(product)
    if color_label:
        tags.append(color_label)
    if custom_values.get("category1"):
        tags.append(custom_values["category1"])
    if custom_values.get("subcategory"):
        tags.append(custom_values["subcategory"])

    subcategory2 = clean(custom_values.get("subcategory2", ""))
    if subcategory2 and custom_values.get("subcategory") == "Dresses":
        if subcategory2 in {"Midi", "Maxi", "Mini"}:
            tags.append(f"{subcategory2} Dresses")
        else:
            tags.append(subcategory2)
    elif subcategory2:
        tags.append(subcategory2)

    adult_prefix = infer_adult_role_prefix(product, custom_values)
    size_values: list[str] = []
    for option in product.options:
        option_name = normalize_text(option.get("name", ""))
        if "size" in option_name or "age" in option_name or "height" in option_name:
            size_values.extend([clean(value) for value in option.get("values", []) if clean(value)])
    if not size_values:
        size_values = [clean(variant.title) for variant in product.variants if clean(variant.title)]

    for raw_value in uniq_preserve(size_values):
        tag = normalize_size_tag(raw_value, adult_prefix)
        if tag:
            tags.append(tag)

    return uniq_preserve(tags)


def merge_generated_tags(existing_tags: list[str], generated_tags: list[str]) -> list[str]:
    replaceable_dress_tags = {normalize_text(tag) for tag in REPLACEABLE_SUBCATEGORY2_VALUES if clean(tag)}
    generated_replaceable_tags = {
        normalize_text(tag) for tag in generated_tags if normalize_text(tag) in replaceable_dress_tags
    }

    merged: list[str] = []
    seen: set[str] = set()
    for tag in existing_tags:
        normalized = normalize_text(tag)
        if generated_replaceable_tags and normalized in replaceable_dress_tags and normalized not in generated_replaceable_tags:
            continue
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        merged.append(clean(tag))

    for tag in generated_tags:
        normalized = normalize_text(tag)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        merged.append(clean(tag))
    return merged


def resolve_extra_field_references(
    *,
    field: str,
    raw_value: str,
    refs_by_field: dict[str, list[MetaobjectRef]],
) -> tuple[list[str], list[MetaobjectRef], list[str]]:
    refs = refs_by_field[field]
    ref_index = build_metaobject_index(refs)
    labels = uniq_preserve([clean(part) for part in raw_value.split("|") if clean(part)])
    resolved_refs: list[MetaobjectRef] = []
    unresolved: list[str] = []
    seen_ref_ids: set[str] = set()

    for label in labels:
        ref = ref_index.get(normalize_text(label))
        if not ref:
            ref = choose_preferred_reference(refs, display_name=label)
        if not ref:
            unresolved.append(f"no_metaobject_for:{label}")
            continue
        if ref.id not in seen_ref_ids:
            seen_ref_ids.add(ref.id)
            resolved_refs.append(ref)
    return labels, resolved_refs, unresolved


def current_filename_from_url(url: str) -> str:
    path = urlsplit(url).path
    return clean(path.rsplit("/", 1)[-1])


def current_extension_from_url(url: str) -> str:
    filename = current_filename_from_url(url)
    suffix = Path(filename).suffix.lower()
    return suffix or ".jpg"


def slugify_filename(value: str) -> str:
    slug = normalize_text(value)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "product-image"


def should_rename_media(filename: str, handle: str) -> bool:
    normalized = normalize_text(filename)
    if not normalized:
        return True
    if normalize_text(handle).replace("-", "") and normalize_text(handle) in normalized:
        return False
    if any(token in normalized for token in GENERIC_MEDIA_FILENAME_TOKENS):
        return True
    return bool(re.fullmatch(r"[a-f0-9-]{16,}\.[a-z0-9]+", normalized))


def extract_primary_color_label(product: ProductDetails) -> str:
    if product.shopify_color_refs:
        return clean(product.shopify_color_refs[0].display_name)
    for option in product.options:
        option_name = normalize_text(option.get("name", ""))
        if "color" not in option_name and "colour" not in option_name:
            continue
        values = uniq_preserve([clean(value) for value in option.get("values", []) if clean(value)])
        if len(values) == 1:
            return values[0].title()
    return ""


def build_media_alt_base(product: ProductDetails) -> str:
    base_title = clean(product.title.split("|")[0] if "|" in product.title else product.title)
    base_title = re.sub(r"\s+", " ", base_title).strip(" -|")
    if not base_title:
        base_title = clean(product.handle.replace("-", " "))
    color_label = extract_primary_color_label(product)
    if color_label and normalize_text(color_label) not in normalize_text(base_title):
        return clean(f"{base_title} in {color_label}")
    return base_title


def build_media_alt_texts(product: ProductDetails) -> list[str]:
    base_alt = build_media_alt_base(product)
    output: list[str] = []
    for index, _media in enumerate(product.media, start=1):
        if index == 1:
            alt_text = base_alt
        else:
            alt_text = clean(f"{base_alt} photo {index}")
        output.append(alt_text[:125].rstrip(" -"))
    return output


def should_replace_media_alt(current_alt: str, target_alt: str, base_alt: str) -> bool:
    normalized_current = normalize_text(current_alt)
    normalized_target = normalize_text(target_alt)
    normalized_base = normalize_text(base_alt)
    if not normalized_current:
        return True
    if normalized_current == normalized_target:
        return False
    if "product image" in normalized_current:
        return True
    if normalized_current.startswith(normalized_base) and re.search(r"\b(photo|image)\s+\d+\b", normalized_current):
        return True
    return False


def plan_media_updates(product: ProductDetails) -> list[MediaFieldPlan]:
    rows: list[MediaFieldPlan] = []
    target_alt_texts = build_media_alt_texts(product)
    base_alt = build_media_alt_base(product)
    base_slug = slugify_filename(product.handle or product.title)

    for index, (media, target_alt) in enumerate(zip(product.media, target_alt_texts), start=1):
        current_filename = current_filename_from_url(media.url)
        extension = current_extension_from_url(media.url)
        target_filename = f"{base_slug}-{index:02d}{extension}"
        alt_needs_update = should_replace_media_alt(media.alt, target_alt, base_alt)
        filename_needs_update = should_rename_media(current_filename, product.handle)

        if not alt_needs_update and not filename_needs_update:
            rows.append(
                MediaFieldPlan(
                    media_id=media.id,
                    current_alt=media.alt,
                    target_alt=target_alt,
                    current_filename=current_filename,
                    target_filename=target_filename,
                    status="skip",
                    reason="media_already_descriptive",
                )
            )
            continue

        rows.append(
                MediaFieldPlan(
                    media_id=media.id,
                    current_alt=media.alt,
                    target_alt=target_alt,
                    current_filename=current_filename,
                    target_filename=target_filename,
                    status="plan",
                    reason="generic_alt_or_filename",
                )
            )
    return rows


def infer_custom_taxonomy(product: ProductDetails) -> dict[str, str]:
    blob = build_taxonomy_blob(product)
    category1 = product.custom_category1 or normalize_category1(product.custom_category1, blob)
    subcategory = product.custom_subcategory or normalize_subcategory(product.custom_subcategory, blob)
    custom_type = product.custom_type or normalize_type(product.product_type or product.custom_type, subcategory, blob)
    style = product.custom_style or normalize_style(product.custom_style, blob)
    pattern = product.custom_pattern or normalize_pattern(product.custom_pattern, blob)
    subcategory2 = product.custom_subcategory2 or normalize_subcategory2(product.custom_subcategory2, subcategory, blob)

    dress_terms = (" dress", "dresses", "gown", "sundress", "halter", "a-line", "tiered")
    swim_terms = ("swimsuit", "swimwear", "bikini", "trunks", "tankini", "rashguard", "one-piece swimsuit")
    if any(term in blob for term in dress_terms) and not any(term in blob for term in swim_terms):
        subcategory = "Dresses"
        custom_type = "Dresses"
        replaceable_subcategory2 = clean(product.custom_subcategory2) in REPLACEABLE_SUBCATEGORY2_VALUES
        if is_blank(product.custom_subcategory2) or replaceable_subcategory2:
            inferred_subcategory2 = infer_dress_subcategory2(
                product,
                {"subcategory": subcategory, "subcategory2": subcategory2},
            )
            if inferred_subcategory2:
                subcategory2 = inferred_subcategory2
            elif "sundress" in blob:
                subcategory2 = "Sundresses"
            elif "maxi" in blob:
                subcategory2 = "Maxi"
            elif "midi" in blob:
                subcategory2 = "Midi"
            elif "mini" in blob:
                subcategory2 = "Mini"
            else:
                subcategory2 = "Everyday Dresses"

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
        if not target_value:
            continue
        if is_blank(current_value):
            plan.custom_values[field] = target_value
            continue
        if (
            field == "subcategory2"
            and clean(current_value) in REPLACEABLE_SUBCATEGORY2_VALUES
            and clean(current_value) != target_value
        ):
            plan.custom_values[field] = target_value

    generated_tags = build_generated_tags(product, custom_values)
    if generated_tags:
        merged_tags = merge_generated_tags(product.tags, generated_tags)
        current_normalized = [normalize_text(tag) for tag in product.tags if clean(tag)]
        merged_normalized = [normalize_text(tag) for tag in merged_tags if clean(tag)]
        if current_normalized != merged_normalized:
            plan.tags = merged_tags

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


def plan_extra_category_updates(
    product: ProductDetails,
    *,
    custom_values: dict[str, str],
    refs_by_field: dict[str, list[MetaobjectRef]],
    min_confidence: str,
) -> list[ExtraCategoryFieldPlan]:
    candidates = infer_extra_category_candidates(product, custom_values)
    threshold_rank = {"low": 1, "medium": 2, "high": 3}
    rows: list[ExtraCategoryFieldPlan] = []

    for field in SUPPORTED_EXTRA_CATEGORY_FIELDS:
        candidate = candidates[field]
        current_raw = product.shopify_extra_raw.get(field, "")
        current_refs = product.shopify_extra_refs.get(field, [])
        status = "skip"
        reason = ""
        normalized_labels = ""
        reference_ids = ""
        reference_labels = ""

        if metafield_present(current_raw, current_refs):
            reason = "field_already_present_live"
        elif not candidate.value:
            reason = "candidate_blank"
        elif threshold_rank.get(candidate.confidence, 0) < threshold_rank.get(min_confidence, 0):
            reason = f"confidence_below_threshold:{candidate.confidence}"
        else:
            labels, refs, unresolved = resolve_extra_field_references(
                field=field,
                raw_value=candidate.value,
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
            ExtraCategoryFieldPlan(
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
    if plan.tags:
        payload["tags"] = plan.tags
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


def apply_execution_plan(
    client: ShopifyClient,
    *,
    product: ProductDetails,
    product_update_plan: ProductUpdatePlan,
    apparel_plans: list[ApparelFieldPlan],
    extra_category_plans: list[ExtraCategoryFieldPlan],
    media_plans: list[MediaFieldPlan],
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
        "extra_category_updates_attempted": 0,
        "extra_category_updates_applied": 0,
        "extra_category_update_errors": [],
        "media_updates_attempted": 0,
        "media_updates_applied": 0,
        "media_update_errors": [],
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

    for item in extra_category_plans:
        if item.status != "plan":
            continue
        summary["extra_category_updates_attempted"] += 1
        errors = client.set_metafield_references(
            product_gid=product.product_gid,
            key=SHOPIFY_EXTRA_FIELD_CONFIG[item.field]["key"],
            reference_ids=[part for part in item.reference_ids.split("|") if part],
        )
        if errors:
            summary["extra_category_update_errors"].append({"field": item.field, "errors": errors})
        else:
            summary["extra_category_updates_applied"] += 1
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)

    file_updates = []
    for item in media_plans:
        if item.status != "plan":
            continue
        payload = {"id": item.media_id}
        if item.target_alt and normalize_text(item.current_alt) != normalize_text(item.target_alt):
            payload["alt"] = item.target_alt
        if item.target_filename and clean(item.current_filename) != clean(item.target_filename):
            payload["filename"] = item.target_filename
        if len(payload) > 1:
            file_updates.append(payload)

    for start in range(0, len(file_updates), 50):
        batch = file_updates[start : start + 50]
        summary["media_updates_attempted"] += len(batch)
        response = client.update_files(batch)
        errors = []
        for item in response.get("userErrors") or []:
            prefix = " / ".join(item.get("field") or [])
            errors.append(f"{prefix}: {clean(item.get('message'))}" if prefix else clean(item.get("message")))
        if errors:
            summary["media_update_errors"].append({"count": len(batch), "errors": errors})
        else:
            summary["media_updates_applied"] += len(batch)
        if pause_ms > 0:
            time.sleep(pause_ms / 1000.0)
    return summary


def run_autofill(
    *,
    store_domain: str = "",
    access_token: str = "",
    handle: str = "",
    product_id: str = "",
    output_dir: Path | None = DEFAULT_OUTPUT_DIR,
    min_confidence: str = "high",
    execute: bool = False,
    pause_ms: int = 250,
) -> dict[str, Any]:
    resolved_output_dir = Path(output_dir) if output_dir is not None else None
    if resolved_output_dir is not None:
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(
        resolve_store_domain(store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(access_token),
    )
    product = client.fetch_product(handle=handle, product_gid=product_id)
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
    extra_refs_by_field = {
        field: client.fetch_metaobjects(config["metaobject_type"])
        for field, config in SHOPIFY_EXTRA_FIELD_CONFIG.items()
    }
    apparel_plans = plan_apparel_updates(
        product,
        custom_values=custom_values,
        refs_by_field=refs_by_field,
        min_confidence=min_confidence,
    )
    extra_category_plans = plan_extra_category_updates(
        product,
        custom_values=custom_values,
        refs_by_field=extra_refs_by_field,
        min_confidence=min_confidence,
    )
    media_plans = plan_media_updates(product)
    execution = apply_execution_plan(
        client,
        product=product,
        product_update_plan=product_update_plan,
        apparel_plans=apparel_plans,
        extra_category_plans=extra_category_plans,
        media_plans=media_plans,
        execute=execute,
        pause_ms=max(pause_ms, 0),
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
            "current_tags": "|".join(product.tags),
            "target_tags": "|".join(product_update_plan.tags or []),
        }
    ]
    apparel_rows = [asdict(item) for item in apparel_plans]
    extra_category_rows = [asdict(item) for item in extra_category_plans]
    media_rows = [asdict(item) for item in media_plans]

    summary = {
        "handle": product.handle,
        "product_id": product.product_id,
        "product_update_payload": build_product_update_payload(product, product_update_plan),
        "planned_custom_updates": len(product_update_plan.custom_values or {}),
        "planned_tag_update": 1 if product_update_plan.tags else 0,
        "planned_apparel_updates": sum(1 for item in apparel_plans if item.status == "plan"),
        "planned_extra_category_updates": sum(1 for item in extra_category_plans if item.status == "plan"),
        "planned_media_updates": sum(1 for item in media_plans if item.status == "plan"),
        "execution": execution,
    }

    if resolved_output_dir is not None:
        write_csv(
            resolved_output_dir / "product_update_plan.csv",
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
                "current_tags",
                "target_tags",
            ],
        )
        write_csv(
            resolved_output_dir / "apparel_field_plan.csv",
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
        write_csv(
            resolved_output_dir / "extra_category_field_plan.csv",
            extra_category_rows,
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
        write_csv(
            resolved_output_dir / "media_seo_plan.csv",
            media_rows,
            [
                "media_id",
                "current_alt",
                "target_alt",
                "current_filename",
                "target_filename",
                "status",
                "reason",
            ],
        )
        (resolved_output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

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

    summary = run_autofill(
        store_domain=args.store_domain,
        access_token=args.access_token,
        handle=args.handle,
        product_id=args.product_id,
        output_dir=Path(args.output_dir),
        min_confidence=args.min_confidence,
        execute=args.execute,
        pause_ms=max(args.pause_ms, 0),
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
