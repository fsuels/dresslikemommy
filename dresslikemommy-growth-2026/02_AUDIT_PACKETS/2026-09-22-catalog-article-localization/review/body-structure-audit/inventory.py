import json,re,html,hashlib,collections,difflib
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();filesha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
locales=['ar','cs','da','de','el','es','fi','fr','he','hi','it','ja','ko','nl','no','pl','pt-BR','ro','ru','sv']
a=json.loads((B/'review/product-title-completeness/worklist_it.json').read_text())['rows'];nodes={};rawcache={}
for r in a:
 p=B/r['rawFile']
 if p not in rawcache:rawcache[p]={n['resourceId']:n for n in json.loads(p.read_text())['data']['translatableResourcesByIds']['nodes']}
 nodes[r['resourceId']]=rawcache[p][r['resourceId']]
overlays={};overfiles=[]
for p in sorted((B/'review/root_released_bodies').glob('body_overlay_*.json')):
 rows=json.loads(p.read_text());overfiles.append({'file':str(p.relative_to(B)),'sha256':filesha(p),'count':len(rows)})
 for r in rows:
  k=(r['resourceId'],r['locale']);assert k not in overlays;overlays[k]=dict(r,overlayFile=str(p.relative_to(B)),overlayFileSHA256=filesha(p))
assert len(overlays)==327
allowed=set('a abbr acronym address applet area article aside audio b base basefont bdi bdo big blockquote body br button canvas caption center cite code col colgroup data datalist dd del details dfn dialog dir div dl dt em embed fieldset figcaption figure font footer form frame frameset h1 h2 h3 h4 h5 h6 head header hgroup hr html i iframe img input ins kbd label legend li link main map mark menu meta meter nav noframes noscript object ol optgroup option output p param picture pre progress q rp rt ruby s samp script search section select small source span strike strong style sub summary sup table tbody td template textarea tfoot th thead time title tr track tt u ul var video wbr'.split())
pat=re.compile(r'<\s*(/?)\s*([^\s<>/]+)(?:\s[^<>]*?)?\s*/?>')
def tags(v):
 v=re.sub(r'<!--.*?-->','',v,flags=re.S)
 return [{'name':m[2].lower(),'close':bool(m[1]),'literal':m[0],'position':m.start()} for m in pat.finditer(v) if m[2][0].isalpha()]
def seq(v):return [('' if not t['close'] else '/')+t['name'] for t in tags(v)]
def plain(v):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',v))).strip()
headpat=re.compile(r'<th(?:\s[^>]*)?>(.*?)</th\s*>',re.S|re.I)
english=re.compile(r'\b(?:Size|Height|Weight|Bust|Chest|Waist|Hips?|Length|Shoulder|Sleeve|Age|Recommended|Pants|Skirt|Dress|Tops?|Shorts|Inseam|Outseam|Category|Measurement|Head|Circumference|Child|Children|Baby|Mother|Father|Girl|Boy|Women|Men|Adults?)\b',re.I)
allrows=[];sourceinventory=[]
for j,r in enumerate(a):
 node=nodes[r['resourceId']];s=next(x for x in node['translatableContent'] if x['key']=='body_html');src=s['value'];st=tags(src);sunknown=sorted({t['name'] for t in st if t['name'] not in allowed});sseq=seq(src)
 src_escaped=re.findall(r'(?:&lt;|&#0*60;|&#x0*3c;)/?[^&<>]{1,60}(?:&gt;|&#0*62;|&#x0*3e;)',src,re.I)
 sourceinventory.append({'productIndex':j,'resourceId':r['resourceId'],'sourceDigest':s['digest'],'sourceSHA256':sha(src),'sourceUnknownOrMalformedTagNames':sunknown,'sourceEscapedTagLiterals':src_escaped,'sourceTagSequence':sseq})
 for loc in locales:
  before=next((v for v in node.get('tr_'+loc.replace('-','_'),[]) if v['key']=='body_html'),None);ov=overlays.get((r['resourceId'],loc));value=ov['value'] if ov else before['value'] if before else None
  row=dict(productIndex=j,resourceId=r['resourceId'],locale=loc,key='body_html',source=src,sourceDigest=s['digest'],sourceSHA256=sha(src),rawBefore=before,before=None if ov else before,expectedEffectiveBeforeValue=value,expectedEffectiveBeforeValueSHA256=sha(value) if value is not None else None,overlayApplied=bool(ov),overlayFile=ov['overlayFile'] if ov else None,overlayFileSHA256=ov['overlayFileSHA256'] if ov else None,rawFile=r['rawFile'],rawFileSHA256=r['rawFileSHA256'],onlineStoreUrl=r['onlineStoreUrl'])
  if value is None:row['classification']='MISSING_BODY';allrows.append(row);continue
  tt=tags(value);unknown=[t for t in tt if t['name'] not in allowed and t['name'] not in sunknown]
  inherited=[t for t in tt if t['name'] not in allowed and t['name'] in sunknown]
  escaped=re.findall(r'(?:&lt;|&#0*60;|&#x0*3c;)/?[^&<>]{1,60}(?:&gt;|&#0*62;|&#x0*3e;)',value,re.I)
  targetescaped=[v for v in escaped if v not in src_escaped]
  headers=[plain(h) for h in headpat.findall(value)];englishheaders=[h for h in headers if english.search(h)]
  tseq=seq(value);opcodes=[{'op':op,'sourceStart':i1,'sourceEnd':i2,'targetStart':j1,'targetEnd':j2,'sourceTags':sseq[i1:i2],'targetTags':tseq[j1:j2]} for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,sseq,tseq,autojunk=False).get_opcodes() if op!='equal']
  row.update(targetOnlyUnknownTags=unknown,inheritedUnknownTags=inherited,targetOnlyEscapedTags=targetescaped,englishFallbackHeaderCandidates=englishheaders,exactEnglishElementSequence=(sseq==tseq),elementSequenceDifferences=opcodes,sourceUnknownOrMalformedTagNames=sunknown,classification='TARGET_ONLY_UNKNOWN_OR_ESCAPED_TAGS' if unknown or targetescaped else 'ELEMENT_SEQUENCE_DIFF' if opcodes else 'ELEMENT_SEQUENCE_MATCH')
  allrows.append(row)
assert len(allrows)==4760
(H/'effective_body_inventory.json').write_text(json.dumps({'status':'FROZEN_RAW_PLUS327_VERIFIED_RELEASED_BODY_OVERLAYS','rows':allrows},ensure_ascii=False,indent=2)+'\n')
(H/'source_structure_inventory.json').write_text(json.dumps({'rows':sourceinventory},ensure_ascii=False,indent=2)+'\n')
unknownrows=[r for r in allrows if r.get('targetOnlyUnknownTags')];escapedrows=[r for r in allrows if r.get('targetOnlyEscapedTags')];headerrows=[r for r in allrows if r.get('englishFallbackHeaderCandidates')]
summary={'status':'INVENTORY_ONLY_REQUIRES_STRUCTURAL_CLASSIFICATION_NO_REPAIRS_YET','tuples':4760,'products':238,'locales':20,'releasedBodyOverlays':327,'missingBodies':sum(r['classification']=='MISSING_BODY' for r in allrows),'exactSourceElementSequence':sum(r.get('exactEnglishElementSequence',False) for r in allrows),'differentSourceElementSequence':sum(r.get('exactEnglishElementSequence') is False for r in allrows),'targetOnlyUnknownTagRows':len(unknownrows),'targetOnlyUnknownTagOccurrences':sum(len(r['targetOnlyUnknownTags']) for r in unknownrows),'unknownNames':dict(collections.Counter(t['name'] for r in unknownrows for t in r['targetOnlyUnknownTags'])),'targetOnlyEscapedTagRows':len(escapedrows),'englishHeaderCandidateRows':len(headerrows),'englishHeaderCandidateOccurrences':sum(len(r['englishFallbackHeaderCandidates']) for r in headerrows),'sourceUnknownTagProducts':sum(bool(r['sourceUnknownOrMalformedTagNames']) for r in sourceinventory),'sourceUnknownNames':dict(collections.Counter(t for r in sourceinventory for t in r['sourceUnknownOrMalformedTagNames'])),'unknownTagRowsByLocale':dict(collections.Counter(r['locale'] for r in unknownrows)),'overlayFiles':overfiles}
(H/'inventory_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(H/'unknown_tag_findings.json').write_text(json.dumps({'rows':[dict(productIndex=r['productIndex'],resourceId=r['resourceId'],locale=r['locale'],tags=r['targetOnlyUnknownTags'],escaped=r['targetOnlyEscapedTags'],englishHeaderCandidates=r['englishFallbackHeaderCandidates'],elementSequenceDifferences=r['elementSequenceDifferences']) for r in allrows if r.get('targetOnlyUnknownTags') or r.get('targetOnlyEscapedTags')]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='overlayFiles'},ensure_ascii=False))
