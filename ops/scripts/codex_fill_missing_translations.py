#!/usr/bin/env python3
"""Fill MISSING product translations (metafields such as custom.type / custom.pattern, option names/values) with the
ChatGPT app's bundled Codex (owner's Pro login; never the OpenAI API), across many products at once.

Why: the poller's free machine-translation fallback is rate-limited (Google 429), so short metafield values on older
products ("Swimwear", "Solid") stayed untranslated and failed the listing-localization audit. Only fields that have no
translation at all are touched; existing translations are never overwritten. Unique source strings are translated once.

Usage:
  codex_fill_missing_translations.py collect --handles h1,h2 | --handles-file F   -> <work>/source_en.json + plan.json
  codex_fill_missing_translations.py run                                           -> Codex writes <work>/out/<locale>.json
  codex_fill_missing_translations.py register [--execute]                          -> dry-run by default
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "ops" / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    ShopifyClient, collect_resource_snapshots, infer_product_context, repair_product_html_translation,
    resolve_target_locales, should_translate_field)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

WORK = Path("/tmp/dlm-codex/fill_missing")
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
FILL_TYPES = {"Metafield", "ProductOption", "ProductOptionValue"}
GLOSSARY = ROOT / "ops" / "organic" / "PRODUCT_GLOSSARY.json"
PROMPT = """You are a professional native-language e-commerce translator for Dress Like Mommy, a store of matching family outfits.
TASK: source_en.json maps short English product attribute values (clothing type, pattern, style, option names/values shown to shoppers)
to themselves. For each locale in {LOCALES}, write ./out/<locale>.json (create ./out) with exactly the same keys and the natural local
shop wording as each value.
RULES:
- Short labels stay short (one to four words); keep capitalisation natural for the language; keep numbers and size codes (S, M, 2XL) exactly.
- Follow glossary.json (store glossary with rules) where a term applies: gender-neutral 'Mommy and Me'/'Daddy and Me' values, never the
  'and me' pronoun pattern; 'Child' neutral; Norwegian 'pysjamas'; Hebrew unpointed.
- Never leave a value in English unless the store glossary or the language itself uses the same word.
- Some values are product description HTML: keep every tag, attribute, comment and table cell exactly as in the source and translate
  only the visible text; keep numbers, units (cm, in, kg, lbs) and size codes; add no claims; natural fluent shopping copy.
Do not ask questions; write all files, then reply DONE."""


def client() -> ShopifyClient:
    return ShopifyClient(resolve_store_domain("", fallback_domain="dresslikemommy-com.myshopify.com"), load_access_token(""))


def collect(handles: list[str], types: set[str] = FILL_TYPES, keys: set[str] | None = None, include_outdated: bool = False) -> None:
    c = client()
    locales = resolve_target_locales(c, "")
    WORK.mkdir(parents=True, exist_ok=True)
    plan, sources = [], {}
    for i, product in enumerate(c.products_by_handles(handles), 1):
        for s in collect_resource_snapshots(c, product.product_gid, locales, 100):
            if s.resource_type not in types:
                continue
            for item in s.translatable_content:
                key, value, digest = item.get("key", ""), item.get("value") or "", item.get("digest", "")
                if not should_translate_field(s.resource_type, key, value) or (keys and key not in keys):
                    continue
                missing = [l for l in locales if (l, key) not in s.existing_translations
                           or (include_outdated and s.existing_translations[(l, key)].outdated)]
                if missing:
                    plan.append({"handle": product.handle, "resource_id": s.resource_id, "type": s.resource_type, "key": key,
                                 "value": value, "digest": digest, "locales": missing})
                    sources[value] = value
        print(f"[{i}/{len(handles)}] {product.handle}: {sum(1 for p in plan if p['handle'] == product.handle)} missing fields", flush=True)
    (WORK / "plan.json").write_text(json.dumps({"locales": locales, "rows": plan}, ensure_ascii=False, indent=1), encoding="utf-8")
    (WORK / "source_en.json").write_text(json.dumps(sources, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(plan)} missing fields, {len(sources)} unique strings -> {WORK}")


def run() -> None:
    plan = json.loads((WORK / "plan.json").read_text(encoding="utf-8"))
    if GLOSSARY.exists():
        (WORK / "glossary.json").write_text(GLOSSARY.read_text(encoding="utf-8"), encoding="utf-8")
    (WORK / "prompt.txt").write_text(PROMPT.replace("{LOCALES}", ", ".join(plan["locales"])), encoding="utf-8")
    with open(WORK / "prompt.txt", encoding="utf-8") as f, open(WORK / "codex.log", "w") as log:
        rc = subprocess.run(["perl", "-e", "alarm shift; exec @ARGV", "3000", CODEX, "exec", "--skip-git-repo-check", "-C", str(WORK),
                             "-s", "workspace-write", "-"], stdin=f, stdout=log, stderr=log, cwd=WORK).returncode
    got = sorted(p.stem for p in (WORK / "out").glob("*.json")) if (WORK / "out").exists() else []
    print("codex rc", rc, "locales", len(got), "missing", [l for l in plan["locales"] if l not in got])


def register(execute: bool) -> None:
    plan = json.loads((WORK / "plan.json").read_text(encoding="utf-8"))
    out = {l: json.loads((WORK / "out" / f"{l}.json").read_text(encoding="utf-8")) for l in plan["locales"]}
    per_resource, problems = {}, []
    contexts: dict[str, dict] = {}
    for row in plan["rows"]:
        for l in row["locales"]:
            t = (out[l].get(row["value"]) or "").strip()
            if t and row["type"] == "Product" and row["key"] == "body_html":  # same size-label/chart repair the poller applies
                ctx = contexts.setdefault(row["handle"], infer_product_context(type("P", (), {"handle": row["handle"], "title": ""})(), []))
                t = repair_product_html_translation(row["value"], t, l, product_context=ctx)
            if not t:
                problems.append((l, row["value"][:40]))
                continue
            per_resource.setdefault(row["resource_id"], []).append(
                {"locale": l, "key": row["key"], "value": t, "translatableContentDigest": row["digest"]})
    if problems:
        raise SystemExit(f"{len(problems)} empty translations, e.g. {problems[:5]}")
    total = sum(len(v) for v in per_resource.values())
    if not execute:
        print(f"DRY RUN: would register {total} translations on {len(per_resource)} resources")
        return
    c = client()
    n = 0
    for rid, trs in per_resource.items():
        for i in range(0, len(trs), 100):
            for attempt in range(5):  # Shopify throttles long bulk runs; back off and retry
                try:
                    c.register_translations(rid, trs[i:i + 100])
                    break
                except Exception as exc:  # noqa: BLE001
                    if "THROTTLED" not in str(exc).upper() or attempt == 4:
                        raise
                    time.sleep(10 * (attempt + 1))
            n += len(trs[i:i + 100])
            time.sleep(0.3)
    print(f"registered {n} translations on {len(per_resource)} resources")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["collect", "run", "register"])
    ap.add_argument("--handles", default="")
    ap.add_argument("--handles-file", default="")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--types", default=",".join(sorted(FILL_TYPES)), help="resource types, e.g. Product")
    ap.add_argument("--keys", default="", help="only these field keys, e.g. body_html")
    ap.add_argument("--include-outdated", action="store_true", help="also replace translations marked outdated (English changed)")
    a = ap.parse_args()
    if a.step == "collect":
        raw = Path(a.handles_file).read_text(encoding="utf-8") if a.handles_file else a.handles
        collect([h.strip() for h in raw.replace("\n", ",").split(",") if h.strip()], set(a.types.split(",")),
                set(k for k in a.keys.split(",") if k) or None, a.include_outdated)
    elif a.step == "run":
        run()
    else:
        register(a.execute)


if __name__ == "__main__":
    main()
