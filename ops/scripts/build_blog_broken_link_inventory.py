#!/usr/bin/env python3
"""Crawl Shopify blog articles and build a spreadsheet-ready broken-link inventory.

The script:
1. Reads all article URLs from the blog sitemap.
2. Fetches each article page and extracts internal links from the article body only.
3. Checks each unique internal link without following redirects.
4. Writes a CSV containing links that return 404, 301, 302, or 5xx.

The output CSV matches the requested Google Sheet columns:
broken_url, found_in_post_url, post_title, link_anchor_text, suggested_replacement_url, status
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List
from xml.etree import ElementTree as ET

from build_gsc_404_audit import (
    DEFAULT_BASE_URL,
    DEFAULT_PRODUCT_EXPORT,
    StatusResult,
    classify_collection_path,
    classify_dead_product,
    extract_collection_handle,
    extract_prefix,
    extract_product_handle,
    load_products,
)


DEFAULT_BLOG_SITEMAP = "https://www.dresslikemommy.com/sitemap_blogs_1.xml"
DEFAULT_OUTPUT_DIR = Path("ops/blog_link_audit")
DEFAULT_OUTPUT_CSV = DEFAULT_OUTPUT_DIR / "blog_broken_link_inventory.csv"
DEFAULT_WORKERS = 4
DEFAULT_TIMEOUT = 20
DEFAULT_RETRIES = 2
ALLOWED_HOSTS = {
    "dresslikemommy.com",
    "www.dresslikemommy.com",
}
REPORTABLE_STATUSES = {301, 302, 404, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511}
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
}


@dataclass(frozen=True)
class ArticleLink:
    broken_url: str
    found_in_post_url: str
    post_title: str
    link_anchor_text: str


class ArticleBodyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._inside_title = False
        self._title_parts: List[str] = []
        self._article_body_depth = 0
        self._current_link_href = ""
        self._current_link_text: List[str] = []
        self.links: List[tuple[str, str]] = []

    @property
    def title(self) -> str:
        return collapse_whitespace("".join(self._title_parts))

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        classes = set(attributes.get("class", "").split())

        if tag == "h1" and ("article-template__title" in classes or attributes.get("itemprop") == "headline"):
            self._inside_title = True

        is_body_root = (
            attributes.get("itemprop") == "articleBody"
            or "article-template__content" in classes
        )
        if is_body_root:
            self._article_body_depth = 1
        elif self._article_body_depth > 0:
            self._article_body_depth += 1

        if self._article_body_depth > 0 and tag == "a":
            self._current_link_href = attributes.get("href", "")
            self._current_link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self._inside_title:
            self._inside_title = False

        if tag == "a" and self._current_link_href:
            anchor_text = collapse_whitespace("".join(self._current_link_text))
            self.links.append((self._current_link_href, anchor_text))
            self._current_link_href = ""
            self._current_link_text = []

        if self._article_body_depth > 0:
            self._article_body_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self._title_parts.append(data)
        if self._current_link_href:
            self._current_link_text.append(data)


def collapse_whitespace(value: str) -> str:
    return " ".join(str(value or "").split())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blog-sitemap",
        default=DEFAULT_BLOG_SITEMAP,
        help="Blog sitemap XML URL or local XML file path",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Storefront base URL")
    parser.add_argument(
        "--product-export",
        type=Path,
        default=DEFAULT_PRODUCT_EXPORT,
        help="Historical product export used for replacement suggestions",
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV, help="Spreadsheet-ready output CSV")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Concurrent article/link workers")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Per-request timeout in seconds")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help="Retries for rate-limited/network fetches")
    parser.add_argument("--limit", type=int, default=0, help="Optional cap on article URLs for smoke tests")
    return parser.parse_args()


def fetch_text_with_retry(url: str, *, timeout: int, retries: int) -> str:
    for attempt in range(retries):
        try:
            status_code, body = curl_fetch_text(url, timeout=timeout)
            if status_code == 429 and attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            if 200 <= status_code < 300:
                return body
            if attempt >= retries - 1:
                raise RuntimeError(f"curl returned HTTP {status_code} for {url}")
        except Exception:
            if attempt >= retries - 1:
                raise
        time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch text from {url}")


def curl_fetch_text(url: str, *, timeout: int) -> tuple[int, str]:
    marker = "__CURL_STATUS__:"
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-A",
            DEFAULT_HEADERS["User-Agent"],
            "--compressed",
            "--max-time",
            str(timeout),
            "-w",
            f"\n{marker}%{{http_code}}",
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl failed for {url}")
    if marker not in result.stdout:
        raise RuntimeError(f"curl output missing status marker for {url}")
    body, _, status_text = result.stdout.rpartition(f"\n{marker}")
    return int(status_text.strip() or "0"), body


def curl_fetch_status(url: str, *, timeout: int) -> StatusResult:
    marker = "__CURL_STATUS__:"
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "-A",
            DEFAULT_HEADERS["User-Agent"],
            "--compressed",
            "--max-time",
            str(timeout),
            "-D",
            "-",
            "-o",
            "/dev/null",
            "-w",
            f"\n{marker}%{{http_code}}",
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl failed for {url}")
    if marker not in result.stdout:
        raise RuntimeError(f"curl output missing status marker for {url}")

    header_text, _, status_text = result.stdout.rpartition(f"\n{marker}")
    location = ""
    for line in header_text.splitlines():
        if line.lower().startswith("location:"):
            location = line.split(":", 1)[1].strip()
    return StatusResult(
        status=status_text.strip() or "0",
        location=location,
        checked_at=int(time.time()),
    )


def parse_sitemap_index(base_url: str, *, timeout: int, retries: int) -> Dict[str, Dict[str, str]]:
    xml_text = fetch_text_with_retry(f"{base_url}/sitemap.xml", timeout=timeout, retries=retries)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls: Dict[str, Dict[str, str]] = {}
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


def parse_sitemap_paths(sitemap_url: str, *, timeout: int, retries: int) -> set[str]:
    xml_text = fetch_text_with_retry(sitemap_url, timeout=timeout, retries=retries)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths: set[str] = set()
    for loc in root.findall("sm:url/sm:loc", ns):
        value = loc.text or ""
        path = urllib.parse.urlsplit(value).path
        if path:
            paths.add(path)
    return paths


def load_live_path_sets_with_retry(base_url: str, *, timeout: int, retries: int) -> Dict[str, set[str]]:
    sitemap_urls = parse_sitemap_index(base_url, timeout=timeout, retries=retries)
    sets: Dict[str, set[str]] = {
        "active_locales": set(),
        "product_paths": set(),
        "collection_paths": set(),
        "page_paths": set(),
    }
    for locale, url_map in sitemap_urls.items():
        if locale:
            sets["active_locales"].add(locale)
        if "products" in url_map:
            key = f"product_paths:{locale}"
            sets[key] = parse_sitemap_paths(url_map["products"], timeout=timeout, retries=retries)
            sets["product_paths"].update(sets[key])
        if "collections" in url_map:
            key = f"collection_paths:{locale}"
            sets[key] = parse_sitemap_paths(url_map["collections"], timeout=timeout, retries=retries)
            sets["collection_paths"].update(sets[key])
        if "pages" in url_map:
            key = f"page_paths:{locale}"
            sets[key] = parse_sitemap_paths(url_map["pages"], timeout=timeout, retries=retries)
            sets["page_paths"].update(sets[key])
    return sets


def load_xml_text(source: str, *, timeout: int, retries: int) -> str:
    local_path = Path(source).expanduser()
    if local_path.exists():
        return local_path.read_text(encoding="utf-8")
    return fetch_text_with_retry(source, timeout=timeout, retries=retries)


def parse_blog_sitemap_urls(sitemap_source: str, *, timeout: int, retries: int) -> List[str]:
    root = ET.fromstring(load_xml_text(sitemap_source, timeout=timeout, retries=retries))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls: List[str] = []
    for loc in root.findall("sm:url/sm:loc", ns):
        value = (loc.text or "").strip()
        if not value:
            continue
        parts = [part for part in urllib.parse.urlsplit(value).path.split("/") if part]
        if len(parts) >= 3 and parts[0] == "blogs":
            urls.append(value)
    return urls


def normalize_internal_path(href: str, *, source_url: str, base_url: str) -> str:
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


def fetch_link_status(base_url: str, path: str, timeout: int, retries: int) -> StatusResult:
    last_result: StatusResult | None = None
    for attempt in range(retries):
        try:
            last_result = curl_fetch_status(urllib.parse.urljoin(base_url, path), timeout=timeout)
            if last_result.status != "429" or attempt >= retries - 1:
                return last_result
        except Exception as error:  # pragma: no cover - network-dependent
            last_result = StatusResult(
                status=f"ERR:{type(error).__name__}",
                location=str(error),
                checked_at=int(time.time()),
            )
            if attempt >= retries - 1:
                return last_result
        time.sleep(1.5 * (attempt + 1))

    assert last_result is not None
    return last_result


def fetch_article_links(article_url: str, base_url: str, timeout: int, retries: int) -> tuple[str, List[ArticleLink]]:
    html = fetch_text_with_retry(article_url, timeout=timeout, retries=retries)
    parser = ArticleBodyParser()
    parser.feed(html)
    parser.close()

    title = parser.title or article_url.rsplit("/", 1)[-1]
    rows: List[ArticleLink] = []
    for href, anchor_text in parser.links:
        normalized_path = normalize_internal_path(href, source_url=article_url, base_url=base_url)
        if not normalized_path:
            continue
        rows.append(
            ArticleLink(
                broken_url=normalized_path,
                found_in_post_url=article_url,
                post_title=title,
                link_anchor_text=anchor_text,
            )
        )
    return article_url, rows


def status_is_reportable(status: StatusResult) -> bool:
    try:
        code = int(status.status)
    except ValueError:
        return False
    return code in REPORTABLE_STATUSES


def normalize_location(location: str, *, source_path: str, base_url: str) -> str:
    normalized = normalize_internal_path(location, source_url=urllib.parse.urljoin(base_url, source_path), base_url=base_url)
    return normalized


def format_status(status: StatusResult, *, source_path: str, base_url: str) -> str:
    location = normalize_location(status.location, source_path=source_path, base_url=base_url)
    if location:
        return f"{status.status} -> {location}"
    if status.location:
        return f"{status.status} -> {status.location}"
    return status.status


def suggest_replacement_url(
    path: str,
    status: StatusResult,
    *,
    base_url: str,
    live_sets: Dict[str, set[str]],
    products: Dict[str, object],
) -> str:
    redirect_target = normalize_location(status.location, source_path=path, base_url=base_url)
    if redirect_target and redirect_target != path:
        return redirect_target
    if not live_sets.get("product_paths") and not live_sets.get("collection_paths"):
        return ""

    split = urllib.parse.urlsplit(path)
    parts = [part for part in split.path.split("/") if part]
    prefix, unprefixed_parts = extract_prefix(parts)

    if "products" in unprefixed_parts:
        handle = extract_product_handle(unprefixed_parts)
        if not handle:
            return ""
        product = products.get(handle)
        decision = classify_dead_product(handle, product, prefix, live_sets)
        return decision.target if decision.bucket == "redirect" else ""

    if "collections" in unprefixed_parts:
        handle = extract_collection_handle(unprefixed_parts)
        if not handle:
            return ""
        decision = classify_collection_path(handle, prefix, live_sets)
        return decision.target if decision.bucket == "redirect" else ""

    return ""


def write_csv(path: Path, rows: Iterable[Dict[str, str]]) -> None:
    fieldnames = [
        "broken_url",
        "found_in_post_url",
        "post_title",
        "link_anchor_text",
        "suggested_replacement_url",
        "status",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")

    article_urls = parse_blog_sitemap_urls(args.blog_sitemap, timeout=args.timeout, retries=args.retries)
    if not article_urls:
        print(f"No article URLs were found in {args.blog_sitemap}.", file=sys.stderr)
        return 1
    if args.limit > 0:
        article_urls = article_urls[: args.limit]

    print(f"Found {len(article_urls)} article URLs in {args.blog_sitemap}")
    live_sets: Dict[str, set[str]] = {
        "active_locales": set(),
        "product_paths": set(),
        "collection_paths": set(),
        "page_paths": set(),
    }
    try:
        live_sets = load_live_path_sets_with_retry(base_url, timeout=args.timeout, retries=args.retries)
    except Exception as error:
        print(f"[WARN] Live sitemap sets unavailable; suggested_replacement_url will stay blank unless a redirect target is present. {error}")
    products = load_products(args.product_export)

    article_rows: List[ArticleLink] = []
    article_failures: List[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(fetch_article_links, article_url, base_url, args.timeout, args.retries): article_url
            for article_url in article_urls
        }
        for future in as_completed(future_map):
            article_url = future_map[future]
            try:
                _, rows = future.result()
            except Exception as error:
                article_failures.append(article_url)
                print(f"[WARN] Failed to crawl article body links: {article_url} | {error}")
                continue
            article_rows.extend(rows)
            print(f"Crawled article body links: {article_url} ({len(rows)} internal links)")

    unique_paths = sorted({row.broken_url for row in article_rows})
    status_map: Dict[str, StatusResult] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(fetch_link_status, base_url, path, args.timeout, args.retries): path
            for path in unique_paths
        }
        for future in as_completed(future_map):
            path = future_map[future]
            status = future.result()
            status_map[path] = status
            print(f"Checked link: {path} -> {format_status(status, source_path=path, base_url=base_url)}")

    report_rows: List[Dict[str, str]] = []
    for row in article_rows:
        status = status_map[row.broken_url]
        if not status_is_reportable(status):
            continue
        report_rows.append(
            {
                "broken_url": row.broken_url,
                "found_in_post_url": row.found_in_post_url,
                "post_title": row.post_title,
                "link_anchor_text": row.link_anchor_text,
                "suggested_replacement_url": suggest_replacement_url(
                    row.broken_url,
                    status,
                    base_url=base_url,
                    live_sets=live_sets,
                    products=products,
                ),
                "status": format_status(status, source_path=row.broken_url, base_url=base_url),
            }
        )

    report_rows.sort(key=lambda item: (item["found_in_post_url"], item["broken_url"], item["link_anchor_text"]))
    write_csv(args.output_csv, report_rows)

    print(f"Wrote {len(report_rows)} report rows to {args.output_csv}")
    print(f"Unique reportable links: {len({row['broken_url'] for row in report_rows})}")
    if article_failures:
        print(f"Article fetch failures: {len(article_failures)}")
        for article_url in article_failures:
            print(f"[MISS] {article_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
