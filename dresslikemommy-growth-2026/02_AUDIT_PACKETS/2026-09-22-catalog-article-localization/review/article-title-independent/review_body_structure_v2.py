# -*- coding: utf-8 -*-
"""Validate only seven v2 deltas over independently verified immutable v1."""
from review_body_structure import *

P1=I/'tag_candidates_v1.json';P2=I/'tag_candidates_v2.json'
assert file_sha(P1)=='ad256696f17797e8e22390d6eff04a91022cccb5c3ce84627265472611a23050'
assert file_sha(P2)=='dd9a2e2f4aab474ad559b4861a90124d04012a4f94b64978d4c200bd9efb9922'
prior_checks=load(H/'body_structure_v1_independent_checks.json')
assert prior_checks['inputSHA256']==file_sha(P1) and prior_checks['allExactBindingsAndAllowedPatches']=='PASS'
a=load(P1)['rows'];b=load(P2)['rows'];assert len(a)==len(b)==374
proof=load(I/'residual_seven_evidence.json')['rows']
proofs={(r['resourceId'],r['locale']):r for r in proof}
expected={(41,'it'),(51,'ar'),(51,'it'),(51,'nl'),(65,'it'),(84,'it'),(97,'ja')}
url=lambda v:re.findall(r'https?://[^\s<>"\']+',v)
cells=lambda v:re.findall(r'<(td|th)\b[^>]*>(.*?)</\1\s*>',v,re.S|re.I)
restored=[];qualified=[];rowchecks=[];english_alt=[];parser_errors=[]
for x,y in zip(a,b):
    for k in x:
        if k not in ['value','valueSHA256','checks']:assert x[k]==y[k],(x['productIndex'],x['locale'],k)
    assert sha(y['value'])==y['valueSHA256']
    changes=[]
    if x['value']!=y['value']:
        assert (y['productIndex'],y['locale']) in expected
        e=proofs[(y['resourceId'],y['locale'])]
        assert e['sourceDigest']==y['sourceDigest'] and e['beforeValueSHA256']==y['beforeValueSHA256']
        assert e['v1ValueSHA256']==x['valueSHA256']==y['versionOneValueSHA256'] and e['v2ValueSHA256']==y['valueSHA256']
        assert e['changes']==y['residualMarkupExceptions']
        value=x['value']
        for ch in e['changes']:
            old,new=ch['before'],ch['after'];assert value.count(old)==1
            if ch['kind']=='RESTORE_TRUNCATED_IMAGE_PARAGRAPH_FROM_UNIQUE_ENGLISH_SOURCE_LOCATION':
                assert y['locale']=='it' and old=='<p><immagine'
                assert new==ch['sourceExactImageParagraph'] and y['source'].count(new)==1
                source_images=re.findall(r'<p>\s*<img\b.*?</p>',y['source'],re.S)
                assert source_images==[new]
                assert not re.findall(r'<img\b',value)
                before_at=value.index(old);assert '</table>' in value[:before_at]
                assert url(new)==ch['imageURLsRestored']
                english_alt.extend({'resourceId':y['resourceId'],'locale':'it','alt':v} for v in re.findall(r'\balt="([^"]*)"',new))
            elif ch['kind']=='RESTORE_SOURCE_PAIRED_THIRD_IMAGE_SRC_AND_MISSING_CLOSE':
                assert y['productIndex']==51 and y['locale'] in ('ar','nl')
                assert old in ['src="___DLMTOK2__','src="__DLMTOK2___']
                source_imgs=[dict(attrs) for tag,attrs in Parsed(y['source']).attrs if tag=='img']
                target_imgs=[dict(attrs) for tag,attrs in Parsed(value).attrs if tag=='img']
                assert len(source_imgs)==3 and len(target_imgs)==3
                assert 'DLMTOK2' in target_imgs[2]['src']
                assert [t['src'] for t in target_imgs[:2]]==[t['src'] for t in source_imgs[:2]]
                assert new=='src="'+source_imgs[2]['src']+'"></p>'
                assert ch['sourceExactThirdImageTag'] in y['source']
                assert ch['imageURLsRestored']==[source_imgs[2]['src']]
                # Existing target-localized third alt stays outside the changed literal.
                at=value.index(old);assert '<img alt=' in value[max(0,at-300):at]
            elif ch['kind']=='SOURCE_ALIGNED_STRONG_CLOSE_IN_LIST_ITEM':
                assert y['productIndex']==97 and y['locale']=='ja'
                assert old in ['<strong>トレンディなストリートウェアの外観:</li>','<strong>トレンドのデザイン:</li>']
                assert new==old[:-5]+'</strong>'
                assert y['source'].count(ch['sourceExactHeadingTag'])==1
            else:raise AssertionError(ch['kind'])
            value=value.replace(old,new,1);changes.append(ch['kind'])
            restored.extend(ch.get('imageURLsRestored',[]))
        assert value==y['value']
        assert Counter(url(y['value']))-Counter(url(x['value']))==Counter(u for ch in e['changes'] for u in ch.get('imageURLsRestored',[]))
        assert not (Counter(url(x['value']))-Counter(url(y['value'])))
    else:assert (y['productIndex'],y['locale']) not in expected
    assert cells(x['value'])==cells(y['value'])
    # A separate HTMLParser plus strict explicit stack validates all completed elements.
    parsed=Parsed(y['value']);stack=[];row_errors=[]
    for token in parsed.tokens:
        if token in VOID:continue
        if token.startswith('/'):
            if not stack or stack[-1]!=token[1:]:row_errors.append({'closing':token,'stack':stack[-4:]})
            elif stack:stack.pop()
        else:stack.append(token)
    if stack:row_errors.append({'unclosed':stack})
    if row_errors:parser_errors.append({'productIndex':y['productIndex'],'locale':y['locale'],'errors':row_errors})
    assert '<immagine' not in y['value']
    q=copy.deepcopy(y)
    q['sourceValue']=q['source']
    q['reviewStatus']='INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    q['independentInputFile']=str(P2.relative_to(R));q['independentInputFileSHA256']=file_sha(P2)
    q['independentReviewStatus']='PASS_EXACT_STRUCTURAL_REPAIRS_AND_EXPLICIT_SOURCE_PAIRED_EXCEPTIONS'
    qualified.append(q)
    rowchecks.append({'productIndex':y['productIndex'],'resourceId':y['resourceId'],'locale':y['locale'],'v1BindingsPreserved':'PASS','v2ExactAllowedDelta':'PASS','allCellsAndHeadersExact':'PASS','independentHTMLParserStrictBalance':'FAILED' if row_errors else 'PASS','residualChanges':changes})
assert len(restored)==14 and len(english_alt)==12 and len(proof)==7
result={'status':'V2_PARITY_QUALIFIED_AWAIT_V3_AUTHORIZED_REMAINING_PLACEHOLDERS_AND_ITALIAN_ALTS','qualifiedRows':374,'inputFile':str(P2.relative_to(R)),'inputSHA256':file_sha(P2),'v1IndependentEvidence':'review/article-title-independent/body_structure_v1_independent_checks.json','exactAllowedTokenRepairs':3575,'exactSourceBackedAttributeNameRepairs':78,'JapaneseP5AuthorizedMeaningCorrections':3,'v2ResidualRowsReviewed':7,'restoredSourceExactImageURLs':14,'independentBalancedBodies':374,'allCellsAndHeaderBytesUnchangedFromV1':'PASS','EnglishAltFallbacksPreservedFromExactSource':english_alt,'checks':rowchecks,'limitations':['Structural scope only: unchanged body wording, chart row labels and source claims are not certified as correct.','Legacy additional fallback charts preserved, including all numbers, cells and headings.','Twelve restored image alt attributes in four Italian bodies remain exact English source text; localized alt follow-up required for full-language completeness.']}
if parser_errors:
    dump('body_structure_v2_parser_failures.json',{'status':'DO_NOT_RELEASE_V2_AWAIT_V3','allSevenExactDeltasAndSourceImages':'PASS','all374CellsPreserved':'PASS','parserFailedRows':parser_errors,'checks':rowchecks})
    print(json.dumps({'v2ExactSevenDeltas':'PASS','parserFailures':[(x['productIndex'],x['locale']) for x in parser_errors]}))
    raise SystemExit(0)
dump('body_structure_v2_reviewed.json',{'rows':qualified})
dump('body_structure_v2_independent_checks.json',result)
print(json.dumps({'qualified':374,'hash':file_sha(H/'body_structure_v2_reviewed.json'),'images':14,'EnglishAltFallbacks':len(english_alt),'balanced':374}))
