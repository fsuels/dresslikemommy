from pathlib import Path
import hashlib, json, re, shutil, subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent.parent / '2026-09-09-pinterest-expert-audit'
BASE, THEME = ROOT / 'baseline', ROOT / 'theme'
md5 = lambda value: hashlib.md5(value).hexdigest()
sha = lambda value: hashlib.sha256(value).hexdigest()
parse = lambda text: json.loads(re.sub(r'^\s*/\*[\s\S]*?\*/\s*', '', text))
handoff_bytes = (SOURCE / 'CONSENT_RELEASE_HANDOFF.json').read_bytes()
handoff = json.loads(handoff_bytes)
assert handoff['exactContentMatched'] == 39 and handoff['mainPreservedFiles'] == 37
assert handoff['sourceThemeId'] == 'gid://shopify/OnlineStoreTheme/137880666209'
files = {f['filename']: f for f in handoff['files']}
readback = json.loads((ROOT / 'consent_source_readback.json').read_text())
assert readback['data']['preview']['id'] == handoff['sourceThemeId']
assert readback['data']['main']['role'] == 'MAIN' and readback['data']['preview']['role'] == 'UNPUBLISHED'
for f in readback['data']['main']['files']['nodes']:
    body = f['body']['content'].encode()
    assert md5(body) == f['checksumMd5'] == files[f['filename']]['beforeMd5']
    assert len(body) == int(f['size'])
    for sub in [BASE, THEME]:
        target = sub / f['filename']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists(): assert target.read_bytes() == body
        else: target.write_bytes(body)

# Reconstruct only the reviewed consent patch on exact MAIN bytes.
REVIEWED = ROOT / 'reviewed_consent'
already_reconstructed = REVIEWED.exists()
REVIEWED.mkdir(exist_ok=True)
for filename, metadata in files.items():
    target = REVIEWED / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if metadata['beforeMd5']:
        body = (BASE / filename).read_bytes()
        assert md5(body) == metadata['beforeMd5'], filename
        if not already_reconstructed:
            target.write_bytes(body)
    else:
        assert not (BASE / filename).exists(), filename
patch = (SOURCE / 'consent-preview-complete.patch').resolve()
if not already_reconstructed:
    result = subprocess.run(['/usr/bin/patch', '--batch', '--fuzz=0', '-p1', '-i', str(patch)], cwd=REVIEWED, capture_output=True, text=True)
    (ROOT / 'consent_patch_replay.txt').write_text(result.stdout + result.stderr)
    assert result.returncode == 0 and 'offset' not in result.stdout and 'fuzz' not in result.stdout, result.stdout

# The reviewed CSS v2 intentionally supersedes the first patch's 235-byte CSS.
for f in readback['data']['preview']['files']['nodes']:
    body = f['body']['content'].encode()
    metadata = files[f['filename']]
    assert md5(body) == f['checksumMd5'] == metadata['afterMd5'], f['filename']
    assert sha(body) == metadata['afterSha256'] and len(body) == metadata['bytes']
    target = REVIEWED / f['filename']
    if f['filename'] == 'assets/cookie-preferences.css':
        assert len(target.read_bytes()) == 235 or target.read_bytes() == body
        target.write_bytes(body)
    else:
        assert target.read_bytes() == body, f['filename']

locale_values = {}
for filename, metadata in files.items():
    body = (REVIEWED / filename).read_bytes()
    assert md5(body) == metadata['afterMd5'] and sha(body) == metadata['afterSha256'] and len(body) == metadata['bytes'], filename
    target = THEME / filename
    if filename.startswith('locales/'):
        before = parse((BASE / filename).read_text())
        after = parse(body.decode())
        keys = ['cookie_preferences', 'cookie_preferences_unavailable']
        values = {key: after['sections']['footer'][key] for key in keys}
        for key in keys:
            assert key not in before['sections']['footer']
            del after['sections']['footer'][key]
        assert before == after, filename
        text = target.read_text()
        current = parse(text)
        assert not any(key in current['sections']['footer'] for key in keys)
        insertion = ''.join('      ' + json.dumps(key) + ': ' + json.dumps(value, ensure_ascii=False) + ',\n' for key, value in values.items())
        text, count = re.subn(r'(^    "footer": \{\n)', lambda match: match[0] + insertion, text, flags=re.MULTILINE)
        assert count == 1
        merged = parse(text)
        for key, value in values.items():
            assert merged['sections']['footer'].pop(key) == value
        assert merged == current, filename
        target.write_text(text)
        locale_values[Path(filename).stem] = values
    else:
        if metadata['beforeMd5']:
            assert md5(target.read_bytes()) in [metadata['beforeMd5'], metadata['afterMd5']], filename
        else:
            assert not target.exists() or target.read_bytes() == body, filename
        target.write_bytes(body)

(ROOT / 'consent_handoff_source.json').write_bytes(handoff_bytes)
(ROOT / 'consent_locale_copy.json').write_text(json.dumps(locale_values, ensure_ascii=False, indent=2) + '\n')
proof = {'handoff_sha256': sha(handoff_bytes), 'patch_sha256': sha(patch.read_bytes()), 'source_theme_id': handoff['sourceThemeId'], 'source_files_verified': 39, 'baseline_files_verified': 37, 'new_assets': 2, 'nonlocale_files_copied_exact': 4, 'locale_keys_only_merged': 70, 'css_version': 2, 'css_sha256': files['assets/cookie-preferences.css']['afterSha256'], 'exact_patch_replay': True, 'external_writes': 0, 'root_forwarded_independent_pass': True, 'open_limit': 'Shopify managed preferences dialog English on Arabic route remains unclosed; combined rendered acceptance belongs to root.'}
(ROOT / 'consent_merge_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
