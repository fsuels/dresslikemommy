from pathlib import Path
from collections import Counter
import difflib, hashlib, json, re

ROOT = Path(__file__).resolve().parent
BASE, THEME = ROOT / 'baseline', ROOT / 'theme'
source = json.loads((ROOT / 'baseline_source.json').read_text())
deps = json.loads((ROOT / 'validation_dependency_source.json').read_text())
inactive = json.loads((ROOT / 'inactive_locale_source.json').read_text())
metadata = {f['filename']: {k:v for k,v in f.items() if k != 'body'} for f in source['files'] + deps['files'] + inactive['files']}
metadata['assets/product-desktop-ux-20260513-ruler-sync.js'] = next(f for f in json.loads((ROOT/'baseline_identity.json').read_text())['files'] if f['filename'].startswith('assets/'))
manifest, patch = [], []
for path in sorted(BASE.rglob('*')):
    if not path.is_file(): continue
    filename = str(path.relative_to(BASE))
    before, after = path.read_bytes(), (THEME / filename).read_bytes()
    assert hashlib.md5(before).hexdigest() == metadata[filename]['checksumMd5'], filename
    assert len(before) == int(metadata[filename]['size']), filename
    changed = before != after
    manifest.append({'filename':filename,'baseline_md5':hashlib.md5(before).hexdigest(),'baseline_sha256':hashlib.sha256(before).hexdigest(),'candidate_sha256':hashlib.sha256(after).hexdigest(),'baseline_bytes':len(before),'candidate_bytes':len(after),'changed':changed})
    if changed: patch.extend(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True), fromfile='a/'+filename, tofile='b/'+filename))
changed = [f['filename'] for f in manifest if f['changed']]
assert len(changed) == 40
assert len(list(BASE.rglob('*'))) == len(list(THEME.rglob('*')))
(ROOT / 'file_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT / 'candidate.patch').write_text(''.join(patch))
(ROOT / 'changed_files.txt').write_text('\n'.join(changed)+'\n')
def issues(filename):
    rows, target = [], ''
    for line in (ROOT / filename).read_text().splitlines():
        if line.startswith('**Details:** '): target = line.removeprefix('**Details:** ').rstrip(':')
        if re.match(r'^(ERROR|WARNING|INFO) \[',line): rows.append((target,re.sub(r'\[line \d+, col \d+\]','[location]',line)))
    return Counter(rows)
b, c = issues('theme_check_baseline.txt'), issues('theme_check_candidate.txt')
comparison={'baseline_issues':sum(b.values()),'candidate_issues':sum(c.values()),'introduced':[{'file':f,'message':m,'count':n} for (f,m),n in (c-b).items()],'resolved':[{'file':f,'message':m,'count':n} for (f,m),n in (b-c).items()],'checked_files':40,'baseline_context_files':len(manifest)}
assert 'Overall Status:** ✅ VALID' in (ROOT/'theme_check_candidate.txt').read_text()
assert 'Overall Status:** ✅ VALID' in (ROOT/'theme_check_baseline.txt').read_text()
assert 'Overall Status:** ✅ VALID' in (ROOT/'theme_check_revision3_asset.txt').read_text()
assert comparison['candidate_issues']==0
(ROOT / 'theme_check_comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
tests=(ROOT/'regression_results.txt').read_text();assert 'fail 0' in tests and 'Error:' not in tests
summary={'status':'LOCAL_CANDIDATE_VERIFIED_NOT_UPLOADED','revision':3,'theme_id':'gid://shopify/OnlineStoreTheme/133290917985','role_at_capture':'MAIN','changed_file_count':len(changed),'baseline_context_files':len(manifest),'theme_check':'40 files covered: 39 unchanged prior passes plus revised JS pass; zero diagnostics','dom_regressions':'18/18 PASS; synthetic DOM only','published_locales':21,'inactive_locale_parity_only':14,'external_writes':0,'draft_required':True,'publish_authorization':'ROOT_OWNED_NOT_GRANTED_BY_THIS_ARTIFACT','rollback':'Exact original bytes in baseline/; verify target before applying only changed_files.txt','patch_sha256':hashlib.sha256((ROOT/'candidate.patch').read_bytes()).hexdigest()}
(ROOT/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
