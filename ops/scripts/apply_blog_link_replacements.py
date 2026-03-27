#!/usr/bin/env python3
"""Apply reviewed blog-link replacements from the inventory CSV to Shopify articles.

This script is dry-run by default. It only updates article HTML when:
1. The CSV row has a non-empty suggested_replacement_url.
2. The corresponding href exists in the Shopify article body HTML.

It performs direct href replacements only. Collection fallbacks that need copy
rewrites should still be reviewed in Shopify preview before final publish.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from shopify_admin_config import (
    DEFAULT_ENV_PATH,
    DEFAULT_STORE_DOMAIN,
    DEFAULT_TOKEN_PATH,
    load_access_token as load_shopify_access_token,
    resolve_store_domain,
)


DEFAULT_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-01")
DEFAULT_BLOG_HANDLE = "news"
DEFAULT_INVENTORY_CSV = Path("ops/blog_link_audit/blog_broken_link_inventory.csv")
ALLOWED_HOSTS = {
    "dresslikemommy.com",
    "www.dresslikemommy.com",
}

BLOGS_QUERY = """
query Blogs($first: Int!) {
  blogs(first: $first) {
    nodes {
      id
      handle
      title
    }
  }
}
"""

BLOG_ARTICLES_QUERY = """
query BlogArticles($id: ID!, $cursor: String) {
  blog(id: $id) {
    articles(first: 100, after: $cursor) {
      nodes {
        id
        handle
        title
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

HREF_RE = re.compile(r"(?P<prefix><a\b[^>]*\bhref\s*=\s*)(?P<quote>[\"'])(?P<url>.*?)(?P=quote)", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class ReplacementRow:
    post_url: str
    post_handle: str
    broken_url: str
    replacement_url: str


@dataclass(frozen=True)
class ArticleRecord:
    id: str
    handle: str
    title: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory-csv", type=Path, default=DEFAULT_INVENTORY_CSV, help="Inventory CSV from build_blog_broken_link_inventory.py")
    parser.add_argument("--blog-handle", default=DEFAULT_BLOG_HANDLE, help="Shopify blog handle")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help="Shopify Admin API version")
    parser.add_argument(
        "--store-domain",
        default=DEFAULT_STORE_DOMAIN,
        help=(
            "Store domain, e.g. dresslikemommy-com.myshopify.com. Falls back to "
            "SHOPIFY_STORE_DOMAIN or ~/.config/dresslikemommy/shopify-admin.env."
        ),
    )
    parser.add_argument("--access-token", default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""), help="Shopify Admin API access token")
    parser.add_argument(
        "--token-file",
        default=str(DEFAULT_TOKEN_PATH),
        help=f"JSON file containing access_token (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument("--execute", action="store_true", help="Run live Shopify article updates")
    return parser.parse_args()


def normalize_internal_path(href: str, *, source_url: str) -> str:
    raw_value = str(href or "").strip()
    if not raw_value or raw_value.startswith("#"):
        return ""
    lowered = raw_value.lower()
    if lowered.startswith(("mailto:", "tel:", "javascript:", "sms:")):
        return ""

    absolute = urllib.parse.urljoin(source_url, raw_value)
    parsed = urllib.parse.urlsplit(absolute)
    if parsed.scheme not in {"http", "https"}:
        return ""
    if parsed.netloc.lower() not in ALLOWED_HOSTS:
        return ""

    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return path


def extract_post_handle(post_url: str) -> str:
    parts = [part for part in urllib.parse.urlsplit(post_url).path.split("/") if part]
    if len(parts) < 3 or parts[0] != "blogs":
        return ""
    return parts[2]


def graphql_request(store_domain: str, access_token: str, api_version: str, query: str, variables: Dict) -> Dict:
    endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify GraphQL HTTP {error.code}: {body}") from error

    decoded = json.loads(body)
    if decoded.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {decoded['errors']}")
    return decoded["data"]


def rest_request(
    store_domain: str,
    access_token: str,
    api_version: str,
    path: str,
    *,
    method: str,
    payload: Optional[Dict] = None,
) -> Dict:
    request = urllib.request.Request(
        f"https://{store_domain}/admin/api/{api_version}{path}",
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify REST HTTP {error.code}: {body}") from error
    return json.loads(body)


def find_blog(store_domain: str, access_token: str, api_version: str, blog_handle: str) -> Dict:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=BLOGS_QUERY,
        variables={"first": 50},
    )
    for blog in data["blogs"]["nodes"]:
        if blog["handle"] == blog_handle:
            return blog
    raise RuntimeError(f"Blog handle '{blog_handle}' was not found")


def fetch_existing_articles(store_domain: str, access_token: str, api_version: str, blog_id: str) -> Dict[str, ArticleRecord]:
    articles: Dict[str, ArticleRecord] = {}
    cursor = None
    while True:
        data = graphql_request(
            store_domain=store_domain,
            access_token=access_token,
            api_version=api_version,
            query=BLOG_ARTICLES_QUERY,
            variables={"id": blog_id, "cursor": cursor},
        )
        article_connection = data["blog"]["articles"]
        for article in article_connection["nodes"]:
            articles[article["handle"]] = ArticleRecord(
                id=article["id"],
                handle=article["handle"],
                title=article["title"],
            )
        if not article_connection["pageInfo"]["hasNextPage"]:
            break
        cursor = article_connection["pageInfo"]["endCursor"]
    return articles


def parse_numeric_id(gid: str) -> str:
    return gid.rsplit("/", 1)[-1]


def load_replacement_rows(inventory_csv: Path) -> List[ReplacementRow]:
    rows: List[ReplacementRow] = []
    with inventory_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            replacement_url = (row.get("suggested_replacement_url") or "").strip()
            post_url = (row.get("found_in_post_url") or "").strip()
            broken_url = (row.get("broken_url") or "").strip()
            if not replacement_url or not post_url or not broken_url:
                continue
            post_handle = extract_post_handle(post_url)
            if not post_handle:
                continue
            rows.append(
                ReplacementRow(
                    post_url=post_url,
                    post_handle=post_handle,
                    broken_url=broken_url,
                    replacement_url=replacement_url,
                )
            )
    return rows


def replace_hrefs(body_html: str, post_url: str, replacements: Dict[str, str]) -> tuple[str, int]:
    replacement_count = 0

    def callback(match: re.Match[str]) -> str:
        nonlocal replacement_count
        raw_url = match.group("url")
        normalized = normalize_internal_path(raw_url, source_url=post_url)
        replacement = replacements.get(normalized)
        if not replacement:
            return match.group(0)
        replacement_count += 1
        return f"{match.group('prefix')}{match.group('quote')}{replacement}{match.group('quote')}"

    updated_html = HREF_RE.sub(callback, body_html)
    return updated_html, replacement_count


def main() -> int:
    args = parse_args()
    if not args.inventory_csv.exists():
        print(f"Inventory CSV not found: {args.inventory_csv}", file=sys.stderr)
        return 1

    replacement_rows = load_replacement_rows(args.inventory_csv)
    if not replacement_rows:
        print("No rows with suggested_replacement_url were found in the inventory CSV.", file=sys.stderr)
        return 1

    grouped_rows: Dict[str, List[ReplacementRow]] = {}
    for row in replacement_rows:
        grouped_rows.setdefault(row.post_handle, []).append(row)

    try:
        store_domain = resolve_store_domain(
            args.store_domain,
            env_path=DEFAULT_ENV_PATH,
            fallback_domain=DEFAULT_STORE_DOMAIN,
        )
        access_token = load_shopify_access_token(
            args.access_token,
            Path(args.token_file).expanduser(),
            env_path=DEFAULT_ENV_PATH,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    blog = find_blog(
        store_domain=store_domain,
        access_token=access_token,
        api_version=args.api_version,
        blog_handle=args.blog_handle,
    )
    articles = fetch_existing_articles(
        store_domain=store_domain,
        access_token=access_token,
        api_version=args.api_version,
        blog_id=blog["id"],
    )

    planned_updates = 0
    planned_replacements = 0

    for post_handle, rows in sorted(grouped_rows.items()):
        article = articles.get(post_handle)
        if not article:
            print(f"[SKIP] Article handle not found in Shopify: {post_handle}")
            continue

        numeric_id = parse_numeric_id(article.id)
        response = rest_request(
            store_domain,
            access_token,
            args.api_version,
            f"/articles/{numeric_id}.json?fields=id,title,handle,body_html",
            method="GET",
        )
        article_payload = response.get("article") or {}
        body_html = str(article_payload.get("body_html") or "")
        replacement_map = {row.broken_url: row.replacement_url for row in rows}
        updated_html, replacement_count = replace_hrefs(body_html, rows[0].post_url, replacement_map)

        if replacement_count == 0:
            print(f"[SKIP] No matching hrefs found in article body: {article.title}")
            continue

        planned_updates += 1
        planned_replacements += replacement_count
        print(f"[PLAN] {article.title} | replacements={replacement_count}")

        if not args.execute:
            continue

        rest_request(
            store_domain,
            access_token,
            args.api_version,
            f"/articles/{numeric_id}.json",
            method="PUT",
            payload={
                "article": {
                    "id": int(numeric_id),
                    "body_html": updated_html,
                }
            },
        )
        print(f"[UPDATED] {article.title}")

    mode = "executed" if args.execute else "planned"
    print(f"{mode.title()} article updates={planned_updates} href replacements={planned_replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
