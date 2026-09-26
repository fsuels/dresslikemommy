import json
from gql import q
locs=q('{shopLocales{locale primary published}}')['data']['shopLocales']
L=[l['locale'] for l in locs if not l['primary']]
print('non-primary locales',len(L),L, 'published',[l['locale'] for l in locs if l['published'] and not l['primary']].__len__())
O=json.load(open('copy_fixes_full.json'))
res={}
for o in O:
    al=' '.join(f'{("l_"+x.replace("-","_"))}: translations(locale:"{x}"){{key outdated}}' for x in L)
    r=q(f'query($id:ID!){{translatableResource(resourceId:$id){{ {al} }}}}',{'id':o['gid']})
    d=r['data']['translatableResource']
    res[o['product_id']]={x:[t for t in d['l_'+x.replace('-','_')] if t['key']=='body_html'] for x in L}
json.dump({'locales':L,'published':[l for l in locs],'per_product':res},open('tr_impact.json','w'),indent=1)
tot=sum(1 for p in res.values() for x,v in p.items() if v)
out=sum(1 for p in res.values() for x,v in p.items() if v and v[0]['outdated'])
print('body_html translations present',tot,'of',len(res)*len(L),'already outdated',out)
