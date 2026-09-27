#!/usr/bin/env python3
"""Register the validated seed translations directly on each 2026 Christmas
pajama draft's own translatable resources (product, nested metafields and
option values), without reading or writing the shared translation cache.

Precedent: Beanie Ghost / Christmas Stocking workaround under
PROB-2026-09-25-TRANSLATION-CACHE-CONCURRENT-LOST-UPDATE. The body is passed
through the poller's own repair_product_html_translation so localized size
tables match what the canonical poller would register. Only DRAFT products are
touched, and only values whose stored English source equals a validated seed
source string.

Usage: register_direct.py [--dry-run] handle [handle ...]
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ops/scripts"))

import ops.scripts.poll_shopify_product_translations as poller  # noqa: E402
import seed_cache  # noqa: E402  (validated seed builder; its main() is not run)

DRY = "--dry-run" in sys.argv
handles = [a for a in sys.argv[1:] if not a.startswith("--")]
LOCALES = seed_cache.LOCALES


def main() -> None:
    store = poller.resolve_store_domain("", fallback_domain="dresslikemommy-com.myshopify.com")
    client = poller.ShopifyClient(store, poller.load_access_token(""))
    report = {}
    for handle in handles:
        built = seed_cache.build_for(TOOLS / "specs" / f"{handle}.json")
        if seed_cache.errors:
            raise SystemExit("seed validation failed: " + "; ".join(seed_cache.errors[:10]))
        data = client.graphql(
            "query($h:String!){productByHandle(handle:$h){id handle title status publishedAt createdAt}}",
            {"h": handle},
        )
        product = data["productByHandle"]
        if not product or product["status"] != "DRAFT" or product.get("publishedAt"):
            raise SystemExit(f"{handle}: not an unpublished DRAFT: {product}")
        snapshots = poller.collect_resource_snapshots(client, product["id"], LOCALES, 100)
        recent = poller.RecentProduct(product_gid=product["id"], product_id=product["id"].split("/")[-1],
                                      handle=handle, title=product["title"], status="DRAFT",
                                      created_at=product["createdAt"], updated_at=product["createdAt"])
        context = poller.infer_product_context(recent, snapshots)
        registered = 0
        matched_keys = set()
        for snap in snapshots:
            for item in snap.translatable_content:
                source = item.get("value") or ""
                if not source or source not in built[LOCALES[0]]:
                    continue
                matched_keys.add((snap.resource_type, item["key"]))
                payload = []
                for loc in LOCALES:
                    value = built[loc][source]
                    if snap.resource_type == "Product" and item["key"] == "body_html":
                        value = poller.repair_product_html_translation(source, value, loc, product_context=context)
                    payload.append({"locale": loc, "key": item["key"], "value": value,
                                    "translatableContentDigest": item["digest"]})
                if not DRY:
                    result = client.register_translations(snap.resource_id, payload)
                    registered += len(result.get("translations") or [])
                else:
                    registered += len(payload)
        needed = {("Product", "title"), ("Product", "body_html"), ("Product", "meta_title"), ("Product", "meta_description")}
        missing = needed - matched_keys
        report[handle] = {"product_id": product["id"], "registered": registered,
                          "matched": sorted(f"{a}.{b}" for a, b in matched_keys), "missing_required": sorted(missing)}
        print(handle, "registered" if not DRY else "would register", registered, "missing:", sorted(missing))
        if missing:
            raise SystemExit(f"{handle}: stored source does not match seed for {sorted(missing)}")
    out = TOOLS / "run_logs" / ("register_direct_dry.json" if DRY else "register_direct.json")
    existing = json.loads(out.read_text()) if out.exists() else {}
    existing.update(report)
    out.write_text(json.dumps(existing, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
