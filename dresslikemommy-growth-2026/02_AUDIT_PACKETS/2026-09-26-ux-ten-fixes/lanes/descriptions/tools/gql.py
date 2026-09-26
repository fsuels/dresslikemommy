import json, sys, urllib.request, time
_c = json.load(open('/Users/fsuels/.config/dresslikemommy/admin-api-token.json'))
READ_ONLY = True
def q(query, variables=None, ver='2026-07'):
    assert 'mutation' not in query.lower().split('{')[0], 'read-only helper'
    for attempt in range(3):
        try:
            req = urllib.request.Request(f"https://{_c['store_domain']}/admin/api/{ver}/graphql.json",
                data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
                headers={'X-Shopify-Access-Token': _c['access_token'], 'Content-Type': 'application/json'})
            r = json.load(urllib.request.urlopen(req, timeout=90))
            if r.get('errors') and any('THROTTLED' in json.dumps(e) for e in r['errors']):
                time.sleep(3); continue
            return r
        except Exception as e:
            if attempt == 2: raise
            time.sleep(3)
