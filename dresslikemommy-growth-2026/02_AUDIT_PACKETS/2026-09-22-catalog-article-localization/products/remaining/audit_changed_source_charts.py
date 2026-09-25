#!/usr/bin/env python3
import collections,hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'));import offline_translation as ot
rows=[]
for r in json.loads((HERE/'body_baseline.json').read_text())['rows']:
 if r['resourceId'].split('/')[-1] not in ['7545279512673','7545279840353'] or r['locale'] in ['ru','sv']:continue
 src=ot.Shape(r['source']);old=ot.Shape(r['before']['value']);diff=[]
 for ti in range(max(len(src.tables),len(old.tables))):
  aa=src.tables[ti]['rows'] if ti<len(src.tables) else [];bb=old.tables[ti]['rows'] if ti<len(old.tables) else []
  for ri in range(max(len(aa),len(bb))):
   a=aa[ri] if ri<len(aa) else [];b=bb[ri] if ri<len(bb) else []
   for ci in range(max(len(a),len(b))):
    s=a[ci]['text'] if ci<len(a) else None;t=b[ci]['text'] if ci<len(b) else None
    if s is None or t is None or ot.numbers(s)!=ot.numbers(t,r['locale']):diff.append({'table':ti,'row':ri,'column':ci,'sourceCell':s,'beforeCell':t,'sourceNumbers':ot.numbers(s) if s else [],'beforeNumbers':ot.numbers(t,r['locale']) if t else [],'note':'Positional comparison; column additions/removals may shift meanings. This is evidence, not an automatic cell substitution.'})
 rid=r['resourceId'].split('/')[-1]
 proseIssue='Source replaced vendor-reference/draft copy with product-facing size-chart and one-shirt guidance; translated body retains previous operational prose.' if rid=='7545279512673' else 'Current English source itself still describes draft variant/selector decisions; source cleanup remains outside translation-only scope.'
 rows.append({**r,'status':'HELD_SOURCE_CHART_AND_BODY_DISPOSITION_REQUIRED','sourceSHA256':hashlib.sha256(r['source'].encode()).hexdigest(),'beforeSHA256':hashlib.sha256(r['before']['value'].encode()).hexdigest(),'sourceTables':src.tables,'beforeTables':old.tables,'positionalNumericOrShapeDifferences':diff,'proseSourceIssue':proseIssue,'blocker':'Current source table differs materially from existing translation. Translation-only assignment preserves measurement facts; parent/source owner must confirm current source chart/options before applying a whole-body candidate.','proposedNextAction':'After source-owner confirmation, translate current source table labels and changed paragraphs together, keeping every confirmed source numeric cell and option code exactly. Do not retain the stale chart under a fresh digest.','changesMade':False})
result={'status':'PRECISE_PER_FIELD_HOLD_NOT_RELEASE_READY','scope':'28 non-Russian/non-Swedish body_html rows; no live or source mutations','rows':rows,'counts':{'fields':len(rows),'products':len(set(r['resourceId'] for r in rows)),'positionalDifferences':sum(len(r['positionalNumericOrShapeDifferences']) for r in rows)},'comparisonLimit':'Arabic spelled dual ages can cause equivalent number differences. Material column/weight differences exist independently and are preserved as raw source/current cell evidence.'}
f=HERE/'changed_source_chart_holds.json';f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['counts']);print(hashlib.sha256(f.read_bytes()).hexdigest())
