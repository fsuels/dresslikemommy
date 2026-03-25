#!/usr/bin/env python3
import argparse
import csv
import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests

from translation_utils import TranslationBackend, htmlish_text, markup_heavy_text


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPORT_DIR = ROOT / "Dress_Like_Mommy_translations_Mar-24-2026"
DEFAULT_GLOSSARY = ROOT / "ops" / "content" / "translation_glossary.json"
DEFAULT_CONTENT_DIR = ROOT / "ops" / "content"
DEFAULT_LIVE_MAP = DEFAULT_CONTENT_DIR / "shopify-live-digest-map.json"
TOKEN_PATH = Path.home() / ".config" / "dresslikemommy" / "translation-helper-token.json"
API_VERSION = "2026-01"

TARGET_LOCALES = [
    "ar", "de", "es", "fr", "hi", "id", "it", "ja", "ko",
    "nl", "pl", "pt-BR", "ru", "sv", "th", "tr", "vi", "zh-CN", "zh-TW",
]

TYPE_CONFIG = {
    "ARTICLE": {"resource_type": "ARTICLE", "prefix": "Article"},
    "BLOG": {"resource_type": "BLOG", "prefix": "Blog"},
    "COLLECTION": {"resource_type": "COLLECTION", "prefix": "Collection"},
    "COLLECTION_IMAGE": {"resource_type": "COLLECTION_IMAGE", "prefix": "CollectionImage"},
    "DELIVERY_METHOD_DEFINITION": {"resource_type": "DELIVERY_METHOD_DEFINITION", "prefix": "DeliveryMethodDefinition"},
    "FILTER": {"resource_type": "FILTER", "prefix": "OnlineStoreFilterSetting"},
    "LINK": {"resource_type": "LINK", "prefix": "Link"},
    "MENU": {"resource_type": "MENU", "prefix": "Menu"},
    "METAFIELD": {"resource_type": "METAFIELD", "prefix": "Metafield"},
    "MEDIA_IMAGE": {"resource_type": "MEDIA_IMAGE", "prefix": "MediaImage"},
    "PACKING_SLIP_TEMPLATE": {"resource_type": "PACKING_SLIP_TEMPLATE", "prefix": "PackingSlipTemplate"},
    "PAGE": {"resource_type": "PAGE", "prefix": "Page"},
    "PRODUCT": {"resource_type": "PRODUCT", "prefix": "Product"},
    "PRODUCT_OPTION": {"resource_type": "PRODUCT_OPTION", "prefix": "ProductOption"},
    "PRODUCT_OPTION_VALUE": {"resource_type": "PRODUCT_OPTION_VALUE", "prefix": "ProductOptionValue"},
    "SHOP": {"resource_type": "SHOP", "prefix": "Shop"},
    "SHOP_POLICY": {"resource_type": "SHOP_POLICY", "prefix": "ShopPolicy"},
}

SKIP_TYPES = {"COOKIE_BANNER", "FILTER_GROUP", "METAOBJECT", "ONLINE_STORE_THEME", "ARTICLE_IMAGE"}
SKIP_FIELDS = {"handle"}
TEXTUAL_FIELDS = {
    "title", "body_html", "meta_title", "meta_description", "summary_html",
    "name", "label", "product_type", "value", "alt", "body", "text",
}
URL_RE = re.compile(r"^https?://|^[\w.-]+\.[a-z]{2,}(/|$)", re.I)
SCRIPTISH_RE = re.compile(r"<\s*(script|style|iframe)\b|\{\{|\}\}|shopify-payment-button|loox|judge\.me|review", re.I)
ENGLISH_WORD_RE = re.compile(r"[A-Za-z][A-Za-z&+'-]*")
JSONISH_RE = re.compile(r'^\s*[\[{].*[\]}]\s*$', re.S)


def load_token():
    if not TOKEN_PATH.exists():
        raise SystemExit(f"Missing token file: {TOKEN_PATH}")
    payload = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    token = payload.get("access_token")
    if not token:
        raise SystemExit("Token file does not contain an access_token.")
    return token


class ShopifyClient:
    def __init__(self, store_domain, access_token):
        self.store_domain = store_domain
        self.access_token = access_token
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Shopify-Access-Token": access_token,
        })

    def graphql(self, query, variables=None):
        for attempt in range(1, 7):
            response = self.session.post(self.endpoint, json={"query": query, "variables": variables or {}}, timeout=60)
            response.raise_for_status()
            payload = response.json()
            errors = payload.get("errors") or []
            if not errors:
                return payload["data"]
            codes = {item.get("extensions", {}).get("code") for item in errors}
            if "THROTTLED" in codes and attempt < 6:
                time.sleep(min(12.0, (1.4 ** attempt) + random.uniform(0.2, 0.8)))
                continue
            raise RuntimeError(json.dumps(errors, ensure_ascii=False))

    def paged_resources(self, resource_type):
        cursor = None
        while True:
            query = """
            query FetchResources($resourceType: TranslatableResourceType!, $after: String) {
              translatableResources(first: 250, resourceType: $resourceType, after: $after) {
                pageInfo { hasNextPage endCursor }
                edges {
                  node {
                    resourceId
                    translatableContent {
                      key
                      value
                      digest
                    }
                  }
                }
              }
            }
            """
            data = self.graphql(query, {"resourceType": resource_type, "after": cursor})
            root = data["translatableResources"]
            for edge in root["edges"]:
                yield edge["node"]
            if not root["pageInfo"]["hasNextPage"]:
                break
            cursor = root["pageInfo"]["endCursor"]

    def staged_upload(self, jsonl_path):
        mutation = """
        mutation CreateStagedUpload($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters { name value }
            }
            userErrors { field message }
          }
        }
        """
        data = self.graphql(mutation, {
            "input": [{
                "resource": "BULK_MUTATION_VARIABLES",
                "filename": jsonl_path.name,
                "mimeType": "text/jsonl",
                "httpMethod": "POST",
            }]
        })["stagedUploadsCreate"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        target = data["stagedTargets"][0]
        form = {item["name"]: item["value"] for item in target["parameters"]}
        with jsonl_path.open("rb") as handle:
            response = requests.post(target["url"], data=form, files={"file": (jsonl_path.name, handle, "text/jsonl")}, timeout=300)
            response.raise_for_status()
        return target["resourceUrl"]

    def run_bulk_mutation(self, staged_upload_path):
        mutation = """
        mutation RunTranslationsBulk($mutation: String!, $stagedUploadPath: String!) {
          bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
            bulkOperation { id status }
            userErrors { field message }
          }
        }
        """
        mutation_body = """
        mutation call($resourceId: ID!, $translations: [TranslationInput!]!) {
          translationsRegister(resourceId: $resourceId, translations: $translations) {
            userErrors { field message }
          }
        }
        """
        data = self.graphql(mutation, {
            "mutation": mutation_body,
            "stagedUploadPath": staged_upload_path,
        })["bulkOperationRunMutation"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return data["bulkOperation"]["id"]

    def current_bulk_operation(self):
        query = """
        query {
          currentBulkOperation {
            id
            status
            errorCode
            objectCount
            fileSize
            url
            partialDataUrl
          }
        }
        """
        return self.graphql(query)["currentBulkOperation"]

    def poll_bulk_operation(self, operation_id):
        while True:
            current = self.current_bulk_operation()
            if current and current["id"] == operation_id and current["status"] in {"CREATED", "RUNNING", "CANCELING"}:
                print(f"bulk status={current['status']} objects={current.get('objectCount')}", flush=True)
                time.sleep(3)
                continue
            return current

    def enable_locale(self, locale):
        mutation = """
        mutation EnableLocale($locale: String!) {
          shopLocaleEnable(locale: $locale) {
            shopLocale { locale published }
            userErrors { field message }
          }
        }
        """
        data = self.graphql(mutation, {"locale": locale})["shopLocaleEnable"]
        return data


def human_facing(default_content, field):
    text = (default_content or "").strip()
    if not text or field in SKIP_FIELDS or field not in TEXTUAL_FIELDS:
        return False
    if URL_RE.search(text):
        return False
    if text.startswith("data:image/") or "base64," in text:
        return False
    if markup_heavy_text(text):
        return False
    if JSONISH_RE.match(text) and ('"lang_id"' in text or '"lang_title"' in text or '"lang_flag"' in text or len(text) > 400):
        return False
    if SCRIPTISH_RE.search(text):
        return False
    if len(re.sub(r"[^A-Za-z\u00C0-\u024F\u0400-\u04FF\u0590-\u05FF\u0600-\u06FF\u0900-\u097F\u0E00-\u0E7F\u3040-\u30FF\u4E00-\u9FFF]", "", htmlish_text(text))) < 2:
        return False
    return True


def strip_ident(ident):
    return ident.lstrip("'").strip()


def locale_slug(locales):
    cleaned = [locale.replace("-", "_") for locale in locales]
    if len(cleaned) <= 4:
        return "_".join(cleaned)
    return f"{cleaned[0]}_to_{cleaned[-1]}_{len(cleaned)}locales"


def default_artifact_path(prefix, locales, suffix):
    DEFAULT_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_CONTENT_DIR / f"{prefix}-{locale_slug(locales)}.{suffix}"


def serialize_digest_map(digest_map):
    return {
        f"{export_type}::{ident}": value
        for (export_type, ident), value in digest_map.items()
    }


def deserialize_digest_map(raw):
    return {
        tuple(key.split("::", 1)): value
        for key, value in raw.items()
    }


def load_candidates(export_dir, locales):
    candidates = []
    unique_texts = defaultdict(set)
    skipped = Counter()
    for path in sorted(Path(export_dir).glob("*.csv")):
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                locale = row["Locale"]
                if locale not in locales:
                    continue
                if row["Type"] in SKIP_TYPES:
                    skipped[f"type:{row['Type']}"] += 1
                    continue
                if (row.get("Translated content") or "").strip():
                    skipped["already_translated"] += 1
                    continue
                if not human_facing(row["Default content"], row["Field"]):
                    skipped[f"non_human:{row['Type']}:{row['Field']}"] += 1
                    continue
                if row["Type"] not in TYPE_CONFIG:
                    skipped[f"unmapped:{row['Type']}"] += 1
                    continue
                candidate = {
                    "type": row["Type"],
                    "id": strip_ident(row["Identification"]),
                    "field": row["Field"],
                    "locale": locale,
                    "default": row["Default content"],
                }
                candidates.append(candidate)
                unique_texts[locale].add(row["Default content"])
    return candidates, unique_texts, skipped


def fetch_live_maps(client, needed_types):
    digest_map = {}
    counts = {}
    for export_type in sorted(needed_types):
        config = TYPE_CONFIG[export_type]
        resource_count = 0
        for node in client.paged_resources(config["resource_type"]):
            resource_count += 1
            resource_id = node["resourceId"]
            ident = resource_id.rsplit("/", 1)[-1]
            ident = ident.split("?", 1)[0]
            key_map = {
                item["key"]: {
                    "digest": item["digest"],
                    "value": item["value"],
                    "resource_id": resource_id,
                }
                for item in node["translatableContent"]
            }
            digest_map[(export_type, ident)] = {
                "resource_id": resource_id,
                "keys": key_map,
            }
        counts[export_type] = resource_count
    return digest_map, counts


def load_or_fetch_live_maps(client, needed_types, live_map_path, refresh=False):
    digest_map = {}
    counts = {}
    cached_types = set()
    if live_map_path.exists() and not refresh:
        payload = json.loads(live_map_path.read_text(encoding="utf-8"))
        digest_map = deserialize_digest_map(payload.get("digest_map", {}))
        counts = payload.get("live_resource_counts", {})
        cached_types = set(payload.get("resource_types", []))

    missing_types = sorted(set(needed_types) - cached_types)
    if missing_types:
        fetched_map, fetched_counts = fetch_live_maps(client, missing_types)
        digest_map.update(fetched_map)
        counts.update(fetched_counts)
        live_map_path.parent.mkdir(parents=True, exist_ok=True)
        live_map_path.write_text(json.dumps({
            "resource_types": sorted(set(cached_types) | set(missing_types)),
            "live_resource_counts": counts,
            "digest_map": serialize_digest_map(digest_map),
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return digest_map, counts


def build_payload(candidates, digest_map, translator):
    grouped = defaultdict(dict)
    skipped = Counter()
    texts_by_locale = defaultdict(list)

    for candidate in candidates:
        live = digest_map.get((candidate["type"], candidate["id"]))
        if not live:
            skipped[f"missing_resource:{candidate['type']}"] += 1
            continue
        key_info = live["keys"].get(candidate["field"])
        if not key_info:
            skipped[f"missing_key:{candidate['type']}:{candidate['field']}"] += 1
            continue
        grouped[(live["resource_id"], candidate["locale"], candidate["field"], candidate["default"])] = {
            "resource_id": live["resource_id"],
            "locale": candidate["locale"],
            "key": candidate["field"],
            "digest": key_info["digest"],
            "default": candidate["default"],
            "type": candidate["type"],
        }
        texts_by_locale[candidate["locale"]].append(candidate["default"])

    translations = {}
    for locale, texts in texts_by_locale.items():
        unique = list(dict.fromkeys(texts))
        print(f"translating locale={locale} unique_strings={len(unique)}", flush=True)
        translations[locale] = translator.translate_many(locale, unique, progress_label=f"locale={locale}")

    payload_by_resource = defaultdict(list)
    quality_counts = Counter()
    quality_samples = defaultdict(list)
    for _, item in grouped.items():
        translated_value = translations[item["locale"]][item["default"]]
        if translated_value is None:
            skipped[f"backend_failed:{item['type']}:{item['key']}"] += 1
            continue
        overlap_ratio = english_overlap_ratio(item["default"], translated_value)
        if overlap_ratio >= 0.5:
            quality_counts[item["locale"]] += 1
            if len(quality_samples[item["locale"]]) < 10:
                quality_samples[item["locale"]].append({
                    "type": item["type"],
                    "resource_id": item["resource_id"],
                    "key": item["key"],
                    "default": item["default"],
                    "translated": translated_value,
                    "english_overlap_ratio": round(overlap_ratio, 3),
                })
        payload_by_resource[item["resource_id"]].append({
            "locale": item["locale"],
            "key": item["key"],
            "value": translated_value,
            "translatableContentDigest": item["digest"],
        })

    return payload_by_resource, skipped, quality_counts, quality_samples


def write_jsonl(payload_by_resource, path):
    with path.open("w", encoding="utf-8") as handle:
        for resource_id, translations in payload_by_resource.items():
            deduped = []
            seen = set()
            for item in translations:
                signature = (item["locale"], item["key"])
                if signature in seen:
                    continue
                seen.add(signature)
                deduped.append(item)
            line = {"resourceId": resource_id, "translations": deduped}
            handle.write(json.dumps(line, ensure_ascii=False) + "\n")


def english_overlap_ratio(source, translated):
    src = {w.lower() for w in ENGLISH_WORD_RE.findall(htmlish_text(source)) if len(w) >= 3}
    dst = {w.lower() for w in ENGLISH_WORD_RE.findall(htmlish_text(translated)) if len(w) >= 3}
    if not src:
        return 0.0
    return len(src & dst) / len(src)


def main():
    parser = argparse.ArgumentParser(description="Translate missing Shopify content and register translations in bulk.")
    parser.add_argument("--store-domain", default="dresslikemommy-com.myshopify.com")
    parser.add_argument("--export-dir", default=str(DEFAULT_EXPORT_DIR))
    parser.add_argument("--cache", default="")
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    parser.add_argument("--report", default="")
    parser.add_argument("--jsonl-path", default="")
    parser.add_argument("--live-map-path", default=str(DEFAULT_LIVE_MAP))
    parser.add_argument("--refresh-live-map", action="store_true")
    parser.add_argument("--fetch-live-map-only", action="store_true")
    parser.add_argument("--locales", default=",".join(TARGET_LOCALES))
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--enable-locales", action="store_true")
    parser.add_argument("--limit-resources", type=int, default=0)
    args = parser.parse_args()

    locales = [item.strip() for item in args.locales.split(",") if item.strip()]
    cache_path = Path(args.cache) if args.cache else default_artifact_path("shopify-translation-cache", locales, "json")
    report_path = Path(args.report) if args.report else default_artifact_path("shopify-translation-sync-report", locales, "json")
    jsonl_path = Path(args.jsonl_path) if args.jsonl_path else default_artifact_path("shopify-translation-bulk", locales, "jsonl")
    live_map_path = Path(args.live_map_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    live_map_path.parent.mkdir(parents=True, exist_ok=True)
    translator = TranslationBackend(
        cache_path,
        args.glossary,
        batch_size=60,
        pause_seconds=0.05,
        request_timeout=15,
        batch_char_limit=12000,
    )
    token = load_token()
    client = ShopifyClient(args.store_domain, token)

    candidates, unique_texts, skipped_source = load_candidates(args.export_dir, locales)
    needed_types = {item["type"] for item in candidates}
    digest_map, live_counts = load_or_fetch_live_maps(client, needed_types, live_map_path, refresh=args.refresh_live_map)
    if args.fetch_live_map_only:
        summary = {
            "locales": locales,
            "needed_types": sorted(needed_types),
            "live_resource_counts": live_counts,
            "live_map_path": str(live_map_path),
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)
        return
    payload_by_resource, skipped_live, quality_counts, quality_samples = build_payload(candidates, digest_map, translator)

    if args.limit_resources:
        limited = {}
        for idx, item in enumerate(payload_by_resource.items()):
            if idx >= args.limit_resources:
                break
            limited[item[0]] = item[1]
        payload_by_resource = limited

    write_jsonl(payload_by_resource, jsonl_path)

    report = {
        "locales": locales,
        "candidate_rows": len(candidates),
        "candidate_unique_texts": {locale: len(texts) for locale, texts in unique_texts.items()},
        "live_resource_counts": live_counts,
        "source_skips": skipped_source,
        "live_skips": skipped_live,
        "bulk_resource_count": len(payload_by_resource),
        "bulk_translation_count": sum(len(items) for items in payload_by_resource.values()),
        "quality_overlap_threshold": 0.5,
        "quality_overlap_counts": quality_counts,
        "quality_overlap_samples": quality_samples,
        "cache_path": str(cache_path),
        "live_map_path": str(live_map_path),
        "jsonl_path": str(jsonl_path),
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)

    if not args.execute:
        return

    staged_resource_url = client.staged_upload(jsonl_path)
    staged_upload_path = staged_resource_url.split("/admin/tmp/files/", 1)[-1]
    operation_id = client.run_bulk_mutation(staged_upload_path)
    result = client.poll_bulk_operation(operation_id)
    print(json.dumps({"bulk_operation_result": result}, indent=2, ensure_ascii=False), flush=True)

    if args.enable_locales:
        for locale in locales:
            if locale in {"es", "fr"}:
                continue
            response = client.enable_locale(locale)
            print(json.dumps({"locale": locale, "enable_response": response}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
