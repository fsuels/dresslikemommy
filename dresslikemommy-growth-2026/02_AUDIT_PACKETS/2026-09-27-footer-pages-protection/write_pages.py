from gql import gql
import json,sys
d=json.load(open('before_pages_policies.json'))
ids={p['handle']:p['id'] for p in d['data']['pages']['nodes']}
titles={'about-us':'About Us','shipping-info':'Shipping Info','return-policy':'Returns & Exchanges','faqs':'Frequently Asked Questions','track-your-order':'Track Your Order','size-guide':'Size Guide','contact-us':'Contact Us','company-information':'Company Information','terms-and-conditions':'Terms and Conditions','privacy-policy':'Privacy Policy'}
m='mutation($id:ID!,$p:PageUpdateInput!){ pageUpdate(id:$id,page:$p){ page{ id handle title updatedAt } userErrors{ field message } } }'
for h in (sys.argv[1:] or titles):
    body=open(f'new/{h}.html').read()
    r=gql(m,{'id':ids[h],'p':{'title':titles[h],'body':body}})
    print(h, json.dumps(r.get('errors') or r['data']['pageUpdate'])[:300])
