#!/usr/bin/env python3
"""Offline evidence classification; no external/provider/browser calls."""
from pathlib import Path
import collections,hashlib,json,re,sys
P=Path(__file__).resolve().parent.parent;H=P/'review';ROOT=P.parents[2]
sys.path.insert(0,str(P/'tooling'));import offline_translation as ot

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vsha(t):return hashlib.sha256(t.encode()).hexdigest()
def write(n,d):(H/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
paths={'ru':P/'articles/ru-bodies/candidate_all_complete.json','sv':P/'tooling/sv-bodies/candidate.json'}
by={lc:{r['resourceId']:r for r in read(p)['rows']} for lc,p in paths.items()}
more={
'559471886433':'The flag matched size up inside a negated safety instruction. Full RU/SV article preserves every checklist item, separate selection and sizing/measurement caveat, delivery uncertainty, current-return reference, unclear-unit warning, intended-fit/sleepwear safety caveat, and explicit do-not-size-up instruction.',
'559471231073':'Full RU/SV article preserves source palette, product/collection directions, comparative fit guidance, garment details and printed card-suit product reference. Sell-best/convert language is existing editorial marketing wording, not a new statistic or a translation error. Parent may retain source within translation-only scope.',
'559662530657':'Full RU/SV article preserves winter styling, half-zip silhouette, colors, adult conditional size-up for chosen fit, childrens room for layers, cold wash and flat-drying. Flagged advice is conditional adult styling, not universal childrens sleepwear sizing.',
'559700803681':'Full RU/SV article preserves summer palette, garment categories, torso/strap-fit guidance, woven-set airflow, conditional between-size advice for heat, swimwear rinsing and avoidance of high heat. No numerical size conversion, compliance or sun-protection promise added.'}
supp=[];reports=[]
for suffix,note in more.items():
 rid='gid://shopify/Article/'+suffix
 for lc in ['ru','sv']:
  r=by[lc][rid];rf=Path(r['rawFile']);rf=rf if rf.is_absolute() else (ROOT/rf if str(rf).startswith('dresslikemommy-growth-2026/') else P/'articles'/rf)
  raw=read(rf);n=next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==rid);s=next(s for s in n['translatableContent'] if s['key']=='body_html' and s['locale']=='en')
  assert s['value']==r['sourceValue'] and s['digest']==r['sourceDigest']
  assert r['before'] is None and not [t for t in n['translations'] if t['key']=='body_html' and t['locale']==lc and t.get('market') is None]
  checks=ot.verify_text(s['value'],r['value'],lc);assert not checks['errors'],(rid,lc,checks)
  assert ot.Shape(s['value']).events==ot.Shape(r['value']).events
  row={'resourceId':rid,'locale':lc,'key':'body_html','marketId':None,'source':s['value'],'sourceDigest':s['digest'],'sourceSHA256':vsha(s['value']),'before':None,'expectedBeforeValueSHA256':None,'value':r['value'],'valueSHA256':vsha(r['value']),'rawFile':str(rf.relative_to(P)),'rawFileSHA256':sha(rf),'candidateFile':str(paths[lc].relative_to(P)),'candidateFileSHA256':sha(paths[lc]),'bindingReviewCode':'EXACT_EN_SOURCE_OPAQUE_DIGEST_EXPLICIT_LOCALE_GLOBAL_MISSING_PASS','meaningReviewCode':'INDEPENDENT_FULL_SOURCE_TARGET_PROSE_PASS','structureReviewCode':'EXACT_HTML_ATTRIBUTES_URLS_NUMBERS_TABLES_PASS','sourceFlagDisposition':'FALSE_POSITIVE_NEGATION' if suffix=='559471886433' else 'SOURCE_PRESERVING_STYLE_ADVICE_NOT_A_TRANSLATION_BLOCKER','requiresFreshLiveSourceAndBeforeGuard':True}
  supp.append(row);reports.append({'resourceId':rid,'locale':lc,'sourceDigest':s['digest'],'valueSHA256':vsha(r['value']),'verdict':'PASS_WITH_LIMITS','note':note})
write('article_additional_eight_review.json',{'status':'PASS_WITH_LIMITS','fields':8,'reports':reports,'limits':['Full source-target prose review, raw source/digest/global-missing-before and exact structure/number/link checks passed.','Source translation fidelity does not prove empirical supplier claims or live route behavior.','No English source change or additional user permission required for these accurate translations.']})
write('qualified_article_body_supplement.json',{'status':'EIGHT_SOURCE_BOUND_ROWS_WITH_FALSE_POSITIVE_OR_STYLE_FLAGS_DISPOSED','rows':supp})
initial=read(H/'qualified_article_body_release_index.json')['rows'];editorial=read(H/'article_editorial_trigger_rows.json')['rows']
for r in editorial:r['sourceFlagDisposition']='SOURCE_PRESERVING_EDITORIAL_COPY_NOT_A_TRANSLATION_BLOCKER'
allrows=initial+editorial+supp
assert len(allrows)==24 and len({(r['resourceId'],r['locale'],r['key']) for r in allrows})==24
write('article_release_index_final.json',{'status':'24_INDEPENDENTLY_MEANING_STRUCTURE_AND_RAW_BOUND_SOURCE_PRESERVING_ROWS','rows':allrows,'supersedesForSelection':['qualified_article_body_release_index.json','article_editorial_trigger_rows.json','qualified_article_body_supplement.json'],'limits':['Parent can release these accurate translations within the current user translation-repair request; no additional permission gate is created by ordinary source marketing wording.','Fresh exact source digest/current-before guard and public verification remain required. Source changes invalidate these bindings.','Recommendation URL redirects/availability remain separate parent checks; absence from direct published handles is not proof a URL is broken.','Other 110 author-draft rows are not independently meaning-qualified by this reviewer.']})

first=read(P/'articles/source_claims_release_review.json');second=read(P/'tooling/sv-bodies/source_claim_holds.json');claims=collections.defaultdict(dict)
for a in first['articles']:
 for c in a['claims']:claims[a['resourceId']].setdefault(c['sourceText'],set()).update(c['flags'])
for c in second['rows']:
 for rid in c['resourceIds']:claims[rid].setdefault(c['sourceText'],set()).update(c['reasons'])
# Read exact policy evidence, without representing an old snapshot as a fresh account read.
policy_file=P.parent/'2026-09-22-multilingual-storefront/content_before_apply.json'
policy=None
for page in read(policy_file):
 for n in page['nodes']:
  if n['resourceId']=='gid://shopify/ShopPolicy/29845782625':
   s=next(s for s in n['translatableContent'] if s['key']=='body' and s['locale']=='en');policy={'resourceId':n['resourceId'],'sourceDigest':s['digest'],'sourceSHA256':vsha(s['value']),'evidenceFile':str(policy_file.relative_to(ROOT)),'evidenceSHA256':sha(policy_file),'exactQualification':'Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.'};break
 if policy:break
assert policy
rows=[]
for rid,clauses in sorted(claims.items()):
 checks=[]
 for text,flags in clauses.items():
  if text.startswith("Do not automatically size up children's sleepwear"):
   category='FALSE_POSITIVE_NEGATED_SAFETY_GUIDANCE';finding='The actual sentence forbids automatic size-up and asks for intended-fit/label confirmation. No source correction indicated.'
  elif re.search(r'free shipping on all orders|Every order ships free',text,re.I):
   category='DEMONSTRATED_SCOPE_MISMATCH_WITH_RECORDED_POLICY';finding='Unqualified all-orders free shipping omits the recorded standard-method availability limitation and possible express upgrade. Policy evidence is Sep22 snapshot; refresh exact current terms before a source repair.'
  elif rid.endswith(('559471231073','559662530657','559700803681')):
   category='ORDINARY_EDITORIAL_OR_CONDITIONAL_STYLE_ADVICE';finding='No demonstrated factual contradiction. Accurate source-preserving translation is eligible and has independent full meaning review.'
  elif rid.endswith('559662366817'):
   category='CONDITIONAL_STYLE_ADVICE_PLUS_SEPARATE_OWNER_RESERVATION';finding='Flagged sentence itself is conditional fit/layering advice. Prior source-editor reservation, not a language detector, is the coordination dependency.'
  elif re.search(r'UPF|sun protection',text,re.I):
   category='SPECIFIC_SUN_PROTECTION_ASSERTION_UNSUBSTANTIATED_IN_PACKET';finding='Exact protection assertion needs product/test substantiation or source-owner disposition. Flag is not proof of falsity; no translation-induced assertion identified.'
  elif re.search(r'size up|go bigger|buy one size bigger|All (?:of our matching sets|sets) come',text,re.I):
   category='BROAD_FIT_OR_SIZE_AVAILABILITY_ASSERTION_REVIEW';finding='Unlike negated or conditional advice, this broad source guidance needs intended-use/product-chart context. No source fact changed by this review.'
  elif re.search(r'tested dozens|testing dozens|Studies show',text,re.I):
   category='EMPIRICAL_TESTING_OR_RESEARCH_ASSERTION_UNSUBSTANTIATED_IN_PACKET';finding='The packet contains no identified test study or supporting record. Do not claim it is proven false; root can assess support/retain or authorize a source correction separately.'
  elif re.search(r'\$|\d+.?\d*%|two pieces|all-in-one|first-purchase discounts|full size range|Limited sizes|over 80|new styles added weekly|new styles drop',text,re.I):
   category='SPECIFIC_PRICE_QUANTITY_INCLUSION_OR_AVAILABILITY_ASSERTION_REVIEW';finding='Needs current product/collection/bundle/promotion evidence to establish truth. Translation fidelity alone neither substantiates nor disproves it.'
  elif re.search(r'2.3x|countless|dozens of cycles|all body types|maintain their shape|great through',text,re.I):
   category='PERFORMANCE_OR_UNIVERSAL_FIT_ASSERTION_UNSUBSTANTIATED_IN_PACKET';finding='Specific or sweeping performance assertion has no supporting test record in this packet. Mark uncertainty, not proven false.'
  else:
   category='MARKETING_OR_CUSTOMER_SENTIMENT_ASSERTION_REVIEW_TRIGGER';finding='Popularity, customer sentiment or style wording is a review trigger; the detector does not prove a factual contradiction or invalidate a faithful translation.'
  checks.append({'sourceText':text,'originalFlags':sorted(flags),'classification':category,'finding':finding})
 reviewed=rid in {r['resourceId'] for r in allrows}
 rows.append({'resourceId':rid,'sourceDigest':by['ru'][rid]['sourceDigest'],'candidateLocales':['ru','sv'],'independentMeaningReview':'PASS' if reviewed else 'NOT_RUN_BY_THIS_REVIEWER','demonstratedPolicyScopeMismatch':any(c['classification'].startswith('DEMONSTRATED') for c in checks),'separateOwnerReservation':rid.endswith('559662366817'),'translationReleaseDisposition':'IN_FINAL_24_ROW_INDEX' if reviewed else 'ROOT_SOURCE_DISPOSITION_AND_INDEPENDENT_MEANING_REVIEW_REMAIN','claims':checks})
result={'status':'EXACT_SOURCE_FLAG_CLASSIFICATION_NOT_BLANKET_INVALIDATION','articles':len(rows),'claimOccurrences':sum(len(r['claims']) for r in rows),'classCounts':dict(collections.Counter(c['classification'] for r in rows for c in r['claims'])),'articlesWithDemonstratedRecordedPolicyMismatch':sum(r['demonstratedPolicyScopeMismatch'] for r in rows),'previouslyFlaggedArticlesNowIndependentlyQualified':sum(r['independentMeaningReview']=='PASS' for r in rows),'policyEvidence':policy,'rows':rows,'limits':['A heuristic source flag is not proof that a claim is false, and is not new user-approval policy. Ordinary accurate source-preserving translations are in scope.','This review does not certify truth of unsupported empirical, protection, bundle, promotion or performance assertions. Root must reconcile specific facts rather than silently rewriting English or fabricating backing evidence.','Only 24 exact body rows have completed independent full language/structure review by this reviewer; the other 110 remain unreviewed here.','No connector calls after the parent reported rate limiting. No provider, browser, live/Git/canonical edits.']}
write('article_source_flag_classification.json',result)
print(json.dumps({k:result[k] for k in ['articles','claimOccurrences','classCounts','articlesWithDemonstratedRecordedPolicyMismatch','previouslyFlaggedArticlesNowIndependentlyQualified']},ensure_ascii=False,indent=2))
