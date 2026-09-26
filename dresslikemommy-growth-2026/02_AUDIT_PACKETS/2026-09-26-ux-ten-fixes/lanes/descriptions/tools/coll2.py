import json
from gql import q
C=json.load(open('collections.json'))
OS='gid://shopify/Publication/55169925'
for c in C:
    r=q('query($id:ID!,$p:ID!){collection(id:$id){publishedOnPublication(publicationId:$p)}}',{'id':c['id'],'p':OS})
    c['onlineStore']=r['data']['collection']['publishedOnPublication']
    prods=[]; after=None
    while True:
        r=q('query($id:ID!,$a:String){collection(id:$id){products(first:250,after:$a,sortKey:COLLECTION_DEFAULT){pageInfo{hasNextPage endCursor} nodes{id handle title status createdAt productType tags onlineStore:publishedOnPublication(publicationId:"%s")}}}}'%OS,{'id':c['id'],'a':after})
        d=r['data']['collection']['products']; prods+=d['nodes']
        if not d['pageInfo']['hasNextPage']: break
        after=d['pageInfo']['endCursor']
    c['products']=prods
json.dump(C,open('collections_full.json','w'))
for c in C:
    live=[p for p in c['products'] if p['status']=='ACTIVE' and p['onlineStore']]
    c['live_count']=len(live)
    print(f"{c['handle'][:36]:36} OS={str(c['onlineStore'])[0]} all={len(c['products'])} live={len(live)} first3={[p['handle'][:30] for p in live[:3]]}")
json.dump(C,open('collections_full.json','w'))
