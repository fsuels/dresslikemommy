import json, hashlib, re, html
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[2]
CANDIDATE=BASE/'root-bodies/he-pl/remaining-review/body_candidates.json'
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def sha_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
rows=json.loads(CANDIDATE.read_text())['rows']
pairs=json.loads((HERE/'text_pairs.json').read_text())
fixes={
15:('أربطة الشعر المتناسقة','فيونكات الشعر المتناسقة','Translate hair bows precisely rather than hair ties.'),
124:('أشرطة الشعر المتطابقة','فيونكات الشعر المتطابقة','Translate hair bows precisely rather than ribbons.'),
225:('أربطة شعر، قبعات','فيونكات شعر، قبعات','Translate hair bows precisely rather than hair ties.'),
245:('أربطة الشعر المتطابقة','فيونكات الشعر المتطابقة','Translate hair bows precisely rather than hair ties.'),
22:('وغسلها من الداخل','وغسلها مقلوبة على الوجه الداخلي','Specify turning clothes inside out, not merely washing the inside.'),
67:('وتجفيفها على حرارة منخفضة','وتجفيفها في المجفف على حرارة منخفضة','Retain tumble drying rather than unspecified low-heat drying.'),
254:('هذا القميص المتناسق على شكل قطعة لغز القلب','هذا التيشيرت المتناسق بتصميم قطعة أحجية على شكل قلب','Describe the heart-puzzle-piece design rather than the shape of the T-shirt itself.')}
proposals=[]
for r in pairs:
 if r['id'] not in fixes: continue
 old,new,reason=fixes[r['id']]
 assert r['value'].count(old)==1
 proposals.append(dict(r, oldFragment=old,newFragment=new,correctedValue=r['value'].replace(old,new),oldTextSHA256=sha(r['value']),correctedTextSHA256=sha(r['value'].replace(old,new)),reason=reason))
dump('correction_proposals.json',{'frozenCandidateFileSHA256':'b2aa9176937b6d65963fec39f647553de6ceb4b2692eceec31d3af0091c15669','status':'PROPOSED_TO_AUTHOR_NOT_ORIGINAL_CANDIDATE_PASS','proposals':proposals})
checks=[]
for r in rows:
 rawpath=BASE/r['rawFile']; raw=json.loads(rawpath.read_text())
 rawrow=next(x for x in raw['data']['translatableResourcesByIds']['nodes'] if x['resourceId']==r['resourceId'])
 s=next(x for x in rawrow['translatableContent'] if x['key']==r['key'])
 t=next(x for x in rawrow['translations'] if x['key']==r['key'] and x['locale']==r['locale'] and not x.get('market'))
 bound=(sha_file(rawpath)==r['rawFileSHA256'] and s['value']==r['source']==r['sourceValue'] and s['digest']==r['sourceDigest'] and t['value']==r['before']['value'] and sha(r['source'])==r['sourceSHA256'] and sha(r['before']['value'])==r['expectedBeforeValueSHA256'] and sha(r['value'])==r['valueSHA256'])
 stags=re.findall(r'<[^>]*>',r['source']); vtags=re.findall(r'<[^>]*>',r['value'])
 norm=lambda tags:[re.sub(r'\balt="[^"]*"','alt="LOCALIZED"',x) for x in tags]
 st=[html.unescape(x).strip() for x in re.split(r'<[^>]*>',r['source']) if x.strip()]
 vt=[html.unescape(x).strip() for x in re.split(r'<[^>]*>',r['value']) if x.strip()]
 snum=re.findall(r'\d+(?:[.,]\d+)*',' '.join(st)); vnum=re.findall(r'\d+(?:[.,]\d+)*',' '.join(vt))
 href=lambda v: re.findall(r'\bhref="([^"]*)"',v)
 image=lambda tags:[re.sub(r'\balt="[^"]*"','alt="LOCALIZED"',x) for x in tags if x.startswith('<img')]
 checks.append({'ledgerId':r['ledgerId'],'locale':r['locale'],'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'expectedBeforeValueSHA256':r['expectedBeforeValueSHA256'],'valueSHA256':r['valueSHA256'],'rawSourceDigestBeforeValueSHA':bound,'nonAltRawTagsIdentical':norm(stags)==norm(vtags),'imageAttributesExceptAltIdentical':image(stags)==image(vtags),'hrefSequenceExact':href(r['source'])==href(r['value']),'visibleNodeCountExact':len(st)==len(vt),'visibleNumericTokensExact':snum==vnum,'sourceNumericTokens':snum,'candidateNumericTokens':vnum})
 assert bound and norm(stags)==norm(vtags) and len(st)==len(vt) and snum==vnum, r['ledgerId']
dump('additional_checks.json',{'candidateFileSHA256':sha_file(CANDIDATE),'rows':checks,'rowsChecked':len(checks),'uniqueRowKeys':len({(r['resourceId'],r['locale'],r['key']) for r in rows})})
affected=sorted({u['ledgerId'] for p in proposals for u in p['uses']},key=int)
print(json.dumps({'checked':len(rows),'proposals':len(proposals),'nodeOccurrences':sum(len(p['uses']) for p in proposals),'affectedRows':affected,'unaffectedRows':len(rows)-len(affected)},indent=2))
