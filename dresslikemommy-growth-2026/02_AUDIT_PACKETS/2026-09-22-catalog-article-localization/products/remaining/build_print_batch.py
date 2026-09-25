#!/usr/bin/env python3
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
PRODUCTS=HERE.parent
sys.path.insert(0,str(PRODUCTS.parent/'tooling'))
import offline_translation as ot
base=json.loads((HERE/'baseline.json').read_text())['rows']
sources=json.loads((HERE/'print_sources.json').read_text())
values={}
for name in ['print_values_latin.json','print_values_nonlatin.json']:
    d=json.loads((HERE/name).read_text());indices=d.pop('sourceIndices')
    for locale,texts in d.items():
        assert len(texts)==len(indices)
        for i,value in zip(indices,texts):values[(locale,sources[i])]=value
for locale,texts in json.loads((HERE/'print_values_extra.json').read_text()).items():
    for i,value in texts.items():values[(locale,sources[int(i)])]=value
rows=[]
for r in base:
    if r['key']!='name' or (r['locale'],r['source']) not in values:continue
    rows.append({**r,'value':values[(r['locale'],r['source'])],'marketId':None,'method':'manual_print_design_and_color_translation'})
f=HERE/'print_names_candidate.json';f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','scope':'Repeated descriptive print/color names and Tank Top label. Cream explicitly means cream color, not cosmetics. Peter Rabbit retained as the named design/character. No source identifiers or product configuration changed.','rows':rows},ensure_ascii=False,indent=2)+'\n')
rep=ot.verify_rows(rows,base);(HERE/'print_names_structure.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
(HERE/'print_names_rollback.json').write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'action':'restore' if r['before'] else 'remove','value':r['before']['value'] if r['before'] else None,'marketId':None} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'uniqueSourceLocale':len(set((r['locale'],r['source']) for r in rows)),'structuralFailures':rep['failedRows'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
