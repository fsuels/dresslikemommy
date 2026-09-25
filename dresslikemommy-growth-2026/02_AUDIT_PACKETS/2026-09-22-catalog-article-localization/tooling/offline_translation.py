#!/usr/bin/env python3
"""Offline cache reuse and independent structural checks. Never calls a provider/API.

Input baseline/candidate: {"rows": [{resourceId, locale, key, source,
sourceDigest, before, value?}]}. Shopify digests are opaque and never synthesized.
Exact cache reuse is a proposal, not a claim of semantic correctness.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata

DECIMAL_COMMA = set("cs da de el es fi fr it nl no pl pt ro ru sv".split())
NUMBER = re.compile(r"\d+(?:(?:[.,\u066b\u066c]\d+)|(?:[ \u00a0\u202f]\d{3}(?!\d)))*")
PLACEHOLDER = re.compile(r"QZXTOKEN|DLMTOKEN|__DLM[A-Z]*TOK\d", re.I)
LIQUID = re.compile(r"\{\{.*?\}\}|\{%.*?%\}", re.S)
URL = re.compile(r"https?://[^\s<>\"']+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
# Explicit equivalent units only; unknown localized units remain review findings.
UNIT_ALIASES = {
    "cm": ["cm", "centimeter", "centimeters", "centimetre", "centimetres", "centimetri", "centímetros", "centimetros", "сантиметр", "сантиметров", "см", "厘米", "センチメートル", "센티미터", "ס״מ", "ס\"מ", "سم", "सेमी"],
    "mm": ["mm", "millimeter", "millimeters", "millimetre", "millimetres", "мм", "毫米", "ミリメートル", "밀리미터"],
    "in": ["inch", "inches", "in", "pouce", "pouces", "Zoll", "pollice", "pollici", "pulgada", "pulgadas", "tommer", "tomme", "tum", "tuuma", "tuumaa", "cali", "cal", "polegadas", "polegada", "inci", "дюйм", "дюйма", "дюймы", "дюймов", "英寸", "インチ", "인치", "אינץ׳", "بوصة", "इंच"],
    "kg": ["kg", "kilogram", "kilograms", "кг", "公斤", "キログラム", "킬로그램", "ק״ג", "كغ", "किग्रा"],
    "lb": ["lb", "lbs", "pound", "pounds", "livre", "livres", "Pfund", "фунт", "фунтов", "磅", "ポンド", "파운드"],
    "%": ["%", "％", "٪", "percent", "procent", "pour cent", "prozent", "процент", "процентов"],
}


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digits(text):
    return "".join(str(unicodedata.decimal(c)) if c.isdecimal() else c for c in text)


def numbers(text, locale="en"):
    """Canonical values; grouping/decimal punctuation follows the supplied locale.

    Number order outside tables may change in translation; callers compare counts.
    Ambiguous punctuation, written-out numbers and unit conversions need review.
    """
    result = []
    for match in NUMBER.finditer(digits(text)):
        raw = match.group().replace(" ", "").replace("\u00a0", "").replace("\u202f", "")
        if "\u066b" in raw or "\u066c" in raw:
            raw = raw.replace("\u066c", "").replace("\u066b", ".")
        elif locale.split("-")[0] in DECIMAL_COMMA:
            if "," in raw:
                raw = raw.replace(".", "").replace(",", ".")
            elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", raw):
                raw = raw.replace(".", "")
        else:
            raw = raw.replace(",", "")
        prefix = text[:match.start()].rstrip()
        if prefix.endswith(("-", "−")) and not prefix[:-1].rstrip()[-1:].isdigit():
            raw = "-" + raw
        try:
            result.append(format(Decimal(raw).normalize(), "f"))
        except InvalidOperation:
            result.append("UNPARSED:" + match.group())
    return result


def units(text):
    result = Counter()
    for canonical, aliases in UNIT_ALIASES.items():
        # "in" is only a measurement beside a number or in a parenthetical header.
        candidates = sorted(aliases, key=len, reverse=True)
        pattern = r"(?<![^\W\d])(?:" + "|".join(re.escape(a) for a in candidates) + r")(?![^\W\d])"
        for match in re.finditer(pattern, text, re.I):
            if match.group().casefold() == "in" and not (
                re.search(r"\d\s*$", text[:match.start()])
                or (text[:match.start()].rstrip().endswith("(") and text[match.end():].lstrip().startswith(")"))
            ):
                continue
            result[canonical] += 1
    return result


class Shape(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.events, self.text, self.tables, self.raw = [], [], [], []
        self.table = self.cell = self.raw_tag = None
        self.nested_tables = False
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        self.events.append(("start", tag, sorted(attrs)))
        if tag in {"script", "style"}:
            self.raw_tag = tag
        if tag == "table":
            if self.table is not None:
                self.nested_tables = True
            self.table = {"attrs": sorted(attrs), "rows": []}
            self.tables.append(self.table)
        elif tag == "tr" and self.table is not None:
            self.table["rows"].append([])
        elif tag in {"td", "th"} and self.table is not None:
            if not self.table["rows"]:
                self.table["rows"].append([])
            self.cell = {"tag": tag, "attrs": sorted(attrs), "text": ""}
            self.table["rows"][-1].append(self.cell)

    def handle_startendtag(self, tag, attrs):
        self.events.append(("empty", tag, sorted(attrs)))

    def handle_endtag(self, tag):
        self.events.append(("end", tag))
        if tag in {"script", "style"}:
            self.raw_tag = None
        if tag in {"td", "th"}:
            self.cell = None
        if tag == "table":
            self.table = None

    def handle_data(self, text):
        if self.raw_tag:
            self.raw.append((self.raw_tag, text))
        else:
            self.text.append(text)
        if self.cell is not None:
            self.cell["text"] += text

    def handle_comment(self, text):
        self.events.append(("comment", text))


def table_facts(shape, locale):
    return [[[(cell["tag"], cell["attrs"], numbers(cell["text"], locale), units(cell["text"]),
               re.findall(r"(?<!\w)(?:XXXL|XXL|XXS|XL|XS|S|M|L)(?!\w)", cell["text"]))
              for cell in row] for row in table["rows"]] for table in shape.tables]


def verify_text(source, target, locale, fact_rules=()):
    errors, warnings = [], []
    if not isinstance(target, str) or not target.strip():
        return {"errors": ["empty_or_nonstring_value"], "warnings": [], "factsChecked": 0}
    a, b = Shape(source), Shape(target)
    if a.events != b.events:
        errors.append("html_structure_or_attributes_changed")
    if a.raw != b.raw:
        errors.append("script_or_style_content_changed")
    if a.nested_tables or b.nested_tables:
        errors.append("nested_tables_require_manual_review")
    if table_facts(a, "en") != table_facts(b, locale):
        errors.append("table_cell_numbers_units_or_shape_changed")
    av, bv = "\n".join(a.text), "\n".join(b.text)
    if Counter(numbers(av)) != Counter(numbers(bv, locale)):
        errors.append("numeric_values_changed")
    if units(av) != units(bv):
        errors.append("measurement_units_changed_or_unrecognized")
    if Counter(URL.findall(source)) != Counter(URL.findall(target)):
        errors.append("urls_or_emails_changed")
    if Counter(LIQUID.findall(source)) != Counter(LIQUID.findall(target)):
        errors.append("liquid_tokens_changed")
    if PLACEHOLDER.search(target):
        errors.append("translation_placeholder_residue")
    if source == target:
        warnings.append("source_equal_requires_language_review")
    checked = 0
    for fact in fact_rules:
        if fact.get("locale") != locale:
            continue
        count = source.count(fact["source"])
        if count:
            checked += 1
            if target.count(fact["target"]) != count:
                errors.append("explicit_fact_mismatch:" + fact.get("id", "unnamed"))
    warnings.append("semantic_equivalence_requires_independent_review")
    return {"errors": errors, "warnings": warnings, "factsChecked": checked}


def key(row):
    return row["resourceId"], row["locale"], row["key"]


def verify_rows(candidate, baseline, fact_rules=()):
    originals = {}
    for row in baseline:
        if key(row) in originals:
            raise ValueError("duplicate baseline key")
        originals[key(row)] = row
    reports, seen = [], set()
    for row in candidate:
        identity = key(row)
        errors = []
        if identity in seen:
            errors.append("duplicate_candidate_key")
        seen.add(identity)
        base = originals.get(identity)
        if base is None:
            errors.append("missing_baseline")
        else:
            for field in ["source", "sourceDigest", "before"]:
                if field not in row or field not in base or row[field] != base[field]:
                    errors.append("baseline_mismatch:" + field)
            if not row.get("sourceDigest"):
                errors.append("missing_opaque_shopify_source_digest")
        text = verify_text(row.get("source", ""), row.get("value"), row["locale"], fact_rules)
        reports.append({"resourceId": identity[0], "locale": identity[1], "key": identity[2],
                        "errors": errors + text["errors"], "warnings": text["warnings"],
                        "factsChecked": text["factsChecked"], "valueSHA256": sha(row.get("value") or "")})
    failed = sum(bool(r["errors"]) for r in reports)
    return {"status": "FAILED" if failed else "PASS_STRUCTURE_REQUIRES_MEANING_REVIEW",
            "rows": reports, "failedRows": failed, "checkedRows": len(reports),
            "baselineFreshness": "Supplied local snapshot only; no live freshness claim."}


def cache_index(paths):
    """No fallback, fuzzy matching, locale remapping, or cache writes."""
    index = defaultdict(lambda: defaultdict(list))
    for path in paths:
        raw = Path(path).read_bytes()
        data = json.loads(raw)
        file_sha = hashlib.sha256(raw).hexdigest()
        for locale, values in data.items():
            if not isinstance(values, dict):
                raise ValueError("cache must have locale -> exact source -> string|null schema")
            for source, value in values.items():
                if value is None:
                    continue
                if not isinstance(value, str):
                    raise ValueError("cache value is not string|null")
                if not value.strip() or PLACEHOLDER.search(value):
                    continue
                index[(locale, source)][value].append({"path": str(path), "fileSHA256": file_sha})
    return index


def reuse(baseline, paths):
    index = cache_index(paths)
    proposed, unresolved = [], []
    for row in baseline:
        values = index.get((row["locale"], row["source"]), {})
        if len(values) != 1:
            unresolved.append({"resourceId": row["resourceId"], "locale": row["locale"], "key": row["key"],
                               "reason": "CACHE_CONFLICT" if values else "CACHE_MISS", "variants": len(values)})
            continue
        value, provenance = next(iter(values.items()))
        proposed.append({**row, "value": value, "cacheProvenance": provenance,
                         "reviewStatus": "UNREVIEWED_CACHE_CANDIDATE"})
    return {"status": "OFFLINE_CANDIDATES_ONLY", "rows": proposed, "unresolved": unresolved,
            "verification": verify_rows(proposed, baseline)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["reuse", "verify"])
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate")
    parser.add_argument("--cache", nargs="*", default=[])
    parser.add_argument("--facts", help="Independently reviewed literal source/target fact rules JSON list")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    baseline = json.loads(Path(args.baseline).read_text())["rows"]
    if args.mode == "reuse":
        result = reuse(baseline, args.cache)
    else:
        if not args.candidate:
            parser.error("verify requires --candidate")
        candidate = json.loads(Path(args.candidate).read_text())["rows"]
        facts = json.loads(Path(args.facts).read_text()) if args.facts else []
        result = verify_rows(candidate, baseline, facts)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rows": len(result.get("rows", [])),
                      "output": args.output}))
    return 1 if result.get("failedRows", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
