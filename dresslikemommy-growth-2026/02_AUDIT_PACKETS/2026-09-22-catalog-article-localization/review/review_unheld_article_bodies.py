#!/usr/bin/env python3
"""Record independent full prose review and reproduce source/markup checks locally."""
import collections,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;P=HERE.parent;ROOT=P.parents[2]
sys.path.insert(0,str(P/'tooling'));import offline_translation as ot

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vsha(v):return hashlib.sha256(v.encode()).hexdigest() if v is not None else None
def write(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

sources={'ru':P/'articles/ru-bodies/candidate_all_complete.json','sv':P/'tooling/sv-bodies/candidate.json'}
bylocale={lc:{r['resourceId']:r for r in read(p)['rows']} for lc,p in sources.items()}
assert set(bylocale['ru'])==set(bylocale['sv']) and len(bylocale['ru'])==67
svmanifest=read(P/'tooling/sv-bodies/final_manifest.json');assert sha(sources['sv'])==svmanifest['candidateSHA256']
sv_batches=[]
for b in svmanifest['finalBatches']:
 p=P/'tooling/sv-bodies'/b['file'];assert sha(p)==b['sha256'];sv_batches+=read(p)['rows']
assert sv_batches==list(bylocale['sv'].values())
ru_author=read(P/'articles/ru-bodies/author_review.json');assert sha(sources['ru'])==ru_author['candidateSHA256']
ru_batches=[]
for b in ru_author['batches']:
 p=P/'articles/ru-bodies'/b['file'];assert sha(p)==b['sha256'];ru_batches+=read(p)['rows']
assert ru_batches==list(bylocale['ru'].values())
existing1=read(P/'articles/source_claims_release_review.json');existing2=read(P/'tooling/sv-bodies/source_claim_holds.json')
held={r['resourceId'] for r in existing1['articles']}|{i for r in existing2['rows'] for i in r['resourceIds']}|set(existing2['existingLedgerEditorialHold'])
assert len(held)==59
reviewed_ids=sorted(set(bylocale['ru'])-held);assert len(reviewed_ids)==8
new_editorial='gid://shopify/Article/559662006369'
review_notes={
'559471427681':'Full palette, outfit-role, accessory, four combination and photo-tip prose compared in both languages. Cream denotes color; negations and all numbered steps retained.',
'559471919201':'Full photo-guide prose compared. Separate piece counts/prices, destination delivery estimates and non-guaranteed fit guidance preserved. Both translations retain independently selected mother/daughter pieces, not a bundle guarantee.',
'559662006369':'Both translations faithfully render all source paragraphs, garment descriptions and soft fit advice. Source editorial wording about high-converting sets and easier-to-sell categories is a parent quality-review trigger, not a demonstrated translation mistake or proof of a false merchant fact.',
'559662661729':'Full spring guide compared. Florals/watercolor, layering, garment measurements, ease, inside-out washing and cool-water/high-heat negations preserved.',
'559662694497':'Full Easter guide compared. Occasion, coverage, family palette, comfort and seasonal reuse meanings retained without adding a promise.',
'559700541537':'Full care guide compared. Both retain cold/gentle wash, avoid harsh bleach/high heat, flat-dry sweaters, air-dry swimwear, low tumble only if needed and dry storage. No numerical dosing or safety instruction invented.',
'559700574305':'Full sizing guide including every table cell compared. Body-vs-flat-garment distinction, same units/method, separate child measurements, no automatic size-up, ask for clarification and separate cart choices retained.',
'559700607073':'Full gifting guide compared. All five occasions/relationships and rewear/comfort guidance retained. Source general merchandising opinions not treated as measured sales results.'}
cache={};reports=[];qualified=[];editorial=[]
for rid in reviewed_ids:
 for lc in ['ru','sv']:
  r=bylocale[lc][rid];rf=Path(r['rawFile']);rf=rf if rf.is_absolute() else (ROOT/rf if str(rf).startswith('dresslikemommy-growth-2026/') else P/'articles'/rf)
  if rf not in cache:cache[rf]=read(rf)
  n=next(n for n in cache[rf]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==rid)
  src=[s for s in n['translatableContent'] if s['key']=='body_html' and s['locale']=='en'];assert len(src)==1
  assert src[0]['value']==r['sourceValue'] and src[0]['digest']==r['sourceDigest']
  tr=[t for t in n['translations'] if t['key']=='body_html' and t['locale']==lc and t.get('market') is None]
  assert not tr and r['before'] is None
  checks=ot.verify_text(r['sourceValue'],r['value'],lc);assert not checks['errors'],(rid,lc,checks)
  events=ot.Shape(r['value']).events;assert events==ot.Shape(r['sourceValue']).events
  record={'resourceId':rid,'locale':lc,'key':'body_html','marketId':None,'source':r['sourceValue'],'sourceDigest':r['sourceDigest'],'sourceSHA256':vsha(r['sourceValue']),'before':None,'expectedBeforeValueSHA256':None,'value':r['value'],'valueSHA256':vsha(r['value']),'rawFile':str(rf.relative_to(P)),'rawFileSHA256':sha(rf),'candidateFile':str(sources[lc].relative_to(P)),'candidateFileSHA256':sha(sources[lc]),'bindingReviewCode':'EXACT_EN_SOURCE_OPAQUE_DIGEST_EXPLICIT_LOCALE_GLOBAL_MISSING_PASS','meaningReviewCode':'INDEPENDENT_FULL_SOURCE_TARGET_PROSE_PASS','structureReviewCode':'EXACT_HTML_ATTRIBUTES_URLS_NUMBERS_TABLES_PASS','requiresFreshLiveSourceAndBeforeGuard':True}
  report={k:record[k] for k in ['resourceId','locale','sourceDigest','valueSHA256','candidateFile','candidateFileSHA256','bindingReviewCode','meaningReviewCode','structureReviewCode']};report['reviewNote']=review_notes[rid.rsplit('/',1)[1]];report['sourceEditorialDisposition']='ROOT_EDITORIAL_REVIEW_TRIGGER_NO_TRANSLATION_ERROR' if rid==new_editorial else 'NO_ADDITIONAL_SOURCE_ERROR_IDENTIFIED'
  reports.append(report)
  (editorial if rid==new_editorial else qualified).append(record)
assert len(qualified)==14 and len(editorial)==2
fresh=read(HERE/'fresh_products_pages.json');f=[n for p in fresh['pages'] for n in p['data']['products']['nodes']];old=[n for p in sorted((P/'products').glob('inventory_page_*.json')) for n in read(p)['data']['products']['nodes']]
a,b={n['id'] for n in old},{n['id'] for n in f};assert len(a)==len(b)==238 and a==b
handles={n['handle']:n['id'] for n in f};links=[]
for rid in reviewed_ids:
 for handle in sorted(set(re.findall(r'href=[\"\'](?:https://www.dresslikemommy.com)?/products/([^\"\'?#]+)',bylocale['ru'][rid]['sourceValue']))):
  links.append({'articleId':rid,'productHandle':handle,'publishedProductId':handles.get(handle),'status':'IN_FRESH_PUBLISHED_INVENTORY' if handle in handles else 'NOT_IN_PUBLISHED_ID_SET_REQUIRES_ROOT_ROUTE_CHECK'})
write('fresh_product_id_reconciliation.json',{'status':'PASS','capturedAt':fresh['capturedAt'],'baselineProducts':len(a),'freshProducts':len(b),'added':sorted(b-a),'removed':sorted(a-b),'pages':5,'lastHasNextPage':fresh['pages'][-1]['data']['products']['pageInfo']['hasNextPage'],'rawSHA256':sha(HERE/'fresh_products_pages.json'),'productLinksInReviewedArticles':links,'limits':'Current ID/handle/publication inventory; does not prove a product in stock or a localized URL rendered correctly.'})
write('qualified_article_body_release_index.json',{'status':'14_INDEPENDENTLY_REVIEWED_ROWS_REQUIRES_FRESH_ROOT_GUARDS','rows':qualified,'limits':['Only these 14 exact source-bound row values qualified here; not the whole 134-draft body cohort.','Source/translation current-before guards and public route checks remain root-owned.','No external writes, providers or Git.']})
write('article_editorial_trigger_rows.json',{'status':'SOURCE_EDITORIAL_TRIGGER_NOT_TRANSLATION_ERROR','rows':editorial,'exactSourcePhrases':['shortest path to a high-converting set','easier to sell'],'assessment':'Both translations are accurate. These two rows have the same independent meaning/structure PASS. Root can release the faithful translation within existing user scope if choosing to retain existing source copy. Do not turn this editorial recommendation into a new permission gate.'})
write('unheld_article_body_independent_review.json',{'status':'PASS_16_MEANING_AND_STRUCTURE_14_RELEASE_INDEX_2_EDITORIAL_TRIGGERS','reviewer':'product_release_review','reviewedArticles':8,'reviewedFields':16,'qualifiedImmediateFields':14,'sourceEditorialTriggerFields':2,'reports':reports,'method':'Independently read full English, Russian and Swedish prose for all eight articles. Raw source/digest and explicit locale/global missing-before, exact HTML tag/attribute events, URLs, numerics, tables and placeholder checks independently recomputed. Reconciled final author batches to authoritative candidates.','limits':['Source opinions are not treated as measured evidence. Previously flagged source claims remain review triggers until root records a demonstrated contradiction, retained-source disposition, or authorized source change.','No supplier/current inventory availability verification inferred; only published ID/handle inventory checked.','No live writes or rendered verification by this lane.']})
print(json.dumps({'articleMeaningPass':16,'articleImmediateIndex':14,'editorialTriggerNoTranslationError':2,'productIDsMatch':238,'articleProductLinks':len(links),'unresolvedProductHandles':[x for x in links if not x['publishedProductId']]},ensure_ascii=False))
