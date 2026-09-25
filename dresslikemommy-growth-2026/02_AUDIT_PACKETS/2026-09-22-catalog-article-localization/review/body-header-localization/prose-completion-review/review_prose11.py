import copy,hashlib,html,json,re
from pathlib import Path
from html.parser import HTMLParser
OUT=Path(__file__).resolve().parent
PACK=OUT.parents[2]
AUTHOR=PACK/'review/body-structure-audit/prose_completion11_candidates_v1.json'
BASE=PACK/'review/size-label-repair/placeholder-review/placeholder88_reviewed.json'
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def fsha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d):
 p=OUT/name;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return fsha(p)
assert fsha(AUTHOR)=='1f02da30ede31cd4c0bbcaf94e1413796c201eeaf3befb2c3da37e9a68b0bc2a'
assert fsha(BASE)=='e51ef0fa972b3a03d84a1b77af7b9fb0e0c88532c14cb756e897e7f8ac0a9fda'
key=lambda r:(r['resourceId'],r['locale'],r['key'])
authored=json.loads(AUTHOR.read_text())['rows'];baseline={key(r):r for r in json.loads(BASE.read_text())['rows']}
rows=copy.deepcopy(authored);corr=[]

def apply(r,old,new,source,reason):
 assert r['value'].count(old)==1,(r['productIndex'],old)
 assert source in r['source']
 r['value']=r['value'].replace(old,new,1)
 for pair in r['tailTextNodePairs']:
  if old in pair['value']:pair['value']=pair['value'].replace(old,new)
 for pair in r['proseChanges']:
  if old in pair['after']:pair['after']=pair['after'].replace(old,new)
 r['localizedTail']=r['localizedTail'].replace(old,new)
 corr.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'sourceQuote':source,'authorText':old,'reviewedText':new,'reason':reason})
for r in rows:
 if (r['productIndex'],r['locale'])==(166,'el'):
  apply(r,'για ένα ευκολοφόρετο cargo στο χρώμα του φασκόμηλου με ευρύχωρες τσέπες με καπάκι.','για ένα cargo στο χρώμα του φασκόμηλου που φοριέται τραβώντας το προς τα πάνω, με ευρύχωρες τσέπες με καπάκι.','pull-on sage cargo shorts with roomy flap pockets.','Retain explicit pull-on construction, not only generally easy-to-wear.')
  apply(r,'Ασορτί επιλογές για όλη την οικογένεια:','Ασορτί επιλογές για τέσσερις οικογενειακούς ρόλους:','Four-Role Matching:','Retain four family roles explicitly; this does not imply exactly four people.')
  apply(r,'Σορτς που φοριέται εύκολα, με ευρύχωρες τσέπες με καπάκι και άνετο, πρακτικό χαρακτήρα για δραστήριες ημέρες.','Σορτς που φοριέται τραβώντας το προς τα πάνω, με ευρύχωρες τσέπες με καπάκι και άνετο, πρακτικό χαρακτήρα για δραστήριες ημέρες.','Pull-on shorts with roomy flap pockets and an easy utility feel for active days.','Retain explicit pull-on construction in corresponding feature text.')
 if (r['productIndex'],r['locale'])==(171,'el'):
  old=re.findall(r'<li\b.*?</li>',r['value'],re.S)[2]
  new='<li>\n<strong>Μοτίβο:</strong> Το «Citrus Bloom» συνδυάζει ζωγραφιστά κίτρινα λουλούδια εσπεριδοειδών, μπλε πέταλα και φυλλώδεις λεπτομέρειες σε απαλό γαλάζιο φόντο, για μια φωτεινή παλέτα έτοιμη για φωτογραφίες.</li>'
  src=re.findall(r'<li\b.*?</li>',r['source'],re.S)[2]
  apply(r,old,new,src,'Fabric print ground means background, not earth; also replace printing-process label with pattern and retain every color/motif.')
  assert 2 in r['retainedFirstListItemOrdinals'];r['retainedFirstListItemOrdinals'].remove(2)
  r['proseChanges'].append({'ordinal':2,'source':src,'before':re.findall(r'<li\b.*?</li>',r['expectedEffectiveBeforeValue'],re.S)[2],'after':new,'reason':'Independent review: print/ground wording corrected.'})
 r['valueSHA256']=sha(r['value']);r['independentReviewStatus']='QUALIFIED_EXACT_SOURCE_FULL_PROSE_AND_PRESERVED_CHARTS'
 r['reviewStatus']='INDEPENDENT_REVIEW_PASS_PENDING_ROOT_FRESH_GUARD'
 r['independentReview']={'reviewer':'article_he_pl_complete','authorFile':str(AUTHOR.relative_to(PACK)),'authorFileSHA256':fsha(AUTHOR),'authorValueSHA256':next(a['valueSHA256'] for a in authored if key(a)==key(r)),'correctionCount':sum(key(c)==key(r) for c in corr),'scope':'Full current source prose, all 14 tail nodes and all six first-list clauses; exact planned-before charts and structural/source bindings.'}

class Parse(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.errors=[];self.events=[];self.data=[]
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('end',t))
  if self.stack and self.stack[-1]==t:self.stack.pop()
  else:self.errors.append((t,self.stack.copy()))
 def handle_startendtag(self,t,a):self.events.append(('empty',t,a))
 def handle_data(self,d):self.data.append(d)
def parsed(t):
 p=Parse();p.feed(t);p.close();return p
def tables(t):return re.findall(r'<table\b[\s\S]*?</table>',t)
def outside(t):return re.sub(r'<table\b[\s\S]*?</table>','',t)
def nums(t):return re.findall(r'\d+(?:\.\d+)?',html.unescape(re.sub(r'<[^>]+>',' ',t)))
rawcache={};evidence=[]
def validate(r):
 assert r['source']==r['sourceValue'] and sha(r['source'])==r['sourceSHA256']
 assert sha(r['value'])==r['valueSHA256']
 bv=r['expectedEffectiveBeforeValue'];assert sha(bv)==r['beforeValueSHA256']==r['expectedBeforeValueSHA256']==r['expectedEffectiveBeforeValueSHA256']
 prev=baseline[key(r)];assert prev['value']==bv and prev['source']==r['source'] and prev['sourceDigest']==r['sourceDigest']
 rf=PACK/r['rawFile'];assert fsha(rf)==r['rawFileSHA256']
 if rf not in rawcache:rawcache[rf]={n['resourceId']:n for n in json.loads(rf.read_text())['data']['translatableResourcesByIds']['nodes']}
 node=rawcache[rf][r['resourceId']];src=next(t for t in node['translatableContent'] if t['key']==r['key'])
 assert src['value']==r['source'] and src['digest']==r['sourceDigest']
 assert next(t for t in node['tr_'+r['locale'].replace('-','_')] if t['key']==r['key'])==r['rawBefore']
 assert len(tables(r['value']))==2 and tables(bv)==tables(r['value'])
 for pattern in [r'https?://[^\s<>"\']+',r'<img\b[^>]*>']:
  assert re.findall(pattern,bv)==re.findall(pattern,r['value'])
 p=parsed(r['value']);assert not p.stack and not p.errors and not p.rawdata
 sa,va=outside(r['source']),outside(r['value']);assert parsed(sa).events==parsed(va).events
 assert nums(sa)==nums(va)
 a=next(a for a in authored if key(a)==key(r));assert parsed(a['value']).events==p.events
 assert re.findall(r'<[^>]+>',a['value'])==re.findall(r'<[^>]+>',r['value'])
 assert len(r['tailTextNodePairs'])==14
 sp=parsed(r['sourceMissingTail']);vp=parsed(r['localizedTail'])
 st=[x for x in sp.data if x.strip()];vt=[x for x in vp.data if x.strip()]
 assert st==[html.unescape(p['source']) for p in r['tailTextNodePairs']]
 assert vt==[html.unescape(p['value']) for p in r['tailTextNodePairs']]
 assert r['sourceMissingTail'] in r['source'] and r['value'].endswith(r['localizedTail'])
 for pair in r['proseChanges']:assert pair['source'] in r['source'] and pair['after'] in r['value']
 return {'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'rawFileSHA256':r['rawFileSHA256'],'beforeValueSHA256':sha(bv),'valueSHA256':r['valueSHA256'],'sourceRawAndPlannedBeforeBindings':'PASS','chartsByteExactPreserved':len(tables(bv)),'chartSHA256':[sha(x) for x in tables(bv)],'sourceProseNumericAndMarkupParity':'PASS','authorVersusReviewedMarkupAttributesParity':'PASS','imagesLinksPreserved':'PASS','fullHTMLParser':'PASS','fullProseManualMeaning':'PASS','tailTextNodePairs':len(st),'independentCorrections':r['independentReview']['correctionCount']}
for r in rows:evidence.append(validate(r))
negative=[]
for kind in ['changed_table_measurement','changed_source_digest','changed_before']:
 r=copy.deepcopy(rows[0])
 if kind=='changed_table_measurement':
  tab=tables(r['value'])[0];m=re.search(r'<td[^>]*>([^<]*\d[^<]*)</td>',tab);assert m;corrupt=tab[:m.start(1)]+'999'+tab[m.end(1):];r['value']=r['value'].replace(tab,corrupt);r['valueSHA256']=sha(r['value'])
 if kind=='changed_source_digest':r['sourceDigest']='0'*64
 if kind=='changed_before':r['expectedEffectiveBeforeValue']+=' '
 try:validate(r)
 except AssertionError:negative.append({'case':kind,'rejected':True})
 else:raise AssertionError('negative failed '+kind)
qh=save('prose_completion11_reviewed.json',{'rows':rows})
save('corrections.json',{'corrections':corr,'count':len(corr),'changedRows':len({key(c) for c in corr})})
report={'status':'PASS','rows':11,'sourceProducts':6,'locales':sorted({r['locale'] for r in rows}),'sourceFile':str(AUTHOR.relative_to(PACK)),'sourceFileSHA256':fsha(AUTHOR),'plannedBeforeFile':str(BASE.relative_to(PACK)),'plannedBeforeFileSHA256':fsha(BASE),'qualifiedFile':'prose_completion11_reviewed.json','qualifiedFileSHA256':qh,'tailTextNodesReviewed':154,'firstListClausesReviewed':66,'chartsByteExactPreserved':22,'correctionCount':len(corr),'correctedRows':len({key(c) for c in corr}),'negativeTests':negative,'sourceEnglishEdited':False,'providersOrAPIUsed':False,'sourcePolicyNotes':['P191 and P196 explicitly retain current source care-inference disclaimers; P176 current source does not contain this disclaimer.','P196 exact current Print source says resort-ready, not photo-ready; source statement was verified, initial proposed review change withdrawn.','Source listing/care assertions are faithfully translated; root owns source decisions and fresh live release guards.'],'rowEvidence':evidence}
save('independent_review.json',report)
print(json.dumps({k:report[k] for k in ['status','rows','tailTextNodesReviewed','firstListClausesReviewed','chartsByteExactPreserved','correctionCount','correctedRows','qualifiedFileSHA256']},ensure_ascii=False))
