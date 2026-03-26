#!/usr/bin/env python3
"""Publish Style Journal article drafts to Shopify from frontmatter HTML files.

Draft files live under ops/content/style-journal/articles by default and use a
simple frontmatter block followed by raw HTML:

---
title: Family Vacation Outfits: Matching Looks for Beach, Cruise, and Resort Trips
handle: family-vacation-outfits-beach-cruise-resort
author: Dress Like Mommy Team
summary: A practical guide to coordinated travel-day, beach, and resort outfits.
tags: family vacation, family matching outfits
image_url: https://example.com/hero.jpg
image_alt: Family in coordinated vacation outfits
publish_date: 2026-04-01T14:00:00Z
is_published: false
---
<p>Body HTML...</p>

By default the script runs in dry-run mode. Use --execute to write to Shopify.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
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
DEFAULT_ARTICLES_DIR = Path("ops/content/style-journal/articles")
DEFAULT_BLOG_HANDLE = "news"

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

ARTICLE_CREATE_MUTATION = """
mutation ArticleCreate($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article {
      id
      handle
      title
      onlineStoreUrl
    }
    userErrors {
      field
      message
    }
  }
}
"""

ARTICLE_UPDATE_MUTATION = """
mutation ArticleUpdate($article: ArticleUpdateInput!) {
  articleUpdate(article: $article) {
    article {
      id
      handle
      title
      onlineStoreUrl
    }
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass
class ArticleDraft:
    path: Path
    title: str
    handle: str
    author: str
    summary: str
    tags: List[str]
    body_html: str
    image_url: str
    image_alt: str
    publish_date: str
    is_published: bool
    seo_title: str
    seo_description: str
    featured_image_prompt: str


def parse_bool(value: str, default: bool = False) -> bool:
    normalized = str(value or "").strip().lower()
    if not normalized:
        return default
    return normalized in {"1", "true", "yes", "y", "on"}


def parse_tags(raw_tags: str) -> List[str]:
    if not raw_tags:
        return []
    return [part.strip() for part in raw_tags.split(",") if part.strip()]


def parse_frontmatter_html(path: Path) -> ArticleDraft:
    text = path.read_text(encoding="utf-8").strip()
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing frontmatter")

    lines = text.splitlines()
    metadata: Dict[str, str] = {}
    body_start = None

    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            body_start = index + 1
            break
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if separator == "":
            raise ValueError(f"{path}: invalid frontmatter line: {line}")
        metadata[key.strip()] = value.strip()

    if body_start is None:
        raise ValueError(f"{path} is missing closing frontmatter separator")

    body_html = "\n".join(lines[body_start:]).strip()
    if not body_html:
        raise ValueError(f"{path} is missing article body HTML")

    title = metadata.get("title", "").strip()
    handle = metadata.get("handle", "").strip()
    if not title or not handle:
        raise ValueError(f"{path} requires title and handle")

    author = metadata.get("author", "Dress Like Mommy Team").strip() or "Dress Like Mommy Team"
    summary = metadata.get("summary", "").strip()
    if not summary:
        raise ValueError(f"{path} requires summary")

    return ArticleDraft(
        path=path,
        title=title,
        handle=handle,
        author=author,
        summary=summary,
        tags=parse_tags(metadata.get("tags", "")),
        body_html=body_html,
        image_url=metadata.get("image_url", "").strip(),
        image_alt=metadata.get("image_alt", "").strip(),
        publish_date=metadata.get("publish_date", "").strip(),
        is_published=parse_bool(metadata.get("is_published", "false"), default=False),
        seo_title=metadata.get("seo_title", "").strip(),
        seo_description=metadata.get("seo_description", "").strip(),
        featured_image_prompt=metadata.get("featured_image_prompt", "").strip(),
    )


def load_drafts(articles_dir: Path, handles: Optional[Iterable[str]] = None) -> List[ArticleDraft]:
    handle_filter = {item.strip() for item in (handles or []) if item.strip()}
    drafts: List[ArticleDraft] = []

    for path in sorted(articles_dir.glob("*.html")):
        draft = parse_frontmatter_html(path)
        if handle_filter and draft.handle not in handle_filter:
            continue
        drafts.append(draft)

    return drafts


def normalize_store_domain(raw_domain: str) -> str:
    value = str(raw_domain or "").strip()
    value = value.replace("https://", "").replace("http://", "")
    return value.rstrip("/")


def is_future_publish_date(value: str) -> bool:
    raw_value = str(value or "").strip()
    if not raw_value:
        return False

    normalized = raw_value.replace("Z", "+00:00")
    try:
        publish_at = datetime.fromisoformat(normalized)
    except ValueError:
        return False

    if publish_at.tzinfo is None:
        publish_at = publish_at.replace(tzinfo=timezone.utc)

    return publish_at > datetime.now(timezone.utc)


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
    raise RuntimeError(f"Blog handle '{blog_handle}' was not found")


def fetch_existing_articles(store_domain: str, access_token: str, api_version: str, blog_id: str) -> Dict[str, Dict]:
    existing: Dict[str, Dict] = {}
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
            existing[article["handle"]] = article
        if not article_connection["pageInfo"]["hasNextPage"]:
            break
        cursor = article_connection["pageInfo"]["endCursor"]

    return existing


def build_article_input(draft: ArticleDraft, blog_id: Optional[str] = None, article_id: Optional[str] = None, publish_override: Optional[bool] = None) -> Dict:
    article_input: Dict = {
        "title": draft.title,
        "handle": draft.handle,
        "body": draft.body_html,
        "summary": draft.summary,
        "tags": draft.tags,
        "author": {"name": draft.author},
        "isPublished": draft.is_published if publish_override is None else publish_override,
    }

    if blog_id:
        article_input["blogId"] = blog_id
    if article_id:
        article_input["id"] = article_id
    if draft.publish_date and not (publish_override is True and is_future_publish_date(draft.publish_date)):
        article_input["publishDate"] = draft.publish_date
    if draft.image_url:
        article_input["image"] = {
            "url": draft.image_url,
            "altText": draft.image_alt or draft.title,
        }
    if draft.seo_title or draft.seo_description:
        article_input["seo"] = {
            "title": draft.seo_title or draft.title,
            "description": draft.seo_description or draft.summary,
        }

    return article_input


def format_user_errors(payload: Dict) -> str:
    messages = []
    for error in payload.get("userErrors", []):
        field = ".".join(error.get("field") or [])
        if field:
            messages.append(f"{field}: {error['message']}")
        else:
            messages.append(error["message"])
    return "; ".join(messages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles-dir", default=str(DEFAULT_ARTICLES_DIR), help="Directory containing frontmatter HTML articles")
    parser.add_argument("--blog-handle", default=DEFAULT_BLOG_HANDLE, help="Shopify blog handle to publish into")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help="Shopify Admin API version")
    parser.add_argument(
        "--store-domain",
        default=DEFAULT_STORE_DOMAIN,
        help=(
            "Store domain, e.g. dresslikemommy.myshopify.com. Falls back to "
            "SHOPIFY_STORE_DOMAIN or ~/.config/dresslikemommy/shopify-admin.env."
        ),
    )
    parser.add_argument("--access-token", default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""), help="Shopify Admin API access token")
    parser.add_argument(
        "--token-file",
        default=str(DEFAULT_TOKEN_PATH),
        help=f"JSON file containing access_token (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument("--handles", default="", help="Comma-separated article handles to limit execution")
    parser.add_argument("--execute", action="store_true", help="Run live create/update mutations")
    parser.add_argument("--update-existing", action="store_true", help="Update an existing article with the same handle instead of skipping it")
    parser.add_argument("--publish", action="store_true", help="Force articles to publish live regardless of frontmatter is_published")
    args = parser.parse_args()

    handles = [part.strip() for part in args.handles.split(",") if part.strip()]
    articles_dir = Path(args.articles_dir)
    drafts = load_drafts(articles_dir=articles_dir, handles=handles)

    if not drafts:
        print("No drafts matched the requested scope.", file=sys.stderr)
        return 1

    if not args.execute:
        print(f"Dry run: {len(drafts)} drafts found in {articles_dir}")
        for draft in drafts:
            print(f"- {draft.handle}: {draft.title}")
        print("Use --execute with Shopify credentials to publish.")
        return 0

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
    existing_articles = fetch_existing_articles(
        store_domain=store_domain,
        access_token=access_token,
        api_version=args.api_version,
        blog_id=blog["id"],
    )

    created = 0
    updated = 0
    skipped = 0

    for draft in drafts:
        existing = existing_articles.get(draft.handle)
        if existing and not args.update_existing:
            print(f"Skip existing article: {draft.handle}")
            skipped += 1
            continue

        if existing:
            mutation = ARTICLE_UPDATE_MUTATION
            article_input = build_article_input(
                draft=draft,
                article_id=existing["id"],
                publish_override=args.publish,
            )
            operation = "update"
        else:
            mutation = ARTICLE_CREATE_MUTATION
            article_input = build_article_input(
                draft=draft,
                blog_id=blog["id"],
                publish_override=args.publish,
            )
            operation = "create"

        if args.publish and draft.publish_date and is_future_publish_date(draft.publish_date):
            print(f"Publish-now override: {draft.handle} will publish immediately instead of waiting until {draft.publish_date}")

        data = graphql_request(
            store_domain=store_domain,
            access_token=access_token,
            api_version=args.api_version,
            query=mutation,
            variables={"article": article_input},
        )

        payload = data["articleUpdate"] if existing else data["articleCreate"]
        if payload.get("userErrors"):
            raise RuntimeError(f"{draft.handle} {operation} failed: {format_user_errors(payload)}")

        article = payload["article"]
        print(f"{operation.title()}d {draft.handle}: {article.get('onlineStoreUrl') or article['id']}")
        if existing:
            updated += 1
        else:
            created += 1

    print(f"Completed. created={created} updated={updated} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
