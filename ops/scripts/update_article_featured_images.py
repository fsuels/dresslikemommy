#!/usr/bin/env python3
"""Backfill Shopify blog article featured images from Shopify Files.

The script:
1. Fetches all articles and filters them to the target blog.
2. Fetches Shopify Files images and maps the required hero assets.
3. Chooses an image for each article missing a featured image using title keywords.
4. Updates each article with GraphQL and falls back to REST if needed.
5. Verifies the final article-image coverage.

By default the script only plans assignments. Use --execute for live updates.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


DEFAULT_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
DEFAULT_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-10")
DEFAULT_BLOG_HANDLE = os.environ.get("SHOPIFY_BLOG_HANDLE", "news")
DEFAULT_BLOG_TITLE = os.environ.get("SHOPIFY_BLOG_TITLE", "News")
DEFAULT_TOKEN_PATH = Path.home() / ".config" / "dresslikemommy" / "translation-helper-token.json"
PAGE_SIZE = 50
UPDATE_DELAY_SECONDS = 0.5
MAX_RETRIES = 3

IMAGE_KEY_SUBSTRINGS = {
    "SWEATERS": "family-sweaters-1152x2048-fixed",
    "EASTER_MOM": "mommy-me-easter-outfit-ideas-2026-hero",
    "FAMILY_RED": "chatgpt_image_mar_23_2026_03_06_20_am",
    "GARDEN_FAMILY": "approve-image-1080x1920",
    "PINK_DRESS": "pomelli-image_44",
    "BEACH_DAD": "pomelli-image_46",
    "SUMMER_PINK": "pomelli-image_47",
    "HEARTS_PINK": "pomelli-image_38",
    "LIFESTYLE": "fixed-size-1080x1920-from-upload",
    "FAMILY_GROUP": "chatgpt_image_mar_23_2026_02_48_47_am",
}

IMAGE_FALLBACKS = {
    "HEARTS_PINK": ("FAMILY_RED", "FAMILY_GROUP"),
    "SWEATERS": ("FAMILY_RED", "FAMILY_GROUP"),
    "EASTER_MOM": ("GARDEN_FAMILY", "FAMILY_RED"),
    "GARDEN_FAMILY": ("EASTER_MOM", "FAMILY_RED"),
    "PINK_DRESS": ("FAMILY_RED", "FAMILY_GROUP"),
    "BEACH_DAD": ("SUMMER_PINK", "FAMILY_RED"),
    "SUMMER_PINK": ("BEACH_DAD", "FAMILY_RED"),
    "LIFESTYLE": ("FAMILY_GROUP", "FAMILY_RED"),
    "FAMILY_GROUP": ("FAMILY_RED",),
    "FAMILY_RED": ("FAMILY_GROUP",),
}

ARTICLES_QUERY = """
query Articles($first: Int!, $after: String) {
  articles(first: $first, after: $after, sortKey: ID) {
    edges {
      cursor
      node {
        id
        title
        handle
        image {
          url
          altText
        }
        blog {
          id
          handle
          title
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

FILES_QUERY = """
query Files($first: Int!, $after: String) {
  files(first: $first, after: $after, query: "media_type:IMAGE") {
    edges {
      cursor
      node {
        __typename
        ... on MediaImage {
          id
          alt
          image {
            url
            altText
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

ARTICLE_UPDATE_MUTATION = """
mutation ArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article {
      id
      title
      image {
        url
        altText
      }
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""


class ShopifyAPIError(RuntimeError):
    """Raised for Shopify HTTP or GraphQL errors."""

    def __init__(self, message: str, *, errors: Optional[List[Dict]] = None):
        super().__init__(message)
        self.errors = errors or []


@dataclass(frozen=True)
class ArticleRecord:
    id: str
    title: str
    handle: str
    blog_handle: str
    blog_title: str
    image_url: str


@dataclass(frozen=True)
class ImageAsset:
    key: str
    url: str
    alt_text: str


@dataclass(frozen=True)
class Assignment:
    article: ArticleRecord
    image: ImageAsset
    matched_key: str
    resolved_key: str
    reason: str


def normalize_store_domain(raw_domain: str) -> str:
    value = str(raw_domain or "").strip()
    value = value.replace("https://", "").replace("http://", "")
    return value.rstrip("/")


def normalize_text(value: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip() + " "


def contains_phrase(normalized_text: str, phrase: str) -> bool:
    normalized_phrase = normalize_text(phrase).strip()
    if not normalized_phrase:
        return False
    return f" {normalized_phrase} " in normalized_text


def contains_any(normalized_text: str, phrases: Iterable[str]) -> bool:
    return any(contains_phrase(normalized_text, phrase) for phrase in phrases)


def parse_numeric_id(gid: str) -> str:
    return gid.rsplit("/", 1)[-1]


def load_access_token(access_token: str, token_file: Path) -> str:
    if access_token.strip():
        return access_token.strip()

    if not token_file.exists():
        raise SystemExit(
            "Missing Shopify Admin API token. Pass --access-token or place a token file at "
            f"{token_file}."
        )

    payload = json.loads(token_file.read_text(encoding="utf-8"))
    token = str(payload.get("access_token", "")).strip()
    if not token:
        raise SystemExit(f"Token file {token_file} does not contain access_token.")
    return token


def format_graphql_errors(errors: List[Dict]) -> str:
    parts: List[str] = []
    for error in errors:
        message = error.get("message") or "Unknown Shopify GraphQL error"
        code = error.get("extensions", {}).get("code")
        if code:
            parts.append(f"{code}: {message}")
        else:
            parts.append(message)
    return "; ".join(parts)


def format_user_errors(user_errors: List[Dict]) -> str:
    parts: List[str] = []
    for error in user_errors:
        field = ".".join(error.get("field") or [])
        message = error.get("message") or "Unknown user error"
        if field:
            parts.append(f"{field}: {message}")
        else:
            parts.append(message)
    return "; ".join(parts)


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str, api_version: str):
        self.store_domain = store_domain
        self.access_token = access_token
        self.api_version = api_version
        self.graphql_endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
        self.rest_base_url = f"https://{store_domain}/admin/api/{api_version}"

    def graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        request = urllib.request.Request(
            self.graphql_endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            },
            method="POST",
        )
        return self._json_request(request, expect_data=True)

    def rest_put(self, path: str, payload: Dict) -> Dict:
        request = urllib.request.Request(
            f"{self.rest_base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": self.access_token,
            },
            method="PUT",
        )
        return self._json_request(request, expect_data=False)

    def _json_request(self, request: urllib.request.Request, *, expect_data: bool) -> Dict:
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            message = f"Shopify HTTP {error.code}: {body}"
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                raise ShopifyAPIError(message) from error

            errors = payload.get("errors")
            if isinstance(errors, list):
                raise ShopifyAPIError(format_graphql_errors(errors), errors=errors) from error
            raise ShopifyAPIError(message) from error
        except urllib.error.URLError as error:
            raise ShopifyAPIError(f"Network error: {error}") from error

        decoded = json.loads(body)
        if expect_data:
            errors = decoded.get("errors") or []
            if errors:
                raise ShopifyAPIError(format_graphql_errors(errors), errors=errors)
            return decoded["data"]
        return decoded


def fetch_all_articles(client: ShopifyClient) -> List[ArticleRecord]:
    articles: List[ArticleRecord] = []
    cursor: Optional[str] = None

    while True:
        data = client.graphql(
            ARTICLES_QUERY,
            {"first": PAGE_SIZE, "after": cursor},
        )
        root = data["articles"]
        for edge in root["edges"]:
            node = edge["node"]
            blog = node["blog"] or {}
            image = node.get("image") or {}
            articles.append(
                ArticleRecord(
                    id=node["id"],
                    title=node["title"],
                    handle=node["handle"],
                    blog_handle=blog.get("handle", ""),
                    blog_title=blog.get("title", ""),
                    image_url=(image.get("url") or "").strip(),
                )
            )
        if not root["pageInfo"]["hasNextPage"]:
            break
        cursor = root["pageInfo"]["endCursor"]

    return articles


def filter_articles_for_blog(
    articles: Iterable[ArticleRecord],
    blog_handle: str,
    blog_title: str,
) -> List[ArticleRecord]:
    handle = str(blog_handle or "").strip().lower()
    title = str(blog_title or "").strip().lower()
    filtered: List[ArticleRecord] = []
    for article in articles:
        if handle and article.blog_handle.lower() == handle:
            filtered.append(article)
            continue
        if title and article.blog_title.lower() == title:
            filtered.append(article)
            continue
    return filtered


def fetch_image_assets(client: ShopifyClient) -> Dict[str, ImageAsset]:
    found: Dict[str, ImageAsset] = {}
    cursor: Optional[str] = None

    while True:
        data = client.graphql(
            FILES_QUERY,
            {"first": PAGE_SIZE, "after": cursor},
        )
        root = data["files"]
        for edge in root["edges"]:
            node = edge["node"]
            if node.get("__typename") != "MediaImage":
                continue
            image = node.get("image") or {}
            url = str(image.get("url") or "").strip()
            if not url:
                continue
            haystack = " ".join(
                part
                for part in (
                    url,
                    node.get("alt", ""),
                    image.get("altText", ""),
                )
                if part
            ).lower()
            for key, substring in IMAGE_KEY_SUBSTRINGS.items():
                if key in found:
                    continue
                if substring in haystack:
                    found[key] = ImageAsset(
                        key=key,
                        url=url,
                        alt_text=str(image.get("altText") or node.get("alt") or "").strip(),
                    )
        if len(found) == len(IMAGE_KEY_SUBSTRINGS):
            break
        if not root["pageInfo"]["hasNextPage"]:
            break
        cursor = root["pageInfo"]["endCursor"]

    return found


def determine_image_key(title: str) -> Tuple[str, str]:
    normalized = normalize_text(title)

    if contains_any(normalized, ("valentine", "heart", "love")):
        return "HEARTS_PINK", "matched valentine/heart/love"
    if contains_any(normalized, ("christmas", "holiday", "pajama")):
        return "SWEATERS", "matched christmas/holiday/pajama"
    if contains_any(normalized, ("new year", "winter", "cold", "cozy", "january", "december")):
        return "SWEATERS", "matched new year/winter/cold/cozy/january/december"
    if contains_any(normalized, ("thanksgiving", "november")):
        return "SWEATERS", "matched thanksgiving/november"
    if contains_any(normalized, ("halloween", "costume", "october")):
        return "LIFESTYLE", "matched halloween/costume/october"
    if contains_any(normalized, ("fall", "autumn", "apple", "september")):
        return "SWEATERS", "matched fall/autumn/apple/september"
    if contains_phrase(normalized, "easter"):
        return "EASTER_MOM", "matched easter"
    if contains_phrase(normalized, "mother") or (
        contains_phrase(normalized, "mom") and contains_phrase(normalized, "day")
    ):
        return "EASTER_MOM", "matched mother or mom+day"
    if contains_any(normalized, ("spring", "floral", "march", "april")):
        return "GARDEN_FAMILY", "matched spring/floral/march/april"
    if contains_any(normalized, ("father", "daddy", "dad")):
        return "GARDEN_FAMILY", "matched father/daddy/dad"
    if contains_any(normalized, ("4th of july", "fourth", "patriotic", "independence")):
        return "FAMILY_RED", "matched 4th/fourth/patriotic/independence"
    if contains_any(normalized, ("summer", "beach", "swim", "vacation", "july", "june", "august")):
        return "BEACH_DAD", "matched summer/beach/swim/vacation/july/june/august"
    if contains_any(normalized, ("school", "back to")):
        return "EASTER_MOM", "matched school/back to"
    if contains_phrase(normalized, "dress") and (
        contains_phrase(normalized, "mommy") or contains_phrase(normalized, "me")
    ):
        return "PINK_DRESS", "matched dress + mommy/me"
    if contains_any(normalized, ("photo", "portrait", "picture")):
        return "FAMILY_GROUP", "matched photo/portrait/picture"
    if contains_any(normalized, ("budget", "guide", "complete", "best", "top", "idea")):
        return "FAMILY_RED", "matched budget/guide/complete/best/top/idea"
    return "FAMILY_RED", "default fallback"


def resolve_image_asset(target_key: str, image_assets: Dict[str, ImageAsset]) -> ImageAsset:
    candidates = [target_key]
    candidates.extend(IMAGE_FALLBACKS.get(target_key, ()))
    candidates.extend(("FAMILY_RED", "FAMILY_GROUP"))

    for key in candidates:
        asset = image_assets.get(key)
        if asset:
            return asset

    if image_assets:
        return next(iter(image_assets.values()))
    raise RuntimeError("No Shopify file images were mapped; cannot assign featured images.")


def build_assignments(articles: Iterable[ArticleRecord], image_assets: Dict[str, ImageAsset]) -> List[Assignment]:
    assignments: List[Assignment] = []
    for article in articles:
        matched_key, reason = determine_image_key(article.title)
        resolved_asset = resolve_image_asset(matched_key, image_assets)
        assignments.append(
            Assignment(
                article=article,
                image=resolved_asset,
                matched_key=matched_key,
                resolved_key=resolved_asset.key,
                reason=reason,
            )
        )
    return assignments


def is_access_denied(error: ShopifyAPIError) -> bool:
    return any((item.get("extensions") or {}).get("code") == "ACCESS_DENIED" for item in error.errors)


def update_assignment(client: ShopifyClient, assignment: Assignment, allow_rest_fallback: bool) -> Tuple[bool, str]:
    alt_text = assignment.image.alt_text or assignment.article.title
    variables = {
        "id": assignment.article.id,
        "article": {
            "image": {
                "src": assignment.image.url,
                "altText": alt_text,
            }
        },
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            data = client.graphql(ARTICLE_UPDATE_MUTATION, variables)
            payload = data["articleUpdate"]
            user_errors = payload.get("userErrors") or []
            if user_errors:
                if allow_rest_fallback:
                    return update_assignment_via_rest(client, assignment)
                return False, format_user_errors(user_errors)
            image = payload.get("article", {}).get("image") or {}
            return True, str(image.get("url") or assignment.image.url)
        except ShopifyAPIError as error:
            if is_access_denied(error):
                return False, str(error)
            if attempt == MAX_RETRIES:
                break
            time.sleep(2 ** (attempt - 1))

    if allow_rest_fallback:
        return update_assignment_via_rest(client, assignment)
    return False, "GraphQL update failed after retries"


def update_assignment_via_rest(client: ShopifyClient, assignment: Assignment) -> Tuple[bool, str]:
    numeric_id = parse_numeric_id(assignment.article.id)
    payload = {
        "article": {
            "id": int(numeric_id),
            "image": {
                "src": assignment.image.url,
            },
        }
    }
    try:
        data = client.rest_put(f"/articles/{numeric_id}.json", payload)
    except ShopifyAPIError as error:
        return False, str(error)
    article = data.get("article") or {}
    image = article.get("image") or {}
    return True, str(image.get("src") or image.get("url") or assignment.image.url)


def print_assignment_summary(assignments: Iterable[Assignment]) -> None:
    counts = Counter(assignment.resolved_key for assignment in assignments)
    print("Assignment distribution:")
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default=DEFAULT_STORE_DOMAIN, help="Shopify store domain")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help="Shopify Admin API version")
    parser.add_argument("--blog-handle", default=DEFAULT_BLOG_HANDLE, help="Target blog handle filter")
    parser.add_argument("--blog-title", default=DEFAULT_BLOG_TITLE, help="Target blog title filter")
    parser.add_argument("--access-token", default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""), help="Shopify Admin API token")
    parser.add_argument("--token-file", default=str(DEFAULT_TOKEN_PATH), help="JSON file containing access_token")
    parser.add_argument("--execute", action="store_true", help="Run live article updates")
    parser.add_argument("--limit", type=int, default=0, help="Limit the number of article updates")
    parser.add_argument("--skip-verify", action="store_true", help="Skip the final verification query")
    parser.add_argument("--no-rest-fallback", action="store_true", help="Disable REST fallback when GraphQL update fails")
    args = parser.parse_args()

    store_domain = normalize_store_domain(args.store_domain)
    access_token = load_access_token(args.access_token, Path(args.token_file).expanduser())
    client = ShopifyClient(store_domain=store_domain, access_token=access_token, api_version=args.api_version)

    try:
        all_articles = fetch_all_articles(client)
    except ShopifyAPIError as error:
        if is_access_denied(error):
            print(
                "Access denied while reading articles. This operation requires a Shopify Admin token with "
                "`read_content` or `read_online_store_pages`.",
                file=sys.stderr,
            )
        print(str(error), file=sys.stderr)
        return 1

    target_articles = filter_articles_for_blog(
        all_articles,
        blog_handle=args.blog_handle,
        blog_title=args.blog_title,
    )
    if not target_articles:
        print(
            f"No articles matched blog handle={args.blog_handle!r} or blog title={args.blog_title!r}.",
            file=sys.stderr,
        )
        return 1

    missing_articles = [article for article in target_articles if not article.image_url]
    print(f"Found {len(all_articles)} total articles")
    print(f"Found {len(target_articles)} articles in target blog")
    print(f"Articles missing featured images: {len(missing_articles)}")

    if not missing_articles:
        print("No updates needed.")
        return 0

    if args.limit > 0:
        missing_articles = missing_articles[: args.limit]
        print(f"Limiting execution to first {len(missing_articles)} missing articles")

    try:
        image_assets = fetch_image_assets(client)
    except ShopifyAPIError as error:
        print(f"Failed to fetch Shopify file images: {error}", file=sys.stderr)
        return 1

    missing_keys = [key for key in IMAGE_KEY_SUBSTRINGS if key not in image_assets]
    if missing_keys:
        print(
            "Warning: not all requested Shopify file images were found. Missing keys: "
            + ", ".join(missing_keys),
            file=sys.stderr,
        )

    try:
        assignments = build_assignments(missing_articles, image_assets)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    print_assignment_summary(assignments)

    if not args.execute:
        print("Dry run complete. Re-run with --execute to update Shopify articles.")
        return 0

    successes = 0
    failures = 0
    allow_rest_fallback = not args.no_rest_fallback

    for assignment in assignments:
        ok, detail = update_assignment(client, assignment, allow_rest_fallback=allow_rest_fallback)
        numeric_id = parse_numeric_id(assignment.article.id)
        if ok:
            successes += 1
            print(
                f"[SUCCESS] {numeric_id} | {assignment.article.title} | "
                f"{assignment.resolved_key} | {detail}"
            )
        else:
            failures += 1
            print(
                f"[FAIL] {numeric_id} | {assignment.article.title} | "
                f"{assignment.resolved_key} | {detail}"
            )
        time.sleep(UPDATE_DELAY_SECONDS)

    print(f"Update pass complete. success={successes} fail={failures}")

    if args.skip_verify:
        return 0 if failures == 0 else 1

    try:
        verified_articles = fetch_all_articles(client)
    except ShopifyAPIError as error:
        print(f"Verification failed while reading articles: {error}", file=sys.stderr)
        return 1

    verified_target_articles = filter_articles_for_blog(
        verified_articles,
        blog_handle=args.blog_handle,
        blog_title=args.blog_title,
    )
    remaining_missing = [article for article in verified_target_articles if not article.image_url]
    print(f"Verification total articles: {len(verified_target_articles)}")
    print(f"Verification articles with image URLs: {len(verified_target_articles) - len(remaining_missing)}")
    print(f"Verification articles with null image: {len(remaining_missing)}")

    if remaining_missing:
        for article in remaining_missing:
            print(f"[MISSING] {parse_numeric_id(article.id)} | {article.title}")
        return 1

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
