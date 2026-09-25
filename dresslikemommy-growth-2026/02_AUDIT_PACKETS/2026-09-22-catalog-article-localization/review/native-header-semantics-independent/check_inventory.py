import json,re,hashlib,unicodedata,collections
from pathlib import Path
from html.parser import HTMLParser
O=Path(__file__).resolve().parent;P=O.parents[1];A=P/'review/native-header-semantics'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fsha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class CellParser(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tables=[];self.active=False;self.row=None;self.cell=None;self.feed(s);self.close()
 def handle_starttag(self,t,a):
  if t=='table':self.tables.append([]);self.active=True
  elif t=='tr' and self.active:self.row=[];self.tables[-1].append(self.row)
  elif t in ('td','th') and self.row is not None:
   a=dict(a);self.cell={'tag':t,'colspan':a.get('colspan','1'),'rowspan':a.get('rowspan','1'),'text':''};self.row.append(self.cell)
 def handle_data(self,t):
  if self.cell is not None:self.cell['text']+=t
 def handle_endtag(self,t):
  if t in ('td','th'):self.cell=None
  elif t=='tr':self.row=None;self.cell=None
  elif t=='table':self.active=False;self.row=None;self.cell=None
 def get(self):
  for t in self.tables:
   for r in t:
    for c in r:c['text']=' '.join(c['text'].split())
  return self.tables
nums=lambda s:tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',unicodedata.normalize('NFKC',s)))
base={(r['resourceId'],r['locale']):r for r in json.loads((P/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows']}
eff={(r['resourceId'],r['locale']):r for r in json.loads((A/'effective_body_values.json').read_text())['rows']}
pairs=json.loads((A/'source_bound_pairs.json').read_text())['rows'];sources={};targets={};relations={};count=0;current=0;methods=collections.Counter();rawcache={}
for pair in pairs:
 for u in pair['uses']:
  k=u['resourceId'],u['locale'];r=base[k];v=eff[k]
  assert sha(r['source'])==r['sourceSHA256']==u['sourceSHA256'];assert r['sourceDigest']==u['sourceDigest']==v['sourceDigest'];assert sha(v['value'])==v['effectiveValueSHA256']==u['effectiveValueSHA256']
  if k not in targets:targets[k]=CellParser(v['value']).get()
  if k[0] not in sources:sources[k[0]]=CellParser(r['source']).get()
  tc=targets[k][u['targetTableIndex']][u['targetRowIndex']][u['targetCellIndex']]
  assert tc['tag']=='th' and tc['text']==u['targetHeader']==pair['targetHeader']
  assert u['sourceHeader']==pair['sourceHeader'];assert len({s['sourceHeader'] for s in u['sourceMatches']})==1
  for sm in u['sourceMatches']:
   sc=sources[k[0]][sm['sourceTableIndex']][sm['sourceRowIndex']][sm['sourceCellIndex']]
   assert sc['tag']=='th' and sc['text']==u['sourceHeader']
   rel=(k,sm['sourceTableIndex'],u['targetTableIndex'])
   if rel in relations:continue
   st=sources[k[0]][sm['sourceTableIndex']];tt=targets[k][u['targetTableIndex']]
   assert len(st)==len(tt);headers=None;used=collections.Counter()
   for sr,tr in zip(st,tt):
    assert [(c['tag'],c['colspan'],c['rowspan']) for c in sr]==[(c['tag'],c['colspan'],c['rowspan']) for c in tr]
    if all(c['tag']=='th' for c in sr):headers=(sr,tr);continue
    for ci,(sc,tc) in enumerate(zip(sr,tr)):
     if sc['tag']!='td' or ci==0:continue
     sn,tn=nums(sc['text']),nums(tc['text'])
     if sn==tn:used['identicalNumericSequence']+=1;continue
     if len(sn)>1 and sorted(sn)==sorted(tn):used['sameNumericMultisetWithinCell']+=1;continue
     if headers and len(headers[0])==len(sr) and re.search(r'\((?:cm|kg)\)',headers[1][ci]['text']) and '/' in sc['text'] and nums(sc['text'].split('/',1)[0])==tn:used['explicitMetricOnlyProjection']+=1;continue
     raise AssertionError((rel,ci,sc,tc))
   relations[rel]=dict(used);methods.update(used)
  count+=1;current+=not u['effectiveOutdated']
assert count==42430 and len(pairs)==4010
report={'status':'PASS_SOURCE_COLUMN_CORRESPONDENCE_ONLY_MEANING_REVIEW_PENDING','sourceBoundOccurrences':count,'currentSourceBoundOccurrences':current,'effectiveOutdatedBoundOccurrences':count-current,'uniqueLocaleSourceTargetPairs':len(pairs),'uniqueSourceTargetTableRelations':len(relations),'numericComparisonMethods':dict(methods),'sizeLabelColumnSkipped':'Separate reviewed size156 lane; source and target header meaning remains explicitly matched.','inputFiles':{f:fsha(A/f) for f in ['source_bound_pairs.json','effective_body_values.json','inventory_summary.json']},'limitations':['Inventory baseline ends at structural375/header2028. Final candidate binding must include subsequent released overlays before qualification.','2,209 unmatched header occurrences and 31 separately assigned native occurrences excluded from this correspondence proof.','This check proves source column identity, not accuracy of current labels or proposed translations.']}
(O/'inventory_binding_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
