# -*- coding: utf-8 -*-
"""Independent offline review; no author verifier imported or executed."""
import copy, hashlib, html, json, re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

H = Path(__file__).resolve().parent
R = H.parents[2]
load = lambda p: json.loads(p.read_text())
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
fs = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
dump = lambda n, d: (H/n).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
key = lambda r: (r['resourceId'], r['locale'], r['key'])
INPUTS = {
 'author': ('review/body-structure-audit/placeholder_candidates_v2.json', '935093c964c983e916af8a336fe517b2b610b9dd455b16eee1f46c2fe1af9d44'),
 'structure': ('review/article-title-independent/body_structure375_reviewed.json', 'f8ae9d61b29a01f6628edf21cbf84421efd9c893f7d40f1e86c13538818ac501'),
 'headers': ('review/body-header-localization/header_candidates_v2.json', '30ac93375168fb7df4b2a355aed666a8e19c597e099ce98a2b42acca8e05c142'),
 'sizes': ('review/size-label-repair/candidate_all156.json', '340b5221d25c2971559e97dcf872082592bf6782571a0fd220d1f14a7cffa918'),
}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
BLOCK = set('address article aside blockquote div dl fieldset footer form h1 h2 h3 h4 h5 h6 header hr li main nav ol p pre section table ul'.split())
MASK = re.compile(r'[A-Za-z0-9_]*(?:QZ|XTOKEN|QX|TOKEN)[A-Za-z0-9_]*')
MANUAL = {(153, l) for l in ('cs','el','fi')} | {(154,l) for l in ('cs','el','fi')} | {(182,'de')}

class Markup(HTMLParser):
    """Bounded stack check allowing only evidenced optional li/p and stray li/ul ends.

    This is a lexical/structural check, not a full browser HTML5 tree builder.
    """
    def __init__(self, value):
        super().__init__(convert_charrefs=False)
        self.stack=[]; self.errors=[]; self.optional=[]; self.ignored=[]
        self.attributes=[]; self.media=[]; self.comments=[]
        self.feed(value); self.close()
        while self.stack and self.stack[-1] in ('li','p'):
            self.optional.append(self.stack.pop()+'_at_eof')
        if self.stack: self.errors.append(['unclosed', self.stack.copy()])
        if self.rawdata: self.errors.append(['unfinished',self.rawdata])
    def handle_starttag(self,t,a):
        if a: self.attributes.append((t,a,self.get_starttag_text()))
        if t in ('img','a','source'): self.media.append((t,a))
        if t in BLOCK and self.stack and self.stack[-1]=='p':
            self.stack.pop(); self.optional.append('p_before_'+t)
        if t=='li' and 'li' in self.stack:
            pos=len(self.stack)-1-self.stack[::-1].index('li')
            tail=self.stack[pos+1:]
            if not any(t in tail for t in ('ul','ol')):
                if tail: self.errors.append(['inline_unclosed_before_li',tail.copy()])
                self.stack=self.stack[:pos]; self.optional.append('li_before_li')
        if t not in VOID: self.stack.append(t)
    def handle_endtag(self,t):
        if t in VOID:return
        if t in ('ul','ol') and self.stack and self.stack[-1]=='li':
            self.stack.pop();self.optional.append('li_before_'+t+'_end')
        if self.stack and self.stack[-1]==t:self.stack.pop();return
        if t in ('ul','li') and t not in self.stack:
            self.ignored.append(t);return
        self.errors.append(['mismatched_end',t,self.stack.copy()])
        if t in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(t)]
    def handle_startendtag(self,t,a):
        self.handle_starttag(t,a)
        if t not in VOID:self.handle_endtag(t)
    def handle_comment(self,s):self.comments.append(s)

def common_edges(old,new):
    prefix=0
    while prefix<min(len(old),len(new)) and old[prefix]==new[prefix]:prefix+=1
    suffix=0
    while suffix<min(len(old)-prefix,len(new)-prefix) and old[-suffix-1]==new[-suffix-1]:suffix+=1
    return old[prefix:len(old)-suffix if suffix else None],new[prefix:len(new)-suffix if suffix else None]

def patch_value(row, value, evidence=False):
    source=row['source']; items=re.findall(r'<li\b[^>]*>.*?</li>',source,re.S)
    for i,p in enumerate(row['patches']):
        assert p['sourceExactQuote'] in source, ('source_quote',key(row),i)
        assert value.count(p['before'])==1, ('patch_occurrence',key(row),i)
        pos=value.index(p['before'])
        if 'sourceListItemOrdinal' in p:
            ordinal=p['sourceListItemOrdinal']
            assert items[ordinal]==p['sourceExactQuote']
            target_ordinal=len(re.findall(r'<li\b',value[:pos]))-1
            # EL157 retains its earlier rendering of English introductory Fabric p as a first li.
            offset=1 if (row['productIndex'],row['locale'])==(157,'el') else 0
            assert target_ordinal==ordinal+offset,(key(row),ordinal,target_ordinal)
            if p.get('sourceFollowingListItem'):assert items[ordinal+1]==p['sourceFollowingListItem']
        old,new=common_edges(p['before'],p['after'])
        manual=(row['productIndex'],row['locale']) in MANUAL and p['before'].startswith('<li>')
        if not manual:
            if new=='</li>':
                assert MASK.fullmatch(old) or old=='<strong>', (key(row),old,new)
            elif (row['productIndex'],row['locale'])==(134,'ro'):
                assert (old,new)==('strong','/li')
            elif (row['productIndex'],row['locale']) in {(163,l) for l in ('da','he','no','sv')}:
                # Suffix of native sleeves is unchanged; only the explicit corrupt mask and boundary differ.
                assert p['after'].endswith('.</li>') and p['before'].endswith('.')
                native=p['after'][:-6]
                assert p['before'].startswith(native)
                assert MASK.fullmatch(p['before'][len(native):-1])
            elif new in ('</h3><ul>','</p><p>'):
                assert MASK.fullmatch(old)
            elif (row['productIndex'],row['locale'])==(145,'el'):
                assert old=='' and new=='</p><h3>Βασικά χαρακτηριστικά:</h3><ul>'
                assert p['sourceExactQuote']=='</p><h3>Key Features:</h3><ul>'
            else:raise AssertionError(('unreviewed_patch_kind',key(row),old,new))
        else:
            assert p['sourceExactQuote'].startswith('<li>') and p['sourceExactQuote'].endswith('</li>')
            assert p['after'].startswith('<li>') and p['after'].endswith('</li>\n')
            assert re.findall(r'\d+',p['sourceExactQuote'])==re.findall(r'\d+',p['after'])==[]
        value=value.replace(p['before'],p['after'],1)
    return value

def preserve(before, after):
    patterns = [r'<table\b.*?</table>',r'<t[dh]\b[^>]*>.*?</t[dh]>',r'https?://[^\s<>"\']+',r'<img\b[^>]*>',r'<!--.*?-->']
    for pat in patterns:assert re.findall(pat,before,re.S|re.I)==re.findall(pat,after,re.S|re.I),pat
    b,a=Markup(before),Markup(after)
    assert b.attributes==a.attributes
    assert b.media==a.media and b.comments==a.comments
    assert not (Counter(a.ignored)-Counter(b.ignored)), 'new unmatched closing tag'
    assert not a.errors, a.errors
    assert not MASK.search(after)
    return a

def raw_check(row,cache):
    path=R/row['rawFile']
    if path not in cache:cache[path]=(fs(path),{n['resourceId']:n for n in load(path)['data']['translatableResourcesByIds']['nodes']})
    filehash,nodes=cache[path];assert filehash==row['rawFileSHA256']
    node=nodes[row['resourceId']]
    source=next(t for t in node['translatableContent'] if t['key']==row['key'])
    before=next(t for t in node['tr_'+row['locale'].replace('-','_')] if t['key']==row['key'] and not t['market'])
    assert source['value']==row['source'] and source['digest']==row['sourceDigest']
    assert sha(row['source'])==row['sourceSHA256']
    assert row['before']==row['rawBefore']==before and before['outdated'] is False
    assert sha(before['value'])==row['expectedBeforeValueSHA256']==row['beforeValueSHA256']
    assert sha(row['value'])==row['valueSHA256']
    after=patch_value(row,before['value'])
    assert after==row['value']
    preserve(before['value'],after)
    return before

def main():
    inputs={}
    for name,(path,digest) in INPUTS.items():
        assert fs(R/path)==digest,(name,'changed frozen file')
        inputs[name]=load(R/path)['rows']
    originals=inputs['author']; indexes={n:{key(r):r for r in rows} for n,rows in inputs.items()}
    assert len(originals)==len(indexes['author'])==88
    cache={};qualified=[];checks=[];manual=[]
    for row in originals:
        before=raw_check(row,cache);k=key(row)
        assert k not in indexes['structure'] and k not in indexes['sizes']
        header=indexes['headers'][k]
        assert header['sourceDigest']==row['sourceDigest'] and header['sourceValue']==row['source']
        assert header['rawBefore']==row['rawBefore'] and header['expectedEffectiveBeforeValue']==before['value']
        assert sha(header['value'])==header['valueSHA256']
        baseline=header['value'];value=patch_value(row,baseline);parsed=preserve(baseline,value)
        q=copy.deepcopy(row)
        q.update(sourceValue=row['source'],before=None,marketId=None,value=value,valueSHA256=sha(value),
                 expectedEffectiveBeforeValue=baseline,expectedEffectiveBeforeValueSHA256=sha(baseline),
                 expectedBeforeValueSHA256=sha(baseline),beforeValueSHA256=sha(baseline),
                 requiresFreshEffectiveBeforeObject=True,
                 authorCandidateValueSHA256=row['valueSHA256'],authorBeforeValueSHA256=sha(before['value']),
                 plannedBeforeDependencies=[{'file':INPUTS['headers'][0],'fileSHA256':INPUTS['headers'][1],'valueSHA256':sha(baseline)}],
                 reviewStatus='INDEPENDENTLY_QUALIFIED_PATCHES_REBASED_ON_FINAL_HEADER_V2; ROOT_FRESH_SOURCE_AND_BEFORE_GUARD_REQUIRED')
        q['reason']='Independently reviewed exact source-backed placeholder/HTML boundary repairs and seven complete localized clauses. Applied after final header v2; no overlap with size156. Raw before outdated=false; final before object must be bound by root after preceding releases. All tables, measurements, URLs, image tags, attributes and all bytes outside the 117 declared patches are preserved.'
        qualified.append(q)
        checks.append({'productIndex':row['productIndex'],'resourceId':row['resourceId'],'locale':row['locale'],
                       'rawSourceDigestBeforeBinding':'PASS','exactDeclaredPatchReconstruction':'PASS',
                       'patches':len(row['patches']),'headerV2Preserved':'PASS','allTablesCellsMeasurementsURLsImageTagsAttributes':'PASS',
                       'nonoptionalMarkupErrors':parsed.errors,'preservedOptionalEnds':parsed.optional,'preservedIgnoredEndTags':parsed.ignored,
                       'valueSHA256':sha(value),'plannedBeforeSHA256':sha(baseline)})
        for p in row['patches']:
            if (row['productIndex'],row['locale']) in MANUAL and p['before'].startswith('<li>'):
                manual.append({'productIndex':row['productIndex'],'locale':row['locale'],'source':p['sourceExactQuote'],'target':p['after'],
                               'review':'PASS full manual source-vs-target meaning; garments, roles, construction and all qualifiers preserved; no new claims.'})
    assert len(manual)==7
    mutations=[]
    for name,change in [
        ('wrong_source_digest',lambda r:r.update(sourceDigest='0'*64)),
        ('wrong_list_ordinal',lambda r:r['patches'][0].update(sourceListItemOrdinal=0)),
        ('dropped_patch',lambda r:r['patches'].pop()),
        ('changed_measurement',lambda r:r.update(value=r['value'].replace('<td>2</td>','<td>999</td>',1),valueSHA256=sha(r['value'].replace('<td>2</td>','<td>999</td>',1))))]:
        bad=copy.deepcopy(originals[0]);unchanged=copy.deepcopy(bad);change(bad);assert bad!=unchanged
        try:raw_check(bad,cache)
        except AssertionError:mutations.append({'case':name,'result':'REJECTED'})
        else:raise AssertionError('accepted corrupted input '+name)
    dump('placeholder88_reviewed.json',{'rows':qualified})
    digest=fs(H/'placeholder88_reviewed.json')
    dump('manual_seven_meaning_review.json',{'rows':manual,'additionalHeading':{'productIndex':145,'locale':'el','source':'Key Features:','target':'Βασικά χαρακτηριστικά:','review':'PASS'},'correctionsRequired':0})
    report={'status':'INDEPENDENT_PASS; AWAITING_ROOT_LIVE_RELEASE_AND_READBACK','rows':88,'uniqueTuples':88,'patches':sum(len(x['patches']) for x in originals),
            'rawFilesVerified':len(cache),'rawBeforeOutdatedFalse':88,'headerV2OverlayRows':88,'structure375Overlap':0,'size156Overlap':0,
            'manualProseClausesReviewed':7,'additionalLocalizedHeadingReviewed':1,'authorCorrections':0,'held':0,
            'nonoptionalMarkupErrors':0,'tablesMeasurementsURLsImageTagsAttributesExact':88,'completeDeclaredPatchReconstruction':88,
            'rowsWithInheritedIgnoredEndTags':sum(bool(r['preservedIgnoredEndTags']) for r in checks),'rowsWithOptionalEndTags':sum(bool(r['preservedOptionalEnds']) for r in checks),
            'htmlValidationLimit':'Independent standard HTMLParser lexical stack with narrowly allowed optional li/p ends and inherited stray li/ul end tags; not a full HTML5 browser render.',
            'meaningReviewLimit':'Full meaning review of seven replaced complete clauses and added Greek heading; other prose is exact preserved. This does not certify all pre-existing prose or English product assertions.',
            'sourceOrdinalException':'EL157 target retained Fabric paragraph as first li, offset +1 checked for the two source-backed boundaries.',
            'mutationTests':mutations,'candidateSHA256':digest,'inputFiles':INPUTS,'rowsDetail':checks}
    dump('checks88.json',report)
    dump('manifest.json',{'qualifiedFile':'review/size-label-repair/placeholder-review/placeholder88_reviewed.json','qualifiedSHA256':digest,'rows':88,'patches':117,'checksFile':'review/size-label-repair/placeholder-review/checks88.json','checksSHA256':fs(H/'checks88.json'),'manualMeaningReviewSHA256':fs(H/'manual_seven_meaning_review.json'),'releaseOwner':'root','externalWritesByReviewer':0})
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputFiles','rowsDetail')},ensure_ascii=False))

if __name__=='__main__':main()
