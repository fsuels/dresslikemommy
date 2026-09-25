import json,hashlib,pathlib,re,html,copy
P=pathlib.Path(__file__).resolve().parents[2]; O=pathlib.Path(__file__).resolve().parent
H=lambda s:hashlib.sha256(s.encode()).hexdigest()
FH=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_text())
def rows(p):
 d=J(p);return d['rows'] if isinstance(d,dict) else d
rid='gid://shopify/Product/7537372463201'
base=[r for r in rows(P/'review/product-title-completeness/all_4760_effective_titles.json') if r['resourceId']==rid]
files=[P/'review/article-title-independent'/n for n in ['product_a_final304_reviewed.json','product_it79_reviewed.json','product_ja55_reviewed.json','product_ko35_reviewed.json','product_nl113_reviewed.json','product_no123_reviewed.json']]+[O/f'{l}_reviewed.json' for l in ['pl','pt-BR','ro','ru','sv']]
overlay={}
for p in files:
 for r in rows(p):
  if r['resourceId']==rid:
   assert r['locale'] not in overlay
   overlay[r['locale']]=(p,r)
rawpath=P/base[0]['rawFile'];raw=next(n for n in J(rawpath)['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==rid)
source=next(f for f in raw['translatableContent'] if f['key']=='title')
body=next(f for f in raw['translatableContent'] if f['key']=='body_html')
quote='Print: Red Stripe — clean horizontal red and off-white stripes with a tiny red heart patch at the chest pocket for a sweet, photo-ready accent.'
normalized=' '.join(html.unescape(re.sub('<[^>]*>',' ',body['value'])).split())
assert quote in normalized
values={
'ar':'بلوزات عائلية متطابقة بخطوط حمراء – تي شيرت بقلب عند جيب الصدر',
'cs':'Sladěné rodinné topy s červenými pruhy – tričko se srdíčkem u náprsní kapsy',
'da':'Matchende rødstribede toppe til familien – T-shirt med et hjerte ved brystlommen',
'de':'Passende rot gestreifte Familienoberteile – T-Shirt mit einem Herz an der Brusttasche',
'el':'Ασορτί οικογενειακά τοπ με κόκκινες ρίγες – μπλουζάκι με καρδιά δίπλα στην τσέπη στο στήθος',
'es':'Tops a juego para la familia con rayas rojas – camiseta con un corazón junto al bolsillo del pecho',
'fi':'Punaraidalliset yhteensopivat perheen yläosat – T-paita, jossa on sydän rintataskun kohdalla',
'fr':'Hauts assortis pour la famille à rayures rouges – T-shirt avec un cœur au niveau de la poche poitrine',
'he':'חולצות משפחתיות תואמות בפסים אדומים – טי שירט עם לב ליד כיס החזה',
'it':'Top coordinati per la famiglia "Red Stripe" - T-shirt con un cuore accanto al taschino',
'pl':'Red Stripe – pasujące rodzinne topy, T-shirt z serduszkiem przy kieszeni na piersi',
'pt-BR':'Red Stripe – blusas combinando para a família, camiseta com um coração junto ao bolso no peito',
'ro':'Red Stripe – topuri asortate pentru familie, tricou cu o inimioară lângă buzunarul de la piept',
'ru':'Red Stripe — парные семейные топы, футболка с сердечком у нагрудного кармана',
'sv':'Red Stripe – matchande familjetoppar, T-shirt med ett hjärta vid bröstfickan',
}
explicit={'ar','es','pl','ro','ru','sv'}
assessment=[];candidates=[];checks=[]
for b in base:
 l=b['locale'];effective=b['effectiveBeforeValue'];ov=overlay.get(l)
 if ov: p,r=ov;effective=r['value']
 else:r=b
 before=next(t for t in raw['tr_'+l.replace('-','_')] if t['key']=='title' and t.get('market') is None)
 assert before==b['rawBefore']
 assert source['value']==b['sourceValue'] and source['digest']==b['sourceDigest']
 assert FH(rawpath)==b['rawFileSHA256']
 work=P/f'review/product-title-completeness/worklist_{l}.json'
 w=next(t for t in rows(work) if t['resourceId']==rid)
 assert w['rawBefore']==before and w['sourceDigest']==source['digest']
 if l in values:
  status='CORRECTION_EXPLICIT_SHAPE_CLAIM' if l in explicit else 'CORRECTION_AMBIGUOUS_HEART_POCKET_OR_MALFORMED_PHRASE'
  reason='English body identifies a small heart detail at the chest pocket. Proposed wording identifies the heart at/beside that pocket without claiming the pocket itself is heart-shaped.'
  c=copy.deepcopy(w);c.update(value=values[l],valueSHA256=H(values[l]),productIndex=206,source=source['value'],effectiveBeforeValue=effective,expectedEffectiveBeforeValueSHA256=H(effective),expectedBeforeValueSHA256=H(effective),before=None if ov else before,requiresFreshEffectiveBeforeObject=bool(ov),requiresFreshLiveSourceAndBeforeGuard=True,reason=reason,reviewStatus='AUTHOR_PENDING_INDEPENDENT_MEANING_REVIEW',inputWorklistFile=str(work.relative_to(P)),inputWorklistFileSHA256=FH(work),supportingSourceDigests={'body_html':body['digest']},sourceContextEvidence={'bodyValueSHA256':H(body['value']),'exactQuoteNormalizedWhitespace':quote,'meaning':'Heart detail at chest pocket; pocket shape is not specified.'})
  if ov:
   c.update(overlayApplied=True,overlaySourceFile=str(p.relative_to(P)),overlaySourceFileSHA256=FH(p),beforeBindingNote='Expected before is final reviewed/planned title value. Root must confirm the exact previously verified release and fresh global before object after the bulk release; null is not missing translation.')
  candidates.append(c)
 elif l in ['nl','no']:
  status='RETAIN_ALREADY_CORRECTED_BY_OTHER_REVIEWER';reason='Reviewed planned value already places the heart at the chest pocket without a pocket-shape claim.'
 else:
  assert l in ['hi','ja','ko']
  status='RETAIN_DESIGN_COMPOUND_NO_POCKET_SHAPE_CLAIM';reason='Heart Pocket loanword/design compound mirrors the English title; it does not assert that the pocket has a heart shape. No narrow source-body precision correction needed.'
 assessment.append({'locale':l,'i':b['i'],'resourceId':rid,'sourceValue':source['value'],'sourceDigest':source['digest'],'rawBefore':before,'finalPlannedBefore':effective,'plannedBeforeSHA256':H(effective),'plannedOverlayFile':str(ov[0].relative_to(P)) if ov else None,'plannedOverlayFileSHA256':FH(ov[0]) if ov else None,'disposition':status,'reason':reason,'proposedValue':values.get(l),'supportingSourceDigests':{'body_html':body['digest']},'exactQuoteNormalizedWhitespace':quote})
 checks.append({'locale':l,'rawFileSHA256Pass':True,'rawBeforeExactPass':True,'sourceTitleValueDigestPass':True,'worklistRawBeforeAndSourcePass':True,'bodyDigest':body['digest'],'bodyExactNormalizedQuotePass':True,'rootFreshPlannedBeforeGuardRequired':bool(ov),'meaningAssessment':status})
assert len(assessment)==20 and len(candidates)==15
for name,data in [('p206_assessment20.json',{'rows':assessment}),('p206_precision_candidate15.json',{'rows':candidates}),('p206_checks.json',{'rows':checks,'allLocalBindingChecksPass':True,'assessed':20,'correctionCandidates':15,'retainedAlreadyCorrected':2,'retainedNeutralDesignCompound':3,'externalWrites':'NONE','releaseStatus':'PENDING_ROOT_INDEPENDENT_REVIEW_AND_FRESH_SOURCE_BODY_BEFORE_GUARDS'})]:
 (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('P206',len(assessment),'assessed',len(candidates),'corrections',FH(O/'p206_precision_candidate15.json'))
