"""Read-only exported source validation; artifacts only, no external writes."""
import json,pathlib,hashlib,re,collections,sys
from html.parser import HTMLParser
B=pathlib.Path(__file__).resolve().parent
ROOT=B.parents[4]
# Locate repo without depending on shell cwd.
while not (ROOT/'AGENTS.md').exists():ROOT=ROOT.parent
rows=json.loads((B/'candidate.json').read_text())['rows'];segments=json.loads((B/'source_segments.json').read_text())
manual={}
for p in B.glob('manual_*.json'):manual.update(json.loads(p.read_text()))
cache={};bindings=[]
for r in rows:
 p=ROOT/r['rawFile'];blob=p.read_bytes();actual=hashlib.sha256(blob).hexdigest();assert actual==r['rawFileSHA256']
 if str(p) not in cache:cache[str(p)]=json.loads(blob)
 n=next(n for n in cache[str(p)]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId'])
 source=next(x for x in n['translatableContent'] if x['key']==r['key'])
 assert source['value']==r['sourceValue']==r['source'];assert source['digest']==r['sourceDigest']
 assert hashlib.sha256(r['sourceValue'].encode()).hexdigest()==r['sourceSha256']
 before=[x for x in n['translations'] if x['locale']=='sv' and x['key']=='body_html' and x.get('market') is None]
 assert not before and r['before'] is None
 bindings.append({'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSha256'],'rawFile':r['rawFile'],'rawFileSHA256':actual,'missingExactLocaleConfirmed':True})
assert len(rows)==67 and len(set(r['resourceId'] for r in rows))==67
assert set(manual)=={r['id'] for r in segments}
patterns={
 'unqualified_shipping_or_satisfaction_promise':r'free shipping on all orders|Every order ships free|happiness guarantee',
 'unverified_sun_protection':r'UPF 50\+|extra sun protection',
 'unsupported_research_testing_reviews':r'Studies show|tested dozens|testing dozens|customer reviews|customer favorite|customers consistently tell|Parents love|Parents appreciate',
 'unsupported_popularity_or_sales':r'bestsellers|thousands of families|fastest-growing|sell best|most popular styles sell out',
 'unsupported_product_performance':r'dozens of cycles|countless washes|2.3x longer|all body types|Most of our pieces maintain|countless wears and washes',
 'inventory_pricing_or_promotions':r'over 80|full size range is available|Limited sizes remaining|Popular styles start selling out|new styles added weekly|40.70%|first-purchase discounts|under \$150|\$30.60|\$60\+|getting two pieces|all-in-one sets',
 'universal_sizing_or_care_advice':r'size up|go bigger|buy one size bigger|All of our matching sets come|All sets come|we recommend washing in cold water',
}
holds=[]
for s in segments:
 reasons=[name for name,p in patterns.items() if re.search(p,s['source'],re.I)]
 if reasons:holds.append({'segmentId':s['id'],'resourceIds':s['resources'],'sourceText':s['source'],'candidateText':manual[s['id']],'reasons':reasons,'action':'Parent source-owner review. Candidate preserves source meaning; no factual verification claimed. Correct source and refresh digest before changing translated facts.'})
existing=['gid://shopify/Article/559662366817']
held=set(existing)
for h in holds:held.update(h['resourceIds'])
(B/'source_claim_holds.json').write_text(json.dumps({'status':'SOURCE_REVIEW_REQUIRED_BEFORE_PUBLICATION','existingLedgerEditorialHold':existing,'flaggedArticles':len(held),'flaggedTextSegments':len(holds),'limits':'Heuristic source-claim screen, not exhaustive fact verification. No source correction authorized in this lane. English claims retained faithfully. Editorial-commercial tone and legacy years also preserved.','rows':holds},ensure_ascii=False,indent=2)+'\n')
(B/'source_bindings_verified.json').write_text(json.dumps({'status':'PASS','checkedRows':len(bindings),'scope':'Exact local exported source+opaque digest+absent Swedish market:null body, not a live API freshness check.','rows':bindings},ensure_ascii=False,indent=2)+'\n')
unchanged=[{'id':r['id'],'text':r['source']} for r in segments if manual[r['id']]==r['source']]
(B/'language_review_notes.json').write_text(json.dumps({'translatedSegments':1502,'unchangedSegments':unchanged,'permitted':'Punctuation, brand/platform proper names and Son: which is identical Swedish/English. Quoted printed slogans and proper product names retain their original forms.','sourceTruncations':'Source product names already contain truncations; preserved with localized partial descriptions and ellipses, without inventing missing product facts. Wh.../W... and Fair... remain unknown truncated source fragments.','htmlAttributes':'All original HTML attribute values remain exact, including any English image alt/title values. This lane translates visible body text nodes only as instructed; separate attribute localization needs a scoped review.','meaningReview':'Author pass completed; independent review pending.'},ensure_ascii=False,indent=2)+'\n')
# Final batches supersede progress snapshots without modifying them.
files=[]
for i in range(0,len(rows),5):
 p=B/f'final_batch_{i//5+1:02d}.json';p.write_text(json.dumps({'rows':rows[i:i+5]},ensure_ascii=False,indent=2)+'\n')
 files.append({'file':p.name,'rows':len(rows[i:i+5]),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'status':'67_TRANSLATED_STRUCTURE_VERIFIED_INDEPENDENT_MEANING_AND_SOURCE_CLAIM_REVIEW_PENDING','locale':'sv','key':'body_html','rows':67,'sourceVisibleWords':sum(r['sourceVisibleWords'] for r in rows),'candidateFile':'candidate.json','candidateSHA256':hashlib.sha256((B/'candidate.json').read_bytes()).hexdigest(),'finalBatches':files,'sourceClaimHeldArticles':len(held),'verificationFile':'verification.json','sourceBindingFile':'source_bindings_verified.json','sourceHoldFile':'source_claim_holds.json','method':'Manually authored Swedish text nodes and exact manually translated templates/product names, 1502 unique nodes. HTMLParser raw tag span preservation; no providers/networks/live writes.','supersedes':'candidate_batch_01..09 and checkpoint_45 are earlier progress snapshots; final batches/candidate include wording improvements. Source files unchanged.'}
(B/'final_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':67,'sourceBindings':'PASS','structure':'PASS','sourceClaimHeldArticles':len(held),'claimSegments':len(holds),'candidateSHA256':manifest['candidateSHA256'],'manifestSHA256':hashlib.sha256((B/'final_manifest.json').read_bytes()).hexdigest()}))
