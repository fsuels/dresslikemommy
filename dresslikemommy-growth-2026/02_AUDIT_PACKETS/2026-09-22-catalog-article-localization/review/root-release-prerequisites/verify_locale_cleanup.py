import json,hashlib,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent; B=H.parents[1]; ROOT=B.parents[2]
C=B/'review/article-chrome'
manifest=json.loads((C/'before_manifest.json').read_text())
removed=json.loads((C/'unused_delivery_journey_removed.json').read_text())['removed']
manual=json.loads((C/'manual_translations.json').read_text())
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
def load(p):
 s=p.read_text();return json.loads(s[s.index('{'):])
def leaves(d,p=''):
 if isinstance(d,dict): return {k:v for key,val in d.items() for k,v in leaves(val,p+'.'+key if p else key).items()}
 return {p:d}
checks=[]
for rel,deleted in removed.items():
 d=load(ROOT/rel); count=len(leaves(d)); article=d['storefront'].pop('article');assert len(article)==20
 assert 'delivery_journey' not in d['products'] and len(deleted)==13
 d['products']['delivery_journey']=deleted
 assert sha(json.dumps(d,sort_keys=True,ensure_ascii=False))==manifest[rel]['json_without_article_sha256'],rel
 expected=manual.get(Path(rel).stem,manual['en.default'])
 assert article==expected,rel
 assert count<=3400,rel
 checks.append({'file':rel,'leaves':count,'removedLeaves':len(deleted),'preArticleBaselineRestoredExactly':True,'articleKeysAndValuesUnchanged':True,'checkoutAndAllOtherValuesUnchanged':True,'currentSHA256':hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()})
q=subprocess.run(['rg','-n','delivery_journey',*[str(ROOT/x) for x in ['assets','config','layout','sections','snippets','templates']]],text=True,capture_output=True)
assert q.returncode==1 and not q.stdout and not q.stderr
report={'status':'PASS','method':'Restore deleted subtree and remove article subtree; compare normalized full JSON SHA to pre-article independent baseline. Check current article exact approved copy, JSON leaf cap, and all shipped theme references.','filesChecked':len(checks),'noShippedReferences':True,'rows':checks,'limitSource':'3400 from root-observed native Shopify rejection; not independently queried','liveImportVerification':'ROOT_OWNED_NOT_RUN_BY_REVIEWER'}
(H/'locale_cleanup_independent.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({'status':'PASS','files':len(checks),'heLeaves':next(x['leaves'] for x in checks if x['file']=='locales/he.json')})
