"""Apply reviewed Microsoft-only continuity edits with exact dirty-state guards."""
from pathlib import Path
import datetime, hashlib, json, re

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
hash_of=lambda data:hashlib.sha256(data).hexdigest()
plan_path=OUT/"canonical_update_plan.json"
plan=json.loads(plan_path.read_text())
review=json.loads((OUT/"canonical_preflight_review.json").read_text())
assert review["status"]=="PASS_EXACT_CANONICAL_PLAN"
assert review["plan_sha256"]==hash_of(plan_path.read_bytes())
expected_after={item["file"]:item["expected_after_sha256"] for item in review["files"]}
assert plan["status"]=="FROZEN_AWAITING_INDEPENDENT_REVIEW"
assert (OUT/"landing_revision_application.json").exists()
snapshot=Path(json.loads((OUT/"canonical_snapshot_location.json").read_text())["directory"])
changes={}
for file,expected_hash in plan["before_hashes"].items():
    before=(ROOT/file).read_bytes()
    assert hash_of(before)==expected_hash, ("before drift",file)
    assert (snapshot/file.replace("/","__")).read_bytes()==before
    result=before.decode()
    file_edits=[edit for edit in plan["edits"] if edit["file"]==file]
    for edit in file_edits:
        if edit["operation"]=="replace":
            assert result.count(edit["before"])==1
            result=result.replace(edit["before"],edit["after"],1)
        else:
            assert edit["operation"]=="append"
            assert edit["after"].strip() not in result
            result+=edit["after"]
    inverse=result
    for edit in reversed(file_edits):
        if edit["operation"]=="replace":
            assert inverse.count(edit["after"])==1
            inverse=inverse.replace(edit["after"],edit["before"],1)
        else:
            assert inverse.endswith(edit["after"])
            inverse=inverse[:-len(edit["after"])]
    assert inverse.encode()==before, ("inverse mismatch",file)
    assert hash_of(result.encode())==expected_after[file], ("reviewed after mismatch",file)
    changes[file]=(before,result.encode())

state=changes["ops/marketing/current_marketing_state.md"][1].decode()
control=re.search(r"<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->",state,re.S).group()
parent=next(line for line in state.splitlines() if line.startswith("One Owner Action:"))
assert hash_of(control.encode())==plan["guarded_sections"]["full_paid_control_sha256"]
assert hash_of(parent.encode())==plan["guarded_sections"]["parent_one_owner_action_sha256"]
before_plan_hash=hash_of(plan_path.read_bytes())
for file,(before,after) in changes.items():
    (ROOT/file).write_bytes(after)
    assert (ROOT/file).read_bytes()==after
receipt=dict(status="APPLIED_EXACT_AFTER_READBACK_VERIFIED",anchor=plan["anchor"],at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),frozen_plan_sha256=before_plan_hash,canonical_preflight_sha256=hash_of((OUT/"canonical_preflight_review.json").read_bytes()),files={file:dict(before=hash_of(before),after=hash_of(after),exact_inverse_preserves_unrelated_bytes=True) for file,(before,after) in changes.items()},guarded_sections=plan["guarded_sections"],source_file_count=len(changes),generated_checks="PENDING_RENDER_INTEGRATION_STRICT",writer_handoff="Ads release, brief root sublease, explicit root release back to Microsoft; next X then Pinterest")
(OUT/"canonical_application_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(dict(status=receipt["status"],source_file_count=len(changes),full_paid_preserved=True,parent_v7_action_preserved=True,all_other_bytes_preserved=True)))
