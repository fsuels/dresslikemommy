#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
base=json.loads((HERE/'body_baseline.json').read_text())['rows'];rows=[];checks=[]
for r in base:
 if not r['resourceId'].endswith('/7228773466209') or r['locale'] not in {'fi','he'}:continue
 before=r['before']['value'];first=re.search(r'<p>(.*?)</p>',before,re.S);heading=re.search(r'<p><strong>(.*?)</strong></p>',before,re.S)
 label,translated=heading[1].split('\n',1)
 assert first[1]==re.search(r'<p>(.*?)</p>',r['source'],re.S)[1]
 # The actual translated paragraph was accidentally concatenated into the bold heading.
 after=before[:first.start(1)]+translated+before[first.end(1):]
 after=after.replace(heading[1],label,1)
 if r['locale']=='he':
  after=after.replace('פרטי הכפתור','פרטי החפתים').replace('פרטי כפתור בקצה','פרטי חפתים')
  after=after.replace('סוודרים תואמים וסטייליסטיים','סוודרים תואמים ואופנתיים')
 else:
  after=after.replace('kalvosin yksityiskohdat','kalvosinyksityiskohdat').replace('kalvosin yksityiskohdilla','kalvosinyksityiskohdilla')
 assert ot.Shape(before).events==ot.Shape(after).events
 assert ot.table_facts(ot.Shape(before),r['locale'])==ot.table_facts(ot.Shape(after),r['locale'])
 rows.append({**r,'value':after,'marketId':None,'method':'move_existing_localized_paragraph_from_bold_heading_to_replace_English_intro','reviewNotes':'Retains existing translated prose, list items, table cells and translated alt attributes. Hebrew mistranslation cuff→button corrected; Finnish compound spelling corrected. No new product claims.'})
 checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'sourceCheck':ot.verify_text(r['source'],after,r['locale']),'beforeAfterTagsAndAttributesUnchanged':True,'beforeAfterTableCellsAndUnitsUnchanged':True,'sourceAttributeCheckLimit':'Existing localized image alt attributes intentionally retained.'})
f=HERE/'sweater_intro_fi_he_candidate.json';f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(HERE/'sweater_intro_fi_he_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(HERE/'sweater_intro_fi_he_rollback.json').write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
