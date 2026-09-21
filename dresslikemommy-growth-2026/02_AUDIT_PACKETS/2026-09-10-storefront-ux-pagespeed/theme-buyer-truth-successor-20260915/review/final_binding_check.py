"""Independent local-only binding checks; writes only its owned review receipt."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

PACKET = Path(__file__).resolve().parent.parent
ROOT = PACKET.parents[3]
EXPECTED_MODULE = "86c6bf6ab98ee2a61f60dd755c41a2861c3d371d040db45655de23e9ce0f46b3"
EXPECTED_PRELIMINARY = "70bc41f8afff09fcb17a8e5b8e7b4aae7d65dabdb3a64088912f24b78fd63f3a"
EXPECTED_ROLLBACK = "244ae9843582d00aaa79106efb1bec993f11348da1ece279b18da8b4fb79b361"
MODULE = "assets/product-desktop-ux-20260513-ruler-sync.js"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((PACKET / name).read_text())


def main():
    expected_payload = sys.argv[1]
    preliminary = read("review/non-module-before-review.json")
    checks = []
    bindings = {}

    def check(name, passed, details=None):
        checks.append({"name": name, "pass": bool(passed), "details": details})

    def bind(path):
        bindings[str(path)] = digest(path)
        return bindings[str(path)]

    check("original_independent_nonmodule_receipt_unchanged", bind(PACKET / "review/non-module-before-review.json") == EXPECTED_PRELIMINARY)
    check("all_30_previously_reviewed_baseline_and_nonmodule_artifacts_unchanged", all(bind(Path(path)) == sha for path, sha in preliminary["reviewed_file_hashes"].items()), {"count": len(preliminary["reviewed_file_hashes"])})
    expected = {f["filename"]: f["candidate_after_sha256"] for f in preliminary["non_module_files"]}
    expected[MODULE] = EXPECTED_MODULE
    expected_local = {f["filename"]: f["local_after_sha256"] for f in preliminary["non_module_files"]}
    expected_local[MODULE] = EXPECTED_MODULE
    check("exact_seven_candidate_files", {str(f.relative_to(PACKET / "candidate-after")) for f in (PACKET / "candidate-after").rglob("*") if f.is_file()} == set(expected))
    for filename in sorted(expected):
        check("candidate_after:" + filename, bind(PACKET / "candidate-after" / filename) == expected[filename])
        check("local_after:" + filename, bind(ROOT / filename) == expected_local[filename])

    for payload_name, directory, payload_sha in [
        ("upload-payload.json", "candidate-after", expected_payload),
        ("rollback-payload.json", "candidate-before", EXPECTED_ROLLBACK),
    ]:
        payload = read(payload_name)
        check(payload_name + ":hash", bind(PACKET / payload_name) == payload_sha)
        check(payload_name + ":exact_target_and_fields", set(payload) == {"themeId", "files"} and payload["themeId"] == "gid://shopify/OnlineStoreTheme/137888792673")
        check(payload_name + ":seven_unique_authorized_existing_files", len(payload["files"]) == 7 and {f["filename"] for f in payload["files"]} == set(expected))
        for f in payload["files"]:
            check(payload_name + ":exact_text:" + f["filename"], set(f) == {"filename", "body"} and set(f["body"]) == {"type", "value"} and f["body"]["type"] == "TEXT" and f["body"]["value"].encode() == (PACKET / directory / f["filename"]).read_bytes())

    prepared = read("PREPARED_FILES.json")
    check("prepared_manifest_not_superseded", "SUPERSEDED" not in prepared["status"])
    check("prepared_manifest_payloads_exact", prepared["uploadPayloadSha256"] == expected_payload and prepared["rollbackPayloadSha256"] == EXPECTED_ROLLBACK)
    check("prepared_manifest_seven_files", len(prepared["files"]) == 7 and {f["filename"] for f in prepared["files"]} == set(expected))
    check("prepared_manifest_file_hashes_exact", all(f["afterSha256"] == expected[f["filename"]] and f["localAfterSha256"] == expected_local[f["filename"]] and f["beforeSha256"] == digest(PACKET / "candidate-before" / f["filename"]) for f in prepared["files"]))

    module_manifest = read("module/MANIFEST.json")
    check("module_manifest_source_exact", module_manifest["module_sha256"] == EXPECTED_MODULE)
    check("module_manifest_all_artifacts_exact", all(bind(ROOT / f["path"]) == f["sha256"] for f in module_manifest["files"] + module_manifest["inputs"]))
    check("worker_corrected_test_results_bound", read("module/VERIFICATION.json")["after_sha256"] == EXPECTED_MODULE and read("module/VERIFICATION.json")["tests"] == 25)
    corrected = read("review/independent-corrected-holdouts.json")
    check("independent_oracle_unchanged_both_failures_now_pass", corrected["exitCode"] == 0 and corrected["sourceStable"] and corrected["productionSha256"] == EXPECTED_MODULE and corrected["oracleSha256"] == digest(PACKET / "review/provisional-challenges.cjs"))
    rerun = read("review/module-independent-checks.json")
    check("independent_syntax_25_tests_nine_protected_functions_pass", rerun["status"] == "PASS" and rerun["moduleSha256"] == EXPECTED_MODULE and rerun["testScriptSha256"] == digest(PACKET / "module/buyer-truth.test.cjs"))
    for name in ["PREPARED_FILES.json", "RELEASE_FRAME.json", "GRAPHQL_VALIDATION.json", "NON_MODULE_VALIDATION.json", "write.graphql", "read.graphql", "module/MANIFEST.json", "module/VERIFICATION.json", "review/provisional-challenges.cjs", "review/provisional-challenges-original-failures.json", "review/independent-corrected-holdouts.json", "review/module-independent-checks.json"]:
        bind(PACKET / name)
    report = {
        "action": "TA06-THEME-BUYER-TRUTH-SUCCESSOR-20260915",
        "checkedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reviewer": "/root/main_sync_review",
        "status": "PASS" if all(c["pass"] for c in checks) else "FAIL",
        "exactUploadSha256": expected_payload,
        "moduleSha256": EXPECTED_MODULE,
        "checks": checks,
        "reviewedFileHashes": bindings,
    }
    destination = PACKET / "review/final-binding-checks.json"
    assert not destination.exists(), "Preserve original review checks"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "checks": len(checks), "failed": [c for c in checks if not c["pass"]], "reportSha256": digest(destination)}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
