#!/usr/bin/env python3
"""Audit public localized PDP routes for obvious English leakage."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://www.dresslikemommy.com"
DEFAULT_LOCALES = "es,fr,de,it,pt-BR,ro"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 "
    "DressLikeMommyLocalizationAudit/1.0"
)

TRANSLATION_KEY_RE = re.compile(
    r"\b(?:translation missing|sections|secciones|products|general|shopify)\.[a-z0-9_.-]+",
    re.I,
)

ENGLISH_PHRASES = [
    "No reviews",
    "Choose size",
    "Choose sizes for each family member",
    "Choose at least one size",
    "Choose the family sizes",
    "Build your matching set",
    "Add selected pieces",
    "Add matching pieces",
    "Secure checkout",
    "Secure Checkout",
    "Standard shipping included",
    "30-day returns",
    "30-day returns & exchanges",
    "Ships to",
    "Return or exchange within 30 days",
    "Open full return policy",
    "Open full privacy policy",
    "Privacy & secure checkout",
    "Customer Reviews",
    "Customer reviews",
    "Be the first to write a review",
    "Write a review",
    "Customer photos",
    "Fabric & feel",
    "Family story",
    "Design details",
    "Machine wash cold",
    "Size range",
    "Key features",
    "Coordinated family options",
    "Vacation-ready",
    "Role-bearing sizes",
    "Chart-backed draft",
    "Shorts excluded",
    "Choose the Type and Size",
    "Family matching styles loved by",
    "Read the",
]

COMMON_ENGLISH_WORDS = {
    "a",
    "about",
    "accept",
    "accepted",
    "add",
    "after",
    "all",
    "and",
    "are",
    "as",
    "at",
    "available",
    "be",
    "before",
    "below",
    "between",
    "by",
    "can",
    "cart",
    "checkout",
    "choose",
    "cold",
    "complete",
    "contact",
    "delivery",
    "details",
    "do",
    "each",
    "for",
    "from",
    "full",
    "if",
    "in",
    "included",
    "is",
    "it",
    "made",
    "matching",
    "must",
    "not",
    "of",
    "on",
    "one",
    "options",
    "or",
    "order",
    "our",
    "payment",
    "photos",
    "policy",
    "privacy",
    "product",
    "ready",
    "return",
    "returns",
    "secure",
    "selection",
    "separately",
    "set",
    "shipping",
    "shop",
    "size",
    "sizes",
    "standard",
    "store",
    "the",
    "this",
    "to",
    "together",
    "type",
    "unwashed",
    "unworn",
    "use",
    "we",
    "with",
    "within",
    "you",
    "your",
}

ALLOW_SNIPPET_RE = re.compile(
    r"\b("
    r"Dress Like Mommy|Shop Pay|Apple Pay|Google Pay|PayPal|Visa|Mastercard|"
    r"American Express|Diners Club|Discover|Amazon|USDC|USD|CAD|EUR|GBP|"
    r"cm|in|kg|lb|lbs|2XL|3XL|4XL|XL|S|M|L"
    r")\b",
    re.I,
)


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_stack: list[str] = []
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "svg", "noscript", "template"}:
            self._skip_stack.append(tag.lower())
        if tag.lower() in {"br", "p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop()
        if tag in {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_stack:
            return
        if data:
            self._chunks.append(data)

    def text(self) -> str:
        value = html.unescape(" ".join(self._chunks))
        lines = [re.sub(r"\s+", " ", line).strip() for line in value.splitlines()]
        return "\n".join(line for line in lines if line)


@dataclass(frozen=True)
class AuditTarget:
    handle: str
    locale: str
    url: str


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def locale_route(locale: str) -> str:
    normalized = locale.strip().replace("_", "-")
    if not normalized or normalized.lower() == "en":
        return ""
    if normalized.lower() == "pt-br":
        return "pt"
    return normalized.lower()


def build_targets(handles: Iterable[str], locales: Iterable[str], base_url: str) -> list[AuditTarget]:
    root = base_url.rstrip("/")
    targets: list[AuditTarget] = []
    for handle in handles:
        for locale in locales:
            route = locale_route(locale)
            path = f"/{route}/products/{handle}" if route else f"/products/{handle}"
            targets.append(AuditTarget(handle=handle, locale=locale, url=f"{root}{path}"))
    return targets


def fetch(url: str, timeout: int) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return int(response.status), body
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body
    except URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def visible_text(markup: str) -> str:
    parser = VisibleTextParser()
    parser.feed(markup)
    parser.close()
    return parser.text()


def snippet_around(text: str, start: int, end: int, context_chars: int) -> str:
    left = max(0, start - context_chars)
    right = min(len(text), end + context_chars)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def phrase_regex(phrase: str) -> re.Pattern[str]:
    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![A-Za-z]){escaped}(?![A-Za-z])", re.I)


def sentences(text: str) -> Iterable[tuple[int, int, str]]:
    for match in re.finditer(r"[^.!?\n]{35,360}(?:[.!?]|\n|$)", text):
        sentence = re.sub(r"\s+", " ", match.group(0)).strip()
        if sentence:
            yield match.start(), match.end(), sentence


def is_likely_english_sentence(sentence: str) -> bool:
    if ALLOW_SNIPPET_RE.fullmatch(sentence.strip()):
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'-]+", sentence)
    if len(words) < 8:
        return False
    lower_words = {word.lower().strip("'") for word in words}
    common_hits = lower_words & COMMON_ENGLISH_WORDS
    return len(common_hits) >= 4


def audit_text(target: AuditTarget, text: str, *, context_chars: int, heuristic: bool, max_snippets: int) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for match in TRANSLATION_KEY_RE.finditer(text):
        issues.append(
            {
                "handle": target.handle,
                "locale": target.locale,
                "url": target.url,
                "issue_type": "translation_key_or_missing",
                "phrase": match.group(0),
                "snippet": snippet_around(text, match.start(), match.end(), context_chars),
            }
        )

    for phrase in ENGLISH_PHRASES:
        for match in phrase_regex(phrase).finditer(text):
            issues.append(
                {
                    "handle": target.handle,
                    "locale": target.locale,
                    "url": target.url,
                    "issue_type": "known_english_phrase",
                    "phrase": phrase,
                    "snippet": snippet_around(text, match.start(), match.end(), context_chars),
                }
            )

    if heuristic:
        for start, end, sentence in sentences(text):
            if not is_likely_english_sentence(sentence):
                continue
            if any(existing["snippet"] == sentence for existing in issues):
                continue
            issues.append(
                {
                    "handle": target.handle,
                    "locale": target.locale,
                    "url": target.url,
                    "issue_type": "likely_english_sentence",
                    "phrase": "",
                    "snippet": snippet_around(text, start, end, context_chars),
                }
            )

    return issues[:max_snippets] if max_snippets > 0 else issues


def write_reports(issues: list[dict[str, str]], report_json: str, report_csv: str) -> None:
    if report_json:
        path = Path(report_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(issues, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if report_csv:
        path = Path(report_csv)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["handle", "locale", "url", "issue_type", "phrase", "snippet"])
            writer.writeheader()
            writer.writerows(issues)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handles", required=True, help="Comma-separated product handles.")
    parser.add_argument("--locales", default=DEFAULT_LOCALES, help="Comma-separated locale route prefixes.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause-ms", type=int, default=250)
    parser.add_argument("--context-chars", type=int, default=90)
    parser.add_argument("--max-snippets", type=int, default=80)
    parser.add_argument("--no-heuristic", action="store_true", help="Disable likely-English sentence heuristic.")
    parser.add_argument("--report-json", default="")
    parser.add_argument("--report-csv", default="")
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()

    handles = split_csv(args.handles)
    locales = split_csv(args.locales)
    if not handles:
        raise SystemExit("No handles provided.")
    if not locales:
        raise SystemExit("No locales provided.")

    issues: list[dict[str, str]] = []
    route_results: list[dict[str, object]] = []
    for target in build_targets(handles, locales, args.base_url):
        try:
            status, markup = fetch(target.url, args.timeout)
            text = visible_text(markup)
            target_issues = audit_text(
                target,
                text,
                context_chars=max(args.context_chars, 20),
                heuristic=not args.no_heuristic,
                max_snippets=max(args.max_snippets, 0),
            )
            issues.extend(target_issues)
            route_results.append(
                {
                    "handle": target.handle,
                    "locale": target.locale,
                    "url": target.url,
                    "status": status,
                    "issue_count": len(target_issues),
                }
            )
        except Exception as exc:  # noqa: BLE001
            issues.append(
                {
                    "handle": target.handle,
                    "locale": target.locale,
                    "url": target.url,
                    "issue_type": "fetch_error",
                    "phrase": "",
                    "snippet": str(exc),
                }
            )
            route_results.append(
                {
                    "handle": target.handle,
                    "locale": target.locale,
                    "url": target.url,
                    "status": "ERROR",
                    "issue_count": 1,
                }
            )

        if args.pause_ms > 0:
            time.sleep(args.pause_ms / 1000)

    write_reports(issues, args.report_json, args.report_csv)
    summary = {
        "routes_checked": len(route_results),
        "routes_with_issues": sum(1 for row in route_results if int(row["issue_count"]) > 0),
        "issue_count": len(issues),
        "results": route_results,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if issues and args.fail_on_issues:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
