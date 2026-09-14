#!/usr/bin/env python3.13
"""
Build a draft US Spanish parent-only Pinterest paid catalog feed.

This is local/read-only against the public storefront. It does not create or
change Pinterest, Shopify, Merchant, Google Ads, GA4, GTM, billing, feeds, or
campaigns. It starts from the verified US parent paid feed and rewrites the
shopping links to Spanish storefront PDPs, then reads each public Spanish PDP
for localized title/description evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-20-pinterest-us-spanish-parent-test"
)
SOURCE_PACKET_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-20-pinterest-shopify-collection-mapping"
)
DEFAULT_INPUT = SOURCE_PACKET_DIR / "feeds/pinterest_us_paid_parent_collection_intent.tsv"
DEFAULT_OUTPUT = PACKET_DIR / "feeds/pinterest_us_es_paid_parent_collection_intent.tsv"
DEFAULT_READBACK = PACKET_DIR / "pinterest_us_es_parent_feed_public_readback.csv"
DEFAULT_TRANSLATION_CACHE = REPO_ROOT / "ops/content/shopify-product-translation-live-cache.json"
LABEL_VERSION = "collection_intent_parent_es_v20260520"
EXPECTED_PARENT_COUNTS = {
    "mommy_and_me": 99,
    "family_matching": 77,
    "daddy_and_me": 34,
}
SUPPLIER_BLOCK_HOSTS = (
    "alibaba.com",
    "aliexpress.com",
    "1688.com",
    "taobao.com",
    "tmall.com",
)
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
    )
}
GOOGLE_TRANSLATE_ENDPOINT = "https://translate.googleapis.com/translate_a/single"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def to_spanish_url(url: str) -> str:
    return url.replace("https://www.dresslikemommy.com/products/", "https://www.dresslikemommy.com/es/products/", 1)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def match_key(value: str) -> str:
    value = clean_text(value).lower()
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = value.replace("&", " and ")
    value = re.sub(r"\|\s*dlm$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\s+", " ", value)
    return value


def cache_title_candidate(source: str) -> bool:
    normalized = match_key(source)
    return bool(normalized) and "<" not in source and len(normalized) <= 220


def source_title_for_translation(row: dict[str, str]) -> str:
    title = row.get("title", "")
    if "..." not in title:
        return title
    handle = row.get("link", "").rstrip("/").split("/")[-1]
    if not handle:
        return title
    return re.sub(r"\s+", " ", handle.replace("-", " ")).strip()


def google_translate_text(text: str, timeout: float) -> str:
    query = urllib.parse.urlencode(
        {
            "client": "gtx",
            "sl": "en",
            "tl": "es",
            "dt": "t",
            "q": text,
        }
    )
    request = urllib.request.Request(
        f"{GOOGLE_TRANSLATE_ENDPOINT}?{query}",
        headers=REQUEST_HEADERS,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    translated = "".join(part[0] for part in payload[0] if part and part[0])
    return clean_text(translated)


class TranslationResolver:
    def __init__(self, cache: dict[str, str], timeout: float, allow_machine_translate: bool):
        self.cache = cache
        self.timeout = timeout
        self.allow_machine_translate = allow_machine_translate
        self.cache_dirty = False
        self.machine_translation_failures: list[str] = []
        self.normalized_entries = [
            (match_key(source), source, translated)
            for source, translated in cache.items()
            if source and translated
        ]
        self.normalized_title_entries = [
            (normalized, source, translated)
            for normalized, source, translated in self.normalized_entries
            if cache_title_candidate(source)
        ]

    def resolve(self, source: str, *, field: str, row: dict[str, str]) -> tuple[str, str, str]:
        source = source or ""
        if not source:
            return "", "missing_source", ""
        if source in self.cache and self.cache[source]:
            return clean_text(self.cache[source]), "cache_exact", source

        normalized = match_key(source)
        entries = self.normalized_title_entries if field == "title" else self.normalized_entries
        for cached_normalized, cached_source, translated in entries:
            if normalized and normalized == cached_normalized:
                return clean_text(translated), "cache_normalized_exact", cached_source

        contains_matches = []
        if field == "title":
            title_prefix = match_key(source.split("...")[0]) if "..." in source else normalized
            contains_matches = [
                (abs(len(cached_normalized) - len(title_prefix)), len(cached_normalized), cached_source, translated)
                for cached_normalized, cached_source, translated in entries
                if title_prefix
                and len(title_prefix) >= 24
                and (
                    cached_normalized.startswith(title_prefix)
                    or title_prefix in cached_normalized
                )
            ]
        elif len(normalized) >= 50:
            contains_matches = [
                (abs(len(cached_normalized) - len(normalized)), len(cached_normalized), cached_source, translated)
                for cached_normalized, cached_source, translated in entries
                if normalized in cached_normalized
            ]
        if contains_matches:
            _, _, cached_source, translated = sorted(contains_matches)[0]
            return clean_text(translated), "cache_contains", cached_source

        if not self.allow_machine_translate:
            return "", "missing", ""

        translation_source = source_title_for_translation(row) if field == "title" else source
        try:
            translated = google_translate_text(translation_source, self.timeout)
        except Exception as exc:  # noqa: BLE001 - report translation gap in summary.
            self.machine_translation_failures.append(f"{field}:{row.get('item_group_id', '')}:{type(exc).__name__}: {exc}")
            return "", "machine_translation_failed", ""
        if not translated:
            self.machine_translation_failures.append(f"{field}:{row.get('item_group_id', '')}:empty")
            return "", "machine_translation_failed", ""

        self.cache[translation_source] = translated
        if translation_source != source:
            self.cache[source] = translated
        self.cache_dirty = True
        return clean_text(translated), "machine_translated", translation_source


def meta_content(body: str, pattern: str) -> str:
    match = re.search(pattern, body, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return clean_text(match.group(1))


def fetch_spanish_page(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=REQUEST_HEADERS)
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            final_url = response.geturl()
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "final_url": exc.geturl() or url,
            "http_status": exc.code,
            "error": f"HTTPError: {exc.reason}",
            "elapsed_ms": int((time.time() - started) * 1000),
        }
    except Exception as exc:  # noqa: BLE001 - report public-readback failure in summary.
        return {
            "url": url,
            "final_url": url,
            "http_status": 0,
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_ms": int((time.time() - started) * 1000),
        }

    title = meta_content(body, r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']')
    description = meta_content(body, r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']')
    if not description:
        description = meta_content(body, r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']')
    canonical = meta_content(body, r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']')
    has_lang_es = bool(re.search(r'<html[^>]+lang=["\']es["\']', body, flags=re.IGNORECASE))
    has_es_cart = "cart_add_url: '/es/cart/add'" in body or 'cart_add_url: "/es/cart/add"' in body
    has_add_to_cart_es = "Agregar al carrito" in body
    supplier_hit = any(host in body.lower() for host in SUPPLIER_BLOCK_HOSTS)
    return {
        "url": url,
        "final_url": final_url,
        "http_status": status,
        "error": "",
        "elapsed_ms": int((time.time() - started) * 1000),
        "title": title,
        "description": description,
        "canonical": canonical,
        "has_lang_es": has_lang_es,
        "has_es_cart": has_es_cart,
        "has_add_to_cart_es": has_add_to_cart_es,
        "supplier_hit": supplier_hit,
    }


def selected_public_sample(rows: list[dict[str, str]], sample_limit: int) -> list[dict[str, str]]:
    if sample_limit <= 0:
        return []
    selected: list[dict[str, str]] = []
    per_lane_seen: Counter[str] = Counter()
    per_lane_target = max(1, sample_limit // 3)
    for row in rows:
        lane = row.get("custom_label_2", "")
        if per_lane_seen[lane] >= per_lane_target:
            continue
        selected.append(row)
        per_lane_seen[lane] += 1
        if len(selected) >= sample_limit:
            return selected
    for row in rows:
        if row in selected:
            continue
        selected.append(row)
        if len(selected) >= sample_limit:
            break
    return selected


def build_feed(
    input_path: Path,
    output_path: Path,
    readback_path: Path,
    translation_cache_path: Path,
    public_sample_limit: int,
    timeout: float,
    workers: int,
    translate_missing: bool,
) -> dict[str, Any]:
    if not input_path.exists():
        raise SystemExit(f"FATAL: missing input feed: {input_path}")

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if not rows:
        raise SystemExit("FATAL: input feed is empty")

    cache_payload: dict[str, Any] = {}
    translation_cache: dict[str, str] = {}
    if translation_cache_path.exists():
        cache_payload = json.loads(translation_cache_path.read_text(encoding="utf-8"))
        translation_cache = cache_payload.get("es", {})
    else:
        raise SystemExit(f"FATAL: missing translation cache: {translation_cache_path}")

    resolver = TranslationResolver(translation_cache, timeout, translate_missing)
    title_translation_hits = 0
    description_translation_hits = 0
    translation_methods: dict[str, Counter[str]] = {
        "title": Counter(),
        "description": Counter(),
    }
    translation_missing: dict[str, list[dict[str, str]]] = {
        "title": [],
        "description": [],
    }
    for row in rows:
        translated_title, title_method, title_source = resolver.resolve(row.get("title", ""), field="title", row=row)
        translated_description, description_method, description_source = resolver.resolve(
            row.get("description", ""),
            field="description",
            row=row,
        )
        translation_methods["title"][title_method] += 1
        translation_methods["description"][description_method] += 1
        if translated_title:
            row["title"] = clean_text(translated_title)[:150]
            title_translation_hits += 1
        else:
            translation_missing["title"].append(
                {
                    "item_group_id": row.get("item_group_id", ""),
                    "link": row.get("link", ""),
                    "source": row.get("title", ""),
                    "method": title_method,
                }
            )
        if translated_description:
            row["description"] = clean_text(translated_description)[:5000]
            description_translation_hits += 1
        else:
            translation_missing["description"].append(
                {
                    "item_group_id": row.get("item_group_id", ""),
                    "link": row.get("link", ""),
                    "source": row.get("description", "")[:300],
                    "method": description_method,
                }
            )
        row["_translation_title_source"] = title_source
        row["_translation_description_source"] = description_source
        row["id"] = row["id"].replace("shopify_us_parent_", "shopify_us_es_parent_", 1)
        row["link"] = to_spanish_url(row["link"])
        row["custom_label_0"] = "us_es"
        row["custom_label_4"] = LABEL_VERSION

    if resolver.cache_dirty:
        cache_payload["es"] = translation_cache
        translation_cache_path.write_text(
            json.dumps(cache_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    readbacks: dict[str, dict[str, Any]] = {}
    sample_rows = selected_public_sample(rows, public_sample_limit)
    if sample_rows:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            futures = {executor.submit(fetch_spanish_page, row["link"], timeout): row["link"] for row in sample_rows}
            for future in as_completed(futures):
                readback = future.result()
                readbacks[readback["url"]] = readback

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])

    readback_path.parent.mkdir(parents=True, exist_ok=True)
    with readback_path.open("w", newline="", encoding="utf-8") as f:
        rb_fields = [
            "item_group_id",
            "lane",
            "title",
            "link",
            "http_status",
            "final_url",
            "canonical",
            "has_lang_es",
            "has_es_cart",
            "has_add_to_cart_es",
            "supplier_hit",
            "error",
        ]
        writer = csv.DictWriter(f, fieldnames=rb_fields, lineterminator="\n")
        writer.writeheader()
        for row in sample_rows:
            readback = readbacks.get(row["link"], {})
            writer.writerow(
                {
                    "item_group_id": row["item_group_id"],
                    "lane": row["custom_label_2"],
                    "title": row["title"],
                    "link": row["link"],
                    "http_status": readback.get("http_status", ""),
                    "final_url": readback.get("final_url", ""),
                    "canonical": readback.get("canonical", ""),
                    "has_lang_es": readback.get("has_lang_es", ""),
                    "has_es_cart": readback.get("has_es_cart", ""),
                    "has_add_to_cart_es": readback.get("has_add_to_cart_es", ""),
                    "supplier_hit": readback.get("supplier_hit", ""),
                    "error": readback.get("error", ""),
                }
            )

    counts_by_lane = Counter(row["custom_label_2"] for row in rows)
    statuses = Counter(str(readback.get("http_status", 0)) for readback in readbacks.values())
    duplicate_ids = [item_id for item_id, count in Counter(row["id"] for row in rows).items() if count > 1]
    missing_required = {
        field: sum(1 for row in rows if not (row.get(field) or "").strip())
        for field in ("id", "item_group_id", "title", "description", "link", "image_link", "price", "availability")
    }
    spanish_page_failures = [
        row["link"]
        for row in sample_rows
        if not (
            (readbacks.get(row["link"], {}).get("http_status") == 200)
            and readbacks.get(row["link"], {}).get("has_lang_es")
            and readbacks.get(row["link"], {}).get("has_es_cart")
            and readbacks.get(row["link"], {}).get("has_add_to_cart_es")
            and not readbacks.get(row["link"], {}).get("supplier_hit")
        )
    ]
    sha = sha256_file(output_path)
    summary = {
        "mode": "pinterest_us_es_paid_parent_only_feed_draft",
        "input": str(input_path.relative_to(REPO_ROOT)),
        "output": str(output_path.relative_to(REPO_ROOT)),
        "readback": str(readback_path.relative_to(REPO_ROOT)),
        "sha256": sha,
        "row_count": len(rows),
        "unique_parent_count": len({row["item_group_id"] for row in rows}),
        "counts_by_paid_lane": dict(sorted(counts_by_lane.items())),
        "expected_parent_counts": EXPECTED_PARENT_COUNTS,
        "counts_match_expected": dict(counts_by_lane) == EXPECTED_PARENT_COUNTS,
        "custom_label_0": "us_es",
        "custom_label_4": LABEL_VERSION,
        "translation_cache": str(translation_cache_path.relative_to(REPO_ROOT)),
            "title_translation_hits": title_translation_hits,
            "description_translation_hits": description_translation_hits,
            "title_translation_missing_count": len(rows) - title_translation_hits,
            "description_translation_missing_count": len(rows) - description_translation_hits,
            "translation_methods": {
                field: dict(sorted(counter.items()))
                for field, counter in sorted(translation_methods.items())
            },
            "translation_missing_sample": {
                field: values[:20]
                for field, values in sorted(translation_missing.items())
            },
            "machine_translation_enabled": translate_missing,
            "machine_translation_failure_count": len(resolver.machine_translation_failures),
            "machine_translation_failure_sample": resolver.machine_translation_failures[:20],
        "public_sample_limit": public_sample_limit,
        "public_sample_evaluated_count": len(sample_rows),
        "public_status_counts": dict(sorted(statuses.items())),
        "spanish_page_failure_count": len(spanish_page_failures),
        "spanish_page_failure_sample": spanish_page_failures[:20],
        "duplicate_id_count": len(duplicate_ids),
        "missing_required_counts": missing_required,
        "guardrail_unique_ids": not duplicate_ids,
        "guardrail_required_fields_present": all(count == 0 for count in missing_required.values()),
        "guardrail_counts_match_expected": dict(counts_by_lane) == EXPECTED_PARENT_COUNTS,
        "guardrail_spanish_copy_complete": title_translation_hits == len(rows)
        and description_translation_hits == len(rows)
        and not resolver.machine_translation_failures,
        "guardrail_spanish_public_sample_purchasable": None if not sample_rows else not spanish_page_failures,
        "not_live_upload_authority": True,
    }
    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_path.with_suffix(".sha256").write_text(f"{sha}  {output_path.name}\n", encoding="utf-8")

    failures = []
    if duplicate_ids:
        failures.append(f"{len(duplicate_ids)} duplicate ids")
    if not summary["guardrail_required_fields_present"]:
        failures.append(f"missing required fields: {missing_required}")
    if not summary["guardrail_counts_match_expected"]:
        failures.append(f"counts mismatch: {dict(counts_by_lane)}")
    if not summary["guardrail_spanish_copy_complete"]:
        failures.append(
            "Spanish copy incomplete: "
            f"title {title_translation_hits}/{len(rows)}, "
            f"description {description_translation_hits}/{len(rows)}, "
            f"machine failures {len(resolver.machine_translation_failures)}"
        )
    if spanish_page_failures:
        failures.append(f"{len(spanish_page_failures)} Spanish public page failures")
    if failures:
        raise SystemExit("FATAL: " + "; ".join(failures))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--readback", type=Path, default=DEFAULT_READBACK)
    parser.add_argument("--translation-cache", type=Path, default=DEFAULT_TRANSLATION_CACHE)
    parser.add_argument("--public-sample-limit", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--translate-missing",
        action="store_true",
        help="Machine-translate true cache gaps into the local cache; no external platform writes.",
    )
    args = parser.parse_args()

    summary = build_feed(
        args.input,
        args.output,
        args.readback,
        args.translation_cache,
        args.public_sample_limit,
        args.timeout,
        args.workers,
        args.translate_missing,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
