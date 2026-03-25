#!/usr/bin/env python3
"""Build redirect, gone, and review CSVs from a GSC 404 export."""

from __future__ import annotations

import argparse
import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_GSC_EXPORT = Path(
    "/Users/fsuels/Downloads/https___www.dresslikemommy.com_-Coverage-Drilldown-2026-03-24/Table.csv"
)
DEFAULT_PRODUCT_EXPORT = Path("GPT/products_export_1_backfill.csv")
DEFAULT_OUTPUT_DIR = Path("ops/redirect_audit_gsc")
DEFAULT_CACHE = DEFAULT_OUTPUT_DIR / "status_cache.json"
DEFAULT_LIVE_PATHS_JSON = DEFAULT_OUTPUT_DIR / "live_path_sets.json"
DEFAULT_BASE_URL = "https://www.dresslikemommy.com"

ROOT_SEGMENTS = {"products", "collections", "pages", "account"}
ACCOUNT_PATHS = {"/account/login", "/account/register"}
HOME_PATHS = {"/"}

ROOT_TARGETS = {
    "bottoms": "/collections/bottoms",
    "daddy_general": "/collections/daddy-and-me",
    "daddy_tees": "/collections/daddy-me-t-shirts",
    "dresses": "/collections/dresses",
    "family_sets": "/collections/family-sets",
    "family_tops": "/collections/family-tops",
    "jumpsuits": "/collections/jumpsuits",
    "leggings": "/collections/leggings",
    "matching_outfits": "/collections/matching-outfits",
    "maternity": "/collections/maternity",
    "maxi_dresses": "/collections/maxi-dresses",
    "midi_dresses": "/collections/midi-dresses",
    "mini_dresses": "/collections/mini-dresses",
    "mommy_me": "/collections/mommy-and-me",
    "pajamas": "/collections/family-pajamas",
    "pants": "/collections/pants",
    "popular_family_matching": "/collections/popular-family-matching",
    "popular_mommy_me": "/collections/popular-mommy-me-1",
    "rompers": "/collections/rompers",
    "skirts": "/collections/skirts",
    "sundresses": "/collections/sundresses",
    "sweaters": "/collections/sweaters",
    "swimsuits": "/collections/swimsuits",
    "tops": "/collections/tops",
    "trunks": "/collections/trunks",
}

COLLECTION_HANDLE_MAP = {
    "casual-dresses": ROOT_TARGETS["dresses"],
    "daddy-me-shorts": ROOT_TARGETS["trunks"],
    "family-matching": ROOT_TARGETS["popular_family_matching"],
    "family-matching-pajamas": ROOT_TARGETS["pajamas"],
    "family-matching-sets": ROOT_TARGETS["family_sets"],
    "family-matching-sweaters-jackets": ROOT_TARGETS["sweaters"],
    "family-matching-swimsuits": ROOT_TARGETS["swimsuits"],
    "family-matching-t-shirts": ROOT_TARGETS["family_tops"],
    "jumpers": ROOT_TARGETS["jumpsuits"],
    "maternity-dresses": ROOT_TARGETS["maternity"],
    "mommy-me": ROOT_TARGETS["mommy_me"],
    "popular-mommy-me": ROOT_TARGETS["popular_mommy_me"],
    "swimwear": ROOT_TARGETS["swimsuits"],
}

PAGE_HANDLE_MAP = {
    "shipping-and-delivery": "/pages/shipping-info",
    "wholesale-drop-shipping": ROOT_TARGETS["dresses"],
}

HARD_HOME_REDIRECTS = {
    "/${t}",
    "/b",
    "/comments",
    "/interfaces/interfacestore.php",
    "/paginfo@dresslikemommy.com",
    "/s",
    "/thank_you",
}

FESTIVE_TOKENS = {
    "christmas",
    "xmas",
    "reindeer",
    "santa",
    "grinch",
    "elf",
    "fair isle",
    "snowflake",
    "holiday",
}
DRAGON_TOKENS = {"dragon"}
DADDY_TOKENS = {
    "daddy and me",
    "daddy-me",
    "daddy me",
    "dad and",
    "father and",
    "father-son",
    "father son",
    "dad and son",
    "dads and",
}
MOMMY_TOKENS = {
    "mommy and me",
    "mommy-me",
    "mom and me",
    "mommy me",
    "mother daughter",
    "mother-daughter",
    "mom daughter",
    "mom-daughter",
}
SWIM_TOKENS = {
    "swim",
    "swimsuit",
    "swimwear",
    "bikini",
    "one-piece",
    "one piece",
    "bathing",
    "beachwear",
    "tankini",
}
TRUNK_TOKENS = {
    "trunk",
    "trunks",
    "swim short",
    "swim shorts",
    "board short",
    "board shorts",
}
TEE_TOKENS = {
    "t-shirt",
    "t shirt",
    "t-shirts",
    "t shirts",
    "tee",
    "tees",
    "graphic tee",
}
SHIRT_TOKENS = {
    "shirt",
    "shirts",
    "button-down",
    "button down",
    "button-up",
    "button up",
    "top",
    "tops",
    "sweatshirt",
    "sweatshirts",
}
SWEATER_TOKENS = {
    "sweater",
    "sweaters",
    "jacket",
    "jackets",
    "coat",
    "coats",
    "hoodie",
    "hoodies",
    "cardigan",
    "cardigans",
    "pullover",
    "pullovers",
    "fleece",
    "vest",
    "knit",
    "knitwear",
    "knitted",
}
PAJAMA_TOKENS = {
    "pajama",
    "pajamas",
    "sleepwear",
    "sleep set",
    "home wear",
    "loungewear",
    "pjs",
}
DRESS_TOKENS = {"dress", "dresses", "gown"}
MAXI_TOKENS = {"maxi"}
MIDI_TOKENS = {"midi", "knee-length", "knee length"}
MINI_TOKENS = {"mini"}
SUNDRESS_TOKENS = {"sundress", "sundresses"}
MATERNITY_TOKENS = {"maternity"}
JUMPSUIT_TOKENS = {"jumpsuit", "jumpsuits"}
ROMPER_TOKENS = {"romper", "rompers"}
SKIRT_TOKENS = {"skirt", "skirts"}
LEGGING_TOKENS = {"legging", "leggings"}
PANT_TOKENS = {"pant", "pants", "trouser", "trousers"}
BOTTOM_TOKENS = {"bottom", "bottoms"}
SET_TOKENS = {"set", "sets", "outfit", "outfits"}
ACCESSORY_TOKENS = {
    "headband",
    "headbands",
    "hat",
    "hats",
    "beanie",
    "beanies",
    "scarf",
    "scarves",
    "bracelet",
    "bracelets",
    "charm",
    "charms",
    "keychain",
    "keychains",
    "pendant",
    "pendants",
}


@dataclass
class ProductRecord:
    handle: str
    title: str
    published: str
    status: str
    category1: str
    subcategory: str
    subcategory2: str
    product_type: str
    style: str
    pattern: str
    tags: str

    @property
    def text_blob(self) -> str:
        parts = [
            self.handle,
            self.title,
            self.category1,
            self.subcategory,
            self.subcategory2,
            self.product_type,
            self.style,
            self.pattern,
            self.tags,
        ]
        return " | ".join(part.strip().lower() for part in parts if part and part.strip())


@dataclass
class GscPathRecord:
    path: str
    occurrences: int
    last_crawled: str
    sample_url: str
    query_examples: str


@dataclass
class StatusResult:
    status: str
    location: str
    checked_at: int


@dataclass
class Decision:
    bucket: str
    reason: str
    confidence: str
    target: str = ""
    kind: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gsc-export", type=Path, default=DEFAULT_GSC_EXPORT, help="GSC Table.csv export")
    parser.add_argument(
        "--product-export",
        type=Path,
        default=DEFAULT_PRODUCT_EXPORT,
        help="Historical Shopify product export for metadata lookups",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for generated files")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache for live status checks")
    parser.add_argument(
        "--live-paths-json",
        type=Path,
        default=DEFAULT_LIVE_PATHS_JSON,
        help="Cached JSON snapshot of live product/collection/page paths",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Storefront origin")
    parser.add_argument(
        "--status-overrides-csv",
        type=Path,
        default=None,
        help="Optional CSV with Path,Status,Location overrides from targeted live verification",
    )
    parser.add_argument("--timeout", type=int, default=12, help="Per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent live status checks")
    parser.add_argument("--retries", type=int, default=3, help="Retries for rate-limited/network checks")
    parser.add_argument(
        "--verify-live-status",
        action="store_true",
        help="HEAD-check each source path against the live storefront instead of trusting the GSC export status",
    )
    parser.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Ignore the existing status cache and recheck all paths",
    )
    return parser.parse_args()


def normalize_handle(value: str) -> str:
    return value.strip().lower()


def load_products(export_path: Path) -> dict[str, ProductRecord]:
    products: dict[str, ProductRecord] = {}
    if not export_path.exists():
        return products

    with export_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            product_handle = normalize_handle(row.get("Handle") or "")
            if not product_handle or product_handle in products:
                continue
            products[product_handle] = ProductRecord(
                handle=product_handle,
                title=(row.get("Title") or "").strip(),
                published=(row.get("Published") or "").strip().lower(),
                status=(row.get("Status") or "").strip().lower(),
                category1=(row.get("Category1 (product.metafields.custom.category1)") or "").strip(),
                subcategory=(row.get("SubCategory (product.metafields.custom.subcategory)") or "").strip(),
                subcategory2=(row.get("SubCategory2 (product.metafields.custom.subcategory2)") or "").strip(),
                product_type=(row.get("Type (product.metafields.custom.type)") or row.get("Type") or "").strip(),
                style=(row.get("Style (product.metafields.custom.style)") or "").strip(),
                pattern=(row.get("Pattern (product.metafields.custom.pattern)") or "").strip(),
                tags=(row.get("Tags") or "").strip(),
            )
    return products


def load_gsc_paths(gsc_path: Path) -> dict[str, GscPathRecord]:
    records: dict[str, GscPathRecord] = {}
    with gsc_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_url = (row.get("URL") or "").strip()
            if not raw_url:
                continue
            split = urllib.parse.urlsplit(raw_url)
            path = split.path or "/"
            query = split.query
            last_crawled = (row.get("Last crawled") or "").strip()
            existing = records.get(path)
            if existing is None:
                records[path] = GscPathRecord(
                    path=path,
                    occurrences=1,
                    last_crawled=last_crawled,
                    sample_url=raw_url,
                    query_examples=query[:500],
                )
                continue

            existing.occurrences += 1
            if last_crawled and last_crawled > existing.last_crawled:
                existing.last_crawled = last_crawled
                existing.sample_url = raw_url
            if query:
                queries = set(filter(None, existing.query_examples.split(" | ")))
                queries.add(query)
                existing.query_examples = " | ".join(sorted(queries)[:5])
    return records


def load_cache(cache_path: Path) -> dict[str, StatusResult]:
    if not cache_path.exists():
        return {}
    raw = json.loads(cache_path.read_text(encoding="utf-8"))
    cache: dict[str, StatusResult] = {}
    for path, payload in raw.items():
        cache[path] = StatusResult(
            status=str(payload.get("status", "")),
            location=str(payload.get("location", "")),
            checked_at=int(payload.get("checked_at", 0)),
        )
    return cache


def load_status_overrides(path: Path | None) -> dict[str, StatusResult]:
    if path is None or not path.exists():
        return {}

    overrides: dict[str, StatusResult] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source_path = (row.get("Path") or "").strip()
            status = (row.get("Status") or "").strip()
            if not source_path or not status:
                continue
            overrides[source_path] = StatusResult(
                status=status,
                location=(row.get("Location") or "").strip(),
                checked_at=int(time.time()),
            )
    return overrides


def save_cache(cache_path: Path, cache: dict[str, StatusResult]) -> None:
    serializable = {
        path: {
            "status": value.status,
            "location": value.location,
            "checked_at": value.checked_at,
        }
        for path, value in sorted(cache.items())
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(serializable, indent=2, sort_keys=True), encoding="utf-8")


def build_opener() -> urllib.request.OpenerDirector:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    context = ssl.create_default_context()
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context), NoRedirect)


def fetch_status(base_url: str, path: str, timeout: int, retries: int) -> StatusResult:
    last_result: StatusResult | None = None
    normalized_path = path if path.startswith("/") else f"/{path}"

    for attempt in range(retries):
        opener = build_opener()
        request = urllib.request.Request(
            f"{base_url}{normalized_path}",
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        try:
            with opener.open(request, timeout=timeout) as response:
                result = StatusResult(
                    status=str(response.status),
                    location=response.headers.get("Location", ""),
                    checked_at=int(time.time()),
                )
        except urllib.error.HTTPError as error:
            result = StatusResult(
                status=str(error.code),
                location=error.headers.get("Location", ""),
                checked_at=int(time.time()),
            )
        except Exception as error:  # pragma: no cover - network-dependent
            result = StatusResult(
                status=f"ERR:{type(error).__name__}",
                location=str(error),
                checked_at=int(time.time()),
            )

        last_result = result
        if result.status not in {"429", "ERR:TimeoutError", "ERR:URLError"}:
            return result
        if attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))

    assert last_result is not None
    return last_result


def fetch_text(url: str, timeout: int = 20, retries: int = 4) -> str:
    last_error: Exception | None = None
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code != 429 or attempt >= retries - 1:
                raise
        except Exception as error:  # pragma: no cover - network-dependent
            last_error = error
            if attempt >= retries - 1:
                raise
        time.sleep(1.5 * (attempt + 1))

    assert last_error is not None
    raise last_error


def parse_sitemap_index(base_url: str) -> dict[str, dict[str, str]]:
    xml_text = fetch_text(f"{base_url}/sitemap.xml")
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls: dict[str, dict[str, str]] = {}

    for loc in root.findall("sm:sitemap/sm:loc", ns):
        value = loc.text or ""
        parsed = urllib.parse.urlsplit(value)
        parts = [part for part in parsed.path.split("/") if part]
        if not parts:
            continue
        locale = ""
        filename = parts[-1]
        if len(parts) == 2:
            locale = parts[0]
        if filename.startswith("sitemap_products_"):
            sitemap_urls.setdefault(locale, {})["products"] = value
        elif filename.startswith("sitemap_collections_"):
            sitemap_urls.setdefault(locale, {})["collections"] = value
        elif filename.startswith("sitemap_pages_"):
            sitemap_urls.setdefault(locale, {})["pages"] = value
    return sitemap_urls


def parse_sitemap_paths(sitemap_url: str) -> set[str]:
    xml_text = fetch_text(sitemap_url)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths: set[str] = set()
    for loc in root.findall("sm:url/sm:loc", ns):
        value = loc.text or ""
        path = urllib.parse.urlsplit(value).path
        if path:
            paths.add(path)
    return paths


def load_live_path_sets(base_url: str) -> dict[str, set[str]]:
    sitemap_urls = parse_sitemap_index(base_url)
    sets: dict[str, set[str]] = {
        "active_locales": set(),
        "product_paths": set(),
        "collection_paths": set(),
        "page_paths": set(),
    }

    for locale, url_map in sitemap_urls.items():
        if locale:
            sets["active_locales"].add(locale)
        if "products" in url_map:
            sets[f"product_paths:{locale}"] = parse_sitemap_paths(url_map["products"])
            sets["product_paths"].update(sets[f"product_paths:{locale}"])
        if "collections" in url_map:
            sets[f"collection_paths:{locale}"] = parse_sitemap_paths(url_map["collections"])
            sets["collection_paths"].update(sets[f"collection_paths:{locale}"])
        if "pages" in url_map:
            sets[f"page_paths:{locale}"] = parse_sitemap_paths(url_map["pages"])
            sets["page_paths"].update(sets[f"page_paths:{locale}"])
    return sets


def serialize_live_sets(live_sets: dict[str, set[str]]) -> dict[str, list[str]]:
    return {key: sorted(values) for key, values in live_sets.items()}


def deserialize_live_sets(payload: dict[str, list[str]]) -> dict[str, set[str]]:
    return {key: set(values) for key, values in payload.items()}


def has_any_token(text: str, tokens: set[str]) -> bool:
    return any(token in text for token in tokens)


def is_active_locale(prefix: str, live_sets: dict[str, set[str]]) -> bool:
    return prefix in live_sets["active_locales"]


def extract_prefix(parts: list[str]) -> tuple[str, list[str]]:
    if len(parts) >= 2 and parts[0] not in ROOT_SEGMENTS and parts[1] in ROOT_SEGMENTS:
        return parts[0], parts[1:]
    return "", parts


def extract_product_handle(parts: list[str]) -> str:
    if "products" not in parts:
        return ""
    idx = parts.index("products")
    if len(parts) <= idx + 1:
        return ""
    return normalize_handle(parts[idx + 1])


def extract_collection_handle(parts: list[str]) -> str:
    if "collections" not in parts:
        return ""
    idx = parts.index("collections")
    if len(parts) <= idx + 1:
        return ""
    return normalize_handle(parts[idx + 1])


def extract_page_handle(parts: list[str]) -> str:
    if "pages" not in parts:
        return ""
    idx = parts.index("pages")
    if len(parts) <= idx + 1:
        return ""
    return normalize_handle(parts[idx + 1])


def target_with_locale(
    root_target: str,
    prefix: str,
    live_sets: dict[str, set[str]],
    target_kind: str,
) -> str:
    if not prefix or not is_active_locale(prefix, live_sets):
        return root_target
    localized = f"/{prefix}{root_target}"
    key = f"{target_kind}:{prefix}"
    if localized in live_sets.get(key, set()):
        return localized
    return root_target


def build_product_text(handle: str, product: ProductRecord | None) -> str:
    if product:
        return product.text_blob
    return handle.replace("-", " ").lower()


def classify_dead_product(
    handle: str,
    product: ProductRecord | None,
    prefix: str,
    live_sets: dict[str, set[str]],
) -> Decision:
    handle_text = handle.replace("-", " ").lower()
    text = build_product_text(handle, product)

    handle_type_flags = {
        "accessory": has_any_token(handle_text, ACCESSORY_TOKENS),
        "swim": has_any_token(handle_text, SWIM_TOKENS),
        "trunks": has_any_token(handle_text, TRUNK_TOKENS),
        "tee": has_any_token(handle_text, TEE_TOKENS),
        "shirt": has_any_token(handle_text, SHIRT_TOKENS),
        "sweater": has_any_token(handle_text, SWEATER_TOKENS),
        "pajama": has_any_token(handle_text, PAJAMA_TOKENS),
        "dress": has_any_token(handle_text, DRESS_TOKENS),
        "sundress": has_any_token(handle_text, SUNDRESS_TOKENS),
        "maxi": has_any_token(handle_text, MAXI_TOKENS),
        "midi": has_any_token(handle_text, MIDI_TOKENS),
        "mini": has_any_token(handle_text, MINI_TOKENS),
        "jumpsuit": has_any_token(handle_text, JUMPSUIT_TOKENS),
        "romper": has_any_token(handle_text, ROMPER_TOKENS),
        "skirt": has_any_token(handle_text, SKIRT_TOKENS),
        "legging": has_any_token(handle_text, LEGGING_TOKENS),
        "pant": has_any_token(handle_text, PANT_TOKENS),
        "bottom": has_any_token(handle_text, BOTTOM_TOKENS),
        "set": has_any_token(handle_text, SET_TOKENS),
    }
    handle_has_explicit_type = any(handle_type_flags.values())

    def choose_type_flag(tokens: set[str], handle_key: str) -> bool:
        full_flag = has_any_token(text, tokens)
        if handle_has_explicit_type:
            return handle_type_flags[handle_key]
        return full_flag

    is_festive = has_any_token(handle_text, FESTIVE_TOKENS) or has_any_token(text, FESTIVE_TOKENS)
    is_dragon = has_any_token(handle_text, DRAGON_TOKENS) or has_any_token(text, DRAGON_TOKENS)
    is_daddy = has_any_token(handle_text, DADDY_TOKENS) or has_any_token(text, DADDY_TOKENS) or "daddy and me" in text or "father son" in text
    is_mommy = has_any_token(handle_text, MOMMY_TOKENS) or has_any_token(text, MOMMY_TOKENS)
    is_trunks = choose_type_flag(TRUNK_TOKENS, "trunks")
    is_swim = choose_type_flag(SWIM_TOKENS, "swim")
    has_tee_terms = choose_type_flag(TEE_TOKENS, "tee")
    has_shirt_terms = choose_type_flag(SHIRT_TOKENS, "shirt")
    is_sweater = choose_type_flag(SWEATER_TOKENS, "sweater")
    is_pajama = choose_type_flag(PAJAMA_TOKENS, "pajama")
    is_maternity = has_any_token(handle_text, MATERNITY_TOKENS) or has_any_token(text, MATERNITY_TOKENS)
    is_maxi = choose_type_flag(MAXI_TOKENS, "maxi")
    is_midi = choose_type_flag(MIDI_TOKENS, "midi")
    is_mini = choose_type_flag(MINI_TOKENS, "mini")
    is_sundress = choose_type_flag(SUNDRESS_TOKENS, "sundress")
    is_dress = choose_type_flag(DRESS_TOKENS, "dress")
    is_jumpsuit = choose_type_flag(JUMPSUIT_TOKENS, "jumpsuit")
    is_romper = choose_type_flag(ROMPER_TOKENS, "romper")
    is_skirt = choose_type_flag(SKIRT_TOKENS, "skirt")
    is_legging = choose_type_flag(LEGGING_TOKENS, "legging")
    is_pant = choose_type_flag(PANT_TOKENS, "pant")
    is_bottom = choose_type_flag(BOTTOM_TOKENS, "bottom")
    is_set = choose_type_flag(SET_TOKENS, "set")
    is_accessory = choose_type_flag(ACCESSORY_TOKENS, "accessory")

    if is_festive:
        return Decision(bucket="gone", reason="seasonal_festive_product", confidence="high", kind="product")
    if is_dragon:
        return Decision(bucket="gone", reason="dragon_novelty_product", confidence="high", kind="product")
    if is_accessory:
        return Decision(bucket="gone", reason="accessory_without_replacement", confidence="medium", kind="product")
    if is_daddy and is_trunks:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_swim_trunks",
            confidence="high",
            target=target_with_locale(ROOT_TARGETS["trunks"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_swim:
        return Decision(
            bucket="redirect",
            reason="swimwear_category_match",
            confidence="high",
            target=target_with_locale(ROOT_TARGETS["swimsuits"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_daddy and has_tee_terms:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_tshirt_match",
            confidence="high",
            target=target_with_locale(ROOT_TARGETS["daddy_tees"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_daddy and has_shirt_terms:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_general_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["daddy_general"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_sweater:
        return Decision(
            bucket="redirect",
            reason="sweater_or_outerwear_match",
            confidence="high",
            target=target_with_locale(ROOT_TARGETS["sweaters"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_pajama:
        return Decision(
            bucket="redirect",
            reason="pajama_category_match",
            confidence="high",
            target=target_with_locale(ROOT_TARGETS["pajamas"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_maternity:
        return Decision(
            bucket="redirect",
            reason="maternity_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["maternity"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_romper:
        return Decision(
            bucket="redirect",
            reason="romper_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["rompers"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_jumpsuit:
        return Decision(
            bucket="redirect",
            reason="jumpsuit_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["jumpsuits"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_dress and is_maxi:
        return Decision(
            bucket="redirect",
            reason="maxi_dress_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["maxi_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_dress and is_midi:
        return Decision(
            bucket="redirect",
            reason="midi_dress_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["midi_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_dress and is_mini:
        return Decision(
            bucket="redirect",
            reason="mini_dress_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["mini_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_sundress:
        return Decision(
            bucket="redirect",
            reason="sundress_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["sundresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_dress:
        general_dress_target = ROOT_TARGETS["mommy_me"] if is_mommy else ROOT_TARGETS["dresses"]
        return Decision(
            bucket="redirect",
            reason="dress_category_match",
            confidence="medium",
            target=target_with_locale(general_dress_target, prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_maxi:
        return Decision(
            bucket="redirect",
            reason="maxi_dress_category_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["maxi_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_midi:
        return Decision(
            bucket="redirect",
            reason="midi_dress_category_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["midi_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_mini:
        return Decision(
            bucket="redirect",
            reason="mini_dress_category_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["mini_dresses"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_skirt:
        return Decision(
            bucket="redirect",
            reason="skirt_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["skirts"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_legging:
        return Decision(
            bucket="redirect",
            reason="legging_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["leggings"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_pant:
        return Decision(
            bucket="redirect",
            reason="pants_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["pants"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_bottom:
        return Decision(
            bucket="redirect",
            reason="bottoms_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["bottoms"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if has_tee_terms or has_shirt_terms:
        return Decision(
            bucket="redirect",
            reason="tops_category_match",
            confidence="medium",
            target=target_with_locale(ROOT_TARGETS["family_tops"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_set:
        fallback = ROOT_TARGETS["family_sets"] if "set" in text or "sets" in text else ROOT_TARGETS["matching_outfits"]
        return Decision(
            bucket="redirect",
            reason="set_or_outfit_category_match",
            confidence="medium",
            target=target_with_locale(fallback, prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_daddy:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_general_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["daddy_general"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if is_mommy:
        return Decision(
            bucket="redirect",
            reason="mommy_and_me_general_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["mommy_me"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    if "family matching" in handle_text or "family matching" in text:
        return Decision(
            bucket="redirect",
            reason="family_matching_general_match",
            confidence="low",
            target=target_with_locale(ROOT_TARGETS["popular_family_matching"], prefix, live_sets, "collection_paths"),
            kind="product",
        )
    return Decision(bucket="review", reason="no_safe_product_rule_match", confidence="low", kind="product")


def classify_collection_path(
    collection_handle: str,
    prefix: str,
    live_sets: dict[str, set[str]],
) -> Decision:
    root_collection = f"/collections/{collection_handle}"
    localized_root_collection = target_with_locale(root_collection, prefix, live_sets, "collection_paths")
    if localized_root_collection in live_sets["collection_paths"]:
        return Decision(
            bucket="redirect",
            reason="live_collection_canonical",
            confidence="high",
            target=localized_root_collection,
            kind="collection",
        )

    mapped = COLLECTION_HANDLE_MAP.get(collection_handle)
    if mapped:
        return Decision(
            bucket="redirect",
            reason="mapped_dead_collection_handle",
            confidence="high",
            target=target_with_locale(mapped, prefix, live_sets, "collection_paths"),
            kind="collection",
        )

    text = collection_handle.replace("-", " ")
    if has_any_token(text, SWIM_TOKENS):
        target = ROOT_TARGETS["swimsuits"]
        reason = "collection_swim_rule"
    elif has_any_token(text, PAJAMA_TOKENS):
        target = ROOT_TARGETS["pajamas"]
        reason = "collection_pajama_rule"
    elif has_any_token(text, SWEATER_TOKENS):
        target = ROOT_TARGETS["sweaters"]
        reason = "collection_outerwear_rule"
    elif has_any_token(text, DRESS_TOKENS):
        target = ROOT_TARGETS["dresses"]
        reason = "collection_dress_rule"
    elif has_any_token(text, TEE_TOKENS | SHIRT_TOKENS):
        target = ROOT_TARGETS["family_tops"]
        reason = "collection_tops_rule"
    elif "mommy me" in text or "mommy and me" in text or "mother daughter" in text:
        target = ROOT_TARGETS["mommy_me"]
        reason = "collection_mommy_me_rule"
    else:
        return Decision(bucket="review", reason="no_safe_collection_rule_match", confidence="low", kind="collection")

    return Decision(
        bucket="redirect",
        reason=reason,
        confidence="medium",
        target=target_with_locale(target, prefix, live_sets, "collection_paths"),
        kind="collection",
    )


def classify_page_path(page_handle: str, prefix: str, live_sets: dict[str, set[str]]) -> Decision:
    root_page = f"/pages/{page_handle}"
    localized_root_page = target_with_locale(root_page, prefix, live_sets, "page_paths")
    if localized_root_page in live_sets["page_paths"]:
        return Decision(
            bucket="redirect",
            reason="live_page_canonical",
            confidence="high",
            target=localized_root_page,
            kind="page",
        )

    mapped = PAGE_HANDLE_MAP.get(page_handle)
    if mapped:
        target_kind = "page_paths" if mapped.startswith("/pages/") else "collection_paths"
        return Decision(
            bucket="redirect",
            reason="mapped_dead_page_handle",
            confidence="high",
            target=target_with_locale(mapped, prefix, live_sets, target_kind),
            kind="page",
        )

    return Decision(bucket="review", reason="no_safe_page_rule_match", confidence="low", kind="page")


def classify_misc_path(path: str) -> Decision:
    normalized = path.lower().rstrip("/") or "/"
    if normalized in HARD_HOME_REDIRECTS or normalized.startswith("/interfaces/"):
        return Decision(bucket="redirect", reason="hardcoded_misc_home_redirect", confidence="medium", target="/", kind="misc")
    return Decision(bucket="review", reason="unexpected_non_catalog_path", confidence="low", kind="misc")


def classify_record(
    record: GscPathRecord,
    status: StatusResult,
    products: dict[str, ProductRecord],
    live_sets: dict[str, set[str]],
) -> Decision:
    if status.status == "200":
        return Decision(bucket="live", reason="still_live", confidence="high")
    if status.status in {"301", "302", "307", "308"}:
        return Decision(
            bucket="already_redirected",
            reason="storefront_redirect_exists",
            confidence="high",
            target=status.location,
        )
    if status.status != "404":
        return Decision(bucket="review", reason=f"unexpected_status_{status.status}", confidence="low")

    parts = [part for part in record.path.split("/") if part]
    prefix, remainder = extract_prefix(parts)

    if "products" in remainder:
        handle = extract_product_handle(remainder)
        if not handle:
            return Decision(bucket="review", reason="missing_product_handle", confidence="low", kind="product")

        canonical_path = f"/products/{handle}"
        localized_canonical_path = target_with_locale(canonical_path, prefix, live_sets, "product_paths")
        if localized_canonical_path in live_sets["product_paths"]:
            return Decision(
                bucket="redirect",
                reason="live_product_canonical",
                confidence="high",
                target=localized_canonical_path,
                kind="product",
            )

        return classify_dead_product(handle, products.get(handle), prefix, live_sets)

    if "collections" in remainder:
        collection_handle = extract_collection_handle(remainder)
        if not collection_handle:
            return Decision(bucket="review", reason="missing_collection_handle", confidence="low", kind="collection")
        return classify_collection_path(collection_handle, prefix, live_sets)

    if "pages" in remainder:
        page_handle = extract_page_handle(remainder)
        if not page_handle:
            return Decision(bucket="review", reason="missing_page_handle", confidence="low", kind="page")
        return classify_page_path(page_handle, prefix, live_sets)

    if remainder[:2] == ["account", "register"]:
        return Decision(
            bucket="redirect",
            reason="account_register_variant",
            confidence="high",
            target="/account/register",
            kind="account",
        )
    if remainder[:2] == ["account", "login"]:
        return Decision(
            bucket="redirect",
            reason="account_login_variant",
            confidence="high",
            target="/account/login",
            kind="account",
        )
    if len(parts) == 1 and re.fullmatch(r"[a-z]{2}(?:-[a-z]{2})?", parts[0]):
        return Decision(bucket="redirect", reason="legacy_locale_root_to_home", confidence="medium", target="/", kind="misc")
    if remainder and remainder[0] in {"es", "fr"} and len(remainder) == 1:
        return Decision(bucket="redirect", reason="bare_locale_to_home", confidence="medium", target=f"/{remainder[0]}/", kind="misc")
    if prefix and not remainder:
        return Decision(bucket="redirect", reason="legacy_locale_root_to_home", confidence="medium", target="/", kind="misc")
    return classify_misc_path(record.path)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_row_common(record: GscPathRecord, status: StatusResult, decision: Decision) -> dict[str, str]:
    return {
        "Path": record.path,
        "Occurrences": str(record.occurrences),
        "Last crawled": record.last_crawled,
        "Sample URL": record.sample_url,
        "Query examples": record.query_examples,
        "Live status": status.status,
        "Live location": status.location,
        "Decision": decision.bucket,
        "Kind": decision.kind,
        "Reason": decision.reason,
        "Confidence": decision.confidence,
        "Target": decision.target,
    }


def write_summary(
    output_path: Path,
    gsc_records: dict[str, GscPathRecord],
    statuses: dict[str, StatusResult],
    decisions: dict[str, Decision],
) -> None:
    status_counts = Counter(status.status for status in statuses.values())
    bucket_counts = Counter(decision.bucket for decision in decisions.values())
    kind_counts = Counter(decision.kind for decision in decisions.values() if decision.kind)
    redirect_target_counts = Counter(
        decision.target for decision in decisions.values() if decision.bucket == "redirect" and decision.target
    )
    total_rows = sum(record.occurrences for record in gsc_records.values())

    lines = [
        "# GSC 404 Audit",
        "",
        f"- Generated at: `{time.strftime('%Y-%m-%d %H:%M:%S %Z')}`",
        f"- Source export: `{DEFAULT_GSC_EXPORT}`",
        f"- Raw GSC rows: `{total_rows}`",
        f"- Unique source paths audited: `{len(gsc_records)}`",
        "",
        "## Live Status Counts",
        "",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: `{count}`")

    lines.extend(["", "## Decision Buckets", ""])
    for bucket, count in sorted(bucket_counts.items()):
        lines.append(f"- `{bucket}`: `{count}`")

    if kind_counts:
        lines.extend(["", "## Path Kinds", ""])
        for kind, count in sorted(kind_counts.items()):
            lines.append(f"- `{kind}`: `{count}`")

    if redirect_target_counts:
        lines.extend(["", "## Redirect Targets", ""])
        for target, count in sorted(redirect_target_counts.items()):
            lines.append(f"- `{target}`: `{count}`")

    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            "- `shopify_url_redirects.csv`: import-ready redirect rows for Shopify admin.",
            "- `redirect_candidates_detailed.csv`: redirect rows with GSC counts, reasons, and current live status.",
            "- `gone_candidates.csv`: URLs that should stay removed rather than be redirected.",
            "- `manual_review.csv`: URLs without a safe automatic rule.",
            "- `already_resolved.csv`: URLs that are already live or already redirect.",
            "",
            "## Notes",
            "",
            "- Query-string variants are collapsed to one source path because Shopify redirects are path-based.",
            "- Default runs trust the GSC `Not found (404)` export and do not re-HEAD every path unless `--verify-live-status` is supplied.",
            "- Seasonal holiday and dragon novelty products are intentionally kept out of the import CSV.",
            "- Exact locale/product/page variants redirect to a live localized path only when the locale currently exists in the sitemap; otherwise they fall back to the root canonical path.",
        ]
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    gsc_records = load_gsc_paths(args.gsc_export)
    products = load_products(args.product_export)
    if args.live_paths_json.exists():
        live_sets = deserialize_live_sets(json.loads(args.live_paths_json.read_text(encoding="utf-8")))
    else:
        live_sets = load_live_path_sets(args.base_url)
        args.live_paths_json.parent.mkdir(parents=True, exist_ok=True)
        args.live_paths_json.write_text(
            json.dumps(serialize_live_sets(live_sets), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    status_overrides = load_status_overrides(args.status_overrides_csv)
    if args.verify_live_status:
        cache = {} if args.refresh_cache else load_cache(args.cache)
        cache.update(status_overrides)

        uncached_paths = [
            path
            for path in gsc_records
            if path not in cache or cache[path].status == "429" or cache[path].status.startswith("ERR:")
        ]
        if uncached_paths:
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                future_map = {
                    executor.submit(fetch_status, args.base_url, path, args.timeout, args.retries): path
                    for path in uncached_paths
                }
                for future in as_completed(future_map):
                    cache[future_map[future]] = future.result()
            save_cache(args.cache, cache)
    else:
        cache = {
            path: status_overrides.get(path, StatusResult(status="404", location="", checked_at=0))
            for path in gsc_records
        }

    decisions: dict[str, Decision] = {}
    redirect_rows: list[dict[str, str]] = []
    redirect_details: list[dict[str, str]] = []
    gone_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    resolved_rows: list[dict[str, str]] = []

    for path, record in sorted(gsc_records.items()):
        status = cache[path]
        decision = classify_record(record, status, products, live_sets)
        decisions[path] = decision
        common = build_row_common(record, status, decision)

        if decision.bucket == "redirect":
            redirect_rows.append({"Redirect from": path, "Redirect to": decision.target})
            redirect_details.append(common)
        elif decision.bucket == "gone":
            gone_rows.append(common)
        elif decision.bucket == "review":
            review_rows.append(common)
        else:
            resolved_rows.append(common)

    detail_fields = [
        "Path",
        "Occurrences",
        "Last crawled",
        "Sample URL",
        "Query examples",
        "Live status",
        "Live location",
        "Decision",
        "Kind",
        "Reason",
        "Confidence",
        "Target",
    ]

    write_csv(args.output_dir / "shopify_url_redirects.csv", redirect_rows, ["Redirect from", "Redirect to"])
    write_csv(args.output_dir / "redirect_candidates_detailed.csv", redirect_details, detail_fields)
    write_csv(args.output_dir / "gone_candidates.csv", gone_rows, detail_fields)
    write_csv(args.output_dir / "manual_review.csv", review_rows, detail_fields)
    write_csv(args.output_dir / "already_resolved.csv", resolved_rows, detail_fields)
    write_summary(args.output_dir / "summary.md", gsc_records, cache, decisions)

    print(f"Audited {len(gsc_records)} unique source paths from {sum(r.occurrences for r in gsc_records.values())} GSC rows")
    print(f"Generated {len(redirect_rows)} redirect rows")
    print(f"Generated {len(gone_rows)} gone candidates")
    print(f"Generated {len(review_rows)} manual review rows")
    print(f"Recorded {len(resolved_rows)} live/already-resolved rows")
    print(f"Output directory: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
