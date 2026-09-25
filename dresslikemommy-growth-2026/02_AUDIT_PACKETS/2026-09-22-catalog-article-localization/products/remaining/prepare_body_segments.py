#!/usr/bin/env python3
"""Local-only lossless text-span inventory, retaining original markup and provenance."""
import collections,hashlib,html,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent;PRODUCTS=HERE.parent
def norm(s):return re.sub(r'\s+',' ',html.unescape(s)).strip()
def spans(s):
    # The split retains original tag bytes; attribute values are outside this text-copy lane.
    return [norm(t) for t in re.split(r'(<[^>]+>)',s) if not t.startswith('<') and norm(t)]
nodes={n['resourceId']:(f.name,n) for f in PRODUCTS.glob('translations_batch_*json') for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']}
base=json.loads((HERE/'baseline.json').read_text())['rows']
body=[r for r in base if r['key']=='body_html'];known={(r['resourceId'],r['locale']) for r in body}
review=list(map(json.loads,(PRODUCTS/'language_review_candidates.jsonl').read_text().splitlines()))
for r in review:
    if r['key']!='body_html' or (r['resourceId'],r['locale']) in known:continue
    fn,n=nodes[r['resourceId']];s=next(x for x in n['translatableContent'] if x['key']=='body_html');before=next(x for x in n['tr_'+r['locale'].replace('-','_')] if x['key']=='body_html' and x['locale']==r['locale'] and x.get('market') is None)
    body.append({'resourceId':r['resourceId'],'productId':r['resourceId'],'locale':r['locale'],'key':'body_html','source':s['value'],'sourceDigest':s['digest'],'before':before,'auditReasons':r['reasons'],'rawFile':fn});known.add((r['resourceId'],r['locale']))
work=collections.defaultdict(list);perfield=[]
for i,r in enumerate(body):
    ss=set(spans(r['source']));target=spans(r['before']['value']) if r['before'] else spans(r['source'])
    hits=[]
    for t in set(target):
        words=re.findall('[A-Za-z]+',t)
        invariant=words and all(x.lower() in {'cm','in','kg','lb','lbs','mm','oz','y','t','xl','xxl','xxxl','xxxxl','s','m','l','xs','xxs'} for x in words)
        if t in ss and words and not invariant:
            hits.append(t);work[t].append(i)
    perfield.append({'bodyIndex':i,'resourceId':r['resourceId'],'locale':r['locale'],'exactSourceTextSpans':len(hits),'longEnglishSpanCount':sum(len(re.findall('[A-Za-z]+',x))>=12 for x in hits),'exactSourceSpanWords':sum(len(x.split()) for x in hits)})
ordered=sorted(work,key=lambda t:(-len(work[t]),t))
records=[{'index':i,'source':t,'words':len(t.split()),'occurrences':len(work[t]),'locales':sorted(set(body[j]['locale'] for j in work[t])),'bodyIndices':work[t]} for i,t in enumerate(ordered)]
for f,o in [('body_baseline.json',{'rows':body}),('body_segment_sources.json',records),('body_segment_fields.json',perfield)]:
    (HERE/f).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'bodyFields':len(body),'sourceTextSpans':len(work),'uniqueSpanWords':sum(len(t.split()) for t in work),'localeSpanPairs':sum(len(set(body[j]['locale'] for j in js)) for js in work.values()),'localizedSpanWordsRequired':sum(len(t.split())*len(set(body[j]['locale'] for j in js)) for t,js in work.items()),'longParagraphSpans':sum(len(re.findall('[A-Za-z]+',t))>=12 for t in work)}))
print(json.dumps([{k:v for k,v in x.items() if k!='bodyIndices'} for x in records[:30]],ensure_ascii=False))
