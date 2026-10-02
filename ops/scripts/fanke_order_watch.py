#!/usr/bin/env python3
"""Watch real lead times on made-to-order maternity gown orders (owner 2026-10-02).

Owner: "when the first Fanke order arrives, check its real dispatch time in BuckyDrop. It's the one fact that tells us
whether to keep growing this line or find a second Western gown store."

Read-only. Finds Shopify orders that contain a gown listed from 六安凡客 (Lu'an Fanke) or another made-to-order
maternity store (recipes in ops/sourcing/state/recipes/ with custom made_to_order_days > 0), and measures
order created -> first Shopify fulfillment (BuckyDrop pushes the tracking when the parcel leaves its warehouse).
Expected: supplier promise (made_to_order_days) + up to 4 days for domestic transit and warehouse handling.

Usage: fanke_order_watch.py [--write]   (--write updates ops/sourcing/state/fanke_order_watch.json)
Prints one summary line per order and a final VERDICT line for the CEO log.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

import urllib.request  # noqa: E402

STATE = ROOT / "ops/sourcing/state/fanke_order_watch.json"
RECIPES = ROOT / "ops/sourcing/state/recipes"
SLACK_DAYS = 4  # domestic transit to the BuckyDrop warehouse + warehouse handling
SINCE = "2026-10-01"


def gql(query: str, variables: dict | None = None) -> dict:
    url = f"https://{resolve_store_domain('', fallback_domain='dresslikemommy-com.myshopify.com')}/admin/api/2025-01/graphql.json"
    req = urllib.request.Request(url, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": load_access_token("")})
    out = json.loads(urllib.request.urlopen(req, timeout=60).read())
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {out['errors']}")
    return out["data"]


def made_to_order_codes() -> dict[str, dict]:
    codes = {}
    for f in RECIPES.glob("*.json"):
        try:
            rc = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        days = int(rc.get("made_to_order_days") or 0)
        if days <= 0 or not rc.get("code"):
            continue
        store = "Lu'an Fanke" if any("凡客" in x or "Fanke" in x for x in rc.get("evidence_lines", [])) else "other made-to-order"
        codes[f"DLM-{rc['code']}-"] = {"handle": rc["handle"], "days": days, "store": store, "offer": rc.get("offer_id")}
    return codes


def parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def main() -> None:
    codes = made_to_order_codes()
    q = """query($q:String!,$after:String){orders(first:50,after:$after,query:$q,sortKey:CREATED_AT){pageInfo{hasNextPage endCursor}
      nodes{name createdAt cancelledAt displayFulfillmentStatus fulfillments{createdAt status}
      lineItems(first:50){nodes{sku quantity}}}}}"""
    rows, after = [], None
    while True:
        d = gql(q, {"q": f"created_at:>={SINCE}", "after": after})["orders"]
        rows += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            break
        after = d["pageInfo"]["endCursor"]
    now = datetime.now(timezone.utc)
    found = []
    for o in rows:
        hits = [(li, codes[p]) for li in o["lineItems"]["nodes"] for p in codes if (li["sku"] or "").startswith(p)]
        if not hits or o["cancelledAt"]:
            continue
        promise = max(h[1]["days"] for h in hits)
        created = parse(o["createdAt"])
        done = sorted(parse(f["createdAt"]) for f in o["fulfillments"] if f.get("createdAt"))
        limit = promise + SLACK_DAYS
        if done:
            lead = round((done[0] - created).total_seconds() / 86400, 1)
            verdict = "ON_TIME" if lead <= limit else "LATE"
        else:
            lead = round((now - created).total_seconds() / 86400, 1)
            verdict = "OPEN_OK" if lead <= limit else "OPEN_OVERDUE"
        found.append({"order": o["name"], "created": o["createdAt"], "fulfilled": done[0].isoformat() if done else None,
                      "days": lead, "promise_days": promise, "limit_days": limit, "verdict": verdict,
                      "stores": sorted({h[1]["store"] for h in hits}), "handles": sorted({h[1]["handle"] for h in hits})})
    for r in found:
        print(f"{r['order']} {r['verdict']} {r['days']}d (promise {r['promise_days']}d, limit {r['limit_days']}d) "
              f"{'fulfilled ' + r['fulfilled'][:10] if r['fulfilled'] else 'not fulfilled yet'} | {', '.join(r['handles'])}")
    if not found:
        verdict = f"VERDICT NO_ORDERS_YET: no made-to-order maternity gown orders since {SINCE} ({len(codes)} gown SKU codes watched)"
    else:
        late = [r for r in found if r["verdict"] in ("LATE", "OPEN_OVERDUE")]
        closed = [r for r in found if r["fulfilled"]]
        verdict = (f"VERDICT {'FLAG_OWNER' if late else 'OK'}: {len(found)} gown order(s), {len(closed)} fulfilled, "
                   f"{len(late)} late/overdue" + (f" ({', '.join(r['order'] for r in late)}): check the BuckyDrop PO for the "
                                                 f"real supplier dispatch date and tell the owner" if late else ""))
    print(verdict)
    if "--write" in sys.argv:
        STATE.write_text(json.dumps({"checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "verdict": verdict,
                                     "orders": found}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
