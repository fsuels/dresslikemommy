from pathlib import Path
import re,json,hashlib,html
from html.parser import HTMLParser
from manual_photo_updates import ADDITIONS,TIMING
from meaning_corrections import PATCHES
OUT=Path(__file__).resolve().parent
BASE=OUT.parent.parent
WORK=BASE/'root-bodies/he-pl/remaining-review/other_body_worklist.json'
rows=json.loads(WORK.read_text())['rows']
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def translated_nodes(source,values):
 parts=re.split(r'(<[^>]*>)',source);i=0
 for n,p in enumerate(parts):
  if not p.startswith('<') and p.strip():
   lead=p[:len(p)-len(p.lstrip())];trail=p[len(p.rstrip()):]
   parts[n]=lead+html.escape(values[i],quote=False)+trail;i+=1
 assert i==len(values),(i,len(values))
 return ''.join(parts)
class Shape(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.events=[];self.text=[];self.links=[];self.feed(s)
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t=='a':self.links.append(dict(a).get('href'))
 def handle_endtag(self,t):self.events.append(('end',t))
 def handle_startendtag(self,t,a):self.events.append(('single',t,a))
 def handle_data(self,d):self.text.append(d)
values=[];checks=[];changes=[]
for row in rows:
 raw=(BASE/row['rawFile']).read_text();assert sha(raw)==row['rawFileSHA256']
 nodes=json.loads(raw)['data']['translatableResourcesByIds']['nodes'];node=next(n for n in nodes if n['resourceId']==row['resourceId'])
 source=next(x for x in node['translatableContent'] if x['key']==row['key'])
 assert source['value']==row['sourceValue'] and source['digest']==row['sourceDigest']
 before=next(x for x in node['translations'] if x['key']==row['key'] and x['locale']==row['locale'] and x.get('market') is None);assert before==row['before']
 locale=row['locale'];src=row['sourceValue'];change=[]
 if row['resourceId'].endswith('559471919201'):
  val=before['value']
  for old,new in PATCHES[locale]:
   assert old in val,(locale,'missing exact semantic patch',old)
   count=val.count(old);val=val.replace(old,new);change.append({'before':old,'after':new,'count':count})
  block=src[src.index("<h2>Plan each person's outfit"):src.index('<h2>The Golden Rule')]
  added=translated_nodes(block,ADDITIONS[locale])
  second=list(re.finditer(r'<p\b[^>]*>.*?</p>',val,re.S))[1]
  val=val[:second.end()]+'\n\n'+added+val[second.end():]
  # Existing photo translations have only the old photographer-tips ordered list.
  ols=list(re.finditer(r'<ol>.*?</ol>',val,re.S));assert len(ols)==2
  ol=ols[-1];li=re.search(r'<li>.*?</li>',ol[0],re.S);assert li
  heading,body=TIMING[locale];updated='<li>\n<strong>'+html.escape(heading,quote=False)+'</strong> — '+html.escape(body,quote=False)+'</li>'
  val=val[:ol.start()+li.start()]+updated+val[ol.start()+li.end():]
  change.append({'sourceUpdate':'Added current20text-node planning section; replaced obsolete two-week advice with current destination delivery estimate and try-on time'})
 else:
  translations=(OUT/'manual_fr_valentine.txt').read_text().strip().splitlines();assert len(translations)==45
  val=translated_nodes(src,translations);change.append({'sourceUpdate':'Full45text-node current-source French rewrite; old shipping threshold and two-to-three-week deadline removed because absent from current source'})
 a,b=Shape(src),Shape(val)
 assert a.events==b.events,(locale,row['resourceId'],'markup/attributes')
 assert a.links==b.links,(locale,'links')
 numbers=lambda obj:re.findall(r'\d+',html.unescape(' '.join(obj.text)))
 assert numbers(a)==numbers(b),(locale,'number mismatch',numbers(a),numbers(b))
 assert src!=val and before['value']!=val
 rel=f'review/other-article-bodies/{locale}_{row["resourceId"].split("/")[-1]}.html';(BASE/rel).write_text(val)
 entry={'ledgerId':row['ledgerId'],'resourceId':row['resourceId'],'locale':locale,'key':row['key'],'marketId':None,'source':src,'sourceDigest':row['sourceDigest'],'sourceSHA256':sha(src),'before':before,'expectedBeforeValueSHA256':sha(before['value']),'value':val,'valueSHA256':sha(val),'rawFile':row['rawFile'],'rawFileSHA256':row['rawFileSHA256'],'candidateFile':rel,'candidateFileSHA256':sha(val),'bindingReviewCode':'EXACT_SOURCE_DIGEST_GLOBAL_BEFORE_AND_RAW_SHA256_BOUND','authorMeaningReviewCode':'FULL_CURRENT_SOURCE_AND_EXISTING_BODY_READ_WITH_MANUAL_SOURCE_DELTA_AND_MEANING_REPAIRS','structureReviewCode':'EXACT_HTML_EVENTS_ATTRIBUTES_LINK_SEQUENCE_AND_NUMERIC_TOKENS','independentMeaningReview':'PENDING_ROOT_OR_OTHER_NONAUTHOR','requiresFreshLiveSourceAndBeforeGuard':True}
 values.append(entry);checks.append({'ledgerId':row['ledgerId'],'resourceId':row['resourceId'],'locale':locale,'sourceBinding':True,'beforeBinding':True,'htmlEvents':len(a.events),'linkSequence':a.links,'numericTokens':numbers(a),'candidateSHA256':sha(val)});changes.append({'ledgerId':row['ledgerId'],'resourceId':row['resourceId'],'locale':locale,'changes':change})
assert len(values)==16 and len({(x['resourceId'],x['locale'],x['key']) for x in values})==16
(OUT/'candidate.json').write_text(json.dumps({'status':'16_AUTHOR_REVIEWED_BOUND_MANUAL_CANDIDATES_REQUIRING_INDEPENDENT_MEANING_REVIEW','worklistFile':str(WORK.relative_to(BASE)),'worklistSHA256':sha(WORK.read_text()),'rows':values},ensure_ascii=False,indent=2)+'\n')
(OUT/'checks.json').write_text(json.dumps({'status':'PASS','rows':checks},ensure_ascii=False,indent=2)+'\n')
(OUT/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('PASS16 exact source/digest/global-before/raw-bound candidates; HTML events/attributes/links/numeric tokens identical to current source.')
