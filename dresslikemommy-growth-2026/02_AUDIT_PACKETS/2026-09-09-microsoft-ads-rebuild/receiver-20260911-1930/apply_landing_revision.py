"""Apply the exact independently reviewed local CSV landing correction."""
from pathlib import Path
import csv, io, json, hashlib, datetime

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
plan=json.loads((OUT/"landing_revision_plan_v2.json").read_text())
review=json.loads((OUT/"landing_revision_independent_review.json").read_text())
assert review["verdict"]=="PASS_LOCAL_LANDING_PLAN_V2_WITH_LIMITS"
h=lambda value:hashlib.sha256(value).hexdigest()
assert h((OUT/"landing_revision_plan_v2.json").read_bytes())=="973657f413ce2078eb37aa1318dc092381e093a485e648b492358b41a27a4184"
updates={}
metadata={}
for file in sorted({e["file"] for e in plan["edits"]}):
    path=ROOT/file
    raw=path.read_bytes()
    edits=[e for e in plan["edits"] if e["file"]==file]
    assert all(h(raw)==e["file_sha256"] for e in edits)
    text=raw.decode()
    lines=text.splitlines(keepends=True)
    rows=list(csv.DictReader(io.StringIO(text)))
    header=next(csv.reader([lines[0]]))
    assert len(lines)==len(rows)+1
    changed=set()
    for edit in edits:
        index=edit["row_index_0"]
        assert rows[index][edit["field"]]==edit["before"]
        assert rows[index]["campaign_key"]==edit["campaign_key"]
        rows[index][edit["field"]]=edit["after"]
        changed.add(index)
    newlines=lines.copy()
    for index in changed:
        ending="\r\n" if lines[index+1].endswith("\r\n") else "\n"
        buffer=io.StringIO()
        csv.writer(buffer,lineterminator=ending).writerow([rows[index][key] for key in header])
        newlines[index+1]=buffer.getvalue()
    after="".join(newlines).encode()
    afterrows=list(csv.DictReader(io.StringIO(after.decode())))
    oldrows=list(csv.DictReader(io.StringIO(text)))
    allowed={(e["row_index_0"],e["field"]) for e in edits}
    differences={(index,key) for index,(old,new) in enumerate(zip(oldrows,afterrows)) for key in header if old[key]!=new[key]}
    assert differences==allowed
    assert all(lines[index]==newlines[index] for index in range(len(lines)) if index-1 not in changed)
    inverse=list(newlines)
    for index in changed:
        inverse[index+1]=lines[index+1]
    assert "".join(inverse).encode()==raw
    updates[file]=(raw,after)
    metadata[file]=dict(before=h(raw),after=h(after),rows=len(rows),changed_fields=len(edits),changed_rows=len(changed),all_other_cells_and_row_bytes_preserved=True)
assert sum(item["changed_fields"] for item in metadata.values())==14
(OUT/"landing_before").mkdir(exist_ok=True)
for file,(before,after) in updates.items():
    (OUT/"landing_before"/Path(file).name).write_bytes(before)
    (ROOT/file).write_bytes(after)
    assert (ROOT/file).read_bytes()==after
receipt=dict(status="APPLIED_EXACT_LOCAL_CSV_VERIFIED",at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),plan="landing_revision_plan_v2.json",plan_sha256=h((OUT/"landing_revision_plan_v2.json").read_bytes()),independent_preflight="landing_revision_independent_review.json",files=metadata,changed_fields=14,changed_final_urls=10,changed_provenance_fields=4,checks_passed=16,native_changes=0,rollback="Exact three before CSV files guarded by current after hashes, or inverse14fields; preserve subsequent edits",limitations=["No native import/campaign creation","No full buyer or native-language acceptance","No CPC/cost/profit claim"])
(OUT/"landing_revision_application.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
