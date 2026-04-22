#!/usr/bin/env python3
"""Poll Shopify for newly created products and translate missing product content automatically."""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import (  # noqa: E402
    DEFAULT_CONFIG_DIR,
    clean,
    load_access_token,
    resolve_store_domain,
)
from ops.scripts.sync_shopify_translations import DEFAULT_GLOSSARY, human_facing  # noqa: E402
from ops.scripts.translation_utils import TranslationBackend  # noqa: E402


API_VERSION = "2026-01"

RECENT_PRODUCTS_QUERY = """
query RecentProducts($first: Int!, $after: String, $reverse: Boolean!) {
  products(first: $first, after: $after, sortKey: CREATED_AT, reverse: $reverse) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        legacyResourceId
        handle
        title
        status
        createdAt
        updatedAt
      }
    }
  }
}
"""

SHOP_LOCALES_QUERY = """
query ShopLocales {
  shopLocales {
    locale
    name
    primary
    published
  }
}
"""

REGISTER_TRANSLATIONS_MUTATION = """
mutation RegisterTranslations($resourceId: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $resourceId, translations: $translations) {
    userErrors {
      field
      message
    }
    translations {
      locale
      key
      value
    }
  }
}
"""

DEFAULT_STATE_PATH = DEFAULT_CONFIG_DIR / "shopify-product-translation-state.json"
DEFAULT_LOG_PATH = Path.home() / "Library" / "Logs" / "dresslikemommy" / "shopify-product-translation.jsonl"
DEFAULT_CACHE_PATH = REPO_ROOT / "ops" / "content" / "shopify-product-translation-live-cache.json"
DEFAULT_NESTED_LIMIT = 100

RESOURCE_FIELD_ALLOWLIST = {
    "Product": {"title", "body_html", "product_type", "meta_title", "meta_description"},
    "ProductOption": {"name"},
    "ProductOptionValue": {"name", "value"},
}


@dataclass
class RecentProduct:
    product_gid: str
    product_id: str
    handle: str
    title: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class ExistingTranslation:
    locale: str
    key: str
    value: str
    outdated: bool


@dataclass
class ResourceSnapshot:
    resource_id: str
    resource_type: str
    translatable_content: list[dict[str, str]]
    existing_translations: dict[tuple[str, str], ExistingTranslation]
    nested_resources: list["ResourceSnapshot"] = field(default_factory=list)
    nested_truncated: bool = False


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(clean(value).replace("Z", "+00:00"))


def isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "created_at_cursor": "",
            "processed_ids_at_cursor": [],
            "initialized_at": "",
            "last_run_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_log(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def initialize_state(
    path: Path,
    *,
    initialize_now: bool,
    bootstrap_hours: int,
) -> dict[str, Any]:
    state = load_state(path)
    if clean(state.get("initialized_at")):
        return state

    if initialize_now or bootstrap_hours <= 0:
        cursor_time = utc_now()
    else:
        cursor_time = utc_now() - timedelta(hours=max(bootstrap_hours, 0))

    state["created_at_cursor"] = isoformat_utc(cursor_time)
    state["processed_ids_at_cursor"] = []
    state["initialized_at"] = isoformat_utc(utc_now())
    state["last_run_at"] = ""
    save_state(path, state)
    return state


def is_newer_than_cursor(product: RecentProduct, state: dict[str, Any]) -> bool:
    cursor = clean(state.get("created_at_cursor"))
    if not cursor:
        return True
    if product.created_at > cursor:
        return True
    if product.created_at == cursor and product.product_id not in set(state.get("processed_ids_at_cursor") or []):
        return True
    return False


def update_cursor_state(state: dict[str, Any], finalized: list[RecentProduct]) -> None:
    if not finalized:
        return

    current_cursor = clean(state.get("created_at_cursor"))
    current_ids = set(state.get("processed_ids_at_cursor") or [])
    newest_created_at = finalized[-1].created_at

    if newest_created_at > current_cursor:
        state["created_at_cursor"] = newest_created_at
        state["processed_ids_at_cursor"] = [item.product_id for item in finalized if item.created_at == newest_created_at]
        return

    if newest_created_at == current_cursor:
        for item in finalized:
            if item.created_at == current_cursor:
                current_ids.add(item.product_id)
        state["processed_ids_at_cursor"] = sorted(current_ids)


def resource_type_from_gid(resource_id: str) -> str:
    parts = clean(resource_id).split("/")
    return parts[3] if len(parts) >= 4 else ""


def locale_alias_fragment(locales: list[str]) -> tuple[str, dict[str, str]]:
    alias_to_locale: dict[str, str] = {}
    lines: list[str] = []
    for idx, locale in enumerate(locales):
        alias = f"loc_{idx}"
        alias_to_locale[alias] = locale
        lines.append(
            f"""{alias}: translations(locale: "{locale}") {{
              key
              value
              outdated
              locale
            }}"""
        )
    return "\n".join(lines), alias_to_locale


def parse_resource_node(node: dict[str, Any], alias_to_locale: dict[str, str]) -> ResourceSnapshot:
    existing: dict[tuple[str, str], ExistingTranslation] = {}
    for alias, locale in alias_to_locale.items():
        for item in node.get(alias) or []:
            key = clean(item.get("key"))
            existing[(locale, key)] = ExistingTranslation(
                locale=clean(item.get("locale")) or locale,
                key=key,
                value=item.get("value") or "",
                outdated=bool(item.get("outdated")),
            )

    nested_root = node.get("nestedTranslatableResources") or {}
    nested_resources = [
        parse_resource_node(edge.get("node") or {}, alias_to_locale)
        for edge in nested_root.get("edges") or []
        if edge.get("node")
    ]

    return ResourceSnapshot(
        resource_id=clean(node.get("resourceId")),
        resource_type=resource_type_from_gid(clean(node.get("resourceId"))),
        translatable_content=[
            {
                "key": clean(item.get("key")),
                "value": item.get("value") or "",
                "digest": clean(item.get("digest")),
                "locale": clean(item.get("locale")),
            }
            for item in node.get("translatableContent") or []
            if clean(item.get("key"))
        ],
        existing_translations=existing,
        nested_resources=nested_resources,
        nested_truncated=bool(nested_root.get("pageInfo", {}).get("hasNextPage")),
    )


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str):
        self.store_domain = store_domain
        self.endpoint = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Shopify-Access-Token": access_token,
            }
        )

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.post(
            self.endpoint,
            json={"query": query, "variables": variables or {}},
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        errors = payload.get("errors") or []
        if errors:
            raise RuntimeError(json.dumps(errors, ensure_ascii=False))
        return payload["data"]

    def shop_locales(self) -> list[dict[str, Any]]:
        return self.graphql(SHOP_LOCALES_QUERY)["shopLocales"]

    def recent_products(self, *, max_pages: int, page_size: int) -> list[RecentProduct]:
        rows: list[RecentProduct] = []
        after: str | None = None
        for _ in range(max_pages):
            data = self.graphql(
                RECENT_PRODUCTS_QUERY,
                {"first": page_size, "after": after, "reverse": True},
            )["products"]
            for edge in data.get("edges") or []:
                node = edge.get("node") or {}
                rows.append(
                    RecentProduct(
                        product_gid=clean(node.get("id")),
                        product_id=clean(node.get("legacyResourceId")),
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        status=clean(node.get("status")),
                        created_at=clean(node.get("createdAt")),
                        updated_at=clean(node.get("updatedAt")),
                    )
                )
            if not data.get("pageInfo", {}).get("hasNextPage"):
                break
            after = clean(data.get("pageInfo", {}).get("endCursor"))
        return rows

    def fetch_resource(self, resource_id: str, locales: list[str], nested_first: int) -> ResourceSnapshot:
        translations_fragment, alias_to_locale = locale_alias_fragment(locales)
        query = f"""
        query ResourceSnapshot($id: ID!, $nestedFirst: Int!) {{
          translatableResource(resourceId: $id) {{
            resourceId
            translatableContent {{
              key
              value
              digest
              locale
            }}
            {translations_fragment}
            nestedTranslatableResources(first: $nestedFirst) {{
              pageInfo {{
                hasNextPage
                endCursor
              }}
              edges {{
                node {{
                  resourceId
                  translatableContent {{
                    key
                    value
                    digest
                    locale
                  }}
                  {translations_fragment}
                }}
              }}
            }}
          }}
        }}
        """
        node = self.graphql(query, {"id": resource_id, "nestedFirst": nested_first})["translatableResource"]
        if not node:
            raise RuntimeError(f"Missing translatable resource for {resource_id}")
        return parse_resource_node(node, alias_to_locale)

    def register_translations(self, resource_id: str, translations: list[dict[str, str]]) -> dict[str, Any]:
        data = self.graphql(
            REGISTER_TRANSLATIONS_MUTATION,
            {"resourceId": resource_id, "translations": translations},
        )["translationsRegister"]
        if data["userErrors"]:
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return data


def resolve_target_locales(client: ShopifyClient, requested_locales: str) -> list[str]:
    if requested_locales:
        return [item.strip() for item in requested_locales.split(",") if item.strip()]

    locales = []
    for item in client.shop_locales():
        locale = clean(item.get("locale"))
        if not locale or item.get("primary") or not item.get("published"):
            continue
        locales.append(locale)
    return locales


def should_translate_field(resource_type: str, key: str, value: str) -> bool:
    allowed_fields = RESOURCE_FIELD_ALLOWLIST.get(resource_type)
    if not allowed_fields or key not in allowed_fields:
        return False
    return human_facing(value, key)


def collect_resource_snapshots(
    client: ShopifyClient,
    product_gid: str,
    locales: list[str],
    nested_limit: int,
) -> list[ResourceSnapshot]:
    product_snapshot = client.fetch_resource(product_gid, locales, nested_limit)
    snapshots_by_id: dict[str, ResourceSnapshot] = {product_snapshot.resource_id: product_snapshot}

    option_ids = []
    for nested in product_snapshot.nested_resources:
        if nested.resource_type == "ProductOption":
            snapshots_by_id[nested.resource_id] = nested
            option_ids.append(nested.resource_id)

    for option_id in option_ids:
        option_snapshot = client.fetch_resource(option_id, locales, nested_limit)
        snapshots_by_id[option_id] = option_snapshot
        for nested in option_snapshot.nested_resources:
            if nested.resource_type == "ProductOptionValue":
                snapshots_by_id[nested.resource_id] = nested

    return list(snapshots_by_id.values())


def build_translation_payload(
    snapshots: list[ResourceSnapshot],
    locales: list[str],
    translator: TranslationBackend,
    *,
    progress_prefix: str,
    force_refresh: bool = False,
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
    pending_rows = []
    texts_by_locale: dict[str, list[str]] = defaultdict(list)
    skipped = defaultdict(int)

    for snapshot in snapshots:
        for item in snapshot.translatable_content:
            key = item["key"]
            default_value = item["value"]
            digest = item["digest"]
            if not should_translate_field(snapshot.resource_type, key, default_value):
                skipped[f"filtered:{snapshot.resource_type}:{key}"] += 1
                continue
            for locale in locales:
                existing = snapshot.existing_translations.get((locale, key))
                if (
                    existing
                    and clean(existing.value)
                    and not existing.outdated
                    and not TranslationBackend._contains_placeholder_tokens(existing.value)  # noqa: SLF001
                    and not force_refresh
                ):
                    skipped[f"already_current:{locale}"] += 1
                    continue
                pending_rows.append(
                    {
                        "resource_id": snapshot.resource_id,
                        "resource_type": snapshot.resource_type,
                        "key": key,
                        "locale": locale,
                        "default": default_value,
                        "digest": digest,
                        "outdated": bool(existing.outdated) if existing else False,
                        "existing_value": clean(existing.value) if existing else "",
                    }
                )
                texts_by_locale[locale].append(default_value)

    translated_by_locale: dict[str, dict[str, str | None]] = {}
    for locale, texts in texts_by_locale.items():
        unique_texts = list(dict.fromkeys(texts))
        translated_by_locale[locale] = translator.translate_many(
            locale,
            unique_texts,
            progress_label=f"{progress_prefix} locale={locale}",
        )

    payload_by_resource: dict[str, list[dict[str, str]]] = defaultdict(list)
    translated_count = 0
    failed_count = 0
    for row in pending_rows:
        translated_value = translated_by_locale[row["locale"]].get(row["default"])
        if translated_value is None:
            failed_count += 1
            skipped[f"translation_failed:{row['locale']}"] += 1
            continue
        if row["existing_value"] and clean(translated_value) == row["existing_value"]:
            skipped[f"already_matches_generated:{row['locale']}"] += 1
            continue
        payload_by_resource[row["resource_id"]].append(
            {
                "locale": row["locale"],
                "key": row["key"],
                "value": translated_value,
                "translatableContentDigest": row["digest"],
            }
        )
        translated_count += 1

    summary = {
        "resource_count": len(snapshots),
        "candidate_count": len(pending_rows),
        "translated_count": translated_count,
        "failed_count": failed_count,
        "skipped": dict(sorted(skipped.items())),
        "resources": {
            snapshot.resource_id: snapshot.resource_type for snapshot in snapshots
        },
    }
    return payload_by_resource, summary


def process_product(
    client: ShopifyClient,
    translator: TranslationBackend,
    product: RecentProduct,
    locales: list[str],
    *,
    nested_limit: int,
    pause_ms: int,
    execute: bool,
    force_refresh: bool = False,
) -> dict[str, Any]:
    snapshots = collect_resource_snapshots(client, product.product_gid, locales, nested_limit)
    payload_by_resource, summary = build_translation_payload(
        snapshots,
        locales,
        translator,
        progress_prefix=f"product={product.handle}",
        force_refresh=force_refresh,
    )

    registered_counts = {}
    if execute:
        for resource_id, translations in payload_by_resource.items():
            if not translations:
                continue
            result = client.register_translations(resource_id, translations)
            registered_counts[resource_id] = len(result.get("translations") or [])
            if pause_ms > 0:
                time.sleep(pause_ms / 1000)

    summary.update(
        {
            "handle": product.handle,
            "product_id": product.product_id,
            "created_at": product.created_at,
            "locales": locales,
            "resource_payload_counts": {key: len(value) for key, value in payload_by_resource.items()},
            "registered_counts": registered_counts,
            "execute": bool(execute),
            "force_refresh": bool(force_refresh),
        }
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--state-path", default=str(DEFAULT_STATE_PATH), help="Persistent worker state path.")
    parser.add_argument("--jsonl-log", default=str(DEFAULT_LOG_PATH), help="Append-only JSONL log path.")
    parser.add_argument("--cache-path", default=str(DEFAULT_CACHE_PATH), help="Shared translation cache path.")
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY), help="Optional glossary JSON path.")
    parser.add_argument("--locales", default="", help="Comma-separated locale list. Defaults to live published non-primary shop locales.")
    parser.add_argument("--min-age-seconds", type=int, default=300, help="Only process products older than this.")
    parser.add_argument("--page-size", type=int, default=25, help="Recent products page size.")
    parser.add_argument("--max-pages", type=int, default=4, help="Maximum recent-products pages per run.")
    parser.add_argument("--max-products-per-run", type=int, default=3, help="Maximum products handled per run.")
    parser.add_argument("--max-nested-resources", type=int, default=DEFAULT_NESTED_LIMIT, help="Nested translatable resources fetched per product or option.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live translation writes.")
    parser.add_argument("--execute", action="store_true", help="Apply translations live instead of dry-run.")
    parser.add_argument("--force-refresh", action="store_true", help="Rebuild current translations and rewrite only values that differ.")
    parser.add_argument("--initialize-now", action="store_true", help="Initialize first-run cursor to now.")
    parser.add_argument("--bootstrap-hours", type=int, default=0, help="On first run only, process products this many hours back.")
    args = parser.parse_args()

    state_path = Path(args.state_path).expanduser()
    log_path = Path(args.jsonl_log).expanduser() if args.jsonl_log else None
    cache_path = Path(args.cache_path).expanduser()

    state = initialize_state(
        state_path,
        initialize_now=args.initialize_now,
        bootstrap_hours=args.bootstrap_hours,
    )

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    access_token = load_access_token(args.access_token)
    client = ShopifyClient(store_domain, access_token)
    locales = resolve_target_locales(client, args.locales)
    if not locales:
        raise SystemExit("No non-primary published locales were found to translate.")

    translator = TranslationBackend(
        cache_path,
        args.glossary,
        batch_size=60,
        pause_seconds=0.05,
        request_timeout=15,
        batch_char_limit=12000,
    )

    recent_products = client.recent_products(max_pages=max(args.max_pages, 1), page_size=max(args.page_size, 1))
    eligible_new = [product for product in recent_products if is_newer_than_cursor(product, state)]
    eligible_new.sort(key=lambda item: (item.created_at, item.product_id))

    finalized: list[RecentProduct] = []
    processed_count = 0
    blocked_by_error = False
    min_age_delta = timedelta(seconds=max(args.min_age_seconds, 0))

    for product in eligible_new:
        if processed_count >= max(args.max_products_per_run, 1):
            break

        if clean(product.status).upper() == "ARCHIVED":
            append_log(
                log_path,
                {
                    "event": "skipped",
                    "reason": "archived",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            if args.execute:
                finalized.append(product)
                processed_count += 1
            continue

        created_at_dt = parse_iso8601(product.created_at)
        if utc_now() - created_at_dt < min_age_delta:
            append_log(
                log_path,
                {
                    "event": "deferred",
                    "reason": "product_too_new",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                },
            )
            continue

        try:
            summary = process_product(
                client,
                translator,
                product,
                locales,
                nested_limit=max(args.max_nested_resources, 1),
                pause_ms=max(args.pause_ms, 0),
                execute=args.execute,
                force_refresh=args.force_refresh,
            )
            append_log(
                log_path,
                {
                    "event": "processed",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "summary": summary,
                },
            )
            processed_count += 1
            if args.execute:
                finalized.append(product)
                update_cursor_state(state, [product])
                state["last_run_at"] = isoformat_utc(utc_now())
                save_state(state_path, state)
        except Exception as exc:  # noqa: BLE001
            blocked_by_error = True
            append_log(
                log_path,
                {
                    "event": "error",
                    "product_id": product.product_id,
                    "handle": product.handle,
                    "created_at": product.created_at,
                    "message": str(exc),
                },
            )
            break

    if args.execute and finalized:
        update_cursor_state(state, finalized)
        state["last_run_at"] = isoformat_utc(utc_now())
        save_state(state_path, state)

    print(
        json.dumps(
            {
                "store_domain": store_domain,
                "locales": locales,
                "candidate_products": len(eligible_new),
                "processed_products": processed_count,
                "finalized_product_ids": [item.product_id for item in finalized],
                "blocked_by_error": blocked_by_error,
                "execute": bool(args.execute),
                "state_path": str(state_path),
                "cache_path": str(cache_path),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
