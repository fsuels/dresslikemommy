import json,re,html,hashlib,collections,unicodedata
from pathlib import Path
H=Path(__file__).resolve().parent
inv=json.loads((H/'effective_body_inventory.json').read_text())['rows']; structural=json.loads((H/'tag_candidates_v3.json').read_text())['rows'];overlay={(r['resourceId'],r['locale']):r for r in structural}
letter=re.compile(r'(?<![\w])(?:XXXL|XXL|XXS|XS|[2-6]XL|XL|S|M|L)(?![\w])')
def text(s):return html.unescape(re.sub(r'<[^>]*>','',s)).strip()
def nums(s):return tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',unicodedata.normalize('NFKC',s)))
def normsize(s):return {'XXL':'2XL','XXXL':'3XL'}.get(s,s)
def rows(s):
 out=[]
 for ti,tm in enumerate(re.finditer(r'<table\b[^>]*>(.*?)</table>',s,re.S)):
  for ri,rm in enumerate(re.finditer(r'<tr\b[^>]*>(.*?)</tr>',tm[1],re.S)):
   cm=list(re.finditer(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',rm[1],re.S));cs=[text(c[1]) for c in cm]
   if len(cs)<2:continue
   sig=tuple(nums(c) for c in cs[1:]);count=sum(len(x) for x in sig)
   if count<2:continue
   out.append({'tableIndex':ti,'rowIndex':ri,'label':cs[0],'labelHTML':cm[0][1],'labelStart':tm.start(1)+rm.start(1)+cm[0].start(1),'labelEnd':tm.start(1)+rm.start(1)+cm[0].end(1),'cells':cs,'signature':sig,'letters':letter.findall(cs[0])})
 return out
findings=[];counts=collections.Counter();sources={};perbody=[]
for r in inv:
 source=sources.setdefault(r['productIndex'],rows(r['source'])); idx=collections.defaultdict(list)
 for sr in source:idx[sr['signature']].append(sr)
 ov=overlay.get((r['resourceId'],r['locale']));v=ov['value'] if ov else r['expectedEffectiveBeforeValue'];localcounts=collections.Counter()
 for tr in rows(v or ''):
  possible=idx.get(tr['signature'],[])
  if not possible:status='NO_EXACT_SOURCE_NUMERIC_SIGNATURE'
  elif len(possible)>1:status='AMBIGUOUS_DUPLICATE_SOURCE_NUMERIC_SIGNATURE'
  else:
   sr=possible[0]
   if not sr['letters'] and not tr['letters']:status='NO_EXPLICIT_SIZE_LETTERS'
   elif not sr['letters'] or not tr['letters']:status='LETTER_PRESENCE_OR_ROLE_DIFFERS'
   elif [normsize(x) for x in sr['letters']]==[normsize(x) for x in tr['letters']]:status='SIZE_LETTERS_MATCH'
   else:status='EXACT_NUMERIC_ROW_SIZE_LETTER_MISMATCH'
  counts[status]+=1;localcounts[status]+=1
  if status in ['EXACT_NUMERIC_ROW_SIZE_LETTER_MISMATCH','LETTER_PRESENCE_OR_ROLE_DIFFERS']:
   findings.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'outdated':r['before']['outdated'] if r['before'] else None,'status':status,'sourceDigest':r['sourceDigest'],'sourceRow':possible[0],'targetRow':tr,'plannedStructuralOverlay':bool(ov),'effectiveValueSHA256':hashlib.sha256((v or '').encode()).hexdigest()})
 perbody.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'counts':dict(localcounts)})
summary={'status':'INVENTORY_PENDING_SEMANTIC_ROLE_REVIEW','scopeBodies':4760,'structuralPlannedOverlayRows':375,'numericRowCounts':dict(counts),'findingRows':len(findings),'findingBodies':len({(r['resourceId'],r['locale']) for r in findings}),'byLocale':dict(collections.Counter(r['locale'] for r in findings)),'byProduct':dict(collections.Counter(r['productIndex'] for r in findings)),'findings':findings}
(H/'size_letter_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');(H/'size_letter_coverage.json').write_text(json.dumps({'rows':perbody},ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='findings'}))
