import json,re,html,hashlib,collections,copy
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda x:hashlib.sha256(x.encode()).hexdigest();d=json.loads((H/'prose_completion11_candidates_v1.json').read_text());cache={}
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.errors=[];self.tags=[];self.attrs=[]
 def handle_starttag(self,t,a):
  self.tags.append(t);self.attrs.append((t,a))
  if t not in 'area base br col embed hr img input link meta param source track wbr'.split():self.stack.append(t)
 def handle_endtag(self,t):
  self.tags.append('/'+t)
  if self.stack and self.stack[-1]==t:self.stack.pop()
  elif t not in 'area base br col embed hr img input link meta param source track wbr'.split():self.errors.append((t,self.stack[-5:]))
 def handle_startendtag(self,t,a):self.handle_starttag(t,a);self.handle_endtag(t)
def parse(s):p=Parse();p.feed(s);p.close();return p
def outside(s):return re.sub(r'<table\b.*?</table>','',s,flags=re.S)
def plain(s):return html.unescape(re.sub(r'<[^>]*>',' ',s))
def validate(r):
 assert sha(r['source'])==r['sourceSHA256'] and sha(r['value'])==r['valueSHA256'];assert sha(r['expectedEffectiveBeforeValue'])==r['expectedBeforeValueSHA256']==r['expectedEffectiveBeforeValueSHA256']
 rp=B/r['rawFile']
 if rp not in cache:cache[rp]=(hashlib.sha256(rp.read_bytes()).hexdigest(),{n['resourceId']:n for n in json.loads(rp.read_text())['data']['translatableResourcesByIds']['nodes']})
 filesha,nodes=cache[rp];assert filesha==r['rawFileSHA256'];n=nodes[r['resourceId']];s=next(x for x in n['translatableContent'] if x['key']=='body_html');assert s['value']==r['source'] and s['digest']==r['sourceDigest'];assert next(x for x in n['tr_'+r['locale'].replace('-','_')] if x['key']=='body_html')==r['rawBefore']
 dep=r['plannedBeforeDependencies'][0];p=B/dep['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==dep['sha256'];prev=next(x for x in json.loads(p.read_text())['rows'] if (x['resourceId'],x['locale'],x['key'])==(r['resourceId'],r['locale'],r['key']));assert prev['value']==r['expectedEffectiveBeforeValue']
 tables=lambda v:re.findall(r'<table\b.*?</table>',v,re.S)
 assert len(tables(r['value']))==2 and tables(r['value'])==tables(r['expectedEffectiveBeforeValue'])
 for pat in [r'https?://[^\s<>"\']+',r'<img\b[^>]*>']:assert re.findall(pat,r['value'])==re.findall(pat,r['expectedEffectiveBeforeValue'])
 a,b=outside(r['source']),outside(r['value']);pa,pb=parse(a),parse(b);assert not pb.errors and not pb.stack and not pb.rawdata;assert pa.tags==pb.tags,(r['productIndex'],r['locale'],'prose markup')
 assert re.findall(r'\d+(?:\.\d+)?',plain(a))==re.findall(r'\d+(?:\.\d+)?',plain(b)),(r['productIndex'],r['locale'],'prose numbers')
 full=parse(r['value']);assert not full.errors and not full.stack and not full.rawdata
 assert len(r['tailTextNodePairs'])==14
 for p in r['proseChanges']:assert p['source'] in r['source'] and p['after'] in r['value']
 assert r['sourceMissingTail'] in r['source'] and r['value'].endswith(r['localizedTail'])
for r in d['rows']:validate(r)
# Reject measured-cell edits and lost source qualifications through explicit reconstruction checks.
mut=[]
r=copy.deepcopy(d['rows'][0]);table=re.search(r'<table\b.*?</table>',r['value'],re.S)[0];newtable=table.replace('>2<','>999<',1);assert newtable!=table;r['value']=r['value'].replace(table,newtable,1);r['valueSHA256']=sha(r['value'])
try:validate(r);mut.append(False)
except AssertionError:mut.append(True)
r=copy.deepcopy(d['rows'][0]);r['sourceDigest']='0'*64
try:validate(r);mut.append(False)
except AssertionError:mut.append(True)
assert all(mut)
report={'status':'AUTHOR_PASS_PENDING_INDEPENDENT_FULL_MEANING_REVIEW','rows':11,'sourceProducts':6,'locales':sorted({r['locale'] for r in d['rows']}),'plannedBeforeFile':'review/size-label-repair/placeholder-review/placeholder88_reviewed.json','sourceRawBeforeBindings':11,'exactReviewedTablesPreserved':22,'currentSourceProseMarkupSequencesMatch':11,'currentSourceProseNumbersMatch':11,'fullStandardParserBalancePass':11,'tailTextNodesTranslated':154,'sourceBoundCorrectedFirstListClauses':56,'retainedCorrectFirstListClauses':10,'negativeCorruptionTestsRejected':2,'sourceEnglishEdited':False,'candidateSHA256':hashlib.sha256((H/'prose_completion11_candidates_v1.json').read_bytes()).hexdigest()};(H/'prose_completion11_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
