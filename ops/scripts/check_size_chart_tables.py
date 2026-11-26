#!/usr/bin/env python3
"""Read-only audit of translated size-chart tables against the English tables.

For every ACTIVE product (Admin GraphQL, reads only) it parses the size-chart
tables in the English descriptionHtml and the matching table in each translated
body_html (match by table id, else by position among size-like tables), then
compares cell by cell:

  numeric_mismatch      a number differs from English (most serious)
  numeric_reordered     same numbers, different order
  numeric_rounded       same numbers within 0.06 (precision changed, e.g. 22.05 -> 22.0462)
  numeric_dropped       translated cell lacks numbers English has (e.g. imperial values omitted)
  decimal_comma_unlisted decimal comma in a locale that does not use it
  size_code_mismatch    size codes differ from English (converted: S-3XL -> P-3GG)
  table_missing / table_count / row_count / col_count
  english_residue       English header/label vocabulary left in a translated cell
  age_unit_wrong        age written with a calendar-year word (ja 年, ko 연도)
  duplicated_header     same header twice in one row (or "X/X" inside one cell)
  label_swapped         mother/father/child label differs in role from English
  nonglossary           header/row label/age unit not equal to the glossary term
                        (aggregated with counts for one-pass review)

Info only (not findings): decimal_comma_ok, native_digits, outdated translations.

Stdlib only, Python 3.9. Never prints the token. No store writes.

  python3 ops/scripts/check_size_chart_tables.py --json
  python3 ops/scripts/check_size_chart_tables.py --handles a,b --locales ja,ko
  python3 ops/scripts/check_size_chart_tables.py --input cache.json --fail-on-findings
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GLOSSARY = next((p for p in (REPO / "ops/sourcing/size_chart_glossary/table-glossary.json", REPO / "ops/organic/receipts/2026-11-26/retranslate-short/table-glossary.json") if p.exists()), REPO / "ops/sourcing/size_chart_glossary/table-glossary.json")
TOKEN_FILE = Path.home() / ".config/dresslikemommy/admin-api-token.json"
ENDPOINT = "https://dresslikemommy-com.myshopify.com/admin/api/2026-10/graphql.json"

LOCALES = ["ar", "cs", "da", "de", "el", "es", "fi", "fr", "he", "hi", "it", "ja", "ko",
           "nl", "no", "pl", "pt-BR", "ro", "ru", "sv"]
DECIMAL_COMMA_OK = {"cs", "de", "es", "fr", "it", "nl", "pl", "pt-BR", "ru", "sv", "da", "no", "fi", "ro", "el"}

# Reviewer corrections (quality-v24 V25-2) applied in memory when the glossary file lacks them.
V25_FIXES = {
    "fi": {"shoulder": "Hartialeveys", "chest": "Rinnanympärys", "hip": "Lantionympärys"},
    "fr": {"height": "Stature", "shoulder": "Carrure"},
    "de": {"garment": "Gesamtlänge", "shoulder": "Schulterbreite"},
    "cs": {"shoulder": "Šířka ramen"},
    "pl": {"shoulder": "Szerokość ramion"},
    "ru": {"shoulder": "Ширина плеч"},
    "sv": {"shoulder": "Axelbredd"},
    "da": {"shoulder": "Skulderbredde"},
    "he": {"girl": "ילדה", "boy": "ילד"},
}

# Acceptable "years" words per locale (age unit); glossary value is added when real.
YEAR_WORDS = {
    "ar": ["سنة", "سنوات", "سنتين", "سنتان", "عام", "أعوام"],
    "cs": ["let", "roky", "rok", "roků"],
    "da": ["år"], "de": ["Jahre", "Jahr", "Jahren"], "el": ["ετών", "έτους", "ετών", "χρονών", "έτη"],
    "es": ["años", "año"], "fi": ["v", "vuotta", "vuotias", "vuotiaat", "vuoden"],
    "fr": ["ans", "an"], "he": ["שנים", "שנה", "שנתיים", "שנות"], "hi": ["वर्ष", "साल", "वर्षों"],
    "it": ["anni", "anno"], "ja": ["歳", "才"], "ko": ["세", "살"], "nl": ["jaar", "jr"], "no": ["år"],
    "pl": ["lat", "lata", "rok", "roku"], "pt-BR": ["anos", "ano"], "ro": ["ani", "an"],
    "ru": ["лет", "года", "год", "г"], "sv": ["år"],
}
# Calendar-year words that are wrong for an age.
YEAR_WRONG = {"ja": ["年"], "ko": ["연도", "년", "해"]}

# English header/label vocabulary that must not stay in translated cells.
EN_VOCAB = ["size", "length", "bust", "chest", "waist", "hip", "hips", "height", "weight", "child",
            "children", "kids", "kid", "mother", "mom", "mommy", "father", "dad", "daddy", "girl",
            "boy", "adult", "years", "year", "months", "month", "suggested", "recommended",
            "shoulder", "sleeve", "skirt", "pants", "strap", "hem", "opening", "adjustable",
            "garment", "age", "toddler", "women", "woman", "men", "man", "inch", "inches"]
EN_VOCAB_SAFE = {"baby", "top", "mini", "midi", "maxi", "set", "body", "shorts", "dress", "cm", "kg", "lbs", "in"}

LAT = "A-Za-z0-9\u00c0-\u024f"  # Latin letters/digits incl. accented: a size code never touches these
EN_CODE = r"(?<![" + LAT + r"])\d?(?:XXXL|XXL|XL|XS|S|M|L)(?![" + LAT + r"])"
CONV_CODE = (r"(?<![" + LAT + r"])\d?(?:XXG|XGG|XG|EGG|EG|PP|GG|TL|TS|P|G)(?![" + LAT + r"])"
             r"|(?<![Ѐ-ӿ])[СМЛ](?![Ѐ-ӿ])"
             r"|\d?(?:एक्स)*(?:एस|एम|एल)")
EN_CODE_RE = re.compile(EN_CODE)
CONV_CODE_RE = re.compile(CONV_CODE)
NUM_RE = re.compile(r"\d+(?:[.,٫]\d+)?")

HEADER_KEYS = [  # (regex on English header, glossary key)
    (r"shoulder", "shoulder"), (r"skirt", "skirt"), (r"(pants?|trouser).*length|length.*(pants?|trouser)", "pants"),
    (r"sleeve", "sleeve"), (r"bust|chest", "chest"), (r"waist", "waist"), (r"\bhips?\b", "hip"),
    (r"height", "height"), (r"weight", "weight"), (r"\bage\b", "age"), (r"length|garment", "garment"),
    (r"^size$", "size"),
]
ROLE_KEYS = [  # (regex on English row label start, glossary key)
    (r"^(mother|mom|mommy|mama|women'?s?|woman|ladies|adult woman)\b", "mother"),
    (r"^(father|dad|daddy|papa|men'?s?|man)\b", "father"),
    (r"^(girl'?s?)\b", "girl"), (r"^(boy'?s?)\b", "boy"),
    (r"^(child|children|kid|kids|toddler)\b", "child"), (r"^(adult)\b", "adult"),
]


# --------------------------------------------------------------------------- parsing
class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self._t = None
        self._row = None
        self._cell = None
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._depth += 1
            if self._depth == 1:
                self._t = {"id": dict(attrs).get("id") or "", "rows": []}
        elif self._t is not None and self._depth == 1:
            if tag == "tr":
                self._row = []
            elif tag in ("td", "th") and self._row is not None:
                self._cell = {"tag": tag, "text": []}
            elif tag == "br" and self._cell is not None:
                self._cell["text"].append(" ")

    def handle_endtag(self, tag):
        if tag == "table":
            if self._depth == 1 and self._t is not None:
                self.tables.append(self._t)
                self._t = None
            self._depth = max(0, self._depth - 1)
        elif self._t is not None and self._depth == 1:
            if tag in ("td", "th") and self._cell is not None and self._row is not None:
                self._row.append((self._cell["tag"], clean(" ".join(self._cell["text"]))))
                self._cell = None
            elif tag == "tr" and self._row is not None:
                if self._row:
                    self._t["rows"].append(self._row)
                self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell["text"].append(data)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


SIZE_HEAD_RE = re.compile(r"\b(size|bust|chest|waist|hips?|height|weight|length|sleeve|shoulder|age)\b", re.I)


def parse_tables(body_html):
    """Return all tables as {id, rows:[[(tag,text)...]]}."""
    p = _TableParser()
    try:
        p.feed(body_html or "")
        p.close()
    except Exception:
        pass
    return p.tables


def english_is_size_table(t):
    if "size" in t["id"].lower():
        return True
    if not t["rows"]:
        return False
    head = " ".join(c[1] for c in t["rows"][0])
    return len(SIZE_HEAD_RE.findall(head)) >= 2


def match_tables(en_html, tr_html):
    """Yield (en_index_among_size, en_table, tr_table_or_None) matching by id, else by position."""
    en_all = parse_tables(en_html)
    tr_all = parse_tables(tr_html)
    en_sz = [(i, t) for i, t in enumerate(en_all) if english_is_size_table(t)]
    used = set()
    out = []
    for pos, (i, et) in enumerate(en_sz):
        tt = None
        if et["id"]:
            for j, t in enumerate(tr_all):
                if j not in used and t["id"] == et["id"]:
                    tt = j
                    break
        if tt is None and i < len(tr_all) and i not in used:
            tt = i if (not et["id"] or not tr_all[i]["id"] or tr_all[i]["id"] == et["id"]) else None
        if tt is None:
            # same position among tables with a size-like shape
            cand = [j for j, t in enumerate(tr_all) if j not in used and english_is_size_table(t)]
            if pos < len(cand):
                tt = cand[pos]
        if tt is not None:
            used.add(tt)
        out.append((pos, et, tr_all[tt] if tt is not None else None))
    return out, len(en_sz), len(tr_all)


# --------------------------------------------------------------------------- pure comparison helpers
def to_ascii_digits(s):
    out = []
    for ch in s:
        if ch.isdigit() and not ch.isascii():
            try:
                out.append(str(unicodedata.decimal(ch)))
                continue
            except ValueError:
                pass
        out.append(ch)
    return "".join(out)


def strip_codes(s, translated):
    s = EN_CODE_RE.sub(" ", s)
    if translated:
        s = CONV_CODE_RE.sub(" ", s)
    return s


def numbers(cell, translated=False):
    """List of raw numeric tokens (ASCII digits) with codes removed."""
    s = to_ascii_digits(cell)
    s = strip_codes(s, translated)
    return NUM_RE.findall(s)


def norm_num(tok):
    return tok.replace(",", ".").replace("٫", ".")


def _close(a, b):
    try:
        return a == b or abs(float(a) - float(b)) <= 0.06
    except ValueError:
        return False


def _is_subsequence(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


def is_dual_age_word(en_cell, tr_cell, locale):
    """ar/he write 1 and 2 years as words (سنة / سنتين, שנה / שנתיים): the digit is legitimately gone."""
    return (locale in ("ar", "he") and numbers(en_cell) in (["1"], ["2"]) and not numbers(tr_cell, True)
            and bool(re.search(r"year", en_cell, re.I)))


def compare_numbers(en_cell, tr_cell):
    """Return (kind, detail). kind in ok, numeric_mismatch, numeric_reordered, decimal_comma, native_digits."""
    en = numbers(en_cell)
    tr_raw = numbers(tr_cell, True)
    tr = [norm_num(x) for x in tr_raw]
    if en == tr:
        kinds = []
        if any(("," in a or "٫" in a) for a in tr_raw):
            kinds.append("decimal_comma")
        if to_ascii_digits(tr_cell) != tr_cell:
            kinds.append("native_digits")
        return (kinds[0] if kinds else "ok"), {"info": kinds}
    if sorted(en) == sorted(tr):
        return "numeric_reordered", {"en": en, "tr": tr}
    if len(en) == len(tr) and all(_close(a, b) for a, b in zip(en, tr)):
        return "numeric_rounded", {"en": en, "tr": tr}
    if tr != en and _is_subsequence(tr, en):
        return "numeric_dropped", {"en": en, "tr": tr}
    return "numeric_mismatch", {"en": en, "tr": tr}


def size_codes(cell):
    return EN_CODE_RE.findall(cell)


def compare_size_codes(en_cell, tr_cell):
    """Return None when codes match, else dict(kind='converted'|'mismatch', en, tr)."""
    en = size_codes(en_cell)
    tr = size_codes(tr_cell)
    if en == tr:
        return None
    conv = CONV_CODE_RE.findall(tr_cell)
    if not en and not conv:
        return None
    if not en:
        return {"kind": "converted", "en": en, "tr": conv}
    return {"kind": "converted" if conv else "mismatch", "en": en, "tr": tr or conv}


def english_residue(tr_cell, locale, glossary_words):
    """English vocabulary words left in a translated text cell."""
    words = re.findall(r"(?<![A-Za-z])[A-Za-z]{2,}(?![A-Za-z])", tr_cell)
    found = []
    for w in words:
        lw = w.lower()
        if lw in EN_VOCAB_SAFE or lw in glossary_words:
            continue
        if (locale == "nl" and lw in ("inch", "inches")) or (locale == "ro" and lw == "bust"):
            continue  # legitimate words in those languages
        if lw in EN_VOCAB:
            found.append(w)
    return found


def age_unit_issue(en_cell, tr_cell, locale):
    """None, or ('wrong'|'unknown', unit_text) for rows whose English cell is an age in Years."""
    if not re.search(r"\d\s*(?:-|to|–)?\s*\d*\s*years?\b", en_cell, re.I):
        return None
    for w in YEAR_WRONG.get(locale, []):
        if re.search(r"\d\s*" + re.escape(w), to_ascii_digits(tr_cell)):
            return ("wrong", w)
    return None


def unit_text(tr_cell, glossary_roles):
    """Leftover words after removing digits, separators, codes and glossary role words."""
    s = to_ascii_digits(tr_cell)
    s = strip_codes(s, True)
    s = NUM_RE.sub(" ", s)
    for w in sorted(glossary_roles, key=len, reverse=True):
        s = s.replace(w, " ")
    s = re.sub(r"[\-–—~～〜/(),.:;]", " ", s)
    return clean(s)


def year_words(locale, gloss):
    yw = list(YEAR_WORDS.get(locale, []))
    gy = gloss.get("years", "")
    if gy and not gy.startswith("*") and gy not in yw:
        yw.append(gy)
    return yw


def has_year_word(text, years):
    low = text.casefold()
    toks = re.split(r"\s+", low)
    for w in years:
        wl = w.casefold()
        if len(wl) == 1 and (wl.isascii() or "\u0400" <= wl <= "\u04ff"):
            if wl in toks:
                return True
        elif wl in low:
            return True
    return False


def label_stem(tr_label, years):
    """Translated row label without numbers, size codes, age words and separators."""
    s = unit_text(tr_label, [])
    for w in sorted(years, key=len, reverse=True):
        if len(w) > 1 or ord(w[0]) > 0x2E80:
            s = s.replace(w, " ")
    return clean(s)



def duplicated_headers(en_row, tr_row):
    """Header duplicated in the translation but distinct in English; also 'X/X' inside a cell."""
    out = []
    norm = lambda s: re.sub(r"\(.*?\)", "", s).strip().casefold()
    en_n = [norm(c) for c in en_row]
    tr_n = [norm(c) for c in tr_row]
    seen = {}
    for i, t in enumerate(tr_n):
        if not t:
            continue
        if t in seen and (i >= len(en_n) or seen[t] >= len(en_n) or en_n[i] != en_n[seen[t]]):
            out.append({"cols": [seen[t], i], "value": tr_row[i]})
        seen.setdefault(t, i)
    for i, c in enumerate(tr_row):
        base = re.sub(r"\(.*?\)", "", c).strip()
        parts = [p.strip() for p in re.split(r"\s*/\s*", base) if p.strip()]
        if len(parts) == 2 and parts[0].casefold() == parts[1].casefold():
            en_base = re.sub(r"\(.*?\)", "", en_row[i] if i < len(en_row) else "").strip()
            en_parts = [x.strip().casefold() for x in re.split(r"\s*/\s*", en_base) if x.strip()]
            if len(en_parts) != 2 or en_parts[0] != en_parts[1]:
                out.append({"cols": [i], "value": c})
    return out


def en_role(label):
    l = label.strip().lower()
    for rx, key in ROLE_KEYS:
        if re.search(rx, l):
            return key
    if re.match(r"^baby\b", l):
        return "baby"
    return None


def en_header_key(h):
    s = re.sub(r"\(.*?\)", "", h).strip().lower()
    for rx, key in HEADER_KEYS:
        if re.search(rx, s):
            return key
    return None


def role_in_label(tr_label, gloss):
    """Glossary roles whose term appears in the translated label."""
    low = tr_label.casefold()
    return {k for k in ("mother", "father", "girl", "boy", "child", "adult")
            if gloss.get(k) and gloss[k].casefold() in low}


def label_swapped(en_label, tr_label, gloss):
    """Return the swapped role found, or None."""
    er = en_role(en_label)
    if er not in ("mother", "father", "girl", "boy", "child", "adult"):
        return None
    found = role_in_label(tr_label, gloss)
    if not found or er in found:
        return None
    if er in ("girl", "boy", "child") and found <= {"child", "girl", "boy"}:
        return None  # child/girl/boy are near-synonyms
    return sorted(found)[0]


def header_term(tr_header):
    return clean(re.sub(r"\(.*?\)", "", tr_header))


def header_matches_glossary(key, tr_header, gloss):
    term = gloss.get(key)
    if not term:
        return True
    return term.casefold() in tr_header.casefold()


# --------------------------------------------------------------------------- glossary
def load_glossary(path=GLOSSARY):
    g = json.loads(Path(path).read_text(encoding="utf-8"))
    applied = False
    for loc, fixes in V25_FIXES.items():
        for k, v in fixes.items():
            if g.get(loc, {}).get(k) != v:
                g.setdefault(loc, {})[k] = v
                applied = True
    return g, applied


# --------------------------------------------------------------------------- table audit
def audit_table(handle, locale, pos, en_t, tr_t, gloss, nonglossary, info):
    """Compare one English/translated table pair; return list of findings."""
    F = []
    base = {"handle": handle, "locale": locale, "table": en_t["id"] or "#%d" % pos}

    def add(typ, **kw):
        d = dict(base)
        d["type"] = typ
        d.update(kw)
        F.append(d)

    if tr_t is None:
        add("table_missing")
        return F
    er, tr = en_t["rows"], tr_t["rows"]
    if len(er) != len(tr):
        add("row_count", en=len(er), tr=len(tr))
    en_head = [c[1] for c in er[0]] if er else []
    tr_head = [c[1] for c in tr[0]] if tr else []
    gl_words = {w.lower() for v in gloss.values() if isinstance(v, str) for w in re.findall(r"[A-Za-z]+", v)}
    role_terms = [v for k, v in gloss.items() if k in ("mother", "father", "girl", "boy", "child", "adult", "baby") and v]
    for d in duplicated_headers(en_head, tr_head):
        add("duplicated_header", col=" | ".join(en_head[c] for c in d["cols"] if c < len(en_head)), tr=d["value"])
    for ci, h in enumerate(tr_head):
        if ci >= len(en_head):
            continue
        key = en_header_key(en_head[ci])
        res = english_residue(h, locale, gl_words)
        if res:
            add("english_residue", row="(header)", col=en_head[ci], en=en_head[ci], tr=h, words=res)
        if key and key != "size" and not header_matches_glossary(key, h, gloss):
            nonglossary[(locale, "header:" + key, gloss.get(key, ""), header_term(h))].append(handle)
        elif key == "size" and not header_matches_glossary("size", h, gloss):
            nonglossary[(locale, "header:size", gloss.get("size", ""), header_term(h))].append(handle)
    swap_stems = defaultdict(set)
    for ri in range(1, min(len(er), len(tr))):
        en_row = [c[1] for c in er[ri]]
        tr_row = [c[1] for c in tr[ri]]
        row_label = en_row[0] if en_row else ""
        if len(en_row) != len(tr_row):
            add("col_count", row=row_label, en=len(en_row), tr=len(tr_row))
        for ci in range(min(len(en_row), len(tr_row))):
            ec, tc = en_row[ci], tr_row[ci]
            col = en_head[ci] if ci < len(en_head) else "col%d" % ci
            kind, det = compare_numbers(ec, tc)
            if kind == "numeric_dropped" and is_dual_age_word(ec, tc, locale):
                info["ar_he_age_word_for_number"] += 1
            elif kind in ("numeric_mismatch", "numeric_reordered", "numeric_dropped", "numeric_rounded"):
                add(kind, row=row_label, col=col, en=ec, tr=tc)
            elif kind == "decimal_comma":
                if locale in DECIMAL_COMMA_OK:
                    info["decimal_comma_ok"] += 1
                else:
                    add("decimal_comma_unlisted", row=row_label, col=col, en=ec, tr=tc)
            elif kind == "native_digits":
                info["native_digits"] += 1
            sc = compare_size_codes(ec, tc)
            if sc:
                add("size_code_mismatch", row=row_label, col=col, en=ec, tr=tc, kind=sc["kind"],
                    en_codes=sc["en"], tr_codes=sc["tr"])
            res = english_residue(tc, locale, gl_words)
            if res:
                add("english_residue", row=row_label, col=col, en=ec, tr=tc, words=res)
            au = age_unit_issue(ec, tc, locale)
            if au:
                add("age_unit_wrong", row=row_label, col=col, en=ec, tr=tc, found=au[1])
        # label checks on column 0
        if en_row and tr_row:
            role = en_role(en_row[0])
            tl = tr_row[0]
            sw = label_swapped(en_row[0], tl, gloss)
            if sw:
                add("label_swapped", row=en_row[0], col=en_head[0] if en_head else "", en=en_row[0], tr=tl,
                    expected=role, found=sw)
            years = year_words(locale, gloss)
            if role in ("mother", "father", "child", "girl", "boy", "adult") and gloss.get(role) and not sw:
                if gloss[role].casefold() not in tl.casefold():
                    nonglossary[(locale, "label:" + role, gloss[role], label_stem(tl, years))].append(handle)
            if re.search(r"\d\s*(?:-|to|–)?\s*\d*\s*years?\b", en_row[0], re.I) and role:
                leftover = unit_text(tl, role_terms)
                if not has_year_word(leftover, years):
                    nonglossary[(locale, "age_unit", "/".join(years[:3]), leftover)].append(handle)
            # stems for cross-role equality
            stem = label_stem(tl, year_words(locale, gloss))
            if role in ("mother", "father", "child") and stem:
                swap_stems[role].add(stem)
    # cross-role stem equality: mother/father/child rows sharing identical label stem
    stems = {r: s for r, s in swap_stems.items() if len(s) == 1}
    seen = {}
    for r, s in stems.items():
        k = next(iter(s))
        if k in seen and k:
            add("label_swapped", row="(table)", col="", en="%s vs %s" % (seen[k], r), tr=k,
                expected=r, found=seen[k])
        seen.setdefault(k, r)
    return F


def audit_product(handle, en_html, translations, locales, gloss_all, nonglossary, info, outdated):
    findings = []
    for loc in locales:
        tr = translations.get(loc)
        if not tr or not tr.get("value"):
            info["locale_missing"] += 1
            continue
        if tr.get("outdated"):
            outdated[loc] += 1
        pairs, n_en, n_tr = match_tables(en_html, tr["value"])
        if n_en and n_tr != len(parse_tables(en_html)):
            findings.append({"handle": handle, "locale": loc, "type": "table_count", "table": "",
                             "en": len(parse_tables(en_html)), "tr": n_tr})
        for pos, et, tt in pairs:
            findings.extend(audit_table(handle, loc, pos, et, tt, gloss_all[loc], nonglossary, info))
    return findings


# --------------------------------------------------------------------------- fetch
def _token():
    return json.loads(TOKEN_FILE.read_text())["access_token"]


def gql(query, variables=None, token=None):
    req = urllib.request.Request(ENDPOINT, json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 {"Content-Type": "application/json", "X-Shopify-Access-Token": token})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            if d.get("errors") and any("THROTTLED" in json.dumps(e) for e in d["errors"]):
                time.sleep(2 + attempt * 2)
                continue
            if d.get("errors"):
                raise RuntimeError("GraphQL errors: %s" % json.dumps(d["errors"])[:300])
            return d
        except Exception as exc:  # transient retry once-ish
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 2)


def fetch_products(locales, handles=None, page=8, pause=0.4, progress=True):
    token = _token()
    aliases = " ".join('t_%s: translations(locale:"%s"){key value outdated}' % (l.replace("-", "_"), l) for l in locales)
    q = ('query($c:String,$q:String){products(first:%d,after:$c,query:$q){pageInfo{hasNextPage endCursor} '
         'edges{node{handle status descriptionHtml %s}}}}' % (page, aliases))
    qs = "status:active"
    if handles:
        qs += " AND (" + " OR ".join("handle:%s" % h for h in handles) + ")"
    out, cur = [], None
    while True:
        d = gql(q, {"c": cur, "q": qs}, token)["data"]["products"]
        for e in d["edges"]:
            n = e["node"]
            if n["status"] != "ACTIVE":
                continue
            tr = {}
            for l in locales:
                for it in n.get("t_" + l.replace("-", "_")) or []:
                    if it["key"] == "body_html":
                        tr[l] = {"value": it["value"], "outdated": it.get("outdated")}
            out.append({"handle": n["handle"], "descriptionHtml": n["descriptionHtml"], "translations": tr})
        if progress:
            print("fetched %d products" % len(out), file=sys.stderr)
        if not d["pageInfo"]["hasNextPage"]:
            break
        cur = d["pageInfo"]["endCursor"]
        time.sleep(pause)
    return out


# --------------------------------------------------------------------------- report
SERIOUS = ("numeric_mismatch",)


def summarize(findings, nonglossary, info, outdated, n_products):
    by_type = Counter(f["type"] for f in findings)
    by_loc = defaultdict(Counter)
    for f in findings:
        by_loc[f["locale"]][f["type"]] += 1
    ng = defaultdict(list)
    for (loc, key, term, found), hs in nonglossary.items():
        ng[loc].append({"key": key, "glossary": term, "found": found, "count": len(hs),
                        "products": len(set(hs)), "example": sorted(set(hs))[:2]})
    for loc in ng:
        ng[loc].sort(key=lambda x: -x["count"])
    return {"products": n_products, "by_type": dict(by_type),
            "by_locale": {l: dict(c) for l, c in sorted(by_loc.items())},
            "nonglossary": {l: v for l, v in sorted(ng.items())},
            "info": dict(info), "outdated_by_locale": dict(outdated)}


def run(products, locales, gloss_all):
    nonglossary = defaultdict(list)
    info = Counter()
    outdated = Counter()
    findings = []
    for p in products:
        findings.extend(audit_product(p["handle"], p["descriptionHtml"], p["translations"], locales, gloss_all,
                                      nonglossary, info, outdated))
    return findings, nonglossary, info, outdated


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--handles", help="comma-separated product handles")
    ap.add_argument("--locales", help="comma-separated locales (default all 20)")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    ap.add_argument("--out", help="write the JSON result to this path")
    ap.add_argument("--input", help="read fetched products from this JSON cache instead of the Admin API")
    ap.add_argument("--save-input", help="save fetched products to this JSON cache")
    ap.add_argument("--fail-on-findings", action="store_true", help="exit 1 when any finding exists (not info)")
    ap.add_argument("--glossary", default=str(GLOSSARY))
    a = ap.parse_args(argv)
    locales = a.locales.split(",") if a.locales else LOCALES
    handles = a.handles.split(",") if a.handles else None
    gloss_all, applied = load_glossary(a.glossary)
    if a.input:
        products = json.loads(Path(a.input).read_text())
        if handles:
            products = [p for p in products if p["handle"] in handles]
    else:
        products = fetch_products(locales if not a.save_input else LOCALES, handles, progress=not a.json)
        if a.save_input:
            Path(a.save_input).write_text(json.dumps(products, ensure_ascii=False))
    findings, ng, info, outdated = run(products, locales, gloss_all)
    result = summarize(findings, ng, info, outdated, len(products))
    result["glossary_v25_applied_in_memory"] = applied
    result["findings"] = findings
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(result, ensure_ascii=False, indent=1))
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print("products=%d findings=%d" % (len(products), len(findings)))
        for t, n in sorted(result["by_type"].items(), key=lambda x: -x[1]):
            print("  %-24s %d" % (t, n))
        print("  info:", result["info"])
    return 1 if (a.fail_on_findings and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
