# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,html,importlib.util,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
rows=[r for r in json.loads((P/'translation_only_held_worklist.json').read_text())['rows'] if r['resourceId'].endswith('/7545279512673')]
sources=json.loads((P/'sunshine_unique_source_nodes.json').read_text());manual={}
for name in ['sunshine_manual_latin.tsv','sunshine_manual_other.tsv']:
 for line in (P/name).read_text().splitlines():
  locale,n,value=line.split('\t',2)
  if locale=='he':value=value.replace('פריטי לבוש תחתונים','פריטי לבוש לחלק הגוף התחתון')
  manual[locale,int(n)]=value
headers=[0,2,4,6,8,10,12,14,15,16,17,18,19,20,114,115,117,119,121,123]
for line in (P/'sunshine_headers.tsv').read_text().splitlines():
 locale,values=line.split('\t',1);vals=values.split('|');assert len(vals)==len(headers),(locale,len(vals))
 for i,value in zip(headers,vals):manual[locale,i]=value
roles={
'ar':['طفل','بالغ','سنوات'],'cs':['Dítě','Dospělý','let'],'da':['Barn','Voksen','år'],'el':['Παιδί','Ενήλικας','ετών'],'fi':['Lapsi','Aikuinen','vuotta'],'he':['ילדים','מבוגר','שנים'],'hi':['बच्चा','वयस्क','वर्ष'],'ja':['子ども','大人','歳'],'ko':['어린이','성인','세'],'nl':['Kind','Volwassene','jaar'],'no':['Barn','Voksen','år'],'pl':['Dziecko','Dorosły','lat'],'pt-BR':['Criança','Adulto','anos'],'ro':['Copil','Adult','ani'],'ru':['Ребёнок','Взрослый','лет'],'sv':['Barn','Vuxen','år']}
def mechanical(s,l):
 if re.fullmatch(r'[\d.]+',s) or re.fullmatch(r'(?:S|M|L|XL|2XL|3XL|4XL)/\d+',s):return s
 m=re.fullmatch(r'Adult (S|M|L|XL|2XL|3XL|4XL)',s)
 if m:return roles[l][1]+' '+m[1]
 m=re.fullmatch(r'Child (\d+(?:-\d+)?) Years',s)
 if m:
  n=m[1];word=roles[l][2]
  if l=='ar':return 'طفل – العمر بالسنوات: '+n
  if l=='he':return 'ילדים – גיל (בשנים): '+n
  if l=='cs' and n in ['2','3','4']:word='roky'
  if l=='ru' and n in ['2','3','4']:word='года'
  return roles[l][0]+' '+n+('' if l in ['ja','ko'] else ' ')+word
 return None
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
out=[];checks=[];review=[]
for r in rows:
 parts=re.split('(<[^>]*>)',r['source']);mapped=0
 for i,old in enumerate(parts):
  if not old.strip() or old.startswith('<'):continue
  ss=html.unescape(old.strip());idx=sources.index(ss);value=manual.get((r['locale'],11 if idx==120 else idx))
  if value is None:value=mechanical(ss,r['locale'])
  assert value is not None,(r['locale'],idx,ss)
  mapped+=1;lead=old[:len(old)-len(old.lstrip())];trail=old[len(old.rstrip()):];parts[i]=lead+html.escape(value,quote=False)+trail
  if not re.fullmatch(r'[\d.]+',ss):review.append({'resourceId':r['resourceId'],'locale':r['locale'],'source':ss,'value':value})
 value=''.join(parts);check=v.verify_text(r['source'],value,r['locale']);assert not check['errors'],(r['locale'],check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']};rr.update(sourceValue=r['source'],value=value,marketId=None,reason='Translate full current Sunshine Stripe source and source chart. Replace obsolete draft/variant prose and stale chart, preserving exact current fiber percentages, each-selection-is-one-shirt statement, excluded accessories and all measurements.',independentReview='FULL_SOURCE_AUTHOR_REVIEW_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'meaning':'FULL_SOURCE_AUTHOR_REVIEW_PASS','preservation':check,'textNodes':mapped,'sourceSHA256':hashlib.sha256(r['source'].encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest()})
assert len(out)==16
for name,data in [('held_sunshine16_candidate.json',{'rows':out}),('held_sunshine16_checks.json',{'fields':checks,'limits':'Exact source-bound translation does not independently substantiate the English vendor measurements; source facts unchanged. Root independently reviews, guards current source/before and applies.'}),('held_sunshine16_review_pairs.json',{'rows':review})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'preservationFailures':0}))
