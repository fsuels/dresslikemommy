#!/usr/bin/env python3
"""Keep storefront product image alt text and filenames search/AI friendly.

Subcommands (all read-only unless --execute is passed):

  audit   Classify every ACTIVE/DRAFT product image (and blog featured image)
          and write a JSON/CSV report.
  queue   Write the images whose alt text still needs an image-specific,
          human-quality description, with product context and a thumbnail
          URL, for a vision reviewer (a person or a scheduled Claude task).
  apply   Validate reviewed alt text from a JSON file and write it, refusing
          any row whose live alt changed since the queue was built.
  guard   Background safety net for new listings (launchd): give empty alt
          text a product-grounded baseline so no image is ever blank, and
          rename generic uploads (ChatGPT_Image_..., pomelli-image_...,
          supplier codes) on recently created products before feeds and
          blog posts start depending on those URLs.

Filenames of older products are never renamed here: renaming changes the
image URL used by Merchant/Pinterest feeds and by blog posts that embed it.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlsplit

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

API_VERSION = "2026-01"
ALT_MAX_LENGTH = 125
ALT_MIN_LENGTH = 15
THUMBNAIL_WIDTH = 640
FILE_UPDATE_BATCH = 20
DEFAULT_RENAME_WINDOW_HOURS = 72
DEFAULT_LOG_PATH = Path.home() / "Library" / "Logs" / "dresslikemommy" / "image-seo-guard.jsonl"
DEFAULT_EVIDENCE_DIR = REPO_ROOT / "dresslikemommy-growth-2026" / "02_AUDIT_PACKETS" / "2026-09-26-image-seo"

TEMPLATE_ALT_LEADS = (
    "product image of",
    "alternate image of",
    "additional image of",
    "detail image of",
    "close product view of",
    "extra image of",
    "image of",
    "photo of",
    "picture of",
)
GENERIC_ALTS = {
    "image",
    "photo",
    "picture",
    "product",
    "product image",
    "product photo",
    "collection image",
    "banner image",
    "hero image",
    "featured image",
    "default title",
}
# Terms that must never appear in alt text: vendor/source leaks, tool names,
# and shopper claims the store cannot substantiate (dropshipping, no stock).
BANNED_ALT_PATTERNS = (
    r"https?://",
    r"\bwww\.",
    r"dresslikemommy",
    r"\b1688\b",
    r"alibaba",
    r"aliexpress",
    r"\bo1cn",
    r"chatgpt",
    r"pomelli",
    r"\bin stock\b",
    r"\bbest ?seller",
    r"\bfree shipping\b",
    r"\bon sale\b",
    r"\d+\s?% off",
    r"\bwarehouse\b",
    r"\bcheap\b",
    r"\bclick\b",
    r"\bbuy now\b",
)
NUMBERED_ALT_RE = re.compile(r"\b(photo|image|picture|view)\s*#?\d+\s*$", re.I)
GENERIC_FILENAME_RE = re.compile(
    r"^(chatgpt[_-]image|pomelli[_-]image|o1cn|image[_-]|img[_-]|photo[_-]|untitled|screenshot|dsc[_-]?\d|pxl[_-]|\d{6,}|[a-f0-9]{20,}|[a-z0-9]{24,}\.)",
    re.I,
)

PRODUCTS_QUERY = """
query ImageSeoProducts($after: String, $query: String) {
  products(first: 50, after: $after, query: $query) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      legacyResourceId
      handle
      title
      status
      productType
      createdAt
      options { name values }
      media(first: 100) {
        nodes {
          id
          alt
          mediaContentType
          ... on MediaImage { image { url width height } }
        }
      }
    }
  }
}
"""
ARTICLES_QUERY = """
query ImageSeoArticles($after: String) {
  articles(first: 100, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle title isPublished blog { handle } image { altText url } body }
  }
}
"""
FILE_ALT_QUERY = """
query ImageSeoFileAlts($ids: [ID!]!) {
  nodes(ids: $ids) { id ... on MediaImage { alt image { url } } }
}
"""
ARTICLE_IMAGE_QUERY = """
query ImageSeoArticleImages($ids: [ID!]!) {
  nodes(ids: $ids) { id ... on Article { image { altText url } } }
}
"""
ARTICLE_UPDATE_MUTATION = """
mutation ImageSeoArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article { id image { altText url } }
    userErrors { field message code }
  }
}
"""
FILE_UPDATE_MUTATION = """
mutation ImageSeoFileUpdate($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id alt ... on MediaImage { image { url } } }
    userErrors { field message code }
  }
}
"""


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(clean(value).replace("Z", "+00:00"))


def filename_from_url(url: str) -> str:
    return clean(urlsplit(url or "").path.rsplit("/", 1)[-1])


def thumbnail_url(url: str, width: int = THUMBNAIL_WIDTH) -> str:
    if not url:
        return ""
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}width={width}&format=jpg"


def comparable(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).lower()).strip()


# ---------------------------------------------------------------- Shopify API


class ShopifyClient:
    def __init__(self, domain: str, token: str, pause_seconds: float = 0.25) -> None:
        self.endpoint = f"https://{domain}/admin/api/{API_VERSION}/graphql.json"
        self.token = token
        self.pause_seconds = pause_seconds

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        last_error: Optional[Exception] = None
        for attempt in range(4):
            request = urllib.request.Request(
                self.endpoint,
                data=body,
                headers={"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    payload = json.loads(response.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError) as error:
                last_error = error
                time.sleep(2 * (attempt + 1))
                continue
            errors = payload.get("errors")
            if errors:
                throttled = any("THROTTLED" in json.dumps(item) for item in errors)
                if throttled:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(f"Shopify GraphQL error: {errors}")
            time.sleep(self.pause_seconds)
            return payload["data"]
        raise RuntimeError(f"Shopify GraphQL request failed after retries: {last_error}")

    def paginate(self, query: str, key: str, variables: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        after = None
        while True:
            data = self.graphql(query, {**(variables or {}), "after": after})[key]
            rows.extend(data["nodes"])
            if not data["pageInfo"]["hasNextPage"]:
                return rows
            after = data["pageInfo"]["endCursor"]

    def fetch_products(self) -> List[Dict[str, Any]]:
        return self.paginate(PRODUCTS_QUERY, "products", {"query": "status:active OR status:draft"})

    def fetch_articles(self) -> List[Dict[str, Any]]:
        return self.paginate(ARTICLES_QUERY, "articles")

    def fetch_media_alts(self, media_ids: List[str]) -> Dict[str, Dict[str, str]]:
        found: Dict[str, Dict[str, str]] = {}
        for start in range(0, len(media_ids), 100):
            chunk = media_ids[start : start + 100]
            for node in self.graphql(FILE_ALT_QUERY, {"ids": chunk})["nodes"]:
                if node and node.get("id"):
                    found[node["id"]] = {
                        "alt": clean(node.get("alt")),
                        "url": clean((node.get("image") or {}).get("url")),
                    }
        return found

    def update_files(self, files: List[Dict[str, str]]) -> Dict[str, Any]:
        return self.graphql(FILE_UPDATE_MUTATION, {"files": files})["fileUpdate"]

    def fetch_article_images(self, article_ids: List[str]) -> Dict[str, Dict[str, str]]:
        found: Dict[str, Dict[str, str]] = {}
        for start in range(0, len(article_ids), 100):
            for node in self.graphql(ARTICLE_IMAGE_QUERY, {"ids": article_ids[start : start + 100]})["nodes"]:
                if node and node.get("id") and node.get("image"):
                    found[node["id"]] = {
                        "alt": clean(node["image"].get("altText")),
                        "url": clean(node["image"].get("url")),
                    }
        return found

    def update_article_image_alt(self, article_id: str, url: str, alt: str) -> Dict[str, Any]:
        # Shopify re-uploads the image on this call: the picture is unchanged but
        # its CDN URL gets a new version, and some old URLs stop resolving.
        article = {"image": {"url": url, "altText": alt}}
        return self.graphql(ARTICLE_UPDATE_MUTATION, {"id": article_id, "article": article})["articleUpdate"]


def build_client(args: argparse.Namespace) -> ShopifyClient:
    return ShopifyClient(resolve_store_domain(args.store_domain), load_access_token(args.access_token))


# ------------------------------------------------------------ classification


def product_base_name(title: str) -> str:
    base = clean(title.split("|")[0])
    return base.strip(" -–—")


def primary_color(product: Dict[str, Any]) -> str:
    for option in product.get("options") or []:
        name = clean(option.get("name")).lower()
        values = [clean(value) for value in option.get("values") or [] if clean(value)]
        if ("color" in name or "colour" in name) and len(values) == 1:
            return values[0]
    return ""


def baseline_alt(product: Dict[str, Any]) -> str:
    """Product-grounded fallback used only when an image has no usable alt.

    It is deliberately plain; the vision pass replaces it with an
    image-specific description.
    """
    base = product_base_name(product.get("title", "")) or clean(product.get("handle", "")).replace("-", " ")
    color = primary_color(product)
    if color and comparable(color) not in comparable(base):
        base = f"{base} in {color}"
    return trim_alt(base)


def trim_alt(text: str, limit: int = ALT_MAX_LENGTH) -> str:
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-–—")


def alt_issues(alt: str, *, product_title: str = "", baseline: str = "", duplicate: bool = False) -> List[str]:
    """Return why an existing alt is not good enough (empty list means keep)."""
    value = clean(alt)
    lowered = value.lower()
    if not value:
        return ["empty"]
    issues: List[str] = []
    if lowered in GENERIC_ALTS:
        issues.append("generic")
    if lowered.startswith(TEMPLATE_ALT_LEADS):
        issues.append("template_lead")
    if NUMBERED_ALT_RE.search(value):
        issues.append("numbered")
    if product_title and comparable(value) == comparable(product_title):
        issues.append("same_as_title")
    if baseline and comparable(value) == comparable(baseline):
        issues.append("baseline_only")
    if len(value) > ALT_MAX_LENGTH:
        issues.append("too_long")
    if len(value) < ALT_MIN_LENGTH and "generic" not in issues:
        issues.append("too_short")
    if any(re.search(pattern, lowered) for pattern in BANNED_ALT_PATTERNS):
        issues.append("banned_term")
    if duplicate:
        issues.append("duplicate_in_product")
    return issues


def validate_new_alt(alt: str, *, sibling_alts: Iterable[str] = ()) -> List[str]:
    """Rules a reviewed alt must pass before it is written."""
    value = clean(alt)
    lowered = value.lower()
    problems: List[str] = []
    if len(value) < ALT_MIN_LENGTH:
        problems.append("too_short")
    if len(value) > ALT_MAX_LENGTH:
        problems.append("too_long")
    if lowered.startswith(TEMPLATE_ALT_LEADS):
        problems.append("starts_with_image_of")
    if NUMBERED_ALT_RE.search(value):
        problems.append("numbered")
    for pattern in BANNED_ALT_PATTERNS:
        if re.search(pattern, lowered):
            problems.append(f"banned:{pattern}")
    words = [word for word in re.findall(r"[a-z]+", lowered) if len(word) > 3]
    repeated = [word for word, count in Counter(words).items() if count > 2]
    if repeated:
        problems.append("keyword_stuffing:" + ",".join(sorted(repeated)))
    if comparable(value) in {comparable(item) for item in sibling_alts if clean(item)}:
        problems.append("duplicate_in_product")
    return problems


def filename_is_generic(filename: str, handle: str) -> bool:
    name = clean(filename).lower()
    if not name:
        return True
    if handle and handle.lower()[:24] in name:
        return False
    return bool(GENERIC_FILENAME_RE.match(name))


def target_filename(handle: str, position: int, current_filename: str) -> str:
    extension = Path(current_filename.split("?")[0]).suffix.lower() or ".jpg"
    slug = re.sub(r"[^a-z0-9]+", "-", handle.lower()).strip("-")[:80].rstrip("-") or "product"
    return f"{slug}-{position:02d}{extension}"


def image_rows(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for product in products:
        images = [
            media
            for media in (product.get("media") or {}).get("nodes") or []
            if media.get("mediaContentType") == "IMAGE" and (media.get("image") or {}).get("url")
        ]
        alt_counts = Counter(comparable(media.get("alt")) for media in images if clean(media.get("alt")))
        base = baseline_alt(product)
        for position, media in enumerate(images, start=1):
            alt = clean(media.get("alt"))
            url = media["image"]["url"]
            filename = filename_from_url(url)
            rows.append(
                {
                    "kind": "product_media",
                    "product_id": product["id"],
                    "product_status": product.get("status"),
                    "handle": product.get("handle"),
                    "title": product.get("title"),
                    "product_type": product.get("productType"),
                    "created_at": product.get("createdAt"),
                    "media_id": media["id"],
                    "position": position,
                    "image_count": len(images),
                    "width": media["image"].get("width"),
                    "height": media["image"].get("height"),
                    "url": url,
                    "thumbnail_url": thumbnail_url(url),
                    "filename": filename,
                    "filename_generic": filename_is_generic(filename, product.get("handle", "")),
                    "current_alt": alt,
                    "baseline_alt": base,
                    "alt_issues": alt_issues(
                        alt,
                        product_title=product.get("title", ""),
                        baseline=base,
                        duplicate=bool(alt) and alt_counts[comparable(alt)] > 1,
                    ),
                }
            )
    return rows


def article_rows(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for article in articles:
        image = article.get("image") or {}
        if not article.get("isPublished") or not image.get("url"):
            continue
        alt = clean(image.get("altText"))
        rows.append(
            {
                "kind": "article_image",
                "article_id": article["id"],
                "handle": article.get("handle"),
                "blog": (article.get("blog") or {}).get("handle"),
                "title": article.get("title"),
                "url": image["url"],
                "thumbnail_url": thumbnail_url(image["url"]),
                "filename": filename_from_url(image["url"]),
                "current_alt": alt,
                "alt_issues": alt_issues(alt, product_title=article.get("title", "")),
            }
        )
    return rows


def article_body_references(articles: List[Dict[str, Any]]) -> str:
    return "\n".join(clean(article.get("body")) for article in articles)


# ------------------------------------------------------------------ commands


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    issue_counter: Counter = Counter()
    for row in rows:
        for issue in row["alt_issues"]:
            issue_counter[issue] += 1
    needs = [row for row in rows if row["alt_issues"]]
    return {
        "images": len(rows),
        "alt_ok": len(rows) - len(needs),
        "alt_needs_work": len(needs),
        "alt_issue_counts": dict(issue_counter.most_common()),
        "generic_filenames": sum(1 for row in rows if row.get("filename_generic")),
    }


def command_audit(args: argparse.Namespace) -> int:
    client = build_client(args)
    products = client.fetch_products()
    rows = image_rows(products)
    articles = article_rows(client.fetch_articles()) if args.include_articles else []
    report = {
        "generated_at": iso(utc_now()),
        "products": len(products),
        "product_media": summarize(rows),
        "article_images": summarize(articles) if articles else None,
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    (output_dir / f"image_seo_audit_{stamp}.json").write_text(
        json.dumps({**report, "rows": rows + articles}, indent=2), encoding="utf-8"
    )
    with (output_dir / f"image_seo_audit_{stamp}.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["kind", "handle", "position", "filename", "filename_generic", "current_alt", "alt_issues"]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows + articles:
            writer.writerow({**row, "alt_issues": ";".join(row["alt_issues"])})
    print(json.dumps(report, indent=2))
    return 0


def command_queue(args: argparse.Namespace) -> int:
    client = build_client(args)
    rows = [row for row in image_rows(client.fetch_products()) if row["alt_issues"]]
    if args.include_articles:
        rows += [row for row in article_rows(client.fetch_articles()) if row["alt_issues"]]
    rows.sort(key=lambda row: (row.get("product_status") != "ACTIVE", row.get("handle") or "", row.get("position") or 0))
    if args.limit:
        rows = rows[: args.limit]
    queue = {"generated_at": iso(utc_now()), "count": len(rows), "items": rows}
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(queue, indent=2), encoding="utf-8")
    print(json.dumps({"queue": str(args.output), "count": len(rows)}))
    return 0


def load_proposals(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    proposals = []
    for item in items:
        target = clean(item.get("media_id")) or clean(item.get("article_id"))
        if not target or not clean(item.get("alt")):
            continue
        proposals.append(
            {
                "kind": "article_image" if clean(item.get("article_id")) else "product_media",
                "media_id": target,
                "product_id": clean(item.get("product_id")),
                "handle": clean(item.get("handle")),
                "expected_current_alt": clean(item.get("expected_current_alt", item.get("current_alt"))),
                "alt": clean(item["alt"]),
            }
        )
    return proposals


def command_apply(args: argparse.Namespace) -> int:
    proposals = load_proposals(Path(args.alts))
    client = build_client(args)
    live = client.fetch_media_alts([item["media_id"] for item in proposals if item["kind"] == "product_media"])
    live.update(client.fetch_article_images([item["media_id"] for item in proposals if item["kind"] == "article_image"]))

    by_product: Dict[str, List[str]] = {}
    for item in proposals:
        by_product.setdefault(item["product_id"] or item["media_id"], []).append(item["alt"])

    accepted: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    for item in proposals:
        siblings = list(by_product[item["product_id"] or item["media_id"]])
        siblings.remove(item["alt"])
        problems = validate_new_alt(item["alt"], sibling_alts=siblings)
        current = live.get(item["media_id"])
        if current is None:
            problems.append("media_not_found")
        elif not args.force and current["alt"] != item["expected_current_alt"]:
            problems.append("live_alt_changed_since_queue")
        elif current["alt"] == item["alt"]:
            problems.append("already_applied")
        row = {**item, "live_alt_before": (current or {}).get("alt", "")}
        (rejected if problems else accepted).append({**row, "problems": problems} if problems else row)

    result: Dict[str, Any] = {
        "generated_at": iso(utc_now()),
        "execute": bool(args.execute),
        "proposals": len(proposals),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "rejected_rows": rejected,
    }
    if args.execute and accepted:
        applied, errors = 0, []
        media = [item for item in accepted if item["kind"] == "product_media"]
        for start in range(0, len(media), FILE_UPDATE_BATCH):
            chunk = media[start : start + FILE_UPDATE_BATCH]
            response = client.update_files([{"id": item["media_id"], "alt": item["alt"]} for item in chunk])
            errors.extend(response.get("userErrors") or [])
            applied += len(response.get("files") or [])
        for item in accepted:
            if item["kind"] != "article_image":
                continue
            response = client.update_article_image_alt(item["media_id"], live[item["media_id"]]["url"], item["alt"])
            errors.extend(response.get("userErrors") or [])
            applied += 1 if response.get("article") else 0
        readback = client.fetch_media_alts([item["media_id"] for item in media])
        readback.update(client.fetch_article_images([item["media_id"] for item in accepted if item["kind"] == "article_image"]))
        mismatches = [item["media_id"] for item in accepted if readback.get(item["media_id"], {}).get("alt") != item["alt"]]
        result.update({"applied": applied, "user_errors": errors, "readback_mismatches": mismatches})
    result["accepted_rows"] = accepted

    if args.receipt:
        Path(args.receipt).parent.mkdir(parents=True, exist_ok=True)
        Path(args.receipt).write_text(json.dumps(result, indent=2), encoding="utf-8")
    summary = {key: value for key, value in result.items() if key not in {"accepted_rows", "rejected_rows"}}
    summary["rejected_examples"] = rejected[:10]
    print(json.dumps(summary, indent=2))
    failed = bool(result.get("user_errors") or result.get("readback_mismatches"))
    return 1 if failed else 0


def plan_guard(
    products: List[Dict[str, Any]],
    article_text: str,
    *,
    now: datetime,
    rename_window_hours: int,
) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
    """Return (file updates, plan rows) for the background guard."""
    updates: List[Dict[str, str]] = []
    plan: List[Dict[str, Any]] = []
    cutoff = now - timedelta(hours=rename_window_hours)
    for row in image_rows(products):
        update: Dict[str, str] = {}
        reasons: List[str] = []
        if set(row["alt_issues"]) & {"empty", "generic"}:
            update["alt"] = row["baseline_alt"]
            reasons.append("baseline_alt")
        is_new = bool(row["created_at"]) and parse_iso(row["created_at"]) >= cutoff
        if is_new and row["filename_generic"]:
            bare = row["filename"].split("?")[0]
            if bare and bare in article_text:
                reasons.append("rename_skipped_referenced_in_article")
            else:
                update["filename"] = target_filename(row["handle"], row["position"], bare)
                reasons.append("rename_new_listing")
        if update:
            updates.append({"id": row["media_id"], **update})
        if reasons:
            plan.append(
                {
                    "handle": row["handle"],
                    "media_id": row["media_id"],
                    "position": row["position"],
                    "reasons": reasons,
                    "alt_before": row["current_alt"],
                    "alt_after": update.get("alt", row["current_alt"]),
                    "filename_before": row["filename"],
                    "filename_after": update.get("filename", row["filename"]),
                }
            )
    return updates, plan


def append_log(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def command_guard(args: argparse.Namespace) -> int:
    client = build_client(args)
    products = client.fetch_products()
    now = utc_now()
    new_products = [
        product
        for product in products
        if parse_iso(product["createdAt"]) >= now - timedelta(hours=args.rename_window_hours)
    ]
    article_text = article_body_references(client.fetch_articles()) if new_products else ""
    updates, plan = plan_guard(products, article_text, now=now, rename_window_hours=args.rename_window_hours)
    rows = image_rows(products)
    event: Dict[str, Any] = {
        "event": "image_seo_guard",
        "at": iso(now),
        "execute": bool(args.execute),
        "products": len(products),
        "images": len(rows),
        "needs_vision_alt": sum(1 for row in rows if row["alt_issues"]),
        "planned_updates": len(updates),
        "plan": plan[:200],
    }
    if args.execute and updates:
        applied, errors = 0, []
        for start in range(0, len(updates), FILE_UPDATE_BATCH):
            response = client.update_files(updates[start : start + FILE_UPDATE_BATCH])
            errors.extend(response.get("userErrors") or [])
            applied += len(response.get("files") or [])
        event.update({"applied": applied, "user_errors": errors})
    append_log(Path(args.jsonl_log), event)
    print(json.dumps({key: value for key, value in event.items() if key != "plan"}, indent=2))
    if plan and not args.execute:
        print(json.dumps(plan[:20], indent=2))
    return 1 if event.get("user_errors") else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit")
    audit.add_argument("--output-dir", default=str(DEFAULT_EVIDENCE_DIR))
    audit.add_argument("--include-articles", action="store_true")
    audit.set_defaults(func=command_audit)

    queue = sub.add_parser("queue")
    queue.add_argument("--output", required=True)
    queue.add_argument("--limit", type=int, default=0)
    queue.add_argument("--include-articles", action="store_true")
    queue.set_defaults(func=command_queue)

    apply = sub.add_parser("apply")
    apply.add_argument(
        "--alts",
        required=True,
        help="JSON list of {media_id or article_id, product_id, expected_current_alt, alt}",
    )
    apply.add_argument("--receipt", default="")
    apply.add_argument("--execute", action="store_true")
    apply.add_argument("--force", action="store_true", help="Write even if the live alt changed since the queue")
    apply.set_defaults(func=command_apply)

    guard = sub.add_parser("guard")
    guard.add_argument("--rename-window-hours", type=int, default=DEFAULT_RENAME_WINDOW_HOURS)
    guard.add_argument("--jsonl-log", default=str(DEFAULT_LOG_PATH))
    guard.add_argument("--execute", action="store_true")
    guard.set_defaults(func=command_guard)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
