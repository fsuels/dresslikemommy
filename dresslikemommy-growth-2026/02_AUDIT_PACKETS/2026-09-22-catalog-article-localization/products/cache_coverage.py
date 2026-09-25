#!/usr/bin/env python3
import collections,hashlib,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'ops/content').exists())
nodes={}
for f in HERE.glob('translations_batch_*.json'):
    for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']:nodes[n['resourceId']]=n
def plain(v):return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',v)).strip()
cache=collections.defaultdict(list);files=[]
paths=set((ROOT/'ops/content').glob('*cache*.json'))
paths.update((ROOT/'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-22-multilingual-storefront/resource-translations').glob('cache_*.json'))
for f in sorted(paths):
    try:d=json.loads(f.read_text())
    except (ValueError,OSError):continue
    count=0
    for locale,values in d.items():
        if not isinstance(values,dict):continue
        for source,value in values.items():
            if isinstance(value,str) and value.strip():cache[(locale,source)].append({'value':value,'file':str(f.relative_to(ROOT))});count+=1
    files.append({'path':str(f.relative_to(ROOT)),'entries':count,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
rows=list(map(json.loads,(HERE/'defects.jsonl').read_text().splitlines()));bykey=collections.Counter();byreason=collections.Counter();groups={};coverage=collections.Counter();loc=collections.defaultdict(collections.Counter)
for r in rows:
    s=next(x['value'] for x in nodes[r['resourceId']]['translatableContent'] if x['key']==r['key'])
    bykey[r['key']]+=1
    for reason in r['reasons']:byreason[reason]+=1
    key=(r['locale'],s)
    if key not in groups:groups[key]={'locale':r['locale'],'source':s,'sourceSHA256':hashlib.sha256(s.encode()).hexdigest(),'references':[]}
    groups[key]['references'].append(r)
    matches=cache.get(key,[]);distinct=sorted(set(x['value'] for x in matches));usable=[x for x in distinct if plain(x).casefold()!=plain(s).casefold()]
    state='different_cached_candidate' if usable else 'only_source_equal_cache' if matches else 'no_exact_cache'
    groups[key]['cacheStatus']=state;groups[key]['cachedValues']=matches
    coverage[state]+=1;loc[r['locale']][state]+=1
summary={'flaggedFieldLocaleRows':len(rows),'byKey':dict(bykey),'byReasonOverlapping':dict(byreason),'uniqueSourceStrings':len(set(s for _,s in groups)),'uniqueSourceLocalePairs':len(groups),'uniqueSourcePlainWords':sum(len(plain(s).split()) for s in set(s for _,s in groups)),'sourceLocaleWords':sum(len(plain(s).split()) for _,s in groups),'fieldRowCacheCoverage':dict(coverage),'sourceLocalePairCacheCoverage':dict(collections.Counter(g['cacheStatus'] for g in groups.values())),'cacheCoverageByLocale':dict(loc),'cacheFilesInspected':files,'limits':'Exact unmodified source + target locale matching only. Cached values are untrusted historical candidates, not reviewed translations or automatic authorization to apply. No provider calls.'}
(HERE/'cache_coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
with (HERE/'grouped_source_workload.jsonl').open('w') as f:
    for g in sorted(groups.values(),key=lambda x:(x['locale'],x['sourceSHA256'])):f.write(json.dumps(g,ensure_ascii=False,separators=(',',':'))+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('cacheFilesInspected','cacheCoverageByLocale')},ensure_ascii=False))
