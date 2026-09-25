import json,re,hashlib,collections
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
v1=json.loads((H/'tag_candidates_v1.json').read_text());rows=v1['rows'];proof=[]
for r in rows:
 j,loc=r['productIndex'],r['locale'];before=r['value'];value=before;changes=[]
 if loc=='it' and j in [41,51,65,84]:
  imagePs=[p for p in re.findall(r'<p\b[^>]*>.*?</p>',r['source'],re.S) if '<img' in p];assert len(imagePs)==1
  old='<p><immagine';assert before.count(old)==1
  new=imagePs[0];value=value.replace(old,new,1)
  changes.append({'kind':'RESTORE_TRUNCATED_IMAGE_PARAGRAPH_FROM_UNIQUE_ENGLISH_SOURCE_LOCATION','before':old,'after':new,'sourceExactImageParagraph':new,'sourceImageParagraphCount':1,'imageURLsRestored':re.findall(r'src="([^"]*)"',new),'attributeValueException':'All missing image attrs copied exactly from unique current English source image paragraph; no guessed URL or alt. English source alt fallback is retained explicitly.','pairingEvidence':'One incomplete image paragraph in target, exactly one image paragraph in current source at matching after-table/before-empty-paragraph location. No complete target images were replaced.'})
 elif j==51 and loc in ['ar','nl']:
  imageTags=re.findall(r'<img\b[^>]*>',r['source']);assert len(imageTags)==3
  srcurls=[re.search(r'src="([^"]*)"',t)[1] for t in imageTags]
  targeturls=re.findall(r'<img\b[^>]*src="(https[^"]*)"[^>]*>',before);assert targeturls==srcurls[:2]
  broken=re.search(r'src="(_+DLMTOK2_+)\s*\n',before);assert broken
  old=broken[0].rstrip('\n');new='src="'+srcurls[2]+'"></p>'
  assert value.count(old)==1;value=value.replace(old,new,1)
  changes.append({'kind':'RESTORE_SOURCE_PAIRED_THIRD_IMAGE_SRC_AND_MISSING_CLOSE','before':old,'after':new,'sourceExactThirdImageTag':imageTags[2],'imageURLsRestored':[srcurls[2]],'pairingEvidence':'First two complete target image URLs exactly equal first two current source images; third target image alt describes same remaining image and ends in DLMTOK2 placeholder. Unique third current source image URL restored. Existing localized alt preserved.','attributeValueException':'Replace invalid placeholder src only with exact third source URL; preserve existing localized alt.'})
 elif j==97 and loc=='ja':
  pairs=[('<strong>トレンディなストリートウェアの外観:</li>','<strong>トレンディなストリートウェアの外観:</strong>','<strong>Trendy Streetwear Look:</strong>'),('<strong>トレンドのデザイン:</li>','<strong>トレンドのデザイン:</strong>','<strong>On-Trend Design:</strong>')]
  for old,new,src in pairs:
   assert value.count(old)==1 and r['source'].count(src)==1;value=value.replace(old,new,1);changes.append({'kind':'SOURCE_ALIGNED_STRONG_CLOSE_IN_LIST_ITEM','before':old,'after':new,'sourceExactHeadingTag':src,'pairingEvidence':'Matching translated heading in same ordered source list item; existing strong opener was wrongly closed as li, leaving following text outside its item.'})
 if not changes:continue
 assert value!=before
 assert re.findall(r'<t[dh](?:\s[^>]*)?>.*?</t[dh]>',before,re.S)==re.findall(r'<t[dh](?:\s[^>]*)?>.*?</t[dh]>',value,re.S)
 for change in changes:
  assert change['before'] in before
  if change['kind'].startswith('RESTORE'):
   for url in change['imageURLsRestored']:assert url in r['source'] and url in value
 if loc=='ja':assert re.sub('<[^>]*>','',before)==re.sub('<[^>]*>','',value)
 r.update(value=value,valueSHA256=sha(value),residualMarkupExceptions=changes,versionOneValueSHA256=sha(before))
 r['checks']['residualSevenTableCellAndHeaderBytesExact']=True;r['checks']['residualSevenAllUnchangedSegmentsExact']=True
 r['checks']['imageURLAndAttributeValueExceptionsExplicit']=bool(loc!='ja')
 r['checks']['residualBalancednessStatus']='RECALCULATED_IN_V2_FINAL_CHECKS'
 proof.append({'productIndex':j,'resourceId':r['resourceId'],'locale':loc,'sourceDigest':r['sourceDigest'],'beforeValueSHA256':r['beforeValueSHA256'],'v1ValueSHA256':sha(before),'v2ValueSHA256':sha(value),'changes':changes})
assert len(proof)==7
(H/'tag_candidates_v2.json').write_text(json.dumps({'status':'CURRENT_FALSE_MINIMAL_MARKUP_PLUS_EXPLICIT_SOURCE_IMAGE_RESTORATION_AND_JA_P5_TIE_PENDING_INDEPENDENT_REVIEW','supersedes':'tag_candidates_v1.json','rows':rows},ensure_ascii=False,indent=2)+'\n')
(H/'residual_seven_evidence.json').write_text(json.dumps({'status':'SOURCE_PAIRED_AUTHOR_CHECKS_PASS','rows':proof},ensure_ascii=False,indent=2)+'\n')
print({'rows':len(rows),'changedFromV1':len(proof),'newlyRestoredImageURLs':sum(len(c.get('imageURLsRestored',[])) for p in proof for c in p['changes']),'v2SHA256':sha((H/'tag_candidates_v2.json').read_text())})
