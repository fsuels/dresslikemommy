"""Owner-approved (2026-09-27): clear unsupported compareAtPrice on active-product variants where compareAtPrice > price.
Modes: before | apply | verify | rollback. Never prints the access token.
"""
import json, sys, time, urllib.request
from pathlib import Path
OUT = Path(__file__).parent
cred = json.load(open(Path.home() / '.config/dresslikemommy/admin-api-token.json'))
EP = f"https://{cred['store_domain']}/admin/api/2026-04/graphql.json"

def gql(q, v=None):
    for attempt in range(5):
        r = urllib.request.Request(EP, method='POST', data=json.dumps({'query': q, 'variables': v or {}}).encode(),
                                   headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': cred['access_token']})
        out = json.loads(urllib.request.urlopen(r, timeout=120).read())
        errs = out.get('errors')
        if errs and any('THROTTLED' in json.dumps(e) for e in errs):
            time.sleep(3 * (attempt + 1)); continue
        if errs:
            raise SystemExit('GraphQL errors: ' + json.dumps(errs)[:600])
        return out['data']
    raise SystemExit('throttled too long')

def snapshot():
    prods, after = [], None
    while True:
        d = gql('''query($a:String){products(first:50,after:$a,query:"status:active"){pageInfo{hasNextPage endCursor}
          nodes{id handle variantsCount{count} variants(first:250){pageInfo{hasNextPage} nodes{id price compareAtPrice}}}}}''', {'a': after})['products']
        for p in d['nodes']:
            assert not p['variants']['pageInfo']['hasNextPage'], p['handle']
        prods += d['nodes']
        if not d['pageInfo']['hasNextPage']:
            break
        after = d['pageInfo']['endCursor']
    return prods

def targets(prods):
    out = []
    for p in prods:
        vs = [v for v in p['variants']['nodes'] if v['compareAtPrice'] and float(v['compareAtPrice']) > float(v['price'])]
        if vs:
            out.append({'productId': p['id'], 'handle': p['handle'], 'variants': [{'id': v['id'], 'price': v['price'], 'compareAtPrice': v['compareAtPrice']} for v in vs]})
    return out

mode = sys.argv[1]
if mode == 'before':
    prods = snapshot()
    t = targets(prods)
    json.dump({'captured_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'targets': t}, open(OUT / 'before_state_execution.json', 'w'), indent=1)
    print('active products', len(prods), '| target products', len(t), '| target variants', sum(len(x['variants']) for x in t))
elif mode == 'apply':
    t = json.load(open(OUT / 'before_state_execution.json'))['targets']
    done, errors = 0, []
    for x in t:
        d = gql('''mutation($p:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$p,variants:$v){
          productVariants{id compareAtPrice} userErrors{field message}}}''',
                {'p': x['productId'], 'v': [{'id': v['id'], 'compareAtPrice': None} for v in x['variants']]})['productVariantsBulkUpdate']
        if d['userErrors']:
            errors.append({'handle': x['handle'], 'errors': d['userErrors']})
        else:
            done += len(d['productVariants'])
    json.dump(errors, open(OUT / 'apply_errors.json', 'w'), indent=1)
    print('variants cleared', done, '| products with errors', len(errors))
elif mode == 'verify':
    prods = snapshot()
    t = targets(prods)
    before = json.load(open(OUT / 'before_state_execution.json'))['targets']
    bmap = {v['id']: v for x in before for v in x['variants']}
    now = {v['id']: v for p in prods for v in p['variants']['nodes']}
    price_changed = [i for i, v in bmap.items() if i in now and now[i]['price'] != v['price']]
    still = [i for i in bmap if i in now and now[i]['compareAtPrice']]
    print('variants still showing compare>price (all active):', sum(len(x['variants']) for x in t), '| targeted variants with compareAtPrice left:', len(still), '| targeted variants whose price changed:', len(price_changed))
    json.dump({'remaining_targets': t}, open(OUT / 'after_state_execution.json', 'w'), indent=1)
elif mode == 'rollback':
    t = json.load(open(OUT / 'before_state_execution.json'))['targets']
    for x in t:
        gql('mutation($p:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$p,variants:$v){userErrors{message}}}',
            {'p': x['productId'], 'v': [{'id': v['id'], 'compareAtPrice': v['compareAtPrice']} for v in x['variants']]})
    print('rollback submitted for', sum(len(x['variants']) for x in t), 'variants')
