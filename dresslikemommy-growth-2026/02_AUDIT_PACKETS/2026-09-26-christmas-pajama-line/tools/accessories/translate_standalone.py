#!/usr/bin/env python3
"""Translate a standalone (non-engine) listing with the ChatGPT app's bundled Codex (owner's Pro login,
never the API) and register the translations directly, so the localization closeout finds them.

It lists exactly the fields the completeness audit checks (same helpers as
ops/scripts/audit_shopify_product_translation_completeness.py), asks Codex for all 20 locales, then
registers each value with its translatable-content digest.

Usage:
  translate_standalone.py <handle> source   # write <work>/source_en.json + prompt.txt
  translate_standalone.py <handle> run      # run Codex in <work>
  translate_standalone.py <handle> register # register <work>/out/<locale>.json
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "ops" / "scripts"))
from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    ShopifyClient, collect_resource_snapshots, resolve_target_locales, should_translate_field)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

SCRATCH = Path("/tmp/dlm-codex")
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
PROMPT = """You are a professional e-commerce translator for Dress Like Mommy, a store of matching family outfits.
TASK: source_en.json maps each English string to itself. For each of these locales: {LOCALES}, write ./out/<locale>.json (create ./out) with exactly the same keys (the English strings) and the translated string as each value.
RULES:
- Translate every value (not keys). Keep 'Dress Like Mommy' untranslated. Keep all numbers, percent values, "cm", "in" and size codes like 2T exactly.
- The HTML description must keep every tag and attribute exactly (only translate visible text).
- Translate print/style names naturally (they are product style names) so they are NOT identical to the English.
- Size values: "2T" stays "2T"; "3-4 Years" style values become the natural local form of "3-4 years" with the same numbers.
- Natural, fluent shopping copy; no added claims. Never leave a value in English unless it is a number or size code.
{EXTRA}
Do not ask questions; write all files, then reply DONE."""


def client() -> ShopifyClient:
    return ShopifyClient(resolve_store_domain("", fallback_domain="dresslikemommy-com.myshopify.com"), load_access_token(""))


def snapshots(c: ShopifyClient, handle: str):
    product = c.products_by_handles([handle])[0]
    locales = resolve_target_locales(c, "")
    return product, locales, collect_resource_snapshots(c, product.product_gid, locales, 50)


def fields(snaps):
    for s in snaps:
        for item in s.translatable_content:
            key, value = item.get("key", ""), item.get("value") or ""
            if should_translate_field(s.resource_type, key, value):
                yield s, key, value, item.get("digest", "")


def main(handle: str, step: str, extra: str = "") -> None:
    work = SCRATCH / f"codex_{handle[:40]}"
    work.mkdir(parents=True, exist_ok=True)
    c = client()
    product, locales, snaps = snapshots(c, handle)
    items = list(fields(snaps))
    if step == "source":
        (work / "source_en.json").write_text(json.dumps({v: v for _, _, v, _ in items}, ensure_ascii=False, indent=1), encoding="utf-8")
        (work / "prompt.txt").write_text(PROMPT.replace("{LOCALES}", ", ".join(locales)).replace("{EXTRA}", extra), encoding="utf-8")
        print(handle, len(items), "strings", len(locales), "locales", work)
    elif step == "run":
        with open(work / "prompt.txt", encoding="utf-8") as f, open(work / "codex.log", "w") as log:
            rc = subprocess.run(["perl", "-e", "alarm shift; exec @ARGV", "3000", CODEX, "exec", "--skip-git-repo-check",
                                 "-C", str(work), "-s", "workspace-write", "-"], stdin=f, stdout=log, stderr=log, cwd=work).returncode
        got = sorted(p.stem for p in (work / "out").glob("*.json")) if (work / "out").exists() else []
        print("codex rc", rc, "locales", len(got), [l for l in locales if l not in got])
    elif step == "register":
        out = {l: json.loads((work / "out" / f"{l}.json").read_text(encoding="utf-8")) for l in locales}
        per_resource, missing = {}, []
        for s, key, value, digest in items:
            for l in locales:
                t = out[l].get(value)
                if not t:
                    missing.append((l, key, value[:40])); continue
                per_resource.setdefault(s.resource_id, []).append(
                    {"locale": l, "key": key, "value": t, "translatableContentDigest": digest})
        if missing:
            raise SystemExit(f"missing {len(missing)}: {missing[:5]}")
        n = 0
        for rid, trs in per_resource.items():
            for i in range(0, len(trs), 100):
                c.register_translations(rid, trs[i:i + 100]); n += len(trs[i:i + 100])
        print(handle, "registered", n, "resources", len(per_resource))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
