#!/usr/bin/env python3
"""Backfill product metadata fields in a Shopify CSV export.

By default this script updates only products with Status=active (case-insensitive).
It writes an import-ready CSV and a markdown coverage summary.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


ROW_HANDLE = "Handle"
ROW_STATUS = "Status"
ROW_PUBLISHED = "Published"
ROW_TITLE = "Title"
ROW_TAGS = "Tags"
ROW_TYPE = "Type"
ROW_IMAGE_SRC = "Image Src"
ROW_IMAGE_ALT = "Image Alt Text"
ROW_VARIANT_IMAGE = "Variant Image"
ROW_OPTION1_VALUE = "Option1 Value"
ROW_OPTION2_VALUE = "Option2 Value"
ROW_OPTION3_VALUE = "Option3 Value"
ROW_OPTION1_NAME = "Option1 Name"
ROW_OPTION2_NAME = "Option2 Name"
ROW_OPTION3_NAME = "Option3 Name"
ROW_VARIANT_SKU = "Variant SKU"
ROW_VARIANT_BARCODE = "Variant Barcode"
ROW_GOOGLE_MPN = "Google Shopping / MPN"
ROW_GOOGLE_CUSTOM_PRODUCT = "Google Shopping / Custom Product"
ROW_GOOGLE_CONDITION = "Google Shopping / Condition"
ROW_GOOGLE_GENDER = "Google Shopping / Gender"
ROW_GOOGLE_AGE_GROUP = "Google Shopping / Age Group"

PRODUCT_SEO_TITLE = "SEO Title"
PRODUCT_SEO_DESCRIPTION = "SEO Description"
PRODUCT_GOOGLE_CATEGORY = "Google Shopping / Google Product Category"
PRODUCT_CATEGORY1 = "Category1 (product.metafields.custom.category1)"
PRODUCT_SUBCATEGORY = "SubCategory (product.metafields.custom.subcategory)"
PRODUCT_SUBCATEGORY2 = "SubCategory2 (product.metafields.custom.subcategory2)"
PRODUCT_TYPE = "Type (product.metafields.custom.type)"
PRODUCT_STYLE = "Style (product.metafields.custom.style)"
PRODUCT_PATTERN = "Pattern (product.metafields.custom.pattern)"
PRODUCT_DISCOVERY_COMPLEMENTARY = (
    "Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products)"
)
PRODUCT_DISCOVERY_RELATED_SETTINGS = (
    "Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display)"
)
PRODUCT_DISCOVERY_RELATED = (
    "Related products (product.metafields.shopify--discovery--product_recommendation.related_products)"
)
PRODUCT_SEARCH_BOOSTS = (
    "Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries)"
)
PRODUCT_GOOGLE_CUSTOM_METAFIELD = (
    "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)"
)
PRODUCT_SHOPIFY_AGE_GROUP = "Age group (product.metafields.shopify.age-group)"
PRODUCT_SHOPIFY_COLOR = "Color (product.metafields.shopify.color-pattern)"
GOOGLE_CATEGORY_GIFT_CARD = (
    "Arts & Entertainment > Party & Celebration > Gift Giving > Gift Cards & Certificates"
)

ACTIVE_STATUS = "active"
RELATED_SETTINGS_MANUAL = "only manual"
DEFAULT_BRAND_SUFFIX = "Dress Like Mommy"
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
VALID_GENDER_VALUES = {"female", "male", "unisex"}
VALID_AGE_GROUP_VALUES = {"newborn", "infant", "toddler", "kids", "adult"}
TAXONOMY_TAG_PREFIXES = (
    "category1:",
    "subcategory:",
    "subcategory2:",
    "type:",
    "style:",
    "pattern:",
)

OVERRIDE_COLUMN_ALIASES: Dict[str, Sequence[str]] = {
    PRODUCT_SEO_TITLE: (PRODUCT_SEO_TITLE, "seo_title"),
    PRODUCT_SEO_DESCRIPTION: (PRODUCT_SEO_DESCRIPTION, "seo_description"),
    PRODUCT_GOOGLE_CATEGORY: (PRODUCT_GOOGLE_CATEGORY, "google_category"),
    PRODUCT_CATEGORY1: (PRODUCT_CATEGORY1, "category1"),
    PRODUCT_SUBCATEGORY: (PRODUCT_SUBCATEGORY, "subcategory"),
    PRODUCT_SUBCATEGORY2: (PRODUCT_SUBCATEGORY2, "subcategory2"),
    PRODUCT_TYPE: (PRODUCT_TYPE, "type"),
    PRODUCT_STYLE: (PRODUCT_STYLE, "style"),
    PRODUCT_PATTERN: (PRODUCT_PATTERN, "pattern"),
    PRODUCT_DISCOVERY_COMPLEMENTARY: (
        PRODUCT_DISCOVERY_COMPLEMENTARY,
        "complementary_products",
    ),
    PRODUCT_DISCOVERY_RELATED_SETTINGS: (
        PRODUCT_DISCOVERY_RELATED_SETTINGS,
        "related_products_settings",
    ),
    PRODUCT_DISCOVERY_RELATED: (PRODUCT_DISCOVERY_RELATED, "related_products"),
    PRODUCT_SEARCH_BOOSTS: (PRODUCT_SEARCH_BOOSTS, "search_boosts"),
    ROW_TAGS: (ROW_TAGS, "tags"),
}

OVERRIDE_TO_RESOLVED = {
    PRODUCT_SEO_TITLE: "seo_title",
    PRODUCT_SEO_DESCRIPTION: "seo_description",
    PRODUCT_GOOGLE_CATEGORY: "google_category",
    PRODUCT_CATEGORY1: "category1",
    PRODUCT_SUBCATEGORY: "subcategory",
    PRODUCT_SUBCATEGORY2: "subcategory2",
    PRODUCT_TYPE: "type",
    PRODUCT_STYLE: "style",
    PRODUCT_PATTERN: "pattern",
}

STOPWORDS = {
    "and",
    "for",
    "the",
    "with",
    "from",
    "your",
    "that",
    "this",
    "these",
    "those",
    "kids",
    "kid",
    "mom",
    "mother",
    "family",
    "matching",
    "set",
}

CATEGORY1_ALIASES = {
    "mommy and me": "Mommy and Me",
    "mommy & me": "Mommy and Me",
    "family matching": "Family Matching",
    "daddy and me": "Daddy and Me",
    "daddy & me": "Daddy and Me",
    "maternity": "Maternity",
    "couples": "Couples",
}

CATEGORY1_HINTS: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("maternity", "pregnan"), "Maternity"),
    (("daddy", "father", "dad"), "Daddy and Me"),
    (("couple", "husband", "wife"), "Couples"),
    (("family", "brother", "sister"), "Family Matching"),
)

SUBCATEGORY_ALIASES = {
    "swimsuits": "Swimwear",
    "family swimsuits": "Swimwear",
    "swimwear": "Swimwear",
    "dresses": "Dresses",
    "matching dresses": "Dresses",
    "maternity dresses": "Dresses",
    "pajamas": "Pajamas",
    "family pajamas": "Pajamas",
    "tops": "Tops",
    "family tops": "Tops",
    "sweaters": "Sweaters",
    "family sweaters": "Sweaters",
    "matching couples sweaters": "Sweaters",
    "daddy & me t-shirts": "T-Shirts",
    "matching couples t-shirts": "T-Shirts",
    "family sets": "Sets",
    "family matching sets": "Sets",
    "matching sets": "Sets",
    "jumpers": "Jumpsuits",
    "jumpsuits": "Jumpsuits",
    "trunks": "Trunks",
}

SUBCATEGORY_HINTS: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("bikini", "swimsuit", "swim", "beach", "pool"), "Swimwear"),
    (("trunk",), "Trunks"),
    (("pajama", "sleepwear", "nightgown", "loungewear"), "Pajamas"),
    (("dress", "gown", "sundress"), "Dresses"),
    (("sweater", "fleece", "hoodie"), "Sweaters"),
    (("t-shirt", "tee", "graphic tee"), "T-Shirts"),
    (("shirt", "top", "blouse"), "Tops"),
    (("romper", "jumpsuit", "jumper"), "Jumpsuits"),
    (("set", "outfit", "two-piece", "2 piece", "2-piece"), "Sets"),
)

TYPE_BY_SUBCATEGORY = {
    "Swimwear": "Swimwear",
    "Trunks": "Swimwear",
    "Dresses": "Dresses",
    "Pajamas": "Pajamas",
    "Tops": "Tops",
    "T-Shirts": "Tops",
    "Sweaters": "Sweaters",
    "Sets": "Sets",
    "Jumpsuits": "Jumpsuits",
}

STYLE_RULES: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("christmas", "holiday", "halloween", "valentine"), "Festive"),
    (("cozy", "fleece", "plush", "warm"), "Cozy"),
    (("formal", "elegant", "lace", "satin"), "Elegant"),
    (("boho", "bohemian"), "Boho"),
    (("casual", "everyday", "daily"), "Casual"),
)

STYLE_ALIASES = {
    "matching": "Matching",
    "festive": "Festive",
    "cozy": "Cozy",
    "casual": "Casual",
    "elegant": "Elegant",
    "boho": "Boho",
}

PATTERN_RULES: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("floral", "flower"), "Floral"),
    (("striped", "stripe"), "Striped"),
    (("plaid", "check"), "Plaid"),
    (("polka",), "Polka Dot"),
    (("leopard", "zebra", "animal print"), "Animal Print"),
)

PATTERN_ALIASES = {
    "solid": "Solid",
    "floral": "Floral",
    "striped": "Striped",
    "plaid": "Plaid",
    "polka dot": "Polka Dot",
    "animal print": "Animal Print",
}

SUBCATEGORY2_KEYWORDS: Sequence[Tuple[Tuple[str, ...], str]] = (
    (("maxi",), "Maxi Dresses"),
    (("midi",), "Midi Dresses"),
    (("mini",), "Mini Dresses"),
    (("sundress",), "Sundresses"),
    (("formal",), "Formal Dresses"),
    (("christmas", "holiday"), "Holiday"),
    (("bikini",), "Bikinis"),
    (("one piece", "one-piece"), "One Piece"),
    (("trunk",), "Swim Trunks"),
    (("jumpsuit", "jumper"), "Jumpsuits"),
)

GOOGLE_CATEGORY_BY_SUBCATEGORY = {
    "Dresses": "Apparel & Accessories > Clothing > Dresses",
    "Pajamas": "Apparel & Accessories > Clothing > Sleepwear & Loungewear",
    "Swimwear": "Apparel & Accessories > Clothing > Swimwear",
    "Trunks": "Apparel & Accessories > Clothing > Swimwear",
    "Tops": "Apparel & Accessories > Clothing > Shirts & Tops",
    "T-Shirts": "Apparel & Accessories > Clothing > Shirts & Tops",
    "Sweaters": "Apparel & Accessories > Clothing > Shirts & Tops",
    "Sets": "Apparel & Accessories > Clothing > Clothing Sets",
    "Jumpsuits": "Apparel & Accessories > Clothing > One-Pieces",
}


@dataclass
class ProductContext:
    handle: str
    status: str
    title: str
    tags: List[str] = field(default_factory=list)
    existing_type: str = ""
    category1: str = ""
    subcategory: str = ""
    subcategory2: str = ""
    pattern: str = ""
    style: str = ""
    custom_type: str = ""


def clean(value: str) -> str:
    return (value or "").strip()


def first_non_blank(row: Dict[str, str], keys: Sequence[str]) -> str:
    for key in keys:
        value = clean(row.get(key, ""))
        if value:
            return value
    return ""


def first_non_blank_from_rows(rows: Sequence[Dict[str, str]], column: str) -> str:
    for row in rows:
        value = clean(row.get(column, ""))
        if value:
            return value
    return ""


def load_overrides(path: Optional[Path]) -> Dict[str, Dict[str, str]]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Overrides CSV not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError("Overrides CSV has no header row")

    handle_keys = (ROW_HANDLE, "handle")
    overrides: Dict[str, Dict[str, str]] = {}
    for row in rows:
        handle = first_non_blank(row, handle_keys)
        if not handle:
            continue

        values: Dict[str, str] = {}
        for target_field, aliases in OVERRIDE_COLUMN_ALIASES.items():
            override_value = first_non_blank(row, aliases)
            if override_value:
                values[target_field] = override_value

        if not values:
            continue
        if handle not in overrides:
            overrides[handle] = {}
        overrides[handle].update(values)

    return overrides


def sku_for_mpn(value: str) -> str:
    return clean(value).lstrip("'")


def normalized_key(value: str) -> str:
    return clean(value).lower()


def parse_bool_true(value: str) -> bool:
    return normalized_key(value) in {"true", "1", "yes", "y"}


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", clean(value)).strip()


def normalize_marketing_title(value: str) -> str:
    text = normalize_spaces(value)
    text = re.sub(r"\s*\|\s*(dlm|dress like mommy).*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bDLM\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\.{3,}", " ", text)
    text = re.sub(r"[\"'“”‘’]+", "", text)
    text = normalize_spaces(text)
    return text.strip(" -:|,.;")


def shorten_phrase(text: str, max_len: int) -> str:
    cleaned = normalize_spaces(text)
    if len(cleaned) <= max_len:
        return cleaned
    short = cleaned[:max_len].rstrip()
    if " " in short:
        short = short.rsplit(" ", 1)[0]
    return short.strip(" -:|,.;")


def tags_from_row(row: Dict[str, str]) -> List[str]:
    tags: List[str] = []
    for raw in clean(row.get(ROW_TAGS, "")).split(","):
        token = clean(raw)
        if token:
            tags.append(token)
    return tags


def merge_status(existing_status: str, incoming_status: str) -> str:
    if normalized_key(existing_status) == ACTIVE_STATUS:
        return existing_status
    if normalized_key(incoming_status) == ACTIVE_STATUS:
        return incoming_status
    return incoming_status or existing_status


def blob_for_context(context: ProductContext) -> str:
    parts = [
        context.title,
        context.existing_type,
        context.category1,
        context.subcategory,
        context.subcategory2,
        context.custom_type,
    ] + context.tags
    return " ".join(part.lower() for part in parts if part)


def first_rule_match(blob: str, rules: Sequence[Tuple[Tuple[str, ...], str]]) -> str:
    for keywords, output in rules:
        if any(keyword in blob for keyword in keywords):
            return output
    return ""


def normalize_category1(raw_value: str, blob: str) -> str:
    alias = CATEGORY1_ALIASES.get(normalized_key(raw_value))
    if alias:
        return alias

    hinted = first_rule_match(blob, CATEGORY1_HINTS)
    if hinted:
        return hinted
    return "Mommy and Me"


def normalize_subcategory(raw_value: str, blob: str) -> str:
    alias = SUBCATEGORY_ALIASES.get(normalized_key(raw_value))
    if alias:
        return alias

    hinted = first_rule_match(blob, SUBCATEGORY_HINTS)
    if hinted:
        return hinted
    return "Sets"


def normalize_type(raw_value: str, subcategory: str, blob: str) -> str:
    type_from_subcategory = TYPE_BY_SUBCATEGORY.get(subcategory)
    if type_from_subcategory:
        return type_from_subcategory

    if clean(raw_value):
        cleaned = clean(raw_value)
        if normalized_key(cleaned) == "split bikini":
            return "Swimwear"
        return cleaned

    hinted_subcategory = first_rule_match(blob, SUBCATEGORY_HINTS)
    return TYPE_BY_SUBCATEGORY.get(hinted_subcategory, "Outfits")


def normalize_style(raw_value: str, blob: str) -> str:
    alias = STYLE_ALIASES.get(normalized_key(raw_value))
    if alias:
        return alias

    hinted = first_rule_match(blob, STYLE_RULES)
    return hinted or "Matching"


def normalize_pattern(raw_value: str, blob: str) -> str:
    alias = PATTERN_ALIASES.get(normalized_key(raw_value))
    if alias:
        return alias

    hinted = first_rule_match(blob, PATTERN_RULES)
    return hinted or "Solid"


def normalize_subcategory2(raw_value: str, subcategory: str, blob: str) -> str:
    candidate = clean(raw_value).split(",")[0]
    candidate_blob = f"{candidate} {blob}".strip().lower()
    keyword_match = first_rule_match(candidate_blob, SUBCATEGORY2_KEYWORDS)
    if keyword_match:
        if keyword_match == "Holiday":
            if subcategory == "Pajamas":
                return "Christmas Pajamas"
            if subcategory == "Tops" or subcategory == "T-Shirts":
                return "Christmas Tops"
            if subcategory == "Sweaters":
                return "Christmas Sweaters"
            return "Holiday"
        return keyword_match

    defaults = {
        "Dresses": "Everyday Dresses",
        "Pajamas": "Everyday Pajamas",
        "Swimwear": "Everyday Swimwear",
        "Trunks": "Swim Trunks",
        "Tops": "Everyday Tops",
        "T-Shirts": "Graphic Tees",
        "Sweaters": "Everyday Sweaters",
        "Sets": "Matching Sets",
        "Jumpsuits": "Everyday Jumpsuits",
    }
    return defaults.get(subcategory, "Core")


def google_category_for_subcategory(subcategory: str) -> str:
    return GOOGLE_CATEGORY_BY_SUBCATEGORY.get(subcategory, "Apparel & Accessories > Clothing")


def infer_seo_title(title: str) -> str:
    base = normalize_marketing_title(title)
    if not base:
        return ""
    if "gift card" in normalized_key(base):
        base = f"{DEFAULT_BRAND_SUFFIX} Gift Card"

    suffix = f" | {DEFAULT_BRAND_SUFFIX}"
    candidate = f"{base}{suffix}"
    if len(candidate) <= 70:
        return candidate

    room = max(0, 70 - len(suffix))
    trimmed = base[:room].rstrip()
    if " " in trimmed and len(base) > room:
        trimmed = trimmed.rsplit(" ", 1)[0]
    return f"{trimmed}{suffix}"


def trim_to_length(text: str, max_len: int) -> str:
    text = clean(text)
    if len(text) <= max_len:
        return text
    shortened = text[: max_len - 1].rstrip()
    if " " in shortened:
        shortened = shortened.rsplit(" ", 1)[0]
    return f"{shortened}."


def fit_description_length(text: str, min_len: int = 140, max_len: int = 155) -> str:
    output = trim_to_length(text, max_len)
    if len(output) >= min_len:
        return output

    additions = [
        " Shop now.",
        " Perfect for matching moments.",
        " New arrivals available.",
    ]
    for addition in additions:
        candidate = output
        if not candidate.endswith((".", "!", "?")):
            candidate = f"{candidate}."
        candidate = f"{candidate.rstrip('.')} {addition.strip()}"
        candidate = trim_to_length(candidate, max_len)
        output = candidate
        if len(output) >= min_len:
            return output

    return output


def infer_seo_description(
    title: str,
    category1: str,
    subcategory: str,
    style: str,
    pattern: str,
) -> str:
    base_title = normalize_marketing_title(title)
    if not base_title:
        return ""
    if "gift card" in normalized_key(base_title):
        sentence = (
            f"Buy a {DEFAULT_BRAND_SUFFIX} Gift Card for matching family outfits. "
            f"Perfect for birthdays, holidays, and last-minute gifting across every style."
        )
        return fit_description_length(sentence, 140, 155)

    short_title = shorten_phrase(base_title, 58)
    subcategory_text = subcategory.lower()
    style_text = style.lower()
    pattern_text = pattern.lower()
    sentence = (
        f"Shop {short_title} at {DEFAULT_BRAND_SUFFIX}. "
        f"{category1} {subcategory_text} in {style_text} {pattern_text} style for coordinated family looks and photo-ready moments."
    )
    return fit_description_length(sentence, 140, 155)


def title_keywords(title: str, limit: int = 5) -> List[str]:
    words = re.findall(r"[a-zA-Z]{4,}", clean(title).lower())
    output: List[str] = []
    for word in words:
        if word in STOPWORDS:
            continue
        if word not in output:
            output.append(word)
        if len(output) >= limit:
            break
    return output


def dedupe_case_insensitive(values: Iterable[str]) -> List[str]:
    output: List[str] = []
    seen = set()
    for raw in values:
        token = clean(raw)
        if not token:
            continue
        key = token.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(token)
    return output


def is_taxonomy_prefixed_tag(tag: str) -> bool:
    normalized = clean(tag).lower()
    return any(normalized.startswith(prefix) for prefix in TAXONOMY_TAG_PREFIXES)


def build_product_tags(existing_tags: Sequence[str], values: Dict[str, str], title: str) -> str:
    required = [
        f"category1:{values['category1']}",
        f"subcategory:{values['subcategory']}",
        f"subcategory2:{values['subcategory2']}",
        f"type:{values['type']}",
        f"style:{values['style']}",
        f"pattern:{values['pattern']}",
    ]

    plain_candidates: List[str] = []
    for tag in existing_tags:
        token = clean(tag)
        if not token or is_taxonomy_prefixed_tag(token):
            continue
        plain_candidates.append(token)

    plain_candidates.extend(
        [
            values["subcategory"],
            values["subcategory2"],
            values["category1"],
            values["type"],
            values["style"],
            values["pattern"],
        ]
    )
    plain_candidates.extend(title_keywords(title, limit=8))

    plain = dedupe_case_insensitive(plain_candidates)
    if len(plain) > 8:
        plain = plain[:8]

    combined = required + plain
    return ", ".join(dedupe_case_insensitive(combined))


def join_handles(handles: Iterable[str], limit: int) -> str:
    deduped: List[str] = []
    for handle in handles:
        token = clean(handle)
        if not token or token in deduped:
            continue
        deduped.append(token)
        if len(deduped) >= limit:
            break
    return ",".join(deduped)


def image_extension_from_url(url: str) -> str:
    raw = clean(url)
    if not raw:
        return ""
    base = raw.split("?", 1)[0].lower()
    name = base.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return f".{name.rsplit('.', 1)[-1]}"


def is_supported_image_url(url: str) -> bool:
    extension = image_extension_from_url(url)
    return bool(extension and extension in SUPPORTED_IMAGE_EXTENSIONS)


def normalize_signal_text(value: str) -> str:
    cleaned = clean(value).lower()
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return ""
    return f" {cleaned} "


def signal_present(normalized_text: str, token: str) -> bool:
    normalized_token = normalize_signal_text(token)
    if not normalized_token:
        return False
    return normalized_token in normalized_text


def first_valid_value(value: str, allowed: Sequence[str]) -> str:
    normalized = normalized_key(value)
    return normalized if normalized in allowed else ""


def variant_option_values(row: Dict[str, str]) -> List[str]:
    values: List[str] = []
    for field in (ROW_OPTION1_VALUE, ROW_OPTION2_VALUE, ROW_OPTION3_VALUE):
        value = clean(row.get(field, ""))
        if not value:
            continue
        if normalized_key(value) in {"default", "default title"}:
            continue
        values.append(value)
    return values


def variant_signal_blob(row: Dict[str, str]) -> str:
    parts = variant_option_values(row)
    sku = clean(row.get(ROW_VARIANT_SKU, ""))
    if sku:
        parts.append(sku)
    return normalize_signal_text(" ".join(parts))


def product_signal_blob(context: ProductContext) -> str:
    return normalize_signal_text(blob_for_context(context))


GENDER_TOKEN_GROUPS: Sequence[Tuple[str, Sequence[str]]] = (
    ("male", (" dad ", " daddy ", " father ", " mens ", " men ", " male ", " boy ", " boys ", " son ", " husband ")),
    (
        "female",
        (
            " mom ",
            " mommy ",
            " mother ",
            " womens ",
            " women ",
            " female ",
            " girl ",
            " girls ",
            " daughter ",
            " wife ",
            " maternity ",
            " pregnant ",
            " breastfeeding ",
        ),
    ),
    ("unisex", (" family ", " matching ", " unisex ", " couple ", " couples ", " parents ", " parent ")),
)

AGE_GROUP_TOKEN_GROUPS: Sequence[Tuple[str, Sequence[str]]] = (
    ("newborn", (" newborn ", " new born ")),
    ("infant", (" infant ", " baby ", " babies ", " 0 3m ", " 0 6m ", " 6 12m ", " 12m ", " 18m ", " 24m ")),
    ("toddler", (" toddler ", " 2t ", " 3t ", " 4t ", " 5t ")),
    ("kids", (" kid ", " kids ", " child ", " children ", " youth ", " teen ", " boy ", " girl ")),
    ("adult", (" adult ", " mom ", " mommy ", " mother ", " dad ", " daddy ", " father ", " women ", " men ", " parent ", " couple ")),
)

COLOR_ALIASES: Sequence[Tuple[str, str]] = (
    ("black", "Black"),
    ("white", "White"),
    ("red", "Red"),
    ("blue", "Blue"),
    ("navy", "Navy"),
    ("green", "Green"),
    ("pink", "Pink"),
    ("yellow", "Yellow"),
    ("orange", "Orange"),
    ("purple", "Purple"),
    ("brown", "Brown"),
    ("gray", "Gray"),
    ("grey", "Gray"),
    ("beige", "Beige"),
    ("khaki", "Khaki"),
    ("cream", "Cream"),
    ("ivory", "Ivory"),
    ("multi color", "Multicolor"),
    ("multicolor", "Multicolor"),
    ("rainbow", "Multicolor"),
    ("floral", "Floral"),
)


def infer_gender_from_signals(option_blob: str, context_blob: str) -> str:
    def resolve(blob: str) -> str:
        if not blob:
            return ""
        male = any(signal in blob for signal in GENDER_TOKEN_GROUPS[0][1])
        female = any(signal in blob for signal in GENDER_TOKEN_GROUPS[1][1])
        unisex = any(signal in blob for signal in GENDER_TOKEN_GROUPS[2][1])
        if unisex or (male and female):
            return "unisex"
        if male:
            return "male"
        if female:
            return "female"
        return ""

    option_guess = resolve(option_blob)
    if option_guess:
        return option_guess

    context_guess = resolve(context_blob)
    if context_guess:
        return context_guess

    return "unisex"


def infer_age_group_from_signals(option_blob: str, context_blob: str) -> str:
    def resolve(blob: str, prefer_adult_on_mix: bool) -> str:
        if not blob:
            return ""

        newborn = any(signal in blob for signal in AGE_GROUP_TOKEN_GROUPS[0][1])
        infant = any(signal in blob for signal in AGE_GROUP_TOKEN_GROUPS[1][1])
        toddler = any(signal in blob for signal in AGE_GROUP_TOKEN_GROUPS[2][1])
        kids = any(signal in blob for signal in AGE_GROUP_TOKEN_GROUPS[3][1])
        adult = any(signal in blob for signal in AGE_GROUP_TOKEN_GROUPS[4][1])

        if newborn:
            return "newborn"
        if infant:
            return "infant"
        if toddler:
            return "toddler"
        if kids and not adult:
            return "kids"
        if adult and not kids:
            return "adult"
        if kids and adult and prefer_adult_on_mix:
            return "adult"
        return ""

    option_guess = resolve(option_blob, prefer_adult_on_mix=False)
    if option_guess:
        return option_guess

    context_guess = resolve(context_blob, prefer_adult_on_mix=True)
    if context_guess:
        return context_guess

    return "adult"


def dominant_age_group(votes: Sequence[str]) -> str:
    filtered = [normalized_key(vote) for vote in votes if normalized_key(vote) in VALID_AGE_GROUP_VALUES]
    if not filtered:
        return "adult"

    ranking = {"adult": 5, "kids": 4, "toddler": 3, "infant": 2, "newborn": 1}
    counts = Counter(filtered)
    return max(counts.items(), key=lambda item: (item[1], ranking.get(item[0], 0)))[0]


def normalize_color_value(value: str) -> List[str]:
    normalized = normalize_signal_text(value)
    if not normalized:
        return []

    output: List[str] = []
    for token, canonical in COLOR_ALIASES:
        if signal_present(normalized, token) and canonical not in output:
            output.append(canonical)
    if output:
        return output

    cleaned = re.sub(r"[\(\)\[\]{}]+", " ", clean(value))
    cleaned = re.sub(r"[/|>;+]+", ",", cleaned)
    primary = clean(cleaned.split(",", 1)[0])
    if not primary:
        return []
    return [shorten_phrase(primary.title(), 40)]


def is_color_option_name(value: str) -> bool:
    normalized = normalize_signal_text(value)
    return signal_present(normalized, "color") or signal_present(normalized, "colour")


def infer_color_from_row(row: Dict[str, str]) -> List[str]:
    colors: List[str] = []
    for index in (1, 2, 3):
        option_name = clean(row.get(f"Option{index} Name", ""))
        option_value = clean(row.get(f"Option{index} Value", ""))
        if not option_value:
            continue
        if is_color_option_name(option_name):
            colors.extend(normalize_color_value(option_value))

    if colors:
        return dedupe_case_insensitive(colors)

    for option_value in variant_option_values(row):
        colors.extend(normalize_color_value(option_value))
    return dedupe_case_insensitive(colors)


def infer_handle_color(rows_for_handle: Sequence[Dict[str, str]]) -> str:
    existing = first_non_blank_from_rows(rows_for_handle, PRODUCT_SHOPIFY_COLOR)
    if existing:
        return existing

    colors: List[str] = []
    for row in rows_for_handle:
        colors.extend(infer_color_from_row(row))

    deduped = dedupe_case_insensitive(colors)
    if not deduped:
        return ""
    return ", ".join(deduped[:3])


def infer_image_alt_text(row: Dict[str, str], title: str) -> str:
    if not clean(row.get(ROW_IMAGE_SRC, "")):
        return ""

    base = clean(title)
    if not base:
        return ""

    options: List[str] = []
    for field in (ROW_OPTION1_VALUE, ROW_OPTION2_VALUE, ROW_OPTION3_VALUE):
        value = clean(row.get(field, ""))
        if not value:
            continue
        if normalized_key(value) in {"default title", "default"}:
            continue
        if value not in options:
            options.append(value)

    if not options:
        return trim_to_length(base, 120)
    return trim_to_length(f"{base} - {', '.join(options)}", 120)


def build_product_contexts(rows: Sequence[Dict[str, str]]) -> Dict[str, ProductContext]:
    contexts: Dict[str, ProductContext] = {}
    for row in rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if not handle:
            continue

        status = clean(row.get(ROW_STATUS, ""))
        if handle not in contexts:
            contexts[handle] = ProductContext(
                handle=handle,
                status=status,
                title=clean(row.get(ROW_TITLE, "")),
                tags=tags_from_row(row),
                existing_type=clean(row.get(ROW_TYPE, "")),
                category1=clean(row.get(PRODUCT_CATEGORY1, "")),
                subcategory=clean(row.get(PRODUCT_SUBCATEGORY, "")),
                subcategory2=clean(row.get(PRODUCT_SUBCATEGORY2, "")),
                pattern=clean(row.get(PRODUCT_PATTERN, "")),
                style=clean(row.get(PRODUCT_STYLE, "")),
                custom_type=clean(row.get(PRODUCT_TYPE, "")),
            )
            continue

        context = contexts[handle]
        context.status = merge_status(context.status, status)
        if not context.title:
            context.title = clean(row.get(ROW_TITLE, ""))
        if not context.tags:
            context.tags = tags_from_row(row)
        if not context.existing_type:
            context.existing_type = clean(row.get(ROW_TYPE, ""))
        if not context.category1:
            context.category1 = clean(row.get(PRODUCT_CATEGORY1, ""))
        if not context.subcategory:
            context.subcategory = clean(row.get(PRODUCT_SUBCATEGORY, ""))
        if not context.subcategory2:
            context.subcategory2 = clean(row.get(PRODUCT_SUBCATEGORY2, ""))
        if not context.pattern:
            context.pattern = clean(row.get(PRODUCT_PATTERN, ""))
        if not context.style:
            context.style = clean(row.get(PRODUCT_STYLE, ""))
        if not context.custom_type:
            context.custom_type = clean(row.get(PRODUCT_TYPE, ""))
    return contexts


def product_field_coverage(
    rows: Sequence[Dict[str, str]],
    handles: Sequence[str],
    field: str,
) -> Tuple[int, int]:
    target = set(handles)
    by_handle: Dict[str, bool] = {handle: False for handle in target}
    for row in rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if handle not in by_handle:
            continue
        if clean(row.get(field, "")):
            by_handle[handle] = True
    filled = sum(1 for value in by_handle.values() if value)
    return filled, len(by_handle)


def is_variant_row(row: Dict[str, str]) -> bool:
    return bool(
        clean(row.get(ROW_VARIANT_SKU, ""))
        or clean(row.get(ROW_OPTION1_VALUE, ""))
        or clean(row.get(ROW_OPTION2_VALUE, ""))
        or clean(row.get(ROW_OPTION3_VALUE, ""))
    )


def variant_field_coverage(
    rows: Sequence[Dict[str, str]],
    handles: Sequence[str],
    field: str,
) -> Tuple[int, int]:
    target = set(handles)
    variants = [row for row in rows if clean(row.get(ROW_HANDLE, "")) in target and is_variant_row(row)]
    total = len(variants)
    filled = sum(1 for row in variants if clean(row.get(field, "")))
    return filled, total


def pct(numerator: int, denominator: int) -> float:
    return (numerator / denominator * 100.0) if denominator else 0.0


def write_summary(
    summary_path: Path,
    input_path: Path,
    output_path: Path,
    input_rows: Sequence[Dict[str, str]],
    output_rows: Sequence[Dict[str, str]],
    target_handles: Sequence[str],
    published_updates: int,
    unsupported_image_replacements: int,
) -> None:
    available_columns = set(input_rows[0].keys()) if input_rows else set()
    product_fields = [
        PRODUCT_SEO_TITLE,
        PRODUCT_SEO_DESCRIPTION,
        PRODUCT_GOOGLE_CATEGORY,
        PRODUCT_SHOPIFY_AGE_GROUP,
        PRODUCT_SHOPIFY_COLOR,
        PRODUCT_CATEGORY1,
        PRODUCT_SUBCATEGORY,
        PRODUCT_SUBCATEGORY2,
        PRODUCT_TYPE,
        PRODUCT_STYLE,
        PRODUCT_PATTERN,
        PRODUCT_DISCOVERY_COMPLEMENTARY,
        PRODUCT_DISCOVERY_RELATED_SETTINGS,
        PRODUCT_DISCOVERY_RELATED,
        PRODUCT_SEARCH_BOOSTS,
    ]
    product_fields = [field for field in product_fields if field in available_columns]
    variant_fields = [
        ROW_VARIANT_BARCODE,
        ROW_GOOGLE_GENDER,
        ROW_GOOGLE_AGE_GROUP,
        ROW_GOOGLE_CONDITION,
        ROW_GOOGLE_MPN,
        ROW_GOOGLE_CUSTOM_PRODUCT,
        PRODUCT_GOOGLE_CUSTOM_METAFIELD,
        ROW_IMAGE_ALT,
    ]
    variant_fields = [field for field in variant_fields if field in available_columns]

    lines: List[str] = []
    lines.append("# Product Metadata Backfill Summary")
    lines.append("")
    lines.append(f"Input file: `{input_path}`")
    lines.append(f"Output file: `{output_path}`")
    lines.append(f"Target products: `{len(target_handles)}` active handles")
    lines.append("")
    lines.append("## Product-level coverage (active products)")
    lines.append("")
    lines.append("| Field | Before | After |")
    lines.append("|---|---:|---:|")
    for field in product_fields:
        before_filled, before_total = product_field_coverage(input_rows, target_handles, field)
        after_filled, after_total = product_field_coverage(output_rows, target_handles, field)
        lines.append(
            f"| {field} | {before_filled}/{before_total} ({pct(before_filled, before_total):.1f}%) | "
            f"{after_filled}/{after_total} ({pct(after_filled, after_total):.1f}%) |"
        )

    lines.append("")
    lines.append("## Variant-level coverage (active products)")
    lines.append("")
    lines.append("| Field | Before | After |")
    lines.append("|---|---:|---:|")
    for field in variant_fields:
        before_filled, before_total = variant_field_coverage(input_rows, target_handles, field)
        after_filled, after_total = variant_field_coverage(output_rows, target_handles, field)
        lines.append(
            f"| {field} | {before_filled}/{before_total} ({pct(before_filled, before_total):.1f}%) | "
            f"{after_filled}/{after_total} ({pct(after_filled, after_total):.1f}%) |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Active handles were normalized to controlled taxonomy values for Category1/SubCategory/SubCategory2/Type/Style/Pattern.")
    lines.append("- Google apparel attributes are backfilled at variant level (`Google Shopping / Gender`, `Google Shopping / Age Group`) with product-level age/color hints.")
    lines.append("- Missing GTINs were not fabricated. Rows without barcode are marked custom product and receive MPN from SKU when available.")
    lines.append(f"- Published state updates applied on target rows: `{published_updates}`.")
    lines.append(f"- Unsupported image URL replacements applied (`.webp` -> supported source): `{unsupported_image_replacements}`.")
    lines.append("- Complementary/related/search boost fields are generated from taxonomy similarity and title keywords for immediate Search & Discovery seeding.")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill metadata in a Shopify product export CSV")
    parser.add_argument(
        "--input",
        default="GPT/products_export_1.csv",
        help="Input CSV path (default: GPT/products_export_1.csv)",
    )
    parser.add_argument(
        "--output",
        default="GPT/products_export_1_backfill.csv",
        help="Output CSV path (default: GPT/products_export_1_backfill.csv)",
    )
    parser.add_argument(
        "--summary",
        default="ops/products_export_1_backfill_summary.md",
        help="Summary markdown path (default: ops/products_export_1_backfill_summary.md)",
    )
    parser.add_argument(
        "--overrides",
        default="",
        help=(
            "Optional overrides CSV path keyed by Handle. Supports canonical column names "
            "or short aliases (e.g. seo_title, google_category, complementary_products)."
        ),
    )
    parser.add_argument(
        "--all-statuses",
        action="store_true",
        help="Backfill all products regardless of Status. Default is active only.",
    )
    parser.add_argument(
        "--publish-targets",
        action="store_true",
        help="Set Published=TRUE for all target rows.",
    )
    parser.add_argument(
        "--replace-unsupported-images",
        action="store_true",
        help="Replace unsupported image URL extensions (for example .webp) with a supported image URL from the same handle.",
    )
    parser.add_argument(
        "--target-only-rows",
        action="store_true",
        help="Write only target-handle rows to the output CSV.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    summary_path = Path(args.summary)
    overrides_path = Path(args.overrides) if clean(args.overrides) else None

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row")
        fieldnames = list(reader.fieldnames)

    required_columns = (
        ROW_HANDLE,
        ROW_STATUS,
        ROW_PUBLISHED,
        ROW_TITLE,
        ROW_TYPE,
        ROW_TAGS,
        ROW_IMAGE_SRC,
        ROW_IMAGE_ALT,
        ROW_OPTION1_NAME,
        ROW_OPTION2_NAME,
        ROW_OPTION3_NAME,
        ROW_VARIANT_SKU,
        ROW_VARIANT_BARCODE,
        ROW_GOOGLE_MPN,
        ROW_GOOGLE_CUSTOM_PRODUCT,
        PRODUCT_SEO_TITLE,
        PRODUCT_SEO_DESCRIPTION,
        PRODUCT_GOOGLE_CATEGORY,
        PRODUCT_CATEGORY1,
        PRODUCT_SUBCATEGORY,
        PRODUCT_SUBCATEGORY2,
        PRODUCT_TYPE,
        PRODUCT_STYLE,
        PRODUCT_PATTERN,
        PRODUCT_DISCOVERY_COMPLEMENTARY,
        PRODUCT_DISCOVERY_RELATED_SETTINGS,
        PRODUCT_DISCOVERY_RELATED,
        PRODUCT_SEARCH_BOOSTS,
        PRODUCT_GOOGLE_CUSTOM_METAFIELD,
    )
    for required in required_columns:
        if required not in fieldnames:
            raise ValueError(f"Missing expected CSV column: {required}")

    optional_columns = {
        ROW_VARIANT_IMAGE,
        ROW_GOOGLE_CONDITION,
        ROW_GOOGLE_GENDER,
        ROW_GOOGLE_AGE_GROUP,
        PRODUCT_SHOPIFY_AGE_GROUP,
        PRODUCT_SHOPIFY_COLOR,
    }

    overrides = load_overrides(overrides_path)

    contexts = build_product_contexts(rows)
    if args.all_statuses:
        target_handles = sorted(contexts.keys())
    else:
        target_handles = sorted(
            handle
            for handle, context in contexts.items()
            if normalized_key(context.status) == ACTIVE_STATUS
        )
    target_handle_set = set(target_handles)

    resolved: Dict[str, Dict[str, str]] = {}
    for handle in target_handles:
        context = contexts[handle]
        blob = blob_for_context(context)
        is_gift_card = "gift card" in normalized_key(context.title) or "gift card" in normalized_key(context.existing_type)
        category1 = normalize_category1(context.category1, blob)
        subcategory = normalize_subcategory(context.subcategory, blob)
        custom_type = normalize_type(context.custom_type or context.existing_type, subcategory, blob)
        style = normalize_style(context.style, blob)
        pattern = normalize_pattern(context.pattern, blob)
        subcategory2 = normalize_subcategory2(context.subcategory2, subcategory, blob)
        google_category = google_category_for_subcategory(subcategory)
        if is_gift_card:
            google_category = GOOGLE_CATEGORY_GIFT_CARD

        resolved[handle] = {
            "seo_title": infer_seo_title(context.title),
            "seo_description": infer_seo_description(
                context.title,
                category1,
                subcategory,
                style,
                pattern,
            ),
            "google_category": google_category,
            "category1": category1,
            "subcategory": subcategory,
            "subcategory2": subcategory2,
            "type": custom_type,
            "style": style,
            "pattern": pattern,
        }

    for handle in target_handles:
        values = resolved[handle]
        override_values = overrides.get(handle, {})
        if not override_values:
            continue
        for column, key in OVERRIDE_TO_RESOLVED.items():
            if column in override_values:
                values[key] = override_values[column]

    handles_by_subcategory: Dict[str, List[str]] = defaultdict(list)
    handles_by_category: Dict[str, List[str]] = defaultdict(list)
    handles_by_type: Dict[str, List[str]] = defaultdict(list)
    for handle in target_handles:
        values = resolved[handle]
        handles_by_subcategory[values["subcategory"].lower()].append(handle)
        handles_by_category[values["category1"].lower()].append(handle)
        handles_by_type[values["type"].lower()].append(handle)

    complementary_handles: Dict[str, str] = {}
    related_handles: Dict[str, str] = {}
    related_settings: Dict[str, str] = {
        handle: RELATED_SETTINGS_MANUAL for handle in target_handles
    }
    search_boosts: Dict[str, str] = {}
    tags_csv_by_handle: Dict[str, str] = {}

    for handle in target_handles:
        context = contexts[handle]
        values = resolved[handle]
        category_key = values["category1"].lower()
        subcategory_key = values["subcategory"].lower()
        type_key = values["type"].lower()

        complementary_candidates: List[str] = []
        complementary_candidates.extend(
            sorted(h for h in handles_by_subcategory[subcategory_key] if h != handle)
        )
        complementary_candidates.extend(
            sorted(h for h in handles_by_category[category_key] if h != handle)
        )
        complementary_candidates.extend(
            sorted(h for h in handles_by_type[type_key] if h != handle)
        )
        complementary_candidates.extend(sorted(h for h in target_handles if h != handle))
        complementary_handles[handle] = join_handles(complementary_candidates, limit=10)

        related_candidates: List[str] = []
        related_candidates.extend(sorted(h for h in handles_by_category[category_key] if h != handle))
        related_candidates.extend(sorted(h for h in handles_by_type[type_key] if h != handle))
        related_candidates.extend(sorted(h for h in handles_by_subcategory[subcategory_key] if h != handle))
        related_candidates.extend(sorted(h for h in target_handles if h != handle))
        related_handles[handle] = join_handles(related_candidates, limit=12)

        boost_terms = [
            values["subcategory"],
            values["subcategory2"],
            values["category1"],
            values["type"],
            values["style"],
            values["pattern"],
        ]
        boost_terms.extend(title_keywords(context.title, limit=5))

        ordered_boosts: List[str] = []
        seen = set()
        for term in boost_terms:
            token = clean(term)
            if not token:
                continue
            if token.lower() in {"core", "holiday"}:
                continue
            key = token.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered_boosts.append(token)
            if len(ordered_boosts) >= 10:
                break
        search_boosts[handle] = ", ".join(ordered_boosts)
        tags_csv_by_handle[handle] = build_product_tags(context.tags, values, context.title)

    for handle, values in overrides.items():
        if handle not in target_handle_set:
            continue
        if PRODUCT_DISCOVERY_COMPLEMENTARY in values:
            complementary_handles[handle] = values[PRODUCT_DISCOVERY_COMPLEMENTARY]
        if PRODUCT_DISCOVERY_RELATED in values:
            related_handles[handle] = values[PRODUCT_DISCOVERY_RELATED]
        if PRODUCT_DISCOVERY_RELATED_SETTINGS in values:
            related_settings[handle] = values[PRODUCT_DISCOVERY_RELATED_SETTINGS]
        if PRODUCT_SEARCH_BOOSTS in values:
            search_boosts[handle] = values[PRODUCT_SEARCH_BOOSTS]
        if ROW_TAGS in values:
            tags_csv_by_handle[handle] = values[ROW_TAGS]

    rows_by_handle: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if handle and handle in target_handle_set:
            rows_by_handle[handle].append(row)

    context_signal_by_handle = {
        handle: product_signal_blob(contexts[handle]) for handle in target_handles
    }

    dominant_age_by_handle: Dict[str, str] = {}
    for handle in target_handles:
        votes: List[str] = []
        handle_rows = rows_by_handle.get(handle, [])

        existing_google_age = first_valid_value(
            first_non_blank_from_rows(handle_rows, ROW_GOOGLE_AGE_GROUP),
            tuple(VALID_AGE_GROUP_VALUES),
        )
        if existing_google_age:
            votes.append(existing_google_age)

        if PRODUCT_SHOPIFY_AGE_GROUP in optional_columns:
            existing_metafield_age = first_valid_value(
                first_non_blank_from_rows(handle_rows, PRODUCT_SHOPIFY_AGE_GROUP),
                tuple(VALID_AGE_GROUP_VALUES),
            )
            if existing_metafield_age:
                votes.append(existing_metafield_age)

        for row in handle_rows:
            if not is_variant_row(row):
                continue
            row_age = first_valid_value(
                clean(row.get(ROW_GOOGLE_AGE_GROUP, "")),
                tuple(VALID_AGE_GROUP_VALUES),
            )
            if row_age:
                votes.append(row_age)
                continue
            votes.append(
                infer_age_group_from_signals(
                    variant_signal_blob(row), context_signal_by_handle[handle]
                )
            )

        dominant_age_by_handle[handle] = dominant_age_group(votes)

    color_hint_by_handle: Dict[str, str] = {}
    if PRODUCT_SHOPIFY_COLOR in optional_columns:
        color_hint_by_handle = {
            handle: infer_handle_color(rows_by_handle.get(handle, []))
            for handle in target_handles
        }

    supported_image_src_by_handle: Dict[str, str] = {}
    supported_variant_image_by_handle: Dict[str, str] = {}
    if args.replace_unsupported_images:
        for handle in target_handles:
            for row in rows_by_handle.get(handle, []):
                image_src = clean(row.get(ROW_IMAGE_SRC, ""))
                if image_src and is_supported_image_url(image_src):
                    supported_image_src_by_handle.setdefault(handle, image_src)

                if ROW_VARIANT_IMAGE in optional_columns:
                    variant_image = clean(row.get(ROW_VARIANT_IMAGE, ""))
                    if variant_image and is_supported_image_url(variant_image):
                        supported_variant_image_by_handle.setdefault(handle, variant_image)

            if handle not in supported_variant_image_by_handle:
                fallback = supported_image_src_by_handle.get(handle)
                if fallback:
                    supported_variant_image_by_handle[handle] = fallback

    output_rows = [
        dict(row)
        for row in rows
        if (not args.target_only_rows) or clean(row.get(ROW_HANDLE, "")) in target_handle_set
    ]
    seen_handles = set()
    published_updates = 0
    unsupported_image_replacements = 0

    for row in output_rows:
        handle = clean(row.get(ROW_HANDLE, ""))
        if not handle or handle not in target_handle_set:
            continue

        context = contexts[handle]
        values = resolved[handle]

        if args.publish_targets and not parse_bool_true(row.get(ROW_PUBLISHED, "")):
            row[ROW_PUBLISHED] = "TRUE"
            published_updates += 1

        if args.replace_unsupported_images:
            image_src = clean(row.get(ROW_IMAGE_SRC, ""))
            if image_src and not is_supported_image_url(image_src):
                fallback_src = supported_image_src_by_handle.get(handle)
                if fallback_src:
                    row[ROW_IMAGE_SRC] = fallback_src
                    unsupported_image_replacements += 1

            if ROW_VARIANT_IMAGE in optional_columns:
                variant_image = clean(row.get(ROW_VARIANT_IMAGE, ""))
                if variant_image and not is_supported_image_url(variant_image):
                    fallback_variant = supported_variant_image_by_handle.get(handle)
                    if fallback_variant:
                        row[ROW_VARIANT_IMAGE] = fallback_variant
                        unsupported_image_replacements += 1

        if is_variant_row(row):
            barcode = clean(row.get(ROW_VARIANT_BARCODE, ""))
            sku = sku_for_mpn(row.get(ROW_VARIANT_SKU, ""))
            has_barcode = bool(barcode)

            if not has_barcode:
                row[ROW_GOOGLE_CUSTOM_PRODUCT] = "TRUE"
                row[PRODUCT_GOOGLE_CUSTOM_METAFIELD] = "TRUE"
                if sku and not clean(row.get(ROW_GOOGLE_MPN, "")):
                    row[ROW_GOOGLE_MPN] = sku
            else:
                if not clean(row.get(ROW_GOOGLE_CUSTOM_PRODUCT, "")):
                    row[ROW_GOOGLE_CUSTOM_PRODUCT] = "FALSE"
                if not clean(row.get(PRODUCT_GOOGLE_CUSTOM_METAFIELD, "")):
                    row[PRODUCT_GOOGLE_CUSTOM_METAFIELD] = "FALSE"
                if sku and not clean(row.get(ROW_GOOGLE_MPN, "")):
                    row[ROW_GOOGLE_MPN] = sku

            option_blob = variant_signal_blob(row)
            context_blob = context_signal_by_handle[handle]

            if ROW_GOOGLE_GENDER in optional_columns:
                existing_gender = first_valid_value(
                    row.get(ROW_GOOGLE_GENDER, ""),
                    tuple(VALID_GENDER_VALUES),
                )
                row[ROW_GOOGLE_GENDER] = existing_gender or infer_gender_from_signals(
                    option_blob, context_blob
                )

            if ROW_GOOGLE_AGE_GROUP in optional_columns:
                existing_age_group = first_valid_value(
                    row.get(ROW_GOOGLE_AGE_GROUP, ""),
                    tuple(VALID_AGE_GROUP_VALUES),
                )
                row[ROW_GOOGLE_AGE_GROUP] = existing_age_group or infer_age_group_from_signals(
                    option_blob, context_blob
                )

            if ROW_GOOGLE_CONDITION in optional_columns and not clean(
                row.get(ROW_GOOGLE_CONDITION, "")
            ):
                row[ROW_GOOGLE_CONDITION] = "new"

        if not clean(row.get(ROW_IMAGE_ALT, "")):
            alt_text = infer_image_alt_text(row, context.title)
            if alt_text:
                row[ROW_IMAGE_ALT] = alt_text

        # Product-level updates written once per handle.
        if handle in seen_handles:
            continue
        seen_handles.add(handle)

        row[PRODUCT_SEO_TITLE] = values["seo_title"]
        row[PRODUCT_SEO_DESCRIPTION] = values["seo_description"]

        row[PRODUCT_GOOGLE_CATEGORY] = values["google_category"]
        row[PRODUCT_CATEGORY1] = values["category1"]
        row[PRODUCT_SUBCATEGORY] = values["subcategory"]
        row[PRODUCT_SUBCATEGORY2] = values["subcategory2"]
        row[PRODUCT_TYPE] = values["type"]
        row[PRODUCT_STYLE] = values["style"]
        row[PRODUCT_PATTERN] = values["pattern"]
        row[PRODUCT_DISCOVERY_COMPLEMENTARY] = complementary_handles.get(handle, "")
        row[PRODUCT_DISCOVERY_RELATED_SETTINGS] = related_settings.get(
            handle, RELATED_SETTINGS_MANUAL
        )
        row[PRODUCT_DISCOVERY_RELATED] = related_handles.get(handle, "")
        row[PRODUCT_SEARCH_BOOSTS] = search_boosts.get(handle, "")
        row[ROW_TAGS] = tags_csv_by_handle.get(handle, row.get(ROW_TAGS, ""))
        if PRODUCT_SHOPIFY_AGE_GROUP in optional_columns and not clean(
            row.get(PRODUCT_SHOPIFY_AGE_GROUP, "")
        ):
            row[PRODUCT_SHOPIFY_AGE_GROUP] = dominant_age_by_handle.get(handle, "adult")
        if PRODUCT_SHOPIFY_COLOR in optional_columns and not clean(
            row.get(PRODUCT_SHOPIFY_COLOR, "")
        ):
            color_hint = color_hint_by_handle.get(handle, "")
            if color_hint:
                row[PRODUCT_SHOPIFY_COLOR] = color_hint

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    write_summary(
        summary_path=summary_path,
        input_path=input_path,
        output_path=output_path,
        input_rows=rows,
        output_rows=output_rows,
        target_handles=target_handles,
        published_updates=published_updates,
        unsupported_image_replacements=unsupported_image_replacements,
    )

    print(f"Backfill written: {output_path}")
    print(f"Summary written: {summary_path}")
    print(f"Target handles: {len(target_handles)}")
    print(f"Published updates: {published_updates}")
    print(f"Unsupported image replacements: {unsupported_image_replacements}")
    if overrides_path:
        print(f"Overrides loaded: {len(overrides)} handles from {overrides_path}")


if __name__ == "__main__":
    main()
