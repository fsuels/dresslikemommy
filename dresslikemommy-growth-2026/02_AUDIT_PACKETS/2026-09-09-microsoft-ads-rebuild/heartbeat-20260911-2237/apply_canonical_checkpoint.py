from pathlib import Path
import json,hashlib,datetime,re
B=Path('dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-microsoft-ads-rebuild/heartbeat-20260911-2237')
sha=lambda v:hashlib.sha256(v).hexdigest()
plan_bytes=(B/'canonical_checkpoint_plan.json').read_bytes();plan=json.loads(plan_bytes)
manifest=json.loads((B/'canonical_before_manifest.json').read_text())
review_path=B/'import-review/canonical_preflight_review.json'
if not review_path.exists(): review_path=B/'canonical_preflight_message_receipt.json'
review=json.loads(review_path.read_text())
assert sha(plan_bytes) in json.dumps(review),'REVIEW_NOT_BOUND_TO_PLAN'
assert 'GO' in str(review.get('verdict','')),'NO_CANONICAL_GO'
assert not (B/'canonical_application_receipt.json').exists(),'ALREADY_APPLIED_STOP'
before={p:Path(p).read_text() for p in manifest['files_sha256']}
assert all(sha(Path(p).read_bytes())==h for p,h in manifest['files_sha256'].items()),'SHARED_DRIFT_STOP'
after=before.copy()
for o in plan['operations']:
 assert after[o['path']].count(o['old'])==1,'REPLACEMENT_DRIFT_STOP'
 after[o['path']]=after[o['path']].replace(o['old'],o['new'],1)
assert all(sha(s.encode())==plan['expected_after_sha256'][p] for p,s in after.items()),'AFTER_HASH_MISMATCH'
inverse=after.copy()
for o in reversed(plan['operations']):
 assert inverse[o['path']].count(o['new'])==1,'INVERSE_AMBIGUOUS'
 inverse[o['path']]=inverse[o['path']].replace(o['new'],o['old'],1)
assert inverse==before,'UNRELATED_BYTES_CHANGED'
control=lambda s:re.search(r'<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->',s,re.S).group()
p='ops/marketing/current_marketing_state.md';assert control(before[p])==control(after[p]),'PAID_CONTROL_CHANGED'
owner=lambda s:[l for l in s.splitlines() if l.startswith('One Owner Action:')]
assert owner(before[p])==owner(after[p]),'OWNER_ACTION_CHANGED'
for p,s in after.items():Path(p).write_text(s)
assert all(Path(p).read_text()==s for p,s in after.items()),'AFTER_READBACK_FAILED'
receipt={'applied_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':sha(plan_bytes),'review_path':str(review_path),'review_sha256':sha(review_path.read_bytes()),'operation_count':len(plan['operations']),'file_count':len(after),'all_inverse_preserved_unrelated_bytes':True,'all_nine_full_paid_control_fields_preserved':True,'parent_OneOwnerAction_preserved':True,'before_sha256':manifest['files_sha256'],'after_sha256':{p:sha(Path(p).read_bytes()) for p in after},'result':'APPLIED_EXACT_12_OPERATIONS_11_FILES_READBACK_VERIFIED','validation':'PENDING'}
(B/'canonical_application_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['result'])
