from pathlib import Path
import json,hashlib,importlib.util
P=Path(__file__).parent;PACK=P.parents[2]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
rows=json.loads((P/'short_worklist.json').read_text())['rows'];manual=json.loads((P/'manual_short.json').read_text());assert set(manual)=={r['ledgerId']for r in rows}
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[]
for r in rows:
 r['value']=manual[r['ledgerId']];r['sourceSHA256']=sha(r['sourceValue']);r['valueSHA256']=sha(r['value']);r['expectedBeforeValueSHA256']=sha(r['before']['value'])if r['before']else None;r['reason']='Offline manual correction of confirmed missing, partly English, token-corrupted or stale article short field; exact current English meaning retained.'
 if r['ledgerId']=='730':r['reason']='Outdated flag is meaning-equivalent, but existing Danish title has broken compound/word order; repair to a natural equivalent title.'
 check=m.verify_text(r['sourceValue'],r['value'],r['locale']);assert not check['errors'],(r['ledgerId'],check)
 checks.append({'ledgerId':r['ledgerId'],'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'check':check,'beforeObjectPreserved':True})
for name,obj in [('short_candidates.json',{'status':'MANUALLY_AUTHORED_PENDING_INDEPENDENT_REVIEW','rows':rows}),('short_checks.json',{'status':'PASS','rows':checks})]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print({'rows':len(rows),'checks':'PASS'})
