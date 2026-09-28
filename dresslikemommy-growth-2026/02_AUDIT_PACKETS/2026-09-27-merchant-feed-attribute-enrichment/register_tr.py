import json,sys,time
from gql import gql
LOC=['ar','cs','da','de','el','es','fi','fr','he','hi','it','ja','ko','nl','no','pl','pt-BR','ro','ru','sv']
T=json.load(open('codex_job/translations.json'))
F=[r for r in json.load(open('final.json')) if not r.get('skip')]
only=sys.argv[1:]  # optional handles
Q='''query($id:ID!,$l:String!){translatableResource(resourceId:$id){translatableContent{key value digest} translations(locale:$l){key value outdated}}}'''
M='''mutation($id:ID!,$t:[TranslationInput!]!){translationsRegister(resourceId:$id,translations:$t){translations{key locale value} userErrors{field message}}}'''
def sep(l): return '' if l in('ja',) else ' '
def tail(r,l):
    lab=T['labels'][l]; tt=T['terms'][l]; parts=[]
    colon={'fr':' :','ja':'：'}.get(l,':')
    lsep={'ar':'، ','ja':'、'}.get(l,', ')
    if r['colors']: parts.append((lab['Colors'] if len(r['colors'])>1 else lab['Color'])+colon+('' if l=='ja' else ' ')+lsep.join(tt[c] for c in r['colors'])+('。' if l=='ja' else '.'))
    if r['pattern']: parts.append(lab['Pattern']+colon+('' if l=='ja' else ' ')+tt[r['pattern']]+('。' if l=='ja' else '.'))
    if r['material']:
        m=r['material'][0].upper()+r['material'][1:]; parts.append(lab['Material']+colon+('' if l=='ja' else ' ')+tt[m]+('。' if l=='ja' else '.'))
    return sep(l).join(parts)
import os
LC=json.load(open('leads_cache.json')) if os.path.exists('leads_cache.json') else {}
rec=[]
for r in F:
    if only and r['handle'] not in only: continue
    for l in LOC:
        d=gql(Q,{'id':r['id'],'l':l})['data']['translatableResource']
        src={c['key']:c for c in d['translatableContent']}['meta_description']
        if src['value']!=r['new']: rec.append({'h':r['handle'],'l':l,'status':'SOURCE_MISMATCH'}); continue
        cur={t['key']:t for t in d['translations']}.get('meta_description')
        if not cur or not cur['value']: rec.append({'h':r['handle'],'l':l,'status':'NO_EXISTING_LEAD'}); continue
        lead=LC.get(f"{r['id']}|{l}",cur['value']).strip(); LC.setdefault(f"{r['id']}|{l}",cur['value'])
        # idempotent: strip a previously appended tail
        lab=T['labels'][l]
        for key in ('Colors','Color','Pattern','Material'):
            pass
        t=tail(r,l)
        if t and t in lead: lead=lead.replace(t,'').strip()
        if lead and lead[-1] not in '.!?。':
            lead+='。' if l=='ja' else '.'
        val=(lead+sep(l)+t).strip()
        res=gql(M,{'id':r['id'],'t':[{'key':'meta_description','locale':l,'value':val,'translatableContentDigest':src['digest']}]})['data']['translationsRegister']
        ok=not res['userErrors']
        rec.append({'h':r['handle'],'id':r['id'],'l':l,'before':cur['value'],'after':val,'status':'REGISTERED' if ok else 'ERROR','err':res['userErrors']})
    time.sleep(0.1)
json.dump(LC,open('leads_cache.json','w'),ensure_ascii=False,indent=0)
json.dump(rec,open('translation_receipts.json','w'),indent=1,ensure_ascii=False)
from collections import Counter
print(Counter(x['status'] for x in rec))
