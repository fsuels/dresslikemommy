"""Bounded public HTTP SEO readback; no credentials, cookies, or writes to Shopify."""
import collections
import hashlib
import html.parser
import json
import pathlib
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE = 'https://www.dresslikemommy.com'
OUT = pathlib.Path(__file__).parent
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html,application/xml'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, r.url, r.read().decode('utf-8', errors='replace')

class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.title = []; self.h1 = []; self.head = []; self.text = []
        self.jsonld = []; self.script = None; self.depth = 0; self.in_head = False; self.in_title = False; self.in_h1 = False; self.in_main = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'head': self.in_head = True
        if tag == 'title' and self.in_head: self.in_title = True
        if tag == 'h1': self.in_h1 = True
        if tag == 'main': self.in_main = True
        if tag == 'link' and a.get('rel') in ('canonical', 'alternate'): self.head.append(a)
        if tag == 'meta' and a.get('name') in ('robots', 'description'): self.head.append(a)
        if tag in ('script', 'style'): self.depth += 1
        if tag == 'script' and a.get('type') == 'application/ld+json': self.script = []
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'head': self.in_head = False
        if tag == 'h1': self.in_h1 = False
        if tag == 'main': self.in_main = False
        if tag == 'script' and self.script is not None:
            try: self.jsonld.append(json.loads(''.join(self.script)))
            except ValueError: self.jsonld.append({'parse_error': True})
            self.script = None
        if tag in ('script', 'style'): self.depth = max(0, self.depth - 1)
    def handle_data(self, data):
        if self.script is not None: self.script.append(data)
        if self.depth: return
        if self.in_title: self.title.append(data)
        if self.in_h1: self.h1.append(data.strip())
        if self.in_main and data.strip(): self.text.append(data.strip())

def schema_summary(obj):
    result = []
    if isinstance(obj, dict):
        if '@type' in obj:
            fields = ['@type', 'name', 'price', 'lowPrice', 'highPrice', 'priceCurrency', 'availability', 'reviewCount', 'ratingValue', 'merchantReturnDays', 'returnFees']
            result.append({k: obj[k] for k in fields if k in obj and not isinstance(obj[k], (list, dict))})
        for v in obj.values(): result.extend(schema_summary(v))
    elif isinstance(obj, list):
        for v in obj: result.extend(schema_summary(v))
    return result

report = {'as_of_utc': datetime.now(timezone.utc).isoformat(), 'method': 'Public GET without cookies. Sample only; no full product crawl. Raw HTML retained only as SHA256; source URLs and public tracking code omitted.', 'routes': [], 'sitemaps': []}
status, final, robots = get(BASE + '/robots.txt')
report['robots'] = {'status': status, 'bytes': len(robots), 'rules': [l for l in robots.splitlines() if re.match(r'(User-agent|Allow|Disallow|Sitemap):', l)]}
status, final, xml = get(BASE + '/sitemap.xml')
locations = [e.text for e in ET.fromstring(xml).findall('s:sitemap/s:loc', NS)]
report['sitemap_index'] = {'status': status, 'child_count': len(locations), 'locale_prefixes': sorted({urllib.parse.urlparse(u).path.split('/')[1] for u in locations if not urllib.parse.urlparse(u).path.startswith('/sitemap')})}
for url in locations:
    if urllib.parse.urlparse(url).path.startswith('/sitemap_') and 'agentic' not in url:
        s, f, body = get(url)
        entries = ET.fromstring(body).findall('s:url/s:loc', NS)
        report['sitemaps'].append({'url': url, 'status': s, 'url_count': len(entries), 'sample_urls': [e.text for e in entries[:3]]})

paths = ['/', '/collections/mommy-and-me', '/collections/new-women-outfits', '/collections/dresses', '/collections/swimsuits', '/collections/family-swimsuits', '/collections/pajamas', '/products/golden-daisy-mommy-and-me-set', '/products/meow-star-garden-mommy-and-me-pajamas', '/products/navy-sprig-mommy-and-me-dresses', '/pages/shipping-info', '/pages/return-policy', '/policies/shipping-policy', '/policies/refund-policy']
for path in paths:
    try:
        s, f, body = get(BASE + path); p = Page(); p.feed(body)
        row = {'url': BASE + path, 'final_url': f, 'status': s, 'bytes': len(body), 'sha256': hashlib.sha256(body.encode()).hexdigest(), 'title': ''.join(p.title), 'h1': p.h1, 'head': p.head, 'schema': schema_summary(p.jsonld), 'source_domain_hits': len(re.findall(r'(?:1688|alibaba|aliexpress|taobao)\.(?:com|cn)', body, re.I)), 'url_brand_hits': len(re.findall(r'(?:data-analytics-vendor|data-item-brand)=[\"\']https?:',body,re.I)), 'main_text': '\n'.join(p.text)}
        row['main_text'] = re.sub(r'https?://[^\s<>]+', '[public URL omitted]', row['main_text'])
        theme = re.search(r'Shopify\.theme\s*=\s*(\{.*?\});', body)
        if theme:
            try: row['public_theme'] = json.loads(theme.group(1))
            except ValueError: pass
        row['vendor_caption_phrase_in_source'] = 'The vendor calls this' in body
        report['routes'].append(row)
        print(path, s, row['source_domain_hits'], ''.join(p.title), flush=True)
        if path == '/':
            for locale in ('es', 'fr', 'de'):
                alt = next((a['href'] for a in p.head if a.get('hreflang') == locale), None)
                if alt:
                    local_path = urllib.parse.urlparse(alt).path
                    if local_path not in paths: paths.append(local_path)
    except Exception as exc:
        report['routes'].append({'url': BASE + path, 'error': type(exc).__name__, 'message': str(exc)[:180]})
        if getattr(exc, 'code', None) == 429:
            report['stopped_reason'] = 'HTTP429: stopped public HTTP scan; do not rerun until rate limit is resolved.'
            break
OUT.joinpath('cro_public_readback.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('DONE', len(report['routes']), 'sample routes; sitemap inventories', len(report['sitemaps']))
