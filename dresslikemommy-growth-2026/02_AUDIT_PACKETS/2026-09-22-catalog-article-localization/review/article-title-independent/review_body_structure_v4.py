# -*- coding: utf-8 -*-
from review_body_structure import *
P3=I/'tag_candidates_v3.json';P4=I/'tag_candidates_v4.json'
assert file_sha(P3)=='db4923e98bfc5f1bd4313b1d8c69f55ad7b966d46d2aa13cebef4ed8967260dc'
assert file_sha(P4)=='a0a54bd0bcdce59936aad065f94e069950ee2bb820fd5a1e2666536bdc8f1c1f'
prior=load(H/'body_structure_v3_image_failures.json')
assert prior['all375ExactPatchBindingsCellPreservation']==prior['all375ParserStackBalance']==prior['all20V3DeltasMeaningAndSourceProof']=='PASS'
a=load(P3)['rows'];b=load(P4)['rows'];assert len(a)==len(b)==375
cells=lambda v:re.findall(r'<(td|th)\b[^>]*>(.*?)</\1\s*>',v,re.S|re.I)
urls=lambda v:re.findall(r'https?://[^\s<>"\']+',v)
rows=[];checks=[];changes=[];image_count=0;independent_corrections=[]
for x,y in zip(a,b):
    for k in x:
        if k not in ['value','valueSHA256','checks']:assert x[k]==y[k],(y['productIndex'],y['locale'],k)
    value=x['value'];delta=y.get('versionFourExceptions',[])
    if value!=y['value']:
        assert (y['productIndex'],y['locale']) in [(65,'hi'),(81,'pl'),(84,'hi')]
        for c in delta:
            assert c['kind']=='EXACT_MISMATCHED_IMAGE_ATTRIBUTE_DELIMITER'
            assert value.count(c['before'])==1 and c['sourceExactImageTag'] in y['source']
            if y['locale']=='pl':
                assert c['before']=='„Need More Juice”” src=' and c['after']=='„Need More Juice”" src='
            else:
                source_img=[dict(attrs) for tag,attrs in Parsed(c['sourceExactImageTag']).attrs if tag=='img'];assert len(source_img)==1
                source_url=source_img[0]['src'];assert urls(c['before'])==[source_url]
                alt=c['preservedLocalizedAltValue'];assert alt in c['before']
                expected='<img src="'+source_url+'" alt="'+html.escape(alt,quote=True)+'">'
                assert c['after']==expected
                # Both delimiters and content boundaries are explicitly observed in the malformed old literal.
                assert c['before'].startswith("<img src='") and '" alt=\'' in c['before']
            value=value.replace(c['before'],c['after'],1)
        changes.append({'productIndex':y['productIndex'],'locale':y['locale'],'repairs':len(delta),'sourceExactImagePairing':'PASS','localizedAltContentPreserved':'PASS'})
    else:assert not delta
    assert value==y['value'] and sha(value)==y['valueSHA256']
    assert cells(x['value'])==cells(value) and urls(x['value'])==urls(value)
    correction_literals=[]
    for match in list(re.finditer(r'<img\b[^>]*>',value)):
        oldtag=match[0];parsed_tag=Parsed(oldtag).attrs
        if not any(v is None for t,ats in parsed_tag for k,v in ats):continue
        assert (y['productIndex'],y['locale']) in [(81,'ar'),(82,'ar'),(82,'it'),(83,'ar'),(83,'it'),(84,'ar')]
        start=oldtag.index('alt="')+5
        end=oldtag.index('" src=') if oldtag.startswith('<img alt=') else len(oldtag)-2
        original_alt=oldtag[start:end];assert '"' in original_alt
        encoded_alt=html.escape(original_alt,quote=True)
        newtag=oldtag[:start]+encoded_alt+oldtag[end:]
        oldurl=re.search(r'src="([^"]*)"',oldtag)[1]
        assert oldurl in y['source'] and value.count(oldtag)==1
        newattrs=dict(Parsed(newtag).attrs[0][1])
        assert newattrs['alt']==original_alt and newattrs['src']==oldurl
        assert set(newattrs)=={'src','alt'}
        assert urls(oldtag)==urls(newtag)
        value=value.replace(oldtag,newtag,1)
        correction_literals.append({'before':oldtag,'after':newtag,'preservedLocalizedAltValue':original_alt,'sourceURL':oldurl,'reason':'HTML-entity encode internal quotation marks so all existing alt wording stays inside its intended attribute; no word, source URL or cell changed.'})
    if correction_literals:
        independent_corrections.append({'productIndex':y['productIndex'],'resourceId':y['resourceId'],'locale':y['locale'],'sourceDigest':y['sourceDigest'],'beforeAuthorValueSHA256':y['valueSHA256'],'valueSHA256':sha(value),'literalChanges':correction_literals})
        assert cells(y['value'])==cells(value) and urls(y['value'])==urls(value)
    parsed=Parsed(value);stack=[];imgs=[]
    for t in parsed.tokens:
        if t in VOID:continue
        if t.startswith('/'):
            assert stack and stack[-1]==t[1:],(y['productIndex'],y['locale'],t,stack[-4:]);stack.pop()
        else:stack.append(t)
    assert not stack
    for tag,attrs in parsed.attrs:
        if tag!='img':continue
        d=dict(attrs);assert d.get('src','').startswith('https://')
        assert not re.search(r'[\s<>"\']',d['src'])
        assert d['src'] in y['source'] or d['src'] in y['before']['value']
        assert len([k for k,v in attrs if k=='src'])==1
        assert not any(v is None for k,v in attrs), (y['productIndex'],y['locale'],attrs)
        imgs.append(d)
    assert len(imgs)==len(re.findall(r'<img\b',value,re.I)),(y['productIndex'],y['locale'])
    assert not re.search(r'_+DLMTOK\d+_+',value)
    image_count+=len(imgs)
    q=copy.deepcopy(y);q['value']=value;q['valueSHA256']=sha(value)
    if correction_literals:q['independentAttributeEncodingRepairs']=correction_literals;q['beforeIndependentReviewValueSHA256']=y['valueSHA256']
    q['sourceValue']=q['source'];q['reviewStatus']='INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    q['independentInputFile']=str(P4.relative_to(R));q['independentInputFileSHA256']=file_sha(P4)
    q['independentReviewStatus']='PASS_SOURCE_BOUND_STRUCTURAL_PATCHES_WITH_EXPLICIT_MEANING_EXCEPTIONS'
    rows.append(q);checks.append({'productIndex':y['productIndex'],'resourceId':y['resourceId'],'locale':y['locale'],'sourceBeforeExactBindings':'PASS','allAllowedPatchesAndCells':'PASS','standardParserBalance':'PASS','allPresentImageAttributesAndSourceProvenance':'PASS','presentImages':len(imgs)})
assert len(changes)==3 and sum(x['repairs'] for x in changes)==6
result={'status':'INDEPENDENTLY_QUALIFIED_PENDING_ROOT_FRESH_SOURCE_BEFORE_PUBLICATION_GUARDS','inputFile':str(P4.relative_to(R)),'inputSHA256':file_sha(P4),'qualifiedRows':375,'all375CellAndHeaderBytesPreserved':'PASS','all375StandardHTMLParserStacksBalanced':'PASS','allPresentImages':image_count,'allPresentImageAttributesAndSourceOrBeforeProvenance':'PASS','initialTagTokenRepairs':3575,'translatedIdNamesRepaired':78,'JapaneseP5MeaningRepairs':3,'manuallyReviewedItalianAltTranslations':12,'manuallyReviewedSourceBoundProsePlaceholders':3,'allNewImageRestorationsExactSourcePaired':'PASS','v4DeltaRows':changes,'independentAltEncodingRows':len(independent_corrections),'independentAltEncodingOccurrences':sum(len(r['literalChanges']) for r in independent_corrections),'evidenceChain':['body_structure_v1_independent_checks.json','body_structure_v2_parser_failures.json','body_structure_v3_image_failures.json'],'checks':checks,'limitations':['Untouched body prose, size-row labels and English source assertions remain outside this structural review; separate review lanes reconcile them.','Every existing table cell/header and legacy fallback table retained. Seven legacy image-count differences are preserved and separately inventoried by author; image count equality to English is not claimed.']}
assert len(independent_corrections)==6 and sum(len(r['literalChanges']) for r in independent_corrections)==7
dump('body_structure375_independent_corrections.json',{'rows':independent_corrections})
dump('body_structure375_reviewed.json',{'rows':rows});dump('body_structure375_independent_checks.json',result)
print(json.dumps({'qualified':375,'presentImages':image_count,'v4DeltaRows':3,'SHA256':file_sha(H/'body_structure375_reviewed.json')}))
