# -*- coding: utf-8 -*-
import copy,hashlib,html,json,re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dump=lambda f,d:(H/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
plain=lambda s:html.unescape(re.sub('<[^>]*>','',s)).strip()
key=lambda r:(r['resourceId'],r['locale'])
files=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_v2.json','review/size-label-repair/candidate_all156.json','review/size-label-repair/placeholder-review/placeholder88_reviewed.json','review/body-structure-audit/prose_completion11_candidates_v1.json']
overlays=[(f,fs(R/f),{key(r):r for r in load(R/f)['rows']}) for f in files]
inv={key(r):r for r in load(R/'review/body-structure-audit/effective_body_inventory.json')['rows']}
findings=load(R/'review/body-header-localization/native_header_alignment_holds.json')['rows']
def cells(v):
 out={}
 for ti,t in enumerate(re.finditer(r'<table\b[^>]*>(.*?)</table>',v,re.S)):
  for ri,row in enumerate(re.finditer(r'<tr\b[^>]*>(.*?)</tr>',t[1],re.S)):
   for ci,c in enumerate(re.finditer(r'<(td|th)\b[^>]*>(.*?)</\1>',row[1],re.S)):
    pos=t.start(1)+row.start(1)+c.start(2);out[ti,ri,ci]={'tag':c[1],'html':c[2],'plain':plain(c[2]),'start':pos,'end':pos+len(c[2])}
 return out
groups=defaultdict(list);deferred=[]
for r in findings:
 if r['effectiveOutdated']:deferred.append({**r,'status':'FULL_CURRENT_BODY_RECONSTRUCTION_IN_PROGRESS','actualIssue':'P211 top-only source versus old two-piece description and obsolete10-column chart.' if r['productIndex']==211 else 'P213 source kg/lbs versus old jin weight column plus stale prose; source variant workflow preserved faithfully, no new product fact invented.'})
 elif r['productIndex'] in [164,206] and r['locale']=='fi':deferred.append({**r,'status':'SOURCE_DIMENSION_UNPROVED_NO_USER_PERMISSION_GATE','actualIssue':'No current English table on P164; P206 first target table is an extra obsolete10-column chart absent from current7-column source. Yarn→hip would infer dimension without current source-column evidence.'})
 else:groups[key(r)].append(r)
rows=[];ledger=[];cache={}
for k,work in groups.items():
 original=inv[k];before=original['before'];assert before['outdated'] is False
 rawp=R/original['rawFile'];assert fs(rawp)==original['rawFileSHA256']
 if rawp not in cache:cache[rawp]=load(rawp)
 n=next(n for n in cache[rawp]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==k[0]);s=next(t for t in n['translatableContent'] if t['key']=='body_html');b=next(t for t in n['tr_'+k[1].replace('-','_')] if t['key']=='body_html' and not t['market'])
 assert s['value']==original['source'] and s['digest']==original['sourceDigest'] and b==before
 baseline=original['expectedEffectiveBeforeValue'];deps=[]
 for path,digest,index in overlays:
  if k in index:
   ov=index[k];expected=ov.get('expectedEffectiveBeforeValue',ov.get('before',{}).get('value') if ov.get('before') else None)
   assert expected==baseline,(k,path,'overlay before')
   baseline=ov['value'];deps.append({'file':path,'fileSHA256':digest,'valueSHA256':sha(baseline)})
 c=cells(baseline);sourcecells=cells(s['value']);patches=[]
 for r in work:
  pos=(r['targetTableIndex'],r['targetRowIndex'],r['targetCellIndex']);old=c[pos];assert old['tag']=='th' and old['plain']==r['beforeLabel']
  after=r['proposedLabel'];proof='UNAMBIGUOUS_NATIVE_SPELLING_OR_LANGUAGE_CORRECTION_PRESERVING_EXISTING_DIMENSION'
  if r['productIndex']==160:
   assert s['value'] and sourcecells[pos]['plain']=='Skirt Length (cm/in)'
   # All data values pair with current English table; decimal separators alone normalize.
   num=lambda z:re.findall(r'\d+(?:\.\d+)?',z.replace(',','.'))
   assert set(c)==set(sourcecells)
   assert all(num(c[x]['plain'])==num(sourcecells[x]['plain']) for x in c if c[x]['tag']=='td')
   after='Délka sukně';proof='CURRENT_ENGLISH_SKIRT_LENGTH_AND_COMPLETE_NUMERIC_TABLE_ALIGNMENT'
  new=old['html'].replace(r['beforeLabel'],after,1);assert new!=old['html']
  entry={**r,'afterLabel':after,'oldHTML':old['html'],'newHTML':new,'start':old['start'],'end':old['end'],'proof':proof,'sourceHeaderAtSameCoordinates':sourcecells.get(pos,{}).get('plain'),'existingDimensionOnly':r['productIndex']!=160}
  patches.append(entry);ledger.append(entry)
 value=baseline
 for p in sorted(patches,key=lambda p:p['start'],reverse=True):value=value[:p['start']]+p['newHTML']+value[p['end']:]
 back=value
 # Compare all non-header bytes and all measurements without reconstructing author substitutions.
 strip=lambda v:re.sub(r'(<th\b[^>]*>).*?(</th>)',r'\1\2',v,flags=re.S)
 assert strip(value)==strip(baseline)
 assert re.findall(r'<td\b.*?</td>',value,re.S)==re.findall(r'<td\b.*?</td>',baseline,re.S)
 assert re.findall(r'<[^>]*>',value)==re.findall(r'<[^>]*>',baseline)
 assert re.findall(r'\d+(?:[.,]\d+)?',value)==re.findall(r'\d+(?:[.,]\d+)?',baseline)
 row={'resourceId':k[0],'locale':k[1],'key':'body_html','marketId':None,'productIndex':original['productIndex'],'source':s['value'],'sourceValue':s['value'],'sourceDigest':s['digest'],'sourceSHA256':sha(s['value']),'rawFile':original['rawFile'],'rawFileSHA256':original['rawFileSHA256'],'rawBefore':before,'before':None if deps else before,'expectedEffectiveBeforeValue':baseline,'expectedEffectiveBeforeValueSHA256':sha(baseline),'expectedBeforeValueSHA256':sha(baseline),'beforeValueSHA256':sha(baseline),'value':value,'valueSHA256':sha(value),'plannedBeforeDependencies':deps,'requiresFreshEffectiveBeforeObject':bool(deps),'requiresFreshLiveSourceAndBeforeGuard':True,'nativeHeaderRepairs':patches,'reviewStatus':'AUTHOR_COMPLETE_MANUALLY_DIMENSION_REVIEWED_PENDING_ROOT_INDEPENDENT_REVIEW','reason':'Exact native spelling/language fixes preserve dimensions; CS160 additionally restores source Skirt Length from full-table numeric proof. All non-header bytes, measurements, tables, markup, attributes, links and images remain unchanged. Existing legacy-chart discrepancies are not represented as resolved.'}
 rows.append(row)
assert len(rows)==19 and len(ledger)==22 and len(deferred)==9
dump('current22_candidates.json',{'rows':rows});dump('current22_cell_ledger.json',{'rows':ledger});dump('remaining9_worklist.json',{'rows':deferred})
dump('current22_checks.json',{'status':'PASS_AUTHOR_AND_MANUAL_DIMENSION_REVIEW_PENDING_ROOT','bodyRows':19,'headerOccurrences':22,'allRawSourceDigestBeforeBindings':True,'allNonHeaderBytesExact':True,'allMeasurementCellsNumbersMarkupAttributesURLsImagesExact':True,'CS160SourceCompleteNumericTableProof':True,'overlays':{f:h for f,h,_ in overlays},'candidateSHA256':fs(H/'current22_candidates.json'),'remaining':{'fullBodyReconstructions':7,'unprovedHipDimensions':2}})
print(json.dumps({'rows':19,'occurrences':22,'candidateSHA256':fs(H/'current22_candidates.json')}))
