"""Read-only readback for the empty-cart picks row (lane C).

1. Simulates the Liquid selection in sections/main-cart-items.liquid (4 picks) and
   snippets/cart-drawer.liquid (3 picks): walk collections['new-arrivals'] in its
   configured sort order, skip unavailable products and products already in the cart.
2. Reads the live breadcrumb label for /collections/new-arrivals in every storefront
   language (the same locale key, sections.breadcrumbs.label_new_arrivals, is the new heading).
3. Confirms the theme locale files carry a non-English value for that key.
GET requests only; no cart writes.
"""
import glob
import html
import json
import re
import time
import urllib.request

BASE = 'https://www.dresslikemommy.com'
LANGS = ['en', 'es', 'fr', 'ar', 'nl', 'de', 'hi', 'it', 'ja', 'ko', 'pl', 'pt', 'ru', 'sv', 'da', 'no', 'el',
         'ro', 'fi', 'he', 'cs']
KEY = 'sections.breadcrumbs.label_new_arrivals'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 dlm-readonly-audit'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode('utf-8', 'replace')


def pick(products, limit, cart_ids=()):
    out = []
    for p in products:
        if len(out) >= limit:
            break
        if not any(v.get('available') for v in p['variants']):
            continue
        if p['id'] in cart_ids:
            continue
        out.append(p)
    return out


def load_locale(path):
    s = open(path, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/', '', s, flags=re.S))


def lookup(d, dotted):
    for part in dotted.split('.'):
        d = d.get(part) if isinstance(d, dict) else None
    return d


report = {}
products = json.loads(get(f'{BASE}/collections/new-arrivals/products.json?limit=50&_cb={int(time.time())}'))['products']
report['cart_page_picks'] = [(p['handle'], p['title'].split(' | ')[0], p['variants'][0]['price'], p['created_at'][:10])
                             for p in pick(products, 4)]
report['drawer_picks'] = [p['handle'] for p in pick(products, 3)]
report['drawer_picks_if_first_pick_in_cart'] = [p['handle'] for p in pick(products, 3, {products[0]['id']})]
report['unavailable_in_first_50'] = [p['handle'] for p in products
                                     if not any(v.get('available') for v in p['variants'])]

labels = {}
for lang in LANGS:
    prefix = '' if lang == 'en' else '/' + lang
    page = get(f'{BASE}{prefix}/collections/new-arrivals?_cb={int(time.time())}')
    m = re.search(r'<nav[^>]*breadcrumb[^>]*>(.*?)</nav>', page, flags=re.S | re.I)
    seg = html.unescape(re.sub(r'<[^>]+>', ' | ', m.group(1))) if m else ''
    labels[lang] = [t.strip() for t in seg.split('|') if t.strip()][-1:] if seg else None
report['live_breadcrumb_label'] = labels

files = sorted(f for f in glob.glob('locales/*.json') if 'schema' not in f)
en = lookup(load_locale('locales/en.default.json'), KEY)
report['locale_file_values'] = {f.split('/')[-1]: lookup(load_locale(f), KEY) for f in files}
report['locale_files_missing_or_english'] = [k for k, v in report['locale_file_values'].items()
                                            if k != 'en.default.json' and (not v or v == en)]
print(json.dumps(report, ensure_ascii=False, indent=1))
