"""Verify and assemble the local-only V8 proposal without changing V7 or Shopify."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
CANDIDATE = PACKET / "candidate"
PROPOSED = HERE / "proposed"
EXPECTED = {
    "sections/footer.liquid", "locales/nl.json", "locales/de.json",
    "locales/el.json", "locales/fi.json", "locales/ro-RO.json", "locales/ro.json",
}


def digest(data, algorithm="md5"):
    return hashlib.new(algorithm, data).hexdigest()


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def locale(data):
    return json.loads(re.sub(r"^\s*/\*[\s\S]*?\*/\s*", "", data.decode()))


def leaves(obj, prefix=""):
    if isinstance(obj, dict):
        return {k: v for key, value in obj.items()
                for k, v in leaves(value, f"{prefix}.{key}" if prefix else key).items()}
    return {prefix: obj}


source = json.loads((HERE / "source-before.json").read_text())
themes = source["data"]
source_files = {n["filename"]: n for n in themes["preview"]["files"]["nodes"]}
assert themes["preview"]["id"] == "gid://shopify/OnlineStoreTheme/137888792673"
assert themes["preview"]["role"] == "UNPUBLISHED"
assert not themes["preview"]["processing"]
assert not any(t["files"]["pageInfo"]["hasNextPage"] for t in themes.values())
actual_files = {str(p.relative_to(CANDIDATE)): p for p in CANDIDATE.rglob("*") if p.is_file()}
assert actual_files.keys() == source_files.keys()
assert len(actual_files) == 527
for name, path in actual_files.items():
    data = path.read_bytes()
    assert digest(data) == source_files[name]["checksumMd5"], name
    assert len(data) == int(source_files[name]["size"]), name

proposal_files = {str(p.relative_to(PROPOSED)): p for p in PROPOSED.rglob("*") if p.is_file()}
assert proposal_files.keys() == EXPECTED
expected_locale_changes = {f["filename"]: f for f in json.loads((HERE / "locale-changes.json").read_text())["files"]}
changes, diff_parts, changed_leaves = [], [], 0
for name in sorted(EXPECTED):
    before = actual_files[name].read_bytes()
    after = proposal_files[name].read_bytes()
    assert before != after, name
    inverse = HERE / "rollback" / name
    if inverse.exists():
        assert inverse.read_bytes() == before, name
    else:
        inverse.parent.mkdir(parents=True, exist_ok=True)
        inverse.write_bytes(before)
    if name.endswith(".json"):
        old, new = leaves(locale(before)), leaves(locale(after))
        assert old.keys() == new.keys(), name
        changed = {k for k in old if old[k] != new[k]}
        spec = expected_locale_changes[name]
        assert changed == {c["key"] for c in spec["changes"]}, name
        for change in spec["changes"]:
            assert old[change["key"]] == change["before"]
            assert new[change["key"]] == change["after"]
        assert digest(before) == spec["beforeMd5"]
        assert digest(after) == spec["afterMd5"]
        changed_leaves += len(changed)
    changes.append({"filename": name, "beforeMd5": digest(before), "afterMd5": digest(after),
                    "beforeSha256": digest(before, "sha256"), "afterSha256": digest(after, "sha256"),
                    "beforeBytes": len(before), "afterBytes": len(after)})
    diff_parts.extend(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
                                         fromfile=f"v7/{name}", tofile=f"v8-local/{name}"))
assert changed_leaves == 22
(HERE / "proposal.diff").write_text("".join(diff_parts))

composite = Path(tempfile.mkdtemp(prefix="dlm-ux-v8-local-")) / "theme"
shutil.copytree(CANDIDATE, composite)
for name, path in proposal_files.items():
    shutil.copyfile(path, composite / name)
composite_files = {str(p.relative_to(composite)): p for p in composite.rglob("*") if p.is_file()}
assert composite_files.keys() == actual_files.keys()
local_manifest = [{"filename": name, "md5": digest(path.read_bytes()),
                   "sha256": digest(path.read_bytes(), "sha256"), "bytes": path.stat().st_size}
                  for name, path in sorted(composite_files.items())]
assert {f["filename"] for f in local_manifest if f["md5"] != source_files[f["filename"]]["checksumMd5"]} == EXPECTED
comparison = {}
for key in ("combined", "main"):
    other = {n["filename"]: n["checksumMd5"] for n in themes[key]["files"]["nodes"]}
    comparison[key] = [f["filename"] for f in local_manifest if f["md5"] != other.get(f["filename"])]

protected = ["final-checks.json", "candidate-source-validation.json"]
protected.extend(p.name for p in PACKET.glob("final-release-*") if p.is_file())
save("protected-v7-files.json", {name: digest((PACKET / name).read_bytes(), "sha256") for name in sorted(protected)})
save("proposed-manifest.json", {
    "checkedAt": datetime.now(timezone.utc).isoformat(), "status": "LOCAL_PROPOSAL_ONLY__NOT_UPLOADED",
    "sourceReadAt": source["checkedAt"], "previewId": themes["preview"]["id"],
    "sourceRole": themes["preview"]["role"], "v7CandidateExactFiles": 527,
    "incrementalFilesChanged": 7, "incrementalFilesPreserved": 520, "localeLeavesChanged": 22,
    "changes": changes, "compositePath": str(composite), "compositeFiles": local_manifest,
    "proposedDifferencesAgainst": comparison, "renderedAfter": "BLOCKED_PUBLIC_HTTP_429_STOP",
    "externalWrites": 0, "publicRequests": 0,
    "nextGate": "Actual access-condition change and bounded rendered review; elapsed time alone does not clear the gate.",
})
print(json.dumps({"status": "PASS_LOCAL_SOURCE_ONLY", "v7FilesExact": 527, "changed": 7,
                  "preserved": 520, "localeLeaves": 22, "rollbackFiles": 7,
                  "proposedDifferencesVsPredecessor": len(comparison["combined"]),
                  "proposedDifferencesVsMain": len(comparison["main"]), "compositePath": str(composite)}))
