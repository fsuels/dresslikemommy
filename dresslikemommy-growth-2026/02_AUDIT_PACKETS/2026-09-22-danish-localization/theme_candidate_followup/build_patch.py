import difflib
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
PACKET = ROOT.parent
BEFORE, AFTER = ROOT/'before', ROOT/'theme'

def payload(name):
    value=json.loads((PACKET/name).read_text())
    return value.get('structuredContent',value)['data']

phase1=json.loads((PACKET/'theme_candidate/MANIFEST.json').read_text())
readback=payload('theme_manifest_after.json')['theme']
assert readback['id']=='gid://shopify/OnlineStoreTheme/137888792673'
assert readback['role']=='UNPUBLISHED'
remote_md5={node['filename']:node['checksumMd5'] for node in readback['files']['nodes']}
sources={}
for name in ['layout/theme.liquid','locales/da.json']:
    contents=(PACKET/'theme_candidate/theme'/name).read_bytes()
    assert hashlib.md5(contents).hexdigest()==remote_md5[name]
    sources[name]=contents
article=payload('theme_article_card_before.json')['theme']['files']['nodes'][0]
assert article['filename']=='snippets/article-card.liquid'
sources[article['filename']]=article['body']['content'].encode()
assert hashlib.md5(sources[article['filename']]).hexdigest()==article['checksumMd5']==remote_md5[article['filename']]
english=payload('theme_english_locale_before.json')['theme']['files']['nodes'][0]
assert english['filename']=='locales/en.default.json'
assert hashlib.md5(english['body']['content'].encode()).hexdigest()==english['checksumMd5']==remote_md5[english['filename']]
english_raw=english['body']['content']
english_locale=json.loads(english_raw[english_raw.index('{'):])
assert 'zero' not in english_locale['products']['facets']['product_count_simple']
assert 'zero' not in english_locale['products']['facets']['product_count']

for name,contents in sources.items():
    for folder in [BEFORE,AFTER]:
        target=folder/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(contents)

def patch(name,old,new):
    path=AFTER/name;s=path.read_text();assert s.count(old)==1,(name,old)
    path.write_text(s.replace(old,new))

description='Guider til matchende tøj, stylingtips og købsråd til mor og barn, far og barn og hele familien.'
patch('layout/theme.liquid',
      "      assign resolved_page_title = 'Style Journal'",
      "      assign resolved_page_title = 'Style Journal'\n      if request.locale.iso_code == 'da'\n        assign resolved_page_title = 'Stiljournal'\n        if current_tags == blank\n          assign resolved_page_description = '"+description+"'\n        endif\n      endif")
patch('layout/theme.liquid',
      "        assign resolved_page_description = 'Outfit guides, styling tips, and shopping advice for mommy and me, daddy and me, and family matching looks.'",
      "        assign resolved_page_description = 'Outfit guides, styling tips, and shopping advice for mommy and me, daddy and me, and family matching looks.'\n        if request.locale.iso_code == 'da'\n          assign resolved_page_description = '"+description+"'\n        endif")
for english_text,danish_text in [('min read','min. læsetid'),('Read article','Læs artiklen')]:
    patch('snippets/article-card.liquid',english_text,"{% if request.locale.iso_code == 'da' %}"+danish_text+'{% else %}'+english_text+'{% endif %}')

locale=AFTER/'locales/da.json';raw=locale.read_text();idx=raw.index('{');header=raw[:idx]
d=json.loads(raw[idx:]);assert json.dumps(d,ensure_ascii=False,indent=2)+'\n'==raw[idx:]
for key in ['product_count_simple','product_count']:
    target=d['products']['facets'][key];assert 'zero' not in target
    target['zero']=target['other']
locale.write_text(header+json.dumps(d,ensure_ascii=False,indent=2)+'\n')

manifest=[];diff=[]
for name in sorted(sources):
    old=sources[name];new=(AFTER/name).read_bytes()
    manifest.append({'filename':name,'sourceMd5':hashlib.md5(old).hexdigest(),'sourceSha256':hashlib.sha256(old).hexdigest(),'candidateMd5':hashlib.md5(new).hexdigest(),'candidateSha256':hashlib.sha256(new).hexdigest()})
    diff.extend(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='before/'+name,tofile='theme/'+name))
(ROOT/'MANIFEST.json').write_text(json.dumps({'themeId':'137888792673','phase':2,'files':manifest,'existingDanishValuesChanged':0,'danishZeroKeysAdded':['products.facets.product_count_simple.zero','products.facets.product_count.zero']},indent=2)+'\n')
(ROOT/'changes.diff').write_text(''.join(diff))
combined={x['filename']:dict(x,finalSourcePath=str(PACKET/'theme_candidate/theme'/x['filename'])) for x in phase1['files']}
for row in manifest:
    name=row['filename']
    if name in combined:
        combined[name]['phase1Md5']=row['sourceMd5']
        combined[name]['candidateMd5']=row['candidateMd5']
        combined[name]['candidateSha256']=row['candidateSha256']
        combined[name]['finalSourcePath']=str(AFTER/name)
    else:combined[name]=dict(row,finalSourcePath=str(AFTER/name))
assert len(combined)==12
(ROOT/'COMBINED_12_FILE_MANIFEST.json').write_text(json.dumps({'themeId':'137888792673','status':'LOCAL_COMPOSITE_NOT_FRESH_REMOTE_BINDING','files':list(combined.values())},indent=2)+'\n')
print('Prepared 3 follow-up files; 12 cumulative changed files; 2 zero keys added and no existing locale values changed.')
