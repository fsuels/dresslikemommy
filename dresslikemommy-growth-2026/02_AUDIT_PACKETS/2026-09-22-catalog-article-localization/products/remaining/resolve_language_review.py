#!/usr/bin/env python3
"""Bind manual dispositions for every statistical review flag; no network or live writes."""
import collections,hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent;PRODUCTS=HERE.parent
sys.path.insert(0,str(PRODUCTS.parent/'tooling'))
import offline_translation as ot
review=list(map(json.loads,(PRODUCTS/'language_review_candidates.jsonl').read_text().splitlines()))
nodes={n['resourceId']:(f.name,n) for f in PRODUCTS.glob('translations_batch_*json') for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']}
body=json.loads((HERE/'body_baseline.json').read_text())['rows']
fields={(r['resourceId'],r['locale']):r for r in json.loads((HERE/'body_segment_fields.json').read_text())}
short_values={
 '7533348618337':'Одевайтесь одинаково с дочкой в хлопковые пижамы Bird Chirping с фруктовым садом — топ на пуговицах с короткими рукавами + шорты, размеры 2Y–10Y и S–XL. Выберите комплект.',
 '7533351272545':'Одевайтесь одинаково с дочкой в пижамы Good Night Song of the Sea из хлопковой марли — топ с короткими рукавами + шорты, размеры 2Y–10Y и S–XL. Выберите комплект.',
 '7537002971233':'Парный семейный комплект терракотового цвета с эффектом льна для мамы, папы, девочек и мальчиков. Размеры платьев, рубашек и топов: 2Y-10Y, мама S-4XL, папа S-4XL.',
 '7537367679073':'Tops'
}
short=[];smallbody=[];dispositions=[]
smallbodyids={'7534719860833','7534826520673'}
falsebodyids={'7670724329569','7670744842337'}
for rv in review:
 fn,n=nodes[rv['resourceId']];src=next(x for x in n['translatableContent'] if x['key']==rv['key']);before=next(x for x in n['tr_'+rv['locale'].replace('-','_')] if x['key']==rv['key'] and x['locale']==rv['locale'] and x.get('market') is None)
 r={'resourceId':rv['resourceId'],'productId':rv['productId'],'locale':rv['locale'],'key':rv['key'],'source':src['value'],'sourceDigest':src['digest'],'before':before,'rawFile':fn,'auditReasons':rv['reasons']}
 id=r['resourceId'].split('/')[-1]
 if r['key'] in {'meta_description','product_type'}:
  if id in short_values:
   short.append({**r,'value':short_values[id],'marketId':None,'method':'manual_review_of_invariant_or_statistical_false_positive_revealed_semantic_defect'})
   reason='Wrong-language classification disproved, but concrete mistranslation repaired: idiomatic match-your-child meaning, linen-look qualifier, or stale Spanish family phrase.'
   status='SEMANTIC_CORRECTION_CANDIDATE'
  else:
   status='WRONG_LANGUAGE_FALSE_POSITIVE_NO_CHANGE';reason='Grammatical Russian copy with English named designs and size codes. Those invariant terms do not establish wrong language. No material meaning defect identified in this narrow comparison.'
 elif id in smallbodyids and r['locale']=='ru':
  values={'Age':'Возраст','Hip':'Бёдра','Picture-Perfect Print:':'Принт для удачных фотографий:'}
  chunks=re.split(r'(<[^>]+>)',before['value']);patches=[]
  for i in range(0,len(chunks),2):
   text=re.sub(r'\s+',' ',html.unescape(chunks[i])).strip()
   if text not in values:continue
   v=values[text];chunks[i]=re.match(r'^\s*',chunks[i]).group()+v+re.search(r'\s*$',chunks[i]).group();patches.append({'before':text,'after':v})
  smallbody.append({**r,'value':''.join(chunks),'marketId':None,'method':'manual_three_remaining_English_labels_only','textNodePatches':patches})
  status='WHOLE_LANGUAGE_FALSE_POSITIVE_THREE_LABEL_FIX';reason='Main prose is Russian; only Age, Hip and Picture-Perfect Print remained English. All three exact labels repaired; other text and markup untouched.'
 elif id in falsebodyids and r['locale']=='ru':
  status='WRONG_LANGUAGE_FALSE_POSITIVE_NO_CHANGE';reason='Product prose and labels are Russian; no exact English source text spans remain. Numeric table/code content biased statistical language prediction. Source-content/operator-copy quality is separate from this language classification.'
 else:
  status='CONFIRMED_ENGLISH_BODY_COPY';reason='Exact copied English text or manually verified English paragraphs split across inline tags are visible in the localized body. Bound to body_baseline.json for candidate composition; statistical score is not the sole evidence.'
 dispositions.append({**rv,'disposition':status,'reason':reason})
for name,rr in [('language_review_short_fixes',short),('russian_body_label_fixes',smallbody)]:
 f=HERE/(name+'_candidate.json');f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rr},ensure_ascii=False,indent=2)+'\n')
 checks=[]
 for r in rr:
  check={'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'check':ot.verify_text(r['source'],r['value'],r['locale'])}
  if name=='russian_body_label_fixes':
   check['sourceUnitAliasCheck']=ot.verify_text(r['source'],r['value'].replace('фунта','lbs'),r['locale'])
   check['unitAliasNote']='Existing correctly inflected Russian фунта means pounds. Supplemental check normalizes that one existing unit spelling only in memory; saved candidate text remains unchanged.'
   check['beforeAfterTagsAndAttributesUnchanged']=ot.Shape(r['before']['value']).events==ot.Shape(r['value']).events
   check['beforeAfterNumericCellsAndUnitsUnchanged']=ot.table_facts(ot.Shape(r['before']['value']),'ru')==ot.table_facts(ot.Shape(r['value']),'ru')
  checks.append(check)
 (HERE/(name+'_checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 (HERE/(name+'_rollback.json')).write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'marketId':None,'action':'restore','value':r['before']['value']} for r in rr],ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'file':f.name,'rows':len(rr),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
summary={'allFlags':len(review),'byDisposition':dict(collections.Counter(x['disposition'] for x in dispositions)),'scope':'All 337 frozen statistical/invariant review candidates individually bound to raw locale-filtered global translations. Detection is triage, not semantic certification. Exact source copies and manual review determine disposition.','rows':dispositions}
(HERE/'language_review_dispositions.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'}))
