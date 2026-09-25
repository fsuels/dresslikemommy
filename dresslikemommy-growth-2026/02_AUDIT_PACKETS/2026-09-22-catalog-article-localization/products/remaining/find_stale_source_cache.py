#!/usr/bin/env python3
import hashlib,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'ops/content').exists())
base=[r for r in json.loads((HERE/'body_baseline.json').read_text())['rows'] if 'outdated' in r['auditReasons'] and r['before']]
def norm(s):return re.sub(r'\s+',' ',s).strip()
want={}
for i,r in enumerate(base):want.setdefault((r['locale'],hashlib.sha256(norm(r['before']['value']).encode()).hexdigest()),[]).append(i)
out={}
for info in json.loads((HERE.parent/'cache_coverage.json').read_text())['cacheFilesInspected']:
 data=json.loads((ROOT/info['path']).read_text())
 for loc,vals in data.items():
  if not isinstance(vals,dict):continue
  for src,value in vals.items():
   if not isinstance(value,str):continue
   key=(loc,hashlib.sha256(norm(value).encode()).hexdigest())
   for i in want.get(key,[]):out.setdefault(i,[]).append({'oldEnglishSource':src,'cacheFile':info['path'],'match':'full_HTML_value_whitespace_normalized'})
rows=[{'resourceId':r['resourceId'],'locale':r['locale'],'sourceDigest':r['sourceDigest'],'matches':out.get(i,[])} for i,r in enumerate(base)]
(HERE/'stale_source_cache_bindings.json').write_text(json.dumps({'rows':rows},ensure_ascii=False,indent=2)+'\n')
print({'staleBodies':len(base),'exactHistoricalBindings':len(out)})
