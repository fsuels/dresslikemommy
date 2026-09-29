#!/usr/bin/env python3
"""Guarded helper for the unattended organic-traffic agent (ops/organic/ORGANIC_ENGINE.md).

Subcommands (every write is dry-run unless --execute is passed):
  inventory       read-only: live collections, blog articles and redirect count -> JSON
  check           read-only: fetch live storefront URLs and report on-page SEO signals
  lint-article    read-only: quality and honesty gate for a Style Journal article draft
  collection-seo  update one collection's SEO title/description (before-state + readback)
  redirect        create one URL redirect after checking the target is live
  article-seo     set one published article's SEO title/description (before-state + readback)
  article-links   read-only: live articles ranked by links to non-active products / dead collections
  article-body    replace one live article's body HTML (full before-body kept in the receipt)
  translate-queue read-only: which article fields are missing/outdated in which storefront languages
  translate-next  read-only: pick the next article + up to N languages to translate (engine articles, then repaired ones)
  translate-apply register an article's translations from a JSON file (validated; digest-bound; readback)

Only the Shopify Admin API and the public storefront are touched. No theme, product,
feed, translation, ad or spend writes are possible from this script.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402

API_VERSION = "2026-01"
STOREFRONT = "https://www.dresslikemommy.com"
USER_AGENT = "Mozilla/5.0 (compatible; DLM-organic-engine/1.0)"

# Head collections whose title/meta/copy the theme forces (snippets/collection-seo-fallback.liquid).
# Admin SEO edits there do not render, so the engine refuses them; change the theme instead.
THEME_OWNED_COLLECTIONS = {
    "mommy-and-me", "christmas-pajamas", "new-women-outfits", "daddy-me", "daddy-and-me",
    "swimsuits", "family-pajamas", "popular-mommy-me-1", "popular-family-matching", "all",
}

# Claims a dropshipping store cannot back up (CLAUDE.md non-negotiables).
BANNED_CLAIMS = [
    r"\bin stock\b", r"\bstocked\b", r"\bon[- ]hand\b", r"\bwarehouse\b", r"\bships? (today|same day|fast)\b",
    r"\bfast shipping\b", r"\bexpress shipping\b", r"\bnext[- ]day\b", r"\b2[- ]day\b", r"\bbest[- ]?sellers?\b",
    r"\bbest[- ]selling\b", r"\btop[- ]rated\b", r"\b5[- ]star\b", r"\bcustomer reviews?\b", r"\breviews? (say|love)\b",
    r"\bour store\b", r"\bvisit us\b", r"\blimited stock\b", r"\bselling out\b", r"\bonly \d+ left\b",
    r"\bguaranteed (delivery|arrival)\b", r"\barrives? by\b", r"\bfree returns\b", r"\b#1\b", r"\bnumber one\b",
    r"1688", r"buckydrop", r"aliexpress", r"taobao", r"\bdropship", r"\bchatgpt\b", r"\bai[- ]generated\b",
    r"\b(dog|cat|pet)s?\b", r"\bhappiness guarantee\b", r"\bmoney[- ]back\b", r"\bfree shipping on all orders\b",
    r"\bdisney\b",
]
BANNED_RE = re.compile("|".join(BANNED_CLAIMS), re.IGNORECASE)


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_json(path: str, payload) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class Admin:
    def __init__(self, store_domain: str = "", token: str = ""):
        domain = resolve_store_domain(store_domain)
        self.endpoint = f"https://{domain}/admin/api/{API_VERSION}/graphql.json"
        self.token = load_access_token(token)

    def gql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint, data=body, method="POST",
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": self.token},
        )
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"Shopify HTTP {error.code}: {error.read().decode('utf-8', 'replace')[:300]}") from error
        if decoded.get("errors"):
            raise RuntimeError(f"Shopify GraphQL errors: {decoded['errors']}")
        return decoded["data"]

    def paged(self, query: str, root: str, variables: Optional[Dict] = None) -> List[Dict]:
        nodes, cursor = [], None
        while True:
            data = self.gql(query, {**(variables or {}), "cursor": cursor})[root]
            nodes.extend(data["nodes"])
            if not data["pageInfo"]["hasNextPage"]:
                return nodes
            cursor = data["pageInfo"]["endCursor"]


COLLECTIONS_Q = """query($cursor: String) { collections(first: 100, after: $cursor) {
  nodes { id handle title updatedAt productsCount { count } seo { title description }
          descriptionHtml ruleSet { appliedDisjunctively } }
  pageInfo { hasNextPage endCursor } } }"""
ARTICLES_Q = """query($cursor: String) { articles(first: 100, after: $cursor) {
  nodes { id handle title isPublished publishedAt updatedAt tags blog { handle }
          seoTitle: metafield(namespace: "global", key: "title_tag") { value }
          seoDesc: metafield(namespace: "global", key: "description_tag") { value } }
  pageInfo { hasNextPage endCursor } } }"""
COLLECTION_BY_HANDLE_Q = """query($handle: String!) { collectionByHandle(handle: $handle) {
  id handle title productsCount { count } seo { title description } } }"""
COLLECTION_UPDATE_M = """mutation($input: CollectionInput!) { collectionUpdate(input: $input) {
  collection { id handle seo { title description } } userErrors { field message } } }"""
COLLECTION_PRODUCTS_Q = """query($id: ID!, $cursor: String) { collection(id: $id) { products(first: 250, after: $cursor) {
  nodes { handle } pageInfo { hasNextPage endCursor } } } }"""
ARTICLE_BY_HANDLE_Q = """query($q: String!) { articles(first: 5, query: $q) { nodes { id handle title isPublished
  seoTitle: metafield(namespace: "global", key: "title_tag") { value }
  seoDesc: metafield(namespace: "global", key: "description_tag") { value } } } }"""
ARTICLE_UPDATE_M = """mutation($id: ID!, $article: ArticleUpdateInput!) { articleUpdate(id: $id, article: $article) {
  article { id handle } userErrors { field message } } }"""
ARTICLE_BODIES_Q = """query($cursor: String) { articles(first: 50, after: $cursor, query: "published_status:published") {
  nodes { id handle title body } pageInfo { hasNextPage endCursor } } }"""
ACTIVE_PRODUCTS_Q = """query($cursor: String) { products(first: 250, after: $cursor, query: "status:active") {
  nodes { handle onlineStoreUrl } pageInfo { hasNextPage endCursor } } }"""
ARTICLE_BODY_Q = """query($q: String!) { articles(first: 5, query: $q) { nodes { id handle isPublished body } } }"""
SHOP_LOCALES_Q = "{ shopLocales { locale primary published } }"
TRANSLATABLE_Q = """query($id: ID!, $l: String!) { translatableResource(resourceId: $id) {
  translatableContent { key value digest locale } translations(locale: $l) { key value outdated } } }"""
TRANSLATIONS_REGISTER_M = """mutation($id: ID!, $t: [TranslationInput!]!) { translationsRegister(resourceId: $id, translations: $t) {
  userErrors { field message } translations { key locale } } }"""
# Highest-click storefront languages first (GSC, 2026-09-29: el, da, no, nl, he lead; then it, cs, ro, pl).
LOCALE_PRIORITY = ["el", "da", "no", "nl", "he", "it", "cs", "ro", "pl", "de", "fr", "es", "pt-BR", "sv", "fi", "ja", "ko", "ru", "ar", "hi"]
TRANSLATE_KEYS = ("title", "body_html", "summary_html", "meta_title", "meta_description")
REDIRECTS_Q = """query($q: String!) { urlRedirects(first: 10, query: $q) { nodes { id path target } } }"""
REDIRECT_CREATE_M = """mutation($r: UrlRedirectInput!) { urlRedirectCreate(urlRedirect: $r) {
  urlRedirect { id path target } userErrors { field message } } }"""


def text_of(html_text: str) -> str:
    stripped = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html_text or "", flags=re.S | re.I)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", stripped))).strip()


def live_product_handles(admin: "Admin") -> set:
    return {p["handle"] for p in admin.paged(ACTIVE_PRODUCTS_Q, "products") if p["onlineStoreUrl"]}


def live_counts(admin: "Admin", collections: List[Dict], live_products: set) -> Dict[str, int]:
    """Products a shopper can actually see: active and on the online store (admin productsCount includes drafts/archived)."""
    counts = {}
    for c in collections:
        handles, cursor = [], None
        while True:
            data = admin.gql(COLLECTION_PRODUCTS_Q, {"id": c["id"], "cursor": cursor})["collection"]["products"]
            handles += [n["handle"] for n in data["nodes"]]
            if not data["pageInfo"]["hasNextPage"]:
                break
            cursor = data["pageInfo"]["endCursor"]
        counts[c["handle"]] = sum(1 for h in handles if h in live_products)
    return counts


def cmd_inventory(args) -> int:
    admin = Admin(args.store_domain)
    collections = admin.paged(COLLECTIONS_Q, "collections")
    counts = live_counts(admin, collections, live_product_handles(admin))
    articles = admin.paged(ARTICLES_Q, "articles")
    payload = {
        "generated_at": now_stamp(),
        "collections": [
            {
                "handle": c["handle"], "title": c["title"], "products": counts[c["handle"]], "products_admin": c["productsCount"]["count"],
                "smart": c["ruleSet"] is not None, "theme_owned": c["handle"] in THEME_OWNED_COLLECTIONS,
                "seo_title": c["seo"]["title"], "seo_description": c["seo"]["description"],
                "description_words": len(text_of(c["descriptionHtml"]).split()), "updated_at": c["updatedAt"],
            }
            for c in collections
        ],
        "articles": [
            {
                "handle": a["handle"], "blog": a["blog"]["handle"], "title": a["title"],
                "published": a["isPublished"], "published_at": a["publishedAt"], "updated_at": a["updatedAt"],
                "tags": a["tags"], "seo_title": (a["seoTitle"] or {}).get("value"),
                "seo_description": (a["seoDesc"] or {}).get("value"),
            }
            for a in articles
        ],
    }
    write_json(args.output, payload)
    summary_path = Path(args.output).with_suffix(".md")
    lines = [f"# Inventory {payload['generated_at']}", "", "## Collections (handle | live products | theme_owned | seo_title chars | seo_description chars)"]
    for c in sorted(payload["collections"], key=lambda c: -c["products"]):
        lines.append(f"- {c['handle']} | {c['products']} | {'T' if c['theme_owned'] else '-'} | {len(c['seo_title'] or '')} | {len(c['seo_description'] or '')}")
    published = [a for a in payload["articles"] if a["published"]]
    lines += ["", f"## Published articles ({len(published)}; {len(payload['articles']) - len(published)} unpublished not listed) (handle | seo_title? | seo_description? | title)"]
    for a in sorted(published, key=lambda a: a["published_at"] or ""):
        lines.append(f"- {a['handle']} | {'Y' if a['seo_title'] else 'N'} | {'Y' if a['seo_description'] else 'N'} | {a['title']}")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"collections={len(payload['collections'])} articles={len(payload['articles'])} -> {args.output}; summary -> {summary_path}")
    return 0


def fetch(url: str) -> Dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"status": response.status, "final_url": response.geturl(), "html": response.read().decode("utf-8", "replace")}
    except urllib.error.HTTPError as error:
        return {"status": error.code, "final_url": url, "html": ""}


def page_signals(url: str, page: Dict) -> Dict:
    doc = page["html"]

    def first(pattern: str) -> Optional[str]:
        match = re.search(pattern, doc, re.I | re.S)
        return html.unescape(match.group(1).strip()) if match else None

    main = re.search(r"<main[^>]*>(.*?)</main>", doc, re.I | re.S)
    body_text = text_of(main.group(1) if main else doc)
    internal = set(re.findall(r'href="(/(?:[a-z]{2}(?:-[a-z]{2})?/)?(?:collections|products|blogs|pages)/[^"#?]+)', doc))
    return {
        "url": url, "status": page["status"], "final_url": page["final_url"],
        "title": first(r"<title[^>]*>(.*?)</title>"),
        "meta_description": first(r'<meta[^>]+name="description"[^>]+content="([^"]*)"'),
        "canonical": first(r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"'),
        "robots": first(r'<meta[^>]+name="robots"[^>]+content="([^"]*)"'),
        "h1_count": len(re.findall(r"<h1[\s>]", doc, re.I)),
        "h1": first(r"<h1[^>]*>(.*?)</h1>") and text_of(first(r"<h1[^>]*>(.*?)</h1>")),
        "hreflang_count": len(re.findall(r'hreflang="', doc)),
        "main_words": len(body_text.split()),
        "internal_links": len(internal),
        "jsonld_types": sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', doc))),
        "banned_claims": sorted({m.group(0).lower() for m in BANNED_RE.finditer(body_text)}),
    }


def cmd_check(args) -> int:
    results = []
    for index, url in enumerate(args.url):
        if index:
            time.sleep(args.pause)
        full = url if url.startswith("http") else STOREFRONT + url
        results.append(page_signals(full, fetch(full)))
    write_json(args.output, {"checked_at": now_stamp(), "pages": results})
    for r in results:
        print(f"{r['status']} {r['url']} h1={r['h1_count']} words={r['main_words']} links={r['internal_links']} robots={r['robots']}")
    return 0


def parse_article(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8").strip()
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return {"meta": meta, "body": body.strip()}


def lint_article(path: Path, inventory: Optional[Dict]) -> Dict:
    article = parse_article(path)
    meta, body = article["meta"], article["body"]
    words = len(text_of(body).split())
    links = re.findall(r'href="([^"]+)"', body)
    collection_links = sorted({l.split("?")[0].rstrip("/").split("/collections/")[1] for l in links if "/collections/" in l})
    external = [l for l in links if l.startswith("http") and "dresslikemommy.com" not in l]
    errors, warnings = [], []
    for field in ("title", "handle", "summary", "seo_title", "seo_description", "tags"):
        if not meta.get(field):
            errors.append(f"missing frontmatter {field}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta.get("handle", "")):
        errors.append("handle must be lowercase-hyphenated")
    if len(meta.get("seo_title", "")) > 65:
        errors.append(f"seo_title {len(meta['seo_title'])} chars > 65")
    if not 110 <= len(meta.get("seo_description", "")) <= 160:
        errors.append(f"seo_description {len(meta.get('seo_description', ''))} chars not in 110-160")
    if words < 700:
        errors.append(f"body {words} words < 700")
    if len(collection_links) < 3:
        errors.append(f"only {len(collection_links)} distinct /collections/ links (need >= 3)")
    if external:
        errors.append(f"external links not allowed: {external[:3]}")
    if re.search(r"<h1[\s>]", body, re.I):
        errors.append("body must not contain <h1> (the theme renders the title as H1)")
    if len(re.findall(r"<h2[\s>]", body, re.I)) < 3:
        warnings.append("fewer than 3 <h2> sections")
    banned = sorted({m.group(0).lower() for m in BANNED_RE.finditer(text_of(body) + " " + " ".join(meta.values()))})
    if banned:
        errors.append(f"unsupported/banned claims: {banned}")
    if inventory:
        live = {c["handle"]: c["products"] for c in inventory.get("collections", [])}
        for handle in collection_links:
            if handle not in live:
                errors.append(f"links to missing collection /collections/{handle}")
            elif live[handle] < 3:
                errors.append(f"links to thin collection /collections/{handle} ({live[handle]} products)")
        taken = {a["handle"] for a in inventory.get("articles", [])}
        if meta.get("handle") in taken:
            warnings.append("handle already exists live: publishing will skip unless --update-existing")
    return {"file": str(path), "words": words, "collection_links": collection_links, "errors": errors, "warnings": warnings, "pass": not errors}


def cmd_lint_article(args) -> int:
    inventory = json.loads(Path(args.inventory).read_text()) if args.inventory else None
    results = [lint_article(Path(f), inventory) for f in args.file]
    print(json.dumps(results, indent=2))
    return 0 if all(r["pass"] for r in results) else 1


def check_meta(title: Optional[str], description: Optional[str]) -> List[str]:
    problems = []
    if title is not None and not 20 <= len(title) <= 65:
        problems.append(f"seo title {len(title)} chars not in 20-65")
    if description is not None and not 110 <= len(description) <= 160:
        problems.append(f"seo description {len(description)} chars not in 110-160")
    banned = sorted({m.group(0).lower() for m in BANNED_RE.finditer(f"{title or ''} {description or ''}")})
    if banned:
        problems.append(f"banned claims: {banned}")
    return problems


def cmd_collection_seo(args) -> int:
    if args.handle in THEME_OWNED_COLLECTIONS:
        print(f"REFUSED: {args.handle} copy is theme-owned; change snippets/collection-seo-fallback.liquid in a main session.")
        return 2
    problems = check_meta(args.seo_title, args.seo_description)
    admin = Admin(args.store_domain)
    before = admin.gql(COLLECTION_BY_HANDLE_Q, {"handle": args.handle})["collectionByHandle"]
    if not before:
        problems.append(f"collection {args.handle} not found")
    else:
        live = live_counts(admin, [before], live_product_handles(admin))[args.handle]
        if live < 3:
            problems.append(f"collection shows {live} live products (theme noindexes <3); fix the catalog before SEO")
    receipt = {"at": now_stamp(), "handle": args.handle, "before": before, "requested": {"title": args.seo_title, "description": args.seo_description}, "problems": problems, "executed": False}
    if problems or not args.execute:
        write_json(args.receipt, receipt)
        print(json.dumps(receipt, indent=2))
        return 1 if problems else 0
    seo = {"title": args.seo_title if args.seo_title is not None else before["seo"]["title"],
           "description": args.seo_description if args.seo_description is not None else before["seo"]["description"]}
    result = admin.gql(COLLECTION_UPDATE_M, {"input": {"id": before["id"], "seo": seo}})["collectionUpdate"]
    after = admin.gql(COLLECTION_BY_HANDLE_Q, {"handle": args.handle})["collectionByHandle"]
    receipt.update(executed=True, user_errors=result["userErrors"], after=after, verified=after["seo"] == seo,
                   rollback={"title": before["seo"]["title"], "description": before["seo"]["description"]})
    write_json(args.receipt, receipt)
    print(json.dumps({k: receipt[k] for k in ("handle", "user_errors", "verified")}, indent=2))
    return 0 if receipt["verified"] and not result["userErrors"] else 1


def find_article(admin: Admin, handle: str) -> Optional[Dict]:
    nodes = admin.gql(ARTICLE_BY_HANDLE_Q, {"q": f"handle:{handle}"})["articles"]["nodes"]
    return next((n for n in nodes if n["handle"] == handle), None)


def cmd_article_seo(args) -> int:
    problems = check_meta(args.seo_title, args.seo_description)
    admin = Admin(args.store_domain)
    before = find_article(admin, args.handle)
    if not before:
        problems.append(f"article {args.handle} not found")
    elif not before["isPublished"]:
        problems.append("article is unpublished; SEO edits only on live articles")
    receipt = {"at": now_stamp(), "handle": args.handle, "before": before, "requested": {"title": args.seo_title, "description": args.seo_description}, "problems": problems, "executed": False}
    if problems or not args.execute:
        write_json(args.receipt, receipt)
        print(json.dumps(receipt, indent=2))
        return 1 if problems else 0
    fields = [("title_tag", args.seo_title), ("description_tag", args.seo_description)]
    metafields = [{"namespace": "global", "key": k, "type": "single_line_text_field", "value": v} for k, v in fields if v]
    result = admin.gql(ARTICLE_UPDATE_M, {"id": before["id"], "article": {"metafields": metafields}})["articleUpdate"]
    after = find_article(admin, args.handle)
    verified = all((after["seoTitle" if k == "title_tag" else "seoDesc"] or {}).get("value") == v for k, v in fields if v)
    receipt.update(executed=True, user_errors=result["userErrors"], after=after, verified=verified,
                   rollback={"title_tag": (before["seoTitle"] or {}).get("value"), "description_tag": (before["seoDesc"] or {}).get("value")})
    write_json(args.receipt, receipt)
    print(json.dumps({k: receipt[k] for k in ("handle", "user_errors", "verified")}, indent=2))
    return 0 if verified and not result["userErrors"] else 1


PRODUCT_LINK_RE = re.compile(r'href="(?:https?://(?:www\.)?dresslikemommy\.com)?(?:/[a-z]{2}(?:-[a-z]{2})?)?/(?:collections/[^/"]+/)?products/([^"/?#]+)')
COLLECTION_LINK_RE = re.compile(r'href="(?:https?://(?:www\.)?dresslikemommy\.com)?(?:/[a-z]{2}(?:-[a-z]{2})?)?/collections/([^"/?#]+)"')


def link_health(body: str, live_products: set, live_collections: set) -> Dict:
    products = PRODUCT_LINK_RE.findall(body or "")
    collections = COLLECTION_LINK_RE.findall(body or "")
    return {
        "dead_products": sorted({h for h in products if h not in live_products}),
        "dead_collections": sorted({h for h in collections if h not in live_collections}),
        "banned_claims": sorted({m.group(0).lower() for m in BANNED_RE.finditer(text_of(body))}),
    }


def live_sets(admin: Admin):
    products = live_product_handles(admin)
    collections = admin.paged(COLLECTIONS_Q, "collections")
    counts = live_counts(admin, collections, products)
    return products, {h for h, n in counts.items() if n >= 3} | {"all"}


def cmd_article_links(args) -> int:
    admin = Admin(args.store_domain)
    live_products, live_collections = live_sets(admin)
    rows = []
    for article in admin.paged(ARTICLE_BODIES_Q, "articles"):
        health = link_health(article["body"], live_products, live_collections)
        if any(health.values()):
            rows.append({"handle": article["handle"], "title": article["title"], **health})
            if args.bodies_dir:
                out = Path(args.bodies_dir) / f"{article['handle']}.html"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(article["body"], encoding="utf-8")
    rows.sort(key=lambda r: -(len(r["dead_products"]) + len(r["dead_collections"]) + len(r["banned_claims"])))
    write_json(args.output, {"at": now_stamp(), "articles_needing_fix": len(rows), "rows": rows})
    print(f"articles needing fix: {len(rows)} -> {args.output}")
    return 0


def cmd_article_body(args) -> int:
    admin = Admin(args.store_domain)
    nodes = admin.gql(ARTICLE_BODY_Q, {"q": f"handle:{args.handle}"})["articles"]["nodes"]
    before = next((n for n in nodes if n["handle"] == args.handle), None)
    new_body = Path(args.body_file).read_text(encoding="utf-8").strip()
    problems = []
    if not before:
        problems.append(f"article {args.handle} not found")
    elif not before["isPublished"]:
        problems.append("article is unpublished; body edits only on live articles")
    else:
        live_products, live_collections = live_sets(admin)
        health = link_health(new_body, live_products, live_collections)
        problems += [f"{k}: {v}" for k, v in health.items() if v]
        old_words, new_words = len(text_of(before["body"]).split()), len(text_of(new_body).split())
        if new_words < old_words * 0.85:
            problems.append(f"body shrinks {old_words}->{new_words} words (>15%)")
        if re.search(r"<h1[\s>]", new_body, re.I):
            problems.append("body must not contain <h1>")
        if re.search(r'href="https?://(?!(?:www\.)?dresslikemommy\.com)', new_body):
            problems.append("external links not allowed")
    receipt = {"at": now_stamp(), "handle": args.handle, "problems": problems, "executed": False,
               "before_body": before and before["body"]}
    if problems or not args.execute:
        write_json(args.receipt, receipt)
        print(json.dumps({k: receipt[k] for k in ("handle", "problems", "executed")}, indent=2))
        return 1 if problems else 0
    result = admin.gql(ARTICLE_UPDATE_M, {"id": before["id"], "article": {"body": new_body}})["articleUpdate"]
    after = admin.gql(ARTICLE_BODY_Q, {"q": f"handle:{args.handle}"})["articles"]["nodes"]
    after_body = next((n["body"] for n in after if n["handle"] == args.handle), "")
    verified = text_of(after_body) == text_of(new_body)
    receipt.update(executed=True, user_errors=result["userErrors"], verified=verified,
                   rollback="article-body with before_body from this receipt")
    write_json(args.receipt, receipt)
    print(json.dumps({k: receipt[k] for k in ("handle", "user_errors", "verified")}, indent=2))
    return 0 if verified and not result["userErrors"] else 1


def locale_prefix(locale: str) -> str:
    """Storefront URL folder for a locale (Shopify serves pt-BR at /pt)."""
    return "/" + ("pt" if locale == "pt-BR" else locale.lower())


def localize_hrefs(body: str, locale: str) -> str:
    return re.sub(r'href="/(collections|products|blogs|pages)/', lambda m: f'href="{locale_prefix(locale)}/{m.group(1)}/', body)


def article_translation_state(admin: "Admin", handle: str, kind: str = "article", keys=TRANSLATE_KEYS):
    if kind == "collection":
        article = admin.gql(COLLECTION_BY_HANDLE_Q, {"handle": handle})["collectionByHandle"]
    else:
        article = find_article(admin, handle)
    if not article:
        raise SystemExit(f"{kind} {handle} not found")
    locales = [l["locale"] for l in admin.gql(SHOP_LOCALES_Q)["shopLocales"] if l["published"] and not l["primary"]]
    locales.sort(key=lambda l: LOCALE_PRIORITY.index(l) if l in LOCALE_PRIORITY else 99)
    source, status = {}, {}
    for locale in locales:
        res = admin.gql(TRANSLATABLE_Q, {"id": article["id"], "l": locale})["translatableResource"]
        source = {c["key"]: c for c in res["translatableContent"] if c["key"] in keys and (c["value"] or "").strip()}
        done = {t["key"]: t for t in res["translations"]}
        status[locale] = [k for k in source if k not in done or done[k]["outdated"] or not (done[k]["value"] or "").strip()]
    return article, source, status


def resource_args(args):
    if getattr(args, "collection", False):
        return "collection", tuple(k.strip() for k in args.keys.split(",")) if args.keys else ("meta_title", "meta_description")
    return "article", TRANSLATE_KEYS


def cmd_translate_queue(args) -> int:
    admin = Admin(args.store_domain)
    article, source, status = article_translation_state(admin, args.handle, *resource_args(args))
    todo = {l: keys for l, keys in status.items() if keys}
    payload = {"handle": args.handle, "article_id": article["id"],
               "source": {k: v["value"] for k, v in source.items()},
               "locales_needing_work": todo,
               "link_rule": "in body_html, prefix every internal href with the locale folder: /collections/x -> /<prefix>/collections/x",
               "locale_prefixes": {l: locale_prefix(l) for l in todo}}
    write_json(args.output, payload)
    print(f"{args.handle}: {len(todo)} of {len(status)} locales need work -> {args.output}")
    return 0


def translation_priority() -> List[str]:
    """Engine-built articles first, then articles whose English body was repaired (their translations are stale)."""
    log = (ROOT / "ops/organic/ENGINE_LOG.md").read_text(encoding="utf-8") if (ROOT / "ops/organic/ENGINE_LOG.md").exists() else ""
    built = re.findall(r"/blogs/news/([a-z0-9-]+)", "\n".join(l for l in log.splitlines() if l.startswith("- Build:")))
    repaired = sorted({p.stem[len("body-"):] for p in (ROOT / "ops/organic/receipts").rglob("body-*.json")})
    order = []
    for handle in built + repaired:
        if handle not in order:
            order.append(handle)
    return order


def cmd_translate_next(args) -> int:
    admin = Admin(args.store_domain)
    for handle in translation_priority():
        article = find_article(admin, handle)
        if not article or not article["isPublished"]:
            continue
        _, source, status = article_translation_state(admin, handle)
        todo = {l: keys for l, keys in status.items() if keys}
        if not todo:
            continue
        picked = dict(list(todo.items())[: args.max_locales])
        payload = {"handle": handle, "article_id": article["id"], "source": {k: v["value"] for k, v in source.items()},
                   "locales_this_run": picked, "locales_left_after_this_run": len(todo) - len(picked),
                   "locale_prefixes": {l: locale_prefix(l) for l in picked},
                   "link_rule": "in body_html, prefix every internal href with the locale folder: /collections/x -> /<prefix>/collections/x"}
        write_json(args.output, payload)
        print(f"{handle}: {len(picked)} locales this run ({', '.join(picked)}); {len(todo) - len(picked)} left -> {args.output}")
        return 0
    print("nothing to translate: every engine-built and repaired article is current in all languages")
    write_json(args.output, {"handle": None})
    return 0


def check_translation(key: str, src: str, value: str, locale: str) -> List[str]:
    problems = []
    if not value.strip():
        return ["empty"]
    ratio = len(value) / max(len(src), 1)
    if not 0.4 <= ratio <= 2.6:
        problems.append(f"length ratio {ratio:.2f} looks wrong")
    if key == "meta_title" and len(value) > 70:
        problems.append(f"meta_title {len(value)} chars > 70")
    if key == "meta_description" and len(value) > 165:
        problems.append(f"meta_description {len(value)} chars > 165")
    if key == "body_html":
        for tag in ("h2", "h3", "p", "li", "a"):
            a, b = len(re.findall(rf"<{tag}[\s>]", src, re.I)), len(re.findall(rf"<{tag}[\s>]", value, re.I))
            if a != b:
                problems.append(f"<{tag}> count {b} != source {a}")
        expected = sorted(re.findall(r'href="([^"]+)"', localize_hrefs(src, locale)))
        got = sorted(re.findall(r'href="([^"]+)"', value))
        if expected != got:
            problems.append(f"hrefs differ from localized source (expected e.g. {expected[:2]})")
    if len(re.findall(r"\b(the|and|with|for|your)\b", text_of(value), re.I)) > 6 and locale not in ("en",):
        problems.append("looks untranslated (many English words)")
    return problems


def cmd_translate_apply(args) -> int:
    admin = Admin(args.store_domain)
    article, source, status = article_translation_state(admin, args.handle, *resource_args(args))
    wanted = json.loads(Path(args.translations).read_text(encoding="utf-8"))
    rows, problems = [], []
    for locale, fields in wanted.items():
        if locale not in status:
            problems.append(f"{locale}: not a published storefront language")
            continue
        for key, value in fields.items():
            if key not in source:
                problems.append(f"{locale}.{key}: not a translatable field of this article")
                continue
            issues = check_translation(key, source[key]["value"], value, locale)
            if issues:
                problems.append(f"{locale}.{key}: " + "; ".join(issues))
            rows.append({"locale": locale, "key": key, "value": value, "translatableContentDigest": source[key]["digest"]})
    receipt = {"at": now_stamp(), "handle": args.handle, "rows": len(rows), "problems": problems, "executed": False}
    if problems or not args.execute:
        write_json(args.receipt, receipt)
        print(json.dumps(receipt, indent=2, ensure_ascii=False)[:3000])
        return 1 if problems else 0
    errors = []
    for locale in sorted({r["locale"] for r in rows}):
        batch = [{k: r[k] for k in ("locale", "key", "value", "translatableContentDigest")} for r in rows if r["locale"] == locale]
        result = admin.gql(TRANSLATIONS_REGISTER_M, {"id": article["id"], "t": batch})["translationsRegister"]
        errors += result["userErrors"]
    _, _, after = article_translation_state(admin, args.handle, *resource_args(args))
    unresolved = {l: [k for k in wanted[l] if k in after.get(l, [])] for l in wanted}
    verified = not errors and not any(unresolved.values())
    receipt.update(executed=True, user_errors=errors, unresolved_after=unresolved, verified=verified)
    write_json(args.receipt, receipt)
    print(json.dumps({k: receipt[k] for k in ("handle", "rows", "user_errors", "unresolved_after", "verified")}, indent=2))
    return 0 if verified else 1


def cmd_redirect(args) -> int:
    source, target = args.source.strip(), args.target.strip()
    problems = []
    if not source.startswith("/") or not target.startswith("/"):
        problems.append("source and target must be store-relative paths starting with /")
    source_page = fetch(STOREFRONT + source)
    time.sleep(1.5)
    target_page = fetch(STOREFRONT + target)
    if source_page["status"] == 200 and source_page["final_url"].rstrip("/").endswith(source.rstrip("/")):
        problems.append(f"source {source} is live (200); redirects only recover dead URLs")
    if target_page["status"] != 200:
        problems.append(f"target {target} returned {target_page['status']}")
    admin = Admin(args.store_domain)
    existing = admin.gql(REDIRECTS_Q, {"q": f"path:{source}"})["urlRedirects"]["nodes"]
    if any(r["path"].rstrip("/") == source.rstrip("/") for r in existing):
        problems.append(f"redirect already exists: {existing}")
    receipt = {"at": now_stamp(), "source": source, "target": target, "source_status": source_page["status"], "target_status": target_page["status"], "problems": problems, "executed": False}
    if problems or not args.execute:
        write_json(args.receipt, receipt)
        print(json.dumps(receipt, indent=2))
        return 1 if problems else 0
    result = admin.gql(REDIRECT_CREATE_M, {"r": {"path": source, "target": target}})["urlRedirectCreate"]
    receipt.update(executed=True, user_errors=result["userErrors"], created=result["urlRedirect"],
                   rollback="urlRedirectDelete(id) on the created id")
    write_json(args.receipt, receipt)
    print(json.dumps({k: receipt[k] for k in ("source", "target", "user_errors", "created")}, indent=2))
    return 0 if result["urlRedirect"] and not result["userErrors"] else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--store-domain", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inventory")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_inventory)

    p = sub.add_parser("check")
    p.add_argument("--url", action="append", required=True, help="absolute URL or store path; repeatable (max 12)")
    p.add_argument("--pause", type=float, default=3.0)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("lint-article")
    p.add_argument("--file", action="append", required=True)
    p.add_argument("--inventory", default="")
    p.set_defaults(func=cmd_lint_article)

    p = sub.add_parser("collection-seo")
    p.add_argument("--handle", required=True)
    p.add_argument("--seo-title")
    p.add_argument("--seo-description")
    p.add_argument("--receipt", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_collection_seo)

    p = sub.add_parser("redirect")
    p.add_argument("--from", dest="source", required=True)
    p.add_argument("--to", dest="target", required=True)
    p.add_argument("--receipt", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_redirect)

    p = sub.add_parser("translate-queue")
    p.add_argument("--handle", required=True)
    p.add_argument("--collection", action="store_true", help="translate a collection (default fields: meta_title, meta_description)")
    p.add_argument("--keys", default="", help="with --collection: comma-separated fields, e.g. meta_title,meta_description,title")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_translate_queue)

    p = sub.add_parser("translate-next")
    p.add_argument("--max-locales", type=int, default=6)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_translate_next)

    p = sub.add_parser("translate-apply")
    p.add_argument("--handle", required=True)
    p.add_argument("--collection", action="store_true", help="translate a collection (default fields: meta_title, meta_description)")
    p.add_argument("--keys", default="", help="with --collection: comma-separated fields, e.g. meta_title,meta_description,title")
    p.add_argument("--translations", required=True, help='JSON {"<locale>": {"<key>": "<translated value>"}}')
    p.add_argument("--receipt", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_translate_apply)

    p = sub.add_parser("article-seo")
    p.add_argument("--handle", required=True)
    p.add_argument("--seo-title")
    p.add_argument("--seo-description")
    p.add_argument("--receipt", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_article_seo)

    p = sub.add_parser("article-links")
    p.add_argument("--output", required=True)
    p.add_argument("--bodies-dir", default="", help="also save each flagged article's current body here")
    p.set_defaults(func=cmd_article_links)

    p = sub.add_parser("article-body")
    p.add_argument("--handle", required=True)
    p.add_argument("--body-file", required=True, help="file holding the complete new body HTML")
    p.add_argument("--receipt", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_article_body)

    args = parser.parse_args(argv)
    if args.command == "check" and len(args.url) > 12:
        parser.error("check accepts at most 12 URLs per run (storefront rate limit)")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
