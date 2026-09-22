import difflib
import hashlib
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parent
PACKET=ROOT.parent

def payload(name):
    value=json.loads((PACKET/name).read_text())
    return value.get('structuredContent',value)['data']

node=payload('theme_daddy_filter_before.json')['theme']['files']['nodes'][0]
assert node['filename']=='assets/daddy-me-collection-filter.js'
javascript=node['body']['content'].encode()
assert hashlib.md5(javascript).hexdigest()==node['checksumMd5']=='45a6e48cda28fc815c3d1b54a0a82a4a'
phase2_locale=(PACKET/'theme_candidate_followup/theme/locales/da.json').read_bytes()
phase2_receipt=payload('theme_followup_execution.json')['themeFilesUpsert']
assert not phase2_receipt['userErrors']
registered={row['filename']:row['checksumMd5'] for row in phase2_receipt['upsertedThemeFiles']}
assert hashlib.md5(phase2_locale).hexdigest()==registered['locales/da.json']=='3ad0181cb1165661d4841d350b9dbf30'
phase1_locale=(PACKET/'theme_candidate/theme/locales/da.json').read_bytes()
assert hashlib.md5(phase1_locale).hexdigest()=='90962b170b6ae87a2bf69a1ac0a0060f'

before={'assets/daddy-me-collection-filter.js':javascript,'locales/da.json':phase2_locale}
after=dict(before)
s=javascript.decode()
def replace(old,new):
    global s
    assert s.count(old)==1,old
    s=s.replace(old,new)

replace('  const TEES_FILTER = "tees";\n', '''  const TEES_FILTER = "tees";
  const IS_DANISH = (document.documentElement.lang || "")
    .toLowerCase()
    .split("-")[0] === "da";
''')
replace('''    const hasShirtText =
      normalized.includes(" shirt ") || normalized.includes(" shirts ");''', '''    const hasShirtText =
      normalized.includes(" shirt ") || normalized.includes(" shirts ") ||
      (IS_DANISH && /(?:^|[^a-zæøå])[a-zæøå]*skjorte(?:r|sæt)?(?=$|[^a-zæøå])/i.test(title || ""));''')
replace('''      element.textContent = `${visibleCount} product${visibleCount === 1 ? "" : "s"}`;''', '''      element.textContent = IS_DANISH
        ? `${visibleCount} produkt${visibleCount === 1 ? "" : "er"}`
        : `${visibleCount} product${visibleCount === 1 ? "" : "s"}`;''')
after['assets/daddy-me-collection-filter.js']=s.encode()
after['locales/da.json']=phase1_locale

records=[];diff=[]
for name in sorted(before):
    for folder,contents in [('before',before[name]),('theme',after[name])]:
        path=ROOT/folder/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(contents)
    old,new=before[name],after[name]
    records.append({'filename':name,'sourceMd5':hashlib.md5(old).hexdigest(),'sourceSha256':hashlib.sha256(old).hexdigest(),'candidateMd5':hashlib.md5(new).hexdigest(),'candidateSha256':hashlib.sha256(new).hexdigest()})
    diff.extend(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='before/'+name,tofile='theme/'+name))
(ROOT/'MANIFEST.json').write_text(json.dumps({'themeId':'137888792673','phase':3,'files':records,'speculativeZeroKeysRemoved':True},indent=2)+'\n')
(ROOT/'changes.diff').write_text(''.join(diff))
combined=json.loads((PACKET/'theme_candidate_followup/COMBINED_12_FILE_MANIFEST.json').read_text())
by_name={row['filename']:row for row in combined['files']}
for row in records:
    name=row['filename']
    if name in by_name:
        by_name[name]['phase2Md5']=row['sourceMd5']
        by_name[name]['candidateMd5']=row['candidateMd5']
        by_name[name]['candidateSha256']=row['candidateSha256']
        by_name[name]['finalSourcePath']=str(ROOT/'theme'/name)
    else:by_name[name]=dict(row,finalSourcePath=str(ROOT/'theme'/name))
assert len(by_name)==13
(ROOT/'COMBINED_13_FILE_MANIFEST.json').write_text(json.dumps({'themeId':'137888792673','status':'LOCAL_COMPOSITE_NOT_FRESH_REMOTE_BINDING','files':list(by_name.values())},indent=2)+'\n')
print('Prepared 2 phase 3 files, including exact restoration of phase 1 Danish locale; 13 cumulative files.')
