#!/usr/bin/env python3
"""Minimal Admin GraphQL helper for this packet. Reads the token from the
owner's config file and never prints it. Usage: admin_gql.py <query.graphql> [vars.json]"""
import json, sys, urllib.request, pathlib
cfg = json.loads((pathlib.Path.home() / ".config/dresslikemommy/admin-api-token.json").read_text())
query = pathlib.Path(sys.argv[1]).read_text()
variables = json.loads(pathlib.Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else {}
req = urllib.request.Request(
    f"https://{cfg['store_domain']}/admin/api/2026-01/graphql.json",
    data=json.dumps({"query": query, "variables": variables}).encode(),
    headers={"Content-Type": "application/json", "X-Shopify-Access-Token": cfg["access_token"]},
)
print(json.dumps(json.loads(urllib.request.urlopen(req, timeout=60).read()), indent=2))
