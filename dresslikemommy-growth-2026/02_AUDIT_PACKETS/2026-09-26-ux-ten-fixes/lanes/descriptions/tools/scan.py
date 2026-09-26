import json,re,html
from collections import Counter,defaultdict
from patterns import COMPILED
P=json.load(open('products_en.json'))
def sentences(h):
    raw = h or ''
    out=[]
    for m in re.finditer(r'<(li|p|td|th|h\d)\b[^>]*>(.*?)</\1>', raw, re.S|re.I):
        t=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',m.group(2))).split())
        for s in re.split(r'(?<=[.!?])\s+',t):
            if s: out.append(s)
    return out
res=[]
for p in P:
    hits=[]
    for s in sentences(p['descriptionHtml']):
        cats=[k for k,rx in COMPILED if rx.search(s)]
        if cats: hits.append({'sentence':s,'categories':cats})
    # raw-html-only checks (admin artifacts)
    if re.search(r'admin\.shopify\.com|http-equiv',p['descriptionHtml'] or '',re.I) and not any('admin_artifact' in h['categories'] for h in hits):
        hits.append({'sentence':'[raw html admin artifact]','categories':['admin_artifact']})
    if hits: res.append({'id':p['id'].split('/')[-1],'handle':p['handle'],'status':p['status'],'title':p['title'],'hits':hits})
json.dump(res,open('flags.json','w'),indent=1)
c=Counter(); cs=Counter(); sent=Counter()
for r in res:
    c[r['status']]+=1
    for h in r['hits']:
        for k in h['categories']: cs[(r['status'],k)]+=1
        sent[(r['status'],h['sentence'])]+=1
print('flagged products by status',dict(c))
print(sorted(cs.items()))
print('distinct flagged sentences', len(sent))
for (st,s),n in sorted(sent.items()):
    print(n,st,'|',s[:230])
