from pathlib import Path
from html.parser import HTMLParser
import json,html,re,hashlib,runpy,copy,sys
O=Path(__file__).resolve().parent;P=O.parents[2]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
work=load(O/'worklist38.json')['rows'];texts=load(O/'source_texts.json');T={}
for f in sorted(O.glob('manual_*.py')):
 for k,v in runpy.run_path(str(f))['TEXT'].items():assert k not in T;T[k]=v
roles={'es':{'Child':'Niño','Girl':'Niña','Boy':'Niño','Mother':'Madre','Father':'Padre','Adult':'Adulto'},'fr':{'Child':'Enfant','Girl':'Fille','Boy':'Garçon','Mother':'Mère','Father':'Père','Adult':'Adulte'},'it':{'Child':'Bambino','Girl':'Bambina','Boy':'Bambino','Mother':'Madre','Father':'Padre','Adult':'Adulto'},'nl':{'Child':'Kind','Girl':'Meisje','Boy':'Jongen','Mother':'Moeder','Father':'Vader','Adult':'Volwassene'},'pl':{'Child':'Dziecko','Girl':'Dziewczynka','Boy':'Chłopiec','Mother':'Mama','Father':'Tata','Adult':'Dorosły'},'pt-BR':{'Child':'Criança','Girl':'Menina','Boy':'Menino','Mother':'Mãe','Father':'Pai','Adult':'Adulto'}}
def label(t,l):
 m=re.fullmatch(r'(Mother|Father|Adult) (S|M|L|XL|[2-5]XL)',t)
 if m:return roles[l][m[1]]+' '+m[2]
 m=re.fullmatch(r'(Child|Girl|Boy) (\d+(?:-\d+)?) Years?',t)
 if m:
  n=m[2];age={'es':'años','fr':'ans','it':'anni','nl':'jaar','pl':('lata' if n=='1-2' or ('-' not in n and 2<=int(n)<=4) else 'lat'),'pt-BR':'anos'}[l]
  if n=='1':age={'es':'año','fr':'an','it':'anno','nl':'jaar','pl':'rok','pt-BR':'ano'}[l]
  return roles[l][m[1]]+' '+n+' '+age
 return None
class Parser(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.events=[];self.stack=[];self.errors=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('end',t))
  if self.stack and self.stack[-1]==t:self.stack.pop()
  else:self.errors.append((t,self.stack.copy()))
 def handle_startendtag(self,t,a):self.events.append(('empty',t,a))
num=lambda s:re.findall(r'\d+(?:[.,]\d+)?',html.unescape(re.sub('<[^>]+>','',s)))
def build(r):
 key=r['productIndex'],r['locale'];s=r['source'];m=dict(zip(texts[str(key[0])],T[key]));assert len(texts[str(key[0])])==len(T[key]),(key,len(texts[str(key[0])]),len(T[key]));assert len(set(texts[str(key[0])]))==len(m)
 parts=re.split('(<[^>]+>)',s);pairs=[]
 for i in range(0,len(parts),2):
  old=parts[i];v=old.strip()
  if not v:continue
  target=m.get(v)
  if target is None:target=label(v,key[1])
  if target is None:
   assert not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',v)),('untranslated',key,v)
   continue
  leading=len(old)-len(old.lstrip());trailing=len(old)-len(old.rstrip());parts[i]=old[:leading]+html.escape(target,quote=False)+(old[-trailing:] if trailing else '')
  pairs.append({'textNodeIndex':i//2,'source':v,'target':target})
 value=''.join(parts)
 return value,pairs
rawcache={}
def validate(r):
 s,v=r['source'],r['value'];assert s==r['sourceValue'] and sha(s)==r['sourceSHA256'];assert sha(r['before']['value'])==r['beforeValueSHA256'];assert sha(v)==r['valueSHA256'];assert re.findall('<[^>]+>',s)==re.findall('<[^>]+>',v);assert num(s)==num(v)
 rf=P/r['rawFile'];assert fs(rf)==r['rawFileSHA256']
 if rf not in rawcache:rawcache[rf]={n['resourceId']:n for n in load(rf)['data']['translatableResourcesByIds']['nodes']}
 n=rawcache[rf][r['resourceId']];sr=next(t for t in n['translatableContent'] if t['key']=='body_html');assert sr['value']==s and sr['digest']==r['sourceDigest'];assert next(t for t in n['tr_'+r['locale'].replace('-','_')] if t['key']=='body_html')==r['before']
 a,b=Parser(s),Parser(v);assert a.events==b.events;assert not b.errors and not b.stack and not b.rawdata,(r['productIndex'],r['locale'],b.errors,b.stack)
 sr=[re.findall('<td\\b[^>]*>(.*?)</td>',row,re.S) for row in re.findall('<tr\\b[^>]*>(.*?)</tr>',s,re.S)];tr=[re.findall('<td\\b[^>]*>(.*?)</td>',row,re.S) for row in re.findall('<tr\\b[^>]*>(.*?)</tr>',v,re.S)];assert len(sr)==len(tr);
 for x,y in zip(sr,tr):
  assert len(x)==len(y)
  for a,b in zip(x[1:],y[1:]):
   if a==b:continue
   assert re.fullmatch(r'Up to [0-9.]+ kg / [0-9.]+ lbs',a) and b==html.escape(dict(zip(texts[str(r['productIndex'])],T[r['productIndex'],r['locale']]))[a],quote=False),(r['productIndex'],r['locale'],a,b)
   assert re.findall(r'[0-9.]+|kg|lbs',a)==re.findall(r'[0-9.]+|kg|lbs',b)
 assert re.findall(r'https?://[^\s<>"\']+',s)==re.findall(r'https?://[^\s<>"\']+',v)
 rebuilt,pairs=build(r);assert rebuilt==v
 return pairs
rows=[];pairs=[];checks=[]
for w in work:
 if (w['productIndex'],w['locale']) not in T:continue
 value,pp=build(w);r={**w,'marketId':None,'rawBefore':w['before'],'expectedBeforeValueSHA256':sha(w['before']['value']),'value':value,'valueSHA256':sha(value),'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'AUTHOR_COMPLETE_EXACT_CURRENT_SOURCE_PENDING_INDEPENDENT_FULL_MEANING_REVIEW','reason':'Complete manual translation of exact current English source, including source uncertainty and workflow notes. Current source markup/attributes/measurement cells retained; role/age size labels translated without altering identifiers.'};verified=validate(r);assert pp==verified;rows.append(r);pairs.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'sourceDigest':r['sourceDigest'],'nodes':pp});checks.append({'productIndex':r['productIndex'],'locale':r['locale'],'sourceRawBeforeHashes':'PASS','sourceMarkupAttributesAllNumericTokens':'PASS','sourceMeasurementValuesUnitsExactOnlyUpToLabelLocalized':'PASS','completeSourceTextNodeCoverage':len(pp),'independentStandardHTMLParser':'PASS'})
version=sys.argv[1] if len(sys.argv)>1 else 'progress'
for filename,data in [(f'candidate_{version}.json',{'rows':rows}),(f'node_pairs_{version}.json',{'rows':pairs}),(f'checks_{version}.json',{'status':'AUTHOR_PASS_PENDING_INDEPENDENT_REVIEW','rows':checks,'sourceEnglishChanged':False,'externalWrites':0})]:
 p=O/filename;assert not p.exists(),('preserve frozen file',p);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sourceNodes':sum(len(p['nodes']) for p in pairs),'file':f'candidate_{version}.json','sha256':fs(O/f'candidate_{version}.json')}))
