# -*- coding: utf-8 -*-
"""Independent final 375-row structural review over immutable staged inputs."""
from review_body_structure import *
P2=I/'tag_candidates_v2.json';P3=I/'tag_candidates_v3.json'
assert file_sha(P2)=='dd9a2e2f4aab474ad559b4861a90124d04012a4f94b64978d4c200bd9efb9922'
assert file_sha(P3)=='db4923e98bfc5f1bd4313b1d8c69f55ad7b966d46d2aa13cebef4ed8967260dc'
v2proof=load(H/'body_structure_v2_parser_failures.json')
assert v2proof['allSevenExactDeltasAndSourceImages']=='PASS' and v2proof['all374CellsPreserved']=='PASS'
a={(r['resourceId'],r['locale']):r for r in load(P2)['rows']}
rows=load(P3)['rows']; evidence=load(I/'v3_delta_evidence.json')['rows'];evidence={(r['resourceId'],r['locale']):r for r in evidence}
inventory={(r['resourceId'],r['locale']):r for r in load(I/'effective_body_inventory.json')['rows']}
assert len(rows)==len({(r['resourceId'],r['locale'],r['key']) for r in rows})==375
cells=lambda v:re.findall(r'<(td|th)\b[^>]*>(.*?)</\1\s*>',v,re.S|re.I)
urls=lambda v:re.findall(r'https?://[^\s<>"\']+',v)
expected_prose={
(3,'ar'):('هذا طقم ملابس سباحة __DLMTOK0___ مطابق','هذا طقم ملابس سباحة متطابق للأم وطفلتها'),
(39,'ar'):('__DLMTOK0____','المتطابق للأم وطفلتها'),
(90,'ja'):('__DLMTOK0___','Tシャツ')}
checks=[];qualified=[];counts=Counter();newURLs=[];image_errors=[]
for y in rows:
    key=(y['resourceId'],y['locale']);old=a.get(key)
    if old:
        for k in old:
            if k not in ['value','valueSHA256','checks']:assert old[k]==y[k],(key,k)
        baseline=old['value']
    else:
        assert y['productIndex']==99 and y['locale']=='fi';inv=inventory[key]
        for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']:
            assert inv[k]==y[k],(key,k)
        assert not inv['overlayApplied'] and y['before']['outdated'] is False
        assert y['before']==y['rawBefore'] and file_sha(R/y['rawFile'])==y['rawFileSHA256']
        node=next(n for n in load(R/y['rawFile'])['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==y['resourceId'])
        source=next(t for t in node['translatableContent'] if t['key']=='body_html')
        before=next(t for t in node['tr_fi'] if t['key']=='body_html')
        assert source['value']==y['source'] and source['digest']==y['sourceDigest'] and before==y['before']
        assert sha(y['source'])==y['sourceSHA256'] and sha(before['value'])==y['beforeValueSHA256']==y['expectedBeforeValueSHA256']
        baseline=before['value']
    current=baseline;extra=[]
    if key in evidence:
        ev=evidence[key];assert ev['sourceDigest']==y['sourceDigest'] and ev['v3ValueSHA256']==y['valueSHA256']
        if old:assert ev['v2ValueSHA256']==sha(baseline)==y['versionTwoValueSHA256']
        assert ev['changes']==y['versionThreeExceptions']
        for ch in ev['changes']:
            kind=ch['kind'];before=ch['before'];after=ch['after'];assert current.count(before)==1
            if kind=='MANUAL_ITALIAN_TRANSLATION_OF_NEWLY_RESTORED_SOURCE_ALT':
                assert y['locale']=='it' and y['productIndex'] in (41,51,65,84)
                assert 'alt="'+ch['source']+'"'==before and before in y['source']
                assert after=='alt="'+html.escape(ch['value'],quote=True)+'"'
                # All 12 complete source-target strings manually read; named print lettering retained.
            elif kind=='EXACT_SOURCE_BACKED_MISSING_PROSE_FRAGMENT':
                assert expected_prose[(y['productIndex'],y['locale'])]==(before,after)
                assert ch['sourceExactQuote'] in y['source']
                if y['locale']=='ar':assert 'mother-daughter' in y['source'].lower()
            elif kind=='RESTORE_MALFORMED_SOURCE_PAIRED_IMAGE_CHAIN':
                assert (y['productIndex'],y['locale']) in [(41,'ar'),(41,'pl'),(65,'ar'),(85,'ar'),(85,'pl'),(86,'pl')]
                source_paragraph=ch['sourceExactImageParagraph'];assert y['source'].count(source_paragraph)==1
                source_images=[dict(attrs) for tag,attrs in Parsed(source_paragraph).attrs if tag=='img']
                target_images=[dict(attrs) for tag,attrs in Parsed(after).attrs if tag=='img']
                assert [im['src'] for im in source_images]==ch['sourceURLsInOrder']==[im['src'] for im in target_images]
                assert [im.get('alt') for im in target_images]==ch['existingLocalizedAltValuesPreserved']
                for alt in ch['existingLocalizedAltValuesPreserved']:assert alt in before
                assert len(source_images)==len(target_images)
                assert urls(before)==ch['survivingURLsPreservedInOrder']
                assert [u for u in ch['sourceURLsInOrder'] if u in urls(before)]==urls(before)
                if y['productIndex']==86:
                    assert [im['src'] for im in source_images[:3]]==urls(before)
                    assert '__DLMTOK3___' in before and '__DLMTOK4___' in before
                # Manually compared source alt order to existing Arabic/Polish meanings for all nonempty alts.
                expected='<p>'+''.join('<img src="'+im['src']+'" alt="'+html.escape(alt,quote=True)+'">' for im,alt in zip(source_images,ch['existingLocalizedAltValuesPreserved']))+'</p>'
                assert after==expected
                newURLs.extend(list((Counter(urls(after))-Counter(urls(before))).elements()))
            elif kind=='EXACT_MISMATCHED_IMAGE_ATTRIBUTE_DELIMITER':
                assert (y['productIndex'],y['locale']) in [(47,'hi'),(49,'hi'),(50,'hi'),(96,'hi'),(84,'pl'),(84,'ru')]
                assert ch['sourceExactImageTag'] in y['source'] and y['source'].count(ch['sourceURL'])==1
                assert urls(before)==urls(after)==[ch['sourceURL']]
                if y['locale']=='hi':assert after==before.replace("src='",'src="',1)
                else:
                    broken_end='”>' if y['locale']=='pl' else '»>'
                    assert before.endswith(broken_end) and after==before[:-2]+'">'
                assert len([t for t,attrs in Parsed(after).attrs if t=='img'])==1
            elif kind=='MISSING_CLOSING_STRONG_BOUNDARY':
                assert (y['productIndex'],y['locale'])==(99,'fi')
                assert before=='</strong yhteensopiviin asuihin' and after=='</strong> yhteensopiviin asuihin'
                assert ch['sourceExactTag'] in y['source']
                assert '<strong data-start="2705" data-end="2729">' in baseline
            else:raise AssertionError(kind)
            current=current.replace(before,after,1);counts[kind]+=1;extra.append(kind)
    else:assert old and y['value']==old['value'] and not y.get('versionThreeExceptions')
    assert current==y['value'] and sha(current)==y['valueSHA256']
    assert cells(current)==cells(baseline)
    assert not re.search(r'_+DLMTOK\d+_+',current)
    parsed=Parsed(current);stack=[]
    for token in parsed.tokens:
        if token in VOID:continue
        if token.startswith('/'):
            assert stack and stack[-1]==token[1:],(key,token,stack[-4:])
            stack.pop()
        else:stack.append(token)
    assert not stack,key
    for tag,attrs in parsed.attrs:
        if tag=='img':
            d=dict(attrs)
            if not (d.get('src','').startswith('https://') and '<' not in d['src'] and '>' not in d['src']):image_errors.append({'productIndex':y['productIndex'],'locale':y['locale'],'attributes':attrs})
    q=copy.deepcopy(y);q['sourceValue']=q['source'];q['reviewStatus']='INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    q['independentInputFile']=str(P3.relative_to(R));q['independentInputFileSHA256']=file_sha(P3)
    q['independentReviewStatus']='PASS_EXACT_STRUCTURAL_PATCHES_WITH_SOURCE_BOUND_EXPLICIT_EXCEPTIONS'
    qualified.append(q);checks.append({'productIndex':y['productIndex'],'resourceId':y['resourceId'],'locale':y['locale'],'sourceBeforeBinding':'PASS','exactV1V2V3AllowedPatch':'PASS','allTableCellsHeadersUnchanged':'PASS','standardHTMLParserBalanced':'PASS','allImageSrcValidBoundaries':'PASS','additionalExceptions':extra})
assert len(evidence)==20 and counts['MANUAL_ITALIAN_TRANSLATION_OF_NEWLY_RESTORED_SOURCE_ALT']==12
result={'status':'INDEPENDENTLY_QUALIFIED_PENDING_ROOT_FRESH_SOURCE_BEFORE_PUBLICATION_GUARDS','inputFile':str(P3.relative_to(R)),'inputSHA256':file_sha(P3),'rows':375,'allTableCellAndHeaderBytesPreserved':375,'independentStandardHTMLParserBalancedRows':375,'allImageSrcAttributeBoundariesValid':375,'authorV1TokenRepairsIndependentlyVerified':3575,'authorV2SevenDeltasIndependentlyVerified':7,'authorV3RowsWithExplicitExceptions':20,'v3ChangeCounts':dict(counts),'v3AdditionalMissingSourceImageURLsRestored':len(newURLs),'manualMeaningReview':'All12 Italian alt translations and3 completed prose phrases individually read against exact English; all3 JA P5 necktie phrases reviewed. Each nonempty Arabic/Polish image alt compared to source ordering for image-pair correctness; pre-existing wording preserved. Six delimiter repairs fix actual parser swallowing; full375 parse balanced.','checks':checks,'limitations':['Structural repairs do not certify untouched body wording, row labels or source measurements as correct. Separate header and size-label lanes reconcile those.','All legacy extra fallback tables retained with every existing cell/header unchanged. No unknown English product facts inferred or changed.']}
if image_errors:
    dump('body_structure_v3_image_failures.json',{'status':'AWAIT_P81_PL_IMAGE_DELIMITER_FIX','all375ExactPatchBindingsCellPreservation':'PASS','all375ParserStackBalance':'PASS','all20V3DeltasMeaningAndSourceProof':'PASS','imageAttributeFailures':image_errors,'counts':dict(counts)})
    print(json.dumps({'all375ParityAndBalance':'PASS','imageFailures':image_errors},ensure_ascii=False));raise SystemExit(0)
dump('body_structure375_reviewed.json',{'rows':qualified});dump('body_structure375_independent_checks.json',result)
print(json.dumps({'qualified':375,'SHA256':file_sha(H/'body_structure375_reviewed.json'),'v3Changes':dict(counts),'additionalSourceImages':len(newURLs)}))
