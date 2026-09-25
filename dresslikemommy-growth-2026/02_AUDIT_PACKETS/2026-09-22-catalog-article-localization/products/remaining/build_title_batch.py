#!/usr/bin/env python3
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
PRODUCTS=HERE.parent
sys.path.insert(0,str(PRODUCTS.parent/'tooling'))
import offline_translation as ot
filename=sys.argv[1]
values=json.loads((HERE/filename).read_text())
sources=json.loads((HERE/'ru_sv_title_sources.json').read_text())
baseline=json.loads((HERE/'baseline.json').read_text())['rows']
nodes={}
for f in PRODUCTS.glob('translations_batch_*.json'):
    for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']:nodes[n['resourceId']]=n
candidate=[];held=[];nochange=[]
for r in baseline:
    if r['key']!='title' or r['locale'] not in values:continue
    idx=str(sources.index(r['source']))
    if idx not in values[r['locale']]:continue
    if idx=='2':
        held.append({**r,'holdReason':'SOURCE_CONTRADICTION: title says hollow-out bikini; same product body says one-piece; SEO title says Halloween Print. Root must establish correct source garment/print.'})
        continue
    if idx=='130':
        held.append({**r,'holdReason':'SOURCE_MATERIAL_CONFLICT: title says Cotton-Silk, while the same body specifies viscose shell / polyester lining. Root must establish actual fibers before translating a cotton/silk composition claim.'})
        continue
    if idx=='135' and r['before']:
        nochange.append({**r,'disposition':'SEMANTICALLY_CORRECT_NO_COPY_CHANGE','reason':'Existing title identifies top or pants, precisely matching the same-product separate-item purchase instruction. Golden Daisy is a retained design name; stale digest alone is not a visible language defect.'})
        continue
    n=nodes[r['resourceId']]
    candidate.append({**r,'value':values[r['locale']][idx],'sourceIndex':int(idx),'method':'manual_translation','supportingSourceDigests':{s['key']:s['digest'] for s in n['translatableContent'] if s['key'] in ('body_html','product_type')},'marketId':None})
stem=filename.replace('title_values_','titles_').replace('.json','')
plan={'status':'PENDING_INDEPENDENT_PARENT_REVIEW','scope':'Russian/Swedish title translations only. Source truncation remains expressed by ellipsis; undecodable clipped words omitted, specific resolved garment details supported by same-product body/type digests. Printed slogans retained. No source edits or prior frozen cohort overlap.','rows':candidate}
target=HERE/(stem+'_candidate.json');target.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
report=ot.verify_rows(candidate,baseline);(HERE/(stem+'_structure.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
inverse=[{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'marketId':None,'action':'restore' if r['before'] else 'remove','value':r['before']['value'] if r['before'] else None} for r in candidate]
(HERE/(stem+'_rollback.json')).write_text(json.dumps(inverse,ensure_ascii=False,indent=2)+'\n')
(HERE/(stem+'_held.json')).write_text(json.dumps({'rows':held},ensure_ascii=False,indent=2)+'\n')
(HERE/(stem+'_no_change.json')).write_text(json.dumps({'rows':nochange},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':target.name,'rows':len(candidate),'held':len(held),'structuralFailures':report['failedRows'],'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
