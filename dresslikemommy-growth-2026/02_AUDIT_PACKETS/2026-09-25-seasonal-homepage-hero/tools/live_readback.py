"""Read-only live readback of the seasonal hero on every storefront language."""
import html
import json
import re
import sys
import time
import urllib.request

BASE = 'https://www.dresslikemommy.com'
LANGS = {'en': '', 'es': '/es', 'fr': '/fr', 'ar': '/ar', 'nl': '/nl', 'de': '/de', 'hi': '/hi', 'it': '/it', 'ja': '/ja',
         'ko': '/ko', 'pl': '/pl', 'pt': '/pt', 'ru': '/ru', 'sv': '/sv', 'da': '/da', 'no': '/no', 'el': '/el',
         'ro': '/ro', 'fi': '/fi', 'he': '/he', 'cs': '/cs'}
EXPECT_PATHS = ['/collections/family-pajamas', '/collections/family-sweaters', '/collections/new-women-outfits']


def get(url, method='GET'):
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.status, (r.read().decode('utf-8', 'replace') if method == 'GET' else '')


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).split()


results, assets, problems = {}, set(), []
for lang, prefix in LANGS.items():
    status, page = get(f'{BASE}{prefix}/?_cb={int(time.time())}')
    i = page.find('class="hero-banner hero-banner--')
    seg = page[i:i + 60000] if i >= 0 else ''
    row = {'status': status, 'new_hero': i >= 0}
    if i < 0:
        problems.append(f'{lang}: new hero markup missing')
        results[lang] = row
        continue
    eyebrow = re.search(r'hero-banner__eyebrow">.*?<span>(.*?)</span>', seg, re.S)
    heading = re.search(r'class="hero-banner__heading">(.*?)</h[12]>', seg, re.S)
    ctas = re.findall(r'<a\s+href="([^"]+)"\s+class="hero-banner__cta[^"]*"[^>]*>(.*?)</a>', seg, re.S)
    slide_links = re.findall(r'<a\s+href="([^"]+)"\s+class="hero-banner__slide-link"\s+aria-label="([^"]*)"', seg)
    alts = re.findall(r'class="hero-banner__art"[\s\S]*?alt="([^"]*)"', seg)
    row.update({
        'eyebrow': html.unescape(eyebrow.group(1)) if eyebrow else None,
        'heading': ' '.join(text(heading.group(1))) if heading else None,
        'ctas': [(h, ' '.join(text(t))) for h, t in ctas],
        'slide_links': [(h, html.unescape(l)) for h, l in slide_links],
        'art_alts': [html.unescape(a)[:60] for a in alts],
        'liquid_error': 'Liquid error' in page,
    })
    for m in re.findall(r'(?:src|srcset)="([^"]*hero-(?:halloween|winter)-[^"]*)"', seg):
        for part in m.split(','):
            u = part.strip().split(' ')[0]
            if u:
                assets.add(('https:' + u) if u.startswith('//') else u)
    exp = [prefix + p for p in EXPECT_PATHS]
    if [h for h, _ in row['ctas']] != exp:
        problems.append(f'{lang}: CTA hrefs {[h for h, _ in row["ctas"]]} != {exp}')
    if [h for h, _ in row['slide_links']] != exp[:2]:
        problems.append(f'{lang}: slide links {row["slide_links"]}')
    if row['liquid_error']:
        problems.append(f'{lang}: Liquid error on page')
    if not row['eyebrow'] or not row['heading'] or len(row['ctas']) != 3:
        problems.append(f'{lang}: missing eyebrow/heading/CTAs')
    results[lang] = row
    time.sleep(0.3)

asset_status = {}
for u in sorted(assets):
    try:
        s, _ = get(u, 'HEAD')
    except Exception as e:  # noqa: BLE001
        s = str(e)
    asset_status[u.split('/')[-1].split('?')[0]] = s
    if s != 200:
        problems.append(f'asset {u} -> {s}')

out = {'results': results, 'assets': asset_status, 'problems': problems}
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('languages checked:', len(results), '| new hero on:', sum(r['new_hero'] for r in results.values()))
print('assets:', asset_status)
print('problems:', problems or 'none')
for lang in ('en', 'es', 'de', 'ja', 'ar'):
    r = results.get(lang, {})
    print(lang, '|', r.get('eyebrow'), '|', r.get('heading'), '|', r.get('ctas'))
