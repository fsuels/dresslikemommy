"""Bounded public, cookie-free GET audit; extracted source is not rendered QA.

Reads 21 configured locale collection routes and one observed RO/NL/EN product
link each. No customer, consent, locale-selection, cart or checkout operations.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

BASE = Path(__file__).resolve().parent
MARKETS = BASE.parent / "markets/market_readback.json"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
SKIP = {"script", "style", "noscript", "template", "svg"}


def now():
    return datetime.now(timezone.utc).isoformat()


def clean(value):
    return re.sub(r"\s+", " ", value).strip()


class SameOriginRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname != "www.dresslikemommy.com":
            raise ValueError("Non-approved redirect destination; stopped")
        if any(part in parsed.path.lower() for part in ["/challenge", "/account/login", "/password"]):
            raise ValueError("Authentication/challenge redirect; stopped")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class SourceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.open_items = []
        self.head_title = []
        self.canonicals = []
        self.headings = []
        self.product_links = []
        self.buttons = []
        self.main_text = []
        self.header_text = []
        self.html_lang = None
        self.html_dir = None
        self.localized_inputs = []
        self.hreflang = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang, self.html_dir = a.get("lang"), a.get("dir")
        in_main = tag == "main" or any(t == "main" for t, _ in self.stack)
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonicals.append(a.get("href"))
        if tag == "link" and a.get("hreflang"):
            self.hreflang.append({"locale": a.get("hreflang"), "href": a.get("href")})
        if tag == "input" and a.get("name") in {"country_code", "locale_code"}:
            self.localized_inputs.append({"name": a["name"], "value": a.get("value")})
        kind = None
        if tag in {"h1", "h2", "h3"}:
            kind = "heading"
        elif tag == "title" and any(t == "head" for t, _ in self.stack):
            kind = "title"
        elif tag == "a" and in_main and "/products/" in a.get("href", ""):
            kind = "product_link"
        elif tag == "button" and in_main:
            kind = "button"
        if tag not in VOID:
            self.stack.append((tag, a))
        if kind:
            self.open_items.append({"kind": kind, "tag": tag, "depth": len(self.stack), "attrs": {k: a[k] for k in ["id", "class", "href", "aria-label", "disabled", "hidden", "aria-hidden"] if k in a}, "in_main": in_main, "text": []})

    def handle_endtag(self, tag):
        pos = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if pos is None:
            return
        for item in list(self.open_items):
            if item["depth"] > pos:
                item["text"] = clean(" ".join(item["text"]))
                kind = item.pop("kind")
                item.pop("depth")
                if kind == "title":
                    self.head_title.append(item["text"])
                elif kind == "heading":
                    self.headings.append(item)
                elif kind == "product_link":
                    self.product_links.append(item)
                else:
                    self.buttons.append(item)
                self.open_items.remove(item)
        del self.stack[pos:]

    def handle_data(self, value):
        tags = {t for t, _ in self.stack}
        if tags.intersection(SKIP):
            return
        text = clean(value)
        if not text:
            return
        for item in self.open_items:
            item["text"].append(text)
        if "main" in tags:
            self.main_text.append(text)
        if "header" in tags:
            self.header_text.append(text)


def safe_bootstrap(source, name, allowed):
    match = re.search(r"Shopify\." + name + r"\s*=\s*(\{[^;]+\})", source)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {"parse": "UNAVAILABLE"}
    return {k: value[k] for k in allowed if k in value}


def fetch(locale, url, kind):
    before = now()
    row = {"locale": locale, "kind": kind, "requested_url": url, "started_at": before, "request_cookies": False, "rendered_qa": "NOT_RUN", "attempts": 0}
    for attempt in range(2):
        row["attempts"] += 1
        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; DLM-ReadOnly-QualityCheck/1.0)", "Accept": "text/html"})
            with build_opener(SameOriginRedirect()).open(request, timeout=30) as response:
                body = response.read(8_000_001)
                if len(body) > 8_000_000:
                    raise ValueError("Response exceeds8MBbound")
                row.update({"http_status": response.status, "final_url": response.geturl(), "response_headers": {k: response.headers.get(k) for k in ["Content-Type", "Content-Language", "Date", "Content-Encoding"] if response.headers.get(k)}, "response_bytes": len(body), "response_sha256": hashlib.sha256(body).hexdigest()})
                source = body.decode("utf-8", "replace")
            if re.search(r"<title[^>]*>\s*(?:Just a moment|Attention Required|Security verification)", source, re.I):
                raise ValueError("Challenge page; stopped")
            parser = SourceParser()
            parser.feed(source)
            parser.close()
            links = []
            seen = set()
            for link in parser.product_links:
                href = urljoin(row["final_url"], link["attrs"].get("href", ""))
                parsed = urlparse(href)
                if parsed.hostname != "www.dresslikemommy.com":
                    continue
                clean_url = parsed._replace(query="", fragment="").geturl()
                if clean_url not in seen:
                    seen.add(clean_url)
                    links.append({"url": clean_url, "text": link["text"], "id": link["attrs"].get("id"), "class": link["attrs"].get("class")})
                elif link["text"]:
                    prior = next(x for x in links if x["url"] == clean_url)
                    if not prior["text"]:
                        prior["text"] = link["text"]
            row.update({"html_lang": parser.html_lang, "html_dir": parser.html_dir, "head_title": parser.head_title, "canonicals": parser.canonicals, "headings": parser.headings, "main_headings": [h for h in parser.headings if h["in_main"]], "product_links": links, "main_unique_product_link_count": len(links), "main_buttons": parser.buttons, "main_text": clean(" ".join(parser.main_text)), "header_text": clean(" ".join(parser.header_text)), "localization_inputs": parser.localized_inputs, "hreflang": parser.hreflang, "shopify_currency": safe_bootstrap(source, "currency", {"active", "rate"}), "shopify_theme": safe_bootstrap(source, "theme", {"id", "role", "schema_name", "schema_version"}), "extraction_status": "PASS"})
            break
        except HTTPError as exc:
            row.update({"http_status": exc.code, "error": str(exc), "extraction_status": "HTTP_ERROR"})
            if exc.code >= 500 and attempt == 0:
                time.sleep(1)
                continue
            break
        except (TimeoutError, URLError) as exc:
            row.update({"error_type": type(exc).__name__, "error": str(exc), "extraction_status": "NETWORK_ERROR"})
            if attempt == 0:
                time.sleep(1)
                continue
            break
        except ValueError as exc:
            row.update({"error": str(exc), "extraction_status": "STOPPED"})
            break
    row["completed_at"] = now()
    return row


def save_json(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    source = json.loads(MARKETS.read_text())
    routes = source["locale_roots"]
    assert len(routes) == 21 and len({r["locale"] for r in routes}) == 21
    targets = [(r["locale"], urljoin(r["root_url"], "collections/mommy-and-me")) for r in routes]
    started = now()
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = {pool.submit(fetch, locale, url, "collection"): locale for locale, url in targets}
        for future in as_completed(pending):
            result = future.result()
            results.append(result)
            save_json("source_collection_" + result["locale"] + ".json", result)
            print(json.dumps({"locale": result["locale"], "status": result.get("http_status"), "lang": result.get("html_lang"), "products": result.get("main_unique_product_link_count"), "source_status": result["extraction_status"]}), flush=True)
    results.sort(key=lambda r: r["locale"])
    deep = []
    for locale in ["ro", "nl", "en"]:
        collection = next(r for r in results if r["locale"] == locale)
        if collection.get("extraction_status") != "PASS" or not collection["product_links"]:
            deep.append({"locale": locale, "extraction_status": "BLOCKED_NO_OBSERVED_PRODUCT_LINK"})
            continue
        link = collection["product_links"][0]
        product = fetch(locale, link["url"], "product")
        product["observed_link_source"] = collection["requested_url"]
        product["observed_link_text"] = link["text"]
        deep.append(product)
        save_json("source_product_" + locale + ".json", product)
        print(json.dumps({"deep_locale": locale, "status": product.get("http_status"), "lang": product.get("html_lang"), "source_status": product["extraction_status"]}), flush=True)
    csv_rows = [{"locale": r["locale"], "requested_url": r["requested_url"], "http_status": r.get("http_status"), "final_url": r.get("final_url"), "canonical": "|".join(r.get("canonicals", [])), "head_title": "|".join(r.get("head_title", [])), "html_lang": r.get("html_lang"), "html_dir": r.get("html_dir"), "main_h1": "|".join(h["text"] for h in r.get("main_headings", []) if h["tag"] == "h1"), "source_unique_products": r.get("main_unique_product_link_count"), "source_currency": (r.get("shopify_currency") or {}).get("active"), "theme_id": (r.get("shopify_theme") or {}).get("id"), "theme_role": (r.get("shopify_theme") or {}).get("role"), "extraction_status": r["extraction_status"], "rendered_acceptance": "NOT_RUN"} for r in results]
    with (BASE / "locale_collection_matrix.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0])); writer.writeheader(); writer.writerows(csv_rows)
    checks = {"all21configured_locales_attempted": len(results) == 21, "each_locale_once": len({r["locale"] for r in results}) == 21, "no_external_host": all(urlparse(r.get("final_url", r["requested_url"])).hostname == "www.dresslikemommy.com" for r in results), "read_only_methods": True, "main_theme_all_successful": all((r.get("shopify_theme") or {}).get("role") == "main" and (r.get("shopify_theme") or {}).get("id") == 133290917985 for r in results if r["extraction_status"] == "PASS"), "three_deep_source_targets": len(deep) == 3}
    save_json("capture_summary.json", {"artifact_type": "READ_ONLY_PUBLIC_SOURCE_EVIDENCE_NOT_RENDERED_ACCEPTANCE", "started_at": started, "completed_at": now(), "locale_source": "../markets/market_readback.json", "locale_source_sha256": hashlib.sha256(MARKETS.read_bytes()).hexdigest(), "http_navigation_limit": "21collections+3observed_products; one earlier Romanian probe; max2workers; max1retry onlytransient5xx/network", "cookies_sent_or_saved": False, "raw_html_persisted": False, "sanitization": "Persist only selected public head/body elements, safe theme/currency fields, public links, response hash and allowlisted headers. Script bodies, cookies, token-bearing URLs and customer data excluded.", "rendered_surface": {"status": "UNAVAILABLE", "attempt": "cua.createBrowserTab('iab',Romanian_collection,{visible:false}) returned Browser is not available: iab; targeted listBrowsers found noIAB", "tabs_created": 0, "native_fallback": False}, "http_successes": sum(r.get("http_status") == 200 for r in results), "source_collections": [{"locale": r["locale"], "evidence": "source_collection_" + r["locale"] + ".json"} for r in results], "deep_source_products": [{"locale": r["locale"], "url": r.get("requested_url"), "status": r.get("extraction_status"), "evidence": "source_product_" + r["locale"] + ".json"} for r in deep], "validation": checks, "external_mutations": 0, "country_context_not_selected": True, "viewport_and_interaction_checks": "NOT_RUN"})
    print(json.dumps({"collections": len(results), "http200": sum(r.get("http_status") == 200 for r in results), "deep_source_products": len(deep), "checks": checks}, indent=2), flush=True)


if __name__ == "__main__":
    main()
