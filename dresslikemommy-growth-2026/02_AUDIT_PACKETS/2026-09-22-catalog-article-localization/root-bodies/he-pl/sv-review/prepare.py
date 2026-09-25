from pathlib import Path
import json,hashlib,re,html,importlib.util
P=Path(__file__).parent;PACK=P.parents[2];SV=PACK/'tooling/sv-bodies'
# Path parent chain: sv-review -> he-pl -> root-bodies -> packet
assert (PACK/'articles/raw').is_dir()
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
release=PACK/'review/article_release_index_final.json';released=json.loads(release.read_text());done={(r['resourceId'],r['locale'],r['key']) for r in released['rows']}
manifest=json.loads((SV/'final_manifest.json').read_text());rows=[];files=[]
for b in manifest['finalBatches']:
 f=SV/b['file'];assert sha(f)==b['sha256'];rr=json.loads(f.read_text())['rows'];assert len(rr)==b['rows'];rows+=rr;files.append({'path':str(f),'SHA256':sha(f)})
selected=[r for r in rows if(r['resourceId'],r['locale'],r['key'])not in done];assert len(selected)==55
raw={};rawfiles=[]
for f in sorted((PACK/'articles/raw').glob('translations_sv_*.json')):
 d=json.loads(f.read_text());rawfiles.append({'path':str(f),'SHA256':sha(f)})
 for n in d['data']['translatableResourcesByIds']['nodes']:raw[n['resourceId']]=n
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[];pairs={};joins={}
for r in selected:
 n=raw[r['resourceId']];s=next(x for x in n['translatableContent'] if x['key']=='body_html' and x['locale']=='en');errors=[]
 for field,rawv in [('sourceValue',s['value']),('sourceDigest',s['digest'])]:
  if r[field]!=rawv:errors.append('raw_'+field+'_mismatch')
 tr=[x for x in n.get('translations',[]) if x['locale']=='sv' and x['key']=='body_html' and x.get('market') is None]
 before=tr[0]['value'] if tr else None
 if r['before']!=before:errors.append('raw_before_mismatch')
 v=m.verify_text(r['sourceValue'],r['value'],'sv');errors+=v['errors'];checks.append({'resourceId':r['resourceId'],'errors':errors,'sourceDigest':r['sourceDigest'],'sourceSHA256':hashlib.sha256(r['sourceValue'].encode()).hexdigest(),'valueSHA256':hashlib.sha256(r['value'].encode()).hexdigest(),'rawBefore':before})
 def seg(t):return[html.unescape(x).strip() for x in re.findall(r'(?<=>)[^<]+(?=<)|^[^<]+(?=<)|(?<=>)[^<]+$',t)if x.strip()]
 ss,tt=seg(r['sourceValue']),seg(r['value']);assert len(ss)==len(tt)
 for s,t in zip(ss,tt):pairs.setdefault((s,t),[]).append(r['resourceId'])
 for z in re.findall(r'<(?:p|li)\b[^>]*>.*?</(?:p|li)>',r['value'],re.S):
  if '<a 'in z:
   t=html.unescape(re.sub('<[^>]+>',' ',z));t=re.sub(r'\s+',' ',t).strip();joins.setdefault(t,[]).append(r['resourceId'])
out=[{'i':i,'source':s,'target':t,'resourceIds':list(dict.fromkeys(ids))} for i,((s,t),ids) in enumerate(pairs.items())]
for name,data in [('selection.json',{'status':'STRUCTURE_AND_RAW_BINDING_PASS' if not any(r['errors']for r in checks)else'FAILED','selectedRows':len(selected),'excludedAlreadyReviewed':len(rows)-len(selected),'releaseIndexSHA256':sha(release),'candidateFiles':files,'rawFiles':rawfiles,'rows':checks}),('pairs.json',out),('inline_paragraphs.json',[{'i':i,'text':t,'resourceIds':list(dict.fromkeys(ids))}for i,(t,ids) in enumerate(joins.items())]),('selected_candidate.json',{'rows':selected})]:
 (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print({'selected':len(selected),'pairs':len(out),'pairChars':sum(len(s)+len(t)for s,t in pairs),'joins':len(joins),'errors':[r for r in checks if r['errors']]})
