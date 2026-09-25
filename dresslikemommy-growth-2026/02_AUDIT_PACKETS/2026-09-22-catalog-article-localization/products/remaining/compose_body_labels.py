#!/usr/bin/env python3
"""Prepare lossless body-text patches, not release-ready whole-body translations."""
import collections,hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent;PRODUCTS=HERE.parent
base=json.loads((HERE/'body_baseline.json').read_text())['rows']
d=json.loads((HERE/'body_label_dictionary.json').read_text());keys=d.pop('sourceKeys');labels={loc:dict(zip(keys,vs)) for loc,vs in d.items()}
roles=json.loads((PRODUCTS/'option_dictionary.json').read_text())
name_pairs={}
for f in [PRODUCTS/'option_cohort_candidate.json',PRODUCTS/'simple_copy_cohort_candidate.json',HERE/'option_misc_candidate.json']:
 for r in json.loads(f.read_text())['rows']:
  if r['key']=='name':name_pairs[(r['locale'],r['source'])]=r.get('value',r.get('after'))
aliases={'Hip':'Hips','Suggested Height':'Recommended Height','Suggested Weight':'Recommended Weight','Clothing Length':'Coat Length','Garment Length':'Coat Length','Pants Length':'Pant Length','Shoulder':'Shoulder Width'}
def norm(t):return re.sub(r'\s+',' ',html.unescape(t)).strip()
def translate(loc,t):
 if (loc,t) in name_pairs:return name_pairs[(loc,t)]
 if t in labels[loc]:return labels[loc][t]
 if t.lower()=='cotton':return labels[loc]['Cotton'].lower()
 if t=='100% cotton':return '100% '+labels[loc]['Cotton'].lower()
 if t in aliases:return labels[loc][aliases[t]]
 m=re.fullmatch(r'(.+?)(\s*\((?:cm|in|kg|lbs?|\s|/)+\))',t)
 if m:
  key=aliases.get(m[1],m[1])
  if key in labels[loc]:return labels[loc][key]+m[2]
 m=re.fullmatch(r'(Mother|Father|Adult|Child)\s+([1-5]?X{0,4}[SL]|[SML])',t)
 if m:return roles[loc][m[1]]+' '+m[2]
 if t.endswith(':') and t[:-1] in labels[loc]:return labels[loc][t[:-1]]+':'
 return None
out=[];counts=collections.Counter()
for idx,r in enumerate(base):
 if not r['before']:continue
 before=r['before']['value'];pieces=re.split(r'(<[^>]+>)',before);patches=[]
 for i in range(0,len(pieces),2):
  t=norm(pieces[i]);v=translate(r['locale'],t) if t else None
  if v is None or v==t:continue
  lead=re.match(r'^\s*',pieces[i]).group();tail=re.search(r'\s*$',pieces[i]).group()
  pieces[i]=lead+html.escape(v,quote=False)+tail
  patches.append({'textNodeIndex':i//2,'before':t,'after':v});counts[r['locale']]+=1
 after=''.join(pieces)
 assert re.findall(r'<[^>]+>',before)==re.findall(r'<[^>]+>',after)
 assert re.findall(r'\d+(?:[.,]\d+)?',before)==re.findall(r'\d+(?:[.,]\d+)?',after)
 if patches:out.append({**r,'value':after,'marketId':None,'bodyIndex':idx,'textNodePatches':patches,'status':'INCOMPLETE_FOR_COMPOSITION_NOT_RELEASE_READY','method':'manual_semantic_labels_and_previous_reviewed_size_terms','limits':'Only exact text nodes changed. All original HTML tags, attributes, numeric cells and other text retained byte-for-byte. English prose or stale source differences may remain.'})
f=HERE/'body_label_partial_candidates.json';f.write_text(json.dumps({'status':'INCOMPLETE_FOR_COMPOSITION_NOT_RELEASE_READY','rows':out},ensure_ascii=False,indent=2)+'\n')
report={'fieldsPartiallyPatched':len(out),'textNodeReplacements':sum(counts.values()),'byLocale':dict(counts),'originalTagsAttributesAndNumbersUnchanged':True,'candidateSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'notReleaseReady':'Requires full per-field source/claim/prose disposition and composition before registration.'}
(HERE/'body_label_partial_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
