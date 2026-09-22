import collections
import hashlib
import json
import pathlib
import re
import subprocess

ROOT=pathlib.Path(__file__).resolve().parent

def statement(line):return re.sub(r'^\{%-?\s*|\s*-?%\}$','',line.strip()).strip()

def non_danish(source):
    source=re.sub(r"{% if request\.locale\.iso_code == 'da' %}[^\n]*?{% else %}([^\n]*?){% endif %}",lambda m:m.group(1),source)
    lines=source.splitlines();out=[];i=0
    while i<len(lines):
        token=statement(lines[i])
        if token=="if request.locale.iso_code == 'da'":
            depth=1;i+=1
            while i<len(lines):
                nested=statement(lines[i])
                if nested.startswith('if '):depth+=1
                elif nested=='endif':depth-=1
                if depth==0:break
                i+=1
            assert depth==0;i+=1;continue
        out.append(lines[i]);i+=1
    return '\n'.join(out)

manifest=json.loads((ROOT/'MANIFEST.json').read_text())
checks={}
for record in manifest['files']:
    name=record['filename'];old=(ROOT/'before'/name).read_bytes();new=(ROOT/'theme'/name).read_bytes()
    assert hashlib.md5(old).hexdigest()==record['sourceMd5']
    assert hashlib.md5(new).hexdigest()==record['candidateMd5']
    assert hashlib.sha256(new).hexdigest()==record['candidateSha256']
    if name.endswith('.liquid'):
        assert non_danish(old.decode())==non_danish(new.decode()),name
        assert re.findall(r'href="(.*?)"',old.decode())==re.findall(r'href="(.*?)"',new.decode())
checks['sourceHashesAndNonDanishLiquidProjection']='PASS'

def locale(which):
    s=(ROOT/which/'locales/da.json').read_text();return json.loads(s[s.index('{'):])
old=locale('before');new=locale('theme')
for key in ['product_count_simple','product_count']:
    assert new['products']['facets'][key].pop('zero')==old['products']['facets'][key]['other']
assert old==new
checks['localeExistingValuesAndPlaceholdersUnchanged']=True
checks['addedZeroKeysUseExistingOtherValues']=True
checks['zeroRenderingStatus']='EXPECTED_UNTIL_PARENT_PREVIEW'
layout=(ROOT/'theme/layout/theme.liquid').read_text();before=(ROOT/'before/layout/theme.liquid').read_text()
for marker in ['{%- if current_tags %}', '{%- if current_page != 1 %}']:
    assert next(line for line in before.splitlines() if marker in line)==next(line for line in layout.splitlines() if marker in line)
checks['tagAndPaginationSuffixBytesUnchanged']=True
checks['newsDescriptionBehavior']='Untagged Danish news index gets Danish generic description. Existing tagged nonblank page_description preserved. Existing blank-description fallback translated for Danish.'

def offenses(which):
    records=json.loads((ROOT/f'theme_check_{which}.json').read_text())
    return collections.Counter((str(pathlib.Path(row['path']).relative_to(ROOT/which)),x['check'],x['message'],x['severity']) for row in records for x in row['offenses'])
baseline=offenses('before');candidate=offenses('theme');assert not candidate-baseline
checks['themeCheck']={'baselineOffenses':sum(baseline.values()),'candidateOffenses':sum(candidate.values()),'newOffenses':sum((candidate-baseline).values()),'syntaxOffenses':sum(n for row,n in candidate.items() if 'Syntax' in row[1]),'dependencyIncompleteSnapshots':True}
whitespace=subprocess.run(['git','diff','--no-index','--check',str(ROOT/'before'),str(ROOT/'theme')],capture_output=True,text=True)
assert whitespace.returncode in (0,1) and not whitespace.stdout and not whitespace.stderr
checks['whitespace']={'exitCode':whitespace.returncode,'diagnostics':'','result':'PASS'}
combined=json.loads((ROOT/'COMBINED_12_FILE_MANIFEST.json').read_text())
assert len(combined['files'])==12
for row in combined['files']:
    assert hashlib.md5(pathlib.Path(row['finalSourcePath']).read_bytes()).hexdigest()==row['candidateMd5']
checks['combined12FinalSourceHashesVerified']=True
checks['status']='PASS_NARROW_CHECKS_RENDER_NOT_RUN'
(ROOT/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
