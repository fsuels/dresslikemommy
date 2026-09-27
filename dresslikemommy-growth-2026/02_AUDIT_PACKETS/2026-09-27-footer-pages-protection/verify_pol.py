from gql import gql
import sys,re
pol={'policy-refund':'gid://shopify/ShopPolicy/14695685','policy-privacy':'gid://shopify/ShopPolicy/14695749','policy-terms':'gid://shopify/ShopPolicy/14695813','policy-shipping':'gid://shopify/ShopPolicy/29845782625','policy-contact':'gid://shopify/ShopPolicy/31171805281'}
norm=lambda s: re.sub(r'\s+',' ',s.replace('&amp;','&')).replace('> <','><').strip()
for k in sys.argv[1:]:
    r=gql('query($id:ID!){ translatableResource(resourceId:$id){ translatableContent{ key value } } }',{'id':pol[k]})
    live=r['data']['translatableResource']['translatableContent'][0]['value']
    f=open(f'new/{k}.html').read()
    a,b=norm(live),norm(f)
    if a==b: print(k,'MATCH',len(live))
    else:
        i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
        print(k,'DIFF at',i,'\n live:',a[i-60:i+80],'\n file:',b[i-60:i+80])
