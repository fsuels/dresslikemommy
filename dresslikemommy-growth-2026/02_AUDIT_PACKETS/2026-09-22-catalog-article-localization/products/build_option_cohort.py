#!/usr/bin/env python3
import collections,hashlib,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent
LEX=json.loads((HERE/'option_dictionary.json').read_text())
nodes={}
for f in HERE.glob('translations_batch_*.json'):
    for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']:nodes[n['resourceId']]=n
def translate(source,locale):
    lex=LEX[locale]
    if source in ('Size','Color'):return lex[source]
    size=re.fullmatch(r'(Mother|Father|Adult) ([2-5]?XL|[SML])',source)
    if size:return lex[size[1]]+' '+size[2]
    age=re.fullmatch(r'Child (\d+(?:-\d+)?) [Yy]ears?',source)
    if not age:return None
    span=age[1];n=int(span.split('-')[-1]);singular=span=='1'
    unit=''
    if locale=='cs':unit='rok' if singular else 'roky' if n in (2,3,4) else 'let'
    elif locale=='de':unit='Jahr' if singular else 'Jahre'
    elif locale=='el':unit='έτους' if singular else 'ετών'
    elif locale=='es':unit='año' if singular else 'años'
    elif locale=='fi':unit='vuosi' if singular else 'vuotta'
    elif locale=='fr':unit='an' if singular else 'ans'
    elif locale=='it':unit='anno' if singular else 'anni'
    elif locale=='pl':unit='rok' if singular else 'lata' if n%10 in (2,3,4) and n%100 not in (12,13,14) else 'lat'
    elif locale=='pt-BR':unit='ano' if singular else 'anos'
    elif locale=='ro':unit='an' if singular else 'ani'
    elif locale=='ru':unit='год' if n%10==1 and n%100!=11 else 'года' if n%10 in (2,3,4) and n%100 not in (12,13,14) else 'лет'
    return lex['ageTemplate'].format(age=span,unit=unit)

rows=[];skipped=collections.Counter();provenance=[]
for line in (HERE/'defects.jsonl').read_text().splitlines():
    d=json.loads(line)
    if d['key']!='name':continue
    n=nodes[d['resourceId']];source=next(s for s in n['translatableContent'] if s['key']=='name')
    value=translate(source['value'],d['locale'])
    if value is None:continue
    # Only missing/copy-English fields in this first cohort; stale translations need separate review.
    if not {'missing','source_english'} & set(d['reasons']):skipped['outdated_only']+=1;continue
    matches=[x for x in n['tr_'+d['locale'].replace('-','_')] if x['locale']==d['locale'] and x.get('market') is None and x['key']=='name']
    assert len(matches)<=1;before=matches[0] if matches else None
    if before and before.get('value')==value:skipped['already_identical_correct_copy']+=1;continue
    assert re.findall(r'\d+',source['value'])==re.findall(r'\d+',value)
    rows.append({'resourceId':d['resourceId'],'productId':d['productId'],'kind':d['kind'],'key':'name','locale':d['locale'],'source':source['value'],'translatableContentDigest':source['digest'],'before':before,'after':value,'marketId':None,'evidenceFile':d['rawFile'],'method':'manual_lexicon_and_exact_size_age_template'})
    provenance.append((d['locale'],source['value'],value))
plan={'status':'CANDIDATE_ONLY_REQUIRES_INDEPENDENT_REVIEW_AND_FRESH_PARENT_READBACK','scope':'Only missing or source-English option names and simple Mother/Father/Adult size codes or Child year-age options. No source, product body, title, prices, stock, variant IDs or handles change. No providers.','rows':rows}
(HERE/'option_cohort_candidate.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
inverse=[{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'action':'restore' if r['before'] else 'remove','value':r['before']['value'] if r['before'] else None,'marketId':None} for r in rows]
(HERE/'option_cohort_rollback.json').write_text(json.dumps(inverse,ensure_ascii=False,indent=2)+'\n')
unique=[{'locale':l,'source':s,'after':v,'rowCount':sum(r['locale']==l and r['source']==s for r in rows)} for l,s,v in sorted(set(provenance))]
(HERE/'option_cohort_dictionary_expansion.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2)+'\n')
summary={'candidateRows':len(rows),'uniqueSourceLocaleValues':len(unique),'products':len(set(r['productId'] for r in rows)),'byLocale':dict(collections.Counter(r['locale'] for r in rows)),'byKind':dict(collections.Counter(r['kind'] for r in rows)),'inverseRestore':sum(r['action']=='restore' for r in inverse),'inverseRemove':sum(r['action']=='remove' for r in inverse),'skipped':dict(skipped),'numericSequenceChecks':len(rows),'planSHA256':hashlib.sha256((HERE/'option_cohort_candidate.json').read_bytes()).hexdigest()}
(HERE/'option_cohort_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary))
