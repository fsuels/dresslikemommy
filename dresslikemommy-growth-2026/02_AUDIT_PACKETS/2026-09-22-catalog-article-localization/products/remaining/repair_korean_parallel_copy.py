#!/usr/bin/env python3
"""Remove explicitly delimited English duplicates, preserving reviewed Korean branches."""
import collections,hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
base=json.loads((HERE/'body_baseline.json').read_text())['rows']
ids={'7502192214113','7502770045025','7502790656097','7502792622177','7502793179233'}
def ko(s):return bool(re.search('[가-힣]',html.unescape(re.sub('<[^>]*>','',s))))
def clean_pair(inner):
 if inner.count('|')!=1:return inner
 a,b=inner.split('|')
 if ko(a) or not ko(b):return inner
 prefix=re.match(r'^(?:\s*<meta\b[^>]*>)*',a).group()
 return prefix+b
rows=[];checks=[]
for r in base:
 if r['locale']!='ko' or r['resourceId'].split('/')[-1] not in ids:continue
 before=r['before']['value'];after=before
 for tag in ['strong','p','li','th','td']:
  def repl(m):return m[1]+clean_pair(m[2])+m[3]
  after=re.sub(r'(<'+tag+r'\b[^>]*>)(.*?)(</'+tag+r'>)',repl,after,flags=re.S)
 # One paragraph has a Korean sizing heading before the remaining bilingual sentence.
 after=re.sub(r'(<br\s*/?>)([^<]*?(?:<strong\b[^>]*>.*?</strong>[^<]*?)*\|[^<]+)(</p>)',lambda m:m[1]+clean_pair(m[2])+m[3],after,flags=re.S)
 if r['resourceId'].endswith('/7502770045025'):
  # The existing Korean sentence omitted source emphasis around these two roles.
  after=after.replace('남성용과 어린이용 사이즈로 함께 입을 수 있습니다.','<strong data-start="1967" data-end="1976">남성용</strong>과 <strong data-start="1981" data-end="1990">어린이용</strong> 사이즈로 함께 입을 수 있습니다.')
 # Garment context is a shirt, not a coat; preserve the original measurement unit.
 after=after.replace('코트 길이 (cm / in)','상의 길이 (cm / in)')
 assert '|' not in after,(r['resourceId'],'unresolved parallel separator')
 assert ko(after)
 a=ot.Shape(r['source']);b=ot.Shape(after)
 src_num=[[ot.numbers(c['text']) for c in row] for t in a.tables for row in t['rows']]
 dst_num=[[ot.numbers(c['text'],'ko') for c in row] for t in b.tables for row in t['rows']]
 assert src_num==dst_num,(r['resourceId'],'table numbers do not match English source')
 # Keep target URLs and all non-duplicate numeric measurements unchanged.
 assert re.findall(r'(?:src|href)=[\"\']([^\"\']+)',before)==re.findall(r'(?:src|href)=[\"\']([^\"\']+)',after)
 row={**r,'value':after,'marketId':None,'method':'remove_delimited_English_duplicate_preserve_reviewed_Korean_translation','reviewNotes':'Five complete existing Korean descriptions were preceded by English copies separated by a literal pipe in paragraphs, list items and table labels. Korean meaning was manually compared with English source; same numeric size chart retained. Three coat-length labels adjusted to shirt-length context.'}
 rows.append(row);checks.append({'resourceId':r['resourceId'],'removedSeparators':before.count('|'),'remainingSeparators':after.count('|'),'tableNumericCellsMatchSource':True,'urlsUnchanged':True,'sourceStructureCheck':ot.verify_text(r['source'],after,'ko')})
f=HERE/'korean_duplicate_body_candidate.json';f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(HERE/'korean_duplicate_body_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(HERE/'korean_duplicate_body_rollback.json').write_text(json.dumps([{'resourceId':r['resourceId'],'locale':'ko','key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
