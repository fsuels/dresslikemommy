"""Versioned native-hold verification; no credentials or network operations."""
import json
import shutil
import subprocess


SOURCE_FILES = ('us-en.tsv', 'us-en.manifest.json', 'us-en.diagnostics.json', 'us-en.snapshot.json')


def verify_release(app):
    raw = app.NATIVE_PROFILE_MANIFEST.read_bytes()
    app.require(app.sha(raw) == app.FREEZE_SHA, 'release_profile_manifest_drift')
    contract = json.loads(raw)
    app.require(contract['profile'] == app.RELEASE_PROFILE and contract['configSha256'] == app.CONFIG_SHA,
                'release_profile_identity_mismatch')
    roots = {'builder': app.RELEASE, 'local': app.HERE, 'audit': app.BASE.parent.parent}
    for item in contract['files']:
        root = roots[item['root']].resolve()
        path = root / item['path']
        app.require(path.resolve().is_relative_to(root) and not path.is_symlink(), 'release_profile_path_out_of_scope')
        app.require(app.sha(path.read_bytes()) == item['sha256'], 'release_profile_dependency_drift')
    app.require(app.sha((app.RELEASE / 'config.json').read_bytes()) == app.CONFIG_SHA, 'us_config_drift')
    return contract


def verify_run_profile(app, run):
    app.verify_freeze()
    prepared = app.read(run / 'prepare.json')
    app.require(prepared.get('release_profile') == app.RELEASE_PROFILE and
                prepared.get('builder_freeze_sha256') == app.FREEZE_SHA and
                prepared.get('config_sha256') == app.CONFIG_SHA, 'run_release_profile_mismatch')


def replay(app, run, directory):
    verify_run_profile(app, run)
    command = [str(app.NODE), str(app.HERE / 'verify_native_candidate.mjs'),
               '--candidate', str(directory), '--config', str(app.RELEASE / 'config.json'),
               '--previous', str(run / 'before.pointer.json'), '--holds', str(run / 'eligibility_holds.json'),
               '--protected', json.dumps(list(app.PROTECTED_US_IDS))]
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    app.require(result.returncode == 0, 'native_candidate_replay_failed')
    try:
        summary = json.loads(result.stdout)
    except (ValueError, TypeError):
        raise app.Stop('native_candidate_replay_invalid') from None
    app.require(summary.get('mode') == 'generator_native_holds_v1' and
                summary.get('exactTsvManifestDiagnostics') is True and summary.get('networkCalls') == 0,
                'native_candidate_replay_invalid')
    app.verify_freeze()
    return summary


def contain(app, run, hold_path=None, revise=False):
    app.require(not revise, 'native_hold_change_requires_new_release_profile')
    verify_run_profile(app, run)
    app.require(not (run / 'contain.receipt.json').exists() and not (run / 'unfiltered').exists(),
                'containment_already_attempted')
    app.require(app.read(run / 'build.json')['returncode'] == 0, 'successful_build_required_before_containment')
    source = run / 'candidate'
    hold_path = hold_path or app.HOLD_SPEC
    hold_copy = run / 'eligibility_holds.json'
    if not hold_copy.exists():
        hold_copy.write_bytes(hold_path.read_bytes())
    hold_sha = app.sha(hold_copy.read_bytes())
    prepared = app.read(run / 'prepare.json')
    app.require(hold_sha == app.sha(app.HOLD_SPEC.read_bytes()) == prepared['planned_eligibility_holds_sha256'],
                'planned_hold_spec_changed')
    summary = replay(app, run, source)
    originals = {name: app.sha((source / name).read_bytes()) for name in SOURCE_FILES}
    original_dir = run / 'unfiltered'
    original_dir.mkdir()
    for name in SOURCE_FILES:
        shutil.copy2(source / name, original_dir / name)
    # The current generator has already applied the holds. Verification must not
    # rewrite the bytes, diagnostics, source snapshot or any timestamps.
    receipt = {'at_utc': app.stamp(), 'mode': 'generator_native_holds_v1',
               'release_profile': app.RELEASE_PROFILE, 'builder_freeze_sha256': app.FREEZE_SHA,
               'original_files': originals, 'hold_spec_sha256': hold_sha,
               'cohort_filter_sha256': app.sha(app.COHORT_CODE.read_bytes()),
               'native_verifier_sha256': app.sha((app.HERE / 'verify_native_candidate.mjs').read_bytes()),
               'native_replay': summary,
               'result': {'removed_available_rows': summary['removedAvailableRows'],
                          'kept_parents': summary['keptParents']},
               'source_scan_reused_without_restamping': True, 'second_filter_applied': False}
    app.save(run / 'contain.receipt.json', receipt)


def verify_containment(app, run):
    verify_run_profile(app, run)
    app.require((run / 'contain.receipt.json').exists(), 'known_eligibility_holds_not_applied')
    receipt = app.read(run / 'contain.receipt.json')
    app.require(receipt.get('mode') == 'generator_native_holds_v1' and
                receipt.get('release_profile') == app.RELEASE_PROFILE and
                receipt.get('builder_freeze_sha256') == app.FREEZE_SHA, 'containment_release_profile_mismatch')
    app.require(app.sha((run / 'eligibility_holds.json').read_bytes()) == receipt['hold_spec_sha256'] ==
                app.sha(app.HOLD_SPEC.read_bytes()), 'hold_spec_changed')
    app.require(app.sha(app.COHORT_CODE.read_bytes()) == receipt['cohort_filter_sha256'], 'cohort_filter_code_changed')
    app.require(app.sha((app.HERE / 'verify_native_candidate.mjs').read_bytes()) == receipt['native_verifier_sha256'],
                'native_verifier_changed')
    app.require(set(receipt['original_files']) == set(SOURCE_FILES), 'original_file_set_changed')
    for name, expected in receipt['original_files'].items():
        app.require(app.sha((run / 'unfiltered' / name).read_bytes()) == expected ==
                    app.sha((run / 'candidate' / name).read_bytes()), 'native_artifact_changed')
    summary = replay(app, run, run / 'candidate')
    app.require(summary == receipt['native_replay'] and receipt['result'] == {
        'removed_available_rows': summary['removedAvailableRows'], 'kept_parents': summary['keptParents']},
        'native_containment_not_exact')
    return receipt
