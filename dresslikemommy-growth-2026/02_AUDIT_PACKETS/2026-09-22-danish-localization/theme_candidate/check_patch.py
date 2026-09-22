import collections
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
manifest = json.loads((ROOT/'MANIFEST.json').read_text())
results = {}

def flatten(obj, prefix=''):
    answer = {}
    for key, value in obj.items():
        full = f'{prefix}.{key}' if prefix else key
        if isinstance(value, dict): answer.update(flatten(value, full))
        else: answer[full] = value
    return answer

def load_locale(path):
    raw = path.read_text()
    return json.loads(raw[raw.index('{'):])

def statement(line):
    return re.sub(r'^\{%-?\s*|\s*-?%\}$', '', line.strip()).strip()

def non_danish_projection(source):
    source = re.sub(r"{% if request\.locale\.iso_code == 'da' %}[^\n]*?{% else %}([^\n]*?){% endif %}", lambda match: match.group(1), source)
    lines = source.splitlines()
    projected=[]
    i=0
    while i<len(lines):
        token=statement(lines[i])
        if token == "when 'da'":
            # Existing homepage helper: exclude this one locale branch in both snapshots.
            i+=1
            while i<len(lines) and lines[i] != '    else':i+=1
            continue
        if token == "if request.locale.iso_code == 'da'":
            depth=1
            alternative=False
            i+=1
            while i<len(lines):
                nested=statement(lines[i])
                if nested.startswith('if '):depth+=1
                elif nested=='endif':
                    depth-=1
                    if depth==0:break
                elif nested=='else' and depth==1:
                    alternative=True;i+=1;continue
                if alternative:projected.append(lines[i])
                i+=1
            assert depth==0
            i+=1
            continue
        if token == "elsif request.locale.iso_code == 'da'":
            i+=1
            while i<len(lines) and not re.match(r'^(elsif |else$|endif$)',statement(lines[i])):i+=1
            continue
        projected.append(lines[i]);i+=1
    return '\n'.join(line.strip() for line in projected if line.strip())

source_nodes={}
for name in ['theme_137888792673_before.json','theme_extra_before.json','theme_navigation_before.json','theme_blog_before.json']:
    payload=json.loads((ROOT.parent/name).read_text())
    assert payload['data']['theme']['id']=='gid://shopify/OnlineStoreTheme/137888792673'
    for node in payload['data']['theme']['files']['nodes']:source_nodes[node['filename']]=node

liquid_results=[]
for record in manifest['files']:
    name=record['filename']
    before=(ROOT/'before'/name).read_bytes()
    after=(ROOT/'theme'/name).read_bytes()
    assert hashlib.md5(before).hexdigest()==source_nodes[name]['checksumMd5']==record['sourceMd5']
    assert before.decode()==source_nodes[name]['body']['content']
    assert hashlib.md5(after).hexdigest()==record['candidateMd5']
    assert hashlib.sha256(after).hexdigest()==record['candidateSha256']
    if not name.endswith('.liquid'):continue
    old,new=before.decode(),after.decode()
    equal=non_danish_projection(old)==non_danish_projection(new)
    assert equal, name
    old_destinations=re.findall(r"['\"](/(?:collections|products|pages|blogs)/[^'\"]+)['\"]",old)
    new_destinations=re.findall(r"['\"](/(?:collections|products|pages|blogs)/[^'\"]+)['\"]",new)
    assert old_destinations==new_destinations,name
    schemas=re.findall(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',new,re.S)
    assert schemas==re.findall(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',old,re.S)
    for schema in schemas:json.loads(schema)
    liquid_results.append({'filename':name,'nonDanishSourceProjectionUnchanged':equal,'existingDestinationLiteralsUnchanged':True,'sectionSchemaUnchangedAndJsonValid':True})
results['sourceBindingsAndCandidateHashesVerified']=True
results['liquidScopeChecks']=liquid_results
whitespace=subprocess.run(['git','diff','--no-index','--check',str(ROOT/'before'),str(ROOT/'theme')],capture_output=True,text=True)
assert whitespace.returncode in (0,1) and not whitespace.stdout and not whitespace.stderr
results['diffWhitespaceCheck']={'command':'git diff --no-index --check before theme','exitCode':whitespace.returncode,'diagnostics':'','result':'PASS_NO_WHITESPACE_ERRORS'}

before=flatten(load_locale(ROOT/'before/locales/da.json'))
after=flatten(load_locale(ROOT/'theme/locales/da.json'))
assert before.keys()==after.keys()
changed={key for key in before if before[key]!=after[key]}
planned=json.loads((ROOT/'locale_changes.json').read_text())
assert changed==planned.keys()
for key in before:
    assert sorted(re.findall(r'{{.*?}}',str(before[key])))==sorted(re.findall(r'{{.*?}}',str(after[key]))),key
    if key in changed:
        assert re.findall(r'href="([^"]+)"',str(before[key]))==re.findall(r'href="([^"]+)"',str(after[key])),key
results['locale']={'keyCount':len(before),'keysPreserved':True,'changedValues':len(changed),'interpolationTokensPreservedAllKeys':True,'changedHtmlHrefValuesPreserved':True,'existingDanishDressesMetaDescriptionPreserved':before['sections.collection_seo.meta_descriptions.dresses']==after['sections.collection_seo.meta_descriptions.dresses']}

def offenses(folder):
    report=json.loads((ROOT/f'theme_check_{folder}.json').read_text())
    return collections.Counter((str(pathlib.Path(file['path']).relative_to(ROOT/folder)),offense['check'],offense['message'],offense['severity']) for file in report for offense in file['offenses'])

original=offenses('before');candidate=offenses('theme')
added=candidate-original
assert not added,added
results['themeCheck']={'baselineOffenses':sum(original.values()),'candidateOffenses':sum(candidate.values()),'newOffenses':sum(added.values()),'syntaxOffenses':sum(count for row,count in candidate.items() if 'Syntax' in row[1]),'scope':f"{len(manifest['files'])}-file dependency-incomplete snapshots; baseline and candidate compared by file, check, message and severity, ignoring shifted line positions",'countsByCheck':dict(collections.Counter({check:sum(count for row,count in candidate.items() if row[1]==check) for check in {row[1] for row in candidate}}))}
results['status']='PASS_NARROW_SOURCE_CHECKS_RENDER_NOT_RUN'
(ROOT/'CHECKS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
