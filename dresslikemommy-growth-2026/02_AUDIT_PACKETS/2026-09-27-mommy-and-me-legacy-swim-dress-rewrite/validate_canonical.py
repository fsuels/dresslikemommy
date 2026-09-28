#!/usr/bin/env python3
"""Validate translations/<loc>.json: coverage, first spaced dash is an em dash,
design length, script, no truncation markers. Usage: validate_canonical.py <loc>..."""
import json, re, sys, pathlib, unicodedata
HERE = pathlib.Path(__file__).resolve().parent
ids = {i["id"] for i in json.load(open(HERE / "translation_input.json"))["items"]}
LIM = {"ja": 20, "ko": 24, "hi": 36, "ru": 38, "el": 38, "ar": 38, "he": 38}
SCRIPT = {"ru": "CYRILLIC", "el": "GREEK", "ar": "ARABIC", "he": "HEBREW", "hi": "DEVANAGARI", "ko": "HANGUL", "ja": ("CJK", "HIRAGANA", "KATAKANA")}
errs = 0
for loc in sys.argv[1:]:
    d = json.load(open(HERE / "translations" / f"{loc}.json"))[loc]; e = []
    if set(d) != ids: e.append(f"coverage missing {len(ids - set(d))} extra {len(set(d) - ids)}")
    for pid, t in d.items():
        m = re.search(r"\s[—–-]\s", t)
        if not m or m.group(0).strip() != "—": e.append(f"{pid} first spaced dash not em dash: {t}"); continue
        design = t[:m.start()]
        if len(design) > LIM.get(loc, 44): e.append(f"{pid} design {len(design)}>{LIM.get(loc, 44)}: {design}")
        if re.search(r"\|\s*DLM|\.\.\.|…", t): e.append(f"{pid} marker")
        w = SCRIPT.get(loc)
        if w:
            w = w if isinstance(w, tuple) else (w,); L = [c for c in t if c.isalpha()]
            if sum(1 for c in L if any(x in unicodedata.name(c, "") for x in w)) < 0.5 * len(L): e.append(f"{pid} script")
    print(f"{loc}: {len(d)} titles, {len(e)} errors"); [print("   ", x) for x in e[:6]]; errs += len(e)
print("TOTAL errors", errs); sys.exit(1 if errs else 0)
