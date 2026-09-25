#!/usr/bin/env python3
import collections,hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
BASE=json.loads((HERE/'body_baseline.json').read_text())['rows']
IDS={'7227375714401','7227378925665','7229026304097'}
PATCH={('7227375714401','he'):{'Father XXL':'אבא XXL'},('7227378925665','el'):{'ροές φορέματα':'ανάλαφρα φορέματα','Ροές φορέματα':'Ανάλαφρα φορέματα'},('7229026304097','el'):{'κηπουρικά πάρτι':'πάρτι στον κήπο'}}
rows=[];dispositions=[];checks=[];blocked=[]
def key(r):return (r['resourceId'].split('/')[-1],r['locale'])
def numcells(s,locale="en"):return [[ot.numbers(c['text'],locale) for c in row[1:]] for t in ot.Shape(s).tables for row in t['rows']]
for r in BASE:
 if key(r)[0] not in IDS or r['locale'] in ['ru','sv']:continue
 src=r['source'];before=r['before']['value'];a,b=ot.Shape(src),ot.Shape(before)
 extra_tags=sorted(set(re.findall(r'</?([^\s>/]+)',before))-set(re.findall(r'</?([^\s>/]+)',src))-{'img'})
 numeric_before=before.replace('כ-','כ ') if r['locale']=='he' else before
 numeric_equal=numcells(src)==numcells(numeric_before,r['locale'])
 copied=sorted(set(t.strip() for t in a.text)&set(t.strip() for t in b.text));copied=[x for x in copied if len(re.findall('[a-zA-Z]{3,}',x))>1]
 d={k:r[k] for k in ['resourceId','locale','key','sourceDigest']};d.update({'sourceSHA256':hashlib.sha256(src.encode()).hexdigest(),'beforeSHA256':hashlib.sha256(before.encode()).hexdigest(),'sourceTables':len(a.tables),'existingTables':len(b.tables),'extraTranslatedMarkupTags':extra_tags,'measurementCellsMatchSourceExcludingLabelColumn':numeric_equal,'sourceCopiedMultiwordNodes':copied,'proseReview':'Main paragraph and product bullet meanings reviewed against supplied English source. No new shipping, price, fiber or return claims identified.','freshnessLimit':'Saved inventory snapshot only; source digest and before-value must be rechecked by release owner.'})
 if extra_tags or len(b.tables)!=1:
  d['disposition']='HELD_MALFORMED_OR_DUPLICATED_TRANSLATED_TABLE';d['blocker']='Current translation contains translated HTML element names and/or duplicate chart. A whole-body translation update must first reconcile a single valid localized chart against the unchanged source measurement cells.'
  blocked.append({**r,**d,'proposal':'Normalize translated HTML tags to canonical tags, keep one localized chart only after per-cell numeric/unit equivalence, preserve source option codes, remove duplicated English chart. Do not apply numeric substitutions automatically.'})
 elif key(r) in PATCH:
  after=before;patches=[]
  for old,new in PATCH[key(r)].items():
   count=after.count(old);assert count>0,(key(r),old);after=after.replace(old,new);patches.append({'before':old,'after':new,'count':count})
  assert ot.Shape(before).events==ot.Shape(after).events
  assert numcells(before,r['locale'])==numcells(after,r['locale'])
  rows.append({**r,'value':after,'marketId':None,'method':'manual_narrow_semantic_or_English_label_repair_preserving_existing_localized_body','textPatches':patches})
  checks.append({**d,'beforeAfterHtmlAttributesUrlsNumericCellsIdentical':True,'sourceCheck':ot.verify_text(src,after,r['locale']),'limit':'Existing localized image alt/URLs differ from current English source, preserved. Hebrew unit aliases may be unrecognized. Candidate edits do not introduce these inherited differences.'})
  d['disposition']='NARROW_REPAIR_CANDIDATE'
 else:
  assert numeric_equal,(key(r),'numeric mismatch requires diagnosis')
  assert not copied,(key(r),copied)
  d['disposition']='NO_LANGUAGE_REPAIR_REQUIRED';d['outdatedFlagDisposition']='Existing wording remains semantically equivalent. No mutation proposed solely to clear the outdated marker. Existing source-image/attribute differences are historical and not claimed reconciled.'
 dispositions.append(d)
for name,value in [('older_stale_bodies_dispositions',{'counts':dict(collections.Counter(d['disposition'] for d in dispositions)),'rows':dispositions}),('older_stale_table_holds',{'status':'HOLD_FOR_SOURCE_CHART_RECONCILIATION','rows':blocked}),('older_stale_narrow_candidate',{'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows}),('older_stale_narrow_checks',checks),('older_stale_narrow_rollback',[{'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows])]:
 (HERE/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(dict(collections.Counter(d['disposition'] for d in dispositions)));print(hashlib.sha256((HERE/'older_stale_narrow_candidate.json').read_bytes()).hexdigest())
