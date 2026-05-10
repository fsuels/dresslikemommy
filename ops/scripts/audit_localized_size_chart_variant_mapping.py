#!/usr/bin/env python3
"""Read-only audit for localized size-chart variant row mapping.

This complements `repair_localized_product_size_charts.py`: that script proves
each locale has chart tables; this script proves available variants can match a
row in those charts using the same conservative role/type rules as the PDP.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.poll_shopify_product_translations import ShopifyClient, clean, has_size_chart_table, resolve_target_locales  # noqa: E402
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


ACTIVE_PRODUCTS_WITH_VARIANTS_QUERY = """
query ActiveProducts($first: Int!, $after: String, $query: String!) {
  products(first: $first, after: $after, query: $query) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        legacyResourceId
        handle
        title
        status
        updatedAt
        descriptionHtml
        options { name position values }
        variants(first: 250) {
          edges {
            node {
              id
              legacyResourceId
              title
              sku
              availableForSale
              selectedOptions { name value }
            }
          }
        }
      }
    }
  }
}
"""

PRODUCT_BY_HANDLE_WITH_VARIANTS_QUERY = """
query ProductByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    id
    legacyResourceId
    handle
    title
    status
    updatedAt
    descriptionHtml
    options { name position values }
    variants(first: 250) {
      edges {
        node {
          id
          legacyResourceId
          title
          sku
          availableForSale
          selectedOptions { name value }
        }
      }
    }
  }
}
"""

ROLE_LABELS_BY_LOCALE = {
    "en": {"mother": "Mother", "father": "Father", "girl": "Girl", "boy": "Boy", "child": "Child", "baby": "Baby", "adult": "Adult"},
    "ar": {"mother": "الأم", "father": "الأب", "girl": "البنت", "boy": "الولد", "child": "الأطفال", "baby": "الرضيع", "adult": "الكبار"},
    "cs": {"mother": "Maminka", "father": "Tatínek", "girl": "Dívka", "boy": "Chlapec", "child": "Dítě", "baby": "Miminko", "adult": "Dospělý"},
    "da": {"mother": "Mor", "father": "Far", "girl": "Pige", "boy": "Dreng", "child": "Barn", "baby": "Baby", "adult": "Voksen"},
    "de": {"mother": "Mama", "father": "Papa", "girl": "Mädchen", "boy": "Junge", "child": "Kind", "baby": "Baby", "adult": "Erwachsene"},
    "el": {"mother": "Μητέρα", "father": "Πατέρας", "girl": "Κορίτσι", "boy": "Αγόρι", "child": "Παιδί", "baby": "Μωρό", "adult": "Ενήλικας"},
    "es": {"mother": "Mamá", "father": "Papá", "girl": "Niña", "boy": "Niño", "child": "Infantil", "baby": "Bebé", "adult": "Adulto"},
    "fi": {"mother": "Äiti", "father": "Isä", "girl": "Tyttö", "boy": "Poika", "child": "Lapsi", "baby": "Vauva", "adult": "Aikuinen"},
    "fr": {"mother": "Maman", "father": "Papa", "girl": "Fille", "boy": "Garçon", "child": "Enfant", "baby": "Bébé", "adult": "Adulte"},
    "he": {"mother": "אמא", "father": "אבא", "girl": "ילדה", "boy": "ילד", "child": "ילדים", "baby": "תינוק", "adult": "מבוגר"},
    "hi": {"mother": "माँ", "father": "पिता", "girl": "लड़की", "boy": "लड़का", "child": "बच्चा", "baby": "शिशु", "adult": "वयस्क"},
    "it": {"mother": "Mamma", "father": "Papà", "girl": "Bambina", "boy": "Bambino", "child": "Bimbi", "baby": "Bebè", "adult": "Adulto"},
    "ja": {"mother": "ママ", "father": "パパ", "girl": "女の子", "boy": "男の子", "child": "子供", "baby": "ベビー", "adult": "大人"},
    "ko": {"mother": "엄마", "father": "아빠", "girl": "여아", "boy": "남아", "child": "아동", "baby": "베이비", "adult": "성인"},
    "nl": {"mother": "Mama", "father": "Papa", "girl": "Meisje", "boy": "Jongen", "child": "Kind", "baby": "Baby", "adult": "Volwassene"},
    "no": {"mother": "Mamma", "father": "Pappa", "girl": "Jente", "boy": "Gutt", "child": "Barn", "baby": "Baby", "adult": "Voksen"},
    "pl": {"mother": "Mama", "father": "Tata", "girl": "Dziewczynka", "boy": "Chłopiec", "child": "Dziecko", "baby": "Niemowlę", "adult": "Dorosły"},
    "pt": {"mother": "Mãe", "father": "Pai", "girl": "Menina", "boy": "Menino", "child": "Infantil", "baby": "Bebê", "adult": "Adulto"},
    "ro": {"mother": "Mamă", "father": "Tată", "girl": "Fată", "boy": "Băiat", "child": "Copil", "baby": "Bebeluș", "adult": "Adult"},
    "ru": {"mother": "Мама", "father": "Папа", "girl": "Девочка", "boy": "Мальчик", "child": "Дети", "baby": "Малыш", "adult": "Взрослый"},
    "sv": {"mother": "Mamma", "father": "Pappa", "girl": "Flicka", "boy": "Pojke", "child": "Barn", "baby": "Baby", "adult": "Vuxen"},
    "zh": {"mother": "妈妈", "father": "爸爸", "girl": "女孩", "boy": "男孩", "child": "儿童", "baby": "婴儿", "adult": "成人"},
}

ROLE_ALIASES = {
    "mother": ["mother", "mom", "mum", "mama", "mamá", "mamă", "maman", "mamma", "mãe", "mae", "moeder", "mor", "äiti", "الأم", "الام"],
    "father": ["father", "dad", "papa", "papá", "papà", "pappa", "padre", "pai", "vader", "far", "isä", "tata", "tată", "الأب", "الاب"],
    "girl": ["girl", "daughter", "hija", "filha", "figlia", "tochter", "niña", "nina", "fille", "bambina", "menina", "mädchen", "maedchen", "flicka", "jente", "娘", "딸", "дочь", "الابنة", "ابنة"],
    "boy": ["boy", "son", "hijo", "filho", "figlio", "sohn", "fils", "niño", "nino", "garçon", "garcon", "bambino", "menino", "junge", "pojke", "gutt", "息子", "아들", "сын", "الابن", "ابن"],
    "child": ["child", "children", "kid", "kids", "infantil", "bimbi", "bambini", "kind", "barn", "dziecko", "dítě"],
    "baby": ["baby", "bebe", "bebé", "bébé", "رضيع", "بيبي"],
    "adult": ["adult", "adults", "adulto", "adulta", "adulte", "adultes", "voksen", "vuxen"],
}


def norm(value: str) -> str:
    text = clean(value).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    return re.sub(r"\s+", " ", text.casefold()).strip()


def active_products(client: ShopifyClient, *, page_size: int, max_products: int, handles: list[str]) -> list[dict[str, Any]]:
    if handles:
        rows = []
        for handle in handles:
            product = client.graphql(PRODUCT_BY_HANDLE_WITH_VARIANTS_QUERY, {"handle": handle}).get("productByHandle")
            if product:
                rows.append(product)
        return rows

    rows: list[dict[str, Any]] = []
    after = None
    while True:
        page = client.graphql(
            ACTIVE_PRODUCTS_WITH_VARIANTS_QUERY,
            {"first": max(1, page_size), "after": after, "query": "status:active"},
        )["products"]
        for edge in page.get("edges") or []:
            product = edge.get("node") or {}
            if clean(product.get("status")).upper() == "ACTIVE":
                rows.append(product)
            if max_products > 0 and len(rows) >= max_products:
                return rows
        if not page.get("pageInfo", {}).get("hasNextPage"):
            break
        after = clean(page.get("pageInfo", {}).get("endCursor"))
    return rows


def variant_rows(product: dict[str, Any]) -> list[dict[str, Any]]:
    return [(edge.get("node") or {}) for edge in (((product.get("variants") or {}).get("edges")) or [])]


def option_value(variant: dict[str, Any], option_name: str) -> str:
    target = norm(option_name)
    for item in variant.get("selectedOptions") or []:
        if norm(item.get("name")) == target:
            return clean(item.get("value"))
    return ""


def is_size_option(name: str) -> bool:
    return norm(name) in {"size", "talla", "taglia", "größe", "grösse", "groesse", "taille", "maat", "rozmiar", "storlek"}


def is_type_option(name: str) -> bool:
    return norm(name) in {"type", "style", "tipo", "typ", "tyyppi", "tipo"}


def size_and_type_options(product: dict[str, Any]) -> tuple[str, str]:
    size_name = ""
    type_name = ""
    for option in product.get("options") or []:
        name = clean(option.get("name"))
        if not size_name and is_size_option(name):
            size_name = name
        if not type_name and is_type_option(name):
            type_name = name
    return size_name, type_name


def garment_key(value: str) -> str:
    text = norm(value)
    if "shirt & shorts" in text or "shirt and shorts" in text or "camisa y short" in text:
        return "shirtShortsSet"
    if re.search(r"dress|vestido|vestito|kleid|robe|jurk|rochie|sukienka|kjole|плать|فستان", text):
        return "dress"
    if re.search(r"shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص", text):
        return "shirt"
    if re.search(r"short|shorts|trunk|bermuda|шорт|شورت", text):
        return "shorts"
    if re.search(r"romper|pelele|barboteuse|strampler|pagliaccetto|rampers", text):
        return "romper"
    if re.search(r"pant|pants|trouser|pantal|hose|broek|bukse|spodnie", text):
        return "pants"
    if re.search(r"top|haut|topp", text):
        return "top"
    return ""


def sku_role(sku: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", norm(sku))
    if re.search(r"(^|-)(grl|girl|daughter)(-|$)", text):
        return "girl"
    if re.search(r"(^|-)(boy|son)(-|$)", text):
        return "boy"
    if re.search(r"(^|-)(mom|mum|mother)(-|$)", text):
        return "mother"
    if re.search(r"(^|-)(dad|father)(-|$)", text):
        return "father"
    return ""


def infer_role_from_type(type_value: str, base_role: str) -> str:
    garment = garment_key(type_value)
    if garment == "dress":
        return "mother" if base_role == "adult" else "girl"
    if garment in {"shirt", "shorts", "shirtShortsSet"}:
        return "father" if base_role == "adult" else "boy"
    return ""


def role_candidates(role: str) -> list[str]:
    values = list(ROLE_ALIASES.get(role, []))
    for labels in ROLE_LABELS_BY_LOCALE.values():
        if labels.get(role):
            values.append(labels[role])
    seen: set[str] = set()
    out = []
    for value in values:
        key = norm(value)
        if key and key not in seen:
            seen.add(key)
            out.append(value)
    return sorted(out, key=len, reverse=True)


def parse_role_size(label: str) -> tuple[str, str]:
    text = clean(label)
    for role in ["mother", "father", "girl", "boy", "child", "baby", "adult"]:
        for alias in role_candidates(role):
            escaped = re.escape(alias).replace(r"\ ", r"\s+")
            start = re.match(rf"^{escaped}(?:\s+|\s*[-–/]\s*)(.+)$", text, flags=re.I)
            end = re.match(rf"^(.+?)(?:\s+|\s*[-–/]\s*){escaped}$", text, flags=re.I)
            if start and clean(start.group(1)):
                return role, clean(start.group(1))
            if end and clean(end.group(1)):
                return role, clean(end.group(1))
    return "", text


def comparable_size_tokens(value: str) -> set[str]:
    role, size = parse_role_size(value)
    text = (
        norm(size or value)
        .replace("–", "-")
        .replace("سنتين", "2 سنة")
        .replace("سنتان", "2 سنة")
        .replace("عامين", "2 سنة")
        .replace("عامان", "2 سنة")
        .replace("شهرين", "2 شهر")
        .replace("شهران", "2 شهر")
        .replace("لام", "l")
        .replace("ميم", "m")
        .replace("إس", "s")
        .replace("اس", "s")
    )
    text = re.sub(r"(\d{1,2})\s*م(?=/|\b)", r"\1m", text)
    text = re.sub(r"(\d{1,2})\s*شهر(?:ا|ًا|ان|ين)?(?=/|\b|$)", r"\1m", text)
    tokens = {text}
    adult = re.search(r"\b(xxxxl|xxxl|xxl|[2-9]xl|xl|xs|s|m|l)\b", text, flags=re.I)
    if adult:
        token = adult.group(1).lower()
        token = {"xxl": "2xl", "xxxl": "3xl", "xxxxl": "4xl"}.get(token, token)
        tokens.add(f"adult:{token}")
    localized_adults = {
        "س": "s",
        "م": "m",
        "ل": "l",
        "小": "s",
        "小号": "s",
        "小號": "s",
        "中": "m",
        "中号": "m",
        "中號": "m",
        "大": "l",
        "長": "l",
        "长": "l",
        "大号": "l",
        "大號": "l",
    }
    if text in localized_adults:
        tokens.add(f"adult:{localized_adults[text]}")
    month = re.search(r"(?:^|[^0-9])(\d{1,2})\s*m(?:onths?)?(?:/|\b|$)", text, flags=re.I)
    if month:
        month_value = int(month.group(1))
        tokens.add(f"month:{month_value}m")
        if month_value % 12 == 0:
            year_value = month_value // 12
            tokens.add(f"age-max:{year_value}")
            tokens.add(f"toddler:{year_value}t")
    toddler = re.search(r"(?:^|[^0-9])(\d{1,2})\s*t(?:/|\b|$)", text, flags=re.I)
    if toddler:
        toddler_value = int(toddler.group(1))
        tokens.add(f"toddler:{toddler_value}t")
        tokens.add(f"age-max:{toddler_value}")
        tokens.add(f"age-range:{max(1, toddler_value - 1)}-{toddler_value}")
    age_range = re.search(
        r"(?:^|[^0-9])(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years|ano|anos|año|años|an|ans|jahr|jahre|anni|anno|jaar|år|lat|lata|ani|лет|года|год|سنة|سنوات)?(?:\b|$)",
        text,
        flags=re.I,
    )
    if age_range:
        age_min = int(age_range.group(1))
        age_max = int(age_range.group(2))
        if 0 < age_min <= age_max <= 20:
            tokens.add(f"age-min:{age_min}")
            tokens.add(f"age-max:{age_max}")
            tokens.add(f"age-range:{age_min}-{age_max}")
            tokens.add(f"toddler:{age_max}t")
    single_age = re.search(
        r"(?:^|[^0-9])(\d{1,2})\s*(?:t|y|yr|yrs|year|years|ano|anos|año|años|an|ans|jahr|jahre|anni|anno|jaar|år|lat|lata|ani|лет|года|год|سنة|سنوات)(?:\b|$)",
        text,
        flags=re.I,
    )
    if single_age:
        age_value = int(single_age.group(1))
        if 0 < age_value <= 20:
            tokens.add(f"age-min:{age_value}")
            tokens.add(f"age-max:{age_value}")
            tokens.add(f"toddler:{age_value}t")
    height = re.search(r"(?:^|[^0-9])(\d{2,3})(?:\s*cm)?(?:\b|$)", text, flags=re.I)
    if height and int(height.group(1)) >= 80:
        tokens.add(f"height-max:{int(height.group(1))}")
    nums = re.findall(r"\d+(?:[.,]\d+)?", text)
    if nums:
        tokens.add("n:" + "-".join(num.replace(",", ".").rstrip("0").rstrip(".") for num in nums))
    return tokens


def numeric_token_values(tokens: set[str], prefix: str) -> list[float]:
    values = []
    for token in tokens:
        if not token.startswith(prefix):
            continue
        try:
            values.append(float(token[len(prefix) :].replace("t", "").replace("m", "")))
        except ValueError:
            continue
    return values


def size_tokens_compatible(selected_tokens: set[str], row_tokens: set[str]) -> bool:
    if selected_tokens & row_tokens:
        return True

    selected_adults = {token for token in selected_tokens if token.startswith("adult:")}
    row_adults = {token for token in row_tokens if token.startswith("adult:")}
    if selected_adults or row_adults:
        return bool(selected_adults & row_adults)

    selected_ages = numeric_token_values(selected_tokens, "age-max:") + numeric_token_values(selected_tokens, "toddler:")
    row_ages = numeric_token_values(row_tokens, "age-max:") + numeric_token_values(row_tokens, "toddler:")
    if selected_ages and row_ages and min(abs(selected - row) for selected in selected_ages for row in row_ages) <= 2:
        return True

    selected_heights = numeric_token_values(selected_tokens, "height-max:")
    row_heights = numeric_token_values(row_tokens, "height-max:")
    if selected_heights and row_heights and min(abs(selected - row) for selected in selected_heights for row in row_heights) <= 10:
        return True

    return False


def roles_compatible(selected: str, row: str) -> bool:
    if not selected or not row or selected == row:
        return True
    if selected == "child" and row in {"girl", "boy", "baby"}:
        return True
    if selected == "adult" and row in {"mother", "father"}:
        return True
    if row == "child" and selected in {"girl", "boy", "baby"}:
        return True
    if row == "adult" and selected in {"mother", "father"}:
        return True
    return False


def table_context(table: Any) -> str:
    parts = [clean(table.get("id"))]
    previous = table.find_previous_sibling()
    while previous is not None:
        if getattr(previous, "name", "").lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            parts.append(previous.get_text(" ", strip=True))
            break
        if getattr(previous, "name", "").lower() == "table":
            break
        previous = previous.find_previous_sibling()
    return norm(" ".join(parts))


def select_table(tables: list[Any], type_value: str) -> Any | None:
    return select_table_for_role(tables, type_value, "")


def context_has_garment(context: str, selected: str) -> bool:
    text = norm(context)
    if not text or not selected:
        return False
    if selected == "dress":
        return bool(re.search(r"dress|skirt|vestido|vestito|kleid|robe|jurk|rochie|sukienka|kjole|плать|فستان", text))
    if selected == "shirt":
        return bool(re.search(r"shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص", text))
    if selected == "shorts":
        return bool(re.search(r"short|shorts|trunk|bermuda|шорт|شورت", text))
    if selected == "shirtShortsSet":
        return context_has_garment(text, "shirt") and context_has_garment(text, "shorts")
    if selected == "romper":
        return bool(re.search(r"romper|pelele|barboteuse|strampler|pagliaccetto|rampers|baby|bebé|bebe|bébé|الرضيع|بيبي", text))
    if selected == "pants":
        return bool(re.search(r"pant|pants|trouser|pantal|hose|broek|bukse|spodnie", text))
    if selected == "top":
        return bool(re.search(r"top|haut|topp", text))
    return False


def table_has_compatible_role(table: Any, expected_role: str) -> bool:
    if not expected_role:
        return False
    rows = table_matrix(table)
    if not rows:
        return False
    for row in rows:
        if not row:
            continue
        row_role, _ = parse_role_size(row[0])
        if row_role and roles_compatible(expected_role, row_role):
            return True
    for header in rows[0]:
        header_role, _ = parse_role_from_header(header)
        if header_role and roles_compatible(expected_role, header_role):
            return True
    return False


def select_table_for_role(tables: list[Any], type_value: str, expected_role: str) -> Any | None:
    if not tables:
        return None
    if len(tables) == 1:
        return tables[0]
    selected = garment_key(type_value)
    for table in tables:
        context = table_context(table)
        context_garment = garment_key(context)
        table_id = norm(table.get("id") or "")
        if selected and context_has_garment(context, selected):
            return table
        if selected == "dress" and (context_garment == "dress" or (not context_garment and table_id == "size-chart")):
            return table
        if selected in {"shirt", "shorts", "shirtShortsSet"} and context_garment in {"shirt", "shorts", "shirtShortsSet"}:
            return table
    if expected_role:
        for table in tables:
            if table_has_compatible_role(table, expected_role):
                return table
    return tables[0]


def table_rows(table: Any) -> list[list[str]]:
    rows = []
    for tr in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows[1:] if len(rows) > 1 else []


def table_matrix(table: Any) -> list[list[str]]:
    rows = []
    for tr in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows


def is_empty_guide_value(value: str) -> bool:
    text = clean(value)
    return not text or text in {"—", "-", "--"} or norm(text) == "n/a"


def parse_role_from_header(header: str) -> tuple[str, str]:
    label = re.sub(r"\s*\([^)]*\)\s*$", "", clean(header))
    if not label:
        return "", ""
    role, measurement = parse_role_size(label)
    if role and measurement:
        return role, measurement
    normalized_label = norm(label)
    for role_key in ["mother", "father", "girl", "boy", "child", "baby", "adult"]:
        for alias in role_candidates(role_key):
            normalized_alias = norm(alias)
            if len(normalized_alias) < 3:
                continue
            if re.fullmatch(r"[a-z0-9]+", normalized_alias):
                if re.search(rf"(^|[^a-z0-9]){re.escape(normalized_alias)}([^a-z0-9]|$)", normalized_label):
                    return role_key, label
            elif normalized_alias in normalized_label:
                return role_key, label
    return "", ""


def variant_matches_header_grouped_table(table: Any, expected_role: str, selected_tokens: set[str]) -> bool:
    rows = table_matrix(table)
    if len(rows) < 2:
        return False

    headers = rows[0]
    matching_columns = []
    for index, header in enumerate(headers):
        if index == 0:
            continue
        header_role, _measurement = parse_role_from_header(header)
        if header_role and roles_compatible(expected_role, header_role):
            matching_columns.append(index)

    if not matching_columns:
        return False

    for row in rows[1:]:
        if not row or not size_tokens_compatible(selected_tokens, comparable_size_tokens(row[0])):
            continue
        if any(index < len(row) and not is_empty_guide_value(row[index]) for index in matching_columns):
            return True

    return False


def variant_expected_role(variant: dict[str, Any], size_value: str, type_value: str) -> str:
    role = sku_role(clean(variant.get("sku")))
    if role:
        return role
    parsed_role, _ = parse_role_size(size_value)
    base_role = parsed_role
    if not base_role:
        tokens = comparable_size_tokens(size_value)
        base_role = "adult" if any(token.startswith("adult:") for token in tokens) else "child"
    type_role = infer_role_from_type(type_value, base_role)
    if not type_role:
        return base_role
    if not base_role or base_role in {"child", "adult"}:
        return type_role
    if base_role == "boy" and type_role == "girl":
        return type_role
    if base_role == "girl" and type_role == "boy":
        return type_role
    return base_role


def variant_matches_table(variant: dict[str, Any], size_name: str, type_name: str, html: str) -> tuple[bool, str]:
    soup = BeautifulSoup(html or "", "html.parser")
    tables = soup.select('table[id*="size-chart"], table.size-chart')
    if not tables:
        return False, "no_size_chart_table"
    size_value = option_value(variant, size_name)
    type_value = option_value(variant, type_name)
    expected_role = variant_expected_role(variant, size_value, type_value)
    selected_tokens = comparable_size_tokens(size_value)
    table = select_table_for_role(tables, type_value, expected_role)
    if not table:
        return False, "no_selected_table"
    for row in table_rows(table):
        row_role, row_size = parse_role_size(row[0])
        if not roles_compatible(expected_role, row_role):
            continue
        if size_tokens_compatible(selected_tokens, comparable_size_tokens(row_size)):
            return True, ""
    if variant_matches_header_grouped_table(table, expected_role, selected_tokens):
        return True, ""
    return False, f"no_row_match:{expected_role}:{size_value}:{type_value}"


def body_item(snapshot: Any) -> dict[str, str] | None:
    for item in snapshot.translatable_content:
        if item.get("key") == "body_html":
            return item
    return None


def audit_product(client: ShopifyClient, product: dict[str, Any], locales: list[str]) -> dict[str, Any]:
    source_html = product.get("descriptionHtml") or ""
    size_name, type_name = size_and_type_options(product)
    variants = [variant for variant in variant_rows(product) if variant.get("availableForSale")]
    row: dict[str, Any] = {
        "product_id": clean(product.get("legacyResourceId")),
        "handle": clean(product.get("handle")),
        "title": clean(product.get("title")),
        "source_has_size_chart": has_size_chart_table(source_html),
        "available_variants": len(variants),
        "variant_locale_checks": 0,
        "unmatched_count": 0,
        "unmatched": [],
    }
    if not row["source_has_size_chart"] or not size_name or not type_name:
        return row
    snapshot = client.fetch_resource(clean(product.get("id")), locales, 1)
    item = body_item(snapshot)
    for locale in locales:
        existing = snapshot.existing_translations.get((locale, "body_html"))
        html = existing.value if existing and clean(existing.value) else (item or {}).get("value", source_html)
        for variant in variants:
            ok, reason = variant_matches_table(variant, size_name, type_name, html)
            row["variant_locale_checks"] += 1
            if not ok:
                row["unmatched_count"] += 1
                if len(row["unmatched"]) < 20:
                    row["unmatched"].append(
                        {
                            "locale": locale,
                            "variant_id": clean(variant.get("legacyResourceId") or variant.get("id")),
                            "sku": clean(variant.get("sku")),
                            "title": clean(variant.get("title")),
                            "reason": reason,
                        }
                    )
    return row


def write_reports(rows: list[dict[str, Any]], report_json: Path, report_csv: Path) -> dict[str, Any]:
    summary = {
        "products_scanned": len(rows),
        "products_with_source_size_chart": sum(1 for row in rows if row["source_has_size_chart"]),
        "variant_locale_checks": sum(int(row["variant_locale_checks"]) for row in rows),
        "products_with_unmatched_variants": sum(1 for row in rows if row["unmatched_count"]),
        "unmatched_variant_locale_count": sum(int(row["unmatched_count"]) for row in rows),
    }
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_csv.parent.mkdir(parents=True, exist_ok=True)
    with report_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["product_id", "handle", "source_has_size_chart", "available_variants", "variant_locale_checks", "unmatched_count", "unmatched"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "product_id": row["product_id"],
                    "handle": row["handle"],
                    "source_has_size_chart": row["source_has_size_chart"],
                    "available_variants": row["available_variants"],
                    "variant_locale_checks": row["variant_locale_checks"],
                    "unmatched_count": row["unmatched_count"],
                    "unmatched": json.dumps(row["unmatched"], ensure_ascii=False),
                }
            )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--locales", default="")
    parser.add_argument("--handles", default="")
    parser.add_argument("--page-size", type=int, default=25)
    parser.add_argument("--max-products", type=int, default=0)
    parser.add_argument("--fail-on-unmatched", action="store_true")
    parser.add_argument("--report-json", default="dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-variant-row-repair/lanes/admin-audit/variant_row_mapping_audit.json")
    parser.add_argument("--report-csv", default="dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-variant-row-repair/lanes/admin-audit/variant_row_mapping_audit.csv")
    args = parser.parse_args()

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    locales = resolve_target_locales(client, args.locales)
    handles = [item.strip() for item in args.handles.split(",") if item.strip()]
    products = active_products(client, page_size=args.page_size, max_products=max(args.max_products, 0), handles=handles)
    rows = []
    for index, product in enumerate(products, start=1):
        rows.append(audit_product(client, product, locales))
        if index == 1 or index % 25 == 0 or index == len(products):
            print(f"[progress] {index}/{len(products)} scanned", flush=True)
    summary = write_reports(rows, Path(args.report_json), Path(args.report_csv))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.fail_on_unmatched and summary["unmatched_variant_locale_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
