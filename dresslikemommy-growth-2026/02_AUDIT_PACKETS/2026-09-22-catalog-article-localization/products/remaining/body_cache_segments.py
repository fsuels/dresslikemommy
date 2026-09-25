#!/usr/bin/env python3
"""Read historical local caches only; produce untrusted exact-span candidates."""
import collections,hashlib,html,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent;PRODUCTS=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'ops/content').exists())
def norm(v):return re.sub(r'\s+',' ',html.unescape(v)).strip()
work=json.loads((HERE/'body_segment_sources.json').read_text())
wanted={(loc,x['source']) for x in work for loc in x['locales']}
hits=collections.defaultdict(dict)
def add(loc,s,v,path,method):
 s=norm(s);v=norm(v)
 if (loc,s) in wanted and v and v!=s:
  hits[(loc,s)].setdefault(v,[]).append({'cacheFile':path,'method':method})
def parts(v):
 split=re.split(r'(<[^>]+>)',v)
 tags=[re.match(r'</?([\w:-]+)',x).group(0).lower() if re.match(r'</?([\w:-]+)',x) else x for x in split[1::2]]
 return tags,split[::2]
for info in json.loads((PRODUCTS/'cache_coverage.json').read_text())['cacheFilesInspected']:
 path=ROOT/info['path'];data=json.loads(path.read_text())
 for loc,values in data.items():
  if not isinstance(values,dict):continue
  for s,v in values.items():
   if not isinstance(v,str):continue
   add(loc,s,v,info['path'],'direct_exact_text')
   if '<' in s and '<' in v:
    st,ss=parts(s);vt,vs=parts(v)
    if st==vt and len(ss)==len(vs):
     for si,vi in zip(ss,vs):add(loc,si,vi,info['path'],'html_tag_sequence_aligned_exact_source_span')
out=[{'locale':loc,'source':s,'values':[{'value':v,'provenance':pp} for v,pp in vals.items()]} for (loc,s),vals in sorted(hits.items())]
(HERE/'body_cached_span_candidates.json').write_text(json.dumps({'status':'UNREVIEWED_NOT_FOR_RELEASE','rows':out},ensure_ascii=False,indent=2)+'\n')
summary={'wantedPairs':len(wanted),'cachePairs':len(out),'unambiguousPairs':sum(len(r['values'])==1 for r in out),'cachedSourceWordsByLocale':dict(collections.Counter({loc:sum(len(r['source'].split()) for r in out if r['locale']==loc) for loc in sorted(set(r['locale'] for r in out))})),'limits':'Historical local candidates only. Identical HTML tag sequence supports correspondence, not meaning. Every reused value still requires semantic review; no provider calls.'}
(HERE/'body_cache_segment_coverage.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
