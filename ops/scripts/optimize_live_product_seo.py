#!/usr/bin/env python3
"""Optimize live Shopify product SEO, media alt text, and taxonomy metafields.

Default mode is dry-run.

Live updates require one of:
  - SHOPIFY_ADMIN_ACCESS_TOKEN
  - ~/.config/dresslikemommy/translation-helper-token.json

The script fetches active products sorted by total inventory so the highest-stock
products are planned and updated first.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "tmp" / "product-seo-optimization"
DEFAULT_TOKEN_PATH = Path.home() / ".config" / "dresslikemommy" / "translation-helper-token.json"
DEFAULT_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
DEFAULT_API_VERSION = os.environ.get(
    "SHOPIFY_ADMIN_API_VERSION",
    os.environ.get("SHOPIFY_API_VERSION", "2026-01"),
)
DEFAULT_PRODUCT_QUERY = "status:active"
DEFAULT_PAGE_SIZE = 15
DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_SLEEP_SECONDS = 0.12
BRAND_SUFFIX = "Dress Like Mommy"
MEDIA_ALT_MAX_LENGTH = 125

PRODUCTS_QUERY = """
query ProductsForSeoOptimization(
  $first: Int!
  $after: String
  $query: String
) {
  products(
    first: $first
    after: $after
    query: $query
    sortKey: INVENTORY_TOTAL
    reverse: true
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      handle
      title
      status
      totalInventory
      productType
      tags
      descriptionHtml
      seo {
        title
        description
      }
      typeField: metafield(namespace: "custom", key: "type") {
        id
        type
        value
      }
      styleField: metafield(namespace: "custom", key: "style") {
        id
        type
        value
      }
      patternField: metafield(namespace: "custom", key: "pattern") {
        id
        type
        value
      }
      media(first: 250) {
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
    }
  }
}
"""

PRODUCT_UPDATE_MUTATION = """
mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      seo {
        title
        description
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

TRUE_VALUES = {"1", "true", "yes", "y"}
LOWERCASE_TITLE_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "in",
    "me",
    "of",
    "on",
    "or",
    "the",
    "to",
    "up",
    "with",
}

AUDIENCE_RULES: Sequence[Tuple[str, Sequence[str], str, str, str]] = (
    ("maternity", (" maternity ", " pregnant ", " pregnancy ", " breastfeeding "), "Maternity", "moms-to-be", "Maternity"),
    ("couples", (" couple ", " couples ", " husband ", " wife ", " boyfriend ", " girlfriend ", " bonnie ", " clyde ", " yin and yang ", " lo ve "), "Matching Couple", "couples", "Couples"),
    ("daddy", (" daddy ", " dad ", " father ", " son ", " boys ", " boy "), "Daddy and Me", "dads and kids", "Daddy and Me"),
    ("mommy", (" mommy ", " mom ", " mother ", " daughter ", " girl ", " girls ", " mom child ", " mom and child "), "Mommy and Me", "moms and daughters", "Mommy and Me"),
    ("family", (" family ", " families ", " family matching ", " family outfit ", " family outfits ", " family set ", " parents and kids ", " whole family "), "Family Matching", "parents and kids", "Family Matching"),
)

STYLE_RULES: Sequence[Tuple[Tuple[str, ...], str, str, str]] = (
    (("swim trunk", "swim trunks", " trunks "), "Swim Trunks", "Trunks", "Swimwear"),
    (("one-piece swimsuit", "one piece swimsuit", "one-piece swim", " one piece "), "One-Piece Swimsuits", "Swimsuits", "Swimwear"),
    (("bikini", "two-piece swimsuit", "two piece swimsuit", "2-piece swimsuit", "2 piece swimsuit"), "Bikini Sets", "Bikinis", "Swimwear"),
    (("tankini",), "Tankinis", "Tankinis", "Swimwear"),
    (("swimsuit", "swimwear", "bathing suit", "rash guard"), "Swimsuits", "Swimsuits", "Swimwear"),
    (("nightgown",), "Nightgowns", "Nightgowns", "Pajamas"),
    (("robe",), "Robes", "Robes", "Pajamas"),
    (("loungewear",), "Loungewear Sets", "Loungewear", "Pajamas"),
    (("pajama", "sleepwear", " pajamas ", " pjs "), "Pajama Sets", "Pajamas", "Pajamas"),
    (("outfit", "matching set", " family set ", " set for ", " outfit set "), "Matching Sets", "Outfits", "Sets"),
    (("button-down", "button down"), "Button-Down Shirts", "Shirts", "Tops"),
    (("t-shirt", "t shirts", "t shirt", "tee shirt", " tee "), "T-Shirts", "T-Shirts", "Tops"),
    (("blouse",), "Blouses", "Blouses", "Tops"),
    (("hoodie",), "Hoodies", "Hoodies", "Tops"),
    (("shirt", " top ", " tops "), "Shirts", "Tops", "Tops"),
    (("cardigan",), "Cardigans", "Cardigans", "Sweaters"),
    (("sweatshirt",), "Sweatshirts", "Sweatshirts", "Sweaters"),
    (("sweater", "pullover"), "Sweaters", "Sweaters", "Sweaters"),
    (("faux leather jacket", "leather jacket"), "Jackets", "Jackets", "Coats"),
    (("puffer jacket", " jacket "), "Jackets", "Jackets", "Coats"),
    (("coat", "outerwear", "parka", "puffer"), "Coats", "Coats", "Coats"),
    (("romper",), "Rompers", "Rompers", "Jumpsuits"),
    (("jumpsuit", " jumper "), "Jumpsuits", "Jumpsuits", "Jumpsuits"),
    (("maxi dress",), "Maxi Dresses", "Dresses", "Dresses"),
    (("midi dress",), "Midi Dresses", "Dresses", "Dresses"),
    (("mini dress",), "Mini Dresses", "Dresses", "Dresses"),
    (("sundress",), "Sundresses", "Dresses", "Dresses"),
    (("dress", " gown "), "Dresses", "Dresses", "Dresses"),
)

PATTERN_RULES: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("chevron",), "Chevron"),
    (("gingham",), "Gingham"),
    (("plaid", "checkered", "tartan"), "Plaid"),
    (("striped", "stripe"), "Striped"),
    (("polka",), "Polka Dot"),
    (("leopard", "zebra", "animal print", "cow print"), "Animal Print"),
    (("floral", "flower"), "Floral"),
    (("cartoon", "bear", "chick", "character"), "Cartoon"),
    (("heart patch", " heart "), "Heart"),
    (("christmas", "holiday", "reindeer", "gnome", "snowflake", "merry christmas"), "Christmas"),
    (("halloween", "pumpkin", "ghost", "bat"), "Halloween"),
    (("tropical", "palm", "leaf print", "leaves print", " leaf ", " leaves "), "Tropical"),
    (("tie dye", "tie-dye"), "Tie-Dye"),
    (("color block", "colour block"), "Color Block"),
    (("graphic", "bonnie", "clyde", "letter print", "slogan"), "Graphic"),
)

SPECIAL_FEATURE_RULES: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("bonnie", "clyde"), "Bonnie & Clyde Graphic"),
    (("mr and mrs", "mr mrs"), "Mr & Mrs Graphic"),
    (("queen king",), "Queen King Graphic"),
    (("yin and yang", "yin yang"), "Yin Yang Graphic"),
    ((" lo ve ",), "Love Graphic"),
    (("faux leather", "leather"), "Faux Leather"),
    (("fleece",), "Fleece"),
    (("mermaid scale", "mermaid scales"), "Mermaid Scale"),
    (("watercolor",), "Watercolor"),
    (("ombre", "gradient"), "Ombre"),
    (("rainbow striped", "rainbow stripe", "rainbow-themed", "rainbow themed"), "Rainbow Stripe"),
    (("plaid flannel", "flannel"), "Plaid Flannel"),
    (("one shoulder", "one-shoulder"), "One Shoulder"),
    (("heart patch",), "Heart Patch"),
    (("wrap skirt",), "Wrap Skirt"),
    (("cartoon", "bear", "chick"), "Cartoon Print"),
    (("ruffle", "ruffled"), "Ruffle Sleeve"),
    (("button-down", "button down"), "Button-Down"),
    (("zip-up", "zip up", "full-zip"), "Zip-Up"),
    (("hooded", "hoodie"), "Hooded"),
    (("long sleeve",), "Long Sleeve"),
    (("short sleeve",), "Short Sleeve"),
    (("one-piece", "one piece"), "One-Piece"),
)

COLOR_RULES: Sequence[Tuple[str, str]] = (
    ("black", "Black"),
    ("white", "White"),
    ("green", "Green"),
    ("pink", "Pink"),
    ("orange", "Orange"),
    ("blue", "Blue"),
    ("red", "Red"),
    ("yellow", "Yellow"),
    ("purple", "Purple"),
    ("brown", "Brown"),
    ("beige", "Beige"),
    ("cream", "Cream"),
    ("khaki", "Khaki"),
    ("gray", "Gray"),
    ("grey", "Gray"),
    ("navy", "Navy"),
    ("gold", "Gold"),
    ("silver", "Silver"),
)

PATTERN_FEATURE_MAP = {
    "Chevron": "Chevron Print",
    "Gingham": "Gingham Print",
    "Plaid": "Plaid Print",
    "Striped": "Striped",
    "Polka Dot": "Polka Dot Print",
    "Animal Print": "Animal Print",
    "Floral": "Floral Print",
    "Cartoon": "Cartoon Print",
    "Heart": "Heart Print",
    "Christmas": "Christmas Print",
    "Halloween": "Halloween Print",
    "Tropical": "Tropical Print",
    "Tie-Dye": "Tie-Dye Print",
    "Color Block": "Color Block",
    "Graphic": "Graphic Print",
}

OCCASION_BY_TYPE = {
    "Swimwear": "beach days, pool parties, and vacations",
    "Pajamas": "bedtime, sleepovers, and cozy family nights",
    "Dresses": "family photos, parties, and everyday matching moments",
    "Tops": "casual days, coordinated outings, and matching photos",
    "Sweaters": "cozy days, holiday moments, and family photos",
    "Coats": "cool-weather outings and matching family photos",
    "Sets": "easy coordinated looks, vacations, and family photos",
    "Jumpsuits": "playdates, outings, and photo-ready matching moments",
}

ALT_LEADS = (
    "Product image of",
    "Alternate image of",
    "Additional image of",
    "Detail image of",
    "Close product view of",
    "Extra image of",
)

HIGH_PRIORITY_SPECIAL_FEATURES = {
    "Bonnie & Clyde Graphic",
    "Mr & Mrs Graphic",
    "Queen King Graphic",
    "Yin Yang Graphic",
    "Love Graphic",
    "Faux Leather",
    "Fleece",
    "Mermaid Scale",
    "Watercolor",
    "Ombre",
    "Rainbow Stripe",
    "Plaid Flannel",
    "One Shoulder",
    "Heart Patch",
    "Wrap Skirt",
    "Cartoon Print",
}


@dataclass
class MediaImage:
    id: str
    alt: str
    url: str
    position: int


@dataclass
class ProductRecord:
    id: str
    handle: str
    title: str
    status: str
    total_inventory: int
    product_type: str
    tags: List[str]
    description_html: str
    seo_title: str
    seo_description: str
    current_type: str
    current_style: str
    current_pattern: str
    media: List[MediaImage] = field(default_factory=list)


@dataclass
class GeneratedSeo:
    source_title: str
    audience_title: str
    audience_people: str
    audience_metafield: str
    style: str
    compact_style: str
    product_type: str
    pattern: str
    feature: str
    seo_title: str
    seo_description: str


@dataclass
class ProductPlan:
    product: ProductRecord
    generated: GeneratedSeo
    needs_product_update: bool
    media_updates: List[Tuple[MediaImage, str]]


def clean(value: object) -> str:
    return str(value or "").strip()


def normalized_key(value: object) -> str:
    return clean(value).lower()


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", clean(value)).strip()


def parse_bool(value: str) -> bool:
    return normalized_key(value) in TRUE_VALUES


def title_case_phrase(value: str) -> str:
    words = normalize_spaces(value).split(" ")
    output: List[str] = []
    for index, word in enumerate(words):
        token = word.lower()
        if index and token in LOWERCASE_TITLE_WORDS:
            output.append(token)
            continue
        if token in {"dlm", "usa"}:
            output.append(token.upper())
            continue
        if token == "&":
            output.append("&")
            continue
        output.append(token.capitalize())
    return " ".join(output).strip()


def humanize_handle(handle: str) -> str:
    text = clean(handle).replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    return title_case_phrase(text)


def html_to_text(raw_html: str) -> str:
    text = clean(raw_html)
    if not text:
        return ""
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return normalize_spaces(text)


def normalize_source_title(title: str, handle: str) -> str:
    text = normalize_spaces(title)
    text = re.sub(r"\s*\|\s*(dlm|dress like mommy)\b.*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\.{3,}", " ", text)
    text = normalize_spaces(text).strip(" -:|,.;")
    if len(text) < 12 or "..." in title:
        handle_title = humanize_handle(handle)
        if handle_title:
            return handle_title
    return text or humanize_handle(handle)


def trim_to_length(text: str, max_length: int) -> str:
    output = normalize_spaces(text)
    if len(output) <= max_length:
        return output
    shortened = output[:max_length].rstrip()
    if " " in shortened:
        shortened = shortened.rsplit(" ", 1)[0]
    return shortened.strip(" -:|,.;")


def comparable_text(value: str) -> str:
    text = normalized_key(value)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return normalize_spaces(text)


def contains_any(blob: str, tokens: Sequence[str]) -> bool:
    return any(token in blob for token in tokens)


def detect_audience(blob: str) -> Tuple[str, str, str]:
    family_tokens = (
        " family ",
        " families ",
        " family matching ",
        " family outfit ",
        " family outfits ",
        " family set ",
        " whole family ",
        " parents and kids ",
    )
    for key, tokens, title_label, people_label, metafield_value in AUDIENCE_RULES:
        if key in {"maternity", "couples"} and contains_any(blob, tokens):
            return title_label, people_label, metafield_value
    if contains_any(blob, family_tokens):
        return "Family Matching", "parents and kids", "Family Matching"
    for key, tokens, title_label, people_label, metafield_value in AUDIENCE_RULES:
        if key in {"maternity", "couples", "family"}:
            continue
        if contains_any(blob, tokens):
            return title_label, people_label, metafield_value
    return "Mommy and Me", "moms and daughters", "Mommy and Me"


def detect_style_and_type(blob: str) -> Tuple[str, str, str]:
    for tokens, style, compact_style, product_type in STYLE_RULES:
        if contains_any(blob, tokens):
            return style, compact_style, product_type
    return "Matching Sets", "Outfits", "Sets"


def detect_pattern(blob: str) -> str:
    for tokens, pattern in PATTERN_RULES:
        if contains_any(blob, tokens):
            return pattern
    return "Solid"


def detect_special_feature(blob: str) -> str:
    for tokens, feature in SPECIAL_FEATURE_RULES:
        if contains_any(blob, tokens):
            return feature
    return ""


def detect_colors(title_blob: str) -> List[str]:
    matches: List[Tuple[int, str]] = []
    for token, label in COLOR_RULES:
        marker = f" {token} "
        position = title_blob.find(marker)
        if position >= 0:
            matches.append((position, label))

    output: List[str] = []
    for _, label in sorted(matches, key=lambda item: item[0]):
        if label not in output:
            output.append(label)
    return output


def pattern_feature(pattern: str) -> str:
    return PATTERN_FEATURE_MAP.get(pattern, pattern)


def compact_color_phrase(colors: Sequence[str], *, prefer_one: bool) -> str:
    if not colors:
        return ""
    if prefer_one or len(colors[0]) + (len(colors[1]) if len(colors) > 1 else 0) > 16:
        return colors[0]
    if len(colors) == 1:
        return colors[0]
    return " ".join(colors[:2])


def build_feature_phrase(
    *,
    pattern: str,
    special_feature: str,
    colors: Sequence[str],
) -> str:
    feature = clean(special_feature)
    color_phrase = compact_color_phrase(colors, prefer_one=bool(feature))
    if feature in HIGH_PRIORITY_SPECIAL_FEATURES:
        if feature == "Rainbow Stripe":
            return feature
        if feature == "Ombre" and colors:
            ombre_colors = " ".join(colors[:2]) if len(colors) > 1 else colors[0]
            candidate = f"{ombre_colors} Ombre"
            if len(candidate) <= 28:
                return candidate
        if color_phrase and feature in {"Faux Leather", "Fleece"}:
            candidate = f"{color_phrase} {feature}"
            if len(candidate) <= 28:
                return candidate
        return feature

    if pattern != "Solid":
        pattern_phrase = pattern_feature(pattern)
        if color_phrase:
            candidate = f"{color_phrase} {pattern_phrase}"
            if len(candidate) <= 28:
                return candidate
            return f"{colors[0]} {pattern_phrase}" if colors else pattern_phrase
        return pattern_phrase

    if color_phrase:
        return color_phrase
    if feature:
        return feature
    return "Matching Style"


def feature_fallbacks(feature: str, pattern: str, colors: Sequence[str]) -> List[str]:
    output: List[str] = []
    color_pattern = ""
    if pattern != "Solid" and colors:
        color_base = compact_color_phrase(colors, prefer_one=False)
        color_pattern = f"{color_base} {pattern}".strip()
    for candidate in (
        clean(feature),
        color_pattern,
        pattern_feature(pattern) if pattern != "Solid" else "",
        compact_color_phrase(colors, prefer_one=False),
        colors[0] if colors else "",
        "Matching",
        "",
    ):
        token = clean(candidate)
        if token not in output:
            output.append(token)
    return output


def audience_fallbacks(audience_title: str) -> List[str]:
    replacements = {
        "Mommy and Me": ["Mommy and Me", "Mommy & Me"],
        "Daddy and Me": ["Daddy and Me", "Daddy & Me"],
        "Family Matching": ["Family Matching", "Matching Family"],
        "Matching Couple": ["Matching Couple", "Couple Matching"],
        "Maternity": ["Maternity"],
    }
    return replacements.get(audience_title, [audience_title])


def style_fallbacks(style: str, compact_style: str, product_type: str) -> List[str]:
    output: List[str] = []
    for candidate in (style, compact_style, product_type):
        token = clean(candidate)
        if token and token not in output:
            output.append(token)
    return output


def keyword_phrase(audience_title: str, style: str) -> str:
    audience = clean(audience_title)
    style_value = clean(style)
    if audience == "Family Matching" and style_value == "Matching Sets":
        return "Family Matching Sets"
    if audience.lower().endswith("matching") and style_value.lower().startswith("matching "):
        return f"{audience} {style_value[9:]}"
    return f"{audience} {style_value}".strip()


def build_seo_title(
    *,
    audience_title: str,
    style: str,
    compact_style: str,
    product_type: str,
    feature: str,
    pattern: str,
    colors: Sequence[str],
) -> str:
    suffix = f" | {BRAND_SUFFIX}"
    for audience_candidate in audience_fallbacks(audience_title):
        for style_candidate in style_fallbacks(style, compact_style, product_type):
            prefix = keyword_phrase(audience_candidate, style_candidate)
            for feature_candidate in feature_fallbacks(feature, pattern, colors):
                if feature_candidate:
                    candidate = f"{prefix} - {feature_candidate}{suffix}"
                else:
                    candidate = f"{prefix}{suffix}"
                if len(candidate) <= 70:
                    return candidate
    fallback_prefix = trim_to_length(f"{audience_title} {compact_style}".strip(), 70 - len(suffix))
    return f"{fallback_prefix}{suffix}"


def build_seo_description(
    *,
    audience_title: str,
    people_label: str,
    style: str,
    product_type: str,
    feature: str,
) -> str:
    feature_text = feature.lower() if feature else "coordinated matching style"
    occasion = OCCASION_BY_TYPE.get(product_type, "matching moments and family photos")
    subject = keyword_phrase(audience_title.lower(), style.lower())
    intro = (
        f"Shop {subject} for {people_label} featuring "
        f"{feature_text}."
    )
    middle = f" Perfect for {occasion}."
    closing = f" Shop now at {BRAND_SUFFIX}. Free shipping + 30-day returns."
    combined = normalize_spaces(f"{intro}{middle}{closing}")
    if len(combined) <= 320:
        return combined

    variants = [
        normalize_spaces(
            f"Shop {subject} for {people_label} with {feature_text}. "
            f"Perfect for {occasion}. Shop now at {BRAND_SUFFIX}. Free shipping + 30-day returns."
        ),
        normalize_spaces(
            f"Shop {subject} with {feature_text}. "
            f"Great for {occasion}. Shop now at {BRAND_SUFFIX}. Free shipping + 30-day returns."
        ),
    ]
    for candidate in variants:
        if len(candidate) <= 320:
            return candidate
    return trim_to_length(variants[-1], 320)


def build_media_alt_texts(
    *,
    audience_title: str,
    style: str,
    feature: str,
    media_count: int,
) -> List[str]:
    subject = f"{audience_title.lower()} {style.lower()}".strip()
    detail = feature.lower() if feature else "matching style"
    output: List[str] = []
    for index in range(media_count):
        lead = ALT_LEADS[index % len(ALT_LEADS)]
        if media_count == 1:
            lead = "Product image of"
        phrase = f"{lead} {subject} with {detail}"
        output.append(trim_to_length(phrase, MEDIA_ALT_MAX_LENGTH))
    return output


def should_replace_alt_text(
    *,
    current_alt: str,
    product_title: str,
    source_title: str,
    duplicate_count: int,
) -> bool:
    alt = clean(current_alt)
    if not alt:
        return True

    comparable_alt = comparable_text(alt)
    comparable_product_title = comparable_text(product_title)
    comparable_source_title = comparable_text(source_title)

    if "dresslikemommy" in normalized_key(alt):
        return True
    if comparable_alt in {comparable_product_title, comparable_source_title}:
        return True
    if comparable_source_title and comparable_alt.startswith(comparable_source_title):
        remainder = comparable_alt[len(comparable_source_title) :].strip()
        if not remainder or len(remainder.split(" ")) <= 4:
            return True
    if duplicate_count > 1 and len(comparable_alt.split(" ")) <= 12:
        return True
    return False


def build_blob(parts: Sequence[str]) -> str:
    normalized = " ".join(part.lower() for part in parts if clean(part))
    normalized = re.sub(r"[^a-z0-9&]+", " ", normalized)
    return f" {normalize_spaces(normalized)} "


def build_primary_blob(product: ProductRecord, source_title: str) -> str:
    parts = [
        source_title,
        product.handle.replace("-", " "),
        product.product_type,
        " ".join(product.tags),
    ]
    return build_blob(parts)


def build_full_blob(product: ProductRecord, source_title: str) -> str:
    description_text = html_to_text(product.description_html)
    description_excerpt = trim_to_length(description_text, 600)
    return build_blob(
        [
            source_title,
            product.handle.replace("-", " "),
            product.product_type,
            " ".join(product.tags),
            description_excerpt,
        ]
    )


def generate_product_seo(product: ProductRecord) -> GeneratedSeo:
    source_title = normalize_source_title(product.title, product.handle)
    primary_blob = build_primary_blob(product, source_title)
    full_blob = build_full_blob(product, source_title)
    title_blob = f" {normalize_spaces(source_title.lower())} "

    audience_title, people_label, audience_metafield = detect_audience(primary_blob)
    style, compact_style, product_type = detect_style_and_type(primary_blob)
    if style == "Matching Sets" and " outfit " not in primary_blob and " set " not in primary_blob:
        style, compact_style, product_type = detect_style_and_type(full_blob)

    pattern = detect_pattern(primary_blob)
    if pattern == "Solid":
        pattern = detect_pattern(full_blob)

    special_feature = detect_special_feature(primary_blob)
    if not special_feature:
        special_feature = detect_special_feature(full_blob)

    colors = detect_colors(title_blob)
    feature = build_feature_phrase(
        pattern=pattern,
        special_feature=special_feature,
        colors=colors,
    )

    seo_title = build_seo_title(
        audience_title=audience_title,
        style=style,
        compact_style=compact_style,
        product_type=product_type,
        feature=feature,
        pattern=pattern,
        colors=colors,
    )
    seo_description = build_seo_description(
        audience_title=audience_title,
        people_label=people_label,
        style=style,
        product_type=product_type,
        feature=feature,
    )

    return GeneratedSeo(
        source_title=source_title,
        audience_title=audience_title,
        audience_people=people_label,
        audience_metafield=audience_metafield,
        style=style,
        compact_style=compact_style,
        product_type=product_type,
        pattern=pattern,
        feature=feature,
        seo_title=seo_title,
        seo_description=seo_description,
    )


def chunked(values: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


class ShopifyClient:
    def __init__(
        self,
        *,
        store_domain: str,
        access_token: str,
        api_version: str,
        timeout_seconds: int,
    ) -> None:
        self.store_domain = clean(store_domain)
        self.access_token = clean(access_token)
        self.api_version = clean(api_version)
        self.timeout_seconds = timeout_seconds
        self.endpoint = f"https://{self.store_domain}/admin/api/{self.api_version}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            }
        )

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        for attempt in range(1, 7):
            response = self.session.post(
                self.endpoint,
                json={"query": query, "variables": variables or {}},
                timeout=self.timeout_seconds,
            )
            if response.status_code == 429 and attempt < 6:
                time.sleep(min(12.0, (1.4 ** attempt) + random.uniform(0.2, 0.8)))
                continue
            response.raise_for_status()
            payload = response.json()
            errors = payload.get("errors") or []
            if not errors:
                return payload.get("data", {})
            codes = {item.get("extensions", {}).get("code") for item in errors}
            if "THROTTLED" in codes and attempt < 6:
                time.sleep(min(12.0, (1.4 ** attempt) + random.uniform(0.2, 0.8)))
                continue
            raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(errors, ensure_ascii=False)}")
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def iter_products(
        self,
        *,
        product_query: str,
        page_size: int,
        max_products: int,
    ) -> Iterable[ProductRecord]:
        cursor: Optional[str] = None
        seen = 0
        while True:
            data = self.graphql(
                PRODUCTS_QUERY,
                {"first": page_size, "after": cursor, "query": product_query or None},
            )
            root = data["products"]
            for node in root.get("nodes", []):
                if clean(node.get("status")) != "ACTIVE":
                    continue
                media_nodes = []
                for index, media_node in enumerate((node.get("media") or {}).get("nodes") or [], start=1):
                    if media_node.get("__typename") != "MediaImage":
                        continue
                    media_nodes.append(
                        MediaImage(
                            id=clean(media_node.get("id")),
                            alt=clean(media_node.get("alt")),
                            url=clean((media_node.get("image") or {}).get("url")),
                            position=index,
                        )
                    )
                yield ProductRecord(
                    id=clean(node.get("id")),
                    handle=clean(node.get("handle")),
                    title=clean(node.get("title")),
                    status=clean(node.get("status")),
                    total_inventory=int(node.get("totalInventory") or 0),
                    product_type=clean(node.get("productType")),
                    tags=[clean(tag) for tag in node.get("tags") or [] if clean(tag)],
                    description_html=clean(node.get("descriptionHtml")),
                    seo_title=clean(((node.get("seo") or {}).get("title"))),
                    seo_description=clean(((node.get("seo") or {}).get("description"))),
                    current_type=clean(((node.get("typeField") or {}).get("value"))),
                    current_style=clean(((node.get("styleField") or {}).get("value"))),
                    current_pattern=clean(((node.get("patternField") or {}).get("value"))),
                    media=media_nodes,
                )
                seen += 1
                if max_products and seen >= max_products:
                    return
            if not root["pageInfo"]["hasNextPage"]:
                return
            cursor = root["pageInfo"]["endCursor"]

    def update_product(self, product_payload: Dict[str, Any]) -> Dict[str, Any]:
        data = self.graphql(PRODUCT_UPDATE_MUTATION, {"product": product_payload})
        return data["productUpdate"]

    def update_files(self, files_payload: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        data = self.graphql(FILE_UPDATE_MUTATION, {"files": list(files_payload)})
        return data["fileUpdate"]


def load_access_token(token_path: Path) -> str:
    env_token = clean(os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    if env_token:
        return env_token
    if not token_path.exists():
        raise FileNotFoundError(
            "Missing Shopify token. Set SHOPIFY_ADMIN_ACCESS_TOKEN or create "
            f"{token_path}"
        )
    payload = json.loads(token_path.read_text(encoding="utf-8"))
    token = clean(payload.get("access_token"))
    if not token:
        raise RuntimeError(f"Token file does not contain access_token: {token_path}")
    return token


def build_plan(products: Sequence[ProductRecord]) -> List[ProductPlan]:
    plans: List[ProductPlan] = []
    for product in products:
        generated = generate_product_seo(product)
        media_updates: List[Tuple[MediaImage, str]] = []
        comparable_alt_counts: Dict[str, int] = {}
        for media in product.media:
            comparable_alt = comparable_text(media.alt)
            if not comparable_alt:
                continue
            comparable_alt_counts[comparable_alt] = comparable_alt_counts.get(comparable_alt, 0) + 1
        planned_alt_texts = build_media_alt_texts(
            audience_title=generated.audience_title,
            style=generated.style,
            feature=generated.feature,
            media_count=len(product.media),
        )
        for media, new_alt in zip(product.media, planned_alt_texts):
            comparable_alt = comparable_text(media.alt)
            duplicate_count = comparable_alt_counts.get(comparable_alt, 0) if comparable_alt else 0
            if not should_replace_alt_text(
                current_alt=media.alt,
                product_title=product.title,
                source_title=generated.source_title,
                duplicate_count=duplicate_count,
            ):
                continue
            if normalize_spaces(media.alt) != normalize_spaces(new_alt):
                media_updates.append((media, new_alt))

        needs_product_update = any(
            [
                normalize_spaces(product.seo_title) != normalize_spaces(generated.seo_title),
                normalize_spaces(product.seo_description) != normalize_spaces(generated.seo_description),
                normalize_spaces(product.current_type) != normalize_spaces(generated.product_type),
                normalize_spaces(product.current_style) != normalize_spaces(generated.style),
                normalize_spaces(product.current_pattern) != normalize_spaces(generated.pattern),
            ]
        )
        plans.append(
            ProductPlan(
                product=product,
                generated=generated,
                needs_product_update=needs_product_update,
                media_updates=media_updates,
            )
        )
    return plans


def write_plan_csv(path: Path, plans: Sequence[ProductPlan]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "inventory_rank",
                "handle",
                "title",
                "inventory",
                "current_seo_title",
                "new_seo_title",
                "current_seo_description",
                "new_seo_description",
                "current_type",
                "new_type",
                "current_style",
                "new_style",
                "current_pattern",
                "new_pattern",
                "feature",
                "media_updates",
            ],
        )
        writer.writeheader()
        for index, item in enumerate(plans, start=1):
            writer.writerow(
                {
                    "inventory_rank": index,
                    "handle": item.product.handle,
                    "title": item.product.title,
                    "inventory": item.product.total_inventory,
                    "current_seo_title": item.product.seo_title,
                    "new_seo_title": item.generated.seo_title,
                    "current_seo_description": item.product.seo_description,
                    "new_seo_description": item.generated.seo_description,
                    "current_type": item.product.current_type,
                    "new_type": item.generated.product_type,
                    "current_style": item.product.current_style,
                    "new_style": item.generated.style,
                    "current_pattern": item.product.current_pattern,
                    "new_pattern": item.generated.pattern,
                    "feature": item.generated.feature,
                    "media_updates": len(item.media_updates),
                }
            )


def write_summary_json(path: Path, plans: Sequence[ProductPlan], execution: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    product_changes = sum(1 for item in plans if item.needs_product_update)
    media_changes = sum(len(item.media_updates) for item in plans)
    payload = {
        "planned_products": len(plans),
        "planned_product_updates": product_changes,
        "planned_media_updates": media_changes,
        "executed": execution,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def execute_plan(
    client: ShopifyClient,
    plans: Sequence[ProductPlan],
    *,
    sleep_seconds: float,
    dry_run: bool,
) -> Dict[str, Any]:
    summary = {
        "product_updates_attempted": 0,
        "product_updates_applied": 0,
        "product_update_errors": [],
        "media_updates_attempted": 0,
        "media_updates_applied": 0,
        "media_update_errors": [],
    }

    if dry_run:
        return summary

    for item in plans:
        if item.needs_product_update:
            summary["product_updates_attempted"] += 1
            payload = {
                "id": item.product.id,
                "seo": {
                    "title": item.generated.seo_title,
                    "description": item.generated.seo_description,
                },
                "metafields": [
                    {
                        "namespace": "custom",
                        "key": "type",
                        "type": "single_line_text_field",
                        "value": item.generated.product_type,
                    },
                    {
                        "namespace": "custom",
                        "key": "style",
                        "type": "single_line_text_field",
                        "value": item.generated.style,
                    },
                    {
                        "namespace": "custom",
                        "key": "pattern",
                        "type": "single_line_text_field",
                        "value": item.generated.pattern,
                    },
                ],
            }
            try:
                response = client.update_product(payload)
            except Exception as exc:  # noqa: BLE001
                summary["product_update_errors"].append(
                    {"handle": item.product.handle, "error": str(exc)}
                )
            else:
                user_errors = response.get("userErrors") or []
                if user_errors:
                    summary["product_update_errors"].append(
                        {
                            "handle": item.product.handle,
                            "error": "; ".join(clean(entry.get("message")) for entry in user_errors),
                        }
                    )
                else:
                    summary["product_updates_applied"] += 1
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

        if item.media_updates:
            for batch in chunked(
                [
                    {"id": media.id, "alt": new_alt}
                    for media, new_alt in item.media_updates
                ],
                50,
            ):
                summary["media_updates_attempted"] += len(batch)
                try:
                    response = client.update_files(batch)
                except Exception as exc:  # noqa: BLE001
                    summary["media_update_errors"].append(
                        {"handle": item.product.handle, "error": str(exc), "count": len(batch)}
                    )
                else:
                    user_errors = response.get("userErrors") or []
                    if user_errors:
                        summary["media_update_errors"].append(
                            {
                                "handle": item.product.handle,
                                "error": "; ".join(clean(entry.get("message")) for entry in user_errors),
                                "count": len(batch),
                            }
                        )
                    else:
                        summary["media_updates_applied"] += len(batch)
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)

    return summary


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default=DEFAULT_STORE_DOMAIN)
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION)
    parser.add_argument("--product-query", default=DEFAULT_PRODUCT_QUERY)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--max-products", type=int, default=0)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--sleep-seconds", type=float, default=DEFAULT_SLEEP_SECONDS)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for plan/audit files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--token-path",
        type=Path,
        default=DEFAULT_TOKEN_PATH,
        help=f"Token file path (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Apply live Shopify updates. Default is dry-run.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    access_token = load_access_token(args.token_path)
    client = ShopifyClient(
        store_domain=args.store_domain,
        access_token=access_token,
        api_version=args.api_version,
        timeout_seconds=args.timeout_seconds,
    )

    products = list(
        client.iter_products(
            product_query=args.product_query,
            page_size=max(1, args.page_size),
            max_products=max(0, args.max_products),
        )
    )
    plans = build_plan(products)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    plan_csv = args.output_dir / "product_seo_plan.csv"
    summary_json = args.output_dir / "product_seo_summary.json"

    write_plan_csv(plan_csv, plans)
    execution = execute_plan(
        client,
        plans,
        sleep_seconds=max(0.0, args.sleep_seconds),
        dry_run=not args.execute,
    )
    write_summary_json(summary_json, plans, execution)

    product_updates = sum(1 for item in plans if item.needs_product_update)
    media_updates = sum(len(item.media_updates) for item in plans)

    print(f"mode={'execute' if args.execute else 'dry-run'}")
    print(f"products_scanned={len(plans)}")
    print(f"planned_product_updates={product_updates}")
    print(f"planned_media_updates={media_updates}")
    print(f"plan_csv={plan_csv}")
    print(f"summary_json={summary_json}")

    if args.execute:
        print(f"product_updates_applied={execution['product_updates_applied']}")
        print(f"media_updates_applied={execution['media_updates_applied']}")
        print(f"product_update_errors={len(execution['product_update_errors'])}")
        print(f"media_update_errors={len(execution['media_update_errors'])}")
        if execution["product_update_errors"] or execution["media_update_errors"]:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
