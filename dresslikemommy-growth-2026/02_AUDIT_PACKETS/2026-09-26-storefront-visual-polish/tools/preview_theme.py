"""Unpublished preview theme for the storefront visual polish release (owner-approved 2026-09-26: "Preview, then ask me").

Modes:
  duplicate  — themeDuplicate MAIN into a new UNPUBLISHED theme; records its id in preview_theme.json
  upsert     — themeFilesUpsert the lane files (working-tree bytes) into the preview theme only
  verify     — compare preview-theme checksums/JSON with the working tree
Refuses to write to any theme whose role is not UNPUBLISHED. Never prints the access token.
"""
import base64
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path('/Users/fsuels/Projects/dresslikemommy')
PACKET = REPO / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-storefront-visual-polish'
STATE = PACKET / 'preview_theme.json'
API_VERSION = '2026-04'
MAIN_ID = 'gid://shopify/OnlineStoreTheme/133290917985'
PREVIEW_NAME = 'DLM visual polish preview v2 2026-09-26'
BINARY = ('.jpg', '.webp', '.png')

TEXT_FILES = [
    'assets/base.css', 'assets/component-card.css', 'assets/component-product-description.css',
    'assets/component-product-desktop-ux-ruler-sync.css', 'assets/section-category-icons.css',
    'assets/section-footer.css', 'assets/section-main-product.css', 'assets/theme-inline-head-static-03.css',
    'assets/theme-inline-head-static-05.css', 'assets/category-tile-layout.css',
    'config/settings_data.json',
    'sections/category-icons.liquid', 'sections/curated-product-grid.liquid', 'sections/footer-group.json',
    'sections/footer.liquid', 'sections/hero-banner.liquid', 'sections/main-product.liquid',
    'sections/seasonal-collection.liquid',
    'snippets/card-product.liquid', 'snippets/product-media-gallery.liquid', 'snippets/pdp-highlights-compact.liquid',
    'snippets/home-spotlight-card.liquid',
    'templates/index.json',
]
TILES = [f'assets/category-tile-{n}-{w}.webp'
         for n in ('mommy-me', 'family-matching', 'pajamas', 'dresses', 'swimsuits', 'daddy-me',
                   'vacation', 'photo-days', 'birthdays', 'beach-days')
         for w in (360, 600, 900)]
ALL = TEXT_FILES + TILES

cred = json.load(open(Path.home() / '.config/dresslikemommy/admin-api-token.json'))
ENDPOINT = f"https://{cred['store_domain']}/admin/api/{API_VERSION}/graphql.json"


def gql(query, variables=None):
    req = urllib.request.Request(
        ENDPOINT, method='POST',
        data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
        headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': cred['access_token']})
    with urllib.request.urlopen(req, timeout=180) as r:
        out = json.loads(r.read())
    if out.get('errors'):
        raise SystemExit(f"GraphQL errors: {json.dumps(out['errors'])[:800]}")
    return out['data']


def theme_role(tid):
    return gql('query($id: ID!){ theme(id: $id){ id name role } }', {'id': tid})['theme']


def strip_json_header(text):
    t = text.lstrip()
    if t.startswith('/*'):
        t = t[t.index('*/') + 2:]
    return json.loads(t)


def mode_duplicate():
    if STATE.exists():
        raise SystemExit(f'preview already recorded: {STATE.read_text()}')
    assert theme_role(MAIN_ID)['role'] == 'MAIN'
    d = gql('''mutation($id: ID!, $name: String){ themeDuplicate(id: $id, name: $name){
      newTheme { id name role } userErrors { field message code } } }''', {'id': MAIN_ID, 'name': PREVIEW_NAME})
    r = d['themeDuplicate']
    if r['userErrors']:
        raise SystemExit('userErrors: ' + json.dumps(r['userErrors']))
    new = r['newTheme']
    print('created:', new)
    assert new['role'] == 'UNPUBLISHED', new
    STATE.write_text(json.dumps({'preview_theme_id': new['id'], 'name': new['name'],
                                 'created_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, indent=1))


def preview_id():
    tid = json.loads(STATE.read_text())['preview_theme_id']
    t = theme_role(tid)
    if t['role'] != 'UNPUBLISHED':
        raise SystemExit(f'ABORT: {tid} role is {t["role"]}, not UNPUBLISHED')
    return tid


def mode_upsert(paths):
    tid = preview_id()
    for i in range(0, len(paths), 10):
        batch = paths[i:i + 10]
        files = []
        for p in batch:
            data = (REPO / p).read_bytes()
            if p.endswith(BINARY):
                files.append({'filename': p, 'body': {'type': 'BASE64', 'value': base64.b64encode(data).decode()}})
            else:
                files.append({'filename': p, 'body': {'type': 'TEXT', 'value': data.decode('utf-8')}})
        d = gql('''mutation($id: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!){
          themeFilesUpsert(themeId: $id, files: $files){ upsertedThemeFiles { filename } job { id done }
          userErrors { field message code filename } } }''', {'id': tid, 'files': files})['themeFilesUpsert']
        if d['userErrors']:
            raise SystemExit('userErrors: ' + json.dumps(d['userErrors']))
        job = d.get('job')
        if job and not job['done']:
            for _ in range(90):
                time.sleep(2)
                if gql('query($id: ID!){ job(id: $id){ done } }', {'id': job['id']})['job']['done']:
                    break
        print('upserted:', [f['filename'] for f in d['upsertedThemeFiles'] or []])


def mode_verify(paths):
    tid = preview_id()
    bad = []
    for i in range(0, len(paths), 25):
        names = paths[i:i + 25]
        d = gql('''query($id: ID!, $names: [String!]!){ theme(id: $id){ files(filenames: $names, first: 50){
          nodes { filename checksumMd5 body { ... on OnlineStoreThemeFileBodyText { content } } } } } }''',
                {'id': tid, 'names': names})
        nodes = {n['filename']: n for n in d['theme']['files']['nodes']}
        for p in names:
            n, local = nodes.get(p), (REPO / p).read_bytes()
            ok = n is not None and (hashlib.md5(local).hexdigest() == n['checksumMd5'] or (
                p.endswith('.json') and n.get('body') and
                strip_json_header(n['body']['content']) == strip_json_header(local.decode())))
            if not ok:
                bad.append(p)
    print(f'verified {len(paths) - len(bad)}/{len(paths)}; mismatches: {bad}')


if __name__ == '__main__':
    mode = sys.argv[1]
    only = sys.argv[2:] or ALL
    {'duplicate': lambda: mode_duplicate(), 'upsert': lambda: mode_upsert(only),
     'verify': lambda: mode_verify(only)}[mode]()
