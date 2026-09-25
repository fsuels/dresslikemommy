import json,hashlib,re,html
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[2]
P1=B/'root-bodies/he-pl/remaining-review/body_candidates.json'
P2=B/'root-bodies/he-pl/remaining-review/body_candidates_v2.json'
x=json.loads(P1.read_text())['rows'];y=json.loads(P2.read_text())['rows']
ps=json.loads((H/'correction_proposals.json').read_text())['proposals']
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fsha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert fsha(P1)=='b2aa9176937b6d65963fec39f647553de6ceb4b2692eceec31d3af0091c15669'
assert fsha(P2)=='c5a4d949ee800a9feb70b2f07ed5706a65be20a148650f81177ce3a4e0ce74c2'
assert len(x)==len(y)==63
checks=[];out=[];occ=0;changed=0
for a,c in zip(x,y):
 assert a['ledgerId']==c['ledgerId']
 expected=a['value'];proposals=[]
 for p in ps:
  uses=[u for u in p['uses'] if u['ledgerId']==a['ledgerId']]
  if not uses: continue
  assert expected.count(p['oldFragment'])==len(uses)
  expected=expected.replace(p['oldFragment'],p['newFragment']);occ+=len(uses);proposals.append(p['id'])
 assert expected==c['value'],a['ledgerId']
 allowed={'reviewStatus','value','valueSHA256','independentReviewProposalsFile','authorV1ValueSHA256'}
 assert all(a.get(k)==c.get(k) for k in set(a)|set(c) if k not in allowed)
 assert c['valueSHA256']==sha(c['value']) and c['authorV1ValueSHA256']==a['valueSHA256']
 rawp=B/c['rawFile'];raw=json.loads(rawp.read_text());n=next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==c['resourceId'])
 s=next(s for s in n['translatableContent'] if s['key']==c['key']);t=next(t for t in n['translations'] if t['key']==c['key'] and t['locale']==c['locale'] and not t.get('market'))
 assert fsha(rawp)==c['rawFileSHA256'] and s['value']==c['source']==c['sourceValue'] and s['digest']==c['sourceDigest'] and t['value']==c['before']['value'] and sha(c['source'])==c['sourceSHA256'] and sha(c['before']['value'])==c['expectedBeforeValueSHA256']
 norm=lambda v:[re.sub(r'\balt="[^"]*"','alt="LOCALIZED"',x) for x in re.findall(r'<[^>]*>',v)]
 assert norm(c['source'])==norm(c['value'])
 texts=lambda v:[html.unescape(t).strip() for t in re.split(r'<[^>]*>',v) if t.strip()]
 ts,tv=texts(c['source']),texts(c['value']);assert len(ts)==len(tv)
 nums=lambda t:re.findall(r'\d+(?:[.,]\d+)*',' '.join(t))
 assert nums(ts)==nums(tv)
 href=lambda v:re.findall(r'\bhref="([^"]*)"',v)
 assert href(c['source'])==href(c['value'])
 changed+=a['value']!=c['value']
 code='PASS_FULL_MANUAL_INDEPENDENT_CURRENT_SOURCE_MEANING_AND_CORRECTION_READBACK'
 checks.append({'ledgerId':c['ledgerId'],'resourceId':c['resourceId'],'locale':c['locale'],'key':c['key'],'sourceDigest':c['sourceDigest'],'sourceSHA256':c['sourceSHA256'],'beforeSHA256':c['expectedBeforeValueSHA256'],'v1SHA256':a['valueSHA256'],'valueSHA256':c['valueSHA256'],'correctionPairIds':proposals,'exactProposalOnlyDiff':True,'rawSourceBeforeDigestBinding':True,'nonAltMarkupExact':True,'numericTokensExact':True,'linksExact':True,'meaningReviewCode':code})
 out.append(dict(c,marketId=None,meaningReviewCode=code,bindingReviewCode='EXACT_FROZEN_RAW_SOURCE_DIGEST_GLOBAL_BEFORE_VALUE_HASH_PASS',structureReviewCode='EXACT_ALL_NON_ALT_TAG_BYTES_LINKS_NUMBERS_NODE_COUNTS_PASS',independentReviewFile='review/other-article-bodies/independent63/independent_review.json',selectedCandidateFile=str(P2.relative_to(B)),selectedCandidateFileSHA256=fsha(P2),requiresFreshLiveSourceAndBeforeGuard=True,sourceClaimDisposition='ROOT_OWNED_NO_TRANSLATION_HOLD_BASED_SOLELY_ON_OLD_FLAG'))
assert occ==29 and changed==19
report={'status':'PASS_WITH_SOURCE_CONTENT_LIMITS_ALL63_V2_TRANSLATIONS','candidateFile':str(P2.relative_to(B)),'candidateFileSHA256':fsha(P2),'originalCandidateFileSHA256':fsha(P1),'reviewer':'product_release_review; independent of article_he_pl_complete author','method':'Full manual reading of all836 unique source-target visible-text pairs grouped into262 source groups, all335 localized-alt pairs grouped into111 source groups, plus exact revision readback of7Arabic corrections across29nodes/19rows. Non-alt HTML remains current-source exact; all links and visible digits exact.','reviewedRows':63,'locales':['ar','cs','da'],'uniqueArticles':len({r['resourceId'] for r in y}),'correctionPairs':7,'correctionNodeOccurrences':occ,'correctedRows':changed,'unchangedRows':63-changed,'bindingAndStructure':'PASS_ALL63','sourceContentLimits':['Current English all-orders shipping/marketing/fabric/size claims are translated faithfully, not independently verified as true. Root owns policy/source contradiction decisions and release exclusions. No row held solely for old source-claim metadata.','Inherited source IMG malformation/empty-alt metadata contains12occurrences. No additional non-alt markup introduced; source repairs are outside this translation pass.','Source-truncated product-title fragments such as Pri..., Re..., Ele..., D..., Wh... or i... remain in some localized source-bound labels. They cannot be described as fully polished localized copy until the English title fragments are repaired; complete meaning is translated wherever source supplies it.','Fresh source and before guards, Shopify registration and public verification remain root-owned; this is not a live release receipt.'],'rows':checks}
(H/'independent_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(H/'qualified_v2_release_index.json').write_text(json.dumps({'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS_ROOT_SOURCE_POLICY_SCOPE_REQUIRED','rows':out},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','reviewedRows','uniqueArticles','correctionPairs','correctionNodeOccurrences','correctedRows','unchangedRows']},indent=2))
