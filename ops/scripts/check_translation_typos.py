#!/usr/bin/env python3
"""Mechanical typo check for translated product descriptions (read-only).

Added 2026-11-27 after Calidad V77: chained search/replace edits produced visible slips such as
"La camisa La camisa", "wie wie" and missing Czech commas. This script finds such slips in the
translated body_html of the given products. Admin GraphQL reads only; nothing is written.

Checks (tables are skipped; each text block is scanned on its own):
  repeat        a word or a group of 2-3 words repeated back to back ("wie wie", "La camisa La camisa")
  space-punct   space before , or . (and before ; : ! ? outside French)
  double-punct  ",,"  ".."  ",."  ".,"  (an ellipsis "..." is fine)
  comma-glued   comma directly followed by a letter ("rosa,blu")
  unbalanced    unclosed ( ) [ ] « » or quotes
  lower-start   sentence starting with a lowercase letter after . ! ?
  cs-comma      Czech: missing comma before která/který/aby/protože/přestože/že/když/zatímco/pokud/kde/což/takže/jenž
  cs-vocal      Czech: v/s/z/k not vocalised before safe clusters (ve vodě, ve sladěných, se sestrou, ze zlata, ke kapse)
  cs-spelling   Czech fixed spellings ("na plocho" -> "naplocho")
Image alt texts inside the body are scanned too (finding text starts with [alt]).

Examples:
  python3 ops/scripts/check_translation_typos.py --handles a-handle,b-handle --locales it,cs,de,es,fr
  python3 ops/scripts/check_translation_typos.py --handles-file ops/organic/receipts/x/selection.json --json
  python3 ops/scripts/check_translation_typos.py --handles-file handles.txt --fail-on-findings
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCALES = ["it", "cs", "de", "es", "fr"]

BLOCK_TAG = re.compile(r"</?(?:p|li|ul|ol|h[1-6]|div|br|tr|td|th|section|blockquote)\b[^>]*>", re.I)
ANY_TAG = re.compile(r"<[^>]+>")
TABLE = re.compile(r"<table\b.*?</table>", re.I | re.S)

# legitimate back-to-back repeats (lowercase); extend when a real case appears
REPEAT_ALLOW = {"sí sí", "no no", "ha ha", "pom pom", "bye bye", "cha cha", "tutu", "chi chi",
               # German pronoun/article pairs are grammatical ("mixen Sie sie", "das das Herz")
               "sie sie", "das das",
               # French reflexive and Czech "se" + preposition "se" are grammatical
               "vous vous", "nous nous", "se se", "die die", "der der", "den den", "dem dem"}
WORD = r"[^\W\d_]+"
REPEAT = re.compile(r"(?<![^\W\d_])(" + WORD + r"(?:\s+" + WORD + r"){0,2})\s+\1(?![^\W\d_])", re.I | re.U)
DOUBLE_PUNCT = re.compile(r",,|(?<!\.)\.\.(?!\.)|,\.|\.,(?!\d)")
COMMA_GLUED = re.compile(r",(?=[^\W\d_])", re.U)
LOWER_START = re.compile(r"(?<![.])([^\s.!?]{0,6})[.!?]\s+([^\W\d_])", re.U)
ABBREV = {"e.g", "i.e", "approx", "aprox", "env", "circa", "sig", "ca", "cca", "tzn", "např", "atd", "apod", "z", "b", "d", "h", "p", "ex",
          "etc", "ecc", "vs", "st", "sv", "č", "tj", "resp", "bzw", "usw", "inkl", "evtl", "ggf", "max", "min"}
CS_COMMA = re.compile(r"(?<=[^\W\d_])\s+(která|který|které|kterou|kterým|kterých|kteří|aby|abyste|protože|přestože|že|když|zatímco|pokud|kde|což|takže|jenž|jež)\b", re.U)
CS_NO_COMMA_BEFORE = {"a", "i", "ani", "nebo", "či", "tak", "jen", "ne", "než", "jako", "proto", "až", "zvlášť", "hlavně",
                      "právě", "teprve", "jakmile", "zatímco", "pokud", "tím", "to",
                      # a conjunction right after another one takes no comma ("takže pokud")
                      "takže", "protože", "přestože", "že", "aby", "když", "ale", "kde", "což",
                      # prepositions before a relative pronoun ("šaty, ve kterých")
                      "v", "ve", "na", "do", "s", "se", "z", "ze", "po", "pro", "o", "u", "k", "ke", "při", "bez",
                      "za", "od", "přes", "mezi", "nad", "pod", "před"}


ALT = re.compile(r"""\balt\s*=\s*(["'])(.*?)\1""", re.I | re.S)
CONS = "bcčdďfghjklmnňpqrřstťvwxzž"
SIB = "szšžSZŠŽ"
# Czech vocalised prepositions, conservative safe cases only (no "s černými": both forms occur)
CS_VOCAL = [
    (re.compile(r"(?<![^\W\d_])(?<!do )([vV])\s+(?=[vVfF][^\W\d_])", re.U), "ve"),
    (re.compile(r"(?<![^\W\d_])(?<!do )([vV])\s+(?=[%s][%s])" % (SIB, CONS), re.U), "ve"),
    (re.compile(r"(?<![^\W\d_])(?<!do )([vV])\s+(?=(?:čt|tř|dv|Čt|Tř|Dv))", re.U), "ve"),
    (re.compile(r"(?<![^\W\d_])([sS])\s+(?=[%s][^\W\d_])" % SIB, re.U), "se"),
    (re.compile(r"(?<![^\W\d_])([zZ])\s+(?=[%s][^\W\d_])" % SIB, re.U), "ze"),
    (re.compile(r"(?<![^\W\d_])([kK])\s+(?=[kKgG][^\W\d_])", re.U), "ke"),
]
CS_FIXED = [(re.compile(r"\bna plocho\b", re.I), "naplocho")]


def alt_texts(body: str) -> List[str]:
    """Image alt texts inside the body (scanned like text blocks)."""
    return [html_lib.unescape(m.group(2)).strip() for m in ALT.finditer(body or "") if m.group(2).strip()]


def text_blocks(body: str) -> List[str]:
    """Visible text of the body, split into blocks; tables removed."""
    s = TABLE.sub("\n", body or "")
    s = BLOCK_TAG.sub("\n", s)
    s = ANY_TAG.sub("", s)
    s = html_lib.unescape(s).replace(" ", " ")
    return [b.strip() for b in s.split("\n") if b.strip()]


def _snip(text: str, start: int, end: int) -> str:
    return text[max(0, start - 35):end + 35]


def scan_text(text: str, locale: str) -> List[Dict[str, str]]:
    """Findings for one block of plain text."""
    out: List[Dict[str, str]] = []
    for m in REPEAT.finditer(text):
        if ("%s %s" % (m.group(1), m.group(1))).lower() in REPEAT_ALLOW or len(m.group(1)) < 2:
            continue
        out.append({"check": "repeat", "text": _snip(text, m.start(), m.end())})
    punct = ",." if locale == "fr" else ",.;:!?"
    for m in re.finditer(r" ([%s])" % re.escape(punct), text):
        # " ..." ellipsis or " - " style dashes are not targeted; skip ellipsis
        if text[m.start(1):m.start(1) + 3] == "...":
            continue
        out.append({"check": "space-punct", "text": _snip(text, m.start(), m.end())})
    for m in DOUBLE_PUNCT.finditer(text):
        out.append({"check": "double-punct", "text": _snip(text, m.start(), m.end())})
    for m in COMMA_GLUED.finditer(text):
        out.append({"check": "comma-glued", "text": _snip(text, m.start(), m.end())})
    pairs = [("(", ")"), ("[", "]"), ("«", "»")]
    for a, b in pairs:
        if text.count(a) != text.count(b):
            out.append({"check": "unbalanced", "text": "%s%s: %s" % (a, b, text[:90])})
    if locale in ("cs", "de", "ro", "pl", "hu", "sk", "hr", "sl", "lt", "bg"):  # „…“ or „…”
        if text.count("„") != text.count("“") + text.count("”"):
            out.append({"check": "unbalanced", "text": "„“: %s" % text[:90]})
    elif text.count("“") != text.count("”"):
        out.append({"check": "unbalanced", "text": "“”: %s" % text[:90]})
    if text.count('"') % 2:
        out.append({"check": "unbalanced", "text": '": %s' % text[:90]})
    for m in LOWER_START.finditer(text):
        prev = m.group(1).lower().strip("(\"'“„«")
        raw_prev = m.group(1).strip("(\"'“„«")
        if prev in ABBREV or len(prev) == 1 or prev.isdigit() or (len(raw_prev) > 1 and raw_prev.isupper()):
            continue
        if m.group(2).islower():
            out.append({"check": "lower-start", "text": _snip(text, m.start(), m.end())})
    if locale == "cs":
        for m in CS_COMMA.finditer(text):
            before = re.findall(WORD, text[:m.start()])
            if before and before[-1].lower() in CS_NO_COMMA_BEFORE:
                continue
            out.append({"check": "cs-comma", "text": _snip(text, m.start(), m.end())})
    if locale == "cs":
        for rx, want in CS_VOCAL:
            for m in rx.finditer(text):
                out.append({"check": "cs-vocal", "text": "%s → %s: %s" % (m.group(1), want, _snip(text, m.start(), m.end() + 10))})
        for rx, want in CS_FIXED:
            for m in rx.finditer(text):
                out.append({"check": "cs-spelling", "text": "→ %s: %s" % (want, _snip(text, m.start(), m.end()))})
    return out


def scan_body(body: str, locale: str) -> List[Dict[str, str]]:
    found = []
    for b in text_blocks(body):
        found.extend(scan_text(b, locale))
    for a in alt_texts(body):
        for f in scan_text(a, locale):
            f["text"] = "[alt] " + f["text"]
            found.append(f)
    return found


def load_handles(args) -> List[str]:
    hs: List[str] = []
    if args.handles:
        hs += [h.strip() for h in args.handles.split(",") if h.strip()]
    for f in args.handles_file or []:
        p = Path(f)
        raw = p.read_text()
        if p.suffix == ".json":
            data = json.loads(raw)
            if isinstance(data, dict):
                data = data.get("handles") or data.get("products") or list(data.values())
            for x in data:
                hs.append(x["handle"] if isinstance(x, dict) else str(x))
        else:
            hs += [x.strip() for x in raw.split() if x.strip()]
    seen, res = set(), []
    for h in hs:
        if h not in seen:
            seen.add(h)
            res.append(h)
    return res


def fetch_bodies(admin, handle: str, locales: List[str]) -> Dict[str, str]:
    d = admin.gql('query($h:String!){productByHandle(handle:$h){id}}', {"h": handle})["productByHandle"]
    if not d:
        return {}
    al = " ".join('l%d:translations(locale:"%s"){key value}' % (i, l) for i, l in enumerate(locales))
    t = admin.gql('query($id:ID!){translatableResource(resourceId:$id){%s}}' % al, {"id": d["id"]})["translatableResource"]
    res = {}
    for i, l in enumerate(locales):
        for x in t["l%d" % i]:
            if x["key"] == "body_html" and x["value"]:
                res[l] = x["value"]
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--handles", default="")
    ap.add_argument("--handles-file", action="append")
    ap.add_argument("--locales", default=",".join(DEFAULT_LOCALES))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on-findings", action="store_true")
    args = ap.parse_args(argv)
    handles = load_handles(args)
    locales = [l.strip() for l in args.locales.split(",") if l.strip()]
    if not handles:
        ap.error("no handles given")
    sys.path.insert(0, str(ROOT / "ops" / "scripts"))
    import organic_engine as oe  # noqa: E402
    admin = oe.Admin()
    rows = []
    for h in handles:
        for loc, body in fetch_bodies(admin, h, locales).items():
            for f in scan_body(body, loc):
                rows.append({"handle": h, "locale": loc, **f})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        for r in rows:
            print("%s\t%s\t%s\t%s" % (r["handle"], r["locale"], r["check"], r["text"].replace("\n", " ")))
        print("findings: %d (products %d, locales %s)" % (len(rows), len(handles), ",".join(locales)))
    return 1 if (rows and args.fail_on_findings) else 0


if __name__ == "__main__":
    sys.exit(main())
