from pathlib import Path
import json,hashlib,importlib.util
P=Path(__file__).resolve().parent;R=P.parent.parent
f=R/'root-bodies/he-pl/pl_candidate_v2.json';rows=json.loads(f.read_text())['rows'];baselines=json.loads((R/'root-bodies/pl_baseline.json').read_text());bi={x['resourceId']:x for x in baselines}
s=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
out=[];proposals=[];checks=[]
for r in rows:
 assert all(r[k]==bi[r['resourceId']][k] for k in ['sourceValue','sourceDigest','before','locale','key'])
 value=r['value'];edits=[]
 for id,old,new,why in [('/559471329377','</a> aby codziennie czerpać inspiracje do stylizacji.','</a>, aby codziennie czerpać inspiracje do stylizacji.','Polish subordinate clause introduced by aby requires comma after the linked Pinterest label.'),('/559471984737','Nie potrzebujesz budżetu na projektantów,','Nie potrzebujesz budżetu na ubrania od projektantów,','Designer budget means a budget for designer clothing, not a budget for designers themselves.')]:
  if r['resourceId'].endswith(id):
   assert value.count(old)==1;value=value.replace(old,new);edits.append({'before':old,'after':new,'reason':why})
 check=v.verify_text(r['sourceValue'],value,'pl');assert not check['errors'];rr={**r,'value':value,'independentReview':'FULL_MEANING_SOURCE_BINDING_AND_PRESERVATION_PASS'}
 if edits:proposals.append({**rr,'beforeCandidateValue':r['value'],'candidateCorrectionReasons':edits})
 out.append(rr);checks.append({'resourceId':r['resourceId'],'sourceBinding':'PASS','meaning':'PASS_WITH_LISTED_MINOR_CORRECTION' if edits else 'PASS','inlineJoins':'PASS_AFTER_LISTED_CORRECTION' if edits else 'PASS','checks':check,'corrections':edits})
for name,d in [('pl_candidate_corrections.json',{'baseCandidateSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'rows':proposals}),('pl_independently_qualified.json',{'status':'10_FULL_BODY_TRANSLATIONS_QUALIFIED_WITH_TWO_MINOR_PROPOSED_EDITS','rows':out}),('pl_independent_review.json',{'status':'PASS_WITH_TWO_MINOR_CORRECTIONS','articles':10,'uniqueAlignedTextPairs':664,'separatelyReviewedUnalignedBody':'gid://shopify/Article/559471820897: 84 versus 83 nonempty text nodes is a grammatical phrase move; all 47 source block meanings retained.','baselineBindings':'10/10 sourceValue, sourceDigest, before match supplied baseline','structuralFailures':0,'sourceAssertions':'Source claims remain source claims; no new permission gate introduced. No external truth audit in this assignment.','fields':checks})]:
 (P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'qualified':10,'correctionRows':len(proposals),'structuralFailures':0}))
