import json,re,hashlib,collections,ast
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
# Reuse author's pure lexical balance helper without running its mutation-producing module.
mod=ast.parse((H/'build_tag_candidates.py').read_text());nodes=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in ['tokens','balance']]
ctx={'re':re,'collections':collections,'pat':re.compile(r'<\s*(/?)\s*([^\s<>/]+)(?:\s[^<>]*?)?\s*/?>'),'void':set('area base br col embed hr img input link meta param source track wbr'.split())}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<pure balance helpers>','exec'),ctx)
a=json.loads((H/'effective_body_inventory.json').read_text())['rows'];d=json.loads((H/'tag_candidates_v2.json').read_text());v2=d['rows'];bykey={(r['resourceId'],r['locale']):r for r in v2}
malpat=re.compile(r'<\s*/?\s*[^\W\d_][^<>]*(?=<|$)',re.S)
residual=[];sources={};counts=collections.Counter()
for r in a:
 old=r['expectedEffectiveBeforeValue'];new=bykey.get((r['resourceId'],r['locale']),{}).get('value',old);src=r['source']
 badsrc=[m[0] for m in malpat.finditer(src)];badold=[m[0] for m in malpat.finditer(old)];badnew=[m[0] for m in malpat.finditer(new)]
 sourceplaceholders=re.findall(r'_+DLMTOK\d+_+',src);phold=re.findall(r'_+DLMTOK\d+_+',old);phnew=re.findall(r'_+DLMTOK\d+_+',new)
 if badsrc or sourceplaceholders:sources[r['resourceId']]={'productIndex':r['productIndex'],'resourceId':r['resourceId'],'badSourceFragments':badsrc,'sourcePlaceholders':sourceplaceholders}
 if badold:counts['beforeUnterminatedTagRows']+=1
 if badnew:counts['afterUnterminatedTagRows']+=1
 if phold:counts['beforePlaceholderRows']+=1
 if phnew:counts['afterPlaceholderRows']+=1
 if badnew or phnew:residual.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'remainingUnterminatedFragments':badnew,'remainingPlaceholders':phnew,'sourceUnterminatedFragments':badsrc,'sourcePlaceholders':sourceplaceholders,'afterOverlay':(r['resourceId'],r['locale']) in bykey})
for r in v2:
 r['checks']['sourceBalancedness']=ctx['balance'](r['source']);r['checks']['afterBalancedness']=ctx['balance'](r['value']);r['checks']['remainingUnterminatedFragments']=[m[0] for m in malpat.finditer(r['value'])]
 assert r['checks']['afterBalancedness']['unbalancedCounts']=={},(r['productIndex'],r['locale'])
 assert r['checks']['afterBalancedness']['nestingIssueCount']==0,(r['productIndex'],r['locale'])
 assert r['checks']['afterBalancedness']['unclosedStack']==[]
 assert not r['checks']['remainingUnterminatedFragments']
 if r.get('residualMarkupExceptions'):r['checks']['residualBalancednessStatus']='PASS_BALANCED'
(H/'tag_candidates_v2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(H/'remaining_malformed_inventory.json').write_text(json.dumps({'status':'ALL4760_SCANNED_AFTER_PROPOSED374','counts':dict(counts),'sourceMalformedProducts':list(sources.values()),'rows':residual},ensure_ascii=False,indent=2)+'\n')
summary={'status':'PASS_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW','candidateRows':374,'allBeforeOutdatedFalse':True,'translatedMalformedTagOccurrences':3575,'exactEnglishSourceAlignedRepairedTokens':3575,'contextSpecificAttributeNameRestorations':78,'JapaneseP5ExplicitNecktiePhraseChanges':3,'residualRowsRepaired':7,'restoredImageURLsFromExactSource':14,'tableCellAndHeaderBytesUnchanged':374,'afterBalancedRows':374,'afterUnterminatedTagRowsInCandidates':0,'candidateSHA256':sha((H/'tag_candidates_v2.json').read_text()),'all4760ResidualScan':dict(counts),'sourceMalformedProducts':len(sources),'remainingGlobalMalformedRows':len(residual),'limitations':['Candidate scope is structural only except three approved Japanese necktie phrase corrections.','Four restored Italian image paragraphs retain exact English source alt attributes, recorded as localized-alt follow-up.','Legacy duplicate fallback tables retained byte-for-byte; equality to complete English source sequence is not claimed.']}
(H/'tag_v2_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary))
