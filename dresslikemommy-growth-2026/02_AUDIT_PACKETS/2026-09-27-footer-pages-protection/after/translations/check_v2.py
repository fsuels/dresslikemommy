import json,sys,re
for l in sys.argv[1:]:
    d=json.load(open(f'tr/{l}.json')); bad=[]
    for k in ['shipping-info','faqs','policy-shipping']:
        if re.search(r'1\s*[–\-~〜－至到]\s*3',d[k]['body']): bad.append(k)
    if '8.50' not in d['policy-privacy']['body'] and '8,50' not in d['policy-privacy']['body']: bad.append('privacy-8.50')
    if '14937' not in d['policy-refund']['body']: bad.append('refund-model-form')
    print(l,'v2 OK' if not bad else f'v2 MISSING {bad}')
