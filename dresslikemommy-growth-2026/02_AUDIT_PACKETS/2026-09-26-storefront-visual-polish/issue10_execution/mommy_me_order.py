"""#10 Mommy & Me default order (owner-approved 2026-09-26).
Modes: before | apply | after. Never prints the access token.
apply: sortOrder CREATED_DESC -> MANUAL, then move whole-family products (tagged "Daddy and Me", or lacking the "Mommy and Me" tag) to the end (relative order kept).
Rollback: collectionUpdate(input:{id, sortOrder: CREATED_DESC}).
"""
import json, sys, time, urllib.request
from pathlib import Path
OUT = Path(__file__).parent
CID = 'gid://shopify/Collection/320794427489'
cred = json.load(open(Path.home() / '.config/dresslikemommy/admin-api-token.json'))
EP = f"https://{cred['store_domain']}/admin/api/2026-04/graphql.json"

def gql(q, v=None):
    r = urllib.request.Request(EP, method='POST', data=json.dumps({'query': q, 'variables': v or {}}).encode(),
                               headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': cred['access_token']})
    out = json.loads(urllib.request.urlopen(r, timeout=120).read())
    if out.get('errors'):
        raise SystemExit('GraphQL errors: ' + json.dumps(out['errors'])[:600])
    return out['data']

def snapshot():
    meta = gql('query($id:ID!){collection(id:$id){id handle title sortOrder updatedAt ruleSet{appliedDisjunctively rules{column relation condition}} productsCount{count}}}', {'id': CID})['collection']
    nodes, after = [], None
    while True:
        d = gql('''query($id:ID!,$a:String){collection(id:$id){products(first:250, after:$a, sortKey:COLLECTION_DEFAULT){
          pageInfo{hasNextPage endCursor} nodes{id handle status tags createdAt}}}}''', {'id': CID, 'a': after})['collection']['products']
        nodes += d['nodes']
        if not d['pageInfo']['hasNextPage']:
            break
        after = d['pageInfo']['endCursor']
    return meta, nodes

def summarize(meta, nodes, label):
    active = [n for n in nodes if n['status'] == 'ACTIVE']
    dad = lambda n: 'daddy and me' in [t.lower() for t in n['tags']] or 'mommy and me' not in [t.lower() for t in n['tags']]
    first_dad = next((i for i, n in enumerate(active) if dad(n)), None)
    print(label, meta['sortOrder'], 'members', len(nodes), 'active', len(active),
          'active dad-inclusive', sum(dad(n) for n in active), 'first dad-inclusive active position', first_dad)
    print('first 12 active:', [n['handle'][:40] for n in active[:12]])

mode = sys.argv[1]
if mode == 'before':
    meta, nodes = snapshot()
    json.dump({'meta': meta, 'order': nodes}, open(OUT / 'before_state.json', 'w'), indent=1)
    summarize(meta, nodes, 'BEFORE')
elif mode == 'apply':
    before = json.load(open(OUT / 'before_state.json'))
    meta, nodes = snapshot()
    assert meta['sortOrder'] == before['meta']['sortOrder'] == 'CREATED_DESC', meta['sortOrder']
    assert meta['updatedAt'] == before['meta']['updatedAt'], 'collection changed since before-state'
    d = gql('mutation($i:CollectionInput!){collectionUpdate(input:$i){collection{id sortOrder} userErrors{field message}}}',
            {'i': {'id': CID, 'sortOrder': 'MANUAL'}})['collectionUpdate']
    if d['userErrors']:
        raise SystemExit('userErrors: ' + json.dumps(d['userErrors']))
    print('sortOrder now', d['collection']['sortOrder'])
    meta2, nodes2 = snapshot()
    if [n['id'] for n in nodes2] != [n['id'] for n in nodes]:
        print('NOTE: manual starting order differs from prior CREATED_DESC order')
        json.dump(nodes2, open(OUT / 'manual_start_order.json', 'w'), indent=1)
    def whole_family(n):
        tags = [t.lower() for t in n['tags']]
        return 'daddy and me' in tags or 'mommy and me' not in tags
    dad_ids = [n['id'] for n in nodes2 if whole_family(n)]
    moves = [{'id': i, 'newPosition': '100000'} for i in dad_ids]
    json.dump(moves, open(OUT / 'moves_applied.json', 'w'), indent=1)
    for k in range(0, len(moves), 250):
        r = gql('mutation($id:ID!,$m:[MoveInput!]!){collectionReorderProducts(id:$id,moves:$m){job{id done} userErrors{field message}}}',
                {'id': CID, 'm': moves[k:k + 250]})['collectionReorderProducts']
        if r['userErrors']:
            raise SystemExit('userErrors: ' + json.dumps(r['userErrors']))
        job = r['job']
        while job and not job['done']:
            time.sleep(2)
            job = gql('query($id:ID!){job(id:$id){id done}}', {'id': job['id']})['job']
    print('moved', len(moves))
elif mode == 'after':
    meta, nodes = snapshot()
    json.dump({'meta': meta, 'order': nodes}, open(OUT / 'after_state.json', 'w'), indent=1)
    summarize(meta, nodes, 'AFTER')
    before = json.load(open(OUT / 'before_state.json'))
    assert sorted(n['id'] for n in nodes) == sorted(n['id'] for n in before['order']), 'membership changed'
    print('membership unchanged:', len(nodes))
