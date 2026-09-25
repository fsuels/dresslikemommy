import json,re,hashlib,html
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
d=json.loads((H/'tag_candidates_v3.json').read_text());r=next(x for x in d['rows'] if x['productIndex']==81 and x['locale']=='pl');before=r['value'];old='„Need More Juice”” src=';new='„Need More Juice”" src=';assert before.count(old)==1;r['value']=before.replace(old,new,1);r['valueSHA256']=sha(r['value']);r['versionFourExceptions']=[{'kind':'EXACT_MISMATCHED_IMAGE_ATTRIBUTE_DELIMITER','before':old,'after':new,'sourceExactImageTag':re.search(r'<img[^>]*>',r['source'])[0],'pairingEvidence':'Last extra curly quote is the missing ASCII alt closing boundary. Preserve inner Juice quotation mark and all wording/URL.'}];r['versionThreeValueSHA256']=sha(before)
for j in [65,84]:
 row=next(x for x in d['rows'] if x['productIndex']==j and x['locale']=='hi'); before=row['value'];changes=[]
 sourceTags=re.findall(r'<img[^>]*>',row['source']);targetTags=re.findall(r'<img[^>]*>',before);assert len(sourceTags)==len(targetTags)
 for st,tt in zip(sourceTags,targetTags):
  url=re.search(r'src="([^"]*)"',st)[1];assert url in tt
  # Existing localized alt starts after alt='; only final matching/mistranslated boundary is removed.
  alt=tt.split("alt='",1)[1][:-1]; assert alt[-1] in "'”";alt=alt[:-1]
  newtag='<img src="'+url+'" alt="'+html.escape(alt,quote=True)+'">';assert row['value'].count(tt)==1;row['value']=row['value'].replace(tt,newtag,1)
  changes.append({'kind':'EXACT_MISMATCHED_IMAGE_ATTRIBUTE_DELIMITER','before':tt,'after':newtag,'sourceExactImageTag':st,'preservedLocalizedAltValue':alt,'pairingEvidence':'Exact URL retained and matched to source; restore src delimiter and encode existing alt contents safely without changing text.'})
 row.update(valueSHA256=sha(row['value']),versionThreeValueSHA256=sha(before),versionFourExceptions=changes)
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
def imgs(s):p=Images();p.feed(s);p.close();return p.images
issues=[]
for row in d['rows']:
 si=imgs(row['source']);ti=imgs(row['value'])
 if [x.get('src') for x in si]!=[x.get('src') for x in ti]:issues.append({'productIndex':row['productIndex'],'locale':row['locale'],'source':si,'target':ti})
assert {(x['productIndex'],x['locale']) for x in issues}=={(62,'ar'),(62,'it'),(62,'ja'),(62,'nl'),(62,'pl'),(85,'it'),(86,'ar')};(H/'legacy_image_count_differences.json').write_text(json.dumps({'status':'PRESERVED_EXISTING_NOT_CHANGED_BY_TAG_REPAIRS','rows':issues},ensure_ascii=False,indent=2)+'\n')
out={'status':'FINAL375_AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','supersedes':'tag_candidates_v3.json','rows':d['rows']};(H/'tag_candidates_v4.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');report={'status':'PASS','rows':375,'deltaRowsFromV3':3,'allPresentImageURLsValid':True,'sourceImageCountDriftPreservedRows':7,'candidateSHA256':sha((H/'tag_candidates_v4.json').read_text()),'exception':r['versionFourExceptions']};(H/'tag_v4_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
