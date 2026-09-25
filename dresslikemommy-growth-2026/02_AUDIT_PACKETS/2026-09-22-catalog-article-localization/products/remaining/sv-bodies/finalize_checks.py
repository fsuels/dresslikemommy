"""Validate only frozen local proposals. No API/provider or publication path."""
import json,pathlib,hashlib,sys,re,collections
B=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(B.parents[2]/'tooling'))
from offline_translation import Shape,verify_text,table_facts
from prepare_segments import parts,norm
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
load=lambda n:json.loads((B/n).read_text())
q=load('qualified_candidates.json')['rows'];h=load('legacy_image_hold_candidates.json')['rows'];bl=load('blocked_fields.json')['rows'];base=load('selected_baseline.json')['rows'];index={r['resourceId']:r for r in base}
assert len(q)==99 and len(h)==2 and len(bl)==23 and len(base)==124
assert len({r['resourceId'] for r in q+h+bl})==124
assert not load('pending.json')['rows']
bindings=[]
for r in q+h+bl:
 p=B.parents[1]/r['rawFile'];data=json.loads(p.read_text());node=next(n for n in data['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId']);source=next(x for x in node['translatableContent'] if x['key']==r['key']);before=next((x for x in node['tr_sv'] if x['key']==r['key'] and x['locale']=='sv' and x.get('market') is None),None)
 assert r['source']==source['value'] and r['sourceDigest']==source['digest']
 assert r['before']==before
 bindings.append({'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['source']),'rawFile':r['rawFile'],'rawSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'PASS'})
checks=[]
for r in q+h:
 old=index[r['resourceId']]['baseValue'];a=Shape(old);b=Shape(r['value'])
 assert a.events==b.events
 assert a.raw==b.raw
 assert table_facts(Shape(r['source']),'en')==table_facts(b,'sv')
 assert sha(r['value'])==r['valueSHA256']
 assert r['sourceSHA256']==sha(r['source'])
 # All numeral characters retained by exact node transformation, decimal aliases handled by source verifier.
 assert not any(x in verify_text(r['source'],r['value'],'sv')['errors'] for x in ['numeric_values_changed','table_cell_numbers_units_or_shape_changed','measurement_units_changed_or_unrecognized','script_or_style_content_changed'])
 checks.append({'resourceId':r['resourceId'],'sourceAndBeforeBound':True,'baselineHtmlAttributesCommentsPreserved':True,'sourceNumbersUnitsTableFactsMatch':True,'candidateSHA256':sha(r['value'])})
files=['batch_01_v3.json','batch_02.json','batch_03.json','batch_04.json','batch_05.json','batch_06.json','batch_07.json','batch_08.json']
frozen=[r for n in files for r in load(n)['rows']];assert len(frozen)==len(q)==99
qi={r['resourceId']:r for r in q};assert len({r['resourceId'] for r in frozen})==99
for r in frozen:assert r['value']==qi[r['resourceId']]['value']
inv=[r for r in load('inverse.json')['rows'] if r['resourceId'] in qi];assert len(inv)==99
(B/'qualified_inverse.json').write_text(json.dumps({'rows':inv},ensure_ascii=False,indent=2)+'\n')
(B/'final_validation.json').write_text(json.dumps({'status':'PASS_WITH_DOCUMENTED_EXISTING_VARIANCES','scope':'Frozen local exports; live freshness and release not performed','selected':124,'qualifiedCandidates':99,'legacyImageHolds':2,'sourceMeasurementHolds':23,'pending':0,'bindings':bindings,'checks':checks,'frozenBatches':files,'limitations':['77 strict structural passes; 21 preexisting HTML-comment differences and 1 preexisting table-position difference independently checked and preserved.','45 existing image/accessibility attribute texts preserved per scope; some remain English and need separate attribute-localization scope.','Ordinary source product claims translated faithfully, not independently validated against supplier evidence.','Full independent meaning review is ongoing; root alone applies after fresh live digest and before-value guards.']},ensure_ascii=False,indent=2)+'\n')
print('PASS: 124 exact local source/digest/before bindings; 101 authored values preserve HTML/attributes/comments and source numeric/table/unit facts; 99 frozen qualified proposals + 25 precise holds; 0 pending.')
