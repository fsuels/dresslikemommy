#!/usr/bin/env python3
"""Validate translations/<locale>.json files against translation_input.json.
Usage: python3 validate_translations.py <locale> [<locale> ...]  -> exit 1 on errors"""
import json, re, sys, pathlib, unicodedata
HERE = pathlib.Path(__file__).resolve().parent
items = {i["id"]: i for i in json.load(open(HERE / "translation_input.json"))["items"]}
MARK = re.compile(r"\|\s*DLM|\.\.\.|…")
SCRIPT = {"ru": "CYRILLIC", "el": "GREEK", "ar": "ARABIC", "he": "HEBREW", "hi": "DEVANAGARI", "ko": "HANGUL", "ja": ("CJK", "HIRAGANA", "KATAKANA")}
MOM = {"es": "mamá y yo", "fr": "maman et moi", "it": "mamma e me", "pt-BR": "mamãe e eu", "nl": "mama en ik", "da": "mor og barn", "no": "mamma og meg",
       "sv": "mamma och jag", "fi": "äiti ja minä", "pl": "mama i ja", "cs": "máma a já", "ro": "mami și eu", "ru": "мама и я", "el": "μαμά και παιδί",
       "ar": "الأم وأنا", "he": "אמא ואני", "ja": "ママとおそろい", "ko": "엄마와 나", "hi": "माँ और मैं"}
DAD = {"es": "papá y yo", "fr": "papa et moi", "it": "papà e me", "pt-BR": "papai e eu", "nl": "papa en ik", "da": "far og barn", "no": "pappa og meg",
       "sv": "pappa och jag", "fi": "isä ja minä", "pl": "tata i ja", "cs": "táta a já", "ro": "tati și eu", "ru": "папа и я", "el": "μπαμπάς και παιδί",
       "ar": "الأب وأنا", "he": "אבא ואני", "ja": "パパとおそろい", "ko": "아빠와 나", "hi": "पापा और मैं"}
SLOGANS = ["Big Trouble", "Little Trouble", "Mr. Fix It", "Mr. Broke It", "Player 1", "Player 2", "CTRL+C", "CTRL+V", "Top Dad", "Top Son", "Beer Monster",
           "Milk Monster", "Daddysaurus", "Babysaurus", "Bestie", "Remix", "Encore", "LOVE", "Love Grows", "Happy Flower", "I Love Family", "Eternal Love"]
def script_ok(loc, t):
    want = SCRIPT.get(loc)
    if not want: return True
    want = want if isinstance(want, tuple) else (want,)
    letters = [c for c in t if c.isalpha()]
    native = [c for c in letters if any(w in unicodedata.name(c, "") for w in want)]
    return len(native) >= 0.5 * max(1, len(letters) - sum(len(s) for s in SLOGANS if s in t))
errors = warns = 0
for loc in sys.argv[1:]:
    f = HERE / "translations" / f"{loc}.json"
    if not f.exists(): print(f"{loc}: MISSING FILE"); errors += 1; continue
    d = json.load(open(f)).get(loc, {})
    need = {i for i, x in items.items() if loc in x["locales_to_translate"]}
    e = []; w = []
    if set(d) != need: e.append(f"coverage: missing {len(need - set(d))}, extra {len(set(d) - need)}")
    for pid, t in d.items():
        en = items[pid]["en_title"] if pid in items else ""
        if not t or not t.strip(): e.append(f"{pid} empty"); continue
        if MARK.search(t): e.append(f"{pid} truncation marker: {t}")
        if t.strip() == en.strip(): e.append(f"{pid} identical to English")
        if not script_ok(loc, t): e.append(f"{pid} wrong script: {t}")
        if len(t) > 150: w.append(f"{pid} long {len(t)}")
        for n in re.findall(r"\d+", en):
            if n not in t and not (loc in ("ar",) and any(ch.isdigit() for ch in t)): e.append(f"{pid} number {n} missing: {t}")
        for sl in SLOGANS:
            if re.search(r"\b" + re.escape(sl) + r"\b", en) and sl not in t: w.append(f"{pid} slogan '{sl}' not kept: {t}")
        if "Mommy and Me" in en and MOM[loc].lower() not in t.lower(): w.append(f"{pid} mommy term: {t}")
        if "Daddy and Me" in en and DAD[loc].lower() not in t.lower(): w.append(f"{pid} daddy term: {t}")
    print(f"{loc}: {len(d)} titles, {len(e)} errors, {len(w)} warnings")
    for x in e[:8]: print("   ERR", x)
    for x in w[:6]: print("   warn", x)
    errors += len(e); warns += len(w)
print("TOTAL errors", errors, "warnings", warns)
sys.exit(1 if errors else 0)
