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
    r"\b(?:find|finding|choose|choosing|pick|picking|get|getting|for)\s+(?:your|the)\s+(?:perfect|best|right)\s+fit\b",
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
           ("performance", r"\brychleschnouc\w*\b|\bhypoalergenn\w*\b|\bdokonal\w* padnut\w*\b|\bvysok\w* kvalit\w*\b|\bvysoce kvalitn\w*\b|\bprémiov\w*\b|\bzaru[cč]uje\w*\b|\bgarantuje\w*\b|\bnemačkav\w*\b|\bvodot[eě]sn\w*\b")],
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
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--markdown", action="store_true", help="markdown table output")
    p.add_argument("--fail-on-findings", action="store_true", help="exit 1 when any finding remains")
    p.add_argument("--store-domain", default="", help="override the store domain")
    p.add_argument("--dump-data", default="", help="save fetched product data (no secrets) to this JSON file")
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
