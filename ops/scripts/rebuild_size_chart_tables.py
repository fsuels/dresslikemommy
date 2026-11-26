#!/usr/bin/env python3
"""Rebuild translated size-chart tables as exact structural copies of the English table.

For a product and locale, each English <table> that check_size_chart_tables.py treats as a size
chart is rebuilt from the ENGLISH table HTML: same tags, attributes, ids, classes, rows and columns.
Numbers, ranges, units (cm, in, kg, lb/lbs) and size codes (S, M, 2XL, 2T, US ...) are copied byte
for byte. Only text vocabulary (Size, Age, Height, Child, Mother, Years ...) is replaced, and only
through the reviewed glossary (ops/organic/receipts/2026-11-26/retranslate-short/table-glossary.json).
No free translation: a text token the glossary does not cover makes that product-locale SKIP and is
recorded in the "uncovered tokens" list so the glossary can be extended and reviewed.

The rebuilt table replaces ONLY that table inside the existing translated body (matched by id, else
by position); every byte outside the tables is asserted identical. If the translated body has a
different number of tables than English the product-locale is skipped.

  python3 ops/scripts/rebuild_size_chart_tables.py                      # dry run, whole catalog (live read)
  python3 ops/scripts/rebuild_size_chart_tables.py --input cache.json   # dry run from a fetch cache
  python3 ops/scripts/rebuild_size_chart_tables.py --apply --handles a,b --locales de,fr

Stdlib only, Python 3.9. Never prints the token. Reads and writes through the Admin API only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_size_chart_tables as chk  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RECEIPTS = REPO / "ops/organic/receipts/2026-11-26"
GLOSSARY = chk.GLOSSARY
EXCLUDE_FILE = RECEIPTS / "retranslate-short/real.json"
OUT_DIR = RECEIPTS / "table-rebuild"
LOCALES = chk.LOCALES

# --------------------------------------------------------------------------- vocabulary
# (regex, glossary key). Longest/most specific first; matched case-insensitively on the text node.
PHRASES = [
    (r"chest\s*/\s*bust", "chest"),
    (r"pants?\s*/\s*shorts?", "pant"),
    (r"garment\s+length", "garment"),
    (r"coat\s+length", "garment"),
    (r"clothing\s+length", "garment"),
    (r"dress\s+length", "garment"),
    (r"skirt\s+length", "skirt"),
    (r"pants?\s+length", "pants"),
    (r"sleeve\s+length", "sleeve"),
    (r"shoulder\s+width", "shoulder"),
    (r"top\s+length", "_extra:Top Length"),
    (r"shirt\s+length", "_extra:Shirt Length"),
    (r"bust", "chest"),
    (r"hips?", "hip"),
    (r"length", "garment"),
    (r"chest", "chest"),
    (r"sleeve", "sleeve"),
    (r"shoulder", "shoulder"),
    (r"skirt", "skirt"),
    (r"waist", "waist"),
    (r"height", "height"),
    (r"weight", "weight"),
    (r"size", "size"),
    (r"age", "age"),
    (r"or", "or"),
    (r"children|child", "child"),
    (r"adult", "adult"),
    (r"mother", "mother"),
    (r"father", "father"),
    (r"girl", "girl"),
    (r"boy", "boy"),
    (r"years?|yrs?", "_years"),
]
PHRASE_RES = [(re.compile(p + r"(?![^\W\d_'’]|['’])", re.I), k) for p, k in PHRASES]

# Invariant tokens copied byte for byte.
INVARIANT = re.compile(
    r"&[#A-Za-z0-9]+;"                                   # entities
    r"|(?<![A-Za-z\u00c0-\u024f\d])\d+T(?![A-Za-z\u00c0-\u024f])"                 # toddler codes 2T 3T
    r"|(?<![A-Za-z\u00c0-\u024f])\d?(?:XXXL|XXL|XL|XXS|XS|S|M|L)(?![A-Za-z\u00c0-\u024f])"  # size codes
    r"|(?<=\d)(?:W|Y|[A-D]{1,4})(?![A-Za-z\u00c0-\u024f])"             # 4W (US plus sizes), 4Y, bra cup letters 75ABC
    r"|\d+(?:[.,]\d+)?"                                  # numbers (ranges are number - number)
    r"|(?<![A-Za-z\u00c0-\u024f])(?:cm|mm|in|IN|kg|lbs|lb|US)(?![A-Za-z\u00c0-\u024f])"  # units / size system label
    r"|[^\sA-Za-z\d]"                                    # punctuation, symbols (non-latin letters excluded below)
    r"|\s+"
)
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'’]*")
TAG_OR_COMMENT = re.compile(r"(<!--.*?-->|<[^>]+>)", re.S)
CELL_NUMBERS = re.compile(r"\d+(?:[.,]\d+)?")
NUM_BEFORE = re.compile(r"(\d+(?:\s*[-–]\s*\d+)?)\s*$")


def years_word(loc, gl_all, num_text):
    """Return the glossary 'years' word for the number text before it, or None if not derivable."""
    g = gl_all[loc]["years"]
    n = (num_text or "").strip()
    if not n:
        return None if g.startswith("*") else g
    last = int(re.findall(r"\d+", n)[-1])
    if re.fullmatch(r"1", n):
        return gl_all["_singular"][loc]
    if g == "*pl":
        return "rok" if last == 1 else ("lata" if last % 10 in (2, 3, 4) and last % 100 not in (12, 13, 14) else "lat")
    if g == "*cs":
        return "rok" if last == 1 else ("roky" if 2 <= last <= 4 else "let")
    if g == "*ru":
        return ("год" if last % 10 == 1 and last != 11 else
                ("года" if last % 10 in (2, 3, 4) and last % 100 not in (12, 13, 14) else "лет"))
    if g == "*ar":
        # Arabic number rule (Calidad V29): the digit stays in the cell, so no dual (V27 was wrong):
        # 1 -> سنة, 2-10 -> سنوات, 11+ -> سنة; a range follows its last number.
        return "سنوات" if last <= 10 else "سنة"
    if g.startswith("*"):
        return None
    return g


def gloss_value(loc, key, gl_all):
    if key.startswith("_extra:"):
        return gl_all.get("_extra", {}).get(key[7:], {}).get(loc)
    return gl_all.get(loc, {}).get(key)


EXT_FILE = next((p for p in (REPO / "ops/sourcing/size_chart_glossary/glossary-extension.json", OUT_DIR / "glossary-extension.json") if p.exists()), REPO / "ops/sourcing/size_chart_glossary/glossary-extension.json")
_PHRASE_CACHE = {}
MEASURE = (r"\d+(?:[.,]\d+)?(?:\s*[-\u2013]\s*\d+(?:[.,]\d+)?)?(?:\s*(?:cm|mm|in|kg|lbs|lb))?")
PATTERNS = [  # (regex with one capture for the measure x, entry key)
    (re.compile(r"^(?:around|approx\.?)\s+(" + MEASURE + r")$", re.I), "around {x}"),
    (re.compile(r"^(" + MEASURE + r")\s+(?:approx\.?|\(approx\.?\))$", re.I), "around {x}"),
    (re.compile(r"^up\s+to\s+(" + MEASURE + r")$", re.I), "up to {x}"),
    (re.compile(r"^(" + MEASURE + r")\s+(?:and\s+below|or\s+less)$", re.I), "{x} and below"),
    (re.compile(r"^under\s+(" + MEASURE + r")$", re.I), "Under {x}"),
]
NOTES_NOT_GLOSSARY = "needs real translation"


def load_extension(path=EXT_FILE):
    """en -> entry (translations by locale). Reviewed extension, Calidad V28."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {e["en"]: e for e in d["entries"] if isinstance(e.get("translations"), dict)}


def _ext_phrases(ext):
    """(regex, ('ext', en)) lists: multi-word first, then single words. Includes aliases."""
    multi, single = [], []
    for en, e in ext.items():
        if e["kind"] in ("measure pattern", "forms", "invariant code") or "{" in en:
            continue
        for name in [en] + [a for a in e.get("same_as_for", []) if "{" not in a and "(" not in a]:
            pat = re.escape(name).replace("\\ ", r"\s+").replace("\\-", r"\s*-\s*").replace("'", "['\u2019]")
            pat = pat.replace(r"\ ", r"\s+").replace(r"\-", r"\s*-\s*")
            rx = re.compile(pat + r"(?![^\W\d_'\u2019]|['\u2019])", re.I)
            (multi if re.search(r"[\s-]", name) else single).append((rx, ("ext", en)))
    multi.sort(key=lambda t: -len(t[0].pattern))
    return multi, single


def _phrase_lists(gl_all):
    k = id(gl_all.get("_ext"))
    if k not in _PHRASE_CACHE:
        ext = gl_all.get("_ext") or {}
        multi, single = _ext_phrases(ext)
        _PHRASE_CACHE[k] = multi + list(PHRASE_RES) + single
    return _PHRASE_CACHE[k]


def _category(loc, n_text):
    n = (n_text or "").strip()
    nums = re.findall(r"\d+", n)
    if not nums:
        return None
    last = int(nums[-1])
    single = len(nums) == 1
    if loc == "ar":
        if single and last == 1:
            return "one"
        return "few" if last <= 10 else "many"
    if loc == "he":
        return "one" if (single and last == 1) else "many"
    if loc == "ru":
        if last % 10 == 1 and last % 100 != 11:
            return "one"
        return "few" if (last % 10 in (2, 3, 4) and last % 100 not in (12, 13, 14)) else "many"
    if loc == "pl":
        if single and last == 1:
            return "one"
        return "few" if (last % 10 in (2, 3, 4) and last % 100 not in (12, 13, 14)) else "many"
    if loc == "cs":
        return "one" if (single and last == 1) else ("few" if 2 <= last <= 4 else "many")
    if loc == "ro":
        if single and last == 1:
            return "one"
        return "few" if last % 100 <= 19 else "many"
    return "one" if (single and last == 1) else "few"


def months_word(loc, gl_all, num_text, abbr=False):
    forms = ((gl_all.get("_ext") or {}).get("months") or {}).get("translations", {}).get(loc)
    cat = _category(loc, num_text)
    if not forms or not cat:
        return None
    if abbr and loc not in ("ar", "ro"):
        return forms.get("abbr")
    return forms.get(cat) or forms.get("many") or forms.get("few")


def _translate_pattern(seg, loc, gl_all):
    """A measure segment such as 'around 12 kg' / 'up to 15 kg' / '110 cm and below'; None when no match."""
    ext = gl_all.get("_ext") or {}
    core = seg.strip()
    for rx, key in PATTERNS:
        m = rx.match(core)
        if m and key in ext and ext[key]["translations"].get(loc):
            lead = seg[: len(seg) - len(seg.lstrip())]
            trail = seg[len(seg.rstrip()):]
            return lead + ext[key]["translations"][loc].replace("{x}", m.group(1)) + trail
    return None


def translate_text(text, loc, gl_all):
    """Translate one HTML text node. Returns (out, uncovered_tokens)."""
    segs = re.split(r"(\s/\s)", text)
    if len(segs) > 1:
        pats = [(_translate_pattern(x, loc, gl_all) if i % 2 == 0 else None) for i, x in enumerate(segs)]
        if any(pats):
            out, unc = [], []
            for i, x in enumerate(segs):
                if i % 2 == 1:
                    out.append(x)
                elif pats[i] is not None:
                    out.append(pats[i])
                else:
                    o, u = _translate_plain(x, loc, gl_all)
                    out.append(o)
                    unc.extend(u)
            return "".join(out), unc
    pat = _translate_pattern(text, loc, gl_all)
    if pat is not None:
        return pat, []
    return _translate_plain(text, loc, gl_all)


def _translate_plain(text, loc, gl_all):
    out, unc, pos = [], [], 0
    ext = gl_all.get("_ext") or {}
    phrases = _phrase_lists(gl_all)
    while pos < len(text):
        if text[pos].isascii() and text[pos].isalpha():
            if not (pos == 0 or not (text[pos - 1].isascii() and text[pos - 1].isalpha())):
                out.append(text[pos]); pos += 1; continue
            inv = INVARIANT.match(text, pos)
            if inv and re.match(r"[A-Za-z]", inv.group(0)):
                out.append(inv.group(0)); pos = inv.end(); continue  # unit / size code / US / 4W 4Y cups
            mm = MONTHS_RE.match(text, pos)
            if mm:
                nm = NUM_BEFORE.search(text[:pos])
                w = months_word(loc, gl_all, nm.group(1) if nm else "", abbr=mm.group(0).lower() == "mo")
                if w and nm:
                    if loc in ("ja", "ko"):
                        while out and out[-1].isspace():
                            out.pop()
                    out.append(w)
                else:
                    unc.append(mm.group(0)); out.append(mm.group(0))
                pos = mm.end()
                continue
            for rx, key in phrases:
                m = rx.match(text, pos)
                if not m:
                    continue
                if isinstance(key, tuple):
                    v = (ext.get(key[1]) or {}).get("translations", {}).get(loc)
                    if isinstance(v, str) and v:
                        out.append(v)
                    else:
                        unc.append(m.group(0)); out.append(m.group(0))
                elif key == "_years":
                    nm = NUM_BEFORE.search(text[:pos])
                    w = years_word(loc, gl_all, nm.group(1) if nm else "")
                    if not w:
                        unc.append(m.group(0))
                    else:
                        if loc in ("ja", "ko"):  # unit attaches to the number: "9-10歳"
                            while out and out[-1].isspace():
                                out.pop()
                        out.append(w)
                else:
                    v = gloss_value(loc, key, gl_all)
                    if not v:
                        unc.append(m.group(0))
                        out.append(m.group(0))
                    else:
                        out.append(v)
                pos = m.end()
                break
            else:
                w = LATIN_WORD.match(text, pos)
                unc.append(w.group(0))
                out.append(w.group(0)); pos = w.end()
            continue
        inv = INVARIANT.match(text, pos)
        if inv and inv.end() > pos:
            out.append(inv.group(0)); pos = inv.end()
        else:  # non-ASCII letter already in the English table: copy it, it is not vocabulary we can map
            out.append(text[pos]); unc.append(text[pos]); pos += 1
    return "".join(out), unc


MONTHS_RE = re.compile(r"(?:months?|mo)(?![^\W\d_'\u2019]|['\u2019])", re.I)


def tag_skeleton(html):
    return [p for i, p in enumerate(TAG_OR_COMMENT.split(html)) if i % 2 == 1]


def invariant_stream(html):
    """Numbers, units and size codes found in the text nodes, in order (must be identical)."""
    toks = []
    for i, part in enumerate(TAG_OR_COMMENT.split(html)):
        if i % 2 == 0:
            for m in re.finditer(r"\d+(?:[.,]\d+)?|(?<![A-Za-z\u00c0-\u024f])(?:cm|mm|in|IN|kg|lbs|lb|US)(?![A-Za-z\u00c0-\u024f])"
                                 r"|(?<![A-Za-z\u00c0-\u024f])\d?(?:XXXL|XXL|XL|XXS|XS|S|M|L)(?![A-Za-z\u00c0-\u024f])|(?<![A-Za-z\u00c0-\u024f])\d+T(?![A-Za-z\u00c0-\u024f])",
                                 part):
                toks.append(m.group(0))
    return toks


def rebuild_table(en_table, loc, gl_all, cells=None):
    """Pure: English table HTML -> (translated table HTML, uncovered tokens).
    cells (optional list) receives the English text of every cell the glossary cannot cover
    (free-text notes: needs real translation)."""
    parts = TAG_OR_COMMENT.split(en_table)
    unc = []
    for i in range(0, len(parts), 2):
        if parts[i].strip():
            src = parts[i]
            parts[i], u = translate_text(src, loc, gl_all)
            unc.extend(u)
            if u and cells is not None:
                cells.append(re.sub(r"\s+", " ", src.strip()))
        # whitespace-only nodes are copied untouched
    new = "".join(parts)
    if not unc:
        if tag_skeleton(new) != tag_skeleton(en_table):
            return en_table, ["!tag-skeleton"]
        if invariant_stream(new) != invariant_stream(en_table):
            return en_table, ["!invariant-tokens"]
    return new, unc


# --------------------------------------------------------------------------- table spans in a body
def table_spans(html):
    """Top-level <table ...>...</table> spans [(start, end)] (nesting-aware)."""
    spans, depth, start = [], 0, None
    for m in re.finditer(r"<(/?)table\b[^>]*>", html, re.I):
        if m.group(1) == "":
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            if depth == 0:
                continue
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
    return spans


def table_id(tbl_html):
    m = re.match(r"<table\b[^>]*>", tbl_html, re.I)
    mm = re.search(r"\bid\s*=\s*([\"'])(.*?)\1", m.group(0)) if m else None
    return mm.group(2) if mm else ""


def rebuild_body(en_html, tr_html, loc, gl_all):
    """Pure. Returns dict(status, body, uncovered, tables). status in ok, unchanged, uncovered,
    table_count, no_size_table, no_translation."""
    if not tr_html:
        return {"status": "no_translation", "body": None, "uncovered": [], "tables": 0}
    en_sp, tr_sp = table_spans(en_html), table_spans(tr_html)
    en_tabs = [en_html[a:b] for a, b in en_sp]
    tr_tabs = [tr_html[a:b] for a, b in tr_sp]
    en_size = [i for i, t in enumerate(chk.parse_tables(en_html)) if chk.english_is_size_table(t)]
    if len(en_sp) != len(chk.parse_tables(en_html)):
        return {"status": "table_count", "body": None, "uncovered": [], "tables": 0, "note": "english parse mismatch"}
    if not en_size:
        return {"status": "no_size_table", "body": None, "uncovered": [], "tables": 0}
    if len(en_sp) != len(tr_sp):
        return {"status": "table_count", "body": None, "uncovered": [], "tables": len(en_size),
                "en_tables": len(en_sp), "tr_tables": len(tr_sp)}
    repl, uncovered, used = {}, [], set()
    cells_acc = []
    for i in en_size:
        tid = table_id(en_tabs[i])
        j = None
        if tid:
            for k, t in enumerate(tr_tabs):
                if k not in used and table_id(t) == tid:
                    j = k
                    break
        if j is None:
            j = i
            if j in used or (tid and table_id(tr_tabs[j]) not in ("", tid)):
                return {"status": "table_count", "body": None, "uncovered": [], "tables": len(en_size),
                        "note": "no unambiguous table match for %s" % (tid or "#%d" % i)}
        used.add(j)
        new_t, unc = rebuild_table(en_tabs[i], loc, gl_all, cells_acc)
        uncovered.extend(unc)
        repl[j] = new_t
    if uncovered:
        return {"status": "uncovered", "body": None, "uncovered": uncovered, "tables": len(en_size),
                "needs_real_translation": cells_acc}
    out, pos = [], 0
    for k, (a, b) in enumerate(tr_sp):
        out.append(tr_html[pos:a])
        out.append(repl.get(k, tr_html[a:b]))
        pos = b
    out.append(tr_html[pos:])
    body = "".join(out)
    assert bytes_outside_tables_equal(tr_html, body), "bytes outside tables changed"
    return {"status": "ok" if body != tr_html else "unchanged", "body": body, "uncovered": [],
            "tables": len(en_size)}


def outside_tables(html):
    sp = table_spans(html)
    segs, pos = [], 0
    for a, b in sp:
        segs.append(html[pos:a])
        pos = b
    segs.append(html[pos:])
    return segs


def bytes_outside_tables_equal(a, b):
    return outside_tables(a) == outside_tables(b)


# --------------------------------------------------------------------------- orchestration
def load_glossary(with_extension=True):
    g, _ = chk.load_glossary(GLOSSARY)
    if with_extension and EXT_FILE.exists():
        g["_ext"] = load_extension()
    return g


def excluded_handles():
    return {row[0] for row in json.loads(EXCLUDE_FILE.read_text())}


def plan(products, locales, gl_all, handles=None, exclude=()):
    res = {}
    for p in products:
        h = p["handle"]
        if h in exclude or (handles and h not in handles):
            continue
        for loc in locales:
            tr = p["translations"].get(loc)
            res[(h, loc)] = rebuild_body(p["descriptionHtml"], tr["value"] if tr else None, loc, gl_all)
    return res


def coverage(res):
    st = Counter(r["status"] for r in res.values())
    unc = Counter()
    unc_prod = defaultdict(set)
    for (h, loc), r in res.items():
        for t in set(r["uncovered"]):
            unc[(loc, t)] += 1
            unc_prod[(loc, t)].add(h)
    by_token = Counter()
    for (loc, t), n in unc.items():
        by_token[t] += n
    return st, unc, by_token


def admin():
    import organic_engine as oe
    return oe.Admin()


Q_FETCH = ('query($h:String!){productByHandle(handle:$h){id handle bodyHtml status}}')
M_REG = ('mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t)'
         '{userErrors{field message} translations{locale}}}')


def fetch_live(a, handle, locales):
    d = a.gql(Q_FETCH, {"h": handle})["productByHandle"]
    al = " ".join('l%d:translations(locale:"%s"){key value outdated}' % (i, l) for i, l in enumerate(locales))
    t = a.gql('query($id:ID!){translatableResource(resourceId:$id){translatableContent{key value digest} %s}}'
              % al, {"id": d["id"]})["translatableResource"]
    digest = next(c["digest"] for c in t["translatableContent"] if c["key"] == "body_html")
    tr = {}
    for i, l in enumerate(locales):
        for x in t["l%d" % i]:
            if x["key"] == "body_html":
                tr[l] = {"value": x["value"], "outdated": x["outdated"]}
    return {"id": d["id"], "handle": handle, "status": d["status"], "english": d["bodyHtml"], "digest": digest,
            "translations": tr}


def apply_product(a, handle, locales, gl_all):
    f = fetch_live(a, handle, LOCALES)
    results = {}
    for loc in locales:
        tr = f["translations"].get(loc)
        results[loc] = rebuild_body(f["english"], tr["value"] if tr else None, loc, gl_all)
    todo = {l: r for l, r in results.items() if r["status"] == "ok"}
    summary = {"handle": handle, "status": Counter(r["status"] for r in results.values())}
    if not todo:
        return summary
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    before = {"handle": handle, "id": f["id"], "english": f["english"], "digest": f["digest"],
              "before": {l: f["translations"][l] for l in todo}, "locales": sorted(todo)}
    # never overwrite an existing before-state: the first one is the true original
    bf = OUT_DIR / ("%s-before.json" % handle)
    k = 2
    while bf.exists():
        bf = OUT_DIR / ("%s-before-%d.json" % (handle, k))
        k += 1
    bf.write_text(json.dumps(before, ensure_ascii=False, indent=1))
    t = [{"key": "body_html", "value": r["body"], "locale": l, "translatableContentDigest": f["digest"]}
         for l, r in sorted(todo.items())]
    r = a.gql(M_REG, {"id": f["id"], "t": t})["translationsRegister"]
    if r["userErrors"]:
        raise RuntimeError("userErrors: %s" % json.dumps(r["userErrors"])[:400])
    time.sleep(1)
    fin = fetch_live(a, handle, LOCALES)
    match = 0
    for l, rr in todo.items():
        got = fin["translations"][l]
        assert bytes_outside_tables_equal(f["translations"][l]["value"], got["value"]), "outside bytes changed " + l
        if got["value"] == rr["body"] and not got["outdated"]:
            match += 1
    assert fin["english"] == f["english"], "english changed"
    summary.update({"written": len(todo), "readback_match": match, "english_same": True})
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="write translations (default is a dry run)")
    ap.add_argument("--dry-run", action="store_true", help="default; kept for explicitness")
    ap.add_argument("--handles", help="comma-separated handles")
    ap.add_argument("--locales", help="comma-separated locales (default all 20)")
    ap.add_argument("--input", help="fetch cache JSON (check_size_chart_tables --save-input) instead of a live read")
    ap.add_argument("--out", default=str(OUT_DIR), help="dry-run output folder")
    a = ap.parse_args(argv)
    locales = a.locales.split(",") if a.locales else LOCALES
    handles = set(a.handles.split(",")) if a.handles else None
    gl_all = load_glossary()
    exclude = excluded_handles()
    if handles and handles & exclude:
        print("refusing: handles in the retranslation exclusion list: %s" % sorted(handles & exclude))
        return 2
    if a.apply:
        if not handles and not a.input:
            print("--apply requires --handles, or --input (fetch cache) to pick every covered product")
            return 2
        if not handles:
            cache = json.loads(Path(a.input).read_text())
            pl = plan(cache, locales, gl_all, None, exclude)
            handles = {h for (h, _), r in pl.items() if r["status"] == "ok"}
        adm = admin()
        tot = Counter()
        for h in sorted(handles):
            if h in excluded_handles():  # re-read every time: the retranslation list can grow
                print("skip (excluded now): %s" % h)
                continue
            try:
                s = apply_product(adm, h, locales, gl_all)
            except Exception as exc:  # permission or API refusal: stop at once, no workaround
                print("STOP at %s: %s" % (h, str(exc)[:300]))
                return 3
            tot["written"] += s.get("written", 0)
            tot["match"] += s.get("readback_match", 0)
            print(json.dumps(s, default=dict, ensure_ascii=False), flush=True)
        print("TOTAL written=%d readback_match=%d" % (tot["written"], tot["match"]))
        return 0
    if a.input:
        products = json.loads(Path(a.input).read_text())
    else:
        products = chk.fetch_products(LOCALES, sorted(handles) if handles else None)
    res = plan(products, locales, gl_all, handles, exclude)
    st, unc, by_token = coverage(res)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bodies = {"%s|%s" % k: r["body"] for k, r in res.items() if r["status"] == "ok"}
    (out / "proposed-bodies.json").write_text(json.dumps(bodies, ensure_ascii=False))
    # residual check findings on the proposed bodies
    nong, info, outd = defaultdict(list), Counter(), Counter()
    resid = []
    for p in products:
        h = p["handle"]
        tr = {l: {"value": bodies.get("%s|%s" % (h, l), (p["translations"].get(l) or {}).get("value"))}
              for l in locales if (p["translations"].get(l) or {}).get("value")}
        if h in exclude or (handles and h not in handles):
            continue
        for l in list(tr):
            if "%s|%s" % (h, l) not in bodies:
                del tr[l]
        if tr:
            resid.extend(chk.audit_product(h, p["descriptionHtml"], tr, list(tr), gl_all, nong, info, outd))
    summary = {
        "products": len({h for h, _ in res}), "product_locales": len(res), "status": dict(st),
        "uncovered_tokens": [{"token": t, "product_locales": n} for t, n in by_token.most_common()],
        "uncovered_by_locale": {"%s|%s" % k: n for k, n in sorted(unc.items())},
        "table_count_skips": sorted("%s|%s" % k for k, r in res.items() if r["status"] == "table_count"),
        "residual_findings_on_proposed": dict(Counter(f["type"] for f in resid)),
        "residual_examples": resid[:20],
    }
    (out / "dry-run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print("product-locales=%d status=%s" % (len(res), dict(st)))
    print("uncovered tokens:", by_token.most_common(40))
    print("residual findings on proposed bodies:", summary["residual_findings_on_proposed"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
