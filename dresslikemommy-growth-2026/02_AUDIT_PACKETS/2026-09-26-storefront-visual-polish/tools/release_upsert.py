"""Release fallback for commit f5c932f when the GitHub->Shopify sync drops the push (owner approved the live release 2026-09-26).
Modes: read | upsert | verify. Uploads only bytes from `git show f5c932f:<path>` to MAIN, refuses any file whose live copy
matches neither the parent commit nor the release. Saves live before-copies for rollback. Never prints the access token.
"""
import base64, hashlib, json, re, subprocess, sys, time, urllib.request
from pathlib import Path
REPO = Path('/Users/fsuels/Projects/dresslikemommy')
PACKET = REPO / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-storefront-visual-polish/release'
REL, PARENT = 'f5c932f', 'f5c932f^'
THEME = 'gid://shopify/OnlineStoreTheme/133290917985'
src = (REPO / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-storefront-visual-polish/tools/preview_theme.py').read_text()
ns = {}; exec(src.split('cred = ')[0], ns)
TEMPLATES = [p for p in ns['ALL'] if p.startswith('templates/')]
OTHERS = [p for p in ns['ALL'] if not p.startswith('templates/')]
ALL = OTHERS + TEMPLATES
cred = json.load(open(Path.home() / '.config/dresslikemommy/admin-api-token.json'))
EP = f"https://{cred['store_domain']}/admin/api/2026-04/graphql.json"

def gql(q, v=None):
    r = urllib.request.Request(EP, method='POST', data=json.dumps({'query': q, 'variables': v or {}}).encode(),
                               headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': cred['access_token']})
    out = json.loads(urllib.request.urlopen(r, timeout=180).read())
    if out.get('errors'):
        raise SystemExit('GraphQL errors: ' + json.dumps(out['errors'])[:600])
    return out['data']

def git(commit, p):
    r = subprocess.run(['git', '-C', str(REPO), 'show', f'{commit}:{p}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None

def strip(t):
    t = t.lstrip()
    if t.startswith('/*'):
        t = t[t.index('*/') + 2:]
    return json.loads(t)

def live(names):
    out = {}
    for i in range(0, len(names), 25):
        d = gql('''query($id:ID!,$n:[String!]!){theme(id:$id){role files(filenames:$n,first:50){nodes{filename checksumMd5
          body{... on OnlineStoreThemeFileBodyText{content}}}}}}''', {'id': THEME, 'n': names[i:i + 25]})['theme']
        assert d['role'] == 'MAIN'
        out.update({n['filename']: n for n in d['files']['nodes']})
    return out

def same(p, node, b):
    if node is None or b is None:
        return node is None and b is None
    if hashlib.md5(b).hexdigest() == node['checksumMd5']:
        return True
    if p.endswith('.json') and node.get('body') and node['body'].get('content') is not None:
        return strip(node['body']['content']) == strip(b.decode())
    return False

def state():
    nodes = live(ALL)
    return nodes, {p: {'eq_parent': same(p, nodes.get(p), git(PARENT, p)), 'eq_release': same(p, nodes.get(p), git(REL, p))} for p in ALL}

mode = sys.argv[1]
if mode == 'read':
    nodes, rep = state()
    PACKET.mkdir(parents=True, exist_ok=True)
    for p, n in nodes.items():
        if n.get('body') and n['body'].get('content') is not None:
            d = PACKET / 'live_before' / p; d.parent.mkdir(parents=True, exist_ok=True); d.write_text(n['body']['content'])
    json.dump(rep, open(PACKET / 'before_state.json', 'w'), indent=1)
    bad = [p for p, r in rep.items() if not (r['eq_parent'] or r['eq_release'])]
    print('files', len(rep), 'eq_parent', sum(r['eq_parent'] for r in rep.values()), 'eq_release', sum(r['eq_release'] for r in rep.values()), 'NEITHER', bad)
elif mode == 'upsert':
    nodes, rep = state()
    bad = [p for p, r in rep.items() if not (r['eq_parent'] or r['eq_release'])]
    if bad:
        raise SystemExit(f'ABORT: live differs from both parent and release: {bad}')
    todo = [p for p in ALL if not rep[p]['eq_release']]
    batches = [[p for p in todo if p in OTHERS][i:i + 10] for i in range(0, len([p for p in todo if p in OTHERS]), 10)] + ([[p for p in todo if p in TEMPLATES]] if any(p in TEMPLATES for p in todo) else [])
    for batch in batches:
        files = []
        for p in batch:
            b = git(REL, p)
            files.append({'filename': p, 'body': {'type': 'BASE64', 'value': base64.b64encode(b).decode()}} if p.endswith(('.webp', '.png', '.jpg'))
                         else {'filename': p, 'body': {'type': 'TEXT', 'value': b.decode('utf-8')}})
        d = gql('''mutation($id:ID!,$f:[OnlineStoreThemeFilesUpsertFileInput!]!){themeFilesUpsert(themeId:$id,files:$f){
          upsertedThemeFiles{filename} job{id done} userErrors{field message code filename}}}''', {'id': THEME, 'f': files})['themeFilesUpsert']
        if d['userErrors']:
            raise SystemExit('userErrors: ' + json.dumps(d['userErrors']))
        job = d.get('job')
        while job and not job['done']:
            time.sleep(2); job = gql('query($id:ID!){job(id:$id){id done}}', {'id': job['id']})['job']
        print('upserted', [f['filename'] for f in d['upsertedThemeFiles'] or []])
elif mode == 'verify':
    nodes, rep = state()
    bad = [p for p, r in rep.items() if not r['eq_release']]
    json.dump(rep, open(PACKET / 'after_state.json', 'w'), indent=1)
    print(f'live equals {REL}: {len(ALL) - len(bad)}/{len(ALL)}; mismatches: {bad}')
