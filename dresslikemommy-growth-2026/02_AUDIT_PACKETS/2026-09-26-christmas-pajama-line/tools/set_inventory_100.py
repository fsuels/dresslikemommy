#!/usr/bin/env python3
"""Owner rule (2026-09-26): every new listing gets available quantity 100 per
variant at the store location. DRAFT products only; status is not changed."""
import json, sys
from pathlib import Path
import requests
ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
sys.path.insert(0, str(ROOT))
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain
API = f"https://{resolve_store_domain('', fallback_domain='dresslikemommy-com.myshopify.com')}/admin/api/2025-01/graphql.json"
TOKEN = load_access_token("")
LOCATION = "gid://shopify/Location/19326085"
QTY = 100

def gql(query, variables=None):
    r = requests.post(API, headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}}, timeout=120)
    r.raise_for_status(); d = r.json()
    if d.get("errors"): raise RuntimeError(d["errors"])
    return d["data"]

READ = """query($h:String!){productByHandle(handle:$h){id status publishedAt variants(first:100){nodes{sku inventoryItem{id tracked
  inventoryLevels(first:5){nodes{location{id} quantities(names:["available"]){quantity}}}}}}}}"""
for handle in sys.argv[1:]:
    p = gql(READ, {"h": handle})["productByHandle"]
    if not p or p["status"] != "DRAFT" or p["publishedAt"]:
        raise SystemExit(f"{handle}: not an unpublished DRAFT")
    items = [v["inventoryItem"]["id"] for v in p["variants"]["nodes"]]
    res = gql("""mutation($input:InventorySetQuantitiesInput!){inventorySetQuantities(input:$input){userErrors{field message}}}""",
              {"input": {"name": "available", "reason": "correction", "ignoreCompareQuantity": True,
                         "quantities": [{"inventoryItemId": i, "locationId": LOCATION, "quantity": QTY} for i in items]}})
    if res["inventorySetQuantities"]["userErrors"]:
        raise RuntimeError(res["inventorySetQuantities"]["userErrors"])
    after = gql(READ, {"h": handle})["productByHandle"]
    qtys = [lvl["quantities"][0]["quantity"] for v in after["variants"]["nodes"] for lvl in v["inventoryItem"]["inventoryLevels"]["nodes"] if lvl["location"]["id"] == LOCATION]
    ok = len(qtys) == len(items) and all(q == QTY for q in qtys) and after["status"] == "DRAFT"
    print(handle, "OK" if ok else "CHECK", f"{len(items)} variants x {QTY}", after["status"])
