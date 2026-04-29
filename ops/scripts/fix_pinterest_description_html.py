#!/usr/bin/env python3
"""Trim Shopify product description HTML that exceeds Pinterest feed limits.

Default mode is dry-run. Live writes require --execute and --approved.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402
from ops.scripts.trim_long_product_body_html import trim_description_html  # noqa: E402


API_VERSION = "2026-04"
TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_PREFIX = Path("ops/reports/pinterest-description-html-fix-2026-04-29")
DEFAULT_MIN_LENGTH = 10_000
DEFAULT_TARGET_LENGTH = 8_000
PRODUCT_PAGE_SIZE = 25


DISCOVER_PUBLICATIONS_QUERY = """
query DiscoverPublications {
  publications(first: 50) {
    nodes {
      id
      name
    }
  }
}
"""

SHOP_LOCALES_QUERY = """
query ShopLocales {
  shopLocales {
    locale
    primary
    published
  }
}
"""

UPDATE_PRODUCT_BODY_MUTATION = """
mutation UpdateProductBody($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      descriptionHtml
    }
    userErrors {
      field
      message
    }
  }
}
"""

REGISTER_TRANSLATIONS_MUTATION = """
mutation RegisterTranslations($resourceId: ID!, $translations: [TranslationInput!]!) {
  translationsRegister(resourceId: $resourceId, translations: $translations) {
    translations {
      key
      locale
      outdated
      value
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class ProductSnapshot:
    id: str
    legacy_resource_id: str
    handle: str
    title: str
    status: str
    description_html: str
    online_store_published: bool
    pinterest_published: bool
    translations: dict[str, str]


@dataclass
class DescriptionPlanRow:
    product_id: str
    legacy_resource_id: str
    handle: str
    title: str
    status: str
    target: str
    locale: str
    old_length: int
    new_length: int
    removed_chars: int
    reason: str
    applied: bool = False
    error: str = ""


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str, api_version: str) -> None:
        self.endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
        self.access_token = access_token

    def graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }
        for attempt in range(7):
            req = request.Request(self.endpoint, data=payload, method="POST", headers=headers)
            try:
                with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                response_body = exc.read().decode("utf-8", errors="replace")
                if exc.code in {429, 500, 502, 503, 504} and attempt < 6:
                    time.sleep(min(25.0, (1.7**attempt)))
                    continue
                raise RuntimeError(f"Shopify GraphQL HTTP {exc.code}: {response_body}") from exc

            errors = body.get("errors") or []
            if errors:
                throttled = any((item.get("extensions") or {}).get("code") == "THROTTLED" for item in errors)
                if throttled and attempt < 6:
                    time.sleep(min(25.0, (1.7**attempt)))
                    continue
                raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(errors, ensure_ascii=False)}")
            return body.get("data") or {}

        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def shop_locales(self) -> list[str]:
        rows = self.graphql(SHOP_LOCALES_QUERY)["shopLocales"]
        return [
            clean(row.get("locale"))
            for row in rows
            if clean(row.get("locale")) and row.get("published") and not row.get("primary")
        ]

    def publication_ids(self) -> dict[str, str]:
        nodes = self.graphql(DISCOVER_PUBLICATIONS_QUERY)["publications"].get("nodes") or []
        by_name = {clean(node.get("name")): clean(node.get("id")) for node in nodes}
        missing = [name for name in ("Online Store", "Pinterest") if not by_name.get(name)]
        if missing:
            raise RuntimeError(f"Could not find Shopify publication IDs for: {', '.join(missing)}")
        return {"online_store": by_name["Online Store"], "pinterest": by_name["Pinterest"]}

    def products(self, locales: list[str], publication_ids: dict[str, str]) -> list[ProductSnapshot]:
        aliases, alias_to_locale = locale_alias_fragment(locales)
        query = f"""
        query Products($first: Int!, $after: String, $onlinePublicationId: ID!, $pinterestPublicationId: ID!) {{
          products(first: $first, after: $after, sortKey: ID) {{
            pageInfo {{
              hasNextPage
              endCursor
            }}
            nodes {{
              id
              legacyResourceId
              handle
              title
              status
              descriptionHtml
              onlineStorePublished: publishedOnPublication(publicationId: $onlinePublicationId)
              pinterestPublished: publishedOnPublication(publicationId: $pinterestPublicationId)
              {aliases}
            }}
          }}
        }}
        """
        products: list[ProductSnapshot] = []
        after: str | None = None
        while True:
            data = self.graphql(
                query,
                {
                    "first": PRODUCT_PAGE_SIZE,
                    "after": after,
                    "onlinePublicationId": publication_ids["online_store"],
                    "pinterestPublicationId": publication_ids["pinterest"],
                },
            )["products"]
            for node in data.get("nodes") or []:
                translations: dict[str, str] = {}
                for alias, locale in alias_to_locale.items():
                    for item in node.get(alias) or []:
                        if item.get("key") == "body_html" and clean(item.get("value")):
                            translations[locale] = clean(item.get("value"))
                products.append(
                    ProductSnapshot(
                        id=clean(node.get("id")),
                        legacy_resource_id=clean(node.get("legacyResourceId")),
                        handle=clean(node.get("handle")),
                        title=clean(node.get("title")),
                        status=clean(node.get("status")),
                        description_html=clean(node.get("descriptionHtml")),
                        online_store_published=bool(node.get("onlineStorePublished")),
                        pinterest_published=bool(node.get("pinterestPublished")),
                        translations=translations,
                    )
                )
            page_info = data.get("pageInfo") or {}
            if not page_info.get("hasNextPage"):
                return products
            after = clean(page_info.get("endCursor"))

    def translatable_resource(self, product_id: str, locales: list[str]) -> dict[str, Any]:
        aliases, _alias_to_locale = locale_alias_fragment(locales)
        query = f"""
        query ProductTranslatableResource($id: ID!) {{
          translatableResource(resourceId: $id) {{
            resourceId
            translatableContent {{
              key
              value
              digest
              locale
            }}
            {aliases}
          }}
        }}
        """
        node = self.graphql(query, {"id": product_id})["translatableResource"]
        if not node:
            raise RuntimeError(f"Missing translatable resource for {product_id}")
        return node

    def update_product_description(self, product_id: str, description_html: str) -> dict[str, Any]:
        data = self.graphql(
            UPDATE_PRODUCT_BODY_MUTATION,
            {"product": {"id": product_id, "descriptionHtml": description_html}},
        )["productUpdate"]
        if data.get("userErrors"):
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return data["product"]

    def register_translations(self, product_id: str, translations: list[dict[str, str]]) -> dict[str, Any]:
        data = self.graphql(
            REGISTER_TRANSLATIONS_MUTATION,
            {"resourceId": product_id, "translations": translations},
        )["translationsRegister"]
        if data.get("userErrors"):
            raise RuntimeError(json.dumps(data["userErrors"], ensure_ascii=False))
        return data


def clean(value: Any) -> str:
    return str(value or "").strip()


def locale_alias_fragment(locales: list[str]) -> tuple[str, dict[str, str]]:
    lines: list[str] = []
    alias_to_locale: dict[str, str] = {}
    for index, locale in enumerate(locales):
        alias = f"l{index}"
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


def fallback_block_trim(html: str, target_length: int) -> str:
    if len(html) <= target_length:
        return html
    boundary_tags = ("</table>", "</ul>", "</ol>", "</p>", "</div>", "</section>")
    lower_html = html.lower()
    best_index = -1
    for tag in boundary_tags:
        index = lower_html.rfind(tag, 0, target_length)
        if index >= 0:
            best_index = max(best_index, index + len(tag))
    if best_index < 0:
        best_index = target_length
    return html[:best_index].rstrip()


def trim_for_pinterest(html: str, target_length: int) -> tuple[str, str]:
    trimmed, info = trim_description_html(html, target_length)
    reasons: list[str] = []
    if info.get("removed_policy_or_tail_blocks"):
        reasons.append("removed_policy_or_tail_blocks")
    if info.get("removed_size_chart_sections"):
        reasons.append("removed_size_chart_sections")
    if len(trimmed) > target_length:
        trimmed = fallback_block_trim(trimmed, target_length)
        reasons.append("fallback_block_boundary_trim")
    return trimmed, "; ".join(reasons or ["trimmed_to_pinterest_description_html_limit"])


def in_scope(product: ProductSnapshot, include_not_published: bool) -> bool:
    if product.status != "ACTIVE":
        return False
    if include_not_published:
        return True
    return product.online_store_published and product.pinterest_published


def build_plan(
    products: list[ProductSnapshot],
    *,
    min_length: int,
    target_length: int,
    include_not_published: bool,
) -> list[DescriptionPlanRow]:
    rows: list[DescriptionPlanRow] = []
    for product in products:
        if not in_scope(product, include_not_published):
            continue
        if len(product.description_html) > min_length:
            trimmed, reason = trim_for_pinterest(product.description_html, target_length)
            rows.append(
                DescriptionPlanRow(
                    product_id=product.id,
                    legacy_resource_id=product.legacy_resource_id,
                    handle=product.handle,
                    title=product.title,
                    status=product.status,
                    target="source",
                    locale="",
                    old_length=len(product.description_html),
                    new_length=len(trimmed),
                    removed_chars=len(product.description_html) - len(trimmed),
                    reason=reason,
                )
            )
        for locale, value in sorted(product.translations.items()):
            if len(value) <= min_length:
                continue
            trimmed, reason = trim_for_pinterest(value, target_length)
            rows.append(
                DescriptionPlanRow(
                    product_id=product.id,
                    legacy_resource_id=product.legacy_resource_id,
                    handle=product.handle,
                    title=product.title,
                    status=product.status,
                    target="translation",
                    locale=locale,
                    old_length=len(value),
                    new_length=len(trimmed),
                    removed_chars=len(value) - len(trimmed),
                    reason=reason,
                )
            )
    return rows


def body_html_digest(resource: dict[str, Any]) -> str:
    for item in resource.get("translatableContent") or []:
        if item.get("key") == "body_html":
            return clean(item.get("digest"))
    raise RuntimeError("Missing body_html translatable content digest.")


def translation_values(resource: dict[str, Any], locales: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for index, locale in enumerate(locales):
        for item in resource.get(f"l{index}") or []:
            if item.get("key") == "body_html" and clean(item.get("value")):
                values[locale] = clean(item.get("value"))
    return values


def apply_plan(
    client: ShopifyClient,
    plan_rows: list[DescriptionPlanRow],
    locales: list[str],
    *,
    target_length: int,
) -> list[DescriptionPlanRow]:
    rows_by_product: dict[str, list[DescriptionPlanRow]] = {}
    for row in plan_rows:
        rows_by_product.setdefault(row.product_id, []).append(row)

    applied_rows: list[DescriptionPlanRow] = []
    for product_id, product_rows in rows_by_product.items():
        source_rows = [row for row in product_rows if row.target == "source"]
        translation_rows = [row for row in product_rows if row.target == "translation"]
        if source_rows:
            row = source_rows[0]
            try:
                resource = client.translatable_resource(product_id, locales)
                source_value = ""
                for item in resource.get("translatableContent") or []:
                    if item.get("key") == "body_html":
                        source_value = clean(item.get("value"))
                        break
                trimmed, reason = trim_for_pinterest(source_value, target_length)
                client.update_product_description(product_id, trimmed)
                row.new_length = len(trimmed)
                row.removed_chars = len(source_value) - len(trimmed)
                row.reason = reason
                row.applied = True
            except Exception as exc:  # noqa: BLE001
                row.error = str(exc)
            applied_rows.append(row)
            time.sleep(0.15)

        if translation_rows:
            try:
                resource = client.translatable_resource(product_id, locales)
                digest = body_html_digest(resource)
                current_translations = translation_values(resource, locales)
                payload: list[dict[str, str]] = []
                row_by_locale = {row.locale: row for row in translation_rows}
                for locale, row in row_by_locale.items():
                    current_value = current_translations.get(locale, "")
                    if len(current_value) <= DEFAULT_MIN_LENGTH:
                        row.applied = True
                        row.new_length = len(current_value)
                        row.removed_chars = max(0, row.old_length - len(current_value))
                        row.reason = "already_under_limit_at_apply_time"
                        continue
                    trimmed, reason = trim_for_pinterest(current_value, target_length)
                    row.new_length = len(trimmed)
                    row.removed_chars = len(current_value) - len(trimmed)
                    row.reason = reason
                    payload.append(
                        {
                            "locale": locale,
                            "key": "body_html",
                            "value": trimmed,
                            "translatableContentDigest": digest,
                        }
                    )
                if payload:
                    client.register_translations(product_id, payload)
                    for item in payload:
                        row_by_locale[item["locale"]].applied = True
                for row in translation_rows:
                    if not row.applied and not row.error:
                        row.applied = True
            except Exception as exc:  # noqa: BLE001
                for row in translation_rows:
                    row.error = str(exc)
            applied_rows.extend(translation_rows)
            time.sleep(0.15)
    return applied_rows


def write_csv(rows: list[DescriptionPlanRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()) if rows else list(DescriptionPlanRow.__annotations__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def summarize(rows: list[DescriptionPlanRow]) -> dict[str, Any]:
    by_target = Counter(row.target for row in rows)
    by_locale = Counter(row.locale for row in rows if row.locale)
    by_status = Counter(row.status for row in rows)
    over_target = [asdict(row) for row in rows if row.new_length > DEFAULT_MIN_LENGTH]
    errors = [asdict(row) for row in rows if row.error]
    return {
        "row_count": len(rows),
        "product_count": len({row.product_id for row in rows}),
        "by_target": dict(sorted(by_target.items())),
        "by_locale": dict(sorted(by_locale.items())),
        "by_status": dict(sorted(by_status.items())),
        "applied_count": sum(1 for row in rows if row.applied),
        "error_count": len(errors),
        "still_over_10000_count": len(over_target),
        "errors": errors[:20],
        "still_over_10000": over_target[:20],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trim Pinterest-overlong product description HTML.")
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument("--api-version", default=API_VERSION, help="Shopify Admin API version.")
    parser.add_argument("--output-prefix", default=str(DEFAULT_OUTPUT_PREFIX), help="Report path prefix.")
    parser.add_argument("--min-length", type=int, default=DEFAULT_MIN_LENGTH, help="Length threshold to fix.")
    parser.add_argument("--target-length", type=int, default=DEFAULT_TARGET_LENGTH, help="Target length after trimming.")
    parser.add_argument("--include-not-published", action="store_true", help="Include active products outside Online Store/Pinterest publication scope.")
    parser.add_argument("--execute", action="store_true", help="Apply Shopify product and translation updates live.")
    parser.add_argument("--approved", action="store_true", help="Required guard for live write mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.execute and not args.approved:
        raise SystemExit("Live writes require --approved after reviewing the dry-run artifacts.")

    output_prefix = Path(args.output_prefix)
    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
        args.api_version,
    )
    locales = client.shop_locales()
    publication_ids = client.publication_ids()
    products = client.products(locales, publication_ids)
    planned_rows = build_plan(
        products,
        min_length=args.min_length,
        target_length=args.target_length,
        include_not_published=args.include_not_published,
    )
    final_rows = (
        apply_plan(client, planned_rows, locales, target_length=args.target_length)
        if args.execute
        else planned_rows
    )

    csv_path = output_prefix.with_name(f"{output_prefix.name}-changes.csv")
    summary_path = output_prefix.with_name(f"{output_prefix.name}-summary.json")
    write_csv(final_rows, csv_path)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_version": args.api_version,
        "execute": bool(args.execute),
        "scope": "ACTIVE products published to Online Store and Pinterest" if not args.include_not_published else "ACTIVE products",
        "min_length": args.min_length,
        "target_length": args.target_length,
        "published_locales": locales,
        "products_read": len(products),
        "changes_csv": str(csv_path),
        "summary": summarize(final_rows),
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
