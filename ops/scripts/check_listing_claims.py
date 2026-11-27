#!/usr/bin/env python3
"""Scan ACTIVE Shopify products for unsupported claims and translation defects (read-only).

Dress Like Mommy is a dropshipping store: no stock, warehouse, bestseller, review, fabric-performance or
health claims we cannot prove, and no supplier notes in public copy. On 2026-11-26 three agents removed
such sentences from ~110 products by hand; this script keeps them from coming back.

Fields scanned: product title, descriptionHtml, SEO title, SEO description, and (optionally) their
translations (title, body_html, meta_title, meta_description). Admin GraphQL reads only; nothing is written.

Examples:
  python3 ops/scripts/check_listing_claims.py                                   # English, all ACTIVE
  python3 ops/scripts/check_listing_claims.py --since-hours 26 --all-locales --fail-on-findings
  python3 ops/scripts/check_listing_claims.py --handles some-handle --locales es,de --json
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

API_VERSION = "2026-10"
BRAND = "Dress Like Mommy"
SNIPPET_MAX = 80

# ---------------------------------------------------------------------------------------------
# English rules. (category, rule_id, regex, reason, also_check_in_translations)
# "also_check_in_translations" marks unambiguous multi-word English terms; if one survives in a
# translated field the translator left an English claim in place.
# ---------------------------------------------------------------------------------------------
_RULES_SRC: List[Tuple[str, str, str, str, bool]] = [
    # popularity
    ("popularity", "bestseller", r"\bbest[- ]?sell(?:er|ers|ing)\b|\btop[- ]sell(?:er|ers|ing)\b|\bhot[- ]sell(?:er|ers|ing)\b",
     "popularity claim with no sales data", True),
    ("popularity", "most-popular", r"\bmost[- ]popular\b|\bvery popular\b|\bpopular (?:choice|pick|style|design|set|item)s?\b|\bpopular with\b",
     "popularity claim with no sales data", True),
    ("popularity", "trending", r"\btrending\b|\bviral\b", "popularity claim with no data", False),
    ("popularity", "customer-favorite", r"\b(?:customer|fan|crowd|shopper)[- ]favou?rites?\b|\bbest[- ]loved\b|\b(?:loved|adored|trusted) by\b|\bcustomers? (?:love|adore)\b|\bproven favou?rites?\b|\btop[- ]rated\b|\b#\s?1\b|\bnumber (?:one|1)\b",
     "popularity claim with no review data", True),
    # stock / shipping / location
    ("stock_shipping", "in-stock", r"\bin[- ]stock\b|\bready to ship\b|\blimited stock\b|\bwhile supplies last\b|\bonly \d+ (?:left|remaining)\b|\bselling (?:out|fast)\b|\bsells? out\b",
     "stock claim; dropshipping holds no inventory", True),
    ("stock_shipping", "ships-today", r"\bships? (?:today|same[- ]day|within \d+ ?(?:hours?|h)|in \d+ ?(?:hours?|h)|fast|quickly|free)\b|\bships? from (?:the )?(?:US|USA|U\.S\.A?\.?|United States|our)\b",
     "shipping-speed or origin claim not backed by the policy", True),
    ("stock_shipping", "fast-shipping", r"\b(?:fast|express|rapid|expedited|speedy|same[- ]day|next[- ]day|2[- ]day|overnight) (?:shipping|delivery|dispatch)\b|\bnext[- ]day\b|\bguaranteed (?:delivery|arrival)\b|\barrives? (?:by|in \d)\b",
     "delivery-speed or arrival promise", True),
    ("stock_shipping", "warehouse-store", r"\bwarehouse\b|\bvisit (?:us|our (?:store|shop|boutique|showroom))\b|\b(?:retail|physical|brick[- ]and[- ]mortar) (?:store|shop|location)s?\b|\blocally (?:stocked|made)\b|\bmade in (?:the )?(?:USA|US|U\.S\.A?\.?)\b|\bon[- ]hand\b",
     "implies store, warehouse or owned inventory", True),
    # performance / material
    ("performance", "quick-dry", r"\bquick[- ]?dr(?:y|ies|ying)\b|\bfast[- ]dr(?:y|ies|ying)\b|\bdr(?:y|ies) (?:quickly|fast)\b|\bspeedy drying\b",
     "unsupported performance claim", True),
    ("performance", "uv-upf", r"\bUPF\b|\bSPF\b|\bUV[- ]?(?:protect\w*|block\w*|resist\w*|rays?|shield\w*)\b|\bsun[- ]?(?:protect\w*|block\w*)\b",
     "unsupported UV/sun-protection claim", False),
    ("performance", "hypoallergenic", r"\bhypo[- ]?allergenic\b|\banti[- ]?(?:bacterial|microbial|allergy)\b|\bodou?r[- ](?:control|resistant|free)\b",
     "unsupported health/hygiene claim", True),
    ("performance", "organic-eco", r"\borganic\b|\beco[- ]?(?:friendly|conscious|safe)\b|\bsustainabl\w+\b|\benvironmentally\b|\bbiodegradable\b|\bplanet[- ]friendly\b|\bgreen (?:fabric|material)\b",
     "unsupported organic/eco claim", False),
    ("performance", "premium-luxury", r"\bpremium\b|\bluxur(?:y|ious)\b|\btop[- ]?(?:notch|tier)\b|\bsuperior (?:quality|fabric|material|craft\w*)\b|\bbest quality\b|\bfinest\b|\bhigh[- ]end\b|\bupscale\b|\bboutique[- ]quality\b",
     "unsupported quality tier claim", False),
    ("performance", "high-quality", r"\bhigh[- ]?quality\b|\btop[- ]?quality\b", "unsupported quality claim", True),
    ("performance", "wrinkle", r"\bwrinkle[- ]?(?:free|resist\w*|proof)\b|\bno[- ]iron\b|\biron[- ]free\b|\b(?:barely|rarely|never) wrinkl\w+\b|\bwrinkles? (?:low|gentle|less)\b|\bkeeps? wrinkles\b|\bresists? wrinkl\w+\b",
     "unsupported wrinkle claim", True),
    ("performance", "resistance", r"\b(?:shrink(?:age)?|fad(?:e|ing)|pill(?:ing)?|chlorine|stain|tear|rip|snag|odou?r|colou?r)[- ]?(?:resist\w*|proof|free)\b|\bresists? (?:shrink\w*|fad\w*|pilling|chlorine|stains?|wrinkl\w+|tears?|cling\w*)\b|\bcolou?r[- ]?fast\b|\bnon[- ]?fading\b|\bwon'?t (?:shrink|fade|pill|stretch out)\b|\bno (?:shrinking|fading|pilling)\b|\bchlorine\b",
     "unsupported resistance claim", True),
    ("performance", "waterproof", r"\bwaterproof\b|\bwater[- ](?:resistant|repellent|proof)\b|\bsplash[- ]proof\b",
     "unsupported waterproofing claim", False),
    ("performance", "wicking", r"\bmoisture[- ]?wick\w*|\bsweat[- ]?(?:wick\w*|proof|absorb\w*)|\bwicks? (?:away|moisture|sweat)\b|\bcooling (?:fabric|technology|effect)\b|\bthermal (?:regulat\w+|insulat\w+)\b",
     "unsupported technical-fabric claim", True),
    ("performance", "perfect-fit", r"\bperfect(?:ly)?[- ]fit\w*\b|\bensures? (?:a |the |you (?:get )?a )?(?:perfect |great |proper |right |comfortable )?fit\b|\bguarantee[sd]?\b|\bguarantees? (?:a )?fit\b|\bfits? (?:true|perfectly)\b|\btrue[- ]to[- ]size\b|\bflawless(?:ly)? fit\b|\bfit(?:s)? like a glove\b",
     "fit or outcome guarantee", True),
    ("performance", "ensures", r"\bensur(?:e|es|ed|ing)\b", "outcome guarantee ('ensures comfort/fit')", False),
    ("performance", "body-type-claim", r"\b(?:all|every|any) body (?:types?|shapes?)\b|\bbody types? and sizes\b|\bvisual(?:ly)? slimming\b|\bslimming (?:effect|look)\b|\bpromises? (?:a |an |the )?(?:\w+ )?fit\b", "fit-for-every-body or slimming claim", False),
    ("performance", "long-lasting", r"\blong[- ]?lasting\b|\bbuilt to last\b|\bdurab\w+\b|\bheavy[- ]duty\b|\bwill last\b|\blasts? (?:for )?(?:years|seasons)\b|\bwear(?:s)? (?:for )?years\b|\bstands? up to\b|\bwithstands?\b",
     "unsupported durability claim", True),
    ("performance", "certification", r"\bOEKO[- ]?TEX\b|\bGOTS\b|\bcertifi\w+\b|\bCPSIA\b|\bASTM\b|\bCE[- ]mark\w*\b|\bFDA\b|\bREACH[- ]compliant\b|\btested (?:for|by)\b|\bsafety[- ](?:tested|approved|certified)\b|\bflame[- ]?(?:retardant|resistant)\b",
     "certification or testing claim we cannot document", True),
    ("performance", "fabric-behavior", r"\b(?:gets?|get|grows?|becomes?) (?:even )?(?:softer|cozier|better|smoother)\b|\bsoftens? (?:with|every|after|over)\b|\b(?:wash after wash|with every (?:wash|cycle|use)|every (?:wash|cycle))\b|\b(?:keeps?|holds?|retains?|maintains?) (?:its|their|the) (?:shape|colou?r|softness)\b|\bpre-?washed\b|\bnever scratch\w*\b|\bkeeps? (?:air|airflow)\b|\b(?:breathes|breathe) (?:through|in|all)\b",
     "unsupported fabric-behavior claim", False),
    # health / skin
    ("health_skin", "gentle-skin", r"\bgentle (?:on|against|to|for)\b[^.;:]{0,25}\b(?:skin|cheeks)\b|\bskin[- ]friendly\b|\bdermatolog\w*\b|\bpediatric\w*\b|\bnon[- ]?toxic\b|\bchemical[- ]free\b|\bsafe for (?:baby|babies|infants?|newborns?|sensitive)\b|\beczema\b|\birritation[- ]free\b|\bno irritation\b|\bsensitive skin\b",
     "skin/health claim", True),
    # handmade / craft
    ("craft", "handmade", r"\bhand[- ]?(?:painted|made|crafted|knit(?:ted)?|sewn|stitched|embroider\w*|woven|dyed)\b|\bhandcrafted\b|\bartisan(?:al)?\b",
     "craft/process claim we cannot verify for a sourced item", True),
    # reviews
    ("reviews", "stars", r"\b[45][- ]stars?\b|\bfive[- ]stars?\b|\b\d(?:\.\d)?\s?/\s?5\b(?: stars?)?|\brave reviews?\b|\bthousands of (?:happy|satisfied|moms|mothers|mamas|families|customers|reviews)\b|\b\d[\d,]*\+? (?:happy|satisfied) (?:customers|families|moms)\b|\b(?:customers|reviewers|buyers|moms) (?:say|rave|report|agree)\b|\bverified (?:buyer|purchase|review)s?\b|\bmoney[- ]back\b|\bsatisfaction[- ]guarantee\w*\b|\bhappiness guarantee\b",
     "review/satisfaction claim; store has almost no reviews", True),
    # internal-note leaks
    ("internal_leak", "internal-note", r"\bmeasurements? (?:are |is )?(?:currently )?(?:unavailable|not available|n/?a|missing|tbd)\b|\bsuppliers?\b|\bfactory\b|\bdrop[- ]?ship\w*\b|(?-i:\bTODO\b)|(?-i:\bTBD\b)|(?-i:\bFIXME\b)|\blorem ipsum\b|\bplaceholder\b|\b1688\b|\bbuckydrop\b|\btaobao\b|\btmall\b|\balibaba\b|\baliexpress\b|\bshein\b|\bcny\b|\brmb\b|\bsee (?:the )?supplier\b|\bper (?:the )?supplier\b|\bchatgpt\b|\bAI[- ]generated\b",
     "internal note, supplier or tooling leaked into public copy", True),
]

# Allowlist: harmless contexts. A finding is dropped when an allowlist regex matches the sentence and its
# span overlaps the finding span (so one allowed phrase cannot hide a different claim in the same sentence).
ALLOW_SRC: List[str] = [
    r"\b(?:is|are|isn'?t|aren'?t|not|nor|never|no)\s+(?:a\s+)?guarantee[sd]?\b",
    r"\bcannot guarantee\b|\bcan'?t guarantee\b|\bdo(?:es)? not guarantee\b|\bdon'?t guarantee\b|\bno guarantee\b",
    r"\bnot guaranteed\b|\bestimates? (?:are|is) not (?:a )?guarantee\w*\b",
    r"\borganic\s+(?:shapes?|silhouettes?|patterns?|prints?|lines?|curves?|textures?|forms?)\b",
    r"\bUV\s+print\w*\b",
    r"\bmeasurements? (?:may|can|will) vary\b",
    # honest made-to-order lead time (maternity gowns): "sewn after you order and is ready to ship in about 7 days"
    r"\bready to ship in (?:about |approximately |around )?\d+(?:\s?-\s?\d+)? (?:business |working )?days\b",
    r"\bruns? (?:closer to |close to )?true[- ]to[- ]size\b",
]

_FLAGS = re.IGNORECASE


class Rule:
    __slots__ = ("category", "rule_id", "regex", "reason", "xl")

    def __init__(self, category: str, rule_id: str, pattern: str, reason: str, xl: bool):
        self.category, self.rule_id, self.reason, self.xl = category, rule_id, reason, xl
        # "#1" and "\b" mix badly; patterns are written to be safe either way.
        self.regex = re.compile(pattern, _FLAGS)


RULES: List[Rule] = [Rule(*row) for row in _RULES_SRC]
ALLOW: List["re.Pattern[str]"] = [re.compile(p, _FLAGS) for p in ALLOW_SRC]

# Per-language claim terms (translations of the highest-value claim words). Short and precise on purpose.
LANG_TERMS_SRC: Dict[str, List[Tuple[str, str]]] = {
    "es": [("popularity", r"\bm[aá]s vendid[oa]s?\b|\bm[aá]s popular(?:es)?\b|\bfavorit[oa]s? de los clientes\b"),
           ("performance", r"\bsecado r[aá]pido\b|\bhipoalerg[eé]nic\w+\b|\bajuste perfecto\b|\balta calidad\b|\bcalidad (?:premium|superior)\b|\bgarantiza\w*\b|\bgarantizad[oa]\w*\b|\bsin arrugas\b|\bimpermeable\b")],
    "de": [("popularity", r"\bbestseller\w*\b|\bverkaufsschlager\b|\bam (?:meisten|besten) verkauft\w*\b|\bbeliebteste\w*\b|\bkundenliebling\w*\b"),
           ("performance", r"\bschnell(?:trocknend\w*|[- ]trocknend\w*)\b|\bschnelltrocknend\w*\b|\bhypoallergen\w*\b|\bperfekte passform\b|\bhochwertig\w*\b|\bpremium\w*\b|\bgarantiert\w*\b|\bfaltenfrei\w*\b|\bwasserdicht\w*\b")],
    "fr": [("popularity", r"\bmeilleures? ventes?\b|\bbest[- ]?sellers?\b|\ble plus populaire\b|\bles plus populaires\b|\bpréféré des clients\b|\bchouchou\b"),
           ("performance", r"\bs[ée]chage rapide\b|\bhypoallerg[ée]nique\w*\b|\bcoupe parfaite\b|\bhaute qualit[ée]\b|\bqualit[ée] (?:premium|sup[ée]rieure)\b|\bgarantit\w*\b|\bgaranti[es]?\b|\binfroissable\w*\b|\bimperm[ée]able\w*\b")],
    "it": [("popularity", r"\bpi[uù] venduto\w*\b|\bpi[uù] popolar\w*\b|\bbest[- ]?seller\w*\b|\bpreferito dai clienti\b"),
           ("performance", r"\basciugatura rapida\b|\bipoallergenic\w*\b|\bvestibilit[aà] perfetta\b|\balta qualit[aà]\b|\bqualit[aà] (?:premium|superiore)\b|\bgarantisce\w*\b|\bgarantit[oa]\b|\banti[- ]?piega\b|\bimpermeabile\b")],
    "cs": [("popularity", r"\bnejprod[aá]van\w*\b|\bnejobl[ií]ben\w*\b|\bbestseller\w*\b"),
           ("performance", r"\brychleschnouc\w*\b|\bhypoalergenn\w*\b|\bdokonal\w* padnut\w*\b|\bvysok\w* kvalit\w*\b|\bvysoce kvalitn\w*\b|\bprémiov\w*\b|\bzaru[cč]uje\w*\b|\bzaji[sš]t['’]?uj\w*\b|\bzajišťuj\w*\b|\bperfektn[ií] (?:st[rř]ih|padnut[ií]|fit)\b|\bgarantuje\w*\b|\bnemačkav\w*\b|\bvodot[eě]sn\w*\b")],
    "pl": [("popularity", r"\bbestseller\w*\b|\bnajpopularniejsz\w*\b|\bnajczęściej kupowan\w*\b|\bulubion\w* przez klient\w*\b"),
           ("performance", r"\bszybkoschn\w*\b|\bhipoalergiczn\w*\b|\bidealne dopasowanie\b|\bwysokiej jako[sś]ci\b|\bwysokiej klasy\b|\bpremium\b|\bgwarantuj\w*\b|\bnie gniecie\b|\bwodoodporn\w*\b")],
    "nl": [("popularity", r"\bbestseller\w*\b|\bmeest verkochte\b|\bmeest populaire\b|\bklantfavoriet\w*\b"),
           ("performance", r"\bsnel[- ]?drogend\w*\b|\bhypoallergeen\b|\bperfecte (?:pasvorm|fit)\b|\bhoogwaardig\w*\b|\bpremium\w*\b|\bgarandeert\w*\b|\bkreukvrij\w*\b|\bwaterdicht\w*\b")],
    "pt-BR": [("popularity", r"\bmais vendid\w*\b|\bmais popular\w*\b|\bbest[- ]?seller\w*\b|\bfavorit\w* dos clientes\b"),
              ("performance", r"\bsecagem r[aá]pida\b|\bhipoalerg[eê]nic\w*\b|\bcaimento perfeito\b|\balta qualidade\b|\bqualidade (?:premium|superior)\b|\bgarante\b|\bgarantid\w*\b|\bantiamassa\w*\b|\bimperme[aá]vel\b")],
}
LANG_TERMS: Dict[str, List[Tuple[str, "re.Pattern[str]"]]] = {
    lang: [(cat, re.compile(pat, _FLAGS)) for cat, pat in rows] for lang, rows in LANG_TERMS_SRC.items()
}
LANG_ALLOW = [  # same "not guaranteed" idea in the eight languages
    re.compile(p, _FLAGS) for p in (
        r"\bno (?:se )?garantiza\w*\b|\bnicht garantiert\b|\bkeine garantie\b|\bne (?:garantit|sont pas garanti\w*)\b|\bnon (?:garantit\w*|[eè] garantit\w*)\b",
        r"\bnen[ií] zaru[cč]en\w*\b|\bnie gwarantuj\w*\b|\bniet gegarandeerd\b|\bn[aã]o (?:garante|[eé] garantid\w*)\b",
    )
]

# ---------------------------------------------------------------------------------------------
# URL / vendor-host handling
# ---------------------------------------------------------------------------------------------
URL_RE = re.compile(r"(?:https?://|//|www\.)[^\s\"'<>)\]]+", re.I)
BARE_HOST_RE = re.compile(
    r"\b(?:[a-z0-9-]+\.)+(?:com|cn|net|org|co|top|shop|xyz|site|store|ru|hk)\b(?:/[^\s\"'<>)\]]*)?", re.I)
VENDOR_HOST_RE = re.compile(
    r"(?:^|\.)(?:1688|alibaba|alicdn|taobao|tmall|aliexpress|buckydrop|temu|shein|dhgate|yunexpress|yiwu\w*|made-in-china)\.", re.I)
ALLOWED_HOSTS = ("dresslikemommy.com", "shopify.com", "myshopify.com", "shopifycdn.com", "schema.org", "w3.org",
                 "youtube.com", "youtu.be", "pinterest.com", "instagram.com", "facebook.com", "tiktok.com")


def host_of(url: str) -> str:
    u = re.sub(r"^(?:https?:)?//", "", url.strip(), flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return re.split(r"[/?#:]", u, maxsplit=1)[0].lower().strip(".")


def mask_host(host: str) -> str:
    """1688.com -> 1***.com : never echo a supplier host in full."""
    if not host:
        return "***"
    dot = host.rfind(".")
    tld = host[dot:] if dot > 0 else ""
    return host[0] + "***" + tld


def host_allowed(host: str) -> bool:
    return any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS)


def find_urls(text: str) -> List[Tuple[str, int, int]]:
    """Return (masked_host, start, end) for each non-allowed URL or bare host in plain text or raw HTML."""
    found: List[Tuple[str, int, int]] = []
    seen: List[Tuple[int, int]] = []
    for rx in (URL_RE, BARE_HOST_RE):
        for m in rx.finditer(text):
            if any(m.start() < e and s < m.end() for s, e in seen):
                continue
            host = host_of(m.group(0))
            if not host or "." not in host:
                continue
            if host_allowed(host):
                continue
            if rx is BARE_HOST_RE and not VENDOR_HOST_RE.search(host):
                # a bare "word.com" in prose is only interesting when it is a known vendor host
                continue
            seen.append((m.start(), m.end()))
            found.append((mask_host(host), m.start(), m.end()))
    return found


# ---------------------------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------------------------
_BLOCK_CLOSE = re.compile(r"</(?:li|p|h[1-6]|div|tr|td|th|ul|ol|table|blockquote|section)\s*>|<br\s*/?>|<hr\s*/?>", re.I)
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t ​‌‍﻿]+")
_SENT = re.compile(r"(?<=[.!?])\s+")


def clean_text(s: str) -> str:
    s = html_lib.unescape(s or "")
    return _WS.sub(" ", s).strip()


def html_to_elements(raw: str) -> List[str]:
    """Visible text of an HTML fragment, one entry per block element (li, p, heading, table cell)."""
    if not raw:
        return []
    marked = _BLOCK_CLOSE.sub("\n", raw)
    marked = re.sub(r"<(?:script|style)\b.*?</(?:script|style)>", " ", marked, flags=re.S | re.I)
    marked = _TAG.sub("", marked)
    return [t for t in (clean_text(line) for line in marked.split("\n")) if t]


def li_items(raw: str) -> List[str]:
    return [clean_text(_TAG.sub("", m)) for m in re.findall(r"<li\b[^>]*>(.*?)</li\s*>", raw or "", flags=re.S | re.I)]


def sentences(element: str) -> List[Tuple[str, int]]:
    out, pos = [], 0
    for part in _SENT.split(element):
        i = element.find(part, pos)
        i = pos if i < 0 else i
        out.append((part, i))
        pos = i + len(part)
    return out


def snippet(sentence: str, start: int, end: int, limit: int = SNIPPET_MAX) -> str:
    """Matched text with a little context, at most `limit` characters."""
    if len(sentence) <= limit:
        return sentence
    span = end - start
    if span >= limit - 2:
        return sentence[start:start + limit - 1] + "…"
    room = limit - span
    lo = max(0, start - room // 2)
    hi = min(len(sentence), lo + limit)
    lo = max(0, hi - limit)
    return ("…" if lo > 0 else "") + sentence[lo:hi].strip() + ("…" if hi < len(sentence) else "")


def _allowed(sentence: str, start: int, end: int, allow: Sequence["re.Pattern[str]"]) -> bool:
    for rx in allow:
        for m in rx.finditer(sentence):
            if m.start() < end and start < m.end():
                return True
    return False


def _finding(category: str, rule: str, reason: str, match: str, snip: str) -> Dict[str, str]:
    return {"category": category, "rule": rule, "reason": reason, "match": match[:SNIPPET_MAX], "snippet": snip}


def _mask_urls_in(text: str) -> str:
    out, last = [], 0
    for masked, s, e in find_urls(text):
        out.append(text[last:s])
        out.append("<" + masked + ">")
        last = e
    out.append(text[last:])
    return "".join(out)


# ---------------------------------------------------------------------------------------------
# Scanners (pure; tested on fixture strings)
# ---------------------------------------------------------------------------------------------
def scan_elements(elements: Iterable[str], rules: Sequence[Rule] = RULES,
                  allow: Sequence["re.Pattern[str]"] = ALLOW, xl_only: bool = False) -> List[Dict[str, str]]:
    """Apply the English rule set to text elements. xl_only keeps only translation-safe multi-word terms."""
    findings: List[Dict[str, str]] = []
    seen = set()
    for element in elements:
        for sent, _ in sentences(element):
            for rule in rules:
                if xl_only and not rule.xl:
                    continue
                for m in rule.regex.finditer(sent):
                    if _allowed(sent, m.start(), m.end(), allow):
                        continue
                    key = (rule.category, rule.rule_id, m.group(0).lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(_finding(rule.category, rule.rule_id, rule.reason, m.group(0),
                                             _mask_urls_in(snippet(sent, m.start(), m.end()))))
    return findings


def scan_english_field(value: str, is_html: bool) -> List[Dict[str, str]]:
    value = value or ""
    elements = html_to_elements(value) if is_html else ([clean_text(value)] if value.strip() else [])
    findings = scan_elements(elements)
    findings.extend(scan_urls(value, elements))
    return _dedupe(findings)


def scan_urls(raw: str, elements: Sequence[str]) -> List[Dict[str, str]]:
    """Vendor hosts and any non-allowed URL, in visible text and in raw HTML (href/src)."""
    out: List[Dict[str, str]] = []
    seen = set()
    for text in list(elements) + [raw or ""]:
        for masked, s, e in find_urls(text):
            if masked in seen:
                continue
            seen.add(masked)
            vendor = bool(VENDOR_HOST_RE.search(host_of(text[s:e])))
            out.append(_finding("internal_leak", "vendor-host" if vendor else "external-url",
                                "supplier/vendor host in public copy" if vendor else "external URL in product copy",
                                masked, "URL host " + masked))
    return out


GLUED_LATIN_RE = re.compile(r"(?<![^\W_])(?!IJ)([A-Z])([A-Z][a-zà-ɏ]{3,})\b")
_NONLATIN = (r"[Ѐ-ӿ֐-׿؀-ۿ฀-๿ऀ-ॿ가-힯]")
GLUED_NONLATIN_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z])(?=" + _NONLATIN + ")")
GLUED_OK_FIRST = set("TVAUOXYSMLD")  # T-shirt, V-neck, A-line, U-neck, size letters
NO_GLUE_NONLATIN = {"zh-CN", "zh-TW", "ja"}  # T恤, V领, S码 are legitimate there
GLUED_WORD_ALLOW = {"UVschutz", "PDFs"}


def scan_glued_letter(text: str, locale: str) -> List[Dict[str, str]]:
    out = []
    for sent, _ in sentences(text):
        for m in GLUED_LATIN_RE.finditer(sent):
            word = m.group(0)
            if word in GLUED_WORD_ALLOW:
                continue
            out.append(_finding("translation_defect", "glued-letter", "stray Latin capital glued before a word",
                                word, snippet(sent, m.start(), m.end())))
        if locale not in NO_GLUE_NONLATIN:
            for m in GLUED_NONLATIN_RE.finditer(sent):
                if m.group(1) in GLUED_OK_FIRST:
                    continue
                out.append(_finding("translation_defect", "glued-letter", "stray Latin capital glued before a word",
                                    sent[m.start():m.end() + 3], snippet(sent, m.start(), m.end() + 3)))
    return _dedupe(out)


NO_SPACE_SCRIPT_LOCALES = {"zh-CN", "zh-TW", "ja", "th", "ko", "ar", "he", "hi"}
_LAST_WORD = re.compile(r"([^\W\d_]+)\.$")
_WORD = re.compile(r"[^\W\d_]+")


def build_vocab(texts: Iterable[str]) -> "Counter[str]":
    """Lower-cased whole-word counts of one locale's translated copy (used to tell cut-off words from short words)."""
    vocab: "Counter[str]" = Counter()
    for t in texts:
        vocab.update(w.lower() for w in _WORD.findall(t))
    return vocab


def scan_truncated_items(en_html: str, tr_html: str, locale: str, vocab: Optional["Counter[str]"] = None) -> List[Dict[str, str]]:
    """A translated list item ending in a cut-off word + '.' where the English item ends in a full word.

    Signals, all required: both bodies have the same number of <li> items (aligned); the English item ends in
    a word of 6+ letters; the translated item ends in a 2-5 letter word; and, using the locale vocabulary,
    that word is unique as a whole word (1 use) while a longer word starting with it exists. Without a
    vocabulary nothing is flagged (a short last word is usually just a short word). Skipped for scripts
    where short final words are normal.
    """
    if locale in NO_SPACE_SCRIPT_LOCALES or not vocab:
        return []
    en_items, tr_items = li_items(en_html), li_items(tr_html)
    if not en_items or len(en_items) != len(tr_items):
        return []
    out = []
    for en_item, tr_item in zip(en_items, tr_items):
        m = _LAST_WORD.search(tr_item)
        if not m or len(tr_item.split()) < 3:
            continue
        last = m.group(1)
        if not (2 <= len(last) <= 5):
            continue
        en_words = _WORD.findall(en_item)
        if not en_words or len(en_words[-1]) < 6:
            continue
        low = last.lower()
        if vocab.get(low, 0) > 1:
            continue
        if not any(w != low and w.startswith(low) and len(low) + 2 <= len(w) <= len(low) + 5 and vocab[w] >= 5 for w in vocab):
            continue
        out.append(_finding("translation_defect", "truncated-item",
                            "list item ends in a cut-off word", last + ".",
                            snippet(tr_item, len(tr_item) - len(last) - 1, len(tr_item))))
    return _dedupe(out)


BRAND_VARIANT_RE = re.compile(r"\bdress[\s-]*like[\s-]*(?:a[\s-]*)?(?:mom\w*|mum\w*|mama\w*|mam\w*|mother\w*)\b|\bdresslikemommy\b", re.I)
_LATIN_RE = re.compile(r"[A-Za-z]")


def scan_brand(en_text: str, tr_text: str, locale: str) -> List[Dict[str, str]]:
    out = []
    for m in BRAND_VARIANT_RE.finditer(tr_text):
        found = m.group(0)
        after = tr_text[m.end():m.end() + 4].lower()
        if found == BRAND or after.startswith((".com", ".co")) or found.lower() == "dresslikemommy":
            continue
        out.append(_finding("translation_defect", "brand-altered", 'brand "' + BRAND + '" altered', found,
                            snippet(tr_text, m.start(), m.end())))
    if (BRAND.lower() in (en_text or "").lower() and BRAND not in tr_text and not out
            and locale not in NO_SPACE_SCRIPT_LOCALES and _LATIN_RE.search(tr_text)):
        out.append(_finding("translation_defect", "brand-altered", 'brand "' + BRAND + '" missing in translation',
                            "(missing)", snippet(tr_text, 0, 0)))
    return _dedupe(out)


def scan_lang_terms(elements: Iterable[str], locale: str) -> List[Dict[str, str]]:
    base = locale if locale in LANG_TERMS else locale.split("-")[0]
    terms = LANG_TERMS.get(base) or LANG_TERMS.get(locale) or []
    out = []
    for element in elements:
        for sent, _ in sentences(element):
            for cat, rx in terms:
                for m in rx.finditer(sent):
                    if _allowed(sent, m.start(), m.end(), LANG_ALLOW):
                        continue
                    out.append(_finding("translated_claim", cat, "claim wording in translation (" + base + ")",
                                        m.group(0), snippet(sent, m.start(), m.end())))
    return _dedupe(out)


SIZE_CHART_ID_RE = re.compile(r"<table\b[^>]*?\sid\s*=\s*[\"']([^\"']*size-chart[^\"']*)[\"']", re.I)


def scan_table_ids(en_html: str, tr_html: str) -> List[Dict[str, str]]:
    """A translated body that lost an English size-chart table id (translated or dropped): the page no longer
    recognises the chart."""
    kept = set(SIZE_CHART_ID_RE.findall(tr_html or ""))
    return [_finding("translation_defect", "table-id", "size-chart table id differs from English", table_id, "")
            for table_id in sorted(set(SIZE_CHART_ID_RE.findall(en_html or "")) - kept)]


def scan_translation_field(locale: str, key: str, value: str, en_value: str = "",
                           vocab: Optional["Counter[str]"] = None) -> List[Dict[str, str]]:
    is_html = key == "body_html"
    value = value or ""
    elements = html_to_elements(value) if is_html else ([clean_text(value)] if value.strip() else [])
    findings: List[Dict[str, str]] = []
    findings.extend(scan_urls(value, elements))
    for f in scan_elements(elements, xl_only=True):
        f = dict(f)
        f["category"], f["reason"] = "english_leftover", "English claim wording left in translation (" + f["category"] + ")"
        findings.append(f)
    findings.extend(scan_lang_terms(elements, locale))
    joined = " \n".join(elements)
    findings.extend(scan_glued_letter(joined, locale))
    if is_html:
        findings.extend(scan_truncated_items(en_value, value, locale, vocab))
        findings.extend(scan_table_ids(en_value, value))
    en_plain = " ".join(html_to_elements(en_value)) if is_html else (en_value or "")
    findings.extend(scan_brand(en_plain, joined, locale))
    return _dedupe(findings)


def _dedupe(findings: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    seen, out = set(), []
    for f in findings:
        k = (f["category"], f["rule"], f["match"].lower())
        if k in seen:
            continue
        seen.add(k)
        out.append(f)
    return out


# ---------------------------------------------------------------------------------------------
# Product-level scan (works on plain dicts, so it can run from a saved dump)
# ---------------------------------------------------------------------------------------------
EN_FIELDS = (("title", "title", False), ("body", "descriptionHtml", True))
TR_KEYS = {"title": "title", "body_html": "body", "meta_title": "seo_title", "meta_description": "seo_description"}


def scan_cut_search_title(name: str, meta_title: str) -> List[Dict[str, str]]:
    """A translated search title that stops part-way through the translated product name (before ' — ')."""
    if " — " not in name:
        return []
    segment = " ".join(name.split(" — ")[0].split())
    core = " ".join(re.split(r"\s*[|–—-]\s*Dress Like", meta_title)[0].split())
    if not core or len(core) >= len(segment) or not segment.startswith(core):
        return []
    return [_finding("seo_title", "cut-search-title", "search title stops part-way through the product name",
                     core, _cell("%s => %s" % (core, segment), SNIPPET_MAX))]


def scan_product(product: Dict, locales: Sequence[str],
                 vocabs: Optional[Dict[str, "Counter[str]"]] = None) -> List[Dict[str, str]]:
    handle = product["handle"]
    rows: List[Dict[str, str]] = []

    def add(locale: str, field: str, findings: List[Dict[str, str]]):
        for f in findings:
            rows.append({"handle": handle, "locale": locale, "field": field, **f})

    seo = product.get("seo") or {}
    add("en", "title", scan_english_field(product.get("title", ""), False))
    add("en", "body", scan_english_field(product.get("descriptionHtml", ""), True))
    add("en", "seo_title", scan_english_field(seo.get("title") or "", False))
    add("en", "seo_description", scan_english_field(seo.get("description") or "", False))
    en_src = {"title": product.get("title", ""), "body_html": product.get("descriptionHtml", ""),
              "meta_title": seo.get("title") or "", "meta_description": seo.get("description") or ""}
    for locale in locales:
        tr = (product.get("translations") or {}).get(locale) or {}
        for key, field in TR_KEYS.items():
            value = tr.get(key)
            if value:
                add(locale, field, scan_translation_field(locale, key, value, en_src[key], (vocabs or {}).get(locale)))
        add(locale, "seo_title", scan_cut_search_title(tr.get("title") or "", tr.get("meta_title") or ""))
    return rows


# ---------------------------------------------------------------------------------------------
# Admin GraphQL (reads only)
# ---------------------------------------------------------------------------------------------
class Admin:
    def __init__(self, store_domain: str = ""):
        from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # lazy: tests skip it
        self.endpoint = "https://%s/admin/api/%s/graphql.json" % (resolve_store_domain(store_domain), API_VERSION)
        self.token = load_access_token()
        self.available: Optional[float] = None
        self.restore = 50.0

    def gql(self, query: str, variables: Optional[Dict] = None, est_cost: float = 50.0) -> Dict:
        if self.available is not None and self.available < est_cost:
            time.sleep(min(10.0, (est_cost - self.available) / max(self.restore, 1.0) + 0.3))
        body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        for attempt in range(8):
            req = urllib.request.Request(self.endpoint, data=body, method="POST", headers={
                "Content-Type": "application/json", "X-Shopify-Access-Token": self.token})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    decoded = json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                if error.code in (429, 502, 503) and attempt < 7:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError("Shopify HTTP %s" % error.code) from error
            except (urllib.error.URLError, TimeoutError) as error:
                if attempt < 2:
                    time.sleep(3)
                    continue
                raise RuntimeError("Shopify request failed: %s" % type(error).__name__) from error
            throttle = ((decoded.get("extensions") or {}).get("cost") or {}).get("throttleStatus") or {}
            if throttle:
                self.available = throttle.get("currentlyAvailable")
                self.restore = throttle.get("restoreRate") or self.restore
            errors = decoded.get("errors")
            if errors and "THROTTLED" in json.dumps(errors).upper() and attempt < 7:
                time.sleep(2 * (attempt + 1))
                continue
            if errors:
                raise RuntimeError("Shopify GraphQL errors: " + json.dumps(errors)[:300])
            return decoded["data"]
        raise RuntimeError("Shopify GraphQL still throttled after retries")


Q_PRODUCTS = """query($cursor:String,$q:String){products(first:50,after:$cursor,query:$q){
 pageInfo{hasNextPage endCursor}
 nodes{id handle title status updatedAt descriptionHtml seo{title description}}}}"""


def fetch_products(admin: Admin, since_hours: Optional[float], handles: Optional[Sequence[str]]) -> List[Dict]:
    q = "status:active"
    if since_hours:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        q += " AND updated_at:>='%s'" % cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")
    out, cursor = [], None
    while True:
        data = admin.gql(Q_PRODUCTS, {"cursor": cursor, "q": q}, est_cost=120)["products"]
        out.extend(n for n in data["nodes"] if n.get("status") == "ACTIVE")
        if not data["pageInfo"]["hasNextPage"]:
            break
        cursor = data["pageInfo"]["endCursor"]
    if handles:
        wanted = set(handles)
        out = [p for p in out if p["handle"] in wanted]
    return out


def fetch_locales(admin: Admin) -> List[str]:
    rows = admin.gql("{shopLocales{locale primary published}}", est_cost=5)["shopLocales"]
    return [r["locale"] for r in rows if not r["primary"]]


def fetch_translations(admin: Admin, products: List[Dict], locales: Sequence[str], chunk: int = 8) -> None:
    """Attach product["translations"] = {locale: {key: value}} (translatable keys we scan only)."""
    wanted = set(TR_KEYS)
    aliases = " ".join('l%d:translations(locale:"%s"){key value}' % (i, loc) for i, loc in enumerate(locales))
    query = "query($ids:[ID!]!){translatableResourcesByIds(first:%d,resourceIds:$ids){nodes{resourceId %s}}}" % (chunk, aliases)
    by_id = {p["id"]: p for p in products}
    ids = list(by_id)
    for i in range(0, len(ids), chunk):
        part = ids[i:i + chunk]
        nodes = admin.gql(query, {"ids": part}, est_cost=40 + 4 * len(locales) * len(part))["translatableResourcesByIds"]["nodes"]
        for node in nodes:
            prod = by_id.get(node["resourceId"])
            if prod is None:
                continue
            prod["translations"] = {
                loc: {t["key"]: t["value"] for t in (node.get("l%d" % idx) or []) if t["key"] in wanted}
                for idx, loc in enumerate(locales)}


# ---------------------------------------------------------------------------------------------
# Content scan: published articles, pages and collections (and products in --resource all)
# ---------------------------------------------------------------------------------------------
# Article-level claim rules, on top of RULES. (category, rule_id, regex, reason)
_CONTENT_RULES_SRC: List[Tuple[str, str, str, str, bool]] = [
    ("popularity", "trend-claim",
     r"\bthis season'?s? (?:hottest|top|must[- ]have|biggest)\b|\bhott?est (?:colou?rs?|looks?|picks?|styles?|trends?|items?|sets?)\b"
     r"|\b(?:biggest|ultimate|hottest|top|#1) (?:\w+ ){0,2}trends?\b|\bfashion movement\b|\bon[- ]trend\b|\bgoing viral\b"
     r"|\beveryone(?:'s| is) (?:wearing|talking about|buying)\b|\bthe (?:look|set|style|colou?r) of the (?:season|year)\b",
     "trend/popularity claim with no data", False),
    ("size_advice", "size-up-kids",
     r"\b(?:size|sizing|order|go|choose|pick|buy|get) (?:up|a size up|one size (?:up|larger|bigger)|a size (?:larger|bigger))\b"
     r"|\b(?:a|one) size (?:up|larger|bigger)\b|\bsize up\b",
     "size-up advice for children (tight-fitting sleepwear safety, no size basis)", False),
]
CONTENT_RULES: List[Rule] = [Rule(*row) for row in _CONTENT_RULES_SRC]
KID_WORD_RE = re.compile(r"\b(?:kids?|child(?:ren)?|toddlers?|babies|baby|boys?|girls?|little ones?|youth|juniors?|mini)\b", re.I)

# "size up" advice in translations (phrase only; English needs a kid word in the sentence)
SIZE_UP_LANG_SRC = {
    "es": r"\buna talla m[aá]s\b|\buna talla (?:superior|mayor|arriba)\b", "de": r"\beine gr[oö](?:ß|ss)e (?:gr[oö](?:ß|ss)er|h[oö]her)\b|\beine nummer gr[oö](?:ß|ss)er\b",
    "fr": r"\bune taille (?:au[- ]dessus|de plus|sup[ée]rieure)\b", "it": r"\buna taglia (?:in pi[uù]|pi[uù] grande|superiore)\b",
    "pt": r"\bum tamanho (?:maior|acima)\b", "nl": r"\been maat (?:groter|omhoog)\b", "pl": r"\bo (?:jeden )?rozmiar (?:wi[eę]ksz\w+|wy[zż]sz\w+)\b",
    "cs": r"\bo (?:jednu )?velikost (?:v[eě]t[sš][ií]|vy[sš][sš][ií])\b|\bvelikost navíc\b",
}
SIZE_UP_LANG = {k: re.compile(v, _FLAGS) for k, v in SIZE_UP_LANG_SRC.items()}

STALE_KW = (r"(?:trends?|guides?|best|new|collections?|lookbook|picks?|styles?|outfits?|ideas?|edit|arrivals?|"
            r"seasons?|must[- ]haves?|updated?|favou?rites?|looks?|gift|sets?)")
STALE_BEFORE_RE = re.compile(r"(\b20\d\d)\b\s+(?:[\w'’&-]+\s+){0,2}" + STALE_KW + r"\b", re.I)
STALE_AFTER_RE = re.compile(r"\b" + STALE_KW + r"\b(?:\s+(?:for|of|in))?\s+(?:[\w'’&-]+\s+){0,1}(20\d\d)\b", re.I)
STALE_HISTORY_RE = re.compile(r"(?:since|from|before|until|through|during|back in|originally|launched|introduced|founded|started|began)\s*$", re.I)
ANY_YEAR_RE = re.compile(r"(?<![\d.])(20\d\d)(?![\d])")
MIN_YEAR = 2015


def find_stale_years(text: str, current_year: int, loose: bool = False) -> List[Tuple[str, int, int]]:
    """Years < current_year presented as current: adjacent to trend/guide/best/new/collection words, not after
    'since/from/before/...', and not part of a range that reaches the current year ('2025-2026').
    loose=True (translations, where the keywords are not English) flags every past year (use on short fields)."""
    out: List[Tuple[str, int, int]] = []
    seen = set()
    matches = []
    if loose:
        matches = [(m.group(1), m.start(1), m.end(1)) for m in ANY_YEAR_RE.finditer(text)]
    else:
        for rx in (STALE_BEFORE_RE, STALE_AFTER_RE):
            for m in rx.finditer(text):
                matches.append((m.group(1), m.start(1), m.end(1)))
    for year, s, e in matches:
        y = int(year)
        if not (MIN_YEAR <= y < current_year) or (s, e) in seen:
            continue
        if STALE_HISTORY_RE.search(text[max(0, s - 18):s]):
            continue
        tail = text[e:e + 14]
        if re.match(r"\s*(?:[-–—/&]|and|to|\+)\s*(?:20)?%02d\b" % (current_year % 100), tail, re.I):
            continue
        seen.add((s, e))
        out.append((year, s, e))
    return out


def scan_stale_years(text: str, current_year: int, loose: bool = False) -> List[Dict[str, str]]:
    out = []
    for year, s, e in find_stale_years(text, current_year, loose):
        out.append(_finding("stale_year", "stale-year", "past year presented as current (now %d)" % current_year,
                            year, snippet(text, s, e)))
    return _dedupe(out)


_ALT_RE = re.compile(r"""\balt\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)


def extract_alt_texts(raw: str) -> List[str]:
    return [clean_text(a or b) for a, b in _ALT_RE.findall(raw or "") if clean_text(a or b)]


_Q_END = ("?", "？", "؟", "?”", '?"')
_HEAD_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1\s*>", re.S | re.I)
_SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary\s*>", re.S | re.I)
_DT_RE = re.compile(r"<dt\b[^>]*>(.*?)</dt\s*>", re.S | re.I)


def _visible(raw: str) -> str:
    raw = re.sub(r"<(?:script|style)\b.*?</(?:script|style)>", " ", raw, flags=re.S | re.I)
    return clean_text(_TAG.sub(" ", raw))


def _is_question(text: str) -> bool:
    t = text.strip().rstrip("\"'”’) ").strip()
    return t.endswith(("?", "？", "؟")) and len(t) > 3


def find_unanswered_questions(raw: str) -> List[str]:
    """Question headings, <summary> and <dt> with no visible text before the next heading / closing block."""
    raw = raw or ""
    out: List[str] = []
    heads = list(_HEAD_RE.finditer(raw))
    for i, m in enumerate(heads):
        q = _visible(m.group(2))
        if not _is_question(q):
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(raw)
        if not _visible(raw[m.end():end]):
            if i + 1 < len(heads) and int(heads[i + 1].group(1)) > int(m.group(1)):
                continue  # section heading that introduces sub-headings, not a question awaiting its answer
            out.append(q)
    for m in _SUMMARY_RE.finditer(raw):
        q = _visible(m.group(1))
        if not _is_question(q):
            continue
        close = raw.lower().find("</details", m.end())
        if not _visible(raw[m.end():close if close >= 0 else len(raw)]):
            out.append(q)
    for m in _DT_RE.finditer(raw):
        q = _visible(m.group(1))
        if not _is_question(q):
            continue
        nxt = re.search(r"<dt\b|</dl", raw[m.end():], re.I)
        if not _visible(raw[m.end():m.end() + nxt.start() if nxt else len(raw)]):
            out.append(q)
    return out


def _norm_sentence(s: str) -> str:
    return re.sub(r"[\W_]+", " ", s.lower(), flags=re.U).strip()


_TERMINAL = (".", "!", "?", "。", "！", "？", "؟", "…", "।")


def find_duplicate_sentences(elements: Sequence[str], min_len: int = 60,
                             boilerplate: Optional[Iterable[str]] = None) -> List[str]:
    """Prose sentences (end in terminal punctuation; normalised, >= min_len characters) that occur twice or more
    inside one body. `boilerplate` = normalised sentences that are a site-wide template (card captions); skipped."""
    skip = set(boilerplate or ())
    counts: "Counter[str]" = Counter()
    first: Dict[str, str] = {}
    for element in elements:
        for sent, _ in sentences(element):
            if not sent.rstrip().endswith(_TERMINAL):
                continue
            n = _norm_sentence(sent)
            if len(n) >= min_len and n not in skip:
                counts[n] += 1
                first.setdefault(n, sent.strip())
    return [first[n] for n, c in counts.items() if c >= 2]


def build_boilerplate(bodies: Iterable[str], min_resources: int = 10, min_len: int = 60) -> set:
    """Normalised sentences found in at least `min_resources` different bodies (template captions)."""
    seen: "Counter[str]" = Counter()
    for raw in bodies:
        local = set()
        for el in html_to_elements(raw):
            for sent, _ in sentences(el):
                n = _norm_sentence(sent)
                if len(n) >= min_len:
                    local.add(n)
        seen.update(local)
    return {n for n, c in seen.items() if c >= min_resources}


def scan_content_rules(elements: Iterable[str]) -> List[Dict[str, str]]:
    """Article-level English rules (trend claims; size-up advice only when the sentence is about children)."""
    out = []
    for element in elements:
        for sent, _ in sentences(element):
            for rule in CONTENT_RULES:
                for m in rule.regex.finditer(sent):
                    if rule.rule_id == "size-up-kids" and not KID_WORD_RE.search(sent):
                        continue
                    out.append(_finding(rule.category, rule.rule_id, rule.reason, m.group(0), snippet(sent, m.start(), m.end())))
    return _dedupe(out)


# ---- internal links --------------------------------------------------------------------------
_HREF_RE = re.compile(r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
_LOCALE_SEG_RE = re.compile(r"^[a-z]{2}(?:-[a-z]{2,4})?$", re.I)
OWN_HOSTS = ("dresslikemommy.com", "myshopify.com")
KNOWN_FIRST = {"products", "collections", "pages", "blogs", "cart", "account", "policies", "search"}


def normalize_link(href: str) -> Optional[str]:
    """Internal href -> '/path' with locale prefix, query, fragment and trailing slash removed; None for external."""
    href = (href or "").strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "{{", "{%")):
        return None
    if re.match(r"^(?:https?:)?//", href, re.I):
        host = host_of(href)
        if not any(host == h or host.endswith("." + h) for h in OWN_HOSTS):
            return None
        href = re.sub(r"^(?:https?:)?//[^/]+", "", href, flags=re.I) or "/"
    if not href.startswith("/"):
        return None
    path = re.split(r"[?#]", href, maxsplit=1)[0]
    path = urllib.parse.unquote(path).rstrip("/") or "/"
    segs = path.split("/")
    if len(segs) > 2 and _LOCALE_SEG_RE.match(segs[1]) and segs[1].lower() not in KNOWN_FIRST and segs[2] in KNOWN_FIRST:
        path = "/" + "/".join(segs[2:])
    return path


def extract_internal_links(raw: str) -> List[str]:
    seen, out = set(), []
    for a, b in _HREF_RE.findall(raw or ""):
        p = normalize_link(a or b)
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def classify_path(path: str) -> Optional[Tuple[str, str]]:
    """('product', handle) | ('collection', handle) | ('page', handle) | ('article', 'blog/handle'); else None."""
    segs = [s for s in path.split("/") if s]
    if len(segs) >= 4 and segs[0] == "collections" and segs[2] == "products":
        return ("product", segs[3])
    if len(segs) >= 2 and segs[0] == "products":
        return ("product", segs[1])
    if len(segs) >= 2 and segs[0] == "collections" and segs[1] not in ("all", "frontpage"):
        return ("collection", segs[1])
    if len(segs) == 2 and segs[0] == "pages":
        return ("page", segs[1])
    if len(segs) >= 3 and segs[0] == "blogs":
        return ("article", segs[1] + "/" + segs[2])
    return None


def _target_state(path: str, index: Dict) -> Optional[str]:
    """None when the path resolves to live content; otherwise a short state word."""
    cls = classify_path(path)
    if cls is None:
        return None
    kind, key = cls
    if kind == "product":
        st = index["products"].get(key)
        return None if st == "ACTIVE" else ("missing" if st is None else st.lower())
    pool = {"collection": index["collections"], "page": index["pages"], "article": index["articles"]}[kind]
    if key not in pool:
        return "missing"
    return None if pool[key] else "unpublished"


def check_link(path: str, index: Dict) -> Optional[Dict[str, str]]:
    """Finding for one internal path, or None when it resolves. index = products{handle:status},
    collections/pages/articles{key:published}, redirects{path:target}. Redirects are followed (max 5) and
    reported as 'redirected' with the final target; a redirect that ends nowhere live is 'redirect-dead'."""
    state = _target_state(path, index)
    if state is None:
        return None
    seen, cur, hops = {path}, path, 0
    while hops < 5 and cur in index["redirects"]:
        nxt = normalize_link(index["redirects"][cur]) if index["redirects"][cur].startswith(("/", "http")) else None
        if not nxt or nxt in seen:
            break
        seen.add(nxt)
        cur, hops = nxt, hops + 1
        if _target_state(cur, index) is None:
            return _finding("link", "link-redirected", "link goes through a redirect; point it at the final target",
                            path, "%s -> %s" % (path, cur))
    if hops:
        return _finding("link", "link-redirect-dead", "redirect chain ends on content that is not live",
                        path, "%s -> %s (%s)" % (path, cur, _target_state(cur, index) or "?"))
    rule = {"missing": "link-missing", "draft": "link-inactive-product", "archived": "link-inactive-product",
            "unpublished": "link-unpublished"}.get(state, "link-inactive-product")
    return _finding("link", rule, "link target is %s" % state, path, "%s (%s)" % (path, state))


def scan_links(raw: str, index: Dict, skip: Optional[Iterable[str]] = None) -> List[Dict[str, str]]:
    skip_set = set(skip or ())
    out = []
    for p in extract_internal_links(raw):
        if p in skip_set:
            continue
        f = check_link(p, index)
        if f:
            out.append(f)
    return out


# ---- per-resource scan -----------------------------------------------------------------------
FIX = {
    "popularity/bestseller": "drop the claim or say 'matching set'", "popularity/most-popular": "drop 'popular'; state the style fact instead",
    "popularity/trending": "drop 'trending/viral'", "popularity/customer-favorite": "drop; no review data",
    "popularity/trend-claim": "rewrite as a neutral style description (no trend/hottest claim)",
    "size_advice/size-up-kids": "remove 'size up' advice; point to the size chart only",
    "stale_year/stale-year": "update the year to 2026 or remove it from the text/alt", "faq/unanswered-faq": "write a 1-2 sentence answer or delete the question",
    "duplicate/duplicate-sentence": "delete the repeated sentence", "link/link-redirected": "replace href with the final target",
    "link/link-missing": "remove the link/card or point at a live page", "link/link-inactive-product": "remove the card or swap for an ACTIVE product",
    "link/link-unpublished": "remove the link or publish the target", "link/link-redirect-dead": "re-point at a live page",
    "translated_claim/size-advice": "retranslate the sentence without size-up advice",
}
EN_CONTENT_SPECS = {
    "article": (("title", "title", False), ("body", "body", True), ("summary", "summary", True),
                ("seo_title", "seo_title", False), ("seo_description", "seo_description", False)),
    "page": (("title", "title", False), ("body", "body", True)),
    "collection": (("title", "title", False), ("body", "descriptionHtml", True),
                   ("seo_title", "seo_title", False), ("seo_description", "seo_description", False)),
}
CONTENT_TR_KEYS = {"title": ("title", False), "body_html": ("body", True), "summary_html": ("summary", True),
                   "meta_title": ("seo_title", False), "meta_description": ("seo_description", False)}
CONTENT_TR_WANTED = set(CONTENT_TR_KEYS)


# Content-only noise filters, tuned on the 2026-11-26 baseline (obvious false positives, not claims).
CONTENT_ALLOW_SRC = [
    r"\b(?:stay|staying|stays|stick(?:ing)? (?:to|with)|go(?:ing)? with|choose|choosing)\s+true[- ]to[- ]size\b",
    r"\b(?:versus|vs\.?|or|and)\s+true[- ]to[- ]size\b",
    r"\b(?:do not|don'?t|never|avoid|not)\b[^.]{0,20}\bsiz(?:e|ing) up\b",
    r"\bsizing up versus\b",
    r"(?:\b(?:no|not|without)\b|n['’]?t have an?)[^.]{0,25}\b(?:physical|retail|brick[- ]and[- ]mortar) (?:store|shop|location)s?\b",
    r"\b(?:non|no|nicht|pas|niet|geen|n[aã]o)\b[^.]{0,45}\bgarant\w*|\bgarant\w*[^.]{0,20}\b(?:non|nicht|pas|niet|geen|n[aã]o)\b",
    r"\blei garante\b|\bgarante prazos\b",
    r"\bships? from our fulfil+ment partners\b",
    r"\bguarantees under the Australian Consumer Law\b",
    r"\byour pediatrician\b|\bpediatrician'?s? (?:guidance|advice)\b",
    r"\bpremium price\b|\bwithout (?:the )?premium\b",
]
CONTENT_ALLOW = [re.compile(p, _FLAGS) for p in CONTENT_ALLOW_SRC]


def content_noise(f: Dict[str, str], locale: str) -> bool:
    """True for a finding that is a known false positive on articles/pages/collections."""
    rule, match, snip = f["rule"], f["match"], f.get("snippet", "")
    if rule == "brand-altered" and match.startswith(BRAND):
        return True  # 'Dress Like Mommyでは', 'Dress Like Mommyssa': the brand with a grammatical suffix
    if rule == "brand-altered" and ("#" + match) in snip:
        return True  # hashtag #DressLikeMommy
    if rule == "truncated-item" or (rule == "glued-letter" and "CTRL" in snip):
        return True  # whole words ('unida', 'parte') and keyboard shortcuts; every baseline hit was one of these
    if f["category"] == "english_leftover" and rule == "long-lasting" and match.lower().startswith("durab"):
        return True  # Romance cognates ('souvenirs durables'), not an English leftover
    if rule == "popularity" and locale.startswith("cs") and match.lower().startswith("nejobl"):
        return True  # 'the favourite photo' is not a product claim
    for rx in CONTENT_ALLOW:
        for m in rx.finditer(snip):
            if match.lower() in m.group(0).lower() or m.group(0).lower() in match.lower():
                return True
    return False



def scan_content_text(value: str, is_html: bool, current_year: int, index: Optional[Dict] = None,
                      field: str = "", boilerplate: Optional[set] = None) -> List[Dict[str, str]]:
    """One English field of a content resource: base rules, trend/size rules, stale years, FAQ, duplicates, links."""
    value = value or ""
    elements = html_to_elements(value) if is_html else ([clean_text(value)] if value.strip() else [])
    findings = [f for f in scan_english_field(value, is_html) if f["rule"] != "external-url"]
    findings.extend(scan_content_rules(elements))
    for el in elements:
        findings.extend(scan_stale_years(el, current_year))
    if is_html:
        for alt in extract_alt_texts(value):
            for f in scan_elements([alt]) + scan_content_rules([alt]) + scan_stale_years(alt, current_year):
                f = dict(f)
                f["snippet"] = "alt: " + f["snippet"]
                findings.append(f)
        for q in find_unanswered_questions(value):
            findings.append(_finding("faq", "unanswered-faq", "question with no answer text", q, snippet(q, 0, len(q))))
        for s in find_duplicate_sentences(elements, boilerplate=boilerplate):
            findings.append(_finding("duplicate", "duplicate-sentence", "same sentence twice in one body", s, snippet(s, 0, len(s))))
        if index is not None:
            findings.extend(scan_links(value, index))
    return [f for f in _dedupe(findings) if not content_noise(f, "en")]


def scan_content_translation(locale: str, key: str, value: str, en_value: str, current_year: int,
                             vocab: Optional["Counter[str]"], index: Optional[Dict],
                             boilerplate: Optional[set] = None) -> List[Dict[str, str]]:
    field, is_html = CONTENT_TR_KEYS[key]
    findings = [f for f in scan_translation_field(locale, "body_html" if is_html else key, value, en_value, vocab)
                if f["rule"] != "external-url"]
    base = locale.split("-")[0]
    rx = SIZE_UP_LANG.get(base)
    elements = html_to_elements(value) if is_html else [clean_text(value)]
    short = list(elements) if not is_html else [t for t in extract_alt_texts(value)]
    if is_html:
        short += [_visible(m.group(2)) for m in _HEAD_RE.finditer(value)]
    for text in short:
        findings.extend(scan_stale_years(text, current_year, loose=True))
    if rx:
        for el in elements:
            for sent, _ in sentences(el):
                for m in rx.finditer(sent):
                    findings.append(_finding("translated_claim", "size-advice", "size-up advice in translation (" + base + ")",
                                             m.group(0), snippet(sent, m.start(), m.end())))
    if is_html:
        for q in find_unanswered_questions(value):
            findings.append(_finding("faq", "unanswered-faq", "question with no answer text", q, snippet(q, 0, len(q))))
        for s in find_duplicate_sentences(elements, boilerplate=boilerplate):
            findings.append(_finding("duplicate", "duplicate-sentence", "same sentence twice in one body", s, snippet(s, 0, len(s))))
        if index is not None:
            findings.extend(scan_links(value, index, skip=extract_internal_links(en_value)))
    return [f for f in _dedupe(findings) if not content_noise(f, locale)]


def content_en_values(kind: str, res: Dict) -> Dict[str, str]:
    seo = res.get("seo") or {}
    return {"title": res.get("title") or "", "body": res.get("body") if kind != "collection" else res.get("descriptionHtml") or "",
            "summary": res.get("summary") or "", "seo_title": seo.get("title") or "", "seo_description": seo.get("description") or ""}


def scan_content_resource(kind: str, res: Dict, locales: Sequence[str], current_year: int,
                          vocabs: Optional[Dict[str, "Counter[str]"]] = None, index: Optional[Dict] = None,
                          boilerplate: Optional[Dict[str, set]] = None) -> List[Dict[str, str]]:
    handle = res["handle"]
    boilerplate = boilerplate or {}
    rows: List[Dict[str, str]] = []

    def add(locale: str, field: str, findings: List[Dict[str, str]]):
        for f in findings:
            if content_noise(f, locale):
                continue
            rows.append({"resource": kind, "handle": handle, "locale": locale, "field": field, **f})

    vals = content_en_values(kind, res)
    for field, _, is_html in EN_CONTENT_SPECS[kind]:
        add("en", field, scan_content_text(vals[field] or "", is_html, current_year, index, field, boilerplate.get("en")))
    img = res.get("image") or {}
    if img.get("altText"):
        add("en", "image_alt", [dict(f) for f in scan_elements([img["altText"]]) + scan_content_rules([img["altText"]])
                                + scan_stale_years(img["altText"], current_year)])
    key_en = {"title": "title", "body_html": "body", "summary_html": "summary", "meta_title": "seo_title", "meta_description": "seo_description"}
    for locale in locales:
        tr = (res.get("translations") or {}).get(locale) or {}
        for key, (field, _) in CONTENT_TR_KEYS.items():
            if tr.get(key) and any(field == f[0] for f in EN_CONTENT_SPECS[kind]):
                add(locale, field, scan_content_translation(locale, key, tr[key], vals[key_en[key]], current_year,
                                                            (vocabs or {}).get(locale), index, boilerplate.get(locale)))
    return rows


# ---- fetch -----------------------------------------------------------------------------------
_SEO_MF = 'metafields(first:5,namespace:"global"){nodes{key value}}'
Q_ARTICLES = """query($cursor:String){articles(first:40,after:$cursor){pageInfo{hasNextPage endCursor}
 nodes{id handle title body summary isPublished blog{handle} image{altText} %s}}}""" % _SEO_MF
Q_PAGES = """query($cursor:String){pages(first:40,after:$cursor){pageInfo{hasNextPage endCursor}
 nodes{id handle title body isPublished %s}}}""" % _SEO_MF
Q_COLLECTIONS = """query($cursor:String){collections(first:40,after:$cursor){pageInfo{hasNextPage endCursor}
 nodes{id handle title descriptionHtml seo{title description}
 resourcePublicationsV2(first:10){nodes{isPublished publication{name}}}}}}"""
Q_PRODUCT_INDEX = """query($cursor:String){products(first:250,after:$cursor){pageInfo{hasNextPage endCursor}nodes{handle status}}}"""
Q_REDIRECTS = """query($cursor:String){urlRedirects(first:250,after:$cursor){pageInfo{hasNextPage endCursor}nodes{path target}}}"""


def _pages(admin: Admin, query: str, root: str, est_cost: float) -> List[Dict]:
    out, cursor = [], None
    while True:
        data = admin.gql(query, {"cursor": cursor}, est_cost=est_cost)[root]
        out.extend(data["nodes"])
        if not data["pageInfo"]["hasNextPage"]:
            return out
        cursor = data["pageInfo"]["endCursor"]


def _seo_from_metafields(node: Dict) -> Dict[str, str]:
    mf = {m["key"]: m["value"] for m in ((node.get("metafields") or {}).get("nodes") or [])}
    return {"title": mf.get("title_tag", ""), "description": mf.get("description_tag", "")}


def fetch_content(admin: Admin) -> Dict:
    """All articles, pages and collections (published flag kept) plus the link index inputs."""
    articles = _pages(admin, Q_ARTICLES, "articles", 150)
    for a in articles:
        a["seo"] = _seo_from_metafields(a)
        a["blog_handle"] = (a.get("blog") or {}).get("handle", "")
    pages = _pages(admin, Q_PAGES, "pages", 100)
    for p in pages:
        p["seo"] = _seo_from_metafields(p)
    collections = _pages(admin, Q_COLLECTIONS, "collections", 120)
    for c in collections:
        pubs = ((c.get("resourcePublicationsV2") or {}).get("nodes") or [])
        c["isPublished"] = any(x.get("isPublished") and (x.get("publication") or {}).get("name") == "Online Store" for x in pubs)
        c.pop("resourcePublicationsV2", None)
    products = {n["handle"]: n["status"] for n in _pages(admin, Q_PRODUCT_INDEX, "products", 60)}
    redirects: Dict[str, str] = {}
    raw_redirects = _pages(admin, Q_REDIRECTS, "urlRedirects", 60)
    for n in raw_redirects:  # plain paths first; market-prefixed copies (/en-hk/...) only fill gaps
        if n["path"].split("/")[1:2] and n["path"].split("/")[1] in KNOWN_FIRST:
            redirects[n["path"].rstrip("/") or "/"] = n["target"]
    for n in raw_redirects:
        redirects.setdefault(normalize_link(n["path"]) or n["path"], n["target"])
    return {"articles": articles, "pages": pages, "collections": collections, "product_status": products, "redirects": redirects}


def build_link_index(content: Dict) -> Dict:
    articles = {}
    for a in content["articles"]:
        articles["%s/%s" % (a.get("blog_handle", ""), a["handle"])] = bool(a.get("isPublished"))
    return {"products": content["product_status"], "redirects": content["redirects"], "articles": articles,
            "collections": {c["handle"]: bool(c.get("isPublished")) for c in content["collections"]},
            "pages": {p["handle"]: bool(p.get("isPublished")) for p in content["pages"]}}


def fetch_content_translations(admin: Admin, items: List[Dict], locales: Sequence[str], chunk: int = 8) -> None:
    aliases = " ".join('l%d:translations(locale:"%s"){key value}' % (i, loc) for i, loc in enumerate(locales))
    query = "query($ids:[ID!]!){translatableResourcesByIds(first:%d,resourceIds:$ids){nodes{resourceId %s}}}" % (chunk, aliases)
    by_id = {p["id"]: p for p in items}
    ids = list(by_id)
    for i in range(0, len(ids), chunk):
        part = ids[i:i + chunk]
        nodes = admin.gql(query, {"ids": part}, est_cost=40 + 4 * len(locales) * len(part))["translatableResourcesByIds"]["nodes"]
        for node in nodes:
            item = by_id.get(node["resourceId"])
            if item is not None:
                item["translations"] = {
                    loc: {t["key"]: t["value"] for t in (node.get("l%d" % idx) or []) if t["key"] in CONTENT_TR_WANTED}
                    for idx, loc in enumerate(locales)}


def summarize_content(rows: List[Dict[str, str]]) -> Dict:
    by_res = Counter(r["resource"] for r in rows)
    by_cat = Counter(r["category"] for r in rows)
    by_rule = Counter("%s/%s" % (r["category"], r["rule"]) for r in rows)
    by_res_cat = Counter("%s:%s" % (r["resource"], r["category"]) for r in rows)
    return {"findings": len(rows), "resources_with_findings": len({(r["resource"], r["handle"]) for r in rows}),
            "by_resource": dict(sorted(by_res.items())), "by_category": dict(sorted(by_cat.items())),
            "by_resource_category": dict(sorted(by_res_cat.items())), "by_rule": dict(sorted(by_rule.items()))}


def group_rows(rows: List[Dict[str, str]]) -> List[Dict]:
    """Collapse locale copies: one group per (resource, handle, field, category, rule, EN-comparable match)."""
    groups: Dict[Tuple, Dict] = {}
    for r in rows:
        key = (r["resource"], r["handle"], r["field"], r["category"], r["rule"], r["match"].lower() if r["locale"] == "en" or r["category"] in ("link", "stale_year") else "(translations)")
        g = groups.setdefault(key, {"resource": r["resource"], "handle": r["handle"], "field": r["field"], "category": r["category"],
                                    "rule": r["rule"], "locales": [], "snippet": r["snippet"], "match": r["match"]})
        if r["locale"] not in g["locales"]:
            g["locales"].append(r["locale"])
    return sorted(groups.values(), key=lambda g: (g["category"], g["rule"], g["resource"], g["handle"], g["field"]))


def _locale_label(locales: List[str]) -> str:
    return ",".join(locales) if len(locales) <= 3 else "%s +%d" % (",".join(locales[:2]), len(locales) - 2)


def render_content_baseline(rows: List[Dict[str, str]], summary: Dict, title: str) -> str:
    groups = group_rows(rows)
    lines = ["# " + title, "", "Counts below are finding rows (one per handle, locale, field and rule). Read-only scan of PUBLISHED content.", "",
             "Scanned: " + ", ".join("%s=%d" % kv for kv in sorted(summary.get("scanned", {}).items())) + "; locales: " + ",".join(summary.get("locales", [])), "",
             "Total: %d rows in %d resources." % (summary["findings"], summary["resources_with_findings"]), "", "## Rows by resource and category", "",
             "| resource | " + " | ".join(sorted(summary["by_category"])) + " | total |", "|---|" + "---|" * (len(summary["by_category"]) + 1)]
    for res in sorted(summary["by_resource"]):
        cells = [str(summary["by_resource_category"].get("%s:%s" % (res, c), 0)) for c in sorted(summary["by_category"])]
        lines.append("| %s | %s | %d |" % (res, " | ".join(cells), summary["by_resource"][res]))
    lines += ["", "## Rows by rule", "", "| category/rule | rows | proposed fix |", "|---|---|---|"]
    for k, v in sorted(summary["by_rule"].items(), key=lambda kv: -kv[1]):
        lines.append("| %s | %d | %s |" % (k, v, FIX.get(k, "see section")))
    lines += ["", "## Findings grouped by fix pattern", "",
              "Rows: locale copies of one finding are collapsed (locales column); every row is also in findings.json.", ""]
    last = None
    for g in groups:
        pat = "%s/%s" % (g["category"], g["rule"])
        if pat != last:
            n = sum(1 for x in groups if x["category"] == g["category"] and x["rule"] == g["rule"])
            lines += ["", "### %s (%d groups) - fix: %s" % (pat, n, FIX.get(pat, "rewrite or remove the matched text")), "",
                      "| resource | handle | locales | field | matched text | proposed fix |", "|---|---|---|---|---|---|"]
            last = pat
        lines.append("| %s | %s | %s | %s | %s | %s |" % (g["resource"], g["handle"], _locale_label(g["locales"]), g["field"],
                                                         _cell(g["snippet"], SNIPPET_MAX), _cell(FIX.get(pat, "rewrite or remove"), 60)))
    return "\n".join(lines) + "\n"


def run_content(args: argparse.Namespace, kinds: Sequence[str]) -> int:
    handles = {h.strip() for h in args.handles.split(",") if h.strip()} if args.handles else None
    current_year = args.year or datetime.now().year
    products: List[Dict] = []
    if args.from_data:
        dump = json.loads(Path(args.from_data).read_text(encoding="utf-8"))
        content, locales = dump["content"], dump["locales"]
        products = dump.get("products") or []
    else:
        admin = Admin(args.store_domain)
        content = fetch_content(admin)
        locales = []
        if args.all_locales:
            locales = fetch_locales(admin)
        elif args.locales:
            locales = [x.strip() for x in args.locales.split(",") if x.strip()]
        if "product" in kinds:
            products = fetch_products(admin, args.since_hours, sorted(handles) if handles else None)
        if locales:
            targets = [x for k in ("articles", "pages", "collections") if k[:-1] in kinds for x in content[k] if x.get("isPublished")]
            fetch_content_translations(admin, targets, locales)
            if products:
                fetch_translations(admin, products, locales)
        if args.dump_data:
            Path(args.dump_data).write_text(json.dumps({"content": content, "locales": locales, "products": products}, ensure_ascii=False), encoding="utf-8")
    index = build_link_index(content)
    pools = {"article": content["articles"], "page": content["pages"], "collection": content["collections"]}
    rows: List[Dict[str, str]] = []
    scanned: Dict[str, int] = {}
    for kind in kinds:
        if kind == "product":
            vocabs = {loc: build_vocab(" ".join(html_to_elements(v) if k == "body_html" else [v])
                                       for p in products for k, v in ((p.get("translations") or {}).get(loc) or {}).items() if v)
                      for loc in locales}
            for p in products:
                for r in scan_product(p, locales, vocabs):
                    rows.append({"resource": "product", **r})
            scanned["product"] = len(products)
            continue
        items = [x for x in pools[kind] if x.get("isPublished") and (not handles or x["handle"] in handles)]
        vocabs = {}
        for loc in locales:
            texts = []
            for it in pools[kind]:
                for k, v in ((it.get("translations") or {}).get(loc) or {}).items():
                    if v:
                        texts.append(" ".join(html_to_elements(v)) if k in ("body_html", "summary_html") else v)
            vocabs[loc] = build_vocab(texts)
        boiler = {"en": build_boilerplate(it.get("body") or it.get("descriptionHtml") or "" for it in pools[kind])}
        for loc in locales:
            boiler[loc] = build_boilerplate((it.get("translations") or {}).get(loc, {}).get("body_html") or "" for it in pools[kind])
        for it in items:
            rows.extend(scan_content_resource(kind, it, locales, current_year, vocabs, index, boiler))
        scanned[kind] = len(items)
    rows.sort(key=lambda r: (r["resource"], r["handle"], r["locale"] != "en", r["locale"], r["field"], r["category"], r["rule"]))
    summary = summarize_content(rows)
    summary.update({"scanned": scanned, "locales": ["en"] + list(locales), "year": current_year})
    if args.json:
        print(json.dumps({"summary": summary, "findings": rows}, ensure_ascii=False, indent=2))
    elif args.markdown:
        print(render_markdown([{**r, "handle": "%s:%s" % (r["resource"], r["handle"])} for r in rows]))
    else:
        print(render_table([{**r, "handle": "%s:%s" % (r["resource"], r["handle"])} for r in rows]))
        print("\nscanned %s; locales: %s" % (", ".join("%d %s" % (v, k) for k, v in scanned.items()), ",".join(["en"] + list(locales))))
        print("findings: %d in %d resources; by category: %s" % (summary["findings"], summary["resources_with_findings"],
              ", ".join("%s=%d" % kv for kv in summary["by_category"].items()) or "none"))
    if args.findings_json:
        p = Path(args.findings_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"summary": summary, "findings": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.baseline_md:
        Path(args.baseline_md).write_text(render_content_baseline(rows, summary, args.baseline_title), encoding="utf-8")
    return 1 if (args.fail_on_findings and rows) else 0


# ---------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------
def summarize(rows: List[Dict[str, str]]) -> Dict:
    by_cat = Counter(r["category"] for r in rows)
    by_rule = Counter("%s/%s" % (r["category"], r["rule"]) for r in rows)
    return {"findings": len(rows), "products_with_findings": len({r["handle"] for r in rows}),
            "by_category": dict(sorted(by_cat.items())), "by_rule": dict(sorted(by_rule.items()))}


def _cell(text: str, width: int) -> str:
    text = (text or "").replace("\n", " ").replace("|", "/")
    return text if len(text) <= width else text[:width - 1] + "…"


def render_table(rows: List[Dict[str, str]]) -> str:
    if not rows:
        return "No findings."
    lines = ["%-44s %-6s %-16s %-26s %s" % ("handle", "locale", "field", "category/rule", "matched text")]
    for r in rows:
        lines.append("%-44s %-6s %-16s %-26s %s" % (_cell(r["handle"], 44), r["locale"], r["field"],
                                                     _cell(r["category"] + "/" + r["rule"], 26), _cell(r["snippet"], SNIPPET_MAX)))
    return "\n".join(lines)


def render_markdown(rows: List[Dict[str, str]]) -> str:
    lines = ["| handle | locale | field | category/rule | matched text |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %s | %s | %s | %s | %s |" % (r["handle"], r["locale"], r["field"],
                                                     r["category"] + "/" + r["rule"], _cell(r["snippet"], SNIPPET_MAX)))
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    resource = getattr(args, "resource", "products")
    if resource != "products":
        kinds = {"all": ["product", "article", "page", "collection"], "content": ["article", "page", "collection"]}.get(resource) or [resource[:-1]]
        return run_content(args, kinds)
    handles = [h.strip() for h in args.handles.split(",") if h.strip()] if args.handles else None
    if args.from_data:
        dump = json.loads(Path(args.from_data).read_text(encoding="utf-8"))
        products, locales = dump["products"], dump["locales"]
        if handles:
            products = [p for p in products if p["handle"] in set(handles)]
    else:
        admin = Admin(args.store_domain)
        products = fetch_products(admin, args.since_hours, handles)
        locales = []
        if args.all_locales:
            locales = fetch_locales(admin)
        elif args.locales:
            locales = [x.strip() for x in args.locales.split(",") if x.strip()]
        if locales and products:
            fetch_translations(admin, products, locales)
        if args.dump_data:
            Path(args.dump_data).write_text(json.dumps({"products": products, "locales": locales}, ensure_ascii=False), encoding="utf-8")
    vocabs = {loc: build_vocab(" ".join(html_to_elements(v) if k == "body_html" else [v])
                               for p in products for k, v in ((p.get("translations") or {}).get(loc) or {}).items() if v)
              for loc in locales}
    rows: List[Dict[str, str]] = []
    for p in products:
        rows.extend(scan_product(p, locales, vocabs))
    if getattr(args, "rule", ""):
        rows = [r for r in rows if r["rule"] == args.rule]
    rows.sort(key=lambda r: (r["handle"], r["locale"] != "en", r["locale"], r["field"], r["category"], r["rule"]))
    summary = summarize(rows)
    summary.update({"products_scanned": len(products), "locales": ["en"] + list(locales)})
    if args.json:
        print(json.dumps({"summary": summary, "findings": rows}, ensure_ascii=False, indent=2))
    elif args.markdown:
        print(render_markdown(rows))
    else:
        print(render_table(rows))
        print("\nscanned %d active products, locales: %s" % (len(products), ",".join(["en"] + list(locales))))
        print("findings: %d in %d products; by category: %s" % (
            summary["findings"], summary["products_with_findings"],
            ", ".join("%s=%d" % kv for kv in summary["by_category"].items()) or "none"))
    return 1 if (args.fail_on_findings and rows) else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--locales", default="", help="comma list of locales to scan, e.g. es,de,fr")
    p.add_argument("--all-locales", action="store_true", help="scan every non-primary shop locale")
    p.add_argument("--handles", default="", help="comma list of product handles to scope the scan")
    p.add_argument("--since-hours", type=float, default=None, help="only products updated in the last N hours")
    p.add_argument("--rule", default="", help="product scan only: keep findings of one rule, e.g. cut-search-title")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--markdown", action="store_true", help="markdown table output")
    p.add_argument("--fail-on-findings", action="store_true", help="exit 1 when any finding remains")
    p.add_argument("--store-domain", default="", help="override the store domain")
    p.add_argument("--dump-data", default="", help="save fetched product data (no secrets) to this JSON file")
    p.add_argument("--resource", choices=("products", "articles", "pages", "collections", "content", "all"), default="products",
                   help="what to scan (default products); articles/pages/collections scan PUBLISHED content incl. internal links; "
                        "content = those three; all = those three plus products")
    p.add_argument("--year", type=int, default=None, help="treat this as the current year for the stale-year rule (default: today)")
    p.add_argument("--findings-json", default="", help="content modes: also write summary+findings to this JSON file")
    p.add_argument("--baseline-md", default="", help="content modes: also write a grouped markdown baseline to this path")
    p.add_argument("--baseline-title", default="Content check baseline", help="title line for --baseline-md")
    p.add_argument("--from-data", default="", help="scan a saved dump instead of calling the Admin API")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except RuntimeError as error:
        print("ERROR: %s" % error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
