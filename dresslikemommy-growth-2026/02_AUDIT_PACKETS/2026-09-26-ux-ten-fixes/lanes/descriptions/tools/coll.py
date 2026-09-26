import json
from gql import q
out=[]; after=None
while True:
    r=q('''query($a:String){collections(first:100,after:$a){pageInfo{hasNextPage endCursor}
      nodes{id handle title sortOrder updatedAt productsCount{count} ruleSet{appliedDisjunctively rules{column relation condition}}
      templateSuffix descriptionHtml publishedOnCurrentPublication resourcePublicationsCount{count}}}}''',{'a':after})
    if 'data' not in r or r.get('errors'): print(json.dumps(r)[:1500]); break
    d=r['data']['collections']; out+=d['nodes']
    if not d['pageInfo']['hasNextPage']: break
    after=d['pageInfo']['endCursor']
json.dump(out,open('collections.json','w'),indent=1)
print(len(out))
m=q('{menus(first:25){nodes{id handle title items{title type url resourceId items{title type url resourceId items{title type url resourceId}}}}}}')
json.dump(m,open('menus.json','w'),indent=1)
print(json.dumps(m)[:600])
