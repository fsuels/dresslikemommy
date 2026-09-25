"""Scoped release of the seasonal hero files to the MAIN theme when the GitHub sync stalls.

Modes:
  read    — confirm MAIN theme id/role, snapshot live copies of the release files, compare with git
  upsert  — write the release files (byte-identical to git HEAD) with themeFilesUpsert, in two batches
  verify  — read back checksums/content and compare with git HEAD
Never prints the access token.
"""
import base64
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path('/Users/fsuels/Projects/dresslikemommy')
PACKET = REPO / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-25-seasonal-homepage-hero/release'
API_VERSION = '2026-04'
THEME_ID = 'gid://shopify/OnlineStoreTheme/133290917985'
RELEASE_COMMIT = '5074fd8'
PREVIOUS_COMMIT = '3019324'
BINARY = ('.jpg', '.webp')
BATCH1 = [
    'assets/hero-halloween-sky.jpg', 'assets/hero-halloween-sky-mobile.jpg',
    'assets/hero-halloween-art-760.webp', 'assets/hero-halloween-art-1140.webp', 'assets/hero-halloween-art-1520.webp',
    'assets/hero-winter-sky.jpg', 'assets/hero-winter-sky-mobile.jpg',
    'assets/hero-winter-art-760.webp', 'assets/hero-winter-art-1140.webp', 'assets/hero-winter-art-1520.webp',
    'snippets/hero-seasonal-copy.liquid',
    'sections/hero-banner.liquid',
]
BATCH2 = ['templates/index.json']
ALL = BATCH1 + BATCH2

cred = json.load(open(Path.home() / '.config/dresslikemommy/admin-api-token.json'))
ENDPOINT = f"https://{cred['store_domain']}/admin/api/{API_VERSION}/graphql.json"


def gql(query, variables=None):
    req = urllib.request.Request(
        ENDPOINT, method='POST',
        data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
        headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': cred['access_token']})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())
    if out.get('errors'):
        raise SystemExit(f"GraphQL errors: {json.dumps(out['errors'])[:800]}")
    return out['data']


def git_bytes(commit, path):
    r = subprocess.run(['git', '-C', str(REPO), 'show', f'{commit}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def strip_json_header(text):
    t = text.lstrip()
    if t.startswith('/*'):
        t = t[t.index('*/') + 2:]
    return json.loads(t)


def live_files(names):
    q = '''query($id: ID!, $names: [String!]!) {
      theme(id: $id) { id name role
        files(filenames: $names, first: 50) { nodes { filename checksumMd5 size
          body { ... on OnlineStoreThemeFileBodyText { content } } } } } }'''
    d = gql(q, {'id': THEME_ID, 'names': names})
    return d['theme'], {n['filename']: n for n in d['theme']['files']['nodes']}


def same(path, live_node, git_content):
    if live_node is None or git_content is None:
        return live_node is None and git_content is None
    if hashlib.md5(git_content).hexdigest() == live_node['checksumMd5']:
        return True
    if path.endswith('.json') and live_node.get('body') and live_node['body'].get('content') is not None:
        return strip_json_header(live_node['body']['content']) == strip_json_header(git_content.decode('utf-8'))
    return False


def mode_read():
    theme, nodes = live_files(ALL)
    print('theme:', theme['id'], theme['name'], theme['role'])
    assert theme['role'] == 'MAIN', 'target theme is not MAIN'
    PACKET.mkdir(parents=True, exist_ok=True)
    report = {}
    for p in ALL:
        n = nodes.get(p)
        prev, rel = git_bytes(PREVIOUS_COMMIT, p), git_bytes(RELEASE_COMMIT, p)
        report[p] = {'live_exists': n is not None, 'live_md5': n and n['checksumMd5'],
                     'live_equals_previous': same(p, n, prev), 'live_equals_release': same(p, n, rel)}
        if n and n.get('body') and n['body'].get('content') is not None:
            dest = PACKET / 'theme_before' / p
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(n['body']['content'], encoding='utf-8')
    json.dump({'theme': theme['id'], 'role': theme['role'], 'files': report}, open(PACKET / 'before_state.json', 'w'), indent=1)
    for p, r in report.items():
        print(f"{p}: exists={r['live_exists']} eq_previous={r['live_equals_previous']} eq_release={r['live_equals_release']}")


def upsert(batch):
    files = []
    for p in batch:
        data = (REPO / p).read_bytes()
        assert data == git_bytes(RELEASE_COMMIT, p), f'{p} differs from {RELEASE_COMMIT}'
        if p.endswith(BINARY):
            files.append({'filename': p, 'body': {'type': 'BASE64', 'value': base64.b64encode(data).decode()}})
        else:
            files.append({'filename': p, 'body': {'type': 'TEXT', 'value': data.decode('utf-8')}})
    m = '''mutation($id: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
      themeFilesUpsert(themeId: $id, files: $files) {
        upsertedThemeFiles { filename }
        job { id done }
        userErrors { field message code filename } } }'''
    d = gql(m, {'id': THEME_ID, 'files': files})['themeFilesUpsert']
    print('upserted:', [f['filename'] for f in d['upsertedThemeFiles'] or []])
    if d['userErrors']:
        raise SystemExit('userErrors: ' + json.dumps(d['userErrors']))
    job = d.get('job')
    if job and not job['done']:
        for _ in range(60):
            time.sleep(2)
            jd = gql('query($id: ID!){ job(id: $id) { id done } }', {'id': job['id']})['job']
            if jd['done']:
                break
        print('job done:', jd['done'])


def mode_upsert():
    theme, nodes = live_files(ALL)
    assert theme['role'] == 'MAIN'
    # Refuse to overwrite anything that is not the pre-release version (protects admin/peer edits).
    for p in ALL:
        n = nodes.get(p)
        prev = git_bytes(PREVIOUS_COMMIT, p)
        if not (same(p, n, prev) or same(p, n, git_bytes(RELEASE_COMMIT, p))):
            raise SystemExit(f'ABORT: live {p} matches neither {PREVIOUS_COMMIT} nor {RELEASE_COMMIT}')
    upsert(BATCH1)
    upsert(BATCH2)


def mode_verify():
    theme, nodes = live_files(ALL)
    ok = True
    rows = {}
    for p in ALL:
        eq = same(p, nodes.get(p), git_bytes(RELEASE_COMMIT, p))
        rows[p] = eq
        ok &= eq
        print(f'{p}: live == {RELEASE_COMMIT}: {eq}')
    json.dump({'theme': theme['id'], 'role': theme['role'], 'release_commit': RELEASE_COMMIT, 'files_equal': rows,
               'all_equal': ok}, open(PACKET / 'after_state.json', 'w'), indent=1)
    print('ALL EQUAL' if ok else 'MISMATCH')


{'read': mode_read, 'upsert': mode_upsert, 'verify': mode_verify}[sys.argv[1]]()
