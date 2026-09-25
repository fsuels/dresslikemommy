# -*- coding: utf-8 -*-
"""Independent exact-patch validation; does not import or execute author code."""
import copy, hashlib, html, json, re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
H = Path(__file__).resolve().parent
R = H.parents[1]
I = R/'review/body-structure-audit'
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
file_sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
dump = lambda n, d: (H/n).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n')
MAP = {
'ar': {'ديف':'div','لي':'li','معرف':'table','الرأس':'thead','تر':'tr','الجسم':'tbody','الجدول':'table','ح3':'h3'},
'hi': {'ली':'li','तालिका':'table','सिर':'thead'},
'it': {'testa':'thead','corpo':'tbody','tcorpo':'tbody','tabella':'table','immagine':'img'},
'ja': {'リ':'li','頭':'thead','本体':'tbody','テーブル':'table','オル':'ol'},
'ko': {'리':'li','테이블':'table','머리':'thead','몸':'tbody'},
'nl': {'thoofd':'thead','tlichaam':'tbody','tabel':'table'},
'pl': {'głowa':'thead','ciało':'tbody','tabela':'table'},
'pt-BR': {'corpo':'tbody','tabela':'table'},
'ru': {'дел':'div','ул':'ul','ли':'li','голова':'thead','тр':'tr','тело':'tbody','тд':'td','таблица':'table'}
}
JA = [('調節可能なネクタイ:', '調節可能な首の結びひも:'),('調節可能なネクタイで','調節可能な首の結びひもで'),('ホルターネックの調節可能なネクタイにより','ホルターネックの調節可能な結びひもにより')]
JA_QUOTES = ['Adjustable Neck Tie:', 'Find your perfect fit with the adjustable neck tie, designed to provide both comfort and secure support throughout all your aquatic adventures.', "The halter's adjustable tie means that you're guaranteed a custom fit, making it perfect for those active in water sports or simply soaking up the sun."]
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
class Parsed(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=False);self.tokens=[];self.attrs=[];self.comments=[];self.feed(value)
    def handle_starttag(self, tag, attrs):
        self.tokens.append(tag);self.attrs.append((tag,attrs))
    def handle_endtag(self, tag): self.tokens.append('/'+tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)
    def handle_comment(self, data):self.comments.append(data)

def reconstructed(row):
    before=row['before']['value']; position=0;chunks=[]
    for rep in row['replacements']:
        old=rep['oldLiteral'];new=rep['newLiteral'];at=rep['beforePosition']
        assert position<=at and before[at:at+len(old)]==old
        head=re.match(r'<\s*/?\s*([^\s<>/]+)',old);assert head
        oldname=head.group(1);expected=None
        if oldname in ('thcolspan="5"','thcolspan="6"'):
            assert row['locale']=='ja';expected=old[:head.start(1)]+'th '+oldname[2:]+old[head.end(1):]
            assert rep['newName']=='th'
        else:
            name=MAP[row['locale']][oldname];assert rep['newName']==name
            expected=old[:head.start(1)]+name+old[head.end(1):]
            if row['locale']=='ar' and oldname=='معرف':
                assert re.fullmatch(r'<معرف الجدول = "[^"]+">',old), old
                expected=expected.replace(' الجدول =',' id =',1)
            if row['locale']=='hi' and oldname=='तालिका' and not old.lstrip().startswith('</'):
                assert re.fullmatch(r'<तालिका आईडी = "[^"]+">',old),old
                expected=expected.replace(' आईडी =',' id =',1)
        assert new==expected,(row['locale'],old,new,expected)
        chunks.extend([before[position:at],expected]);position=at+len(old)
    chunks.append(before[position:]);tag_only=''.join(chunks);value=tag_only
    if row['productIndex']==5 and row['locale']=='ja':
        source_text=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',row['source']))).strip()
        for quote in JA_QUOTES:assert quote in source_text
        assert len(row['proseExceptions'])==3
        for rule,(old,new) in zip(row['proseExceptions'],JA):
            assert rule['before']==old and rule['after']==new and value.count(old)==1
            value=value.replace(old,new,1)
    else:assert not row['proseExceptions']
    return tag_only,value

def verify(row, raw_cache, inventory):
    key=(row['resourceId'],row['locale'])
    inv=inventory[key]
    assert not inv['overlayApplied']
    for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']:
        assert row[k]==inv[k],(key,k)
    assert row['before']['outdated'] is False and row['before']==row['rawBefore']
    p=R/row['rawFile'];assert file_sha(p)==row['rawFileSHA256']
    if p not in raw_cache:raw_cache[p]=load(p)
    node=next(n for n in raw_cache[p]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==row['resourceId'])
    source=next(x for x in node['translatableContent'] if x['key']=='body_html')
    tr=next(x for x in node['tr_'+row['locale'].replace('-','_')] if x['key']=='body_html')
    assert source['value']==row['source'] and source['digest']==row['sourceDigest']
    assert tr==row['before']
    assert row['sourceSHA256']==sha(row['source']) and row['beforeValueSHA256']==sha(tr['value'])==row['expectedBeforeValueSHA256']
    tag_only,value=reconstructed(row)
    assert sha(tag_only)==row['tagOnlyValueSHA256']
    assert value==row['value'] and sha(value)==row['valueSHA256']
    # Every changed token has an exact corresponding source token, checked by a separate standard HTML parser.
    source_tokens=Parsed(row['source']).tokens
    for rep in row['replacements']:
        idx=rep['alignedSourceTokenIndex'];assert idx is not None and source_tokens[idx]==rep['sourceToken']
    # These are independent redundant preservation checks, in addition to exact byte reconstruction.
    text=lambda s:re.sub(r'<[^>]*>','',s)
    assert text(tr['value'])==text(tag_only)
    assert re.findall(r'\d+(?:[.,]\d+)?',tr['value'])==re.findall(r'\d+(?:[.,]\d+)?',value)
    assert re.findall(r'https?://[^\s<>"\']+',tr['value'])==re.findall(r'https?://[^\s<>"\']+',value)
    assert re.findall(r'=\s*(["\'])(.*?)\1',tr['value'])==re.findall(r'=\s*(["\'])(.*?)\1',value)
    assert re.findall(r'<!--.*?-->',tr['value'],re.S)==re.findall(r'<!--.*?-->',value,re.S)
    return {'productIndex':row['productIndex'],'resourceId':row['resourceId'],'locale':row['locale'],'binding':'PASS','exactAllowedBytePatch':'PASS','sourceParserTokenProof':'PASS','textNumericURLAttributeValuesComments':'PASS','occurrences':len(row['replacements'])}

if __name__=='__main__':
    path=I/'tag_candidates_v1.json';assert file_sha(path)=='ad256696f17797e8e22390d6eff04a91022cccb5c3ce84627265472611a23050'
    rows=load(path)['rows'];inventory={(x['resourceId'],x['locale']):x for x in load(I/'effective_body_inventory.json')['rows']}
    raw_cache={};checks=[verify(x,raw_cache,inventory) for x in rows]
    assert len(rows)==374==len({(x['resourceId'],x['locale']) for x in rows})
    negatives=[]
    for kind,mutate in [('measurement',lambda x:x.update(value=x['value'].replace('80-100','81-100',1))),('attribute_value',lambda x:x.update(value=x['value'].replace('حجم الرسم البياني','changed-id',1))),('wrong_tag',lambda x:x['replacements'][0].update(newLiteral='<p>'))]:
        x=copy.deepcopy(rows[0]);old=json.dumps(x);mutate(x);assert json.dumps(x)!=old
        try:verify(x,raw_cache,inventory)
        except AssertionError:negatives.append({'case':kind,'result':'REJECTED_AS_EXPECTED'})
        else:raise AssertionError('corrupt candidate passed '+kind)
    samples={}
    for x in rows:
        for rep in x['replacements']:
            k=(x['locale'],rep['oldName'],rep['newName'])
            if k not in samples:samples[k]={'locale':k[0],'old':k[1],'new':k[2],'productIndex':x['productIndex'],'oldLiteral':rep['oldLiteral'],'newLiteral':rep['newLiteral'],'sourceTokenIndex':rep['alignedSourceTokenIndex']}
    residuals=[{'productIndex':x['productIndex'],'resourceId':x['resourceId'],'locale':x['locale']} for x in rows if x['checks']['afterBalancedness']['unbalancedCounts'] or x['checks']['afterBalancedness']['nestingIssueCount'] or x['checks']['afterBalancedness']['unclosedStack']]
    out={'status':'V1_INDEPENDENT_PARITY_PASS_AWAIT_V2_SEVEN_EXPLICIT_RESIDUAL_REPAIRS','inputFile':str(path.relative_to(R)),'inputSHA256':file_sha(path),'reviewed':len(rows),'allExactBindingsAndAllowedPatches':'PASS','replacedTokens':sum(x['occurrences'] for x in checks),'independentlyReviewedRuleSamples':list(samples.values()),'negativeMutationTests':negatives,'rows':checks,'v2PendingResidualRows':residuals,'JapaneseP5MeaningReview':'All three formal necktie references corrected to halter neck tying cords, preserving the complete surrounding meaning. Exact source quotes independently verified.','limitation':'Structural scope only. Existing prose and numbers are preserved, not certified as factually accurate or completely translated. Author v2 will separately address the seven known residual malformed elements.'}
    dump('body_structure_v1_independent_checks.json',out)
    print(json.dumps({'rows':len(rows),'tokens':out['replacedTokens'],'ruleSamples':len(samples),'negativeTests':negatives,'residuals':residuals},ensure_ascii=False))
