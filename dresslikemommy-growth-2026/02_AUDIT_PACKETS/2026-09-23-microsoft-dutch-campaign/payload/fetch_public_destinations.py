"""Unauthenticated, read-only HTTP checks of exactly the eight supplied final URLs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import gzip
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
payload = json.loads((HERE / 'campaign_payload.json').read_text())

class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.captures = []
        self.done = []
        self.hidden = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag in ('script', 'style', 'noscript'):
            self.hidden += 1
        if tag in ('title', 'h1') or (tag == 'a' and '/products/' in a.get('href', '')) or a.get('id') in ('ProductCount', 'ProductCountDesktop'):
            self.captures.append({'tag': tag, 'attrs': a, 'parts': []})

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)
            for item in self.captures:
                item['parts'].append(data)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.hidden = max(0, self.hidden - 1)
        for i in range(len(self.captures)-1, -1, -1):
            if self.captures[i]['tag'] == tag:
                item = self.captures.pop(i)
                item['text'] = ' '.join(' '.join(item.pop('parts')).split())
                self.done.append(item)
                break

def fetch(g):
    out = {'group_number': g['number'], 'group_name': g['name'], 'requested_url': g['final_url'],
           'as_of_utc': datetime.now(timezone.utc).isoformat(), 'browser_rendered': False}
    try:
        with urlopen(Request(g['final_url'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=35) as r:
            body = r.read()
            out.update({'http_status': r.status, 'final_url': r.url, 'content_type': r.headers.get('Content-Type'),
                        'bytes': len(body), 'body_sha256': sha256(body).hexdigest()})
        raw_dir = HERE / 'public_html_evidence'
        raw_dir.mkdir(exist_ok=True)
        raw_path = raw_dir / f"group_{g['number']}.html.gz"
        raw_path.write_bytes(gzip.compress(body))
        out['raw_html_gzip'] = str(raw_path.relative_to(HERE))
        s = body.decode('utf-8')
        p = Extract(); p.feed(s)
        products = []
        seen = set()
        for a in p.done:
            if a['tag'] == 'a' and a['text'] and 'full-unstyled-link' in a['attrs'].get('class', ''):
                href = a['attrs']['href'].split('?')[0]
                if href not in seen:
                    seen.add(href)
                    products.append({'url_path': href, 'title': a['text']})
        country = re.search(r'Shopify\.country\s*=\s*(["\'])(.*?)\1', s)
        currency = re.search(r'Shopify\.currency\s*=\s*(\{[^;\n]+\})', s)
        out.update({'html_lang': p.lang, 'titles': [x['text'] for x in p.done if x['tag']=='title'],
                    'h1': [x['text'] for x in p.done if x['tag']=='h1'],
                    'product_count_labels': [x['text'] for x in p.done if x['attrs'].get('id') in ('ProductCount','ProductCountDesktop')],
                    'unique_rendered_card_links': len(products), 'products_on_returned_page': products,
                    'shopify_country_literal': country.group(2) if country else None,
                    'shopify_currency_literal': currency.group(1) if currency else None})
        text_lines = [x.strip() for x in p.text if x.strip()]
        out['sample_locale_terms_present'] = {x:any(x in line for line in text_lines) for x in ['Winkelwagen', 'Zoeken', 'Producten', 'Filteren', 'Toevoegen', 'Uitverkocht']}
    except Exception as e:
        out['error'] = {'type': type(e).__name__, 'message': str(e), 'http_status': getattr(e, 'code', None)}
    return out

with ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, payload['ad_groups']))
result = {'scope': 'exact_eight_public_final_urls_unauthenticated_http_only',
          'web_tool_result': 'All eight URLs not accessible via web tool; representative dresses retry same. No website status inferred from tool error.',
          'http_fallback': 'Python urllib, normal unauthenticated GET, TLS verification retained, max4 concurrent reads',
          'limitations': ['HTTP HTML only, not browser-rendered experience', 'No product-detail, variant, inventory, cart or checkout testing',
                          'Returned product cards do not establish whole assortment or availability', 'No campaign/account interaction'],
          'destinations': rows}
(HERE / 'public_destination_readback.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k in ('group_number','http_status','final_url','html_lang','h1','product_count_labels','unique_rendered_card_links','shopify_country_literal','shopify_currency_literal','error')}
                  for r in rows], ensure_ascii=False, indent=2))
