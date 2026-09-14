from pathlib import Path
from collections import Counter
import difflib, hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parent
BASE, THEME = ROOT / 'baseline', ROOT / 'theme'
PRIOR = ROOT.parent / 'theme_candidate'
sha = lambda value: hashlib.sha256(value).hexdigest()
md5 = lambda value: hashlib.md5(value).hexdigest()
write_json = lambda name, value: (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
assert sha((PRIOR / 'candidate_files.json').read_bytes()) == '1ac332a2a99ce5ae66dc9f0485f476631457acd52b594b73134f086c433d8a6b'
baseline = json.loads((ROOT / 'complete_baseline_manifest.json').read_text())
assert len(baseline['files']) == 525
for file in baseline['files']:
    body = (BASE / file['filename']).read_bytes()
    assert md5(body) == file['md5'] and sha(body) == file['sha256'] and len(body) == file['bytes'], file['filename']

manifest, patch, delta_patch, files, rollback = [], [], [], [], []
for filename in sorted(str(file.relative_to(THEME)) for file in THEME.rglob('*') if file.is_file()):
    before = (BASE / filename).read_bytes() if (BASE / filename).exists() else None
    after = (THEME / filename).read_bytes()
    changed = before != after
    manifest.append({'filename': filename, 'baseline_md5': md5(before) if before is not None else None, 'baseline_sha256': sha(before) if before is not None else None, 'candidate_md5': md5(after), 'candidate_sha256': sha(after), 'baseline_bytes': len(before) if before is not None else None, 'candidate_bytes': len(after), 'changed': changed})
    if not changed: continue
    files.append({'filename': filename, 'baseline_checksum_md5': md5(before) if before is not None else None, 'candidate_sha256': sha(after), 'content': after.decode()})
    rollback.append({'filename': filename, 'candidate_sha256': sha(after), 'action': 'restore' if before is not None else 'remove_only_if_exact_candidate', 'content': before.decode() if before is not None else None})
    patch.extend(difflib.unified_diff((before or b'').decode().splitlines(True), after.decode().splitlines(True), fromfile='a/' + filename, tofile='b/' + filename))
    prior_path = PRIOR / 'theme' / filename
    previous = prior_path.read_bytes() if prior_path.exists() else (before or b'')
    if previous != after:
        delta_patch.extend(difflib.unified_diff(previous.decode().splitlines(True), after.decode().splitlines(True), fromfile='merchant-revision3/' + filename, tofile='release/' + filename))
assert len(manifest) == 527 and len(files) == 46
assert sum(file['baseline_checksum_md5'] is None for file in files) == 2
assert all((THEME / file['filename']).exists() for file in baseline['files'])
write_json('file_manifest.json', manifest)
(ROOT / 'changed_files.txt').write_text('\n'.join(file['filename'] for file in files) + '\n')
(ROOT / 'candidate.patch').write_text(''.join(patch))
(ROOT / 'release_delta_from_revision3.patch').write_text(''.join(delta_patch))
write_json('rollback_files.json', {'scope': 'Same exact unpublished target only, after current candidate checksum verification; do not apply automatically', 'source_theme_id': 'gid://shopify/OnlineStoreTheme/133290917985', 'files': rollback})

def verify_check(name, expected):
    text = (ROOT / name).read_text()
    assert 'Overall Status:** ✅ VALID' in text, name
    assert not re.search(r'^(ERROR|WARNING|INFO) \[', text, re.M), name
    assert f'Total Files:** {expected}' in text, name
verify_check('theme_check_release46.txt', 46)
verify_check('theme_check_baseline43.txt', 43)
verify_check('theme_check_baseline_jsonld.txt', 1)
tests = {}
for name, total, passes, failures in [('landing_regression_results.txt', 18, 18, 0), ('consent_regression_results.txt', 28, 28, 0), ('cart_regression_results.txt', 16, 15, 1), ('release_integration_results.txt', 10, 10, 0)]:
    text = (ROOT / name).read_text()
    assert f'# tests {total}\n' in text and f'# pass {passes}\n' in text and f'# fail {failures}\n' in text, name
    if failures:
        assert text.count('not ok ') == 1 and 'not ok 16 - the existing quantity count and subtotal refresh targets stay intact' in text
    tests[name] = {'total': total, 'passed': passes, 'failed': failures, 'sha256': sha((ROOT / name).read_bytes())}
whitespace = subprocess.run(['git', 'diff', '--no-index', '--check', str(BASE), str(THEME)], capture_output=True, text=True)
assert whitespace.returncode in [0, 1] and not whitespace.stdout and not whitespace.stderr
syntax = []
node = '/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
for filename in ['assets/product-desktop-ux-20260513-ruler-sync.js', 'assets/cart.js', 'assets/cookie-preferences.js']:
    result = subprocess.run([node, '--check', str(THEME / filename)], capture_output=True, text=True)
    assert result.returncode == 0 and not result.stdout and not result.stderr
    syntax.append(filename)
summary = {'status': 'FROZEN_FOR_INDEPENDENT_REVIEW_NOT_UPLOADED', 'release_revision': 1, 'source_theme_id': 'gid://shopify/OnlineStoreTheme/133290917985', 'candidate_target_theme_id': 'gid://shopify/OnlineStoreTheme/137881223265', 'baseline_files': 525, 'candidate_files': 527, 'changed_files': 46, 'new_assets': 2, 'theme_check': {'candidate_changed_files': 46, 'candidate_diagnostics': 0, 'baseline_changed_files': 44, 'baseline_diagnostics': 0, 'complete_MAIN_context': True}, 'tests': tests, 'syntax_pass': syntax, 'whitespace_check': 'PASS; expected diff exit1 with no diagnostics', 'known_cart_failure': 'Existing quantity/subtotal fixture test16 fails identically in the unchanged reviewed cart source; no newly failing test. Not a full-cart certification.', 'consent_open_limit': 'Shopify managed preferences dialog remains English on Arabic route in peer rendered evidence.', 'rendered_combined_acceptance': 'NOT_RUN; root owns exact preview desktop/mobile/locales, cart/currency, full emitted JSON parsing and policy links.', 'external_writes': 0, 'merchant_revision3_immutable': True, 'full_patch_sha256': sha((ROOT / 'candidate.patch').read_bytes()), 'delta_patch_sha256': sha((ROOT / 'release_delta_from_revision3.patch').read_bytes()), 'rollback_sha256': sha((ROOT / 'rollback_files.json').read_bytes())}
write_json('verification_summary.json', summary)
payload = {'status': summary['status'], 'release_revision': 1, 'source_theme_id': summary['source_theme_id'], 'candidate_target_theme_id': summary['candidate_target_theme_id'], 'requires_unpublished_target': True, 'file_count': len(files), 'files': files}
write_json('candidate_files.json', payload)
receipt = {'filename': 'candidate_files.json', 'sha256': sha((ROOT / 'candidate_files.json').read_bytes()), 'bytes': (ROOT / 'candidate_files.json').stat().st_size, 'file_count': len(files), 'status': summary['status'], 'release_revision': 1, 'source_theme_id': summary['source_theme_id'], 'candidate_target_theme_id': summary['candidate_target_theme_id'], 'requires_unpublished_target': True, 'full_patch_sha256': summary['full_patch_sha256'], 'delta_patch_sha256': summary['delta_patch_sha256'], 'verification_summary_sha256': sha((ROOT / 'verification_summary.json').read_bytes()), 'file_manifest_sha256': sha((ROOT / 'file_manifest.json').read_bytes())}
write_json('candidate_files_receipt.json', receipt)
print(json.dumps(receipt, indent=2))
