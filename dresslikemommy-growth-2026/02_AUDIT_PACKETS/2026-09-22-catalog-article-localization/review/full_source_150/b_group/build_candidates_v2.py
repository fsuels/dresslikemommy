import re,json,html,hashlib,runpy,collections
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;B=H.parents[2];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();W=json.loads((H/'worklist40.json').read_text())['rows'];P={x['productIndex']:x['nodes'] for x in json.loads((H/'source_prose_nodes.json').read_text())['rows']};D=runpy.run_path(str(H/'table_dictionary.py'));T={l:runpy.run_path(str(H/(f'prose_{l}_v2.py' if l in ['ar','ja'] else f'prose_{l}.py')))['TEXTS'] for l in ['ar','he','hi','ja','ko']}
raw=json.loads((B/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows'];R={(r['resourceId'],r['locale']):r for r in raw};effective={k:(r['expectedEffectiveBeforeValue'],[]) for k,r in R.items()}
files=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json','review/size-label-repair/candidate_root_reviewed156.json','review/size-label-repair/placeholder-review/placeholder88_root_bound.json','review/body-header-localization/prose-completion-review/prose_completion11_root_bound.json','review/native-header-final/current22_root_reviewed.json','review/native-header-semantics-independent/full7/full7_reviewed.json','review/native-header-semantics-independent/native_header2145_reviewed.json']
for f in files:
 p=B/f;fs=hashlib.sha256(p.read_bytes()).hexdigest()
 for r in json.loads(p.read_text())['rows']:
  k=r['resourceId'],r['locale'];v,dep=effective[k];effective[k]=(r['value'],dep+[{'file':f,'sha256':fs,'valueSHA256':sha(r['value'])}])
class Audit(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=False);self.events=[];self.feed(s)
 def handle_starttag(self,t,a):self.events.append(('start',t,a,self.get_starttag_text()))
 def handle_startendtag(self,t,a):self.events.append(('startend',t,a,self.get_starttag_text()))
 def handle_endtag(self,t):self.events.append(('end',t))
 def handle_comment(self,s):self.events.append(('comment',s))
num=lambda s:re.findall(r'\d+(?:\.\d+)?',s)
rows=[];checks=[];pairs=[];englishres=[]
for r in W:
 k=r['resourceId'],r['locale'];l=r['locale'];product=r['productIndex'];source=r['source'];rr=R[k];assert source==rr['source'];assert r['sourceDigest']==sha(source)==r['sourceSHA256'];assert rr['rawBefore']==r['before'];assert r['beforeValueSHA256']==sha(r['before']['value']);rawfile=B/'products'/r['rawFile'];rawfilesha=hashlib.sha256(rawfile.read_bytes()).hexdigest();assert rawfilesha==rr['rawFileSHA256']
 parts=re.split(r'(<[^>]*>)',source);translated=list(parts);nodes=P[product];assert len(nodes)==len(T[l][product]),(l,product,len(nodes),len(T[l][product]));prose_indices=set()
 for n,t in zip(nodes,T[l][product]):
  i=n['partIndex'];s=parts[i];assert html.unescape(s.strip())==n['sourceText'];lead=s[:len(s)-len(s.lstrip())];tail=s[len(s.rstrip()):];translated[i]=lead+html.escape(t,quote=False)+tail;prose_indices.add(i);pairs.append({'productIndex':product,'resourceId':k[0],'locale':l,'kind':'prose','nodeIndex':n['index'],'source':n['sourceText'],'target':t})
 intable=False;cell=None;tablesource=[];tabletarget=[]
 for i,s in enumerate(parts):
  if s.startswith('<table'):intable=True
  elif s.startswith('</table'):intable=False
  elif re.match(r'<(th|td)(?:\s|>)',s):cell=re.match(r'<(th|td)',s).group(1)
  elif s in ['</td>','</th>']:cell=None
  elif intable and cell and not s.startswith('<') and s.strip():
   text=html.unescape(s.strip());out=text
   if cell=='th':
    m=re.match(r'^(.*?)(\s*\([^()]*\))?$',text);base=m.group(1);suffix=m.group(2) or '';assert base in D['TABLE_MAP'][l],(base,l);out=D['TABLE_MAP'][l][base]+suffix
   elif re.match(r'^(Child|Mother|Father)\b',text):
    out=re.sub(r'^(Child|Mother|Father)\b',lambda m:D['ROLES'][l][m.group()],out)
    out=re.sub(r'\bYears?\b',D['YEARS'][l],out)
   elif text.startswith('Up to '):out=D['UP_TO'][l]+' '+text[len('Up to '):]
   elif re.fullmatch(r'[\d\-]+ Years?',text):out=re.sub(r'Years?',D['YEARS'][l],text)
   assert num(text)==num(out),(text,out)
   lead=s[:len(s)-len(s.lstrip())];tail=s[len(s.rstrip()):];translated[i]=lead+html.escape(out,quote=False)+tail
   pairs.append({'productIndex':product,'resourceId':k[0],'locale':l,'kind':cell,'partIndex':i,'source':text,'target':out});tablesource.append(text);tabletarget.append(out)
   if re.search(r'[A-Za-z]{3,}',out) and re.search(r'[A-Za-z]{3,}',re.sub(r'\b(?:cm|in|kg|lbs|XL)\b','',out)):englishres.append({'productIndex':product,'locale':l,'source':text,'target':out})
 value=''.join(translated);assert Audit(source).events==Audit(value).events;assert num(source)==num(value);assert not re.search('QZXTOKEN|QZX|XTOKEN',value);assert num(' '.join(tablesource))==num(' '.join(tabletarget))
 # Numeric/unit-only cells are exactly source strings; empty cells and all tags remain untouched.
 for x,y in zip(tablesource,tabletarget):
  if not re.search(r'Child|Mother|Father|Years?|Up to',x) and not any(x==h or x.startswith(h+' (') for h in D['HEADERS']):assert x==y,(x,y)
 before,deps=effective[k];out={z:rr[z] for z in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']};out.update({'sourceValue':source,'marketId':None,'before':None,'expectedEffectiveBeforeValue':before,'expectedEffectiveBeforeValueSHA256':sha(before),'beforeValueSHA256':sha(before),'expectedBeforeValueSHA256':sha(before),'value':value,'valueSHA256':sha(value),'plannedBeforeDependencies':deps,'requiresFreshEffectiveBeforeObject':True,'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'FULL_CURRENT_SOURCE_MANUAL_TRANSLATION_PENDING_INDEPENDENT_REVIEW','reason':'Full current English source translated including every qualification about unknown composition, source access, selected garment scope and workflow. Exact current source HTML/attributes/comments/tables/measurement values/units retained. Replaces stale source clauses and all leftover English prose; no English source edited.','manualProseFile':f'prose_{l}_v2.py' if l in ['ar','ja'] else f'prose_{l}.py','manualProseFileSHA256':hashlib.sha256((H/(f'prose_{l}_v2.py' if l in ['ar','ja'] else f'prose_{l}.py')).read_bytes()).hexdigest()});rows.append(out)
 checks.append({'productIndex':product,'locale':l,'sourceRawBeforeDigestBindings':True,'sourceHTMLTagsAttributesCommentsExact':True,'allSourceTableNumericTokensExact':True,'allSourceMeasurementCellsUnitsExact':True,'allProseNodesTranslated':len(nodes),'tableNodes':len(tablesource),'noPlaceholderArtifacts':True,'beforeOutdated':r['before']['outdated'],'sourceMetaAdminBreadcrumbPreserved':product==215})
summary={'rows':len(rows),'products':len({r['resourceId'] for r in rows}),'locales':dict(collections.Counter(r['locale'] for r in rows)),'proseNodes':sum(x['allProseNodesTranslated'] for x in checks),'tableNodes':sum(x['tableNodes'] for x in checks),'unresolvedEnglishTableText':englishres,'requiresRootFreshBeforeAfterNative2145':True}
assert not englishres,englishres
for name,obj in [('candidates40_v2.json',{'summary':summary,'rows':rows}),('checks40_v2.json',{'summary':summary,'rows':checks}),('node_pairs40_v2.json',{'rows':pairs})]:(H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(summary);print('candidateSHA',hashlib.sha256((H/'candidates40_v2.json').read_bytes()).hexdigest())
