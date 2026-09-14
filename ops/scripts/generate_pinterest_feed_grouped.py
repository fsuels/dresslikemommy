#!/usr/bin/env python3.13
"""
Generate a Pinterest-compatible catalog feed (Google-Shopping-style TSV)
with parent-product grouping, for any active Shopify Market.

Path B fallback for the variant-as-product duplication fix. Use this only
when the Shopify Pinterest sales-channel UI does NOT expose a parent-
grouping toggle for the market.

Output schema follows Pinterest's catalog spec, which accepts the same
columns as Google Merchant: id, item_group_id, title, description, link,
image_link, additional_image_link, availability, price, sale_price, brand,
condition, google_product_category, product_type, gtin, mpn, custom_label_*.
Rows without a checksum-valid GTIN are emitted with blank `gtin` and
`identifier_exists=no` for Pinterest-only feed quality.

This script is READ-ONLY against Shopify Admin GraphQL. It does NOT mutate
any product, variant, channel, source, catalog, campaign, billing, theme,
or credential. The generated TSV is local repo evidence only and must be
uploaded to Pinterest separately under explicit owner approval.

Credentials are read from environment variables (sourced from
~/.config/dresslikemommy/shopify-admin.env). Credentials are never written
to the output file or to any other repo file.

Guardrails:
- Never emit `vendor` or `tags` values that contain http(s):// to the feed.
- Never emit supplier/source URLs in any column.
- `item_group_id` is REQUIRED on every emitted row; if a product cannot
  resolve a parent ID, the row is skipped and logged.
- `image_link` is the parent product's featuredImage, never a variant swatch.
- `link` is the parent PDP, never a variant-only URL that hides options.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode

try:
    import urllib.request
    import urllib.error
except Exception:  # pragma: no cover
    print("urllib unavailable; cannot proceed", file=sys.stderr)
    raise


SHOP_DOMAIN_ENV = "SHOPIFY_ADMIN_SHOP_DOMAIN"
ADMIN_TOKEN_ENV = "SHOPIFY_ADMIN_API_TOKEN"
LEGACY_SHOP_DOMAIN_ENV = "SHOPIFY_STORE_DOMAIN"
LEGACY_ADMIN_TOKEN_ENV = "SHOPIFY_ADMIN_ACCESS_TOKEN"
ADMIN_API_VERSION_ENV = "SHOPIFY_ADMIN_API_VERSION"
DEFAULT_API_VERSION = "2025-01"
ADMIN_TOKEN_JSON = Path.home() / ".config/dresslikemommy/admin-api-token.json"

URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)
SUPPLIER_BLOCK_HOSTS = (
    "alibaba.com",
    "aliexpress.com",
    "1688.com",
    "taobao.com",
    "tmall.com",
)

STOREFRONT_BASE_URL = "https://www.dresslikemommy.com"
PUBLIC_COLLECTION_PAGE_SIZE = 250

# Paid-lane labels are intentionally based on the storefront collection intent,
# not on broad product_type/category labels. Priority resolves overlap once.
PAID_LANE_COLLECTION_HANDLES = {
    "mommy_and_me": ("mommy-and-me",),
    "family_matching": ("new-women-outfits",),
    "daddy_and_me": ("daddy-me-shirts", "daddy-me-t-shirts"),
}
PRIMARY_PAID_LANE_PRIORITY = ("daddy_and_me", "family_matching", "mommy_and_me")
PAID_LANE_LABEL_VERSION = "collection_intent_v20260520"


def fatal(msg: str) -> "Exception":
    return SystemExit(f"FATAL: {msg}")


def load_admin_token_json() -> dict:
    if not ADMIN_TOKEN_JSON.exists():
        return {}
    try:
        with ADMIN_TOKEN_JSON.open(encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # pragma: no cover
        raise fatal(f"cannot parse {ADMIN_TOKEN_JSON}: {exc}")


def credential_value(primary_env: str, legacy_env: str, json_key: str) -> str:
    value = os.environ.get(primary_env) or os.environ.get(legacy_env)
    if value:
        return value
    data = load_admin_token_json()
    value = data.get(json_key)
    if value:
        return str(value)
    raise fatal(
        f"missing required credential. Set {primary_env} or {legacy_env}, or provide "
        f"{json_key!r} in ~/.config/dresslikemommy/admin-api-token.json."
    )


def admin_graphql(query: str, variables: dict | None = None) -> dict:
    shop = credential_value(SHOP_DOMAIN_ENV, LEGACY_SHOP_DOMAIN_ENV, "store_domain")
    token = credential_value(ADMIN_TOKEN_ENV, LEGACY_ADMIN_TOKEN_ENV, "access_token")
    version = os.environ.get(ADMIN_API_VERSION_ENV, DEFAULT_API_VERSION)
    url = f"https://{shop}/admin/api/{version}/graphql.json"
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:  # pragma: no cover
        raise fatal(f"Admin API HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}")
    if data.get("errors"):
        raise fatal(f"Admin API errors: {data['errors']}")
    return data["data"]


PRODUCTS_QUERY = """
query Products($cursor: String) {
  products(first: 100, after: $cursor, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        handle
        title
        descriptionHtml
        productType
        vendor
        tags
        onlineStoreUrl
        status
        featuredImage { url }
        images(first: 10) { edges { node { url } } }
        priceRangeV2 {
          minVariantPrice { amount currencyCode }
          maxVariantPrice { amount currencyCode }
        }
        variants(first: 100) {
          edges {
            node {
              id
              sku
              barcode
              price
              compareAtPrice
              availableForSale
              inventoryQuantity
              selectedOptions { name value }
              image { url }
            }
          }
        }
      }
    }
  }
}
"""


def gid_to_numeric(gid: str) -> str:
    if not gid:
        return ""
    return gid.rsplit("/", 1)[-1]


def safe(value: str | None) -> str:
    if value is None:
        return ""
    value = str(value)
    # Block vendor/source URL leakage to feed-visible columns
    if URL_PATTERN.search(value):
        return ""
    lowered = value.lower()
    for host in SUPPLIER_BLOCK_HOSTS:
        if host in lowered:
            return ""
    # Strip TSV-breaking characters
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def parent_link(handle: str, market_handle: str) -> str:
    # For per-market Shopify Markets the public storefront uses /<locale-or-market-prefix>/products/<handle>.
    # The owner-approved expert-level behavior is to emit the canonical PDP URL.
    # Pinterest will respect Shopify Markets country/currency redirects automatically.
    return f"{STOREFRONT_BASE_URL}/products/{handle}"


def fetch_collection_product_handles(collection_handle: str) -> set[str]:
    """Read public storefront collection membership by product handle.

    The Pinterest lane labels should match what shoppers can browse. This uses
    Shopify's public products.json endpoint and never mutates Shopify state.
    """
    handles: set[str] = set()
    page = 1
    while True:
        query = urlencode({"limit": PUBLIC_COLLECTION_PAGE_SIZE, "page": page})
        url = f"{STOREFRONT_BASE_URL}/collections/{collection_handle}/products.json?{query}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:  # pragma: no cover
            raise fatal(f"Storefront collection HTTP {e.code} for {collection_handle}")
        products = payload.get("products") or []
        for product in products:
            handle = safe(product.get("handle"))
            if handle:
                handles.add(handle)
        if len(products) < PUBLIC_COLLECTION_PAGE_SIZE:
            break
        page += 1
        time.sleep(0.1)
        if page >= 40:
            raise fatal(f"too many pages while reading collection {collection_handle}")
    return handles


def build_paid_lane_map() -> tuple[dict[str, dict[str, str | list[str]]], dict]:
    """Build handle -> primary lane/memberships from storefront collection intent."""
    lane_handles: dict[str, set[str]] = {}
    collection_counts: dict[str, dict[str, int | list[str]]] = {}
    for lane, collection_handles in PAID_LANE_COLLECTION_HANDLES.items():
        merged: set[str] = set()
        per_collection_counts: dict[str, int] = {}
        for collection_handle in collection_handles:
            handles = fetch_collection_product_handles(collection_handle)
            merged.update(handles)
            per_collection_counts[collection_handle] = len(handles)
        lane_handles[lane] = merged
        collection_counts[lane] = {
            "collection_handles": list(collection_handles),
            "collection_counts": per_collection_counts,
            "unique_handles": len(merged),
        }

    all_handles = set().union(*lane_handles.values()) if lane_handles else set()
    handle_map: dict[str, dict[str, str | list[str]]] = {}
    for handle in sorted(all_handles):
        memberships = [
            lane
            for lane in PAID_LANE_COLLECTION_HANDLES
            if handle in lane_handles.get(lane, set())
        ]
        primary = "unassigned"
        for lane in PRIMARY_PAID_LANE_PRIORITY:
            if lane in memberships:
                primary = lane
                break
        handle_map[handle] = {"primary": primary, "memberships": memberships}

    overlaps = {
        "mommy_and_me__family_matching": len(
            lane_handles["mommy_and_me"] & lane_handles["family_matching"]
        ),
        "family_matching__daddy_and_me": len(
            lane_handles["family_matching"] & lane_handles["daddy_and_me"]
        ),
        "mommy_and_me__daddy_and_me": len(
            lane_handles["mommy_and_me"] & lane_handles["daddy_and_me"]
        ),
    }
    source_counts = {
        "collection_counts": collection_counts,
        "overlaps": overlaps,
        "primary_priority": list(PRIMARY_PAID_LANE_PRIORITY),
        "label_version": PAID_LANE_LABEL_VERSION,
    }
    return handle_map, source_counts


def map_availability(qty: int | None, available_for_sale: bool) -> str:
    if available_for_sale:
        return "in stock"
    return "out of stock"


PRODUCT_TYPE_CATEGORY_MAP = {
    "couples": "Apparel & Accessories > Clothing > Outfit Sets",
    "dresses": "Apparel & Accessories > Clothing > Dresses",
    "family matching": "Apparel & Accessories > Clothing > Outfit Sets",
    "jumpsuits": "Apparel & Accessories > Clothing > One-Pieces",
    "matching family dresses": "Apparel & Accessories > Clothing > Dresses",
    "matching family outerwear": "Apparel & Accessories > Clothing > Outerwear",
    "matching family pajamas": "Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas",
    "matching family sets": "Apparel & Accessories > Clothing > Outfit Sets",
    "matching family sweaters": "Apparel & Accessories > Clothing > Shirts & Tops",
    "matching family swimwear": "Apparel & Accessories > Clothing > Swimwear",
    "matching family tops": "Apparel & Accessories > Clothing > Shirts & Tops",
    "pajamas": "Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas",
    "sets": "Apparel & Accessories > Clothing > Outfit Sets",
    "sweaters": "Apparel & Accessories > Clothing > Shirts & Tops",
    "swimwear": "Apparel & Accessories > Clothing > Swimwear",
    "tops": "Apparel & Accessories > Clothing > Shirts & Tops",
}


def google_product_category(product_type: str) -> str:
    normalized = safe(product_type).strip().lower()
    return PRODUCT_TYPE_CATEGORY_MAP.get(
        normalized,
        "Apparel & Accessories > Clothing > Outfit Sets",
    )


def is_valid_gtin(value: str) -> bool:
    """Validate GTIN-8/12/13/14 format and checksum."""
    if not value or not value.isdigit() or len(value) not in {8, 12, 13, 14}:
        return False
    digits = [int(ch) for ch in value]
    body = digits[:-1]
    check_digit = digits[-1]
    total = 0
    for index, digit in enumerate(reversed(body)):
        total += digit * (3 if index % 2 == 0 else 1)
    return (10 - total % 10) % 10 == check_digit


def clean_gtin(value: str | None) -> str:
    candidate = safe(value).replace("-", "").replace(" ", "")
    return candidate if is_valid_gtin(candidate) else ""


def emit_grouped_rows(
    market: str,
    products: Iterable[dict],
    paid_lane_map: dict[str, dict[str, str | list[str]]] | None = None,
) -> list[dict]:
    """Emit one row per VARIANT, but every variant carries item_group_id.

    This is "Mode B" from the diagnosis doc and is the safest fallback if
    Pinterest specifically needs per-size rows. For "Mode A" (one row per
    parent), call emit_parent_only_rows instead.
    """
    rows: list[dict] = []
    for p in products:
        parent_id = gid_to_numeric(p.get("id", ""))
        if not parent_id:
            continue
        parent_image = (p.get("featuredImage") or {}).get("url") or ""
        addl_images = []
        for e in (p.get("images") or {}).get("edges", []):
            url = (e.get("node") or {}).get("url")
            if url and url != parent_image:
                addl_images.append(url)
        addl_join = ",".join(addl_images[:10])
        handle = p.get("handle", "")
        title = safe(p.get("title"))
        desc_html = p.get("descriptionHtml") or ""
        # very small text version
        desc_text = re.sub(r"<[^>]+>", " ", desc_html)
        desc_text = safe(re.sub(r"\s+", " ", desc_text))[:5000]
        product_type = safe(p.get("productType"))
        product_category = google_product_category(product_type)
        link = parent_link(handle, market)
        lane_info = (paid_lane_map or {}).get(handle, {})
        primary_paid_lane = safe(str(lane_info.get("primary") or "unassigned"))
        memberships_value = lane_info.get("memberships") or []
        memberships = [
            safe(str(value))
            for value in memberships_value
            if safe(str(value))
        ]
        collection_memberships = "|".join(memberships) if memberships else "unassigned"
        for ve in (p.get("variants") or {}).get("edges", []):
            v = ve.get("node") or {}
            vid = gid_to_numeric(v.get("id", ""))
            if not vid:
                continue
            price = v.get("price") or ""
            sale_price = ""
            cap = v.get("compareAtPrice")
            if cap and price and cap != price:
                # Shopify's compareAtPrice is the "was" price; the live price is the "sale"
                sale_price = price
            qty = v.get("inventoryQuantity") if v.get("inventoryQuantity") is not None else 0
            available = bool(v.get("availableForSale"))
            options = " / ".join(
                f"{o.get('name')}: {o.get('value')}" for o in (v.get("selectedOptions") or [])
            )
            variant_title = f"{title} ({options})" if options else title
            gtin = clean_gtin(v.get("barcode"))
            row = {
                "id": f"shopify_{market.upper()}_{parent_id}_{vid}",
                "item_group_id": parent_id,
                "title": variant_title[:150],
                "description": desc_text,
                "link": link,
                "image_link": parent_image,  # parent featured image, NOT variant swatch
                "additional_image_link": addl_join,
                "availability": map_availability(qty, available),
                "price": price,
                "sale_price": sale_price,
                "brand": "Dress Like Mommy",
                "condition": "new",
                "google_product_category": product_category,
                "product_type": product_type,
                "gtin": gtin,
                "identifier_exists": "yes" if gtin else "no",
                "mpn": safe(v.get("sku")),
                "custom_label_0": market,
                "custom_label_1": product_type or "uncategorized",
                "custom_label_2": primary_paid_lane,
                "custom_label_3": collection_memberships,
                "custom_label_4": PAID_LANE_LABEL_VERSION,
            }
            rows.append(row)
    return rows


def fetch_all_products() -> list[dict]:
    out: list[dict] = []
    cursor: str | None = None
    page = 0
    while True:
        page += 1
        data = admin_graphql(PRODUCTS_QUERY, {"cursor": cursor})
        block = data["products"]
        for edge in block["edges"]:
            out.append(edge["node"])
        info = block["pageInfo"]
        if not info["hasNextPage"]:
            break
        cursor = info["endCursor"]
        time.sleep(0.25)  # gentle pacing
        if page >= 200:  # hard safety stop
            break
    return out


COLUMNS = [
    "id",
    "item_group_id",
    "title",
    "description",
    "link",
    "image_link",
    "additional_image_link",
    "availability",
    "price",
    "sale_price",
    "brand",
    "condition",
    "google_product_category",
    "product_type",
    "gtin",
    "identifier_exists",
    "mpn",
    "custom_label_0",
    "custom_label_1",
    "custom_label_2",
    "custom_label_3",
    "custom_label_4",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--market",
        required=True,
        help="Shopify Market handle (us, canada, united-kingdom, eu, australia, international)",
    )
    ap.add_argument(
        "--output",
        required=True,
        help="Output TSV path. Convention: dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_<market>.tsv",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip Admin API calls; write a 0-row TSV with just headers (for guardrail wiring tests).",
    )
    args = ap.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        rows: list[dict] = []
        paid_lane_source_counts = {}
    else:
        paid_lane_map, paid_lane_source_counts = build_paid_lane_map()
        products = fetch_all_products()
        rows = emit_grouped_rows(args.market, products, paid_lane_map)

    # Sanity check: every row MUST have item_group_id non-empty.
    bad = [r for r in rows if not r.get("item_group_id")]
    if bad:
        print(
            f"GUARDRAIL_VIOLATION: {len(bad)} rows missing item_group_id; aborting write.",
            file=sys.stderr,
        )
        return 2

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=COLUMNS,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)

    unique_parents_by_paid_lane: dict[str, int] = {}
    rows_by_paid_lane: dict[str, int] = {}
    for lane in sorted({r.get("custom_label_2", "unassigned") for r in rows}):
        lane_rows = [r for r in rows if r.get("custom_label_2") == lane]
        rows_by_paid_lane[lane] = len(lane_rows)
        unique_parents_by_paid_lane[lane] = len({r["item_group_id"] for r in lane_rows})

    summary = {
        "market": args.market,
        "output": str(out_path),
        "row_count": len(rows),
        "unique_parents": len({r["item_group_id"] for r in rows}),
        "guardrail_item_group_id_present_on_every_row": all(r.get("item_group_id") for r in rows),
        "paid_lane_source_counts": paid_lane_source_counts,
        "unique_parents_by_paid_lane": unique_parents_by_paid_lane,
        "rows_by_paid_lane": rows_by_paid_lane,
    }
    summary_path = out_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
