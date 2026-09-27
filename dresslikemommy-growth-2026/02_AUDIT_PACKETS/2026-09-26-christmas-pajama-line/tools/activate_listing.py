#!/usr/bin/env python3
"""Activate reviewed DRAFT listings: publish to the store's 8 sales channels, set ACTIVE, read back.

Owner authority (2026-09-27 chat): "activate them … you will have total control of the store".
Precondition checked per handle: DRAFT, 4 media (AI images attached), inventory > 0.
Usage: activate_listing.py handle [handle ...]
"""
import json
import pathlib
import sys
import urllib.request

TOKEN = json.loads(pathlib.Path("~/.config/dresslikemommy/admin-api-token.json").expanduser().read_text())["access_token"]
URL = "https://dresslikemommy-com.myshopify.com/admin/api/2025-01/graphql.json"
PUBLICATIONS = [  # same 8 channels as every active pajama listing
    "gid://shopify/Publication/55169925",     # Online Store
    "gid://shopify/Publication/85065989",     # Buy Button
    "gid://shopify/Publication/8877965409",   # Point of Sale
    "gid://shopify/Publication/21969633377",  # Google & YouTube
    "gid://shopify/Publication/29172400225",  # Facebook & Instagram
    "gid://shopify/Publication/76582879329",  # Pinterest
    "gid://shopify/Publication/76604735585",  # Microsoft Channel
    "gid://shopify/Publication/76604768353",  # TikTok
    # Markets catalog publications (autoPublish only covers newly created products;
    # products restored from ARCHIVED must be added explicitly — incident 2026-09-27).
    "gid://shopify/Publication/77106053217",  # United States catalog
    "gid://shopify/Publication/77105660001",  # Eurozone catalog
    "gid://shopify/Publication/77105823841",  # International catalog
    "gid://shopify/Publication/77105627233",  # Estonia catalog
]


def gql(query, variables=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    out = json.loads(urllib.request.urlopen(req).read())
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {out['errors']}")
    return out["data"]


def activate(handle):
    p = gql("query($h:String!){productByHandle(handle:$h){id status totalInventory mediaCount{count}}}", {"h": handle})["productByHandle"]
    if not p:
        return f"{handle} MISSING"
    if p["mediaCount"]["count"] != 4 or p["totalInventory"] <= 0:
        return f"{handle} SKIP not ready (media={p['mediaCount']['count']} inv={p['totalInventory']})"
    r = gql("mutation($id:ID!,$in:[PublicationInput!]!){publishablePublish(id:$id,input:$in){userErrors{field message}}}",
            {"id": p["id"], "in": [{"publicationId": x} for x in PUBLICATIONS]})["publishablePublish"]
    if r["userErrors"]:
        return f"{handle} PUBLISH ERROR {r['userErrors']}"
    r = gql("mutation($in:ProductInput!){productUpdate(input:$in){userErrors{field message}}}",
            {"in": {"id": p["id"], "status": "ACTIVE"}})["productUpdate"]
    if r["userErrors"]:
        return f"{handle} STATUS ERROR {r['userErrors']}"
    import time
    for _ in range(6):
        after = gql("query($id:ID!){product(id:$id){status onlineStoreUrl resourcePublicationsV2(first:20){nodes{isPublished}} "
                    "us:publishedInContext(context:{country:US}) de:publishedInContext(context:{country:DE}) gb:publishedInContext(context:{country:GB}) "
                    "au:publishedInContext(context:{country:AU}) ca:publishedInContext(context:{country:CA})}}", {"id": p["id"]})["product"]
        markets = {k: after[k] for k in ("us", "de", "gb", "au", "ca")}
        if after["onlineStoreUrl"] and all(markets.values()):
            break
        time.sleep(5)
    pubs = sum(1 for n in after["resourcePublicationsV2"]["nodes"] if n["isPublished"])
    ok = "OK" if after["onlineStoreUrl"] and all(markets.values()) else "NOT VISIBLE"
    return f"{handle} {after['status']} {ok} channels={pubs}/8 markets={''.join(k for k, v in markets.items() if v)} url={after['onlineStoreUrl']}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for h in sys.argv[1:]:
        print(activate(h))
