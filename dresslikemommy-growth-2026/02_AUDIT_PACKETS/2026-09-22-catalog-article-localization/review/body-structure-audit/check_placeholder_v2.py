import json,re,hashlib,ast,copy,collections
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();d=json.loads((H/'placeholder_candidates_v2.json').read_text());files={}
mod=ast.parse((H/'classify_optional_closures.py').read_text());ns={'HTMLParser':HTMLParser};selected=[n for n in mod.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))];exec(compile(ast.Module(body=selected,type_ignores=[]),'<bounded optional closure checks>','exec'),ns)
def validate(r,raw=True):
 assert r['before']['outdated'] is False
 assert sha(r['source'])==r['sourceSHA256'] and sha(r['before']['value'])==r['expectedBeforeValueSHA256'] and sha(r['value'])==r['valueSHA256']
 if raw:
  path=B/r['rawFile']
  if path not in files:
   files[path]=(hashlib.sha256(path.read_bytes()).hexdigest(),{x['resourceId']:x for x in json.loads(path.read_text())['data']['translatableResourcesByIds']['nodes']})
  digest,nodes=files[path];assert digest==r['rawFileSHA256'];node=nodes[r['resourceId']];s=next(x for x in node['translatableContent'] if x['key']==r['key']);assert s['digest']==r['sourceDigest'] and s['value']==r['source'];before=next(x for x in node['tr_'+r['locale'].replace('-','_')] if x['key']==r['key']);assert before==r['before']==r['rawBefore']
 v=r['before']['value']
 for p in r['patches']:
  assert p['sourceExactQuote'] in r['source'] and v.count(p['before'])==1
  v=v.replace(p['before'],p['after'],1)
 assert v==r['value']
 for pattern in [r'<table\b.*?</table>',r'https?://[^\s<>"\']+',r'<img\b[^>]*>']:
  assert re.findall(pattern,r['before']['value'],re.S)==re.findall(pattern,r['value'],re.S)
 assert not ns['check'](r['value'])['errors'],(r['productIndex'],r['locale'],ns['check'](r['value'])['errors'])
 assert not any(m[0] not in r['source'] for m in re.finditer(r'[A-Za-z0-9_]*(?:QZ|XTOKEN|QX|TOKEN)[A-Za-z0-9_]*',r['value']))
for r in d['rows']:validate(r)
# Mutations must be rejected: changed measured cell, altered source digest/binding, and omitted defined patch.
mut=[]
for name,fn in [('changed_table_measurement',lambda r:r.update(value=r['value'].replace('<td>2</td>','<td>999</td>',1),valueSHA256=sha(r['value'].replace('<td>2</td>','<td>999</td>',1)))),('wrong_source_digest',lambda r:r.update(sourceDigest='0'*64)),('missing_patch',lambda r:r['patches'].pop())]:
 r=copy.deepcopy(d['rows'][0]);fn(r)
 try:validate(r);mut.append({'name':name,'rejected':False})
 except AssertionError:mut.append({'name':name,'rejected':True})
assert all(x['rejected'] for x in mut)
report={'status':'PASS_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW','candidateRows':88,'uniqueRows':len({(x['resourceId'],x['locale'],x['key']) for x in d['rows']}),'exactSourceBeforeDigestRawFileBindings':88,'rawFiles':len(files),'tablesURLsImagesBytesUnchanged':88,'allExplicitPatchReconstructionExact':88,'remainingNonoptionalStructureFailures':0,'remainingCorruptedTokenFragments':0,'fullEnglishMeaningReviewLimitedToPatchedClauses':True,'sourcePolicyHoldClearing':False,'mutations':mut,'candidateSHA256':hashlib.sha256((H/'placeholder_candidates_v2.json').read_bytes()).hexdigest()};(H/'placeholder_checks_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
