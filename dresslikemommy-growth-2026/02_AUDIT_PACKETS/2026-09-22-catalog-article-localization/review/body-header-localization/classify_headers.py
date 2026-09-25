import json,pathlib,re,html,hashlib,collections
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1];I=P/'review/body-structure-audit/effective_body_inventory.json'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();filesha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_text()); rows=J(I)['rows']
header=re.compile(r'<th(?:\s[^>]*)?>(.*?)</th\s*>',re.S|re.I)
plain=lambda s:' '.join(html.unescape(re.sub('<[^>]*>',' ',s)).split())
english=re.compile(r'\b(?:Size|Height|Weight|Bust|Chest|Waist|Hips?|Length|Shoulder|Sleeve|Age|Recommended|Pants|Skirt|Dress|Tops?|Shorts|Inseam|Outseam|Category|Measurement|Head|Circumference|Child|Children|Baby|Mother|Father|Girl|Boy|Women|Men|Adults?)\b',re.I)
expanded=re.compile(r'\b(?:Pant|Short|Underbust|Leg Opening)\b|Pantlængde|Pantlängd',re.I)
# Manually classified language terms shared with English. These exact phrases are valid in the observed locale.
# Bare English measurement/role labels are otherwise defects; international unit abbreviations are never flagged.
short_native={'da','de','es','fr','it','nl','no','pt-BR','sv'}
top_native={'cs','da','de','es','fr','it','nl','pl','pt-BR','ro'}
def classify(loc,t):
 if loc=='fr' and t=='Age':return 'LOCAL_ORTHOGRAPHY_DEFECT','French âge needs its circumflex; local cognate rather than a foreign measurement label.'
 if loc=='ro' and re.search(r'\bbust\b',t,re.I) and not re.search(r'\b(?:Hip|Weight|Waist|Age|Shoulder|Sleeve|Height|Length|Recommended|Pants|Size|Chest)\b',t,re.I):return 'KEEP_NATIVE_TERM','Romanian bust is a native noun for the bust/chest. Other words and labels are already Romanian.'
 toks=[m.group().lower() for m in english.finditer(t)]
 if toks and all(x in {'top','tops'} for x in toks) and loc in top_native:return 'KEEP_ESTABLISHED_GARMENT_LOAN','Top is an established garment noun in this locale; the surrounding measurement label is localized.'
 if toks and all(x=='shorts' for x in toks) and loc in short_native:return 'KEEP_ESTABLISHED_GARMENT_LOAN','Shorts is an established garment noun in this locale; the surrounding chart label is localized.'
 if not toks and re.search(r'\bshort\b',t,re.I) and loc in {'de','es','fr','nl','pt-BR'} and not re.search(r'\bpant\b|\bor\b',t,re.I):return 'KEEP_ESTABLISHED_GARMENT_LOAN','Short is used as an established garment loan in this locale; no English connective or Pant label remains.'
 if '|' in t and loc=='ko':return 'ENGLISH_BILINGUAL_DUPLICATE','English label is unnecessarily retained alongside the complete Korean label in the same header cell.'
 return 'ENGLISH_LABEL_DEFECT','English measurement, garment or role wording remains in a localized chart header; preserve the numeric data and unit symbols.'
# Existing tag-only proposals are tracked without overlaying their mutable author files.
tagfile=P/'review/body-structure-audit/tag_candidates_v1.json';tagdata=J(tagfile);tagrows=tagdata.get('rows',tagdata) if isinstance(tagdata,dict) else tagdata
tagkeys={(r['resourceId'],r['locale']) for r in tagrows}
occ=[];groups=collections.defaultdict(list);rawcache={};overcache={};checks=[]
for r in rows:
 v=r['expectedEffectiveBeforeValue']; assert sha(v)==r['expectedEffectiveBeforeValueSHA256']
 rp=P/r['rawFile']
 if rp not in rawcache:
  assert filesha(rp)==r['rawFileSHA256'];rawcache[rp]={n['resourceId']:n for n in J(rp)['data']['translatableResourcesByIds']['nodes']}
 raw=rawcache[rp][r['resourceId']];source=next(f for f in raw['translatableContent'] if f['key']=='body_html')
 assert source['value']==r['source'] and source['digest']==r['sourceDigest'] and sha(source['value'])==r['sourceSHA256']
 before=next((q for q in raw.get('tr_'+r['locale'].replace('-','_'),[]) if q['key']=='body_html' and q.get('market') is None),None)
 assert before==r['rawBefore']
 if r['overlayApplied']:
  op=P/r['overlayFile']
  if op not in overcache:assert filesha(op)==r['overlayFileSHA256'];overcache[op]={(q['resourceId'],q['locale']):q for q in J(op)}
  assert overcache[op][(r['resourceId'],r['locale'])]['value']==v
  effective_outdated=False;outdated_basis='VERIFIED_RELEASED_OVERLAY_REQUIRES_FRESH_READ'
 else:
  assert before['value']==v;effective_outdated=before['outdated'];outdated_basis='EXACT_RAW_GLOBAL_BEFORE'
 actual=[];sourceHeaders=[plain(m[1]) for m in header.finditer(r['source'])]
 for celli,m in enumerate(header.finditer(v)):
  t=plain(m[1]);detector=bool(english.search(t));extra=bool(expanded.search(t))
  if detector:actual.append(t)
  if not(detector or extra):continue
  c,why=classify(r['locale'],t)
  # Explicit th tokens are preserved even where the ancestor table tags were translated; a tag-only repair owns that structural issue.
  o={'resourceId':r['resourceId'],'productIndex':r['productIndex'],'locale':r['locale'],'key':'body_html','headerIndex':celli,'cellStart':m.start(),'cellEnd':m.end(),'cellHTML':m[0],'visibleHeader':t,'classification':c,'reason':why,'originalDetectorMatch':detector,'expandedDetectorOnly':not detector,'rawOutdated':before.get('outdated') if before else None,'effectiveOutdated':effective_outdated,'effectiveOutdatedBasis':outdated_basis,'tagRepairOverlap':(r['resourceId'],r['locale']) in tagkeys,'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'beforeValueSHA256':sha(v),'rawFile':r['rawFile'],'rawFileSHA256':r['rawFileSHA256'],'overlayFile':r['overlayFile'],'overlayFileSHA256':r['overlayFileSHA256'],'sourceExactHeaderPresent':t in sourceHeaders}
  occ.append(o);groups[(r['locale'],t,c)].append(o)
 assert actual==r['englishFallbackHeaderCandidates']
 checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'rawSourceBeforeAndOverlayBindingsPass':True,'originalHeaderDetectorExactPass':True})
classified=[]
for (l,t,c),uses in sorted(groups.items()):
 classified.append({'locale':l,'visibleHeader':t,'classification':c,'reason':uses[0]['reason'],'occurrences':len(uses),'distinctBodies':len({u['resourceId'] for u in uses}),'effectiveOutdatedFalse':sum(u['effectiveOutdated'] is False for u in uses),'effectiveOutdatedTrue':sum(u['effectiveOutdated'] is True for u in uses),'rawOutdatedTrue':sum(u['rawOutdated'] is True for u in uses),'tagOverlapOccurrences':sum(u['tagRepairOverlap'] for u in uses),'uses':[{'resourceId':u['resourceId'],'productIndex':u['productIndex'],'headerIndex':u['headerIndex']} for u in uses]})
def counts(os):
 bodies={(o['resourceId'],o['locale']) for o in os}
 return {'headerOccurrences':len(os),'bodyTuples':len(bodies),'uniqueVisiblePhrases':len({o['visibleHeader'] for o in os}),'uniqueLocalePhrases':len({(o['locale'],o['visibleHeader']) for o in os}),'effectiveOutdatedFalseBodyTuples':len({(o['resourceId'],o['locale']) for o in os if o['effectiveOutdated'] is False}),'effectiveOutdatedTrueBodyTuples':len({(o['resourceId'],o['locale']) for o in os if o['effectiveOutdated'] is True}),'rawOutdatedTrueBodyTuples':len({(o['resourceId'],o['locale']) for o in os if o['rawOutdated'] is True}),'tagRepairOverlapBodyTuples':len({(o['resourceId'],o['locale']) for o in os if o['tagRepairOverlap']})}
summary={'scope':'LOCAL_CLASSIFICATION_ONLY_NO_REPAIR_CANDIDATES','inputFile':str(I.relative_to(P)),'inputFileSHA256':filesha(I),'all4760BindingsPass':True,'originalDetector':counts([o for o in occ if o['originalDetectorMatch']]),'expandedDetectorOnly':counts([o for o in occ if o['expandedDetectorOnly']]),'allClassified':counts(occ),'byClassification':{c:counts([o for o in occ if o['classification']==c]) for c in sorted({o['classification'] for o in occ})},'perLocale':{},'preservation':'Only actual closed <th> cells considered. No td measurements, units, HTML, text, translations or external values changed. Final tag repair overlay must be applied before header mutation where overlapping. No status reset is authorized for outdated source-body translations.'}
for l in sorted({o['locale'] for o in occ}):
 los=[o for o in occ if o['locale']==l]
 summary['perLocale'][l]={'all':counts(los),'actualEnglish':counts([o for o in los if o['classification'].startswith('ENGLISH')]),'localOrthography':counts([o for o in los if o['classification']=='LOCAL_ORTHOGRAPHY_DEFECT']),'keepNativeOrLoan':counts([o for o in los if o['classification'].startswith('KEEP')])}
for n,d in [('classification_summary.json',summary),('unique_locale_phrases.json',{'rows':classified}),('header_occurrence_ledger.json',{'rows':occ}),('binding_checks.json',{'rows':checks,'allPass':True,'count':len(checks)})]:(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['originalDetector','expandedDetectorOnly','allClassified','byClassification']},indent=2))
print('PER LOCALE')
for l,d in summary['perLocale'].items():print(l,'EN',d['actualEnglish']['bodyTuples'],d['actualEnglish']['headerOccurrences'],'keep',d['keepNativeOrLoan']['headerOccurrences'],'effectiveOutdated',d['actualEnglish']['effectiveOutdatedTrueBodyTuples'])
