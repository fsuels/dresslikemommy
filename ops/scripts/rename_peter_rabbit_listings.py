#!/usr/bin/env python3
"""Rename the three "Peter Rabbit" pajama listings to non-trademarked names.

Owner-approved 2026-09-24: new titles, handles (with 301 redirects), SEO,
body copy, tags, Color option value, custom.pattern, and media alt text.
Translations are refreshed separately with poll_shopify_product_translations.py.

Dry-run by default; pass --execute to write. Before-state lives in
dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-24-peter-rabbit-trademark-rename/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

API_VERSION = "2026-01"
PACKET = REPO_ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-24-peter-rabbit-trademark-rename"
TRADEMARK_RE = re.compile(r"peter\s*rabbit|peter-rabbit", re.I)

PLAN = {
    "gid://shopify/Product/7533379059809": {
        "title": "Watercolor Bunny Garden Mommy and Me Pajamas — Short-Sleeve Set",
        "handle": "watercolor-bunny-garden-mommy-and-me-pajamas",
        "seo_title": "Watercolor Bunny Mommy & Me Pajamas | Dress Like Mommy",
        "seo_description": "Shop our watercolor bunny matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. Kids 1–6Y & Mom One Size.",
        "body": [
            ("Watercolor Peter Rabbit bunnies tucked into", "Watercolor bunnies tucked into"),
            ("Our Peter Rabbit Mommy and Me Pajamas bring", "Our Watercolor Bunny Garden Mommy and Me Pajamas bring"),
            ("Hand-painted-style Peter Rabbit bunnies + meadow florals", "Hand-painted-style bunnies + meadow florals"),
            ("Slip into matching Peter Rabbit pajamas", "Slip into matching bunny garden pajamas"),
        ],
        "tags_remove": ["Peter Rabbit"],
        "tags_add": [],
        "color": ("Peter Rabbit", "Bunny Garden"),
        "pattern": "Watercolor bunnies + meadow floral print",
    },
    "gid://shopify/Product/7533454098529": {
        "title": "Autumn Woodland Bunny Mommy and Me Pajamas — Long-Sleeve Set",
        "handle": "autumn-woodland-bunny-mommy-and-me-pajamas",
        "seo_title": "Autumn Bunny Mommy & Me Pajamas | Dress Like Mommy",
        "seo_description": "Shop our autumn woodland bunny matching mommy-and-me pajamas — soft cotton gauze long-sleeve sets for mom + daughter. Kids 2Y–10Y, Mom S–XL.",
        "body": [
            ('"Autumn Peter Rabbit" — watercolor bunnies', '"Autumn Woodland Bunny" — watercolor bunnies'),
            ("our Autumn Peter Rabbit Mommy and Me Pajamas", "our Autumn Woodland Bunny Mommy and Me Pajamas"),
            ("the print gathers up Peter Rabbit, his leafy friends, and little harvest vignettes",
             "the print gathers up little bunnies, leafy friends, and harvest vignettes"),
        ],
        "tags_remove": ["Peter Rabbit", "Short Sleeve Pajamas"],
        "tags_add": ["Long Sleeve Pajamas"],
        "color": ("Autumn Peter Rabbit", "Autumn Woodland Bunny"),
        "pattern": "Autumn Woodland Bunny",
    },
    "gid://shopify/Product/7533454655585": {
        "title": "Eucalyptus Bunny Gauze Mommy and Me Pajamas — Long-Sleeve Set",
        "handle": "eucalyptus-bunny-gauze-mommy-and-me-pajamas",
        "seo_title": "Eucalyptus Bunny Mommy & Me Pajamas — Gauze | Dress Like Mommy",
        "seo_description": "Shop our eucalyptus bunny matching mommy-and-me pajamas — cotton gauze long-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL.",
        "body": [
            ("Watercolor Peter Rabbit bunnies tucked among", "Watercolor bunnies tucked among"),
            ("Our Peter Rabbit Mommy and Me Pajamas are a cozy", "Our Eucalyptus Bunny Gauze Mommy and Me Pajamas are a cozy"),
            ("a little watercolor Peter Rabbit peeks out", "a little watercolor bunny peeks out"),
            ("Watercolor Peter Rabbit meadow art", "Watercolor bunny meadow art"),
            ("slip into our Peter Rabbit Mommy and Me Pajamas", "slip into our Eucalyptus Bunny Mommy and Me Pajamas"),
        ],
        "tags_remove": ["Peter Rabbit"],
        "tags_add": [],
        "color": ("Peter Rabbit Meadow", "Eucalyptus Bunny Meadow"),
        "pattern": "Watercolor bunnies + eucalyptus meadow print",
    },
}

READ_QUERY = """
query PR($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on Product {
      id title handle descriptionHtml tags
      seo { title description }
      options { id name optionValues { id name } }
      pattern: metafield(namespace: "custom", key: "pattern") { value }
      media(first: 50) { edges { node { id alt } } }
    }
  }
}
"""

PRODUCT_UPDATE = """
mutation U($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id title handle }
    userErrors { field message }
  }
}
"""

OPTION_UPDATE = """
mutation O($productId: ID!, $option: OptionUpdateInput!, $values: [OptionValueUpdateInput!]) {
  productOptionUpdate(productId: $productId, option: $option, optionValuesToUpdate: $values) {
    product { id }
    userErrors { field message }
  }
}
"""

FILE_UPDATE = """
mutation F($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id alt }
    userErrors { field message }
  }
}
"""


def gql(domain: str, token: str, query: str, variables: dict) -> dict:
    resp = requests.post(
        f"https://{domain}/admin/api/{API_VERSION}/graphql.json",
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": token},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"]))
    return data["data"]


def build(product: dict, plan: dict) -> dict:
    body = product["descriptionHtml"]
    for old, new in plan["body"]:
        if body.count(old) != 1:
            raise SystemExit(f"{product['id']}: expected exactly one body match for {old!r}, found {body.count(old)}")
        body = body.replace(old, new)
    if TRADEMARK_RE.search(body):
        raise SystemExit(f"{product['id']}: trademark still present in body after replacements")

    tags = [t for t in product["tags"] if t not in plan["tags_remove"]]
    tags += [t for t in plan["tags_add"] if t not in tags]

    color_opt = next(o for o in product["options"] if o["name"] == "Color")
    old_color, new_color = plan["color"]
    color_val = next(v for v in color_opt["optionValues"] if v["name"] == old_color)

    old_title = product["title"]
    media = []
    for edge in product["media"]["edges"]:
        alt = edge["node"]["alt"] or ""
        if TRADEMARK_RE.search(alt):
            if old_title not in alt:
                raise SystemExit(f"{product['id']}: unexpected alt text {alt!r}")
            media.append({"id": edge["node"]["id"], "alt": alt.replace(old_title, plan["title"])})

    return {
        "product": {
            "id": product["id"],
            "title": plan["title"],
            "handle": plan["handle"],
            "redirectNewHandle": True,
            "descriptionHtml": body,
            "tags": tags,
            "seo": {"title": plan["seo_title"], "description": plan["seo_description"]},
            "metafields": [{
                "namespace": "custom", "key": "pattern",
                "type": "single_line_text_field", "value": plan["pattern"],
            }],
        },
        "option": {
            "productId": product["id"],
            "option": {"id": color_opt["id"]},
            "values": [{"id": color_val["id"], "name": new_color}],
        },
        "files": media,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Write to live Shopify (default: dry-run).")
    args = parser.parse_args()

    domain = resolve_store_domain("")
    token = load_access_token("")
    products = gql(domain, token, READ_QUERY, {"ids": list(PLAN)})["nodes"]

    payloads = {}
    for product in products:
        if not TRADEMARK_RE.search(product["title"]):
            print(f"{product['id']}: already renamed ({product['title']}); skipping")
            continue
        payloads[product["id"]] = build(product, PLAN[product["id"]])

    PACKET.mkdir(parents=True, exist_ok=True)
    (PACKET / "PLANNED_PAYLOADS.json").write_text(json.dumps(payloads, ensure_ascii=False, indent=1))
    for pid, p in payloads.items():
        print(f"{pid}: -> {p['product']['title']} /products/{p['product']['handle']}"
              f" | color -> {p['option']['values'][0]['name']} | alt updates {len(p['files'])}")
    if not args.execute:
        print("dry-run only; payloads written to", PACKET / "PLANNED_PAYLOADS.json")
        return 0

    results = {}
    for pid, p in payloads.items():
        res = {"productUpdate": gql(domain, token, PRODUCT_UPDATE, {"product": p["product"]})["productUpdate"]}
        res["productOptionUpdate"] = gql(domain, token, OPTION_UPDATE, p["option"])["productOptionUpdate"]
        if p["files"]:
            res["fileUpdate"] = gql(domain, token, FILE_UPDATE, {"files": p["files"]})["fileUpdate"]
        results[pid] = res
        errors = [e for r in res.values() for e in r["userErrors"]]
        print(pid, "OK" if not errors else f"ERRORS {errors}")
    (PACKET / "EXECUTION_RESULTS.json").write_text(json.dumps(results, ensure_ascii=False, indent=1))
    return 0 if all(not e for r in results.values() for x in r.values() for e in x["userErrors"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
