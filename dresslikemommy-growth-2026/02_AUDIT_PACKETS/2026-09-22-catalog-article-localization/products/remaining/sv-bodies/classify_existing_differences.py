"""Bounded existing HTML variance review. Never rewrites markup or measurements."""
import json, pathlib, sys, re, hashlib
B=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(B.parents[2]/'tooling'))
from offline_translation import verify_text, Shape, table_facts
selected={r['resourceId']:r for r in json.loads((B/'selected_baseline.json').read_text())['rows']}
strict=json.loads((B/'completed_candidates.json').read_text())['rows']
held=json.loads((B/'held_completed_candidates.json').read_text())['rows']
accepted=[];remaining=[];reviews=[]
stripcomments=lambda s:re.sub(r'<!--.*?-->','',s,flags=re.S)
tablere=re.compile(r'<table\b.*?</table>',re.S|re.I)
for r in held:
 base=selected[r['resourceId']]['baseValue']; a=Shape(r['source']); c=Shape(r['value']); old=Shape(base)
 assert old.events==c.events, 'Translation introduced HTML mutation'
 assert table_facts(a,'en')==table_facts(c,'sv'), 'Table facts differed'
 decision={'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'strictErrors':r['verification']['errors'],'baselineHtmlEventsPreserved':True,'sourceTableCellFactsMatch':True}
 nc=verify_text(stripcomments(r['source']),stripcomments(r['value']),'sv')
 if not nc['errors']:
  decision.update(status='QUALIFIED_COMMENT_ONLY_VARIANCE',reason='Only existing translated/added HTML comments differ from English. Non-comment HTML, attributes, URLs, all table facts and numerical values match source. Baseline comments retained exactly.',normalizedSourceCheck=nc)
  accepted.append(r)
 elif r['resourceId']=='gid://shopify/Product/7241105670241':
  ats=tablere.findall(r['source']);bts=tablere.findall(r['value']);assert len(ats)==len(bts)==1
  tablecheck=verify_text(stripcomments(ats[0]),stripcomments(bts[0]),'sv')
  restcheck=verify_text(stripcomments(tablere.sub('',r['source'])),stripcomments(tablere.sub('',r['value'])),'sv')
  assert not tablecheck['errors'] and not restcheck['errors']
  decision.update(status='QUALIFIED_EXISTING_TABLE_POSITION_VARIANCE',reason='Exactly one identical-fact size table is positioned later in existing Swedish HTML. Table checked independently: tags, attributes, cells, numeric values and units match source apart from retained existing translated comments. Remaining HTML and links match source. Baseline position retained; no data removed or duplicated.',tableCheck=tablecheck,remainingBodyCheck=restcheck)
  accepted.append(r)
 else:
  assert r['resourceId'] in ['gid://shopify/Product/7227375714401','gid://shopify/Product/7227378925665']
  decision.update(status='HOLD_LEGACY_IMAGE_DIFFERENCE',reason='Existing Swedish body retains supplier image tags where fresh English has br tags. Full prose translated but exact source image/link reconciliation requires owner review. Existing attributes preserved; proposed root decision is whether to replace only the listed obsolete image tags with br, matching current English.',source=r['source'],before=r['before'],value=r['value'])
  remaining.append(r)
 r['existingVarianceReview']=decision
 reviews.append(decision)
for fn,d in [('qualified_candidates.json',{'rows':strict+accepted}),('legacy_image_hold_candidates.json',{'rows':remaining}),('existing_variance_review.json',{'rows':reviews})]:
 (B/fn).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'strict':len(strict),'qualifiedExistingVariance':len(accepted),'qualifiedTotal':len(strict+accepted),'legacyImageHolds':len(remaining)}))
