#!/usr/bin/env python3
"""Repair exact `matching matching` duplicates in Shopify news article bodies.

Defaults to dry-run mode. Use `--execute` to write updated article bodies and
`--report-path` to persist the execution report.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from time import sleep
from typing import Dict, Iterable, List

from shopify_admin_config import load_access_token, resolve_store_domain


DEFAULT_API_VERSION = "2026-01"
DEFAULT_BLOG_HANDLE = "news"
DEFAULT_REPORT_PATH = Path("ops/content/news-matching-matching-fix-report.json")
SEARCH = "matching matching"
REPLACEMENT = "matching"
SEARCH_PATTERN = re.compile(r"\b(matching)\s+(matching)\b", re.IGNORECASE)

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

ARTICLES_QUERY = """
query BlogArticles($id: ID!, $cursor: String) {
  blog(id: $id) {
    articles(first: 100, after: $cursor) {
      nodes {
        id
        handle
        title
        body
        publishedAt
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

ARTICLE_UPDATE_MUTATION = """
mutation ArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article {
      id
      handle
      title
    }
    userErrors {
      field
      message
    }
  }
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Write the body repairs to Shopify.")
    parser.add_argument(
        "--store-domain",
        default="dresslikemommy-com.myshopify.com",
        help="Shopify store domain. Defaults to the dresslikemommy shop domain.",
    )
    parser.add_argument("--blog-handle", default=DEFAULT_BLOG_HANDLE, help="Blog handle to scan.")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help="Shopify Admin API version.")
    parser.add_argument(
        "--storefront-scan-scope",
        choices=("none", "candidates", "all"),
        default="candidates",
        help="Public storefront verification scope. Use 'all' for the final full-blog sweep.",
    )
    parser.add_argument(
        "--report-path",
        default=str(DEFAULT_REPORT_PATH),
        help="Optional JSON report output path.",
    )
    return parser.parse_args()


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
    raise RuntimeError(f"Blog handle '{blog_handle}' was not found.")


def fetch_articles(store_domain: str, access_token: str, api_version: str, blog_id: str) -> List[Dict]:
    articles: List[Dict] = []
    cursor = None

    while True:
        data = graphql_request(
            store_domain=store_domain,
            access_token=access_token,
            api_version=api_version,
            query=ARTICLES_QUERY,
            variables={"id": blog_id, "cursor": cursor},
        )
        connection = data["blog"]["articles"]
        articles.extend(connection["nodes"])
        if not connection["pageInfo"]["hasNextPage"]:
            return articles
        cursor = connection["pageInfo"]["endCursor"]


def update_article_body(store_domain: str, access_token: str, api_version: str, article_id: str, body: str) -> Dict:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=ARTICLE_UPDATE_MUTATION,
        variables={"id": article_id, "article": {"body": body}},
    )
    payload = data["articleUpdate"]
    if payload["userErrors"]:
        formatted = "; ".join(
            f"{'.'.join(item.get('field') or [])}: {item['message']}" for item in payload["userErrors"]
        )
        raise RuntimeError(f"Shopify articleUpdate returned userErrors: {formatted}")
    return payload["article"]


def storefront_page_has_phrase(handle: str, blog_handle: str) -> bool:
    url = f"https://www.dresslikemommy.com/blogs/{blog_handle}/{handle}"
    request = urllib.request.Request(url, headers={"User-Agent": "Codex repair_news_matching_matching/1.0"})

    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                html = response.read().decode("utf-8", errors="replace")
            return bool(SEARCH_PATTERN.search(html))
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 3:
                raise
            sleep(1.5 * (attempt + 1))
        finally:
            sleep(0.2)


def build_candidate_result(article: Dict, replacements: int) -> Dict:
    return {
        "handle": article["handle"],
        "title": article["title"],
        "article_id": article["id"].split("/")[-1],
        "replacements": replacements,
    }


def scan_storefront(handles: Iterable[str], blog_handle: str) -> List[str]:
    residual: List[str] = []
    for handle in handles:
        try:
            if storefront_page_has_phrase(handle, blog_handle):
                residual.append(handle)
        except Exception as error:  # pragma: no cover - network failure should be surfaced in report
            residual.append(f"{handle} [scan_error: {error}]")

    residual.sort()
    return residual


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def count_matches(text: str) -> int:
    return len(list(SEARCH_PATTERN.finditer(text or "")))


def collapse_matches(text: str) -> str:
    return SEARCH_PATTERN.sub(lambda match: match.group(1), text or "")


def main() -> int:
    args = parse_args()
    store_domain = resolve_store_domain(explicit_domain=args.store_domain, fallback_domain=args.store_domain)
    access_token = load_access_token()
    blog = find_blog(store_domain, access_token, args.api_version, args.blog_handle)
    articles = fetch_articles(store_domain, access_token, args.api_version, blog["id"])

    candidates = [article for article in articles if SEARCH_PATTERN.search(article.get("body") or "")]
    results: List[Dict] = []
    errors: List[Dict] = []

    for article in candidates:
        body = article.get("body") or ""
        replacements = count_matches(body)
        updated_body = collapse_matches(body)
        result = build_candidate_result(article, replacements)

        try:
            if args.execute:
                update_article_body(store_domain, access_token, args.api_version, article["id"], updated_body)
            result["remaining_body_matches"] = count_matches(updated_body)
            result["status"] = "updated" if args.execute else "candidate"
        except Exception as error:  # pragma: no cover - live API failure is reported directly
            result["status"] = "error"
            result["error"] = str(error)
            errors.append(result)
        results.append(result)

    published_handles = [article["handle"] for article in articles if article.get("publishedAt")]
    if args.storefront_scan_scope == "all":
        storefront_handles = published_handles
    elif args.storefront_scan_scope == "candidates":
        storefront_handles = [article["handle"] for article in candidates if article.get("publishedAt")]
    else:
        storefront_handles = []

    storefront_residual = scan_storefront(storefront_handles, args.blog_handle) if storefront_handles else []

    report = {
        "generated_at": now_iso(),
        "mode": "execute" if args.execute else "dry_run",
        "store_domain": store_domain,
        "blog_handle": args.blog_handle,
        "storefront_scan_scope": args.storefront_scan_scope,
        "search_phrase": SEARCH,
        "search_pattern": SEARCH_PATTERN.pattern,
        "replacement": REPLACEMENT,
        "summary": {
            "article_count": len(articles),
            "candidate_count": len(candidates),
            "updated_count": len([item for item in results if item["status"] == "updated"]),
            "error_count": len(errors),
            "storefront_scanned_count": len(storefront_handles),
            "storefront_residual_count": len(storefront_residual),
        },
        "storefront_residual_handles": storefront_residual,
        "results": results,
    }

    report_path = Path(args.report_path)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    if storefront_residual:
        print("storefront_residual_handles:")
        for handle in storefront_residual:
            print(handle)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
