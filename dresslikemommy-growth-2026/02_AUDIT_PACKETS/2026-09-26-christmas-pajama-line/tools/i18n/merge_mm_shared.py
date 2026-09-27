#!/usr/bin/env python3
"""Validate and merge Codex translations of mode-specific shared strings
(default i18n/mm_shared_en.json; pass another source file name as the second
argument, e.g. sw_shared_en.json) into tr_<loc>.json and en_source.json.

Checks per locale: identical nested structure, placeholders kept, numbers kept,
labels end with a colon, nothing left in English. Nothing is merged unless every
locale passes. Usage: merge_mm_shared.py <codex_out_dir> [source_en.json]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCALES = ["ar", "cs", "da", "de", "el", "es", "fi", "fr", "he", "hi", "it", "ja", "ko", "nl", "no", "pl", "pt-BR", "ro", "ru", "sv"]
SRC = json.loads((HERE / (sys.argv[2] if len(sys.argv) > 2 else "mm_shared_en.json")).read_text(encoding="utf-8"))
NUMS = lambda s: sorted(re.findall(r"\d+(?:\.\d+)?", s))
UNTRANSLATABLE = {"Winter"}  # identical in several locales (e.g. de "Winter")


def walk(en, tr, path, probs):
    if isinstance(en, dict):
        if not isinstance(tr, dict) or set(en) != set(tr):
            probs.append(f"{path}: keys differ")
            return
        for k in en:
            walk(en[k], tr[k], f"{path}.{k}", probs)
        return
    if not isinstance(tr, str) or not tr.strip():
        probs.append(f"{path}: empty")
        return
    for ph in re.findall(r"\{[A-Z]+\}", en):
        if ph not in tr:
            probs.append(f"{path}: lost {ph}")
    if NUMS(en) != NUMS(tr) and "p2" not in path:
        probs.append(f"{path}: numbers {NUMS(tr)} != {NUMS(en)}")
    if path.endswith("_label_mm") and not tr.rstrip().endswith((":", "：")):
        probs.append(f"{path}: label colon")
    if tr.strip() == en.strip() and en not in UNTRANSLATABLE and not en.startswith("{P}") and "Dress Like Mommy" not in en:
        probs.append(f"{path}: untranslated")


def main():
    out = Path(sys.argv[1])
    probs = []
    trs = {}
    for loc in LOCALES:
        f = out / f"{loc}.json"
        if not f.exists():
            probs.append(f"{loc}: missing")
            continue
        trs[loc] = json.loads(f.read_text(encoding="utf-8"))
        walk(SRC, trs[loc], loc, probs)
    if probs:
        print("\n".join(probs[:80]))
        raise SystemExit(f"{len(probs)} problems; nothing merged")
    for loc, t in trs.items():
        p = HERE / f"tr_{loc}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        for group, vals in t.items():
            d.setdefault(group, {}).update(vals)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    e = json.loads((HERE / "en_source.json").read_text(encoding="utf-8"))
    for group, vals in SRC.items():
        e.setdefault(group, {}).update(vals)
    (HERE / "en_source.json").write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    print("merged mommy-and-me shared strings into", len(trs), "locales + en_source")


if __name__ == "__main__":
    main()
