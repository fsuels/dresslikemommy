import json
from gql import q
out=[]; after=None
while True:
    r=q('query($a:String){products(first:100,after:$a){pageInfo{hasNextPage endCursor} nodes{id handle title status updatedAt descriptionHtml onlineStoreUrl}}}',{'a':after})
    if 'data' not in r: print(r); break
    d=r['data']['products']; out+=d['nodes']
    if not d['pageInfo']['hasNextPage']: break
    after=d['pageInfo']['endCursor']
json.dump(out,open('products_en.json','w'))
from collections import Counter
print(len(out), Counter(p['status'] for p in out))
