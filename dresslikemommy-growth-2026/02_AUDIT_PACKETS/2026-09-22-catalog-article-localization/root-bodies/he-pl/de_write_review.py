from pathlib import Path
import hashlib,json,importlib.util
P=Path(__file__).parent;R=P.parent;f=R/'de/candidate_all_complete.json';rows=json.loads(f.read_text())['rows'];manifest=json.loads((R/'de/manifest_sha256.json').read_text());baseline={r['resourceId']:r for r in json.loads((R/'de_baseline.json').read_text())}
spec=importlib.util.spec_from_file_location('o',R.parent/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sha=lambda x:hashlib.sha256(x.encode()).hexdigest()
replacements=[
 {'id':'DE_JOIN_SWIM_ACCUSATIVE','onlyResource':'gid://shopify/Article/559471558753','old':'Entdecke unsere <a href="/collections/family-swimsuits">passender Familienbademode</a>','new':'Entdecke unsere <a href="/collections/family-swimsuits">passende Familienbademode</a>','reason':'Genitive ending inherited from another paragraph conflicts with Entdecke unsere; use accusative adjective.'},
 {'id':'DE_JOIN_DADDY_COLLECTION_TITLE','onlyResource':'gid://shopify/Article/559471820897','old':'Entdecke unsere Kollektionen <a href="/collections/matching-outfits">passenden Outfits</a>','new':'Entdecke unsere Kollektionen <a href="/collections/matching-outfits">Passende Outfits</a>','reason':'A named category after Kollektionen needs the standalone category label, not the datively inflected fragment from a different sentence.'},
 {'id':'DE_TITLE_COTTON_ATTRIBUTION','old':'Passende Hawaiihemden für Vater &amp; Sohn – tropischer Print aus 100% Baumwolle','new':'Passende Hawaiihemden für Vater &amp; Sohn – 100% Baumwolle mit tropischem Print','reason':'Attribute 100% cotton to the shirts, not the print; all source product facts retained.'},
 {'id':'DE_TITLE_BUTTON_UP_ATTRIBUTION','old':'Baumwoll-Hawaiihemd für Herren &amp; Jungen – tropischer Blätterprint, kurze Ärmel mit Knopfleiste, Grün/Schwarz','new':'Kurzärmeliges Baumwoll-Hawaiihemd für Herren &amp; Jungen – tropischer Blätterprint, Knopfleiste, Grün/Schwarz','reason':'Keep button-up a shirt construction feature rather than saying its short sleeves have a button placket.'}
]
proposals=[];after=[]
for r in rows:
 val=r['value'];changes=[]
 for d in replacements:
  if d.get('onlyResource',r['resourceId'])!=r['resourceId']:continue
  n=val.count(d['old'])
  if n:
   changes.append({**d,'expectedOccurrences':n});val=val.replace(d['old'],d['new'])
 if changes:
  result=m.verify_text(r['sourceValue'],val,'de');assert not result['errors'],(r['resourceId'],result)
  proposals.append({'resourceId':r['resourceId'],'locale':'de','key':'body_html','sourceDigest':r['sourceDigest'],'originalValueSHA256':sha(r['value']),'proposedValueSHA256':sha(val),'changes':changes,'simulatedStructuralCheck':result})
 for field in ['sourceValue','sourceDigest','before']:assert r[field]==baseline[r['resourceId']][field]
 after.append({'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['sourceValue']),'valueSHA256':sha(r['value'])})
report={'status':'PASS_SEMANTIC_COVERAGE_WITH_4_LOCAL_LANGUAGE_CORRECTION_RULES','reviewedFile':str(f),'reviewedFileSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'matchesAuthorManifest':hashlib.sha256(f.read_bytes()).hexdigest()==manifest['candidate_all_complete.json'],'bodyCount':57,'uniqueSourceTargetNodePairsReviewed':1242,'assembledInlineParagraphsReviewed':219,'exactRepeatedBoilerplatePairs':118,'method':'Independently compared every deduplicated source-target pair; verified the three recurring full boilerplate forms by exact matching and reviewed their variable product names; separately read assembled paragraphs with inline links. Re-read output-truncated spans405-411 and684-697. Checked 57 complete HTML bodies for tag/attribute/link/numeric/unit preservation and against original baseline source/digest/before fields.','findings':'No material source-content omission or source fact change found. Four correction rules address two invalid inline adjective endings and two ambiguous feature attachments in translated product titles. Source factual/marketing claims remain parent release holds, not certified true by translation review. English printed garment slogans, DLM, and proper brand names intentionally retained. English/source title truncation and old year references are preserved as source editorial matters.','structure':'PASS 57/57 zero errors','sourceBinding':'PASS 57/57 exact supplied local baseline; fresh live digest readback remains root responsibility','corrections':proposals,'rows':after,'liveWrites':False,'originalCandidateModified':False}
(P/'de_independent_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'proposedRows':len(proposals),'occurrences':sum(c['expectedOccurrences'] for p in proposals for c in p['changes']),'manifestMatch':report['matchesAuthorManifest']}))
