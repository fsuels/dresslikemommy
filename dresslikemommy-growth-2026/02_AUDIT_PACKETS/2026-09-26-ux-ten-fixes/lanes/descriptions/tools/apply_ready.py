#!/usr/bin/env python3
"""Apply READY copy fixes from copy_fixes.json under the packet's apply contract:
precondition sha256(current)==before_sha256, one productUpdate per product,
readback sha256==after_sha256. Writes apply/apply_log.json. Token via shared config."""
import hashlib, json, pathlib, sys, time, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from ops.scripts.shopify_admin_config import load_access_token
URL = "https://dresslikemommy-com.myshopify.com/admin/api/2026-01/graphql.json"
TOKEN = load_access_token()
def gql(q, v=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if d.get("errors"): raise RuntimeError(d["errors"])
    return d["data"]
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
READ = "query($id:ID!){ product(id:$id){ descriptionHtml updatedAt } }"
WRITE = "mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ product{ id } userErrors{ field message } } }"
fixes = json.load(open(ROOT / "copy_fixes.json"))["products"]
execute = "--execute" in sys.argv
log = []
for p in [x for x in fixes if x["fix_status"] == "READY"]:
    row = {"handle": p["handle"], "gid": p["gid"]}
    cur = gql(READ, {"id": p["gid"]})["product"]["descriptionHtml"]
    if sha(cur) == p["after_sha256"]: row["result"] = "ALREADY_APPLIED"
    elif sha(cur) != p["before_sha256"]: row["result"] = "SKIPPED_BEFORE_MISMATCH"
    elif not execute: row["result"] = "WOULD_APPLY"
    else:
        r = gql(WRITE, {"p": {"id": p["gid"], "descriptionHtml": p["after_html"]}})["productUpdate"]
        if r["userErrors"]: row["result"] = f"ERROR {r['userErrors']}"
        else:
            back = gql(READ, {"id": p["gid"]})["product"]["descriptionHtml"]
            row["result"] = "APPLIED_VERIFIED" if sha(back) == p["after_sha256"] else "APPLIED_READBACK_MISMATCH"
        time.sleep(0.4)
    log.append(row); print(row["result"], p["handle"])
(ROOT / "apply").mkdir(exist_ok=True)
json.dump(log, open(ROOT / "apply" / ("apply_log.json" if execute else "dry_run.json"), "w"), indent=1)
from collections import Counter; print(Counter(r["result"] for r in log))
