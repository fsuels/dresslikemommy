import pathlib,json,hashlib,re,html,sys,collections
P=pathlib.Path(__file__).resolve().parent;PACK=P.parent.parent;AUTHOR=P.parent/'product-title-completeness-b'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();filehash=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();loads=lambda f:json.loads(f.read_text())
def norm(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',s))).strip()
locale=sys.argv[1];name=sys.argv[2]if len(sys.argv)>2 else f'candidate_{locale}_v1.json';f=AUTHOR/name;obj=loads(f);rows=obj if isinstance(obj,list)else obj['rows'];candidatehash=filehash(f)
config=loads(P/f'corrections_{locale}.json')if(P/f'corrections_{locale}.json').exists()else{};corrections=[];checks=[];reviewed=[];holds=[]
for row in rows:
 r=dict(row);errors=[];raw=PACK/r['rawFile'];wfile=PACK/r['inputWorklistFile'];rawobj=loads(raw);nodes=rawobj['data']['translatableResourcesByIds']['nodes'];node=next(n for n in nodes if n['resourceId']==r['resourceId']);source=next(x for x in node['translatableContent']if x['key']=='title');body=next(x for x in node['translatableContent']if x['key']=='body_html');rawbefore=next((x for x in node['tr_'+r['locale'].replace('-','_')]if x['key']=='title'),None);work=next(x for x in loads(wfile)['rows']if x['i']==r['i'])
 for ok,label in [(filehash(raw)==r['rawFileSHA256'],'RAW_FILE_SHA'),(filehash(wfile)==r['inputWorklistFileSHA256'],'WORKLIST_FILE_SHA'),(source['value']==r['sourceValue']==r['source'],'SOURCE_VALUE'),(source['digest']==r['sourceDigest'],'SOURCE_DIGEST'),(sha(source['value'])==r['sourceSHA256'],'SOURCE_SHA'),(rawbefore==r['rawBefore'],'RAW_BEFORE_OBJECT'),(work['effectiveBeforeValue']==r['effectiveBeforeValue'],'EFFECTIVE_BEFORE_VALUE'),(sha(r['effectiveBeforeValue'] or'')==r['expectedBeforeValueSHA256']==r['expectedEffectiveBeforeValueSHA256'],'EFFECTIVE_BEFORE_SHA'),(r['before']==work['before'],'BEFORE_OBJECT'),(sha(r['value'])==r['valueSHA256'],'AUTHOR_VALUE_SHA')]:
  if not ok:errors.append(label)
 if r.get('overlayApplied'):
  overlay=PACK/r['overlaySourceFile']
  if filehash(overlay)!=r['overlaySourceFileSHA256']:errors.append('OVERLAY_SHA')
  match=[x for x in loads(overlay)if x['resourceId']==r['resourceId']and x['locale']==r['locale']and x['key']=='title']
  if len(match)!=1 or match[0]['value']!=r['effectiveBeforeValue']:errors.append('OVERLAY_VALUE')
 for key,digest in r.get('supportingSourceDigests',{}).items():
  s=next(x for x in node['translatableContent']if x['key']==key)
  if s['digest']!=digest:errors.append('SUPPORTING_DIGEST_'+key)
 def walk(v):
  if isinstance(v,dict):
   if 'exactQuoteNormalizedWhitespace'in v and v['exactQuoteNormalizedWhitespace']not in norm(body['value']):errors.append('EXACT_BODY_QUOTE')
   if 'bodyValueSHA256'in v and v['bodyValueSHA256']!=sha(body['value']):errors.append('BODY_SHA')
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(r)
 change=config.get(str(r['i']))
 if change:
  r['value']=change['value'];r['valueSHA256']=sha(r['value']);r['independentMeaningCorrection']=change['reason'];corrections.append({'i':r['i'],'tuple':[r['resourceId'],r['locale'],'title',None],'sourceValue':r['sourceValue'],'authorValue':row['value'],'reviewedValue':r['value'],'reason':change['reason']})
  if change.get('bodyQuote'):
   assert change['bodyQuote']in norm(body['value']);r.setdefault('supportingSourceDigests',{})['body_html']=body['digest'];r['independentAdditionalBodyEvidence']={'bodyValueSHA256':sha(body['value']),'exactQuoteNormalizedWhitespace':change['bodyQuote']}
 r['independentReviewStatus']='INDEPENDENT_FULL_TITLE_MEANING_AND_EXACT_BINDINGS_PASS'if not errors else'HELD_BINDING_FAILURE';r['independentReviewedFromFile']='review/product-title-completeness-b/'+name;r['independentReviewedFromFileSHA256']=candidatehash;r['independentReviewMethod']='Read full source/effective-before/proposed title; review garment, role, design, printed text, material, color, complete generic words and clipped fragment fidelity. Preserve source/body before/digest guards.'
 checks.append({'i':r['i'],'tuple':[r['resourceId'],r['locale'],'title',None],'bindingFailures':errors,'meaning':'CORRECTED_PASS'if change else'PASS','corrected':bool(change)})
 (holds if errors else reviewed).append(r)
for nameout,data in [(f'{locale}_reviewed.json',{'rows':reviewed}),(f'{locale}_corrections.json',{'rows':corrections}),(f'{locale}_holds.json',{'rows':holds})]:
 (P/nameout).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
report={'authorFile':'review/product-title-completeness-b/'+name,'authorFileSHA256':candidatehash,'rowsIndependentlyCompared':len(rows),'qualifiedRows':len(reviewed),'correctionRows':len(corrections),'heldRows':len(holds),'allBindingsPass':not holds,'reviewedFile':f'{locale}_reviewed.json','reviewedSHA256':filehash(P/f'{locale}_reviewed.json'),'checks':checks,'externalWrites':'NONE','liveFreshGuard':'ROOT_REQUIRED'};(P/f'{locale}_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in report.items()if k!='checks'})
