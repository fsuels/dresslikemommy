#!/usr/bin/env python3
"""Build exact-source-bound, offline manual metadata cohorts. No API calls."""
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
BASE=json.loads((HERE/'baseline.json').read_text())['rows']
def save(name,rows,scope):
    f=HERE/(name+'_candidate.json')
    f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','scope':scope,'rows':rows},ensure_ascii=False,indent=2)+'\n')
    rep=ot.verify_rows(rows,BASE)
    (HERE/(name+'_structure.json')).write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
    (HERE/(name+'_rollback.json')).write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'action':'restore' if r['before'] else 'remove','value':r['before']['value'] if r['before'] else None,'marketId':None} for r in rows],ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'file':f.name,'rows':len(rows),'structuralFailures':rep['failedRows'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
def indexed(name,key,sourcefile,valuefile,suffix=''):
    sources=json.loads((HERE/sourcefile).read_text());values=json.loads((HERE/valuefile).read_text());idx=values.pop('sourceIndices')
    lookup={(loc,sources[i]):v+suffix for loc,vs in values.items() for i,v in zip(idx,vs)}
    assert all(len(v)==len(idx) for v in values.values())
    rows=[{**r,'value':lookup[(r['locale'],r['source'])],'marketId':None,'method':'manual_exact_source_metadata_translation'} for r in BASE if r['key']==key and (r['locale'],r['source']) in lookup]
    save(name,rows,'Exact English source meaning; named designs and Dress Like Mommy retained literally; no source claims added. Existing source-conflict metadata excluded.')
if __name__=='__main__':
    if sys.argv[1]=='custom_titles': indexed('custom_meta_titles','meta_title','meta_title_sources.json','custom_meta_title_values.json',' | Dress Like Mommy')
    if sys.argv[1]=='descriptions': indexed('qualified_meta_descriptions','meta_description','unheld_meta_description_sources.json','meta_description_values.json')
