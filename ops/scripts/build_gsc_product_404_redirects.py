#!/usr/bin/env python3
"""Build Shopify redirect CSVs from a GSC Coverage drilldown export.

The script reads the Search Console `Table.csv` export for `Not found (404)`,
keeps only product-like paths that should be redirected, excludes locale-
prefixed and parameterized URLs, and maps deleted product handles to the most
relevant live collection pages.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

from shopify_admin_config import (
    DEFAULT_ENV_PATH,
    DEFAULT_STORE_DOMAIN,
    DEFAULT_TOKEN_PATH,
    load_access_token,
    resolve_store_domain,
)


DEFAULT_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-01")
MOMMY_ME_REDIRECT_SAFE_TARGET = "/collections/matching-outfits"
PRODUCTS_QUERY = """
query Products($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      handle
      status
    }
  }
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table",
        type=Path,
        required=True,
        help="Path to the GSC Coverage drilldown Table.csv export.",
    )
    parser.add_argument(
        "--redirect-csv",
        type=Path,
        required=True,
        help="Output CSV for Shopify redirects (Redirect from / Redirect to).",
    )
    parser.add_argument(
        "--ignored-csv",
        type=Path,
        required=True,
        help="Output CSV logging ignored URLs and reasons.",
    )
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION)
    parser.add_argument("--store-domain", default=DEFAULT_STORE_DOMAIN)
    parser.add_argument("--access-token", default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    parser.add_argument("--token-file", default=str(DEFAULT_TOKEN_PATH))
    parser.add_argument(
        "--include-collection-product-paths",
        action="store_true",
        help="Also emit redirects for /collections/.../products/... paths in the GSC export.",
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


def fetch_product_statuses(store_domain: str, access_token: str, api_version: str) -> Dict[str, str]:
    statuses: Dict[str, str] = {}
    after: Optional[str] = None
    while True:
        data = graphql_request(
            store_domain=store_domain,
            access_token=access_token,
            api_version=api_version,
            query=PRODUCTS_QUERY,
            variables={"first": 250, "after": after},
        )["products"]
        for node in data["nodes"]:
            statuses[str(node["handle"])] = str(node["status"])
        if not data["pageInfo"]["hasNextPage"]:
            break
        after = data["pageInfo"]["endCursor"]
    return statuses


def tokenize(handle: str) -> set[str]:
    return {part for part in handle.lower().split("-") if part}


def has_phrase(handle: str, phrases: Sequence[str]) -> bool:
    return any(phrase in handle for phrase in phrases)


def has_token(tokens: set[str], token_values: Iterable[str]) -> bool:
    return any(token in tokens for token in token_values)


def is_locale_prefix(segment: str) -> bool:
    raw = (segment or "").strip().lower()
    if not raw:
        return False
    parts = raw.split("-")
    if len(parts) == 1:
        return len(parts[0]) == 2 and parts[0].isalpha()
    if len(parts) == 2:
        return all(len(part) == 2 and part.isalpha() for part in parts)
    return False


def is_mommy_me(handle: str, tokens: set[str]) -> bool:
    return has_phrase(
        handle,
        (
            "mommy-and-me",
            "mommy-me",
            "mom-and-daughter",
            "mother-daughter",
            "mother-and-daughter",
        ),
    ) or (
        has_token(tokens, ("mom", "mommy", "mother"))
        and has_token(tokens, ("daughter", "girl", "baby", "me"))
    )


def is_daddy_me(handle: str, tokens: set[str]) -> bool:
    return has_phrase(
        handle,
        (
            "daddy-and-me",
            "daddy-me",
            "father-son",
            "father-baby",
            "father-and-child",
            "big-man",
            "little-man",
            "pilot-co-pilot",
            "like-father-like-son",
            "dad-and-kid",
            "mini-me",
        ),
    ) or (
        has_token(tokens, ("dad", "daddy", "father"))
        and has_token(tokens, ("son", "baby", "child", "kid"))
    )


def is_family_matching(handle: str, tokens: set[str]) -> bool:
    return "family" in tokens or has_phrase(handle, ("family-matching", "matching-family"))


def target_for_handle(handle: str) -> str:
    normalized = handle.lower()
    tokens = tokenize(normalized)
    christmas = has_token(tokens, ("christmas", "holiday", "grinch", "reindeer", "snowman", "santa", "elf", "gnome")) or has_phrase(
        normalized, ("fair-isle", "ho-ho-ho", "merry-christmas")
    )
    mommy_me = is_mommy_me(normalized, tokens)
    daddy_me = is_daddy_me(normalized, tokens)
    family_matching = is_family_matching(normalized, tokens)

    if has_token(tokens, ("maternity",)):
        return "/collections/maternity"

    if has_token(tokens, ("swimsuit", "swimsuits", "swimwear", "swim", "bikini", "bikinis", "tankini", "tankinis", "monokini", "trunk", "trunks", "beachwear")):
        return "/collections/swimsuits"

    if has_token(tokens, ("pajama", "pajamas", "sleepwear", "loungewear", "pjs")):
        if christmas:
            return "/collections/christmas-pajamas"
        if family_matching:
            return "/collections/family-pajamas"
        return "/collections/pajamas"

    if has_token(tokens, ("hoodie", "hoodies", "sweater", "sweaters", "sweatshirt", "sweatshirts", "jacket", "jackets", "coat", "coats", "outerwear", "fleece", "shearling", "winter", "pullover", "pullovers")) and not has_token(tokens, ("dress", "dresses")):
        if christmas:
            return "/collections/christmas-sweaters"
        if family_matching:
            return "/collections/family-sweaters"
        if daddy_me:
            return "/collections/daddy-and-me"
        return "/collections/fall-winter"

    if family_matching and has_token(tokens, ("romper", "rompers", "cardigan")):
        return "/collections/family-sets"

    if has_phrase(normalized, ("t-shirt", "t-shirts")) or has_token(tokens, ("shirt", "shirts", "top", "tops")):
        if christmas:
            return "/collections/christmas-tops"
        if daddy_me:
            return "/collections/daddy-and-me"
        if mommy_me:
            return MOMMY_ME_REDIRECT_SAFE_TARGET
        if family_matching:
            return "/collections/family-tops"
        return "/collections/matching-outfits"

    if has_token(tokens, ("set", "sets", "outfit", "outfits", "romper", "rompers")) and (family_matching or mommy_me or daddy_me):
        if family_matching:
            return "/collections/family-sets"
        if daddy_me:
            return "/collections/daddy-and-me"
        if mommy_me and has_token(tokens, ("dress", "dresses", "maxi", "midi", "sundress")):
            return "/collections/dresses"
        if mommy_me:
            return MOMMY_ME_REDIRECT_SAFE_TARGET
        return "/collections/family-sets"

    if has_token(tokens, ("dress", "dresses", "maxi", "midi", "sundress")):
        if has_token(tokens, ("formal", "party", "customize", "customized")) or has_token(tokens, ("princess",)) and not has_token(tokens, ("pajamas", "pajama")):
            return "/collections/formal-dresses"
        if has_token(tokens, ("sundress",)):
            return "/collections/sundresses"
        return "/collections/dresses"

    if has_token(tokens, ("jumpsuit", "jumpsuits")):
        return "/collections/jumpsuits"

    if has_token(tokens, ("headband", "turban", "keychain", "bracelet", "pendant", "charms", "charm", "scarf", "shawls", "beanie", "beanies", "hat", "hats")):
        if has_token(tokens, ("winter", "wool", "cashmere", "plaid")):
            return "/collections/fall-winter"
        if mommy_me:
            return MOMMY_ME_REDIRECT_SAFE_TARGET
        return "/collections/matching-outfits"

    if daddy_me:
        return "/collections/daddy-and-me"
    if mommy_me:
        return MOMMY_ME_REDIRECT_SAFE_TARGET
    if family_matching:
        return "/collections/matching-outfits"
    return "/collections/matching-outfits"


def load_table_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def classify_row(url: str) -> Tuple[str, str, str]:
    parsed = urlparse(url)
    path = parsed.path
    segments = [segment for segment in path.split("/") if segment]
    first_segment = segments[0] if segments else ""

    if is_locale_prefix(first_segment) and first_segment not in {"products", "collections", "pages", "blogs"}:
        return "ignore", path, "locale_prefixed"
    if parsed.query:
        return "ignore", path, "parameterized"
    if path.startswith("/products/"):
        return "base_product", path, ""
    if "/collections/" in path and "/products/" in path:
        return "collection_product", path, ""
    return "ignore", path, "non_product"


def handle_from_path(path: str) -> str:
    if "/products/" not in path:
        return ""
    return path.rsplit("/products/", 1)[1].strip("/")


def write_redirect_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Redirect from", "Redirect to"])
        writer.writeheader()
        writer.writerows(rows)


def write_ignored_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["URL", "Path", "Handle", "Reason"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    store_domain = resolve_store_domain(
        args.store_domain,
        env_path=DEFAULT_ENV_PATH,
        fallback_domain=DEFAULT_STORE_DOMAIN,
    )
    access_token = load_access_token(
        args.access_token,
        Path(args.token_file).expanduser(),
        env_path=DEFAULT_ENV_PATH,
    )
    product_statuses = fetch_product_statuses(store_domain, access_token, args.api_version)
    table_rows = load_table_rows(args.table.expanduser())

    redirect_rows: List[Dict[str, str]] = []
    ignored_rows: List[Dict[str, str]] = []
    seen_paths: set[str] = set()
    action_counts: Counter[str] = Counter()

    for row in table_rows:
        url = str(row.get("URL", "") or "").strip()
        if not url:
            continue
        classification, path, reason = classify_row(url)
        handle = handle_from_path(path)

        if classification == "ignore":
            ignored_rows.append({"URL": url, "Path": path, "Handle": handle, "Reason": reason})
            action_counts[reason] += 1
            continue
        if classification == "collection_product" and not args.include_collection_product_paths:
            ignored_rows.append({"URL": url, "Path": path, "Handle": handle, "Reason": "collection_product_path"})
            action_counts["collection_product_path"] += 1
            continue
        if not handle:
            ignored_rows.append({"URL": url, "Path": path, "Handle": handle, "Reason": "missing_handle"})
            action_counts["missing_handle"] += 1
            continue
        if path in seen_paths:
            continue
        seen_paths.add(path)

        status = product_statuses.get(handle, "MISSING")
        if status == "ACTIVE":
            ignored_rows.append({"URL": url, "Path": path, "Handle": handle, "Reason": "active_handle"})
            action_counts["active_handle"] += 1
            continue

        redirect_rows.append(
            {
                "Redirect from": path,
                "Redirect to": target_for_handle(handle),
            }
        )
        action_counts[f"emit_{classification}"] += 1
        action_counts[f"product_status_{status.lower()}"] += 1

    redirect_rows.sort(key=lambda item: item["Redirect from"])
    ignored_rows.sort(key=lambda item: (item["Reason"], item["Path"], item["URL"]))

    write_redirect_csv(args.redirect_csv.expanduser(), redirect_rows)
    write_ignored_csv(args.ignored_csv.expanduser(), ignored_rows)

    print(f"redirect_rows={len(redirect_rows)} ignored_rows={len(ignored_rows)}")
    for key, value in sorted(action_counts.items()):
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
