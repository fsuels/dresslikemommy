"""Read-only, unauthenticated public GET landing evidence; no browser/cookie writes."""
import concurrent.futures
import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

OUT = Path(__file__).resolve().parent
PAYLOAD = json.loads((OUT / 'payload.json').read_text())


def text_only(markup):
    markup = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', markup, flags=re.S | re.I)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', markup)).split())


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.canonical = None
        self.portuguese_alternates = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        elif tag == 'link':
            if attrs.get('rel') == 'canonical':
                self.canonical = attrs.get('href')
            if attrs.get('rel') == 'alternate' and attrs.get('hreflang', '').startswith('pt'):
                self.portuguese_alternates.append({'hreflang': attrs.get('hreflang'), 'href': attrs.get('href')})


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.redirects = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects.append({'from': req.full_url, 'status': code, 'to': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(group):
    redirect = RedirectRecorder()
    opener = urllib.request.build_opener(redirect)
    url = group['final_url']
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = {'group': group['number'], 'group_name': group['name'], 'requested_url': url, 'started_at_utc': started}
    try:
        with opener.open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            raw = response.read()
            source = raw.decode('utf-8')
            result.update({'http_status': response.status, 'final_url': response.url, 'redirects': redirect.redirects, 'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw)})
        parser = MetadataParser()
        parser.feed(source)
        main_match = re.search(r'<main\b[^>]*>(.*?)</main>', source, flags=re.S | re.I)
        assert main_match, 'No main element found'
        main = main_match[1]
        main_text = text_only(main)
        h1 = [text_only(s) for s in re.findall(r'<h1\b[^>]*>(.*?)</h1>', main, flags=re.S | re.I)]
        h3 = [text_only(s) for s in re.findall(r'<h3\b[^>]*>(.*?)</h3>', main, flags=re.S | re.I)]
        links = [html.unescape(s) for s in re.findall(r'<a\b[^>]*href="([^"]*/products/[^"#]+)"', main, flags=re.S | re.I)]
        handles = sorted(set(re.search(r'/products/([^/?#]+)', s)[1] for s in links))
        result.update({'html_lang': parser.lang, 'canonical_url': parser.canonical, 'portuguese_alternate_links': parser.portuguese_alternates, 'main_h1': h1, 'main_h3_product_titles': h3, 'main_h3_unique_product_titles': list(dict.fromkeys(h3)), 'main_product_unique_handle_count': len(handles), 'main_product_handles': handles, 'main_text_prefix': main_text[:2400], 'not_found_marker': bool(re.search(r'Page Not Found|Página não encontrada', main_text, re.I)), 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
        (OUT / f"landing_group_{group['number']}_main.txt").write_text(main_text + '\n')
    except Exception as exc:
        result.update({'error_type': type(exc).__name__, 'error': str(exc), 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    return result


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, PAYLOAD['groups']))
output = {
    'artifact_type': 'PUBLIC_HTTP_SOURCE_READBACK_NOT_BROWSER_OR_CHECKOUT_RECEIPT',
    'browser_context': 'Subagent cua.getState exposed Chrome only; createBrowserTab(iab, visible=false) returned Browser is not available: iab. No existing browser tab was selected, changed or closed. Isolated public GET fallback communicated to parent.',
    'method': 'Fresh per-request urllib opener; no CookieJar, Cookie request header, auth, selectors, POST, cart or checkout. Parse server-rendered main text, H1, product H3 and unique product URL handles; repeated card links deduplicated by handle.',
    'limitations': 'HTTP source evidence cannot prove JavaScript-rendered browser behavior, selected Brazil/Portugal country/currency, all catalog pages, stock/paired sizes, shipping, mobile layout or checkout. Counts are first-page unique product handles, not verified availability.',
    'rows': rows,
}
(OUT / 'landing_readback.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps([{'group': r['group'], 'status': r.get('http_status'), 'final_url': r.get('final_url'), 'lang': r.get('html_lang'), 'h1': r.get('main_h1'), 'first_page_product_handles': r.get('main_product_unique_handle_count'), 'error': r.get('error')} for r in rows], ensure_ascii=False, indent=2))
