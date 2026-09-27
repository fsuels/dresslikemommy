"""Register translations from tr/<locale>.json. Usage: register_tr.py <locale>... [--dry]"""
from gql import gql
import json,sys,re
d=json.load(open('before_pages_policies.json'))
pid={p['handle']:p['id'] for p in d['data']['pages']['nodes']}
pol={'policy-refund':'gid://shopify/ShopPolicy/14695685','policy-privacy':'gid://shopify/ShopPolicy/14695749','policy-terms':'gid://shopify/ShopPolicy/14695813','policy-shipping':'gid://shopify/ShopPolicy/29845782625','policy-contact':'gid://shopify/ShopPolicy/31171805281'}
FIELD={'title':'title','body':'body_html','meta_title':'meta_title','meta_description':'meta_description'}
dry='--dry' in sys.argv
digests={}
def content(rid):
    if rid not in digests:
        r=gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key digest value } } }',{'id':rid})
        digests[rid]={c['key']:c for c in r['data']['translatableResource']['translatableContent']}
    return digests[rid]
for loc in [a for a in sys.argv[1:] if not a.startswith('--')]:
    t=json.load(open(f'tr/{loc}.json'))
    ok=err=0
    for key,fields in t.items():
        if key.startswith('policy-'):
            rid=pol[key]; items=[('body',fields['body'])]
        else:
            rid=pid[key]; items=[(FIELD[f],v) for f,v in fields.items()]
        c=content(rid); regs=[]
        for k,v in items:
            if k not in c: print('  missing key',key,k); err+=1; continue
            regs.append({'locale':loc,'key':k,'value':v,'translatableContentDigest':c[k]['digest']})
        if dry: ok+=len(regs); continue
        r=gql('mutation($id:ID!,$t:[TranslationInput!]!){ translationsRegister(resourceId:$id,translations:$t){ userErrors{ field message } translations{ key } } }',{'id':rid,'t':regs})
        ue=(r.get('errors') or r['data']['translationsRegister']['userErrors'])
        if ue: print('  ERR',key,json.dumps(ue)[:300]); err+=1
        else: ok+=len(regs)
    print(loc,'registered',ok,'errors',err)
